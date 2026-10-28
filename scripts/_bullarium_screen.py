"""Screen pinned raw OCR geometry for research leads; never clear a source."""
from __future__ import annotations

import argparse
import bisect
from collections import Counter, defaultdict
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import statistics
import sys
import tomllib
from xml.etree import ElementTree
from xml.parsers import expat

import _bullarium_geometry as geometry
from _tooling import Example, with_examples

ROOT = Path(__file__).resolve().parents[1]
MAP_SCHEMA = "triptych-bullarium-screen-input-map/v1"
SCHEMA = "triptych-bullarium-geometry-screen/v1"
CACHE_SCHEMA = "triptych-bullarium-screen-native-cache/v1"
FRONTIER_SCHEMA = "triptych-bullarium-unflagged-active-frontier/v1"
THRESHOLDS = {"min_line_tokens": 5, "min_line_width_W": .22, "max_line_width_W": .48,
              "min_line_y_H": .08, "max_line_y_H": .92, "max_line_height_H": .04,
              "min_lane_lines": 12, "max_edge_MAD_W": .04, "outward_gap_W": .002,
              "min_core_WORDs": 2, "backward_jump_H": .12, "hyphen_max_intervening_WORDs": 24}
LIMITS = ["Candidate prose bands are numerical fits, not confirmed body or marginal ownership.",
          "Flags are research leads, not act dispositions or proof of a source-order defect.",
          "NO_SIGNAL_NOT_CLEAR does not establish correct order, caption ownership or source clearance.",
          "No OCR correction, word joining, new transcription, admission, withdrawal, authentication or image collation."]
WORD_FIELDS = ["source_word_global_1", "source_word_page_1", "source_line_global_1", "source_line_page_1",
               "source_xml_byte_range_0", "value", "coords", "source_bbox",
               "source_txt_token_byte_ranges_0", "source_txt_physical_lines"]
PAGE_FIELDS = ["artifact_page", "leaf", "dimensions", "source_token_range_0", "source_word_range_1",
               "word_count", "line_count", "source_lf_range_1", "source_byte_range_0"]
EXAMPLES = (
    Example("tools/bullarium screen --frontier ../outside --catalog src/sources/papal-documents/bullarium-catalog.json --input-map .scratch/bullarium_reconstruction/geometry_screen_engine/input-map.json --out .scratch/bullarium_reconstruction/geometry_screen_engine/preflight --json",
            ('{"code":"input","error":"input path must be canonical repository-relative without traversal","status":"error","v":1}',),
            "Traversal is refused before input reads, source extraction or output writes."),
    Example("tools/bullarium screen --frontier ../outside --catalog src/sources/papal-documents/bullarium-catalog.json --input-map .scratch/bullarium_reconstruction/geometry_screen_engine/input-map.json --out .scratch/bullarium_reconstruction/geometry_screen_engine/preflight",
            ("bullarium screen: input path must be canonical repository-relative without traversal",),
            "The same deterministic traversal refusal in ordinary text."),
)


class ScreenError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise ScreenError(message)


def _bytes(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _hash(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def _path(root, value):
    return geometry._path(root, value, relative=True)


def _json(path, label):
    try:
        return json.loads(path.read_bytes(), object_pairs_hook=geometry._object_pairs,
                          parse_constant=geometry._constant)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ScreenError("screen " + label + " is not readable JSON") from error


def _pin(path):
    return {"sha256": _hash(path), "byte_size": path.stat().st_size}


def _matches_pin(path, pin):
    _require(isinstance(pin, dict) and set(pin) == {"sha256", "byte_size"}
             and isinstance(pin["sha256"], str) and geometry.SHA.fullmatch(pin["sha256"])
             and type(pin["byte_size"]) is int and pin["byte_size"] >= 0, "invalid screen input pin")
    _require(path.is_file() and _pin(path) == pin, "screen input hash or byte size mismatch")


def _write(path, data):
    """Derived evidence is absent-or-identical; never replace an old run."""
    _require(path.resolve() == path, "screen/cache output cannot pass through symlinks")
    _require(not path.exists() or (path.is_file() and path.read_bytes() == data),
             "refusing to replace existing screen/cache bytes")
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("xb") as stream:
                stream.write(data)
        except FileExistsError:
            _require(path.read_bytes() == data, "concurrent screen/cache bytes disagree")


def _gzip(data):
    stream = io.BytesIO()
    with gzip.GzipFile(fileobj=stream, mode="wb", filename="", mtime=0) as compressed:
        compressed.write(data)
    return stream.getvalue()


def _ranges(value):
    _require(isinstance(value, list) and value, "selection needs nonempty physical_line_ranges")
    previous = 0
    for pair in value:
        _require(isinstance(pair, list) and len(pair) == 2 and all(type(n) is int for n in pair)
                 and previous < pair[0] <= pair[1], "physical_line_ranges must be sorted, positive and disjoint")
        previous = pair[1]
    return value


def _volume(value):
    _require(value == "appendix" or type(value) is int and 1 <= value <= 24, "unknown screen volume")
    return str(value)


def _selected(line, ranges):
    return any(a <= line <= z for a, z in ranges)


def _fingerprint(words):
    return _sha(_bytes([part for word in words for part in word["value"].split()]))


def _compact(page):
    return {**{key: page[key] for key in PAGE_FIELDS}, "WORD_fields": WORD_FIELDS,
            "WORDs": [[word[key] for key in WORD_FIELDS] for word in page["words"]],
            "full_page_tokens_sha256": _fingerprint(page["words"]),
            "full_page_token_count": sum(len(word["value"].split()) for word in page["words"])}


def _expand(page):
    _require(isinstance(page, dict) and set(page) == set(PAGE_FIELDS) |
             {"WORD_fields", "WORDs", "full_page_tokens_sha256", "full_page_token_count"}
             and page["WORD_fields"] == WORD_FIELDS and isinstance(page["WORDs"], list),
             "native page cache shape mismatch")
    _require(all(isinstance(row, list) and len(row) == len(WORD_FIELDS) for row in page["WORDs"]),
             "native page cache WORD shape mismatch")
    words = [dict(zip(WORD_FIELDS, row)) for row in page["WORDs"]]
    _require(len(words) == page["word_count"] and _fingerprint(words) == page["full_page_tokens_sha256"]
             and sum(len(w["value"].split()) for w in words) == page["full_page_token_count"],
             "native page cache full-page token fingerprint mismatch")
    if words:
        _require([w["source_word_global_1"] for w in words] ==
                 list(range(page["source_word_range_1"][0], page["source_word_range_1"][1] + 1))
                 and [w["source_word_page_1"] for w in words] == list(range(1, len(words) + 1)),
                 "native page cache WORD ordinal mismatch")
    return {**{key: page[key] for key in PAGE_FIELDS}, "words": words,
            "full_page_tokens_sha256": page["full_page_tokens_sha256"]}


def _record(root, entry, expected_id, frozen):
    path = _path(root, entry)
    data = path.read_bytes()
    record = tomllib.loads(data.decode())
    _require(record.get("schema") == 1 and record.get("record_type") == "artifact"
             and record.get("id") == expected_id, "catalog source record identity mismatch")
    frozen[path] = _sha(data)
    return record


def _source(root, volume, inputs, frozen):
    container = volume["container"]
    pins, locations = {}, {}
    for name in ("ocr", "xml"):
        entry = container["artifacts"][name]
        record = _record(root, entry["manifest"], entry["id"], frozen)
        _require(record.get("sha256") == entry["sha256"], "catalog source record hash disagrees")
        pin = {key: record[key] for key in ("sha256", "byte_size")}
        pin["artifact_id"] = record["id"]
        if "source_url" in record:
            pin["source_url"] = record["source_url"]
        location = inputs.get(record["id"], inputs.get(record["sha256"], record.get("path")))
        _require(location is not None, "source bytes unavailable; supply explicit runtime input-map path")
        path = _path(root, location)
        _matches_pin(path, {key: pin[key] for key in ("sha256", "byte_size")})
        frozen[path] = pin["sha256"]
        pins["source_txt" if name == "ocr" else "source_xml"] = pin
        locations[record["id"]] = location
    line_path = _path(root, container["line_map_path"])
    line_record = _record(root, str((line_path.parent / "artifact.toml").relative_to(root)),
                          container["line_map_id"], frozen)
    _matches_pin(line_path, {key: line_record[key] for key in ("sha256", "byte_size")})
    frozen[line_path] = line_record["sha256"]
    line_map = _json(line_path, "line map")
    _require(line_map.get("schema") == "triptych-bullarium-line-map/v1"
             and line_map.get("ocr_sha256") == pins["source_txt"]["sha256"]
             and line_map.get("xml_sha256") == pins["source_xml"]["sha256"]
             and isinstance(line_map.get("pages"), list), "line map source hashes or schema mismatch")
    return pins, locations, line_map, {key: line_record[key] for key in ("sha256", "byte_size")}


def _page_token_intervals(line_map):
    """Exact page intervals come from the pinned map's per-OBJECT counts."""
    intervals, refs, cursor = {}, {}, 0
    for ordinal, page in enumerate(line_map["pages"], 1):
        _require(isinstance(page, dict) and type(page.get("artifact_page")) is int
                 and page["artifact_page"] == ordinal, "line map OBJECT sequence must be exactly 1..N")
        leaf, count = page.get("leaf"), page.get("tokens")
        _require(type(leaf) is int and leaf >= 0 and leaf not in refs, "line map scan leaves must be unique nonnegative integers")
        _require(type(count) is int and count >= 0, "line map page tokens must be nonnegative integers")
        intervals[leaf], refs[leaf] = [cursor, cursor + count], page
        cursor += count
    _require(type(line_map.get("token_count")) is int and line_map["token_count"] == cursor,
             "line map complete token total disagrees with page counts")
    return intervals, refs, cursor


def _active_controller(root, active, frozen):
    """Resolve older pointers through their exact registered source segment."""
    if active.get("artifact_id") is not None:
        return active["artifact_id"], {"method": "explicit-active-pointer"}
    segment_path = _path(root, active.get("segment_path"))
    _require(segment_path.is_relative_to(root / "src/sources/works")
             and segment_path.parent.name == "segments" and segment_path.suffix == ".toml",
             "active controller requires a source-owned segment record")
    data = segment_path.read_bytes()
    segment = tomllib.loads(data.decode())
    _require(segment.get("schema") == 2 and segment.get("record_type") == "segment"
             and isinstance(active.get("segment_id"), str) and segment.get("id") == active["segment_id"]
             and isinstance(active.get("sha256"), str) and geometry.SHA.fullmatch(active["sha256"])
             and segment.get("artifact_sha256") == active["sha256"]
             and segment.get("physical_line_ranges") == active.get("physical_line_ranges")
             and isinstance(segment.get("artifact_id"), str)
             and re.fullmatch(r"artifact\.[a-z0-9.-]+", segment["artifact_id"]),
             "registered active segment disagrees with pointer identity, source hash or ranges")
    _ranges(segment["physical_line_ranges"])
    digest = _sha(data)
    frozen[segment_path] = digest
    return segment["artifact_id"], {"method": "registered-active-segment", "segment_id": segment["id"],
                                    "segment_record_sha256": digest}


def _native_pages(root, out, pins, locations, line_map, line_pin, leaves, frozen):
    """At most one whole extraction per volume/run, never one parse per act.

    Cache reuse rehashes whole inputs first. The cache is checked derived
    evidence, not an independently authoritative transcription.
    """
    recipe = {"schema": CACHE_SCHEMA, **pins, "line_map": line_pin,
              "extractor_sha256": _hash(Path(geometry.__file__)), "screen_sha256": _hash(Path(__file__)),
              "WORD_fields": WORD_FIELDS, "page_token_fingerprint": "sha256 of canonical JSON whitespace-token array plus LF"}
    recipe_sha = _sha(_bytes(recipe))
    cache_dir = out / "native-cache" / recipe_sha
    _require(cache_dir.resolve() == cache_dir, "screen/cache output cannot pass through symlinks")
    # Individual page receipts are immutable and reusable across bounded runs.
    # A leaf-set index is also immutable; adding leaves never rewrites one.
    generation = _sha(_bytes(sorted(leaves)))
    index_path = cache_dir / "indexes" / (generation + ".json")
    index = {"schema": CACHE_SCHEMA, "recipe": recipe, "recipe_sha256": recipe_sha,
             "whole_TXT_XML_token_equality": True, "pages": {}}
    pages, missing = [], []
    token_intervals, expected, mapped_token_count = _page_token_intervals(line_map)
    for leaf in sorted(leaves):
        receipt_path = cache_dir / f"leaf-{leaf}.receipt.json"
        payload_path = cache_dir / f"leaf-{leaf}.json.gz"
        if not receipt_path.exists():
            _require(not payload_path.exists(), "native page cache has payload without checked receipt")
            missing.append(leaf)
            continue
        receipt = _json(receipt_path, "page cache receipt")
        _require(set(receipt) == {"recipe_sha256", "leaf", "whole_TXT_XML_token_equality", "product"}
                 and receipt["recipe_sha256"] == recipe_sha and receipt["leaf"] == leaf
                 and receipt["whole_TXT_XML_token_equality"] is True, "native page cache recipe/leaf mismatch")
        entry = receipt["product"]
        _require(isinstance(entry, dict) and set(entry) == {"gzip_sha256", "page_sha256", "full_page_tokens_sha256"},
                 "native page cache receipt shape mismatch")
        payload = payload_path.read_bytes()
        _require(_sha(payload) == entry["gzip_sha256"], "native page cache compressed hash mismatch")
        decoded = gzip.decompress(payload)
        _require(_sha(decoded) == entry["page_sha256"], "native page cache decoded hash mismatch")
        compact = json.loads(decoded, object_pairs_hook=geometry._object_pairs, parse_constant=geometry._constant)
        _require(compact.get("full_page_tokens_sha256") == entry["full_page_tokens_sha256"],
                 "native page cache fingerprint receipt mismatch")
        page = _expand(compact)
        _require(page["leaf"] == leaf, "native page cache leaf mismatch")
        pages.append(page)
        index["pages"][str(leaf)] = entry
    if missing:
        native = geometry.source_pages(root, pins["source_txt"], pins["source_xml"], missing, input_map=locations)
        for page in native["pages"]:
            compact = _compact(page)
            decoded = _bytes(compact)
            payload = _gzip(decoded)
            index["pages"][str(page["leaf"])] = {"gzip_sha256": _sha(payload), "page_sha256": _sha(decoded),
                "full_page_tokens_sha256": compact["full_page_tokens_sha256"]}
            pages.append(_expand(compact))
            _write(cache_dir / f"leaf-{page['leaf']}.json.gz", payload)
            _write(cache_dir / f"leaf-{page['leaf']}.receipt.json", _bytes({"recipe_sha256": recipe_sha,
                "leaf": page["leaf"], "whole_TXT_XML_token_equality": True, "product": index["pages"][str(page["leaf"]) ]}))
    raw_path = _path(root, locations[pins["source_txt"]["artifact_id"]])
    raw = raw_path.read_bytes()
    newlines = [match.start() for match in re.finditer(b"\n", raw)]
    xml_path = _path(root, locations[pins["source_xml"]["artifact_id"]])
    # A bounded per-volume structural scan independently checks cache ordinals,
    # page identity and native LINE membership, even if a receipt is rewritten.
    # It does not extract source prose again or run once per act.
    xml = xml_path.read_bytes()
    object_starts = [m.start() for m in re.finditer(rb"<OBJECT\b", xml)]
    line_starts = [m.start() for m in re.finditer(rb"<LINE\b", xml)]
    word_starts = [m.start() for m in re.finditer(rb"<WORD\b", xml)]
    raw_tokens = geometry._tokens(raw)
    _require(mapped_token_count == len(raw_tokens), "line map whole token sum disagrees with complete raw TXT")
    _require(len(line_map["pages"]) == len(object_starts), "line map whole OBJECT count mismatch")
    with io.BytesIO(xml) as xml_stream:
        for page in pages:
            ref = expected.get(page["leaf"])
            _require(ref is not None and page["artifact_page"] == ref["artifact_page"]
                     and page["source_lf_range_1"] == [ref["physical_line_start"], ref["physical_line_end"]],
                     "native page leaf/OBJECT/LF map mismatch")
            lf_a, lf_z = page["source_lf_range_1"]
            byte_a = newlines[lf_a - 2] + 1 if lf_a > 1 else 0
            byte_z = newlines[lf_z - 1] + 1 if lf_z <= len(newlines) else len(raw)
            _require(page["source_byte_range_0"] == [byte_a, byte_z], "native page source byte/LF bounds mismatch")
            ordinal = page["artifact_page"]
            _require(type(ordinal) is int and 1 <= ordinal <= len(object_starts), "native page OBJECT ordinal invalid")
            object_a = object_starts[ordinal - 1]
            object_z = object_starts[ordinal] if ordinal < len(object_starts) else len(xml)
            tag_z = geometry._tag_end(xml, object_a)
            tag = xml[object_a:tag_z]
            obj = ElementTree.fromstring(tag if tag.endswith(b"/>") else tag[:-1] + b"/>")
            leaf_match = re.search(r"_(\d+)\.djvu$", obj.get("usemap", ""))
            _require(leaf_match is not None and int(leaf_match[1]) == page["leaf"]
                     and page["dimensions"] == [int(obj.get("width", "0")), int(obj.get("height", "0"))],
                     "native cache source OBJECT leaf/dimensions mismatch")
            first_word = bisect.bisect_left(word_starts, object_a)
            last_word = bisect.bisect_left(word_starts, object_z)
            first_line = bisect.bisect_left(line_starts, object_a)
            last_line = bisect.bisect_left(line_starts, object_z)
            _require(page["word_count"] == last_word - first_word and page["line_count"] == last_line - first_line
                     and page["source_word_range_1"] == ([first_word + 1, last_word] if first_word < last_word else None),
                     "native cache source page WORD/LINE count mismatch")
            page_token_offsets = [pair for word in page["words"] for pair in word["source_txt_token_byte_ranges_0"]]
            # LF-enclosing page byte spans can overlap when adjacent XML pages
            # share one TXT LF. Exact token intervals instead use the pinned
            # per-OBJECT token-count prefix, never cached WORD offsets or all
            # tokens in an enclosing LF. Repeated page text cannot substitute.
            token_a, token_z = token_intervals[page["leaf"]]
            expected_tokens = raw_tokens[token_a:token_z]
            _require(sum(len(word["value"].split()) for word in page["words"]) == ref["tokens"],
                     "native full-page token count disagrees with pinned line map")
            _require(page["source_token_range_0"] == [token_a, token_z]
                     and all(byte_a <= a < z <= byte_z for a, z in page_token_offsets)
                     and [[a, z] for a, z, value in expected_tokens] == page_token_offsets
                     and page["full_page_tokens_sha256"] == _sha(_bytes([value for a, z, value in expected_tokens])),
                     "native cache full-page raw token interval mismatch")
            for word in page["words"]:
                parts = word["value"].split()
                ranges = word["source_txt_token_byte_ranges_0"]
                _require(len(parts) == len(ranges) and all(0 <= a < z <= len(raw) for a, z in ranges)
                         and [raw[a:z].decode() for a, z in ranges] == parts,
                         "native cache WORD/raw token byte mapping mismatch")
                lines = sorted({bisect.bisect_left(newlines, a) + 1 for a, z in ranges})
                _require(lines == word["source_txt_physical_lines"] and all(lf_a <= line <= lf_z for line in lines),
                         "native cache exact LF mapping mismatch")
                a, z = word["source_xml_byte_range_0"]
                _require(0 <= a < z <= pins["source_xml"]["byte_size"], "native cache XML byte bounds mismatch")
                global_word = bisect.bisect_left(word_starts, a)
                global_line = bisect.bisect_right(line_starts, a)
                _require(object_a < a < z <= object_z and global_word < len(word_starts) and word_starts[global_word] == a
                         and word["source_word_global_1"] == global_word + 1
                         and word["source_line_global_1"] == global_line
                         and word["source_line_page_1"] == global_line - first_line,
                         "native cache source WORD/LINE/XML membership mismatch")
                tag_z = geometry._tag_end(xml, a)
                if xml[a:tag_z].endswith(b"/>"):
                    expected_z = tag_z
                else:
                    close_a = xml.find(b"</WORD", tag_z)
                    _require(close_a >= tag_z, "native cache XML WORD closing tag is absent")
                    expected_z = geometry._tag_end(xml, close_a)
                _require(z == expected_z, "native cache exact XML WORD end offset mismatch")
                xml_stream.seek(a)
                try:
                    node = ElementTree.fromstring(xml_stream.read(z - a))
                except ElementTree.ParseError as error:
                    raise ScreenError("native cache XML WORD byte mapping mismatch") from error
                _require(node.tag == "WORD" and not list(node) and (node.text or "") == word["value"]
                         and node.get("coords") == word["coords"], "native cache XML WORD value/coords mismatch")
                x0, y0, x1, y1 = map(int, word["coords"].split(","))
                _require(word["source_bbox"] == [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)],
                         "native cache normalized bbox mismatch")
    _write(index_path, _bytes(index))
    pages.sort(key=lambda page: page["artifact_page"])
    return pages, {"recipe_sha256": recipe_sha, "index_sha256": _sha(_bytes(index)),
                   "pages": index["pages"], "whole_TXT_XML_token_equality": True}


def fit_bands(page):
    """Numerical candidate prose bands; no semantic ownership is assigned."""
    width, height = page["dimensions"]
    lines = defaultdict(list)
    for word in page["words"]:
        if word["value"].split():
            lines[word["source_line_global_1"]].append(word)
    eligible = {"left": [], "right": []}
    for words in lines.values():
        x0, y0 = (min(w["source_bbox"][i] for w in words) for i in (0, 1))
        x1, y1 = (max(w["source_bbox"][i] for w in words) for i in (2, 3))
        if (sum(len(w["value"].split()) for w in words) >= THRESHOLDS["min_line_tokens"]
                and THRESHOLDS["min_line_width_W"] * width <= x1 - x0 <= THRESHOLDS["max_line_width_W"] * width
                and THRESHOLDS["min_line_y_H"] * height <= (y0 + y1) / 2 <= THRESHOLDS["max_line_y_H"] * height
                and y1 - y0 <= THRESHOLDS["max_line_height_H"] * height):
            eligible["left" if (x0 + x1) / 2 < width / 2 else "right"].append((x0, x1))
    result = {}
    for side, edges in eligible.items():
        lane = {"status": "UNKNOWN", "eligible_native_lines": len(edges)}
        if edges:
            a, z = (statistics.median(edge[i] for edge in edges) for i in (0, 1))
            ma, mz = (statistics.median(abs(edge[i] - mid) for edge in edges)
                      for i, mid in ((0, a), (1, z)))
            lane.update({"median_x0": a, "median_x1": z, "x0_MAD": ma, "x1_MAD": mz})
            if len(edges) >= THRESHOLDS["min_lane_lines"] and max(ma, mz) < THRESHOLDS["max_edge_MAD_W"] * width:
                lane["status"] = "FITTED_CANDIDATE"
        result[side] = lane
    if all(lane["status"] == "FITTED_CANDIDATE" for lane in result.values()):
        if result["left"]["median_x1"] >= result["right"]["median_x0"]:
            for lane in result.values():
                lane["status"] = "UNKNOWN"
                lane["reason"] = "candidate bands overlap"
    return result


def _word_evidence(word):
    return {key: word[key] for key in WORD_FIELDS}


def screen_page(page, ranges, bands=None):
    """Screen selected WORD geometry without changing order or source wording."""
    bands = fit_bands(page) if bands is None else bands
    width, height = page["dimensions"]
    selected = [w for w in page["words"] if any(_selected(line, ranges) for line in w["source_txt_physical_lines"])]
    flags = []
    def add(kind, words, side=None, **extra):
        words = sorted({w["source_word_global_1"]: w for w in words}.values(), key=lambda w: w["source_word_global_1"])
        flags.append({"kind": kind, "leaf": page["leaf"], "artifact_page": page["artifact_page"],
                      "lead_priority": "mixed-LF" if kind == "mixed-native-line-and-LF" else "broader-geometry",
                      "candidate_band": side, "physical_lines": sorted({n for w in words for n in w["source_txt_physical_lines"]
                                                                               if _selected(n, ranges)}),
                      "WORDs": [_word_evidence(w) for w in words], **extra})
    for word in selected:
        if any(not _selected(line, ranges) for line in word["source_txt_physical_lines"]):
            add("partial-indivisible-WORD-selection", [word])
    fitted = {side: band for side, band in bands.items() if band["status"] == "FITTED_CANDIDATE"}
    def core(word, side):
        band = fitted[side]
        x0, y0, x1, y1 = word["source_bbox"]
        return (band["median_x0"] <= (x0 + x1) / 2 <= band["median_x1"]
                and THRESHOLDS["min_line_y_H"] * height <= (y0 + y1) / 2 <= THRESHOLDS["max_line_y_H"] * height)
    def outward(word, side):
        x0, y0, x1, y1 = word["source_bbox"]
        band, gap = fitted[side], THRESHOLDS["outward_gap_W"] * width
        return x1 < band["median_x0"] - gap if side == "left" else x0 > band["median_x1"] + gap
    native_lines = defaultdict(list)
    for word in selected:
        native_lines[word["source_line_global_1"]].append(word)
    for line_id, words in native_lines.items():
        for side in fitted:
            for line in sorted({n for w in words for n in w["source_txt_physical_lines"] if _selected(n, ranges)}):
                row = [w for w in words if line in w["source_txt_physical_lines"]]
                body = [w for w in row if core(w, side)]
                outer = [w for w in row if outward(w, side)]
                if len(body) >= THRESHOLDS["min_core_WORDs"] and outer:
                    add("mixed-native-line-and-LF", body + outer, side, native_line_global_1=line_id,
                        shared_physical_line=line, core_WORD_ids=[w["source_word_global_1"] for w in body],
                        outward_WORD_ids=[w["source_word_global_1"] for w in outer])
        if len(fitted) == 2:
            left, right = ([w for w in words if core(w, side)] for side in ("left", "right"))
            if min(len(left), len(right)) >= THRESHOLDS["min_core_WORDs"]:
                add("both-candidate-bands-selected-native-line", left + right, native_line_global_1=line_id)
    for side in fitted:
        edge = fitted[side]["median_x0" if side == "left" else "median_x1"]
        for word in selected:
            x0, y0, x1, y1 = word["source_bbox"]
            if (len(word["value"].split()) > 1 and x0 < edge < x1
                    and THRESHOLDS["min_line_y_H"] * height <= (y0 + y1) / 2 <= THRESHOLDS["max_line_y_H"] * height):
                add("indivisible-multitoken-WORD-crosses-edge", [word], side,
                    limit="The complete WORD box crosses a candidate edge; character ownership is unknown.")
        previous = None
        core_indices = [i for i, w in enumerate(selected) if core(w, side)]
        for i in core_indices:
            word = selected[i]
            x0, y0, x1, y1 = word["source_bbox"]
            if previous is not None and previous["source_line_global_1"] != word["source_line_global_1"]:
                before_y = (previous["source_bbox"][1] + previous["source_bbox"][3]) / 2
                if before_y - (y0 + y1) / 2 > THRESHOLDS["backward_jump_H"] * height:
                    add("same-candidate-band-large-backward-y", [previous, word], side,
                        backward_jump_pixels=before_y - (y0 + y1) / 2)
            previous = word
        for a, z in zip(core_indices, core_indices[1:]):
            if selected[a]["value"].rstrip().endswith("-") and 1 < z - a <= THRESHOLDS["hyphen_max_intervening_WORDs"] + 1:
                between = [w for w in selected[a + 1:z] if outward(w, side)]
                if between:
                    add("literal-hyphen-outward-WORDs-before-next-core", [selected[a], *between, selected[z]], side,
                        limit="Literal sequence only; letters are never joined and continuation is not inferred.")
    return {"leaf": page["leaf"], "selected_WORDs": len(selected), "flags": flags,
            "unknown_candidate_bands": [side for side, band in bands.items() if band["status"] == "UNKNOWN"]}


def screen(root, frontier_path, catalog_path, input_map_path, out_dir, *, volumes=None):
    """Write deterministic scratch evidence only; return a compact run summary."""
    root = Path(root).resolve()
    frontier_path, catalog_path, map_path, out = (_path(root, value) for value in
                                                 (frontier_path, catalog_path, input_map_path, out_dir))
    _require(out.is_relative_to(root / ".scratch") and out != root / ".scratch", "screen output must be below repository .scratch")
    _require(all(path.resolve() == path for path in (out / "native-cache", out / "screen.json", out / "pages.json.gz")),
             "screen/cache output cannot pass through symlinks")
    frontier = _json(frontier_path, "frontier")
    catalog, recipe = _json(catalog_path, "catalog"), _json(map_path, "input map")
    geometry._fields(recipe, {"schema", "frontier", "catalog", "inputs"}, {"controls"}, "screen input map")
    _require(recipe["schema"] == MAP_SCHEMA, "unknown screen input-map schema")
    _matches_pin(frontier_path, recipe["frontier"])
    _matches_pin(catalog_path, recipe["catalog"])
    _require(frontier.get("schema") == FRONTIER_SCHEMA and isinstance(frontier.get("rows"), list), "unknown frontier schema")
    _require(catalog.get("schema") == "triptych-bullarium-catalog/v1" and isinstance(catalog.get("units"), list)
             and isinstance(catalog.get("volumes"), list), "unknown screen catalog schema")
    inputs = recipe["inputs"]
    _require(isinstance(inputs, dict) and all(isinstance(key, str) for key in inputs), "runtime inputs must be an identity/path object")
    for value in inputs.values():
        _path(root, value)
    controls = recipe.get("controls", {})
    _require(isinstance(controls, dict) and all(isinstance(key, str) and value in
             {"mixed-row-positive", "no-mixed-row-observed"} for key, value in controls.items()), "invalid screen calibration controls")
    volume_filter = None if volumes is None else {_volume(value) for value in volumes}
    _require(volume_filter is None or volume_filter, "volumes filter cannot be empty")
    by_volume = {_volume(v["volume"]): v for v in catalog["volumes"]}
    units = {u["id"]: u for u in catalog["units"]}
    _require(len(units) == len(catalog["units"]) and len(by_volume) == len(catalog["volumes"]), "duplicate catalog identity")
    allowed_inputs = {entry[key] for v in catalog["volumes"] for entry in v["container"]["artifacts"].values()
                      for key in ("id", "sha256")}
    _require(set(inputs) <= allowed_inputs, "unknown runtime input-map source identity")
    frozen = {path: _hash(path) for path in (frontier_path, catalog_path, map_path, Path(__file__), Path(geometry.__file__))}
    grouped, excluded, results = defaultdict(list), [], []
    seen = set()
    for row in frontier["rows"]:
        _require(isinstance(row, dict) and isinstance(row.get("unit_id"), str) and row["unit_id"] not in seen,
                 "invalid or duplicate frontier unit ID")
        seen.add(row["unit_id"])
        _ranges(row.get("physical_line_ranges"))
        key = _volume(row.get("volume"))
        _require(key in by_volume and row["unit_id"] in units, "frontier unit/volume absent from current catalog")
        if volume_filter is not None and key not in volume_filter:
            active = units[row["unit_id"]].get("active_render_selection", {})
            excluded.append({"unit_id": row["unit_id"], "frontier_document_id": row.get("current_document_id"),
                             "current_document_id": active.get("id", row.get("current_document_id")),
                             "reason": "outside explicit volume filter", "control": controls.get(row["unit_id"])})
        else:
            grouped[key].append(row)
    _require(set(controls) <= seen, "calibration control is absent from frontier")
    source_reports, page_reports = [], []
    for key in sorted(grouped, key=lambda x: 25 if x == "appendix" else int(x)):
        volume = by_volume[key]
        pins, locations, line_map, line_pin = _source(root, volume, inputs, frozen)
        rows = grouped[key]
        leaves, runnable = set(), []
        for row in rows:
            current = units[row["unit_id"]]
            active = current.get("active_render_selection")
            selected = active if isinstance(active, dict) else current.get("review", current)
            current_id = active.get("id") if isinstance(active, dict) else row.get("current_document_id")
            expected_ranges = selected.get("physical_line_ranges", current.get("physical_line_ranges"))
            source_sha = active.get("sha256") if isinstance(active, dict) else current.get("artifact_sha256")
            source_id, resolution = (_active_controller(root, active, frozen) if isinstance(active, dict)
                                     else (current.get("artifact_id"), {"method": "catalog-raw-controller"}))
            segment_id = active.get("segment_id") if isinstance(active, dict) else current.get("segment_id")
            base = {"unit_id": row["unit_id"], "frontier_document_id": row.get("current_document_id"),
                    "current_document_id": current_id, "current_catalog_status": current["status"],
                    "current_reader_status": current.get("active_reader_status"),
                    "controller_resolution": resolution,
                    "current_selection_status": active.get("status") if isinstance(active, dict) else current["status"],
                    "frontier_segment_id": row.get("segment_id"), "current_segment_id": segment_id,
                    "physical_line_ranges": row["physical_line_ranges"], "control": controls.get(row["unit_id"]),
                    "artifact_id": row["artifact_id"], "artifact_sha256": row["artifact_sha256"]}
            if (source_id != row["artifact_id"] or source_sha != row["artifact_sha256"]
                    or pins["source_txt"]["artifact_id"] != source_id or pins["source_txt"]["sha256"] != source_sha
                    or expected_ranges != row["physical_line_ranges"] or current_id != row.get("current_document_id")
                    or segment_id != row.get("segment_id")):
                results.append({**base, "status": "UNKNOWN", "flags": [], "unknown_reasons": ["frontier and current source selection disagree"]})
                continue
            _require(row["physical_line_ranges"][-1][1] <= line_map["physical_line_count"], "selection exceeds whole source LF bounds")
            own_leaves = {p["leaf"] for p in line_map["pages"] if p.get("physical_line_start") is not None and
                          any(a <= p["physical_line_end"] and p["physical_line_start"] <= z for a, z in row["physical_line_ranges"])}
            if not own_leaves:
                results.append({**base, "status": "UNKNOWN", "flags": [], "unknown_reasons": ["selected LF has no mapped native page"]})
                continue
            leaves.update(own_leaves)
            runnable.append((row, base, own_leaves))
        if not leaves:
            continue
        pages, cache = _native_pages(root, out, pins, locations, line_map, line_pin, leaves, frozen)
        page_index = {p["leaf"]: p for p in pages}
        fitted = {p["leaf"]: fit_bands(p) for p in pages}
        for page in pages:
            page_reports.append({"volume": volume["volume"], **{k: page[k] for k in PAGE_FIELDS},
                "full_page_tokens_sha256": page["full_page_tokens_sha256"], "candidate_prose_bands": fitted[page["leaf"]],
                "cache": cache["pages"][str(page["leaf"])]})
        for row, base, own_leaves in runnable:
            screened = [screen_page(page_index[leaf], row["physical_line_ranges"], fitted[leaf]) for leaf in sorted(own_leaves)]
            flags = [flag for p in screened for flag in p["flags"]]
            unknown = [{"leaf": p["leaf"], "bands": p["unknown_candidate_bands"]} for p in screened if p["unknown_candidate_bands"]]
            if not sum(p["selected_WORDs"] for p in screened):
                unknown.append({"reason": "selection contains no native WORD tokens"})
            partial = any(f["kind"] == "partial-indivisible-WORD-selection" for f in flags)
            results.append({**base, "status": "FLAGGED" if flags else "UNKNOWN" if unknown else "NO_SIGNAL_NOT_CLEAR",
                            "flags": flags, "unknown_candidate_pages": unknown, "partial_WORD_selection": partial,
                            "selected_WORDs": sum(p["selected_WORDs"] for p in screened), "scan_leaves": sorted(own_leaves)})
        source_reports.append({"volume": volume["volume"], **pins, "line_map": line_pin, "native_cache": cache})
        del pages, page_index
    results.sort(key=lambda row: row["unit_id"])
    control_reports = []
    for row in results:
        if row["control"]:
            mixed = sum(flag["kind"] == "mixed-native-line-and-LF" for flag in row["flags"])
            control_reports.append({"unit_id": row["unit_id"], "expected": row["control"], "status": row["status"],
                "observed_mixed_rows": mixed, "other_flag_counts": dict(sorted(Counter(f["kind"] for f in row["flags"]
                    if f["kind"] != "mixed-native-line-and-LF").items())),
                "missed_positive": row["control"] == "mixed-row-positive" and mixed == 0,
                "false_mixed_flag": row["control"] == "no-mixed-row-observed" and mixed > 0,
                "negative_seed_any_flag": row["control"] == "no-mixed-row-observed" and bool(row["flags"]),
                "unknown_fit": bool(row.get("unknown_candidate_pages") or row.get("unknown_reasons")),
                "limitation": "A numerical match does not clear source order or separate caption ownership."})
    report = {"schema": SCHEMA, "frontier": recipe["frontier"], "catalog": recipe["catalog"],
              "frontier_original_catalog_receipt": frontier.get("catalog_receipt"), "input_map_sha256": frozen[map_path],
              "screen_sha256": frozen[Path(__file__)], "thresholds": THRESHOLDS, "limitations": LIMITS,
              "volumes": None if volume_filter is None else sorted(volume_filter), "sources": source_reports,
              "results": results, "excluded_by_volume": excluded, "calibration": control_reports,
              "counts": {"frontier_rows": len(frontier["rows"]), "screened_rows": len(results), "excluded_rows": len(excluded),
                         "native_pages": len(page_reports), "statuses": dict(sorted(Counter(r["status"] for r in results).items())),
                         "flags": dict(sorted(Counter(f["kind"] for r in results for f in r["flags"]).items()))}}
    _require(all(path.is_file() and _hash(path) == digest for path, digest in frozen.items()), "screen input changed during run")
    pages_bytes = _gzip(_bytes(page_reports))
    _write(out / "pages.json.gz", pages_bytes)
    report["page_evidence"] = {"sha256": _sha(pages_bytes), "byte_size": len(pages_bytes), "file": "pages.json.gz"}
    output = _bytes(report)
    _write(out / "screen.json", output)
    return {"schema": SCHEMA, "counts": report["counts"], "screen_sha256": _sha(output),
            "page_evidence_sha256": _sha(pages_bytes), "calibration": control_reports, "limitations": LIMITS}


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ScreenError(message)


def main(argv=None, examples=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = _Parser(prog="bullarium screen", description=__doc__)
    with_examples(parser, examples.get("screen", EXAMPLES) if isinstance(examples, dict) else examples or EXAMPLES)
    parser.add_argument("--root", type=Path, default=ROOT)
    for option in ("frontier", "catalog", "input-map", "out"):
        parser.add_argument("--" + option, required=True)
    parser.add_argument("--volumes", nargs="+", help="explicit bounded volume numbers or appendix; comma-separated values also accepted")
    parser.add_argument("--json", action="store_true")
    try:
        args = parser.parse_args(argv)
        volumes = None if args.volumes is None else [int(v) if v.isdigit() else v for token in args.volumes for v in token.split(",")]
        info = screen(args.root, args.frontier, args.catalog, args.input_map, args.out, volumes=volumes)
        result = {"v": 1, "status": "screened-research-only", **info}
        print(json.dumps(result, sort_keys=True, separators=(",", ":")) if args.json else
              f"screen: {info['counts']['screened_rows']} selections; {info['counts']['native_pages']} pages; research leads only")
        return 0
    except (ValueError, OSError, KeyError, TypeError, EOFError, expat.ExpatError, ElementTree.ParseError) as error:
        print(json.dumps({"v": 1, "status": "error", "code": "input", "error": str(error)}, sort_keys=True, separators=(",", ":"))
              if "--json" in argv else f"bullarium screen: {error}", file=sys.stderr)
        return 2
