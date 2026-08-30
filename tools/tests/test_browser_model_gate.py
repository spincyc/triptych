#!/usr/bin/env python3
"""What `make check` asserts about the browser models, and what it does not.

Four browser models were exercised by `make check` — `assembly-model.js`
through `check-calendar-rubrics`, `catena-model.js` through `check-catena`,
`reader-model.js` through `check-source-reader`, `catalogue-model.js` through
`check-document-catalogue`. Every other model, every reader-integration
contract, and the corpus foundation's own recorded evidence — the published
hash contracts, the selector and plumbing collisions, the two truthfulness
suites — lived behind `check-tests`, a target `make check` does not run and
which nothing outside the Makefile mentions. A change to `code-model.js`,
`reader-state.js`, `day.js` or `ordinary-seating.js` therefore reached the
deploy gates with no assertion made about it.

`check-browser-models` closes that. This module holds the gate to being what it
claims: the modules it names exist, each of them really does drive a file under
`src/web/browser` rather than merely sitting in the list, and — the assertion
that matters — no module in `tools/tests` that drives browser JavaScript under
node can go missing from the gate silently. A suite that is not gated has to be
written down here with the reason it is not, so the gate's coverage is a
statement rather than whatever the list happens to contain.

It asserts nothing about how long the gate takes or how the pages look.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAKEFILE = ROOT / "Makefile"
TESTS = ROOT / "tools/tests"

# A module that runs browser JavaScript under node and is deliberately not in
# the gate, with the reason. Every one of these is already reached by `check`
# through the tool that replays the same model, or is owned elsewhere. The map
# is the record: shortening it means gating a suite, and lengthening it means
# stating why a suite is not gated.
UNGATED_WITH_REASON = {
  "test_browser_static.py":
    "check-browser-static already runs it inside `check`",
  "test_calendar_rubrics.py":
    "assembly-model.js is replayed by check-calendar-rubrics inside `check`",
  "test_catena.py":
    "catena-model.js is replayed by check-catena inside `check`",
  "test_document_library.py":
    "catalogue-model.js is replayed by check-document-catalogue inside `check`",
  "test_source_reader.py":
    "reader-model.js is replayed by check-source-reader inside `check`",
  "test_catena_production.py":
    "the closed Catena E1 production suite; whether it gates `check` is that "
    "lane's decision and not this gate's to take",
  "test_corpus_foundation_prototype.py":
    "an unlinked review-only prototype under src/web/browser/prototypes/, which "
    "no published route loads",
}


def makefile() -> str:
  return MAKEFILE.read_text(encoding="utf-8")


def gated_modules() -> list[str]:
  """The module names the Makefile variable holds, in its own order."""
  text = makefile()
  block = re.search(r"^BROWSER_MODEL_TESTS := (.*?)(?<!\\)\n(?!\t)", text, re.M | re.S)
  if block is None:
    raise AssertionError("the Makefile no longer declares BROWSER_MODEL_TESTS")
  return re.findall(r"\btest_[A-Za-z0-9_]+\b", block.group(1))


def prerequisites_of(target: str) -> list[str]:
  text = makefile()
  rule = re.search(rf"^{re.escape(target)}: (.*?)(?<!\\)\n", text, re.M | re.S)
  if rule is None:
    raise AssertionError(f"the Makefile no longer declares a `{target}:` rule")
  return rule.group(1).replace("\\\n", " ").split()


def drives_browser_javascript(module: Path) -> bool:
  """The module invokes node and names something under `src/web/browser`.

  Source-level, because that is what decides whether a suite belongs in a
  browser-model gate: a module that never reaches the browser tree is not one
  this gate is short of.
  """
  source = module.read_text(encoding="utf-8")
  return bool(re.search(r"[\"']node[\"']", source)) and "web/browser" in source


class GateDeclarationTest(unittest.TestCase):
  def test_check_runs_the_browser_model_gate(self):
    self.assertIn(
      "check-browser-models", prerequisites_of("check"),
      "the gate exists but `make check` does not run it, which is the state it "
      "was written to end",
    )

  def test_the_gate_is_declared_phony(self):
    phony = re.search(r"^\.PHONY: (.*?)(?<!\\)\n", makefile(), re.M | re.S)
    self.assertIsNotNone(phony)
    assert phony is not None
    self.assertIn("check-browser-models", phony.group(1).split())

  def test_the_gate_names_its_modules_rather_than_globbing_them(self):
    """A glob would grow the gate by accident; a list grows it on purpose."""
    rule = re.search(
      r"^check-browser-models:\n(.*?)(?=\n[^\t\n])", makefile(), re.M | re.S
    )
    self.assertIsNotNone(rule, "the check-browser-models recipe is missing")
    assert rule is not None
    self.assertIn("$(BROWSER_MODEL_TESTS)", rule.group(1))

  def test_check_tests_is_still_a_separate_opt_in_target(self):
    """The gate is narrow deliberately; wiring the whole suite is not its call."""
    self.assertNotIn("check-tests", prerequisites_of("check"))


class GateContentTest(unittest.TestCase):
  def test_every_gated_module_exists(self):
    modules = gated_modules()
    self.assertGreaterEqual(len(modules), 8, "the gate lost most of its modules")
    self.assertEqual(len(modules), len(set(modules)), "a module is named twice")
    for name in modules:
      with self.subTest(module=name):
        self.assertTrue((TESTS / f"{name}.py").is_file(), f"{name}.py is not in tools/tests")

  def test_every_gated_module_really_drives_browser_javascript(self):
    for name in gated_modules():
      with self.subTest(module=name):
        self.assertTrue(
          drives_browser_javascript(TESTS / f"{name}.py"),
          f"{name}.py neither invokes node nor names anything under "
          "src/web/browser, so it does not belong in a browser-model gate",
        )

  def test_no_browser_model_suite_is_ungated_without_a_recorded_reason(self):
    """The one assertion that keeps the gate's coverage honest as the tree grows.

    A new suite that drives browser JavaScript is either gated or written into
    UNGATED_WITH_REASON. Silence is the failure, because silence is how the
    models ended up protected by a sha256 pin and nothing else.
    """
    gated = {f"{name}.py" for name in gated_modules()}
    driving = {
      path.name for path in sorted(TESTS.glob("test_*.py"))
      if drives_browser_javascript(path)
    }
    self.assertTrue(driving, "no suite in tools/tests drives browser JavaScript")
    unaccounted = sorted(driving - gated - set(UNGATED_WITH_REASON))
    self.assertEqual(
      unaccounted, [],
      "these suites drive browser JavaScript and are neither in "
      "BROWSER_MODEL_TESTS nor recorded as ungated with a reason: "
      f"{unaccounted}",
    )

  def test_the_ungated_record_names_only_suites_that_exist_and_are_ungated(self):
    """A stale exclusion is a reason nobody needs standing in the way of one."""
    gated = {f"{name}.py" for name in gated_modules()}
    for name, reason in sorted(UNGATED_WITH_REASON.items()):
      with self.subTest(module=name):
        self.assertTrue((TESTS / name).is_file(), f"{name} no longer exists")
        self.assertNotIn(name, gated, f"{name} is gated; delete its excuse")
        self.assertTrue(reason.strip(), "an exclusion needs its reason")


if __name__ == "__main__":
  unittest.main()
