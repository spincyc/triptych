"""Two lines rejoin only at a documented reception, and the guard is proved.

TASK-141. `tools/act-history` refused every multi-parent edge whose parents
stood on two lines -- `merges across lines; lines never rejoin` -- while
`guidance/time-machine.md` Rule 2 permits a merge WHEREVER RECEPTION IS
DOCUMENTED WITH THE ACT CITED and restricts it to no one line, and section 3
calls a translation drawing on a Latin typical edition an interchange in terms.
The code and the design promise disagreed, and the code refused the CLAIM by
refusing the SHAPE.

Everything below is built on a CONSTRUCTED slice, in a sandbox, because the
three tracked slices record no rejoining at all and a guard exercised only
against data that never trips it is a guard nobody has run. The fixture extends
the Holy Week tracer with a vernacular line whose second station stands on its
own predecessor AND on the 1962 typical edition -- the first of the two cases
the maintainer's all-Latin-rites ruling makes real. Nothing in it is a
historical claim: no book, decree, authority or date in the constructed rows is
asserted of the world, and the test says so in the fixture's own prose.

Half of these tests assert a REFUSAL, and that half is the point. A cross-line
merge asserts MORE than a merge on one line -- not only that a synthesis
occurred but that one tradition received from another -- so it is held above the
ordinary bar and not merely at it, and each thing it must cite is removed here
one at a time to show the tool notices.
"""

import importlib.machinery
import importlib.util
import pathlib
import re
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

# The station the constructed line receives from, and the line it stands on.
RECEIVED = "editio-typica-1962"
RECEIVED_LINE = "typica"
RECEIVING = "vernacular-second-1969"

# The fixture, and the whole of what it claims: nothing. It is written out in
# full rather than assembled from fragments, because a reader of a failing test
# has to be able to see the shape being asserted without running anything.
FIXTURE = """

# --- Constructed by tools/tests/test_act_history_reception.py ----------------
#
# NOT A HISTORICAL CLAIM. The line, the two acts, the instruments and the dates
# below are invented to exercise one shape: an official vernacular edition
# standing on its own predecessor AND on the typical edition it implements, at
# its own lag. No book, decree, authority or date here is asserted of the world,
# and nothing in this fixture may be read into any tracked slice.

[[lines]]
id = "vernacular"
label = "A constructed vernacular line"
note = "Constructed by the reception test. It exists to be received into."

[[acts]]
id = "vernacular-first-1965"
station_kind = "promulgated"
line = "vernacular"
kind = "promulgation"
date = "1965-03-07"
authority = "A constructed conference of bishops"
instrument = "A constructed decree approving a first vernacular edition"
title = "A first vernacular edition is approved"
parents = []
root_basis = "Constructed. The record of this line starts here because the fixture does."
act_citation = "cited-externally"
citation = "tools/tests/test_act_history_reception.py"
read_from = "not-read"
effect = "Opens the line and its book."
effect_established = true

[[acts]]
id = "{receiving}"
station_kind = "promulgated"
line = "vernacular"
kind = "promulgation"
date = "1969-11-30"
authority = "A constructed conference of bishops"
instrument = "A constructed decree approving the second vernacular edition"
title = "The second vernacular edition implements the typical edition"
parents = {parents}
parent_kind = "act-states-it"
parent_basis = "Constructed: the decree recites the edition it replaces."
reception_basis = \"\"\"
Constructed. The two parents converge because the book is the vernacular line's
own and the norm it renders is the other line's: neither alone accounts for it.
\"\"\"
act_citation = "{act_citation}"{extra}
citation = "tools/tests/test_act_history_reception.py"
read_from = "not-read"
effect = "Carries the received norm into this line's book."
effect_established = true
{receptions}
[[masses]]
id = "vernacular-ordo"
at = "vernacular-first-1965"
book = "vernacular"
title = "A constructed Order of Mass"
day = "every day"
hour = "as appointed"

[[units]]
id = "vern.introitus"
at = "vernacular-first-1965"
mass = "vernacular-ordo"
slot = "introitus"
name = "Introit"
order = 10
incipit = "A constructed incipit, standing on this line from its first station."
read_from = "not-read"

[[units]]
id = "vern.oratio"
at = "{receiving}"
mass = "vernacular-ordo"
slot = "oratio"
name = "Collect"
order = 20
incipit = "A constructed collect, entering at the station that received."
read_from = "not-read"
"""

# The reception itself, kept apart so each thing it must cite can be taken away
# one at a time. In TOML this stands after the act's own keys, which is what
# `[[acts.receptions]]` means: one table per received parent.
RECEPTION = """
[[acts.receptions]]
from = "{source}"
kind = "{kind}"
instrument = "A constructed decree of the receiving conference"
citation = "tools/tests/test_act_history_reception.py, which is not a source"
basis = \"\"\"
Constructed. It stands for the sentence a real reception has to have: the
receiving act's own instrument saying which edition it renders, read somewhere a
reader can check.
\"\"\"
"""


def load_tool():
    loader = importlib.machinery.SourceFileLoader("act_history_reception", str(TOOL_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def run(*arguments):
    return subprocess.run(
        [str(TPT), "act-history", *arguments],
        capture_output=True, text=True, cwd=ROOT,
    )


def git(repo, *arguments):
    return subprocess.run(["git", *arguments], cwd=repo, capture_output=True, text=True)


class CrossLineReceptionTests(unittest.TestCase):
    """A merge across lines is admitted where it cites its reception, and only there."""

    def setUp(self):
        self.tool = load_tool()
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.sandbox = pathlib.Path(self.tmp.name)

    # --- the fixture ----------------------------------------------------------

    def slice_file(self, name="reception.toml", *, receptions=RECEPTION, source=RECEIVED,
                   kind="translates-typical-edition", parents=None,
                   act_citation="cited-externally", extra=""):
        """The Holy Week tracer plus a vernacular line that receives from it."""
        if parents is None:
            parents = ["vernacular-first-1965", RECEIVED]
        body = FIXTURE.format(
            receiving=RECEIVING,
            parents="[" + ", ".join(f'"{parent}"' for parent in parents) + "]",
            act_citation=act_citation,
            extra=extra,
            receptions=receptions.format(source=source, kind=kind) if receptions else "",
        )
        target = self.sandbox / name
        target.write_text(HOLY_WEEK.read_text(encoding="utf-8") + body, encoding="utf-8")
        return target

    def checked(self, source):
        result = run("check", "--source", str(source), "--json")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        return result.stdout

    def refused(self, source, *, naming):
        result = run("check", "--source", str(source))
        said = result.stdout + result.stderr
        self.assertNotEqual(0, result.returncode, f"check passed: {said}")
        for phrase in naming:
            self.assertIn(phrase, said, said)
        return said

    def emitted(self, source, name="repository"):
        out = self.sandbox / name
        result = run("emit", "--source", str(source), "--out", str(out))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        return out

    # --- admitted, because it cites what a rejoining has to cite ---------------

    def test_a_cross_line_merge_that_cites_its_reception_is_admitted(self):
        payload = self.checked(self.slice_file())
        self.assertIn('"receptions":1', payload.replace(" ", ""))
        self.assertIn("translates-typical-edition", payload)

    def test_the_emitted_commit_carries_both_parents_and_the_line_stands_first(self):
        """git must see the rejoining, or `merge-base` cannot.

        The tree is this line's own and the second parent is a claim about
        descent, so the parent list is the only place the join exists for git.
        """
        repo = self.emitted(self.slice_file())
        parents = git(repo, "rev-list", "--parents", "--max-count=1",
                      f"act/{RECEIVING}").stdout.split()
        self.assertEqual(3, len(parents), parents)
        self.assertEqual(
            git(repo, "rev-parse", "act/vernacular-first-1965").stdout.strip(), parents[1],
            "the line's own parent must be the FIRST parent, so --first-parent follows it",
        )
        self.assertEqual(
            git(repo, "rev-parse", f"act/{RECEIVED}").stdout.strip(), parents[2])
        message = git(repo, "show", "--no-patch", "--format=%B", f"act/{RECEIVING}").stdout
        self.assertIn(f"Receives: {RECEIVED} on line {RECEIVED_LINE}", message)
        self.assertIn("Reception-kind: translates-typical-edition", message)
        self.assertIn("THIS STATION RECEIVES ACROSS LINES", message)
        # And the act's own record carries the evidence, not only the trailer.
        record = git(repo, "show",
                     f"act/{RECEIVING}:acts/1969-11-30-vernacular-second.txt").stdout
        self.assertIn(
            f"receives:   {RECEIVED} on line {RECEIVED_LINE} (translates-typical-edition)",
            record,
        )
        self.assertIn("instrument: A constructed decree of the receiving conference", record)

    def test_the_reception_carries_ancestry_and_not_text(self):
        """The substance of the model, and the reason a union would be false.

        The 2011 English Missal does not contain the Latin typical edition, so a
        merge that unioned the two trees would put a book into a commit that
        never held it -- and `commonality` would then report the two lines
        holding identical prayers because this tool copied them.
        """
        repo = self.emitted(self.slice_file())
        received = self.tool.blobs(repo, f"act/{RECEIVED}")
        receiving = self.tool.blobs(repo, f"act/{RECEIVING}")
        self.assertTrue(received, "the Latin line's tip carries no liturgy at all")
        self.assertTrue(all(path.startswith("holy-week/") for path in received))
        self.assertTrue(
            all(path.startswith("vernacular/") for path in receiving),
            sorted(receiving),
        )
        self.assertEqual(set(), set(received) & set(receiving))
        # What the receiving act DID take stands in its own cited row, which is
        # how every other change to a book is written here.
        self.assertIn("vernacular/vernacular-ordo/oratio.txt", receiving)

    def test_the_received_line_is_not_disturbed(self):
        """A reception takes; it does not reach back into what it received.

        Asserted on the liturgy of the received tip against the same tip emitted
        from the tracked slice, which knows nothing of the vernacular line.
        """
        untouched = self.tool.blobs(self.emitted(HOLY_WEEK, "tracked"), f"act/{RECEIVED}")
        received = self.tool.blobs(self.emitted(self.slice_file()), f"act/{RECEIVED}")
        self.assertEqual(untouched, received)

    def test_fsck_strict_passes_on_the_emitted_repository(self):
        strict = git(self.emitted(self.slice_file()), "fsck", "--strict")
        self.assertEqual(0, strict.returncode, strict.stdout + strict.stderr)

    def test_the_emission_is_byte_stable(self):
        source = self.slice_file()
        refs = [
            git(self.emitted(source, name), "for-each-ref",
                "--format=%(refname) %(objectname)").stdout
            for name in ("once", "twice")
        ]
        self.assertEqual(refs[0], refs[1])
        self.assertIn(f"refs/tags/act/{RECEIVING}", refs[0])

    # --- and git agrees with the graph about what the two lines share ----------

    def test_commonality_still_agrees_with_git(self):
        """The consequence that must be verified rather than assumed.

        A cross-line merge changes what `git merge-base` computes. `commonality`
        derives the shared base from the act graph, runs `git merge-base --all`
        on the emitted repository and RAISES if the two disagree, so running it
        over every pair of lines is the proof -- and the pair is read out of it
        afterwards so a silent no-op cannot pass for agreement.
        """
        source = self.slice_file()
        repo = self.emitted(source)
        data = self.tool.load(source)
        report = self.tool.commonality(data, repo, None)
        pairs = {(row["a"], row["b"]): row for row in report["pairs"]}
        self.assertEqual(3, len(pairs), sorted(pairs))
        self.assertEqual([RECEIVED], pairs[("typica", "vernacular")]["shared_base"])
        # The fork's own pair is unmoved: the exempted uses still part from Rome
        # at Quo primum, and the new line reaches them only through it.
        self.assertEqual(["quo-primum-1570"],
                         pairs[("exempt-uses", "typica")]["shared_base"])
        self.assertEqual(["quo-primum-1570"],
                         pairs[("exempt-uses", "vernacular")]["shared_base"])
        # And the same question, asked of git directly rather than through the
        # verb that proves itself, so this test does not rest on the tool it is
        # testing agreeing with itself.
        found = git(repo, "merge-base", "--all", f"act/{RECEIVING}",
                    f"act/{RECEIVED}").stdout.split()
        self.assertEqual([git(repo, "rev-parse", f"act/{RECEIVED}").stdout.strip()], found)

    def test_commonality_refuses_a_graph_git_disagrees_with(self):
        """The proof proves something: break the graph and the verb raises.

        Without this, `commonality` passing would be consistent with it having
        stopped asking git anything at all.
        """
        source = self.slice_file()
        repo = self.emitted(source)
        data = self.tool.load(source)
        acts = self.tool.indexed(data["acts"], "id", "acts")
        # Withdrawn cleanly, so what is asked of git is a graph that is valid
        # and no longer the one the repository was written from.
        acts[RECEIVING]["parents"] = ["vernacular-first-1965"]
        acts[RECEIVING].pop("receptions")
        with self.assertRaises(self.tool.Problem) as refused:
            self.tool.commonality(data, repo, None)
        self.assertIn("git merge-base and the act graph disagree", str(refused.exception))

    # --- refused, one missing citation at a time ------------------------------

    def test_a_cross_line_merge_that_cites_nothing_is_refused(self):
        """The old refusal, kept, and now said with its reason.

        This is the case `merges across lines; lines never rejoin` used to
        refuse, and it must still be refused -- a merge with no reception is
        exactly the tidy history Rule 2 forbids.
        """
        self.refused(
            self.slice_file(receptions=""),
            naming=[f"merges {RECEIVED}", "declares no reception", "[[acts.receptions]]"],
        )

    def test_every_field_a_reception_must_cite_is_demanded(self):
        for field, _ in self.tool.RECEPTION_EVIDENCE:
            with self.subTest(field=field):
                stripped = re.sub(
                    rf'^{field} = ("[^"\n]*"|"""(?:.|\n)*?""")$', "", RECEPTION,
                    count=1, flags=re.M,
                )
                # One field taken away and the others left standing, or the
                # refusal below would not be about the one being tested.
                self.assertNotIn(f"\n{field} = ", stripped)
                for other, _ in self.tool.RECEPTION_EVIDENCE:
                    if other != field:
                        self.assertIn(f"\n{other} = ", stripped)
                self.refused(
                    self.slice_file(name=f"no-{field}.toml", receptions=stripped),
                    naming=[f"the reception from {RECEIVED}", f"in `{field}`"],
                )

    def test_a_reception_of_an_unagreed_kind_is_refused(self):
        self.refused(
            self.slice_file(kind="borrowed-from"),
            naming=["must state a kind", "translates-typical-edition"],
        )

    def test_a_reception_that_names_a_parent_on_its_own_line_is_refused(self):
        """Two descents converging on ONE line is an ordinary merge, not this."""
        self.refused(
            self.slice_file(source="vernacular-first-1965"),
            naming=["stands on this act's own line"],
        )

    def test_a_reception_that_names_no_parent_at_all_is_refused(self):
        self.refused(
            self.slice_file(source="quo-primum-1570"),
            naming=["names no parent of this act"],
        )

    def test_a_single_cross_line_parent_may_not_declare_a_reception(self):
        """A fork is a birth and is drawn by naming that parent alone.

        This is the distinction the change turns on: one parent synthesises
        nothing, so there is nothing for a reception to assert.
        """
        self.refused(
            self.slice_file(parents=[RECEIVED]),
            naming=["every parent is a received one", "is a FORK"],
        )

    def test_a_received_parent_may_not_stand_first(self):
        self.refused(
            self.slice_file(parents=[RECEIVED, "vernacular-first-1965"]),
            naming=["stands first", "--first-parent"],
        )

    def test_a_station_whose_own_instrument_was_not_read_may_not_receive(self):
        """Rule 1 lets a station stand on an instrument nobody has read. A
        rejoining may not: the thing that documents a reception is an act, and
        an act nobody has read documents nothing."""
        self.refused(
            self.slice_file(
                act_citation="not-found",
                # The two things a not-found station owes on its own account,
                # so that the only complaint left is the one being tested.
                extra='\nact_citation_note = "Constructed; nothing was searched."'
                      '\nact_citation_scope = "Constructed; nothing was searched."',
            ),
            naming=["receives across lines with act_citation", "must have been read"],
        )

    def test_a_reception_may_not_precede_what_it_receives(self):
        source = self.slice_file(name="early.toml")
        text = source.read_text(encoding="utf-8").replace('date = "1969-11-30"',
                                                          'date = "1961-11-30"', 1)
        source.write_text(text, encoding="utf-8")
        self.refused(source, naming=["cannot precede what it receives"])

    def test_the_refusal_is_the_writers_and_not_the_clis(self):
        """`check` refusing is necessary and not sufficient.

        The CLI happens to run `check` before `emit`. A guard living only there
        would be one call-ordering change away from writing a rejoining nobody
        evidenced into commit objects that cannot be withdrawn once published.
        """
        data = self.tool.load(self.slice_file(receptions=""))
        out = self.sandbox / "direct"
        with self.assertRaises(self.tool.Problem) as refused:
            self.tool.emit(data, out)
        self.assertIn("declares no reception", str(refused.exception))
        self.assertFalse(out.exists(), "emit created a repository for a refused slice")

    # --- the drawing says which of the two things a cross-lane edge is --------

    def test_the_plate_draws_a_reception_as_itself_and_not_as_a_fork(self):
        """A fork leaves a lane and a reception arrives in one.

        `time-machine.md` section 9 measured that the same interchange drawn as
        a dot rather than as a link CHANGED which transfers passengers made, so
        the two must not share a mark.
        """
        out = self.sandbox / "plates"
        result = run("plate", "--source", str(self.slice_file()), "--out", str(out))
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        text = (out / "roman-holy-week.dot").read_text(encoding="utf-8")
        edges = re.findall(r'^  "([^"]+)" -- "([^"]+)" \[(.*)\];$', text, re.M)
        nodes = dict(re.findall(r'^  "([^"]+)" \[(.*)\];$', text, re.M))
        marks = {
            (parent, child): dict(re.findall(r'(\w+)="([^"]*)"', attributes))
            for parent, child, attributes in edges
        }
        reception = marks[(RECEIVED, RECEIVING)]
        self.assertEqual("true", reception.get("reception"))
        self.assertNotIn("fork", reception)
        self.assertEqual("translates-typical-edition", reception["descent"])
        # A reception must cite an instrument to be drawn at all, so it is drawn
        # at the width of an edge an instrument draws.
        self.assertEqual(("stated", "3"), (reception["strength"], reception["penwidth"]))
        # The fork on the same sheet still reads as a birth and not as this.
        fork = marks[("quo-primum-1570", "quo-primum-exemption-1570")]
        self.assertEqual("true", fork.get("fork"))
        self.assertNotIn("reception", fork)
        # And the station two edges arrive at is an interchange, which is the
        # one place Rule 2 lets a reader change trains.
        attributes = dict(re.findall(r'(\w+)="([^"]*)"', nodes[RECEIVING]))
        self.assertEqual("interchange", attributes["role"])
        self.assertIn("reception 1: a line REJOINS another", text)

    # --- what must not have broken --------------------------------------------

    def test_the_three_tracked_slices_still_pass(self):
        """A guard that refuses valid existing data fails as loudly as one that admits bad."""
        for source in (HOLY_WEEK, MISSAL, LAW):
            with self.subTest(source=source.name):
                result = run("check", "--source", str(source))
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_no_tracked_slice_records_a_rejoining(self):
        """The tracked slices are unchanged by this, and say so in their own numbers.

        The mechanism is new and no inventory uses it yet, which is why the
        fixture above exists at all. If a slice ever does, this test says so
        rather than letting a rejoining land unremarked.
        """
        for source in (HOLY_WEEK, MISSAL, LAW):
            data = self.tool.load(source)
            with self.subTest(source=source.name):
                self.assertEqual(0, self.tool.check(data)["receptions"])

    def test_a_same_line_merge_is_still_a_merge_and_still_needs_its_basis(self):
        """The guard this one stands beside must not have been widened away."""
        data = self.tool.load(HOLY_WEEK)
        acts = self.tool.indexed(data["acts"], "id", "acts")
        self.assertEqual(2, len(acts["editio-typica-1962"]["parents"]))
        acts["editio-typica-1962"].pop("reception_basis")
        with self.assertRaises(self.tool.Problem) as refused:
            self.tool.check(data)
        self.assertIn("more than one parent asserts a reception", str(refused.exception))


if __name__ == "__main__":
    unittest.main()
