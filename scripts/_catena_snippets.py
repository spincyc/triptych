"""Reviewed Scripture links into existing Catena text; never citation mining.

The sidecar stores offsets, not a second transcription. Source-library evidence
states and the parent fragment's natural extent remain unchanged. A text hash
pins every boundary; no search or fuzzy match repairs a stale review.
"""
from __future__ import annotations

from datetime import date
from collections import Counter
import hashlib
from pathlib import Path
import re

PATH = Path("src/sources/commentary/passage-snippets.yaml")
SCHEMA = "triptych-catena-passage-snippets/v1"
SNIPPET_FIELDS = {"id", "start", "end", "extent", "locator", "basis"}


def reviewed(root, sources, edges, *, passage_ids=None):
    """Return validated code-point records and all errors, without partial use."""
    import _catena

    path = root / PATH
    if not path.exists():
        return {}, []
    try:
        document = _catena._load_yaml(path)
    except (OSError, ValueError, _catena._yaml().YAMLError) as error:
        return {}, [f"{PATH}: cannot read snippet review: {error}"]
    errors = []
    fields = {"schema", "numbering", "offset_unit", "reviewed_on", "passages"}
    if not isinstance(document, dict) or set(document) != fields:
        return {}, [f"{PATH}: needs exactly {', '.join(sorted(fields))}"]
    if document["schema"] != SCHEMA or document["numbering"] != "vulgate":
        errors.append(f"{PATH}: unsupported schema or numbering")
    if document["offset_unit"] != "unicode-code-point":
        errors.append(f"{PATH}: offsets must count unicode-code-point")
    try:
        date.fromisoformat(document["reviewed_on"])
    except (TypeError, ValueError):
        errors.append(f"{PATH}: reviewed_on must be an ISO date string")
    if not isinstance(document["passages"], list):
        return {}, errors + [f"{PATH}: passages must be a list"]
    parents = {row.get("passage_id"): row for row in edges.get("fragments", [])
               if isinstance(row, dict)}
    result, seen = {}, set()
    ceilings = _catena._chapter_ceiling(root)
    for ordinal, row in enumerate(document["passages"], 1):
        label = f"{PATH}: passages[{ordinal}]"
        if not isinstance(row, dict) or set(row) != {"passage_id", "text_sha256", "snippets"}:
            errors.append(f"{label}: needs exactly passage_id, text_sha256, snippets")
            continue
        identifier = row["passage_id"]
        if not isinstance(identifier, str) or identifier not in parents:
            errors.append(f"{label}: parent is not an admitted fragment")
            continue
        label = f"{PATH}: {identifier}"
        if identifier in seen:
            errors.append(f"{label}: duplicate parent")
        seen.add(identifier)
        # Interactive reads validate the selected parents' exact text and
        # boundaries. The full producer still validates every parent by default.
        if passage_ids is not None and identifier not in passage_ids:
            continue
        passage = sources.passages.get(identifier, {})
        text = passage.get("text")
        if not isinstance(text, str) or not text.strip():
            errors.append(f"{label}: parent has no explicit text")
            continue
        if not {"inspected", "verified"}.intersection(passage.get("states", [])):
            errors.append(f"{label}: parent text has not been inspected")
        if row["text_sha256"] != hashlib.sha256(text.encode("utf-8")).hexdigest():
            errors.append(f"{label}: stale parent text hash; review the boundaries again")
        parent = _catena._extent(parents[identifier].get("extent"))
        if parent is None:
            errors.append(f"{label}: parent has no valid canonical extent")
            continue
        snippets = row["snippets"]
        if not isinstance(snippets, list) or not snippets:
            errors.append(f"{label}: snippets must be a nonempty list")
            continue
        ids, prior_end = set(), 0
        for number, snippet in enumerate(snippets, 1):
            at = f"{label}: snippets[{number}]"
            if not isinstance(snippet, dict) or set(snippet) != SNIPPET_FIELDS:
                errors.append(f"{at}: needs exactly {', '.join(sorted(SNIPPET_FIELDS))}")
                continue
            slug = snippet["id"]
            if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                errors.append(f"{at}: id must be a lowercase kebab-case identifier")
            elif slug in ids:
                errors.append(f"{at}: duplicate snippet id")
            else:
                ids.add(slug)
            for field in ("locator", "basis"):
                if not isinstance(snippet[field], str) or not snippet[field].strip():
                    errors.append(f"{at}: {field} must be nonempty text")
            start, end = snippet["start"], snippet["end"]
            if (type(start) is not int or type(end) is not int
                    or not 0 <= start < end <= len(text)):
                errors.append(f"{at}: offsets must bound a nonempty parent text slice")
            else:
                if start < prior_end:
                    errors.append(f"{at}: snippets must follow source order without overlap")
                prior_end = end
                if not text[start:end].strip():
                    errors.append(f"{at}: selected text is blank")
                if ((start and not text[start - 1].isspace())
                        or (end < len(text) and not text[end].isspace())):
                    errors.append(f"{at}: boundary cuts through a source word")
            raw_extent = snippet["extent"]
            if (not isinstance(raw_extent, dict)
                    or set(raw_extent) != _catena.EXTENT_FIELDS
                    or not isinstance(raw_extent.get("token"), str)
                    or any(type(raw_extent.get(key)) is not int or raw_extent[key] < 1
                           for key in _catena.EXTENT_FIELDS - {"token"})):
                errors.append(f"{at}: canonical extent needs a token and positive integer endpoints")
                continue
            extent = _catena._extent(raw_extent)
            if extent is None:
                errors.append(f"{at}: invalid canonical extent")
                continue
            errors.extend(_catena._extent_errors(root, at, extent, ceilings))
            if (extent.token != parent.token
                    or (extent.first_chapter, extent.first_verse)
                    < (parent.first_chapter, parent.first_verse)
                    or (extent.last_chapter, extent.last_verse)
                    > (parent.last_chapter, parent.last_verse)):
                errors.append(f"{at}: snippet extends beyond its parent Scripture extent")
        result[identifier] = snippets
    return ({} if errors else result), sorted(errors)


def project(text, snippets):
    """Translate exact authored offsets into JavaScript's UTF-16 indexing."""
    return [{**row,
             "start": len(text[:row["start"]].encode("utf-16-le")) // 2,
             "end": len(text[:row["end"]].encode("utf-16-le")) // 2}
            for row in snippets]


def source_record(passage, artifact):
    """The bounded parent witness, independent of its intellectual author."""
    record = {"edition_id": passage.get("edition_id", ""),
              "artifact_id": artifact.get("id", ""),
              "artifact_sha256": passage.get("artifact_sha256", "")}
    for field in ("segment_id", "physical_line_ranges", "artifact_page_ranges"):
        if passage.get(field):
            record[field] = passage[field]
    return record


def audit(root, *, minimum_words=1000):
    """Enumerate every admitted parent and the remaining long-text worklist.

    The word threshold is a reading-length heuristic, not an evidence state or
    a claim that shorter fragments have complete verse-level correspondence.
    """
    import _catena
    import _catena_scope

    sources = _catena.load_sources(root)
    edges = _catena.load_edges(root)
    snippets, errors = reviewed(root, sources, edges)
    scope = _catena_scope.Scope(root, works=sources.works)
    rows = []
    for edge in edges.get("fragments", []):
        if not scope.allowed_work(edge["work_id"]):
            continue
        identifier = edge["passage_id"]
        passage = sources.passages.get(identifier, {})
        artifact = _catena.controlling_artifact(sources, passage) or {}
        edition = sources.editions.get(passage.get("edition_id"), {})
        text = passage.get("text", "")
        rows.append({"passage_id": identifier, "work_id": edge["work_id"],
                     "language": edition.get("language", ""), "extent": edge["extent"],
                     "words": len(text.split()), "snippet_count": len(snippets.get(identifier, [])),
                     "source_record": source_record(passage, artifact)})
    rows.sort(key=lambda row: (-row["words"], row["passage_id"]))
    long_rows = [row for row in rows if row["words"] >= minimum_words]
    pending = [row["passage_id"] for row in long_rows if not row["snippet_count"]]
    return {"schema": "triptych-catena-linkage-audit/v1", "numbering": "vulgate",
            "minimum_words": minimum_words,
            "counted": {"fragments": len(rows), "snippets": sum(row["snippet_count"] for row in rows),
                        "parents_with_snippets": sum(bool(row["snippet_count"]) for row in rows),
                        "large_parents": len(long_rows),
                        "large_parents_without_snippets": len(pending),
                        "fragments_by_language": dict(sorted(Counter(row["language"] for row in rows).items())),
                        "large_parents_by_language": dict(sorted(Counter(row["language"] for row in long_rows).items()))},
            "large_parents_without_snippets": pending,
            "fragments": rows, "errors": errors}
