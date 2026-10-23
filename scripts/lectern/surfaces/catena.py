"""Catena Omnia: a chapter, its dated chain and admitted undated commentary."""
from __future__ import annotations

import re

from textual import on, work
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import OptionList, Static
from textual.widgets.option_list import Option

from .. import bridge, refs
from ..dialogs import Ask, Reading
from ..repo import Refused
from ..strip import Cell, ChapterStrip
from ..surface import Surface
from ..widgets import SUPERSCRIPT, Ink, Panel, ScrollPanel, literal

ADAPTER = "catena"


def _plain(text: str) -> str:
    """The page sets fragment text `pre-line`: line breaks kept, runs of spaces
    collapsed, nothing interpreted."""
    return "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in (text or "").split("\n"))


class Catena(Surface):
    key = "3"
    label = "Catena"
    FIRST = "#catena-chain-list"
    HELP = (
        ("← / →", "previous / next chapter"),
        ("[ / ]", "previous / next book"),
        ("g", "go to a reference, e.g. 'John 1' or '1 Cor 13'"),
        ("b", "next scripture edition"),
        ("v", "next commentary voice (everything held, own language, a translation)"),
        ("enter", "open or close an author's fragments; on a fragment, read it (n / p walk the chain)"),
        ("a", "open or close every author's fragments"),
        ("click", "a bar in the strip opens that chapter"),
        ("f", "focus: scripture and chain alone; again to restore"),
    )
    BINDINGS = [
        Binding("left,h", "chapter(-1)", "previous chapter", show=False),
        Binding("right,l", "chapter(1)", "next chapter", show=False),
        Binding("left_square_bracket", "book(-1)", "previous book", show=False),
        Binding("right_square_bracket", "book(1)", "next book", show=False),
        Binding("g", "goto", "go to"),
        Binding("b", "bible", "edition"),
        Binding("v", "voice", "voice"),
        Binding("a", "expand_all", "open all authors", show=False),
    ]
    DEFAULT_CSS = """
    Catena #catena-books { width: 30; }
    Catena #catena-strip-box { height: auto; max-height: 10; }
    Catena #catena-scripture { width: 2fr; }
    Catena #catena-right { width: 3fr; }
    Catena #catena-chain { height: 2fr; }
    Catena #catena-leads { height: 1fr; min-height: 5; }
    Catena .verse-paragraph { padding: 0 0 1 0; }
    Catena .verse-paragraph.projected { border-left: dashed $catena-color 70%; padding: 0 0 1 1; }
    Catena .verse-paragraph.printed { border-left: heavy $catena-color; padding: 0 0 1 1; }
    Catena .note { color: $text-muted; }
    Catena .refusal { color: $warning; padding: 0 0 1 0; }
    """

    # A lead is not commentary, and its frame says so (catena.css:23-26):
    # a dashed rule, never the solid one the chain is drawn in.
    CSS = """
    .catena.focus #catena-books, .catena.focus #catena-strip-box, .catena.focus #catena-leads { display: none; }
    .catena.narrow #catena-books { display: none; }
    .catena #catena-leads { border: dashed $catena-color 45%; }
    .catena #catena-leads:focus, .catena #catena-leads:focus-within { border: dashed $catena-color; }
    """

    def __init__(self, **options) -> None:
        super().__init__(**options)
        self.books: list[dict] = []
        self.bibles: list[dict] = []
        self.token = "Gen"
        self.chapter = 1
        self.bible = ""
        self.voice = ""
        self.current: dict | None = None
        self.density: dict[str, list[dict]] = {}
        # Which author groups of the chain in front of the reader are open; each
        # chapter arrives with every group closed.
        self.opened_groups: set[int] = set()
        self.chain_for: tuple | None = None

    # --- building --------------------------------------------------------

    def build(self) -> None:
        self.mount(
            Horizontal(
                Panel(OptionList(id="catena-book-list"), title="books", id="catena-books"),
                Vertical(
                    Panel(ChapterStrip(id="catena-strip"), title="chapters", id="catena-strip-box"),
                    Horizontal(
                        ScrollPanel(Static("", id="catena-loading"), title="scripture", id="catena-scripture"),
                        Vertical(
                            Panel(OptionList(id="catena-chain-list"), title="chain", id="catena-chain"),
                            ScrollPanel(Static("", id="catena-lead-text"), title="acquisition list",
                                        id="catena-leads"),
                            id="catena-right",
                        ),
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
        box.mount(Static(ink.content()))

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
        found = refs.parse(ref, self.books)
        if found is None:
            self.app.notify(f"No book of this canon is called {literal(repr(ref))}.", severity="warning")
            return
        book, chapter = found
        self.go(book["token"], chapter)

    def go(self, token: str, chapter: int) -> None:
        self.token, self.chapter = token, chapter
        self.load()

    @work(thread=True, exclusive=True, group="catena-view")
    def load(self) -> None:
        token, chapter, bible, voice = self.token, self.chapter, self.bible, self.voice
        try:
            view = bridge.call(ADAPTER, "view", token, chapter, bible, voice)
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

        self.app.push_screen(Ask("go to", "A book and chapter, e.g. Gen 1, John 3, 1 Cor 13", ""), answered)

    def action_bible(self) -> None:
        if not self.bibles:
            return
        ids = [one["id"] for one in self.bibles]
        current = self.bible or ids[0]
        self.bible = ids[(ids.index(current) + 1) % len(ids)]
        self.load()

    def action_voice(self) -> None:
        if not self.current or self.current.get("problems"):
            return
        values = [option["value"] for option in self.current["voices"]]
        position = values.index(self.voice) if self.voice in values else 0
        self.voice = values[(position + 1) % len(values)]
        self.load()

    @on(OptionList.OptionSelected, "#catena-book-list")
    def picked_book(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("book-"):
            self.go(event.option.id[5:], 1)

    @on(ChapterStrip.Picked)
    def picked_chapter(self, event: ChapterStrip.Picked) -> None:
        self.go(self.token, event.chapter)

    @on(OptionList.OptionSelected, "#catena-chain-list")
    def picked_fragment(self, event: OptionList.OptionSelected) -> None:
        if event.option.id and event.option.id.startswith("frag-"):
            self.read(int(event.option.id[5:]))
        elif event.option.id and event.option.id.startswith("grp-"):
            group = int(event.option.id[4:])
            self.opened_groups ^= {group}
            self.draw_chain(keep=event.option.id)

    def action_expand_all(self) -> None:
        if not self.current or not self.current.get("chain"):
            return
        groups = range(len(self.groups(self.current["chain"]["fragments"])))
        self.opened_groups = set() if self.opened_groups >= set(groups) else set(groups)
        listing = self.query_one("#catena-chain-list", OptionList)
        keep = None
        if listing.highlighted is not None:
            keep = listing.get_option_at_index(listing.highlighted).id
        self.draw_chain(keep=keep)

    # --- drawing ---------------------------------------------------------

    def where(self) -> str:
        if not self.current or self.current.get("problems"):
            return ""
        return f"{self.current['reference']} · {self.current['bible']['label']} · {self.current['tally']['spoken']}"

    def show(self, view: dict) -> None:
        if view.get("problems"):
            good = self.current if self.current and not self.current.get("problems") else None
            if good:
                # Refused, as the page refuses it (catena.js:626); the chapter in
                # front of the reader stays, and nothing nearby is put in its place.
                self.token, self.chapter = good["book"]["token"], good["chapter"]
                said = "; ".join(f"{one['key']} = {one['value']!r}: {one['note']}" for one in view["problems"])
                self.app.notify(literal(f"{view['heading']}. {said}"), severity="warning", timeout=6)
                return
            self.current = view
            self.show_problems(view)
            return
        self.current = view
        self.bible = view["bible"]["id"]
        self.show_books(view)
        self.show_strip(view)
        self.show_scripture(view)
        self.show_chain(view)
        self.show_leads(view)
        self.app.refresh_where()

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
            f"█ fragments ({held} of {len(rows)} chapters) · · only leads · ▲ chapter {view['chapter']}"
        )

    def show_scripture(self, view: dict) -> None:
        box = self.query_one("#catena-scripture", ScrollPanel)
        box.remove_children()
        bible = view["bible"]
        box.retitle(f"{view['reference']} · {bible['label']}")
        scripture = view["scripture"]
        widgets = []
        if view["refusal"]:
            widgets.append(Static(Ink()(view["refusal"]).content(), classes="refusal"))
        if not scripture["ok"]:
            widgets.append(Static(Ink()(scripture["problem"], "bold").content(), classes="note"))
        else:
            if scripture["note"]:
                widgets.append(Static(Ink()(scripture["note"], "italic").content(), classes="note"))
            for section in scripture["sections"]:
                widgets.append(Static(Ink()(section["label"], "bold $catena-color").content()))
                for paragraph in section["paragraphs"]:
                    text = Ink()
                    for verse in paragraph["verses"]:
                        text(str(verse["number"]).translate(SUPERSCRIPT), "bold $catena-color")
                        text(verse["text"] + " ")
                    classes = "verse-paragraph"
                    if paragraph["kind"]:
                        classes += " " + paragraph["kind"]
                    widgets.append(Static(text.content(), classes=classes))
                widgets.append(Static(Ink()(section["note"], "italic").content(), classes="note"))
        box.mount_all(widgets)
        box.border_subtitle = (
            f"{scripture.get('verseCount', 0)} verses · ┃ printed ¶ · ╏ projected ¶"
            if scripture["ok"] else ""
        )
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

    def show_chain(self, view: dict) -> None:
        here = (view["book"]["token"], view["chapter"], view["voice"])
        if here != self.chain_for:
            self.chain_for = here
            self.opened_groups = set()
        self.draw_chain()

    def draw_chain(self, keep: str | None = None) -> None:
        view = self.current
        listing = self.query_one("#catena-chain-list", OptionList)
        listing.clear_options()
        box = self.query_one("#catena-chain", Panel)
        chain = view["chain"]
        if view["unfetched"]:
            listing.add_option(Option(Ink()(view["unfetched"], "bold $error").content(), disabled=True))
            box.retitle("chain")
            return
        if not view["held"]:
            box.retitle("chain")
            box.border_subtitle = ""
            for note in (chain or {}).get("notes") or []:
                listing.add_option(Option(Ink()(note, "italic").content(), disabled=True))
            return
        voice = next((option["label"] for option in view["voices"] if option["value"] == view["voice"]),
                     "Everything held")
        box.retitle(f"{chain['heading']} · {voice}")
        box.border_subtitle = "oldest first · ▸ closed ▾ open · ◌ inspected, not collated · ● verified"
        for note in chain["notes"]:
            listing.add_option(Option(Ink()(note, "italic").content(), disabled=True))
        absences = chain.get("absences")
        if absences:
            if absences.get("summary"):
                listing.add_option(Option(Ink()(absences["summary"], "bold $warning").content(), disabled=True))
            for row in absences.get("rows", []):
                said = Ink()(row["author"], "bold")
                if row.get("author") and row.get("work"):
                    said(" — ", "bold")
                said(row.get("work") or "", "bold italic")
                if row.get("reason"):
                    said.line()(row["reason"])
                if row.get("offer"):
                    said.line()(row["offer"], "italic $success")
                listing.add_option(Option(said.content(), disabled=True))
            if absences.get("unread"):
                listing.add_option(Option(Ink()(absences["unread"], "italic").content(), disabled=True))
        fragments = chain["fragments"]
        undated = False
        for number, run in enumerate(self.groups(fragments)):
            first = fragments[run[0]]
            if first.get("composition_date_status") == "unestablished" and not undated:
                listing.add_option(Option(Ink()("Composition date not established", "bold $warning").content(),
                                          disabled=True))
                box.border_subtitle = (
                    "dated oldest first · undated separate · ▸ closed ▾ open · "
                    "◌ inspected, not collated · ● verified"
                )
                undated = True
            opened = number in self.opened_groups
            words = sum(fragments[position]["text_words"] or 0 for position in run)
            heading = Ink()("▾ " if opened else "▸ ", "bold $catena-color")
            heading(first["author"] or first["work"], "bold $catena-color")
            if first["date"]:
                heading(f"  {first['date']}", "bold")
            count = f"{len(run)} fragment" + ("" if len(run) == 1 else "s")
            heading(f"  · {count} · {words:,} words", "$text-muted")
            listing.add_option(Option(heading.content(), id=f"grp-{number}"))
            if not opened:
                continue
            for position in run:
                fragment = fragments[position]
                row = Ink()("    ")
                row("● " if fragment["review"] == "verified" else "◌ ", "$text-muted")
                row(fragment["extent"], "bold")
                if fragment["spans"]:
                    row(" ↔ runs across the chapter boundary", "$warning")
                row("  ")(fragment["work"], "italic")
                row.line()("      ")
                # The language and the length are always whole; the locator takes what room is left.
                tail = f"{fragment['chip']} · {fragment['text_words']:,} words"
                room = (listing.size.width - 2 if listing.size.width else 60) - 6 - len(tail) - 3
                locator = fragment["locator"]
                if locator and locator != fragment["work"] and room >= 6:
                    row(locator if len(locator) <= room else locator[:room - 1] + "…", "$text-muted")
                    row(" · ", "$text-muted")
                row(tail, "$text-muted")
                listing.add_option(Option(row.content(), id=f"frag-{position}"))
        if keep is not None:
            try:
                listing.highlighted = listing.get_option_index(keep)
                return
            except Exception:  # noqa: BLE001 - the kept row may be gone; fall through to the first
                pass
        first = next((index for index in range(listing.option_count)
                      if not listing.get_option_at_index(index).disabled), None)
        if first is not None:
            listing.highlighted = first
            listing.call_after_refresh(listing.scroll_home, animate=False)

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
        box.border_subtitle = f"{len(leads)} leads · not commentary"
        box.scroll_home(animate=False)

    # --- reading a fragment ----------------------------------------------

    def read(self, position: int) -> None:
        if not self.current or not self.current.get("chain"):
            return
        fragments = self.current["chain"]["fragments"]
        if not 0 <= position < len(fragments):
            return
        # The chapter on screen, not one still loading behind it.
        self.fetch_body(position, fragments[position], self.current["book"]["token"],
                        self.current["chapter"], self.current["voice"])

    @work(thread=True, exclusive=True, group="catena-body")
    def fetch_body(self, position: int, fragment: dict, token: str, chapter: int, voice: str) -> None:
        try:
            body = bridge.call(ADAPTER, "body", token, chapter, voice, fragment["id"])
        except Refused as refusal:
            body = {"missing": True, "said": str(refusal)}
        self.deliver(self.open_reading, position, fragment, body)

    def open_reading(self, position: int, fragment: dict, body: dict) -> None:
        text = Ink()(fragment["author"], "bold $catena-color")
        if fragment["date"]:
            text(f"  {fragment['date']}", "bold")
        elif fragment.get("composition_date_status") == "unestablished":
            text("  Composition date not established", "bold $warning")
        text.line()
        text(fragment["work"], "italic").line(f"  {fragment['locator']}")
        text(fragment["extent"], "bold")
        if fragment["spans"]:
            text(" — runs across the chapter boundary", "$warning")
        text.line(f"  ·  {fragment['chip']}  ·  {fragment['text_words']:,} words", "$text-muted").line()
        if body.get("acknowledgement_broken"):
            text.line("The recorded acknowledgement is malformed and not shown.", "bold $warning").line()
        elif body.get("acknowledgement"):
            text("Licence: ", "bold").line(body["acknowledgement"]).line()
        said = body.get("said")
        if body.get("missing"):
            text.line(said or "The text of this fragment could not be loaded.", "bold $warning")
        else:
            text.line(_plain(said if isinstance(said, str) else ""))
        if body.get("basis"):
            text.line()("Extent — ", "bold").line(body["basis"])
        date_basis = fragment.get("composition_date_basis") or body.get("date_basis")
        if date_basis:
            text.line()("Date — ", "bold").line(date_basis)
        facts = [fragment["locator"], fragment["edition"], fragment["edition_published"]]
        if fragment["translators"]:
            facts.append("tr. " + ", ".join(fragment["translators"]))
        facts += [fragment["rights"], fragment["attribution"], fragment["rights_basis"]]
        if fragment["reviewNote"]:
            facts.append(fragment["reviewNote"])
        facts.append(f"source library: {fragment['id']}")
        text.line()("  ·  ".join(fact for fact in facts if fact), "$text-muted")

        def walked(step: str | None) -> None:
            if step == "next":
                self.read(position + 1)
            elif step == "previous":
                self.read(position - 1)
            elif step == "source":
                self.app.action_surface("sources", passage=fragment["id"])

        title = f"{fragment['author']} · {fragment['work']} {fragment['locator']}"
        self.app.push_screen(
            Reading(title, text.content(), f"{position + 1} of {len(self.current['chain']['fragments'])}"
                    " · esc close · n next · p previous · s source library", source=True),
            walked,
        )
