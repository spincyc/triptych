"""A corrected proper must not inherit a false exact-image claim."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars
from _proper_latin import LatinKey, SURFACES, decision_for, read_sidecar, text_sha256

BODY = "Misericordiae tuae remediis, quaesumus, Domine, fragilitas nostra subsistat:\nut, quae sua condicione atteritur, tua clementia reparetur. Per Dominum\nnostrum.\n"
HASH = "7124589a58d990e82bde57e5490109b76db17d82ab7d9af302f13b94d51f8793"
HISTORICAL_HASH = "ddf31f59d694ac6c7873d657d3ff89f28d0e0be682f321eeaa20710a6178b0a1"
MAME = "catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam"
PROJECT = "triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-21"
TARGET = "catholic-church.missale-romanum.vatican-typica-1962"
OLD = "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-09-03-editorial-projection"
KEY = LatinKey("september-ember-wednesday", "", "Collect", "", "", 1)


def record(identifier):
    kind, owner, work, edition, name = identifier.split(".")
    if edition.startswith("editorial-projection-"):
        edition = edition.removeprefix("editorial-projection-") + "-editorial-projection"
    base = ROOT / "src/sources/works" / owner / work / "editions" / edition
    rel = Path("artifacts") / name / "artifact.toml" if kind == "artifact" else Path("passages") / (name+".toml")
    result = tomllib.loads((base / rel).read_text())
    if result["id"] != identifier:
        raise AssertionError(identifier)
    return result


class SeptemberCollectCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = _calendars.load_document(ROOT / "src/sources/calendars", "roman-1962")
        cls.mass = next(m for s in cls.document["sections"].values() for m in s["masses"] if m["key"] == KEY.mass)
        cls.node = next(p for p in cls.mass["propers"] if p["name"] == "Collect")
        cls.records, errors = read_sidecar(ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if errors: raise AssertionError(errors)
        cls.row = cls.records[KEY]

    def test_complete_body_hash_and_independent_source_binding(self):
        self.assertEqual(BODY, self.node["text"])
        self.assertEqual(HASH, text_sha256(BODY))
        self.assertEqual(HASH, self.row["text_sha256"])
        self.assertEqual("passage."+PROJECT+".september-ember-wednesday-collect", self.row["source_id"])
        self.assertEqual("passage."+TARGET+".september-ember-wednesday-collect-word-collation-2026-10-21", self.row["verification_source_id"])
        self.assertEqual("editorial-projection-exact-to-target", self.row["relationship"])
        self.assertEqual("high", self.row["provenance_confidence"])
        decision = decision_for(KEY, BODY, self.records)
        self.assertTrue(decision.permits(SURFACES), decision.reason)
        projected = record(self.row["source_id"])
        self.assertEqual("2026-10-21", projected["verified_on"])
        self.assertEqual([[1,3]], projected["physical_line_ranges"])
        artifact = record(projected["artifact_id"])
        self.assertEqual(BODY.encode(), (ROOT / artifact["path"]).read_bytes())
        self.assertEqual([artifact["id"], "artifact."+MAME+".september-ember-wednesday-collect-la-checked-ddf31f59"], self.row["publication_source_ids"])

    def test_legacy_dementia_hash_is_denied(self):
        bad = BODY.replace("clementia", "dementia")
        self.assertEqual("75bc8b97a9a395ce0e034a2a62b198bec2d819b8572cfbe5fa514ca284569b78", text_sha256(bad))
        result = decision_for(KEY, bad, self.records)
        self.assertFalse(result.permits(SURFACES))
        self.assertIn("stale text hash", result.reason)

    def test_source_spelling_and_short_cue_remain_distinct_from_projection(self):
        historical = record(self.row["publication_source_ids"][1])
        data = (ROOT / historical["path"]).read_bytes()
        self.assertEqual(HISTORICAL_HASH, hashlib.sha256(data).hexdigest())
        self.assertEqual("public-domain", historical["rights_status"])
        self.assertIn("conditióne", data.decode())
        self.assertIn("cleméntia", data.decode())
        self.assertTrue(data.decode().endswith("Per Dóminum.\n"))
        self.assertNotIn("nostrum", data.decode())
        target = record(self.row["verification_source_id"])
        self.assertEqual("2026-10-21", target["verified_on"])
        self.assertIn("condicione", target["context"])
        self.assertIn("Per Dominum nostrum", target["context"])

    def test_superseded_legacy_payload_and_other_passage_owners_are_preserved(self):
        artifact = tomllib.loads((ROOT / OLD / "artifacts/gap-seasonal-2-orations-7f669120/artifact.toml").read_text())
        data = (ROOT / artifact["path"]).read_bytes()
        self.assertEqual("7f66912037e93998541350bf1597d8f8c9af94a5de3f6abe1149b445e4064509", hashlib.sha256(data).hexdigest())
        self.assertEqual(13947, len(data))
        self.assertEqual(BODY.replace("clementia", "dementia"), "".join(data.decode().splitlines(keepends=True)[106:109]))
        passage = tomllib.loads((ROOT / OLD / "passages/september-ember-wednesday-collect.toml").read_text())
        self.assertEqual(artifact["id"], passage["artifact_id"])
        self.assertEqual(artifact["sha256"], passage["artifact_sha256"])
        self.assertEqual([[107,109]], passage["physical_line_ranges"])
        self.assertNotIn("verified", passage["states"])
        self.assertNotIn("verified_on", passage)
        self.assertIn("withdrawn", passage["notes"])
        self.assertIn(self.row["source_id"], passage["notes"])
        legacy_target = record("passage."+TARGET+".temporal-september-ember-wednesday-orations")
        self.assertEqual("2026-09-03", legacy_target["verified_on"])
        self.assertIn("withdrawn for this Collect", legacy_target["notes"])
        self.assertIn("Secret/Postcommunion verification is otherwise unchanged", legacy_target["notes"])

    def test_existing_exact_english_absence_is_retained(self):
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        rows = [r for r in ledger["untranslated"] if (r.get("mass"),r.get("form_id"),r.get("proper"),r.get("cycle"),r.get("occurrence"),r.get("lang"),r.get("extent")) == (KEY.mass,"main","Collect","all",1,"en","body")]
        self.assertEqual(1,len(rows))
        self.assertEqual({"kind":"no-exemplar"},rows[0]["reason"])
        self.assertEqual("unavailable",rows[0]["availability"])

    def test_actual_cli_raw_and_appointed_collect_publish_correct_bytes(self):
        command=[sys.executable,"-B",str(ROOT/"tools/mass-propers"),"show","--calendar","roman-1962","--mass",KEY.mass,"--format","json"]
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,check=True)
        payload=json.loads(result.stdout)
        raw=next(p for p in payload["mass"]["propers"] if p["name"]=="Collect")
        appointed=next(p["proper"] for p in payload["appointed"] if p["name"]=="Collect")
        for node in (raw,appointed):
            self.assertEqual(BODY,node["text"])
            self.assertEqual(HASH,text_sha256(node["text"]))
            self.assertFalse(node.get("latin",{}).get("withheld",False))
            self.assertNotIn("dementia",node["text"])


if __name__ == "__main__":
    unittest.main()
