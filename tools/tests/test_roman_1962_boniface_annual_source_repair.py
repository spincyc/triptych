"""Boniface: retained historical page, exact local prayers, no guessed Common set."""
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

MASS = "comm-s-bonifatii-martyris"
PROJECT = "triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22"
HISTORICAL = "catholic-church.missale-romanum.pustet-ratisbon-1862"
TARGET = "catholic-church.missale-romanum.vatican-typica-1962"
PDF = "artifact." + HISTORICAL + ".boniface-page-445-883fb31d"
PDF_HASH = "883fb31d665d53a701a1d7a32012b6de3bf7d7ce4bfbaef235873595ea7bc9b6"
PROJECT_ARTIFACT = "artifact." + PROJECT + ".boniface-three-orations-ae811235"
BODY = (
    "Refecti participatione muneris sacri, quaesumus, Domine Deus noster:\n"
    "ut, cujus exsequimur cultum, intercedente beato Bonifatio Martyre tuo,\n"
    "sentiamus effectum. Per Dominum.\n"
)
HASH = "5003e0531a176d0ce4d3d1dd0c3476e3a178d3355acbc09b08985dd2386be0c7"
UNCHANGED = {
    "Collect": "04e1c0bdb1009538613a545d3853c8995c2e48f20f4d2eb0c731b1828b8e261e",
    "Secret": "7136443afcf7107246f1dc917fdacadb4424768c52943b27722560da283fe077",
}


def record(identifier):
    kind, owner, work, edition, name = identifier.split(".")
    if edition.startswith("editorial-projection-"):
        edition = edition.removeprefix("editorial-projection-") + "-editorial-projection"
    base = ROOT / "src/sources/works" / owner / work / "editions" / edition
    relative = Path("artifacts") / name / "artifact.toml" if kind == "artifact" else Path("passages") / (name + ".toml")
    result = tomllib.loads((base / relative).read_text())
    if result["id"] != identifier:
        raise AssertionError(identifier)
    return result


class BonifaceAnnualSourceRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = _calendars.load_document(ROOT / "src/sources/calendars", "roman-1962")
        cls.mass = _calendars.mass_index(cls.document)[MASS]
        cls.propers = {p["name"]: p for p in cls.mass["propers"]}
        cls.records, errors = read_sidecar(ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if errors:
            raise AssertionError(errors)

    def test_complete_postcommunion_has_fresh_exact_body_and_permission(self):
        node = self.propers["Postcommunion"]
        self.assertEqual(BODY, node["text"])
        self.assertNotIn("text_status", node)
        key = LatinKey(MASS, "", "Postcommunion", "", "", 1)
        row = self.records[key]
        self.assertEqual(HASH, text_sha256(BODY))
        self.assertEqual(HASH, row["text_sha256"])
        self.assertNotIn("body_status", row)
        self.assertEqual("passage." + PROJECT + ".boniface-postcommunion", row["source_id"])
        self.assertEqual("editorial-projection-exact-to-target", row["relationship"])
        self.assertEqual([PROJECT_ARTIFACT, PDF], row["publication_source_ids"])
        self.assertTrue(decision_for(key, BODY, self.records).permits(SURFACES))
        self.assertFalse(decision_for(key, BODY.replace("Bonifatio", "N."), self.records).permits(SURFACES))

    def test_collect_and_secret_bytes_are_unchanged_but_loci_are_repaired(self):
        for name, expected in UNCHANGED.items():
            with self.subTest(proper=name):
                body = self.propers[name]["text"]
                key = LatinKey(MASS, "", name, "", "", 1)
                row = self.records[key]
                self.assertEqual(expected, text_sha256(body))
                self.assertEqual(expected, row["text_sha256"])
                self.assertEqual("passage." + PROJECT + ".boniface-" + name.lower(), row["source_id"])
                self.assertIn("printed p. 445", row["locator"])
                self.assertNotIn("text-layer", row["locator"])
                self.assertTrue(decision_for(key, body, self.records).permits(SURFACES))

    def test_all_projected_passages_cover_exact_bytes(self):
        artifact = record(PROJECT_ARTIFACT)
        data = (ROOT / artifact["path"]).read_bytes()
        self.assertEqual(artifact["sha256"], hashlib.sha256(data).hexdigest())
        self.assertEqual(artifact["byte_size"], len(data))
        self.assertEqual("project-created", artifact["rights_status"])
        self.assertEqual([PDF, "artifact." + TARGET + ".cmaa-facsimile-pdf"], artifact["projected_from"])
        lines = data.decode().splitlines(keepends=True)
        for name in ("Collect", "Secret", "Postcommunion"):
            passage = record("passage." + PROJECT + ".boniface-" + name.lower())
            self.assertEqual(artifact["sha256"], passage["artifact_sha256"])
            self.assertEqual("2026-10-22", passage["verified_on"])
            begin, end = passage["physical_line_ranges"][0]
            self.assertEqual(self.propers[name]["text"], "".join(lines[begin - 1:end]))

    def test_retained_historical_page_is_exact_and_has_complete_parent_chain(self):
        artifact = record(PDF)
        data = (ROOT / artifact["path"]).read_bytes()
        self.assertEqual(PDF_HASH, hashlib.sha256(data).hexdigest())
        self.assertEqual((110089, 1, "public-domain"), (len(data), artifact["page_count"], artifact["rights_status"]))
        self.assertEqual(110089, artifact["byte_size"])
        parent = record(artifact["derived_from"])
        self.assertEqual("363d6fc3f556bf596f3b56d4efcb7be849b7e9904304ba886b7977c39e8f7474", parent["sha256"])
        self.assertEqual(102880787, parent["byte_size"])
        passage = record("passage." + HISTORICAL + ".boniface-three-orations-page-image-2026-10-22")
        self.assertEqual(PDF, passage["artifact_id"])
        self.assertEqual(PDF_HASH, passage["artifact_sha256"])
        self.assertEqual([[1, 1]], passage["artifact_page_ranges"])
        self.assertEqual("2026-10-22", passage["verified_on"])
        self.assertIn("Bonifacio", passage["notes"])
        self.assertIn("coelestibus", passage["notes"])

    def test_target_recheck_is_separate_from_publication_authority(self):
        target = record("passage." + TARGET + ".boniface-three-orations-recheck-2026-10-22")
        self.assertEqual("648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a", target["artifact_sha256"])
        self.assertEqual("2026-10-22", target["verified_on"])
        self.assertIn("200 and 400 dpi", target["notes"])
        self.assertIn("Secret C 3", target["context"])
        self.assertIn("Postcommunion C 4", target["context"])
        for name in self.propers:
            row = self.records[LatinKey(MASS, "", name, "", "", 1)]
            self.assertEqual(target["id"], row["verification_source_id"])
            self.assertNotIn(target["artifact_id"], row["publication_source_ids"])

    def test_unresolved_common_candidates_do_not_displace_local_orations(self):
        self.assertEqual(
            {"mass": "commune-martyrum-tempore-paschali-1", "citation": "Commune Sanctorum [15]",
             "common_sets": {"orations": {"state": "unresolved", "candidates": ["c3", "c4"]}}},
            self.mass["takes_from"],
        )
        rows, _ = _calendars.resolve_propers(self.document, self.mass)
        for name, own in self.propers.items():
            matching = [(p, origin) for _, p, origin in rows if p["name"] == name]
            self.assertEqual([(own, None)], matching)
        self.assertFalse(any(name.startswith(("Collect (", "Secret (", "Postcommunion (")) for _, p, _ in rows for name in [p["name"]]))

    def test_existing_english_postcommunion_absence_is_not_invented(self):
        ledger = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        rows = [r for r in ledger["untranslated"] if
                (r.get("mass"), r.get("form_id"), r.get("proper"), r.get("cycle"), r.get("occurrence"), r.get("lang"), r.get("extent")) ==
                (MASS, "main", "Postcommunion", "all", 1, "en", "body")]
        self.assertEqual(1, len(rows))
        self.assertEqual("unavailable", rows[0]["availability"])
        self.assertEqual("witness-gap", rows[0]["reason"]["kind"])

    def test_actual_cli_raw_and_appointed_prayers_publish_same_body(self):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/mass-propers"), "show", "--calendar", "roman-1962",
             "--mass", MASS, "--format", "json"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        payload = json.loads(result.stdout)
        for name, expected in self.propers.items():
            raw = next(p for p in payload["mass"]["propers"] if p["name"] == name)
            appointed = [p for p in payload["appointed"] if p["name"] == name]
            self.assertEqual(1, len(appointed))
            self.assertIsNone(appointed[0]["taken_from"])
            for node in (raw, appointed[0]["proper"]):
                self.assertEqual(expected["text"], node["text"])
                self.assertFalse(node.get("latin", {}).get("withheld", False))


if __name__ == "__main__":
    unittest.main()
