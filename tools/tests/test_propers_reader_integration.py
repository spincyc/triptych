#!/usr/bin/env python3
"""Focused static, contract, and isolation gates for the W3 Propers candidate."""

from __future__ import annotations

import hashlib
import subprocess
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = "c4c071d6ba962524487bc8f4c6a4b781981851c7"
LITURGY = ROOT / "src/web/browser/liturgy"
HTML = LITURGY / "propers-reader.html"
JS = LITURGY / "propers-reader.js"
CSS = LITURGY / "propers-reader.css"
SHELL_JS = LITURGY / "reader-shell.js"
SHELL_CSS = LITURGY / "reader-shell.css"
DAY_HTML = LITURGY / "day-reader.html"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout


class PropersReaderIntegrationTests(unittest.TestCase):
    def test_candidate_is_noindex_unlinked_and_normal_preview_source(self) -> None:
        html = text(HTML)
        script = text(JS)
        self.assertIn('data-reader-shell', html)
        self.assertIn('data-entrance="propers"', html)
        self.assertIn("meta[name=\"robots\"]", script)
        self.assertIn("noindex, nofollow, noarchive", script)
        self.assertIn("Internal Propers Read candidate", html)
        self.assertNotIn("M3 candidate", html)
        self.assertNotIn("prototypes/reader-shell", html)
        for asset in (
            "reader-shell.js", "reader-shell.css", "reader-state.js",
            "reader-state-adapters.js", "propers-reader.js", "propers-reader.css",
            "reader-instrument.css",
        ):
            self.assertIn(asset, html)

        linked_from = []
        for page in LITURGY.glob("*.html"):
            if page == HTML:
                continue
            if "propers-reader.html" in text(page):
                linked_from.append(page.relative_to(ROOT).as_posix())
        self.assertEqual(linked_from, [])

    def test_day_and_propers_use_the_exact_same_shell_files(self) -> None:
        for page in (text(DAY_HTML), text(HTML)):
            self.assertIn('<script src="reader-shell.js"></script>', page)
            self.assertIn('<link rel="stylesheet" href="reader-shell.css">', page)
        self.assertEqual(text(HTML).count('data-reader-shell'), 1)
        self.assertNotIn("TriptychReaderShell =", text(JS))
        self.assertNotIn("showModal()", text(JS))
        # The adapter may identify the Browse trigger when it must foreground
        # an unresolved entry, but lifecycle ownership remains in the shell.
        self.assertEqual(text(JS).count('data-reader-action="browse"'), 1)

    def test_shared_shell_remains_one_entrance_neutral_implementation(self) -> None:
        source = text(SHELL_JS)
        for token in (
            "data-reader-action", "data-reader-surface", "showModal()",
            "aria-expanded", "scrollIntoView", "aria-current", "preventScroll",
        ):
            self.assertIn(token, source)
        for forbidden in (
            "MassAssembly", "adaptPropers", "renderProper", "fetchFragments",
            "calendar/", "formulary", "cycle", "geolocation",
        ):
            self.assertNotIn(forbidden, source)
        self.assertIn("captureSemanticLocation", source)
        self.assertIn("restoreSemanticLocation", source)
        original_css = subprocess.run(
            ["git", "show", f"{BASE}:{SHELL_CSS.relative_to(ROOT).as_posix()}"],
            cwd=ROOT, check=True, capture_output=True,
        ).stdout
        self.assertEqual(hashlib.sha256(SHELL_CSS.read_bytes()).digest(), hashlib.sha256(original_css).digest())

    def test_candidate_crosses_m1_and_production_renderer_boundaries(self) -> None:
        source = text(JS)
        for token in (
            "Contract.parseLegacy('propers'", "Contract.normalizeLegacy",
            "Contract.validateReaderState", "Adapters.validationContext",
            "Adapters.adaptPropers", "T.fetchFragments", "T.renderProper",
            "T.citationsOf", "T.uncompiledNote",
        ):
            self.assertIn(token, source)
        self.assertNotIn("innerHTML", source)
        self.assertNotIn("navigator.geolocation", source)
        self.assertNotIn("prototypes/reader-shell", source)
        self.assertNotIn("synthetic", source.lower())

    def test_explicit_propers_entrance_and_browse_sentinel_are_constructed(self) -> None:
        source = text(JS)
        for token in (
            "entrance: 'propers'", "civilDate: null",
            "browse: { kind: 'browse-entry' }", "requestedMode: 'read'",
        ):
            self.assertIn(token, source)
        self.assertIn("!hasMass || !hasType", source)
        self.assertIn("No liturgical text is selected by list order", source)
        self.assertNotIn("state.masses[0].key", source)

    def test_legacy_and_internal_state_spelling_are_bounded(self) -> None:
        source = text(JS)
        for key in ("missal", "type", "mass", "bible", "orations"):
            self.assertIn(key, source)
        self.assertIn("_candidate-cycle", source)
        self.assertIn("_candidate-alternative", source)
        self.assertIn("_candidate-translation-witness", source)
        self.assertNotIn("params.set('cycle'", source)
        self.assertNotIn("params.set('alternative'", source)
        self.assertIn("T.params.get('missals')", source)
        self.assertIn("T.dataRoot", source)

    def test_no_arbitrary_fallback_and_cross_missal_revalidation(self) -> None:
        source = text(JS)
        for phrase in (
            "the explicit formulary is not held in the requested missal and type",
            "the current Propers identity requires both type and mass",
            "The prior formulary was cleared",
            "none was selected automatically",
            "Choose a formulary before applying",
        ):
            self.assertIn(phrase, source)
        self.assertIn("fillFormularies(groups, typeSelect.value, null)", source)
        self.assertIn("placeholder(formularySelect, 'Choose a formulary…')", source)

    def test_cycles_and_alternatives_remain_independent(self) -> None:
        source = text(JS)
        self.assertIn("event.selected.kind === 'cycle-alternatives'", source)
        self.assertIn("event.selected.alternatives.forEach", source)
        self.assertIn("cycle: alternative.cycle", source)
        self.assertIn("Several cycles are held. They remain separate", source)
        self.assertIn("Adapters.adaptPropers", source)
        self.assertNotIn("alternatives.join", source)
        self.assertNotIn("Object.keys(proper.cycles)[0]", source)
        self.assertNotIn("sort()[0]", source)
        self.assertNotIn("pop()", source)

    def test_all_four_actions_and_read_only_mode_are_explicit(self) -> None:
        source = text(HTML)
        for action, label in (
            ("browse", "Browse"), ("contents", "Contents"),
            ("mode", "Mode"), ("details", "Details"),
        ):
            self.assertIn(f'data-reader-action="{action}"', source)
            self.assertIn(f'class="action-label">{label}</span>', source)
        self.assertIn('data-mode="read"', source)
        self.assertEqual(source.count('aria-disabled="true"'), 3)
        self.assertEqual(source.count(' disabled>'), 3)
        for name in ("Missal", "Study", "Compare"):
            self.assertIn(f"<strong>{name}</strong>", source)
            self.assertIn("Not integrated in this internal candidate.", source)

    def test_each_render_clears_state_and_superseded_work_cannot_commit(self) -> None:
        source = text(JS)
        self.assertIn("function clearSelectionState(outcome)", source)
        self.assertIn("clearSelectionState('loading')", source)
        for assignment in (
            "runtime.normalized = null", "runtime.result = null",
            "runtime.mass = null", "runtime.structure = null",
            "window.propersReaderDebug.state = null",
            "window.propersReaderDebug.semantic = null",
        ):
            self.assertIn(assignment, source)
        self.assertGreaterEqual(source.count("serial !== runtime.serial"), 6)
        self.assertIn("if (!rendered || serial !== runtime.serial) return", source)
        self.assertIn("runtime.browseSerial += 1", source)
        self.assertIn("onClose: function (name)", source)
        self.assertIn("if (name === 'browse')", source)

    def test_witness_choice_is_formulary_and_translation_specific(self) -> None:
        source = text(JS)
        for token in (
            "function formularyWitnessState(structure, mass, language)",
            "language === T.SOURCE_LANGUAGE || !mass",
            "mass.propers || []",
            "proper.translations || []",
            "translationIdentity(row)",
            "witnessState.choices.length > 1",
            "witnessState.deterministic",
            "selectedBrowseMass(groups)",
        ):
            self.assertIn(token, source)
        self.assertNotIn("function translationRows(structure, language)", source)
        self.assertIn("witnessSelect.replaceChildren();\n    witnessField.hidden = true;", source)
        self.assertIn("updates[INTERNAL_WITNESS_KEY] = witnessField.hidden ? null", source)
        self.assertIn(".surface-field[hidden] { display: none; }", text(CSS))

    def test_complete_notice_details_and_print_boundaries_are_encoded(self) -> None:
        source = text(JS)
        html = text(HTML)
        css = text(CSS)
        self.assertIn("row.completeness === 'complete'", source)
        self.assertIn("coverageNotice.hidden = !notice", source)
        self.assertNotIn("No blocking notices", source)
        self.assertNotIn("JSON.stringify(runtime", source)
        self.assertNotIn("Available source identities", source)
        self.assertNotIn("proper-structure", html)
        self.assertIn("@media print", css)
        self.assertIn(".candidate-flag, .cycle-choice-controls { display: none !important; }", css)
        self.assertIn("break-inside: avoid", css)

    def test_responsive_and_accessibility_rules_share_the_accepted_shell(self) -> None:
        shell = text(SHELL_CSS)
        candidate = text(CSS)
        self.assertIn("--reader-shell-height: 3.65rem", shell)
        self.assertIn("env(safe-area-inset-bottom", shell)
        self.assertIn("@media (prefers-reduced-motion: reduce)", shell)
        self.assertIn("@media (forced-colors: active)", shell)
        self.assertIn("@media (max-width: 25rem)", shell)
        self.assertIn("overflow-x: hidden", shell)
        self.assertIn("@media (max-width: 25rem)", candidate)
        self.assertIn("grid-template-columns: repeat(3, minmax(0, 1fr))", candidate)

    def test_public_routes_propers_candidate_m1_and_production_data_are_unchanged(self) -> None:
        protected = [
            "src/web/browser/liturgy/index.html",
            "src/web/browser/liturgy/liturgy.js",
            "src/web/browser/liturgy/liturgy.css",
            "src/web/browser/liturgy/day.html",
            "src/web/browser/liturgy/day.css",
            "src/web/browser/liturgy/day-missal.css",
            "src/web/browser/liturgy/reader-state.js",
            "src/web/browser/liturgy/reader-state-adapters.js",
        ]
        for relative in protected:
            current = (ROOT / relative).read_bytes()
            original = subprocess.run(
                ["git", "show", f"{BASE}:{relative}"], cwd=ROOT,
                check=True, capture_output=True,
            ).stdout
            self.assertEqual(hashlib.sha256(current).hexdigest(), hashlib.sha256(original).hexdigest(), relative)
        changed_data = git(
            "diff", "--name-only", BASE, "--", "src/web/data", "src/sources/calendars"
        ).splitlines()
        self.assertEqual(changed_data, [])

    def test_renderer_extension_is_optional_and_public_callers_are_unchanged(self) -> None:
        core = text(ROOT / "src/web/browser/shared/browser-core.js")
        self.assertIn("function orationFor(proper, wanted, witness)", core)
        self.assertIn("held.translationWitness || null", core)
        public = text(LITURGY / "liturgy.js")
        self.assertNotIn("translationWitness", public)
        self.assertNotIn("_candidate-", public)

    def test_candidate_and_contract_fixtures_do_not_leak_into_generated_data(self) -> None:
        changed = git("diff", "--name-only", BASE).splitlines()
        forbidden = [
            path for path in changed
            if path.startswith("src/web/data/")
            or "fixtures/liturgy-reader-state" in path
            or path.endswith("sitemap.xml")
        ]
        self.assertEqual(forbidden, [])
        sentinels = ("synthetic-cycle-order", "candidate-contract-only")
        for path in (ROOT / "src/web/data").rglob("*.json"):
            payload = text(path)
            for sentinel in sentinels:
                self.assertNotIn(sentinel, payload, path.as_posix())

    def test_promised_deliverable_is_one_accepted_w3_record(self) -> None:
        with (ROOT / "promised-deliverables.toml").open("rb") as handle:
            ledger = tomllib.load(handle)
        propers_rows = [
            row for row in ledger["deliverables"]
            if row["id"] == "liturgy-propers-read-w3-candidate-2026-08-04"
        ]
        day_rows = [
            row for row in ledger["deliverables"]
            if row["id"] == "liturgy-day-reader-shell-m3-candidate-2026-08-04"
        ]
        self.assertEqual(len(propers_rows), 1)
        self.assertEqual(propers_rows[0]["state"], "complete")
        self.assertEqual(
            propers_rows[0]["owner"],
            "src/web/browser/liturgy/propers-reader.html",
        )
        self.assertIn("W3 Propers Read", propers_rows[0]["promise"])
        self.assertTrue(
            all(
                requirement["status"] == "pass"
                for requirement in propers_rows[0]["requirements"]
            )
        )
        self.assertEqual(len(day_rows), 1)
        self.assertEqual(day_rows[0]["state"], "complete")
        missal_rows = [
            row for row in ledger["deliverables"]
            if row["id"] == "liturgy-day-missal-w3-candidate-2026-08-05"
        ]
        self.assertEqual(len(missal_rows), 1)
        self.assertEqual(missal_rows[0]["state"], "complete")
        self.assertEqual(len(ledger["deliverables"]), 22)
        self.assertEqual(
            sum(
                row["state"] == "complete"
                for row in ledger["deliverables"]
            ),
            16,
        )

    def test_candidate_sizes_are_bounded_and_shell_is_not_copied(self) -> None:
        prototype = LITURGY / "prototypes/reader-shell/reader-shell.js"
        self.assertLess(JS.stat().st_size, prototype.stat().st_size)
        self.assertLess(CSS.stat().st_size, SHELL_CSS.stat().st_size)
        self.assertNotIn(text(SHELL_JS), text(JS))


if __name__ == "__main__":
    unittest.main()
