"""Whole-source acquisition and canonical identity for papal documents.

Index dates identify acts, not publication rights. Full HTML and candidate text
stay in scratch until an approval pins their exact hashes and historical
publication evidence. Existing work identities are reused by delivery URL.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import threading
import time
import tomllib
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

from _tooling import Example, examples_live_on_the_verbs, with_examples

ROOT = Path(__file__).resolve().parents[1]
CATALOG = Path("src/sources/papal-documents/catalog.json")
SAFE_ID = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
LANGUAGE = re.compile(r"^[a-z][a-z0-9_-]*$")
DEFAULT_CUTOFF = "1930-12-31"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_url(value: str) -> str:
    bits = urlsplit(value)
    if bits.scheme not in {"https", "http"} or bits.hostname not in {"www.vatican.va", "vatican.va"} or bits.username or bits.password:
        raise ValueError("source URL must be a public Vatican HTTP(S) URL")
    if bits.port not in {None, 80, 443}:
        raise ValueError("unexpected source URL port")
    return urlunsplit(("https", "www.vatican.va", bits.path, bits.query, ""))


def read_catalog(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "triptych-papal-documents/v1" or not isinstance(data.get("documents"), list):
        raise ValueError("expected triptych-papal-documents/v1 catalog")
    seen = set()
    for doc in data["documents"]:
        if not isinstance(doc, dict) or not SAFE_ID.fullmatch(str(doc.get("id", ""))):
            raise ValueError("invalid papal document id")
        if doc["id"] in seen:
            raise ValueError("duplicate papal document id: " + doc["id"])
        seen.add(doc["id"])
        for field in ("title", "pope", "pope_id", "document_type"):
            if not isinstance(doc.get(field), str) or not doc[field].strip():
                raise ValueError(f"{doc['id']}: missing {field}")
        if not isinstance(doc.get("languages"), dict):
            raise ValueError(f"{doc['id']}: invalid language deliveries")
        for language, url in doc["languages"].items():
            if not LANGUAGE.fullmatch(language):
                raise ValueError("invalid language code")
            canonical_url(url)
        if doc.get("date") is not None:
            dt.date.fromisoformat(doc["date"])
        if doc.get("resolved_date") is not None:
            dt.date.fromisoformat(doc["resolved_date"])
            if not doc.get("date_resolution"):
                raise ValueError(doc["id"] + ": resolved date lacks reviewed source evidence")
        if doc.get("record_role", "whole-work") not in {"whole-work", "constituent", "composite", "index-mislink"}:
            raise ValueError(doc["id"] + ": unknown catalog record role")
    return data


def write_if_changed(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == data:
        return
    temp = path.with_name(path.name + ".new")
    temp.write_bytes(data)
    temp.replace(path)


def write_json(path: Path, data: object) -> None:
    write_if_changed(path, (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))


def toml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(toml_value(v) for v in value) + "]"
    raise ValueError("unsupported manifest value")


def write_record(path: Path, data: dict) -> None:
    write_if_changed(path, ("\n".join(f"{key} = {toml_value(value)}" for key, value in data.items()) + "\n").encode("utf-8"))


def scratch_path(root: Path, path: Path) -> Path:
    path = path.resolve()
    if not path.is_relative_to((root / ".scratch").resolve()):
        raise ValueError("cache and staging destinations must be beneath the repository .scratch directory")
    return path


def canonical_work_index(root: Path) -> dict:
    """Reuse an exact delivery identity, never an incipit alone."""
    source = root / "src/sources/works"
    works, editions, urls, artifacts, edition_records = {}, {}, {}, {}, {}
    for path in sorted(source.glob("*/*/work.toml")):
        record = tomllib.loads(path.read_text(encoding="utf-8"))
        works[record["id"]] = {"record": record, "path": path}
    for path in sorted(source.glob("*/*/editions/*/edition.toml")):
        record = tomllib.loads(path.read_text(encoding="utf-8"))
        editions[record["id"]] = record["work_id"]
        edition_records[record["id"]] = {"record": record, "path": path}
    for path in sorted(source.glob("*/*/editions/*/artifacts/*/artifact.toml")):
        record = tomllib.loads(path.read_text(encoding="utf-8"))
        artifacts[record["id"]] = {"record": record, "path": path}
        try:
            url = canonical_url(record.get("source_url", ""))
        except (ValueError, TypeError):
            continue
        work_id = editions.get(record.get("edition_id"))
        if work_id:
            urls.setdefault(url, set()).add(work_id)
    return {"works": works, "urls": urls, "editions": editions, "edition_records": edition_records, "artifacts": artifacts}


def container_delivery(root: Path, doc: dict, language: str, index: dict) -> dict | None:
    binding = doc.get("delivery_ownership", {}).get(language)
    if binding is None:
        return None
    if not isinstance(binding, dict) or not binding.get("reason"):
        raise ValueError("container delivery ownership requires a reviewed reason")
    held = index.get("artifacts", {}).get(binding.get("artifact_id"))
    if held is None:
        raise ValueError("container delivery artifact is not registered")
    artifact = held["record"]
    url = canonical_url(doc["languages"][language])
    if canonical_url(binding.get("source_url", "")) != url or artifact.get("source_url") != url:
        raise ValueError("container ownership does not match the exact catalog delivery URL")
    if artifact.get("sha256") != binding.get("source_sha256") or not re.fullmatch(r"[0-9a-f]{64}", str(binding.get("source_sha256", ""))):
        raise ValueError("container ownership does not pin the complete source response")
    edition_id = artifact["edition_id"]
    if index["editions"].get(edition_id) != binding.get("container_work_id"):
        raise ValueError("container artifact is not owned by the declared container work")
    return {"status": "container-owned-delivery", "container_work_id": binding["container_work_id"], "artifact_id": artifact["id"], "artifact_path": str(held["path"].relative_to(root)), "edition_id": edition_id, "edition_path": str(index["edition_records"][edition_id]["path"].relative_to(root)), "source_url": url, "reason": binding["reason"]}


def effective_date(doc: dict) -> str | None:
    return doc.get("resolved_date") if doc.get("date_resolution") else doc.get("date")


def resolved_body_identity(doc: dict) -> bool:
    return doc.get("record_role") == "index-mislink" and bool(doc.get("resolved_title") and doc.get("title_resolution") and doc.get("resolved_date") and doc.get("date_resolution"))


def whole_source_identity(doc: dict) -> bool:
    return doc.get("record_role", "whole-work") == "whole-work" or resolved_body_identity(doc) or related_source_identity(doc)


def linked_constituent_identity(doc: dict) -> bool:
    """An identified abstract work remains distinct from its compound delivery."""
    return doc.get("record_role") == "composite" and bool(doc.get("source_work_id") and doc.get("delivery_ownership"))


def related_source_identity(doc: dict) -> bool:
    identity = doc.get("source_unit_identity")
    return isinstance(identity, dict) and identity.get("kind") == "related-regulation" and bool(identity.get("source_url") and identity.get("locus") and identity.get("basis") and doc.get("source_responsible") and doc.get("display_responsible") and doc.get("source_work_type") == "curial-regulation")


def owned_new_work(root: Path, path: Path) -> bool:
    if not path.is_relative_to(root / "src/sources/works/papal-documents"):
        return False
    relative = str((path / "work.toml").relative_to(root))
    return subprocess.run(["git", "cat-file", "-e", "HEAD:" + relative], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0


def external_source_references(root: Path, work_dir: Path, record_ids: set[str]) -> list[str]:
    references = []
    for path in (root / "src").rglob("*.toml"):
        if path.is_relative_to(work_dir):
            continue
        text = path.read_text(encoding="utf-8")
        if any(json.dumps(value) in text for value in record_ids):
            references.append(str(path.relative_to(root)))
    return references


def reconcile_catalog_owners(root: Path, documents: list[dict], stage: Path) -> list[dict]:
    """Reconcile only new, unpublished task records against explicit review facts."""
    index = canonical_work_index(root)
    changes = []
    for doc in documents:
        role = doc.get("record_role", "whole-work")
        canonical_id = doc.get("source_work_id", "work." + doc["id"])
        for language in doc.get("delivery_ownership", {}):
            controller = container_delivery(root, doc, language, index)
            held = index["works"].get(canonical_id)
            if not held:
                raise ValueError("constituent work identity must already be registered before delivery reconciliation")
            work_dir = held["path"].parent
            if not owned_new_work(root, work_dir):
                raise ValueError("composite-delivery reconciliation would alter a preexisting work")
            for old_path in list(work_dir.glob("editions/*/artifacts/*/artifact.toml")):
                old = tomllib.loads(old_path.read_text(encoding="utf-8"))
                if old.get("source_url") != controller["source_url"] or old.get("media_type") != "text/html":
                    continue
                if old.get("sha256") != doc["delivery_ownership"][language]["source_sha256"]:
                    raise ValueError("old constituent-owned response differs from the reviewed container bytes")
                if external_source_references(root, old_path.parent, {old["id"]}):
                    raise ValueError("constituent-owned compound artifact still has source dependencies")
                backup = stage / "reconciled-deliveries" / sha(old["id"].encode())[:16]
                if backup.exists():
                    raise ValueError("composite-delivery backup already exists")
                backup.parent.mkdir(parents=True, exist_ok=True)
                edition_dir = old_path.parents[2]
                old_edition = tomllib.loads((edition_dir / "edition.toml").read_text(encoding="utf-8"))
                shutil.move(str(old_path.parent), str(backup))
                remaining = [p for p in edition_dir.rglob("*") if p.is_file() and p.name != "edition.toml"]
                if not remaining and not external_source_references(root, edition_dir, {old_edition["id"]}):
                    edition_backup = stage / "reconciled-editions" / sha(old_edition["id"].encode())[:16]
                    edition_backup.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(edition_dir), str(edition_backup))
                changes.append({"id": doc["id"], "action": "retired-constituent-owned-compound-delivery", "retired_artifact_id": old["id"], "container_artifact_id": controller["artifact_id"], "source_sha256": old["sha256"]})
            index = canonical_work_index(root)
        if related_source_identity(doc) and canonical_id in index["works"]:
            path = index["works"][canonical_id]["path"]
            if owned_new_work(root, path.parent):
                record = tomllib.loads(path.read_text(encoding="utf-8"))
                record["responsible"] = doc["source_responsible"]
                record["work_type"] = doc["source_work_type"]
                record["description"] = "Related curial regulation under " + doc["pope"] + ", dated " + (effective_date(doc) or "unresolved") + ". " + doc["source_unit_identity"]["basis"]
                parent = doc.get("parent_work_id")
                if parent in index["works"]:
                    record["relations"] = sorted(set(record.get("relations", [])) | {parent})
                write_record(path, record)
                changes.append({"id": doc["id"], "action": "identified-related-regulation", "work_id": canonical_id, "responsible": doc["source_responsible"]})
        if resolved_body_identity(doc) and canonical_id not in index["works"]:
            backups = [p for p in (stage / "reconciled-records").glob("*/work.toml") if tomllib.loads(p.read_text(encoding="utf-8")).get("id") == canonical_id]
            if len(backups) > 1:
                raise ValueError("multiple retired records claim the resolved body identity")
            if backups:
                _, destination, _ = work_owner(root, doc, index)
                if destination.exists():
                    raise ValueError("resolved body destination already exists")
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(backups[0].parent), str(destination))
                record = tomllib.loads((destination / "work.toml").read_text(encoding="utf-8"))
                record["title"] = doc["resolved_title"]
                record["description"] = "Papal act dated " + doc["resolved_date"] + ", identified from the actual Latin body and the reviewed historical publication. The official index heading instead names " + doc["title"] + "; that heading is retained as mislink provenance only. " + doc["date_resolution"].get("source_url", "") + " " + doc["date_resolution"].get("locus", "")
                write_record(destination / "work.toml", record)
                changes.append({"id": doc["id"], "action": "restored-reviewed-body-identity", "work_id": canonical_id, "title": doc["resolved_title"], "date": doc["resolved_date"]})
                index = canonical_work_index(root)
        if not whole_source_identity(doc) and not linked_constituent_identity(doc):
            held = index["works"].get(canonical_id)
            if not held:
                continue
            work_dir = held["path"].parent
            if not owned_new_work(root, work_dir):
                raise ValueError(doc["id"] + ": reviewed non-whole record has a preexisting work; manual reconciliation required")
            ids = {tomllib.loads(p.read_text(encoding="utf-8"))["id"] for p in work_dir.rglob("*.toml")}
            references = external_source_references(root, work_dir, ids)
            if references:
                raise ValueError(doc["id"] + ": obsolete source records remain referenced by " + ", ".join(references))
            backup = stage / "reconciled-records" / work_dir.name
            if backup.exists():
                raise ValueError("an obsolete-work backup already exists; inspect before retrying")
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(work_dir), str(backup))
            changes.append({"id": doc["id"], "action": "retired-unpublished-non-whole-work", "record_role": role, "retired_work_id": canonical_id})
            index = canonical_work_index(root)
            continue
        reviewed = doc.get("reviewed_aliases", [])
        aliases = doc.get("identity_aliases", [])
        if not reviewed or not aliases:
            continue
        target = index["works"].get(canonical_id)
        if not target:
            continue
        target_dir = target["path"].parent
        for alias in aliases:
            alias_work_id = "work." + alias
            prior = index["works"].get(alias_work_id)
            if not prior or alias_work_id == canonical_id:
                continue
            prior_dir = prior["path"].parent
            if not owned_new_work(root, prior_dir) or not owned_new_work(root, target_dir):
                raise ValueError(doc["id"] + ": alias merge would alter a preexisting canonical identity")
            references = external_source_references(root, prior_dir, {alias_work_id})
            if references:
                raise ValueError(doc["id"] + ": retiring work identity remains referenced outside its editions")
            for edition_dir in sorted((prior_dir / "editions").iterdir()):
                edition_file = edition_dir / "edition.toml"
                edition = tomllib.loads(edition_file.read_text(encoding="utf-8"))
                edition["work_id"] = canonical_id
                destination = target_dir / "editions" / (edition_dir.name + "-alias-" + sha(alias_work_id.encode())[:8])
                if destination.exists():
                    raise ValueError("alias edition destination already exists")
                for artifact_file in edition_dir.glob("artifacts/*/artifact.toml"):
                    artifact = tomllib.loads(artifact_file.read_text(encoding="utf-8"))
                    if artifact.get("path"):
                        payload = root / artifact["path"]
                        artifact["path"] = str((destination / payload.relative_to(edition_dir)).relative_to(root))
                        write_record(artifact_file, artifact)
                write_record(edition_file, edition)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(edition_dir), str(destination))
            backup = stage / "reconciled-records" / prior_dir.name
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(prior_dir), str(backup))
            changes.append({"id": doc["id"], "action": "merged-reviewed-alias", "retired_work_id": alias_work_id, "work_id": canonical_id, "artifact_identity": "Exact artifact and edition IDs, acquired hashes and bytes preserved under the reviewed canonical owner."})
            index = canonical_work_index(root)
    prior_changes = []
    if (stage / "reconciliation.json").exists():
        prior_changes = json.loads((stage / "reconciliation.json").read_text())["changes"]
    write_json(stage / "reconciliation.json", {"schema": "triptych-papal-source-reconciliation/v1", "changes": prior_changes + [change for change in changes if change not in prior_changes]})
    return changes


def work_owner(root: Path, doc: dict, index: dict) -> tuple[str, Path, bool]:
    explicit = doc.get("source_work_id")
    if explicit:
        held = index["works"].get(explicit)
        if held is None:
            raise ValueError("explicit catalog source work is not registered")
        return explicit, held["path"].parent, True
    candidates = set()
    for url in set(doc["languages"].values()) | set(doc.get("url_aliases", [])):
        candidates.update(index["urls"].get(canonical_url(url), set()))
    if len(candidates) > 1:
        raise ValueError(doc["id"] + ": delivery URLs point to multiple existing works; identity review required")
    if candidates:
        work_id = candidates.pop()
        return work_id, index["works"][work_id]["path"].parent, True
    work_id = "work." + doc["id"]
    existing = index["works"].get(work_id)
    if existing:
        return work_id, existing["path"].parent, False
    name = re.sub(r"[^a-z0-9-]+", "-", doc["id"]).strip("-")[:100].rstrip("-")
    name += "-" + sha(doc["id"].encode())[:8]
    return work_id, root / "src/sources/works/papal-documents" / ((effective_date(doc) or "undated") + "-" + name), False


def edition_info(work_id: str, work_dir: Path, language: str, retrieved: str) -> tuple[str, Path]:
    slug = retrieved + "-vatican-" + language.replace("_", "-")
    return "edition." + work_id.removeprefix("work.") + "." + slug, work_dir / "editions" / slug


def register_document(root: Path, doc: dict, index: dict, retrieved: str) -> dict:
    role = doc.get("record_role", "whole-work")
    if not whole_source_identity(doc) and not linked_constituent_identity(doc):
        links = {"id": doc["id"], "record_role": role, "status": "not-registered-as-whole-work", "editions": {}, "reason": "Reviewed catalog record is a " + role + "; no independent whole papal work is inferred.", "issues": doc.get("issues", [])}
        parent = doc.get("parent_work_id")
        if parent:
            if parent not in index["works"]:
                raise ValueError(doc["id"] + ": constituent parent is not registered")
            links["parent_work_id"] = parent
            links["parent_work_path"] = str(index["works"][parent]["path"].relative_to(root))
        return links
    work_id, work_dir, reused = work_owner(root, doc, index)
    if not (work_dir / "work.toml").exists():
        work = {"schema": 1, "record_type": "work", "id": work_id, "title": doc.get("resolved_title", doc["title"]), "responsible": doc.get("source_responsible", doc["pope"]), "work_type": doc.get("source_work_type", doc["document_type"]), "languages": sorted(doc["languages"]), "description": "Source document dated " + (effective_date(doc) or "unresolved in the index") + "; identified from the Holy See index and its explicit reviewed body/date corrections where recorded. Index metadata establishes discovery identity, not whole-text verification. " + " ".join(doc.get("source_index_urls", []))}
        if related_source_identity(doc):
            work["description"] = "Related curial regulation under " + doc["pope"] + ". " + doc["source_unit_identity"]["basis"]
            if doc.get("parent_work_id") in index["works"]:
                work["relations"] = [doc["parent_work_id"]]
        if not work["languages"]:
            del work["languages"]
        write_record(work_dir / "work.toml", work)
        index["works"][work_id] = {"record": work, "path": work_dir / "work.toml"}
    links = {"id": doc["id"], "record_role": role, "work_id": work_id, "work_path": str((work_dir / "work.toml").relative_to(root)), "reused_work": reused, "editions": {}}
    if linked_constituent_identity(doc):
        links.update({"status": "identified-constituent-in-composite", "constituents": doc.get("constituents", []), "issues": doc.get("issues", [])})
    if resolved_body_identity(doc):
        links.update({"status": "resolved-body-identity", "resolved_title": doc["resolved_title"], "resolved_date": doc["resolved_date"], "index_title_raw": doc["index_title_raw"]})
    if related_source_identity(doc):
        links.update({"status": "related-regulation-identity", "responsible": doc["source_responsible"], "source_work_type": doc["source_work_type"], "pope_context": doc["pope"]})
    for language, source_url in sorted(doc["languages"].items()):
        controller = container_delivery(root, doc, language, index)
        if controller:
            links["editions"][language] = controller
            continue
        edition_id, edition_dir = edition_info(work_id, work_dir, language, retrieved)
        for prior_artifact in work_dir.glob("editions/" + retrieved + "-vatican-" + language.replace("_", "-") + "*/artifacts/html/artifact.toml"):
            prior = tomllib.loads(prior_artifact.read_text(encoding="utf-8"))
            if prior.get("source_url") == canonical_url(source_url):
                edition_dir = prior_artifact.parents[2]
                edition_id = prior["edition_id"]
                break
        artifact_file = edition_dir / "artifacts/html/artifact.toml"
        if artifact_file.exists() and tomllib.loads(artifact_file.read_text(encoding="utf-8")).get("source_url") != canonical_url(source_url):
            suffix = "-alias-" + sha(canonical_url(source_url).encode())[:8]
            edition_dir = edition_dir.with_name(edition_dir.name + suffix)
            edition_id += suffix
        if not (edition_dir / "edition.toml").exists():
            edition_notes = "Delivery cataloged from the index; this date identifies the web record, not the original publication or translation date. Cataloging establishes neither wording nor original publication date."
            if resolved_body_identity(doc):
                edition_notes += " Original index label: " + doc["index_title_raw"] + ". The reviewed title identifies the delivered body; see the catalog's title resolution."
            write_record(edition_dir / "edition.toml", {"schema": 1, "record_type": "edition", "id": edition_id, "work_id": work_id, "title": (doc.get("resolved_title") or doc["title"]) + " — Holy See " + language + " web delivery", "language": language, "publication": "Holy See web delivery identified from its official index on " + retrieved, "date": retrieved, "authority": "Holy See web presentation", "notes": edition_notes})
        artifact_id = "artifact." + edition_id.removeprefix("edition.") + ".html"
        artifact_file = edition_dir / "artifacts/html/artifact.toml"
        artifact = {"schema": 1, "record_type": "artifact", "id": artifact_id, "edition_id": edition_id, "artifact_type": "official-html", "media_type": "text/html", "storage": "restricted", "rights_status": "restricted", "rights_basis": "Vatican portal Legal Notes §§4 and 7 do not establish redistribution permission for this HTML delivery: https://www.vatican.va/content/vatican/en/legal-notes.html .", "source_url": canonical_url(source_url), "indexable": False, "notes": "HTML bytes are not retained in Git. A network connection is required to reopen this delivery; the catalog records identity only. Historical wording, translations and modern markup require separate rights review."}
        if artifact_file.exists():
            held = tomllib.loads(artifact_file.read_text(encoding="utf-8"))
            if held.get("source_url") != artifact["source_url"]:
                raise ValueError(doc["id"] + ": delivery URL changed; register another snapshot")
            artifact_id = held["id"]
        else:
            write_record(artifact_file, artifact)
        index["urls"].setdefault(canonical_url(source_url), set()).add(work_id)
        links["editions"][language] = {"edition_id": edition_id, "artifact_id": artifact_id, "edition_path": str((edition_dir / "edition.toml").relative_to(root)), "artifact_path": str(artifact_file.relative_to(root))}
    return links


def candidate_reason(doc: dict, cutoff: str = DEFAULT_CUTOFF) -> str | None:
    if not whole_source_identity(doc):
        return "non-whole-record"
    if "la" not in doc["languages"]:
        return "no-latin-delivery"
    date = effective_date(doc)
    if not date:
        return "unresolved-act-date"
    if doc.get("date_conflicts") and not doc.get("date_resolution"):
        return "conflicting-act-dates"
    if date > cutoff:
        return "later-act-date"
    return None


class Fetcher:
    def __init__(self, cache: Path, pace: float = 0.4):
        self.cache, self.pace = cache, pace
        self.lock = threading.Lock()
        self.next_request = 0.0

    def fetch(self, url: str) -> tuple[bytes, dict]:
        url = canonical_url(url)
        key = sha(url.encode())
        path, meta_path = self.cache / (key + ".html"), self.cache / (key + ".json")
        if path.exists() and meta_path.exists():
            data, meta = path.read_bytes(), json.loads(meta_path.read_text())
            if meta.get("source_url") != url or meta.get("sha256") != sha(data) or meta.get("byte_size") != len(data):
                raise ValueError("cached source failed its hash or URL check")
            return data, meta
        with self.lock:
            delay = max(0.0, self.next_request - time.monotonic())
            if delay:
                time.sleep(delay)
            self.next_request = time.monotonic() + self.pace
        request = Request(url, headers={"User-Agent": "Triptych-source-research/1.0 (+https://github.com/spincyc/triptych)"})
        with urlopen(request, timeout=45) as response:
            if urlsplit(response.url).hostname not in {"vatican.va", "www.vatican.va"}:
                raise ValueError("source redirected away from the Holy See")
            data = response.read()
            length = response.headers.get("Content-Length")
            if length and len(data) != int(length):
                raise ValueError("source download was truncated")
        meta = {"source_url": url, "sha256": sha(data), "byte_size": len(data), "retrieved": utc_now()[:10]}
        write_if_changed(path, data)
        write_json(meta_path, meta)
        return data, meta


def extract_candidate(data: bytes, url: str) -> dict:
    from _typeset_papal import extract_document
    result = extract_document(data, url)
    if not isinstance(result.get("text"), str) or len(result["text"].strip()) < 100:
        raise ValueError("source extraction is empty or implausibly short")
    return result


def normalized_candidate(extracted: dict, approval: dict | None = None) -> str:
    """Apply only exact, recorded exclusions; never rewrite source wording."""
    approval = approval or {}
    blocks = [dict(block) for block in extracted["blocks"]]
    ranges = retained_block_ranges(approval)
    selected_blocks = []
    previous_end = 0
    for retained_range in ranges:
        if not isinstance(retained_range, dict):
            raise ValueError("retained block range requires a bounded selector")
        start, end = retained_range.get("start"), retained_range.get("end")
        if not isinstance(start, int) or isinstance(start, bool) or not isinstance(end, int) or isinstance(end, bool) or not 0 <= start < end <= len(blocks):
            raise ValueError("retained block range must be nonempty, zero-based and end-exclusive inside the complete source")
        if start < previous_end:
            raise ValueError("retained block ranges must be ordered and nonoverlapping")
        if blocks[start]["text"] != retained_range.get("first") or blocks[end - 1]["text"] != retained_range.get("last"):
            raise ValueError("retained block range does not match its exact first/last source pins")
        selected_blocks.extend(blocks[start:end])
        previous_end = end
    if ranges:
        blocks = selected_blocks
    for omitted in approval.get("omit_exact_blocks", []):
        matches = [i for i, block in enumerate(blocks) if block["text"] == omitted]
        if len(matches) != 1:
            raise ValueError("an approved apparatus exclusion must match exactly one whole block")
        del blocks[matches[0]]
    for join in approval.get("join_exact_blocks", []):
        left, right, separator = join.get("left"), join.get("right"), join.get("separator")
        if not isinstance(left, str) or not left or not isinstance(right, str) or not right or separator not in {"", " "}:
            raise ValueError("reviewed block joins require exact nonempty left/right text and an explicit empty or space separator")
        left_matches = [i for i, block in enumerate(blocks) if block["text"] == left]
        right_matches = [i for i, block in enumerate(blocks) if block["text"] == right]
        if len(left_matches) != 1 or len(right_matches) != 1 or right_matches[0] != left_matches[0] + 1:
            raise ValueError("reviewed block join must identify two unique adjacent blocks in source order")
        i = left_matches[0]
        if blocks[i]["kind"] != blocks[i + 1]["kind"]:
            raise ValueError("reviewed block join cannot merge different block kinds")
        blocks[i]["text"] = left + separator + right
        del blocks[i + 1]
    for replacement in reviewed_replacements(approval):
        matches = [i for i, block in enumerate(blocks) if block["text"] == replacement["before"]]
        if len(matches) != 1:
            raise ValueError("a reviewed correction must match one unique whole source block")
        blocks[matches[0]]["text"] = replacement["after"]
    for suffix in approval.get("omit_exact_suffixes", []):
        if not isinstance(suffix, str) or not suffix:
            raise ValueError("apparatus suffix exclusions must be nonempty strings")
        matches = [i for i, block in enumerate(blocks) if block["text"].endswith(suffix)]
        if len(matches) != 1:
            raise ValueError("an apparatus suffix exclusion must match exactly one block end")
        i = matches[0]
        blocks[i]["text"] = blocks[i]["text"][:-len(suffix)].rstrip()
        if not blocks[i]["text"]:
            raise ValueError("use omit_exact_blocks to omit an entire apparatus block")
    for marked in approval.get("strip_asterisk_after", []):
        if not isinstance(marked, str) or not marked or "*" in marked:
            raise ValueError("title marker exclusions require an exact unmarked title")
        token = marked + "*"
        matches = [(i, block["text"].count(token)) for i, block in enumerate(blocks) if token in block["text"]]
        if sum(count for _, count in matches) != 1:
            raise ValueError("a title marker exclusion must match exactly once")
        i = matches[0][0]
        blocks[i]["text"] = blocks[i]["text"].replace(token, marked)
    if approval.get("strip_title_asterisk"):
        changed = False
        for block in blocks:
            if block["kind"] == "heading" and block["text"].endswith("*"):
                block["text"] = block["text"][:-1].rstrip()
                changed = True
        if not changed:
            raise ValueError("approved title marker exclusion matched no heading")
    return "\n\n".join(block["text"] for block in blocks) + "\n"


def retained_block_ranges(approval: dict) -> list[dict]:
    singular = approval.get("retain_exact_block_range")
    plural = approval.get("retain_exact_block_ranges")
    if singular is not None and plural is not None:
        raise ValueError("choose one retained-block selector form")
    if plural is not None:
        if not isinstance(plural, list) or not plural:
            raise ValueError("retained block ranges require a nonempty ordered selector list")
        return plural
    return [singular] if singular is not None else []


def reviewed_replacements(approval: dict) -> list[dict]:
    replacements = approval.get("replace_exact_blocks", [])
    if not isinstance(replacements, list):
        raise ValueError("reviewed source corrections must be a list")
    for replacement in replacements:
        if not isinstance(replacement, dict):
            raise ValueError("reviewed source correction must identify an exact block and witness")
        for key in ("before", "after", "publication_citation", "source_witness_sha256", "locus"):
            if not isinstance(replacement.get(key), str) or not replacement[key].strip():
                raise ValueError("reviewed source correction missing " + key)
        if replacement["before"] == replacement["after"]:
            raise ValueError("reviewed source correction must change the identified erroneous block")
        if not re.fullmatch(r"[0-9a-f]{64}", replacement["source_witness_sha256"]):
            raise ValueError("reviewed source correction requires an exact witness SHA-256")
    return replacements


def validate_approval(doc: dict, approval: dict, raw_hash: str, text_hash: str) -> None:
    if approval.get("source_sha256") != raw_hash or approval.get("text_sha256") != text_hash:
        raise ValueError("approval does not pin the acquired HTML and extracted wording")
    reviewed_replacements(approval)
    approved_extent(approval)
    if retained_block_ranges(approval) and not any(isinstance(approval.get(key), str) and approval[key].strip() for key in ("extent", "source_extent")):
        raise ValueError("a retained Latin constituent requires an explicit source extent")
    if approval.get("language") != "la":
        raise ValueError("approval must identify Latin wording")
    if approval.get("original_language") is True:
        if approval.get("expression_kind", "original-latin") != "original-latin":
            raise ValueError("an original-language approval cannot identify a translation")
    elif approval.get("original_language") is False:
        if approval.get("expression_kind") != "historical-latin-translation":
            raise ValueError("a Latin translation requires an identified historical expression kind")
        note = approval.get("expression_note")
        if not isinstance(note, str) or not note.strip():
            raise ValueError("a historical Latin translation requires an expression_note identifying its published edition")
    else:
        raise ValueError("approval must explicitly identify original language or a historical Latin translation")
    year = approval.get("publication_year")
    if not isinstance(year, int) or isinstance(year, bool) or not 1 <= year <= 1930:
        raise ValueError("approval requires an identified publication no later than 1930")
    for key in ("publication_citation", "rights_basis", "apparatus_review", "reviewed_on"):
        if not isinstance(approval.get(key), str) or not approval[key].strip():
            raise ValueError("approval missing " + key)
    dt.date.fromisoformat(approval["reviewed_on"])
    if approval.get("rights_status") != "public-domain" or approval.get("rights_jurisdiction") != "United States":
        raise ValueError("approval must state the United States public-domain basis")
    if "la" not in doc["languages"] or not whole_source_identity(doc):
        raise ValueError("approval requires a whole-work Latin delivery; act dates alone do not decide publication rights")


def expression_provenance(approval: dict) -> tuple[str, str]:
    """Describe the approved expression without attributing a translation as original."""
    if approval.get("original_language") is False:
        return "Historical Latin translation publication: ", "Historical Latin translation: " + approval["expression_note"].strip()
    return "Original Latin publication: ", ""


def approved_extent(record: dict) -> str:
    """A known missing substantive extent cannot silently become a complete act."""
    kind = record.get("extent_kind", "complete")
    if not isinstance(kind, str) or kind not in {"complete", "fragment"}:
        raise ValueError("extent_kind must be complete or fragment")
    missing = record.get("missing_content")
    if kind == "fragment" and (not isinstance(missing, str) or not missing.strip()):
        raise ValueError("a fragment requires a nonempty missing_content notice")
    if kind == "complete" and missing:
        raise ValueError("a complete extent cannot carry a missing_content notice")
    return kind


def source_qualifications(doc: dict, approval: dict) -> str:
    parts = ["Historical witness: " + approval.get("publication_citation", "unrecorded publication") + ". Uncollated normalized web transcription; source wording and numbering retained apart from the explicitly recorded corrections and apparatus exclusions."]
    limitations = approval.get("textual_limitations", "").strip()
    generic_prefixes = (
        "Normalized Vatican web transcription; historical Latin publication identified, but not a facsimile, corrected text, diplomatic transcription or critical edition. No full-work image collation performed.",
        "Normalized Vatican web transcription, with source errors and delivery-specific punctuation/numbering preserved; not a facsimile, diplomatic transcription or critical edition.",
        "Normalized Vatican web transcription; spelling, punctuation, erroneous words, and reference numbering retained except declared modern apparatus. Not a facsimile, corrected text, or diplomatic edition.",
        "Normalized Vatican web transcription preserving its spelling, punctuation, reference placement and declared source discrepancies; not a diplomatic transcript, facsimile, corrected text or critical edition. Historical publication identity was checked, not every word against page images.",
        "Normalized Vatican web transcription with its spelling, punctuation and reference numbering; not a diplomatic transcript, facsimile, corrected text or critical edition. Sample comparison establishes historical identity, not complete verbal identity to the scan.",
        "Normalized transcription of the identified Latin web witness; not a facsimile or critical edition.",
    )
    for prefix in generic_prefixes:
        if limitations.startswith(prefix):
            limitations = limitations[len(prefix):].strip()
            break
    limitations = limitations.replace("The publication_year field records the latest year of the identified historical volume, not a separately established first-issue date.", "Publication is bounded by the identified volume's final year; its first issue date is unrecorded.")
    if limitations:
        parts.append(limitations)
    for key in ("source_notes", "extent", "source_extent"):
        value = approval.get(key)
        if isinstance(value, str) and value.strip():
            if value.strip() != "A normalized web transcription identified against the contemporary AAS printing; source spelling and punctuation are preserved.":
                parts.append(value.strip())
        elif isinstance(value, list):
            parts.extend(str(item) for item in value if str(item).strip())
        elif isinstance(value, dict) and value:
            parts.append(key.replace("_", " ").capitalize() + ": " + json.dumps(value, ensure_ascii=False, sort_keys=True))
    if retained_block_ranges(approval):
        parts.append("This artifact retains the complete reviewed Latin constituent of a mixed-language web delivery; the appended translation is excluded.")
    if approval.get("join_exact_blocks"):
        parts.append("Declared source paragraph boundaries are joined without supplying or changing letters.")
    for replacement in reviewed_replacements(approval):
        parts.append(replacement.get("reader_note") or "A reviewed source transcription correction replaces “" + replacement["before"] + "” with “" + replacement["after"] + "”, following " + replacement["publication_citation"] + ", " + replacement["locus"] + ".")
    if approved_extent(approval) == "fragment":
        notice = approval["missing_content"].strip()
        if not any(notice in part for part in parts):
            parts.append("Missing content: " + notice)
    if doc.get("date_conflicts"):
        if doc.get("resolved_date") and doc.get("date_resolution"):
            resolution = doc["date_resolution"]
            parts.append("The official indexes give conflicting act dates. The reviewed act date is " + doc["resolved_date"] + ", identified at " + resolution.get("source_url", "the historical publication") + " " + resolution.get("locus", "") + ".")
        else:
            parts.append("The official indexes give conflicting act dates; the act date remains unresolved in this reading edition. The identified historical publication establishes the retained wording's publication basis independently.")
    return " ".join(dict.fromkeys(parts))


def acquire_one(root: Path, doc: dict, links: dict, fetcher: Fetcher, stage: Path, approval: dict | None) -> dict:
    if links["editions"]["la"].get("status") == "container-owned-delivery":
        return {"id": doc["id"], "status": "segmented", "source_url": doc["languages"]["la"], "container_artifact_id": links["editions"]["la"]["artifact_id"], "reason": "The whole compound delivery has a separately owned container; reading editions use the registered constituent segments."}
    url = canonical_url(doc["languages"]["la"])
    if approval and hasattr(fetcher, "cache"):
        allowed_urls = {url} | {canonical_url(u) for u in doc.get("url_aliases", []) if "/la/" in urlsplit(u).path}
        for candidate_url in sorted(allowed_urls):
            meta_file = fetcher.cache / (sha(candidate_url.encode()) + ".json")
            if meta_file.exists() and json.loads(meta_file.read_text()).get("sha256") == approval["source_sha256"]:
                url = candidate_url
                break
    data, meta = fetcher.fetch(url)
    extracted = extract_candidate(data, url)
    payload = normalized_candidate(extracted, approval).encode("utf-8")
    key = sha(doc["id"].encode())[:16]
    candidate_file = stage / (key + ".txt")
    write_if_changed(candidate_file, payload)
    receipt = {"id": doc["id"], "source_url": url, "source_sha256": meta["sha256"], "text_sha256": sha(payload), "byte_size": len(payload), "source_byte_size": len(data), "language": "la", "status": "staged", "candidate_path": str(candidate_file.relative_to(root)), "extractor": extracted.get("extractor", "unknown"), "document_title": extracted.get("title", ""), "publication_review": "Original publication and retained wording require review; act date alone does not establish rights."}
    delivery = links["editions"]["la"]
    raw_path = root / delivery["artifact_path"]
    if tomllib.loads(raw_path.read_text(encoding="utf-8")).get("source_url") != url:
        owner = (root / links["work_path"]).parent
        matches = []
        snapshot = tomllib.loads((root / delivery["edition_path"]).read_text(encoding="utf-8"))["date"]
        for candidate in owner.glob("editions/*/artifacts/*/artifact.toml"):
            record = tomllib.loads(candidate.read_text(encoding="utf-8"))
            edition_file = candidate.parents[2] / "edition.toml"
            edition = tomllib.loads(edition_file.read_text(encoding="utf-8"))
            if record.get("source_url") == url and record.get("media_type") == "text/html" and edition.get("date") == snapshot:
                matches.append((candidate, record, edition_file))
        if len(matches) != 1:
            raise ValueError("approved alias delivery lacks one exact canonical artifact owner")
        raw_path, record, edition_file = matches[0]
        delivery = {"artifact_path": str(raw_path.relative_to(root)), "artifact_id": record["id"], "edition_id": record["edition_id"], "edition_path": str(edition_file.relative_to(root))}
    raw_record = tomllib.loads(raw_path.read_text(encoding="utf-8"))
    if raw_record.get("sha256") and raw_record["sha256"] != meta["sha256"]:
        raise ValueError("HTML changed within an existing dated artifact identity")
    raw_record.update({"sha256": meta["sha256"], "byte_size": len(data), "retrieved": meta["retrieved"], "provenance": "Complete HTML acquired directly over HTTPS; bytes excluded from Git under the portal rights boundary."})
    write_record(raw_path, raw_record)
    if approval:
        validate_approval(doc, approval, meta["sha256"], sha(payload))
        publication_prefix, expression_note = expression_provenance(approval)
        edition_id = delivery["edition_id"]
        edition_dir = (root / delivery["edition_path"]).parent
        artifact_id = "artifact." + edition_id.removeprefix("edition.") + ".latin-text-" + sha(payload)[:12]
        artifact_dir = edition_dir / "artifacts" / ("latin-text-" + sha(payload)[:12])
        text_path = artifact_dir / "text.txt"
        write_if_changed(text_path, payload)
        record = {"schema": 1, "record_type": "artifact", "id": artifact_id, "edition_id": edition_id, "artifact_type": "normalized-transcription", "media_type": "text/plain", "storage": "tracked", "rights_status": "public-domain", "rights_basis": approval["rights_basis"], "rights_jurisdiction": "United States", "source_url": url, "retrieved": meta["retrieved"], "sha256": sha(payload), "byte_size": len(payload), "path": str(text_path.relative_to(root)), "encoding": "utf-8", "indexable": True, "derived_from": delivery["artifact_id"], "transformation": "Extracted complete document text with " + extracted.get("extractor", "typeset-papal") + "; removed navigation and markup, decoded HTML entities, joined blocks with blank lines. " + approval["apparatus_review"], "provenance": "Original Latin publication: " + approval["publication_citation"] + ". Source and text hashes reviewed on " + approval["reviewed_on"] + ".", "notes": "Normalized transcription, not a facsimile or critical edition. Historical Latin wording is public domain in the United States; portal markup and translations have separate rights."}
        record_path = artifact_dir / "artifact.toml"
        record["transformation"] += " Exact per-document exclusions and source/text hash pins are recorded under " + doc["id"] + " in src/sources/papal-documents/publication-approvals.json."
        if retained_block_ranges(approval):
            bounds = ", ".join(str(bound["start"]) + ":" + str(bound["end"]) for bound in retained_block_ranges(approval))
            record["artifact_type"] = "bounded-latin-transcription"
            record["transformation"] += " Retained zero-based block ranges " + bounds + " (ends exclusive), checked by exact first/last block pins, before the declared omissions; this is the complete reviewed Latin constituent, not the whole mixed-language delivery."
        for replacement in reviewed_replacements(approval):
            record["artifact_type"] = "corrected-normalized-transcription"
            record["transformation"] += " Replaced one unique exact whole block from “" + replacement["before"] + "” to “" + replacement["after"] + "” under " + replacement["publication_citation"] + ", " + replacement["locus"] + "; exact witness SHA-256 " + replacement["source_witness_sha256"] + "."
        record["provenance"] = publication_prefix + approval["publication_citation"] + ". Source and text hashes reviewed on " + approval["reviewed_on"] + "."
        if expression_note:
            record["provenance"] += " " + expression_note
        qualification = source_qualifications(doc, approval)
        record["notes"] += " " + qualification
        write_record(record_path, record)
        receipt.update({"status": "retained", "text_path": str(text_path.relative_to(root)), "artifact_id": artifact_id, "rights_status": "public-domain", "rights_basis": approval["rights_basis"], "source_note": qualification, "rights_notice": "Historical Latin wording is public domain in the United States; rights in portal markup, later translations and modern additions are separate."})
        if expression_note:
            receipt["source_note"] = expression_note + " " + receipt["source_note"]
            receipt["expression_kind"] = "historical-latin-translation"
        if "extent_kind" in approval:
            receipt["extent_kind"] = approved_extent(approval)
            if receipt["extent_kind"] == "fragment":
                receipt["missing_content"] = approval["missing_content"].strip()
    write_json(stage / (key + ".json"), receipt)
    return receipt


def manifest(catalog: dict, receipts: list[dict], revision: str) -> dict:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", revision):
        raise ValueError("revision must be an explicit whole-second UTC instant")
    docs = {doc["id"]: doc for doc in catalog["documents"]}
    rows = []
    for receipt in receipts:
        if receipt.get("status") != "retained":
            continue
        doc = docs[receipt["id"]]
        row = {key: doc.get(key) for key in ("id", "title", "pope", "date", "document_type")} | {key: receipt[key] for key in ("language", "source_url", "text_path", "artifact_id", "rights_status", "rights_basis")} | {"sha256": receipt["text_sha256"]}
        row["date"] = effective_date(doc)
        row["title"] = doc.get("resolved_title", doc["title"])
        extent = approved_extent(receipt)
        if "extent_kind" in receipt:
            row["extent_kind"] = extent
        if extent == "fragment":
            row["missing_content"] = receipt["missing_content"].strip()
            if not re.search(r"\bfragment\)?\s*$", row["title"], re.IGNORECASE):
                row["title"] += " — Fragment"
        if related_source_identity(doc):
            row["pope"] = doc["display_responsible"]
            row["pope_context"] = doc["pope"]
            row["document_type"] = doc["source_work_type"]
        for key in ("source_note", "rights_notice"):
            if receipt.get(key):
                row[key] = receipt[key]
        rows.append(row)
    return {"schema": "triptych-papal-typeset/v1", "revision": revision, "documents": sorted(rows, key=lambda row: (row.get("date") or "", row["id"]))}


def withdraw_retained(root: Path, receipt: dict, decision: dict, stage: Path) -> dict:
    """Withdraw only an exact, unpublished payload; retain research bytes and identity."""
    reason = decision.get("withdrawal_reason")
    evidence = decision.get("withdrawal_evidence")
    if not isinstance(reason, str) or not reason.strip() or not evidence:
        raise ValueError("rights withdrawal requires its factual reason and evidence")
    if receipt.get("status") == "withdrawn":
        return receipt
    if receipt.get("status") != "retained":
        return receipt | {"status": "withdrawn", "withdrawal_reason": reason, "withdrawal_evidence": evidence}
    if receipt.get("text_sha256") != decision.get("text_sha256") or receipt.get("source_sha256") != decision.get("source_sha256"):
        raise ValueError("rights withdrawal does not pin the exact source and retained text")
    payload = (root / receipt["text_path"]).resolve()
    if not payload.is_relative_to((root / "src/sources/works").resolve()):
        raise ValueError("rights withdrawal payload is outside the canonical source library")
    relative = str(payload.relative_to(root))
    if subprocess.run(["git", "cat-file", "-e", "HEAD:" + relative], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        raise ValueError("rights withdrawal of an already committed payload requires separate history review")
    record_path = payload.parent / "artifact.toml"
    record = tomllib.loads(record_path.read_text(encoding="utf-8"))
    data = payload.read_bytes()
    if record.get("id") != receipt["artifact_id"] or record.get("path") != relative or record.get("sha256") != sha(data) or sha(data) != receipt["text_sha256"]:
        raise ValueError("rights withdrawal artifact does not match the exact retained payload")
    audit_dir = scratch_path(root, stage / "withdrawals" / sha(receipt["id"].encode())[:16])
    research = audit_dir / (sha(data) + ".txt")
    write_if_changed(research, data)
    write_json(audit_dir / "prior-state.json", {"receipt": receipt, "artifact": record, "decision": decision, "withdrawn_on": utc_now()})
    qualification = "Distribution clearance withdrawn: " + reason + " Evidence: " + str(evidence) + ". Exact acquired HTML and normalized text remain in research scratch; no distribution permission is asserted."
    record.update({"storage": "restricted", "rights_status": "restricted", "rights_basis": qualification, "indexable": False, "notes": qualification})
    record.pop("path", None)
    write_record(record_path, record)
    payload.unlink()
    result = receipt | {"status": "withdrawn", "rights_status": "restricted", "rights_basis": qualification, "source_note": qualification, "publication_review": "Earlier pre-1931 publication inference withdrawn; release evidence identifies 1931 publication.", "withdrawal_reason": reason, "withdrawal_evidence": evidence, "withdrawn_on": utc_now(), "research_text_path": str(research.relative_to(root))}
    result.pop("text_path", None)
    result.pop("rights_notice", None)
    write_json(stage / "candidates" / (sha(receipt["id"].encode())[:16] + ".json"), result)
    return result


def command(args: argparse.Namespace) -> dict:
    root = args.root.resolve()
    if args.verb == "witness":
        # Native page witnesses depend on an existing canonical parent artifact,
        # not on discovery/index entries or network acquisition state.
        from _papal_page_witness import extract_witness, register_witness
        local = lambda path: path if path.is_absolute() else root / path
        recipe = json.loads(local(args.recipe).read_text(encoding="utf-8"))
        operation = register_witness if args.register else extract_witness
        result = operation(root, recipe, local(args.cached_pdf), local(args.scratch))
        receipt = result["receipt"]
        summary = {"status": result.get("status", "reused-staging" if result.get("reused") else "staged"),
                   "parent_artifact_id": receipt["parent_artifact_id"], "pages": receipt["pages"],
                   "sha256": receipt["output_sha256"], "byte_size": receipt["output_byte_size"],
                   "rights": "caller-supplied; extraction does not infer clearance",
                   "source_review": "not assessed; no passage or verified status created"}
        if args.register:
            summary["artifact_ids"] = result["artifact_ids"]
            summary["registration_source"] = result["registration_source"]
            if "staged_output_sha256" in result:
                summary["staged_output_sha256"] = result["staged_output_sha256"]
        else:
            summary["output_path"] = str((result["stage"] / "witness.pdf").relative_to(root))
            summary["receipt_path"] = str((result["stage"] / "receipt.json").relative_to(root))
        return summary
    catalog = read_catalog(args.catalog if args.catalog.is_absolute() else root / args.catalog)
    selected = [d for d in catalog["documents"] if not args.document or d["id"] in args.document]
    if args.document and len(selected) != len(set(args.document)):
        raise ValueError("an explicitly selected document was not found")
    if args.verb == "plan":
        candidates = [d["id"] for d in selected if candidate_reason(d) is None]
        excluded = {reason: sum(candidate_reason(d) == reason for d in selected) for reason in ("non-whole-record", "no-latin-delivery", "unresolved-act-date", "conflicting-act-dates", "later-act-date")}
        return {"status": "ok", "documents": len(selected), "latin_candidates": len(candidates), "candidate_ids": candidates, "excluded": excluded, "rights": "Candidate scope only; promotion requires reviewed publication and exact-wording approval."}
    stage = scratch_path(root, root / args.stage if not args.stage.is_absolute() else args.stage)
    mapping_file = stage / "source-links.json"
    if args.verb == "register":
        canonical_mapping = root / "src/sources/papal-documents/source-links.json"
        previous = {}
        if args.document:
            prior_mapping = canonical_mapping if canonical_mapping.exists() else mapping_file
            if prior_mapping.exists():
                held = json.loads(prior_mapping.read_text(encoding="utf-8"))
                if held.get("schema") != "triptych-papal-source-links/v1" or not isinstance(held.get("documents"), list):
                    raise ValueError("existing source mapping has an invalid schema or documents array")
                for row in held["documents"]:
                    if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"] or row["id"] in previous:
                        raise ValueError("existing source mapping contains an invalid or duplicate document id")
                    previous[row["id"]] = row
        changes = reconcile_catalog_owners(root, selected, stage)
        index = canonical_work_index(root)
        retrieved = catalog.get("retrieved_on", utc_now()[:10])[:10]
        dt.date.fromisoformat(retrieved)
        links = [register_document(root, doc, index, retrieved) for doc in selected]
        previous.update({row["id"]: row for row in links})
        mapped = [previous[key] for key in sorted(previous)] if args.document else links
        mapping = {"schema": "triptych-papal-source-links/v1", "documents": mapped}
        write_json(mapping_file, mapping)
        write_json(canonical_mapping, mapping)
        return {"status": "ok", "documents": len(links), "mapping_documents": len(mapped), "reused_works": sum(l.get("reused_work", False) for l in links), "non_whole_records": sum(l.get("record_role", "whole-work") != "whole-work" for l in links), "reconciled": len(changes), "editions": sum(len(l["editions"]) for l in links), "mapping": "src/sources/papal-documents/source-links.json"}
    if not mapping_file.exists():
        raise ValueError("run register with this --stage before acquisition")
    links = {row["id"]: row for row in json.loads(mapping_file.read_text())["documents"]}
    if args.verb == "acquire":
        approval_data = json.loads(args.approvals.read_text()) if args.approvals else {}
        approvals = approval_data.get("documents", {})
        withdrawals = approval_data.get("withdrawn_documents", {})
        if not isinstance(approvals, dict):
            raise ValueError("approval documents must be an id-keyed object")
        if not isinstance(withdrawals, dict) or approvals.keys() & withdrawals.keys():
            raise ValueError("withdrawn documents must be an id-keyed object disjoint from approvals")
        withheld = [{"id": d["id"], "status": "withheld", "reason": "Reviewed catalog record role " + d["record_role"] + " requires truthful constituent/container or corrected body ownership; it is not registered as an independent whole act."} for d in selected if d["id"] in approvals and not whole_source_identity(d) and not linked_constituent_identity(d)]
        candidates = [d for d in selected if d["id"] not in withdrawals and (linked_constituent_identity(d) or whole_source_identity(d) and (candidate_reason(d) is None or d["id"] in approvals))]
        if args.limit is not None:
            candidates = candidates[:args.limit]
        if not 1 <= args.workers <= 8 or args.pace < 0.1:
            raise ValueError("workers must be 1..8 and pace at least 0.1 seconds")
        fetcher = Fetcher(stage / "raw", args.pace)
        def one(doc: dict) -> dict:
            try:
                return acquire_one(root, doc, links[doc["id"]], fetcher, stage / "candidates", approvals.get(doc["id"]))
            except Exception as error:
                return {"id": doc["id"], "status": "failed", "error": str(error)}
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            receipts = list(pool.map(one, candidates)) + withheld
        previous = {}
        report_file = stage / "acquisition.json"
        if report_file.exists():
            previous = {r["id"]: r for r in json.loads(report_file.read_text())["documents"]}
        for document_id, decision in withdrawals.items():
            if document_id in previous:
                previous[document_id] = withdraw_retained(root, previous[document_id], decision, stage)
        latest_failures = [r for r in receipts if r["status"] == "failed"]
        attempted_failures = len(latest_failures)
        for receipt in receipts:
            old = previous.get(receipt["id"])
            # Re-staging without an approval never downgrades a retained,
            # immutable witness. A fresh failure is still reported below.
            if old and old.get("status") == "retained" and receipt["status"] != "retained":
                continue
            previous[receipt["id"]] = receipt
        receipts = sorted(previous.values(), key=lambda row: row["id"])
        report = {"schema": "triptych-papal-acquisition/v1", "acquired_on": utc_now(), "documents": receipts, "attempted": len(candidates), "attempted_failures": attempted_failures, "latest_failures": latest_failures, "retained": sum(r["status"] == "retained" for r in receipts), "staged": sum(r["status"] == "staged" for r in receipts), "segmented": sum(r["status"] == "segmented" for r in receipts), "withheld": sum(r["status"] == "withheld" for r in receipts), "withdrawn": sum(r["status"] == "withdrawn" for r in receipts), "failed": sum(r["status"] == "failed" for r in receipts)}
        write_json(stage / "acquisition.json", report)
        if args.manifest:
            if not args.revision:
                raise ValueError("--manifest requires explicit --revision")
            write_json(args.manifest, manifest(catalog, receipts, args.revision))
        return {"status": "partial" if report["failed"] or attempted_failures else "ok", "retained": report["retained"], "staged": report["staged"], "segmented": report["segmented"], "withheld": report["withheld"], "withdrawn": report["withdrawn"], "failed": report["failed"], "attempted_failures": attempted_failures, "report": str((stage / "acquisition.json").relative_to(root))}
    report = json.loads((stage / "acquisition.json").read_text())
    result = manifest(catalog, report["documents"], args.revision)
    write_json(args.out, result)
    return {"status": "ok", "documents": len(result["documents"]), "manifest": str(args.out)}


def parser(examples: dict | None = None) -> argparse.ArgumentParser:
    p = examples_live_on_the_verbs(argparse.ArgumentParser(prog="papal-sources", description=__doc__), "papal-sources")
    verbs = p.add_subparsers(dest="verb", required=True)
    for verb, help_text in (("plan", "count original-Latin candidates"), ("register", "register identities without retaining source text"), ("acquire", "stage complete documents and retain approved wording"), ("manifest", "emit the retained-text typesetting manifest")):
        child = verbs.add_parser(verb, help=help_text)
        child.add_argument("--root", type=Path, default=ROOT)
        child.add_argument("--catalog", type=Path, default=CATALOG)
        child.add_argument("--stage", type=Path, default=Path(".scratch/source_records"))
        child.add_argument("--document", action="append", default=[])
        child.add_argument("--json", action="store_true")
        if verb == "acquire":
            child.add_argument("--workers", type=int, default=4)
            child.add_argument("--pace", type=float, default=0.4)
            child.add_argument("--limit", type=int)
            child.add_argument("--approvals", type=Path)
            child.add_argument("--manifest", type=Path)
            child.add_argument("--revision")
        if verb == "manifest":
            child.add_argument("--revision", required=True)
            child.add_argument("--out", type=Path, required=True)
        with_examples(child, (examples or {}).get(verb, ()))
    child = verbs.add_parser("witness", help="extract or register native pages from a pinned cached parent PDF", description="""Stage first, then optionally register three immutable same-edition artifacts.

The JSON recipe must supply schema triptych-papal-page-witness/v1, UTC revision,
slug, title, parent_artifact_path, parent_artifact_id, parent_sha256,
parent_byte_size, edition_id, increasing one-based pages, rights_status,
rights_basis, rights_jurisdiction and extent_note. Native pages
are copied with Poppler; native-bilevel-images additionally requires one exact
image ordinal/dimensions/dpi/pixel_sha256 selector per page. No index catalog,
network access, inferred clearance or source/visual verification is involved.

Use --recipe your-reviewed-recipe.json --cached-pdf .scratch/whole-source.pdf
--scratch .scratch/your-witness-lane to stage and inspect the receipt. Repeat
with --register only after the caller's rights assessment covers that output.
Existing canonical bytes are reused only after exact checks, never replaced.
New registration extracts again from the pinned parent; mutable staging bytes
are never promoted. Poppler trailer IDs can differ; final hashes are reported.
""")
    child.add_argument("--root", type=Path, default=ROOT)
    child.add_argument("--recipe", type=Path, required=True, help="triptych-papal-page-witness/v1 JSON with exact parent, pages and affirmative caller rights")
    child.add_argument("--cached-pdf", type=Path, required=True, help="whole local PDF matching the existing parent artifact SHA and size")
    child.add_argument("--scratch", type=Path, required=True, help="exclusive staging beneath repository .scratch")
    child.add_argument("--register", action="store_true", help="add three immutable same-edition artifacts after mechanical checks; default stages only")
    child.add_argument("--json", action="store_true")
    with_examples(child, (examples or {}).get("witness", ()))
    return p


def main(argv: list[str] | None = None, *, examples: dict | None = None) -> int:
    args = parser(examples).parse_args(argv)
    try:
        result = command(args)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        payload = {"status": "error", "code": "input", "error": str(error), "v": 1}
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if args.json else "papal-sources: " + str(error), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result | {"v": 1}, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    else:
        for key, value in result.items():
            print(f"{key}\t{value}")
    return 1 if result.get("status") == "partial" else 0
