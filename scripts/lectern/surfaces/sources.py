"""The Source Library: find a work, open an edition, read it passage by passage.

Work, Edition, Artifact, Segment and Passage stay five things here, as on the
page: a work owns its editions; an edition owns its artifacts, segments and
passages side by side; and each passage names the one artifact that controls
it, directly or through a segment. Nothing is drawn as a chain from one to the
next. Whether a passage's words may be shown is the generator's decision,
carried in the published layers; where they may not, the reason is printed in
their place, with the same provenance a text would have. Every choice, order,
count, label and refusal is asked of `adapters/sources.js`.
"""
from __future__ import annotations

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge
from ..dialogs import Ask, Pick
from ..repo import Refused
from ..surface import Surface
from ..widgets import Ink, Panel, ScrollPanel, count, fitted, literal, meter

ADAPTER = "sources"
ACCENT = "$sources-color"
CONTROLS = (
    # (state key, key that reaches it, its name here)
    ("author", "a", "author"),
    ("category", "k", "kind"),
    ("language", "l", "language"),
    ("period", "p", "period"),
    ("rights", "r", "rights"),
    ("sort", "o", "order"),
)
BLANK = {"author": "", "category": "", "language": "", "period": "", "rights": "",
         "readable": False, "find": "", "sort": "author"}


def split_line(line: str, first: int, rest: int) -> list[str]:
    """One physical line in pieces no wider than the pane, every character kept.

    A piece ends after a space where one falls in reach, else at the width.
    """
    pieces = []
    room = first
    while len(line) > room:
        cut = line.rfind(" ", 0, room)
        cut = cut + 1 if cut > 0 else room
        pieces.append(line[:cut])
        line = line[cut:]
        room = max(8, rest)
    pieces.append(line)
    return pieces


class Sources(Surface):
    key = "6"
    label = "Sources"
    HELP = (
        ("/", "find: a title, author, alias or id"),
        ("escape", "leave the find box for the list"),
        ("enter", "on a work, go to its editions; on an edition, open it"),
        ("↑ / ↓", "in the passages, move to a passage; it is read at once"),
        ("← / →", "previous / next passage of the open edition (none when it has one)"),
        ("a k l p r", "author, kind, language, period, rights"),
        ("v", "only what can be read here"),
        ("o", "next order: author, title, earliest edition, readable passage count"),
        ("x", "clear every choice"),
        ("g", "go to an edition or passage id, as a link would"),
        ("b", "back to the corpus: close the edition"),
        ("f", "focus: the edition alone, full width; again to restore"),
    )
    BINDINGS = [
        Binding("slash", "search", "find a source"),
        Binding("r", "pick('rights')", "choose a rights status"),
        Binding("v", "readable", "only what can be read here"),
        Binding("g", "goto", "go to an edition or passage id"),
        Binding("left", "step(-1)", "previous passage", show=False),
        Binding("right", "step(1)", "next passage", show=False),
        Binding("a", "pick('author')", "choose an author", show=False),
        Binding("k", "pick('category')", "choose a kind", show=False),
        Binding("l", "pick('language')", "choose a language", show=False),
        Binding("p", "pick('period')", "choose a period", show=False),
        Binding("o", "order", "next order", show=False),
        Binding("x", "clear", "clear every choice", show=False),
        Binding("b", "back", "back to the corpus", show=False),
    ]
    CSS = """
    .sources.focus #sources-left { display: none; }
    .sources.narrow #sources-left { width: 34; }
    .sources.narrow #sources-body { layout: vertical; }
    .sources.narrow #sources-passages { width: 1fr; height: 6; }
    .sources.narrow #sources-head { max-height: 7; }
    .sources #sources-passages.withheld-here { border: round $warning 60%; }
    """
    DEFAULT_CSS = """
    Sources #sources-left { width: 46; }
    Sources #sources-find { height: auto; }
    Sources #sources-find Input { border: none; background: $surface; height: 1; padding: 0 1; }
    Sources #sources-controls { height: auto; }
    Sources #sources-status { color: $text-muted; height: auto; }
    Sources #sources-works { height: 1fr; }
    Sources #sources-head { height: auto; max-height: 16; }
    Sources #sources-body { height: 1fr; }
    Sources #sources-passages { width: 28; height: 1fr; }
    Sources #sources-reading { height: 1fr; }
    Sources #sources-overview { height: 1fr; }
    """

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.opening: dict = {}
        self.state: dict = dict(BLANK)
        self.found: dict = {}
        self.order: list[tuple[int, list[int]]] = []
        self.open_edition: dict | None = None
        self.at = 0
        self.passage: dict | None = None
        self._intent: dict = {}
        self._token = 0
        self._edition_token = 0

    # --- building --------------------------------------------------------

    def build(self) -> None:
        head = ScrollPanel(Static("", id="sources-head-text"), title="edition", id="sources-head")
        body = Horizontal(
            Panel(OptionList(id="sources-passage-list"), title="passages", id="sources-passages"),
            ScrollPanel(Static("", id="sources-reading-text"), title="passage", id="sources-reading"),
            id="sources-body",
        )
        head.display = False
        body.display = False
        self.mount(
            Horizontal(
                Vertical(
                    Panel(Static("", id="sources-controls"),
                          Input(placeholder="title, author, alias or id", id="sources-query"),
                          Static("", id="sources-status"), title=" find a source", key="/", id="sources-find"),
                    Panel(OptionList(id="sources-list"), title="works", id="sources-works"),
                    id="sources-left",
                ),
                Vertical(
                    ScrollPanel(Static("", id="sources-overview-text"), title="the source library",
                                id="sources-overview"),
                    head,
                    body,
                    id="sources-right",
                ),
            )
        )
        self.call_after_refresh(lambda: self.query_one("#sources-list", OptionList).focus())
        self.start()

    @work(thread=True, exclusive=True, group="sources-start")
    def start(self) -> None:
        try:
            opening = bridge.call(ADAPTER, "opening")
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.opened_with, opening)

    def opened_with(self, opening: dict) -> None:
        self.opening = opening
        self.draw_controls()
        self.draw_overview()
        self.refind()

    def fail(self, message: str) -> None:
        self.query_one("#sources-overview-text", Static).update(
            Ink().line("The source corpus could not be loaded.", "bold $error").line(message).content())

    def draw_overview(self, refusal: str = "") -> None:
        counted = self.opening.get("counted") or {}
        ink = Ink()
        box = self.query_one("#sources-overview", ScrollPanel)
        if refusal:
            # A cited edition or passage that cannot be opened is refused here, with the
            # id as asked; nothing else is opened in its place.
            ink.line("This address cannot be opened", "bold $warning")
            ink.line(refusal, "$warning")
            ink.line("The finder on the left is unchanged; the corpus is below.", "italic $text-muted")
            ink.line()
            box.retitle("refused")
        else:
            box.retitle("the source library")
        ink.line("The Source Library", f"bold {ACCENT}")
        ink.line(f"{counted.get('works', 0):,} works · {counted.get('editions', 0):,} editions · "
                 f"{counted.get('artifacts', 0):,} artifacts · {counted.get('passages', 0):,} passages",
                 "$text-muted")
        ink.line()
        passages, readable = counted.get("passages", 0), counted.get("readable", 0)
        ink(f"{'readable here':<17}", "bold")
        meter(ink, readable, passages, 24)(f" {readable:,} of {passages:,} passages").line()
        ink.line("Every other passage is listed with the reason its words are not shown.", "italic $text-muted")
        ink.line()
        editions = counted.get("editions", 0)
        ink.line(f"Rights, by the editions whose artifacts record each, of {editions:,}", f"bold underline {ACCENT}")
        ink.line("An edition may record several, so the rows do not sum to the whole.", "italic $text-muted")
        for one in self.opening.get("rights") or []:
            ink(f"{one['id']:<17}", "bold")
            meter(ink, one["editions"], editions, 24)
            ink(f" {count(one['editions'], 'edition'):>13} · {count(one['artifacts'], 'artifact')}").line()
        ink.line()
        ink.line("Enter on a work opens the edition it opens on — the first that can be read here, else the "
                 "first — and on an edition, that edition. g goes to an edition or passage id.", "italic")
        for paragraph in self.opening.get("glossary") or []:
            ink.line()
            ink.line(paragraph, "italic $text-muted")
        if self.opening.get("advisory"):
            ink.line()
            ink.line("The corpus says of itself", "bold $text-muted")
            ink.line(self.opening["advisory"], "italic $text-muted")
        self.query_one("#sources-overview-text", Static).update(ink.content())

    # --- choosing --------------------------------------------------------

    def label_of(self, name: str, value: str) -> str:
        for option in (self.opening.get("controls") or {}).get(name, []):
            if option["value"] == value:
                return option["label"]
        return value

    def draw_controls(self) -> None:
        ink = Ink()
        for name, key, said in CONTROLS:
            value = self.state[name]
            ink(f"{key} ", "bold $hotkey")(f"{said:<9}", "$text-muted")
            ink(self.label_of(name, value), f"bold {ACCENT}" if value and value != "author" else "")
            ink.line()
        ink("v ", "bold $hotkey")(f"{'readable':<9}", "$text-muted")
        ink("☑ only what can be read here" if self.state["readable"] else "☐ only what can be read here",
            f"bold {ACCENT}" if self.state["readable"] else "")
        self.query_one("#sources-controls", Static).update(ink.content())

    def action_pick(self, name: str) -> None:
        options = (self.opening.get("controls") or {}).get(name)
        if not options:
            return
        said = next(one[2] for one in CONTROLS if one[0] == name)
        current = self.state[name]
        offers = [(one["value"], ("● " if one["value"] == current else "  ") + one["label"]) for one in options]

        def picked(value) -> None:
            if value is None:
                return
            self.state[name] = value
            self.draw_controls()
            self.refind()

        self.app.push_screen(Pick(said, offers, "The page's own choices, counted by the generator; "
                                                "● marks the one in force."), picked)

    def action_order(self) -> None:
        sorts = [one["value"] for one in (self.opening.get("controls") or {}).get("sort", [])]
        if sorts:
            current = self.state["sort"] if self.state["sort"] in sorts else sorts[0]
            self.state["sort"] = sorts[(sorts.index(current) + 1) % len(sorts)]
            self.draw_controls()
            self.refind()

    def action_readable(self) -> None:
        self.state["readable"] = not self.state["readable"]
        self.draw_controls()
        self.refind()

    def action_clear(self) -> None:
        self.state = dict(BLANK)
        query = self.query_one("#sources-query", Input)
        with query.prevent(Input.Changed):
            query.value = ""
        self.draw_controls()
        self.refind()

    def action_search(self) -> None:
        self._focus_finder("#sources-query")

    def _focus_finder(self, selector: str) -> None:
        """An explicit finder command reveals its target before moving focus."""
        self.remove_class("focus")
        self.call_after_refresh(self.query_one(selector).focus)

    def key_escape(self) -> None:
        if self.query_one("#sources-query", Input).has_focus:
            self.query_one("#sources-list", OptionList).focus()

    @on(Input.Changed, "#sources-query")
    def typed(self, event: Input.Changed) -> None:
        self.state["find"] = event.value
        self.refind()

    @on(Input.Submitted, "#sources-query")
    def submitted(self) -> None:
        self.query_one("#sources-list", OptionList).focus()

    def refind(self) -> None:
        if self.opening:
            self.find(dict(self.state))

    @work(thread=True, exclusive=True, group="sources-find")
    def find(self, state: dict) -> None:
        try:
            found = bridge.call(ADAPTER, "find", state)
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.listed, found)

    # --- the finder list -------------------------------------------------

    def listed(self, found: dict) -> None:
        self.found = found
        self.order = [(row[0], row[1]) for row in found["rows"]]
        self.draw_list()
        self.query_one("#sources-status", Static).update(Ink()(found["tally"], "italic").content())
        works = self.query_one("#sources-works", Panel)
        works.retitle(f"works · {self.label_of('sort', found['state']['sort'])}")
        works.border_subtitle = "▸ text readable here · ○ none"
        if self._intent:
            intent, self._intent = self._intent, {}
            self.follow(**intent)
        self.app.refresh_where()

    def draw_list(self) -> None:
        if not self.found:
            return
        works = self.opening["works"]
        listing = self.query_one("#sources-list", OptionList)
        width = max(12, listing.size.width - 1) if listing.size.width else 50
        self._drawn_width = width
        kept = listing.highlighted_option.id if listing.highlighted_option is not None else None
        listing.clear_options()
        options = []
        for at, shown in self.order:
            one = works[at]
            head = fitted([(one["title"], f"bold {ACCENT}")], width)
            head.line()
            fitted([(one["author"], "" if one["authorRecorded"] else "italic $warning"),
                    (f" · {one['category']}" if one["category"] else "", "$text-muted")], width, head)
            if one["also"]:
                head.line()
                fitted([(one["also"], "italic $text-muted")], width, head)
            if not one["editions"]:
                head.line()
                fitted([("  no edition record", "italic $text-muted")], width, head)
            options.append(Option(head.content(), id=f"w-{at}"))
            for index in shown:
                edition = one["editions"][index]
                mark = ("  ▸ ", f"bold {ACCENT}") if edition["readable"] else ("  ○ ", "$text-muted")
                ink = fitted([mark, (edition["title"], "")], width)
                ink.line()
                facts = [("    " + edition["facts"], "$text-muted")]
                if edition["withheld"]:
                    facts.append((" · " + edition["withheld"], "italic $warning"))
                fitted(facts, width, ink)
                options.append(Option(ink.content(), id=f"e-{at}-{index}"))
        if self.found.get("zero"):
            options.append(Option(Ink()(self.found["zero"], "italic $warning").content(), disabled=True))
        listing.add_options(options)
        if kept is not None:
            try:
                listing.highlighted = listing.get_option_index(kept)
            except Exception:  # noqa: BLE001 - what the cursor was on is not listed under these choices
                pass

    def on_resize(self, event) -> None:
        super().on_resize(event)
        self.call_after_refresh(self.redraw_list)

    def redraw_list(self) -> None:
        self.redraw_passage_list()
        if self.passage and self.passage.get("source") == "physical-lines" and \
                self.query_one("#sources-reading", ScrollPanel).scrollable_content_region.width != \
                getattr(self, "_drawn_at", None):
            self.draw_passage()
        if not self.found:
            return
        listing = self.query_one("#sources-list", OptionList)
        if (max(12, listing.size.width - 1) if listing.size.width else 50) != getattr(self, "_drawn_width", None):
            self.draw_list()

    @on(OptionList.OptionSelected, "#sources-list")
    def chosen(self, event: OptionList.OptionSelected) -> None:
        ident = event.option.id or ""
        if ident.startswith("e-"):
            at, index = ident[2:].split("-")
            self.open_at(int(at), int(index), 0)
        elif ident.startswith("w-"):
            self.to_editions(int(ident[2:]))

    def to_editions(self, at: int) -> None:
        """A work lists its editions; the reader chooses one (sources.js:209-223).
        Nothing is opened by order: the cursor only moves to the first of them."""
        listing = self.query_one("#sources-list", OptionList)
        for index in range(listing.option_count):
            if (listing.get_option_at_index(index).id or "").startswith(f"e-{at}-"):
                listing.highlighted = index
                return
        work_title = self.opening["works"][at]["title"]
        self.app.notify(f"{literal(work_title)}: this work is identified, and no edition of it is recorded "
                        "under these choices.")

    # --- an edition ------------------------------------------------------

    def open_at(self, at: int, index: int, passage_at: int) -> None:
        self._edition_token += 1
        # Even an empty or refused edition supersedes the old passage.
        self._token += 1
        self.fetch_edition(self._edition_token, at, index, passage_at)

    @work(thread=True, exclusive=True, group="sources-edition")
    def fetch_edition(self, token: int, at: int, index: int, passage_at: int) -> None:
        try:
            edition = bridge.call(ADAPTER, "edition", at, index)
        except Refused as refusal:
            edition = {"problem": str(refusal), "at": [at, index], "id": ""}
        self.deliver(self.show_edition, token, edition, passage_at)

    def show_edition(self, token: int, edition: dict, passage_at: int) -> None:
        if token != self._edition_token:
            return
        self.open_edition = edition
        self.query_one("#sources-overview").display = False
        self.query_one("#sources-head").display = True
        self.query_one("#sources-body").display = True
        self.draw_head(edition)
        listing = self.query_one("#sources-passage-list", OptionList)
        listing.clear_options()
        reading = self.query_one("#sources-reading-text", Static)
        box = self.query_one("#sources-passages", Panel)
        if edition.get("problem"):
            box.retitle("passages")
            reading.update(Ink().line(edition["problem"], "bold $error").content())
            self.query_one("#sources-reading", ScrollPanel).retitle("passage")
            self.passage = None
            self.app.refresh_where()
            return
        passages = edition["passages"]
        self.draw_passage_list()
        self.call_after_refresh(self.redraw_passage_list)
        count = len(passages)
        box.retitle(f"passages · {count}")
        box.border_subtitle = "▸ text · ○ not shown" if count else ""
        self.land_finder(edition["at"])
        if not count:
            self.passage = None
            self.at = 0
            ink = Ink().line(edition["empty"], "italic $warning").line()
            self.apparatus(ink, edition, None)
            reading.update(ink.content())
            self.query_one("#sources-reading", ScrollPanel).retitle("no passage")
            self.query_one("#sources-reading", ScrollPanel).border_subtitle = ""
            self.app.refresh_where()
            return
        self.at = max(0, min(passage_at, count - 1))
        with listing.prevent(OptionList.OptionHighlighted):
            listing.highlighted = self.at
        self.call_after_refresh(listing.scroll_to_highlight, top=True)
        self.read(self.at)
        if self.focused_in_finder():
            listing.focus()

    def draw_passage_list(self) -> None:
        """The edition's passages, one locus and one mark each, cut to the list's width."""
        listing = self.query_one("#sources-passage-list", OptionList)
        width = max(12, listing.size.width - 1) if listing.size.width else 24
        self._passages_width = width
        kept = listing.highlighted
        listing.clear_options()
        options = []
        for row in (self.open_edition or {}).get("passages") or []:
            glyph = ("▸ ", f"bold {ACCENT}") if row["readable"] else ("○ ", "$warning")
            ink = fitted([glyph, (row["number"], "bold"), (row["locus"], "")], width)
            ink.line()
            fitted([(" " * (2 + len(row["number"])), ""),
                    (row["mark"], "$text-muted" if row["readable"] else "italic $warning")], width, ink)
            options.append(Option(ink.content(), id=f"p-{len(options)}"))
        listing.add_options(options)
        if kept is not None and kept < listing.option_count:
            with listing.prevent(OptionList.OptionHighlighted):
                listing.highlighted = kept

    def redraw_passage_list(self) -> None:
        if not self.open_edition or self.open_edition.get("problem"):
            return
        listing = self.query_one("#sources-passage-list", OptionList)
        width = max(12, listing.size.width - 1) if listing.size.width else 24
        if width != getattr(self, "_passages_width", None):
            self.draw_passage_list()
            with listing.prevent(OptionList.OptionHighlighted):
                listing.highlighted = self.at
            self.call_after_refresh(listing.scroll_to_highlight, top=True)

    def land_finder(self, at: list[int]) -> None:
        """Keep the finder's cursor on the edition being read, where the choices list it."""
        listing = self.query_one("#sources-list", OptionList)
        try:
            position = listing.get_option_index(f"e-{at[0]}-{at[1]}")
        except Exception:  # noqa: BLE001 - not listed under the choices in force: the finder is left as it is
            return
        if listing.highlighted != position:
            listing.highlighted = position
            self.call_after_refresh(listing.scroll_to_highlight)

    def focused_in_finder(self) -> bool:
        focused = self.app.focused
        return focused is None or self.query_one("#sources-left") in focused.ancestors_with_self

    def draw_head(self, edition: dict) -> None:
        box = self.query_one("#sources-head", ScrollPanel)
        ink = Ink()
        if edition.get("problem"):
            ink.line(edition["problem"], "bold $error")
            box.retitle("edition")
            box.border_subtitle = edition.get("id") or ""
            self.query_one("#sources-head-text", Static).update(ink.content())
            return
        head = edition["head"]
        ink.line(head["author"], "bold")
        ink.line(head["edition"], "italic")
        if head["facts"]:
            ink.line(head["facts"], "$text-muted")
        if head["publication"]:
            ink.line(head["publication"], "$text-muted")
        for label, value in (("Authority", edition.get("authority")), ("Jurisdiction", edition.get("jurisdiction"))):
            if value:
                ink(f"{label}: ", "bold")(value).line()
        total, readable = edition["passagesIndexed"], edition["readableIndexed"]
        if total:
            ink(f"{'readable here':<15}", "bold")
            meter(ink, readable, total, 20)(f" {readable} of {total} passages")
            for reason in edition["reasons"]:
                ink.line()
                ink(f"{'not shown':<15}" if reason is edition["reasons"][0] else " " * 15, "bold")
                meter(ink, reason["count"], total, 20)(f" {reason['count']} · {reason['code']}: ", "")
                ink(reason["reason"], "italic $text-muted")
        else:
            ink("No passage of this edition is addressed.", "italic $warning")
        self.query_one("#sources-head-text", Static).update(ink.content())
        box.retitle(head["title"], key=None)
        box.border_subtitle = edition["id"]

    # --- a passage -------------------------------------------------------

    @on(OptionList.OptionHighlighted, "#sources-passage-list")
    def glanced(self, event: OptionList.OptionHighlighted) -> None:
        ident = event.option.id or ""
        if ident.startswith("p-") and int(ident[2:]) != self.at:
            self.read(int(ident[2:]))

    def read(self, at: int) -> None:
        if not self.open_edition or self.open_edition.get("problem"):
            return
        self.at = at
        self._token += 1
        work_at, edition_at = self.open_edition["at"]
        self.fetch_passage(self._token, work_at, edition_at, at)

    @work(thread=True, exclusive=True, group="sources-passage")
    def fetch_passage(self, token: int, work_at: int, edition_at: int, at: int) -> None:
        try:
            passage = bridge.call(ADAPTER, "passage", work_at, edition_at, at)
        except Refused as refusal:
            passage = {"failed": str(refusal), "at": at}
        self.deliver(self.show_passage, token, passage)

    def show_passage(self, token: int, passage: dict) -> None:
        # Showing any passage supersedes every load still running (sources.js:454-461):
        # a late answer for another passage is dropped, never painted here.
        if token != self._token:
            return
        self.passage = passage
        self.draw_passage(scroll_home=True)
        listing = self.query_one("#sources-passage-list", OptionList)
        if listing.highlighted != passage["at"]:
            with listing.prevent(OptionList.OptionHighlighted):
                listing.highlighted = passage["at"]
        self.app.refresh_where()

    def draw_passage(self, scroll_home: bool = False) -> None:
        passage = self.passage
        if passage is None:
            return
        box = self.query_one("#sources-reading", ScrollPanel)
        ink = Ink()
        if passage.get("failed"):
            ink.line(passage["failed"], "bold $error")
            self.query_one("#sources-reading-text", Static).update(ink.content())
            return
        ink.line(passage["locus"], f"bold {ACCENT}")
        if passage["states"]:
            ink.line(passage["states"], "$text-muted")
        if passage["context"]:
            ink.line(passage["context"], "italic")
        ink.line()
        physical = passage.get("source") == "physical-lines"
        width = box.scrollable_content_region.width
        self._drawn_at = width
        if not passage["readable"]:
            ink("Not shown: ", "bold $warning").line(passage["reason"], "$warning")
        elif passage.get("unloaded"):
            ink("Not shown: ", "bold $warning").line(passage["unloaded"], "$warning")
        else:
            if passage.get("acknowledgement"):
                ink("Licence: ", "bold").line(passage["acknowledgement"]).line()
            for paragraph in passage["paragraphs"]:
                for line in paragraph:
                    if physical and width and len(line) > width:
                        # A physical line longer than the pane continues on marked lines,
                        # so the artifact's own line breaks stay the only unmarked ones.
                        first, *rest = split_line(line, width, width - 2)
                        ink.line(first)
                        for part in rest:
                            ink("⤷ ", "$text-muted").line(part)
                    else:
                        ink.line(line)
                ink.line()
        self.provenance(ink, passage)
        if passage["notes"]:
            ink.line()
            ink.line(passage["notes"], "italic $text-muted")
        ink.line()
        self.apparatus(ink, self.open_edition, passage)
        self.query_one("#sources-reading-text", Static).update(ink.content())
        box.retitle(passage["count"])
        if passage["readable"] and not passage.get("unloaded"):
            said = f"{passage['words']} words · {passage.get('source') or 'source not recorded'}"
            if physical:
                said += " · ⤷ a line continued"
        else:
            said = f"not shown here · {passage.get('withheld') or 'unloaded'}"
        if len((self.open_edition or {}).get("passages") or []) > 1:
            said += " · ← → step"
        box.border_subtitle = said
        if scroll_home:
            box.scroll_home(animate=False)

    @staticmethod
    def provenance(ink: Ink, passage: dict) -> None:
        """Whose bytes these are, and under what: for a text and a refusal alike (sources.js:542-579)."""
        said = passage["provenance"]
        ink.line("─" * 24, "$text-muted")
        if said["controller"]:
            ink("Controlling artifact: ", "bold")(said["controller"], ACCENT)(".").line()
        else:
            ink.line(said["none"], "bold")
        if said["facts"]:
            ink.line(said["facts"], "$text-muted")
        if said["basis"]:
            ink.line(said["basis"], "$text-muted")
        if said["segment"]:
            ink.line(said["segment"], "italic")
        if said["sourceUrl"]:
            url = said["sourceUrl"]
            ink.line(url, f"underline {ACCENT}")

    @staticmethod
    def apparatus(ink: Ink, edition: dict, passage: dict | None) -> None:
        """The edition's artifacts under the reading, where they explain it (sources.js:581-645)."""
        controller = (passage or {}).get("provenance", {}).get("controller") or ""
        artifacts = edition.get("artifacts") or []
        if artifacts:
            ink.line(edition["artifactsSummary"], f"bold underline {ACCENT}")
            for one in artifacts:
                chosen = bool(controller) and one["id"] == controller
                ink("◆ " if chosen else "◇ ", f"bold {ACCENT}" if chosen else "$text-muted")
                ink(one["idSaid"], "bold" if one["id"] else "italic $warning")
                if chosen:
                    ink("  Controls the selected passage", f"bold {ACCENT}")
                ink.line()
                ink("  ")(one["relationship"], "italic")
                facts = [fact for fact in (one["type"], one["rights"], one["storage"]) if fact]
                ink(" · " + " · ".join(facts), "$text-muted").line()
                if one["basis"]:
                    ink("  ")(one["basis"], "$text-muted").line()
        if edition.get("about"):
            ink.line()
            ink.line("About this work", f"bold underline {ACCENT}")
            ink.line(edition["about"])

    def action_step(self, by: int) -> None:
        if not self.open_edition or self.open_edition.get("problem"):
            return
        count = len(self.open_edition.get("passages") or [])
        target = self.at + by
        if count > 1 and 0 <= target < count:
            self.read(target)

    def action_back(self) -> None:
        self._edition_token += 1
        self._token += 1
        self.open_edition = None
        self.passage = None
        self.draw_overview()
        self.query_one("#sources-overview").display = True
        self.query_one("#sources-head").display = False
        self.query_one("#sources-body").display = False
        self._focus_finder("#sources-list")
        self.app.refresh_where()

    # --- where, and being sent here --------------------------------------

    def where(self) -> str:
        if self.open_edition and not self.open_edition.get("problem"):
            head = self.open_edition["head"]["title"]
            if self.passage and self.passage.get("count"):
                return f"{head} · {self.passage['count']}"
            return head
        return self.found.get("tally", "")

    def action_goto(self) -> None:
        def answered(value: str | None) -> None:
            if not value:
                return
            if value.startswith("edition."):
                self.follow(edition=value)
            else:
                self.follow(passage=value)

        self.app.push_screen(Ask("go to", "An edition id (edition.…) or a passage id (passage.…), "
                                          "as a link would carry it.", ""), answered)

    def follow(self, passage: str | None = None, edition: str | None = None, **_) -> None:
        if not passage and not edition:
            return
        if not self.found:
            self._intent = {"passage": passage, "edition": edition}
            return
        self.locate(edition or "", passage or "")

    @work(thread=True, exclusive=True, group="sources-locate")
    def locate(self, edition: str, passage: str) -> None:
        try:
            found = bridge.call(ADAPTER, "follow", edition, passage)
        except Refused as refusal:
            found = {"problem": str(refusal)}
        self.deliver(self.located, found)

    def located(self, found: dict) -> None:
        if found.get("problem"):
            # Refused where the reading would be, with the id as asked; nothing else is opened.
            self._edition_token += 1
            self._token += 1
            self.open_edition = None
            self.passage = None
            self.query_one("#sources-overview").display = True
            self.query_one("#sources-head").display = False
            self.query_one("#sources-body").display = False
            self.draw_overview(refusal=found["problem"])
            self.query_one("#sources-overview", ScrollPanel).scroll_home(animate=False)
            self.app.notify(found["problem"], severity="warning", timeout=6)
            self.app.refresh_where()
            return
        self.open_at(found["work"], found["edition"], found["at"])
