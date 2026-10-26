"""Replay explicit page geometry without changing or dropping XML WORD values."""
from __future__ import annotations

import argparse
import bisect
from collections import Counter
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from urllib.parse import urlsplit
from xml.parsers import expat

from _tooling import Example, with_examples

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-bullarium-geometry-recipe/v1"
ROLES = {"header", "body-left", "body-right", "margin-left", "margin-right",
         "notes-left", "notes-right", "footer", "uncertain", "gutter-ocr"}
SHA = re.compile(r"[a-f0-9]{64}")
LIMITATIONS = ["No OCR character correction, word restoration or translation.",
              "Unchanged pages retain their original OCR order, including unresolved defects.",
              "Explicit coordinates, role assignments and order are replayed; their historical meaning is not inferred.",
              "Geometry replay establishes no act admission, note ownership, authentication or image collation."]
EXAMPLES = (
    Example("tools/bullarium geometry --recipe .scratch/bullarium_reconstruction/geometry_engine/absent-recipe.json --out .scratch/bullarium_reconstruction/geometry_engine/preflight --json",
            ('{"code":"input","error":"geometry recipe is not readable JSON","status":"error","v":1}',),
            "A missing recipe is refused before creating outputs."),
    Example("tools/bullarium geometry --recipe .scratch/bullarium_reconstruction/geometry_engine/absent-recipe.json --out .scratch/bullarium_reconstruction/geometry_engine/preflight",
            ("bullarium geometry: geometry recipe is not readable JSON",),
            "The same safe preflight refusal in ordinary text."),
)


class GeometryError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise GeometryError(message)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def _path(root, value, relative=False):
    _require(isinstance(value, (str, Path)) and str(value), "path must be nonempty")
    raw, path = str(value), Path(value)
    _require("\\" not in raw and not any(ord(c) < 32 for c in raw) and ".." not in path.parts
             and not (relative and (path.is_absolute() or path.as_posix() != raw)),
             "input path must be canonical repository-relative without traversal")
    path = (root / path).resolve()
    _require(path.is_relative_to(root), "path escapes the repository")
    return path


def _object_pairs(items):
    result = {}
    for key, value in items:
        _require(key not in result, "duplicate recipe JSON key: " + key)
        result[key] = value
    return result


def _constant(value):
    raise GeometryError("non-finite recipe JSON value: " + value)


def _fields(value, required, optional=(), name="record"):
    _require(isinstance(value, dict) and set(required) <= set(value)
             and set(value) <= set(required) | set(optional), name + " has missing or unsupported fields")


def _pair(value, name, minimum=0):
    _require(isinstance(value, list) and len(value) == 2 and all(type(n) is int for n in value)
             and minimum <= value[0] <= value[1], name + " must be an inclusive-line or half-open-byte pair")


def _pin(root, item, frozen, input_map):
    _fields(item, {"sha256", "byte_size"}, {"path", "artifact_id", "source_url"}, "source pin")
    _require(isinstance(item["sha256"], str) and SHA.fullmatch(item["sha256"])
             and type(item["byte_size"]) is int and item["byte_size"] >= 0, "source requires a complete hash and byte size")
    if "source_url" in item:
        value = item["source_url"]
        _require(isinstance(value, str) and not any(c.isspace() for c in value), "source_url must be a public HTTP(S) URL")
        url = urlsplit(value)
        _require(url.scheme in {"http", "https"} and url.netloc and not url.username and not url.password,
                 "source_url must be a public HTTP(S) URL")
    location = input_map.get(item.get("artifact_id"), input_map.get(item["sha256"], item.get("path")))
    _require(location is not None, "source bytes unavailable; supply an explicit input_map cache path")
    path = _path(root, location, True)
    data = path.read_bytes()
    _require(len(data) == item["byte_size"] and _sha(data) == item["sha256"], "complete source hash or byte size mismatch")
    if "artifact_id" in item:
        _require(isinstance(item["artifact_id"], str) and re.fullmatch(r"artifact\.[a-z0-9.-]+", item["artifact_id"]),
                 "source artifact_id must be an explicit source-library identity")
    frozen[path] = item["sha256"]
    return data


def load_recipe(root, recipe_path, input_map=None):
    """Read the small versioned recipe; reject unpinned inputs and OBJECT attrs."""
    root = Path(root).resolve()
    path = _path(root, recipe_path)
    try:
        payload = path.read_bytes()
        recipe = json.loads(payload, object_pairs_hook=_object_pairs, parse_constant=_constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise GeometryError("geometry recipe is not readable JSON") from error
    _fields(recipe, {"schema", "source_txt", "source_xml", "changed_pages"},
            {"volume", "notes", "limitations", "evidence", "serialization", "expected_output", "source_evidence_pins"}, "recipe")
    _require(recipe["schema"] == SCHEMA, "unknown geometry recipe schema")
    _require(recipe.get("serialization", "recipe-whitespace") in {"recipe-whitespace", "word-per-line"},
             "unknown page serialization")
    _require(isinstance(recipe["changed_pages"], list), "changed_pages requires an array")
    for name in ("notes", "evidence"):
        if name in recipe:
            value = recipe[name]
            _require(isinstance(value, str) or (isinstance(value, list) and all(isinstance(v, str) for v in value)),
                     name + " accepts prose only, never OBJECT attributes")
    if "limitations" in recipe:
        _require(isinstance(recipe["limitations"], list) and all(isinstance(v, str) for v in recipe["limitations"]),
                 "limitations must contain strings")
    frozen = {path: _sha(payload)}
    if isinstance(input_map, (str, Path)):
        map_path = _path(root, input_map)
        map_bytes = map_path.read_bytes()
        mapped = json.loads(map_bytes, object_pairs_hook=_object_pairs, parse_constant=_constant)
        _fields(mapped, {"schema", "inputs"}, name="input map")
        _require(mapped["schema"] == "triptych-bullarium-geometry-input-map/v1", "unknown runtime input-map schema")
        input_map = mapped["inputs"]
        frozen[map_path] = _sha(map_bytes)
    input_map = {} if input_map is None else input_map
    _require(isinstance(input_map, dict), "input_map requires an artifact-id or SHA256 to cache-path object")
    allowed = {recipe[name].get("artifact_id") for name in ("source_txt", "source_xml")
               if isinstance(recipe[name], dict)} | {recipe[name].get("sha256") for name in ("source_txt", "source_xml")
                                                    if isinstance(recipe[name], dict)}
    _require(all(isinstance(k, str) and k in allowed for k in input_map), "unknown input_map source identity")
    raw, xml = (_pin(root, recipe[name], frozen, input_map) for name in ("source_txt", "source_xml"))
    evidence = recipe.get("source_evidence_pins", {})
    _require(isinstance(evidence, dict), "source_evidence_pins requires a path/hash object")
    for value, digest in evidence.items():
        _require(isinstance(digest, str) and SHA.fullmatch(digest), "evidence requires an exact SHA-256")
        evidence_path = _path(root, value, True)
        _require(_sha(evidence_path.read_bytes()) == digest, "source evidence SHA-256 mismatch")
        frozen[evidence_path] = digest
    return recipe, raw, xml, frozen


def _tokens(data):
    text = data.decode("utf-8")
    char_cursor = byte_cursor = 0
    result = []
    for match in re.finditer(r"\S+", text):
        byte_cursor += len(text[char_cursor:match.start()].encode())
        end = byte_cursor + len(match.group().encode())
        result.append((byte_cursor, end, match.group()))
        char_cursor, byte_cursor = match.end(), end
    return result


def _line(newlines, byte):
    return bisect.bisect_left(newlines, byte) + 1


def _tag_end(data, start):
    quote = None
    for index in range(start, len(data)):
        char = data[index]
        if quote is not None:
            if char == quote:
                quote = None
        elif char in (34, 39):
            quote = char
        elif char == 62:
            return index + 1
    raise GeometryError("unterminated XML tag")


def _xml_pages(xml, raw, tokens, changed):
    """Expat supplies offsets in the original XML, including encoded entities."""
    xml.decode("utf-8")
    parser = expat.ParserCreate()
    pages, leaves, newlines = [], set(), [m.start() for m in re.finditer(b"\n", raw)]
    page = word = None
    token_cursor = word_count = line_count = 0
    in_line = False

    def start(name, attrs):
        nonlocal page, word, word_count, line_count, in_line
        if name == "OBJECT":
            _require(page is None, "nested XML OBJECT")
            match = re.search(r"_(\d+)\.djvu$", attrs.get("usemap", ""))
            _require(match is not None, "XML OBJECT requires an explicit scan leaf")
            leaf = int(match[1])
            _require(leaf not in leaves, "duplicate XML scan leaf")
            leaves.add(leaf)
            dims = [int(attrs.get(name, "0")) for name in ("width", "height")]
            _require(all(n > 0 for n in dims), "XML page requires positive dimensions")
            page = {"artifact_page": len(pages) + 1, "leaf": leaf, "dimensions": dims,
                    "source_token_range_0": [token_cursor, token_cursor], "source_word_range_1": None,
                    "words": [], "word_count": 0, "line_count": 0}
        elif name == "LINE":
            _require(page is not None and not in_line and word is None, "XML LINE has no unique page owner")
            in_line = True
            line_count += 1
            page["line_count"] += 1
        elif name == "WORD":
            _require(page is not None and in_line and word is None, "XML WORD has no unique LINE/page owner")
            word_count += 1
            page["word_count"] += 1
            begin = parser.CurrentByteIndex
            end = _tag_end(xml, begin)
            word = {"source_word_global_1": word_count, "source_word_page_1": page["word_count"],
                    "source_line_global_1": line_count, "source_line_page_1": page["line_count"],
                    "start": begin, "tag_end": end, "selfclosing": xml[begin:end].endswith(b"/>"),
                    "chars": [], "attrs": dict(attrs)}

    def chars(value):
        if word is not None:
            word["chars"].append(value)

    def end(name):
        nonlocal page, word, token_cursor, in_line
        if name == "WORD":
            value = "".join(word["chars"])
            parts = value.split()
            matched = tokens[token_cursor:token_cursor + len(parts)]
            _require([t[2] for t in matched] == parts, "whole raw TXT/XML WORD token mismatch")
            if page["leaf"] in changed:
                coords = word["attrs"].get("coords")
                _require(isinstance(coords, str) and re.fullmatch(r"-?\d+,-?\d+,-?\d+,-?\d+", coords),
                         "changed WORD requires exact integer coordinates")
                x0, y0, x1, y1 = map(int, coords.split(","))
                stop = word["tag_end"] if word["selfclosing"] else _tag_end(xml, parser.CurrentByteIndex)
                page["words"].append({**{k: word[k] for k in ("source_word_global_1", "source_word_page_1", "source_line_global_1", "source_line_page_1")},
                    "source_xml_byte_range_0": [word["start"], stop], "value": value, "coords": coords,
                    "source_attrs": word["attrs"], "source_bbox": [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)],
                    "source_txt_token_byte_ranges_0": [[a, b] for a, b, _ in matched],
                    "source_txt_physical_lines": sorted({_line(newlines, a) for a, b, _ in matched})})
            token_cursor += len(parts)
            word = None
        elif name == "LINE":
            in_line = False
        elif name == "OBJECT":
            _require(word is None and not in_line, "unterminated page WORD or LINE")
            page["source_token_range_0"][1] = token_cursor
            first, last = page["source_token_range_0"]
            page["source_word_range_1"] = [word_count - page["word_count"] + 1, word_count] if page["word_count"] else None
            page["source_lf_range_1"] = page["source_byte_range_0"] = None
            if first < last:
                a, z = _line(newlines, tokens[first][0]), _line(newlines, tokens[last - 1][1] - 1)
                begin = newlines[a - 2] + 1 if a > 1 else 0
                stop = newlines[z - 1] + 1 if z <= len(newlines) else len(raw)
                page["source_lf_range_1"], page["source_byte_range_0"] = [a, z], [begin, stop]
            pages.append(page)
            page = None

    def doctype(name, system, public, subset):
        _require(name == "DjVuXML" and system is None and public is None and not subset,
                 "external or entity-bearing XML DOCTYPE is not permitted")

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.CharacterDataHandler, parser.StartDoctypeDeclHandler = chars, doctype
    parser.XmlDeclHandler = lambda version, encoding, standalone: _require(
        encoding is None or encoding.lower().replace("-", "") == "utf8", "source XML must use UTF-8")
    parser.Parse(xml, True)
    _require(token_cursor == len(tokens), "XML does not account for every raw TXT token")
    return pages, word_count


def _whitespace(value):
    return isinstance(value, str) and all(char in " \t\r\n" for char in value)


def source_pages(root, source_txt, source_xml, leaves, *, input_map=None):
    """Extract exact native WORD geometry after checking both whole inputs.

    This is a read-only recipe-preparation API. It does not propose column
    order or assign WORDs to an act; those remain explicit review decisions.
    """
    root = Path(root).resolve()
    _require(isinstance(leaves, list) and leaves and
             all(type(leaf) is int and leaf >= 0 for leaf in leaves) and len(set(leaves)) == len(leaves),
             "selected scan leaves must be a nonempty unique integer array")
    input_map = {} if input_map is None else input_map
    _require(isinstance(input_map, dict), "input_map requires an artifact-id or SHA256 to cache-path object")
    allowed = {pin.get(key) for pin in (source_txt, source_xml) if isinstance(pin, dict)
               for key in ("artifact_id", "sha256")}
    _require(all(isinstance(key, str) and key in allowed for key in input_map), "unknown input_map source identity")
    frozen = {}
    raw, xml = (_pin(root, pin, frozen, input_map) for pin in (source_txt, source_xml))
    pages, count = _xml_pages(xml, raw, _tokens(raw), {leaf: {} for leaf in leaves})
    selected = [page for page in pages if page["leaf"] in leaves]
    _require({page["leaf"] for page in selected} == set(leaves), "selected scan leaf is absent from XML")
    _require(all(_sha(path.read_bytes()) == digest for path, digest in frozen.items()),
             "pinned input changed during page extraction")
    # Source identity is durable; runtime cache locations are deliberately absent.
    pin_keys = {"artifact_id", "sha256", "byte_size", "source_url"}
    return {"schema": "triptych-bullarium-native-word-pages/v1",
            "source_txt": {key: value for key, value in source_txt.items() if key in pin_keys},
            "source_xml": {key: value for key, value in source_xml.items() if key in pin_keys},
            "source_WORDs": count, "pages": selected,
            "limits": "Whole TXT/XML token correspondence and exact WORD byte coordinates are checked. Column order, act ownership and historical authenticity are not inferred."}


def _derive(root, recipe_path, input_map=None):
    recipe, raw, xml, frozen = load_recipe(root, recipe_path, input_map)
    specifications = {}
    for item in recipe["changed_pages"]:
        _fields(item, {"leaf", "object_ordinal_1", "source_byte_range_0", "source_lf_range_1", "words"},
                {"before", "output_byte_range_0", "replacement_sha256"}, "changed page")
        _require(type(item["leaf"]) is int and item["leaf"] >= 0 and item["leaf"] not in specifications,
                 "changed scan leaf is invalid or duplicated")
        specifications[item["leaf"]] = item
    tokens = _tokens(raw)
    pages, word_count = _xml_pages(xml, raw, tokens, specifications)
    found = {p["leaf"] for p in pages}
    _require(set(specifications) <= found, "changed scan leaf is absent from XML")
    patches = []
    serialization = recipe.get("serialization", "recipe-whitespace")
    for page in pages:
        if page["leaf"] not in specifications:
            continue
        item = specifications[page["leaf"]]
        _pair(item["source_byte_range_0"], "source byte range")
        _pair(item["source_lf_range_1"], "source LF range", 1)
        _require(type(item["object_ordinal_1"]) is int and item["object_ordinal_1"] == page["artifact_page"],
                 "changed page OBJECT ordinal mismatch")
        _require(page["source_byte_range_0"] is not None and item["source_byte_range_0"] == page["source_byte_range_0"]
                 and item["source_lf_range_1"] == page["source_lf_range_1"], "changed page raw byte/LF span mismatch")
        first, last = page["source_token_range_0"]
        a, z = item["source_byte_range_0"]
        _require((first == 0 or tokens[first - 1][1] <= a) and (last == len(tokens) or tokens[last][0] >= z),
                 "changed page LF span includes a neighboring page token")
        _require(isinstance(item["words"], list) and len(item["words"]) == len(page["words"]),
                 "changed page omitted or duplicated a WORD")
        source_words = {w["source_word_global_1"]: w for w in page["words"]}
        before = item.get("before", "")
        _require(_whitespace(before), "page may insert only whitespace around unchanged WORDs")
        payload, mapped, seen = bytearray(before.encode()), [], set()
        for selected in item["words"]:
            required = {"source_word_global_1", "source_word_page_1", "source_line_global_1", "source_line_page_1",
                        "source_xml_byte_range_0", "value", "coords", "role", "flags", "after"}
            optional = {"source_attrs", "source_bbox", "source_txt_token_byte_ranges_0", "source_txt_physical_lines", "output_utf8_byte_range_0"}
            _fields(selected, required, optional, "changed WORD")
            for key in ("source_word_global_1", "source_word_page_1", "source_line_global_1", "source_line_page_1"):
                _require(type(selected[key]) is int and selected[key] > 0, "WORD ordinals must be positive integers")
            number = selected["source_word_global_1"]
            _require(number in source_words and number not in seen, "WORD is absent, duplicated or belongs to a different page")
            original = source_words[number]
            _pair(selected["source_xml_byte_range_0"], "XML WORD byte range")
            for key in required - {"role", "flags", "after"} | (optional & set(selected)) - {"output_utf8_byte_range_0"}:
                _require(selected[key] == original[key], "changed WORD source pin mismatch: " + key)
            _require(isinstance(selected["role"], str) and selected["role"] in ROLES and isinstance(selected["flags"], list)
                     and all(isinstance(flag, str) and flag for flag in selected["flags"]), "WORD requires a typed role and retained flags")
            after = selected["after"]
            _require(_whitespace(after), "only whitespace may be inserted around a WORD")
            if serialization == "word-per-line":
                _require(after and all(c == "\n" for c in after), "word-per-line requires an independent LF after every WORD")
            begin = len(payload)
            payload.extend(original["value"].encode())
            mapped.append({**original, "role": selected["role"], "flags": selected["flags"],
                           "relative_output_byte_range_0": [begin, len(payload)],
                           "expected_output_byte_range_0": selected.get("output_utf8_byte_range_0")})
            payload.extend(after.encode())
            seen.add(number)
        _require(seen == set(source_words), "changed page does not map all source WORDs exactly once")
        payload = bytes(payload)
        expected_tokens = [part for w in item["words"] for part in w["value"].split()]
        _require([t[2] for t in _tokens(payload)] == expected_tokens, "WORD boundaries merged or introduced output tokens")
        if "replacement_sha256" in item:
            _require(isinstance(item["replacement_sha256"], str) and SHA.fullmatch(item["replacement_sha256"])
                     and _sha(payload) == item["replacement_sha256"], "replacement page SHA-256 mismatch")
        patches.append({"page": page, "specification": item, "payload": payload, "mapping": mapped})
    patches.sort(key=lambda p: p["page"]["source_byte_range_0"][0])
    output, chunks, cursor, word_map = bytearray(), [], 0, []

    def copied(stop):
        nonlocal cursor
        if cursor < stop:
            begin = len(output)
            data = raw[cursor:stop]
            output.extend(data)
            chunks.append({"kind": "copied-raw-ocr", "source_byte_range_0": [cursor, stop],
                           "output_byte_range_0": [begin, len(output)], "sha256": _sha(data)})
            cursor = stop

    for patch in patches:
        page, item = patch["page"], patch["specification"]
        a, z = page["source_byte_range_0"]
        _require(cursor <= a < z, "changed page byte spans overlap")
        copied(a)
        begin = len(output)
        output.extend(patch["payload"])
        page["output_byte_range_0"] = [begin, len(output)]
        if "output_byte_range_0" in item:
            _pair(item["output_byte_range_0"], "output page byte range")
            _require(item["output_byte_range_0"] == page["output_byte_range_0"], "output page byte range mismatch")
        chunks.append({"kind": "reviewed-page-serialization", "leaf": page["leaf"],
                       "source_byte_range_0": [a, z], "output_byte_range_0": page["output_byte_range_0"],
                       "source_sha256": _sha(raw[a:z]), "output_sha256": _sha(patch["payload"])})
        for word in patch["mapping"]:
            x, y = word.pop("relative_output_byte_range_0")
            span = [begin + x, begin + y]
            expected = word.pop("expected_output_byte_range_0")
            if expected is not None:
                _pair(expected, "output WORD byte range")
                _require(expected == span, "output WORD byte range mismatch")
            word.update(leaf=page["leaf"], object_ordinal_1=page["artifact_page"], output_utf8_byte_range_0=span)
            # The XML pin preserves all attributes; the compact map needs only coordinates.
            word.pop("source_attrs")
            word_map.append(word)
        cursor = z
    copied(len(raw))
    output = bytes(output)
    output_tokens = _tokens(output)
    _require(Counter(t[2] for t in output_tokens) == Counter(t[2] for t in tokens), "whole output token bijection failed")
    output_lfs = [m.start() for m in re.finditer(b"\n", output)]
    for word in word_map:
        a, z = word["output_utf8_byte_range_0"]
        _require(output[a:z] == word["value"].encode(), "output WORD value changed")
        word["output_lf_range_1"] = [_line(output_lfs, a), _line(output_lfs, max(a, z - 1))]
    if serialization == "word-per-line":
        _require(all(a["output_lf_range_1"][1] < z["output_lf_range_1"][0]
                     for a, z in zip(word_map, word_map[1:]) if a["leaf"] == z["leaf"]),
                 "changed WORDs share output LF lines")
    copy_chunks = [c for c in chunks if c["kind"] == "copied-raw-ocr"]
    copy_starts = [c["source_byte_range_0"][0] for c in copy_chunks]
    for page in pages:
        page.pop("words")
        if page["leaf"] not in specifications:
            span = page["source_byte_range_0"]
            page["output_byte_range_0"] = None
            if span is not None:
                index = bisect.bisect_right(copy_starts, span[0]) - 1
                _require(index >= 0, "unchanged page escapes a copied byte chunk")
                chunk = copy_chunks[index]
                a, z = chunk["source_byte_range_0"]
                _require(a <= span[0] <= span[1] <= z, "unchanged page overlaps a changed page byte span")
                offset = chunk["output_byte_range_0"][0] - a
                page["output_byte_range_0"] = [n + offset for n in span]
        span = page["output_byte_range_0"]
        page["output_lf_range_1"] = [_line(output_lfs, span[0]), _line(output_lfs, span[1] - 1)] if span else None
        page["serialization"] = serialization if page["leaf"] in specifications else "unchanged-raw-ocr"
    if "expected_output" in recipe:
        expected = recipe["expected_output"]
        _fields(expected, {"sha256", "byte_size"}, name="expected output")
        _require(type(expected["byte_size"]) is int and expected["byte_size"] == len(output)
                 and expected["sha256"] == _sha(output), "whole hybrid output hash or byte size mismatch")
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=compressed, mode="wb", mtime=0, compresslevel=6) as stream:
        for word in word_map:
            stream.write((json.dumps(word, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode())
    products = {"hybrid.txt": output,
                "byte-map.json": _json_bytes({"schema": "triptych-bullarium-hybrid-byte-map/v1", "source_sha256": _sha(raw),
                                              "output_sha256": _sha(output), "chunks": chunks}),
                "page-map.json": _json_bytes({"schema": "triptych-bullarium-hybrid-page-map/v1", "pages": pages}),
                "changed-word-map.jsonl.gz": compressed.getvalue()}
    info = {"schema": "triptych-bullarium-hybrid-witness/v1", "generator": "bullarium-geometry", "generator_version": 1,
            "recipe_sha256": frozen[_path(root, recipe_path)], "source_txt": recipe["source_txt"], "source_xml": recipe["source_xml"],
            "source_evidence_pins": recipe.get("source_evidence_pins", {}), "serialization": serialization,
            "source_WORDs": word_count, "source_tokens": len(tokens), "source_pages": len(pages),
            "changed_pages": len(patches), "changed_WORDs": len(word_map), "hybrid_sha256": _sha(output), "hybrid_bytes": len(output),
            "word_map_coverage": "changed-pages-only; unchanged bytes and page WORD/token ranges are mapped compactly",
            "roles": dict(sorted(Counter(w["role"] for w in word_map).items())), "limitations": LIMITATIONS + recipe.get("limitations", []),
            "checks": {name: True for name in ("whole_raw_TXT_XML_token_equality", "whole_output_token_bijection",
                "every_changed_WORD_exactly_once", "indivisible_WORD_values_unchanged", "exact_XML_byte_offsets_and_coordinates",
                "unchanged_raw_chunks_byte_identical", "all_source_and_output_bytes_accounted", "no_OBJECT_attributes_serialized")},
            "outputs": {name: {"sha256": _sha(data), "byte_size": len(data)} for name, data in products.items()}}
    if "artifact_id" in recipe["source_txt"]:
        info["derived_from"] = recipe["source_txt"]["artifact_id"]
    if "volume" in recipe:
        info["volume"] = recipe["volume"]
    products["validation.json"] = _json_bytes(info)
    return products, info, frozen


def _destination(root, out_dir):
    out = _path(root, out_dir)
    _require(any(out.is_relative_to(root / owner) for owner in (".scratch", "build")),
             "geometry output must remain under .scratch or build")
    return out


def build(root, recipe_path, out_dir, *, input_map=None):
    """Build five deterministic scratch products, never canonical source records."""
    root = Path(root).resolve()
    out = _destination(root, out_dir)
    products, info, frozen = _derive(root, recipe_path, input_map)
    for name, data in products.items():
        path = out / name
        _require(path not in frozen and (not path.exists() or path.read_bytes() == data),
                 "refusing to overwrite input or differing geometry output: " + name)
    _require(all(_sha(path.read_bytes()) == digest for path, digest in frozen.items()), "pinned input changed during geometry replay")
    out.mkdir(parents=True, exist_ok=True)
    for name, data in products.items():
        path = out / name
        if not path.exists():
            with tempfile.NamedTemporaryFile(dir=out, delete=False) as staged:
                temporary = Path(staged.name)
                staged.write(data)
            try:
                try:
                    os.link(temporary, path)
                except FileExistsError:
                    _require(path.read_bytes() == data, "geometry output appeared with differing bytes")
            finally:
                temporary.unlink()
    return info


def check(root, recipe_path, out_dir, *, input_map=None):
    """Independently replay inputs and compare every product, including all maps."""
    root = Path(root).resolve()
    out = _destination(root, out_dir)
    products, info, frozen = _derive(root, recipe_path, input_map)
    for name, data in products.items():
        _require((out / name).is_file() and (out / name).read_bytes() == data, "geometry product mismatch: " + name)
    _require(all(_sha(path.read_bytes()) == digest for path, digest in frozen.items()), "pinned input changed during geometry check")
    return info


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise GeometryError(message)


def main(argv=None, examples=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = _Parser(prog="bullarium geometry", description=__doc__)
    with_examples(parser, examples.get("geometry", EXAMPLES) if isinstance(examples, dict) else examples or EXAMPLES)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--recipe", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--input-map", type=Path, help="explicit versioned artifact-id/SHA256 to acquired-cache path map")
    parser.add_argument("--json", action="store_true")
    try:
        args = parser.parse_args(argv)
        info = (check if args.check else build)(args.root, args.recipe, args.out, input_map=args.input_map)
        result = {"v": 1, "status": "valid" if args.check else "built", "hybrid_sha256": info["hybrid_sha256"],
                  "changed_pages": info["changed_pages"], "changed_WORDs": info["changed_WORDs"]}
        print(json.dumps(result, sort_keys=True, separators=(",", ":")) if args.json else
              f"geometry: {result['status']}; {result['changed_pages']} pages; {result['changed_WORDs']} unchanged WORD values")
        return 0
    except (ValueError, OSError, KeyError, TypeError, expat.ExpatError) as error:
        print(json.dumps({"v": 1, "status": "error", "code": "input", "error": str(error)}, sort_keys=True, separators=(",", ":"))
              if "--json" in argv else f"bullarium geometry: {error}", file=sys.stderr)
        return 2
