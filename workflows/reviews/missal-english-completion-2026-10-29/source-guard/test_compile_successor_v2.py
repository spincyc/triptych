"""Meaningful scratch-only controls for a pending guard successor."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

PATH = Path(__file__).with_name('compile_successor_v2.py')
spec = importlib.util.spec_from_file_location('bounded_guard_successor', PATH)
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
SCRATCH = G.REPO / '.scratch/reader-audit-20261029/compiler-controls'
SCRATCH.mkdir(parents=True, exist_ok=True)


class BoundedScopeTests(unittest.TestCase):
    def test_scope_retains_every_old_pin_adds_only_source_deltas_and_explicit_inputs(self):
        old = [{'path': G.HELPER}, {'path': 'src/sources/existing.toml'}]
        changed = b'src/sources/added.toml\0src/sources/inventories/source-family-migration-v1.toml\0'
        untracked = b'src/sources/new.txt\0'
        with mock.patch.object(G.subprocess, 'check_output', side_effect=[changed, untracked]):
            actual = G.scope_paths(Path('.'), old, [G.REVIEW_PREFIX + 'ordinary/new-review.json'])
        self.assertEqual(actual, {G.HELPER, 'src/sources/existing.toml', 'src/sources/added.toml',
                                  'src/sources/new.txt', G.REVIEW_PREFIX + 'ordinary/new-review.json'})

    def test_only_explicit_source_or_same_task_json_authority_extras_are_admitted(self):
        G.extra_input('src/sources/works/synthetic/work.toml')
        G.extra_input(G.REVIEW_PREFIX + 'ordinary/root-adoption.json')
        for path in ('.git/config', 'tools/mass-propers', 'workflows/reviews/unrelated/authority.json',
                     G.REVIEW_PREFIX + 'ordinary/approval.py', G.REVIEW_PREFIX + 'source-guard/acceptance.json'):
            with self.subTest(path=path), self.assertRaises(AssertionError):
                G.extra_input(path)

    def test_shared_registry_and_self_cycle_extras_refuse(self):
        for path in [*G.EXCLUDED_REGISTRIES, G.FIXTURE, G.MANIFEST]:
            with self.subTest(path=path), mock.patch.object(G.subprocess, 'check_output', return_value=b''):
                with self.assertRaises(AssertionError):
                    G.scope_paths(Path('.'), [], [path])

    def test_missing_or_symlinked_inputs_and_changed_strict_helper_refuse(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            root = Path(temporary)
            helper = root / G.HELPER
            helper.parent.mkdir(parents=True)
            helper.write_bytes(b'changed strict helper')
            with self.assertRaisesRegex(AssertionError, 'strict helper'):
                G.read_epoch(root, {G.HELPER})
            (root / 'link').symlink_to(helper)
            for path in ('link', 'missing'):
                with self.subTest(path=path), self.assertRaisesRegex(AssertionError, 'missing or symlinked'):
                    G.read_epoch(root, {path})

    def test_exact_declared_delta_is_required_before_consuming_a_new_source_epoch(self):
        row = {'path': 'src/sources/new.toml', 'before_sha256': None, 'post_sha256': 'a' * 64}
        data = {'schema': 'triptych-bounded-source-input-delta/v1', 'parent_git_revision': G.PARENT,
                'parent_manifest_sha256': 'b' * 64, 'extra_inputs': [], 'files': [row]}
        raw = G.serialized(data)
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            path = Path(temporary) / 'delta.json'
            path.write_bytes(raw)
            with mock.patch.object(G, 'input_delta', return_value=({'one'}, {'one': 'pin'}, [row])):
                result = G.declared_inputs(Path('.'), [], object(), path, G.digest(raw),
                                           {'manifest_sha256': 'b' * 64})
                self.assertEqual(result[:3], ({'one'}, {'one': 'pin'}, [row]))
            with mock.patch.object(G, 'input_delta', return_value=({'one'}, {'one': 'pin'}, [])):
                with self.assertRaisesRegex(AssertionError, 'complete observed file delta'):
                    G.declared_inputs(Path('.'), [], object(), path, G.digest(raw),
                                      {'manifest_sha256': 'b' * 64})
            path.write_bytes(raw + b' ')
            with self.assertRaisesRegex(AssertionError, 'exact explicitly supplied input delta'):
                G.declared_inputs(Path('.'), [], object(), path, G.digest(raw),
                                  {'manifest_sha256': 'b' * 64})

    def test_a_source_below_an_escaped_symlinked_ancestor_refuses(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            base = Path(temporary)
            root = base / 'root'
            outside = base / 'outside'
            (root / 'src').mkdir(parents=True)
            outside.mkdir()
            (outside / 'source.toml').write_text('source = "outside"\n')
            (root / 'src/sources').symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(AssertionError, 'escaped or symlinked ancestor'):
                G.read_epoch(root, {'src/sources/source.toml'})


class EnglishComplementTests(unittest.TestCase):
    positive = {'kept': {'translations': [{'lang': 'en', 'text': 'Kept literal text.'}]}}
    absent = {'gap': {'reason': {'kind': 'witness-gap'}}}
    new_body = {'translations': [{'lang': 'en', 'text': 'New study English.'}]}

    def test_exact_admission_preserves_all_prior_positives_and_consumes_only_its_gap(self):
        G.check_english_complements(self.positive, self.absent,
                                   {**self.positive, 'gap': self.new_body}, {})
        G.check_english_complements(self.positive, self.absent, self.positive, self.absent)

    def test_changed_positive_or_unconsumed_absence_refuses(self):
        with self.assertRaisesRegex(AssertionError, 'prior positive'):
            G.check_english_complements(self.positive, self.absent,
                                       {'kept': self.new_body}, self.absent)
        with self.assertRaisesRegex(AssertionError, 'prior English refusal'):
            G.check_english_complements(self.positive, self.absent, self.positive,
                                       {'gap': {'reason': {'kind': 'no-exemplar'}}})

    def test_a_different_new_owner_cannot_hide_a_removed_old_gap(self):
        with self.assertRaises(AssertionError):
            G.check_english_complements(self.positive, self.absent,
                                       {**self.positive, 'different': self.new_body}, {})

    def test_text_free_or_wrong_language_admission_refuses(self):
        for body in ({}, {'translations': [{'lang': 'la', 'text': 'Latine.'}]},
                     {'translations': [{'lang': 'en', 'text': '   '}]}):
            with self.subTest(body=body), self.assertRaisesRegex(AssertionError, 'literal nonempty English'):
                G.check_english_complements(self.positive, self.absent,
                                           {**self.positive, 'gap': body}, {})

    def test_overlapping_partitions_refuse(self):
        with self.assertRaisesRegex(AssertionError, 'partitions overlap'):
            G.check_english_complements(self.positive, self.absent,
                                       {**self.positive, 'gap': self.new_body}, self.absent)


class ExactPalmCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (G.REPO / G.PALM_CORRECTION).read_bytes()
        cls.correction = json.loads(raw)
        cls.identity = G.canonical(G.PALM_TARGET)
        cls.pins = {G.PALM_CORRECTION: G.digest(raw),
                    cls.correction['source_review']: G.digest((G.REPO / cls.correction['source_review']).read_bytes())}

    def test_complete_exact_palm_dictionary_change_is_recognized_and_all_others_preserved(self):
        before = {self.identity: self.correction['old_entry'], **EnglishComplementTests.positive}
        current = {self.identity: self.correction['new_entry'], **EnglishComplementTests.positive}
        protected, evidence = G.positive_complement(G.REPO, self.pins, 'roman-1962', before, current)
        self.assertEqual(protected, current)
        self.assertEqual(len(evidence), 1)
        G.check_english_complements(protected, {}, current, {})

    def test_foreign_owner_calendar_or_other_modified_positive_refuses(self):
        before = {self.identity: self.correction['old_entry'], **EnglishComplementTests.positive}
        current = {self.identity: self.correction['new_entry'], **EnglishComplementTests.positive}
        with self.assertRaisesRegex(AssertionError, 'unrecorded prior'):
            G.positive_complement(G.REPO, self.pins, 'postconciliar', before, current)
        changed = {**current, 'kept': EnglishComplementTests.new_body}
        with self.assertRaisesRegex(AssertionError, 'unrecorded prior'):
            G.positive_complement(G.REPO, self.pins, 'roman-1962', before, changed)

    def test_wrong_whole_dictionary_or_missing_exact_receipt_and_review_pins_refuse(self):
        before = {self.identity: self.correction['old_entry']}
        current = {self.identity: self.correction['new_entry']}
        for pins in ({}, {G.PALM_CORRECTION: '0' * 64}, {G.PALM_CORRECTION: G.PALM_CORRECTION_SHA}):
            with self.subTest(pins=pins), self.assertRaises(AssertionError):
                G.positive_complement(G.REPO, pins, 'roman-1962', before, current)
        for changed in ({self.identity: {**self.correction['new_entry'], 'printed_page': 'invented'}},
                        {self.identity: EnglishComplementTests.new_body}):
            with self.subTest(changed=changed), self.assertRaisesRegex(AssertionError, 'entire recorded'):
                G.positive_complement(G.REPO, self.pins, 'roman-1962', before, changed)

    def test_palm_receipt_bytes_are_checked_independently_of_supplied_pin_values(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            root = Path(temporary)
            receipt = root / G.PALM_CORRECTION
            receipt.parent.mkdir(parents=True)
            receipt.write_text('{}\n')
            with self.assertRaisesRegex(AssertionError, 'entire exact Palm correction receipt bytes'):
                G.positive_complement(root, self.pins, 'roman-1962',
                                      {self.identity: self.correction['old_entry']},
                                      {self.identity: self.correction['new_entry']})


if __name__ == '__main__':
    unittest.main()
