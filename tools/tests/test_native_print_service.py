"""Native PDF API admission, asynchronous work and artifact integrity boundaries."""
from __future__ import annotations

import hashlib
import http.client
from http.server import ThreadingHTTPServer
import json
import io
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _native_print_service as native

REVISION = "a" * 40
TOOLCHAIN = "sha256:" + "b" * 64
DOCUMENT = "publication:gpt/articles/faith/example"
PDF = b"%PDF-1.7\nNative TeX fixture; not a visually reviewed PDF.\n%%EOF\n"


class ServiceTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/tex-print-service/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.base = Path(self.temporary.name)
        self.root = self.base / "source"
        self.root.mkdir()
        self.input = self.root / "src/exact.tex"
        self.input.parent.mkdir()
        self.input.write_text("Canonical TeX words.\n")
        self.selection = {"id": DOCUMENT, "document": DOCUMENT, "edition": "main", "title": "Example"}
        self.selections = {(DOCUMENT, "main"): self.selection}
        self.services = []
        self.compiles = 0

    def tearDown(self):
        for service in self.services:
            service.close()
        self.temporary.cleanup()

    def compiler(self, selected, workspace):
        self.compiles += 1
        pdf = workspace / "selected.pdf"
        pdf.write_bytes(PDF)
        receipt = workspace / "selected.print.json"
        receipt.write_text(json.dumps({
            "schema": "triptych-print-document/v1", "status": "built", "output_format": "pdf",
            "document": {"id": selected["id"]}, "path_base": "receipt-directory", "output": pdf.name,
            "bytes": len(PDF), "output_sha256": hashlib.sha256(PDF).hexdigest(),
            "inputs": [{"path": "src/exact.tex", "bytes": self.input.stat().st_size,
                        "sha256": hashlib.sha256(self.input.read_bytes()).hexdigest()}],
        }))
        return pdf, receipt

    def service(self, **options):
        arguments = {"toolchain": TOOLCHAIN, "revision": REVISION,
                     "source_checker": lambda root, revision: None,
                     "selection_loader": lambda root: dict(self.selections),
                     "compiler": self.compiler}
        arguments.update(options)
        service = native.PrintService(self.root, self.base / "cache", **arguments)
        self.services.append(service)
        return service

    def request(self, **options):
        return {"document": DOCUMENT, "edition": "main", "source_revision": REVISION, **options}

    def ready(self, service, job):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            result = service.status(job["key"])
            if result["state"] in {"ready", "failed"}:
                return result
            time.sleep(0.005)
        self.fail("fixture native job did not finish")

    def test_current_admitted_edition_produces_verified_download(self):
        service = self.service()
        result = self.ready(service, service.submit(self.request()))
        self.assertEqual(result["state"], "ready")
        self.assertEqual(result["source_revision"], REVISION)
        self.assertEqual(result["output_id"], DOCUMENT)
        self.assertEqual(result["pdf_sha256"], hashlib.sha256(PDF).hexdigest())
        path, name = service.pdf(result["key"])
        self.assertEqual(path.read_bytes(), PDF)
        self.assertEqual(name, "example.pdf")
        self.assertEqual(list(service.work.iterdir()), [])

    def test_held_extra_native_recipes_and_implicit_edition_aliases_are_refused(self):
        service = self.service()
        for request in (self.request(document="publication:gpt/held"),
                        self.request(document="papal:not-admitted/la"),
                        self.request(edition="research"), self.request(document="../../etc/passwd")):
            with self.subTest(request=request), self.assertRaises(native.ServiceError) as error:
                service.submit(request)
            self.assertEqual(error.exception.status, 404)
        self.assertEqual(self.compiles, 0)

    def test_source_revision_mismatch_is_a_conflict(self):
        with self.assertRaises(native.ServiceError) as error:
            self.service().submit(self.request(source_revision="c" * 40))
        self.assertEqual(error.exception.status, 409)

    def test_no_uploaded_tex_paths_urls_or_extra_fields(self):
        service = self.service()
        for field in ("tex", "command", "url", "path"):
            with self.subTest(field=field), self.assertRaises(native.ServiceError):
                service.submit({**self.request(), field: "untrusted"})
        with self.assertRaises(native.ServiceError):
            service.submit(self.request(document=[DOCUMENT]))

    def test_parallel_same_edition_is_deduplicated(self):
        started = threading.Event()
        release = threading.Event()

        def compile_blocking(selected, workspace):
            started.set()
            self.assertTrue(release.wait(5))
            return self.compiler(selected, workspace)

        service = self.service(compiler=compile_blocking)
        first = service.submit(self.request())
        self.assertTrue(started.wait(5))
        second = service.submit(self.request())
        self.assertEqual(first["key"], second["key"])
        self.assertEqual(second["state"], "building")
        release.set()
        self.assertEqual(self.ready(service, first)["state"], "ready")
        self.assertEqual(self.compiles, 1)

    def test_queue_is_bounded_and_busy_is_retryable(self):
        release = threading.Event()

        def compile_blocking(selected, workspace):
            self.assertTrue(release.wait(5))
            return self.compiler(selected, workspace)

        for suffix in ("-two", "-three"):
            selected = {**self.selection, "id": DOCUMENT + suffix, "document": DOCUMENT + suffix}
            self.selections[(selected["document"], "main")] = selected
        service = self.service(compiler=compile_blocking, workers=1, queue_limit=1)
        first = service.submit(self.request())
        second = service.submit(self.request(document=DOCUMENT + "-two"))
        try:
            with self.assertRaises(native.ServiceError) as error:
                service.submit(self.request(document=DOCUMENT + "-three"))
            self.assertEqual(error.exception.status, 429)
        finally:
            release.set()
        self.assertEqual(self.ready(service, first)["state"], "ready")
        self.assertEqual(self.ready(service, second)["state"], "ready")

    def test_bad_receipt_or_non_pdf_cannot_be_published(self):
        def corrupt(selected, workspace):
            pdf, receipt = self.compiler(selected, workspace)
            pdf.write_bytes(b"<!doctype html>not a PDF")
            return pdf, receipt

        service = self.service(compiler=corrupt)
        result = self.ready(service, service.submit(self.request()))
        self.assertEqual(result["state"], "failed")
        self.assertIsNone(result["pdf_url"])
        self.assertEqual(list(service.objects.iterdir()), [])

    def test_receipt_for_a_different_output_cannot_be_published(self):
        def wrong_output(selected, workspace):
            pdf, receipt = self.compiler(selected, workspace)
            saved = json.loads(receipt.read_bytes())
            saved["document"]["id"] = "publication:gpt/some-other-edition"
            receipt.write_text(json.dumps(saved))
            return pdf, receipt

        service = self.service(compiler=wrong_output)
        result = self.ready(service, service.submit(self.request()))
        self.assertEqual(result["state"], "failed")
        self.assertEqual(list(service.objects.iterdir()), [])

    def test_internal_exceptions_never_leak_machine_paths_or_source_text(self):
        def failure(selected, workspace):
            raise RuntimeError("/home/private-user/secret and private source contents")

        service = self.service(compiler=failure)
        result = self.ready(service, service.submit(self.request()))
        self.assertEqual(result["state"], "failed")
        self.assertNotIn("private", result["error"])
        self.assertNotIn("/home", result["error"])

    def test_receipt_inputs_must_still_match_canonical_sources(self):
        def mutate_after_receipt(selected, workspace):
            result = self.compiler(selected, workspace)
            self.input.write_text("Changed after typesetting.\n")
            return result

        service = self.service(compiler=mutate_after_receipt)
        result = self.ready(service, service.submit(self.request()))
        self.assertEqual(result["state"], "failed")
        self.assertIn("source dependency changed", result["error"])

    def test_current_admission_is_rechecked_before_download(self):
        service = self.service()
        result = self.ready(service, service.submit(self.request()))
        self.selections.clear()
        with self.assertRaises(native.ServiceError) as error:
            service.pdf(result["key"])
        self.assertEqual(error.exception.status, 409)

    def test_verified_cache_survives_restart_and_corrupt_bytes_are_regenerated(self):
        first = self.service()
        result = self.ready(first, first.submit(self.request()))
        first.close()
        second = self.service()
        reused = second.submit(self.request())
        self.assertEqual(reused["state"], "ready")
        self.assertEqual(self.compiles, 1)
        path, _ = second.pdf(result["key"])
        path.write_bytes(b"%PDF-1.7\ncorrupt cached bytes\n%%EOF\n")
        self.assertEqual(second.status(result["key"])["state"], "failed")
        regenerated = self.ready(second, second.submit(self.request()))
        self.assertEqual(regenerated["state"], "ready")
        self.assertEqual(self.compiles, 2)

    def test_cache_key_binds_toolchain_and_source_revision(self):
        first = self.service()
        original = self.ready(first, first.submit(self.request()))
        other = self.service(toolchain="sha256:" + "c" * 64)
        changed = self.ready(other, other.submit(self.request()))
        self.assertNotEqual(original["key"], changed["key"])

    def test_receipt_cache_corruption_is_not_a_ready_download(self):
        service = self.service()
        result = self.ready(service, service.submit(self.request()))
        receipt = service.objects / result["key"] / "document.print.json"
        receipt.write_text("{}")
        self.assertEqual(service.status(result["key"])["state"], "failed")
        with self.assertRaises(native.ServiceError):
            service.pdf(result["key"])

    def test_compiler_sanitizes_environment_and_limits_an_isolated_process_group(self):
        service = self.service()
        workspace = service.work / "subprocess-fixture"
        workspace.mkdir()
        process = MagicMock(pid=123456789)
        process.wait.return_value = 0

        def start(command, **options):
            self.compiler(self.selection, workspace / "output")
            return process

        with patch.object(native.subprocess, "Popen", side_effect=start) as launch, \
                patch.object(native.os, "killpg") as kill, \
                patch.dict(native.os.environ, {"SECRET_TOKEN": "private", "TEXINPUTS": "untrusted", "MAKEFLAGS": "--evil"}):
            pdf, receipt = service.compile(self.selection, workspace)
        arguments, options = launch.call_args
        self.assertIn("RLIMIT_AS", arguments[0][2])
        self.assertIn("RLIMIT_FSIZE", arguments[0][2])
        self.assertIn(str(self.root / "tools/print-document"), arguments[0])
        self.assertTrue(options["start_new_session"])
        self.assertNotIn("shell", options)
        for secret in ("SECRET_TOKEN", "TEXINPUTS", "MAKEFLAGS"):
            self.assertNotIn(secret, options["env"])
        self.assertEqual(options["env"]["TRIPTYCH_PRINT_WORK_ROOT"], str(workspace / "native-work"))
        self.assertEqual(options["env"]["shell_escape"], "f")
        self.assertEqual(pdf.read_bytes(), PDF)
        self.assertTrue(receipt.is_file())
        kill.assert_called_with(process.pid, native.signal.SIGKILL)
        self.assertEqual(service.processes, set())

    def test_timeout_kills_and_waits_for_the_whole_compiler_process_group(self):
        service = self.service()
        workspace = service.work / "timeout-fixture"
        workspace.mkdir()
        process = MagicMock(pid=123456789)
        process.wait.side_effect = [subprocess.TimeoutExpired("native print", 1), 0]
        with patch.object(native.subprocess, "Popen", return_value=process), \
                patch.object(native.os, "killpg") as kill:
            with self.assertRaises(native.ServiceError) as error:
                service.compile(self.selection, workspace)
        self.assertIn("time limit", str(error.exception))
        kill.assert_called_with(process.pid, native.signal.SIGKILL)
        self.assertEqual(process.wait.call_count, 2)
        self.assertEqual(service.processes, set())

    def test_invalid_toolchain_and_cache_source_destinations_are_refused(self):
        for value in ("latest", "sha256:abc", "", "ghcr.io/example:latest"):
            with self.subTest(value=value), self.assertRaises(native.ServiceError):
                self.service(toolchain=value)
        for cache in (self.root, self.root / "src/cache", self.base):
            with self.subTest(cache=cache), self.assertRaises(native.ServiceError):
                native._safe_directory(cache, self.root)
        link = self.base / "cache-link"
        link.symlink_to(self.base / "real-cache")
        with self.assertRaises(native.ServiceError):
            native._safe_directory(link, self.root)

    def test_unknown_and_traversal_job_keys_are_refused(self):
        service = self.service()
        for key in ("../source", "f" * 64, "a" * 65, "%2e%2e"):
            with self.subTest(key=key), self.assertRaises(native.ServiceError):
                service.status(key)

    def test_http_submit_poll_download_and_cors(self):
        service = self.service(origins=("https://mystago.gy",))
        server = native.BoundedHTTPServer(("127.0.0.1", 0), native.handler(service))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        try:
            connection.request("GET", "/v1/health")
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read())["editions"], 1)
            connection.request("OPTIONS", "/v1/jobs", headers={"Origin": "https://mystago.gy",
                               "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "content-type"})
            response = connection.getresponse()
            self.assertEqual(response.status, 204)
            self.assertEqual(response.getheader("Access-Control-Allow-Origin"), "https://mystago.gy")
            response.read()
            connection.request("POST", "/v1/jobs", json.dumps(self.request()),
                               {"Origin": "https://mystago.gy", "Content-Type": "application/json"})
            response = connection.getresponse()
            self.assertEqual(response.status, 202)
            job = json.loads(response.read())
            result = self.ready(service, job)
            connection.request("GET", result["status_url"], headers={"Origin": "https://mystago.gy"})
            response = connection.getresponse()
            self.assertEqual(json.loads(response.read())["state"], "ready")
            connection.request("GET", result["pdf_url"])
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(response.getheader("Content-Type"), "application/pdf")
            self.assertIn("example.pdf", response.getheader("Content-Disposition"))
            self.assertEqual(response.read(), PDF)
            connection.request("GET", "/v1/health", headers={"Origin": "https://not-enabled.example"})
            response = connection.getresponse()
            self.assertEqual(response.status, 403)
            self.assertIsNone(response.getheader("Access-Control-Allow-Origin"))
            response.read()
            connection.request("GET", "/v1/jobs/../source")
            response = connection.getresponse()
            self.assertEqual(response.status, 404)
            response.read()
            connection.request("POST", "/v1/jobs", b"x" * 2049, {"Content-Type": "application/json"})
            response = connection.getresponse()
            self.assertEqual(response.status, 413)
            response.read()
        finally:
            connection.close()
            server.shutdown()
            server.server_close()
            thread.join(5)

    def test_slow_pdf_download_releases_job_lock_and_survives_cache_pruning(self):
        service = self.service()
        result = self.ready(service, service.submit(self.request()))
        entered = threading.Event()
        release = threading.Event()
        query_finished = threading.Event()
        output = io.BytesIO()
        failures = []

        class SlowWriter:
            def write(self, block):
                entered.set()
                if not release.wait(5):
                    raise AssertionError("slow download fixture was not released")
                output.write(block)

        handler = native.handler(service).__new__(native.handler(service))
        handler.headers = {}
        handler.path = result["pdf_url"]
        handler._headers = lambda *arguments: None
        handler.send_header = lambda *arguments: None
        handler.end_headers = lambda: None
        handler.connection = MagicMock()
        handler.wfile = SlowWriter()

        def download():
            try:
                handler.do_GET()
            except BaseException as error:
                failures.append(error)

        def query():
            try:
                self.assertEqual(service.submit(self.request())["state"], "ready")
            except BaseException as error:
                failures.append(error)
            finally:
                query_finished.set()

        download_thread = threading.Thread(target=download)
        query_thread = threading.Thread(target=query)
        download_thread.start()
        self.assertTrue(entered.wait(5))
        try:
            query_thread.start()
            self.assertTrue(query_finished.wait(1), "a slow PDF response held the global job lock")
            with service.lock:
                shutil.rmtree(service.objects / result["key"])
        finally:
            release.set()
            download_thread.join(5)
            query_thread.join(5)
        self.assertFalse(download_thread.is_alive())
        self.assertFalse(query_thread.is_alive())
        self.assertEqual(failures, [])
        self.assertEqual(output.getvalue(), PDF)


class SourceGuardTests(unittest.TestCase):
    def test_git_source_ref_changes_and_added_source_files_are_refused(self):
        scratch = ROOT / ".scratch/tex-print-service/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            root = Path(temporary)
            (root / "src").mkdir()
            (root / "src/input.tex").write_text("Trusted words.\n")
            def git(*arguments):
                return subprocess.run(["git", "-C", str(root), *arguments], check=True,
                                      capture_output=True, text=True).stdout.strip()
            git("init", "-q")
            git("add", "src/input.tex")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qm", "Fixture")
            revision = git("rev-parse", "HEAD")
            native.assert_source(root, revision)
            with self.assertRaises(native.ServiceError):
                native.assert_source(root, "f" * 40)
            (root / "src/extra.tex").write_text("Untracked source input.\n")
            with self.assertRaises(native.ServiceError):
                native.assert_source(root, revision)
            (root / "src/extra.tex").unlink()
            (root / "src/input.tex").write_text("Changed words.\n")
            with self.assertRaises(native.ServiceError):
                native.assert_source(root, revision)


if __name__ == "__main__":
    unittest.main()
