"""Render the reader headlessly, once settled, as text or SVG.

This is how the reader is checked without a terminal: the same app, the same
data, driven at a fixed size, with the screen read back exactly as it would be
drawn.
"""
from __future__ import annotations

import asyncio
import datetime as dt
import io

from rich.console import Console

from . import bridge
from .app import TriptychApp

# The drawing's own glyphs, each mark that carries a meaning given its own
# ASCII stand-in so a plain-tier snapshot keeps every distinction its legends
# draw; lines keep their weights. Prose characters are left to the
# repository's fold (scripts/_tooling.py FOLD), which the plain tier applies
# after this. tools/tests/test_lectern.py holds each legend's marks apart.
DRAWING = str.maketrans({
    **{one: "-" for one in "─╴╶"}, "━": "=", "═": "=", **{one: "~" for one in "╌╍"}, **{one: "." for one in "┄┅┈┉"},
    **{one: "|" for one in "│║▏▕▎▍▌▊▉"}, "┃": "!", **{one: ":" for one in "╎╏┆┇┊┋"}, "⋮": ";",
    **{one: "+" for one in "╭╮╯╰┌┐└┘┏┓┗┛├┤┬┴┼┣┫┳┻╋╔╗╚╝╠╣╦╩╬"},
    **{one: "_" for one in "▁▂▃"}, **{one: "=" for one in "▄▅"}, **{one: "#" for one in "▆▇█"},
    "▔": "-", "■": "#",
    "◆": "#", "◇": "+", "•": ".", "○": "O", "●": "*", "◌": "o", "◉": "@", "◈": "%",
    "◐": "(", "◑": ")", "✕": "x", "×": "x", "⊘": "X", "⑂": "Y",
    "▶": ">", "▷": "}", "▸": ">", "▾": "v", "▼": "v", "▲": "^", "◁": "<", "▷": "}",
    "←": "<", "→": ">", "↔": "<>", "↳": "L", "⤷": "\\", "☐": "[ ]", "☑": "[x]",
    "⠋": "-", "⠙": "\\", "⠹": "|", "⠸": "/", "⠼": "-", "⠴": "\\", "⠦": "|", "⠧": "/", "⠇": "-", "⠏": "|",
    **{chr(code): str(digit) for code, digit in zip((0x2070, 0xB9, 0xB2, 0xB3, 0x2074, 0x2075, 0x2076,
                                                      0x2077, 0x2078, 0x2079), range(10))},
})

# What each legend asks a reader to tell apart, for the test that keeps them so.
LEGENDS = {
    "day": "◆◇•○?⑂×",
    "catena": "◌●▸▾┃╏",
    "law": "┃⊘◌",
    "history timeline": "●◇━─╌┄▶▼▲",
    "history map": "●○◉┃│┆⋮",
    "sources": "☐☑▸⤷",
    "propers choice": "▶▷",
}


async def _settle(app: TriptychApp, pilot, rounds: int = 400) -> None:
    """Wait until no worker is running and nothing is left to lay out."""
    quiet = 0
    for _ in range(rounds):
        await pilot.pause(0.05)
        # A superseded worker is finished in name while its thread may still be
        # in a bridge call; wait for the bridge too.
        busy = any(not worker.is_finished for worker in app.workers) or bridge.BRIDGE_PROCESS.waiting
        quiet = 0 if busy else quiet + 1
        if quiet >= 3:
            return
    raise TimeoutError(f"snapshot did not settle within {rounds} polling rounds "
                       "(50 ms pauses); no snapshot was captured")


def _text(app: TriptychApp, *, styles: bool) -> str:
    width, height = app.size
    console = Console(
        width=width,
        height=height,
        file=io.StringIO(),
        force_terminal=True,
        color_system="truecolor",
        record=True,
        legacy_windows=False,
        safe_box=False,
    )
    console.print(app.screen._compositor.render_update(full=True, screen_stack=app._background_screens))
    return console.export_text(styles=styles)


async def capture(*, surface: str, intent: dict, size: tuple[int, int], keys: list[str],
                  form: str, theme: str, plain: bool = False) -> str:
    # A snapshot's "today" is its own date, or a fixed one: never the clock's.
    today = dt.date.fromisoformat(intent["date"]) if intent.get("date") else dt.date(2026, 1, 1)
    app = TriptychApp(start=surface, intent=intent, theme=theme, today=today)
    async with app.run_test(size=size) as pilot:
        try:
            await _settle(app, pilot)
            for key in keys:
                await pilot.press(key)
                await _settle(app, pilot)
        except TimeoutError:
            # Cancel delivery first; the bridge owner then wakes active reads
            # and reaps their child before this context exits with our timeout.
            app.workers.cancel_all()
            bridge.BRIDGE_PROCESS.close()
            raise
        if form == "svg":
            return app.export_screenshot(title=f"triptych {surface}")
        text = _text(app, styles=form == "ansi" and not plain)
        if plain:
            text = text.translate(DRAWING)
        return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def render(**options) -> str:
    return asyncio.run(capture(**options))
