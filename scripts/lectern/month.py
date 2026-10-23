"""A civil month, drawn as a grid; the surface supplies what each date carries."""
from __future__ import annotations

import calendar
import datetime as dt
from typing import Callable

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
    """Seven columns, Monday first; the chosen date is reversed, today underlined."""

    DEFAULT_CSS = """
    Month { height: auto; width: 100%; }
    """
    chosen: reactive[dt.date] = reactive(dt.date.today)

    class Chosen(Message):
        def __init__(self, date: dt.date) -> None:
            super().__init__()
            self.date = date

    def __init__(self, *, mark: Mark | None = None, today: dt.date | None = None, **options) -> None:
        super().__init__(**options)
        self.mark = mark
        self.today = today or dt.date.today()

    def watch_chosen(self) -> None:
        self.refresh()

    def render(self):
        day = self.chosen
        weeks = month_weeks(day)
        cell = self._cell()
        out = Ink()
        out.line(day.strftime("%B %Y").center(cell * 7).rstrip(), "bold")
        for name in ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"):
            out(name.rjust(cell), "bold $accent" if name == "Su" else "bold $text-muted")
        out.line()
        for week in weeks:
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
                if date == day:
                    style = (style + " reverse bold").strip()
                # The mark touches the day it marks: "•2", never "• 2" between two days.
                mark = glyph.strip()
                out(" " * (cell - len(mark) - len(str(date.day))))
                if mark:
                    out(mark, (tone + " bold").strip() if date != day else style)
                out(str(date.day), style)
            out.line()
        return out.content()

    def get_content_height(self, container, viewport, width: int) -> int:
        day = self.chosen
        return 2 + len(month_weeks(day))

    def _cell(self) -> int:
        return max(3, min(5, max(21, self.size.width) // 7))

    def on_click(self, event) -> None:
        offset = event.get_content_offset(self)
        if offset is None:
            return
        day = self.chosen
        weeks = month_weeks(day)
        cell = self._cell()
        row, column = offset.y - 2, offset.x // cell
        if 0 <= row < len(weeks) and 0 <= column < 7:
            date = weeks[row][column]
            if date is not None:
                self.post_message(self.Chosen(date))
