"""The Propers of the Mass: any formulary of any missal, read without a date."""
from __future__ import annotations

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge, missal
from ..dialogs import Pick
from ..repo import Refused
from ..surface import Surface
from ..widgets import Ink, Panel, ScrollPanel

ADAPTER = "liturgy"
SEARCHED = "titles, keys, kinds, seasons, fixed dates, incipits, citations and witnesses"


class Propers(Surface):
    key = "2"
    label = "Propers"
    HELP = (
        ("/", "search this missal's formularies"),
        ("escape", "leave the search box"),
        ("enter", "read the highlighted formulary"),
        ("c", "next missal"),
        ("o", "orations in English or Latin"),
        ("b", "next Bible edition"),
        ("w", "choose an oration witness"),
        ("s", "choose a form, a lectionary cycle or a source choice"),
        ("m", "missal mode: these propers seated in the Ordinary"),
        ("r", "rubrics shown or hidden in missal mode"),
        ("f", "focus: the reading alone, full width; again to restore"),
    )
    BINDINGS = [
        Binding("slash", "search", "search"),
        Binding("c", "calendar", "missal"),
        Binding("o", "orations", "en/la"),
        Binding("b", "bible", "bible", show=False),
        Binding("w", "witness", "witness", show=False),
        Binding("s", "choose", "choose"),
        Binding("m", "missal", "missal mode"),
        Binding("r", "rubrics", "rubrics", show=False),
    ]
    CSS = """
    .propers.focus #propers-left { display: none; }
    .propers.narrow #propers-left { width: 34; }
    """
    DEFAULT_CSS = """
    Propers #propers-left { width: 52; }
    Propers #propers-find { height: auto; }
    Propers #propers-find Input { border: none; background: $surface; height: 1; padding: 0 1; }
    Propers #propers-status { color: $text-muted; height: auto; }
    Propers #propers-list-box { height: 1fr; }
    """

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.calendars: list[dict] = []
        self.calendar = ""
        self.bibles: list[dict] = []
        self.bible = ""
        self.orations = "en"
        self.ordinary = False
        self.rubrics = True
        self.catalogues: dict[str, dict] = {}
        self.shown: list[int] = []
        self.reading: tuple[str, str, str | None] | None = None
        self.choices: dict[tuple, dict] = {}
        self.view: dict | None = None
        self.opening: dict = {}
        self._intent: dict = {}

    def build(self) -> None:
        self.mount(
            Horizontal(
                Vertical(
                    Panel(Static("", id="propers-missals"), Input(placeholder="Title, incipit, citation, MM-DD, witness…",
                                                                   id="propers-query"),
                          Static("", id="propers-status"), title="find a formulary", id="propers-find"),
                    Panel(OptionList(id="propers-list"), title="formularies", id="propers-list-box"),
                    id="propers-left",
                ),
                ScrollPanel(Static("", id="propers-text"), title="propers", id="propers-reading"),
            )
        )
        self.start()

    @work(thread=True, exclusive=True, group="propers-start")
    def start(self) -> None:
        try:
            opening = bridge.call(ADAPTER, "opening")
        except Refused as refusal:
            self.app.call_from_thread(self.fail, str(refusal))
            return
        self.app.call_from_thread(self.opened_with, opening)

    def opened_with(self, opening: dict) -> None:
        self.opening = opening
        self.calendars = opening["calendars"]
        self.bibles = opening["bibles"]
        ids = [one["id"] for one in self.calendars]
        if self.calendar not in ids:
            self.calendar = opening.get("default") if opening.get("default") in ids else ids[0]
        self.bible = self.bible or self.bibles[0]["id"]
        self.welcome()
        self.list_calendar()
        if self._intent.get("mass"):
            self.read(self.calendar, self._intent["mass"], None)

    def fail(self, message: str) -> None:
        self.query_one("#propers-text", Static).update(Ink()(message, "bold $error").content())

    def follow(self, calendar: str | None = None, mass: str | None = None, **_) -> None:
        if calendar:
            self.calendar = calendar
        if not self.calendars:
            self._intent = {"mass": mass}
            return
        self.list_calendar()
        if mass:
            self.read(self.calendar, mass, None)

    def welcome(self) -> None:
        ink = Ink()
        ink.line("Choose a formulary to read.", "bold")
        ink.line()
        ink.line("Propers are read independently of a civil date: a formulary's fixed date in the list is the date "
                 "its source declares, not a claim about when it is celebrated. To read the Mass a date appoints, "
                 "use the day surface (1), where p opens its formulary here.", "italic $text-muted")
        ink.line()
        ink.line("Nothing is opened for you: the list is the missal's own order, searched by the page's own search.",
                 "italic $text-muted")
        self.query_one("#propers-text", Static).update(ink.content())

    # --- the list ----------------------------------------------------------

    def list_calendar(self) -> None:
        names = Ink()
        for one in self.calendars:
            chosen = one["id"] == self.calendar
            short = one["short"].replace(" Missal", "")
            names(f" {short} ", "bold reverse $propers-color" if chosen else "$text-muted")(" ")
        names("c", "bold $hotkey")
        self.query_one("#propers-missals", Static).update(names.content())
        self.load_catalogue(self.calendar)

    @work(thread=True, exclusive=True, group="propers-catalogue")
    def load_catalogue(self, calendar: str) -> None:
        try:
            if calendar not in self.catalogues:
                self.catalogues[calendar] = bridge.call(ADAPTER, "catalogue", calendar)
        except Refused as refusal:
            self.app.call_from_thread(self.fail, str(refusal))
            return
        query = self.query_one("#propers-query", Input).value
        self.app.call_from_thread(self.filter, query)

    @on(Input.Changed, "#propers-query")
    def typed(self, event: Input.Changed) -> None:
        self.find(event.value)

    @work(thread=True, exclusive=True, group="propers-find")
    def find(self, query: str) -> None:
        if self.calendar not in self.catalogues:
            return
        self.app.call_from_thread(self.filter, query)

    def filter(self, query: str) -> None:
        catalogue = self.catalogues.get(self.calendar)
        if not catalogue:
            return
        rows = catalogue["rows"]
        if query.strip():
            try:
                ordinals = bridge.call(ADAPTER, "search", self.calendar, query)
            except Refused as refusal:
                self.fail(str(refusal))
                return
        else:
            ordinals = list(range(len(rows)))
        self.shown = ordinals
        listing = self.query_one("#propers-list", OptionList)
        listing.clear_options()
        season = None
        for ordinal in ordinals:
            row = rows[ordinal]
            if not query.strip() and row.get("season") != season:
                season = row.get("season")
                listing.add_option(Option(Ink()((season or row.get("kind") or "").replace("-", " "),
                                                "bold $propers-color").content(), disabled=True))
            ink = Ink()(row["name"])
            if row.get("form_name"):
                ink(f" · {row['form_name']}", "italic")
            ink.line()
            ink(f"  {row['kind']}", "$text-muted")
            if row.get("fixed_date"):
                ink(f" · {row['fixed_date']}", "$text-muted")
            listing.add_option(Option(ink.content(), id=f"row-{ordinal}"))
        first = next((index for index in range(listing.option_count)
                      if not listing.get_option_at_index(index).disabled), None)
        if first is not None:
            listing.highlighted = first
        status = self.query_one("#propers-status", Static)
        edition = catalogue.get("short") or self.calendar
        if query.strip() and not ordinals:
            status.update(Ink()(f"No formulary in {edition} matches {query!r}. The search covers {SEARCHED}; "
                                "nothing nearby is offered in its place.", "italic $warning").content())
        elif query.strip():
            status.update(Ink()(f"Showing {len(ordinals)} of {len(rows)} form-qualified results in {edition}.",
                                "italic").content())
        else:
            status.update(Ink()(f"{len(rows)} form-qualified formularies in {edition}.", "italic").content())
        self.query_one("#propers-list-box", Panel).retitle(f"formularies · {edition}")

    def action_search(self) -> None:
        self.query_one("#propers-query", Input).focus()

    def key_escape(self) -> None:
        if self.query_one("#propers-query", Input).has_focus:
            self.query_one("#propers-list", OptionList).focus()

    @on(Input.Submitted, "#propers-query")
    def submitted(self) -> None:
        self.query_one("#propers-list", OptionList).focus()

    @on(OptionList.OptionSelected, "#propers-list")
    def picked(self, event: OptionList.OptionSelected) -> None:
        if not (event.option.id or "").startswith("row-"):
            return
        row = self.catalogues[self.calendar]["rows"][int(event.option.id[4:])]
        form = row["form_id"] if row.get("form_id") and row["form_id"] != "main" else None
        self.read(self.calendar, row["key"], form)

    # --- reading -----------------------------------------------------------

    def selection(self) -> dict:
        if not self.reading:
            return {}
        return self.choices.setdefault(self.reading, {})

    def read(self, calendar: str, key: str, form: str | None) -> None:
        self.reading = (calendar, key, form)
        self.fetch()

    def options(self) -> dict:
        calendar, key, form = self.reading
        options = {"orations": self.orations, "bible": self.bible, "ordinary": self.ordinary,
                   "ordinaryLang": self.orations}
        if form:
            options["form"] = form
        options.update({name: value for name, value in self.selection().items() if value})
        return options

    @work(thread=True, exclusive=True, group="propers-read")
    def fetch(self) -> None:
        if not self.reading:
            return
        calendar, key, _ = self.reading
        try:
            view = bridge.call(ADAPTER, "propers", calendar, key, self.options())
        except Refused as refusal:
            view = {"refused": str(refusal), "calendar": calendar, "key": key}
        self.app.call_from_thread(self.show, view)

    def where(self) -> str:
        mass = (self.view or {}).get("mass") or {}
        edition = next((one["short"] for one in self.calendars if one["id"] == self.calendar), self.calendar)
        return f"{edition} · {mass.get('name') or 'browse'}"

    def show(self, view: dict) -> None:
        self.view = view
        box = self.query_one("#propers-reading", ScrollPanel)
        text = self.query_one("#propers-text", Static)
        ink = Ink()
        if view.get("refused"):
            box.retitle("propers")
            text.update(ink.line(view["refused"], "bold $error").content())
            return
        mass = view.get("mass") or {}
        state = view.get("state") or {}
        edition = mass.get("editionShort") or view["calendar"]
        box.retitle(f"{mass.get('name') or view['key']} · {edition}")
        mode = "missal" if state.get("ordinary") else "read"
        language = "English" if state.get("orations") == "en" else "Latin"
        extra = []
        if state.get("form"):
            extra.append(f"form {state['form']}")
        if state.get("cycle"):
            extra.append(f"year {state['cycle']}")
        box.border_subtitle = " · ".join([mode, f"{language} orations", view["bible"]["label"], *extra])
        ink(mass.get("name") or view["key"], "bold $propers-color")
        if mass.get("kind"):
            ink(f"  ·  {mass['kind']}", "$text-muted")
        if mass.get("season"):
            ink(f"  ·  {mass['season'].replace('-', ' ')}", "$text-muted")
        ink.line()
        # page: propers-reader.js:634
        ink.line("Propers are read independently of a civil date", "italic $text-muted")
        for absence in view.get("explicitAbsences") or []:
            reason = absence.get("reason") or ""
            if " " in reason:
                ink.line(reason, "italic $text-muted")
        ink.line()
        missal.choices(ink, view)
        if mass.get("recension"):
            ink.line(str(mass["recension"]), "italic $warning")
        if mass.get("coverage"):
            ink.line(mass["coverage"], "italic $text-muted")
        if state.get("ordinary") and (view.get("ordinary") or {}).get("advisory"):
            ink.line(view["ordinary"]["advisory"], "italic $text-muted")
        missal.events(ink, view, rubrics=self.rubrics, accent="$propers-color")
        text.update(ink.content())
        box.scroll_home(animate=False)
        self.app.refresh_where()

    # --- controls ----------------------------------------------------------

    def action_calendar(self) -> None:
        ids = [one["id"] for one in self.calendars]
        if ids:
            self.calendar = ids[(ids.index(self.calendar) + 1) % len(ids)]
            self.list_calendar()

    def again(self) -> None:
        if self.reading:
            self.fetch()

    def action_orations(self) -> None:
        self.orations = "la" if self.orations == "en" else "en"
        for selection in self.choices.values():
            selection.pop("witness", None)
        self.again()

    def action_bible(self) -> None:
        ids = [one["id"] for one in self.bibles]
        if ids:
            self.bible = ids[(ids.index(self.bible) + 1) % len(ids)] if self.bible in ids else ids[0]
            self.again()

    def action_missal(self) -> None:
        self.ordinary = not self.ordinary
        self.again()

    def action_rubrics(self) -> None:
        self.rubrics = not self.rubrics
        if self.view:
            self.show(self.view)

    def action_witness(self) -> None:
        witnesses = ((self.view or {}).get("mass") or {}).get("witnesses") or []
        if not witnesses:
            self.app.notify("No oration witness in this language is recorded for this missal.")
            return
        offers = [("", "every held witness, each named (no single witness chosen)")]
        offers += [(one["source_id"], f"{one['label'] or 'Triptych'}  ·  {one['held']} held") for one in witnesses]

        def picked(value) -> None:
            if value is None:
                return
            if value:
                self.selection()["witness"] = value
            else:
                self.selection().pop("witness", None)
            self.again()

        self.app.push_screen(Pick("oration witness", offers,
                                  "A missing text stays missing; no other witness fills it."), picked)

    def action_choose(self) -> None:
        view = self.view or {}
        offers = []
        for choice in view.get("unresolvedChoices") or []:
            ident = choice.get("id") or ""
            for option in choice.get("options") or []:
                offers.append(((ident, option["id"]), f"{missal.option_label(choice, option, view)}"
                                                      f"   ({choice.get('reason') or ident})"))
        cycles: list[str] = []
        for event in view.get("events") or []:
            selected = event.get("selected") or {}
            if selected.get("kind") == "cycle-alternatives":
                for cycle in selected.get("cycles") or []:
                    if cycle not in cycles:
                        cycles.append(cycle)
            if event.get("kind") == "proper-choice":
                for option in event.get("options") or []:
                    offers.append((("proper-choice", event["id"], option["id"]),
                                   f"{event.get('group')}  →  option {option['id']}"))
        offers += [(("cycle", cycle), f"Year {cycle}   (the lectionary cycle)") for cycle in cycles]
        if self.selection().get("cycle"):
            offers.append((("cycle", None), "every cycle, kept apart (no year chosen)"))
        if not offers:
            self.app.notify("Nothing in this formulary is left open for the reader to choose.")
            return

        def picked(value) -> None:
            if not value:
                return
            selection = self.selection()
            kind = value[0]
            if kind.startswith("proper-form"):
                self.reading = (self.reading[0], self.reading[1], value[1])
            elif kind == "cycle":
                selection["cycle"] = value[1]
            elif kind == "proper-choice":
                selection.setdefault("properChoices", {})[value[1]] = value[2]
            elif kind.startswith("translation-witness"):
                selection["witness"] = value[1]
            else:
                self.app.notify(f"This reader cannot make the choice {kind!r} yet.", severity="warning")
                return
            self.again()

        self.app.push_screen(Pick("choose", offers, "The sources leave this open. Nothing is chosen by order."),
                             picked)
