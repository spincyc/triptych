from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import tomllib


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
        self.review = Path(
            "src/sources/inventories/classification-review-v1.toml"
        )

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

    def write_review(
        self,
        documents: list[str],
        categories: dict[str, list[str]] | None = None,
    ) -> None:
        documents = sorted(documents)
        categories = categories or {
            document: ["magisterial", "patristic", "scholastic", "scripture", "secondary"]
            for document in documents
        }
        classifications = [
            {
                "document": document,
                "source_categories": sorted(categories[document]),
            }
            for document in documents
        ]
        snapshot = hashlib.sha256(
            "".join(f"{document}\n" for document in documents).encode("utf-8")
        ).hexdigest()
        classification_snapshot = hashlib.sha256(
            json.dumps(
                classifications,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        rows = []
        for classification in classifications:
            quoted_categories = ", ".join(
                f'"{category}"'
                for category in classification["source_categories"]
            )
            rows.extend(
                [
                    "",
                    "[[classifications]]",
                    f'document = "{classification["document"]}"',
                    f"source_categories = [{quoted_categories}]",
                ]
            )
        self.write(
            self.review.as_posix(),
            "\n".join(
                [
                    "classification_schema = 1",
                    'record_type = "publication-source-classification-review"',
                    'audited_on = "2026-07-22"',
                    f'publication_snapshot = "sha256:{snapshot}"',
                    f'classification_snapshot = "sha256:{classification_snapshot}"',
                    *rows,
                    "",
                ]
            ),
        )

    def resnapshot_inventory(self, text: str) -> str:
        data = tomllib.loads(text)
        payload = {
            "documents": data["documents"],
            "owners": data["owners"],
            "files": data["files"],
        }
        snapshot = hashlib.sha256(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        return text.replace(data["snapshot"], f"sha256:{snapshot}", 1)

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

    def test_classify_records_reviewed_strata_and_replays(self) -> None:
        self.bootstrap()
        self.write_review(
            ["articles/faith/demo"],
            {"articles/faith/demo": ["secondary"]},
        )
        classified = self.run_tool(
            "classify",
            self.inventory.as_posix(),
            "--review",
            self.review.as_posix(),
        )

        self.assertEqual(classified.returncode, 0, classified.stderr)
        text = (self.root / self.inventory).read_text(encoding="utf-8")
        self.assertIn('inventory_state = "sources-categorized"', text)
        self.assertIn('source_categories = ["secondary"]', text)
        self.assertNotIn('"magisterial"', text)
        self.assertEqual(
            self.run_tool("check", self.inventory.as_posix()).returncode,
            0,
        )

    def test_classification_bootstrap_requires_semantic_review(self) -> None:
        generated = self.run_tool(
            "bootstrap-classification-review",
            self.review.as_posix(),
            "--audited-on",
            "2026-07-22",
        )
        self.assertEqual(generated.returncode, 0, generated.stderr)
        review = tomllib.loads(
            (self.root / self.review).read_text(encoding="utf-8")
        )
        self.assertEqual(
            review["classifications"],
            [
                {
                    "document": "articles/faith/demo",
                    "source_categories": ["unresolved"],
                }
            ],
        )
        self.bootstrap()
        classified = self.run_tool(
            "classify",
            self.inventory.as_posix(),
            "--review",
            self.review.as_posix(),
        )
        self.assertEqual(classified.returncode, 1)
        self.assertIn("source_categories must be resolved", classified.stderr)

    def test_classification_refresh_preserves_reviewed_rows(self) -> None:
        self.write_review(
            ["articles/faith/demo"],
            {"articles/faith/demo": ["secondary"]},
        )
        self.write("src/gpt/articles/faith/future-study/main.tex", "Future\n")

        refreshed = self.run_tool(
            "bootstrap-classification-review",
            self.review.as_posix(),
            "--audited-on",
            "2026-07-23",
        )

        self.assertEqual(refreshed.returncode, 0, refreshed.stderr)
        review = tomllib.loads(
            (self.root / self.review).read_text(encoding="utf-8")
        )
        self.assertEqual(review["audited_on"], "2026-07-23")
        self.assertEqual(
            review["classifications"],
            [
                {
                    "document": "articles/faith/demo",
                    "source_categories": ["secondary"],
                },
                {
                    "document": "articles/faith/future-study",
                    "source_categories": ["unresolved"],
                },
            ],
        )

    def test_classify_fails_closed_for_an_unreviewed_collection(self) -> None:
        self.write("src/gpt/articles/faith/future-study/main.tex", "Demo\n")
        self.bootstrap()
        self.write_review(["articles/faith/demo"])
        before = (self.root / self.inventory).read_bytes()

        classified = self.run_tool(
            "classify",
            self.inventory.as_posix(),
            "--review",
            self.review.as_posix(),
        )

        self.assertEqual(classified.returncode, 1)
        self.assertIn("publications lack classification review", classified.stderr)
        self.assertEqual((self.root / self.inventory).read_bytes(), before)

    def test_classify_rejects_a_stale_category_snapshot(self) -> None:
        self.bootstrap()
        self.write_review(["articles/faith/demo"])
        path = self.root / self.review
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                '"magisterial", ', "", 1
            ),
            encoding="utf-8",
        )
        before = (self.root / self.inventory).read_bytes()

        classified = self.run_tool(
            "classify",
            self.inventory.as_posix(),
            "--review",
            self.review.as_posix(),
        )

        self.assertEqual(classified.returncode, 1)
        self.assertIn("classification_snapshot is stale", classified.stderr)
        self.assertEqual((self.root / self.inventory).read_bytes(), before)

    def test_check_rejects_inventory_categories_diverging_from_review(self) -> None:
        self.bootstrap()
        self.write_review(["articles/faith/demo"])
        classified = self.run_tool(
            "classify",
            self.inventory.as_posix(),
            "--review",
            self.review.as_posix(),
        )
        self.assertEqual(classified.returncode, 0, classified.stderr)
        path = self.root / self.inventory
        text = path.read_text(encoding="utf-8").replace(
            '"magisterial", ', "", 1
        )
        path.write_text(self.resnapshot_inventory(text), encoding="utf-8")

        checked = self.run_tool(
            "check",
            self.inventory.as_posix(),
            "--review",
            self.review.as_posix(),
        )

        self.assertEqual(checked.returncode, 1)
        self.assertIn("inventory categories diverge", checked.stderr)

    def test_classify_preserves_later_migration_state(self) -> None:
        self.bootstrap()
        self.write_review(["articles/faith/demo"])
        first = self.run_tool(
            "classify",
            self.inventory.as_posix(),
            "--review",
            self.review.as_posix(),
        )
        self.assertEqual(first.returncode, 0, first.stderr)
        path = self.root / self.inventory
        text = path.read_text(encoding="utf-8").replace(
            'inventory_state = "sources-categorized"',
            'inventory_state = "partially-migrated"',
            1,
        )
        path.write_text(self.resnapshot_inventory(text), encoding="utf-8")

        second = self.run_tool(
            "classify",
            self.inventory.as_posix(),
            "--review",
            self.review.as_posix(),
        )

        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn(
            'inventory_state = "partially-migrated"',
            path.read_text(encoding="utf-8"),
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
