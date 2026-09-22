#!/usr/bin/env python3
"""Mass-keyed commentary loci, and their projection onto any calendar's mass.

THE DEFECT THIS AVOIDS. A liturgical commentator heads his chapter with his own
Sunday number, and the numbers drift: Rupert of Deutz's "Dominica decima
octava" carries the 1962 Eighteenth Sunday's chants and Epistle with another
Gospel, and the 1962 Gospel of that Sunday is his NINETEENTH. Filing a locus by
its heading misfiles it; filing it by its Gospel alone loses the chapter that
shares six elements with the Mass. Only a comparison element by element reports
both truthfully.

WHAT IS STORED AND WHAT IS DERIVED. `src/sources/commentary/formulary-loci.yaml`
stores each locus as the commentator gives it: his heading as data, and the
elements he names -- incipits he quotes, scripture he cites or quotes, and his
own words where he describes rather than quotes. Nothing in it names a
calendar's mass. Every match is derived here, every run, against whichever
calendar is asked, so a stored match can never become a second source of truth
beside the calendar (`guidance/the-shape.md` section 2).

A match is a finding aid. It says where a commentator's Mass and the calendar's
share elements; it verifies nothing, and a study still reads and binds the locus.
"""
from __future__ import annotations

import re
import tomllib
import unicodedata
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Any, NamedTuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-commentary-formulary-loci/v1"
REPORT_SCHEMA = "triptych-commentary-formulary-report/v1"
LOCI_RELATIVE = Path("src/sources/commentary/formulary-loci.yaml")
CALENDARS_RELATIVE = Path("src/sources/calendars")
WORKS_RELATIVE = Path("src/sources/works")
NUMBERING = "vulgate"

GENRES = (
    "office-exposition",
    "mass-exposition",
    "missal-commentary",
    "sunday-sermons",
    "sunday-catena",
    "structural",
)
TREATMENTS = ("whole-office", "per-element", "single-element", "structural")
STATES = ("located", "inspected")
ROLES = (
    "introit", "collect", "lesson", "epistle", "gradual", "alleluia", "tract",
    "sequence", "gospel", "offertory", "secret", "preface", "communion",
    "postcommunion", "historia", "other",
)
# A locus is listed under a mass when it shares one of these, or two others.
ANCHOR_ROLES = ("introit", "collect", "lesson", "epistle", "gospel")
OCCASIONS = ("sunday-after-ember-saturday",)
EMBERS = ("advent", "lent", "pentecost", "september")

TOP_FIELDS = {"schema", "updated", "numbering", "works"}
WORK_FIELDS = {"work_id", "genre", "locus_grammar", "label_system", "writer", "notes", "loci"}
WRITER_FIELDS = {"person", "scope", "basis"}
LOCUS_FIELDS = {
    "locus", "read_in", "lines", "pages", "printed", "own_label", "own_label_in_layer",
    "season", "ordinal", "occasion", "treatment", "elements", "state", "checked_on", "notes",
}
OCCASION_FIELDS = {"kind", "embers"}
ELEMENT_FIELDS = {"role", "incipit", "ref", "said", "as", "alternative"}
ELEMENT_AS = ("verse", "antiphon", "response")

KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# A calendar mass whose key is `<anchor>-<n>` carries its own season and ordinal.
MASS_ORDINAL = re.compile(r"^(advent|epiphany|lent|easter|pentecost)-(\d+)$")
MASS_SEASON = {
    "advent": "advent",
    "epiphany": "after-epiphany",
    "lent": "lent",
    "easter": "after-easter",
    "pentecost": "after-pentecost",
}

# The calendars name their propers in their own words; the loci use one closed
# vocabulary. Ordinal words ("First Lesson", "Greater Alleluia") are stripped
# before the table is read, so every lesson and gradual of an Ember Saturday is
# a lesson and a gradual.
CALENDAR_ROLE = {
    "introit": "introit",
    "entrance antiphon": "introit",
    "collect": "collect",
    "lesson": "lesson",
    "reading": "lesson",
    "epistle": "epistle",
    "second reading": "epistle",
    "gradual": "gradual",
    "responsorial psalm": "gradual",
    "alleluia": "alleluia",
    "gospel acclamation": "alleluia",
    "verse before the gospel": "alleluia",
    "tract": "tract",
    "sequence": "sequence",
    "gospel": "gospel",
    "offertory": "offertory",
    "secret": "secret",
    "prayer over the offerings": "secret",
    "preface": "preface",
    "communion": "communion",
    "communion antiphon": "communion",
    "postcommunion": "postcommunion",
    "prayer after communion": "postcommunion",
}
_ORDINAL_WORDS = re.compile(r"^(?:first|second|third|fourth|fifth|sixth|seventh|greater)\s+")


class FormularyError(RuntimeError):
    """The loci file cannot be read at all."""


# ---------------------------------------------------------------------------
# Normalisation and comparison
# ---------------------------------------------------------------------------


def normalize_words(text: Any) -> list[str]:
    """An incipit as words: casefolded, unaccented, with Latin's spelling variants folded.

    j/i, v/u, y/i and the ae/oe digraphs and ligatures are one letter each, so
    "Laetatus" meets "Letatus" and "Moyses" meets "Moises". Nothing else is
    folded: two incipits that differ in a word are two incipits.
    """
    value = unicodedata.normalize("NFKD", str(text or "")).casefold()
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.replace("æ", "e").replace("œ", "e").replace("ae", "e").replace("oe", "e")
    value = value.translate(str.maketrans({"j": "i", "v": "u", "y": "i"}))
    return re.sub(r"[^a-z]+", " ", value).split()


def incipits_match(left: Any, right: Any) -> bool:
    """The shorter is a prefix of the longer, and at least two words long."""
    a, b = normalize_words(left), normalize_words(right)
    shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
    return len(shorter) >= 2 and longer[: len(shorter)] == shorter


def layer_text(text: str) -> str:
    """How a heading is found in a text layer: spacing folded, case folded."""
    return " ".join(text.split()).casefold()


class Span(NamedTuple):
    book: str
    begin: tuple[int, int]
    end: tuple[int, int]


_OPEN = 10_000


def _spans(record: dict[str, Any]) -> list[Span]:
    book = str(record.get("book") or "")
    spans: list[Span] = []
    for entry in record.get("ranges") or []:
        begin = (entry or {}).get("begin") or {}
        end = (entry or {}).get("end") or begin
        try:
            c1 = int(begin["chapter"])
            c2 = int(end.get("chapter", c1))
        except (KeyError, TypeError, ValueError):
            continue
        v1 = begin.get("verse") if isinstance(begin.get("verse"), int) else 0
        v2 = end.get("verse") if isinstance(end.get("verse"), int) else _OPEN
        spans.append(Span(book, (c1, v1), (c2, v2)))
    return spans


def overlaps(left: list[Span], right: list[Span]) -> bool:
    """Overlap at the precision each side recorded; a chapter is never narrowed."""
    return any(
        a.book == b.book and a.begin <= b.end and b.begin <= a.end
        for a in left
        for b in right
    )


class Citations:
    """The repository's one citation parser, and its one psalm concordance."""

    def __init__(self, root: Path = ROOT) -> None:
        tool = Path(root) / "tools" / "citations"
        if not tool.is_file():
            tool = ROOT / "tools" / "citations"
        self.module = SourceFileLoader("triptych_citations_formulary", str(tool)).load_module()
        import _psalms  # noqa: E402  (scripts/ is on the path of every caller)

        self._psalms = _psalms

    def parse(self, text: str) -> dict[str, Any]:
        return self.module.parse_citation(str(text))

    def spans(self, text: str, numbering: str = NUMBERING) -> list[Span]:
        """Spans of one citation, with psalms converted into the loci's numbering."""
        record = self.parse(text)
        if record.get("book") == self._psalms.PSALMS and numbering != NUMBERING:
            ranges = []
            for entry in record.get("ranges") or []:
                begin = dict(entry.get("begin") or {})
                end = dict(entry.get("end") or begin)
                b = self._psalms.convert_point(begin.get("chapter"), begin.get("verse"), numbering, NUMBERING)
                e = self._psalms.convert_point(
                    end.get("chapter", begin.get("chapter")), end.get("verse"), numbering, NUMBERING
                )
                ranges.append({"begin": {"chapter": b[0], "verse": b[1]}, "end": {"chapter": e[0], "verse": e[1]}})
            record = {**record, "ranges": ranges}
        return _spans(record)


# ---------------------------------------------------------------------------
# The library, as far as a locus row needs it
# ---------------------------------------------------------------------------


def _toml(path: Path) -> dict[str, Any] | None:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def artifact_record(root: Path, artifact_id: str) -> dict[str, Any] | None:
    """An artifact's manifest, located from its id without scanning the library."""
    kind, _, rest = str(artifact_id).partition(".")
    parts = rest.split(".")
    if kind != "artifact" or len(parts) < 4:
        return None
    path = (
        Path(root) / WORKS_RELATIVE / parts[0] / parts[1] / "editions" / parts[2]
        / "artifacts" / ".".join(parts[3:]) / "artifact.toml"
    )
    data = _toml(path)
    if data is None or data.get("id") != artifact_id:
        return None
    return {**data, "_manifest": path}


def work_record(root: Path, work_id: str) -> dict[str, Any] | None:
    parts = str(work_id).split(".")
    if len(parts) != 3 or parts[0] != "work":
        return None
    data = _toml(Path(root) / WORKS_RELATIVE / parts[1] / parts[2] / "work.toml")
    return data if data and data.get("id") == work_id else None


def owning_work(artifact_id: str) -> str:
    parts = str(artifact_id).split(".")
    return f"work.{parts[1]}.{parts[2]}" if len(parts) >= 4 else ""


def _contained(root: Path, artifact_id: str, work_id: str) -> bool:
    """Whether the containment inventory records `work_id` inside this artifact's bytes."""
    path = Path(root) / "src/sources/inventories/source-containment-v1.toml"
    data = _toml(path) or {}
    holders = {artifact_id, owning_work(artifact_id)}
    for container in data.get("containers") or []:
        if str((container or {}).get("id")) in holders:
            for part in container.get("constituents") or []:
                if str((part or {}).get("work_id") or "") == work_id:
                    return True
    return False


# ---------------------------------------------------------------------------
# Loading and validation
# ---------------------------------------------------------------------------


def _read(root: Path) -> tuple[dict[str, Any], Any]:
    path = Path(root) / LOCI_RELATIVE
    if not path.is_file():
        raise FormularyError(f"{LOCI_RELATIVE.as_posix()}: not found")
    text = path.read_text(encoding="utf-8")
    try:
        node = yaml.compose(text)
        data = yaml.safe_load(text)
    except yaml.YAMLError as error:
        raise FormularyError(f"{LOCI_RELATIVE.as_posix()}: {error}") from error
    if not isinstance(data, dict):
        raise FormularyError(f"{LOCI_RELATIVE.as_posix()}: not a mapping")
    if data.get("schema") != SCHEMA:
        raise FormularyError(
            f"{LOCI_RELATIVE.as_posix()}: declares schema {data.get('schema')!r}, expected {SCHEMA!r}"
        )
    return data, node


def load(root: Path = ROOT) -> dict[str, Any]:
    return _read(root)[0]


def works_of(data: dict[str, Any]) -> list[dict[str, Any]]:
    value = data.get("works") or []
    return [w for w in value if isinstance(w, dict)] if isinstance(value, list) else []


def _unquoted(node: Any, trail: str, errors: list[str]) -> None:
    """Every string scalar is quoted: a comma or colon in Latin must not split it."""
    if isinstance(node, yaml.MappingNode):
        for key, value in node.value:
            _unquoted(value, f"{trail}.{key.value}" if trail else str(key.value), errors)
    elif isinstance(node, yaml.SequenceNode):
        for index, value in enumerate(node.value):
            _unquoted(value, f"{trail}[{index}]", errors)
    elif isinstance(node, yaml.ScalarNode):
        if node.tag == "tag:yaml.org,2002:str" and node.style not in ("'", '"', "|", ">"):
            errors.append(
                f"{LOCI_RELATIVE.as_posix()}: {trail} = {node.value!r} is unquoted; quote every "
                "string, since an unquoted comma or colon silently splits it (guidance/sources.md)"
            )


def _layer_lines(path: Path) -> list[str] | None:
    try:
        return path.read_text(encoding="utf-8").split("\n")
    except (OSError, UnicodeDecodeError):
        return None


def _range(value: Any) -> tuple[int, int] | None:
    if (
        isinstance(value, list) and len(value) == 2
        and all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in value)
        and value[0] <= value[1]
    ):
        return value[0], value[1]
    return None


def validate(root: Path = ROOT, citations: Citations | None = None, registry: Any = None) -> list[str]:
    """Every reason the loci file cannot be trusted, sorted and deduplicated."""
    root = Path(root)
    where = LOCI_RELATIVE.as_posix()
    try:
        data, node = _read(root)
    except FormularyError as error:
        return [str(error)]
    errors: list[str] = []
    _unquoted(node, "", errors)
    unknown = sorted(set(data) - TOP_FIELDS)
    if unknown:
        errors.append(f"{where}: unknown top-level fields: {', '.join(unknown)}")
    if data.get("numbering") != NUMBERING:
        errors.append(f"{where}: numbering must be {NUMBERING!r}; every ref is a Clementine Vulgate address")
    if not DATE.match(str(data.get("updated") or "")):
        errors.append(f"{where}: updated must be an ISO date")
    citations = citations or Citations(root)
    layers: dict[str, list[str] | None] = {}
    seen_works: set[str] = set()
    for w_index, work in enumerate(works_of(data), start=1):
        work_id = str(work.get("work_id") or "")
        wlabel = f"{where}: works[{w_index}] {work_id}".rstrip()
        unknown = sorted(set(work) - WORK_FIELDS)
        if unknown:
            errors.append(f"{wlabel} has unknown fields: {', '.join(unknown)}")
        if work_id in seen_works:
            errors.append(f"{wlabel} is entered twice; one entry per work")
        seen_works.add(work_id)
        if work_record(root, work_id) is None:
            errors.append(f"{wlabel} names no work record in the library")
        if work.get("genre") not in GENRES:
            errors.append(f"{wlabel} genre {work.get('genre')!r} is not one of {', '.join(GENRES)}")
        for field in ("locus_grammar", "label_system"):
            if not str(work.get(field) or "").strip():
                errors.append(f"{wlabel} states no {field}")
        writer = work.get("writer")
        if writer is not None:
            if not isinstance(writer, dict):
                errors.append(f"{wlabel} writer must be a mapping")
            else:
                unknown = sorted(set(writer) - WRITER_FIELDS)
                if unknown:
                    errors.append(f"{wlabel} writer has unknown fields: {', '.join(unknown)}")
                for field in WRITER_FIELDS:
                    if not str(writer.get(field) or "").strip():
                        errors.append(f"{wlabel} writer states no {field}")
                if registry is not None and str(writer.get("person") or "") not in registry.by_id:
                    errors.append(f"{wlabel} writer {writer.get('person')!r} has no row in the author-standing registry")
        loci = work.get("loci")
        if not isinstance(loci, list) or not loci:
            errors.append(f"{wlabel} lists no loci")
            loci = []
        seen_loci: set[str] = set()
        for l_index, locus in enumerate(loci, start=1):
            if not isinstance(locus, dict):
                errors.append(f"{wlabel} loci[{l_index}] must be a mapping")
                continue
            name = str(locus.get("locus") or "")
            label = f"{wlabel} {name or f'loci[{l_index}]'}"
            errors.extend(_locus_errors(root, work_id, locus, label, citations, layers))
            if name in seen_loci:
                errors.append(f"{label} is entered twice under this work")
            seen_loci.add(name)
    return sorted(set(errors))


def _locus_errors(
    root: Path,
    work_id: str,
    locus: dict[str, Any],
    label: str,
    citations: Citations,
    layers: dict[str, list[str] | None],
) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(locus) - LOCUS_FIELDS)
    if unknown:
        errors.append(f"{label} has unknown fields: {', '.join(unknown)}")
    for field in ("locus", "read_in", "own_label", "treatment", "state", "checked_on"):
        if not str(locus.get(field) or "").strip():
            errors.append(f"{label} states no {field}")
    treatment = locus.get("treatment")
    if treatment is not None and treatment not in TREATMENTS:
        errors.append(f"{label} treatment {treatment!r} is not one of {', '.join(TREATMENTS)}")
    if locus.get("state") is not None and locus.get("state") not in STATES:
        errors.append(f"{label} state {locus.get('state')!r} is not one of {', '.join(STATES)}")
    if locus.get("checked_on") is not None and not DATE.match(str(locus.get("checked_on"))):
        errors.append(f"{label} checked_on must be an ISO date")
    # Season and ordinal are the commentator's own heading, and come together.
    has_ordinal = "ordinal" in locus
    if has_ordinal and (not isinstance(locus["ordinal"], int) or isinstance(locus["ordinal"], bool) or locus["ordinal"] < 1):
        errors.append(f"{label} ordinal must be a positive integer, the commentator's own")
    if has_ordinal != ("season" in locus):
        errors.append(f"{label} gives season and ordinal together or neither")
    if "season" in locus and not KEBAB.match(str(locus.get("season") or "")):
        errors.append(f"{label} season must be kebab-case, such as after-pentecost")
    occasion = locus.get("occasion")
    if occasion is not None:
        if not isinstance(occasion, dict):
            errors.append(f"{label} occasion must be a mapping")
        else:
            unknown = sorted(set(occasion) - OCCASION_FIELDS)
            if unknown:
                errors.append(f"{label} occasion has unknown fields: {', '.join(unknown)}")
            if occasion.get("kind") not in OCCASIONS:
                errors.append(f"{label} occasion kind {occasion.get('kind')!r} is not one of {', '.join(OCCASIONS)}")
            embers = occasion.get("embers")
            if not isinstance(embers, list) or not embers or any(e not in EMBERS for e in embers):
                errors.append(f"{label} occasion embers must be a nonempty list drawn from {', '.join(EMBERS)}")
    # The layer: a tracked text is replayed; anything else is bounded by pages.
    artifact_id = str(locus.get("read_in") or "")
    artifact = artifact_record(root, artifact_id) if artifact_id else None
    if artifact_id and artifact is None:
        errors.append(f"{label} read_in {artifact_id!r} is not an artifact in the library")
    if artifact is not None and owning_work(artifact_id) != work_id and not _contained(root, artifact_id, work_id):
        errors.append(
            f"{label} read_in {artifact_id} belongs to {owning_work(artifact_id)}, and the containment "
            f"inventory does not record {work_id} inside it"
        )
    lines, pages = locus.get("lines"), locus.get("pages")
    if (lines is None) == (pages is None):
        errors.append(f"{label} gives exactly one of lines (a text layer) or pages (any other artifact)")
    if artifact is not None:
        media = str(artifact.get("media_type") or "").split(";")[0].strip()
        text_layer = media == "text/plain"
        if lines is not None:
            span = _range(lines)
            if span is None:
                errors.append(f"{label} lines must be [first, last], positive and ascending")
            elif not text_layer:
                errors.append(f"{label} lines are for a text/plain layer; {artifact_id} is {media}")
            elif artifact.get("storage") != "tracked" or not artifact.get("path"):
                errors.append(f"{label} lines need a tracked layer to replay; {artifact_id} is {artifact.get('storage')}")
            else:
                if artifact_id not in layers:
                    layers[artifact_id] = _layer_lines(Path(root) / str(artifact["path"]))
                layer = layers[artifact_id]
                if layer is None:
                    errors.append(f"{label} cannot read the layer of {artifact_id}")
                elif span[1] > len(layer):
                    errors.append(f"{label} lines {span[0]}-{span[1]} run past the layer's {len(layer)} lines")
                else:
                    heading = str(locus.get("own_label_in_layer") or locus.get("own_label") or "")
                    found = layer_text(" ".join(layer[span[0] - 1 : span[1]]))
                    if heading and layer_text(heading) not in found:
                        field = "own_label_in_layer" if locus.get("own_label_in_layer") else "own_label"
                        errors.append(
                            f"{label} {field} {heading!r} does not occur in lines {span[0]}-{span[1]} "
                            f"of {artifact_id}; the locus is filed at the wrong lines or the label is misread"
                        )
        if pages is not None:
            span = _range(pages)
            count = artifact.get("page_count")
            if span is None:
                errors.append(f"{label} pages must be [first, last], positive and ascending")
            elif text_layer:
                errors.append(f"{label} is read in a text layer, so give lines, which replay, not pages")
            elif isinstance(count, int) and span[1] > count:
                errors.append(f"{label} pages {span[0]}-{span[1]} run past the artifact's {count} pages")
    # Elements: none on a structural locus, and every one comparable on another.
    elements = locus.get("elements")
    if treatment == "structural":
        if elements:
            errors.append(f"{label} is structural and names no element; give it a non-structural treatment instead")
    elif treatment is not None:
        if not isinstance(elements, list) or not elements:
            errors.append(f"{label} names no element, and only a structural locus may")
            elements = []
        for e_index, element in enumerate(elements, start=1):
            elabel = f"{label} elements[{e_index}]"
            if not isinstance(element, dict):
                errors.append(f"{elabel} must be a mapping")
                continue
            unknown = sorted(set(element) - ELEMENT_FIELDS)
            if unknown:
                errors.append(f"{elabel} has unknown fields: {', '.join(unknown)}")
            if element.get("role") not in ROLES:
                errors.append(f"{elabel} role {element.get('role')!r} is not one of {', '.join(ROLES)}")
            if not element.get("incipit") and not element.get("ref"):
                errors.append(f"{elabel} gives neither an incipit nor a ref, so nothing can compare it")
            if element.get("incipit") and len(normalize_words(element["incipit"])) < 2:
                errors.append(f"{elabel} incipit needs at least two words to be compared")
            if element.get("as") is not None and element.get("as") not in ELEMENT_AS:
                errors.append(f"{elabel} as {element.get('as')!r} is not one of {', '.join(ELEMENT_AS)}")
            if element.get("ref"):
                try:
                    if not citations.spans(str(element["ref"])):
                        errors.append(f"{elabel} ref {element['ref']!r} parses to no range")
                except Exception as error:  # the parser's own refusal, verbatim
                    errors.append(f"{elabel} ref {element['ref']!r} does not parse: {error}")
    if treatment == "structural" and occasion is None:
        errors.append(f"{label} is structural and states no occasion, so no mass can list it")
    return errors


# ---------------------------------------------------------------------------
# Projection onto a calendar's mass
# ---------------------------------------------------------------------------


def calendar_role(name: str) -> str:
    base = str(name or "").split(" (", 1)[0].strip().casefold()
    base = _ORDINAL_WORDS.sub("", base)
    return CALENDAR_ROLE.get(base, "other")


def _incipit_of(proper: dict[str, Any]) -> str:
    if proper.get("incipit"):
        return str(proper["incipit"])
    text = " ".join(str(proper.get("text") or "").split())
    return " ".join(text.split()[:6])


class MassElement(NamedTuple):
    role: str
    name: str
    incipit: str
    refs: tuple[str, ...]
    spans: tuple[Span, ...]


def mass_elements(document: dict[str, Any], mass: dict[str, Any], citations: Citations) -> list[MassElement]:
    import _calendars  # noqa: E402

    numbering = str(document.get("psalm_numbering") or NUMBERING)
    entries, _ = _calendars.resolve_propers(document, mass)
    out: list[MassElement] = []
    for _, proper, _ in entries:
        role = calendar_role(str(proper.get("name") or ""))
        if role == "other":
            continue
        refs: list[str] = []
        spans: list[Span] = []
        for verse in proper.get("verses") or []:
            if not isinstance(verse, dict):
                continue
            ref = str(verse.get("ref") or "")
            try:
                found = citations.spans(ref, numbering) if ref else []
            except Exception:
                found = _spans(verse)
            if ref:
                refs.append(ref)
            spans.extend(found or _spans(verse))
        out.append(MassElement(role, str(proper.get("name") or ""), _incipit_of(proper), tuple(refs), tuple(spans)))
    return out


def _compare(element: dict[str, Any], candidates: list[MassElement], citations: Citations) -> tuple[str, str]:
    """`same` or `different` or `not-comparable`, with what decided it."""
    comparable = False
    spans = citations.spans(str(element["ref"])) if element.get("ref") else []
    for candidate in candidates:
        if element.get("incipit") and candidate.incipit:
            comparable = True
            if incipits_match(element["incipit"], candidate.incipit):
                return "same", "incipit"
        if spans and candidate.spans:
            comparable = True
            if overlaps(spans, list(candidate.spans)):
                return "same", "ref"
    return ("different", "") if comparable else ("not-comparable", "")


def _mass_label(mass: dict[str, Any]) -> tuple[str | None, int | None]:
    found = MASS_ORDINAL.match(str(mass.get("key") or ""))
    if not found:
        return None, None
    return MASS_SEASON[found.group(1)], int(found.group(2))


def _drift(locus: dict[str, Any], mass: dict[str, Any]) -> dict[str, Any]:
    season, ordinal = _mass_label(mass)
    if "ordinal" not in locus:
        return {"status": "unnumbered", "note": "his heading carries no Sunday number"}
    if ordinal is None:
        return {"status": "not-comparable", "note": "the calendar's mass carries no season ordinal"}
    if (locus.get("season"), locus.get("ordinal")) == (season, ordinal):
        return {"status": "none"}
    return {
        "status": "label-drift",
        "note": f"his {locus.get('season')} {locus.get('ordinal')} against the calendar's {season} {ordinal}",
    }


def _occasion_masses(document: dict[str, Any], embers: list[str]) -> set[str]:
    """The mass each named Ember Saturday is followed by, in the calendar's own order."""
    wanted = {e: re.compile(rf"^{e}(?:-\d+)?-ember-saturday$") for e in embers}
    found: set[str] = set()
    for _, body in sorted((document.get("sections") or {}).items()):
        masses = [m for m in (body or {}).get("masses") or [] if isinstance(m, dict)]
        for index, mass in enumerate(masses[:-1]):
            if any(pattern.match(str(mass.get("key") or "")) for pattern in wanted.values()):
                found.add(str(masses[index + 1].get("key") or ""))
    return found


class Recurrence:
    """How many masses of a calendar each locus element matches, derived and cached."""

    def __init__(self, document: dict[str, Any], citations: Citations) -> None:
        import _calendars  # noqa: E402

        self.citations = citations
        self.by_mass = [
            (key, mass_elements(document, mass, citations))
            for key, mass in _calendars.mass_index(document).items()
        ]
        self.cache: dict[tuple, int] = {}

    def count(self, element: dict[str, Any]) -> int:
        key = (element.get("role"), element.get("incipit"), element.get("ref"))
        if key not in self.cache:
            self.cache[key] = sum(
                1
                for _, elements in self.by_mass
                if _compare(element, [e for e in elements if e.role == element.get("role")], self.citations)[0] == "same"
            )
        return self.cache[key]


def project_locus(
    work: dict[str, Any],
    locus: dict[str, Any],
    mass: dict[str, Any],
    elements: list[MassElement],
    citations: Citations,
    recurrence: Recurrence | None,
) -> dict[str, Any]:
    """One locus against one mass: a result per role, the listing, the drift, the weak flag."""
    by_role: dict[str, list[MassElement]] = {}
    for element in elements:
        by_role.setdefault(element.role, []).append(element)
    comparisons = []
    for element in locus.get("elements") or []:
        role = element.get("role")
        candidates = by_role.get(role, [])
        if not candidates:
            result, basis = "not-in-calendar", ""
        else:
            result, basis = _compare(element, candidates, citations)
        comparisons.append(
            {
                "role": role,
                "incipit": element.get("incipit"),
                "ref": element.get("ref"),
                "said": element.get("said"),
                "as": element.get("as"),
                "alternative": element.get("alternative"),
                "result": result,
                "basis": basis,
                "calendar": [
                    {"name": c.name, "incipit": c.incipit, "refs": list(c.refs)} for c in candidates
                ],
            }
        )
    named = {c["role"] for c in comparisons}
    unnamed = sorted({e.role for e in elements} - named, key=ROLES.index)
    same_roles = sorted({c["role"] for c in comparisons if c["result"] == "same"}, key=ROLES.index)
    anchors = [role for role in same_roles if role in ANCHOR_ROLES]
    others = [role for role in same_roles if role not in ANCHOR_ROLES]
    listed = bool(anchors) or len(others) >= 2
    weak = None
    if listed and recurrence is not None:
        counts = {
            f"{c['role']}:{c.get('incipit') or c.get('ref')}": recurrence.count(c)
            for c in comparisons
            if c["result"] == "same"
        }
        weak = {"weak": all(n > 1 for n in counts.values()), "recurrence": counts}
    return {
        "locus": locus.get("locus"),
        "own_label": locus.get("own_label"),
        "season": locus.get("season"),
        "ordinal": locus.get("ordinal"),
        "treatment": locus.get("treatment"),
        "listed": listed,
        "same": same_roles,
        "different": sorted(
            {c["role"] for c in comparisons if c["result"] == "different"} - set(same_roles), key=ROLES.index
        ),
        "not_named_by_commentator": unnamed,
        "elements": comparisons,
        "drift": _drift(locus, mass),
        "weak": weak,
        "read_in": locus.get("read_in"),
        "lines": locus.get("lines"),
        "pages": locus.get("pages"),
        "printed": locus.get("printed"),
        "state": locus.get("state"),
        "checked_on": locus.get("checked_on"),
        "notes": locus.get("notes"),
    }


def project(
    root: Path,
    calendar: str,
    mass_key: str,
    *,
    registry: Any = None,
    holdings: Any = None,
    citations: Citations | None = None,
) -> dict[str, Any]:
    """Every locus whose Mass shares elements with this mass, derived now, stored nowhere."""
    import _calendars  # noqa: E402

    root = Path(root)
    data = load(root)
    citations = citations or Citations(root)
    document = _calendars.load_document(root / CALENDARS_RELATIVE, calendar)
    mass = _calendars.mass_index(document).get(mass_key)
    if mass is None:
        raise ValueError(f"{calendar} has no mass {mass_key!r}")
    elements = mass_elements(document, mass, citations)
    recurrence = Recurrence(document, citations)
    occasioned: dict[tuple[str, ...], set[str]] = {}
    listed: list[dict[str, Any]] = []
    structural: list[dict[str, Any]] = []
    compared = 0
    for work in works_of(data):
        work_id = str(work.get("work_id") or "")
        record = work_record(root, work_id) or {}
        writer = work.get("writer") or {}
        person = None
        if registry is not None:
            person = registry.by_id.get(str(writer.get("person"))) if writer else registry.for_work(work_id)
        shared = {
            "work_id": work_id,
            "title": record.get("title", ""),
            "responsible": record.get("responsible", ""),
            "genre": work.get("genre"),
            "writer": (
                {"person": writer.get("person"), "name": (person or {}).get("name"), "scope": writer.get("scope")}
                if writer else None
            ),
            "standing": (
                {"person": person.get("id"), "name": person.get("name"), "standing": person.get("standing"),
                 "censures": len(person.get("censures") or [])}
                if person else None
            ),
        }
        if holdings is not None:
            found = holdings.for_work("", "", work_id, [])
            shared["holding"] = {
                "status": found["status"],
                "storage": _storage_summary(found),
            }
        for locus in work.get("loci") or []:
            if not isinstance(locus, dict):
                continue
            if locus.get("treatment") == "structural":
                occasion = locus.get("occasion") or {}
                key = tuple(occasion.get("embers") or ())
                if key not in occasioned:
                    occasioned[key] = _occasion_masses(document, list(key))
                if mass_key in occasioned[key]:
                    structural.append(
                        {**shared, "locus": locus.get("locus"), "own_label": locus.get("own_label"),
                         "occasion": occasion, "read_in": locus.get("read_in"), "lines": locus.get("lines"),
                         "pages": locus.get("pages"), "state": locus.get("state"),
                         "checked_on": locus.get("checked_on"), "notes": locus.get("notes")}
                    )
                continue
            compared += 1
            row = project_locus(work, locus, mass, elements, citations, recurrence)
            if row["listed"]:
                listed.append({**shared, **row})
    listed.sort(key=lambda row: (bool((row.get("weak") or {}).get("weak")), -len(row["same"])))
    season, ordinal = _mass_label(mass)
    return {
        "schema": REPORT_SCHEMA,
        "status": "ok",
        "calendar": calendar,
        "numbering": NUMBERING,
        "mass": {
            "key": mass_key,
            "name": mass.get("name"),
            "registry": mass.get("registry"),
            "season": season,
            "ordinal": ordinal,
        },
        "elements": [
            {"role": e.role, "name": e.name, "incipit": e.incipit, "refs": list(e.refs)} for e in elements
        ],
        "loci_compared": compared,
        "listed": listed,
        "structural": structural,
        "basis": {
            "loci": LOCI_RELATIVE.as_posix(),
            "listing": (
                "a locus is listed when it shares one of "
                + ", ".join(ANCHOR_ROLES)
                + ", or two other elements, with this mass; shared means a quoted incipit "
                "meets the calendar's (the shorter a prefix of the longer, two words at "
                "least) or a cited or quoted verse overlaps the calendar's at the "
                "precision recorded"
            ),
            "weak": "every shared element also matches other masses of this calendar",
            "drift": "the commentator's own season and Sunday number against the calendar's; information, not an error",
            "structural": "a locus about this Sunday's place in the year, listed by its occasion, never by elements",
            "finding_aid": "a match is a finding aid; the locus is still read and bound by the study that uses it",
        },
    }


def _storage_summary(found: dict[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in found.get("direct") or []:
        for storage, count in (record.get("artifact_storage") or {}).items():
            counts[storage] = counts.get(storage, 0) + count
    return dict(sorted(counts.items()))


def summary(root: Path = ROOT, citations: Citations | None = None, registry: Any = None) -> dict[str, Any]:
    """The loci file validated and counted, as the check verb prints it."""
    root = Path(root)
    errors = validate(root, citations, registry)
    try:
        data = load(root)
    except FormularyError:
        data = {}
    loci = [(work, locus) for work in works_of(data) for locus in work.get("loci") or [] if isinstance(locus, dict)]
    replayed = sum(1 for _, locus in loci if locus.get("lines") is not None)
    return {
        "schema": REPORT_SCHEMA,
        "status": "invalid" if errors else "ok",
        "errors": errors,
        "loci": LOCI_RELATIVE.as_posix(),
        "updated": data.get("updated"),
        "totals": {
            "works": len(works_of(data)),
            "loci": len(loci),
            "structural": sum(1 for _, locus in loci if locus.get("treatment") == "structural"),
            "labels_replayed": replayed,
            "labels_not_replayable": len(loci) - replayed,
            "by_genre": {
                genre: sum(1 for work in works_of(data) if work.get("genre") == genre)
                for genre in GENRES
                if any(work.get("genre") == genre for work in works_of(data))
            },
        },
    }
