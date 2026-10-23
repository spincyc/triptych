"""Setting a reading of the Missal in the terminal.

What a proper says is written by the browser's own renderer and arrives here as
blocks of runs, each run carrying the class names the page gave it; this
module only decides how a class looks. An Ordinary element is set by its
`kind`, as `scripts/_ordinary_text.py` sets it for the command line: a rubric
bracketed, a heading as a heading, the words of a prayer plainly, a dialogue
with its cues. Nothing is chosen here that the reader state left open.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _ordinary_text import SPOKEN, absence_side  # noqa: E402

from .widgets import SUPERSCRIPT, Ink  # noqa: E402

# Run classes, most specific first, and the look each is given.
RUN_STYLES = (
    ("verse-num", "bold $accent"),
    ("vr-glyph", "bold $rubric"),
    ("inline-rubric", "italic $rubric"),
    ("elision", "$text-muted"),
    ("citation-numbering", "$text-muted"),
    ("citation-recast", "italic $text-muted"),
    ("proper-ref", "bold"),
    ("proper-form", "italic"),
    ("composed-label", "italic $text-muted"),
    ("unit-absence", "italic $warning"),
    ("composed-note", "italic $text-muted"),
    ("unit-claim", "italic $text-muted"),
    ("notice", "italic $warning"),
    ("uncompiled-mark", "bold $warning"),
    ("uncompiled", "italic $warning"),
    ("chapter-mark", "bold $text-muted"),
    ("citation-ref", "bold"),
    ("cycle-name", "bold underline"),
    ("proper-incipit", "italic"),
    ("text-side-label", "bold $text-muted"),
    ("proper-name", "bold $primary"),
    ("compare-status", "italic $warning"),
    ("compare-evidence", "$text-muted"),
    ("compare-anchor", "$text-muted"),
    ("compare-calendar-relation", "italic"),
    ("compare-calendar-name", "bold"),
    ("reasoning-locus", "italic $accent"),
    ("reasoning-latin", "italic"),
    ("reasoning-lead", ""),
)


def _run_style(classes: list[str], tags: list[str]) -> str:
    for name, style in RUN_STYLES:
        if name in classes:
            return style
    if "strong" in tags or "b" in tags:
        return "bold"
    if "em" in tags or "i" in tags:
        return "italic"
    return ""


def blocks(ink: Ink, items: list[dict], *, accent: str = "$primary") -> Ink:
    """The page's blocks, one line group each, styled by the classes they carry."""
    for block in items:
        heading = block.get("tag", "").startswith("h") or block.get("tag") == "summary"
        previous = None
        for run in block.get("runs", []):
            text = run.get("text", "")
            names = run.get("classes", [])
            # The page sets these with normal white-space: a newline inside a
            # text node is a space, and only a <br> breaks the line.
            if (run.get("tags") or [""])[-1] != "br":
                text = WHITESPACE.sub(" ", text)
            if "verse-num" in names:
                text = text.translate(SUPERSCRIPT)
            if heading and previous is not None:
                if "proper-ref" in names and "citation-numbering" not in names and "proper-ref" not in previous:
                    ink("   ")
                elif "citation-numbering" in names and "citation-numbering" not in previous:
                    ink("  · ")
                elif "proper-form" in names and "proper-form" not in previous:
                    ink(" — ")
            if "composed-label" in names:
                ink.line(text, _run_style(names, run.get("tags", [])))
                previous = names
                continue
            if "citation-numbering" in names and not heading and previous is not None \
                    and "citation-numbering" not in previous:
                ink("  · ")
            if "citation-recast" in names and previous is not None and "citation-recast" not in previous:
                ink("  ")
            style = _run_style(names, run.get("tags", []))
            if heading and "proper-name" in names and not ({"proper-ref", "proper-form", "citation-numbering"} & set(names)):
                style = f"bold {accent}"
            elif heading and not style:
                style = "bold underline" if block.get("tag") == "summary" else "bold"
            ink(text, style)
            previous = names
        ink.line()
    return ink


def absence_label(ordinary: dict | None, key: str | None) -> str | None:
    """The Ordinary's own label for an absence it declares, by its key."""
    if not ordinary or not key:
        return None
    for row in ordinary.get("absences") or []:
        if row.get("key") == key and row.get("label"):
            return row["label"]
    return None


WHITESPACE = re.compile(r"\s+")

CUES = {"priest": "Priest", "server": "Server", "all": "All", "people": "People", "deacon": "Deacon"}
ROLES = {"versicle": "℣", "response": "℟"}


def ordinary_element(ink: Ink, event: dict, ordinary: dict | None, *, rubrics: bool = True) -> Ink:
    """One element of the Ordinary, set as what its kind says it is. Never a blank."""
    element = event.get("element") or {}
    text = event.get("text") or {}
    kind = element.get("kind") or ""
    if kind == "rubric" and not rubrics:
        return ink
    words = text.get("text")
    named = element.get("name") or element.get("latin_incipit")
    if kind == "heading":
        if words:
            ink.line(str(words).strip(), "bold underline")
        return ink
    if named and kind in SPOKEN:
        ink(str(named), "bold")
        if element.get("speaker"):
            ink(f"  ({element['speaker']})", "$text-muted")
        ink.line()
    if words:
        if kind == "rubric":
            ink.line(f"[ {' '.join(str(words).split())} ]", "italic $rubric")
            return ink
        turns = text.get("turns") or []
        if turns and kind in SPOKEN:
            for turn in turns:
                said = str(turn.get("text") or "")
                if turn.get("gloss") is True:
                    ink.line(f"[ Source translation: {said} ]", "italic $text-muted")
                    continue
                if turn.get("action") is True:
                    if rubrics:
                        ink.line(f"[ {said} ]", "italic $rubric")
                    continue
                speaker = CUES.get(turn.get("speaker") or "")
                role = ROLES.get(turn.get("dialogue_role") or "")
                marker = turn.get("printed_marker")
                if (role or speaker) and marker and said.startswith(marker + " "):
                    said = said[len(marker) + 1:]
                if role:
                    ink(role + " ", "bold $rubric")
                if speaker:
                    ink(speaker + ": ", "$text-muted")
                ink.line(said)
        else:
            ink.line(str(words).strip())
        return ink
    # Absent: the element's own recorded reason, by the side of the book it names.
    if not named:
        ink.line(f"[{kind or 'element'}]", "$text-muted")
    language = text.get("language") or ""
    reason = absence_label(ordinary, text.get("absenceKey")) or \
        ((element.get("absent") or {}).get(absence_side(language)) if language else None)
    availability = text.get("availability")
    if availability == "choice-required":
        ink.line("Several witnesses hold this text; choose one before reading it.", "italic $warning")
    else:
        ink.line(f"[absent: {reason or 'not held'}]", "italic $warning")
    if element.get("latin_incipit") and element.get("latin_incipit") != element.get("name"):
        ink.line(f"opens {element['latin_incipit']}", "italic $text-muted")
    return ink


def seat_note(event: dict) -> str | None:
    seat = event.get("seat") or {}
    if seat.get("placement") == "unseated" and seat.get("region") in ("before-frame", "after-frame"):
        position = "before" if seat["region"] == "before-frame" else "after"
        # propers-events.js:118 / day-reader.js:1866
        return ("Exceptional source placement: the source assigns this Proper " + position +
                " the ordinary Mass frame. It remains here in source order; no Ordinary seat is invented.")
    return None


def events(ink: Ink, view: dict, *, rubrics: bool = True, accent: str = "$primary") -> Ink:
    """Every event of a reading, in the order the reader state gives them."""
    ordinary = view.get("ordinary")
    for event in view.get("events") or []:
        kind = event.get("kind")
        if kind == "ordinary-section":
            ink.line()
            ink.line(f"── {event.get('name') or ''} ", f"bold {accent}")
            continue
        if kind == "ordinary-element":
            ink.line()
            ordinary_element(ink, event, ordinary, rubrics=rubrics)
            continue
        ink.line()
        if kind == "proper":
            note = seat_note(event)
            if event.get("placeholder"):
                ink.line(f"{event.get('slot') or 'Proper'}: a placeholder; this Mass's text is not yet transcribed.",
                         "italic $warning")
                continue
            if event.get("problem"):
                ink.line(event["problem"], "bold $error")
                continue
            blocks(ink, event.get("blocks") or [], accent=accent)
            if note:
                ink.line(note, "italic $warning")
        elif kind == "proper-choice":
            # As source-choice-controls.js sets it: title, note, basis, then each option.
            ink.line(event.get("title") or "Source Proper choice", f"bold {accent}")
            if event.get("note"):
                ink.line(event["note"], "italic $warning")
            if event.get("basis"):
                ink.line(f"Source basis: {event['basis']}", "italic $text-muted")
            selection = event.get("selection") or {}
            options = list(event.get("options") or [])
            chosen = selection.get("option")
            options.sort(key=lambda one: one.get("id") != chosen)  # the selected one first, as the page shows it
            for option in options:
                mark = "▶" if option.get("id") == chosen else "▷"
                ink(f"{mark} {option.get('label') or option.get('id')}", "bold")
                if option.get("unavailable"):
                    ink(" — unavailable for this context", "italic $text-muted")
                ink.line()
                for member in option.get("members") or []:
                    blocks(ink, member.get("blocks") or [], accent=accent)
        else:
            ink.line(f"[{kind}]", "$text-muted")
    return ink


def option_label(choice: dict, option: dict, view: dict) -> str:
    """An open option by the name the data gives it, else by its id."""
    ident = option.get("id") or ""
    kind = choice.get("id") or ""
    if kind == "calendar-formulary":
        for branch in (view.get("day") or {}).get("branches") or []:
            for row in branch.get("readable") or []:
                if row.get("key") == ident and row.get("label"):
                    return row["label"]
    if kind.startswith("proper-form"):
        for form in (view.get("mass") or {}).get("forms") or []:
            if form.get("id") == ident and form.get("name"):
                return form["name"]
    return ident.replace("-", " ")


def choice_label(event: dict, option: dict) -> str:
    """A source proper choice's option, by the page's name for it."""
    return f"{event.get('title') or 'Source Proper choice'}  →  {option.get('label') or option.get('id')}"


def choices(ink: Ink, view: dict) -> Ink:
    """What the reader state left open, said as open."""
    for choice in view.get("unresolvedChoices") or []:
        ink.line(f"⑂ {choice.get('reason') or choice.get('id')}", "bold $warning")
        for number, option in enumerate(choice.get("options") or [], 1):
            ink(f"   {number}. ", "bold")(option_label(choice, option, view))
            ink(f"   {option.get('id')}", "$text-muted").line()
        ink.line("   Press s to choose. Nothing is selected for you by order.", "italic $text-muted")
    for event in view.get("events") or []:
        selected = event.get("selected") or {}
        if selected.get("kind") == "cycle-alternatives" and selected.get("availability") == "choice-required":
            ink.line(f"⑂ {event.get('slot') or 'A Proper'}: several cycles are held. They remain separate below "
                     "until one is chosen (press s).", "bold $warning")
            break
    return ink
