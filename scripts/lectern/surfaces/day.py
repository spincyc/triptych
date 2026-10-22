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
from ..widgets import Ink, Panel, ScrollPanel

ADAPTER = "liturgy"

def tone(season: str | None) -> str:
    """The theme's hue for a season (theme.SEASON_TONES), or none."""
    return f"$season-{season}" if season in SEASON_TONES else ""


# Rank, as the derivation reports it: a class where the code has classes, a
# nature where it does not. The glyph says it without colour.
FIRST = {"solemnity", "solemnity-or-sunday", "triduum", "sacred-triduum"}
SECOND = {"feast"}
THIRD = {"memorial", "office", "vigil", "day-within-an-octave", "vigil-or-octave-day", "commemoration-of-the-dead"}


def rank_glyph(winner: dict | None) -> str:
    if not winner:
        return " "
    level = winner.get("class")
    nature = winner.get("nature") or ""
    if level == "I" or (not level and nature in FIRST):
        return "◆"
    if level == "II" or (not level and nature in SECOND):
        return "◇"
    if level == "III" or (not level and nature in THIRD):
        return "•"
    if not level and nature == "sunday":
        return "○"
    return " "


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
    HELP = (
        ("← / →", "previous / next day"),
        ("[ / ]", "previous / next week"),
        ("{ / }", "previous / next month"),
        ("t", "today"),
        ("g", "go to a date (YYYY-MM-DD)"),
        ("c", "next missal (postconciliar, 1962, pre-1955)"),
        ("v", "compare: this missal beside the next, on the same date"),
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
        Binding("c", "calendar", "missal"),
        Binding("v", "compare", "compare"),
        Binding("m", "missal", "missal mode"),
        Binding("o", "orations", "en/la"),
        Binding("b", "bible", "bible", show=False),
        Binding("w", "witness", "witness", show=False),
        Binding("s", "choose", "choose"),
        Binding("r", "rubrics", "rubrics", show=False),
        Binding("p", "propers", "propers", show=False),
    ]
    CSS = """
    .day.focus #day-left { display: none; }
    .day.narrow #day-left { width: 30; }
    .day.narrow #day-legend { display: none; }
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
        self.orations = "en"
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
        if not self.bible:
            self.bible = self.bibles[0]["id"]
        legend = Ink()
        legend("◆", "bold")(" I ")("◇", "bold")(" II ")("•", "bold")(" III ")("○", "bold")(" Sun ")
        legend("?", "bold $warning")(" open ")("⑂", "bold $warning").line(" choice")
        legend.line("class, else rank · hue = season only", "italic $text-muted")
        self.query_one("#day-legend", Static).update(legend.content())
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
        self.go(self.date + dt.timedelta(days=days))

    def action_month(self, step: int) -> None:
        month = self.date.month - 1 + step
        year = self.date.year + month // 12
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
                self.app.notify(f"Not a date: {value!r}. Write it YYYY-MM-DD.", severity="warning")

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
        view = self.views.get(self.calendar)
        mass = (view or {}).get("mass")
        if not mass:
            self.app.notify("No single formulary is being read on this date yet.", severity="warning")
            return
        self.app.action_surface("propers", calendar=self.calendar, mass=mass["key"])

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

    def action_choose(self) -> None:
        view = self.views.get(self.calendar)
        if not view:
            return
        offers = []
        for choice in view.get("unresolvedChoices") or []:
            ident = choice.get("id") or ""
            for option in choice.get("options") or []:
                offers.append(((ident, option["id"]), f"{missal.option_label(choice, option, view)}"
                                                      f"   ({choice.get('reason') or ident})"))
        for event in view.get("events") or []:
            if event.get("kind") == "proper-choice":
                for option in event.get("options") or []:
                    offers.append((("proper-choice", event["id"], option["id"]),
                                   f"{event.get('group')}  →  option {option['id']}"))
        if not offers:
            self.app.notify("Nothing on this date is left open for the reader to choose.")
            return

        def picked(value) -> None:
            if not value:
                return
            selection = self.selection()
            kind = value[0]
            if kind == "calendar-territory":
                selection.clear()
                selection["territory"] = value[1]
            elif kind == "calendar-formulary":
                territory = selection.get("territory")
                selection.clear()
                if territory:
                    selection["territory"] = territory
                selection["mass"] = value[1]
            elif kind.startswith("proper-form"):
                selection["form"] = value[1]
                mass = (view.get("mass") or {}).get("key") or self.resolved_key(view)
                if mass:
                    selection.setdefault("mass", mass)
            elif kind == "proper-choice":
                selection.setdefault("properChoices", {})[value[1]] = value[2]
            elif kind.startswith("translation-witness"):
                selection["witness"] = value[1]
            else:
                self.app.notify(f"This reader cannot make the choice {kind!r} yet.", severity="warning")
                return
            self.load()

        self.app.push_screen(Pick("choose", offers,
                                  "The rubrics or the sources leave this open. Nothing is chosen by order."), picked)

    @staticmethod
    def resolved_key(view: dict) -> str | None:
        resolved = view.get("resolved") or {}
        formulary = resolved.get("formulary")
        return formulary.get("id") if isinstance(formulary, dict) else formulary

    def action_witness(self) -> None:
        view = self.views.get(self.calendar) or {}
        witnesses = ((view.get("mass") or {}).get("witnesses")) or []
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
        return ids[(ids.index(self.calendar) + 1) % len(ids)] if len(ids) > 1 else self.calendar

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
            self.app.call_from_thread(self.fail, str(refusal))
            return
        self.app.call_from_thread(self.show, date, views)

    # --- drawing ---------------------------------------------------------

    def mark(self, date: dt.date) -> tuple[str, str] | None:
        rows = self.months.get((self.calendar, date.strftime("%Y-%m")))
        if not rows:
            return None
        row = next((one for one in rows["days"] if one["date"] == date.isoformat()), None)
        if not row or row.get("refused"):
            return None
        hue = tone(row.get("season"))
        branches = row.get("branches") or []
        if len(branches) > 1 or any(branch.get("choiceRequired") for branch in branches):
            return "⑂", hue
        if branches and branches[0].get("settled") is False:
            return "?", hue
        return rank_glyph(branches[0].get("winner") if branches else None), hue

    def where(self) -> str:
        view = self.views.get(self.calendar) or {}
        mass = view.get("mass") or {}
        edition = next((one["short"] for one in self.calendars if one["id"] == self.calendar), self.calendar)
        title = mass.get("name") or "—"
        return f"{self.date.strftime('%a %d %b %Y')} · {edition} · {title}"

    def show(self, date: dt.date, views: dict[str, dict]) -> None:
        if date != self.date:
            return
        self.views = views
        self.query_one(Month).refresh()
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
        for branch in day["branches"]:
            ink.line()
            if branch.get("option"):
                ink.line(f"branch: {branch['option']}", "bold $day-color")
            if branch.get("settled") is False:
                ink.line("This date is not settled here:", "bold $warning")
                for row in branch.get("unsettled") or []:
                    ink("  ")(f"{row['what']}: ", "bold").line(row["why"])
            winner = branch.get("winner")
            if winner:
                ink(rank_glyph(winner) + " ", "bold")(winner["name"], "bold").line()
                ink.line(f"  {winner.get('rowLabel') or ''}", "$text-muted")
                if winner.get("why"):
                    ink.line(f"  {winner['why']}")
                if winner.get("locus"):
                    ink.line(f"  {winner['locus']}", "italic $day-color")
                formulary = winner.get("formulary")
                if formulary and formulary.get("kind") == "borrowed":
                    ink.line(f"  Mass borrowed: {formulary.get('name') or formulary.get('key')}", "italic")
            if branch.get("choice"):
                choice = branch["choice"]
                ink.line(f"⑂ {choice.get('what') or 'a choice'}", "bold $warning")
                if choice.get("locus"):
                    ink.line(f"  {choice['locus']}", "italic $day-color")
            for condition in branch.get("conditions") or []:
                said = condition if isinstance(condition, str) else (condition.get("what") or condition.get("id"))
                ink.line(f"only if: {said}", "italic $warning")
            readable = branch.get("readable") or []
            for standing in missal.STANDING_ORDER:
                group = [one for one in readable if one["state"] == standing]
                if not group:
                    continue
                ink.line()
                ink.line(missal.STANDING_GROUPS[standing], "bold underline")
                for one in group:
                    ink(f"{missal.STANDING_MARK[standing]} ", "bold")(one["label"]).line()
                    if one.get("why") and standing != "said":
                        ink.line(f"    {one['why']}", "$text-muted")
                    if one.get("locus") and standing != "said":
                        ink.line(f"    {one['locus']}", "italic $day-color")
            orations = (branch.get("orations") or {}).get("low_mass") or []
            if orations:
                ink.line()
                ink.line("Orations at Low Mass", "bold underline")
                for row in orations:
                    ink(f"{row.get('position')}. ", "bold")(row.get("label") or "")
                    ink(f" — {row.get('of_name') or row.get('of')}").line()
                    ink.line(f"    {row.get('kind') or ''} · {row.get('locus') or ''}", "$text-muted")
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
        mass = view.get("mass") or {}
        state = view.get("state") or {}
        day = view.get("day") or {}
        resolved = view.get("resolved") or {}
        standing = resolved.get("standing")
        title = mass.get("name") or "No single Mass is read here yet"
        box.retitle(f"{title} · {edition}")
        mode = "missal" if state.get("ordinary") else "read"
        language = "English" if state.get("orations") == "en" else "Latin"
        chosen = [f"{name} {state[name]}" for name in ("territory", "form", "witness") if state.get(name)]
        if state.get("mass") and standing != "said":
            chosen.insert(0, "chosen Mass")
        box.border_subtitle = " · ".join([mode, f"{language} orations", view["bible"]["label"], *chosen])

        ink(dt.date.fromisoformat(view["date"]).strftime("%A %-d %B %Y"), "bold")
        ink(f"  ·  {season_name(day.get('season'))}", tone(day.get("season"))).line()
        if mass.get("rank"):
            ink.line(f"{mass['rank']}", "$text-muted")
        if standing and standing != "said":
            ink.line(f"{missal.STANDING_MARK.get(standing, '')} {missal.STANDING_GROUPS.get(standing, standing)}",
                     "bold $warning")
        for branch in day.get("branches") or []:
            if branch.get("settled") is False:
                ink.line("This date is not settled here; no Mass is presented as the day's.", "bold $warning")
                break
        ink.line()
        missal.choices(ink, view, (self.opening.get("territorial") or {}).get(calendar))
        if mass.get("recension"):
            ink.line(str(mass["recension"]), "italic $warning")
        if mass.get("coverage"):
            ink.line(mass["coverage"], "italic $text-muted")
        if state.get("ordinary") and view.get("ordinary"):
            ordinary = view["ordinary"]
            if ordinary.get("advisory"):
                ink.line(ordinary["advisory"], "italic $text-muted")
        for row in view.get("ordinaryUnresolved") or []:
            said = row if isinstance(row, str) else (row.get("reason") or row.get("id") or str(row))
            ink.line(f"Ordinary unresolved: {said}", "italic $warning")
        missal.events(ink, view, rubrics=self.rubrics, accent="$day-color")
        if not view.get("events") and not view.get("unresolvedChoices"):
            for absence in view.get("explicitAbsences") or []:
                reason = absence.get("reason") or ""
                if " " in reason:
                    ink.line(reason, "italic $warning")
        text.update(ink.content())
        box.scroll_home(animate=False)
