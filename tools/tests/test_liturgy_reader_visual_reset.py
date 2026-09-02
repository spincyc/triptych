from __future__ import annotations

import hashlib
import json
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
BROWSER_HARNESS = ROOT / "tools/tests/liturgy_reader_visual_reset_browser.mjs"


def held(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def relative_luminance(color: str) -> float:
    channels = [int(color[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(first: str, second: str) -> float:
    lighter, darker = sorted(
        (relative_luminance(first), relative_luminance(second)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def instrument_tokens(css: str) -> dict[str, str]:
    root = re.search(r":root\s*\{([^}]*)\}", css, re.DOTALL)
    if root is None:
        return {}
    return dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})\s*;", root.group(1)))


class LiturgyReaderVisualResetTest(unittest.TestCase):
    def test_capture_matrix_uses_only_same_tree_prototype_and_production_pages(self) -> None:
        harness = held(BROWSER_HARNESS)
        self.assertNotIn("https://spincyc.github.io/triptych/liturgy/", harness)
        self.assertNotRegex(harness, r"before-(?:current|accepted)-")
        self.assertIn("variant: 'prototype'", harness)
        self.assertIn("variant: 'production'", harness)

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

    def test_instrument_response_safe_areas_and_print_reset_are_exact(self) -> None:
        css = held(INSTRUMENT)

        ordinary = json.loads(held(
            ROOT / "src/web/data/structure/ordinary/postconciliar.json"
        ))
        elements = [
            element
            for section in ordinary["sections"]
            for element in section["elements"]
        ]
        orate = next(
            element for element in elements
            if element["key"] == "praeparatio-donorum/orate-fratres"
        )
        latin = next(
            translation for translation in orate["translations"]
            if translation["lang"] == "la"
        )
        responses = [
            turn for turn in latin["turns"]
            if turn.get("dialogue_role") == "response"
        ]
        self.assertEqual(len(responses), 1)
        self.assertRegex(responses[0]["text"], r"^R\.\s")

        response_rule = re.search(
            r'\[data-semantic-event-id="ordinary-element/'
            r'praeparatio-donorum/orate-fratres"\]\s+'
            r'\.ordinary-turn\[data-dialogue-role="response"\]\s*>\s*'
            r'\.ordinary-turn-cue\s+\.cue-mark::before\s*\{([^}]*)\}',
            css,
            re.DOTALL,
        )
        self.assertIsNotNone(response_rule)
        self.assertIn("content: none;", response_rule.group(1))

        for rule in (
            "padding-inline: max(1rem, var(--reader-safe-left)) "
            "max(1rem, var(--reader-safe-right));",
            "padding-inline: max(1.5rem, var(--reader-safe-left)) "
            "max(1.5rem, var(--reader-safe-right));",
            "padding-inline: max(1.25rem, var(--reader-safe-left)) "
            "max(1.25rem, var(--reader-safe-right));",
        ):
            self.assertIn(rule, css)

        print_css = css[css.index("@media print"):]
        self.assertIn(
            ".reader-instrument .reader-document .ordinary-frame > "
            ".ordinary-element { display: block; }",
            print_css,
        )

    def test_instrument_contrast_and_dock_focus_are_explicit(self) -> None:
        css = held(INSTRUMENT)
        tokens = instrument_tokens(css)

        for background in (
            tokens["instrument-paper"],
            tokens["instrument-panel"],
            tokens["instrument-accent-soft"],
            "#ffffff",
        ):
            self.assertGreaterEqual(
                contrast_ratio(tokens["instrument-faint"], background),
                4.5,
                (tokens["instrument-faint"], background),
            )
        for background in (
            tokens["instrument-paper"],
            tokens["instrument-panel"],
            tokens["instrument-accent-soft"],
        ):
            self.assertGreaterEqual(
                contrast_ratio(tokens["instrument-control-line"], background),
                3.0,
                (tokens["instrument-control-line"], background),
            )

        form_controls = re.search(
            r"\.reader-instrument \.surface-field input,.*?"
            r"\.reader-instrument \.date-steps button\s*\{([^}]*)\}",
            css,
            re.DOTALL,
        )
        self.assertIsNotNone(form_controls)
        self.assertIn(
            "border: 1px solid var(--instrument-control-line);",
            form_controls.group(1),
        )
        dock_focus = re.search(
            r"\.reader-instrument \.reader-actions button:focus-visible\s*\{([^}]*)\}",
            css,
            re.DOTALL,
        )
        self.assertIsNotNone(dock_focus)
        self.assertRegex(dock_focus.group(1), r"outline-offset:\s*-[0-9.]+px")
        self.assertIn("--instrument-control-line: CanvasText;", css)

    def test_enlarged_surface_headings_keep_words_intact(self) -> None:
        css = held(INSTRUMENT)
        self.assertIn(
            "--instrument-control: clamp(44px, 3rem, 48px);",
            css,
        )
        heading = re.search(
            r"\.reader-instrument \.surface-head h2\s*\{([^}]*)\}",
            css,
            re.DOTALL,
        )
        self.assertIsNotNone(heading)
        self.assertIn("overflow-wrap: normal;", heading.group(1))
        self.assertIn("word-break: normal;", heading.group(1))
        self.assertIn(
            "padding-right: max(min(1.1rem, 20px), var(--reader-safe-right));",
            css,
        )
        self.assertIn(
            "padding-left: max(min(1.1rem, 20px), var(--reader-safe-left));",
            css,
        )

    def test_candidate_routes_have_static_privacy_and_route_neutral_identity(self) -> None:
        expected = {
            PRODUCTION_DAY: ("Day — Triptych", "Date"),
            PRODUCTION_PROPERS: ("Propers — Triptych", "Browse"),
        }
        robots = (
            '<meta name="robots" content="noindex, nofollow, noarchive, '
            'nosnippet, noimageindex">'
        )
        for path, (title, first_action) in expected.items():
            source = held(path)
            self.assertEqual(source.count(robots), 1, path.name)
            self.assertIn(f"<title>{title}</title>", source)
            self.assertNotIn('class="candidate-flag"', source)
            self.assertNotIn("internal candidate", source.lower())
            self.assertEqual(source.count('class="action-label"'), 4)
            self.assertIn(f'class="action-label">{first_action}</span>', source)
            for copy in (
                "Continuous reading of the appointed texts.",
                "Expanded notes and apparatus.",
                "Parallel editions and recensions.",
            ):
                self.assertIn(copy, source)

    def test_compatibility_closure_uses_public_propers_state_and_day_owned_apparatus(self) -> None:
        state = held(LITURGY / "reader-state.js")
        propers = held(LITURGY / "propers-reader.js")
        day = held(LITURGY / "day-reader.js")
        self.assertIn("'cycle', 'alternative', 'translation-witness'", state)
        self.assertIn("const PUBLIC_KEYS = Object.freeze", propers)
        self.assertIn("const LEGACY_KEYS = Object.freeze", propers)
        self.assertIn("publicKeys: PUBLIC_KEYS", propers)
        self.assertIn("legacyInputAliases: LEGACY_KEYS", propers)
        self.assertIn("row[PUBLIC_KEYS.cycle] = alternative.cycle", propers)
        self.assertIn("updates[PUBLIC_KEYS.translationWitness]", propers)
        self.assertIn("function reasoningApparatus(branch, rubrics, structure, result, ordinary)", day)
        self.assertIn("appendProperReasoning(body, branch, rubrics, structure, result)", day)
        self.assertIn("appendOrdinaryReasoning(body, result, ordinary)", day)
        self.assertIn("function commitResultDocuments(rows, assembled, state, showWhy)", day)
        self.assertIn("territorial-branch", day)
        self.assertNotIn("TriptychDayApparatus", day)

    def test_pages_have_unique_ids(self) -> None:
        for page in (DAY, PROPERS):
            ids = re.findall(r'\bid="([^"]+)"', held(page))
            self.assertEqual(len(ids), len(set(ids)), page.name)

    def test_visual_oracle_is_exactly_unchanged(self) -> None:
        expected = {
            "reader-visual-reset-day.html": "ff734f07b797e5706c7e62a4c890f47c32c0fbfd78bfc855f421a4123273c18d",
            "reader-visual-reset-propers.html": "638a816e189ab14b2c38dce83e8998a8cc440ebc38c025e920677a6bf8594312",
            "reader-visual-reset.css": "850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48",
            "reader-visual-reset.js": "eb1c1dd5c0c9c7076b74f2187627dc56e39963429212c0a51872df0ea98a9679",
        }
        for name, digest in expected.items():
            self.assertEqual(hashlib.sha256((LITURGY / name).read_bytes()).hexdigest(), digest, name)


if __name__ == "__main__":
    unittest.main()
