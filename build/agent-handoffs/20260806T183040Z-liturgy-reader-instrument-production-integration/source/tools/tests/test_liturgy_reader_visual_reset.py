from __future__ import annotations

import hashlib
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
LITURGY = ROOT / "src/web/browser/liturgy"
DAY = LITURGY / "reader-visual-reset-day.html"
PROPERS = LITURGY / "reader-visual-reset-propers.html"
CSS = LITURGY / "reader-visual-reset.css"
SCRIPT = LITURGY / "reader-visual-reset.js"
INSTRUMENT = LITURGY / "reader-instrument.css"
PRODUCTION_DAY = LITURGY / "day-reader.html"
PRODUCTION_PROPERS = LITURGY / "propers-reader.html"


def held(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class LiturgyReaderVisualResetTest(unittest.TestCase):
    def test_prototypes_are_unlinked_noindex_pages(self) -> None:
        for path in (DAY, PROPERS):
            source = held(path)
            self.assertIn(
                '<meta name="robots" content="noindex, nofollow, noarchive, '
                'nosnippet, noimageindex">', source
            )
            self.assertIn("Unlinked visual-direction prototype · noindex", source)
        for public in (LITURGY / "day.html", LITURGY / "index.html"):
            self.assertNotIn("reader-visual-reset", held(public))

    def test_day_reuses_the_accepted_production_paths(self) -> None:
        scripts = re.findall(r'<script src="([^"]+)"></script>', held(DAY))
        self.assertEqual(
            scripts,
            [
                "../shared/browser-core.js",
                "assembly-model.js",
                "ordinary-seating.js",
                "day.js",
                "reader-state.js",
                "reader-state-adapters.js",
                "reader-shell.js",
                "day-reader.js",
                "reader-visual-reset.js",
            ],
        )
        self.assertNotIn("renderProper", held(SCRIPT))
        self.assertNotIn("renderOrdinary", held(SCRIPT))
        self.assertNotIn("semantic seat", held(SCRIPT).lower())

    def test_propers_reuses_the_accepted_production_paths(self) -> None:
        scripts = re.findall(r'<script src="([^"]+)"></script>', held(PROPERS))
        self.assertEqual(
            scripts,
            [
                "../shared/browser-core.js",
                "ordinary-seating.js",
                "reader-state.js",
                "reader-state-adapters.js",
                "reader-shell.js",
                "propers-reader.js",
                "reader-visual-reset.js",
            ],
        )
        source = held(PROPERS)
        self.assertEqual(source.count('data-mode="read"'), 1)
        self.assertNotIn('data-mode="missal"', source)
        self.assertNotIn("Study", source)
        self.assertNotIn("Compare", source)

    def test_three_directions_share_one_dom_and_component_layer(self) -> None:
        script = held(SCRIPT)
        css = held(CSS)
        self.assertIn("new Set(['folio', 'instrument', 'reader'])", script)
        for design in ("folio", "instrument", "reader"):
            self.assertIn(f'[data-design="{design}"]', css)
        for page in (DAY, PROPERS):
            source = held(page)
            self.assertEqual(source.count('data-reader-shell'), 1)
            self.assertIn('href="reader-visual-reset.css"', source)
            self.assertIn('src="reader-visual-reset.js"', source)

    def test_shared_shell_actions_have_local_svg_icons_and_text_names(self) -> None:
        script = held(SCRIPT)
        self.assertIn("createElementNS('http://www.w3.org/2000/svg'", script)
        self.assertNotIn("fetch(", script)
        for page in (DAY, PROPERS):
            source = held(page)
            actions = re.findall(
                r'<button[^>]+data-reader-action="([^"]+)"[^>]+data-icon="([^"]+)"[^>]*>(.*?)</button>',
                source,
                re.DOTALL,
            )
            self.assertEqual(len(actions), 4)
            for action, icon, body in actions:
                self.assertTrue(action)
                self.assertTrue(icon)
                self.assertRegex(body, r'class="action-label">[^<]+</span>')

    def test_instrument_finish_is_presentation_only_and_source_honest(self) -> None:
        script = held(SCRIPT)
        css = held(CSS)
        self.assertIn("normalizeInstrumentCoverage", script)
        self.assertIn("coverageNotice.replaceChildren(...uncompiled.childNodes)", script)
        self.assertIn("ordinary-absence-inline", script)
        self.assertNotIn("Some appointed text", script)
        self.assertIn('[data-design="instrument"] .reader-progress { display: none; }', css)
        self.assertIn('[data-design="instrument"] .ordinary-absence-inline', css)
        self.assertIn('border-left: 2px solid var(--vr-ink);', css)
        self.assertIn('background: var(--vr-panel);', css)

    def test_instrument_shell_has_continuous_edge_and_extreme_reflow_rules(self) -> None:
        css = held(CSS)
        self.assertIn('container: reader-shell / inline-size;', css)
        self.assertIn('@media (max-width: 71.999rem)', css)
        self.assertIn('@container reader-shell (max-width: 18rem)', css)
        self.assertIn('grid-template-columns: repeat(2, minmax(0, 1fr));', css)
        self.assertIn('white-space: nowrap;', css)
        instrument_edge = re.search(
            r'@media \(max-width: 71\.999rem\).*?'
            r'\.reader-visual-reset\[data-design="instrument"\] \.reader-actions \{(.*?)\n  \}',
            css,
            re.DOTALL,
        )
        self.assertIsNotNone(instrument_edge)
        rule = instrument_edge.group(1)
        self.assertIn('border-radius: 0;', rule)
        self.assertIn('background: var(--vr-panel);', rule)
        self.assertIn('box-shadow: none;', rule)

    def test_accepted_instrument_has_one_scoped_production_presentation_seam(self) -> None:
        css = held(INSTRUMENT)
        self.assertIn("Accepted Liturgical Instrument presentation", css)
        self.assertIn(".reader-instrument", css)
        self.assertIn("container: reader-shell / inline-size", css)
        self.assertIn('@container reader-shell (max-width: 18rem)', css)
        self.assertIn("ordinary-absence-inline", css)
        self.assertNotIn('[data-design=', css)
        for page in (PRODUCTION_DAY, PRODUCTION_PROPERS):
            source = held(page)
            self.assertIn('class="reader-shell reader-instrument"', source)
            self.assertIn('href="reader-instrument.css"', source)
            self.assertEqual(source.count('class="reader-masthead"'), 1)
            self.assertEqual(source.count('class="action-label"'), 4)
        self.assertIn("composeInstrumentAbsences", held(LITURGY / "day-reader.js"))
        self.assertIn("shellRoot.dataset.readerMode", held(LITURGY / "day-reader.js"))
        self.assertIn("coverageNotice.replaceChildren(...uncompiled.childNodes)", held(LITURGY / "propers-reader.js"))

    def test_pages_have_unique_ids(self) -> None:
        for page in (DAY, PROPERS):
            ids = re.findall(r'\bid="([^"]+)"', held(page))
            self.assertEqual(len(ids), len(set(ids)), page.name)

    def test_accepted_and_public_boundaries_are_exactly_unchanged(self) -> None:
        expected = {
            "day.html": "bc5a98de6b718431f3b91e6a133bb847c2dcdf4d21fce6f45aae3ad4984de868",
            "index.html": "f630f4a66f3f525144336f183b1485c698030c7531ff679375b3a7aa00150c65",
            "reader-shell.js": "e17ccd767c016facc3d03820f5c0c1e71ab166f5a9c7a86de95245e0b87966a9",
            "reader-shell.css": "e7195cd86ed4fc4a8455e97369702239eb22d709a13d3d8462d7759c01fe814a",
            "reader-state.js": "86fcb653738089a569f0f9747d5092e4e51fd2f4ee0ae7b4e7fe9a0c5f5a7cdc",
            "reader-state-adapters.js": "ec655b52e850152a1a3034b09fbc36b828000a5edc9d01b7b8d98dfaeea96bcb",
            "ordinary-seating.js": "67917f4888764f1aac097d291df5e655fb485d89219fda56ffba9a25aee993ba",
        }
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256((LITURGY / name).read_bytes()).hexdigest(), digest, name)


if __name__ == "__main__":
    unittest.main()
