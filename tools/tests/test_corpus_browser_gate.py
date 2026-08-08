#!/usr/bin/env python3
"""Static boundary gates for the design-neutral corpus browser gate.

The gate itself needs Chromium and the built artifact, neither of which the
repository's own installer provides; `make dependencies-arch-browser` is a
separate, opt-in target. So the invariants that can be checked without a browser
are checked here on every host, and the live run is skipped with a reason that
names the environment variable which would enable it.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "tools/tests/corpus_browser_gate.mjs"
SITE = ROOT / "build/public-alpha/site"

# The design-neutral facts the gate exists to assert, in two groups. A name
# removed from the harness is a weakened gate, and these lists are what makes that
# visible.
#
# The first group is asserted for every route at every state in the matrix.
MATRIX_ASSERTION_NAMES = (
    "no-console-errors",
    "no-failed-requests",
    "single-main-element",
    "single-h1-element",
    "skip-link-targets-existing-element",
    "title-present-and-unduplicated",
    "html-element-has-lang",
    "no-horizontal-overflow-at-320",
    "interactive-controls-have-accessible-names",
    "tab-traversal-reaches-visible-controls",
    "escape-key-does-not-throw",
    "focus-indicator-differs-from-resting",
    "primary-controls-meet-target-size",
)

# The rest are facts about a route rather than about a screen size, so they are
# asserted once per route in their own phase.
PHASE_ASSERTION_NAMES = (
    "no-script-static-truth",
    "hash-deep-link-is-honoured",
    "subpath-deep-link-startup",
    "internal-links-resolve",
)

ASSERTION_NAMES = MATRIX_ASSERTION_NAMES + PHASE_ASSERTION_NAMES

# A visual contract does not exist yet, so the gate must not read one. Naming any
# of these would be an opinion about how the site looks rather than whether it
# works.
FORBIDDEN_DESIGN_TOKENS = (
    "background-color",
    "backgroundColor",
    "background-image",
    "font-family",
    "fontFamily",
    "font-weight",
    "fontWeight",
    "font-size",
    "line-height",
    "lineHeight",
    "letter-spacing",
    "letterSpacing",
    "border-radius",
    "borderRadius",
    "text-align",
    "textAlign",
    "text-transform",
    "margin-",
    "padding-",
    "rgb(",
    "rgba(",
    "hsl(",
    "#fff",
    "#000",
)

# `getComputedStyle` is the door every visual opinion comes through, so the gate
# is allowed exactly one use of it and exactly these properties. They are the
# three ways a stylesheet can draw a focus ring, and the gate reads them only to
# compare an element with itself unfocused — a difference, never a value. Adding a
# property here widens what the gate can see of the design, so it is a decision,
# not an edit.
FOCUS_INDICATOR_PROPERTIES = (
    "outline-style",
    "outline-width",
    "outline-color",
    "outline-offset",
    "box-shadow",
    "border-style",
    "border-width",
    "border-color",
)

# The governing screenshot/state matrix.
VIEWPORTS = ((1440, 900), (1024, 768), (768, 1024), (393, 852), (320, 852))


def browser_binary() -> str | None:
    named = os.environ.get("TRIPTYCH_CHROME")
    if named:
        return named if Path(named).is_file() else None
    for candidate in (
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome",
    ):
        if Path(candidate).is_file():
            return candidate
    return shutil.which("chromium") or shutil.which("google-chrome-stable")


class CorpusBrowserGateStructureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = HARNESS.read_text(encoding="utf-8")

    def test_javascript_syntax(self) -> None:
        subprocess.run(["node", "--check", str(HARNESS)], cwd=ROOT, check=True)

    def test_gate_depends_on_nothing_outside_the_node_standard_library(self) -> None:
        imports = re.findall(r"^import\s+[^;]*?from\s+'([^']+)'", self.source, re.M)
        self.assertTrue(imports, "the harness imports nothing at all")
        for specifier in imports:
            self.assertTrue(
                specifier.startswith("node:"),
                f"{specifier} is not a node: builtin; this host has no npm and no node_modules",
            )
        self.assertNotIn("require(", self.source)
        self.assertNotIn("await import(", self.source)

    def test_gate_asserts_every_design_neutral_fact(self) -> None:
        for name in ASSERTION_NAMES:
            self.assertIn(
                f"'{name}'", self.source, f"the gate no longer records {name}"
            )

    def test_gate_states_no_opinion_about_how_the_site_looks(self) -> None:
        for token in FORBIDDEN_DESIGN_TOKENS:
            self.assertNotIn(
                token,
                self.source,
                f"{token} names a visual property; the gate asserts correctness, not design",
            )

    def test_gate_reads_computed_style_only_to_compare_focus_with_its_absence(
        self,
    ) -> None:
        # One reader of computed style, and it lives in the focus-indicator probe.
        self.assertEqual(
            self.source.count("getComputedStyle"),
            1,
            "computed style is readable in exactly one place: the focus indicator",
        )
        block = self.source.split("const FOCUS_INDICATOR_PROPERTIES = [", 1)[1].split(
            "];", 1
        )[0]
        named = tuple(re.findall(r"'([a-z-]+)'", block))
        self.assertEqual(
            named,
            FOCUS_INDICATOR_PROPERTIES,
            "the focus indicator reads a different set of properties than agreed",
        )
        # The assertion is a difference, not an appearance: the reading taken while
        # the element held focus is compared with a second reading of the same
        # element, never with a literal style value.
        probe = self.source.split("const FOCUS_RESTING = `", 1)[1].split("`;", 1)[0]
        self.assertIn("one.focused !== ", probe)
        for token in ("px", "solid", "none'", "auto'"):
            self.assertNotIn(
                token, probe, f"{token} would fix an appearance rather than compare one"
            )

    def test_gate_samples_focus_from_real_tab_presses(self) -> None:
        # A programmatic `focus()` does not reliably put Chromium into the keyboard
        # modality that `:focus-visible` needs, and a check built on one flickers.
        # The reading has to be taken while a Tab press really holds the focus.
        self.assertNotIn(
            "focus({ preventScroll",
            self.source,
            "the focus sample must come from a Tab press, not a programmatic focus",
        )
        self.assertIn("ACTIVE_ELEMENT_SAMPLING", self.source)
        self.assertIn("step < FOCUS_SAMPLE ? ACTIVE_ELEMENT_SAMPLING", self.source)
        self.assertIn("const FOCUS_SAMPLE = 6", self.source)

    def test_gate_measures_target_size_as_a_number_and_exempts_inline_prose(
        self,
    ) -> None:
        self.assertIn("const TARGET_SIZE_MIN_PX = 44", self.source)
        self.assertIn("const TARGET_SIZE_WIDTH = 393", self.source)
        # An inline link inside a sentence is exempt by the standard's own
        # exception; a link in navigation, a header, a footer or a form is not,
        # however it is marked up.
        self.assertIn("const PROSE_ANCESTORS =", self.source)
        self.assertIn("const CHROME_ANCESTORS =", self.source)
        self.assertIn("exempt", self.source)

    def test_gate_keeps_every_hash_deep_link_in_one_table(self) -> None:
        block = self.source.split("const HASH_DEEP_LINKS = [", 1)[1].split("\n];", 1)[0]
        routes = re.findall(r"route: '(/[^']+)'", block)
        hashes = re.findall(r"hash: '(#[^']+)'", block)
        self.assertEqual(len(routes), len(hashes))
        self.assertGreaterEqual(len(routes), 8, routes)
        self.assertEqual(sorted(routes), routes, "hash deep links are unsorted")
        self.assertEqual(len(set(routes)), len(routes), "a route is listed twice")
        # The redirect page must stay out: its hash contract is that the hash
        # moves, so asserting it survives would assert the opposite.
        self.assertNotIn("/scripture/index.html", block)
        self.assertIn("THE ONE PLACE A ROUTER CHANGE HAS TO BE UPDATED", self.source)

    def test_gate_serves_the_artifact_under_a_published_subpath(self) -> None:
        self.assertIn("const SUBPATH_PREFIX = '/triptych'", self.source)
        self.assertIn("staticServer(SUBPATH_PREFIX)", self.source)
        self.assertIn("outside the published prefix", self.source)

    def test_gate_loads_each_route_with_script_execution_disabled(self) -> None:
        self.assertIn("Emulation.setScriptExecutionDisabled", self.source)
        self.assertIn("{ value: true }", self.source)
        self.assertIn("{ value: false }", self.source)

    def test_gate_states_what_it_capped_rather_than_capping_silently(self) -> None:
        self.assertIn("const LINKS_PER_ROUTE_CAP = 40", self.source)
        self.assertIn("NOT CHECKED", self.source)
        self.assertIn("cappedRoutes", self.source)
        for bound in (
            "tabDepth",
            "focusSample",
            "targetSizeMinPx",
            "linksPerRouteCap",
            "hashDeepLinksCovered",
        ):
            self.assertIn(bound, self.source, f"{bound} is not reported as a bound")

    def test_gate_summarises_by_assertion_kind_and_orders_the_table(self) -> None:
        self.assertIn("summary,", self.source)
        self.assertIn("routesFailing", self.source)
        self.assertIn("assertions.sort(order)", self.source)
        self.assertIn("localeCompare", self.source)

    def test_gate_reads_the_built_artifact_and_not_the_repository_pages(self) -> None:
        self.assertIn("join(REPO, 'build/public-alpha/site')", self.source)
        self.assertIn("process.env.TRIPTYCH_REVIEW_ROOT", self.source)
        # No route may address the repository copies: this gate exists precisely
        # because the published page differs from the page it was rendered from.
        routes = re.findall(r"'(/[^']*\.html)'", self.source)
        self.assertTrue(routes)
        for route in routes:
            self.assertNotIn("src/", route)
            self.assertNotIn("prototypes", route)

    def test_gate_covers_the_thirteen_instrument_routes_and_a_static_sample(self) -> None:
        block = self.source.split("const INSTRUMENT_ROUTES = [", 1)[1].split("];", 1)[0]
        instrument = re.findall(r"'(/[^']+)'", block)
        self.assertEqual(len(instrument), 13, instrument)
        self.assertEqual(sorted(instrument), instrument, "instrument routes are unsorted")
        for route in ("/index.html", "/about.html", "/404.html"):
            self.assertIn(f"'{route}'", self.source)
        for family in ("library", "docs", "web"):
            self.assertIn(f"directory: '{family}'", self.source)
        self.assertIn("--routes", self.source)

    def test_gate_covers_every_required_viewport_and_emulation_state(self) -> None:
        for width, height in VIEWPORTS:
            self.assertIn(f"width: {width}, height: {height}", self.source)
        self.assertIn("textScale: 2", self.source)
        self.assertIn("pageScale: 4", self.source)
        self.assertIn("'forced-colors', value: 'active'", self.source)
        self.assertIn("'prefers-reduced-motion', value: 'reduce'", self.source)

    def test_gate_reports_one_timestamp_and_leaks_no_ephemeral_port(self) -> None:
        self.assertEqual(self.source.count("new Date()"), 1)
        self.assertIn("generatedAt", self.source)
        self.assertIn("function scrub(", self.source)
        self.assertIn("--json-out", self.source)
        self.assertIn("--capture-dir", self.source)

    def test_gate_is_honest_when_no_browser_is_installed(self) -> None:
        self.assertIn("const EXIT_NO_BROWSER = 3", self.source)
        self.assertIn("TRIPTYCH_CHROME", self.source)
        self.assertIn("reports nothing rather than reporting a pass", self.source)


class CorpusBrowserGateLiveTest(unittest.TestCase):
    """One real Chromium run, deliberately opt-in because it is slow."""

    def setUp(self) -> None:
        if os.environ.get("TRIPTYCH_BROWSER_GATE") != "1":
            raise unittest.SkipTest(
                "the live browser gate is slow; set TRIPTYCH_BROWSER_GATE=1 to run it"
            )
        if browser_binary() is None:
            raise unittest.SkipTest(
                "no Chromium binary is installed; set TRIPTYCH_CHROME to one "
                "(the repository installer deliberately omits the browser)"
            )
        if not (SITE / "index.html").is_file():
            raise unittest.SkipTest(
                "no built artifact at build/public-alpha/site; run `make public-site`"
            )

    def test_gate_runs_and_emits_a_parseable_report(self) -> None:
        environment = dict(os.environ)
        environment.setdefault("TRIPTYCH_CHROME", browser_binary() or "")
        with tempfile.TemporaryDirectory() as directory:
            report_path = Path(directory) / "gate.json"
            finished = subprocess.run(
                [
                    "node", str(HARNESS),
                    "--routes", "/index.html",
                    "--json-out", str(report_path),
                ],
                cwd=ROOT, env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertIn(finished.returncode, (0, 1), finished.stderr.decode()[-2000:])
            report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertEqual(report["routes"], ["/index.html"])
        self.assertEqual(report["counts"]["states"], 9)
        recorded = {entry["name"] for entry in report["assertions"]}
        for name in MATRIX_ASSERTION_NAMES:
            self.assertIn(name, recorded)
        # `/index.html` carries no hash contract, so that one phase records
        # nothing for it; the other three are facts about any route at all.
        for name in (
            "no-script-static-truth",
            "subpath-deep-link-startup",
            "internal-links-resolve",
        ):
            self.assertIn(name, recorded)
        summarised = {entry["name"] for entry in report["summary"]}
        self.assertEqual(summarised, recorded, "the summary and the table disagree")
        for entry in report["summary"]:
            self.assertEqual(
                entry["total"],
                entry["passed"] + entry["failed"] + entry["skipped"],
                entry,
            )
        ordered = [
            (one["route"], one["state"], one["name"]) for one in report["assertions"]
        ]
        self.assertEqual(ordered, sorted(ordered), "the assertion table is unordered")
        self.assertNotIn("127.0.0.1", json.dumps(report["assertions"]))
        self.assertNotIn("127.0.0.1", json.dumps(report["summary"]))


if __name__ == "__main__":
    unittest.main()
