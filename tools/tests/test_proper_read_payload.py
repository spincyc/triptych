"""The 1962 resolved-Read split reconstructs the served public structure."""
from __future__ import annotations

import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
PROPERS = ROOT / "src/web/data/structure/propers"


def load_generator():
    path = ROOT / "tools/mass-propers"
    loader = importlib.machinery.SourceFileLoader("proper_read_payload_generator", str(path))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ProperReadPayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.generator = load_generator()

    def test_all_masses_reconstruct_the_exact_public_structure(self) -> None:
        source_bytes = (PROPERS / "roman-1962.json").read_bytes()
        source = json.loads(source_bytes)
        catalog = json.loads((PROPERS / "catalog/roman-1962.json").read_text())
        index = json.loads((PROPERS / "index.json").read_text())
        entry = next(row for row in index["missals"] if row["id"] == "roman-1962")
        self.assertEqual(entry["read_payload"], {
            "catalog": "structure/propers/catalog/roman-1962.json",
            "mass_prefix": "structure/propers/mass/roman-1962/",
        })
        self.assertEqual(catalog["schema"], self.generator.READ_CATALOG_SCHEMA)
        self.assertEqual(catalog["calendar"], "roman-1962")
        self.assertEqual(catalog["generation"], hashlib.sha256(source_bytes).hexdigest())
        self.assertEqual(catalog["structure"], {
            key: value for key, value in source.items() if key != "masses"
        })
        descriptors = catalog["masses"]
        self.assertEqual(len(descriptors), 491)
        self.assertEqual([row["key"] for row in descriptors],
                         [mass["key"] for mass in source["masses"]])
        self.assertEqual(len({row["key"] for row in descriptors}), 491)

        files = sorted((PROPERS / "mass/roman-1962").glob("*.json"))
        self.assertEqual({path.stem for path in files},
                         {mass["key"] for mass in source["masses"]})
        reconstructed = []
        for descriptor, original in zip(descriptors, source["masses"], strict=True):
            key = original["key"]
            self.assertRegex(key, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
            envelope = json.loads((PROPERS / "mass/roman-1962" / f"{key}.json").read_text())
            self.assertEqual(set(envelope), {"schema", "calendar", "generation", "mass"})
            self.assertEqual(envelope["schema"], self.generator.READ_MASS_SCHEMA)
            self.assertEqual(envelope["calendar"], catalog["calendar"])
            self.assertEqual(envelope["generation"], catalog["generation"])
            self.assertEqual(envelope["mass"], original)
            self.assertEqual(descriptor, {
                "key": key,
                "name": original.get("name"),
                "kind": original.get("kind"),
                "season": original.get("season"),
                "date": original.get("date"),
                "coverage": original.get("coverage"),
                "forms": [{"id": form.get("id"), "name": form.get("name"),
                           "ordinal": form.get("ordinal")}
                          for form in original.get("forms") or []],
            })
            reconstructed.append(envelope["mass"])
        self.assertEqual({**catalog["structure"], "masses": reconstructed}, source)

    def test_unsafe_or_duplicate_mass_keys_refuse_file_projection(self) -> None:
        minimal = {"calendar": "roman-1962", "masses": [{"key": "valid"}]}
        for key in ("../escape", "Uppercase", "bad_underscore", "", "a//b"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.generator.read_payloads(
                    {**minimal, "masses": [{"key": key}]}, "0" * 64
                )
        with self.assertRaises(ValueError):
            self.generator.read_payloads(
                {**minimal, "masses": [{"key": "valid"}, {"key": "valid"}]},
                "0" * 64,
            )

    def test_scoped_check_and_full_orphan_check_preserve_owned_files(self) -> None:
        scratch = Path(os.environ.get(
            "TRIPTYCH_PROPER_READ_TEST_SCRATCH",
            ROOT / ".scratch/agent-print-composition/read-payload-tests",
        ))
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            out = Path(temporary)
            args = argparse.Namespace(
                root=str(ROOT / "src/sources/calendars"), out=str(out),
                calendar="roman-1962", check=False, verbose=False,
            )
            self.generator.run_structure(args)
            args.check = True
            self.assertEqual(self.generator.run_structure(args)["status"], "ok")

            mass = out / "structure/propers/mass/roman-1962/pentecost-10.json"
            original = mass.read_bytes()
            mass.write_bytes(b"{}\n")
            orphan = out / "structure/propers/mass/roman-1962/foreign.json"
            orphan.write_bytes(b"{}\n")
            scoped = self.generator.run_structure(args)
            self.assertEqual(scoped["status"], "stale")
            self.assertIn(str(mass), scoped["drifted"])
            self.assertNotIn(str(orphan), scoped["drifted"])
            self.assertEqual(mass.read_bytes(), b"{}\n")
            self.assertTrue(orphan.is_file())

            args.calendar = None
            with mock.patch.object(self.generator, "calendars", return_value=["roman-1962"]):
                full = self.generator.run_structure(args)
                self.assertIn(str(mass), full["drifted"])
                self.assertIn(str(orphan), full["drifted"])
                args.check = False
                repaired = self.generator.run_structure(args)
            self.assertEqual(repaired["status"], "ok")
            self.assertEqual(mass.read_bytes(), original)
            self.assertFalse(orphan.exists())


if __name__ == "__main__":
    unittest.main()
