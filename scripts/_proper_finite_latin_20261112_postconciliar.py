"""Closed, initially inactive admission of six source-based Latin selections.

Recognition refuses copies; it never grants permission. Only a code-pinned
Root admission, complete review files and exact source records can admit a
tuple. Source-based reconstruction does not establish the 2008 target text.
"""
from collections.abc import Mapping
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath

BASIS = "qualified-nonoriginal-adaptation"
RELATIONSHIP = "source-based-latin-study-reconstruction"
METHOD_ID = "postconciliar-six-source-based-latin-20261112-v1"
ADOPTION_PATH = "workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-six/finite-latin-authority.json"
# Actual Root code/source adoption is pinned for reviewed staging.
# Canonical integration remains subject to Root's final review.
ADOPTION_SHA256 = "8ce3912dfe6c8724da8067b24c59703d93b22b72f3350a1da6c54d5c9c2ff357"
TRUSTED_ROOT = Path(__file__).resolve().parents[1]
KEY_FIELDS = ("mass", "form", "proper", "course", "cycle", "occurrence")
SURFACES = frozenset({"web", "download", "print", "cli", "corpus-data", "public-git"})
EXPECTED_KEYS = frozenset({
    ("ot-3", "", "Prayer over the Offerings", "", "", 1),
    ("ot-5", "", "Prayer over the Offerings", "", "", 1),
    ("ot-12", "", "Prayer over the Offerings", "", "", 1),
    ("ot-8", "", "Prayer after Communion", "", "", 1),
    ("ot-11", "", "Prayer after Communion", "", "", 1),
    ("ot-12", "", "Prayer after Communion", "", "", 1),
})
# Filled from the immutable candidate tuples; these are refusal-only pins.
RECOGNITION = ({'key': ['ot-11', '', 'Prayer after Communion', '', '', 1],
  'source_id': 'passage.triptych.ot11-haec-tua-latin-study-selection.finite-latin-proposal-2026-11-12.complete-latin',
  'artifact_id': 'artifact.triptych.ot11-haec-tua-latin-study-selection.finite-latin-proposal-2026-11-12.complete-latin',
  'body_sha256': 'cb11f78fd7bc664d8596cf62fe763738549a054552d2facef67105325f60e736',
  'artifact_payload_sha256': 'd776c9b12e4705fdb82d014856714067b6d001d813699b2d354e7aaab919ba2f'},
 {'key': ['ot-12', '', 'Prayer after Communion', '', '', 1],
  'source_id': 'passage.triptych.postconciliar-ot8-ot12-historical-latin-study-assembly.2026-11-12.ot-12-postcommunion',
  'artifact_id': 'artifact.triptych.postconciliar-ot8-ot12-historical-latin-study-assembly.2026-11-12.ot-12-postcommunion',
  'body_sha256': '876c5dbcf544df2efbeb0e77cf2486144830b243a57ed7713822a808bc5fb3a7',
  'artifact_payload_sha256': '38f6b4e4d0cc47cd7dbafd071414f97576b3a41f6572d979fd4d5477fbae7c6c'},
 {'key': ['ot-12', '', 'Prayer over the Offerings', '', '', 1],
  'source_id': 'passage.triptych.ordinarytime-offerings-historical-adaptations.2026-11-12.ot-12-complete-la',
  'artifact_id': 'artifact.triptych.ordinarytime-offerings-historical-adaptations.2026-11-12.ot-12-complete-la',
  'body_sha256': 'd2d0b7227e96809ac08bafe208fcb28b549cf1464e2daff3e09a5a12375f9054',
  'artifact_payload_sha256': '72b31ed2ed746e7491ef182e55dc5530f88e3e62fa1e45e79b37e31c63cb1ba9'},
 {'key': ['ot-3', '', 'Prayer over the Offerings', '', '', 1],
  'source_id': 'passage.triptych.ordinarytime-offerings-historical-adaptations.2026-11-12.ot-3-complete-la',
  'artifact_id': 'artifact.triptych.ordinarytime-offerings-historical-adaptations.2026-11-12.ot-3-complete-la',
  'body_sha256': 'cb21f358f6fdabce9c2068955b0bec34f9447aa0d5cfb9f95ec307ef35d2c57c',
  'artifact_payload_sha256': '7f491ee46910aa495cb785d8e94be8999a0da6ab9df28a0416d18263a731cf71'},
 {'key': ['ot-5', '', 'Prayer over the Offerings', '', '', 1],
  'source_id': 'passage.triptych.ordinarytime-offerings-historical-adaptations.2026-11-12.ot-5-complete-la',
  'artifact_id': 'artifact.triptych.ordinarytime-offerings-historical-adaptations.2026-11-12.ot-5-complete-la',
  'body_sha256': 'd42378c196035ebc6bba7952f3b4d314fb3efc2c1cf9844b300e6ed664acc012',
  'artifact_payload_sha256': 'b5776f8e2a255bdcbfefa0fa0eb2dacf1d1f1764c9acf68ad4d68563c06f66b1'},
 {'key': ['ot-8', '', 'Prayer after Communion', '', '', 1],
  'source_id': 'passage.triptych.postconciliar-ot8-ot12-historical-latin-study-assembly.2026-11-12.ot-8-postcommunion',
  'artifact_id': 'artifact.triptych.postconciliar-ot8-ot12-historical-latin-study-assembly.2026-11-12.ot-8-postcommunion',
  'body_sha256': '965afcd29dd137e8775e8f2efcbc7dd893d64bdf530cfa8e31513a2fc11f1076',
  'artifact_payload_sha256': 'bb3ad6b3199882f075efc0c2f91c9fb7950cbfc1d11b121d2dcaaf2257bd7a0e'})
_UNSELECTED_TEXT = object()


def _digest(value):
    try:
        return sha256(json.dumps(dict(value), sort_keys=True, ensure_ascii=False,
                                 separators=(",", ":")).encode()).hexdigest()
    except (TypeError, ValueError):
        return ""


def _hex(value):
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _data(value):
    value = value.data if hasattr(value, "data") else value
    return value if isinstance(value, Mapping) else {}


def _bytes(root, relative):
    if not isinstance(relative, str) or not relative:
        raise ValueError("finite Latin path missing")
    rel = PurePosixPath(relative)
    if rel.is_absolute() or str(rel) != relative or any(p in {".", ".."} for p in rel.parts):
        raise ValueError("finite Latin path is not canonical and relative")
    root = Path(root).resolve()
    path = root / relative
    if any(part.is_symlink() for part in [path, *path.parents] if part != root and part.is_relative_to(root)):
        raise ValueError("finite Latin path contains a symlink")
    if not path.resolve().is_relative_to(root):
        raise ValueError("finite Latin path escapes repository")
    return path.read_bytes()


def _proof_valid(root, pin):
    return (isinstance(pin, dict) and set(pin) == {"path", "sha256"}
            and isinstance(pin["path"], str)
            and pin["path"].startswith("workflows/reviews/")
            and _hex(pin["sha256"])
            and sha256(_bytes(root, pin["path"])).hexdigest() == pin["sha256"])


def recognition_from_scopes(scopes):
    return tuple({field: scope[field] for field in
                  ("key", "source_id", "artifact_id", "body_sha256", "artifact_payload_sha256")}
                 for scope in scopes)


def _scopes():
    # Deliberately uncached: removing or changing an authority/proof must close
    # an already running process as well as its next invocation.
    if not _hex(ADOPTION_SHA256):
        return ()
    try:
        payload = _bytes(TRUSTED_ROOT, ADOPTION_PATH)
        if sha256(payload).hexdigest() != ADOPTION_SHA256:
            return ()
        authority = json.loads(payload)
        if (not isinstance(authority, dict)
                or set(authority) != {"schema", "method_id", "state", "adoption", "scopes"}
                or authority["schema"] != "triptych-postconciliar-finite-latin-authority/v1"
                or authority["method_id"] != METHOD_ID or authority["state"] != "adopted"
                or not _proof_valid(TRUSTED_ROOT, authority["adoption"])):
            return ()
        scopes = authority["scopes"]
        if not isinstance(scopes, list) or len(scopes) != len(EXPECTED_KEYS):
            return ()
        keys, passages, artifacts = set(), set(), set()
        for scope in scopes:
            if not isinstance(scope, dict) or set(scope) != {
                    "calendar", "key", "row_sha256", "body_sha256", "source_id", "artifact_id",
                    "artifact_payload_sha256", "verification_source_id", "publication_source_ids",
                    "projected_from", "physical_line_ranges", "record_sha256", "proof_files", "public"}:
                return ()
            key = scope["key"]
            if (scope["calendar"] != "postconciliar" or not isinstance(key, list)
                    or len(key) != len(KEY_FIELDS) or any(not isinstance(v, str) for v in key[:-1])
                    or type(key[-1]) is not int or tuple(key) not in EXPECTED_KEYS or tuple(key) in keys):
                return ()
            keys.add(tuple(key))
            if any(not _hex(scope[field]) for field in
                   ("row_sha256", "body_sha256", "artifact_payload_sha256")):
                return ()
            for field in ("source_id", "artifact_id", "verification_source_id"):
                if not isinstance(scope[field], str) or not scope[field]:
                    return ()
            if scope["source_id"] in passages or scope["artifact_id"] in artifacts:
                return ()
            passages.add(scope["source_id"])
            artifacts.add(scope["artifact_id"])
            records = scope["record_sha256"]
            if (not isinstance(records, dict)
                    or not {scope["source_id"], scope["artifact_id"], scope["verification_source_id"]}.issubset(records)
                    or any(not isinstance(k, str) or not k or not _hex(v) for k, v in records.items())):
                return ()
            for field in ("publication_source_ids", "projected_from"):
                values = scope[field]
                if (not isinstance(values, list) or not values or any(not isinstance(v, str) for v in values)
                        or len(values) != len(set(values)) or not set(values).issubset(records)):
                    return ()
            if scope["artifact_id"] not in scope["publication_source_ids"]:
                return ()
            ranges = scope["physical_line_ranges"]
            if (not isinstance(ranges, list) or not ranges or any(
                    not isinstance(r, list) or len(r) != 2 or any(type(n) is not int for n in r)
                    or r[0] < 1 or r[1] < r[0] for r in ranges)):
                return ()
            proof = scope["proof_files"]
            if (not isinstance(proof, dict) or set(proof) != {"source_review", "latin_merits"}
                    or not all(_proof_valid(TRUSTED_ROOT, pin) for pin in proof.values())):
                return ()
            public = scope["public"]
            if (not isinstance(public, dict) or set(public) != {"relationship", "source_date", "provenance_confidence", "note", "notice"}
                    or any(not isinstance(v, str) or not v.strip() for v in public.values())
                    or public["relationship"] != RELATIONSHIP
                    or public["provenance_confidence"] not in {"low", "medium", "high"}):
                return ()
        if keys != EXPECTED_KEYS or recognition_from_scopes(scopes) != RECOGNITION:
            return ()
        return tuple(scopes)
    except (OSError, ValueError, TypeError, KeyError):
        return ()


def _scope_for_row(row):
    row = _data(row)
    key = tuple(row.get(field) for field in KEY_FIELDS)
    return next((s for s in _scopes() if tuple(s["key"]) == key), None)


def _selected_sha256(text):
    # Runtime body has no added LF; the separate carrier pin binds all bytes.
    return sha256(text.encode()).hexdigest() if isinstance(text, str) else None


def claims_row(row):
    row = _data(row)
    if (set(row) == set(KEY_FIELDS) | {"body_status", "text_sha256", "provenance_status",
                                    "publication_status", "publication_basis", "surfaces"}
            and row.get("body_status") == "removed" and row.get("surfaces") == []
            and all(row.get(f) == "unresolved" for f in
                    ("provenance_status", "publication_status", "publication_basis"))):
        return False
    ids = row.get("publication_source_ids")
    ids = ids if isinstance(ids, list) else []
    return (any(METHOD_ID in str(row.get(f) or "") or ADOPTION_PATH in str(row.get(f) or "")
                for f in ("publication_authority", "publication_evidence", "note"))
            or any(row.get("source_id") == s["source_id"] or row.get("text_sha256") == s["body_sha256"]
                   or s["artifact_id"] in ids for s in RECOGNITION))


def claims_artifact(artifact):
    artifact = _data(artifact)
    return (any(METHOD_ID in str(artifact.get(f) or "") or ADOPTION_PATH in str(artifact.get(f) or "")
                for f in ("rights_basis", "notes"))
            or any(artifact.get("id") == s["artifact_id"]
                   or artifact.get("sha256") == s["artifact_payload_sha256"] for s in RECOGNITION))


def claims_reading(passage, artifact, *, text=_UNSELECTED_TEXT):
    return claims_artifact(artifact) or any(
        _data(passage).get("id") == s["source_id"] or _selected_sha256(text) == s["body_sha256"]
        for s in RECOGNITION)


def row_problems(row):
    row = _data(row)
    scope = _scope_for_row(row)
    if (scope is None or _digest(row) != scope["row_sha256"]
            or any(row.get(row_field) != scope[scope_field] for row_field, scope_field in (
                ("text_sha256", "body_sha256"), ("source_id", "source_id"),
                ("verification_source_id", "verification_source_id"),
                ("publication_source_ids", "publication_source_ids")))
            or row.get("relationship") != RELATIONSHIP
            or row.get("provenance_status") != "collated"
            or row.get("publication_status") != "permitted" or row.get("publication_basis") != BASIS
            or not isinstance(row.get("surfaces"), list) or len(row["surfaces"]) != len(SURFACES)
            or any(not isinstance(s, str) for s in row["surfaces"])
            or set(row["surfaces"]) != SURFACES
            or row.get("note") != scope["public"]["note"]
            or row.get("provenance_confidence") != scope["public"]["provenance_confidence"]
            or row.get("source_date") != scope["public"]["source_date"]):
        return ["Postconciliar finite Latin requires its exact adopted owner/body/proof/surface tuple"]
    return []


def authority_problems(root):
    try:
        authority = json.loads(_bytes(root, ADOPTION_PATH))
        if (not _scopes() or sha256(_bytes(root, ADOPTION_PATH)).hexdigest() != ADOPTION_SHA256
                or not _proof_valid(root, authority["adoption"])
                or not all(_proof_valid(root, pin) for s in authority["scopes"] for pin in s["proof_files"].values())):
            raise ValueError("authority or proof mismatch")
        return []
    except (OSError, ValueError, TypeError, KeyError):
        return ["Postconciliar finite Latin requires the actual pinned Root admission and review files"]


def _record_problems(scope, sources):
    if not isinstance(sources, Mapping):
        return ["Postconciliar finite Latin requires every registered source controller"]
    problems = ["Postconciliar finite Latin controller missing or changed: " + name
                for name, expected in scope["record_sha256"].items()
                if _digest(_data(sources.get(name))) != expected]
    passage, artifact = _data(sources.get(scope["source_id"])), _data(sources.get(scope["artifact_id"]))
    if (not isinstance(passage.get("notes"), str)
            or scope["public"]["note"] not in passage["notes"]):
        problems.append("Postconciliar finite Latin source passage omits its exact Latin qualification")
    if (passage.get("artifact_id") != scope["artifact_id"]
            or passage.get("artifact_sha256") != scope["artifact_payload_sha256"]
            or passage.get("physical_line_ranges") != scope["physical_line_ranges"]
            or artifact.get("sha256") != scope["artifact_payload_sha256"]
            or artifact.get("projected_from") != scope["projected_from"]):
        problems.append("Postconciliar finite Latin controller/range edges differ from admission")
    return problems


def source_problems(row, sources, *, effective_calendar=""):
    if effective_calendar != "postconciliar":
        return ["Postconciliar finite Latin admits no other calendar or inherited permission"]
    problems = row_problems(row)
    return problems or _record_problems(_scope_for_row(row), sources)


def artifact_problems(root, artifact, *, sources=None):
    artifact = _data(artifact)
    scope = next((s for s in _scopes() if s["artifact_id"] == artifact.get("id")), None)
    problems = authority_problems(root)
    if scope is None or _digest(artifact) != scope["record_sha256"][scope["artifact_id"]]:
        return problems + ["Postconciliar finite Latin carrier is outside exact adopted scope"]
    try:
        if sha256(_bytes(root, artifact.get("path"))).hexdigest() != scope["artifact_payload_sha256"]:
            raise ValueError("carrier changed")
    except (OSError, ValueError):
        problems.append("Postconciliar finite Latin carrier payload is missing or changed")
    return problems + _record_problems(scope, sources)


def reading_problems(root, passage, artifact, *, sources=None, text=_UNSELECTED_TEXT):
    passage, artifact = _data(passage), _data(artifact)
    scope = next((s for s in _scopes() if s["source_id"] == passage.get("id")), None)
    problems = artifact_problems(root, artifact, sources=sources)
    if (scope is None or artifact.get("id") != scope["artifact_id"]
            or _digest(passage) != scope["record_sha256"][scope["source_id"]]):
        return problems + ["Postconciliar finite Latin reading requires exact passage/controller/ranges"]
    if text is not _UNSELECTED_TEXT and _selected_sha256(text) != scope["body_sha256"]:
        problems.append("Postconciliar finite Latin selected text differs from adopted whole body")
    return problems


def claims_public(latin):
    latin = _data(latin)
    provenance = _data(latin.get("provenance"))
    return (provenance.get("relationship") == RELATIONSHIP
            or any(latin.get("text_sha256") == s["body_sha256"]
                   or provenance.get("source_id") == s["source_id"] for s in RECOGNITION))


def public_scope(latin):
    latin = _data(latin)
    provenance, publication = _data(latin.get("provenance")), _data(latin.get("publication"))
    surfaces = publication.get("surfaces")
    if not isinstance(surfaces, list) or any(not isinstance(s, str) for s in surfaces):
        return None
    for scope in _scopes():
        public = scope["public"]
        if (latin.get("text_sha256") == scope["body_sha256"]
                and provenance.get("source_id") == scope["source_id"]
                and provenance.get("status") == "collated"
                and provenance.get("relationship") == public["relationship"]
                and provenance.get("source_date") == public["source_date"]
                and provenance.get("provenance_confidence") == public["provenance_confidence"]
                and provenance.get("verification_source_id", scope["verification_source_id"]) == scope["verification_source_id"]
                and latin.get("note") == public["note"]
                and publication.get("status") == "permitted" and publication.get("basis") == BASIS
                and publication.get("notice", public["notice"]) == public["notice"]
                and publication.get("source_ids") in (scope["publication_source_ids"], [scope["artifact_id"]])
                and sorted(surfaces) == sorted(SURFACES)
                and latin.get("state") is None and not latin.get("reason")
                and latin.get("withheld") is False):
            return {"source_id": scope["source_id"], "artifact_id": scope["artifact_id"],
                    "body_sha256": scope["body_sha256"], **public}
    return None


def cache_fingerprint(root):
    digest = sha256(Path(__file__).read_bytes())
    # Inactive code reads no authority path. Activation must add ADOPTION_PATH
    # and all referenced proof paths to the browser-product input recipe.
    if _hex(ADOPTION_SHA256):
        paths = [ADOPTION_PATH]
        try:
            authority = json.loads(_bytes(root, ADOPTION_PATH))
            paths += [authority["adoption"]["path"]]
            paths += [pin["path"] for s in authority["scopes"] for pin in s["proof_files"].values()]
        except (OSError, ValueError, TypeError, KeyError):
            pass
        for path in sorted(set(paths)):
            try:
                value = sha256(_bytes(root, path)).hexdigest()
            except (OSError, ValueError):
                value = "missing-or-invalid"
            digest.update((path + "\0" + value + "\0").encode())
    return digest.hexdigest()
