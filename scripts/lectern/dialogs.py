"""Small overlays: a question with one answer, and a page of text to read."""
from __future__ import annotations

import math
import os
import re
import shutil
import subprocess
from pathlib import Path

from rich.console import RenderableType
from textual.app import ComposeResult, SuspendNotSupported
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Input, Static

from .widgets import Ink, literal, titled

_SOURCE_ID_RE = re.compile(r"^(?:edition|artifact|passage)\.[a-z0-9_.-]+$", re.IGNORECASE)


class Ask(ModalScreen[str | None]):
    """One line of input; Enter answers, Escape declines."""

    DEFAULT_CSS = """
    Ask { align: center middle; background: $background 65%; }
    Ask > Vertical {
        width: 64; max-width: 95%; height: auto;
        border: round $primary 65%; background: $surface; padding: 1 2;
    }
    Ask Static { color: $text-muted; padding: 0 0 1 0; }
    """
    BINDINGS = [Binding("escape", "decline", "cancel")]

    def __init__(self, title: str, hint: str = "", value: str = "") -> None:
        super().__init__()
        self.title_text = title
        self.hint = hint
        self.value = value

    def compose(self) -> ComposeResult:
        with Vertical() as box:
            box.border_title = titled(None, self.title_text)
            box.border_subtitle = "enter apply · esc cancel"
            if self.hint:
                yield Static(self.hint)
            yield Input(value=self.value)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        # Enter answers, even with nothing (an empty answer clears); only
        # Escape declines.
        self.dismiss(event.value.strip())

    def action_decline(self) -> None:
        self.dismiss(None)


class Reading(ModalScreen[str | None]):
    """A long text over the surface, scrolled with the usual keys.

    `n` and `p` ask the surface for the next or previous item, so a reader can
    walk a chain without closing the page.
    """

    DEFAULT_CSS = """
    Reading { align: center middle; background: $background 65%; }
    Reading > VerticalScroll {
        width: 96; max-width: 96%; height: 92%;
        border: round $primary 65%; background: $surface; padding: 1 3;
        scrollbar-size-vertical: 1;
    }
    """
    BINDINGS = [
        Binding("escape,q", "dismiss(None)", "close"),
        Binding("n", "dismiss('next')", "next"),
        Binding("p", "dismiss('previous')", "previous"),
        Binding("s", "dismiss('source')", "source library"),
    ]

    def __init__(self, title: str, body: RenderableType, subtitle: str = "", *, walks: bool = True,
                 source: bool = False) -> None:
        super().__init__()
        self.title_text = title
        self.body = body
        self.subtitle = subtitle
        self.walks = walks
        self.source = source

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        if action == "dismiss" and parameters in (("next",), ("previous",)):
            return self.walks
        if action == "dismiss" and parameters == ("source",):
            return self.source
        return True

    def compose(self) -> ComposeResult:
        with VerticalScroll() as box:
            box.border_title = titled(None, self.title_text)
            hint = "esc close · n next · p previous" if self.walks else "esc close"
            box.border_subtitle = literal(self.subtitle or hint)
            yield Static(self.body, id="reading-body")

    def on_mount(self) -> None:
        self.query_one(VerticalScroll).focus()


def terminal_browser() -> str | None:
    for name in ("lynx", "w3m", "links", "elinks"):
        installed = shutil.which(name)
        if installed:
            return installed
        local = Path.home() / ".local" / "bin" / name
        if local.is_file() and os.access(local, os.X_OK):
            return str(local)
    return None


def browse_in_terminal(app, url: str) -> None:
    browser = terminal_browser()
    if browser:
        try:
            with app.suspend():
                subprocess.run([browser, url], check=False)
        except (OSError, SuspendNotSupported) as error:
            app.notify(str(error), severity="warning")


class MissalSource(Reading):
    """An identified external missal witness, usable by URL or keyboard."""

    DEFAULT_CSS = """
    MissalSource > VerticalScroll {
        height: auto; max-height: 90%;
    }
    """
    BINDINGS = [
        Binding("o", "open_witness", "open source"),
        Binding("c", "copy_url", "copy URL"),
        Binding("t", "terminal_witness", "terminal browser"),
        Binding("s", "inspect_source", "source library"),
    ]

    def __init__(self, title: str, link: dict, passage: list | None = None, common: dict | None = None) -> None:
        from .missal import blocks, source_rights, witness_label

        self.url = link["url"]
        self.source_id = link.get("source_id") or ""
        ink = Ink().line(title, "bold").line(witness_label(link)).line(link["locus"])
        if passage is not None:
            if common:
                ink.line(common["label"] + " · " + common["qualification"], "bold")
                blocks(ink, passage)
            else:
                ink.line("Consult the 1962 facsimile for the chant wording.", "italic")
        if link.get("rights_status"):
            ink.line(source_rights(link["rights_status"]), "$text-muted")
        roles = [r for r in (link.get("prayer_roles") or []) if not title.endswith(f" · {r}") and title != r]
        if roles:
            ink.line(" · ".join(roles))
        if self.source_id:
            ink.line(self.source_id, "$text-muted")
        ink.line().line(self.url, f'underline $primary link="{self.url}"')
        hints = ["o open", "c copy URL"]
        if terminal_browser():
            hints.append("t terminal browser")
        if self._has_source_record():
            hints.append("s source library")
        hints.append("esc close")
        super().__init__("Missal Source", ink.content(), " · ".join(hints), walks=False)

    def _has_source_record(self) -> bool:
        return bool(_SOURCE_ID_RE.match(self.source_id))

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        if action == "inspect_source":
            return self._has_source_record()
        return super().check_action(action, parameters)

    def action_terminal_witness(self) -> None:
        browse_in_terminal(self.app, self.url)

    def action_open_witness(self) -> None:
        self.app.open_url(self.url)

    def action_copy_url(self) -> None:
        self.app.copy_to_clipboard(self.url)
        self.app.notify("Source URL copied")

    def action_inspect_source(self) -> None:
        if not self._has_source_record():
            return
        source_id = self.source_id
        self.dismiss(None)
        if source_id.startswith("passage."):
            self.app.action_surface("sources", passage=source_id)
        else:
            self.app.action_surface("sources", edition=source_id)


class JanuaryReading(Reading):
    """A source-qualified January selection, including both external witnesses."""

    DEFAULT_CSS = """
    JanuaryReading > VerticalScroll {
        height: auto; max-height: 90%;
    }
    """
    BINDINGS = [
        Binding("o", "open_source('latin_url')", "Latin missal"),
        Binding("a", "open_source('english_url')", "English antiphons"),
        Binding("e", "open_source('english_prayer_url')", "English missal"),
        Binding("c", "copy_url", "copy URL"),
        Binding("t", "terminal_english", "English missal in terminal"),
        Binding("r", "open_source('rule_url')", "rubric"),
    ]

    def __init__(self, reading: dict, role: str | None = None) -> None:
        from .missal import blocks, source_rights

        if role and role not in (reading.get("english_prayer_roles") or []):
            reading = {**reading, "english_prayer_url": None}
        self.reading = reading
        phase = {"before-epiphany": "before Epiphany", "after-epiphany": "after Epiphany"}[reading["phase"]]
        ink = Ink()
        for prayer in reading["prayers"]:
            if role is None or prayer["role"] == role:
                blocks(ink, prayer["blocks"])
                ink.line()
        for field, label in (("latin_url", "Latin missal prayers"), ("english_prayer_url", "U.S. English missal prayers"),
                             ("english_url", "English antiphons only"),
                             ("rule_url", reading["rule_locus"])):
            if reading.get(field):
                ink.line(label, "bold")
                source_id = reading.get({"latin_url": "latin_source_id", "english_url": "english_source_id",
                                         "english_prayer_url": "english_prayer_source_id"}.get(field))
                if source_id:
                    ink.line(source_id, "$text-muted")
                locus = {"english_url": "english_locus", "english_prayer_url": "english_prayer_locus"}.get(field)
                if reading.get(locus):
                    ink.line(reading[locus])
                if field == "english_prayer_url" and reading.get("english_prayer_rights_status"):
                    ink.line(source_rights(reading["english_prayer_rights_status"]), "$text-muted")
                url = reading[field]
                ink.line(url, f'underline $primary link="{url}"').line()
        hint = "o Latin · a English antiphons · r rubric · c copy URL"
        if reading.get("english_prayer_url"):
            hint += " · e English missal" + (" · t terminal browser" if terminal_browser() else "")
        super().__init__(reading["label"] + " " + phase, ink.content(), hint + " · esc close", walks=False)

    def action_terminal_english(self) -> None:
        if self.reading.get("english_prayer_url"):
            browse_in_terminal(self.app, self.reading["english_prayer_url"])

    def action_open_source(self, field: str) -> None:
        if self.reading.get(field):
            self.app.open_url(self.reading[field])

    def action_copy_url(self) -> None:
        url = (self.reading.get("english_prayer_url") or self.reading.get("latin_url")
               or self.reading.get("english_url") or self.reading.get("rule_url"))
        if url:
            self.app.copy_to_clipboard(url)
            self.app.notify("Source URL copied")


class StudyDialog(Reading):
    """Contextual scholarly apparatus with Overview, Current Unit, and All Units views."""

    DEFAULT_CSS = """
    StudyDialog { align: center middle; background: $background 65%; }
    StudyDialog > Vertical {
        width: 100; max-width: 96%; height: 92%;
        border: round $primary 65%; background: $surface; padding: 0 2;
    }
    StudyDialog #study-tabs { height: auto; padding: 1 0 0 0; }
    StudyDialog #study-scroll {
        height: 1fr; padding: 1 1 1 0;
        scrollbar-size-vertical: 1;
    }
    """
    BINDINGS = [
        Binding("escape,q", "dismiss(None)", "close"),
        Binding("1", "tab('overview')", "overview", show=False),
        Binding("2", "tab('unit')", "this unit", show=False),
        Binding("3", "tab('all')", "all units", show=False),
        Binding("tab", "next_tab", "next section", show=False),
        Binding("a", "toggle_audit", "raw audit", show=False),
        Binding("o", "open_url_choice", "open source", show=False),
        Binding("c", "copy_url_choice", "copy URL", show=False),
        Binding("s", "inspect_source", "source library", show=False),
    ]

    def __init__(self, title: str, *, overview_builder, unit_builder=None, all_builder=None,
                 unit_label: str = "", initial_tab: str = "overview",
                 urls: list[tuple[str, str]] | None = None,
                 source_ids: list[str] | None = None,
                 accent: str = "$primary") -> None:
        self._overview_builder = overview_builder
        self._unit_builder = unit_builder
        self._all_builder = all_builder
        self._unit_label = unit_label
        self._accent = accent
        self._urls = urls or []
        self._source_ids = source_ids or []
        self._show_audit = False
        self._tabs: list[tuple[str, str]] = [("overview", "1 Overview")]
        if unit_builder is not None and unit_label:
            short_unit = unit_label if len(unit_label) <= 26 else unit_label[:25] + "…"
            self._tabs.append(("unit", f"2 This Unit ({short_unit})"))
        if all_builder is not None:
            self._tabs.append(("all", "3 All Units & Witnesses"))
        valid = [ident for ident, _ in self._tabs]
        self._active_tab = initial_tab if initial_tab in valid else valid[0]
        body = self._build_active()
        super().__init__(title, body, self._subtitle(), walks=False)

    def _build_active(self):
        if self._active_tab == "unit" and self._unit_builder is not None:
            return self._unit_builder(self._show_audit)
        if self._active_tab == "all" and self._all_builder is not None:
            return self._all_builder(self._show_audit)
        return self._overview_builder(self._show_audit)

    def _subtitle(self) -> str:
        parts = []
        if len(self._tabs) > 1:
            parts.append("tab/1–3 sections")
        parts.append("a " + ("hide audit" if self._show_audit else "raw audit"))
        if self._urls:
            parts.append("o open · c copy URL")
        if self._source_ids:
            parts.append("s source library")
        parts.append("esc close")
        return " · ".join(parts)

    def _tab_bar(self):
        ink = Ink()
        for ident, label in self._tabs:
            if ident == self._active_tab:
                ink(f" {label} ", f"bold reverse {self._accent}")("  ")
            else:
                ink(f" {label} ", "$text-muted")("  ")
        if self._show_audit:
            ink(" [raw audit shown]", "italic $warning")
        ink.line()
        ink("─" * 78, "$rule")
        return ink.content()

    def compose(self) -> ComposeResult:
        with Vertical() as box:
            box.border_title = titled(None, self.title_text)
            box.border_subtitle = literal(self._subtitle())
            if len(self._tabs) > 1 or self._show_audit:
                yield Static(self._tab_bar(), id="study-tabs")
            with VerticalScroll(id="study-scroll"):
                yield Static(self.body, id="reading-body")

    def on_mount(self) -> None:
        self.query_one("#study-scroll", VerticalScroll).focus()

    def _refresh_view(self) -> None:
        self.body = self._build_active()
        self.query_one("#reading-body", Static).update(self.body)
        tabs = self.query("#study-tabs")
        if tabs:
            tabs.first(Static).update(self._tab_bar())
        self.query_one(Vertical).border_subtitle = literal(self._subtitle())
        self.query_one("#study-scroll", VerticalScroll).scroll_home(animate=False)

    def action_tab(self, name: str) -> None:
        if any(ident == name for ident, _ in self._tabs) and name != self._active_tab:
            self._active_tab = name
            self._refresh_view()

    def action_next_tab(self) -> None:
        if len(self._tabs) < 2:
            return
        ids = [ident for ident, _ in self._tabs]
        self._active_tab = ids[(ids.index(self._active_tab) + 1) % len(ids)]
        self._refresh_view()

    def action_toggle_audit(self) -> None:
        self._show_audit = not self._show_audit
        self._refresh_view()

    def action_open_url_choice(self) -> None:
        if not self._urls:
            self.app.notify("No external witness URL is listed in this Study view.")
            return
        if len(self._urls) == 1:
            self.app.open_url(self._urls[0][1])
            return
        self.app.push_screen(
            Pick("Open Source URL", [(url, label) for label, url in self._urls]),
            lambda url: self.app.open_url(url) if url else None,
        )

    def action_copy_url_choice(self) -> None:
        if not self._urls:
            self.app.notify("No external witness URL is listed in this Study view.")
            return
        if len(self._urls) == 1:
            self.app.copy_to_clipboard(self._urls[0][1])
            self.app.notify("Source URL copied")
            return
        def copy(url) -> None:
            if url:
                self.app.copy_to_clipboard(url)
                self.app.notify("Source URL copied")
        self.app.push_screen(
            Pick("Copy Source URL", [(url, label) for label, url in self._urls]),
            copy,
        )

    def action_inspect_source(self) -> None:
        if not self._source_ids:
            self.app.notify("No Source Library edition or passage record is listed here.")
            return

        def jump(ident: str | None) -> None:
            if not ident:
                return
            self.dismiss(None)
            if ident.startswith("passage."):
                self.app.action_surface("sources", passage=ident)
            else:
                self.app.action_surface("sources", edition=ident)

        if len(self._source_ids) == 1:
            jump(self._source_ids[0])
            return
        self.app.push_screen(
            Pick("Inspect in Source Library", [(ident, ident) for ident in self._source_ids]),
            jump,
        )


def _label_lines(label: object, inner_width: int) -> int:
    text = label.plain if hasattr(label, "plain") else str(label)
    if not text:
        return 1
    total = 0
    for line in text.splitlines() or [""]:
        total += max(1, math.ceil(max(1, len(line)) / max(20, inner_width)))
    return total


class Pick(ModalScreen[str | None]):
    """One choice among named options; nothing is preselected for coequal choices."""

    DEFAULT_CSS = """
    Pick { align: center middle; background: $background 65%; }
    Pick > Vertical {
        width: 82; max-width: 95%; height: auto; max-height: 90%;
        border: round $primary 65%; background: $surface; padding: 1 2;
    }
    Pick Static { color: $text-muted; padding: 0 0 1 0; }
    Pick OptionList { border: none; background: transparent; padding: 0; height: 1fr; }
    Pick OptionList > .option-list--option-highlighted {
        background: $primary 25%;
        color: $foreground;
        text-style: bold;
    }
    Pick.reading-settings > Vertical { max-height: 92%; padding: 0 1; }
    Pick OptionList:focus { border: none; }
    """
    BINDINGS = [Binding("escape", "decline", "cancel")]

    def __init__(self, title: str, options: list[tuple[object, object]], hint: str = "",
                 *, sections: dict[int, str] | None = None,
                 initial_highlight: bool = False) -> None:
        super().__init__(classes="reading-settings" if sections else None)
        self.title_text = title
        self.options = options
        self.sections = sections or {}
        self.hint = hint
        self.initial_highlight = initial_highlight

    def _desired_height(self) -> int:
        term_w = (self.app.size.width if self.app and self.app.size.width else 100)
        term_h = (self.app.size.height if self.app and self.app.size.height else 40)
        box_w = min(82, int(term_w * 0.95))
        inner_w = max(24, box_w - (4 if self.sections else 6))
        rows = 0
        for index, (_, label) in enumerate(self.options):
            if index in self.sections:
                rows += 1
            rows += _label_lines(label, inner_w)
        hint_rows = (_label_lines(self.hint, inner_w) + 1) if self.hint else 0
        chrome = 2 if self.sections else 4  # top/bottom border + vertical padding
        cap = min(max(8, int(term_h * 0.88)), max(8, term_h - 3))
        return min(cap, max(6, rows + hint_rows + chrome))

    def compose(self) -> ComposeResult:
        from textual.widgets import OptionList
        from textual.widgets.option_list import Option

        with Vertical() as box:
            box.styles.height = self._desired_height()
            box.border_title = titled(None, self.title_text)
            box.border_subtitle = "↑↓ choose · enter apply · esc cancel"
            if self.hint:
                yield Static(self.hint)
            items = []
            for index, (_, label) in enumerate(self.options):
                if index in self.sections:
                    header = Ink()
                    if index > 0:
                        header("─ ", "$rule")
                    header(self.sections[index], "bold $primary")
                    items.append(Option(header.content(), disabled=True))
                items.append(Option(label, id=str(index)))
            yield OptionList(*items)

    def on_mount(self) -> None:
        from textual.widgets import OptionList

        listing = self.query_one(OptionList)
        listing.focus()
        if self.initial_highlight:
            first = next((i for i in range(listing.option_count)
                          if not listing.get_option_at_index(i).disabled), None)
            listing.highlighted = first
        else:
            # Nothing is offered as already chosen: Enter does nothing until the
            # reader has moved to an option.
            listing.highlighted = None

    def on_option_list_option_selected(self, event) -> None:
        self.dismiss(self.options[int(event.option.id)][0])

    def action_decline(self) -> None:
        self.dismiss(None)
