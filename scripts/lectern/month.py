"""A civil month, drawn as a grid; the surface supplies what each date carries."""
from __future__ import annotations

import calendar
import datetime as dt
from typing import Callable

from textual.binding import Binding
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget

from .widgets import Ink

Mark = Callable[[dt.date], tuple[str, str] | None]


def month_weeks(day: dt.date) -> list[list[dt.date | None]]:
    """The month's weeks, Monday first, None where a week runs outside it. Built
    from day numbers, so no date beyond the calendar's own range is made."""
    return [[dt.date(day.year, day.month, number) if number else None for number in week]
            for week in calendar.Calendar(firstweekday=0).monthdayscalendar(day.year, day.month)]


class Month(Widget, can_focus=True):
    """Seven columns, Monday first; the chosen date is reversed, today underlined.

    When focused, arrow keys move a lightweight cursor across the month (posting
    `Highlighted` for a 1-line feast preview) and Enter selects that date.
    """

    DEFAULT_CSS = """
    Month { height: auto; width: 100%; }
    """
    BINDINGS = [
        Binding("left", "move(-1)", "previous day", show=False),
        Binding("right", "move(1)", "next day", show=False),
        Binding("up", "move(-7)", "previous week", show=False),
        Binding("down", "move(7)", "next week", show=False),
        Binding("enter", "select_cursor", "read date", show=False),
    ]
    chosen: reactive[dt.date] = reactive(dt.date.today)
    cursor: reactive[dt.date] = reactive(dt.date.today)

    class Chosen(Message):
        def __init__(self, date: dt.date) -> None:
            super().__init__()
            self.date = date

    class Highlighted(Message):
        def __init__(self, date: dt.date) -> None:
            super().__init__()
            self.date = date

    def __init__(self, *, mark: Mark | None = None, today: dt.date | None = None, **options) -> None:
        super().__init__(**options)
        self.mark = mark
        self.today = today or dt.date.today()

    def watch_chosen(self, new: dt.date) -> None:
        self.cursor = new
        self.refresh()

    def watch_cursor(self) -> None:
        self.refresh()

    def on_focus(self) -> None:
        self.cursor = self.chosen
        self.post_message(self.Highlighted(self.cursor))
        self.refresh()

    def on_blur(self) -> None:
        self.cursor = self.chosen
        self.post_message(self.Highlighted(self.chosen))
        self.refresh()

    def action_move(self, days: int) -> None:
        try:
            target = self.cursor + dt.timedelta(days=days)
        except OverflowError:
            return
        if target.year != self.chosen.year or target.month != self.chosen.month:
            # Crossing a month boundary loads that date directly so the grid follows.
            self.post_message(self.Chosen(target))
            return
        self.cursor = target
        self.post_message(self.Highlighted(target))

    def action_select_cursor(self) -> None:
        self.post_message(self.Chosen(self.cursor))

    def _left_pad(self, cell: int) -> int:
        if self.size.width <= 0:
            return 0
        return max(0, (self.size.width - cell * 7) // 2)

    def render(self):
        day = self.chosen
        weeks = month_weeks(day)
        cell = self._cell()
        pad = " " * self._left_pad(cell)
        out = Ink()
        out(pad)
        for name in ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"):
            out(name.rjust(cell), "bold $accent" if name == "Su" else "bold $text-muted")
        out.line()
        for week in weeks:
            out(pad)
            for date in week:
                if date is None:
                    out(" " * cell, "")
                    continue
                glyph, tone = " ", ""
                marked = self.mark(date) if self.mark else None
                if marked:
                    glyph, tone = marked
                style = tone
                if date.weekday() == 6:
                    style = (style + " bold").strip()
                if date == self.today:
                    style = (style + " underline").strip()
                is_cursor = self.has_focus and date == self.cursor and date != day
                if date == day:
                    style = (style + " reverse bold").strip()
                elif is_cursor:
                    style = "reverse bold $accent"
                # The mark touches the day it marks: "•2", never "• 2" between two days.
                mark = glyph.strip()
                out(" " * (cell - len(mark) - len(str(date.day))))
                if mark:
                    out(mark, (tone + " bold").strip() if date != day and not is_cursor else style)
                out(str(date.day), style)
            out.line()
        return out.content()

    def get_content_height(self, container, viewport, width: int) -> int:
        day = self.chosen
        return 1 + len(month_weeks(day))

    def _cell(self) -> int:
        return max(3, min(4, max(21, self.size.width) // 7))

    def on_click(self, event) -> None:
        offset = event.get_content_offset(self)
        if offset is None:
            return
        day = self.chosen
        weeks = month_weeks(day)
        cell = self._cell()
        pad = self._left_pad(cell)
        x = offset.x - pad
        row = offset.y - 1
        column = x // cell if x >= 0 else -1
        if 0 <= row < len(weeks) and 0 <= column < 7:
            date = weeks[row][column]
            if date is not None:
                self.post_message(self.Chosen(date))
