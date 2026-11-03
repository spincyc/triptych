"""Import an optional, pinned browser-cache candidate pack; never approve outputs."""
from __future__ import annotations

import argparse
import ctypes
import errno
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

sys.dont_write_bytecode = True
import _browser_products as products

SCHEMA = "triptych-browser-products-bootstrap/v1"
METADATA = ".github/browser-products-bootstrap.json"
MARKER = ".browser-products-cache-v1"
MAX_ARCHIVE_BYTES = 512 * 1024 * 1024
MAX_UNPACKED_BYTES = 1024 * 1024 * 1024
MAX_MEMBER_BYTES = 64 * 1024 * 1024
MAX_INDEX_BYTES = 1024 * 1024
MAX_HEADERS = 150_000
MAX_PAX_BYTES = 16 * 1024
MAX_PADDING_BYTES = 10_240
MAX_RAW_BYTES = MAX_UNPACKED_BYTES + MAX_HEADERS * 1024
DOWNLOAD_SECONDS = 180
REDIRECT_HOSTS = frozenset({"github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com", "github-releases.githubusercontent.com"})


class BootstrapError(ValueError):
    pass


class Unavailable(OSError):
    """An optional public delivery could not be opened; cold generation remains."""


def _need(condition, message):
    if not condition:
        raise BootstrapError(message)


def _regular(path: Path):
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    info = os.fstat(descriptor)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        os.close(descriptor)
        raise BootstrapError("bootstrap input must be a single regular file")
    return os.fdopen(descriptor, "rb")


def metadata(path: Path):
    with _regular(path) as handle:
        raw = handle.read(MAX_INDEX_BYTES + 1)
    _need(len(raw) <= MAX_INDEX_BYTES, "bootstrap metadata is too large")
    value = products._decode(raw)
    _need(isinstance(value, dict) and set(value) == {"schema", "archive"} and value["schema"] == SCHEMA,
          "unsupported bootstrap metadata schema or fields")
    archive = value["archive"]
    if archive is None:
        return None
    _need(isinstance(archive, dict) and set(archive) == {"url", "sha256", "bytes", "unpacked_bytes"},
          "unsupported bootstrap archive fields")
    _need(isinstance(archive["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", archive["sha256"]), "invalid bootstrap SHA-256")
    for field, limit in (("bytes", MAX_ARCHIVE_BYTES), ("unpacked_bytes", MAX_UNPACKED_BYTES)):
        _need(type(archive[field]) is int and 0 < archive[field] <= limit, "invalid bootstrap " + field)
    _need(isinstance(archive["url"], str), "invalid bootstrap URL")
    url = urllib.parse.urlsplit(archive["url"])
    _need(url.scheme == "https" and url.netloc == "github.com" and not url.query and not url.fragment
          and re.fullmatch(r"/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/releases/download/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\.tar\.gz", url.path)
          and "/latest/" not in url.path, "bootstrap URL must name an immutable public GitHub release asset")
    return archive


class _Redirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 4

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlsplit(newurl)
        _need(parsed.scheme == "https" and parsed.hostname in REDIRECT_HOSTS and not parsed.username
              and not parsed.password and parsed.port in (None, 443), "unsafe bootstrap redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _copy_checked(source, destination: Path, declaration: dict):
    digest, size = hashlib.sha256(), 0
    deadline = time.monotonic() + DOWNLOAD_SECONDS
    with destination.open("xb") as target:
        while True:
            _need(time.monotonic() <= deadline, "bootstrap download exceeded its time limit")
            body = source.read(min(65536, declaration["bytes"] - size + 1))
            if not body:
                break
            size += len(body)
            _need(size <= declaration["bytes"], "bootstrap archive exceeds its declared byte extent")
            target.write(body)
            digest.update(body)
    _need(size == declaration["bytes"], "bootstrap archive has the wrong byte extent")
    _need(digest.hexdigest() == declaration["sha256"], "bootstrap archive SHA-256 mismatch")
    destination.chmod(0o400)


def download(declaration: dict, destination: Path):
    request = urllib.request.Request(declaration["url"], headers={"User-Agent": "Triptych-browser-cache-bootstrap", "Accept-Encoding": "identity"})
    try:
        response = urllib.request.build_opener(_Redirects()).open(request, timeout=30)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
        raise Unavailable("optional bootstrap delivery is unavailable") from error
    with response:
        declared = response.headers.get("Content-Length")
        if declared is not None:
            _need(declared.isdecimal() and int(declared) == declaration["bytes"], "bootstrap HTTP byte extent mismatch")
        try:
            _copy_checked(response, destination, declaration)
        except (OSError, EOFError) as error:
            raise BootstrapError("bootstrap delivery was interrupted") from error


class _Reader:
    def __init__(self, handle):
        self.handle, self.bytes = handle, 0

    def read(self, size):
        _need(size >= 0 and self.bytes + size <= MAX_RAW_BYTES, "bootstrap TAR exceeds its raw size limit")
        body = self.handle.read(size)
        self.bytes += len(body)
        return body

    def exact(self, size):
        body = self.read(size)
        _need(len(body) == size, "truncated bootstrap TAR")
        return body

    def padding(self, size):
        padding = (-size) % 512
        _need(self.exact(padding) == bytes(padding), "nonzero bootstrap TAR member padding")


def _pax_path(body: bytes):
    values, offset = {}, 0
    while offset < len(body):
        space = body.find(b" ", offset)
        _need(space > offset and space - offset <= 10 and body[offset:space].isdigit(), "invalid PAX record length")
        length = int(body[offset:space])
        end = offset + length
        _need(end <= len(body) and length > space - offset + 2 and body[end - 1:end] == b"\n", "invalid PAX record extent")
        record = body[space + 1:end - 1]
        key, separator, value = record.partition(b"=")
        _need(separator and key == b"path" and key not in values, "only one PAX path field is permitted")
        values[key] = value.decode("utf-8", errors="strict")
        offset = end
    _need(set(values) == {b"path"}, "PAX header must declare exactly one path")
    return values[b"path"]


def _member_path(value: str):
    products._relative(value)
    _need(len(value.encode("utf-8")) <= 4096 and all(len(part.encode("utf-8")) <= 255 for part in value.split("/")), "bootstrap member path is too long")
    if value in {MARKER, products.CANDIDATE_INDEX}:
        return value
    parts = value.split("/")
    _need(len(parts) >= 3 and re.fullmatch(r"[0-9a-f]{64}", parts[0]) and parts[1] == "data"
          and value.endswith(".json"), "bootstrap member is outside a candidate data envelope")
    return value


def extract(archive: Path, staging: Path, declaration: dict):
    seen, headers, unpacked, pending = set(), 0, 0, None
    with gzip.open(archive, "rb") as compressed:
        stream = _Reader(compressed)
        while True:
            block = stream.exact(512)
            if block == bytes(512):
                _need(stream.exact(512) == bytes(512) and pending is None, "invalid bootstrap TAR end marker")
                tail = 0
                while True:
                    body = stream.read(65536)
                    if not body:
                        break
                    tail += len(body)
                    _need(tail <= MAX_PADDING_BYTES and not any(body), "unexpected data after bootstrap TAR end")
                break
            headers += 1
            _need(headers <= MAX_HEADERS, "too many bootstrap TAR headers")
            _need(block[257:263] in {b"ustar\0", b"ustar "}, "bootstrap archive requires a POSIX TAR header")
            info = tarfile.TarInfo.frombuf(block, "utf-8", "strict")
            _need(type(info.size) is int and info.size >= 0, "invalid bootstrap member size")
            if info.type == tarfile.XHDTYPE:
                _need(pending is None and info.size <= MAX_PAX_BYTES, "invalid or oversized PAX header")
                pending = _pax_path(stream.exact(info.size))
                stream.padding(info.size)
                continue
            _need(info.type in {tarfile.REGTYPE, tarfile.AREGTYPE} and not info.linkname,
                  "bootstrap TAR may contain regular files only")
            name, pending = _member_path(pending if pending is not None else info.name), None
            _need(name not in seen, "duplicate bootstrap TAR member")
            seen.add(name)
            limit = MAX_INDEX_BYTES if name == products.CANDIDATE_INDEX else MAX_MEMBER_BYTES
            _need(info.size <= limit and (name != MARKER or info.size == 0), "oversized bootstrap member or invalid cache marker")
            unpacked += info.size
            _need(unpacked <= declaration["unpacked_bytes"], "bootstrap unpacked byte extent exceeded")
            destination = staging / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("xb") as target:
                remaining = info.size
                while remaining:
                    body = stream.exact(min(65536, remaining))
                    target.write(body)
                    remaining -= len(body)
            destination.chmod(0o644)
            stream.padding(info.size)
    _need(unpacked == declaration["unpacked_bytes"], "bootstrap unpacked byte extent mismatch")
    _need({MARKER, products.CANDIDATE_INDEX} <= seen, "bootstrap archive is missing root management metadata")
    index = products.load_candidate_index(staging)
    _need(index["entries"], "bootstrap archive contains no candidates")
    keys = {name.split("/", 1)[0] for name in seen - {MARKER, products.CANDIDATE_INDEX}}
    _need(keys == set(index["entries"]), "bootstrap payload keys differ from the candidate index")
    _need(len(seen) == 2 + sum(hint["count"] for hint in index["entries"].values()), "bootstrap file membership differs from its candidate index")
    for key, hint in index["entries"].items():
        products.validate_candidate_entry(staging, key, hint)
    return index


def _rename_absent(source_fd, destination_fd, name):
    library = ctypes.CDLL(None, use_errno=True)
    rename = getattr(library, "renameat2", None)
    _need(rename is not None, "atomic cache bootstrap requires Linux renameat2")
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(source_fd, os.fsencode(name), destination_fd, os.fsencode(name), 1):
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), name)


def merge(root: Path, staging: Path, cache: Path, incoming: dict):
    products._safe_directory(cache, create=True)
    existing_keys = products._cache_keys(cache)
    index = products.load_candidate_index(cache)
    for key, hint in incoming["entries"].items():
        previous = index["entries"].get(key)
        _need(previous is None or previous == hint, "existing candidate hint differs; refusing to repair it")
        if key in existing_keys:
            products.validate_candidate_entry(cache, key, hint)
    marker = cache / MARKER
    if os.path.lexists(marker):
        with _regular(marker) as handle:
            _need(handle.read(1) == b"", "invalid existing cache ownership marker")
    added = 0
    source_fd = os.open(staging, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    destination_fd = os.open(cache, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        _need(os.fstat(source_fd).st_dev == os.fstat(destination_fd).st_dev, "bootstrap staging and cache must share a filesystem")
        for key, hint in incoming["entries"].items():
            if key not in existing_keys:
                try:
                    _rename_absent(source_fd, destination_fd, key)
                    added += 1
                except OSError as error:
                    if error.errno != errno.EEXIST:
                        raise
                    products.validate_candidate_entry(cache, key, hint)
            index["entries"][key] = hint
        if not os.path.lexists(marker):
            descriptor = os.open(MARKER, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_NOFOLLOW, 0o644, dir_fd=destination_fd)
            os.close(descriptor)
        merged = staging / "merged-index.json"
        merged.write_text(json.dumps(index, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        os.replace(merged.name, products.CANDIDATE_INDEX, src_dir_fd=source_fd, dst_dir_fd=destination_fd)
    finally:
        os.close(source_fd)
        os.close(destination_fd)
    return added


def bootstrap(root: Path, metadata_path: Path, *, cache_root=None, archive: Path | None = None, fetch=False):
    _need(not (archive is not None and fetch), "choose a local archive or explicit fetching, not both")
    declaration = metadata(metadata_path)
    if declaration is None or archive is None and not fetch:
        return {"status": "unavailable", "reason": "no bootstrap configured or fetching not requested", "added": 0}
    scratch = products._safe_directory(root / ".scratch/cache-bootstrap-fix", create=True)
    with tempfile.TemporaryDirectory(prefix="bootstrap-", dir=scratch) as temporary:
        workspace = Path(temporary)
        downloaded = workspace / "candidate.tar.gz"
        if archive is not None:
            with _regular(archive) as source:
                _copy_checked(source, downloaded, declaration)
        else:
            try:
                download(declaration, downloaded)
            except Unavailable as error:
                return {"status": "unavailable", "reason": str(error), "added": 0}
        staging = workspace / "unpacked"
        staging.mkdir()
        incoming = extract(downloaded, staging, declaration)
        cache = products.cache_directory(root, cache_root)
        with products._cache_lock(root, cache_root, exclusive=True):
            added = merge(root, staging, cache, incoming)
        return {"status": "imported", "added": added, "preserved": len(incoming["entries"]) - added,
                "files": sum(hint["count"] for hint in incoming["entries"].values()),
                "bytes": sum(hint["bytes"] for hint in incoming["entries"].values()),
                "authority": "untrusted candidates; browser-products build must verify current inputs and outputs"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--metadata", type=Path, help="pinned metadata; default .github/browser-products-bootstrap.json")
    parser.add_argument("--cache-root", type=Path)
    delivery = parser.add_mutually_exclusive_group()
    delivery.add_argument("--archive", type=Path, help="verify a complete local pack without network access")
    delivery.add_argument("--fetch", action="store_true", help="explicitly fetch the optional public candidate pack")
    args = parser.parse_args(argv)
    try:
        root = products._safe_directory(args.root)
        result = bootstrap(root, args.metadata or root / METADATA, cache_root=args.cache_root, archive=args.archive, fetch=args.fetch)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (BootstrapError, products.ProductError, OSError, EOFError, tarfile.TarError, UnicodeError) as error:
        print("browser cache bootstrap: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
