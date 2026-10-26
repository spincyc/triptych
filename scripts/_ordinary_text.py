#!/usr/bin/env python3
"""How an Ordinary's elements are set in a terminal, once, for every tool.

Two tools print the Ordinary — `mass-ordinary show`, which prints the frame,
and `mass-today show --expanded`, which prints the day's propers inside it —
and until this module existed only the first had a renderer. It set every
element at one indent in one face, so this is what a reader saw:

        P. May they rest in peace. R. Amen.

        Bowing before the Altar, the Priest says

      Placeat tibi sancta Trinitas (priest)
        Let the performance of my homage be pleasing to thee, ...

        Turning himself towards the People, he gives them his Blessing, saying,

The two rubrics bracketing the Placeat read as its first and last lines. The
data is not at fault: each is its own element, correctly carrying `kind:
rubric`, and the browser sets `.ordinary-element.is-rubric` apart for exactly
this reason. It was the terminal that had never learned the distinction.

So an element is set as what its `kind` says it is, in every tier:

    heading   the book's own division, set as a heading
    rubric    an instruction, bracketed — never merely dimmed, because dim is
              a decoration a monochrome terminal does not have and the
              distinction between an action and a prayer is not decoration
    prayer    the words, set plainly
    form      the words, set plainly; it is a prayer with a sacramental effect
              and nothing about the setting should suggest a stage direction
    dialogue  the words, with V. and R. as glyphs where the stream carries them

WHAT IS NOT DECIDED HERE. Not rights — the generator has already dropped every
witness it may not publish and written the recorded reason on each element.
Structured fragments use only their reviewed speaker and dialogue_role; the
1861 book's P./R. speaker letters never create a role. A source translation
gloss is a separately named nonspoken note, and an action remains an action.
Only legacy opaque blocks still use the printed-mark formatter; no boundary
or new role is inferred here.
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _tooling import Style  # noqa: E402

WIDTH = 88

# Which kinds are words that are said. Everything else is printed matter about
# the Mass rather than words of it, and is set apart.
SPOKEN = ("prayer", "form", "dialogue")


def wrap(text: str, indent: str, width: int = WIDTH) -> list[str]:
    out: list[str] = []
    for paragraph in str(text).strip().split("\n\n"):
        block = " ".join(paragraph.split())
        if block:
            out.extend(textwrap.wrap(block, max(20, width - len(indent))))
            out.append("")
    return [indent + line if line else "" for line in (out[:-1] or out)]


def absence_side(lang: str) -> str:
    """The key an element's `absent` block names this language's reason under.

    The block is keyed by the side of the book — `english`, `latin` — and not
    by ISO code. Reading it by code found nothing and fell through to the
    English reason, so `--lang la` once reported the postconciliar Latin
    withheld under ICEL: a real reason, for the other text, printed under this
    one.
    """
    return {"en": "english", "la": "latin"}.get(lang, lang)


def translation_applicability(translation: dict, context: dict | None = None) -> str:
    """Source heldness does not authorize executing a scoped language body."""
    if "applicability" not in translation:
        return "applicable"
    scope = translation["applicability"]
    import re
    identifier = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    if (not isinstance(scope, dict) or set(scope) != {"kind", "calendar", "formularies", "basis"}
            or scope.get("kind") != "formulary"
            or not isinstance(scope.get("calendar"), str) or not identifier.fullmatch(scope["calendar"])
            or not isinstance(scope.get("basis"), str) or not scope["basis"].strip()
            or not isinstance(scope.get("formularies"), list) or not scope["formularies"]
            or any(not isinstance(one, str) or not identifier.fullmatch(one) for one in scope["formularies"])
            or len(scope["formularies"]) != len(set(scope["formularies"]))):
        raise ValueError("malformed Ordinary translation applicability")
    if (not isinstance(context, dict) or set(context) != {"calendar", "formulary"}
            or any(not isinstance(context.get(key), str) or not identifier.fullmatch(context[key])
                   for key in ("calendar", "formulary"))):
        return "unresolved"
    return ("applicable" if context["calendar"] == scope["calendar"]
            and context["formulary"] in scope["formularies"] else "inapplicable")


def element_lines(
    element: dict,
    lang: str,
    style: Style,
    *,
    indent: str = "  ",
    show_rubrics: bool = True,
    why: bool = False,
    context: dict | None = None,
) -> list[str]:
    """One element of the Ordinary, set as what it is. Never a blank.

    `show_rubrics` HIDES a rubric; it does not remove it from anything. The
    caller has already seated the day's propers against the elements, and the
    slots anchor to rubrics — the Introit is seated after
    `rubrica-benedictio-incensi-et-introitus` — so filtering them out before
    seating would unseat the propers and pour the Mass out in a plausible
    wrong order. Hiding is only ever a matter of what is printed.
    """
    kind = str(element.get("kind") or "")
    if kind == "rubric" and not show_rubrics:
        return []

    held = [
        one
        for one in (element.get("translations") or [])
        if isinstance(one, dict) and one.get("lang") == lang
    ]
    # A section head with nothing held is furniture with no words; it says
    # nothing and is not an absence a reader can act on.
    if kind == "heading" and not held:
        return []

    named = element.get("name") or element.get("latin_incipit")
    lines: list[str] = []

    if kind == "heading":
        applicability = translation_applicability(held[0], context)
        if applicability != "applicable":
            return [indent + style.note(f"[held source text; applicability {applicability} for this formulary context]")]
        lines.append("")
        lines.extend(indent + one for one in style.heading(str(held[0]["text"]).strip(), rule="-"))
        if why and element.get("locus"):
            lines.append(indent + style.note(f"[{element['locus']}]"))
        return lines

    if named:
        speaker = element.get("speaker")
        title = str(named) + (f" ({speaker})" if speaker else "")
        lines.append("")
        lines.extend(indent + one for one in style.heading(title))
        if why and element.get("locus"):
            lines.append(indent + "  " + style.note(f"[{element['locus']}]"))
    elif held:
        lines.append("")

    body = indent + "  "
    if held:
        applicability = translation_applicability(held[0], context)
        if applicability != "applicable":
            lines.append(body + style.note(f"[held source text; applicability {applicability} for this formulary context]"))
            return lines
        text = str(held[0].get("text") or "")
        if kind == "rubric":
            # Bracketed in every tier. The brackets are the distinction; the
            # dimming, where a terminal has it, is only ease.
            for line in wrap(f"[ {' '.join(text.split())} ]", body):
                lines.append(style.note(line))
        elif kind in SPOKEN:
            turns = held[0].get("turns") or []
            if turns:
                for turn in turns:
                    words = str(turn.get("text") or "")
                    if turn.get("gloss") is True:
                        lines.extend(style.note(line) for line in wrap(f"[ Source translation: {words} ]", body))
                    elif turn.get("action") is True:
                        if show_rubrics:
                            lines.extend(style.note(line) for line in wrap(f"[ {words} ]", body))
                    else:
                        speaker = {"priest": "Priest", "server": "Server", "all": "All"}.get(turn.get("speaker"))
                        role = {"versicle": "℣", "response": "℟"}.get(turn.get("dialogue_role"))
                        cue = (role + (" — " + speaker if speaker else "")) if role else speaker
                        marker = turn.get("printed_marker")
                        if cue and marker and words.startswith(marker + " "):
                            words = words[len(marker) + 1:]
                        shown = ((cue + ": ") if cue else "") + words
                        lines.extend(wrap(style.text(shown), body))
            else:
                for line in wrap(style.versicled(text), body):
                    lines.append(line)
        else:
            lines.extend(wrap(text, body))
        return lines

    # Absence, with the reason the element itself records, and never a blank.
    if not named:
        lines.append("")
        lines.append(indent + style.note(f"[{kind or 'element'}]"))
    reason = (element.get("absent") or {}).get(absence_side(lang))
    lines.append(body + style.note(f"[absent: {reason or 'not held'}]"))
    if element.get("latin_incipit") and element.get("latin_incipit") != element.get("name"):
        lines.append(body + style.note(f"opens {element['latin_incipit']}"))
    return lines
