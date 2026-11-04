"""Ordinary source maintenance checks every adopted chronology projection."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import shutil
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.tests.test_example_replay import make_reached

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _chronology as corpus

LOADER = importlib.machinery.SourceFileLoader(
    "chronology_freshness_preflight", str(ROOT / "tools/check-content-preflight"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
PREFLIGHT = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(PREFLIGHT)


def generated_leaves(root: Path) -> list[Path]:
    """Carrying either generated artifact adopts its currentness contract."""
    return sorted({path.parent.parent
                   for provider in ("gpt", "claude")
                   for name in ("chronology.toml", "chronology-annotations.tex")
                   for path in (root / "src" / provider).rglob(name)
                   if path.parent.name == "research"
                   and (path.parent.parent / "publication.toml").is_file()
                   and tomllib.loads((path.parent.parent / "publication.toml").read_text())
                   .get("kind") in ("proper-1962", "proper-postconciliar")})


class GeneratedProperChronologyFreshnessTests(unittest.TestCase):
    def test_source_maintenance_and_publication_reach_the_freshness_gate(self):
        makefile = (ROOT / "Makefile").read_text()
        for goal in ("check-sources", "check-deployment-sources", "public-site"):
            with self.subTest(goal=goal):
                reached = make_reached(goal, makefile)
                self.assertIn("check-proper-chronology-current", reached)
                self.assertIn("tools.tests.test_generated_proper_chronology_freshness",
                              reached["check-proper-chronology-current"])

    def test_every_adopted_record_and_annotation_is_current(self):
        leaves = generated_leaves(ROOT)
        self.assertTrue(leaves, "No generated chronology consumers discovered")
        for leaf in leaves:
            for name in ("chronology-record-current", "chronology-annotations-current"):
                with self.subTest(leaf=str(leaf.relative_to(ROOT)), check=name):
                    problems, _ = PREFLIGHT.CHECKS[name](leaf, ROOT)
                    self.assertEqual(problems, [])


class FreshnessRefusalTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/tests/generated-proper-chronology-freshness"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        relative = Path("src/claude/liturgy/roman-rite/1962/propers/temporal/"
                        "57-seventeenth-after-pentecost")
        self.leaf = self.root / relative
        shutil.copytree(ROOT / relative, self.leaf)
        (self.root / "src/sources").symlink_to(ROOT / "src/sources")

    def problems(self, name):
        return PREFLIGHT.CHECKS[name](self.leaf, self.root)[0]

    def test_an_altered_dossier_is_refused(self):
        path = self.leaf / "research/chronology.toml"
        text = path.read_text()
        self.assertIn('reigned from 1055 to 1015 B.C.', text)
        path.write_text(text.replace('reigned from 1055 to 1015 B.C.',
                                     'reigned from 1054 to 1015 B.C.'))
        self.assertTrue(self.problems("chronology-record-current"))

    def test_an_omitted_annotation_qualification_is_refused(self):
        path = self.leaf / "research/chronology-annotations.tex"
        text = path.read_text()
        self.assertIn("Occasion date unresolved.", text)
        path.write_text(text.replace("Occasion date unresolved.", "", 1))
        self.assertTrue(self.problems("chronology-annotations-current"))

    def test_a_changed_corpus_refuses_both_unchanged_consumer_artifacts(self):
        # Change an actual upstream claim while leaving the consumer intact.
        held = corpus.load()
        subject = "israel.monarchy.david-traditional-era"
        event = held.events[subject]
        claim = event.claims[0]
        changed = claim._replace(date=claim.date._replace(
            label="reigned from 1055 to 1015 B.C. (source qualification changed)"))
        events = dict(held.events)
        events[subject] = event._replace(claims=(changed, *event.claims[1:]))
        with patch.object(corpus, "load", return_value=held._replace(events=events)):
            for name in ("chronology-record-current", "chronology-annotations-current"):
                with self.subTest(check=name):
                    self.assertTrue(self.problems(name))

    def test_discovery_keeps_an_annotation_consumer_without_its_record(self):
        (self.leaf / "research/chronology.toml").unlink()
        self.assertEqual(generated_leaves(self.root), [self.leaf])
        self.assertTrue(self.problems("chronology-record-current"))

    def test_discovery_excludes_an_unrelated_genre_chronology_record(self):
        article = self.root / "src/gpt/articles/faith/example"
        (article / "research").mkdir(parents=True)
        (article / "publication.toml").write_text('kind = "article-faith"\n')
        (article / "research/chronology.toml").write_text('year = 1900\n')
        self.assertEqual(generated_leaves(self.root), [self.leaf])


if __name__ == "__main__":
    unittest.main()
