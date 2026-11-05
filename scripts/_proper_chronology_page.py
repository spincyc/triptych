"""The Scriptural Date and Location page, generated whole.

The maintainer's decision of 2026-11-04: the Scriptural Date and Location page
of a proper study "is meant to be deterministic, not derived by agents". This
module is that page. It projects, and only projects:

- the leaf's chronology record (the dossier `tools/tpt proper-chronology
  record` writes as `research/chronology.toml`) through the orientation-v3
  rows and table that `_proper_chronology` already generates;
- the corpus's own orientation metadata (episode descriptions, settings and
  their sources) carried on those rows; and
- the source library's bibliographic labels for every cited source id.

Two variants share one row model. ``section`` is the expansive study's terminal
appendix: heading, a fixed introduction, the complete table, and evidence notes
for every row. ``page`` is the concise study's physical page 2: heading, the
same table, a fixed legend and a fixed pointer to the expansive section.
A one- or two-document guide, whose page 2 must stay one page, takes the other
two: ``sheet`` (the table with its legend, pointing to the appendix) on page 2
and ``evidence`` (the same notes) as a terminal appendix before its scope
appendix.

Nothing here is written by an author and nothing here refers to a row by its
position: a note is headed by exactly the Passage cell the table prints, so a
book is named one way on the whole page (the table's abbreviation, and the
corpus's own subject wording, which calls Revelation the Apocalypse). Absent
states are printed as what they are -- research pending, undated in tradition,
no calendar formulary, no reviewed appointment input -- never filled.
"""

from __future__ import annotations

import re
import tomllib
from functools import lru_cache
from pathlib import Path

import _chronology
import _proper_chronology as wiring

PROJECTION = "scriptural-date-location"
VERSION = 2
SECTION = "section"
PAGE = "page"
SHEET = "sheet"
EVIDENCE = "evidence"
VARIANTS = (SECTION, PAGE, SHEET, EVIDENCE)
EVIDENCE_HEADING = "Appendix: Evidence for the Scriptural Dates"
HEADING = "Scriptural Date and Location"
SECTION_LABEL = "sec:date-location"
EVIDENCE_LABEL = "sec:date-location-evidence"
ANNOTATIONS = wiring.ANNOTATIONS_RECORD.removesuffix(".tex")
TABLE = wiring.ORIENTATION_TABLE_RECORD.removesuffix(".tex")

# Every reader-facing sentence below is fixed text. Changing one changes every
# leaf at the next refresh, which is the point.
SECTION_INTRO = (
    "Each passage the Mass reads or sings from Scripture, in canonical order. "
    "The Context column distinguishes the event or setting, an attributed "
    "author's era, and the writing or formation of the text. The Date column "
    "gives calendar orientation. A proposal span summarizes the extent of "
    "numerical dates in the sources, including gaps between proposals. "
    "Undated occasions and relative formation bounds beside a composition "
    "date are left to the evidence. "
    "The complete alternatives and their evidence follow the table."
)
EVIDENCE_INTRO = (
    "For each passage, as the Scriptural Date and Location table names it: what "
    "is dated, how the corpus "
    "weighs each answer, the source's own words, and the sources cited. A "
    "subject the corpus does not date is reported as such and given no date."
)
PAGE_LEGEND = (
    "\\emph{c.}: approximately. Proposal spans summarize numerical alternatives, "
    "including gaps between them. \\emph{Disputed}: no preferred answer. "
    "An author's era does not date a poem's occasion; undated occasions are "
    "omitted. \\emph{(derived)} marks a calculation from the sources."
)
SHEET_POINTER = (
    "The evidence for every date, with its sources, is set out in the "
    "appendix \\emph{Evidence for the Scriptural Dates}."
)
PAGE_POINTER = (
    "The evidence for every date, with its sources, is set out in the "
    "expansive study's section \\emph{Scriptural Date and Location}."
)

ABSENT = {
    wiring.NO_CALENDAR_FORMULARY: (
        "No passage is dated here. This proper is appointed by a rite rather "
        "than by a day, and the calendar sources the Scripture chronology "
        "corpus is queried through carry no formulary for it. That is a limit "
        "of those sources, not a statement that the rite appoints no "
        "Scripture, and no date is supplied from anywhere else."
    ),
    "appointment-input-pending": (
        "No passage is dated here yet. This proper's appointed citations have "
        "not been entered as a reviewed query input for the Scripture "
        "chronology corpus (research pending), so the corpus has been asked "
        "about no passage and no date is supplied from anywhere else."
    ),
    "no-scripture": (
        "No passage is dated here: the corpus resolved no appointed Scripture "
        "for this proper."
    ),
}

GAP_SENTENCES = {
    wiring.QUALIFICATION_PENDING: ("The corpus holds a date for this that it reports from another "
                                   "edition by exception, which is not printed until the corpus "
                                   "records the source's own qualification of it (research pending)."),
    "research-pending": "The chronology corpus has not yet dated this (research pending).",
    "undated-in-tradition": "The traditional chronology gives this no date (undated in tradition).",
    wiring.NONUNIFORM: "The appointed verses do not share one answer, so none is given for the passage as a whole.",
    "not-alignable": "The corpus cannot align this passage with a dated subject.",
    "textually-distinct": "The corpus holds this passage's text as distinct from the dated text.",
}
DISPOSITION_WORDS = {"preferred": "preferred", "alternate": "alternative", "disputed": "disputed"}


# --- Source labels -------------------------------------------------------------


@lru_cache(maxsize=4)
def _source_records(root: str) -> dict[str, dict]:
    """Every source-library record, by id, read from the library's own tree."""
    records: dict[str, dict] = {}
    base = Path(root) / "src/sources/works"
    for path in sorted(base.rglob("*.toml")):
        text = path.read_text(encoding="utf-8")
        if not re.search(r'^id = "', text, re.M):
            continue
        try:
            data = tomllib.loads(text)
        except tomllib.TOMLDecodeError:
            continue
        identifier = data.get("id")
        if isinstance(identifier, str):
            records[identifier] = data
    return records


@lru_cache(maxsize=4)
def _bible_titles(root: str) -> dict[str, str]:
    titles: dict[str, str] = {}
    base = Path(root) / "src/sources/bibles"
    if not base.is_dir():
        return titles
    for edition in sorted(base.iterdir()):
        index = edition / "index.yaml"
        if not index.is_file():
            continue
        match = re.search(r"^edition:\s*(.+?)\s*$", index.read_text(encoding="utf-8"), re.M)
        titles[edition.name] = match.group(1).strip("'\"") if match else edition.name
    return titles


@lru_cache(maxsize=1)
def _book_short_names() -> dict[str, str]:
    """Corpus locus token -> the table's own short book name ("Matt.", "Ps.")."""
    by_name = wiring._short_book_names()
    shorts = {}
    for book in wiring._canon.books():
        short = by_name.get(book["name"], book["token"])
        # The period marks an abbreviation. "Kings" in "2 Kings." is a whole
        # word of the book's own title, so it takes none.
        word = re.sub(r"^[0-9]", "", book["token"])
        if short.endswith(".") and re.search(rf"\b{re.escape(word)}\b", book.get("title", "")):
            short = short[:-1]
        shorts[book["token"]] = short
    return shorts


def _locus(token_locus: str) -> str:
    """A corpus locus ("Matt.5.1") spelled as the table spells a citation."""
    match = re.fullmatch(r"([0-9]?[A-Za-z]+)\.([0-9]+)(?:\.([0-9]+))?", token_locus)
    if not match:
        return token_locus
    book = _book_short_names().get(match.group(1), match.group(1))
    if book == "Psalms":
        book = "Ps."
    return f"{book} {match.group(2)}" + (f":{match.group(3)}" if match.group(3) else "")


def _year(record: dict) -> str:
    for value in (record.get("date"), record.get("publication")):
        found = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", str(value or ""))
        if found:
            return found.group(1)
    return ""


def source_label(source: str, root: Path = wiring.ROOT) -> str:
    """The library's bibliographic label for one cited source id.

    The edition's own title (with its year when the title does not carry it),
    and a verified passage's own locus where the citation is to a passage. An
    id the library does not hold is printed as the id, because a label
    invented here would be a citation nobody checked.
    """
    if source.startswith("bible:"):
        _, edition, locus = (source.split(":", 2) + ["", ""])[:3]
        title = _bible_titles(str(root)).get(edition)
        return f"{title}, {_locus(locus)}" if title and locus else source
    records = _source_records(str(root))
    record = records.get(source)
    if record is None:
        return source
    kind = record.get("record_type")
    edition = record if kind == "edition" else records.get(record.get("edition_id", ""))
    if edition is None:
        return str(record.get("title") or source)
    title = str(edition.get("title") or source)
    year = _year(edition)
    label = f"{title} ({year})" if year and year not in title else title
    locus = record.get("locus") if kind == "passage" else None
    return f"{label}, {locus}" if locus else label


def _source_labels(sources: tuple[str, ...], root: Path) -> list[str]:
    """Labels in citation order, a bare edition dropped beside its own passage,
    and one Bible's loci gathered after its title."""
    labels: list[str] = []
    bible: dict[str, list[str]] = {}
    for source in sources:
        label = source_label(source, root)
        if source.startswith("bible:") and ", " in label and label != source:
            title, _, locus = label.rpartition(", ")
            if title not in bible:
                bible[title] = []
                labels.append("\0bible:" + title)
            if locus not in bible[title]:
                bible[title].append(locus)
        elif label not in labels:
            labels.append(label)
    labels = [item for item in labels
              if not any(other != item and other.startswith(item + ", ") for other in labels)]
    return [f"{item[7:]}: {_loci(bible[item[7:]])}" if item.startswith("\0bible:") else item
            for item in labels]


def _loci(spelled: list[str]) -> str:
    """Several loci of one Bible, each book named once per run."""
    parts, book = [], None
    for locus in spelled:
        name, _, address = locus.rpartition(" ")
        parts.append(address if name == book else locus)
        book = name
    return ", ".join(parts)


def _sources_tex(sources: tuple[str, ...], root: Path) -> str:
    return "; ".join(wiring.tex_escape(label) for label in _source_labels(sources, root))


# --- The notes -----------------------------------------------------------------


def _profile_names(corpus_root: Path | None) -> dict[str, str]:
    corpus = _chronology.load(corpus_root)
    return {
        identifier: str((profile.get("display") or {}).get("reader_name", "")).strip()
        for identifier, profile in corpus.profiles.items()
    }


def _primary_profile(corpus_root: Path | None, requested: str) -> str:
    corpus = _chronology.load(corpus_root)
    cascade = corpus.cascades.get(requested)
    return cascade.fallback_profiles[0] if cascade else requested


def _heading(row: wiring.OrientationRow) -> str:
    """The row's relation, as the table's Context cell opens it."""
    group = row.group
    if group.anchor_context is not None:
        return "Historical background"
    if group.relation == "narrated-event":
        return "Narrated event"
    if group.requested_profile == "catholic-critical-v1":
        return f"{wiring._relation_label(group.relation)}, Catholic critical comparison"
    return wiring._group_heading(group)


def _candidate(claim: wiring.AnnotationClaim, *, mixed: bool, primary: str,
               names: dict[str, str], root: Path) -> str:
    value = wiring._date_tex(claim.display_label)
    if mixed:
        value = f"{DISPOSITION_WORDS.get(claim.disposition, claim.disposition)}: {value}"
    details = []
    raw = claim.label.strip()
    # The source's words are shown unless the display already prints them.
    if raw and raw.rstrip(".").casefold() not in claim.display_label.casefold():
        details.append("``" + wiring.tex_escape(claim.label.strip()) + "''")
    if claim.profile != primary:
        details.append(wiring.tex_escape(names.get(claim.profile) or claim.profile))
    sources = _sources_tex(claim.sources, root)
    if sources:
        details.append(sources)
    return value + (f" ({'; '.join(details)})" if details else "")


def _row_note(row: wiring.OrientationRow, *, primary: str, names: dict[str, str],
              root: Path) -> str:
    group = row.group
    heading = "\\item \\textbf{" + wiring.tex_escape(_heading(row)) + "}"
    if not group.claims:
        sentence = GAP_SENTENCES.get(group.status, wiring.GAP_DISPLAY.get(group.status, group.status) + ".")
        described = ""
        if row.context_label:
            sources = _sources_tex(row.context_sources, root)
            described = " " + wiring.tex_escape(row.context_label) + (f" ({sources})" if sources else "") + "."
        return f"{heading}.{described} No date: {sentence[:1].lower() + sentence[1:]}"
    statuses = {claim.disposition for claim in group.claims}
    status = wiring._group_status(group.claims)
    word = DISPOSITION_WORDS.get(status, status)
    seen: set[tuple] = set()
    candidates = []
    for claim in group.claims:
        key = (claim.display_label.casefold(), claim.label, claim.sources, claim.profile)
        if key in seen:
            continue
        seen.add(key)
        candidates.append(_candidate(claim, mixed=len(statuses) > 1, primary=primary,
                                     names=names, root=root))
    title = wiring.tex_escape(group.claims[0].title)
    note = f"{heading} ({word if len(statuses) == 1 else 'answers differ'}). {title}: " + "; ".join(candidates) + "."
    if row.calendar_estimate:
        sources = _sources_tex(row.calendar_estimate.sources, root)
        note += (" Calendar orientation: " + wiring._date_tex(wiring.orientation_calendar_date(row))
                 + (f" ({sources})" if sources else "") + ".")
    if group.anchor_context is not None:
        note += (" These dates belong to that event, not to the passage or its composition, "
                 "and the two could fall in the same year.")
    if row.setting_label:
        sources = _sources_tex(row.context_sources, root)
        note += " Place: " + wiring.tex_escape(row.setting_label) + (f" ({sources})" if sources else "") + "."
    return note


def _passages(rows: tuple[wiring.OrientationRow, ...]) -> list[list[wiring.OrientationRow]]:
    groups: list[list[wiring.OrientationRow]] = []
    for row in rows:
        if row.passage_start or not groups:
            groups.append([])
        groups[-1].append(row)
    return groups


def _notes(found: wiring.AnnotationProjection, root: Path, corpus_root: Path | None) -> list[str]:
    """One list per passage, headed by the table's own Passage cell.

    A row whose evidence was already given under an earlier passage (the same
    relation, claims and place, as three Matthew chants share one composition)
    points back to that passage by name instead of repeating it.
    """
    names = _profile_names(corpus_root)
    primary = _primary_profile(corpus_root, found.profile)
    given: dict[str, str] = {}
    lines = []
    for rows in _passages(found.orientation_rows):
        passage = wiring.orientation_passage(rows[0])
        lines.append("\\par\\smallskip\\noindent\\textit{" + wiring._date_tex(passage) + "}\\par\\nobreak")
        lines.append("\\begin{itemize}[leftmargin=1.2em,itemsep=1pt,topsep=1pt,parsep=0pt]")
        for row in rows:
            note = _row_note(row, primary=primary, names=names, root=root)
            if note in given:
                lines.append("\\item \\textbf{" + wiring.tex_escape(_heading(row)) + "}. As under "
                             + wiring._date_tex(given[note]) + ".")
                continue
            given[note] = passage
            lines.append(note)
        lines.append("\\end{itemize}")
    return lines


# --- The page ------------------------------------------------------------------


def _header(document: str, variant: str) -> list[str]:
    return [
        "% Generated. Do not edit.",
        f"% Projection {PROJECTION}/{variant}, version {VERSION}: the Scriptural Date and",
        "% Location page, generated whole from research/chronology.toml, the Scripture",
        "% chronology corpus and the source library by tools/tpt document-types refresh.",
        f"% document: {document}",
    ]


def absent_reason(found: wiring.AnnotationProjection | None, reason: str = "") -> str:
    """Why the page dates nothing, or the empty string when it has rows."""
    if found is None:
        return reason or "appointment-input-pending"
    if found.state != wiring.APPOINTED:
        return found.state
    if not found.orientation_rows:
        return "no-scripture"
    return ""


def render(found: wiring.AnnotationProjection | None, *, document: str, variant: str,
           root: Path = wiring.ROOT, corpus_root: Path | None = None,
           absent: str = "") -> str:
    """One variant of the page, as complete TeX.

    ``found`` is the orientation-v3 projection of the leaf's dossier, or None
    when no dossier could be formed (``absent`` then names why).
    """
    if variant not in VARIANTS:
        raise wiring.ChronologyWiringError(f"unknown page variant {variant!r}")
    if found is not None and found.presentation != wiring.ORIENTATION_V3:
        raise wiring.ChronologyWiringError("the generated page reads orientation-v3 rows")
    why = absent_reason(found, absent)
    lines = _header(document, variant)
    if variant in (SHEET, EVIDENCE):
        return "\n".join(lines + _guide_variant(found, why, document, variant, root, corpus_root)) + "\n"
    lines += ["\\runninghead{" + HEADING + "}", "\\section{" + HEADING + "}"]
    if variant == SECTION:
        lines += ["\\label{" + SECTION_LABEL + "}", "", "{\\small " + SECTION_INTRO + "\\par}",
                  "\\medskip"]
    else:
        lines.append("\\zlabel{triptych:concise:chronology:start}")
    if why:
        lines.append("{\\small\\noindent " + ABSENT.get(why, ABSENT["appointment-input-pending"]) + "\\par}")
    else:
        lines += ["\\input{" + document + "/" + ANNOTATIONS + "}",
                  "\\input{" + document + "/" + TABLE + "}"]
    if variant == SECTION:
        if not why:
            lines += ["", "\\subsection{Evidence for each date}", "\\label{" + EVIDENCE_LABEL + "}",
                      "{\\small " + EVIDENCE_INTRO + "\\par}", "{\\small"]
            lines += _notes(found, root, corpus_root)  # type: ignore[arg-type]
            lines.append("\\par}")
    else:
        if not why:
            lines += ["\\smallskip", "{\\footnotesize\\noindent " + PAGE_LEGEND + " " + PAGE_POINTER + "\\par}"]
        lines.append("\\zlabel{triptych:concise:chronology:end}")
        # Page 2's running head is its own (propers-format's
        # \closerunninghead): a following page with no mark of its own (a
        # starred section) keeps the empty head it had, and the next numbered
        # section marks itself as usual. The expansive appendix needs none:
        # every apparatus after it marks its own head.
        lines.append("\\closerunninghead")
    return "\n".join(lines) + "\n"


def _guide_variant(found, why: str, document: str, variant: str, root: Path,
                   corpus_root: Path | None) -> list[str]:
    """The two variants of a one- or two-document guide (unnumbered headings,
    no page-two markers or running head, which those guides do not load)."""
    if variant == EVIDENCE:
        if why:
            return ["% No passage is dated, so there is no evidence appendix."]
        return (["\\section*{" + EVIDENCE_HEADING + "}", "\\label{" + EVIDENCE_LABEL + "}",
                 "{\\small " + EVIDENCE_INTRO + "\\par}", "{\\small"]
                + _notes(found, root, corpus_root) + ["\\par}"])
    lines = ["\\section*{" + HEADING + "}", "\\label{" + SECTION_LABEL + "}"]
    if why:
        return lines + ["{\\small\\noindent " + ABSENT.get(why, ABSENT["appointment-input-pending"]) + "\\par}"]
    return lines + ["\\input{" + document + "/" + ANNOTATIONS + "}",
                    "\\input{" + document + "/" + TABLE + "}",
                    "\\smallskip",
                    "{\\footnotesize\\noindent " + PAGE_LEGEND + " " + SHEET_POINTER + "\\par}"]


def projection(document: str, *, root: Path = wiring.ROOT, provider: str = "claude",
               corpus_root: Path | None = None) -> tuple[wiring.Dossier | None,
                                                          wiring.AnnotationProjection | None, str]:
    """The leaf's dossier and its orientation-v3 projection, or why neither exists."""
    try:
        found = wiring.dossier(document, root=root, provider=provider, corpus_root=corpus_root)
    except wiring.ChronologyWiringError as exc:
        # Only the absence of the leaf's own reviewed appointment input is an
        # absent state; any other refusal is a defect and stays one.
        if str(exc) == (f"missing appointment dependency: src/{provider}/{document}/"
                        "research/chronology-inputs.toml"):
            return None, None, "appointment-input-pending"
        raise
    if found.presentation not in ("", wiring.ORIENTATION_V3):
        raise wiring.ChronologyWiringError(
            f"{document} declares chronology_presentation = {found.presentation!r}; the generated "
            f"Scriptural Date and Location page reads {wiring.ORIENTATION_V3!r} rows, so migrate the "
            "declaration first")
    held = found._replace(presentation=wiring.ORIENTATION_V3)
    return held, wiring.annotations(held, presentation=wiring.ORIENTATION_V3), ""
