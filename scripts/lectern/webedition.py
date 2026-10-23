"""A web edition, set for a terminal by the site's own renderer and pandoc.

The tracked, reviewed Markdown under `web/<provider>/<leaf>.md` is what the
site renders (guidance/web-editions.md), and the catalogue names the page it
becomes, `web/<provider>/<leaf>.html`: the generator writes that name from
this very file (scripts/_corpus.py:837-854), so the one is followed back to the
other and no path is composed from anything else.

The Markdown is turned into HTML by `scripts/_markdown_render.render_markdown`,
the site's one locked primitive, the call `tools/public-alpha`'s `render_page`
makes. It refuses unless the installed Python Markdown is exactly the version
`requirements-public-alpha.txt` pins, and that refusal is kept: two versions
of the renderer already disagree over 21 of the 137 editions, so a text set by
any other version would not be the text the site publishes. The HTML is then
set by pandoc's `ansi` writer at the reading width; measured over all 137
editions, not one visible letter or digit of the site's HTML is lost, tables
are wrapped to the width, and only an unbreakable URL runs past it.

Nothing falls back. If the renderer refuses or pandoc is missing, the reason
is what the reader is shown, in the place of the text.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from .repo import ROOT, Refused, _Cache

_SET = _Cache(24)

# One SGR sequence, or one OSC 8 hyperlink opening or closing.
_SEQUENCE = re.compile(r"\x1b\[([0-9;]*)m|\x1b\]8;[^;\x1b\x07]*;([^\x1b\x07]*)(?:\x1b\\|\x07)")
_SAFE_URL = re.compile(r"[A-Za-z][A-Za-z0-9+.-]*:[^\s\"'<>\\]+")


def source_of(web: str) -> Path:
    """The tracked Markdown a catalogue's `web` page is rendered from."""
    if not (web.startswith("web/") and web.endswith(".html")):
        raise Refused(f"The catalogue names {web!r} as a web edition, which is not a page under web/.")
    path = (ROOT / (web[: -len(".html")] + ".md")).resolve()
    if ROOT / "web" not in path.parents:
        raise Refused(f"The catalogue names {web!r}, which leads outside web/.")
    if not path.is_file():
        raise Refused(f"The catalogue names {web}, but its tracked source {path.relative_to(ROOT)} "
                      "is not in this checkout, so there is nothing here to set.")
    return path


def _html(markdown_text: str) -> str:
    try:
        from _markdown_render import MarkdownRenderError, render_markdown
    except ImportError as error:  # scripts/ is on the path whenever lectern is
        raise Refused(f"The site's Markdown renderer (scripts/_markdown_render.py) could not be loaded: {error}") \
            from error
    try:
        return render_markdown(markdown_text, ROOT)
    except MarkdownRenderError as error:
        raise Refused(
            f"The site's Markdown renderer refused: {error}. The text is not set by any other version, "
            "because it would not be the text the site publishes. To read it here, run the reader where the "
            "Markdown version requirements-public-alpha.txt pins is installed."
        ) from error


def pandoc_version() -> str:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        return ""
    done = subprocess.run([pandoc, "--version"], capture_output=True, text=True, timeout=30)
    first = done.stdout.splitlines()[0] if done.stdout else ""
    return first.strip()


def _ansi(html: str, columns: int) -> str:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        raise Refused("pandoc is not installed, and it is what sets the site's HTML as terminal text "
                      "(the repository already requires it for tools/web-edition).")
    done = subprocess.run(
        [pandoc, "-f", "html", "-t", "ansi", "--wrap=auto", f"--columns={columns}"],
        input=html, capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    if done.returncode != 0:
        raise Refused(f"pandoc could not set this edition: {(done.stderr or '').strip() or f'exit {done.returncode}'}")
    return done.stdout


def _runs(ansi: str) -> list[tuple[str, str]]:
    """pandoc's emphasis kept, its fixed colours replaced by the surface's accent.

    pandoc marks strong text bold, emphasis italic, a link underlined in a
    colour, and code in a colour on a background. The weights are kept as they
    are; every colour becomes the surface's accent, so the text follows a change
    of theme like everything else drawn here.
    """
    bold = italic = underline = strike = coloured = False
    link = ""
    out: list[tuple[str, str]] = []

    def style() -> str:
        words = []
        if bold:
            words.append("bold")
        if italic:
            words.append("italic")
        if underline or link:
            words.append("underline")
        if strike:
            words.append("strike")
        if coloured or link:
            words.append("$texts-color")
        if link and _SAFE_URL.fullmatch(link):
            words.append(f'link="{link}"')
        return " ".join(words)

    position = 0
    for match in _SEQUENCE.finditer(ansi):
        if match.start() > position:
            out.append((ansi[position:match.start()], style()))
        position = match.end()
        if match.group(1) is None:
            link = match.group(2) or ""
            continue
        codes = [int(code) for code in match.group(1).split(";") if code] or [0]
        index = 0
        while index < len(codes):
            code = codes[index]
            if code == 0:
                bold = italic = underline = strike = coloured = False
            elif code == 1:
                bold = True
            elif code == 22:
                bold = False
            elif code == 3:
                italic = True
            elif code == 23:
                italic = False
            elif code == 4:
                underline = True
            elif code == 24:
                underline = False
            elif code == 9:
                strike = True
            elif code == 29:
                strike = False
            elif code in (38, 48):  # an extended colour: skip its arguments
                coloured = True
                index += 2 if index + 1 < len(codes) and codes[index + 1] == 5 else 4
            elif 30 <= code <= 37 or 90 <= code <= 97 or 40 <= code <= 47 or 100 <= code <= 107:
                coloured = True
            elif code in (39, 49):
                coloured = False
            index += 1
    if position < len(ansi):
        out.append((ansi[position:], style()))
    merged: list[tuple[str, str]] = []
    for text, look in out:
        if merged and merged[-1][1] == look:
            merged[-1] = (merged[-1][0] + text, look)
        elif text:
            merged.append((text, look))
    return merged


_UNAVAILABLE: list = []


def unavailable() -> str | None:
    """Why no web edition can be set on this machine, said before one is asked
    for; None where one can. Asked once: of the renderer with a trivial
    document, so its refusal is its own, and of pandoc."""
    if not _UNAVAILABLE:
        try:
            _ansi(_html("x"), 40)
            _UNAVAILABLE.append(None)
        except Refused as refusal:
            _UNAVAILABLE.append(str(refusal))
    return _UNAVAILABLE[0]


def set_for_terminal(web: str, columns: int) -> dict:
    """The edition's text as styled runs, and how it was set.

    Raises Refused, with the reason, where the text cannot be set faithfully.
    """
    source = source_of(web)
    columns = max(30, int(columns))
    key = (str(source), source.stat().st_mtime_ns, columns)
    held = _SET.get(key)
    if held is not None:
        return held
    html = _html(source.read_text(encoding="utf-8"))
    runs = _runs(_ansi(html, columns))
    from importlib.metadata import version

    return _SET.put(key, {
        "source": str(source.relative_to(ROOT)),
        "runs": runs,
        "columns": columns,
        "markdown": version("Markdown"),
        "pandoc": pandoc_version(),
    })
