"""Palettes. Colour decorates; every distinction it draws is also drawn in words."""
from __future__ import annotations

from textual.theme import Theme

# One accent per surface, so a reader knows where they are by the frame alone.
SURFACE_ACCENTS = {
    "day": ("#c9a227", "#8a6d12"),
    "propers": ("#c0485c", "#8e2a3c"),
    "catena": ("#8b6fd6", "#5b43a3"),
    "scripture": ("#4fa36a", "#2e6e44"),
    "texts": ("#3fa3b0", "#22707a"),
    "sources": ("#c48a45", "#86592a"),
    "history": ("#5b8bd6", "#335ea3"),
    "law": ("#cf6a8f", "#94405f"),
}


# A hue per season, for a month to read at a glance. It marks the season the
# calendar layer computes and nothing else: no liturgical colour is recorded in
# the published data, and none is implied. Both calendars' vocabularies.
SEASON_TONES = {
    "advent": ("#8b7fd6", "#5a4bb0"),
    "christmas": ("#d9b44a", "#8a6a00"), "christmastide": ("#d9b44a", "#8a6a00"),
    "epiphanytide": ("#7fb8a4", "#2f7a62"),
    "ordinary-time": ("#6fae7f", "#2e7040"), "after-pentecost": ("#6fae7f", "#2e7040"),
    "septuagesima": ("#a58fc9", "#6a4f96"),
    "lent": ("#9f78d0", "#6b3fa3"), "passiontide": ("#c2789a", "#934065"), "holy-week": ("#c2789a", "#934065"),
    "triduum": ("#d86a6a", "#a32929"),
    "easter": ("#e6d9a0", "#8a7a20"), "paschaltide": ("#e6d9a0", "#8a7a20"),
}


def _variables(dark: bool) -> dict[str, str]:
    index = 0 if dark else 1
    found = {f"{name}-color": pair[index] for name, pair in SURFACE_ACCENTS.items()}
    found.update({f"season-{name}": pair[index] for name, pair in SEASON_TONES.items()})
    found["hotkey"] = "#ff5f6d" if dark else "#b3122e"
    found["muted"] = "#99958a" if dark else "#706658"
    found["rubric"] = "#e05252" if dark else "#a3141c"
    found["meter-empty"] = "#2a2d36" if dark else "#ddd5c4"
    found["rule"] = "#30333d" if dark else "#cfc6b4"
    found["footer-key-foreground"] = found["hotkey"]
    return found


THEMES = (
    Theme(
        name="triptych",
        primary="#c9a227",
        secondary="#8b6fd6",
        accent="#ff5f6d",
        warning="#e3a33b",
        error="#e05252",
        success="#5fb878",
        foreground="#ddd8cc",
        background="#0c0d11",
        surface="#12141a",
        panel="#1a1d25",
        dark=True,
        variables=_variables(True),
    ),
    Theme(
        name="triptych-vellum",
        primary="#8a6d12",
        secondary="#5b43a3",
        accent="#b3122e",
        warning="#9a5b00",
        error="#a3141c",
        success="#2e6e44",
        foreground="#2a251e",
        background="#f3eee2",
        surface="#ebe4d4",
        panel="#e2d9c5",
        dark=False,
        variables=_variables(False),
    ),
    Theme(
        name="triptych-compline",
        primary="#a9a9b8",
        secondary="#7c7c96",
        accent="#e8e8f0",
        warning="#c8b070",
        error="#d07070",
        success="#90b090",
        foreground="#c8c8d4",
        background="#000000",
        surface="#08080c",
        panel="#101018",
        dark=True,
        variables={
            **_variables(True),
            **{f"{name}-color": "#5a5a70" for name in SURFACE_ACCENTS},
            "hotkey": "#ffffff",
        },
    ),
)

# A gradient for meters, as btop draws them: cool where little is held,
# warm where much is. It is never the only statement of a count.
METER_STOPS = ("#4a6fa5", "#5fa39a", "#8fbf5a", "#d9b64a", "#e07b3c")


def blend(stops: tuple[str, ...], fraction: float) -> str:
    """The colour `fraction` of the way along `stops`."""
    fraction = min(1.0, max(0.0, fraction))
    if len(stops) == 1:
        return stops[0]
    scaled = fraction * (len(stops) - 1)
    low = int(scaled)
    if low >= len(stops) - 1:
        return stops[-1]
    part = scaled - low
    a, b = stops[low], stops[low + 1]
    channels = []
    for offset in (1, 3, 5):
        x = int(a[offset : offset + 2], 16)
        y = int(b[offset : offset + 2], 16)
        channels.append(round(x + (y - x) * part))
    return "#" + "".join(f"{value:02x}" for value in channels)
