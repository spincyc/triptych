"""Ordinary source maintenance checks every adopted chronology projection."""

from __future__ import annotations

import importlib.machinery
import importlib.util
import argparse
import shutil
import sys
import tempfile
import tomllib
import unittest
import yaml
from pathlib import Path
from unittest.mock import patch

from tools.tests.test_example_replay import make_reached

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _chronology as corpus
import _document_types as document_types

LOADER = importlib.machinery.SourceFileLoader(
    "chronology_freshness_preflight", str(ROOT / "tools/check-content-preflight"))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
PREFLIGHT = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(PREFLIGHT)


def generated_leaves(root: Path) -> list[Path]:
    """Typed assemblies need no carried artifact; legacy adopters still do."""
    carried = {path.parent.parent
                   for provider in ("gpt", "claude")
                   for name in ("chronology.toml", "chronology-annotations.tex")
                   for path in (root / "src" / provider).rglob(name)
                   if path.parent.name == "research"
                   and (path.parent.parent / "publication.toml").is_file()
                   and _kind(root, path.parent.parent) in ("proper-1962", "proper-postconciliar")}
    typed = {leaf for leaf in document_types.opted_in_leaves(root)
             if _kind(root, leaf) in ("proper-1962", "proper-postconciliar")}
    return sorted(carried | typed)


def _kind(root: Path, leaf: Path) -> str | None:
    """The registered kind of a leaf, which its path determines."""
    import _document_schema

    try:
        return _document_schema.classify(root, leaf)
    except _document_schema.SchemaError:
        return None


class GeneratedProperChronologyFreshnessTests(unittest.TestCase):
    def test_source_maintenance_and_publication_reach_the_freshness_gate(self):
        makefile = (ROOT / "Makefile").read_text()
        for goal in ("check-sources", "check-deployment-sources", "public-site", "pages-site"):
            with self.subTest(goal=goal):
                reached = make_reached(goal, makefile)
                self.assertIn("check-proper-chronology-current", reached)
                self.assertIn("tools.tests.test_generated_proper_chronology_freshness",
                              reached["check-proper-chronology-current"])

    def test_every_adopted_projection_and_authored_claim_is_current(self):
        leaves = generated_leaves(ROOT)
        self.assertTrue(leaves, "No generated chronology consumers discovered")
        for leaf in leaves:
            for name in ("chronology-record-current", "chronology-annotations-current",
                         "chronology-claims-supported"):
                with self.subTest(leaf=str(leaf.relative_to(ROOT)), check=name):
                    problems, _ = PREFLIGHT.CHECKS[name](leaf, ROOT)
                    self.assertEqual(problems, [])


class FreshnessFixture(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/assembly-gates"
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


class FreshnessRefusalTests(FreshnessFixture):
    def setUp(self):
        super().setUp()
        # Legacy consumers have no shared assembly to supersede their copies.
        path = self.leaf / "publication.toml"
        path.write_text(path.read_text().split("[document]", 1)[0])

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


class AssemblyFreshnessTests(FreshnessFixture):
    def setUp(self):
        super().setUp()
        (self.root / "src/common").symlink_to(ROOT / "src/common")
        (self.root / "guidance").symlink_to(ROOT / "guidance")

    def assert_current(self):
        for name in ("chronology-record-current", "chronology-annotations-current",
                     "chronology-claims-supported"):
            with self.subTest(check=name):
                self.assertEqual(self.problems(name), [])

    def test_missing_snapshots_use_the_live_assembly_without_writing(self):
        assembly = document_types.Assembly(self.root)
        generated = assembly.files(self.leaf)
        for path in generated:
            path.unlink(missing_ok=True)
        self.assertEqual(generated_leaves(self.root), [self.leaf])
        self.assert_current()
        self.assertTrue(all(not path.exists() for path in generated))

    def test_stale_snapshots_do_not_replace_current_shared_content(self):
        generated = document_types.Assembly(self.root).files(self.leaf)
        for path in generated:
            path.write_text("Stale generated snapshot.\n")
        self.assert_current()
        self.assertTrue(all(path.read_text() == "Stale generated snapshot.\n" for path in generated))

    def test_changed_corpus_reaches_checks_without_refreshing_snapshots(self):
        held = corpus.load()
        subject = "israel.monarchy.david-traditional-era"
        event = held.events[subject]
        claim = event.claims[0]
        changed = claim._replace(date=claim.date._replace(
            label="reigned from 1055 to 1015 B.C. (source qualification changed)"))
        events = dict(held.events)
        events[subject] = event._replace(claims=(changed, *event.claims[1:]))
        before = (self.leaf / "research/chronology.toml").read_bytes()
        with patch.object(corpus, "load", return_value=held._replace(events=events)):
            self.assert_current()
            rendered = document_types.Assembly(self.root).read_text(self.leaf / "research/chronology.toml")
            self.assertIn("source qualification changed", rendered)
        self.assertEqual((self.leaf / "research/chronology.toml").read_bytes(), before)

    def test_authored_unsupported_claim_remains_refused(self):
        path = self.leaf / "sections/00-opening.tex"
        path.write_text(path.read_text() + r"\chronology{invented.subject}{composition}{A.D. 999}" + "\n")
        self.assertTrue(self.problems("chronology-claims-supported"))

    def test_authored_date_page_cannot_hide_behind_fresh_assembly(self):
        path = self.leaf / "sections/duplicate-dates.tex"
        path.write_text(r"\section*{Scriptural Date and Location}" + "\n")
        for name in ("chronology-record-current", "chronology-annotations-current",
                     "chronology-claims-supported"):
            with self.subTest(check=name), self.assertRaisesRegex(ValueError, "authored generated content"):
                self.problems(name)

    def test_wrong_scope_is_not_treated_as_an_absent_projection(self):
        path = self.leaf / "research/chronology-profile-comparisons.toml"
        text = path.read_text()
        document = self.leaf.relative_to(self.root / "src/claude").as_posix()
        path.write_text(text.replace(document, "liturgy/roman-rite/1962/propers/temporal/58-eighteenth-after-pentecost"))
        with self.assertRaises(ValueError):
            self.problems("chronology-record-current")

    def test_malformed_shared_corpus_is_refused(self):
        sources = self.root / "src/sources"
        sources.unlink()
        sources.mkdir()
        for path in (ROOT / "src/sources").iterdir():
            if path.name == "chronology":
                shutil.copytree(path, sources / path.name)
            else:
                (sources / path.name).symlink_to(path)
        (sources / "chronology/profiles.yaml").write_text("profiles: [\n")
        with self.assertRaises((ValueError, yaml.YAMLError)):
            self.problems("chronology-record-current")

    def test_missing_appointment_input_remains_explicitly_pending(self):
        # Appointment ownership forbids symlink aliases outside the root.
        (self.root / "guidance").unlink()
        registry = Path("guidance/liturgy/postconciliar-propers-registry.md")
        (self.root / registry).parent.mkdir(parents=True)
        shutil.copyfile(ROOT / registry, self.root / registry)
        relative = Path("src/gpt/liturgy/roman-rite/postconciliar/"
                        "roman-missal-third-edition-en-us-2011/propers/temporal/"
                        "pc-s42-sixteenth-sunday-in-ordinary-time-year-a")
        leaf = self.root / relative
        shutil.copytree(ROOT / relative, leaf)
        (leaf / "research/chronology-inputs.toml").unlink(missing_ok=True)
        assembly = document_types.Assembly(self.root)
        files = assembly.files(leaf)
        page = files[leaf / "generated/scriptural-date-location-sheet.tex"]
        self.assertIn("research pending", page)
        self.assertNotIn(leaf / "research/chronology.toml", files)
        for name in ("chronology-record-current", "chronology-annotations-current"):
            with self.subTest(check=name):
                self.assertEqual(PREFLIGHT.CHECKS[name](leaf, self.root)[0], [])

    def test_unavailable_ritual_formulary_does_not_acquire_dates(self):
        relative = Path("src/gpt/liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass")
        leaf = self.root / relative
        shutil.copytree(ROOT / relative, leaf)
        files = document_types.Assembly(self.root).files(leaf)
        self.assertIn("carry no formulary", files[leaf / "generated/scriptural-date-location-sheet.tex"])
        self.assertNotIn(leaf / "research/chronology-table.tex", files)
        self.assertEqual(PREFLIGHT.CHECKS["chronology-record-current"](leaf, self.root)[0], [])
        self.assertEqual(PREFLIGHT.CHECKS["chronology-claims-supported"](
            leaf, self.root, "research")[0], [])

    def test_refresh_check_validates_live_assembly_without_rewriting(self):
        loader = importlib.machinery.SourceFileLoader(
            "assembly_document_types_cli", str(ROOT / "tools/document-types"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cli = importlib.util.module_from_spec(spec)
        loader.exec_module(cli)
        path = self.leaf / "research/chronology.toml"
        path.write_text("stale snapshot\n")
        args = argparse.Namespace(all=False, check=True,
                                  leaf=[self.leaf.relative_to(self.root / "src").as_posix()])
        with patch.object(cli, "ROOT", self.root):
            self.assertEqual(cli.refresh_verb(args)["status"], "ok")
        self.assertEqual(path.read_text(), "stale snapshot\n")


if __name__ == "__main__":
    unittest.main()
