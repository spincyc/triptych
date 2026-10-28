"""Replay explicit page geometry without changing or dropping XML WORD values."""
from __future__ import annotations

import argparse
import bisect
from collections import Counter, defaultdict
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import statistics
import sys
import tempfile
import tomllib
from urllib.parse import urlsplit
from xml.parsers import expat

from _tooling import Example, with_examples

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-bullarium-geometry-recipe/v1"
SCHEMA_V2 = "triptych-bullarium-geometry-recipe/v2"
# v2 rows name their role by code; the replay contract (ROLES) is unchanged.
ROLE_CODES = {"H": "header", "L": "body-left", "R": "body-right", "ML": "margin-left", "MR": "margin-right",
              "F": "footer", "G": "gutter-ocr"}
V2_PAGE_FIELDS = {"leaf", "object_ordinal_1", "status"}
V2_PAGE_OPTIONAL = {"rows", "hold", "measurements", "role_WORD_counts", "inseparable_WORDs", "margin_blocks",
                    "header_rows", "paragraph_breaks", "source_word_range_1", "source_lf_range_1"}
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
    _require(isinstance(recipe, dict) and recipe.get("schema") in {SCHEMA, SCHEMA_V2}, "unknown geometry recipe schema")
    if recipe["schema"] == SCHEMA_V2:
        _fields(recipe, {"schema", "source_txt", "source_xml", "pages"},
                {"volume", "notes", "limitations", "expected_output", "proposal"}, "recipe")
        _require(isinstance(recipe["pages"], list) and recipe["pages"], "v2 pages requires a nonempty array")
    else:
        _fields(recipe, {"schema", "source_txt", "source_xml", "changed_pages"},
                {"volume", "notes", "limitations", "evidence", "serialization", "expected_output", "source_evidence_pins"}, "recipe")
        _require(isinstance(recipe["changed_pages"], list), "changed_pages requires an array")
    _require(recipe.get("serialization", "recipe-whitespace") in {"recipe-whitespace", "word-per-line"},
             "unknown page serialization")
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


def _v2_runs(value):
    _require(isinstance(value, list) and value, "v2 row requires nonempty WORD runs")
    ids = []
    for run in value:
        _require(isinstance(run, list) and len(run) == 2 and all(type(n) is int and n > 0 for n in run)
                 and run[0] <= run[1], "v2 WORD run must be an ascending positive ordinal pair")
        ids.extend(range(run[0], run[1] + 1))
    return ids


def expand_v2(recipe, raw, xml):
    """Expand compact v2 rows into the explicit v1 recipe the replay checks.

    Every page of the XML is listed, in OBJECT order, as ``reordered``,
    ``held`` or ``empty``.  A reordered page lists output rows ``[code, break,
    runs]``: one LF per row, a blank line before a row whose break is ``p``,
    one TAB before a marginal row, and inside a row one SPACE unless the
    preceding WORD value already ends in whitespace.  Held and empty pages are
    not changed.  The expansion supplies only pins read from the XML; the v1
    path then proves every WORD exactly once and every value unchanged.
    """
    _require(recipe["schema"] == SCHEMA_V2, "v2 expansion requires a v2 recipe")
    specs = recipe["pages"]
    for item in specs:
        _fields(item, V2_PAGE_FIELDS, V2_PAGE_OPTIONAL, "v2 page")
        _require(type(item["leaf"]) is int and item["leaf"] >= 0 and type(item["object_ordinal_1"]) is int
                 and item["status"] in {"reordered", "held", "empty"}, "v2 page identity or status is invalid")
        _require((item["status"] == "reordered") == ("rows" in item), "only a reordered v2 page carries rows")
        _require(item["status"] != "held" or isinstance(item.get("hold"), dict), "a held v2 page records its hold")
    reordered = {item["leaf"]: item for item in specs if item["status"] == "reordered"}
    _require(len(reordered) == sum(item["status"] == "reordered" for item in specs), "duplicate reordered v2 leaf")
    pages, _ = _xml_pages(xml, raw, _tokens(raw), reordered)
    _require([(p["leaf"], p["artifact_page"]) for p in pages] == [(i["leaf"], i["object_ordinal_1"]) for i in specs],
             "v2 pages must list every XML OBJECT once, in order")
    changed = []
    for page, item in zip(pages, specs):
        if item["status"] == "empty":
            _require(page["word_count"] == 0, "an empty v2 page has WORDs")
        if item["status"] != "reordered":
            continue
        words = {w["source_word_global_1"]: w for w in page["words"]}
        rows = item["rows"]
        _require(isinstance(rows, list) and rows, "a reordered v2 page requires rows")
        sequence = []
        for index, row in enumerate(rows):
            _require(isinstance(row, list) and len(row) == 3 and row[0] in ROLE_CODES and row[1] in {"l", "p"},
                     "v2 row must be [role code, l|p, runs]")
            sequence.extend((wid, row[0], index) for wid in _v2_runs(row[2]))
        entries = []
        for k, (wid, code, index) in enumerate(sequence):
            _require(wid in words, "v2 row names a WORD absent from its page")
            value = words[wid]["value"]
            if k + 1 == len(sequence):
                after = "\n"
            elif sequence[k + 1][2] == index:
                after = "" if value and value[-1] in " \t\r\n" else " "
            else:
                following = rows[sequence[k + 1][2]]
                after = ("\n\n" if following[1] == "p" else "\n") + ("\t" if following[0] in {"ML", "MR"} else "")
            entries.append({**{key: words[wid][key] for key in ("source_word_global_1", "source_word_page_1",
                            "source_line_global_1", "source_line_page_1", "source_xml_byte_range_0", "value", "coords")},
                            "role": ROLE_CODES[code], "flags": [], "after": after})
        changed.append({"leaf": page["leaf"], "object_ordinal_1": page["artifact_page"],
                        "source_byte_range_0": page["source_byte_range_0"], "source_lf_range_1": page["source_lf_range_1"],
                        "before": "\t" if rows[0][0] in {"ML", "MR"} else "", "words": entries})
    expanded = {"schema": SCHEMA, "source_txt": recipe["source_txt"], "source_xml": recipe["source_xml"],
                "serialization": "recipe-whitespace", "changed_pages": changed}
    for name in ("volume", "notes", "limitations", "expected_output"):
        if name in recipe:
            expanded[name] = recipe[name]
    return expanded


def _derive(root, recipe_path, input_map=None):
    recipe, raw, xml, frozen = load_recipe(root, recipe_path, input_map)
    source_schema = recipe["schema"]
    if source_schema == SCHEMA_V2:
        recipe = expand_v2(recipe, raw, xml)
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
    if source_schema == SCHEMA_V2:   # v1 validation bytes stay exactly as before
        info["recipe_schema"] = SCHEMA_V2
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


# ---------------------------------------------------------------------------
# Reading-order proposal (`geometry propose`), unit mapping (`geometry
# map-units`) and registration (`geometry register`).
#
# The proposal is the only heuristic step.  It reads WORD boxes, token counts
# and non-whitespace character counts, never wording, and writes an explicit
# v2 recipe that the replay above expands and proves.  Pixel thresholds are
# fractions of the volume's measured column width (M) or a page's line pitch
# (P); the values were calibrated on volume IV (measure 750 px) and are stated
# here as px/750 so that the calibration is visible.
# ---------------------------------------------------------------------------
PROPOSAL_ALGORITHM = "bullarium-envelope/v1"
PROPOSAL_PARAMS = {
    "min_page_words": 60, "line_min_tokens": 3, "line_band_y_H": [0.10, 0.95], "line_max_height_H": 0.04,
    "line_min_width_W": 0.15, "gutter_search_W": [0.30, 0.70], "gutter_step_W": 4 / 2274,
    "gutter_max_crossings": 6, "min_lines_per_column": 10, "measure_bin_W": 4 / 2274,
    "edge_min_support": 8, "edge_bin_M": 6 / 750, "edge_window_M": 30 / 750, "edge_inlier_M": 6 / 750,
    "edge_max_mad_M": 4 / 750, "edge_max_slope": 0.03, "left_confirm_window_M": 12 / 750, "left_confirm_min": 3,
    "unconfirmed_extra_M": 8 / 750, "full_line_tol_M": 8 / 750,
    "left_body_tol_M": 9 / 750, "left_margin_tol_M": 12 / 750, "right_body_tol_M": 2 / 750,
    "right_margin_tol_M": 4 / 750, "gutter_tol_M": 6 / 750, "right_start_tol_M": 14 / 750,
    "gutter_ocr_max_chars": 2, "last_word_hang_M": 24 / 750, "merged_line_indent_M": 140 / 750,
    "margin_absorb_indent_M": 140 / 750, "margin_min_char_M": 5 / 750, "body_min_char_M": 8 / 750,
    "margin_body_min_gap_M": 8 / 750, "header_band_H": 0.16, "header_row_tol_P": 0.5,
    "header_isolation_P": 1.2, "text_top_min_tokens": 4, "text_top_min_width_M": 0.4,
    "text_top_min_height": 0.85, "footer_band_H": 0.88, "footer_gap_P": 1.6, "row_merge_P": 0.45,
    "margin_row_merge_P": 0.3, "margin_block_gap_factor": 1.5, "margin_block_gap_default_P": 0.9,
    "margin_block_max_gap_P": 3.0, "margin_anchor_back_rows": 2, "paragraph_indent_M": 22 / 750,
    "paragraph_short_M": 45 / 750,
}
CODE_OF = {role: code for code, role in ROLE_CODES.items()}
CATALOG = "src/sources/papal-documents/bullarium-catalog.json"
WITHDRAWALS = "src/sources/papal-documents/bullarium-active-withdrawals.json"
GEOMETRY_MANIFEST = "src/sources/papal-documents/bullarium-geometry-manifest.json"
GEOMETRY_FRAGMENT_MANIFEST = "src/sources/papal-documents/bullarium-geometry-fragment-manifest.json"
MAPPING_SCHEMA = "triptych-bullarium-reading-order-unit-mapping/v1"


class Hold(Exception):
    """A page-level hold: the page keeps its raw OCR bytes and a stated reason."""

    def __init__(self, reason, **detail):
        super().__init__(reason)
        self.reason, self.detail = reason, detail


def _yc(word):
    return (word["source_bbox"][1] + word["source_bbox"][3]) / 2


def _page_lines(words):
    lines = {}
    for word in words:
        lines.setdefault(word["source_line_global_1"], []).append(word)
    return [lines[key] for key in sorted(lines)]


def _box(words):
    return (min(w["source_bbox"][0] for w in words), min(w["source_bbox"][1] for w in words),
            max(w["source_bbox"][2] for w in words), max(w["source_bbox"][3] for w in words))


def _ntok(words):
    return sum(len(w["value"].split()) for w in words)


def _nchars(word):
    return len("".join(word["value"].split()))


def _theil_sen(points):
    slopes = [(xj - xi) / (yj - yi) for i, (yi, xi) in enumerate(points) for yj, xj in points[i + 1:] if yj != yi]
    slope = statistics.median(slopes) if slopes else 0.0
    return statistics.median(x - slope * y for y, x in points), slope


def _at(edge, y):
    return edge["a"] + edge["b"] * y


def _candidate_lines(page, p):
    width, height = page["dimensions"]
    out = []
    for words in _page_lines(page["words"]):
        x0, y0, x1, y1 = _box(words)
        if (_ntok(words) >= p["line_min_tokens"] and p["line_band_y_H"][0] * height < (y0 + y1) / 2 < p["line_band_y_H"][1] * height
                and y1 - y0 < p["line_max_height_H"] * height and x1 - x0 > p["line_min_width_W"] * width):
            out.append((words, x0, y0, x1, y1))
    return out


def volume_measure(pages, p=PROPOSAL_PARAMS):
    """The printed measure: modal width of single-column body lines over the volume."""
    widths, bin_px = [], None
    for page in pages:
        if not page["words"]:
            continue
        width = page["dimensions"][0]
        bin_px = bin_px or p["measure_bin_W"] * width
        widths += [c[3] - c[1] for c in _candidate_lines(page, p) if c[3] - c[1] < 0.5 * width]
    _require(widths, "no body lines from which to measure the column width")
    bins = Counter(int(w // bin_px) for w in widths)
    best = max(sorted(bins), key=lambda k: (bins[k - 1] + bins[k] + bins[k + 1], -k))
    near = [w for w in widths if abs(w - (best + 0.5) * bin_px) <= 2 * bin_px]
    return round(statistics.median(near), 1)


def _fit_right(points, measure, p, name):
    if len(points) < p["edge_min_support"]:
        raise Hold("too-few-lines", edge=name, support=len(points))
    bin_px = p["edge_bin_M"] * measure
    bins = Counter(int(x // bin_px) for _, x in points)
    best = max(sorted(bins), key=lambda k: (bins[k - 1] + bins[k] + bins[k + 1], -k))
    near = [(y, x) for y, x in points if abs(x - (best + 0.5) * bin_px) <= p["edge_window_M"] * measure]
    if len(near) < p["edge_min_support"]:
        raise Hold("edge-no-dominant-cluster", edge=name, support=len(near))
    a, b = _theil_sen(near)
    inliers = [(y, x) for y, x in points if abs(x - (a + b * y)) <= p["edge_inlier_M"] * measure]
    if len(inliers) < p["edge_min_support"]:
        raise Hold("edge-insufficient-inliers", edge=name, support=len(inliers))
    a, b = _theil_sen(inliers)
    mad = statistics.median(abs(x - (a + b * y)) for y, x in inliers)
    if abs(b) > p["edge_max_slope"] or mad > p["edge_max_mad_M"] * measure:
        raise Hold("edge-unstable", edge=name, slope=round(b, 5), mad=round(mad, 2))
    return {"a": round(a, 3), "b": round(b, 6), "support": len(inliers), "mad": round(mad, 3)}


def _derive_left(right, starts, measure, p, name):
    window = p["left_confirm_window_M"] * measure
    confirm = [(y, x) for y, x in starts if abs(x - (_at(right, y) - measure)) <= window]
    if len(confirm) < p["left_confirm_min"]:
        # No line starts at the edge (a page of hanging-indent summary): use the
        # measure itself; classification widens its dead zone accordingly.
        return {"a": round(right["a"] - measure, 3), "b": right["b"], "support": len(confirm), "mad": None,
                "measure_px": measure, "confirmed": False}
    offset = statistics.median(_at(right, y) - x for y, x in confirm)
    mad = statistics.median(abs(_at(right, y) - x - offset) for y, x in confirm)
    if mad > p["edge_max_mad_M"] * measure:
        raise Hold("edge-unstable", edge=name, mad=round(mad, 2))
    return {"a": round(right["a"] - offset, 3), "b": right["b"], "support": len(confirm), "mad": round(mad, 3),
            "measure_px": round(offset, 2), "confirmed": True}


def measure_page(page, measure, p=PROPOSAL_PARAMS):
    """Column envelopes of one two-column page, or Hold."""
    width, height = page["dimensions"]
    if page["word_count"] < p["min_page_words"]:
        raise Hold("too-few-words", words=page["word_count"])
    cands = _candidate_lines(page, p)
    step = max(1, int(round(p["gutter_step_W"] * width)))
    lo, hi = int(p["gutter_search_W"][0] * width), int(p["gutter_search_W"][1] * width)
    scored = []
    for x in range(lo, hi, step):
        cross = sum(1 for c in cands if c[1] < x < c[3])
        left, right = sum(1 for c in cands if c[3] <= x), sum(1 for c in cands if c[1] >= x)
        scored.append(((cross, -min(left, right)), x, left, right, cross))
    if not scored:
        raise Hold("no-candidate-lines")
    key = min(s[0] for s in scored)
    xs = [s[1] for s in scored if s[0] == key]
    _, _, n_left, n_right, cross = next(s for s in scored if s[0] == key)
    gutter = (min(xs) + max(xs)) / 2
    if cross > p["gutter_max_crossings"]:
        raise Hold("gutter-crossed", crossings=cross)
    if min(n_left, n_right) < p["min_lines_per_column"]:
        raise Hold("not-two-column", left_lines=n_left, right_lines=n_right)
    edges = {}
    for side, rows in (("L", [c for c in cands if c[3] <= gutter]), ("R", [c for c in cands if c[1] >= gutter])):
        right = _fit_right([((c[2] + c[4]) / 2, c[3]) for c in rows], measure, p, side + "1")
        edges[side + "0"] = _derive_left(right, [((c[2] + c[4]) / 2, c[1]) for c in rows], measure, p, side + "0")
        edges[side + "1"] = right
    middle = height / 2
    if _at(edges["R0"], middle) - _at(edges["L1"], middle) < 2 * p["gutter_tol_M"] * measure:
        raise Hold("gutter-too-narrow")
    pitches = []
    for side in ("L", "R"):
        ys = sorted((c[2] + c[4]) / 2 for c in cands if (c[3] <= gutter if side == "L" else c[1] >= gutter))
        pitches += [b - a for a, b in zip(ys, ys[1:]) if b - a > 5]
    return {"W": width, "H": height, "gutter_x": gutter, "gutter_crossings": cross, "edges": edges,
            "pitch": round(statistics.median(pitches), 2) if pitches else round(measure / 15, 2),
            "line_height": statistics.median(c[4] - c[2] for c in cands), "measure_px": measure,
            "candidate_lines": [n_left, n_right]}


def _group_rows(fragments, tolerance):
    rows = []
    for fragment in sorted(fragments, key=lambda f: (f[0], f[1])):
        if rows and abs(fragment[0] - rows[-1]["yc"]) <= tolerance:
            rows[-1]["frags"].append(fragment)
            rows[-1]["yc"] = statistics.median(f[0] for f in rows[-1]["frags"])
        else:
            rows.append({"yc": fragment[0], "frags": [fragment]})
    out = []
    for row in rows:
        words = [w for f in sorted(row["frags"], key=lambda f: f[1]) for w in f[2]]
        out.append({"yc": row["yc"], "words": words, "x0": min(w["source_bbox"][0] for w in words),
                    "x1": max(w["source_bbox"][2] for w in words)})
    return out


def _running_head(page, m, p):
    """WORDs above the text top that form the running head (and specks above it)."""
    E, gutter, pitch, height, measure = m["edges"], m["gutter_x"], m["pitch"], m["H"], m["measure_px"]
    tol = p["full_line_tol_M"] * measure
    tops = []
    for line in _page_lines(page["words"]):
        y = statistics.median(_yc(w) for w in line)
        for a, z in (("L0", "L1"), ("R0", "R1")):
            e0, e1 = _at(E[a], y), _at(E[z], y)
            words = [w for w in line if e0 - tol <= w["source_bbox"][0] <= e1 + tol]
            if _ntok(words) < p["text_top_min_tokens"]:
                continue
            starts = abs(words[0]["source_bbox"][0] - e0) <= tol
            ends = words[-1] is line[-1] and abs(words[-1]["source_bbox"][2] - e1) <= tol
            tall = (max(w["source_bbox"][3] for w in words) - min(w["source_bbox"][1] for w in words)
                    >= p["text_top_min_height"] * m["line_height"])
            wide = words[-1]["source_bbox"][0] - words[0]["source_bbox"][0] >= p["text_top_min_width_M"] * measure
            if (starts or ends) and tall and wide:
                tops.append(y)
    limit = min((min(tops) - p["header_row_tol_P"] * pitch) if tops else float("inf"), p["header_band_H"] * height)
    clusters = []
    for word in sorted(page["words"], key=_yc):
        if _yc(word) >= limit:
            break
        if clusters and _yc(word) - clusters[-1][0] <= p["header_row_tol_P"] * pitch:
            clusters[-1][1].append(word)
        else:
            clusters.append([_yc(word), [word]])
    for k, (y, words) in enumerate(clusters):
        centres = [(w["source_bbox"][0] + w["source_bbox"][2]) / 2 for w in words]
        both = min(centres) < gutter < max(centres)
        isolated = k == len(clusters) - 1 and tops and min(tops) - y >= p["header_isolation_P"] * pitch
        if both or isolated:
            return {w["source_word_global_1"] for _, ws in clusters[:k + 1] for w in ws}
        if _ntok(words) > 2:
            break
    return set()


def propose_page(page, m, p=PROPOSAL_PARAMS):
    """Classify every WORD of a measured page and return its explicit rows, or Hold."""
    E, gutter, pitch, height, measure = m["edges"], m["gutter_x"], m["pitch"], m["H"], m["measure_px"]
    px = {key[:-2]: value * measure for key, value in p.items() if key.endswith("_M")}
    words = page["words"]
    role, uncertain, inseparable, crossings = {}, [], [], []
    header = _running_head(page, m, p)
    remaining = [w for w in sorted(words, key=_yc) if w["source_word_global_1"] not in header]
    footer = set()
    if remaining and _yc(remaining[-1]) > p["footer_band_H"] * height:
        bottom = _yc(remaining[-1])
        row = [w for w in remaining if _yc(w) >= bottom - p["header_row_tol_P"] * pitch]
        above = [w for w in remaining if _yc(w) < bottom - p["header_row_tol_P"] * pitch]
        if above and (min(w["source_bbox"][1] for w in row) - max(w["source_bbox"][3] for w in above)
                      >= p["footer_gap_P"] * pitch - m["line_height"]):
            footer = {w["source_word_global_1"] for w in row}
    for word in words:
        wid = word["source_word_global_1"]
        if wid in header or wid in footer:
            role[wid] = "header" if wid in header else "footer"
            continue
        x0, x1, y = word["source_bbox"][0], word["source_bbox"][2], _yc(word)
        L0, L1, R0, R1 = (_at(E[k], y) for k in ("L0", "L1", "R0", "R1"))
        widen_l = 0 if E["L0"]["confirmed"] else px["unconfirmed_extra"]
        widen_r = 0 if E["R0"]["confirmed"] else px["unconfirmed_extra"]
        if x0 <= L0 - px["left_margin_tol"] - widen_l:
            role[wid] = "margin-left"
        elif x0 < L0 - px["left_body_tol"]:
            uncertain.append((wid, "left-edge-dead-zone"))
        elif x0 <= L1 + px["gutter_tol"]:
            role[wid] = "body-left"
        elif x0 < R0 - px["right_start_tol"] - widen_r:
            if _nchars(word) <= p["gutter_ocr_max_chars"]:
                role[wid] = "gutter-ocr"
            else:
                uncertain.append((wid, "gutter-text"))
        elif x0 <= R1 + px["right_body_tol"]:
            role[wid] = "body-right"
        elif x0 < R1 + px["right_margin_tol"]:
            uncertain.append((wid, "right-edge-dead-zone"))
        else:
            role[wid] = "margin-right"
        if len(word["value"].split()) > 1:
            for name, edge in (("outer-left", L0 - px["left_body_tol"]), ("gutter-left", L1 + px["gutter_tol"]),
                               ("gutter-right", R0 - px["gutter_tol"]), ("outer-right", R1 + px["right_body_tol"])):
                if x0 < edge < x1:
                    crossings.append((word, name))
    lines = _page_lines(words)
    line_of = {w["source_word_global_1"]: line for line in lines for w in line}
    for word, name in crossings:
        wid = word["source_word_global_1"]
        line = line_of[wid]
        k = line.index(word)
        following = role.get(line[k + 1]["source_word_global_1"]) if k + 1 < len(line) else None
        if name == "outer-left" and following == "body-left":
            role[wid] = "body-left"
            inseparable.append((wid, "multitoken-WORD-margin-and-body-start"))
        elif name == "outer-right" and role.get(wid) == "body-right":
            inseparable.append((wid, "multitoken-WORD-body-and-right-margin"))
        else:
            uncertain.append((wid, "multitoken-WORD-crosses-" + name))
    for line in lines:
        for i, word in enumerate(line):
            wid, r, y = word["source_word_global_1"], role.get(word["source_word_global_1"]), _yc(word)
            last = i == len(line) - 1
            following = None if last else role.get(line[i + 1]["source_word_global_1"])
            if last and r == "body-right" and word["source_bbox"][2] > _at(E["R1"], y) + px["last_word_hang"]:
                inseparable.append((wid, "line-final-body-WORD-overhangs-right-edge"))
            if last and r == "body-left" and word["source_bbox"][2] > _at(E["L1"], y) + px["last_word_hang"]:
                uncertain.append((wid, "line-final-body-WORD-overhangs-gutter"))
            if last and r == "margin-left" and word["source_bbox"][2] > _at(E["L0"], y) + px["left_body_tol"]:
                inseparable.append((wid, "line-final-margin-WORD-reaches-body"))
            # A WORD of n characters is at least n * min_char wide: a lower
            # bound already crossing an envelope proves glyphs on both sides.
            if r == "margin-left" and (last or following == "body-left"):
                if word["source_bbox"][0] + _nchars(word) * px["margin_min_char"] > _at(E["L0"], y) - px["margin_body_min_gap"]:
                    if following == "body-left":
                        role[wid] = "body-left"
                        inseparable.append((wid, "margin-WORD-extent-enters-body-start"))
                    else:
                        uncertain.append((wid, "margin-WORD-extent-enters-body"))
            if r == "body-right" and word["source_bbox"][0] + _nchars(word) * px["body_min_char"] > _at(E["R1"], y) + px["margin_body_min_gap"]:
                inseparable.append((wid, "body-WORD-extent-enters-right-margin"))
            if r == "body-left" and word["source_bbox"][0] + _nchars(word) * px["body_min_char"] > _at(E["L1"], y) + px["margin_body_min_gap"]:
                uncertain.append((wid, "body-WORD-extent-enters-gutter"))
            if r == "margin-left" and following == "body-left" and role.get(wid) == "margin-left":
                body = [x for x in line[i + 1:] if role.get(x["source_word_global_1"]) == "body-left"]
                if (body[0]["source_bbox"][0] > _at(E["L0"], y) + px["margin_absorb_indent"]
                        and body[-1]["source_bbox"][2] >= _at(E["L1"], y) - px["full_line_tol"]):
                    role[wid] = "body-left"     # the full-measure line's start lies inside this WORD
                    inseparable.append((wid, "margin-WORD-absorbs-body-start"))
        sides = [role.get(w["source_word_global_1"]) for w in line]
        if "body-left" in sides and "body-right" in sides:
            first = next(w for w in line if role.get(w["source_word_global_1"]) == "body-right")
            r0 = _at(E["R0"], _yc(first))
            if not r0 - px["gutter_tol"] <= first["source_bbox"][0] <= r0 + px["merged_line_indent"]:
                uncertain.append((first["source_word_global_1"], "spanning-row-not-two-column-lines"))
    if uncertain:
        raise Hold("uncertain-WORD-role", WORDs=sorted(set(uncertain)))
    zones = defaultdict(list)
    for line in lines:
        groups = defaultdict(list)
        for word in line:
            groups[role[word["source_word_global_1"]]].append(word)
        for r, fragment in groups.items():
            zones[r].append((statistics.median(_yc(w) for w in fragment), fragment[0]["source_bbox"][0], fragment))
    rows = {r: _group_rows(f, (p["margin_row_merge_P"] if r.startswith("margin") else p["row_merge_P"]) * pitch)
            for r, f in zones.items()}
    para_start, previous = {}, None
    for column in ("body-left", "body-right"):
        e0 = E["L0"] if column == "body-left" else E["R0"]
        for i, row in enumerate(rows.get(column, [])):
            if previous is None:
                para_start[(column, i)] = True
            else:
                prior, prior_column = previous
                e1 = E["L1"] if prior_column == "body-left" else E["R1"]
                indented = (len(row["words"][0]["value"].split()) == 1
                            and row["x0"] > _at(e0, row["yc"]) + px["paragraph_indent"])
                short = prior["x1"] < _at(e1, prior["yc"]) - px["paragraph_short"]
                hyphen = prior["words"][-1]["value"].rstrip().endswith("-")
                para_start[(column, i)] = (indented or short) and not hyphen
            previous = (row, column)
    anchors, tails, block_records = defaultdict(list), defaultdict(list), []
    for side, column in (("margin-left", "body-left"), ("margin-right", "body-right")):
        body, margin = rows.get(column, []), rows.get(side, [])
        starts = [body[i]["yc"] for i in range(len(body)) if para_start.get((column, i))]
        gaps = [b["yc"] - a["yc"] for a, b in zip(margin, margin[1:]) if b["yc"] - a["yc"] < pitch]
        small = (p["margin_block_gap_factor"] * statistics.median(gaps)) if len(gaps) >= 2 else p["margin_block_gap_default_P"] * pitch
        blocks = []
        for row in margin:
            if blocks:
                last_y = blocks[-1][-1]["yc"]
                section = any(last_y + 0.6 * pitch < s <= row["yc"] + 0.6 * pitch for s in starts)
                if row["yc"] - last_y <= small or (row["yc"] - last_y <= p["margin_block_max_gap_P"] * pitch and not section):
                    blocks[-1].append(row)
                    continue
            blocks.append([row])
        for block in blocks:
            y = block[0]["yc"]
            kind = "column-end"
            if body:
                index = min(range(len(body)), key=lambda i: (abs(body[i]["yc"] - y), i))
                kind = "nearest-row"
                order = [(0, "paragraph-start")]
                if index + 1 < len(body) and abs(body[index + 1]["yc"] - y) <= pitch:
                    order.append((-1, "paragraph-start-below"))
                order += [(k, "paragraph-start-above") for k in range(1, p["margin_anchor_back_rows"] + 1)]
                for back, label in order:
                    if 0 <= index - back < len(body) and para_start.get((column, index - back)):
                        index, kind = index - back, label
                        break
                anchors[(column, index)].append(block)
            else:
                index = None
                tails[column].append(block)
            block_records.append({"side": side, "anchor_row": index, "anchor_kind": kind, "rows": len(block),
                                  "first_WORD": block[0]["words"][0]["source_word_global_1"]})
    plan = []

    def emit(r, brk, ws):
        plan.append([CODE_OF[r], brk, [w["source_word_global_1"] for w in ws]])

    for row in rows.get("header", []):
        emit("header", "l" if plan else "p", row["words"])
    for column, side in (("body-left", "margin-left"), ("body-right", "margin-right")):
        for i, row in enumerate(rows.get(column, [])):
            for block in anchors.get((column, i), []):
                for j, mrow in enumerate(block):
                    emit(side, "l" if j else "p", mrow["words"])
            emit(column, "p" if para_start[(column, i)] or (plan and plan[-1][0] in {"ML", "MR"}) else "l", row["words"])
        for block in tails.get(column, []):
            for j, mrow in enumerate(block):
                emit(side, "l" if j else "p", mrow["words"])
    for r in ("gutter-ocr", "footer"):
        for row in rows.get(r, []):
            emit(r, "p", row["words"])
    planned = [wid for _, _, ids in plan for wid in ids]
    _require(sorted(planned) == sorted(w["source_word_global_1"] for w in words) and len(set(planned)) == len(planned),
             "internal proposal does not conserve WORDs")
    seen, recorded = set(), []
    for wid, reason in inseparable:
        if wid not in seen:
            seen.add(wid)
            recorded.append([wid, reason])
    counts = Counter()
    for code, _, ids in plan:
        counts[ROLE_CODES[code]] += len(ids)
    return {"rows": [[code, brk, _runs(ids)] for code, brk, ids in plan], "role_WORD_counts": dict(sorted(counts.items())),
            "inseparable_WORDs": sorted(recorded), "margin_blocks": block_records,
            "header_rows": [_runs(ids) for code, _, ids in plan if code == "H"],
            "paragraph_breaks": sum(1 for key, value in para_start.items() if value) - (1 if para_start else 0)}


def _runs(ids):
    out = []
    for wid in ids:
        if out and out[-1][1] + 1 == wid:
            out[-1][1] = wid
        else:
            out.append([wid, wid])
    return out


def _input_map(root, path):
    mapped = json.loads(_path(root, path, True).read_bytes(), object_pairs_hook=_object_pairs, parse_constant=_constant)
    _fields(mapped, {"schema", "inputs"}, name="input map")
    _require(mapped["schema"] == "triptych-bullarium-geometry-input-map/v1" and isinstance(mapped["inputs"], dict),
             "unknown runtime input-map schema")
    return mapped["inputs"]


def _record_pin(root, record_path):
    record = tomllib.loads(_path(root, record_path, True).read_text())
    _require(record.get("record_type") == "artifact" and SHA.fullmatch(str(record.get("sha256", ""))),
             "source record is not a hashed artifact record")
    pin = {key: record[key] for key in ("sha256", "byte_size")}
    pin["artifact_id"] = record["id"]
    if record.get("storage") == "tracked" and record.get("path"):
        pin["path"] = record["path"]
    if "source_url" in record:
        pin["source_url"] = record["source_url"]
    return pin


def _source_records(root, volume, txt_record, xml_record):
    if volume is not None:
        _require(txt_record is None and xml_record is None, "choose --volume or explicit source records, not both")
        catalog = json.loads(_path(root, CATALOG, True).read_bytes())
        matches = [v for v in catalog["volumes"] if str(v["volume"]) == str(volume)]
        _require(len(matches) == 1, "volume is absent from the Bullarium catalog")
        artifacts = matches[0]["container"]["artifacts"]
        return artifacts["ocr"]["manifest"], artifacts["xml"]["manifest"], matches[0]["volume"]
    _require(txt_record and xml_record, "propose requires --volume or both --source-txt-record and --source-xml-record")
    return txt_record, xml_record, None


def propose(root, out_dir, *, volume=None, source_txt_record=None, source_xml_record=None, input_map=None):
    """Write recipe.json (v2) and running-heads.tsv under scratch/build; never source records."""
    root = Path(root).resolve()
    out = _destination(root, out_dir)
    txt_record, xml_record, volume_key = _source_records(root, volume, source_txt_record, source_xml_record)
    pins = {"source_txt": _record_pin(root, txt_record), "source_xml": _record_pin(root, xml_record)}
    inputs = _input_map(root, input_map) if input_map else {}
    locations = {pin["artifact_id"]: inputs[pin["artifact_id"]] for pin in pins.values() if pin["artifact_id"] in inputs}
    frozen = {}
    raw, xml = (_pin(root, pins[name], frozen, locations) for name in ("source_txt", "source_xml"))

    class _All:
        def __contains__(self, leaf):
            return True

    pages, count = _xml_pages(xml, raw, _tokens(raw), _All())
    measure = volume_measure(pages)
    entries, statuses = [], Counter()
    heads = []
    for page in pages:
        entry = {"leaf": page["leaf"], "object_ordinal_1": page["artifact_page"],
                 "source_lf_range_1": page["source_lf_range_1"]}
        if not page["word_count"]:
            entry["status"] = "empty"
        else:
            try:
                m = measure_page(page, measure)
                result = propose_page(page, m)
            except Hold as hold:
                entry.update(status="held", hold={"reason": hold.reason, "detail": json.loads(json.dumps(hold.detail))})
            else:
                entry.update(status="reordered", measurements=m, **result)
        statuses[entry["status"]] += 1
        entries.append(entry)
        values = {w["source_word_global_1"]: w["value"] for w in page["words"]}
        if entry["status"] == "reordered":
            head = " | ".join(" ".join(values[i].strip() for a, z in row for i in range(a, z + 1)) for row in entry["header_rows"])
        else:
            head = "(page " + entry["status"] + ")"
        heads.append(f"{page['leaf']}\t{entry['status']}\t{head}")
    # A page sharing a raw LF line with its neighbour cannot be replaced by an
    # LF-enclosed span; the replay would refuse it, so it is held here.
    spans = [(i, e["source_lf_range_1"]) for i, e in enumerate(entries) if e["source_lf_range_1"]]
    for (i, a), (j, b) in zip(spans, spans[1:]):
        if a[1] >= b[0]:
            for k in (i, j):
                if entries[k]["status"] == "reordered":
                    statuses["reordered"] -= 1
                    statuses["held"] += 1
                    entries[k] = {key: entries[k][key] for key in ("leaf", "object_ordinal_1", "source_lf_range_1")}
                    entries[k].update(status="held", hold={"reason": "raw-LF-line-shared-with-neighbouring-page", "detail": {}})
    _require(all(_sha(path.read_bytes()) == digest for path, digest in frozen.items()), "pinned input changed during proposal")
    recipe = {"schema": SCHEMA_V2, **pins, "pages": entries,
              "proposal": {"algorithm": PROPOSAL_ALGORITHM, "params": PROPOSAL_PARAMS, "measure_px": measure,
                           "source_WORDs": count, "page_status_counts": dict(sorted(statuses.items())),
                           "proposer_sha256": _sha(Path(__file__).read_bytes()),
                           "limits": "Coordinates, token counts and character counts only; no wording is read or changed. "
                                     "Held pages keep raw OCR. Recorded inseparable WORDs mix body and marginal glyphs."}}
    if volume_key is not None:
        recipe["volume"] = volume_key
    products = {"recipe.json": (json.dumps(recipe, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode(),
                "running-heads.tsv": ("\n".join(heads) + "\n").encode()}
    out.mkdir(parents=True, exist_ok=True)
    for name, data in products.items():
        path = out / name
        _require(not path.exists() or path.read_bytes() == data, "refusing to overwrite a differing proposal: " + name)
        if not path.exists():
            path.write_bytes(data)
    return {"recipe_sha256": _sha(products["recipe.json"]), "page_status_counts": recipe["proposal"]["page_status_counts"],
            "measure_px": measure, "inseparable_WORDs": sum(len(e.get("inseparable_WORDs", [])) for e in entries)}


def _replay_products(root, replay_dir):
    replay = _path(root, replay_dir)
    validation = json.loads((replay / "validation.json").read_bytes())
    for name, pin in validation["outputs"].items():
        _require(_sha((replay / name).read_bytes()) == pin["sha256"], "replay product hash mismatch: " + name)
    words = []
    with gzip.open(replay / "changed-word-map.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            words.append(json.loads(line))
    pages = json.loads((replay / "page-map.json").read_bytes())["pages"]
    return replay, validation, words, pages


def map_units(root, recipe_path, replay_dir, out_path, *, catalog_path=CATALOG, withdrawals_path=WITHDRAWALS):
    """Locate every catalog unit of the volume in the derivative through WORD identity."""
    root = Path(root).resolve()
    target = _destination(root, out_path)
    recipe_file = _path(root, recipe_path)
    recipe = json.loads(recipe_file.read_bytes())
    _require(recipe.get("schema") == SCHEMA_V2 and "volume" in recipe, "map-units requires a Bullarium v2 recipe")
    replay, validation, words, pages = _replay_products(root, replay_dir)
    _require(validation.get("recipe_sha256") == _sha(recipe_file.read_bytes()), "replay was not built from this recipe")
    catalog_bytes = _path(root, catalog_path, True).read_bytes()
    withdrawals_bytes = _path(root, withdrawals_path, True).read_bytes()
    catalog, withdrawals = json.loads(catalog_bytes), json.loads(withdrawals_bytes)
    inseparable = {wid for page in recipe["pages"] for wid, _ in page.get("inseparable_WORDs", [])}
    by_raw, by_out = defaultdict(list), defaultdict(list)
    for word in words:
        item = {"id": word["source_word_global_1"], "role": word["role"], "ol": word["output_lf_range_1"][0], "leaf": word["leaf"],
                "sl": word["source_txt_physical_lines"]}
        for n in word["source_txt_physical_lines"]:
            by_raw[n].append(item)
        by_out[item["ol"]].append(item)
    for page in pages:   # unchanged pages: raw line n is output line n + offset
        if page["serialization"] == "unchanged-raw-ocr" and page["source_lf_range_1"]:
            delta = page["output_lf_range_1"][0] - page["source_lf_range_1"][0]
            for n in range(page["source_lf_range_1"][0], page["source_lf_range_1"][1] + 1):
                item = {"id": "raw-line-%d" % n, "role": "unchanged", "ol": n + delta, "leaf": page["leaf"], "sl": [n]}
                by_raw[n].append(item)
                by_out[n + delta].append(item)
    body_roles, margin_roles = {"body-left", "body-right", "unchanged"}, {"margin-left", "margin-right"}
    affected = {a["unit_id"]: a for a in withdrawals["affected_units"]}
    sha_txt = recipe["source_txt"]["sha256"]
    out_lines = sorted(by_out)
    results = []
    for unit in (u for u in catalog["units"] if u["volume"] == recipe["volume"]):
        active = unit.get("active_render_selection")
        if isinstance(active, dict):
            ranges, source_sha = active["physical_line_ranges"], active.get("sha256")
        elif isinstance(unit.get("review"), dict) and unit["review"].get("physical_line_ranges"):
            ranges, source_sha = unit["review"]["physical_line_ranges"], unit["review"].get("artifact_sha256", unit["artifact_sha256"])
        else:
            ranges, source_sha = unit["physical_line_ranges"], unit["artifact_sha256"]
        row = {"unit_id": unit["id"], "status": unit["status"], "old_ranges": ranges,
               "withdrawn_confirmed_fusion": unit["id"] in affected}
        if source_sha != sha_txt:
            results.append({**row, "category": "hold:selection-not-on-raw-ocr"})
            continue
        inside = lambda n: any(a <= n <= z for a, z in ranges)
        selected = {}
        for a, z in ranges:
            for n in range(a, z + 1):
                for item in by_raw.get(n, ()):
                    selected[item["id"]] = item
        partial = sorted(i["id"] for i in selected.values() if not all(inside(n) for n in i["sl"]))
        body = [i for i in selected.values() if i["role"] in body_roles]
        margin = [i for i in selected.values() if i["role"] in margin_roles]
        if not body:
            results.append({**row, "category": "hold:no-body-WORDs"})
            continue
        lo, hi = min(i["ol"] for i in body), max(i["ol"] for i in body)
        foreign_body = foreign_margin = 0
        furniture = set()
        for n in out_lines:
            if lo <= n <= hi:
                for item in by_out[n]:
                    if item["id"] in selected:
                        continue
                    if item["role"] in body_roles:
                        foreign_body += 1
                    elif item["role"] in margin_roles:
                        foreign_margin += 1
                    else:
                        furniture.add(n)
        lead = [i for i in margin if i["ol"] < lo and all(x["id"] in selected or x["role"] not in body_roles | margin_roles
                                                          for n in out_lines if i["ol"] <= n < lo for x in by_out[n])]
        escaped = [i for i in margin if not lo <= i["ol"] <= hi and i not in lead]
        start = min([lo] + [i["ol"] for i in lead])
        mixed = sorted(i["id"] for i in selected.values() if i["id"] in inseparable)
        held = sorted({i["leaf"] for i in selected.values() if i["role"] == "unchanged"})
        loci = []
        if unit["id"] in affected:
            for a, z in affected[unit["id"]]["source_order_evidence"]["affected_physical_line_ranges"]:
                loci += [n for n in range(a, z + 1) if any(i["role"] == "unchanged" for i in by_raw.get(n, ()))]
        if partial:
            category = "hold:partial-WORD-selection"
        elif foreign_body:
            category = "hold:body-not-contiguous"
        elif loci:
            category = "hold:reviewed-fusion-on-held-page"
        elif mixed:
            category = "hold:inseparable-WORD"
        elif foreign_margin or escaped:
            category = "review:margin-ownership-at-boundary"
        else:
            category = "clean-with-unchanged-pages" if held else "clean"
        results.append({**row, "category": category, "new_physical_line_ranges": [[start, hi]],
                        "furniture_lines_inside": sorted(furniture), "foreign_body_WORDs": foreign_body,
                        "foreign_margin_WORDs": foreign_margin, "escaped_margin_WORDs": len(escaped),
                        "partial_WORDs": partial, "inseparable_WORDs": mixed, "unchanged_leaves": held,
                        "reviewed_fusion_lines_on_held_pages": sorted(set(loci))})
    loci_report = Counter()
    for unit_id, a in affected.items():
        if not any(r["unit_id"] == unit_id for r in results):
            continue
        for x, z in a["source_order_evidence"]["affected_physical_line_ranges"]:
            items = [i for n in range(x, z + 1) for i in by_raw.get(n, ())]
            roles = {i["role"] for i in items}
            loci_report["held-page" if "unchanged" in roles else "marginal-WORDs-separated" if roles & margin_roles
                        else "inseparable-WORD-recorded" if any(i["id"] in inseparable for i in items) else "no-marginal-WORD"] += 1
    mixed_lines = sum(1 for items in by_raw.values() if {i["role"] for i in items} & {"body-left", "body-right"}
                      and {i["role"] for i in items} & margin_roles)
    report = {"schema": MAPPING_SCHEMA, "volume": recipe["volume"],
              "inputs": {"recipe_sha256": _sha(recipe_file.read_bytes()), "derivative_sha256": validation["hybrid_sha256"],
                         "catalog_sha256": _sha(catalog_bytes), "withdrawals_sha256": _sha(withdrawals_bytes)},
              "summary": {"units": len(results), "categories": dict(sorted(Counter(r["category"] for r in results).items())),
                          "withdrawn_confirmed_fusion_categories": dict(sorted(Counter(
                              r["category"] for r in results if r["withdrawn_confirmed_fusion"]).items())),
                          "reviewed_fusion_loci": dict(sorted(loci_report.items())),
                          "raw_LF_lines_mixing_body_and_margin_roles": mixed_lines},
              "limits": "Mechanical WORD-identity mapping. Only 'clean' units are registration candidates; every other "
                        "category is a hold or a review item. Margin ownership follows the block's anchor row.",
              "units": results}
    data = (json.dumps(report, ensure_ascii=False, sort_keys=True, indent=1) + "\n").encode()
    _require(not target.exists() or target.read_bytes() == data, "refusing to overwrite a differing unit mapping")
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(data)
    return report["summary"]


def _artifact(root, edition_dir, edition_id, key, filename, payload, raw_record, kind, media_type, notes, retrieved,
              derived_from=None):
    """Stage one immutable artifact (payload and record) under the volume edition."""
    digest = _sha(payload)
    folder = edition_dir / "artifacts" / f"{key}-{digest[:12]}"
    record = {"schema": 1, "record_type": "artifact", "id": f"artifact.{edition_id.removeprefix('edition.')}.{key}-{digest[:12]}",
              "edition_id": edition_id, "artifact_type": kind, "media_type": media_type, "storage": "tracked",
              "rights_status": raw_record["rights_status"], "rights_basis": raw_record["rights_basis"],
              "rights_jurisdiction": raw_record.get("rights_jurisdiction", "United States"),
              "path": str((folder / filename).relative_to(root)), "sha256": digest, "byte_size": len(payload),
              "retrieved": retrieved,
              "provenance": "Deterministic product of tools/bullarium geometry; whole bytes hashed and replayable.",
              "notes": notes}
    if derived_from:
        record.update(derived_from=derived_from, transformation=notes)
    if "source_url" in raw_record and media_type == "text/plain":
        record["source_url"] = raw_record["source_url"]
    if media_type == "text/plain":
        record.update(indexable=True, encoding="utf-8")
    return record, folder / filename, folder / "artifact.toml", payload


def _map_lines(raw_lines, by_raw, ranges):
    out = sorted({ol for n in raw_lines for ol, role in by_raw.get(n, ()) if role in {"body-left", "body-right"}})
    _require(out and all(any(a <= n <= z for a, z in ranges) for n in out), "attribution lines do not map inside the new range")
    return [out[0], out[-1]]


def register(root, recipe_path, replay_dir, mapping_path, units_path, revision, *, input_map=None):
    """Register the derivative and admit explicitly selected clean units through `bullarium admit`.

    Writes are append-only: artifact payloads and records are absent-or-identical;
    the catalog gains container declarations only; segments, editions and
    manifest rows are staged by the existing admission path with its own
    absent-or-identical rules.  Raw artifacts, prior segments and the withdrawal
    inventory are read, never written.
    """
    import _bullarium as bullarium
    _require(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", str(revision)), "revision requires explicit whole-second UTC")
    root = Path(root).resolve()
    recipe_file = _path(root, recipe_path)
    recipe = json.loads(recipe_file.read_bytes())
    _require(recipe.get("schema") == SCHEMA_V2 and "volume" in recipe, "register requires a Bullarium v2 recipe")
    replay = _path(root, replay_dir)
    info = check(root, recipe_path, replay_dir, input_map=input_map)    # full independent replay
    mapping = json.loads(_path(root, mapping_path, True).read_bytes())
    _require(mapping.get("schema") == MAPPING_SCHEMA and mapping["inputs"]["derivative_sha256"] == info["hybrid_sha256"]
             and mapping["inputs"]["recipe_sha256"] == info["recipe_sha256"], "unit mapping is not for this derivative")
    selected = json.loads(_path(root, units_path, True).read_bytes())
    _require(isinstance(selected, dict) and selected.get("schema") == "triptych-bullarium-reading-order-selection/v1"
             and isinstance(selected.get("units"), list) and selected["units"]
             and len(set(selected["units"])) == len(selected["units"]), "unit selection requires an explicit nonempty list")
    rows = {r["unit_id"]: r for r in mapping["units"]}
    for unit_id in selected["units"]:
        _require(rows.get(unit_id, {}).get("category") == "clean",
                 "only units mapped 'clean' may be registered: " + unit_id)
    catalog_file = _path(root, CATALOG, True)
    catalog = json.loads(catalog_file.read_bytes())
    current = {u["id"]: u for u in catalog["units"]}
    for unit_id in selected["units"]:
        unit = current.get(unit_id)
        active = (unit or {}).get("active_render_selection")
        ranges = active["physical_line_ranges"] if isinstance(active, dict) else (unit or {}).get("review", {}).get(
            "physical_line_ranges", (unit or {}).get("physical_line_ranges"))
        _require(unit and unit["volume"] == recipe["volume"] and ranges == rows[unit_id]["old_ranges"]
                 and unit["artifact_sha256"] == recipe["source_txt"]["sha256"], "unit selection changed since mapping: " + unit_id)
    volume = next(v for v in catalog["volumes"] if v["volume"] == recipe["volume"])
    container = volume["container"]
    raw_record_path = _path(root, container["artifacts"]["ocr"]["manifest"], True)
    raw_record = tomllib.loads(raw_record_path.read_text())
    _require(raw_record["id"] == recipe["source_txt"]["artifact_id"] and raw_record["sha256"] == recipe["source_txt"]["sha256"],
             "recipe source is not this volume's raw OCR")
    edition_dir = _path(root, container["edition_path"], True)
    edition_id = container["edition_id"]
    recipe_bytes = recipe_file.read_bytes()
    pieces = {
        "recipe": _artifact(root, edition_dir, edition_id, "reading-order-recipe", "recipe.json.gz",
                            gzip.compress(recipe_bytes, mtime=0), raw_record, "coordinate-reading-order-recipe",
                            "application/gzip", f"Explicit v2 reading-order recipe (decoded SHA256 {_sha(recipe_bytes)}) "
                            f"for raw OCR {raw_record['id']} and XML {recipe['source_xml']['artifact_id']}.", revision[:10]),
        "page_map": _artifact(root, edition_dir, edition_id, "reading-order-page-map", "page-map.json",
                              (replay / "page-map.json").read_bytes(), raw_record, "coordinate-reading-order-page-map",
                              "application/json", "Per-page source and output byte/LF spans of the reading-order derivative.", revision[:10]),
        "validation": _artifact(root, edition_dir, edition_id, "reading-order-validation", "validation.json",
                                (replay / "validation.json").read_bytes(), raw_record, "coordinate-reading-order-validation",
                                "application/json", "Replay receipt: input pins, output hashes and the conservation checks.", revision[:10]),
    }
    hybrid = (replay / "hybrid.txt").read_bytes()
    recipe_id = pieces["recipe"][0]["id"]
    pieces["order"] = _artifact(root, edition_dir, edition_id, "reading-order", "hybrid.txt", hybrid, raw_record,
                                "coordinate-reading-order-ocr", "text/plain",
                                f"Deterministic output of tools/bullarium geometry from recipe {recipe_id}; source XML "
                                f"{recipe['source_xml']['artifact_id']} (SHA256 {recipe['source_xml']['sha256']}). Every native "
                                "WORD appears exactly once with its value unchanged; only page order, roles and inter-WORD "
                                "whitespace change. Marginal summaries are separate TAB-led blocks at their anchors; held "
                                "pages keep raw OCR bytes.", revision[:10], derived_from=raw_record["id"])
    staged = []
    for name, (record, payload_path, record_path, payload) in pieces.items():
        bullarium.check_source_write(payload_path, payload)
        bullarium.check_source_write(record_path, bullarium.record_bytes(record))
        staged.append((payload_path, payload, record_path, record))
    keys = {"order": "reading_order", "recipe": "reading_order_recipe", "page_map": "reading_order_page_map",
            "validation": "reading_order_validation"}
    declarations = {}
    for name, (record, payload_path, record_path, _) in pieces.items():
        key = f"{keys[name]}_{record['sha256'][:12]}"
        declaration = {"id": record["id"], "manifest": str(record_path.relative_to(root)), "sha256": record["sha256"]}
        if name == "order":
            declaration["line_map_path"] = str(pieces["page_map"][1].relative_to(root))
        _require(container["artifacts"].get(key, declaration) == declaration, "a container declaration already differs: " + key)
        declarations[key] = declaration
    order_record = pieces["order"][0]
    by_raw = defaultdict(list)
    with gzip.open(replay / "changed-word-map.jsonl.gz", "rt", encoding="utf-8") as stream:
        for line in stream:
            word = json.loads(line)
            for n in word["source_txt_physical_lines"]:
                by_raw[n].append((word["output_lf_range_1"][0], word["role"]))
    units = {u["id"]: u for u in catalog["units"]}
    reviews = []
    for unit_id in selected["units"]:
        unit, row = units[unit_id], rows[unit_id]
        history = [r for r in [unit.get("review")] + list(reversed(unit.get("review_history", [])))
                   if isinstance(r, dict) and r.get("decision") in {"admit", "fragment"} and r.get("source_attribution_lines")]
        _require(history, "a registered unit requires its prior admitted boundary review: " + unit_id)
        prior = history[0]
        ranges = row["new_physical_line_ranges"]
        a, z = prior["source_attribution_lines"]
        item = {"unit_id": unit_id + ".reading-order", "parent_unit_id": unit_id, "reading_selection_variant_of": unit_id,
                "canonical_work_id": unit["work_id"],
                "identity_evidence": {"existing_work_id": unit["work_id"],
                                      "basis": "Same printed act: every native WORD of the prior reviewed raw extent maps to this "
                                               "contiguous reading-order range through WORD identity."},
                "source_artifact_id": order_record["id"], "artifact_sha256": order_record["sha256"],
                "physical_line_ranges": ranges, "decision": prior["decision"],
                "printed_attribution": prior["printed_attribution"], "title": prior["title"],
                "source_attribution_lines": _map_lines(range(a, z + 1), by_raw, ranges),
                "review_note": f"Reading-order selection of the reviewed raw extent {unit_id} {prior['physical_line_ranges']}, "
                               "mapped mechanically through native WORD identity: body WORDs contiguous, no foreign body or "
                               "marginal WORD inside, no partial or inseparable WORD. " + prior.get("review_note", ""),
                "reviewed_extent": "WORD-identity mapping of the prior reviewed extent; volume evidence gate on native page "
                                   "images; no whole-act image collation.",
                "reader_source_note": "Reading order follows native word coordinates; the printing's marginal summaries are "
                                      "kept as separate blocks beside the sections they annotate; held pages, if any, keep "
                                      "raw OCR order."}
        for key in ("language", "language_label", "document_type", "extent_kind", "source_extent_limit"):
            if key in prior:
                item[key] = prior[key]
        if prior["decision"] == "fragment":     # the missing-content statement stays first
            item["reader_source_note"] = " ".join(filter(None, [prior.get("reader_source_note", prior.get("source_extent_limit")),
                                                                item["reader_source_note"]]))
        reviews.append(item)
    review_bytes = bullarium.json_bytes({"schema": "triptych-bullarium-boundary-reviews/v1", "reviews": reviews})
    review_path = replay / "register-review.json"
    _require(not review_path.exists() or review_path.read_bytes() == review_bytes, "a differing register review already exists")
    # Every check passed: write artifacts, then declare them, then admit.
    for payload_path, payload, record_path, record in staged:
        bullarium.write_source(payload_path, payload)
        bullarium.record(record_path, record)
    if any(container["artifacts"].get(k) != d for k, d in declarations.items()):
        container["artifacts"].update(declarations)
        bullarium.write(catalog_file, bullarium.json_bytes(catalog))
    bullarium.write(review_path, review_bytes)
    result = bullarium.admit(root, [review_path], revision, GEOMETRY_MANIFEST, GEOMETRY_FRAGMENT_MANIFEST)
    return {"derivative_artifact_id": order_record["id"], "derivative_sha256": order_record["sha256"],
            "artifacts": [record["id"] for _, _, _, record in staged], "admitted_units": len(reviews),
            "additional_reading_selections": result.get("additional_reading_selections")}


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise GeometryError(message)


VERB_EXAMPLES = {
    "propose": (
        Example("tools/bullarium geometry propose --volume 4 --out ../outside --json",
                ('{"code":"input","error":"input path must be canonical repository-relative without traversal","status":"error","v":1}',),
                "An output outside scratch/build is refused before any source is read."),
        Example("tools/bullarium geometry propose --volume 4 --out ../outside",
                ("bullarium geometry propose: input path must be canonical repository-relative without traversal",),
                "The same refusal in ordinary text."),
    ),
    "map-units": (
        Example("tools/bullarium geometry map-units --recipe .scratch/absent/recipe.json --replay .scratch/absent --out ../outside.json --json",
                ('{"code":"input","error":"input path must be canonical repository-relative without traversal","status":"error","v":1}',),
                "The mapping destination is checked before the recipe, replay or catalog is read."),
        Example("tools/bullarium geometry map-units --recipe .scratch/absent/recipe.json --replay .scratch/absent --out ../outside.json",
                ("bullarium geometry map-units: input path must be canonical repository-relative without traversal",),
                "The same refusal in ordinary text."),
    ),
    "register": (
        Example("tools/bullarium geometry register --recipe .scratch/absent/recipe.json --replay .scratch/absent --mapping .scratch/absent/mapping.json --units .scratch/absent/units.json --revision invalid --json",
                ('{"code":"input","error":"revision requires explicit whole-second UTC","status":"error","v":1}',),
                "An invalid revision is refused before replay, catalog reads or any source write."),
        Example("tools/bullarium geometry register --recipe .scratch/absent/recipe.json --replay .scratch/absent --mapping .scratch/absent/mapping.json --units .scratch/absent/units.json --revision invalid",
                ("bullarium geometry register: revision requires explicit whole-second UTC",),
                "The same refusal in ordinary text."),
    ),
}
VERB_HELP = {
    "propose": "Propose an explicit v2 reading-order recipe from native WORD geometry (scratch/build output only).",
    "map-units": "Map every catalog unit of the volume onto a replayed derivative through WORD identity.",
    "register": "Register a replayed derivative and admit explicitly selected 'clean' units via bullarium admit.",
}


def _verb_main(verb, argv, examples):
    parser = _Parser(prog="bullarium geometry " + verb, description=VERB_HELP[verb])
    chosen = examples.get("geometry " + verb) if isinstance(examples, dict) else None
    with_examples(parser, chosen or VERB_EXAMPLES[verb])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    if verb == "propose":
        parser.add_argument("--volume", help="Bullarium catalog volume (1-24 or appendix)")
        parser.add_argument("--source-txt-record", help="explicit raw OCR artifact.toml (another series)")
        parser.add_argument("--source-xml-record", help="explicit DjVu XML artifact.toml (another series)")
        parser.add_argument("--input-map", help="triptych-bullarium-geometry-input-map/v1 locating cached whole inputs")
        parser.add_argument("--out", required=True)
    elif verb == "map-units":
        parser.add_argument("--recipe", required=True)
        parser.add_argument("--replay", required=True, help="output directory of `bullarium geometry --recipe`")
        parser.add_argument("--out", required=True)
        parser.add_argument("--catalog", default=CATALOG)
        parser.add_argument("--withdrawals", default=WITHDRAWALS)
    else:
        for name in ("recipe", "replay", "mapping", "units", "revision"):
            parser.add_argument("--" + name, required=True)
        parser.add_argument("--input-map")
    try:
        args = parser.parse_args(argv)
        if verb == "propose":
            volume = None if args.volume is None else ("appendix" if args.volume == "appendix" else int(args.volume))
            info = propose(args.root, args.out, volume=volume, source_txt_record=args.source_txt_record,
                           source_xml_record=args.source_xml_record, input_map=args.input_map)
        elif verb == "map-units":
            info = map_units(args.root, args.recipe, args.replay, args.out, catalog_path=args.catalog,
                             withdrawals_path=args.withdrawals)
        else:
            info = register(args.root, args.recipe, args.replay, args.mapping, args.units, args.revision,
                            input_map=args.input_map)
        result = {"v": 1, "status": "ok", **info}
        print(json.dumps(result, sort_keys=True, separators=(",", ":")) if args.json else
              "\n".join(f"{key}: {value}" for key, value in result.items()))
        return 0
    except (ValueError, OSError, KeyError, TypeError, StopIteration, expat.ExpatError, tomllib.TOMLDecodeError) as error:
        print(json.dumps({"v": 1, "status": "error", "code": "input", "error": str(error)}, sort_keys=True, separators=(",", ":"))
              if "--json" in argv else f"bullarium geometry {verb}: {error}", file=sys.stderr)
        return 2


def main(argv=None, examples=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    prefix, rest = [], argv
    if rest[:1] == ["--root"] and len(rest) > 2:
        prefix, rest = rest[:2], rest[2:]
    elif rest and rest[0].startswith("--root="):
        prefix, rest = rest[:1], rest[1:]
    if rest and rest[0] in VERB_HELP:
        return _verb_main(rest[0], prefix + rest[1:], examples)
    parser = _Parser(prog="bullarium geometry", description=__doc__ + " Verbs `propose`, `map-units` and `register` "
                     "(see `bullarium geometry VERB --help`) propose, map and register v2 reading-order recipes.")
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
