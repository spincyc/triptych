"""Pinned five-character print marks; offline lookup, explicit font authoring.

The separate font-software delivery domain does not alter the frozen Libertinus
faces. Native HarfBuzz/WOFF2 calls occur only in the explicit ``author`` command.
The existing canonical Junicode OFL notice remains the sole plaintext owner.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import struct

import _artifact_store as transport

INDEX_PATH = "src/common/browser-print-marks.json"
LICENSE_PATH = "src/web/browser/shared/fonts/OFL-Junicode.txt"
RECIPE_PATH = "src/web/browser/shared/fonts/README.md"
SCHEMA = "triptych-browser-print-marks/v1"
DELIVERY_SCHEMA = "triptych-browser-print-marks-delivery/v1"
FAMILY = "Triptych Source Marks"
POSTSCRIPT = "TriptychSourceMarks-Regular"
UNICODE_RANGE = "U+211F,U+2123,U+21A9,U+2610,U+2720"
CODEPOINTS = (0x211F, 0x2123, 0x21A9, 0x2610, 0x2720)
SOURCE_CODEPOINTS = tuple(cp for cp in CODEPOINTS if cp != 0x2610)
PREFIX = "web-print-marks/"
LICENSE_SHA = "6078ed582d53a416f761fd2fdeb384320b69191bf316234c21aabe71e2416822"
UPSTREAM = {
    "repository": "https://github.com/psb1558/Junicode-font",
    "commit": "180ce3c94bf051f9457422b87e87e9b1cb41107e", "tag": "v2.218",
    "url": "https://raw.githubusercontent.com/psb1558/Junicode-font/180ce3c94bf051f9457422b87e87e9b1cb41107e/webfiles/JunicodeVF-Roman.woff2",
    "sha256": "a5838c9ed2cd6eca5a013220932bcddd1825523b85ceb5561393313c754e4639", "bytes": 1001940,
    "ttf_sha256": "dee372223b0124472d7bd2076c8ad2e71d137f667785a4a784b1ff26d08145dc",
    "embedded_version": "Version 2.003",
}
DESCRIPTION = ("Modified static derivative of Junicode VF Roman, Version 2.003: "
               "four retained Junicode marks U+211F, U+2123, U+21A9, U+2720 plus "
               "a project-authored U+2610 geometric hollow square, not an upstream Junicode glyph. "
               "All upstream variable axes pinned to defaults. Renamed Triptych Source Marks. "
               "Upstream copyright and SIL Open Font License 1.1 remain unchanged; the entire derivative is OFL-1.1.")


class MarksError(ValueError):
    pass


def need(value, message):
    if not value:
        raise MarksError(message)


def sha(body):
    return hashlib.sha256(body).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _read(root, pin):
    path = transport._path(root, pin["path"])
    body = transport._verify(path, pin).read_bytes()
    need(len(body) == pin["bytes"] and sha(body) == pin["sha256"], "marks bytes changed during read")
    return body


def _typed(body):
    need(len(body) >= 48 and body[:8] == b"wOF2\x00\x01\x00\x00" and struct.unpack_from(">I", body, 8)[0] == len(body), "marks payload is not the expected typed WOFF2")


def _validate(data):
    need(isinstance(data, dict) and set(data) == {"schema", "manifest_digest", "font", "upstream", "license", "recipe_reference", "derivation", "delivery"}, "invalid marks manifest fields")
    need(data["schema"] == SCHEMA and data["manifest_digest"] == sha(canonical({k: v for k, v in data.items() if k != "manifest_digest"})), "marks manifest schema/digest mismatch")
    need(data["upstream"] == UPSTREAM, "marks upstream provenance differs from the pinned Junicode input")
    font = data["font"]
    need(set(font) == {"family", "weight", "style", "unicode_range", "path", "sha256", "bytes", "media_type"}, "invalid marks font descriptor")
    need((font["family"], font["weight"], font["style"], font["unicode_range"], font["media_type"]) == (FAMILY, "400", "normal", UNICODE_RANGE, "font/woff2"), "marks face identity/range mismatch")
    need(font["path"] == PREFIX + font["sha256"] + ".woff2", "noncanonical marks payload path")
    transport.validate_delivery_index(data["delivery"], schema=DELIVERY_SCHEMA, kinds=("font-software",), path_prefix=PREFIX)
    need(len(data["delivery"]["artifacts"]) == len(data["delivery"]["archives"]) == 1, "marks require exactly one payload/archive")
    entry = data["delivery"]["artifacts"][0]
    need(all(entry[k] == font[k] for k in ("path", "sha256", "bytes", "media_type")), "marks delivery identity mismatch")
    license = data["license"]
    need(license["path"] == LICENSE_PATH and license["sha256"] == LICENSE_SHA and license["bytes"] == 4356 and license["spdx"] == "OFL-1.1" and license["reserved_font_names"] == [], "marks canonical license mismatch")
    need(data["recipe_reference"]["path"] == RECIPE_PATH, "marks recipe must reference the canonical Junicode provenance")
    proof = data["derivation"]
    need(proof["recipe"] == "harfbuzz-four-default-marks-plus-project-checkbox-renamed/v1" and proof["unicode_range"] == UNICODE_RANGE and proof["static_default_axes"] is True, "marks derivation scope mismatch")
    need(proof["input_woff2_sha256"] == UPSTREAM["sha256"] and proof["input_ttf_sha256"] == UPSTREAM["ttf_sha256"] and proof["output_woff2_sha256"] == font["sha256"] and proof["output_woff2_bytes"] == font["bytes"], "marks derivation byte pins mismatch")
    points = {f"U+{cp:04X}" for cp in CODEPOINTS}
    need(set(proof["source_glyphs"]) == {f"U+{cp:04X}" for cp in SOURCE_CODEPOINTS} and set(proof["output_glyphs"]) == points, "marks cmap scope mismatch")
    for cp in proof["source_glyphs"]:
        a, b = proof["source_glyphs"][cp], proof["output_glyphs"][cp]
        need(a["gid"] > 0 and b["gid"] > 0 and a["outline_sha256"] == b["outline_sha256"] and a["advance"] == b["advance"] and a["extents"] == b["extents"], "marks glyph shape or metrics changed")
    need(proof["preserved_name_ids"] == [0, 5, 13, 14] and proof["changed_name_ids"] == [1, 3, 4, 6] and proof["added_name_ids"] == [10] and proof["source_protected_names"] == proof["output_protected_names"], "marks origin/license names changed")
    need(set(proof["cmap"]) == points and all(type(v) is int and v > 0 for v in proof["cmap"].values()), "marks cmap is not exactly the five declared characters")
    need(proof["woff2_roundtrip_verified"] is True and proof["two_fresh_passes_identical"] is True, "marks conversion proof incomplete")
    need(proof["roundtrip_glyphs"] == proof["output_glyphs"], "marks roundtrip outline/metrics mismatch")
    box = proof["added_ballot_box"]
    need(box == ballot_box_geometry(box["source_units_per_em"], box["source_cap_height"]), "marks ballot-box construction mismatch")
    need(proof["output_glyphs"]["U+2610"]["advance"] == box["advance"] and proof["output_glyphs"]["U+2610"]["extents"] == [box["sidebearing"], box["source_cap_height"], box["source_cap_height"], -box["source_cap_height"]], "marks ballot-box metrics mismatch")


def load_index(root):
    try:
        root = Path(root).resolve()
        data = json.loads(transport._path(root, INDEX_PATH).read_text(), object_pairs_hook=transport._unique_keys)
        _validate(data)
        _read(root, data["license"])
        _read(root, data["recipe_reference"])
        return data
    except (KeyError, TypeError, AttributeError, IndexError, struct.error, UnicodeError, transport.ArtifactStoreError) as error:
        raise MarksError("invalid print marks manifest: " + str(error)) from error


def font_asset(root, *, include_body=True):
    """Read the exact renamed five-character face; never fetch or run native code."""
    root = Path(root).resolve(); data = load_index(root); font = data["font"]
    entry = data["delivery"]["artifacts"][0]
    path = transport.cache_path(root, entry)
    try:
        body = transport._verify(path, entry).read_bytes()
    except FileNotFoundError as error:
        raise FileNotFoundError("print marks are not cached; explicitly run python scripts/_web_print_marks.py hydrate --archive-dir DIR (or --fetch)") from error
    need(len(body) == font["bytes"] and sha(body) == font["sha256"], "marks payload changed during read")
    _typed(body)
    license = data["license"]
    notice = {"src": "shared/fonts/OFL-Junicode.txt", "sha256": license["sha256"], "bytes": license["bytes"], "mime": "text/plain", "spdx": "OFL-1.1"}
    record = {"id": "font:" + POSTSCRIPT, "family": FAMILY, "weight": "400", "style": "normal", "unicode_range": UNICODE_RANGE, "src": font["path"], "href": font["path"], "sha256": font["sha256"], "bytes": font["bytes"], "mime": "font/woff2", "license": notice}
    if include_body:
        record["body"] = body; notice["body"] = _read(root, license)
    return record


def check(root, *, local_bytes=False):
    data = load_index(root)
    if local_bytes:
        font_asset(root, include_body=False)
    return {"status": "ok", "family": FAMILY, "unicode_range": UNICODE_RANGE, "sha256": data["font"]["sha256"], "bytes": data["font"]["bytes"], "manifest_digest": data["manifest_digest"], "local_bytes": local_bytes}


def hydrate(root, *, archive_dir=None, fetch=False):
    need(type(fetch) is bool, "fetch must be an explicit boolean")
    root = Path(root).resolve(); data = load_index(root); delivery = data["delivery"]
    archive = delivery["archives"][0]
    path = transport._archive_path(root, archive, Path(archive_dir) if archive_dir is not None else None, fetch)
    count = transport._read_archive(path, delivery["artifacts"], root, {data["font"]["path"]})
    return dict(check(root, local_bytes=True), hydrated=count)


def _checksum(body):
    body += b"\0" * (-len(body) % 4)
    return sum(struct.unpack(">" + "I" * (len(body) // 4), body)) & 0xFFFFFFFF


def sfnt_tables(body):
    """Strict bounded SFNT table parser used by explicit authoring and tests."""
    need(len(body) >= 12 and body[:4] == b"\x00\x01\x00\x00", "expected TrueType SFNT")
    count = struct.unpack_from(">H", body, 4)[0]; tables = {}
    need(0 < count <= 100 and 12 + 16 * count <= len(body) and _checksum(body) == 0xB1B0AFBA, "invalid SFNT header/checksum")
    for i in range(count):
        tag, stored, offset, length = struct.unpack_from(">4sIII", body, 12 + i * 16)
        need(tag not in tables and offset % 4 == 0 and offset >= 12 + count * 16 and offset + length <= len(body), "invalid SFNT table extent")
        raw = body[offset:offset + length]
        checked = raw[:8] + bytes(4) + raw[12:] if tag == b"head" else raw
        need(_checksum(checked) == stored, "invalid SFNT table checksum")
        tables[tag] = raw
    return tables


def cmap_mapping(tables):
    data = tables[b"cmap"]; version, count = struct.unpack_from(">HH", data); need(version == 0, "unsupported cmap version")
    glyph_count = struct.unpack_from(">H", tables[b"maxp"], 4)[0]
    maps = []
    for i in range(count):
        platform, encoding, at = struct.unpack_from(">HHI", data, 4 + i * 8)
        if not (platform == 0 or platform == 3 and encoding in (1, 10)):
            continue
        fmt = struct.unpack_from(">H", data, at)[0]; current = {}
        if fmt == 4:
            length = struct.unpack_from(">H", data, at + 2)[0]; n = struct.unpack_from(">H", data, at + 6)[0] // 2
            ends = at + 14; starts = ends + 2 * n + 2; deltas = starts + 2 * n; distances = deltas + 2 * n
            need(distances + 2 * n <= at + length <= len(data), "invalid cmap4 extent")
            prior = -1
            for j in range(n):
                end = struct.unpack_from(">H", data, ends + 2 * j)[0]; start = struct.unpack_from(">H", data, starts + 2 * j)[0]
                delta = struct.unpack_from(">h", data, deltas + 2 * j)[0]; distance = struct.unpack_from(">H", data, distances + 2 * j)[0]
                need(prior < start <= end, "invalid cmap4 segments")
                for cp in range(start, end + 1):
                    if distance:
                        target = distances + 2 * j + distance + 2 * (cp - start)
                        need(distances + 2 * n <= target and target + 2 <= at + length, "invalid cmap4 glyph extent")
                        gid = struct.unpack_from(">H", data, target)[0]; gid = (gid + delta) & 0xFFFF if gid else 0
                    else:
                        gid = (cp + delta) & 0xFFFF
                    if gid: current[cp] = gid
                prior = end
        elif fmt == 12:
            _, reserved, length, _, n = struct.unpack_from(">HHIII", data, at)
            need(reserved == 0 and length == 16 + 12 * n and at + length <= len(data), "invalid cmap12 extent")
            prior = -1
            for j in range(n):
                start, end, first = struct.unpack_from(">III", data, at + 16 + j * 12)
                need(prior < start <= end <= 0x10FFFF, "invalid cmap12 groups")
                for cp in range(start, end + 1):
                    if first + cp - start: current[cp] = first + cp - start
                prior = end
        else:
            raise MarksError("unsupported Unicode cmap format")
        need(all(0 < gid < glyph_count and not 0xD800 <= cp <= 0xDFFF for cp, gid in current.items()), "cmap invalid glyph/scalar")
        maps.append(current)
    need(bool(maps), "no Unicode cmap")
    fullest = max(maps, key=len)
    need(all(m == fullest or m == {cp: gid for cp, gid in fullest.items() if cp <= 0xFFFF} for m in maps), "Unicode cmap records disagree")
    return fullest


def name_records(tables):
    body = tables[b"name"]; fmt, count, storage = struct.unpack_from(">HHH", body)
    need(fmt == 0 and 6 + count * 12 <= storage <= len(body), "unsupported name table")
    result = []
    for i in range(count):
        platform, encoding, language, name, length, offset = struct.unpack_from(">HHHHHH", body, 6 + i * 12)
        need(storage + offset + length <= len(body), "invalid name extent")
        result.append((platform, encoding, language, name, body[storage + offset:storage + offset + length]))
    return result


def _protected(tables):
    return {str(n): sha(canonical([[p, e, l, value.hex()] for p, e, l, name, value in name_records(tables) if name == n])) for n in (0, 5, 13, 14)}


def _build_sfnt(tables):
    tables = dict(tables); head = bytearray(tables[b"head"]); head[8:12] = bytes(4); tables[b"head"] = bytes(head)
    n = len(tables); power = 1 << (n.bit_length() - 1)
    result = bytearray(struct.pack(">IHHHH", 0x10000, n, power * 16, power.bit_length() - 1, n * 16 - power * 16) + bytes(n * 16))
    head_at = None
    for i, (tag, raw) in enumerate(sorted(tables.items())):
        offset = len(result); struct.pack_into(">4sIII", result, 12 + 16 * i, tag, _checksum(raw), offset, len(raw))
        if tag == b"head": head_at = offset
        result.extend(raw); result.extend(bytes(-len(result) % 4))
    need(head_at is not None, "font has no head")
    struct.pack_into(">I", result, head_at + 8, (0xB1B0AFBA - _checksum(bytes(result))) & 0xFFFFFFFF)
    return bytes(result)


def ballot_box_geometry(upem, cap):
    """Plaintext construction: source cap-height square with opposite winding."""
    need(type(upem) is int and type(cap) is int and upem == 1000 and cap == 663, "unexpected pinned Junicode metrics")
    stroke = (7 * cap + 50) // 100; bearing = (6 * upem + 50) // 100
    outer = [[bearing, 0], [bearing, cap], [bearing + cap, cap], [bearing + cap, 0]]
    inner = [[bearing + stroke, stroke], [bearing + cap - stroke, stroke], [bearing + cap - stroke, cap - stroke], [bearing + stroke, cap - stroke]]
    def area(points): return sum(x * points[(i + 1) % len(points)][1] - points[(i + 1) % len(points)][0] * y for i, (x, y) in enumerate(points))
    need(cap > 2 * stroke > 0 and area(outer) < 0 < area(inner), "invalid hollow-box contour winding")
    return {"codepoint": "U+2610", "origin": "project-authored geometric glyph under OFL-1.1; absent from upstream Junicode", "source_units_per_em": upem, "source_cap_height": cap, "sizing_rule": "side=OS/2.sCapHeight; stroke=round(7% cap height); sidebearings=round(6% unitsPerEm); baseline=0", "stroke": stroke, "sidebearing": bearing, "advance": cap + 2 * bearing, "outer_clockwise": outer, "inner_counterclockwise": inner, "center_winding": 0}


def add_ballot_box(body, source_tables):
    tables = sfnt_tables(body); mapping = cmap_mapping(tables)
    need(set(mapping) == set(SOURCE_CODEPOINTS), "ballot-box input must retain exactly the four upstream marks")
    upem = struct.unpack_from(">H", source_tables[b"head"], 18)[0]; cap = struct.unpack_from(">h", source_tables[b"OS/2"], 88)[0]
    box = ballot_box_geometry(upem, cap); points = box["outer_clockwise"] + box["inner_counterclockwise"]
    glyph = bytearray(struct.pack(">hhhhhHHH", 2, box["sidebearing"], 0, box["sidebearing"] + cap, cap, 3, 7, 0) + bytes([1] * 8))
    for axis in (0, 1):
        prior = 0
        for point in points: glyph.extend(struct.pack(">h", point[axis] - prior)); prior = point[axis]
    count = struct.unpack_from(">H", tables[b"maxp"], 4)[0]
    need(struct.unpack_from(">h", tables[b"head"], 50)[0] == 0 and tables[b"post"][:4] == b"\x00\x03\x00\x00", "unexpected pinned subset loca/post form")
    offsets = list(struct.unpack(">" + "H" * (count + 1), tables[b"loca"]))
    need(offsets[-1] * 2 == len(tables[b"glyf"]) and len(glyph) % 2 == 0, "invalid glyph append extent")
    tables[b"glyf"] += glyph; offsets.append(len(tables[b"glyf"]) // 2)
    tables[b"loca"] = struct.pack(">" + "H" * len(offsets), *offsets)
    maxp = bytearray(tables[b"maxp"]); struct.pack_into(">H", maxp, 4, count + 1)
    for offset, minimum in ((6, 8), (8, 2)): struct.pack_into(">H", maxp, offset, max(minimum, struct.unpack_from(">H", maxp, offset)[0]))
    tables[b"maxp"] = bytes(maxp)
    hhea = bytearray(tables[b"hhea"]); metrics = struct.unpack_from(">H", hhea, 34)[0]; hmtx = tables[b"hmtx"]
    rows = [struct.unpack_from(">Hh", hmtx, i * 4) for i in range(metrics)]
    rows.extend((rows[-1][0], struct.unpack_from(">h", hmtx, metrics * 4 + (i - metrics) * 2)[0]) for i in range(metrics, count))
    rows.append((box["advance"], box["sidebearing"])); tables[b"hmtx"] = b"".join(struct.pack(">Hh", *row) for row in rows)
    struct.pack_into(">H", hhea, 34, count + 1); tables[b"hhea"] = bytes(hhea)
    mapping[0x2610] = count; ordered = sorted(mapping.items()) + [(0xFFFF, 0)]
    n = len(ordered); power = 1 << (n.bit_length() - 1)
    subtable = bytearray(struct.pack(">HHHHHHH", 4, 16 + 8 * n, 0, n * 2, power * 2, power.bit_length() - 1, n * 2 - power * 2))
    subtable.extend(b"".join(struct.pack(">H", cp) for cp, _ in ordered)); subtable.extend(bytes(2))
    subtable.extend(b"".join(struct.pack(">H", cp) for cp, _ in ordered))
    subtable.extend(b"".join(struct.pack(">H", (gid - cp) & 0xFFFF) for cp, gid in ordered)); subtable.extend(bytes(2 * n))
    tables[b"cmap"] = struct.pack(">HHHHIHHI", 0, 2, 0, 3, 20, 3, 1, 20) + subtable
    os2 = bytearray(tables[b"OS/2"]); struct.pack_into(">I", os2, 46, struct.unpack_from(">I", os2, 46)[0] | (1 << (46 - 32))); tables[b"OS/2"] = bytes(os2)
    return _build_sfnt(tables), box


def rename_sfnt(body):
    tables = sfnt_tables(body); rows = []
    for p, e, l, name, value in name_records(tables):
        need((p, e, l) == (3, 1, 0x409), "unexpected name language/platform")
        replacement = {1: FAMILY, 3: "2.003;NONE;" + POSTSCRIPT, 4: FAMILY + " Regular", 6: POSTSCRIPT}.get(name)
        need(name != 10, "unexpected existing derivative description")
        rows.append((p, e, l, name, replacement.encode("utf-16-be") if replacement else value))
    rows.append((3, 1, 0x409, 10, DESCRIPTION.encode("utf-16-be"))); rows.sort(key=lambda r: r[:4])
    strings = bytearray(); offsets = {}; records = bytearray()
    for p, e, l, name, value in rows:
        if value not in offsets: offsets[value] = len(strings); strings.extend(value)
        records.extend(struct.pack(">HHHHHH", p, e, l, name, len(value), offsets[value]))
    tables[b"name"] = struct.pack(">HHH", 0, len(rows), 6 + 12 * len(rows)) + records + strings
    return _build_sfnt(tables)


def _native_author(input_ttf, subset_path):
    """Lazy native C API: static subset plus exact glyph outlines/metrics."""
    import ctypes as C
    hb = C.CDLL("/usr/lib/libharfbuzz.so.0"); sub = C.CDLL("/usr/lib/libharfbuzz-subset.so.0")
    def fn(lib, name, result, *args):
        f = getattr(lib, name); f.restype = result; f.argtypes = list(args); return f
    blob_file = fn(hb, "hb_blob_create_from_file_or_fail", C.c_void_p, C.c_char_p)
    face_create = fn(hb, "hb_face_create", C.c_void_p, C.c_void_p, C.c_uint)
    create_input = fn(sub, "hb_subset_input_create_or_fail", C.c_void_p)
    cfg = create_input(); need(cfg, "HarfBuzz subset input failed")
    face = face_create(blob_file(str(input_ttf).encode()), 0); need(face, "HarfBuzz source face failed")
    unicode_set = fn(sub, "hb_subset_input_unicode_set", C.c_void_p, C.c_void_p)(cfg)
    add = fn(hb, "hb_set_add", None, C.c_void_p, C.c_uint)
    for cp in SOURCE_CODEPOINTS: add(unicode_set, cp)
    names = fn(sub, "hb_subset_input_set", C.c_void_p, C.c_void_p, C.c_int)(cfg, 4)
    for name in (0, 5, 13, 14): add(names, name)
    need(fn(sub, "hb_subset_input_pin_all_axes_to_default", C.c_int, C.c_void_p, C.c_void_p)(cfg, face), "axis pinning failed")
    result = fn(sub, "hb_subset_or_fail", C.c_void_p, C.c_void_p, C.c_void_p)(face, cfg); need(result, "HarfBuzz subset failed")
    blob = fn(hb, "hb_face_reference_blob", C.c_void_p, C.c_void_p)(result)
    length = C.c_uint(); pointer = fn(hb, "hb_blob_get_data", C.c_void_p, C.c_void_p, C.POINTER(C.c_uint))(blob, C.byref(length))
    subset_path.write_bytes(C.string_at(pointer, length.value))
    font_create = fn(hb, "hb_font_create", C.c_void_p, C.c_void_p)
    ot_funcs = fn(hb, "hb_ot_font_set_funcs", None, C.c_void_p)
    nominal = fn(hb, "hb_font_get_nominal_glyph", C.c_int, C.c_void_p, C.c_uint, C.POINTER(C.c_uint))
    advance = fn(hb, "hb_font_get_glyph_h_advance", C.c_int, C.c_void_p, C.c_uint)
    extents = fn(hb, "hb_font_get_glyph_extents", C.c_int, C.c_void_p, C.c_uint, C.POINTER(C.c_int))
    draw = fn(hb, "hb_font_draw_glyph", None, C.c_void_p, C.c_uint, C.c_void_p, C.c_void_p)
    def proof(which, codepoints=SOURCE_CODEPOINTS):
        face = face_create(blob_file(str(which).encode()), 0); font = font_create(face); ot_funcs(font)
        funcs = fn(hb, "hb_draw_funcs_create", C.c_void_p)(); events = []; callbacks = []
        for name, arity in (("move_to", 2), ("line_to", 2), ("quadratic_to", 4), ("cubic_to", 6), ("close_path", 0)):
            callback_type = C.CFUNCTYPE(None, C.c_void_p, C.c_void_p, C.c_void_p, *([C.c_float] * arity), C.c_void_p)
            def event(*args, label=name): events.append([label, *[round(float(v), 6) for v in args[3:-1]]])
            callback = callback_type(event); callbacks.append(callback)
            fn(hb, "hb_draw_funcs_set_" + name + "_func", None, C.c_void_p, callback_type, C.c_void_p, C.c_void_p)(funcs, callback, None, None)
        rows = {}
        for cp in codepoints:
            gid = C.c_uint(); need(nominal(font, cp, C.byref(gid)) and gid.value > 0, "upstream/subset lacks requested mark")
            bounds = (C.c_int * 4)(); need(extents(font, gid.value, bounds), "mark has no outline extents")
            events.clear(); draw(font, gid.value, funcs, None); need(events, "mark outline is empty")
            rows[f"U+{cp:04X}"] = {"gid": gid.value, "advance": advance(font, gid.value), "extents": list(bounds), "outline_sha256": sha(canonical(events)), "outline_commands": len(events)}
        return rows
    return proof(input_ttf), proof(subset_path), fn(hb, "hb_version_string", C.c_char_p)().decode(), proof


def author(root, input_woff2, out):
    """Explicit optional authoring; fresh scratch output, no automatic downloads."""
    import subprocess
    root = Path(root).resolve(); out = Path(out).resolve(); input_woff2 = Path(input_woff2).resolve()
    need(out.is_relative_to(root / ".scratch") and not out.exists(), "author output must be a fresh repository .scratch directory")
    source = input_woff2.read_bytes(); need(len(source) == UPSTREAM["bytes"] and sha(source) == UPSTREAM["sha256"], "author input is not pinned Junicode")
    license_body = transport._path(root, LICENSE_PATH).read_bytes(); need(sha(license_body) == LICENSE_SHA, "canonical Junicode license mismatch")
    tools = {"compress": ("/usr/bin/woff2_compress", "cc7e0a999038e6a009e62a42e7c672cfd14759c49fe4503cb9ad7b6813ea60ad"), "decompress": ("/usr/bin/woff2_decompress", "8212b031b71cac802c0e8d2ff263102538a5808280ab2f631eb8cbbd771dcf7b")}
    for executable, pin in tools.values(): need(sha(Path(executable).read_bytes()) == pin, "authoring WOFF2 tool differs from pinned recipe")
    out.mkdir(parents=True); original = out / "JunicodeVF-Roman.woff2"; original.write_bytes(source)
    subprocess.run([tools["decompress"][0], str(original)], check=True, capture_output=True)
    input_ttf = original.with_suffix(".ttf"); need(sha(input_ttf.read_bytes()) == UPSTREAM["ttf_sha256"], "upstream decompression identity mismatch")
    source_tables = sfnt_tables(input_ttf.read_bytes()); source_cmap = cmap_mapping(source_tables)
    need(set(SOURCE_CODEPOINTS) <= source_cmap.keys() and 0x2610 not in source_cmap, "upstream four-mark/added-box coverage differs")
    subset = out / "subset.ttf"; source_glyphs, output_glyphs, version, glyph_proof = _native_author(input_ttf, subset)
    combined, box = add_ballot_box(subset.read_bytes(), source_tables)
    renamed = rename_sfnt(combined); final_ttf = out / "triptych-source-marks.ttf"; final_ttf.write_bytes(renamed)
    output_glyphs = glyph_proof(final_ttf, CODEPOINTS)
    tables = sfnt_tables(renamed); cmap = cmap_mapping(tables)
    need(set(cmap) == set(CODEPOINTS) and not (set(tables) & {b"fvar", b"gvar", b"avar", b"HVAR", b"VVAR", b"MVAR"}), "subset is not exactly five static marks")
    need(_protected(source_tables) == _protected(tables), "source origin/license name bytes changed")
    for cp in source_glyphs:
        need(all(source_glyphs[cp][k] == output_glyphs[cp][k] for k in ("advance", "extents", "outline_sha256")), "mark outlines or advances changed")
    subprocess.run([tools["compress"][0], str(final_ttf)], check=True, capture_output=True)
    woff = final_ttf.with_suffix(".woff2"); _typed(woff.read_bytes())
    restored_dir = out / "roundtrip"; restored_dir.mkdir(); restored_woff = restored_dir / woff.name; restored_woff.write_bytes(woff.read_bytes())
    subprocess.run([tools["decompress"][0], str(restored_woff)], check=True, capture_output=True)
    restored = sfnt_tables(restored_woff.with_suffix(".ttf").read_bytes())
    need(tables.keys() == restored.keys(), "WOFF2 table inventory changed")
    for tag in tables:
        a, b = bytearray(tables[tag]), bytearray(restored[tag])
        if tag == b"head":
            a[8:12] = b[8:12] = bytes(4); a[16:18] = (int.from_bytes(a[16:18], "big") | 0x0800).to_bytes(2, "big"); b[16:18] = (int.from_bytes(b[16:18], "big") | 0x0800).to_bytes(2, "big")
        if tag not in {b"glyf", b"loca"}:
            need(a == b, "WOFF2 roundtrip changed a non-outline SFNT table")
    roundtrip_glyphs = glyph_proof(restored_woff.with_suffix(".ttf"), CODEPOINTS)
    need(roundtrip_glyphs == output_glyphs, "WOFF2 roundtrip changed glyph outlines or metrics")
    proof = {"recipe": "harfbuzz-four-default-marks-plus-project-checkbox-renamed/v1", "unicode_range": UNICODE_RANGE, "static_default_axes": True, "added_ballot_box": box, "input_woff2_sha256": sha(source), "input_ttf_sha256": sha(input_ttf.read_bytes()), "output_ttf_sha256": sha(renamed), "output_ttf_bytes": len(renamed), "output_woff2_sha256": sha(woff.read_bytes()), "output_woff2_bytes": woff.stat().st_size, "source_cmap_sha256": sha(source_tables[b"cmap"]), "cmap_sha256": sha(tables[b"cmap"]), "cmap": {f"U+{cp:04X}": gid for cp, gid in sorted(cmap.items())}, "glyphs": struct.unpack_from(">H", tables[b"maxp"], 4)[0], "source_glyphs": source_glyphs, "output_glyphs": output_glyphs, "preserved_name_ids": [0, 5, 13, 14], "changed_name_ids": [1, 3, 4, 6], "added_name_ids": [10], "source_protected_names": _protected(source_tables), "output_protected_names": _protected(tables), "woff2_roundtrip_verified": True, "roundtrip_glyphs": roundtrip_glyphs, "roundtrip_table_policy": "All tables byte-identical except head checksum/required bit11 and WOFF2 glyf/loca serialization; each retained glyph outline, advance and extents is independently identical after decompression.", "harfbuzz_version": version, "authoring_tools": {k: {"program": Path(v[0]).name, "sha256": v[1]} for k, v in tools.items()}, "axes": "all upstream variable axes pinned to defaults; no variable tables retained", "outline_scope": "Four retained Junicode glyph outlines/advances match their upstream default instance; U+2610 matches the separately recorded project geometry. All five survive WOFF2 roundtrip unchanged; no broader shaping/corpus claim."}
    transport._json(out / "derivation.json", proof)
    return proof


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "hydrate", "author"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--local-bytes", action="store_true")
    parser.add_argument("--archive-dir", type=Path)
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--input", type=Path, help="author only: exact pinned JunicodeVF WOFF2")
    parser.add_argument("--out", type=Path, help="author only: fresh .scratch output directory")
    args = parser.parse_args(argv)
    if args.command == "check" and (args.fetch or args.archive_dir): parser.error("check never hydrates or downloads")
    if args.command != "author" and (args.input or args.out): parser.error("--input/--out require explicit author")
    if args.command == "author" and (not args.input or not args.out or args.fetch or args.archive_dir): parser.error("author requires --input/--out and never downloads")
    try:
        if args.command == "author": result = author(args.root, args.input, args.out)
        elif args.command == "hydrate": result = hydrate(args.root, archive_dir=args.archive_dir, fetch=args.fetch)
        else: result = check(args.root, local_bytes=args.local_bytes)
    except (OSError, ValueError, struct.error) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
