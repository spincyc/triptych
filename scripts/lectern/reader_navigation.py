"""Presentation positions over the reader owner's stable semantic event IDs."""
from __future__ import annotations

from bisect import bisect_right
from functools import lru_cache
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader

from textual import work
from textual.widgets import Static

from . import bridge
from .dialogs import JanuaryReading, MissalSource, Pick, Reading
from .missal import event_source_readings, memorial_sources, witness_label, witness_readings
from .repo import ROOT, Refused
from .surface import Surface, shown
from .widgets import Ink


@lru_cache(maxsize=1)
def _site_url():
    """Use the publisher's URL owner, including its single declared origin."""
    loader = SourceFileLoader("_lectern_public_urls", str(ROOT / "tools" / "public-alpha"))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    loader.exec_module(module)
    return module.public_site_url


def share(surface, route: str) -> None:
    url = _site_url()(route)
    surface.app.copy_to_clipboard(url)
    ink = Ink().line("The canonical reader URL has been copied to the terminal clipboard.", "italic")
    ink.line().line(url)
    surface.app.push_screen(Reading("Share this reading", ink.content(), walks=False))


class MissalSurface(Surface):
    """The shared reading, navigation and settings controls of Day and Propers."""

    READING = ""
    BROWSE = ""

    def reading_panel(self):
        selector = "#day-compare" if getattr(self, "comparing", False) else self.READING
        return self.query_one(selector)

    def show_reading_pane(self) -> None:
        self.remove_class("navigation")
        self.add_class("focus")
        self.call_after_refresh(self.focus_reading_panel)

    def focus_reading_panel(self) -> None:
        panel = self.reading_panel()
        if shown(panel) and self.app.screen is self.screen:
            panel.focus(scroll_visible=False)

    def action_focus_reading(self) -> None:
        browsing = self.has_class("navigation") if self.has_class("compact") else not self.has_class("focus")
        if browsing:
            self.show_reading_pane()
        else:
            self.remove_class("focus")
            self.add_class("navigation")
            self.call_after_refresh(self.query_one(self.BROWSE).focus)

    def source_rows(self) -> list[dict]:
        raise NotImplementedError

    def action_rite_source(self) -> None:
        choices = [(name, link) for row in self.source_rows() for name, link in witness_readings(row)
                   if link.get("rite_opening")]
        self.show_source_choices("Complete rite in facsimile", choices)

    def action_missal_source(self) -> None:
        choices = []
        for row in self.source_rows():
            for name, link in witness_readings(row):
                title = f"{row['option']} · {name}" if row.get("option") else name
                choices.append((title, link))

        self.show_source_choices("Source texts", choices)

    def show_source_choices(self, heading: str, choices: list[tuple[str, dict]]) -> None:
        def display(index) -> None:
            if index is not None:
                title, link = choices[index]
                self.app.push_screen(MissalSource(title, link))

        if len(choices) == 1:
            display(0)
        elif choices:
            options = [(index, f"{name} · {witness_label(link)} · {link['locus']}")
                       for index, (name, link) in enumerate(choices)]
            self.app.push_screen(Pick(heading, options), display)

    def action_prayer_source(self) -> None:
        rows = self.source_rows()
        current = None
        if not getattr(self, "comparing", False) and self.navigation.entries:
            panel = self.reading_panel()
            current = self.navigation.current(panel, panel.query_one(Static))
        choices = []
        passage = False
        for row in rows:
            prefix = row.get("prefix") or ""
            if current and prefix and not current.startswith(prefix):
                continue
            event = next((e for e in row.get("events") or [] if prefix + e["id"] == current), {})
            exact = list(event_source_readings(event))
            if exact:
                passage = True
                choices.extend(exact)
                if any(link["language"] == "en" for _, link in exact):
                    continue
            if event.get("kind") == "january-prayer" and row.get("januarySelection"):
                selected = row["januarySelection"]
                self.show_january_prayers(row["mass"]["key"], selected["weekday"], selected["phase"], event["slot"])
                return
            if event.get("kind") == "ordinary-element":
                choices.extend(((event.get("element") or {}).get("name") or "Ordinary", link)
                               for link in event.get("sourceLinks") or [] if link["language"] == "en")
                continue
            mass = row.get("mass") or {}
            owner = row.get("orationSelection") or {}
            sources = [(mass, row.get("missalWitnessLinks") or [])]
            if owner:
                sources.append(({"key": owner["owner"], "name": owner["label"]}, row.get("orationWitnessLinks") or []))
            roles = {event.get("slot")}
            selected = (event.get("selection") or {}).get("option")
            roles.update(member.get("slot") for option in event.get("options") or []
                         if not selected or option["id"] == selected for member in option.get("members") or [])
            proper = event.get("kind") in ("proper", "proper-choice")
            for source, links in sources:
                if proper and event["id"].split("/")[2] != source.get("key"):
                    continue
                for link in links:
                    if link["language"] != "en":
                        continue
                    for role in link.get("prayer_roles") or []:
                        if not proper or role in roles:
                            title = " · ".join(filter(None, (row.get("option"), source.get("name"), role)))
                            choices.append((title, link))
        if choices:
            self.show_source_choices("Passage source" if passage else "English missal prayers", choices)
        else:
            self.app.notify("No English missal source is identified for this passage.")

    def january_rows(self):
        return [row for row in self.source_rows() if not row.get("primaryDayChoice") and
                (row.get("januarySelection") or self.surface_id() == "propers" and
                 (row.get("mass") or {}).get("januaryWeekdays"))]

    def action_january_prayers(self) -> None:
        rows = self.january_rows()

        def select(row) -> None:
            mass = row["mass"]
            selected = row.get("januarySelection")
            if selected:
                self.show_january_prayers(mass["key"], selected["weekday"], selected["phase"])
                return

            def weekday_chosen(weekday) -> None:
                if weekday is None:
                    return
                phases = [("before-epiphany", "Before Epiphany"), ("after-epiphany", "After Epiphany")]
                self.app.push_screen(Pick("January Collect", phases),
                                     lambda phase: self.show_january_prayers(mass["key"], weekday, phase) if phase else None)

            self.app.push_screen(Pick("January weekday", [(day["weekday"], day["label"]) for day in mass["januaryWeekdays"]],
                                      "The civil date and local Epiphany determine the appointed prayers."), weekday_chosen)
        if len(rows) == 1:
            select(rows[0])
        elif rows:
            self.app.push_screen(Pick("January prayer source", [(i, row["option"] or row["title"]) for i, row in enumerate(rows)]),
                                 lambda i: select(rows[i]) if i is not None else None)

    @work(thread=True, exclusive=True, group="january-prayers")
    def show_january_prayers(self, mass: str, weekday: int, phase: str, role: str | None = None) -> None:
        try:
            source = bridge.call("liturgy", "januaryPrayerReading", self.calendar, mass, weekday, phase,
                                 {"orations": self.orations, "textDisplay": self.text_display})
        except Refused as error:
            self.deliver(self.app.notify, str(error), severity="warning")
            return
        self.deliver(self.app.push_screen, JanuaryReading(source, role))

    def memorial_prayer(self, role: str) -> None:
        rows = [row for row in self.source_rows() if role in memorial_sources(row).get("roles", [])]

        def choose_source(row) -> None:
            sources = memorial_sources(row)
            groups = sources["groups"]
            options = [(group["id"], group["label"] + (" · see qualification" if group.get("qualification") else ""))
                       for group in groups]
            if sources.get("current_feria"):
                options.append(("current-feria", "Current feria"))

            def source_chosen(identifier) -> None:
                if identifier is None:
                    return
                if identifier == "current-feria":
                    feria = row.get("memorialFeria") or {}
                    if feria.get("january"):
                        selection = feria["january"]
                        self.show_january_prayers(feria["mass"], selection["weekday"], selection["phase"], role)
                    elif role in feria.get("roles", []):
                        self.open_prayer_source(feria["mass"], role)
                    elif feria.get("owners"):
                        options = [(owner["id"], owner["label"]) for owner in feria["owners"]]
                        self.app.push_screen(Pick(role, options, feria["name"]),
                                             lambda owner: self.open_prayer_source(owner, role) if owner else None)
                    else:
                        ink = Ink().line(role, "bold")
                        if feria:
                            ink.line(feria["name"]).line(
                                "This feria does not print this prayer. A separate, eligible prayer formulary must be identified.")
                        else:
                            ink.line("The current feria is an available source. This reading supplies no dated ferial formulary.")
                        ink.line().line(sources["locus"]).line(sources["source_id"]).line(sources["url"])
                        self.app.push_screen(Reading("Current feria", ink.content(), walks=False))
                    return
                group = next(one for one in groups if one["id"] == identifier)

                self.open_memorial_group(row["mass"]["key"], role, group)

            self.app.push_screen(Pick(role, options, "Open a source in Propers. The memorial keeps its own Collect."), source_chosen)

        if len(rows) == 1:
            choose_source(rows[0])
        elif rows:
            self.app.push_screen(Pick(role, [(i, row["title"]) for i, row in enumerate(rows)]),
                                 lambda i: choose_source(rows[i]) if i is not None else None)

    def open_prayer_source(self, mass: str, role: str, form: str | None = None) -> None:
        self.app.action_surface("propers", calendar=self.calendar, mass=mass, form=form,
                                prayerRole=role, ordinary=False, replace=True, bible=self.bible,
                                orations=self.orations, textDisplay=self.text_display, companion=self.companion)

    @work(thread=True, exclusive=True, group="memorial-source")
    def open_memorial_group(self, memorial: str, role: str, group: dict) -> None:
        try:
            forms = bridge.call("liturgy", "memorialPrayerForms", self.calendar, memorial, role, group["id"])
        except Refused as error:
            self.deliver(self.app.notify, str(error), severity="warning")
            return

        def open_form(form) -> None:
            if form is not None:
                self.open_prayer_source(group["mass"], role, form)

        if len(forms) == 1 and not group.get("qualification"):
            self.deliver(open_form, forms[0]["id"])
        else:
            options = [(form["id"], form["name"]) for form in forms]
            self.deliver(self.app.push_screen, Pick(group["label"], options, group.get("qualification") or role), open_form)

    def action_votive_chants(self) -> None:
        rows = [(row["key"], chant) for row in self.source_rows() for chant in row.get("votiveChants", [])]
        self.app.push_screen(Pick("Seasonal and votive chants", [((key, item["id"]), item["label"]) for key, item in rows],
                                  "Choose the printed off-date provision."), self.open_votive_chant)

    @work(thread=True, exclusive=True, group="votive-chant")
    def open_votive_chant(self, choice) -> None:
        if not choice:
            return
        try:
            result = bridge.call("liturgy", "votiveChant", self.calendar, *choice, {
                "orations": self.orations, "bible": self.bible, "companion": self.companion,
                "textDisplay": self.text_display})
            chant = result["chant"]
            self.app.call_from_thread(self.app.push_screen, MissalSource(
                chant["label"], chant["source"], result["blocks"], chant.get("common")))
        except Refused as error:
            self.app.call_from_thread(self.app.notify, str(error), severity="error")

    def action_settings(self) -> None:
        edition = next((one["short"] for one in self.calendars if one["id"] == self.calendar), self.calendar)
        bible = next((one["label"] for one in self.bibles if one["id"] == self.bible), self.bible)
        options = [("calendar", f"Missal   {edition}"), ("missal", "Mode   " + ("Missal" if self.ordinary else "Read")),
                   ("choose", "Mass, form and source options")]
        sections = {0: "Celebration", len(options): "Prayers"}
        names = {"en": "English", "la": "Latin"}
        options.extend([("orations", "Oration language   " + names.get(self.orations, self.orations)),
                        ("bilingual", "Parallel Latin   " + ("on" if self.text_display == "latin-and-selected" else "off")),
                        ("witness", "Translation witness")])
        if self.ordinary:
            options.extend([("ordinary_language", "Ordinary language   " + names.get(self.ordinary_language, self.ordinary_language)),
                            ("rubrics", "Ordinary rubrics   " + ("shown" if self.rubrics else "hidden"))])
        if any(row.get("votiveChants") for row in self.source_rows()):
            options.append(("votive_chants", "Seasonal and votive chants"))
        if self.january_rows():
            options.append(("january_prayers", "January weekday prayers"))
        roles = dict.fromkeys(role for row in self.source_rows() for role in memorial_sources(row).get("roles", []))
        options.extend(("memorial/" + role, role + "   Sources") for role in roles)
        sections[len(options)] = "Scripture"
        options.extend([("bible", f"Bible   {bible}"), ("companion", "Latin companion   " + (self.companion or "none"))])

        if any(link for row in self.source_rows() for _, link in witness_readings(row)):
            sections[len(options)] = "Sources"
            if any(link.get("rite_opening") for row in self.source_rows() for _, link in witness_readings(row)):
                options.append(("rite_source", "Complete rite in facsimile"))
            if any(link.get("prayer_roles") for row in self.source_rows() for _, link in witness_readings(row)):
                options.append(("prayer_source", "English missal prayers   Ctrl+O"))
            options.append(("missal_source", "Read source texts"))

        def picked(action) -> None:
            if action in ("calendar", "bible"):
                rows = self.calendars if action == "calendar" else self.bibles
                choices = [(one["id"], one["short"] if action == "calendar" else one["label"]) for one in rows]
                def apply(value) -> None:
                    if value is None:
                        return
                    if action == "calendar":
                        self.follow(calendar=value, browse=self.surface_id() == "propers")
                    else:
                        self.bible = value
                        self.reload_reading()
                self.app.push_screen(Pick("Missal" if action == "calendar" else "Bible", choices), apply)
            elif action and action.startswith("memorial/"):
                self.memorial_prayer(action.removeprefix("memorial/"))
            elif action:
                getattr(self, "action_" + action)()

        self.app.push_screen(Pick("Reading settings", options, sections=sections), picked)


class ReadingNavigation:
    """A semantic Contents list whose scroll coordinates belong to Textual.

    Prefix heights are measured by the same Content formatter the Static uses;
    no translated heading, source order or liturgical seat is reconstructed.
    """

    def __init__(self) -> None:
        self.entries: list[tuple[str, str, int]] = []
        self.ink: Ink | None = None
        self.identity: tuple | None = None
        self.saved: tuple[str | None, float] | None = None
        self.pending: str | None = None
        self.focused: tuple[str, float] | None = None

    def _height(self, end: int, text) -> int:
        # Measure a prefix only when navigating. Storing a fully styled copy
        # at every event made opening a long Missal quadratic in its length.
        assert self.ink is not None
        prefix = self.ink.content(end)
        return max(0, prefix.get_height(text.styles, max(1, text.content_size.width)) - 1)

    def current(self, box, text) -> str | None:
        if self.focused and abs(self.focused[1] - box.scroll_y) < 0.5:
            return self.focused[0]
        self.focused = None
        index = bisect_right(self.entries, box.scroll_y, key=lambda entry: self._height(entry[2], text))
        return self.entries[index - 1][0] if index else None

    def begin(self, identity: tuple, box, text) -> None:
        self.saved = (self.current(box, text), box.scroll_y) if identity == self.identity else None
        self.identity = identity
        self.entries = []
        self.ink = None
        self.focused = None

    def mark(self, ident: str, label: str, ink: Ink) -> None:
        self.ink = ink
        self.entries.append((ident, label, len(ink.parts)))

    def finish(self, surface, box, text) -> None:
        requested = self.pending
        self.pending = None
        saved = self.saved
        self.saved = None

        def restore() -> None:
            ident = requested or (saved[0] if saved else None)
            entry = next((one for one in self.entries if one[0] == ident), None)
            if entry:
                box.scroll_to(y=self._height(entry[2], text), animate=False, force=True, immediate=True)
                self.focused = (entry[0], box.scroll_y)
            else:
                box.scroll_to(y=saved[1] if saved and not requested else 0, animate=False, force=True, immediate=True)
            if requested and not entry:
                surface.app.notify("That semantic location is absent from this reading.", severity="warning")

        surface.call_after_refresh(restore)

    def choose(self, surface, box, text) -> None:
        if not self.entries:
            surface.app.notify("There are no liturgical units in this reading yet.")
            return
        current = self.current(box, text)
        options = [(ident, label + ("  ·  here" if ident == current else ""))
                   for ident, label, _ in self.entries]

        def picked(ident) -> None:
            if ident is None:
                return
            entry = next(one for one in self.entries if one[0] == ident)
            surface.show_reading_pane()

            def move() -> None:
                box.scroll_to(y=self._height(entry[2], text), animate=False, force=True, immediate=True)
                self.focused = (entry[0], box.scroll_y)

            surface.call_after_refresh(move)
            box.focus()

        surface.app.push_screen(Pick("Contents", options, "Source events in their liturgical order."), picked)
