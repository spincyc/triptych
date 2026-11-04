"""The Scriptural Date and Location page of a proper study.

Owns, for one proper leaf: the chronology record, its sealed annotations and
the shared orientation-v3 table under ``research/``, and the two generated
page variants under ``generated/``. The record and the page are therefore
refreshed by one command and held current by one check; the page's content
model is ``scripts/_proper_chronology_page.py``.
"""

from __future__ import annotations

import re

import _proper_chronology as wiring
import _proper_chronology_page as page

NAME = "scriptural-date-location"
OUTPUTS = {
    page.SECTION: "generated/scriptural-date-location.tex",
    page.PAGE: "generated/scriptural-date-location-page.tex",
}
KINDS = ("proper-1962", "proper-postconciliar")


def render(context) -> dict[str, str]:
    if context.kind not in KINDS:
        raise ValueError(f"{context.document}: {NAME} serves proper leaves, not {context.kind!r}")
    found, projected, absent = page.projection(
        context.document, root=context.root, provider=context.provider)
    files = {
        path: page.render(projected, document=context.document, variant=variant,
                          root=context.root, absent=absent)
        for variant, path in OUTPUTS.items()
    }
    if found is not None and projected is not None:
        files[wiring.RECORD] = wiring.render(found)
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
