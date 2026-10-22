"""The Code, Canon by Canon: a citation in, the canon's history out.

A canon lawyer arrives with a citation, so the citation is the entrance: look
one up and read where the canon stands, every act that touched it, and each
paragraph before and after. The acts are the second axis. Everything is asked
of the law page's own model (`code-model.js`) through `adapters/law.js`.

A canon's words are in one of three states and the three never look alike:
present (only the 1917 Latin, which is public domain), withheld with the
reason (the 1983 Code and the Eastern Code, with the act that established the
text now in force beside the reason), or unread. An authentic interpretation
is its own kind of stop: it settles meaning and changes no word.

This is a study aid, not legal advice, and the record declares no as-of date;
the caption says both.
"""
from __future__ import annotations

import re

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge
from ..dialogs import Ask, Pick, Reading
from ..repo import Refused
from ..surface import Surface
from ..timeline import Doc
from ..widgets import Ink, Panel, ScrollPanel

ADAPTER = "law"
TIGHT = 90  # columns under which the side column is swapped in by `f` rather than shown beside
TONE = "$law-color"
KIND_MARKS = {"promulgated": "●", "printed": "○", "unstated": "◌"}


def body_text(ink: Doc, body: dict, indent: str) -> None:
    """Present, withheld (with its reason and the establishing act), or unread."""
    state = body["state"]
    if state == "present":
        ink(indent)("┃ ", TONE)(body["text"]).line()
        return
    if state == "withheld":
        ink(indent)("⊘ ", "bold $warning")(body["lead"], "bold $warning")(" ".join(body["reason"].split()), "$warning").line()
    else:
        ink(indent)("◌ ", "$text-muted")(body["text"], "italic $text-muted").line()
    if body.get("established"):
        ink(indent)("  ↳ ", TONE).line(body["established"]["sentence"], "italic")


def side_text(ink: Doc, side: dict, indent: str) -> None:
    if side.get("nothing"):
        ink(indent).line(side["nothing"], "italic $text-muted")
        return
    for edition in side.get("editions") or []:
        ink(indent)(edition["label"], "bold")(f"  {edition['language']}", "$text-muted").line()
        body_text(ink, edition["body"], indent + "  ")
    if side.get("body"):
        body_text(ink, side["body"], indent)


def interpretation_text(ink: Doc, card: dict, indent: str) -> None:
    # The force and the Pope's disposition are different things and are said apart.
    ink(indent)("Force  ", f"bold {TONE}").line(card["force"])
    if card.get("papal"):
        ink(indent)("How the Pope disposed of it  ", f"bold {TONE}").line(card["papal"])
    if card.get("withheld"):
        ink(indent)("⊘ ", "bold $warning").line(" ".join(card["withheld"].split()), "$warning")
    for name in ("question", "answer"):
        if card.get(name):
            ink(indent).line(card[name]["label"], "bold underline")
            ink(indent).line(card[name]["text"])
    for note in card.get("notes") or []:
        ink(indent).line(" ".join(note.split()), "$text-muted")


def stop_text(ink: Doc, stop: dict, indent: str = "    ") -> None:
    interpreted = stop["state"] == "interpreted"
    mark = "◆" if interpreted else "●"
    ink(indent[:-2])(f"{mark} ", f"bold {TONE}")(stop["title"], "bold")(f" — {stop['what']}", f"italic {TONE}").line()
    ink(indent).line(stop["meta"], "$text-muted")
    if interpreted:
        ink(indent).line(stop["note"], "italic")
        if stop.get("interpretation"):
            interpretation_text(ink, stop["interpretation"], indent)
    elif stop.get("before") is not None:
        ink(indent).line("Before", "bold")
        side_text(ink, stop["before"], indent + "  ")
        ink(indent).line("After", "bold")
        side_text(ink, stop["after"], indent + "  ")
        ink(indent).line(stop["fields"], "$text-muted")
    elif stop.get("standing") is not None:
        side_text(ink, stop["standing"], indent)
    if stop.get("marker"):
        ink(indent).line(stop["marker"], "$warning")
    for row in stop["basis"]:
        ink(indent)(f"{row['kind']} ", f"bold {TONE}").line(" ".join(row["text"].split()), "$text-muted")


def canon_text(view: dict) -> Doc:
    """The page's canon view (law.js openCanon and paragraphSection)."""
    ink = Doc()
    ink(view["citation"], f"bold {TONE}")("   " + view["line_label"], "bold").line()
    if view["place"]:
        for position, step in enumerate(view["place"]):
            if position:
                ink(" › ", "$text-muted")
            if step["kind"]:
                ink(f"{step['kind']} ", "$text-muted")
            ink(step["label"])
        ink.line()
    else:
        ink.line(view["place_none"], "italic $text-muted")
    ink.line(view["count"], "$text-muted")
    if view.get("fell_through"):
        ink.line(view["fell_through"], "italic $warning")
    ink.line()
    correspondence = view["correspondence"]
    ink.line(correspondence["heading"], "bold underline")
    ink.line(correspondence["note"], "italic $text-muted")
    for claim in correspondence["claims"]:
        ink.line(claim["heading"], "bold")
        if claim["note"]:
            ink.line(claim["note"])
        ink.line(claim["source"], "$text-muted")
    for paragraph in view["paragraphs"]:
        ink.line()
        ink(paragraph["citation"], f"bold {TONE}")
        if paragraph.get("asked"):
            ink("  ◀ " + paragraph["asked_mark"], "bold $hotkey")
        ink.line()
        if paragraph.get("error"):
            ink.line(paragraph["error"], "bold $error")
            continue
        ink.line("  " + paragraph["state"])
        ink.line("  " + paragraph["now_heading"], "bold")
        side_text(ink, paragraph["now"], "    ")
        ink.line("  Through time", "bold")
        if paragraph["through_none"]:
            ink.line("    " + paragraph["through_none"], "italic $text-muted")
        for stop in paragraph["through"]:
            stop_text(ink, stop)
    return ink


def act_text(view: dict, *, full: bool) -> Doc:
    """The page's act panel (law.js openStation and renderStationChanges)."""
    ink = Doc()
    if view.get("missing"):
        return ink.line(view["missing"], "bold $warning")
    ink.line(view["title"], f"bold {TONE}")
    for name, value in view["facts"]:
        ink(f"{name}: ", "bold").line(" ".join(value.split()))
    for name in ("kind_note", "gap_note", "departures"):
        if view.get(name):
            ink.line(view[name], "italic $text-muted")
    if view.get("change_error"):
        ink.line(view["change_error"], "italic $warning")
        return ink
    ink.line().line(view["extent"], "bold")
    if view.get("printed_caveat"):
        ink.line(view["printed_caveat"], "italic $warning")
    if view.get("rests_on"):
        ink.line().line("On what this station rests", "bold underline")
        for title, said in view["rests_on"]:
            ink.line(title, "bold")
            ink.line(" ".join(said.split()), "$text-muted")
    if view.get("divisions"):
        ink.line().line(view["divisions_heading"], "bold underline")
        for row in view["divisions"]:
            ink(f"  {row['title']}", "bold")(f"  {row['meta']}", "$text-muted").line()
            if row["note"]:
                ink.line(f"    {' '.join(row['note'].split())}", "$text-muted")
    if view.get("groups"):
        ink.line().line(view["units_heading"], "bold underline")
        shown = 0
        for group in view["groups"]:
            ink.line(f"  {group['heading']}", f"bold {TONE}")
            for canon in group["canons"]:
                shown += 1
                if not full and shown > 6:
                    continue
                ink(f"    {canon['citation']}", "bold")(f"  {canon['what']}", f"italic {TONE}").line()
                if canon.get("before") is not None:
                    ink.line("      Before", "$text-muted")
                    side_text(ink, canon["before"], "        ")
                    ink.line("      After", "$text-muted")
                    side_text(ink, canon["after"], "        ")
                elif canon.get("standing") is not None:
                    side_text(ink, canon["standing"], "      ")
                if canon.get("marker"):
                    ink.line(f"      {canon['marker']}", "$warning")
                if full:
                    for row in canon["basis"]:
                        ink(f"      {row['kind']} ", f"bold {TONE}").line(" ".join(row["text"].split()), "$text-muted")
        if not full and shown > 6:
            ink.line(f"  … {shown - 6} more; enter on the act reads it whole", "italic $text-muted")
    if view.get("interpretations"):
        ink.line().line(view["interpretations_heading"], "bold underline")
        ink.line(view["interpretations_note"], "italic $text-muted")
        for row in view["interpretations"]:
            ink.line(f"  {row['citation']}", f"bold {TONE}")
            interpretation_text(ink, row["card"], "    ")
    if view.get("unestablished"):
        ink.line().line("Left unestablished", "bold underline")
        ink.line(view["unestablished_note"], "italic $text-muted")
        for row in view["unestablished"]:
            ink.line(f"  {row['unit']}", "bold").line(f"    {row['marker']}", "$warning")
    if view.get("empty"):
        ink.line(view["empty"], "italic $text-muted")
    if view.get("state_label"):
        ink.line()("  x ", "bold $hotkey").line(view["state_label"], "underline")
    return ink


class Law(Surface):
    key = "8"
    label = "Law"
    HELP = (
        ("g or /", "look up a canon: c. 1095, can. 1095 §2, or the number alone"),
        ("b", "choose the body of law the lookup keeps to (Any, 1917, 1983, CCEO, …)"),
        ("a", "the acts, oldest first; enter opens one"),
        ("enter", "read the open act whole, or open the highlighted act"),
        ("x", "the law as it stood after the open act"),
        ("s", "the structure of the Code, and a canon from it"),
        ("o", "the bodies of law, and no map between them"),
        ("e", "what this record claims, in its own words"),
        ("backspace", "back to what was open before"),
        ("f", "focus: the canon alone, full width; again to restore (under 90 columns: swap in lookup and acts)"),
    )
    BINDINGS = [
        Binding("g,slash", "lookup", "look up a canon"),
        Binding("b", "body", "body of law"),
        Binding("a", "acts", "acts list"),
        Binding("s", "structure", "structure of the Code"),
        Binding("x", "state", "the law as it stood after the open act", show=False),
        Binding("o", "bodies", "the bodies of law, and no map between them", show=False),
        Binding("e", "extent", "what this record claims", show=False),
        Binding("backspace", "back", "back to what was open before", show=False),
    ]
    DEFAULT_CSS = """
    Law #law-caption { height: auto; max-height: 3; padding: 0 1; }
    Law .law-side { width: 52; }
    Law #law-lookup { height: auto; }
    Law #law-acts { height: 1fr; }
    Law #law-canon { width: 1fr; }
    """
    CSS = """
    .law OptionList { scrollbar-color: $law-color 45%; scrollbar-color-hover: $law-color 75%;
        scrollbar-color-active: $law-color; scrollbar-background: $surface; }
    .law.focus .law-side { display: none; }
    .law.narrow .law-side { width: 38; }
    .law.narrow #law-caption { max-height: 2; }
    .law.tight .law-side { display: none; }
    .law.tight.focus .law-side { display: block; width: 1fr; }
    .law.tight.focus #law-canon { display: none; }
    """

    def on_resize(self, event) -> None:
        super().on_resize(event)
        # Under 90 columns the lookup and the acts give way to the canon; f swaps them in.
        self.set_class(event.size.width < TIGHT, "tight")

    def refocus(self) -> None:
        """The canon is the reading: it takes the focus when it shows, so the keys scroll it."""
        focused = self.app.focused
        if focused is not None and self in focused.ancestors and focused.region.area:
            return
        if self.has_class("tight") and self.has_class("focus"):
            super().refocus()
        else:
            self.query_one("#law-canon", ScrollPanel).focus()

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.opening: dict = {}
        self.asked = ""
        self.line = ""
        self.shown: dict = {}
        self.act: dict = {}
        self.trail: list[tuple[str, dict]] = []
        self.pending: dict = {}

    # --- building --------------------------------------------------------

    def build(self) -> None:
        self.mount(
            Static("", id="law-caption"),
            Horizontal(
                Vertical(
                    Panel(Static("", id="law-lookup-text"), title="lookup", id="law-lookup"),
                    Panel(OptionList(id="law-act-list"), title="acts, oldest first", id="law-acts"),
                    classes="law-side",
                ),
                ScrollPanel(Static("", id="law-canon-text"), title="canon", id="law-canon"),
            ),
        )
        self.start()

    @work(thread=True, exclusive=True, group="law-start")
    def start(self) -> None:
        try:
            opening = bridge.call(ADAPTER, "opening")
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.opened_with, opening)

    def fail(self, message: str) -> None:
        self.query_one("#law-canon-text", Static).update(Ink()(message, "bold $error").content())

    def opened_with(self, opening: dict) -> None:
        self.opening = opening
        caption = Ink()
        # The reader's own caption: AGENTS.md asks canon-law work to say both, and neither the
        # page nor the record does. The as-of date is the record's own, and it declares none.
        caption("A study aid, not legal advice. ", "bold $warning")
        if opening.get("recorded_on"):
            caption(f"The record is as of {opening['recorded_on']}, as it declares.", "$warning")
        else:
            caption("This record declares no as-of date; none is supplied here.", "$warning")
        caption.line()
        if opening.get("banner"):
            caption.line(opening["banner"], "bold $error")
        caption(opening["heading"], f"bold {TONE}")("  " + opening["tally"], "$text-muted")
        self.query_one("#law-caption", Static).update(caption.content())
        listing = self.query_one("#law-act-list", OptionList)
        options = []
        for act in opening["acts"]:
            ink = Doc()
            ink(KIND_MARKS.get(act["kind"], "●") + " ", f"bold {TONE}").line(act["title"], "bold")
            ink.line(f"  {act['meta']}", "$text-muted")
            ink(f"  {act['extent']}", f"italic {TONE}")
            options.append(Option(ink, id=f"act-{act['id']}"))
        listing.add_options(options)
        self.show_lookup()
        pending, self.pending = self.pending, {}
        if pending:
            self.follow(**pending)
        elif not self.shown:
            self.show_invite()

    def show_invite(self) -> None:
        ink = Doc()
        ink.line(self.opening["invite"])
        ink.line()
        ink.line(self.opening["rights_heading"], "bold")
        ink.line(self.opening["rights"], "$text-muted")
        ink.line()
        ink.line("How the three states of a canon's words are drawn", "bold")
        ink("  ┃ ", TONE).line("present: the words, printed here (only the 1917 Code's Latin)")
        ink("  ⊘ ", "bold $warning").line("withheld here, with the reason and the act that established the text")
        ink("  ◌ ", "$text-muted").line("unread: the record carries the canon's identity, not its words")
        ink("  ◆ ", f"bold {TONE}").line("an authentic interpretation: it settles meaning and changes no word")
        self.query_one("#law-canon-text", Static).update(ink.content())
        self.query_one("#law-canon", ScrollPanel).retitle("canon")

    def show_lookup(self) -> None:
        ink = Ink()
        ink("Canon  ", "bold")(self.asked or "—", f"bold {TONE}").line()
        label = next((row["label"] for row in self.opening.get("lines", []) if row["id"] == self.line), "Any")
        ink("Body of law  ", "bold")(label, TONE).line()
        ink("g look up · b body of law · a acts · s structure", "$text-muted")
        self.query_one("#law-lookup-text", Static).update(ink.content())

    # --- intent ----------------------------------------------------------

    def follow(self, canon: str | None = None, line: str | None = None, act: str | None = None,
               unit: str | None = None, **_) -> None:
        if not self.opening:
            self.pending = {key: value for key, value in dict(canon=canon, line=line, act=act, unit=unit).items() if value}
            return
        if line is not None:
            self.line = self.line_of(line) or ""
        if canon:
            self.look_up(canon)
        elif unit:
            self.fetch("unit", unit)
        if act:
            self.fetch_act(act, False)

    def look_up(self, text: str) -> None:
        """A typed citation, from the command line or the lookup box alike.

        "1983 c. 1008": a leading word naming a body of law, then a citation,
        keeps the lookup to that body. It is never a mapping from one body's
        numbering to another's."""
        text = text.strip()
        match = re.match(r"^\s*(\S+)\s+((?:c|can|cann|canon|cc)\.?\s*\d.*|\d.*)$", text, re.I)
        if match:
            found = self.line_of(match.group(1))
            if found:
                self.line, text = found, match.group(2)
        self.run_lookup(text)

    def line_of(self, word: str) -> str | None:
        """The body of law a word names: its id, or a year its own label carries
        ("1917", "1983", "1990"). Never a guess from anything else."""
        word = word.strip().lower()
        for row in self.opening.get("lines", []):
            if word == row["id"].lower():
                return row["id"]
            if re.fullmatch(r"\d{4}", word) and re.search(rf"\b{word}\b", row["label"]):
                return row["id"]
        return None

    def where(self) -> str:
        if self.shown.get("view") == "canon":
            return f"{self.shown['citation']} · {self.shown['line_label']} · a study aid, not legal advice"
        if self.act:
            return f"{self.act.get('title', '')}"
        return "a study aid, not legal advice"

    # --- looking up ------------------------------------------------------

    def action_lookup(self) -> None:
        if not self.opening:
            return

        def answered(value: str | None) -> None:
            if value:
                self.look_up(value)

        self.app.push_screen(Ask("look up a canon", "c. 1095, can. 1095 §2, 1095, or 1983 c. 1095 to keep to one "
                                 "body of law — or any word in a canon's identity or division. Each body of law "
                                 "numbers on its own.", self.asked), answered)

    def run_lookup(self, text: str) -> None:
        self.asked = text
        self.show_lookup()
        self.fetch("lookup", text, self.line)

    def action_body(self) -> None:
        if not self.opening:
            return
        offers = [("", "Any")] + [(row["id"], f"{row['label']}  ·  {row['acts']} acts") for row in self.opening["lines"]]

        def picked(value) -> None:
            if value is None:
                return
            self.line = value
            self.show_lookup()
            if self.asked:
                self.run_lookup(self.asked)  # page: law.js:1376-1378 — a change of body re-runs the lookup

        self.app.push_screen(Pick("body of law", offers, "A lookup keeps to the body chosen; it never widens to "
                                  "another, whose canon of that number is a different law."), picked)

    @work(thread=True, exclusive=True, group="law-canon")
    def fetch(self, fn: str, *args) -> None:
        try:
            view = bridge.call(ADAPTER, fn, *args)
        except Refused as refusal:
            view = {"view": "none", "heading": "", "message": str(refusal)}
        self.deliver(self.show, view)

    def remember(self) -> None:
        if self.shown:
            self.trail.append(("shown", self.shown))
            del self.trail[:-12]

    def show(self, view: dict, *, back: bool = False) -> None:
        if not back:
            self.remember()
        self.shown = view
        box = self.query_one("#law-canon", ScrollPanel)
        text = self.query_one("#law-canon-text", Static)
        kind = view.get("view")
        if kind == "canon":
            text.update(canon_text(view).content())
            box.retitle(f"{view['citation']} · {view['line_label']}")
            box.border_subtitle = "a study aid, not legal advice · backspace back"
        elif kind == "choices":
            ink = Doc()
            ink.line(view["heading"], f"bold {TONE}")
            if view.get("fell_through"):
                ink.line(view["fell_through"], "italic $warning")
            ink.line(view["note"]).line()
            for row in view["choices"]:
                ink(f"  {row['citation']}", "bold")(f"  {row['line_label']}", TONE)
                ink(f"  {row['place']}  ·  {row['size']}", "$text-muted").line()
            text.update(ink.content())
            box.retitle(f"{len(view['choices'])} canons answer to {view['heading']}")
            box.border_subtitle = "choose one in the list"
            offers = [(row["key"], f"{row['citation']}  ·  {row['line_label']}  ·  {row['place']}  ·  {row['size']}")
                      for row in view["choices"]]
            hint = (view["fell_through"] + " " if view.get("fell_through") else "") + view["note"]
            self.app.push_screen(Pick(f"canons answering to {view['heading']}", offers, hint),
                                 lambda value: value and self.fetch("canon", value, None))
        elif kind == "structure":
            text.update(self.structure_text(view).content())
            box.retitle("the structure of the Code")
            box.border_subtitle = "s again: open a canon from it"
        elif kind == "bodies":
            text.update(self.bodies_text(view).content())
            box.retitle("the bodies of law, and no map between them")
            box.border_subtitle = ""
        elif kind == "extent":
            ink = Doc()
            # page: law/index.html, "What this record claims"
            ink.line("Written by the record itself, not by this page. Silence in it is silence because nothing was "
                     "established, never because a canon was checked and found unchanged.", "italic $text-muted")
            ink.line()
            ink.line(view["text"])
            text.update(ink.content())
            box.retitle("what this record claims")
            box.border_subtitle = ""
        elif kind == "act":
            text.update(act_text(view["act"], full=False).content())
            box.retitle(f"act · {view['act'].get('kind', '')}")
            box.border_subtitle = "enter read whole · x the law after it · backspace back"
        else:
            ink = Doc()
            if view.get("heading"):
                ink.line(view["heading"], f"bold {TONE}")
            ink.line(view.get("message", ""), "italic")
            text.update(ink.content())
            box.retitle("canon")
            box.border_subtitle = ""
        box.scroll_home(animate=False)
        self.app.refresh_where()

    def action_back(self) -> None:
        if self.trail:
            _, view = self.trail.pop()
            self.show(view, back=True)

    # --- the acts --------------------------------------------------------

    def action_acts(self) -> None:
        self.query_one("#law-act-list", OptionList).focus()

    @on(OptionList.OptionSelected, "#law-act-list")
    def picked_act(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("act-"):
            ident = event.option.id[4:]
            self.fetch_act(ident, self.act.get("id") == ident and self.shown.get("view") == "act")

    @work(thread=True, exclusive=True, group="law-act")
    def fetch_act(self, ident: str, read: bool) -> None:
        try:
            view = bridge.call(ADAPTER, "act", ident)
        except Refused as refusal:
            view = {"missing": str(refusal)}
        self.deliver(self.show_act, view, read)

    def show_act(self, view: dict, read: bool) -> None:
        self.act = view
        if read:
            self.app.push_screen(Reading(f"{view.get('title', '')}", act_text(view, full=True).content(),
                                         "esc close · a study aid, not legal advice", walks=False))
            return
        self.show({"view": "act", "act": view})

    def action_state(self) -> None:
        if not self.act.get("state_label"):
            self.app.notify("Open an act that names a recorded state first (a, then enter).")
            return
        self.fetch_state(self.act["id"])

    @work(thread=True, exclusive=True, group="law-state")
    def fetch_state(self, ident: str) -> None:
        try:
            view = bridge.call(ADAPTER, "state", ident)
        except Refused as refusal:
            view = {"error": str(refusal)}
        self.deliver(self.read_state, view)

    def read_state(self, view: dict) -> None:
        ink = Doc()
        if view.get("error"):
            ink.line(view["error"], "bold $error")
        else:
            ink.line(view["summary"], "bold")
            for division in view["divisions"]:
                ink.line().line(division["title"], f"bold {TONE}")
                if division["designation"]:
                    ink.line(division["designation"], "$text-muted")
                if division["empty"]:
                    ink.line(division["empty"], "italic $text-muted")
                for unit in division["units"]:
                    ink.line(f"  {unit['citation']}", "bold")
                    side_text(ink, unit["side"], "    ")
            if view["unestablished"]:
                ink.line().line("Not established at this point", "bold underline")
                for marker in view["unestablished"]:
                    ink.line(f"  {marker}", "$warning")
            if view["interpretations"]:
                ink.line().line("Interpretations standing at this point", "bold underline")
                for row in view["interpretations"]:
                    ink.line(f"  {row['citation']}", "bold").line(f"    {row['record']}", "$text-muted")
        self.app.push_screen(Reading("Read the law as it stood after this act", ink.content(),
                                     view.get("title", ""), walks=False))

    # --- structure, bodies, extent --------------------------------------

    def action_structure(self) -> None:
        if not self.opening:
            return
        if self.shown.get("view") == "structure":
            self.show_structure_pick(self.shown)
        else:
            self.fetch("structure")

    def structure_text(self, view: dict) -> Doc:
        ink = Doc()
        # page: law/index.html, "The structure of the Code"
        ink.line("Books, Parts, Titles and Chapters, as the record places each canon. Nothing here is worked out from "
                 "the shape of an identifier; where the record places a canon nowhere, it stands apart and says so.",
                 "italic $text-muted")

        def walk(node: dict, depth: int) -> None:
            pad = "  " * depth
            if node.get("unplaced"):
                ink(pad + node["unplaced"], "italic")(", ".join(row["citation"] for row in node["canons"])).line()
                return
            ink(pad)(f"{node['kind']} ", "$text-muted")(node["label"], "bold")(f"  {node['count']}", TONE).line()
            for child in node["children"]:
                walk(child, depth + 1)
            if node["canons"]:
                ink(pad + "  ")
                for position, canon in enumerate(node["canons"]):
                    if position:
                        ink(" · ", "$text-muted")
                    ink(canon["citation"])
                    if canon["size"]:
                        ink(f" {canon['size']}", "$text-muted")
                    if canon["gone"]:
                        ink(f" ({canon['gone']})", "italic $text-muted")
                ink.line()

        for body in view["bodies"]:
            ink.line()
            if body["label"]:
                ink.line(body["label"], f"bold {TONE}")
            if body["none"]:
                ink.line(body["none"], "italic $text-muted")
            for node in body["tree"]:
                walk(node, 0)
        return ink

    def show_structure_pick(self, view: dict) -> None:
        offers: list[tuple[str, str]] = []

        def walk(node: dict, trail: list[str], body: str) -> None:
            if node.get("unplaced"):
                for canon in node["canons"]:
                    offers.append((canon["key"], f"{canon['citation']}  ·  {body}  ·  placed nowhere by this record"))
                return
            here = trail + [f"{node['kind']} {node['label']}".strip()]
            for canon in node["canons"]:
                offers.append((canon["key"], f"{canon['citation']}  ·  {body}  ·  {' › '.join(here)}"))
            for child in node["children"]:
                walk(child, here, body)

        for body in view["bodies"]:
            for node in body["tree"]:
                walk(node, [], body["label"])
        self.app.push_screen(Pick("a canon from the structure", offers,
                                  "As the record places each canon; numbers are never carried across bodies of law."),
                             lambda value: value and self.fetch("canon", value, None))

    def action_bodies(self) -> None:
        if self.opening:
            self.fetch("bodies")

    def bodies_text(self, view: dict) -> Doc:
        ink = Doc()
        # page: law/index.html, "The bodies of law, and no map between them"
        ink.line("Where this record carries more than one Code, they are separate lines and they number independently. "
                 "This page joins no canon of one to a canon of another: any such correspondence is a scholarly claim, "
                 "and it is shown with its source or it is not shown.", "italic $text-muted")
        for line in view["lines"]:
            ink.line().line(line["heading"], f"bold {TONE}")
            ink.line(line["meta"], "$text-muted")
            if line["note"]:
                ink.line(" ".join(line["note"].split()))
        ink.line()
        for pair in view["pairs"]:
            ink.line(pair["heading"], "bold")
            ink.line(pair["text"], "$text-muted")
        return ink

    def action_extent(self) -> None:
        if self.opening:
            self.show({"view": "extent", "text": self.opening.get("extent") or "This record states no extent."})

    @on(OptionList.OptionHighlighted, "#law-act-list")
    def highlighted_act(self, event: OptionList.OptionHighlighted) -> None:
        box = self.query_one("#law-acts", Panel)
        box.border_subtitle = "enter open · again to read whole"
