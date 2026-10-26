"""Bullarium source bounds, geometry warnings and truthful constituent ownership."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"scripts"))
import _bullarium as b


class BullariumTests(unittest.TestCase):
    def setUp(self):
        directory=b.ROOT/".scratch/bullarium_reconstruction/tests"
        directory.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=directory)
        self.root=Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def xml(self,objects):
        payload='<DjVuXML><BODY>'
        for leaf,rows in objects:
            payload+=f'<OBJECT usemap="w_{leaf:04d}.djvu" width="2000" height="3000">'
            for text,x0,x1,y in rows:
                payload+='<LINE>'
                for word in text.split():
                    payload+=f'<WORD coords="{x0},{y+20},{x1},{y}">{word}</WORD>'
                payload+='</LINE>'
            payload+='</OBJECT>'
        path=self.root/"ocr.xml"
        path.write_text(payload+'</BODY></DjVuXML>')
        return path

    def test_physical_lines_are_lf_only(self):
        self.assertEqual(b.lines(b"a\vb\r\nc\n"),["a\vb","c"])

    def test_numerals_keep_ambiguity(self):
        self.assertEqual(b.numeral("Vili"),8)
        self.assertEqual(b.numeral("L"),50)
        self.assertIsNone(b.numeral("IM"))
        self.assertIsNone(b.numeral("ceni"))
        self.assertEqual(b.heading("An. C. 1628 CCXCVIII."),("CCXCVIII",298))

    def test_leaf_join_uses_filename_not_ordinal(self):
        path=self.xml([(0,[("prima",200,850,600)]),(7,[("secunda",200,850,600)])])
        result=b.page_map(b"prima\n\nsecunda\n",path,{"pages":[{"leafNum":7,"pageNumber":"1900"}]})
        self.assertEqual([p["leaf"] for p in result["pages"]],[0,7])
        self.assertIsNone(result["pages"][0]["source_page_label_raw"])
        self.assertEqual(result["pages"][1]["source_page_label_raw"],"1900")
        self.assertEqual(result["pages"][1]["physical_line_start"],3)

    def test_complete_token_mismatch_is_refused(self):
        path=self.xml([(1,[("prima",200,850,600)])])
        with self.assertRaisesRegex(ValueError,"every TXT token"):
            b.page_map(b"prima secunda\n",path,{"pages":[]})

    def test_reversed_columns_are_held(self):
        path=self.xml([(1,[("left",200,850,600),("right",1100,1800,700),("leftagain",200,850,800)])])
        result=b.page_map(b"left\nright\nleftagain\n",path,{"pages":[]})
        self.assertIn("body-column-order-reverses",result["pages"][0]["layout_hold_reasons"])

    def test_merged_body_line_is_held(self):
        path=self.xml([(1,[("merged columns",200,1800,600)])])
        result=b.page_map(b"merged columns\n",path,{"pages":[]})
        self.assertIn("wide-body-lines-cross-columns-or-tables",result["pages"][0]["layout_hold_reasons"])

    def admission_fixture(self,count=2):
        text=b"I.\nTitulus\nLeo Papa I\nVerba integra.\nData Romae.\nII.\nAlter titulus\nLeo Papa I\nAlia verba.\nData Romae.\n"
        target=self.root/"src/sources/works/bullarium-romanum/volume-01/editions/1857-turin-latin/artifacts/ocr/ocr.txt"
        b.write(target,text)
        artifact={"schema":1,"record_type":"artifact","id":"artifact.example.ocr","edition_id":"edition.example",
            "storage":"tracked","media_type":"text/plain","rights_status":"public-domain","rights_basis":"Identified1857printing.",
            "path":str(target.relative_to(self.root)),"sha256":b.sha(text),"byte_size":len(text),"source_url":"https://example.org/ocr.txt"}
        b.record(target.parent/"artifact.toml",artifact)
        container={"work_id":"work.example.volume","edition_id":"edition.example","edition_path":"src/sources/works/bullarium-romanum/volume-01/editions/1857-turin-latin",
            "artifacts":{"ocr":{"id":artifact["id"],"sha256":artifact["sha256"],"manifest":str((target.parent/"artifact.toml").relative_to(self.root))}}}
        units=[{"id":f"bullarium.volume-01.unit-{i:04d}","volume":1,"artifact_id":artifact["id"],"artifact_sha256":artifact["sha256"],
            "act_number_raw":str(i),"status":"held"} for i in range(1,count+1)]
        b.write(self.root/b.CATALOG,b.json_bytes({"schema":"triptych-bullarium-catalog/v1","volumes":[{"volume":1,"container":container}],
            "units":units,"coverage":{"raw_candidate_units":count,"independent_papal_acts_admitted":0,"units_held":count}}))
        b.write(self.root/b.MANIFEST,b.json_bytes({"schema":"triptych-papal-typeset/v1","documents":[]}))
        return artifact,units

    def review(self,artifact,unit,number):
        item={"unit_id":unit["id"],"artifact_sha256":artifact["sha256"],"physical_line_ranges":[[1,5]] if number==1 else [[6,10]],
            "decision":"admit","printed_attribution":"Leo Papa I","title":"Titulus "+str(number),"source_attribution_lines":[3,3] if number==1 else [8,8],
            "review_note":"Whole extent and both boundaries inspected.","reviewed_extent":"Entire selected raw extent and context; no image collation."}
        path=self.root/f"review-{number}.json"
        b.write(path,b.json_bytes({"schema":"triptych-bullarium-boundary-reviews/v1","reviews":[item]}))
        return path

    def test_constituent_pins_whole_container_without_copy(self):
        artifact,units=self.admission_fixture()
        review=self.review(artifact,units[0],1)
        b.admit(self.root,[review],"2026-10-26T04:00:00Z")
        manifest=json.loads((self.root/b.MANIFEST).read_text())
        document=manifest["documents"][0]
        self.assertEqual(document["sha256"],artifact["sha256"])
        self.assertEqual(document["text_path"],artifact["path"])
        segment=tomllib.loads((self.root/document["segment_path"]).read_text())
        self.assertEqual(segment["schema"],2)
        self.assertEqual(segment["physical_line_ranges"],[[1,5]])
        self.assertEqual(len(list((self.root/"src/sources/works").rglob("ocr.txt"))),1)

    def test_admissions_are_cumulative(self):
        artifact,units=self.admission_fixture()
        for i,unit in enumerate(units,1):
            b.admit(self.root,[self.review(artifact,unit,i)],"2026-10-26T04:00:00Z")
        self.assertEqual(len(json.loads((self.root/b.MANIFEST).read_text())["documents"]),2)

    def test_wrong_source_hash_cannot_be_admitted(self):
        artifact,units=self.admission_fixture()
        path=self.review(artifact,units[0],1)
        review=json.loads(path.read_text())
        review["reviews"][0]["artifact_sha256"]="0"*64
        b.write(path,b.json_bytes(review))
        with self.assertRaisesRegex(ValueError,"exact source"):
            b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        self.assertFalse(list((self.root/"src/sources/works").rglob("source-ocr.toml")))

    def test_literal_printed_attribution_controls_manifest(self):
        artifact,units=self.admission_fixture()
        path=self.review(artifact,units[0],1)
        data=json.loads(path.read_text())
        data["reviews"][0]["printed_attribution"]="Pope Leo I"
        b.write(path,b.json_bytes(data))
        b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        document=json.loads((self.root/b.MANIFEST).read_text())["documents"][0]
        self.assertEqual(document["pope"],"Leo Papa I")

    def test_withdrawn_extent_leaves_no_renderable_segment(self):
        artifact,units=self.admission_fixture()
        path=self.review(artifact,units[0],1)
        b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        data=json.loads(path.read_text())
        data["reviews"][0].update({"decision":"hold","review_note":"Substantive opening is omitted by the printing."})
        b.write(path,b.json_bytes(data))
        b.admit(self.root,[path],"2026-10-26T04:00:01Z")
        self.assertEqual(json.loads((self.root/b.MANIFEST).read_text())["documents"],[])
        self.assertFalse(list((self.root/"src/sources/works").rglob("source-ocr.toml")))

    def test_split_keeps_a_held_partial_child(self):
        artifact,units=self.admission_fixture(count=1)
        path=self.review(artifact,units[0],1)
        first=json.loads(path.read_text())["reviews"][0]
        second={**first,"physical_line_ranges":[[6,10]],"source_attribution_lines":[8,8],
            "decision":"hold","review_note":"Substantive continuation is absent from the source."}
        b.write(path,b.json_bytes({"schema":"triptych-bullarium-boundary-reviews/v1","reviews":[{
            "unit_id":units[0]["id"],"artifact_sha256":artifact["sha256"],"decision":"split",
            "review_note":"Two independently headed source units.","constituents":[first,second]}]}))
        b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        self.assertEqual(len(json.loads((self.root/b.MANIFEST).read_text())["documents"]),1)
        catalog=json.loads((self.root/b.CATALOG).read_text())
        self.assertEqual(len(catalog["units"]),3)
        self.assertEqual(catalog["units"][2]["status"],"specifically-held")

    def test_changed_source_bytes_are_not_admitted(self):
        artifact,units=self.admission_fixture()
        path=self.review(artifact,units[0],1)
        (self.root/artifact["path"]).write_bytes(b"changed source")
        with self.assertRaisesRegex(ValueError,"source bytes changed"):
            b.admit(self.root,[path],"2026-10-26T04:00:00Z")


if __name__=="__main__":
    unittest.main()
