"""A native spacing projection fails closed on uncertain or changed witnesses."""
import sys
import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import _papal_native_spacing as spacing


class NativeSpacingTests(unittest.TestCase):
    def retained(self, line, payload, page=1):
        return {"source_line": line, "source_line_sha256": spacing.digest(payload),
            "native_page": page, "reason": "Native marker position differs; preserve this original LF exactly."}

    def preserved(self, line, payload, count, page=1):
        return {**self.retained(line, payload, page),
            "preserve_original": True, "native_match_count": count}

    def test_whitespace_changes_preserve_every_glyph_and_source_note_order(self):
        source = "B o d y t e x t.\n\n(1) N o t e.\n".encode()
        native = "folio\n(1) Note.\nBody text.\f".encode()
        selections = [{"source_range": [1, 3], "native_page": 10}]
        output, mapping, differences = spacing.project(source, native, 10, selections, [10])
        self.assertEqual(output, b"Body text.\n\n(1) Note.\n")
        self.assertEqual(differences, [10])
        self.assertEqual([r["native_raw_line"] for r in mapping], [3, 2])
        self.assertEqual(spacing.nonspace(source.decode()), spacing.nonspace(output.decode()))

    def test_unreviewed_native_note_movement_is_held(self):
        with self.assertRaisesRegex(spacing.NativeSpacingError, "independent page review"):
            spacing.project(b"Body.\nNote.\n", b"Note.\nBody.\f", 1,
                [{"source_range": [1, 2], "native_page": 1}])

    def test_a_changed_glyph_or_new_word_is_not_reconstructed(self):
        for native in (b"A changed word.\f", b"A missing word.\f"):
            with self.assertRaisesRegex(spacing.NativeSpacingError, "found 0"):
                spacing.project(b"A source word.\n", native, 1,
                    [{"source_range": [1, 1], "native_page": 1}])

    def test_duplicate_native_lines_are_ambiguous_even_if_wording_agrees(self):
        with self.assertRaisesRegex(spacing.NativeSpacingError, "found 2"):
            spacing.project(b"S a m e.\n", b"Same.\nSame.\f", 1,
                [{"source_range": [1, 1], "native_page": 1}])

    def test_native_lines_cannot_be_reused(self):
        with self.assertRaisesRegex(spacing.NativeSpacingError, "multiple selected"):
            spacing.project(b"S a m e.\nS a m e.\n", b"Same.\f", 1,
                [{"source_range": [1, 2], "native_page": 1}])

    def test_ranges_cannot_overlap_or_reverse(self):
        with self.assertRaisesRegex(spacing.NativeSpacingError, "overlap"):
            spacing.project(b"One.\nTwo.\n", b"Two.\fOne.\f", 1,
                [{"source_range": [2, 2], "native_page": 1},
                 {"source_range": [1, 1], "native_page": 2}])

    def test_literal_hyphens_and_unicode_are_unchanged(self):
        output, _, _ = spacing.project("f i -\nn i s æ.\n".encode(), "fi-\nnis æ.\f".encode(), 1,
            [{"source_range": [1, 2], "native_page": 1}])
        self.assertEqual(output.decode(), "fi-\nnis æ.\n")

    def test_terminal_separators_are_not_physical_records_or_pages(self):
        for source, native, selection in (
            (b"Body.\n", b"Body.\f", {"source_range": [2, 2], "native_page": 1}),
            (b"Body.\n\n", b"Body.\f", {"source_range": [2, 2], "native_page": 2}),
            (b"", b"", {"source_range": [1, 1], "native_page": 1}),
        ):
            with self.subTest(selection=selection), self.assertRaises(spacing.NativeSpacingError):
                spacing.project(source, native, 1, [selection])
        output, _, _ = spacing.project(b"Body.\n\n", b"Body.\f", 1,
            [{"source_range": [1, 2], "native_page": 1}])
        self.assertEqual(output, b"Body.\n\n")

    def test_explicit_retained_lines_remain_byte_exact_without_moving_markers(self):
        source = b"1\nB o d y.\nG o o d.\n"
        retained = [self.retained(1, b"1"), self.retained(2, b"B o d y.")]
        output, mapping, _ = spacing.project(source, b"Body1.\nGood.\f", 1,
            [{"source_range": [1, 3], "native_page": 1}], retained_source_lines=retained)
        self.assertEqual(output, b"1\nB o d y.\nGood.\n")
        self.assertEqual([r['origin'] for r in mapping],
            ['retained-original', 'retained-original', 'native-whitespace'])
        self.assertEqual(spacing.nonspace(source.decode()), spacing.nonspace(output.decode()))

    def test_retained_lines_need_exact_hash_page_reason_and_unique_selected_identity(self):
        original = self.retained(1, b"m a r k")
        variants = []
        for key, value in [('source_line_sha256', '0'*64), ('native_page', 2),
                           ('source_line', True), ('reason', '')]:
            row = {**original, key: value}; variants.append([row])
        variants.extend([[original, original], [{**original, 'unknown': 1}],
            [self.retained(3, b"Outside.")]])
        for retained in variants:
            with self.subTest(retained=retained), self.assertRaises(spacing.NativeSpacingError):
                spacing.project(b"m a r k\nB o d y.\nOutside.\n", b"mark1\nBody.\f", 1,
                    [{"source_range": [1, 2], "native_page": 1}], retained_source_lines=retained)

    def test_retained_lines_cannot_bypass_ambiguous_unique_or_blank_records(self):
        for source, native in [(b"Same.\n", b"Same.\nSame.\f"),
                               (b"Same.\n", b"Same.\f"), (b"\n", b"\f")]:
            with self.subTest(native=native), self.assertRaises(spacing.NativeSpacingError):
                spacing.project(source, native, 1, [{'source_range':[1,1], 'native_page':1}],
                    retained_source_lines=[self.retained(1, source[:-1])])

    def test_one_retained_line_does_not_make_other_unmatched_lines_optional(self):
        with self.assertRaisesRegex(spacing.NativeSpacingError, 'found 0'):
            spacing.project(b"1\nB o d y.\n", b"Body1.\f", 1,
                [{'source_range':[1,2], 'native_page':1}],
                retained_source_lines=[self.retained(1, b'1')])

    def test_explicit_preservation_keeps_both_numeral_lines_without_claiming_native_identity(self):
        source = b" \t1\r\nB o d y.\n1\t \n(1) N o t e.\n"
        selections = [{"source_range": [1, 4], "native_page": 1}]
        for count, native, ordinals in (
            (1, b"1\nBody.\n(1) Note.\f", [2, 3]),
            (2, b"1\nBody.\n1\n(1) Note.\f", [2, 4]),
        ):
            with self.subTest(count=count):
                with self.assertRaises(spacing.NativeSpacingError):
                    spacing.project(source, native, 1, selections)
                records = [self.preserved(1, b" \t1\r", count),
                           self.preserved(3, b"1\t ", count)]
                output, mapping, differences = spacing.project(source, native, 1,
                    selections, retained_source_lines=records)
                self.assertEqual(output, b" \t1\r\nBody.\n1\t \n(1) Note.\n")
                self.assertEqual(differences, [])
                self.assertEqual([r["native_raw_line"] for r in mapping
                    if "native_raw_line" in r], ordinals)
                for row, record in zip((mapping[0], mapping[2]), records):
                    self.assertEqual(row["origin"], "retained-original")
                    self.assertEqual(row["native_match_count"], count)
                    self.assertEqual(row["retention_reason"], record["reason"])
                    self.assertEqual(row["recovered_line_sha256"], record["source_line_sha256"])
                    self.assertNotIn("native_raw_line", row)
                self.assertEqual(spacing.nonspace(source.decode()), spacing.nonspace(output.decode()))

    def test_explicit_protocol_preservation_keeps_parent_spacing_byte_exact(self):
        protocol = "  PIVS\u00a0 PP.  XI \t\r".encode()
        source = protocol + b"\nB o d y.\n"
        native = b"P I V S P P. X I\nBody.\f"
        selections = [{"source_range": [1, 2], "native_page": 1}]
        ordinary, _, _ = spacing.project(source, native, 1, selections)
        self.assertEqual(ordinary, b"P I V S P P. X I\nBody.\n")
        record = {**self.preserved(1, protocol, 1),
            "reason": "The parent's protocol spacing is retained literally after review."}
        output, mapping, _ = spacing.project(source, native, 1, selections,
            retained_source_lines=[record])
        self.assertEqual(output, protocol + b"\nBody.\n")
        self.assertEqual(mapping[0]["source_line_sha256"], spacing.digest(protocol))
        self.assertEqual(mapping[0]["recovered_line_sha256"], spacing.digest(protocol))
        self.assertEqual(mapping[1]["origin"], "native-whitespace")

    def test_preserved_count_pins_all_candidates_on_only_the_selected_page(self):
        selections = [{"source_range": [1, 1], "native_page": 10}]
        for count, native in [(0, b"1\n1\fOther.\f"), (1, b"1\n1\f1\f"),
                              (2, b"1\f1\n1\f")]:
            with self.subTest(count=count):
                record = self.preserved(1, b" 1 ", count, page=10)
                output, mapping, _ = spacing.project(b" 1 \n", native, 9, selections,
                    retained_source_lines=[record])
                self.assertEqual(output, b" 1 \n")
                self.assertEqual(mapping[0]["native_match_count"], count)
                for stale in {0, 1, 2, 3} - {count}:
                    with self.assertRaisesRegex(spacing.NativeSpacingError, "native_match_count mismatch"):
                        spacing.project(b" 1 \n", native, 9, selections,
                            retained_source_lines=[{**record, "native_match_count": stale}])

    def test_preserved_records_require_the_complete_exact_opt_in(self):
        original = self.preserved(1, b" 1 ", 1)
        variants = [{k: v for k, v in original.items() if k != missing}
            for missing in ("preserve_original", "native_match_count")]
        variants.append({**original, "unknown": True})
        for flag in (False, 1, 0, "true", None, [], {}):
            variants.append({**original, "preserve_original": flag})
        for count in (True, False, -1, 1.0, "1", None, [], {}):
            variants.append({**original, "native_match_count": count})
        for record in variants:
            with self.subTest(record=record), self.assertRaises(spacing.NativeSpacingError):
                spacing.project(b" 1 \n", b"1\f", 1,
                    [{"source_range": [1, 1], "native_page": 1}],
                    retained_source_lines=[record])

    def test_preserved_records_still_require_hash_page_reason_and_selected_nonblank_identity(self):
        original = self.preserved(1, b" 1 ", 1)
        variants = [[{**original, key: value}] for key, value in (
            ("source_line_sha256", "0" * 64), ("source_line_sha256", "bad"),
            ("native_page", 2), ("native_page", True), ("source_line", True),
            ("reason", " \t\r"), ("reason", None))]
        variants.extend([[original, original], [self.preserved(3, b"Outside.", 0)]])
        for records in variants:
            with self.subTest(records=records), self.assertRaises(spacing.NativeSpacingError):
                spacing.project(b" 1 \nB o d y.\nOutside.\n", b"1\nBody.\f", 1,
                    [{"source_range": [1, 2], "native_page": 1}],
                    retained_source_lines=records)
        with self.assertRaisesRegex(spacing.NativeSpacingError, "blank record"):
            spacing.project(b" \t\r\n", b"\f", 1,
                [{"source_range": [1, 1], "native_page": 1}],
                retained_source_lines=[self.preserved(1, b" \t\r", 0)])

    def test_preservation_does_not_relax_other_lines_or_native_witness_reuse(self):
        for source, native, message in (
            (b"1\nUnknown.\n", b"1\f", "found 0"),
            (b"1\nS a m e.\n", b"1\nSame.\nSame.\f", "found 2"),
            (b"1\nS a m e.\nS a m e.\n", b"1\nSame.\f", "multiple selected"),
        ):
            with self.subTest(source=source), self.assertRaisesRegex(spacing.NativeSpacingError, message):
                spacing.project(source, native, 1,
                    [{"source_range": [1, source.count(b"\n")], "native_page": 1}],
                    retained_source_lines=[self.preserved(1, b"1", 1)])
        with self.assertRaisesRegex(spacing.NativeSpacingError, "independent page review"):
            spacing.project(b"1\nB o d y.\nN o t e.\n", b"1\nNote.\nBody.\f", 1,
                [{"source_range": [1, 3], "native_page": 1}],
                retained_source_lines=[self.preserved(1, b"1", 1)])

    def test_legacy_and_default_projection_maps_keep_their_exact_contract(self):
        output, mapping, differences = spacing.project(b"B o d y.\n", b"Body.\f", 1,
            [{"source_range": [1, 1], "native_page": 1}])
        native_row = {"source_line": 1, "native_page": 1, "native_raw_line": 1,
            "source_line_sha256": spacing.digest(b"B o d y."),
            "recovered_line_sha256": spacing.digest(b"Body."), "nonwhitespace_characters": 5}
        self.assertEqual((output, mapping, differences), (b"Body.\n", [native_row], []))
        retained = self.retained(1, b"1")
        output, mapping, differences = spacing.project(b"1\nB o d y.\n", b"Body.\f", 1,
            [{"source_range": [1, 2], "native_page": 1}], retained_source_lines=[retained])
        self.assertEqual((output, mapping, differences), (b"1\nBody.\n", [
            {"source_line": 1, "native_page": 1, "source_line_sha256": spacing.digest(b"1"),
             "recovered_line_sha256": spacing.digest(b"1"), "nonwhitespace_characters": 1,
             "origin": "retained-original", "retention_reason": retained["reason"]},
            {**native_row, "source_line": 2, "origin": "native-whitespace"}], []))
        for native in (b"1\f", b"1\n1\f"):
            with self.subTest(native=native), self.assertRaisesRegex(spacing.NativeSpacingError, "zero native matches"):
                spacing.project(b"1\n", native, 1,
                    [{"source_range": [1, 1], "native_page": 1}], retained_source_lines=[retained])

    def test_native_raw_line_numbers_use_only_literal_lf_boundaries(self):
        for separator in ['\r', '\v', '\x85', '\u2028', '\u2029']:
            with self.subTest(separator=separator), self.assertRaisesRegex(spacing.NativeSpacingError, 'found 0'):
                spacing.project(b'A\nB\n', ('A'+separator+'B\n\f').encode(), 1,
                    [{'source_range':[1,2],'native_page':1}])

    def test_unexpected_review_pages_and_selection_fields_are_rejected(self):
        for selection, reviewed in [({'source_range':[1,1], 'native_page':1, 'extra':True}, []),
                                    ({'source_range':[1,1], 'native_page':1}, [1])]:
            with self.assertRaises(spacing.NativeSpacingError):
                spacing.project(b"Body.\n", b"Body.\f", 1, [selection], reviewed)

    def test_cli_checks_canonical_outputs_without_overwriting_inputs_or_other_files(self):
        tool = Path(__file__).resolve().parents[1] / 'papal-native-spacing'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); scratch=root/'.scratch';scratch.mkdir()
            parent=scratch/'parent.txt';native=scratch/'native.txt';spec=scratch/'recipe.json'
            parent.write_bytes(b'B o d y.\n');native.write_bytes(b'Body.\f')
            recipe={'schema':spacing.SCHEMA, 'parent':{'artifact_id':'a', 'path':'.scratch/parent.txt', 'sha256':spacing.digest(parent.read_bytes())},
                'native_raw':{'artifact_id':'b', 'path':'.scratch/native.txt', 'sha256':spacing.digest(native.read_bytes())},
                'native_first_page':1,'selections':[{'source_range':[1,1],'native_page':1}],
                'output_sha256':spacing.digest(b'Body.\n'),'stream_order_difference_pages':[]}
            spec.write_text(json.dumps(recipe))
            def run(out, *extra):
                return subprocess.run([sys.executable,str(tool),'--root',str(root),'--recipe',str(spec),
                    '--out',str(out),'--json',*extra],text=True,capture_output=True)
            target=scratch/'output.txt';self.assertEqual(run(target).returncode,0)
            self.assertEqual(target.read_bytes(),b'Body.\n')
            canonical=root/'retained.txt';canonical.write_bytes(b'Body.\n')
            self.assertEqual(run(canonical,'--check').returncode,0)
            for output in [parent,native,spec,canonical]:
                before=output.read_bytes();result=run(output)
                self.assertEqual(result.returncode,2,result.stdout+result.stderr)
                self.assertEqual(output.read_bytes(),before)
                self.assertEqual(json.loads(result.stderr)['code'],'input')
            target.write_bytes(b'other bytes');self.assertEqual(run(target).returncode,2)
            self.assertEqual(target.read_bytes(),b'other bytes')
            spec.write_text('{"schema":"x","schema":"y"}')
            self.assertIn('duplicate JSON key',run(target).stderr)

    def test_preserved_recipe_replay_and_cli_report_parent_literal_lines_honestly(self):
        tool = Path(__file__).resolve().parents[1] / 'papal-native-spacing'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); scratch = root / '.scratch'; scratch.mkdir()
            source = b" 1 \nPIVS  PP. XI\nB o d y.\n1\t\n"
            native = b"1\nP I V S P P. X I\nBody.\f"
            expected = b" 1 \nPIVS  PP. XI\nBody.\n1\t\n"
            (scratch / 'parent.txt').write_bytes(source)
            (scratch / 'native.txt').write_bytes(native)
            recipe = {'schema': spacing.SCHEMA,
                'parent': {'artifact_id': 'a', 'path': '.scratch/parent.txt', 'sha256': spacing.digest(source)},
                'native_raw': {'artifact_id': 'b', 'path': '.scratch/native.txt', 'sha256': spacing.digest(native)},
                'native_first_page': 1, 'selections': [{'source_range': [1, 4], 'native_page': 1}],
                'retained_source_lines': [self.preserved(1, b" 1 ", 1),
                    self.preserved(2, b"PIVS  PP. XI", 1), self.preserved(4, b"1\t", 1)],
                'output_sha256': spacing.digest(expected), 'stream_order_difference_pages': []}
            self.assertEqual(spacing.replay(recipe, root)[0], expected)
            spec = scratch / 'recipe.json'; spec.write_text(json.dumps(recipe))
            target = scratch / 'output.txt'
            result = subprocess.run([sys.executable, str(tool), '--root', str(root),
                '--recipe', str(spec), '--out', str(target), '--json'], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(target.read_bytes(), expected)
            self.assertEqual(json.loads(result.stdout), {'v': 1, 'status': 'pass',
                'sha256': spacing.digest(expected), 'matched_source_lines': 1,
                'retained_source_lines': [1, 2, 4], 'stream_order_difference_pages': []})
            for key in ('parent', 'native_raw', 'output_sha256'):
                stale = copy.deepcopy(recipe)
                if key == 'output_sha256':
                    stale[key] = '0' * 64
                else:
                    stale[key]['sha256'] = '0' * 64
                with self.subTest(key=key), self.assertRaisesRegex(spacing.NativeSpacingError, 'SHA-256 mismatch'):
                    spacing.replay(stale, root)

    def test_recipe_rejects_absolute_or_unknown_owner_and_top_level_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'parent.txt';p.write_bytes(b'Body.\n')
            native=root/'native.txt';native.write_bytes(b'Body.\f')
            original={'schema':spacing.SCHEMA,
                'parent':{'artifact_id':'a','path':'parent.txt','sha256':spacing.digest(p.read_bytes())},
                'native_raw':{'artifact_id':'b','path':'native.txt','sha256':spacing.digest(native.read_bytes())},
                'native_first_page':1,'selections':[{'source_range':[1,1],'native_page':1}],
                'output_sha256':spacing.digest(b'Body.\n'),'stream_order_difference_pages':[]}
            self.assertEqual(spacing.replay(original,root)[0],b'Body.\n')
            for change in ['absolute','owner-extra','top-extra','missing']:
                recipe=copy.deepcopy(original)
                if change=='absolute':recipe['parent']['path']=str(p)
                elif change=='owner-extra':recipe['parent']['extra']=True
                elif change=='top-extra':recipe['unknown']=True
                else:del recipe['output_sha256']
                with self.subTest(change=change), self.assertRaises(spacing.NativeSpacingError):
                    spacing.replay(recipe,root)


if __name__ == "__main__":
    unittest.main()
