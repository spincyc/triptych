"""Matched commentary excerpts, side-by-side reading, drawers, and source navigation."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
TEXTUAL = importlib.util.find_spec("textual") is not None


@unittest.skipUnless(TEXTUAL, "Textual is required for commentary reading controls")
class CatenaExcerptReadingTests(unittest.IsolatedAsyncioTestCase):
    async def ready(self, app, pilot):
        from lectern.snapshot import _settle
        await _settle(app, pilot)
        return app.current()

    def fragment(self, *, ident="passage.fixture.commentary.edition.section", author="Commentator",
                 date=400, extent="Philippians 1:18–24", span=None):
        return {
            "id": ident, "author": author,
            "date": date, "work": "Commentary", "locator": "Section 3", "extent": extent,
            "span": span if span is not None else {"start": 18, "end": 24, "crossesBefore": False, "crossesAfter": False},
            "spans": False, "chip": "English translation", "text_words": 100, "language": "en",
            "edition": "Source edition", "edition_published": "1900", "translators": ["Translator"],
            "rights": "licensed-free", "attribution": "Source attribution", "rights_basis": "Fixture licence",
            "review": "inspected", "reviewNote": "inspected, not collated", "englishVersions": [],
        }

    def body(self):
        text = "Exact excerpt with ⛪ and [bold] literal text.\nSecond line."
        full = "Whole source opening.\n\n" + text + "\n\nWhole source ending."
        return {
            "missing": False, "said": full, "text": full,
            "blocks": [
                {"kind": "plain", "text": "Whole source opening.", "speaker": None, "transition": None, "notes": []},
                {"kind": "plain", "text": text, "speaker": None, "transition": None, "notes": []},
                {"kind": "plain", "text": "Whole source ending.", "speaker": None, "transition": None, "notes": []},
            ],
            "acknowledgement": "Required fixture acknowledgement", "basis": "Natural extent basis",
            "date_basis": "Composition basis", "snippets": [{
                "id": "verse-21", "extent": "Philippians 1:21", "locator": "Section 3, verse 21",
                "basis": "The source explicitly discusses verse 21 here.", "text": text,
                "blocks": [{"kind": "plain", "text": text, "speaker": None, "transition": None, "notes": []}],
            }],
        }

    def sample_view(self, fragments, *, verses="", voice="", absences=None, leads=None, by_verse_order=None):
        verses_list = [{"number": n, "text": f"Verse {n} fixture Scripture wording."} for n in range(1, 25)]
        return {
            "problems": [],
            "reference": "Philippians 1" + (f":{verses}" if verses else ""),
            "testament": "New Testament",
            "book": {"token": "Phil", "name": "Philippians", "chapters": 4},
            "chapter": 1,
            "bible": {"id": "first", "label": "Fixture Bible", "language": "en", "numbering": "vulgate"},
            "voice": voice,
            "verses": verses,
            "focusNote": f"Commentary focus: Vulgate 1:{verses}." if verses else "",
            "voices": [{"value": "", "label": "Everything held"},
                       {"value": "translation:en", "label": "English translation"}],
            "held": True,
            "tally": {"spoken": f"{len(fragments)} fragments held"},
            "refusal": "",
            "scripture": {
                "ok": True, "verseCount": len(verses_list), "canonicalAligned": True, "note": "",
                "sections": [{"label": "Philippians 1:1-24", "verseCount": len(verses_list),
                              "paragraphs": [
                                  {"kind": "", "verses": verses_list[:12]},
                                  {"kind": "projected", "verses": verses_list[12:]},
                              ], "note": ""}],
            },
            "verse_commentary": {
                "byVerse": {str(n): {"count": 1, "fragmentIds": [f["id"] for f in fragments],
                                     "authors": [f["author"] for f in fragments]} for n in range(18, 25)},
                "count": 7, "verses": list(range(18, 25)),
            },
            "chain": {
                "heading": f"{len(fragments)} fragments held here",
                "notes": [], "total": len(fragments), "shown": len(fragments),
                "absences": absences, "fragments": fragments,
                "by_verse_order": by_verse_order if by_verse_order is not None else list(range(len(fragments))),
                "authors": list(dict.fromkeys(f["author"] for f in fragments)),
                "availability": "", "contextNote": "",
            },
            "leads": leads if leads is not None else [{"who": "Lead Father", "title": "In Phil.", "when": "400"}],
            "blocked": [],
            "unfetched": "",
        }

    def set_current(self, owner, fragment):
        owner.current = self.sample_view([fragment], verses="21")
        owner.show(owner.current)

    async def test_excerpt_full_context_toggle_zoom_and_source_action_at_both_sizes(self):
        from lectern.app import TriptychApp
        from lectern.surface import shown
        from lectern.surfaces.catena import Catena, FragmentReading

        for size in ((80, 24), (140, 40)):
            with self.subTest(size=size), patch.object(Catena, "start", lambda owner: None):
                app = TriptychApp(start="catena")
                async with app.run_test(size=size) as pilot:
                    owner = await self.ready(app, pilot)
                    fragment, body = self.fragment(), self.body()
                    self.set_current(owner, fragment)
                    owner.open_reading(0, fragment, body)
                    await pilot.pause()

                    # Docked side-by-side reader keeps Scripture visible alongside commentary.
                    self.assertIs(app.screen, owner.screen)
                    reader = owner.query_one("#catena-reader")
                    scripture = owner.query_one("#catena-scripture")
                    self.assertTrue(shown(reader))
                    self.assertTrue(shown(scripture))
                    excerpt = owner._reader_text
                    self.assertIn(body["snippets"][0]["text"], excerpt)
                    self.assertIn(body["snippets"][0]["basis"], excerpt)
                    self.assertIn("Section 3, verse 21", excerpt)
                    self.assertIn(body["acknowledgement"], excerpt)
                    # Required Licence stands above the prose (Rule 9).
                    self.assertLess(excerpt.index("Licence: " + body["acknowledgement"]),
                                    excerpt.index(body["snippets"][0]["text"]))
                    self.assertNotIn("Whole source opening.", excerpt)
                    self.assertIn("c full context", reader.border_subtitle)
                    self.assertIn("s source library", reader.border_subtitle)

                    await pilot.press("c")
                    await pilot.pause()
                    full_text = owner._reader_text
                    self.assertIn("Whole source opening.", full_text)
                    self.assertIn(body["snippets"][0]["text"], full_text)
                    self.assertIn(body["acknowledgement"], full_text)
                    self.assertIn("Complete source passage", full_text)
                    self.assertIn("c excerpts", reader.border_subtitle)

                    await pilot.press("c")
                    await pilot.pause()
                    self.assertEqual(owner._reader_text, excerpt)

                    # z zooms to fullscreen FragmentReading and z returns to docked side-by-side.
                    await pilot.press("z")
                    await pilot.pause()
                    self.assertIsInstance(app.screen, FragmentReading)
                    self.assertIn("c full context", app.screen.subtitle)
                    self.assertIn(body["snippets"][0]["text"], str(app.screen.body))
                    await pilot.press("z")
                    await pilot.pause()
                    self.assertIs(app.screen, owner.screen)
                    self.assertTrue(shown(reader))

                    with patch.object(app, "action_surface") as source:
                        await pilot.press("s")
                        await pilot.pause()
                        source.assert_called_once_with("sources", passage=fragment["id"])

                    await pilot.press("escape")
                    await pilot.pause()
                    self.assertFalse(shown(reader))
                    self.assertTrue(shown(owner.query_one("#catena-chain-list")))

    async def test_without_matching_excerpts_full_fragment_remains_available(self):
        from lectern.app import TriptychApp
        from lectern.surfaces.catena import Catena

        with patch.object(Catena, "start", lambda owner: None):
            app = TriptychApp(start="catena")
            async with app.run_test(size=(80, 30)) as pilot:
                owner = await self.ready(app, pilot)
                fragment, body = self.fragment(), self.body()
                body["snippets"] = []
                self.set_current(owner, fragment)
                owner.open_reading(0, fragment, body)
                await pilot.pause()
                reader = owner.query_one("#catena-reader")
                self.assertIn("Whole source opening.", owner._reader_text)
                self.assertNotIn("Matched commentary excerpts", owner._reader_text)
                self.assertNotIn("c full context", reader.border_subtitle)
                before = owner._reader_text
                await pilot.press("c")
                await pilot.pause()
                self.assertEqual(owner._reader_text, before)

    async def test_refused_body_never_displays_excerpts_or_offers_context(self):
        from lectern.app import TriptychApp
        from lectern.surfaces.catena import Catena

        with patch.object(Catena, "start", lambda owner: None):
            app = TriptychApp(start="catena")
            async with app.run_test(size=(80, 30)) as pilot:
                owner = await self.ready(app, pilot)
                fragment, body = self.fragment(), self.body()
                body.update(missing=True, said="The excerpt metadata is invalid.")
                self.set_current(owner, fragment)
                owner.open_reading(0, fragment, body)
                await pilot.pause()
                self.assertIn(body["said"], owner._reader_text)
                self.assertNotIn(body["snippets"][0]["text"], owner._reader_text)
                self.assertFalse(owner.check_action("toggle_context", ()))

    async def test_finder_filters_chapters_opens_reference_and_cancels(self):
        from lectern.app import TriptychApp
        from lectern.catena_find import CommentaryFinder, EnglishToggle
        from lectern.surfaces.catena import Catena

        for size in ((60, 16), (140, 40)):
            with self.subTest(size=size), patch.object(Catena, "start", lambda owner: None):
                app = TriptychApp(start="catena")
                async with app.run_test(size=size) as pilot:
                    owner = await self.ready(app, pilot)
                    owner.books = [{"token": "Mark", "name": "Mark"}]
                    owner.holdings = [{**owner.books[0], "chapters": [
                        {"chapter": 1, "fragments": 9, "english": 0}, {"chapter": 10, "fragments": 4, "english": 2},
                    ]}]
                    owner.voice = "original"
                    owner.verses = "1-3"
                    owner.hidden_authors = {"Excluded author"}
                    with patch.object(owner, "load") as load:
                        await pilot.press("i")
                        self.assertIsInstance(app.screen, CommentaryFinder)
                        toggle = app.screen.query_one(EnglishToggle)
                        self.assertIn("☐", str(toggle.render()))
                        self.assertEqual(len(app.screen.matches), 2)
                        await pilot.press("tab", "space")
                        self.assertIn("☑", str(toggle.render()))
                        self.assertEqual(app.screen.matches, [("Mark", 10)])
                        await pilot.press("tab", "enter")
                        self.assertEqual((owner.token, owner.chapter, owner.verses, owner.voice), ("Mark", 10, "", ""))
                        self.assertEqual(owner.hidden_authors, {"Excluded author"})
                        load.assert_called_once()
                        await pilot.press("i", "m", "a", "r", "k", "space", "1")
                        self.assertEqual(app.screen.matches, [("Mark", 1)])
                        await pilot.press("0", "enter")
                        self.assertEqual(load.call_count, 2)
                        await pilot.press("i", "z")
                        self.assertEqual(app.screen.matches, [])
                        await pilot.press("enter", "escape")
                        self.assertEqual(load.call_count, 2)

    async def test_scripture_and_commentary_choices_are_independent_and_preserve_scroll(self):
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.surfaces.catena import Catena

        with patch.object(Catena, "start", lambda owner: None):
            app = TriptychApp(start="catena")
            async with app.run_test(size=(80, 24)) as pilot:
                owner = await self.ready(app, pilot)
                self.set_current(owner, self.fragment())
                owner.bibles = [{"id": "first", "label": "Edition One", "languageName": "English",
                                 "numberingLabel": "hebrew numbering, psalm titles unnumbered"},
                                {"id": "second", "label": "Edition Two", "languageName": "Latin",
                                 "numberingLabel": "vulgate numbering"}]
                owner.bible, owner.voice = "first", ""
                scripture = owner.query_one("#catena-scripture")
                scripture.scroll_to(y=4, animate=False)
                await pilot.pause()
                saved_scroll = scripture.scroll_y
                with patch.object(owner, "load") as load:
                    await pilot.press("B")
                    self.assertIsInstance(app.screen, Pick)
                    self.assertIn("Latin · vulgate numbering", str(app.screen.options[1][1]))
                    await pilot.press("down", "down", "enter")
                    self.assertEqual((owner.bible, owner.voice), ("second", ""))
                    self.assertIsNotNone(owner._preserve_on_bible_switch)
                    self.assertEqual(owner._preserve_on_bible_switch[0], float(saved_scroll))
                    await pilot.press("V", "down", "down", "enter")
                    self.assertEqual((owner.bible, owner.voice), ("second", "translation:en"))
                    await pilot.press("b", "v")
                    self.assertEqual((owner.bible, owner.voice), ("first", ""))
                    await pilot.press("B", "escape", "V", "escape")
                    self.assertEqual(load.call_count, 4)

    async def test_linked_version_toggles_inline_beside_original_and_deduplicates_basis(self):
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.surfaces.catena import Catena
        from textual.widgets import OptionList

        original = dict(self.fragment(), chip="Latin — the author’s own", language="la",
                        translators=[], edition="Latin edition")
        english = dict(self.fragment(), id="passage.fixture.english", edition="English edition")
        original["englishVersions"] = [{
            "fragment": english, "basis": "These sections correspond.", "coverage": "excerpt",
            "label": "English excerpt · Philippians 1:18–24",
        }]
        original_body = dict(self.body(), snippets=[], said="Original wording.", blocks=[
            {"kind": "plain", "text": "Original wording.", "speaker": None, "transition": None, "notes": []}
        ])
        english_body = dict(self.body(), snippets=[], said="Translated wording.",
                            basis="These sections correspond.", acknowledgement="English credit.", blocks=[
            {"kind": "plain", "text": "Translated wording.", "speaker": None, "transition": None, "notes": []}
        ])
        with patch.object(Catena, "start", lambda owner: None):
            app = TriptychApp(start="catena")
            async with app.run_test(size=(120, 36)) as pilot:
                owner = await self.ready(app, pilot)
                self.set_current(owner, original)
                owner.current.update(book={"token": "Phil", "name": "Philippians", "chapters": 4},
                                     chapter=1, voice="original", verses="21")
                with patch("lectern.bridge.call", return_value=english_body) as fetch:
                    owner.open_reading(0, original, original_body)
                    await pilot.pause()
                    await pilot.press("p", "n")
                    await pilot.pause()
                    self.assertEqual(owner.reading_state.position, 0)

                    # Press e: shows paired English INLINE directly below the original Latin.
                    await pilot.press("e")
                    await self.ready(app, pilot)
                    fetch.assert_called_once_with("catena", "body", "Phil", 1, "original", english["id"], "21")
                    combined = owner._reader_text
                    for expected in ("Original wording.", "Translated wording.", "English credit.", english["id"],
                                     "English edition", "Translated by Translator", "English version · excerpt",
                                     "These sections correspond."):
                        self.assertIn(expected, combined)
                    # Basis identical to version["basis"] is never printed twice.
                    self.assertEqual(combined.count("These sections correspond."), 1)

                    # Press e again: toggles paired English off without refetching.
                    await pilot.press("e")
                    await pilot.pause()
                    self.assertIn("Original wording.", owner._reader_text)
                    self.assertNotIn("Translated wording.", owner._reader_text)
                    self.assertEqual(fetch.call_count, 1)

                    # Multiple English versions open EnglishPick with option 0 pre-highlighted and distinguishing clause.
                    second = dict(english, id="passage.fixture.second", extent="Philippians 1:30")
                    original["englishVersions"].append({
                        "fragment": second, "basis": "Complete correspondence.", "coverage": "whole",
                        "label": "Whole passage in English · Philippians 1:30 · Section 3 · Complete correspondence.",
                    })
                    await pilot.press("e")
                    await pilot.pause()
                    self.assertIsInstance(app.screen, Pick)
                    self.assertEqual(app.screen.query_one(OptionList).highlighted, 0)
                    self.assertIn(english["extent"], str(app.screen.options[0][1]))
                    self.assertIn(second["extent"], str(app.screen.options[1][1]))
                    self.assertIn("Complete correspondence.", str(app.screen.options[1][1]))
                    await pilot.press("escape")
                    await pilot.pause()
                    self.assertNotIn("Translated wording.", owner._reader_text)

                    # Choose second option (down once from pre-highlighted option 0, then enter).
                    await pilot.press("e", "down", "enter")
                    await self.ready(app, pilot)
                    self.assertIn("English version · whole passage", owner._reader_text)
                    with patch.object(app, "action_surface") as source:
                        await pilot.press("s")
                        await pilot.pause()
                        source.assert_called_once_with("sources", passage=second["id"])

    async def test_structured_catena_aurea_blocks_and_drawers_and_tab_order(self):
        from lectern.app import TriptychApp
        from lectern.surface import shown
        from lectern.surfaces.catena import Catena

        frag_a = self.fragment(ident="passage.a", author="Author One", date=380,
                               extent="Philippians 1:18-20",
                               span={"start": 18, "end": 20, "crossesBefore": False, "crossesAfter": False})
        frag_b = self.fragment(ident="passage.b", author="Author Two", date=420,
                               extent="Philippians 1:1-3",
                               span={"start": 1, "end": 3, "crossesBefore": False, "crossesAfter": False})
        absences = {
            "summary": "1 work standing here has no English this project may publish",
            "rows": [{"author": "Ambrose", "work": "Hexameron", "finding": "in-copyright",
                      "stands": "closed", "reason": "Only a 1961 translation exists.", "offer": ""}],
        }
        view = self.sample_view([frag_a, frag_b], verses="1-20", voice="translation:en",
                                absences=absences, by_verse_order=[1, 0])
        structured_body = {
            "missing": False, "said": "Ver. 1: Gospel lemma.\n\nBede: It goes on: Commentary [ed. note: cf. Jerome].",
            "blocks": [
                {"kind": "lemma", "text": "Ver. 1: Gospel lemma.", "speaker": None, "transition": None, "notes": []},
                {"kind": "commentary", "text": "Bede: It goes on: Commentary [ed. note: cf. Jerome].",
                 "speaker": [0, 5], "transition": [6, 17], "notes": [[29, 49]]},
            ],
            "acknowledgement": "", "basis": "Natural extent.", "date_basis": "", "snippets": [],
        }

        with patch.object(Catena, "start", lambda owner: None):
            app = TriptychApp(start="catena")
            async with app.run_test(size=(120, 36)) as pilot:
                owner = await self.ready(app, pilot)
                owner.show(view)
                await pilot.pause()

                # where() reports matching count under a verse filter.
                self.assertIn("· 2 matching", owner.where())

                # Leads hidden by default when fragments exist; L toggles leads drawer on/off.
                self.assertFalse(shown(owner.query_one("#catena-leads")))
                await pilot.press("L")
                await pilot.pause()
                self.assertTrue(shown(owner.query_one("#catena-leads")))
                await pilot.press("L")
                await pilot.pause()
                self.assertFalse(shown(owner.query_one("#catena-leads")))

                # Absences live in scrollable drawer toggled by 'a' (never trapped in disabled rows).
                self.assertFalse(shown(owner.query_one("#catena-absences")))
                await pilot.press("a")
                await pilot.pause()
                self.assertTrue(shown(owner.query_one("#catena-absences")))
                self.assertEqual(app.focused.id, "catena-absences")
                self.assertIn("Only a 1961 translation exists.",
                              str(owner.query_one("#catena-absences-text").render()))
                await pilot.press("escape")
                await pilot.pause()
                self.assertFalse(shown(owner.query_one("#catena-absences")))
                self.assertEqual(app.focused.id, "catena-chain-list")

                # 1 Tab switches directly between chain and Scripture (and back in 1 Tab).
                await pilot.press("tab")
                await pilot.pause()
                self.assertEqual(app.focused.id, "catena-scripture")
                await pilot.press("tab")
                await pilot.pause()
                self.assertEqual(app.focused.id, "catena-chain-list")

                # o toggles By verse ordering (frag_b v.1-3 comes before frag_a v.18-20).
                await pilot.press("o")
                await pilot.pause()
                self.assertTrue(owner.sort_by_verse)
                self.assertEqual(owner.query_one("#catena-chain-list").highlighted_option.id, "frag-1")

                # Structured Catena Aurea lemma/speaker/transition/notes render inside docked reader.
                owner.open_reading(1, frag_b, structured_body)
                await pilot.pause()
                self.assertIn("Ver. 1: Gospel lemma.", owner._reader_text)
                self.assertIn("Bede:", owner._reader_text)
                self.assertIn("[ed. note: cf. Jerome]", owner._reader_text)
                self.assertTrue(owner.query_one("#catena-reader").query(".reader-lemma"))


if __name__ == "__main__":
    unittest.main()
