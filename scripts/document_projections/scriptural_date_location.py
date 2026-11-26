"""The Scriptural Date and Location page of a proper study.

Owns, for one proper leaf: the chronology record, its sealed annotations and
the shared orientation-v3 table under ``research/``, and the two generated
page variants under ``generated/``. The record and the page are therefore
refreshed by one command and held current by one check; the page's content
model is ``scripts/_proper_chronology_page.py``.
"""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path

import _proper_chronology as wiring
import _proper_chronology_page as page

NAME = "scriptural-date-location"
OUTPUTS = {
    page.SECTION: "generated/scriptural-date-location.tex",
    page.PAGE: "generated/scriptural-date-location-page.tex",
    page.SHEET: "generated/scriptural-date-location-sheet.tex",
    page.EVIDENCE: "generated/scriptural-date-location-evidence.tex",
}
KINDS = ("proper-1962", "proper-postconciliar")

_INPUT_STATE: dict[Path, bytes] = {}
_FROZEN_ROOTS: set[Path] = set()


def freeze_input_state(root: Path) -> None:
    """Trust an already-prepared input state inside a short-lived batch child.

    Only takes effect when the parent has already prepared ``root``; the parent
    must verify the live input state after the batch finishes.
    """
    if root in _INPUT_STATE:
        _FROZEN_ROOTS.add(root)


def verify_input_state(root: Path, *, workers: int | None = None) -> bool:
    """Return True when ``root`` still has the exact prepared input state."""
    expected = _INPUT_STATE.get(root)
    return expected is None or _input_state_digest(root, workers=workers) == expected


def prepare(root: Path, *, workers: int | None = None) -> None:
    """Invalidate the readers' process caches when canonical inputs change.

    These modules predate operation-scoped document assembly. Their caches
    may be reused between operations only while every chronology, calendar,
    concordance, Bible and bibliography input still has the same file identity.
    No data hash is replaced by these stats: output and provenance seals still
    hash the actual bytes. This only decides whether parsed objects may be reused.
    """
    if root in _FROZEN_ROOTS and root in _INPUT_STATE:
        return
    import _chronology
    import _deuterocanon
    import _psalms
    import _psalter

    state = _input_state_digest(root, workers=workers)
    if _INPUT_STATE.get(root) == state:
        return
    for module in (_chronology, wiring, page, _deuterocanon, _psalms, _psalter):
        for value in vars(module).values():
            clear = getattr(value, "cache_clear", None)
            if getattr(value, "__module__", None) == module.__name__ and callable(clear):
                clear()
    if root not in _INPUT_STATE and len(_INPUT_STATE) >= 4:
        _INPUT_STATE.pop(next(iter(_INPUT_STATE)))
    _INPUT_STATE[root] = state


_WATCHED = (
    ("chronology", (".yaml", ".toml")), ("calendars", (".yaml",)),
    ("bibles", (".yaml", ".json")), ("works", (".toml", ".tsv")),
)


def _scan_input_state(root: Path, *, workers: int | None = None) -> list[tuple]:
    """The sorted file identity rows of every watched input, in path order.

    Every operation (each new `Assembly`) asks this, so it is a scandir walk
    over plain strings: the same files `rglob("*")` reaches -- symlinked
    directories are not descended, symlinked files are followed -- with the
    same stat fields, at a fifth of the cost of building and sorting ~67,000
    Path objects.
    """
    def scan(start: str, suffixes: tuple[str, ...]) -> list[tuple]:
        local: list[tuple] = []
        pending = [start]
        while pending:
            try:
                listing = os.scandir(pending.pop())
            except OSError:
                continue
            with listing:
                for entry in listing:
                    if entry.is_dir(follow_symlinks=False):
                        pending.append(entry.path)
                    elif os.path.splitext(entry.name)[1] in suffixes and entry.is_file():
                        st = entry.stat()
                        local.append((entry.path, st.st_dev, st.st_ino, st.st_size,
                                      st.st_mtime_ns, st.st_ctime_ns))
        return local

    found: list[tuple] = []
    if workers is None:
        counter = getattr(os, "process_cpu_count", None) or os.cpu_count
        workers = min(8, (counter() if callable(counter) else None) or 4)
    else:
        workers = min(8, max(1, workers))
    for tree, suffixes in _WATCHED:
        base = os.path.join(root, "src", "sources", tree)
        try:
            listing = os.scandir(base)
        except OSError:
            continue
        subdirs: list[str] = []
        with listing:
            for entry in listing:
                if entry.is_dir(follow_symlinks=False):
                    subdirs.append(entry.path)
                elif os.path.splitext(entry.name)[1] in suffixes and entry.is_file():
                    st = entry.stat()
                    found.append((entry.path, st.st_dev, st.st_ino, st.st_size,
                                  st.st_mtime_ns, st.st_ctime_ns))
        if workers > 1 and len(subdirs) >= 8:
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=workers) as pool:
                for batch in pool.map(lambda d: scan(d, suffixes), subdirs):
                    found.extend(batch)
        else:
            for d in subdirs:
                found.extend(scan(d, suffixes))
    found.sort()
    return found


def _input_state(root: Path, *, workers: int | None = None) -> tuple:
    """The file identity of every watched input, in path order."""
    return tuple(_scan_input_state(root, workers=workers))


def _input_state_digest(root: Path, *, workers: int | None = None) -> bytes:
    """32-byte digest of `_input_state` so `_INPUT_STATE` retains no 67k tuple."""
    digest = hashlib.sha256()
    for row in _scan_input_state(root, workers=workers):
        digest.update(f"{row[0]}\0{row[1]}:{row[2]}:{row[3]}:{row[4]}:{row[5]}\n".encode("utf-8", "surrogateescape"))
    return digest.digest()


def dependency_trace(context) -> dict[str, list[str]]:
    """The cold read trace of the computation: one independent process.

    Split from `dependencies` so an assembly can run many leaves' traces side
    by side (`Assembly.prefetch_dependencies`); it touches no shared state.
    """
    try:
        return wiring.computation_reads(context.document, root=context.root,
                                        provider=context.provider)
    except wiring.ChronologyWiringError as exc:
        result = _trace_result(exc)
        if isinstance(result, Exception):
            raise
        return result


def _trace_result(value):
    # The absent-input page is intentional. Adding the appointment input
    # changes assembly bytes and therefore the render identity.
    if (isinstance(value, wiring.ChronologyWiringError)
            and "missing appointment dependency:" in str(value)
            and str(value).endswith("research/chronology-inputs.toml")):
        return {"reads": [], "modules": [], "source_files": [], "sources": []}
    return value


def dependency_traces(contexts, jobs):
    """Read the common corpus once in this batch's fresh audited interpreter."""
    root = contexts[0].root
    before = _input_state_digest(root)
    requests = [(context.document, context.provider) for context in contexts]
    traces = wiring.batch_computation_reads(requests, root, jobs)
    if _input_state_digest(root) != before:
        raise wiring.ChronologyWiringError("chronology inputs changed during the dependency traces")
    return [_trace_result(trace) for trace in traces]


def dependencies(context, trace: dict[str, list[str]] | None = None) -> set[Path]:
    """Canonical inputs of the computation, including cited bibliography.

    The chronology adapter owns the cold read trace; the source graph owns
    citation ancestry. Neither a hand-maintained date list nor a generated
    leaf snapshot serves as the dependency authority. ``trace`` is this
    leaf's `dependency_trace`, when the caller has already run it.
    """
    from _document_schema import _evidence_ancestry

    reads = dependency_trace(context) if trace is None else trace
    paths = {context.root / value for key in ("reads", "modules", "source_files")
             for value in reads[key]}
    paths.update(_evidence_ancestry(context.root, set(), source_ids=reads["sources"]))
    paths.update(context.root / name for name in (
        "scripts/document_projections/scriptural_date_location.py",
        "scripts/_proper_chronology_page.py", "scripts/_proper_chronology.py")
                 if (context.root / name).is_file())
    return paths


def render(context) -> dict[str, str]:
    if context.kind not in KINDS:
        raise ValueError(f"{context.document}: {NAME} serves proper leaves, not {context.kind!r}")
    import yaml
    corpus_root = context.root / "src/sources/chronology"
    try:
        found, projected, absent = page.projection(
            context.document, root=context.root, provider=context.provider, corpus_root=corpus_root)
    except yaml.YAMLError as exc:
        raise ValueError(f"{context.document}: malformed Scripture chronology input: {exc}") from exc
    wanted = context.outputs or tuple(OUTPUTS)
    files = {
        OUTPUTS[variant]: page.render(projected, document=context.document, variant=variant,
                                      root=context.root, corpus_root=corpus_root, absent=absent)
        for variant in wanted
    }
    if found is not None and projected is not None:
        files[wiring.RECORD] = wiring.render(found)
        # A proper with no appointed formulary has a record saying so and no
        # rows: the page prints its absent state and inputs neither file.
        if not page.absent_reason(projected, absent):
            files[wiring.ANNOTATIONS_RECORD] = wiring.render_annotations_tex(projected)
            files[wiring.ORIENTATION_TABLE_RECORD] = wiring.render_orientation_table(projected)
    return files


# What makes an authored file a date page: the page's own heading, the former
# per-row notes, or an authored import of the generated table or annotations.
AUTHORED_DATE_PAGE = re.compile(
    r"\\(?:sub)*section\*?\s*\{[^{}]*Scriptural Date and Location[^{}]*\}"
    r"|\\paragraph\*?\s*\{Setting notes\.?\}"
    r"|\\input\s*\{[^{}]*research/chronology-(?:table|annotations)(?:\.tex)?\}")
NOT_AUTHORED = ("generated", "research", "evaluations", "evaluation")


def authored_conflicts(context, generated: frozenset[str]) -> list[str]:
    """Authored TeX in the leaf that still is, or imports, a date page."""
    tex_files: list[Path] = []
    leaf_str = str(context.leaf)
    if os.path.isdir(leaf_str):
        stack: list[tuple[str, bool]] = [(leaf_str, True)]
        while stack:
            current, is_root = stack.pop()
            try:
                listing = os.scandir(current)
            except OSError:
                continue
            with listing:
                for entry in listing:
                    if is_root and entry.name in NOT_AUTHORED:
                        continue
                    if entry.is_dir(follow_symlinks=False):
                        stack.append((entry.path, False))
                    elif entry.name.endswith(".tex") and entry.is_file(follow_symlinks=True):
                        tex_files.append(Path(entry.path))
    found = []
    for path in sorted(tex_files):
        relative = path.relative_to(context.leaf)
        if relative.as_posix() in generated:
            continue
        text = "\n".join(line.split("%", 1)[0] if not line.lstrip().startswith("%") else ""
                         for line in path.read_text(encoding="utf-8").splitlines())
        if AUTHORED_DATE_PAGE.search(text):
            found.append(relative.as_posix())
    return found
