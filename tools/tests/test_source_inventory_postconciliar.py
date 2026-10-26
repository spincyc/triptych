"""General-calendar studies participate in the existing edition-owned inventory."""

from __future__ import annotations

import os
import runpy
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools/source-inventory"
EDITION_ROOT = ("liturgy/roman-rite/postconciliar/"
                "roman-missal-third-edition-en-us-2011/propers")
DOCUMENT = f"{EDITION_ROOT}/general-calendar/pc-r07-all-saints-abc"
SHARED = f"{EDITION_ROOT}/general-calendar/shared/formularies/pc-r07-all-saints/propers/verified.md"
OWNER = "owner.liturgy.roman-rite.postconciliar.roman-missal-third-edition-en-us-2011-propers"
TEMPORAL = f"{EDITION_ROOT}/temporal/pc-s51-twenty-fifth-sunday-in-ordinary-time-year-a"


class PostconciliarSourceInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tool = runpy.run_path(str(TOOL))

    def setUp(self):
        scratch = ROOT / ".scratch/pc-r-workflow-support/inventory"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_tool(self, *arguments):
        result = subprocess.run([sys.executable, str(TOOL), "--root", str(self.root),
                                 *arguments], cwd=ROOT, capture_output=True,
                                text=True, check=False, env={**os.environ, "PROVIDER": "gpt"})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def edition(self, provider):
        # Existing edition roots precede PC-R production; their recorded owner
        # must remain refreshable without creating new roots in both providers.
        for suffix in ("registry", "shared", "temporal/shared"):
            self.write(f"src/{provider}/{EDITION_ROOT}/{suffix}/README.md", "Edition evidence.\n")
        self.write(f"src/{provider}/{TEMPORAL}/main.tex", "Temporal study.\n")

    def replacement(self, provider):
        self.write(f"src/{provider}/{DOCUMENT}/main.tex", "Replacement study.\n")
        self.write(f"src/{provider}/{DOCUMENT}/instance/manifest.md", "Instance audit.\n")
        self.write(f"src/{provider}/{SHARED}", "Canonical replacement formulary audit.\n")

    def review(self, path, documents):
        self.write(path, self.tool["_render_classification_review"](
            documents, "2026-10-25", {document: ["liturgical", "scripture"] for document in documents}))

    def test_bootstrap_discovers_replacement_and_edition_owner_for_each_provider(self):
        for provider in ("gpt", "claude"):
            self.edition(provider)
            self.replacement(provider)
        for provider in ("gpt", "claude"):
            with self.subTest(provider=provider):
                inventory_path = f"inventories/{provider}.toml"
                self.run_tool("bootstrap", inventory_path, "--provider", provider,
                              "--audited-on", "2026-10-25")
                data = tomllib.loads((self.root / inventory_path).read_text())
                row = next(row for row in data["documents"] if row["id"] == DOCUMENT)
                self.assertEqual((row["source_mode"], row["publication_kind"]),
                                 ("mixed", "proper-instance"))
                self.assertEqual(row["record_owners"], [
                    {"id": DOCUMENT, "relationship": "local"},
                    {"id": OWNER, "relationship": "source-owner"}])
                source = next(row for row in data["files"] if row["path"] == f"src/{provider}/{SHARED}")
                self.assertEqual((source["owners"], source["kind"]), ([OWNER], "proper-verification"))
                self.assertTrue(all(row["path"].startswith(f"src/{provider}/") for row in data["files"]))
                self.run_tool("check", inventory_path)

    def test_refresh_migrates_previous_owner_roots_and_preserves_other_provider(self):
        for provider in ("gpt", "claude"):
            self.edition(provider)
            inventory_path, review_path = f"inventories/{provider}.toml", f"inventories/{provider}-review.toml"
            self.run_tool("bootstrap", inventory_path, "--provider", provider,
                          "--audited-on", "2026-10-25")
            self.review(review_path, [TEMPORAL])
            self.run_tool("classify", inventory_path, "--review", review_path)
            data = tomllib.loads((self.root / inventory_path).read_text())
            owner = next(row for row in data["owners"] if row["id"] == OWNER)
            self.assertNotIn(f"src/{provider}/{EDITION_ROOT}/general-calendar/shared", owner["roots"])
        self.replacement("gpt")
        self.run_tool("refresh", "inventories/gpt.toml", "--review", "inventories/gpt-review.toml",
                      "--audited-on", "2026-10-25")
        data = tomllib.loads((self.root / "inventories/gpt.toml").read_text())
        owner = next(row for row in data["owners"] if row["id"] == OWNER)
        self.assertIn(f"src/gpt/{EDITION_ROOT}/general-calendar/shared", owner["roots"])
        row = next(row for row in data["documents"] if row["id"] == DOCUMENT)
        self.assertEqual((row["source_mode"], row["publication_kind"], row["source_categories"]),
                         ("mixed", "proper-instance", ["unresolved"]))
        self.review("inventories/gpt-review.toml", [TEMPORAL, DOCUMENT])
        self.run_tool("classify", "inventories/gpt.toml", "--review", "inventories/gpt-review.toml")
        self.run_tool("check", "inventories/gpt.toml", "--review", "inventories/gpt-review.toml")
        self.run_tool("check", "inventories/claude.toml", "--review", "inventories/claude-review.toml")

    def test_unknown_shared_roots_and_cross_provider_files_remain_unowned(self):
        for relative in (
            SHARED.replace("general-calendar/shared/", "general-calendar/sharedness/"),
            SHARED.replace("general-calendar/shared/", "unknown-calendar/shared/"),
            SHARED.replace("en-us-2011", "en-gb-2011"),
        ):
            with self.subTest(relative=relative):
                self.assertIsNone(self.tool["_owner_for_file"](f"src/gpt/{relative}", [DOCUMENT], "gpt"))
        self.assertIsNone(self.tool["_owner_for_file"](f"src/claude/{SHARED}", [DOCUMENT], "gpt"))
        self.edition("gpt")
        self.write(f"src/gpt/{SHARED.replace('general-calendar/shared/', 'general-calendar/sharedness/')}",
                   "Unowned source.\n")
        result = subprocess.run([sys.executable, str(TOOL), "--root", str(self.root), "bootstrap",
                                 "inventories/refused.toml", "--audited-on", "2026-10-25"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("source-bearing file has no explicit owner", result.stderr)
        self.assertFalse((self.root / "inventories/refused.toml").exists())

    def test_legacy_refresh_exception_does_not_accept_other_owner_changes(self):
        self.edition("gpt")
        self.run_tool("bootstrap", "inventories/gpt.toml", "--provider", "gpt",
                      "--audited-on", "2026-10-25")
        self.review("inventories/gpt-review.toml", [TEMPORAL])
        self.run_tool("classify", "inventories/gpt.toml", "--review", "inventories/gpt-review.toml")
        path = self.root / "inventories/gpt.toml"
        data = tomllib.loads(path.read_text())
        owner = next(row for row in data["owners"] if row["id"] == OWNER)
        owner["roots"].remove(f"src/gpt/{EDITION_ROOT}/temporal/shared")
        data["snapshot"] = self.tool["_snapshot"](data["documents"], data["owners"], data["files"])
        path.write_text(self.tool["_render"](data))
        before = path.read_bytes()
        result = subprocess.run([sys.executable, str(TOOL), "--root", str(self.root), "refresh",
                                 "inventories/gpt.toml", "--review", "inventories/gpt-review.toml",
                                 "--audited-on", "2026-10-25"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not match explicit ownership rules", result.stderr)
        self.assertEqual(path.read_bytes(), before)

    def test_only_single_pc_r_leaves_receive_the_general_calendar_owner_edge(self):
        for document in (
            DOCUMENT.replace("pc-r07", "pc-s07"), DOCUMENT.replace("pc-r07", "pc-r7"),
            DOCUMENT + "/nested", DOCUMENT.replace("general-calendar/", "unknown-calendar/"),
            DOCUMENT.replace("en-us-2011", "en-gb-2011"),
        ):
            with self.subTest(document=document):
                mode, edges, kind = self.tool["_document_shape"](document, "gpt")
                self.assertEqual((mode, edges, kind),
                                 ("local", [{"id": document, "relationship": "local"}], "canonical"))
        mode, edges, kind = self.tool["_document_shape"](TEMPORAL, "gpt")
        self.assertEqual((mode, kind), ("mixed", "proper-instance"))
        self.assertIn({"id": OWNER, "relationship": "source-owner"}, edges)
        ritual = "liturgy/roman-rite/1962/propers/ritual/m01-nuptial-mass"
        self.assertIn({"id": "theology/sacraments", "relationship": "render-import"},
                      self.tool["_document_shape"](ritual, "gpt")[1])


if __name__ == "__main__":
    unittest.main()
