"""Two transcriptions of one book are an error detector, and it is now standing.

This repository measured the detector before it built it. Two people read the
same 1861 Cummiskey hand missal out of the same Internet Archive text layer,
independently, and on 2026-07-31 the two readings were compared by hand: they
differed at 45 of the 153 orations both carried, every one of the 38 errors the
site was then serving sat inside those 45, and at the 54 loci where the two
agreed the reading was right 54 times out of 54. Disagreement is very nearly a
detector of error and agreement very nearly a certificate of correctness.

The comparison was then run once, by hand, and the file it corrected went on
changing. When `epiphany-2` was added on 2026-08-01 it brought a ninth divergence
that nobody saw, because nothing re-ran the comparison and nothing was going to.
That is what these rules are for: the comparison is derived on every run, from
the two witnesses attached to each entry, and cannot go stale between passes.

What is deliberately NOT tested here is that the witnesses agree. A gate failing
on disagreement, at a base rate near one in three, would be red the day it landed
and would be silenced rather than answered. The gate is on the UNRECORDED case —
a divergence nobody has answered, and an answer left behind by a correction —
which asks for one sentence per locus and cannot rot in either direction.
"""

from __future__ import annotations

import sys
import copy
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


checker = load_tool("check-calendar-masses")

EDITION = "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861"
ARTIFACT = (
    "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861"
    ".temporal-orations-en"
)
SIDECAR = ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"


def reading(source_id: str, text: str) -> dict:
    return {
        "lang": "en",
        "rights": "public-domain",
        "source_id": source_id,
        "text": text,
    }


def entry(*translations: dict, **fields) -> tuple[dict, list[dict]]:
    return dict(fields), list(translations)


class WitnessVerdict(unittest.TestCase):
    """Which propers are compared at all, and on what."""

    def test_one_witness_is_not_agreement(self):
        """A prayer nobody read twice must not be counted as a prayer that held.

        `None` and `False` are different findings and the count depends on it:
        242 entries carry English and 153 were read twice, so folding the other
        89 into the agreeing side would report a 231-of-242 agreement that no
        second reader ever produced.
        """
        self.assertIsNone(checker.witness_verdict([reading(EDITION, "Hear us.")]))

    def test_two_witnesses_reading_alike_agree(self):
        payload = [reading(EDITION, "Hear us."), reading(ARTIFACT, "Hear us.")]
        self.assertIs(checker.witness_verdict(payload), False)

    def test_two_witnesses_reading_differently_disagree(self):
        payload = [reading(EDITION, "Hear us."), reading(ARTIFACT, "Hear us, Lord.")]
        self.assertIs(checker.witness_verdict(payload), True)

    def test_apostrophe_and_dash_are_not_readings(self):
        """The two transcriptions differ on typography in every row that holds it.

        The artifact writes `Thro’.` with U+2019 and the sidecar `Thro'.` with
        the ASCII apostrophe, in 162 rows and 153 respectively. Comparing raw
        bytes would report the convention at nearly every locus and the wording
        at none, which is a detector that has been turned off by being too loud.
        """
        payload = [
            reading(EDITION, "of our sins. Thro'."),
            reading(ARTIFACT, "of our sins. Thro’."),
        ]
        self.assertIs(checker.witness_verdict(payload), False)

    def test_a_comma_is_a_reading(self):
        """Because a comma is what three of the nine live divergences are.

        `may hasten, what is delayed` against `may hasten what is delayed` is an
        entry the page images settled, and a normaliser generous enough to fold
        punctuation would have hidden it along with the apostrophe.
        """
        payload = [
            reading(EDITION, "may hasten, what is delayed"),
            reading(ARTIFACT, "may hasten what is delayed"),
        ]
        self.assertIs(checker.witness_verdict(payload), True)

    def test_a_language_heard_once_from_two_sources_is_not_compared(self):
        """Uniqueness is keyed `(lang, source_id)` and so is the comparison.

        A French translation beside an English one is not a second reading of
        the English, and pooling them would compare two prayers in two languages
        and call the result a divergence.
        """
        payload = [
            reading(EDITION, "Hear us."),
            {"lang": "fr", "rights": "public-domain", "source_id": ARTIFACT, "text": "x"},
        ]
        self.assertIsNone(checker.witness_verdict(payload))


class WitnessGate(unittest.TestCase):
    """What fails, and — as much to the point — what does not."""

    def test_a_recorded_disagreement_is_not_a_problem(self):
        fields, payload = entry(
            reading(EDITION, "adversity Thro'."),
            reading(ARTIFACT, "adversity. Thro'."),
            disagreement="the artifact adds a stop the page does not print",
        )
        problems, verdict = checker.witness_problems("where", fields, payload)
        self.assertIs(verdict, True)
        self.assertEqual(problems, [])

    def test_an_unrecorded_disagreement_fails(self):
        fields, payload = entry(
            reading(EDITION, "adversity Thro'."),
            reading(ARTIFACT, "adversity. Thro'."),
        )
        problems, verdict = checker.witness_problems("where", fields, payload)
        self.assertIs(verdict, True)
        self.assertEqual(len(problems), 1)
        self.assertIn(checker.OVERLAY_DISAGREEMENT, problems[0])

    def test_a_note_outliving_its_disagreement_fails(self):
        """Self-cleaning in the other direction, so it cannot rot into a licence.

        The psalm-numbering ledger beside it works the same way and for the same
        reason: a permission nobody remembers granting outlives the defect it was
        granted for, and then absorbs the next one.
        """
        fields, payload = entry(
            reading(EDITION, "Hear us."),
            reading(ARTIFACT, "Hear us."),
            disagreement="settled on the page in 1861's favour",
        )
        problems, verdict = checker.witness_problems("where", fields, payload)
        self.assertIs(verdict, False)
        self.assertEqual(len(problems), 1)
        self.assertIn("no longer have", problems[0])

    def test_a_note_with_nothing_to_disagree_with_fails(self):
        fields, payload = entry(
            reading(EDITION, "Hear us."),
            disagreement="the artifact reads otherwise",
        )
        problems, verdict = checker.witness_problems("where", fields, payload)
        self.assertIsNone(verdict)
        self.assertEqual(len(problems), 1)

    def test_an_asserted_agreement_must_be_checkable(self):
        """`detector = "sibling-agrees"` was a claim nothing read.

        50 entries carried it, meaning "the other transcription reads this the
        same way", with the other transcription nowhere in the file. Now that it
        is attached the claim is derivable, so asserting it without the second
        reading present is refused rather than believed.
        """
        fields, payload = entry(
            reading(EDITION, "Hear us."),
            detector=checker.SIBLING_AGREES,
        )
        problems, _ = checker.witness_problems("where", fields, payload)
        self.assertEqual(len(problems), 1)
        self.assertIn(checker.SIBLING_AGREES, problems[0])

    def test_an_asserted_agreement_that_is_false_fails(self):
        fields, payload = entry(
            reading(EDITION, "Hear us."),
            reading(ARTIFACT, "Hear us, Lord."),
            detector=checker.SIBLING_AGREES,
            disagreement="settled on the page",
        )
        problems, _ = checker.witness_problems("where", fields, payload)
        self.assertEqual(len(problems), 1)
        self.assertIn("witnesses differ", problems[0])


class PageImageProvenanceGate(unittest.TestCase):
    """A visual collation and its publication basis remain two exact records."""

    def setUp(self):
        import tomllib

        document = tomllib.loads(SIDECAR.read_text(encoding="utf-8"))
        self.witnesses = {row["id"]: row for row in document["sources"]}
        self.bound = [
            row
            for row in document["entries"]
            if row.get("artifact_id", "").endswith(
                "internet-archive-facsimile-pdf-6cf3c3d0"
            )
        ]

    def test_all_lasance_page_collations_resolve_exactly(self):
        self.assertEqual(len(self.bound), 13)
        for row in self.bound:
            where = f"{row['mass']}/{row['proper']}"
            self.assertEqual(
                checker.overlay_entry_source_problems(where, row, self.witnesses),
                [],
            )

    def test_a_starting_leaf_cannot_hide_a_missing_second_leaf(self):
        row = copy.deepcopy(
            next(
                row
                for row in self.bound
                if row["mass"].startswith("s-cyrilli")
                and row["proper"] == "Secret"
            )
        )
        row["ia_leaf_range"] = [912, 912]
        problems = checker.overlay_entry_source_problems(
            "Cyril/Secret", row, self.witnesses
        )
        self.assertTrue(any("artifact_page_ranges" in problem for problem in problems))

    def test_unresolved_page_images_cannot_become_the_rights_artifact(self):
        witnesses = copy.deepcopy(self.witnesses)
        witnesses["lasance-1945"]["artifact_id"] = self.bound[0]["artifact_id"]
        problems = checker.overlay_entry_source_problems(
            "Lasance", self.bound[0], witnesses
        )
        self.assertTrue(any("tracked public-domain artifact" in p for p in problems))


class TheCorpusItself(unittest.TestCase):
    """The rules above, against the file they were written for."""

    def test_the_sidecar_is_read_twice_and_reports_both_halves(self):
        """Agreement is a finding, not the absence of one.

        It is reported whether or not anything is wrong, because it is the
        strongest evidence this corpus holds and a channel carrying only faults
        would throw it away.
        """
        problems, witnessed = checker.overlay_problems(
            [ROOT / "src/sources/calendars/roman-1962/propers.yaml"]
        )
        self.assertEqual(problems, [])
        self.assertEqual(len(witnessed), 1)
        row = witnessed[0]
        self.assertEqual(row["source"], SIDECAR.relative_to(ROOT).as_posix())
        self.assertEqual(row["read_twice"], row["agree"] + row["disagree"])
        self.assertGreater(row["agree"], row["disagree"])
        # Every divergence is named, so a reader of `--json` gets the loci and
        # not only the figure.
        self.assertEqual(len(row["loci"]), row["disagree"])
        self.assertEqual(row["loci"], sorted(row["loci"]))

    def test_the_second_witness_is_registered_and_attested(self):
        """A book quoted into a calendar says which state of the rite it prints.

        The transcription is the same 1861 printing as the edition row, so it is
        held to the same act and the same strength; a transcription attests what
        the printing it transcribes attests and not one thing more.
        """
        import tomllib

        document = tomllib.loads(SIDECAR.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in document["sources"]}
        self.assertIn("cummiskey-1861-transcription", rows)
        printing = rows["cummiskey-1861"]
        transcription = rows["cummiskey-1861-transcription"]
        self.assertEqual(transcription["source_id"], ARTIFACT)
        for field in checker.OVERLAY_ATTESTS_FIELDS:
            self.assertTrue(str(transcription.get(field) or "").strip())
        for field in (checker.OVERLAY_ATTESTS, checker.OVERLAY_ATTESTS_KIND):
            self.assertEqual(transcription[field], printing[field])

    def test_the_unbound_second_witness_is_quarantined_verbatim(self):
        """The historical artifact remains evidence, never served wording.

        None of its payload may survive in positive entries until each target
        has an exact page and publication binding. The typed absence ledger,
        not an unbound transcription, carries that disposition.
        """
        import csv
        import tomllib

        artifact = ROOT / (
            "src/sources/works/eugene-cummiskey/roman-missal-english-laity/editions"
            "/philadelphia-1861/artifacts/temporal-orations-en/temporal-orations-en.tsv"
        )
        with artifact.open(encoding="utf-8") as handle:
            printed = {
                (row["formulary"], row["oration"]): row["english"]
                for row in csv.DictReader(handle, delimiter="\t")
            }
        document = tomllib.loads(SIDECAR.read_text(encoding="utf-8"))
        carried = [
            translation["text"].strip()
            for row in document["entries"]
            for translation in row["translations"]
            if translation.get("source_id") == ARTIFACT
        ]
        self.assertEqual(carried, [])
        wording = {text.strip() for text in printed.values()}
        retained = {
            translation["text"].strip()
            for row in document["entries"]
            for translation in row["translations"]
        }
        self.assertTrue(wording.isdisjoint(retained))
        unavailable = [
            row
            for row in document["untranslated"]
            if row.get("reason", {}).get("source_id") == EDITION
            and row.get("reason", {}).get("kind") == "rights-withheld"
        ]
        self.assertEqual(len(unavailable), 406)
        self.assertTrue(all("text" not in row for row in unavailable))

    def test_holy_week_is_outside_the_second_witness(self):
        """The gap the sibling could not close, and which the page closed instead.

        The artifact excludes Palm Sunday, the rest of Holy Week and the Easter
        Vigil by its own record, which is exactly where the seven orations with
        no evidence of any kind sat. They are not evidence-less now — every one
        was read on a page image — but no second witness reaches them, so the
        detector is silent there and a reader should not read silence as assent.
        """
        import tomllib

        document = tomllib.loads(SIDECAR.read_text(encoding="utf-8"))
        holy_week = {"palm-sunday", "mass-of-the-lords-supper", "good-friday", "easter-vigil"}
        for row in document["entries"]:
            if row["mass"] not in holy_week:
                continue
            sources = {t.get("source_id") for t in row["translations"]}
            self.assertNotIn(ARTIFACT, sources)
            self.assertTrue(str(row.get("collated") or "").strip(), row["mass"])


if __name__ == "__main__":
    unittest.main()
