from __future__ import annotations

import hashlib
import importlib.machinery
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import tomllib


ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools/source-family-migration"
SOURCE_INVENTORY = ROOT / "tools/source-inventory"
loader = importlib.machinery.SourceFileLoader("source_family_migration", str(TOOL))
spec = importlib.util.spec_from_loader(loader.name, loader)
assert spec is not None
MODULE = importlib.util.module_from_spec(spec)
loader.exec_module(MODULE)


class SourceFamilyMigrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.inventory = Path("src/sources/inventories/publications-v1.toml")
        self.review = Path(
            "src/sources/inventories/classification-review-v1.toml"
        )
        self.ledger = Path(
            "src/sources/inventories/source-family-migration-v1.toml"
        )
        self.audit = Path(
            "src/gpt/articles/faith/demo/research/source-audit.md"
        )
        self.write("src/gpt/articles/faith/demo/main.tex", "Demo\n")
        self.write(self.audit.as_posix(), "Augustine, City of God 19.13.\n")
        self.bootstrap_inventory()
        self.write_review()

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

    def run_inventory(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SOURCE_INVENTORY),
                "--root",
                str(self.root),
                *arguments,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def bootstrap_inventory(self) -> None:
        result = self.run_inventory(
            "bootstrap",
            self.inventory.as_posix(),
            "--audited-on",
            "2026-07-22",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def write_review(self) -> None:
        document = "articles/faith/demo"
        classifications = [
            {"document": document, "source_categories": ["patristic"]}
        ]
        publication_snapshot = hashlib.sha256(
            f"{document}\n".encode("utf-8")
        ).hexdigest()
        classification_snapshot = hashlib.sha256(
            json.dumps(
                classifications,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        self.write(
            self.review.as_posix(),
            "\n".join(
                [
                    "classification_schema = 1",
                    'record_type = "publication-source-classification-review"',
                    'audited_on = "2026-07-22"',
                    f'publication_snapshot = "sha256:{publication_snapshot}"',
                    f'classification_snapshot = "sha256:{classification_snapshot}"',
                    "",
                    "[[classifications]]",
                    f'document = "{document}"',
                    'source_categories = ["patristic"]',
                    "",
                ]
            ),
        )

    def bootstrap_ledger(self) -> None:
        result = self.run_tool(
            "bootstrap",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-22",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def ledger_data(self) -> dict:
        return tomllib.loads(
            (self.root / self.ledger).read_text(encoding="utf-8")
        )

    def write_ledger(self, data: dict) -> None:
        data["snapshot"] = MODULE._ledger_snapshot(data)
        (self.root / self.ledger).write_text(
            MODULE._render(data), encoding="utf-8"
        )

    def resnapshot_ledger_text(self, text: str) -> str:
        data = tomllib.loads(text)
        expected = MODULE._ledger_snapshot(data)
        return text.replace(data["snapshot"], expected, 1)

    def add_city_family(self, *, screened: bool = False) -> None:
        self.write(
            "src/sources/works/augustine/de-civitate-dei/work.toml",
            "\n".join(
                [
                    "schema = 1",
                    'record_type = "work"',
                    'id = "work.augustine.de-civitate-dei"',
                    'title = "De civitate Dei"',
                    'responsible = "Augustine of Hippo"',
                    'work_type = "patristic-treatise"',
                    'languages = ["la"]',
                    'description = "Fixture work for family-ledger validation."',
                    "",
                ]
            ),
        )
        data = self.ledger_data()
        data["canonical_catalog_snapshot"] = MODULE._canonical_catalog(self.root)[1]
        data["families"] = [
            {
                "id": "family.augustine.de-civitate-dei",
                "label": "Augustine, De civitate Dei",
                "kind": "work",
                "source_categories": ["patristic"],
                "identity_confidence": "confirmed",
                "identity_gaps": [],
                "artifact_availability": "canonicalized",
                "storage_plan": ["remote"],
                "rights_review": "all-known-artifacts-reviewed",
                "mutability": "fixed",
                "freshness_rule": "not-applicable",
                "evidence_ceiling": "bounded-corpus",
                "disposition": "bind-existing",
                "priority": "p0",
                "canonical_ids": ["work.augustine.de-civitate-dei"],
                "trace_patterns": ["City of God", "De civitate Dei"],
                "reviewed_on": "2026-07-22",
                "notes": "Fixture family.",
            }
        ]
        unit = data["review_units"][0]
        unit["family_presence"] = [
            {
                "family_id": "family.augustine.de-civitate-dei",
                "basis": "reviewed" if screened else "trace-scan",
                "record_paths": [self.audit.as_posix()],
            }
        ]
        if screened:
            unit["review_state"] = "family-screened"
            unit["reviewed_on"] = "2026-07-22"
            unit["family_screening_snapshot"] = MODULE._family_screening_snapshot(
                data["families"]
            )
        self.write_ledger(data)

    def add_future_work(self) -> str:
        work_id = "work.fixture.future-source"
        self.write(
            "src/sources/works/fixture/future-source/work.toml",
            "\n".join(
                [
                    "schema = 1",
                    'record_type = "work"',
                    f'id = "{work_id}"',
                    'title = "Future source"',
                    'responsible = "Fixture"',
                    'work_type = "reference-work"',
                    'languages = ["en"]',
                    'description = "Fixture work added after catalog review."',
                    "",
                ]
            ),
        )
        return work_id

    def test_bootstrap_is_pending_non_atomic_and_checkable(self) -> None:
        self.bootstrap_ledger()
        checked = self.run_tool("check", self.ledger.as_posix())
        strict = self.run_tool(
            "check", self.ledger.as_posix(), "--require-family-screened"
        )

        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertIn("review_units=1 screened=0 pending=1", checked.stdout)
        self.assertIn("atomic_citation_coverage=false", checked.stdout)
        self.assertEqual(strict.returncode, 1)
        self.assertIn("pending family review units", strict.stderr)
        data = self.ledger_data()
        self.assertIs(data["atomic_citation_coverage"], False)
        self.assertEqual(data["families"], [])

    def test_atomic_writes_create_and_preserve_collaborative_file_modes(self) -> None:
        self.bootstrap_ledger()
        path = self.root / self.ledger
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o644)
        os.chmod(path, 0o640)

        refreshed = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
        )

        self.assertEqual(refreshed.returncode, 0, refreshed.stderr)
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o640)

    def test_refresh_writer_refuses_to_overwrite_a_concurrent_ledger_edit(self) -> None:
        self.bootstrap_ledger()
        path = self.root / self.ledger
        expected = path.read_bytes()
        concurrent = expected + b"# concurrent reviewed edit\n"
        path.write_bytes(concurrent)

        with self.assertRaisesRegex(RuntimeError, "changed during refresh"):
            MODULE._write_atomic(
                path,
                expected.decode("utf-8"),
                expected_bytes=expected,
            )

        self.assertEqual(path.read_bytes(), concurrent)

    def test_rejects_atomic_coverage_even_with_a_fresh_snapshot(self) -> None:
        self.bootstrap_ledger()
        data = self.ledger_data()
        data["atomic_citation_coverage"] = True
        self.write_ledger(data)

        checked = self.run_tool("check", self.ledger.as_posix())

        self.assertEqual(checked.returncode, 1)
        self.assertIn("atomic_citation_coverage must be boolean false", checked.stderr)

    def test_rejects_changed_source_surface_before_inventory_refresh(self) -> None:
        self.bootstrap_ledger()
        before = (self.root / self.ledger).read_bytes()
        self.write(self.audit.as_posix(), "Changed City of God record.\n")

        checked = self.run_tool("check", self.ledger.as_posix())

        self.assertEqual(checked.returncode, 1)
        self.assertIn("sha256 is stale", checked.stderr)
        self.assertEqual((self.root / self.ledger).read_bytes(), before)

    def test_trace_presence_requires_owned_matching_record(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family()
        data = self.ledger_data()
        data["review_units"][0]["family_presence"][0]["record_paths"] = [
            "src/gpt/articles/faith/demo/main.tex"
        ]
        self.write_ledger(data)

        checked = self.run_tool("check", self.ledger.as_posix())

        self.assertEqual(checked.returncode, 1)
        self.assertIn("lacks a replayable trace", checked.stderr)

    def test_canonical_ids_must_resolve(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family()
        manifest = self.root / "src/sources/works/augustine/de-civitate-dei/work.toml"
        manifest.unlink()

        checked = self.run_tool("check", self.ledger.as_posix())

        self.assertEqual(checked.returncode, 1)
        self.assertIn("canonical_ids do not resolve", checked.stderr)

    def test_ledger_snapshot_covers_family_decisions(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family()
        path = self.root / self.ledger
        path.write_text(
            path.read_text(encoding="utf-8").replace('priority = "p0"', 'priority = "p1"'),
            encoding="utf-8",
        )

        checked = self.run_tool("check", self.ledger.as_posix())

        self.assertEqual(checked.returncode, 1)
        self.assertIn("snapshot is stale", checked.stderr)

    def test_bootstrap_rejects_an_audit_date_before_its_inputs(self) -> None:
        result = self.run_tool(
            "bootstrap",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-21",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot predate", result.stderr)
        self.assertFalse((self.root / self.ledger).exists())

    def test_refresh_rejects_a_backward_audit_date_without_writing(self) -> None:
        self.bootstrap_ledger()
        before = (self.root / self.ledger).read_bytes()

        refreshed = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-21",
        )

        self.assertEqual(refreshed.returncode, 1)
        self.assertIn("cannot predate", refreshed.stderr)
        self.assertEqual((self.root / self.ledger).read_bytes(), before)

    def test_refresh_marks_changed_unit_pending_and_keeps_only_known_trace(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family(screened=True)
        self.write(self.audit.as_posix(), "Augustine, City of God 19.13, refreshed.\n")
        new_path = "src/gpt/articles/faith/demo/research/new-source.md"
        self.write(new_path, "Another City of God trace.\n")
        self.bootstrap_inventory()

        refreshed = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
        )

        self.assertEqual(refreshed.returncode, 0, refreshed.stderr)
        data = self.ledger_data()
        unit = data["review_units"][0]
        self.assertEqual(unit["review_state"], "pending")
        self.assertNotIn("reviewed_on", unit)
        self.assertEqual(
            unit["family_presence"],
            [
                {
                    "family_id": "family.augustine.de-civitate-dei",
                    "basis": "trace-scan",
                    "record_paths": [self.audit.as_posix()],
                }
            ],
        )
        self.assertNotIn(new_path, unit["family_presence"][0]["record_paths"])
        checked = self.run_tool("check", self.ledger.as_posix())
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_refresh_preserves_a_family_after_its_last_trace_disappears(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family(screened=True)
        self.write(self.audit.as_posix(), "No recurring source-family trace remains.\n")
        self.bootstrap_inventory()

        refreshed = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
        )

        self.assertEqual(refreshed.returncode, 0, refreshed.stderr)
        data = self.ledger_data()
        self.assertEqual(
            [family["id"] for family in data["families"]],
            ["family.augustine.de-civitate-dei"],
        )
        unit = data["review_units"][0]
        self.assertEqual(unit["review_state"], "pending")
        self.assertNotIn("family_presence", unit)
        checked = self.run_tool("check", self.ledger.as_posix())
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_new_family_invalidates_prior_family_screening(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family(screened=True)
        data = self.ledger_data()
        data["families"].append(
            {
                "id": "family.future.unresolved",
                "label": "Future unresolved family",
                "kind": "work",
                "source_categories": ["patristic"],
                "identity_confidence": "unreviewed",
                "identity_gaps": ["work"],
                "artifact_availability": "citation-only",
                "storage_plan": ["unknown"],
                "rights_review": "unreviewed",
                "mutability": "unknown",
                "freshness_rule": "Reassess when the family identity is resolved.",
                "evidence_ceiling": "work-only",
                "disposition": "research-identity",
                "priority": "p2",
                "canonical_ids": [],
                "trace_patterns": ["Future unresolved family"],
                "reviewed_on": "2026-07-22",
                "notes": "Fixture family added after the unit review.",
            }
        )
        self.write_ledger(data)

        strict = self.run_tool(
            "check",
            self.ledger.as_posix(),
            "--require-family-screened",
        )
        self.assertEqual(strict.returncode, 1)
        self.assertIn("family_screening_snapshot is stale", strict.stderr)

        refreshed = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
        )
        self.assertEqual(refreshed.returncode, 0, refreshed.stderr)
        unit = self.ledger_data()["review_units"][0]
        self.assertEqual(unit["review_state"], "pending")
        self.assertNotIn("family_screening_snapshot", unit)
        checked = self.run_tool("check", self.ledger.as_posix())
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_malformed_types_fail_with_schema_errors_not_tracebacks(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family()
        path = self.root / self.ledger
        valid = path.read_text(encoding="utf-8")
        mutations = {
            "family id": (
                'id = "family.augustine.de-civitate-dei"',
                'id = ["family.augustine.de-civitate-dei"]',
            ),
            "identity confidence": (
                'identity_confidence = "confirmed"',
                'identity_confidence = ["confirmed"]',
            ),
            "canonical ids": (
                'canonical_ids = ["work.augustine.de-civitate-dei"]',
                'canonical_ids = [["work.augustine.de-civitate-dei"]]',
            ),
            "review state": (
                'review_state = "pending"',
                'review_state = ["pending"]',
            ),
            "presence basis": (
                'basis = "trace-scan"',
                'basis = ["trace-scan"]',
            ),
            "invalid trace regex": (
                'trace_patterns = ["City of God", "De civitate Dei"]',
                'trace_patterns = ["("]',
            ),
        }
        for label, (before, after) in mutations.items():
            with self.subTest(label=label):
                path.write_text(
                    self.resnapshot_ledger_text(valid.replace(before, after, 1)),
                    encoding="utf-8",
                )
                checked = self.run_tool("check", self.ledger.as_posix())
                self.assertEqual(checked.returncode, 1)
                self.assertIn("source-family-migration error:", checked.stderr)
                self.assertNotIn("Traceback", checked.stderr)

    def test_pinned_upstream_contracts_are_validated_not_only_hashed(self) -> None:
        self.bootstrap_ledger()
        cases = (
            (
                self.root / self.inventory,
                'record_type = "publication-source-inventory"',
                'record_type = "wrong-type"',
            ),
            (
                self.root / self.review,
                "classification_schema = 1",
                "classification_schema = 999",
            ),
        )
        for path, before, after in cases:
            with self.subTest(path=path.name):
                valid = path.read_text(encoding="utf-8")
                path.write_text(valid.replace(before, after, 1), encoding="utf-8")
                checked = self.run_tool("check", self.ledger.as_posix())
                self.assertEqual(checked.returncode, 1)
                self.assertIn("source-family-migration error:", checked.stderr)
                self.assertNotIn("Traceback", checked.stderr)
                path.write_text(valid, encoding="utf-8")

    def test_canonical_catalog_pin_covers_membership_and_manifest_content(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family()
        work = (
            self.root
            / "src/sources/works/augustine/de-civitate-dei/work.toml"
        )
        valid_work = work.read_text(encoding="utf-8")

        work.write_text(
            valid_work.replace(
                "Fixture work for family-ledger validation.",
                "Changed fixture work metadata.",
                1,
            ),
            encoding="utf-8",
        )
        changed = self.run_tool("check", self.ledger.as_posix())
        self.assertEqual(changed.returncode, 1)
        self.assertIn("pinned canonical_catalog_snapshot is stale", changed.stderr)
        work.write_text(valid_work, encoding="utf-8")

        self.add_future_work()
        added = self.run_tool("check", self.ledger.as_posix())
        self.assertEqual(added.returncode, 1)
        self.assertIn("pinned canonical_catalog_snapshot is stale", added.stderr)

    def test_canonical_catalog_accepts_each_supported_schema_type_pair(self) -> None:
        manifests = (
            (
                1,
                "work",
                "work.fixture.catalog-v1",
                "src/sources/works/fixture/catalog-v1/work.toml",
            ),
            (
                1,
                "edition",
                "edition.fixture.catalog-v1.one",
                "src/sources/works/fixture/catalog-v1/editions/one/edition.toml",
            ),
            (
                1,
                "artifact",
                "artifact.fixture.catalog-v1.one",
                "src/sources/works/fixture/catalog-v1/editions/one/artifacts/v1/artifact.toml",
            ),
            (
                1,
                "passage",
                "passage.fixture.catalog-v1.one",
                "src/sources/works/fixture/catalog-v1/editions/one/passages/v1.toml",
            ),
            (
                1,
                "corpus",
                "corpus.fixture.catalog-v1",
                "src/sources/corpora/catalog-v1.toml",
            ),
            (
                2,
                "artifact",
                "artifact.fixture.catalog-v2.one",
                "src/sources/works/fixture/catalog-v2/editions/one/artifacts/v2/artifact.toml",
            ),
            (
                2,
                "passage",
                "passage.fixture.catalog-v2.one",
                "src/sources/works/fixture/catalog-v2/editions/one/passages/v2.toml",
            ),
            (
                2,
                "segment",
                "segment.fixture.catalog-v2.one",
                "src/sources/works/fixture/catalog-v2/editions/one/segments/v2.toml",
            ),
        )
        for schema, record_type, record_id, relative in manifests:
            self.write(
                relative,
                "\n".join(
                    [
                        f"schema = {schema}",
                        f'record_type = "{record_type}"',
                        f'id = "{record_id}"',
                        "",
                    ]
                ),
            )

        found, _, errors = MODULE._canonical_catalog(self.root)

        self.assertEqual(errors, [])
        self.assertEqual(found, {record_id for _, _, record_id, _ in manifests})

    def test_canonical_catalog_rejects_unsupported_schema_type_pairs(self) -> None:
        cases = (
            (
                1,
                "segment",
                "src/sources/works/fixture/invalid/editions/one/segments/invalid.toml",
            ),
            (
                2,
                "work",
                "src/sources/works/fixture/invalid/work.toml",
            ),
            (
                2,
                "edition",
                "src/sources/works/fixture/invalid/editions/one/edition.toml",
            ),
            (
                2,
                "corpus",
                "src/sources/corpora/invalid.toml",
            ),
            (
                3,
                "artifact",
                "src/sources/works/fixture/invalid/editions/one/artifacts/invalid/artifact.toml",
            ),
        )
        for schema, record_type, relative in cases:
            with self.subTest(schema=schema, record_type=record_type):
                path = self.write(
                    relative,
                    "\n".join(
                        [
                            f"schema = {schema}",
                            f'record_type = "{record_type}"',
                            f'id = "{record_type}.fixture.invalid"',
                            "",
                        ]
                    ),
                )

                found, _, errors = MODULE._canonical_catalog(self.root)

                self.assertEqual(found, set())
                self.assertEqual(
                    errors,
                    [f"{path}: canonical source identity is malformed"],
                )
                path.unlink()

    def test_catalog_acceptance_requires_complete_reviewed_family_membership(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family()
        artifact_id = self.add_future_work()
        path = self.root / self.ledger
        before = path.read_bytes()

        ordinary = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
        )
        self.assertEqual(ordinary.returncode, 1)
        self.assertIn("pinned canonical_catalog_snapshot is stale", ordinary.stderr)
        self.assertEqual(path.read_bytes(), before)

        rejected = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
            "--accept-canonical-catalog",
        )
        self.assertEqual(rejected.returncode, 1)
        self.assertIn("lack reviewed family membership", rejected.stderr)
        self.assertEqual(path.read_bytes(), before)

        data = self.ledger_data()
        data["families"][0]["canonical_ids"].append(artifact_id)
        data["families"][0]["canonical_ids"].sort()
        data["families"][0]["reviewed_on"] = "2026-07-23"
        path.write_text(MODULE._render(data), encoding="utf-8")
        accepted = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
            "--accept-canonical-catalog",
        )
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        checked = self.run_tool("check", self.ledger.as_posix())
        self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_catalog_acceptance_with_no_families_preserves_pending_claim(self) -> None:
        self.bootstrap_ledger()
        self.add_future_work()

        ordinary = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
        )
        self.assertEqual(ordinary.returncode, 1)
        self.assertIn("pinned canonical_catalog_snapshot is stale", ordinary.stderr)

        accepted = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
            "--accept-canonical-catalog",
        )
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        checked = self.run_tool("check", self.ledger.as_posix())
        self.assertEqual(checked.returncode, 0, checked.stderr)
        data = self.ledger_data()
        self.assertEqual(data["families"], [])
        self.assertTrue(
            all(unit["review_state"] == "pending" for unit in data["review_units"])
        )

    def test_catalog_acceptance_seals_reviewed_manifest_content_changes(self) -> None:
        self.bootstrap_ledger()
        self.add_city_family()
        work = (
            self.root
            / "src/sources/works/augustine/de-civitate-dei/work.toml"
        )
        work.write_text(
            work.read_text(encoding="utf-8").replace(
                "Fixture work for family-ledger validation.",
                "Reviewed fixture work metadata.",
                1,
            ),
            encoding="utf-8",
        )
        data = self.ledger_data()
        data["families"][0]["reviewed_on"] = "2026-07-23"
        (self.root / self.ledger).write_text(
            MODULE._render(data),
            encoding="utf-8",
        )

        accepted = self.run_tool(
            "refresh",
            self.ledger.as_posix(),
            "--audited-on",
            "2026-07-23",
            "--accept-canonical-catalog",
        )

        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        checked = self.run_tool("check", self.ledger.as_posix())
        self.assertEqual(checked.returncode, 0, checked.stderr)


if __name__ == "__main__":
    unittest.main()
