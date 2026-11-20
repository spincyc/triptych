"""Exercise the Pages source preparation and artifact barrier with real child processes."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[2]
COORDINATOR = ROOT / ".github/scripts/pages-native-reference.py"
# Keep the actual coordinator and GNU Make. These two small fixtures stand in
# for the remote Actions archive and the expensive source/artifact validators.
CALL_COORDINATOR = """
import importlib.util
from pathlib import Path
import sys
spec = importlib.util.spec_from_file_location("pages_native_reference", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.__file__ = str(Path("fetch-reference.py").resolve())
module.verify_site()
"""
REFERENCE = """
import os
from pathlib import Path
import signal
import sys
import time

assert sys.argv[1:] == ["--digest"]
assert os.environ["PAGES_NATIVE_REFERENCE_DIR"].endswith("/verifier")
if os.environ["FAIL"] == "early":
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    Path("reference-pid").write_text(str(os.getpid()))
    with open("reference-started", "wb") as ready:
        ready.write(b"R")
    time.sleep(90)
if os.environ["FAIL"] == "hold-reference":
    for stage in ("initial-policy", "browser-scan"):
        with open(stage, "rb") as work:
            assert work.read() == b"ready"
print("invalid" if os.environ["FAIL"] == "digest" else "a" * 64)
"""
MAKEFILE = """
.PHONY: pages-site prepare-browser-data writer gate
prepare-browser-data:
	@echo prepare >> preparations
	@test "$(FAIL)" != "prepare"
pages-site: writer gate
writer: | prepare-browser-data
	@echo bbbbbbbb > "$$PAGES_NATIVE_REFERENCE_DIR.sha256"
	@touch writer-complete
gate:
	@if [ "$(FAIL)" = early ]; then cat reference-started > /dev/null; exit 2; fi
	@cat prewarmed > gate-check
	@test "$(FAIL)" != "gate"
	@if [ "$(FAIL)" = manifest ]; then echo changed > manifest; fi
	@touch gate-complete
"""
PUBLIC_ALPHA = """
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path
import os

SNAPSHOT = ContextVar("snapshot")
MANIFEST_PATH = Path("manifest")
OUTPUT_ROOT = Path("output")
failure = os.environ["FAIL"]

def load_manifest():
    return {"text": MANIFEST_PATH.read_text()}

def validate_manifest(manifest, require_active_release):
    assert require_active_release
    if not Path("policies").exists():
        assert SNAPSHOT.get() == "private browser snapshot"
        assert os.environ["TRIPTYCH_NATIVE_REFERENCE_DIR"].endswith("/verifier")
        assert "TRIPTYCH_NATIVE_REFERENCE_SHA256" not in os.environ
        if failure == "hold-reference":
            with open("initial-policy", "wb") as signal:
                signal.write(b"ready")
    with open("policies", "a") as policy:
        print("check", file=policy)
    if failure == "expired" and Path("gate-complete").exists():
        raise ValueError("expired release")
    return {}

def _require_reference_checkout(revision):
    assert revision == os.environ["GITHUB_SHA"]
    with open("clean-checks", "a") as checks:
        print("clean", file=checks)
    if (failure == "dirty-first" or (failure == "dirty" and Path("gate-complete").exists())
            or (failure == "dirty-final" and Path("checked-end").exists())):
        raise ValueError("dirty checkout")

def web_data_files():
    assert SNAPSHOT.get() == "private browser snapshot"
    if failure == "hold-reference":
        assert "TRIPTYCH_NATIVE_REFERENCE_SHA256" not in os.environ
        with open("browser-scan", "wb") as signal:
            signal.write(b"ready")
    if failure == "scan":
        raise ValueError("browser JSON scan failed")
    Path("scanned").touch()


def site_source_paths(manifest):
    assert Path("scanned").exists()
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_DIR"].endswith("/verifier")
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_SHA256"] == "a" * 64
    with open("prewarmed", "wb") as signal:
        signal.write(b"W")

def verify_output(manifest, publications, path, preview):
    assert not preview and path == OUTPUT_ROOT / "site"
    assert Path("gate-complete").exists()
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_SHA256"] == "a" * 64
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_DIR"].endswith("/verifier")
    Path("opened-artifact").touch()

def included_publications(publications, preview):
    return []

def artifact_authorization(manifest, items):
    return {}

def validate_deployment_target(authorization, target):
    assert target == "github-pages"
    if failure == "target":
        raise ValueError("unmet target")

@contextmanager
def held_repository_inputs(*, prefetch_web):
    assert not prefetch_web
    assert "TRIPTYCH_NATIVE_REFERENCE_DIR" not in os.environ
    assert "TRIPTYCH_NATIVE_REFERENCE_SHA256" not in os.environ
    assert Path("clean-checks").exists()
    SNAPSHOT.set("private browser snapshot")
    yield
    if failure == "final":
        raise ValueError("final source drift")
    Path("checked-end").touch()
"""


@unittest.skipUnless(hasattr(os, "pidfd_open"), "requires Linux process descriptors used on the Pages runner")
class PagesCoordinatorTests(unittest.TestCase):
    def run_build(self, failure=""):
        scratch = ROOT / ".scratch/pages-coordinator-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        work = Path(temporary.name)
        (work / "tools").mkdir()
        (work / "tools/public-alpha").write_text(PUBLIC_ALPHA)
        (work / "manifest").write_text("approved\n")
        (work / "Makefile").write_text(MAKEFILE)
        (work / "fetch-reference.py").write_text(REFERENCE)
        for name in ("prewarmed", "reference-started", "initial-policy", "browser-scan"):
            os.mkfifo(work / name)
        env = {**os.environ, "FAIL": failure, "RUNNER_TEMP": str(work), "GITHUB_SHA": "a" * 40,
               "TEXLIVE_IMAGE": "ghcr.io/a/b@sha256:" + "a" * 64,
               "TRIPTYCH_NATIVE_REFERENCE_SHA256": "d" * 64, "TRIPTYCH_NATIVE_REFERENCE_DIR": "untrusted"}
        result = subprocess.run(
            [sys.executable, "-B", "-c", CALL_COORDINATOR, str(COORDINATOR)], cwd=work, env=env,
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual((work / "preparations").read_text().splitlines(), ["prepare"])
        return work, result

    def test_independent_preparation_and_successful_full_make_precede_artifact(self):
        work, result = self.run_build("hold-reference")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((work / "clean-checks").read_text().splitlines(), ["clean"] * 3)
        self.assertEqual((work / "policies").read_text().splitlines(), ["check", "check"])
        self.assertTrue((work / "opened-artifact").exists())
        self.assertTrue((work / "checked-end").exists())
        events = ["starting independent reference retrieval", "independent source expectations ready",
                  "opening the assembled artifact", "artifact, deployment target and final source checks passed"]
        positions = [result.stdout.index(event) for event in events]
        self.assertEqual(positions, sorted(positions))

    def test_failed_source_gate_product_preparation_or_reference_prevents_artifact_access(self):
        for failure in ("gate", "prepare", "digest", "scan", "dirty-first"):
            with self.subTest(failure=failure):
                work, result = self.run_build(failure)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((work / "opened-artifact").exists())
                if failure == "prepare":
                    self.assertFalse((work / "writer-complete").exists())

    def test_checkout_manifest_and_active_release_are_checked_after_full_make(self):
        for failure in ("dirty", "manifest", "expired"):
            with self.subTest(failure=failure):
                work, result = self.run_build(failure)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue((work / "gate-complete").exists())
                self.assertFalse((work / "opened-artifact").exists())

    def test_target_and_final_snapshot_errors_fail_the_operation(self):
        for failure in ("target", "final"):
            with self.subTest(failure=failure):
                work, result = self.run_build(failure)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue((work / "opened-artifact").exists())
                self.assertFalse((work / "checked-end").exists())

    def test_late_checkout_drift_after_snapshot_closes_fails_verification(self):
        work, result = self.run_build("dirty-final")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((work / "opened-artifact").exists())
        self.assertTrue((work / "checked-end").exists())
        self.assertNotIn("artifact, deployment target and final source checks passed", result.stdout)

    def test_early_gate_failure_kills_a_stalled_reference_download(self):
        start = time.monotonic()
        work, result = self.run_build("early")
        self.assertLess(time.monotonic() - start, 10)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((work / "opened-artifact").exists())
        self.assertFalse(Path("/proc", (work / "reference-pid").read_text()).exists())
