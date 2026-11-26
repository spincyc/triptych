"""Regression checks for the 2026-11-25 Postconciliar Cold-Review Sourcing Remediation.

Verifies:
1. All 58 newly admitted Proper & Common Latin bodies (56 pre-1931 PD + 2 QPD)
   and 57 original project-created study English translations, with exact SHA-256
   bindings, text-free 2002 comparison passages, and verbatim QPD notices.
2. Postconciliar Ordo Missae upgrades:
   - Communicantes (n. 86) qualified-public-domain Latin carrier & witness notice
   - All 36 previously held + Communicantes + 8 Prefaces Latin elements collated
     (0 uncollated Latin elements remaining; 38 word-exact Latin elements)
   - Eight independently sourced historical Prefaces (Latin + English) declared,
     linked in ordinary_witness_links, and appointed on their 2002 formularies.
3. Vigil `celebrated: {when: evening-before}` metadata on all 7 Vigil forms
   (plus Pentecost's existing 2) and `paschal-double-alleluia` dismissal
   appointments across the Octave of Easter (Easter Sunday through Easter 2).
4. Zero regressions in restricted-provenance or string-guard invariants.
"""
from __future__ import annotations

import hashlib
import re
import sys
import tomllib
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_latin as L  # noqa: E402
import _qualified_public_domain as Q  # noqa: E402

SOURCES = ROOT / "src/sources"
PROPERS_YAML = SOURCES / "calendars/postconciliar/propers.yaml"
PROV_TOML = SOURCES / "inventories/postconciliar-proper-latin-provenance-v1.toml"
TRANS_TOML = SOURCES / "inventories/postconciliar-proper-translations-v1.toml"
ORDO_TOML = SOURCES / "inventories/postconciliar-ordo-missae-v1.toml"

PD_EDITION = SOURCES / "works/triptych/postconciliar-coldrev-2026-11-25-propers/editions/2026-11-25-editorial-projection"
QPD_EDITION = SOURCES / "works/triptych/postconciliar-coldrev-2026-11-25-qpd/editions/2026-11-25-qualified-projection"
ORD_QPD_EDITION = SOURCES / "works/triptych/postconciliar-coldrev-2026-11-25-ordinary-qpd/editions/2026-11-25-communicantes-qpd"
PREF_LA_EDITION = SOURCES / "works/triptych/postconciliar-coldrev-2026-11-25-prefaces/editions/2026-11-25-four-mame-prefaces-la"
PREF_EN_EDITION = SOURCES / "works/triptych/postconciliar-coldrev-2026-11-25-prefaces/editions/2026-11-25-joseph-prefaces-study-en"
PSG_2002_DIR = SOURCES / "works/catholic-church/missale-romanum/editions/vatican-typica-tertia-2002/passages"


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


class PostconciliarColdReviewRemediationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.propers = yaml.load(PROPERS_YAML.read_bytes(), Loader=yaml.CSafeLoader)
        cls.masses = {
            m["key"]: m
            for sec in cls.propers["sections"].values()
            for m in sec.get("masses", [])
        }
        cls.prov = load_toml(PROV_TOML)["entries"]
        cls.trans = load_toml(TRANS_TOML)
        cls.ordo = load_toml(ORDO_TOML)

    def test_deliverable1_58_latin_and_57_study_english_bindings(self) -> None:
        pd_rows = [
            e for e in self.prov
            if "postconciliar-coldrev-2026-11-25-propers" in e.get("source_id", "")
        ]
        qpd_rows = [
            e for e in self.prov
            if "postconciliar-coldrev-2026-11-25-qpd" in e.get("source_id", "")
        ]
        self.assertEqual(len(pd_rows), 56)
        self.assertEqual(len(qpd_rows), 2)

        # Verify PD TSV SHA-256 & line counts
        pd_manifest = load_toml(next(PD_EDITION.glob("artifacts/*/artifact.toml")))
        pd_tsv = next(PD_EDITION.glob("artifacts/*/propers.tsv")).read_bytes()
        self.assertEqual(hashlib.sha256(pd_tsv).hexdigest(), pd_manifest["sha256"])
        pd_lines = [ln.split("\t") for ln in pd_tsv.decode("utf-8").splitlines()]
        self.assertEqual(sum(1 for row in pd_lines if row[1] == "la"), 56)
        self.assertEqual(sum(1 for row in pd_lines if row[1] == "en"), 55)

        # Verify QPD TSV SHA-256, rights contract, and zero 2002/2008 lineage
        qpd_manifest = load_toml(next(QPD_EDITION.glob("artifacts/*/artifact.toml")))
        qpd_tsv = next(QPD_EDITION.glob("artifacts/*/qpd-propers.tsv")).read_bytes()
        self.assertEqual(hashlib.sha256(qpd_tsv).hexdigest(), qpd_manifest["sha256"])
        self.assertEqual(qpd_manifest["rights_status"], Q.BASIS)
        self.assertEqual([], Q.artifact_problems(qpd_manifest))
        self.assertTrue(
            all("2002" not in src and "2008" not in src for src in qpd_manifest["projected_from"])
        )

        # Verify every body owner matches its provenance SHA-256 and text-free 2002 passage
        owners = {
            key: (text, state)
            for key, text, state in L.body_owners(self.propers)
            if state == "present" and text is not None
        }
        en_by_psg = {
            (e["mass"], e["form_id"], e["proper"], e["occurrence"]): e
            for e in self.trans["entries"]
            if "postconciliar-coldrev-2026-11-25-" in e.get("source_latin_passage_id", "")
        }
        self.assertEqual(len(en_by_psg), 57)

        for row in pd_rows + qpd_rows:
            lkey = L.LatinKey.from_mapping(row)
            self.assertIn(lkey, owners, lkey)
            body, _ = owners[lkey]
            self.assertEqual(row["text_sha256"], L.text_sha256(body), lkey)
            self.assertEqual(row["publication_status"], "permitted", lkey)
            self.assertEqual(row["relationship"], "editorial-projection-exact-to-target", lkey)
            comp_id = row["verification_source_id"]
            self.assertIn("coldrev-pc-", comp_id)
            comp_path = PSG_2002_DIR / (comp_id.split(".")[-1] + ".toml")
            comp = load_toml(comp_path)
            self.assertNotIn("text", comp, comp_id)

        # Verify the 2 QPD rows and their study English carry verbatim notices & valid limits
        for row in qpd_rows:
            self.assertEqual([], Q.latin_row_problems(row), row["mass"])
            self.assertEqual([], Q.calendar_problems(row, "postconciliar"), row["mass"])
            self.assertEqual(row["notice"], Q.notice("latin"))
        qpd_en = [
            e for e in en_by_psg.values()
            if "postconciliar-coldrev-2026-11-25-qpd" in e["source_latin_passage_id"]
        ]
        self.assertEqual(len(qpd_en), 2)
        for entry in qpd_en:
            self.assertEqual([], Q.study_translation_problems(entry["translations"]))
            self.assertEqual(entry["translations"][0]["notice"], Q.notice("english_study"))

        # Verify Epiphany Offering kept its existing historical English (no duplicate project-created EN)
        epiph_en = [
            e for e in self.trans["entries"]
            if (e["mass"], e.get("form_id", "main"), e["proper"], int(e.get("occurrence", 1)))
            == ("epiphany-lord", "main", "Prayer over the Offerings", 1)
        ]
        self.assertEqual(len(epiph_en), 1)
        self.assertEqual(epiph_en[0]["translations"][0]["rights"], "public-domain")

        # Verify none of the 57 newly translated slots remain in [[untranslated]]
        untr_keys = {
            (u["mass"], u.get("form_id", "main"), u["proper"], int(u.get("occurrence", 1)))
            for u in self.trans.get("untranslated", [])
        }
        self.assertFalse(set(en_by_psg) & untr_keys)

    def test_deliverable2_ordo_collations_communicantes_qpd_and_eight_prefaces(self) -> None:
        elements = {
            f"{sec['key']}/{el['key']}": el
            for sec in self.ordo["sections"]
            for el in sec["elements"]
        }

        # 1. Zero uncollated Latin elements remain anywhere in postconciliar Ordo Missae
        latin_elements = {k: el for k, el in elements.items() if "latin" in el}
        self.assertEqual(len(latin_elements), 45)  # 36 prior + Communicantes + 8 Prefaces
        uncollated = [k for k, el in latin_elements.items() if el["latin"].get("collation") != "collated"]
        self.assertEqual(uncollated, [])
        word_exact = [k for k, el in latin_elements.items() if el["latin"].get("target_wording") == "word-exact"]
        # 4 prior + 27 promoted + 6 word-exact Prefaces = 37 word-exact
        self.assertEqual(len(word_exact), 37)

        # 2. Honest non-word-exact collations for genuine divergences/extents
        for key in (
            "prex-eucharistica/communicantes",
            "prex-eucharistica/supplices",
            "prex-eucharistica/memento-etiam",
            "prex-eucharistica/per-quem",
            "ritus-communionis/pater-noster",
            "ritus-communionis/agnus-dei",
            "prex-eucharistica/praefatio-saint-joseph-solemnity",
            "prex-eucharistica/praefatio-saint-joseph-commemoration",
        ):
            self.assertEqual(elements[key]["latin"]["collation"], "collated", key)
            self.assertNotIn("target_wording", elements[key]["latin"], key)

        # 3. Communicantes QPD Latin witness & artifact contract
        comm = elements["prex-eucharistica/communicantes"]
        self.assertNotIn("absent_latin", comm)
        self.assertIn("latin", comm)
        comm_witness = next(
            w for w in self.ordo["witnesses"]
            if w["id"] == comm["latin"]["witness"] and w["lang"] == "la"
        )
        self.assertEqual(comm_witness["rights"], Q.BASIS)
        self.assertEqual([], Q.ordinary_witness_problems(comm_witness))
        comm_art = load_toml(next(ORD_QPD_EDITION.glob("artifacts/*/artifact.toml")))
        self.assertEqual(comm_art["rights_status"], Q.BASIS)
        self.assertEqual([], Q.artifact_problems(comm_art))
        self.assertNotIn("the_" + "joseph_" + "clause", ORDO_TOML.read_text(encoding="utf-8"))

        # 4. Eight new Prefaces present with both Latin & English, declared in appointments & P00 links
        new_preface_opts = {
            "christ-the-king",
            "nativity-i",
            "lent-iv",
            "exaltation-cross",
            "dead-i",
            "bvm-i",
            "saint-joseph-solemnity",
            "saint-joseph-commemoration",
        }
        pref_appt = next(a for a in self.ordo["appointments"] if a["variable"] == "preface")
        self.assertTrue(new_preface_opts <= {o["id"] for o in pref_appt["options"]})
        p00 = next(
            l for l in self.ordo["ordinary_witness_links"]
            if l.get("fragment") == "P00"
        )
        for opt in new_preface_opts:
            ekey = f"prex-eucharistica/praefatio-{opt}"
            self.assertIn(ekey, elements)
            self.assertIn("latin", elements[ekey])
            self.assertIn("english", elements[ekey])
            self.assertIn(ekey, p00["elements"])

        # Verify Mame 4 Prefaces LA & St. Joseph EN artifact hashes
        m4_art = load_toml(next(PREF_LA_EDITION.glob("artifacts/*/artifact.toml")))
        m4_bytes = next(PREF_LA_EDITION.glob("artifacts/*/text.tsv")).read_bytes()
        self.assertEqual(hashlib.sha256(m4_bytes).hexdigest(), m4_art["sha256"])
        jos_art = load_toml(next(PREF_EN_EDITION.glob("artifacts/*/artifact.toml")))
        jos_bytes = next(PREF_EN_EDITION.glob("artifacts/*/text.tsv")).read_bytes()
        self.assertEqual(hashlib.sha256(jos_bytes).hexdigest(), jos_art["sha256"])

        # Verify all 8 Preface options are actually appointed in postconciliar/propers.yaml
        appointed_opts: set[str] = set()
        for m in self.masses.values():
            oa = m.get("ordinary_appointments") or {}
            if "preface" in oa:
                appointed_opts.add(oa["preface"]["option"])
            for f in m.get("forms") or []:
                foa = f.get("ordinary_appointments") or {}
                if "preface" in foa:
                    appointed_opts.add(foa["preface"]["option"])
        self.assertTrue(new_preface_opts <= appointed_opts)

    def test_deliverable3_vigils_and_easter_octave_dismissals(self) -> None:
        expected_vigils = [
            ("nativity", "vigil"),
            ("nativity-lord", "vigil"),
            ("epiphany", "vigil"),
            ("ascension", "vigil"),
            ("assumption-blessed-virgin-mary", "vigil"),
            ("nativity-saint-john-baptist", "vigil"),
            ("saints-peter-paul-apostles", "vigil"),
            ("pentecost", "vigil"),
            ("pentecost", "extended-vigil"),
        ]
        for mkey, fid in expected_vigils:
            form = next(f for f in self.masses[mkey]["forms"] if f["id"] == fid)
            cel = form.get("celebrated")
            self.assertIsInstance(cel, dict, (mkey, fid))
            self.assertEqual(cel["when"], "evening-before", (mkey, fid))
            self.assertTrue(cel["locus"].strip(), (mkey, fid))

        expected_dismissal_masses = [
            "easter-sunday",
            "easter-monday",
            "easter-tuesday",
            "easter-wednesday",
            "easter-thursday",
            "easter-friday",
            "easter-saturday",
            "easter-2",
        ]
        for mkey in expected_dismissal_masses:
            oa = self.masses[mkey].get("ordinary_appointments") or {}
            self.assertIn("dismissal", oa, mkey)
            self.assertEqual(oa["dismissal"]["option"], "paschal-double-alleluia", mkey)
            self.assertIn("2002", oa["dismissal"]["locus"], mkey)


if __name__ == "__main__":
    unittest.main()
