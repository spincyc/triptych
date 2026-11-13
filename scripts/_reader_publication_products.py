"""Publication discovery metadata and one source-owned reader at a time.

The tracked lookup contains titles, dispositions and recipes, never a rendered
body. Maintenance derives it from the full producers; opening a reader checks
and converts only that selected recipe in an isolated interpreter.
"""
from __future__ import annotations

import hashlib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

CATALOG = "src/index/documents/corpus.json"
READERS = "src/index/documents/readers.json"
SCHEMA = "triptych-publication-reader-index/v1"
_TOOLS = {}
WORKER_TIMEOUT = 120.0
WORKER_POLL = 0.1
# Conservative publication-runtime scope. Generated lookup commits are outside
# it; source edits followed by a byte-identical revert remain inside its history.
HISTORY_PATHS = (
    "src", ":(exclude)src/index", "scripts", "tools", ":(exclude)tools/tests",
    "web", "release/publications", "workflows/pipelines", "workflows/fragments",
    "workflows/schema", "guidance/liturgy/postconciliar-propers-registry.md", "requirements*.txt",
    "LICENSE", "THIRD_PARTY.md",
)


def _git(root, *arguments):
    result = subprocess.run(["git", *arguments], cwd=root, capture_output=True,
                            text=True, check=False,
                            env={**os.environ, "GIT_NO_LAZY_FETCH": "1"})
    if result.returncode:
        raise ValueError("publication history is unavailable; refresh publication metadata "
                         "from complete history: " + result.stderr.strip()[-2000:])
    return result.stdout.strip()


def _history_head(root):
    if _git(root, "rev-parse", "--is-shallow-repository") != "false":
        raise ValueError("publication history is shallow; restore complete history and "
                         "refresh publication metadata")
    return _git(root, "rev-parse", "--verify", "HEAD")


def _clean_history_head(root):
    head = _history_head(root)
    if _git(root, "status", "--porcelain", "--untracked-files=all", "--", *HISTORY_PATHS):
        raise ValueError("publication metadata requires committed runtime inputs; "
                         "commit source and producer changes before refreshing")
    return head


def _check_history(root, discovery):
    base = discovery.get("generation_commit")
    if not isinstance(base, str) or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", base):
        raise ValueError("publication metadata has no generation commit; refresh publication metadata")
    head = _history_head(root)
    # This checks ancestry, including missing base objects, without fetching or
    # reading historical source blobs. Trees and commit metadata suffice.
    try:
        _git(root, "merge-base", "--is-ancestor", base, head)
    except ValueError as error:
        raise ValueError("publication metadata generation commit is missing or not an ancestor; "
                         "restore history and refresh publication metadata") from error
    changed = _git(root, "log", "--full-history", "-m", "--format=", "--name-only",
                   f"{base}..{head}", "--", *HISTORY_PATHS)
    if changed:
        raise ValueError("publication inputs changed since metadata generation; "
                         "refresh publication metadata")


def _discovery(root, index):
    discovery = json.loads(index.read(READERS))
    if (not isinstance(discovery, dict) or discovery.get("schema") != SCHEMA
            or not isinstance(discovery.get("readers"), dict)):
        raise ValueError("invalid publication reader index")
    _check_history(root, discovery)
    return discovery


def verify_history(root: Path, index) -> None:
    """Validate Publications history before accepting a warm reader cache."""
    _discovery(root, index)


def _tool(root, name):
    path = Path(root).resolve() / "tools" / name
    if path not in _TOOLS:
        loader = SourceFileLoader("_publication_reader_" + name.replace("-", "_"), str(path))
        spec = spec_from_loader(loader.name, loader)
        module = module_from_spec(spec)
        sys.modules[loader.name] = module
        loader.exec_module(module)
        _TOOLS[path] = module
    return _TOOLS[path]


def _json(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=1,
                       allow_nan=False) + "\n").encode("utf-8")


def build_reader_indexes(root: Path, *, generation_commit: str | None = None) -> dict[str, bytes]:
    """Explicit maintenance only; independent calls rederive canonical inputs.

    Keep the catalogue's existing revision timestamps and qualifications. Its
    expensive whole-corpus discovery is never part of an individual read.
    """
    from _corpus import documents
    root = Path(root).resolve()
    current_head = _clean_history_head(root)
    if generation_commit is None:
        generation_commit = current_head
    else:
        # An independent check preserves a still-valid authority across commits
        # that only record metadata, rather than changing the anchor each time.
        _check_history(root, {"generation_commit": generation_commit})
    owner = _tool(root, "document-library")
    documents.cache_clear()
    rows = documents(root=root)
    catalogue = owner.catalogue(rows, {row.key: row for row in rows}, root=root)
    if any("(uncommitted sources)" in edition.get("revised", "")
           for work in catalogue["works"] for edition in work["editions"]):
        raise ValueError("publication discovery requires committed edition sources; "
                         "derived revision timestamps must be reproducible")
    readers = _tool(root, "web-edition").reader_outputs()
    if _clean_history_head(root) != current_head:
        raise ValueError("publication history changed during metadata generation; refresh again")
    return {CATALOG: owner._serialise(catalogue).encode("utf-8"),
            READERS: _json({"schema": SCHEMA, "generation_commit": generation_commit, "readers": {
                row["provider"] + "/" + row["document"]: row for row in readers}})}


def _stop_worker(process):
    """Terminate the owned session, including children outliving its leader."""
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.communicate(timeout=0.25)
    except subprocess.TimeoutExpired:
        pass
    finally:
        # The leader may already have exited and closed its pipes while pandoc
        # still runs. Never make group cleanup conditional on leader.poll().
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.communicate(timeout=2.0)


def _run_worker(command, *, input: str, cwd: Path, index, timeout=WORKER_TIMEOUT):
    """Capture one isolated conversion with bounded, cooperative cancellation."""
    cancelled = getattr(index, "_reader_cancelled", None)

    def check():
        if cancelled is not None and cancelled.is_set():
            raise ValueError("publication reader cancelled")

    check()
    deadline = time.monotonic() + timeout
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, cwd=cwd,
                               start_new_session=True)
    try:
        pending = input
        while True:
            check()  # Also closes the cancellation race during process creation.
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise ValueError(f"publication reader exceeded its {timeout:g}s timeout")
            try:
                stdout, stderr = process.communicate(input=pending, timeout=min(WORKER_POLL, remaining))
            except subprocess.TimeoutExpired:
                pending = None  # communicate retains its partially written input.
                continue
            check()
            return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    except BaseException:
        _stop_worker(process)
        raise
    finally:
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is not None and not stream.closed:
                stream.close()


def resolve(relative: str, root: Path, index) -> bytes | None:
    """Resolve discovery or one edition, recording its verified dependencies.

    The child verifies canonical bytes at consumption. Re-reading its complete
    captured closure here rejects changes during conversion and registers those
    dependencies with the caller's disposable cache. No family build is used.
    """
    if relative == "structure/documents/corpus.json":
        _discovery(root, index)
        body = index.read(CATALOG)
        catalogue = json.loads(body)
        if not isinstance(catalogue, dict) or catalogue.get("schema") != "triptych-document-catalogue/v1":
            raise ValueError("invalid publication discovery index")
        return body
    if not relative.startswith("web-editions/") or relative == "web-editions/index.json":
        return None
    match = re.fullmatch(r"web-editions/((?:claude|gpt)/[a-z0-9][a-z0-9./-]*)\.json", relative)
    if match is None or any(part in {"", ".", ".."} for part in match[1].split("/")):
        raise ValueError("unsafe publication reader path")
    identity = match[1]
    discovery = _discovery(root, index)
    row = discovery["readers"].get(identity)
    if (not isinstance(row, dict) or not isinstance(row.get("provider"), str)
            or not isinstance(row.get("document"), str)
            or row["provider"] + "/" + row["document"] != identity):
        raise ValueError(f"no indexed publication reader: {identity}")
    done = _run_worker(
        [sys.executable, "-B", str(Path(root) / "tools/web-edition"),
         "--indexed-product-row-json", identity],
        input=json.dumps(row, ensure_ascii=False, allow_nan=False),
        cwd=root, index=index)
    if done.returncode:
        raise ValueError(f"publication reader {identity}: {done.stderr.strip()[-6000:]}")
    result = json.loads(done.stdout)
    if not isinstance(result, dict):
        raise ValueError("publication reader returned an invalid response")
    dependencies = result.get("dependencies")
    if not isinstance(dependencies, dict) or not dependencies:
        raise ValueError("publication reader returned no verified dependencies")
    for path, digest in dependencies.items():
        if hashlib.sha256(index.read(path)).hexdigest() != digest:
            raise ValueError(f"publication input changed during conversion: {path}")
    _check_history(root, discovery)
    record = result.get("record")
    if (not isinstance(record, dict) or record.get("schema") != "triptych-web-edition/v1"
            or record.get("id") != identity or not isinstance(record.get("markdown"), str)
            or hashlib.sha256(record["markdown"].encode("utf-8")).hexdigest()
            != record.get("markdown_sha256")):
        raise ValueError("publication reader returned an invalid product")
    return _json(record)
