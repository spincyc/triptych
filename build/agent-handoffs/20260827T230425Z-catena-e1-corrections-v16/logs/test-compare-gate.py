#!/usr/bin/env python3
"""THE GATE COMPARISON'S THREE FIGURES, EACH PROVED SEPARATELY.

V15 shipped `compare-gate.py` with no test file at all, and the V15 review
found what that cost: "its diagnostic collapses 2,290 rows to 17 names while
calling them assertion objects".

The mechanism was one line. `walk()` built each row's identity from the
DIAGNOSTIC NAME alone -- `route` and `state` were read and never used in the
key -- and the caller poured the resulting tuples into a dict. The gate runs
seventeen diagnostics across 171 pages, so 2,290 rows arrived at 17 keys and
2,273 of them silently overwrote an earlier one. Then it printed `assertion
objects, base: 17`, which is true of neither quantity: there are not 17
assertion objects, and 17 is not a count of objects.

WHAT WAS NOT WRONG, AND IS ASSERTED HERE TO STAY THAT WAY: the verdict. It
comes from `strip(base) == strip(head)`, a whole-report comparison minus four
named volatile fields, and it never depended on the walk at all. Every test
below that changes a row also asserts the verdict moves with it.
"""

from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "compare-gate.py"

#: The seventeen diagnostics the real gate runs, from the V15 reports.
NAMES = (
    "escape-key-does-not-throw", "focus-indicator-differs-from-resting",
    "hash-deep-link-is-honoured", "html-element-has-lang",
    "interactive-controls-have-accessible-names", "internal-links-resolve",
    "no-console-errors", "no-failed-requests",
    "no-horizontal-overflow-at-320", "no-script-static-truth",
    "primary-controls-meet-target-size", "single-h1-element",
    "single-main-element", "skip-link-targets-existing-element",
    "subpath-deep-link-startup", "tab-traversal-reaches-visible-controls",
    "title-present-and-unduplicated",
)


def report(pages: int = 10, names=NAMES, status: str = "pass",
           detail: str = "", generated: str = "2026-08-26T19:24:46Z"):
    """A gate report shaped like the real one: pages, each with assertions.

    `counts.assertions` is the gate's OWN tally and the walk is proved
    against it, so a fixture whose shape drifts from its own count is itself
    a test of the refusal.
    """
    page_rows = []
    for index in range(pages):
        page_rows.append({
            "route": f"/route-{index % 3}",
            "state": f"state-{index % 2}",
            "url": f"https://example.invalid/page-{index}",
            "assertions": [
                {"name": one, "status": status, "detail": detail}
                for one in names
            ],
        })
    return {
        "generatedAt": generated,
        "root": "/some/absolute/path/that/differs",
        "durationMs": 1234,
        "browser": "chromium-1.2.3",
        "counts": {"routes": 3, "states": 2, "pages": pages,
                   "assertions": pages * len(names),
                   "passed": pages * len(names), "failed": 0, "skipped": 0},
        "summary": [{"name": one, "total": pages, "passed": pages,
                     "failed": 0, "skipped": 0, "routesFailing": 0}
                    for one in names],
        "pages": page_rows,
    }


class CompareGate(unittest.TestCase):

    def run_tool(self, base: dict, head: dict):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            (root / "base.json").write_text(json.dumps(base), encoding="utf-8")
            (root / "head.json").write_text(json.dumps(head), encoding="utf-8")
            done = subprocess.run(
                [sys.executable, "-B", str(TOOL),
                 str(root / "base.json"), str(root / "head.json")],
                capture_output=True, text=True)
            return done.returncode, done.stdout + done.stderr

    # -- the control -----------------------------------------------------

    def test_two_equal_reports_pass(self):
        # WITHOUT THIS EVERY REFUSAL BELOW IS VACUOUS.
        code, said = self.run_tool(report(), report())
        self.assertEqual(code, 0, said)
        self.assertIn("whole report identical under the named volatile "
                      "exclusions", said)
        self.assertIn(": True", said)

    def test_the_volatile_fields_really_are_excluded(self):
        """The four named exclusions, and only those four."""
        head = report(generated="2026-08-26T19:40:51Z")
        head["root"] = "/a/completely/different/root"
        head["durationMs"] = 99999
        head["browser"] = "chromium-9.9.9"
        code, said = self.run_tool(report(), head)
        self.assertEqual(code, 0, said)
        self.assertIn("browser, durationMs, generatedAt, root", said)

    # -- THE DEFECT: ROWS ARE NOT NAMES ----------------------------------

    def test_rows_and_diagnostic_names_are_reported_as_two_figures(self):
        """THE V15 DEFECT, EXACTLY.

        Ten pages by seventeen diagnostics is 170 assertion ROWS carrying 17
        NAMES. V15 printed `assertion objects, base: 17`.
        """
        code, said = self.run_tool(report(pages=10), report(pages=10))
        self.assertEqual(code, 0, said)
        self.assertIn("base assertion rows (every assertion object): 170",
                      said)
        self.assertIn("base distinct diagnostic names: 17", said)
        self.assertIn("distinct row identities, base: 170", said)
        self.assertIn("comparison: assertion_rows 170, "
                      "distinct_diagnostic_names 17, whole_report_equal True",
                      said)
        self.assertNotIn("assertion objects, base: 17", said)

    def test_the_walk_is_proved_against_the_reports_own_count(self):
        """A walk that disagrees with the report it walked is partial, and a
        comparison built on it cannot claim to be over the whole set."""
        base = report(pages=10)
        base["counts"]["assertions"] = 999
        code, said = self.run_tool(base, report(pages=10))
        self.assertEqual(code, 2, said)
        self.assertIn("the report declares 999 assertion rows and this walk "
                      "found 170", said)
        self.assertIn("not over the whole report", said)

    def test_every_row_is_its_own_identity(self):
        """171 pages' worth of `single-h1-element` are 171 rows, not one.

        V15 keyed on the name, so 170 of them were discarded before any
        comparison ran -- and a status change on any of the discarded 170
        would have been invisible.
        """
        base = report(pages=10)
        head = report(pages=10)
        head["pages"][7]["assertions"][3]["status"] = "fail"
        code, said = self.run_tool(base, head)
        self.assertEqual(code, 1, said)
        self.assertIn("rows with changed status: 1", said)
        self.assertIn("pass -> fail", said)
        self.assertIn("whole report identical under the named volatile "
                      "exclusions (browser, durationMs, generatedAt, root): "
                      "False", said)

    def test_a_status_change_on_a_late_page_is_not_swallowed(self):
        """THE MATCHED NEGATIVE FOR THE COLLAPSE.

        Under the V15 key the LAST row for a name won, so a change on any
        earlier page vanished. This changes the FIRST page's row and asserts
        it is seen.
        """
        base = report(pages=10)
        head = report(pages=10)
        head["pages"][0]["assertions"][0]["status"] = "skip"
        code, said = self.run_tool(base, head)
        self.assertEqual(code, 1, said)
        self.assertIn("rows with changed status: 1", said)

    def test_a_detail_change_is_reported_per_row(self):
        base = report(pages=4, detail="the same detail")
        head = report(pages=4, detail="the same detail")
        head["pages"][2]["assertions"][1]["detail"] = "something else"
        code, said = self.run_tool(base, head)
        self.assertEqual(code, 1, said)
        self.assertIn("rows with changed detail: 1", said)

    def test_the_per_diagnostic_breakdown_is_printed(self):
        """The collapse is made VISIBLE rather than applied silently."""
        code, said = self.run_tool(report(pages=10), report(pages=10))
        self.assertEqual(code, 0, said)
        for one in NAMES:
            self.assertIn(f"10  {one}", said)

    def test_a_diagnostic_present_on_one_side_only_is_named(self):
        head = report(pages=4, names=NAMES[:-1])
        head["counts"]["assertions"] = 4 * (len(NAMES) - 1)
        code, said = self.run_tool(report(pages=4), head)
        self.assertEqual(code, 1, said)
        self.assertIn("diagnostic names only in base: "
                      "['title-present-and-unduplicated']", said)

    def test_the_row_and_name_counts_differ_and_both_are_stated(self):
        """The whole point: the two figures are not the same number, and a
        reader is given both rather than one labelled as the other."""
        code, said = self.run_tool(report(pages=3), report(pages=3))
        self.assertEqual(code, 0, said)
        self.assertIn("base assertion rows (every assertion object): 51",
                      said)
        self.assertIn("base distinct diagnostic names: 17", said)

    def test_the_whole_report_verdict_survives_the_walk_being_wrong(self):
        """THE PRESERVED PROOF. `strip()`-equality never used the walk, and a
        report the walk cannot enumerate is still compared whole."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("cg", TOOL)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        base = report(pages=2)
        head = report(pages=2)
        self.assertEqual(module.strip(base), module.strip(head))
        head["pages"][0]["url"] = "https://example.invalid/other"
        self.assertNotEqual(module.strip(base), module.strip(head),
                            "a field outside `assertions` still moves the "
                            "whole-report verdict")

    def test_the_summary_comparison_is_still_reported(self):
        base = report(pages=4)
        head = report(pages=4)
        head["summary"][0]["failed"] = 1
        code, said = self.run_tool(base, head)
        self.assertEqual(code, 1, said)
        self.assertIn("summary equal: False", said)

    def test_the_real_v15_reports_reproduce_the_published_figures(self):
        """CALIBRATION AGAINST THE REAL PACKAGE, when it is on this machine.

        The V15 archive's two browser reports carry 2,290 assertion rows over
        17 diagnostic names at each endpoint, and their normalized whole
        reports are equal. All three figures are asserted, separately.
        """
        package = None
        for candidate in HERE.parent.glob(
                "*/build/agent-handoffs/*catena-e1-corrections-v15"):
            if (candidate / "logs").is_dir():
                package = candidate
                break
        if package is None:
            self.skipTest("the V15 package is not extracted on this machine")
        parent = next(package.glob("logs/attempt-*/browser-gate-parent.json"),
                      None)
        head = next(package.glob("logs/attempt-*/browser-gate-head.json"),
                    None)
        if parent is None or head is None:
            self.skipTest("the V15 browser reports are not present")
        done = subprocess.run(
            [sys.executable, "-B", str(TOOL), str(parent), str(head)],
            capture_output=True, text=True)
        said = done.stdout + done.stderr
        self.assertEqual(done.returncode, 0, said)
        self.assertIn("base assertion rows (every assertion object): 2290",
                      said)
        self.assertIn("base assertion rows the report itself declares: 2290",
                      said)
        self.assertIn("base distinct diagnostic names: 17", said)
        self.assertIn("distinct row identities, base: 2290", said)
        self.assertIn("comparison: assertion_rows 2290, "
                      "distinct_diagnostic_names 17, whole_report_equal True",
                      said)


if __name__ == "__main__":
    unittest.main(verbosity=2)
