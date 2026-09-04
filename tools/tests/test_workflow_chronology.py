#!/usr/bin/env python3
"""A proper's biblical dates come from the corpus, and are held against it.

`guidance/scripture-chronology.md` §14: a publication that needs biblical
chronology MUST read `src/sources/chronology/` and MUST NOT independently
infer, research, harmonize, or assign a replacement date; where the corpus
returns an unresolved state the consumer preserves it or omits the date.
Until `proper` v17 nothing in the propers workflow carried that rule, and each
guide found its own dates.

Almost every test here RUNS the wiring and the gate checks over a real
formulary in a copied tree. The two exceptions assert the pipeline's declared
command text, because a check the workflow never invokes gates nothing however
well it works from a shell.

The fixture is the Fourteenth Sunday after Pentecost because its formulary
covers all three answers at once: the Offertory's Ps. 33 is `dated` by a
superscription-setting bound to an event, the Epistle and Gospel are
`composition-only` with several disputed dates apiece, and the Gradual's
Ps. 117 and the Alleluia's Ps. 94 are `undated-in-tradition` — the state a
guide must preserve rather than fill.

TWO CORRECTIONS TO THE RECORD, kept here because this is the file that names
the same formulary and a reader chasing either claim arrives at it. The commit
that first wired these checks (`1f2025701`, "Let a proper read its dates
instead of researching them") closed with two statements about this formulary
that are not true of the corpus, and a pushed message cannot be reworded.

1. It said the corpus asserts "49-50, about 53-54 and 56 and nothing later"
   for the Galatians locus. It also asserts `A.D. 57 or 58`:
   `tools/tpt scripture-chronology query Gal.5.16` returns four disputed
   composition dates, and that is the fourth. `SUPPORTED` below prints it, and
   `test_a_date_the_corpus_supports_passes` executes the fact.
2. It said `1055--1015 BC` sits "in a cell whose psalm the corpus holds
   undated". It does not. That figure is in the leaf's **Offertory** row,
   whose Ps. 33:8-9a the corpus holds `dated` — `superscription-setting`,
   label `A. M. 2944, A. C. 1060`, the preferred profile's answer. The psalms
   this formulary leaves undated are the Gradual's Ps. 117 and the Alleluia's
   Ps. 94, and the published leaf prints no figure in either row: it prints a
   stated absence, which is what §14 requires.

Neither correction changes what the checks do. Both change what a reader would
otherwise believe the corpus says.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAUNCHER = ROOT / "tools" / "tpt"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_workflow_research_fanout import workflow_json  # noqa: E402

STAGE = "content-preflight"
TOOL = "check-content-preflight"
WIRING = "proper-chronology"
RECORD = "research/chronology.toml"
RECORD_CHECK = "chronology-record-current"
CLAIMS_CHECK = "chronology-claims-supported"
BINDS_FROM = 17
# Any version below BINDS_FROM. The fixture states it itself rather than
# borrowing whichever version the tree happens to publish: this leaf is a
# production target, and a later run rewriting it to v17 would silently turn
# the out-of-scope case into the bound one and the bind into a no-op.
PRE_CONTRACT = 11
RESOLVE_CONTEXT = (ROOT / "workflows" / "fragments" / "propers" /
                   "resolve-context.md")

DOCUMENT = ("liturgy/roman-rite/1962/propers/temporal/"
            "54-fourteenth-after-pentecost")
DOSSIER = "sections/redevelopment/02-scriptural-date-location.tex"


def _at_version(metadata: str, version: int) -> str:
    """The same provenance record, bound to a given proper version.

    The surviving GPT fixture predates recorded workflow identity. Set its
    first two fields explicitly; nothing else in the file is allowed to move,
    because the checks under test read the rest of it.
    """
    pattern = re.compile(
        r"(\\AIGenerationProvenance)\{[^{}]*\}\{[^{}]*\}")
    text, count = pattern.subn(
        lambda m: f"{m.group(1)}{{proper}}{{{version}}}", metadata, count=1)
    if count != 1:
        raise AssertionError(
            "the fixture leaf carries no AIGenerationProvenance record to "
            "set a version on")
    return text

# What the corpus answers for this formulary, in its own words. Every string
# here was read out of `tools/tpt scripture-chronology query` and is asserted
# rather than assumed: a fixture that made up its own "supported" date would
# prove only that the check agrees with the fixture.
KORAH = "composition.psalms-of-the-sons-of-korah"
GALATIANS = "composition.epistle-to-the-galatians"
MATTHEW = "composition.gospel-of-matthew"
GETH = "israel.monarchy.david-at-geth"
GETH_LABEL = "A. M. 2944, A. C. 1060"

SUPPORTED = r"""\section*{Scriptural Date and Location}
\chronodate{introit}{\chronology{%s}{composition}{between the days of Isaias
and the return from exile}}
\chronodate{epistle}{\chronology{%s}{composition}{A.D.~57 or 58}}
\chronodate{gradual}{No year is held for this psalm.}
\chronodate{alleluia}{No year is held for this psalm.}
\chronodate{gospel,communion}{\chronology{%s}{composition}{about the year 50}}
\chronodate{offertory}{\chronology{%s}{superscription-setting}{A.~M.~2944,
A.~C.~1060}}
""" % (KORAH, GALATIANS, MATTHEW, GETH)


def stage() -> dict:
    return {s["id"]: s for s in workflow_json()["stages"]}[STAGE]


def check_commands() -> dict[str, str]:
    return {check["id"]: check["command"] for check in stage()["checks"]}


class WiringTests(unittest.TestCase):
    """The route from a leaf id to a locus, and what it refuses."""

    def run_tool(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([str(LAUNCHER), WIRING, *args],
                              capture_output=True, text=True, cwd=ROOT)

    def test_the_loci_are_the_corpus_s_own_spelling(self):
        """Vulgate numbers and canon tokens, from the calendar and _canon.

        The missal appoints Psalm 83; an English psalter numbers the same
        psalm 84. A wiring that carried the wrong one would ask the corpus
        about a different psalm and get a confident answer.
        """
        done = self.run_tool("loci", "--document", DOCUMENT, "--json")
        self.assertEqual(done.returncode, 0, done.stderr)
        payload = json.loads(done.stdout)
        by_key = {e["key"]: e for e in payload["elements"]}
        self.assertEqual(payload["mass"], "pentecost-14")
        self.assertEqual(payload["system"], "vulgate")
        self.assertEqual(by_key["introit"]["loci"],
                         ["Ps.83.10", "Ps.83.11", "Ps.83.2", "Ps.83.3"])
        self.assertEqual(by_key["offertory"]["loci"], ["Ps.33.8", "Ps.33.9"])
        self.assertEqual(by_key["gospel"]["loci"],
                         [f"Matt.6.{verse}" for verse in range(24, 34)])

    def test_the_statuses_are_the_corpus_s_and_include_its_negatives(self):
        """`undated-in-tradition` is an answer, and must arrive as one."""
        done = self.run_tool("loci", "--document", DOCUMENT, "--json")
        by_key = {e["key"]: e for e in json.loads(done.stdout)["elements"]}
        self.assertEqual(by_key["offertory"]["status"], "dated")
        self.assertEqual(by_key["epistle"]["status"], "composition-only")
        self.assertEqual(by_key["gradual"]["status"], "undated-in-tradition")
        self.assertEqual(by_key["alleluia"]["status"], "undated-in-tradition")
        # An element the missal composes carries no Scripture and is still
        # listed: an absent row and a forgotten row look alike afterwards.
        self.assertEqual(by_key["collect"]["loci"], [])
        self.assertEqual(by_key["collect"]["status"], "")

    def test_every_published_leaf_resolves(self):
        """A formulary this cannot address is one the contract cannot bind.

        ENUMERATED FROM EVERY DIRECTORY WITH THE PUBLICATION MARKER, not from
        a component manifest some leaves happen to carry. This once globbed
        `*/*/proper-components.toml` and silently skipped
        `ritual/m01-nuptial-mass`, which has no manifest — the one published
        leaf the wiring could not answer for at all. `main.tex` is the
        workflow's publication marker; a pre-authoring checkpoint may already
        own `propers/` and `research/` without being a published leaf yet.
        The count is compared against the complete marked set rather than
        against zero.
        """
        checked: set[str] = set()
        expected: set[str] = set()
        for provider in ("claude", "gpt"):
            root = ROOT / "src" / provider / "liturgy/roman-rite/1962/propers"
            for leaf in sorted(root.glob("*/*")):
                if not leaf.is_dir() or not (leaf / "main.tex").is_file():
                    continue
                document = leaf.relative_to(ROOT / "src" / provider).as_posix()
                expected.add(f"{provider}/{document}")
                with self.subTest(leaf=f"{provider}/{document}"):
                    done = self.run_tool("loci", "--provider", provider,
                                         "--document", document)
                    self.assertEqual(done.returncode, 0, done.stderr)
                checked.add(f"{provider}/{document}")
        self.assertEqual(checked, expected)
        # The leaf the old glob dropped, named so the regression cannot come
        # back quietly.
        self.assertIn(
            "gpt/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass",
            checked)

    def test_a_ritual_identity_is_answered_and_not_refused(self):
        """`m01` is a real published leaf and the calendar registers no `M`.

        The wiring reaches Scripture through the calendar's mass entries, and
        the 1962 calendar transcribed here carries the temporal and sanctoral
        cycles: a nuptial Mass is appointed by a rite, not by a day. Raising
        left a v17 run on this leaf with no compliant path at all, because
        `chronology-record-current` demands a record and nothing could write
        one. The answer is typed instead, and it says which fact it is.
        """
        document = "liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass"
        done = self.run_tool("loci", "--provider", "gpt", "--document",
                             document, "--json")
        self.assertEqual(done.returncode, 0, done.stderr)
        payload = json.loads(done.stdout)
        self.assertEqual(payload["formulary"], "no-calendar-formulary")
        self.assertEqual(payload["elements"], [])
        self.assertIn("ritual Mass", payload["formulary_reason"])
        # And the reason reaches a human reader, who would otherwise see an
        # empty list and read it as "the corpus holds nothing here".
        human = self.run_tool("loci", "--provider", "gpt", "--document",
                              document)
        self.assertIn("ritual Mass", human.stdout)

    def test_the_ritual_record_is_empty_and_valid(self):
        """An empty record a gate can regenerate, not an impossible one."""
        import tomllib

        done = self.run_tool(
            "record", "--provider", "gpt", "--document",
            "liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass")
        self.assertEqual(done.returncode, 0, done.stderr)
        record = tomllib.loads(done.stdout)
        self.assertEqual(record["record_type"], "proper-chronology")
        self.assertEqual(record["formulary"], "no-calendar-formulary")
        self.assertEqual(record.get("elements", []), [])
        self.assertIn("no date may be supplied", record["formulary_reason"])

    def test_the_unregistered_refusal_claims_no_interlock_it_does_not_have(self):
        """It said `check-proper-identity` refuses this at the scope gate.

        That tool deliberately ACCEPTS an `m` identity on its grammar and
        documents at length why, so the sentence sent a reader to a check that
        would have passed the thing they were told it refused.
        """
        done = self.run_tool(
            "loci", "--document",
            "liturgy/roman-rite/1962/propers/temporal/99-invented-sunday")
        self.assertEqual(done.returncode, 1)
        self.assertNotIn("check-proper-identity", done.stderr)

    def test_the_record_carries_the_stable_ids(self):
        """§14: event id, unit id, profile, relation, in the audit payload."""
        done = self.run_tool("record", "--document", DOCUMENT)
        self.assertEqual(done.returncode, 0, done.stderr)
        import tomllib

        record = tomllib.loads(done.stdout)
        self.assertEqual(record["record_type"], "proper-chronology")
        self.assertEqual(record["document"], DOCUMENT)
        by_key = {e["key"]: e for e in record["elements"]}
        offertory = by_key["offertory"]["claims"]
        self.assertEqual(len(offertory), 1)
        claim = offertory[0]
        self.assertEqual(claim["subject"], GETH)
        self.assertEqual(claim["relation"], "superscription-setting")
        self.assertEqual(claim["label"], GETH_LABEL)
        self.assertEqual(claim["profile"], "catholic-traditional-v1")
        self.assertTrue(claim["sources"],
                        "a claim with nothing behind it is what §14 forbids")
        # The corpus's own reason for a negative travels with it, so that a
        # guide can state the absence at the extent that was actually
        # searched instead of as plain silence.
        self.assertEqual(by_key["gradual"]["status"], "undated-in-tradition")
        self.assertIn("Catholic Encyclopedia", by_key["gradual"]["reason"])

    def test_the_record_is_byte_stable(self):
        """A gate regenerates it and compares; it may not move on its own."""
        first = self.run_tool("record", "--document", DOCUMENT)
        second = self.run_tool("record", "--document", DOCUMENT)
        self.assertEqual(first.stdout, second.stdout)
        self.assertTrue(first.stdout)

    def test_an_unregistered_identity_is_refused_not_answered_empty(self):
        done = self.run_tool(
            "loci", "--document",
            "liturgy/roman-rite/1962/propers/temporal/99-invented-sunday")
        self.assertEqual(done.returncode, 1)
        self.assertIn("registered by no mass entry", done.stderr)

    def test_the_wiring_reads_the_corpus_only_through_its_seam(self):
        """§2: `scripts/_chronology.py` is the whole seam.

        A second reader of `src/sources/chronology/` would be a second set of
        rules about what the corpus answers with, which is the failure the
        profile machinery exists to prevent.
        """
        import _proper_chronology

        source = (ROOT / "scripts" / "_proper_chronology.py").read_text(
            encoding="utf-8")
        code = "\n".join(line for line in source.splitlines()
                         if not line.lstrip().startswith("#"))
        self.assertIn("import _chronology", code)
        for forbidden in ("import yaml", "CORPUS_ROOT", "open(",
                          "read_text", "glob("):
            self.assertNotIn(forbidden, code,
                             "the wiring reads no corpus file itself")
        # And the seam is the function, not a copy of what it decides: the
        # profile gate that says which claims are answerable lives in
        # `_chronology._candidates` and is never reimplemented here.
        self.assertTrue(hasattr(_proper_chronology, "chronology") is False)
        self.assertTrue(callable(_proper_chronology._claims_at))


class ResolveContextFreshLeafTests(unittest.TestCase):
    """The workflow can materialize chronology before source audit runs."""

    def test_resolve_context_creates_research_before_the_required_write(self):
        text = RESOLVE_CONTEXT.read_text(encoding="utf-8")
        create = 'mkdir -p "$research_dir"'
        write = "tools/tpt proper-chronology record"
        verify = 'test -f "$research_dir/chronology.toml"'
        for command in (create, write, verify):
            self.assertIn(command, text)
        self.assertLess(text.index(create), text.index(write))
        self.assertLess(text.index(write), text.index(verify))

    def test_the_materialized_directory_makes_a_fresh_leaf_writable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "tree"
            (root / "src").mkdir(parents=True)
            (root / "src" / "sources").symlink_to(ROOT / "src" / "sources")
            leaf = root / "src" / "gpt" / DOCUMENT
            self.assertFalse(leaf.exists(), "the regression needs a fresh leaf")

            research = leaf / "research"
            research.mkdir(parents=True)
            done = subprocess.run(
                [str(LAUNCHER), WIRING, "record", "--root", str(root),
                 "--provider", "gpt", "--document", DOCUMENT, "--write"],
                capture_output=True, text=True, cwd=ROOT)

            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertTrue((research / "chronology.toml").is_file())

    def test_resolve_context_blocks_if_the_required_write_fails(self):
        text = RESOLVE_CONTEXT.read_text(encoding="utf-8")
        self.assertIn('return `disposition: "BLOCKED"`', text)
        self.assertIn('never `PASS`', text)
        self.assertIn("failed required write is not", text)


class GateCommandTests(unittest.TestCase):
    """The gate must actually invoke the checks. Text, because that is the fact."""

    def test_the_preflight_declares_both_chronology_checks(self):
        commands = check_commands()
        for check in (RECORD_CHECK, CLAIMS_CHECK):
            with self.subTest(check=check):
                self.assertIn(check, commands)
                self.assertEqual(
                    commands[check],
                    f"tools/tpt {TOOL} --provider {{provider}} "
                    f"--document {{proper}} --check {check}")

    def test_a_failure_is_repaired_in_the_leaf(self):
        """A wrong date is an authoring defect, not a research one.

        The corpus already holds the evidence, so sending this back through
        seven research lanes would spend the whole discovery budget on a fact
        the tree could hand over in one command.
        """
        self.assertEqual(stage()["fail_transition"], "content-revision")


class BoundLeafTests(unittest.TestCase):
    """The checks, driven over a copy of a real leaf that states v17."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name) / "tree"
        leaf = cls.root / "src" / "gpt" / DOCUMENT
        leaf.parent.mkdir(parents=True)
        shutil.copytree(ROOT / "src" / "gpt" / DOCUMENT, leaf)
        (cls.root / "src" / "sources").symlink_to(ROOT / "src" / "sources")
        cls.leaf = leaf
        cls.metadata = leaf / "generation-metadata.tex"
        published = cls.metadata.read_text(encoding="utf-8")
        cls.unbound_metadata = _at_version(published, PRE_CONTRACT)
        cls.bound_metadata = _at_version(published, BINDS_FROM)
        cls.published_dossier = (leaf / DOSSIER).read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        self.metadata.write_text(self.unbound_metadata, encoding="utf-8")
        (self.leaf / DOSSIER).write_text(self.published_dossier,
                                         encoding="utf-8")
        (self.leaf / RECORD).unlink(missing_ok=True)

    # --- helpers ---------------------------------------------------------

    def bind(self):
        """State the version the chronology contract binds from."""
        self.assertNotEqual(self.bound_metadata, self.unbound_metadata,
                            "the bind must change the recorded version, or "
                            "every test below is testing the same state twice")
        self.metadata.write_text(self.bound_metadata, encoding="utf-8")

    def write_record(self):
        done = subprocess.run(
            [str(LAUNCHER), WIRING, "record", "--root", str(self.root),
             "--provider", "gpt", "--document", DOCUMENT, "--write"],
            capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(done.returncode, 0, done.stderr)

    def write_dossier(self, text: str):
        (self.leaf / DOSSIER).write_text(text, encoding="utf-8")

    def check(self, name: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(ROOT / "tools" / TOOL), "--root", str(self.root),
             "--provider", "gpt", "--document", DOCUMENT, "--check", name],
            capture_output=True, text=True, cwd=ROOT)

    def assertRefused(self, name: str, because: str):
        done = self.check(name)
        self.assertEqual(done.returncode, 1,
                         f"{name} accepted it: {done.stdout}")
        self.assertIn(because, done.stderr)

    def assertAccepted(self, name: str):
        done = self.check(name)
        self.assertEqual(done.returncode, 0, done.stderr)

    # --- scope -----------------------------------------------------------

    def test_a_leaf_published_before_the_contract_is_out_of_scope(self):
        """Correct work is not retrospectively refused.

        The fixture states a `proper` version below the one the contract
        binds from. Refusing such a leaf would say the production that made
        it was wrong, which it was not: there was no corpus to read.
        """
        for name in (RECORD_CHECK, CLAIMS_CHECK):
            with self.subTest(check=name):
                done = self.check(name)
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertIn("v%d" % BINDS_FROM, done.stdout,
                              "the pass says which version binds it")

    def test_a_bound_leaf_must_carry_the_record(self):
        self.bind()
        self.assertRefused(RECORD_CHECK, RECORD)

    def test_the_record_the_wiring_writes_is_the_one_the_gate_wants(self):
        self.bind()
        self.write_record()
        self.assertAccepted(RECORD_CHECK)

    def test_a_hand_edited_record_is_refused(self):
        """The defect the whole wiring exists for: a plausible wrong figure."""
        self.bind()
        self.write_record()
        path = self.leaf / RECORD
        text = path.read_text(encoding="utf-8")
        edited = text.replace(f'label = "{GETH_LABEL}"',
                              'label = "1055-1015 B.C."')
        self.assertNotEqual(edited, text, "the edit changed nothing")
        path.write_text(edited, encoding="utf-8")
        self.assertRefused(RECORD_CHECK, "not what the chronology corpus")

    def test_deleting_the_record_does_not_escape_it(self):
        """A leaf that once carried one is held to it whatever it states."""
        self.bind()
        self.write_record()
        self.metadata.write_text(self.unbound_metadata, encoding="utf-8")
        self.assertAccepted(RECORD_CHECK)
        path = self.leaf / RECORD
        path.write_text(path.read_text(encoding="utf-8").replace(
            f'label = "{GETH_LABEL}"', 'label = "1055-1015 B.C."'),
            encoding="utf-8")
        self.assertRefused(RECORD_CHECK, "not what the chronology corpus")

    # --- the dates on the page -------------------------------------------

    def test_a_date_the_corpus_supports_passes(self):
        """Every figure a corpus assertion, in the source's own label.

        LaTeX ties and an en-dash are not a different date. A check that
        called them different would teach an author to fight the typesetter
        rather than to quote.
        """
        self.bind()
        self.write_record()
        self.write_dossier(SUPPORTED)
        self.assertAccepted(CLAIMS_CHECK)

    def test_a_date_the_corpus_does_not_support_fails(self):
        """Cornelius a Lapide's A.D. 58 for Galatians is a real reading of a
        real source, and this corpus does not assert it. That is exactly the
        case §14 is about: not a careless date, a researched one."""
        self.bind()
        self.write_record()
        self.write_dossier(SUPPORTED.replace("A.D.~57 or 58", "A.D.~58"))
        self.assertRefused(CLAIMS_CHECK, "the corpus asserts no 'composition'")

    def test_an_invented_date_where_the_corpus_is_undated_fails(self):
        """Ps. 117 is `undated-in-tradition`, so there is no claim to make."""
        self.bind()
        self.write_record()
        self.write_dossier(SUPPORTED.replace(
            r"\chronodate{gradual}{No year is held for this psalm.}",
            r"\chronodate{gradual}{David's reign, 1055--1015 B.C.}"))
        self.assertRefused(CLAIMS_CHECK, "outside a")

    def test_a_corpus_date_printed_at_the_wrong_element_fails(self):
        """The assertion is real and it is about another element's verses."""
        self.bind()
        self.write_record()
        self.write_dossier(SUPPORTED.replace(
            r"\chronodate{gradual}{No year is held for this psalm.}",
            r"\chronodate{gradual}{\chronology{%s}{superscription-setting}"
            r"{%s}}" % (GETH, GETH_LABEL)))
        self.assertRefused(CLAIMS_CHECK, "not at the verses this element")

    def test_a_shared_cell_holds_its_claim_against_every_element_it_names(self):
        """Naming an extra element must not widen what the cell may print.

        `A.D. 49-50` is a real corpus assertion about Galatians, and the
        Gradual's Ps. 117 is `undated-in-tradition`. In its own cell the claim
        is refused. Held against the UNION of the two elements' answers,
        `{gradual,epistle}` accepted it — and the extra key satisfied the
        coverage rule at the same time. A cell prints one date for every
        element it names, so the permitted set is the intersection.
        """
        self.bind()
        self.write_record()
        self.write_dossier(SUPPORTED.replace(
            r"\chronodate{gradual}{No year is held for this psalm.}",
            r"\chronodate{gradual,epistle}{\chronology{%s}{composition}"
            r"{A.D.~49-50}}" % GALATIANS))
        self.assertRefused(CLAIMS_CHECK, "some but not all of the elements")

    def test_naming_the_whole_formulary_in_one_cell_does_not_launder_a_date(self):
        """One cell, one date, every element: the widest shape of the same bug.

        Against the union this passed clean — a single Date cell carrying one
        year for the Introit, Epistle, Gradual, Alleluia, Gospel, Offertory
        and Communion at once, the Gradual among them a psalm the corpus dates
        nowhere, with nothing left uncovered for the coverage rule to name.
        """
        self.bind()
        self.write_record()
        self.write_dossier(
            "\\section*{Scriptural Date and Location}\n"
            r"\chronodate{introit,epistle,gradual,alleluia,gospel,offertory,"
            r"communion}{\chronology{%s}{composition}{A.D.~49-50}}" % GALATIANS
            + "\n")
        done = self.check(CLAIMS_CHECK)
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn("some but not all of the elements", done.stderr)
        # And the coverage rule is NOT what caught it: every appointed element
        # is named, so it has nothing to say. The intersection is doing the
        # work, which is the point of the fix.
        self.assertNotIn("no date cell for", done.stderr)

    def test_a_shared_cell_the_corpus_supports_at_both_elements_passes(self):
        """The intersection must not refuse a legitimate shared row.

        The Communion adapts a verse inside the Gospel pericope and shares its
        row, and the corpus asserts the same Matthew composition date at both.
        A rule that broke this would push authors to split rows the missal
        joins.
        """
        self.bind()
        self.write_record()
        self.assertIn(r"\chronodate{gospel,communion}", SUPPORTED)
        self.write_dossier(SUPPORTED)
        done = self.check(CLAIMS_CHECK)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_an_element_may_not_be_covered_by_two_cells(self):
        """Two cells for one passage are two dates and no way to tell which."""
        self.bind()
        self.write_record()
        self.write_dossier(
            SUPPORTED
            + r"\chronodate{gradual}{\chronology{%s}{composition}"
              r"{about the year 50}}" % MATTHEW
            + "\n")
        self.assertRefused(CLAIMS_CHECK, "more than one \\chronodate names")

    def test_a_figure_wrapped_in_texttt_is_still_a_figure(self):
        r"""`prose()` is the wrong lens for "does this cell print a number".

        It drops `\texttt`, `\url`, `\nolinkurl` and `\href` whole, because
        for a citation check a locator is not a mention of a work. But
        `\texttt` is typeset: the reader sees the digits. The bare figure was
        refused and the same figure in `\texttt` exited 0, so the rule had a
        five-character bypass.
        """
        self.bind()
        self.write_record()
        for cell in (r"David reigned 1055--1015 B.C.",
                     r"David reigned \texttt{1055--1015 B.C.}"):
            with self.subTest(cell=cell):
                self.write_dossier(SUPPORTED.replace(
                    "No year is held for this psalm.", cell, 1))
                self.assertRefused(CLAIMS_CHECK, "outside a")

    def test_the_pass_line_counts_the_cells_it_checked(self):
        """A summary that named only claims read as a pass on the dates.

        At v11 with no record and cells full of bare figures the line was
        "0 chronology claims, every one asserted by the corpus" and the exit
        was 0 — a pass on nothing, printed as a pass on everything.
        """
        self.bind()
        self.write_record()
        self.write_dossier(SUPPORTED)
        done = self.check(CLAIMS_CHECK)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn("6 date cells", done.stdout)
        self.assertIn("no figure printed outside one", done.stdout)

    def test_a_leaf_that_prints_a_cell_is_held_to_the_figure_rule_unbound(self):
        r"""The version gates the discipline; printing a cell opts into it.

        A leaf that writes `\chronodate` has adopted the machinery, so the
        one rule that cannot be read off the page — is this figure sourced —
        applies to it whatever version it states. Nothing published prints a
        cell, so this retro-refuses no correct work.
        """
        self.write_dossier(SUPPORTED.replace(
            "No year is held for this psalm.",
            "David reigned 1055--1015 B.C.", 1))
        done = self.check(CLAIMS_CHECK)
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn("outside a", done.stderr)
        self.assertNotIn("every one asserted by the corpus", done.stdout)

    def test_an_appointed_scripture_with_no_date_cell_fails(self):
        """An element with no cell is indistinguishable from a forgotten one."""
        self.bind()
        self.write_record()
        self.write_dossier("\n".join(
            line for line in SUPPORTED.splitlines()
            if "chronodate{alleluia}" not in line) + "\n")
        self.assertRefused(CLAIMS_CHECK, "no date cell for ['alleluia']")

    def test_a_claim_outside_a_date_cell_is_held_to_the_same_rule(self):
        self.bind()
        self.write_record()
        self.write_dossier(
            SUPPORTED
            + r"\chronology{%s}{composition}{about the year 51}" % MATTHEW
            + "\n")
        self.assertRefused(CLAIMS_CHECK, "outside a date cell")

    def test_the_claim_check_binds_before_the_macro_discipline_does(self):
        """A claim about the corpus is either true of it or it is not.

        The cell discipline is versioned because it changes how a guide is
        written. This is not: a leaf at any version that says the corpus
        asserts something has said something checkable about the corpus.
        """
        self.write_dossier(
            self.published_dossier
            + r"\chronology{%s}{composition}{about the year 51}" % MATTHEW
            + "\n")
        self.assertRefused(CLAIMS_CHECK, "the corpus asserts no")

    def test_the_other_checks_are_unaffected(self):
        self.bind()
        self.write_record()
        self.write_dossier(SUPPORTED)
        for name in ("references-used", "identifiers-resolve",
                     "relation-coverage"):
            with self.subTest(check=name):
                self.assertAccepted(name)


class RitualLeafTests(unittest.TestCase):
    """`ritual/m01-nuptial-mass` at v17 must have a compliant path.

    It is a real published leaf, out of scope today only because its
    provenance record states `unknown`. Its next v17 run was unbuildable:
    `chronology-record-current` demanded `research/chronology.toml` and the
    remedy it printed raised, because no mass entry in the calendar carries an
    `M` registry value. A gate with no compliant path is not a gate.
    """

    DOCUMENT = "liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass"

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name) / "tree"
        leaf = cls.root / "src" / "gpt" / cls.DOCUMENT
        leaf.parent.mkdir(parents=True)
        shutil.copytree(ROOT / "src" / "gpt" / cls.DOCUMENT, leaf)
        (cls.root / "src" / "sources").symlink_to(ROOT / "src" / "sources")
        cls.leaf = leaf
        cls.metadata = leaf / "generation-metadata.tex"
        cls.published_metadata = cls.metadata.read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        self.metadata.write_text(self.published_metadata, encoding="utf-8")
        (self.leaf / RECORD).unlink(missing_ok=True)

    def bind(self):
        """State `proper` v17, which is what the contract reads."""
        text = self.published_metadata.replace(
            r"\AIGenerationProvenance{unknown}{unknown}",
            r"\AIGenerationProvenance{proper}{%d}" % BINDS_FROM)
        self.assertNotEqual(text, self.published_metadata)
        self.metadata.write_text(text, encoding="utf-8")

    def check(self, name: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(ROOT / "tools" / TOOL), "--root", str(self.root),
             "--provider", "gpt", "--document", self.DOCUMENT,
             "--check", name],
            capture_output=True, text=True, cwd=ROOT)

    def test_a_bound_ritual_leaf_still_needs_a_record(self):
        self.bind()
        done = self.check(RECORD_CHECK)
        self.assertEqual(done.returncode, 1, done.stdout)
        self.assertIn(RECORD, done.stderr)

    def test_the_remedy_the_check_prints_actually_writes_the_record(self):
        """It named no provider, so a gpt leaf's repair ran against claude."""
        self.bind()
        done = self.check(RECORD_CHECK)
        quoted = done.stderr.split("`")
        self.assertEqual(len(quoted), 3, done.stderr)
        remedy = quoted[1].split()
        self.assertEqual(remedy[:2], ["tools/tpt", "proper-chronology"])
        self.assertIn("--provider", remedy)
        self.assertEqual(remedy[remedy.index("--provider") + 1], "gpt")
        written = subprocess.run(
            [str(LAUNCHER), *remedy[1:], "--root", str(self.root)],
            capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(written.returncode, 0, written.stderr)
        self.assertTrue((self.leaf / RECORD).is_file())

    def test_the_written_record_satisfies_both_checks(self):
        self.bind()
        subprocess.run(
            [str(LAUNCHER), WIRING, "record", "--root", str(self.root),
             "--provider", "gpt", "--document", self.DOCUMENT, "--write"],
            capture_output=True, text=True, cwd=ROOT, check=True)
        for name in (RECORD_CHECK, CLAIMS_CHECK):
            with self.subTest(check=name):
                done = self.check(name)
                self.assertEqual(done.returncode, 0, done.stderr)
                # The pass line says the formulary is unaddressable rather
                # than reporting an empty dossier as a clean sweep.
                self.assertIn("ritual Mass", done.stdout)

    def test_a_ritual_leaf_may_still_not_print_a_corpus_claim(self):
        """No element here, so no assertion can be true of one.

        The empty record must not read as permission: a nuptial Mass appoints
        a great deal of Scripture, and that this repository's calendar sources
        do not encode it is a reason to print no date, never a reason to
        supply one.
        """
        self.bind()
        subprocess.run(
            [str(LAUNCHER), WIRING, "record", "--root", str(self.root),
             "--provider", "gpt", "--document", self.DOCUMENT, "--write"],
            capture_output=True, text=True, cwd=ROOT, check=True)
        stray = self.leaf / "sections-chronology-probe.tex"
        stray.write_text(
            r"\chronology{%s}{composition}{about the year 50}" % MATTHEW
            + "\n", encoding="utf-8")
        try:
            done = self.check(CLAIMS_CHECK)
            self.assertEqual(done.returncode, 1, done.stdout)
            self.assertIn("the corpus asserts no", done.stderr)
        finally:
            stray.unlink()


if __name__ == "__main__":
    unittest.main()
