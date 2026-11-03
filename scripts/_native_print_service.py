"""Bounded, source-pinned native TeX PDF jobs for a separately hosted service.

The public API accepts admitted document identities, never TeX, paths or commands.
The owning print-document recipe supplies the original layout and source gates.
Run behind an HTTPS proxy in the isolated, read-only compiler container; this
module does not turn GitHub Pages into a server or confer print-review approval.
"""
from __future__ import annotations

import argparse
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-native-print-service/v1"
CACHE_SCHEMA = "triptych-native-print-cache/v1"
KEY = re.compile(r"[0-9a-f]{64}\Z")
REVISION = re.compile(r"[0-9a-f]{40}\Z")
TOOLCHAIN = re.compile(r"sha256:[0-9a-f]{64}\Z")
REQUEST_LIMIT = 2048


class ServiceError(ValueError):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def _canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _plain_file(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def _safe_directory(path: Path, root: Path) -> Path:
    path = path.expanduser().absolute()
    if any(parent.is_symlink() for parent in (path, *path.parents)):
        raise ServiceError("The print cache directory must not contain symlinks.")
    resolved = path.resolve()
    if resolved == root or root.is_relative_to(resolved):
        raise ServiceError("The print cache must have its own directory.")
    if resolved.is_relative_to(root) and not any(
        resolved.is_relative_to(root / name) and resolved != root / name
        for name in (".scratch", "build")
    ):
        raise ServiceError("A repository-local print cache belongs under .scratch or build.")
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def _git(root: Path, *arguments: str) -> str:
    try:
        result = subprocess.run(["git", "--no-optional-locks", "-c", "safe.directory=" + str(root),
                                 "-C", str(root), *arguments],
                                capture_output=True, text=True, timeout=30,
                                env={"PATH": os.environ.get("PATH", os.defpath),
                                     "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ServiceError("The compiler source snapshot cannot be verified.", 503) from error
    if result.returncode:
        raise ServiceError("The compiler source snapshot cannot be verified.", 503)
    return result.stdout.strip()


def assert_source(root: Path, revision: str) -> None:
    """Refuse drift and uncommitted source changes, including added source inputs."""
    if _git(root, "rev-parse", "HEAD") != revision:
        raise ServiceError("The compiler source revision changed; restart the service.", 409)
    # Ignored compiler output may be writable, but it cannot become source.
    if (_git(root, "status", "--porcelain=v1", "--untracked-files=no")
            or _git(root, "ls-files", "--others", "--exclude-standard", "--",
                    "src", "release", "scripts", "tools", "Makefile")):
        raise ServiceError("The compiler source snapshot has uncommitted changes.", 503)


def admitted_selections(root: Path) -> dict:
    from _native_print import admitted_selections as selections
    return selections(root)


def _origin(value: str) -> str:
    parsed = urlsplit(value)
    if (parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.username
            or parsed.password or parsed.path or parsed.query or parsed.fragment):
        raise ServiceError("Each allowed origin must be an exact HTTP(S) origin without a path.")
    if parsed.scheme != "https" and parsed.hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise ServiceError("A public browser origin must use HTTPS.")
    return value


def _receipt(root: Path, path: Path, pdf: Path, selected: dict, maximum: int) -> dict:
    """Verify the owning tool's source-output attestation before exporting bytes."""
    if not _plain_file(path) or path.stat().st_size > 16 * 1024 * 1024:
        raise ServiceError("The native typesetter did not produce a valid receipt.", 500)
    saved = json.loads(path.read_bytes())
    if (saved.get("schema") != "triptych-print-document/v1" or saved.get("status") != "built"
            or saved.get("output_format") != "pdf" or saved.get("document", {}).get("id") != selected["id"]
            or saved.get("path_base") != "receipt-directory" or saved.get("output") != pdf.name
            or not isinstance(saved.get("inputs"), list) or not saved["inputs"]):
        raise ServiceError("The native PDF receipt does not match the selected edition.", 500)
    if not _plain_file(pdf) or not 0 < pdf.stat().st_size <= maximum:
        raise ServiceError("The native PDF is missing or exceeds the configured output limit.", 500)
    with pdf.open("rb") as stream:
        if not stream.read(8).startswith(b"%PDF-"):
            raise ServiceError("The native typesetter returned a non-PDF response.", 500)
        stream.seek(max(0, pdf.stat().st_size - 1024))
        if b"%%EOF" not in stream.read():
            raise ServiceError("The native PDF is incomplete.", 500)
    if (saved.get("bytes") != pdf.stat().st_size or saved.get("output_sha256") != _sha(pdf)):
        raise ServiceError("The native PDF does not match its source-output receipt.", 500)
    seen = set()
    for row in saved["inputs"]:
        relative = row.get("path") if isinstance(row, dict) else None
        if (not isinstance(relative, str) or not relative or "\\" in relative
                or Path(relative).is_absolute() or ".." in Path(relative).parts or relative in seen):
            raise ServiceError("The native receipt contains an invalid source dependency.", 500)
        seen.add(relative)
        source = root / relative
        if (any(parent.is_symlink() for parent in (source, *source.parents) if parent != root.parent)
                or not source.resolve().is_relative_to(root) or not _plain_file(source)
                or row.get("bytes") != source.stat().st_size or row.get("sha256") != _sha(source)):
            raise ServiceError("A native PDF source dependency changed during compilation.", 409)
    return saved


class PrintService:
    """One immutable source snapshot with finite asynchronous work and verified cache."""
    def __init__(self, root: Path, cache_root: Path, *, toolchain: str,
                 origins=(), workers: int = 1, queue_limit: int = 8,
                 timeout: int = 1800, max_pdf_bytes: int = 128 * 1024 * 1024,
                 max_cache_bytes: int = 2 * 1024 * 1024 * 1024, max_records: int = 256,
                 revision: str | None = None, source_checker=assert_source,
                 selection_loader=admitted_selections, compiler=None):
        self.root = Path(root).resolve()
        if not TOOLCHAIN.fullmatch(toolchain or ""):
            raise ServiceError("An immutable toolchain sha256 digest is required.")
        if (not 1 <= workers <= 8 or not 1 <= queue_limit <= 128 or not 1 <= timeout <= 7200
                or not 1024 <= max_pdf_bytes <= max_cache_bytes or max_records < queue_limit + workers):
            raise ServiceError("Invalid native print service resource limits.")
        self.toolchain = toolchain
        self.revision = revision or _git(self.root, "rev-parse", "HEAD")
        if not REVISION.fullmatch(self.revision or ""):
            raise ServiceError("The source revision must be a full Git commit identity.")
        self.source_checker = source_checker
        self.selection_loader = selection_loader
        self.source_checker(self.root, self.revision)
        self.selections = self.selection_loader(self.root)
        if not self.selections:
            raise ServiceError("The admitted print catalogue is empty.")
        self.cache = _safe_directory(Path(cache_root), self.root)
        self.objects = self.cache / "objects"
        self.work = self.cache / "work"
        for directory in (self.objects, self.work):
            if directory.is_symlink():
                raise ServiceError("Compiler state directories must not be symlinks.")
            directory.mkdir(exist_ok=True)
        self.origins = frozenset(_origin(value) for value in origins)
        self.queue_limit = queue_limit
        self.timeout = timeout
        self.max_pdf_bytes = max_pdf_bytes
        self.max_cache_bytes = max_cache_bytes
        self.max_records = max_records
        self.jobs = OrderedDict()
        self.lock = threading.RLock()
        self.processes = set()
        self.slots = threading.BoundedSemaphore(queue_limit + workers)
        self.executor = ThreadPoolExecutor(max_workers=workers, thread_name_prefix="native-print")
        self.compiler = compiler or self.compile
        self.closed = False

    def _current(self, selection=None) -> None:
        self.source_checker(self.root, self.revision)
        if selection is not None:
            try:
                current = self.selection_loader(self.root).get((selection["document"], selection["edition"]))
            except (OSError, ValueError, KeyError, TypeError) as error:
                raise ServiceError("The current public print catalogue cannot be verified.", 503) from error
            if current != selection:
                raise ServiceError("This print edition was changed or withdrawn.", 409)

    def _identity(self, selected: dict) -> dict:
        return {"schema": SCHEMA, "source_revision": self.revision,
                "toolchain": self.toolchain, "document": selected["document"],
                "edition": selected["edition"], "output_id": selected["id"]}

    def _view(self, job: dict) -> dict:
        key = job["key"]
        result = {"schema": SCHEMA, "key": key, "source_revision": self.revision,
                "document": job["selection"]["document"], "edition": job["selection"]["edition"],
                "output_id": job["selection"]["id"], "state": job["state"],
                "status_url": "/v1/jobs/" + key,
                "pdf_url": "/v1/jobs/" + key + "/pdf" if job["state"] == "ready" else None,
                "error": job.get("error"), "retry_after": 2}
        if job["state"] == "ready":
            manifest = json.loads((self.objects / key / "manifest.json").read_bytes())
            result.update(bytes=manifest["bytes"], pdf_sha256=manifest["sha256"],
                          receipt_sha256=manifest["receipt_sha256"])
        return result

    def _cached(self, key: str, selected: dict) -> bool:
        directory = self.objects / key
        try:
            if directory.is_symlink() or not directory.is_dir():
                return False
            manifest_path = directory / "manifest.json"
            if not _plain_file(manifest_path) or manifest_path.stat().st_size > 8192:
                return False
            manifest = json.loads(manifest_path.read_bytes())
            if (manifest.get("schema") != CACHE_SCHEMA or manifest.get("key") != key
                    or manifest.get("identity") != self._identity(selected)):
                return False
            pdf = directory / "document.pdf"
            receipt = directory / "document.print.json"
            if (not _plain_file(pdf) or not _plain_file(receipt)
                    or not 0 < pdf.stat().st_size <= self.max_pdf_bytes
                    or manifest.get("bytes") != pdf.stat().st_size
                    or manifest.get("sha256") != _sha(pdf)
                    or manifest.get("receipt_sha256") != _sha(receipt)):
                return False
            saved = json.loads(receipt.read_bytes())
            return (saved.get("document", {}).get("id") == selected["id"]
                    and saved.get("output_sha256") == manifest["sha256"]
                    and saved.get("bytes") == manifest["bytes"])
        except (OSError, ValueError, TypeError):
            return False

    def submit(self, request: dict) -> dict:
        if not isinstance(request, dict) or set(request) != {"document", "edition", "source_revision"}:
            raise ServiceError("Supply only document, edition and source_revision.")
        if not all(isinstance(value, str) for value in request.values()):
            raise ServiceError("Print selection fields must be strings.")
        if request["source_revision"] != self.revision:
            raise ServiceError("This page and the PDF service have different source revisions. Reload the page.", 409)
        selected = self.selections.get((request["document"], request["edition"]))
        if selected is None:
            raise ServiceError("This document edition is not admitted for public printing.", 404)
        self._current(selected)
        key = hashlib.sha256(_canonical(self._identity(selected))).hexdigest()
        with self.lock:
            if self.closed:
                raise ServiceError("The PDF service is shutting down.", 503)
            existing = self.jobs.get(key)
            if existing and existing["state"] in {"queued", "building"}:
                return self._view(existing)
            if self._cached(key, selected):
                job = {"key": key, "selection": selected, "state": "ready"}
                self.jobs[key] = job
                self._trim_records()
                return self._view(job)
            if not self.slots.acquire(blocking=False):
                raise ServiceError("The PDF typesetter is busy. Please try again shortly.", 429)
            job = {"key": key, "selection": selected, "state": "queued"}
            self.jobs[key] = job
            self._trim_records()
            try:
                self.executor.submit(self._build, job)
            except RuntimeError:
                self.slots.release()
                self.jobs.pop(key, None)
                raise ServiceError("The PDF service is shutting down.", 503) from None
            return self._view(job)

    def _trim_records(self) -> None:
        for key in list(self.jobs):
            if len(self.jobs) <= self.max_records:
                break
            if self.jobs[key]["state"] in {"ready", "failed"}:
                del self.jobs[key]

    def status(self, key: str) -> dict:
        if not KEY.fullmatch(key):
            raise ServiceError("Unknown PDF job.", 404)
        with self.lock:
            job = self.jobs.get(key)
            if job is None:
                raise ServiceError("Unknown PDF job. Request the edition again.", 404)
            if job["state"] == "ready" and not self._cached(key, job["selection"]):
                job.update(state="failed", error="The cached PDF failed verification. Request this edition again.")
            return self._view(job)

    def pdf(self, key: str) -> tuple[Path, str]:
        status = self.status(key)
        with self.lock:
            selected = self.jobs[key]["selection"]
            self._current(selected)
            if status["state"] != "ready":
                raise ServiceError("The native PDF is not ready.", 409)
            path = self.objects / key / "document.pdf"
            stem = selected["id"].split(":", 1)[-1].rsplit("/", 1)[-1]
            filename = re.sub(r"[^a-zA-Z0-9._-]", "-", stem)[:100] + ".pdf"
            return path, filename

    def _prune(self, keep: str, incoming: int) -> None:
        entries = []
        for directory in self.objects.iterdir():
            if directory.is_symlink() or not directory.is_dir() or not KEY.fullmatch(directory.name):
                continue
            size = sum(path.stat().st_size for path in directory.iterdir() if _plain_file(path))
            entries.append((directory.stat().st_mtime_ns, directory, size))
        total = sum(row[2] for row in entries)
        for _, directory, size in sorted(entries):
            if total + incoming <= self.max_cache_bytes:
                return
            if directory.name != keep:
                shutil.rmtree(directory)
                total -= size
        if total + incoming > self.max_cache_bytes:
            raise ServiceError("The native PDF cache is full.", 503)

    def _build(self, job: dict) -> None:
        try:
            with self.lock:
                if self.closed:
                    raise ServiceError("The PDF service is shutting down.", 503)
                job["state"] = "building"
            selected, key = job["selection"], job["key"]
            self._current(selected)
            with tempfile.TemporaryDirectory(prefix=key[:12] + "-", dir=self.work) as folder:
                workspace = Path(folder)
                pdf, receipt = self.compiler(selected, workspace)
                saved = _receipt(self.root, receipt, pdf, selected, self.max_pdf_bytes)
                self._current(selected)
                prepared = workspace / "verified"
                prepared.mkdir()
                shutil.copyfile(pdf, prepared / "document.pdf")
                shutil.copyfile(receipt, prepared / "document.print.json")
                manifest = {"schema": CACHE_SCHEMA, "key": key, "identity": self._identity(selected),
                            "bytes": saved["bytes"], "sha256": saved["output_sha256"],
                            "receipt_sha256": _sha(prepared / "document.print.json")}
                (prepared / "manifest.json").write_bytes(_canonical(manifest) + b"\n")
                with self.lock:
                    target = self.objects / key
                    if target.is_symlink():
                        raise ServiceError("The native PDF cache entry is invalid.", 500)
                    if target.exists():
                        shutil.rmtree(target)
                    incoming = sum(path.stat().st_size for path in prepared.iterdir())
                    self._prune(key, incoming)
                    prepared.replace(target)
                    if not self._cached(key, selected):
                        raise ServiceError("The native PDF failed final cache verification.", 500)
                    job["state"] = "ready"
        except Exception as error:
            # Paths, source contents, subprocess logs and infrastructure identity
            # are never reflected to an anonymous browser.
            message = (str(error) if isinstance(error, ServiceError) else
                       "The TeX typesetter could not build this edition. Please retry later or report the document.")
            with self.lock:
                job.update(state="failed", error=message)
        finally:
            self.slots.release()

    def compile(self, selected: dict, workspace: Path) -> tuple[Path, Path]:
        output = workspace / "output"
        output.mkdir()
        for name in ("home", "texmf-var", "texmf-config", "tmp"):
            (workspace / name).mkdir()
        # Do not inherit service/proxy credentials, caller Make flags, Python
        # imports, font overrides or TeX search/command overrides.
        environment = {"PATH": os.environ.get("PATH", os.defpath),
                       "LANG": "C.UTF-8", "TZ": "UTC", "PYTHONDONTWRITEBYTECODE": "1",
                       "HOME": str(workspace / "home"), "TMPDIR": str(workspace / "tmp"),
                       "TEXMFVAR": str(workspace / "texmf-var"),
                       "TEXMFCONFIG": str(workspace / "texmf-config"),
                       "TRIPTYCH_PRINT_WORK_ROOT": str(workspace / "native-work"),
                       "shell_escape": "f", "openout_any": "p"}
        print_command = [sys.executable, str(self.root / "tools/print-document"), "build",
                   "--document", selected["document"], "--edition", selected["edition"],
                   "--output-format", "pdf", "--out", str(output), "--json"]
        # A small Python launcher establishes inherited per-process resource
        # ceilings before any owning tool or TeX child is started. Unlike a
        # preexec_fn this is safe in the service's worker threads. The container
        # additionally caps aggregate memory/CPU/process count and denies egress.
        limits = (
            "import os,resource,sys; "
            "resource.setrlimit(resource.RLIMIT_CORE,(0,0)); "
            "resource.setrlimit(resource.RLIMIT_NOFILE,(128,128)); "
            "resource.setrlimit(resource.RLIMIT_AS,(2147483648,2147483648)); "
            f"resource.setrlimit(resource.RLIMIT_CPU,({self.timeout},{self.timeout})); "
            f"resource.setrlimit(resource.RLIMIT_FSIZE,({max(self.max_pdf_bytes, 16777216)},"
            f"{max(self.max_pdf_bytes, 16777216)})); "
            "os.execv(sys.argv[1],sys.argv[1:])"
        )
        command = [sys.executable, "-c", limits, *print_command]
        log_path = workspace / "compiler.log"
        with log_path.open("wb") as log:
            try:
                with self.lock:
                    if self.closed:
                        raise ServiceError("The PDF service is shutting down.", 503)
                    process = subprocess.Popen(command, cwd=self.root, env=environment,
                                               stdin=subprocess.DEVNULL, stdout=log,
                                               stderr=subprocess.STDOUT, start_new_session=True)
                    self.processes.add(process)
            except OSError as error:
                raise ServiceError("The native TeX compiler is unavailable.", 503) from error
            try:
                result = process.wait(timeout=self.timeout)
            except BaseException:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
                raise ServiceError("This native PDF exceeded the compilation time limit.", 503) from None
            finally:
                # Also close any descendant left behind after its parent exits.
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                with self.lock:
                    self.processes.discard(process)
        if result:
            raise ServiceError("The TeX typesetter could not build this edition. Please report the document.", 500)
        receipts = list(output.glob("*.print.json"))
        pdfs = list(output.glob("*.pdf"))
        if len(receipts) != 1 or len(pdfs) != 1:
            raise ServiceError("The native typesetter did not produce one PDF and receipt.", 500)
        return pdfs[0], receipts[0]

    def close(self) -> None:
        with self.lock:
            self.closed = True
            for process in self.processes:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
        self.executor.shutdown(wait=True, cancel_futures=False)


class BoundedHTTPServer(ThreadingHTTPServer):
    """Bound connection threads as well as the independently bounded job queue."""
    daemon_threads = True

    def __init__(self, address, request_handler, *, connection_limit=32):
        self.connection_slots = threading.BoundedSemaphore(connection_limit)
        super().__init__(address, request_handler)

    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(15)
        return connection, address

    def process_request(self, request, address):
        if not self.connection_slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, address)
        except BaseException:
            self.connection_slots.release()
            raise

    def process_request_thread(self, request, address):
        try:
            super().process_request_thread(request, address)
        finally:
            self.connection_slots.release()

    def handle_error(self, request, client_address):
        # Unexpected client disconnects cannot print private network metadata.
        return


def handler(service: PrintService):
    class Handler(BaseHTTPRequestHandler):
        server_version = "TriptychNativePrint/1"
        sys_version = ""

        def log_message(self, format, *arguments):
            # Do not persist client addresses or request data in default logs.
            return

        def _cors(self) -> None:
            origin = self.headers.get("Origin")
            if origin:
                if origin not in service.origins:
                    raise ServiceError("This browser origin is not enabled for native printing.", 403)
                self._allowed_origin = origin

        def _headers(self, status, mime, length):
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(length))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            if getattr(self, "_allowed_origin", None):
                self.send_header("Access-Control-Allow-Origin", self._allowed_origin)
                self.send_header("Vary", "Origin")

        def _json(self, status, value):
            payload = _canonical(value) + b"\n"
            self._headers(status, "application/json; charset=utf-8", len(payload))
            self.end_headers()
            self.wfile.write(payload)

        def _error(self, error):
            self._json(error.status, {"schema": SCHEMA, "error": str(error),
                                      "source_revision": service.revision})

        def do_OPTIONS(self):
            try:
                self._cors()
                if self.path != "/v1/jobs":
                    raise ServiceError("Unknown native print endpoint.", 404)
                if self.headers.get("Access-Control-Request-Method") != "POST":
                    raise ServiceError("Unsupported native print method.", 405)
                requested = self.headers.get("Access-Control-Request-Headers", "").lower()
                if any(value.strip() not in {"content-type", ""} for value in requested.split(",")):
                    raise ServiceError("Unsupported native print request headers.")
                self._headers(204, "application/json", 0)
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header("Access-Control-Allow-Headers", "Content-Type")
                self.send_header("Access-Control-Max-Age", "600")
                self.end_headers()
            except ServiceError as error:
                self._error(error)
            except (BrokenPipeError, ConnectionResetError, TimeoutError):
                return

        def do_POST(self):
            try:
                self._cors()
                if self.path != "/v1/jobs":
                    raise ServiceError("Unknown native print endpoint.", 404)
                if self.headers.get("Transfer-Encoding"):
                    raise ServiceError("Chunked print requests are not supported.")
                length = self.headers.get("Content-Length", "")
                if not length.isdecimal() or not 0 < int(length) <= REQUEST_LIMIT:
                    raise ServiceError("The print selection exceeds its request limit.", 413)
                if self.headers.get_content_type() != "application/json":
                    raise ServiceError("A native print request must be JSON.", 415)
                try:
                    request = json.loads(self.rfile.read(int(length)))
                except (ValueError, UnicodeError):
                    raise ServiceError("The native print request is not valid JSON.") from None
                self._json(202, service.submit(request))
            except ServiceError as error:
                self._error(error)
            except (BrokenPipeError, ConnectionResetError, TimeoutError):
                return

        def do_GET(self):
            try:
                self._cors()
                if self.path == "/v1/health":
                    service._current()
                    return self._json(200, {"schema": SCHEMA, "status": "ok",
                                           "source_revision": service.revision,
                                           "toolchain": service.toolchain,
                                           "editions": len(service.selections)})
                match = re.fullmatch(r"/v1/jobs/([0-9a-f]{64})(/pdf)?", self.path)
                if not match:
                    raise ServiceError("Unknown native print endpoint.", 404)
                key, download = match.groups()
                if not download:
                    return self._json(200, service.status(key))
                # Verify and open the selected object while publication/pruning
                # is excluded, then release the global job lock before network
                # I/O. On the supported Unix host an open descriptor remains
                # valid if a later cache eviction unlinks its directory.
                with service.lock:
                    path, filename = service.pdf(key)
                    source = path.open("rb")
                    length = os.fstat(source.fileno()).st_size
                with source:
                    self._headers(200, "application/pdf", length)
                    self.send_header("Content-Disposition", 'attachment; filename="' + filename + '"')
                    self.end_headers()
                    deadline = time.monotonic() + 300
                    while block := source.read(1024 * 1024):
                        remaining = deadline - time.monotonic()
                        if remaining <= 0:
                            self.close_connection = True
                            return
                        self.connection.settimeout(min(15, remaining))
                        self.wfile.write(block)
            except ServiceError as error:
                self._error(error)
            except (BrokenPipeError, ConnectionResetError, TimeoutError):
                return

    return Handler


def main(argv=None, *, examples=None) -> int:
    from _tooling import examples_live_on_the_verbs, with_examples
    parser = argparse.ArgumentParser(prog="native-print-service", description=__doc__)
    examples_live_on_the_verbs(parser, "native-print-service")
    commands = parser.add_subparsers(dest="verb", required=True)
    serve = commands.add_parser("serve", help="serve source-pinned native PDF jobs behind an HTTPS proxy")
    with_examples(serve, (examples or {}).get("serve", ()))
    serve.add_argument("--root", type=Path, default=ROOT)
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8080)
    serve.add_argument("--cache-root", type=Path, help="default: .scratch/native-print-service")
    serve.add_argument("--origin", action="append", default=[], help="exact allowed browser origin; repeat for additional origins")
    serve.add_argument("--toolchain-id", default=os.environ.get("TRIPTYCH_PRINT_TOOLCHAIN", ""),
                       help="immutable renderer image sha256 digest; also TRIPTYCH_PRINT_TOOLCHAIN")
    serve.add_argument("--workers", type=int, default=1)
    serve.add_argument("--queue-limit", type=int, default=8)
    serve.add_argument("--timeout", type=int, default=1800, help="compilation timeout in seconds")
    serve.add_argument("--max-pdf-bytes", type=int, default=128 * 1024 * 1024)
    serve.add_argument("--max-cache-bytes", type=int, default=2 * 1024 * 1024 * 1024)
    arguments = parser.parse_args(argv)
    service = None
    try:
        if not 1 <= arguments.port <= 65535:
            raise ServiceError("The native print port is invalid.")
        cache = arguments.cache_root or arguments.root / ".scratch/native-print-service"
        service = PrintService(arguments.root, cache, toolchain=arguments.toolchain_id,
                               origins=arguments.origin, workers=arguments.workers,
                               queue_limit=arguments.queue_limit, timeout=arguments.timeout,
                               max_pdf_bytes=arguments.max_pdf_bytes,
                               max_cache_bytes=arguments.max_cache_bytes)
        server = BoundedHTTPServer((arguments.host, arguments.port), handler(service))
        server.timeout = 30
        try:
            server.serve_forever(poll_interval=0.5)
        finally:
            server.server_close()
        return 0
    except KeyboardInterrupt:
        return 0
    except (ServiceError, OSError, ValueError) as error:
        print("native-print-service: " + str(error), file=sys.stderr)
        return 2
    finally:
        if service:
            service.close()


if __name__ == "__main__":
    raise SystemExit(main())
