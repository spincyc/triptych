#!/usr/bin/env python3
"""Focused static and isolation gates for the W3 Day reader candidate."""

from __future__ import annotations

import hashlib
import subprocess
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = "c4c071d6ba962524487bc8f4c6a4b781981851c7"
LITURGY = ROOT / "src/web/browser/liturgy"
HTML = LITURGY / "day-reader.html"
SHELL_JS = LITURGY / "reader-shell.js"
SHELL_CSS = LITURGY / "reader-shell.css"
DAY_JS = LITURGY / "day-reader.js"
DAY_CSS = LITURGY / "day-reader.css"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout


class DayReaderIntegrationTests(unittest.TestCase):
    def test_candidate_is_noindex_unlinked_and_built_from_top_level_sources(self) -> None:
        source = text(HTML)
        self.assertIn("meta[name=\"robots\"]", text(DAY_JS))
        self.assertIn("noindex, nofollow, noarchive", text(DAY_JS))
        self.assertIn("Internal W3 candidate", source)
        self.assertIn('data-reader-shell', source)
        self.assertNotIn("shell=persistent", source)
        self.assertNotIn("shell=reveal", source)
        self.assertNotIn("prototypes/reader-shell", source)
        for asset in (
            "reader-shell.js", "reader-shell.css", "day-reader.js", "day-reader.css",
            "day.js", "day.css", "day-missal.css",
        ):
            self.assertIn(asset, source)

        linked_from = []
        for page in LITURGY.glob("*.html"):
            if page == HTML:
                continue
            if "day-reader.html" in text(page):
                linked_from.append(page.relative_to(ROOT).as_posix())
        self.assertEqual(linked_from, [])

    def test_shared_shell_owns_only_persistent_interaction_concerns(self) -> None:
        source = text(SHELL_JS)
        for token in (
            "data-reader-action", "data-reader-surface", "showModal()",
            "aria-expanded", "scrollIntoView", "aria-current", "preventScroll"
        ):
            self.assertIn(token, source)
        for forbidden in (
            "MassAssembly", "renderProper", "fetchFragments", "calendar/",
            "reader-state", "shell-hidden", "scroll-reveal", "geolocation"
        ):
            self.assertNotIn(forbidden, source)
        self.assertEqual(source.count("showModal()"), 1)

    def test_candidate_crosses_existing_state_assembly_and_renderer_boundaries(self) -> None:
        source = text(DAY_JS)
        for token in (
            "Contract.parseLegacy", "Contract.normalizeLegacy",
            "Contract.validateReaderState", "Adapters.validationContext",
            "Adapters.adaptDay", "Model.derive", "T.fetchFragments",
            "T.renderProper", "T.citationsOf"
        ):
            self.assertIn(token, source)
        self.assertNotIn("innerHTML", source)
        self.assertNotIn("navigator.geolocation", source)
        self.assertNotIn("localStorage", source)
        self.assertNotIn("prototypes/reader-shell", source)
        self.assertNotIn("fixture", source.lower())

    def test_all_four_actions_and_bounded_modes_are_explicit(self) -> None:
        source = text(HTML)
        for action, label in (
            ("date", "Date &amp; edition"),
            ("contents", "Contents"),
            ("mode", "Mode"),
            ("details", "Details"),
        ):
            self.assertIn(f'data-reader-action="{action}"', source)
            self.assertIn(label, source)
        self.assertIn('data-mode="read"', source)
        self.assertIn('data-mode="missal"', source)
        self.assertEqual(source.count('aria-disabled="true" disabled'), 2)
        self.assertIn("Continuous Ordinary with appointed propers in place.", source)
        for name in ("Study", "Compare"):
            self.assertIn(f"<strong>{name}</strong>", source)
            self.assertIn("Not integrated in the W3 candidate.", source)

    def test_only_why_remains_deferred_while_missal_state_is_active_or_latent(self) -> None:
        source = text(DAY_JS)
        for key in ("ordinary", "ordinary-lang", "rubrics", "why"):
            self.assertIn(key, source)
        self.assertIn("parsed.variantKeys", source)
        self.assertIn("day.html", source)
        self.assertIn("window.location.hash", source)
        self.assertIn("but did not partially render it", source)
        self.assertIn("recognized.why === '1'", source)
        self.assertNotIn("recognized.rubrics === '1'", source)
        self.assertNotIn("const ordinaryActive = recognized.ordinary === '1'", source)
        self.assertIn("async function validateExplicitVariants", source)
        self.assertIn("structure.variants", source)
        self.assertIn("window.dayReaderDebug.legacy = normalized.legacy", source)

    def test_each_render_clears_selection_state_before_validation(self) -> None:
        source = text(DAY_JS)
        self.assertIn("function clearSelectionState(outcome)", source)
        self.assertIn("clearSelectionState('loading')", source)
        self.assertIn("if (!held.preserveSelection) clearSelectionState(outcome)", source)
        self.assertIn("const pendingNavigation = takePendingNavigation()", source)
        self.assertIn("runtime.pendingFocus = null", source)
        self.assertIn("window.dayReaderDebug.pendingNavigation = null", source)
        for assignment in (
            "runtime.normalized = null", "runtime.result = null",
            "runtime.derived = null", "runtime.structure = null",
            "runtime.branch = null", "runtime.deferred = []",
            "window.dayReaderDebug.state = null",
            "window.dayReaderDebug.semantic = null",
        ):
            self.assertIn(assignment, source)
        self.assertIn("No validated selection is available for the current candidate outcome", source)
        self.assertIn("'Choice required'", source)

    def test_superseded_async_renders_cannot_mutate_current_output(self) -> None:
        source = text(DAY_JS)
        self.assertIn(
            "async function renderResult(result, structure, derived, branch, renderContext, isCurrent)",
            source,
        )
        self.assertIn("if (!isCurrent()) return false", source)
        self.assertIn("function () { return serial === runtime.serial; }", source)
        self.assertIn("if (!rendered || serial !== runtime.serial) return", source)
        catch = source.index("} catch (error) {", source.index("async function renderCandidate"))
        failure = source.index("renderFailure([{ code: 'candidate-load'", catch)
        self.assertIn("if (serial !== runtime.serial) return", source[catch:failure])

    def test_weekday_and_details_are_human_facing(self) -> None:
        source = text(DAY_JS)
        self.assertIn("sunday: 'Sunday'", source)
        self.assertIn("WEEKDAY_NAMES[weekday]", source)
        self.assertNotIn("WEEKDAYS[weekday]", source)
        self.assertNotIn("Available source identities", source)
        self.assertNotIn("hook.kind + ': '", source)
        self.assertNotIn("source-identifier', hook", source)

    def test_complete_notice_and_machine_envelope_boundaries_are_encoded(self) -> None:
        source = text(DAY_JS)
        self.assertIn("row.completeness === 'complete'", source)
        self.assertIn("coverageNotice.hidden = !notice", source)
        self.assertNotIn("No blocking notices", source)
        self.assertNotIn("bound M1 state", source)
        self.assertNotIn("JSON.stringify(runtime", source)
        self.assertNotIn("JSON.stringify(normalized", source)

    def test_responsive_print_and_modal_rules_are_present(self) -> None:
        shell = text(SHELL_CSS)
        candidate = text(DAY_CSS)
        self.assertIn("--reader-shell-height: 3.65rem", shell)
        self.assertIn("env(safe-area-inset-bottom", shell)
        self.assertIn("@media (prefers-reduced-motion: reduce)", shell)
        self.assertIn("@media (forced-colors: active)", shell)
        self.assertIn("@media (max-width: 25rem)", shell)
        self.assertIn("overflow-x: hidden", shell)
        self.assertIn("@media print", shell)
        self.assertIn(".reader-actions, .reader-surface { display: none !important; }", shell)
        self.assertIn(".candidate-flag { display: none !important; }", candidate)
        self.assertIn("break-inside: avoid", candidate)

    def test_public_pages_propers_m1_and_production_data_are_isolated(self) -> None:
        protected = [
            "src/web/browser/liturgy/day.html",
            "src/web/browser/liturgy/day.css",
            "src/web/browser/liturgy/day-missal.css",
            "src/web/browser/liturgy/index.html",
            "src/web/browser/liturgy/liturgy.js",
            "src/web/browser/liturgy/reader-state.js",
            "src/web/browser/liturgy/reader-state-adapters.js",
            "src/web/browser/liturgy/propers-reader.html",
            "src/web/browser/liturgy/propers-reader.js",
            "src/web/browser/liturgy/propers-reader.css",
        ]
        for path in protected:
            current = (ROOT / path).read_bytes()
            original = subprocess.run(
                ["git", "show", f"{BASE}:{path}"], cwd=ROOT,
                check=True, capture_output=True
            ).stdout
            self.assertEqual(
                hashlib.sha256(current).hexdigest(),
                hashlib.sha256(original).hexdigest(),
                path,
            )
        changed_data = git(
            "diff", "--name-only", BASE, "--",
            "src/web/data", "src/sources/calendars"
        ).splitlines()
        self.assertEqual(changed_data, [])
        public_renderer = text(LITURGY / "day.js")
        self.assertIn("window.TriptychOrdinaryRenderer", public_renderer)
        self.assertIn("renderSemanticFrame", public_renderer)
        self.assertIn("if (!reading || !controls) return", public_renderer)

    def test_candidate_does_not_leak_fixture_or_discovery_records(self) -> None:
        changed = git("diff", "--name-only", BASE).splitlines()
        forbidden = [
            path for path in changed
            if path.startswith("src/web/data/")
            or "fixtures/liturgy-reader-state" in path
            or path.endswith("sitemap.xml")
        ]
        self.assertEqual(forbidden, [])
        for path in ROOT.rglob("*.html"):
            if path == HTML or "build" in path.parts or ".git" in path.parts:
                continue
            self.assertNotIn("day-reader.html", text(path), path.as_posix())

    def test_promised_deliverable_records_the_accepted_m3_day_slice(self) -> None:
        with (ROOT / "promised-deliverables.toml").open("rb") as handle:
            ledger = tomllib.load(handle)
        rows = [
            row for row in ledger["deliverables"]
            if row["id"] == "liturgy-day-reader-shell-m3-candidate-2026-08-04"
        ]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["state"], "complete")
        self.assertEqual(rows[0]["owner"], "src/web/browser/liturgy/day-reader.html")
        self.assertEqual(
            {requirement["status"] for requirement in rows[0]["requirements"]},
            {"pass"},
        )
        candidate = [
            row for row in ledger["deliverables"]
            if row["id"] == "liturgy-day-missal-w3-candidate-2026-08-05"
        ]
        self.assertEqual(len(candidate), 1)
        self.assertEqual(candidate[0]["state"], "complete")

    def test_candidate_size_is_bounded_below_prototype_harness(self) -> None:
        prototype = LITURGY / "prototypes/reader-shell/reader-shell.js"
        self.assertLess(SHELL_JS.stat().st_size, prototype.stat().st_size // 4)
        self.assertLess(DAY_JS.stat().st_size, prototype.stat().st_size)

    def test_chromium_evidence_distinguishes_commit_from_visual_settlement(self) -> None:
        harness = text(ROOT / "tools/tests/day_reader_integration_browser.mjs")
        commit = harness.index("async function waitForCommittedRender")
        settlement = harness.index("return waitForVisualSettlement", commit)
        self.assertGreater(settlement, commit)
        self.assertIn("window.dayReaderDebug.committedRender.generation >", harness[commit:settlement])
        self.assertIn("semanticTargetRect", harness)
        self.assertIn("stableFramesObserved", harness)
        self.assertIn("expectedSemanticEventId", harness)


if __name__ == "__main__":
    unittest.main()
