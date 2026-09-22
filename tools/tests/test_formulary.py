"""Mass-keyed commentary loci: matched on elements, never on the Sunday number.

The defect guarded against is a commentator filed under the wrong Mass because
his heading's number drifted. So the first tests pin the Eighteenth Sunday of
the 1962 calendar, where the drift is known: Rupert's, Honorius's and
Durandus's "eighteenth" Sundays keep the chants and give another Gospel, and
the 1962 Gospel of the paralytic is their NINETEENTH. The rest keep the file
true: a heading not in the lines it names, an unquoted string, an unknown key,
a role outside the vocabulary and a structural locus that names elements are
each refused.
"""
from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _containment  # noqa: E402
import _formulary  # noqa: E402
import _standing  # noqa: E402

CITATIONS = _formulary.Citations(ROOT)


def by_locus(payload: dict) -> dict[str, dict]:
    return {row["locus"]: row for row in payload["listed"]}


def element(row: dict, role: str, alternative: str | None = None) -> list[dict]:
    return [
        e for e in row["elements"]
        if e["role"] == role and (alternative is None or e.get("alternative") == alternative)
    ]


class EighteenthSundayTests(unittest.TestCase):
    """The fixture the plan of 2026-09-22 set for 1962 #58, against the tracked file."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = _formulary.project(
            ROOT, "roman-1962", "pentecost-18",
            registry=_standing.Registry(ROOT), holdings=_containment.Holdings(ROOT),
            citations=CITATIONS,
        )
        cls.rows = by_locus(cls.payload)

    def test_the_tracked_loci_validate(self) -> None:
        self.assertEqual(_formulary.validate(ROOT, CITATIONS, _standing.Registry(ROOT)), [])

    def test_rupert_xii_18_is_listed_with_another_gospel_and_no_drift(self) -> None:
        row = self.rows["XII.18"]
        self.assertEqual(row["drift"]["status"], "none")
        self.assertIn("gospel", row["different"])
        self.assertEqual(element(row, "gospel")[0]["ref"], "Matthew 23:2")
        self.assertTrue({"introit", "epistle", "gradual", "offertory", "communion"} <= set(row["same"]))

    def test_rupert_xii_19_carries_the_gospel_and_drifts(self) -> None:
        row = self.rows["XII.19"]
        self.assertEqual(row["same"], ["gospel"])
        self.assertEqual(row["drift"]["status"], "label-drift")
        self.assertIn("after-pentecost 19", row["drift"]["note"])
        self.assertIn("after-pentecost 18", row["drift"]["note"])

    def test_honorius_iv_84_gives_the_two_commandments(self) -> None:
        row = self.rows["IV.84"]
        self.assertEqual(row["drift"]["status"], "none")
        self.assertIn("gospel", row["different"])
        self.assertIn("alleluia", row["different"])
        self.assertIn("collect", row["same"])

    def test_honorius_iv_86_carries_the_gospel_and_drifts(self) -> None:
        row = self.rows["IV.86"]
        self.assertEqual(row["same"], ["gospel"])
        self.assertEqual(row["drift"]["status"], "label-drift")

    def test_durandus_vi_135_gives_two_other_gospels_as_alternatives(self) -> None:
        row = self.rows["VI.135"]
        gospels = element(row, "gospel", "in quibusdam Ecclesiis")
        self.assertEqual(len(gospels), 2)
        self.assertEqual({g["result"] for g in gospels}, {"different"})
        self.assertEqual(row["drift"]["status"], "none")

    def test_durandus_vi_136_carries_the_gospel_in_some_churches(self) -> None:
        row = self.rows["VI.136"]
        self.assertEqual(row["same"], ["gospel"])
        self.assertEqual(element(row, "gospel")[0]["alternative"], "in quibusdam Ecclesiis")
        self.assertEqual(row["drift"]["status"], "label-drift")

    def test_schuster_matches_every_element(self) -> None:
        row = self.rows["vol. III pp. 167-170"]
        self.assertEqual(row["different"], [])
        self.assertEqual(len(row["same"]), len(self.payload["elements"]))
        self.assertEqual(row["standing"]["standing"], "blessed")

    def test_the_continuation_is_credited_to_fromage(self) -> None:
        row = self.rows["Time after Pentecost II (series vol. XI), pp. 393-409"]
        self.assertEqual(row["writer"]["person"], "lucien-fromage")
        self.assertEqual(row["standing"]["person"], "lucien-fromage")
        self.assertEqual(row["different"], [])

    def test_blunts_trinity_nineteen_drifts_in_season_and_number(self) -> None:
        row = self.rows["trinity-19"]
        self.assertEqual(set(row["same"]), {"collect", "gospel"})
        self.assertIn("after-trinity 19", row["drift"]["note"])
        self.assertEqual(row["standing"]["standing"], "non-catholic")

    def test_the_vacant_sunday_structural_loci_are_listed_by_occasion(self) -> None:
        loci = {(row["work_id"], row["locus"]) for row in self.payload["structural"]}
        self.assertIn(("work.bernold-of-constance.micrologus-de-ecclesiasticis-observationibus", "XXIX"), loci)
        self.assertIn(("work.john-beleth.summa-de-ecclesiasticis-officiis", "L"), loci)

    def test_no_row_is_weak_here(self) -> None:
        self.assertFalse(any((row.get("weak") or {}).get("weak") for row in self.payload["listed"]))

    def test_holdings_are_joined(self) -> None:
        self.assertEqual(self.rows["IV.84"]["holding"]["status"], "held")


class PortabilityTests(unittest.TestCase):
    """The same rows project onto another mass, with no row naming either."""

    def project(self, mass: str) -> dict:
        return _formulary.project(ROOT, "roman-1962", mass, registry=_standing.Registry(ROOT), citations=CITATIONS)

    def test_the_nineteenth_sunday_lists_the_nineteenth_chapters_without_drift(self) -> None:
        rows = by_locus(self.project("pentecost-19"))
        self.assertEqual(rows["XII.19"]["drift"]["status"], "none")
        self.assertNotIn("XII.18", rows)
        self.assertEqual(rows["VIII.19"]["drift"]["status"], "none")

    def test_a_structural_locus_follows_its_occasion_not_a_number(self) -> None:
        payload = self.project("advent-4")
        self.assertIn("XXIX", {row["locus"] for row in payload["structural"]})
        self.assertEqual(self.project("pentecost-17")["structural"], [])

    def test_an_unknown_mass_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            self.project("no-such-mass")


def mass(key: str, introit: str, gospel: str) -> dict:
    return {
        "key": key,
        "name": key,
        "propers": [
            {"name": "Introit", "incipit": introit, "source": "scripture", "verses": []},
            {"name": "Gospel", "source": "scripture",
             "verses": [{"ref": gospel, **CITATIONS.parse(gospel)}]},
        ],
    }


class WeakFlagTests(unittest.TestCase):
    """A match only on a chant the calendar repeats is weak, and says why."""

    def setUp(self) -> None:
        self.document = {
            "psalm_numbering": "vulgate",
            "sections": {"seasonal": {"kind": "temporal", "masses": [
                mass("pentecost-3", "Respice in me", "Luke 15:1-10"),
                mass("pentecost-4", "Respice in me", "Luke 5:1-11"),
                mass("pentecost-5", "Exaudi Domine", "Matthew 5:20-24"),
            ]}},
        }
        self.recurrence = _formulary.Recurrence(self.document, CITATIONS)

    def locus(self, *elements: dict) -> dict:
        return {"locus": "1", "own_label": "x", "treatment": "whole-office", "elements": list(elements)}

    def run_locus(self, locus: dict, key: str) -> dict:
        target = next(m for m in self.document["sections"]["seasonal"]["masses"] if m["key"] == key)
        elements = _formulary.mass_elements(self.document, target, CITATIONS)
        return _formulary.project_locus({}, locus, target, elements, CITATIONS, self.recurrence)

    def test_a_repeated_introit_alone_is_weak(self) -> None:
        row = self.run_locus(self.locus({"role": "introit", "incipit": "Respice in me"}), "pentecost-3")
        self.assertTrue(row["listed"])
        self.assertTrue(row["weak"]["weak"])
        self.assertEqual(list(row["weak"]["recurrence"].values()), [2])

    def test_a_gospel_found_once_is_not_weak(self) -> None:
        row = self.run_locus(
            self.locus({"role": "introit", "incipit": "Respice in me"}, {"role": "gospel", "ref": "Luke 15:3"}),
            "pentecost-3",
        )
        self.assertFalse(row["weak"]["weak"])

    def test_one_other_role_alone_is_not_listed(self) -> None:
        document = dict(self.document)
        target = self.document["sections"]["seasonal"]["masses"][2]
        target = {**target, "propers": target["propers"] + [
            {"name": "Offertory", "incipit": "Benedicam Dominum", "source": "scripture", "verses": []}
        ]}
        elements = _formulary.mass_elements(document, target, CITATIONS)
        row = _formulary.project_locus(
            {}, self.locus({"role": "offertory", "incipit": "Benedicam Dominum qui"}), target, elements, CITATIONS, None
        )
        self.assertFalse(row["listed"])


class NormalisationTests(unittest.TestCase):
    def test_latin_spelling_variants_meet(self) -> None:
        self.assertTrue(_formulary.incipits_match("Laetatus sum", "Letatus sum in his"))
        self.assertTrue(_formulary.incipits_match("Sanctificavit Moyses", "Sanctificauit Moises altare"))
        self.assertTrue(_formulary.incipits_match("Ascendens Jesus", "Ascendens Iesus in naviculam"))

    def test_one_word_never_matches(self) -> None:
        self.assertFalse(_formulary.incipits_match("Dirigatur", "Dirigatur oratio mea"))

    def test_different_words_do_not_match(self) -> None:
        self.assertFalse(_formulary.incipits_match("Da pacem", "Dirigat corda"))

    def test_a_chapter_is_never_narrowed_and_verses_stay_verses(self) -> None:
        chapter = CITATIONS.spans("Matthew 9")
        self.assertTrue(_formulary.overlaps(chapter, CITATIONS.spans("Matthew 9:18-26")))
        self.assertFalse(
            _formulary.overlaps(CITATIONS.spans("Matthew 9:2-6"), CITATIONS.spans("Matthew 9:18-26"))
        )

    def test_a_hebrew_calendar_psalm_is_compared_in_vulgate_numbering(self) -> None:
        self.assertTrue(
            _formulary.overlaps(CITATIONS.spans("Psalm 122:1", "hebrew"), CITATIONS.spans("Psalm 121:1"))
        )


class ValidatorTests(unittest.TestCase):
    """A sandbox library of one work, one tracked layer and one remote artifact."""

    LAYER = "Line one.\nCAPUT XVIII.\nDominica decima octava post Pentecosten.\nDa pacem, Domine.\n"

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        edition = self.root / "src/sources/works/ns/work/editions/ed"
        self.write("src/sources/works/ns/work/work.toml", 'id = "work.ns.work"\ntitle = "Work"\n')
        self.write("src/sources/works/ns/other/work.toml", 'id = "work.ns.other"\ntitle = "Other"\n')
        self.write(
            "src/sources/works/ns/work/editions/ed/artifacts/layer/artifact.toml",
            'id = "artifact.ns.work.ed.layer"\nmedia_type = "text/plain"\nstorage = "tracked"\n'
            'path = "src/sources/works/ns/work/editions/ed/artifacts/layer/layer.txt"\n',
        )
        (edition / "artifacts/layer/layer.txt").write_text(self.LAYER, encoding="utf-8")
        self.write(
            "src/sources/works/ns/work/editions/ed/artifacts/remote/artifact.toml",
            'id = "artifact.ns.work.ed.remote"\nmedia_type = "text/plain"\nstorage = "remote"\n',
        )
        self.write(
            "src/sources/works/ns/other/editions/ed/artifacts/layer/artifact.toml",
            'id = "artifact.ns.other.ed.layer"\nmedia_type = "text/plain"\nstorage = "tracked"\n'
            'path = "src/sources/works/ns/work/editions/ed/artifacts/layer/layer.txt"\n',
        )

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def loci(self, locus: str) -> list[str]:
        self.write(
            "src/sources/commentary/formulary-loci.yaml",
            textwrap.dedent(
                """\
                schema: 'triptych-commentary-formulary-loci/v1'
                updated: '2026-09-22'
                numbering: 'vulgate'
                works:
                  - work_id: 'work.ns.work'
                    genre: 'office-exposition'
                    locus_grammar: 'chapter'
                    label_system: 'his own'
                    loci:
                """
            )
            + textwrap.indent(textwrap.dedent(locus), " " * 6),
        )
        return _formulary.validate(self.root, CITATIONS)

    GOOD = """\
        - locus: 'XVIII'
          read_in: 'artifact.ns.work.ed.layer'
          lines: [2, 4]
          own_label: 'Dominica decima octava post Pentecosten'
          season: 'after-pentecost'
          ordinal: 18
          treatment: 'whole-office'
          elements:
            - {role: 'introit', incipit: 'Da pacem', ref: 'Sirach 36:18'}
          state: 'located'
          checked_on: '2026-09-22'
        """

    def test_a_well_formed_locus_validates(self) -> None:
        self.assertEqual(self.loci(self.GOOD), [])

    def test_a_heading_outside_its_lines_is_refused(self) -> None:
        errors = self.loci(self.GOOD.replace("[2, 4]", "[1, 2]"))
        self.assertTrue(any("does not occur in lines 1-2" in e for e in errors), errors)

    def test_lines_past_the_layer_are_refused(self) -> None:
        errors = self.loci(self.GOOD.replace("[2, 4]", "[2, 40]"))
        self.assertTrue(any("run past the layer" in e for e in errors), errors)

    def test_an_unquoted_string_is_refused(self) -> None:
        errors = self.loci(self.GOOD.replace("state: 'located'", "state: located"))
        self.assertTrue(any("is unquoted" in e for e in errors), errors)

    def test_an_unknown_key_is_refused(self) -> None:
        errors = self.loci(
            self.GOOD.replace("          state: 'located'", "          state: 'located'\n          mass: 'pentecost-18'")
        )
        self.assertTrue(any("unknown fields: mass" in e for e in errors), errors)

    def test_a_role_outside_the_vocabulary_is_refused(self) -> None:
        errors = self.loci(self.GOOD.replace("role: 'introit'", "role: 'antiphon'"))
        self.assertTrue(any("role 'antiphon'" in e for e in errors), errors)

    def test_a_structural_locus_naming_elements_is_refused(self) -> None:
        errors = self.loci(self.GOOD.replace("'whole-office'", "'structural'"))
        self.assertTrue(any("is structural and names no element" in e for e in errors), errors)

    def test_an_element_with_nothing_to_compare_is_refused(self) -> None:
        errors = self.loci(self.GOOD.replace("incipit: 'Da pacem', ref: 'Sirach 36:18'", "said: 'he prays for peace'"))
        self.assertTrue(any("neither an incipit nor a ref" in e for e in errors), errors)

    def test_lines_in_a_remote_layer_are_refused(self) -> None:
        errors = self.loci(self.GOOD.replace("ed.layer", "ed.remote"))
        self.assertTrue(any("need a tracked layer to replay" in e for e in errors), errors)

    def test_a_layer_of_another_work_is_refused_unless_contained(self) -> None:
        errors = self.loci(self.GOOD.replace("artifact.ns.work.ed.layer", "artifact.ns.other.ed.layer"))
        self.assertTrue(any("does not record work.ns.work inside it" in e for e in errors), errors)

    def test_season_without_ordinal_is_refused(self) -> None:
        errors = self.loci(self.GOOD.replace("          ordinal: 18\n", ""))
        self.assertTrue(any("season and ordinal together" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
