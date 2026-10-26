"""Install exact, current, fully page-reviewed papal reading PDFs.

The delivery matrix is deliberately not an authority: every candidate is matched
against a fresh source plan, its frozen receipt, and its original review record.
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
from urllib.parse import unquote

import _papal_collection as collection

ROOT = Path(__file__).resolve().parents[1]
PREPARED_SCHEMA = "triptych-papal-install-plan/v1"
RELEASE_SCHEMA = "triptych-papal-release/v1"
PAIRS_SCHEMA = "triptych-papal-render-batch-pairs/v1"
RELEASE = Path("release/papal-documents.json")
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


def _relative(path):
    path = Path(path).resolve()
    _require(path.is_relative_to(ROOT), "installation input escapes the repository")
    return path.relative_to(ROOT).as_posix()


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
    supplied, supplied_sha, _ = collection._manifest(Path(path).resolve())
    _require(supplied_sha == fresh_sha, "source plan is stale; regenerate papal-plan before installing")
    provenance = supplied.get("selection_plan")
    _require(isinstance(provenance, dict) and provenance.get("schema") == collection.PLAN_SCHEMA,
             "installation requires an explicit current source-selection plan")
    for item in provenance["inputs"]:
        _require(collection._sha(_safe(item["path"])) == item["sha256"], "canonical source input changed after planning")
    return fresh, supplied_sha


def _archive(path, kind, archives, expected_sha=None):
    path = Path(path).resolve()
    relative = _relative(path)
    existing = next((row for row in archives.values() if row["source"] == relative), None)
    if existing is not None:
        _require(expected_sha is None or existing["sha256"] == expected_sha, "conflicting release evidence pins")
        return {key: existing[key] for key in ("path", "sha256", "bytes")}
    payload = path.read_bytes()
    # These are project records, never a dump of a machine's runtime state.
    text = payload.decode("utf-8")
    _require(str(ROOT) not in text and not re.search(r"/(?:home|Users|tmp|var/tmp)/", text),
             "release evidence contains a machine-specific path")
    digest = hashlib.sha256(payload).hexdigest()
    _require(expected_sha is None or digest == expected_sha, "release evidence changed while preparing")
    suffix = ".md" if kind == "report" else ".json"
    folder = "reports" if kind == "report" else "inputs"
    destination = (ARCHIVE_ROOT / folder / (digest + suffix)).as_posix()
    record = {"path": destination, "sha256": digest, "bytes": len(payload)}
    previous = archives.get(destination)
    _require(previous is None or previous["sha256"] == digest, "conflicting evidence archive")
    archives[destination] = dict(record, source=relative, kind=kind)
    return record


def _filename(source):
    identity = source["id"] + "--" + source["language"]
    safe = re.sub(r"[^a-z0-9.-]+", "-", identity.lower()).strip(".-")[:145]
    _require(bool(safe), "source identity cannot form a safe PDF filename")
    token = hashlib.sha256(identity.encode()).hexdigest()[:16]
    return (PDF_ROOT / ((source.get("date") or "unknown-date") + "--" + safe + "--" + token + ".pdf")).as_posix()


def _source_check(source, pdf, pages):
    from _typeset_papal import validate_document, pdf_body_fidelity
    document = validate_document(copy.deepcopy(source), root=ROOT)
    return pdf_body_fidelity(pdf, document, pages)


def _review_rows(paths):
    records, inputs = {}, []
    for path in paths:
        path = Path(path).resolve()
        data, digest = collection._json(path)
        _require(data.get("schema") == collection.REVIEW_SCHEMA and isinstance(data.get("documents"), list), "incorrect visual-review manifest")
        inputs.append({"path": _relative(path), "sha256": digest})
        for index, row in enumerate(data["documents"]):
            key = (*collection._identity(row), row.get("pdf_sha256"))
            _require(collection._digest(key[2]), "review row requires an exact PDF hash")
            records.setdefault(key, []).append((path, data, index, row))
    return records, inputs


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


def _prepare_data(plan_path, pair_path, review_paths):
    plan_path, pair_path = Path(plan_path).resolve(), Path(pair_path).resolve()
    plan, plan_sha = _fresh_plan(plan_path)
    pairs, pairs_sha = collection._json(pair_path)
    _require(pairs.get("schema") == PAIRS_SCHEMA and isinstance(pairs.get("batches"), list), "incorrect batch-pair inventory")
    archives = {}
    plan_ref = _archive(plan_path, "source-plan", archives, plan_sha)
    for item in plan["selection_plan"]["inputs"]:
        _archive(_safe(item["path"]), "source-input", archives, item["sha256"])
    reviews, review_inputs = _review_rows(review_paths)
    review_hashes = {item["path"]: item["sha256"] for item in review_inputs}
    matches, names = {}, set()
    for spec in pairs["batches"]:
        _require(isinstance(spec, dict) and collection._nonempty(spec.get("name"))
                 and all(isinstance(spec.get(field), str) and collection._digest(spec.get(field + "_sha256"))
                         for field in ("receipt", "manifest")), "batch pair requires a name and exact receipt/manifest path/hash pins")
        _require(spec.get("name") not in names, "duplicate render batch name")
        names.add(spec.get("name"))
        resolved = dict(spec, receipt=_safe(spec["receipt"]), manifest=_safe(spec["manifest"]))
        for field in ("receipt", "manifest"):
            _require(collection._sha(resolved[field]) == spec[field + "_sha256"], "batch inventory input SHA-256 mismatch")
        rows, _ = collection._batch(resolved, ROOT / ".scratch/papal-install")
        manifest, _, sources = collection._manifest(resolved["manifest"])
        receipt, _ = collection._json(resolved["receipt"])
        indices = {collection._identity(item): index for index, item in enumerate(receipt["documents"])}
        source_indices = {collection._identity(item): index for index, item in enumerate(manifest["documents"])}
        for row in rows:
            key = collection._identity(row)
            matches.setdefault(key, []).append((row, _normalized(sources[key], manifest), resolved,
                                               source_indices[key], indices[key]))
    documents, states, destinations = [], [], set()
    for source in plan["documents"]:
        key = collection._identity(source)
        normalized = _normalized(source, plan)
        exact = [item for item in matches.get(key, []) if _canonical(item[1]) == _canonical(normalized)]
        successful = [item for item in exact if item[0]["status"] == "compiled"]
        _require(len(successful) <= 1, "ambiguous successful receipts for a current source selection")
        state = {"id": key[0], "language": key[1], "corpus": source.get("collection_corpus", "papal-documents"),
                 "selection_sha256": hashlib.sha256(_canonical(normalized).encode()).hexdigest()}
        if not successful:
            state["status"] = "failed" if any(item[0]["status"] == "failed" for item in exact) else "missing"
            states.append(state)
            continue
        row, _, spec, source_index, receipt_index = successful[0]
        evidence = reviews.get((*key, row["pdf_sha256"]), [])
        _require(len(evidence) <= 1, "duplicate or conflicting current PDF review records")
        if not evidence or evidence[0][3].get("status") != "PASS":
            status = evidence[0][3].get("status") if evidence else None
            _require(status in {None, "PENDING", "CHANGES_REQUIRED"}, "unknown current review state")
            state["status"] = "changes-required" if status == "CHANGES_REQUIRED" else "review-pending"
            states.append(state)
            continue
        audit_path, audit, review_index, review = evidence[0]
        _validate_pass(row, audit, review)
        pdf = (ROOT / ".scratch/papal-install" / unquote(row["files"]["pdf"])).resolve()
        fidelity = _source_check(normalized, pdf, row["pages"])
        _require(fidelity.get("status") == "pass", "PDF source fidelity check did not pass")
        destination = _filename(normalized)
        _require(destination not in destinations, "installed PDF filename collision")
        destinations.add(destination)
        reports = {}
        report_pins = [(review["report"], review["report_sha256"]),
                       *((proof["prior_report"], proof["prior_report_sha256"]) for proof in review.get("reuse_proofs", []))]
        for value, digest in report_pins:
            reports[value] = _archive(collection._report(value), "report", archives, digest)
        documents.append({"id": key[0], "language": key[1], "corpus": state["corpus"],
                          "source": normalized, "render_revision": normalized["revision"],
                          "pdf": destination, "pdf_source": _relative(pdf), "pdf_sha256": row["pdf_sha256"],
                          "bytes": pdf.stat().st_size, "pages": row["pages"], "text_fidelity": fidelity,
                          "manifest": dict(_archive(spec["manifest"], "frozen-manifest", archives, spec["manifest_sha256"]), row_index=source_index),
                          "receipt": dict(_archive(spec["receipt"], "receipt", archives, spec["receipt_sha256"]), row_index=receipt_index),
                          "review": {"audit": dict(_archive(audit_path, "visual-review", archives, review_hashes[_relative(audit_path)]), row_index=review_index),
                                     "reports": reports, "status": "PASS", "original_receipt_sha256": review.get("receipt_sha256", audit["frozen_receipt_sha256"]),
                                     "current_receipt_sha256": row["receipt_sha256"]}})
        states.append(dict(state, status="ready"))
    summary = {"current": len(states), "ready": len(documents), "pages": sum(row["pages"] for row in documents),
               "bytes": sum(row["bytes"] for row in documents)}
    for status in ("review-pending", "changes-required", "failed", "missing"):
        summary[status.replace("-", "_")] = sum(row["status"] == status for row in states)
    return {"schema": PREPARED_SCHEMA, "generator": "typeset-papal prepare-install", "generator_version": 1,
            "plan": {"path": _relative(plan_path), "sha256": plan_sha, "archive": plan_ref},
            "batch_pairs": {"path": _relative(pair_path), "sha256": pairs_sha}, "review_inputs": review_inputs,
            "documents": documents, "delivery_states": states, "archives": sorted(archives.values(), key=lambda row: row["path"]),
            "summary": summary}


def _atomic(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    scratch = ROOT / ".scratch/papal-install"
    scratch.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=scratch, prefix=".papal-install-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
        temporary.chmod(0o644)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def _transaction(operations, verify=None):
    """Stage every payload and old byte sequence before changing owned paths."""
    scratch = ROOT / ".scratch/papal-install"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as directory:
        staging = Path(directory)
        staged, backups = {}, {}
        for number, (path, payload) in enumerate(operations):
            _require(path not in backups, "duplicate installation transaction path")
            if path.exists():
                backup = staging / (str(number) + ".before")
                backup.write_bytes(path.read_bytes())
                backups[path] = backup
            else:
                backups[path] = None
            if payload is not None:
                target = staging / (str(number) + ".after")
                target.write_bytes(payload)
                staged[path] = target
        attempted = []
        try:
            for path, payload in operations:
                backup = backups[path]
                _require(not path.is_symlink(), "installation destination became a symlink")
                _require((not path.exists()) if backup is None else
                         (path.is_file() and collection._sha(path) == collection._sha(backup)),
                         "installation destination changed after preflight; preserved")
                attempted.append(path)
                if payload is None:
                    path.unlink()
                else:
                    _atomic(path, staged[path].read_bytes())
            if verify is not None:
                verify()
        except BaseException:
            for path in reversed(attempted):
                backup = backups[path]
                if backup is None:
                    path.unlink(missing_ok=True)
                else:
                    backup.replace(path)
            raise


def prepare_install(plan, batch_pairs, out, review_manifests=()):
    supplied_out = Path(out).absolute()
    _require(supplied_out.is_relative_to(ROOT), "prepared installation escapes the repository")
    out = _safe(supplied_out.relative_to(ROOT).as_posix())
    _require(out.is_relative_to(ROOT / ".scratch"), "prepared installation must be under repository .scratch")
    reviews = sorted(map(Path, review_manifests)) if review_manifests else sorted((ROOT / "src/sources/papal-documents").glob("*-visual-review.json"))
    data = _prepare_data(plan, batch_pairs, reviews)
    inputs = {Path(plan).resolve(), Path(batch_pairs).resolve(), *(Path(path).resolve() for path in reviews)}
    inputs.update(_safe(row["source"]) for row in data["archives"])
    _require(out not in inputs and not out.is_symlink(), "prepared installation output collides with an input")
    _atomic(out, _payload(data))
    return data


def _owned_release():
    path = _safe(RELEASE.as_posix())
    if not path.exists():
        return None
    data, _ = collection._json(path)
    _require(data.get("schema") == RELEASE_SCHEMA and data.get("generator") == "typeset-papal install"
             and isinstance(data.get("documents"), list), "existing release is not owned by this installer")
    return data


def _owned_files(release):
    owned = {}
    for row in release["documents"] if release else []:
        path = _safe(row["pdf"])
        _require(path.parent == _safe(PDF_ROOT.as_posix()) and path.suffix == ".pdf", "release owns an unexpected PDF path")
        _require(row["pdf"] not in owned and path.is_file() and collection._sha(path) == row["pdf_sha256"],
                 "existing owned PDF is missing, duplicated, or has unexpected bytes; preserved")
        owned[row["pdf"]] = row
    folder = _safe(PDF_ROOT.as_posix())
    entries = list(folder.iterdir()) if folder.exists() else []
    _require(all(path.is_file() and not path.is_symlink() for path in entries), "installed PDF directory contains a symlink or unowned directory; preserved")
    actual = {path.relative_to(ROOT).as_posix() for path in entries}
    _require(actual == set(owned), "installed PDF directory contains an unowned path; preserved")
    return owned


def install_prepared(prepared):
    path = Path(prepared).resolve()
    proposal, _ = collection._json(path)
    _require(proposal.get("schema") == PREPARED_SCHEMA, "incorrect prepared installation schema")
    # Re-run the real source, receipt, PDF and review gates immediately before copy.
    reviews = {_safe(row["path"]) for row in proposal["review_inputs"]}
    reviews.update((ROOT / "src/sources/papal-documents").glob("*-visual-review.json"))
    current = _prepare_data(_safe(proposal["plan"]["path"]), _safe(proposal["batch_pairs"]["path"]), sorted(reviews))
    _require(_canonical(current) == _canonical(proposal), "prepared installation changed; prepare and review it again")
    old_release = _owned_release()
    owned = _owned_files(old_release)
    targets = {row["pdf"]: row for row in proposal["documents"]}
    for row in proposal["archives"]:
        target = _safe(row["path"])
        _require(not target.exists() or collection._sha(target) == row["sha256"], "existing evidence archive has unexpected bytes; preserved")
    for name in targets:
        _safe(name)
        _require(not _safe(name).exists() or name in owned, "installation would replace an unowned PDF")
    obsolete = [dict({key: row[key] for key in ("id", "language", "pdf", "pdf_sha256")},
                     reason="withdrawn-or-no-longer-ready" if name not in targets else "replaced-by-current-pass")
                for name, row in owned.items() if name not in targets or row["pdf_sha256"] != targets[name]["pdf_sha256"]]
    operations = []
    for row in proposal["archives"]:
        target = _safe(row["path"])
        if not target.exists():
            payload = _safe(row["source"]).read_bytes()
            _require(hashlib.sha256(payload).hexdigest() == row["sha256"] and len(payload) == row["bytes"],
                     "release evidence changed during installation")
            operations.append((target, payload))
    for row in proposal["documents"]:
        target = _safe(row["pdf"])
        if not target.exists() or collection._sha(target) != row["pdf_sha256"]:
            payload = _safe(row["pdf_source"]).read_bytes()
            _require(hashlib.sha256(payload).hexdigest() == row["pdf_sha256"], "candidate PDF changed during installation")
            operations.append((target, payload))
    for row in obsolete:
        if row["pdf"] in targets:
            continue
        target = _safe(row["pdf"])
        _require(collection._sha(target) == row["pdf_sha256"], "obsolete PDF changed during installation; preserved")
        operations.append((target, None))
    documents = [{key: value for key, value in row.items() if key != "pdf_source"} for row in proposal["documents"]]
    release = {"schema": RELEASE_SCHEMA, "generator": "typeset-papal install", "generator_version": 1,
               "source_plan": proposal["plan"]["archive"], "documents": documents,
               "delivery_states": proposal["delivery_states"], "summary": proposal["summary"],
               "evidence": [{key: value for key, value in row.items() if key != "source"} for row in proposal["archives"]],
               "obsolete": obsolete}
    operations.append((_safe(RELEASE.as_posix()), _payload(release)))
    def verify():
        _owned_files(release)
        for ref in release["evidence"]:
            _archived(ref)
    _transaction(operations, verify)
    return release


def _archived(ref):
    _require(collection._digest(ref.get("sha256")) and type(ref.get("bytes")) is int and ref["bytes"] > 0,
             "invalid durable evidence pins")
    path = _safe(ref["path"])
    _require(path.is_relative_to(_safe(ARCHIVE_ROOT.as_posix())) and path.is_file(), "missing durable release evidence")
    _require(collection._sha(path) == ref["sha256"] and path.stat().st_size == ref["bytes"], "durable release evidence hash/size mismatch")
    return path


def check_install(plan):
    current, current_sha = _fresh_plan(plan)
    release = _owned_release()
    _require(release is not None, "no installed papal release")
    owned = _owned_files(release)
    for ref in release["evidence"]:
        _archived(ref)
    frozen_plan, _ = collection._json(_archived(release["source_plan"]))
    for item in frozen_plan["selection_plan"]["inputs"]:
        retained = _safe((ARCHIVE_ROOT / "inputs" / (item["sha256"] + ".json")).as_posix())
        _require(retained.is_file() and collection._sha(retained) == item["sha256"],
                 "retained source plan is missing an exact original input")
    active = {collection._identity(row): _normalized(row, current) for row in current["documents"]}
    frozen = {collection._identity(row): _normalized(row, frozen_plan) for row in frozen_plan["documents"]}
    identities = set()
    for row in owned.values():
        key = collection._identity(row)
        _require(type(row.get("pages")) is int and row["pages"] > 0 and type(row.get("bytes")) is int and row["bytes"] > 0,
                 "installed PDF requires integer page and byte counts")
        _require(key not in identities and row["pdf"] == _filename(row["source"]), "duplicate installed identity or unexpected owned filename")
        identities.add(key)
        _require(key in active and _canonical(active[key]) == _canonical(row["source"]), "installed PDF is no longer a current source selection")
        _require(key in frozen and _canonical(frozen[key]) == _canonical(row["source"]), "installed PDF is absent from its retained source plan")
        manifest, _ = collection._json(_archived(row["manifest"]))
        source = manifest["documents"][row["manifest"]["row_index"]]
        _require(_canonical(_normalized(source, manifest)) == _canonical(row["source"]), "retained frozen manifest selection disagrees")
        receipt, receipt_sha = collection._json(_archived(row["receipt"]))
        item = receipt["documents"][row["receipt"]["row_index"]]
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
        audit, _ = collection._json(_archived(row["review"]["audit"]))
        review = audit["documents"][row["review"]["audit"]["row_index"]]
        _require(row["review"]["current_receipt_sha256"] == receipt_sha
                 and row["review"]["original_receipt_sha256"] == review.get("receipt_sha256", audit["frozen_receipt_sha256"]),
                 "release review receipt provenance disagrees")
        for ref in row["review"]["reports"].values():
            _archived(ref)
        fake = {"id": key[0], "language": key[1], "pdf_sha256": row["pdf_sha256"], "pages": row["pages"],
                "status": "compiled", "receipt_sha256": receipt_sha, "files": {}}
        _validate_pass(fake, audit, review, row["review"]["reports"])
        pdf = _safe(row["pdf"])
        _require(pdf.stat().st_size == row["bytes"], "installed PDF byte count mismatch")
        _source_check(row["source"], pdf, row["pages"])
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
            "release_plan_is_current": current_sha == release["source_plan"]["sha256"], "uninstalled": uninstalled}
