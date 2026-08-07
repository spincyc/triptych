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
STATE_JS = LITURGY / "reader-state.js"
ROBOTS = "noindex, nofollow, noarchive, nosnippet, noimageindex"

FROZEN_SOURCE_HASHES = {
    "src/web/browser/liturgy/reader-shell.css":
        "e7195cd86ed4fc4a8455e97369702239eb22d709a13d3d8462d7759c01fe814a",
    "src/web/browser/liturgy/reader-visual-reset-day.html":
        "ff734f07b797e5706c7e62a4c890f47c32c0fbfd78bfc855f421a4123273c18d",
    "src/web/browser/liturgy/reader-visual-reset-propers.html":
        "7b0a3a4c7ef1189f27bf134a9f6df90315c62675a19cabca0135adaf7201ba65",
    "src/web/browser/liturgy/reader-visual-reset.css":
        "850e1acacb6f487a5c2f3118388b3fce7b96f9db667e783ba35cdef7d9918b48",
    "src/web/browser/liturgy/reader-visual-reset.js":
        "eb1c1dd5c0c9c7076b74f2187627dc56e39963429212c0a51872df0ea98a9679",
}


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout


class DayReaderIntegrationTests(unittest.TestCase):
    def test_reader_is_source_noindex_route_neutral_unlinked_and_top_level(self) -> None:
        source = text(HTML)
        script = text(DAY_JS)
        self.assertEqual(
            source.count(f'<meta name="robots" content="{ROBOTS}">'), 1
        )
        self.assertNotIn("meta[name=\"robots\"]", script)
        self.assertNotIn("robots.content", script)
        self.assertIn("<title>Day — Triptych</title>", source)
        for obsolete in (
            "Internal W3 candidate", "live Day page is unchanged",
            "Available and active in this candidate",
            "Not integrated in the W3 candidate",
        ):
            self.assertNotIn(obsolete, source)
        self.assertNotIn("Internal Day reader candidate", script)
        self.assertIn('data-reader-shell', source)
        self.assertNotIn("shell=persistent", source)
        self.assertNotIn("shell=reveal", source)
        self.assertNotIn("prototypes/reader-shell", source)
        for asset in (
            "reader-shell.js", "reader-shell.css", "day-reader.js", "day-reader.css",
            "reader-instrument.css", "day.js", "day.css", "day-missal.css",
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
            ("date", "Date"),
            ("contents", "Contents"),
            ("mode", "Mode"),
            ("details", "Details"),
        ):
            self.assertIn(f'data-reader-action="{action}"', source)
            self.assertIn(f'class="action-label">{label}</span>', source)
        self.assertIn('data-mode="read"', source)
        self.assertIn('data-mode="missal"', source)
        self.assertEqual(source.count('aria-disabled="true" disabled'), 2)
        self.assertIn("Continuous reading of the appointed texts.", source)
        self.assertIn("Continuous Ordinary with appointed propers in place.", source)
        self.assertIn("<strong>Study</strong><span>Expanded notes and apparatus.</span>", source)
        self.assertIn("<strong>Compare</strong><span>Parallel editions and recensions.</span>", source)

    def test_why_uses_source_derived_apparatus_without_a_self_link(self) -> None:
        source = text(DAY_JS)
        for key in ("ordinary", "ordinary-lang", "rubrics", "why"):
            self.assertIn(key, source)
        self.assertIn("parsed.variantKeys", source)
        self.assertIn("function deferredState(parsed) {\n    return [];", source)
        self.assertNotIn("recognized.why === '1'", source)
        self.assertNotIn("recognized.rubrics === '1'", source)
        self.assertNotIn("const ordinaryActive = recognized.ordinary === '1'", source)
        self.assertIn("async function validateExplicitVariants", source)
        self.assertIn("structure.variants", source)
        for token in (
            "function reasoningApparatus(branch, rubrics, structure, result, ordinary)",
            "Model.placeWord(rubrics)",
            "REASONING_SOURCE_WORDS[winner.source]",
            "longDate(loser.destination, Model.weekdayOf(loser.destination))",
            "if (winner.formulary.latin)",
            "if (choice.latin)",
            "function appendProperReasoning(body, branch, rubrics, structure, result)",
            "function appendOrdinaryReasoning(body, result, ordinary)",
            "ordinary.slots_derived_from",
            "event.seat.locus",
            "if (winner.rowLabel)",
            "winner.why && winner.why !== winner.rowLabel",
            "winner.locus",
            "(branch.candidates || [])",
            "branch.ceilings && branch.ceilings.low_mass",
            "rubrics.mass_category",
            "Boolean(normalized.state.apparatus && normalized.state.apparatus.why)",
        ):
            self.assertIn(token, source)
        self.assertNotIn("day.html", source)
        self.assertNotIn("Open this selection in the current Day reader", source)
        self.assertIn("window.dayReaderDebug.legacy = normalized.legacy", source)

    def test_all_held_territorial_branches_render_without_a_public_locality_key(self) -> None:
        source = text(DAY_JS)
        for token in (
            "function resultStateForBranch(state, branch, multiple)",
            "calendar: Object.assign({}, state.calendar, { territory: { id: branch.option } })",
            "for (let branchIndex = 0; branchIndex < assembled.derived.options.length; branchIndex += 1)",
            "branch.dataset.territorialBranch = row.branch.option",
            "runtime.branches = rendered.map(function (row)",
            "runtime.branch = multiple ? null : rendered[0].branch",
            "title.textContent = multiple\n      ? 'Held territorial branches'",
            "territory: row.branch.option",
        ):
            self.assertIn(token, source)
        self.assertNotIn("territorial-choice", source)
        self.assertIn("All held territorial branches are shown; no locality is inferred.", text(HTML))

        day_keys = text(STATE_JS).split("const DAY_KEYS", 1)[1].split("]);", 1)[0]
        self.assertNotIn("territory", day_keys)
        self.assertNotIn("locality", day_keys)

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
        self.assertIn("No validated selection is available for the current reader outcome", source)
        self.assertIn("runtime.branches = []", source)

    def test_superseded_async_renders_cannot_mutate_current_output(self) -> None:
        source = text(DAY_JS)
        self.assertIn(
            "async function buildResultDocument(result, structure, branch, renderContext, isCurrent)",
            source,
        )
        self.assertIn("if (!isCurrent()) return false", source)
        self.assertIn("function () { return serial === runtime.serial; }", source)
        self.assertIn("if (!row || serial !== runtime.serial) return", source)
        catch = source.index("} catch (error) {", source.index("async function renderCandidate"))
        failure = source.index("renderFailure([{ code: 'candidate-load'", catch)
        self.assertIn("if (serial !== runtime.serial) return", source[catch:failure])

    def test_weekday_and_details_are_human_facing_with_direct_links(self) -> None:
        source = text(DAY_JS)
        self.assertIn("sunday: 'Sunday'", source)
        self.assertIn("WEEKDAY_NAMES[weekday]", source)
        self.assertNotIn("WEEKDAYS[weekday]", source)
        self.assertNotIn("Available source identities", source)
        self.assertNotIn("hook.kind + ': '", source)
        self.assertNotIn("source-identifier', hook", source)
        self.assertIn("function detailsLinkSection(heading, links)", source)
        self.assertIn("detailsLinkSection('Related reader'", source)
        self.assertIn("{ label: 'Browse the Propers', href: 'index.html' }", source)
        self.assertIn("detailsLinkSection('Elsewhere in Triptych'", source)
        self.assertIn("{ label: 'The Code, Canon by Canon', href: '../law/' }", source)
        self.assertIn("{ label: 'Every Document', href: '../texts/' }", source)

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
        instrument = text(LITURGY / "reader-instrument.css")
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
        self.assertIn("container: reader-shell / inline-size", instrument)
        self.assertIn("@container reader-shell (max-width: 18rem)", instrument)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr))", instrument)

    def test_data_legacy_shell_css_and_visual_oracle_are_frozen(self) -> None:
        for path, expected in FROZEN_SOURCE_HASHES.items():
            actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, path)

        protected = [
            "src/web/browser/liturgy/day.css",
            "src/web/browser/liturgy/day-missal.css",
            "src/web/browser/liturgy/liturgy.js",
            "src/web/browser/liturgy/reader-state-adapters.js",
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

    def test_live_routes_expose_source_owned_locus_and_current_map_hooks(self) -> None:
        for page in (LITURGY / "day.html", HTML):
            self.assertEqual(text(page).count("data-reader-locus"), 3)
        shell = text(SHELL_JS)
        day = text(DAY_JS)
        self.assertIn("function currentLocus()", shell)
        self.assertIn("function centerCurrentContents(surface)", shell)
        self.assertIn("data-reader-locus-major", shell)
        self.assertIn("node.dataset.readerLocusMajor = major", day)
        self.assertIn("event.seat && event.seat.anchor", day)
        self.assertNotIn("aria-live", shell)

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

    def test_reader_size_remains_bounded_after_compatibility_closure(self) -> None:
        prototype = LITURGY / "prototypes/reader-shell/reader-shell.js"
        self.assertLess(SHELL_JS.stat().st_size, prototype.stat().st_size // 4)
        self.assertLess(DAY_JS.stat().st_size, 76_000)

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
