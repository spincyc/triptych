"""Regression tests for Roman 1962 TLM cold-review sourcing remediation (2026-11-25)."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.machinery
import importlib.util
import re
import tomllib
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
INV = REPO / "src/sources/inventories"
WORKS = REPO / "src/sources/works"
LAS46_EDITION = "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945-printing-1946"
LAS46_DIR = WORKS / "francis-xavier-lasance/the-new-roman-missal/editions/1946-benziger-revised-1945"
MAME_DIR = WORKS / "catholic-church/missale-romanum/editions/1922-tours-mame-editio-quarta-iuxta-typicam"

DELIV4_KEYS = [
    ("epiphania-domini", "main", "Postcommunion", "all", 1),
    ("transfiguratione-domini-nostri-iesu-christi", "main", "Postcommunion", "all", 1),
    ("exaltatione-s-crucis", "main", "Alleluia", "all", 1),
    ("exaltatione-s-crucis", "main", "Communion", "all", 1),
    ("commune-unius-martyris-1", "main", "Secret", "all", 1),
    ("commune-confessoris-pontificis-1", "main", "Alleluia (Tempore paschali)", "all", 1),
    ("commune-non-virginum-1", "main", "Alleluia (Tempore paschali)", "all", 1),
    ("commune-non-virginum-2", "main", "Alleluia (Tempore paschali)", "all", 1),
    ("commemoratione-omnium-fidelium-defunctorum", "first", "Gradual", "all", 1),
    ("commemoratione-omnium-fidelium-defunctorum", "second", "Gradual", "all", 1),
    ("commemoratione-omnium-fidelium-defunctorum", "third", "Gradual", "all", 1),
    ("purificatione-beatae-mariae-virginis", "main", "Alleluia", "all", 1),
    ("apparitione-beatae-mariae-virginis-immaculatae", "main", "Alleluia", "all", 1),
    ("apparitione-beatae-mariae-virginis-immaculatae", "main", "Tract", "all", 1),
    ("septem-dolorum-beatae-mariae-virginis", "main", "Gradual", "all", 1),
    ("septem-dolorum-beatae-mariae-virginis", "main", "Offertory", "all", 1),
    ("comm-septem-dolorum-beatae-mariae-virginis", "main", "Offertory", "all", 1),
    ("septem-dolorum-beatae-mariae-virginis", "main", "Communion", "all", 1),
    ("sanctissimi-nominis-beatae-mariae-virginis", "main", "Gradual", "all", 1),
    ("sanctissimi-nominis-beatae-mariae-virginis", "main", "Alleluia", "all", 1),
    ("sanctissimi-nominis-beatae-mariae-virginis", "main", "Communion", "all", 1),
    ("vigil-assumption", "main", "Gradual", "all", 1),
    ("vigil-assumption", "main", "Offertory", "all", 1),
    ("vigil-assumption", "main", "Communion", "all", 1),
    ("visitatione-beatae-mariae-virginis", "main", "Gradual", "all", 1),
    ("visitatione-beatae-mariae-virginis", "main", "Alleluia", "all", 1),
    ("visitatione-beatae-mariae-virginis", "main", "Offertory", "all", 1),
    ("visitatione-beatae-mariae-virginis", "main", "Communion", "all", 1),
    ("mass-of-the-first-sunday-after-epiphany", "main", "Introit", "all", 1),
    ("lent-3-thursday", "main", "Introit", "all", 1),
    ("pentecost-monday", "main", "Alleluia", "all", 1),
    ("pentecost-tuesday", "main", "Introit", "all", 1),
    ("pentecost-tuesday", "main", "Alleluia", "all", 1),
    ("pentecost-thursday", "main", "Alleluia", "all", 1),
    ("pentecost-ember-friday", "main", "Alleluia", "all", 1),
    ("s-andreae-apostoli", "main", "Alleluia", "all", 1),
    ("s-agathae-virginis-martyris", "main", "Introit", "all", 1),
    ("s-agathae-virginis-martyris", "main", "Communion", "all", 1),
    ("s-agnetis-virginis-martyris", "main", "Tract", "all", 1),
    ("ss-nerei-achillei-domitillae-virginis-atque", "main", "Alleluia", "all", 1),
    ("s-bartholomaei-apostoli", "main", "Alleluia", "all", 1),
    ("dedicatione-s-michaelis-archangeli", "main", "Alleluia", "all", 1),
    ("s-iosaphat-episcopi-martyris", "main", "Alleluia", "all", 1),
    ("s-polycarpi-episcopi-martyris", "main", "Alleluia", "all", 1),
    ("ss-ianuarii-episcopi-sociorum-martyrum", "main", "Alleluia", "all", 1),
]

UPGRADED_ORDINARY_LA_KEYS = {
    "oblatio/gloria-patri",
    "oblatio/suscipiat-dominus",
    "praefatio/praefatio-de-ss-trinitate",
    "praefatio/praefatio-de-nativitate",
    "praefatio/praefatio-de-epiphania",
    "praefatio/praefatio-de-quadragesima",
    "praefatio/praefatio-de-sancta-cruce",
    "praefatio/praefatio-paschalis",
    "praefatio/praefatio-de-ascensione",
    "praefatio/praefatio-de-beata-maria-virgine",
    "praefatio/praefatio-de-apostolis",
    "canon/simili-modo",
    "canon/forma-sanguinis",
    "communio/agnus-dei-defunctorum",
    "conclusio/dominus-vobiscum-defunctorum",
}

UPGRADED_ORDINARY_EN_KEYS = {
    "praefatio/praefatio-communis",
    "praefatio/sanctus",
    "praefatio/sanctus-post-praefationem",
    "praefatio/praefatio-de-spiritu-sancto-initium",
    "praefatio/praefatio-de-spiritu-sancto",
    "canon/communicantes",
    "conclusio/dominus-vobiscum-ite-missa-est",
    "conclusio/dominus-vobiscum-defunctorum",
}

REMEDIATED_ADAPTED_READING_KEYS = {
    ("friday-after-ash-wednesday", "Lesson"),
    ("lent-3-friday", "Lesson"),
    ("lent-3-monday", "Lesson"),
    ("lent-3-wednesday", "Lesson"),
    ("saturday-after-ash-wednesday", "Lesson"),
    ("pentecost-ember-saturday", "Lesson"),
    ("s-gregorii-thaumaturgi-episcopi-confessoris", "Epistle"),
    ("epiphany-2", "Epistle"),
    ("epiphany-3", "Epistle"),
    ("advent-1", "Epistle"),
    ("s-nicolai-episcopi-confessoris", "Epistle"),
}


def _load_tool(name: str):
    path = REPO / "tools" / name
    loader = importlib.machinery.SourceFileLoader(name.replace("-", "_"), str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


class TestRoman1962ColdReviewRemediation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.prov = tomllib.loads((INV / "roman-1962-proper-latin-provenance-v1.toml").read_text(encoding="utf-8"))
        cls.trans = tomllib.loads((INV / "roman-1962-proper-translations-v1.toml").read_text(encoding="utf-8"))
        cls.finding = tomllib.loads((INV / "roman-1962-finding-aid-coverage-v1.toml").read_text(encoding="utf-8"))

    def test_no_raw_json_locators_in_1962_inventories(self) -> None:
        json_pat = re.compile(r'\{\s*"|\[\s*\{')
        for field in ("locator", "verification_locator", "publication_locator"):
            for i, e in enumerate(self.prov["entries"]):
                val = e.get(field)
                if isinstance(val, str):
                    self.assertIsNone(
                        json_pat.search(val),
                        f"Raw JSON remains in provenance entries[{i}].{field} ({e.get('mass')} {e.get('proper')})",
                    )
            for i, e in enumerate(self.trans["entries"]):
                val = e.get(field)
                if isinstance(val, str):
                    self.assertIsNone(
                        json_pat.search(val),
                        f"Raw JSON remains in translations entries[{i}].{field} ({e.get('mass')} {e.get('proper')})",
                    )
        # Also confirm the 11 remediated adapted-reading entries have zero embedded JSON in provenance_evidence
        for i, e in enumerate(self.prov["entries"]):
            if (e.get("mass"), e.get("proper")) in REMEDIATED_ADAPTED_READING_KEYS:
                ev = e.get("provenance_evidence")
                if isinstance(ev, str):
                    self.assertIsNone(
                        json_pat.search(ev),
                        f"Raw JSON remains in remediated provenance_evidence entries[{i}] ({e.get('mass')} {e.get('proper')})",
                    )

    def test_deliverable2_exact_target_latin_and_vigil_nativity_alleluia(self) -> None:
        by_key = {
            (e["mass"], e.get("form", ""), e["proper"], e.get("occurrence", 1)): e
            for e in self.prov["entries"]
        }
        # 1. lent-3-thursday Introit & mass-of-the-lords-supper Pange lingua upgraded to exact-target
        for key in (
            ("lent-3-thursday", "", "Introit", 1),
            ("mass-of-the-lords-supper", "", "Hymn at the Translation of the Blessed Sacrament", 1),
            ("vigil-nativity-lord", "", "Alleluia", 1),
        ):
            self.assertIn(key, by_key)
            self.assertEqual(by_key[key]["relationship"], "editorial-projection-exact-to-target")

        # 2. vigil-nativity-lord Alleluia has Lasance 1946 English on ordinary printed p. 134
        trans_by_key = {
            (e["mass"], e.get("form_id", "main"), e["proper"], e.get("cycle", "all"), e.get("occurrence", 1)): e
            for e in self.trans["entries"]
        }
        vna = trans_by_key[("vigil-nativity-lord", "main", "Alleluia", "all", 1)]
        self.assertEqual(vna["witness"], "lasance-1945-printing-1946")
        self.assertEqual(vna["printed_page"], "134")
        self.assertEqual(vna["ia_leaf_range"], [143, 143])
        self.assertEqual(vna["translations"][0]["rights"], "public-domain")
        self.assertEqual(vna["translations"][0]["source_id"], LAS46_EDITION)

        # 3. finding-aid-coverage records the 2026-11-25 remediation evidence row
        ev_ids = {ev["id"] for ev in self.finding.get("evidence", [])}
        self.assertIn("cold-review-sourcing-remediation-2026-11-25", ev_ids)

    def test_deliverable3_ordinary_exact_latin_and_lasance_english(self) -> None:
        mo = _load_tool("mass-ordinary")
        built_list = mo.build(argparse.Namespace(root=str(REPO / "src/sources"), calendar="roman-1962"))
        self.assertEqual(len(built_list), 1)
        built = built_list[0]
        sections = built["sections"]

        total_la = 0
        exact_la = 0
        non_exact_keys = set()
        upgraded_en_found = set()
        for sec in sections:
            for elem in sec["elements"]:
                key = elem["key"]
                translations = elem.get("translations") or []
                la_rows = [t for t in translations if t.get("lang") == "la"]
                en_rows = [t for t in translations if t.get("lang") == "en"]
                if la_rows:
                    total_la += 1
                    is_exact = any(
                        r.get("relation") == "own"
                        or r.get("coverage_relationship") == "exact-target"
                        or r.get("target_wording") == "word-exact"
                        for r in la_rows
                    )
                    if is_exact:
                        exact_la += 1
                    else:
                        non_exact_keys.add(key)
                    if key in UPGRADED_ORDINARY_LA_KEYS:
                        self.assertTrue(
                            is_exact,
                            f"Expected upgraded Ordinary Latin {key} to be exact-target, got {la_rows!r}",
                        )
                if key in UPGRADED_ORDINARY_EN_KEYS:
                    self.assertTrue(
                        any(r.get("source_id") == LAS46_EDITION for r in en_rows),
                        f"Expected Lasance 1946 English on {key}, got {en_rows!r}",
                    )
                    upgraded_en_found.add(key)
                    if key == "praefatio/praefatio-de-spiritu-sancto":
                        en_row = next(r for r in en_rows if r.get("source_id") == LAS46_EDITION)
                        self.assertIn("(this day)", en_row["text"])
                        spans = en_row.get("conditional_spans", [])
                        self.assertTrue(any(s.get("text") == "(this day)" for s in spans))

        self.assertEqual(total_la, 188)
        self.assertEqual(exact_la, 185)
        self.assertEqual(
            non_exact_keys,
            {
                "praeparatio/gloria-in-excelsis-heading",
                "praefatio/praefatio-sancto-ioseph",
                "conclusio/dominus-vobiscum-ante-postcommunionem",
            },
        )
        self.assertEqual(upgraded_en_found, UPGRADED_ORDINARY_EN_KEYS)

    def test_deliverable4_45_lasance_1946_proper_english_recoveries(self) -> None:
        trans_by_key = {
            (e["mass"], e.get("form_id", "main"), e["proper"], e.get("cycle", "all"), e.get("occurrence", 1)): e
            for e in self.trans["entries"]
        }
        tsv_path = LAS46_DIR / "artifacts/coldrev-1962-propers-lasance-en/text.tsv"
        self.assertTrue(tsv_path.is_file())
        tsv_sha = hashlib.sha256(tsv_path.read_bytes()).hexdigest()
        tsv_lines = tsv_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(tsv_lines), 46)

        passages = {}
        for p in (LAS46_DIR / "passages").glob("coldrev-1962-proper-*.toml"):
            rec = tomllib.loads(p.read_text(encoding="utf-8"))
            passages[rec["id"]] = rec

        rubric_masses = {"pentecost-monday", "pentecost-tuesday", "pentecost-thursday", "pentecost-ember-friday"}
        for key in DELIV4_KEYS:
            self.assertIn(key, trans_by_key)
            e = trans_by_key[key]
            self.assertEqual(e["witness"], "lasance-1945-printing-1946")
            self.assertEqual(e["collation_result"], "confirmed")
            self.assertEqual(e["publication_artifact_sha256"], tsv_sha)
            # Ordinary integer/range printed page only (never 1298a-n, 1302a-d, 1168b)
            self.assertRegex(e["printed_page"], r"^\d+(?:-\d+)?$")
            t = e["translations"][0]
            self.assertEqual(t["rights"], "public-domain")
            self.assertEqual(t["source_id"], LAS46_EDITION)

            verify_p = passages[e["passage_id"]]
            publish_p = passages[e["publication_passage_id"]]
            self.assertEqual(verify_p["locus"], publish_p["locus"])
            leaf0, leaf1 = e["ia_leaf_range"]
            self.assertEqual(verify_p["artifact_page_ranges"], [[leaf0 + 1, leaf1 + 1]])
            line_no = publish_p["physical_line_ranges"][0][0]
            row = next(csv.DictReader([tsv_lines[0], tsv_lines[line_no - 1]], delimiter="\t"))
            self.assertEqual(row["mass"], key[0])
            self.assertEqual(row["form_id"], key[1])
            self.assertEqual(row["proper"], key[2])
            self.assertEqual(row["english"], t["text"])

            if key[0] in rubric_masses and key[2] == "Alleluia":
                ts = t.get("text_structure")
                self.assertIsInstance(ts, dict)
                self.assertEqual(ts["text_sha256"], hashlib.sha256(t["text"].encode("utf-8")).hexdigest())
                act = ts["actions"][0]
                self.assertEqual(act["kind"], "rubric")
                self.assertEqual(t["text"][act["offset"] : act["offset"] + len(act["text"])], act["text"])


if __name__ == "__main__":
    unittest.main()
