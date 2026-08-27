#!/usr/bin/env python3
"""Focused static and isolation gates for the W3 Day reader candidate."""

from __future__ import annotations

import hashlib
import json
import subprocess
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
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

CHOICE_NODE = r"""
const fs = require('fs');
const source = fs.readFileSync('src/web/browser/liturgy/day-reader.js', 'utf8');
const start = source.indexOf('  function primaryDayChoice(result, branch)');
const end = source.indexOf('  function commitUnresolvedChoice(', start);
if (start < 0 || end < 0) throw new Error('Day choice functions are absent');

class Node {
  constructor(tag, className, ownText) {
    this.tagName = String(tag || '').toUpperCase();
    this.className = className || '';
    this.ownText = ownText || '';
    this.children = [];
    this.dataset = {};
    this.listeners = {};
    this.disabled = false;
    this.checked = false;
    this.name = '';
    this.value = '';
    this.id = '';
    this.tabIndex = 0;
  }
  appendChild(child) { this.children.push(child); return child; }
  addEventListener(name, callback) { this.listeners[name] = callback; }
  querySelector(selector) {
    const held = all(this).filter((node) => node.tagName === 'INPUT');
    if (selector.includes(':checked')) return held.find((node) => node.checked) || null;
    return held[0] || null;
  }
  get textContent() {
    return this.ownText + this.children.map((child) => child.textContent || '').join('');
  }
}
function all(node) {
  return [node].concat(node.children.flatMap((child) => all(child)));
}
const document = {
  createElement(tag) { return new Node(tag); },
  createTextNode(value) { return new Node('#text', '', String(value)); }
};
const T = { el(tag, className, value) { return new Node(tag, className, value); } };
const navigations = [];
const readerShell = { close(value) { this.closed = value; } };
function navigate(updates, removals, state) { navigations.push({updates, removals, state}); }
eval(source.slice(start, end));

function properResult(ids) {
  return {
    resolved: {formulary: 'authored-mass'},
    unresolvedChoices: [{
      id: 'proper-form:postconciliar/authored-mass', reason: 'source choice',
      options: ids.map((id) => ({id})), sourceHooks: []
    }]
  };
}
const structure = {masses: [{key: 'authored-mass', forms: [
  {id: 'night', name: 'At Night'}, {id: 'day', name: 'During the Day'}
]}]};
const proper = unresolvedChoiceDocument(properResult(['night', 'day']), {}, structure);
const properNodes = all(proper.node);
const radios = properNodes.filter((node) => node.tagName === 'INPUT');
const submit = properNodes.find((node) => node.tagName === 'BUTTON');
const form = properNodes.find((node) => node.tagName === 'FORM');
const initiallyDisabled = submit.disabled;
radios[1].checked = true;
form.listeners.change();
const enabledAfterChoice = !submit.disabled;
form.listeners.submit({preventDefault() {}});

const calendar = unresolvedChoiceDocument({
  resolved: null,
  unresolvedChoices: [{id: 'calendar-formulary', reason: 'calendar choice', options: [
    {id: 'saint'}, {id: 'feria'}
  ], sourceHooks: [{kind: 'locus', id: 'GNLYC 14'}]}]
}, {readable: [
  {key: 'saint', label: 'Saint'}, {key: 'feria', label: 'Weekday'}
]}, {masses: []});
const calendarNodes = all(calendar.node);
const calendarRadios = calendarNodes.filter((node) => node.tagName === 'INPUT');
const calendarForm = calendarNodes.find((node) => node.tagName === 'FORM');
calendarRadios[0].checked = true;
calendarForm.listeners.change();
calendarForm.listeners.submit({preventDefault() {}});

function rejection(ids, forms) {
  try {
    unresolvedChoiceDocument(properResult(ids), {}, {
      masses: [{key: 'authored-mass', forms}]
    });
    return null;
  } catch (error) { return error.message; }
}
process.stdout.write(JSON.stringify({
  proper: {
    className: proper.node.className, tabIndex: proper.node.tabIndex,
    headingId: proper.id, text: proper.node.textContent,
    radioIds: radios.map((node) => node.value),
    initiallyDisabled, enabledAfterChoice,
    navigation: navigations[0]
  },
  calendar: {
    headingId: calendar.id,
    radioIds: calendarRadios.map((node) => node.value),
    navigation: navigations[1]
  },
  mainError: rejection(['main', 'day'], [
    {id: 'main', name: 'Internal'}, {id: 'day', name: 'Day'}
  ]),
  mismatchError: rejection(['night', 'foreign'], structure.masses[0].forms)
}));
"""


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


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
        self.assertIn(
            "return mode === 'study' ? ['mode=' + mode] : [];",
            source,
        )
        self.assertIn("Compare deliberately does not", source)
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

    def test_canonical_mode_location_and_cold_read_are_first_class(self) -> None:
        source = text(DAY_JS)
        for token in (
            "const needsOrdinary = requestedMode === 'missal' || explicitOrdinary",
            "const variantErrors = await validateExplicitVariants(",
            "Contract.defaultBibleId(runtime.bibles)",
            "runtime.mode = normalized.state.requestedMode",
            "Contract.canonicalRoute('day', window.location.pathname)",
            "Contract.serializeLegacy(normalized)",
            "normalized.state.semanticLocation",
            "navigate({ mode: 'read' }",
            "navigate({ mode: 'missal' }",
            "(removals || []).concat(['ordinary'])",
        ):
            self.assertIn(token, source)
        self.assertNotIn("runtime.bibles[0]", source)
        self.assertNotIn("navigate({ ordinary: '1'", source)
        for token in (
            "function translationWitnessState", "validateExplicitTranslationWitness",
            "dataset.translationWitness", "translation-witness-result",
        ):
            self.assertIn(token, source)

    def test_authorized_day_and_proper_form_choices_have_one_accessible_control(self) -> None:
        source = text(DAY_JS)
        for token in (
            "one.id === 'calendar-formulary' || /^proper-form:/.test(one.id)",
            "section.dataset.unresolvedChoice = choice.id",
            "section.tabIndex = -1",
            "const fieldset = T.el('fieldset')",
            "input.type = 'radio'",
            "input.dataset.choiceOption = option.id",
            "submit.disabled = true",
            "optionIds.indexOf('main') >= 0",
            "source choice options do not match the readable identities",
            "mass: result.resolved.formulary, form: selected.value, location: null",
            "readerShell.setContents([",
            "focus: { kind: 'day-choice-result' }",
            "reading.querySelector('[data-semantic-event-id]')",
            "if (readable.length > 1 && runtime.outcome !== 'unresolved')",
            "['Mass form', state.form ||",
        ):
            self.assertIn(token, source)
        self.assertIn("'No default selected'", source)
        choice_gate = source.index("if (primaryDayChoice(result, branch))")
        render_gate = source.index("if (!result.resolved)", choice_gate)
        self.assertLess(choice_gate, render_gate)

    def test_choice_dom_uses_only_authored_ids_and_submits_explicit_state(self) -> None:
        run = subprocess.run(
            ["node", "-e", CHOICE_NODE], cwd=ROOT, text=True,
            capture_output=True, check=False,
        )
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        value = json.loads(run.stdout)
        self.assertIn("proper-form-choice", value["proper"]["className"])
        self.assertEqual(value["proper"]["tabIndex"], -1)
        self.assertEqual(value["proper"]["headingId"], "proper-form-choice")
        self.assertEqual(value["proper"]["radioIds"], ["night", "day"])
        self.assertIn("At Night", value["proper"]["text"])
        self.assertIn("During the Day", value["proper"]["text"])
        self.assertTrue(value["proper"]["initiallyDisabled"])
        self.assertTrue(value["proper"]["enabledAfterChoice"])
        self.assertEqual(value["proper"]["navigation"]["updates"], {
            "mass": "authored-mass", "form": "day", "location": None,
        })
        self.assertEqual(value["proper"]["navigation"]["removals"], ["location"])
        self.assertEqual(value["calendar"]["headingId"], "calendar-formulary-choice")
        self.assertEqual(value["calendar"]["radioIds"], ["saint", "feria"])
        self.assertEqual(value["calendar"]["navigation"]["updates"], {
            "mass": "saint", "form": None, "location": None,
        })
        self.assertIn("internal main form", value["mainError"])
        self.assertIn("do not match", value["mismatchError"])

    def test_day_history_coalesces_events_and_preserves_semantic_location(self) -> None:
        source = text(DAY_JS)
        for token in (
            "Object.assign({}, history.state || {}, { dayReaderLocation: currentLocation })",
            "updates.location = navigation.location && navigation.location.kind === 'event'",
            "dayReaderLocation: runtime.pendingLocation",
            "function scheduleHistoryRender()",
            "if (historyRenderTimer !== null) return",
            "window.addEventListener('popstate'",
            "window.addEventListener('hashchange'",
            "readerShell.restoreSemanticLocation(held.location)",
        ):
            self.assertIn(token, source)

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

    def test_accepted_shell_and_visual_oracle_hashes_are_current(self) -> None:
        bindings = subprocess.run(
            [str(ROOT / "tools/tpt"), "release-bindings", "status"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(
            bindings.returncode,
            0,
            bindings.stdout + bindings.stderr,
        )
        for path, expected in FROZEN_SOURCE_HASHES.items():
            actual = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            self.assertEqual(actual, expected, path)
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
        sentinels = ("synthetic-cycle-order", "candidate-contract-only")
        for path in (ROOT / "src/web/data").rglob("*.json"):
            payload = text(path)
            for sentinel in sentinels:
                self.assertNotIn(sentinel, payload, path.as_posix())
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
        self.assertLess(DAY_JS.stat().st_size, 100_000)

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
