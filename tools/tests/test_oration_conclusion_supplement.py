"""Finite conclusions preserve source quotations and require their own contexts."""
import copy
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _oration_endings as endings


def module(name, path):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    spec = importlib.util.spec_from_loader(name, loader)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    loader.exec_module(result)
    return result


class SupplementalConclusions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not endings.AUTHORITY_SHA256:
            raise unittest.SkipTest("finite conclusion authority awaits review activation")
        cls.declaration, cls.indexed = endings.authority(ROOT)
        cls.native = cls.declaration.get("supplemental_records", [])
        if not cls.native:
            raise unittest.SkipTest("no supplemental conclusion cohort admitted")
        cls.owner = module("_supplement_test_owner", ROOT / "tools/mass-propers")
        cls.sources, cls.documents, cls.masses = {}, {}, {}
        cls.controls_cache = {}
        for calendar in sorted({row["calendar"] for row in cls.native}):
            cls.sources[calendar] = endings.load_sources(ROOT / "src/sources/calendars", calendar, cls.owner)
            document = cls.owner.load_calendar(ROOT / "src/sources/calendars", calendar)
            cls.documents[calendar] = document
            cls.masses[calendar] = {mass["key"]: mass for _, mass in cls.owner.masses_of(document)}

    def member(self, row, language):
        native = row["languages"][language]
        target, calendar = row["target"], row["calendar"]
        if language == "la":
            proper = endings.supplement.direct_source(self.owner, self.documents[calendar], self.masses[calendar], target)
            text, witness = proper["text"], None
        else:
            controls = endings.supplement.source_controls(ROOT, native["source_controls"], cache=self.controls_cache)
            binding = next(value for kind, value in controls if kind == "translation-binding")
            translation = next(value for value in binding["translations"] if value.get("lang") == "en" and (value.get("source_id") or "") == native["source_id"])
            text = translation["text"]
            witness = translation.get("source_id") or translation.get("source")
        context = row["public"]["context"]
        identity = f"proper/{calendar}/{target[0]}/{context['source_index'] + 1:03}" if context["execution_kind"] == "proper-rite" else "/".join(map(str, target))
        return {"id": identity, "source": row["public"], "target": target, "text": text, "language": language, "witness": witness}

    def case(self, row, language):
        member = self.member(row, language)
        source = row["public"]["context"]
        kind = source["execution_kind"]
        if kind == "source-local-study":
            constraint = source["constraints"]["source_local_study"]
            selection = {key: constraint[key] for key in ("target", "source_selection", "rule_id", "alternative", "only_one_collect")}
            return "executeStudy", {"calendar": row["calendar"], "executionScope": kind, "sourceRule": source["source_rule"], "selection": selection, "member": member}
        if kind == "proper-rite":
            target = row["target"]
            rite = {"id": source["rite_id"], "semanticRole": source["semantic_role"], "ownConclusion": True, "locus": source["rite_locus"], "appointment": {"mass": target[0], "form_id": target[1], "proper": target[2], "occurrence": target[4]}, "sourceIndex": source["source_index"], "appointmentLocus": source["appointment_locus"]}
            return "executeProperRite", {"calendar": row["calendar"], "rite": rite, "member": member}
        context = {"calendar": row["calendar"], "massCategory": "mass-of-office", "rule": endings.GROUP_RULE, "groups": [{"kind": "principal", "position": 1, "conclusion_group": 1, "conclusion_final": True, "slot": row["target"][2], "members": [member]}]}
        choice = source.get("constraints", {}).get("wording_choice")
        if choice:
            branch = next(one for one in choice["branches"] if one["required_use"] == "principal-office-mass")
            context["prayerUse"] = {"kind": branch["required_use"], "sourceTarget": row["target"], "choiceId": choice["id"], "branch": branch["id"]}
        return "executeGroup", context

    def execute(self, api, context):
        method = {"executeGroup": endings.execute_group, "executeStudy": endings.execute_study, "executeProperRite": endings.execute_proper_rite}[api]
        return method(context, repository=ROOT, authority_rows=self.indexed)

    def test_each_admitted_language_preserves_quote_and_separates_response(self):
        cases = []
        for row in self.native:
            self.assertEqual(self.sources[row["calendar"]][tuple(row["target"])], row["public"])
            for language in row["languages"]:
                api, context = self.case(row, language)
                member = context["member"] if "member" in context else context["groups"][0]["members"][0]
                result = self.execute(api, context)
                with self.subTest(target=row["target"], language=language):
                    self.assertEqual(result["state"], "source-derived-complete")
                    projected = result["members"][0]
                    self.assertEqual(projected["source_method"], row["public"]["method_id"])
                    self.assertEqual(projected["source_text"], member["text"])
                    self.assertEqual(projected["qualification"], row["public"]["qualification"][language])
                    self.assertEqual(projected["body_fidelity"], row["public"]["body_fidelity"][language])
                    self.assertEqual(result["response"]["provider_id"], member["id"])
                    self.assertFalse(projected["priest_text"].rstrip().endswith("Amen."))
                    self.assertNotIn("℟.", projected["priest_text"])
                cases.append({"api": api, "context": context, "expected": result})
        done = subprocess.run(["node", str(ROOT / "tools/tests/oration_conclusion_supplement.mjs"), str(ROOT)], input=json.dumps({"authority_sha256": endings.AUTHORITY_SHA256, "cases": cases}), text=True, capture_output=True)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_context_target_requires_typed_source_identity(self):
        representatives = {}
        for row in self.native:
            kind = row["public"]["context"]["execution_kind"]
            if row["target"][4] == 1:
                representatives.setdefault(kind, row)
        self.assertEqual(set(representatives), {"grouped-mass-orations", "source-local-study", "proper-rite"})
        cases = []
        for row in representatives.values():
            language = next(iter(row["languages"]))
            api, context = self.case(row, language)
            for occurrence in (True, False, None, "1", 0, -1, 1.5, [], {}):
                candidate = copy.deepcopy(context)
                member = candidate["member"] if "member" in candidate else candidate["groups"][0]["members"][0]
                member["target"][4] = occurrence
                result = self.execute(api, candidate)
                with self.subTest(api=api, occurrence=occurrence):
                    self.assertEqual(result["state"], "unresolved")
                    self.assertEqual(result["members"], [])
                cases.append({"api": api, "context": candidate, "expected": result})
            # Python callers have a distinct float type. JavaScript numbers do
            # not distinguish 1.0 from 1, so this is a Python API type check.
            candidate = copy.deepcopy(context)
            member = candidate["member"] if "member" in candidate else candidate["groups"][0]["members"][0]
            member["target"][4] = 1.0
            self.assertEqual(self.execute(api, candidate)["state"], "unresolved")
        done = subprocess.run(["node", str(ROOT / "tools/tests/oration_conclusion_supplement.mjs"), str(ROOT)], input=json.dumps({"authority_sha256": endings.AUTHORITY_SHA256, "cases": cases}), text=True, capture_output=True)
        self.assertEqual(done.returncode, 0, done.stderr)

    def test_changed_source_or_context_never_leaves_partial_execution(self):
        for row in self.native:
            language = next(iter(row["languages"]))
            api, context = self.case(row, language)
            for change in ("body", "descriptor", "calendar", "witness", "identity"):
                candidate = copy.deepcopy(context)
                member = candidate["member"] if "member" in candidate else candidate["groups"][0]["members"][0]
                if change == "body": member["text"] += " "
                elif change == "descriptor": member["source"]["languages"][language]["full_conclusion"] += " "
                elif change == "calendar": candidate["calendar"] = "roman-pre-1955"
                elif change == "identity": member["id"] = ""
                elif language == "en": member["witness"] = "unheld-witness"
                else: continue
                result = self.execute(api, candidate)
                with self.subTest(target=row["target"], change=change):
                    self.assertEqual(result["state"], "unresolved")
                    self.assertEqual(result["members"], [])


if __name__ == "__main__":
    unittest.main()
