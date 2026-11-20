"""Retrieve the canonical native inputs produced by the print jobs in this Pages run."""
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import runpy
import select
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import zipfile
from types import SimpleNamespace


SHARDS = 8
CORPUS_JOB = "canonical-check (check-corpus-index)"


def select_artifacts(artifacts, run_id, revision):
    expected = {f"native-print-reference-{run_id}-shard-{n}": n for n in range(1, SHARDS + 1)}
    selected = {}
    for artifact in artifacts:
        n = expected.get(artifact["name"])
        if n is None or artifact["expired"]:
            continue
        source = artifact["workflow_run"]
        if (str(source["id"]) != run_id or source["head_sha"] != revision
                or n in selected or not re.fullmatch(r"sha256:[a-f0-9]{64}", artifact["digest"])):
            raise ValueError(f"unexpected Actions identity for partition {n}")
        selected[n] = artifact
    return selected


def latest_jobs(endpoint, *, prior_attempts=False):
    if not prior_attempts:
        return json.loads(subprocess.check_output(["gh", "api", f"{endpoint}/jobs?per_page=100"], timeout=30))["jobs"]
    # A partial rerun can retain successful jobs from a preceding attempt.
    # Carry the latest execution of each job name, including duplicates so
    # the caller can reject ambiguous identities.
    pages = json.loads(subprocess.check_output(["gh", "api", "--paginate", "--slurp",
                      f"{endpoint}/jobs?filter=all&per_page=100"], timeout=30))
    jobs = [job for page in pages for job in page["jobs"]]
    newest = {}
    for job in jobs:
        name = job["name"]
        newest[name] = max(newest.get(name, 0), job["run_attempt"])
    return [job for job in jobs if job["run_attempt"] == newest[job["name"]]]


def corpus_gate_passed(jobs, run_id, revision, attempt):
    """Check the completed corpus-index job and the step that ran its Make target."""
    matches = [job for job in jobs if job["name"] == CORPUS_JOB]
    if not matches:
        return False
    job = matches[0]
    if (len(matches) != 1 or str(job["run_id"]) != run_id or job["head_sha"] != revision
            or not 1 <= job["run_attempt"] <= attempt):
        raise ValueError("unexpected canonical corpus job identity")
    if job["status"] != "completed":
        return False
    checks = [step["conclusion"] for step in job["steps"] if step["name"] == "Run canonical source check"]
    if job["conclusion"] == "success" and checks == ["success"]:
        return True
    if job["run_attempt"] < attempt:
        return False  # a rerun of the failed gate may still be queued
    raise ValueError(f"{CORPUS_JOB} did not pass its source check ({job['conclusion']})")


def wait_for_corpus_gate(env):
    revision, run_id = env["GITHUB_SHA"], env["GITHUB_RUN_ID"]
    if subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() != revision:
        raise ValueError("the checkout differs from the current Pages run")
    attempt = int(env["GITHUB_RUN_ATTEMPT"])
    run = f"repos/{env['GITHUB_REPOSITORY']}/actions/runs/{run_id}"
    deadline = time.monotonic() + 90 * 60
    failures = 0
    while time.monotonic() < deadline:
        try:
            jobs = latest_jobs(run, prior_attempts=attempt > 1)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            failures += 1
            if failures >= 3:
                raise
        else:
            failures = 0
            if corpus_gate_passed(jobs, run_id, revision, attempt):
                return
        time.sleep(5)
    raise ValueError("timed out waiting for the canonical corpus check")


def fetch_partition(endpoint, artifact, destination):
    archive = destination.with_suffix(".zip")
    with archive.open("xb") as output:
        subprocess.run(["gh", "api", f"{endpoint}/artifacts/{artifact['id']}/zip"], stdout=output, check=True)
    with archive.open("rb") as incoming:
        digest = hashlib.file_digest(incoming, "sha256").hexdigest()
    if archive.stat().st_size != artifact["size_in_bytes"] or f"sha256:{digest}" != artifact["digest"]:
        raise ValueError(f"archive differs from Actions' recorded bytes for {artifact['name']}")
    # Only regular catalog and transport files, under a newly created directory.
    # An archive path cannot select where the next partition or the site is written.
    destination.mkdir()
    with zipfile.ZipFile(archive) as source:
        for entry in source.infolist():
            path = PurePosixPath(entry.filename)
            if (path.is_absolute() or ".." in path.parts or "\\" in entry.filename or not path.parts
                    or path.parts[0] not in {"catalog.json", "native-tex"}
                    or path.as_posix() != entry.filename.rstrip("/")):
                raise ValueError(f"unexpected native partition archive path: {entry.filename!r}")
            target = destination / path
            if entry.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            if stat.S_IFMT(entry.external_attr >> 16) not in (0, stat.S_IFREG):
                raise ValueError(f"unexpected partition member type for {path}")
            target.parent.mkdir(parents=True, exist_ok=True)
            with source.open(entry) as member, target.open("xb") as output:
                shutil.copyfileobj(member, output)
    archive.unlink()
    with (destination / "catalog.json").open("rb") as catalog:
        return hashlib.file_digest(catalog, "sha256").hexdigest()


def prepare(env):
    revision, run_id = env["GITHUB_SHA"], env["GITHUB_RUN_ID"]
    checkout = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    if revision != checkout:
        raise ValueError("the checkout differs from the current Pages run")
    endpoint = f"repos/{env['GITHUB_REPOSITORY']}/actions"
    output = Path(env["PAGES_NATIVE_REFERENCE_DIR"])
    with tempfile.TemporaryDirectory(dir=output.parent, prefix="print-partitions-") as folder:
        scratch = Path(folder)
        partitions = scratch / "partitions"
        partitions.mkdir()
        pending = {}
        # Matrix shards finish at different times. Download and authenticate
        # each immutable artifact by ID as soon as Actions makes it available.
        with ThreadPoolExecutor(max_workers=SHARDS) as downloads:
            run = f"{endpoint}/runs/{run_id}"
            next_job_check = time.monotonic() + 30
            completed_without_upload = set()
            while len(pending) < SHARDS:
                pages = json.loads(subprocess.check_output([
                    "gh", "api", "--paginate", "--slurp", f"{run}/artifacts?per_page=100"]))
                selected = select_artifacts((a for page in pages for a in page["artifacts"]), run_id, revision)
                for n in selected.keys() - pending.keys():
                    pending[n] = downloads.submit(fetch_partition, endpoint, selected[n], partitions / str(n))
                if len(pending) < SHARDS:
                    # A failed producer cannot upload its partition. Surface
                    # that failure while allowing normally queued shards to start.
                    if time.monotonic() >= next_job_check:
                        missing = set(range(1, SHARDS + 1)) - pending.keys()
                        jobs = {job["name"]: job for job in latest_jobs(run)}
                        for n in missing:
                            job = jobs.get(f"print-compile ({n})", {})
                            if job.get("status") == "completed":
                                if job["conclusion"] != "success" or n in completed_without_upload:
                                    raise ValueError(f"partition {n} ended with {job['conclusion']} and has no reference")
                                completed_without_upload.add(n)
                        next_job_check = time.monotonic() + 30
                    time.sleep(4)
            keys = {str(n): result.result() for n, result in pending.items()}
        manifest = scratch / "expected-keys.json"
        manifest.write_text(json.dumps(keys), encoding="utf-8")
        merged = subprocess.check_output([
            sys.executable, ".github/scripts/verify-native-print.py", "merge",
            "--references", str(partitions), "--expected-keys", str(manifest), "--out", str(output),
            "--shards", str(SHARDS), "--revision", revision, "--run-id", run_id,
            "--run-attempt", env["GITHUB_RUN_ATTEMPT"]], text=True).strip()
        if not re.fullmatch(r"[0-9a-f]{64}", merged):
            raise ValueError("the native catalog merger did not produce its identity")
        stamp = scratch / "catalog.sha256"
        stamp.write_text(merged + "\n", encoding="ascii")
        stamp.replace(output.with_name(output.name + ".sha256"))
        with open(env["GITHUB_OUTPUT"], "a", encoding="utf-8") as step:
            print(f"native-reference-sha256={merged}", file=step)
        return merged


def clear_native_reference():
    for key in ("TRIPTYCH_NATIVE_REFERENCE_DIR", "TRIPTYCH_NATIVE_REFERENCE_SHA256"):
        os.environ.pop(key, None)


@contextmanager
def prepared_inputs(reference, authenticate, report, *, figure_runner=None):
    """Hold this operation's own checked inputs and admit only its authenticated native reference."""
    clear_native_reference()
    tool = SimpleNamespace(**runpy.run_path("tools/public-alpha"))
    revision = os.environ["GITHUB_SHA"]
    tool._require_reference_checkout(revision)
    with tool.held_repository_inputs(prefetch_web=False):
        report("verified browser snapshot acquired")
        # A directory with no digest refuses any premature native source use.
        os.environ["TRIPTYCH_NATIVE_REFERENCE_DIR"] = str(reference)
        with ThreadPoolExecutor(max_workers=1) as checks:
            scan = checks.submit(copy_context().run, tool.web_data_files)
            before = tool.MANIFEST_PATH.read_bytes()
            manifest = tool.load_manifest()
            publications = tool.validate_manifest(manifest, require_active_release=True)
            included = tool.included_publications(publications, False)
            tool.prefetch_publication_dependencies(included)
            for key in included:
                tool.publication_source_identity(*key)
            report("current publication dependencies and identities prepared")
            if figure_runner:
                from _web_figure_build import prepare as prepare_figures
                products = tool.held_browser_products()
                if products is None:
                    raise tool.ReleaseError("web figures require verified web-edition products")
                candidates = os.environ.get("TRIPTYCH_WEB_FIGURE_CANDIDATES")
                figures = prepare_figures(tool.ROOT, products, tool.web_figures_root(), runner=figure_runner,
                                          candidates=Path(candidates) if candidates is not None else None)
                print(json.dumps(figures, sort_keys=True), flush=True)
            digest = authenticate()
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise ValueError("invalid protected native reference digest")
            os.environ["TRIPTYCH_NATIVE_REFERENCE_SHA256"] = digest
            report("native reference authenticated")
            scan.result()
        yield tool, before, manifest
    tool._require_reference_checkout(revision)


def current_policy(tool, before):
    tool._require_reference_checkout(os.environ["GITHUB_SHA"])
    if before != tool.MANIFEST_PATH.read_bytes():
        raise ValueError("release manifest changed during Pages build")
    manifest = tool.load_manifest()
    return manifest, tool.validate_manifest(manifest, require_active_release=True)


def build_site(figure_runner):
    start = time.monotonic()

    def report(message):
        print(f"Pages writer +{time.monotonic() - start:.2f}s: {message}", flush=True)

    reference = Path(os.environ["PAGES_NATIVE_REFERENCE_DIR"])
    with os.fdopen(int(os.environ["PAGES_WRITER_REFERENCE_FD"]), "r") as receipt:
        with prepared_inputs(reference, lambda: receipt.read().strip(), report, figure_runner=figure_runner) as held:
            tool, before, early_manifest = held
            tool.site_source_paths(early_manifest)
            report("writer canonical sources ready")
            manifest, publications = current_policy(tool, before)
            output = tool.build_site(manifest, publications, False)
            report(f"site written to {output.relative_to(tool.ROOT)}; rechecking source snapshot")
    report("writer final source checks passed")


def verify_site():
    """Prepare independent release inputs while the full, separately gated Pages build runs."""
    start = time.monotonic()

    def report(message):
        print(f"Pages verification +{time.monotonic() - start:.2f}s: {message}", flush=True)

    report("starting independent reference retrieval and browser product preparation")
    image = os.environ["TEXLIVE_IMAGE"]
    if not re.fullmatch(r"ghcr\.io/[a-z0-9._/-]+@sha256:[0-9a-f]{64}", image):
        raise ValueError("TEXLIVE_IMAGE must name an immutable digest")
    children = set()
    env = {**os.environ, **dict.fromkeys(
        ("GITHUB_OUTPUT", "GITHUB_ENV", "GITHUB_PATH", "GITHUB_STATE", "GITHUB_STEP_SUMMARY"), os.devnull)}
    clear_native_reference()
    for key in ("TRIPTYCH_NATIVE_REFERENCE_DIR", "TRIPTYCH_NATIVE_REFERENCE_SHA256"):
        env.pop(key, None)

    def spawn(command, **kwargs):
        child = subprocess.Popen(command, start_new_session=True, **kwargs)
        children.add(child)
        return child

    def succeeded(child):
        if status := child.wait():
            raise subprocess.CalledProcessError(status, child.args)
        children.remove(child)

    def interrupt(signum, _frame):
        raise InterruptedError(f"Pages coordination interrupted by signal {signum}")

    temporary = tempfile.TemporaryDirectory(dir=env["RUNNER_TEMP"], prefix="pages-verified-")
    prior = signal.signal(signal.SIGTERM, interrupt)
    try:
        verifier = Path(temporary.name) / "verifier"
        reference = spawn([sys.executable, __file__, "--digest"], stdout=subprocess.PIPE, text=True,
                          env={**env, "PAGES_NATIVE_REFERENCE_DIR": str(verifier)})
        succeeded(spawn(["make", "prepare-browser-data"], env=env))
        report("browser products prepared; starting complete source gates and site assembly")
        writer_dir = Path(temporary.name) / "writer"
        writer_reference = spawn([sys.executable, __file__, "--digest"], stdout=subprocess.PIPE, text=True,
                                 env={**env, "PAGES_NATIVE_REFERENCE_DIR": str(writer_dir)})
        with writer_reference.stdout as pipe:
            writer = spawn(["make", "-j3", "--assume-old=prepare-browser-data", "pages-site",
                            f"WEB_FIGURES_RUNNER=docker:{image}"], pass_fds=(pipe.fileno(),),
                           env={**env, "PAGES_NATIVE_REFERENCE_DIR": str(writer_dir),
                                "PAGES_WRITER_REFERENCE_FD": str(pipe.fileno())})

        def authenticate():
            # A failed gate may finish before the parallel GitHub download.
            with os.fdopen(os.pidfd_open(writer.pid), "rb") as exit_fd, reference.stdout:
                ready, _, _ = select.select((exit_fd, reference.stdout), (), ())
                if exit_fd in ready and writer.wait():
                    raise subprocess.CalledProcessError(writer.returncode, writer.args)
                digest = reference.stdout.read().strip()
            succeeded(reference)
            return digest

        with prepared_inputs(verifier, authenticate, report) as (tool, before, manifest):
            tool.site_source_paths(manifest)
            report("independent source expectations ready")
            succeeded(writer)
            succeeded(writer_reference)
            manifest, publications = current_policy(tool, before)
            report("all source gates passed; opening the assembled artifact for read-back")
            tool.verify_output(manifest, publications, tool.OUTPUT_ROOT / "site", False)
            tool.validate_deployment_target(tool.artifact_authorization(
                manifest, tool.included_publications(publications, False)), "github-pages")
            report("artifact read-back and deployment target passed; rechecking source snapshot")
        report("artifact, deployment target and final source checks passed")
    finally:
        for sig in (signal.SIGTERM, signal.SIGKILL):
            for child in children:
                try:
                    os.killpg(child.pid, sig)
                except ProcessLookupError:
                    pass
            if children and sig == signal.SIGTERM:
                time.sleep(.25)
        for child in children:
            child.wait()
        temporary.cleanup()
        signal.signal(signal.SIGTERM, prior)


if __name__ == "__main__":
    try:
        if sys.argv[1:] == ["--verify-site"]:
            verify_site()
        elif sys.argv[1:] == ["--corpus-gate"]:
            wait_for_corpus_gate(os.environ)
        elif len(sys.argv) == 3 and sys.argv[1] == "--build-site":
            build_site(sys.argv[2])
        elif sys.argv[1:] == ["--digest"]:
            print(prepare({**os.environ, "GITHUB_OUTPUT": os.devnull}))
        elif not sys.argv[1:]:
            prepare(os.environ)
        else:
            raise ValueError("expected --verify-site, --corpus-gate, --digest or no argument")
    except (KeyError, OSError, ValueError, zipfile.BadZipFile, subprocess.SubprocessError) as error:
        sys.exit(f"native print reference: {error}")
