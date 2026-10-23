"""The Story of Salvation: the reading plan at three depths, walked in order.

Everything here is drawn from what `adapters/scripture.js` asks of the page's
own model (`plan-model.js`) and renderer (`Triptych.renderCitation`). The
tracks, their nesting, their counts and pacing, each reading's place, its
reference, and its verse text under an edition, with every refusal and recast
note, are the model's; this module lays them out and moves between them.

A period is known here by its place among the plan's periods, and shown by its
label alone: its key never reaches the terminal.
"""
from __future__ import annotations

import re

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge, refs
from ..dialogs import Ask, Pick
from ..repo import Refused
from ..surface import Surface
from ..theme import METER_STOPS, blend
from ..widgets import SUPERSCRIPT, Ink, Panel, ScrollPanel, literal

ADAPTER = "scripture"
WHITESPACE = re.compile(r"\s+")
# A reading that first appears at a smaller track than the one being read, by
# that track's rank: the page's tier badge (track.js:420), as a glyph with a legend.
BADGES = ("◆", "◇", "◈")
# The stacked meter in the periods pane: one glyph per track, smallest first.
LAYERS = ("█", "▆", "▃")


def _clip(text: str, width: int) -> str:
    if width <= 1:
        return text[:max(0, width)]
    return text if len(text) <= width else text[: width - 1] + "…"


def _the(label: str, *, start: bool = False) -> str:
    """'the Landmarks track', 'The Story track': the article said once, where the
    page's "in the " + label says it twice (track.js:480, 566, 755)."""
    said = f"{label} track" if label.lower().startswith("the ") else f"the {label} track"
    return said[0].upper() + said[1:] if start else said


def _plain(text: str) -> str:
    return WHITESPACE.sub(" ", text or "")


def _meter(ink: Ink, fraction: float, width: int) -> Ink:
    """A btop meter in the theme's own empty tone: filled cells take the
    gradient colour of their position. The count is always printed beside it."""
    width = max(1, width)
    filled = round(min(1.0, max(0.0, fraction)) * width)
    for cell in range(width):
        ink("■", blend(METER_STOPS, cell / max(1, width - 1)) if cell < filled else "$meter-empty")
    return ink


# Run classes the shared renderer writes (browser-core.js renderLocus,
# renderCitation, notice), most specific first, and the look each is given.
RUN_STYLES = (
    ("verse-num", "bold $scripture-color"),
    ("elision", "$muted"),
    ("chapter-mark", "bold $scripture-color"),
    ("citation-ref-recast-only", "italic $muted"),
    ("citation-recast", "italic $muted"),
    ("notice", "$warning"),
)


def _run_style(classes: list[str], tags: list[str]) -> str:
    for name, style in RUN_STYLES:
        if name in classes:
            if name == "notice" and "strong" in tags:
                return "bold $warning"
            return style
    if "strong" in tags or "b" in tags:
        return "bold"
    if "em" in tags or "i" in tags:
        return "italic"
    return ""


def runs(ink: Ink, block: dict, *, verse_lines: bool = False, style: str = "") -> Ink:
    """One block of the page's, styled by the classes its runs carry.

    The page sets running text with normal white-space, so a newline inside a
    text node is a space. With `verse_lines` each verse after the first begins
    a line of its own; nothing else changes.
    """
    started = False
    for run in block.get("runs", []):
        names = run.get("classes", [])
        text = _plain(run.get("text", ""))
        if "verse-num" in names:
            if verse_lines and started:
                ink.line()
            text = text.translate(SUPERSCRIPT)
        ink(text, _run_style(names, run.get("tags", [])) or style)
        started = True
    return ink


class Scripture(Surface):
    key = "4"
    label = "Scripture"
    HELP = (
        ("← / →", "previous / next reading; in a period's view, previous / next period; "
                  "from the orientation, → opens the reading in hand"),
        ("[ / ]", "previous / next period"),
        ("t", "next track, smallest first; the place in the story is kept"),
        ("b", "next Bible edition, in the manifest's order"),
        ("e", "choose the Bible edition from the list"),
        ("g", "go to a reading: its number in this track, a reference such as 'Gen 3', or words of its title"),
        ("o", "the track's orientation: what it is, how long it takes, what it leaves out"),
        ("p", "all of the period this reading belongs to"),
        ("enter", "read the highlighted track, period or reading"),
        ("v", "verses as running text, as the page sets them, or one verse to a line"),
        ("c", "the commentary held on this reading's first chapter, in Catena"),
        ("f", "focus: the page alone, full width; again to restore"),
        ("click", "a track, a period or a reading in the side panes"),
    )
    BINDINGS = [
        Binding("left,h", "step(-1)", "previous reading, or previous period in a period's view", show=False),
        Binding("right,l", "step(1)", "next reading, or next period in a period's view", show=False),
        Binding("left_square_bracket", "period(-1)", "previous period", show=False),
        Binding("right_square_bracket", "period(1)", "next period", show=False),
        Binding("t", "track", "next track"),
        Binding("b", "bible", "next edition"),
        Binding("e", "choose_bible", "choose an edition", show=False),
        Binding("g", "goto", "go to a reading"),
        Binding("o", "orient", "what it leaves out"),
        Binding("v", "verses", "running text or a verse to a line", show=False),
        Binding("p", "this_period", "all of this reading's period", show=False),
        Binding("c", "catena", "commentary on this chapter in Catena", show=False),
    ]
    CSS = """
    .scripture.focus #scripture-left { display: none; }
    .scripture.narrow #scripture-left { width: 34; }
    .scripture.short #scripture-tracks { display: none; }
    """
    DEFAULT_CSS = """
    Scripture #scripture-left { width: 46; }
    Scripture #scripture-tracks { height: auto; }
    Scripture #scripture-periods { height: auto; max-height: 50%; }
    Scripture #scripture-periods OptionList { height: auto; max-height: 100%; }
    Scripture #scripture-tracks OptionList { height: auto; }
    Scripture #scripture-readings { height: 1fr; }
    Scripture #scripture-readings OptionList { height: 1fr; }
    Scripture #scripture-head { height: auto; }
    Scripture #scripture-page { height: 1fr; }
    Scripture .sc-h1 { text-style: bold; color: $scripture-color; padding: 0 0 1 0; }
    Scripture .sc-h2 { text-style: bold; padding: 0 0 0 0; }
    Scripture .sc-p { padding: 0 0 1 0; }
    Scripture .sc-lead { color: $text-muted; padding: 0 0 1 0; }
    Scripture .sc-aside { margin: 0 0 1 2; padding: 0 0 0 1; border-left: outer $scripture-color 60%; }
    Scripture .sc-why {
        margin: 0 0 1 0; padding: 0 1; border-left: thick $scripture-color; background: $scripture-color 8%;
    }
    Scripture .sc-notice { color: $warning; padding: 0 0 1 0; }
    Scripture .sc-diverted { margin: 0 0 1 0; padding: 0 1; border-left: thick $warning; color: $warning; }
    Scripture .sc-recast { color: $text-muted; text-style: italic; padding: 0 0 1 0; }
    Scripture .sc-chapter { padding: 0 0 0 0; }
    Scripture .sc-passage { padding: 0 0 1 0; }
    Scripture .sc-rule { color: $text-muted; padding: 0 0 1 0; }
    Scripture .sc-table { padding: 0 0 1 2; }
    """

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.opening: dict = {}
        self.tracks: dict[str, dict] = {}
        self.track: dict = {}
        self.tier = ""
        self.bible = ""
        self.view = "orient"  # orient | period | reading
        self.order: int | None = None  # the reading in hand, by its key (`order`)
        self.n = 1  # the period in view, by its place among the plan's periods
        self.listed = 0  # the period whose readings the list shows
        self.reading: dict | None = None
        self.notice = ""
        self.verse_lines = False
        self.pending: dict = {}
        self.seq = 0

    # --- building --------------------------------------------------------

    def build(self) -> None:
        self.mount(
            Horizontal(
                Vertical(
                    Panel(OptionList(id="scripture-track-list"), title="tracks", id="scripture-tracks"),
                    Panel(OptionList(id="scripture-period-list"), title="periods", id="scripture-periods"),
                    Panel(OptionList(id="scripture-reading-list"), title="readings", id="scripture-readings"),
                    id="scripture-left",
                ),
                Vertical(
                    Panel(Static("", id="scripture-head-text"), title="the story of salvation", id="scripture-head"),
                    ScrollPanel(Static("", id="scripture-loading"), title="", id="scripture-page"),
                    id="scripture-right",
                ),
            )
        )
        self.start()

    @work(thread=True, exclusive=True, group="scripture-start")
    def start(self) -> None:
        try:
            opening = bridge.call(ADAPTER, "opening")
            first = opening["tracks"][0]["tier"]
            track = bridge.call(ADAPTER, "track", first)
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.opened_with, opening, track)

    def opened_with(self, opening: dict, track: dict) -> None:
        self.opening = opening
        self.tracks[track["tier"]] = track
        self.track = self.track or track
        # The first track and the manifest's first edition, as the page opens
        # (track.js:795, 816).
        self.tier = self.tier or track["tier"]
        self.bible = self.bible or opening["bibles"][0]["id"]
        # The readings are what a reader moves through, so the cursor starts
        # there, wherever the shell first put it within this surface.
        if self.app.focused is None or self in self.app.focused.ancestors_with_self:
            self.query_one("#scripture-reading-list", OptionList).focus()
        # The orientation first; an intent carried here moves on from it, and
        # one that finds nothing leaves the reader there rather than nowhere.
        self.request()
        pending, self.pending = self.pending, {}
        if pending:
            self.follow(**pending)

    def fail(self, message: str) -> None:
        page = self.query_one("#scripture-page", ScrollPanel)
        page.remove_children()
        page.mount(Static(Ink()(message, "bold $error").content(), classes="sc-notice"))

    # --- what is asked, and what comes back --------------------------------

    def request(self, *, land: bool = False, notice: str = "") -> None:
        if not self.opening:
            return
        self.seq += 1
        self.fetch({"seq": self.seq, "tier": self.tier, "view": self.view, "order": self.order,
                    "n": self.n, "bible": self.bible, "land": land, "notice": notice})

    @work(thread=True, exclusive=True, group="scripture-view")
    def fetch(self, ask: dict) -> None:
        try:
            track = self.tracks.get(ask["tier"]) or bridge.call(ADAPTER, "track", ask["tier"])
            if ask["land"] and ask["order"] is not None:
                landed = bridge.call(ADAPTER, "land", ask["tier"], str(ask["order"]))
                ask["order"] = landed["order"]
                ask["notice"] = landed["notice"] or ask["notice"]
            reading = None
            if ask["view"] == "reading" and ask["order"] is not None:
                reading = bridge.call(ADAPTER, "reading", ask["tier"], str(ask["order"]), ask["bible"])
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.show, ask, track, reading)

    def show(self, ask: dict, track: dict, reading: dict | None) -> None:
        if ask["seq"] != self.seq:
            return
        self.tracks[track["tier"]] = track
        self.track = track
        self.order = ask["order"]
        self.notice = ask["notice"] if self.view == "reading" else ""
        self.reading = reading
        if reading:
            self.n = reading["n"]
        if not self.period(self.n):
            self.n = track["periods"][0]["n"]
            if self.view == "period":
                self.view = "orient"
        self.draw()

    # --- looking things up in what the model gave ---------------------------

    def period(self, n: int) -> dict | None:
        return next((one for one in self.track.get("periods", []) if one["n"] == n), None)

    def entries(self, n: int) -> list[dict]:
        return [one for one in self.track.get("readings", []) if one["n"] == n]

    def entry(self, order: int | None) -> dict | None:
        return next((one for one in self.track.get("readings", []) if one["order"] == order), None)

    def track_row(self, tier: str) -> dict:
        return next(one for one in self.opening["tracks"] if one["tier"] == tier)

    def bible_row(self) -> dict:
        return next((one for one in self.opening["bibles"] if one["id"] == self.bible), self.opening["bibles"][0])

    # --- moving --------------------------------------------------------------

    def follow(self, ref: str | None = None, reading: str | int | None = None, **_) -> None:
        if not (ref or reading):
            return
        if not self.opening:
            self.pending = {"ref": ref, "reading": reading}
            return
        if reading:
            try:
                self.locate(int(reading))
            except (TypeError, ValueError):
                self.app.notify(f"No reading of this plan is keyed {literal(repr(reading))}.", severity="warning")
        else:
            self.goto_ref(ref)

    def read(self, order: int) -> None:
        self.view, self.order = "reading", order
        self.request()

    def open_period(self, n: int) -> None:
        self.view, self.n = "period", n
        self.request()

    def action_step(self, step: int) -> None:
        if not self.track or self.track["tier"] != self.tier:
            return
        if self.view == "reading":
            readings = self.track["readings"]
            # Requests advance order before their response replaces reading.
            # Orders are keys, not consecutive positions in this track.
            at = next((i for i, row in enumerate(readings) if row["order"] == self.order), None)
            if at is not None and 0 <= at + step < len(readings):
                self.read(readings[at + step]["order"])
        elif self.view == "period":
            self.action_period(step)
        elif step > 0:
            self.read(self.order if self.entry(self.order) else self.track["begin"]["order"])

    def action_period(self, step: int) -> None:
        if not self.track:
            return
        places = [one["n"] for one in self.track["periods"]]
        here = self.n if self.n in places else places[0]
        at = places.index(here) + step
        if 0 <= at < len(places):
            self.open_period(places[at])

    def set_track(self, tier: str) -> None:
        if not self.opening or tier == self.tier:
            return
        self.tier = tier
        # The place is kept whatever is on screen (track.js:712); the page says
        # so only over a reading, where it is read.
        self.request(land=self.order is not None)

    def action_track(self) -> None:
        if not self.opening:
            return
        tiers = [one["tier"] for one in self.opening["tracks"]]
        self.set_track(tiers[(tiers.index(self.tier) + 1) % len(tiers)])

    def set_bible(self, ident: str) -> None:
        self.bible = ident
        if self.view == "reading":
            self.request()
        else:
            self.draw_head()
            self.app.refresh_where()

    def action_bible(self) -> None:
        if not self.opening:
            return
        ids = [one["id"] for one in self.opening["bibles"]]
        self.set_bible(ids[(ids.index(self.bible) + 1) % len(ids)] if self.bible in ids else ids[0])

    def action_choose_bible(self) -> None:
        if not self.opening:
            return

        def picked(value: str | None) -> None:
            if value:
                self.set_bible(value)

        offers = [(one["id"], ("● " if one["id"] == self.bible else "  ") + one["choice"])
                  for one in self.opening["bibles"]]
        self.app.push_screen(Pick("Bible edition", offers,
                                  "The editions the published manifest offers, in its order."), picked)

    def action_orient(self) -> None:
        if not self.opening:
            return
        self.view = "orient"
        self.request()

    def action_focus_reading(self) -> None:
        """The side panes away, the page full width; the cursor goes with what
        stays on screen, so the surface's keys still reach it."""
        super().action_focus_reading()
        target = "#scripture-page" if self.has_class("focus") else "#scripture-reading-list"
        self.query_one(target).focus()

    def action_this_period(self) -> None:
        if self.view == "reading" and self.reading:
            self.open_period(self.reading["n"])

    def action_verses(self) -> None:
        self.verse_lines = not self.verse_lines
        if self.view == "reading":
            self.draw_page()

    def action_catena(self) -> None:
        chapters = (self.reading or {}).get("chapters") or []
        if self.view != "reading" or not chapters:
            self.app.notify("Open a reading first; its first chapter is opened in Catena.")
            return
        first = chapters[0]
        self.app.action_surface("catena", ref=f"{first['token']} {first['chapter']}")

    def action_goto(self) -> None:
        if not self.track:
            return

        def answered(value: str | None) -> None:
            if value:
                self.goto_text(value)

        count = self.track["count"]
        self.app.push_screen(Ask("go to a reading",
                                 f"Its number in {_the(self.track['label'])} (1–{count}), a reference such as "
                                 "Gen 3 or Luke 2, or words of its title.", ""), answered)

    def goto_text(self, text: str) -> None:
        text = text.strip()
        if text.isdigit():
            index = int(text)
            readings = self.track["readings"]
            if 1 <= index <= len(readings):
                self.read(readings[index - 1]["order"])
            else:
                self.app.notify(f"{_the(self.track['label'], start=True)} has readings 1 to {len(readings)}.",
                                severity="warning")
            return
        if refs.parse(text, self.opening["books"]) is not None:
            self.goto_ref(text)
            return
        words = text.casefold()
        found = [one for one in self.track["readings"] if words in one["title"].casefold()]
        if len(found) == 1:
            self.read(found[0]["order"])
        elif found:
            self.offer(found, f"Readings of {_the(self.track['label'])} whose titles hold “{text}”")
        else:
            self.app.notify(f"No reading of {_the(self.track['label'])} has “{literal(text)}” in its title.",
                            severity="warning")

    def goto_ref(self, text: str) -> None:
        found = refs.parse(text, self.opening["books"])
        if found is None:
            named = re.sub(r"\s*\d+\s*$", "", text.strip()) or text
            self.app.notify(f"No book this plan reads is called “{literal(named)}”.", severity="warning")
            return
        book, chapter = found
        self.find_chapter(book["token"], chapter, f"{book['name']} {chapter}")

    @work(thread=True, exclusive=True, group="scripture-find")
    def find_chapter(self, token: str, chapter: int, said: str) -> None:
        try:
            found = bridge.call(ADAPTER, "at", self.tier, token, chapter)
        except Refused as refusal:
            self.deliver(self.app.notify, str(refusal), severity="warning")
            return
        self.deliver(self.found_chapter, found, said)

    def found_chapter(self, found: dict, said: str) -> None:
        here, anywhere = found["here"], found["anywhere"]
        if len(here) == 1:
            self.read(here[0]["order"])
        elif here:
            self.offer(here, f"Readings of {_the(self.track['label'])} that read {said}")
        elif anywhere:
            # Not at this depth: each is offered with the track it first appears at.
            def picked(value: str | None) -> None:
                if value:
                    row = next(one for one in anywhere if str(one["order"]) == value)
                    self.tier, self.view, self.order = row["tier"], "reading", row["order"]
                    self.request()

            offers = [(str(one["order"]), f"{one['title']} — {one['reference']}   ({one['tierLabel']} track)")
                      for one in anywhere]
            self.app.push_screen(Pick(f"{said} is not read in {_the(self.track['label'])}", offers,
                                      "Each reading is offered in the track it first appears at."), picked)
        else:
            self.app.notify(f"This plan reads nothing of {said}.", severity="warning")

    def offer(self, rows: list[dict], title: str) -> None:
        def picked(value: str | None) -> None:
            if value:
                self.read(int(value))

        listed = {one["order"]: one for one in self.track["readings"]}
        offers = []
        for row in rows:
            index = listed.get(row["order"], {}).get("index")
            offers.append((str(row["order"]), f"{index}. {row['title']} — {row['reference']}" if index
                           else f"{row['title']} — {row['reference']}"))
        self.app.push_screen(Pick(title, offers, "Nothing is chosen for you by order."), picked)

    @work(thread=True, exclusive=True, group="scripture-find")
    def locate(self, order: int) -> None:
        """Another surface asked for a reading by its key: read it in this track
        if it holds it, else in the track it first appears at."""
        try:
            tracks = [one["tier"] for one in self.opening["tracks"]]
            widest = self.tracks.get(tracks[-1]) or bridge.call(ADAPTER, "track", tracks[-1])
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.located, order, widest)

    def located(self, order: int, widest: dict) -> None:
        self.tracks[widest["tier"]] = widest
        row = next((one for one in widest["readings"] if one["order"] == order), None)
        if row is None:
            self.app.notify(f"This plan has no reading keyed {order}.", severity="warning")
            return
        current = self.tracks.get(self.tier) or {}
        held = any(one["order"] == order for one in current.get("readings", []))
        notice = ""
        if not held:
            self.tier = row["tier"]
            notice = (f"Reading {order} first appears at {_the(self.track_row(row['tier'])['label'])}, "
                      "which is shown.")
        self.view, self.order = "reading", order
        self.request(notice=notice)

    # --- the side panes -------------------------------------------------------

    @on(OptionList.OptionSelected, "#scripture-track-list")
    def picked_track(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("track-"):
            self.set_track(event.option.id[6:])

    @on(OptionList.OptionSelected, "#scripture-period-list")
    def picked_period(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("period-"):
            self.open_period(int(event.option.id[7:]))

    @on(OptionList.OptionHighlighted, "#scripture-period-list")
    def glanced_period(self, event: OptionList.OptionHighlighted) -> None:
        """Moving through the periods shows each one's readings, without leaving the page."""
        if event.option.id and event.option.id.startswith("period-"):
            n = int(event.option.id[7:])
            if n != self.listed:
                self.draw_readings(n)

    @on(OptionList.OptionSelected, "#scripture-reading-list")
    def picked_reading(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("reading-"):
            self.read(int(event.option.id[8:]))

    def on_resize(self, event) -> None:
        super().on_resize(event)
        self.set_class(event.size.height < 26, "short")
        if self.track:
            self.call_after_refresh(self.draw_sides)

    @staticmethod
    def _width(widget, fallback: int) -> int:
        width = widget.size.width
        return width if width > 8 else fallback

    def draw(self) -> None:
        self.draw_sides()
        self.draw_head()
        self.draw_page()
        self.app.refresh_where()

    def draw_sides(self) -> None:
        self.draw_tracks()
        self.draw_periods()
        self.draw_readings(self.n, follow=True)

    def draw_tracks(self) -> None:
        listing = self.query_one("#scripture-track-list", OptionList)
        width = self._width(listing, 40) - 1
        rows = self.opening["tracks"]
        widest = max(one["count"] for one in rows)
        name = max(len(one["label"]) for one in rows)
        bar = width - 2 - name - 1 - 3 - 1 - 1 - 4
        listing.clear_options()
        for one in rows:
            chosen = one["tier"] == self.tier
            ink = Ink()("● " if chosen else "  ", "bold $scripture-color")
            ink(f"{one['label']:<{name}} ", "bold" if chosen else "")
            ink(f"{one['count']:>3} ", "bold")
            if bar >= 4:
                _meter(ink, one["count"] / widest, bar)(" ")
            ink(f"+{one['newHere']}", "$muted")
            listing.add_option(Option(ink.content(), id=f"track-{one['tier']}"))
        listing.highlighted = next(i for i, one in enumerate(rows) if one["tier"] == self.tier)
        box = self.query_one("#scripture-tracks", Panel)
        box.border_subtitle = "readings · +new here · t next" if width >= 34 else "+new · t next"

    def draw_periods(self) -> None:
        listing = self.query_one("#scripture-period-list", OptionList)
        width = self._width(listing, 40) - 1
        rows = self.opening["periods"]
        rank = next(i for i, one in enumerate(self.opening["tracks"]) if one["tier"] == self.tier)
        peak = max(max(count or 0 for count in one["counts"]) for one in rows) or 1
        # A label is worth more than a meter: under 36 columns the meter goes
        # and the counts stay (each track's count is in the period's header).
        bar = 10 if width >= 40 else 8 if width >= 36 else 0
        label = width - 1 - 2 - 1 - 1 - (bar + 1 if bar else 0) - 3
        here = self.reading["n"] if self.view == "reading" and self.reading else (
            self.n if self.view == "period" else None)
        listing.clear_options()
        for one in rows:
            counts = [count or 0 for count in one["counts"]]
            held = counts[rank] if rank < len(counts) else 0
            ink = Ink()
            ink("▸" if one["n"] == here else " ", "bold $hotkey")
            ink(f"{one['n']:>2} ", "$muted")
            ink(f"{_clip(one['label'], label):<{label}} ", "bold" if one["n"] == here else "")
            if bar:
                # Each track's share, cumulative: a track that adds readings
                # here adds at least one cell, so no depth is drawn as nothing.
                edges, edge, before = [], 0, 0
                for count in counts:
                    edge = min(bar, max(edge + (1 if count > before else 0), round(count / peak * bar)))
                    edges.append(edge)
                    before = count
                start = 0
                for layer, end in enumerate(edges):
                    if end > start:
                        ink(LAYERS[min(layer, len(LAYERS) - 1)] * (end - start),
                            "$scripture-color" if layer <= rank else "$muted")
                    start = max(start, end)
                ink(" " * (bar - start) + " ")
            ink(f"{held:>3}" if held else "  —", "bold" if held else "$muted")
            listing.add_option(Option(ink.content(), id=f"period-{one['n']}", disabled=not held))
        target = self.n
        index = next((i for i, one in enumerate(rows) if one["n"] == target), 0)
        if listing.highlighted != index:
            listing.highlighted = index
        box = self.query_one("#scripture-periods", Panel)
        box.retitle(f"periods · {self.track['label']}")
        # The glyphs' legend; a period's own header names each track with its count.
        glyphs = " ".join(LAYERS[: min(len(LAYERS), len(self.opening["tracks"]))])
        box.border_subtitle = f"{glyphs}: each track, smallest first" if bar else "readings in this track"

    def draw_readings(self, n: int, *, follow: bool = False) -> None:
        listing = self.query_one("#scripture-reading-list", OptionList)
        width = self._width(listing, 40) - 1
        entries = self.entries(n)
        self.listed = n
        listing.clear_options()
        rank = self.track.get("rank", 0)
        tiers = [one["tier"] for one in self.opening["tracks"]]
        hand = self.order if self.view == "reading" else None
        digits = len(str(self.track.get("count", 0)))
        indent = 2 + digits + 1
        for entry in entries:
            ink = Ink()
            ink("▶ " if entry["order"] == hand else "  ", "bold $hotkey")
            ink(f"{entry['index']:>{digits}} ", "$muted")
            mark = ""
            if entry["badge"]:
                mark = BADGES[min(tiers.index(entry["badge"]["tier"]), len(BADGES) - 1)]
            ink(_clip(entry["title"], width - indent - (2 if mark else 0)), "bold" if entry["order"] == hand else "")
            if mark:
                ink(f" {mark}", "$scripture-color")
            ink.line()
            ink(" " * indent)(_clip(entry["reference"], width - indent), "$muted")
            listing.add_option(Option(ink.content(), id=f"reading-{entry['order']}"))
        index = next((i for i, one in enumerate(entries) if one["order"] == hand), None) \
            if follow and hand is not None else None
        if entries:
            listing.highlighted = index if index is not None else 0
        period = self.period(n)
        box = self.query_one("#scripture-readings", Panel)
        box.retitle(f"{period['label']}" if period else "readings")
        smaller = self.opening["tracks"][:rank]
        legend = " · ".join(f"{BADGES[i]} also {one['label']}" for i, one in enumerate(smaller[:len(BADGES)]))
        box.border_subtitle = legend if legend and len(legend) <= width else (
            f"{len(entries)} readings" if entries else "")

    # --- the page --------------------------------------------------------------

    def where(self) -> str:
        if not self.track:
            return ""
        label = self.track["label"]
        if self.view == "reading" and self.reading:
            return (f"{label} · {self.reading['index']}/{self.reading['count']} {self.reading['title']}"
                    f" · {self.reading['bible']['label']}")
        if self.view == "period":
            period = self.period(self.n)
            return f"{label} · {period['label']}" if period else label
        return f"{self.track['heading']} · before you begin"

    def draw_head(self) -> None:
        box = self.query_one("#scripture-head", Panel)
        text = self.query_one("#scripture-head-text", Static)
        width = self._width(text, 80)
        ink = Ink()
        track = self.track
        if self.opening.get("warning"):
            ink.line(self.opening["warning"], "bold $warning")
        if self.view == "reading" and self.reading:
            reading = self.reading
            box.retitle(f"{track['heading']} › {reading['period']}")
            ink(reading["title"], "bold")("   ")(reading["reference"], "bold $scripture-color").line()
            position = " · ".join(reading["position"])
            meta = " · ".join(reading["bible"]["meta"])
            if len(position) + 3 + len(meta) <= width:
                ink(f"{position} · {meta}", "$muted")
            else:
                ink.line(position, "$muted")(meta, "$muted")
            if not self.has_class("narrow"):
                _meter(ink.line(), reading["index"] / reading["count"], max(4, width - 12))
                ink(f"  {reading['index']}/{reading['count']}", "bold")
            box.border_subtitle = literal(reading["badge"]["title"]) if reading["badge"] else ""
        elif self.view == "period" and self.period(self.n):
            period = self.period(self.n)
            box.retitle(track["heading"])
            ink.line(period["label"], "bold $scripture-color")
            ink.line(period["meta"], "$muted")
            row = next((one for one in self.opening["periods"] if one["n"] == period["n"]), None)
            if row:
                for at, one in enumerate(self.opening["tracks"]):
                    count = row["counts"][at] if at < len(row["counts"]) else None
                    if at:
                        ink(" · ", "$muted")
                    ink(f"{LAYERS[min(at, len(LAYERS) - 1)]} {one['label']} ",
                        "$scripture-color" if one["tier"] == self.tier else "$muted")
                    ink(str(count) if count else "—", "bold" if one["tier"] == self.tier else "")
            box.border_subtitle = "readings in this period at each depth"
        else:
            box.retitle(self.opening.get("title") or "The Story of Salvation")
            ink(track["heading"], "bold $scripture-color")("   ")(track["figures"], "bold").line()
            ink.line(track["lede"], "italic")
            day = track["pacing"][0]
            ink(f"{day['pace']}: ", "$muted")(day["takes"])
            ink(f"   ·   reading in {self.bible_row()['label']}", "$muted")
            held = self.entry(self.order)
            if held:
                box.border_subtitle = literal(f"→ returns to reading {held['index']}")
            elif track.get("begin"):
                box.border_subtitle = "→ begins at reading 1"
            else:
                box.border_subtitle = ""
        text.update(ink.content())

    def draw_page(self) -> None:
        page = self.query_one("#scripture-page", ScrollPanel)
        page.remove_children()
        if self.view == "reading" and self.reading:
            widgets = self.page_reading()
        elif self.view == "period" and self.period(self.n):
            widgets = self.page_period()
        else:
            widgets = self.page_orientation()
        page.mount_all(widgets)
        page.scroll_home(animate=False)

    @staticmethod
    def _prose(blocks: list[dict], style: str = "") -> list[Static]:
        """The plan's own prose, as the model paragraphs it: an indented
        paragraph is an aside, and the words are never altered."""
        out = []
        for block in blocks:
            aside = "prose-aside" in block.get("classes", [])
            out.append(Static(runs(Ink(), block, style=style).content(), classes="sc-aside" if aside else "sc-p"))
        return out

    def page_orientation(self) -> list[Static]:
        """The track's orientation, before any scripture.

        The page (track.js:355-407) orders it: what the track is, where to
        begin, how long it takes, what it leaves out, the periods. Here the
        plan's account of what it leaves out comes first and in full, because
        that is the obligation the plan sets itself ("This account belongs at
        the front and not in a footnote", plan.js:181): the header above
        already says what the track is and how long a reading a day takes.
        The rest follows in the page's order, every sentence the page's.
        """
        track = self.track
        page = self.query_one("#scripture-page", ScrollPanel)
        page.retitle("orientation")
        page.border_subtitle = literal(f"{track['heading']} · ← → read · [ ] periods")
        out: list[Static] = []
        out.append(Static(Ink()("Before you begin").content(), classes="sc-h1"))  # page: track.js:356
        out.append(Static(Ink()("What it leaves out").content(), classes="sc-h2"))  # track.js:391
        out.append(Static(Ink()(track["nesting"], "italic").content(), classes="sc-lead"))
        out += self._prose(self.opening["omissions"])
        out.append(Static(Ink()("What this track is").content(), classes="sc-h2"))  # track.js:358
        out.append(Static(Ink()(track["figures"], "$muted").content(), classes="sc-lead"))
        out += self._prose(track["description"])
        begin = track.get("begin")
        if begin:
            ink = Ink()("▶ ", "bold $scripture-color")(begin["said"], "bold")
            held = self.entry(self.order)
            if held and held["index"] > 1:
                # page: track.js:374-379
                ink.line()("  Or return to reading ")(f"{held['index']} — {held['title']}", "bold")(".")
            hand = held or self.entry(begin["order"])
            if hand:
                ink.line()(f"  → reads {hand['index']}. {hand['title']}", "$muted")
            out.append(Static(ink.content(), classes="sc-p"))
        out.append(Static(Ink()("How long it takes").content(), classes="sc-h2"))  # track.js:385
        out.append(Static(Ink()("At one reading a sitting, and counting nothing else.").content(),  # track.js:386
                          classes="sc-lead"))
        pace = max(len("Pace"), *(len(row["pace"]) for row in track["pacing"]))
        table = Ink()(f"{'Pace':<{pace}}   ", "bold $muted").line("Finishes in", "bold $muted")  # :305-307
        for row in track["pacing"]:
            table(f"{row['pace']:<{pace}}   ").line(row["takes"], "bold")
        out.append(Static(table.content(), classes="sc-table"))
        out.append(Static(Ink()("The twelve periods").content(), classes="sc-h2"))  # track.js:402
        out.append(Static(Ink()(  # page: track.js:403-405
            "The periods are the spine of the story. Each holds its own readings in sequence, "
            "and each opens with an account of the arc it covers.").content(), classes="sc-lead"))
        for period in track["periods"]:
            ink = Ink()(f"{period['index']:>2}  ", "$muted")(period["label"], "bold $scripture-color").line()
            ink("    ")(period["contents"], "$muted")
            if period["line"]:
                ink.line()("    ")(period["line"])
            out.append(Static(ink.content(), classes="sc-p"))
        text = self.opening.get("text")
        if text:
            out.append(Static(Ink()("Text and numbering").content(), classes="sc-h2"))  # page: plan.js:194
            width = max(len(term) for term, _ in text["rows"])
            facts = Ink()
            for term, value in text["rows"]:
                facts(f"{term:<{width}}   ", "bold $muted").line(value)
            out.append(Static(facts.content(), classes="sc-table"))
            out.append(Static(Ink()(text["lead"]).content(), classes="sc-lead"))
        return out

    def page_period(self) -> list[Static]:
        period = self.period(self.n)
        page = self.query_one("#scripture-page", ScrollPanel)
        page.retitle(period["label"])
        page.border_subtitle = "[ ] or ← → periods · enter on a reading to read it"
        out = self._prose(period["summary"])
        if period["badged"]:
            out.append(Static(Ink()(  # page: track.js:488-490
                "A badge marks a reading that also belongs to a smaller track: those are the hinges "
                "the shorter readings of the plan are built from.", "italic").content(), classes="sc-lead"))
        tiers = [one["tier"] for one in self.opening["tracks"]]
        for entry in self.entries(period["n"]):
            ink = Ink()(f"{entry['index']}. ", "$muted")(entry["title"], "bold")
            if entry["badge"]:
                mark = BADGES[min(tiers.index(entry["badge"]["tier"]), len(BADGES) - 1)]
                ink(f"  {mark} {entry['badge']['label']}", "$scripture-color")
            ink.line()(entry["reference"], "$scripture-color")
            if entry["note"]:
                ink.line()(entry["note"], "$muted")
            out.append(Static(ink.content(), classes="sc-p"))
        places = [one["n"] for one in self.track["periods"]]
        at = places.index(period["n"])
        steps = Ink()
        before = self.period(places[at - 1]) if at > 0 else None
        after = self.period(places[at + 1]) if at + 1 < len(places) else None
        steps("Before  ", "bold $muted")  # page: track.js:452-465
        steps.line(before["label"] if before else "The story starts here.", "" if before else "italic")
        steps("After   ", "bold $muted")
        steps(after["label"] if after else "The story ends here.", "" if after else "italic")
        out.append(Static(steps.content(), classes="sc-rule"))
        return out

    def page_reading(self) -> list[Static]:
        reading = self.reading
        page = self.query_one("#scripture-page", ScrollPanel)
        bible = reading["bible"]
        page.retitle(f"{reading['title']} · {bible['label']}")
        out: list[Static] = []
        if self.notice:
            out.append(Static(Ink()(self.notice).content(), classes="sc-diverted"))
        if reading["note"]:
            out.append(Static(Ink()("Why this reading is here", "bold $scripture-color").line()  # track.js:573
                              (reading["note"]).content(), classes="sc-why"))
        verses = 0
        language = ""
        for block in reading["blocks"]:
            names = block.get("classes", [])
            if "notice" in names:
                kind = "sc-notice"
            elif "chapter-mark" in names:
                kind = "sc-chapter"
            elif "citation-ref-recast-only" in names:
                kind = "sc-recast"
            elif "passage" in names:
                kind = "sc-passage"
                language = language or block.get("lang") or ""
                verses += sum(1 for run in block.get("runs", []) if "verse-num" in run.get("classes", []))
            else:
                kind = "sc-p"
            out.append(Static(runs(Ink(), block, verse_lines=self.verse_lines).content(), classes=kind))
        ink = Ink()
        for side in (reading["before"], reading["after"]):  # track.js:524-550
            ink(f"{side['side']:<7} ", "bold $muted")
            if side.get("none"):
                ink.line(side["none"], "italic")
                continue
            ink(side["title"], "bold")("  ")(side["reference"], "$scripture-color")
            if side["crossing"]:
                ink("  ")(side["crossing"], "italic $muted")
            ink.line()
        ink.line()
        # page: track.js:592-595
        ink("What this track leaves out", "underline")(" (o)", "$muted")(" · ")
        ink(f"All of {reading['period']}", "underline")(" (p)", "$muted")
        out.append(Static(ink.content(), classes="sc-rule"))
        said = [f"{verses} verse{'s' if verses != 1 else ''}" if verses else "no verses shown"]
        if language and language != bible["language"]:
            said.append(f"set as {language}")
        elif bible["languageName"]:
            said.append(bible["languageName"])
        said.append("v verse per line" if not self.verse_lines else "v running text")
        page.border_subtitle = " · ".join(said)
        return out
