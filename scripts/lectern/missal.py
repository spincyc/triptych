"""Setting a reading of the Missal in the terminal.

What a proper says is written by the browser's own renderer and arrives here as
blocks of runs, each run carrying the class names the page gave it; this
module only decides how a class looks. Ordinary words and cues come from that
same browser owner; a rubric is bracketed and a heading set as a heading.
Nothing is chosen here that the reader state left open.
"""
from __future__ import annotations

import re

from textual.content import Content

from .widgets import SUPERSCRIPT, Ink

_SAFE_URL = re.compile(r"https?://[^\s\"'<>\\]+")
_SOURCE_ID_RE = re.compile(r"\b(?:edition|artifact|passage)\.[a-z0-9_.-]+\b", re.IGNORECASE)
_COMPLETE_COVERAGE_RE = re.compile(
    r"(\d+)/(\d+)\s+represented texts,\s*(\d+)/(\d+)\s+uses available"
)
_COMPLETE_OF_RE = re.compile(r"(\d+)\s+of\s+(\d+)\s+(represented texts|uses)\b")
_INCOMPLETE_MARKERS = (
    "unavailable",
    "incomplete",
    "not yet",
    "missing",
    "withheld",
    "unresolved",
    "uncollated",
    "recension",
    "differs",
    "departs",
    "departure",
    "does not hold",
    "partial",
    "restricted",
)
_RAW_AUDIT_JSON_RE = re.compile(r"\[\s*\{\s*\"source_word_1_based\".*?\}\s*\]", re.DOTALL)
_RAW_AUDIT_SENTENCE_RE = re.compile(
    r"(?:No donor fanout is performed[^.]*\.\s*"
    r"|[^.]*?\bSHA-?256\s+[0-9a-fA-F]{12,}[^.]*\.\s*"
    r"|[^.]*?wraps and final LF[^.]*\.\s*)",
    re.IGNORECASE,
)

# Blocks carrying these classes are metadata, credits, headings, or statutory
# notices — never rubric prose — even when nested under an `is-rubric` element.
_NON_RUBRIC_CLASSES = frozenset({
    "text-side-label",
    "composed-note",
    "ordinary-reading-note",
    "ordinary-reading-source",
    "ordinary-grant",
    "latin-rights-qualification",
    "ordinary-head",
    "proper-incipit",
    "notice",
    "unit-absence",
    "translation-credit",
    "translation-qualification",
    "translation-apparatus",
    "published-prayer-link",
})

# Run classes, most specific first, and the look each is given.
RUN_STYLES = (
    ("verse-num", "bold $accent"),
    ("vr-glyph", "bold $rubric"),
    ("cue-mark", "bold $rubric"),
    ("speaker-tag", "bold $text-muted"),
    ("ordinary-locus", "$text-muted"),
    ("ordinary-head", "bold underline"),
    ("ordinary-head-rubric", "italic $rubric"),
    # A priority-6 qualified-public-domain notice is a rights marking, not a
    # rubric and not a muted aside: keep it legible in calm secondary warning.
    ("latin-rights-qualification", "italic $warning"),
    ("ordinary-grant", "italic $text-muted"),
    ("ordinary-reading-source", "italic $text-muted"),
    ("ordinary-reading-note", "italic $text-muted"),
    ("text-side-lang", "bold $text-muted"),
    ("text-side-relation", "$text-muted"),
    ("text-side-meta", "italic $text-muted"),
    ("text-side-label", "bold $text-muted"),
    ("composed-note", "italic $text-muted"),
    ("unit-absence", "italic $warning"),
    ("notice", "italic $warning"),
    ("published-prayer-link", "underline $primary"),
    ("study-source-link", "underline $sources-color"),
    ("inline-rubric", "italic $rubric"),
    ("elision", "$text-muted"),
    ("citation-numbering", "$text-muted"),
    ("citation-recast", "italic $text-muted"),
    ("proper-ref", "bold"),
    ("proper-form", "italic"),
    ("composed-label", "italic $text-muted"),
    ("unit-claim", "italic $text-muted"),
    ("uncompiled-mark", "bold $warning"),
    ("uncompiled", "italic $warning"),
    ("chapter-mark", "bold $text-muted"),
    ("citation-ref", "bold"),
    ("cycle-name", "bold underline"),
    ("proper-incipit", "italic"),
    ("proper-name", "bold $primary"),
    ("compare-status", "italic $warning"),
    ("compare-evidence", "$text-muted"),
    ("compare-anchor", "$text-muted"),
    ("compare-calendar-relation", "italic"),
    ("compare-calendar-name", "bold"),
    ("reasoning-locus", "italic $accent"),
    ("reasoning-latin", "italic"),
    ("reasoning-lead", ""),
    ("is-rubric", "italic $rubric"),
)

WHITESPACE = re.compile(r"\s+")
_RAW_URL_RE = re.compile(r",?\s*https?://\S+")


def humanize_slug(raw: str) -> str:
    """Turn an internal slash/hyphen identifier into readable prose."""
    tail = str(raw or "").rstrip("/").split("/")[-1]
    words = tail.replace("_", " ").replace("-", " ").strip()
    if not words:
        return str(raw or "")
    return words[0].upper() + words[1:]


def format_coverage_notice(notice: str) -> str:
    """Omit redundant N/N ratios once a missal/language holds all represented texts."""
    if not notice:
        return ""

    def _replace_pair(match: re.Match[str]) -> str:
        a, b, c, d = (int(match.group(i)) for i in range(1, 5))
        if b > 0 and a >= b and d > 0 and c >= d:
            return "all represented texts available"
        return match.group(0)

    def _replace_of(match: re.Match[str]) -> str:
        a, b, noun = int(match.group(1)), int(match.group(2)), match.group(3)
        if b > 0 and a >= b:
            return f"all {noun}"
        return match.group(0)

    cleaned = _COMPLETE_COVERAGE_RE.sub(_replace_pair, notice)
    cleaned = _COMPLETE_OF_RE.sub(_replace_of, cleaned)
    return cleaned


def is_complete_notice(notice: str, *, recension: str | None = None) -> bool:
    """True when a coverage notice reports routine complete availability with no caveats."""
    if recension:
        return False
    if not notice:
        return True
    lower = notice.lower()
    if any(marker in lower for marker in _INCOMPLETE_MARKERS):
        return False
    for match in re.finditer(r"(\d+)/(\d+)", notice):
        if int(match.group(1)) < int(match.group(2)):
            return False
    for match in re.finditer(r"(\d+)\s+of\s+(\d+)", notice):
        if int(match.group(1)) < int(match.group(2)):
            return False
    return True


def is_contents_event(event: dict) -> bool:
    """Filter minor rubric-only Ordinary elements out of Contents while keeping landmarks."""
    if event.get("kind") != "ordinary-element":
        return True
    element = event.get("element") or {}
    if element.get("kind") == "rubric":
        return False
    if element.get("kind") == "heading" and not element.get("name"):
        return False
    return True


def event_label(event: dict, *, indent_children: bool = False) -> str:
    """Derive a human title for any event; never leak raw ordinary-element/... IDs."""
    kind = event.get("kind")
    if kind == "ordinary-section":
        return event.get("name") or humanize_slug(event.get("id") or "")
    prefix = "  " if indent_children else ""
    if kind in ("proper", "proper-choice", "january-prayer"):
        name = event.get("slot") or event.get("title") or event.get("name") or humanize_slug(event.get("id") or "")
        return prefix + name
    if kind == "ordinary-element":
        element = event.get("element") or {}
        name = element.get("name") or element.get("latin_incipit")
        if not name:
            for block in event.get("blocks") or []:
                bclasses = set(block.get("classes") or [])
                if bclasses & {"text-side-label", "composed-note", "ordinary-reading-note",
                               "ordinary-reading-source", "latin-rights-qualification", "ordinary-grant"}:
                    continue
                line = WHITESPACE.sub(" ", "".join(r.get("text", "") for r in block.get("runs") or [])).strip()
                if line:
                    name = line if len(line) <= 46 else line[:45] + "…"
                    break
        return prefix + (name or humanize_slug(element.get("key") or event.get("id") or ""))
    return prefix + (event.get("slot") or event.get("name") or humanize_slug(event.get("id") or ""))


def _run_style(classes: list[str], tags: list[str], *, ordinary_element: bool = False) -> str:
    if ordinary_element and "proper-ref" in classes:
        return "$text-muted"
    for name, style in RUN_STYLES:
        if name in classes:
            if name == "is-rubric" and (_NON_RUBRIC_CLASSES & set(classes)):
                continue
            return style
    if "strong" in tags or "b" in tags:
        return "bold"
    if "em" in tags or "i" in tags:
        return "italic"
    return ""


def _render_pair_columns(ink: Ink, left_blocks: list[dict], right_blocks: list[dict], *,
                         pair_width: int, accent: str, missal_mode: bool,
                         seen_notes: set[str] | None) -> None:
    col_w = max(32, (pair_width - 3) // 2)
    left_ink = blocks(Ink(), left_blocks, accent=accent, missal_mode=missal_mode,
                      seen_notes=seen_notes, pair_width=0)
    right_ink = blocks(Ink(), right_blocks, accent=accent, missal_mode=missal_mode,
                       seen_notes=seen_notes, pair_width=0)
    left_lines = left_ink.content().wrap(col_w) if left_ink else []
    right_lines = right_ink.content().wrap(col_w) if right_ink else []
    while left_lines and not left_lines[-1].plain.strip():
        left_lines.pop()
    while right_lines and not right_lines[-1].plain.strip():
        right_lines.pop()
    total = max(len(left_lines), len(right_lines))
    for i in range(total):
        left = left_lines[i] if i < len(left_lines) else Content("")
        right = right_lines[i] if i < len(right_lines) else Content("")
        pad = max(0, col_w - left.cell_length)
        ink.parts.append(Content.assemble(left, " " * pad, (" │ ", "$rule"), right, "\n"))


def _block_plain(block: dict) -> str:
    return WHITESPACE.sub(" ", "".join(r.get("text", "") for r in block.get("runs") or [])).strip()


def _render_block_runs(ink: Ink, block: dict, *, accent: str, missal_mode: bool,
                       action: bool = False, gloss: bool = False, rubric: bool = False,
                       heading: bool = False) -> None:
    block_classes = set(block.get("classes") or [])
    is_ordinary_el = "ordinary-element" in block_classes
    previous = None
    linked_prayer_hint_added = False
    for run in block.get("runs", []):
        text = run.get("text", "")
        names = run.get("classes", [])
        if (run.get("tags") or [""])[-1] != "br":
            text = WHITESPACE.sub(" ", text)
        if "verse-num" in names:
            text = text.translate(SUPERSCRIPT)
        # A declared priest cue is distinct from a versicle. Keep the
        # browser's source-defined marks and give each a clean aligned gutter.
        cue = "vr-glyph" in names or "cue-mark" in names
        stripped = text.strip()
        if "speaker-tag" in names and "is-priest" in names and stripped == "Priest":
            cue, text, stripped = True, "P", "P"
        elif "speaker-tag" in names and stripped in ("All", "All."):
            cue, text, stripped = True, "All", "All"
        if cue:
            gap = " " if len(stripped) >= 3 else "  "
            ink(stripped + gap, "bold $rubric")
            previous = ["reading-cue"]
            continue
        if previous == ["reading-cue"]:
            text = text.lstrip(" ")
        if heading and previous is not None and "ordinary-locus" in names and "ordinary-locus" not in previous:
            ink("  ")
        if heading and previous is not None:
            if "proper-ref" in names and "citation-numbering" not in names and "proper-ref" not in previous:
                ink("   ")
            elif "citation-numbering" in names and "citation-numbering" not in previous:
                ink("  · ")
            elif "proper-form" in names and "proper-form" not in previous:
                ink(" — ")
        if "composed-label" in names:
            label, separator, language = text.partition(" · ")
            if label == "Composed text — not scripture":
                if separator and language.strip():
                    ink.line(language, _run_style(names, run.get("tags", []), ordinary_element=is_ordinary_el))
                previous = names
                continue
            ink.line(text, _run_style(names, run.get("tags", []), ordinary_element=is_ordinary_el))
            previous = names
            continue
        if "citation-numbering" in names and not heading and previous is not None \
                and "citation-numbering" not in previous:
            ink("  · ")
        if "citation-recast" in names and previous is not None and "citation-recast" not in previous:
            ink("  ")
        style = _run_style(names, run.get("tags", []), ordinary_element=is_ordinary_el)
        if action or gloss:
            style = "italic $text-muted" if gloss else "italic $rubric"
        elif rubric and not style:
            style = "italic $rubric"
        if heading and "proper-name" in names and not ({"proper-ref", "proper-form", "citation-numbering", "ordinary-locus"} & set(names)):
            style = "italic $rubric" if ("is-rubric" in block_classes) else f"bold {accent}"
        elif heading and not style:
            style = "bold underline" if block.get("tag") == "summary" else "bold"
        href = run.get("href") or ""
        if href:
            if _SAFE_URL.fullmatch(href):
                base = style or accent
                style = f'underline {accent} link="{href}"' if "underline" not in base else f'{base} link="{href}"'
            elif href.startswith("../sources/#"):
                style = "underline $sources-color"
        ink(text, style)
        if href and _SAFE_URL.fullmatch(href) and ("published-prayer-link" in names or "a" in (run.get("tags") or [])):
            if not linked_prayer_hint_added and not block_classes & {"study-facts", "study-event"}:
                ink("  [Ctrl+O]", "$text-muted")
                linked_prayer_hint_added = True
        previous = names


def blocks(ink: Ink, items: list[dict], *, accent: str = "$primary", missal_mode: bool = False,
           pair_width: int = 0, seen_notes: set[str] | None = None,
           dl_label_width: int = 22) -> Ink:
    """The page's blocks, one line group each, styled by the classes they carry."""
    if missal_mode and seen_notes is None:
        seen_notes = getattr(ink, "_seen_notes", None)
        if seen_notes is None:
            seen_notes = set()
            setattr(ink, "_seen_notes", seen_notes)
    previous_block: list[str] = []
    idx = 0
    total = len(items)
    while idx < total:
        block = items[idx]
        # Side-by-side bilingual pair on wide terminals (>=110 cols -> pair_width >= 80).
        pair_id = block.get("pair")
        if pair_id is not None and pair_width >= 80:
            group = []
            while idx < total and items[idx].get("pair") == pair_id:
                group.append(items[idx])
                idx += 1
            left_blocks = [b for b in group if b.get("side") == 0]
            right_blocks = [b for b in group if b.get("side") == 1]
            if left_blocks and right_blocks:
                _render_pair_columns(ink, left_blocks, right_blocks,
                                     pair_width=pair_width, accent=accent,
                                     missal_mode=missal_mode, seen_notes=seen_notes)
                previous_block = group[-1].get("classes", [])
                continue
            # Fallback if only one side is present: render sequentially.
            blocks(ink, group, accent=accent, missal_mode=missal_mode,
                   pair_width=0, seen_notes=seen_notes, dl_label_width=dl_label_width)
            previous_block = group[-1].get("classes", [])
            continue

        # Crisp 2-column key-value rows for <dl><dt><dd> pairs (Study apparatus).
        if block.get("tag") == "dt" and idx + 1 < total and items[idx + 1].get("tag") == "dd":
            key_text = _block_plain(block)
            dd_block = items[idx + 1]
            val_text = _block_plain(dd_block)
            # Collapse duplicate consecutive "Unavailable state: unavailable" after "Availability reason: unavailable".
            if (key_text == "Unavailable state" and val_text == "unavailable" and
                    idx >= 2 and items[idx - 2].get("tag") == "dt" and
                    _block_plain(items[idx - 2]) == "Availability reason" and
                    _block_plain(items[idx - 1]) == "unavailable"):
                idx += 2
                continue
            padded_key = (key_text + "  ").ljust(dl_label_width + 2) if len(key_text) <= dl_label_width else key_text + "  "
            ink(padded_key, "bold $text-muted")
            _render_block_runs(ink, dd_block, accent=accent, missal_mode=missal_mode)
            ink.line()
            previous_block = dd_block.get("classes", [])
            idx += 2
            continue

        idx += 1
        names = block.get("classes", [])
        name_set = set(names)
        if missal_mode and "translation-apparatus-closed" in name_set:
            # The disclosure itself is opened by Study. Adjacent credits, rights
            # qualifications and warnings still accompany their text.
            continue
        # Deduplicate repeated identical base Ordinary witness credits/notes in
        # Missal mode while preserving the first occurrence, every distinct
        # witness, and every statutory priority-6/grant notice verbatim.
        if missal_mode and seen_notes is not None and (name_set & {"ordinary-reading-source", "ordinary-reading-note"}):
            note_key = _block_plain(block)
            if note_key in seen_notes:
                continue
            seen_notes.add(note_key)
        if (("stanza" in name_set and "stanza" in previous_block) or
                ("passage" in name_set and "passage" in previous_block) or
                ("text-side-label" in name_set and previous_block and "text-side-label" not in previous_block and "text-side" in previous_block)):
            ink.line()
        heading = block.get("tag", "").startswith("h") or block.get("tag") == "summary"
        action = "is-action" in name_set or "source-local-actor-action" in name_set
        gloss = "is-gloss" in name_set
        rubric = (
            "ordinary-head-rubric" in name_set
            or ("is-rubric" in name_set and not heading and not (name_set & _NON_RUBRIC_CLASSES))
        )
        if action or gloss or rubric:
            ink("[ Source translation: " if gloss else "[ ",
                "italic $text-muted" if gloss else "italic $rubric")
        _render_block_runs(ink, block, accent=accent, missal_mode=missal_mode,
                           action=action, gloss=gloss, rubric=rubric, heading=heading)
        if action or gloss or rubric:
            ink(" ]", "italic $text-muted" if gloss else "italic $rubric")
        if {"translation-apparatus-closed", "source-local-actor-quotation-closed"} & name_set:
            ink("  (d Study)", "$text-muted")
        ink.line()
        previous_block = names
    return ink


def ordinary_element(ink: Ink, event: dict, ordinary: dict | None, *, rubrics: bool = True,
                     accent: str = "$primary", pair_width: int = 0,
                     seen_notes: set[str] | None = None) -> Ink:
    """The browser's Ordinary element, including its exact absences and grants."""
    element = event.get("element") or {}
    if element.get("kind") == "rubric" and not rubrics:
        return ink
    if "blocks" not in event:
        raise ValueError("Ordinary elements must be set by the shared browser renderer")
    filtered = [block for block in event["blocks"]
                if rubrics or ("is-action" not in block.get("classes", [])
                               and "ordinary-head-rubric" not in block.get("classes", []))]
    return blocks(ink, filtered, accent=accent, missal_mode=True,
                  pair_width=pair_width, seen_notes=seen_notes)


def seat_note(event: dict) -> str | None:
    seat = event.get("seat") or {}
    if seat.get("placement") == "unseated" and seat.get("region") in ("before-frame", "after-frame"):
        position = "before" if seat["region"] == "before-frame" else "after"
        # propers-events.js:118 / day-reader.js:1866
        return ("Exceptional source placement: the source assigns this Proper " + position +
                " the ordinary Mass frame. It remains here in source order; no Ordinary seat is invented.")
    return None


def events(ink: Ink, view: dict, *, rubrics: bool = True, accent: str = "$primary",
           pair_width: int = 0, seen_notes: set[str] | None = None,
           leading_blank: bool = True) -> Ink:
    """Every event of a reading, in the order the reader state gives them."""
    ordinary = view.get("ordinary")
    missal_mode = bool((view.get("state") or {}).get("ordinary"))
    rule_width = max(54, pair_width or 72)
    for index, event in enumerate(view.get("events") or []):
        kind = event.get("kind")
        if kind == "ordinary-section":
            if leading_blank or index > 0:
                ink.line()
            name = event.get("name") or humanize_slug(event.get("id") or "")
            tail = "─" * max(4, rule_width - len(name) - 4)
            ink("── ", "$rule")(name, f"bold {accent}").line(f" {tail}", "$rule")
            continue
        if kind == "ordinary-element":
            if not rubrics and (event.get("element") or {}).get("kind") == "rubric":
                continue
            if leading_blank or index > 0:
                ink.line()
            ordinary_element(ink, event, ordinary, rubrics=rubrics, accent=accent,
                             pair_width=pair_width, seen_notes=seen_notes)
            continue
        if leading_blank or index > 0:
            ink.line()
        if kind == "january-prayer":
            blocks(ink, event.get("blocks") or [], accent=accent, missal_mode=missal_mode,
                   pair_width=pair_width, seen_notes=seen_notes)
            continue
        if kind == "proper":
            note = seat_note(event)
            if event.get("placeholder"):
                ink.line(f"{event.get('slot') or 'Proper'}: a placeholder; this Mass's text is not yet transcribed.",
                         "italic $warning")
                continue
            if event.get("problem"):
                ink.line(event["problem"], "bold $error")
                continue
            blocks(ink, event.get("blocks") or [], accent=accent, missal_mode=missal_mode,
                   pair_width=pair_width, seen_notes=seen_notes)
            if note:
                ink.line(note, "italic $warning")
        elif kind == "proper-choice":
            # A Missal follows the elected option. Read keeps the alternative texts for comparison.
            ink.line(event.get("title") or "Source Proper choice", f"bold {accent}")
            if event.get("note") and not missal_mode:
                ink.line(event["note"], "italic $warning")
            if event.get("basis") and not missal_mode:
                ink.line(f"Source basis: {event['basis']}", "italic $text-muted")
            selection = event.get("selection") or {}
            options = list(event.get("options") or [])
            chosen = selection.get("option")
            if missal_mode and not chosen:
                ink.line("Choose a reading with s.", "$text-muted")
            if missal_mode and chosen:
                options = [option for option in options if option.get("id") == chosen]
            else:
                options.sort(key=lambda one: one.get("id") != chosen)
            for option in options:
                mark = "▶" if option.get("id") == chosen else "▷"
                ink(f"{mark} {option.get('label') or option.get('id')}", "bold")
                if option.get("unavailable"):
                    ink(" — unavailable for this context", "italic $text-muted")
                ink.line()
                if missal_mode and not chosen:
                    continue
                for member in option.get("members") or []:
                    blocks(ink, member.get("blocks") or [], accent=accent, missal_mode=missal_mode,
                           pair_width=pair_width, seen_notes=seen_notes)
        else:
            ink.line(f"[{kind}]", "$text-muted")
    return ink


def option_label(choice: dict, option: dict, view: dict) -> str:
    """An open option by the name the data gives it, else cleanly humanized."""
    ident = option.get("id") or ""
    kind = choice.get("id") or ""
    if kind in ("calendar-formulary", "calendar-reading"):
        for branch in (view.get("day") or {}).get("branches") or []:
            for row in branch.get("readable") or []:
                if row.get("key") == ident and row.get("label"):
                    return row["label"]
    if kind.startswith("proper-form"):
        for form in (view.get("mass") or {}).get("forms") or []:
            if form.get("id") == ident and form.get("name"):
                return form["name"]
    if ident == "pray":
        return "Pray (optional)"
    if ident == "omit":
        return "Omit"
    return ident.replace("-", " ").capitalize() if ident else ""


def choice_label(event: dict, option: dict) -> str:
    """A source proper choice's option, by the page's name for it."""
    opt_id = option.get("id") or ""
    opt_name = "Pray (optional)" if opt_id == "pray" else ("Omit" if opt_id == "omit" else (option.get("label") or opt_id))
    return f"{event.get('title') or 'Source Proper choice'}  →  {opt_name}"


def clean_choice_reason(choice: dict, view: dict) -> str:
    """Humanize a choice prompt: prefix proper-choice titles and move raw URLs out."""
    ident = str(choice.get("id") or "")
    reason = str(choice.get("reason") or ident)
    reason = _RAW_URL_RE.sub("", reason).replace(" ,", ",").strip()
    if ident.startswith("proper-choice/"):
        event = next((e for e in view.get("events") or [] if e.get("id") == ident), None)
        title = (event or {}).get("title") or humanize_slug(ident)
        if title and title.lower() not in reason.lower():
            return f"{title}: {reason}"
    return reason


def event_source_readings(event: dict):
    for link in event.get("sourceConsultations") or []:
        yield event["slot"], link
    selected = (event.get("selection") or {}).get("option")
    for option in event.get("options") or []:
        if selected and option["id"] != selected:
            continue
        for member in option.get("members") or []:
            for link in member.get("sourceConsultations") or []:
                yield f"{option['label']} · {member['slot']}", link


def witness_readings(view: dict):
    name = (view.get("mass") or {}).get("name") or ""
    for link in view.get("missalWitnessLinks") or []:
        yield name, link
    prayer_owner = view.get("orationSelection") or {}
    for link in view.get("orationWitnessLinks") or []:
        yield "Prayers from " + prayer_owner["label"], link
    for link in view.get("ordinaryWitnessLinks") or []:
        yield "Ordinary", link


def witness_label(link: dict) -> str:
    languages = {"la": "Latin", "en": "English"}
    language = " and ".join(languages[code] for code in link.get("languages") or [link["language"]])
    extent = {"section": "section", "form": "selected form", "ordinary": "Ordinary"}[link["scope"]]
    return f"{language} · {link['edition_label']} · {extent}"


def source_rights(status: str | None) -> str:
    if not status:
        return ""
    friendly = {
        "restricted": "Restricted rights · consult at the publisher.",
        "unresolved": "Rights status not yet settled for this scan.",
        "public-domain": "Public domain",
        "qualified-public-domain": "Qualified public domain",
    }
    return friendly.get(status, "Source rights · " + status.replace("-", " "))


def memorial_sources(view: dict) -> dict:
    if view.get("primaryDayChoice"):
        return {}
    return (view.get("mass") or {}).get("memorialPrayerSources") or {}


def source_witness(ink: Ink, view: dict, *, detail: bool = False) -> None:
    links = list(witness_readings(view))
    opening = next((link for _, link in links if link.get("rite_opening")), None)
    if opening and not detail:
        ink.line("Complete rite in facsimile", "bold").line(opening["locus"])
        url = opening["url"]
        ink.line(url, f'underline $primary link="{url}"').line()
    january = view.get("januarySelection")
    if january and detail:
        ink.line("January weekday prayers", "bold").line(january["label"] + " · " + january["phase"].replace("-", " "))
        ink.line(january["ruleLocus"]).line(january["ruleUrl"], f'underline $primary link="{january["ruleUrl"]}"').line()
    elif view.get("entrance") == "propers" and (view.get("mass") or {}).get("januaryWeekdays"):
        ink.line("Choose the weekday and Epiphany phase in Reading settings (,).", "$text-muted")
    memorial = memorial_sources(view)
    if memorial:
        if detail:
            ink.line("Memorial prayer sources", "bold").line(" · ".join(memorial["roles"]))
            ink.line("Choose each source independently in Reading settings. The memorial keeps its own Collect.")
            if memorial.get("current_feria"):
                feria = view.get("memorialFeria") or {}
                ink.line("Current feria" + (f" · {feria['name']}" if feria else ""))
            for group in memorial["groups"]:
                ink.line(group["label"]).line(" · ".join(group["form_ids"]), "$text-muted")
                if group.get("qualification"):
                    ink.line(group["qualification"], "italic $text-muted")
            ink.line(memorial["locus"]).line(memorial["source_id"], "$text-muted")
            ink.line(memorial["url"], f'underline $primary link="{memorial["url"]}"')
            ink.line(memorial["rule_source_id"], "$text-muted").line()
        else:
            ink.line("Offerings and Postcommunion sources (press , for Reading settings)", "$text-muted")
    if detail:
        for name, link in links:
            ink.line(name, "bold").line(witness_label(link)).line(link["locus"])
            if link.get("rights_status"):
                ink.line(source_rights(link["rights_status"]), "$text-muted")
            if link.get("source_id"):
                ink.line(link["source_id"], "$text-muted")
            url = link["url"]
            ink.line(url, f'underline $primary link="{url}"').line()
    elif links and not any(event.get("kind") in ("proper", "proper-choice") for event in view.get("events") or []):
        ink.line("Source texts (press , for Reading settings)", "$text-muted")


def ordinary_conditions(ink: Ink, view: dict, *, compact: bool = False) -> None:
    rows = view.get("ordinaryUnresolved") or []
    if compact:
        status = []
        coverage = view.get("coverage") or []
        frame = next((row for row in coverage if row.get("scope", "").startswith("ordinary-frame:")), {})
        if frame.get("state") == "unavailable":
            status.append("Specialized Ordinary unavailable")
        elif frame.get("state") == "absent":
            status.append("No Mass Ordinary for this rite")
        elif any(row.get("state") == "unavailable" for row in coverage):
            status.append("Some text unavailable")
        elif any(row.get("state") == "unsupported" or row.get("completeness") == "partial" for row in coverage):
            status.append("Partial coverage")
        if rows:
            noun = "condition" if len(rows) == 1 else "conditions"
            status.append(f"{len(rows)} unresolved Ordinary {noun}")
        if status:
            ink.line(" · ".join([*status, "d Study"]), "italic $warning")
        return
    for row in rows:
        subject = row["element"].split("/")[-1].replace("-", " ")
        condition = row.get("condition") or {}
        ink.line(f"{subject.capitalize()} · Ordinary condition unresolved", "bold $warning")
        if condition.get("basis"):
            ink.line(condition["basis"], "italic $text-muted")


def select_proper_option(selection: dict, row: dict, group: str, candidate: str) -> None:
    event = next(event for event in row["events"] if event["id"] == group)
    option = next(option for option in event["options"] if option["id"] == candidate)
    selection["properChoices"] = option["properChoices"].copy()
    selection.pop("alternative", None)
    if option["dropWitness"]:
        selection.pop("witness", None)


def choices(ink: Ink, view: dict) -> Ink:
    """What the reader state left open, said as open (without 1..8 hotkey collisions)."""
    open_choices = view.get("unresolvedChoices") or []
    if open_choices and (view.get("state") or {}).get("ordinary") and view.get("events") and not view.get("primaryDayChoice"):
        selectable = any(not str(choice.get("id") or "").startswith(("proper-condition/", "common-set:"))
                         for choice in open_choices)
        detail = "s Choose" if selectable else "d Study"
        noun = "choice" if len(open_choices) == 1 else "choices"
        ink.line(f"{len(open_choices)} unresolved source {noun} · {detail}", "bold $warning")
        return ink
    for choice in open_choices:
        ink.line(f"⑂ {clean_choice_reason(choice, view)}", "bold $warning")
        for option in choice.get("options") or []:
            ink("   • ", "bold")(option_label(choice, option, view)).line()
        if str(choice.get("id") or "").startswith(("proper-condition/", "common-set:")):
            ink.line("   This source condition remains unresolved; no selection is offered here.",
                     "italic $text-muted")
        else:
            ink.line("   Press s to choose. Nothing is selected for you by order.", "italic $text-muted")
    for event in view.get("events") or []:
        selected = event.get("selected") or {}
        if selected.get("kind") == "cycle-alternatives" and selected.get("availability") == "choice-required":
            ink.line(f"⑂ {event.get('slot') or 'A Proper'}: several cycles are held. They remain separate below "
                     "until one is chosen (press s).", "bold $warning")
            break
    return ink


def filter_study_audit(study_blocks: list[dict], *, show_audit: bool = False) -> list[dict]:
    """Keep Study scholarly by hiding raw JSON word maps and SHA-256 build hashes behind `a`."""
    if show_audit:
        return study_blocks
    cleaned = []
    for block in study_blocks:
        changed = False
        new_runs = []
        for run in block.get("runs") or []:
            text = run.get("text", "")
            updated = _RAW_AUDIT_JSON_RE.sub("[word-alignment audit hidden — press a]", text)
            updated = _RAW_AUDIT_SENTENCE_RE.sub("", updated)
            if updated != text:
                changed = True
                updated = re.sub(r"\s{2,}", " ", updated).strip()
                if updated:
                    new_runs.append({**run, "text": updated})
            else:
                new_runs.append(run)
        if changed:
            if new_runs:
                cleaned.append({**block, "runs": new_runs})
        else:
            cleaned.append(block)
    return cleaned


def split_study_blocks(study_blocks: list[dict]) -> tuple[list[dict], dict[str, list[dict]], list[dict]]:
    """Separate overview blocks, per-event unit blocks, and ordered unit blocks."""
    overview: list[dict] = []
    by_event: dict[str, list[dict]] = {}
    all_units: list[dict] = []
    for block in study_blocks:
        event_id = block.get("studyEventId") or ""
        if event_id:
            by_event.setdefault(event_id, []).append(block)
            all_units.append(block)
        else:
            overview.append(block)
    return overview, by_event, all_units


def extract_study_references(rows: list[dict], study_blocks: list[dict]) -> tuple[list[tuple[str, str]], list[str]]:
    """Collect deduplicated (label, URL) pairs and Source Library IDs for Study actions."""
    urls: list[tuple[str, str]] = []
    seen_urls: set[str] = set()
    source_ids: list[str] = []
    seen_ids: set[str] = set()

    def add_url(label: str, url: str | None) -> None:
        if url and _SAFE_URL.fullmatch(url) and url not in seen_urls:
            seen_urls.add(url)
            urls.append((f"{label} · {url}" if label else url, url))

    def add_id(ident: str | None) -> None:
        if ident and _SOURCE_ID_RE.fullmatch(ident) and ident not in seen_ids:
            seen_ids.add(ident)
            source_ids.append(ident)

    for row in rows:
        for name, link in witness_readings(row):
            add_url(f"{name} ({link.get('edition_label') or ''})".strip(), link.get("url"))
            add_id(link.get("source_id"))
        jan = row.get("januarySelection") or {}
        if jan.get("ruleUrl"):
            add_url("January rubric", jan["ruleUrl"])
        mem = memorial_sources(row)
        if mem:
            add_url("Memorial prayer sources", mem.get("url"))
            add_id(mem.get("source_id"))
            add_id(mem.get("rule_source_id"))
    for block in study_blocks:
        for run in block.get("runs") or []:
            href = run.get("href") or ""
            if _SAFE_URL.fullmatch(href):
                add_url(run.get("text", "").strip(), href)
            for match in _SOURCE_ID_RE.findall(run.get("text", "")):
                add_id(match)
    return urls, source_ids


def extract_scripture_citations(rows: list[dict], *, current_event_id: str | None = None) -> list[tuple[str, str]]:
    """Extract deduplicated (slot, ref) Scripture citations, current unit first."""
    found: list[tuple[str, str]] = []
    seen: set[str] = set()

    def add_event(event: dict) -> None:
        slot = event.get("slot") or "Scripture"
        for cite in event.get("citations") or []:
            ref = cite.get("ref") or ""
            if ref and ref not in seen:
                seen.add(ref)
                found.append((slot, ref))
        for option in event.get("options") or []:
            for member in option.get("members") or []:
                for cite in member.get("citations") or []:
                    ref = cite.get("ref") or ""
                    if ref and ref not in seen:
                        seen.add(ref)
                        found.append((member.get("slot") or slot, ref))

    if current_event_id:
        for row in rows:
            prefix = row.get("prefix") or ""
            for event in row.get("events") or []:
                if prefix + event["id"] == current_event_id:
                    add_event(event)
    for row in rows:
        for event in row.get("events") or []:
            add_event(event)
    return found
