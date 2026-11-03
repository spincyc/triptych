"""Canonical server-training browser-print products for the cold producer.

Authored TeX and inventories remain authoritative. Verified SVGs are injected;
explicit diagram authoring lives in `_web_print_server_diagrams`. Mechanical
coverage does not confer editorial, publication or native-print approval.
"""
from __future__ import annotations

from collections import Counter
import functools
import hashlib
import html
from html.parser import HTMLParser
import importlib.machinery
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from typing import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
from document_schema_checks import liturgy
import _document_schema as document_schema
import _web_print_semantics as semantics

loader = importlib.machinery.SourceFileLoader("_web_print_server_web", str(ROOT / "tools/web-edition"))
spec = importlib.util.spec_from_loader(loader.name, loader)
web = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = web
loader.exec_module(web)

BASE = "liturgy/roman-rite/1962/reference/altar-server-guides"
LEAVES = ("01-low-mass", "01-low-mass-trainer-manual", "01-low-mass-flash-cards",
          "02-missa-cantata", "02-missa-cantata-cue-cards", "03-solemn-mass", "03-solemn-mass-cue-cards")


class Refusal(ValueError):
    pass


def sha(data: bytes | str) -> str:
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def _source_bytes(root: Path, path: Path, inputs: dict) -> bytes:
    path = Path(path)
    if path.suffix.lower() in {".pdf", ".dvi"}:
        raise Refusal("browser print source selection cannot consume a PDF or DVI")
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise Refusal("source escapes the repository or is a symlink")
    path = path.resolve()
    data = path.read_bytes()
    inputs[path.relative_to(root).as_posix()] = sha(data)
    return data


def _provider(provider: str) -> None:
    if provider not in {"gpt", "claude"}:
        raise Refusal("unknown publication provider")


def calls(text, command, count):
    return list(liturgy._calls(web.mask_tex_comments(text), command, count))


def replace(text, name, count, render):
    found = calls(text, name, count)
    for args, start, end in reversed(found):
        text = text[:start] + render(args) + text[end:]
    return text



def without_environment_definitions(text):
    pattern = re.compile(r"\\(?:new|renew)environment\s*\{")
    while match := pattern.search(text):
        _, end = web.brace_group(text, match.end() - 1)
        end = web.skip_gap(text, end)
        if text[end:end + 1] == "[":
            end = text.index("]", end) + 1
        _, end = web.brace_group(text, end)
        _, end = web.brace_group(text, end)
        text = text[:match.start()] + text[end:]
    return text


def tipa_unicode(text):
    """The current bank's bounded TIPA repertoire, per TIPA/tipauni encoding."""
    text = re.sub(r"\\textltailn\s*", "ɲ", text).replace('""', "ˌ").replace("{", "").replace("}", "")
    if re.search(r"[^a-zNSZɲˌ\". /]", text):
        raise Refusal("unimplemented TIPA source symbol; do not silently discard IPA")
    return text.translate(str.maketrans({'"': 'ˈ', 'N': 'ŋ', 'S': 'ʃ', 'Z': 'ʒ', 'g': 'ɡ'}))


@functools.lru_cache(maxsize=8)
def _checked_pandoc(executable: str) -> str:
    try:
        completed = subprocess.run([executable, "--version"], text=True, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        raise Refusal("cannot verify the pinned Pandoc 3.11") from error
    lines = (completed.stdout or completed.stderr).splitlines()
    version = lines[0] if lines else ""
    if version != "pandoc 3.11":
        raise Refusal("browser print generation requires the pinned Pandoc 3.11")
    return version


def pandoc_command() -> str:
    executable = shutil.which("pandoc")
    if executable is None:
        raise Refusal("the pinned Pandoc 3.11 is unavailable")
    _checked_pandoc(executable)
    return executable


@functools.lru_cache(maxsize=16384)
def pandoc_fragment(text):
    text = web.terminate_swallowers(web.set_text_dashes(web.PERIOD_CENTERED_RE.sub("·", text)))
    completed = subprocess.run([pandoc_command(), "-f", "latex", "-t", "html5", "--wrap=none"],
                               input=text, text=True, capture_output=True)
    if completed.returncode or completed.stderr.strip():
        raise Refusal(completed.stderr.strip() + "\nFRAGMENT: " + text[:300])
    return completed.stdout.strip()


def _column_alignment(spec: str) -> str:
    """Retain a table's column count/alignment while browser widths reflow."""
    result = []
    index = 0
    while index < len(spec):
        char = spec[index]
        if char.isspace() or char == "|":
            index += 1
        elif char in "@!><":
            index = web.skip_gap(spec, index + 1)
            _, index = web.brace_group(spec, index)
        elif char in "lrcX":
            result.append("l" if char == "X" else char)
            index += 1
        elif char in "pmb":
            _, index = web.brace_group(spec, web.skip_gap(spec, index + 1))
            result.append("l")
        elif char == "*":
            count, index = web.brace_group(spec, web.skip_gap(spec, index + 1))
            inner, index = web.brace_group(spec, web.skip_gap(spec, index))
            if not count.isdecimal() or not 1 <= int(count) <= 20:
                raise Refusal("unreviewed repeated table-column specification")
            result.extend(_column_alignment(inner) * int(count))
        else:
            raise Refusal("unreviewed server table-column specification")
    if not result or len(result) > 20:
        raise Refusal("invalid server table-column count")
    return "".join(result)


def _multicolumn_projection(source: str) -> str:
    """Prevent Pandoc losing a spanning header with decorated p columns.

    Only tables containing a canonical multicolumn are affected. Their cell
    content/order/spans remain canonical; browser CSS owns the reflow widths.
    The independent fragment ledger still reads the unprojected source.
    """
    edits = []
    pattern = re.compile(r"\\begin\s*\{(longtable|tabular\*?|tabularx|array)\}")
    for match in pattern.finditer(source):
        cursor = web.skip_gap(source, match.end())
        if source[cursor:cursor+1] == "[":
            cursor = source.index("]", cursor) + 1
        if match[1] in {"tabularx", "tabular*"}:
            _, cursor = web.brace_group(source, web.skip_gap(source, cursor))
        opening = web.skip_gap(source, cursor)
        spec, end = web.brace_group(source, opening)
        stop = web.table_rows_extent(source, end, match[1])
        rows = source[end:stop]
        if not calls(rows, "multicolumn", 3):
            continue
        if pattern.search(rows):
            raise Refusal("nested spanning server tables need an explicit layout adapter")
        edits.append((opening, end, "{" + _column_alignment(spec) + "}"))
        for args, start, finish in calls(rows, "multicolumn", 3):
            alignment = _column_alignment(args[1])
            if len(alignment) != 1:
                raise Refusal("spanning table cell has more than one alignment")
            replacement = r"\multicolumn{" + args[0] + "}{" + alignment + "}{" + args[2] + "}"
            edits.append((end + start, end + finish, replacement))
    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]
    return source


def _bracket_argument(text: str, start: int) -> tuple[str, int]:
    if text[start:start+1] != "[":
        raise Refusal("expected a source list option")
    depth = 0
    cursor = start + 1
    while cursor < len(text):
        char = text[cursor]
        if char == "\\":
            cursor += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        elif char == "]" and depth == 0:
            return text[start+1:cursor], cursor + 1
        cursor += 1
    raise Refusal("unclosed source list option")


def _option_label(options: str) -> str | None:
    match = re.search(r"(?:^|,)\s*label\s*=", options)
    if match is None:
        return None
    start = cursor = match.end()
    depth = 0
    while cursor < len(options):
        char = options[cursor]
        if char == "\\":
            cursor += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        elif char == "," and depth == 0:
            break
        cursor += 1
    return options[start:cursor].strip()


def _labeled_list_projection(source: str) -> str:
    """Preserve source enumitem labels that Pandoc otherwise discards.

    Custom Scene/Stage labels and explicit range labels become description
    terms. Labels are derived before conversion from source options/items,
    never from the rendered DOM. Ordinary unlabeled lists remain ordered lists.
    """
    pattern = re.compile(r"\\begin\s*\{enumerate\}")
    edits = []
    for match in pattern.finditer(source):
        cursor = web.skip_gap(source, match.end())
        options = ""
        if source[cursor:cursor+1] == "[":
            options, cursor = _bracket_argument(source, cursor)
        stop = source.find(r"\end{enumerate}", cursor)
        if stop < 0:
            raise Refusal("unclosed source ordered list")
        body = source[cursor:stop]
        template = _option_label(options)
        items = []
        for item in re.finditer(r"\\item(?![A-Za-z@])", body):
            end = web.skip_gap(body, item.end())
            label = None
            if body[end:end+1] == "[":
                label, end = _bracket_argument(body, end)
            else:
                end = item.end()
            items.append((item.start(), end, label))
        if template is None and not any(label is not None for _, _, label in items):
            continue
        if re.search(r"\\(?:begin|end)\s*\{(?:enumerate|description|itemize)\}", body):
            raise Refusal("nested custom-labeled server list needs an explicit adapter")
        if not items:
            raise Refusal("source labeled list has no items")
        if re.search(r"(?:^|,)\s*(?:resume|resume\*)\b", options):
            raise Refusal("resumed source labels need an explicit counter state")
        initial = re.search(r"(?:^|,)\s*start\s*=\s*([0-9]+)(?:,|$)", options)
        number = int(initial[1]) if initial else 1
        for start, end, explicit in reversed(items):
            index = next(i for i, item in enumerate(items) if item[0] == start)
            if explicit is not None:
                label = explicit
            elif template is not None and template.count(r"\arabic*") == 1:
                label = template.replace(r"\arabic*", str(number + index))
            else:
                raise Refusal("source list label cannot be derived from its declared counter")
            body = body[:start] + r"\item[" + label + "]" + body[end:]
        replacement = r"\begin{description}" + body + r"\end{description}"
        edits.append((match.start(), stop + len(r"\end{enumerate}"), replacement))
    for start, end, replacement in sorted(edits, reverse=True):
        source = source[:start] + replacement + source[end:]
    return source


def _fragment_container_bindings(rendered: str, expected: list[dict]) -> str:
    """Bind existing Pandoc containers to independently selected source IDs.

    This copy is only for the fragment auditor. It creates no expected
    content and cannot turn a missing/extra minipage into a covered one.
    The final product retains the original source-profile HTML hierarchy.
    """
    class Binder(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.output = []
            self.index = 0

        def handle_starttag(self, tag, attrs):
            raw = self.get_starttag_text()
            values = dict(attrs)
            if "data-semantic-minipage" in values:
                raise Refusal("fragment renderer supplied its own source-container proof")
            if "minipage" in values.get("class", "").split():
                if self.index >= len(expected):
                    raise Refusal("fragment renderer added an unselected minipage")
                key = expected[self.index]["id"]
                self.index += 1
                raw = raw[:-1] + ' data-semantic-minipage="' + html.escape(key, quote=True) + '">'
            self.output.append(raw)

        def handle_startendtag(self, tag, attrs):
            self.output.append(self.get_starttag_text())

        def handle_endtag(self, tag):
            self.output.append("</" + tag + ">")

        def handle_data(self, text):
            self.output.append(text)

        def handle_entityref(self, name):
            self.output.append("&" + name + ";")

        def handle_charref(self, name):
            self.output.append("&#" + name + ";")

        def handle_comment(self, text):
            self.output.append("<!--" + text + "-->")

    parser = Binder()
    parser.feed(rendered)
    parser.close()
    if parser.index != len(expected):
        raise Refusal("fragment renderer omitted a canonical minipage")
    return "".join(parser.output)


def _check_fragment_container_bounds(ledger: dict, rendered: str, report: dict) -> None:
    """Require every matched canonical block to stay in its source container."""
    expected = ledger["containers"]
    if not expected:
        return
    parser = semantics.HtmlLedger()
    parser.feed(rendered)
    parser.finish()
    if [item["id"] for item in parser.containers] != [item["id"] for item in expected]:
        raise Refusal("fragment minipage order disagrees with its source")
    matched = {item["id"]: item["output_block"] for item in report["matched_units"]}
    for source, actual in zip(expected, parser.containers):
        if "unit_end" not in source or "unit_end" not in actual:
            raise Refusal("fragment minipage is unclosed")
        for index, unit in enumerate(ledger["units"]):
            should_contain = source["unit_start"] <= index < source["unit_end"]
            output_index = matched[unit["id"]]
            does_contain = actual["unit_start"] <= output_index < actual["unit_end"]
            if should_contain != does_contain:
                raise Refusal("fragment text moved across a canonical minipage boundary")
    for i, source in enumerate(expected):
        for j in range(i + 1, len(expected)):
            child = expected[j]
            source_contains = source["unit_start"] <= child["unit_start"] and child["unit_end"] <= source["unit_end"]
            actual, nested = parser.containers[i], parser.containers[j]
            actual_contains = actual["unit_start"] <= nested["unit_start"] and nested["unit_end"] <= actual["unit_end"]
            if source_contains != actual_contains:
                raise Refusal("fragment minipage nesting changed")


class Adapter:
    def __init__(self, root: Path, provider: str, output_id: str, *,
                 asset_resolver: Callable | None = None, fragment_renderer: Callable | None = None):
        self.root = root.resolve()
        _provider(provider)
        self.provider = provider
        self.output_id = output_id.removeprefix(provider + "/")
        if self.output_id not in [BASE + "/" + name for name in LEAVES]:
            raise Refusal("not an exact declared server-training output")
        self.name = self.output_id.rsplit("/", 1)[1]
        self.form = "low" if self.name.startswith("01-") else "cantata" if self.name.startswith("02-") else "solemn"
        self.trainer = "trainer-manual" in self.name
        self.cards = self.name.endswith(("flash-cards", "cue-cards"))
        self.owner = self.root / "src" / provider / BASE
        self.leaf = self.owner / self.name
        self.asset_resolver = asset_resolver
        self.fragment_renderer = fragment_renderer or pandoc_fragment
        self.inputs = {}
        self._fragment_cache = {}
        self.fragment_audits = []
        self.publication = document_schema.load_manifest(self.root, self.leaf / "publication.toml")
        if (self.publication["id"] != provider + "/" + self.output_id or
                self.publication["source_format"] != "latex" or self.publication["entrypoint"] != "main.tex" or
                len(self.publication["outputs"]) != 1 or self.publication["outputs"][0]["role"] != "canonical" or
                self.publication["outputs"][0]["entrypoint"] != "main.tex"):
            raise Refusal("typed publication does not declare this exact canonical server entrypoint")
        source_check = document_schema.validate(self.root, self.publication, phase="source", run_gates=False)
        if not source_check["ok"]:
            raise Refusal("invalid server source declaration: " + "; ".join(source_check["errors"]))
        self.units, self.expected, self.assets, self.gaps = [], [], [], []
        self.block_counter = 0
        self.tokens = {}
        self.diagram_counts = {}
        self.definitions = {}
        self.bank_raw = self.read(self.owner / "shared/response-reference.tex")
        self.bank = {}
        for command in ("serveranswer", "RegisterServerData"):
            for args, _, _ in calls(self.bank_raw, command, 6):
                identity = args[0].split(" --- ", 1)[0]
                if re.fullmatch("A[0-9]+", identity):
                    self.bank[identity] = dict(zip(("title", "latin", "learner", "sound", "ipa", "meaning"), args))
        inventory = self.read(self.owner / "research/response-inventory.md")
        expected = [row[0] for row in liturgy._rows(inventory, r"A\d+", 6)]
        if set(self.bank) != set(expected) or len(self.bank) != len(expected):
            raise Refusal("response bank differs from the independent canonical response inventory")
        names = ["server-guide-format.tex", "response-reference.tex"]
        if self.form == "low" and not self.cards:
            names += ["low-mass-book-format.tex", "low-mass-diagrams.tex"]
        elif self.form != "low" and not self.cards:
            stem = "missa-cantata" if self.form == "cantata" else "solemn"
            names += [stem + "-role-sheets.tex", stem + "-ceremony.tex", "terminal-apparatus.tex"]
        for filename in names:
            path = self.owner / "shared" / filename
            defs, _ = web.command_definitions(self.read(path))
            self.definitions.update(defs)
        defs, _ = web.command_definitions(self.read(self.leaf / "main.tex"))
        self.definitions.update(defs)
        for identity in ("A8", "A14"):
            match = re.search(r"servertitle@" + identity + r"\\endcsname\s*\{", self.bank_raw)
            if match is not None:
                self.bank[identity]["title"] = web.brace_group(self.bank_raw, match.end() - 1)[0]
        self.lookup = {}
        for command, field, count in (("DefineResponseVoice", "voice", 4), ("DefineResponseJob", "job", 4),
                                      ("DefineResponseCue", "cue", 2), ("DefineResponseLesson", "lesson", 2)):
            for args, _, _ in calls(self.bank_raw, command, count):
                if args[0] in self.bank:
                    self.lookup[field, args[0]] = args[1] if count == 2 else args[1 + (0 if self.form == "low" else 1 if self.form == "cantata" else 2)]
        kyrie = self.bank["A14"]["latin"].split(". ")
        if len(kyrie) != 2:
            raise Refusal("A14 no longer has the declared two-invocation split")
        self.definitions["LowMassKyrieResponse"] = (0, None, kyrie[0] + ".")
        self.definitions["LowMassChristeResponse"] = (0, None, kyrie[1])
        self.manifest = self.read(self.owner / "research/flash-card-manifest.md")
        self.metadata = self.read(self.leaf / "generation-metadata.tex")
        self.revised = re.search(r"\\AIDocumentRevisionTimestamp\{([^}]+)\}", self.metadata)[1]
        preamble = self.read(self.root / "src/common/preamble.tex")
        common_defs, _ = web.command_definitions(preamble)
        self.rights = common_defs["TriptychRightsNotice"][2]
        self.read(self.leaf / "publication.toml")
        self.read(self.leaf / "research/guide-map.md")
        diagram_file = "low-mass-diagrams.tex" if self.form == "low" else "sung-mass-diagrams.tex"
        diagram_definitions, _ = web.command_definitions(self.read(self.owner / "shared" / diagram_file))
        self.diagram_names = {name for name in diagram_definitions
                              if (name.startswith("LMScene") or name.endswith("Diagram"))
                              and name not in {"LMSceneXUnit", "LMSceneYUnit"}}
        from _web_print_server_schedule import source_schedule
        self._assembly_schedule = source_schedule(self)

    def read(self, path):
        return _source_bytes(self.root, Path(path), self.inputs).decode()

    def select(self, text):
        states = {r"\ifLowMassGuide": self.form == "low", r"\ifMissaCantataGuide": self.form == "cantata",
                  r"\ifSolemnMassGuide": self.form == "solemn", r"\ifCardsOnlyGuide": self.cards or self.form == "low",
                  r"\ifResponseDataOnlyGuide": self.form == "low", r"\ifTrainerManualGuide": self.trainer,
                  r"\ifChildBookletGuide": self.form == "low" and not self.trainer and not self.cards,
                  r"\ifTriptychRightsNoticeRendered": False}
        return liturgy._conditional(web.strip_tex_comments(text), states)

    def expand(self, text):
        for _ in range(15):
            before = text
            text = replace(text, "GuideVoiceChoice", 3, lambda a: "{" + a[0 if self.form == "low" else 1 if self.form == "cantata" else 2] + "}")
            for field in ("Latin", "Learner", "Sound", "IPA", "Meaning", "Title", "Voice", "Job", "Cue"):
                key = field.lower()
                def value(args, key=key):
                    if args[0] not in self.bank:
                        raise Refusal("unknown canonical response " + args[0])
                    return "{" + self.bank[args[0]].get(key, self.lookup.get((key, args[0]), "")) + "}"
                text = replace(text, "Server" + field + "Data", 1, value)
            text = replace(text, "ResponseLessonData", 1, lambda a: self.lookup["lesson", a[0]])
            text = replace(text, "ServerStress", 1, lambda a: r"\textbf{" + a[0].upper() + "}")
            text = replace(text, "LowMassQualifiedCue", 2, lambda a: a[1] + r"\par\textbf{" + a[0].upper() + "}")
            for name, macro in self.definitions.items():
                if macro[0] == 0 and (name.startswith(("Aight", "QuietFootVoice", "LowMassKyrie", "LowMassChriste", "Guide"))
                                      or name.endswith("Job") or name in {"MCRoleAlways"}):
                    text = web.expand_macros(text, {name: (0, None, "{" + macro[2] + "}")})
            if text == before:
                return self.select(text)
        raise Refusal("unresolved recursive response macro")

    def fragment_source(self, text):
        """Pure selected canonical normal form; no converter or HTML is consulted."""
        text = self.expand(text)
        aliases = {"CanonLatin": (1, None, r"\textit{#1}"), "LearnLatin": (1, None, r"\textbf{#1}"),
                   "SoundLine": (1, None, "{#1}"), "ServerLearnerLine": (1, None, "{#1}"), "ServerAnswerRef": (1, None, r"\textbf{#1}"),
                   "SpokenCue": (1, None, "℣. #1"), "SpokenResponse": (1, None, "℟. #1"),
                   "MissalDisplay": (1, None, "{#1}"), "MissalSeparator": (0, None, "{·}"),
                   "LocalChoice": (0, None, "local choice"), "MissalRule": (0, None, "missal"), "ModelRule": (0, None, "model"),
                   "MCGuideCheck": (0, None, "□"), "fbox": (1, None, "{#1}"),
                   "mbox": (1, None, "{#1}"), "hbox": (1, None, "{#1}")}
        text = web.expand_macros(text, aliases)
        text = replace(text, "BroadIPA", 1, lambda a: tipa_unicode("/" + a[0] + "/"))
        text = replace(text, "textipa", 1, lambda a: tipa_unicode(a[0]))
        for name, count in (("vspace", 1), ("hspace", 1), ("fontsize", 2), ("Needspace", 1), ("needspace", 1)):
            text = replace(text, name, count, lambda a: "")
        text = replace(text, "rule", 2, lambda a: "________")
        text = replace(text, "MCGuideLine", 1, lambda a: "________")
        text = replace(text, "MakeUppercase", 1, lambda a: a[0].upper())
        text = replace(text, "colorbox", 2, lambda a: "{" + a[1] + "}")
        def table_parbox(args):
            width = re.sub(r"\s+", "", args[0])
            if width not in {r"\dimexpr\linewidth-2\fboxsep-6pt\relax",
                             r"\dimexpr\linewidth-2\fboxsep\relax"}:
                raise Refusal("unreviewed server paragraph-box width")
            # The canonical role-table cell already owns this header's
            # position and boundaries. Retain the complete paragraph content
            # while allowing its width to reflow with the browser table.
            return "{" + args[1] + "}"
        text = replace(text, "parbox", 2, table_parbox)
        text = re.sub(r"\\textls(?:\[[^]]*\])?", "", text)
        text = text.replace(r"\(\cdot\)", "·")
        text = _labeled_list_projection(text)
        text = web.LIST_OPTION_RE.sub(r"\1", text)
        def reference(args):
            label = args[0]
            role = label.split(":")[1].upper() if ":" in label else "common track"
            return r"\href{\#" + label + "}{" + role + " section}"
        text = replace(text, "pageref", 1, reference)
        text = re.sub(r"\\(?:scriptsize|tiny|footnotesize|small|normalsize|large|Large|LARGE|huge|Huge|selectfont|sffamily|rmfamily|mdseries|scshape|RaggedRight|centering|noindent|vfill|hfill|smallskip|medskip|bigskip|nobreak|quad|qquad|enspace|thinspace|negthinspace)(?![A-Za-z@])", " ", text)
        text = re.sub(r"\\(?:textwidth|linewidth|textheight)", "", text)
        unknown = sorted(set(re.findall(r"\\([A-Za-z@]+)", text)) - web.KNOWN_COMMANDS)
        if unknown:
            raise Refusal("unimplemented source macros: " + ", ".join(unknown))
        return text

    def fragment(self, text):
        original = text
        if original in self._fragment_cache:
            return self._fragment_cache[original]
        text = self.fragment_source(text)
        rendered = self.fragment_renderer(_multicolumn_projection(text))
        if not isinstance(rendered, str):
            raise Refusal("fragment renderer did not return HTML text")
        # The generic bounded source ledger independently checks the ordinary
        # LaTeX after the owning server macros select their canonical fields.
        # Fragment checking does not inject publication titles or rights.
        origin = (self.leaf / "main.tex").relative_to(self.root).as_posix()
        projection = dict(kind="server-expanded-fragment", source_inputs=dict(self.inputs),
                          macro_definitions_sha256=sha(json.dumps(self.definitions, sort_keys=True)),
                          expanded_sha256=sha(text))
        # No owner macros remain in this normal form. Their source graph
        # and exact selected definitions are pinned by the projection above;
        # the fragment checker must refuse any unknown surviving execution.
        selected = dict(body=text, head="", sources={},
                        chunks=[dict(path=origin, occurrence=len(self.fragment_audits)+1,
                                     selected_line=1, text=text, projection=projection)],
                        selection=dict(entrypoint=origin, role="canonical-fragment",
                                       selection_digest=sha(json.dumps(projection, sort_keys=True))))
        try:
            ledger = semantics.expected_fragment_units(selected, web)
            verification = _fragment_container_bindings(rendered, ledger["containers"])
            report = semantics.check_units(ledger, verification, web)
            if report["status"] == "pass":
                _check_fragment_container_bounds(ledger, verification, report)
        except (ValueError, KeyError) as error:
            raise Refusal("server fragment source cannot be accounted for: " + str(error)) from error
        if report["status"] != "pass":
            failures = [{key: item[key] for key in ("id", "kind", "expected", "text", "reason") if key in item}
                        for item in report.get("failures", [])]
            raise Refusal("server fragment lost canonical text or structure: " +
                          json.dumps(failures, ensure_ascii=False)[:4000])
        self.fragment_audits.append(dict(ledger_digest=ledger["ledger_digest"],
                                        source_units=len(ledger["units"]), expanded_sha256=sha(text)))
        self._fragment_cache[original] = rendered
        return rendered

    def unit(self, identity, kind, content, **metadata):
        if identity in {unit["id"] for unit in self.units}:
            raise Refusal("duplicate rendered unit " + identity)
        self.units.append(dict(id=identity, kind=kind, html=content, **metadata))
        return self.units[-1]

    def card_face(self, name, args):
        def sized(text, base=11):
            probe = text.strip()
            while probe.startswith("{"):
                inner, end = web.brace_group(probe, 0)
                if probe[end:].strip():
                    break
                probe = inner.strip()
            size = re.match(r"\\(tiny|scriptsize|footnotesize|small|normalsize)(?![A-Za-z])", probe)
            points = {"tiny": 6, "scriptsize": 8, "footnotesize": 9, "small": 10, "normalsize": 11}.get(size[1], base) if size else base
            return 'source-size-' + str(points)
        if name.startswith("LowMass"):
            _, _, number, stage, body = args
            identity = "LM-F" + number
            back = name == "LowMassBackCard"
            header = f'<span>{number} · {"BOTH" if back else "PRIEST"}</span><span>LOW MASS</span><span>{html.escape(stage)}</span>'
            content = self.fragment(("℟. " if back else "℣. ") + body)
            content = '<div class="answer">' + content + '</div>' if back else content
        else:
            identity, back = args[0], name not in {"integratedresponsefront", "flashfront"}
            marker = "MC" if self.form == "cantata" else "SOLEMN"
            printed_id = identity if name in {"flashfront", "actionflashback"} else identity + " · " + marker
            header = f'<span>{printed_id}</span><span>{"Answer" if back else "Cue"}</span>'
            if name == "integratedresponsefront":
                content = '<div class="' + sized(args[2]) + '">' + self.fragment("℣. " + args[2]) + '</div>'
            elif name == "flashfront":
                content = self.fragment(args[1])
            else:
                if name == "storedresponseback":
                    item = self.bank[args[1]]
                    args = [identity, item["latin"], item["learner"], item["sound"], item["meaning"],
                            "Lesson " + self.lookup["lesson", args[1]] + " · " + args[1] + "."]
                if name == "actionflashback":
                    content = self.fragment(r"\textit{" + args[1] + "}") + '<div class="action-body">' + self.fragment(args[2]) + '</div>'
                    content += '<div class="face-footer">' + self.fragment(args[3]) + '</div>'
                else:
                    dense = name == "denseintegratedresponseback"
                    content = '<div class="dense">' if dense else '<div>'
                    content += "".join('<div class="field ' + field + ' ' + sized(value, 8 if dense else default) + '">' +
                                       ('' if dense and field in {'response', 'meaning'} else '<span class="field-label">' + label + '</span>') + self.fragment(('℟. ' if field == 'response' else '') + value) + '</div>'
                                       for field, label, value, default in zip(("response", "learner", "sound", "meaning"),
                                           ("RESPONSE", "LATIN CHUNKS", "SAY IT LIKE", "MEANING"), args[1:5], (10, 8, 10, 8)))
                    content += '</div>'
                    content += '<div class="face-footer">' + self.fragment(args[5]) + '</div>'
        return identity, "back" if back else "front", '<header class="face-header">' + header + '</header>' + content

    def render_cards(self):
        low = self.form == "low"
        source = self.read(self.leaf / "main.tex") if low else self.select(self.bank_raw)
        if not low:
            source += self.select(self.read(self.owner / "shared" / ("missa-cantata-action-cards.tex" if self.form == "cantata" else "solemn-action-cards.tex")))
        environment = "tikzpicture" if low else "flashgrid"
        grids = re.findall(r"\\begin\{" + environment + r"\}(.*?)\\end\{" + environment + r"\}", source, re.S)
        commands = {"LowMassFrontCard": 5, "LowMassBackCard": 5} if low else {
            "integratedresponsefront": 3, "storedresponseback": 2, "integratedresponseback": 6,
            "denseintegratedresponseback": 6, "flashfront": 2, "actionflashback": 4}
        sheets, all_ids, sheet_metadata_ids = [], [], []
        for grid in grids:
            events = sorted((start, command, args) for command, count in commands.items() for args, start, _ in calls(grid, command, count))
            if not events:
                continue
            faces = [self.card_face(command, args) for _, command, args in events]
            sides = {side for _, side, _ in faces}
            if len(sides) != 1:
                raise Refusal("mixed front/back source sheet")
            side = sides.pop()
            expected_side = "front" if len(sheets) % 2 == 0 else "back"
            if side != expected_side:
                raise Refusal("source does not alternate complete front/back sheets")
            ids = [identity for identity, _, _ in faces]
            if side == "back":
                prior = sheets[-1]["face_ids"]
                mirrored = [item for index in range(0, len(prior), 2) for item in prior[index:index + 2][::-1]]
                if ids != mirrored:
                    raise Refusal("source back grid is not the exact row-mirrored front grid")
            capacity = 8 if low else 6
            if len(faces) > capacity:
                raise Refusal("card grid exceeds owning profile capacity")
            cells = []
            for index, (identity, _, content) in enumerate(faces):
                key = f"{identity}:{side}"
                self.unit(key, "card-face", content, sheet=len(sheets) + 1, slot=index + 1,
                          row=index // 2 + 1, column=index % 2 + 1, pair_id=identity)
                cells.append(f'<article class="face" data-unit-id="{key}" data-pair-id="{identity}">{content}</article>')
                all_ids.append(key)
            cells.extend('<div class="face blank" aria-hidden="true"></div>' for _ in range(capacity - len(cells)))
            sheet_html = f'<section class="sheet {"low" if low else "sung"}" data-side="{side}" data-sheet="{len(sheets)+1}"><div class="grid" style="--rows:{4 if low else 3}">' + ''.join(cells) + '</div>'
            if low:
                footers = calls(grid, "LowMassSheetFooter", 1)
                if len(footers) > 1:
                    raise Refusal("source sheet repeats its duplex instruction")
                for footer_args, _, _ in footers:
                    key = f"sheet-{len(sheets)+1:02d}-duplex-instruction"
                    text = self.fragment(footer_args[0])
                    self.unit(key, "duplex-instruction", text, sheet=len(sheets)+1, side=side)
                    sheet_metadata_ids.append(key)
                    sheet_html += '<footer class="sheet-duplex" data-unit-id="' + key + '">' + text + '</footer>'
            sheets.append(dict(id=f"sheet-{len(sheets)+1:02d}-{side}", kind="card-sheet", html=sheet_html + '</section>', face_ids=ids, side=side))
        if not sheets or len(sheets) % 2:
            raise Refusal("incomplete duplex source selection")
        if low:
            rows = liturgy._rows(self.manifest, r"LM-F\d{2} / \d{2}", 4)
            expected_pairs = [row[0].split(" / ")[0] for row in rows]
        else:
            expected_pairs = sorted(liturgy._manifest_card_ids(self.manifest, "R01"))
            expected_pairs += sorted(liturgy._manifest_card_ids(self.manifest, "MC-A" if self.form == "cantata" else "SO-A"))
        self.expected = [identity + ":" + side for identity in expected_pairs for side in ("front", "back")]
        if set(self.expected) != set(all_ids) or len(self.expected) != len(all_ids):
            raise Refusal("rendered card-face IDs differ from the independently declared physical-card manifest")
        self.expected.extend(sheet_metadata_ids)
        # These two canonical entrypoints append source matter forbidden by
        # the cards-only profile. Preserve it after the complete card run and
        # record the conflict, rather than claiming source parity after a cut.
        if self.form in {"low", "cantata"}:
            raw = self.definitions["CardCompanionTerminalApparatus"][2]
            node = re.search(r"at\s*\([^)]*\)\s*\{", raw)
            if node is None:
                raise Refusal("terminal apparatus no longer has its declared text node")
            body, _ = web.brace_group(raw, node.end() - 1)
            text = self.fragment(body)
            self.unit("card-terminal-apparatus", "apparatus", text)
            self.expected.append("card-terminal-apparatus")
            sheets.append(dict(id="card-terminal-apparatus", kind="apparatus", html='<section class="apparatus" data-unit-id="card-terminal-apparatus">' + text + '</section>'))
            self.gaps.append("Canonical source adds CardCompanionTerminalApparatus after the final back; profile prohibits terminal-reference sheets. Preserved as separately typed ordered apparatus pending maintainer normalization.")
        return sheets

    def diagram(self, name):
        if self.asset_resolver is None:
            from _web_print_assets import server_asset
            resolver = server_asset
        else:
            resolver = self.asset_resolver
        variant = "sung" if self.form != "low" else "trainer" if self.trainer else "child"
        record = dict(resolver(self.root, variant, name))
        key = variant + ":" + name
        if (record.get("id") != key or not isinstance(record.get("src"), str) or not record["src"] or
                not re.fullmatch(r"[a-f0-9]{64}", str(record.get("sha256", ""))) or
                not isinstance(record.get("bytes"), int) or isinstance(record["bytes"], bool) or record["bytes"] <= 0 or
                not isinstance(record.get("source_inputs"), dict) or not record["source_inputs"] or
                not isinstance(record.get("includes_caption"), bool)):
            raise Refusal("verified diagram resolver returned an incomplete or mismatched source-bound asset")
        if "body" in record and (not isinstance(record["body"], bytes) or
                                 len(record["body"]) != record["bytes"] or sha(record["body"]) != record["sha256"]):
            raise Refusal("diagram body does not match its verified asset record")
        for source, digest in record["source_inputs"].items():
            if isinstance(source, str) and source.split("/")[:2] in (["src", "gpt"], ["src", "claude"]) and source.split("/")[1] != self.provider:
                raise Refusal("diagram source belongs to another publication provider")
            if not isinstance(source, str) or not source.startswith("src/") or sha(_source_bytes(self.root, self.root / source, self.inputs)) != digest:
                raise Refusal("diagram projection is stale: " + str(source))
        asset = {**record, "source_macro": name, "mime": "image/svg+xml"}
        if not any(item["id"] == key for item in self.assets):
            self.assets.append(asset)
        elif next(item for item in self.assets if item["id"] == key) != asset:
            raise Refusal("diagram resolver changed one asset within the selected output")
        caption = re.sub(r"^(?:LMScene|MC|Solemn)", "", name).removesuffix("Diagram")
        caption = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", caption)
        return ('<figure class="diagram" data-diagram-id="' + html.escape(key, quote=True) +
                '"><img src="' + html.escape(record["src"], quote=True) + '" alt="' + html.escape(caption) + '"></figure>')

    def render_tex(self, source):
        source = self.select(source)
        def hook(args):
            if args[0] != "shipout/foreground":
                raise Refusal("unsupported source shipout hook")
            match = re.search(r"at\s*\([^)]*\)\s*\{", args[1])
            if match is None or r"\includegraphics" in args[1]:
                raise Refusal("shipout teaching text needs an exact asset adapter")
            return web.brace_group(args[1], match.end() - 1)[0]
        source = replace(source, "AddToHookNext", 2, hook)
        definitions, source = web.command_definitions(source)
        self.definitions.update(definitions)
        source = without_environment_definitions(source)
        # A source table row must remain a table row while Pandoc parses it.
        # Stashing a complete HTML <tr> here would put it inside a generated
        # <td>, forcing browser repair and corrupting the canonical row grid.
        source = replace(source, "TrainerIPARow", 1,
                         lambda a: r"\textbf{" + a[0] + "} & " +
                         tipa_unicode('/' + self.bank[a[0]]["ipa"] + '/') + r"\\" + "\n")
        for name, count in (("serveranswer", 6), ("RegisterServerData", 6), ("DefineResponseVoice", 4),
                            ("DefineResponseJob", 4), ("DefineResponseCue", 2), ("DefineResponseLesson", 2)):
            source = replace(source, name, count, lambda a: "")
        source = re.sub(r"\\(?:LowMass|MissaCantata|SolemnMass|CardsOnly|ResponseDataOnly|ChildBooklet|TrainerManual|LMSuppressTrainerMeaning)Guide(?:true|false)", "", source)
        source = re.sub(r"\\LMSuppressTrainerMeaning(?:true|false)", "", source)
        source = source.replace(r"\TriptychRightsNoticeRenderedtrue", "").replace(r"\AIDisplayDocumentRevisionTimestamp", "")
        tokens = self.tokens
        def stash(content):
            token = "SERVERPRINTBLOCK" + str(len(tokens)).zfill(5) + "END"
            tokens[token] = content
            return "\n\n" + token + "\n\n"
        def block(name, args):
            self.block_counter += 1
            key = "block-" + str(self.block_counter).zfill(4)
            if name == "actionrowid":
                key = args[0]
                value = '<article class="action" data-unit-id="' + key + '"><h4>' + html.escape(key) + '</h4><dl>'
                value += ''.join('<dt>' + label + '</dt><dd>' + self.fragment(value) + '</dd>' for label, value in
                                 zip(("Cue", "Actor", "Action", "Finish / next"), args[1:])) + '</dl></article>'
                self.unit(key, "ceremonial-action", value)
                return value
            if name in {"LMAction", "LMCompactTrainerAction"}:
                return '<article class="action" data-source-action="' + html.escape(args[0]) + '"><h4>' + self.fragment(args[0] + " · " + args[1]) + '</h4>' + self.fragment(r"\textbf{DO:} " + args[2] + r"\par\textbf{HOW / FINISH:} " + args[3]) + '</article>'
            if name in {"LMDialogueFirst", "LMDialogueRepeat", "LMDialogueLiteral"}:
                if name == "LMDialogueLiteral":
                    number, actor, cue, response = args
                    sound = ""
                else:
                    number, cue, identity = args
                    actor, response = "Priest", self.bank[identity]["latin"]
                    sound = self.bank[identity]["sound"] if name == "LMDialogueFirst" else ""
                return '<article class="response" data-dialogue="' + html.escape(number) + '"><h4>' + html.escape(number) + '</h4><div class="paired-lanes"><div><strong>℣ · ' + html.escape(actor) + '</strong>' + self.fragment(cue) + '</div><div><strong>℟ · Both</strong>' + self.fragment(r"\textbf{" + response + "}") + (('<strong>SAY IT</strong>' + self.fragment(sound)) if sound else '') + '</div></div></article>'
            if name == "LMPhraseBlock":
                return '<article class="response"><h4>' + self.fragment(args[0] + " · " + args[1]) + '</h4>' + self.fragment(r"\textbf{" + args[2] + "}") + '<strong>SAY IT</strong>' + self.fragment(args[3]) + '</article>'
            if name in {"LMBranch", "LMTrainerNote", "TerminalNote"}:
                return '<aside class="branch"><strong>' + self.fragment(args[0]) + '</strong>' + self.fragment(args[1]) + '</aside>'
            if name in {"LMPageIntro", "LMDiagramNote", "LMModelChoice"}:
                return self.fragment(args[0])
            if name == "masterybox":
                return '<blockquote>' + self.fragment(args[0]) + '</blockquote>'
            if name == "serverguidetitle":
                return '<header><h1>' + self.fragment(args[0]) + '</h1>' + self.fragment(args[1]) + self.fragment(args[2]) + '</header>'
            if name == "PrintServerAnswer":
                identity = args[0]
                item = self.bank[identity]
                value = '<article class="response" data-unit-id="response-' + identity + '"><h3>' + self.fragment(item["title"]) + '</h3>'
                value += ''.join('<strong>' + label + '</strong>' + self.fragment(text) for label, text in
                                 (("YOUR JOB", self.lookup["job", identity]), ("HEAR", self.lookup["cue", identity]),
                                  ("RESPONSE", item["latin"]), ("LATIN CHUNKS", item["learner"]),
                                  ("SAY IT LIKE", item["sound"]), ("MEANING", item["meaning"]))) + '</article>'
                self.unit("response-" + identity, "response-reference", value)
                return value
            if name in {"PrintAightAnswer", "PrintMassOrderVoiceMap", "SolemnEveryRoleTrack", "LMTitlePage", "LMReadingKey", "LMModelKeyLine", "coachreference"}:
                value = self.definitions[name][2]
                value = re.sub(r"\\ifdefined\\LMTitleApparatus.*?\\fi", "", value, flags=re.S)
                if name == "SolemnEveryRoleTrack":
                    boxes = calls(value, "parbox", 2)
                    if len(boxes) != 1:
                        raise Refusal("Solemn role reminder has changed its source container")
                    value = boxes[0][0][1]
                rendered = self.render_tex(value)
                if name == "PrintAightAnswer":
                    rendered = '<section data-unit-id="response-A8">' + rendered + '</section>'
                    self.unit("response-A8", "response-reference", rendered)
                return rendered
            if name in {"rolecard", "mcrolerow", "MCSceneTile", "SolemnMapStop"}:
                return '<section class="role"><h3>' + self.fragment(args[0]) + '</h3>' + ''.join(self.render_tex(value) for value in args[1:]) + '</section>'
            if name in {"mcroleheading", "actionsection"}:
                return '<h3>' + self.fragment(args[0]) + '</h3>'
            if name == "servervoicerow":
                voice = args[2 + (0 if self.form == "low" else 1 if self.form == "cantata" else 2)]
                return '<article class="response">' + self.fragment(args[0]) + self.fragment(args[1]) + '<strong>Who answers</strong>' + self.fragment(voice) + '</article>'
            if name == "TrainerIPARow":
                return '<tr><th>' + args[0] + '</th><td>' + html.escape(tipa_unicode('/' + self.bank[args[0]]["ipa"] + '/')) + '</td></tr>'
            if name == "LMRenderGenerationMetadata":
                return '<p>Last revised (UTC): ' + html.escape(self.revised) + '</p>'
            if name == "TriptychRightsNotice":
                # Text is sourced from the same preamble, not a new rights grant.
                return self.render_tex(self.rights)
            if name == "LMLaneHeadings":
                return '<div class="paired-lanes"><strong>℣ · Priest’s cue</strong><strong>℟ · Both answer</strong></div>'
            if name.endswith("Diagram") or name.startswith("LMScene"):
                self.diagram_counts[name] = self.diagram_counts.get(name, 0) + 1
                identity = "diagram-" + name + "-" + str(self.diagram_counts[name])
                rendered = self.diagram(name).replace('<figure ', '<figure data-unit-id="' + identity + '" ', 1)
                self.unit(identity, "diagram", rendered, macro=name)
                return rendered
            raise Refusal("unimplemented structural macro " + name)
        commands = {"actionrowid": 5, "actionsection": 1, "rolecard": 2, "mcroleheading": 1, "mcrolerow": 2,
                    "MCSceneTile": 3, "SolemnMapStop": 4, "servervoicerow": 5, "TrainerIPARow": 1,
                    "LMAction": 4, "LMCompactTrainerAction": 4, "LMBranch": 2, "LMTrainerNote": 2,
                    "TerminalNote": 2, "LMPageIntro": 1, "LMDiagramNote": 1, "LMModelChoice": 1,
                    "LMDialogueFirst": 3, "LMDialogueRepeat": 3, "LMDialogueLiteral": 4, "LMPhraseBlock": 5,
                    "PrintServerAnswer": 1, "masterybox": 1, "serverguidetitle": 3}
        events = [(start, end, name, args) for name, count in commands.items() for args, start, end in calls(source, name, count)]
        zero = {"PrintAightAnswer", "PrintMassOrderVoiceMap", "SolemnEveryRoleTrack", "LMTitlePage", "LMReadingKey", "LMModelKeyLine",
                "LMRenderGenerationMetadata", "TriptychRightsNotice", "LMLaneHeadings", "coachreference"}
        zero.update(self.diagram_names)
        for name in zero:
            events.extend((match.start(), match.end(), name, []) for match in re.finditer(re.escape("\\" + name) + r"(?![A-Za-z@])", source))
        out, offset = [], 0
        for start, end, name, args in sorted(events):
            if start < offset:
                continue
            out.append(source[offset:start])
            out.append(stash(block(name, args)))
            offset = end
        out.append(source[offset:])
        text = ''.join(out)
        # Format-only environments are replaced without dropping their content.
        for name in ("actiontable", "servervoicetable"):
            text = text.replace(r"\begin{" + name + "}", "").replace(r"\end{" + name + "}", "")
        text = replace(text, "label", 1, lambda a: stash('<span id="' + html.escape(a[0], quote=True) + '"></span>'))
        text = re.sub(r"\\begin\{mcroleroute\}\{([^}]+)\}", lambda m: stash('<h4>' + html.escape(m[1]) + ' · Every scene</h4>' + self.fragment(self.definitions["MCRoleAlways"][2])), text)
        text = text.replace(r"\end{mcroleroute}", "")
        box = re.compile(r"\\begin\{(learnerbox|coachbox|watchbox|familybox)\}\s*\{")
        while match := box.search(text):
            title, end = web.brace_group(text, match.end() - 1)
            stop = text.find(r"\end{" + match[1] + "}", end)
            if stop < 0:
                raise Refusal("unclosed source teaching box")
            value = '<blockquote><h4>' + self.fragment(title) + '</h4>' + self.render_tex(text[end:stop]) + '</blockquote>'
            text = text[:match.start()] + stash(value) + text[stop + len(r"\end{" + match[1] + "}"):]
        for name, count in (("addcontentsline", 3), ("addtocontents", 2), ("microtypesetup", 1),
                            ("titleformat", 5), ("titlespacing", 4), ("setcounter", 2),
                            ("setlength", 2), ("addtolength", 2), ("enlargethispage", 1)):
            text = replace(text, name, count, lambda a: "")
        text = text.replace(r"\global", "")
        text = web.REGISTER_ASSIGNMENT_RE.sub("", text)
        text = re.sub(r"\\hrule(?:\s+height\s*[0-9.]+(?:pt|in|em|cm))?", "", text)
        text = re.sub(r"\\(?:EndLMPage|rolecardstart|columnbreak|guidecontents|carddeckoddpage)(?![A-Za-z@])", "", text)
        text = text.replace(r"\begin{deepstudy}", "").replace(r"\end{deepstudy}", "")
        text = text.replace(r"\begin{multicols}{2}", "").replace(r"\end{multicols}", "")
        text = re.sub(r"\\AddToHookNext\{shipout/foreground\}\{.*?\\end\{tikzpicture\}\}", "", text, flags=re.S)
        text = web.drop_continuation_heads(web.terminate_swallowers(web.fix_column_specs(text)))
        rendered = self.fragment(text)
        for _ in range(6):
            before = rendered
            for token, value in tokens.items():
                rendered = rendered.replace('<p>' + token + '</p>', value).replace(token, value)
            if rendered == before:
                break
        if "SERVERPRINTBLOCK" in rendered:
            raise Refusal("a nested semantic source block was not restored")
        return rendered

    def render_guides(self):
        parts = []
        if self.form == "low":
            path = self.owner / "shared/low-mass-ceremony.tex"
            raw = self.read(path)
            begin = sorted((start, end, args, command) for command in ("BeginLMPage", "BeginLMSingleScenePage", "ContinueLMPairedScene")
                           for args, start, end in calls(raw, command, 3))
            title = self.render_tex(raw[:begin[0][0]])
            parts.append(dict(id="title", kind="guide-title", html='<section class="guide-part">' + title + '</section>'))
            action_locations = {}
            inventory = self.read(self.owner / "research/ceremonial-inventory.md")
            expected_actions = [row[0] for row in liturgy._rows(inventory, r"LM-\d{3}", 11)]
            for index, (start, end, args, command) in enumerate(begin):
                stop = begin[index + 1][0] if index + 1 < len(begin) else len(raw)
                content = self.render_tex(raw[end:stop])
                rail = self.render_tex(args[2]) if self.trainer else ""
                header = re.findall(r"^% PAGES?[^\n]*", raw[:start], re.M)
                identifiers = []
                if args[1] == "PREPARE AND MAP YOUR CHURCH":
                    identifiers = ["LM-001"]
                elif args[0] != "APPENDIX" and header:
                    latest = header[-1]
                    span = re.search(r"LM-(\d{3}) through LM-(\d{3})", latest)
                    identifiers = ["LM-" + str(n).zfill(3) for n in range(int(span[1]), int(span[2]) + 1)] if span else re.findall(r"LM-\d{3}", latest)
                own_ids = []
                for identity in identifiers:
                    if identity not in action_locations:
                        action_locations[identity] = f"scene-{index+1:02d}"
                        own_ids.append(identity)
                        self.unit(identity, "ceremonial-action-locator", "", source_scene=f"scene-{index+1:02d}",
                                  locator_basis="canonical route comment" if identity != "LM-001" else "canonical preparation inventory and preparation scene")
                anchors = ''.join('<span data-unit-id="' + identity + '"></span>' for identity in own_ids)
                title = '<h2>' + self.fragment(args[0] + " · " + args[1]) + '</h2>'
                value = '<section class="guide-part scene' + (' continuation' if command == 'ContinueLMPairedScene' else '') + '" data-scene="' + str(index + 1) + '">' + anchors + title
                value += ('<div class="trainer-layout"><aside class="trainer-rail">' + rail + '</aside><div>' + content + '</div></div>') if self.trainer else content
                parts.append(dict(id=f"scene-{index+1:02d}", kind="paired-scene", continuation=command == 'ContinueLMPairedScene',
                                  canonical_action_ids=own_ids, paired_source=path.relative_to(self.root).as_posix(), html=value + '</section>'))
            if set(action_locations) != set(expected_actions):
                raise Refusal("Low-Mass scene locators do not account for the canonical 43-action inventory")
            consumers = raw
            expected_responses = []
        else:
            main = self.read(self.leaf / "main.tex")
            _, body = web.split_document(main)
            def include(args):
                name = args[0]
                if name.endswith("sung-mass-diagrams"):
                    return ""
                path = self.root / "src" / self.provider / (name + ("" if name.endswith(".tex") else ".tex"))
                if "generation-metadata" in name:
                    return "\nLast revised (UTC): " + self.revised + "\n"
                return self.read(path)
            body = replace(body, "input", 1, include)
            content = self.render_tex(body)
            content += self.render_tex(self.rights)
            parts.append(dict(id="complete-guide", kind="guide", html='<section class="guide-part">' + content + '</section>'))
            inventory = self.read(self.owner / "research/ceremonial-inventory.md")
            prefix = "MC" if self.form == "cantata" else "SO"
            action_ids = [row[0] for row in liturgy._rows(inventory, prefix + r"-\d{3}", 11)]
            actual_ids = [unit["id"] for unit in self.units if unit["kind"] == "ceremonial-action"]
            if action_ids != actual_ids:
                raise Refusal("chronological HTML actions do not match independent ceremonial inventory order")
            expected_responses = ["response-" + identity for identity in self.bank]
            if set(expected_responses) != {unit["id"] for unit in self.units if unit["kind"] == "response-reference"}:
                raise Refusal("guide response references do not match canonical response inventory")
            expected_actions = action_ids
            consumers = self.read(self.owner / "shared" / ("missa-cantata-role-sheets.tex" if self.form == "cantata" else "solemn-role-sheets.tex"))
            consumers += self.read(self.owner / "shared" / ("missa-cantata-ceremony.tex" if self.form == "cantata" else "solemn-ceremony.tex"))
        active_names = self.diagram_names
        expected_diagrams = []
        for name in active_names:
            count = len(re.findall(re.escape('\\' + name) + r'(?![A-Za-z@])', web.mask_tex_comments(consumers)))
            expected_diagrams += ["diagram-" + name + "-" + str(n) for n in range(1, count + 1)]
        self.expected = expected_actions + expected_responses + sorted(expected_diagrams)
        return parts

    def finish(self, parts, print_expectation=None):
        metadata = self.read(self.leaf / "generation-metadata.tex")
        match = re.search(r"\\AIDocumentRevisionTimestamp\{([^}]+)\}", metadata)
        revised = match[1] if match else None
        title_match = re.search(r"pdftitle\s*=\s*\{([^}]+)\}", self.read(self.leaf / "main.tex"))
        title = title_match[1] if title_match else self.name
        if self.cards:
            if self.form == "low":
                raw = self.definitions["LowMassFinalNotice"][2]
                node = re.search(r"at\s*\([^)]*\)\s*\{", raw)
                notice, _ = web.brace_group(raw, node.end() - 1)
                notice = self.fragment(notice.replace(r"\AIDocumentRevisionTimestampValue", self.revised))
            else:
                notice = '<p><strong>Last revised (UTC):</strong> ' + html.escape(self.revised) + '</p>' + self.render_tex(self.rights)
            final_back = next(part for part in reversed(parts) if part.get("side") == "back")
            final_back["html"] = final_back["html"].removesuffix('</section>') + '<footer class="sheet-notice" data-unit-id="card-revision-rights">' + notice + '</footer></section>'
            self.unit("card-revision-rights", "revision-rights", notice)
            self.expected.append("card-revision-rights")
            if parts[-1]["kind"] == "apparatus":
                self.units.insert(len(self.units) - 2, self.units.pop())
        # Pandoc returns block fragments; a heading or label receives only its
        # paragraph's inline children, without malformed nested paragraphs.
        def headings(value):
            return re.sub(r"<(h[1-6]|strong)><p>((?:(?!</p>).)*)</p></\1>",
                          r"<\1>\2</\1>", value, flags=re.S)
        for part in parts:
            part["html"] = headings(part["html"])
        for unit in self.units:
            unit["html"] = headings(unit["html"])
        ids = [unit["id"] for unit in self.units]
        if len(ids) != len(set(ids)) or set(ids) != set(self.expected):
            raise Refusal("rendered unit coverage does not match the independent expected selection")
        for part in parts:
            if len(part["html"].encode()) >= 750_000:
                raise Refusal("HTML part exceeds the bounded part budget")
        body = "".join(part["html"] for part in parts)
        dom_ids = re.findall(r'data-unit-id="([^"]+)"', body)
        if Counter(dom_ids) != Counter(self.expected):
            raise Refusal("actual HTML unit IDs differ from the independent expected selection: missing=" +
                          str(list((Counter(self.expected) - Counter(dom_ids)).elements())) + "; extra=" +
                          str(list((Counter(dom_ids) - Counter(self.expected)).elements())))
        if print_expectation and dom_ids != print_expectation["expected_print_units"]:
            raise Refusal("physical DOM order differs from independent canonical source expectation")
        if print_expectation is None:
            raise Refusal("independent ordered source selection is required")
        expectations = print_expectation["print_unit_expectations"]
        if print_expectation["expected_print_units"] != [unit["id"] for unit in expectations]:
            raise Refusal("independent source order records disagree")
        for source, digest in print_expectation["source_selection"]["source_inputs"].items():
            if sha(_source_bytes(self.root, self.root / source, self.inputs)) != digest:
                raise Refusal("source order belongs to another source revision: " + source)
        expected = [dict(id=unit["id"], source="server:" + unit["id"], occurrence=unit["occurrence_id"])
                    for unit in expectations]
        source_digest = sha(json.dumps(self.inputs, sort_keys=True))
        selection_digest = sha(json.dumps(expected, sort_keys=True, separators=(",", ":")))
        from _web_print_server_schedule import verify_assembly
        assembly = verify_assembly(self._assembly_schedule, parts, self.assets, root=self.root)
        # Owner authority covers these exact final UTF-8 bodies. The cold
        # preparer must verify this pin before normalizing or transporting a
        # part; it cannot manufacture authority from subsequently changed HTML.
        for part in parts:
            part["html_sha256"] = sha(part["html"])
        identity = "publication:" + self.provider + "/" + self.output_id
        coverage = dict(status="pass", output_id=identity, source_digest=source_digest,
                        selection_digest=selection_digest, expected_units=expected,
                        editorial_review=False, physical_print_review=False, gaps=self.gaps,
                        final_assembly=assembly,
                        literal_coverage=dict(status="pass", scope="canonical-expanded-fragments", fragments=len(self.fragment_audits),
                                              units=sum(item["source_units"] for item in self.fragment_audits),
                                              ledger_digest=sha(json.dumps(self.fragment_audits, sort_keys=True))))
        return dict(id=identity, output_id=self.provider + "/" + self.output_id,
                    print_type="server-cards" if self.cards else "server-guide", page_format="letter-full-bleed",
                    title=title, revision=revised, language="en", source_digest=source_digest,
                    selection_digest=selection_digest, expected_units=expected, coverage_result=coverage,
                    parts=parts, assets=self.assets, sources={"server:" + unit["id"]: unit["source_refs"] for unit in expectations},
                    source_inputs=self.inputs, units=self.units, **print_expectation,
                    renderer=dict(code_sha256=sha(Path(__file__).read_bytes()),
                                  converter="injected" if self.fragment_renderer is not pandoc_fragment else _checked_pandoc(pandoc_command()),
                                  ipa_mapping="TIPA 1.3 appendix A and tipauni 0.7a; bounded source repertoire; unknown symbols refuse"))



def expected_card_print_selection(root: Path, provider: str, output_id: str):
    """Derive physical reading order from selected source grids, before rendering.

    The independent research manifest supplies the allowable face identities;
    canonical TeX grid invocations supply physical sheet/slot order. No HTML,
    rendered unit inventory, PDF, or diagram payload is inspected.
    """
    root = root.resolve()
    _provider(provider)
    output_id = output_id.removeprefix(provider + "/")
    name = output_id.rsplit("/", 1)[-1]
    if output_id not in [BASE + "/" + item for item in LEAVES if item.endswith(("flash-cards", "cue-cards"))]:
        raise Refusal("not an exact declared server card output")
    form = "low" if name.startswith("01-") else "cantata" if name.startswith("02-") else "solemn"
    owner = root / "src" / provider / BASE
    hashes = {}
    def read(path):
        return _source_bytes(root, path, hashes).decode()
    states = {r"\ifLowMassGuide": form == "low", r"\ifMissaCantataGuide": form == "cantata",
              r"\ifSolemnMassGuide": form == "solemn", r"\ifCardsOnlyGuide": True,
              r"\ifResponseDataOnlyGuide": form == "low", r"\ifTrainerManualGuide": False,
              r"\ifChildBookletGuide": False, r"\ifTriptychRightsNoticeRendered": False}
    main_path = owner / name / "main.tex"
    main = read(main_path)
    manifest_path = owner / "research/flash-card-manifest.md"
    manifest = read(manifest_path)
    if form == "low":
        expected_pairs = [row[0].split(" / ")[0] for row in liturgy._rows(manifest, r"LM-F\d{2} / \d{2}", 4)]
        sources = [(main_path, main)]
        commands = {"LowMassFrontCard": 5, "LowMassBackCard": 5}
    else:
        expected_pairs = sorted(liturgy._manifest_card_ids(manifest, "R01"))
        expected_pairs += sorted(liturgy._manifest_card_ids(manifest, "MC-A" if form == "cantata" else "SO-A"))
        sources = [(path, read(path)) for path in (owner / "shared/response-reference.tex", owner / "shared" / ("missa-cantata-action-cards.tex" if form == "cantata" else "solemn-action-cards.tex"))]
        commands = {"integratedresponsefront": 3, "storedresponseback": 2, "integratedresponseback": 6,
                    "denseintegratedresponseback": 6, "flashfront": 2, "actionflashback": 4}
    units, sheets = [], []
    environment = "tikzpicture" if form == "low" else "flashgrid"
    for path, raw in sources:
        selected = liturgy._conditional(web.strip_tex_comments(raw), states)
        invocation_index = 0
        for grid in re.finditer(r"\\begin\{" + environment + r"\}(.*?)\\end\{" + environment + r"\}", selected, re.S):
            body = grid[1]
            events = sorted((start, end, command, args) for command, count in commands.items() for args, start, end in calls(body, command, count))
            if not events:
                continue
            sheet, ids = len(sheets) + 1, []
            side = "front" if sheet % 2 else "back"
            for slot, (start, end, command, args) in enumerate(events, 1):
                invocation_index += 1
                identity = "LM-F" + args[2] if form == "low" else args[0]
                source_side = "front" if command in {"LowMassFrontCard", "integratedresponsefront", "flashfront"} else "back"
                if source_side != side:
                    raise Refusal("canonical source expectation has a mixed or non-alternating grid")
                if form == "low":
                    expected_xy = (0.25 if slot % 2 else 4.30, (8.28, 5.76, 3.24, 0.72)[(slot - 1) // 2])
                    if tuple(map(float, args[:2])) != expected_xy:
                        raise Refusal("canonical Low Mass source coordinate differs from its ordered slot")
                key = identity + ":" + side
                ids.append(identity)
                units.append(dict(id=key, occurrence_id=key, kind="card-face", sheet=sheet, slot=slot,
                                  row=(slot - 1) // 2 + 1, column=(slot - 1) % 2 + 1, side=side,
                                  source_refs=[dict(path=path.relative_to(root).as_posix(), sha256=hashes[path.relative_to(root).as_posix()],
                                                    macro=command, selected_invocation=invocation_index,
                                                    selected_invocation_sha256=sha(body[start:end]),
                                                    selected_span=[grid.start(1) + start, grid.start(1) + end])]))
            if len(ids) > (8 if form == "low" else 6):
                raise Refusal("canonical source expectation exceeds sheet capacity")
            if side == "back" and ids != [item for index in range(0, len(sheets[-1]), 2) for item in sheets[-1][index:index + 2][::-1]]:
                raise Refusal("canonical source expectation back is not row-mirrored")
            if form == "low":
                footer_calls = calls(body, "LowMassSheetFooter", 1)
                if len(footer_calls) > 1:
                    raise Refusal("canonical source repeats a sheet duplex instruction")
                for footer_args, start, end in footer_calls:
                    key = f"sheet-{sheet:02d}-duplex-instruction"
                    units.append(dict(id=key, occurrence_id=key, kind="duplex-instruction", sheet=sheet, side=side,
                                      source_refs=[dict(path=path.relative_to(root).as_posix(), sha256=hashes[path.relative_to(root).as_posix()],
                                                        macro="LowMassSheetFooter", selected_invocation_sha256=sha(body[start:end]),
                                                        selected_span=[grid.start(1)+start, grid.start(1)+end])]))
            sheets.append(ids)
    expected_set = {identity + ":" + side for identity in expected_pairs for side in ("front", "back")}
    if len(sheets) % 2 or len([u for u in units if u["kind"] == "card-face"]) != len(expected_set) or {u["id"] for u in units if u["kind"] == "card-face"} != expected_set:
        raise Refusal("canonical source order differs from independent face manifest")
    metadata_path = owner / name / "generation-metadata.tex"
    read(metadata_path)
    read(root / "src/common/preamble.tex")
    read(owner / "shared/server-guide-format.tex")
    units.append(dict(id="card-revision-rights", occurrence_id="card-revision-rights", kind="revision-rights", sheet=len(sheets), side="back",
                      source_refs=[dict(path=path.relative_to(root).as_posix(), sha256=hashes[path.relative_to(root).as_posix()]) for path in
                                   (main_path, metadata_path, root / "src/common/preamble.tex", owner / "shared/server-guide-format.tex")]))
    if r"\CardCompanionTerminalApparatus" in web.strip_tex_comments(main):
        units.append(dict(id="card-terminal-apparatus", occurrence_id="card-terminal-apparatus", kind="apparatus",
                          source_refs=[dict(path=path.relative_to(root).as_posix(), sha256=hashes[path.relative_to(root).as_posix()]) for path in (main_path, owner / "shared/server-guide-format.tex")]))
    return dict(expected_print_units=[u["id"] for u in units], print_unit_expectations=units,
                source_selection=dict(conditionals=states, identity_manifest=manifest_path.relative_to(root).as_posix(), source_inputs=hashes))


def expected_guide_print_selection(root: Path, provider: str, output_id: str):
    root = root.resolve()
    _provider(provider)
    output_id = output_id.removeprefix(provider + '/')
    name = output_id.rsplit('/', 1)[-1]
    if output_id not in [BASE + '/' + leaf for leaf in LEAVES if not leaf.endswith(('flash-cards', 'cue-cards'))]:
        raise Refusal('not an exact declared server guide output')
    form = 'low' if name.startswith('01-') else 'cantata' if name.startswith('02-') else 'solemn'
    trainer = 'trainer-manual' in name
    owner = root / 'src' / provider / BASE
    hashes = {}
    units = []
    diagram_counts = {}

    def read(path):
        return _source_bytes(root, path, hashes).decode()
    states = {'\\ifLowMassGuide': form == 'low', '\\ifMissaCantataGuide': form == 'cantata', '\\ifSolemnMassGuide': form == 'solemn', '\\ifCardsOnlyGuide': form == 'low', '\\ifResponseDataOnlyGuide': form == 'low', '\\ifTrainerManualGuide': trainer, '\\ifChildBookletGuide': form == 'low' and (not trainer), '\\ifTriptychRightsNoticeRendered': False}

    def select(value):
        return liturgy._conditional(web.strip_tex_comments(value), states)
    main_path = owner / name / 'main.tex'
    main = read(main_path)
    inventory_path = owner / 'research/ceremonial-inventory.md'
    inventory = read(inventory_path)
    response_path = owner / 'research/response-inventory.md'
    responses = read(response_path)
    definitions_path = owner / 'shared' / ('low-mass-diagrams.tex' if form == 'low' else 'sung-mass-diagrams.tex')
    definitions, _ = web.command_definitions(read(definitions_path))
    diagram_names = {k for k in definitions if k.startswith('LMScene') or k.endswith('Diagram')}

    def append(identity, kind, path, macro, selected, span, **extra):
        key = path.relative_to(root).as_posix()
        units.append(dict(id=identity, occurrence_id=identity, kind=kind, source_refs=[dict(path=key, sha256=hashes[key], macro=macro, selected_span=list(span), selected_text_sha256=sha(selected[span[0]:span[1]]))], **extra))

    def scan(path, value):
        selected = select(value)
        _, selected = web.command_definitions(selected)
        events = []
        for command, count in [('input', 1), ('actionrowid', 5), ('PrintServerAnswer', 1)]:
            events.extend(((start, end, command, args) for args, start, end in calls(selected, command, count)))
        for command in diagram_names | {'PrintAightAnswer'}:
            events.extend(((m.start(), m.end(), command, []) for m in re.finditer(re.escape('\\' + command) + '(?![A-Za-z@])', selected)))
        for start, end, command, args in sorted(events):
            if command == 'input':
                path2 = root / 'src' / provider / (args[0] + ('' if args[0].endswith('.tex') else '.tex'))
                raw2 = read(path2)
                if not args[0].endswith('sung-mass-diagrams'):
                    scan(path2, raw2)
            elif command == 'actionrowid':
                append(args[0], 'ceremonial-action', path, command, selected, (start, end))
            elif command in {'PrintServerAnswer', 'PrintAightAnswer'}:
                identity = 'response-' + ('A8' if command == 'PrintAightAnswer' else args[0])
                append(identity, 'response-reference', path, command, selected, (start, end))
            else:
                diagram_counts[command] = diagram_counts.get(command, 0) + 1
                append('diagram-' + command + '-' + str(diagram_counts[command]), 'diagram', path, command, selected, (start, end))
    if form == 'low':
        path = owner / 'shared/low-mass-ceremony.tex'
        raw = read(path)
        scenes = sorted(((start, end, args, command) for command in ('BeginLMPage', 'BeginLMSingleScenePage', 'ContinueLMPairedScene') for args, start, end in calls(raw, command, 3)))
        action_seen = set()
        scan(path, raw[:scenes[0][0]])
        for index, (start, end, args, command) in enumerate(scenes):
            stop = scenes[index + 1][0] if index + 1 < len(scenes) else len(raw)
            headers = re.findall('^% PAGES?[^\\n]*', raw[:start], re.M)
            ids = []
            if args[1] == 'PREPARE AND MAP YOUR CHURCH':
                ids = ['LM-001']
            elif args[0] != 'APPENDIX' and headers:
                span = re.search('LM-(\\d{3}) through LM-(\\d{3})', headers[-1])
                ids = ['LM-' + str(n).zfill(3) for n in range(int(span[1]), int(span[2]) + 1)] if span else re.findall('LM-\\d{3}', headers[-1])
            for identity in ids:
                if identity not in action_seen:
                    action_seen.add(identity)
                    append(identity, 'ceremonial-action-locator', path, command, raw, (start, end), source_scene=f'scene-{index + 1:02d}', locator_basis='canonical route comment' if identity != 'LM-001' else 'canonical preparation inventory and preparation scene', identity_manifest=inventory_path.relative_to(root).as_posix())
            if trainer:
                scan(path, args[2])
            scan(path, raw[end:stop])
        expected_actions = [row[0] for row in liturgy._rows(inventory, 'LM-\\d{3}', 11)]
        if action_seen != set(expected_actions):
            raise Refusal('source scene order does not cover independent Low Mass inventory')
    else:
        _, body = web.split_document(main)
        scan(main_path, body)
        prefix = 'MC' if form == 'cantata' else 'SO'
        expected_actions = [row[0] for row in liturgy._rows(inventory, prefix + '-\\d{3}', 11)]
        if [u['id'] for u in units if u['kind'] == 'ceremonial-action'] != expected_actions:
            raise Refusal('source order differs from independent ceremonial inventory')
        expected_responses = {'response-' + row[0] for row in liturgy._rows(responses, 'A\\d+', 6)}
        if {u['id'] for u in units if u['kind'] == 'response-reference'} != expected_responses:
            raise Refusal('source order differs from independent response inventory')
    if len({u['id'] for u in units}) != len(units):
        raise Refusal('canonical guide source order repeats unit identities')
    return dict(expected_print_units=[u['id'] for u in units], print_unit_expectations=units, source_selection=dict(conditionals=states, entrypoint=main_path.relative_to(root).as_posix(), source_inputs=hashes, identity_manifests=[inventory_path.relative_to(root).as_posix(), response_path.relative_to(root).as_posix()]))


def render_server_document(root: Path, provider: str, output_id: str, *,
                           asset_resolver: Callable | None = None,
                           fragment_renderer: Callable | None = None) -> dict:
    """Prepare one canonical server publication for the cold print producer.

    The resolver is an injected, source-bound `_web_print_assets` lookup. It
    returns `{id, src, sha256, bytes, source_inputs, includes_caption, ...}`
    for `(root, variant, macro)` and must verify the hydrated SVG itself.
    Text conversion may use pinned Pandoc 3.11. This module never renders
    diagrams, invokes TeX/PDF tools, hydrates assets, or writes products.
    """
    root = Path(root).resolve()
    # The public cold-producer boundary attests immutable compiler bytes,
    # including builds that advertise the same version. Source-only selection
    # helpers and explicit dependency-injection unit checks stay independent.
    from _web_print_publication import Refused, require_print_toolchain
    try:
        toolchain = require_print_toolchain(root)
    except Refused as error:
        raise Refusal(str(error)) from error
    adapter = Adapter(root, provider, output_id, asset_resolver=asset_resolver,
                      fragment_renderer=fragment_renderer)
    expectation = (expected_card_print_selection if adapter.cards else expected_guide_print_selection)(root, provider, output_id)
    parts = adapter.render_cards() if adapter.cards else adapter.render_guides()
    product = adapter.finish(parts, expectation)
    product["render_toolchain"] = toolchain
    return product
