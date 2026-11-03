"""Compact independently proved print products for the private cold cache."""
from __future__ import annotations

import base64
from collections import Counter
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re

from _source_projection_receipt import read_file
from _web_print_common import compact_descriptor, normalize_html, normalize_text, part_statistics

CATALOG_SCHEMA = "triptych-web-print-preparation/v1"
PRODUCT_SCHEMA = "triptych-prepared-print-product/v1"
ASSET_SCHEMA = "triptych-prepared-print-asset/v1"
PREFIX = "print/preparation"
PART_LIMIT = 750_000
DESCRIPTOR_LIMIT = 256_000
PROFILES = frozenset({"flow", "proper", "curriculum", "server-guide", "server-cards", "plates", "bible"})
MIME_EXT = {"image/svg+xml": "svg", "image/png": "png", "image/jpeg": "jpg",
            "font/woff2": "woff2", "text/plain": "txt"}
_SHA = re.compile(r"[a-f0-9]{64}\Z")
_PART_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")


class PreparationError(ValueError):
    """A private product lacks an exact source proof or safe transport shape."""


def need(condition, message):
    if not condition:
        raise PreparationError(message)


def canonical_json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def proof_digest(value):
    result = hashlib.sha256()
    encoder = json.JSONEncoder(ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    for block in encoder.iterencode(value):
        result.update(block.encode())
    return result.hexdigest()


def relative(value):
    need(isinstance(value, str) and value and "\\" not in value and not any(ord(c) < 32 for c in value), "unsafe relative print path")
    path = PurePosixPath(value)
    need(not path.is_absolute() and all(part not in {"", ".", ".."} for part in value.split("/")) and ":" not in path.parts[0], "unsafe relative print path: " + value)
    return value


def source_path(value):
    value = relative(value)
    need(value.startswith(("src/", "scripts/", "tools/", "guidance/", "workflows/", "release/", "web/")) or
         value in {"AGENTS.md", "LICENSE", "THIRD_PARTY.md", "Makefile", "tmt.json", ".gitattributes", ".gitignore"} or
         value.startswith("requirements-"), "print source path is not canonical: " + value)
    return value


def route(value):
    value = relative(value)
    need(value.startswith("print/") and value.endswith(".html") and not any(c in value for c in "?#"), "unsafe print route: " + value)
    return value


class _Safety(HTMLParser):
    def handle_decl(self, declaration):
        raise PreparationError("document declaration in print part")

    def handle_pi(self, instruction):
        raise PreparationError("processing instruction in print part")

    def handle_starttag(self, tag, attrs):
        need(tag not in {"script", "style", "iframe", "object", "embed", "base", "link", "meta", "html", "head", "body"}, "active or document markup in print part: " + tag)
        for key, value in attrs:
            need(not key.startswith("on"), "executable attribute in print part")
            if key in {"href", "src", "xlink:href", "action", "formaction"} and value:
                url = re.sub(r"[\x00-\x20]", "", value)
                need(not re.match(r"(?:javascript|data|file|vbscript):", url, re.I) and not url.startswith("//"), "unsafe print URL")

    handle_startendtag = handle_starttag


def source_paths(product, recipe):
    paths = set(recipe.get("source_paths", ()))
    for field in ("source_paths", "source_inputs"):
        values = product.get(field, ())
        need(isinstance(values, (list, tuple, set, dict)), "invalid print source-path inventory")
        paths.update(values)
    for field in ("selection", "semantic_selection"):
        for item in product.get(field, {}).get("ordered_inputs", ()):
            paths.add(item["path"])
    for item in product.get("publication_binding", ()):
        paths.add(item["path"])
    if recipe.get("entrypoint"):
        paths.add(recipe["entrypoint"])
    return sorted(source_path(value) for value in paths)


def independent_units(product, identifier):
    proof = product.get("coverage_result")
    need(isinstance(proof, dict) and proof.get("status") == "pass", "independent print coverage has not passed")
    need(proof.get("complete", True) is True, "independent print coverage is incomplete")
    full = product.get("expected_units")
    need(isinstance(full, list) and full, "independent print source selection is absent")
    if "expected_units" in proof:
        need(proof.get("output_id") == identifier and proof.get("source_digest") == product.get("source_digest") and
             proof.get("selection_digest") == product.get("selection_digest") and proof["expected_units"] == full,
             "independent print proof belongs to another output or selection")
        units = full
    else:
        need(proof.get("complete") is True and not proof.get("failures") and not proof.get("missing_units"), "independent semantic coverage is incomplete")
        need(isinstance(proof.get("ledger_digest"), str) and _SHA.fullmatch(proof["ledger_digest"]), "independent semantic ledger is not pinned")
        matched = proof.get("matched_units")
        need(isinstance(matched, list) and Counter(row["id"] for row in matched) == Counter(row["id"] for row in full), "semantic proof does not bind the complete source selection")
        ledger = product.get("expected_ledger", product.get("semantic_ledger"))
        need(isinstance(ledger, dict) and ledger.get("units") == full and ledger.get("ledger_digest") == proof["ledger_digest"] and
             ledger.get("macro_state_digest") == proof.get("macro_state_digest"), "semantic proof belongs to another canonical ledger")
        # The owner's ledger uses the standard sorted JSON encoding. Hash it
        # incrementally; the full canonical audit can exceed 100 MB.
        ledger_pin = hashlib.sha256()
        for block in json.JSONEncoder(sort_keys=True).iterencode({key: value for key, value in ledger.items() if key != "ledger_digest"}):
            ledger_pin.update(block.encode())
        need(ledger_pin.hexdigest() == proof["ledger_digest"] and ledger.get("selection_digest") == product["selection_digest"], "canonical semantic ledger or selection changed after source coverage")
        units = product.get("print_unit_expectations")
        need(isinstance(units, list) and units and [row["id"] for row in units] == product.get("expected_print_units"), "independent DOM-ordered print expectations are absent or inconsistent")
        from _web_print_publication import unit_expectations
        need(unit_expectations(ledger, product["expected_print_units"]) == units, "print occurrence provenance differs from the independent source ledger")
    ids = [unit.get("id") for unit in units]
    need(all(isinstance(uid, str) and uid for uid in ids) and len(set(ids)) == len(ids), "independent print unit IDs are missing or duplicated")
    need(all(unit.get("source") and unit.get("occurrence") for unit in units), "independent print provenance is incomplete")
    for unit in units:
        need(not Path(str(unit["source"])).is_absolute() and "\\" not in str(unit["source"]), "physical path in print unit provenance")
    if product.get("expected_print_units") is not None:
        need(ids == product["expected_print_units"], "independent print occurrence orders disagree")
    return units, proof


def _typed_part(fragment, part_id, identifier, source_digest, profile):
    need(isinstance(fragment, str) and fragment.strip(), "empty print body")
    fragment = normalize_html(fragment, profile=profile)
    safety = _Safety(convert_charrefs=True)
    safety.feed(fragment)
    safety.close()
    # Existing source-owned wrappers retain their complete attributes and body.
    opening = re.match(r"\s*<([a-z][a-z0-9-]*)\b[^>]*>", fragment)
    attrs = {}
    if opening:
        class First(HTMLParser):
            def handle_starttag(self, tag, pairs):
                if not self.attrs:
                    self.attrs = dict(pairs)
        parser = First()
        parser.attrs = {}
        parser.feed(opening.group())
        attrs = parser.attrs
    if "data-print-part" in attrs:
        need(attrs["data-print-part"] == part_id and attrs.get("data-print-document") == identifier and
             attrs.get("data-print-source") == source_digest, "source print wrapper belongs to another part or document")
    else:
        fragment = '<section data-print-part="' + html.escape(part_id, quote=True) + '" data-print-document="' + html.escape(identifier, quote=True) + '" data-print-source="' + source_digest + '">' + fragment + '</section>'
    need(len(fragment.encode()) < PART_LIMIT, "print part exceeds the bounded HTML budget")
    # No selector is supplied: all bytes must form exactly one complete part.
    return fragment, part_statistics(fragment)


def _owner_body(part):
    """Check the final bytes pinned after the owner's independent audit."""
    fragment = part.get("html")
    need(isinstance(fragment, str) and fragment.strip(), "empty print body")
    pins = [part[field] for field in ("html_sha256", "sha256") if field in part]
    need("html_sha256" in part and all(isinstance(pin, str) and _SHA.fullmatch(pin) and digest(fragment) == pin for pin in pins), "print part body differs from its required owner pin")
    if "bytes" in part:
        need(part["bytes"] == len(fragment.encode()), "print part byte size differs from its owner pin")
    # Generic balanced parts may contain several top-level source blocks;
    # typed owner parts already have a root. Read text without adding roots.
    class Text(HTMLParser):
        def handle_data(self, value):
            self.words.append(value)
    text = Text(convert_charrefs=True)
    text.words = []
    text.feed(fragment)
    text.close()
    text_sha = digest(normalize_text("".join(text.words)))
    fields = ("text_sha256", "structure_sha256", "expected_ids", "units", "counts")
    statistics = part_statistics(fragment) if any(field in part for field in fields) else {}
    for field in ("text_sha256", "structure_sha256", "expected_ids", "units"):
        if field in part:
            need(part[field] == statistics[field], "print part " + field + " differs from its owner pin")
    if "counts" in part:
        need(isinstance(part["counts"], dict), "invalid owner semantic counts")
        counted = part_statistics(fragment, selectors=list(part["counts"]))["counts"]
        need(counted == part["counts"], "print part counts differ from their owner pin")
    return text_sha


def _response_geometry(product, parts):
    if product["print_type"] != "curriculum":
        return None
    expected = product.get("expected_response_geometry")
    proof = product.get("response_geometry_coverage")
    need(isinstance(expected, list) and isinstance(proof, dict) and proof.get("status") == "pass" and proof.get("complete") is True,
         "curriculum response geometry lacks complete independent source coverage")
    for event in expected:
        need(isinstance(event, dict), "invalid canonical response geometry event")
        reference = event.get("source_ref", {})
        need(isinstance(reference, dict), "invalid canonical response source reference")
        source_path(reference.get("path"))
        need(reference.get("coordinate_space") == "canonical-expansion" and type(reference.get("occurrence")) is int and reference["occurrence"] > 0,
             "curriculum response geometry lacks canonical occurrence provenance")
        need(isinstance(event.get("source_payload_digest"), str) and _SHA.fullmatch(event["source_payload_digest"]), "curriculum response source payload is not pinned")
        definitions = event.get("definition_refs")
        need(isinstance(definitions, list), "invalid canonical response definition inventory")
        for definition in definitions:
            need(isinstance(definition, dict), "invalid canonical response definition reference")
            source_path(definition.get("path"))
            need(isinstance(definition.get("sha256"), str) and _SHA.fullmatch(definition["sha256"]), "curriculum response definition is not pinned")
    from _web_print_curriculum.response_geometry import check
    actual = check(expected, "".join(part["html"] for part in parts))
    need(actual == proof, "curriculum response geometry proof differs from its source plan or final parts")
    return actual


def prepare_product(product, recipe, *, asset_ids=None):
    identifier = recipe["id"]
    need(product.get("id", product.get("output_id")) == identifier, "print product namespace differs from its declared recipe")
    if product.get("id") is not None:
        need(product["id"] == identifier, "print product identity differs from its declared recipe")
    profile = product.get("print_type")
    need(profile in PROFILES, "unknown print profile: " + str(profile))
    for field in ("source_digest", "selection_digest"):
        need(isinstance(product.get(field), str) and _SHA.fullmatch(product[field]), "invalid print " + field)
    units, proof = independent_units(product, identifier)
    root_route = route(product.get("root_route") or "print/" + identifier.removeprefix("publication:") + ".html")
    raw_parts = product.get("parts")
    need(isinstance(raw_parts, list) and raw_parts, "print output has no parts")
    parts, measured, seen = [], [], set()
    for index, part in enumerate(raw_parts):
        part_id = part.get("id")
        need(isinstance(part_id, str) and _PART_ID.fullmatch(part_id) and part_id not in seen, "unsafe or duplicate print part ID")
        seen.add(part_id)
        original = _owner_body(part)
        fragment, statistics = _typed_part(part.get("html"), part_id, identifier, product["source_digest"], profile)
        need(statistics["text_sha256"] == original, "typed print normalization changed source words")
        if part.get("expected_print_units") is not None:
            need(statistics["units"] == part["expected_print_units"], "part differs from its source-bound print occurrences")
        raw_href = part.get("href")
        if raw_href:
            raw_href = relative(raw_href)
            target = route(raw_href if raw_href.startswith("print/") else str(PurePosixPath(root_route).parent / raw_href))
            location = {"href": target}
        elif part.get("selector") or index == 0:
            target = root_route
            location = {"selector": '[data-print-part="' + part_id + '"]'}
        else:
            target = route(root_route.removesuffix(".html") + "/parts/" + part_id + ".html")
            location = {"href": target}
        parts.append({"id": part_id, "html": fragment, "route": target, **location})
        measured.append({"id": part_id, **location, **statistics})
    need([uid for part in measured for uid in part["units"]] == [unit["id"] for unit in units], "print parts differ from independent ordered source units")
    geometry = _response_geometry(product, parts)
    audit = proof_digest({"coverage": proof, "print_unit_expectations": units, "response_geometry_coverage": geometry})
    descriptor = {"schema": "triptych-web-print-document/v1", "id": identifier,
                  "title": product.get("title") or recipe.get("title") or identifier,
                  "language": product.get("language", "en"), "print_type": profile,
                  "source_digest": product["source_digest"], "selection_digest": product["selection_digest"],
                  "expected_units": units, "parts": measured,
                  "coverage_result": {"status": proof["status"], "output_id": identifier,
                                      "source_digest": product["source_digest"], "selection_digest": product["selection_digest"],
                                      "expected_units": units, "audit_sha256": audit},
                  "assets": [{"id": row["id"], "href": row.get("href", row.get("src")),
                              "sha256": row["sha256"], "mime": row.get("mime", row.get("media_type")),
                              "role": row.get("role", "diagram")} for row in product.get("assets", ())]}
    for field in ("edition", "revision", "page_format", "availability"):
        if field in product:
            descriptor[field] = product[field]
    compact = compact_descriptor(descriptor)
    compact.pop("fonts", None)
    compact.pop("style_sha256", None)
    need(len(canonical_json(compact)) < DESCRIPTOR_LIMIT, "compact print descriptor exceeds budget")
    metadata = {key: recipe[key] for key in ("provider", "document", "kind", "entrypoint") if recipe.get(key) is not None}
    metadata["output"] = recipe.get("document", identifier.partition(":")[2])
    metadata["role"] = recipe.get("edition", "main")
    if product.get("source_id"):
        metadata["source_id"] = product["source_id"]
    if geometry is not None:
        metadata["response_geometry_coverage"] = geometry
    return {"schema": PRODUCT_SCHEMA, "descriptor": compact, "root_route": root_route,
            "parts": parts, "source_paths": source_paths(product, recipe), "metadata": metadata,
            "asset_ids": dict(sorted((asset_ids or {}).items()))}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    need(not path.is_symlink(), "private print output is a symlink")
    path.write_bytes(canonical_json(value) + b"\n")


class AssetPool:
    """Write one private payload per exact byte hash; keep no binary body cache."""
    def __init__(self, root, destination):
        self.root, self.destination = Path(root), Path(destination)
        self.records = {}
        self.source_paths = set()

    def add(self, record, *, role=None, canonical_path=None):
        media = record.get("mime", record.get("media_type"))
        need(media in MIME_EXT, "unsupported print asset media type")
        sha = record.get("sha256")
        need(isinstance(sha, str) and _SHA.fullmatch(sha), "invalid print asset hash")
        canonical_path = canonical_path or record.get("canonical_path")
        if canonical_path is None and media in {"image/png", "image/jpeg", "image/svg+xml"}:
            canonical_path = record.get("source")
        body = record.get("body")
        if canonical_path:
            canonical_path = source_path(canonical_path)
            need(canonical_path.startswith("src/"), "print asset source is outside canonical source tree")
            actual = read_file(self.root, canonical_path)
            if body is not None:
                need(body == actual, "print asset body differs from its canonical file")
            body = actual
            self.source_paths.add(canonical_path)
            # Raster artwork may reuse the canonical file. SVG payloads are
            # embedded, so the hot reader never needs an SVG generation cache.
            if media == "image/svg+xml":
                canonical_path = None
        elif body is None:
            existing = self.records.get(sha)
            need(existing is not None, "print asset has no verified body or canonical file")
            body_size = existing["asset"]["bytes"]
        if body is not None:
            need(isinstance(body, bytes) and digest(body) == sha, "print asset body hash mismatch")
            body_size = len(body)
        need(record.get("bytes", body_size) == body_size and type(body_size) is int and body_size > 0, "print asset byte size mismatch")
        role = role or record.get("role") or ("font" if media == "font/woff2" else "font-license" if media == "text/plain" else "diagram" if media == "image/svg+xml" else "illustration")
        asset = {"id": sha, "src": "print-assets/" + sha + "." + MIME_EXT[media],
                 "sha256": sha, "bytes": body_size, "mime": media, "role": role}
        for field in ("family", "weight", "style", "unicode_range", "license", "spdx"):
            if field in record:
                need(isinstance(record[field], (str, int)), "private asset metadata must not contain raw source records")
                asset[field] = record[field]
        previous = self.records.get(sha)
        if previous is not None:
            need(previous["asset"] == asset, "identical print asset bytes have conflicting metadata")
            return sha
        envelope = {"schema": ASSET_SCHEMA, "asset": asset}
        if canonical_path:
            envelope["canonical_path"] = canonical_path
        else:
            need(body is not None, "first print asset registration has no bytes")
            envelope["body_base64"] = base64.b64encode(body).decode("ascii")
        write_json(self.destination / "assets" / (sha + ".json"), envelope)
        self.records[sha] = {"asset": asset, "path": "assets/" + sha + ".json"}
        return sha

    def rows(self):
        return [{"id": sha, "path": self.records[sha]["path"]} for sha in sorted(self.records)]


def read_index(data_root):
    """Read the private index supplied by a caller's held product snapshot."""
    value = json.loads(read_file(Path(data_root), PREFIX + "/catalog.json"))
    need(isinstance(value, dict) and set(value) == {"schema", "products", "assets", "source_paths"} and value["schema"] == CATALOG_SCHEMA, "invalid private print catalogue")
    for field, directory in (("products", "products/"), ("assets", "assets/")):
        need(isinstance(value[field], list), "invalid private print catalogue table")
        seen = set()
        for row in value[field]:
            need(isinstance(row, dict) and set(row) == {"id", "path"} and isinstance(row["id"], str) and row["id"] not in seen, "duplicate or invalid private print catalogue row")
            relative(row["path"])
            need(row["path"].startswith(directory) and row["path"].endswith(".json"), "private print member is outside its owned directory")
            seen.add(row["id"])
    need(isinstance(value["source_paths"], list) and value["source_paths"] == sorted(set(value["source_paths"])), "invalid private print source membership")
    for path in value["source_paths"]:
        source_path(path)
    return value


def read_product(data_root, row):
    path = relative(row["path"])
    need(path.startswith("products/") and re.fullmatch(r"products/[a-f0-9]{64}\.json", path), "unsafe private print product member")
    body = read_file(Path(data_root), PREFIX + "/" + path)
    value = json.loads(body)
    need(digest(canonical_json(value)) == PurePosixPath(path).stem, "private print product filename differs from its contents")
    need(isinstance(value, dict) and set(value) == {"schema", "descriptor", "root_route", "parts", "source_paths", "metadata", "asset_ids"} and value["schema"] == PRODUCT_SCHEMA and value["descriptor"]["id"] == row["id"], "invalid private print product identity")
    route(value["root_route"])
    need("fonts" not in value["descriptor"] and "style_sha256" not in value["descriptor"], "private print data contains final publication styling")
    need(isinstance(value["asset_ids"], dict) and all(isinstance(key, str) and _SHA.fullmatch(sha) for key, sha in value["asset_ids"].items()), "invalid per-product print asset map")
    for path in value["source_paths"]:
        source_path(path)
    for part in value["parts"]:
        route(part["route"])
        need(isinstance(part.get("html"), str), "private print part has no complete HTML body")
    return value


def read_asset(data_root, row):
    path = relative(row["path"])
    need(isinstance(row["id"], str) and _SHA.fullmatch(row["id"]) and path == "assets/" + row["id"] + ".json", "unsafe private print asset member")
    value = json.loads(read_file(Path(data_root), PREFIX + "/" + path))
    need(isinstance(value, dict) and set(value) in ({"schema", "asset", "body_base64"}, {"schema", "asset", "canonical_path"}) and value["schema"] == ASSET_SCHEMA, "invalid private print asset envelope")
    asset = value["asset"]
    need(asset.get("id") == row["id"] == asset.get("sha256") and asset.get("mime") in MIME_EXT and
         asset.get("src") == "print-assets/" + row["id"] + "." + MIME_EXT[asset["mime"]], "invalid private print asset identity")
    if "canonical_path" in value:
        source_path(value["canonical_path"])
    else:
        try:
            body = base64.b64decode(value["body_base64"], validate=True)
        except (ValueError, TypeError) as error:
            raise PreparationError("invalid private print asset body") from error
        need(digest(body) == row["id"] and len(body) == asset.get("bytes"), "private print asset body differs from its pin")
    return value
