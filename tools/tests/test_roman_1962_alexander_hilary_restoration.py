"""Bounded whole-prayer source oracles; independent acceptance is a separate gate."""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
import sys
import tomllib
import unittest
ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import _calendars as C
from _proper_latin import LatinKey, SURFACES, body_owners, decision_for, publication_records, read_sidecar
from tools.tests.test_roman_1962_octnov_commemoration_source_repair import record, digest, canonical, phase5_owner
def key(r):
    return LatinKey(r["mass"], "", r["proper"], "", "", 1)
def prayer(index,r):
    return next(p for p in index[r["mass"]]["propers"] if p["name"] == r["proper"])
TARGET = "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"
TARGET_HASH = "648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a"
def project(s):
    changes = {'Iesum': 'Jesum', 'Iesu': 'Jesu', 'Iuvenale': 'Juvenale', 'eius': 'ejus', 'cuius': 'cujus', 'adiuti': 'adjuti', 'adiuvemur': 'adjuvemur', 'maiestati': 'majestati'}
    return re.sub(r"\b("+"|".join(changes)+r")\b",lambda m:changes[m[0]],s)
LANES = {'main': {'edition': 'pustet-ratisbon-1862', 'name': 'Pustet Ratisbon 1862', 'year': 1862, 'parent': 'ia-facsimile-pdf-363d6fc3', 'held': '.scratch/roman-annual-source-repair-1/pustet-1862-complete.pdf', 'parent_hash': '363d6fc3f556bf596f3b56d4efcb7be849b7e9904304ba886b7977c39e8f7474', 'pages': [525, 532, 586, 588, 589, 617, 618, 626, 627, 628, 637, 641, 645, 646], 'historical_slug': 'phase4-mayoct-alexander-oration-pages-20261022', 'project_slug': 'phase4-mayoct-alexander-twentytwo-orations-20261022', 'payload_name': 'phase4-mayoct-alexander-twentytwo-orations.txt', 'url': 'https://archive.org/download/bub_gb_E7sPAAAAIAAJ/bub_gb_E7sPAAAAIAAJ.pdf', 'hist': 'catholic-church.missale-romanum.pustet-ratisbon-1862', 'historical_id': 'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-mayoct-alexander-oration-pages-20261022', 'project_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-mayoct-alexander-twentytwo-orations-20261022', 'pdf_hash': 'd87ea7debe9992fb92b4d838e2e93893c9e2a3d1a7ccece01e9160f8926a5a3e', 'pdf_byte_size': 2963971, 'project_sha256': 'dd94f56f258e665930043284c747c41852bb47371aa2fda01337a58bb459dc11', 'project_byte_size': 4242}, 'hilary': {'edition': '1922-tours-mame-editio-quarta-iuxta-typicam', 'name': 'Mame Tours 1922, editio quarta iuxta typicam', 'year': 1922, 'parent': 'ia-scan-pdf-9873693a', 'held': '.scratch/c1-pre1955/download/mame1922.pdf', 'parent_hash': '9873693a2937c6a573ed050351b30c545b7464b87b06390785e504fb0aac7005', 'pages': [904, 905], 'historical_slug': 'phase4-hilary-doctor-pontiff-pages-20261022', 'project_slug': 'phase4-hilary-postcommunion-20261022', 'payload_name': 'phase4-hilary-postcommunion.txt', 'url': 'https://archive.org/download/missaleromanum0000unse/missaleromanum0000unse.pdf', 'hist': 'catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam', 'historical_id': 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase4-hilary-doctor-pontiff-pages-20261022', 'project_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-hilary-postcommunion-20261022', 'pdf_hash': '54f346b6e359a864a8596823ebf815d2fd8a1a0c377450c9b81edd648463e1ba', 'pdf_byte_size': 389906, 'project_sha256': '7037ccdbaacb3debd53b93d275f320b12899fb9c5f7fbf98b2526dd8c497fab0', 'project_byte_size': 147}, 'common': {'edition': 'pustet-ratisbon-1862', 'name': 'Pustet Ratisbon 1862', 'year': 1862, 'parent': 'ia-facsimile-pdf-363d6fc3', 'held': '.scratch/roman-annual-source-repair-1/pustet-1862-complete.pdf', 'parent_hash': '363d6fc3f556bf596f3b56d4efcb7be849b7e9904304ba886b7977c39e8f7474', 'pages': [698, 699], 'historical_slug': 'phase4-common-virgin-ii-orations-pages-698-699-20261022', 'project_slug': 'phase4-common-virgin-ii-two-word-repair-ce623d9f', 'payload_name': 'common-virgin-ii-collect-secret.txt', 'url': 'https://archive.org/download/bub_gb_E7sPAAAAIAAJ/bub_gb_E7sPAAAAIAAJ.pdf', 'hist': 'catholic-church.missale-romanum.pustet-ratisbon-1862', 'historical_id': 'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-common-virgin-ii-orations-pages-698-699-20261022', 'project_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-common-virgin-ii-two-word-repair-ce623d9f', 'pdf_hash': 'd78a82cf27b7fc5aa1e8aa92714304ede819fef4848cbd4f0eebaf2075c55369', 'pdf_byte_size': 466366, 'project_sha256': 'ce623d9f71e6021c3e7121f910ef5f7adce6122d6e007eb5905ec50834a6841e', 'project_byte_size': 328}}
ORACLES = json.loads(r'''[
  {
    "mass": "comm-ss-alexandri-eventii-theoduli-martyrum",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Refecti participatione muneris sacri, quaesumus, Domine Deus noster:\nut, cujus exsequimur cultum, intercedentibus sanctis tuis Alexandro,\nEventio, Theodulo et Juvenale, sentiamus effectum. Per Dominum.\n",
    "body_sha256": "29f3b83ed1b97962f387f549ee58ff2febcd15915110992273f023cb494048cd",
    "lane": "main",
    "physical_line_ranges": [
      [
        92,
        94
      ]
    ],
    "historical": "Pustet PDF 525 / printed 439, right middle, Pro SS. Alexandro etc. Postcommunio",
    "historical_pages": [
      525
    ],
    "target": "PDF 600 / printed 519, unit 2507 P, left lower",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-comm-ss-alexandri-eventii-theoduli-martyrum-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-comm-ss-alexandri-eventii-theoduli-martyrum-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-comm-ss-alexandri-eventii-theoduli-martyrum-orations-recheck-2026-10-22",
    "saint_blank": null,
    "verdict": "ready removed restoration, whole named petition including Juvenal matches; exequimur/exsequimur received spelling and j/i only"
  },
  {
    "mass": "s-hilarii-episcopi-confessoris-ecclesiae-doctoris",
    "form": "",
    "proper": "Postcommunion",
    "course": "",
    "cycle": "",
    "occurrence": 1,
    "body": "Ut nobis, Domine, tua sacrificia dent salutem: beatus Hilarius\nPontifex tuus et Doctor egregius, quaesumus, precator accedat. Per\nDominum nostrum.\n",
    "body_sha256": "7037ccdbaacb3debd53b93d275f320b12899fb9c5f7fbf98b2526dd8c497fab0",
    "lane": "hilary",
    "physical_line_ranges": [
      [
        1,
        3
      ]
    ],
    "historical": "Mame 1922 PDF 904 / printed 26*, right bottom, Pro Doctore Pontifice Postcommunio; continues PDF 905 / printed 27*, left top",
    "historical_pages": [
      904,
      905
    ],
    "target": "PDF 524 / printed 443, unit 1919 C1, left top (not PDF 523 unit 1918, which is Felix Secret)",
    "historical_conclusion": "Per Dominum.",
    "target_conclusion": "Per Dominum nostrum.",
    "projection_passage_id": "passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-s-hilarii-episcopi-confessoris-ecclesiae-doctoris-postcommunion",
    "historical_passage_id": "passage.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase4-s-hilarii-episcopi-confessoris-ecclesiae-doctoris-orations-page-image-2026-10-22",
    "target_passage_id": "passage.catholic-church.missale-romanum.vatican-typica-1962.phase4-s-hilarii-episcopi-confessoris-ecclesiae-doctoris-orations-recheck-2026-10-22",
    "saint_blank": {
      "historical": "N.",
      "target": "Hilarius",
      "case": "nominative",
      "authority": "Printed Common Doctor Pontiff blank plus named controlling Hilary C1 appointment; only this blank substituted."
    },
    "verdict": "ready removed restoration: whole petition, explicit rubric-directed N. -> Hilarius nominative and target conclusion, no clause added; Mame 1922 US public domain"
  }
]''')

class SourceRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = C.load_document(ROOT/"src/sources/calendars","roman-1962")
        cls.index = C.mass_index(cls.document)
        cls.records,errors = read_sidecar(ROOT/"src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml")
        if errors:
            raise AssertionError(errors)
    def test_exact_whole_bodies_and_six_surface_hash_joins(self):
        for r in ORACLES:
            with self.subTest(mass=r["mass"],proper=r["proper"]):
                p = prayer(self.index,r)
                self.assertEqual(r["body"],p["text"])
                self.assertEqual(r["body_sha256"],digest(p["text"]))
                self.assertEqual("composed",p["source"])
                self.assertNotIn("text_status",p)
                row = self.records[key(r)]
                self.assertNotIn("body_status",row)
                self.assertEqual((r["body_sha256"],"collated","permitted","public-domain"),
                                 tuple(row[k] for k in ["text_sha256","provenance_status","publication_status","publication_basis"]))
                self.assertEqual(set(SURFACES),set(row["surfaces"]))
                self.assertTrue(decision_for(key(r),r["body"],self.records).permits(SURFACES))
                self.assertFalse(decision_for(key(r),"Mutatum "+r["body"],self.records).permits(SURFACES))
                self.assertEqual(r["projection_passage_id"],row["source_id"])
                self.assertEqual(r["target_passage_id"],row["verification_source_id"])
                self.assertIn(r["historical_passage_id"],row["provenance_evidence"])
                self.assertNotIn(TARGET,row["publication_source_ids"])
                self.assertTrue(" ".join(p["text"].split()).endswith(project(r["target_conclusion"])))
    def test_bounded_projection_slices_and_lawful_historical_pages(self):
        for r in ORACLES:
            lane = LANES[r["lane"]]
            row = self.records[key(r)]
            self.assertEqual([lane["project_id"],lane["historical_id"]],row["publication_source_ids"])
            passage = record(r["projection_passage_id"])
            art = record(passage["artifact_id"])
            payload = (ROOT/art["path"]).read_bytes()
            self.assertEqual((lane["project_sha256"],lane["project_byte_size"]),(digest(payload),len(payload)))
            self.assertEqual((lane["project_id"],lane["project_sha256"],r["physical_line_ranges"]),
                             (passage["artifact_id"],passage["artifact_sha256"],passage["physical_line_ranges"]))
            lines = payload.decode().splitlines(keepends=True)
            self.assertEqual(r["body"],"".join("".join(lines[a-1:b]) for a,b in passage["physical_line_ranges"]))
            historical = record(r["historical_passage_id"])
            extract = record(historical["artifact_id"])
            pdf = (ROOT/extract["path"]).read_bytes()
            self.assertEqual((lane["pdf_hash"],lane["pdf_byte_size"]),(digest(pdf),len(pdf)))
            self.assertEqual("public-domain",extract["rights_status"])
            self.assertEqual(lane["parent_hash"],record(extract["derived_from"])["sha256"])
            self.assertIn(", ".join(map(str,lane["pages"])),extract["transformation"])
            selected = {p for a,b in historical["artifact_page_ranges"] for p in range(a,b+1)}
            self.assertTrue({lane["pages"].index(p)+1 for p in r["historical_pages"]} <= selected)
            target = record(r["target_passage_id"])
            self.assertEqual((TARGET,TARGET_HASH),(target["artifact_id"],target["artifact_sha256"]))
            self.assertIn(r["target"],target["locus"])
    def test_raw_and_appointed_whole_bodies_override_once(self):
        for mass in sorted({r["mass"] for r in ORACLES}):
            rows,errors = C.resolve_propers(self.document,self.index[mass])
            self.assertEqual([],errors)
            for r in [r for r in ORACLES if r["mass"] == mass]:
                found = [(p,o) for _,p,o in rows if C.proper_family(p["name"]) == r["proper"]]
                self.assertEqual([(r["body"],None)],[(p["text"],o) for p,o in found])
    def test_real_cli_same_1962_bytes_no_pre1955_published_body_or_attestation(self):
        pre,errors = publication_records(ROOT/"src/sources/calendars","roman-pre-1955")
        self.assertEqual([],errors)
        for mass in sorted({r["mass"] for r in ORACLES}):
            for calendar in ["roman-1962","roman-pre-1955"]:
                proc = subprocess.run([sys.executable,"-B",str(ROOT/"tools/mass-propers"),"show","--calendar",calendar,
                                       "--mass",mass,"--format","json"],cwd=ROOT,capture_output=True,text=True,check=True)
                payload = json.loads(proc.stdout)
                for r in [r for r in ORACLES if r["mass"] == mass]:
                    p = next(p for p in payload["mass"]["propers"] if p["name"] == r["proper"])
                    if calendar == "roman-1962":
                        self.assertEqual(r["body"],p["text"])
                    else:
                        self.assertIsNone(p.get("text"))
                        self.assertTrue(p["latin"]["withheld"])
                        self.assertFalse(decision_for(key(r),r["body"],pre).permits(SURFACES))
                        self.assertIn("target-recension",pre[key(r)]["note"])

    def test_two_removed_postcommunions_do_not_clear_other_doctor_or_papal_gaps(self):
        self.assertEqual(2,len(ORACLES))
        a,h = ORACLES
        self.assertIn("Alexandro, Eventio, Theodulo et Juvenale"," ".join(a["body"].split()))
        self.assertIn("exequimur/exsequimur",a["verdict"])
        self.assertEqual(("N.","Hilarius","nominative"),tuple(h["saint_blank"][k] for k in ["historical","target","case"]))
        self.assertIn("Pontifex tuus et Doctor egregius",h["body"])
        # John of the Cross alone now has a complete accepted Schott antecedent.
        john = LatinKey("s-ioannis-a-cruce-confessoris-ecclesiae", "", "Collect", "", "", 1)
        accepted = phase5_owner(self.document, john, self.records)
        self.assertIn("atque Doctorem", accepted["body"])
        self.assertEqual(accepted["body"],
                         prayer(self.index, dict(mass=john.mass, proper=john.proper))["text"])
        self.assertIn("anselm-schott", accepted["historical_passage_id"])
        for mass in ["s-antonii-padua-confessoris-ecclesiae-doctoris","comm-s-silvestri-i-papae-confessoris"]:
            self.assertNotIn("text",prayer(self.index,dict(mass=mass,proper="Collect")))

if __name__ == "__main__":
    unittest.main()
