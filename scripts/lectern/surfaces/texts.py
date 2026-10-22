"""Every Document: each work the project publishes, and each independent treatment of it.

A work is one subject; a treatment is one provider's independently produced
document on it, and the two treatments of a work usually carry different titles,
so no work is given a single name here. The page calls a treatment an "edition";
the accepted vision keeps that word for Source Editions and says "independent
treatment" (guidance/corpus-browser-vision.md:129-141), which is the word used
here. Every choice, title, order and count is the catalogue model's, asked
through `adapters/texts.js`; a web edition is set by the site's own renderer
(`lectern/webedition.py`).
"""
from __future__ import annotations

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge, webedition
from ..dialogs import Pick, Reading
from ..repo import Refused
from ..surface import Surface
from ..widgets import Ink, Panel, ScrollPanel, fitted, meter

ADAPTER = "texts"
ACCENT = "$texts-color"
CONTROLS = (
    # (state key, key that reaches it, its name here)
    ("author", "a", "author"),
    ("edition", "t", "treatment"),
    ("section", "s", "section"),
    ("reading", "r", "reading"),
    ("sort", "o", "order"),
)


def availability(row: dict) -> str:
    """Where a treatment can be read, in the list's few words."""
    if row["web"]:
        return "read here"
    if row["pdf"]:
        return "PDF only"
    if row["pdfAbsent"]:
        return "PDF absent"
    return "no PDF, no web edition"


class Texts(Surface):
    key = "5"
    label = "Texts"
    HELP = (
        ("/", "find: words of a title, subject, path, provider or model"),
        ("escape", "leave the find box for the list"),
        ("↑ / ↓", "move through works and treatments; the record follows the cursor"),
        ("enter, w", "read the highlighted treatment's web edition, set as the site sets it"),
        ("a", "author: one model, or any"),
        ("t", "treatment: Claude's, GPT's, or both"),
        ("s", "section"),
        ("r", "reading: readable here, PDF only, or however held"),
        ("o", "next order: section then path, title, last revised, extent"),
        ("x", "clear every choice"),
        ("f", "focus: the record alone, full width; again to restore"),
    )
    BINDINGS = [
        Binding("slash", "search", "find a document"),
        Binding("w", "read", "read the web edition"),
        Binding("s", "pick('section')", "choose a section"),
        Binding("r", "pick('reading')", "choose how it is held"),
        Binding("o", "order", "next order"),
        Binding("a", "pick('author')", "choose an author model", show=False),
        Binding("t", "pick('edition')", "choose a treatment's provider", show=False),
        Binding("x", "clear", "clear every choice", show=False),
    ]
    CSS = """
    .texts.focus #texts-left { display: none; }
    .texts.narrow #texts-left { width: 42; }
    .texts.narrow #texts-cards, .texts.narrow #texts-holdings { display: none; }
    .texts .texts-card.chosen { border: round $texts-color; }
    """
    DEFAULT_CSS = """
    Texts #texts-left { width: 62; }
    Texts #texts-find { height: auto; }
    Texts #texts-find Input { border: none; background: $surface; height: 1; padding: 0 1; }
    Texts #texts-controls { height: auto; }
    Texts #texts-status { color: $text-muted; height: auto; }
    Texts #texts-works { height: 1fr; }
    Texts #texts-cards { height: auto; max-height: 16; }
    Texts .texts-card { height: auto; width: 1fr; }
    Texts #texts-record { height: 1fr; }
    Texts #texts-holdings { height: auto; }
    """

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.opening: dict = {}
        self.state: dict = {"author": "", "edition": "", "section": "", "reading": "", "sort": "section", "find": ""}
        self.found: dict = {}
        self.order: list[tuple[int, list[int]]] = []
        self.cursor: tuple[int, int | None] | None = None
        self.record: dict | None = None
        self._intent: dict = {}
        self._token = 0

    # --- building --------------------------------------------------------

    def build(self) -> None:
        self.mount(
            Horizontal(
                Vertical(
                    Panel(Static("", id="texts-controls"),
                          Input(placeholder="title, subject or path", id="texts-query"),
                          Static("", id="texts-status"), title=" find a document", key="/", id="texts-find"),
                    Panel(OptionList(id="texts-list"), title="works", id="texts-works"),
                    id="texts-left",
                ),
                Vertical(
                    Horizontal(id="texts-cards"),
                    ScrollPanel(Static("", id="texts-record-text"), title="record", id="texts-record"),
                    Panel(Static("", id="texts-holdings-text"), title="how these are held", id="texts-holdings"),
                    id="texts-right",
                ),
            )
        )
        self.call_after_refresh(lambda: self.query_one("#texts-list", OptionList).focus())
        self.start()

    @work(thread=True, exclusive=True, group="texts-start")
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
        self.welcome()
        self.refind()

    def fail(self, message: str) -> None:
        self.query_one("#texts-record-text", Static).update(
            Ink().line("The catalogue could not be loaded.", "bold $error").line(message).content())

    def welcome(self) -> None:
        counted = self.opening.get("counted") or {}
        ink = Ink()
        ink.line("Every Document", f"bold {ACCENT}")
        ink.line(f"{counted.get('works', 0)} works · {counted.get('documents', 0)} documents · "
                 f"{counted.get('pages', 0):,} pages, read from one generated file.", "$text-muted")
        ink.line()
        ink.line("Move through the list: the treatments of the work under the cursor stand side by side above, "
                 "and the full record of a treatment fills this pane. Enter reads a treatment's web edition.",
                 "italic")
        ink.line()
        ink.line("A work is one subject; a treatment is one provider's independently produced document on it. "
                 "The two treatments of a work usually carry different titles, so no work is given a single "
                 "name here: each treatment is listed under the title it actually prints.", "italic $text-muted")
        self.advisory(ink)
        self.query_one("#texts-record-text", Static).update(ink.content())
        self.query_one("#texts-record", ScrollPanel).retitle("record")

    def advisory(self, ink: Ink) -> None:
        if self.opening.get("advisory"):
            ink.line()
            ink.line("The catalogue says of itself", "bold $text-muted")
            ink.line(self.opening["advisory"], "italic $text-muted")

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
            ink(f"{key} ", "bold $hotkey")(f"{said:<10}", "$text-muted")
            ink(self.label_of(name, value), f"bold {ACCENT}" if value and value != "section" else "")
            if name != CONTROLS[-1][0]:
                ink.line()
        self.query_one("#texts-controls", Static).update(ink.content())

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

        self.app.push_screen(Pick(said, offers, "The page's own choices; ● marks the one in force."), picked)

    def action_order(self) -> None:
        sorts = [one["value"] for one in (self.opening.get("controls") or {}).get("sort", [])]
        if sorts:
            current = self.state["sort"] if self.state["sort"] in sorts else sorts[0]
            self.state["sort"] = sorts[(sorts.index(current) + 1) % len(sorts)]
            self.draw_controls()
            self.refind()

    def action_clear(self) -> None:
        self.state = {"author": "", "edition": "", "section": "", "reading": "", "sort": "section", "find": ""}
        query = self.query_one("#texts-query", Input)
        with query.prevent(Input.Changed):
            query.value = ""
        self.draw_controls()
        self.refind()

    def action_search(self) -> None:
        self.query_one("#texts-query", Input).focus()

    def key_escape(self) -> None:
        if self.query_one("#texts-query", Input).has_focus:
            self.query_one("#texts-list", OptionList).focus()

    @on(Input.Changed, "#texts-query")
    def typed(self, event: Input.Changed) -> None:
        self.state["find"] = event.value
        self.refind()

    @on(Input.Submitted, "#texts-query")
    def submitted(self) -> None:
        self.query_one("#texts-list", OptionList).focus()

    def refind(self, then: tuple[int, int | None] | None = None) -> None:
        if self.opening:
            self.find(dict(self.state), then)

    @work(thread=True, exclusive=True, group="texts-find")
    def find(self, state: dict, then: tuple[int, int | None] | None) -> None:
        try:
            found = bridge.call(ADAPTER, "find", state)
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.listed, found, then)

    # --- the list --------------------------------------------------------

    def listed(self, found: dict, then: tuple[int, int | None] | None) -> None:
        self.found = found
        self.order = [(row[0], row[1]) for row in found["rows"]]
        self.draw_list()
        status = self.query_one("#texts-status", Static)
        status.update(Ink()(found["tally"], "italic").content())
        works = self.query_one("#texts-works", Panel)
        works.retitle(f"works · {self.label_of('sort', found['state']['sort'])}")
        works.border_subtitle = "● read here · ○ PDF only or none · ◆ drift, advisory"
        self.draw_holdings(found)
        self.land(then or self.cursor)
        if self._intent:
            intent, self._intent = self._intent, {}
            self.follow(**intent)
        self.app.refresh_where()

    def draw_list(self) -> None:
        """One line per work and two per treatment, each cut to the list's width.

        A title cut short ends in an ellipsis; the whole of it stands in the
        treatment's card and record beside the list.
        """
        if not self.found:
            return
        works = self.opening["works"]
        listing = self.query_one("#texts-list", OptionList)
        width = max(12, listing.size.width - 1) if listing.size.width else 56
        self._drawn_width = width
        listing.clear_options()
        by_section = self.found["state"]["sort"] == "section"
        section = None
        options = []
        for at, shown in self.order:
            one = works[at]
            if by_section and one["section"] != section:
                section = one["section"]
                options.append(Option(Ink()(one["sectionLabel"], f"bold {ACCENT}").content(), disabled=True))
            parts = [] if by_section else [(one["sectionLabel"] + "  ", f"bold {ACCENT}")]
            parts.append((one["leaf"], "$text-muted"))
            options.append(Option(fitted(parts, width).content(), id=f"w-{at}"))
            for index in shown:
                row = one["treatments"][index]
                first = [("  ", ""), (f"{row['providerLabel']:<7}", f"bold {ACCENT}"),
                         (row["title"], "italic $warning" if row["unrecorded"] else "")]
                said = f"bold {ACCENT}" if row["web"] else ("$text-muted" if row["pdf"] else "italic $warning")
                second = [(" " * 9, ""), ("● " if row["web"] else "○ ", f"bold {ACCENT}" if row["web"] else "$text-muted"),
                          (availability(row), said),
                          (" · ", "$text-muted"),
                          (row["extent"] or "extent unrecorded", "$text-muted" if row["extent"] else "italic $warning")]
                if row["revised"]:
                    second.append((f" · revised {row['revised']}", "$text-muted"))
                if row["drift"]:
                    second.append((" · ◆ drift", "$warning"))
                ink = fitted(first, width)
                ink.line()
                options.append(Option(fitted(second, width, ink).content(), id=f"t-{at}-{index}"))
        if self.found.get("zero"):
            options.append(Option(Ink()(self.found["zero"], "italic $warning").content(), disabled=True))
        listing.add_options(options)

    def on_resize(self, event) -> None:
        super().on_resize(event)
        self.call_after_refresh(self.redraw_list)

    def redraw_list(self) -> None:
        if not self.found:
            return
        listing = self.query_one("#texts-list", OptionList)
        if (max(12, listing.size.width - 1) if listing.size.width else 56) != getattr(self, "_drawn_width", None):
            self.draw_list()
            self.land(self.cursor)

    def land(self, target: tuple[int, int | None] | None) -> None:
        """Put the cursor back where it was, if what it was on is still listed."""
        listing = self.query_one("#texts-list", OptionList)
        if target is None:
            return
        at, index = target
        ident = f"w-{at}" if index is None else f"t-{at}-{index}"
        try:
            position = listing.get_option_index(ident)
        except Exception:  # noqa: BLE001 - no longer listed under these choices
            # What the cursor was on is hidden now, so nothing stands in its place.
            self.cursor = None
            self.record = None
            self.query_one("#texts-cards", Horizontal).remove_children()
            self.welcome()
            return
        listing.highlighted = position
        self.call_after_refresh(listing.scroll_to_highlight, top=True)

    def draw_holdings(self, found: dict) -> None:
        held = found["holdings"]
        width = 18
        ink = Ink()
        total = held["held"]
        ink(f"{'readable here':<14}", "bold")
        meter(ink, held["readable"], total, width)(f" {held['readable']}/{total} documents").line()
        ink(f"{'PDF only':<14}", "bold")
        meter(ink, held["pdfOnly"], total, width)(f" {held['pdfOnly']}/{total}")
        for one in held["providers"]:
            ink.line()
            ink(f"{one['label']:<14}", "bold")
            meter(ink, one["documents"], held["providersOf"], width)(f" {one['documents']}/{held['providersOf']}")
        box = self.query_one("#texts-holdings", Panel)
        box.query_one("#texts-holdings-text", Static).update(ink.content())
        whole = found.get("whole") or 0
        box.border_subtitle = "of every document" if found["counted"]["documents"] == whole else "of these choices"

    @on(OptionList.OptionHighlighted, "#texts-list")
    def glanced(self, event: OptionList.OptionHighlighted) -> None:
        ident = event.option.id or ""
        if ident.startswith("w-"):
            self.cursor = (int(ident[2:]), None)
        elif ident.startswith("t-"):
            at, index = ident[2:].split("-")
            self.cursor = (int(at), int(index))
        else:
            return
        self.draw_cards()
        self.load_record()
        self.app.refresh_where()

    @on(OptionList.OptionSelected, "#texts-list")
    def chosen(self, event: OptionList.OptionSelected) -> None:
        if (event.option.id or "").startswith("t-"):
            self.action_read()

    # --- the work and its treatments --------------------------------------

    def shown_of(self, at: int) -> list[int]:
        return next((shown for work_at, shown in self.order if work_at == at), [])

    def draw_cards(self) -> None:
        cards = self.query_one("#texts-cards", Horizontal)
        cards.remove_children()
        if self.cursor is None:
            return
        at, chosen = self.cursor
        one = self.opening["works"][at]
        panels = []
        for index in self.shown_of(at):
            row = one["treatments"][index]
            ink = Ink()
            ink.line(row["title"], "bold italic $warning" if row["unrecorded"] else "bold")
            if row["unrecordedNote"]:
                ink("Not shown: ", "bold $warning").line(row["unrecordedNote"])
            facts = [row["extent"] or "extent unrecorded"]
            if row["revised"]:
                facts.append(f"revised {row['revised']}")
            ink.line(" · ".join(facts), "$text-muted")
            if row["drift"]:
                ink("◆ ", "$warning")(row["drift"]["words"])(" — advisory only", "italic $text-muted").line()
            if row["models"]:
                ink.line(" · ".join(row["models"]), "$text-muted")
            else:
                ink.line("authorship not stated", "italic $warning")
            if row["web"]:
                ink("● ", f"bold {ACCENT}")("Read here", f"bold {ACCENT}")(" — enter opens it", "$text-muted")
                ink.line()
            if row["pdf"]:
                self.pdf_line(ink, "PDF", row["pdf"], row["pdfHere"])
            elif row["pdfAbsent"]:
                ink("○ ", "$text-muted")(row["pdfAbsent"], "italic $warning").line()
            if not row["web"] and not row["pdf"] and not row["pdfAbsent"]:
                ink("○ ", "$warning")("No web edition and no PDF are recorded for this treatment, "
                                      "and the catalogue gives no reason", "italic $warning")
                ink(f"; its status is {row['status'] or 'not recorded'}.", "italic $warning").line()
            for issue in row["also"]:
                if issue["pdf"]:
                    pages = f", {issue['pages']}pp" if issue["pages"] is not None else ""
                    self.pdf_line(ink, issue["label"] + pages, issue["pdf"], issue["pdfHere"])
            card = Panel(Static(ink.content()), title=f"{row['providerLabel']} · independent treatment",
                         classes="texts-card" + (" chosen" if index == chosen else ""))
            if index == chosen:
                card.border_subtitle = "▲ the record below"
            panels.append(card)
        cards.mount_all(panels)

    @staticmethod
    def pdf_line(ink: Ink, label: str, path: str, here: bool) -> None:
        if here:
            ink("▪ ", "$text-muted")(f"{label}: ", "bold")(path).line()
        else:
            ink("▫ ", "$text-muted")(f"{label}: ", "bold")("recorded, not installed in this checkout",
                                                             "italic $text-muted").line()

    def load_record(self) -> None:
        self._token += 1
        if self.cursor is None or self.cursor[1] is None:
            self.record = None
            self.draw_work_record()
            return
        self.fetch_record(self._token, *self.cursor)

    @work(thread=True, exclusive=True, group="texts-record")
    def fetch_record(self, token: int, at: int, index: int) -> None:
        try:
            record = bridge.call(ADAPTER, "record", at, index)
        except Refused as refusal:
            record = {"refused": str(refusal)}
        self.deliver(self.draw_record, token, record)

    def draw_work_record(self) -> None:
        if self.cursor is None:
            return
        one = self.opening["works"][self.cursor[0]]
        shown = self.shown_of(self.cursor[0])
        ink = Ink()
        ink.line(one["leaf"], f"bold {ACCENT}")
        ink.line(f"{one['sectionLabel']} · " + (f"catalogued in {one['catalog']}" if one["catalog"]
                                                  else "no catalogue page recorded"), "$text-muted")
        ink.line()
        count = len(shown)
        ink.line(f"{count} treatment{'s' if count != 1 else ''} listed under these choices, each under the title "
                 "it prints. Move down to one for its full record.", "italic")
        held = len(one["treatments"])
        if held != count:
            ink.line(f"The catalogue holds {held} for this work; the others are hidden by the choices in force.",
                     "italic $text-muted")
        self.advisory(ink)
        self.query_one("#texts-record-text", Static).update(ink.content())
        box = self.query_one("#texts-record", ScrollPanel)
        box.retitle("work")
        box.border_subtitle = ""
        box.scroll_home(animate=False)

    def draw_record(self, token: int, record: dict) -> None:
        if token != self._token:
            return  # a later cursor move has superseded this record
        self.record = record
        box = self.query_one("#texts-record", ScrollPanel)
        ink = Ink()
        if record.get("refused"):
            ink.line(record["refused"], "bold $error")
            self.query_one("#texts-record-text", Static).update(ink.content())
            return
        ink.line(record["heading"], "bold italic $warning" if record["unrecorded"] else f"bold {ACCENT}")
        ink.line(record["sub"], "$text-muted")
        if record["notice"]:
            ink("Not shown: ", "bold $warning").line(record["notice"])
        ink.line()
        self.rows(ink, record["lines"])
        ink.line()
        ink.line("What produced it", f"bold underline {ACCENT}")
        for label, value, recorded in record["production"]:
            ink(f"{label:<18}", "bold")(value, "" if recorded else "italic $warning").line()
        drift = record["treatment"].get("drift")
        if drift:
            ink("◆ ", "$warning")(drift["words"]).line()
            ink.line(drift["title"], "italic $text-muted")
        ink.line()
        ink.line("In the browser", f"bold underline {ACCENT}")
        browser = record["browser"]
        ink(f"{browser['label']:<18}", "bold")(browser["value"]).line()
        if browser.get("basis"):
            ink(f"{browser['basis']:<18}", "bold")(browser.get("rationale") or "").line()
        if browser.get("blockedBy"):
            ink(f"{'Blocked by':<18}", "bold")(browser["blockedBy"]).line()
        ink.line()
        ink.line("Issues", f"bold underline {ACCENT}")
        for issue in record["issues"]:
            ink(f"{issue['kind']:<18}", "bold")(issue["said"])
            if issue["title"]:
                ink(f" · {issue['title']}", "italic")
            ink.line()
            ink(" " * 18)
            if issue["pdf"]:
                ink(issue["pdf"])
                ink(" — installed here" if issue["pdfHere"] else " — recorded, not installed in this checkout",
                    "italic $text-muted")
            elif issue["absent"]:
                ink(issue["absent"], "italic $warning")
            else:
                ink("no PDF recorded, and no reason is given", "italic $warning")
            ink.line()
        ink.line()
        ink.line("Authorship", f"bold underline {ACCENT}")
        authorship = record["authorship"]
        if authorship.get("inherited"):
            ink(f"{'Inherited from':<18}", "bold")(authorship["inherited"]).line()
            ink("Not shown: ", "bold $warning").line(authorship["notice"])
        elif authorship.get("contributions"):
            for one in authorship["contributions"]:
                ink.line(one["model"], f"bold {ACCENT}")
                self.rows(ink, [("Configuration", one["qualifiers"]), ("Agent and runtime", one["runtime"])])
        else:
            ink("Not shown: ", "bold $warning").line(authorship["notice"])
        self.advisory(ink)
        self.query_one("#texts-record-text", Static).update(ink.content())
        box.retitle(f"record · {record['treatment']['providerLabel']}")
        treatment = record["treatment"]
        box.border_subtitle = "enter reads the web edition" if treatment["web"] else "not rendered for the browser"
        box.scroll_home(animate=False)

    @staticmethod
    def rows(ink: Ink, pairs) -> None:
        for label, value in pairs:
            ink(f"{label:<18}", "bold")(value or "").line()

    # --- reading a web edition ---------------------------------------------

    def action_read(self) -> None:
        if self.cursor is None or self.cursor[1] is None:
            self.app.notify("Move to one treatment of the work to read it.")
            return
        at, index = self.cursor
        row = self.opening["works"][at]["treatments"][index]
        if not row["web"]:
            said = "This treatment has no web edition"
            if self.record and self.record.get("browser"):
                said += f" ({self.record['browser']['label'].lower()}: {self.record['browser']['value']})"
            self.app.notify(said + "; its record says why.", severity="warning")
            return
        width = self.app.size.width
        columns = min(96, int(width * 0.96)) - 7  # the Reading box: border, padding and scrollbar
        self.set_text(row, columns)

    @work(thread=True, exclusive=True, group="texts-read")
    def set_text(self, row: dict, columns: int) -> None:
        try:
            done = webedition.set_for_terminal(row["web"], columns, ACCENT)
        except Refused as refusal:
            done = {"refused": str(refusal)}
        self.deliver(self.open_reading, row, done)

    def open_reading(self, row: dict, done: dict) -> None:
        ink = Ink()
        ink.line(row["title"], f"bold {ACCENT}")
        facts = [f"{row['providerLabel']} · independent treatment"]
        if row["revised"]:
            facts.append(f"revised {row['revised']}")
        ink.line(" · ".join(facts), "$text-muted")
        if row["pdf"]:
            self.pdf_line(ink, "Canonical PDF", row["pdf"], row["pdfHere"])
        elif row["pdfAbsent"]:
            ink("○ ", "$text-muted")(row["pdfAbsent"], "italic $warning").line()
        for issue in row["also"]:
            if issue["pdf"]:
                pages = f", {issue['pages']}pp" if issue["pages"] is not None else ""
                self.pdf_line(ink, issue["label"] + pages, issue["pdf"], issue["pdfHere"])
        if done.get("refused"):
            ink.line()
            ink.line("The text is not set here.", "bold $warning")
            ink.line(done["refused"], "$warning")
            subtitle = "esc close"
        else:
            ink.line(f"Set from {done['source']} by the site's own Markdown renderer (Python-Markdown "
                     f"{done['markdown']}), then {done['pandoc'] or 'pandoc'}, at {done['columns']} columns.",
                     "italic $text-muted")
            ink.line("─" * min(40, done["columns"]), "$text-muted")
            ink.line()
            for text, style in done["runs"]:
                ink(text, style)
            subtitle = f"esc close · ↑ ↓ pgup pgdn home end · {done['source']}"
        self.app.push_screen(Reading(row["title"], ink.content(), subtitle,
                                     walks=False, source=False))

    # --- where, and being sent here ------------------------------------------

    def where(self) -> str:
        if self.cursor is not None and self.opening:
            one = self.opening["works"][self.cursor[0]]
            if self.cursor[1] is not None:
                return f"{one['leaf']} · {one['treatments'][self.cursor[1]]['providerLabel']}"
            return one["leaf"]
        return self.found.get("tally", "")

    def follow(self, leaf: str | None = None, provider: str | None = None, **_) -> None:
        if not leaf:
            return
        if not self.found:
            self._intent = {"leaf": leaf, "provider": provider}
            return
        self.locate(leaf, provider)

    @work(thread=True, exclusive=True, group="texts-locate")
    def locate(self, leaf: str, provider: str | None) -> None:
        try:
            found = bridge.call(ADAPTER, "locate", leaf, provider or "")
        except Refused as refusal:
            found = {"problem": str(refusal)}
        self.deliver(self.located, found)

    def located(self, found: dict) -> None:
        if found.get("problem"):
            # A cited treatment that is not held is refused where its record would be; nothing else is chosen.
            self.cursor = None
            self.query_one("#texts-cards", Horizontal).remove_children()
            self.query_one("#texts-record-text", Static).update(
                Ink().line("This address cannot be followed", "bold $warning").line(found["problem"]).content())
            self.app.notify(found["problem"], severity="warning")
            return
        target = (found["work"], found["edition"])
        listed = target[0] in {at for at, _ in self.order} and (
            target[1] is None or target[1] in self.shown_of(target[0]))
        if listed:
            self.land(target)
            return
        self.app.notify("The choices in force hid what was asked for, so they are cleared.")
        self.state = {"author": "", "edition": "", "section": "", "reading": "", "sort": self.state["sort"], "find": ""}
        query = self.query_one("#texts-query", Input)
        with query.prevent(Input.Changed):
            query.value = ""
        self.draw_controls()
        self.refind(then=target)
