"""Check binding of authenticated Actions archives to the native catalog merger."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("pages_native_reference", ROOT / ".github/scripts/pages-native-reference.py")
pages = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pages)


class NativeReferenceDownloadTests(unittest.TestCase):
    revision = "a" * 40

    def setUp(self):
        scratch = ROOT / ".scratch/print-reference-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        directory = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def archive(self, member="catalog.json"):
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w") as writer:
            writer.writestr(member, b"test catalog\n")
        return output.getvalue()

    def artifact(self, n, body):
        return {"id": n + 50, "name": f"native-print-reference-42-shard-{n}", "expired": False,
                "workflow_run": {"id": 42, "head_sha": self.revision}, "size_in_bytes": len(body),
                "digest": "sha256:" + hashlib.sha256(body).hexdigest()}

    def test_artifact_set_is_scoped_to_run_revision_and_unique_shards(self):
        original = self.artifact(1, self.archive())
        for records in ([original, original], [dict(original, workflow_run={"id": 7, "head_sha": self.revision})],
                        [dict(original, workflow_run={"id": 42, "head_sha": "c" * 40})]):
            with self.subTest(records=records), self.assertRaises(ValueError):
                pages.select_artifacts(records, "42", self.revision)
        self.assertEqual({}, pages.select_artifacts([dict(original, expired=True)], "42", self.revision))
        self.assertEqual({}, pages.select_artifacts([dict(original, name="github-pages")], "42", self.revision))

    def test_wrong_archive_or_unexpected_member_fails_before_merge(self):
        good = self.archive()
        for member in ("catalog.json", "../escape", "/escape", "native-tex/../../escape"):
            body = self.archive(member)
            item = self.artifact(1, good if member == "catalog.json" else body)
            if member == "catalog.json":
                body += b"changed"
            with self.subTest(member=member), tempfile.TemporaryDirectory(dir=self.root) as directory:
                with patch.object(pages.subprocess, "run", side_effect=lambda cmd, *, stdout, check: stdout.write(body)):
                    with self.assertRaises(ValueError):
                        pages.fetch_partition("repo/actions", item, Path(directory) / "1")
                self.assertFalse((Path(directory) / "escape").exists())

    def test_all_eight_catalog_digests_reach_merger_and_workflow_output(self):
        body = self.archive()
        partitions = [self.artifact(n, body) for n in range(1, pages.SHARDS + 1)]
        env = {"GITHUB_SHA": self.revision, "GITHUB_RUN_ID": "42", "GITHUB_RUN_ATTEMPT": "2",
               "GITHUB_REPOSITORY": "o/r", "GITHUB_OUTPUT": str(self.root / "step"),
               "PAGES_NATIVE_REFERENCE_DIR": str(self.root / "merged")}
        expected = hashlib.sha256(b"test catalog\n").hexdigest()

        def run(cmd, *, stdout, check):
            self.assertIn(cmd[-1], [f"repos/o/r/actions/artifacts/{a['id']}/zip" for a in partitions])
            stdout.write(body)

        def capture(cmd, **kwargs):
            if cmd[0] == "git":
                return self.revision + "\n"
            if cmd[0] == "gh":
                self.assertEqual(cmd[-1], "repos/o/r/actions/runs/42/artifacts?per_page=100")
                return json.dumps([{"artifacts": partitions}]).encode()
            refs = Path(cmd[cmd.index("--references") + 1])
            keys = json.loads(Path(cmd[cmd.index("--expected-keys") + 1]).read_bytes())
            self.assertEqual({p.name for p in refs.iterdir()}, {str(n) for n in range(1, 9)})
            self.assertEqual(keys, {p.name: expected for p in refs.iterdir()})
            for part in refs.iterdir():
                self.assertEqual((part / "catalog.json").read_bytes(), b"test catalog\n")
            return "b" * 64 + "\n"

        with patch.object(pages.subprocess, "run", side_effect=run), patch.object(pages.subprocess, "check_output",
                                                                                    side_effect=capture):
            pages.prepare(env)
        self.assertEqual((self.root / "merged.sha256").read_text().strip(), "b" * 64)
        self.assertEqual((self.root / "step").read_text(), "native-reference-sha256=" + "b" * 64 + "\n")
