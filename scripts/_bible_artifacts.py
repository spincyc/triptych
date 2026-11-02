"""Select one exact edition-owned reference artifact without rewriting history.

The optional verse_aliases_artifact_id and book_index_artifact_id fields in
EDITIONS are source-index controls, not additions to frozen source manifests.
Absent the role's control,
exactly one legacy table may be selected. Several tables require an exact ID;
directory order, dates and hashes never choose which interpretation is active.
This module deliberately imports neither _projection nor _psalms.
"""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path, PurePosixPath
import re
import stat
import tomllib
from collections.abc import Mapping

from _bible_editions import EDITIONS

ACTIVE_ALIAS_FIELD = "verse_aliases_artifact_id"
ACTIVE_BOOK_FIELD = "book_index_artifact_id"
ROLES = {"verse-aliases": (ACTIVE_ALIAS_FIELD, "verse-aliases.tsv"),
         "book-index": (ACTIVE_BOOK_FIELD, "book-index.tsv")}
ALIAS_NAME = "verse-aliases.tsv"
INDEX_FIELDS = frozenset({"rank", "label", "edition", "source_id", "rights", "publishable",
                         "numbering", "language", "psalter", "psalm_titles", "artifacts",
                         ACTIVE_ALIAS_FIELD, ACTIVE_BOOK_FIELD})
ID = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
HASH = re.compile(r"^[0-9a-f]{64}$")
READABLE_RIGHTS = frozenset({"project-created", "public-domain", "licensed", "permission", "legal-exception"})


class AliasArtifactError(ValueError):
    """The requested reference table has no exact readable artifact owner."""


def _manifest(path: Path) -> dict:
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, ValueError) as error:
        raise AliasArtifactError(f"{path}: cannot read reference source metadata: {error}") from error


def _regular_contained(path: Path, edition_root: Path) -> None:
    try:
        relative = path.relative_to(edition_root)
        # A link must not make another artifact's payload appear locally owned.
        # Hard links are valid exact bytes; nlink is intentionally unrestricted.
        for part in (path, *path.parents):
            if part.is_symlink():
                raise AliasArtifactError(f"{path}: reference artifact path must not contain a symlink")
            if part == edition_root:
                break
        physical_root = edition_root.resolve(strict=True)
        if path.resolve(strict=True) != physical_root.joinpath(*relative.parts):
            raise AliasArtifactError(f"{path}: reference artifact must have exact physical containment")
        if not stat.S_ISREG(path.stat().st_mode):
            raise AliasArtifactError(f"{path}: reference artifact must be a regular file")
    except (OSError, ValueError) as error:
        if isinstance(error, AliasArtifactError):
            raise
        raise AliasArtifactError(f"{path}: reference artifact must be an existing contained regular file") from error


def _owner_artifacts_path(value: object) -> tuple[str, ...] | None:
    """A full canonical owner/work/editions/edition/artifacts registry path."""
    if not isinstance(value, str) or "\\" in value:
        return None
    path = PurePosixPath(value)
    if (path.is_absolute() or path.as_posix() != value or len(path.parts) != 5
            or path.parts[2] != "editions" or path.parts[4] != "artifacts"
            or any(part in {"", ".", ".."} for part in value.split("/"))):
        return None
    return path.parts


def _selection(edition_root: Path, edition_id: str | None, registry: Mapping, field: str) -> str | None:
    if not isinstance(registry, Mapping):
        raise AliasArtifactError("Bible registry must be a mapping")
    declarations = []
    owner = edition_root.parts[-4:]
    actual_path = (*owner, "artifacts") if len(owner) == 4 and owner[2] == "editions" else None
    for name, entry in registry.items():
        if not isinstance(entry, Mapping):
            raise AliasArtifactError(f"Bible registry entry {name!r} must be a mapping")
        unknown = set(entry) - INDEX_FIELDS
        if unknown:
            raise AliasArtifactError(f"Bible registry {name!r}: unknown fields {sorted(unknown)!r}")
        artifacts = _owner_artifacts_path(entry.get("artifacts"))
        matches_path = artifacts is not None and artifacts == actual_path
        controls = any(control in entry for control in (ACTIVE_ALIAS_FIELD, ACTIVE_BOOK_FIELD))
        if artifacts is None and (controls or entry.get("source_id") == edition_id):
            raise AliasArtifactError(f"Bible registry {name!r}: artifacts must be a canonical full owner-relative path")
        if entry.get("source_id") != edition_id and not matches_path:
            continue
        if edition_id is None:
            raise AliasArtifactError(f"{edition_root}: registered edition has no edition.toml identity")
        if entry.get("source_id") != edition_id or not matches_path:
            raise AliasArtifactError(f"{edition_root}: registry path and edition identity disagree")
        for control in (ACTIVE_ALIAS_FIELD, ACTIVE_BOOK_FIELD):
            if control in entry and (not isinstance(entry[control], str) or not entry[control].startswith("artifact.") or not ID.fullmatch(entry[control])):
                raise AliasArtifactError(f"Bible registry {name!r}: {control} must be an exact artifact ID")
        if field not in entry:
            continue
        value = entry[field]
        if not isinstance(value, str) or not value.startswith("artifact.") or not ID.fullmatch(value):
            raise AliasArtifactError(f"Bible registry {name!r}: {field} must be an exact artifact ID")
        declarations.append(value)
    if len(set(declarations)) > 1:
        raise AliasArtifactError(f"{edition_root}: conflicting active reference artifact declarations")
    return declarations[0] if declarations else None


def _validated_payload(path: Path, edition_root: Path, edition_id: str, metadata: dict, name: str) -> Path:
    manifest = path.parent / "artifact.toml"
    _regular_contained(manifest, edition_root)
    if type(metadata.get("schema")) is not int or metadata["schema"] not in (1, 2) or metadata.get("record_type") != "artifact":
        raise AliasArtifactError(f"{manifest}: expected a source-library artifact record")
    artifact_id = metadata.get("id")
    if not isinstance(artifact_id, str) or not artifact_id.startswith("artifact.") or not ID.fullmatch(artifact_id):
        raise AliasArtifactError(f"{manifest}: invalid artifact ID")
    if metadata.get("edition_id") != edition_id:
        raise AliasArtifactError(f"{manifest}: reference artifact belongs to another edition")
    if metadata.get("storage") != "tracked" or metadata.get("rights_status") not in READABLE_RIGHTS or not isinstance(metadata.get("rights_basis"), str) or not metadata["rights_basis"].strip():
        raise AliasArtifactError(f"{manifest}: reference artifact lacks tracked readable rights and basis")
    if metadata.get("rights_status") in {"public-domain", "legal-exception"} and not str(metadata.get("rights_jurisdiction") or "").strip():
        raise AliasArtifactError(f"{manifest}: reference-table rights require a jurisdiction")
    if metadata.get("artifact_type") != "reference-table" or str(metadata.get("media_type") or "").split(";", 1)[0] != "text/tab-separated-values" or metadata.get("indexable") is not True or metadata.get("encoding") != "utf-8":
        raise AliasArtifactError(f"{manifest}: expected an indexable UTF-8 reference table")
    declared = metadata.get("path")
    if not isinstance(declared, str) or "\\" in declared:
        raise AliasArtifactError(f"{manifest}: reference artifact path must be canonical POSIX")
    relative = PurePosixPath(declared)
    if relative.is_absolute() or relative.as_posix() != declared or any(part in {"", ".", ".."} for part in declared.split("/")):
        raise AliasArtifactError(f"{manifest}: reference artifact path must be canonical and relative")
    try:
        source_relative = relative.relative_to("src/sources/works")
    except ValueError as error:
        raise AliasArtifactError(f"{manifest}: reference artifact path must identify its source-library owner") from error
    owner_path = source_relative.parts[:-3]
    if source_relative.parts[-3:] != ("artifacts", path.parent.name, name) or len(owner_path) != 4 or owner_path[2] != "editions" or tuple(edition_root.parts[-4:]) != owner_path:
        raise AliasArtifactError(f"{manifest}: reference artifact path does not identify this exact edition payload")
    _regular_contained(path, edition_root)
    digest = metadata.get("sha256")
    size = metadata.get("byte_size")
    if not isinstance(digest, str) or not HASH.fullmatch(digest) or type(size) is not int or size < 0:
        raise AliasArtifactError(f"{manifest}: reference artifact needs exact SHA-256 and byte size")
    payload = path.read_bytes()
    if len(payload) != size or sha256(payload).hexdigest() != digest:
        raise AliasArtifactError(f"{manifest}: reference artifact bytes differ from the recorded hash or size")
    try:
        payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AliasArtifactError(f"{manifest}: reference artifact is not UTF-8") from error
    return path


def select_reference_artifact(edition_root: Path, role: str, *, registry: Mapping | None = None) -> Path | None:
    """Select the role's active payload, checking its exact metadata and bytes.

    Unregistered bare directories retain the previous unique-file behavior only
    when they carry neither edition.toml nor any reference artifact manifests. This
    bounds compatibility for technical fixtures and external legacy inputs;
    a declared active ID or any source metadata always requires full validation.
    An absent table remains None, so alias_rows and alias_table retain
    their distinct existing absence contracts.
    """
    if role not in ROLES:
        raise AliasArtifactError(f"unsupported reference artifact role {role!r}")
    field, name = ROLES[role]
    edition_root = Path(edition_root)
    # An alias of the edition directory must not make another physical owner
    # appear to have supplied its source record. Bare legacy fixtures obey the
    # same root rule even when they have no manifest to trigger validation.
    if edition_root.is_symlink() or ".." in edition_root.parts:
        raise AliasArtifactError(f"{edition_root}: edition root must be canonical and must not be a symlink")
    registry = EDITIONS if registry is None else registry
    edition_path = edition_root / "edition.toml"
    edition_id = None
    if edition_path.exists() or edition_path.is_symlink():
        _regular_contained(edition_path, edition_root)
        edition = _manifest(edition_path)
        edition_id = edition.get("id")
        if type(edition.get("schema")) is not int or edition["schema"] != 1 or edition.get("record_type") != "edition" or not isinstance(edition_id, str) or not edition_id.startswith("edition.") or not ID.fullmatch(edition_id):
            raise AliasArtifactError(f"{edition_path}: expected an exact source-library edition identity")
    active = _selection(edition_root, edition_id, registry, field)
    found = sorted(edition_root.glob(f"artifacts/{role}-*/{name}"))
    manifests = sorted(edition_root.glob(f"artifacts/{role}-*/artifact.toml"))
    if active is not None:
        matching = []
        for path in manifests:
            _regular_contained(path, edition_root)
            matching.append((path, _manifest(path)))
        matching = [(path, data) for path, data in matching if data.get("id") == active]
        if len(matching) != 1:
            raise AliasArtifactError(f"{edition_root}: active reference artifact {active!r} must identify exactly one local artifact, found {len(matching)}")
        manifest, data = matching[0]
        return _validated_payload(manifest.parent / name, edition_root, edition_id, data, name)
    if max(len(found), len(manifests)) > 1:
        raise AliasArtifactError(f"{edition_root}: {max(len(found), len(manifests))} {role} tables require a declared {field}")
    if not found:
        if manifests:
            if edition_id is None:
                raise AliasArtifactError(f"{edition_root}: reference artifact metadata requires an edition.toml identity")
            _regular_contained(manifests[0], edition_root)
            return _validated_payload(manifests[0].parent / name, edition_root, edition_id, _manifest(manifests[0]), name)
        return None
    path = found[0]
    manifest = path.parent / "artifact.toml"
    if edition_id is None and not any(edition_root.glob("artifacts/*/artifact.toml")):
        _regular_contained(path, edition_root)
        return path
    if edition_id is None:
        raise AliasArtifactError(f"{edition_root}: reference artifact metadata requires an edition.toml identity")
    _regular_contained(manifest, edition_root)
    return _validated_payload(path, edition_root, edition_id, _manifest(manifest), name)


def select_verse_aliases(edition_root: Path, *, registry: Mapping | None = None) -> Path | None:
    """The active exact alias table, without changing historical evidence."""
    return select_reference_artifact(edition_root, "verse-aliases", registry=registry)


def select_book_index(edition_root: Path, *, registry: Mapping | None = None) -> Path | None:
    """The active exact book index under the same source-index contract."""
    return select_reference_artifact(edition_root, "book-index", registry=registry)
