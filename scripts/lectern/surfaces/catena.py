"""Catena Omnia: a chapter, its dated chain and admitted undated commentary."""
from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
import re

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge, refs
from ..catena_find import CommentaryFinder
from ..dialogs import Ask, Pick, Reading
from ..repo import Refused
from ..strip import Cell, ChapterStrip
from ..surface import Surface, shown
from ..widgets import SUPERSCRIPT, Ink, Panel, ScrollPanel, literal

ADAPTER = "catena"
BOOKS_COLLAPSE_WIDTH = 130


def _plain(text: str) -> str:
    """The page sets fragment text `pre-line`: line breaks kept, runs of spaces
    collapsed, nothing interpreted."""
    return "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in (text or "").split("\n"))


def _collapse_ws(text: str) -> str:
    """Collapse internal horizontal space runs while preserving span boundaries."""
    return "\n".join(re.sub(r"[ \t]+", " ", line) for line in text.split("\n"))


def _utf16_to_py(text: str, pos: int) -> int:
    """Convert a UTF-16 code-unit offset from JS into a Python str index."""
    if pos <= 0:
        return 0
    if all(ord(ch) <= 0xFFFF for ch in text):
        return min(pos, len(text))
    units = 0
    for idx, ch in enumerate(text):
        if units >= pos:
            return idx
        units += 2 if ord(ch) > 0xFFFF else 1
    return len(text)


def _blocks_for(text: str, blocks: list[dict] | None) -> list[dict]:
    """Use validated adapter blocks when available, or split plain text on blank lines."""
    if blocks:
        return blocks
    cleaned = _plain(text)
    if not cleaned.strip():
        return []
    parts = [part.strip() for part in re.split(r"\n\s*\n+", cleaned) if part.strip()]
    return [{"kind": "plain", "text": part, "speaker": None, "transition": None, "notes": []}
            for part in parts]


def _render_block(ink: Ink, block: dict, *, lemma_prefix: str = "") -> Ink:
    """Render one structured block (lemma / commentary / plain) into theme-aware Ink."""
    raw = block.get("text") or ""
    if not raw:
        return ink
    kind = block.get("kind") or "plain"
    base_style = "italic $text-muted" if kind == "lemma" else ""

    # Collect non-overlapping styled spans (speaker, transition, editorial notes).
    spans: list[tuple[int, int, str]] = []
    speaker = block.get("speaker")
    if isinstance(speaker, (list, tuple)) and len(speaker) == 2:
        spans.append((_utf16_to_py(raw, speaker[0]), _utf16_to_py(raw, speaker[1]), "bold $catena-color"))
    transition = block.get("transition")
    if isinstance(transition, (list, tuple)) and len(transition) == 2:
        spans.append((_utf16_to_py(raw, transition[0]), _utf16_to_py(raw, transition[1]), "italic $text-muted"))
    for note in block.get("notes") or ():
        if isinstance(note, (list, tuple)) and len(note) == 2:
            spans.append((_utf16_to_py(raw, note[0]), _utf16_to_py(raw, note[1]), "dim italic"))
    spans.sort(key=lambda item: (item[0], item[1]))

    def emit(segment: str, style: str, at_line_start: bool) -> bool:
        if not segment:
            return at_line_start
        cleaned = _collapse_ws(segment)
        if lemma_prefix and kind == "lemma":
            lines = cleaned.split("\n")
            for idx, piece in enumerate(lines):
                if idx > 0:
                    ink("\n")
                    at_line_start = True
                if at_line_start and piece:
                    ink(lemma_prefix, base_style)
                    at_line_start = False
                if piece:
                    ink(piece, style)
            return at_line_start
        ink(cleaned, style)
        return cleaned.endswith("\n")

    cursor = 0
    line_start = True
    for start, end, style in spans:
        start = max(cursor, min(start, len(raw)))
        end = max(start, min(end, len(raw)))
        if start > cursor:
            line_start = emit(raw[cursor:start], base_style, line_start)
        if end > start:
            line_start = emit(raw[start:end], style, line_start)
        cursor = end
    if cursor < len(raw):
        emit(raw[cursor:], base_style, line_start)
    return ink


def _parse_verse_range(verses: str) -> tuple[int, int] | None:
    text = (verses or "").strip()
    if not text:
        return None
    match = re.fullmatch(r"([1-9][0-9]*)(?:-([1-9][0-9]*))?", text)
    if not match:
        return None
    first = int(match.group(1))
    last = int(match.group(2)) if match.group(2) else first
    return (first, last) if last >= first else None


def _span_bounds(span: dict | None) -> tuple[int, int | None] | None:
    if not isinstance(span, dict):
        return None
    start = span.get("start")
    end = span.get("end")
    if not isinstance(start, int) or start < 1:
        return None
    if end is not None and (not isinstance(end, int) or end < start):
        return None
    return (start, end)


def _verse_in_span(number: int, bounds: tuple[int, int | None] | None) -> bool:
    if bounds is None:
        return False
    lo, hi = bounds
    return number >= lo and (hi is None or number <= hi)


def _match_snippet_block_index(blocks: list[dict], snippets: list[dict]) -> int | None:
    """Locate the first full-context block containing the first matched snippet."""
    if not blocks or not snippets:
        return None
    first = snippets[0]
    snip_blocks = first.get("blocks") or []
    probe = (snip_blocks[0].get("text") if snip_blocks else first.get("text") or "").strip()
    if not probe:
        return None
    sample = re.sub(r"\s+", " ", probe)[:64]
    for index, block in enumerate(blocks):
        hay = re.sub(r"\s+", " ", block.get("text") or "")
        if sample and sample in hay:
            return index
    short = sample[:28]
    if short:
        for index, block in enumerate(blocks):
            hay = re.sub(r"\s+", " ", block.get("text") or "")
            if short in hay:
                return index
    return None


@dataclass
class _ReadingState:
    position: int
    fragment: dict
    body: dict
    full_context: bool = False
    english_version: dict | None = None
    english_body: dict | None = None


class CatenaScrollPanel(ScrollPanel):
    """A scrolling reading pane with j/k and clean non-animated page turns."""

    BINDINGS = [
        Binding("j", "scroll_down", "down", show=False),
        Binding("k", "scroll_up", "up", show=False),
    ]

    def action_scroll_down(self) -> None:
        self.scroll_relative(y=1, animate=False, immediate=True)

    def action_scroll_up(self) -> None:
        self.scroll_relative(y=-1, animate=False, immediate=True)

    def action_page_down(self) -> None:
        self.scroll_relative(y=max(1, self.scrollable_content_region.height - 1), animate=False, immediate=True)

    def action_page_up(self) -> None:
        self.scroll_relative(y=-max(1, self.scrollable_content_region.height - 1), animate=False, immediate=True)


class BookList(OptionList):
    """Canonical book list with j/k movement."""

    BINDINGS = [
        Binding("j", "cursor_down", "down", show=False),
        Binding("k", "cursor_up", "up", show=False),
    ]


class FragmentList(OptionList):
    """Chain option list with j/k movement and responsive locator re-ellipsizing."""

    BINDINGS = [
        Binding("j", "cursor_down", "down", show=False),
        Binding("k", "cursor_up", "up", show=False),
    ]

    def on_resize(self) -> None:
        # Pane toggles and terminal resizing can change width (requiring fresh
        # locator truncation) or move the highlighted fragment out of view.
        surface = next((node for node in self.ancestors if isinstance(node, Catena)), None)
        if surface is not None and surface.current and surface.current.get("chain"):
            width = self.size.width
            if width and width != surface._chain_drawn_width:
                surface.call_after_refresh(surface._redraw_chain_for_resize)
                return
        if self.highlighted is not None:
            option = self.get_option_at_index(self.highlighted)
            if option.id and option.id.startswith("frag-"):
                self.call_after_refresh(self.scroll_to_highlight)


class EnglishPick(Pick):
    """Choose among linked English versions with clean spacing and first option highlighted."""

    DEFAULT_CSS = Pick.DEFAULT_CSS + """
    EnglishPick OptionList > .option-list--option { padding: 0 1 1 1; }
    """

    def on_mount(self) -> None:
        self.call_after_refresh(self._highlight_first)

    def _highlight_first(self) -> None:
        listing = self.query_one(OptionList)
        if listing.highlighted is None and listing.option_count:
            listing.highlighted = 0


class FragmentReading(Reading):
    """Fullscreen zoomed commentary reading; z or Esc returns to side-by-side."""

    BINDINGS = [
        Binding("z", "dismiss('unzoom')", "side-by-side"),
        Binding("c", "dismiss('context')", "full context"),
        Binding("e", "dismiss('english')", "English version"),
        Binding("j", "scroll_down", "down", show=False),
        Binding("k", "scroll_up", "up", show=False),
    ]

    def __init__(self, *args, excerpts: bool, english: bool, previous: bool, following: bool, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.excerpts = excerpts
        self.english = english
        self.previous = previous
        self.following = following

    def action_scroll_down(self) -> None:
        self.query_one(VerticalScroll).scroll_relative(y=1, animate=False, immediate=True)

    def action_scroll_up(self) -> None:
        self.query_one(VerticalScroll).scroll_relative(y=-1, animate=False, immediate=True)

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        if action == "dismiss" and parameters:
            actions = {"context": self.excerpts, "english": self.english,
                       "next": self.following, "previous": self.previous}
            if parameters[0] in actions:
                return actions[parameters[0]]
        return super().check_action(action, parameters)


class Catena(Surface):
    key = "3"
    label = "Catena"
    FIRST = "#catena-chain-list"
    HELP = (
        ("i", "find chapters with commentary by book or reference, including chapters with English"),
        ("← / →, h / l", "previous / next chapter"),
        ("↑ / ↓, j / k", "move or scroll in Scripture, chain, commentary, and drawers"),
        ("[ / ]", "previous / next book"),
        ("tab / shift+tab", "switch directly between commentary and Scripture"),
        ("g", "go to a reference, e.g. 'Mark 1', 'John 1:1-5', or '1 Cor 13' (Vulgate)"),
        ("G", "show or hide the books sidebar (auto-hidden below 130 columns)"),
        ("r", "focus commentary on a verse or range; empty restores the whole chapter"),
        ("x", "exclude or restore an author; exclusions persist across chapters"),
        ("o", "toggle commentary order between By author and By verse"),
        ("b / B", "next Scripture edition / choose a named edition (keeps scroll and selection)"),
        ("v / V", "next commentary voice / choose everything held, original language, or translation"),
        ("enter", "open/close an author, read a fragment beside Scripture, or open research notes"),
        ("n / p", "in the commentary reader, step to the next or previous fragment (syncs Scripture)"),
        ("e", "in the commentary reader, toggle paired English inline beside the original"),
        ("c", "in the commentary reader with matched excerpts, switch to full context and back"),
        ("z", "zoom commentary to fullscreen and back to side-by-side"),
        ("s", "in the commentary reader, open the current passage in the Source Library"),
        ("esc / backspace", "close the commentary reader or open drawer and return to the chain"),
        ("L", "show or hide the acquisition leads drawer (auto-shown when no fragments are held)"),
        ("a", "show or hide scrollable translation research notes (under translation voices)"),
        ("A", "open or close every author's fragments"),
        ("click", "a bar in the strip opens that chapter"),
        ("f", "focus: scripture and commentary alone; again to restore chapter strip and books"),
    )
    BINDINGS = [
        Binding("left,h", "chapter(-1)", "previous chapter", show=False),
        Binding("right,l", "chapter(1)", "next chapter", show=False),
        Binding("left_square_bracket", "book(-1)", "previous book", show=False),
        Binding("right_square_bracket", "book(1)", "next book", show=False),
        Binding("tab", "switch_pane(1)", "switch pane", show=False),
        Binding("shift+tab", "switch_pane(-1)", "previous pane", show=False),
        Binding("i", "find_commentary", "find"),
        Binding("g", "goto", "go to"),
        Binding("G", "toggle_books", "books", show=False),
        Binding("b", "bible", "edition"),
        Binding("v", "voice", "voice"),
        Binding("B", "choose_bible", "choose Scripture edition", show=False),
        Binding("V", "choose_voice", "choose commentary voice", show=False),
        Binding("r", "verses", "verses"),
        Binding("x", "authors", "authors"),
        Binding("o", "toggle_order", "order"),
        Binding("L", "toggle_leads", "leads"),
        Binding("a", "toggle_absences", "notes", show=False),
        Binding("A", "expand_all", "open all authors", show=False),
        Binding("n", "step_fragment(1)", "next", show=False),
        Binding("p", "step_fragment(-1)", "previous", show=False),
        Binding("e", "toggle_english", "English", show=False),
        Binding("c", "toggle_context", "context", show=False),
        Binding("z", "zoom_reading", "zoom", show=False),
        Binding("s", "open_source", "source library", show=False),
        Binding("escape,backspace", "close_active", "back", show=False),
    ]
    DEFAULT_CSS = """
    Catena #catena-books { width: 28; }
    Catena #catena-strip-box { height: auto; max-height: 6; }
    Catena #catena-scripture { width: 1fr; min-height: 4; }
    Catena #catena-right { width: 1fr; }
    Catena #catena-chain { height: 2fr; min-height: 4; }
    Catena #catena-reader { display: none; height: 2fr; min-height: 4; }
    Catena #catena-absences { display: none; height: 1fr; min-height: 5; }
    Catena #catena-leads { display: none; height: 1fr; min-height: 5; }
    Catena #catena-instruction { display: none; height: auto; color: $text-muted; }
    Catena .verse-paragraph { margin: 0 0 1 0; padding: 0 0 0 2; }
    Catena .verse-paragraph.projected { border-left: dashed $catena-color 70%; margin: 0 0 1 0; padding: 0 0 0 1; }
    Catena .verse-paragraph.printed { border-left: heavy $catena-color; margin: 0 0 1 0; padding: 0 0 0 1; }
    Catena .note { color: $text-muted; }
    Catena .refusal { color: $warning; border-left: heavy $warning; padding: 0 0 0 1; margin: 0 0 1 0; }
    Catena .reader-head { margin: 0 0 1 0; }
    Catena .reader-licence { margin: 0 0 1 0; }
    Catena .reader-block { margin: 0 0 1 0; }
    Catena .reader-lemma { border-left: heavy $catena-color 45%; padding: 0 0 0 1; margin: 0 0 1 1; }
    Catena .reader-block.excerpt-hit { border-left: heavy $catena-color; padding: 0 0 0 1; }
    Catena .reader-english-divider { margin: 1 0 1 0; }
    Catena .reader-apparatus { margin: 1 0 0 0; }
    Catena.cramped .reader-head { margin: 0; }
    """

    # A lead is not commentary, and its frame says so (catena.css:23-26):
    # a dashed rule, never the solid one the chain is drawn in.
    CSS = """
    .catena.books-collapsed #catena-books { display: none; }
    .catena.focus #catena-books, .catena.focus #catena-strip-box { display: none; }
    .catena.reading-open #catena-chain { display: none; }
    .catena.reading-open #catena-reader { display: block; }
    .catena.leads-shown #catena-leads { display: block; }
    .catena.absences-shown #catena-absences { display: block; }
    .catena.narrow #catena-books { display: none; }
    .catena.compact #catena-reading { layout: vertical; }
    .catena.compact #catena-scripture { width: 1fr; height: 2fr; min-height: 4; }
    .catena.compact #catena-right { width: 1fr; height: 3fr; min-height: 4; }
    .catena.compact #catena-instruction { display: block; }
    .catena.compact #catena-chain-list { height: 1fr; }
    .catena.compact.cramped #catena-instruction { display: none; }
    .catena.compact.cramped #catena-chain { min-height: 4; }
    .catena.compact.cramped #catena-reader { min-height: 4; }
    .catena.compact.cramped #catena-right { min-height: 4; }
    .catena.compact.cramped #catena-leads { min-height: 4; }
    .catena.compact.cramped #catena-absences { min-height: 4; }
    .catena #catena-leads { border: dashed $catena-color 45%; }
    .catena #catena-leads:focus, .catena #catena-leads:focus-within { border: dashed $catena-color; }
    .catena #catena-absences { border: round $warning 55%; }
    .catena #catena-absences:focus, .catena #catena-absences:focus-within { border: round $warning; }
    """

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.books: list[dict] = []
        self.holdings: list[dict] = []
        self.bibles: list[dict] = []
        self.token = "Gen"
        self.chapter = 1
        self.bible = ""
        self.voice = ""
        self.verses = ""
        self.hidden_authors: set[str] = set()
        self.current: dict | None = None
        self.density: dict[str, list[dict]] = {}
        # Which author groups of the chain in front of the reader are open.
        self.opened_groups: set[int] = set()
        self.chain_for: tuple | None = None
        self.panes_chosen = False
        self.books_override: bool | None = None
        self.sort_by_verse = False
        self.leads_override: bool | None = None
        self.absences_open = False
        self.reading_state: _ReadingState | None = None
        self._reader_text = ""
        self._chain_drawn_width = 0
        self._scripture_paragraphs: list[tuple[Static, dict, list[int]]] = []
        self._active_span: tuple[int, int | None] | None = None
        self._preserve_on_bible_switch: tuple[float, str | None] | None = None
        self._has_printed_breaks = False
        self._has_projected_breaks = False

    # --- building --------------------------------------------------------

    def on_resize(self, event) -> None:
        super().on_resize(event)
        self.set_class(event.size.height < 27, "cramped")
        if self.books_override is None:
            self.set_class(event.size.width < BOOKS_COLLAPSE_WIDTH, "books-collapsed")
        if not self.panes_chosen:
            self.set_class(self.has_class("compact") and self.has_class("cramped"), "focus")
        self._sync_drawer_classes()

    def action_focus_reading(self) -> None:
        self.panes_chosen = True
        super().action_focus_reading()
        self._sync_drawer_classes()

    def action_toggle_books(self) -> None:
        currently_hidden = self.has_class("books-collapsed") or self.has_class("focus") or self.has_class("narrow")
        if currently_hidden:
            self.books_override = True
            self.remove_class("books-collapsed")
            if self.has_class("focus"):
                self.panes_chosen = True
                self.remove_class("focus")
            if self.has_class("narrow"):
                self.remove_class("narrow")
        else:
            self.books_override = False
            self.add_class("books-collapsed")
        self.call_after_refresh(self.refocus)

    def _sync_drawer_classes(self) -> None:
        """Keep #catena-leads and #catena-absences visibility consistent with chapter state."""
        view = self.current if self.current and not self.current.get("problems") else None
        chain = view.get("chain") if view else None
        held_total = chain.get("total", 0) if chain else 0
        if self.leads_override is not None:
            show_leads = self.leads_override
        elif self.has_class("focus") or self.reading_state is not None:
            show_leads = False
        else:
            show_leads = bool(view and held_total == 0 and (view.get("leads") or view.get("blocked")))
        self.set_class(show_leads, "leads-shown")
        has_absences = bool(chain and chain.get("absences") and (
            chain["absences"].get("rows") or chain["absences"].get("unread")
        ))
        if not has_absences:
            self.absences_open = False
        self.set_class(self.absences_open and has_absences, "absences-shown")
        self.set_class(self.reading_state is not None, "reading-open")

    def build(self) -> None:
        self.mount(
            Horizontal(
                Panel(BookList(id="catena-book-list"), title="books", id="catena-books"),
                Vertical(
                    Panel(ChapterStrip(id="catena-strip"), title="chapters", id="catena-strip-box"),
                    Horizontal(
                        CatenaScrollPanel(Static("", id="catena-loading"), title="scripture", id="catena-scripture"),
                        Vertical(
                            Panel(Static("Enter opens an author or reads a fragment beside Scripture.",
                                         id="catena-instruction"),
                                  FragmentList(id="catena-chain-list"), title="chain", id="catena-chain"),
                            CatenaScrollPanel(Static("", id="catena-reader-empty"), title="commentary",
                                              id="catena-reader"),
                            CatenaScrollPanel(Static("", id="catena-absences-text"),
                                              title="translation research notes", id="catena-absences"),
                            CatenaScrollPanel(Static("", id="catena-lead-text"), title="acquisition list",
                                              id="catena-leads"),
                            id="catena-right",
                        ),
                        id="catena-reading",
                    ),
                ),
            )
        )
        self.start()

    @work(thread=True, exclusive=True, group="catena-start")
    def start(self) -> None:
        try:
            opening = bridge.call(ADAPTER, "opening")
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.opened_with, opening)

    def opened_with(self, opening: dict) -> None:
        self.books = opening["books"]
        self.holdings = opening["holdings"]
        self.bibles = opening["bibles"]
        listing = self.query_one("#catena-book-list", OptionList)
        listing.clear_options()
        testament = None
        for book in self.books:
            if book["testament"] != testament:
                testament = book["testament"]
                if listing.option_count:
                    listing.add_option(None)
                listing.add_option(Option(Ink()(testament, "bold $text-muted").content(), disabled=True))
            row = Ink()(f"{book['name']:<17}"[:17])
            if book["fragments"]:
                row(f"{book['fragments']:>6}", "bold $catena-color")
            elif book["present"]:
                row("     ·", "$text-muted")
            listing.add_option(Option(row.content(), id=f"book-{book['token']}"))
        pending = getattr(self, "_pending_ref", None)
        self._pending_ref = None
        if pending is not None:
            self.goto_text(pending)
        else:
            self.go(self.token, self.chapter)

    def fail(self, message: str) -> None:
        self.say(Ink()(message, "bold $error"))

    def say(self, ink: Ink) -> None:
        """A message where the scripture would be, whatever the pane held before."""
        box = self.query_one("#catena-scripture", ScrollPanel)
        box.remove_children()
        self._scripture_paragraphs = []
        box.mount(Static(ink.content()))

    # --- pane focus & action gating --------------------------------------

    def action_switch_pane(self, direction: int) -> None:
        """Tab switches directly between commentary (#catena-chain-list / #catena-reader)
        and #catena-scripture in 1 Tab, then any open drawers or visible books pane."""
        right_primary = self.query_one("#catena-reader" if self.reading_state is not None else "#catena-chain-list")
        scripture = self.query_one("#catena-scripture")
        ring = [right_primary, scripture]
        if self.has_class("absences-shown"):
            ring.append(self.query_one("#catena-absences"))
        if self.has_class("leads-shown"):
            ring.append(self.query_one("#catena-leads"))
        if self.reading_state is None:
            books = self.query_one("#catena-book-list")
            if shown(books):
                ring.append(books)
        ring = [widget for widget in ring if widget.focusable and shown(widget)]
        if not ring:
            return
        focused = self.app.focused
        if focused in ring:
            target = ring[(ring.index(focused) + direction) % len(ring)]
        else:
            target = ring[0]
        target.focus()

    def check_action(self, action: str, parameters: tuple) -> bool | None:
        state = self.reading_state
        if action == "step_fragment":
            if state is None:
                return False
            order = self._ordered_indices()
            if state.position not in order:
                return False
            idx = order.index(state.position)
            step = parameters[0] if parameters else 1
            return 0 <= idx + step < len(order)
        if action == "toggle_english":
            return state is not None and bool(state.fragment.get("englishVersions"))
        if action == "toggle_context":
            return state is not None and not state.body.get("missing") and bool(state.body.get("snippets"))
        if action in ("zoom_reading", "open_source"):
            return state is not None
        if action == "close_active":
            return (
                state is not None
                or self.absences_open
                or (self.app.focused is not None and self.app.focused.id == "catena-leads")
            )
        return super().check_action(action, parameters)

    # --- moving ----------------------------------------------------------

    def follow(self, ref: str | None = None, **_) -> None:
        if ref is None:
            return
        ref = ref.strip()
        if not self.books:
            self._pending_ref = ref
            return
        self.goto_text(ref)

    def goto_text(self, ref: str) -> None:
        reference, separator, verses = ref.partition(":")
        found = refs.parse(reference, self.books)
        if found is None:
            self.app.notify(f"No book of this canon is called {literal(repr(ref))}.", severity="warning")
            return
        book, chapter = found
        self.go(book["token"], chapter, verses if separator else "")

    def go(self, token: str, chapter: int, verses: str = "") -> None:
        if (token, chapter) != (self.token, self.chapter):
            self._close_reader_state()
            self.absences_open = False
            self.leads_override = None
        self.token, self.chapter = token, chapter
        self.verses = verses
        self.load()

    @work(thread=True, exclusive=True, group="catena-view")
    def load(self) -> None:
        token, chapter, bible, voice = self.token, self.chapter, self.bible, self.voice
        verses, excluded = self.verses, sorted(self.hidden_authors)
        try:
            view = bridge.call(ADAPTER, "view", token, chapter, bible, voice,
                               verses, excluded)
            if token not in self.density and not view.get("problems"):
                self.density[token] = bridge.call(ADAPTER, "density", token)
        except Refused as refusal:
            self.deliver(self.fail, str(refusal))
            return
        self.deliver(self.show, view)

    def action_chapter(self, step: int) -> None:
        if self.current and not self.current.get("problems"):
            last = self.current["book"]["chapters"]
            target = self.chapter + step
            if 1 <= target <= last:
                self.go(self.token, target)

    def action_book(self, step: int) -> None:
        tokens = [book["token"] for book in self.books]
        if self.token in tokens:
            position = (tokens.index(self.token) + step) % len(tokens)
            self.go(tokens[position], 1)

    def action_goto(self) -> None:
        def answered(value: str | None) -> None:
            if value:
                self.goto_text(value)

        self.app.push_screen(Ask("go to", "Vulgate reference, e.g. Gen 1:3-8, Mark 1, 1 Cor 13", ""), answered)

    def action_find_commentary(self) -> None:
        if not self.books:
            return

        def answered(reference: tuple[str, int] | None) -> None:
            if reference:
                self.voice = ""
                self._close_reader_state()
                self.go(*reference)
                self.query_one("#catena-chain-list", OptionList).focus()

        self.app.push_screen(CommentaryFinder(self.holdings), answered)

    def action_verses(self) -> None:
        def answered(value: str | None) -> None:
            if value is not None:
                self.verses = value
                self.load()

        self.app.push_screen(Ask("Commentary verses (Vulgate)",
                                 "One verse or an ascending range, e.g. 3 or 3-8. Empty shows the whole chapter. "
                                 "Scripture retains its edition’s own numbering.", self.verses), answered)

    def action_authors(self) -> None:
        if not self.current or not self.current.get("chain"):
            return
        names = self.current["chain"].get("authors", [])
        options = [("restore-all", "Restore all authors")]
        options += [(name, ("Restore " if name in self.hidden_authors else "Exclude ") + name) for name in names]

        def answered(value: str | None) -> None:
            if value is None:
                return
            if value == "restore-all":
                self.hidden_authors.clear()
            else:
                self.hidden_authors ^= {value}
            self.load()

        self.app.push_screen(Pick("Authors shown", options,
                                  "Choose an author to switch off or restore. Exclusions persist across chapters."),
                             answered)

    def _capture_bible_switch_state(self) -> None:
        """Preserve Scripture scroll position and chain highlight across Bible switches."""
        scripture = self.query_one("#catena-scripture", ScrollPanel)
        listing = self.query_one("#catena-chain-list", OptionList)
        keep: str | None = None
        if listing.highlighted is not None and listing.option_count:
            keep = listing.get_option_at_index(listing.highlighted).id
        self._preserve_on_bible_switch = (float(scripture.scroll_y), keep)

    def action_bible(self) -> None:
        if not self.bibles:
            return
        ids = [one["id"] for one in self.bibles]
        current = self.bible or ids[0]
        self._capture_bible_switch_state()
        self.bible = ids[(ids.index(current) + 1) % len(ids)]
        self.load()

    def action_voice(self) -> None:
        if not self.current or self.current.get("problems"):
            return
        values = [option["value"] for option in self.current["voices"]]
        position = values.index(self.voice) if self.voice in values else 0
        self.voice = values[(position + 1) % len(values)]
        self.absences_open = False
        self.load()

    def action_choose_bible(self) -> None:
        if not self.bibles:
            return
        choices = []
        for bible in self.bibles:
            facts = [bible["label"], bible["languageName"], bible["numberingLabel"]]
            if bible["id"] == self.bible:
                facts.append("selected")
            choices.append((bible["id"], Ink()(" · ".join(filter(None, facts))).content()))

        def answered(value: str | None) -> None:
            if value is not None and value != self.bible:
                self._capture_bible_switch_state()
                self.bible = value
                self.load()

        self.app.push_screen(Pick("Scripture edition", choices,
                                  "Scripture follows the edition’s numbering. Commentary uses Vulgate references."),
                             answered)

    def action_choose_voice(self) -> None:
        if not self.current or self.current.get("problems"):
            return
        choices = [(row["value"], row["label"] + (" · selected" if row["value"] == self.voice else ""))
                   for row in self.current["voices"]]

        def answered(value: str | None) -> None:
            if value is not None and value != self.voice:
                self.voice = value
                self.absences_open = False
                self.load()

        self.app.push_screen(Pick("Commentary voice", choices, "Choose which commentary editions to read here."),
                             answered)

    def action_toggle_order(self) -> None:
        if not self.current or not self.current.get("chain"):
            return
        self.sort_by_verse = not self.sort_by_verse
        if self.reading_state is not None:
            self._render_docked_reader()
            self.app.refresh_bindings()
            return
        listing = self.query_one("#catena-chain-list", OptionList)
        keep = None
        if listing.highlighted is not None and listing.option_count:
            keep = listing.get_option_at_index(listing.highlighted).id
        self.draw_chain(keep=keep)

    def action_toggle_leads(self) -> None:
        if not self.current or self.current.get("problems"):
            return
        currently = self.has_class("leads-shown")
        self.leads_override = not currently
        self._sync_drawer_classes()
        if self.has_class("leads-shown"):
            leads = self.query_one("#catena-leads", ScrollPanel)
            leads.scroll_home(animate=False)
            leads.focus()
        else:
            self._focus_primary_right()
        self.app.refresh_bindings()

    def action_toggle_absences(self) -> None:
        if not self.current or not self.current.get("chain"):
            return
        absences = self.current["chain"].get("absences")
        if not absences or not (absences.get("rows") or absences.get("unread")):
            self.app.notify("No translation research notes for this chapter and voice.", timeout=2)
            return
        self.absences_open = not self.absences_open
        self._sync_drawer_classes()
        if self.absences_open:
            panel = self.query_one("#catena-absences", ScrollPanel)
            panel.scroll_home(animate=False)
            panel.focus()
        else:
            self._focus_primary_right()
        self.app.refresh_bindings()

    def action_close_active(self) -> None:
        if self.absences_open:
            self.absences_open = False
            self._sync_drawer_classes()
            self._focus_primary_right()
            self.app.refresh_bindings()
            return
        if self.app.focused is not None and self.app.focused.id == "catena-leads":
            self.leads_override = False
            self._sync_drawer_classes()
            self._focus_primary_right()
            self.app.refresh_bindings()
            return
        if self.reading_state is not None:
            self.close_reading()

    def _focus_primary_right(self) -> None:
        target_id = "#catena-reader" if self.reading_state is not None else "#catena-chain-list"
        target = self.query_one(target_id)
        if target.focusable and shown(target):
            target.focus()
        else:
            self.refocus()

    @on(OptionList.OptionSelected, "#catena-book-list")
    def picked_book(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("book-"):
            self.go(event.option.id[5:], 1)

    @on(ChapterStrip.Picked)
    def picked_chapter(self, event: ChapterStrip.Picked) -> None:
        self.go(self.token, event.chapter)

    @on(OptionList.OptionSelected, "#catena-chain-list")
    def picked_fragment(self, event: OptionList.OptionSelected) -> None:
        if event.option.id == "open-absences":
            self.action_toggle_absences()
        elif event.option.id and event.option.id.startswith("frag-"):
            self.read(int(event.option.id[5:]))
        elif event.option.id and event.option.id.startswith("grp-"):
            group = int(event.option.id[4:])
            self.opened_groups ^= {group}
            self.draw_chain(keep=event.option.id)

    @on(OptionList.OptionHighlighted, "#catena-chain-list")
    def reveal_fragment(self, event: OptionList.OptionHighlighted) -> None:
        if event.option.id and event.option.id.startswith("frag-"):
            event.option_list.call_after_refresh(event.option_list.scroll_to_highlight)
            if self.reading_state is None and self.current and self.current.get("chain"):
                position = int(event.option.id[5:])
                fragments = self.current["chain"]["fragments"]
                if 0 <= position < len(fragments):
                    self._sync_scripture_highlight(_span_bounds(fragments[position].get("span")))
        elif self.reading_state is None:
            self._sync_scripture_highlight(_parse_verse_range(self.verses), scroll=False)

    def action_expand_all(self) -> None:
        if not self.current or not self.current.get("chain") or self.sort_by_verse:
            return
        groups = range(len(self.groups(self.current["chain"]["fragments"])))
        self.opened_groups = set() if self.opened_groups >= set(groups) else set(groups)
        listing = self.query_one("#catena-chain-list", OptionList)
        keep = None
        if listing.highlighted is not None and listing.option_count:
            keep = listing.get_option_at_index(listing.highlighted).id
        self.draw_chain(keep=keep)

    # --- drawing ---------------------------------------------------------

    def where(self) -> str:
        if not self.current or self.current.get("problems"):
            return ""
        parts = [self.current["reference"], self.current["bible"]["label"], self.current["tally"]["spoken"]]
        if self.current.get("verses") and self.current.get("chain") is not None:
            parts.append(f"{self.current['chain']['shown']} matching")
        return " · ".join(parts)

    def show(self, view: dict) -> None:
        if view.get("problems"):
            good = self.current if self.current and not self.current.get("problems") else None
            if good:
                # Refused, as the page refuses it (catena.js:626); the chapter in
                # front of the reader stays, and nothing nearby is put in its place.
                self.token, self.chapter = good["book"]["token"], good["chapter"]
                self.verses = good.get("verses", "")
                self._preserve_on_bible_switch = None
                said = "; ".join(f"{one['key']} = {one['value']!r}: {one['note']}" for one in view["problems"])
                self.app.notify(literal(f"{view['heading']}. {said}"), severity="warning", timeout=6)
                return
            self.current = view
            self._preserve_on_bible_switch = None
            self.show_problems(view)
            return

        preserved = self._preserve_on_bible_switch
        self._preserve_on_bible_switch = None
        same_chapter = (
            self.current is not None
            and not self.current.get("problems")
            and self.current.get("book", {}).get("token") == view["book"]["token"]
            and self.current.get("chapter") == view["chapter"]
        )
        prev_reading_id = self.reading_state.fragment["id"] if self.reading_state else None
        prev_verses = self.current.get("verses", "") if self.current else ""

        self.current = view
        self.verses = view.get("verses", "")
        self.bible = view["bible"]["id"]

        if not same_chapter:
            self._close_reader_state()
        elif self.reading_state is not None:
            # Keep docked reader open if the same fragment still stands in this view.
            frags = (view.get("chain") or {}).get("fragments") or []
            matched = next((i for i, row in enumerate(frags) if row["id"] == prev_reading_id), None)
            if matched is None:
                self._close_reader_state()
            else:
                self.reading_state.position = matched
                self.reading_state.fragment = frags[matched]
                if self.verses != prev_verses:
                    self.read(matched)

        self.show_books(view)
        self.show_strip(view)
        self.show_scripture(view, preserve_scroll=preserved[0] if (preserved and same_chapter) else None)
        self.show_chain(view, keep=preserved[1] if (preserved and same_chapter) else None)
        self.show_absences(view)
        self.show_leads(view)
        self._sync_drawer_classes()
        if self.reading_state is not None:
            self._sync_scripture_highlight(
                _span_bounds(self.reading_state.fragment.get("span")),
                scroll=preserved is None,
            )
        self.app.refresh_where()
        self.app.refresh_bindings()

    def show_problems(self, view: dict) -> None:
        text = Ink().line(view["heading"], "bold").line()
        for problem in view["problems"]:
            text(f"{problem['key']} = {problem['value']!r}: ", "bold").line(problem["note"])
        self.say(text)
        self.app.notify(view["heading"], severity="warning")

    def show_books(self, view: dict) -> None:
        listing = self.query_one("#catena-book-list", OptionList)
        try:
            index = listing.get_option_index(f"book-{view['book']['token']}")
        except Exception:
            return
        if listing.highlighted != index:
            listing.highlighted = index

    def show_strip(self, view: dict) -> None:
        rows = self.density.get(view["book"]["token"], [])
        cells = [
            Cell(row["fragments"], faint=bool(row["leads"] or row["blocked"]), broken=row["unreadable"])
            for row in rows
        ]
        self.query_one(ChapterStrip).show(cells, view["chapter"])
        box = self.query_one("#catena-strip-box", Panel)
        box.retitle(f"{view['book']['name']} · {view['testament']}")
        held = sum(1 for row in rows if row["fragments"])
        box.border_subtitle = (
            f"█ fragments ({held}/{len(rows)}) · · leads · ▲ ch. {view['chapter']}"
        )

    def _render_scripture_paragraph(self, paragraph: dict, by_verse: dict | None,
                                    active: tuple[int, int | None] | None) -> Ink:
        text = Ink()
        for verse in paragraph["verses"]:
            num = verse["number"]
            is_active = by_verse is not None and _verse_in_span(num, active)
            has_commentary = by_verse is None or str(num) in by_verse
            sup = str(num).translate(SUPERSCRIPT)
            if is_active:
                text(sup, "bold $catena-color on $catena-color 35%")
                text(" " + verse["text"] + " ", "on $catena-color 20%")
            elif has_commentary:
                text(sup, "bold $catena-color")
                text(" " + verse["text"] + " ")
            else:
                text(sup, "$text-muted")
                text(" " + verse["text"] + " ")
        return text

    def _update_scripture_subtitle(self, view: dict) -> None:
        box = self.query_one("#catena-scripture", ScrollPanel)
        scripture = view["scripture"]
        if not scripture["ok"]:
            box.border_subtitle = ""
            return
        parts = [f"{scripture.get('verseCount', 0)} verses"]
        if self._has_printed_breaks:
            parts.append("┃ printed ¶")
        if self._has_projected_breaks:
            parts.append("╏ projected ¶")
        if view.get("verse_commentary") is not None and self._active_span is not None:
            lo, hi = self._active_span
            parts.append(f"v. {lo}" if hi == lo else (f"v. {lo}–{hi}" if hi else f"v. {lo}+"))
        box.border_subtitle = " · ".join(parts)

    def _sync_scripture_highlight(self, bounds: tuple[int, int | None] | None, *,
                                  scroll: bool = True, force_scroll: bool = False) -> None:
        view = self.current
        if not view or view.get("problems") or not view.get("scripture", {}).get("ok"):
            return
        verse_map = view.get("verse_commentary")
        if verse_map is None:
            # Never highlight canonical verse numbers under a refusal or recast shift.
            self._active_span = None
            self._update_scripture_subtitle(view)
            return
        target = bounds if bounds is not None else _parse_verse_range(view.get("verses", ""))
        previous = self._active_span
        if target == previous and not force_scroll:
            return
        self._active_span = target
        by_verse = verse_map.get("byVerse", {})
        scroll_widget: Static | None = None
        for widget, paragraph, numbers in self._scripture_paragraphs:
            was_hit = any(_verse_in_span(n, previous) for n in numbers)
            now_hit = any(_verse_in_span(n, target) for n in numbers)
            if was_hit or now_hit:
                widget.update(self._render_scripture_paragraph(paragraph, by_verse, target).content())
            if scroll_widget is None and target is not None and now_hit:
                scroll_widget = widget
        self._update_scripture_subtitle(view)
        if scroll and scroll_widget is not None:
            box = self.query_one("#catena-scripture", ScrollPanel)

            def bring_into_upper_third(widget: Static = scroll_widget) -> None:
                if not widget.is_attached:
                    return
                height = max(1, box.scrollable_content_region.height)
                target_y = max(0, widget.virtual_region.y - height // 3)
                box.scroll_to(y=target_y, animate=False)

            box.call_after_refresh(bring_into_upper_third)

    def show_scripture(self, view: dict, *, preserve_scroll: float | None = None) -> None:
        box = self.query_one("#catena-scripture", ScrollPanel)
        box.remove_children()
        self._scripture_paragraphs = []
        self._active_span = None
        self._has_printed_breaks = False
        self._has_projected_breaks = False
        bible = view["bible"]
        box.retitle(f"{view['reference']} · {bible['label']}")
        scripture = view["scripture"]
        verse_map = view.get("verse_commentary")
        by_verse = verse_map.get("byVerse", {}) if verse_map is not None else None
        initial_active = (
            _span_bounds(self.reading_state.fragment.get("span"))
            if self.reading_state is not None
            else _parse_verse_range(view.get("verses", ""))
        )
        if verse_map is None:
            initial_active = None
        self._active_span = initial_active

        widgets = []
        if view.get("focusNote"):
            widgets.append(Static(Ink()(view["focusNote"], "italic").content(), classes="note"))
        if view["refusal"]:
            widgets.append(Static(Ink()(view["refusal"]).content(), classes="refusal"))
        if not scripture["ok"]:
            refusal_ink = Ink()("Scripture not shown — ", "bold $warning")(scripture["problem"], "$warning")
            widgets.append(Static(refusal_ink.content(), classes="refusal"))
        else:
            if scripture["note"]:
                widgets.append(Static(Ink()(scripture["note"], "italic").content(), classes="note"))
            scroll_target: Static | None = None
            for section in scripture["sections"]:
                widgets.append(Static(Ink()(section["label"], "bold $catena-color").content()))
                for paragraph in section["paragraphs"]:
                    if paragraph["kind"] == "printed":
                        self._has_printed_breaks = True
                    elif paragraph["kind"] == "projected":
                        self._has_projected_breaks = True
                    text = self._render_scripture_paragraph(paragraph, by_verse, initial_active)
                    classes = "verse-paragraph"
                    if paragraph["kind"]:
                        classes += " " + paragraph["kind"]
                    widget = Static(text.content(), classes=classes)
                    numbers = [v["number"] for v in paragraph["verses"]]
                    self._scripture_paragraphs.append((widget, paragraph, numbers))
                    if scroll_target is None and initial_active is not None:
                        if any(_verse_in_span(n, initial_active) for n in numbers):
                            scroll_target = widget
                    widgets.append(widget)
                widgets.append(Static(Ink()(section["note"], "italic").content(), classes="note"))
        box.mount_all(widgets)
        self._update_scripture_subtitle(view)
        if preserve_scroll is not None:
            box.call_after_refresh(lambda y=preserve_scroll: box.scroll_to(y=y, animate=False))
        elif scripture["ok"] and initial_active is not None:
            target = next(
                (w for w, _, nums in self._scripture_paragraphs
                 if any(_verse_in_span(n, initial_active) for n in nums)),
                None,
            )
            if target is not None:
                def jump(widget: Static = target) -> None:
                    if widget.is_attached:
                        height = max(1, box.scrollable_content_region.height)
                        box.scroll_to(y=max(0, widget.virtual_region.y - height // 3), animate=False)

                box.call_after_refresh(jump)
            else:
                box.scroll_home(animate=False)
        else:
            box.scroll_home(animate=False)

    @staticmethod
    def groups(fragments: list[dict]) -> list[list[int]]:
        """Contiguous runs of one author, date and composition-date class
        in the chain's own order; the adapter's order is never re-sorted."""
        runs: list[list[int]] = []
        last = None
        for position, fragment in enumerate(fragments):
            key = (fragment["author"], fragment["date"], fragment.get("composition_date_status"))
            if fragment["author"] and runs and key == last:
                runs[-1].append(position)
            else:
                runs.append([position])
            last = key
        return runs

    def _ordered_indices(self) -> list[int]:
        if not self.current or not self.current.get("chain"):
            return []
        chain = self.current["chain"]
        fragments = chain["fragments"]
        if self.sort_by_verse:
            order = chain.get("by_verse_order")
            if isinstance(order, list) and len(order) == len(fragments):
                return order
        return list(range(len(fragments)))

    def show_chain(self, view: dict, *, keep: str | None = None) -> None:
        here = (view["book"]["token"], view["chapter"], view["voice"], view.get("verses", ""),
                tuple(sorted(self.hidden_authors)))
        auto_opened = False
        if here != self.chain_for:
            self.chain_for = here
            groups = self.groups(view["chain"]["fragments"]) if view.get("chain") else []
            # Auto-open single-author chapters (e.g. Mark/Matt Catena Aurea) and
            # single-author filtered results; keep multi-author chapters closed.
            if len(groups) == 1:
                self.opened_groups = {0}
                auto_opened = True
            else:
                self.opened_groups = set()
        if keep is None and auto_opened and not self.sort_by_verse:
            keep = "frag-0"
        self.draw_chain(keep=keep)

    def _redraw_chain_for_resize(self) -> None:
        if not self.current or not self.current.get("chain"):
            return
        listing = self.query_one("#catena-chain-list", OptionList)
        keep = None
        if listing.highlighted is not None and listing.option_count:
            keep = listing.get_option_at_index(listing.highlighted).id
        self.draw_chain(keep=keep)

    def _fragment_row(self, fragment: dict, *, listing_width: int, shared_work: str = "",
                      show_author: bool = False, indent: str = "    ") -> Ink:
        row = Ink()(indent)
        row("● " if fragment["review"] == "verified" else "◌ ", "$text-muted")
        row(fragment["extent"], "bold")
        if fragment["spans"]:
            row(" ↔", "$warning")
        if show_author and fragment.get("author"):
            row("  ")(fragment["author"], "bold $catena-color")
            if fragment.get("date"):
                row(f" {fragment['date']}", "$text-muted")
        if not shared_work and fragment.get("work"):
            row("  ")(fragment["work"], "italic")
        row.line()(indent + "  ")
        # Build crisp tail: compact [en] / [+en] indicator + word count; locator takes remaining width.
        badges = []
        if fragment.get("language") == "en" and not fragment.get("text_refused"):
            badges.append("[en]")
        elif fragment.get("englishVersions"):
            badges.append("[+en]")
        elif fragment.get("chip"):
            badges.append(fragment["chip"])
        words_str = f"{fragment['text_words']:,} w" if fragment.get("text_words") else ""
        tail_parts = [part for part in (words_str, " ".join(badges)) if part]
        tail = " · ".join(tail_parts)
        room = (listing_width - 2 if listing_width else 56) - (len(indent) + 2) - len(tail) - 3
        locator = fragment.get("locator") or ""
        if locator and locator != fragment.get("work") and room >= 6:
            row(locator if len(locator) <= room else locator[:room - 1] + "…", "$text-muted")
            row(" · ", "$text-muted")
        row(tail, "$text-muted")
        return row

    def draw_chain(self, keep: str | None = None) -> None:
        view = self.current
        if not view or view.get("problems"):
            return
        listing = self.query_one("#catena-chain-list", OptionList)
        self._chain_drawn_width = listing.size.width
        listing.clear_options()
        box = self.query_one("#catena-chain", Panel)
        chain = view["chain"]
        if view["unfetched"]:
            listing.add_option(Option(Ink()(view["unfetched"], "bold $error").content(), disabled=True))
            box.retitle("chain")
            box.border_subtitle = ""
            return
        voice = next((option["label"] for option in view["voices"] if option["value"] == view["voice"]),
                     "Everything held")
        fragments = chain["fragments"]
        has_dated = any(f.get("composition_date_status") != "unestablished" for f in fragments)
        has_undated = any(f.get("composition_date_status") == "unestablished" for f in fragments)
        if self.sort_by_verse:
            order_tag = "by verse"
        elif has_dated and has_undated:
            order_tag = "oldest + undated"
        elif has_dated:
            order_tag = "oldest"
        elif has_undated:
            order_tag = "undated"
        else:
            order_tag = ""
        short_heading = chain["heading"].replace(" held here", "").replace("One fragment", "1 fragment")
        title_parts = [short_heading, voice]
        if order_tag:
            title_parts.append(order_tag)
        box.retitle(" · ".join(title_parts))

        leads_count = len(view.get("leads") or [])
        absences = chain.get("absences")
        has_absences = bool(absences and (absences.get("rows") or absences.get("unread")))
        sub_parts = ["● verified ◌ uncollated"]
        if leads_count and has_absences:
            sub_parts.append(f"{leads_count}L")
            sub_parts.append("a notes")
        else:
            if leads_count:
                sub_parts.append(f"{leads_count} leads (L)")
            if has_absences:
                sub_parts.append("a notes")
        if fragments:
            sub_parts.append("o author" if self.sort_by_verse else "o verse")
        box.border_subtitle = " · ".join(sub_parts)

        for note in chain["notes"]:
            listing.add_option(Option(Ink()(note, "italic").content(), disabled=True))
        for note in (chain.get("availability"), chain.get("contextNote")):
            if note:
                listing.add_option(Option(Ink()(note, "italic $text-muted").content(), disabled=True))

        if self.sort_by_verse:
            for position in self._ordered_indices():
                fragment = fragments[position]
                row = self._fragment_row(fragment, listing_width=listing.size.width,
                                         show_author=True, indent="  ")
                listing.add_option(Option(row.content(), id=f"frag-{position}"))
        else:
            undated_header = False
            for number, run in enumerate(self.groups(fragments)):
                first = fragments[run[0]]
                if first.get("composition_date_status") == "unestablished" and not undated_header:
                    listing.add_option(Option(Ink()("Composition date not established", "bold $warning").content(),
                                              disabled=True))
                    undated_header = True
                opened = number in self.opened_groups
                words = sum(fragments[position]["text_words"] or 0 for position in run)
                works = {fragments[position]["work"] for position in run if fragments[position].get("work")}
                shared_work = next(iter(works)) if len(works) == 1 else ""
                heading = Ink()("▾ " if opened else "▸ ", "bold $catena-color")
                heading(first["author"] or first["work"], "bold $catena-color")
                if first["date"]:
                    heading(f"  {first['date']}", "bold")
                # Hoist shared work title onto the opened header so fragment rows stay crisp
                # without leaking work titles onto collapsed multi-author rows.
                if opened and shared_work and first["author"]:
                    heading("  ")(shared_work, "italic")
                count = f"{len(run)} fragment" + ("" if len(run) == 1 else "s")
                heading(f"  · {count} · {words:,} words", "$text-muted")
                english = sum(1 for position in run if fragments[position].get("language") == "en"
                              and not fragments[position].get("text_refused"))
                if english:
                    heading(f" · {english} in English", "$text-muted")
                listing.add_option(Option(heading.content(), id=f"grp-{number}"))
                if not opened:
                    continue
                for position in run:
                    fragment = fragments[position]
                    row = self._fragment_row(fragment, listing_width=listing.size.width,
                                             shared_work=shared_work if first["author"] else "")
                    listing.add_option(Option(row.content(), id=f"frag-{position}"))

        # Keyboard-reachable action item for translation research notes (replaces disabled items!).
        if has_absences:
            rows = absences.get("rows") or []
            n_works = len(rows)
            action = Ink()("▸ ", "bold $warning")
            if n_works:
                action(f"Translation research notes ({n_works} {'work' if n_works == 1 else 'works'})",
                       "bold $warning")
                action(" · press a or Enter", "$text-muted")
            else:
                action("Translation research note · press a or Enter", "bold $warning")
            if absences.get("summary"):
                action.line()("  ")(absences["summary"], "italic $text-muted")
            listing.add_option(Option(action.content(), id="open-absences"))

        if keep is not None:
            try:
                index = listing.get_option_index(keep)
                listing.highlighted = index
                if keep.startswith("frag-") and self.reading_state is None:
                    pos = int(keep[5:])
                    if 0 <= pos < len(fragments):
                        self._sync_scripture_highlight(_span_bounds(fragments[pos].get("span")), scroll=False)
                return
            except Exception:  # noqa: BLE001 - the kept row may be gone; fall through to the first
                pass
        first_idx = next((index for index in range(listing.option_count)
                          if not listing.get_option_at_index(index).disabled), None)
        if first_idx is not None:
            listing.highlighted = first_idx
            listing.call_after_refresh(listing.scroll_home, animate=False)

    def show_absences(self, view: dict) -> None:
        box = self.query_one("#catena-absences", ScrollPanel)
        chain = view.get("chain") or {}
        absences = chain.get("absences")
        text = Ink()
        if absences:
            if absences.get("summary"):
                text.line(absences["summary"], "bold $warning").line()
            for row in absences.get("rows", []):
                text(row.get("author") or "", "bold")
                if row.get("author") and row.get("work"):
                    text(" — ", "bold")
                text.line(row.get("work") or "", "bold italic")
                if row.get("reason"):
                    text.line(row["reason"])
                if row.get("offer"):
                    text.line(row["offer"], "italic $success")
                text.line()
            if absences.get("unread"):
                text.line(absences["unread"], "italic")
            count = len(absences.get("rows") or [])
            box.retitle(f"translation research notes ({count} {'work' if count == 1 else 'works'})"
                        if count else "translation research notes")
            box.border_subtitle = "↑↓/j/k scroll · a or Esc close"
        else:
            box.retitle("translation research notes")
            box.border_subtitle = ""
        box.query_one("#catena-absences-text", Static).update(text.content())
        box.scroll_home(animate=False)

    def show_leads(self, view: dict) -> None:
        box = self.query_one("#catena-leads", ScrollPanel)
        leads, blocked = view["leads"], view["blocked"]
        text = Ink()
        if blocked:
            text.line("Held, and not renderable yet", "bold")
            for entry in blocked:
                text(f"{entry.get('named', '')} ", "bold").line(entry.get("why", ""))
            text.line()
        if leads:
            # page: catena.js:571-578
            text.line(
                f"{len(leads)} " + ("unreconciled lead entry" if len(leads) == 1 else "unreconciled lead entries")
                + " on the acquisition record for this chapter, which omits its confidence. An entry "
                "establishes no distinct work, no possession and nothing renderable, and the list is "
                "not checked against the commentary above.",
                "italic $text-muted",
            )
            for lead in leads:
                if lead.get("who"):
                    text(f"{lead['who']} — ")
                text(lead.get("title", ""), "italic")
                if lead.get("when"):
                    text(f" ({lead['when']})", "$text-muted")
                text.line()
        else:
            text("No lead entries on the acquisition record for this chapter.", "italic $text-muted")
        box.query_one("#catena-lead-text", Static).update(text.content())
        box.retitle("believed to comment here — the acquisition list")
        box.border_subtitle = f"{len(leads)} leads · not commentary · L close"
        box.scroll_home(animate=False)

    # --- reading a fragment ----------------------------------------------

    def _close_reader_state(self) -> None:
        self.reading_state = None
        self._reader_text = ""
        self.remove_class("reading-open")

    def close_reading(self) -> None:
        state = self.reading_state
        if state is None:
            return
        position = state.position
        self._close_reader_state()
        self._sync_drawer_classes()
        if self.current and self.current.get("chain"):
            if not self.sort_by_verse:
                groups = self.groups(self.current["chain"]["fragments"])
                for number, run in enumerate(groups):
                    if position in run:
                        self.opened_groups.add(number)
                        break
            self.draw_chain(keep=f"frag-{position}")
        listing = self.query_one("#catena-chain-list", OptionList)
        listing.focus()
        listing.call_after_refresh(listing.scroll_to_highlight)
        self.app.refresh_bindings()

    def read(self, position: int, *, zoomed: bool = False) -> None:
        if not self.current or not self.current.get("chain"):
            return
        fragments = self.current["chain"]["fragments"]
        if not 0 <= position < len(fragments):
            return
        # The chapter on screen, not one still loading behind it.
        self.fetch_body(position, fragments[position], self.current, zoomed=zoomed)

    @work(thread=True, exclusive=True, group="catena-body")
    def fetch_body(self, position: int, fragment: dict, view: dict, *,
                   version: dict | None = None, zoomed: bool = False,
                   inline_english: bool = False) -> None:
        try:
            body = bridge.call(ADAPTER, "body", view["book"]["token"], view["chapter"], view["voice"],
                               fragment["id"], view.get("verses", ""))
        except Refused as refusal:
            body = {"missing": True, "said": str(refusal)}

        def display() -> None:
            if self.current is not view or self.app.current() is not self:
                return
            if inline_english:
                if self.reading_state is None or self.reading_state.position != position:
                    return
                self.reading_state.english_version = version
                self.reading_state.english_body = body
                self._render_docked_reader(scroll_to_english=True)
                self.app.refresh_bindings()
                if zoomed:
                    self._push_zoomed_reading()
                return
            if self.app.screen is self.screen or zoomed:
                self.open_reading(position, fragment, body, zoomed=zoomed)

        self.deliver(display)

    def _build_reading_sections(
        self,
        fragment: dict,
        body: dict,
        *,
        full_context: bool = False,
        english_version: dict | None = None,
        english_body: dict | None = None,
    ) -> tuple[Ink, Ink | None, list[tuple[Ink, str, bool]], list[tuple[Ink, str, bool]], Ink, Ink]:
        """Build compact header, required licence above prose, structured prose blocks,
        optional inline paired English blocks, below-prose apparatus, and combined Ink."""
        snippets = body.get("snippets", []) if not body.get("missing") else []
        versions = fragment.get("englishVersions", [])
        seen_notes: set[str] = set()

        # 1. Compact 2-line top header so prose starts immediately even at 60x16.
        head = Ink()(fragment["author"], "bold $catena-color")
        if fragment["date"]:
            head(f" · {fragment['date']}", "bold")
        elif fragment.get("composition_date_status") == "unestablished":
            head(" · undated", "bold $warning")
        head(" · ")(fragment["extent"], "bold")
        if fragment.get("spans"):
            head(" ↔", "$warning")
        length = f"{fragment['text_words']:,} w" if fragment.get("text_words") else ""
        if length:
            head(f" · {length}", "$text-muted")
        head.line()
        head(fragment["work"], "italic")
        meta = [fragment.get("locator") or "", fragment.get("chip") or ""]
        meta_str = " · ".join(part for part in meta if part)
        if meta_str:
            head(f" · {meta_str}", "$text-muted")
        if versions and english_version is None:
            head.line()(self.english_offer(versions) + " (e)", "bold $catena-color")
        elif english_version is not None:
            head.line()("Paired English below (e toggle)", "bold $catena-color")

        # 2. Required Licence ABOVE the prose (Rule 9).
        licence_ink: Ink | None = None
        if body.get("acknowledgement_broken"):
            licence_ink = Ink()("The recorded acknowledgement is malformed and not shown.", "bold $warning")
        elif body.get("acknowledgement"):
            licence_ink = Ink()("Licence: ", "bold")(body["acknowledgement"])

        # 3. Commentary prose (structured blocks with blank-line separation).
        prose_items: list[tuple[Ink, str, bool]] = []
        said = body.get("said")
        if body.get("missing"):
            prose_items.append((
                Ink()(said or "The text of this fragment could not be loaded.", "bold $warning"),
                "reader-block",
                False,
            ))
        elif snippets and not full_context:
            banner = Ink()("Matched commentary excerpts", "bold $catena-color")(" · c full context", "italic $text-muted")
            prose_items.append((banner, "reader-block", False))
            for snippet in snippets:
                s_head = Ink()(snippet["extent"], "bold")
                if snippet.get("locator"):
                    s_head(" · ")(snippet["locator"], "italic $text-muted")
                prose_items.append((s_head, "reader-block", False))
                for block in _blocks_for(snippet.get("text", ""), snippet.get("blocks")):
                    b_ink = _render_block(Ink(), block)
                    cls = "reader-block reader-lemma" if block.get("kind") == "lemma" else "reader-block"
                    prose_items.append((b_ink, cls, False))
                s_basis = (snippet.get("basis") or "").strip()
                if s_basis and s_basis not in seen_notes:
                    seen_notes.add(s_basis)
                    prose_items.append((Ink()("Selection — ", "bold")(s_basis), "reader-block", False))
        else:
            if snippets:
                banner = Ink()("Complete source passage", "bold $catena-color")(" · c excerpts", "italic $text-muted")
                prose_items.append((banner, "reader-block", False))
            full_blocks = _blocks_for(said if isinstance(said, str) else "", body.get("blocks"))
            hit_idx = _match_snippet_block_index(full_blocks, snippets) if snippets else None
            for idx, block in enumerate(full_blocks):
                b_ink = _render_block(Ink(), block)
                is_hit = hit_idx is not None and idx == hit_idx
                cls = "reader-block reader-lemma" if block.get("kind") == "lemma" else "reader-block"
                if is_hit:
                    cls += " excerpt-hit"
                prose_items.append((b_ink, cls, is_hit))

        # 4. Inline paired English section (when toggled open via 'e').
        english_items: list[tuple[Ink, str, bool]] = []
        if english_version is not None and english_body is not None:
            target = english_version["fragment"]
            eng_seen: set[str] = set()
            divider = Ink()("── " + self.version_label(english_version) + " ──", "bold $catena-color")
            english_items.append((divider, "reader-english-divider", False))

            e_head = Ink()(target["extent"], "bold")
            if target.get("work"):
                e_head(" · ")(target["work"], "italic")
            if target.get("locator"):
                e_head(f" · {target['locator']}", "$text-muted")
            if target.get("text_words"):
                e_head(f" · {target['text_words']:,} words", "$text-muted")
            link_basis = (english_version.get("basis") or "").strip()
            if link_basis:
                eng_seen.add(link_basis)
                e_head.line()(link_basis, "italic $text-muted")
            english_items.append((e_head, "reader-block", False))

            # English Licence ABOVE English prose (Rule 9).
            if english_body.get("acknowledgement_broken"):
                english_items.append((
                    Ink()("The recorded acknowledgement is malformed and not shown.", "bold $warning"),
                    "reader-licence",
                    False,
                ))
            elif english_body.get("acknowledgement"):
                english_items.append((
                    Ink()("Licence: ", "bold")(english_body["acknowledgement"]),
                    "reader-licence",
                    False,
                ))

            e_snippets = english_body.get("snippets", []) if not english_body.get("missing") else []
            e_said = english_body.get("said")
            if english_body.get("missing"):
                english_items.append((
                    Ink()(e_said or "The text of this fragment could not be loaded.", "bold $warning"),
                    "reader-block",
                    False,
                ))
            elif e_snippets and not full_context:
                for snippet in e_snippets:
                    sh = Ink()(snippet["extent"], "bold")
                    if snippet.get("locator"):
                        sh(" · ")(snippet["locator"], "italic $text-muted")
                    english_items.append((sh, "reader-block", False))
                    for block in _blocks_for(snippet.get("text", ""), snippet.get("blocks")):
                        b_ink = _render_block(Ink(), block)
                        cls = "reader-block reader-lemma" if block.get("kind") == "lemma" else "reader-block"
                        english_items.append((b_ink, cls, False))
                    sb = (snippet.get("basis") or "").strip()
                    if sb and sb not in eng_seen:
                        eng_seen.add(sb)
                        english_items.append((Ink()("Selection — ", "bold")(sb), "reader-block", False))
            else:
                for block in _blocks_for(e_said if isinstance(e_said, str) else "", english_body.get("blocks")):
                    b_ink = _render_block(Ink(), block)
                    cls = "reader-block reader-lemma" if block.get("kind") == "lemma" else "reader-block"
                    english_items.append((b_ink, cls, False))

            # English apparatus below English prose (deduplicating basis against version["basis"]).
            e_app = Ink()
            if target.get("edition"):
                e_app("Edition — ", "bold").line(target["edition"])
            if target.get("translators"):
                e_app("Translated by ", "bold").line(", ".join(target["translators"]))
            e_basis = (english_body.get("basis") or "").strip()
            if e_basis and e_basis not in eng_seen:
                eng_seen.add(e_basis)
                e_app("Extent — ", "bold").line(e_basis)
            e_date_basis = (target.get("composition_date_basis") or english_body.get("date_basis") or "").strip()
            if e_date_basis and e_date_basis not in eng_seen:
                eng_seen.add(e_date_basis)
                e_app("Date — ", "bold").line(e_date_basis)
            e_facts = [target.get("locator"), target.get("edition_published"),
                       target.get("rights"), target.get("attribution"), target.get("rights_basis"),
                       target.get("reviewNote"), f"source library: {target['id']}"]
            e_app(" · ".join(fact for fact in e_facts if fact), "$text-muted")
            english_items.append((e_app, "reader-apparatus", False))

        # 5. Primary apparatus BELOW the commentary prose.
        apparatus = Ink().line("───", "$text-muted")
        if fragment.get("composition_date_status") == "unestablished":
            apparatus.line("Composition date not established", "bold $warning")
        if fragment.get("edition"):
            apparatus("Edition — ", "bold").line(fragment["edition"])
        if fragment.get("translators"):
            apparatus("Translated by ", "bold").line(", ".join(fragment["translators"]))
        body_basis = (body.get("basis") or "").strip()
        if body_basis and body_basis not in seen_notes:
            seen_notes.add(body_basis)
            apparatus("Extent — ", "bold").line(body_basis)
        date_basis = (fragment.get("composition_date_basis") or body.get("date_basis") or "").strip()
        if date_basis and date_basis not in seen_notes:
            seen_notes.add(date_basis)
            apparatus("Date — ", "bold").line(date_basis)
        facts = [fragment.get("locator"), fragment.get("edition_published"),
                 fragment.get("rights"), fragment.get("attribution"), fragment.get("rights_basis")]
        if fragment.get("reviewNote"):
            facts.append(fragment["reviewNote"])
        facts.append(f"source library: {fragment['id']}")
        apparatus(" · ".join(fact for fact in facts if fact), "$text-muted")

        # 6. Combined Ink for fullscreen FragmentReading modal (preserving blank lines and lemma indent).
        combined = Ink()
        combined.parts.extend(head.parts)
        combined.line().line()
        if licence_ink is not None:
            combined.parts.extend(licence_ink.parts)
            combined.line().line()
        for item_ink, cls, _ in prose_items:
            if "reader-lemma" in cls:
                # Indent lemma blocks explicitly in the flat fullscreen modal.
                combined("  ", "italic $text-muted")
            combined.parts.extend(item_ink.parts)
            combined.line().line()
        for item_ink, cls, _ in english_items:
            if "reader-lemma" in cls:
                combined("  ", "italic $text-muted")
            combined.parts.extend(item_ink.parts)
            combined.line().line()
        combined.parts.extend(apparatus.parts)

        return head, licence_ink, prose_items, english_items, apparatus, combined

    def _reading_subtitle(self, state: _ReadingState, *, zoomed: bool = False) -> str:
        order = self._ordered_indices()
        count = len(order) or len((self.current.get("chain") or {}).get("fragments") or [])
        pos_num = (order.index(state.position) + 1) if state.position in order else state.position + 1
        snippets = state.body.get("snippets", []) if not state.body.get("missing") else []
        versions = state.fragment.get("englishVersions", [])
        hints = [f"{pos_num}/{count}"]
        if versions:
            hints.append("e English")
        if snippets:
            hints.append("c excerpts" if state.full_context else "c full context")
        if count > 1:
            hints.append("n/p")
        if zoomed:
            hints.append("z side-by-side")
            hints.append("s source library")
            hints.append("Esc back")
        else:
            hints.append("z zoom" if not (versions or snippets) else "z")
            hints.append("s source library")
            if not (versions or snippets):
                hints.append("Esc")
        return " · ".join(hints)

    def _render_docked_reader(self, *, scroll_to_excerpt: bool = False,
                              scroll_to_english: bool = False) -> None:
        state = self.reading_state
        if state is None:
            return
        head, licence_ink, prose_items, english_items, apparatus, combined = self._build_reading_sections(
            state.fragment,
            state.body,
            full_context=state.full_context,
            english_version=state.english_version,
            english_body=state.english_body,
        )
        self._reader_text = str(combined.content())
        reader = self.query_one("#catena-reader", ScrollPanel)
        reader.remove_children()
        title = f"{state.fragment['author']} · {state.fragment['extent']}"
        reader.retitle(title)
        reader.border_subtitle = self._reading_subtitle(state, zoomed=False)

        widgets: list[Static] = [Static(head.content(), classes="reader-head")]
        if licence_ink is not None:
            widgets.append(Static(licence_ink.content(), classes="reader-licence"))
        excerpt_widget: Static | None = None
        for item_ink, cls, is_hit in prose_items:
            widget = Static(item_ink.content(), classes=cls)
            if is_hit and excerpt_widget is None:
                excerpt_widget = widget
            widgets.append(widget)
        english_anchor: Static | None = None
        for idx, (item_ink, cls, _) in enumerate(english_items):
            widget = Static(item_ink.content(), classes=cls, id="catena-reader-english" if idx == 0 else None)
            if idx == 0:
                english_anchor = widget
            widgets.append(widget)
        widgets.append(Static(apparatus.content(), classes="reader-apparatus"))
        reader.mount_all(widgets)

        if scroll_to_excerpt and excerpt_widget is not None:
            def jump_excerpt(widget: Static = excerpt_widget) -> None:
                if widget.is_attached:
                    reader.scroll_to_widget(widget, top=True, animate=False)

            reader.call_after_refresh(jump_excerpt)
        elif scroll_to_english and english_anchor is not None:
            def jump_english(widget: Static = english_anchor) -> None:
                if not widget.is_attached:
                    return
                height = max(1, reader.scrollable_content_region.height)
                if widget.virtual_region.y > max(2, height - 4):
                    reader.scroll_to(y=max(0, widget.virtual_region.y - 2), animate=False)

            reader.call_after_refresh(jump_english)
        else:
            reader.scroll_home(animate=False)

    def open_reading(self, position: int, fragment: dict, body: dict, *, full_context: bool = False,
                     zoomed: bool = False) -> None:
        self.reading_state = _ReadingState(
            position=position,
            fragment=fragment,
            body=body,
            full_context=full_context,
        )
        self._sync_drawer_classes()
        self._render_docked_reader()
        self._sync_scripture_highlight(_span_bounds(fragment.get("span")), force_scroll=True)
        # Keep #catena-chain-list aligned with the active fragment for clean Esc return.
        if self.current and self.current.get("chain") and not self.sort_by_verse:
            for number, run in enumerate(self.groups(self.current["chain"]["fragments"])):
                if position in run:
                    self.opened_groups.add(number)
                    break
        if zoomed:
            self._push_zoomed_reading()
        else:
            reader = self.query_one("#catena-reader", ScrollPanel)
            reader.focus()
        self.app.refresh_bindings()

    def _push_zoomed_reading(self) -> None:
        state = self.reading_state
        if state is None:
            return
        _, _, _, _, _, combined = self._build_reading_sections(
            state.fragment,
            state.body,
            full_context=state.full_context,
            english_version=state.english_version,
            english_body=state.english_body,
        )
        order = self._ordered_indices()
        count = len(order) or len((self.current.get("chain") or {}).get("fragments") or [])
        pos_in_order = order.index(state.position) if state.position in order else state.position
        snippets = state.body.get("snippets", []) if not state.body.get("missing") else []
        versions = state.fragment.get("englishVersions", [])
        title = f"{state.fragment['author']} · {state.fragment['work']} {state.fragment['locator']}".strip()
        subtitle = self._reading_subtitle(state, zoomed=True)

        def walked(step: str | None) -> None:
            if step == "next":
                self.action_step_fragment(1, zoomed=True)
            elif step == "previous":
                self.action_step_fragment(-1, zoomed=True)
            elif step == "source":
                self.action_open_source()
            elif step == "context":
                self.action_toggle_context(zoomed=True)
            elif step == "english":
                self.action_toggle_english(zoomed=True)
            else:
                # Esc / q / z returns smoothly to the docked side-by-side reader.
                if self.reading_state is not None:
                    self.query_one("#catena-reader", ScrollPanel).focus()

        self.app.push_screen(
            FragmentReading(
                title,
                combined.content(),
                subtitle,
                source=True,
                excerpts=bool(snippets),
                english=bool(versions),
                previous=pos_in_order > 0,
                following=pos_in_order + 1 < count,
            ),
            walked,
        )

    def action_zoom_reading(self) -> None:
        if self.reading_state is not None:
            self._push_zoomed_reading()

    def action_step_fragment(self, step: int, *, zoomed: bool = False) -> None:
        state = self.reading_state
        if state is None:
            return
        order = self._ordered_indices()
        if state.position not in order:
            return
        target_idx = order.index(state.position) + step
        if 0 <= target_idx < len(order):
            self.read(order[target_idx], zoomed=zoomed)

    def action_toggle_context(self, *, zoomed: bool = False) -> None:
        state = self.reading_state
        if state is None or state.body.get("missing") or not state.body.get("snippets"):
            return
        state.full_context = not state.full_context
        self._render_docked_reader(scroll_to_excerpt=state.full_context)
        self.app.refresh_bindings()
        if zoomed:
            self._push_zoomed_reading()

    def action_toggle_english(self, *, zoomed: bool = False) -> None:
        state = self.reading_state
        if state is None:
            return
        versions = state.fragment.get("englishVersions", [])
        if not versions:
            return
        if len(versions) == 1:
            if state.english_version is not None:
                state.english_version = None
                state.english_body = None
                self._render_docked_reader()
                self.app.refresh_bindings()
                if zoomed:
                    self._push_zoomed_reading()
            else:
                self.fetch_body(state.position, versions[0]["fragment"], self.current,
                                version=versions[0], zoomed=zoomed, inline_english=True)
            return
        self.choose_english(state, versions, zoomed=zoomed)

    def action_open_source(self) -> None:
        state = self.reading_state
        if state is None:
            return
        target = state.english_version["fragment"] if state.english_version is not None else state.fragment
        self.app.action_surface("sources", passage=target["id"])

    @staticmethod
    def english_offer(versions: list[dict]) -> str:
        if any(version["coverage"] == "whole" for version in versions):
            return "English version available"
        if len(versions) == 1:
            return f"English excerpt · {versions[0]['fragment']['extent']}"
        return f"{len(versions)} English excerpts available"

    @staticmethod
    def version_label(version: dict) -> str:
        return "English version · whole passage" if version["coverage"] == "whole" else "English version · excerpt"

    def choose_english(self, state: _ReadingState, versions: list[dict], *, zoomed: bool = False) -> None:
        def answered(value: str | None) -> None:
            if value is None:
                if zoomed:
                    self._push_zoomed_reading()
                return
            if value == "hide":
                state.english_version = None
                state.english_body = None
                self._render_docked_reader()
                self.app.refresh_bindings()
                if zoomed:
                    self._push_zoomed_reading()
                return
            chosen = versions[int(value)]
            self.fetch_body(state.position, chosen["fragment"], self.current,
                            version=chosen, zoomed=zoomed, inline_english=True)

        locators = [(v["fragment"]["edition"], v["fragment"]["locator"], v["fragment"]["extent"])
                    for v in versions]
        counts = Counter(locators)
        choices: list[tuple[object, object]] = []
        for index, version in enumerate(versions):
            target = version["fragment"]
            label = Ink()(target["extent"], "bold").line(" · " + target["edition"])
            label(target["locator"]).line()
            label(self.version_label(version))
            if target.get("translators"):
                label(" · " + ", ".join(target["translators"]))
            # Use distinguishing clause from M.englishVersionLabels when provided by adapter.
            model_label = (version.get("label") or "").strip()
            if model_label:
                parts = [p.strip() for p in model_label.split("·")]
                extra = " · ".join(parts[3:]) if len(parts) > 3 else ""
                if extra:
                    label.line()(extra, "$text-muted")
                elif counts[locators[index]] > 1 and version.get("basis"):
                    label.line()(version["basis"], "$text-muted")
            elif counts[locators[index]] > 1 and version.get("basis"):
                label.line()(version["basis"], "$text-muted")
            choices.append((str(index), label.content()))
        if state.english_version is not None:
            choices.append(("hide", Ink()("Hide paired English", "italic $text-muted").content()))
        self.app.push_screen(
            EnglishPick("English versions", choices, "Choose an English version to read beside the original."),
            answered,
        )
