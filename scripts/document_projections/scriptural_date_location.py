"""The Scriptural Date and Location page of a proper study.

Owns, for one proper leaf: the chronology record, its sealed annotations and
the shared orientation-v3 table under ``research/``, and the two generated
page variants under ``generated/``. The record and the page are therefore
refreshed by one command and held current by one check; the page's content
model is ``scripts/_proper_chronology_page.py``.
"""

from __future__ import annotations

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

_INPUT_STATE: dict[Path, tuple] = {}


def prepare(root: Path) -> None:
    """Invalidate the readers' process caches when canonical inputs change.

    These modules predate operation-scoped document assembly. Their caches
    may be reused between operations only while every chronology, calendar,
    concordance, Bible and bibliography input still has the same file identity.
    No data hash is replaced by these stats: output and provenance seals still
    hash the actual bytes. This only decides whether parsed objects may be reused.
    """
    import _chronology
    import _deuterocanon
    import _psalms
    import _psalter

    sources = root / "src/sources"
    paths = set()
    for tree, suffixes in (
        ("chronology", {".yaml", ".toml"}), ("calendars", {".yaml"}),
        ("bibles", {".yaml", ".json"}), ("works", {".toml", ".tsv"}),
    ):
        paths.update(path for path in (sources / tree).rglob("*")
                     if path.suffix in suffixes and path.is_file())
    state = tuple((str(path), stat.st_dev, stat.st_ino, stat.st_size,
                   stat.st_mtime_ns, stat.st_ctime_ns)
                  for path in sorted(paths) for stat in (path.stat(),))
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


def dependency_trace(context) -> dict[str, list[str]]:
    """The cold read trace of the computation: one independent process.

    Split from `dependencies` so an assembly can run many leaves' traces side
    by side (`Assembly.prefetch_dependencies`); it touches no shared state.
    """
    try:
        return wiring.computation_reads(context.document, root=context.root,
                                        provider=context.provider)
    except wiring.ChronologyWiringError as exc:
        if ("missing appointment dependency:" not in str(exc)
                or not str(exc).endswith("research/chronology-inputs.toml")):
            raise
        # The absent-input page is intentional. Adding the appointment input
        # changes assembly bytes and therefore the render identity.
        return {"reads": [], "modules": [], "source_files": [], "sources": []}


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
    found = []
    for path in sorted(context.leaf.rglob("*.tex")):
        relative = path.relative_to(context.leaf)
        if relative.parts[0] in NOT_AUTHORED or relative.as_posix() in generated:
            continue
        text = "\n".join(line.split("%", 1)[0] if not line.lstrip().startswith("%") else ""
                         for line in path.read_text(encoding="utf-8").splitlines())
        if AUTHORED_DATE_PAGE.search(text):
            found.append(relative.as_posix())
    return found
