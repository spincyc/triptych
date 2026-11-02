"""The October successor admits only its code-pinned finite assessment."""
import copy
from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile
import tomllib
import types
import unittest
from unittest.mock import patch
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_finite_latin_20261029 as F
import _proper_qualified_latin as Q


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":")).encode()).hexdigest()


class FiniteLatinTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/roman-english-completion-20261029/finite-guard/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.body = "Alpha beta.\n"
        self.artifact = {
            "record_type": "artifact", "id": "artifact.finite.fixture.projection",
            "edition_id": "edition.finite.fixture", "rights_status": "project-created",
            "rights_basis": "Synthetic finite guard test: " + F.METHOD_ID,
            "sha256": sha256(self.body.encode()).hexdigest(),
            "path": "src/sources/finite-fixture/latin.txt", "storage": "tracked",
            "projected_from": ["artifact.finite.fixture.historical", "artifact.finite.fixture.target"],
        }
        self.passage = {
            "record_type": "passage", "id": "passage.finite.fixture.projection",
            "edition_id": "edition.finite.fixture", "artifact_id": self.artifact["id"],
            "artifact_sha256": self.artifact["sha256"], "language": "la",
            "physical_line_ranges": [[1, 1]],
        }
        self.records = {
            self.artifact["id"]: self.artifact, self.passage["id"]: self.passage,
            "artifact.finite.fixture.historical": {
                "record_type": "artifact", "rights_status": "public-domain",
                "storage": "tracked", "sha256": "a" * 64,
            },
            "artifact.finite.fixture.target": {
                "record_type": "artifact", "rights_status": "unresolved",
                "storage": "remote", "sha256": "b" * 64,
            },
            "passage.finite.fixture.target": {
                "record_type": "passage", "artifact_id": "artifact.finite.fixture.target",
                "artifact_sha256": "b" * 64, "language": "la",
                "artifact_page_ranges": [[1, 1]],
            },
        }
        self.row = {
            "mass": "finite-fixture", "form": "", "proper": "Collect",
            "course": "", "cycle": "", "occurrence": 1,
            "text_sha256": self.artifact["sha256"], "provenance_status": "collated",
            "source_id": self.passage["id"],
            "verification_source_id": "passage.finite.fixture.target",
            "publication_status": "permitted", "publication_basis": F.BASIS,
            "publication_source_ids": [self.artifact["id"], *self.artifact["projected_from"]],
            "publication_authority": F.METHOD_ID,
            "surfaces": ["web", "download", "print", "cli", "corpus-data", "public-git"],
        }
        self.inherited = dict(
            self.row, publication_status="unresolved", publication_basis="unresolved",
            surfaces=[], note="Provenance inherited from roman-1962; target-recension attestation for roman-pre-1955 is not established.")
        self.scope = {
            "key": [self.row[field] for field in F.KEY_FIELDS],
            "row_sha256": digest(self.row), "inherited_row_sha256": digest(self.inherited),
            "body_sha256": self.row["text_sha256"], "source_id": self.row["source_id"],
            "artifact_payload_sha256": self.artifact["sha256"],
            "artifact_id": self.artifact["id"],
            "verification_source_id": self.row["verification_source_id"],
            "publication_source_ids": self.row["publication_source_ids"],
            "projected_from": self.artifact["projected_from"],
            "physical_line_ranges": self.passage["physical_line_ranges"],
            "record_sha256": {name: digest(value) for name, value in self.records.items()},
            "public_notice": "Synthetic bounded assessment; no general clearance.",
        }
        self.authority = {
            "schema": "triptych-finite-latin-authority/v1", "state": "adopted",
            "method_id": F.METHOD_ID, "scopes": [self.scope],
            "prior_routes": {"row_sha256": [], "artifacts": [], "readings": []},
        }
        payload = json.dumps(self.authority, sort_keys=True).encode()
        path = self.root / F.ADOPTION_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
        carrier = self.root / self.artifact["path"]
        carrier.parent.mkdir(parents=True, exist_ok=True)
        carrier.write_text(self.body)
        self.pins = patch.multiple(F, TRUSTED_ROOT=self.root,
                                   ADOPTION_SHA256=sha256(payload).hexdigest(),
                                   RECOGNITION=F.recognition_from_scopes([self.scope]),
                                   PRIOR_ROUTES=copy.deepcopy(self.authority["prior_routes"]))
        self.pins.start()
        F._scopes.cache_clear()
        self.addCleanup(self.pins.stop)
        self.addCleanup(F._scopes.cache_clear)

    def seal_prior_routes(self, routes):
        self.authority["prior_routes"] = copy.deepcopy(routes)
        payload = json.dumps(self.authority, sort_keys=True).encode()
        (self.root / F.ADOPTION_PATH).write_bytes(payload)
        F.PRIOR_ROUTES = copy.deepcopy(routes)
        F.ADOPTION_SHA256 = sha256(payload).hexdigest()
        F._scopes.cache_clear()

    def reader(self):
        loader = SourceFileLoader("finite_guard_counterexample_reader", str(ROOT / "tools/source-reader"))
        spec = spec_from_loader(loader.name, loader)
        reader = module_from_spec(spec)
        sys.modules[spec.name] = reader
        loader.exec_module(reader)
        return reader

    def copied_reading(self, *, wrapper=False):
        artifact = dict(self.artifact, id="artifact.unknown.copy",
                        rights_basis="Original editorial carrier",
                        media_type="text/plain; charset=utf-8")
        passage = dict(self.passage, id="passage.unknown.copy",
                       artifact_id=artifact["id"])
        if wrapper:
            payload = "Prefix.\n" + self.body + "Suffix.\n"
            artifact.update(sha256=sha256(payload.encode()).hexdigest(),
                            path="src/sources/finite-fixture/wrapped.txt")
            (self.root / artifact["path"]).write_text(payload)
            passage.update(artifact_sha256=artifact["sha256"], physical_line_ranges=[[2, 2]])
        return artifact, passage

    def test_exact_scope_reaches_every_dispatcher(self):
        self.assertEqual(Q.row_problems(self.row), [])
        self.assertEqual(Q.source_problems(self.row, self.records), [])
        self.assertEqual(Q.authority_problems(self.root, row=self.row), [])
        self.assertEqual(Q.artifact_problems(self.root, self.artifact, sources=self.records), [])
        self.assertEqual(Q.reading_problems(
            self.root, self.passage, self.artifact, sources=self.records,
            text=self.body.removesuffix("\n")), [])
        state = {"text_sha256": self.row["text_sha256"],
                 "provenance": {"source_id": self.row["source_id"]}}
        self.assertEqual(Q.public_scope(state)["notice"], self.scope["public_notice"])

    def test_changed_owner_body_proof_basis_and_surface_are_refused(self):
        changes = {
            "mass": "another-owner", "form": "another-form", "proper": "Secret",
            "course": "cycles", "cycle": "A", "occurrence": 2,
            "text_sha256": "0" * 64, "source_id": "passage.unadopted",
            "verification_source_id": "passage.other.target",
            "publication_basis": "public-domain", "publication_status": "unresolved",
            "publication_authority": "another assessment", "surfaces": ["web"],
            "publication_source_ids": [self.artifact["id"]],
        }
        for field, value in changes.items():
            with self.subTest(field=field):
                changed = dict(self.row, **{field: value})
                self.assertTrue(Q.row_problems(changed))
                self.assertTrue(Q.source_problems(changed, self.records))
        self.assertTrue(Q.row_problems(dict(self.row, invented_field=True)))

    def test_no_authority_file_or_unadopted_file_grants_nothing(self):
        authority = self.root / F.ADOPTION_PATH
        authority.unlink()
        self.assertTrue(Q.authority_problems(self.root, row=self.row))
        self.assertTrue(Q.reading_problems(
            self.root, self.passage, self.artifact, sources=self.records, text="Alpha beta."))
        pending = dict(self.authority, state="pending")
        payload = json.dumps(pending, sort_keys=True).encode()
        authority.write_bytes(payload)
        with patch.object(F, "ADOPTION_SHA256", sha256(payload).hexdigest()):
            F._scopes.cache_clear()
            self.assertEqual(F._scopes(), ())
            self.assertTrue(Q.row_problems(self.row))
            self.assertTrue(Q.authority_problems(self.root, row=self.row))

    def test_changed_controller_or_rights_boundary_is_refused(self):
        for name, record in self.records.items():
            for field, value in [("sha256", "0" * 64), ("rights_status", "permission"),
                                 ("artifact_id", "artifact.another.controller")]:
                with self.subTest(source=name, field=field):
                    changed = copy.deepcopy(self.records)
                    changed[name][field] = value
                    self.assertTrue(Q.source_problems(self.row, changed))
                    self.assertTrue(Q.artifact_problems(self.root, self.artifact, sources=changed))
        self.assertTrue(Q.artifact_problems(self.root, self.artifact))

    def test_carrier_and_selected_text_are_both_bound(self):
        for change in [{"rights_basis": "wholly original"}, {"id": "artifact.other"},
                       {"edition_id": "edition.other"}, {"sha256": "0" * 64},
                       {"projected_from": ["artifact.other"]}, {"path": "../outside"}]:
            with self.subTest(change=change):
                self.assertTrue(Q.artifact_problems(
                    self.root, dict(self.artifact, **change), sources=self.records))
        for change in [{"physical_line_ranges": [[1, 2]]}, {"text": "another body"},
                       {"language": "en"}, {"id": "passage.other"},
                       {"artifact_id": "artifact.other"}, {"edition_id": "edition.other"}]:
            with self.subTest(change=change):
                self.assertTrue(Q.reading_problems(
                    self.root, dict(self.passage, **change), self.artifact,
                    sources=self.records, text="Alpha beta."))
        for text in ["Alpha", "Alpha beta.\n", "another whole body", None]:
            self.assertTrue(Q.reading_problems(
                self.root, self.passage, self.artifact, sources=self.records, text=text))
        (self.root / self.artifact["path"]).write_text("another body\n")
        self.assertTrue(Q.artifact_problems(self.root, self.artifact, sources=self.records))

    def test_inherited_permission_reset_is_not_a_new_admission(self):
        self.assertTrue(Q.inherited_row_exact(self.inherited))
        self.assertTrue(Q.row_problems(self.inherited))
        self.assertEqual(Q.source_problems(
            self.inherited, self.records, effective_calendar="roman-pre-1955"), [])
        self.assertTrue(Q.source_problems(
            self.inherited, self.records, effective_calendar="postconciliar"))
        for calendar in ("roman-pre-1955", "postconciliar", "another-calendar"):
            self.assertTrue(Q.source_problems(
                self.row, self.records, effective_calendar=calendar))
        for change in [{"publication_status": "permitted"}, {"surfaces": ["web"]}]:
            self.assertTrue(Q.source_problems(
                dict(self.inherited, **change), self.records,
                effective_calendar="roman-pre-1955"))

    def test_shared_edition_is_not_itself_a_qualified_carrier(self):
        ordinary = {
            "id": "artifact.ordinary.public-domain", "edition_id": self.artifact["edition_id"],
            "rights_status": "project-created", "rights_basis": "Original editorial carrier",
        }
        self.assertFalse(F.claims_artifact(ordinary))
        self.assertEqual(Q.artifact_problems(self.root, ordinary), [])

    def test_malformed_and_unrecognised_claims_fail_closed(self):
        for value in [None, [], 1, "not a mapping"]:
            self.assertTrue(F.row_problems(value))
        for change in [{"mass": {}}, {"publication_source_ids": [{}]},
                       {"publication_source_ids": 42}]:
            self.assertTrue(Q.row_problems(dict(self.row, **change)))
        self.assertTrue(Q.row_problems({"publication_basis": F.BASIS,
                                       "publication_authority": F.METHOD_ID}))

    def test_unknown_copied_row_cannot_strip_all_markers(self):
        copied = dict(self.row, mass="another-owner", source_id="passage.independent.copy",
                      verification_source_id="passage.independent.target",
                      publication_basis="public-domain",
                      publication_source_ids=["artifact.independent.public-domain"],
                      publication_authority="Independent public-domain control")
        self.assertTrue(Q.row_problems(copied))

    def test_unknown_copied_carrier_is_refused_before_reading(self):
        artifact, passage = self.copied_reading()
        self.assertTrue(Q.artifact_problems(self.root, artifact, sources=self.records))
        self.assertTrue(Q.reading_problems(self.root, passage, artifact,
                                         sources=self.records, text=self.body[:-1]))
        library = types.SimpleNamespace(root=self.root, records={
            artifact["id"]: types.SimpleNamespace(data=artifact)})
        result = self.reader().reading_of(library, passage)
        self.assertFalse(result["readable"])
        self.assertNotIn("text", result)

    def test_unknown_wrapper_cannot_emit_selected_finite_body(self):
        artifact, passage = self.copied_reading(wrapper=True)
        self.assertTrue(Q.reading_problems(self.root, passage, artifact,
                                         sources=self.records, text=self.body[:-1]))
        library = types.SimpleNamespace(root=self.root, records={
            artifact["id"]: types.SimpleNamespace(data=artifact)})
        result = self.reader().reading_of(library, passage)
        self.assertFalse(result["readable"])
        self.assertNotIn("text", result)

    def test_copied_body_recognition_survives_removed_authority_and_empty_cache(self):
        artifact, passage = self.copied_reading(wrapper=True)
        (self.root / F.ADOPTION_PATH).unlink()
        F._scopes.cache_clear()
        self.assertEqual(F._scopes(), ())
        self.assertTrue(Q.reading_problems(self.root, passage, artifact,
                                         sources=self.records, text=self.body[:-1]))
        copied, _ = self.copied_reading()
        self.assertTrue(Q.artifact_problems(self.root, copied, sources=self.records))

    def test_exact_old_rows_and_inheritance_keep_their_original_authority(self):
        table = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text())
        rows = [{**table["defaults"], **row} for row in table["entries"]
                if tuple(row.get(field, table["defaults"].get(field))
                         for field in Q.KEY_FIELDS) in Q.ROW_SHA256]
        wanted = (set(Q.CONTROLLER_SHA256) | set(Q.PARENT_FIELDS)
                  | {one["verification_source_id"] for one in Q.SCOPES})
        namespaces = {(one.split(".")[1], one.split(".")[2]) for one in wanted}
        sources = {}
        for namespace, work in namespaces:
            for path in (ROOT / "src/sources/works" / namespace / work).rglob("*.toml"):
                record = tomllib.loads(path.read_text())
                if record.get("id") in wanted:
                    sources[record["id"]] = record
        self.assertEqual(set(sources), wanted)
        for row in rows:
            inherited = dict(row, publication_status="unresolved", publication_basis="unresolved",
                             surfaces=[], note="Provenance inherited from roman-1962; target-recension attestation for roman-pre-1955 is not established.")
            colliding = dict(self.scope, body_sha256=row["text_sha256"])
            with self.subTest(owner=row["mass"]), patch.object(F, "_scopes", return_value=(colliding,)):
                self.assertEqual(Q.row_problems(row), [])
                self.assertEqual(Q.source_problems(row, sources), [])
                self.assertEqual(Q.authority_problems(ROOT, row=row), [])
                self.assertTrue(Q.inherited_row_exact(inherited))
                self.assertEqual(Q.source_problems(inherited, sources,
                                                   effective_calendar="roman-pre-1955"), [])

    def test_independent_prior_public_domain_row_needs_exact_root_seal(self):
        table = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml").read_text())
        prior = next({**table["defaults"], **row} for row in table["entries"]
                     if row.get("publication_basis") == "public-domain"
                     and row.get("publication_status") == "permitted")
        colliding = dict(self.scope, body_sha256=prior["text_sha256"])
        with patch.object(F, "_scopes", return_value=(colliding,)):
            self.assertTrue(Q.row_problems(prior))
        self.seal_prior_routes({"row_sha256": [digest(prior)], "artifacts": [], "readings": []})
        with patch.object(F, "_scopes", return_value=(colliding,)):
            self.assertEqual(Q.row_problems(prior), [])
            self.assertTrue(Q.row_problems(dict(prior, mass="copied-prior-owner")))

    def test_independent_prior_reading_binds_record_payload_passage_and_body(self):
        artifact, passage = self.copied_reading()
        artifact.update(id="artifact.prior.public-domain", rights_status="public-domain",
                        rights_basis="Independently proved historical source",
                        path="src/sources/finite-fixture/prior.txt")
        (self.root / artifact["path"]).write_text(self.body)
        passage.update(id="passage.prior.body", artifact_id=artifact["id"])
        self.seal_prior_routes({"row_sha256": [], "artifacts": [{
            "artifact_record_sha256": digest(artifact), "payload_sha256": artifact["sha256"]}],
            "readings": [{"artifact_record_sha256": digest(artifact),
                          "passage_record_sha256": digest(passage),
                          "body_sha256": sha256(self.body.encode()).hexdigest()}]})
        self.assertEqual(Q.artifact_problems(self.root, artifact), [])
        self.assertEqual(Q.reading_problems(self.root, passage, artifact, text=self.body[:-1]), [])
        self.assertTrue(Q.reading_problems(self.root, dict(passage, id="passage.copy"),
                                         artifact, text=self.body[:-1]))
        self.assertTrue(Q.reading_problems(self.root, passage, artifact, text="another body"))
        self.assertTrue(Q.artifact_problems(self.root, dict(artifact, rights_status="project-created")))
        (self.root / artifact["path"]).write_text("changed prior payload\n")
        self.assertTrue(Q.artifact_problems(self.root, artifact))

    def test_cache_changes_when_authority_or_helper_changes(self):
        before = Q.cache_fingerprint(self.root)
        (self.root / F.ADOPTION_PATH).write_text("changed adoption")
        self.assertNotEqual(before, Q.cache_fingerprint(self.root))
        helper = self.root / "helper.py"
        helper.write_bytes(Path(F.__file__).read_bytes())
        with patch.object(F, "__file__", str(helper)):
            before = Q.cache_fingerprint(self.root)
            helper.write_text(helper.read_text() + "\n# changed dependency\n")
            self.assertNotEqual(before, Q.cache_fingerprint(self.root))

    def test_original_two_scope_constants_and_default_authority_are_preserved(self):
        names = ["ROW_SHA256", "CONTROLLER_SHA256", "ARTIFACT_SHA256", "PARENT_FIELDS",
                 "SCOPES", "INHERITED_ROW_SHA256"]
        self.assertEqual(Q._digest({name: str(getattr(Q, name)) for name in names}),
                         "062fe30a78347a6b0fde731a34815dde501c2c0112ada9ab17e470a3d3eaa223")
        self.assertEqual(Q.authority_problems(ROOT), [])
        for scope in Q.SCOPES:
            state = {"text_sha256": scope["body_sha256"],
                     "provenance": {"source_id": scope["source_id"]}}
            self.assertIn("theological-redaction originality objection remains",
                          Q.public_scope(state)["notice"])


if __name__ == "__main__":
    unittest.main()
