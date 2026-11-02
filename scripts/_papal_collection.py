"""A local metadata index over exact, independently owned papal PDF batches."""
from __future__ import annotations

import datetime as dt
import copy
import hashlib
import html
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-papal-collection/v1"
RECEIPT_SCHEMA = "triptych-papal-typeset-receipt/v1"
MANIFEST_SCHEMA = "triptych-papal-typeset/v1"
REVIEW_SCHEMA = "triptych-papal-visual-review/v1"
PLAN_SCHEMA = "triptych-papal-source-plan/v1"
SHA = re.compile(r"[a-f0-9]{64}")
LANGUAGE = re.compile(r"[a-z]{2,3}(?:-[A-Za-z0-9]{2,8})*")
LANGUAGE_NAMES = {"en": "English", "la": "Latin", "it": "Italian", "fr": "French",
                  "de": "German", "es": "Spanish", "pt": "Portuguese", "grc": "Greek",
                  "mul": "Multilingual"}


class PapalCollectionError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise PapalCollectionError(message)


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _digest(value):
    return isinstance(value, str) and SHA.fullmatch(value) is not None


def _sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            _require(key not in result, f"duplicate JSON key in {path.name}: {key}")
            result[key] = value
        return result

    def constant(value):
        raise PapalCollectionError(f"non-finite JSON value in {path.name}: {value}")

    try:
        payload = path.read_bytes()
        value = json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)
    except (OSError, ValueError, UnicodeError) as error:
        if isinstance(error, PapalCollectionError):
            raise
        raise PapalCollectionError(f"unreadable JSON: {path.name}") from error
    _require(isinstance(value, dict), f"JSON object required: {path.name}")
    return value, hashlib.sha256(payload).hexdigest()


def _revision(value):
    _require(isinstance(value, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z", value),
             "manifest revision must be explicit whole-second UTC")
    try:
        dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as error:
        raise PapalCollectionError("manifest revision is not a calendar timestamp") from error


def _identity(row):
    _require(isinstance(row, dict) and _nonempty(row.get("id")), "document requires an id")
    language = row.get("language")
    _require(isinstance(language, str) and LANGUAGE.fullmatch(language), "invalid document language code")
    return row["id"], language


def _local_file(batch_root, value, suffix, required=True):
    _require(_nonempty(value), "batch file path must be nonempty")
    _require(not any(ord(char) < 32 for char in value), "batch file path contains a control character")
    path = Path(value)
    _require(not path.is_absolute() and ".." not in path.parts and "\\" not in value,
             "batch file path must be relative without traversal")
    resolved = (batch_root / path).resolve()
    _require(resolved.is_relative_to(batch_root), "batch file path escapes its receipt directory")
    _require(resolved.suffix.lower() == suffix, "batch file has an unexpected extension")
    if required:
        _require(resolved.is_file(), f"missing batch output: {value}")
    return resolved if resolved.is_file() else None


def _link(path, out):
    return quote(os.path.relpath(path, out), safe="/")


def _manifest(path):
    data, digest = _json(path)
    _require(data.get("schema") == MANIFEST_SCHEMA, "incorrect source manifest schema")
    _revision(data.get("revision"))
    _require(isinstance(data.get("documents"), list), "source manifest requires documents[]")
    rows = {}
    for row in data["documents"]:
        key = _identity(row)
        _require(key not in rows, "duplicate identity in source manifest")
        rows[key] = row
    return data, digest, rows


def _batch(spec, out):
    _require(isinstance(spec, dict) and _nonempty(spec.get("name")), "batch requires a name")
    _require(all(isinstance(spec.get(key), (str, Path)) for key in ("receipt", "manifest")), "batch requires receipt and manifest paths")
    receipt_path, manifest_path = Path(spec["receipt"]).resolve(), Path(spec["manifest"]).resolve()
    batch_root = receipt_path.parent
    _require(out != batch_root, "collection output cannot replace a batch index")
    receipt, receipt_sha = _json(receipt_path)
    manifest, manifest_sha, sources = _manifest(manifest_path)
    _require(receipt.get("schema") == RECEIPT_SCHEMA, "incorrect batch receipt schema")
    _require(receipt.get("revision") == manifest["revision"], "receipt and frozen manifest revisions disagree")
    if "input_manifest" in receipt or "input_manifest_sha256" in receipt:
        _require(_digest(receipt.get("input_manifest_sha256")), "receipt requires its frozen manifest SHA-256")
        frozen = _local_file(batch_root, receipt.get("input_manifest"), ".json")
        _require(_sha(frozen) == receipt["input_manifest_sha256"] == manifest_sha,
                 "receipt frozen-manifest bytes disagree with the provided source manifest")
    _require(isinstance(receipt.get("documents"), list), "batch receipt requires documents[]")
    rows, seen = [], set()
    for item in receipt["documents"]:
        key = _identity(item)
        _require(key not in seen, "duplicate identity in batch receipt")
        seen.add(key)
        source = sources.get(key)
        _require(source is not None, "batch edition is absent from its frozen manifest")
        effective_revision = source.get("revision", manifest["revision"])
        _revision(effective_revision)
        _require(item.get("render_revision", receipt["revision"]) == effective_revision,
                 "receipt and selected source render revisions disagree")
        for receipt_key, manifest_key in (("artifact_id", "artifact_id"), ("source_sha256", "sha256"),
                                          ("segment_id", "segment_id"), ("physical_line_ranges", "physical_line_ranges")):
            _require(item.get(receipt_key) == source.get(manifest_key),
                     f"receipt and frozen manifest disagree on {receipt_key}")
        _require(_nonempty(item.get("artifact_id")) and _digest(item.get("source_sha256")), "invalid source pins")
        _require(_nonempty(source.get("title")) and _nonempty(source.get("pope")), "source metadata requires title and issuer")
        date = source.get("date")
        if date is not None:
            try:
                _require(isinstance(date, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", date), "invalid source date")
                dt.date.fromisoformat(date)
            except ValueError as error:
                raise PapalCollectionError("invalid source date") from error
        status = item.get("status")
        _require(status in {"compiled", "rendered", "failed"}, "unknown batch result status")
        compiled = status == "compiled"
        files = {}
        for field in ("tex", "body_tex"):
            path = _local_file(batch_root, item.get(field), ".tex", required=compiled)
            if path:
                files[field] = _link(path, out)
        support = item.get("support_tex", [])
        _require(isinstance(support, list), "support_tex requires an array")
        for value in support:
            _local_file(batch_root, value, ".tex", required=compiled)
        if compiled:
            _require(_digest(item.get("pdf_sha256")), "compiled PDF requires a SHA-256")
            _require(type(item.get("pages")) is int and item["pages"] > 0, "compiled PDF requires a positive page count")
            fidelity = item.get("text_fidelity")
            _require(isinstance(fidelity, dict) and fidelity.get("status") == "pass", "compiled PDF lacks a passing text-fidelity receipt")
            path = _local_file(batch_root, item.get("pdf"), ".pdf")
            _require(_sha(path) == item["pdf_sha256"], "compiled PDF SHA-256 mismatch")
            files["pdf"] = _link(path, out)
        elif item.get("pdf"):
            _local_file(batch_root, item["pdf"], ".pdf", required=False)
        language_label = source.get("language_label") or LANGUAGE_NAMES.get(key[1], key[1])
        _require(_nonempty(language_label), "language label must be text")
        corpus = source.get("collection_corpus", spec["name"])
        _require(_nonempty(corpus), "collection corpus must be text")
        row = {"corpus": corpus, "id": key[0], "language": key[1],
               "language_label": language_label,
               "title": source["title"], "issuer": source["pope"], "date": date,
               "status": status, "artifact_id": item["artifact_id"], "source_sha256": item["source_sha256"],
               "receipt_sha256": receipt_sha, "render_revision": effective_revision, "files": files,
               "page_review": {"status": "not-recorded"}}
        if item.get("segment_id"):
            row["segment_id"] = item["segment_id"]
        if compiled:
            row.update(pdf_sha256=item["pdf_sha256"], pages=item["pages"])
        if item.get("error"):
            _require(isinstance(item["error"], str), "batch error must be text")
            row["error"] = item["error"]
        rows.append(row)
    summary = receipt.get("summary")
    expected = {"selected": len(rows), "compiled": sum(row["status"] == "compiled" for row in rows),
                "failed": sum(row["status"] == "failed" for row in rows)}
    _require(isinstance(summary, dict) and all(type(summary.get(key)) is int and summary[key] == value for key, value in expected.items()),
             "batch receipt summary disagrees with its results")
    return rows, {"name": spec["name"], "receipt": _link(receipt_path, out), "receipt_sha256": receipt_sha,
                  "manifest": _link(manifest_path, out), "manifest_sha256": manifest_sha, "revision": manifest["revision"]}


def _pins(row, assertion):
    for key in ("artifact_id", "source_sha256", "segment_id"):
        if key in assertion:
            _require(_nonempty(assertion[key]) and row.get(key) == assertion[key], f"supersession source pin disagrees on {key}")


def _supersede(rows, paths, out):
    actions, excluded, inputs = [], set(), []
    for path in paths:
        path = Path(path).resolve()
        manifest, digest, _ = _manifest(path)
        assertions = manifest.get("supersessions")
        _require(isinstance(assertions, list), "correction manifest requires supersessions[]")
        inputs.append({"path": _link(path, out), "sha256": digest})
        for assertion in assertions:
            _require(isinstance(assertion, dict) and _nonempty(assertion.get("reason")), "supersession requires a reason")
            prior = assertion.get("prior")
            key = _identity(prior)
            _require(_digest(prior.get("pdf_sha256")), "supersession requires an exact prior PDF hash")
            matches = [index for index, row in enumerate(rows) if row["status"] == "compiled"
                       and (row["id"], row["language"]) == key and row["pdf_sha256"] == prior["pdf_sha256"]]
            _require(len(matches) == 1, "supersession prior must match exactly one successful PDF")
            index = matches[0]
            _require(index not in excluded, "conflicting or duplicate supersession prior")
            _pins(rows[index], prior)
            replacement = assertion.get("replacement", "missing")
            _require(replacement is None or isinstance(replacement, dict), "supersession requires replacement or explicit null withdrawal")
            if replacement is not None:
                _identity(replacement)
            excluded.add(index)
            actions.append((index, assertion))
    exclusions = []
    for index, assertion in actions:
        replacement = assertion["replacement"]
        if replacement is not None:
            key = _identity(replacement)
            matches = [row for number, row in enumerate(rows) if number not in excluded and row["status"] == "compiled"
                       and (row["id"], row["language"]) == key]
            _require(len(matches) == 1, "supersession replacement must match exactly one remaining successful PDF")
            _pins(matches[0], replacement)
        exclusions.append({"prior": assertion["prior"], "replacement": replacement, "reason": assertion["reason"],
                           "corpus": rows[index]["corpus"]})
    return [row for index, row in enumerate(rows) if index not in excluded], exclusions, inputs


def _report(value):
    _require(_nonempty(value), "visual review requires a report path")
    path = Path(value)
    _require(not path.is_absolute() and ".." not in path.parts, "visual report must be repo-relative without traversal")
    path = (ROOT / path).resolve()
    _require(path.is_relative_to(ROOT) and path.is_file(), "visual report is absent or escapes the repository")
    return path


def _page_set(value, pages):
    _require(isinstance(value, list) and all(type(page) is int and 1 <= page <= pages for page in value), "invalid reviewed page coverage")
    _require(len(set(value)) == len(value), "duplicate reviewed page coverage")
    return set(value)


def _protect_report_inputs(value, protected):
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"report", "prior_report"} and _nonempty(item):
                _require(not any(ord(char) < 32 for char in item), "visual report path contains a control character")
                protected.add((ROOT / item).resolve())
            elif isinstance(item, (dict, list)):
                _protect_report_inputs(item, protected)
    elif isinstance(value, list):
        for item in value:
            _protect_report_inputs(item, protected)


def _reviews(rows, paths, out, protected_paths=None):
    inputs, seen, unmatched, report_hashes = [], set(), 0, {}
    for path in paths:
        path = Path(path).resolve()
        data, digest = _json(path)
        if protected_paths is not None:
            protected_paths.add(path)
            _protect_report_inputs(data, protected_paths)
        _require(data.get("schema") == REVIEW_SCHEMA and isinstance(data.get("documents"), list), "incorrect visual-review manifest schema")
        top_receipt = data.get("frozen_receipt_sha256")
        _require(_digest(top_receipt), "visual review requires a frozen receipt SHA-256")
        inputs.append({"path": _link(path, out), "sha256": digest})
        for review in data["documents"]:
            key = _identity(review)
            _require(_digest(review.get("pdf_sha256")), "visual review requires an exact PDF SHA-256")
            matches = [row for row in rows if row["status"] == "compiled" and (row["id"], row["language"]) == key
                       and row["pdf_sha256"] == review["pdf_sha256"]]
            if not matches:
                unmatched += 1
                continue
            _require(len(matches) == 1, "visual review PDF identity is ambiguous")
            row = matches[0]
            _require((key, review["pdf_sha256"]) not in seen, "duplicate or conflicting visual review")
            seen.add((key, review["pdf_sha256"]))
            _require(type(review.get("pages")) is int and review["pages"] == row["pages"], "visual review page count disagrees")
            status = review.get("status")
            _require(status in {"PASS", "CHANGES_REQUIRED", "PENDING"}, "unknown visual-review status")
            reviewed_receipt = review.get("receipt_sha256", top_receipt)
            _require(_digest(reviewed_receipt), "visual review requires its original receipt SHA-256")
            same_receipt = reviewed_receipt == row["receipt_sha256"]
            _require(same_receipt or status == "PASS", "receipt portability requires complete PASS review evidence")
            evidence = {"status": {"PASS": "pass", "CHANGES_REQUIRED": "changes-required", "PENDING": "pending"}[status],
                        "review_receipt_sha256": reviewed_receipt, "current_receipt_sha256": row["receipt_sha256"],
                        "receipt_binding": "exact-receipt" if same_receipt else "exact-pdf-bytes"}
            if status != "PENDING" or review.get("report"):
                report = _report(review.get("report"))
                _require(_digest(review.get("report_sha256")), "visual report requires a SHA-256")
                if report not in report_hashes:
                    report_hashes[report] = _sha(report)
                _require(report_hashes[report] == review["report_sha256"], "visual report SHA-256 mismatch")
                evidence.update(report=_link(report, out), report_sha256=review["report_sha256"])
            if status == "PASS":
                inspected = _page_set(review.get("individually_inspected_pages"), row["pages"])
                reused = _page_set(review.get("reused_pages"), row["pages"])
                _require(not inspected & reused and inspected | reused == set(range(1, row["pages"] + 1)), "PASS visual review must cover every page exactly once")
                proofs = review.get("reuse_proofs", [])
                _require(isinstance(proofs, list), "reuse_proofs requires an array")
                proved, retained_proofs = [], []
                for proof in proofs:
                    _require(isinstance(proof, dict) and type(proof.get("page")) is int and proof["page"] in reused, "reuse proof names an unclaimed page")
                    _require(_digest(proof.get("current_raster_sha256")) and proof["current_raster_sha256"] == proof.get("prior_raster_sha256"), "reused page requires equal exact raster hashes")
                    _require(_digest(proof.get("prior_pdf_sha256")), "reused page requires its prior PDF hash")
                    prior_report = _report(proof.get("prior_report"))
                    _require(_digest(proof.get("prior_report_sha256")), "reused page requires its prior report SHA-256")
                    if prior_report not in report_hashes:
                        report_hashes[prior_report] = _sha(prior_report)
                    _require(report_hashes[prior_report] == proof["prior_report_sha256"], "prior visual report SHA-256 mismatch")
                    proved.append(proof["page"])
                    retained_proofs.append({key: proof[key] for key in (
                        "page", "current_raster_sha256", "prior_raster_sha256", "prior_report", "prior_report_sha256",
                        "prior_pdf_sha256", "renderer_fingerprint", "current_renderer_fingerprint",
                        "prior_renderer_fingerprint", "equality_method") if key in proof})
                _require(len(set(proved)) == len(proved) and set(proved) == reused, "every reused page requires one exact proof")
                evidence.update(individually_inspected_pages=sorted(inspected), reused_pages=sorted(reused),
                                reuse_proofs=retained_proofs)
            if status == "CHANGES_REQUIRED":
                row["files"].pop("pdf", None)
            row["page_review"] = evidence
    return inputs, unmatched


def _html(data):
    escape = lambda value: html.escape(str(value), quote=True)
    rows, previous = [], None
    for row in data["documents"]:
        if row["corpus"] != previous:
            rows.append('<tr class="group"><th colspan="9">' + escape(row["corpus"]) + '</th></tr>')
            previous = row["corpus"]
        links = []
        for kind, label in (("pdf", "PDF" if row["page_review"]["status"] == "pass" else "PDF (review pending)"),
                            ("tex", "TeX"), ("body_tex", "Body TeX")):
            if kind in row["files"]:
                links.append('<a href="' + escape(row["files"][kind]) + '">' + label + '</a>')
        review = {"pass": "Layout reviewed", "not-recorded": "Page review not recorded", "pending": "Page review pending",
                  "changes-required": "Layout changes required"}[row["page_review"]["status"]]
        if row["page_review"].get("report"):
            review = '<a href="' + escape(row["page_review"]["report"]) + '">' + review + '</a>'
        values = [escape(row["corpus"]), escape(row["issuer"]), escape(row["date"] or "Unknown"),
                  escape(row["language_label"]), escape(row["title"]) + '<br><small>' + escape(row["id"]) + '</small>',
                  escape(row.get("pages", "—")), " · ".join(links) or "—", escape(row["status"]), review]
        attributes = " ".join('data-' + key + '="' + escape(value) + '"' for key, value in {
            "corpus": row["corpus"], "issuer": row["issuer"], "date": row["date"] or "Unknown",
            "language": row["language_label"], "title": row["title"], "pages": row.get("pages", 0)}.items())
        rows.append('<tr class="edition" ' + attributes + '>' + "".join('<td>' + value + '</td>' for value in values) + '</tr>')
    summary = data["summary"]
    heading = f'{summary["compiled"]} compiled PDFs; {summary["layout_reviewed"]} layout reviewed; {summary["excluded"]} superseded or withdrawn snapshots excluded.'
    if "source_selection_plan" in data:
        heading = f'0 current readers; {summary["source_exclusions"]} source selections superseded or withdrawn.'
    return '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Papal source collection</title><style>
body{font:16px system-ui,sans-serif;line-height:1.5;max-width:110rem;margin:2rem auto;padding:0 1rem}table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;padding:.5rem;border-bottom:1px solid #ccc}th{background:#eee}button,input,select{font:inherit}th button{border:0;background:transparent;text-align:left;padding:0;text-decoration:underline;cursor:pointer}.group th{background:#ddd}.controls{display:flex;gap:1rem;flex-wrap:wrap;margin:1rem 0}small,footer{font-size:.85rem}a{color:#14528c}
</style></head><body><h1>Papal source collection</h1><p>''' + escape(heading) + '''</p>
<p>Local compiled previews. Page review concerns layout; source transcriptions and OCR retain the qualifications in each PDF. These links do not record installation, publication, or source verification. <a href="collection.json">Collection record</a>.</p>
<div class="controls"><label>Search <input id="search" type="search"></label><label>Group by <select id="group"><option value="corpus">Corpus</option><option value="issuer">Issuer</option><option value="date">Date</option><option value="language">Language</option></select></label><span id="visible" aria-live="polite"></span></div>
<div style="overflow-x:auto"><table><thead><tr>''' + "".join('<th scope="col"><button type="button" data-sort="' + key + '">' + label + '</button></th>' for key, label in
       (("corpus", "Corpus"), ("issuer", "Issuer"), ("date", "Date"), ("language", "Language"), ("title", "Title"), ("pages", "Pages"))) + '''<th scope="col">Files</th><th scope="col">Build</th><th scope="col">Page review</th></tr></thead><tbody>''' + "\n".join(rows) + '''</tbody></table></div>
<footer>One language per two-column reading edition unless the historical source explicitly contains several languages. Distinct historical witness identities are retained. Failed builds and rejected layouts have no PDF link.</footer>
<script>
const body=document.querySelector('tbody'), editions=Array.from(body.querySelectorAll('tr.edition'));
const search=document.getElementById('search'), group=document.getElementById('group');
let sort='date', direction=1;
const compare=(a,b,key)=>{const x=a.dataset[key],y=b.dataset[key];if(x==='Unknown')return y==='Unknown'?0:1;if(y==='Unknown')return -1;return x.localeCompare(y,undefined,{numeric:true,sensitivity:'base'});};
function update(){const query=search.value.toLocaleLowerCase().trim();const visible=editions.filter(row=>!query||row.textContent.toLocaleLowerCase().includes(query));visible.sort((a,b)=>compare(a,b,group.value)||direction*compare(a,b,sort)||compare(a,b,'title'));body.replaceChildren();let previous=null;for(const row of visible){const value=row.dataset[group.value];if(value!==previous){const header=document.createElement('tr'),cell=document.createElement('th');header.className='group';cell.colSpan=9;cell.textContent=value;header.append(cell);body.append(header);previous=value;}body.append(row);}document.getElementById('visible').textContent=visible.length+' source editions shown';}
search.addEventListener('input',update);group.addEventListener('change',update);document.querySelectorAll('[data-sort]').forEach(button=>button.addEventListener('click',()=>{direction=sort===button.dataset.sort?-direction:1;sort=button.dataset.sort;update();}));update();
</script></body></html>
'''


def collect_batches(batches, out, supersession_manifests=(), review_manifests=()):
    """Validate every linked output before writing a metadata-only collection."""
    out = Path(out).resolve()
    _require(out.is_relative_to(ROOT / ".scratch") or out.is_relative_to(ROOT / "build"),
             "collection output must be under repository .scratch or build")
    _require(isinstance(batches, (list, tuple)) and batches, "collection requires at least one named batch")
    rows, inputs, names, protected = [], [], set(), set()
    for spec in batches:
        _require(isinstance(spec, dict) and _nonempty(spec.get("name")), "batch requires a name")
        _require(spec["name"] not in names, "duplicate batch name")
        names.add(spec["name"])
        batch_rows, batch_input = _batch(spec, out)
        protected.update(Path(spec[key]).resolve() for key in ("receipt", "manifest"))
        raw_receipt, _ = _json(Path(spec["receipt"]).resolve())
        if raw_receipt.get("input_manifest"):
            protected.add((Path(spec["receipt"]).resolve().parent / raw_receipt["input_manifest"]).resolve())
        rows.extend(batch_rows)
        inputs.append(batch_input)
    rows, excluded, corrections = _supersede(rows, supersession_manifests, out)
    protected.update(Path(path).resolve() for path in supersession_manifests)
    identities = set()
    for row in rows:
        key = _identity(row)
        _require(key not in identities, "conflicting or ambiguous duplicate active identity")
        identities.add(key)
    reviews, unmatched_reviews = _reviews(rows, review_manifests, out, protected)
    rows.sort(key=lambda row: (row["corpus"].casefold(), row["issuer"].casefold(), row["date"] or "9999-99-99", row["language"], row["id"]))
    compiled = [row for row in rows if row["status"] == "compiled"]
    summary = {"batches": len(inputs), "documents": len(rows), "compiled": len(compiled),
               "failed": sum(row["status"] == "failed" for row in rows),
               "rendered": sum(row["status"] == "rendered" for row in rows),
               "layout_reviewed": sum(row["page_review"]["status"] == "pass" for row in compiled),
               "review_pending": sum(row["page_review"]["status"] in {"pending", "not-recorded"} for row in compiled),
               "changes_required": sum(row["page_review"]["status"] == "changes-required" for row in compiled),
               "excluded": len(excluded), "pages": sum(row["pages"] for row in compiled)}
    result = {"schema": SCHEMA, "generator": "typeset-papal collect", "generator_version": 1,
              "batches": inputs, "supersession_inputs": corrections, "review_inputs": reviews,
              "unmatched_review_entries": unmatched_reviews, "documents": rows, "excluded": excluded, "summary": summary}
    _write_collection_outputs(result, out, protected)
    return result


def _write_collection_outputs(result, out, protected_paths=()):
    endpoints = {(out / name).resolve() for name in ("collection.json", "index.html")}
    _require(not endpoints.intersection(protected_paths), "collection output collides with an input or report")
    payloads = {"collection.json": json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                "index.html": _html(result)}
    _require(all(not (out / name).is_symlink() for name in payloads), "collection output file must not be a symlink")
    out.mkdir(parents=True, exist_ok=True)
    for name, payload in payloads.items():
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=out, prefix=".collection-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(payload)
        try:
            temporary.replace(out / name)
        finally:
            temporary.unlink(missing_ok=True)


def collect_empty_plan(manifest, out):
    """Replace stale navigation with an explicit validated zero-reader selection."""
    out = Path(out).resolve()
    _require(out.is_relative_to(ROOT / ".scratch") or out.is_relative_to(ROOT / "build"),
             "collection output must be under repository .scratch or build")
    path = Path(manifest).resolve()
    _require(path not in {out / "collection.json", out / "index.html"},
             "empty collection output collides with its source plan")
    plan, digest, rows = _manifest(path)
    provenance = plan.get("selection_plan")
    _require(not rows and isinstance(provenance, dict) and provenance.get("schema") == PLAN_SCHEMA,
             "empty collection requires a derived source plan with no active readers")
    _require(isinstance(provenance.get("summary"), dict) and type(provenance["summary"].get("selected")) is int
             and provenance["summary"]["selected"] == 0, "empty source plan must select exactly zero readers")
    _require(isinstance(provenance.get("inputs"), list) and provenance["inputs"]
             and isinstance(provenance.get("exclusions"), list), "empty source plan requires input/exclusion provenance")
    _require(all(isinstance(item, dict) and _digest(item.get("sha256")) for item in provenance["inputs"]),
             "empty source plan inputs require exact hashes")
    summary = dict.fromkeys(("batches", "documents", "compiled", "failed", "rendered", "layout_reviewed",
                            "review_pending", "changes_required", "excluded", "pages"), 0)
    summary["source_exclusions"] = len(provenance["exclusions"])
    result = {"schema": SCHEMA, "generator": "typeset-papal collect", "generator_version": 1,
              "selection_kind": "source-only-empty-plan", "batches": [], "documents": [], "excluded": [],
              "supersession_inputs": [], "review_inputs": [], "unmatched_review_entries": 0, "summary": summary,
              "source_selection_plan": {"path": _link(path, out), "sha256": digest,
                                        "revision": plan["revision"], "provenance": provenance}}
    _write_collection_outputs(result, out)
    return result


SOURCE_FIELDS = ("artifact_id", "sha256", "segment_id", "segment_path", "physical_line_ranges",
                 "text_path", "edition_id", "work_id")


def _row_sha(row):
    return hashlib.sha256(json.dumps(row, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def _source_fields(row):
    _require(_nonempty(row.get("artifact_id")) and _digest(row.get("sha256")), "source plan requires exact artifact and SHA-256 pins")
    _require("text" not in row and "blocks" not in row, "source plans accept metadata references, never copied source bodies")
    return {key: row.get(key) for key in SOURCE_FIELDS}


def _plan_pins(row, assertion):
    _require(isinstance(assertion, dict), "source supersession requires exact pins")
    _require(assertion.get("artifact_id") == row.get("artifact_id") and
             assertion.get("source_sha256") == row.get("sha256"), "source supersession artifact/SHA pins disagree")
    if row.get("segment_id") is not None:
        _require(assertion.get("segment_id") == row["segment_id"], "source supersession requires the exact segment pin")
    elif "segment_id" in assertion:
        _require(assertion["segment_id"] is None, "source supersession has an unexpected segment pin")
    for key in ("physical_line_ranges", "text_path", "segment_path", "edition_id", "work_id"):
        if key in assertion:
            _require(_row_sha(assertion[key]) == _row_sha(row.get(key)), f"source supersession disagrees on {key}")
    if "pdf_sha256" in assertion:
        _require(_digest(assertion["pdf_sha256"]), "declared prior PDF hash must be an exact SHA-256")


def plan_sources(base_manifests, correction_manifests, out):
    """Select current source references before rendering, without changing inputs."""
    _require(not Path(out).is_symlink(), "source plan output must not be a symlink")
    out = Path(out).resolve()
    _require((out.is_relative_to(ROOT / ".scratch") or out.is_relative_to(ROOT / "build")) and out.suffix == ".json",
             "source plan must be a JSON file under repository .scratch or build")
    _require(isinstance(base_manifests, (list, tuple)) and base_manifests,
             "source plan requires at least one base or delta manifest")
    _require(isinstance(correction_manifests, (list, tuple)), "source corrections must be an ordered component array")
    active, inputs, exclusions, names = {}, [], [], set()
    counts = {"base_rows": 0, "correction_rows": 0, "metadata_overrides": 0,
              "source_supersessions": 0, "withdrawals": 0}

    def load(spec, role):
        _require(isinstance(spec, dict) and _nonempty(spec.get("name")) and isinstance(spec.get("path"), (str, Path)),
                 "source component requires a name and manifest path")
        _require(spec["name"] not in names, "duplicate source component name")
        names.add(spec["name"])
        path = Path(spec["path"]).resolve()
        _require(path.is_relative_to(ROOT), "source component manifest must remain repository-relative")
        _require(path != out, "source plan cannot replace an input component manifest")
        data, digest, rows = _manifest(path)
        records = []
        for index, row in enumerate(data["documents"]):
            _source_fields(row)
            _require(row.get("date") is None or isinstance(row["date"], str), "source plan date must be text or null")
            revision = row.get("revision", data["revision"])
            _revision(revision)
            records.append((_identity(row), row, {"component": spec["name"], "manifest_sha256": digest,
                "row_index": index, "row_sha256": _row_sha(row), "revision": revision}))
        info = {"name": spec["name"], "role": role, "path": path.relative_to(ROOT).as_posix(),
                "sha256": digest, "revision": data["revision"], "documents": len(rows)}
        inputs.append(info)
        return data, digest, records

    def entry(row, origin, corpus, lineage):
        _require(_nonempty(corpus), "source component corpus must be text")
        selected = copy.deepcopy(row)
        selected["revision"] = origin["revision"]
        selected["collection_corpus"] = corpus
        return {"row": selected, "origin": origin, "lineage": set(lineage)}

    def exclude(old, replacement, component_sha, reason, kind, declared_prior=None):
        record = {"kind": kind, "prior": {"id": old["row"]["id"], "language": old["row"]["language"],
                  "source": _source_fields(old["row"]), "selection": old["origin"]},
                  "replacement": replacement, "correction_manifest_sha256": component_sha, "reason": reason}
        if declared_prior is not None:
            record["declared_prior"] = copy.deepcopy(declared_prior)
        exclusions.append(record)

    for spec in base_manifests:
        _require(isinstance(spec, dict), "source component requires a named manifest")
        _, digest, records = load(spec, spec.get("role", "base"))
        _require(spec.get("role", "base") in {"base", "delta"}, "invalid additive source role")
        for key, row, origin in records:
            _require(key not in active, "unexplained collision between base/delta source identities")
            active[key] = entry(row, origin, row.get("collection_corpus", spec["name"]), {digest})
        counts["base_rows"] += len(records)

    for spec in correction_manifests:
        data, digest, records = load(spec, "correction")
        known_hashes = {item["sha256"] for item in inputs[:-1]}
        base_pin = data.get("base_manifest_sha256")
        if base_pin is not None:
            _require(_digest(base_pin) and base_pin in known_hashes, "correction base manifest SHA-256 is not an included predecessor")
        assertions = data.get("supersessions", [])
        _require(isinstance(assertions, list), "source corrections require a supersessions array")
        replacements, removed, actions = {}, {}, []
        for assertion in assertions:
            _require(isinstance(assertion, dict) and _nonempty(assertion.get("reason")), "source supersession requires a reason")
            prior = assertion.get("prior")
            key = _identity(prior)
            _require(key in active and key not in removed, "source supersession requires one unique active predecessor")
            old = active[key]
            _plan_pins(old["row"], prior)
            if base_pin is not None:
                _require(base_pin in old["lineage"], "correction base pin does not identify this predecessor")
            replacement = assertion.get("replacement", "missing")
            _require(replacement is None or isinstance(replacement, dict), "source supersession requires a replacement or explicit null")
            if replacement is not None:
                target = _identity(replacement)
                _require(target not in replacements, "source replacement must have one uniquely proven predecessor")
                replacements.setdefault(target, []).append(old)
            removed[key] = old
            actions.append((old, assertion))
        for key in removed:
            del active[key]
        for key, row, origin in records:
            old = active.get(key)
            claimed = replacements.get(key, [])
            if claimed:
                _require(old is None, "declared source replacement collides with another active identity")
                corpora = {prior["row"]["collection_corpus"] for prior in claimed}
                corpus = next(iter(corpora)) if len(corpora) == 1 else spec["name"]
                lineage = set().union(*(prior["lineage"] for prior in claimed)) | {digest}
            else:
                _require(old is not None, "correction row has no uniquely proven predecessor")
                _require(_row_sha(_source_fields(old["row"])) == _row_sha(_source_fields(row)),
                         "changed source identity or bounds require an explicit source supersession")
                if base_pin is not None:
                    _require(base_pin in old["lineage"], "correction base pin does not identify this predecessor")
                exclude(old, {"id": key[0], "language": key[1]}, digest,
                        "Explicit metadata/layout correction retains the exact source identity and selection.", "same-source-correction")
                counts["metadata_overrides"] += 1
                corpus, lineage = old["row"]["collection_corpus"], old["lineage"] | {digest}
            active[key] = entry(row, origin, corpus, lineage)
        for old, assertion in actions:
            replacement = assertion["replacement"]
            if replacement is not None:
                target = _identity(replacement)
                _require(target in active, "declared source replacement is absent")
                _plan_pins(active[target]["row"], replacement)
                counts["source_supersessions"] += 1
            else:
                counts["withdrawals"] += 1
            exclude(old, replacement, digest, assertion["reason"],
                    "source-supersession" if replacement is not None else "withdrawal", assertion["prior"])
        counts["correction_rows"] += len(records)
    selected = sorted(active.values(), key=lambda item: (item["row"]["collection_corpus"],
                      item["row"].get("date") or "9999-99-99", item["row"]["id"], item["row"]["language"]))
    selections = [{"id": item["row"]["id"], "language": item["row"]["language"],
                   "collection_corpus": item["row"]["collection_corpus"], **item["origin"]} for item in selected]
    summary = {"inputs": len(inputs), **counts, "selected": len(selected), "excluded": len(exclusions)}
    revisions = [item["revision"] for item in inputs] + [item["row"]["revision"] for item in selected]
    result = {"schema": MANIFEST_SCHEMA, "revision": max(revisions), "documents": [item["row"] for item in selected],
              "selection_plan": {"schema": PLAN_SCHEMA, "row_hash_method": "sha256-json-utf8-sorted-keys-compact-v1",
                                 "inputs": inputs, "selections": selections,
                                 "exclusions": exclusions, "summary": summary}}
    _require(not out.is_symlink(), "source plan output must not be a symlink")
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=out.parent, prefix=".source-plan-", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    try:
        temporary.replace(out)
    finally:
        temporary.unlink(missing_ok=True)
    return result
