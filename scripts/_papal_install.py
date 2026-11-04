"""Validate the historical papal reader release record.

`release/papal-documents.json` records the papal reader PDFs that were once
installed under `pdf/papal-documents/`, with their source selections, render
receipts, page reviews and retained evidence. Installation into that tree was
retired on 2026-11-04: readers are served from retained source text and printed
on demand, so nothing here writes a PDF or the release record. What remains is
the metadata check `scripts/_papal_input_receipt.py check` runs, which proves
the record still agrees with the current source plan and its attested inputs
without opening a PDF or an original snapshot.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

import _papal_collection as collection
import _snapshot_store
from _papal_input_receipt import InputRecords

ROOT = Path(__file__).resolve().parents[1]
RELEASE_SCHEMA = "triptych-papal-release/v1"
RELEASE = Path("release/papal-documents.json")
# Where the retired installer put each reader. The release record names every
# reader by the filename `_filename` derives under this root, so the check still
# needs the rule; nothing creates or reads files there.
PDF_ROOT = Path("pdf/papal-documents")
ARCHIVE_ROOT = Path("release/papal-documents")


class PapalInstallError(collection.PapalCollectionError):
    pass


def _require(condition, message):
    if not condition:
        raise PapalInstallError(message)


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _payload(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def _safe(value):
    _require(isinstance(value, str) and value and not any(ord(char) < 32 for char in value), "invalid release path")
    path = Path(value)
    _require(not path.is_absolute() and ".." not in path.parts and "\\" not in value, "release path must be relative without traversal")
    current = ROOT
    for part in path.parts:
        current /= part
        _require(not current.is_symlink(), "release paths must not contain symlinks")
    _require(current.resolve().is_relative_to(ROOT), "release path escapes the repository")
    return current


def _normalized(row, manifest):
    result = copy.deepcopy(row)
    result.pop("collection_corpus", None)
    result["revision"] = row.get("revision", manifest["revision"])
    return result


def _fresh_plan(path):
    """Re-resolve Make's optional inputs, including newly added withdrawals."""
    scratch = ROOT / ".scratch/papal-install"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as directory:
        target = Path(directory) / "current-manifest.json"
        environment = {key: value for key, value in os.environ.items()
                       if key not in {"MAKEFLAGS", "MFLAGS", "MAKEOVERRIDES"} and not key.startswith("PAPAL_")}
        run = subprocess.run(["make", "--no-print-directory", "papal-plan", f"PAPAL_CURRENT_MANIFEST={target}"],
                             cwd=ROOT, env=environment, capture_output=True, text=True)
        _require(run.returncode == 0, "cannot regenerate the current source plan: " + run.stderr.strip())
        fresh, fresh_sha, _ = collection._manifest(target)
    supplied, supplied_sha = fresh, fresh_sha
    if path is not None:
        supplied, supplied_sha, _ = collection._manifest(Path(path).resolve())
    _require(supplied_sha == fresh_sha, "source plan is stale; regenerate papal-plan before installing")
    provenance = supplied.get("selection_plan")
    _require(isinstance(provenance, dict) and provenance.get("schema") == collection.PLAN_SCHEMA,
             "installation requires an explicit current source-selection plan")
    for item in provenance["inputs"]:
        _require(collection._sha(_safe(item["path"])) == item["sha256"], "canonical source input changed after planning")
    return fresh, supplied_sha


def _filename(source):
    identity = source["id"] + "--" + source["language"]
    safe = re.sub(r"[^a-z0-9.-]+", "-", identity.lower()).strip(".-")[:145]
    _require(bool(safe), "source identity cannot form a safe PDF filename")
    token = hashlib.sha256(identity.encode()).hexdigest()[:16]
    return (PDF_ROOT / ((source.get("date") or "unknown-date") + "--" + safe + "--" + token + ".pdf")).as_posix()


def _validate_pass(row, audit, review, reports=None):
    """Reuse the collector's exact PDF/receipt/page/report/reuse proof gate."""
    projected = copy.deepcopy(review)
    if reports is not None:
        projected["report"] = reports[projected["report"]]["path"]
        for proof in projected.get("reuse_proofs", []):
            proof["prior_report"] = reports[proof["prior_report"]]["path"]
    data = {"schema": collection.REVIEW_SCHEMA, "frozen_receipt_sha256": audit["frozen_receipt_sha256"],
            "documents": [projected]}
    scratch = ROOT / ".scratch/papal-install"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as directory:
        path = Path(directory) / "review.json"
        path.write_bytes(_payload(data))
        selected = copy.deepcopy(row)
        selected["page_review"] = {"status": "not-recorded"}
        try:
            collection._reviews([selected], [path], ROOT)
        except collection.PapalCollectionError as error:
            raise PapalInstallError(f"{row['id']} ({row['language']}): {error}") from error
    _require(selected["page_review"]["status"] == "pass", "installation requires complete layout PASS evidence")
    return selected["page_review"]


def _owned_release():
    path = _safe(RELEASE.as_posix())
    if not path.exists():
        return None
    data, _ = collection._json(path)
    _require(data.get("schema") == RELEASE_SCHEMA and data.get("generator") == "typeset-papal install"
             and isinstance(data.get("documents"), list), "existing release is not owned by this installer")
    return data


def _archived(ref):
    _require(collection._digest(ref.get("sha256")) and type(ref.get("bytes")) is int and ref["bytes"] > 0,
             "invalid durable evidence pins")
    path = _safe(ref["path"])
    if ref["path"].startswith(_snapshot_store.PREFIX):
        _snapshot_store.validate_ref(ROOT, ref, require_bytes=True)
        return _snapshot_store.resolve(ROOT, ref["path"], fetch=False)
    _require(path.is_relative_to(_safe(ARCHIVE_ROOT.as_posix())) and path.is_file(), "missing durable release evidence")
    _require(collection._sha(path) == ref["sha256"] and path.stat().st_size == ref["bytes"], "durable release evidence hash/size mismatch")
    return path


def check_release_metadata(plan=None):
    """Validate all release selections and reviews without opening a PDF or original."""
    current, current_sha = _fresh_plan(plan)
    release = _owned_release()
    _require(release is not None, "no papal release record")
    records = InputRecords(ROOT)
    _require(records.index is not None,
             "metadata release validation requires recorded original header/row extracts")
    owned = {}
    for row in release["documents"]:
        _require(row["pdf"] not in owned and row["pdf"] == _filename(row["source"]),
                 "duplicate released identity or unexpected historical filename")
        owned[row["pdf"]] = row
    for ref in release["evidence"]:
        if not ref["path"].startswith(_snapshot_store.PREFIX):
            _archived(ref)
        else:
            records.validate_ref(ref)
    frozen_plan = records.header(release["source_plan"])
    for item in frozen_plan["selection_plan"]["inputs"]:
        _require(any(ref["sha256"] == item["sha256"] for ref in records.index["originals"].values()),
                 "retained source plan input identity is missing")
    active = {collection._identity(row): _normalized(row, current) for row in current["documents"]}
    frozen = {collection._identity(row): _normalized(row, frozen_plan) for row in records.plan_rows(release["source_plan"])}
    identities = set()
    for row in owned.values():
        key = collection._identity(row)
        _require(type(row.get("pages")) is int and row["pages"] > 0 and type(row.get("bytes")) is int and row["bytes"] > 0,
                 "installed PDF requires integer page and byte counts")
        _require(key not in identities and row["pdf"] == _filename(row["source"]), "duplicate installed identity or unexpected owned filename")
        identities.add(key)
        _require(key in active and _canonical(active[key]) == _canonical(row["source"]), "installed PDF is no longer a current source selection")
        _require(key in frozen and _canonical(frozen[key]) == _canonical(row["source"]), "installed PDF is absent from its retained source plan")
        manifest = records.header(row["manifest"])
        source = records.row(row["manifest"], row["manifest"]["row_index"])
        _require(_canonical(_normalized(source, manifest)) == _canonical(row["source"]), "retained frozen manifest selection disagrees")
        receipt = records.header(row["receipt"])
        receipt_sha = row["receipt"]["sha256"]
        item = records.row(row["receipt"], row["receipt"]["row_index"])
        _require(collection._identity(item) == key and item.get("status") == "compiled"
                 and item.get("pdf_sha256") == row["pdf_sha256"] and item.get("pages") == row["pages"]
                 and item.get("render_revision", receipt["revision"]) == row["render_revision"]
                 and item.get("text_fidelity", {}).get("status") == "pass", "retained receipt disagrees with installed PDF")
        _require(receipt["revision"] == manifest["revision"], "retained receipt/manifest revisions disagree")
        _require(row["render_revision"] == row["source"]["revision"], "installed render revision disagrees with its source selection")
        if "input_manifest_sha256" in receipt:
            _require(receipt["input_manifest_sha256"] == row["manifest"]["sha256"], "retained receipt frozen-manifest hash disagrees")
        for output, original in (("artifact_id", "artifact_id"), ("source_sha256", "sha256"),
                                 ("segment_id", "segment_id"), ("physical_line_ranges", "physical_line_ranges")):
            _require(item.get(output) == source.get(original), "retained receipt source identity disagrees")
        audit = records.header(row["review"]["audit"])
        review = records.row(row["review"]["audit"], row["review"]["audit"]["row_index"])
        _require(row["review"]["current_receipt_sha256"] == receipt_sha
                 and row["review"]["original_receipt_sha256"] == review.get("receipt_sha256", audit["frozen_receipt_sha256"]),
                 "release review receipt provenance disagrees")
        for ref in row["review"]["reports"].values():
            _archived(ref)
        fake = {"id": key[0], "language": key[1], "pdf_sha256": row["pdf_sha256"], "pages": row["pages"],
                "status": "compiled", "receipt_sha256": receipt_sha, "files": {}}
        _validate_pass(fake, audit, review, row["review"]["reports"])
    known_states = {collection._identity(row): row for row in release["delivery_states"]}
    uninstalled = []
    for key, source in active.items():
        if key in identities:
            continue
        state = {"id": key[0], "language": key[1], "status": "not-installed"}
        previous = known_states.get(key)
        selection_hash = hashlib.sha256(_canonical(source).encode()).hexdigest()
        if previous and previous.get("selection_sha256") == selection_hash:
            state["last_prepared_status"] = previous["status"]
        uninstalled.append(state)
    return {"schema": RELEASE_SCHEMA, "status": "valid", "installed": len(owned), "current": len(active),
            "not_installed": len(active) - len(owned), "source_plan_sha256": current_sha,
            "release_plan_is_current": current_sha == release["source_plan"]["sha256"], "uninstalled": uninstalled,
            "verification": "mechanically-attested-release-metadata"}
