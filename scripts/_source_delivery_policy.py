"""Shared metadata contracts for exact source delivery.

These declarations identify records; they never run a projection command or
retrieve evidence. Source manifests retain their frozen identity and hashes.
"""
from __future__ import annotations

from pathlib import Path, PurePosixPath
import tomllib

import _artifact_store


def external_source_identity(root: Path, relative: str, *, metadata: dict | None = None) -> dict | None:
    """Return an exact declared witness identity without opening its payload.

    This is an ancestry/provenance lookup, never a statement that bytes were
    inspected. A missing undeclared payload has no substitute. The caller must
    resolve exact bytes separately when it needs to read the actual witness.
    """

    if not relative.startswith("src/sources/works/"):
        return None
    entry = _artifact_store.known_external(root, relative)
    if entry is None:
        return None
    parts = PurePosixPath(relative).parts
    if len(parts) < 10 or parts[5] != "editions" or parts[7] != "artifacts":
        raise ValueError(f"external source payload has no canonical artifact owner: {relative}")
    if metadata is None:
        manifest = root.joinpath(*parts[:9], "artifact.toml")
        current = root
        for part in manifest.relative_to(root).parts:
            current = current / part
            if current.is_symlink():
                raise ValueError(f"external source manifest must not traverse symlinks: {relative}")
        metadata = tomllib.loads(manifest.read_text(encoding="utf-8"))
    if metadata.get("record_type") != "artifact" or metadata.get("storage") != "tracked":
        raise ValueError(f"external delivery requires its exact tracked source artifact: {relative}")
    for field, source_field in (("path", "path"), ("sha256", "sha256"),
                                ("bytes", "byte_size"), ("media_type", "media_type")):
        if entry[field] != metadata.get(source_field):
            raise ValueError(f"external delivery does not match artifact {field}: {relative}")
    rights = metadata.get("rights_status")
    if (not isinstance(rights, str)
            or rights not in {"public-domain", "licensed", "permission", "legal-exception", "project-created"}
            or not isinstance(metadata.get("rights_basis"), str) or not metadata["rights_basis"].strip()
            or (rights in {"public-domain", "legal-exception"}
                and (not isinstance(metadata.get("rights_jurisdiction"), str)
                     or not metadata["rights_jurisdiction"].strip()))):
        raise ValueError(f"external source artifact lacks affirmative distribution rights: {relative}")
    media = metadata.get("media_type", "").lower().split(";", 1)[0].strip()
    if (media.startswith("text/") or media in {"application/json", "application/xml"}
            or media.endswith(("+json", "+xml")) or metadata.get("indexable") is True):
        raise ValueError(f"searchable text payload must remain in the checkout: {relative}")
    return {"path": relative, "sha256": entry["sha256"], "byte_size": entry["bytes"]}
