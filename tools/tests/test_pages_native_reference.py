"""Check binding of authenticated Actions archives to the native catalog merger."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import subprocess
from unittest.mock import patch
import zipfile


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("pages_native_reference", ROOT / ".github/scripts/pages-native-reference.py")
pages = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pages)


class CorpusGateTests(unittest.TestCase):
    revision = "a" * 40
    env = {"GITHUB_SHA": revision, "GITHUB_RUN_ID": "42", "GITHUB_REPOSITORY": "o/r", "GITHUB_RUN_ATTEMPT": "2"}

    def jobs(self):
        return [{"name": f"canonical-check ({gate})", "run_id": 42, "head_sha": self.revision, "run_attempt": 2,
                 "status": "completed", "conclusion": "success",
                 "steps": [{"name": "Run canonical source check", "status": "completed", "conclusion": "success"}]}
                for gate in ("check-corpus-index", "check-proper-chronology-current", "check-source-graph")]

    def test_exact_latest_same_source_job_results_and_executed_steps(self):
        first, *rest = self.jobs()
        passed = lambda jobs: pages.source_gate_passed(jobs, "42", self.revision, 2, pages.CORPUS_GATE)
        self.assertTrue(passed([dict(first, run_attempt=1), *rest]))  # partial rerun retained a success
        self.assertFalse(passed(rest))
        self.assertFalse(passed([dict(first, status="in_progress", conclusion=None), *rest]))
        for change in ({"run_id": 13}, {"head_sha": "b" * 40}, {"run_attempt": 3},
                       {"conclusion": "cancelled"},
                       {"conclusion": "skipped"}, {"conclusion": "failure"}, {"steps": []},
                       {"steps": [{"name": "Run canonical source check", "conclusion": "skipped"}]}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                passed([dict(first, **change), *rest])
        with self.assertRaises(ValueError):
            passed([first, first, *rest])

    def test_other_runner_must_complete_its_own_canonical_step_on_this_run_and_source(self):
        gate = pages.DEPLOYMENT_GATE
        source = dict(self.jobs()[0], name=gate[0], run_attempt=1,
                      steps=[{"name": gate[1], "status": "completed", "conclusion": "success"}])
        check = lambda jobs: pages.source_gate_passed(jobs, "42", self.revision, 2, gate)
        self.assertFalse(check(self.jobs()))
        self.assertTrue(check([source]))  # latest successful job retained on a partial retry
        self.assertFalse(check([dict(source, conclusion="failure")]))
        self.assertFalse(check([dict(source, run_attempt=2, status="queued", conclusion=None)]))
        for change in ({"run_id": 43}, {"head_sha": "b" * 40}, {"run_attempt": 3},
                       {"steps": []}, {"steps": source["steps"] * 2},
                       {"steps": [{"name": pages.CORPUS_GATE[1], "status": "completed", "conclusion": "success"}]},
                       {"steps": [{"name": gate[1], "status": "in_progress", "conclusion": "success"}]},
                       {"steps": [{"name": gate[1], "conclusion": "skipped"}]}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                check([{**source, "run_attempt": 2, **change}])
        with self.assertRaises(ValueError):
            check([source, source])

    def test_failed_other_runner_is_reported_while_corpus_is_still_missing(self):
        job_name, step_name = pages.DEPLOYMENT_GATE
        failure = dict(self.jobs()[0], name=job_name, conclusion="failure",
                       steps=[{"name": step_name, "conclusion": "failure"}])
        with patch.object(pages.subprocess, "check_output", return_value=self.revision), \
             patch.object(pages, "latest_jobs", return_value=[failure]), \
             patch.object(pages.time, "sleep") as sleep, self.assertRaisesRegex(ValueError, job_name):
            pages.wait_for_source_gates(self.env, (pages.CORPUS_GATE, pages.DEPLOYMENT_GATE))
        sleep.assert_not_called()

    def test_retry_selects_latest_execution_even_across_api_pages(self):
        first, second, third = self.jobs()
        stale = dict(first, run_attempt=1)
        running = dict(first, status="queued", conclusion=None)
        retained = dict(second, run_attempt=1)
        result = json.dumps([{"jobs": [stale, retained]}, {"jobs": [third, running]}])
        with patch.object(pages.subprocess, "check_output", return_value=result) as query:
            selected = pages.latest_jobs("run", prior_attempts=True)
        query.assert_called_once_with(["gh", "api", "--paginate", "--slurp",
                                       "run/jobs?filter=all&per_page=100"], timeout=30)
        self.assertCountEqual(selected, [running, retained, third])
        self.assertFalse(pages.source_gate_passed(selected, "42", self.revision, 2, pages.CORPUS_GATE))

    def test_poll_retries_interruptions_and_requires_all_successes(self):
        failed = subprocess.CalledProcessError(1, ["gh", "api"])
        running = self.jobs()[1:]
        with patch.object(pages.subprocess, "check_output", return_value=self.revision), \
                patch.object(pages.time, "sleep"), \
                patch.object(pages, "latest_jobs", side_effect=[failed, running, self.jobs()]) as query:
            pages.wait_for_source_gates(self.env, (pages.CORPUS_GATE,))
            self.assertEqual(query.call_count, 3)
            query.assert_called_with("repos/o/r/actions/runs/42", prior_attempts=True)
        with patch.object(pages.subprocess, "check_output", return_value=self.revision), \
                patch.object(pages.time, "sleep"), patch.object(pages, "latest_jobs", side_effect=failed) as query, \
                self.assertRaises(subprocess.CalledProcessError):
            pages.wait_for_source_gates(self.env, (pages.CORPUS_GATE,))
        self.assertEqual(query.call_count, 3)
        with patch.object(pages.subprocess, "check_output", return_value=self.revision), \
                patch.object(pages.time, "sleep"), patch.object(pages.time, "monotonic", side_effect=[0, 1, 10000]), \
                patch.object(pages, "latest_jobs", return_value=running), self.assertRaisesRegex(ValueError, "timed out"):
            pages.wait_for_source_gates(self.env, (pages.CORPUS_GATE,))
        with patch.object(pages.subprocess, "check_output", return_value="wrong"), \
                patch.object(pages, "latest_jobs") as query, self.assertRaisesRegex(ValueError, "checkout"):
            pages.wait_for_source_gates(self.env, (pages.CORPUS_GATE,))
        query.assert_not_called()


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

    def test_download_retries_the_same_id_and_discards_partial_bytes(self):
        body = self.archive()
        artifact = self.artifact(1, body)
        destination = self.root / "1"
        command = ["gh", "api", "repo/actions/artifacts/51/zip"]
        attempts = []

        def download(argv, *, stdout, check, timeout):
            attempts.append(list(argv))
            if len(attempts) == 1:
                stdout.write(b"partial response" * 40)
                raise subprocess.CalledProcessError(1, argv)
            stdout.write(body)

        with patch.object(pages.subprocess, "run", side_effect=download), patch.object(pages.time, "sleep") as wait:
            digest = pages.fetch_partition("repo/actions", artifact, destination)
        self.assertEqual(attempts, [command, command])
        wait.assert_called_once_with(2)
        self.assertEqual(digest, hashlib.sha256(b"test catalog\n").hexdigest())

    def test_persistent_download_failure_keeps_the_partition_unavailable(self):
        item = self.artifact(1, self.archive())
        destination = self.root / "1"
        failure = subprocess.TimeoutExpired("gh", timeout=90)
        with patch.object(pages.subprocess, "run", side_effect=failure) as download, patch.object(pages.time, "sleep"):
            with self.assertRaises(subprocess.TimeoutExpired):
                pages.fetch_partition("repo/actions", item, destination)
        self.assertEqual(download.call_count, 5)
        self.assertFalse(destination.exists())

    def test_wrong_archive_or_unexpected_member_fails_before_merge(self):
        good = self.archive()
        for member in ("catalog.json", "../escape", "/escape", "native-tex/../../escape"):
            body = self.archive(member)
            item = self.artifact(1, good if member == "catalog.json" else body)
            if member == "catalog.json":
                body += b"changed"
            with self.subTest(member=member), tempfile.TemporaryDirectory(dir=self.root) as directory:
                with patch.object(pages.subprocess, "run", side_effect=lambda cmd, *, stdout, check, timeout: stdout.write(body)):
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

        def run(cmd, *, stdout, check, timeout):
            self.assertIn(cmd[-1], [f"repos/o/r/actions/artifacts/{a['id']}/zip" for a in partitions])
            stdout.write(body)

        def capture(cmd, **kwargs):
            if cmd[0] == "git":
                return self.revision + "\n"
            if cmd[0] == "gh":
                self.assertEqual(cmd[-1], "repos/o/r/actions/runs/42/artifacts?per_page=100")
                return json.dumps([{"artifacts": partitions}]).encode()
            self.assertIn("--publication-sources", cmd)
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
