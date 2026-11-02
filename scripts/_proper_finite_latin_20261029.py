"""Closed successor for the separately adopted 29 October Latin assessment.

The authority digest is a code-owned pin, not a permission supplied by source
metadata. An absent or unadopted authority admits no row, carrier or reading.
Ordinary public-domain carriers in the same edition remain outside this scope.
"""
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from collections.abc import Mapping

BASIS = "qualified-nonoriginal-adaptation"
METHOD_ID = "english-completion-20261029-finite-latin-v1"
ADOPTION_PATH = 'workflows/reviews/missal-english-completion-2026-10-29/roman-1962/finite-latin-authority-v2.json'
# Set only to the actual independently reviewed root adoption's byte digest.
ADOPTION_SHA256 = '495e5b3672cccb8f2c3ea07398104c4b72026ffb7139de21d25087edcab1f48e'
# These recognition pins survive missing authority data. They classify copied
# bodies for refusal; only the exact authority below can authorize new wording.
RECOGNITION = ({'key': ['beatae-mariae-virginis-reginae', '', 'Alleluia', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.queenship-regular-alleluia-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.queenship-regular-alleluia-qualified-01c6691e',
  'body_sha256': '01c6691e3d76f113226e381bcb55c959ab40f630541c544fbbfadb0a110f2071',
  'artifact_payload_sha256': '01c6691e3d76f113226e381bcb55c959ab40f630541c544fbbfadb0a110f2071'},
 {'key': ['beatae-mariae-virginis-reginae', '', 'Introit', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.queenship-introit-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.queenship-introit-qualified-62bc1f50',
  'body_sha256': '62bc1f505027f3ba9f914511ae9c836b6b460068c08409677226a16ff44de459',
  'artifact_payload_sha256': '62bc1f505027f3ba9f914511ae9c836b6b460068c08409677226a16ff44de459'},
 {'key': ['beatae-mariae-virginis-reginae', '', 'Offertory', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.queenship-offertory-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.queenship-offertory-qualified-f4e866f4',
  'body_sha256': 'f4e866f44553d4181484958a6e4d79ffe7d1e560a4a56f39c298b877093de446',
  'artifact_payload_sha256': 'f4e866f44553d4181484958a6e4d79ffe7d1e560a4a56f39c298b877093de446'},
 {'key': ['chrism-mass', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.chrism-collect-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.chrism-collect-qualified-100ae514',
  'body_sha256': '100ae514cc635ab67fa0b2f223954bbb9053f77c01dead58eb11309c16815d33',
  'artifact_payload_sha256': '100ae514cc635ab67fa0b2f223954bbb9053f77c01dead58eb11309c16815d33'},
 {'key': ['comm-s-silvestri-i-papae-confessoris', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.comm-s-silvestri-i-papae-confessoris--collect--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.comm-s-silvestri-i-papae-confessoris--collect--1',
  'body_sha256': '61fa6b8ea693b00660f9d11521ac5f6330018be9982109845a252f53cd056f53',
  'artifact_payload_sha256': '61fa6b8ea693b00660f9d11521ac5f6330018be9982109845a252f53cd056f53'},
 {'key': ['comm-s-zephyrini-papae-martyris', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.comm-s-zephyrini-papae-martyris--collect--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.comm-s-zephyrini-papae-martyris--collect--1',
  'body_sha256': 'f8732dcb77e4139160ed879dc19947b26595c5d3541442c3f9ec67cc5bf774ad',
  'artifact_payload_sha256': 'f8732dcb77e4139160ed879dc19947b26595c5d3541442c3f9ec67cc5bf774ad'},
 {'key': ['commune-summorum-pontificum', '', 'Collect (in plurali)', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.pontiff-plural-collect-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.pontiff-plural-collect-qualified-77215320',
  'body_sha256': '77215320cce36c1a3823c3643d63bac8f3f98579ded3eb454c1fead0f6abf440',
  'artifact_payload_sha256': '77215320cce36c1a3823c3643d63bac8f3f98579ded3eb454c1fead0f6abf440'},
 {'key': ['commune-summorum-pontificum', '', 'Postcommunion', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.pontiff-postcommunion-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.pontiff-two-qualified-3920bd77',
  'body_sha256': 'bfd0be06cd5ff6e036d7a9e22ee73a2bec99a413c24cc12baefc939a3db52bce',
  'artifact_payload_sha256': '3920bd772a32ebba24b336a71f9bcd30eeff745c60630d5fe20739609e58a75b'},
 {'key': ['commune-summorum-pontificum', '', 'Secret', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.pontiff-secret-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.pontiff-two-qualified-3920bd77',
  'body_sha256': '513de5a7dff9120d02f2fcc6cbc4c5a9d19a69ffd18e9075c5325885a98e43ab',
  'artifact_payload_sha256': '3920bd772a32ebba24b336a71f9bcd30eeff745c60630d5fe20739609e58a75b'},
 {'key': ['easter-vigil', '', 'Blessing of the Lighted Candle', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.lighted-candle-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.lighted-candle-qualified-05954809',
  'body_sha256': '0595480950da324de25ef33113f56537a979517bd4bd23beb75d7643f3310b5f',
  'artifact_payload_sha256': '0595480950da324de25ef33113f56537a979517bd4bd23beb75d7643f3310b5f'},
 {'key': ['exaltatione-s-crucis', '', 'Offertory', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.cross-offertory-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.cross-offertory-qualified-18060fef',
  'body_sha256': '18060fef847e0615136dba2a6e73b16797e3b944665c4e1475dc8643be33fa79',
  'artifact_payload_sha256': '18060fef847e0615136dba2a6e73b16797e3b944665c4e1475dc8643be33fa79'},
 {'key': ['good-friday', '', 'Improperia', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.improperia-whole-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.improperia-whole-qualified-83cbd703',
  'body_sha256': '83cbd70391a22369245ab9c1019d3d25db59e02b5b267474f3b039130d40a616',
  'artifact_payload_sha256': '83cbd70391a22369245ab9c1019d3d25db59e02b5b267474f3b039130d40a616'},
 {'key': ['immaculati-cordis-beatae-mariae-virginis', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.immaculati-cordis-beatae-mariae-virginis--collect--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.immaculati-cordis-beatae-mariae-virginis--collect--1',
  'body_sha256': 'c8b53661561aac747517845360d96151db5afb6707c0c3b798b8de710559395a',
  'artifact_payload_sha256': 'c8b53661561aac747517845360d96151db5afb6707c0c3b798b8de710559395a'},
 {'key': ['immaculati-cordis-beatae-mariae-virginis', '', 'Postcommunion', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.immaculati-cordis-beatae-mariae-virginis--postcommunion--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.immaculati-cordis-beatae-mariae-virginis--postcommunion--1',
  'body_sha256': '6c81c9d5ef0912c0e01fc911ab4dc9fe86648e27e49651092086e38d2ca17795',
  'artifact_payload_sha256': '6c81c9d5ef0912c0e01fc911ab4dc9fe86648e27e49651092086e38d2ca17795'},
 {'key': ['palm-sunday', '', 'Blessing of the Palms', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.palm-blessing-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.palm-blessing-qualified-800c4d2c',
  'body_sha256': '800c4d2cbcdd38b63a488b726080ae2c8497cd882d277602dd389a396c01f31e',
  'artifact_payload_sha256': '800c4d2cbcdd38b63a488b726080ae2c8497cd882d277602dd389a396c01f31e'},
 {'key': ['s-clementis-i-papae-martyris', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-clementis-i-papae-martyris--collect--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-clementis-i-papae-martyris--collect--1',
  'body_sha256': 'd57235904e4e32436dfda5e58d4ac5c98822e784725000a41d75bbc1a24d4aa8',
  'artifact_payload_sha256': 'd57235904e4e32436dfda5e58d4ac5c98822e784725000a41d75bbc1a24d4aa8'},
 {'key': ['s-clementis-i-papae-martyris', '', 'Postcommunion', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-clementis-i-papae-martyris--postcommunion--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-clementis-i-papae-martyris--postcommunion--1',
  'body_sha256': 'bfd0be06cd5ff6e036d7a9e22ee73a2bec99a413c24cc12baefc939a3db52bce',
  'artifact_payload_sha256': 'bfd0be06cd5ff6e036d7a9e22ee73a2bec99a413c24cc12baefc939a3db52bce'},
 {'key': ['s-clementis-i-papae-martyris', '', 'Secret', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-clementis-i-papae-martyris--secret--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-clementis-i-papae-martyris--secret--1',
  'body_sha256': '85e15b6f86d5c6f8c122d9c2c70203102ad0659a6006d502467d9e1afb0628de',
  'artifact_payload_sha256': '85e15b6f86d5c6f8c122d9c2c70203102ad0659a6006d502467d9e1afb0628de'},
 {'key': ['s-ioannis-bosco-confessoris', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-ioannis-bosco-confessoris--collect--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-ioannis-bosco-confessoris--collect--1',
  'body_sha256': '20e15f699f0c8c1a9538024049d905c97a6d86577e24a2f5d3cae4a9c9b60155',
  'artifact_payload_sha256': '20e15f699f0c8c1a9538024049d905c97a6d86577e24a2f5d3cae4a9c9b60155'},
 {'key': ['s-ioannis-bosco-confessoris', '', 'Postcommunion', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-ioannis-bosco-confessoris--postcommunion--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-ioannis-bosco-confessoris--postcommunion--1',
  'body_sha256': '4f47d9dd70abae1166e980d2935e2a4552abd9e65d7105af44e7f8909fce62ea',
  'artifact_payload_sha256': '4f47d9dd70abae1166e980d2935e2a4552abd9e65d7105af44e7f8909fce62ea'},
 {'key': ['s-ioannis-damasceni-confessoris-ecclesiae-doctoris', '', 'Offertory', '', '', 2],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.damascene-paschal-offertory-qualified',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.damascene-paschal-offertory-qualified-e88531b6',
  'body_sha256': 'e88531b6aff711ffb42e4d411fc44e81d0f07c5836d36e34fe3570b33a8a3c96',
  'artifact_payload_sha256': 'e88531b6aff711ffb42e4d411fc44e81d0f07c5836d36e34fe3570b33a8a3c96'},
 {'key': ['s-laurentii-brundusio-confessoris-ecclesiae-doctoris', '', 'Collect', '', '', 1],
  'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-laurentii-brundusio-confessoris-ecclesiae-doctoris--collect--1',
  'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29-sanctoral-english-completion.s-laurentii-brundusio-confessoris-ecclesiae-doctoris--collect--1',
  'body_sha256': '9d2e1a29fd2df2395e01d7078745f77af00df9a266f597ea9b822c49d4eb8005',
  'artifact_payload_sha256': '9d2e1a29fd2df2395e01d7078745f77af00df9a266f597ea9b822c49d4eb8005'})
PRIOR_ROUTES = {'row_sha256': [], 'artifacts': [], 'readings': []}
TRUSTED_ROOT = Path(__file__).resolve().parents[1]
KEY_FIELDS = ("mass", "form", "proper", "course", "cycle", "occurrence")
_UNSELECTED_TEXT = object()


def _hex_digest(value):
    return (isinstance(value, str) and len(value) == 64
            and all(c in "0123456789abcdef" for c in value))


def _digest(value):
    try:
        return sha256(json.dumps(dict(value), sort_keys=True, ensure_ascii=False,
                                 separators=(",", ":")).encode("utf-8")).hexdigest()
    except (TypeError, ValueError):
        return ""


def _data(record):
    value = record.data if hasattr(record, "data") else record
    return value if isinstance(value, Mapping) else {}


def _bytes(root, relative):
    root = Path(root).resolve()
    path = root / str(relative)
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError("finite Latin path escapes its selected repository")
    return path.read_bytes()


def recognition_from_scopes(scopes):
    return tuple({field: scope[field] for field in
                  ("key", "source_id", "artifact_id", "body_sha256",
                   "artifact_payload_sha256")} for scope in scopes)


def _prior_routes_valid(routes):
    if (not isinstance(routes, dict)
            or set(routes) != {"row_sha256", "artifacts", "readings"}
            or any(not isinstance(routes[field], list) for field in routes)):
        return False
    if any(not _hex_digest(value) for value in routes["row_sha256"]):
        return False
    for field, keys in (
            ("artifacts", {"artifact_record_sha256", "payload_sha256"}),
            ("readings", {"artifact_record_sha256", "passage_record_sha256", "body_sha256"})):
        if any(not isinstance(row, dict) or set(row) != keys
               or any(not _hex_digest(value) for value in row.values())
               for row in routes[field]):
            return False
    return True


@lru_cache(maxsize=1)
def _scopes():
    """Read only the code-pinned canonical authority, never caller policy."""
    if len(ADOPTION_SHA256) != 64:
        return ()
    try:
        payload = _bytes(TRUSTED_ROOT, ADOPTION_PATH)
        if sha256(payload).hexdigest() != ADOPTION_SHA256:
            return ()
        authority = json.loads(payload)
        if (authority.get("schema") != "triptych-finite-latin-authority/v1"
                or authority.get("method_id") != METHOD_ID
                or authority.get("state") != "adopted"
                or not _prior_routes_valid(authority.get("prior_routes"))
                or authority["prior_routes"] != PRIOR_ROUTES):
            return ()
        scopes = authority["scopes"]
        if not isinstance(scopes, list) or not scopes:
            return ()
        keys, passages, artifacts = set(), set(), set()
        for scope in scopes:
            if not isinstance(scope, dict):
                return ()
            key = scope["key"]
            if (not isinstance(key, list) or len(key) != len(KEY_FIELDS)
                    or any(not isinstance(one, str) for one in key[:-1])
                    or isinstance(key[-1], bool) or not isinstance(key[-1], int)
                    or key[-1] < 1 or tuple(key) in keys):
                return ()
            keys.add(tuple(key))
            for field in ("row_sha256", "inherited_row_sha256", "body_sha256",
                          "artifact_payload_sha256"):
                value = scope[field]
                if not _hex_digest(value):
                    return ()
            for field in ("source_id", "artifact_id", "verification_source_id",
                          "public_notice"):
                if not isinstance(scope[field], str) or not scope[field].strip():
                    return ()
            if scope["source_id"] in passages:
                return ()
            passages.add(scope["source_id"])
            artifacts.add(scope["artifact_id"])
            records = scope["record_sha256"]
            if (not isinstance(records, dict)
                    or not {scope["source_id"], scope["artifact_id"],
                            scope["verification_source_id"]}.issubset(records)
                    or any(not isinstance(name, str) or not isinstance(value, str)
                           or len(value) != 64
                           or any(c not in "0123456789abcdef" for c in value)
                           for name, value in records.items())):
                return ()
            for field in ("publication_source_ids", "projected_from"):
                values = scope[field]
                if (not isinstance(values, list) or not values
                        or any(not isinstance(one, str) or not one for one in values)
                        or len(values) != len(set(values))
                        or not set(values).issubset(records)):
                    return ()
            if scope["artifact_id"] not in scope["publication_source_ids"]:
                return ()
            ranges = scope["physical_line_ranges"]
            if (not isinstance(ranges, list) or not ranges
                    or any(not isinstance(one, list) or len(one) != 2
                           or any(isinstance(n, bool) or not isinstance(n, int)
                                  for n in one)
                           or one[0] < 1 or one[1] < one[0] for one in ranges)):
                return ()
        if recognition_from_scopes(scopes) != RECOGNITION:
            return ()
        return tuple(scopes)
    except (OSError, ValueError, TypeError, KeyError):
        return ()


def _scope_for_row(row):
    try:
        key = tuple(row.get(field) for field in KEY_FIELDS)
        return next((one for one in _scopes() if tuple(one["key"]) == key), None)
    except (AttributeError, TypeError):
        return None


def _marker(value):
    return isinstance(value, str) and (METHOD_ID in value or ADOPTION_PATH in value)


def _signatures():
    # The scope-derived portion keeps diagnostic fixtures useful; production
    # scopes must exactly equal the separately compiled recognition pins.
    signatures = list(RECOGNITION)
    for signature in recognition_from_scopes(_scopes()):
        if signature not in signatures:
            signatures.append(signature)
    return signatures


def prior_row_exact(row):
    return (_prior_routes_valid(PRIOR_ROUTES)
            and _digest(row) in PRIOR_ROUTES["row_sha256"])


def _prior_artifact(artifact):
    if not _prior_routes_valid(PRIOR_ROUTES):
        return None
    return next((one for one in PRIOR_ROUTES["artifacts"]
                 if one["artifact_record_sha256"] == _digest(artifact)
                 and one["payload_sha256"] == artifact.get("sha256")), None)


def _prior_reading(passage, artifact, text):
    if not _prior_routes_valid(PRIOR_ROUTES):
        return False
    body_sha = _selected_sha256(text)
    return any(one["artifact_record_sha256"] == _digest(artifact)
               and one["passage_record_sha256"] == _digest(passage)
               and one["body_sha256"] == body_sha
               for one in PRIOR_ROUTES["readings"])


def _selected_sha256(text):
    return sha256((text + "\n").encode("utf-8")).hexdigest() if isinstance(text, str) else None


def claims_row(row):
    if not isinstance(row, Mapping):
        return False
    # A pure quarantine retains only a former hash, with no body or permission.
    if (set(row) == set(KEY_FIELDS) | {
            "body_status", "text_sha256", "provenance_status",
            "publication_status", "publication_basis", "surfaces"}
            and row["body_status"] == "removed"
            and all(isinstance(row[field], str) and not _marker(row[field])
                    for field in KEY_FIELDS[:-1])
            and all(row[field].strip() for field in ("mass", "proper"))
            and isinstance(row["occurrence"], int)
            and not isinstance(row["occurrence"], bool) and row["occurrence"] > 0
            and _hex_digest(row["text_sha256"])
            and all(row[field] == "unresolved" for field in
                    ("provenance_status", "publication_status", "publication_basis"))
            and row["surfaces"] == []):
        return False
    if prior_row_exact(row):
        return False
    if _scope_for_row(row) is not None:
        return True
    ids = row.get("publication_source_ids")
    ids = ids if isinstance(ids, list) else []
    return (any(_marker(row.get(field)) for field in
                ("publication_authority", "publication_evidence", "note"))
            or any(row.get("source_id") == one["source_id"]
                   or row.get("text_sha256") == one["body_sha256"]
                   or one["artifact_id"] in ids for one in _signatures()))


def claims_artifact(artifact):
    if not isinstance(artifact, Mapping):
        return False
    return (_prior_artifact(artifact) is not None
            or _marker(artifact.get("rights_basis"))
            or _marker(artifact.get("notes"))
            or any(artifact.get("id") == one["artifact_id"]
                   or artifact.get("sha256") == one["artifact_payload_sha256"]
                   for one in _signatures()))


def claims_reading(passage, artifact, *, text=_UNSELECTED_TEXT):
    return claims_artifact(artifact) or any(
        _data(passage).get("id") == one["source_id"]
        or _selected_sha256(text) == one["body_sha256"] for one in _signatures())


def row_problems(row):
    if prior_row_exact(row):
        return []
    scope = _scope_for_row(row)
    if scope is None or _digest(row) != scope["row_sha256"]:
        return ["finite Latin assessment requires its exact adopted owner/body/proof/surface tuple"]
    return []


def inherited_row_exact(row):
    scope = _scope_for_row(row)
    return scope is not None and _digest(row) == scope["inherited_row_sha256"]


def authority_problems(root):
    try:
        actual = sha256(_bytes(root, ADOPTION_PATH)).hexdigest()
    except (OSError, ValueError):
        actual = None
    if not _scopes() or actual != ADOPTION_SHA256:
        return ["finite Latin assessment requires exact adopted authority " + ADOPTION_PATH]
    return []


def _record_problems(scope, sources):
    if not isinstance(sources, Mapping):
        return ["finite Latin assessment requires its registered source controllers"]
    problems = []
    for source_id, expected in scope["record_sha256"].items():
        if _digest(_data(sources.get(source_id))) != expected:
            problems.append("finite Latin controller is missing or changed: " + source_id)
    passage = _data(sources.get(scope["source_id"]))
    artifact = _data(sources.get(scope["artifact_id"]))
    if (passage.get("artifact_id") != scope["artifact_id"]
            or passage.get("artifact_sha256") != artifact.get("sha256")
            or passage.get("physical_line_ranges") != scope["physical_line_ranges"]
            or artifact.get("projected_from") != scope["projected_from"]):
        problems.append("finite Latin source/controller/range edges differ from the adopted scope")
    return problems


def source_problems(row, sources, *, effective_calendar=""):
    scope = _scope_for_row(row)
    inherited = (effective_calendar == "roman-pre-1955"
                 and inherited_row_exact(row))
    if (effective_calendar not in {"", "roman-1962"}
            and not inherited):
        return ["finite Latin assessment does not authorize this calendar or inherited permission"]
    problems = [] if inherited else row_problems(row)
    if problems or scope is None:
        return problems or ["finite Latin source is outside the adopted scope"]
    return _record_problems(scope, sources)


def artifact_problems(root, artifact, *, sources=None):
    artifact = _data(artifact)
    prior = _prior_artifact(artifact)
    if prior is not None:
        try:
            actual = sha256(_bytes(root, artifact.get("path"))).hexdigest()
        except (OSError, ValueError):
            actual = None
        return ([] if actual == prior["payload_sha256"] else
                ["prior finite-body route has a missing or changed independently proved carrier"])
    scopes = [one for one in _scopes() if one["artifact_id"] == artifact.get("id")]
    problems = authority_problems(root)
    if (not scopes or any(_digest(artifact) != one["record_sha256"][one["artifact_id"]]
                          for one in scopes)):
        return problems + ["finite Latin carrier is outside the exact adopted artifact scope"]
    try:
        actual = sha256(_bytes(root, artifact.get("path"))).hexdigest()
    except (OSError, ValueError):
        actual = None
    if actual != artifact.get("sha256"):
        problems.append("finite Latin carrier payload is missing or changed")
    for scope in scopes:
        problems.extend(_record_problems(scope, sources))
    return list(dict.fromkeys(problems))


def reading_problems(root, passage, artifact, *, sources=None, text=_UNSELECTED_TEXT):
    passage, artifact = _data(passage), _data(artifact)
    if _prior_artifact(artifact) is not None:
        problems = artifact_problems(root, artifact, sources=sources)
        if text is _UNSELECTED_TEXT:
            if not any(one["artifact_record_sha256"] == _digest(artifact)
                       and one["passage_record_sha256"] == _digest(passage)
                       for one in PRIOR_ROUTES["readings"]):
                problems.append("prior finite-body reading lacks its exact independently proved passage")
        elif not _prior_reading(passage, artifact, text):
            problems.append("prior finite-body reading differs from its independently proved selected body")
        return problems
    scope = next((one for one in _scopes() if one["source_id"] == passage.get("id")), None)
    problems = artifact_problems(root, artifact, sources=sources)
    if (scope is None or artifact.get("id") != scope["artifact_id"]
            or _digest(passage) != scope["record_sha256"][scope["source_id"]]
            or passage.get("physical_line_ranges") != scope["physical_line_ranges"]):
        return problems + ["finite Latin reading requires its exact adopted passage/controller/ranges"]
    if text is not _UNSELECTED_TEXT:
        actual = _selected_sha256(text)
        if actual != scope["body_sha256"]:
            problems.append("finite Latin reading body differs from the adopted whole body")
    return problems


def public_scope(latin):
    latin = _data(latin)
    source_id = _data(latin.get("provenance")).get("source_id")
    scope = next((one for one in _scopes()
                  if one["source_id"] == source_id
                  and one["body_sha256"] == latin.get("text_sha256")), None)
    if scope is None:
        return None
    return {"source_id": scope["source_id"], "artifact_id": scope["artifact_id"],
            "body_sha256": scope["body_sha256"], "notice": scope["public_notice"]}


def cache_fingerprint(root):
    digest = sha256()
    for path in (Path(root).resolve() / ADOPTION_PATH, Path(__file__)):
        try:
            if (path.is_symlink()
                    or path != Path(__file__) and not path.resolve().is_relative_to(Path(root).resolve())):
                raise ValueError("finite Latin cache input escapes its repository")
            value = sha256(path.read_bytes()).hexdigest()
        except (OSError, ValueError):
            value = "missing-or-invalid"
        digest.update((str(path) + "\0" + value + "\0").encode("utf-8"))
    return digest.hexdigest()
