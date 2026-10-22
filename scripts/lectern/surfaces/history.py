"""How the Missal Changed: book states through time, the recorded lines, the catalogue.

Three of the /history/ page's views, each asked of the page's own model
through `adapters/history.js`:

- the timeline ("Books through time"): one tradition's dated book states on
  the page's year axis, joined only by recorded transitions;
- the recorded historical lines: the act map, one route panel per line;
- the Eucharistic book catalogue: every source record, filtered by record
  group and by every word typed.

Literal text appears only behind the page's gates: a native text after its
routing and payload checks, a witness comparison after its own.
"""
from __future__ import annotations

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge
from ..dialogs import Ask, Pick, Reading
from ..repo import Refused
from ..surface import Surface
from ..timeline import Doc, Drawing, paint_map, paint_timeline
from ..widgets import Ink, Panel, ScrollPanel

ADAPTER = "history"
TIGHT = 90  # columns under which a side pane is swapped in by `f` rather than shown beside
VIEWS = (("timeline", "t", "timeline"), ("map", "m", "recorded lines"), ("catalogue", "k", "catalogue"))
TONE = "$history-color"

# Which keys belong to which view; the rest belong to all three.
VIEW_ACTIONS = {
    "window": "timeline", "tradition": "timeline", "leads": "timeline", "native": "timeline",
    "slice": "map", "state": "map", "unit": "map", "junctions": "map",
    "search": "catalogue", "group": "catalogue",
}

# The page's legend for the timeline (history/index.html, "Books through time"),
# in the terminal's glyphs: each mark is also said in words.
TIMELINE_LEGEND = (
    ("●", "Documented state"), ("◇", "Provisional lead"), ("├──┤", "Date uncertainty, not how long the book was in use"),
    ("◁ ▷", "a bracket running past the edge of the window"),
    ("○", "a hollow endpoint: a continuation outside this view"),
    ("━", "text collation"), ("─", "primary description"), ("╌", "scholarly description"),
    ("┄", "bibliographic succession or provisional lead"),
    ("▶ ▼ ▲", "the arrow points to the receiving state"),
)
MAP_MARKS = {"promulgated": "●", "printed": "○", "unstated": "◌", "reception": "◉",
             "stated": "┃", "attributed": "│", "sequence": "┆", "broken": "⋮", "": "·"}


def _three(ink: Doc, value: dict, indent: str = "") -> None:
    """One of three states, never two: words, words withheld (with why), or words
    this record does not carry. The glyph says which without colour."""
    state = value.get("state")
    if state == "present":
        ink(indent)("┃ ", f"{TONE}")(value["text"]).line()
    elif state == "withheld":
        ink(indent)("⊘ ", "bold $warning")(value["text"], "italic $warning").line()
    else:
        ink(indent)("◌ ", "$text-muted")(value["text"], "italic $text-muted").line()


def _citations(ink: Doc, rows: list[dict], indent: str = "  ") -> None:
    for row in rows:
        ink(indent)("◦ ", TONE)(row["title"], "bold")
        if row.get("url"):
            ink(f"  {row['url']}", "underline $text-muted")
        ink.line()
        ink.line(f"{indent}  {row['locus']}")
        ink.line(f"{indent}  {row['meta']}", "$text-muted")
        if row.get("limitations"):
            ink.line(f"{indent}  {row['limitations']}", "italic $text-muted")


def _transition(ink: Doc, view: dict, *, full: bool = True) -> None:
    ink(view["heading"], f"bold {TONE}")("  " + view["meta"], "$text-muted").line()
    ink.line(view["summary"])
    ink(f"{view['from']['key']} ", "$text-muted")(view["from"]["label"])
    ink("  →  ", f"bold {TONE}")(f"{view['to']['key']} ", "$text-muted").line(view["to"]["label"])
    for change in view["changes"]:
        ink.line(f"  {change['component']}", "bold underline")
        ink.line(f"  {change['before']}")
        ink.line(f"    {change['before_locus']}", "$text-muted")
        ink.line(f"  {change['after']}")
        ink.line(f"    {change['after_locus']}", "$text-muted")
        if full:
            _citations(ink, change["evidence"], "    ")
    if view["no_changes"]:
        ink.line(view["no_changes"], "italic $text-muted")
    ink.line(view["limitations"], "italic $text-muted")
    if full:
        _citations(ink, view["evidence"])
    for row in view["comparisons"]:
        ink("  c ", "bold $hotkey").line(row["label"], "underline")


def stage_text(view: dict, *, full: bool = True) -> Doc:
    """The page's evidence panel for one state (history.js showDetail)."""
    ink = Doc()
    if view.get("missing"):
        return ink.line(view["missing"], "bold $warning")
    ink.line(view["heading"], f"bold {TONE}")
    ink.line(view["tradition"], "italic $text-muted")
    ink.line(view["date"], "bold")
    ink.line(view["bounds"], "$text-muted")
    ink.line(view["coverage"], "$text-muted")
    if view["routing"]:
        ink.line(view["routing"], "bold $error")
    for row in view["native"]:
        ink("  n ", "bold $hotkey").line(row["label"], "underline")
    ink.line()
    ink.line(view["summary"])
    for name in ("scope", "parts", "witness", "reception"):
        ink.line(view[name])
    ink.line(view["limitations"], "italic $text-muted")
    if full:
        _citations(ink, view["evidence"])
        for row in view["witnesses"]:
            ink("  ▸ ", TONE)(row["label"], "italic $warning" if row.get("missing") else "")
            if row.get("act_ref"):
                ink("  · recorded act and text state", "$text-muted")
            ink.line()
    ink.line()
    ink.line("What changed into this state", "bold underline")
    if not view["incoming"]:
        ink.line(view["incoming_none"], "italic $text-muted")
    for transition in view["incoming"]:
        _transition(ink, transition, full=full)
        ink.line()
    ink.line("What follows from this state", "bold underline")
    if not view["outgoing"]:
        ink.line(view["outgoing_none"], "italic $text-muted")
    for transition in view["outgoing"]:
        _transition(ink, transition, full=full)
        ink.line()
    return ink


def transition_text(view: dict) -> Doc:
    ink = Doc()
    if view.get("missing"):
        return ink.line(view["missing"], "bold $warning")
    _transition(ink, view)
    return ink


def native_text(view: dict) -> Doc:
    """The page's source-text disclosure (history.js renderNativeText)."""
    ink = Doc()
    if view.get("error"):
        return ink.line(view["error"], "bold $error")
    ink.line(view["title"], f"bold {TONE}")
    ink.line(view["stage"], "italic $text-muted")
    ink.line(view["extent"], "bold")
    ink.line(view["scope"])
    if view["excluded"]:
        ink.line(view["excluded_heading"], "bold")
        for row in view["excluded"]:
            ink.line(f"  · {row}")
    ink.line()
    for unit in view["units"]:
        heading = f"{unit['heading']} · {unit['language']}"
        if unit["direction"] == "rtl":
            heading += " · right to left"
        ink.line(heading, f"bold {TONE}")
        ink.line(unit["text"])
        ink(f"  {unit['source']} · {unit['locator']}", "$text-muted")
        if unit.get("url"):
            ink(f"  {unit['url']}", "underline $text-muted")
        ink.line().line()
    for row in view["rights"]:
        ink.line(row["line"], "bold")
        if row["normalization"]:
            ink.line("Transcription and normalization", "underline")
            ink.line(row["normalization"], "$text-muted")
    return ink


def comparison_text(view: dict) -> Doc:
    """The page's witness comparison (history.js renderComparison)."""
    ink = Doc()
    if view.get("error"):
        return ink.line(view["error"], "bold $error")
    ink.line(view["identity"], f"bold {TONE}")
    ink.line(view["basis"])
    ink.line(view["caveat"], "italic $warning").line()
    for name in ("left", "right"):
        side = view[name]
        ink.line(side["heading"], "bold")
        ink.line(side["dates"], "$text-muted")
        ink.line(side["text"])
        ink.line(side["count"], "italic $text-muted")
        for member in side["members"]:
            ink.line("  · " + " — ".join(member), "$text-muted")
        ink.line()
    ink.line(view["diff_heading"], "bold underline")
    ink.line(view["diff_legend"], "italic $text-muted")
    for row in view["diff"].split("\n"):
        style = "$success" if row.startswith("+") and not row.startswith("+++") else \
            "$error" if row.startswith("-") and not row.startswith("---") else "$text-muted"
        ink.line(row, style)
    ink.line()
    for row in view["limitations"]:
        ink.line(row, "italic $text-muted")
    if view["sources"]:
        ink.line().line("Source records and access", "bold underline")
        for row in view["sources"]:
            ink(f"  · {row['title']}")
            if row.get("url"):
                ink(f"  {row['url']}", "underline $text-muted")
            ink.line()
    return ink


def _field_rows(ink: Doc, fields: list[dict]) -> None:
    for field in fields:
        ink.line(f"    {field['name']}", "$text-muted")
        _three(ink, field["before"], "      ")
        ink("      → ", TONE).line()
        _three(ink, field["after"], "      ")


def _unit_card(ink: Doc, card: dict) -> None:
    ink(f"  {card['title']}", "bold")(f"  {card['kinds']}", f"italic {TONE}").line()
    ink.line(f"    {card['where']}", "$text-muted")
    if card.get("fields") is not None:
        _field_rows(ink, card["fields"])
        if card.get("same"):
            ink.line(f"    {card['same']}", "italic $text-muted")
    elif card.get("standing"):
        _three(ink, card["standing"]["incipit"], "    ")
        if card["standing"]["text"]:
            ink.line(f"    {card['standing']['text']}")
    if card.get("marker"):
        ink.line(f"    {card['marker']}", "$warning")
    for row in card.get("basis") or []:
        ink(f"    {row['kind']} ", f"bold {TONE}").line(row["text"], "$text-muted")


def station_text(view: dict, *, full: bool = True) -> Doc:
    """The page's station panel (history.js open and renderChanges)."""
    ink = Doc()
    if view.get("missing"):
        return ink.line(view["missing"], "bold $warning")
    ink.line(view["title"], f"bold {TONE}")
    for name, value in view["facts"]:
        ink(f"{name}: ", "bold")(value).line()
    if view.get("receptions"):
        ink.line().line("Documented reception", "bold underline")
        ink.line(view["reception_note"], "italic $text-muted")
        for row in view["receptions"]:
            ink.line(row["title"], "bold")
            for name, value in row["facts"]:
                ink(f"  {name}: ", "bold").line(value)
    for name in ("kind_note", "gap_note", "departures", "parents_note"):
        if view.get(name):
            ink.line(view[name], "italic $warning" if name == "gap_note" else "italic $text-muted")
    if view.get("change_error"):
        ink.line(view["change_error"], "italic $warning")
    changes = view.get("changes")
    if changes:
        ink.line().line(changes["summary"], "bold")
        if changes.get("printed_caveat"):
            ink.line(changes["printed_caveat"], "italic $warning")
        if changes["rests_on"]:
            ink.line().line("On what this station rests", "bold underline")
            for title, said in changes["rests_on"]:
                ink.line(title, "bold")
                ink.line(" ".join(said.split()), "$text-muted")
        if changes["groups"]:
            ink.line().line(changes["groups_title"], "bold underline")
            for card in changes["groups"] if full else changes["groups"][:6]:
                ink(f"  {card['title']}", "bold")(f"  {card['kinds']}", f"italic {TONE}").line()
                ink.line(f"    {card['where']}", "$text-muted")
                _field_rows(ink, card["fields"])
                for row in card["basis"]:
                    ink(f"    {row['kind']} ", f"bold {TONE}").line(row["text"], "$text-muted")
            if not full and len(changes["groups"]) > 6:
                ink.line(f"  … {len(changes['groups']) - 6} more; enter reads the station whole", "italic $text-muted")
        if changes["units"]:
            ink.line().line(changes["units_title"], "bold underline")
            for card in changes["units"] if full else changes["units"][:8]:
                _unit_card(ink, card)
            if not full and len(changes["units"]) > 8:
                ink.line(f"  … {len(changes['units']) - 8} more; enter reads the station whole", "italic $text-muted")
        if changes.get("unestablished"):
            ink.line().line("Left unestablished", "bold underline")
            ink.line(changes["unestablished_note"], "italic $text-muted")
            for row in changes["unestablished"]:
                ink.line(f"  {row['unit']}", "bold")
                ink.line(f"    {row['marker']}", "$warning")
        if changes.get("empty"):
            ink.line(changes["empty"], "italic $text-muted")
    if view.get("state_label"):
        ink.line()("  x ", "bold $hotkey").line(view["state_label"], "underline")
    return ink


class History(Surface):
    key = "7"
    label = "History"
    HELP = (
        ("t / m / k", "timeline · recorded lines (the act map) · source catalogue"),
        ("↑ / ↓", "move through the states, transitions, stations or records"),
        ("enter", "read the chosen item whole (n / p walk the list)"),
        ("click", "choose a state, transition, station or record"),
        ("← / →", "timeline: earlier / later years, by half the window"),
        ("+ / -", "timeline: zoom in / out on the years"),
        ("a / y", "timeline: all recorded years / this tradition's full history"),
        ("r", "timeline: choose a tradition, or all traditions on one axis"),
        ("l", "timeline: include or leave out provisional leads"),
        ("L", "timeline: read it as a chronological list, or as the year-axis map again"),
        ("n", "timeline: read the chosen state's source text, behind the page's checks"),
        ("c", "read a witness comparison (linked from the chosen transition, or any)"),
        ("s", "lines: the next recorded slice (latin-missal, Holy Week, the Code)"),
        ("x", "lines: the recorded units as they stood after the chosen act"),
        ("u", "lines: follow one prayer (or canon) through the record"),
        ("w", "lines: where the lines part"),
        ("/ , g", "catalogue: search every word / choose a record group"),
        ("i", "coverage limits and configured text sets"),
        ("f", "focus: the drawing or list alone, full width; again to restore (under 90 columns: swap in the side panes)"),
    )
    BINDINGS = [
        Binding("t", "view('timeline')", "books through time"),
        Binding("m", "view('map')", "recorded lines"),
        Binding("k", "view('catalogue')", "source catalogue"),
        Binding("r", "tradition", "choose tradition"),
        Binding("n", "native", "read source text"),
        Binding("c", "comparison", "read comparison"),
        Binding("left", "window('earlier')", "show earlier years", show=False),
        Binding("right", "window('later')", "show later years", show=False),
        Binding("plus,equals_sign", "window('zoom-in')", "zoom in on the years", show=False),
        Binding("minus", "window('zoom-out')", "zoom out from the years", show=False),
        Binding("a", "window('all-years')", "show all recorded years", show=False),
        Binding("y", "window('local-years')", "show this tradition's full history", show=False),
        Binding("l", "leads", "include or leave out provisional leads", show=False),
        Binding("L", "listing", "read the timeline as a chronological list", show=False),
        Binding("s", "slice", "show the next recorded slice", show=False),
        Binding("x", "state", "read the record as it stood after the chosen act", show=False),
        Binding("u", "unit", "follow one prayer or canon through the record", show=False),
        Binding("w", "junctions", "read where the recorded lines part", show=False),
        Binding("slash", "search", "search the source records", show=False),
        Binding("g", "group", "choose a record group", show=False),
        Binding("i", "limits", "read the coverage limits and configured text sets", show=False),
    ]
    DEFAULT_CSS = """
    History #history-views { height: 1; padding: 0 1; }
    History #history-status { height: auto; max-height: 3; padding: 0 1; color: $text-muted; }
    History .history-view { height: 1fr; }
    History .history-side { width: 54; }
    History #history-notes { height: 2fr; }
    History #history-detail { height: 3fr; }
    History #history-map-legend { height: 1fr; }
    History #history-station { height: 3fr; }
    History #history-record-list { height: 1fr; }
    """
    # Frames that must outrank the shared rules: hidden views, focus, narrow.
    CSS = """
    .history .history-view.hidden { display: none; }
    .history #history-list-box { display: none; }
    .history.listing #history-list-box { display: block; }
    .history.listing #history-chart-box { display: none; }
    .history.focus .history-side { display: none; }
    .history.narrow .history-side { width: 40; }
    .history OptionList { scrollbar-color: $history-color 45%; scrollbar-color-hover: $history-color 75%;
        scrollbar-color-active: $history-color; scrollbar-background: $surface; }
    .history Drawing { scrollbar-color: $history-color 45%; scrollbar-color-hover: $history-color 75%;
        scrollbar-color-active: $history-color; scrollbar-background: $surface; }
    .history.narrow #history-status { max-height: 2; }
    .history.tight .history-side { display: none; }
    .history.tight.focus .history-side { display: block; width: 1fr; }
    .history.tight.focus #history-chart-box, .history.tight.focus #history-lines-box,
    .history.tight.focus #history-records { display: none; }
    """

    def on_resize(self, event) -> None:
        super().on_resize(event)
        # Under 90 columns the side panes give way to the drawing; f swaps them in.
        self.set_class(event.size.width < TIGHT, "tight")

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.view = "timeline"
        self.opening: dict = {}
        self.state: dict = {}
        self.timeline: dict = {}
        self.chosen: tuple[str, str] | None = None
        self.detail: dict = {}
        self.slice = ""
        self.map: dict = {}
        self.station: dict = {}
        self.filter = {"family": "", "q": ""}
        self.records: list[str] = []
        self.catalogue_view: dict | None = None
        self.record: dict = {}
        self.pending: dict = {}

    # --- building --------------------------------------------------------

    def build(self) -> None:
        self.mount(
            Static("", id="history-views"),
            Static("", id="history-status"),
            Horizontal(
                Panel(Drawing(paint_timeline, "history", id="history-chart"), title="timeline", key="ᵗ",
                      id="history-chart-box"),
                ScrollPanel(Static("", id="history-list-text"), title="chronological reading list",
                            id="history-list-box"),
                Vertical(
                    ScrollPanel(Static("", id="history-detail-text"), title="state", id="history-detail"),
                    ScrollPanel(Static("", id="history-notes-text"), title="not yet established", id="history-notes"),
                    classes="history-side",
                ),
                id="history-timeline", classes="history-view",
            ),
            Horizontal(
                Panel(Drawing(paint_map, "history", id="history-lines"), title="recorded lines", key="ᵐ",
                      id="history-lines-box"),
                Vertical(
                    ScrollPanel(Static("", id="history-station-text"), title="station", id="history-station"),
                    ScrollPanel(Static("", id="history-map-legend-text"), title="legend", id="history-map-legend"),
                    classes="history-side",
                ),
                id="history-map", classes="history-view hidden",
            ),
            Horizontal(
                Panel(OptionList(id="history-record-list"), title="catalogue", key="ᵏ", id="history-records"),
                Vertical(
                    ScrollPanel(Static("", id="history-record-text"), title="record", id="history-record"),
                    classes="history-side",
                ),
                id="history-catalogue", classes="history-view hidden",
            ),
        )
        self.show_views()
        self.query_one("#history-status", Static).update(Ink()("Reading the catalogue…", "italic").content())
        self.start()

    @work(thread=True, exclusive=True, group="history-start")
    def start(self) -> None:
        try:
            opening = bridge.call(ADAPTER, "opening")
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.opened_with, opening)

    def opened_with(self, opening: dict) -> None:
        self.opening = opening
        self.slice = self.slice or opening["default_slice"]
        pending, self.pending = self.pending, {}
        if pending:
            self.follow(**pending)
        else:
            self.load_timeline({}, None)

    def fail(self, message: str) -> None:
        self.query_one("#history-status", Static).update(Ink()(message, "bold $error").content())

    # --- views -----------------------------------------------------------

    def show_views(self) -> None:
        bar = Ink()
        for name, key, words in VIEWS:
            bar(key, "bold $hotkey")
            bar(f" {words} ", f"bold reverse {TONE}" if name == self.view else TONE)
            bar("  ")
        bar("How the Missal Changed", "italic $text-muted")
        self.query_one("#history-views", Static).update(bar.content())
        for name, _, _ in VIEWS:
            self.query_one(f"#history-{name}").set_class(name != self.view, "hidden")
        # A view that went away may have held the focus; the keys follow the view shown.
        self.call_after_refresh(self.refocus)

    def action_view(self, name: str) -> None:
        if name == self.view and self.opening:
            return
        self.view = name
        self.show_views()
        self.refresh_bindings()
        if not self.opening:
            return
        if name == "timeline":
            self.show_status()
            self.query_one("#history-chart", Drawing).focus()
        elif name == "map":
            if not self.map or self.map.get("slice") != self.slice:
                self.load_map(self.slice, None)
            else:
                self.show_status()
            self.query_one("#history-lines", Drawing).focus()
        else:
            if not self.records:
                self.load_catalogue(None)
            else:
                self.show_status()
            self.query_one("#history-record-list", OptionList).focus()
        self.app.refresh_where()

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        owner = VIEW_ACTIONS.get(action)
        if owner and owner != self.view:
            return False
        return True

    def _in(self, view: str) -> bool:
        if self.view != view:
            self.action_view(view)
        return bool(self.opening)

    # --- intent ----------------------------------------------------------

    def follow(self, view: str | None = None, tradition: str | None = None, stage: str | None = None,
               slice: str | None = None, station: str | None = None, record: str | None = None,
               q: str | None = None, group: str | None = None, **_) -> None:
        if not self.opening:
            self.pending = {key: value for key, value in dict(view=view, tradition=tradition, stage=stage, slice=slice,
                                                                station=station, record=record, q=q, group=group).items()
                            if value}
            return
        if slice or station:
            self.slice = slice or self.slice
            self.view = "map"
            self.show_views()
            self.load_map(self.slice, station)
        elif record or q or group:
            self.view = "catalogue"
            self.show_views()
            self.filter = {"family": group or "", "q": q or ""}
            self.load_catalogue(record)
        else:
            self.view = view if view in ("timeline", "map", "catalogue") else "timeline"
            self.show_views()
            if self.view == "map":
                self.load_map(self.slice, None)
            elif self.view == "catalogue":
                self.load_catalogue(None)
            else:
                self.load_timeline({"tradition": tradition, "stage": stage}, "tradition" if tradition else None,
                                   keep=stage)
        self.refresh_bindings()

    def where(self) -> str:
        if self.view == "timeline" and self.timeline.get("lanes") is not None:
            lane = self.timeline["lanes"][0]["label"] if len(self.timeline["lanes"]) == 1 else "all traditions"
            state = self.timeline.get("state") or {}
            return f"timeline · {lane} · {state.get('start')}–{state.get('end')}"
        if self.view == "map" and self.map:
            return f"recorded lines · {self.map.get('slice')}"
        if self.view == "catalogue":
            return f"catalogue · {self.filter_label()}"
        return ""

    def filter_label(self) -> str:
        return (self.catalogue_view or {}).get("filter", {}).get("label", "All record groups")

    def show_status(self) -> None:
        ink = Ink()
        if self.view == "timeline" and self.timeline:
            if self.timeline.get("error"):
                ink.line(self.timeline["error"], "bold $warning")
            else:
                ink(self.timeline["status"], "bold")
                if (self.timeline.get("state") or {}).get("leads"):
                    ink("  · provisional leads included", f"bold {TONE}")
                ink.line()
                ink(self.timeline["tally"], "italic")
        elif self.view == "map" and self.map:
            ink(self.map["tally"], "bold")
        elif self.view == "catalogue" and self.catalogue_view:
            view = self.catalogue_view
            ink(view["status"], "bold")(f"  · {view['filter']['label']}", TONE)
            if view["filter"]["q"]:
                ink(f"  · every word of “{view['filter']['q']}”", TONE)
            ink.line()
            ink(view["tally"], "italic")
        self.query_one("#history-status", Static).update(ink.content())

    # --- the timeline ----------------------------------------------------

    def load_timeline(self, state: dict, move: str | None, keep: str | None = None) -> None:
        self.fetch_timeline(dict(state), move, keep)

    @work(thread=True, exclusive=True, group="history-timeline")
    def fetch_timeline(self, state: dict, move: str | None, keep: str | None) -> None:
        try:
            model = bridge.call(ADAPTER, "timeline", state, move)
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.show_timeline, model, keep)

    def show_timeline(self, model: dict, keep: str | None) -> None:
        self.timeline = model
        self.state = model.get("state") or {}
        box = self.query_one("#history-chart-box", Panel)
        drawing = self.query_one("#history-chart", Drawing)
        if model.get("error"):
            self.show_status()
            return
        lanes = model["lanes"]
        tradition = "All traditions on a shared year axis" if self.state.get("tradition") == "all" else \
            (lanes[0]["label"] if lanes else self.state.get("tradition", ""))
        box.retitle(f"timeline · {tradition}", key="ᵗ")
        box.border_subtitle = f"{model['state']['start']}–{model['state']['end']} · ← → years · + - zoom · r tradition"
        if keep is None and self.chosen and self.chosen[0] in ("stage", "transition"):
            keep = self.chosen[1]
        drawing.show(model, keep=keep)
        self.show_list(model)
        self.show_notes(model)
        self.show_status()
        self.app.refresh_where()

    def action_listing(self) -> None:
        """The page's other presentation of the same window: a chronological
        reading list, for a narrow screen or a reader moving by keys
        (history/index.html "Read as"; guidance/time-machine.md:676-677)."""
        if not self._in("timeline"):
            return
        self.toggle_class("listing")
        self.call_after_refresh(self.refocus)

    def show_list(self, model: dict) -> None:
        ink = Doc()
        ink.line(model.get("status") or "", "italic $text-muted").line()
        for lane in model.get("lanes") or []:
            ink.line(lane["label"], f"bold {TONE}")
            if lane.get("scope"):
                ink.line(lane["scope"], "$text-muted")
            if lane.get("coverage_note"):
                ink.line(lane["coverage_note"], "italic $text-muted")
            ink.line()
            for card in lane.get("cards") or []:
                ink(f"{card['key']} ", "$text-muted")(card["label"], "bold").line()
                ink.line(f"  {card['date']}", TONE)
                ink.line(f"  {card['meta']}", "$text-muted")
                if card.get("scope"):
                    ink.line(f"  {card['scope']}")
                for change in card.get("changes") or []:
                    ink.line(f"  ▶ {change['line']}", "italic")
                    ink.line(f"    {change['evidence']}", "$text-muted")
                ink.line()
        self.query_one("#history-list-text", Static).update(ink)
        box = self.query_one("#history-list-box", ScrollPanel)
        box.border_subtitle = f"{model['state']['start']}–{model['state']['end']} · L the year-axis map"

    def show_notes(self, model: dict) -> None:
        ink = Doc()
        ink.line("What this history does not yet establish", f"bold {TONE}")
        for gap in model["gaps"]:
            ink.line(gap["period"], "bold")
            ink.line(gap["missing"])
            ink.line(gap["consequence"], "italic")
            ink.line(gap["next"], "$text-muted").line()
        if not model["gaps"]:
            ink.line(model["gaps_none"], "italic $text-muted").line()
        ink.line("States without a positioned date", f"bold {TONE}")
        self._cards(ink, model["unpositioned"], model["none_recorded"])
        ink.line("Provisional leads, separate from documented states", f"bold {TONE}")
        self._cards(ink, model["provisional"], model["none_recorded"])
        if self.timeline.get("lanes"):
            for lane in self.timeline["lanes"][:1] if len(self.timeline["lanes"]) == 1 else []:
                ink.line("This tradition", f"bold {TONE}")
                ink.line(lane["scope"])
                if lane["coverage_note"]:
                    ink.line(lane["coverage_note"], "italic $text-muted")
                ink.line()
        ink.line("How to read the drawing", f"bold {TONE}")
        for mark, words in TIMELINE_LEGEND:
            ink(f"  {mark:<5} ", f"bold {TONE}").line(words)
        ink.line("Only explicitly recorded transitions connect states. Contemporary books can coexist without "
                 "descending from each other. Historical evidence and transcription coverage are independent; "
                 "“documented” does not mean the full text is available here.", "italic $text-muted")
        ink.line()
        ink.line("Stage-history limitations", f"bold {TONE}")
        for row in self.opening.get("stage_limitations", []):
            ink.line(f"· {row}", "$text-muted")
        self.query_one("#history-notes-text", Static).update(ink.content())

    @staticmethod
    def _cards(ink: Doc, cards: list[dict], none: str) -> None:
        if not cards:
            ink.line(none, "italic $text-muted").line()
            return
        for card in cards:
            ink(f"{card['key']} ", "$text-muted")(card["label"], "bold").line()
            ink.line(f"  {card['date']}", "$text-muted")
            ink.line(f"  {card['meta']}", "$text-muted")
        ink.line()

    @on(Drawing.Chosen, "#history-chart")
    def chose_in_timeline(self, event: Drawing.Chosen) -> None:
        self.chosen = (event.item.kind, event.item.key)
        self.fetch_detail(event.item.kind, event.item.key, False)

    @on(Drawing.Opened, "#history-chart")
    def opened_in_timeline(self, event: Drawing.Opened) -> None:
        self.chosen = (event.item.kind, event.item.key)
        self.fetch_detail(event.item.kind, event.item.key, True)

    @work(thread=True, exclusive=True, group="history-detail")
    def fetch_detail(self, kind: str, key: str, read: bool) -> None:
        try:
            view = bridge.call(ADAPTER, "stage" if kind == "stage" else "transition", key)
        except Refused as refusal:
            view = {"missing": str(refusal)}
        self.deliver(self.show_detail, kind, view, read)

    def show_detail(self, kind: str, view: dict, read: bool) -> None:
        self.detail = {"kind": kind, **view}
        box = self.query_one("#history-detail", ScrollPanel)
        ink = stage_text(view, full=False) if kind == "stage" else transition_text(view)
        self.query_one("#history-detail-text", Static).update(ink.content())
        box.retitle(f"{'state' if kind == 'stage' else 'transition'} · {view.get('key', '')}")
        box.border_subtitle = "enter read whole" + (" · n source text" if view.get("native") else "")
        box.scroll_home(animate=False)
        if read:
            self.read_detail()

    def read_detail(self) -> None:
        view = self.detail
        if not view:
            return
        kind = view.get("kind")
        ink = stage_text(view) if kind == "stage" else transition_text(view)
        title = f"{view.get('heading', view.get('key', ''))}"

        def walked(step: str | None) -> None:
            drawing = self.query_one("#history-chart", Drawing)
            if step in ("next", "previous"):
                drawing.action_move(1 if step == "next" else -1)
                item = drawing.current()
                if item:
                    self.chosen = (item.kind, item.key)
                    self.fetch_detail(item.kind, item.key, True)

        self.app.push_screen(Reading(title, ink.content(), "esc close · n next · p previous"), walked)

    def action_window(self, move: str) -> None:
        if not self._in("timeline") or not self.state:
            return
        self.load_timeline(self.state, move)

    def action_leads(self) -> None:
        if not self._in("timeline") or not self.state:
            return
        state = dict(self.state)
        state["leads"] = not state.get("leads")
        self.load_timeline(state, None)

    def action_tradition(self) -> None:
        if not self._in("timeline"):
            return
        offers = [("all", "All traditions on a shared year axis")]
        offers += [(row["id"], f"{row['label']}  ·  {row['stages']} states") for row in self.opening["traditions"]]

        def picked(value) -> None:
            if value:
                self.chosen = None
                self.load_timeline({**self.state, "tradition": value}, "tradition")

        self.app.push_screen(Pick("tradition or recension", offers,
                                  "Each lane names one tradition or recension. The list is the record's own order; "
                                  "nothing is ranked."), picked)

    def action_native(self) -> None:
        if not self._in("timeline"):
            return
        view = self.detail
        if not view or view.get("kind") != "stage":
            self.app.notify("Choose a state on the timeline first; a source text belongs to a state.")
            return
        if view.get("routing"):
            self.app.notify(view["routing"], severity="error")
            return
        offers = view.get("native") or []
        if not offers:
            self.app.notify(f"{view.get('key')} carries no checked source text. {view.get('coverage', '')}")
            return
        if len(offers) == 1:
            self.fetch_native(view["id"], 0)
            return
        self.app.push_screen(Pick("source text", [(str(row["index"]), row["label"]) for row in offers],
                                  "Each constituent is checked and fetched on its own."),
                             lambda value: value is not None and self.fetch_native(view["id"], int(value)))

    @work(thread=True, exclusive=True, group="history-native")
    def fetch_native(self, stage: str, index: int) -> None:
        try:
            view = bridge.call(ADAPTER, "native", stage, index)
        except Refused as refusal:
            view = {"error": str(refusal)}
        self.deliver(self.read_native, view)

    def read_native(self, view: dict) -> None:
        title = f"{view.get('title') or 'source text'}"
        self.app.push_screen(Reading(title, native_text(view).content(),
                                     "esc close · the rights line and normalization follow the text",
                                     walks=False))

    # --- comparisons -----------------------------------------------------

    def action_comparison(self) -> None:
        if not self.opening:
            return
        linked: list[dict] = []
        if self.view == "timeline" and self.detail:
            if self.detail.get("kind") == "transition":
                linked = self.detail.get("comparisons") or []
            else:
                for one in (self.detail.get("incoming") or []) + (self.detail.get("outgoing") or []):
                    linked += one.get("comparisons") or []
        elif self.view == "catalogue" and self.record:
            for relation in self.record.get("relations") or []:
                linked += relation.get("comparisons") or []
        if len(linked) == 1:
            self.fetch_comparison(linked[0]["id"])
            return
        if linked:
            offers = [(row["id"], row["label"]) for row in linked]
            hint = "Comparisons linked from what is chosen. Differences are between witnesses, not revisions."
        else:
            offers = [(row["id"], f"{row['title']}  ·  {row['kind']}") for row in self.opening["comparisons"]]
            # page: history/index.html, "Read a bounded witness comparison"
            hint = ("These are differences between witnesses, not asserted revisions or ancestry. "
                    "A printed edition’s date does not date the introduction of a reading.")
        self.app.push_screen(Pick("witness comparison", offers, hint),
                             lambda value: value and self.fetch_comparison(value))

    @work(thread=True, exclusive=True, group="history-comparison")
    def fetch_comparison(self, ident: str) -> None:
        try:
            view = bridge.call(ADAPTER, "comparison", ident)
        except Refused as refusal:
            view = {"error": str(refusal)}
        self.deliver(self.read_comparison, view)

    def read_comparison(self, view: dict) -> None:
        self.app.push_screen(Reading(f"{view.get('title') or 'witness comparison'}",
                                     comparison_text(view).content(), "esc close", walks=False))

    # --- the recorded lines ------------------------------------------------

    def load_map(self, slice_id: str, station: str | None) -> None:
        self.fetch_map(slice_id, station)

    @work(thread=True, exclusive=True, group="history-map")
    def fetch_map(self, slice_id: str, station: str | None) -> None:
        try:
            model = bridge.call(ADAPTER, "map", slice_id)
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.show_map, model, station)

    def show_map(self, model: dict, station: str | None) -> None:
        self.map = model
        self.slice = model["slice"]
        box = self.query_one("#history-lines-box", Panel)
        box.retitle(f"recorded lines · {model['slice']}", key="ᵐ")
        box.border_subtitle = "s next slice · u follow one " + model["follow_word"] + " · w where lines part"
        self.query_one("#history-lines", Drawing).show(model, keep=station or model.get("default_station"))
        legend = Doc()
        for row in model["legend"]:
            legend(f"  {MAP_MARKS.get(row['mark'], '·')} ", f"bold {TONE}").line(row["text"])
        if any(row["mark"] == "reception" for row in model["legend"]):
            legend.line("  ║  the hollow (double) track of a documented reception", "$text-muted")
        legend.line()
        legend.line(model["note"], "italic $text-muted")
        legend.line("Columns are the page's tracks of descent; a column is not a date.", "italic $text-muted")
        self.query_one("#history-map-legend-text", Static).update(legend.content())
        self.show_status()
        self.app.refresh_where()

    @on(Drawing.Chosen, "#history-lines")
    def chose_in_map(self, event: Drawing.Chosen) -> None:
        self.fetch_station(event.item.key, False)

    @on(Drawing.Opened, "#history-lines")
    def opened_in_map(self, event: Drawing.Opened) -> None:
        self.fetch_station(event.item.key, True)

    @work(thread=True, exclusive=True, group="history-station")
    def fetch_station(self, ident: str, read: bool) -> None:
        try:
            view = bridge.call(ADAPTER, "station", self.slice, ident)
        except Refused as refusal:
            view = {"missing": str(refusal)}
        self.deliver(self.show_station, view, read)

    def show_station(self, view: dict, read: bool) -> None:
        self.station = view
        box = self.query_one("#history-station", ScrollPanel)
        self.query_one("#history-station-text", Static).update(station_text(view, full=False).content())
        box.retitle(f"station · {view.get('kind', '')}")
        box.border_subtitle = "enter read whole" + (" · x state after" if view.get("state_label") else "")
        box.scroll_home(animate=False)
        if read:
            def walked(step: str | None) -> None:
                if step in ("next", "previous"):
                    drawing = self.query_one("#history-lines", Drawing)
                    drawing.action_move(1 if step == "next" else -1)
                    item = drawing.current()
                    if item:
                        self.fetch_station(item.key, True)

            self.app.push_screen(Reading(f"{view.get('title', '')}", station_text(view).content(),
                                         "esc close · n next · p previous"), walked)

    def action_slice(self) -> None:
        if not self._in("map"):
            return
        ids = [row["id"] for row in self.opening["slices"]]
        if ids:
            following = ids[(ids.index(self.slice) + 1) % len(ids)] if self.slice in ids else ids[0]
            self.load_map(following, None)

    def action_state(self) -> None:
        if not self._in("map") or not self.station.get("state_label"):
            self.app.notify("Choose a station that names a recorded state first.")
            return
        self.fetch_state(self.station["id"], self.station["state_label"])

    @work(thread=True, exclusive=True, group="history-state")
    def fetch_state(self, ident: str, label: str) -> None:
        try:
            view = bridge.call(ADAPTER, "state", self.slice, ident)
        except Refused as refusal:
            view = {"error": str(refusal)}
        self.deliver(self.read_state, view, label)

    def read_state(self, view: dict, label: str) -> None:
        ink = Doc()
        if view.get("error"):
            ink.line(view["error"], "bold $error")
        else:
            ink.line(view["summary"], "bold")
            ink.line(view["note"], "italic $text-muted")
            if view["witnessed"]:
                ink.line(view["witnessed"], "italic $warning")
            for group in view["groups"]:
                ink.line().line(group["title"], f"bold {TONE}")
                if group["meta"]:
                    ink.line(group["meta"], "$text-muted")
                if group["empty"]:
                    ink.line(group["empty"], "italic $text-muted")
                for unit in group["units"]:
                    ink(f"  {unit['name']}", "bold")(f"  {unit['slot']}", "$text-muted").line()
                    _three(ink, unit["incipit"], "    ")
                    if unit["text"]:
                        ink.line(f"    {unit['text']}")
            if view["unestablished"]:
                ink.line().line(view["unestablished_heading"], "bold underline")
                for marker in view["unestablished"]:
                    ink.line(f"  {marker}", "$warning")
        self.app.push_screen(Reading(f"{label}", ink.content(), view.get("title", ""), walks=False))

    def action_unit(self) -> None:
        if not self._in("map"):
            return
        self.fetch_units()

    @work(thread=True, exclusive=True, group="history-units")
    def fetch_units(self) -> None:
        try:
            view = bridge.call(ADAPTER, "units", self.slice)
        except Refused as refusal:
            view = {"error": str(refusal)}
        self.deliver(self.pick_unit, view)

    def pick_unit(self, view: dict) -> None:
        if view.get("error"):
            self.app.notify(view["error"], severity="error")
            return
        offers = [(row["value"], f"{row['label']}   ({row['group']})") for row in view["units"]]
        self.app.push_screen(Pick(f"follow one {view['follow_word']}", offers,
                                  "Where this record first carries it, the acts recorded as touching it, and any "
                                  "recorded absence."),
                             lambda value: value and self.fetch_unit(value))

    @work(thread=True, exclusive=True, group="history-unit")
    def fetch_unit(self, ident: str) -> None:
        try:
            view = bridge.call(ADAPTER, "unit", self.slice, ident)
        except Refused as refusal:
            view = {"error": str(refusal)}
        self.deliver(self.read_unit, view)

    def read_unit(self, view: dict) -> None:
        ink = Doc()
        if view.get("error"):
            ink.line(view["error"], "bold $error")
        else:
            ink.line(view["summary"], "bold").line()
            for stop in view["stops"]:
                ink(stop["title"], f"bold {TONE}")(f"  {stop['kinds']}", "italic").line()
                ink.line(f"  {stop['where']}", "$text-muted")
                if stop.get("fields") is not None:
                    _field_rows(ink, stop["fields"])
                elif stop.get("standing"):
                    _three(ink, stop["standing"]["incipit"], "  ")
                    if stop["standing"]["text"]:
                        ink.line(f"  {stop['standing']['text']}")
                for row in stop["basis"]:
                    ink(f"  {row['kind']} ", f"bold {TONE}").line(row["text"], "$text-muted")
                ink.line()
        self.app.push_screen(Reading(f"{view.get('title', 'unit')}", ink.content(), walks=False))

    def action_junctions(self) -> None:
        if not self._in("map"):
            return
        self.fetch_junctions()

    @work(thread=True, exclusive=True, group="history-junctions")
    def fetch_junctions(self) -> None:
        try:
            view = bridge.call(ADAPTER, "junctions", self.slice)
        except Refused as refusal:
            view = {"none": str(refusal)}
        self.deliver(self.read_junctions, view)

    def read_junctions(self, view: dict) -> None:
        ink = Doc()
        if view.get("none"):
            ink.line(view["none"], "italic")
        else:
            for pair in view["pairs"]:
                ink.line(pair["heading"], f"bold {TONE}")
                ink.line(pair["base"])
                if pair["several"]:
                    ink.line(pair["several"], "italic $text-muted")
                for side in pair["sides"]:
                    ink.line(f"  {side['line']}", "bold")
                    if side["empty"]:
                        ink.line(f"    {side['empty']}", "italic $text-muted")
                    for station in side["stations"]:
                        ink(f"    · {station['title']}")(f"  {station['summary']}", "$text-muted").line()
                ink.line()
            if view["unconnected_heading"]:
                ink.line(view["unconnected_heading"], "bold underline")
                ink.line(view["unconnected_note"], "italic $text-muted")
                for row in view["unconnected"]:
                    ink.line(f"  {row}", "$text-muted")
        self.app.push_screen(Reading("Where the lines part", ink.content(), self.slice, walks=False))

    # --- the catalogue ---------------------------------------------------

    def load_catalogue(self, record: str | None) -> None:
        self.fetch_catalogue(dict(self.filter), record)

    @work(thread=True, exclusive=True, group="history-catalogue")
    def fetch_catalogue(self, current: dict, record: str | None) -> None:
        try:
            view = bridge.call(ADAPTER, "catalogue", current)
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.show_catalogue, view, record)

    def show_catalogue(self, view: dict, record: str | None) -> None:
        self.catalogue_view = view
        listing = self.query_one("#history-record-list", OptionList)
        listing.clear_options()
        self.records = []
        options: list[Option | None] = []
        if view["none"]:
            options.append(Option(Ink()(view["none"], "italic").content(), disabled=True))
        for section in view["sections"]:
            if options:
                options.append(None)
            options.append(Option(Ink()(section["title"], f"bold {TONE}").content(), disabled=True))
            if section["note"]:
                options.append(Option(Ink()(section["note"], "italic $text-muted").content(), disabled=True))
            for row in section["rows"]:
                ink = Doc()
                ink("● " if row["linked"] else "○ ", f"bold {TONE}")(row["title"], "bold" if row["linked"] else "").line()
                ink(f"  {row['date']}", TONE)(f"  ·  {row['group']}", "$text-muted").line()
                ink(f"  {row['statuses']}", "italic $text-muted")
                options.append(Option(ink, id=f"rec-{len(self.records)}"))
                self.records.append(row["id"])
        listing.add_options(options)
        box = self.query_one("#history-records", Panel)
        box.retitle(f"catalogue · {view['filter']['label']}", key="ᵏ")
        box.border_subtitle = "/ search · g record group · c comparison · i limits"
        missing = bool(record) and record not in self.records
        if self.records and not missing:
            # Highlighting fetches the highlighted record; a record asked for
            # that this list does not hold gets no highlight to race its refusal.
            wanted = self.records.index(record) if record in self.records else 0
            listing.highlighted = listing.get_option_index(f"rec-{wanted}")
        self.show_status()
        self.app.refresh_where()
        if missing:
            self.fetch_record(record, False)

    @on(OptionList.OptionHighlighted, "#history-record-list")
    def highlighted_record(self, event: OptionList.OptionHighlighted) -> None:
        if event.option.id and event.option.id.startswith("rec-"):
            self.fetch_record(self.records[int(event.option.id[4:])], False)

    @on(OptionList.OptionSelected, "#history-record-list")
    def selected_record(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("rec-"):
            self.fetch_record(self.records[int(event.option.id[4:])], True)

    @work(thread=True, exclusive=True, group="history-record")
    def fetch_record(self, ident: str, read: bool) -> None:
        try:
            view = bridge.call(ADAPTER, "record", ident)
        except Refused as refusal:
            view = {"missing": str(refusal)}
        self.deliver(self.show_record, view, read)

    def record_text(self, view: dict, *, full: bool) -> Doc:
        ink = Doc()
        if view.get("missing"):
            return ink.line(view["missing"], "bold $warning")
        ink.line(view["title"], f"bold {TONE}")
        ink.line(view["mark"], TONE)
        for name, value in view["facts"]:
            ink(f"{name}: ", "bold").line(value)
        ink.line(view["separate"], "italic $text-muted")
        if view["act_ref"]:
            ink.line(f"Recorded station: {view['act_ref']['station_id']} in {view['act_ref']['slice']} "
                     "(m opens the recorded lines)", TONE)
        else:
            ink.line(view["act_none"], "italic $text-muted")
        ink.line().line(view["relations_heading"], "bold underline")
        if view["relations_none"]:
            ink.line(view["relations_none"], "italic $text-muted")
        for relation in view["relations"]:
            ink.line(relation["heading"], f"bold {TONE}")
            if relation["label"]:
                ink.line(relation["label"], "italic")
            for end in (relation["from"], relation["to"]):
                ink(f"  {'→' if relation['directed'] and end is relation['to'] else '·'} ", TONE)
                ink(end["title"], "bold")(f"  {end['group']} · {end['date']}", "$text-muted").line()
                ink.line(f"    {end['status']}" + (f" · {end['meta']}" if end["meta"] else ""), "$text-muted")
            if full:
                ink.line(relation["basis"])
                ink.line(relation["scope"], "$text-muted")
                ink.line(relation["limitations"], "italic $text-muted")
                ink.line(relation["boundary"], "italic $text-muted")
                for row in relation["evidence"]:
                    ink(f"  ◦ {row['title']}", "bold")
                    if row["url"]:
                        ink(f"  {row['url']}", "underline $text-muted")
                    ink.line().line(f"    {row['locus']}").line(f"    {row['inspection']}", "$text-muted")
                ink.line(relation["id"], "$text-muted")
            for row in relation["comparisons"]:
                ink("  c ", "bold $hotkey").line(row["label"], "underline")
        ink.line().line(view["sources_heading"], "bold underline")
        if view["sources_none"]:
            ink.line(view["sources_none"], "italic $text-muted")
        for row in view["sources"]:
            ink(f"  · {row['label']}")
            if row["url"]:
                ink(f"  {row['url']}", "underline $text-muted")
            ink.line()
            if row["note"]:
                ink.line(f"    {row['note']}", "$text-muted")
        ink.line().line(view["original_heading"], "bold underline")
        ink.line(view["origin"], "$text-muted")
        if full:
            ink.line(view["source_record"], "$text-muted")
        else:
            ink.line("enter reads the original record verbatim", "italic $text-muted")
        return ink

    def show_record(self, view: dict, read: bool) -> None:
        self.record = view
        box = self.query_one("#history-record", ScrollPanel)
        self.query_one("#history-record-text", Static).update(self.record_text(view, full=False).content())
        box.retitle("record")
        box.border_subtitle = "enter read whole"
        box.scroll_home(animate=False)
        if read:
            def walked(step: str | None) -> None:
                if step in ("next", "previous"):
                    listing = self.query_one("#history-record-list", OptionList)
                    index = listing.highlighted or 0
                    move = 1 if step == "next" else -1
                    index += move
                    while 0 <= index < listing.option_count and listing.get_option_at_index(index).disabled:
                        index += move
                    if 0 <= index < listing.option_count:
                        listing.highlighted = index
                        option = listing.get_option_at_index(index)
                        if option.id:
                            self.fetch_record(self.records[int(option.id[4:])], True)

            self.app.push_screen(Reading(f"{view.get('title', '')}", self.record_text(view, full=True).content(),
                                         "esc close · n next · p previous"), walked)

    def action_search(self) -> None:
        if not self._in("catalogue"):
            return

        def answered(value: str | None) -> None:
            if value is not None:
                self.filter = {**self.filter, "q": value[:200]}
                self.load_catalogue(None)

        # page: history.js:2610 — every term must occur, in any order.
        self.app.push_screen(Ask("search source records", "Every word must occur: title, family, group, date, id or "
                                 "the original record. Empty clears the search.", self.filter.get("q", "")), answered)

    def action_group(self) -> None:
        if not self._in("catalogue"):
            return
        offers = [("", "All record groups")] + [(row["value"], f"{row['label']}  ·  {row['records']} records")
                                               for row in self.opening["groups"]]

        def picked(value) -> None:
            if value is not None:
                self.filter = {**self.filter, "family": value}
                self.load_catalogue(None)

        self.app.push_screen(Pick("record group", offers,
                                  "Navigation groups, not a census of rites and not a count of complete books."),
                             picked)

    def action_limits(self) -> None:
        if not self.opening:
            return
        ink = Doc()
        ink.line("Coverage limits of the source catalogue", f"bold {TONE}")
        for row in self.opening["catalogue_limitations"]:
            ink.line(f"· {row}")
        ink.line().line("Stage-history limitations", f"bold {TONE}")
        for row in self.opening["stage_limitations"]:
            ink.line(f"· {row}")
        ink.line().line("Configured text sets", f"bold {TONE}")
        ink.line(self.opening["text_sets_note"], "italic $text-muted")
        for row in self.opening["text_sets"]:
            ink.line(f"· {row}", "$text-muted")
        ink.line().line("Witness comparisons", f"bold {TONE}")
        ink.line(f"{len(self.opening['comparisons'])} configured; each is opened only after the page's own check "
                 "of its declared members (c reads one).", "$text-muted")
        self.app.push_screen(Reading("Coverage limits", ink.content(), walks=False))
