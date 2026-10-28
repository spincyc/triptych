"""Geometry replay preserves complete WORDs, page bytes and independently checked maps."""
from __future__ import annotations

import contextlib
import copy
import gzip
import hashlib
from html import escape
import io
import json
from pathlib import Path
import shlex
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _bullarium_geometry as geometry


class GeometryTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/bullarium_reconstruction/geometry_engine/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temp.name)
        self.out = self.root / ".scratch/output"
        self.xml_path, self.raw_path, self.recipe_path = (self.root / name for name in ("source.xml", "source.txt", "recipe.json"))
        self.words = []
        xml = bytearray(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE DjVuXML>\n<DjVuXML><BODY>')
        raw = bytearray()
        global_line = 0
        self.private_object_path = "file://HOST-PRIVATE-OBJECT-PATH/book.djvu"
        definitions = [
            [[("FRONT", "100,120,200,100"), ("æ.", "210,120,230,100")]],
            [[("HEADER", "100,30,200,10")],
             [("L2", "100,220,150,200"), ("R1", "700,120,750,100"), ("margin", "10,190,70,170")],
             [("L1", "100,120,150,100"), ("  qui bene  ", "100,320,240,300")],
             [("R2", "700,220,750,200"), ("A & B", "100,820,240,800")],
             [("|", "500,420,501,400"), ("", "10,420,11,400")]],
            [[("FINIS.", "100,120,200,100")], [("RAW", "100,220,150,200"), ("TAIL", "160,220,200,200")]],
        ]
        self.page_span = None
        for page, lines in enumerate(definitions, 1):
            xml.extend(f'<OBJECT data="{self.private_object_path}" usemap="book_{page:04d}.djvu" width="1000" height="1200"><HIDDENTEXT>'.encode())
            page_begin, first_line = len(raw), raw.count(b"\n") + 1
            page_word = 0
            for local_line, entries in enumerate(lines, 1):
                global_line += 1
                xml.extend(b"<LINE>")
                for value, coords in entries:
                    page_word += 1
                    begin = len(xml)
                    tag = f'<WORD coords="{coords}" x-confidence="1">{escape(value)}</WORD>' if value else f'<WORD coords="{coords}" x-confidence="1"/>'
                    xml.extend(tag.encode())
                    self.words.append({"source_word_global_1": len(self.words) + 1,
                        "source_word_page_1": page_word, "source_line_global_1": global_line,
                        "source_line_page_1": local_line, "source_xml_byte_range_0": [begin, len(xml)],
                        "value": value, "coords": coords, "role": "body-left", "flags": [], "after": "\n"})
                xml.extend(b"</LINE>")
                # Original TXT has its own layout whitespace; XML WORD padding is not copied here.
                raw.extend(" ".join(part for value, coords in entries for part in value.split()).encode())
                if page != 3 or local_line != len(lines):
                    raw.extend(b"\r\n")
            if page == 2:
                self.page_span = [page_begin, len(raw)]
                self.page_lfs = [first_line, raw.count(b"\n")]
            xml.extend(b"</HIDDENTEXT></OBJECT>")
        xml.extend(b"</BODY></DjVuXML>")
        self.raw, self.xml = bytes(raw), bytes(xml)
        self.raw_path.write_bytes(self.raw)
        self.xml_path.write_bytes(self.xml)
        ordered = [3, 7, 4, 8, 5, 9, 6, 10, 12, 11]
        roles = ["header", "body-left", "body-left", "body-left", "body-right", "body-right",
                 "margin-left", "notes-left", "uncertain", "gutter-ocr"]
        chosen = []
        for number, role in zip(ordered, roles):
            word = copy.deepcopy(self.words[number - 1])
            word["role"] = role
            if role in {"uncertain", "gutter-ocr"}:
                word["flags"] = ["source-recognition-retained"]
            chosen.append(word)
        self.recipe = {"schema": geometry.SCHEMA, "serialization": "word-per-line",
                       "source_txt": self.pin(self.raw_path, self.raw, "artifact.fixture.ocr"),
                       "source_xml": self.pin(self.xml_path, self.xml, "artifact.fixture.xml"),
                       "changed_pages": [{"leaf": 2, "object_ordinal_1": 2, "source_byte_range_0": self.page_span,
                                          "source_lf_range_1": self.page_lfs, "before": "", "words": chosen}]}

    def tearDown(self):
        self.temp.cleanup()

    def pin(self, path, data, identity):
        return {"path": path.relative_to(self.root).as_posix(), "sha256": hashlib.sha256(data).hexdigest(),
                "byte_size": len(data), "artifact_id": identity}

    def test_source_page_preparation_keeps_native_words_and_no_cache_locations(self):
        result=geometry.source_pages(self.root,self.recipe["source_txt"],self.recipe["source_xml"],[2])
        page=result["pages"][0]
        self.assertEqual(page["leaf"],2)
        self.assertEqual([w["source_word_global_1"] for w in page["words"]],list(range(3,13)))
        self.assertNotIn("path",result["source_xml"])
        self.assertNotIn(self.private_object_path,json.dumps(result))
        self.assertEqual(next(w["value"] for w in page["words"] if w["source_word_global_1"]==8),"  qui bene  ")

    def test_source_page_preparation_checks_whole_input_and_selected_leaf(self):
        with self.assertRaisesRegex(ValueError,"absent from XML"):
            geometry.source_pages(self.root,self.recipe["source_txt"],self.recipe["source_xml"],[99])
        self.raw_path.write_bytes(self.raw+b"tampered")
        with self.assertRaisesRegex(ValueError,"complete source hash"):
            geometry.source_pages(self.root,self.recipe["source_txt"],self.recipe["source_xml"],[2])

    def write_recipe(self):
        self.recipe_path.write_bytes(geometry._json_bytes(self.recipe))

    def build(self, **kwargs):
        self.write_recipe()
        return geometry.build(self.root, self.recipe_path, self.out, **kwargs)

    def word_map(self):
        return [json.loads(line) for line in gzip.decompress((self.out / "changed-word-map.jsonl.gz").read_bytes()).splitlines()]

    def test_mixed_columns_margin_and_uncertainty_replay_without_byte_changes_elsewhere(self):
        before = self.raw_path.read_bytes(), self.xml_path.read_bytes()
        info = self.build()
        hybrid = (self.out / "hybrid.txt").read_bytes()
        body = b"".join(w["value"].encode() + b"\n" for w in self.recipe["changed_pages"][0]["words"])
        a, z = self.page_span
        self.assertEqual(hybrid, self.raw[:a] + body + self.raw[z:])
        self.assertEqual((self.raw_path.read_bytes(), self.xml_path.read_bytes()), before)
        self.assertEqual(info["source_WORDs"], 15)
        self.assertEqual(info["changed_WORDs"], 10)
        self.assertEqual(info["derived_from"], "artifact.fixture.ocr")
        self.assertEqual(info["roles"]["uncertain"], 1)
        for path in self.out.iterdir():
            data = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
            self.assertNotIn(self.private_object_path.encode(), data)

    def test_multi_token_and_entity_WORDs_remain_indivisible_with_exact_xml_byte_offsets(self):
        self.build()
        hybrid = (self.out / "hybrid.txt").read_bytes()
        rows = {row["source_word_global_1"]: row for row in self.word_map()}
        for number in (8, 10, 12):
            word = rows[number]
            a, z = word["output_utf8_byte_range_0"]
            self.assertEqual(hybrid[a:z], self.words[number - 1]["value"].encode())
            a, z = word["source_xml_byte_range_0"]
            self.assertTrue(self.xml[a:z].startswith(b"<WORD "))
        self.assertEqual(rows[8]["value"], "  qui bene  ")
        self.assertEqual(rows[10]["value"], "A & B")
        self.assertEqual(rows[12]["value"], "")
        rows = self.word_map()
        self.assertTrue(all(a["output_lf_range_1"][1] < b["output_lf_range_1"][0] for a, b in zip(rows, rows[1:])))

    def test_maps_are_compact_and_builds_and_checks_are_deterministic(self):
        first = self.build()
        before = {p.name: p.read_bytes() for p in self.out.iterdir()}
        other = self.root / ".scratch/independent"
        self.assertEqual(geometry.build(self.root, self.recipe_path, other), first)
        self.assertEqual({p.name: p.read_bytes() for p in other.iterdir()}, before)
        self.assertEqual(geometry.check(self.root, self.recipe_path, self.out), first)
        self.assertEqual(len(self.word_map()), 10)
        self.assertNotIn(b"FRONT", gzip.decompress(before["changed-word-map.jsonl.gz"]))
        pages = json.loads(before["page-map.json"])["pages"]
        self.assertEqual(len(pages), 3)
        self.assertEqual(pages[0]["serialization"], "unchanged-raw-ocr")
        self.assertIsNotNone(pages[2]["output_lf_range_1"])

    def test_recipe_whitespace_can_replay_a_pinned_alternate_layout(self):
        self.recipe["serialization"] = "recipe-whitespace"
        for word in self.recipe["changed_pages"][0]["words"]:
            word["after"] = " \t"
        self.recipe["changed_pages"][0]["words"][-1]["after"] = "\n\n"
        payload = b"".join(w["value"].encode() + w["after"].encode() for w in self.recipe["changed_pages"][0]["words"])
        a, z = self.page_span
        expected = self.raw[:a] + payload + self.raw[z:]
        self.recipe["expected_output"] = {"sha256": hashlib.sha256(expected).hexdigest(), "byte_size": len(expected)}
        self.recipe["changed_pages"][0]["replacement_sha256"] = hashlib.sha256(payload).hexdigest()
        self.build()
        self.assertEqual((self.out / "hybrid.txt").read_bytes(), expected)

    def test_omitted_duplicated_and_wrong_page_WORDs_are_rejected(self):
        original = copy.deepcopy(self.recipe)
        for kind in ("omitted", "duplicated", "other-page"):
            self.recipe = copy.deepcopy(original)
            words = self.recipe["changed_pages"][0]["words"]
            if kind == "omitted":
                words.pop()
            elif kind == "duplicated":
                words[-1] = copy.deepcopy(words[0])
            else:
                words[-1] = copy.deepcopy(self.words[0])
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.build()
        self.assertFalse(self.out.exists())

    def test_mutated_values_coordinates_offsets_and_optional_map_pins_are_rejected(self):
        original = copy.deepcopy(self.recipe)
        changes = {"value": "repaired", "coords": "1,2,3,4", "source_xml_byte_range_0": [1, 20],
                   "source_attrs": {"coords": "1,2,3,4"}, "source_bbox": [1, 2, 3, 4],
                   "source_txt_token_byte_ranges_0": [[0, 1]], "output_utf8_byte_range_0": [0, 1]}
        for field, value in changes.items():
            self.recipe = copy.deepcopy(original)
            self.recipe["changed_pages"][0]["words"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.build()
        self.assertFalse(self.out.exists())

    def test_wrong_leaf_object_and_raw_byte_or_LF_ranges_are_rejected(self):
        original = copy.deepcopy(self.recipe)
        for field, value in {"leaf": 999, "object_ordinal_1": 1, "source_byte_range_0": [0, 10], "source_lf_range_1": [1, 2]}.items():
            self.recipe = copy.deepcopy(original)
            self.recipe["changed_pages"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.build()

    def test_unhashed_changed_sources_and_repinned_token_mismatch_are_rejected(self):
        original = copy.deepcopy(self.recipe)
        self.recipe["source_xml"].pop("sha256")
        with self.assertRaises(ValueError):
            self.build()
        self.recipe = copy.deepcopy(original)
        self.raw_path.write_bytes(self.raw + b"MUTATED")
        with self.assertRaisesRegex(ValueError, "source hash or byte size"):
            self.build()
        changed = self.raw.replace(b"FRONT", b"ALTER")
        self.raw_path.write_bytes(changed)
        self.recipe["source_txt"] = self.pin(self.raw_path, changed, "artifact.fixture.ocr")
        with self.assertRaisesRegex(ValueError, "TXT/XML WORD token mismatch"):
            self.build()

    def test_nonwhitespace_insertions_and_nonindependent_word_lines_are_rejected(self):
        self.recipe["changed_pages"][0]["words"][0]["after"] = " editorial label "
        with self.assertRaisesRegex(ValueError, "only whitespace"):
            self.build()
        self.recipe["changed_pages"][0]["words"][0]["after"] = " "
        with self.assertRaisesRegex(ValueError, "independent LF"):
            self.build()

    def test_checker_rejects_tampered_byte_page_or_compressed_word_maps(self):
        self.build()
        for name in ("byte-map.json", "page-map.json", "changed-word-map.jsonl.gz", "hybrid.txt"):
            path = self.out / name
            before = path.read_bytes()
            path.write_bytes(before + b"tampered")
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "geometry product mismatch"):
                geometry.check(self.root, self.recipe_path, self.out)
            path.write_bytes(before)

    def test_machine_local_OBJECT_attributes_and_canonical_output_paths_are_refused(self):
        self.recipe["changed_pages"][0]["object_attrs"] = {"data": self.private_object_path}
        with self.assertRaisesRegex(ValueError, "unsupported fields"):
            self.build()
        self.recipe["changed_pages"][0].pop("object_attrs")
        self.write_recipe()
        with self.assertRaisesRegex(ValueError, "under .scratch or build"):
            geometry.build(self.root, self.recipe_path, self.root / "src/sources/new")
        self.assertFalse((self.root / "src").exists())

    def test_existing_different_outputs_are_not_overwritten(self):
        self.build()
        path = self.out / "hybrid.txt"
        path.write_bytes(b"Earlier retained output.")
        with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
            self.build()
        self.assertEqual(path.read_bytes(), b"Earlier retained output.")

    def test_remote_XML_has_explicit_runtime_cache_mapping_and_no_serialized_cache_path(self):
        self.recipe["source_xml"].pop("path")
        self.recipe["source_xml"]["source_url"] = "https://example.org/whole-djvu.xml"
        with self.assertRaisesRegex(ValueError, "explicit input_map"):
            self.build()
        mapping = {"artifact.fixture.xml": "source.xml"}
        first = self.build(input_map=mapping)
        self.assertNotIn("path", first["source_xml"])
        self.assertEqual(first["source_xml"]["source_url"], "https://example.org/whole-djvu.xml")
        map_path = self.root / "runtime-map.json"
        map_path.write_bytes(geometry._json_bytes({"schema": "triptych-bullarium-geometry-input-map/v1", "inputs": mapping}))
        self.assertEqual(geometry.check(self.root, self.recipe_path, self.out, input_map=map_path), first)

    def test_safe_cli_examples_and_json_argument_errors(self):
        for example in geometry.EXAMPLES:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = geometry.main(shlex.split(example.command)[2:])
            self.assertEqual(code, 2)
            self.assertFalse(out.getvalue())
            self.assertEqual(tuple(err.getvalue().splitlines()), example.output)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(geometry.main(["--json"]), 2)
        self.assertEqual(json.loads(err.getvalue())["code"], "input")


if __name__ == "__main__":
    unittest.main()
