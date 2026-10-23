"""The Propers of the Mass: any formulary of any missal, read without a date."""
from __future__ import annotations

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge, missal
from ..dialogs import Ask, Pick, Reading
from ..reader_navigation import ReadingNavigation, share
from ..repo import Refused
from ..surface import Surface
from ..widgets import Ink, Panel, ScrollPanel

ADAPTER = "liturgy"
SEARCHED = "titles, keys, kinds, seasons, fixed dates, incipits, citations and witnesses"


class Propers(Surface):
    key = "2"
    label = "Propers"
    FIRST = "#propers-list"
    HELP = (
        ("/", "search this missal's formularies"),
        ("escape", "leave the search box"),
        ("enter", "read the highlighted formulary"),
        ("c", "next missal"),
        ("o", "orations in English or Latin"),
        ("b", "next Bible edition"),
        ("B", "pair Latin and the selected language"),
        ("L", "choose the Ordinary language independently"),
        ("K", "choose a named Latin Bible companion, or remove it"),
        ("i", "Contents: move to a semantic liturgical unit"),
        ("u", "copy the canonical website URL for this reading"),
        ("g", "open a Day or Propers reader URL"),
        ("d", "Study: coverage, placement and source records"),
        ("v / V", "compare this formulary / choose a comparison"),
        ("[ / ]", "previous / next formulary in this browse or search result"),
        ("w", "choose an oration witness"),
        ("s", "choose a form, a lectionary cycle or a source choice"),
        ("m", "missal mode: these propers seated in the Ordinary"),
        ("r", "rubrics shown or hidden in missal mode"),
        ("f", "show or hide navigation panes; narrow screens start with the reading"),
    )
    BINDINGS = [
        Binding("slash", "search", "search"),
        Binding("c", "calendar", "missal"),
        Binding("o", "orations", "language"),
        Binding("b", "bible", "bible", show=False),
        Binding("B", "bilingual", "bilingual", show=False),
        Binding("L", "ordinary_language", "Ordinary language", show=False),
        Binding("K", "companion", "Latin Bible", show=False),
        Binding("i", "contents", "contents"),
        Binding("u", "share", "share", show=False),
        Binding("g", "open_url", "open URL", show=False),
        Binding("d", "study", "study"),
        Binding("v", "compare", "compare"),
        Binding("V", "comparison", "compare choices", show=False),
        Binding("left_square_bracket", "step(-1)", "previous formulary", show=False),
        Binding("right_square_bracket", "step(1)", "next formulary", show=False),
        Binding("w", "witness", "witness", show=False),
        Binding("s", "choose", "choose"),
        Binding("m", "missal", "missal mode"),
        Binding("r", "rubrics", "rubrics", show=False),
    ]
    CSS = """
    .propers.focus #propers-left { display: none; }
    .propers.narrow #propers-left { width: 32; }
    .propers.compact #propers-left { display: none; }
    .propers.compact.navigation #propers-left { display: block; width: 1fr; margin-right: 0; }
    .propers.compact.navigation #propers-reading { display: none; }
    .propers #propers-reading { padding: 1 3; align: center top; }
    .propers.narrow #propers-reading { padding: 1 2; }
    .propers #propers-text { max-width: 78; }
    """
    DEFAULT_CSS = """
    Propers #propers-left { width: 38; margin-right: 1; }
    Propers #propers-find { height: auto; }
    Propers #propers-find Input { border: none; background: $panel; height: 3; padding: 1; }
    Propers #propers-status { color: $text-muted; height: auto; }
    Propers #propers-list-box { height: 1fr; }
    """

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.calendars: list[dict] = []
        self.calendar = ""
        self.bibles: list[dict] = []
        self.bible = ""
        self.orations = ""
        self.ordinary_language = ""
        self.text_display = "selected"
        self.companion = ""
        self.navigation = ReadingNavigation()
        self.pending_study = False
        self.url_legacy: dict = {}
        self.comparison: dict | None = None
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
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.opened_with, opening)

    def opened_with(self, opening: dict) -> None:
        self.opening = opening
        self.calendars = opening.get("propersCalendars") or opening["calendars"]
        self.bibles = opening["bibles"]
        self.bible = self.bible or opening.get("defaultBible") or self.bibles[0]["id"]
        self.orations = self.orations or opening.get("defaultOrations") or "la"
        self.ordinary_language = self.ordinary_language or opening.get("defaultOrdinaryLanguage") or "en"
        ids = [one["id"] for one in self.calendars]
        if self.calendar not in ids:
            if self.calendar:
                self.fail(f"No missal called {self.calendar!r} is offered here. Choose a held missal with c.")
                return
            self.calendar = opening.get("default") if opening.get("default") in ids else ids[0]
        self.welcome()
        self.list_calendar()
        if self._intent.get("mass"):
            self.reading = (self.calendar, self._intent["mass"], self._intent.get("form"))
            self.selection().update(self._intent.get("selection") or {})
            self.fetch()

    def fail(self, message: str) -> None:
        self.query_one("#propers-text", Static).update(Ink()(message, "bold $error").content())

    def follow(self, calendar: str | None = None, mass: str | None = None, form: str | None = None,
               **options) -> None:
        if calendar:
            self.calendar = calendar
        for key, attribute in (("bible", "bible"), ("orations", "orations"), ("ordinary", "ordinary"),
                               ("ordinaryLang", "ordinary_language"), ("textDisplay", "text_display"),
                               ("companion", "companion"), ("urlLegacy", "url_legacy")):
            if key in options:
                setattr(self, attribute, options[key])
        selection = {name: options[name] for name in ("cycle", "witness", "properChoices", "variants", "alternative")
                     if name in options}
        self.navigation.pending = options.get("location")
        self.pending_study = bool(options.get("study"))
        self.comparison = options.get("comparison")
        if not self.calendars:
            self._intent = {"mass": mass, "form": form, "selection": selection}
            return
        self.list_calendar()
        if options.get("browse"):
            self.reading = None
            self.view = None
            self.welcome()
            self.remove_class("focus")
            self.add_class("navigation")
            self.call_after_refresh(self.query_one("#propers-list", OptionList).focus)
            return
        if mass:
            self.reading = (self.calendar, mass, form)
            if options.get("replace"):
                self.choices[self.reading] = {}
            self.selection().update(selection)
            self.fetch()

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
        self.query_one("#propers-missals", Static).update(names.content())
        self.load_catalogue(self.calendar)

    @work(thread=True, exclusive=True, group="propers-catalogue")
    def load_catalogue(self, calendar: str) -> None:
        try:
            if calendar not in self.catalogues:
                self.catalogues[calendar] = bridge.call(ADAPTER, "catalogue", calendar)
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.again_find)

    def again_find(self) -> None:
        self.find(self.calendar, self.query_one("#propers-query", Input).value)

    @on(Input.Changed, "#propers-query")
    def typed(self, event: Input.Changed) -> None:
        self.find(self.calendar, event.value)

    @work(thread=True, exclusive=True, group="propers-find")
    def find(self, calendar: str, query: str) -> None:
        """The page's own search, off the screen's thread; the list is drawn
        only if the missal and the words are still the ones asked about."""
        catalogue = self.catalogues.get(calendar)
        if not catalogue:
            return
        try:
            ordinals = (bridge.call(ADAPTER, "search", calendar, query) if query.strip()
                        else list(range(len(catalogue["rows"]))))
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.filter, calendar, query, ordinals)

    def filter(self, calendar: str, query: str, ordinals: list[int]) -> None:
        catalogue = self.catalogues.get(calendar)
        if not catalogue or calendar != self.calendar:
            return
        rows = catalogue["rows"]
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
            ink.line()
            key = row["key"] if len(row["key"]) <= 29 else row["key"][:28] + "…"
            ink(f"  {key}", "$text-muted")
            counts = row.get("coverageCounts") or []
            if counts:
                ink.line().line("  " + " · ".join(f"{one['lang']} {one['available']}/{one['occurrences']}"
                                                   for one in counts), "italic $text-muted")
            listing.add_option(Option(ink.content(), id=f"row-{ordinal}"))
        active = None
        if self.reading and self.reading[0] == calendar:
            active = next((f"row-{ordinal}" for ordinal in ordinals if rows[ordinal]["key"] == self.reading[1]
                           and (rows[ordinal].get("form_id") or "main") == (self.reading[2] or "main")), None)
        first = (listing.get_option_index(active) if active else
                 next((index for index in range(listing.option_count)
                       if not listing.get_option_at_index(index).disabled), None))
        if first is not None:
            listing.highlighted = first
            if active:
                self.call_after_refresh(listing.scroll_to_highlight)
        status = self.query_one("#propers-status", Static)
        edition = catalogue.get("short") or self.calendar
        if query.strip() and not ordinals:
            status.update(Ink()(f"No formulary in {edition} matches {query!r}. The search covers {SEARCHED}; "
                                "nothing nearby is offered in its place.", "italic $warning").content())
        elif query.strip():
            status.update(Ink()(f"Showing {len(ordinals)} of {len(rows)} form-qualified results in {edition}.",
                                "italic").content())
        else:
            status.update(Ink()(f"{len(rows)} form-qualified formularies in {edition}. Counts: composed text; Bible separate.",
                                "italic").content())
        self.query_one("#propers-list-box", Panel).retitle(f"formularies · {edition}")

    def action_search(self) -> None:
        self.remove_class("focus")
        self.add_class("navigation")
        self.call_after_refresh(self.query_one("#propers-query", Input).focus)

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
        self.comparison = None
        self.fetch()

    def action_step(self, step: int) -> None:
        if not self.reading or self.reading[0] != self.calendar:
            self.app.notify("Choose a formulary in this browse or search result first.")
            return
        rows = (self.catalogues.get(self.calendar) or {}).get("rows") or []
        matches = [index for index, ordinal in enumerate(self.shown)
                   if rows[ordinal]["key"] == self.reading[1] and
                   (rows[ordinal].get("form_id") or "main") == (self.reading[2] or "main")]
        if len(matches) != 1 or not 0 <= matches[0] + step < len(self.shown):
            self.app.notify("No further formulary in the current browse or search result.")
            return
        ordinal = self.shown[matches[0] + step]
        row = rows[ordinal]
        form = row.get("form_id")
        self.read(self.calendar, row["key"], None if form == "main" else form)
        listing = self.query_one("#propers-list", OptionList)
        listing.highlighted = listing.get_option_index(f"row-{ordinal}")

    def options(self) -> dict:
        calendar, key, form = self.reading
        options = {"orations": self.orations, "bible": self.bible, "ordinary": self.ordinary,
                   "ordinaryLang": self.ordinary_language or self.orations, "textDisplay": self.text_display,
                   "companion": self.companion, "urlLegacy": self.url_legacy}
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
            if self.comparison:
                try:
                    view["comparison"] = bridge.call(ADAPTER, "comparePropers", calendar, key,
                                                     self.options(), self.comparison)
                except Refused as refusal:
                    view["comparison"] = {"refused": str(refusal)}
        except Refused as refusal:
            view = {"refused": str(refusal), "calendar": calendar, "key": key}
        self.deliver(self.show, view)

    def where(self) -> str:
        mass = (self.view or {}).get("mass") or {}
        calendar = (self.view or {}).get("calendar") or self.calendar
        edition = next((one["short"] for one in self.calendars if one["id"] == calendar), "")
        return " · ".join(part for part in (edition, mass.get("name") or "choose a formulary") if part)

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
        if state.get("textDisplay") == "latin-and-selected":
            extra.append("Latin paired with selected language")
        if state.get("ordinary"):
            extra.append(f"{state.get('ordinaryLang') or state.get('orations')} Ordinary")
        if state.get("companion"):
            extra.append(f"Latin Bible: {state['companion']}")
        box.border_subtitle = " · ".join([mode, f"{language} orations", view["bible"]["label"], *extra])
        ink(mass.get("name") or view["key"], "bold $propers-color")
        if mass.get("kind"):
            ink(f"  ·  {mass['kind']}", "$text-muted")
        if mass.get("season"):
            ink(f"  ·  {mass['season'].replace('-', ' ')}", "$text-muted")
        ink.line()
        ink.line(view["key"], "$text-muted")
        # page: propers-reader.js:634
        ink.line("Propers are read independently of a civil date", "italic $text-muted")
        for absence in view.get("explicitAbsences") or []:
            reason = absence.get("reason") or ""
            if " " in reason:
                ink.line(reason, "italic $text-muted")
        ink.line()
        missal.choices(ink, view)
        if view.get("notice"):
            ink.line(view["notice"], "italic $warning")
        if state.get("ordinary") and (view.get("ordinary") or {}).get("advisory"):
            ink.line(view["ordinary"]["advisory"], "italic $text-muted")
        self.navigation.begin((view["calendar"], view["key"], state.get("form")), box, text)
        compared = view.get("comparison")
        if compared:
            box.border_subtitle = f"compare · {compared.get('title') or 'unsupported selection'} · v reading · V choices"
            if compared.get("refused"):
                ink.line("This comparison cannot be made as asked", "bold $warning")
                ink.line(compared["refused"], "italic $warning")
            else:
                missal.blocks(ink, compared.get("lead") or [], accent="$propers-color")
                for section in compared.get("sections") or []:
                    self.navigation.mark(section["id"], section["label"], ink)
                    missal.blocks(ink, section["blocks"], accent="$propers-color")
        else:
            for path in view.get("sourcePaths") or []:
                if not path.get("beforeEventId"):
                    missal.blocks(ink, path["blocks"], accent="$propers-color")
            for event in view.get("events") or []:
                if not self.rubrics and (event.get("element") or {}).get("kind") == "rubric":
                    continue
                for path in view.get("sourcePaths") or []:
                    if path.get("beforeEventId") == event["id"]:
                        missal.blocks(ink, path["blocks"], accent="$propers-color")
                label = event.get("slot") or event.get("name") or (event.get("element") or {}).get("name") or event["id"]
                self.navigation.mark(event["id"], label, ink)
                missal.events(ink, {**view, "events": [event]}, rubrics=self.rubrics, accent="$propers-color")
        text.update(ink.content())
        self.navigation.finish(self, box, text)
        self.show_reading_pane()
        self.app.refresh_where()
        if self.pending_study:
            self.pending_study = False
            self.action_study()

    # --- controls ----------------------------------------------------------

    def action_calendar(self) -> None:
        ids = [one["id"] for one in self.calendars]
        if ids:
            self.calendar = ids[(ids.index(self.calendar) + 1) % len(ids)] if self.calendar in ids else ids[0]
            self.list_calendar()

    def again(self) -> None:
        if self.reading:
            self.fetch()

    def action_orations(self) -> None:
        self.orations = "la" if self.orations == "en" else "en"
        for selection in self.choices.values():
            selection.pop("witness", None)
        self.again()

    def action_bilingual(self) -> None:
        self.text_display = "selected" if self.text_display == "latin-and-selected" else "latin-and-selected"
        self.again()

    def action_companion(self) -> None:
        offers = [("", "no Latin Bible companion")]
        offers += [(one["id"], one["label"]) for one in self.bibles if one.get("language") == "la"]

        def picked(value) -> None:
            if value is not None:
                self.companion = value
                self.again()

        self.app.push_screen(Pick("Latin Bible companion", offers,
                                  "Each edition retains its own numbering, provenance and refusals."), picked)

    def action_contents(self) -> None:
        self.navigation.choose(self, self.query_one("#propers-reading", ScrollPanel),
                               self.query_one("#propers-text", Static))

    @work(thread=True, exclusive=True, group="propers-share")
    def action_share(self) -> None:
        if not self.reading:
            return
        calendar, key, _ = self.reading
        options = self.options()
        options["location"] = self.navigation.current(self.query_one("#propers-reading", ScrollPanel),
                                                      self.query_one("#propers-text", Static))
        try:
            route = bridge.call(ADAPTER, "readerUrl", "propers", calendar, key, options, self.comparison)
        except Refused as refusal:
            self.deliver(self.app.notify, str(refusal), severity="warning")
            return
        self.deliver(share, self, route)

    def action_open_url(self) -> None:
        self.app.push_screen(Ask("open a reader URL", "Paste a canonical or retained Day or Propers link."),
                             lambda value: value and self.open_link(value))

    @work(thread=True, exclusive=True, group="propers-open-url")
    def open_link(self, value: str) -> None:
        try:
            target = bridge.call(ADAPTER, "openReaderLink", value, "propers")
        except Refused as refusal:
            self.deliver(self.app.notify, str(refusal), severity="warning")
            return
        self.deliver(self.app.action_surface, target["entrance"], **target["intent"])

    def action_ordinary_language(self) -> None:
        ordinary = (self.view or {}).get("ordinary") or {}
        languages = [(one["lang"], one.get("label") or one.get("name") or one["lang"])
                     for one in ordinary.get("languages") or []]
        if not languages:
            self.app.notify("Open Missal mode (m) to choose this edition's Ordinary language.")
            return

        def picked(value) -> None:
            if value:
                self.ordinary_language = value
                self.again()

        self.app.push_screen(Pick("Ordinary language", languages,
                                  "The oration language stays independently selected; unavailable text stays explicit."),
                             picked)

    @work(thread=True, exclusive=True, group="propers-study")
    def action_study(self) -> None:
        if not self.reading:
            return
        calendar, key, _ = self.reading
        try:
            blocks = bridge.call(ADAPTER, "studyPropers", calendar, key, self.options())
        except Refused as refusal:
            self.deliver(self.app.notify, str(refusal), severity="warning")
            return
        self.deliver(self.app.push_screen, Reading("Study this formulary",
                     missal.blocks(Ink(), blocks, accent="$propers-color").content(), walks=False))

    def action_compare(self) -> None:
        if self.comparison:
            self.map_comparison_location(None)
            self.comparison = None
            self.again()
        else:
            self.action_comparison()

    def map_comparison_location(self, dimension: str | None) -> None:
        current = self.navigation.current(self.query_one("#propers-reading", ScrollPanel),
                                          self.query_one("#propers-text", Static))
        maps = (self.view or {}).get("navigation") or {}
        if self.comparison:
            current = ((maps.get("fromCompare") or {}).get(self.comparison["dimension"]) or {}).get(current)
        if dimension:
            current = ((maps.get("compare") or {}).get(dimension) or {}).get(current)
        self.navigation.pending = current
        if not current:
            self.navigation.identity = None

    def action_comparison(self) -> None:
        offers = (self.view or {}).get("comparisonOffers") or []
        if not offers:
            self.app.notify("Choose an exact formulary with supported comparison peers first.")
            return

        def dimension_chosen(dimension) -> None:
            if not dimension:
                return
            offer = next(one for one in offers if one["dimension"] == dimension)
            peers = [(one["id"], one["label"]) for one in offer["options"]]

            def primary_chosen(primary) -> None:
                if primary is None:
                    return

                def peer_chosen(peer) -> None:
                    if peer is not None:
                        self.map_comparison_location(dimension)
                        self.comparison = {"dimension": dimension, "primary": primary, "peer": peer}
                        self.again()

                self.app.push_screen(Pick("second comparison side", [(ident, label) for ident, label in peers
                                                                        if ident != primary],
                                          "The formulary stays independent of a date."), peer_chosen)

            self.app.push_screen(Pick("first comparison side", peers, "Choose both peers explicitly."), primary_chosen)

        self.app.push_screen(Pick("compare this formulary", [(one["dimension"], one["label"]) for one in offers],
                                  "Semantic slots are paired by the page's comparison model."), dimension_chosen)

    def action_bible(self) -> None:
        ids = [one["id"] for one in self.bibles]
        if ids:
            self.bible = ids[(ids.index(self.bible) + 1) % len(ids)] if self.bible in ids else ids[0]
            self.again()

    def action_missal(self) -> None:
        if self.ordinary:
            current = self.navigation.current(self.query_one("#propers-reading", ScrollPanel),
                                              self.query_one("#propers-text", Static))
            self.navigation.pending = (((self.view or {}).get("navigation") or {}).get("nearest") or {}).get(current)
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
        offers = [("", "no single witness chosen; coequal witnesses remain open")]
        offers += [(one["id"], one["label"]) for one in witnesses]

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
        path_ids = {path["id"] for path in view.get("sourcePaths") or []}
        for choice in view.get("unresolvedChoices") or []:
            ident = choice.get("id") or ""
            if ident in path_ids or ident.startswith(("proper-condition/", "common-set:")):
                continue
            for option in choice.get("options") or []:
                offers.append(((ident, option["id"]), f"{missal.option_label(choice, option, view)}"
                                                      f"   ({choice.get('reason') or ident})"))
        for path in view.get("sourcePaths") or []:
            for option in path["options"]:
                if not option["unavailable"] and option.get("properChoices"):
                    offers.append((("source-path", option["properChoices"]), option["label"]))
        cycles: list[str] = []
        for form in (view.get("mass") or {}).get("forms") or []:
            if form["id"] != (self.reading[2] or "main"):
                offers.append((("proper-form", form["id"]), f"{form['name']}   (formulary form)"))
        for event in view.get("events") or []:
            selected = event.get("selected") or {}
            if selected.get("kind") == "cycle-alternatives":
                for cycle in selected.get("cycles") or []:
                    if cycle not in cycles:
                        cycles.append(cycle)
            if event.get("kind") == "proper-choice":
                for option in event.get("options") or []:
                    if option.get("unavailable"):
                        continue
                    offers.append((("proper-choice", event["id"], option["id"]), missal.choice_label(event, option)))
        cycles = list(dict.fromkeys(cycles + (view.get("cycles") or [])))
        offers += [(("cycle", cycle), f"Cycle {cycle}   (the lectionary cycle)") for cycle in cycles]
        ordinary = view.get("ordinary") or {}
        for group in ordinary.get("variants") or []:
            for option in group.get("options") or []:
                offers.append((("ordinary-variant", group["group"], option["id"]),
                               f"{group.get('name') or group['group']}: {option['name']}"))
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
            elif kind == "ordinary-variant":
                selection.setdefault("variants", {})[value[1]] = value[2]
            elif kind == "source-path":
                selection["properChoices"] = value[1]
                selection.pop("alternative", None)
            else:
                self.app.notify(f"This reader cannot make the choice {kind!r} yet.", severity="warning")
                return
            self.again()

        self.app.push_screen(Pick("choose", offers, "The sources leave this open. Nothing is chosen by order."),
                             picked)
