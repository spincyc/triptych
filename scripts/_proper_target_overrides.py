"""Three source-reviewed Bonn witness bodies, without changing inherited owners.

This deliberately bounded schema is a target-witness attestation, not a calendar
rule or a new transcription of the whole pre-1955 recension. Pending review is
valid metadata and releases no text. All bytes and joins are checked on every
application; neither a source id nor a body hash alone is an attestation.
"""
from __future__ import annotations

import copy
from hashlib import sha256
import json
from pathlib import Path
import tomllib

import _calendars

SCHEMA = "triptych-bonn-pentecost-target-propers/v1"
SUFFIX = "-proper-target-overrides-v1.toml"
CALENDAR = "roman-pre-1955"
BASE = "roman-1962"
WITNESS_EDITION = "edition.catholic-church.missale-romanum.2004-bonn-palmarum-reimpressio-editio-28-iuxta-typicam-1920"
WITNESS_ARTIFACT = "artifact.catholic-church.missale-romanum.2004-bonn-palmarum-reimpressio-editio-28-iuxta-typicam-1920.ia-reimpressio-pdf-b676ce5c"
WITNESS_HASH = "b676ce5c9598b434ac6b356dd48a49c7e864deb49a45480db1f2a5068738ca1d"
TARGETS = frozenset(("pentecost", "main", name, "", "", 1)
                    for name in ("Collect", "Secret", "Postcommunion"))
COORDINATE = ("mass", "form_id", "proper", "course", "cycle", "occurrence")
PIN_FIELDS = (*COORDINATE, "base_text_sha256", "text_sha256", "source_id", "target_passage_id", "evidence_sha256")
CONTEXT = {
    "scope": "witness-state-only",
    "edition_id": WITNESS_EDITION,
    "artifact_id": WITNESS_ARTIFACT,
    "artifact_sha256": WITNESS_HASH,
    "label": "Bonn 2004 reimpressio of a conformed edition of about 1954",
    "civil_date_authority": False,
}


PUBLIC_CONTEXT = {field: CONTEXT[field]
                  for field in ("scope", "label", "civil_date_authority")}


def public_context(context: object) -> dict | None:
    """Expose the bounded witness claim, keeping its source-study proof private."""
    if (not isinstance(context, dict) or context != CONTEXT
            or context.get("civil_date_authority") is not False):
        return None
    return dict(PUBLIC_CONTEXT)


def is_public_context(context: object) -> bool:
    """The exact public metadata shape grants neither permission nor date law."""
    return (isinstance(context, dict) and context == PUBLIC_CONTEXT
            and context.get("civil_date_authority") is False)


def digest(value: bytes) -> str:
    return sha256(value).hexdigest()


def path_under(root: Path, relative: object) -> Path:
    if not isinstance(relative, str):
        raise ValueError("payload/review path must be a string")
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != relative:
        raise ValueError("payload/review path must be canonical and repository-relative")
    full = root / path
    if not full.resolve().is_relative_to(root.resolve()):
        raise ValueError("payload/review path escapes the selected repository")
    return full


def exact_body(root: Path, passage: dict, sources: dict) -> str:
    """The schema owns one physical UTF-8 line, excluding its LF terminator."""
    artifact = sources.get(passage.get("artifact_id")) or {}
    edition = sources.get(artifact.get("edition_id")) or {}
    if (passage.get("record_type") != "passage"
            or artifact.get("record_type") != "artifact"
            or passage.get("edition_id") != artifact.get("edition_id")
            or edition.get("record_type") != "edition" or edition.get("language") != "la"
            or artifact.get("storage") != "tracked"
            or not str(artifact.get("media_type") or "").startswith("text/plain")
            or passage.get("artifact_sha256") != artifact.get("sha256")
            or not {"inspected", "verified"} <= set(passage.get("states") or [])
            or not passage.get("verified_on")):
        raise ValueError("body requires an exact retained text artifact and passage")
    payload = path_under(root, artifact.get("path")).read_bytes()
    if digest(payload) != artifact.get("sha256") or len(payload) != artifact.get("byte_size"):
        raise ValueError("body artifact bytes have changed")
    bounds = passage.get("physical_line_ranges")
    if (not isinstance(bounds, list) or len(bounds) != 1
            or not isinstance(bounds[0], list) or len(bounds[0]) != 2
            or type(bounds[0][0]) is not int or bounds[0][0] < 1
            or bounds[0][1] != bounds[0][0]):
        raise ValueError("body passage must identify exactly one physical line")
    if b"\r" in payload:
        raise ValueError("body artifact must use LF line endings")
    lines = payload.decode("utf-8").split("\n")
    if bounds[0][0] > len(lines) or not lines[bounds[0][0] - 1]:
        raise ValueError("body passage line is empty or outside its artifact")
    return lines[bounds[0][0] - 1]


def evidence_fingerprint(row: dict, sources: dict) -> str:
    """Pin source metadata and its evidence/identity ancestors, not just IDs."""
    held, pending = {}, [row["source_id"], row["target_passage_id"],
                         *(row["provenance"].get("publication_source_ids") or [])]
    while pending:
        identifier = pending.pop()
        if identifier in held:
            continue
        record = sources.get(identifier)
        if not isinstance(record, dict):
            raise ValueError("target evidence ancestor is not registered")
        held[identifier] = record
        for field in ("artifact_id", "segment_id", "edition_id", "work_id"):
            if record.get(field):
                pending.append(record[field])
        pending.extend(record.get("projected_from") or [])
        if record.get("derived_from"):
            pending.append(record["derived_from"])
    return digest(json.dumps(held, sort_keys=True, ensure_ascii=False,
                             separators=(",", ":"), default=str).encode())


def locate(document: dict, row: dict):
    mass = _calendars.mass_index(document).get(row["mass"])
    if not isinstance(mass, dict):
        raise ValueError("target owner Mass is missing")
    stamp = mass.get(_calendars.RECENSION) or {}
    if stamp.get("text_from") != BASE or stamp.get("stated"):
        raise ValueError("target owner is not mechanically inherited from the pinned base")
    if row["form_id"] != "main" or mass.get("forms"):
        raise ValueError("this bounded cohort supports only its source-authored main form")
    matching = [proper for proper in mass.get("propers") or []
                if proper.get("name") == row["proper"] and not proper.get("takes_from")]
    occurrence = row["occurrence"]
    if type(occurrence) is not int or not 1 <= occurrence <= len(matching):
        raise ValueError("target source occurrence does not exist")
    owner = matching[occurrence - 1]
    if not isinstance(owner.get("text"), str) or digest(owner["text"].encode()) != row["base_text_sha256"]:
        raise ValueError("inherited target owner has a stale or wrong base body")
    return owner


def load(root: Path, calendar_root: Path, calendar: str, document: dict,
         sources: dict, *, row_problems, source_problems) -> tuple[list[dict], list[str]]:
    """Return only accepted, fully checked exact body replacements."""
    path = calendar_root.parent / "inventories" / (calendar + SUFFIX)
    if not path.is_file():
        return [], []
    try:
        data = tomllib.loads(path.read_text())
        if set(data) != {"schema", "calendar", "base_calendar", "target_context", "review", "entries"}:
            raise ValueError("target overlay has missing or unknown top-level fields")
        if (data["schema"] != SCHEMA or calendar != CALENDAR
                or data["calendar"] != CALENDAR or data["base_calendar"] != BASE
                or document.get("text_from") != BASE or data["target_context"] != CONTEXT):
            raise ValueError("target overlay calendar/base/witness-state context does not match")
        artifact = sources.get(WITNESS_ARTIFACT) or {}
        edition = sources.get(WITNESS_EDITION) or {}
        if (artifact.get("record_type") != "artifact" or artifact.get("edition_id") != WITNESS_EDITION
                or artifact.get("sha256") != WITNESS_HASH
                or edition.get("record_type") != "edition" or edition.get("language") != "la"):
            raise ValueError("accepted Bonn witness artifact identity is not current")
        review = data["review"]
        if not isinstance(review, dict) or set(review) != {"path", "sha256"}:
            raise ValueError("target overlay requires one exact independent-review receipt")
        review_path = path_under(root, review["path"])
        if not str(review["path"]).startswith("src/sources/inventories/reviews/"):
            raise ValueError("target source review must belong to the source inventory")
        review_bytes = review_path.read_bytes()
        if digest(review_bytes) != review["sha256"]:
            raise ValueError("target source review receipt has changed")
        receipt = tomllib.loads(review_bytes.decode("utf-8"))
        if (set(receipt) != {"schema", "disposition", "independent", "reviewer", "target_context", "entries"}
                or receipt["schema"] != "triptych-proper-target-source-review/v1"
                or receipt["target_context"] != CONTEXT
                or receipt["disposition"] not in {"pending", "accepted"}):
            raise ValueError("target source review has invalid schema/context/disposition")
        if receipt["disposition"] == "accepted" and (
                receipt["independent"] is not True or not str(receipt["reviewer"]).strip()):
            raise ValueError("accepted target source review must name an independent reviewer")
        entries = data["entries"]
        if not isinstance(entries, list) or len(entries) != 3:
            raise ValueError("this target overlay must preserve the exact three-owner cohort")
        seen, checked, pins = set(), [], []
        for row in entries:
            if not isinstance(row, dict) or set(row) != {*PIN_FIELDS, "provenance"}:
                raise ValueError("target entry has missing or unknown fields")
            identity = tuple(row[field] for field in COORDINATE)
            if identity not in TARGETS or identity in seen:
                raise ValueError("target entry is outside the exact cohort or duplicated")
            seen.add(identity)
            locate(document, row)
            passage = sources.get(row["source_id"]) or {}
            target = sources.get(row["target_passage_id"]) or {}
            if (target.get("record_type") != "passage"
                    or target.get("edition_id") != WITNESS_EDITION
                    or target.get("artifact_id") != WITNESS_ARTIFACT
                    or target.get("artifact_sha256") != WITNESS_HASH
                    or not {"inspected", "verified"} <= set(target.get("states") or [])
                    or not target.get("verified_on")
                    or not str(target.get("locus") or "").strip()):
                raise ValueError("target attestation requires an inspected verified exact Bonn page passage")
            text = exact_body(root, passage, sources)
            if digest(text.encode()) != row["text_sha256"]:
                raise ValueError("replacement body does not match its attested hash")
            provenance = row["provenance"]
            expected_key = {"mass": row["mass"], "form": "", "proper": row["proper"],
                            "course": row["course"], "cycle": row["cycle"], "occurrence": row["occurrence"]}
            if (any(provenance.get(key) != value for key, value in expected_key.items())
                    or provenance.get("text_sha256") != row["text_sha256"]
                    or provenance.get("source_id") != row["source_id"]
                    or provenance.get("verification_source_id") != row["target_passage_id"]
                    or provenance.get("provenance_status") != "collated"
                    or provenance.get("relationship") != "editorial-projection-exact-to-target"):
                raise ValueError("target body/provenance/source/occurrence pins do not agree")
            errors = [*row_problems("target body", provenance),
                      *source_problems("target body", provenance, sources)]
            if errors:
                raise ValueError("; ".join(errors))
            if evidence_fingerprint(row, sources) != row["evidence_sha256"]:
                raise ValueError("target attestation evidence graph has changed")
            pins.append({field: row[field] for field in PIN_FIELDS})
            checked.append(dict(row, text=text))
        if receipt["entries"] != pins:
            raise ValueError("independent review does not pin every exact owner/body/source")
        if receipt["disposition"] != "accepted":
            return [], []
        return checked, []
    except (OSError, ValueError, TypeError, KeyError, tomllib.TOMLDecodeError) as error:
        return [], [f"{path}: {error}"]


def apply(document: dict, overrides: list[dict]) -> dict:
    if not overrides:
        return document
    result = copy.deepcopy(document)
    for row in overrides:
        owner = locate(result, row)
        owner["text"] = row["text"]
        # The identity, source appointment, English dictionary and every other
        # owner stay inherited. This marker is derived by the validated loader.
        owner["_target_witness_context"] = dict(CONTEXT)
    return result
