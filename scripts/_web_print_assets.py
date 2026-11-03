"""Source-bound browser-print render products and redistributable font software.

Normal lookup is offline and runs no renderer. The compact registry authenticates
current canonical inputs; the separate delivery index only locates exact bytes.
These generated products confer no source, editorial, rights or visual approval.
Run ``python scripts/_web_print_assets.py hydrate --help`` for explicit bootstrap.
"""
from __future__ import annotations

import argparse
import base64
import copy
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET

import _artifact_store as transport

INDEX_PATH = "src/common/browser-print-assets.json"
DELIVERY_PATH = "src/common/browser-print-assets-delivery.json"
FONT_ROOT = "src/common/browser-print-fonts"
SCHEMA = "triptych-browser-print-assets/v1"
DELIVERY_SCHEMA = "triptych-browser-print-asset-delivery/v1"
PREFIX = "web-print-assets/"
KINDS = ("project-render-product", "font-software")
SERVER_OWNER = "src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/"
_HASH = re.compile(r"[0-9a-f]{64}\Z")
_SVG_NS = "http://www.w3.org/2000/svg"


class AssetError(ValueError):
    """A registry, current source closure or immutable asset failed validation."""


def digest(data: bytes | str) -> str:
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def canonical_json(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _require(condition, message):
    if not condition:
        raise AssetError(message)


def _hash(value):
    _require(isinstance(value, str) and _HASH.fullmatch(value), "invalid asset SHA-256")


def _source_path(value: str, *, provider: str | None = None):
    transport._relative(value)
    _require(value.startswith("src/") and len(value.split("/")) >= 3,
             "asset source must belong to canonical src owners")
    _require(value.endswith((".tex", ".png")), "unsupported asset source type")
    if provider is not None:
        _require(value.startswith((f"src/{provider}/", "src/common/")), "asset source escapes provider/common owner")


def _closure(rows, *, provider=None):
    _require(isinstance(rows, dict) and bool(rows), "empty or invalid asset source closure")
    for path, pin in rows.items():
        _source_path(path, provider=provider)
        _hash(pin)


def _verify_sources(root: Path, rows: dict):
    for relative, pin in rows.items():
        path = transport._path(root, relative)
        _require(path.is_file() and digest(path.read_bytes()) == pin,
                 "stale browser-print source closure: " + relative)


def _verify_definitions(root, server):
    sources = {}
    for pin, definition in server["definitions"].items():
        path = definition["source"]
        if path not in sources:
            sources[path] = transport._path(root, path).read_text(encoding="utf-8")
        source = sources[path]
        start, end = definition["start"], definition["end"]
        _require(end <= len(source) and digest(source[start:end]) == pin and source[:start].count("\n") + 1 == definition["line"], "stale macro source span: " + path)


def _json_file(root: Path, relative: str):
    try:
        path = transport._path(root, relative)
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=transport._unique_keys)
    except (OSError, UnicodeError, ValueError) as error:
        raise AssetError(f"cannot read {relative}: {error}") from error


def _validate(data, delivery):
    _require(isinstance(data, dict) and set(data) == {
        "schema", "registry_digest", "provenance", "payloads", "server", "generic", "fonts"}, "invalid browser-print asset registry fields")
    _require(data["schema"] == SCHEMA, "unsupported browser-print asset registry")
    _hash(data["registry_digest"])
    _require(data["registry_digest"] == digest(canonical_json({k: v for k, v in data.items() if k != "registry_digest"})), "browser-print registry digest mismatch")
    transport.validate_delivery_index(delivery, schema=DELIVERY_SCHEMA, kinds=KINDS, path_prefix=PREFIX)
    entries = {row["path"]: row for row in delivery["artifacts"]}
    payloads = data["payloads"]
    _require(isinstance(payloads, dict) and payloads.keys() == entries.keys(), "registry and delivery payloads differ")
    for path, row in payloads.items():
        _require(isinstance(row, dict) and set(row) == {"sha256", "bytes", "media_type", "kind"}, "invalid browser-print payload record")
        _hash(row["sha256"])
        extension = "svg" if row["media_type"] == "image/svg+xml" else "woff2" if row["media_type"] == "font/woff2" else None
        _require(extension is not None and path == f"{PREFIX}{row['sha256']}.{extension}", "noncanonical typed browser-print payload path")
        _require(row["kind"] == ("font-software" if extension == "woff2" else "project-render-product"), "wrong browser-print asset kind")
        _require(type(row["bytes"]) is int and 0 < row["bytes"] <= transport.MAX_ARCHIVE_BYTES, "invalid browser-print payload size")
        _require(all(entries[path][k] == v for k, v in row.items()), "registry/delivery asset identity mismatch")
    used = set()
    server = data["server"]
    _require(isinstance(server, dict) and set(server) == {"origin", "source_inputs", "definitions", "variants", "entries"}, "invalid server asset registry")
    _closure(server["source_inputs"])
    _require(all(p == "src/common/preamble.tex" or p.startswith(SERVER_OWNER) for p in server["source_inputs"]), "server asset source escapes owner")
    _require(set(server["variants"]) == {"child", "trainer", "sung"}, "unsupported server variants")
    for pin, definition in server["definitions"].items():
        _hash(pin)
        _require(set(definition) == {"source", "line", "start", "end", "sha256"} and definition["sha256"] == pin, "invalid server macro definition metadata")
        _require(definition["source"] in server["source_inputs"] and definition["source"].endswith(".tex"), "unbound server macro source")
        _require(all(type(definition[k]) is int for k in ("line", "start", "end")) and definition["line"] > 0 and 0 <= definition["start"] < definition["end"], "invalid server macro source span")
    for key, row in server["entries"].items():
        _require(set(row) == {"variant", "macro", "payload", "includes_caption", "definition", "definition_closure", "usage"}, "invalid server asset fields")
        _require(row["variant"] in server["variants"] and re.fullmatch(r"[A-Za-z]+", row["macro"]) and key == f"{row['variant']}:{row['macro']}", "invalid server macro identity")
        _require(type(row["includes_caption"]) is bool and row["includes_caption"] == (row["variant"] == "sung" and row["macro"] != "CommunionPatenSafetyDiagram"), "incorrect server caption binding")
        _require(row["definition"] in server["definitions"] and isinstance(row["definition_closure"], list) and bool(row["definition_closure"]), "missing server macro closure")
        for ref in row["definition_closure"]:
            _require(set(ref) <= {"macro", "definition", "selected_branch", "alternatives"} and {"macro", "definition"} <= ref.keys(), "invalid server macro closure reference")
            _require(ref["definition"] in server["definitions"] and re.fullmatch(r"[A-Za-z]+", ref["macro"]), "unknown macro definition")
            _require(all(p in server["definitions"] for p in ref.get("alternatives", [])), "unknown alternate macro definition")
            _require(ref.get("selected_branch", "child") in {"child", "trainer"}, "unknown macro branch")
        for ref in row["usage"]:
            _require(set(ref) == {"source", "line"} and ref["source"] in server["source_inputs"] and type(ref["line"]) is int and ref["line"] > 0, "invalid server macro usage")
        _payload(payloads, row["payload"], "image/svg+xml"); used.add(row["payload"])
    generic = data["generic"]
    _require(isinstance(generic, dict) and set(generic) == {"origin", "outputs"}, "invalid generic asset registry")
    for output_id, row in generic["outputs"].items():
        transport._relative(output_id)
        _require("/" in output_id and set(row) == {"selection_digest", "head_sha256", "body_sha256", "source_closure", "entrypoint", "role", "flags", "diagrams"}, "invalid selected-output asset metadata")
        for key in ("selection_digest", "head_sha256", "body_sha256"):
            _hash(row[key])
        _closure(row["source_closure"], provider=output_id.split("/")[0])
        _require(row["entrypoint"] in row["source_closure"], "unbound generic entrypoint")
        _require(row["role"] in {"main", "research", "synthesis", "homily"} and isinstance(row["flags"], dict) and set(row["flags"]) == {"TriptychPrintEdition", "TriptychSynthesisEdition", "TriptychHomilyEdition"} and all(type(v) is bool for v in row["flags"].values()), "invalid selected-output flags")
        last = -1
        for unit in row["diagrams"]:
            _require(set(unit) == {"start", "end", "context", "source_tex_sha256", "asset_id", "index", "payload", "svg_sha256", "bytes", "width", "height", "viewBox", "labels_sha256", "source_refs", "selection_digest", "source_closure_digest", "recipe_digest", "runtime_fingerprint", "includes_caption"}, "invalid selected diagram fields")
            _require(type(unit["start"]) is int and type(unit["end"]) is int and last <= unit["start"] < unit["end"], "invalid or unordered diagram spans")
            last = unit["end"]
            _require(re.fullmatch(r"tikz-[a-f0-9]{24}", unit["asset_id"]) and isinstance(unit["context"], list) and all(isinstance(c, str) for c in unit["context"]), "invalid diagram identity/context")
            for key in ("source_tex_sha256", "svg_sha256", "labels_sha256", "selection_digest", "source_closure_digest", "recipe_digest", "runtime_fingerprint"):
                _hash(unit[key])
            _require(unit["selection_digest"] == row["selection_digest"] and unit["source_closure_digest"] == digest(canonical_json([{"path": p, "sha256": h} for p, h in sorted(row["source_closure"].items())])), "diagram selection/closure pin mismatch")
            _payload(payloads, unit["payload"], "image/svg+xml")
            _require(unit["svg_sha256"] == payloads[unit["payload"]]["sha256"] and unit["bytes"] == payloads[unit["payload"]]["bytes"] and type(unit["includes_caption"]) is bool, "diagram byte or caption mismatch")
            for ref in unit["source_refs"]:
                _require(set(ref) == {"path", "occurrence", "selected_line", "diagram_offset", "length", "selected_fragment_sha256"} and ref["path"] in row["source_closure"], "invalid diagram source reference")
                _hash(ref["selected_fragment_sha256"])
                _require(all(type(ref[k]) is int and ref[k] >= (0 if k == "diagram_offset" else 1) for k in ("occurrence", "selected_line", "diagram_offset", "length")), "invalid source reference span")
            used.add(unit["payload"])
    fonts = data["fonts"]
    _require(isinstance(fonts, dict) and set(fonts) == {"origin", "license", "coverage", "control_policy", "faces"}, "invalid font registry")
    for name, field in (("OFL.txt", "license"), ("glyph-coverage.json", "coverage"), ("glyph-control-policy.json", "control_policy")):
        pin = fonts[field]
        _require(pin["path"] == FONT_ROOT + "/" + name and type(pin["bytes"]) is int and pin["bytes"] > 0, "invalid font plaintext metadata pin")
        _hash(pin["sha256"])
    faces = set()
    for face in fonts["faces"]:
        _payload(payloads, face["payload"], "font/woff2"); used.add(face["payload"])
        _require(face["family"] in {"Libertinus Serif", "Libertinus Sans", "Libertinus Math"} and face["weight"] in {"400", "700"} and face["style"] in {"normal", "italic"}, "unsupported font face")
        identity = (face["family"], face["weight"], face["style"])
        _require(identity not in faces, "duplicate physical font face"); faces.add(identity)
        _require(face.get("role") in {None, "math"} and (face.get("role") == "math") == (face["family"] == "Libertinus Math"), "incorrect math font role")
        _hash(face["source"]["sha256"]); _hash(face["roundtrip_tables_sha256"])
    _require(len(faces) == 8, "expected eight actual Libertinus faces")
    _require(used == payloads.keys(), "unowned browser-print asset payload")


def _payload(payloads, path, media):
    _require(path in payloads and payloads[path]["media_type"] == media, "unknown or mistyped asset payload")


@lru_cache(maxsize=8)
def _load(root: Path, signature: tuple):
    data, delivery = _json_file(root, INDEX_PATH), _json_file(root, DELIVERY_PATH)
    try:
        _validate(data, delivery)
    except (KeyError, TypeError, AttributeError, IndexError, transport.ArtifactStoreError) as error:
        raise AssetError("invalid browser-print asset metadata: " + str(error)) from error
    return data, delivery


def _domain(root):
    root = Path(root).resolve()
    paths = [transport._path(root, relative) for relative in (INDEX_PATH, DELIVERY_PATH)]
    signature = tuple((p.stat().st_mtime_ns, p.stat().st_ctime_ns, p.stat().st_size) for p in paths)
    return root, *_load(root, signature)


def load_index(root):
    """Return an independent strict compact registry; no source or network reads."""
    return copy.deepcopy(_domain(root)[1])


def _plaintext(root, pin):
    path = transport._path(root, pin["path"])
    body = transport._verify(path, pin).read_bytes()
    _require(len(body) == pin["bytes"] and digest(body) == pin["sha256"], "font plaintext changed during read")
    return body


def _font_metadata(root, data):
    bodies = {}
    for key in ("license", "coverage", "control_policy"):
        pin = data["fonts"][key]
        bodies[key] = _plaintext(root, pin)
    coverage = json.loads(bodies["coverage"], object_pairs_hook=transport._unique_keys)
    _require(coverage["schema"] == "triptych-font-glyph-coverage/v1", "unsupported font cmap coverage")
    controls = data["fonts"]["control_policy"]
    _require(coverage["controls"] == {"file": Path(controls["path"]).name, "sha256": controls["sha256"], "bytes": controls["bytes"]} and coverage["font_manifest_sha256"] == data["fonts"]["origin"]["original_font_manifest"]["sha256"], "font coverage provenance/control pin mismatch")
    expected = {(f["family"], f["weight"], f["style"]): f for f in data["fonts"]["faces"]}
    _require(len(coverage["faces"]) == len(expected), "font coverage face count mismatch")
    seen = set()
    for face in coverage["faces"]:
        identity = face["family"], face["weight"], face["style"]
        _require(identity in expected and identity not in seen, "unbound or duplicate cmap coverage face"); seen.add(identity)
        actual = expected[identity]; payload = data["payloads"][actual["payload"]]
        _hash(face["source_cmap_sha256"])
        _require(face["woff2_sha256"] == payload["sha256"] and face["woff2_bytes"] == payload["bytes"] and face["source_otf_sha256"] == actual["source"]["sha256"] and face["source_cmap_sha256"] == face["roundtrip_cmap_sha256"], "font coverage byte/source identity mismatch")
        last = -2; count = 0
        for lo, hi in face["ranges"]:
            _require(type(lo) is int and type(hi) is int and last + 1 < lo <= hi <= 0x10FFFF and not (lo <= 0xDFFF and hi >= 0xD800), "invalid cmap coverage ranges")
            last = hi; count += hi - lo + 1
        _require(count == face["unicode_count"], "font coverage count mismatch")
    return coverage


def _svg(body):
    _require(b"<!DOCTYPE" not in body.upper() and b"<!ENTITY" not in body.upper(), "SVG declarations/entities are forbidden")
    try:
        root = ET.fromstring(body)
    except (ET.ParseError, ValueError) as error:
        raise AssetError("invalid SVG XML") from error
    _require(root.tag == "{" + _SVG_NS + "}svg", "asset is not SVG")
    tags = {"svg", "title", "defs", "path", "g", "clipPath", "use", "image"}
    attrs = {"version", "width", "height", "viewBox", "role", "id", "d", "stroke-miterlimit", "transform", "fill", "stroke", "stroke-width", "clip-path", "stroke-dasharray", "stroke-dashoffset", "stroke-linejoin", "stroke-linecap", "x", "y", "fill-rule", "fill-opacity", "stroke-opacity", "overflow", "{http://www.w3.org/1999/xlink}href", "href"}
    for element in root.iter():
        _require(element.tag in {"{" + _SVG_NS + "}" + tag for tag in tags}, "unsupported active SVG element")
        for key, value in element.attrib.items():
            _require(key in attrs, "unsupported SVG attribute")
            _require("\\" not in value, "escaped SVG attribute values are forbidden")
            if key.endswith("href"):
                if value.startswith("#"):
                    _require(bool(re.fullmatch(r"#[A-Za-z0-9_.:-]+", value)), "invalid SVG fragment")
                else:
                    _require(element.tag == "{" + _SVG_NS + "}image" and value.startswith("data:image/png;base64,"), "external SVG resource is forbidden")
                    try:
                        image = base64.b64decode(value.split(",", 1)[1], validate=True)
                    except ValueError as error:
                        raise AssetError("invalid embedded SVG PNG") from error
                    _require(image.startswith(b"\x89PNG\r\n\x1a\n"), "embedded SVG image is not PNG")
            if "url(" in value.lower():
                _require(bool(re.fullmatch(r"url\(#[A-Za-z0-9_.:-]+\)", value)), "external SVG CSS reference is forbidden")


def _typed(body, media):
    if media == "image/svg+xml":
        _svg(body)
    elif media == "font/woff2":
        _require(len(body) >= 48 and body[:4] == b"wOF2" and struct.unpack_from(">I", body, 8)[0] == len(body), "invalid WOFF2 signature/declared length")
    else:
        raise AssetError("unsupported browser-print asset media type")


def _bytes(root, data, delivery, src):
    row = data["payloads"][src]
    entry = next(e for e in delivery["artifacts"] if e["path"] == src)
    path = transport.cache_path(root, entry)
    try:
        body = transport._verify(path, entry).read_bytes()
    except FileNotFoundError as error:
        raise FileNotFoundError(f"browser-print asset is not cached: {src}; explicitly run python scripts/_web_print_assets.py hydrate --archive-dir PATH (or --fetch)") from error
    _require(len(body) == row["bytes"] and digest(body) == row["sha256"], "browser-print asset changed during read")
    _typed(body, row["media_type"])
    return body


def _record(root, data, delivery, src, *, include_body):
    row = data["payloads"][src]
    body = _bytes(root, data, delivery, src)
    result = {"src": src, "sha256": row["sha256"], "bytes": row["bytes"], "mime": row["media_type"]}
    if include_body:
        result["body"] = body
    return result


def server_asset(root, variant: str, macro: str, *, include_body=True):
    """Resolve an exact active server macro; no TeX, subprocess or network."""
    root, data, delivery = _domain(root)
    key = f"{variant}:{macro}"
    row = data["server"]["entries"].get(key)
    if row is None:
        raise AssetError("unknown server diagram: " + key)
    sources = data["server"]["source_inputs"]
    _verify_sources(root, sources)
    _verify_definitions(root, data["server"])
    result = _record(root, data, delivery, row["payload"], include_body=include_body)
    result.update(id=key, source_macro=macro, source_inputs=dict(sources), includes_caption=row["includes_caption"])
    return result


resolve_server = server_asset


def generic_assets(root, output_id: str, selection: dict, *, include_body=True):
    """Bind selected occurrences to SVGs, deriving labels from canonical text."""
    import _web_print_diagrams as diagrams
    root, data, delivery = _domain(root)
    spans = diagrams.diagram_spans(selection["body"])
    row = data["generic"]["outputs"].get(output_id)
    if row is None:
        _require(not spans, "no verified generic projection for " + output_id)
        return []
    declared = selection["selection"]
    _require(declared["selection_digest"] == digest(canonical_json({k: v for k, v in declared.items() if k != "selection_digest"})), "invalid selected-source state digest")
    expected = {"selection_digest": declared["selection_digest"], "head_sha256": digest(selection["head"]), "body_sha256": digest(selection["body"]), "source_closure": {r["path"]: r["sha256"] for r in diagrams.closure(selection)}, "entrypoint": declared["entrypoint"], "role": declared["role"], "flags": declared["flags"]}
    _require(all(row[k] == value for k, value in expected.items()), "stale selected-output projection: " + output_id)
    _verify_sources(root, row["source_closure"])
    _require(len(spans) == len(row["diagrams"]), "generic diagram occurrence count mismatch")
    result = []
    for span, unit in zip(spans, row["diagrams"]):
        _require(all(span[k] == unit[k] for k in ("start", "end", "context", "source_tex_sha256")), "generic diagram source span mismatch")
        labels = diagrams.node_labels(selection["body"][span["start"]:span["end"]])
        refs = diagrams.selected_source_refs(selection, span["start"], span["end"])
        _require(digest(canonical_json(labels)) == unit["labels_sha256"] and refs == unit["source_refs"], "generic diagram label/source reference mismatch")
        record = {k: copy.deepcopy(v) for k, v in unit.items() if k != "payload"}
        record.update(_record(root, data, delivery, unit["payload"], include_body=include_body))
        record.update(id=unit["asset_id"], asset=unit["payload"], labels=labels, source_inputs=dict(row["source_closure"]))
        result.append(record)
    return result


def font_assets(root, *, include_body=True):
    """Return eight actual, individually pinned faces and their license route."""
    root, data, delivery = _domain(root)
    _font_metadata(root, data)
    license_pin = data["fonts"]["license"]
    license_record = {"src": PREFIX + license_pin["sha256"] + ".txt", "sha256": license_pin["sha256"], "bytes": license_pin["bytes"], "mime": "text/plain", "spdx": "OFL-1.1"}
    if include_body:
        license_record["body"] = _plaintext(root, license_pin)
    result = []
    for face in data["fonts"]["faces"]:
        record = {k: copy.deepcopy(v) for k, v in face.items() if k != "payload"}
        record.update(_record(root, data, delivery, face["payload"], include_body=include_body))
        record.update(id="font:" + face["name"], href=face["payload"], license=copy.deepcopy(license_record))
        result.append(record)
    return result


def glyph_coverage(root):
    """Return per-physical-face cmap ranges; no shaping or family-union claim."""
    root, data, _ = _domain(root)
    return copy.deepcopy(_font_metadata(root, data))


def asset_bytes(root, id_or_src: str) -> bytes:
    """Read a typed source-bound asset; public tokens never name source files."""
    root, data, delivery = _domain(root)
    if id_or_src in data["server"]["entries"]:
        return server_asset(root, *id_or_src.split(":"), include_body=True)["body"]
    for face in data["fonts"]["faces"]:
        if id_or_src == "font:" + face["name"]:
            id_or_src = face["payload"]
            break
    for output in data["generic"]["outputs"].values():
        for unit in output["diagrams"]:
            if id_or_src == unit["asset_id"]:
                id_or_src = unit["payload"]
    license_pin = data["fonts"]["license"]
    if id_or_src == PREFIX + license_pin["sha256"] + ".txt":
        return _plaintext(root, license_pin)
    _require(id_or_src in data["payloads"], "unknown browser-print asset")
    if any(row["payload"] == id_or_src for row in data["server"]["entries"].values()):
        _verify_sources(root, data["server"]["source_inputs"])
        _verify_definitions(root, data["server"])
    for output in data["generic"]["outputs"].values():
        if any(unit["payload"] == id_or_src or unit["asset_id"] == id_or_src for unit in output["diagrams"]):
            _verify_sources(root, output["source_closure"])
    if data["payloads"][id_or_src]["kind"] == "font-software":
        _font_metadata(root, data)
    return _bytes(root, data, delivery, id_or_src)


def validate_registry(root, *, local_bytes=False):
    """Check metadata/current closures; optional offline exact-byte validation."""
    root, data, delivery = _domain(root)
    _verify_sources(root, data["server"]["source_inputs"])
    _verify_definitions(root, data["server"])
    for output in data["generic"]["outputs"].values():
        _verify_sources(root, output["source_closure"])
    _font_metadata(root, data)
    if local_bytes:
        for src in data["payloads"]:
            _bytes(root, data, delivery, src)
    return {"status": "ok", "payloads": len(data["payloads"]), "payload_bytes": sum(v["bytes"] for v in data["payloads"].values()), "server_diagrams": len(data["server"]["entries"]), "generic_diagrams": sum(len(v["diagrams"]) for v in data["generic"]["outputs"].values()), "font_faces": len(data["fonts"]["faces"]), "local_bytes": local_bytes, "registry_digest": data["registry_digest"]}


def hydrate(root, *, archive_dir=None, fetch=False):
    """Explicitly verify complete archives and hydrate typed disposable cache."""
    _require(type(fetch) is bool, "fetch must be an explicit boolean")
    root, data, delivery = _domain(root)
    validate_registry(root)
    hydrated = 0
    for archive in delivery["archives"]:
        expected = [entry for entry in delivery["artifacts"] if entry["archive"] == archive["id"]]
        path = transport._archive_path(root, archive, Path(archive_dir) if archive_dir is not None else None, fetch)
        hydrated += transport._read_archive(path, expected, root, {e["path"] for e in expected})
    return dict(validate_registry(root, local_bytes=True), hydrated=hydrated)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "hydrate"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--local-bytes", action="store_true", help="check every cached exact payload (offline)")
    parser.add_argument("--archive-dir", type=Path, help="explicit offline delivery pack directory")
    parser.add_argument("--fetch", action="store_true", help="explicitly download pinned immutable archives")
    args = parser.parse_args(argv)
    if args.command == "check" and (args.fetch or args.archive_dir):
        parser.error("check never fetches or hydrates; use hydrate explicitly")
    try:
        value = hydrate(args.root, archive_dir=args.archive_dir, fetch=args.fetch) if args.command == "hydrate" else validate_registry(args.root, local_bytes=args.local_bytes)
    except (AssetError, transport.ArtifactStoreError, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(value, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
