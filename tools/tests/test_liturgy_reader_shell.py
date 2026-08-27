#!/usr/bin/env python3
"""Static boundary and architecture gates for the W2 reader-shell prototype."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROTOTYPE = ROOT / "src/web/browser/liturgy/prototypes/reader-shell"
HTML = PROTOTYPE / "index.html"
CSS = PROTOTYPE / "reader-shell.css"
JS = PROTOTYPE / "reader-shell.js"
PRODUCTION = [
    "src/web/browser/liturgy/day.html",
    "src/web/browser/liturgy/day.css",
    "src/web/browser/liturgy/index.html",
    "src/web/browser/liturgy/liturgy.css",
    "src/web/browser/liturgy/liturgy.js",
    "src/web/browser/liturgy/day-missal.css",
    "src/web/browser/liturgy/reading-contents.js",
    "src/web/browser/liturgy/proper-placement-notes.js",
    "src/web/browser/liturgy/ordinary-seating.js",
    "src/web/browser/liturgy/assembly-model.js",
    "src/web/browser/shared/browser-core.css",
]


def load_public_alpha():
    path = ROOT / "tools/public-alpha"
    loader = importlib.machinery.SourceFileLoader("reader_shell_public_alpha", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not load tools/public-alpha")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ReaderShellPrototypeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = HTML.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")
        cls.js = JS.read_text(encoding="utf-8")

    def test_shared_shell_has_both_entrances_and_four_actions(self) -> None:
        self.assertEqual(self.html.count('id="reader-shell"'), 1)
        for action in ("entrance", "contents", "mode", "study"):
            self.assertIn(f'data-surface="{action}"', self.html)
        for label in ("Date &amp; edition", "Contents", "Mode", "Details", "Study"):
            self.assertIn(label, self.html)
        details_action = self.html.split('data-surface="study"', 1)[1].split("</button>", 1)[0]
        self.assertIn("Details", details_action)
        self.assertNotIn(">Study<", details_action)
        self.assertIn("config.entrance === 'day' ? 'Date & edition' : 'Browse & edition'", self.js)
        self.assertIn("'propers-formulary'", self.js)
        self.assertIn("'day-read'", self.js)

    def test_read_is_default_and_all_modes_are_accessibly_exposed(self) -> None:
        self.assertIn("const DEFAULT_STATE = 'day-read'", self.js)
        self.assertIn("const MODES = ['read', 'missal', 'study', 'compare']", self.js)
        for mode in ("read", "missal", "study", "compare"):
            self.assertIn(f'data-mode="{mode}"', self.html)
        self.assertIn('role="radiogroup"', self.html)
        self.assertIn("aria-checked", self.js)

    def test_prototype_uses_the_existing_renderer_and_not_copied_mass_html(self) -> None:
        self.assertIn("T.renderProper", self.js)
        self.assertIn("T.fetchFragments", self.js)
        self.assertIn("T.loadBibles", self.js)
        self.assertIn("../../../shared/browser-core.js", self.html)
        self.assertNotIn("<section class=\"proper\"", self.html)
        self.assertNotIn("In principio", self.html + self.js)

    def test_representative_states_are_explicit_and_synthetic_ones_are_bounded(self) -> None:
        for state in (
            "day-read", "day-postconciliar", "day-missal", "day-study",
            "propers-formulary", "propers-browse", "unavailable", "compare",
            "unresolved", "bilingual", "compare-day", "propers-postconciliar",
        ):
            self.assertIn(state, self.js)
        self.assertIn("M1_FIXTURE_ROOT = '/tools/tests/fixtures/", self.js)
        self.assertIn("Contract.validateFixture", self.js)
        self.assertIn("fixtureIdentity", self.js)
        self.assertIn("Synthetic non-public M1", self.js)
        for path in (ROOT / "src/web/data").rglob("*.json"):
            public_data = path.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn("compare-propers-synthetic-correspondence", public_data, path)
            self.assertNotIn("choice-synthetic-coequal", public_data, path)

    def test_state_parser_fails_closed_and_preserves_explicit_selections(self) -> None:
        self.assertIn("Unsupported prototype state", self.js)
        self.assertIn("No fallback was selected", self.js)
        self.assertNotIn("navigator.geolocation", self.js)
        self.assertIn("addOption(locality, 'universal', 'Universal')", self.js)
        for key in ("config.bible", "config.orations", "config.mass", "config.edition"):
            self.assertIn(key, self.js)

    def test_focus_scroll_escape_and_single_modal_contract_is_present(self) -> None:
        self.assertIn("dialog.showModal()", self.js)
        self.assertIn("dialog.show()", self.js)
        self.assertIn("surfacePresentation", self.js)
        self.assertIn("pinnedStudyAvailable", self.js)
        self.assertIn("closeOtherSurface()", self.js)
        self.assertIn("runtime.preservedY = window.scrollY", self.js)
        self.assertIn("window.scrollTo({ top: y, behavior: 'auto' })", self.js)
        self.assertIn("invoker.focus({ preventScroll: true })", self.js)
        self.assertIn("dialog.addEventListener('cancel'", self.js)
        self.assertIn("aria-expanded", self.html)

    def test_complete_read_and_reader_facing_study_boundaries_are_explicit(self) -> None:
        self.assertIn("coverage.hidden = true", self.js)
        self.assertIn("coverage.textContent = ''", self.js)
        self.assertNotIn("No blocking notices", self.js)
        self.assertNotIn("bound M1 state", self.js)
        self.assertIn("1962 Roman Missal", self.js)
        self.assertIn("Coverage is partial or unavailable", self.js)
        self.assertNotIn("JSON.stringify", self.js)
        self.assertIn("calendarOutcome", self.js)
        self.assertIn("coverageList", self.js)

    def test_every_surface_has_explicit_shrink_and_wrapping_rules(self) -> None:
        self.assertIn(".aux-surface *", self.css)
        self.assertIn("overflow-wrap: anywhere", self.css)
        self.assertIn("overflow-x: clip", self.css)
        self.assertIn("grid-template-columns: minmax(0, 1fr)", self.css)
        self.assertIn(".is-pinned-study", self.css)
        self.assertIn("position: fixed", self.css)

    def test_contents_are_semantic_location_aware(self) -> None:
        self.assertIn("[data-semantic-location]", self.js)
        self.assertIn("aria-current", self.js)
        self.assertIn("scrollIntoView", self.js)
        self.assertIn("focus({ preventScroll: true })", self.js)

    def test_both_shell_variants_have_deep_scroll_reachability(self) -> None:
        self.assertIn("const SHELLS = ['persistent', 'reveal']", self.js)
        self.assertIn("shell-hidden", self.js)
        self.assertIn('id="shell-reveal"', self.html)
        self.assertIn("position: fixed", self.css)
        self.assertIn("env(safe-area-inset-bottom", self.css)

    def test_print_and_320_reflow_rules_are_explicit(self) -> None:
        self.assertIn("@media print", self.css)
        self.assertIn(".global-actions", self.css)
        self.assertIn("display: none !important", self.css)
        self.assertIn("@media (max-width: 25rem)", self.css)
        self.assertIn("overflow-x: clip", self.css)
        self.assertIn("min-height: 2.75rem", self.css)

    def test_prototype_is_noindex_and_excluded_from_public_browser_manifest(self) -> None:
        self.assertIn('content="noindex, nofollow, noarchive"', self.html)
        pages = load_public_alpha().web_browser_pages()
        self.assertFalse(any("prototypes/reader-shell" in str(path) for path in pages))
        self.assertFalse(any("prototypes/reader-shell" in str(path) for path in pages.values()))

    def test_prototype_remains_isolated_from_production_assets(self) -> None:
        for relative in PRODUCTION:
            source = (ROOT / relative).read_text(encoding="utf-8")
            self.assertNotIn("prototypes/reader-shell", source, relative)
        for path in (HTML, CSS, JS):
            self.assertTrue(path.is_relative_to(PROTOTYPE))
        self.assertIn("../../../shared/browser-core.js", self.html)
        self.assertNotIn("reader-shell.js", self.js)

    def test_javascript_syntax(self) -> None:
        subprocess.run(["node", "--check", str(JS)], cwd=ROOT, check=True)
        subprocess.run(
            ["node", "--check", str(ROOT / "tools/tests/liturgy_reader_shell_browser.mjs")],
            cwd=ROOT, check=True,
        )


if __name__ == "__main__":
    unittest.main()
