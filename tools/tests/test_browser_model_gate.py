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

THE GUARANTEE WAS ITSELF UNGUARDED, WHICH IS WHY THIS FILE NOW READS `make -n`.
An independent cold review returned B0/B1 as CHANGES_REQUIRED on exactly that:
this module was in neither `BROWSER_MODEL_TESTS` nor any other prerequisite of
`check`, so the one assertion written to refuse a future unlisted suite ran only
under the separately opt-in full discovery. A new suite could drive browser
JavaScript, be named nowhere, and leave `make check` green. `check-browser-models`
now has `check-browser-model-coverage` as a PREREQUISITE, and the tests below
prove the topology two ways: by reading the Makefile, and by replaying what
`make -n` says it will actually execute, which is not a claim about the Makefile
but the command list make itself produces. `test_browser_collisions.py` — a suite
the gate does run — holds the same fact from outside this file, so deleting the
prerequisite fails a test that is not the one being deleted.

It asserts nothing about how long the gate takes or how the pages look.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import NamedTuple


ROOT = Path(__file__).resolve().parents[2]
MAKEFILE = ROOT / "Makefile"
TESTS = ROOT / "tools/tests"
THIS_MODULE = Path(__file__).stem
MAKE = shutil.which("make")

# The target that runs this module, and the variable that names it. Held here as
# constants because three tests and the collision suite all speak about them.
GATE = "check-browser-models"
COVERAGE_GATE = "check-browser-model-coverage"
COVERAGE_VARIABLE = "BROWSER_MODEL_GATE_TESTS"


class Ungated(NamedTuple):
  """One suite that drives browser JavaScript and is deliberately not gated.

  `reason` is the record. `target` is the `make check` prerequisite that makes
  the reason true, or None when the exclusion does not rest on `check` reaching
  anything — and `runs_this_module` says whether that target runs THIS suite or
  merely replays the same model through the tool that owns it. Both are checked,
  so an exclusion cannot go on standing after the target it names stops being
  reached.
  """

  reason: str
  target: str | None
  runs_this_module: bool


# Every one of these is already reached by `check` through the tool that replays
# the same model, or is owned elsewhere. The map is the record: shortening it
# means gating a suite, and lengthening it means stating why a suite is not
# gated.
UNGATED_WITH_REASON = {
  "test_browser_static.py": Ungated(
    "check-browser-static already runs it inside `check`",
    "check-browser-static", True),
  "test_calendar_rubrics.py": Ungated(
    "assembly-model.js is replayed by check-calendar-rubrics inside `check`",
    "check-calendar-rubrics", False),
  "test_catena.py": Ungated(
    "catena-model.js is replayed by check-catena inside `check`",
    "check-catena", False),
  "test_document_library.py": Ungated(
    "catalogue-model.js is replayed by check-document-catalogue inside `check`",
    "check-document-catalogue", False),
  "test_source_reader.py": Ungated(
    "reader-model.js is replayed by check-source-reader inside `check`",
    "check-source-reader", False),
  "test_catena_production.py": Ungated(
    "the closed Catena E1 production suite; whether it gates `check` is that "
    "lane's decision and not this gate's to take",
    None, False),
  "test_corpus_foundation_prototype.py": Ungated(
    "an unlinked review-only prototype under src/web/browser/prototypes/, which "
    "no published route loads",
    None, False),
}


def makefile() -> str:
  return MAKEFILE.read_text(encoding="utf-8")


def named_modules(variable: str) -> list[str]:
  """The module names one Makefile variable holds, in its own order."""
  text = makefile()
  block = re.search(rf"^{re.escape(variable)} := (.*?)(?<!\\)\n(?!\t)", text, re.M | re.S)
  if block is None:
    raise AssertionError(f"the Makefile no longer declares {variable}")
  return re.findall(r"\btest_[A-Za-z0-9_]+\b", block.group(1))


def gated_modules() -> list[str]:
  return named_modules("BROWSER_MODEL_TESTS")


def coverage_modules() -> list[str]:
  return named_modules(COVERAGE_VARIABLE)


def prerequisites_of(target: str) -> list[str]:
  text = makefile()
  rule = re.search(rf"^{re.escape(target)}: (.*?)(?<!\\)\n", text, re.M | re.S)
  if rule is None:
    raise AssertionError(f"the Makefile no longer declares a `{target}:` rule")
  return rule.group(1).replace("\\\n", " ").split()


def recipe_of(target: str) -> str:
  rule = re.search(
    rf"^{re.escape(target)}:[^\n]*\n(.*?)(?=\n[^\t\n])", makefile(), re.M | re.S
  )
  if rule is None:
    raise AssertionError(f"the Makefile no longer declares a `{target}:` recipe")
  return rule.group(1)


def reached_by_check(target: str) -> bool:
  """Is `target` a prerequisite of `check`, directly or through another?"""
  seen: set[str] = set()
  frontier = list(prerequisites_of("check"))
  while frontier:
    name = frontier.pop()
    if name in seen:
      continue
    seen.add(name)
    if name == target:
      return True
    try:
      frontier.extend(prerequisites_of(name))
    except AssertionError:
      continue
  return False


def drives_browser_javascript(module: Path) -> bool:
  """The module invokes node and names something under `src/web/browser`.

  Source-level, because that is what decides whether a suite belongs in a
  browser-model gate: a module that never reaches the browser tree is not one
  this gate is short of.
  """
  source = module.read_text(encoding="utf-8")
  return bool(re.search(r"[\"']node[\"']", source)) and "web/browser" in source


def unaccounted_suites(
  directory: Path, gated: set[str], excused: set[str]
) -> list[str]:
  """Suites under `directory` that drive browser JavaScript and are named nowhere.

  Parameterised over its inputs rather than reading the repository directly, so
  the adversarial test below can put a genuine future suite in a temporary tree
  and prove this returns it.
  """
  driving = {
    path.name for path in sorted(directory.glob("test_*.py"))
    if drives_browser_javascript(path)
  }
  return sorted(driving - gated - excused)


def dry_run(target: str) -> str:
  """What make says it will execute for one target, without executing it."""
  result = subprocess.run(
    [MAKE or "make", "--no-print-directory", "-n", target],
    cwd=ROOT, capture_output=True, text=True,
  )
  if result.returncode != 0:
    raise AssertionError(
      f"`make -n {target}` failed ({result.returncode}): {result.stderr.strip()}"
    )
  return result.stdout


class GateDeclarationTest(unittest.TestCase):
  def test_check_runs_the_browser_model_gate(self):
    self.assertIn(
      GATE, prerequisites_of("check"),
      "the gate exists but `make check` does not run it, which is the state it "
      "was written to end",
    )

  def test_the_gate_is_declared_phony(self):
    phony = re.search(r"^\.PHONY: (.*?)(?<!\\)\n", makefile(), re.M | re.S)
    self.assertIsNotNone(phony)
    assert phony is not None
    declared = phony.group(1).split()
    for target in (GATE, COVERAGE_GATE):
      with self.subTest(target=target):
        self.assertIn(target, declared)

  def test_the_gate_names_its_modules_rather_than_globbing_them(self):
    """A glob would grow the gate by accident; a list grows it on purpose."""
    self.assertIn("$(BROWSER_MODEL_TESTS)", recipe_of(GATE))

  def test_check_tests_is_still_a_separate_opt_in_target(self):
    """The gate is narrow deliberately; wiring the whole suite is not its call."""
    self.assertNotIn("check-tests", prerequisites_of("check"))


class CoverageIsGatedTest(unittest.TestCase):
  """The repair for the first CHANGES_REQUIRED finding, asserted four ways.

  The coverage guarantee is only a guarantee while something runs it. These hold
  the Make topology that makes it run: a prerequisite edge from the gate, a
  recipe that really invokes the named variable, that variable really naming this
  module, and `check` really reaching the gate.
  """

  def test_the_gate_requires_the_coverage_target(self):
    self.assertIn(
      COVERAGE_GATE, prerequisites_of(GATE),
      f"`{COVERAGE_GATE}` is no longer a prerequisite of `{GATE}`, so the gate "
      "can run without the assertion that keeps its coverage honest",
    )

  def test_the_coverage_target_is_reached_by_check(self):
    self.assertTrue(
      reached_by_check(COVERAGE_GATE),
      f"nothing in `make check` reaches `{COVERAGE_GATE}`",
    )

  def test_the_coverage_recipe_runs_the_modules_it_names(self):
    recipe = recipe_of(COVERAGE_GATE)
    self.assertIn(f"$({COVERAGE_VARIABLE})", recipe)
    self.assertIn("unittest discover", recipe)

  def test_the_coverage_variable_names_this_very_module(self):
    self.assertIn(
      THIS_MODULE, coverage_modules(),
      f"{THIS_MODULE}.py is the coverage assertion; if {COVERAGE_VARIABLE} "
      "stops naming it, nothing under `make check` runs it",
    )

  def test_every_coverage_module_exists(self):
    for name in coverage_modules():
      with self.subTest(module=name):
        self.assertTrue((TESTS / f"{name}.py").is_file())

  def test_the_coverage_module_is_not_in_the_browser_model_list(self):
    """It reads the Makefile; it drives no browser.

    Putting it in BROWSER_MODEL_TESTS would be the easy repair and would make
    that list's own invariant false — every module in it drives a file under
    src/web/browser — so the two are separate variables on purpose.
    """
    self.assertNotIn(THIS_MODULE, gated_modules())
    self.assertFalse(
      drives_browser_javascript(Path(__file__)),
      "this module now drives browser JavaScript, so it belongs in "
      "BROWSER_MODEL_TESTS and this separation is no longer the right shape",
    )

  @unittest.skipIf(MAKE is None, "make is not installed; the topology cannot be replayed")
  def test_make_itself_says_the_gate_runs_the_coverage_module(self):
    """Not what the Makefile reads like — what make reports it will execute.

    The static assertions above can all be satisfied by a Makefile whose
    variables and rules have drifted apart. This asks make.
    """
    # The printed loop names the module and appends `.py` in the shell, so the
    # assertion is that make will hand THIS module to unittest, not that the
    # string `.py` appears anywhere.
    runs_this_module = re.compile(
      rf"for module in [^;]*\b{THIS_MODULE}\b[^;]*;.*?unittest discover", re.S
    )
    for target in (GATE, "check"):
      with self.subTest(target=target):
        self.assertRegex(
          dry_run(target), runs_this_module,
          f"`make -n {target}` does not hand {THIS_MODULE} to unittest",
        )

  @unittest.skipIf(MAKE is None, "make is not installed; the topology cannot be replayed")
  def test_the_dry_run_also_names_every_gated_module(self):
    """The same replay, over the list, so the loop cannot expand to nothing."""
    printed = dry_run(GATE)
    for name in gated_modules():
      with self.subTest(module=name):
        self.assertIn(name, printed)


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
    unaccounted = unaccounted_suites(TESTS, gated, set(UNGATED_WITH_REASON))
    self.assertEqual(
      unaccounted, [],
      "these suites drive browser JavaScript and are neither in "
      "BROWSER_MODEL_TESTS nor recorded as ungated with a reason: "
      f"{unaccounted}",
    )

  def test_the_ungated_record_names_only_suites_that_exist_and_are_ungated(self):
    """A stale exclusion is a reason nobody needs standing in the way of one."""
    gated = {f"{name}.py" for name in gated_modules()}
    for name, excuse in sorted(UNGATED_WITH_REASON.items()):
      with self.subTest(module=name):
        self.assertTrue((TESTS / name).is_file(), f"{name} no longer exists")
        self.assertNotIn(name, gated, f"{name} is gated; delete its excuse")
        self.assertTrue(excuse.reason.strip(), "an exclusion needs its reason")
        self.assertTrue(
          drives_browser_javascript(TESTS / name),
          f"{name} no longer drives browser JavaScript, so it needs no excuse",
        )

  def test_every_recorded_excuse_still_rests_on_something_check_reaches(self):
    """An exclusion whose target `check` stopped running is an exclusion no more.

    Five of the seven say a `check` prerequisite makes them unnecessary. That is
    a claim about the Makefile, and it is checked here rather than trusted.
    """
    for name, excuse in sorted(UNGATED_WITH_REASON.items()):
      if excuse.target is None:
        continue
      with self.subTest(module=name, target=excuse.target):
        self.assertTrue(
          reached_by_check(excuse.target),
          f"{name} is excused because `{excuse.target}` runs inside `check`, "
          "and `check` no longer reaches it",
        )
        if excuse.runs_this_module:
          self.assertIn(
            name, recipe_of(excuse.target),
            f"{name} is excused because `{excuse.target}` runs it, and that "
            "target's recipe no longer names it",
          )

  def test_an_excuse_that_names_no_target_names_no_check_coverage_either(self):
    """The two remaining exclusions rest on ownership, not on `check`.

    Recorded separately so that "owned elsewhere" and "already reached" cannot
    be confused for one another when the next suite is excused.
    """
    for name, excuse in sorted(UNGATED_WITH_REASON.items()):
      if excuse.target is not None:
        continue
      with self.subTest(module=name):
        self.assertFalse(excuse.runs_this_module)
        self.assertNotIn("inside `check`", excuse.reason)


class FutureSuiteOmissionTest(unittest.TestCase):
  """The failure mode itself, driven rather than described.

  A suite that drives browser JavaScript and is named in neither list must make
  the coverage assertion fail. Proved over a temporary tree so the repository
  keeps no synthetic module, and paired with the topology tests above: the
  predicate fires, and the thing that runs the predicate is inside `make check`.
  """

  # Assembled from fragments rather than written out, because the predicate is a
  # source-level one: a literal quoted node invocation beside the browser path
  # would make THIS module look like a suite that drives browser JavaScript, and
  # `test_the_coverage_module_is_not_in_the_browser_model_list` is right to say
  # it does not.
  SUITE = (
    "import subprocess, unittest\n"
    "class FutureBrowserModelTests(unittest.TestCase):\n"
    "  def test_it_drives_a_browser_model(self):\n"
    "    subprocess.run(['" + "no" + "de" + "', '-e', ''], cwd='src/" + "web/" + "browser')\n"
  )

  def test_an_unlisted_javascript_driving_suite_is_reported_as_unaccounted(self):
    with tempfile.TemporaryDirectory() as temporary:
      directory = Path(temporary)
      (directory / "test_future_browser_suite.py").write_text(self.SUITE, encoding="utf-8")
      self.assertEqual(
        unaccounted_suites(directory, set(), set()),
        ["test_future_browser_suite.py"],
      )

  def test_gating_it_or_excusing_it_are_the_two_ways_to_account_for_it(self):
    with tempfile.TemporaryDirectory() as temporary:
      directory = Path(temporary)
      (directory / "test_future_browser_suite.py").write_text(self.SUITE, encoding="utf-8")
      self.assertEqual(
        unaccounted_suites(directory, {"test_future_browser_suite.py"}, set()), [])
      self.assertEqual(
        unaccounted_suites(directory, set(), {"test_future_browser_suite.py"}), [])

  def test_a_suite_that_touches_no_browser_is_not_something_the_gate_is_short_of(self):
    with tempfile.TemporaryDirectory() as temporary:
      directory = Path(temporary)
      (directory / "test_unrelated.py").write_text(
        "import unittest\n"
        "class T(unittest.TestCase):\n"
        "  def test_nothing(self):\n"
        "    self.assertTrue(True)\n",
        encoding="utf-8",
      )
      self.assertEqual(unaccounted_suites(directory, set(), set()), [])

  def test_the_live_repository_would_report_a_missing_suite_too(self):
    """The same predicate over the real tree, with one real suite un-named.

    `test_browser_collisions` is gated. Removing it from both lists — in the
    arguments, not in the tree — must produce exactly it, which proves the live
    assertion is one substitution away from failing rather than vacuously green.
    """
    gated = {f"{name}.py" for name in gated_modules()} - {"test_browser_collisions.py"}
    self.assertEqual(
      unaccounted_suites(TESTS, gated, set(UNGATED_WITH_REASON)),
      ["test_browser_collisions.py"],
    )


if __name__ == "__main__":
  unittest.main()
