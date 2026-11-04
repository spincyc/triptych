"""Web-reader source selection for the Ecclesiastical Latin curriculum.

The course is a small TeX program: packets select lesson units, worksheet
variants and review forms from shared banks, the same exercise source sets a
learner's response space or a keyed answer according to ``\\ifsolutions``, and
memory sheets are generated from etoolbox registries. Pandoc can execute none
of that, so ``tools/web-edition`` refused every curriculum leaf.

This module executes that program for the web, as TeX would: definitions in
document order, groups (``\\begingroup``, environments) with ``\\global``,
``\\newif`` switches, LaTeX counters, the etoolbox registry and list commands,
xstring's fully expanded tests, ``\\NewEnviron`` bodies and ``\\input`` with
``\\endinput``. What it returns is a flattened LaTeX document of ordinary
commands, which the converter then hands to pandoc and audits like any other
leaf. Anything it cannot model -- an unknown conditional, an unbraced macro
argument, a registry error -- is refused, never guessed at.

Two print constructs become reader constructs (``guidance/web-editions.md``):

* a write-in rule (``\\hrulefill``, a ``\\vspace`` above a rule, a thin
  ``\\rule`` blank) becomes a visible response space: a block
  ``<span class="web-response" data-lines="N">`` when it stands alone, an
  inline ``<span class="web-blank" data-size="...">`` inside text or a cell;
* everything set while ``\\ifsolutions`` is true -- the "Answers and Models"
  part of a packet or review -- stays where the PDF sets it, each heading's
  unit wrapped in ``<!-- triptych:answer-key SUMMARY -->`` ...
  ``<!-- /triptych:answer-key -->`` for the site to collapse.

Layout-only material (page breaks, ``\\Needspace``, contents lines, running
heads, decorative rules, frames) carries no text and is dropped; minipages,
coloured boxes, centring and the title page are unwrapped into the flow.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

COURSE = "curriculums/ecclesiastical-latin"
KINDS = frozenset({
    "curriculum-packet", "curriculum-poetry", "curriculum-assessment",
    "curriculum-guide", "curriculum-reference",
})
# Course-format.sty is a document class extension: its hyperref and titlesec
# machinery is print layout. Only its definitions are read, never executed.
DEFINITIONS_ONLY = (COURSE + "/shared/course-format.sty",)
# Shared commands the web shim defines identically, left for the shim to set so
# the converter's own payload audits (\Latin, \Term) still see them.
SHIM_OWNED = {"Latin": r"\textit{#1}", "Term": r"\textbf{#1}"}
SHIM_ADDITIONS = ""

# Tokens pandoc passes through as words. The hyphens keep a \Latin payload
# that holds a blank out of the converter's verbatim payload audit, which could
# not match the blank's HTML; the words around it remain in coverage.
RESPONSE = "TRIPTYCHCURRICULUM-RESPONSE-"
KEY_ON, KEY_OFF = "TRIPTYCHCURRICULUM-KEY-ON", "TRIPTYCHCURRICULUM-KEY-OFF"
MATH = "TRIPTYCHCURRICULUM-MATH-"
TOKEN_RE = re.compile(r"TRIPTYCHCURRICULUM[-A-Z0-9]*")
RESPONSE_RE = re.compile(RESPONSE + r"([0-9]+)-END")
MATH_RE = re.compile(MATH + r"([0-9]+)-END")

CS_RE = re.compile(r"\\([A-Za-z@]+|.)", re.DOTALL)
COMMENT_RE = re.compile(r"\\.|%[^\n]*(?:\n[ \t]*)?", re.DOTALL)
PARAMETER_RE = re.compile(r"#(#|[1-9])")
PRIMITIVE_IFS = frozenset("if ifx ifnum ifdim ifodd ifcase ifcat ifdefined ifcsname ifvmode "
                          "ifhmode ifmmode ifinner".split())
HEADINGS = {"part": "section", "chapter": "subsection", "section": "subsubsection",
            "subsection": "paragraph", "subsubsection": "subparagraph"}
# Commands that carry no reader text, with the brace arguments they take.
LAYOUT = {"Needspace": 1, "addcontentsline": 3, "markboth": 2, "markright": 1,
          "pagenumbering": 1, "thispagestyle": 1, "pagestyle": 1, "setlength": 2,
          "addtolength": 2, "fontsize": 2, "phantomsection": 0, "removelastskip": 0,
          "tableofcontents": 0, "clearpage": 0, "newpage": 0, "vfill": 0, "sloppy": 0,
          "raggedbottom": 0, "selectfont": 0, "protect": 0, "nopagebreak": 0,
          "pagebreak": 0, "makeatletter": 0, "makeatother": 0, "relax": 0, "long": 0}
REGISTERS = frozenset("hbadness vbadness tolerance pretolerance emergencystretch".split())
PASS_ENVIRONMENTS = frozenset("enumerate itemize description quote quotation verse".split())
UNWRAP_ENVIRONMENTS = {"minipage": 1, "titlepage": 0, "center": 0, "flushleft": 0,
                       "flushright": 0, "multicols": 1}
TABLE_ENVIRONMENTS = {"tabular": 0, "tabularx": 1, "xltabular": 1, "longtable": 0}
# Column types course-format.sty declares with \newcolumntype, as paragraph
# columns pandoc reads; X and Y share the remaining width in print.
COLUMN_RE = re.compile(r"@\{[^{}]*\}|[PCpmb]\{([^{}]*)\}|[XY]|[lcr|]|\s+|[<>]\{[^{}]*\}")
INCHES = {"in": 1.0, "pt": 1 / 72.27, "bp": 1 / 72, "mm": 1 / 25.4, "cm": 1 / 2.54,
          "em": 0.15, "ex": 0.07, "baselineskip": 0.19}
LINE_INCHES = 0.3


class CurriculumError(ValueError):
    """A curriculum construct the web selection cannot set as TeX would."""


def applies(kind: str) -> bool:
    return kind in KINDS


def uncomment(text: str) -> str:
    """Remove comments as TeX reads them: through the line end and the indent after."""
    return COMMENT_RE.sub(lambda match: match.group(0) if match.group(0)[0] == "\\" else "", text)


# TeX substitutes tokens, not characters: an argument ending in a control word
# never joins the letters after it, nor a body's control word the letters of
# an argument. This separator keeps those boundaries and is set as nothing.
SEPARATOR = "\x01"
TRAILING_WORD_RE = re.compile(r"\\[A-Za-z@]+$")


def substitute(body: str, arguments: list[str]) -> str:
    def replace(match: re.Match[str]) -> str:
        if match.group(1) == "#":
            return "#"
        index = int(match.group(1)) - 1
        if index >= len(arguments):
            raise CurriculumError(f"parameter #{index + 1} has no argument")
        value = arguments[index]
        before, after = body[:match.start()], body[match.end():match.end() + 1]
        if TRAILING_WORD_RE.search(before) and re.match(r"[A-Za-z@]", value):
            value = SEPARATOR + value
        if TRAILING_WORD_RE.search(value) and re.match(r"[A-Za-z@]", after):
            value += SEPARATOR
        return value
    return PARAMETER_RE.sub(replace, body)


def inches(value: str) -> float | None:
    match = re.fullmatch(r"\s*([0-9]*\.?[0-9]+)\s*\\?(in|pt|bp|mm|cm|em|ex|baselineskip)\s*", value)
    return float(match.group(1)) * INCHES[match.group(2)] if match else None


class _Course:
    def __init__(self, root: Path, provider: str, leaf: str, library):
        self.root, self.web, self.provider = Path(root).resolve(), library, provider
        self.base = self.root / "src" / provider
        self.entry = self.base / leaf / "main.tex"
        if not self.entry.is_file():
            raise CurriculumError(f"no curriculum entrypoint: {self.entry}")
        self.macros: dict[str, tuple[int, str | None, str]] = {}
        self.environs: dict[str, tuple[int, str | None, str]] = {}
        self.environments: dict[str, tuple[int, str | None, str, str]] = {}
        self.bools: dict[str, bool] = {}
        self.counters: dict[str, int] = {}
        self.children: dict[str, list[str]] = {}
        self.frames: list[tuple] = []
        self.global_next = False
        self.files: dict[Path, str] = {}
        self.active: list[Path] = []
        self.endinput = False
        self.started = self.finished = False
        self.keymode = False
        self.responses: list[dict] = []
        self.maths: list[str] = []
        self.metadata: dict[str, str] = {}

    # --- reading -------------------------------------------------------

    def resolve(self, name: str) -> Path:
        name = name.strip()
        for base in (self.base, self.root / "src"):
            for path in (base / name, base / f"{name}.tex"):
                if path.is_file():
                    path = path.resolve()
                    if not path.is_relative_to(self.root / "src"):
                        break
                    return path
        raise CurriculumError(f"cannot resolve \\input{{{name}}}")

    def read(self, path: Path) -> str:
        raw = path.read_text(encoding="utf-8")
        self.files.setdefault(path, raw)
        return uncomment(raw)

    def group(self, text: str, pos: int) -> tuple[str, int]:
        cursor = self.web.skip_gap(text, pos)
        if text[cursor:cursor + 1] != "{":
            # TeX also takes one unbraced token; the course never relies on it
            # except for control sequences handed to etoolbox commands.
            match = CS_RE.match(text, cursor)
            if match is None:
                raise CurriculumError("expected an argument near " + repr(text[cursor:cursor + 60]))
            return match.group(0), match.end()
        try:
            return self.web.brace_group(text, cursor)
        except Exception as exc:
            raise CurriculumError(f"unbalanced argument near {text[cursor:cursor + 60]!r}") from exc

    def arguments(self, text: str, pos: int, count: int) -> tuple[list[str], int]:
        values = []
        for _ in range(count):
            value, pos = self.group(text, pos)
            values.append(value)
        return values, pos

    def optional(self, text: str, pos: int) -> tuple[str | None, int]:
        cursor = self.web.skip_gap(text, pos)
        if text[cursor:cursor + 1] != "[":
            return None, pos
        depth = 0
        for index in range(cursor, len(text)):
            if text[index] in "[{":
                depth += 1
            elif text[index] in "]}":
                depth -= 1
                if depth == 0:
                    return text[cursor + 1:index], index + 1
        raise CurriculumError("unclosed optional argument")

    def name_argument(self, text: str, pos: int) -> tuple[str, int]:
        """A control sequence given braced or bare: ``{\\name}`` or ``\\name``."""
        value, pos = self.group(text, pos)
        match = re.fullmatch(r"\s*\\([A-Za-z@]+)\s*", value)
        if match is None:
            raise CurriculumError(f"expected a control sequence, found {value!r}")
        return match.group(1), pos

    def scalar(self, text: str) -> str:
        value = self.eval(text, 1)
        if "\\" in value or "{" in value or "}" in value:
            raise CurriculumError(f"cannot expand {text!r} to plain text: {value!r}")
        return value.strip()

    # --- scopes --------------------------------------------------------

    def push(self, name: str) -> None:
        self.frames.append((name, dict(self.macros), dict(self.environs),
                            dict(self.environments), dict(self.bools)))

    def pop(self, name: str) -> None:
        if not self.frames or self.frames[-1][0] != name:
            raise CurriculumError(f"unbalanced group: closing {name} inside "
                                  f"{self.frames[-1][0] if self.frames else 'nothing'}")
        _, self.macros, self.environs, self.environments, self.bools = self.frames.pop()

    def assign(self, table: str, name: str, value) -> None:
        getattr(self, table)[name] = value
        if self.global_next:
            index = {"macros": 1, "environs": 2, "environments": 3, "bools": 4}[table]
            for frame in self.frames:
                frame[index][name] = value
        self.global_next = False

    # --- definitions ---------------------------------------------------

    def signature(self, text: str, pos: int) -> tuple[int, str | None, int]:
        count, default = 0, None
        value, pos = self.optional(text, pos)
        if value is not None:
            count = int(value)
            default, pos = self.optional(text, pos)
        return count, default, pos

    def define_command(self, name: str, text: str, pos: int) -> int:
        if text[pos:pos + 1] == "*":
            pos += 1
        target, pos = self.name_argument(text, pos)
        count, default, pos = self.signature(text, pos)
        body, pos = self.group(text, pos)
        defined = target in self.macros
        if name == "providecommand" and defined:
            self.global_next = False
            return pos
        if name == "newcommand" and defined:
            raise CurriculumError(f"\\newcommand of an existing \\{target}")
        self.assign("macros", target, (count, default, body))
        return pos

    def define_environment(self, name: str, text: str, pos: int) -> int:
        if text[pos:pos + 1] == "*":
            pos += 1
        target, pos = self.group(text, pos)
        count, default, pos = self.signature(text, pos)
        if name in {"NewEnviron", "RenewEnviron"}:
            body, pos = self.group(text, pos)
            self.assign("environs", target.strip(), (count, default, body))
        else:
            (opening, closing), pos = self.arguments(text, pos, 2)
            self.assign("environments", target.strip(), (count, default, opening, closing))
        return pos

    def define_primitive(self, name: str, text: str, pos: int) -> int:
        if name in {"edef", "xdef"}:
            raise CurriculumError(f"\\{name} expands at definition time and is not modelled")
        match = CS_RE.match(text, self.web.skip_gap(text, pos))
        if match is None:
            raise CurriculumError(f"\\{name} without a control sequence")
        brace = text.find("{", match.end())
        parameters = text[match.end():brace]
        if brace < 0 or not re.fullmatch(r"\s*(?:#[1-9])*\s*", parameters):
            raise CurriculumError(f"\\{name}\\{match.group(1)} has a delimited parameter text")
        count = parameters.count("#")
        body, pos = self.web.brace_group(text, brace)
        if name == "gdef":
            self.global_next = True
        self.assign("macros", match.group(1), (count, None, body))
        return pos

    def harvest(self, path: Path) -> None:
        """Read a definitions-only file: record definitions, execute nothing."""
        text = self.read(path)
        pattern = re.compile(r"\\(newcommand|renewcommand|providecommand|NewEnviron|"
                             r"newenvironment|renewenvironment|newif|newcounter)(?![A-Za-z@])")
        pos = 0
        while (match := pattern.search(text, pos)) is not None:
            name = match.group(1)
            if name in {"newcommand", "renewcommand", "providecommand"}:
                try:
                    pos = self.define_command(name, text, match.end())
                except CurriculumError:
                    # An unbraced \renewcommand*\l@... restyles print contents.
                    pos = match.end()
            elif name == "newif":
                pos = self.newif(text, match.end())
            elif name == "newcounter":
                pos = self.newcounter(text, match.end())
            else:
                pos = self.define_environment(name, text, match.end())

    def newif(self, text: str, pos: int) -> int:
        match = re.compile(r"\s*\\if([A-Za-z@]+)").match(text, pos)
        if match is None:
            raise CurriculumError("\\newif without a switch")
        self.assign("bools", match.group(1), False)
        return match.end()

    def newcounter(self, text: str, pos: int) -> int:
        name, pos = self.group(text, pos)
        parent, pos = self.optional(text, pos)
        self.counters[name.strip()] = 0
        if parent:
            self.children.setdefault(parent.strip(), []).append(name.strip())
        return pos

    def step(self, name: str) -> None:
        if name not in self.counters:
            raise CurriculumError(f"unknown counter {name}")
        self.counters[name] += 1
        pending = list(self.children.get(name, ()))
        while pending:
            child = pending.pop()
            self.counters[child] = 0
            pending.extend(self.children.get(child, ()))

    # --- conditionals --------------------------------------------------

    def branches(self, text: str, pos: int) -> tuple[str, str, int]:
        depth, split = 1, None
        for match in CS_RE.finditer(text, pos):
            word = match.group(1)
            if word in PRIMITIVE_IFS or (word.startswith("if") and word[2:] in self.bools):
                depth += 1
            elif word == "fi":
                depth -= 1
                if depth == 0:
                    if split is None:
                        return text[pos:match.start()], "", match.end()
                    return text[pos:split.start()], text[split.end():match.start()], match.end()
            elif word == "else" and depth == 1:
                split = match
        raise CurriculumError("unclosed conditional")

    def number(self, text: str, pos: int) -> tuple[int, int]:
        pos = self.web.skip_gap(text, pos)
        if text.startswith("\\value", pos):
            name, pos = self.group(text, pos + len("\\value"))
            if name.strip() not in self.counters:
                raise CurriculumError(f"unknown counter {name}")
            return self.counters[name.strip()], pos
        match = re.compile(r"(-?[0-9]+) ?").match(text, pos)
        if match is None:
            raise CurriculumError("unmodelled \\ifnum operand near " + repr(text[pos:pos + 40]))
        return int(match.group(1)), match.end()

    # --- reader constructs ---------------------------------------------

    def response(self, kind: str, lines: int = 1, size: str = "fill") -> str:
        self.responses.append({"kind": kind, "lines": max(1, lines), "size": size})
        return f" {RESPONSE}{len(self.responses)}-END "

    def rule_after_space(self, text: str, pos: int, height: str) -> tuple[str, int] | None:
        match = re.compile(r"\s*\\(hrulefill|hrule)(?![A-Za-z@])").match(text, pos)
        if match is None:
            return None
        size = inches(height)
        if size is None:
            raise CurriculumError(f"unmodelled response height {height!r}")
        return self.response("line", round(size / LINE_INCHES)), match.end()

    def rule(self, text: str, pos: int) -> tuple[str, int]:
        _, pos = self.optional(text, pos)
        (width, height), pos = self.arguments(text, pos, 2)
        breadth = inches(width)
        if breadth == 0:
            return "", pos  # a strut
        if width.strip() in {r"\linewidth", r"\textwidth"} or (inches(height) or 0) >= 0.01:
            return "", pos  # a decorative full-width or heavy rule
        if breadth is None:
            raise CurriculumError(f"unmodelled rule width {width!r}")
        return self.response("blank", size="long" if breadth >= 2 else "short"), pos

    def display_math(self, text: str, pos: int) -> tuple[str, int]:
        end = text.find("\\]", pos)
        if end < 0:
            raise CurriculumError("unclosed display math")
        # The course's displays are metrical schemes. Pandoc renders a display
        # as loose text and refuses a labelled underbrace, so each is set as
        # MathML from the finite scansion language the sources use.
        self.maths.append(scansion_mathml(text[pos:end]))
        # A display stands inside its paragraph, as TeX sets it.
        return f" {MATH}{len(self.maths)}-END ", end + 2

    def hypersetup(self, value: str) -> None:
        for key in ("pdftitle", "pdfsubject"):
            match = re.search(key + r"\s*=\s*\{", value)
            if match:
                text, _ = self.web.brace_group(value, match.end() - 1)
                self.metadata[key] = plain(self.eval(text, 1))

    # --- environments --------------------------------------------------

    def environment_body(self, text: str, pos: int, name: str) -> tuple[str, int]:
        pattern = re.compile(r"\\(begin|end)\s*\{" + re.escape(name) + r"\}")
        depth = 1
        for match in pattern.finditer(text, pos):
            depth += 1 if match.group(1) == "begin" else -1
            if depth == 0:
                return text[pos:match.start()], match.end()
        raise CurriculumError(f"unclosed environment {name}")

    def call_arguments(self, text: str, pos: int, count: int, default: str | None):
        values = []
        for index in range(count):
            if index == 0 and default is not None:
                value, pos = self.optional(text, pos)
                values.append(default if value is None else value)
                continue
            value, pos = self.group(text, pos)
            values.append(value)
        return values, pos

    def begin(self, text: str, pos: int, depth: int) -> tuple[str, int]:
        name, pos = self.group(text, pos)
        name = name.strip()
        if name == "document":
            self.started = True
            return "\\begin{document}\n", pos
        if name in self.environs:
            count, default, code = self.environs[name]
            values, pos = self.call_arguments(text, pos, count, default)
            body, pos = self.environment_body(text, pos, name)
            expanded = re.sub(r"\\BODY(?![A-Za-z@])", lambda _: body, substitute(code, values))
            self.push(name)
            output = self.eval(expanded, depth + 1)
            self.pop(name)
            return output, pos
        if name in self.environments:
            count, default, opening, closing = self.environments[name]
            values, pos = self.call_arguments(text, pos, count, default)
            body, pos = self.environment_body(text, pos, name)
            self.push(name)
            output = self.eval(substitute(opening, values) + body + closing, depth + 1)
            self.pop(name)
            return output, pos
        if name in UNWRAP_ENVIRONMENTS:
            _, pos = self.optional(text, pos)
            _, pos = self.optional(text, pos)
            _, pos = self.arguments(text, pos, UNWRAP_ENVIRONMENTS[name])
            self.push(name)
            return "\n", pos
        if name in TABLE_ENVIRONMENTS:
            _, pos = self.arguments(text, pos, TABLE_ENVIRONMENTS[name])
            _, pos = self.optional(text, pos)
            spec, pos = self.group(text, pos)
            self.push(name)
            target = "longtable" if name in {"xltabular", "longtable"} else "tabular"
            return f"\\begin{{{target}}}{{{column_spec(spec)}}}", pos
        if name in PASS_ENVIRONMENTS:
            option, pos = self.optional(text, pos)
            self.push(name)
            return f"\\begin{{{name}}}" + ("" if option is None else f"[{option}]"), pos
        raise CurriculumError(f"unmodelled environment {name}")

    def end(self, text: str, pos: int) -> tuple[str, int]:
        name, pos = self.group(text, pos)
        name = name.strip()
        if name == "document":
            self.finished = True
            return "\n\\end{document}\n", pos
        self.pop(name)
        if name in UNWRAP_ENVIRONMENTS:
            return "\n", pos
        if name in TABLE_ENVIRONMENTS:
            return "\\end{" + ("longtable" if name in {"xltabular", "longtable"} else "tabular") + "}", pos
        if name in PASS_ENVIRONMENTS:
            return f"\\end{{{name}}}", pos
        raise CurriculumError(f"unmodelled environment end {name}")

    # --- inputs --------------------------------------------------------

    def include(self, name: str, depth: int) -> str:
        name = self.scalar(name)
        path = self.resolve(name)
        relative = path.relative_to(self.root / "src").as_posix()
        if path.is_relative_to(self.base):
            relative = path.relative_to(self.base).as_posix()
        if relative == "common/preamble.tex":
            self.read(path)
            return ""
        if relative in DEFINITIONS_ONLY:
            self.harvest(path)
            return ""
        if path in self.active:
            raise CurriculumError(f"recursive \\input of {relative}")
        self.active.append(path)
        try:
            output = self.eval(self.read(path), depth + 1)
        finally:
            self.active.pop()
            self.endinput = False
        return output

    # --- evaluation ----------------------------------------------------

    def eval(self, text: str, depth: int = 0) -> str:
        if depth > 400:
            raise CurriculumError("macro expansion is too deep")
        out, pos = [], 0
        while pos < len(text) and not self.finished and not self.endinput:
            index = text.find("\\", pos)
            if index < 0:
                out.append(text[pos:].replace(SEPARATOR, ""))
                break
            out.append(text[pos:index].replace(SEPARATOR, ""))
            match = CS_RE.match(text, index)
            piece, pos = self.command(match.group(1), text, match.end(), depth)
            out.append(piece)
            solutions = self.bools.get("solutions", False)
            if self.started and solutions != self.keymode:
                self.keymode = solutions
                out.append(f"\n\n{KEY_ON if solutions else KEY_OFF}\n\n")
        return "".join(out)

    def command(self, name: str, text: str, pos: int, depth: int) -> tuple[str, int]:
        if name in {"newcommand", "renewcommand", "providecommand"}:
            return "", self.define_command(name, text, pos)
        if name in {"NewEnviron", "RenewEnviron", "newenvironment", "renewenvironment"}:
            return "", self.define_environment(name, text, pos)
        if name in {"def", "gdef", "edef", "xdef"}:
            return "", self.define_primitive(name, text, pos)
        if name == "global":
            self.global_next = True
            return "", pos
        if name == "let":
            target = CS_RE.match(text, self.web.skip_gap(text, pos))
            cursor = self.web.skip_gap(text, target.end())
            if text[cursor:cursor + 1] == "=":
                cursor = self.web.skip_gap(text, cursor + 1)
            source = CS_RE.match(text, cursor)
            if source is None or source.group(1) not in self.macros:
                raise CurriculumError(f"\\let\\{target.group(1)} copies an unmodelled control sequence")
            self.assign("macros", target.group(1), self.macros[source.group(1)])
            return "", source.end()
        if name == "newif":
            return "", self.newif(text, pos)
        if name == "newcounter":
            return "", self.newcounter(text, pos)
        if name in {"setcounter", "addtocounter"}:
            (counter, value), pos = self.arguments(text, pos, 2)
            counter = counter.strip()
            if counter not in self.counters:
                raise CurriculumError(f"unknown counter {counter}")
            amount = int(self.scalar(value))
            self.counters[counter] = amount if name == "setcounter" else self.counters[counter] + amount
            return "", pos
        if name in {"stepcounter", "refstepcounter"}:
            counter, pos = self.group(text, pos)
            self.step(counter.strip())
            return "", pos
        if name == "arabic":
            if text[pos:pos + 1] == "*":
                return "\\arabic*", pos + 1
            counter, pos = self.group(text, pos)
            if counter.strip() not in self.counters:
                raise CurriculumError(f"unknown counter {counter}")
            return str(self.counters[counter.strip()]), pos
        if name in {"csdef", "csgdef"}:
            (key, body), pos = self.arguments(text, pos, 2)
            self.global_next = self.global_next or name == "csgdef"
            self.assign("macros", self.scalar(key), (0, None, body))
            return "", pos
        if name in {"csappto", "csgappto", "appto", "gappto", "preto", "gpreto"}:
            if name.startswith("cs"):
                key, pos = self.group(text, pos)
                key = self.scalar(key)
            else:
                key, pos = self.name_argument(text, pos)
            addition, pos = self.group(text, pos)
            current = self.macros.get(key, (0, None, ""))[2]
            self.global_next = self.global_next or name in {"csgappto", "gappto", "gpreto"}
            value = addition + current if name.endswith("preto") else current + addition
            self.assign("macros", key, (0, None, value))
            return "", pos
        if name == "csuse":
            key, pos = self.group(text, pos)
            macro = self.macros.get(self.scalar(key))
            return ("" if macro is None else self.eval(macro[2], depth + 1)), pos
        if name == "ifcsdef":
            (key, yes, no), pos = self.arguments(text, pos, 3)
            return self.eval(yes if self.scalar(key) in self.macros else no, depth + 1), pos
        if name == "ifdefempty":
            key, pos = self.name_argument(text, pos)
            (yes, no), pos = self.arguments(text, pos, 2)
            macro = self.macros.get(key)
            empty = macro is not None and macro[0] == 0 and not macro[2].strip()
            return self.eval(yes if empty else no, depth + 1), pos
        if name in {"IfStrEq", "IfSubStr"}:
            (left, right, yes, no), pos = self.arguments(text, pos, 4)
            left, right = self.scalar(left), self.scalar(right)
            truth = left == right if name == "IfStrEq" else right in left
            return self.eval(yes if truth else no, depth + 1), pos
        if name in {"forcsvlist", "docsvlist"}:
            if name == "forcsvlist":
                handler, pos = self.group(text, pos)
            else:
                handler = "\\do"
            items, pos = self.group(text, pos)
            calls = "".join(handler + "{" + item.strip() + "}"
                            for item in items.split(",") if item.strip())
            return self.eval(calls, depth + 1), pos
        if name in {"input", "include"}:
            target, pos = self.group(text, pos)
            return self.include(target, depth), pos
        if name == "InputIfFileExists":
            (target, yes, no), pos = self.arguments(text, pos, 3)
            try:
                self.resolve(self.scalar(target))
            except CurriculumError:
                return self.eval(no, depth + 1), pos
            return self.eval(yes, depth + 1) + self.include(target, depth), pos
        if name == "endinput":
            self.endinput = True
            return "", pos
        if name == "PackageError":
            (package, message, _), pos = self.arguments(text, pos, 3)
            raise CurriculumError(f"{package}: {message}")
        if name in {"begingroup", "bgroup"}:
            self.push("group")
            return "", pos
        if name in {"endgroup", "egroup"}:
            self.pop("group")
            return "", pos
        if name == "begin":
            return self.begin(text, pos, depth)
        if name == "end":
            return self.end(text, pos)
        if name in HEADINGS:
            star = text[pos:pos + 1] == "*"
            _, cursor = self.optional(text, pos + star)
            title, pos = self.group(text, cursor)
            if name == "part" and self.bools.get("solutions"):
                raise CurriculumError("a Part opens inside an answer key")
            rendered = " ".join(self.eval(title, depth + 1).split())
            return f"\n\n\\{HEADINGS[name]}{'*' if star else ''}{{{rendered}}}\n\n", pos
        if name == "noalign":
            body, pos = self.group(text, pos)
            if self.eval(body, depth + 1).strip():
                raise CurriculumError("\\noalign sets material between table rows")
            return "", pos
        if name == "hypersetup":
            value, pos = self.group(text, pos)
            self.hypersetup(value)
            return "", pos
        if name in LAYOUT:
            if text[pos:pos + 1] == "*":
                pos += 1
            _, pos = self.arguments(text, pos, LAYOUT[name])
            return "", pos
        if name in REGISTERS:
            match = re.compile(r"\s*=?\s*-?[0-9.]+\s*(?:pt|em|in)?").match(text, pos)
            return "", match.end() if match else pos
        if name == "vspace":
            star = text[pos:pos + 1] == "*"
            height, pos = self.group(text, pos + star)
            ruled = self.rule_after_space(text, pos, height)
            return ruled if ruled is not None else ("", pos)
        if name == "hrulefill":
            return self.response("line"), pos
        if name == "hrule":
            return "", pos  # a frame line; write-in rules come after a \vspace
        if name == "rule":
            return self.rule(text, pos)
        if name == "fcolorbox":
            (_, _, content), pos = self.arguments(text, pos, 3)
            return self.eval(content, depth + 1), pos
        if name == "space":
            return " ", pos
        if name == "[":
            return self.display_math(text, pos)
        if name == "ifdim":
            return self.layout_conditional(text, pos)
        if name == "ifnum":
            left, cursor = self.number(text, pos)
            cursor = self.web.skip_gap(text, cursor)
            relation = text[cursor:cursor + 1]
            right, cursor = self.number(text, cursor + 1)
            truth = {"=": left == right, "<": left < right, ">": left > right}.get(relation)
            if truth is None:
                raise CurriculumError(f"unmodelled \\ifnum relation {relation!r}")
            yes, no, pos = self.branches(text, cursor)
            return self.eval(yes if truth else no, depth + 1), pos
        if name.startswith("if") and name[2:] in self.bools:
            truth = self.bools[name[2:]]
            if name == "ifmemorysolutions" and truth and not self.bools.get("solutions"):
                raise CurriculumError("a memory key is set outside the answers")
            yes, no, pos = self.branches(text, pos)
            return self.eval(yes if truth else no, depth + 1), pos
        if name in PRIMITIVE_IFS or name in {"else", "fi"}:
            raise CurriculumError(f"unmodelled conditional \\{name}")
        for suffix, value in (("true", True), ("false", False)):
            if name.endswith(suffix) and name[:-len(suffix)] in self.bools:
                self.assign("bools", name[:-len(suffix)], value)
                return "", pos
        if name in self.macros and not (name in SHIM_OWNED and self.macros[name][2] == SHIM_OWNED[name]):
            count, default, body = self.macros[name]
            values, pos = self.call_arguments(text, pos, count, default)
            if count == 0 and re.match(r"[A-Za-z@]", name):
                pos = len(text) - len(text[pos:].lstrip(" \t"))
            return self.eval(substitute(body, values), depth + 1), pos
        return "\\" + name, pos

    def layout_conditional(self, text: str, pos: int) -> tuple[str, int]:
        match = re.compile(r"\s*\\pagetotal\s*=\s*0pt").match(text, pos)
        if match is None:
            raise CurriculumError("unmodelled \\ifdim")
        yes, no, pos = self.branches(text, match.end())
        for branch in (yes, no):
            if re.sub(r"\\(?:clearpage|newpage)(?![A-Za-z@])|\s", "", branch):
                raise CurriculumError("a page-position conditional sets text")
        return "", pos

    # --- result --------------------------------------------------------

    def run(self) -> dict:
        source = self.eval(self.read(self.entry.resolve()))
        if not self.finished:
            raise CurriculumError("the curriculum document never ended")
        if self.frames:
            raise CurriculumError("unclosed groups: " + ", ".join(frame[0] for frame in self.frames))
        if self.keymode:
            raise CurriculumError("the document ends inside an answer key")
        if "pdftitle" not in self.metadata:
            raise CurriculumError("no pdftitle")
        begin = source.index("\\begin{document}") + len("\\begin{document}")
        body = source[begin:source.rindex("\\end{document}")]
        body = re.sub(r"\n{3,}", "\n\n", body)
        if re.search(r"\\(?:input|include)(?![A-Za-z@])", body):
            raise CurriculumError("an \\input survived selection")
        head = ("\\hypersetup{pdftitle={" + self.metadata["pdftitle"] + "},pdfsubject={"
                + self.metadata.get("pdfsubject", "") + "}}\n")
        return {"head": head, "body": body}


# --- scansion displays ---------------------------------------------------

SYMBOLS = {"smile": "⌣", "times": "×", "mid": "∣", "Vert": "‖", "parallel": "∥"}


def scansion_mathml(source: str) -> str:
    """The course's labelled metrical schemes as MathML, refusing anything else."""
    def row(text: str) -> str:
        parts, pos = [], 0
        while pos < len(text):
            char = text[pos]
            if char.isspace():
                pos += 1
            elif char == "\\":
                match = CS_RE.match(text, pos)
                word, pos = match.group(1), match.end()
                if word in SYMBOLS:
                    parts.append(f"<mo>{SYMBOLS[word]}</mo>")
                elif word in {",", ";", ":", " ", "!"}:
                    continue
                elif word == "text":
                    value, pos = braced(text, pos)
                    parts.append(text_node(value))
                elif word == "underbrace":
                    body, pos = braced(text, pos)
                    while text[pos:pos + 1].isspace():
                        pos += 1
                    if text[pos:pos + 1] != "_":
                        raise CurriculumError("an underbrace without its label")
                    label, pos = braced(text, pos + 1)
                    parts.append(f"<munder><munder><mrow>{row(body)}</mrow><mo>⏟</mo></munder>"
                                 f"<mrow>{row(label)}</mrow></munder>")
                else:
                    raise CurriculumError(f"unmodelled scansion command \\{word}")
            elif char == "{":
                value, pos = braced(text, pos)
                parts.append(f"<mrow>{row(value)}</mrow>")
            elif char in ".,|":
                parts.append(f"<mo>{html.escape(char)}</mo>")
                pos += 1
            else:
                raise CurriculumError(f"unmodelled scansion token {char!r}")
        return "".join(parts)

    def braced(text: str, pos: int) -> tuple[str, int]:
        if text[pos:pos + 1] != "{":
            raise CurriculumError("a scansion argument must be braced")
        depth = 0
        for index in range(pos, len(text)):
            if text[index] == "\\":
                continue
            depth += (text[index] == "{") - (text[index] == "}")
            if depth == 0:
                return text[pos + 1:index], index + 1
        raise CurriculumError("unclosed scansion group")

    def text_node(value: str) -> str:
        parts = []
        for index, piece in enumerate(re.split(r"\$", value)):
            if index % 2:
                parts.append(f"<mrow>{row(piece)}</mrow>")
                continue
            if "\\" in piece:
                raise CurriculumError("unmodelled scansion text")
            words = " ".join(piece.replace("---", "—").replace("--", "–").split())
            if words:
                # Text mode keeps the spaces around an inner formula.
                lead = "\u00a0" if index and piece[:1].isspace() else ""
                trail = "\u00a0" if index + 1 < value.count("$") + 1 and piece[-1:].isspace() else ""
                parts.append(f"<mtext>{lead}{html.escape(words)}{trail}</mtext>")
        if value.count("$") % 2:
            raise CurriculumError("unclosed math inside scansion text")
        return "".join(parts)

    return f'<math display="block"><mrow>{row(source)}</mrow></math>'


# --- columns and titles ----------------------------------------------------

def column_spec(spec: str) -> str:
    while (repeat := re.search(r"\*\{([0-9]+)\}\{([^{}]*)\}", spec)) is not None:
        spec = spec[:repeat.start()] + repeat.group(2) * int(repeat.group(1)) + spec[repeat.end():]
    out, pos = [], 0
    while pos < len(spec):
        match = COLUMN_RE.match(spec, pos)
        if match is None:
            raise CurriculumError(f"unmodelled column specification {spec!r}")
        token = match.group(0)
        if token[0] in "PCpmb":
            out.append("p{" + match.group(1) + "}")
        elif token in {"X", "Y"}:
            out.append(r"p{0.3\linewidth}")
        elif token in {"l", "c", "r"}:
            out.append(token)
        pos = match.end()
    return "".join(out)


def plain(value: str) -> str:
    value = re.sub(r"\\(?:textit|textbf|emph|textsc|Latin|Term)\{([^{}]*)\}", r"\1", value)
    value = value.replace("``", "“").replace("''", "”").replace("---", "—").replace("--", "–")
    if re.search(r"[\\{}]", value):
        raise CurriculumError(f"unmodelled title markup {value!r}")
    return " ".join(value.split())


# --- Markdown projection -----------------------------------------------------

HEADING_RE = re.compile(r"^(#{1,6}) (.*?)(?: \{[^{}]*\})?$")


def heading_summary(line: str) -> str:
    match = HEADING_RE.match(line)
    text = match.group(2) if match else line
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\\(.)", r"\1", re.sub(r"[*_`]", "", text))
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return " ".join(text.replace("--", "–").replace(">", "›").split())


def project(markdown: str, responses: list[dict], maths: list[str]) -> str:
    """Turn the selection's tokens into reader HTML and answer-key comments."""
    lines = markdown.split("\n")
    # Response spaces: a token alone in its paragraph is a block; adjacent
    # block tokens of one paragraph run merge into one space of summed lines.
    used: set[int] = set()
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        alone = RESPONSE_RE.fullmatch(stripped)
        if alone and responses[int(alone.group(1)) - 1]["kind"] == "line" and not stripped.startswith("|"):
            number = int(alone.group(1))
            used.add(number)
            lines_here = responses[number - 1]["lines"]
            indent = line[:len(line) - len(line.lstrip())]
            previous = next((index for index in range(len(out) - 1, -1, -1) if out[index].strip()), None)
            if (previous is not None and all(not item.strip() for item in out[previous + 1:])
                    and out[previous].startswith(indent + '<span class="web-response"')
                    and out[previous][len(indent):len(indent) + 1] == "<"):
                total = int(re.search(r'data-lines="([0-9]+)"', out[previous]).group(1)) + lines_here
                out[previous] = indent + block_response(total)
                del out[previous + 1:]
                continue
            out.append(indent + block_response(lines_here))
            continue

        def inline(match: re.Match[str]) -> str:
            number = int(match.group(1))
            used.add(number)
            record = responses[number - 1]
            size = record["size"] if record["kind"] == "blank" else "fill"
            return (f'<span class="web-blank" data-size="{size}" role="img" '
                    'aria-label="blank"></span>')
        out.append(RESPONSE_RE.sub(inline, line))
    if used != set(range(1, len(responses) + 1)):
        raise CurriculumError("response space(s) lost in conversion: "
                              + ", ".join(map(str, sorted(set(range(1, len(responses) + 1)) - used))))
    text = "\n".join(out)

    found_maths = [int(match.group(1)) for match in MATH_RE.finditer(text)]
    if found_maths != list(range(1, len(maths) + 1)):
        raise CurriculumError("scansion display(s) lost in conversion")
    text = MATH_RE.sub(lambda match: maths[int(match.group(1)) - 1], text)

    text = fill_write_in_rows(text)
    text = wrap_keys(text)
    if TOKEN_RE.search(text):
        raise CurriculumError("a curriculum token stood inside other text: "
                              + TOKEN_RE.search(text).group(0))
    return text


CELL_BLANK = '<span class="web-blank" data-size="fill" role="img" aria-label="blank"></span>'
EMPTY_PIPE_ROW_RE = re.compile(r"^((?:[ \t]*>[ \t]?)*)\|((?:[ \t]*\|)+)[ \t]*$")
PIPE_DELIMITER_RE = re.compile(r"^(?:[ \t]*>[ \t]?)*\|(?:[ :]*-+[ :]*\|)+[ \t]*$")
EMPTY_HTML_ROW_RE = re.compile(r"<tr>((?:\s*<td[^>]*></td>)+)\s*</tr>")


def fill_write_in_rows(text: str) -> str:
    """A table row TeX sets with every cell empty is a row of a blank form.

    It is the reader's to write in, so each of its cells gets a visible blank.
    The empty header row of a headerless pipe table stays as pandoc wrote it.
    """
    lines = text.split("\n")
    for index, line in enumerate(lines):
        match = EMPTY_PIPE_ROW_RE.match(line)
        following = lines[index + 1] if index + 1 < len(lines) else ""
        if match and not PIPE_DELIMITER_RE.match(following):
            cells = match.group(2).count("|")
            lines[index] = match.group(1) + "|" + (" " + CELL_BLANK + " |") * cells
    text = "\n".join(lines)
    return EMPTY_HTML_ROW_RE.sub(
        lambda row: re.sub(r"(<td[^>]*>)(</td>)", r"\1" + CELL_BLANK + r"\2", row.group(0)), text)


def block_response(lines: int) -> str:
    return (f'<span class="web-response" data-lines="{lines}" role="img" '
            'aria-label="Space for a written answer"></span>')


def heading_level(line: str) -> int | None:
    match = HEADING_RE.match(line)
    return len(match.group(1)) if match else None


def key_units(lines: list[str]) -> list[str]:
    """Wrap one answer region: a chapter with its own text is one key; a
    chapter that only groups sections leaves each section its own key."""
    levels = [level for level in map(heading_level, lines) if level is not None]
    if not levels:
        if any(line.strip() for line in lines):
            raise CurriculumError("answer-key material outside any heading")
        return lines
    top = min(levels)
    starts = [index for index, line in enumerate(lines) if heading_level(line) == top]
    out = list(lines[:starts[0]])
    if any(line.strip() for line in out):
        raise CurriculumError("answer-key material before its first heading")
    for number, start in enumerate(starts):
        block = lines[start:starts[number + 1] if number + 1 < len(starts) else len(lines)]
        direct = []
        for line in block[1:]:
            if heading_level(line) is not None:
                break
            direct.append(line)
        if not any(line.strip() for line in block[1:]):
            out.extend(block)
        elif any(line.strip() for line in direct) or len(direct) == len(block) - 1:
            while block and not block[-1].strip():
                block = block[:-1]
            out.extend([f"<!-- triptych:answer-key {heading_summary(block[0])} -->", ""])
            out.extend(block)
            out.extend(["", "<!-- /triptych:answer-key -->", ""])
        else:
            out.extend(block[:1 + len(direct)])
            out.extend(key_units(block[1 + len(direct):]))
    return out


def wrap_keys(text: str) -> str:
    out: list[str] = []
    region: list[str] | None = None
    for line in text.split("\n"):
        if line in {KEY_ON, KEY_OFF}:
            if (line == KEY_ON) == (region is not None):
                raise CurriculumError("unbalanced answer-key marks")
            if region is None:
                region = []
            else:
                out.extend(key_units(region))
                region = None
            continue
        if KEY_ON in line or KEY_OFF in line:
            raise CurriculumError("an answer-key mark is not a block of its own")
        (out if region is None else region).append(line)
    if region is not None:
        raise CurriculumError("unclosed answer-key region")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out))


# --- interface -------------------------------------------------------------

def selection(root: Path, provider: str, leaf: str, library) -> dict:
    """The `selected` contract for ``library.convert(provider, leaf, ...)``."""
    course = _Course(Path(root), provider, leaf, library)
    if not leaf.startswith(COURSE + "/") or provider != "gpt":
        raise CurriculumError(f"{provider}/{leaf} is not an Ecclesiastical Latin curriculum leaf")
    result = course.run()
    body = result["body"]
    responses, maths = list(course.responses), list(course.maths)
    raw = "\n\n".join(text for _, text in sorted(course.files.items()))
    return {
        "edition": "main",
        "entrypoint": str(course.entry),
        "source": result["head"] + "\\begin{document}\n" + body + "\n\\end{document}\n",
        "sources": dict(course.files),
        "body": body,
        # Paragraph audits judge against the files on disk, never the expansion.
        "canonical_body": raw,
        # Response spaces are cells TeX leaves empty for the reader to fill.
        "audit_body": RESPONSE_RE.sub("", body),
        "preserve_titlepage": True,
        "markdown_projection": lambda markdown: project(markdown, responses, maths),
    }
