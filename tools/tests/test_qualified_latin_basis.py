"""Finite qualified rights basis rejects changed authority and scope."""
import copy
import importlib.util
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest
import types
from unittest.mock import patch
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_qualified_latin as Q


class QualifiedLatinTests(unittest.TestCase):
    def test_received_owners_and_meaningful_mutations(self):
        sidecar = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text())
        rows = [{**sidecar["defaults"], **row} for row in sidecar["entries"]
                if row.get("publication_basis") == Q.BASIS]
        self.assertEqual(len(rows), 2)
        self.assertEqual(Q.authority_problems(ROOT), [])
        for row in rows:
            self.assertEqual(Q.row_problems(row), [])
            for field, value in [("text_sha256", "0" * 64),
                                 ("source_id", "passage.another.source"),
                                 ("publication_authority", "forged"),
                                 ("publication_evidence", "forged"),
                                 ("publication_basis", "public-domain"),
                                 ("publication_basis", "project-created"),
                                 ("surfaces", ["web"]),
                                 ("provenance_confidence", "low"),
                                 ("notice", "unqualified public domain")]:
                with self.subTest(owner=row["mass"], mutation=field):
                    changed=copy.deepcopy(row)
                    changed[field]=value
                    self.assertTrue(Q.row_problems(changed))

    def test_unknown_owner_and_three_Albert_owners_are_refused(self):
        for mass, proper in [("another-owner", "Collect"), *[
                ("s-alberti-magni-episcopi-confessoris-ecclesiae", proper)
                for proper in ("Collect", "Secret", "Postcommunion")]]:
            with self.subTest(mass=mass, proper=proper):
                row = dict(zip(Q.KEY_FIELDS, [mass, "", proper, "", "", 1]))
                row["publication_basis"] = Q.BASIS
                self.assertTrue(Q.row_problems(row))

    def test_missing_or_forged_authority_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(len(Q.authority_problems(tmp)), 2)
            for relative in (Q.ADOPTION_PATH, Q.RIGHTS_PATH):
                path=Path(tmp)/relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("forged approval")
            self.assertEqual(len(Q.authority_problems(tmp)), 2)

    def test_project_created_carrier_cannot_invent_qualified_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(Q.artifact_problems(tmp, {
                "id": "artifact.project.forged", "edition_id": Q.EDITION_ID,
                "rights_status": "project-created", "rights_basis": Q.BASIS}))

    def test_malformed_qualified_rows_fail_as_diagnostics(self):
        for malformed in ({"mass": {}}, {"publication_source_ids": 42},
                          {"publication_source_ids": [{}]}):
            self.assertTrue(Q.row_problems({"publication_basis": Q.BASIS, **malformed}))

    def test_ordinary_project_created_artifacts_keep_existing_meaning(self):
        self.assertEqual(Q.artifact_problems(ROOT, {
            "edition_id":"edition.other", "rights_status":"project-created",
            "rights_basis":"original project prose"}), [])

    def test_exact_carriers_and_tampered_payload_are_distinguished(self):
        for path in (ROOT / "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/editions/2026-10-26-gregem-qualified/artifacts").glob("*/artifact.toml"):
            artifact=tomllib.loads(path.read_text())
            self.assertEqual(Q.artifact_problems(ROOT, artifact), [])
            parents=copy.deepcopy(Q.PARENT_FIELDS)
            self.assertEqual(Q.artifact_problems(ROOT, artifact, sources=parents), [])
            for parent_id in artifact["projected_from"]:
                for field, value in [("sha256", "0" * 64), ("rights_status", "permission")]:
                    changed=copy.deepcopy(parents)
                    changed[parent_id][field]=value
                    self.assertTrue(Q.artifact_problems(ROOT, artifact, sources=changed))
            relabeled=dict(artifact, rights_basis="wholly project authored", edition_id="edition.other")
            self.assertTrue(Q.artifact_problems(ROOT, relabeled))
            # Keep the authoritative metadata and authority exact while the
            # selected data root has a different payload. It must not read.
            with tempfile.TemporaryDirectory() as tmp:
                for relative in (Q.ADOPTION_PATH, Q.RIGHTS_PATH):
                    dest=Path(tmp)/relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes((ROOT/relative).read_bytes())
                payload=Path(tmp)/artifact["path"]
                payload.parent.mkdir(parents=True, exist_ok=True)
                payload.write_text("another prayer")
                self.assertTrue(Q.artifact_problems(tmp, artifact))



class QualifiedIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader=SourceFileLoader("qualified_integration_reader", str(ROOT/"tools/source-reader"))
        spec=spec_from_loader(loader.name, loader)
        cls.reader=module_from_spec(spec)
        sys.modules[spec.name]=cls.reader
        loader.exec_module(cls.reader)
        cls.library=cls.reader.source_library().load_library(ROOT, check_binding_fingerprints=False)
        if cls.library.errors:
            raise AssertionError(cls.library.errors)
        cls.sources={key:record.data for key,record in cls.library.records.items()}
        cls.calendar_root=ROOT/"src/sources/calendars"

    def test_three_calendars_and_exact_Bonn_three_are_conserved(self):
        import _proper_latin as L
        import _proper_target_overrides as target
        roman, problems=L.publication_records(self.calendar_root,"roman-1962",registered_sources=self.sources)
        self.assertEqual(problems, [])
        child, problems=L.publication_records(self.calendar_root,"roman-pre-1955",registered_sources=self.sources)
        self.assertEqual(problems, [])
        pc, problems=L.publication_records(self.calendar_root,"postconciliar",registered_sources=self.sources)
        self.assertEqual(problems, [])
        self.assertTrue(pc)
        self.assertEqual(len(child),len(roman))
        expected_overrides, problems=L.target_overrides(self.calendar_root,"roman-pre-1955",registered_sources=self.sources)
        self.assertEqual(problems, [])
        self.assertEqual(len(expected_overrides),3)
        bonn={L.LatinKey.from_mapping(row["provenance"]):dict(row["provenance"],_target_context=dict(target.CONTEXT)) for row in expected_overrides}
        self.assertEqual({k:r for k,r in child.items() if r.get("publication_status")=="permitted"},bonn)
        for key,parent in roman.items():
            expected=bonn.get(key) or dict(parent,publication_status="unresolved",publication_basis="unresolved",surfaces=[],
                note="Provenance inherited from roman-1962; target-recension attestation for roman-pre-1955 is not established.")
            self.assertEqual(child[key],expected)
        for scope in Q.SCOPES:
            key=L.LatinKey(*scope["key"])
            row=child[key]
            self.assertTrue(Q.inherited_row_exact(row))
            self.assertEqual(row["publication_status"],"unresolved")
            self.assertEqual(row["surfaces"],[])
            self.assertTrue(Q.row_problems(row))  # forbidden as a direct row
            self.assertEqual(Q.source_problems(row,self.sources,effective_calendar="roman-pre-1955"),[])
            self.assertTrue(Q.source_problems(row,self.sources,effective_calendar="postconciliar"))
            for change in [{"publication_status":"permitted"},{"publication_basis":Q.BASIS},{"surfaces":["cli"]}]:
                self.assertTrue(Q.source_problems(dict(row,**change),self.sources,effective_calendar="roman-pre-1955"))

    def test_inline_range_body_language_and_ID_tampering_never_read_in_either_mode(self):
        for strict in (False,True):
            library=self.reader.load(types.SimpleNamespace(strict=strict))
            for scope in Q.SCOPES:
                passage=copy.deepcopy(self.sources[scope["source_id"]])
                good=self.reader.reading_of(library,passage)
                self.assertTrue(good["readable"])
                self.assertEqual(__import__("hashlib").sha256((good["text"]+"\n").encode()).hexdigest(),scope["body_sha256"])
                mutations=[dict(passage,text="synthetic private negative control"),
                    dict(passage,text=good["text"][:20]),dict(passage,text=good["text"]),
                    dict(passage,physical_line_ranges=[[1,1]] if scope["physical_line_ranges"]!=[[1,1]] else [[1,2]]),
                    dict(passage,language="en"),dict(passage,id="passage.unknown"),
                    dict(passage,id="passage.albert.collect"),dict(passage,artifact_sha256="0"*64),
                    dict(passage,edition_id="edition.other"),
                    dict(passage,artifact_id="artifact.catholic-church.sacramentarium-veronense.feltoe-1896.internet-archive-pdf-3b991b13")]
                for mutation_index, changed in enumerate(mutations):
                    with self.subTest(strict=strict,owner=scope["key"],mutation=mutation_index):
                        result=self.reader.reading_of(library,changed)
                        self.assertFalse(result["readable"])
                        self.assertNotIn("text",result)

    def test_actual_resolved_content_is_checked_after_selection(self):
        # Simulate a content-selection defect without changing passage metadata,
        # artifact bytes or authority: the selected text must still be refused.
        for strict in (False,True):
            library=self.reader.load(types.SimpleNamespace(strict=strict))
            for scope in Q.SCOPES:
                passage=self.sources[scope["source_id"]]
                for lines in (["prefix only"],["synthetic whole private negative control"]*4):
                    with patch.object(self.reader,"_payload_lines",return_value=lines):
                        result=self.reader.reading_of(library,passage)
                        self.assertFalse(result["readable"])
                        self.assertNotIn("text",result)

    def test_root_authority_tamper_is_refused_in_both_modes(self):
        for strict in (False,True):
            library=self.reader.load(types.SimpleNamespace(strict=strict))
            with tempfile.TemporaryDirectory() as tmp:
                for relative in (Q.ADOPTION_PATH,Q.RIGHTS_PATH):
                    dest=Path(tmp)/relative;dest.parent.mkdir(parents=True,exist_ok=True)
                    dest.write_bytes((ROOT/relative).read_bytes())
                for scope in Q.SCOPES:
                    artifact=self.sources[scope["artifact_id"]]
                    dest=Path(tmp)/artifact["path"];dest.parent.mkdir(parents=True,exist_ok=True)
                    dest.write_bytes((ROOT/artifact["path"]).read_bytes())
                (Path(tmp)/Q.ADOPTION_PATH).write_text("forged root adoption")
                changed=copy.copy(library);changed.root=Path(tmp)
                for scope in Q.SCOPES:
                    result=self.reader.reading_of(changed,self.sources[scope["source_id"]])
                    self.assertFalse(result["readable"])
                    self.assertNotIn("text",result)

    def test_corpus_cache_rechecks_removed_authority_and_helper_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            for relative in (Q.ADOPTION_PATH,Q.RIGHTS_PATH):
                dest=root/relative;dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes((ROOT/relative).read_bytes())
            for scope in Q.SCOPES:
                artifact=self.sources[scope["artifact_id"]]
                dest=root/artifact["path"];dest.parent.mkdir(parents=True,exist_ok=True)
                dest.write_bytes((ROOT/artifact["path"]).read_bytes())
            library=copy.copy(self.library);library.root=root
            def qualified_readings(corpus):
                return [passage["reading"] for work in corpus for edition in work["editions"]
                        for passage in edition["passages"] if passage["id"] in {s["source_id"] for s in Q.SCOPES}]
            with patch.object(self.reader,"ROOT",root), patch.object(self.reader,"CORPUS_CACHE_FLOOR",0), \
                 patch.dict(__import__("os").environ,{"TRIPTYCH_CORPUS_CACHE":"1"}), \
                 patch.object(self.reader,"_corpus",wraps=self.reader._corpus) as derive:
                first=self.reader.corpus(library)
                self.assertTrue(all(r["readable"] for r in qualified_readings(first)))
                second=self.reader.corpus(library)
                self.assertEqual(first,second)
                self.assertEqual(derive.call_count,1)  # actual persistent hit
                (root/Q.ADOPTION_PATH).unlink()
                revoked=self.reader.corpus(library)
                self.assertEqual(derive.call_count,2)
                self.assertTrue(all(not r["readable"] and "text" not in r for r in qualified_readings(revoked)))
            helper=root/"helper.py";helper.write_bytes(Path(Q.__file__).read_bytes())
            with patch.object(Q,"__file__",str(helper)):
                before=Q.cache_fingerprint(root)
                helper.write_text(helper.read_text()+"\n# cache dependency change\n")
                self.assertNotEqual(before,Q.cache_fingerprint(root))


if __name__ == "__main__":
    unittest.main()
