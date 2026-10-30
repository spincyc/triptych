"""Closed qualified Latin assessment for exactly two received Gregem forms.

This is the executable scope of one dated rights adoption, not a general
nonoriginality classifier. Any different owner, body, proof, controller,
surface or authority needs a separately reviewed successor. The project-created
carrier never supplies rights in the underlying third-party Latin.
"""
from hashlib import sha256
import json
from pathlib import Path
import _proper_finite_latin_20261029 as finite_20261029

BASIS = "qualified-nonoriginal-adaptation"
KEY_FIELDS = ("mass", "form", "proper", "course", "cycle", "occurrence")
ADOPTION_PATH = 'workflows/reviews/missal-reader-completion-2026-10-26/gregem-damasus-qualified-rights-adoption.json'
ADOPTION_SHA256 = '652f44afd2c566e48391c7b249137eab32a483ace0346f751059ac8c842fad9c'
RIGHTS_PATH = 'src/sources/inventories/gregem-damasus-qualified-latin-rights-v1.toml'
RIGHTS_SHA256 = 'a7f69af84b9dc2ee3b2f9f53c9b93c436111b1a4855fcdd451c56bd92b9bd0a8'
EDITION_ID = 'edition.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified'
ROW_SHA256 = {('commune-summorum-pontificum', '', 'Collect', '', '', 1): 'd34afb603d2e48f142aceed7f19da53b4f6b90ba91fe82e4886314f5b6cf8183', ('s-damasi-i-papae-confessoris', '', 'Collect', '', '', 1): '38e4e3262ab6a141e1ffb3f27baa4a8bce92b26175461db16c314bb53e98d7c3'}
CONTROLLER_SHA256 = {'artifact.holy-see.acta-apostolicae-sedis.volume-34-1942.ia-issue-4-facsimile-55e40f1e': 'ca990fddd4726db8b0412a4d193c78fd01e2289ba381067509d94be54d719aac', 'passage.holy-see.acta-apostolicae-sedis.volume-34-1942.gregem-common-collect-20261026': 'c13003fd6aa5c06ed66d39dc70ef39e39c78eb16666bed42c6a568a100ef8a30', 'passage.catholic-church.sacramentarium-veronense.feltoe-1896.gregem-whole-and-erratum-20261026': '5ccfbe2ab6e916da25ec38ebd416718533d54366ce932a916e01f225c80df4bb', 'passage.catholic-church.missale-romanum.vatican-typica-1962.gregem-common-collect-20261026': 'a47c53ef1413a6c3f3f03036314ab05cedef7f11067934cd8aab87dad55155ca', 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.common-gregem-collect-e520fa2e': 'd68c142d2836cca70b1c2a34b3ebef505731cd28c1f358ddb344949b02c18e4a', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.common-gregem-collect': 'abe1ec7fbfa093703948a7fd59b684818fc4bcb930820d5250c8ebd601289e93', 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.damasus-gregem-collect-8be4980d': '1faec4f3ad28b3953f4b6793e593aac4eb072304ca5e5b8fb7b4ce1f74a50248', 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.damasus-gregem-collect': '2fff9cb4615bd12decf8af0d568d7eaf10647eed0145ad15165e2d6d4e8b8eaf'}
ARTIFACT_SHA256 = {'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.common-gregem-collect-e520fa2e': 'd68c142d2836cca70b1c2a34b3ebef505731cd28c1f358ddb344949b02c18e4a', 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.damasus-gregem-collect-8be4980d': '1faec4f3ad28b3953f4b6793e593aac4eb072304ca5e5b8fb7b4ce1f74a50248'}
PARENT_FIELDS = {'artifact.catholic-church.sacramentarium-veronense.feltoe-1896.internet-archive-pdf-3b991b13': {'record_type': 'artifact', 'sha256': '3b991b133889bbd4803831455bb4f49de30ecb4d8386534cee1f80f79541967a', 'storage': 'tracked', 'rights_status': 'public-domain'}, 'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf': {'record_type': 'artifact', 'sha256': '648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a', 'storage': 'remote', 'rights_status': 'unresolved'}, 'artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.internet-archive-facsimile-pdf-6cf3c3d0': {'record_type': 'artifact', 'sha256': '6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70', 'storage': 'remote', 'rights_status': 'unresolved'}, 'artifact.holy-see.acta-apostolicae-sedis.volume-34-1942.ia-issue-4-facsimile-55e40f1e': {'record_type': 'artifact', 'sha256': '55e40f1e8b6bde3f45c95e8e08c597ae2dcde76d0cbcb74a4d0a904ba70d5e27', 'storage': 'restricted', 'rights_status': 'unresolved'}}
SCOPES = [{'key': ['commune-summorum-pontificum', '', 'Collect', '', '', 1], 'body_sha256': 'e520fa2e88c8241c62b0ab06171beb2da1532bb39d25b2b7059a6dd80b2f1bd4', 'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.common-gregem-collect', 'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.common-gregem-collect-e520fa2e', 'verification_source_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.gregem-common-collect-20261026', 'publication_source_ids': ['artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.common-gregem-collect-e520fa2e', 'artifact.holy-see.acta-apostolicae-sedis.volume-34-1942.ia-issue-4-facsimile-55e40f1e', 'artifact.catholic-church.sacramentarium-veronense.feltoe-1896.internet-archive-pdf-3b991b13', 'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'], 'projected_from': ['artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf', 'artifact.catholic-church.sacramentarium-veronense.feltoe-1896.internet-archive-pdf-3b991b13', 'artifact.holy-see.acta-apostolicae-sedis.volume-34-1942.ia-issue-4-facsimile-55e40f1e'], 'physical_line_ranges': [[1, 1]]}, {'key': ['s-damasi-i-papae-confessoris', '', 'Collect', '', '', 1], 'body_sha256': '8be4980dfd10f7a70ea1e0674d51271639d7f187b2013678d884a52f51d1bef5', 'source_id': 'passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.damasus-gregem-collect', 'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.damasus-gregem-collect-8be4980d', 'verification_source_id': 'passage.catholic-church.missale-romanum.vatican-typica-1962.sanctoral-damasus-pope-collect', 'publication_source_ids': ['artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-26-gregem-qualified.damasus-gregem-collect-8be4980d', 'artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.internet-archive-facsimile-pdf-6cf3c3d0', 'artifact.catholic-church.sacramentarium-veronense.feltoe-1896.internet-archive-pdf-3b991b13', 'artifact.holy-see.acta-apostolicae-sedis.volume-34-1942.ia-issue-4-facsimile-55e40f1e', 'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'], 'projected_from': ['artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf', 'artifact.catholic-church.sacramentarium-veronense.feltoe-1896.internet-archive-pdf-3b991b13', 'artifact.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945.internet-archive-facsimile-pdf-6cf3c3d0', 'artifact.holy-see.acta-apostolicae-sedis.volume-34-1942.ia-issue-4-facsimile-55e40f1e'], 'physical_line_ranges': [[1, 3]]}]


def _digest(value):
    try:
        encoded = json.dumps(dict(value), sort_keys=True, ensure_ascii=False,
                             separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError):
        return ""
    return sha256(encoded).hexdigest()


def _qualified_row(row):
    source_id = row.get("source_id")
    publication_ids = row.get("publication_source_ids")
    if not isinstance(publication_ids, list):
        publication_ids = []
    return (row.get("publication_basis") == BASIS or
            isinstance(source_id, str) and source_id in {one["source_id"] for one in SCOPES} or
            any(isinstance(one, str) and one in ARTIFACT_SHA256 for one in publication_ids))


def _legacy_row_exact(row, *, inherited=False):
    try:
        key = tuple(row.get(field) for field in KEY_FIELDS)
        expected = (INHERITED_ROW_SHA256 if inherited else ROW_SHA256).get(key)
    except (AttributeError, TypeError):
        return False
    return expected is not None and _digest(row) == expected


def _legacy_artifact_exact(artifact):
    try:
        expected = ARTIFACT_SHA256.get(artifact.get("id"))
    except (AttributeError, TypeError):
        return False
    return expected is not None and _digest(artifact) == expected


def _legacy_passage_exact(passage, artifact):
    try:
        expected = CONTROLLER_SHA256.get(passage.get("id"))
    except (AttributeError, TypeError):
        return False
    return (_legacy_artifact_exact(artifact) and expected is not None
            and _digest(passage) == expected)


def row_problems(row):
    if not _legacy_row_exact(row) and finite_20261029.claims_row(row):
        return finite_20261029.row_problems(row)
    if not _qualified_row(row):
        return []
    key = tuple(row.get(field) for field in KEY_FIELDS)
    try:
        expected = ROW_SHA256.get(key)
    except TypeError:
        expected = None
    if expected is None or _digest(row) != expected:
        return ["qualified Latin basis requires its exact adopted owner/body/proof/surface tuple"]
    return []


def authority_problems(root, *, row=None):
    if (row is not None and not _legacy_row_exact(row)
            and not _legacy_row_exact(row, inherited=True)
            and finite_20261029.claims_row(row)):
        return finite_20261029.authority_problems(root)
    problems = []
    root = Path(root).resolve()
    for relative, expected in ((ADOPTION_PATH, ADOPTION_SHA256),
                               (RIGHTS_PATH, RIGHTS_SHA256)):
        path = root / relative
        try:
            # Data files are never executable authority and cannot escape the
            # selected repository through a symlink.
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError("authority path escapes its repository")
            actual = sha256(path.read_bytes()).hexdigest()
        except (OSError, ValueError):
            actual = None
        if actual != expected:
            problems.append("qualified Latin basis requires exact authority " + relative)
    return problems



# Exact effective copies produced by publication_records when it removes the
# Roman1962 permission during inheritance. These hashes are not accepted by
# row_problems and cannot stand in a direct sidecar or authorize any surface.
INHERITED_ROW_SHA256 = {('commune-summorum-pontificum', '', 'Collect', '', '', 1): 'c56754649a1b63e4071f7534f218e51fbde2605b22e3b7b8a573496213c8227f', ('s-damasi-i-papae-confessoris', '', 'Collect', '', '', 1): 'd387ddfd874cb2e6b87f939e59e919d26ace0b20baf4ca86c68df696195797e7'}


def inherited_row_exact(row):
    if _legacy_row_exact(row, inherited=True):
        return True
    if _legacy_row_exact(row):
        return False
    if finite_20261029.claims_row(row):
        return finite_20261029.inherited_row_exact(row)
    key = tuple(row.get(field) for field in KEY_FIELDS)
    try:
        expected = INHERITED_ROW_SHA256.get(key)
    except TypeError:
        expected = None
    return expected is not None and _digest(row) == expected


def source_problems(row, sources, *, effective_calendar=""):
    if (not _legacy_row_exact(row)
            and not _legacy_row_exact(row, inherited=True)
            and finite_20261029.claims_row(row)):
        return finite_20261029.source_problems(
            row, sources, effective_calendar=effective_calendar)
    if not _qualified_row(row):
        return []
    if effective_calendar == "roman-pre-1955" and inherited_row_exact(row):
        # This is the existing effective permission reset, never an admission.
        # Direct sidecar rows still pass only row_problems above.
        problems = []
    else:
        problems = row_problems(row)
    if problems:
        return problems
    scope = next(one for one in SCOPES if tuple(one["key"]) ==
                 tuple(row.get(field) for field in KEY_FIELDS))
    needed = {scope["source_id"], scope["artifact_id"]}
    needed.add("passage.catholic-church.missale-romanum.vatican-typica-1962.gregem-common-collect-20261026")
    needed.add("passage.holy-see.acta-apostolicae-sedis.volume-34-1942.gregem-common-collect-20261026")
    needed.add("passage.catholic-church.sacramentarium-veronense.feltoe-1896.gregem-whole-and-erratum-20261026")
    for source_id in sorted(needed):
        record = sources.get(source_id)
        if record is None or _digest(record) != CONTROLLER_SHA256[source_id]:
            problems.append("qualified Latin controller is missing or changed: " + source_id)
    for source_id in scope["projected_from"]:
        record = sources.get(source_id) or {}
        if any(record.get(field) != value for field, value in PARENT_FIELDS[source_id].items()):
            problems.append("qualified Latin source identity/rights boundary changed: " + source_id)
    verification = sources.get(scope["verification_source_id"]) or {}
    if verification.get("artifact_id") != "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf":
        problems.append("qualified Latin target passage has a different controller")
    return problems


def artifact_problems(root, artifact, *, sources=None):
    """Keep the normal Sources reader inside the same finite authority."""
    if not _legacy_artifact_exact(artifact) and finite_20261029.claims_artifact(artifact):
        return finite_20261029.artifact_problems(root, artifact, sources=sources)
    if (artifact.get("id") not in ARTIFACT_SHA256 and
            artifact.get("edition_id") != EDITION_ID and
            BASIS not in str(artifact.get("rights_basis") or "")):
        return []
    expected = ARTIFACT_SHA256.get(artifact.get("id"))
    problems = authority_problems(root)
    if expected is None or _digest(artifact) != expected:
        problems.append("qualified Latin carrier is outside the exact adopted artifact scope")
    else:
        root = Path(root).resolve()
        path = root / str(artifact.get("path") or "")
        try:
            if path.is_symlink() or not path.resolve().is_relative_to(root):
                raise ValueError("carrier path escapes its repository")
            actual = sha256(path.read_bytes()).hexdigest()
        except (OSError, ValueError):
            actual = None
        if actual != artifact.get("sha256"):
            problems.append("qualified Latin carrier payload is missing or changed")
        if sources is not None:
            for source_id in artifact.get("projected_from", []):
                record = sources.get(source_id)
                data = record.data if hasattr(record, "data") else record or {}
                expected_parent = PARENT_FIELDS.get(source_id, {})
                if not expected_parent or any(data.get(field) != value
                        for field, value in expected_parent.items()):
                    problems.append("qualified Latin carrier source boundary changed: " + source_id)
    return problems


_UNSELECTED_TEXT = object()


def reading_problems(root, passage, artifact, *, sources=None, text=_UNSELECTED_TEXT):
    """Bind both the selected passage and the actual emitted wording.

    The carrier hash alone cannot license arbitrary inline text or a different
    range under that carrier. Only the two original passage dictionaries and
    their full physical-line bodies are inside this finite assessment.
    """
    arguments = {"sources": sources}
    selected = {}
    if text is not _UNSELECTED_TEXT:
        arguments["text"] = selected["text"] = text
    legacy_passage = _legacy_passage_exact(passage, artifact)
    if (not legacy_passage
            and finite_20261029.claims_reading(passage, artifact, **selected)):
        return finite_20261029.reading_problems(root, passage, artifact, **arguments)
    artifact = artifact or {}
    passage_id = passage.get("id")
    scope = next((one for one in SCOPES if one["source_id"] == passage_id), None)
    qualified_artifact = (artifact.get("id") in ARTIFACT_SHA256 or
                          artifact.get("edition_id") == EDITION_ID or
                          BASIS in str(artifact.get("rights_basis") or ""))
    if scope is None and not qualified_artifact:
        return []
    problems = artifact_problems(root, artifact, sources=sources)
    if (scope is None or artifact.get("id") != scope["artifact_id"] or
            _digest(passage) != CONTROLLER_SHA256[scope["source_id"]]):
        problems.append("qualified Latin reading requires its exact adopted passage/controller/ranges")
        return problems
    if text is not _UNSELECTED_TEXT:
        # Sources returns the exact physical lines without a terminal LF;
        # the adopted source artifact and Proper body include precisely one.
        actual = sha256((text + "\n").encode("utf-8")).hexdigest() if isinstance(text, str) else None
        if actual != scope["body_sha256"]:
            problems.append("qualified Latin reading body differs from the exact adopted whole body")
    return problems


def public_scope(latin):
    """Public qualification for an already validated exact Latin body."""
    provenance = latin.get("provenance") or {}
    scope = next((one for one in SCOPES
                  if one["body_sha256"] == latin.get("text_sha256")
                  and one["source_id"] == provenance.get("source_id")), None)
    if scope is not None:
        return {
            "source_id": scope["source_id"], "artifact_id": scope["artifact_id"],
            "body_sha256": scope["body_sha256"],
            "notice": "Qualified United States editorial assessment under publication policy section 1 priority 6; moderate confidence. The later form is assessed as a nonoriginal adaptation of an older public-domain whole prayer. The theological-redaction originality objection remains. This is not holder permission or an unqualified public-domain claim. Triptych owns only its editorial carrier.",
        }
    return finite_20261029.public_scope(latin)


def cache_fingerprint(root):
    """Inputs outside the source tree must invalidate readable corpus caches."""
    root = Path(root).resolve()
    digest = sha256()
    for path in (root / ADOPTION_PATH, root / RIGHTS_PATH, Path(__file__)):
        try:
            if path.is_symlink() or (path != Path(__file__) and not path.resolve().is_relative_to(root)):
                raise ValueError("qualified cache input escapes its repository")
            value = sha256(path.read_bytes()).hexdigest()
        except (OSError, ValueError):
            value = "missing-or-invalid"
        digest.update((str(path) + "\0" + value + "\0").encode("utf-8"))
    digest.update(finite_20261029.cache_fingerprint(root).encode("ascii"))
    return digest.hexdigest()
