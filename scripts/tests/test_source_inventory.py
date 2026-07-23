from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "scripts/source-inventory"


class SourceInventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.write("src/gpt/articles/faith/demo/main.tex", "Demo\n")
        self.write(
            "src/gpt/articles/faith/demo/research/source-audit.md",
            "# Legacy audit\n\nA source record.\n",
        )
        self.inventory = Path("src/sources/inventories/publications-v1.toml")

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_tool(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOL), "--root", str(self.root), *arguments],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def bootstrap(self) -> None:
        result = self.run_tool(
            "bootstrap", self.inventory.as_posix(), "--audited-on", "2026-07-22"
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_bootstrap_and_check_minimal_inventory(self) -> None:
        self.bootstrap()
        first = self.run_tool("check", self.inventory.as_posix())
        second = self.run_tool("check", self.inventory.as_posix())

        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(
            first.stdout,
            "source-inventory valid: publications=1 source_surface_files=2 owners=0\n",
        )

    def test_check_rejects_missing_publication_and_source_file(self) -> None:
        self.bootstrap()
        self.write("src/gpt/theology/new/main.tex", "New\n")
        self.write("src/gpt/theology/new/research/scope.md", "# Scope\n")

        result = self.run_tool("check", self.inventory.as_posix())

        self.assertEqual(result.returncode, 1)
        self.assertIn("publications missing from inventory: theology/new", result.stderr)
        self.assertIn("source-bearing files missing from inventory", result.stderr)

    def test_check_rejects_stale_file_hash(self) -> None:
        self.bootstrap()
        self.write(
            "src/gpt/articles/faith/demo/research/source-audit.md",
            "# Changed legacy audit\n",
        )

        result = self.run_tool("check", self.inventory.as_posix())

        self.assertEqual(result.returncode, 1)
        self.assertIn("sha256 is stale", result.stderr)

    def test_check_rejects_changed_inheritance_rule(self) -> None:
        self.bootstrap()
        path = self.root / self.inventory
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace('source_mode = "local"', 'source_mode = "inherited"', 1),
            encoding="utf-8",
        )

        result = self.run_tool("check", self.inventory.as_posix())

        self.assertEqual(result.returncode, 1)
        self.assertIn("source_mode does not match explicit ownership rules", result.stderr)

    def test_check_reports_native_toml_types_without_crashing(self) -> None:
        self.bootstrap()
        path = self.root / self.inventory
        text = path.read_text(encoding="utf-8")
        path.write_text(
            text.replace('source_mode = "local"', "source_mode = 2026-07-22", 1),
            encoding="utf-8",
        )

        result = self.run_tool("check", self.inventory.as_posix())

        self.assertEqual(result.returncode, 1)
        self.assertIn("source_mode is invalid", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_bootstrap_rejects_source_file_without_explicit_owner(self) -> None:
        self.write("src/gpt/unowned/shared/source-notes.tex", "Notes\n")

        result = self.run_tool(
            "bootstrap", self.inventory.as_posix(), "--audited-on", "2026-07-22"
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("source-bearing file has no explicit owner", result.stderr)
        self.assertFalse((self.root / self.inventory).exists())


if __name__ == "__main__":
    unittest.main()
