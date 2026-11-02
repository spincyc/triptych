from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[2]
PUS = (
    ROOT
    / "src/sources/works/catholic-church/missale-romanum/editions"
    / "pustet-ratisbon-1862"
)
INVENTORY = ROOT / "src/sources/inventories/postconciliar-ordo-missae-v1.toml"
STRUCTURE = ROOT / "src/web/data/structure/ordinary/postconciliar.json"
TARGET_CANON = (
    ROOT
    / "src/sources/works/catholic-church/missale-romanum/editions"
    / "vatican-typica-tertia-2002/passages/ordo-missae-prex-eucharistica-i.toml"
)


PAGES = {
    303: ("17282ee4", "17282ee48b82e3e275f678c65d1ebb0f6cbbbf31027321c20fa6aa1c4f7d7bd1", 1133342, "printed p. 218"),
    347: ("3c28d4d7", "3c28d4d751308b6cc01759a9518f570be1ce9439870f1fdac4f84209341d64f9", 944147, "printed p. 262"),
    348: ("75926a78", "75926a78ac0aeb115af05776c85c12754d291274cafa45a9254d79a3e8bab538", 944738, "printed p. 263"),
    349: ("2cc46456", "2cc46456741fc210f5b7ad14d793507be42f1833f44756d298aa703cc97cb648", 968902, "printed p. 264"),
}


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


class PostconciliarOrdinaryDivergenceRecoveryTests(unittest.TestCase):
    def test_exact_pustet_page_images_control_the_four_passages(self) -> None:
        for leaf, (suffix, digest, size, printed) in PAGES.items():
            with self.subTest(leaf=leaf):
                artifact_dir = PUS / "artifacts" / f"ia-bookreader-leaf-{leaf}-{suffix}"
                artifact = load_toml(artifact_dir / "artifact.toml")
                image = artifact_dir / f"page-{leaf}.jpg"
                passage = load_toml(PUS / "passages" / f"ordo-missae-leaf-{leaf}.toml")

                self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), digest)
                self.assertEqual(image.stat().st_size, size)
                self.assertEqual(artifact["sha256"], digest)
                self.assertEqual(artifact["byte_size"], size)
                self.assertEqual(artifact["media_type"], "image/jpeg")
                self.assertEqual(artifact["rights_status"], "public-domain")
                self.assertEqual(artifact["rights_jurisdiction"], "United States")
                self.assertIn(f"leaf n{leaf}", artifact["provenance"])
                self.assertIn("independently re-fetched", artifact["provenance"])
                self.assertEqual(passage["artifact_id"], artifact["id"])
                self.assertEqual(passage["artifact_sha256"], digest)
                self.assertEqual(passage["artifact_page_ranges"], [[1, 1]])
                self.assertEqual(passage["states"], ["cataloged", "acquired", "inspected", "verified"])
                self.assertIn(printed, passage["locus"])
                self.assertIn(f"leaf n{leaf}", passage["locus"])
                self.assertNotIn("text", passage)
                self.assertNotIn("transcription_segments", passage)

    def test_named_divergences_and_peace_conclusion_are_bounded(self) -> None:
        inventory = load_toml(INVENTORY)
        absences = {row["key"]: row for row in inventory["absences"]}
        finding = absences["antecedent-diverges-at-named-words"]
        self.assertEqual(finding["kind"], "rights-withheld")
        self.assertIn("UNTESTED, not an established omission", finding["what"])
        self.assertIn("peccata nostra", finding["what"])
        self.assertIn("Perceptio Corporis et Sanguinis tui", finding["what"])
        self.assertIn("exspectantes beatam spem", finding["what"])

        elements = {
            element["key"]: element
            for section in inventory["sections"]
            for element in section["elements"]
        }
        for key in (
            "libera-nos",
            "domine-iesu-christe-qui-dixisti",
            "praeparatio-sacerdotis",
        ):
            self.assertEqual(elements[key]["absent_latin"], finding["key"])

    def test_pax_is_split_without_overstating_the_response(self) -> None:
        inventory = load_toml(INVENTORY)
        communion = next(section for section in inventory["sections"] if section["key"] == "ritus-communionis")
        keys = [element["key"] for element in communion["elements"]]
        pax_index = keys.index("pax-domini")
        self.assertEqual(keys[pax_index : pax_index + 2], ["pax-domini", "offerte-vobis-pacem"])

        pax, invitation = communion["elements"][pax_index : pax_index + 2]
        self.assertEqual(pax["missal_number"], "n. 127")
        self.assertEqual(pax["latin"]["relation"], "antecedent")
        self.assertEqual(pax["latin"]["collation"], "uncollated")
        self.assertIn("does not establish Et cum spiritu tuo", pax["latin"]["note"])
        self.assertEqual(invitation["missal_number"], "n. 128")
        self.assertEqual(invitation["latin"]["witness"],
                         "edition.archdiocese-of-milan.missale-ambrosianum.milan-de-sirturis-1712")
        self.assertEqual(invitation["latin"]["relation"], "antecedent")
        self.assertEqual(invitation["latin"]["collation"], "uncollated")
        self.assertEqual(invitation["english"]["relation"], "own")
        self.assertEqual(invitation["speaker"], "deacon-or-priest")
        self.assertEqual(invitation["english_turns"],
                         [{"key": "invitation", "seq": [1], "speaker": "deacon-or-priest"}])
        self.assertIn("separate source response is omitted", invitation["latin"]["reading_note"])
        self.assertIn("Not approved", invitation["english"]["reading_note"])
        self.assertNotIn("target_wording", invitation["latin"])
        self.assertEqual(invitation["absent_english"], "approved-english-publication-restriction")
        self.assertIn("pro opportunitate", invitation["note"])

    def test_canon_split_has_twelve_children_and_correct_rendered_branches(self) -> None:
        inventory = load_toml(INVENTORY)
        section = next(section for section in inventory["sections"] if section["key"] == "prex-eucharistica")
        elements = section["elements"]
        ep_one = [
            element
            for element in elements
            if {"group": "eucharistic-prayer", "option": "ep-i"} in element.get("alternatives", [])
        ]
        expected = [
            "te-igitur", "memento-domine", "communicantes", "hanc-igitur",
            "quam-oblationem", "qui-pridie", "unde-et-memores", "supra-quae",
            "supplices", "memento-etiam", "nobis-quoque", "per-quem",
        ]
        self.assertEqual([element["key"] for element in ep_one], expected)
        self.assertEqual(sum("latin" in element for element in ep_one), 10)
        self.assertEqual(
            [element["key"] for element in ep_one if element.get("latin", {}).get("collation") == "collated"],
            ["quam-oblationem"],
        )
        self.assertEqual(
            {element["key"]: element.get("absent_latin") for element in ep_one if "latin" not in element},
            {
                "communicantes": "element-spans-mixed-matter",
                "qui-pridie": "editio-typica-new-matter",
            },
        )

        by_key = {element["key"]: element for element in ep_one}
        self.assertEqual(by_key["supplices"]["latin"]["witness"],
                         "edition.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam")
        self.assertEqual(by_key["supplices"]["latin"]["collation"], "uncollated")
        self.assertIn("conclusion is omitted", by_key["supplices"]["latin"]["reading_note"])
        self.assertIn("common form only", by_key["communicantes"]["english"]["reading_note"])
        self.assertIn("Seasonal proper forms remain unfilled",
                      by_key["communicantes"]["english"]["reading_note"])
        self.assertNotIn("english", by_key["qui-pridie"])
        self.assertTrue(all("target_wording" not in element.get("latin", {})
                            for element in ep_one))

        def shown(option: str) -> list[str]:
            selected = []
            for element in elements:
                alternatives = element.get("alternatives", [])
                if not alternatives or {"group": "eucharistic-prayer", "option": option} in alternatives:
                    selected.append(element["key"])
            return selected

        ep_one_rendered = shown("ep-i")
        self.assertLess(ep_one_rendered.index("qui-pridie"), ep_one_rendered.index("mysterium-fidei"))
        self.assertLess(ep_one_rendered.index("mysterium-fidei"), ep_one_rendered.index("unde-et-memores"))
        self.assertLess(ep_one_rendered.index("per-quem"), ep_one_rendered.index("doxologia"))
        ep_two_rendered = shown("ep-ii")
        self.assertLess(ep_two_rendered.index("prex-eucharistica-ii"), ep_two_rendered.index("mysterium-fidei"))
        self.assertLess(ep_two_rendered.index("mysterium-fidei"), ep_two_rendered.index("doxologia"))

        target = load_toml(TARGET_CANON)
        for locus in ("Te igitur n. 84", "Qui pridie nn. 89-90", "Per quem n. 97", "Per ipsum n. 98"):
            self.assertIn(locus, target["context"])
        self.assertEqual(target["verified_on"], "2026-08-27")

    def test_generated_structure_has_the_settled_coverage(self) -> None:
        structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
        # Original61 semantic IDs remain, plus nine source-complete children.
        # This checkpoint does not include the pending next-epoch packages.
        self.assertEqual(sum(len(section["elements"]) for section in structure["sections"]), 70)
        self.assertEqual(
            structure["language_coverage"],
            [
                {"absent": 35, "elements": 70, "held": 35, "lang": "en", "missing": 35},
                {"absent": 38, "elements": 70, "held": 32, "lang": "la", "missing": 38},
            ],
        )
        self.assertEqual(
            structure["relation_coverage"],
            [
                {"collation": "uncollated", "count": 26, "lang": "en", "relation": "antecedent"},
                {"collation": "not-applicable", "count": 9, "lang": "en", "relation": "own"},
                {"collation": "collated", "count": 5, "lang": "la", "relation": "antecedent"},
                {"collation": "uncollated", "count": 27, "lang": "la", "relation": "antecedent"},
            ],
        )
        by_key = {element["key"]: element for section in structure["sections"]
                  for element in section["elements"]}
        refinements = {
            "ritus-initiales/introitus": ["ritus-initiales/signum-crucis"],
            "ritus-initiales/salutatio": ["ritus-initiales/greeting-trinitarian",
                "ritus-initiales/greeting-grace-peace", "ritus-initiales/greeting-lord",
                "ritus-initiales/greeting-bishop", "ritus-initiales/greeting-response"],
            "ritus-communionis/ecce-agnus-dei": ["ritus-communionis/ecce-agnus",
                "ritus-communionis/beati-ad-cenam", "ritus-communionis/domine-non-sum-dignus"],
        }
        order = list(by_key)
        for parent, children in refinements.items():
            self.assertEqual(by_key[parent]["kind"], "rubric")
            self.assertIsNone(by_key[parent]["translations"])
            self.assertEqual(by_key[parent]["absent"],
                             {"english": "not-a-text", "latin": "not-a-text"})
            self.assertTrue(all(order.index(parent) < order.index(child) for child in children))
            self.assertTrue(all({row["lang"] for row in by_key[child]["translations"]} == {"en", "la"}
                                for child in children))



if __name__ == "__main__":
    unittest.main()
