"""Expand a web edition's reader comments after the site renders its Markdown.

The converter (tools/web-edition) writes constructs the site's Markdown cannot
express as HTML comments on lines of their own. Python-Markdown passes them
through untouched, so the rendered page carries them in order; this module
turns each into its reader markup and refuses anything unbalanced:

- ``<!-- triptych:answer-key SUMMARY -->`` … ``<!-- /triptych:answer-key -->``
  becomes ``<details class="web-answer-key"><summary>SUMMARY</summary>`` …
  ``</details>``: an answer key is collapsed, never hidden or interleaved.
- adjacent ``<!-- triptych:column -->`` … ``<!-- /triptych:column -->`` blocks
  (a paired, usually bilingual, layout) become one ``div.web-columns`` of
  ``div.web-column`` children, side by side on wide screens and stacked on
  narrow ones. A lone column is plain content.
- every table between ``<!-- triptych:wide -->`` and ``<!-- /triptych:wide -->``
  (a landscape page) gains ``class="web-wide-table"`` and scrolls sideways at a
  readable width instead of squeezing its columns.
- a figure's ``src="web-figures/<id>.svg"`` is made relative to the page.

The markup carries no text of its own beyond an answer key's summary, which the
converter took from the key's own heading.
"""
from __future__ import annotations

import html
import posixpath
import re

FIGURE_ROUTE = "web-figures"
ANSWER_KEY_RE = re.compile(r"<!-- triptych:answer-key (.*?) -->")
ANSWER_KEY_END = "<!-- /triptych:answer-key -->"
COLUMN_START = "<!-- triptych:column -->"
COLUMN_END = "<!-- /triptych:column -->"
WIDE_START = "<!-- triptych:wide -->"
WIDE_END = "<!-- /triptych:wide -->"
MARKER_RE = re.compile(r"<!-- /?triptych:[a-z-]+(?: [^>]*?)? -->")
COLUMN_RUN_RE = re.compile(
    r"(?:" + re.escape(COLUMN_START) + r".*?" + re.escape(COLUMN_END) + r"\s*)+",
    re.DOTALL,
)
FIGURE_SRC_RE = re.compile(r'(<img src=")' + FIGURE_ROUTE + r'/([0-9a-f]{64}\.svg")')


class ReaderMarkupError(ValueError):
    """A reader comment the page cannot carry faithfully."""


def _balanced(page: str, start: str | re.Pattern, end: str, name: str) -> None:
    depth = 0
    pattern = start if isinstance(start, re.Pattern) else re.compile(re.escape(start))
    events = sorted([(match.start(), 1) for match in pattern.finditer(page)]
                    + [(match.start(), -1) for match in re.finditer(re.escape(end), page)])
    for _, step in events:
        depth += step
        if depth not in (0, 1):
            raise ReaderMarkupError(f"unbalanced or nested {name} marks")
    if depth:
        raise ReaderMarkupError(f"unbalanced {name} marks")


def _columns(match: re.Match[str]) -> str:
    run = match.group(0)
    bodies = re.findall(re.escape(COLUMN_START) + r"(.*?)" + re.escape(COLUMN_END), run, re.DOTALL)
    if len(bodies) == 1:
        return bodies[0].strip() + "\n"
    columns = "".join(f'<div class="web-column">{body.strip()}</div>' for body in bodies)
    return f'<div class="web-columns">{columns}</div>\n'


def _answer_key(match: re.Match[str]) -> str:
    summary = html.unescape(match.group(1)).strip()
    if not summary:
        raise ReaderMarkupError("an answer key has no summary")
    return ('<details class="web-answer-key"><summary>'
            + html.escape(summary, quote=False) + "</summary>")


def _wide(page: str) -> str:
    pieces, cursor = [], 0
    for start in re.finditer(re.escape(WIDE_START), page):
        end = page.index(WIDE_END, start.end())
        pieces.append(page[cursor:start.start()])
        inner = page[start.end():end]
        inner = re.sub(r"<table(?=[\s>])(?![^>]*\bclass=)", '<table class="web-wide-table"', inner)
        pieces.append(inner)
        cursor = end + len(WIDE_END)
    pieces.append(page[cursor:])
    return "".join(pieces)


def expand(page: str, route: str) -> str:
    """Return ``page`` (rendered reader HTML at ``route``) with its marks expanded."""
    if "triptych:" not in page and f'src="{FIGURE_ROUTE}/' not in page:
        return page
    _balanced(page, ANSWER_KEY_RE, ANSWER_KEY_END, "answer-key")
    _balanced(page, COLUMN_START, COLUMN_END, "column")
    _balanced(page, WIDE_START, WIDE_END, "wide")
    page = COLUMN_RUN_RE.sub(_columns, page)
    page = _wide(page)
    page = ANSWER_KEY_RE.sub(_answer_key, page).replace(ANSWER_KEY_END, "</details>")
    leftover = MARKER_RE.search(page)
    if leftover is not None:
        raise ReaderMarkupError(f"unknown reader mark: {leftover.group(0)}")
    prefix = posixpath.relpath(FIGURE_ROUTE, posixpath.dirname(route) or ".")
    return FIGURE_SRC_RE.sub(lambda match: match.group(1) + prefix + "/" + match.group(2), page)


def figure_ids(markdown: str) -> list[str]:
    """The figures a converted edition references, in order."""
    return re.findall(r'<img src="' + FIGURE_ROUTE + r'/([0-9a-f]{64})\.svg"', markdown)
