"""The Propers of the Mass: any formulary of any missal, read without a date."""
from __future__ import annotations

import re

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Input, OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge, missal
from ..dialogs import Ask, Pick, Reading, StudyDialog
from ..reader_navigation import MissalSurface, ReadingNavigation, share
from ..repo import Refused
from ..widgets import Ink, MissalPanel, Panel, ScrollPanel

ADAPTER = "liturgy"
SEARCHED = "titles, keys, kinds, seasons, fixed dates, incipits, citations and witnesses"
_UNSET = object()
_YEAR_RE = re.compile(r"\b(1\d{3}|2\d{3})\b")


def _missal_chip(short: str) -> str:
    """Compact §10 year chip (`1962`, `2008`, `1920`) so pills always fit on one line."""
    match = _YEAR_RE.search(short or "")
    return match.group(1) if match else (short or "").split()[0]


def _ordinary_lang_label(entry: dict) -> str:
    label = entry.get("label") or entry.get("name") or entry.get("lang") or ""
    if entry.get("lang") == "en" and label == "en":
        return "English"
    if entry.get("lang") == "la" and label == "la":
        return "Latin"
    return missal.format_coverage_notice(label)


def _format_browse_counts(counts: list[dict]) -> str:
    """Show language availability, omitting N/N ratios once complete."""
    parts = []
    for one in counts:
        lang = str(one.get("lang") or "").upper()
        avail = one.get("available")
        occ = one.get("occurrences")
        if not lang:
            continue
        if isinstance(occ, int) and occ > 0 and isinstance(avail, int):
            if avail >= occ:
                parts.append(lang)
            else:
                parts.append(f"{lang} {avail}/{occ}")
        elif isinstance(avail, int) and avail > 0:
            parts.append(lang)
    return " · ".join(parts)


class Propers(MissalSurface):
    READING = "#propers-reading"
    BROWSE = "#propers-list"
    key = "2"
    label = "Propers"

    @property
    def FIRST(self):
        return self.READING if self.reading and not self.has_class("navigation") else self.BROWSE

    HELP = (
        ("℣ · ℟ · P · S · All", "versicle · response · priest · server · congregation"),
        (",", "reading settings: celebration, prayers, Scripture, sources"),
        ("↑ / ↓ · PgUp / PgDn", "scroll the reading by a line or a page"),
        ("/", "search this missal's formularies"),
        ("escape", "leave the search box"),
        ("enter", "read the highlighted formulary"),
        ("c", "next missal (2008 emended reprint, 1962 typical edition, 1920 typical edition)"),
        ("o", "oration prayers in English or Latin"),
        ("b", "next Bible edition"),
        ("B", "pair Latin and the selected language (side by side on wide terminals)"),
        ("L", "choose the Ordinary language independently"),
        ("K", "choose or remove a named Latin Bible companion"),
        ("i", "Contents: jump to a liturgical landmark"),
        ("Ctrl+O", "open external source witness for the current prayer"),
        ("e", "related links: dates in Day (1), Catena (3), Scripture (4), Sources (6), History (7)"),
        ("u", "copy canonical website URL for this reading"),
        ("g", "open a Day or Propers reader URL"),
        ("d", "Study: Overview, Current Unit, and All Units apparatus"),
        ("v / V", "compare this formulary / choose a comparison"),
        ("[ / ]", "previous / next formulary in this browse or search result"),
        ("w", "choose an oration witness"),
        ("s", "choose a form, a lectionary cycle, or a source/Ordinary option"),
        ("m", "missal mode: these propers seated in the Ordinary"),
        ("r", "show or hide Ordinary rubrics in missal mode"),
        ("f", "show or hide navigation panes; narrow screens start with Browse or reading"),
    )
    BINDINGS = [
        Binding("comma", "settings", "settings"),
        Binding("slash", "search", "search"),
        Binding("c", "calendar", "edition"),
        Binding("o", "orations", "prayers"),
        Binding("b", "bible", "bible", show=False),
        Binding("B", "bilingual", "bilingual", show=False),
        Binding("L", "ordinary_language", "Ordinary language", show=False),
        Binding("K", "companion", "Latin Bible", show=False),
        Binding("i", "contents", "contents"),
        Binding("ctrl+o", "prayer_source", "current prayer source", show=False),
        Binding("e", "explore", "links", show=False),
        Binding("u", "share", "share", show=False),
        Binding("g", "open_url", "open URL", show=False),
        Binding("d", "study", "study"),
        Binding("v", "compare", "compare"),
        Binding("V", "comparison", "compare choices", show=False),
        Binding("left_square_bracket", "step(-1)", "previous formulary", show=False),
        Binding("right_square_bracket", "step(1)", "next formulary", show=False),
        Binding("w", "witness", "witness", show=False),
        Binding("s", "choose", "choose"),
        Binding("m", "missal", "missal"),
        Binding("r", "rubrics", "rubrics", show=False),
    ]
    CSS = """
    .propers.focus #propers-left { display: none; }
    .propers.narrow #propers-left { width: 32; }
    .propers.compact #propers-left { display: none; }
    .propers.compact.navigation #propers-left { display: block; width: 1fr; margin-right: 0; }
    .propers.compact.navigation #propers-reading { display: none; }
    .propers #propers-reading { padding: 1 3; align: center top; }
    .propers.compact #propers-reading { padding: 0 1; }
    .propers.narrow #propers-reading { padding: 1 2; }
    .propers.narrow.compact #propers-reading { padding: 0 1; }
    .propers #propers-text { max-width: 78; }
    .propers.bilingual #propers-text, .propers.comparing #propers-text { max-width: 132; width: 100%; }
    .propers.bilingual.narrow #propers-text, .propers.comparing.narrow #propers-text { max-width: 78; width: auto; }
    .propers.short #propers-find Input,
    .propers.compact #propers-find Input { height: 1; padding: 0 1; }
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
        self.pending_source_role = None
        self.pending_study = False
        self.return_from_day = ""
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
        self._explicit_prefs: set[str] = set()
        self._last_pair_width: int = 0

    def build(self) -> None:
        self.mount(
            Horizontal(
                Vertical(
                    Panel(Static("", id="propers-missals"), Input(placeholder="Title, incipit, citation, MM-DD, witness…",
                                                                   id="propers-query"),
                          Static("", id="propers-status"), title="Find a Formulary", id="propers-find"),
                    Panel(OptionList(id="propers-list"), title="Formularies", id="propers-list-box"),
                    id="propers-left",
                ),
                MissalPanel(Static("", id="propers-text"), title="Propers", id="propers-reading"),
            )
        )
        self.start()

    def on_resize(self, event) -> None:
        super().on_resize(event)
        if self.view:
            current_pair = self.pair_column_width() if self._is_wide_spread() else 0
            if current_pair != self._last_pair_width:
                self.show(self.view)
        if self.calendar in self.catalogues:
            self._update_status(self.catalogues[self.calendar], self.query_one("#propers-query", Input).value)

    def _is_wide_spread(self) -> bool:
        return bool(self.comparison) or self.text_display == "latin-and-selected" or bool(self.companion)

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
        saved = self.app.saved_prefs()
        bible_ids = {one["id"] for one in self.bibles}
        cal_ids = [one["id"] for one in self.calendars]
        la_bibles = {one["id"] for one in self.bibles if one.get("language") == "la"}
        if not self.bible:
            saved_bible = saved.get("bible")
            self.bible = (saved_bible if saved_bible in bible_ids else None) or opening.get("defaultBible") or self.bibles[0]["id"]
        if not self.orations:
            saved_orations = saved.get("orations")
            self.orations = (saved_orations if saved_orations in ("en", "la") else None) or opening.get("defaultOrations") or "la"
        if not self.ordinary_language:
            saved_ord = saved.get("ordinary_language")
            self.ordinary_language = (saved_ord if saved_ord in ("en", "la") else None) or opening.get("defaultOrdinaryLanguage") or "en"
        if "textDisplay" not in self._explicit_prefs and saved.get("text_display") in ("selected", "latin-and-selected"):
            self.text_display = saved["text_display"]
        if "rubrics" not in self._explicit_prefs and isinstance(saved.get("rubrics"), bool):
            self.rubrics = saved["rubrics"]
        if "companion" not in self._explicit_prefs and saved.get("companion") in la_bibles:
            self.companion = saved["companion"]
        if self.calendar not in cal_ids:
            if self.calendar:
                self.fail(f"No missal called {self.calendar!r} is offered here. Choose a held missal with c.")
                return
            saved_cal = saved.get("calendar")
            self.calendar = (saved_cal if saved_cal in cal_ids else None) or (
                opening.get("default") if opening.get("default") in cal_ids else cal_ids[0])
        self.welcome()
        self.list_calendar()
        if self._intent.get("mass"):
            self.reading = (self.calendar, self._intent["mass"], self._intent.get("form"))
            self.show_reading_pane()
            self.selection().update(self._intent.get("selection") or {})
            self.fetch()

    def fail(self, message: str) -> None:
        self.query_one("#propers-text", Static).update(Ink()(message, "bold $error").content())

    def follow(self, calendar: str | None = None, mass: str | None = None, form: str | None = None,
               **options) -> None:
        if calendar:
            self.calendar = calendar
            self._explicit_prefs.add("calendar")
        for key, attribute in (("bible", "bible"), ("orations", "orations"), ("ordinary", "ordinary"),
                               ("ordinaryLang", "ordinary_language"), ("textDisplay", "text_display"),
                               ("companion", "companion"), ("urlLegacy", "url_legacy")):
            if key in options:
                setattr(self, attribute, options[key])
                self._explicit_prefs.add(key)
        if options.get("ordinary"):
            self.add_class("focus")
        selection = {name: options[name] for name in ("cycle", "witness", "properChoices", "variants", "alternative", "sourceLocal1970")
                     if name in options}
        self.navigation.pending = options.get("location")
        self.pending_source_role = options.get("prayerRole")
        self.pending_study = bool(options.get("study"))
        self.return_from_day = options.get("returnFromDay") or ""
        self.comparison = options.get("comparison")
        if not self.calendars:
            self._intent = {"mass": mass, "form": form, "selection": selection}
            return
        self.list_calendar()
        if options.get("browse"):
            self.reading = None
            self.view = None
            self.return_from_day = ""
            self.welcome()
            self.remove_class("focus")
            self.add_class("navigation")
            self.app.refresh_where()
            self.call_after_refresh(self.query_one("#propers-list", OptionList).focus)
            return
        if mass:
            self.reading = (self.calendar, mass, form)
            self.show_reading_pane()
            if options.get("replace"):
                self.choices[self.reading] = {}
            self.selection().update(selection)
            self.fetch()

    def welcome(self) -> None:
        ink = Ink()
        ink.line("Choose a formulary to read.", "bold $propers-color")
        ink.line()
        ink.line("Propers are read independently of a civil date: a formulary's fixed date in the list is the date "
                 "its source declares, not a claim about when it is celebrated. To read the Mass a date appoints, "
                 "use the Day surface (1), where p opens its formulary here.", "italic $text-muted")
        ink.line()
        ink.line("Nothing is opened for you: the list is the missal's own order, searched by the page's own search.",
                 "italic $text-muted")
        self.query_one("#propers-text", Static).update(ink.content())

    # --- the list ----------------------------------------------------------

    def list_calendar(self) -> None:
        names = Ink()
        for one in self.calendars:
            chosen = one["id"] == self.calendar
            chip = _missal_chip(one["short"])
            names(f" {chip} ", "bold reverse $propers-color" if chosen else "$text-muted")(" ")
        self.query_one("#propers-missals", Static).update(names.content())
        self.app.refresh_where()
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

    def _update_status(self, catalogue: dict, query: str) -> None:
        rows = catalogue["rows"]
        status = self.query_one("#propers-status", Static)
        edition = catalogue.get("short") or self.calendar
        compact = self.has_class("short") or self.has_class("compact")
        if query.strip() and not self.shown:
            status.update(Ink()(f"No formulary in {edition} matches {query!r}. The search covers {SEARCHED}; "
                                "nothing nearby is offered in its place.", "italic $warning").content())
        elif query.strip():
            status.update(Ink()(f"{len(self.shown)} of {len(rows)} matches in {edition}." if compact else
                                f"Showing {len(self.shown)} of {len(rows)} form-qualified results in {edition}.",
                                "italic").content())
        else:
            status.update(Ink()(f"{len(rows)} formularies · {edition}" if compact else
                                f"{len(rows)} form-qualified formularies in {edition}.",
                                "italic").content())

    def filter(self, calendar: str, query: str, ordinals: list[int]) -> None:
        catalogue = self.catalogues.get(calendar)
        if not catalogue or calendar != self.calendar:
            return
        rows = catalogue["rows"]
        self.shown = ordinals
        listing = self.query_one("#propers-list", OptionList)
        listing.clear_options()
        # The page's list presentation (adapter `catalogue`): the resumed
        # Sundays after the Epiphany form, by the data's order, their own group
        # after the Last Sunday after Pentecost, and a marked row's note closes
        # its group.
        notes = {note["mark"]: note["text"] for note in catalogue.get("notes") or []}
        marks: list[str] = []

        def close_group() -> None:
            for mark in marks:
                listing.add_option(Option(Ink()(f"{mark} {notes[mark]}", "italic $text-muted").line().content(),
                                          disabled=True))
            marks.clear()

        season: object = _UNSET
        for ordinal in ordinals:
            row = rows[ordinal]
            group_key = row.get("listSeason") or row.get("kind") or ""
            if not query.strip() and group_key != season:
                close_group()
                season = group_key
                listing.add_option(Option(Ink()(str(group_key).replace("-", " "),
                                                "bold $propers-color").content(), disabled=True))
            ink = Ink()(row["name"])
            if row.get("mark"):
                ink(f" {row['mark']}", "bold $propers-color")
                if row["mark"] not in marks:
                    marks.append(row["mark"])
            if row.get("form_name"):
                ink(f" · {row['form_name']}", "italic")
            if row.get("fixed_date"):
                ink(f"  {row['fixed_date']}", "$text-muted")
            ink.line()
            detail_parts = [row["kind"].replace("-", " ")]
            avail = _format_browse_counts(row.get("coverageCounts") or [])
            if avail:
                detail_parts.append(avail)
            ink("  " + " · ".join(detail_parts), "$text-muted")
            listing.add_option(Option(ink.content(), id=f"row-{ordinal}"))
        close_group()
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
        self._update_status(catalogue, query)
        edition = catalogue.get("short") or self.calendar
        self.query_one("#propers-list-box", Panel).retitle(f"Formularies · {edition}")

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
        self.return_from_day = ""
        self.read(self.calendar, row["key"], form)

    # --- reading -----------------------------------------------------------

    def selection(self) -> dict:
        if not self.reading:
            return {}
        return self.choices.setdefault(self.reading, {})

    def read(self, calendar: str, key: str, form: str | None) -> None:
        self.reading = (calendar, key, form)
        self.show_reading_pane()
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
        self.return_from_day = ""
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
        return " · ".join(part for part in (edition, mass.get("name") or "Browse formularies") if part)

    @staticmethod
    def _compare_pair_sides(section_blocks: list[dict]) -> tuple[list[dict], list[list[dict]]]:
        """Split a Propers Compare section into lead blocks and side columns."""
        lead: list[dict] = []
        sides: list[list[dict]] = []
        for block in section_blocks:
            classes = set(block.get("classes") or [])
            if block.get("tag") == "h3" and ({"compare-side-title", "compare-calendar-side"} & classes):
                sides.append([block])
            elif sides:
                sides[-1].append(block)
            else:
                lead.append(block)
        return lead, sides

    def show(self, view: dict) -> None:
        self.view = view
        box = self.query_one("#propers-reading", ScrollPanel)
        text = self.query_one("#propers-text", Static)
        ink = Ink()
        if view.get("refused"):
            box.retitle("Propers")
            text.update(ink.line(view["refused"], "bold $error").content())
            return
        mass = view.get("mass") or {}
        state = view.get("state") or {}
        compared = view.get("comparison")
        self.set_class(bool(compared), "comparing")
        self.set_class(self._is_wide_spread() and not compared, "bilingual")
        pair_w = self.pair_column_width() if self._is_wide_spread() else 0
        self._last_pair_width = pair_w
        rule_w = max(46, min(pair_w or 72, (self.size.width or 78) - 8))

        edition = mass.get("editionShort") or view["calendar"]
        box.retitle(edition)
        mode = "Missal" if state.get("ordinary") else "Read"
        language = "English" if state.get("orations") == "en" else "Latin"
        extra = []
        if state.get("form"):
            extra.append(f"form {state['form']}")
        if state.get("cycle"):
            extra.append(f"Year {state['cycle']}")
        if state.get("textDisplay") == "latin-and-selected":
            extra.append("Bilingual")
        if state.get("ordinary"):
            ord_code = state.get("ordinaryLang") or state.get("orations")
            ord_name = "English" if ord_code == "en" else ("Latin" if ord_code == "la" else str(ord_code))
            extra.append(f"{ord_name} Ordinary")
        if state.get("companion"):
            comp_label = next((b["label"] for b in self.bibles if b["id"] == state["companion"]), state["companion"])
            extra.append(f"Latin Bible: {comp_label}")
        box.border_subtitle = " · ".join([mode, f"{language} orations", view["bible"]["label"], *extra])

        configured = bool(state.get("ordinary") and view.get("events") and not compared)
        if self.return_from_day:
            ink.line(f"Opened from Day ({self.return_from_day}) · press 1 to return", "bold $day-color")
        # Ceremonial Hand-Missal Header (no raw slug; crisp title + identity ribbon + rule)
        ink.line(mass.get("name") or view["key"], "bold $propers-color")
        ribbon = []
        if mass.get("kind"):
            ribbon.append(mass["kind"].replace("-", " ").capitalize())
        if mass.get("season"):
            ribbon.append(mass["season"].replace("-", " ").capitalize())
        ribbon.append("Date-independent formulary")
        ink.line(" · ".join(ribbon), "$text-muted")
        ink.line("─" * rule_w, "$rule")

        if configured and mass.get("recension"):
            ink.line(mass["recension"], "italic $warning")
        missal.source_witness(ink, view)
        missal.ordinary_conditions(ink, view, compact=configured)
        for absence in view.get("explicitAbsences") or []:
            reason = absence.get("reason") or ""
            if " " in reason:
                ink.line(reason, "italic $text-muted")
        if not compared:
            missal.choices(ink, view)
        notice = view.get("notice") or ""
        if notice and not configured:
            complete = missal.is_complete_notice(notice, recension=mass.get("recension"))
            style = "italic $text-muted" if complete else "italic $warning"
            ink.line(missal.format_coverage_notice(notice), style)
        if not configured and state.get("ordinary") and (view.get("ordinary") or {}).get("advisory"):
            ink.line(view["ordinary"]["advisory"], "italic $text-muted")
        self.navigation.begin((view["calendar"], view["key"], state.get("form")), box, text)
        if compared:
            box.border_subtitle = f"Compare · {compared.get('title') or 'unsupported selection'} · v reading · V choices"
            if compared.get("refused"):
                ink.line("This comparison cannot be made as asked", "bold $warning")
                ink.line(compared["refused"], "italic $warning")
            else:
                missal.blocks(ink, compared.get("lead") or [], accent="$propers-color")
                for section in compared.get("sections") or []:
                    self.navigation.mark(section["id"], section["label"], ink)
                    ink.line()
                    lead_blocks, sides = self._compare_pair_sides(section["blocks"])
                    if lead_blocks:
                        missal.blocks(ink, lead_blocks, accent="$propers-color")
                    if len(sides) == 2 and pair_w >= 80:
                        missal._render_pair_columns(ink, sides[0], sides[1],
                                                    pair_width=pair_w, accent="$propers-color",
                                                    missal_mode=False, seen_notes=None)
                    elif sides:
                        for side_idx, side in enumerate(sides):
                            if side_idx > 0:
                                ink.line()
                            missal.blocks(ink, side, accent="$propers-color")
        else:
            for path in view.get("sourcePaths") or []:
                if not path.get("beforeEventId"):
                    missal.blocks(ink, path["blocks"], accent="$propers-color", pair_width=pair_w)
            for event in view.get("events") or []:
                if not self.rubrics and (event.get("element") or {}).get("kind") == "rubric":
                    continue
                for path in view.get("sourcePaths") or []:
                    if path.get("beforeEventId") == event["id"]:
                        missal.blocks(ink, path["blocks"], accent="$propers-color", pair_width=pair_w)
                if missal.is_contents_event(event):
                    label = missal.event_label(event, indent_children=bool(state.get("ordinary")))
                    self.navigation.mark(event["id"], label, ink)
                event_kwargs = {"rubrics": self.rubrics, "accent": "$propers-color"}
                if pair_w:
                    event_kwargs["pair_width"] = pair_w
                missal.events(ink, {**view, "events": [event]}, **event_kwargs)
        text.update(ink.content())
        if self.pending_source_role:
            locations = [event["id"] for event in view.get("events", [])
                         if event.get("slot") == self.pending_source_role or
                         any(member.get("slot") == self.pending_source_role
                             for option in event.get("options", []) for member in option.get("members", []))]
            if len(locations) == 1:
                self.navigation.pending = locations[0]
            else:
                self.app.notify(f"An exact location for {self.pending_source_role} is unavailable in this form.")
            self.pending_source_role = None
        self.navigation.finish(self, box, text)
        self.app.refresh_where()
        if self.pending_study:
            self.pending_study = False
            self.action_study()

    # --- controls ----------------------------------------------------------

    def action_calendar(self) -> None:
        ids = [one["id"] for one in self.calendars]
        if ids:
            self.calendar = ids[(ids.index(self.calendar) + 1) % len(ids)] if self.calendar in ids else ids[0]
            self.app.remember_pref("calendar", self.calendar)
            self.list_calendar()

    def again(self) -> None:
        if self.reading:
            self.fetch()

    def action_orations(self) -> None:
        self.orations = "la" if self.orations == "en" else "en"
        self.app.remember_pref("orations", self.orations)
        for selection in self.choices.values():
            selection.pop("witness", None)
        self.again()

    def action_bilingual(self) -> None:
        self.text_display = "selected" if self.text_display == "latin-and-selected" else "latin-and-selected"
        self.app.remember_pref("text_display", self.text_display)
        self.again()

    def action_companion(self) -> None:
        offers = [("", "No Latin Bible companion")]
        offers += [(one["id"], one["label"]) for one in self.bibles if one.get("language") == "la"]

        def picked(value) -> None:
            if value is not None:
                self.companion = value
                self.app.remember_pref("companion", value or None)
                self.again()

        self.app.push_screen(Pick("Latin Bible Companion", offers,
                                  "Each edition retains its own numbering, provenance and refusals."), picked)

    def action_contents(self) -> None:
        self.navigation.choose(self, self.query_one("#propers-reading", ScrollPanel),
                               self.query_one("#propers-text", Static))

    @work(thread=True, exclusive=True, group="propers-dates")
    def action_calendar_dates(self) -> None:
        if not self.reading:
            return
        calendar, key, _ = self.reading
        year = self.app.today.year
        try:
            dates = bridge.call(ADAPTER, "formularyDates", calendar, key, year)
        except Refused as refusal:
            self.deliver(self.app.notify, str(refusal), severity="warning")
            return
        if not dates:
            self.deliver(self.app.notify, f"No civil date in {year} appoints this formulary directly.")
            return
        options = [(row["date"],
                    f"{row['longDate']}" + (f" · {row['branch']}" if row.get("branch") else "") +
                    (f" ({row['standing']})" if row.get("standing") != "appointed" else ""))
                   for row in dates]

        def picked(iso) -> None:
            if iso:
                self.app.action_surface("day", calendar=calendar, date=iso)

        self.deliver(self.app.push_screen,
                     Pick(f"Calendar Uses in {year}", options,
                          "Open a civil date in Day (1); the formulary itself remains date-independent."),
                     picked)

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
        self.app.push_screen(Ask("Open a Reader URL", "Paste a canonical or retained Day or Propers link."),
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
        languages = [(one["lang"], _ordinary_lang_label(one))
                     for one in ordinary.get("languages") or []]
        if not languages:
            self.app.notify("Open Missal mode (m) to choose this edition's Ordinary language.")
            return

        def picked(value) -> None:
            if value:
                self.ordinary_language = value
                self.app.remember_pref("ordinary_language", value)
                self.again()

        self.app.push_screen(Pick("Ordinary Language", languages,
                                  "The oration language stays independently selected; unavailable text stays explicit."),
                             picked)

    @work(thread=True, exclusive=True, group="propers-study")
    def action_study(self) -> None:
        if not self.reading:
            return
        panel = self.query_one("#propers-reading", ScrollPanel)
        text = self.query_one("#propers-text", Static)
        scrolled = panel.scroll_y > 0.5 or self.navigation.focused is not None
        current_id = self.navigation.current(panel, text) if not self.comparison and self.navigation.entries else None
        current_label = self.navigation.current_label(panel, text) if current_id else ""
        calendar, key, _ = self.reading
        try:
            study_blocks = bridge.call(ADAPTER, "studyPropers", calendar, key, self.options())
        except Refused as refusal:
            self.deliver(self.app.notify, str(refusal), severity="warning")
            return
        view = self.view or {}
        overview_blocks, by_event, all_units = missal.split_study_blocks(study_blocks)
        unit_blocks = by_event.get(current_id or "", [])
        urls, source_ids = missal.extract_study_references([view], study_blocks)

        def build_overview(show_audit: bool):
            ink = Ink()
            missal.source_witness(ink, view, detail=True)
            missal.ordinary_conditions(ink, view)
            if view.get("notice"):
                ink.line(missal.format_coverage_notice(view["notice"]), "italic $text-muted").line()
            # Never dump the Ordinary monograph in Read mode (`self.ordinary` is False).
            if self.ordinary and (view.get("ordinary") or {}).get("advisory"):
                ink.line("Ordinary of the Mass — Witness Notes", "bold $propers-color")
                ink.line(view["ordinary"]["advisory"], "italic $text-muted").line()
            missal.blocks(ink, missal.filter_study_audit(overview_blocks, show_audit=show_audit),
                          accent="$propers-color")
            return ink.content()

        def build_unit(show_audit: bool):
            ink = Ink()
            if current_label:
                ink.line(current_label, "bold $propers-color").line()
            filtered = missal.filter_study_audit(unit_blocks, show_audit=show_audit)
            if filtered:
                missal.blocks(ink, filtered, accent="$propers-color")
            else:
                ink.line("No separate unit apparatus is recorded for this anchor; see Overview or All Units.",
                         "italic $text-muted")
            return ink.content()

        def build_all(show_audit: bool):
            ink = Ink()
            missal.blocks(ink, missal.filter_study_audit(all_units, show_audit=show_audit),
                          accent="$propers-color")
            return ink.content()

        initial_tab = "unit" if (scrolled and unit_blocks) else "overview"
        dialog = StudyDialog(
            "Study This Formulary",
            overview_builder=build_overview,
            unit_builder=build_unit if unit_blocks else None,
            all_builder=build_all if all_units else None,
            unit_label=current_label,
            initial_tab=initial_tab,
            urls=urls,
            source_ids=source_ids,
            accent="$propers-color",
        )
        self.deliver(self.app.push_screen, dialog)

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
                        self.show_reading_pane(hide_nav=True)
                        self.again()

                self.app.push_screen(Pick("Second Comparison Side", [(ident, label) for ident, label in peers
                                                                     if ident != primary],
                                          "The formulary stays independent of a date."), peer_chosen)

            self.app.push_screen(Pick("First Comparison Side", peers, "Choose both peers explicitly."), primary_chosen)

        self.app.push_screen(Pick("Compare This Formulary", [(one["dimension"], one["label"]) for one in offers],
                                  "Semantic slots are paired by the page's comparison model."), dimension_chosen)

    def source_rows(self) -> list[dict]:
        return [self.view] if self.view else []

    def reload_reading(self) -> None:
        self.again()

    def action_bible(self) -> None:
        ids = [one["id"] for one in self.bibles]
        if ids:
            self.bible = ids[(ids.index(self.bible) + 1) % len(ids)] if self.bible in ids else ids[0]
            self.app.remember_pref("bible", self.bible)
            self.again()

    def action_missal(self) -> None:
        if self.ordinary:
            current = self.navigation.current(self.query_one("#propers-reading", ScrollPanel),
                                              self.query_one("#propers-text", Static))
            self.navigation.pending = (((self.view or {}).get("navigation") or {}).get("nearest") or {}).get(current)
        self.ordinary = not self.ordinary
        if self.reading:
            self.show_reading_pane(hide_nav=self.ordinary)
            self.again()

    def action_rubrics(self) -> None:
        self.rubrics = not self.rubrics
        self.app.remember_pref("rubrics", self.rubrics)
        if self.view:
            self.show(self.view)

    def action_witness(self) -> None:
        witnesses = ((self.view or {}).get("mass") or {}).get("witnesses") or []
        if not witnesses:
            self.app.notify("No oration witness in this language is recorded for this missal.")
            return
        offers = [("", "No single witness chosen; coequal witnesses remain open")]
        offers += [(one["id"], one["label"]) for one in witnesses]

        def picked(value) -> None:
            if value is None:
                return
            if value:
                self.selection()["witness"] = value
            else:
                self.selection().pop("witness", None)
            self.again()

        self.app.push_screen(Pick("Oration Witness", offers,
                                  "A missing text stays missing; no other witness fills it."), picked)

    def action_choose(self) -> None:
        view = self.view or {}
        form_items: list = []
        proper_items: list = []
        cycle_items: list = []
        ordinary_groups: list[tuple[str, list]] = []

        historical = [event.get("sourceLocalActorChoice") for event in view.get("events") or []
                      if (event.get("sourceLocalActorChoice") or {}).get("available")]
        if historical:
            selected = any(offer.get("selected") for offer in historical)
            proper_items.append((("source-local-1970", not selected),
                                 "Return to unchanged source quotation" if selected else
                                 "Historical 1970 reading (current 2008 correspondence not established)"))
        path_ids = {path["id"] for path in view.get("sourcePaths") or []}
        proper_choice_ids = {e["id"] for e in view.get("events") or [] if e.get("kind") == "proper-choice"}
        for choice in view.get("unresolvedChoices") or []:
            ident = choice.get("id") or ""
            if ident in path_ids or ident in proper_choice_ids or ident.startswith(("proper-condition/", "common-set:")):
                continue
            reason = missal.clean_choice_reason(choice, view)
            for option in choice.get("options") or []:
                proper_items.append(((ident, option["id"]), f"{missal.option_label(choice, option, view)}   ({reason})"))
        for path in view.get("sourcePaths") or []:
            for option in path["options"]:
                if not option["unavailable"] and option.get("properChoices"):
                    proper_items.append((("source-path", option["properChoices"]), option["label"]))
        cycles: list[str] = []
        for form in (view.get("mass") or {}).get("forms") or []:
            if form["id"] != (self.reading[2] or "main"):
                form_items.append((("proper-form", form["id"]), f"{form['name']}"))
        for event in view.get("events") or []:
            selected = event.get("selected") or {}
            if selected.get("kind") == "cycle-alternatives":
                for cycle in selected.get("cycles") or []:
                    if cycle not in cycles:
                        cycles.append(cycle)
            if event.get("kind") == "proper-choice":
                chosen = (event.get("selection") or {}).get("option")
                for option in event.get("options") or []:
                    if option.get("unavailable"):
                        continue
                    mark = " (selected)" if option["id"] == chosen else ""
                    proper_items.append((("proper-choice", event["id"], option["id"]),
                                         f"{missal.choice_label(event, option)}{mark}"))
        cycles = list(dict.fromkeys(cycles + (view.get("cycles") or [])))
        cur_cycle = self.selection().get("cycle")
        for cycle in cycles:
            mark = " (selected)" if cycle == cur_cycle else ""
            cycle_items.append((("cycle", cycle), f"Cycle {cycle}{mark}"))
        if cur_cycle:
            cycle_items.append((("cycle", None), "Every cycle, kept apart (no year chosen)"))
        ordinary = view.get("ordinary") or {}
        for group in ordinary.get("variants") or []:
            selected = (ordinary.get("selection") or {}).get(group["group"])
            gname = group.get("name") or group["group"]
            gitems = []
            for option in group.get("options") or []:
                mark = " (selected)" if option["id"] == selected else ""
                app = option.get("applicability")
                app_note = (" — applicability unresolved" if app == "unresolved"
                            else (" — not appointed here" if app == "inapplicable" else ""))
                gitems.append((("ordinary-variant", group["group"], option["id"]),
                               f"{option['name']}{app_note}{mark}"))
            if gitems:
                ordinary_groups.append((gname, gitems))

        groups: list[tuple[str, list]] = []
        if form_items:
            groups.append(("Formulary Form", form_items))
        if cycle_items:
            groups.append(("Lectionary Cycle", cycle_items))
        if proper_items:
            groups.append(("Proper Options", proper_items))
        groups.extend(ordinary_groups)

        offers: list = []
        sections: dict[int, str] = {}
        use_sections = len(groups) > 1
        for heading, items in groups:
            if use_sections:
                sections[len(offers)] = heading
            offers.extend(items)
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
                missal.select_proper_option(selection, view, value[1], value[2])
            elif kind.startswith("translation-witness"):
                selection["witness"] = value[1]
            elif kind == "ordinary-variant":
                selection.setdefault("variants", {})[value[1]] = value[2]
            elif kind == "source-local-1970":
                if value[1]:
                    selection["sourceLocal1970"] = True
                else:
                    selection.pop("sourceLocal1970", None)
            elif kind == "source-path":
                selection["properChoices"] = value[1]
                selection.pop("alternative", None)
            else:
                self.app.notify(f"This reader cannot make the choice {kind!r} yet.", severity="warning")
                return
            self.again()

        self.app.push_screen(Pick("Choose", offers, "The sources leave this open. Nothing is chosen by order.",
                                  sections=sections or None), picked)
