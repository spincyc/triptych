"""Static boundary checks for the isolated Wave 1 corpus prototype.

These tests intentionally use only the Python standard library.  The prototype
is review evidence, not a public browser route, and its isolation is part of the
artifact's contract rather than a convention reviewers must remember.
"""

from __future__ import annotations

from html.parser import HTMLParser
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
PROTOTYPE = ROOT / "src/web/browser/prototypes/corpus-wave-1"
HTML = PROTOTYPE / "index.html"
CSS = PROTOTYPE / "prototype.css"
JS = PROTOTYPE / "prototype.js"
MATRIX = ROOT / "tools/tests/fixtures/corpus-wave1-prototype-matrix-v1.json"
HARNESS = ROOT / "tools/tests/corpus_wave1_prototype_browser.mjs"

ROBOTS = "noindex, nofollow, noarchive, nosnippet, noimageindex"
VIEWPORTS = {(1440, 900), (1024, 768), (768, 1024), (393, 852), (320, 852)}
SURFACE_ROUTE_PREFIXES = {
    "home": "/",
    "publications": "/texts/",
    "reader": "/web/",
    "catena": "/catena/",
    "sources": "/sources/",
}
EMULATIONS = {
    "default", "text-200", "reflow-400", "keyboard", "forced-colors",
    "reduced-motion", "no-js", "print", "zoom-400",
}


class ContractParser(HTMLParser):
    """Retain the small amount of HTML structure needed by this contract."""

    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.visible_text: list[str] = []
        self._suppressed = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, dict(attrs)))
        if tag in {"script", "style", "template"}:
            self._suppressed += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "template"} and self._suppressed:
            self._suppressed -= 1

    def handle_data(self, data: str) -> None:
        if not self._suppressed and data.strip():
            self.visible_text.append(" ".join(data.split()))

    def matching(self, tag: str, **attrs: str) -> list[dict[str, str | None]]:
        return [
            held
            for held_tag, held in self.tags
            if held_tag == tag
            and all(held.get(name) == value for name, value in attrs.items())
        ]


def load_public_alpha():
    path = ROOT / "tools/public-alpha"
    loader = importlib.machinery.SourceFileLoader("wave1_public_alpha", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not load tools/public-alpha")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def collect_viewports(value: object) -> set[tuple[int, int]]:
    """Find explicit width/height pairs without coupling to matrix row layout."""

    found: set[tuple[int, int]] = set()
    if isinstance(value, dict):
        width = value.get("width")
        height = value.get("height")
        if isinstance(width, int) and isinstance(height, int):
            found.add((width, height))
        for child in value.values():
            found.update(collect_viewports(child))
    elif isinstance(value, list):
        for child in value:
            found.update(collect_viewports(child))
    elif isinstance(value, str):
        for width, height in re.findall(r"(?<!\d)(\d{3,4})\s*[x×]\s*(\d{3,4})(?!\d)", value):
            found.add((int(width), int(height)))
    return found


class CorpusWave1PrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        for path in (HTML, CSS, JS, MATRIX, HARNESS):
            if not path.is_file():
                raise AssertionError(f"missing Wave 1 prototype asset: {path.relative_to(ROOT)}")
        cls.html = HTML.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")
        cls.js = JS.read_text(encoding="utf-8")
        cls.matrix_text = MATRIX.read_text(encoding="utf-8")
        cls.matrix = json.loads(cls.matrix_text)
        cls.harness = HARNESS.read_text(encoding="utf-8")
        cls.parser = ContractParser()
        cls.parser.feed(cls.html)

    def test_assets_are_exactly_local_and_dependency_free(self) -> None:
        stylesheet_hrefs = [
            attrs.get("href")
            for tag, attrs in self.parser.tags
            if tag == "link" and "stylesheet" in (attrs.get("rel") or "").split()
        ]
        script_sources = [
            attrs.get("src")
            for tag, attrs in self.parser.tags
            if tag == "script" and attrs.get("src") is not None
        ]
        self.assertEqual(stylesheet_hrefs, ["prototype.css"])
        self.assertEqual(script_sources, ["prototype.js"])
        self.assertFalse(self.parser.matching("base"))
        self.assertFalse(self.parser.matching("style"))
        self.assertFalse(
            [
                attrs
                for tag, attrs in self.parser.tags
                if tag == "script" and attrs.get("src") is None
            ]
        )

        for tag, attrs in self.parser.tags:
            for name in ("href", "src"):
                value = attrs.get(name)
                if value is None:
                    continue
                self.assertFalse(
                    value.startswith(("/", "http:", "https:", "//", "data:")),
                    f"{tag} {name} is not a local relative reference: {value}",
                )

        combined = "\n".join((self.html, self.css, self.js)).lower()
        for forbidden in (
            "@font-face", "@import", "fonts.googleapis", "fonts.gstatic",
            "font-awesome", "material-icons", "bootstrap", "tailwind",
            "react", "vue.js", "angular", "jquery",
        ):
            self.assertNotIn(forbidden, combined)
        self.assertNotRegex(self.css, r"\burl\s*\(")

    def test_review_boundary_is_exact_visible_and_noindex(self) -> None:
        robots = [
            attrs.get("content")
            for tag, attrs in self.parser.tags
            if tag == "meta" and (attrs.get("name") or "").casefold() == "robots"
        ]
        self.assertEqual(robots, [ROBOTS])
        titles = [
            " ".join(text.split())
            for text in re.findall(r"<title>(.*?)</title>", self.html, flags=re.DOTALL)
        ]
        self.assertEqual(len(titles), 1)
        self.assertIn("prototype", titles[0].casefold())

        visible = " ".join(self.parser.visible_text)
        self.assertIn("Wave 1 design prototype", visible)
        self.assertIn("not production", visible.casefold())
        self.assertRegex(
            self.html,
            r'data-(?:prototype|fixture|review)-boundary="[^"]+"',
        )

    def test_prototype_has_no_canonical_or_social_identity(self) -> None:
        for tag, attrs in self.parser.tags:
            rel = set((attrs.get("rel") or "").casefold().split())
            self.assertFalse(tag == "link" and "canonical" in rel)
            if tag == "meta":
                name = (attrs.get("name") or "").casefold()
                prop = (attrs.get("property") or "").casefold()
                self.assertFalse(name.startswith("twitter:"), name)
                self.assertFalse(prop.startswith("og:"), prop)
        lowered = self.html.casefold()
        for forbidden in ("spincyc.github.io", "sitemap", "rel=\"canonical\""):
            self.assertNotIn(forbidden, lowered)

    def test_prototype_cannot_collide_with_a_public_mapping(self) -> None:
        tool = load_public_alpha()
        mappings = (tool.web_browser_pages(), tool.web_data_files(), tool.site_pages())
        marker = "prototypes/corpus-wave-1"
        for mapping in mappings:
            for key, value in mapping.items():
                self.assertNotIn(marker, str(key))
                self.assertNotIn(marker, str(value))
        self.assertNotIn(PROTOTYPE / "index.html", tool.web_browser_pages().values())

    def test_prototype_javascript_has_no_runtime_or_navigation_side_channel(self) -> None:
        for forbidden in (
            r"\bfetch\s*\(", r"\bXMLHttpRequest\b", r"\bWebSocket\b",
            r"\bEventSource\b", r"\blocalStorage\b", r"\bsessionStorage\b",
            r"\bindexedDB\b", r"\bdocument\s*\.\s*cookie\b",
            r"\bhistory\s*\.", r"\bpushState\b", r"\breplaceState\b",
            r"\bserviceWorker\b", r"\bsendBeacon\b", r"\bimport\s*\(",
        ):
            self.assertNotRegex(self.js, forbidden)
        self.assertNotRegex(self.js, r"https?://|['\"]//")

    def test_public_and_archetype_terminology_is_accepted(self) -> None:
        visible = " ".join(self.parser.visible_text)
        for term in (
            "Publications", "Independent treatment", "Parallel treatment",
            "Reader", "Catalogue", "Instrument", "Catena Omnia",
            "Source Library",
        ):
            self.assertIn(term, visible)
        for rejected in (
            "Every Document", "parallel provider treatment", "provider edition",
            "Parallel treatments",
        ):
            self.assertNotIn(rejected.casefold(), visible.casefold())
        for term in ("Independent treatment", "Parallel treatment"):
            self.assertIn(term, self.js)
        self.assertNotIn("Parallel treatments", self.js)

    def test_matrix_names_all_routes_and_required_viewports(self) -> None:
        self.assertIsInstance(self.matrix, dict)
        self.assertEqual(self.matrix.get("version"), 1)
        assets = self.matrix.get("prototype_assets")
        self.assertIsInstance(assets, dict)
        self.assertEqual(
            assets.get("css"),
            "src/web/browser/prototypes/corpus-wave-1/prototype.css",
        )
        self.assertEqual(
            assets.get("javascript"),
            "src/web/browser/prototypes/corpus-wave-1/prototype.js",
        )
        cases = self.matrix.get("cases")
        self.assertIsInstance(cases, list)
        self.assertTrue(cases)

        ids: set[str] = set()
        surfaces: set[str] = set()
        phases_by_surface: dict[str, set[str]] = {}
        emulations: set[str] = set()
        core: set[tuple[str, str, int, int]] = set()
        for case in cases:
            self.assertIsInstance(case, dict)
            held_id = case.get("id")
            self.assertIsInstance(held_id, str)
            self.assertRegex(held_id, r"^[a-z0-9][a-z0-9-]*$")
            self.assertNotIn(held_id, ids)
            ids.add(held_id)

            surface = case.get("surface")
            self.assertIn(surface, SURFACE_ROUTE_PREFIXES)
            surfaces.add(surface)
            phase = case.get("phase")
            self.assertIn(phase, {"before", "after"})
            phases_by_surface.setdefault(surface, set()).add(phase)

            route = case.get("route")
            self.assertIsInstance(route, str)
            if surface == "home":
                self.assertRegex(route, r"^/(?:[?#].*)?$")
            else:
                self.assertTrue(route.startswith(SURFACE_ROUTE_PREFIXES[surface]))
            self.assertFalse(route.startswith("//"))
            self.assertFalse(route.startswith("/triptych"))
            self.assertNotIn("prototypes/corpus-wave-1", route)

            viewport = case.get("viewport")
            self.assertIsInstance(viewport, dict)
            self.assertIn((viewport.get("width"), viewport.get("height")), VIEWPORTS)

            emulation = case.get("emulation", "default")
            self.assertIn(emulation, EMULATIONS)
            emulations.add(emulation)
            if emulation == "reflow-400":
                self.assertEqual(viewport.get("width"), 320)
            if emulation in {"print", "zoom-400"}:
                self.assertEqual(surface, "reader")

            if held_id.startswith(
                (f"before-{surface}-default-", f"after-{surface}-default-")
            ):
                core.add(
                    (surface, phase, viewport.get("width"), viewport.get("height"))
                )

            self.assertIsInstance(case.get("actions", []), list)
            self.assertIsInstance(case.get("expect", {}), dict)

        self.assertEqual(surfaces, set(SURFACE_ROUTE_PREFIXES))
        self.assertEqual(emulations, EMULATIONS)
        self.assertTrue(VIEWPORTS.issubset(collect_viewports(cases)))
        for surface, phases in phases_by_surface.items():
            self.assertEqual(phases, {"before", "after"}, surface)
        expected_core = {
            (surface, phase, width, height)
            for surface in SURFACE_ROUTE_PREFIXES
            for phase in ("before", "after")
            for width, height in VIEWPORTS
        }
        self.assertTrue(expected_core.issubset(core))
        self.assertTrue(any(case.get("emulation") == "print" for case in cases))
        self.assertTrue(any(case.get("emulation") == "zoom-400" for case in cases))
        detail_case = next(
            case for case in cases
            if case.get("id") == "after-publications-detail-keyboard-393x852"
        )
        self.assertEqual(detail_case.get("emulation"), "keyboard")
        self.assertIn("close_and_restore", detail_case.get("expect", {}))
        self.assertEqual(len(detail_case["expect"].get("exact_text", [])), 3)
        self.assertTrue(
            any(action.get("op") == "click" for action in detail_case.get("actions", []))
        )
        deep_reader = next(
            case for case in cases
            if case.get("id") == "after-reader-deep-heading-1024x768"
        )
        deep_id = "current-governance-is-a-ladder-not-one-permission"
        self.assertTrue(deep_reader.get("route", "").endswith(f"#{deep_id}"))
        self.assertEqual(deep_reader["expect"].get("ready"), f"#{deep_id}")
        self.assertEqual(deep_reader["expect"].get("useful"), f"#{deep_id}")
        self.assertEqual(deep_reader["expect"].get("current_contents"), deep_id)
        reader_no_js = next(
            case for case in cases if case.get("id") == "after-reader-no-js-393x852"
        )
        inherited_overlay = reader_no_js["expect"].get("inherited_overlay")
        self.assertEqual(
            inherited_overlay.get("assertions"),
            ["reader-record-visible-provider", "reader-record-visible-pdf"],
        )
        self.assertIn("JavaScript overlay", inherited_overlay.get("reason", ""))

    def test_harness_is_bound_to_the_prototype_and_fixed_matrix(self) -> None:
        self.assertIn(
            "tools/tests/fixtures/corpus-wave1-prototype-matrix-v1.json",
            self.harness,
        )
        self.assertIn("prototype_assets.css", self.harness)
        self.assertIn("prototype_assets.javascript", self.harness)
        self.assertIn("/__wave1/prototype.css", self.harness)
        self.assertIn("/__wave1/prototype.js", self.harness)
        self.assertIn("reader-colophon-action-target", self.harness)
        self.assertIn('[data-wave-action="colophon"]', self.harness)
        self.assertIn(
            "normalizedExtracted.indexOf(normalizedExpected, orderedCursor)",
            self.harness,
        )
        self.assertIn("normalizePrintText(extracted)", self.harness)
        self.assertIn("normalizePrintText(text)", self.harness)
        self.assertIn(r"\p{Dash_Punctuation}", self.harness)
        self.assertIn("IPV4_LOOPBACK_OCTETS", self.harness)
        self.assertIn("IPV4_LOOPBACK_OCTETS.join", self.harness)
        self.assertNotIn(".".join(("0", "0", "0", "0")), self.harness)
        self.assertIn("mkdtemp", self.harness)
        self.assertNotRegex(self.harness, r"listen\(\s*(?:80|443|8000|8080)\b")

        imports = re.findall(r"from\s+['\"]([^'\"]+)['\"]", self.harness)
        self.assertTrue(imports)
        for module in imports:
            self.assertTrue(module.startswith("node:"), module)

    def test_protected_liturgy_assets_are_not_referenced(self) -> None:
        combined = "\n".join(
            (self.html, self.css, self.js, self.matrix_text, self.harness)
        )
        self.assertNotIn("src/web/browser/liturgy/", combined)
        self.assertIn("governedPrototypeRoute", self.harness)
        self.assertIn("protectedSurfaceAssertions", self.harness)
        self.assertIn("'/liturgy/', '/liturgy/day.html'", self.harness)

    def test_css_covers_accessibility_media_without_masking_overflow(self) -> None:
        for required in (
            "@media (forced-colors: active)",
            "@media (prefers-reduced-motion: reduce)",
            "@media print",
            ":focus-visible",
        ):
            self.assertIn(required, self.css)

        qualifier = r"(?:[.#][\w-]+|\[[^\]]+\])*"
        global_selector = (
            rf"(?::root|html{qualifier}|body{qualifier}|\*|"
            rf"html{qualifier}\s+body{qualifier}|html{qualifier}\s+\*)"
        )
        global_overflow_mask = re.compile(
            rf"^\s*{global_selector}\s*(?:,\s*{global_selector}\s*)*"
            r"\{[^{}]*\boverflow(?:-x)?\s*:\s*(?:hidden|clip)\b",
            flags=re.IGNORECASE | re.DOTALL | re.MULTILINE,
        )
        self.assertIsNone(global_overflow_mask.search(self.css))

    def test_javascript_syntax_when_node_is_available(self) -> None:
        if shutil.which("node") is None:
            self.skipTest("node is not installed")
        for path in (JS, HARNESS):
            with self.subTest(path=path.relative_to(ROOT)):
                subprocess.run(
                    ["node", "--check", str(path)],
                    cwd=ROOT,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )


if __name__ == "__main__":
    unittest.main()
