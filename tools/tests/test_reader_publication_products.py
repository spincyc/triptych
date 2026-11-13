"""Lazy publication reads keep admission, source hashes and exact product bytes."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import signal
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _reader_publication_products as reader


class Index:
    def __init__(self, files):
        self.files, self.reads = files, []

    def read(self, path):
        self.reads.append(path)
        return self.files[path]


class PublicationReaderTests(unittest.TestCase):
    def setUp(self):
        self.head = "a" * 40
        self.history = self.enterContext(mock.patch.object(reader, "_check_history"))
        self.enterContext(mock.patch.object(reader, "_clean_history_head", return_value=self.head))
        self.identity = "gpt/articles/faith/example"
        self.route = "web-editions/" + self.identity + ".json"
        self.row = {"provider": "gpt", "document": "articles/faith/example"}
        self.source = "src/gpt/articles/faith/example/main.tex"
        self.index = Index({reader.READERS: reader._json({"schema": reader.SCHEMA, "generation_commit": self.head,
                            "readers": {self.identity: self.row}}), self.source: b"source"})
        markdown = "# Exact text\n\nA retained source notice.\n"
        self.product = {"schema": "triptych-web-edition/v1", "id": self.identity,
                        "markdown": markdown,
                        "markdown_sha256": hashlib.sha256(markdown.encode()).hexdigest()}
        self.result = {"record": self.product,
                       "dependencies": {self.source: hashlib.sha256(b"source").hexdigest()}}

    def worker(self, result=None, status=0):
        return mock.patch.object(reader, "_run_worker", return_value=subprocess.CompletedProcess(
            [], status, json.dumps(self.result if result is None else result), "conversion refused"))

    def test_catalogue_opens_only_tracked_metadata_without_a_producer(self):
        body = b'{"schema":"triptych-document-catalogue/v1", "works":[]}\n'
        self.index.files[reader.CATALOG] = body
        with mock.patch.object(reader, "_tool", side_effect=AssertionError("producer loaded")):
            self.assertEqual(reader.resolve("structure/documents/corpus.json", ROOT, self.index), body)
        self.assertEqual(self.index.reads, [reader.READERS, reader.CATALOG])
        self.history.assert_called_once()

    def test_selected_worker_rechecks_all_consumed_inputs_and_preserves_exact_bytes(self):
        with self.worker() as worker:
            result = reader.resolve(self.route, ROOT, self.index)
        self.assertEqual(result, reader._json(self.product))
        self.assertEqual(self.index.reads, [reader.READERS, self.source])
        args, kwargs = worker.call_args
        self.assertEqual(args[0][-2:], ["--indexed-product-row-json", self.identity])
        self.assertIn("-B", args[0])
        self.assertEqual(json.loads(kwargs["input"]), self.row)

    def test_edit_during_conversion_refuses_the_product(self):
        self.index.files[self.source] = b"edited"
        with self.worker(), self.assertRaisesRegex(ValueError, "changed during conversion"):
            reader.resolve(self.route, ROOT, self.index)

    def test_missing_current_source_is_not_a_cached_reader(self):
        del self.index.files[self.source]
        with self.worker(), self.assertRaises(KeyError):
            reader.resolve(self.route, ROOT, self.index)

    def test_invalid_or_unbound_worker_results_are_refused(self):
        for changes in ({"dependencies": {}}, {"dependencies": []},
                        {"record": {**self.product, "markdown": "changed"}},
                        {"record": {**self.product, "id": "gpt/other"}}):
            with self.subTest(changes=changes), self.worker({**self.result, **changes}), self.assertRaises(ValueError):
                reader.resolve(self.route, ROOT, self.index)

    def test_worker_refusal_is_visible_and_unlisted_output_never_runs(self):
        with self.worker(status=1), self.assertRaisesRegex(ValueError, "conversion refused"):
            reader.resolve(self.route, ROOT, self.index)
        with self.worker() as worker, self.assertRaisesRegex(ValueError, "no indexed"):
            reader.resolve("web-editions/gpt/articles/faith/absent.json", ROOT, self.index)
        worker.assert_not_called()

    def test_unsafe_paths_and_other_product_families_never_convert(self):
        with self.worker() as worker:
            for route in ("web-editions/gpt/../example.json", "web-editions/gpt//example.json",
                          "web-editions/gpt/example.json/extra", "web-editions/gpt/\\example.json"):
                with self.subTest(route=route), self.assertRaises(ValueError):
                    reader.resolve(route, ROOT, self.index)
            for route in ("structure/propers/index.json", "web-editions/index.json"):
                self.assertIsNone(reader.resolve(route, ROOT, self.index))
        worker.assert_not_called()

    def test_maintenance_uses_full_producers_without_copying_reading_bodies(self):
        document = SimpleNamespace(key=("gpt", "articles/faith/example"))
        catalogue = {"schema": "triptych-document-catalogue/v1", "works": [
            {"editions": [{"revised": "2026-01-01T00:00:00Z"}]}]}
        owner = SimpleNamespace(catalogue=mock.Mock(return_value=catalogue),
                                _serialise=lambda value: json.dumps(value) + "\n")
        converter = SimpleNamespace(reader_outputs=mock.Mock(return_value=[self.row]))
        with mock.patch("_corpus.documents", return_value=(document,)) as documents, \
                mock.patch.object(reader, "_tool", side_effect=[owner, converter]):
            files = reader.build_reader_indexes(ROOT)
        documents.cache_clear.assert_called_once()
        documents.assert_called_once_with(root=ROOT)
        owner.catalogue.assert_called_once_with((document,), {document.key: document}, root=ROOT)
        self.assertEqual(json.loads(files[reader.CATALOG]), catalogue)
        self.assertEqual(json.loads(files[reader.READERS])["readers"], {self.identity: self.row})
        self.assertEqual(json.loads(files[reader.READERS])["generation_commit"], self.head)
        self.assertNotIn(b'"markdown"', files[reader.READERS])

    def test_maintenance_refuses_clock_dependent_uncommitted_revision_metadata(self):
        catalogue = {"works": [{"editions": [{"revised": "2026-01-01T00:00:00Z (uncommitted sources)"}]}]}
        owner = SimpleNamespace(catalogue=mock.Mock(return_value=catalogue))
        with mock.patch("_corpus.documents", return_value=()), \
                mock.patch.object(reader, "_tool", return_value=owner), \
                self.assertRaisesRegex(ValueError, "committed edition sources"):
            reader.build_reader_indexes(ROOT)

    def test_independent_check_preserves_the_valid_recorded_history_anchor(self):
        owner = SimpleNamespace(catalogue=lambda *args, **kwargs: {"works": []},
                                _serialise=lambda value: json.dumps(value))
        converter = SimpleNamespace(reader_outputs=lambda: [])
        base = "b" * 40
        with mock.patch("_corpus.documents", return_value=()), \
                mock.patch.object(reader, "_tool", side_effect=[owner, converter]):
            files = reader.build_reader_indexes(ROOT, generation_commit=base)
        self.history.assert_called_once_with(ROOT, {"generation_commit": base})
        self.assertEqual(json.loads(files[reader.READERS])["generation_commit"], base)

    def test_generation_refuses_a_head_change_during_derivation(self):
        owner = SimpleNamespace(catalogue=lambda *args, **kwargs: {"works": []})
        converter = SimpleNamespace(reader_outputs=lambda: [])
        with mock.patch("_corpus.documents", return_value=()), \
                mock.patch.object(reader, "_tool", side_effect=[owner, converter]), \
                mock.patch.object(reader, "_clean_history_head", side_effect=[self.head, "b" * 40]), \
                self.assertRaisesRegex(ValueError, "history changed during"):
            reader.build_reader_indexes(ROOT)


class PublicationWorkerLifecycleTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/project-perf/tmp"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.cancelled = threading.Event()
        self.index = SimpleNamespace(_reader_cancelled=self.cancelled)
        self.processes = []
        popen = subprocess.Popen

        def capture(*args, **kwargs):
            process = popen(*args, **kwargs)
            self.processes.append(process)
            return process

        self.enterContext(mock.patch.object(reader.subprocess, "Popen", side_effect=capture))
        self.addCleanup(self.cleanup_processes)

    def cleanup_processes(self):
        for process in self.processes:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait(timeout=3)
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None and not stream.closed:
                    stream.close()

    def run_worker(self, source, **kwargs):
        return reader._run_worker([sys.executable, "-B", "-c", source], input="selected row — exact\n",
                                  cwd=self.root, index=self.index, **kwargs)

    def assert_reaped_and_closed(self):
        self.assertTrue(self.processes)
        for process in self.processes:
            self.assertIsNotNone(process.returncode)
            self.assertTrue(all(stream.closed for stream in (process.stdin, process.stdout, process.stderr)))
            with self.assertRaises(ChildProcessError):
                os.waitpid(process.pid, os.WNOHANG)

    def test_success_preserves_input_and_both_captured_streams(self):
        result = self.run_worker("import sys; sys.stdout.write(sys.stdin.read()); sys.stderr.write('diagnostic\\n')")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "selected row — exact\n")
        self.assertEqual(result.stderr, "diagnostic\n")
        self.assert_reaped_and_closed()

    def test_cancellation_before_launch_creates_no_process(self):
        self.cancelled.set()
        with self.assertRaisesRegex(ValueError, "reader cancelled"):
            self.run_worker("raise AssertionError('must not run')")
        self.assertEqual(self.processes, [])

    def test_cancellation_during_process_creation_still_reaps_the_worker(self):
        launch = reader.subprocess.Popen.side_effect

        def race(*args, **kwargs):
            process = launch(*args, **kwargs)
            self.cancelled.set()
            return process

        with mock.patch.object(reader.subprocess, "Popen", side_effect=race):
            with self.assertRaisesRegex(ValueError, "reader cancelled"):
                self.run_worker("import time; time.sleep(60)")
        self.assert_reaped_and_closed()

    def test_timeout_kills_a_worker_ignoring_term_and_closes_its_pipes(self):
        started = time.monotonic()
        with self.assertRaisesRegex(ValueError, "timeout"):
            self.run_worker("import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(60)",
                            timeout=0.2)
        self.assertLess(time.monotonic() - started, 3)
        self.assertEqual(self.processes[0].returncode, -signal.SIGKILL)
        self.assert_reaped_and_closed()

    @unittest.skipUnless(sys.platform.startswith("linux"), "requires Linux orphan adoption for fixture cleanup")
    def test_cancel_kills_stubborn_descendant_even_after_leader_exits(self):
        # Adopt only this fixture's orphan so the test can reap it and prove its
        # death, rather than leaving a zombie with the container's init process.
        import ctypes
        libc, previous = ctypes.CDLL(None, use_errno=True), ctypes.c_int()
        self.assertEqual(libc.prctl(37, ctypes.byref(previous), 0, 0, 0), 0)
        self.assertEqual(libc.prctl(36, 1, 0, 0, 0), 0)
        self.addCleanup(lambda: libc.prctl(36, previous.value, 0, 0, 0))
        marker = self.root / "descendant.json"
        descendant = ("import json,os,signal,time; from pathlib import Path; "
                      "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                      f"Path({str(marker)!r}).write_text(json.dumps(dict(pid=os.getpid(),pgid=os.getpgrp()))); "
                      "time.sleep(60)")
        producer = ("import subprocess,sys,time; "
                    f"subprocess.Popen([sys.executable,'-c',{descendant!r}], "
                    "stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(60)")
        failures = []

        def work():
            try:
                self.run_worker(producer, timeout=10)
            except BaseException as error:
                failures.append(error)

        thread = threading.Thread(target=work)
        thread.start()
        try:
            deadline = time.monotonic() + 3
            while not marker.exists() and thread.is_alive() and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue(marker.exists(), failures)
            child = json.loads(marker.read_text())
            self.assertEqual(child["pgid"], self.processes[0].pid)

            def reap_fixture():
                try:
                    if os.waitpid(child["pid"], os.WNOHANG)[0] == 0:
                        os.kill(child["pid"], signal.SIGKILL)
                        os.waitpid(child["pid"], 0)
                except ChildProcessError:
                    pass

            self.addCleanup(reap_fixture)
            self.cancelled.set()
            thread.join(timeout=3)
            self.assertFalse(thread.is_alive())
            self.assertEqual(len(failures), 1)
            self.assertIsInstance(failures[0], ValueError)
            self.assertIn("cancelled", str(failures[0]))
            self.assert_reaped_and_closed()
            deadline = time.monotonic() + 3
            while True:
                pid, status = os.waitpid(child["pid"], os.WNOHANG)
                if pid or time.monotonic() >= deadline:
                    break
                time.sleep(0.01)
            self.assertEqual(pid, child["pid"], "descendant survived cancellation")
            self.assertTrue(os.WIFSIGNALED(status))
            self.assertEqual(os.WTERMSIG(status), signal.SIGKILL)
        finally:
            self.cancelled.set()
            thread.join(timeout=3)


class PublicationHistoryTests(unittest.TestCase):
    """Actual Git histories, including reverted source edits and divergent bases."""

    def setUp(self):
        scratch = ROOT / ".scratch/project-perf/tmp"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "--quiet", "--initial-branch=feature/tui-perf")
        self.source = self.root / "src/gpt/articles/faith/example/main.tex"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("Original source.\n")
        self.base = self.commit("initial source")

    def git(self, *arguments):
        result = subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                                 *arguments], cwd=self.root, check=True, capture_output=True, text=True)
        return result.stdout.strip()

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "--quiet", "-m", message)
        return self.git("rev-parse", "HEAD")

    def check(self, base=None):
        reader._check_history(self.root, {"generation_commit": base or self.base})

    def test_metadata_documentation_and_test_only_commits_preserve_the_binding(self):
        self.check()
        for name in ("src/index/documents/readers.json", "README.md", "guidance/editorial.md", "tools/tests/example.py"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Lookup, documentation or test.\n")
        self.commit("metadata only")
        self.check()

    def test_source_edit_and_revert_still_requires_new_revision_metadata(self):
        self.source.write_text("Changed source.\n")
        self.commit("revise source")
        self.source.write_text("Original source.\n")
        self.commit("restore original bytes")
        self.assertEqual(self.git("diff", self.base, "HEAD"), "")
        with self.assertRaisesRegex(ValueError, "changed since metadata"):
            self.check()

    def test_reverted_source_edits_on_a_merged_branch_are_not_hidden(self):
        self.git("checkout", "--quiet", "-b", "feature/side")
        self.source.write_text("Changed source.\n")
        self.commit("revise on side")
        self.source.write_text("Original source.\n")
        self.commit("restore on side")
        self.git("checkout", "--quiet", "feature/tui-perf")
        self.git("merge", "--quiet", "--no-ff", "feature/side", "-m", "merge side history")
        self.assertEqual(self.git("diff", self.base, "HEAD"), "")
        with self.assertRaisesRegex(ValueError, "changed since metadata"):
            self.check()

    def test_missing_or_nonancestor_generation_commit_is_refused(self):
        with self.assertRaisesRegex(ValueError, "missing or not an ancestor"):
            self.check("0" * 40)
        self.git("checkout", "--quiet", "-b", "feature/side")
        (self.root / "README.md").write_text("Side branch.\n")
        side = self.commit("side history")
        self.git("checkout", "--quiet", "feature/tui-perf")
        with self.assertRaisesRegex(ValueError, "missing or not an ancestor"):
            self.check(side)

    def test_shallow_and_unbound_history_are_refused(self):
        (self.root / ".git/shallow").write_text(self.base + "\n")
        with self.assertRaisesRegex(ValueError, "history is shallow"):
            self.check()
        with self.assertRaisesRegex(ValueError, "no generation commit"):
            reader._check_history(self.root, {})

    def test_generation_requires_clean_runtime_inputs_but_allows_new_indexes(self):
        path = self.root / "src/index/documents/new.json"
        path.parent.mkdir(parents=True)
        path.write_text("{}\n")
        self.assertEqual(reader._clean_history_head(self.root), self.base)
        self.source.write_text("Uncommitted change.\n")
        with self.assertRaisesRegex(ValueError, "requires committed runtime inputs"):
            reader._clean_history_head(self.root)


if __name__ == "__main__":
    unittest.main()
