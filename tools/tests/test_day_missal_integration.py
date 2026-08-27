#!/usr/bin/env python3
"""Focused architecture, state, and isolation gates for Day Missal mode."""

from __future__ import annotations

import json
import subprocess
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LITURGY = ROOT / "src/web/browser/liturgy"
HTML = LITURGY / "day-reader.html"
JS = LITURGY / "day-reader.js"
CSS = LITURGY / "day-reader.css"
PUBLIC_RENDERER = LITURGY / "day.js"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DayMissalIntegrationTests(unittest.TestCase):
    def test_read_default_and_bounded_mode_surface(self) -> None:
        html = text(HTML)
        self.assertIn('data-mode="read"', html)
        self.assertIn('data-mode="missal"', html)
        self.assertEqual(html.count('aria-disabled="true" disabled'), 2)
        self.assertIn("Study", html)
        self.assertIn("Compare", html)
        source = text(JS)
        self.assertIn("runtime.mode = normalized.state.requestedMode", source)
        self.assertIn("navigate({ mode: 'missal' }", source)
        self.assertIn("navigate({ mode: 'read' }", source)

    def test_one_production_renderer_and_one_seating_engine_own_the_frame(self) -> None:
        candidate = text(JS)
        public = text(PUBLIC_RENDERER)
        self.assertIn("const OrdinaryRenderer = window.TriptychOrdinaryRenderer", candidate)
        self.assertIn("OrdinaryRenderer.renderSemanticFrame(result.events", candidate)
        self.assertIn("OrdinaryRenderer.renderElement(raw, ordinary)", candidate)
        self.assertIn("T.renderProper", candidate)
        self.assertIn("window.TriptychOrdinaryRenderer", public)
        self.assertIn("renderSemanticFrame(massEvents(shown, placed)", public)
        self.assertNotIn("function seatPropers", candidate)
        self.assertNotIn("function massEvents", candidate)
        self.assertNotIn("innerHTML", candidate)

    def test_state_language_option_and_why_rules_are_explicit(self) -> None:
        source = text(JS)
        for token in (
            "validateExplicitVariants", "invalid-explicit-variant",
            "the explicit option is not applicable", "ordinary-lang",
            "function reasoningApparatus(branch, rubrics, structure, result, ordinary)",
            "appendProperReasoning(body, branch, rubrics, structure, result)",
            "appendOrdinaryReasoning(body, result, ordinary)",
            "Boolean(normalized.state.apparatus && normalized.state.apparatus.why)",
            "apparatus.className = 'day-reasoning'", "renderOrdinaryChoice",
            "window.OrdinarySeating.chosenOption", "group.options || []",
        ):
            self.assertIn(token, source)
        self.assertIn("return mode === 'study' ? ['mode=' + mode] : [];", source)
        self.assertIn("Compare deliberately does not", source)
        self.assertNotIn("recognized.why === '1'", source)
        self.assertNotIn("recognized.rubrics === '1'", source)
        self.assertNotIn("group.options[0]", source)
        self.assertNotIn("Object.keys(group", source)
        self.assertNotIn(".sort()[0]", source)

    def test_real_edition_structures_remain_distinct_and_source_default_is_explicit(self) -> None:
        roman = json.loads((ROOT / "src/web/data/structure/ordinary/roman-1962.json").read_text())
        post = json.loads((ROOT / "src/web/data/structure/ordinary/postconciliar.json").read_text())
        roman_elements = sum(len(section["elements"]) for section in roman["sections"])
        post_elements = sum(len(section["elements"]) for section in post["sections"])
        self.assertEqual((len(roman["sections"]), roman_elements, len(roman["slots"])), (6, 195, 9))
        self.assertEqual((len(post["sections"]), post_elements, len(post["slots"])), (7, 47, 11))
        self.assertEqual(roman.get("variants", []), [])
        group = post["variants"][0]
        self.assertEqual(group["group"], "eucharistic-prayer")
        self.assertEqual([row["id"] for row in group["options"]], ["ep-i", "ep-ii", "ep-iii", "ep-iv"])
        self.assertEqual([row["id"] for row in group["options"] if row.get("default")], ["ep-i"])

    def test_semantic_location_races_contents_and_details_have_owned_paths(self) -> None:
        candidate = text(JS)
        shell = text(LITURGY / "reader-shell.js")
        for token in (
            "captureModeLocation", "nearestProperLocation", "restorePendingNavigation",
            "modeStartedAt", "derivations", "if (!row || serial !== runtime.serial) return",
            "if (!rendered.length || serial !== runtime.serial) return",
            "renderContext", "sourceHooks", "data-semantic-location",
            "ordinary-option", "pendingNavigation", "committedRender",
            "(optionGroup || optionTarget).scrollIntoView({ block: 'start', behavior: 'auto' })",
        ):
            self.assertIn(token, candidate if token not in {"data-semantic-location"} else shell)
        self.assertIn("captureSemanticLocation", shell)
        self.assertIn("restoreSemanticLocation", shell)
        for branch_token in (
            "function locationPrefix(branch, multiple)",
            "function resultStateForBranch(state, branch, multiple)",
            "const territorial = /^territory\\/[^/]+\\//.exec(eventId)",
            "runtime.branches.find(function (row) { return row.prefix === prefix; })",
            "id: (prefix || '') + event.id",
            "group.dataset.optionBranch === (held.focus.branch || '')",
        ):
            self.assertIn(branch_token, candidate)
        self.assertNotIn("JSON.stringify(runtime", candidate)
        self.assertNotIn("hook.kind + ': '", candidate)

    def test_every_outcome_has_one_deterministic_mode_commit_path(self) -> None:
        source = text(JS)
        self.assertIn("function commitOutcomePresentation(presentation)", source)
        self.assertIn("function requestedModeOf(parsed)", source)
        self.assertIn("mode ? modeLabel(mode) : 'Unavailable'", source)
        self.assertIn("outcomeClass: 'unrenderable'", source)
        self.assertIn("outcomeClass: 'deferred'", source)
        self.assertIn("outcomeClass: hasUnresolved ? 'unresolved' : 'ready'", source)
        self.assertIn("function commitResultDocuments(rows, assembled, state, showWhy)", source)
        self.assertIn("function failedBranchDocument(branch, prefix, error)", source)
        self.assertIn("if (branchFailures === rendered.length)", source)
        self.assertIn("throw branchErrors[0]", source)
        self.assertIn("invalid: 'explicit state rejected'", source)
        self.assertNotIn("Read candidate limitation", source)

    def test_accessible_continuous_and_print_presentation_is_bounded(self) -> None:
        css = text(CSS)
        instrument = text(LITURGY / "reader-instrument.css")
        html = text(HTML)
        for token in (
            ".ordinary-choice", "min-height: 2.75rem", "overflow-x: clip",
            "@media (max-width: 25rem)", "@media print", ".ordinary-choice { display: none; }",
        ):
            self.assertIn(token, css)
        self.assertIn("role=\"radiogroup\"", html)
        self.assertIn("aria-live=\"polite\"", html)
        self.assertIn("day.css", html)
        self.assertIn("day-missal.css", html)
        self.assertIn("day.js", html)
        self.assertIn("ordinary-absence-inline", instrument)
        self.assertIn("composeInstrumentAbsences", text(JS))
        self.assertIn("shellRoot.dataset.readerMode", text(JS))

    def test_public_routes_renderer_and_test_fixtures_are_isolated(self) -> None:
        for relative in ("day.html", "index.html"):
            source = text(LITURGY / relative)
            self.assertIn("data-reader-shell", source)
            self.assertNotIn("reader-visual-reset", source)

        public_renderer = text(PUBLIC_RENDERER)
        self.assertIn("window.TriptychOrdinaryRenderer", public_renderer)
        self.assertIn("renderSemanticFrame", public_renderer)
        for path in (ROOT / "src/web/data").rglob("*.json"):
            payload = text(path)
            self.assertNotIn("synthetic-cycle-order", payload, path.as_posix())
            self.assertNotIn("candidate-contract-only", payload, path.as_posix())

    def test_candidate_tracking_is_distinct_and_accepted(self) -> None:
        with (ROOT / "promised-deliverables.toml").open("rb") as handle:
            ledger = tomllib.load(handle)
        rows = [row for row in ledger["deliverables"] if row["id"] ==
                "liturgy-day-missal-w3-candidate-2026-08-05"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["state"], "complete")
        self.assertEqual(rows[0]["owner"], "src/web/browser/liturgy/day-reader.html")
        self.assertEqual(
            {requirement["status"] for requirement in rows[0]["requirements"]},
            {"pass"},
        )
        ids = [row["id"] for row in ledger["deliverables"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_javascript_syntax_and_browser_harness(self) -> None:
        for path in (JS, PUBLIC_RENDERER, LITURGY / "reader-shell.js"):
            subprocess.run(["node", "--check", str(path)], cwd=ROOT, check=True)
        subprocess.run(
            ["node", "--check", str(ROOT / "tools/tests/day_reader_integration_browser.mjs")],
            cwd=ROOT, check=True,
        )

    def test_browser_harness_waits_for_settled_scroll_target_and_focus(self) -> None:
        harness = text(ROOT / "tools/tests/day_reader_integration_browser.mjs")
        for token in (
            "async function waitForVisualSettlement",
            "requiredStableFrames: options.requiredStableFrames || 5",
            "requestAnimationFrame(resolve)",
            "targetIntersectsViewport",
            "activeElementIntersectsViewport",
            "Visual settlement timed out",
            "prefers-reduced-motion",
        ):
            self.assertIn(token, harness)
        self.assertNotIn("function postRenderFrames", harness)
        self.assertNotIn("setTimeout(resolve, 1000", harness)

    def test_browser_harness_covers_both_duplicate_ordinary_orderings(self) -> None:
        harness = text(ROOT / "tools/tests/day_reader_integration_browser.mjs")
        self.assertIn("STATES.roman + '&ordinary=0&ordinary=1'", harness)
        self.assertIn("STATES.roman + '&ordinary=1&ordinary=0'", harness)
        self.assertIn("both duplicated Ordinary orderings are neutral and history-independent", harness)
        self.assertIn("['Read', STATES.postconciliar]", harness)
        self.assertIn("['Missal', STATES.postMissal]", harness)


if __name__ == "__main__":
    unittest.main()
