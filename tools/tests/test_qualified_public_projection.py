"""Qualified Proper publication exposes the carrier, never comparison proofs."""
import copy
from hashlib import sha256
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _proper_latin as L
import _proper_qualified_latin as Q


def tool(name, path):
    loader = SourceFileLoader(name, str(path))
    spec = spec_from_loader(name, loader)
    module = module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module


class QualifiedPublicProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mass = tool("qualified_public_mass", ROOT / "tools/mass-propers")
        cls.release = tool("qualified_public_release", ROOT / "tools/public-alpha")
        records, problems = L.publication_records(ROOT / "src/sources/calendars", "roman-1962")
        if problems:
            raise AssertionError(problems)
        document = L._calendars.load_document(ROOT / "src/sources/calendars", "roman-1962")
        bodies = dict(L.text_owners(document))
        cls.private = {}
        for scope in Q.SCOPES:
            key = L.LatinKey(*scope["key"])
            cls.private[scope["body_sha256"]] = L._decision(key, bodies[key], records[key]).projection(L.SURFACES)
        cls.payloads = {p.stem: json.loads(p.read_text()) for p in
                        (ROOT / "src/web/data/structure/propers/mass/roman-1962").glob("*.json")}

    def test_actual_Common_Damasus_and_all_reference_wrappers_pass_public_gate(self):
        common = damasus = references = private_refusals = 0
        with tempfile.TemporaryDirectory() as tmp, patch.object(self.release, "WEB_DATA_ROOT_RELATIVE", Path(tmp)):
            for key, original in self.payloads.items():
                payload = copy.deepcopy(original)
                affected = []
                for proper in payload["mass"]["propers"]:
                    latin = proper.get("latin") or {}
                    digest = latin.get("text_sha256")
                    if digest in self.private:
                        private = copy.deepcopy(self.private[digest])
                        proper["latin"] = private
                        affected.append(proper)
                        if digest == Q.SCOPES[0]["body_sha256"]:
                            common += 1
                            references += key != "commune-summorum-pontificum"
                        else:
                            damasus += 1
                path = Path(tmp) / "structure/propers/mass/roman-1962" / (key + ".json")
                path.parent.mkdir(parents=True, exist_ok=True)
                if affected:
                    path.write_text(json.dumps(payload))
                    with self.assertRaisesRegex(self.release.ReleaseError, "protected source identity"):
                        self.release.validate_liturgical_public_data(path)
                    private_refusals += 1
                before_bodies = [p.get("text") for p in payload["mass"]["propers"]]
                before_English = [p.get("translations") for p in payload["mass"]["propers"]]
                projected = self.mass.rights_safe_copy(payload)
                self.assertEqual([p.get("text") for p in projected["mass"]["propers"]], before_bodies)
                self.assertEqual([p.get("translations") for p in projected["mass"]["propers"]], before_English)
                path.write_text(json.dumps(projected))
                self.release.validate_liturgical_public_data(path)
        self.assertEqual((common, references, damasus, private_refusals), (18, 17, 1, 19))

    def test_public_envelope_retains_qualification_and_full_private_proof_is_unchanged(self):
        for scope in Q.SCOPES:
            private = self.private[scope["body_sha256"]]
            before = copy.deepcopy(private)
            public = self.mass.public_latin_state(private, "Collect")
            self.assertEqual(private, before)
            self.assertGreater(len(private["publication"]["source_ids"]), 1)
            self.assertEqual(public["text_sha256"], scope["body_sha256"])
            self.assertEqual(public["publication"]["basis"], Q.BASIS)
            self.assertEqual(public["publication"]["surfaces"], private["publication"]["surfaces"])
            self.assertEqual(public["publication"]["source_ids"], [scope["artifact_id"]])
            self.assertIn("moderate confidence", public["publication"]["notice"])
            self.assertIn("originality objection remains", public["publication"]["notice"])
            for field in ("verification_source_id", "verification_locator", "provenance_evidence", "locator"):
                self.assertNotIn(field, public["provenance"])
            for field in ("authority", "evidence", "locator"):
                self.assertNotIn(field, public["publication"])

    def test_unknown_qualified_context_is_neutral_and_other_states_are_conserved(self):
        private = copy.deepcopy(next(iter(self.private.values())))
        private["text_sha256"] = "0" * 64
        self.assertEqual(self.mass.public_latin_state(private, "Collect"), {
            "target": "Collect", "state": "unavailable", "held": False,
            "available": False, "withheld": True})
        ordinary = {"text_sha256": "public", "withheld": False, "publication": {"basis": "public-domain"},
                    "target_context": {"scope": "witness-state-only", "civil_date_authority": False}}
        self.assertIs(self.mass.public_latin_state(ordinary, "Collect"), ordinary)
        held = {"withheld": True, "source_id": "private", "state": "unavailable"}
        self.assertEqual(self.mass.public_latin_state(held, "Collect"), {
            "target": "Collect", "state": "unavailable", "held": False,
            "available": False, "withheld": True})

    def test_actual_Bonn_and_other_calendar_public_states_are_unchanged(self):
        bonn = 0
        for calendar in ("roman-pre-1955", "postconciliar"):
            payload = json.loads((ROOT / "src/web/data/structure/propers" / (calendar + ".json")).read_text())
            def visit(value):
                nonlocal bonn
                if isinstance(value, list):
                    for item in value:
                        visit(item)
                elif isinstance(value, dict):
                    latin = value.get("latin")
                    if isinstance(latin, dict):
                        before = json.dumps(latin, sort_keys=True)
                        after = self.mass.public_latin_state(latin, value.get("name") or "Proper")
                        self.assertEqual(json.dumps(after, sort_keys=True), before)
                        if latin.get("target_context"):
                            bonn += 1
                    for item in value.values():
                        visit(item)
            visit(payload)
        self.assertEqual(bonn, 3)


if __name__ == "__main__":
    unittest.main()
