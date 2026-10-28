"""Reading-order recipes: v2 rows, proposal envelopes, unit mapping and registration."""
from __future__ import annotations

import copy
import gzip
import json
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.dont_write_bytecode = True
import _bullarium as b
import _bullarium_geometry as geometry

W, H, L0, MEASURE, R0, PITCH, TOP = 2000, 3000, 300, 600, 960, 50, 330
L1, R1 = L0 + MEASURE, R0 + MEASURE


def body_line(column, index, *, words=6, indent=0, short=False, prefix="w"):
    e0 = L0 if column == "L" else R0
    y0 = TOP + index * PITCH
    count = 4 if short else words
    step = (MEASURE - indent) // words
    entries = []
    for k in range(count):
        x0 = e0 + indent + k * step
        x1 = e0 + MEASURE if (k == count - 1 and not short) else x0 + step
        entries.append((f"{prefix}{column.lower()}{index}x{k}", (x0, y0, x1, y0 + 40)))
    return entries


def note_rows():
    """Two small-type page-foot note rows below a rule's gap at the foot of the left column."""
    rows = []
    for k, values in enumerate((["(1)", "Ex", "Regest.", "Vatic.", "notaa", "notab", "notac", "notad"],
                                ["notae", "notaf", "notag", "notah", "notai", "notaj", "notak", "notal"])):
        y0 = TOP + 18 * PITCH + 25 + k * 38
        rows.append([(value, (L0 + j * 70, y0, L0 + (j + 1) * 70, y0 + 28)) for j, value in enumerate(values)])
    return rows


def garbled_note_rows(first, gaps=None):
    """Small-type note rows below a wide gap whose mark OCR garbled (or lost).

    ``first`` is one row of WORD values, or a list of such rows; ``gaps``
    optionally gives the spacing above each row after the first (default 38).
    """
    rows = first if first and isinstance(first[0], list) else [first]
    out, y0 = [], TOP + 18 * PITCH + 25
    for k, values in enumerate(rows):
        y0 += (gaps[k - 1] if gaps else 38) if k else 0
        out.append([(value, (L0 + j * 70, y0, L0 + (j + 1) * 70, y0 + 28)) for j, value in enumerate(values)])
    return out


def page_lines(*, interleave=False, deadzone=False, mixed=False, fused=True, notes=False, note_rows=None,
               note_gaps=None):
    header = [[("An.", (100, 180, 140, 210)), ("C.", (140, 180, 170, 210)), ("1300", (170, 180, 280, 210))],
              [("BULLARIUM", (820, 180, 960, 210)), ("ROMANUM", (960, 180, 1100, 210))],
              [("17", (1450, 180, 1500, 210)), ("An.", (1600, 180, 1640, 210)), ("C.", (1640, 180, 1670, 210)),
               ("1300", (1670, 180, 1780, 210))]]
    left, right = [], []
    for i in range(20):
        indent = 40 if i in (0, 10) else 0
        line = body_line("L", i, indent=indent, short=(i == 9))
        if fused and i == 10:     # a marginal summary fused at the start of a body LINE
            line = [("Prooemium.", (150, TOP + i * PITCH + 5, L0 + indent, TOP + i * PITCH + 30))] + line
        if mixed and i == 14:     # marginal hyphen and first body word in one WORD
            line = [("-et", (L0 - 16, TOP + i * PITCH, L0 + 40, TOP + i * PITCH + 40))] + \
                   [(v, (x0 + 40 if j == 0 else x0, y0, x1, y1)) for j, (v, (x0, y0, x1, y1)) in enumerate(line)]
        if deadzone and i == 16:
            line = [(v, (L0 - 8.5 if j == 0 else x0, y0, x1, y1)) for j, (v, (x0, y0, x1, y1)) in enumerate(line)]
        if notes and i == 17:     # the body breaks a word at the foot of the column
            line = line[:-1] + [("fun-", line[-1][1])]
        if not ((notes or note_rows) and i >= 18):
            left.append(line)
        line = body_line("R", i, indent=40 if i in (0, 12) else 0, short=(i == 11))
        if fused and i == 5:      # a marginal summary fused at the end of a body LINE
            line = line + [("Clausulae", (R1 + 20, TOP + i * PITCH + 5, R1 + 150, TOP + i * PITCH + 30))]
        right.append(line)
    if notes:
        left += globals()["note_rows"]()
    elif note_rows:
        left += garbled_note_rows(note_rows, note_gaps)
    note = [[("summarium", (160, TOP + 11 * PITCH + 5, 290, TOP + 11 * PITCH + 30))]] if fused else []
    if interleave:
        body = left[:10] + right[:5] + left[10:] + note + right[5:]
    else:
        body = left + note + right
    return header + body


class Fixture:
    """A synthetic two-page volume with a blank leaf, its records and catalog."""

    def __init__(self, root, pages, baseline=False):
        self.root = root
        xml = bytearray(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE DjVuXML>\n<DjVuXML><BODY>')
        raw = bytearray()
        for number, lines in enumerate(pages, 1):
            xml.extend(f'<OBJECT usemap="vol_{number:04d}.djvu" width="{W}" height="{H}"><HIDDENTEXT>'.encode())
            for line in lines:
                xml.extend(b"<LINE>")
                for value, (x0, y0, x1, y1) in line:
                    extra = f",{int(y1) - 4}" if baseline else ""     # the five-value DjVu form ends in a baseline
                    xml.extend(f'<WORD coords="{int(x0)},{int(y1)},{int(x1)},{int(y0)}{extra}">{value}</WORD>'.encode())
                xml.extend(b"</LINE>")
                raw.extend((" ".join(v for v, _ in line) + "\n").encode())
            raw.extend(b"\n")
            xml.extend(b"</HIDDENTEXT></OBJECT>")
        xml.extend(b"</BODY></DjVuXML>")
        self.raw, self.xml = bytes(raw), bytes(xml)
        base = root / "src/sources/works/bullarium-romanum/volume-01/editions/1857-turin-latin"
        self.edition_path = base
        records = {}
        for key, name, payload in (("ocr", "ocr.txt", self.raw), ("xml", "ocr.xml", self.xml)):
            folder = base / "artifacts" / key
            b.write(folder / name, payload)
            record = {"schema": 1, "record_type": "artifact", "id": f"artifact.bullarium-romanum.volume-01.1857-turin-latin.{key}",
                      "edition_id": "edition.bullarium-romanum.volume-01.1857-turin-latin", "storage": "tracked",
                      "media_type": "text/plain" if key == "ocr" else "application/xml", "rights_status": "public-domain",
                      "rights_basis": "Identified 1857 printing.", "path": str((folder / name).relative_to(root)),
                      "sha256": b.sha(payload), "byte_size": len(payload), "source_url": f"https://example.org/{name}"}
            b.record(folder / "artifact.toml", record)
            records[key] = (record, str((folder / "artifact.toml").relative_to(root)))
        self.records = records
        self.container = {"work_id": "work.bullarium-romanum.volume-01", "edition_id": "edition.bullarium-romanum.volume-01.1857-turin-latin",
                          "edition_path": str(base.relative_to(root)),
                          "artifacts": {key: {"id": rec["id"], "sha256": rec["sha256"], "manifest": manifest}
                                        for key, (rec, manifest) in records.items()}}

    def catalog(self, units):
        b.write(self.root / b.CATALOG, b.json_bytes({"schema": "triptych-bullarium-catalog/v1",
                                                     "volumes": [{"volume": 1, "container": self.container}],
                                                     "units": units, "coverage": {}}))
        b.write(self.root / geometry.WITHDRAWALS, b.json_bytes({"affected_units": []}))

    def unit(self, number, ranges, **extra):
        rec = self.records["ocr"][0]
        return {"id": f"bullarium.volume-01.unit-{number:04d}", "volume": 1, "artifact_id": rec["id"],
                "artifact_sha256": rec["sha256"], "act_number_raw": str(number), "status": "held",
                "physical_line_ranges": ranges, **extra}


class ReadingOrderTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/bullarium_reconstruction/geometry_engine/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def volume(self, *pages, units=None, baseline=False):
        fixture = Fixture(self.root, list(pages) + [[]], baseline=baseline)
        fixture.catalog(units(fixture) if units else [])
        return fixture

    def propose(self, name="proposal"):
        geometry.propose(self.root, f".scratch/{name}", volume=1)
        return json.loads((self.root / f".scratch/{name}/recipe.json").read_bytes())

    def test_proposal_separates_margins_heads_and_columns(self):
        self.volume(page_lines())
        recipe = self.propose()
        page = recipe["pages"][0]
        self.assertEqual(page["status"], "reordered")
        self.assertEqual([p["status"] for p in recipe["pages"]], ["reordered", "empty"])
        codes = [row[0] for row in page["rows"]]
        self.assertEqual(codes[0], "H")
        self.assertLess(max(i for i, c in enumerate(codes) if c == "L"), min(i for i, c in enumerate(codes) if c == "R"))
        products = geometry.build(self.root, ".scratch/proposal/recipe.json", ".scratch/replay")
        text = (self.root / ".scratch/replay/hybrid.txt").read_text()
        self.assertIn("\n\n\tProoemium.\n\tsummarium\n\n", text)       # one block, TAB-led, before its section
        self.assertIn("\n\n\tClausulae\n\n", text)
        self.assertTrue(text.startswith("An. C. 1300 BULLARIUM ROMANUM 17 An. C. 1300\n\n"))
        self.assertLess(text.index("wl19x5"), text.index("wr0x0"))
        self.assertEqual(products["changed_pages"], 1)
        head = (self.root / ".scratch/proposal/running-heads.tsv").read_text().splitlines()
        self.assertEqual(head[0], "1\treordered\tAn. C. 1300 BULLARIUM ROMANUM 17 An. C. 1300")

    def test_v2_replay_is_byte_equivalent_to_its_explicit_v1_expansion(self):
        self.volume(page_lines(mixed=True, notes=True))
        self.propose()
        geometry.build(self.root, ".scratch/proposal/recipe.json", ".scratch/v2")
        recipe, raw, xml, _ = geometry.load_recipe(self.root, ".scratch/proposal/recipe.json")
        expanded = geometry.expand_v2(recipe, raw, xml)
        self.assertTrue(any(page["before"] == "" for page in expanded["changed_pages"]))
        b.write(self.root / ".scratch/v1.json", json.dumps(expanded).encode())
        geometry.build(self.root, ".scratch/v1.json", ".scratch/v1")
        for name in ("hybrid.txt", "page-map.json", "byte-map.json", "changed-word-map.jsonl.gz"):
            self.assertEqual((self.root / ".scratch/v2" / name).read_bytes(), (self.root / ".scratch/v1" / name).read_bytes(), name)
        v1, v2 = (json.loads((self.root / f".scratch/{n}/validation.json").read_text()) for n in ("v1", "v2"))
        self.assertEqual(v2.pop("recipe_schema"), geometry.SCHEMA_V2)
        self.assertNotIn("recipe_schema", v1)
        for item in (v1, v2):
            item.pop("recipe_sha256")
            item["outputs"].pop("validation.json", None)
        self.assertEqual(v1, v2)

    def test_page_initial_marginal_row_keeps_its_tab_in_both_schemas(self):
        self.volume(page_lines())
        recipe = self.propose()
        page = recipe["pages"][0]
        header = [row for row in page["rows"] if row[0] == "H"]
        rest = [row for row in page["rows"] if row[0] != "H"]
        page["rows"] = [["ML", "p", rest[0][2]]] + rest[1:] + [["H", "p", run] for row in header for run in [row[2]]]
        b.write(self.root / ".scratch/tab.json", json.dumps(recipe).encode())
        geometry.build(self.root, ".scratch/tab.json", ".scratch/tab")
        recipe2, raw, xml, _ = geometry.load_recipe(self.root, ".scratch/tab.json")
        expanded = geometry.expand_v2(recipe2, raw, xml)
        self.assertEqual(expanded["changed_pages"][0]["before"], "\t")
        b.write(self.root / ".scratch/tab-v1.json", json.dumps(expanded).encode())
        geometry.build(self.root, ".scratch/tab-v1.json", ".scratch/tab-v1")
        self.assertEqual((self.root / ".scratch/tab/hybrid.txt").read_bytes(), (self.root / ".scratch/tab-v1/hybrid.txt").read_bytes())

    def test_v2_rows_must_name_every_page_WORD_exactly_once(self):
        self.volume(page_lines())
        recipe = self.propose()
        rows = recipe["pages"][0]["rows"]
        first = rows[1][2][0][0]
        cases = {
            "duplicate": lambda r: r["pages"][0]["rows"].append(["L", "l", [[first, first]]]),
            "missing": lambda r: r["pages"][0]["rows"].pop(),
            "foreign": lambda r: r["pages"][0]["rows"].append(["L", "l", [[99999, 99999]]]),
            "bad code": lambda r: r["pages"][0]["rows"][1].__setitem__(0, "X"),
            "page order": lambda r: r["pages"].reverse(),
            "held with rows": lambda r: r["pages"][0].update(status="held", hold={"reason": "x"}),
        }
        for name, mutate in cases.items():
            with self.subTest(name):
                broken = copy.deepcopy(recipe)
                mutate(broken)
                b.write(self.root / ".scratch/broken.json", json.dumps(broken).encode())
                with self.assertRaises(geometry.GeometryError):
                    geometry.build(self.root, ".scratch/broken.json", ".scratch/broken-" + name.replace(" ", "-"))

    def test_margin_hyphen_joined_to_first_body_word_stays_with_the_body_and_is_recorded(self):
        self.volume(page_lines(mixed=True))
        page = self.propose()["pages"][0]
        self.assertEqual(page["status"], "reordered")
        self.assertEqual([reason for _, reason in page["inseparable_WORDs"]], ["margin-WORD-extent-enters-body-start"])
        wid = page["inseparable_WORDs"][0][0]
        role = next(code for code, _, runs in page["rows"] for a, z in runs if a <= wid <= z)
        self.assertEqual(role, "L")

    def straddle_page(self, *, left=None, right=None, margin_on_row=True):
        """page_lines() with left line 6 opening on a margin WORD (value, x1, height, body indent)
        and/or right line 3 ending on a body WORD (value, or (value, x0)) run 60 px past R1, beside
        a marginal block whose first row (on line 3 unless margin_on_row is false) is indented.
        Each call builds its own fixture root (source records are immutable)."""
        self.root = Path(tempfile.mkdtemp(dir=self.temp.name))
        lines = page_lines(fused=False)
        if left:
            value, x1, height, indent = left
            y0 = TOP + 6 * PITCH
            lines[3 + 6] = [(value, (120, y0, x1, y0 + height))] + body_line("L", 6, indent=indent, short=indent > 140)
        if right:
            k = 3 + 20 + 3
            y0 = TOP + 3 * PITCH
            body = lines[k]
            value, x0 = right if isinstance(right, tuple) else (right, body[-1][1][0])
            body = [w for w in body if w[1][2] <= x0] if isinstance(right, tuple) else body[:-1]
            # the LINE runs on to a marginal row printed beside it, or only to a speck
            lines[k] = body + [(value, (x0, y0, R1 + 60, y0 + 40)),
                               ("Confirmatio", (R1 + 62, y0 + 5, R1 + 200, y0 + 30)) if margin_on_row
                               else ("•", (R1 + 62, y0 + 12, R1 + 70, y0 + 20))]
            lines += [[(text, (R1 + 20, y0 + j * PITCH + 5, R1 + 150, y0 + j * PITCH + 30))]
                      for j, text in ((1, "litterarum"), (2, "fatarum."))]
        self.volume(lines)
        page = self.propose()["pages"][0]
        self.assertEqual(page["status"], "reordered")
        return page

    def test_a_margin_WORD_whose_box_holds_the_body_rows_start_is_inseparable(self):
        for left in (("dat,tantumper-tione", L0 + 90, 40, 90),  # beyond the widest paragraph indent
                     ("«a-p(", L0 + 60, 40, 60),                # an indent's width, but garbled OCR
                     ("ronontsdu-s", L0 + 61, 60, 61)):         # two margin rows and the body in one box
            with self.subTest(left=left[0]):
                page = self.straddle_page(left=left)
                self.assertEqual([reason for _, reason in page["inseparable_WORDs"]], ["margin-WORD-box-holds-body-start"])
                wid = page["inseparable_WORDs"][0][0]     # held, not reassigned: the value is the margin's
                self.assertEqual(next(code for code, _, runs in page["rows"] for a, z in runs if a <= wid <= z), "ML")

    def test_padded_margin_boxes_over_an_indent_a_gap_or_in_margin_type_are_not_straddles(self):
        for left in (("hic", L0 + 51, 40, 51),                  # the box stops in a paragraph indent
                     ("prohi-", L0 + 90, 20, 95),               # margin-size type cannot hold body glyphs
                     ("prae-", L0 + 66, 40, 311)):              # its LINE resumes far into a short row
            with self.subTest(left=left[0]):
                page = self.straddle_page(left=left)
                self.assertEqual(page["inseparable_WORDs"], [])

    def test_a_body_WORD_running_on_into_a_marginal_row_with_its_glyphs_is_inseparable(self):
        for right in ('operis""\'', ("Tmodj", R0)):        # marginal glyphs; one box over the whole measure
            with self.subTest(right=right):
                page = self.straddle_page(right=right)
                self.assertEqual([reason for _, reason in page["inseparable_WORDs"]], ["body-WORD-box-runs-into-right-margin"])
        for right, on_row in (("tempore", True),              # a padded box, no marginal glyphs
                              (("gestari.", R0), False)):     # a short last line's box over blank margin and a speck
            with self.subTest(right=right):
                page = self.straddle_page(right=right, margin_on_row=on_row)
                self.assertEqual(page["inseparable_WORDs"], [])
        self.assertTrue(geometry._junk_run_on("pro-„em,"))
        self.assertTrue(geometry._junk_run_on("eis-mo"))
        self.assertFalse(geometry._junk_run_on("evangelica™"))     # an ink blot
        self.assertFalse(geometry._junk_run_on("■'-nis"))
        self.assertFalse(geometry._junk_run_on("Iu-"))
        self.assertFalse(geometry._junk_run_on("eiusdem,"))

    def test_dead_zone_start_holds_the_page_without_guessing(self):
        self.volume(page_lines(deadzone=True))
        page = self.propose()["pages"][0]
        self.assertEqual((page["status"], page["hold"]["reason"]), ("held", "uncertain-WORD-role"))
        self.assertEqual(page["hold"]["detail"]["WORDs"][0][1], "left-edge-dead-zone")
        geometry.build(self.root, ".scratch/proposal/recipe.json", ".scratch/held")
        self.assertEqual((self.root / ".scratch/held/hybrid.txt").read_bytes(),
                         (self.root / "src/sources/works/bullarium-romanum/volume-01/editions/1857-turin-latin/artifacts/ocr/ocr.txt").read_bytes())

    def test_proposal_is_deterministic_and_refuses_to_replace_a_different_one(self):
        self.volume(page_lines())
        first = self.propose()
        self.assertEqual(self.propose(), first)
        path = self.root / ".scratch/proposal/recipe.json"
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "differing proposal"):
            self.propose()

    def test_measure_relative_thresholds_scale_with_the_printed_measure(self):
        self.volume(page_lines())
        native = geometry.source_pages(self.root, geometry._record_pin(self.root, self.records("ocr")),
                                       geometry._record_pin(self.root, self.records("xml")), [1])
        page = native["pages"][0]
        self.assertEqual(geometry.volume_measure([page]), MEASURE)
        m = geometry.measure_page(page, MEASURE)
        self.assertEqual((round(m["edges"]["L0"]["a"]), round(m["edges"]["R1"]["a"]), m["edges"]["L0"]["confirmed"]), (L0, R1, True))

    def records(self, key):
        return f"src/sources/works/bullarium-romanum/volume-01/editions/1857-turin-latin/artifacts/{key}/artifact.toml"

    def mapped(self, units, **page):
        self.volume(page_lines(**page), units=units)
        self.propose()
        geometry.build(self.root, ".scratch/proposal/recipe.json", ".scratch/replay")
        geometry.map_units(self.root, ".scratch/proposal/recipe.json", ".scratch/replay", ".scratch/mapping.json")
        return {u["unit_id"]: u for u in json.loads((self.root / ".scratch/mapping.json").read_text())["units"]}

    def test_unit_mapping_finds_a_clean_contiguous_range(self):
        rows = self.mapped(lambda f: [f.unit(1, [[1, 46]])])
        self.assertEqual(rows["bullarium.volume-01.unit-0001"]["category"], "clean")

    def test_unit_cut_on_raw_order_is_held_when_coordinate_order_interleaves_it(self):
        # raw order: left 1-10, right 1-5, left 11-20 ...: an old boundary after
        # right line 5 is not a boundary in coordinate order.
        rows = self.mapped(lambda f: [f.unit(1, [[1, 18]]), f.unit(2, [[19, 46]])], interleave=True)
        self.assertEqual(rows["bullarium.volume-01.unit-0001"]["category"], "hold:body-not-contiguous")

    def test_unit_with_an_inseparable_WORD_is_held(self):
        rows = self.mapped(lambda f: [f.unit(1, [[1, 46]])], mixed=True)
        self.assertEqual(rows["bullarium.volume-01.unit-0001"]["category"], "hold:inseparable-WORD")

    def registration_fixture(self):
        fixture = self.volume(page_lines(), units=lambda f: [f.unit(1, [[1, 46]])])
        review = {"unit_id": "bullarium.volume-01.unit-0001", "artifact_sha256": fixture.records["ocr"][0]["sha256"],
                  "physical_line_ranges": [[1, 46]], "decision": "admit", "printed_attribution": "wl0x1 wl0x2",
                  "title": "Titulus", "source_attribution_lines": [4, 4], "review_note": "Whole extent inspected.",
                  "reviewed_extent": "Entire selected raw extent; no image collation."}
        b.write(self.root / "review.json", b.json_bytes({"schema": "triptych-bullarium-boundary-reviews/v1", "reviews": [review]}))
        b.admit(self.root, [self.root / "review.json"], "2026-10-27T00:00:00Z")
        catalog = json.loads((self.root / b.CATALOG).read_text())
        unit = catalog["units"][0]
        unit.update(status="specifically-held", active_reader_status="source-order-hold",
                    review_history=[copy.deepcopy(unit["review"])],
                    review={**unit["review"], "decision": "hold", "review_note": "Synthetic confirmed fusion."})
        b.write(self.root / b.CATALOG, b.json_bytes(catalog))
        self.propose()
        geometry.build(self.root, ".scratch/proposal/recipe.json", ".scratch/replay")
        geometry.map_units(self.root, ".scratch/proposal/recipe.json", ".scratch/replay", ".scratch/mapping.json")
        b.write(self.root / ".scratch/units.json", json.dumps({"schema": "triptych-bullarium-reading-order-selection/v1",
                                                               "units": [unit["id"]]}).encode())
        return fixture, unit

    def snapshot(self, below="src"):
        return {p: p.read_bytes() for p in (self.root / below).rglob("*") if p.is_file()}

    def register(self):
        return geometry.register(self.root, ".scratch/proposal/recipe.json", ".scratch/replay", ".scratch/mapping.json",
                                 ".scratch/units.json", "2026-10-28T00:00:00Z")

    def test_register_appends_a_new_reading_selection_and_preserves_raw_pins(self):
        fixture, unit = self.registration_fixture()
        before = self.snapshot()
        result = self.register()
        after = self.snapshot()
        changed = {p for p in before if before[p] != after.get(p)}
        self.assertEqual({p.relative_to(self.root).as_posix() for p in changed}, {b.CATALOG})   # every other write is new
        for key in ("ocr", "xml"):      # raw artifact pins and bytes are untouched
            record, manifest = fixture.records[key]
            self.assertEqual(after[self.root / manifest], before[self.root / manifest])
            self.assertEqual(after[self.root / record["path"]], before[self.root / record["path"]])
        old_segment = self.root / unit["segment_path"]
        self.assertEqual(after[old_segment], before[old_segment])
        catalog = json.loads((self.root / b.CATALOG).read_text())
        child = next(u for u in catalog["units"] if u["id"].endswith(".reading-order"))
        self.assertEqual((child["status"], child["reading_selection_variant_of"], child["work_id"]),
                         ("admitted-mechanical-ocr-extent", unit["id"], unit["work_id"]))
        self.assertEqual(child["artifact_sha256"], result["derivative_sha256"])
        derived = tomllib.loads((self.root / next(d["manifest"] for k, d in catalog["volumes"][0]["container"]["artifacts"].items()
                                                  if k.startswith("reading_order_") and "recipe" not in k and "map" not in k
                                                  and "validation" not in k)).read_text())
        self.assertEqual((derived["artifact_type"], derived["derived_from"]),
                         ("coordinate-reading-order-ocr", fixture.records["ocr"][0]["id"]))
        for declared in catalog["volumes"][0]["container"]["artifacts"].values():
            if declared["id"].split(".")[-1].startswith("reading-order"):   # source-library: tracked artifacts carry a date
                self.assertEqual(tomllib.loads((self.root / declared["manifest"]).read_text())["retrieved"], "2026-10-28")
        document = json.loads((self.root / geometry.GEOMETRY_MANIFEST).read_text())["documents"][0]
        self.assertEqual((document["id"], document["artifact_id"]), (child["id"], derived["id"]))
        self.assertIn("marginal summaries are kept as separate blocks", document["source_note"])
        segment = tomllib.loads((self.root / document["segment_path"]).read_text())
        self.assertEqual(segment["artifact_sha256"], derived["sha256"])
        self.assertEqual(b.check(self.root, self.root / b.CATALOG)["status"], "ok")

    def test_register_replay_is_absent_or_identical(self):
        self.registration_fixture()
        self.register()
        frozen = self.snapshot()
        self.register()
        self.assertEqual(self.snapshot(), frozen)

    def test_register_refuses_a_differing_existing_artifact_before_any_write(self):
        self.registration_fixture()
        hybrid = (self.root / ".scratch/replay/hybrid.txt").read_bytes()
        key = "reading-order-" + b.sha(hybrid)[:12]
        target = self.root / "src/sources/works/bullarium-romanum/volume-01/editions/1857-turin-latin/artifacts" / key / "hybrid.txt"
        b.write(target, b"different bytes\n")
        frozen = self.snapshot()
        with self.assertRaisesRegex(ValueError, "immutable"):
            self.register()
        self.assertEqual(self.snapshot(), frozen)

    def test_register_refuses_a_unit_already_holding_the_canonical_edition_key(self):
        _, unit = self.registration_fixture()
        catalog = json.loads((self.root / b.CATALOG).read_text())
        catalog["units"][0]["edition_id"] = "edition.example.work.1857-turin-bullarium-volume-01-latin"
        b.write(self.root / b.CATALOG, b.json_bytes(catalog))
        frozen = self.snapshot()
        with self.assertRaisesRegex(ValueError, "canonical edition key"):
            self.register()
        self.assertEqual(self.snapshot(), frozen)

    def test_register_admits_only_units_mapped_clean(self):
        self.registration_fixture()
        mapping = json.loads((self.root / ".scratch/mapping.json").read_text())
        mapping["units"][0]["category"] = "review:margin-ownership-at-boundary"
        path = self.root / ".scratch/mapping.json"
        path.write_text(json.dumps(mapping))
        frozen = self.snapshot()
        with self.assertRaisesRegex(ValueError, "only units mapped 'clean'"):
            self.register()
        self.assertEqual(self.snapshot(), frozen)

    def test_page_foot_notes_are_a_separate_block_at_the_page_break(self):
        self.volume(page_lines(notes=True))
        page = self.propose()["pages"][0]
        codes = [row[0] for row in page["rows"]]
        self.assertEqual([row[1] for row in page["rows"] if row[0] == "NL"], ["p", "l"])
        self.assertGreater(min(i for i, c in enumerate(codes) if c == "NL"), max(i for i, c in enumerate(codes) if c == "R"))
        self.assertEqual(page["notes_blocks"][0]["side"], "notes-left")
        geometry.build(self.root, ".scratch/proposal/recipe.json", ".scratch/notes")
        text = (self.root / ".scratch/notes/hybrid.txt").read_text()
        self.assertIn("fun-\nwr0x0", text)                      # the body runs on across the column
        self.assertIn("\n\n(1) Ex Regest. Vatic. notaa notab notac notad\nnotae", text)
        self.assertNotIn("fun-\n(1)", text)

    def test_garbled_or_lost_marks_with_editorial_wording_are_notes(self):
        for first in (["t", "Ex", "Regest.", "in", "Secret.", "Brevium."],
                      ["{", "Alia", "reformatio", "in", "Pii", "IV"],
                      ["i", "Leg.", "forte", "ecclesiam", "(r.", "t.)."],
                      ["Ea", "omittit", "Mainardus,", "quia", "notum", "est"]):
            with self.subTest(first=first[0]):
                self.root = Path(tempfile.mkdtemp(dir=self.temp.name))
                self.volume(page_lines(note_rows=first))
                page = self.propose()["pages"][0]
                self.assertEqual([b["side"] for b in page["notes_blocks"]], ["notes-left"])

    def test_note_marks_hidden_by_OCR_specks_and_joined_WORDs(self):
        mark = lambda *values: geometry._note_mark([{"value": v} for v in values])
        self.assertTrue(mark("ti) Legitur ", "haec"))          # mark and first word in one WORD
        self.assertTrue(mark(".", "„,", "■", "I", "Cherubinus"))  # specks before the mark
        self.assertTrue(mark("(l)'Leg.", "f."))                # quote between mark and word
        self.assertTrue(mark("!", "Puerperam"))
        self.assertTrue(mark("■", "Haec", "moderatio"))           # the mark printed as a lone square
        self.assertFalse(mark("■", "haec"))
        cued = lambda *values: geometry._note_mark([{"value": v} for v in values], cue=True)
        self.assertFalse(mark("d", "Erectionem"))              # "1" read as d or f needs editorial wording
        self.assertTrue(cued("d", "Erectionem"))
        self.assertFalse(mark("f", "leges,"))
        self.assertTrue(cued("f", "leges,"))
        self.assertTrue(cued("1", ".", "Ex", "Regest."))       # the mark's period set apart
        self.assertTrue(geometry.NOTE_CUE.search("quid aliud deest (R. T.}."))
        self.assertTrue(geometry.NOTE_CUE.search("Ex Archiv. Vatic."))
        self.assertTrue(geometry.NOTE_CUE.search("(1) Ex arcliiv. Ecclesiae huius"))

    def test_section_signs_and_subscription_crosses_are_not_note_marks(self):
        mark = lambda *values: geometry._note_mark([{"value": v} for v in values])
        cued = lambda *values: geometry._note_mark([{"value": v} for v in values], cue=True)
        self.assertFalse(cued("§", "1.", "Cum", "itaque"))     # a section sign is not a speck
        self.assertFalse(cued("§", "1", ".", "Praestantia"))
        self.assertFalse(cued("8", "2.", "Cum", "autem"))      # "§ 2." read as "8 2."
        self.assertFalse(cued("8", "1", ".", "Nullus"))
        self.assertFalse(mark("I", "2.", "Non", "praemissis"))
        self.assertFalse(cued("^", "A.", "Ipsorum"))          # "§" read as "^"
        self.assertFalse(mark("f", "Ego", "Antonius"))        # the cross before a subscription
        self.assertFalse(cued("'", "i", "•", "■n", "•"))      # OCR specks, not a note's words

    def test_editorial_wording_in_a_later_note_does_not_corroborate_a_bare_mark(self):
        self.volume(page_lines(note_rows=[["1", "taluni", "romae", "apud", "sanctum", "petrum"],
                                          ["romae", "apud", "sanctum", "petrum", "dicta"],
                                          ["(1)", "Ex", "Regest.", "Vatic.", "notaa", "notab"]]))
        page = self.propose()["pages"][0]
        self.assertEqual([(b["side"], b["rows"]) for b in page["notes_blocks"]], [("notes-left", 1)])

    def test_a_synopsis_closing_with_sigla_above_the_notes_rule_space_stays_body(self):
        self.volume(page_lines(note_rows=[["Exordium.", "Ecclesias", "quas", "monasterium", "possidet"],
                                          ["sub", "protectione", "suscipit", "(r.", "t.)"],
                                          ["(1)", "Ex", "archiv.", "Ecclesiae", "huius", "edidit"]],
                               note_gaps=[38, 60]))
        page = self.propose()["pages"][0]
        self.assertEqual([(b["side"], b["rows"]) for b in page["notes_blocks"]], [("notes-left", 1)])

    def test_editorial_wording_later_in_the_note_corroborates_a_bare_mark(self):
        self.volume(page_lines(note_rows=[["1", "florum", "generalem", "reformationem", "habes", "in"],
                                          ["Const.", "praec;", "declarationem", "autem", "illius", "et"],
                                          ["in", "subseq.", "(r.", "t.)."]]))
        page = self.propose()["pages"][0]
        self.assertEqual([(b["side"], b["rows"]) for b in page["notes_blocks"]], [("notes-left", 3)])

    def test_a_continued_note_closing_with_editorial_wording_joins_the_note_block(self):
        self.volume(page_lines(note_rows=[["libet", "referre", "haec", "acta,", "quibus", "post"],
                                          ["pacemque", "ei", "reddit.", "(r.", "t.)"],
                                          ["(1)", "Ex", "Baronio", "ad", "annum", "1122."]]))
        page = self.propose()["pages"][0]
        self.assertEqual([(b["side"], b["rows"]) for b in page["notes_blocks"]], [("notes-left", 3)])

    def test_body_like_rows_are_not_notes(self):
        mark = lambda *values: geometry._note_mark([{"value": v} for v in values])
        self.assertTrue(mark("(1)", "Ex"))
        self.assertTrue(mark("(1)Ex", "Regest."))
        self.assertTrue(mark("\\", "Ex"))
        self.assertTrue(mark("i", "Leg."))
        self.assertFalse(mark("1", "ad"))                   # "1 ad 4." in a synopsis
        self.assertFalse(mark("1.", "Ouuritur"))            # a synopsis's first item
        self.assertTrue(geometry._note_mark([{"value": "1."}, {"value": "Foulaninus"}], cue=True))
        self.assertFalse(mark("(juomodolibet", "ac"))       # body word read with a bracket
        self.assertFalse(mark("[)at.", "die"))              # a dating line's "Dat."
        self.assertFalse(mark("§", "1."))

    def test_unmarked_small_rows_after_a_heading_gap_stay_body(self):
        lines = page_lines()
        lines[-1] = [(v.replace("wr19", "summ"), (x0, y0 + 30, x1, y1 + 2)) for v, (x0, y0, x1, y1) in lines[-1]]
        self.volume(lines)
        page = self.propose()["pages"][0]
        self.assertEqual(page["notes_blocks"], [])

    def test_unit_keeps_its_page_foot_notes(self):
        rows = self.mapped(lambda f: [f.unit(1, [[1, 46]])], notes=True)
        self.assertEqual(rows["bullarium.volume-01.unit-0001"]["category"], "clean")

    def test_notes_displaced_past_the_next_unit_become_an_extra_range(self):
        rows = self.mapped(lambda f: [f.unit(1, [[1, 24]]), f.unit(2, [[25, 46]])], notes=True)
        first, second = rows["bullarium.volume-01.unit-0001"], rows["bullarium.volume-01.unit-0002"]
        self.assertEqual((first["category"], second["category"]), ("clean", "clean"))
        self.assertEqual(len(first["new_physical_line_ranges"]), 2)
        self.assertLess(second["new_physical_line_ranges"][0][1], first["new_physical_line_ranges"][1][0])

    def test_raw_line_numbers_are_labelled_in_reader_notes(self):
        self.assertEqual(geometry._raw_line_note("Retain source note12296–12298 and LF 15845; exclude nextXV54890."),
                         "Retain source note (raw OCR line 12296–12298) and raw OCR line 15845; exclude next XV (raw OCR line 54890).")

    def test_supersede_appends_a_replacement_reading_and_keeps_the_prior_one(self):
        fixture, unit = self.registration_fixture()
        self.register()
        prior = json.loads((self.root / b.CATALOG).read_text())
        prior_child = next(u for u in prior["units"] if u["id"] == unit["id"] + ".reading-order")
        recipe = json.loads((self.root / ".scratch/proposal/recipe.json").read_text())
        row = next(r for r in recipe["pages"][0]["rows"] if r[0] == "L" and r[1] == "l")
        row[1] = "p"                                          # a different, still conserving derivative
        b.write(self.root / ".scratch/v2/recipe.json", json.dumps(recipe).encode())
        geometry.build(self.root, ".scratch/v2/recipe.json", ".scratch/v2/replay")
        geometry.map_units(self.root, ".scratch/v2/recipe.json", ".scratch/v2/replay", ".scratch/v2/mapping.json")
        keep = [self.root / prior_child["segment_path"], self.root / prior_child["segment_path"].replace("/segments/source-ocr.toml", "/edition.toml"),
                self.root / geometry.GEOMETRY_MANIFEST]
        frozen = {path: path.read_bytes() for path in keep}
        call = lambda: geometry.register(self.root, ".scratch/v2/recipe.json", ".scratch/v2/replay", ".scratch/v2/mapping.json",
                                         ".scratch/units.json", "2026-10-29T00:00:00Z", supersede=True, reason="Synthetic replacement.")
        result = call()
        self.assertEqual(result["superseded_readings"], 1)
        self.assertEqual({path: path.read_bytes() for path in keep}, frozen)
        catalog = json.loads((self.root / b.CATALOG).read_text())
        units = {u["id"]: u for u in catalog["units"]}
        self.assertEqual(units[prior_child["id"]], prior_child)
        child = units[unit["id"] + ".reading-order-v2"]
        self.assertEqual((child["reading_selection_variant_of"], child["work_id"], child["status"]),
                         (prior_child["id"], prior_child["work_id"], "admitted-mechanical-ocr-extent"))
        self.assertTrue(child["edition_id"].endswith("-reading-order-v2-latin"))
        corrections = json.loads((self.root / geometry.READING_ORDER_CORRECTIONS).read_text())
        self.assertEqual([s["prior"]["id"] for s in corrections["supersessions"]], [prior_child["id"]])
        self.assertEqual(corrections["documents"][0]["id"], child["id"])
        self.assertEqual(b.check(self.root, self.root / b.CATALOG)["status"], "ok")
        snapshot = self.snapshot()
        call()
        self.assertEqual(self.snapshot(), snapshot)

    def test_supersede_requires_a_reason_and_a_prior_reading(self):
        self.registration_fixture()
        with self.assertRaisesRegex(ValueError, "nothing to supersede"):
            geometry.register(self.root, ".scratch/proposal/recipe.json", ".scratch/replay", ".scratch/mapping.json",
                              ".scratch/units.json", "2026-10-29T00:00:00Z", supersede=True, reason="x")
        with self.assertRaisesRegex(ValueError, "explicit --reason"):
            geometry.register(self.root, ".scratch/proposal/recipe.json", ".scratch/replay", ".scratch/mapping.json",
                              ".scratch/units.json", "2026-10-29T00:00:00Z", supersede=True)

    def withdrawal(self, *ids, pdf=None, name="withdraw.json"):
        readings = [{"id": i, "pdf_sha256": pdf} for i in ids]
        b.write(self.root / ".scratch" / name, json.dumps({"schema": geometry.WITHDRAWAL_SELECTION_SCHEMA,
                                                           "readings": readings}).encode())
        return ".scratch/" + name

    def plan(self):
        from _papal_collection import plan_sources
        docs = self.root / "src/sources/papal-documents"
        corrections = [{"name": n, "path": docs / f} for n, f in (
            ("bullarium-reading-order-corrections", "bullarium-reading-order-corrections-manifest.json"),
            ("bullarium-reading-order-withdrawals", "bullarium-reading-order-withdrawals-manifest.json")) if (docs / f).exists()]
        bases = [{"name": n, "path": docs / f} for n, f in (
            ("bullarium-geometry", "bullarium-geometry-manifest.json"),
            ("bullarium-geometry-fragments", "bullarium-geometry-fragment-manifest.json")) if (docs / f).exists()]
        return plan_sources(bases, corrections, self.root / ".scratch/plan.json")["selection_plan"]["summary"]

    def test_withdraw_holds_the_reading_and_records_a_null_supersession(self):
        _, unit = self.registration_fixture()
        self.register()
        reading_id = unit["id"] + ".reading-order"
        prior = next(u for u in json.loads((self.root / b.CATALOG).read_text())["units"] if u["id"] == reading_id)
        base = (self.root / geometry.GEOMETRY_MANIFEST).read_bytes()
        call = lambda: geometry.withdraw(self.root, self.withdrawal(reading_id), "2026-10-29T00:00:00Z",
                                         "Synthetic straddling WORD.", "a" * 64)
        self.assertEqual(call()["withdrawn_readings"], 1)
        units = {u["id"]: u for u in json.loads((self.root / b.CATALOG).read_text())["units"]}
        held = units[reading_id]
        self.assertEqual((held["status"], held["review"]["decision"], held["reader_withdrawal_evidence_sha256"]),
                         ("specifically-held", "hold", "a" * 64))
        self.assertEqual(held["review_history"][-1], prior["review"])
        self.assertIn("Synthetic straddling WORD.", held["review"]["review_note"])
        manifest = json.loads((self.root / geometry.READING_ORDER_WITHDRAWALS).read_text())
        self.assertEqual(manifest["supersessions"], [held["reader_withdrawal"]])
        self.assertIsNone(held["reader_withdrawal"]["replacement"])
        self.assertNotIn("pdf_sha256", held["reader_withdrawal"]["prior"])     # never installed
        self.assertEqual((self.root / geometry.GEOMETRY_MANIFEST).read_bytes(), base)
        self.assertEqual(b.check(self.root, self.root / b.CATALOG)["status"], "ok")
        summary = self.plan()
        self.assertEqual((summary["withdrawals"], summary["selected"]), (1, 0))
        snapshot = self.snapshot()
        self.assertEqual(call()["withdrawn_readings"], 0)      # an identical rerun changes nothing
        self.assertEqual(self.snapshot(), snapshot)
        with self.assertRaisesRegex(ValueError, "already withdrawn differently"):
            geometry.withdraw(self.root, self.withdrawal(reading_id), "2026-10-29T00:00:00Z", "Another reason.", "a" * 64)

    def test_withdraw_reaches_a_replacement_reading_and_pins_an_installed_pdf(self):
        _, unit = self.registration_fixture()
        self.register()
        recipe = json.loads((self.root / ".scratch/proposal/recipe.json").read_text())
        row = next(r for r in recipe["pages"][0]["rows"] if r[0] == "L" and r[1] == "l")
        row[1] = "p"
        b.write(self.root / ".scratch/v2/recipe.json", json.dumps(recipe).encode())
        geometry.build(self.root, ".scratch/v2/recipe.json", ".scratch/v2/replay")
        geometry.map_units(self.root, ".scratch/v2/recipe.json", ".scratch/v2/replay", ".scratch/v2/mapping.json")
        geometry.register(self.root, ".scratch/v2/recipe.json", ".scratch/v2/replay", ".scratch/v2/mapping.json",
                          ".scratch/units.json", "2026-10-29T00:00:00Z", supersede=True, reason="Synthetic replacement.")
        v1, v2 = unit["id"] + ".reading-order", unit["id"] + ".reading-order-v2"
        args = ("2026-10-30T00:00:00Z", "Synthetic straddling WORD.", "b" * 64)
        with self.assertRaisesRegex(ValueError, "withdrawn through its replacement"):
            geometry.withdraw(self.root, self.withdrawal(v1), *args)
        b.write(self.root / geometry.RELEASE, json.dumps({"documents": [{"id": v2, "language": "la", "pdf_sha256": "c" * 64}]}).encode())
        for pdf in (None, "d" * 64):
            with self.subTest(pdf=pdf), self.assertRaisesRegex(ValueError, "exact release PDF"):
                geometry.withdraw(self.root, self.withdrawal(v2, pdf=pdf), *args)
        geometry.withdraw(self.root, self.withdrawal(v2, pdf="c" * 64), *args)
        manifest = json.loads((self.root / geometry.READING_ORDER_WITHDRAWALS).read_text())
        self.assertEqual([(x["prior"]["id"], x["prior"]["pdf_sha256"]) for x in manifest["supersessions"]], [(v2, "c" * 64)])
        self.assertEqual(b.check(self.root, self.root / b.CATALOG)["status"], "ok")
        summary = self.plan()      # the replacement is planned from the corrections, then withdrawn
        self.assertEqual((summary["source_supersessions"], summary["withdrawals"], summary["selected"]), (1, 1, 0))

    def test_withdraw_refuses_incomplete_or_unknown_selections_before_any_write(self):
        _, unit = self.registration_fixture()
        self.register()
        reading_id = unit["id"] + ".reading-order"
        good, unknown = self.withdrawal(reading_id, name="good.json"), self.withdrawal(unit["id"] + ".reading-order-v7", name="unknown.json")
        pinned = self.withdrawal(reading_id, pdf="e" * 64, name="pinned.json")
        before = self.snapshot()
        cases = ((good, "bad", "x", "a" * 64, "whole-second UTC"),
                 (good, "2026-10-29T00:00:00Z", " ", "a" * 64, "explicit --reason"),
                 (good, "2026-10-29T00:00:00Z", "x", "A" * 64, "evidence-sha256"),
                 (unknown, "2026-10-29T00:00:00Z", "x", "a" * 64, "no registered reading"),
                 (pinned, "2026-10-29T00:00:00Z", "x", "a" * 64, "uninstalled reading"))
        for path, revision, reason, evidence, message in cases:
            with self.subTest(message), self.assertRaisesRegex(ValueError, message):
                geometry.withdraw(self.root, path, revision, reason, evidence)
        self.assertEqual(self.snapshot(), before)

    def test_five_value_coords_give_the_same_geometry_and_text(self):
        outputs, base = {}, self.root
        for baseline in (False, True):
            with self.subTest(baseline=baseline):
                self.root = base / ("five" if baseline else "four")     # each fixture needs its own source tree
                self.volume(page_lines(notes=True), baseline=baseline)
                name = "five" if baseline else "four"
                recipe = self.propose(name)
                geometry.build(self.root, f".scratch/{name}/recipe.json", f".scratch/{name}-replay")
                outputs[name] = (recipe["pages"], (self.root / f".scratch/{name}-replay/hybrid.txt").read_bytes())
                recipe2, raw, xml, _ = geometry.load_recipe(self.root, f".scratch/{name}/recipe.json")
                expanded = geometry.expand_v2(recipe2, raw, xml)
                if baseline:
                    self.assertTrue(all(w["coords"].count(",") == 4 for p in expanded["changed_pages"] for w in p["words"]))
                b.write(self.root / f".scratch/{name}-v1.json", json.dumps(expanded).encode())
                geometry.build(self.root, f".scratch/{name}-v1.json", f".scratch/{name}-v1")
                self.assertEqual((self.root / f".scratch/{name}-v1/hybrid.txt").read_bytes(), outputs[name][1])
        self.assertEqual(outputs["four"], outputs["five"])

    def test_six_value_coords_are_refused(self):
        self.volume(page_lines())
        recipe = self.propose()
        xml_path = self.root / "src/sources/works/bullarium-romanum/volume-01/editions/1857-turin-latin/artifacts/xml/ocr.xml"
        bad = xml_path.read_bytes().replace(b'coords="', b'coords="1,1,', 1)      # six values
        self.assertNotEqual(bad, xml_path.read_bytes())
        with self.assertRaisesRegex(ValueError, "exact integer coordinates"):
            geometry._xml_pages(bad, (self.root / recipe["source_txt"]["path"]).read_bytes(),
                                geometry._tokens((self.root / recipe["source_txt"]["path"]).read_bytes()),
                                {page["leaf"]: {} for page in recipe["pages"]})

    def test_verbs_refuse_unsafe_inputs_before_reading_sources(self):
        cases = (
            (["propose", "--volume", "4", "--out", "../outside", "--json"], "without traversal"),
            (["map-units", "--recipe", "x.json", "--replay", "x", "--out", "../outside.json", "--json"], "without traversal"),
            (["register", "--recipe", "x", "--replay", "x", "--mapping", "x", "--units", "x", "--revision", "bad", "--json"], "whole-second UTC"),
            (["withdraw", "--units", "x", "--revision", "bad", "--reason", "x", "--evidence-sha256", "x", "--json"], "whole-second UTC"),
        )
        for argv, message in cases:
            with self.subTest(argv[0]):
                import contextlib
                import io
                stream = io.StringIO()
                with contextlib.redirect_stderr(stream):
                    self.assertEqual(geometry.main(["--root", str(self.root)] + argv), 2)
                self.assertIn(message, stream.getvalue())


if __name__ == "__main__":
    unittest.main()
