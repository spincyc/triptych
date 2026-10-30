"""Meaningful scratch-only controls for a pending guard successor."""
import importlib.util
import ast
import copy
import dataclasses
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

PATH = Path(__file__).with_name('compile_successor_v3.py')
spec = importlib.util.spec_from_file_location('bounded_guard_successor', PATH)
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
SCRATCH = G.REPO / '.scratch/checkpoint-source-batch-20261030/compiler-v3-controls'
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


class DirectPublicDomainProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.path.insert(0, str(G.REPO / 'scripts'))
        from _proper_latin import (LatinKey, SURFACES, body_owners, decision_for,
                                   publication_records, read_sidecar)
        from _calendars import load_document
        cls.Key, cls.surfaces, cls.decide = LatinKey, SURFACES, staticmethod(decision_for)
        cls.support = G.libraries()[1]
        cls.declaration = json.loads((G.REPO / G.DIRECT_DECLARATION).read_bytes())
        records, errors = read_sidecar(G.REPO / 'src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml')
        if errors:
            raise AssertionError(errors)
        cls.parsed = {G.canonical(key.as_dict()): row for key, row in records.items()}
        cls.validated, errors = publication_records(G.REPO / 'src/sources/calendars', 'roman-1962')
        if errors:
            raise AssertionError(errors)
        cls.texts, cls.bodies = {}, {}
        for key, text, state in body_owners(load_document(G.REPO / 'src/sources/calendars', 'roman-1962')):
            identity = G.canonical(key.as_dict())
            cls.bodies[identity] = {'state': state, 'body_sha256': G.digest(text) if text is not None else None}
            if isinstance(text, str):
                cls.texts[identity] = text
        cls.pins = {G.DIRECT_DECLARATION: G.DIRECT_DECLARATION_SHA}
        for artifact in cls.declaration['primary_artifacts']:
            cls.pins[artifact['path']] = artifact['sha256']
            cls.pins[artifact['payload_path']] = artifact['payload_sha256']
        cls.expected = {G.canonical(row['key']): row for row in cls.declaration['records']}

    def run_oracles(self, **changes):
        values = dict(source=G.REPO, pins=self.pins, parsed=self.parsed,
                      bodies=self.bodies, texts=self.texts, validated=self.validated,
                      decide=self.decide, key_class=self.Key, surfaces=self.surfaces,
                      declaration=self.declaration)
        values.update(changes)
        return self.support['direct_pd_oracles'](**values)

    def test_all25_exact_records_and_actual_production_decisions(self):
        self.assertEqual(self.run_oracles(), self.expected)
        for identity, expected in self.expected.items():
            with self.subTest(target=identity):
                decision = self.decide(self.Key(**expected['key']), self.texts[identity], self.validated)
                self.assertTrue(decision.permits(self.surfaces))
                self.assertEqual(decision.projection(self.surfaces), expected['production_decision'])

    def test_missing_extra_and_retargeted_proof_are_refused(self):
        identity = next(iter(self.expected))
        removed = dict(self.parsed)
        removed.pop(identity)
        with self.assertRaisesRegex(AssertionError, 'complete exact direct-PD partition'):
            self.run_oracles(parsed=removed)
        extra = dict(self.parsed)
        extra['unreviewed-target'] = dict(self.parsed[identity])
        with self.assertRaisesRegex(AssertionError, 'complete exact direct-PD partition'):
            self.run_oracles(parsed=extra)
        retargeted = dict(self.parsed)
        retargeted[identity] = dict(self.parsed[identity], mass='different-owner')
        with self.assertRaisesRegex(AssertionError, 'entire exact direct-PD proof dictionary'):
            self.run_oracles(parsed=retargeted)

    def test_each25_body_tamper_is_denied_by_actual_production_and_oracle(self):
        for identity, expected in self.expected.items():
            with self.subTest(target=identity):
                texts = dict(self.texts)
                texts[identity] += ' changed'
                decision = self.decide(self.Key(**expected['key']), texts[identity], self.validated)
                self.assertFalse(decision.permits(self.surfaces))
                with self.assertRaisesRegex(AssertionError, 'entire direct-PD body'):
                    self.run_oracles(texts=texts)

    def test_each25_basis_surface_and_whole_record_tamper_refuse(self):
        for identity, expected in self.expected.items():
            for field, value in [('publication_basis', 'unresolved'), ('surfaces', []),
                                 ('publication_status', 'unresolved')]:
                with self.subTest(target=identity, field=field):
                    changed = dict(self.parsed)
                    changed[identity] = dict(self.parsed[identity], **{field: value})
                    validated = dict(self.validated)
                    validated[self.Key(**expected['key'])] = changed[identity]
                    self.assertFalse(self.decide(self.Key(**expected['key']), self.texts[identity], validated).permits(self.surfaces))
                    with self.assertRaises(AssertionError):
                        self.run_oracles(parsed=changed, validated=validated)

    def test_each25_actual_production_denial_is_not_ignored(self):
        for identity, expected in self.expected.items():
            target = self.Key(**expected['key'])
            def deny(key, text, records):
                decision = self.decide(key, text, records)
                return dataclasses.replace(decision, publication_status='unresolved') if key == target else decision
            with self.subTest(target=identity), self.assertRaisesRegex(AssertionError, 'actual production decision permits'):
                self.run_oracles(decide=deny)

    def test_artifact_pin_and_actual_metadata_payload_bytes_are_exact(self):
        for path in [p for p in self.pins if p.startswith('src/sources/')]:
            with self.subTest(path=path):
                pins = dict(self.pins, **{path: '0' * 64})
                with self.assertRaisesRegex(AssertionError, 'exact declared direct-PD artifact input'):
                    self.run_oracles(pins=pins)
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            source = Path(temporary)
            paths = [p for p in self.pins if p.startswith('src/sources/')]
            for path in paths:
                target = source / path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(G.REPO / path, target)
            for path in paths:
                target = source / path
                original = target.read_bytes()
                target.write_bytes(original + b'changed')
                with self.subTest(path=path), self.assertRaisesRegex(AssertionError, 'exact declared direct-PD artifact input'):
                    self.run_oracles(source=source)
                target.write_bytes(original)

    def test_entire_code_pinned_declaration_and_explicit_input_are_required(self):
        self.assertEqual(G.direct_declaration(G.REPO, self.pins)[0], self.declaration)
        with self.assertRaisesRegex(AssertionError, 'exact direct-PD declaration'):
            G.direct_declaration(G.REPO, {})
        with tempfile.TemporaryDirectory(dir=SCRATCH) as temporary:
            root = Path(temporary)
            path = root / G.DIRECT_DECLARATION
            path.parent.mkdir(parents=True)
            path.write_text('{}\n')
            with self.assertRaisesRegex(AssertionError, 'exact direct-PD declaration'):
                G.direct_declaration(root, self.pins)

    def test_legacy_projection_logic_and_all_immutable_history_are_preserved(self):
        old = ast.parse((PATH.parent / 'support.py').read_text())
        new = ast.parse((PATH.parent / 'support_v3.py').read_text())
        for name in ['projection_oracles', 'ledger', 'hashrows', 'reverse', 'replay_spec']:
            original = next(node for node in old.body if isinstance(node, ast.FunctionDef) and node.name == name)
            successor = next(node for node in new.body if isinstance(node, ast.FunctionDef) and node.name == name)
            self.assertEqual(ast.dump(original), ast.dump(successor), name)
        _, _, _, prior, rows, originals, proof = G.parent_state()
        self.assertEqual(len(rows), 5615)
        self.assertEqual(len(originals), 17)
        self.assertEqual(len(proof['historical_fields']), 12)
        self.assertEqual(G.digest((G.REPO / G.HELPER).read_bytes()), G.HELPER_SHA)
        current = self.support['hashrows'](self.parsed)
        parent = prior['latin_current_rows']['roman-1962']
        added = sorted(set(current) - set(parent) - set(self.expected))
        changed = sorted(key for key in parent if parent[key] != current[key] and key not in self.expected)
        editions, artifacts, cross, _ = self.support['projection_oracles'](G.REPO, prior, self.parsed, added, changed)
        for field, actual in [('new_projection_specs', editions), ('new_projection_artifact_specs', artifacts),
                              ('cross_supplement_specs', cross)]:
            for identity, expected in prior[field].items():
                if field == 'new_projection_specs':
                    self.assertEqual(actual[identity]['artifact_id'], expected['artifact_id'])
                    self.assertTrue(set(expected['publication_source_ids']) <= set(actual[identity]['publication_source_ids']))
                    self.assertTrue(set(expected['projected_from']) <= set(actual[identity]['projected_from']))
                else:
                    self.assertEqual(actual[identity], expected)


if __name__ == '__main__':
    unittest.main()
