"""Research screening preserves source identity and never converts silence to clearance."""
from __future__ import annotations

import contextlib
import copy
import gzip
import hashlib
from html import escape
import io
import json
import re
from pathlib import Path
import shlex
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _bullarium_geometry as geometry
import _bullarium_screen as screen


class ScreenTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/bullarium_reconstruction/geometry_screen_engine/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.out = ".scratch/output"
        self.raw_path, self.xml_path = self.root / "raw.txt", self.root / "source.xml"
        self.frontier_path, self.catalog_path, self.map_path = (self.root / name for name in ("frontier.json", "catalog.json", "inputs.json"))
        self.private = "file://PRIVATE-HOST-CACHE/book.djvu"
        self.raw, self.xml = bytearray(), bytearray(b'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE DjVuXML><DjVuXML><BODY>')
        self.markers, pages = {}, []
        for leaf in (1, 2):
            first = self.raw.count(b"\n") + 1
            page_byte_start = len(self.raw)
            self.xml.extend(f'<OBJECT data="{self.private}" usemap="book_{leaf:04d}.djvu" width="1000" height="1000"><HIDDENTEXT>'.encode())
            for i in range(12):
                self.line(self.prose("left", 150 + 40 * i))
                self.line(self.prose("right", 150 + 40 * i))
            self.markers[f"caption{leaf}"] = self.line([("separate", 80, 700, 130, 720), ("caption", 135, 700, 180, 720)])
            if leaf == 1:
                self.markers["mixed"] = self.line(self.prose("left", 720) + [("margin", 120, 720, 170, 740)])
                self.markers["multitoken"] = self.line([("margin body", 150, 750, 230, 770)] + self.prose("left", 750)[1:])
                words = self.prose("left", 800)
                words[-1] = ("literal-", *words[-1][1:])
                self.markers["hyphen"] = self.line(words + [("outward", 120, 800, 170, 820)])
                self.line(self.prose("left", 840))
                self.markers["backward"] = self.line(self.prose("left", 250))
                self.markers["both"] = self.line(self.prose("left", 880)[:3] + self.prose("right", 880)[:3])
                self.markers["partial"] = self.line([("first second", 200, 900, 350, 920)], break_WORD=True)
            self.xml.extend(b"</HIDDENTEXT></OBJECT>")
            pages.append({"artifact_page": leaf, "leaf": leaf, "physical_line_start": first,
                          "physical_line_end": self.raw.count(b"\n"),
                          "tokens": len(self.raw[page_byte_start:].decode().split())})
        self.xml.extend(b"</BODY></DjVuXML>")
        self.raw_path.write_bytes(self.raw)
        self.xml_path.write_bytes(self.xml)
        self.line_map_path = self.root / "sources/line-map/line-map.json"
        self.line_map = {"schema": "triptych-bullarium-line-map/v1", "ocr_sha256": screen._sha(self.raw),
                         "xml_sha256": screen._sha(self.xml), "physical_line_count": self.raw.count(b"\n"),
                         "token_count": len(self.raw.decode().split()), "pages": pages}
        self.ocr_id, self.xml_id, self.line_id = "artifact.fixture.ocr", "artifact.fixture.xml", "artifact.fixture.lines"
        self.container = {"artifacts": {
            "ocr": {"id": self.ocr_id, "manifest": "sources/ocr/artifact.toml", "sha256": screen._sha(self.raw)},
            "xml": {"id": self.xml_id, "manifest": "sources/xml/artifact.toml", "sha256": screen._sha(self.xml)}},
            "line_map_id": self.line_id, "line_map_path": str(self.line_map_path.relative_to(self.root))}
        self.rows = []
        self.units = []
        for name, ranges in (("positive", [[self.markers["mixed"], self.markers["mixed"]]]),
                             ("negative", [[pages[1]["physical_line_start"], pages[1]["physical_line_end"]]]),
                             ("partial", [[self.markers["partial"], self.markers["partial"]]]),
                             ("all", [[1, pages[0]["physical_line_end"]]])):
            identity = "bullarium.fixture." + name
            self.rows.append({"unit_id": identity, "current_document_id": identity, "volume": 1,
                              "artifact_id": self.ocr_id, "artifact_sha256": screen._sha(self.raw),
                              "physical_line_ranges": ranges})
            self.units.append({"id": identity, "volume": 1, "status": "admitted-mechanical-ocr-extent",
                               "artifact_id": self.ocr_id, "artifact_sha256": screen._sha(self.raw),
                               "physical_line_ranges": ranges})
        self.frontier = {"schema": screen.FRONTIER_SCHEMA, "rows": self.rows,
                         "catalog_receipt": {"sha256": "0" * 64, "revision": "old snapshot"}}
        self.catalog = {"schema": "triptych-bullarium-catalog/v1", "units": self.units,
                        "volumes": [{"volume": 1, "container": self.container}]}
        self.recipe = {"schema": screen.MAP_SCHEMA, "inputs": {self.xml_id: "source.xml", self.ocr_id: "raw.txt"},
                       "controls": {"bullarium.fixture.positive": "mixed-row-positive",
                                    "bullarium.fixture.negative": "no-mixed-row-observed"}}
        self.refresh()

    def tearDown(self):
        self.temp.cleanup()

    @staticmethod
    def prose(side, y):
        x = 200 if side == "left" else 520
        return [("body" + str(i), x + 56 * i, y, x + 56 * (i + 1), y + 20) for i in range(5)]

    def line(self, words, break_WORD=False):
        first = self.raw.count(b"\n") + 1
        self.xml.extend(b"<LINE>")
        for value, x0, y0, x1, y1 in words:
            self.xml.extend(f'<WORD coords="{x0},{y1},{x1},{y0}">{escape(value)}</WORD>'.encode())
        self.xml.extend(b"</LINE>")
        text = " ".join(value for value, *bbox in words)
        if break_WORD:
            text = text.replace(" ", "\n", 1)
        self.raw.extend((text + "\n").encode())
        return first

    def record(self, path, identity, payload, source_path=None):
        record = {"schema": 1, "record_type": "artifact", "id": identity,
                  "sha256": screen._sha(payload), "byte_size": len(payload)}
        if source_path:
            record["path"] = source_path
        path = self.root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(f"{key} = {json.dumps(value)}" for key, value in record.items()) + "\n")

    def refresh(self):
        raw, xml = self.raw_path.read_bytes(), self.xml_path.read_bytes()
        self.line_map["ocr_sha256"], self.line_map["xml_sha256"] = screen._sha(raw), screen._sha(xml)
        self.container["artifacts"]["ocr"]["sha256"] = screen._sha(raw)
        self.container["artifacts"]["xml"]["sha256"] = screen._sha(xml)
        self.line_map_path.parent.mkdir(parents=True, exist_ok=True)
        self.line_map_path.write_bytes(screen._bytes(self.line_map))
        self.record("sources/ocr/artifact.toml", self.ocr_id, raw, "raw.txt")
        self.record("sources/xml/artifact.toml", self.xml_id, xml)
        self.record("sources/line-map/artifact.toml", self.line_id, self.line_map_path.read_bytes())
        self.frontier_path.write_bytes(screen._bytes(self.frontier))
        self.catalog_path.write_bytes(screen._bytes(self.catalog))
        self.recipe.update(frontier=screen._pin(self.frontier_path), catalog=screen._pin(self.catalog_path))
        self.map_path.write_bytes(screen._bytes(self.recipe))

    def run_screen(self, **kwargs):
        return screen.screen(self.root, "frontier.json", "catalog.json", "inputs.json", self.out, **kwargs)

    def report(self):
        return json.loads((self.root / self.out / "screen.json").read_bytes())

    def test_exact_sources_one_extraction_and_deterministic_cache_replay(self):
        before = self.raw_path.read_bytes(), self.xml_path.read_bytes()
        with patch.object(geometry, "source_pages", wraps=geometry.source_pages) as extract:
            first = self.run_screen()
            self.assertEqual(extract.call_count, 1)
            self.assertEqual(extract.call_args.args[3], [1, 2])
        with patch.object(geometry, "source_pages", side_effect=AssertionError("unexpected extraction")):
            second = self.run_screen()
        self.assertEqual(first, second)
        self.assertEqual(before, (self.raw_path.read_bytes(), self.xml_path.read_bytes()))
        self.assertNotIn(self.private, json.dumps(self.report()))
        self.assertNotIn("source.xml", json.dumps(self.report()))
        for cache in (self.root / self.out / "native-cache").rglob("leaf-*.json.gz"):
            page = json.loads(gzip.decompress(cache.read_bytes()))
            self.assertRegex(page["full_page_tokens_sha256"], r"^[a-f0-9]{64}$")
            self.assertNotIn(self.private, json.dumps(page))

    def test_five_value_coords_screen_exactly_like_four_value_coords(self):
        def summary(out):
            report = json.loads((self.root / out / "screen.json").read_bytes())
            return [(row["unit_id"], row["status"], [(flag["kind"], [w["source_bbox"] for w in flag["WORDs"]])
                                                     for flag in row["flags"]]) for row in report["results"]]
        self.run_screen()
        four = summary(self.out)
        five_xml = re.sub(rb'coords="(-?\d+),(-?\d+),(-?\d+),(-?\d+)"',
                          lambda m: b'coords="%s,%s,%s,%s,%d"' % (*m.groups(), int(m[2]) - 3), self.xml_path.read_bytes())
        self.assertNotEqual(five_xml, self.xml_path.read_bytes())
        self.xml_path.write_bytes(five_xml)
        self.refresh()
        self.out = ".scratch/output-five"
        self.run_screen()
        self.assertEqual(summary(self.out), four)
        self.assertTrue(any(flag["WORDs"][0]["coords"].count(",") == 4
                            for row in self.report()["results"] for flag in row["flags"]))

    def test_positive_negative_and_pure_caption_are_not_clearance(self):
        self.run_screen()
        rows = {row["unit_id"]: row for row in self.report()["results"]}
        self.assertEqual(rows["bullarium.fixture.positive"]["status"], "FLAGGED")
        self.assertEqual(rows["bullarium.fixture.negative"]["status"], "NO_SIGNAL_NOT_CLEAR")
        self.assertFalse(rows["bullarium.fixture.negative"]["flags"])
        self.assertTrue(all(not c["false_mixed_flag"] and not c["missed_positive"] for c in self.report()["calibration"]))

    def test_concrete_signals_retain_WORD_value_byte_coords_and_literal_hyphen(self):
        self.run_screen()
        row = next(row for row in self.report()["results"] if row["unit_id"] == "bullarium.fixture.all")
        kinds = {flag["kind"] for flag in row["flags"]}
        self.assertTrue({"mixed-native-line-and-LF", "both-candidate-bands-selected-native-line",
                         "indivisible-multitoken-WORD-crosses-edge", "literal-hyphen-outward-WORDs-before-next-core",
                         "same-candidate-band-large-backward-y"} <= kinds)
        for flag in row["flags"]:
            for word in flag["WORDs"]:
                a, z = word["source_xml_byte_range_0"]
                self.assertIn(word["coords"].encode(), self.xml_path.read_bytes()[a:z])
                self.assertTrue(word["source_txt_token_byte_ranges_0"])
        self.assertTrue(any(w["value"] == "literal-" for f in row["flags"] for w in f["WORDs"]))

    def test_partial_multitoken_WORD_never_reports_no_signal(self):
        self.run_screen()
        row = next(row for row in self.report()["results"] if row["unit_id"] == "bullarium.fixture.partial")
        self.assertEqual(row["status"], "FLAGGED")
        self.assertTrue(row["partial_WORD_selection"])
        self.assertEqual(row["flags"][0]["WORDs"][0]["value"], "first second")

    def test_ambiguous_fit_and_sparse_page_remain_UNKNOWN(self):
        native = geometry.source_pages(self.root,
            {"artifact_id": self.ocr_id, **screen._pin(self.raw_path)},
            {"artifact_id": self.xml_id, **screen._pin(self.xml_path)}, [2], input_map=self.recipe["inputs"])
        page = native["pages"][0]
        page["words"] = page["words"][:5]
        self.assertTrue(all(band["status"] == "UNKNOWN" for band in screen.fit_bands(page).values()))
        self.assertEqual(len(screen.screen_page(page, [[1, 1000]])["unknown_candidate_bands"]), 2)

    def test_current_selection_change_is_explicit_unknown(self):
        self.units[0]["physical_line_ranges"] = [[1, 1]]
        self.refresh()
        self.run_screen()
        row = next(row for row in self.report()["results"] if row["unit_id"] == "bullarium.fixture.positive")
        self.assertEqual(row["status"], "UNKNOWN")
        self.assertIn("disagree", row["unknown_reasons"][0])

    def test_withdrawn_positive_control_is_preserved_with_current_document_ID(self):
        unit, row = self.units[0], self.rows[0]
        unit["active_reader_status"] = "source-order-hold"
        unit["status"] = "specifically-held"
        unit["active_render_selection"] = {"id": row["current_document_id"], "physical_line_ranges": row["physical_line_ranges"],
                                           "artifact_id": self.ocr_id, "sha256": row["artifact_sha256"], "status": "withdrawn-source-order"}
        self.refresh()
        self.run_screen()
        found = next(r for r in self.report()["results"] if r["unit_id"] == row["unit_id"])
        self.assertEqual(found["current_reader_status"], "source-order-hold")
        self.assertEqual(found["control"], "mixed-row-positive")

    def active_segment_fixture(self):
        row = self.rows[0]
        path = self.root / "src/sources/works/fixture/positive/editions/1857-latin/segments/source-ocr.toml"
        segment = {"schema": 2, "record_type": "segment", "id": "segment.fixture.positive",
                   "artifact_id": self.ocr_id, "artifact_sha256": row["artifact_sha256"],
                   "physical_line_ranges": copy.deepcopy(row["physical_line_ranges"])}
        active = {"id": row["current_document_id"] + ".apparatus-v2", "sha256": row["artifact_sha256"],
                  "segment_id": segment["id"], "segment_path": str(path.relative_to(self.root)),
                  "physical_line_ranges": copy.deepcopy(row["physical_line_ranges"])}
        self.units[0]["active_render_selection"] = active
        row.update(current_document_id=active["id"], segment_id=active["segment_id"])
        return path, segment, active

    @staticmethod
    def write_segment(path, segment):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(f"{key} = {json.dumps(value)}" for key, value in segment.items()) + "\n")

    def test_older_pointer_without_artifact_ID_resolves_exact_registered_segment(self):
        path, segment, active = self.active_segment_fixture()
        self.write_segment(path, segment)
        before = path.read_bytes()
        self.refresh()
        self.run_screen()
        row = next(r for r in self.report()["results"] if r["unit_id"] == self.rows[0]["unit_id"])
        self.assertEqual(row["status"], "FLAGGED")
        self.assertEqual(row["current_document_id"], active["id"])
        self.assertEqual(row["controller_resolution"], {"method": "registered-active-segment",
            "segment_id": segment["id"], "segment_record_sha256": screen._sha(before)})
        self.assertEqual(path.read_bytes(), before)
        frozen = {}
        self.assertEqual(screen._active_controller(self.root, active, frozen)[0], self.ocr_id)
        self.assertEqual(frozen[path], screen._sha(before))

    def test_active_segment_mismatch_cannot_fall_back_to_raw_controller(self):
        path, original, active = self.active_segment_fixture()
        mutations = [("record_type", "artifact"), ("id", "segment.wrong"),
                     ("artifact_sha256", "0" * 64), ("physical_line_ranges", [[1, 2]])]
        for key, value in mutations:
            with self.subTest(field=key):
                segment = {**original, key: value}
                self.write_segment(path, segment)
                with self.assertRaisesRegex(ValueError, "active segment disagrees"):
                    screen._active_controller(self.root, active, {})
        self.write_segment(path, {**original, "artifact_id": "artifact.other.controller"})
        self.refresh()
        self.run_screen()
        row = next(r for r in self.report()["results"] if r["unit_id"] == self.rows[0]["unit_id"])
        self.assertEqual(row["status"], "UNKNOWN")
        self.assertIn("disagree", row["unknown_reasons"][0])

    def test_false_and_missed_control_signals_are_reported(self):
        self.recipe["controls"] = {"bullarium.fixture.negative": "mixed-row-positive", "bullarium.fixture.positive": "no-mixed-row-observed"}
        self.refresh()
        self.run_screen()
        controls = {row["unit_id"]: row for row in self.report()["calibration"]}
        self.assertTrue(controls["bullarium.fixture.negative"]["missed_positive"])
        self.assertTrue(controls["bullarium.fixture.positive"]["false_mixed_flag"])
        self.assertTrue(controls["bullarium.fixture.positive"]["negative_seed_any_flag"])

    def test_explicit_volume_filter_preserves_excluded_IDs_without_extraction(self):
        with patch.object(geometry, "source_pages", side_effect=AssertionError("no selected volume")):
            self.run_screen(volumes=[2])
        report = self.report()
        self.assertEqual(report["counts"]["screened_rows"], 0)
        self.assertEqual({r["current_document_id"] for r in report["excluded_by_volume"]},
                         {r["current_document_id"] for r in self.rows})

    def test_cache_adds_missing_union_once_and_reuses_old_pages(self):
        frozen = {}
        pins, locations, line_map, line_pin = screen._source(self.root, self.catalog["volumes"][0], self.recipe["inputs"], frozen)
        out = self.root / self.out
        with patch.object(geometry, "source_pages", wraps=geometry.source_pages) as extract:
            screen._native_pages(self.root, out, pins, locations, line_map, line_pin, {1}, frozen)
            screen._native_pages(self.root, out, pins, locations, line_map, line_pin, {1, 2}, frozen)
        self.assertEqual([call.args[3] for call in extract.call_args_list], [[1], [2]])

    def test_rehashed_cache_cannot_forge_page_fingerprint_or_SOURCE_membership(self):
        self.run_screen()
        cache = next((self.root / self.out / "native-cache").rglob("leaf-1.json.gz"))
        original = cache.read_bytes()
        receipt_path = cache.with_name("leaf-1.receipt.json")
        original_receipt = json.loads(receipt_path.read_bytes())
        for mutation, message in ((lambda page: page.update(full_page_tokens_sha256="0" * 64), "fingerprint"),
                                  (lambda page: page.update(dimensions=[999, 999]), "OBJECT leaf/dimensions"),
                                  (lambda page: page.update(source_byte_range_0=[0, 1]), "source byte/LF bounds"),
                                  (lambda page: page["WORDs"][0][screen.WORD_FIELDS.index("source_xml_byte_range_0")].__setitem__(1,
                                      page["WORDs"][0][screen.WORD_FIELDS.index("source_xml_byte_range_0")][1] + 1), "exact XML WORD end"),
                                  (lambda page: page["WORDs"][0].__setitem__(2, 999), "WORD/LINE/XML membership")):
            with self.subTest(message=message):
                compact = json.loads(gzip.decompress(original))
                mutation(compact)
                decoded = screen._bytes(compact)
                payload = screen._gzip(decoded)
                receipt = copy.deepcopy(original_receipt)
                receipt["product"].update(gzip_sha256=screen._sha(payload), page_sha256=screen._sha(decoded),
                                           full_page_tokens_sha256=compact["full_page_tokens_sha256"])
                cache.write_bytes(payload)
                receipt_path.write_bytes(screen._bytes(receipt))
                with self.assertRaisesRegex(ValueError, message):
                    self.run_screen()
        cache.write_bytes(original)
        receipt_path.write_bytes(screen._bytes(original_receipt))

    def test_unhashed_or_changed_map_source_and_tokens_are_refused(self):
        self.raw_path.write_bytes(self.raw_path.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "hash or byte size mismatch"):
            self.run_screen()
        self.raw_path.write_bytes(self.raw)
        self.xml_path.write_bytes(self.xml_path.read_bytes().replace(b">body0<", b">changed<", 1))
        self.refresh()
        with self.assertRaisesRegex(ValueError, "TXT/XML WORD token mismatch"):
            self.run_screen()
        self.assertFalse((self.root / self.out / "screen.json").exists())

    def test_wrong_leaf_and_LF_map_are_refused(self):
        self.line_map["pages"][0]["leaf"] = 99
        self.refresh()
        with self.assertRaisesRegex(ValueError, "scan leaf is absent"):
            self.run_screen()

    def test_tampered_compressed_page_fails_instead_of_reextracting(self):
        self.run_screen()
        cache = next((self.root / self.out / "native-cache").rglob("leaf-1.json.gz"))
        cache.write_bytes(cache.read_bytes() + b"tampered")
        with patch.object(geometry, "source_pages", side_effect=AssertionError("must not hide invalid cache")):
            with self.assertRaisesRegex(ValueError, "cache compressed hash mismatch"):
                self.run_screen()

    def test_rehashed_cache_cannot_change_source_WORD_geometry(self):
        self.run_screen()
        cache = next((self.root / self.out / "native-cache").rglob("leaf-1.json.gz"))
        compact = json.loads(gzip.decompress(cache.read_bytes()))
        compact["WORDs"][0][screen.WORD_FIELDS.index("coords")] = "1,2,3,4"
        decoded, payload = screen._bytes(compact), screen._gzip(screen._bytes(compact))
        cache.write_bytes(payload)
        receipt_path = cache.with_name("leaf-1.receipt.json")
        receipt = json.loads(receipt_path.read_bytes())
        receipt["product"].update(gzip_sha256=screen._sha(payload), page_sha256=screen._sha(decoded))
        receipt_path.write_bytes(screen._bytes(receipt))
        with self.assertRaisesRegex(ValueError, "XML WORD value/coords mismatch"):
            self.run_screen()

    def test_repeated_page_text_cannot_forge_raw_offsets_with_correct_page_metadata(self):
        self.run_screen()
        cache1 = next((self.root / self.out / "native-cache").rglob("leaf-1.json.gz"))
        cache2 = cache1.with_name("leaf-2.json.gz")
        page1, page2 = (json.loads(gzip.decompress(path.read_bytes())) for path in (cache1, cache2))
        unchanged = {key: copy.deepcopy(page2[key]) for key in screen.PAGE_FIELDS if key != "source_token_range_0"}
        fields = screen.WORD_FIELDS
        originals = copy.deepcopy(page2["WORDs"])
        # The complete second page deliberately repeats the first page's text
        # prefix. Its native XML/geometry/page metadata remain entirely intact.
        for earlier, target in zip(page1["WORDs"], page2["WORDs"]):
            self.assertEqual(earlier[fields.index("value")], target[fields.index("value")])
            for key in ("source_txt_token_byte_ranges_0", "source_txt_physical_lines"):
                target[fields.index(key)] = copy.deepcopy(earlier[fields.index(key)])
        token_count = page2["full_page_token_count"]
        page2["source_token_range_0"] = [page1["source_token_range_0"][0], page1["source_token_range_0"][0] + token_count]
        self.assertEqual(unchanged, {key: page2[key] for key in unchanged})
        for old, forged in zip(originals, page2["WORDs"]):
            for key in ("source_xml_byte_range_0", "coords", "source_bbox", "source_word_global_1", "source_line_global_1"):
                self.assertEqual(old[fields.index(key)], forged[fields.index(key)])
        decoded = screen._bytes(page2)
        payload = screen._gzip(decoded)
        receipt_path = cache2.with_name("leaf-2.receipt.json")
        receipt = json.loads(receipt_path.read_bytes())
        receipt["product"].update(gzip_sha256=screen._sha(payload), page_sha256=screen._sha(decoded),
                                   full_page_tokens_sha256=page2["full_page_tokens_sha256"])
        cache2.write_bytes(payload)
        receipt_path.write_bytes(screen._bytes(receipt))
        with patch.object(geometry, "source_pages", side_effect=AssertionError("must reject forged cache, not refresh it")):
            with self.assertRaisesRegex(ValueError, "full-page raw token interval mismatch"):
                self.run_screen()

    def test_adjacent_XML_pages_can_legitimately_share_one_raw_LF(self):
        pages = self.line_map["pages"]
        boundary_lf = pages[0]["physical_line_end"]
        boundary_byte = [i for i, char in enumerate(self.raw) if char == 10][boundary_lf - 1]
        # A space preserves the exact whole token sequence while placing the
        # last token of page1 and first tokens of page2 on the same raw LF.
        shared = self.raw[:boundary_byte] + b" " + self.raw[boundary_byte + 1:]
        self.raw_path.write_bytes(shared)
        pages[1]["physical_line_start"] -= 1
        pages[1]["physical_line_end"] -= 1
        self.line_map["physical_line_count"] -= 1
        self.rows[1]["physical_line_ranges"] = [[pages[1]["physical_line_start"], pages[1]["physical_line_end"]]]
        self.units[1]["physical_line_ranges"] = self.rows[1]["physical_line_ranges"]
        for row in self.rows + self.units:
            row["artifact_sha256"] = screen._sha(shared)
        self.refresh()
        with patch.object(geometry, "source_pages", wraps=geometry.source_pages) as extract:
            first = self.run_screen()
            self.assertEqual(extract.call_count, 1)
        cache1 = next((self.root / self.out / "native-cache").rglob("leaf-1.json.gz"))
        p1 = json.loads(gzip.decompress(cache1.read_bytes()))
        p2 = json.loads(gzip.decompress(cache1.with_name("leaf-2.json.gz").read_bytes()))
        self.assertEqual(p1["source_lf_range_1"][1], p2["source_lf_range_1"][0])
        self.assertGreater(p1["source_byte_range_0"][1], p2["source_byte_range_0"][0])
        self.assertEqual(p1["source_token_range_0"][1], p2["source_token_range_0"][0])
        self.assertEqual(p2["source_token_range_0"], [pages[0]["tokens"], self.line_map["token_count"]])
        with patch.object(geometry, "source_pages", side_effect=AssertionError("must replay checked shared-LF cache")):
            self.assertEqual(first, self.run_screen())

    def test_pinned_page_counts_require_order_unique_leaves_and_true_integers(self):
        original = copy.deepcopy(self.line_map)
        mutations = [(lambda m: m["pages"][0].update(artifact_page=2), "OBJECT sequence"),
                     (lambda m: m["pages"][1].update(leaf=1), "scan leaves"),
                     (lambda m: m["pages"][0].update(tokens=True), "page tokens"),
                     (lambda m: m["pages"][0].update(tokens=-1), "page tokens"),
                     (lambda m: m.update(token_count=m["token_count"] + 1), "complete token total")]
        for mutate, message in mutations:
            with self.subTest(message=message):
                line_map = copy.deepcopy(original)
                mutate(line_map)
                with self.assertRaisesRegex(ValueError, message):
                    screen._page_token_intervals(line_map)

    def test_page_prefix_whole_sum_and_selected_native_counts_are_checked(self):
        self.line_map["pages"][0]["tokens"] += 1
        self.line_map["token_count"] += 1
        self.refresh()
        with self.assertRaisesRegex(ValueError, "whole token sum"):
            self.run_screen()
        self.line_map["pages"][1]["tokens"] -= 1
        self.line_map["token_count"] -= 1
        self.refresh()
        with self.assertRaisesRegex(ValueError, "native full-page token count"):
            self.run_screen()

    def test_runtime_path_unknown_identity_and_duplicate_JSON_are_refused(self):
        self.recipe["inputs"][self.xml_id] = "../outside.xml"
        self.refresh()
        with self.assertRaisesRegex(ValueError, "traversal"):
            self.run_screen()
        self.recipe["inputs"] = {"artifact.unknown": "source.xml"}
        self.refresh()
        with self.assertRaisesRegex(ValueError, "unknown runtime"):
            self.run_screen()
        self.map_path.write_bytes(b'{"schema":1,"schema":2}')
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.run_screen()

    def test_output_outside_scratch_refused_and_worked_examples_truthful(self):
        self.out = "src/screen-output"
        with self.assertRaisesRegex(ValueError, "below repository .scratch"):
            self.run_screen()
        for example in screen.EXAMPLES:
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                code = screen.main(["--root", str(self.root), *shlex.split(example.command)[2:]])
            self.assertEqual(code, 2)
            self.assertEqual(tuple(stderr.getvalue().splitlines()), example.output)
        self.assertFalse((self.root / "src").exists())

    def test_input_and_nested_cache_symlink_escapes_fail_before_writes(self):
        with tempfile.TemporaryDirectory(dir=self.root.parent) as outside:
            target = Path(outside) / "source.xml"
            target.write_bytes(self.xml)
            self.xml_path.unlink()
            self.xml_path.symlink_to(target)
            with self.assertRaisesRegex(ValueError, "escapes the repository"):
                self.run_screen()
            self.assertFalse((self.root / self.out).exists())
            self.xml_path.unlink()
            self.xml_path.write_bytes(self.xml)
        out = self.root / self.out
        out.mkdir(parents=True)
        (out / "native-cache").symlink_to(self.root / "sources", target_is_directory=True)
        before = sorted(str(p) for p in (self.root / "sources").rglob("*"))
        with self.assertRaisesRegex(ValueError, "cannot pass through symlinks"):
            self.run_screen()
        self.assertEqual(before, sorted(str(p) for p in (self.root / "sources").rglob("*")))
        self.assertFalse((out / "screen.json").exists())


if __name__ == "__main__":
    unittest.main()
