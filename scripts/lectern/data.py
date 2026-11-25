"""An indexed reading session and disposable, dependency-bound projections."""
from __future__ import annotations

import base64
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
import threading

from _corpus_index import CorpusIndex


class ReaderData:
    """Keep immutable consumed bytes, without preparing a corpus of products."""

    MEMORY_LIMIT = 32 * 1024 * 1024
    CACHE_VERSION = 3
    SIDECAR_THRESHOLD = 64 * 1024

    def __init__(self, root: Path, index: CorpusIndex | None = None):
        self.root = Path(root)
        # A caller that has just checked membership hands that index over, so
        # one session does not repeat the Git scan before its first read.
        self.index = index if index is not None else CorpusIndex(self.root)
        self._cancelled = threading.Event()
        self.index._reader_cancelled = self._cancelled
        self.cache = self.root / ".scratch/reader-data"
        self.index._reader_parse_cache_dir = self.cache / "parsed"
        self._memory: OrderedDict[str, bytes] = OrderedDict()
        self._size = 0
        self._code: str | None = None
        self._verified_batch: dict[str, str] | None = None
        self._batch_lock = threading.Lock()

    @contextmanager
    def batch_verification(self):
        """Deduplicate disk SHA-256 reads of identical inputs within one RPC."""
        previous = self._verified_batch
        if previous is not None:
            yield
            return
        self._verified_batch = {}
        try:
            yield
        finally:
            self._verified_batch = None

    def _verify_input_sha(self, source: str, expected: str) -> None:
        batch = self._verified_batch
        if batch is not None:
            with self._batch_lock:
                seen = batch.get(source)
            if seen is not None:
                if seen != expected:
                    raise ValueError("reader cache input changed")
                return
        # CorpusIndex.read already verifies disk bytes against its indexed
        # SHA-256; avoid hashing the same buffer twice when unpatched.
        if type(self.index).read is CorpusIndex.read:
            self.index.read(source)
            actual = self.index._file_row(source)[1]
        else:
            actual = hashlib.sha256(self.index.read(source)).hexdigest()
        if batch is not None:
            with self._batch_lock:
                batch[source] = actual
        if actual != expected:
            raise ValueError("reader cache input changed")

    def _verify_inputs(self, inputs: dict[str, str], meta_inputs: dict[str, str] | None = None) -> None:
        if meta_inputs:
            for source, expected in meta_inputs.items():
                if self.index.metadata(source)[0] != expected:
                    raise ValueError("reader cache metadata input changed")
        batch = self._verified_batch
        pending = []
        for source, expected in inputs.items():
            if batch is not None:
                seen = batch.get(source)
                if seen is not None:
                    if seen != expected:
                        raise ValueError("reader cache input changed")
                    continue
            pending.append((source, expected))
        if len(pending) < 8:
            for source, expected in pending:
                self._verify_input_sha(source, expected)
            return
        # Pre-load referenced index shards and validate any reader-surface
        # proof on the caller thread so workers only perform GIL-free disk
        # reads and OpenSSL SHA-256 verification.
        if type(self.index).read is CorpusIndex.read:
            threaded = []
            for source, expected in pending:
                if source.startswith("src/index/"):
                    self._verify_input_sha(source, expected)
                else:
                    self.index._file_row(source)
                    threaded.append((source, expected))
            pending = threaded
        if len(pending) < 8:
            for source, expected in pending:
                self._verify_input_sha(source, expected)
            return
        with ThreadPoolExecutor(max_workers=min(4, len(pending))) as pool:
            futures = [pool.submit(self._verify_input_sha, source, expected) for source, expected in pending]
            for future in futures:
                future.result()

    def _code_identity(self) -> str:
        if self._code is None:
            digest = hashlib.sha256()
            paths = set()
            for prefix in ("scripts/", "tools/", "src/web/browser/"):
                paths.update(self.index.paths(prefix=prefix))
            metadata = self.index.metadata
            for name in sorted(paths):
                if "/tests/" in name or name.endswith((".md", ".test")):
                    continue
                digest.update(name.encode("utf-8") + b"\0")
                digest.update(str(metadata(name)).encode("utf-8") + b"\n")
            for name in self.index.paths(prefix="requirements"):
                if "/" not in name:
                    digest.update(name.encode("utf-8") + b"\0")
                    digest.update(str(metadata(name)).encode("utf-8") + b"\n")
            # Publication revision stamps also depend on commit history.
            env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0", "GIT_NO_LAZY_FETCH": "1"}
            revision = subprocess.run(["git", "-C", str(self.root), "rev-parse", "HEAD"],
                                      capture_output=True, check=True, env=env).stdout
            digest.update(revision)
            self._code = digest.hexdigest()
        return self._code

    @staticmethod
    def _name(relative: str) -> str:
        if not isinstance(relative, str) or not relative or "\\" in relative:
            raise ValueError("invalid reader data path")
        path = PurePosixPath(relative)
        if path.is_absolute() or any(part in ("", ".", "..") for part in relative.split("/")):
            raise ValueError("invalid reader data path")
        if path.suffix != ".json":
            raise ValueError("reader data must name a JSON record")
        return relative

    def _remember(self, name: str, body: bytes) -> bytes:
        if len(body) <= self.MEMORY_LIMIT:
            self._memory[name] = body
            self._size += len(body)
            while self._size > self.MEMORY_LIMIT:
                _, evicted = self._memory.popitem(last=False)
                self._size -= len(evicted)
        return body

    def read(self, relative: str) -> bytes | None:
        if self._cancelled.is_set():
            raise ValueError("reading was cancelled")
        name = self._name(relative)
        if name in self._memory:
            self._memory.move_to_end(name)
            return self._memory[name]
        if name == "structure/documents/corpus.json" or name.startswith("web-editions/"):
            from _reader_publication_products import verify_history
            verify_history(self.root, self.index)
        code = self._code_identity()
        key = hashlib.sha256(name.encode("utf-8")).hexdigest()
        target = self.cache / (key + ".json")
        sidecar_name = key + ".bin"
        try:
            if target.is_symlink():
                raise ValueError("unsafe reader cache")
            held = json.loads(target.read_bytes())
            if (held["version"] != self.CACHE_VERSION or held["path"] != name
                    or held["code"] != code
                    or held.get("membership") != self.index.membership_identity
                    or not isinstance(held["inputs"], dict)):
                raise ValueError("reader cache identity changed")
            meta_inputs = held.get("meta_inputs")
            if meta_inputs is not None and not isinstance(meta_inputs, dict):
                raise ValueError("reader cache metadata invalid")
            self._verify_inputs(held["inputs"], meta_inputs)
            if "body_file" in held:
                if "body" in held or held["body_file"] != sidecar_name:
                    raise ValueError("reader cache body reference invalid")
                sidecar = self.cache / sidecar_name
                if sidecar.is_symlink():
                    raise ValueError("unsafe reader cache body")
                body = sidecar.read_bytes()
            else:
                body = base64.b64decode(held["body"], validate=True)
            if hashlib.sha256(body).hexdigest() != held["sha256"]:
                raise ValueError("reader cache bytes changed")
            return self._remember(name, body)
        except (OSError, ValueError, KeyError, TypeError):
            # A disposable projection is rebuilt from verified canonical data;
            # it never supplies missing source text or repairs the tracked index.
            pass

        from _reader_products import resolve

        with self.index.verified_reads() as inputs:
            body = resolve(name, self.root, self.index)
        if body is None:
            return None
        if not isinstance(body, bytes):
            raise TypeError("reader producer did not return bytes")
        # Catch malformed output before it can become a reusable projection.
        json.loads(body)
        self.cache.mkdir(parents=True, exist_ok=True)
        meta_only = getattr(self.index, "_last_metadata_only", None)
        body_inputs = dict(inputs)
        meta_inputs = {}
        if isinstance(meta_only, dict) and meta_only:
            for source, digest in meta_only.items():
                if source in body_inputs:
                    meta_inputs[source] = body_inputs.pop(source)
        entry = {"version": self.CACHE_VERSION, "path": name, "code": code,
                 "membership": self.index.membership_identity,
                 "inputs": body_inputs,
                 "sha256": hashlib.sha256(body).hexdigest()}
        if meta_inputs:
            entry["meta_inputs"] = meta_inputs
        if len(body) > self.SIDECAR_THRESHOLD:
            temporary_bin = None
            try:
                with tempfile.NamedTemporaryFile(mode="wb", dir=self.cache,
                                                 prefix=".projection-body-", delete=False) as stream:
                    temporary_bin = Path(stream.name)
                    stream.write(body)
                os.replace(temporary_bin, self.cache / sidecar_name)
                temporary_bin = None
            finally:
                if temporary_bin is not None:
                    temporary_bin.unlink(missing_ok=True)
            entry["body_file"] = sidecar_name
        else:
            entry["body"] = base64.b64encode(body).decode("ascii")
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.cache,
                                             prefix=".projection-", delete=False) as stream:
                temporary = Path(stream.name)
                json.dump(entry, stream, ensure_ascii=False, separators=(",", ":"))
            os.replace(temporary, target)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        return self._remember(name, body)

    def close(self) -> None:
        self.cancel()
        self._memory.clear()
        self._size = 0

    def cancel(self) -> None:
        self._cancelled.set()


@contextmanager
def indexed_products(root: Path, index: CorpusIndex | None = None):
    reader = ReaderData(root, index)
    try:
        yield reader
    finally:
        reader.close()
