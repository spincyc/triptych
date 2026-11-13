"""An indexed reading session and disposable, dependency-bound projections."""
from __future__ import annotations

import base64
from collections import OrderedDict
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
    CACHE_VERSION = 2

    def __init__(self, root: Path):
        self.root = Path(root)
        self.index = CorpusIndex(self.root)
        self._cancelled = threading.Event()
        self.index._reader_cancelled = self._cancelled
        self.cache = self.root / ".scratch/reader-data"
        self._memory: OrderedDict[str, bytes] = OrderedDict()
        self._size = 0
        self._code: str | None = None

    def _code_identity(self) -> str:
        if self._code is None:
            digest = hashlib.sha256()
            paths = set()
            for prefix in ("scripts/", "tools/", "src/web/browser/"):
                paths.update(self.index.paths(prefix=prefix))
            for name in sorted(paths):
                if "/tests/" in name or name.endswith((".md", ".test")):
                    continue
                digest.update(name.encode("utf-8") + b"\0")
                digest.update(str(self.index.metadata(name)).encode("utf-8") + b"\n")
            for name in self.index.paths(prefix="requirements"):
                if "/" not in name:
                    digest.update(name.encode("utf-8") + b"\0")
                    digest.update(str(self.index.metadata(name)).encode("utf-8") + b"\n")
            # Publication revision stamps also depend on commit history.
            revision = subprocess.run(["git", "-C", str(self.root), "rev-parse", "HEAD"],
                                      capture_output=True, check=True).stdout
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
        try:
            if target.is_symlink():
                raise ValueError("unsafe reader cache")
            held = json.loads(target.read_bytes())
            if (held["version"] != self.CACHE_VERSION or held["path"] != name
                    or held["code"] != code
                    or held.get("membership") != self.index.membership_identity
                    or not isinstance(held["inputs"], dict)):
                raise ValueError("reader cache identity changed")
            for source, expected in held["inputs"].items():
                # Verification reads the actual source bytes, including changes
                # whose size and timestamp were restored outside Git.
                if hashlib.sha256(self.index.read(source)).hexdigest() != expected:
                    raise ValueError("reader cache input changed")
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
        entry = {"version": self.CACHE_VERSION, "path": name, "code": code,
                 "membership": self.index.membership_identity,
                 "inputs": dict(inputs), "sha256": hashlib.sha256(body).hexdigest(),
                 "body": base64.b64encode(body).decode("ascii")}
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
def indexed_products(root: Path):
    reader = ReaderData(root)
    try:
        yield reader
    finally:
        reader.close()
