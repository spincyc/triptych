"""Retrieve the canonical native inputs produced by the print jobs in this Pages run."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile


SHARDS = 8


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


def latest_jobs(endpoint):
    return json.loads(subprocess.check_output(["gh", "api", f"{endpoint}/jobs?per_page=100"]))["jobs"]


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


if __name__ == "__main__":
    try:
        prepare(os.environ)
    except (KeyError, OSError, ValueError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        sys.exit(f"native print reference: {error}")
