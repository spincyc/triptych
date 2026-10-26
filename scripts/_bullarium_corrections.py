"""Append-only metadata and source-selection corrections for papal editions."""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib

import _bullarium as source
from _tooling import Example, with_examples
from _typeset_papal import LANGUAGES, SCHEMA, validate_document

ROOT = source.ROOT
PLAN_SCHEMA = "triptych-papal-correction-plan/v1"
RECEIPT_SCHEMA = "triptych-papal-typeset-receipt/v1"
CHANGES = {"title", "pope", "date", "language", "language_label", "document_type",
           "source_note", "reader_source_note", "extent_kind", "keep_with_next",
           "terminal_keep_blocks", "compact_layout"}
ID = re.compile(r"[a-z0-9][a-z0-9.-]*")
KEY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
SHA = re.compile(r"[a-f0-9]{64}")
EXAMPLES = (
    Example("tools/bullarium corrections --plan .scratch/bullarium_reconstruction/correction_engine/absent.json --out .scratch/bullarium_reconstruction/correction_engine/preflight.json --revision invalid --json",
            ('{"code":"input","error":"revision requires explicit whole-second UTC","status":"error","v":1}',),
            "An invalid revision is refused before reading inputs or writing records."),
    Example("tools/bullarium corrections --plan .scratch/bullarium_reconstruction/correction_engine/absent.json --out .scratch/bullarium_reconstruction/correction_engine/preflight.json --revision invalid",
            ("bullarium corrections: revision requires explicit whole-second UTC",),
            "The same safe preflight refusal in ordinary text."),
)


class CorrectionError(ValueError):
    """A correction cannot preserve the frozen source and publication evidence."""


def _require(condition, message):
    if not condition:
        raise CorrectionError(message)


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _revision(value):
    try:
        _require(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value),
                 "revision requires explicit whole-second UTC")
        dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise CorrectionError("revision requires explicit whole-second UTC") from error


def _path(root, value, *, relative=False):
    _require(isinstance(value, (str, Path)) and bool(str(value)), "path must be nonempty")
    raw = str(value)
    _require(not any(ord(char) < 32 for char in raw) and "\\" not in raw,
             "path must not contain control characters or backslashes")
    path = Path(value)
    _require(".." not in path.parts and not (relative and path.is_absolute()),
             "path must be repository-relative without traversal")
    resolved = (root / path).resolve()
    _require(resolved.is_relative_to(root), "path escapes the repository")
    return resolved


def _json_payload(payload):
    def pairs(items):
        result = {}
        for key, value in items:
            _require(key not in result, "duplicate JSON key: " + key)
            result[key] = value
        return result

    def constant(value):
        raise CorrectionError("non-finite JSON value: " + value)

    result = json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)
    _require(isinstance(result, dict), "JSON input requires an object")
    return result


def _json(path):
    return _json_payload(path.read_bytes())


def _toml(path, kind):
    record = tomllib.loads(path.read_text(encoding="utf-8"))
    _require(record.get("record_type") == kind, "source record has the wrong record_type")
    _require(record.get("schema") == (2 if kind == "segment" else 1),
             "source record has an unsupported schema")
    _require(_text(record.get("id")), "source record requires an id")
    return record


def _hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _identity(row):
    _require(isinstance(row, dict) and isinstance(row.get("id"), str)
             and ID.fullmatch(row["id"]), "document requires a valid id")
    _require(isinstance(row.get("language"), str) and row["language"] in LANGUAGES,
             "document requires a supported language")
    return row["id"], row["language"]


def _repo_paths(plan, name, root):
    values = plan.get(name)
    _require(isinstance(values, list) and values and all(_text(value) for value in values),
             name + " requires nonempty repository-relative paths")
    paths = [_path(root, value, relative=True) for value in values]
    _require(len(paths) == len(set(paths)), name + " contains duplicate paths")
    return paths


def _initial_documents(paths, frozen, overrides=None):
    documents, revisions = {}, {}
    overrides = {} if overrides is None else overrides
    for path in paths:
        manifest = overrides[path] if path in overrides else _json(path)
        _require(manifest.get("schema") == SCHEMA, "initial manifest has an unknown schema")
        _revision(manifest.get("revision"))
        rows = manifest.get("documents")
        _require(isinstance(rows, list), "initial manifest requires documents[]")
        seen = set()
        for row in rows:
            key = _identity(row)
            effective_revision = row.get("revision", manifest["revision"])
            _revision(effective_revision)
            _require(key not in seen, "duplicate identity in initial manifest")
            seen.add(key)
            # A cumulative inventory makes the formerly implicit row revision
            # explicit when its header advances. That representation change is
            # not a change to this frozen document's source or metadata.
            content = {name: value for name, value in row.items() if name != "revision"}
            _require(key not in documents or
                     {name: value for name, value in documents[key].items() if name != "revision"} == content,
                     "initial manifests disagree on a prior document")
            documents[key] = row
            revisions.setdefault(key, set()).add(effective_revision)
        if path not in overrides:
            frozen[path] = _hash(path)
    return documents, revisions


def _prior_pdfs(paths, documents, revisions, root, frozen):
    observed = {}
    for path in paths:
        receipt = _json(path)
        _require(receipt.get("schema") == RECEIPT_SCHEMA, "prior receipt has an unknown schema")
        _revision(receipt.get("revision"))
        _require(isinstance(receipt.get("documents"), list), "prior receipt requires documents[]")
        seen = set()
        for row in receipt["documents"]:
            key = _identity(row)
            _require(key not in seen, "duplicate identity in prior receipt")
            seen.add(key)
            _require(row.get("status") in {"compiled", "rendered", "failed"},
                     "prior receipt has an unknown result status")
            if row["status"] != "compiled":
                continue
            old = documents.get(key)
            _require(old is not None, "successful prior is absent from initial manifests")
            # Current receipts state the row's render revision independently of
            # the cumulative inventory header. Legacy receipts predate that
            # field, so only their own header can attest their render revision.
            effective_revision = row.get("render_revision", receipt["revision"])
            _revision(effective_revision)
            _require(effective_revision in revisions[key],
                     "prior receipt and initial document render revision disagree")
            for receipt_key, document_key in (("artifact_id", "artifact_id"), ("source_sha256", "sha256"),
                                               ("segment_id", "segment_id"),
                                               ("physical_line_ranges", "physical_line_ranges")):
                _require(row.get(receipt_key) == old.get(document_key),
                         "prior receipt disagrees with frozen source on " + receipt_key)
            declared = row.get("pdf_sha256")
            _require(isinstance(declared, str) and SHA.fullmatch(declared),
                     "successful prior requires an exact PDF SHA-256")
            pdf = _path(path.parent, row.get("pdf"), relative=True)
            _require(pdf.is_relative_to(root) and pdf.suffix.lower() == ".pdf" and pdf.is_file(),
                     "successful prior PDF is absent or has an invalid path")
            actual = _hash(pdf)
            _require(actual == declared, "prior PDF SHA-256 mismatch for " + row["id"])
            frozen[pdf] = actual
            observed.setdefault(key, set()).add(actual)
        frozen[path] = _hash(path)
    return observed


def _selection(root, document, frozen):
    payload = _path(root, document["text_path"], relative=True)
    paths = [payload, payload.parent / "artifact.toml"]
    segment = None
    if document.get("segment_id"):
        segment_path = _path(root, document["segment_path"], relative=True)
        _require(segment_path.parent.name == "segments" and segment_path.suffix == ".toml",
                 "segment must occupy its source-owned segments directory")
        segment = _toml(segment_path, "segment")
        edition_dir = segment_path.parents[1]
        paths.append(segment_path)
    else:
        edition_dir = payload.parents[2]
    works = root / "src/sources/works"
    _require(payload.is_relative_to(works) and edition_dir.is_relative_to(works),
             "source records must remain under src/sources/works")
    relative = edition_dir.relative_to(works).parts
    _require(len(relative) == 4 and relative[2] == "editions",
             "selected edition has no canonical work owner")
    edition_path, work_path = edition_dir / "edition.toml", edition_dir.parents[1] / "work.toml"
    edition, work = _toml(edition_path, "edition"), _toml(work_path, "work")
    _require(edition.get("work_id") == work["id"], "selected edition disagrees with its work owner")
    paths.extend([edition_path, work_path])
    for path in paths:
        frozen[path] = _hash(path)
    return edition_dir, edition, segment


def _record_bytes(record):
    return ("\n".join(f"{key} = {source.toml_value(value)}" for key, value in record.items()) + "\n").encode()


def _queue(records, path, record):
    data = _record_bytes(record)
    _require(path not in records or records[path][1] == data, "new source records conflict on a path")
    records[path] = record, data


def _new_selection(root, old, row, frozen, records):
    edition_dir, edition, old_segment = _selection(root, old, frozen)
    spec, expression = row.get("new_segment"), row.get("new_edition")
    if spec is None and expression is None:
        return {}
    if expression is not None:
        _require(isinstance(expression, dict) and set(expression) == {"key", "language", "notes"},
                 "new_edition requires exactly key, language and notes")
        key = expression["key"]
        _require(isinstance(key, str) and KEY.fullmatch(key) and re.match(r"[0-9]{4}-", key)
                 and 1 <= int(key[:4]) <= 9999 and key != edition_dir.name,
                 "new_edition requires a distinct dated key")
        printing_date = edition.get("date")
        printing_year = re.match(r"([0-9]{4})(?:$|[^0-9])", printing_date) if isinstance(printing_date, str) else None
        _require(printing_year is not None and key[:4] == printing_year[1],
                 "new_edition key year must match the existing historical printing date")
        _require(isinstance(expression["language"], str) and expression["language"] in LANGUAGES
                 and _text(expression["notes"]),
                 "new_edition requires truthful language and nonempty notes")
        title = edition["title"].removesuffix(" — " + edition_dir.name) + " — " + key
        edition_dir = edition_dir.parent / key
        edition = {**edition, "id": "edition." + edition["work_id"].removeprefix("work.") + "." + key,
                   "title": title, "language": expression["language"], "notes": expression["notes"]}
        _queue(records, edition_dir / "edition.toml", edition)
    if spec is not None:
        _require(isinstance(spec, dict) and set(spec) <= {"key", "physical_line_ranges", "context", "notes"}
                 and {"key", "context", "notes"} <= set(spec),
                 "new_segment requires key, context, notes and optional physical_line_ranges")
        _require(all(_text(spec[name]) for name in ("key", "context", "notes")),
                 "new_segment metadata must be nonempty")
        if "physical_line_ranges" in spec:
            _require(isinstance(spec["physical_line_ranges"], list) and spec["physical_line_ranges"],
                     "explicit new_segment physical_line_ranges must be nonempty")
        key = spec["key"]
        _require(KEY.fullmatch(key), "new_segment key must be lowercase kebab-case")
    else:
        spec = {}
        key = Path(old.get("segment_path", "source-ocr.toml")).stem
    ranges = copy.deepcopy(spec.get("physical_line_ranges", old.get("physical_line_ranges")))
    if ranges is None:
        ranges = [[1, len(source.lines((root / old["text_path"]).read_bytes()))]]
    segment = copy.deepcopy(old_segment) if old_segment else {
        "schema": 2, "record_type": "segment", "segment_type": "constituent-work",
        "states": ["cataloged", "acquired"], "context": "Exact source selection retained by a correction plan."}
    if ranges != old.get("physical_line_ranges"):
        segment.pop("artifact_page_ranges", None)
        segment.pop("verified_on", None)
        segment["states"] = ["cataloged", "acquired"]
    segment.update({"id": "segment." + edition["id"].removeprefix("edition.") + "." + key,
                    "edition_id": edition["id"], "artifact_id": old["artifact_id"],
                    "artifact_sha256": old["sha256"], "physical_line_ranges": ranges})
    segment.update({name: spec[name] for name in ("context", "notes") if name in spec})
    path = edition_dir / "segments" / (key + ".toml")
    _queue(records, path, segment)
    return {"segment_id": segment["id"], "segment_path": path.relative_to(root).as_posix(),
            "physical_line_ranges": ranges, "language": edition["language"]}


def _absent_or_identical(path, data):
    _require(not path.exists() or (path.is_file() and path.read_bytes() == data),
             "refusing to replace existing bytes: " + path.name)


def _frozen_unchanged(frozen):
    _require(all(path.is_file() and _hash(path) == digest for path, digest in frozen.items()),
             "frozen source, plan, manifest, receipt or PDF changed during correction")


def _append_file(root, path, data, writer):
    """Use the common serializers; publish a complete new file without clobbering."""
    _absent_or_identical(path, data)
    if path.exists():
        return False
    scratch = root / ".scratch/bullarium_reconstruction/correction_engine/staging"
    _require(scratch.resolve().is_relative_to(root), "correction staging path escapes the repository")
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch) as directory:
        staged = Path(directory) / "record"
        writer(staged)
        _require(staged.read_bytes() == data, "source writer produced unexpected bytes")
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.link(staged, path)
        except FileExistsError:
            _absent_or_identical(path, data)
            return False
    return True


def _git_history_bytes(root, commit, path):
    """Read an exact committed input without changing refs or the worktree."""
    _require(isinstance(commit, str) and re.fullmatch(r"[a-f0-9]{40}", commit),
             "append Git input requires a full commit object ID")
    _path(root, path, relative=True)

    def git(*args):
        result = subprocess.run(["git", "--no-replace-objects", "-C", str(root), *args], capture_output=True, check=False)
        _require(result.returncode == 0, "append Git input commit/path is unavailable")
        return result.stdout

    _require(Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve() == root,
             "append Git input must belong to the exact source repository")
    _require(git("cat-file", "-t", commit).strip() == b"commit", "append Git input object is not a commit")
    return git("show", commit + ":" + path)


def _cumulative_base(root, plan, out_path, revision, frozen):
    if "append" not in plan:
        return None
    spec = plan["append"]
    _require(isinstance(spec, dict) and set(spec) in (
        {"base_sha256", "base_revision", "archive_path"},
        {"base_sha256", "base_revision", "git_commit", "git_path"}),
        "append requires base_sha256, base_revision and archive_path or git_commit/git_path")
    _require(isinstance(spec["base_sha256"], str) and SHA.fullmatch(spec["base_sha256"]),
             "append requires an exact base SHA256")
    _revision(spec["base_revision"])
    _require(revision > spec["base_revision"], "append revision must advance the frozen base revision")
    _require(out_path.is_file(), "append requires the existing correction inventory")
    current = out_path.read_bytes()
    archive = None
    if "git_commit" in spec:
        _require(spec["git_path"] == out_path.relative_to(root).as_posix(),
                 "append Git path must identify the same existing inventory")
        payload = _git_history_bytes(root, spec["git_commit"], spec["git_path"])
        storage = {"storage": "git", "git_commit": spec["git_commit"], "git_path": spec["git_path"]}
    else:
        archive = _path(root, spec["archive_path"], relative=True)
        _require(archive != out_path and archive.suffix == ".json"
                 and not archive.is_relative_to(root / "src/sources/works"),
                 "append archive must be separate JSON outside source record owners")
        payload = archive.read_bytes() if archive.exists() else current
        if archive.exists():
            frozen[archive] = _hash(archive)
        storage = {"storage": "archive", "archive_key": "sha256:" + spec["base_sha256"]}
    _require(hashlib.sha256(payload).hexdigest() == spec["base_sha256"], "append frozen base SHA256 mismatch")
    base = _json_payload(payload)
    _require(base.get("schema") == SCHEMA and base.get("revision") == spec["base_revision"],
             "append frozen base schema/revision mismatch")
    _require(set(base) <= {"schema", "revision", "documents", "supersessions", "input_history"}
             and isinstance(base.get("documents"), list) and base["documents"]
             and isinstance(base.get("supersessions"), list),
             "append base must be an ordinary correction inventory with documents/supersessions")
    identities = set()
    for document in base["documents"]:
        key = _identity(document)
        _require(key not in identities, "append base has duplicate document identities")
        identities.add(key)
        when = document.get("revision", base["revision"])
        _revision(when)
        _require(when <= base["revision"], "append base row revision exceeds its inventory revision")
    rows = {_identity(document): document for document in base["documents"]}
    prior_pins = set()
    for item in base["supersessions"]:
        _require(isinstance(item, dict) and set(item) == {"prior", "replacement", "reason"}
                 and _text(item["reason"]) and isinstance(item["prior"], dict)
                 and isinstance(item["replacement"], dict), "append base has a malformed correction supersession")
        prior, replacement = item["prior"], item["replacement"]
        key, replacement_key = _identity(prior), _identity(replacement)
        _require(isinstance(prior.get("pdf_sha256"), str) and SHA.fullmatch(prior["pdf_sha256"]),
                 "append base supersession lacks its exact prior PDF pin")
        _require((key, prior["pdf_sha256"]) not in prior_pins, "append base has duplicate prior PDF pins")
        prior_pins.add((key, prior["pdf_sha256"]))
        target = rows.get(replacement_key)
        _require(target is not None, "append base replacement is absent from its document inventory")
        for pin, field in (("artifact_id", "artifact_id"), ("source_sha256", "sha256"), ("segment_id", "segment_id")):
            _require(replacement.get(pin) == target.get(field), "append base replacement source pin disagrees")
    _require(isinstance(base.get("input_history", []), list), "append base input_history must be an array")
    return {"base": base, "bytes": payload, "archive": archive, "storage": storage,
            "observed_output_sha256": hashlib.sha256(current).hexdigest(), "spec": spec}


def _cumulative_result(state, documents, supersessions, revision):
    if state is None:
        return {"schema": SCHEMA, "revision": revision, "documents": documents, "supersessions": supersessions}
    base = state["base"]
    old_ids = {document["id"] for document in base["documents"]}
    _require(not old_ids.intersection(document["id"] for document in documents),
             "append replacements must have distinct IDs from frozen inventory rows")
    retired = {_identity(row["prior"]) for row in base["supersessions"]}
    _require(not retired.intersection(_identity(row["prior"]) for row in supersessions),
             "append must correct the current document identity, not an already superseded alias")
    retained = copy.deepcopy(base["documents"])
    for document in retained:
        document.setdefault("revision", base["revision"])
    history = copy.deepcopy(base.get("input_history", []))
    history.append({"revision": base["revision"], "sha256": state["spec"]["base_sha256"],
                    "document_count": len(base["documents"]), "supersession_count": len(base["supersessions"]),
                    **state["storage"]})
    return {"schema": SCHEMA, "revision": revision, "documents": retained + documents,
            "supersessions": copy.deepcopy(base["supersessions"]) + supersessions, "input_history": history}


def _install_cumulative(root, out_path, output, state):
    """Replace only the exact state checked under the cooperating-builder lock."""
    if out_path.read_bytes() == output:
        return
    scratch = root / ".scratch/bullarium_reconstruction/correction_engine/staging"
    with tempfile.NamedTemporaryFile(dir=scratch, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(output)
    try:
        _require(out_path.is_file() and _hash(out_path) == state["observed_output_sha256"],
                 "correction inventory changed before cumulative replacement")
        os.replace(temporary, out_path)
    finally:
        temporary.unlink(missing_ok=True)


def _build_corrections(root, plan_path, out_path, revision):
    """Return/write a new manifest; preserve old records, source bytes and PDFs.

    Inner plan paths are repository-relative. A new edition automatically creates
    a v2 segment with the prior bounds, unless new_segment supplies reviewed bounds.
    Its dated key retains the historical edition's printing year.
    Initial rows may pin their original revision beneath a newer manifest header;
    receipt render revisions must match those rows (legacy receipts use headers).
    Replacement rows explicitly pin this correction's requested revision.
    New records and the output may be absent or exactly identical to a prior replay.
    """
    _revision(revision)
    root = Path(root).resolve()
    plan_path, out_path = _path(root, plan_path), _path(root, out_path)
    _require(out_path.suffix == ".json" and not out_path.is_relative_to(root / "src/sources/works"),
             "correction manifest must be JSON outside source record owners")
    plan = _json(plan_path)
    _require(plan.get("schema") == PLAN_SCHEMA, "unknown correction plan schema")
    _require({"schema", "initial_manifests", "prior_receipts", "corrections"} <= set(plan)
             and set(plan) <= {"schema", "initial_manifests", "prior_receipts", "corrections", "append"},
             "correction plan has missing or unsupported fields")
    _require(isinstance(plan["corrections"], list) and plan["corrections"], "corrections[] must be nonempty")
    frozen = {plan_path: _hash(plan_path)}
    cumulative = _cumulative_base(root, plan, out_path, revision, frozen)
    initial_paths = _repo_paths(plan, "initial_manifests", root)
    _require(cumulative is None or out_path in initial_paths,
             "append inventory must be explicitly listed in initial_manifests")
    overrides = {out_path: cumulative["base"]} if cumulative is not None else {}
    initial, revisions = _initial_documents(initial_paths, frozen, overrides)
    observed = _prior_pdfs(_repo_paths(plan, "prior_receipts", root), initial, revisions, root, frozen)
    documents, supersessions, records, seen = [], [], {}, set()
    old_ids = {key[0] for key in initial}
    for row in plan["corrections"]:
        _require(isinstance(row, dict) and set(row) <= {"prior_id", "replacement_id", "reason", "changes", "new_segment", "new_edition"}
                 and {"prior_id", "replacement_id", "reason", "changes"} <= set(row),
                 "correction requires prior_id, replacement_id, reason, changes and optional new source records")
        prior_id, replacement_id = row["prior_id"], row["replacement_id"]
        _require(isinstance(prior_id, str) and prior_id not in seen, "duplicate or invalid prior_id")
        matches = [key for key in initial if key[0] == prior_id]
        _require(len(matches) == 1, "prior_id is absent or ambiguous in initial manifests")
        prior = matches[0]
        _require(observed.get(prior), "correction lacks a successful prior PDF")
        _require(isinstance(replacement_id, str) and ID.fullmatch(replacement_id)
                 and replacement_id not in old_ids and all(d["id"] != replacement_id for d in documents),
                 "replacement_id must be distinct from all prior and replacement IDs")
        _require(_text(row["reason"]), "correction requires a nonempty reason")
        changes = row["changes"]
        _require(isinstance(changes, dict) and set(changes) <= CHANGES,
                 "changes may override only project metadata and layout, never body, source, hashes or rights")
        for name in {"document_type", "reader_source_note", "extent_kind"} & set(changes):
            _require(_text(changes[name]), name + " must be nonempty text")
        if "date" in changes:
            _require(changes["date"] is None or _text(changes["date"]),
                     "date must be an ISO calendar date or null")
        if "language" in changes:
            _require(isinstance(changes["language"], str) and changes["language"] in LANGUAGES,
                     "language must be a supported code")
        old = initial[prior]
        validate_document(old, root)
        document = copy.deepcopy(old)
        document.update(copy.deepcopy(changes))
        if changes.get("language_label", "present") is None:
            document.pop("language_label", None)
        document["id"] = replacement_id
        document["revision"] = revision
        selection = _new_selection(root, old, row, frozen, records)
        if "language" in changes and selection:
            _require(changes["language"] == selection["language"], "language correction disagrees with new source edition")
        document.update(selection)
        if "reader_source_note" in document:
            _require(_text(document["reader_source_note"]), "reader_source_note must be nonempty text")
        documents.append(document)
        for digest in sorted(observed[prior]):
            previous = {"id": old["id"], "language": old["language"], "pdf_sha256": digest,
                        "artifact_id": old["artifact_id"], "source_sha256": old["sha256"]}
            replacement = {"id": document["id"], "language": document["language"],
                           "artifact_id": document["artifact_id"], "source_sha256": document["sha256"]}
            if old.get("segment_id"):
                previous["segment_id"] = old["segment_id"]
            if document.get("segment_id"):
                replacement["segment_id"] = document["segment_id"]
            supersessions.append({"prior": previous, "replacement": replacement, "reason": row["reason"]})
        seen.add(prior_id)
    result = _cumulative_result(cumulative, documents, supersessions, revision)
    output = source.json_bytes(result)
    _require(out_path not in frozen and not (set(records) & set(frozen)), "new output would edit a frozen input")
    for path, (_, data) in records.items():
        _path(root, path)
        _require(path.resolve() == path, "new source paths cannot pass through symlinks")
        _absent_or_identical(path, data)
    if cumulative is None:
        _absent_or_identical(out_path, output)
    else:
        _require(cumulative["observed_output_sha256"] in {
            cumulative["spec"]["base_sha256"], hashlib.sha256(output).hexdigest()},
            "existing inventory is neither the frozen base nor the exact cumulative replay")
    _frozen_unchanged(frozen)
    created = []
    try:
        for path, (record, data) in records.items():
            _require(path.resolve() == path, "new source paths cannot pass through symlinks")
            if _append_file(root, path, data, lambda staged: source.record(staged, record)):
                created.append((path, data))
        for document in result["documents"]:
            validate_document(document, root)
        _frozen_unchanged(frozen)
        if cumulative is None:
            _append_file(root, out_path, output, lambda staged: source.write(staged, output))
        else:
            if "git_commit" in cumulative["spec"]:
                _require(_git_history_bytes(root, cumulative["spec"]["git_commit"], cumulative["spec"]["git_path"])
                         == cumulative["bytes"], "committed correction input changed during validation")
            else:
                _append_file(root, cumulative["archive"], cumulative["bytes"],
                             lambda staged: source.write(staged, cumulative["bytes"]))
                frozen[cumulative["archive"]] = cumulative["spec"]["base_sha256"]
            _frozen_unchanged(frozen)
            _install_cumulative(root, out_path, output, cumulative)
    except Exception:
        for path, data in reversed(created):
            if path.is_file() and path.read_bytes() == data:
                path.unlink()
                parent = path.parent
                while parent != root:
                    try:
                        parent.rmdir()
                    except OSError:
                        break
                    parent = parent.parent
        raise
    return result


def build_corrections(root, plan_path, out_path, revision):
    """Create or explicitly append a PDF-pinned correction inventory.

    Optional plan append:{} pins the exact old inventory and immutable archive
    or Git input. Retained rows keep their effective render revisions. An
    advisory directory lock serializes cooperating correction builders; the
    existing inventory is compared again immediately before atomic replacement.
    """
    _revision(revision)
    root = Path(root).resolve()
    scratch = root / ".scratch/bullarium_reconstruction/correction_engine/staging"
    _require(scratch.resolve().is_relative_to(root), "correction staging path escapes the repository")
    scratch.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(scratch, os.O_RDONLY)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        return _build_corrections(root, plan_path, out_path, revision)
    finally:
        fcntl.flock(descriptor, fcntl.LOCK_UN)
        os.close(descriptor)


def build_withdrawals(root, plan_path, out_path, revision):
    """Write cumulative, PDF-pinned withdrawal metadata without editing sources.

    The existing correction-plan envelope uses withdrawals[] instead of
    corrections[]. Each row identifies a reviewed unit, a prior document and
    explicit confirmed-fusion evidence. No replacement body is generated.
    """
    _revision(revision)
    root = Path(root).resolve()
    plan_path, out_path = _path(root, plan_path), _path(root, out_path)
    _require(out_path.suffix == ".json" and not out_path.is_relative_to(root / "src/sources/works"),
             "withdrawal inventory must be JSON outside source record owners")
    plan = _json(plan_path)
    _require(plan.get("schema") == PLAN_SCHEMA and
             set(plan) == {"schema", "initial_manifests", "prior_receipts", "withdrawals"},
             "withdrawal plan requires the correction-plan envelope and withdrawals[]")
    _require(isinstance(plan["withdrawals"], list) and plan["withdrawals"], "withdrawals[] must be nonempty")
    frozen = {plan_path: _hash(plan_path)}
    initial, revisions = _initial_documents(_repo_paths(plan, "initial_manifests", root), frozen)
    observed = _prior_pdfs(_repo_paths(plan, "prior_receipts", root), initial, revisions, root, frozen)
    previous = _json(out_path) if out_path.exists() else {"documents": [], "supersessions": [], "affected_units": []}
    previous_hash = _hash(out_path) if out_path.exists() else None
    if previous_hash is not None:
        _require(previous.get("schema") == SCHEMA, "existing withdrawal inventory has an unknown schema")
        _revision(previous.get("revision"))
    _require(not previous.get("documents") and isinstance(previous.get("supersessions"), list)
             and isinstance(previous.get("affected_units"), list), "withdrawal inventory cannot contain replacement bodies")
    supersessions = {}
    current_withdrawal_ids={row.get("current_document_id") for row in previous["affected_units"]}
    for row in previous["supersessions"]:
        _require(row.get("replacement", "absent") is None, "withdrawal inventory contains a non-withdrawal")
        prior = row.get("prior", {})
        key = _identity(prior)
        _require(key[0] in current_withdrawal_ids, "existing null row names a retired alias rather than its current corrected identity")
        old = initial.get(key)
        _require(old is not None and prior.get("pdf_sha256") in observed.get(key, set()),
                 "existing withdrawal lacks an actual provided prior PDF")
        for a, z in (("artifact_id", "artifact_id"), ("source_sha256", "sha256"), ("segment_id", "segment_id")):
            _require(prior.get(a) == old.get(z), "existing withdrawal source pin changed")
        supersessions[(key, prior["pdf_sha256"])] = row
    affected = {row["unit_id"]: row for row in previous["affected_units"]}
    seen = set()

    def clean(value):
        if isinstance(value, dict):
            return {key: clean(item) for key, item in value.items()
                    if not (isinstance(item, str) and (item.startswith((".scratch/", "/home/", "/tmp/")) or "file://" in item))}
        if isinstance(value, list):
            return [clean(item) for item in value]
        return value

    for row in plan["withdrawals"]:
        _require(isinstance(row, dict) and set(row) == {"unit_id", "prior_id", "reason", "evidence"},
                 "withdrawal requires unit_id, prior_id, reason and evidence")
        _require(all(_text(row[key]) for key in ("unit_id", "prior_id", "reason")), "withdrawal identifiers and reason are required")
        _require(ID.fullmatch(row["unit_id"]), "withdrawal unit_id must be an exact catalog identifier")
        _require(row["prior_id"] not in seen, "duplicate withdrawal prior_id")
        seen.add(row["prior_id"])
        evidence = row["evidence"]
        _require(isinstance(evidence, dict) and evidence.get("classification") == "confirmed-fusion"
                 and evidence.get("unit_id") == row["unit_id"], "withdrawal requires confirmed current source-order evidence")
        matches = [key for key in initial if key[0] == row["prior_id"]]
        anchors = [key for key in initial if key[0] == evidence.get("current_document_id")]
        _require(len(matches) == len(anchors) == 1, "withdrawal prior/current identity is absent or ambiguous")
        prior, anchor = matches[0], initial[anchors[0]]
        old = initial[prior]
        _require(old["id"]==anchor["id"], "active withdrawal must name the current corrected identity; retired aliases remain correction history")
        _require(observed.get(prior), "withdrawal lacks a successful actual prior PDF")
        for name, field in (("artifact_id", "artifact_id"), ("artifact_sha256", "sha256"),
                            ("segment_id", "segment_id"), ("physical_line_ranges", "physical_line_ranges")):
            _require(evidence.get(name) == anchor.get(field), "withdrawal evidence disagrees with current source on " + name)
        chain = {evidence.get("current_document_id"), evidence.get("original_document_id"), *evidence.get("known_correction_ids", [])}
        _require(old["id"] in chain and old["artifact_id"] == anchor["artifact_id"] and old["sha256"] == anchor["sha256"],
                 "withdrawal alias lacks explicit same-controller source evidence")
        ranges = evidence.get("affected_physical_line_ranges")
        _require(isinstance(ranges, list) and ranges and evidence.get("native_word_evidence"),
                 "withdrawal requires affected LF ranges and native WORD evidence")
        for span in ranges:
            _require(isinstance(span, list) and len(span) == 2 and all(type(n) is int for n in span)
                     and 1 <= span[0] <= span[1]
                     and any(a <= span[0] <= span[1] <= z for a, z in old.get("physical_line_ranges", [])),
                     "confirmed fusion lies outside the prior selected source")
        _selection(root, old, frozen)
        validate_document(old, root)
        pins = []
        for digest in sorted(observed[prior]):
            pin = {"id": old["id"], "language": old["language"], "pdf_sha256": digest,
                   "artifact_id": old["artifact_id"], "source_sha256": old["sha256"], "segment_id": old.get("segment_id")}
            supersessions.setdefault((prior, digest), {"prior": pin, "replacement": None, "reason": row["reason"]})
            pins.append(pin)
        record = affected.setdefault(row["unit_id"], {"unit_id": row["unit_id"], "withdrawn_documents": []})
        record.update(current_document_id=anchor["id"], artifact_id=anchor["artifact_id"], source_sha256=anchor["sha256"],
                      segment_id=anchor.get("segment_id"), physical_line_ranges=anchor.get("physical_line_ranges"),
                      active_disposition="source-order-hold", source_order_evidence=clean(evidence))
        indexed = {(p["id"], p["language"], p["pdf_sha256"]): p for p in record["withdrawn_documents"]}
        indexed.update({(p["id"], p["language"], p["pdf_sha256"]): p for p in pins})
        record["withdrawn_documents"] = [indexed[key] for key in sorted(indexed)]
    result = {"schema": SCHEMA, "revision": revision, "documents": [],
              "supersessions": [supersessions[key] for key in sorted(supersessions)],
              "affected_units": [affected[key] for key in sorted(affected)]}
    if previous.get("input_history"):
        result["input_history"]=copy.deepcopy(previous["input_history"])
    if previous_hash is not None and any(previous.get(key)!=result[key] for key in ("revision","supersessions","affected_units")):
        archive=root/".scratch/bullarium_reconstruction/withdrawal-history"/(previous_hash+".json")
        source.write(archive,out_path.read_bytes())
        entry={"revision":previous["revision"],"sha256":previous_hash,"archive_key":"sha256:"+previous_hash,
               "affected_unit_ids":[row["unit_id"] for row in previous["affected_units"]],
               "supersession_count":len(previous["supersessions"])}
        history=result.setdefault("input_history",[])
        if not history or history[-1].get("sha256")!=previous_hash:
            history.append(entry)
    output = source.json_bytes(result)
    _require(out_path not in frozen, "withdrawal output would overwrite a frozen input")
    _frozen_unchanged(frozen)
    _require(not out_path.exists() if previous_hash is None else _hash(out_path) == previous_hash,
             "withdrawal inventory changed during validation")
    scratch = root / ".scratch/bullarium_reconstruction/withdrawal_engine"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=scratch, delete=False) as staged:
        temporary = Path(staged.name)
        staged.write(output)
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        os.replace(temporary, out_path)
    finally:
        temporary.unlink(missing_ok=True)
    return result


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise CorrectionError(message)


def main(argv=None, examples=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = _Parser(prog="bullarium corrections", description=__doc__)
    with_examples(parser, examples.get("corrections", EXAMPLES) if isinstance(examples, dict) else examples or EXAMPLES)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--withdrawals", action="store_true", help="write PDF-pinned withdrawal metadata without replacement bodies")
    try:
        args = parser.parse_args(argv)
        result = (build_withdrawals if args.withdrawals else build_corrections)(args.root, args.plan, args.out, args.revision)
        payload = {"v": 1, "status": "ok", "documents": len(result["documents"]),
                   "supersessions": len(result["supersessions"]),
                   "manifest": _path(args.root.resolve(), args.out).relative_to(args.root.resolve()).as_posix()}
        if args.withdrawals:
            payload["affected_units"]=len(result["affected_units"])
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if args.json
              else (f"withdrawals: {payload['affected_units']} source-order holds; {payload['supersessions']} exact prior PDFs" if args.withdrawals
                    else f"corrections: {payload['documents']} replacement editions; {payload['supersessions']} exact prior PDFs"))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({"v": 1, "status": "error", "code": "input", "error": str(error)},
                         sort_keys=True, separators=(",", ":")) if "--json" in argv
              else f"bullarium corrections: {error}", file=sys.stderr)
        return 2
