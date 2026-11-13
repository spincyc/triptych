"""Every document-type leaf assembles current content, and none is authored.

Like `tools/tpt document-types refresh --check`, the ordinary source gates
validate the live assembly of every opted-in leaf. Carried generated files are
optional snapshots; declarations, projection inputs, authored conflicts and
orphaned generated files remain checked by the assembly.
"""

from __future__ import annotations

import importlib.machinery
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
        for goal in ("check-sources", "check-deployment-sources", "public-site", "pages-site"):
            with self.subTest(goal=goal):
                reached = make_reached(goal, makefile)
                self.assertIn("check-generated-documents-current", reached)
                self.assertIn("tools.tests.test_generated_documents_freshness",
                              reached["check-generated-documents-current"])

    def test_every_opted_in_leaf_assembles_and_has_no_authored_copy(self):
        leaves = types.opted_in_leaves(ROOT)
        self.assertTrue(leaves, "no document-type consumers discovered")
        assembly = types.Assembly(ROOT)
        for leaf in leaves:
            with self.subTest(leaf=leaf.relative_to(ROOT).as_posix()):
                self.assertTrue(assembly.files(leaf), "an opted-in leaf assembles no files")


class EveryProperLeafIsOnADocumentTypeTests(unittest.TestCase):
    """The maintainer's decision of 2026-11-04: the Scriptural Date and
    Location page of every proper is generated, which needs every proper on a
    document type whose template places it."""

    def test_every_proper_leaf_declares_a_type_that_slots_the_date_page(self):
        found = types.discover_types(ROOT)
        import _document_schema  # noqa: PLC0415

        # A leaf's kind is derived from its path by the schema registry.
        leaves = [manifest.parent for provider in types.PROVIDERS
                  for manifest in sorted((ROOT / "src" / provider).rglob("publication.toml"))
                  if _document_schema.classify(ROOT, manifest.parent).startswith("proper-")]
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


class PrepareInputStateTests(unittest.TestCase):
    """`prepare` watches exactly what an rglob walk of the source trees sees.

    The walk runs once per Assembly, so it is a scandir walk; it must keep the
    rglob semantics: matching suffixes only, symlinked files followed,
    symlinked directories not descended, and a change to any watched file seen.
    """

    @staticmethod
    def rglob_state(root: Path) -> set:
        found = set()
        for tree, suffixes in date_page._WATCHED:
            for path in (root / "src/sources" / tree).rglob("*"):
                if path.suffix in suffixes and path.is_file():
                    stat = path.stat()
                    found.add((str(path), stat.st_dev, stat.st_ino, stat.st_size,
                               stat.st_mtime_ns, stat.st_ctime_ns))
        return found

    def test_the_walk_matches_rglob_and_sees_every_change(self):
        scratch = ROOT / ".scratch/tests/generated-documents"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temp:
            root = Path(temp)
            sources = root / "src/sources"
            for name, text in {
                "chronology/events/a.yaml": "a: 1\n", "chronology/notes.md": "not watched\n",
                "calendars/roman-1962/propers.yaml": "x: 1\n", "calendars/x.toml": "not watched\n",
                "bibles/drb/chapters/gen/1.json": "{}\n", "bibles/drb/index.yaml": "id: drb\n",
                "works/w/record.toml": "id = 'w'\n", "works/w/verse-text-x/a.tsv": "1\t2\n",
                "works/w/.hidden.toml": "id = 'h'\n", "elsewhere/ignored.yaml": "n: 1\n",
            }.items():
                (sources / name).parent.mkdir(parents=True, exist_ok=True)
                (sources / name).write_text(text)
            outside = root / "outside"
            outside.mkdir()
            (outside / "linked.toml").write_text("id = 'l'\n")
            (sources / "works/linked-file.toml").symlink_to(outside / "linked.toml")
            (sources / "works/linked-directory").symlink_to(outside, target_is_directory=True)
            state = date_page._input_state(root)
            self.assertEqual(list(state), sorted(state))
            self.assertEqual(set(state), self.rglob_state(root))
            self.assertEqual(len(state), 8)
            self.assertIn(str(sources / "works/linked-file.toml"), {row[0] for row in state})
            self.assertNotIn(str(sources / "works/linked-directory/linked.toml"),
                             {row[0] for row in state})
            (sources / "works/w/record.toml").write_text("id = 'changed'\n")
            self.assertNotEqual(date_page._input_state(root), state)
            (sources / "works/w/new.tsv").write_text("new\n")
            self.assertEqual(set(date_page._input_state(root)), self.rglob_state(root))


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
