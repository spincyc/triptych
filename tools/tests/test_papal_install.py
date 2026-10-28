"""Durable releases keep exact reviewed bytes and refuse stale withdrawals."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _papal_collection as collection
import _papal_install as installer


class InstallTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/build_integration/install-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.patches = [patch.object(installer, "ROOT", self.root), patch.object(collection, "ROOT", self.root),
                        patch.object(installer, "_source_check", return_value={"status": "pass", "method": "synthetic-test"}),
                        patch.object(installer, "_fresh_plan", side_effect=self.fresh)]
        for item in self.patches:
            item.start()
        self.folder = self.root / ".scratch/batch"
        self.folder.mkdir(parents=True)
        self.revision = "2026-10-26T05:00:00Z"
        self.manifest = {"schema": collection.MANIFEST_SCHEMA, "revision": self.revision, "documents": []}
        self.receipt = {"schema": collection.RECEIPT_SCHEMA, "revision": self.revision, "documents": []}
        self.audits = self.root / "src/sources/papal-documents"
        self.audits.mkdir(parents=True)
        self.report = self.audits / "report.md"
        self.report.write_text("Synthetic individually inspected full-page evidence.\n")
        self.plan_path = self.root / ".scratch/current.json"
        self.pairs_path = self.root / ".scratch/pairs.json"
        self.prepared_path = self.root / ".scratch/prepared.json"
        self.live_plan = None

    def tearDown(self):
        for item in reversed(self.patches):
            item.stop()
        self.temp.cleanup()

    def write(self, path, data):
        path.write_text(json.dumps(data), encoding="utf-8")

    def fresh(self, path):
        value, digest, _ = collection._manifest(Path(path))
        if self.live_plan is not None and installer._canonical(value) != installer._canonical(self.live_plan):
            raise installer.PapalInstallError("source plan is stale")
        return value, digest

    def fixtures(self, statuses=("PASS",)):
        for number, status in enumerate(statuses):
            identity = "papal.synthetic." + str(number)
            pdf = self.folder / (str(number) + ".pdf")
            pdf.write_bytes(("%PDF synthetic " + identity).encode())
            for suffix in (".tex", ".body.tex"):
                (self.folder / (str(number) + suffix)).write_text("synthetic TeX")
            source = {"id": identity, "language": "la", "title": "Synthetic title", "pope": "Synthetic issuer",
                      "artifact_id": "artifact.synthetic." + str(number), "sha256": "a" * 64,
                      "text_path": "src/sources/synthetic/text.txt", "date": "1900-01-01"}
            self.manifest["documents"].append(source)
            self.receipt["documents"].append({"id": identity, "language": "la", "artifact_id": source["artifact_id"],
                "source_sha256": source["sha256"], "status": "compiled", "tex": str(number) + ".tex",
                "body_tex": str(number) + ".body.tex", "pdf": pdf.name, "pdf_sha256": collection._sha(pdf),
                "pages": 2, "text_fidelity": {"status": "pass"}})
        self.receipt["summary"] = {"selected": len(statuses), "compiled": len(statuses), "failed": 0}
        self.manifest_path = self.folder / "frozen.json"
        self.receipt_path = self.folder / "receipt.json"
        self.write(self.manifest_path, self.manifest)
        self.write(self.receipt_path, self.receipt)
        plan = collection.plan_sources([{"name": "synthetic", "path": self.manifest_path}], [], self.plan_path)
        self.live_plan = copy.deepcopy(plan)
        self.write(self.pairs_path, {"schema": installer.PAIRS_SCHEMA, "batches": [{"name": "synthetic",
            "receipt": self.receipt_path.relative_to(self.root).as_posix(), "receipt_sha256": collection._sha(self.receipt_path),
            "manifest": self.manifest_path.relative_to(self.root).as_posix(), "manifest_sha256": collection._sha(self.manifest_path)}]})
        reviews = []
        for item, status in zip(self.receipt["documents"], statuses):
            row = {key: item[key] for key in ("id", "language", "pdf_sha256", "pages")}
            row.update(status=status, individually_inspected_pages=[1, 2], reused_pages=[])
            if status != "PENDING":
                row.update(report=self.report.relative_to(self.root).as_posix(), report_sha256=collection._sha(self.report))
            else:
                row.update(planned_report="future-not-yet-written.md", report_sha256=None)
            reviews.append(row)
        self.audit_path = self.audits / "synthetic-visual-review.json"
        self.audit = {"schema": collection.REVIEW_SCHEMA, "frozen_receipt_sha256": collection._sha(self.receipt_path), "documents": reviews}
        self.write(self.audit_path, self.audit)
        return plan

    def prepare(self):
        return installer.prepare_install(self.plan_path, self.pairs_path, self.prepared_path)

    def install(self):
        self.prepare()
        return installer.install_prepared(self.prepared_path)

    def installed_snapshot(self):
        return {path.relative_to(self.root).as_posix(): path.read_bytes()
                for folder in (self.root / "pdf", self.root / "release")
                if folder.exists() for path in folder.rglob("*") if path.is_file()}

    def replace_built_pdfs(self):
        for number, row in enumerate(self.receipt["documents"]):
            path = self.folder / row["pdf"]
            path.write_bytes(path.read_bytes() + b" newly reviewed generated bytes")
            row["pdf_sha256"] = collection._sha(path)
            self.audit["documents"][number]["pdf_sha256"] = row["pdf_sha256"]
        self.write(self.receipt_path, self.receipt)
        self.audit["frozen_receipt_sha256"] = collection._sha(self.receipt_path)
        self.write(self.audit_path, self.audit)
        pairs = json.loads(self.pairs_path.read_text())
        pairs["batches"][0]["receipt_sha256"] = collection._sha(self.receipt_path)
        self.write(self.pairs_path, pairs)

    def test_installs_only_exact_pass_bytes_and_survives_build_cleanup(self):
        self.fixtures(("PASS", "PENDING", "CHANGES_REQUIRED"))
        proposal = self.prepare()
        self.assertEqual(proposal["summary"]["ready"], 1)
        self.assertEqual(proposal["summary"]["review_pending"], 1)
        self.assertEqual(proposal["summary"]["changes_required"], 1)
        release = installer.install_prepared(self.prepared_path)
        self.assertEqual(len(release["documents"]), 1)
        row = release["documents"][0]
        self.assertEqual((self.root / row["pdf"]).read_bytes(), (self.folder / "0.pdf").read_bytes())
        self.assertTrue(Path(row["pdf"]).name.startswith("1900-01-01--papal.synthetic.0"))
        for path in self.folder.iterdir():
            path.unlink()
        self.assertEqual(installer.check_install(self.plan_path)["not_installed"], 2)

    def test_pending_future_report_never_promotes_or_blocks_other_pass_reader(self):
        self.fixtures(("PASS", "PENDING"))
        proposal = self.prepare()
        self.assertEqual(proposal["summary"]["ready"], 1)
        self.assertFalse(any("future-not" in row["source"] for row in proposal["archives"]))

    def test_install_replays_only_the_explicitly_prepared_review_scope(self):
        self.fixtures(("PASS", "PASS"))
        second = copy.deepcopy(self.audit)
        second["documents"] = [second["documents"][1]]
        self.audit["documents"] = [self.audit["documents"][0]]
        self.write(self.audit_path, self.audit)
        other = self.audits / "other-visual-review.json"
        self.write(other, second)
        proposal = installer.prepare_install(self.plan_path, self.pairs_path, self.prepared_path,
                                             review_manifests=[self.audit_path])
        self.assertEqual(proposal["summary"]["ready"], 1)
        state = next(row for row in proposal["delivery_states"] if row["id"] == "papal.synthetic.1")
        self.assertEqual(state["review_evidence"], "not-supplied")
        self.assertIn("not supplied", state["reason"])
        release = installer.install_prepared(self.prepared_path)
        self.assertEqual(len(release["documents"]), 1)
        self.assertEqual(release["documents"][0]["id"], "papal.synthetic.0")

    def test_tampered_pdf_or_report_refuses_before_any_installed_write(self):
        self.fixtures()
        self.prepare()
        (self.folder / "0.pdf").write_bytes(b"unexpected PDF bytes")
        with self.assertRaises(collection.PapalCollectionError):
            installer.install_prepared(self.prepared_path)
        self.assertFalse((self.root / installer.RELEASE).exists())
        self.assertFalse((self.root / installer.PDF_ROOT).exists())

    def test_failed_current_source_fidelity_never_reaches_installation(self):
        self.fixtures()
        with patch.object(installer, "_source_check", return_value={"status": "failed"}):
            with self.assertRaisesRegex(installer.PapalInstallError, "fidelity"):
                self.prepare()
        self.assertFalse(self.prepared_path.exists())
        self.assertFalse((self.root / installer.PDF_ROOT).exists())

    def test_prepared_candidate_metadata_cannot_be_changed_to_bypass_revalidation(self):
        self.fixtures()
        proposal = self.prepare()
        proposal["documents"][0]["pages"] = 1
        self.write(self.prepared_path, proposal)
        with self.assertRaisesRegex(installer.PapalInstallError, "changed"):
            installer.install_prepared(self.prepared_path)
        self.assertFalse((self.root / installer.PDF_ROOT).exists())

    def test_incomplete_page_review_is_refused(self):
        self.fixtures()
        self.audit["documents"][0]["individually_inspected_pages"] = [1]
        self.write(self.audit_path, self.audit)
        with self.assertRaisesRegex(collection.PapalCollectionError, "every page"):
            self.prepare()

    def test_prepared_plan_cannot_reintroduce_newly_withdrawn_reader(self):
        plan = self.fixtures()
        self.prepare()
        self.live_plan = dict(plan, documents=[])
        with self.assertRaisesRegex(installer.PapalInstallError, "stale"):
            installer.install_prepared(self.prepared_path)
        self.assertFalse((self.root / installer.PDF_ROOT).exists())

    def test_all_withdrawn_removes_only_unchanged_previously_owned_pdf(self):
        plan = self.fixtures()
        release = self.install()
        previous = self.root / release["documents"][0]["pdf"]
        plan["documents"] = []
        plan["selection_plan"]["summary"]["selected"] = 0
        self.write(self.plan_path, plan)
        self.live_plan = plan
        proposal = self.prepare()
        self.assertEqual(proposal["summary"]["ready"], 0)
        updated = installer.install_prepared(self.prepared_path)
        self.assertFalse(previous.exists())
        self.assertEqual(updated["obsolete"][0]["pdf_sha256"], release["documents"][0]["pdf_sha256"])
        self.assertEqual(installer.check_install(self.plan_path)["installed"], 0)

    def test_unexpected_owned_bytes_survive_withdrawal_attempt(self):
        plan = self.fixtures()
        release = self.install()
        path = self.root / release["documents"][0]["pdf"]
        path.write_bytes(b"unexpected user content")
        before = (self.root / installer.RELEASE).read_bytes()
        plan["documents"] = []
        self.write(self.plan_path, plan)
        self.live_plan = plan
        self.prepare()
        with self.assertRaisesRegex(installer.PapalInstallError, "unexpected bytes"):
            installer.install_prepared(self.prepared_path)
        self.assertEqual(path.read_bytes(), b"unexpected user content")
        self.assertEqual((self.root / installer.RELEASE).read_bytes(), before)

    def test_unowned_file_and_symlink_are_preserved(self):
        self.fixtures()
        self.prepare()
        folder = self.root / installer.PDF_ROOT
        folder.mkdir(parents=True)
        foreign = folder / "foreign.pdf"
        foreign.write_bytes(b"user PDF")
        with self.assertRaisesRegex(installer.PapalInstallError, "unowned"):
            installer.install_prepared(self.prepared_path)
        self.assertEqual(foreign.read_bytes(), b"user PDF")
        foreign.unlink()
        foreign.symlink_to(self.folder / "0.pdf")
        with self.assertRaisesRegex(installer.PapalInstallError, "symlink"):
            installer.install_prepared(self.prepared_path)
        self.assertTrue(foreign.is_symlink())

    def test_durable_report_tampering_breaks_release_validation(self):
        self.fixtures()
        release = self.install()
        report = next(row for row in release["evidence"] if row["kind"] == "report")
        (self.root / report["path"]).write_bytes(b"changed old review")
        with self.assertRaisesRegex(installer.PapalInstallError, "hash/size"):
            installer.check_install(self.plan_path)

    def test_second_pdf_write_failure_rolls_back_all_owned_bytes_then_retry_succeeds(self):
        self.fixtures(("PASS", "PASS"))
        self.install()
        before = self.installed_snapshot()
        self.replace_built_pdfs()
        self.prepare()
        original = installer._atomic
        writes = []
        def fail_second_pdf(path, payload):
            if path.suffix == ".pdf":
                writes.append(path)
                if len(writes) == 2:
                    raise OSError("injected second PDF write failure")
            return original(path, payload)
        with patch.object(installer, "_atomic", side_effect=fail_second_pdf):
            with self.assertRaisesRegex(OSError, "second PDF"):
                installer.install_prepared(self.prepared_path)
        self.assertEqual(self.installed_snapshot(), before)
        installer.install_prepared(self.prepared_path)
        self.assertEqual(installer.check_install(self.plan_path)["installed"], 2)
        self.assertNotEqual(self.installed_snapshot(), before)

    def test_release_replace_failure_restores_owned_pdfs_and_all_evidence(self):
        self.fixtures(("PASS", "PASS"))
        self.install()
        before = self.installed_snapshot()
        self.replace_built_pdfs()
        self.prepare()
        original = installer._atomic
        def fail_after_release_replace(path, payload):
            original(path, payload)
            if path == self.root / installer.RELEASE:
                raise OSError("injected release replacement failure")
        with patch.object(installer, "_atomic", side_effect=fail_after_release_replace):
            with self.assertRaisesRegex(OSError, "release replacement"):
                installer.install_prepared(self.prepared_path)
        self.assertEqual(self.installed_snapshot(), before)

    def test_obsolete_unlink_failure_restores_old_release_without_removing_other_files(self):
        plan = self.fixtures(("PASS", "PASS"))
        release = self.install()
        before = self.installed_snapshot()
        plan["documents"] = []
        self.write(self.plan_path, plan)
        self.live_plan = plan
        self.prepare()
        target = self.root / release["documents"][1]["pdf"]
        original = Path.unlink
        def fail_unlink(path, *args, **kwargs):
            if path == target:
                raise OSError("injected obsolete unlink failure")
            return original(path, *args, **kwargs)
        with patch.object(Path, "unlink", fail_unlink):
            with self.assertRaisesRegex(OSError, "obsolete unlink"):
                installer.install_prepared(self.prepared_path)
        self.assertEqual(self.installed_snapshot(), before)

    def test_metadata_only_source_change_cannot_reuse_old_successful_pdf(self):
        plan = self.fixtures()
        plan["documents"][0]["title"] = "New source notice requires a new rendering"
        self.write(self.plan_path, plan)
        self.live_plan = plan
        proposal = self.prepare()
        self.assertEqual(proposal["summary"]["ready"], 0)
        self.assertEqual(proposal["summary"]["missing"], 1)

    def test_safe_paths_refuse_traversal_and_parent_symlinks(self):
        for value in ("../outside.pdf", "/absolute.pdf", "pdf\\escape.pdf"):
            with self.subTest(value=value), self.assertRaises(installer.PapalInstallError):
                installer._safe(value)
        (self.root / "pdf").symlink_to(self.folder, target_is_directory=True)
        with self.assertRaisesRegex(installer.PapalInstallError, "symlink"):
            installer._safe("pdf/papal-documents/example.pdf")

    def test_preparation_output_does_not_follow_a_symlink_to_unrelated_bytes(self):
        self.fixtures()
        unrelated = self.root / ".scratch/unrelated.json"
        unrelated.write_bytes(b"unrelated original bytes")
        self.prepared_path.symlink_to(unrelated)
        with self.assertRaisesRegex(installer.PapalInstallError, "symlink"):
            self.prepare()
        self.assertEqual(unrelated.read_bytes(), b"unrelated original bytes")

    def test_every_atomic_temporary_file_stays_under_repository_scratch(self):
        self.fixtures()
        original = installer.tempfile.NamedTemporaryFile
        directories = []
        def tracked(*args, **kwargs):
            directories.append(Path(kwargs["dir"]))
            return original(*args, **kwargs)
        with patch.object(installer.tempfile, "NamedTemporaryFile", side_effect=tracked):
            self.install()
        self.assertTrue(directories)
        self.assertTrue(all(path.is_relative_to(self.root / ".scratch") for path in directories))

    def test_new_uninstalled_selection_is_reported_without_inventing_a_review_state(self):
        plan = self.fixtures()
        self.install()
        new = copy.deepcopy(plan["documents"][0])
        new["id"] = "papal.synthetic.new"
        plan["documents"].append(new)
        self.write(self.plan_path, plan)
        self.live_plan = plan
        checked = installer.check_install(self.plan_path)
        self.assertEqual(checked["not_installed"], 1)
        self.assertEqual(checked["uninstalled"], [{"id": new["id"], "language": "la", "status": "not-installed"}])
        self.assertFalse(checked["release_plan_is_current"])

    def test_default_freshness_resolves_new_optional_source_inputs(self):
        old = self.fixtures()
        fresh = copy.deepcopy(old)
        fresh["selection_plan"]["inputs"].append({"name": "new-withdrawal", "path": "new.json", "sha256": "b" * 64})
        self.patches[-1].stop()
        def regenerate(command, **kwargs):
            self.assertNotIn("MAKEFLAGS", kwargs["env"])
            self.assertNotIn("PAPAL_BASE_MANIFESTS", kwargs["env"])
            destination = Path(next(value.split("=", 1)[1] for value in command if value.startswith("PAPAL_CURRENT_MANIFEST=")))
            self.write(destination, fresh)
            return type("Run", (), {"returncode": 0, "stderr": ""})()
        with patch.dict(installer.os.environ, {"MAKEFLAGS": "PAPAL_BASE_MANIFESTS=subset", "PAPAL_BASE_MANIFESTS": "subset"}), \
                patch.object(installer.subprocess, "run", side_effect=regenerate):
            with self.assertRaisesRegex(installer.PapalInstallError, "stale"):
                installer._fresh_plan(self.plan_path)
        self.patches[-1].start()


if __name__ == "__main__":
    unittest.main()
