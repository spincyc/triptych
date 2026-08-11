#!/usr/bin/env python3
"""Static contract for the isolated A3/A4 corpus-foundation prototype."""

from __future__ import annotations

import importlib.machinery
import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROTOTYPE = ROOT / "src/web/browser/prototypes/corpus-foundation"
HTML = PROTOTYPE / "index.html"
CSS = PROTOTYPE / "prototype.css"
JS = PROTOTYPE / "prototype.js"


class ContractParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs)))

    def matching(self, tag: str, **attrs: str) -> list[dict[str, str | None]]:
        return [
            held
            for held_tag, held in self.tags
            if held_tag == tag and all(held.get(name) == value for name, value in attrs.items())
        ]


def load_public_alpha():
    path = ROOT / "tools/public-alpha"
    loader = importlib.machinery.SourceFileLoader("corpus_foundation_public_alpha", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not load tools/public-alpha")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class CorpusFoundationPrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = HTML.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")
        cls.js = JS.read_text(encoding="utf-8")
        cls.parser = ContractParser()
        cls.parser.feed(cls.html)

    def test_all_assets_exist_and_are_local(self) -> None:
        self.assertTrue(HTML.is_file())
        self.assertTrue(CSS.is_file())
        self.assertTrue(JS.is_file())
        self.assertEqual(re.findall(r'<link[^>]+href="([^"]+)"', self.html), ["prototype.css"])
        self.assertEqual(re.findall(r'<script[^>]+src="([^"]+)"', self.html), ["prototype.js"])
        for value in re.findall(r'(?:href|src)="([^"]+)"', self.html):
            self.assertFalse(value.startswith(("/", "http:", "https:", "//", "data:")), value)

    def test_review_boundary_is_visible_and_machine_readable(self) -> None:
        self.assertIn('data-review-query-keys="surface panel"', self.html)
        self.assertIn('data-fixture-boundary="synthetic-review-v1"', self.html)
        for phrase in (
            "A3/A4 prototype",
            "Synthetic review fixtures",
            "not a public route or data contract",
            "surface and panel query values are review-only",
        ):
            self.assertIn(phrase, self.html)
        self.assertEqual(self.html.count("Illustrative prototype state—not a corpus claim."), 3)

    def test_prototype_is_noindex_and_outside_public_artifact(self) -> None:
        self.assertIn(
            'content="noindex, nofollow, noarchive, nosnippet, noimageindex"',
            self.html,
        )
        pages = load_public_alpha().web_browser_pages()
        files = load_public_alpha().web_data_files()
        for mapping in (pages, files):
            self.assertFalse(any("prototypes/corpus-foundation" in str(item) for item in mapping))
            self.assertFalse(any("prototypes/corpus-foundation" in str(item) for item in mapping.values()))

    def test_one_shell_and_three_complete_archetypes(self) -> None:
        self.assertEqual(len(self.parser.matching("header", **{"data-prototype-shell": "single"})), 1)
        self.assertEqual(len(self.parser.matching("main", id="prototype-main")), 1)
        self.assertEqual(len(self.parser.matching("footer", **{"class": "corpus-footer"})), 1)
        for name in ("reader", "catalogue", "instrument"):
            matches = self.parser.matching("article", **{"data-archetype": name})
            matches += self.parser.matching("section", **{"data-archetype": name})
            self.assertEqual(len(matches), 1, name)
            self.assertEqual(matches[0].get("data-prototype-fixture"), "synthetic-review-v1")

    def test_navigation_and_dialogs_have_names(self) -> None:
        names = {attrs.get("aria-label") for tag, attrs in self.parser.tags if tag == "nav"}
        self.assertTrue({"Global corpus", "Mobile global corpus", "Project"}.issubset(names))
        for dialog_id, label in (
            ("menu-dialog", "menu-dialog-title"),
            ("jump-dialog", "jump-dialog-title"),
            ("related-dialog", "related-dialog-title"),
        ):
            matches = self.parser.matching("dialog", id=dialog_id)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0].get("aria-labelledby"), label)
        self.assertEqual(self.html.count('data-open-dialog="jump-dialog"'), 1)
        self.assertGreaterEqual(self.html.count('data-open-dialog="related-dialog"'), 2)

    def test_global_places_and_provider_language_are_exact(self) -> None:
        for place in (
            "Home", "Publications", "Sources", "Scripture", "Liturgy",
            "History", "Law", "Commentary",
        ):
            self.assertIn(f">{place}<", self.html)
        self.assertIn("parallel provider treatment", self.html.lower())
        self.assertNotIn("provider edition", self.html.lower())

    def test_object_levels_and_availability_are_not_flattened(self) -> None:
        for label in ("Work", "Edition", "Artifact", "Passage"):
            self.assertIn(f"<dt>{label}</dt>", self.html)
        for state in ("PDF only", "Text withheld", "Rights", "not acquired"):
            self.assertIn(state, self.html)
        self.assertIn("a hash would prove bytes, not authority", self.html)

    def test_jump_is_a_bounded_synthetic_filter(self) -> None:
        self.assertIn("This is not production global search.", self.html)
        self.assertIn('role="status" aria-live="polite"', self.html)
        self.assertEqual(self.js.count("params.get("), 2)
        self.assertIn('const surfaces = ["reader", "catalogue", "instrument"]', self.js)
        self.assertIn('const panels = ["none", "menu", "jump", "related"]', self.js)
        for forbidden in ("fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "history.", "pushState", "replaceState", "serviceWorker", "import("):
            self.assertNotIn(forbidden, self.js)
        self.assertEqual(self.js.count("window.location.search"), 1)

    def test_modal_and_focus_contract_is_explicit(self) -> None:
        for expected in (
            "showModal()", "dialog.close()", 'dialog[open]',
            "dialogInvokers", "focus({ preventScroll: true })",
        ):
            self.assertIn(expected, self.js)
        self.assertIn("if (event.target === dialog) dialog.close()", self.js)

    def test_visual_system_has_required_roles_and_adaptive_states(self) -> None:
        for token in (
            "--tp-canvas", "--tp-surface", "--tp-text", "--tp-accent",
            "--tp-focus", "--tp-reader", "--tp-instrument", "--tp-catalogue",
            "--tp-target: 2.75rem",
        ):
            self.assertIn(token, self.css)
        for state in (
            "@media (max-width: 30rem)",
            "@media (prefers-reduced-motion: reduce)",
            "@media (forced-colors: active)",
            "@media print",
            ":focus-visible",
        ):
            self.assertIn(state, self.css)
        self.assertNotIn("border-radius: 1", self.css)
        self.assertNotIn("linear-gradient", self.css)

    def test_javascript_syntax(self) -> None:
        subprocess.run(["node", "--check", str(JS)], cwd=ROOT, check=True)
        subprocess.run(
            ["node", "--check", str(ROOT / "tools/tests/corpus_foundation_prototype_browser.mjs")],
            cwd=ROOT,
            check=True,
        )


if __name__ == "__main__":
    unittest.main()
