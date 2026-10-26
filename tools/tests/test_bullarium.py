"""Bullarium source bounds, geometry warnings and truthful constituent ownership."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

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

    def test_registered_withdrawal_requires_pinned_metadata_and_preserves_sources(self):
        artifact,units=self.admission_fixture()
        path=self.review(artifact,units[0],1)
        b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        frozen_manifest=(self.root/b.MANIFEST).read_bytes()
        sources={p:p.read_bytes() for p in (self.root/"src/sources/works").rglob("*.toml")}
        data=json.loads(path.read_text())
        data["reviews"][0].update({"decision":"hold","review_note":"Substantive opening is omitted by the printing."})
        b.write(path,b.json_bytes(data))
        with self.assertRaisesRegex(ValueError,"PDF-pinned withdrawal metadata"):
            b.admit(self.root,[path],"2026-10-26T04:00:01Z")
        self.assertEqual((self.root/b.MANIFEST).read_bytes(),frozen_manifest)
        self.assertEqual(sources,{p:p.read_bytes() for p in (self.root/"src/sources/works").rglob("*.toml")})

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

    def test_configured_adapters_preserve_global_root_and_arguments(self):
        for verb,module in (("series","_bullarium_series"),("corrections","_bullarium_corrections"),("geometry","_bullarium_geometry")):
            with self.subTest(verb=verb),patch(module+".main",return_value=7) as adapter:
                self.assertEqual(b.main(["--root",str(self.root),verb,"--help"],examples={}),7)
                adapter.assert_called_once_with(["--root",str(self.root),"--help"],examples={})

    def test_non_latin_selection_has_truthful_edition_language_and_key(self):
        artifact,units=self.admission_fixture()
        path=self.review(artifact,units[0],1)
        b.admit(self.root,[path],"2026-10-26T04:00:00Z",reader_notes={units[0]["id"]:{"language":"mul","language_label":"Latin and Italian","component_languages":["la","it"]}})
        document=json.loads((self.root/b.MANIFEST).read_text())["documents"][0]
        edition=tomllib.loads((self.root/document["segment_path"]).parents[1].joinpath("edition.toml").read_text())
        self.assertEqual((document["language"],edition["language"]),("mul","mul"))
        self.assertIn("1857-turin-multilingual",edition["id"])

    def source_order_fixture(self,foreign_parent=False):
        artifact,units=self.admission_fixture(count=1)
        payload=b"Leo Papa I\nTitulus\nVerba integra.\nData Romae.\n"
        folder=self.root/Path(artifact["path"]).parent.parent/"coordinate-order"
        b.write(folder/"ocr.txt",payload)
        derived={**artifact,"id":"artifact.example.coordinate-order","path":str((folder/"ocr.txt").relative_to(self.root)),
            "sha256":b.sha(payload),"byte_size":len(payload),"artifact_type":"coordinate-reading-order-ocr",
            "derived_from":"artifact.foreign" if foreign_parent else artifact["id"]}
        b.record(folder/"artifact.toml",derived)
        catalog=json.loads((self.root/b.CATALOG).read_text())
        catalog["units"][0]["physical_line_ranges"]=[[1,5]]
        catalog["volumes"][0]["container"]["artifacts"]["coordinate-order"]={"id":derived["id"],"sha256":derived["sha256"],"manifest":str((folder/"artifact.toml").relative_to(self.root))}
        b.write(self.root/b.CATALOG,b.json_bytes(catalog))
        path=self.review(artifact,units[0],1)
        child=json.loads(path.read_text())["reviews"][0]
        child.update(source_artifact_id=derived["id"],artifact_sha256=derived["sha256"],physical_line_ranges=[[1,4]],source_attribution_lines=[1,1])
        b.write(path,b.json_bytes({"schema":"triptych-bullarium-boundary-reviews/v1","reviews":[{
            "unit_id":units[0]["id"],"artifact_sha256":artifact["sha256"],"decision":"split",
            "review_note":"The raw candidate is reconstructed through a separately identified checked reading-order controller.","constituents":[child]}]}))
        return path,derived

    def test_source_order_child_uses_registered_derivative_and_preserves_raw_parent(self):
        path,derived=self.source_order_fixture()
        b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        d=json.loads((self.root/b.MANIFEST).read_text())["documents"][0]
        self.assertEqual((d["artifact_id"],d["sha256"]),(derived["id"],derived["sha256"]))
        self.assertIn("Source-derived reading-order LF lines",d["source_note"])
        catalog=json.loads((self.root/b.CATALOG).read_text())
        self.assertEqual(catalog["units"][1]["source_order_parent"]["artifact_id"],"artifact.example.ocr")
        self.assertEqual(catalog["units"][0]["artifact_id"],"artifact.example.ocr")

    def test_source_order_child_rejects_foreign_parent(self):
        path,_=self.source_order_fixture(foreign_parent=True)
        with self.assertRaisesRegex(ValueError,"exact raw parent"):
            b.admit(self.root,[path],"2026-10-26T04:00:00Z")

    def test_source_order_child_rejects_changed_derivative_bytes(self):
        path,derived=self.source_order_fixture()
        (self.root/derived["path"]).write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError,"exact source bytes changed"):
            b.admit(self.root,[path],"2026-10-26T04:00:00Z")

    def test_identified_discovery_is_counted_separately_from_split_children(self):
        artifact,units=self.admission_fixture(count=1)
        path=self.review(artifact,units[0],2)
        review=json.loads(path.read_text())
        review["reviews"][0].update(unit_id="bullarium.volume-01.identified-extra",parent_unit_id=units[0]["id"])
        b.write(path,b.json_bytes(review))
        result=b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        self.assertEqual((result["additional_source_units"],result["additional_split_constituents"],result["identified_additional_source_units"]),(1,0,1))

    def test_cumulative_manifest_preserves_row_revision_and_exact_prior_input(self):
        artifact,units=self.admission_fixture()
        first=self.review(artifact,units[0],1)
        second=self.review(artifact,units[1],2)
        b.admit(self.root,[first],"2026-10-26T04:00:00Z")
        frozen=(self.root/b.MANIFEST).read_bytes()
        b.admit(self.root,[second],"2026-10-26T05:00:00Z")
        manifest=json.loads((self.root/b.MANIFEST).read_text())
        self.assertEqual([d["revision"] for d in manifest["documents"]],["2026-10-26T04:00:00Z","2026-10-26T05:00:00Z"])
        digest=b.sha(frozen)
        self.assertEqual((self.root/".scratch/bullarium_reconstruction/manifest-history"/(digest+".json")).read_bytes(),frozen)
        self.assertEqual(manifest["input_history"][0]["sha256"],digest)
        current=(self.root/b.MANIFEST).read_bytes()
        b.admit(self.root,[second],"2026-10-26T05:00:00Z")
        self.assertEqual((self.root/b.MANIFEST).read_bytes(),current)

    def test_known_source_order_hold_cannot_be_lifted_by_reader_note(self):
        artifact,units=self.admission_fixture(count=1)
        catalog=json.loads((self.root/b.CATALOG).read_text())
        catalog["units"][0]["active_reader_status"]="source-order-hold"
        b.write(self.root/b.CATALOG,b.json_bytes(catalog))
        path=self.review(artifact,units[0],1)
        with self.assertRaisesRegex(ValueError,"new source/selection identity"):
            b.admit(self.root,[path],"2026-10-26T04:00:00Z",reader_notes={units[0]["id"]:{"reader_source_note":"A marginal caption is retained."}})

    def test_new_source_order_child_does_not_inherit_prior_reader_hold(self):
        path,_=self.source_order_fixture()
        catalog=json.loads((self.root/b.CATALOG).read_text())
        catalog["units"][0].update(active_reader_status="source-order-hold",reader_withdrawal={"document_id":"prior-reader"})
        b.write(self.root/b.CATALOG,b.json_bytes(catalog))
        b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        child=json.loads((self.root/b.CATALOG).read_text())["units"][1]
        self.assertNotIn("active_reader_status",child)
        self.assertNotIn("reader_withdrawal",child)

    def test_repaired_selection_reuses_work_and_preserves_withdrawn_predecessor(self):
        order_path,derived=self.source_order_fixture()
        child=json.loads(order_path.read_text())["reviews"][0]["constituents"][0]
        catalog=json.loads((self.root/b.CATALOG).read_text())
        parent=catalog["units"][0]
        raw=tomllib.loads((self.root/catalog["volumes"][0]["container"]["artifacts"]["ocr"]["manifest"]).read_text())
        original=self.review(raw,parent,1)
        b.admit(self.root,[original],"2026-10-26T03:00:00Z")
        catalog=json.loads((self.root/b.CATALOG).read_text())
        prior=catalog["units"][0]
        old_segment=(self.root/prior["segment_path"]).read_bytes()
        work_path=(self.root/prior["segment_path"]).parents[3]/"work.toml"
        old_work=work_path.read_bytes()
        prior.update(status="specifically-held",active_reader_status="source-order-hold")
        prior["review"].update(decision="hold",review_note="Known synthetic source-order fixture.")
        b.write(self.root/b.CATALOG,b.json_bytes(catalog))
        child.update(unit_id=prior["id"]+".ordered-v2",parent_unit_id=prior["id"],
            canonical_work_id=prior["work_id"],identity_evidence={"existing_work_id":prior["work_id"],"basis":"Same synthetic source act and new checked controller."},
            reading_selection_variant_of=prior["id"])
        path=self.root/"new-reading.json"
        b.write(path,b.json_bytes({"schema":"triptych-bullarium-boundary-reviews/v1","reviews":[child]}))
        result=b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        current=next(u for u in json.loads((self.root/b.CATALOG).read_text())["units"] if u["id"]==child["unit_id"])
        self.assertEqual(current["work_id"],prior["work_id"])
        self.assertNotEqual(current["edition_id"],prior["edition_id"])
        self.assertEqual(current["reading_selection_variant_of"],prior["id"])
        self.assertEqual((self.root/prior["segment_path"]).read_bytes(),old_segment)
        self.assertEqual(work_path.read_bytes(),old_work)
        self.assertEqual((result["additional_reading_selections"],result["identified_additional_source_units"]),(1,0))

    def test_discovered_child_does_not_inherit_other_acts_protocol_or_date_leads(self):
        artifact,units=self.admission_fixture(count=1)
        catalog=json.loads((self.root/b.CATALOG).read_text())
        catalog["units"][0].update(date_raw=[{"line":2,"raw":"First lead"},{"line":9,"raw":"Second lead"}],protocol={"line":3,"raw":"First protocol"})
        b.write(self.root/b.CATALOG,b.json_bytes(catalog))
        path=self.review(artifact,units[0],2)
        review=json.loads(path.read_text());review["reviews"][0].update(unit_id="bullarium.volume-01.identified-extra",parent_unit_id=units[0]["id"])
        b.write(path,b.json_bytes(review));b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        child=next(u for u in json.loads((self.root/b.CATALOG).read_text())["units"] if u["id"].endswith("identified-extra"))
        self.assertEqual(child["date_raw"],[{"line":9,"raw":"Second lead"}])
        self.assertNotIn("protocol",child)
        self.assertEqual(child["reviewed_protocol"]["physical_line_ranges"],[[8,8]])

    def test_discovery_replay_cannot_replace_registered_constituent_inputs(self):
        artifact,units=self.admission_fixture(count=1)
        path=self.review(artifact,units[0],1)
        b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        frozen=(self.root/b.MANIFEST).read_bytes()
        with self.assertRaisesRegex(ValueError,"registered constituent witnesses are immutable"):
            b.reconstruct(self.root,[1],"2026-10-26T05:00:00Z")
        self.assertEqual((self.root/b.MANIFEST).read_bytes(),frozen)

    def test_split_replay_cannot_overwrite_a_registered_childs_source_bounds(self):
        path,_=self.source_order_fixture()
        b.admit(self.root,[path],"2026-10-26T04:00:00Z")
        frozen=(self.root/b.MANIFEST).read_bytes()
        review=json.loads(path.read_text());review["reviews"][0]["constituents"][0]["physical_line_ranges"]=[[1,3]]
        b.write(path,b.json_bytes(review))
        with self.assertRaisesRegex(ValueError,"immutable registered source pins"):
            b.admit(self.root,[path],"2026-10-26T05:00:00Z")
        self.assertEqual((self.root/b.MANIFEST).read_bytes(),frozen)


if __name__=="__main__":
    unittest.main()
