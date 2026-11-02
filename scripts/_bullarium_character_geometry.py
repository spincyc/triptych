"""Replay explicitly reviewed page components using exact native OCR characters.

This separate engine never relaxes the indivisible-WORD geometry engine. A
nominated WORD may instead be represented by complete native charParams only
after its position and complete value have been checked against both sources.
"""
from __future__ import annotations

from collections import Counter
import gzip
import hashlib
import io
import json
import mmap
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlsplit
from xml.parsers import expat
import xml.etree.ElementTree as ET

import _bullarium_geometry as words

SCHEMA = "triptych-bullarium-character-geometry-recipe/v1"
INPUT_MAP_SCHEMA = "triptych-bullarium-character-geometry-input-map/v1"
SOURCES = ("source_txt", "source_xml", "source_abbyy_gz", "source_abbyy_xml", "source_scandata")
PIN_FIELDS = {"sha256", "byte_size", "sha1", "artifact_id", "source_url"}
WORD_FIELDS = {"source_word_global_1", "source_word_page_1", "source_line_global_1", "source_line_page_1",
               "source_xml_byte_range_0", "value", "coords", "source_bbox",
               "source_txt_token_byte_ranges_0", "source_txt_physical_lines"}
CHAR_FIELDS = {"native_char_global_1", "native_char_page_1", "native_line_global_1", "native_line_page_1",
               "source_xml_byte_range_0", "value", "bbox"}
LIMITS = ["Native OCR character values are not corrected, restored or authenticated.",
          "Explicit source-role assignments and component order require independent source review.",
          "Unchanged raw bytes and unreviewed original order retain their recorded defects.",
          "Page replay proves no whole-act repair, admission, juridical weight or image collation.",
          "Whole upstream hashes do not establish rights clearance of excluded or unreviewed upstream surfaces; their native text is never emitted."]


class CharacterGeometryError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise CharacterGeometryError(message)


def _fields(value, required, optional=(), owner="record"):
    _require(isinstance(value, dict) and set(required) <= set(value)
             and set(value) <= set(required) | set(optional), owner + " has missing or unsupported fields")


def _sha(value):
    return hashlib.sha256(value).hexdigest()


def _nonwhite(value):
    return "".join(value.split())


def _json(path):
    try:
        return json.loads(path.read_bytes(), object_pairs_hook=words._object_pairs,
                          parse_constant=words._constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CharacterGeometryError("character recipe/input map is not readable JSON") from error


def _file_hash(path):
    size, digest, sha1 = 0, hashlib.sha256(), hashlib.sha1()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(chunk)
            digest.update(chunk)
            sha1.update(chunk)
    return {"byte_size": size, "sha256": digest.hexdigest(), "sha1": sha1.hexdigest()}


def _pin(root, pin, input_map, frozen):
    _fields(pin, {"sha256", "byte_size"}, PIN_FIELDS | {"path"}, "source pin")
    _require(isinstance(pin["sha256"], str) and words.SHA.fullmatch(pin["sha256"])
             and type(pin["byte_size"]) is int and pin["byte_size"] > 0,
             "whole source requires SHA256 and positive byte_size")
    if "sha1" in pin:
        _require(isinstance(pin["sha1"], str) and re.fullmatch(r"[a-f0-9]{40}", pin["sha1"]), "invalid source SHA1")
    if "artifact_id" in pin:
        _require(isinstance(pin["artifact_id"], str) and re.fullmatch(r"artifact\.[a-z0-9.-]+", pin["artifact_id"]),
                 "invalid source artifact identity")
    if "source_url" in pin:
        value = pin["source_url"]
        _require(isinstance(value, str) and not any(c.isspace() for c in value), "invalid source URL")
        url = urlsplit(value)
        _require(url.scheme in {"http", "https"} and url.netloc and not url.username and not url.password,
                 "source URL must be public HTTP(S)")
    location = input_map.get(pin.get("artifact_id"), input_map.get(pin["sha256"], pin.get("path")))
    _require(location is not None, "source unavailable; provide an explicit runtime input_map")
    path = words._path(root, location, True)
    observed = _file_hash(path)
    _require(all(observed[k] == pin[k] for k in ("sha256", "byte_size"))
             and ("sha1" not in pin or observed["sha1"] == pin["sha1"]), "whole source hash or byte size mismatch")
    frozen[path] = observed
    return path


def _public_pin(pin):
    # Neither recipe cache hints nor runtime override locations belong in maps.
    return {k: pin[k] for k in sorted(PIN_FIELDS & set(pin))}


def _frozen(frozen):
    _require(all(path.is_file() and _file_hash(path) == pin for path, pin in frozen.items()),
             "pinned input changed during character replay")


def _secure_xml(parser):
    def forbidden(*args):
        raise CharacterGeometryError("DOCTYPE/entities are not permitted in native or scandata XML")
    parser.StartDoctypeDeclHandler = forbidden
    parser.ExternalEntityRefHandler = forbidden
    parser.XmlDeclHandler = lambda version, encoding, standalone: _require(
        encoding is None or encoding.lower().replace("-", "") == "utf8", "source XML must use UTF8")


def _scandata(data):
    parser = expat.ParserCreate()
    _secure_xml(parser)
    parser.Parse(data, True)
    tree = ET.fromstring(data)
    pages = tree.findall("./pageData/page")
    _require(pages, "scandata requires a complete pageData sequence")
    rows = []
    for index, page in enumerate(pages):
        leaf = page.attrib.get("leafNum")
        _require(isinstance(leaf, str) and re.fullmatch(r"\d+", leaf) and int(leaf) == index,
                 "scandata leaves must be the complete ordered zero-based scan sequence")
        access = page.findtext("addToAccessFormats")
        _require(access in {"true", "false"}, "scandata requires explicit access-format flags")
        try:
            dims = [int(page.findtext("cropBox/w")), int(page.findtext("cropBox/h"))]
        except (TypeError, ValueError) as error:
            raise CharacterGeometryError("scandata requires explicit crop dimensions") from error
        _require(all(n > 0 for n in dims), "scandata crop dimensions must be positive")
        rows.append({"leaf": index, "native_page_ordinal_1": index + 1,
                     "access": access == "true", "crop_dimensions": dims,
                     "page_type": page.findtext("pageType"), "page_number": page.findtext("pageNumber")})
    return rows


def _native_pages(path, selected):
    """Stream the complete native XML; retain details only for nominated pages."""
    parser = expat.ParserCreate()
    parser.buffer_text = True
    _secure_xml(parser)
    pages, page, char, in_line = [], None, None, False
    char_count = line_count = declared = 0
    with path.open("rb") as stream, mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
        def start(name, attrs):
            nonlocal page, char, char_count, line_count, declared, in_line
            if name == "document":
                _require(declared == 0, "nested native document")
                declared = int(attrs.get("pagesCount", "0"))
                _require(declared > 0, "native document requires pagesCount")
            elif name == "page":
                _require(page is None, "nested native page")
                dims = [int(attrs.get(k, "0")) for k in ("width", "height")]
                _require(all(n > 0 for n in dims), "native page dimensions must be positive")
                page = {"native_page_ordinal_1": len(pages) + 1, "dimensions": dims,
                        "source_xml_byte_range_0": [parser.CurrentByteIndex, None],
                        "chars": [], "char_count": 0, "line_count": 0,
                        "nonwhite_codepoints": 0, "digest": hashlib.sha256()}
            elif name == "line":
                _require(page is not None and char is None and not in_line, "native line has no unique page")
                in_line = True
                line_count += 1
                page["line_count"] += 1
            elif name == "charParams":
                _require(page is not None and in_line and char is None, "native character has no unique line/page")
                char_count += 1
                page["char_count"] += 1
                if page["native_page_ordinal_1"] not in selected:
                    char = {"value": ""}
                    return
                begin = parser.CurrentByteIndex
                end = words._tag_end(data, begin)
                box = [int(attrs.get(k, "-1")) for k in ("l", "t", "r", "b")]
                _require(0 <= box[0] <= box[2] and 0 <= box[1] <= box[3], "invalid native character bbox")
                char = {"native_char_global_1": char_count, "native_char_page_1": page["char_count"],
                        "native_line_global_1": line_count, "native_line_page_1": page["line_count"],
                        "source_xml_byte_range_0": [begin, None], "value": "", "bbox": box,
                        "source_attrs": dict(attrs), "tag_end": end,
                        "selfclosing": data[begin:end].endswith(b"/>")}

        def text(value):
            if char is not None:
                char["value"] += value

        def end(name):
            nonlocal page, char, in_line
            if name == "charParams":
                content = _nonwhite(char["value"])
                page["nonwhite_codepoints"] += len(content)
                page["digest"].update(content.encode())
                if page["native_page_ordinal_1"] in selected:
                    stop = char.pop("tag_end") if char.pop("selfclosing") else words._tag_end(data, parser.CurrentByteIndex)
                    char.pop("tag_end", None)
                    char["source_xml_byte_range_0"][1] = stop
                    page["chars"].append(char)
                char = None
            elif name == "line":
                _require(in_line and char is None, "unterminated native line character")
                in_line = False
            elif name == "page":
                _require(page is not None and char is None and not in_line, "unterminated native page character")
                page["source_xml_byte_range_0"][1] = words._tag_end(data, parser.CurrentByteIndex)
                page["nonwhite_sha256"] = page.pop("digest").hexdigest()
                pages.append(page)
                page = None

        parser.StartElementHandler, parser.EndElementHandler, parser.CharacterDataHandler = start, end, text
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            parser.Parse(chunk, False)
        parser.Parse(b"", True)
    _require(declared == len(pages), "native pagesCount disagrees with complete XML")
    return pages, char_count


def _inputs(root, recipe_path, input_map):
    path = words._path(root, recipe_path)
    recipe = _json(path)
    _fields(recipe, {"schema", *SOURCES, "excluded_scan_leaves", "changed_pages", "expected_output"},
            {"notes", "source_evidence_pins", "limitations"}, "character recipe")
    _require(recipe["schema"] == SCHEMA, "unknown character geometry recipe schema")
    _require(isinstance(recipe.get("notes", ""), str), "notes require a prose string")
    _require(isinstance(recipe.get("limitations", []), list)
             and all(isinstance(v, str) for v in recipe.get("limitations", [])), "limitations require prose strings")
    frozen = {path: _file_hash(path)}
    if isinstance(input_map, (str, Path)):
        mp = words._path(root, input_map)
        mapped = _json(mp)
        _fields(mapped, {"schema", "inputs"}, owner="runtime input map")
        _require(mapped["schema"] == INPUT_MAP_SCHEMA, "unknown character input-map schema")
        input_map = mapped["inputs"]
        frozen[mp] = _file_hash(mp)
    input_map = {} if input_map is None else input_map
    _require(isinstance(input_map, dict), "runtime input_map must be an object")
    allowed = {pin.get(k) for name in SOURCES for pin in [recipe[name]] if isinstance(pin, dict)
               for k in ("sha256", "artifact_id")}
    _require(all(isinstance(k, str) and k in allowed for k in input_map), "unknown runtime source identity")
    paths = {name: _pin(root, recipe[name], input_map, frozen) for name in SOURCES}
    evidence = recipe.get("source_evidence_pins", {})
    _require(isinstance(evidence, dict), "source_evidence_pins must be a path/SHA256 object")
    evidence_pins = []
    for name, digest in evidence.items():
        _require(isinstance(digest, str) and words.SHA.fullmatch(digest), "evidence must have a complete SHA256")
        ep = words._path(root, name, True)
        observed = _file_hash(ep)
        _require(observed["sha256"] == digest, "source evidence hash mismatch")
        frozen[ep] = observed
        evidence_pins.append({"sha256": digest, "byte_size": observed["byte_size"]})
    _require(isinstance(recipe["changed_pages"], list) and recipe["changed_pages"], "changed_pages must be nonempty")
    selected, specifications = set(), {}
    for spec in recipe["changed_pages"]:
        _fields(spec, {"leaf", "object_ordinal_1", "native_page_ordinal_1", "source_byte_range_0", "source_lf_range_1",
                       "native_page_byte_range_0", "nonwhite_fingerprint", "word_pins", "split_words", "components",
                       "before", "replacement_sha256"}, owner="character page")
        _require(type(spec["leaf"]) is int and spec["leaf"] >= 0 and spec["leaf"] not in specifications,
                 "changed leaf is invalid or duplicated")
        _require(type(spec["native_page_ordinal_1"]) is int and spec["native_page_ordinal_1"] > 0,
                 "native page ordinal must be positive")
        _require(type(spec["object_ordinal_1"]) is int and spec["object_ordinal_1"] > 0,
                 "DjVu OBJECT ordinal must be positive")
        for name in ("source_byte_range_0", "native_page_byte_range_0"):
            words._pair(spec[name], name)
        words._pair(spec["source_lf_range_1"], "source LF range", 1)
        selected.add(spec["native_page_ordinal_1"])
        specifications[spec["leaf"]] = spec
    digest, count = hashlib.sha256(), 0
    with gzip.open(paths["source_abbyy_gz"], "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
            count += len(chunk)
            _require(count <= recipe["source_abbyy_xml"]["byte_size"], "gzip decoded bytes exceed pinned native XML size")
    _require(count == recipe["source_abbyy_xml"]["byte_size"]
             and digest.hexdigest() == recipe["source_abbyy_xml"]["sha256"],
             "whole compressed ABBYY does not decode to the pinned complete native XML")
    native, char_count = _native_pages(paths["source_abbyy_xml"], selected)
    scan = _scandata(paths["source_scandata"].read_bytes())
    _require(len(scan) == len(native), "scandata and native complete page sequences disagree")
    excluded = [{**p, "native_XML_byte_range_0": native[p["native_page_ordinal_1"] - 1]["source_xml_byte_range_0"],
                 "native_nonwhite_codepoints": native[p["native_page_ordinal_1"] - 1]["nonwhite_codepoints"],
                 "scope": "metadata-only; no upstream character text emitted or rights clearance inferred"}
                for p in scan if not p["access"]]
    _require(isinstance(recipe["excluded_scan_leaves"], list)
             and all(type(n) is int for n in recipe["excluded_scan_leaves"])
             and recipe["excluded_scan_leaves"] == [p["leaf"] for p in excluded],
             "explicit excluded scan leaves disagree with complete scandata")
    raw, xml = paths["source_txt"].read_bytes(), paths["source_xml"].read_bytes()
    tokens = words._tokens(raw)
    pages, word_count = words._xml_pages(xml, raw, tokens, specifications)
    _require([p["leaf"] for p in pages] == [p["leaf"] for p in scan if p["access"]],
             "DjVu leaf sequence disagrees with explicit scandata access leaves")
    _require(set(specifications) <= {p["leaf"] for p in pages}, "changed leaf absent from DjVu/scandata")
    for page in pages:
        scanned = scan[page["leaf"]]
        np = native[scanned["native_page_ordinal_1"] - 1]
        _require(page["dimensions"] == np["dimensions"] == scanned["crop_dimensions"],
                 "native/DjVu/scandata access-page dimensions disagree")
        a, z = page["source_token_range_0"]
        content = "".join(t[2] for t in tokens[a:z])
        fingerprint = {"sha256": _sha(content.encode()), "codepoints": len(content)}
        _require(np["nonwhite_sha256"] == fingerprint["sha256"]
                 and np["nonwhite_codepoints"] == fingerprint["codepoints"],
                 "whole native/DjVu page nonwhite fingerprint mismatch")
        page["native_page_ordinal_1"] = np["native_page_ordinal_1"]
        page["nonwhite_fingerprint"] = fingerprint
        if page["leaf"] in specifications:
            spec = specifications[page["leaf"]]
            _require(fingerprint["codepoints"] > 0, "empty text fingerprints cannot establish a changed-page alignment")
            for key, value in (("object_ordinal_1", page["artifact_page"]), ("native_page_ordinal_1", np["native_page_ordinal_1"]),
                               ("source_byte_range_0", page["source_byte_range_0"]), ("source_lf_range_1", page["source_lf_range_1"]),
                               ("native_page_byte_range_0", np["source_xml_byte_range_0"]), ("nonwhite_fingerprint", fingerprint)):
                _require(spec[key] == value, "changed page alignment pin mismatch: " + key)
    return recipe, raw, tokens, pages, native, specifications, frozen, evidence_pins, word_count, char_count, excluded


def _word_pin(actual, nominated):
    _fields(nominated, WORD_FIELDS, {"source_attrs"}, "WORD pin")
    _require(words._json_bytes(nominated) == words._json_bytes({k: actual[k] for k in nominated}),
             "exact original WORD pin mismatch")


def _character_pin(actual, nominated):
    _fields(nominated, CHAR_FIELDS, {"source_attrs"}, "native character pin")
    _require(words._json_bytes(nominated) == words._json_bytes({k: actual[k] for k in nominated}),
             "exact native character value/bbox/byte pin mismatch")


def _binding(word, spec, chars, positions, word_span):
    _fields(spec, {"source_word_global_1", "native_chars", "whitespace_policy"}, owner="split WORD")
    _require(spec["whitespace_policy"] in {"exact", "unicode-whitespace-only"}, "unknown WORD whitespace policy")
    declared = spec["native_chars"]
    _require(isinstance(declared, list) and declared, "split WORD needs complete native characters")
    ids = [c.get("native_char_global_1") for c in declared if isinstance(c, dict)]
    _require(len(ids) == len(declared) and all(type(n) is int for n in ids)
             and ids == list(range(ids[0], ids[0] + len(ids))), "split WORD native character IDs must be a contiguous source sequence")
    a, z = word_span
    required = {number for number, (x, y) in positions.items() if x < z and y > a}
    _require(required and required <= set(ids), "split WORD dropped position-aligned source characters")
    for nominated in declared:
        number = nominated["native_char_global_1"]
        _require(number in chars, "split character belongs to a different native page")
        actual = chars[number]
        _character_pin(actual, nominated)
        x, y = positions[number]
        _require((a <= x < y <= z) if x != y else (a <= x <= z),
                 "native charParams crosses a WORD boundary or belongs to another source position")
    value = "".join(chars[n]["value"] for n in ids)
    _require(_nonwhite(value) == _nonwhite(word["value"]), "complete native character binding changed original WORD characters")
    _require(spec["whitespace_policy"] != "exact" or value == word["value"],
             "complete native binding differs from exact original WORD whitespace")
    return ids, value


def _components(page, native, spec):
    original = {w["source_word_global_1"]: w for w in page["words"]}
    pins = spec["word_pins"]
    _require(isinstance(pins, list) and len(pins) == len(original), "changed page omitted or duplicated WORD pins")
    seen = set()
    for pin in pins:
        number = pin.get("source_word_global_1") if isinstance(pin, dict) else None
        _require(number in original and number not in seen, "WORD pin absent, duplicated or on another page")
        _word_pin(original[number], pin)
        seen.add(number)
    chars = {c["native_char_global_1"]: c for c in native["chars"]}
    positions, cursor = {}, 0
    for c in native["chars"]:
        stop = cursor + len(_nonwhite(c["value"]))
        positions[c["native_char_global_1"]] = cursor, stop
        cursor = stop
    word_spans, cursor = {}, 0
    for w in page["words"]:
        stop = cursor + len(_nonwhite(w["value"]))
        word_spans[w["source_word_global_1"]] = cursor, stop
        cursor = stop
    _require(isinstance(spec["split_words"], list), "split_words must list explicitly nominated WORDs")
    bindings, bound_chars = {}, set()
    for split in spec["split_words"]:
        number = split.get("source_word_global_1") if isinstance(split, dict) else None
        _require(type(number) is int and number in original and number not in bindings,
                 "split WORD absent, invalid or duplicated")
        ids, value = _binding(original[number], split, chars, positions, word_spans[number])
        _require(not bound_chars.intersection(ids), "native character is bound to multiple WORDs")
        bound_chars.update(ids)
        bindings[number] = {"ids": ids, "value": value, "policy": split["whitespace_policy"]}
    _require(words._whitespace(spec["before"]), "page prefix may contain only whitespace")
    payload, maps, seen_words, seen_chars = bytearray(spec["before"].encode()), [], set(), set()
    _require(isinstance(spec["components"], list) and spec["components"], "ordered components must be nonempty")
    for component in spec["components"]:
        _fields(component, {"kind", "source_word_global_1", "value", "role", "flags", "after"},
                {"native_char_global_ids_1"}, "page component")
        number = component["source_word_global_1"]
        _require(type(number) is int and number in original, "component WORD belongs to another page")
        _require(isinstance(component["role"], str) and component["role"] in words.ROLES and isinstance(component["flags"], list)
                 and all(isinstance(v, str) and v for v in component["flags"]), "component requires typed role and flags")
        _require(isinstance(component["after"], str) and component["after"]
                 and all(c == "\n" for c in component["after"]), "each component requires its own following LF")
        kind, native_chars = component["kind"], []
        if kind == "word":
            _require("native_char_global_ids_1" not in component and number not in bindings and number not in seen_words,
                     "whole WORD duplicated or also nominated for character splitting")
            value = original[number]["value"]
            seen_words.add(number)
        elif kind == "native-chars":
            ids = component.get("native_char_global_ids_1")
            _require(number in bindings and isinstance(ids, list) and ids
                     and all(type(n) is int for n in ids) and ids == sorted(set(ids)),
                     "native component needs unique ascending indivisible character IDs")
            _require(set(ids) <= set(bindings[number]["ids"]) and not seen_chars.intersection(ids),
                     "native character omitted, duplicated or from another WORD")
            native_chars = [{k: chars[n][k] for k in sorted(CHAR_FIELDS)} for n in ids]
            value = "".join(chars[n]["value"] for n in ids)
            seen_chars.update(ids)
        else:
            raise CharacterGeometryError("unknown component kind")
        _require(component["value"] == value, "component mutated exact source characters")
        begin = len(payload)
        payload.extend(value.encode())
        maps.append({"kind": kind, "source_word_global_1": number, "value": value,
                     "source_WORD_xml_byte_range_0": original[number]["source_xml_byte_range_0"],
                     "source_WORD_coords": original[number]["coords"],
                     "source_txt_token_byte_ranges_0": original[number]["source_txt_token_byte_ranges_0"],
                     "native_chars": native_chars, "role": component["role"], "flags": component["flags"],
                     "relative_output_byte_range_0": [begin, len(payload)]})
        payload.extend(component["after"].encode())
    _require(seen_words == set(original) - set(bindings) and seen_chars == bound_chars,
             "page components dropped or duplicated an original WORD/native character")
    payload = bytes(payload)
    _require(Counter(_nonwhite(payload.decode())) == Counter(_nonwhite("".join(w["value"] for w in page["words"]))),
             "page nonwhite source character conservation failed")
    _require(_sha(payload) == spec["replacement_sha256"], "expected page replacement hash mismatch")
    return payload, maps, [{"source_word_global_1": n, "native_char_global_ids_1": b["ids"],
                            "whitespace_policy": b["policy"], "original_WORD_value_sha256": _sha(original[n]["value"].encode()),
                            "native_value_sha256": _sha(b["value"].encode())} for n, b in sorted(bindings.items())]


def _derive(root, recipe_path, input_map):
    recipe, raw, tokens, pages, native, specs, frozen, evidence, word_count, char_count, excluded = _inputs(root, recipe_path, input_map)
    patches = []
    for page in pages:
        if page["leaf"] not in specs:
            continue
        a, z = page["source_byte_range_0"]
        first, last = page["source_token_range_0"]
        _require((first == 0 or tokens[first - 1][1] <= a) and (last == len(tokens) or tokens[last][0] >= z),
                 "changed page LF span includes a neighboring page token")
        spec = specs[page["leaf"]]
        payload, components, bindings = _components(page, native[page["native_page_ordinal_1"] - 1], spec)
        patches.append((page, payload, components, bindings))
    output, chunks, component_map, cursor = bytearray(), [], [], 0

    def copied(stop):
        nonlocal cursor
        if cursor < stop:
            begin, data = len(output), raw[cursor:stop]
            output.extend(data)
            chunks.append({"kind": "copied-raw-ocr", "source_byte_range_0": [cursor, stop],
                           "output_byte_range_0": [begin, len(output)], "sha256": _sha(data)})
            cursor = stop

    for page, payload, components, bindings in sorted(patches, key=lambda p: p[0]["source_byte_range_0"][0]):
        a, z = page["source_byte_range_0"]
        _require(cursor <= a < z, "changed page source spans overlap")
        copied(a)
        begin = len(output)
        output.extend(payload)
        page["output_byte_range_0"] = [begin, len(output)]
        page["split_words"] = bindings
        chunks.append({"kind": "explicit-character-page-patch", "leaf": page["leaf"], "source_byte_range_0": [a, z],
                       "output_byte_range_0": page["output_byte_range_0"], "source_sha256": _sha(raw[a:z]),
                       "output_sha256": _sha(payload)})
        for component in components:
            x, y = component.pop("relative_output_byte_range_0")
            component.update(leaf=page["leaf"], object_ordinal_1=page["artifact_page"],
                             native_page_ordinal_1=page["native_page_ordinal_1"],
                             output_utf8_byte_range_0=[begin + x, begin + y])
            component_map.append(component)
        cursor = z
    copied(len(raw))
    output = bytes(output)
    _require(Counter(_nonwhite(output.decode())) == Counter(_nonwhite(raw.decode())),
             "whole output nonwhite character conservation failed")
    expected = recipe["expected_output"]
    _fields(expected, {"sha256", "byte_size"}, owner="expected output")
    _require(type(expected["byte_size"]) is int and expected["byte_size"] == len(output)
             and expected["sha256"] == _sha(output), "expected whole output hash/size mismatch")
    newlines = [m.start() for m in re.finditer(b"\n", output)]
    for component in component_map:
        a, z = component["output_utf8_byte_range_0"]
        _require(output[a:z] == component["value"].encode(), "component output changed")
        component["output_lf_range_1"] = [words._line(newlines, a), words._line(newlines, max(a, z - 1))]
    _require(all(a["output_lf_range_1"][1] < b["output_lf_range_1"][0]
                 for a, b in zip(component_map, component_map[1:]) if a["leaf"] == b["leaf"]),
             "components share physical output LF lines")
    copied_chunks = [c for c in chunks if c["kind"] == "copied-raw-ocr"]
    for page in pages:
        page.pop("words")
        if page["leaf"] not in specs:
            span = page["source_byte_range_0"]
            page["output_byte_range_0"] = None
            if span:
                chunk = next((c for c in copied_chunks if c["source_byte_range_0"][0] <= span[0]
                              <= span[1] <= c["source_byte_range_0"][1]), None)
                _require(chunk is not None, "unchanged page escaped exact copied chunks")
                delta = chunk["output_byte_range_0"][0] - chunk["source_byte_range_0"][0]
                page["output_byte_range_0"] = [n + delta for n in span]
        span = page["output_byte_range_0"]
        page["output_lf_range_1"] = [words._line(newlines, span[0]), words._line(newlines, span[1] - 1)] if span else None
        page["serialization"] = "explicit-component-per-line" if page["leaf"] in specs else "unchanged-raw-ocr"
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=buf, mode="wb", mtime=0, compresslevel=6) as stream:
        for component in component_map:
            stream.write((json.dumps(component, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode())
    products = {"hybrid.txt": output,
                "byte-map.json": words._json_bytes({"schema": "triptych-bullarium-character-byte-map/v1", "chunks": chunks,
                                                    "source_sha256": _sha(raw), "output_sha256": _sha(output)}),
                "page-map.json": words._json_bytes({"schema": "triptych-bullarium-character-page-map/v1", "pages": pages}),
                "component-map.jsonl.gz": buf.getvalue()}
    info = {"schema": "triptych-bullarium-character-witness/v1", "generator": "bullarium-character-geometry", "generator_version": 1,
            "recipe_sha256": frozen[words._path(root, recipe_path)]["sha256"],
            "sources": {n: _public_pin(recipe[n]) for n in SOURCES}, "evidence": sorted(evidence, key=lambda p: p["sha256"]),
            "source_WORDs": word_count, "source_native_charParams": char_count, "native_pages": len(native),
            "source_pages": len(pages), "changed_pages": len(patches), "changed_components": len(component_map),
            "excluded_upstream_pages": excluded, "native_character_output_scope": sorted(specs),
            "split_WORDs": sum(len(p[3]) for p in patches), "hybrid_sha256": _sha(output), "hybrid_bytes": len(output),
            "roles": dict(sorted(Counter(c["role"] for c in component_map).items())),
            "limitations": LIMITS + recipe.get("limitations", []),
            "checks": {n: True for n in ("complete_source_hashes", "whole_gzip_decoded_XML_identity", "whole_TXT_XML_tokens",
                "all_access_leaves_match_scandata_sequence", "all_access_page_native_nonwhite_fingerprints",
                "every_original_WORD_whole_or_completely_bound", "native_charParams_indivisible_and_position_aligned",
                "each_split_source_character_exactly_once", "whole_nonwhite_character_conservation", "unchanged_raw_bytes_identical",
                "all_components_independent_LF_bounds", "excluded_native_text_never_emitted", "no_runtime_paths_or_OBJECT_attributes")},
            "outputs": {n: {"sha256": _sha(b), "byte_size": len(b)} for n, b in products.items()}}
    if "artifact_id" in recipe["source_txt"]:
        info["derived_from"] = recipe["source_txt"]["artifact_id"]
    products["validation.json"] = words._json_bytes(info)
    return products, info, frozen


def _destination(root, out_dir):
    out = words._path(root, out_dir)
    _require(out.is_relative_to(root / ".scratch"), "character products must remain under repository .scratch")
    return out


def build(root, recipe_path, out_dir, input_map=None):
    """Build deterministic scratch products from fully pinned source components."""
    root = Path(root).resolve()
    out = _destination(root, out_dir)
    products, info, frozen = _derive(root, recipe_path, input_map)
    for name, data in products.items():
        path = out / name
        _require(path not in frozen and (not path.exists() or path.read_bytes() == data),
                 "refusing to overwrite input or differing character product: " + name)
    _frozen(frozen)
    out.mkdir(parents=True, exist_ok=True)
    for name, data in products.items():
        path = out / name
        if path.exists():
            continue
        with tempfile.NamedTemporaryFile(dir=out, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        try:
            try:
                os.link(temporary, path)
            except FileExistsError:
                _require(path.read_bytes() == data, "character output appeared with differing bytes")
        finally:
            temporary.unlink()
    return info


def check(root, recipe_path, out_dir, input_map=None):
    """Independently replay all inputs and compare every byte of every product."""
    root = Path(root).resolve()
    out = _destination(root, out_dir)
    products, info, frozen = _derive(root, recipe_path, input_map)
    for name, data in products.items():
        _require((out / name).is_file() and (out / name).read_bytes() == data, "character product mismatch: " + name)
    _frozen(frozen)
    return info


def prepare(root, recipe_path, input_map=None):
    """Return verified page/character pins; infer no roles, order or admissions.

    The same recipe envelope/pins are used, but expected_output, WORD/component
    arrays and expected page hashes may be placeholders until reviewed. All
    whole inputs, native/scandata alignment and raw page extents still validate.
    """
    root = Path(root).resolve()
    recipe, raw, tokens, pages, native, specs, frozen, evidence, word_count, char_count, excluded = _inputs(root, recipe_path, input_map)
    selected = []
    for page in pages:
        if page["leaf"] in specs:
            np = native[page["native_page_ordinal_1"] - 1]
            selected.append({"page": page, "native_page": {k: v for k, v in np.items() if k != "chars"},
                             "native_chars": np["chars"]})
    _frozen(frozen)
    return {"schema": "triptych-bullarium-character-preparation/v1", "sources": {n: _public_pin(recipe[n]) for n in SOURCES},
            "source_WORDs": word_count, "source_native_charParams": char_count, "pages": selected,
            "excluded_upstream_pages": excluded,
            "limitations": LIMITS}
