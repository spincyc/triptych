"""The publication split binds RG110 metadata to its exact public rubric owner."""
from __future__ import annotations

import copy
import hashlib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(os.environ.get("TRIPTYCH_RG110_PUBLICATION_ROOT", Path(__file__).resolve().parents[2]))
TOOL = Path(os.environ.get("TRIPTYCH_RG110_PUBLICATION_TOOL", ROOT / "tools/public-alpha"))
sys.path.insert(0, str(ROOT / "scripts"))


def load_tool(path: Path, name: str):
    loader = SourceFileLoader(name, str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


class Rg110Publication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = load_tool(TOOL, "_rg110_publication_guard")
        cls.producer = load_tool(ROOT / "tools/mass-propers", "_rg110_publication_producer")
        cls.rubrics = json.loads((ROOT / "src/web/data/structure/rubrics/roman-1962.json").read_bytes())
        pairs = cls.rubrics["commemoration"]["inseparable"]["pairs"]
        cls.keys = [pair[field] for pair in pairs for field in ("host", "companion")]
        cls.structure = json.loads((ROOT / "src/web/data/structure/propers/roman-1962.json").read_bytes())
        cls.structure["masses"] = [mass for mass in cls.structure["masses"] if mass["key"] in cls.keys]
        assert len(cls.structure["masses"]) == 6
        cls.index = json.loads((ROOT / "src/web/data/structure/propers/index.json").read_bytes())
        scratch = ROOT / ".scratch"
        scratch.mkdir(exist_ok=True)
        cls.temporary = tempfile.TemporaryDirectory(prefix="rg110-publication-test-", dir=scratch)
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.fixture_root = Path(cls.temporary.name)

    def write_json(self, path: Path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = (json.dumps(value, sort_keys=True) + "\n").encode()
        path.write_bytes(raw)
        return raw

    def fixture(self, structure=None, rubrics=None):
        data = self.fixture_root / "data"
        structure = copy.deepcopy(self.structure if structure is None else structure)
        rubrics = copy.deepcopy(self.rubrics if rubrics is None else rubrics)
        self.write_json(data / "structure/rubrics/roman-1962.json", rubrics)
        self.write_json(data / "structure/propers/index.json", self.index)
        raw = self.write_json(data / "structure/propers/roman-1962.json", structure)
        catalog, payloads = self.producer.read_payloads(structure, hashlib.sha256(raw).hexdigest())
        self.write_json(data / "structure/propers/catalog/roman-1962.json", catalog)
        for key, payload in payloads.items():
            self.write_json(data / f"structure/propers/mass/roman-1962/{key}.json", payload)
        return data

    def test_current_whole_generated_source_and_six_owner_fixture_are_accepted(self):
        self.tool.validate_propers_read_payload_sources(ROOT / "src/web/data")
        self.tool.validate_propers_read_payload_sources(self.fixture())

    def test_matching_generations_do_not_license_changed_missing_or_extra_relation_fields(self):
        mutations = {
            "unknown-field": lambda relation: relation.update(private_source="unbound"),
            "wrong-host": lambda relation: relation.update(host="advent-1"),
            "wrong-companion": lambda relation: relation.update(companion="cathedrae-s-petri-apostoli"),
            "wrong-scope": lambda relation: relation.update(scope="votive"),
            "wrong-order": lambda relation: relation["slots"].reverse(),
            "incomplete-slots": lambda relation: relation.update(slots=["Collect"]),
            "wrong-locus": lambda relation: relation.update(locus="unproved source"),
            "missing-field": lambda relation: relation.pop("companion"),
        }
        for key in self.keys:
            for label, mutate in mutations.items():
                with self.subTest(key=key, mutation=label):
                    structure = copy.deepcopy(self.structure)
                    mass = next(mass for mass in structure["masses"] if mass["key"] == key)
                    mutate(mass["oration_relation"])
                    with self.assertRaisesRegex(self.tool.ReleaseError, "unbound inseparable-oration relation"):
                        self.tool.validate_propers_read_payload_sources(self.fixture(structure))
            with self.subTest(key=key, mutation="dropped-relation"):
                structure = copy.deepcopy(self.structure)
                next(mass for mass in structure["masses"] if mass["key"] == key).pop("oration_relation")
                with self.assertRaisesRegex(self.tool.ReleaseError, "unbound inseparable-oration relation"):
                    self.tool.validate_propers_read_payload_sources(self.fixture(structure))

    def test_matching_split_does_not_license_an_unrelated_mass_field(self):
        structure = copy.deepcopy(self.structure)
        structure["masses"][0]["private_source"] = "unbound"
        with self.assertRaisesRegex(self.tool.ReleaseError, "unbound fields"):
            self.tool.validate_propers_read_payload_sources(self.fixture(structure))

    def test_relation_cannot_be_attached_to_an_unlisted_mass(self):
        generated = json.loads((ROOT / "src/web/data/structure/propers/roman-1962.json").read_bytes())
        unrelated = copy.deepcopy(next(mass for mass in generated["masses"] if mass["key"] == "advent-1"))
        unrelated["oration_relation"] = copy.deepcopy(self.structure["masses"][0]["oration_relation"])
        structure = copy.deepcopy(self.structure)
        structure["masses"].append(unrelated)
        with self.assertRaisesRegex(self.tool.ReleaseError, "source Mass advent-1 has an unbound inseparable-oration relation"):
            self.tool.validate_propers_read_payload_sources(self.fixture(structure))

    def test_split_relation_and_body_remain_exact_to_the_source_monolith(self):
        for key in self.keys:
            for label in ["relation", "body"]:
                with self.subTest(key=key, mutation=label):
                    data = self.fixture()
                    path = data / f"structure/propers/mass/roman-1962/{key}.json"
                    payload = json.loads(path.read_bytes())
                    if label == "relation":
                        payload["mass"]["oration_relation"]["scope"] = "votive"
                    else:
                        proper = next(p for p in payload["mass"]["propers"] if p.get("text"))
                        proper["text"] += " CORRUPTION CONTROL"
                    self.write_json(path, payload)
                    with self.assertRaisesRegex(self.tool.ReleaseError, "envelope differs"):
                        self.tool.validate_propers_read_payload_sources(data)

    def test_relation_requires_the_supported_applied_rubric_and_unique_existing_members(self):
        mutations = {
            "inactive": lambda rule: rule.update(applied=False),
            "string-applied": lambda rule: rule.update(applied="true"),
            "wrong-context": lambda rule: rule["execution"].update(scope="ritual"),
            "wrong-count": lambda rule: rule["execution"].update(count=2),
            "boolean-count": lambda rule: rule["execution"].update(count=True),
            "extra-execution": lambda rule: rule["execution"].update(extra=True),
            "unapplied": lambda rule: rule.update(unapplied={}),
            "missing-pairs": lambda rule: rule.update(pairs=[]),
            "unknown-member": lambda rule: rule["pairs"][0].update(host="unknown"),
            "extra-pair-field": lambda rule: rule["pairs"][0].update(extra=True),
            "duplicate-member": lambda rule: rule["pairs"].append(copy.deepcopy(rule["pairs"][0])),
        }
        for label, mutate in mutations.items():
            with self.subTest(mutation=label):
                rubrics = copy.deepcopy(self.rubrics)
                mutate(rubrics["commemoration"]["inseparable"])
                with self.assertRaisesRegex(self.tool.ReleaseError, "inseparable-oration"):
                    self.tool.validate_propers_read_payload_sources(self.fixture(rubrics=rubrics))
        data = self.fixture()
        (data / "structure/rubrics/roman-1962.json").unlink()
        with self.assertRaisesRegex(self.tool.ReleaseError, "unbound inseparable-oration relation"):
            self.tool.validate_propers_read_payload_sources(data)


if __name__ == "__main__":
    unittest.main()
