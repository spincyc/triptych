"""Today's Missal: the Mass a date appoints, in each missal, with the rubric behind it."""
from __future__ import annotations

import datetime as dt

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge, missal
from ..dialogs import Ask, Pick, Reading, StudyDialog
from ..month import Month
from ..repo import Refused
from ..reader_navigation import MissalSurface, ReadingNavigation, share
from ..theme import SEASON_TONES
from ..widgets import Ink, MissalPanel, Panel, ScrollPanel, literal

ADAPTER = "liturgy"


def tone(season: str | None) -> str:
    """The theme's hue for a season (theme.SEASON_TONES), or none."""
    return f"$season-{season}" if season in SEASON_TONES else ""


# Rank, in the derivation's own terms: a class where the code has classes
# (1962, pre-1955), else the day's nature (the postconciliar Norms rank by
# nature, not class). The glyph says it without colour; the legend names it in
# the words of whichever missal is on screen.
CLASS_MARKS = {"I": "◆", "II": "◇", "III": "•"}
NATURE_MARKS = {"solemnity": "◆", "solemnity-or-sunday": "◆", "triduum": "◆", "feast": "◇",
                "memorial": "•", "sunday": "○"}
OPEN_ORATION_MARK = "·"
REFUSED = "×"


def rank_glyph(winner: dict | None) -> str:
    if not winner:
        return " "
    if winner.get("class"):
        return CLASS_MARKS.get(winner["class"], " ")
    return NATURE_MARKS.get(winner.get("nature") or "", " ")


def legend_for(month: dict | None) -> Ink:
    """The marks of this month, said in its missal's own terms."""
    days = (month or {}).get("days") or []
    classed = any((branch.get("winner") or {}).get("class") for day in days for branch in day.get("branches") or [])
    legend = Ink()
    if classed:
        legend("◆", "bold")(" Class I  ")("◇", "bold")(" Class II  ")("•", "bold").line(" Class III")
        legend.line("blank: Class IV", "$text-muted")
    else:
        legend("◆", "bold")(" Solemnity  ")("◇", "bold")(" Feast  ")("•", "bold").line(" Memorial")
        legend("○", "bold")(" Sunday  ")(OPEN_ORATION_MARK, "bold")(" Weekday (open prayers)  ")
        legend.line("blank: settled weekday", "$text-muted")
    legend("?", "bold $warning")(" not settled  ")("⑂", "bold $warning")(" a choice  ")
    legend(REFUSED, "bold $error").line(" refused")
    legend.line("hue = season; no vestment colour is recorded", "italic $text-muted")
    return legend


def season_name(season: str | None) -> str:
    names = {"after-pentecost": "After Pentecost", "ordinary-time": "Ordinary Time", "holy-week": "Holy Week"}
    if not season:
        return ""
    return names.get(season, season.replace("-", " ").capitalize())


def rank_words(winner: dict | None) -> str:
    if not winner:
        return ""
    if winner.get("class"):
        return f"Class {winner['class']}"
    nature = winner.get("nature") or ""
    if nature == "solemnity-or-sunday":
        name = (winner.get("name") or "").lower()
        return "Sunday" if "sunday" in name else "Solemnity"
    mapping = {
        "solemnity": "Solemnity",
        "feast": "Feast",
        "memorial": "Memorial",
        "sunday": "Sunday",
        "triduum": "Triduum",
        "weekday": "Weekday",
    }
    return mapping.get(nature, nature.replace("-", " ").capitalize())


def standing_words(standing: str) -> str:
    mapping = {
        "option": "Optional celebration",
        "unresolved": "Prayers open — press s to choose",
        "displaced": "Displaced celebration",
        "commemorated": "Commemorated",
    }
    return mapping.get(standing, standing.replace("-", " ").capitalize())


def _ordinary_lang_label(entry: dict) -> str:
    label = entry.get("label") or entry.get("name") or entry.get("lang") or ""
    if entry.get("lang") == "en" and label == "en":
        return "English"
    if entry.get("lang") == "la" and label == "la":
        return "Latin"
    return missal.format_coverage_notice(label)


def _trim(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[: max(1, limit - 1)] + "…"


class Day(MissalSurface):
    READING = "#day-reading-a"
    BROWSE = "#day-missal-list"
    key = "1"
    label = "Day"
    FIRST = "#day-reading-a"
    HELP = (
        ("℣ · ℟ · P · S · All", "versicle · response · priest · server · congregation"),
        (",", "reading settings: celebration, prayers, Scripture, sources"),
        ("↑ / ↓ · PgUp / PgDn", "scroll the reading by a line or a page"),
        ("← / →", "previous / next day (or move cursor when Calendar is focused)"),
        ("[ / ]", "previous / next week"),
        ("{ / }", "previous / next month"),
        ("t", "today"),
        ("g", "go to a date (YYYY-MM-DD) or paste a Day / Propers reader URL"),
        ("c", "next missal (2008 emended reprint, 1962 typical edition, 1920 typical edition)"),
        ("v / V", "compare this missal with another / choose peer missal"),
        ("m", "missal mode: propers seated in the Ordinary"),
        ("o", "oration prayers in English or Latin"),
        ("b", "next Bible edition for Scripture readings"),
        ("B", "pair Latin and the selected language (side by side on wide terminals)"),
        ("L", "choose Ordinary language independently of orations"),
        ("K", "choose or remove a named Latin Bible companion"),
        ("i", "Contents: jump to a liturgical landmark"),
        ("Ctrl+O", "open external source witness for the current prayer"),
        ("e", "related links: open Scripture in Catena/Scripture, witness in Sources, or History"),
        ("u", "copy canonical website URL for this reading"),
        ("d", "Study: Overview, Current Unit, and All Units apparatus"),
        ("w", "choose an oration witness, where several are held"),
        ("s", "make a choice the rubrics leave open (Mass, form, prayers, Ordinary options)"),
        ("r", "show or hide Ordinary rubrics in missal mode"),
        ("p", "open this formulary in the Propers surface"),
        ("f", "show or hide navigation panes; narrow screens start with the reading"),
    )
    BINDINGS = [
        Binding("comma", "settings", "settings"),
        Binding("left,h", "step(-1)", "previous day", show=False),
        Binding("right,l", "step(1)", "next day", show=False),
        Binding("left_square_bracket", "step(-7)", "previous week", show=False),
        Binding("right_square_bracket", "step(7)", "next week", show=False),
        Binding("left_curly_bracket", "month(-1)", "previous month", show=False),
        Binding("right_curly_bracket", "month(1)", "next month", show=False),
        Binding("t", "today", "today"),
        Binding("g", "goto", "date"),
        Binding("c", "calendar", "edition"),
        Binding("v", "compare", "compare"),
        Binding("V", "peer", "compare with…", show=False),
        Binding("m", "missal", "missal"),
        Binding("o", "orations", "prayers"),
        Binding("b", "bible", "bible", show=False),
        Binding("B", "bilingual", "bilingual", show=False),
        Binding("L", "ordinary_language", "Ordinary language", show=False),
        Binding("K", "companion", "Latin Bible", show=False),
        Binding("i", "contents", "contents"),
        Binding("ctrl+o", "prayer_source", "current prayer source", show=False),
        Binding("e", "explore", "links", show=False),
        Binding("u", "share", "share", show=False),
        Binding("d", "study", "study"),
        Binding("w", "witness", "witness", show=False),
        Binding("s", "choose", "choose"),
        Binding("r", "rubrics", "rubrics", show=False),
        Binding("p", "propers", "propers", show=False),
    ]
    CSS = """
    .day.focus #day-left { display: none; }
    .day.comparing #day-left { display: none; }
    .day.narrow #day-left { width: 32; }
    .day.narrow #day-legend { display: none; }
    .day.wide #day-left { width: 36; }
    .day.compact #day-left { display: none; }
    .day.compact.navigation #day-left { display: block; width: 100%; margin-right: 0; }
    .day.compact.navigation #day-reading-a, .day.compact.navigation #day-compare { display: none; }
    .day.short #day-why { display: none; }
    .day.compact.navigation.short #day-why { display: block; }
    .day #day-reading-a, .day #day-compare { padding: 1 3; }
    .day.compact #day-reading-a, .day.compact #day-compare { padding: 0 1; }
    .day #day-reading-a { align: center top; }
    .day.narrow #day-reading-a, .day.narrow #day-compare { padding: 1 2; }
    .day.narrow.compact #day-reading-a, .day.narrow.compact #day-compare { padding: 0 1; }
    .day.narrow #day-compare-body Horizontal { layout: vertical; }
    .day.narrow .compare-side { width: 100%; padding: 0 0 1 0; }
    .day #day-text-a { max-width: 78; width: 100%; }
    .day.bilingual #day-text-a { max-width: 132; width: 100%; }
    .day.bilingual.narrow #day-text-a { max-width: 78; width: 100%; }
    """
    DEFAULT_CSS = """
    Day #day-left { width: 36; margin-right: 1; }
    Day #day-calendar { height: auto; align: center top; }
    Day #day-month { width: 100%; }
    Day #day-preview { height: 1; width: 100%; color: $text-muted; text-align: center; }
    Day #day-legend { display: none; }
    Day #day-missals { height: auto; }
    Day #day-why { height: 1fr; }
    Day #day-compare { display: none; }
    Day.comparing #day-compare { display: block; }
    Day.comparing #day-reading-a { display: none; }
    Day #day-compare-body { height: auto; }
    Day #day-compare-body Horizontal { height: auto; }
    Day .compare-side { width: 1fr; height: auto; padding: 0 1 0 0; }
    Day .compare-unit { height: auto; padding: 1 0 0 0; }
    Day OptionList { height: auto; }
    """

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.today = dt.date.today()
        self.date = self.today
        self.pinned = False
        self.calendars: list[dict] = []
        self.calendar = ""
        self.bibles: list[dict] = []
        self.bible = ""
        self.orations = ""
        self.ordinary_language = ""
        self.text_display = "selected"
        self.companion = ""
        self.navigation = ReadingNavigation()
        self.compare_locations: list = []
        self.compare_focus: tuple[str, float] | None = None
        self.pending_study = False
        self.pending_selection: dict = {}
        self.url_legacy: dict = {}
        self.ordinary = False
        self.rubrics = True
        self.comparing = False
        self.compare_territory = ""
        self.compared: dict | None = None
        self.months: dict[tuple[str, str], dict] = {}
        self.choices: dict[tuple[str, str], dict] = {}
        self.views: dict[str, dict] = {}
        self.opening: dict = {}
        self._explicit_prefs: set[str] = set()
        self._last_pair_width: int = 0

    # --- building --------------------------------------------------------

    def build(self) -> None:
        self.today = self.app.today
        if not self.pinned:
            self.date = self.today
        self.mount(
            Horizontal(
                Vertical(
                    Panel(Month(mark=self.mark, today=self.today, id="day-month"),
                          Static("", id="day-preview"),
                          Static("", id="day-legend"), title="Calendar", id="day-calendar"),
                    Panel(OptionList(id="day-missal-list"), title="Missals", id="day-missals"),
                    ScrollPanel(Static("", id="day-why-text"), title="Why This Mass", id="day-why"),
                    id="day-left",
                ),
                Horizontal(
                    MissalPanel(Static("", id="day-text-a"), title="Mass", id="day-reading-a"),
                    ScrollPanel(Vertical(id="day-compare-body"), title="Compare", id="day-compare"),
                ),
            )
        )
        self.start()

    def on_resize(self, event) -> None:
        super().on_resize(event)
        if self.views and not self.comparing:
            current_pair = self.pair_column_width() if self._is_bilingual_spread() else 0
            if current_pair != self._last_pair_width:
                self.redraw()

    def _is_bilingual_spread(self) -> bool:
        return self.text_display == "latin-and-selected" or bool(self.companion)

    @work(thread=True, exclusive=True, group="day-start")
    def start(self) -> None:
        try:
            opening = bridge.call(ADAPTER, "opening")
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.opened_with, opening)

    def opened_with(self, opening: dict) -> None:
        self.opening = opening
        self.calendars = opening["calendars"]
        self.bibles = opening["bibles"]
        saved = self.app.saved_prefs()
        bible_ids = {one["id"] for one in self.bibles}
        cal_ids = [one["id"] for one in self.calendars]
        la_bibles = {one["id"] for one in self.bibles if one.get("language") == "la"}
        # Precedence (Vision Invariant #6): URL/CLI intent > remembered prefs > repo defaults.
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
        self.adopt_pending()
        self.load()

    def fail(self, message: str) -> None:
        self.query_one("#day-text-a", Static).update(Ink()(message, "bold $error").content())

    # --- intent and movement ---------------------------------------------

    def follow(self, date: str | None = None, calendar: str | None = None, mass: str | None = None, **options) -> None:
        if date:
            self.date = dt.date.fromisoformat(date)
            self.pinned = True
        if calendar:
            self.calendar = calendar
            self._explicit_prefs.add("calendar")
        if mass:
            self.pending_mass = mass
        for key, attribute in (("bible", "bible"), ("orations", "orations"), ("ordinary", "ordinary"),
                               ("ordinaryLang", "ordinary_language"), ("textDisplay", "text_display"),
                               ("companion", "companion"), ("rubrics", "rubrics"), ("comparing", "comparing")):
            if key in options:
                setattr(self, attribute, options[key])
                self._explicit_prefs.add(key)
        if options.get("ordinary"):
            self.add_class("focus")
        if "urlLegacy" in options:
            self.url_legacy = options["urlLegacy"]
        self.set_class(self.comparing, "comparing")
        if options.get("peer"):
            self.chosen_peer = options["peer"]
        if "compare_territory" in options:
            self.compare_territory = "" if options["compare_territory"] == "universal" else options["compare_territory"]
        if options.get("replace"):
            self.choices[(self.calendar, self.date.isoformat())] = {}
        self.pending_selection = {key: options[key] for key in ("form", "witness", "properChoices", "variants", "orationMass", "orationTerritory", "sourceLocal1970")
                                  if key in options}
        self.navigation.pending = options.get("location")
        self.pending_study = bool(options.get("study"))
        if self.calendars:
            self.adopt_pending()
            self.load()

    def adopt_pending(self) -> None:
        """A Mass named on arrival belongs to the missal it was named for, which
        is known only once the missals are."""
        mass = getattr(self, "pending_mass", None)
        if mass:
            self.choices[(self.calendar, self.date.isoformat())] = {"mass": mass}
            self.pending_mass = None
        if self.pending_selection:
            self.selection().update(self.pending_selection)
            self.pending_selection = {}

    def go(self, date: dt.date) -> None:
        self.date = date
        self.load()

    def action_step(self, days: int) -> None:
        try:
            self.go(self.date + dt.timedelta(days=days))
        except OverflowError:
            self.app.notify("No date lies beyond the calendar's own range.", severity="warning")

    def action_month(self, step: int) -> None:
        month = self.date.month - 1 + step
        year = self.date.year + month // 12
        if not dt.MINYEAR <= year <= dt.MAXYEAR:
            self.app.notify("No date lies beyond the calendar's own range.", severity="warning")
            return
        month = month % 12 + 1
        day = min(self.date.day, [31, 29 if year % 4 == 0 and (year % 100 or year % 400 == 0) else 28,
                                  31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        self.go(dt.date(year, month, day))

    def action_today(self) -> None:
        self.go(self.today)

    def action_goto(self) -> None:
        def answered(value: str | None) -> None:
            if not value:
                return
            if "#" in value or "://" in value:
                self.open_link(value)
                return
            try:
                self.go(dt.date.fromisoformat(value))
            except ValueError:
                self.app.notify(f"Not a date: {literal(repr(value))}. Write it YYYY-MM-DD.", severity="warning")

        self.app.push_screen(Ask("Go to Date or Reader URL", "YYYY-MM-DD, or paste a Day or Propers URL",
                                 self.date.isoformat()), answered)

    @work(thread=True, exclusive=True, group="day-open-url")
    def open_link(self, value: str) -> None:
        try:
            target = bridge.call(ADAPTER, "openReaderLink", value, "day")
        except Refused as refusal:
            self.deliver(self.app.notify, str(refusal), severity="warning")
            return
        self.deliver(self.app.action_surface, target["entrance"], **target["intent"])

    def action_calendar(self) -> None:
        ids = [one["id"] for one in self.calendars]
        if ids:
            self.calendar = ids[(ids.index(self.calendar) + 1) % len(ids)] if self.calendar in ids else ids[0]
            self.app.remember_pref("calendar", self.calendar)
            self.load()

    def action_compare(self) -> None:
        if not self.comparing and self.selection().get("dedicationAttestation"):
            self.app.notify("The confirmed celebration location cannot be carried into Compare.", severity="warning")
            return
        if not self.comparing and self.selection().get("orationMass"):
            self.app.notify("This prayer selection has no source-backed comparison dimension yet.", severity="warning")
            return
        self.map_mode_location("read" if self.comparing else "compare")
        self.comparing = not self.comparing
        self.set_class(self.comparing, "comparing")
        if self.comparing:
            self.call_after_refresh(self.focus_reading_panel)
        self.load()

    def action_missal(self) -> None:
        if self.ordinary and not self.comparing:
            self.map_mode_location("read")
        self.ordinary = not self.ordinary
        self.show_reading_pane(hide_nav=self.ordinary)
        self.load()

    def map_mode_location(self, mode: str) -> None:
        current = self.compare_current() if self.comparing else self.navigation.current(
            self.query_one("#day-reading-a", ScrollPanel), self.query_one("#day-text-a", Static))
        destination = None
        for row in (self.views.get(self.calendar) or {}).get("rows") or []:
            prefix = row.get("prefix") or ""
            maps = row.get("navigation") or {}
            if self.comparing:
                target = ((maps.get("fromCompare") or {}).get("recension") or {}).get(current)
                if target:
                    destination = prefix + target
                    break
            elif current and current.startswith(prefix):
                source = current[len(prefix):]
                target = (((maps.get("compare") or {}).get("recension") or {}).get(source) if mode == "compare"
                          else (maps.get("nearest") or {}).get(source))
                if target:
                    destination = target if mode == "compare" else prefix + target
                    break
        self.navigation.pending = destination
        if not destination:
            self.navigation.identity = None

    def action_rubrics(self) -> None:
        self.rubrics = not self.rubrics
        self.app.remember_pref("rubrics", self.rubrics)
        self.redraw()

    def action_orations(self) -> None:
        self.orations = "la" if self.orations == "en" else "en"
        self.app.remember_pref("orations", self.orations)
        for selection in self.choices.values():
            selection.pop("witness", None)
        self.load()

    def action_bilingual(self) -> None:
        self.text_display = "selected" if self.text_display == "latin-and-selected" else "latin-and-selected"
        self.app.remember_pref("text_display", self.text_display)
        self.load()

    def action_companion(self) -> None:
        offers = [("", "No Latin Bible companion")]
        offers += [(one["id"], one["label"]) for one in self.bibles if one.get("language") == "la"]

        def picked(value) -> None:
            if value is not None:
                self.companion = value
                self.app.remember_pref("companion", value or None)
                self.load()

        self.app.push_screen(Pick("Latin Bible Companion", offers,
                                  "Each edition retains its own numbering, provenance and refusals."), picked)

    def action_contents(self) -> None:
        if self.comparing:
            if not self.compare_locations:
                self.app.notify("There are no comparison units in this selection yet.")
                return
            box = self.query_one("#day-compare", ScrollPanel)

            def picked(ident) -> None:
                if ident is None:
                    return
                host = next(host for key, _, host in self.compare_locations if key == ident)
                self.show_reading_pane()
                self.call_after_refresh(self.move_compare_to, ident, host)
                box.focus()

            self.app.push_screen(Pick("Contents", [(key, label) for key, label, _ in self.compare_locations],
                                      "Calendar results, then corresponding semantic units."), picked)
        else:
            self.navigation.choose(self, self.query_one("#day-reading-a", ScrollPanel),
                                   self.query_one("#day-text-a", Static))

    @work(thread=True, exclusive=True, group="day-share")
    def action_share(self) -> None:
        if self.comparing:
            options = {"orations": self.orations, "bible": self.bible, "territory": self.compare_territory,
                       "companion": self.companion, "textDisplay": self.text_display, "urlLegacy": self.url_legacy}
            location = self.compare_current()
            comparison = {"peer": self.peer()}
        else:
            options = self.options_for(self.calendar)
            location = self.navigation.current(self.query_one("#day-reading-a", ScrollPanel),
                                               self.query_one("#day-text-a", Static))
            comparison = None
        options["location"] = location
        try:
            route = bridge.call(ADAPTER, "readerUrl", "day", self.calendar, self.date.isoformat(), options, comparison)
        except Refused as refusal:
            self.deliver(self.app.notify, str(refusal), severity="warning")
            return
        self.deliver(share, self, route)

    def action_ordinary_language(self) -> None:
        ordinary = (self.views.get(self.calendar) or {}).get("ordinary") or {}
        languages = [(one["lang"], _ordinary_lang_label(one))
                     for one in ordinary.get("languages") or []]
        if not languages:
            self.app.notify("Open Missal mode (m) to choose this edition's Ordinary language.")
            return

        def picked(value) -> None:
            if value:
                self.ordinary_language = value
                self.app.remember_pref("ordinary_language", value)
                self.load()

        self.app.push_screen(Pick("Ordinary Language", languages,
                                  "The oration language stays independently selected; unavailable text stays explicit."),
                             picked)

    @work(thread=True, exclusive=True, group="day-study")
    def action_study(self) -> None:
        panel = self.query_one("#day-reading-a", ScrollPanel)
        text = self.query_one("#day-text-a", Static)
        scrolled = panel.scroll_y > 0.5 or self.navigation.focused is not None
        current_id = self.navigation.current(panel, text) if not self.comparing and self.navigation.entries else None
        current_label = self.navigation.current_label(panel, text) if current_id else ""
        try:
            rows = bridge.call(ADAPTER, "studyDay", self.calendar, self.date.isoformat(), self.options_for(self.calendar))
        except Refused as refusal:
            self.deliver(self.app.notify, str(refusal), severity="warning")
            return
        view = self.views.get(self.calendar) or {}
        view_rows = view.get("rows") or []
        all_study_blocks = [b for row in rows for b in (row.get("blocks") or [])]
        urls, source_ids = missal.extract_study_references(view_rows, all_study_blocks)

        # Match current unit (stripping branch prefix if present).
        unit_blocks: list[dict] = []
        if current_id:
            for row, view_row in zip(rows, view_rows):
                prefix = view_row.get("prefix") or ""
                target = current_id[len(prefix):] if prefix and current_id.startswith(prefix) else current_id
                _, by_event, _ = missal.split_study_blocks(row.get("blocks") or [])
                if target in by_event:
                    unit_blocks.extend(by_event[target])
                    break

        def build_overview(show_audit: bool):
            ink = Ink()
            for branch in view_rows:
                missal.source_witness(ink, branch, detail=True)
                missal.ordinary_conditions(ink, branch)
                if branch.get("notice"):
                    ink.line(missal.format_coverage_notice(branch["notice"]), "italic $text-muted").line()
            # Never dump the Ordinary monograph in Read mode (`self.ordinary` is False).
            if self.ordinary and (view.get("ordinary") or {}).get("advisory"):
                ink.line("Ordinary of the Mass — Witness Notes", "bold $day-color")
                ink.line(view["ordinary"]["advisory"], "italic $text-muted").line()
            for row in rows:
                overview_blocks, _, _ = missal.split_study_blocks(row.get("blocks") or [])
                if row.get("option"):
                    ink.line(row["option"], "bold $day-color")
                missal.blocks(ink, missal.filter_study_audit(overview_blocks, show_audit=show_audit),
                              accent="$day-color")
            return ink.content()

        def build_unit(show_audit: bool):
            ink = Ink()
            if current_label:
                ink.line(current_label, "bold $day-color").line()
            filtered = missal.filter_study_audit(unit_blocks, show_audit=show_audit)
            if filtered:
                missal.blocks(ink, filtered, accent="$day-color")
            else:
                ink.line("No separate unit apparatus is recorded for this anchor; see Overview or All Units.",
                         "italic $text-muted")
            return ink.content()

        def build_all(show_audit: bool):
            ink = Ink()
            for row in rows:
                _, _, all_units = missal.split_study_blocks(row.get("blocks") or [])
                if row.get("option"):
                    ink.line(row["option"], "bold $day-color")
                missal.blocks(ink, missal.filter_study_audit(all_units, show_audit=show_audit),
                              accent="$day-color")
            return ink.content()

        initial_tab = "unit" if (scrolled and unit_blocks) else "overview"
        dialog = StudyDialog(
            "Study This Day",
            overview_builder=build_overview,
            unit_builder=build_unit if unit_blocks else None,
            all_builder=build_all if any(missal.split_study_blocks(r.get("blocks") or [])[2] for r in rows) else None,
            unit_label=current_label,
            initial_tab=initial_tab,
            urls=urls,
            source_ids=source_ids,
            accent="$day-color",
        )
        self.deliver(self.app.push_screen, dialog)

    def source_rows(self) -> list[dict]:
        return (self.views.get(self.calendar) or {}).get("rows") or []

    def reload_reading(self) -> None:
        self.load()

    def action_bible(self) -> None:
        ids = [one["id"] for one in self.bibles]
        if ids:
            self.bible = ids[(ids.index(self.bible) + 1) % len(ids)] if self.bible in ids else ids[0]
            self.app.remember_pref("bible", self.bible)
            self.load()

    def action_propers(self) -> None:
        rows = (self.views.get(self.calendar) or {}).get("rows") or []
        readable = [row for row in rows if row.get("mass")]
        if not readable:
            self.app.notify("No formulary is being read on this date yet.", severity="warning")
            return

        def open_row(row: dict) -> None:
            options = self.options_for(self.calendar)
            options.pop("territory", None)
            options.pop("mass", None)
            options.pop("orationMass", None)
            options.pop("orationTerritory", None)
            options.pop("dedicationAttestation", None)
            options.pop("urlLegacy", None)
            resolved = row.get("resolved") or {}
            if resolved.get("form"):
                options["form"] = resolved["form"]
            cycles = {(event.get("selected") or {}).get("cycle") for event in row.get("events") or []}
            cycles.discard(None)
            if len(cycles) == 1:
                options["cycle"] = cycles.pop()
            self.app.action_surface("propers", calendar=self.calendar, mass=row["mass"]["key"], **options)

        if len(readable) == 1:
            open_row(readable[0])
            return
        self.app.push_screen(
            Pick("Open in Propers", [(str(index), row["mass"]["name"]) for index, row in enumerate(readable)],
                 "Each held territorial branch reads its own formulary."),
            lambda key: key is not None and open_row(readable[int(key)]))

    @on(Month.Chosen)
    def chosen_date(self, event: Month.Chosen) -> None:
        self.go(event.date)
        self.show_reading_pane()

    @on(Month.Highlighted)
    def highlighted_date(self, event: Month.Highlighted) -> None:
        self.update_day_preview(event.date)

    @on(OptionList.OptionSelected, "#day-missal-list")
    def picked_calendar(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("cal-"):
            self.calendar = event.option.id[4:]
            self.app.remember_pref("calendar", self.calendar)
            self.load()
            self.show_reading_pane()

    # --- choices the rubrics leave open -----------------------------------

    def selection(self, calendar: str | None = None) -> dict:
        return self.choices.setdefault((calendar or self.calendar, self.date.isoformat()), {})

    def offers(self, calendar: str) -> tuple[list, dict[int, str], str]:
        """The source's choices stay reachable after a selection, grouped cleanly."""
        view = self.views.get(calendar) or {}
        celebration_items: list = []
        proper_items: list = []
        weekday_items: list = []
        ordinary_groups: list[tuple[str, list]] = []
        oration_locus = ""
        current_week = (view.get("day") or {}).get("week")

        for row in view.get("rows") or []:
            if row.get("failed"):
                continue
            branch = (row.get("heading") or {}).get("label")
            prefix = f"{branch} · " if branch else ""
            context = {**row, "day": {"branches": [row.get("branch") or {}]}}
            path_ids = {path["id"] for path in row.get("sourcePaths") or []}
            proper_choice_ids = {e["id"] for e in row.get("events") or [] if e.get("kind") == "proper-choice"}
            for choice in row.get("unresolvedChoices") or []:
                ident = choice.get("id") or ""
                if ident in path_ids or ident in proper_choice_ids or ident.startswith(("proper-condition/", "common-set:")):
                    continue
                reason = missal.clean_choice_reason(choice, row)
                for option in choice.get("options") or []:
                    celebration_items.append(((calendar, row.get("option"), ident, option["id"], row),
                                              f"{prefix}{missal.option_label(choice, option, context)}   ({reason})"))
            resolved = self.resolved_key(row)
            readable = (row.get("branch") or {}).get("readable") or []
            primary = row.get("primaryDayChoice")
            primary_options = {option["id"] for choice in row.get("unresolvedChoices") or []
                               if choice["id"] == primary for option in choice["options"]}
            if len(readable) > 1 and (resolved or primary):
                for option in readable:
                    if not resolved and option["key"] in primary_options:
                        continue
                    mark = " (selected)" if option["key"] == resolved else ""
                    celebration_items.append(((calendar, row.get("option"), "calendar-formulary", option["key"], row),
                                              f"{prefix}{option.get('label') or option['key']} — {option['state']}{mark}"))
            selected_form = (row.get("resolved") or {}).get("form")
            for option in (row.get("dedicationChoices") or {}).get("options") or []:
                mark = " (confirmed)" if option["id"] == (row.get("dedicationSelection") or {}).get("relation") else ""
                celebration_items.append(((calendar, row.get("option"), "dedication-location", option["id"], row),
                                          f"{prefix}Celebration location: {option['label']}{mark}"))
            forms = (row.get("mass") or {}).get("forms") or []
            if selected_form and len(forms) > 1:
                for form in forms:
                    mark = " (selected)" if form["id"] == selected_form else ""
                    celebration_items.append(((calendar, row.get("option"), "proper-form", form["id"], row),
                                              f"{prefix}{form['name']}   (formulary form){mark}"))
            oration_choices = row.get("orationChoices") or {}
            if oration_choices.get("locus"):
                oration_locus = oration_choices["locus"]
            for option in oration_choices.get("options") or []:
                mark = " (selected)" if option["id"] == (row.get("orationSelection") or {}).get("owner") else ""
                cur = " · current week" if current_week and option["id"] == f"ot-{current_week}" else ""
                weekday_items.append(((calendar, row.get("option"), "weekday-orations", option["id"], row),
                                      f"{prefix}{option['label']}{cur}{mark}"))
            historical = [event.get("sourceLocalActorChoice") for event in row.get("events") or []
                          if (event.get("sourceLocalActorChoice") or {}).get("available")]
            if historical:
                selected = any(offer.get("selected") for offer in historical)
                proper_items.append(((calendar, row.get("option"), "source-local-1970", not selected, row),
                                     prefix + ("Return to unchanged source quotation" if selected else
                                               "Historical 1970 reading (current 2008 correspondence not established)")))
            for path in row.get("sourcePaths") or []:
                for option in path["options"]:
                    if not option["unavailable"] and option.get("properChoices"):
                        proper_items.append(((calendar, row.get("option"), "source-path", option["properChoices"], row),
                                             prefix + option["label"]))
            for event in row.get("events") or []:
                if event.get("kind") == "proper-choice":
                    chosen = (event.get("selection") or {}).get("option")
                    for option in event.get("options") or []:
                        if option.get("unavailable"):
                            continue
                        mark = " (selected)" if option["id"] == chosen else ""
                        proper_items.append(((calendar, row.get("option"), "proper-choice", (event["id"], option["id"]), row),
                                             f"{prefix}{missal.choice_label(event, option)}{mark}"))
        if (view.get("state") or {}).get("territory"):
            celebration_items.append(((calendar, None, "every-branch", None, None),
                                      "Every held territorial branch, as the page shows them"))
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
                gitems.append(((calendar, None, "ordinary-variant", (group["group"], option["id"]), None),
                               f"{option['name']}{app_note}{mark}"))
            if gitems:
                ordinary_groups.append((gname, gitems))

        groups: list[tuple[str, list]] = []
        if celebration_items:
            groups.append(("Celebration & Form", celebration_items))
        if proper_items:
            groups.append(("Proper Options", proper_items))
        if weekday_items:
            heading = f"Weekday Prayers ({oration_locus})" if oration_locus else "Weekday Prayers"
            groups.append((heading, weekday_items))
        groups.extend(ordinary_groups)

        found: list = []
        sections: dict[int, str] = {}
        use_sections = len(groups) > 1 or bool(weekday_items and oration_locus)
        for heading, items in groups:
            if use_sections:
                sections[len(found)] = heading
            found.extend(items)
        hint = ("IGMR 363 permits prayers from any Sunday in Ordinary Time. Nothing is chosen by order."
                if weekday_items and not celebration_items and not proper_items
                else "The rubrics or the sources leave this open. Nothing is chosen by order.")
        return found, sections, hint

    def action_choose(self) -> None:
        if self.comparing:
            held = (getattr(self, "compared", None) or {}).get("territories") or []
            if not held:
                self.app.notify("No territory is held by both missals on this date.")
                return

            def chosen(value) -> None:
                if value:
                    self.compare_territory = "" if value == "universal" else value
                    self.load()

            self.app.push_screen(Pick("Compare Under", [(one, one.replace("-", " ").title()) for one in held],
                                      "The territorial context both sides are read in."), chosen)
            return
        offers, sections, hint = self.offers(self.calendar)
        if not offers:
            self.app.notify("Nothing on this date is left open for the reader to choose.")
            return

        def picked(value) -> None:
            if not value:
                return
            calendar, option, kind, choice, row = value
            selection = self.selection(calendar)
            if kind == "every-branch":
                selection.clear()
                self.load()
                return
            # A choice belongs to the branch it was offered in; making it reads that branch.
            if option and (self.views.get(calendar) or {}).get("multiple"):
                selection.clear()
                selection["territory"] = option
            if kind == "ordinary-variant":
                selection.setdefault("variants", {})[choice[0]] = choice[1]
            elif kind == "calendar-formulary" or (kind == row.get("primaryDayChoice") and not kind.startswith("proper-form:")):
                territory = selection.get("territory")
                selection.clear()
                if territory:
                    selection["territory"] = territory
                selection["mass"] = choice
            elif kind.startswith("proper-form"):
                selection.pop("orationMass", None)
                selection.pop("orationTerritory", None)
                selection.pop("dedicationAttestation", None)
                selection["form"] = choice
                key = (row.get("mass") or {}).get("key") or self.resolved_key(row)
                if key:
                    selection.setdefault("mass", key)
            elif kind == "weekday-orations":
                selection["orationMass"] = choice
                selection["orationTerritory"] = option
            elif kind == "dedication-location":
                context = row["dedicationChoices"]
                label = next(one["label"] for one in context["options"] if one["id"] == choice)
                attestation = {"schema": "triptych-dedication-location/v1", "relation": choice,
                               **{key: context[key] for key in ("calendar", "civilDate", "mass", "formId", "territory")}}

                def confirmed(answer) -> None:
                    if answer == "confirmed":
                        selection["dedicationAttestation"] = attestation
                    elif answer == "unknown":
                        selection.pop("dedicationAttestation", None)
                    else:
                        return
                    self.load()

                self.app.push_screen(Pick("Confirm Celebration Location", [
                    ("confirmed", "I confirm: " + label), ("unknown", "Location unknown; leave unresolved")],
                    "Confirm the actual location of this celebration. This applies only to this date, Mass, form and branch; a shared link does not carry the confirmation."), confirmed)
                return
            elif kind == "proper-choice":
                missal.select_proper_option(selection, row, choice[0], choice[1])
            elif kind.startswith("translation-witness"):
                selection["witness"] = choice
            elif kind == "source-local-1970":
                if choice:
                    selection["sourceLocal1970"] = True
                else:
                    selection.pop("sourceLocal1970", None)
            elif kind == "source-path":
                selection["properChoices"] = choice
                selection.pop("alternative", None)
            else:
                self.app.notify(f"This reader cannot make the choice {kind!r} yet.", severity="warning")
                return
            self.load()

        self.app.push_screen(Pick("Choose", offers, hint, sections=sections or None), picked)

    @staticmethod
    def resolved_key(row: dict) -> str | None:
        resolved = row.get("resolved") or {}
        formulary = resolved.get("formulary")
        return formulary.get("id") if isinstance(formulary, dict) else formulary

    def action_witness(self) -> None:
        view = self.views.get(self.calendar) or {}
        offers = [((None, ""), "No single witness chosen; coequal witnesses remain open")]
        for row in view.get("rows") or []:
            territory = row.get("option") if view.get("multiple") else None
            prefix = (row.get("heading") or {}).get("label") if territory else None
            for witness in (row.get("mass") or {}).get("witnesses") or []:
                label = witness["label"]
                offers.append(((territory, witness["id"]), f"{prefix} · {label}" if prefix else label))
        if len(offers) == 1:
            self.app.notify("No oration witness in this language is recorded for this missal.")
            return

        def picked(value) -> None:
            if value is None:
                return
            territory, witness = value
            selection = self.selection()
            if territory:
                selection["territory"] = territory
            if witness:
                selection["witness"] = witness
            else:
                selection.pop("witness", None)
            self.load()

        self.app.push_screen(Pick("Oration Witness", offers, "A missing text stays missing; no other witness fills it."),
                             picked)

    # --- loading ---------------------------------------------------------

    def options_for(self, calendar: str) -> dict:
        chosen = dict(self.choices.get((calendar, self.date.isoformat()), {}))
        options = {"orations": self.orations, "bible": self.bible, "ordinary": self.ordinary,
                   "ordinaryLang": self.ordinary_language or self.orations, "textDisplay": self.text_display,
                   "companion": self.companion, "rubrics": self.rubrics, "urlLegacy": self.url_legacy}
        options.update({key: value for key, value in chosen.items() if value})
        return options

    def peer(self) -> str:
        ids = [one["id"] for one in self.calendars]
        if getattr(self, "chosen_peer", None) in ids and self.chosen_peer != self.calendar:
            return self.chosen_peer
        return ids[(ids.index(self.calendar) + 1) % len(ids)] if len(ids) > 1 else self.calendar

    def action_peer(self) -> None:
        others = [(one["id"], one["short"]) for one in self.calendars if one["id"] != self.calendar]
        if not others:
            return

        def picked(value) -> None:
            if value:
                self.chosen_peer = value
                if not self.comparing:
                    self.action_compare()
                else:
                    self.load()

        self.app.push_screen(Pick("Compare With", others, "The other missal, read on the same date."), picked)

    def load(self) -> None:
        if not self.calendars:
            return
        self.query_one(Month).chosen = self.date
        self.fetch(self.date, self.calendar, self.comparing)

    @work(thread=True, exclusive=True, group="day-load")
    def fetch(self, date: dt.date, calendar: str, comparing: bool) -> None:
        iso, month = date.isoformat(), date.strftime("%Y-%m")
        views: dict[str, dict] = {}
        try:
            for one in self.calendars:
                key = (one["id"], month)
                if key not in self.months:
                    self.months[key] = bridge.call(ADAPTER, "month", one["id"], month)
            try:
                views[calendar] = bridge.call(ADAPTER, "day", calendar, iso, self.options_for(calendar))
            except Refused as refusal:
                views[calendar] = {"refused": str(refusal), "calendar": calendar, "date": iso}
            compared = None
            if comparing:
                # The page's Compare takes no Mass, form or witness of its own
                # (day-compare.js:31-46 preflight): only the language, the Bible
                # and a territory both sides hold.
                asked = {"orations": self.orations, "bible": self.bible, "companion": self.companion,
                         "textDisplay": self.text_display}
                if self.compare_territory:
                    asked["territory"] = self.compare_territory
                try:
                    compared = bridge.call(ADAPTER, "compare", calendar, self.peer(), iso, asked)
                except Refused as refusal:
                    compared = {"refused": str(refusal), "territories": []}
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.show, date, views, compared)

    # --- drawing ---------------------------------------------------------

    def mark(self, date: dt.date) -> tuple[str, str] | None:
        rows = self.months.get((self.calendar, date.strftime("%Y-%m")))
        if not rows:
            return None
        row = next((one for one in rows["days"] if one["date"] == date.isoformat()), None)
        if not row:
            return None
        if row.get("refused"):
            return REFUSED, "$error"
        hue = tone(row.get("season"))
        branches = row.get("branches") or []
        if len(branches) > 1 or any(branch.get("choiceRequired") for branch in branches):
            return "⑂", hue
        if branches and branches[0].get("weekdayOrationOpen"):
            return OPEN_ORATION_MARK, hue
        if branches and branches[0].get("settled") is False:
            return "?", "$warning"
        return rank_glyph(branches[0].get("winner") if branches else None), hue

    def update_day_preview(self, date: dt.date) -> None:
        preview_widget = self.query_one("#day-preview", Static)
        rows = self.months.get((self.calendar, date.strftime("%Y-%m")))
        row = next((one for one in (rows or {}).get("days") or [] if one["date"] == date.isoformat()), None)
        ink = Ink()
        short_date = date.strftime("%a %-d %b")
        if not row:
            ink(short_date, "$text-muted")
        elif row.get("refused"):
            ink(f"{short_date} · refused", "$error")
        else:
            branches = row.get("branches") or []
            glyph, hue = self.mark(date) or ("", "")
            width = max(24, (self.query_one("#day-left").size.width or 36) - 4)
            lead = f"{short_date} · "
            if len(branches) > 1:
                summary = f"⑂ {len(branches)} branches"
            elif branches and branches[0].get("choiceRequired"):
                summary = "⑂ " + (branches[0].get("preview") or "Choice of Mass")
            elif branches and branches[0].get("weekdayOrationOpen"):
                summary = branches[0].get("preview") or "Weekday (open prayers)"
            elif branches and branches[0].get("winner"):
                summary = branches[0]["winner"]["name"]
            else:
                summary = branches[0].get("preview") or "Not settled" if branches else "No Mass"
            ink(lead, "$text-muted")(_trim(summary, max(12, width - len(lead))), hue or "")
        preview_widget.update(ink.content())

    def where(self) -> str:
        view = self.views.get(self.calendar) or {}
        edition = next((one["short"] for one in self.calendars if one["id"] == self.calendar), self.calendar)
        mode = "Compare" if self.comparing else ("Missal" if self.ordinary else "Read")
        language = "Bilingual" if self.text_display == "latin-and-selected" else ("English" if self.orations == "en" else "Latin")
        return f"{self.date.strftime('%a %d %b %Y')} · {edition} · {mode} · {language} · {view.get('title') or '—'}"

    def show(self, date: dt.date, views: dict[str, dict], compared: dict | None = None) -> None:
        if date != self.date:
            return
        self.views = views
        self.compared = compared
        self.query_one(Month).refresh()
        self.update_day_preview(self.date)
        self.query_one("#day-legend", Static).update(
            legend_for(self.months.get((self.calendar, self.date.strftime("%Y-%m")))).content())
        self.show_missals()
        self.redraw()
        self.app.refresh_where()
        if self.pending_study:
            self.pending_study = False
            self.action_study()

    def redraw(self) -> None:
        self.set_class(self._is_bilingual_spread() and not self.comparing, "bilingual")
        self.show_why(self.views.get(self.calendar))
        if self.comparing:
            self.show_compare(getattr(self, "compared", None) or {})
        else:
            self.show_reading("#day-reading-a", "#day-text-a", self.views.get(self.calendar), self.calendar)

    @staticmethod
    def compare_sections(blocks: list[dict]) -> list[dict]:
        """The page's compare document, cut where it is cut: a heading opens a
        section, and each side's own heading opens that side's column."""
        sections = [{"title": None, "lead": [], "sides": []}]
        for block in blocks:
            classes = block.get("classes") or []
            if block.get("tag") == "h2":
                sections.append({"title": block, "lead": [], "sides": []})
            elif block.get("tag") == "h3" and ({"compare-side-title", "compare-calendar-side"} & set(classes)):
                sections[-1]["sides"].append([block])
            elif sections[-1]["sides"]:
                sections[-1]["sides"][-1].append(block)
            else:
                sections[-1]["lead"].append(block)
        return [one for one in sections if one["title"] or one["lead"] or one["sides"]]

    def show_compare(self, compared: dict) -> None:
        box = self.query_one("#day-compare", ScrollPanel)
        restore = self.navigation.pending or self.compare_current()
        self.navigation.pending = None
        self.compare_locations = []
        self.compare_focus = None
        peer = next((one["short"] for one in self.calendars if one["id"] == self.peer()), self.peer())
        edition = next((one["short"] for one in self.calendars if one["id"] == self.calendar), self.calendar)
        box.retitle(f"{compared.get('title') or 'Compare'} · {edition} & {peer}")
        language = "English" if self.orations == "en" else "Latin"
        territory = self.compare_territory or "universal"
        box.border_subtitle = f"Compare · {language} orations · {territory} · V another missal · s territory"
        widgets = []
        if compared.get("refused"):
            # The page fails closed, and says why (day-reader.js renderFailure).
            ink = Ink().line("This comparison cannot be made as asked", "bold $warning")
            ink.line(compared["refused"], "italic $warning").line()
            ink.line("Compare reads each missal's own result for the date and pairs their Propers; it does not "
                     "choose for either side. Leave compare (v) to make a choice on the missal that holds one.",
                     "italic $text-muted")
            if compared.get("territories"):
                ink.line(f"Territories both sides hold: {', '.join(compared['territories'])}", "$text-muted")
            widgets.append(Static(ink.content()))
        else:
            head = Ink().line(compared.get("longDate") or "", "bold $day-color")
            head.line(compared.get("metadata") or "", "$text-muted")
            if compared.get("notice"):
                head.line(compared["notice"], "italic $text-muted")
            widgets.append(Static(head.content()))
            source_sections = [{"id": None, "label": "Introduction", "blocks": compared.get("lead") or []}]
            source_sections += compared.get("sections") or []
            units = ((source, section) for source in source_sections
                     for section in self.compare_sections(source["blocks"]))
            for source_section, section in units:
                parts = []
                if section["title"] or section["lead"]:
                    lead = missal.blocks(Ink(), ([section["title"]] if section["title"] else []) + section["lead"],
                                         accent="$day-color")
                    parts.append(Static(lead.content()))
                columns = [Static(missal.blocks(Ink(), side, accent="$day-color").content(), classes="compare-side")
                           for side in section["sides"]]
                if len(columns) == 2:
                    parts.append(Horizontal(*columns))
                else:
                    parts.extend(columns)
                unit = Vertical(*parts, classes="compare-unit")
                if source_section.get("id"):
                    self.compare_locations.append((source_section["id"], source_section["label"], unit))
                widgets.append(unit)

        self.mount_comparison(widgets, restore)

    @work(exclusive=True, group="day-compare-layout")
    async def mount_comparison(self, widgets: list, restore: str | None) -> None:
        body = self.query_one("#day-compare-body", Vertical)
        await body.remove_children()
        await body.mount_all(widgets)

        def restore_location() -> None:
            host = next((host for ident, _, host in self.compare_locations if ident == restore), None)
            if host:
                self.move_compare_to(restore, host)
            else:
                self.query_one("#day-compare", ScrollPanel).scroll_home(animate=False)

        self.call_after_refresh(restore_location)

    def move_compare_to(self, ident: str, host) -> None:
        box = self.query_one("#day-compare", ScrollPanel)
        box.scroll_to_widget(host, top=True, animate=False, force=True, immediate=True)
        self.compare_focus = (ident, box.scroll_y)

    def compare_current(self) -> str | None:
        box = self.query_one("#day-compare", ScrollPanel)
        if self.compare_focus and abs(self.compare_focus[1] - box.scroll_y) < 0.5:
            return self.compare_focus[0]
        self.compare_focus = None
        return next((ident for ident, _, host in reversed(self.compare_locations)
                     if host.virtual_region.y <= box.scroll_y), None)

    def show_missals(self) -> None:
        listing = self.query_one("#day-missal-list", OptionList)
        listing.clear_options()
        month = self.date.strftime("%Y-%m")
        rail_w = self.query_one("#day-left").size.width or 36
        # Inner content width: subtract box border (2) + panel padding (2) + OptionList padding (2).
        inner_w = max(22, rail_w - 6)
        active_view = self.views.get(self.calendar) or {}
        active_rows = active_view.get("rows") or []
        for one in self.calendars:
            rows = self.months.get((one["id"], month)) or {"days": []}
            row = next((day for day in rows["days"] if day["date"] == self.date.isoformat()), None)
            ink = Ink()
            ink("● " if one["id"] == self.calendar else "  ", "bold $day-color")
            ink.line(_trim(one["short"], max(14, inner_w - 2)), "bold")
            ink("  ")
            if not row or row.get("refused"):
                ink.line(_trim((row or {}).get("refused") or "no day", inner_w - 2), "italic $warning")
            else:
                branches = row["branches"]
                # Sync active user selection on open-choice days instead of showing stale `⑂ a choice of Mass`.
                chosen_mass = None
                if one["id"] == self.calendar and len(active_rows) == 1 and active_rows[0].get("mass") and not active_rows[0].get("primaryDayChoice"):
                    chosen_mass = active_rows[0]["mass"]["name"]
                if len(branches) > 1:
                    ink.line(_trim(f"⑂ {len(branches)} territorial branches", inner_w - 2), "$warning")
                elif branches and branches[0]["choiceRequired"]:
                    if chosen_mass:
                        ink("✓ ", "bold $day-color").line(_trim(chosen_mass, max(12, inner_w - 4)))
                    else:
                        ink.line(_trim("⑂ Choice of Mass", inner_w - 2), "$warning")
                elif branches and branches[0].get("weekdayOrationOpen"):
                    if chosen_mass and active_rows[0].get("orationSelection"):
                        ink("✓ ", "bold $day-color").line(_trim(chosen_mass, max(12, inner_w - 4)))
                    else:
                        ink(f"{OPEN_ORATION_MARK} ", tone(row.get("season"))).line(
                            _trim(branches[0].get("preview") or "Weekday (open prayers)", max(12, inner_w - 4)))
                elif branches and branches[0]["settled"] is False:
                    ink.line(_trim("? Not settled here", inner_w - 2), "$warning")
                elif branches and branches[0]["winner"]:
                    winner = branches[0]["winner"]
                    glyph = rank_glyph(winner).strip()
                    prefix = (glyph + " ") if glyph else ""
                    if prefix:
                        ink(prefix, "bold")
                    ink.line(_trim(winner["name"], max(12, inner_w - 2 - len(prefix))))
                else:
                    ink.line("No Mass held", "$text-muted")
                meta_parts = [season_name(row.get("season"))]
                if row.get("week"):
                    meta_parts[0] = f"{meta_parts[0]}, wk {row['week']}" if meta_parts[0] else f"Week {row['week']}"
                if branches and branches[0].get("winner") and len(branches) == 1:
                    rw = rank_words(branches[0]["winner"])
                    if rw:
                        meta_parts.append(rw)
                meta_str = _trim(" · ".join(p for p in meta_parts if p), inner_w - 2)
                if meta_str:
                    first_seg, sep, rest = meta_str.partition(" · ")
                    ink("  ")(first_seg, tone(row.get("season")))
                    if sep:
                        ink(f" · {rest}", "$text-muted")
            listing.add_option(Option(ink.content(), id=f"cal-{one['id']}"))
        box = self.query_one("#day-missals", Panel)
        box.border_subtitle = "c next · enter read"
        calendar_box = self.query_one("#day-calendar", Panel)
        calendar_box.retitle(self.date.strftime("%B %Y"))
        calendar_box.border_subtitle = "? marks · ↑↓←→ browse"

    def show_why(self, view: dict | None) -> None:
        box = self.query_one("#day-why", ScrollPanel)
        text = self.query_one("#day-why-text", Static)
        ink = Ink()
        if not view or view.get("refused"):
            text.update(ink((view or {}).get("refused") or "", "italic $warning").content())
            return
        day = view["day"]
        ink(season_name(day.get("season")), "bold " + tone(day.get("season")))
        if day.get("week"):
            ink(f", week {day['week']}")
        ink.line()
        year = day.get("year") or {}
        if year.get("label"):
            ink.line(year["label"], "$text-muted")
        lectionary = year.get("lectionary") or {}
        if lectionary:
            ink.line(f"Lectionary: Year {lectionary.get('sunday') or '—'} · Weekday {lectionary.get('weekday') or '—'}",
                     "$text-muted")
        for row in year.get("unresolved") or []:
            ink.line(f"? {row.get('what')}: {row.get('why')}", "italic $warning")
        # The page's own "Why this Mass" (day-reader.js reasoningApparatus), per branch.
        for row in view.get("rows") or []:
            ink.line()
            heading = row.get("heading")
            if heading:
                ink.line(heading["label"], "bold $day-color")
            if row.get("failed"):
                ink.line(row["failed"], "italic $warning")
                continue
            missal.blocks(ink, row.get("reasoning") or [], accent="$day-color")
        ink.line()
        for name in ("dayAdvisory", "advisory"):
            if day.get(name):
                ink.line(day[name], "italic $text-muted").line()
        text.update(ink.content())
        box.retitle("Why This Mass · " + next((one["short"] for one in self.calendars if one["id"] == view["calendar"]),
                                              view["calendar"]))
        box.scroll_home(animate=False)

    def show_reading(self, box_id: str, text_id: str, view: dict | None, calendar: str) -> None:
        box = self.query_one(box_id, ScrollPanel)
        text = self.query_one(text_id, Static)
        edition = next((one["short"] for one in self.calendars if one["id"] == calendar), calendar)
        ink = Ink()
        if not view:
            text.update("")
            return
        if view.get("refused"):
            box.retitle(edition)
            text.update(ink.line(view["refused"], "bold $error").content())
            return
        state = view.get("state") or {}
        rows = view.get("rows") or []
        pair_w = self.pair_column_width() if self._is_bilingual_spread() else 0
        self._last_pair_width = pair_w
        term_w = self.size.width or (self.app.size.width if self.app else 78)
        nav_shown = not self.has_class("compact") and not self.has_class("focus")
        avail_w = max(24, term_w - (46 if nav_shown else 10))
        rule_w = min(pair_w or 72, avail_w)
        ink._pair_width = pair_w
        ink._rule_width = rule_w

        self.navigation.begin((calendar, view["date"]), box, text)
        box.retitle(edition)

        mode = "Missal" if state.get("ordinary") else "Read"
        language = "English" if state.get("orations") == "en" else "Latin"
        sub_parts = [mode, f"{language} orations"]
        if state.get("ordinary"):
            ord_lang = "English" if (state.get("ordinaryLang") or state.get("orations")) == "en" else "Latin"
            sub_parts.append(f"{ord_lang} Ordinary")
        if state.get("textDisplay") == "latin-and-selected":
            sub_parts.append("Bilingual")
        sub_parts.append(view["bible"]["label"])
        if state.get("companion"):
            comp_label = next((b["label"] for b in self.bibles if b["id"] == state["companion"]), state["companion"])
            sub_parts.append(f"Latin Bible: {comp_label}")
        for name in ("form", "witness"):
            if state.get(name):
                sub_parts.append(f"{name}: {state[name]}")
        box.border_subtitle = " · ".join(sub_parts)

        configured = bool(state.get("ordinary") and any(row.get("events") for row in rows))
        day_info = view.get("day") or {}
        branches = day_info.get("branches") or []
        winner = branches[0].get("winner") if len(branches) == 1 else None

        # Ceremonial Hand-Missal Header (3 crisp lines -> immediately into the liturgy!)
        ink.line(view["title"], "bold $day-color")
        ribbon_parts: list[tuple[str, str]] = [(view.get("longDate") or view["date"], "")]
        sname = season_name(day_info.get("season"))
        if sname:
            ribbon_parts.append((sname, tone(day_info.get("season"))))
        if winner:
            rw = rank_words(winner)
            if rw:
                ribbon_parts.append((rw, "$text-muted"))
        lectionary = ((day_info.get("year") or {}).get("lectionary")) or {}
        if lectionary.get("sunday") or lectionary.get("weekday"):
            lec = " · ".join(p for p in (
                f"Year {lectionary['sunday']}" if lectionary.get("sunday") else "",
                f"Weekday {lectionary['weekday']}" if lectionary.get("weekday") else "",
            ) if p)
            if lec:
                ribbon_parts.append((lec, "$text-muted"))
        for idx, (part, style) in enumerate(ribbon_parts):
            if idx:
                ink(" · ", "$text-muted")
            ink(part, style)
        ink.line()
        ink.line("─" * rule_w, "$rule")

        if view.get("multiple"):
            ink.line("All held territorial branches are shown; no locality is inferred.", "italic $text-muted")
            territorial = (self.opening.get("territorial") or {}).get(calendar)
            if territorial:
                ink.line(territorial, "italic $text-muted")

        for row_idx, row in enumerate(rows):
            if row_idx > 0 or view.get("multiple"):
                ink.line()
            heading = row.get("heading")
            if heading:
                ink.line(heading["label"], "bold $day-color")
                ink.line(heading["title"], "bold")
            if row.get("failed"):
                ink.line(row["failed"], "italic $warning")
                continue
            # Only show Formulary line when borrowed (e.g., feria taking a Sunday Mass).
            if row.get("mass") and not heading and row["mass"]["name"] != view["title"]:
                ink("Takes the Mass of: ", "$text-muted").line(row["mass"]["name"], "bold")
            resolved = row.get("resolved") or {}
            if resolved.get("standing") and resolved["standing"] != "said":
                ink.line(standing_words(resolved["standing"]), "bold $warning")
            # Per-branch notices: move routine complete coverage telemetry to Study (d) so
            # even 60x16 shows actual liturgical text above the fold. Keep recension caveats,
            # real partial coverage, selections, and unsettled notices visible right on the branch!
            recension = (row.get("mass") or {}).get("recension")
            notice = row.get("notice") or ""
            if configured:
                if recension:
                    ink.line(recension, "italic $warning")
                if row.get("dedicationSelection"):
                    ink.line("Celebration location: " + row["dedicationSelection"]["label"], "$text-muted")
                if row.get("orationSelection"):
                    ink.line("Prayers from " + row["orationSelection"]["label"], "$text-muted")
            elif notice and not missal.is_complete_notice(notice, recension=recension):
                ink.line(missal.format_coverage_notice(notice), "italic $warning" if recension else "italic $text-muted")
            elif row.get("orationSelection"):
                ink.line("Prayers from " + row["orationSelection"]["label"], "$text-muted")
            elif row.get("dedicationSelection"):
                ink.line("Celebration location: " + row["dedicationSelection"]["label"], "$text-muted")
            for unsettled in row.get("unsettled") or []:
                ink.line(unsettled, "italic $warning")

            context = {**row, "day": {"branches": [row.get("branch") or {}]}, "ordinary": view.get("ordinary"), "state": state}
            missal.source_witness(ink, row)
            missal.choices(ink, context)
            for path in row.get("sourcePaths") or []:
                if not path.get("beforeEventId"):
                    missal.blocks(ink, path["blocks"], accent="$day-color", pair_width=pair_w)
            missal.ordinary_conditions(ink, row, compact=configured)

            emitted_any = False
            for event in context.get("events") or []:
                if not self.rubrics and (event.get("element") or {}).get("kind") == "rubric":
                    continue
                for path in row.get("sourcePaths") or []:
                    if path.get("beforeEventId") == event["id"]:
                        missal.blocks(ink, path["blocks"], accent="$day-color", pair_width=pair_w)
                if missal.is_contents_event(event):
                    label = missal.event_label(event, indent_children=bool(state.get("ordinary")))
                    prefix = row.get("prefix") or ""
                    branch_label = f"{row['option']} · " if prefix else ""
                    self.navigation.mark(prefix + event["id"], branch_label + label, ink)
                ink._leading_blank = emitted_any
                missal.events(ink, {**context, "events": [event]}, rubrics=self.rubrics, accent="$day-color")
                emitted_any = True
        # The Ordinary's own advisory, at the foot only in Missal mode when unconfigured.
        if not configured and state.get("ordinary") and (view.get("ordinary") or {}).get("advisory"):
            ink.line().line(view["ordinary"]["advisory"], "italic $text-muted")
        text.update(ink.content())
        self.navigation.finish(self, box, text)
