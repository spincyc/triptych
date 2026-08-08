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

# The eleven design-neutral facts the gate exists to assert. A name removed from
# the harness is a weakened gate, and this list is what makes that visible.
ASSERTION_NAMES = (
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
)

# A visual contract does not exist yet, so the gate must not read one. Naming any
# of these would be an opinion about how the site looks rather than whether it
# works, and `getComputedStyle` is the door every such opinion comes through.
FORBIDDEN_DESIGN_TOKENS = (
    "getComputedStyle",
    "background-color",
    "backgroundColor",
    "font-family",
    "fontFamily",
    "font-weight",
    "fontWeight",
    "line-height",
    "lineHeight",
    "letter-spacing",
    "letterSpacing",
    "border-radius",
    "borderRadius",
    "box-shadow",
    "boxShadow",
    "text-align",
    "textAlign",
    "margin-",
    "padding-",
    "rgb(",
    "rgba(",
    "hsl(",
)

VIEWPORTS = ((1440, 1000), (1024, 768), (768, 1024), (393, 852), (320, 800))


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

    def test_gate_asserts_the_eleven_design_neutral_facts(self) -> None:
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
        for name in ASSERTION_NAMES:
            self.assertIn(name, recorded)
        self.assertNotIn("127.0.0.1", json.dumps(report["assertions"]))


if __name__ == "__main__":
    unittest.main()
