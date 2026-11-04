"""Install only the web-edition converter pinned by its toolchain lock.

Network access requires --fetch. A local --archive uses the same immutable
package and binary checks without downloading or installing any TeX packages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import tarfile
import tempfile
import time
import tomllib
import urllib.parse
import urllib.request

LOCK = "src/common/web-edition-toolchain.toml"
MAX_ARCHIVE_BYTES = 128 * 1024 * 1024
MAX_BINARY_BYTES = 256 * 1024 * 1024
HOSTS = {"github.com", "release-assets.githubusercontent.com", "objects.githubusercontent.com",
         "github-releases.githubusercontent.com"}


class InstallError(ValueError):
    pass


def load_lock(root: Path) -> dict:
    try:
        value = tomllib.loads((root / LOCK).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise InstallError(f"invalid web-edition toolchain lock: {error}") from error
    if (set(value) != {"schema_version", "record_type", "pandoc"}
            or type(value["schema_version"]) is not int or value["schema_version"] != 1
            or value["record_type"] != "web-edition-toolchain"):
        raise InstallError("invalid web-edition toolchain lock fields")
    pin = value["pandoc"]
    fields = {"version", "archive_url", "archive_sha256", "archive_bytes",
              "binary_sha256", "binary_bytes", "member"}
    if not isinstance(pin, dict) or set(pin) != fields:
        raise InstallError("invalid pinned Pandoc fields")
    if not isinstance(pin["version"], str) or not re.fullmatch(r"[0-9]+\.[0-9]+(?:\.[0-9]+)?", pin["version"]):
        raise InstallError("invalid pinned Pandoc version")
    version = pin["version"]
    if (pin["archive_url"] != f"https://github.com/jgm/pandoc/releases/download/{version}/pandoc-{version}-linux-amd64.tar.gz"
            or pin["member"] != f"pandoc-{version}/bin/pandoc"):
        raise InstallError("Pandoc must use its exact official versioned release and binary")
    for field in ("archive_sha256", "binary_sha256"):
        if not isinstance(pin[field], str) or not re.fullmatch(r"[0-9a-f]{64}", pin[field]):
            raise InstallError(f"invalid pinned Pandoc {field}")
    for field, maximum in (("archive_bytes", MAX_ARCHIVE_BYTES), ("binary_bytes", MAX_BINARY_BYTES)):
        if type(pin[field]) is not int or not 0 < pin[field] <= maximum:
            raise InstallError(f"invalid pinned Pandoc {field}")
    return pin


class Redirects(urllib.request.HTTPRedirectHandler):
    max_redirections = 4

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlsplit(newurl)
        if (parsed.scheme != "https" or parsed.hostname not in HOSTS
                or parsed.username or parsed.password or parsed.port not in (None, 443)):
            raise InstallError("unsafe Pandoc release redirect")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def safe_directory(path: Path) -> Path:
    path = Path(os.path.abspath(path))
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if current.is_symlink():
            raise InstallError("installation directories cannot traverse symlinks")
        current.mkdir(exist_ok=True)
        if not current.is_dir():
            raise InstallError("installation parent is not a directory")
    return path


def copy_verified(source, target: Path, *, size: int, sha256: str, description: str) -> None:
    count, digest = 0, hashlib.sha256()
    deadline = time.monotonic() + 180
    with target.open("xb") as output:
        while True:
            if time.monotonic() > deadline:
                raise InstallError(f"{description} exceeded its time bound")
            body = source.read(min(65536, size - count + 1))
            if not body:
                break
            count += len(body)
            if count > size:
                raise InstallError(f"{description} exceeded its pinned extent")
            digest.update(body)
            output.write(body)
    if count != size or digest.hexdigest() != sha256:
        raise InstallError(f"{description} hash or byte extent mismatch")


def install(root: Path, destination: Path, *, archive: Path | None = None, fetch: bool = False) -> dict:
    if type(fetch) is not bool or (archive is None) == (not fetch):
        raise InstallError("choose exactly one of --archive or --fetch")
    pin = load_lock(root)
    destination = safe_directory(destination)
    binary = destination / "pandoc"
    if os.path.lexists(binary):
        raise InstallError("refusing to overwrite an existing Pandoc binary")
    with tempfile.TemporaryDirectory(prefix="pandoc-stage-", dir=destination) as temporary:
        stage = Path(temporary)
        pinned = stage / "verified.tar.gz"
        if archive is not None:
            descriptor = os.open(archive, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
            with os.fdopen(descriptor, "rb") as source:
                if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                    raise InstallError("Pandoc archive must be a regular file")
                copy_verified(source, pinned, size=pin["archive_bytes"], sha256=pin["archive_sha256"], description="Pandoc release")
        else:
            request = urllib.request.Request(pin["archive_url"], headers={"User-Agent": "Triptych-pinned-Pandoc", "Accept-Encoding": "identity"})
            with urllib.request.build_opener(Redirects()).open(request, timeout=30) as source:
                size = source.headers.get("Content-Length")
                if size is not None and (not size.isdecimal() or int(size) != pin["archive_bytes"]):
                    raise InstallError("Pandoc release HTTP extent mismatch")
                copy_verified(source, pinned, size=pin["archive_bytes"], sha256=pin["archive_sha256"], description="Pandoc release")
        # Interpret the archive only after authenticating its complete pinned
        # bytes. Copy one exact regular binary; never extract unrelated paths.
        with tarfile.open(pinned, "r:gz") as package:
            selected = [member for member in package if member.name == pin["member"]]
            if len(selected) != 1:
                raise InstallError("Pandoc archive must name exactly one selected binary")
            member = selected[0]
            if not member.isreg() or member.linkname or member.size != pin["binary_bytes"]:
                raise InstallError("selected Pandoc binary has an unsafe type or extent")
            source = package.extractfile(member)
            if source is None:
                raise InstallError("selected Pandoc binary is unreadable")
            staged = stage / "pandoc"
            with source:
                copy_verified(source, staged, size=pin["binary_bytes"], sha256=pin["binary_sha256"], description="Pandoc binary")
        staged.chmod(0o755)
        result = subprocess.run([str(staged), "--version"], check=True, capture_output=True, text=True, timeout=10)
        if result.stdout.splitlines()[:1] != ["pandoc " + pin["version"]]:
            raise InstallError("Pandoc binary does not report its pinned version")
        # Publish a complete verified binary without replacing a racing path.
        os.link(staged, binary, follow_symlinks=False)
    return {"binary": str(binary), "version": pin["version"],
            "archive_sha256": pin["archive_sha256"], "binary_sha256": pin["binary_sha256"]}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--bin-dir", type=Path, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--archive", type=Path)
    group.add_argument("--fetch", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = install(args.root, args.bin_dir, archive=args.archive, fetch=args.fetch)
    except (InstallError, OSError, ValueError, tarfile.TarError, subprocess.SubprocessError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
