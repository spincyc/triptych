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
role = Path(os.environ["PAGES_NATIVE_REFERENCE_DIR"]).name
assert role in {"writer", "verifier"}
if os.environ["FAIL"] == "early" and role == "verifier":
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    Path("reference-pid").write_text(str(os.getpid()))
    with open("reference-started", "wb") as ready:
        ready.write(b"R")
    time.sleep(90)
if os.environ["FAIL"] == "hold-reference":
    stages = ["browser-scan", "admission-census"] + (["figures"] if role == "writer" else [])
    for stage in stages:
        with open(stage + "-" + role, "rb") as work:
            assert work.read() == b"ready"
failure = os.environ["FAIL"]
print("invalid" if failure in ("digest", "digest-" + role) else ("a" if role == "verifier" else "b") * 64)
"""
MAKEFILE = """
.PHONY: pages-protected-writer prepare-browser-data check-curriculum-source-rights writer gate
prepare-browser-data:
	@echo prepare >> preparations
	@test "$(FAIL)" != "prepare"
check-curriculum-source-rights:
	@echo rights >> rights-checks
	@test "$(FAIL)" != "rights"
pages-protected-writer: writer gate
writer: check-curriculum-source-rights | prepare-browser-data
	@echo bbbbbbbb > "$$PAGES_NATIVE_REFERENCE_DIR.sha256"
	@"$$COORDINATOR_PYTHON" "$$COORDINATOR_TOOL" --build-site '$(WEB_FIGURES_RUNNER)'
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
ROOT = Path.cwd()
MANIFEST_PATH = Path("manifest")
OUTPUT_ROOT = Path("output")
failure = os.environ["FAIL"]
role = "writer" if "PAGES_WRITER_REFERENCE_FD" in os.environ else "verifier"
policies = Path("policies" if role == "verifier" else "writer-policies")
clean = Path("clean-checks" if role == "verifier" else "writer-clean-checks")

def load_manifest():
    return {"text": MANIFEST_PATH.read_text()}

def validate_manifest(manifest, require_active_release):
    assert require_active_release
    if not policies.exists():
        assert SNAPSHOT.get() == "private browser snapshot"
        assert os.environ["TRIPTYCH_NATIVE_REFERENCE_DIR"].endswith("/" + role)
        assert Path("source-facts-" + role).exists()
    with open(policies, "a") as policy:
        print("check", file=policy)
    if role == "verifier" and failure == "expired" and Path("gate-complete").exists():
        raise ValueError("expired release")
    return {}

def _require_reference_checkout(revision):
    assert revision == os.environ["GITHUB_SHA"]
    with open(clean, "a") as checks:
        print("clean", file=checks)
    if role == "verifier" and (failure == "dirty-first" or (failure == "dirty" and Path("gate-complete").exists())
            or (failure == "dirty-final" and Path("checked-end").exists())):
        raise ValueError("dirty checkout")

def web_data_files():
    assert SNAPSHOT.get() == "private browser snapshot"
    if failure == "hold-reference":
        assert "TRIPTYCH_NATIVE_REFERENCE_SHA256" not in os.environ
        with open("browser-scan-" + role, "wb") as signal:
            signal.write(b"ready")
    if failure == "scan":
        raise ValueError("browser JSON scan failed")
    Path("scanned" + role).touch()


def site_source_paths(manifest):
    assert Path("held-census-" + role).is_file()
    assert Path("scanned" + role).exists()
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_DIR"].endswith("/" + role)
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_SHA256"] == ("a" if role == "verifier" else "b") * 64
    if role == "verifier":
        with open("prewarmed", "wb") as signal:
            signal.write(b"W")

def verify_output(manifest, publications, path, preview):
    assert not preview and path == OUTPUT_ROOT / "site"
    assert Path("gate-complete").exists()
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_SHA256"] == "a" * 64
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_DIR"].endswith("/" + role)
    Path("opened-artifact").touch()

def included_publications(publications, preview):
    return {("gpt", "one"): {}, ("claude", "two"): {}}

@contextmanager
def held_source_admissions(root):
    assert root == ROOT and not os.environ.get("TRIPTYCH_NATIVE_REFERENCE_SHA256")
    assert clean.exists() and SNAPSHOT.get() == "private browser snapshot"
    path = Path("held-census-" + role)
    path.touch(exist_ok=False)
    try:
        if failure == "hold-reference":
            with open("admission-census-" + role, "wb") as signal:
                signal.write(b"ready")
        yield
    finally:
        path.unlink()

def _hold_pages_publication_sources(shards):
    assert Path("held-census-" + role).is_file()
    assert shards == 8
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_SHA256"] == ("a" if role == "verifier" else "b") * 64
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_DIR"].endswith("/" + role)
    Path("source-facts-" + role).touch()

def publication_source_identity(provider, output):
    assert Path("source-facts-" + role).exists()
    with open("identities-checked-" + role, "a") as log:
        print(provider, output, file=log)
    if failure == "identity-" + role:
        raise ValueError("unapproved source identity")

def held_browser_products():
    return SNAPSHOT.get()

def web_figures_root():
    return ROOT / "web-figures"

def build_site(manifest, publications, preview):
    assert role == "writer" and not preview
    assert Path("scannedwriter").exists() and Path("figures-ready").exists()
    assert os.environ["TRIPTYCH_NATIVE_REFERENCE_SHA256"] == "b" * 64
    Path("writer-complete").touch()
    return ROOT / "output/site"

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
    assert clean.exists()
    SNAPSHOT.set("private browser snapshot")
    yield
    if role == "verifier" and failure == "final":
        raise ValueError("final source drift")
    if role == "verifier":
        Path("checked-end").touch()
"""


FIGURES = """
from pathlib import Path
import os
def prepare(root, products, out, *, runner, candidates):
    assert root == Path.cwd() and out == root / "web-figures"
    assert products == "private browser snapshot"
    assert runner == "docker:" + os.environ["TEXLIVE_IMAGE"]
    assert candidates == Path("figure-candidates")
    assert "TRIPTYCH_NATIVE_REFERENCE_SHA256" not in os.environ
    if os.environ["FAIL"] == "figures":
        raise ValueError("figure source failed")
    if os.environ["FAIL"] == "hold-reference":
        with open("figures-writer", "wb") as signal:
            signal.write(b"ready")
    Path("figures-ready").touch()
    return {"ok": True}
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
        (work / "_web_figure_build.py").write_text(FIGURES)
        (work / "manifest").write_text("approved\n")
        (work / "Makefile").write_text(MAKEFILE)
        (work / "fetch-reference.py").write_text(REFERENCE)
        for name in ["prewarmed", "reference-started", "figures-writer",
                     *(s + "-" + role for role in ("writer", "verifier") for s in ("browser-scan", "admission-census"))]:
            os.mkfifo(work / name)
        env = {**os.environ, "FAIL": failure, "PYTHONPATH": str(work), "COORDINATOR_TOOL": str(COORDINATOR),
               "COORDINATOR_PYTHON": sys.executable, "TRIPTYCH_WEB_FIGURE_CANDIDATES": "figure-candidates", "RUNNER_TEMP": str(work), "GITHUB_SHA": "a" * 40,
               "TEXLIVE_IMAGE": "ghcr.io/a/b@sha256:" + "a" * 64,
               "TRIPTYCH_NATIVE_REFERENCE_SHA256": "d" * 64, "TRIPTYCH_NATIVE_REFERENCE_DIR": "untrusted"}
        result = subprocess.run(
            [sys.executable, "-B", "-c", CALL_COORDINATOR, str(COORDINATOR)], cwd=work, env=env,
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual((work / "preparations").read_text().splitlines(), ["prepare"])
        self.assertEqual((work / "rights-checks").read_text().splitlines(), ["rights"])
        return work, result

    def test_independent_preparation_and_successful_full_make_precede_artifact(self):
        work, result = self.run_build("hold-reference")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((work / "clean-checks").read_text().splitlines(), ["clean"] * 3)
        self.assertEqual((work / "policies").read_text().splitlines(), ["check", "check"])
        self.assertTrue((work / "opened-artifact").exists())
        self.assertTrue((work / "checked-end").exists())
        self.assertTrue((work / "writer-complete").exists())
        writer_events = ["writer canonical sources ready", "site written to output/site", "writer final source checks passed"]
        marker_positions = [result.stdout.index(event) for event in writer_events]
        self.assertEqual(marker_positions, sorted(marker_positions))
        for role in ("verifier", "writer"):
            self.assertEqual((work / ("identities-checked-" + role)).read_text().splitlines(), ["gpt one", "claude two"])
        events = ["starting independent reference retrieval", "verified browser snapshot acquired",
                  "independent source expectations ready", "opening the assembled artifact",
                  "artifact read-back and deployment target passed", "artifact, deployment target and final source checks passed"]
        positions = [result.stdout.index(event) for event in events]
        self.assertEqual(positions, sorted(positions))

    def test_failed_source_gate_product_preparation_or_reference_prevents_artifact_access(self):
        for failure in ("gate", "prepare", "rights", "digest", "scan", "dirty-first", "digest-writer",
                        "identity-writer", "identity-verifier", "figures"):
            with self.subTest(failure=failure):
                work, result = self.run_build(failure)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((work / "opened-artifact").exists())
                if failure in ("prepare", "rights"):
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
