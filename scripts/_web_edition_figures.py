"""TikZ figures of web editions: source-identified, compiled by real TeX to SVG.

A web edition cannot carry a TikZ picture as text, so the converter replaces
each picture with a token naming its *source identity* and the site serves the
picture as an SVG compiled from that same source. The identity covers the
standalone document compiled (the leaf's own preamble and the picture), the
bytes of every repository file that preamble inputs, and this generator's
version. It does not cover the TeX toolchain: the SVG bytes depend on it, so
they are never committed and never enter the browser-product descriptor. They
are compiled at site-build time -- in CI inside the pinned print toolchain
image, locally with the host's TeX -- and each figure is compiled twice in
fresh directories, refused unless both SVGs are byte-identical.

Nothing here decides admission or review; the converter and the site do.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile

FIGURE_GENERATOR_VERSION = "triptych-web-figure/v1"
SCHEMA = "triptych-web-figures/v1"
TOKEN_PREFIX = "TRIPTYCHWEBFIGURE"
TOKEN_SUFFIX = "ENDFIGURE"
# The converter appends this to its pandoc shim. Pandoc expands the macro to a
# single alphanumeric word that no Markdown escaping touches.
SHIM_ADDITIONS = (
    "\\newcommand{\\TriptychWebFigure}[1]{" + TOKEN_PREFIX + "#1" + TOKEN_SUFFIX + "}\n"
)
FIGURE_ROUTE = "web-figures"
CAPTION_MACROS = ("caption", "sketchcaption")
# Margin around the picture's own bounding box, as preview's tightpage sets it.
PREVIEW_BORDER = "2pt"
PDFLATEX = ("pdflatex", "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error")

_ID = re.compile(r"[0-9a-f]{64}")
_BEGIN = re.compile(r"\\begin\s*\{tikzpicture\}")
_ENV = re.compile(r"\\(begin|end)\s*\{([^{}\s]+)\}")
_INPUT = re.compile(r"\\(?:input|include)\s*\{([^{}]+)\}")
_TOKEN_LINE = re.compile(
    r"^(?P<quote>(?:[ \t]*>[ \t]?)*)[ \t]*" + TOKEN_PREFIX + r"(?P<id>[0-9a-f]{64})"
    + TOKEN_SUFFIX + r"[ \t]*$",
    re.MULTILINE,
)
_TOKEN_ANYWHERE = re.compile(TOKEN_PREFIX + r"([0-9A-Za-z]*)" + TOKEN_SUFFIX)


class FigureError(ValueError):
    """A picture could not be identified, projected or compiled faithfully."""


def _sha(data: bytes | str) -> str:
    return hashlib.sha256(data.encode("utf-8") if isinstance(data, str) else data).hexdigest()


def mask_comments(text: str) -> str:
    """Blank TeX comments while keeping offsets, so slices of the raw text stay raw."""
    def blank(match: re.Match[str]) -> str:
        start = match.start()
        slashes = 0
        while start - slashes - 1 >= 0 and text[start - slashes - 1] == "\\":
            slashes += 1
        return match.group() if slashes % 2 else " " * len(match.group())
    return re.sub(r"%[^\n]*", blank, text)


def _group(text: str, masked: str, start: int) -> tuple[str, int]:
    """Return the brace group opening at ``start`` and the offset after it."""
    if masked[start:start + 1] != "{":
        raise FigureError("expected a brace group")
    depth, cursor = 0, start
    while cursor < len(text):
        char = masked[cursor]
        if char == "\\":
            cursor += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:cursor], cursor + 1
        cursor += 1
    raise FigureError("unclosed brace group")


def picture_spans(body: str) -> list[tuple[int, int, list[tuple[str, int]]]]:
    """Each tikzpicture's (start, end, enclosing environments outermost-first).

    A body without a picture is returned untouched: its environments are the
    converter's to judge, not this module's.
    """
    masked = mask_comments(body)
    if not _BEGIN.search(masked):
        return []
    stack: list[tuple[str, int]] = []
    spans = []
    active = None
    for match in _ENV.finditer(masked):
        action, name = match.groups()
        if action == "begin":
            if name == "tikzpicture":
                if active is not None:
                    raise FigureError("nested tikzpicture")
                active = (match.start(), list(stack))
            stack.append((name, match.start()))
            continue
        if not stack or stack[-1][0] != name:
            raise FigureError(f"unbalanced environment around a figure: {name}")
        stack.pop()
        if name == "tikzpicture":
            assert active is not None
            spans.append((active[0], match.end(), active[1]))
            active = None
    if active is not None:
        raise FigureError("unclosed tikzpicture")
    if len(spans) != len(_BEGIN.findall(masked)):
        raise FigureError("tikzpicture count differs from its balanced spans")
    return spans


def _environment_end(body: str, masked: str, name: str, start: int) -> int:
    depth = 0
    for match in _ENV.finditer(masked, start):
        action, found = match.groups()
        if found != name:
            continue
        depth += 1 if action == "begin" else -1
        if depth == 0:
            return match.end()
    raise FigureError(f"unclosed environment: {name}")


def _caption(body: str, masked: str, enclosing: list[tuple[str, int]], picture: tuple[int, int]) -> str | None:
    """The caption of the nearest enclosing environment that has one."""
    for name, start in reversed(enclosing):
        end = _environment_end(body, masked, name, start)
        found = []
        for macro in CAPTION_MACROS:
            for match in re.finditer(r"\\" + macro + r"(?![A-Za-z@])\s*(?:\[[^\]]*\])?\s*(?=\{)", masked[start:end]):
                offset = start + match.end()
                if picture[0] <= offset < picture[1]:
                    continue
                found.append(_group(body, masked, offset)[0])
        if len(found) > 1:
            raise FigureError("a figure environment carries more than one caption")
        if found:
            return found[0]
    return None


_NODE = re.compile(r"(?<![A-Za-z@])\\?node(?![A-Za-z@])")


def node_texts(picture: str) -> list[str]:
    """Each node's text in source order: ``\\node[...] (name) at (x,y) {text}``."""
    masked = mask_comments(picture)
    texts = []
    for match in _NODE.finditer(masked):
        cursor, square, paren = match.end(), 0, 0
        while cursor < len(masked):
            char = masked[cursor]
            if char == "\\":
                cursor += 2
                continue
            if char == "[":
                square += 1
            elif char == "]":
                square -= 1
            elif char == "(" and square == 0:
                paren += 1
            elif char == ")" and square == 0:
                paren -= 1
            elif char == "{" and square == 0 and paren == 0:
                text, cursor = _group(picture, masked, cursor)
                texts.append(text)
                break
            elif char == ";" and square == 0 and paren == 0:
                break
            cursor += 1
    return texts


_REPLACEMENTS = (
    (r"\\longrightarrow|\\rightarrow|\\to(?![A-Za-z])", "→"),
    (r"\\longleftarrow|\\leftarrow", "←"),
    (r"\\leftrightarrow|\\longleftrightarrow", "↔"),
    (r"\\cdots|\\ldots|\\dots(?![A-Za-z])", "…"),
    (r"\\times(?![A-Za-z])", "×"),
    (r"\\textperiodcentered(?![A-Za-z])", "·"),
    (r"---", "—"),
    (r"--", "–"),
    (r"``|''", "\""),
    (r"`", "‘"),
    (r"'", "’"),
    (r"\\&", "&"),
    (r"\\%", "%"),
    (r"\\_", "_"),
    (r"\\#", "#"),
    (r"~", " "),
)


def plain_text(tex: str) -> str:
    """A reader-facing plain rendering of a short TeX label or caption."""
    text = mask_comments(tex)
    text = re.sub(r"\\\\(?:\*)?(?:\[[^\]]*\])?", " \u2014 ", text)
    text = re.sub(r"\\(?:par|newline)(?![A-Za-z@])", " \u2014 ", text)
    text = re.sub(r"\\(?:label|ref|pageref|index|hspace\*?|vspace\*?|phantom)\s*\{[^{}]*\}", " ", text)
    # Accent commands carry a character of their own; keep the letter.
    text = re.sub(r"\\['`^\"~=.]\{?([A-Za-z])\}?", r"\1", text)
    text = text.replace("\\$", "\uE000")
    text = text.replace("$", " ")
    for pattern, replacement in _REPLACEMENTS:
        text = re.sub(pattern, replacement, text)
    text = text.replace("\uE000", "$")
    text = re.sub(r"\\(?:[A-Za-z@]+)\*?(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"\\.", " ", text)
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"(?:\s*\u2014\s*)+", " \u2014 ", text).strip(" \u2014")
    return text


def _numbered(labels: list[str]) -> str:
    if len(labels) == 1:
        return labels[0]
    # Numbered, because a label may itself hold a semicolon.
    return "; ".join(f"({number}) {label}" for number, label in enumerate(labels, 1))


def alternative_text(caption: str | None, picture: str) -> str:
    """The figure's text for a reader who cannot see it.

    The SVG sets its words as glyph outlines, so every node text the picture
    carries is part of the alternative; a caption, which also stays visible in
    the body, leads it.
    """
    labels = [label for label in (plain_text(text) for text in node_texts(picture)) if label]
    if caption is not None:
        text = plain_text(caption)
        if not text:
            raise FigureError("a figure caption has no text for its alternative")
        return text + (" Labels in the figure: " + _numbered(labels) if labels else "")
    if not labels:
        raise FigureError("an uncaptioned figure has no node text for its alternative")
    return "Diagram: " + _numbered(labels)


def resolve_input(root: Path, provider: str, name: str) -> Path | None:
    """Resolve an ``\\input`` as the converter and ``TEXINPUTS`` do."""
    src = root / "src"
    for path in (src / provider / name, src / provider / f"{name}.tex", src / name, src / f"{name}.tex"):
        if path.is_file():
            return path
    return None


def input_closure(root: Path, provider: str, head: str) -> list[dict]:
    """Every repository file the preamble inputs, recursively, with its bytes' hash."""
    found: dict[str, str] = {}
    pending = [head]
    while pending:
        text = mask_comments(pending.pop())
        for match in _INPUT.finditer(text):
            name = match.group(1).strip()
            if "\\" in name or "#" in name:
                raise FigureError(f"a figure preamble inputs a computed name: {name}")
            path = resolve_input(root, provider, name)
            if path is None:
                raise FigureError(f"cannot resolve figure preamble input: {name}")
            relative = path.resolve().relative_to(root.resolve()).as_posix()
            if relative in found:
                continue
            body = path.read_bytes()
            found[relative] = _sha(body)
            pending.append(body.decode("utf-8"))
    return [{"path": path, "sha256": found[path]} for path in sorted(found)]


def standalone(head: str, picture: str) -> str:
    """One page holding exactly the picture, set with the leaf's own preamble."""
    head = head.rstrip("\n")
    return (
        f"{head}\n"
        "\\usepackage[active,tightpage]{preview}\n"
        f"\\setlength\\PreviewBorder{{{PREVIEW_BORDER}}}\n"
        "\\PreviewEnvironment{tikzpicture}\n"
        "\\begin{document}\n"
        "\\pagestyle{empty}\n"
        f"{picture}\n"
        "\\end{document}\n"
    )


def identity(tex: str, inputs: list[dict]) -> str:
    return _sha(json.dumps({"generator": FIGURE_GENERATOR_VERSION, "tex": tex, "inputs": inputs},
                           ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def extract(body: str, head: str, *, root: Path, provider: str, entrypoint: Path) -> tuple[str, list[dict]]:
    """Replace each tikzpicture with its token paragraph; return the figure records."""
    spans = picture_spans(body)
    if not spans:
        return body, []
    root = Path(root).resolve()
    if not Path(entrypoint).resolve().is_relative_to(root / "src" / provider):
        raise FigureError("figure entrypoint escapes its provider")
    masked = mask_comments(body)
    inputs = input_closure(root, provider, head)
    records, pieces, cursor = [], [], 0
    for start, end, enclosing in spans:
        picture = body[start:end]
        caption = _caption(body, masked, enclosing, (start, end))
        tex = standalone(head, picture)
        figure = identity(tex, inputs)
        records.append({"id": figure, "alt": alternative_text(caption, picture),
                        "labels": [label for label in (plain_text(text) for text in node_texts(picture)) if label],
                        "captioned": caption is not None, "tex": tex, "inputs": inputs,
                        "provider": provider})
        pieces.extend((body[cursor:start], f"\n\n\\TriptychWebFigure{{{figure}}}\n\n"))
        cursor = end
    pieces.append(body[cursor:])
    return "".join(pieces), records


def strip_figures(text: str) -> str:
    """The text with every tikzpicture removed, for audits of prose sources."""
    spans = picture_spans(text)
    pieces, cursor = [], 0
    for start, end, _ in spans:
        pieces.extend((text[cursor:start], "\n\n"))
        cursor = end
    pieces.append(text[cursor:])
    return "".join(pieces)


def figure_html(record: dict) -> str:
    figure = record["id"]
    if not _ID.fullmatch(figure):
        raise FigureError("invalid figure identity")
    return (f'<figure class="web-figure" data-figure="{figure}">'
            f'<img src="{FIGURE_ROUTE}/{figure}.svg" alt="{html.escape(record["alt"], quote=True)}"'
            ' loading="lazy" decoding="async"></figure>')


def project(markdown: str, records: list[dict]) -> str:
    """Turn every figure token paragraph into the figure's HTML, exactly once each."""
    expected = Counter(record["id"] for record in records)
    by_id = {}
    for record in records:
        if record["id"] in by_id and by_id[record["id"]]["alt"] != record["alt"]:
            raise FigureError("one figure identity carries two alternatives")
        by_id[record["id"]] = record
    found = Counter(match.group("id") for match in _TOKEN_LINE.finditer(markdown))
    anywhere = Counter(_TOKEN_ANYWHERE.findall(markdown))
    if anywhere != found:
        raise FigureError("a figure token does not stand alone on its line")
    if found != expected:
        missing = sorted((expected - found).elements())
        extra = sorted((found - expected).elements())
        raise FigureError("figure tokens differ from the extracted figures: missing="
                          + ",".join(missing[:3]) + " extra=" + ",".join(extra[:3]))

    def replace(match: re.Match[str]) -> str:
        return match.group("quote") + figure_html(by_id[match.group("id")])
    return _TOKEN_LINE.sub(replace, markdown)


# --- compilation -------------------------------------------------------------

_SCRIPT_HEAD = """#!/bin/sh
# Generated by scripts/_web_edition_figures.py. Every figure is compiled twice,
# in two fresh directories, with the same commands; jobs run in parallel.
set -eu
export SOURCE_DATE_EPOCH=0 FORCE_SOURCE_DATE=1 TZ=UTC LC_ALL=C
pdflatex --version | head -n 1 > {versions}/pdflatex.txt
pdftocairo -v 2>&1 | head -n 1 > {versions}/pdftocairo.txt
jobs=$(nproc 2>/dev/null || echo 2)
sort {joblist} | xargs -P "$jobs" -n 1 sh
"""
_SCRIPT_JOB = """set -eu
export SOURCE_DATE_EPOCH=0 FORCE_SOURCE_DATE=1 TZ=UTC LC_ALL=C
cd {job}
TEXINPUTS={texinputs} {pdflatex} figure.tex > compile.log 2>&1 || {{ tail -n 40 compile.log >&2; echo "figure failed: {figure}" >&2; exit 1; }}
pdfinfo figure.pdf | sed -n 's/^Pages: *//p' > pages.txt
pdftocairo -svg -f 1 -l 1 figure.pdf figure.svg
"""


def _runner_command(runner: str, root: Path, script: Path) -> list[str]:
    if runner == "host":
        return ["sh", str(script)]
    if runner.startswith("docker:"):
        image = runner.removeprefix("docker:")
        if not re.fullmatch(r"[a-z0-9][a-z0-9._/-]*(?::[A-Za-z0-9._-]+)?(?:@sha256:[0-9a-f]{64})?", image):
            raise FigureError("docker runner requires an image reference")
        return ["docker", "run", "--rm", "--network", "none",
                "--user", f"{os.getuid()}:{os.getgid()}",
                "--volume", f"{root}:{root}", "--workdir", str(root),
                "--tmpfs", "/tmp", "--env", "HOME=/tmp",
                image, "sh", str(script)]
    raise FigureError(f"unknown figure runner: {runner}")


def compile_figures(records: list[dict], out: Path, *, root: Path, runner: str = "host") -> dict:
    """Compile each distinct figure twice; write ``<id>.svg`` and ``manifest.json``."""
    root = Path(root).resolve()
    out = Path(out).absolute()
    figures: dict[str, dict] = {}
    for record in records:
        if not _ID.fullmatch(record.get("id", "")):
            raise FigureError("invalid figure identity")
        if identity(record["tex"], record["inputs"]) != record["id"]:
            raise FigureError(f"figure source no longer matches its identity: {record['id']}")
        figures.setdefault(record["id"], record)
    out.mkdir(parents=True, exist_ok=True)
    for existing in out.iterdir():
        if existing.name == "manifest.json" or (existing.suffix == ".svg" and _ID.fullmatch(existing.stem)):
            existing.unlink()
        else:
            raise FigureError(f"figure output holds an unrelated file: {existing.name}")
    work_parent = root / ".scratch" / "web-figure-compile"
    work_parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="run-", dir=work_parent))
    try:
        versions = work / "versions"
        versions.mkdir()
        joblist = work / "jobs.txt"
        scripts = []
        for figure, record in sorted(figures.items()):
            provider = record["provider"]
            texinputs = f"{root / 'src' / provider}:{root / 'src'}:"
            for copy in ("a", "b"):
                job = work / figure / copy
                job.mkdir(parents=True)
                (job / "figure.tex").write_text(record["tex"], encoding="utf-8")
                (job / "run.sh").write_text(_SCRIPT_JOB.format(
                    job=shlex.quote(str(job)), figure=figure, texinputs=shlex.quote(texinputs),
                    pdflatex=" ".join(PDFLATEX)), encoding="utf-8")
                scripts.append(str(job / "run.sh"))
        joblist.write_text("".join(f"{line}\n" for line in scripts), encoding="utf-8")
        path = work / "compile.sh"
        path.write_text(_SCRIPT_HEAD.format(versions=shlex.quote(str(versions)),
                                            joblist=shlex.quote(str(joblist))), encoding="utf-8")
        finished = subprocess.run(_runner_command(runner, root, path), capture_output=True, text=True)
        if finished.returncode:
            raise FigureError("figure compilation failed:\n" + (finished.stderr or finished.stdout)[-4000:])
        manifest = {"schema": SCHEMA, "generator": FIGURE_GENERATOR_VERSION, "figures": {},
                    "toolchain": {"runner": runner,
                                  "pdflatex": (versions / "pdflatex.txt").read_text().strip(),
                                  "pdftocairo": (versions / "pdftocairo.txt").read_text().strip()}}
        for figure in sorted(figures):
            first = work / figure / "a"
            second = work / figure / "b"
            if any((job / "pages.txt").read_text().strip() != "1" for job in (first, second)):
                raise FigureError(f"figure did not set exactly one page: {figure}")
            svg = (first / "figure.svg").read_bytes()
            if svg != (second / "figure.svg").read_bytes():
                raise FigureError(f"figure SVG is not deterministic: {figure}")
            if not svg.lstrip().startswith((b"<?xml", b"<svg")) or b"<svg" not in svg:
                raise FigureError(f"figure compiler wrote no SVG: {figure}")
            (out / f"{figure}.svg").write_bytes(svg)
            manifest["figures"][figure] = {"sha256": _sha(svg), "bytes": len(svg)}
        (out / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return manifest
    finally:
        shutil.rmtree(work, ignore_errors=True)


def check(out: Path, figure_ids) -> list[str]:
    """Problems with a compiled figure directory for exactly these identities."""
    out = Path(out)
    try:
        manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"no readable figure manifest: {error}"]
    if manifest.get("schema") != SCHEMA or manifest.get("generator") != FIGURE_GENERATOR_VERSION:
        return ["figure manifest has another schema or generator"]
    wanted, recorded = set(figure_ids), set(manifest.get("figures", {}))
    problems = [f"figure not compiled: {figure}" for figure in sorted(wanted - recorded)]
    problems += [f"figure compiled for no edition: {figure}" for figure in sorted(recorded - wanted)]
    for figure in sorted(wanted & recorded):
        path = out / f"{figure}.svg"
        if path.is_symlink() or not path.is_file():
            problems.append(f"figure SVG missing: {figure}")
        elif _sha(path.read_bytes()) != manifest["figures"][figure]["sha256"]:
            problems.append(f"figure SVG differs from its manifest: {figure}")
    return problems
