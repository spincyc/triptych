"""Target-body admission is three exact Bonn witness owners, never inheritance.

Accepted receipts below are isolated implementation fixtures. They are not an
independent source acceptance of the real three-prayer proposal.
"""
from __future__ import annotations

import copy
import hashlib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars
import _proper_latin as latin
import _proper_target_overrides as target
import _missal_coverage as coverage


def dump(data):
    lines = []
    def table(value, prefix=""):
        for key, child in value.items():
            if not isinstance(child, dict) and not (isinstance(child, list) and child and isinstance(child[0], dict)):
                lines.append(key + " = " + json.dumps(child, ensure_ascii=False))
        for key, child in value.items():
            name = prefix + key
            if isinstance(child, dict):
                lines.extend(["", "[" + name + "]"]); table(child, name + ".")
            elif isinstance(child, list) and child and isinstance(child[0], dict):
                for one in child:
                    lines.extend(["", "[[" + name + "]]"]); table(one, name + ".")
    table(data)
    return "\n".join(lines) + "\n"


class TargetOverrideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calendar_root = ROOT / "src/sources/calendars"
        cls.document = _calendars.load_document(cls.calendar_root, target.CALENDAR)
        cls.registered, problems = latin._source_library_records(cls.calendar_root)
        if problems:
            raise AssertionError(problems)
        cls.sidecar = ROOT / "src/sources/inventories" / (target.CALENDAR + target.SUFFIX)
        cls.template = tomllib.loads(cls.sidecar.read_text())

    def setUp(self):
        self.room = tempfile.TemporaryDirectory()
        self.addCleanup(self.room.cleanup)
        self.root = Path(self.room.name)
        self.calendars = self.root / "src/sources/calendars"
        self.calendars.mkdir(parents=True)
        self.path = self.root / self.sidecar.relative_to(ROOT)
        self.path.parent.mkdir(parents=True)
        self.data = copy.deepcopy(self.template)
        self.sources = dict(self.registered)
        self.doc = copy.deepcopy(self.document)
        review = self.root / self.data["review"]["path"]
        review.parent.mkdir(parents=True)
        shutil.copy2(ROOT / self.data["review"]["path"], review)
        self.receipt = tomllib.loads(review.read_text())
        self.receipt.update(disposition="pending", independent=False, reviewer="")
        for row in self.data["entries"]:
            passage = self.sources[row["source_id"]]
            artifact = self.sources[passage["artifact_id"]]
            destination = self.root / artifact["path"]
            if not destination.exists():
                destination.parent.mkdir(parents=True)
                shutil.copy2(ROOT / artifact["path"], destination)
        self.save()

    def save(self):
        review = self.root / self.data["review"]["path"]
        review.write_text(dump(self.receipt))
        self.data["review"]["sha256"] = target.digest(review.read_bytes())
        self.path.write_text(dump(self.data))

    def accepted_fixture(self):
        self.receipt.update(disposition="accepted", independent=True,
                            reviewer="Synthetic implementation fixture; no actual source acceptance")
        self.save()

    def load(self, calendar=target.CALENDAR):
        return target.load(self.root, self.calendars, calendar, self.doc, self.sources,
                           row_problems=latin._row_problems,
                           source_problems=latin._source_record_problems)

    def refused(self):
        rows, errors = self.load()
        self.assertEqual(rows, [])
        self.assertTrue(errors)

    def test_pending_review_is_valid_and_releases_zero(self):
        rows, errors = self.load()
        self.assertEqual((rows, errors), ([], []))

    def test_three_only_change_body_and_keep_every_owner_and_english_field(self):
        self.accepted_fixture()
        rows, errors = self.load()
        self.assertFalse(errors, errors)
        self.assertEqual(len(rows), 3)
        changed = target.apply(self.doc, rows)
        before = list(latin.body_owners(self.doc))
        after = list(latin.body_owners(changed))
        self.assertEqual([key for key, _, _ in before], [key for key, _, _ in after])
        differences = [(old[0], old[1], new[1]) for old, new in zip(before, after) if old != new]
        self.assertEqual({key.proper for key, _, _ in differences}, {"Collect", "Secret", "Postcommunion"})
        self.assertEqual(len(differences), 3)
        self.assertEqual(self.doc, self.document)
        for row in rows:
            original = target.locate(self.doc, row)
            updated = next(proper for proper in _calendars.mass_index(changed)["pentecost"]["propers"]
                           if proper["name"] == row["proper"])
            self.assertEqual({key: value for key, value in original.items() if key != "text"},
                             {key: value for key, value in updated.items()
                              if key not in {"text", "_target_witness_context"}})

    def test_wrong_parent_body_is_refused(self):
        self.accepted_fixture()
        target.locate(self.doc, self.data["entries"][0])["text"] += " changed"
        self.refused()

    def test_replacement_hash_cannot_name_the_inherited_long_ending(self):
        self.accepted_fixture()
        self.data["entries"][0]["text_sha256"] = self.data["entries"][0]["base_text_sha256"]
        self.save(); self.refused()

    def test_mutated_payload_is_refused(self):
        self.accepted_fixture()
        passage = self.sources[self.data["entries"][0]["source_id"]]
        artifact = self.sources[passage["artifact_id"]]
        path = self.root / artifact["path"]
        path.write_bytes(path.read_bytes().replace(b"Dominum", b"Dominus", 1))
        self.refused()

    def test_wrong_occurrence_form_or_name_is_refused(self):
        for field, value in (("occurrence",2),("form_id","another"),("proper","Introit"),
                             ("course","cycles"),("cycle","A")):
            with self.subTest(field=field):
                original = self.data["entries"][0][field]
                self.data["entries"][0][field] = value
                self.save(); self.refused()
                self.data["entries"][0][field] = original

    def test_foreign_calendar_and_generic_1920_context_are_refused(self):
        self.data["calendar"] = "roman-1962"
        self.save(); self.refused()
        self.data["calendar"] = target.CALENDAR
        self.data["target_context"]["edition_id"] = "edition.catholic-church.missale-romanum.vatican-typica-1920"
        self.save(); self.refused()

    def test_other_source_horizon_and_civil_date_authority_are_refused(self):
        self.data["target_context"]["civil_date_authority"] = True
        self.save(); self.refused()

    def test_uncollated_target_passage_is_refused(self):
        self.accepted_fixture()
        identifier = self.data["entries"][0]["target_passage_id"]
        self.sources[identifier] = dict(self.sources[identifier], states=["cataloged", "acquired", "inspected"])
        self.refused()

    def test_uncollated_projection_passage_is_refused(self):
        self.accepted_fixture()
        identifier = self.data["entries"][0]["source_id"]
        self.sources[identifier] = dict(self.sources[identifier], states=["cataloged", "acquired"])
        self.refused()

    def test_wrong_body_language_is_refused(self):
        self.accepted_fixture()
        passage = self.sources[self.data["entries"][0]["source_id"]]
        identifier = passage["edition_id"]
        self.sources[identifier] = dict(self.sources[identifier], language="en")
        self.refused()

    def test_metadata_only_source_change_invalidates_the_attestation(self):
        self.accepted_fixture()
        identifier = self.data["entries"][0]["target_passage_id"]
        self.sources[identifier] = dict(self.sources[identifier], locus="Another prayer, another page")
        self.refused()

    def test_valid_scalar_derivative_ancestor_is_one_id_not_characters(self):
        row = self.data["entries"][0]
        passage = self.sources[row["source_id"]]
        artifact = self.sources[passage["artifact_id"]]
        identifier = "artifact.fixture.same-edition-derivative-input"
        self.sources[identifier] = {"record_type":"artifact", "id":identifier,
                                    "edition_id":artifact["edition_id"], "sha256":"0"*64}
        self.sources[artifact["id"]] = dict(artifact, derived_from=identifier)
        current = target.evidence_fingerprint(row, self.sources)
        self.assertEqual(len(current),64)
        self.assertNotEqual(current,row["evidence_sha256"])

    def test_wrong_target_artifact_is_refused(self):
        self.accepted_fixture()
        identifier = self.data["entries"][0]["target_passage_id"]
        self.sources[identifier] = dict(self.sources[identifier], artifact_id="artifact.other")
        self.refused()

    def test_stale_or_incomplete_receipt_cannot_admit_a_body(self):
        self.accepted_fixture()
        self.receipt["entries"] = self.receipt["entries"][:2]
        self.save(); self.refused()

    def test_review_is_independent_and_exactly_hash_pinned(self):
        self.accepted_fixture()
        self.receipt["independent"] = False
        self.save(); self.refused()
        self.receipt["independent"] = True
        self.save()
        review = self.root / self.data["review"]["path"]
        review.write_text(review.read_text() + "\n# changed\n")
        self.refused()

    def test_witness_wording_never_becomes_generic_exact_target(self):
        record = {"provenance":{"status":"collated", "relationship":"editorial-projection-exact-to-target"},
                  "publication":{"basis":"public-domain","status":"permitted"}, "withheld":False, "target_context":dict(target.PUBLIC_CONTEXT)}
        for inherited in (False, True):
            evidence = coverage.latin_evidence(record, inherited=inherited)
            self.assertEqual(evidence["relationship"], "unresolved")
            self.assertEqual(evidence["collation"], "collated")
        record["provenance"]["status"] = "identified"
        self.assertEqual(coverage.latin_evidence(record,inherited=True)["collation"],"uncollated")
        record["provenance"]["status"] = "collated"
        del record["target_context"]
        self.assertEqual(coverage.latin_evidence(record,inherited=True)["collation"],"uncollated")

    def test_cli_qualifies_latin_without_relabelling_english(self):
        loader = SourceFileLoader("pre55_target_cli_selection", str(ROOT / "tools/mass-propers"))
        spec = spec_from_loader(loader.name, loader)
        tool = module_from_spec(spec)
        sys.modules[spec.name] = tool
        loader.exec_module(tool)
        proper = {"name":"Collect", "source":"composed", "text":"Synthetic Latin fixture.",
                  "latin":{"withheld":False,"target_context":dict(target.PUBLIC_CONTEXT),
                           "provenance":{"status":"collated", "relationship":"editorial-projection-exact-to-target"},
                           "publication":{"status":"permitted", "basis":"public-domain"}},
                  "translations":[{"lang":"en","source_id":"fixture.english","text":"Synthetic English fixture.","source_label":"English witness"}]}
        selected = tool.select_texts(proper,"la")
        self.assertEqual(selected[0][0],"Synthetic Latin fixture.")
        self.assertIn("Bonn 2004",selected[0][1])
        self.assertIn("no civil-date-specific",selected[0][2])
        english = tool.select_texts(proper,"en")
        self.assertEqual(english,[("Synthetic English fixture.","English witness","")])


class PublicWitnessContextTests(unittest.TestCase):
    """Public context is a checked claim, never a private source-study tuple."""
    def setUp(self):
        self.key = latin.LatinKey("pentecost", "", "Collect", "", "", 1)
        self.text = "Synthetic exact prayer."
        self.row = {**self.key.as_dict(), "text_sha256": latin.text_sha256(self.text),
                    "provenance_status": "collated", "relationship": "editorial-projection-exact-to-target",
                    "publication_status": "permitted", "publication_basis": "public-domain",
                    "surfaces": sorted(latin.SURFACES), "_target_context": dict(target.CONTEXT)}

    def projected(self, row=None, key=None, text=None, wanted=latin.STRUCTURE_SURFACES):
        return latin.decision_for(key or self.key, self.text if text is None else text,
                                  {self.key: self.row if row is None else row}).projection(wanted)

    def test_only_three_public_fields_project_without_mutating_private_context(self):
        before = copy.deepcopy(self.row)
        public = self.projected()
        self.assertEqual(public["target_context"], target.PUBLIC_CONTEXT)
        self.assertEqual(set(public["target_context"]), {"scope", "label", "civil_date_authority"})
        self.assertEqual(self.row, before)
        self.assertNotIn(target.WITNESS_ARTIFACT, json.dumps(public))
        self.assertNotIn(target.WITNESS_EDITION, json.dumps(public))
        self.assertNotIn(target.WITNESS_HASH, json.dumps(public))

    def test_changed_private_context_cannot_emit_the_public_claim(self):
        for field, value in (("scope", "generic-recension"), ("label", "Another witness"),
                             ("artifact_id", "artifact.other"), ("artifact_sha256", "0" * 64),
                             ("civil_date_authority", True), ("civil_date_authority", 0),
                             ("unreviewed", "extra")):
            with self.subTest(field=field, value=value):
                row = copy.deepcopy(self.row); row["_target_context"][field] = value
                self.assertNotIn("target_context", self.projected(row))

    def test_stale_body_wrong_occurrence_or_unpermitted_surface_emits_no_context(self):
        for public in (
            self.projected(text=self.text + " changed"),
            self.projected(key=latin.LatinKey("pentecost", "", "Secret", "", "", 1)),
            self.projected(key=latin.LatinKey("pentecost", "", "Collect", "", "", 2)),
            self.projected(row={**self.row, "publication_status": "withheld"}),
            self.projected(row={**self.row, "surfaces": ["cli"]}),
        ):
            self.assertTrue(public["withheld"])
            self.assertNotIn("target_context", public)

    def test_public_shape_and_source_grade_are_closed(self):
        public = self.projected()
        self.assertTrue(coverage.is_witness_state_body(public))
        contexts = [dict(target.CONTEXT), {}, None,
                    {**target.PUBLIC_CONTEXT, "scope": "generic-recension"},
                    {**target.PUBLIC_CONTEXT, "label": ""},
                    {**target.PUBLIC_CONTEXT, "label": "Another witness"},
                    {**target.PUBLIC_CONTEXT, "civil_date_authority": True},
                    {**target.PUBLIC_CONTEXT, "civil_date_authority": 0},
                    {**target.PUBLIC_CONTEXT, "artifact_id": target.WITNESS_ARTIFACT}]
        for context in contexts:
            with self.subTest(context=context):
                self.assertFalse(coverage.is_witness_state_body({**public, "target_context": context}))
        for fields in ({"withheld": True},
                       {"publication": {"status": "withheld", "basis": "public-domain"}},
                       {"publication": {"status": "permitted", "basis": "unresolved"}},
                       {"provenance": {"status": "identified", "relationship": "editorial-projection-exact-to-target"}}):
            with self.subTest(fields=fields):
                self.assertFalse(coverage.is_witness_state_body({**public, **fields}))

    def test_public_context_never_attests_generic_target_wording(self):
        for inherited in (False, True):
            evidence = coverage.latin_evidence(self.projected(), inherited=inherited)
            self.assertEqual(evidence["relationship"], "unresolved")
            self.assertEqual(evidence["collation"], "collated")
        private = {**self.projected(), "target_context": dict(target.CONTEXT)}
        self.assertEqual(coverage.latin_evidence(private, inherited=True)["collation"], "uncollated")

    def load_cli(self):
        loader = SourceFileLoader("public_witness_context_cli", str(ROOT / "tools/mass-propers"))
        spec = spec_from_loader(loader.name, loader)
        tool = module_from_spec(spec); sys.modules[spec.name] = tool
        loader.exec_module(tool)
        return tool

    def test_raw_appointed_nested_and_withheld_payloads_drop_internal_marker(self):
        cli = self.load_cli()
        public = self.projected()
        proper = {"name": "Collect", "text": self.text, "latin": public,
                  "_target_witness_context": dict(target.CONTEXT)}
        held = latin.sanitize_proper(proper, self.key, {}, latin.STRUCTURE_SURFACES)
        self.assertIsNone(held["text"])
        self.assertIn("_target_witness_context", held)
        payload = {"mass": {"propers": [proper, held], "forms": [{"propers": [proper]}]},
                   "appointed": [proper, {"cycles": {"A": held}}]}
        original = copy.deepcopy(payload)
        rendered = cli.rights_safe_copy(payload)
        self.assertEqual(payload, original)
        self.assertNotIn("_target_witness_context", json.dumps(rendered))
        self.assertNotIn(target.WITNESS_ARTIFACT, json.dumps(rendered))
        self.assertEqual(rendered["appointed"][0]["latin"]["target_context"], target.PUBLIC_CONTEXT)
        self.assertTrue(rendered["mass"]["propers"][1]["latin"]["withheld"])

    def test_public_coverage_names_witness_without_changing_private_evidence_or_grade(self):
        cli = self.load_cli()
        value = {"status": "partial", "evidence": [{"id": "bonn-pentecost-three-prayers",
                 "grade": "page-image-collated", "record": "source-study.toml",
                 "witnesses": [target.WITNESS_EDITION, "pustet-1862"]}]}
        original = copy.deepcopy(value)
        projected = cli.public_recension_coverage(value)
        self.assertEqual(value, original)
        self.assertEqual(projected["evidence"][0]["witnesses"], [target.PUBLIC_CONTEXT["label"], "pustet-1862"])
        projected["evidence"][0]["witnesses"] = original["evidence"][0]["witnesses"]
        self.assertEqual(projected, original)
        wrapped = cli.rights_safe_copy({"recension_coverage": value})
        self.assertNotIn(target.WITNESS_EDITION, json.dumps(wrapped))

    def test_show_header_uses_public_coverage_without_mutating_source_document(self):
        from unittest import mock
        cli = self.load_cli()
        coverage = {"status": "partial", "evidence": [{"grade": "page-image-collated",
                    "witnesses": [target.WITNESS_EDITION]}]}
        document = {"sections": {"fixture": {"masses": [{"key": "fixture", "propers": []}]}},
                    "recension_coverage": coverage}
        original = copy.deepcopy(document)
        with mock.patch.object(cli, "load_calendar", return_value=document):
            payload = cli.find_mass(ROOT / "src/sources/calendars", target.CALENDAR, "fixture")
        self.assertEqual(document, original)
        self.assertEqual(payload["recension_coverage"]["evidence"][0]["witnesses"],
                         [target.PUBLIC_CONTEXT["label"]])
        self.assertEqual(payload["recension_coverage"]["evidence"][0]["grade"], "page-image-collated")
        self.assertEqual(payload["_document"], original)

    def test_cli_does_not_label_private_full_or_malformed_context(self):
        cli = self.load_cli()
        for context in (dict(target.CONTEXT), {**target.PUBLIC_CONTEXT, "civil_date_authority": True},
                        {**target.PUBLIC_CONTEXT, "label": ""}, {**target.PUBLIC_CONTEXT, "extra": True}):
            proper = {"name": "Collect", "source": "composed", "text": self.text,
                      "latin": {**self.projected(), "target_context": context}}
            self.assertNotIn(target.PUBLIC_CONTEXT["label"], str(cli.select_texts(proper, "la")))

    def test_browser_retains_public_label_and_date_limitation_without_private_ids(self):
        import subprocess
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is required for pure witness-context DOM controls")
        result = subprocess.run([node, str(ROOT / "tools/tests/pre1955_public_witness_context.cjs")],
                                cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["pure_ui_controls"], 14)


if __name__ == "__main__":
    unittest.main()
