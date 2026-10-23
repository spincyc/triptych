"""Reviewed work identity survives harvest promotion and corpus aggregation."""

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
loader = importlib.machinery.SourceFileLoader("harvest_work_identity", str(ROOT / "tools/harvest"))
spec = importlib.util.spec_from_loader(loader.name, loader)
harvest = importlib.util.module_from_spec(spec)
loader.exec_module(harvest)


class CanonicalWorkIdentityTests(unittest.TestCase):
    def setUp(self):
        self.runs = [{
            "run_id": "one", "model": "test", "audited_on": "2026-10-23",
            "passages": {"John 1": [{
                "author": "Augustine", "title": "Tractates", "aliases": ["Homilies"],
                "role": "church-father", "death_year": 430,
            }]},
        }]
        self.row = {
            "author": "Augustine", "work": "Homilies",
            "work_id": "work.augustine.tractates",
            "reason": "The work record identifies this complete collection under both titles.",
        }
        self.library = {self.row["work_id"]: {"responsible": "Augustine"}}

    def registry(self):
        groups, _ = harvest._derive_groups(self.runs, {})
        group = groups[0]
        self.row["work"] = group["work"]
        key = (harvest._fold(group["author"]), harvest._fold(group["work"]))
        return harvest._Registry({("augustine", title): key for title in group["titles"]})

    def review(self, rows=None):
        return {"canonical_work_ids": [self.row] if rows is None else rows}

    def resolve(self, review=None, registry=None):
        registry = registry if registry is not None else self.registry()
        with patch("_containment.catalog", return_value={"works": self.library}):
            return harvest._reviewed_work_ids(review or self.review(), registry, self.runs)

    def test_review_applies_to_every_title_without_rewriting_the_run(self):
        registry = self.registry()
        registry.work_ids = self.resolve(registry=registry)
        before = copy.deepcopy(self.runs)
        alternate = copy.deepcopy(self.runs[0])
        alternate["passages"]["John 1"][0]["title"] = "Homilies"
        for run in [self.runs[0], alternate]:
            found = next(iter(harvest._locus_answers(run, registry)["John 1"].values()))
            self.assertEqual(found["work"]["work_id"], self.row["work_id"])
        self.assertEqual(self.runs, before)

    def test_no_review_leaves_holdings_separate_from_identity(self):
        with patch("_containment.catalog") as catalog:
            self.assertEqual(harvest._reviewed_work_ids({}, self.registry(), self.runs), {})
            catalog.assert_not_called()
        found = next(iter(harvest._locus_answers(self.runs[0], self.registry())["John 1"].values()))
        self.assertNotIn("work_id", found["work"])

    def test_an_unreviewed_raw_id_cannot_bypass_identity_review(self):
        for raw_id in ("work.missing", "work.john-chrysostom.homilies-on-philippians"):
            with self.subTest(raw_id=raw_id):
                self.runs[0]["passages"]["John 1"][0]["work_id"] = raw_id
                before = copy.deepcopy(self.runs)
                found = next(iter(harvest._locus_answers(self.runs[0], self.registry())["John 1"].values()))
                self.assertNotIn("work_id", found["work"])
                self.assertEqual(self.runs, before)

    def test_a_missing_library_work_is_refused(self):
        self.library.clear()
        with self.assertRaisesRegex(ValueError, "not a work record"):
            self.resolve()

    def test_a_stale_group_name_is_refused(self):
        registry = self.registry()
        self.row["work"] = "Lost canonical title"
        with self.assertRaisesRegex(ValueError, "no harvested canonical work"):
            self.resolve(registry=registry)

    def test_a_reason_is_required(self):
        self.row["reason"] = ""
        with self.assertRaisesRegex(ValueError, "must all be stated"):
            self.resolve()

    def test_two_claims_for_one_group_are_refused(self):
        registry = self.registry()
        other = {**self.row, "work_id": "work.augustine.other"}
        self.library[other["work_id"]] = {"responsible": "Augustine"}
        with self.assertRaisesRegex(ValueError, "identified twice"):
            self.resolve(self.review([self.row, other]), registry)

    def test_two_groups_cannot_silently_become_one_library_work(self):
        registry = self.registry()
        self.runs[0]["passages"]["John 1"].append({
            "author": "Augustine", "title": "Different work",
            "role": "church-father", "death_year": 430,
        })
        other = {**self.row, "work": "Different work"}
        with self.assertRaisesRegex(ValueError, "identifies two harvested works"):
            self.resolve(self.review([self.row, other]), registry)

    def test_a_work_by_another_author_is_refused(self):
        self.library[self.row["work_id"]]["responsible"] = "John Chrysostom"
        with self.assertRaisesRegex(ValueError, "does not match the source-library author"):
            self.resolve()

    def test_a_declared_author_equivalence_is_honored(self):
        registry = self.registry()
        registry.authors = {"augustin": ("augustine", "Augustine")}
        self.library[self.row["work_id"]]["responsible"] = "Augustin"
        self.assertEqual(self.resolve(registry=registry), {
            ("augustine", harvest._fold(self.row["work"])): self.row["work_id"],
        })

    def test_review_of_a_single_title_work_does_not_require_an_alias_group(self):
        self.runs[0]["passages"]["John 1"][0].pop("aliases")
        self.row["work"] = "Tractates"
        registry = harvest._Registry()
        self.assertEqual(self.resolve(registry=registry), {
            ("augustine", "tractates"): self.row["work_id"],
        })
        self.assertEqual(registry, {})

    def test_promotion_and_mass_corpus_keep_the_reviewed_identity(self):
        registry = self.registry()
        groups, digest = harvest._derive_groups(self.runs, {})
        scratch = ROOT / ".scratch/resume-corpus-pipeline"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temp:
            folder = Path(temp)
            ledger, aliases, index = (folder / name for name in ("ledger.yaml", "aliases.yaml", "index.yaml"))
            ledger.write_text(yaml.safe_dump({"runs": self.runs}), encoding="utf-8")
            aliases.write_text(yaml.safe_dump({
                "schema": harvest.ALIAS_SCHEMA, "evidence_sha256": digest,
                "review": self.review(), "groups": groups,
            }), encoding="utf-8")
            args = argparse.Namespace(
                ledger=ledger, alias_table=aliases, index=index,
                min_confidence=0, audited_on="2026-10-23", dry_run=False,
            )
            with patch("_containment.catalog", return_value={"works": self.library}), \
                 patch.object(harvest, "_index_numbering_survey", return_value={}), \
                 patch.object(harvest, "_canonical_chapters", return_value=(("John", 21),)):
                payload = harvest.run_promote(args)
                payload["_commit"]()
                before = index.read_bytes()
                args.check = True
                args.audited_on = None
                self.assertEqual(harvest.run_promote(args)["status"], "current")
                changed = yaml.safe_load(aliases.read_text(encoding="utf-8"))
                changed["review"]["canonical_work_ids"] = []
                aliases.write_text(yaml.safe_dump(changed), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "missing or stale"):
                    harvest.run_promote(args)
                self.assertEqual(index.read_bytes(), before)
            work_index = harvest._work_index_tool()
            discovery = work_index._load_discovery(index)
            citation = {
                "book": "John", "ref": "John 1:1", "ranges": [{
                    "begin": {"chapter": 1, "verse": 1}, "end": {"chapter": 1, "verse": 1},
                }],
            }
            records = [{
                "calendar": "test", "mass_key": "sunday", "mass_name": "Sunday",
                "mass_kind": "seasonal", "date": "", "proper_slot": "Gospel",
                "numbering": "vulgate", "source_category": "base", "passage": citation,
            }]
            masses, _, unresolved, corpus, *_ = work_index._build_mass_coverage(
                work_index._load_citations_tool(), discovery, records, 20, 20,
            )
            self.assertEqual(unresolved, [])
            self.assertEqual(masses[0]["works"][0]["work_id"], self.row["work_id"])
            self.assertEqual(corpus[0]["work_id"], self.row["work_id"])
            self.assertEqual(masses[0]["works"][0]["confidence"], 1)


if __name__ == "__main__":
    unittest.main()
