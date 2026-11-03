"""Exact native TeX software, packages and fonts for a static browser compiler.

The tracked manifest supplies byte identity. Release archives are delivery only;
ordinary lookup and publication never fetch or execute a renderer. Hydration is
an explicit operation and never accepts a partial, changed or unsafe archive.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tarfile
import tempfile
from urllib.parse import urlsplit

import _artifact_store as transport

INDEX_PATH = "src/common/native-tex-runtime.json"
SCHEMA = "triptych-native-tex-runtime/v1"
DELIVERY_SCHEMA = "triptych-native-tex-delivery/v1"
PUBLIC_KEYS = ("schema", "id", "engines", "texFiles", "texMissing", "notices", "correspondingSource")
KINDS = ("engine-software", "tex-package", "font-software", "license-notice", "runtime-metadata")
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


class AssetError(ValueError):
    """Native software metadata or exact delivered bytes are invalid."""


def digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def canonical_json(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _need(condition, message):
    if not condition:
        raise AssetError(message)


def _hash(value):
    _need(isinstance(value, str) and _HASH.fullmatch(value), "invalid native TeX SHA-256")


def _url(value):
    parsed = urlsplit(value) if isinstance(value, str) else None
    _need(parsed is not None and parsed.scheme == "https" and parsed.netloc
          and not parsed.username and not parsed.password and not parsed.query
          and not parsed.fragment, "native TeX delivery requires a public HTTPS URL")


def _size(value):
    _need(type(value) is int and 0 < value <= transport.MAX_ARCHIVE_BYTES,
          "invalid native TeX byte extent")


def _key(row):
    _need(isinstance(row, dict) and type(row.get("format")) is int
          and 0 <= row["format"] <= 100, "invalid native TeX lookup format")
    name = row.get("name")
    _need(isinstance(name, str) and name and name not in {".", ".."}
          and not any(c in name for c in "/\\\x00?#%") and all(ord(c) >= 32 for c in name),
          "native TeX lookup must name one plain file")
    return row["format"], name


def validate_index(data):
    """Validate complete membership and bindings without opening any payload."""
    required = {*PUBLIC_KEYS, "registry_sha256", "upstream", "payloads", "delivery"}
    _need(isinstance(data, dict) and set(data) == required and data["schema"] == SCHEMA,
          "invalid native TeX registry fields or schema")
    _need(isinstance(data["id"], str) and _ID.fullmatch(data["id"]), "invalid native TeX runtime ID")
    _hash(data["registry_sha256"])
    _need(data["registry_sha256"] == digest(canonical_json(
        {key: value for key, value in data.items() if key != "registry_sha256"})),
        "native TeX registry digest mismatch")
    _need(isinstance(data["upstream"], dict) and bool(data["upstream"]), "missing native TeX provenance")
    prefix = "native-tex/" + data["id"] + "/"
    payloads = data["payloads"]
    _need(isinstance(payloads, dict) and bool(payloads), "empty native TeX payload registry")
    for path, row in payloads.items():
        transport._relative(path)
        _need(path.startswith(prefix) and not any(c in path for c in "%?#")
              and not path.lower().endswith((".pdf", ".ps")),
              "native TeX payload escapes its runtime or contains a print output")
        _need(isinstance(row, dict) and set(row) == {"sha256", "bytes", "media_type", "kind"},
              "invalid native TeX payload record")
        _hash(row["sha256"]); _size(row["bytes"])
        _need(row["kind"] in KINDS and isinstance(row["media_type"], str)
              and re.fullmatch(r"[\w.+-]+/[\w.+-]+", row["media_type"]),
              "invalid native TeX payload kind or media type")
    transport.validate_delivery_index(data["delivery"], schema=DELIVERY_SCHEMA,
                                      kinds=KINDS, path_prefix=prefix)
    for archive in data["delivery"]["archives"]:
        for url in archive["urls"]:
            _url(url)
    entries = {row["path"]: row for row in data["delivery"]["artifacts"]}
    _need(entries.keys() == payloads.keys(), "native TeX payload/delivery membership differs")
    for path, row in payloads.items():
        _need(all(entries[path][key] == value for key, value in row.items()),
              "native TeX payload/delivery byte identity differs")
    used = set()

    def reference(row):
        _need(isinstance(row, dict) and set(row) == {"url", "sha256", "bytes"},
              "invalid native TeX public byte reference")
        url = row["url"]
        _need(url in payloads and all(row[key] == payloads[url][key] for key in ("sha256", "bytes")),
              "native TeX reference does not bind a registered payload")
        used.add(url)

    _need(isinstance(data["engines"], dict) and set(data["engines"]) == {"pdflatex", "xelatex", "dvipdfmx"},
          "native TeX requires its declared pdfTeX, XeTeX and PDF converter")
    for engine, files in data["engines"].items():
        roles = {"worker", "core", "wasm"} | ({"format"} if engine != "dvipdfmx" else set())
        optional = {"support"} | ({"icu"} if engine == "xelatex" else set())
        _need(isinstance(files, dict) and roles <= files.keys()
              and not files.keys() - roles - optional, "incomplete native TeX engine files")
        for role, row in files.items():
            if role == "support":
                _need(isinstance(row, list), "invalid native TeX support scripts")
                for support in row:
                    reference(support)
                    _need(support["url"].endswith(".js")
                          and payloads[support["url"]]["kind"] == "engine-software",
                          "invalid native TeX support script")
                continue
            reference(row)
            _need(payloads[row["url"]]["kind"] == "engine-software", "engine role names a non-engine payload")
            extension = (".js" if role in {"worker", "core"} else ".wasm" if role == "wasm"
                         else ".dat" if role == "icu" else (".fmt", ".fmt.gz"))
            _need(row["url"].endswith(extension), "native TeX engine file has the wrong type")
    _need(isinstance(data["texFiles"], list) and isinstance(data["texMissing"], list),
          "invalid native TeX lookup arrays")
    found = set()
    for row in data["texFiles"]:
        _need(isinstance(row, dict) and set(row) == {"format", "name", "url", "sha256", "bytes"},
              "invalid native TeX file lookup")
        key = _key(row)
        _need(key not in found, "duplicate native TeX lookup")
        found.add(key)
        reference({k: row[k] for k in ("url", "sha256", "bytes")})
        _need(row["url"] == prefix + "tex/" + row["sha256"] + ".bin"
              and payloads[row["url"]]["kind"] in {"tex-package", "font-software"},
              "native TeX package lookup is not content addressed")
    absent = set()
    for row in data["texMissing"]:
        _need(isinstance(row, dict) and set(row) == {"format", "name"}, "invalid native TeX absence lookup")
        key = _key(row)
        _need(key not in found and key not in absent, "contradictory or duplicate native TeX absence")
        absent.add(key)
    _need(isinstance(data["notices"], list) and bool(data["notices"]), "native TeX requires redistribution notices")
    notices = set()
    for row in data["notices"]:
        reference(row)
        _need(row["url"] not in notices and payloads[row["url"]]["kind"] in {"license-notice", "runtime-metadata"},
              "invalid or duplicate native TeX notice")
        notices.add(row["url"])
    _need(used == payloads.keys(), "native TeX registry contains unreferenced payloads")
    source = data["correspondingSource"]
    _need(isinstance(source, dict) and set(source) == {"url", "sha256", "bytes"},
          "missing complete corresponding-source offer")
    _url(source["url"]); _hash(source["sha256"]); _size(source["bytes"])


def load_index(root: Path | str) -> dict:
    try:
        data = json.loads(transport._path(Path(root), INDEX_PATH).read_text(encoding="utf-8"),
                          object_pairs_hook=transport._unique_keys)
        validate_index(data)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, AttributeError) as error:
        raise AssetError("invalid native TeX registry: " + str(error)) from error
    return data


def public_manifest(root: Path | str) -> dict:
    data = load_index(root)
    return copy.deepcopy({key: data[key] for key in PUBLIC_KEYS})


def _cache(root, cache_root):
    path = Path(cache_root) if cache_root is not None else Path(root) / ".scratch/native-tex-runtime"
    if not path.is_absolute():
        path = Path(root) / path
    _need(not path.is_symlink() and not any(p.is_symlink() for p in path.parents),
          "native TeX cache may not traverse symlinks")
    return path


def _cached(cache, url, row):
    return transport._path(cache, "objects/" + row["sha256"] + "/" + Path(url).name)


def _verified_payload(path, row):
    path = transport._verify(path, row)
    if row["media_type"] == "application/wasm":
        with path.open("rb") as stream:
            _need(stream.read(8) == b"\0asm\x01\0\0\0", "invalid native TeX WASM header")
    return path


def payload_paths(root: Path | str, cache_root: Path | str | None = None) -> dict[str, Path]:
    """Return the complete authenticated local payload set, offline only."""
    data = load_index(root)
    cache = _cache(root, cache_root)
    result = {}
    for url, row in data["payloads"].items():
        path = _verified_payload(_cached(cache, url, row), dict(row, path=url))
        result[url] = path
    return result


def payload_path(root, url, cache_root=None):
    """Read one declared object without fetching or accepting a changed cache."""
    data = load_index(root)
    _need(url in data["payloads"], "unknown native TeX payload")
    row = data["payloads"][url]
    return _verified_payload(_cached(_cache(root, cache_root), url, row), dict(row, path=url))


def _hydrate_archive(local, members, cache):
    """Stage all authenticated regular members before promoting any object."""
    expected = {row["member"]: row for row in members}
    cache.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".hydrate-", dir=cache))
    seen = set()
    staged = []
    try:
        with tarfile.open(local, "r:") as archive:
            for member in archive:
                name = transport._relative(member.name)
                _need(name in expected and name not in seen and member.isreg() and not member.linkname,
                      "unregistered, duplicate or unsafe native TeX archive member")
                row = expected[name]
                _need(member.size == row["bytes"], "native TeX archive member extent differs")
                target = stage / str(len(seen))
                stream = archive.extractfile(member)
                _need(stream is not None, "unreadable native TeX archive member")
                with stream, target.open("wb") as output:
                    shutil.copyfileobj(stream, output, length=1024 * 1024)
                _verified_payload(target, row)
                seen.add(name)
                staged.append((target, row))
        _need(seen == expected.keys(), "native TeX archive is missing registered members")
        return stage, staged
    except BaseException:
        shutil.rmtree(stage)
        raise


def hydrate(root: Path | str, cache_root=None, archive_dir=None, fetch=False) -> dict:
    """Explicitly materialize exact archives; reject corrupt existing objects."""
    root = Path(root).resolve()
    data = load_index(root)
    cache = _cache(root, cache_root)
    missing = set()
    for url, row in data["payloads"].items():
        try:
            transport._verify(_cached(cache, url, row), dict(row, path=url))
        except FileNotFoundError:
            missing.add(url)
    hydrated = 0
    for archive in data["delivery"]["archives"]:
        members = [row for row in data["delivery"]["artifacts"] if row["archive"] == archive["id"]]
        if not missing.intersection(row["path"] for row in members):
            continue
        local = transport._archive_path(root, archive, Path(archive_dir) if archive_dir else None, fetch)
        stage, staged_members = _hydrate_archive(local, members, cache)
        try:
            for staged, row in staged_members:
                if row["path"] not in missing:
                    continue
                target = _cached(cache, row["path"], row)
                target.parent.mkdir(parents=True, exist_ok=True)
                transport._verify(staged, row)
                os.replace(staged, target)
                missing.remove(row["path"])
                hydrated += 1
        finally:
            shutil.rmtree(stage)
    files = payload_paths(root, cache_root=cache)
    return {"status": "verified", "runtime": data["id"], "files": len(files), "hydrated": hydrated,
            "bytes": sum(path.stat().st_size for path in files.values())}


def publish(root, site_root, cache_root=None):
    """Copy verified payloads into an isolated static artifact, without network."""
    result = {}
    data = load_index(root)
    for url, source in payload_paths(root, cache_root).items():
        target = transport._path(Path(site_root), url)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        transport._verify(target, dict(data["payloads"][url], path=url))
        result[url] = {"sha256": transport._digest(target), "bytes": target.stat().st_size}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "hydrate"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--cache-root", type=Path)
    parser.add_argument("--archive-dir", type=Path)
    parser.add_argument("--fetch", action="store_true", help="explicitly fetch declared exact public archives")
    args = parser.parse_args(argv)
    if args.command == "check":
        if args.fetch:
            parser.error("check never fetches; omit --fetch")
        data = load_index(args.root)
        files = payload_paths(args.root, args.cache_root)
        result = {"status": "verified", "runtime": data["id"], "files": len(files)}
    else:
        result = hydrate(args.root, args.cache_root, args.archive_dir, args.fetch)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
