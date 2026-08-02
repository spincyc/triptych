"""The rights marker is enforced: a row withholds its words or carries them.

This reproduces the probe recorded as finding `nothing-enforces-withheld` in
`src/sources/inventories/act-history-repository-publication-v1.toml`. A unit of
the canon-law slice already carrying `withheld = "holy-see-post-1929"` was given
a `text`; `check` reported zero problems and `emit` then wrote the words into a
commit object underneath the banner saying they are absent.

Everything below therefore asserts a REFUSAL. A test that only walked the happy
path would leave the hole exactly where it was: 237 of 237 post-1929 canon blobs
carry the marker today and none carries words, so the current inventories pass
either way, and it is the tool and not the inventory that has to hold the line.

The three tracked slices are checked here too, so that a guard which refuses
valid existing data fails as loudly as one that admits invalid data.
"""

import importlib.machinery
import importlib.util
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
TOOL_PATH = ROOT / "tools" / "act-history"
TPT = ROOT / "tools" / "tpt"
INVENTORIES = ROOT / "src" / "sources" / "inventories"
HOLY_WEEK = INVENTORIES / "roman-holy-week-acts-v1.toml"
MISSAL = INVENTORIES / "latin-missal-acts-v1.toml"
LAW = INVENTORIES / "canon-law-acts-v1.toml"

# The probe's own string, kept verbatim so a search of any artifact this test
# leaves behind finds it. It is not a canon; nothing here handles protected text.
PASTED = "PROTECTED WORDS PASTED HERE BY MISTAKE, canon 1 of the CCEO."
COMPLAINT = "and also withholds its words; one or the other"


def load_tool():
    loader = importlib.machinery.SourceFileLoader("act_history_under_test", str(TOOL_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def run(*arguments):
    return subprocess.run(
        [str(TPT), "act-history", *arguments],
        capture_output=True, text=True, cwd=ROOT,
    )


class WithheldWordsTests(unittest.TestCase):
    """A row that both withholds its words and carries them is refused."""

    def setUp(self):
        self.tool = load_tool()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.sandbox = pathlib.Path(self.tmp.name)

    # --- helpers --------------------------------------------------------------

    def patched(self, source, old, new, name="patched.toml"):
        """A copy of a tracked inventory with one substitution, in the sandbox."""
        text = source.read_text(encoding="utf-8")
        self.assertIn(old, text, f"{source.name} no longer contains the patch site")
        target = self.sandbox / name
        target.write_text(text.replace(old, new, 1), encoding="utf-8")
        return target

    def appended(self, source, addition, name="appended.toml"):
        target = self.sandbox / name
        target.write_text(source.read_text(encoding="utf-8") + addition, encoding="utf-8")
        return target

    def probe_file(self, field="text"):
        """The probe: the first withheld canon of the Code slice, given words."""
        return self.patched(
            LAW,
            'withheld = "holy-see-post-1929"\n',
            f'withheld = "holy-see-post-1929"\n{field} = "{PASTED}"\n',
            name=f"probe-{field}.toml",
        )

    def assert_refused(self, source, *, naming):
        result = run("check", "--source", str(source))
        self.assertNotEqual(0, result.returncode, f"check passed on {source.name}")
        said = result.stdout + result.stderr
        self.assertIn(COMPLAINT, said, said)
        for phrase in naming:
            self.assertIn(phrase, said, said)
        return said

    # --- the probe, as it was run --------------------------------------------

    def test_check_refuses_the_probe(self):
        said = self.assert_refused(self.probe_file(), naming=["`text`", "unit cceo-c-1"])
        # The words are named by their field, never quoted back at the reader.
        self.assertNotIn(PASTED, said)

    def test_check_refuses_a_withheld_row_that_carries_an_incipit(self):
        # `unit_body` prints an incipit INSTEAD of the banner, so this row's
        # marker does nothing at all and the words print unannounced. It is the
        # quieter half of the same hole.
        self.assert_refused(self.probe_file("incipit"), naming=["`incipit`", "unit cceo-c-1"])

    def test_emit_cannot_write_the_probe(self):
        out = self.sandbox / "repository"
        result = run("emit", "--source", str(self.probe_file()), "--out", str(out))
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(COMPLAINT, result.stdout + result.stderr)
        self.assertFalse(out.exists(), "emit created a repository for a refused slice")

    def test_emit_refuses_without_check_being_run_first(self):
        """`check` refusing is necessary and not sufficient.

        The CLI happens to run `check` before `emit`, so a guard living only in
        `check` would be one call-ordering change away from letting the words
        through. `emit` is called directly here, on data the loader handed over,
        to show the refusal is the writer's own and not the CLI's.
        """
        data = self.tool.load(self.probe_file())
        out = self.sandbox / "direct"
        with self.assertRaises(self.tool.Problem) as refused:
            self.tool.emit(data, out)
        self.assertIn(COMPLAINT, str(refused.exception))
        self.assertFalse(out.exists(), "emit created a repository for a refused slice")

    def test_no_verb_that_writes_will_take_the_probe(self):
        """`structure` and `plate` write text and JSON a reader can read too."""
        data = self.tool.load(self.probe_file())
        for verb, arguments in (
            (self.tool.structure, (self.sandbox / "browser",)),
            (self.tool.plate, (self.sandbox / "plates",)),
            (self.tool.graph, ()),
        ):
            with self.subTest(verb=verb.__name__):
                with self.assertRaises(self.tool.Problem):
                    verb(data, *arguments)

    # --- the other row kinds that can carry both ------------------------------

    def test_check_refuses_a_departure_that_withholds_and_carries_text(self):
        """An `added` or `replaced` departure carries the words it installs.

        TASK-130 counted 11 withheld departures of 131 in the Code slice and 2
        of 13 in the missal, so this is not the rarer half of the defect. The
        probe used a unit; fixing only units would have left this open.
        """
        addition = (
            '\n[[departures]]\nact = "sacri-canones-1990"\nunit = "cceo-c-1"\n'
            'kind = "replaced"\nwithheld = "holy-see-post-1929"\n'
            f'text = "{PASTED}"\n'
            'basis = "constructed by tools/tests/test_act_history_withheld.py"\n'
        )
        self.assert_refused(
            self.appended(LAW, addition, name="departure.toml"),
            naming=["`text`", "departure"],
        )

    def test_check_refuses_an_interpretation_that_withholds_and_carries_a_responsum(self):
        """The guard this one was modelled on, still saying the same thing.

        `interpretation_block` writes `[words withheld: ...]` and then whatever
        `dubium` and `responsum` hold, exactly as `unit_body` does. The three
        tables now share one implementation, so this asserts the shared one did
        not lose the case it started from.
        """
        # In the loaded slice rather than in the file, because the first
        # `withheld` line the file holds belongs to a unit and the row wanted
        # here is an interpretation, which no textual patch can pick out.
        data = self.tool.load(LAW)
        row = next(row for row in data["interpretations"] if row.get("withheld"))
        row["responsum"] = "Ad dubium ... negative."
        with self.assertRaises(self.tool.Problem) as refused:
            self.tool.check(data)
        self.assertIn("`responsum` and also withholds its words", str(refused.exception))

    # --- the case no reading of the rows can see ------------------------------

    def replaced_by_withholding(self, clearing):
        """A `replaced` that marks a unit withheld, clearing its words or not.

        This is the combination the ROWS never show: the departure carries no
        words at all, and the unit it names carries the words it inherited.
        """
        data = self.tool.load(HOLY_WEEK)
        order, states, _ = self.tool.build(data)
        act_id = order[-1]
        unit_id, unit = next(
            (unit_id, unit) for unit_id, unit in sorted(states[act_id].units.items())
            if (unit.get("incipit") or unit.get("text"))
        )
        self.assertTrue(unit.get("incipit") or unit.get("text"))
        addition = (
            f'\n[[departures]]\nact = "{act_id}"\nunit = "{unit_id}"\n'
            'kind = "replaced"\n'
            'withheld = "a rights position asserted by this test, not a slug"\n'
            + ('incipit = ""\ntext = ""\n' if clearing else "")
            + 'basis = "constructed by tools/tests/test_act_history_withheld.py"\n'
        )
        return unit_id, self.appended(
            HOLY_WEEK, addition, name=f"replaced-{'clearing' if clearing else 'leaving'}.toml"
        )

    def test_a_replaced_departure_may_not_leave_the_inherited_words_standing(self):
        unit_id, source = self.replaced_by_withholding(clearing=False)
        self.assert_refused(source, naming=[f"unit {unit_id}"])

    def test_a_replaced_departure_that_clears_the_words_is_still_allowed(self):
        """The guard must not refuse the one honest way to withhold.

        An act that makes a published text unpublishable writes `withheld` and
        EMPTIES the words. Refusing that would leave a slice unable to record
        the withdrawal at all, which is the failure mode a blunt guard has.
        """
        _, source = self.replaced_by_withholding(clearing=True)
        result = run("check", "--source", str(source))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        # And the emitted blob carries the banner and no words.
        out = self.sandbox / "withdrawn"
        self.assertEqual(0, run("emit", "--source", str(source), "--out", str(out)).returncode)
        listed = subprocess.run(
            ["git", "grep", "-h", "incipit withheld", "HEAD"],
            cwd=out, capture_output=True, text=True,
        )
        self.assertIn("[incipit withheld: a rights position asserted by this test",
                      listed.stdout)

    # --- what must not have broken --------------------------------------------

    def test_the_three_tracked_slices_still_pass(self):
        for source in (HOLY_WEEK, MISSAL, LAW):
            with self.subTest(source=source.name):
                result = run("check", "--source", str(source))
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_the_code_slice_still_holds_the_rows_the_measurement_counted(self):
        """The guard is only worth anything if the withholdings survived it."""
        data = self.tool.load(LAW)
        units = sum(1 for row in data["units"] if row.get("withheld"))
        departures = sum(1 for row in data["departures"] if row.get("withheld"))
        interpretations = sum(1 for row in data["interpretations"] if row.get("withheld"))
        self.assertEqual((134, 11, 29), (units, departures, interpretations))


class EmittedRepositoryGcTests(unittest.TestCase):
    """`git gc` must not turn the emitted repository into one fsck calls corrupt.

    The commit-graph stores a commit date in 34 bits, so its ceiling is near the
    year 2514; the ten-thousand-year shift puts every stamp here about eighteen
    times past it. `gc` writes a commit-graph by default, and a reader who clones
    a published slice and runs routine maintenance gets a repository their own
    tools report as broken, with a date-ordered walk that puts 1570 first.
    """

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.sandbox = pathlib.Path(cls.tmp.name)
        cls.repo = cls.sandbox / "emitted"
        result = run("emit", "--source", str(HOLY_WEEK), "--out", str(cls.repo))
        assert result.returncode == 0, result.stdout + result.stderr

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    @staticmethod
    def git(repo, *arguments):
        return subprocess.run(["git", *arguments], cwd=repo, capture_output=True, text=True)

    def test_the_emitter_throws_the_switch_itself(self):
        got = self.git(self.repo, "config", "--get", "gc.writeCommitGraph")
        self.assertEqual("false", got.stdout.strip())

    def test_gc_leaves_the_emitted_repository_strict_clean(self):
        copy = self.sandbox / "gc-run"
        shutil.rmtree(copy, ignore_errors=True)
        shutil.copytree(self.repo, copy)
        self.assertEqual(0, self.git(copy, "gc").returncode)
        strict = self.git(copy, "fsck", "--strict")
        self.assertEqual(0, strict.returncode, strict.stdout + strict.stderr)
        self.assertNotIn("commit-graph", strict.stdout + strict.stderr)

    def test_the_hazard_the_switch_is_thrown_against_is_real(self):
        """Not assumed. The same gc with the switch off breaks the same repository.

        Without this the test above would pass on a git that had stopped writing
        commit-graphs, and would be asserting nothing.
        """
        copy = self.sandbox / "gc-graph"
        shutil.rmtree(copy, ignore_errors=True)
        shutil.copytree(self.repo, copy)
        self.assertEqual(0, self.git(copy, "-c", "gc.writeCommitGraph=true", "gc").returncode)
        strict = self.git(copy, "fsck", "--strict")
        self.assertNotEqual(0, strict.returncode, "the commit-graph overflow no longer bites")
        self.assertIn("commit-graph", strict.stdout + strict.stderr)


if __name__ == "__main__":
    unittest.main()
