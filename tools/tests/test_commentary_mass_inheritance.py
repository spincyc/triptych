"""Commentary and harvest read the same appointed Scripture as the Missal."""

from __future__ import annotations

import argparse
import copy
import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[2]
loader = importlib.machinery.SourceFileLoader("commentary_mass_inheritance", str(ROOT / "tools/commentary-work-index"))
spec = importlib.util.spec_from_loader(loader.name, loader)
index = importlib.util.module_from_spec(spec)
# Dataclasses inspects its module during import.
import sys
sys.modules[spec.name] = index
loader.exec_module(index)


def scripture(name, ref):
    return {"name": name, "source": "scripture", "verses": [ref]}


class AppointedMassScriptureTests(unittest.TestCase):
    def setUp(self):
        self.base = {"key": "common", "name": "Common", "propers": [
            scripture("Epistle", "1 Corinthians 1:4-8"), scripture("Gospel", "John 1:1-5"),
        ]}
        self.target = {"key": "weekday", "name": "Weekday", "takes_from": {"mass": "common"}}
        self.doc = {"psalm_numbering": "vulgate", "sections": {"seasonal": {
            "kind": "seasonal", "masses": [self.base, self.target],
        }}}
        self.citations = index._load_citations_tool()

    def collect(self):
        return [row for row in index._collect_mass_records(self.citations, self.doc, "test")
                if row["mass_key"] == "weekday"]

    def refs(self):
        return [(row["proper_slot"], row["passage"]["ref"]) for row in self.collect()]

    def test_a_referenced_mass_keeps_every_appointed_scripture_slot(self):
        self.assertEqual(self.refs(), [("Epistle", "1 Corinthians 1:4-1:8"), ("Gospel", "John 1:1-1:5")])

    def test_a_local_override_replaces_the_common_reading(self):
        self.target["propers"] = [scripture("Gospel", "Luke 1:1-4")]
        self.assertEqual(self.refs(), [("Epistle", "1 Corinthians 1:4-1:8"), ("Gospel", "Luke 1:1-1:4")])

    def test_an_individually_referenced_proper_resolves(self):
        self.target.pop("takes_from")
        self.target["propers"] = [{"name": "Gospel", "takes_from": {"mass": "common", "proper": "Gospel"}}]
        self.assertEqual(self.refs(), [("Gospel", "John 1:1-1:5")])

    def test_reference_to_a_named_form_keeps_the_target_mass_identity(self):
        self.base.pop("propers")
        self.base["forms"] = [{"name": "Vigil", "propers": [scripture("Gospel", "John 1:1-5")]}]
        self.target["takes_from"]["form"] = "Vigil"
        rows = self.collect()
        self.assertEqual([(row["mass_key"], row["mass_name"], row["source_category"]) for row in rows],
                         [("weekday", "Weekday", "base")])
        self.assertEqual(self.refs(), [("Gospel", "John 1:1-1:5")])

    def test_local_form_still_has_its_own_corpus_identity(self):
        self.target.pop("takes_from")
        self.target["forms"] = [{"name": "Vigil", "kind": "ritual", "propers": [scripture("Gospel", "John 1:1-5")]}]
        rows = index._collect_mass_records(self.citations, self.doc, "test")
        row = next(row for row in rows if row["mass_key"] == "weekday:Vigil")
        self.assertEqual((row["mass_name"], row["mass_kind"], row["source_category"]), ("Weekday (Vigil)", "ritual", "form"))

    def test_inherited_psalm_keeps_its_declared_numbering(self):
        self.doc["psalm_numbering"] = "hebrew"
        self.base["propers"] = [{**scripture("Introit", "Psalm 118:4-5"), "psalm_numbering": "vulgate"}]
        row = self.collect()[0]
        self.assertEqual(row["numbering"], "vulgate")
        canonical = index._canonical_passage(row["passage"], row["numbering"])
        self.assertEqual(canonical["ranges"][0]["begin"]["chapter"], 118)

    def test_both_weekday_reading_courses_are_included(self):
        self.base["propers"] = [{"name": "First Reading", "source": "scripture", "weekday_cycles": {
            "I": {"verses": ["Hebrews 1:1-6"]},
            "II": {"verses": ["1 Samuel 1:1-8"]},
        }}]
        self.assertEqual(self.refs(), [
            ("First Reading/I", "Hebrews 1:1-1:6"),
            ("First Reading/II", "1 Samuel 1:1-1:8"),
        ])

    def test_every_cycle_owner_retains_its_numbering(self):
        self.doc["psalm_numbering"] = "hebrew"
        self.base["propers"] = [{
            "name": "Psalm", "source": "scripture", "psalm_numbering": "vulgate",
            "verses": ["Psalm 118:4-5"],
            "cycles": {"A": {"verses": ["Psalm 118:4-5"]}},
            "weekday_cycles": {
                "I": {"verses": ["Psalm 118:4-5"]},
                "II": {"psalm_numbering": "hebrew", "verses": ["Psalm 119:4-5"]},
            },
        }]
        rows = self.collect()
        self.assertEqual([(row["proper_slot"], row["numbering"]) for row in rows], [
            ("Psalm", "vulgate"), ("Psalm/A", "vulgate"),
            ("Psalm/I", "vulgate"), ("Psalm/II", "hebrew"),
        ])
        self.assertEqual({
            index._canonical_passage(row["passage"], row["numbering"])["ranges"][0]["begin"]["chapter"]
            for row in rows
        }, {118})

    def test_unresolvable_inheritance_is_refused(self):
        self.target["takes_from"]["mass"] = "missing"
        with self.assertRaisesRegex(ValueError, "names mass 'missing'"):
            self.collect()

    def test_reading_references_does_not_mutate_the_calendar(self):
        before = copy.deepcopy(self.doc)
        self.collect()
        self.assertEqual(self.doc, before)

    def test_corpus_check_detects_changed_inherited_readings_without_writing(self):
        scratch = ROOT / ".scratch/resume-corpus-pipeline"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temp:
            folder = Path(temp)
            calendar = folder / "test/propers.yaml"
            calendar.parent.mkdir()
            calendar.write_text("{}\n", encoding="utf-8")
            discovery = folder / "index.yaml"
            discovery.write_text(yaml.safe_dump({
                "schema": index.SCHEMA_DISCOVERY, "numbering": "vulgate", "passages": [{
                    "passage": "John 1", "works": [{"author": "Author", "title": "Commentary"}],
                }],
            }), encoding="utf-8")
            args = argparse.Namespace(
                root=folder, discovery=discovery, calendar=["test"],
                output=folder / "corpus.yaml", check=False,
                max_results_per_mass=20, max_results_per_passage=20,
            )
            with patch.object(index, "_load_calendar_doc", return_value=self.doc):
                index.run_build_corpus(args, self.citations)
                before = args.output.read_bytes()
                args.check = True
                index.run_build_corpus(args, self.citations)
                self.base["propers"][1]["verses"] = ["John 2:1-5"]
                with self.assertRaisesRegex(ValueError, "missing or stale"):
                    index.run_build_corpus(args, self.citations)
                self.assertEqual(args.output.read_bytes(), before)
                args.output.unlink()
                with self.assertRaisesRegex(ValueError, "missing or stale"):
                    index.run_build_corpus(args, self.citations)
                self.assertFalse(args.output.exists())


if __name__ == "__main__":
    unittest.main()
