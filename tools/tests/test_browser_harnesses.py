#!/usr/bin/env python3
"""Keeps the Chromium reader harnesses discovered, syntactic, and runnable.

`tools/tests/*_browser.mjs` are dependency-free CDP harnesses that nothing in the
suite ran: no Makefile target invoked them and no Python test did more than
`node --check` one of them. They were therefore believed broken for a long time,
and they were not. Most serve their pages out of
`build/public-alpha/preview`, so in a checkout that has never run
`make public-preview` every request 404s and the harness reports
"Timed out waiting for ... readiness" — a missing build artifact wearing the
costume of a code defect.

This module removes both failure modes. Without a browser it still asserts the
set of harnesses, checks their syntax, and pins the preview dependency in place
so nobody "fixes" the data root without also arranging for the build. With
`TRIPTYCH_BROWSER_HARNESSES=1` it runs all of them for real, parses the JSON report
each one emits — from stdout, or from stderr, because the propers harness writes
its failing report to stderr and a parser that only reads stdout would score that
run as zero assertions — and requires every recorded assertion and process exit
to be green. Console, request, and HTTP diagnostics are checked separately so a
nominal assertion count cannot conceal a page problem.
"""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TESTS = ROOT / "tools/tests"
# Every harness addresses the preview build as its data root. That is the fact
# which makes `make public-preview` a real prerequisite rather than a habit, so it
# is asserted rather than remembered.
PREVIEW_ROOT = "build/public-alpha/preview"
PREVIEW = ROOT / PREVIEW_ROOT

# Exact all-green contracts: harness -> expected passing and total assertions.
# Adding or removing a harness assertion is a deliberate contract change; a
# partial result, a new unaccounted assertion, or a nonzero exit all fail here.
ASSERTION_COUNTS = {
    "day_reader_choices_browser.mjs": 8,
    "day_reader_integration_browser.mjs": 43,
    "liturgy_reader_shell_browser.mjs": 18,
    "liturgy_reader_visual_reset_browser.mjs": 26,
    "propers_reader_integration_browser.mjs": 40,
}

# Review-only prototype harnesses serve the tracked tree directly rather than
# the preview artifact, and each keeps its floor in its own test module
# (test_corpus_foundation_prototype.py), so they are accounted for here without
# a preview requirement or a duplicate contract.
PROTOTYPE_HARNESSES = frozenset({"corpus_foundation_prototype_browser.mjs"})

# The diagnostic arrays a harness keeps beside its assertions. A console error,
# a dead request or a non-200 is a defect in the page whoever ran the gate should
# hear about, and it says so with the offending entries rather than only an exit
# number.
PROBLEM_KEYS = ("consoleProblems", "failedRequests", "httpProblems")

# The propers harness keeps no such arrays; it folds the same two signals into its
# `failures` list under these fixed names, so they are read from there instead.
PROBLEM_FAILURE_NAMES = frozenset({"console", "network", "harness"})

BROWSER_CANDIDATES = ("/usr/bin/chromium", "/usr/bin/google-chrome-stable")

# A single harness drives Chromium through dozens of navigations; the slowest of
# the five takes minutes on a warm host. The timeout exists to bound a hang, not
# to bound a slow run.
HARNESS_TIMEOUT_SECONDS = 1800


def discovered_harnesses() -> list[str]:
    return sorted(path.name for path in TESTS.glob("*_browser.mjs"))


def browser_binary() -> str | None:
    named = os.environ.get("TRIPTYCH_CHROME")
    if named:
        return named if Path(named).is_file() else None
    for candidate in BROWSER_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    return None


def parse_report(stdout: str, stderr: str) -> dict | None:
    """Read the harness's JSON report from stdout, falling back to stderr.

    `propers_reader_integration_browser.mjs` prints its failing report with
    `console.error`. Reading stdout alone would find nothing there and mistake a
    partial run for a run that asserted nothing at all.
    """
    for stream in (stdout, stderr):
        text = stream.strip()
        if not text:
            continue
        for candidate in (text, text[text.find("{"): text.rfind("}") + 1]):
            if not candidate.startswith("{"):
                continue
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
    return None


def assertion_counts(report: dict) -> tuple[int, int]:
    """Return (passed, total) over whichever key holds the per-assertion records.

    Three harnesses record them under `assertions`; the propers harness records
    them under `results` and additionally uses `assertions` for a bare count on
    its passing path, so a list is required before the key is believed.
    """
    for key in ("assertions", "results"):
        entries = report.get(key)
        if isinstance(entries, list):
            passed = sum(1 for entry in entries if entry.get("status") == "pass")
            return passed, len(entries)
    return 0, 0


def recorded_problems(report: dict) -> dict[str, list]:
    """Return the non-empty diagnostic arrays, keyed by where they were found."""
    found = {}
    for key in PROBLEM_KEYS:
        entries = report.get(key)
        if not isinstance(entries, list):
            continue
        # The harnesses discount canceled requests themselves: a navigation that
        # supersedes an in-flight fetch cancels it, which is the browser working.
        live = [
            entry for entry in entries
            if not (isinstance(entry, dict) and entry.get("canceled"))
        ]
        if live:
            found[key] = live
    folded = [
        entry for entry in report.get("failures", [])
        if isinstance(entry, dict) and entry.get("name") in PROBLEM_FAILURE_NAMES
    ]
    if folded:
        found["failures"] = folded
    return found


class BrowserHarnessStructureTest(unittest.TestCase):
    """Checks that hold on every host, browser or no browser."""

    def test_every_expected_harness_is_present_and_none_is_unaccounted_for(self) -> None:
        self.assertEqual(
            discovered_harnesses(),
            sorted(set(ASSERTION_COUNTS) | PROTOTYPE_HARNESSES),
            "a *_browser.mjs harness appeared or vanished; add or remove its count "
            "(or its PROTOTYPE_HARNESSES entry) deliberately rather than letting "
            "the set drift",
        )

    def test_every_harness_parses(self) -> None:
        for name in discovered_harnesses():
            with self.subTest(harness=name):
                subprocess.run(["node", "--check", str(TESTS / name)], cwd=ROOT, check=True)

    def test_every_harness_reads_the_preview_build(self) -> None:
        for name in discovered_harnesses():
            if name in PROTOTYPE_HARNESSES:
                continue
            with self.subTest(harness=name):
                source = (TESTS / name).read_text(encoding="utf-8")
                self.assertIn(
                    PREVIEW_ROOT,
                    source,
                    f"{name} no longer addresses {PREVIEW_ROOT}; if the data root moved, "
                    "the Makefile prerequisite and this test have to move with it",
                )

    def test_every_harness_can_be_pointed_at_an_installed_browser(self) -> None:
        for name in discovered_harnesses():
            with self.subTest(harness=name):
                source = (TESTS / name).read_text(encoding="utf-8")
                self.assertIn("TRIPTYCH_CHROME", source)


class BrowserHarnessLiveTest(unittest.TestCase):
    """The real Chromium runs, opt-in because together they take several minutes."""

    def setUp(self) -> None:
        if os.environ.get("TRIPTYCH_BROWSER_HARNESSES") != "1":
            raise unittest.SkipTest(
                "the live browser harnesses are slow; set TRIPTYCH_BROWSER_HARNESSES=1 "
                "to run them"
            )
        self.browser = browser_binary()
        if self.browser is None:
            raise unittest.SkipTest(
                "no Chromium binary was found at TRIPTYCH_CHROME, /usr/bin/chromium, or "
                "/usr/bin/google-chrome-stable; set TRIPTYCH_CHROME to one (the "
                "repository installer deliberately omits the browser)"
            )
        if not (PREVIEW / "liturgy/day.html").is_file() or not (PREVIEW / "browse").is_dir():
            raise unittest.SkipTest(
                f"no preview build at {PREVIEW_ROOT}; run `make public-preview`. "
                "A missing build artifact is not a code defect, so this is a skip and not "
                "a failure"
            )

    # Each harness costs tens of seconds of real Chromium, and the assertion
    # contract and problem arrays are two readings of one run rather than two runs.
    runs: dict[str, tuple[int, dict | None, str]] = {}

    def run_harness(self, name: str) -> tuple[int, dict | None, str]:
        if name in self.runs:
            return self.runs[name]
        environment = dict(os.environ)
        environment["TRIPTYCH_CHROME"] = self.browser
        finished = subprocess.run(
            ["node", str(TESTS / name)],
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=HARNESS_TIMEOUT_SECONDS,
        )
        stdout = finished.stdout.decode("utf-8", "replace")
        stderr = finished.stderr.decode("utf-8", "replace")
        self.runs[name] = (finished.returncode, parse_report(stdout, stderr), stderr)
        return self.runs[name]

    def test_every_harness_runs_and_passes_its_exact_contract(self) -> None:
        for name, expected in sorted(ASSERTION_COUNTS.items()):
            with self.subTest(harness=name):
                status, report, stderr = self.run_harness(name)
                self.assertIsNotNone(
                    report,
                    f"{name} exited {status} without a parseable JSON report on either "
                    f"stream; last stderr:\n{stderr[-2000:]}",
                )
                assert report is not None
                passed, total = assertion_counts(report)
                # Zero assertions is never a result. It means the report was not
                # found or not understood, and softening it would restore exactly
                # the blind spot the stdout/stderr fallback exists to close.
                self.assertGreater(
                    total, 0, f"{name} exited {status} having recorded no assertions at all"
                )
                self.assertEqual(
                    (status, passed, total),
                    (0, expected, expected),
                    f"{name} must complete its exact live contract with a zero exit status",
                )

    def test_no_harness_records_a_console_request_or_http_problem(self) -> None:
        for name in sorted(ASSERTION_COUNTS):
            with self.subTest(harness=name):
                status, report, stderr = self.run_harness(name)
                self.assertIsNotNone(
                    report,
                    f"{name} exited {status} without a parseable JSON report on either "
                    f"stream; last stderr:\n{stderr[-2000:]}",
                )
                assert report is not None
                found = recorded_problems(report)
                self.assertEqual(
                    found,
                    {},
                    f"{name} recorded page problems: "
                    + json.dumps(found, indent=2, default=str)[:4000],
                )


if __name__ == "__main__":
    unittest.main()
