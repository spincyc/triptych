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
"""
import json
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

DOCUMENT = ("liturgy/roman-rite/1962/propers/temporal/"
            "54-fourteenth-after-pentecost")
DOSSIER = "sections/10-date-location.tex"

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
        """A formulary this cannot address is one the contract cannot bind."""
        checked = 0
        for provider in ("claude", "gpt"):
            root = ROOT / "src" / provider / "liturgy/roman-rite/1962/propers"
            for manifest in sorted(root.glob("*/*/proper-components.toml")):
                document = manifest.parent.relative_to(
                    ROOT / "src" / provider).as_posix()
                with self.subTest(leaf=f"{provider}/{document}"):
                    done = self.run_tool("loci", "--provider", provider,
                                         "--document", document)
                    self.assertEqual(done.returncode, 0, done.stderr)
                checked += 1
        self.assertGreater(checked, 0, "no published leaf was resolved")

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
        leaf = cls.root / "src" / "claude" / DOCUMENT
        leaf.parent.mkdir(parents=True)
        shutil.copytree(ROOT / "src" / "claude" / DOCUMENT, leaf)
        (cls.root / "src" / "sources").symlink_to(ROOT / "src" / "sources")
        cls.leaf = leaf
        cls.metadata = leaf / "generation-metadata.tex"
        cls.published_metadata = cls.metadata.read_text(encoding="utf-8")
        cls.published_dossier = (leaf / DOSSIER).read_text(encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        self.metadata.write_text(self.published_metadata, encoding="utf-8")
        (self.leaf / DOSSIER).write_text(self.published_dossier,
                                         encoding="utf-8")
        (self.leaf / RECORD).unlink(missing_ok=True)

    # --- helpers ---------------------------------------------------------

    def bind(self):
        """State the version the chronology contract binds from."""
        text = self.published_metadata.replace(
            "{proper}{11}", "{proper}{%d}" % BINDS_FROM)
        self.assertNotEqual(text, self.published_metadata)
        self.metadata.write_text(text, encoding="utf-8")

    def write_record(self):
        done = subprocess.run(
            [str(LAUNCHER), WIRING, "record", "--root", str(self.root),
             "--provider", "claude", "--document", DOCUMENT, "--write"],
            capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(done.returncode, 0, done.stderr)

    def write_dossier(self, text: str):
        (self.leaf / DOSSIER).write_text(text, encoding="utf-8")

    def check(self, name: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [str(ROOT / "tools" / TOOL), "--root", str(self.root),
             "--provider", "claude", "--document", DOCUMENT, "--check", name],
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

        The leaf as published states `proper` v11. Refusing it would say the
        production that made it was wrong, which it was not: there was no
        corpus to read.
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
        self.metadata.write_text(self.published_metadata, encoding="utf-8")
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


if __name__ == "__main__":
    unittest.main()
