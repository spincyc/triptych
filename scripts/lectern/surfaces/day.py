"""Today's Missal: the Mass a date appoints, in each missal, with the rubric behind it."""
from __future__ import annotations

import datetime as dt

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge, missal
from ..dialogs import Ask, Pick
from ..month import Month
from ..repo import Refused
from ..surface import Surface
from ..theme import SEASON_TONES
from ..widgets import Ink, Panel, ScrollPanel, literal

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
        legend("◆", "bold")(" class I  ")("◇", "bold")(" class II  ")("•", "bold").line(" class III")
        legend.line("blank: class IV", "$text-muted")
    else:
        legend("◆", "bold")(" solemnity  ")("◇", "bold")(" feast  ")("•", "bold").line(" memorial")
        legend("○", "bold")(" Sunday  ")("blank: weekday", "$text-muted").line()
    legend("?", "bold $warning")(" not settled  ")("⑂", "bold $warning")(" a choice  ")
    legend(REFUSED, "bold $error").line(" refused")
    legend.line("hue = season; no colour is recorded", "italic $text-muted")
    return legend


def season_name(season: str | None) -> str:
    names = {"after-pentecost": "after Pentecost", "ordinary-time": "Ordinary Time", "holy-week": "Holy Week"}
    if not season:
        return ""
    return names.get(season, season.replace("-", " ").capitalize())


def rank_words(winner: dict | None) -> str:
    if not winner:
        return ""
    if winner.get("class"):
        return f"class {winner['class']}"
    return (winner.get("nature") or "").replace("-", " ")


class Day(Surface):
    key = "1"
    label = "Day"
    FIRST = "#day-reading-a"
    HELP = (
        ("← / →", "previous / next day"),
        ("[ / ]", "previous / next week"),
        ("{ / }", "previous / next month"),
        ("t", "today"),
        ("g", "go to a date (YYYY-MM-DD)"),
        ("c", "next missal (postconciliar, 1962, pre-1955)"),
        ("v", "compare: this missal beside another, on the same date"),
        ("V", "choose the missal to compare with"),
        ("m", "missal mode: the propers seated in the Ordinary"),
        ("o", "orations in English or Latin"),
        ("b", "next Bible edition for the readings"),
        ("w", "choose an oration witness, where several are held"),
        ("s", "make a choice the rubrics leave open (Mass, form, branch, cycle)"),
        ("r", "rubrics shown or hidden in missal mode"),
        ("p", "open this formulary in the Propers surface"),
        ("f", "focus: the reading alone, full width; again to restore"),
    )
    BINDINGS = [
        Binding("left,h", "step(-1)", "previous day", show=False),
        Binding("right,l", "step(1)", "next day", show=False),
        Binding("left_square_bracket", "step(-7)", "previous week", show=False),
        Binding("right_square_bracket", "step(7)", "next week", show=False),
        Binding("left_curly_bracket", "month(-1)", "previous month", show=False),
        Binding("right_curly_bracket", "month(1)", "next month", show=False),
        Binding("t", "today", "today"),
        Binding("g", "goto", "go to"),
        Binding("c", "calendar", "next missal"),
        Binding("v", "compare", "compare"),
        Binding("V", "peer", "compare with…", show=False),
        Binding("m", "missal", "with the Ordinary"),
        Binding("o", "orations", "en/la"),
        Binding("b", "bible", "bible", show=False),
        Binding("w", "witness", "witness", show=False),
        Binding("s", "choose", "choose"),
        Binding("r", "rubrics", "rubrics", show=False),
        Binding("p", "propers", "propers", show=False),
    ]
    CSS = """
    .day.focus #day-left { display: none; }
    .day.narrow #day-left { width: 32; }
    .day.narrow #day-legend { display: none; }
    .day.wide #day-left { width: 50; }
    """
    DEFAULT_CSS = """
    Day #day-left { width: 40; }
    Day #day-calendar { height: auto; }
    Day #day-missals { height: auto; }
    Day #day-why { height: 1fr; }
    Day #day-reading-b { display: none; }
    Day.comparing #day-reading-b { display: block; }
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
        self.ordinary = False
        self.rubrics = True
        self.comparing = False
        self.months: dict[tuple[str, str], dict] = {}
        self.choices: dict[tuple[str, str], dict] = {}
        self.views: dict[str, dict] = {}
        self.opening: dict = {}

    # --- building --------------------------------------------------------

    def build(self) -> None:
        self.today = self.app.today
        if not self.pinned:
            self.date = self.today
        self.mount(
            Horizontal(
                Vertical(
                    Panel(Month(mark=self.mark, today=self.today, id="day-month"),
                          Static("", id="day-legend"), title="calendar", id="day-calendar"),
                    Panel(OptionList(id="day-missal-list"), title="missals", id="day-missals"),
                    ScrollPanel(Static("", id="day-why-text"), title="why", id="day-why"),
                    id="day-left",
                ),
                Horizontal(
                    ScrollPanel(Static("", id="day-text-a"), title="mass", id="day-reading-a"),
                    ScrollPanel(Static("", id="day-text-b"), title="mass", id="day-reading-b"),
                ),
            )
        )
        self.start()

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
        ids = [one["id"] for one in self.calendars]
        if self.calendar not in ids:
            if self.calendar:
                self.app.notify(f"No missal called {self.calendar!r} is offered here.", severity="warning")
            self.calendar = opening.get("default") if opening.get("default") in ids else ids[0]
        # The page's own defaults: the declared Bible and the Missal's own
        # language (reader-state.js DEFAULT_BIBLE_ID; Triptych.SOURCE_LANGUAGE).
        if not self.bible:
            self.bible = opening.get("defaultBible") or self.bibles[0]["id"]
        if not self.orations:
            self.orations = opening.get("defaultOrations") or "la"
        self.adopt_pending()
        self.load()

    def fail(self, message: str) -> None:
        self.query_one("#day-text-a", Static).update(Ink()(message, "bold $error").content())

    # --- intent and movement ---------------------------------------------

    def follow(self, date: str | None = None, calendar: str | None = None, mass: str | None = None, **_) -> None:
        if date:
            self.date = dt.date.fromisoformat(date)
            self.pinned = True
        if calendar:
            self.calendar = calendar
        if mass:
            self.pending_mass = mass
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
            try:
                self.go(dt.date.fromisoformat(value))
            except ValueError:
                self.app.notify(f"Not a date: {literal(repr(value))}. Write it YYYY-MM-DD.", severity="warning")

        self.app.push_screen(Ask("go to a date", "A civil date, YYYY-MM-DD", self.date.isoformat()), answered)

    def action_calendar(self) -> None:
        ids = [one["id"] for one in self.calendars]
        if ids:
            self.calendar = ids[(ids.index(self.calendar) + 1) % len(ids)]
            self.load()

    def action_compare(self) -> None:
        self.comparing = not self.comparing
        self.set_class(self.comparing, "comparing")
        self.load()

    def action_missal(self) -> None:
        self.ordinary = not self.ordinary
        self.load()

    def action_rubrics(self) -> None:
        self.rubrics = not self.rubrics
        self.redraw()

    def action_orations(self) -> None:
        self.orations = "la" if self.orations == "en" else "en"
        for selection in self.choices.values():
            selection.pop("witness", None)
        self.load()

    def action_bible(self) -> None:
        ids = [one["id"] for one in self.bibles]
        if ids:
            self.bible = ids[(ids.index(self.bible) + 1) % len(ids)] if self.bible in ids else ids[0]
            self.load()

    def action_propers(self) -> None:
        rows = (self.views.get(self.calendar) or {}).get("rows") or []
        masses = [row["mass"] for row in rows if row.get("mass")]
        if not masses:
            self.app.notify("No formulary is being read on this date yet.", severity="warning")
            return
        if len(masses) == 1:
            self.app.action_surface("propers", calendar=self.calendar, mass=masses[0]["key"])
            return
        self.app.push_screen(
            Pick("open in propers", [(one["key"], one["name"]) for one in masses],
                 "Each held territorial branch reads its own formulary."),
            lambda key: key and self.app.action_surface("propers", calendar=self.calendar, mass=key))

    @on(Month.Chosen)
    def chosen_date(self, event: Month.Chosen) -> None:
        self.go(event.date)

    @on(OptionList.OptionSelected, "#day-missal-list")
    def picked_calendar(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("cal-"):
            self.calendar = event.option.id[4:]
            self.load()

    # --- choices the rubrics leave open -----------------------------------

    def selection(self, calendar: str | None = None) -> dict:
        return self.choices.setdefault((calendar or self.calendar, self.date.isoformat()), {})

    def offers(self, calendar: str) -> list:
        """Every open choice of one missal's reading, each tagged with its branch."""
        view = self.views.get(calendar) or {}
        found = []
        for row in view.get("rows") or []:
            branch = (row.get("heading") or {}).get("label")
            prefix = f"{branch} · " if branch else ""
            context = {**row, "day": {"branches": [row.get("branch") or {}]}}
            for choice in row.get("unresolvedChoices") or []:
                ident = choice.get("id") or ""
                for option in choice.get("options") or []:
                    found.append(((calendar, row.get("option"), ident, option["id"], row),
                                  f"{prefix}{missal.option_label(choice, option, context)}"
                                  f"   ({choice.get('reason') or ident})"))
            for event in row.get("events") or []:
                if event.get("kind") == "proper-choice":
                    for option in event.get("options") or []:
                        if option.get("unavailable"):
                            continue
                        found.append(((calendar, row.get("option"), "proper-choice", (event["id"], option["id"]), row),
                                      f"{prefix}{missal.choice_label(event, option)}"))
        if (view.get("state") or {}).get("territory"):
            found.append(((calendar, None, "every-branch", None, None),
                          "every held territorial branch, as the page shows them"))
        return found

    def action_choose(self) -> None:
        sides = [self.calendar] + ([self.peer()] if self.comparing and self.peer() != self.calendar else [])
        offers = []
        for side in sides:
            edition = next((one["short"] for one in self.calendars if one["id"] == side), side)
            for value, label in self.offers(side):
                offers.append((value, f"{edition} · {label}" if len(sides) > 1 else label))
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
            if kind == "calendar-formulary":
                territory = selection.get("territory")
                selection.clear()
                if territory:
                    selection["territory"] = territory
                selection["mass"] = choice
            elif kind.startswith("proper-form"):
                selection["form"] = choice
                key = (row.get("mass") or {}).get("key") or self.resolved_key(row)
                if key:
                    selection.setdefault("mass", key)
            elif kind == "proper-choice":
                selection.setdefault("properChoices", {})[choice[0]] = choice[1]
            elif kind.startswith("translation-witness"):
                selection["witness"] = choice
            else:
                self.app.notify(f"This reader cannot make the choice {kind!r} yet.", severity="warning")
                return
            self.load()

        self.app.push_screen(Pick("choose", offers,
                                  "The rubrics or the sources leave this open. Nothing is chosen by order."), picked)

    @staticmethod
    def resolved_key(row: dict) -> str | None:
        resolved = row.get("resolved") or {}
        formulary = resolved.get("formulary")
        return formulary.get("id") if isinstance(formulary, dict) else formulary

    def action_witness(self) -> None:
        rows = (self.views.get(self.calendar) or {}).get("rows") or []
        witnesses = next((row["mass"].get("witnesses") for row in rows if row.get("mass")), None) or []
        if not witnesses:
            self.app.notify("No oration witness in this language is recorded for this missal.")
            return
        offers = [("", "every held witness, each named (no single witness chosen)")]
        offers += [(one["source_id"], f"{one['label'] or 'Triptych'}  ·  {one['held']} held") for one in witnesses]

        def picked(value) -> None:
            if value is None:
                return
            selection = self.selection()
            if value:
                selection["witness"] = value
            else:
                selection.pop("witness", None)
            self.load()

        self.app.push_screen(Pick("oration witness", offers, "A missing text stays missing; no other witness fills it."),
                             picked)

    # --- loading ---------------------------------------------------------

    def options_for(self, calendar: str) -> dict:
        chosen = dict(self.choices.get((calendar, self.date.isoformat()), {}))
        options = {"orations": self.orations, "bible": self.bible, "ordinary": self.ordinary,
                   "ordinaryLang": self.orations}
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

        self.app.push_screen(Pick("compare with", others, "The other missal, read on the same date."), picked)

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
            wanted = [calendar] + ([self.peer()] if comparing else [])
            for name in wanted:
                try:
                    views[name] = bridge.call(ADAPTER, "day", name, iso, self.options_for(name))
                except Refused as refusal:
                    views[name] = {"refused": str(refusal), "calendar": name, "date": iso}
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.show, date, views)

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
        if branches and branches[0].get("settled") is False:
            return "?", hue
        return rank_glyph(branches[0].get("winner") if branches else None), hue

    def where(self) -> str:
        view = self.views.get(self.calendar) or {}
        edition = next((one["short"] for one in self.calendars if one["id"] == self.calendar), self.calendar)
        return f"{self.date.strftime('%a %d %b %Y')} · {edition} · {view.get('title') or '—'}"

    def show(self, date: dt.date, views: dict[str, dict]) -> None:
        if date != self.date:
            return
        self.views = views
        self.query_one(Month).refresh()
        self.query_one("#day-legend", Static).update(
            legend_for(self.months.get((self.calendar, self.date.strftime("%Y-%m")))).content())
        self.show_missals()
        self.redraw()
        self.app.refresh_where()

    def redraw(self) -> None:
        self.show_why(self.views.get(self.calendar))
        self.show_reading("#day-reading-a", "#day-text-a", self.views.get(self.calendar), self.calendar)
        if self.comparing:
            peer = self.peer()
            self.show_reading("#day-reading-b", "#day-text-b", self.views.get(peer), peer)

    def show_missals(self) -> None:
        listing = self.query_one("#day-missal-list", OptionList)
        listing.clear_options()
        month = self.date.strftime("%Y-%m")
        for one in self.calendars:
            rows = self.months.get((one["id"], month)) or {"days": []}
            row = next((day for day in rows["days"] if day["date"] == self.date.isoformat()), None)
            ink = Ink()
            ink("● " if one["id"] == self.calendar else "  ", "bold $day-color")
            ink.line(one["short"], "bold")
            ink("  ")
            if not row or row.get("refused"):
                ink.line(((row or {}).get("refused") or "no day")[:32], "italic $warning")
            else:
                branches = row["branches"]
                if len(branches) > 1:
                    ink.line(f"⑂ {len(branches)} territorial branches", "$warning")
                elif branches and branches[0]["choiceRequired"]:
                    ink.line("⑂ a choice of Mass", "$warning")
                elif branches and branches[0]["settled"] is False:
                    ink.line("? not settled here", "$warning")
                elif branches and branches[0]["winner"]:
                    winner = branches[0]["winner"]
                    name = winner["name"] if len(winner["name"]) <= 30 else winner["name"][:29] + "…"
                    ink(rank_glyph(winner) + " ", "bold").line(name)
                else:
                    ink.line("no Mass held", "$text-muted")
                ink("  ")(season_name(row.get("season")), tone(row.get("season")))
                if row.get("week"):
                    ink(f", week {row['week']}", "$text-muted")
                if branches and branches[0].get("winner") and len(branches) == 1:
                    ink(f" · {rank_words(branches[0]['winner'])}", "$text-muted")
            listing.add_option(Option(ink.content(), id=f"cal-{one['id']}"))
        box = self.query_one("#day-missals", Panel)
        box.border_subtitle = "c next · enter read"
        calendar_box = self.query_one("#day-calendar", Panel)
        calendar_box.retitle(self.date.strftime("%A %-d %B %Y"))
        calendar_box.border_subtitle = "computed, not celebrated"

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
            ink.line(f"Lectionary: Sunday {lectionary.get('sunday') or '—'}, weekday {lectionary.get('weekday') or '—'}",
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
        box.retitle("why · " + next((one["short"] for one in self.calendars if one["id"] == view["calendar"]),
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
        box.retitle(f"{view['title']} · {edition}")
        mode = "missal" if state.get("ordinary") else "read"
        language = "English" if state.get("orations") == "en" else "Latin"
        chosen = [f"{name} {state[name]}" for name in ("mass", "form", "witness") if state.get(name)]
        box.border_subtitle = " · ".join([mode, f"{language} orations", view["bible"]["label"], *chosen])

        # The page's header: the long date, then its metadata line (day-reader.js:1683-1696).
        ink.line(view.get("longDate") or view["date"], "bold")
        branch = (f"{len(rows)} source-defined territorial results" if view.get("multiple")
                  else (rows[0].get("option") if rows and rows[0].get("option") else "Universal"))
        meta = [edition, branch, view["bible"]["label"], f"{language} orations"]
        if state.get("ordinary"):
            meta.append(f"{language} Ordinary")
        ink(" · ".join(meta), "$text-muted")
        ink(f"  ·  {season_name(view['day'].get('season'))}", tone(view["day"].get("season"))).line()
        if view.get("multiple"):
            ink.line("All held territorial branches are shown; no locality is inferred.", "italic $text-muted")
            territorial = (self.opening.get("territorial") or {}).get(calendar)
            if territorial:
                ink.line(territorial, "italic $text-muted")
        # The page's notices (day-reader.js:1711-1716): coverage, then any oration owner left open.
        for row in rows:
            if row.get("notice"):
                ink.line(row["notice"], "italic $text-muted")
            for unsettled in row.get("unsettled") or []:
                ink.line(unsettled, "italic $warning")
        for row in rows:
            ink.line()
            heading = row.get("heading")
            if heading:
                ink.line(heading["label"], "bold $day-color")
                ink.line(heading["title"], "bold")
            if row.get("failed"):
                ink.line(row["failed"], "italic $warning")
                continue
            resolved = row.get("resolved") or {}
            if row.get("mass") and not row.get("heading"):
                ink("Formulary: ", "$text-muted").line(row["mass"]["name"], "bold")
            if resolved.get("standing") and resolved["standing"] != "said":
                ink.line(f"Standing: {resolved['standing']}", "bold $warning")
            context = {**row, "day": {"branches": [row.get("branch") or {}]}, "ordinary": view.get("ordinary")}
            missal.choices(ink, context)
            for unresolved in row.get("ordinaryUnresolved") or []:
                said = unresolved if isinstance(unresolved, str) else (
                    unresolved.get("reason") or unresolved.get("id") or str(unresolved))
                ink.line(f"Ordinary unresolved: {said}", "italic $warning")
            missal.events(ink, context, rubrics=self.rubrics, accent="$day-color")
        # The Ordinary's own advisory, at the foot (day.js:1609-1612).
        if state.get("ordinary") and (view.get("ordinary") or {}).get("advisory"):
            ink.line().line(view["ordinary"]["advisory"], "italic $text-muted")
        text.update(ink.content())
        box.scroll_home(animate=False)
