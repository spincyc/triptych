"""Every document-type leaf's generated files are current, and none is authored.

`tools/tpt document-types refresh --check` is the one freshness check for
every projection a document-type template slots (the generated entrypoints and
deterministic pages such as the Scriptural Date and Location page). This module
runs it over every opted-in leaf from the ordinary source gates.
"""

from __future__ import annotations

import importlib.machinery
import re
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from tools.tests.test_example_replay import make_reached

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _document_types as types  # noqa: E402
from document_projections import scriptural_date_location as date_page  # noqa: E402

LOADER = importlib.machinery.SourceFileLoader(
    "generated_documents_preflight", str(ROOT / "tools/check-content-preflight"))
PREFLIGHT = importlib.util.module_from_spec(importlib.util.spec_from_loader(LOADER.name, LOADER))
LOADER.exec_module(PREFLIGHT)


class GeneratedDocumentsFreshnessTests(unittest.TestCase):
    def test_source_maintenance_and_publication_reach_the_gate(self):
        makefile = (ROOT / "Makefile").read_text()
        for goal in ("check-sources", "check-deployment-sources", "public-site"):
            with self.subTest(goal=goal):
                reached = make_reached(goal, makefile)
                self.assertIn("check-generated-documents-current", reached)
                self.assertIn("tools.tests.test_generated_documents_freshness",
                              reached["check-generated-documents-current"])

    def test_every_opted_in_leaf_is_current_and_has_no_authored_copy(self):
        for result in types.refresh(ROOT, types.opted_in_leaves(ROOT), check=True):
            with self.subTest(leaf=result.leaf):
                self.assertEqual(result.changed, (), "regenerate with tools/tpt document-types refresh")
                self.assertEqual(result.conflicts, (), "an authored date page remains")
                self.assertEqual(result.orphans, (), "a generated file nothing generates")


class EveryProperLeafIsOnADocumentTypeTests(unittest.TestCase):
    """The maintainer's decision of 2026-11-04: the Scriptural Date and
    Location page of every proper is generated, which needs every proper on a
    document type whose template places it."""

    def test_every_proper_leaf_declares_a_type_that_slots_the_date_page(self):
        found = types.discover_types(ROOT)
        leaves = [manifest.parent for provider in types.PROVIDERS
                  for manifest in sorted((ROOT / "src" / provider).rglob("publication.toml"))
                  if re.search(r'^kind = "proper-', manifest.read_text(), re.M)]
        self.assertTrue(leaves)
        for leaf in leaves:
            with self.subTest(leaf=str(leaf.relative_to(ROOT))):
                decl = types.declaration(ROOT, leaf, found)
                self.assertIsNotNone(decl, "a proper leaf without a [document] type")
                slots = {slot for name in decl.editions
                         for slot in types.render_edition(decl, name)[1]}
                self.assertTrue(any(slot.startswith("scriptural-date-location/") for slot in slots))


class AuthoredDatePageTests(unittest.TestCase):
    def conflicts(self, files: dict[str, str]) -> list[str]:
        scratch = ROOT / ".scratch/tests/generated-documents"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temp:
            leaf = Path(temp)
            for name, text in files.items():
                (leaf / name).parent.mkdir(parents=True, exist_ok=True)
                (leaf / name).write_text(text)
            context = types.LeafContext(ROOT, "claude", "x", leaf, "proper-1962", "proper-study-v1", ())
            return date_page.authored_conflicts(context, frozenset({"main.tex"}))

    def test_an_authored_heading_notes_or_table_import_is_refused(self):
        self.assertEqual(self.conflicts({
            "sections/80-date.tex": "\\section{Scriptural Date and Location}\n",
            "sections/70-history.tex": "\\section{Historical appendix: Scriptural Date and Location}\n",
            "sections/81-notes.tex": "\\paragraph{Setting notes.}\n",
            "sections/concise/03.tex": "\\input{x/research/chronology-table.tex}\n",
        }), ["sections/70-history.tex", "sections/80-date.tex", "sections/81-notes.tex",
             "sections/concise/03.tex"])

    def test_generated_research_comment_and_prose_mentions_are_not(self):
        self.assertEqual(self.conflicts({
            "main.tex": "\\input{x/research/chronology-table}\n",
            "generated/scriptural-date-location.tex": "\\section{Scriptural Date and Location}\n",
            "research/chronology-table.tex": "\\begin{chronologysharedtable}\n",
            "sections/90-apparatus.tex": "% \\section{Scriptural Date and Location}\n"
                                         "Every date in the Scriptural Date and Location appendix.\n",
        }), [])


class PreflightExemptionTests(unittest.TestCase):
    def test_only_an_opted_in_leafs_generated_pages_skip_the_prose_date_scan(self):
        scratch = ROOT / ".scratch/tests/generated-documents"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temp:
            leaf = Path(temp)
            page = leaf / "generated/scriptural-date-location.tex"
            page.parent.mkdir()
            page.write_text("A.D. 70\n")
            authored = leaf / "sections/80.tex"
            authored.parent.mkdir()
            authored.write_text("A.D. 70\n")
            (leaf / "publication.toml").write_text('kind = "proper-1962"\n')
            self.assertFalse(PREFLIGHT.generated_page(leaf, page), "not opted in: scanned")
            (leaf / "publication.toml").write_text('kind = "proper-1962"\n\n[document]\ntype = "x"\n')
            self.assertTrue(PREFLIGHT.generated_page(leaf, page))
            self.assertFalse(PREFLIGHT.generated_page(leaf, authored))


if __name__ == "__main__":
    unittest.main()
