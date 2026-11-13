"""Closed, initially inactive admission of ten source-based Latin selections.

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
METHOD_ID = "postconciliar-ten-source-based-latin-20261113-v1"
ADOPTION_PATH = "workflows/reviews/missal-reader-resume-2026-11-12/postconciliar-ten/finite-latin-authority.json"
# Actual Root source/code decisions are pinned for reviewed staging.
# Final canonical integration remains subject to Root review.
ADOPTION_SHA256 = "a36da69def13447a71247d91bdd2ad79df33782e50ab3ecb2dcd8c2d74250275"
TRUSTED_ROOT = Path(__file__).resolve().parents[1]
KEY_FIELDS = ("mass", "form", "proper", "course", "cycle", "occurrence")
SURFACES = frozenset({"web", "download", "print", "cli", "corpus-data", "public-git"})
EXPECTED_KEYS = frozenset((('ot-13', '', 'Collect', '', '', 1),
 ('ot-16', '', 'Collect', '', '', 1),
 ('ot-18', '', 'Collect', '', '', 1),
 ('ot-20', '', 'Prayer after Communion', '', '', 1),
 ('ot-20', '', 'Prayer over the Offerings', '', '', 1),
 ('ot-29', '', 'Prayer after Communion', '', '', 1),
 ('ot-32', '', 'Prayer after Communion', '', '', 1),
 ('ot-32', '', 'Prayer over the Offerings', '', '', 1),
 ('ot-33', '', 'Prayer after Communion', '', '', 1),
 ('ot-9', '', 'Prayer after Communion', '', '', 1)))
# Exact refusal-only signatures; these do not activate the method.
RECOGNITION = ({'key': ['ot-13', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-13-collect',
  'artifact_id': 'artifact.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-13-collect',
  'body_sha256': 'fdd07fe54189d7d80d62951e7286cf34c7b85152d52a9051a4a26e0e70572558',
  'artifact_payload_sha256': '1ee73133bf87e64edf16ed050c6ad9bdb223b5ccf763dec7ca6d0dc2e3aac1b3'},
 {'key': ['ot-16', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-16-collect',
  'artifact_id': 'artifact.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-16-collect',
  'body_sha256': '51c9d78dae29d24905046e2eddd8e8ea4637a00297eb9f33de7a8176637ddf0f',
  'artifact_payload_sha256': 'da87093bd19b1948fb59fe261d0533ced4c6c1fc8489196824788f8ddc34729a'},
 {'key': ['ot-18', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-18-collect',
  'artifact_id': 'artifact.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-18-collect',
  'body_sha256': 'cf89091cf8350fc93248130a5bb7a6ec80cdb86367847d9f158e83d47e5e32b9',
  'artifact_payload_sha256': 'b531e489e2977ace9516ce5a118c75e6848e3b1464224bb639819a252eb568b0'},
 {'key': ['ot-20', '', 'Prayer after Communion', '', '', 1],
  'source_id': 'passage.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-20-postcommunion',
  'artifact_id': 'artifact.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-20-postcommunion',
  'body_sha256': '111ca00384932d15adc3d2e60105ff8651c2a27444da38a0d94e78049255e505',
  'artifact_payload_sha256': '24d50d3d53ba5769198ded3edc82695cd31d156552910740cb9814cbfc21d145'},
 {'key': ['ot-20', '', 'Prayer over the Offerings', '', '', 1],
  'source_id': 'passage.triptych.ot-20-offerings-finite-latin-reconstruction.2026-11-12.complete',
  'artifact_id': 'artifact.triptych.ot-20-offerings-finite-latin-reconstruction.2026-11-12.complete',
  'body_sha256': '9df264da8c50ed0bbb4ea2f625daa3c1dca6fa7ba9b7a414bd5944510f2f538d',
  'artifact_payload_sha256': '92a03777c2f4d28d94adca1bc9ad48128562a61e1a55a7686a09943112be0e80'},
 {'key': ['ot-29', '', 'Prayer after Communion', '', '', 1],
  'source_id': 'passage.triptych.ot29-historical-study-selection.2026-11-12.complete-latin',
  'artifact_id': 'artifact.triptych.ot29-historical-study-selection.2026-11-12.complete-latin',
  'body_sha256': '6cbb1c373bc78e0ac6762983bb35ccd24d972771dc1df7a455342e322c7b459e',
  'artifact_payload_sha256': 'b31b7c34bdad8ce36c56d0688de0f323db8f20053d27700514e98391af973366'},
 {'key': ['ot-32', '', 'Prayer after Communion', '', '', 1],
  'source_id': 'passage.triptych.ot32-historical-study-selection.2026-11-12.complete-latin',
  'artifact_id': 'artifact.triptych.ot32-historical-study-selection.2026-11-12.complete-latin',
  'body_sha256': '18b6feba170a0dd93eb4317365fb6c6ff9e911c9743a76e2d2f7631eba33c98b',
  'artifact_payload_sha256': '4ac81b99c1469d8c36b00f9a446bb3cf46d310bdc884dac29774e9381dd0ef1a'},
 {'key': ['ot-32', '', 'Prayer over the Offerings', '', '', 1],
  'source_id': 'passage.triptych.ot-32-offerings-finite-latin-reconstruction.2026-11-12.complete',
  'artifact_id': 'artifact.triptych.ot-32-offerings-finite-latin-reconstruction.2026-11-12.complete',
  'body_sha256': 'b3a22356bd12d54e562a3d4e86f7defaabbb355b5de542d4572dfee61b7bb90a',
  'artifact_payload_sha256': '67d6996a2513feffbf3e0863ff304d10548f44472b7f57d802f12785e9017aeb'},
 {'key': ['ot-33', '', 'Prayer after Communion', '', '', 1],
  'source_id': 'passage.triptych.ot33-historical-study-selection.2026-11-12.complete-latin',
  'artifact_id': 'artifact.triptych.ot33-historical-study-selection.2026-11-12.complete-latin',
  'body_sha256': 'a879429dc4cd91a83742a2e6ba818fb2f45054396c507a540f8614ba86bc3027',
  'artifact_payload_sha256': '679113f3b0578d20b6a34e79d77cfda2cc6fc11c262d3d39dee1643d094fcefa'},
 {'key': ['ot-9', '', 'Prayer after Communion', '', '', 1],
  'source_id': 'passage.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-9-postcommunion',
  'artifact_id': 'artifact.triptych.ordinarytime-remaining-five-latin-study-reconstruction-20261113.2026-11-13.ot-9-postcommunion',
  'body_sha256': 'dbdb37f66752edf5f91ab107c842bbea7bec105d6ab505c4fb23492b7ee5c788',
  'artifact_payload_sha256': '32cfbbf3bab75d129dbea6b6d1e1a73d3df5a3363621b404250e39b8323fb70b'})
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
