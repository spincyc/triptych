"""Regression suite for Lane D TUI Cold Review remediation & parity invariants."""
from __future__ import annotations

import datetime as dt
import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

TEXTUAL = importlib.util.find_spec("textual") is not None
NODE = shutil.which("node") is not None


class MissalPresentationUnitTests(unittest.TestCase):
    def test_compline_theme_has_accessible_accent_and_monochrome_footer_keys(self) -> None:
        from lectern.theme import THEMES

        compline = next(t for t in THEMES if t.name == "triptych-compline")
        self.assertEqual(compline.variables["day-color"], "#b8b8cc")
        self.assertEqual(compline.variables["propers-color"], "#b8b8cc")
        self.assertEqual(compline.variables["footer-key-foreground"], "#ffffff")
        self.assertEqual(compline.variables["hotkey"], "#ffffff")

    def test_rubric_brackets_never_bleed_onto_metadata_credits_or_statutory_notices(self) -> None:
        from lectern.missal import blocks
        from lectern.widgets import Ink

        sample = [
            {
                "tag": "p",
                "classes": ["ordinary-element", "is-rubric", "text-side-label"],
                "runs": [{"text": "Latin · own · qualified public domain", "classes": ["is-rubric", "text-side-label"]}],
            },
            {
                "tag": "p",
                "classes": ["ordinary-element", "is-rubric", "composed"],
                "runs": [{"text": "Sacerdos paratus cum ingreditur ad altare.", "classes": ["is-rubric", "composed"]}],
            },
            {
                "tag": "p",
                "classes": ["ordinary-element", "is-rubric", "composed-note", "ordinary-reading-source"],
                "runs": [{"text": "Source: Missale Romanum 1962", "classes": ["is-rubric", "composed-note", "ordinary-reading-source"]}],
            },
            {
                "tag": "p",
                "classes": ["ordinary-element", "is-rubric", "composed-note", "latin-rights-qualification"],
                "runs": [{"text": "Published on a qualified basis (publication policy priority 6).", "classes": ["is-rubric", "latin-rights-qualification"]}],
            },
        ]
        ink = blocks(Ink(), sample, missal_mode=True)
        lines = ink.content().plain.splitlines()
        self.assertEqual(lines[0], "Latin · own · qualified public domain")
        self.assertEqual(lines[1], "[ Sacerdos paratus cum ingreditur ad altare. ]")
        self.assertEqual(lines[2], "Source: Missale Romanum 1962")
        # Verbatim statutory notice preserved without crimson rubric brackets!
        self.assertEqual(lines[3], "Published on a qualified basis (publication policy priority 6).")
        self.assertFalse(any(p[0].startswith("[") and "priority 6" in str(ink.content().plain)
                             for p in ink.parts if isinstance(p, tuple) and "Latin" in p[0]))

    def test_composed_label_hidden_in_both_read_and_missal_modes(self) -> None:
        from lectern.missal import blocks
        from lectern.widgets import Ink

        sample = [{"tag": "p", "classes": ["composed-label"], "runs": [
            {"text": "Composed text — not scripture", "classes": ["composed-label"]},
        ]}]
        for mode in (False, True):
            with self.subTest(missal_mode=mode):
                out = blocks(Ink(), sample, missal_mode=mode).content().plain
                self.assertNotIn("Composed text — not scripture", out)

    def test_complete_ratios_omitted_and_partial_ratios_retained(self) -> None:
        from lectern.missal import format_coverage_notice, is_complete_notice
        from lectern.surfaces.propers import _format_browse_counts

        complete = "Latin Propers: 4/4 represented texts, 4/4 uses available. 6 Bible reconstructions."
        formatted = format_coverage_notice(complete)
        self.assertNotIn("4/4", formatted)
        self.assertIn("all represented texts available", formatted)
        self.assertTrue(is_complete_notice(complete))

        partial = "English Propers: 1/4 represented texts, 1/4 uses available. Exact target wording remains incomplete."
        self.assertIn("1/4", format_coverage_notice(partial))
        self.assertFalse(is_complete_notice(partial))

        browse_complete = _format_browse_counts([
            {"lang": "la", "available": 3, "occurrences": 3},
            {"lang": "en", "available": 3, "occurrences": 3},
        ])
        self.assertEqual(browse_complete, "LA · EN")
        browse_partial = _format_browse_counts([
            {"lang": "la", "available": 3, "occurrences": 3},
            {"lang": "en", "available": 1, "occurrences": 3},
        ])
        self.assertEqual(browse_partial, "LA · EN 1/3")

    def test_external_href_renders_osc8_link_and_ctrl_o_hint(self) -> None:
        from lectern.missal import blocks
        from lectern.widgets import Ink

        sample = [{"tag": "p", "classes": [], "runs": [
            {"text": "Read in the U.S. English Missal", "tags": ["p", "a"],
             "classes": ["published-prayer-link"], "href": "https://rmhealey.com/docs/RMU/#A1"},
        ]}]
        ink = blocks(Ink(), sample)
        plain = ink.content().plain
        self.assertIn("Read in the U.S. English Missal", plain)
        self.assertIn("[Ctrl+O]", plain)
        self.assertTrue(any(isinstance(part, tuple) and 'link="https://rmhealey.com/docs/RMU/#A1"' in part[1]
                            for part in ink.parts))

    def test_dl_dt_dd_renders_aligned_two_column_rows(self) -> None:
        from lectern.missal import blocks
        from lectern.widgets import Ink

        sample = [
            {"tag": "dt", "classes": ["study-facts"], "runs": [{"text": "Edition", "classes": []}]},
            {"tag": "dd", "classes": ["study-facts"], "runs": [{"text": "roman-1962", "classes": []}]},
            {"tag": "dt", "classes": ["study-facts"], "runs": [{"text": "Availability reason", "classes": []}]},
            {"tag": "dd", "classes": ["study-facts"], "runs": [{"text": "unavailable", "classes": []}]},
            {"tag": "dt", "classes": ["study-facts"], "runs": [{"text": "Unavailable state", "classes": []}]},
            {"tag": "dd", "classes": ["study-facts"], "runs": [{"text": "unavailable", "classes": []}]},
        ]
        lines = blocks(Ink(), sample).content().plain.splitlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("Edition", lines[0])
        self.assertIn("roman-1962", lines[0])
        self.assertIn("Availability reason", lines[1])

    def test_inline_choices_use_bullets_instead_of_colliding_digits(self) -> None:
        from lectern.missal import choices
        from lectern.widgets import Ink

        view = {
            "state": {"ordinary": False},
            "unresolvedChoices": [{
                "id": "proper-form:all-souls",
                "reason": "Three Masses are appointed.",
                "options": [{"id": "first"}, {"id": "second"}],
            }],
            "mass": {"forms": [{"id": "first", "name": "First Mass"}, {"id": "second", "name": "Second Mass"}]},
        }
        plain = choices(Ink(), view).content().plain
        self.assertIn("• First Mass", plain)
        self.assertIn("• Second Mass", plain)
        self.assertNotIn("1. First Mass", plain)
        self.assertNotIn("   first", plain)

    def test_raw_audit_json_and_sha256_hidden_by_default_and_revealed_with_toggle(self) -> None:
        from lectern.missal import filter_study_audit

        raw = [{"tag": "p", "classes": ["composed-note"], "runs": [{
            "text": 'Helpful scholarly note. No donor fanout is performed in this batch. '
                    '[{"source_word_1_based": 20, "target": "x"}] wraps and final LF, SHA256 6393934d1234567890abcdef.',
            "classes": ["composed-note"],
        }]}]
        hidden = filter_study_audit(raw, show_audit=False)
        shown = filter_study_audit(raw, show_audit=True)
        hidden_text = "".join(r["text"] for b in hidden for r in b["runs"])
        shown_text = "".join(r["text"] for b in shown for r in b["runs"])
        self.assertIn("Helpful scholarly note.", hidden_text)
        self.assertNotIn("source_word_1_based", hidden_text)
        self.assertNotIn("6393934d1234567890abcdef", hidden_text)
        self.assertIn("source_word_1_based", shown_text)
        self.assertIn("6393934d1234567890abcdef", shown_text)


@unittest.skipUnless(TEXTUAL and NODE, "Textual and node are required")
class ColdReviewIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def settle(self, app, pilot) -> None:
        from lectern.snapshot import _settle

        await _settle(app, pilot)

    async def test_60x16_day_shows_title_and_opening_liturgical_text_above_fold(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _text

        app = TriptychApp(start="day", intent={"calendar": "roman-1962", "date": "2026-11-29"},
                          today=dt.date(2026, 11, 29))
        async with app.run_test(size=(60, 16)) as pilot:
            await self.settle(app, pilot)
            drawn = _text(app, styles=False)
            self.assertIn("First Sunday of Advent", drawn)
            self.assertIn("Introit", drawn)
            self.assertTrue("To thee" in drawn or "Ad te levavi" in drawn or "Psalm" in drawn, drawn)

    async def test_wide_bilingual_missal_renders_side_by_side_without_rubric_bleed(self) -> None:
        from lectern.app import TriptychApp
        from lectern.snapshot import _text

        app = TriptychApp(
            start="day",
            intent={"calendar": "roman-1962", "date": "2026-05-24", "ordinary": True,
                    "orations": "en", "ordinaryLang": "en", "textDisplay": "latin-and-selected"},
            today=dt.date(2026, 5, 24),
        )
        async with app.run_test(size=(140, 40)) as pilot:
            await self.settle(app, pilot)
            drawn = _text(app, styles=False)
            self.assertIn("│", drawn)
            self.assertIn("Latin", drawn)
            self.assertIn("English", drawn)
            self.assertIn("English Ordinary", drawn)
            self.assertIn("Bilingual", drawn)
            self.assertNotIn("[ Latin", drawn)
            self.assertNotIn("[ Source:", drawn)
            self.assertNotIn("[ Published on a qualified basis", drawn)

    async def test_contents_has_zero_raw_ordinary_ids_and_marks_here_at_top(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.snapshot import _text

        app = TriptychApp(
            start="day",
            intent={"calendar": "roman-1962", "date": "2026-05-24", "ordinary": True},
            today=dt.date(2026, 5, 24),
        )
        async with app.run_test(size=(140, 40)) as pilot:
            await self.settle(app, pilot)
            await pilot.press("i")
            await self.settle(app, pilot)
            self.assertIsInstance(app.screen, Pick)
            labels = [label.plain if hasattr(label, "plain") else str(label)
                      for _, label in app.screen.options]
            self.assertTrue(labels)
            self.assertFalse(any("ordinary-element/" in lbl for lbl in labels), labels[:15])
            self.assertTrue(any("· here" in lbl for lbl in labels), labels[:5])
            self.assertIn("· here", _text(app, styles=False))

    async def test_settings_modal_does_not_clip_at_140x40_and_choose_deduplicates_proper_choice(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import Pick
        from lectern.snapshot import _text
        from textual.widgets import OptionList

        app = TriptychApp(
            start="day",
            intent={"calendar": "postconciliar", "date": "2027-02-26", "ordinary": True},
            today=dt.date(2027, 2, 26),
        )
        async with app.run_test(size=(140, 40)) as pilot:
            await self.settle(app, pilot)
            await pilot.press("comma")
            await self.settle(app, pilot)
            self.assertIsInstance(app.screen, Pick)
            self.assertIsNotNone(app.screen.query_one(OptionList).highlighted)
            drawn = _text(app, styles=False)
            self.assertIn("Read source texts", drawn)
            self.assertIn("[Ctrl+O]", drawn)
            self.assertIn("open", drawn)
            await pilot.press("escape", "s")
            await self.settle(app, pilot)
            self.assertIsInstance(app.screen, Pick)
            self.assertTrue(app.screen.sections)
            labels = [str(lbl) for _, lbl in app.screen.options]
            pray_matches = [lbl for lbl in labels if "Pray (optional)" in lbl]
            self.assertEqual(len(pray_matches), 1, labels)
            self.assertTrue(any("IV" in lbl and "unresolved" in lbl for lbl in labels), labels)

    async def test_read_mode_study_omits_ordinary_advisory_and_uses_contextual_tabs(self) -> None:
        from lectern.app import TriptychApp
        from lectern.dialogs import StudyDialog

        app = TriptychApp(
            start="day",
            intent={"calendar": "roman-1962", "date": "2026-05-24"},
            today=dt.date(2026, 5, 24),
        )
        async with app.run_test(size=(140, 40)) as pilot:
            await self.settle(app, pilot)
            await pilot.press("d")
            await self.settle(app, pilot)
            self.assertIsInstance(app.screen, StudyDialog)
            body = app.screen.body.plain
            self.assertNotIn("A pre-1955 lay hand missal's Ordinary", body)
            self.assertIn("Edition", body)
            await pilot.press("2")
            await self.settle(app, pilot)
            self.assertIn("Introit", app.screen.body.plain)

    async def test_wide_navigation_rail_stays_open_when_picking_formulary_and_folds_in_day_compare(self) -> None:
        from lectern.app import TriptychApp
        from lectern.surface import shown

        app = TriptychApp(start="propers", intent={"calendar": "roman-1962"}, today=dt.date(2026, 5, 24))
        async with app.run_test(size=(140, 40)) as pilot:
            await self.settle(app, pilot)
            await pilot.press("enter")
            await self.settle(app, pilot)
            self.assertTrue(shown(app.query_one("#propers-left")))
            self.assertIsNotNone(app.current().reading)

        app2 = TriptychApp(start="day", intent={"calendar": "roman-1962", "date": "2026-10-25"},
                           today=dt.date(2026, 10, 25))
        async with app2.run_test(size=(140, 40)) as pilot:
            await self.settle(app2, pilot)
            self.assertTrue(shown(app2.query_one("#day-left")))
            await pilot.press("v")
            await self.settle(app2, pilot)
            self.assertFalse(shown(app2.query_one("#day-left")))

    async def test_topbar_preserves_surface_accent_and_month_keyboard_preview_works(self) -> None:
        from lectern.app import TriptychApp
        from lectern.month import Month
        from textual.widgets import Static

        app = TriptychApp(start="day", intent={"calendar": "postconciliar", "date": "2026-11-13"},
                          today=dt.date(2026, 11, 13))
        async with app.run_test(size=(140, 40)) as pilot:
            await self.settle(app, pilot)
            svg = app.export_screenshot()
            self.assertIn("#c9a227", svg.lower())
            # IGMR 363 weekday uses quiet · rather than alarming ?
            month_widget = app.query_one(Month)
            mark = app.current().mark(dt.date(2026, 11, 13))
            self.assertIsNotNone(mark)
            self.assertEqual(mark[0], "·")
            month_widget.focus()
            await pilot.pause()
            await pilot.press("right", "right")
            await pilot.pause()
            self.assertEqual(month_widget.cursor, dt.date(2026, 11, 15))
            preview = str(app.query_one("#day-preview", Static).render())
            self.assertIn("Sun 15 Nov", preview)
            self.assertIn("Thirty-third", preview)

    async def test_propers_browse_christological_header_60x16_rows_and_where(self) -> None:
        from lectern.app import TopBar, TriptychApp
        from textual.widgets import OptionList

        app = TriptychApp(start="propers", intent={"calendar": "roman-1962"})
        async with app.run_test(size=(60, 16)) as pilot:
            await self.settle(app, pilot)
            self.assertIn("1962 typical edition", app.query_one(TopBar).where)
            listing = app.query_one("#propers-list", OptionList)
            self.assertEqual(str(listing.get_option_at_index(0).prompt).strip().lower(), "christological")
            self.assertGreaterEqual(listing.region.height, 4)

    async def test_preference_persistence_round_trips_and_defers_to_explicit_intent(self) -> None:
        from lectern.app import TriptychApp
        from lectern.surfaces.day import Day

        with tempfile.TemporaryDirectory() as tmp:
            prefs_file = Path(tmp) / "lectern.json"
            app1 = TriptychApp(start="day", intent={"date": "2026-11-29"},
                               today=dt.date(2026, 11, 29), persist=True, prefs_path=prefs_file)
            async with app1.run_test(size=(120, 40)) as pilot:
                await self.settle(app1, pilot)
                await pilot.press("T", "o")
                await self.settle(app1, pilot)
                self.assertEqual(app1.theme, "triptych-vellum")
                self.assertEqual(app1.query_one(Day).orations, "en")
            self.assertTrue(prefs_file.is_file())

            # Second session restores saved theme & orations when not overridden by intent.
            app2 = TriptychApp(start="day", intent={"date": "2026-11-29"},
                               today=dt.date(2026, 11, 29), persist=True, prefs_path=prefs_file)
            async with app2.run_test(size=(120, 40)) as pilot:
                await self.settle(app2, pilot)
                self.assertEqual(app2.theme, "triptych-vellum")
                self.assertEqual(app2.query_one(Day).orations, "en")

            # Explicit URL/CLI intent overrides saved preferences (Vision Invariant #6).
            app3 = TriptychApp(start="day", intent={"date": "2026-11-29", "orations": "la"},
                               theme="triptych-compline", today=dt.date(2026, 11, 29),
                               persist=True, prefs_path=prefs_file)
            async with app3.run_test(size=(120, 40)) as pilot:
                await self.settle(app3, pilot)
                self.assertEqual(app3.theme, "triptych-compline")
                self.assertEqual(app3.query_one(Day).orations, "la")


if __name__ == "__main__":
    unittest.main()
