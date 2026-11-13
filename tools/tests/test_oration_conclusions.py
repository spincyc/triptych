"""Exact sourced conclusion execution cannot silently repair or change a source."""
import copy
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import sys
import subprocess
import unittest
from unittest.mock import patch

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


class OrationConclusions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not endings.AUTHORITY_SHA256:
            raise unittest.SkipTest("finite conclusion authority awaits exact review activation")
        cls.owner = module("_conclusion_owner", ROOT / "tools/mass-propers")
        cls.calendar_root = ROOT / "src/sources/calendars"
        cls.declaration, all_expected = endings.authority(ROOT)
        cls.expected = {key: row for key, row in all_expected.items() if len(key) == 5}
        cls.sources = {key: row for key, row in endings.load_sources(cls.calendar_root, "roman-1962", cls.owner).items() if key in cls.expected}
        cls.document = cls.owner.load_calendar(cls.calendar_root, "roman-1962")
        cls.masses = {mass["key"]: mass for _, mass in cls.owner.masses_of(cls.document)}
        import tomllib
        cls.bindings = {cls.owner.translation_record_identity(row, cls.document): row for row in tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())["entries"]}

    def text(self, key, language):
        if language == "la":
            return next(row["text"] for row in self.masses[key[0]]["propers"] if row["name"] == key[2])
        return next(row["text"] for row in self.bindings[key]["translations"] if row.get("source_id") == endings.SOURCE_ID and row["lang"] == "en")

    def arguments(self, key, language):
        return dict(repository=ROOT, calendar="roman-1962", target=key, language=language, witness=endings.SOURCE_ID, group_final=True, mass_category=self.sources[key]["context"]["mass_category"], authority_rows=self.expected)

    def member(self, key, language):
        return {"id": "/".join(str(part) for part in key), "target": list(key), "source": self.sources[key], "text": self.text(key, language), "language": language, "witness": endings.SOURCE_ID}

    def context(self, language, commemorations=False):
        keys = [("s-ioannis-damasceni-confessoris-ecclesiae-doctoris", "main", "Postcommunion", "all", 1), ("comm-septem-dolorum-beatae-mariae-virginis", "main", "Postcommunion", "all", 1)] if commemorations else [("advent-2", "main", "Secret", "all", 1)]
        return {"calendar": "roman-1962", "massCategory": "mass-of-office", "rule": endings.GROUP_RULE, "groups": [{"kind": "commemoration" if commemorations else "principal", "position": index + (2 if commemorations else 1), "conclusion_group": 2 if commemorations else 1, "conclusion_final": index == len(keys)-1, "slot": key[2], "members": [self.member(key, language)]} for index, key in enumerate(keys)]}

    def test_every_closed_owner_reconstructs_both_languages(self):
        self.assertEqual(set(self.sources), set(self.expected))
        for key, source in self.sources.items():
            for language in ("en", "la"):
                original = self.text(key, language)
                result = endings.execute(source, original, **self.arguments(key, language))
                self.assertEqual(result["source_text"], original)
                self.assertEqual(result["response"], {"speaker": "response", "text": "Amen."})
                self.assertEqual(result["execution_extent"]["state"], "source-derived-complete")
                self.assertTrue(result["priest_text"].endswith(source["languages"][language]["full_conclusion"]))
        self.assertNotIn(("comm-ss-processi-martiniani-martyrum", "main", "Postcommunion", "all", 1), self.sources)
        self.assertEqual(endings.load_sources(self.calendar_root, "roman-pre-1955", self.owner), {})

    def test_witness_context_and_source_changes_refuse(self):
        key = ("advent-2", "main", "Secret", "all", 1)
        source = self.sources[key]
        for language in ("en", "la"):
            text = self.text(key, language)
            arguments = self.arguments(key, language)
            changes = [{"calendar": "postconciliar"}, {"target": ("advent-3", *key[1:])}, {"group_final": False}, {"group_final": 1}, {"mass_category": "votive"}, {"language": "xx"}]
            if language == "en":
                changes.append({"witness": "edition.unheld"})
            for change in changes:
                with self.subTest(language=language, change=change), self.assertRaises(ValueError):
                    endings.execute(source, text, **{**arguments, **change})
            with self.assertRaises(ValueError):
                endings.execute(source, text + " ", **arguments)
        for field in ("family", "source_id", "source_publication_passage_id", "rule_passage_id", "formula_table_sha256", "target_proof_sha256", "private_field"):
            bad = copy.deepcopy(source)
            bad[field] = "changed"
            with self.subTest(field=field), self.assertRaises(ValueError):
                endings.validate_public(bad, ROOT, authority_rows=self.expected)
        for field in ("cue", "cue_start", "cue_end", "full_conclusion", "offset_units"):
            bad = copy.deepcopy(source)
            bad["languages"]["en"][field] = "changed"
            with self.subTest(field=field), self.assertRaises(ValueError):
                endings.validate_public(bad, ROOT, authority_rows=self.expected)

    def test_authority_and_source_record_drift_refuse(self):
        read_bytes = Path.read_bytes
        for relative in (endings.AUTHORITY_PATH, endings.TABLE_PATH, *[row["path"] for row in self.declaration["source_records"]]):
            def altered(path):
                raw = read_bytes(path)
                return raw + b" " if path == ROOT / relative else raw
            with self.subTest(path=relative), patch.object(Path, "read_bytes", altered), self.assertRaises(ValueError):
                endings.load_sources(self.calendar_root, "roman-1962", self.owner)

    def test_latin_family_is_checked_independently_of_english_cue(self):
        key = ("advent-2", "main", "Secret", "all", 1)
        formula = next(row for row in json.loads((ROOT / endings.TABLE_PATH).read_text())["formulas"] if row["key"] == self.expected[key]["family"])
        altered = copy.deepcopy(formula)
        altered["full_latin"] = "Qui vivis et regnas cum Deo Patre in unitate Spiritus Sancti, Deus, per omnia saecula saeculorum."
        with self.assertRaisesRegex(ValueError, "Latin cue"):
            endings.public_projection(self.expected[key], self.text(key, "en"), self.text(key, "la"), self.bindings[key], altered)

    def test_groups_are_atomic_and_principal_concludes_separately(self):
        for language in ("en", "la"):
            principal = endings.execute_group(self.context(language), repository=ROOT, authority_rows=self.expected)
            grouped = endings.execute_group(self.context(language, True), repository=ROOT, authority_rows=self.expected)
            self.assertEqual(principal["state"], "source-derived-complete")
            self.assertEqual(principal["conclusion_group"], 1)
            self.assertEqual(grouped["state"], "source-derived-complete")
            self.assertEqual([row["role"] for row in grouped["members"]], ["petition", "conclusion-provider"])
            self.assertEqual(grouped["response"]["provider_id"], grouped["members"][-1]["id"])
            first = self.context(language, True)["groups"][0]["members"][0]
            cut = first["source"]["languages"][language]["cue_start"]
            self.assertEqual(grouped["members"][0]["priest_text"], first["text"].encode("utf-16-le")[:cut*2].decode("utf-16-le"))
            for change in ("missing-provider", "changed-intermediate", "wrong-order", "mixed-groups", "wrong-rule"):
                context = self.context(language, True)
                if change == "missing-provider": context["groups"][1]["members"][0]["source"] = None
                elif change == "changed-intermediate": context["groups"][0]["members"][0]["text"] += " "
                elif change == "wrong-order": context["groups"].reverse()
                elif change == "mixed-groups": context["groups"][0]["conclusion_group"] = 1
                elif change == "wrong-rule": context["rule"] = "unsourced"
                result = endings.execute_group(context, repository=ROOT, authority_rows=self.expected)
                with self.subTest(language=language, change=change):
                    self.assertEqual(result["state"], "unresolved")
                    self.assertEqual(result["members"], [])

    def test_browser_projector_matches_python_and_generated_pins(self):
        cases = [self.context(language, grouped) for language in ("en", "la") for grouped in (False, True)]
        expected = [endings.execute_group(context, repository=ROOT, authority_rows=self.expected) for context in cases]
        pins = {endings.canonical(row["target"]): row["public_sha256"] for row in self.declaration["records"]}
        pins.update({endings.canonical([row["calendar"], *row["target"]]): row["public_sha256"] for row in self.declaration.get("supplemental_records", [])})
        payload = {"authority_sha256": endings.AUTHORITY_SHA256, "pins": pins, "cases": cases, "expected": expected}
        done = subprocess.run(["node", str(ROOT / "tools/tests/oration_conclusions.mjs"), str(ROOT)], input=json.dumps(payload), text=True, capture_output=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertGreaterEqual(json.loads(done.stdout)["refusals"], 20)
        browser = (ROOT / "src/web/browser/liturgy/oration-conclusions.js").read_text()
        section = endings.browser_pin_section(self.declaration, endings.AUTHORITY_SHA256)
        self.assertIn(section, browser)

    def test_public_gate_checks_owner_and_witness_but_allows_borrowed_repeats(self):
        import _missal_coverage
        gate = module("_conclusion_public_gate", ROOT / "tools/public-alpha")
        key = ("advent-2", "main", "Secret", "all", 1)
        source = self.sources[key]
        proper = {"name": "Secret", "form_id": "main", "source": "composed", "text": self.text(key, "la"), "translations": [{"lang": "en", "source_id": endings.SOURCE_ID, "rights": "public-domain", "text": self.text(key, "en")}], "coverage": {"target_id": _missal_coverage.identity(_missal_coverage.identity("roman-1962", "proper", key[0], key[1], key[2], key[4]), "all", "all")}, "conclusion_execution": [source]}
        payload = {"calendar": "roman-1962", "masses": [{"key": "advent-2", "propers": [proper]}]}
        virtual = ROOT / "src/web/data/structure/propers/conclusion-execution-test.json"
        read_text = Path.read_text

        def check(data):
            def read(path, *args, **kwargs):
                return json.dumps(data, ensure_ascii=False) if path == virtual else read_text(path, *args, **kwargs)
            # This unit exercises only the new finite descriptor gate using
            # checked historical text. The existing quarantine/release suite
            # independently checks the full current source-epoch receipt.
            with patch.object(Path, "read_text", read), patch.object(gate, "postconciliar_quarantined_text_hashes", return_value=frozenset()):
                gate.validate_liturgical_public_data(virtual)

        check(payload)
        borrowed = copy.deepcopy(payload)
        other = copy.deepcopy(proper)
        other["taken_from"] = {"mass": "advent-2", "form": "", "proper": "Secret"}
        borrowed["masses"].append({"key": "borrowing-appointment", "propers": [other]})
        # The separate source replay owns appointment correctness; this gate
        # must not reject a second occurrence of the same authenticated owner.
        check(borrowed)
        for change in ("calendar", "owner", "body", "witness", "descriptor", "occurrence", "duplicate"):
            bad = copy.deepcopy(payload)
            row = bad["masses"][0]["propers"][0]
            if change == "calendar": bad["calendar"] = "roman-pre-1955"
            elif change == "owner": bad["masses"][0]["key"] = "advent-3"
            elif change == "body": row["text"] += " "
            elif change == "witness": row["translations"][0]["source_id"] = "edition.other"
            elif change == "descriptor": row["conclusion_execution"][0]["private_field"] = "changed"
            elif change == "occurrence": row["coverage"]["target_id"] += "changed"
            elif change == "duplicate": row["conclusion_execution"].append(copy.deepcopy(source))
            with self.subTest(change=change), self.assertRaises(gate.ReleaseError):
                check(bad)


if __name__ == "__main__":
    unittest.main()
