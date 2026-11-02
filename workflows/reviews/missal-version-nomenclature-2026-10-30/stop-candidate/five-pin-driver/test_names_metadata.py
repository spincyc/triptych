"""Bounded metadata and fresh-parent runtime controls; emits no candidate."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd().resolve()
spec = importlib.util.spec_from_file_location('names_metadata_subject', HERE / 'names_metadata.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Store:
    def __init__(self, rows):
        self.rows = rows
    def tree(self, revision):
        return self.rows
    def blob(self, revision, name):
        return self.rows[name]


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ready, cls.updates, cls.runtime = m.names_context(ROOT)
        cls.support = runpy.run_path(str(ROOT / m.SUPPORT))
        cls.prior = json.loads((ROOT / m.FIXTURE).read_bytes())
        cls.rows = json.loads((ROOT / m.MANIFEST).read_bytes())
        cls.before = {p: (ROOT / (m.OWN if p == m.TEST else m.NAMES) / 'before' / p).read_bytes() for p in cls.updates}
        cls.after = {p: (ROOT / (m.OWN if p == m.TEST else m.NAMES) / 'postimages' / p).read_bytes() for p in cls.updates}
        cls.originals = {p: cls.support['reverse'](cls.before[p] if p in cls.before else (ROOT / p).read_bytes(), s) for p, s in cls.prior['files'].items()}
        versions = ROOT / m.NAMES / 'postimages/scripts/_missal_versions.py'
        cls.versions = runpy.run_path(str(versions))

    def test_exact_real_names_context(self):
        self.assertEqual(set(self.updates), m.SOURCE_INPUTS)
        self.assertEqual(len(self.runtime), 7)

    def test_real_bookkeeping_preserves_every_oracle_and_original_stream(self):
        result, rows = m.successor(self.prior, self.rows, self.before, self.after, self.originals, self.support)
        self.assertEqual([r['path'] for r in rows], sorted(r['path'] for r in self.rows))
        self.assertEqual({k for k in result if result[k] != self.prior[k]},
                         {'files', 'source_input_manifest_sha256', 'acceptance', 'state'})
        for field in self.support['HISTORICAL_FIELDS']:
            self.assertEqual(result[field], self.prior[field])
        store = self.support['GitObjects'](ROOT)
        for name, spec in result['files'].items():
            raw = self.after[name] if name in self.after else (ROOT / name).read_bytes()
            self.assertEqual(self.support['reverse'](raw, spec), store.blob(self.support['ORIGINAL'], name))
        self.assertEqual(result['current_roman_document_sha256'], self.prior['current_roman_document_sha256'])
        self.assertEqual(result['reviewed_transition_contract_sha256'], self.prior['reviewed_transition_contract_sha256'])
        self.assertEqual({p for p in result['files'] if result['files'][p] != self.prior['files'][p]}, {m.PC, m.TEST})
        self.assertEqual(len([p for p in result['files'] if result['files'][p] == self.prior['files'][p]]), 15)

    def test_nonheader_semantic_changes_refuse(self):
        before = {'edition': 'old', 'calendar': 'fixed', 'body': 'words', 'source_id': 'source',
                  'grade': 'unresolved', 'rights': 'restricted', 'appointments': [1], 'choices': [1]}
        for field in ('calendar', 'body', 'source_id', 'grade', 'rights', 'appointments', 'choices'):
            with self.subTest(field=field), self.assertRaisesRegex(AssertionError, 'header-only'):
                m.header_only(before, {**before, 'edition': 'new', field: 'altered'})

    def test_allowed_headers_are_metadata_only(self):
        m.header_only({'calendar': 'fixed', 'text': 'same', 'edition': 'old'},
                      {'calendar': 'fixed', 'text': 'same', 'edition': 'new', 'advisory': 'partial'})

    def test_header_nonmetadata_boolean_integer_float_types_are_exact(self):
        before = {'calendar': 'same', 'appointments': [{'occurrence': 1}], 'edition': 'old'}
        for value in [True, 1.0]:
            after = copy.deepcopy(before);after['edition'] = 'new';after['appointments'][0]['occurrence'] = value
            with self.subTest(value=repr(value)), self.assertRaisesRegex(AssertionError, 'header-only'):
                m.header_only(before, after)

    def catalog(self):
        path = 'src/sources/calendars/recensions.json'
        return json.loads(self.before[path]), json.loads(self.after[path])

    def test_catalog_identity_change_refuses(self):
        before, after = self.catalog(); after['recensions'][1]['id'] = 'invented'
        with self.assertRaisesRegex(AssertionError, 'preserved scholarly'):
            m.catalog_only(before, after)

    def test_catalog_permission_upgrade_refuses(self):
        before, after = self.catalog()
        after['recensions'][0]['capabilities']['calendar']['publication_availability'] = 'available'
        with self.assertRaisesRegex(AssertionError, 'preserved scholarly'):
            m.catalog_only(before, after)

    def test_catalog_unknown_top_field_refuses(self):
        before, after = self.catalog(); after['permission'] = True
        with self.assertRaisesRegex(AssertionError, 'top-level'):
            m.catalog_only(before, after)

    def test_catalog_preserved_year_type_is_exact(self):
        before, after = self.catalog()
        # Pick an existing scholarly year rather than a new Names book field.
        def replace_year(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if type(child) is int and child == 1920:
                        value[key] = 1920.0;return True
                    if replace_year(child):return True
            elif isinstance(value, list):
                return any(replace_year(child) for child in value)
            return False
        self.assertTrue(replace_year(after['recensions']))
        with self.assertRaisesRegex(AssertionError, 'preserved scholarly'):
            m.catalog_only(before, after)

    def test_duplicate_manifest_rows_refuse(self):
        rows = copy.deepcopy(self.rows); rows[-1] = rows[0]
        with self.assertRaisesRegex(AssertionError, 'exact7264'):
            m.successor(self.prior, rows, self.before, self.after, self.originals, self.support)

    def test_extra_manifest_row_field_refuses(self):
        rows = copy.deepcopy(self.rows); rows[0]['permission'] = True
        with self.assertRaisesRegex(AssertionError, 'row schema'):
            m.successor(self.prior, rows, self.before, self.after, self.originals, self.support)

    def test_extra_source_path_refuses(self):
        after = {**self.after, 'src/sources/new-body.txt': b'words'}
        with self.assertRaisesRegex(AssertionError, 'five exact existing'):
            m.successor(self.prior, self.rows, self.before, after, self.originals, self.support)

    def test_fifth_test_postimage_is_fixed_not_arbitrary_source(self):
        after = {**self.after, m.TEST: self.after[m.TEST] + b'\nUNREVIEWED = True\n'}
        with self.assertRaisesRegex(AssertionError, 'separately reviewed fifth test delta'):
            m.successor(self.prior, self.rows, self.before, after, self.originals, self.support)

    def test_missing_fifth_test_delta_refuses(self):
        after = {p: raw for p, raw in self.after.items() if p != m.TEST}
        with self.assertRaisesRegex(AssertionError, 'five exact existing'):
            m.successor(self.prior, self.rows, self.before, after, self.originals, self.support)

    def test_fifth_test_branch_is_the_only_new_ast(self):
        marker = b'            elif path == "scripts/_missal_coverage.py":\n'
        start = self.after[m.TEST].index(b'            elif path == "scripts/_calendars.py":\n')
        end = self.after[m.TEST].index(marker, start)
        restored = self.after[m.TEST][:start] + self.after[m.TEST][end:]
        self.assertEqual(restored, self.before[m.TEST])

    def test_snapshot_cannot_be_resampled_from_named_current_code(self):
        wrong = (ROOT / m.NAMES / 'postimages/scripts/_calendars.py').read_bytes()
        self.assertNotEqual(m.sha(wrong), m.SNAPSHOT_SHA)
        self.assertEqual(m.sha((ROOT / m.OWN / 'postimages' / m.SNAPSHOT).read_bytes()), m.SNAPSHOT_SHA)

    def test_generic_root_receipt_cannot_authorize_fifth_source(self):
        temp = tempfile.TemporaryDirectory(dir=HERE);self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve();p = root / 'root.json'
        raw = m.encoded({'status': 'accepted', 'schema': 'generic', 'source': 'anything'});p.write_bytes(raw)
        with self.assertRaisesRegex(AssertionError, 'Root exact test application'):
            m.test_root_binding(root, 'root.json', m.sha(raw), 'a' * 40)

    def exact_root_binding(self):
        temp = tempfile.TemporaryDirectory(dir=HERE);self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve()
        ref = 'review.json'
        review = ROOT / m.OWN / 'test-cold-review/REVIEW-RECEIPT-v1.json'
        (root / ref).write_bytes(review.read_bytes())
        self.assertEqual(m.sha(review.read_bytes()), m.TEST_REVIEW_SHA)
        value = {'schema': 'triptych-root-Names-phase5-calendars-currentness/v1',
                 'status': 'applied-exact-reviewed-test-and-snapshot',
                 'test': {'path': m.TEST, 'before_sha256': m.TEST_BEFORE, 'after_sha256': m.TEST_AFTER},
                 'historical_snapshot': {'path': m.SNAPSHOT, 'sha256': m.SNAPSHOT_SHA},
                 'Named_calendars_after_sha256': m.NAMED_CALENDARS,
                 'parent_git_revision': 'a' * 40,
                 'parent_source_receipt_sha256': m.RECEIPT_SHA,
                 'independent_test_review': {'path': ref, 'sha256': m.TEST_REVIEW_SHA}}
        return root, value

    def bind(self, root, value):
        raw = m.encoded(value);(root / 'root.json').write_bytes(raw)
        return m.test_root_binding(root, 'root.json', m.sha(raw), 'a' * 40)

    def test_exact_separate_root_review_binding_accepts_only_known_pair(self):
        root, value = self.exact_root_binding()
        self.assertEqual(self.bind(root, value), value)

    def test_root_binding_wrong_test_postimage_refuses(self):
        root, value = self.exact_root_binding();value['test']['after_sha256'] = '0' * 64
        with self.assertRaisesRegex(AssertionError, 'fixed Root'):
            self.bind(root, value)

    def test_root_binding_wrong_snapshot_refuses(self):
        root, value = self.exact_root_binding();value['historical_snapshot']['sha256'] = m.NAMED_CALENDARS
        with self.assertRaisesRegex(AssertionError, 'fixed Root'):
            self.bind(root, value)

    def test_root_binding_old_named_current_code_refuses(self):
        root, value = self.exact_root_binding();value['Named_calendars_after_sha256'] = m.SNAPSHOT_SHA
        with self.assertRaisesRegex(AssertionError, 'fixed Root'):
            self.bind(root, value)

    def test_root_binding_wrong_epoch_or_review_refuses(self):
        for field in ('parent_source_receipt_sha256', 'parent_git_revision', 'independent_test_review'):
            root, value = self.exact_root_binding()
            if field == 'independent_test_review':value[field]['sha256'] = '0' * 64
            else:value[field] = '0' * 64
            with self.subTest(field=field), self.assertRaises(AssertionError):
                self.bind(root, value)

    def test_wrong_metadata_preimage_refuses(self):
        before = {**self.before, m.PC: self.before[m.PC] + b'\n'}
        with self.assertRaisesRegex(AssertionError, 'metadata preimage'):
            m.successor(self.prior, self.rows, before, self.after, self.originals, self.support)

    def test_missing_new_parent_commit_refuses(self):
        with self.assertRaisesRegex(AssertionError, 'supply fresh accepted parent'):
            m.parent_state(ROOT, None, self.support)

    def test_old702_is_not_current_accepted_parent(self):
        with self.assertRaisesRegex(AssertionError, 'accepted English parent binding'):
            m.parent_state(ROOT, '702f650020d69a45aa747b1c5b5e30be6c42ca59', self.support)

    def runtime_case(self, raw, parent_raw, names=None):
        temp = tempfile.TemporaryDirectory(dir=HERE); self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve(); name = 'scripts/code.py'; path = root / name
        path.parent.mkdir(); path.write_bytes(raw)
        store = Store({name: parent_raw} if parent_raw is not None else {})
        return root, name, path, m.Runtime(root, store, 'fresh-parent', names or {})

    def test_runtime_uses_fresh_parent_not_old_v3(self):
        root, name, path, guard = self.runtime_case(b'NEW_MAIN = True\n', b'NEW_MAIN = True\n')
        guard.check(path); self.assertEqual(guard.observed[name], m.sha(path.read_bytes()))

    def test_runtime_changed_unreviewed_parent_dependency_refuses(self):
        root, name, path, guard = self.runtime_case(b'UNREVIEWED = True\n', b'NEW_MAIN = True\n')
        with self.assertRaisesRegex(AssertionError, 'fresh-parent-or-Names'):
            guard.check(path)

    def test_runtime_parent_fallback_for_named_successor_refuses(self):
        name = 'scripts/code.py'
        root, _, path, guard = self.runtime_case(b'BEFORE = True\n', b'BEFORE = True\n', {name: m.sha(b'AFTER = True\n')})
        with self.assertRaisesRegex(AssertionError, 'fresh-parent-or-Names'):
            guard.check(path)

    def test_runtime_exact_new_named_helper_accepts(self):
        name = 'scripts/code.py'; raw = b'EXACT_NEW = True\n'
        root, _, path, guard = self.runtime_case(raw, None, {name: m.sha(raw)})
        guard.check(path)

    def test_runtime_unrecognized_new_helper_refuses(self):
        root, name, path, guard = self.runtime_case(b'NEW = True\n', None)
        with self.assertRaisesRegex(AssertionError, 'unreviewed new runtime'):
            guard.check(path)

    def test_runtime_symlink_to_venv_does_not_escape(self):
        root, name, path, guard = self.runtime_case(b'OLD = True\n', b'OLD = True\n')
        path.unlink(); path.symlink_to(Path(sys.prefix) / 'lib/python3.14/site-packages/yaml/__init__.py')
        with self.assertRaisesRegex(AssertionError, 'ordinary repository input'):
            guard.check(path)

    def test_runtime_venv_prefix_traversal_refuses(self):
        temp = tempfile.TemporaryDirectory(dir=HERE);self.addCleanup(temp.cleanup)
        path = Path(temp.name).resolve() / 'code.py';path.write_bytes(b'BAD = True\n')
        name = path.relative_to(ROOT).as_posix()
        alias = Path(sys.prefix) / os.path.relpath(path, sys.prefix)
        guard = m.Runtime(ROOT, Store({name: b'OLD = True\n'}), 'fresh-parent', {})
        with self.assertRaisesRegex(AssertionError, 'canonical runtime path'):
            guard.check(alias)

    def test_runtime_external_alias_into_repository_refuses(self):
        root, name, path, guard = self.runtime_case(b'BAD = True\n', b'OLD = True\n')
        alias = root.parent / ('alias-' + root.name + '.py')
        alias.symlink_to(path);self.addCleanup(alias.unlink)
        with self.assertRaisesRegex(AssertionError, 'external runtime alias'):
            guard.check(alias)

    def test_nested_interpreter_prefix_alias_into_repo_code_refuses(self):
        root, name, path, guard = self.runtime_case(b'BAD = True\n', None)
        prefix = root / 'venv';alias = prefix / 'lib/site-packages/alias.py'
        alias.parent.mkdir(parents=True);alias.symlink_to(path)
        with patch.object(sys, 'prefix', str(prefix)):
            with self.assertRaisesRegex(AssertionError, 'interpreter runtime alias'):
                guard.check(alias)

    def test_unknown_metadata_byte_is_not_accepted_by_a_receipt(self):
        temp = tempfile.TemporaryDirectory(dir=HERE); self.addCleanup(temp.cleanup)
        root = Path(temp.name).resolve(); name = 'catalog.json'; (root / name).write_bytes(b'{"accepted":true}')
        with self.assertRaisesRegex(AssertionError, 'exact bytes'):
            m.pinned(root, name, m.sha(b'{"reviewed":true}'))

    def test_top_presentation_changes_preserve_producer_semantics(self):
        before = {'calendar': 'same', 'edition': 'old', 'masses': [{'text': 'same'}]}
        after = {**before, 'edition': 'new', 'reader_version': {'id': 'label'}}
        self.assertEqual(m.producer_semantics(before), m.producer_semantics(after))

    def test_nested_text_rights_source_grade_choice_and_event_changes_are_visible(self):
        old = {'masses': [{'text': 'words', 'rights': 'restricted', 'source': 'id',
                           'grade': 'antecedent', 'choice': 'one', 'event': 'fixed', 'edition': 'witness'}]}
        for field in old['masses'][0]:
            changed = copy.deepcopy(old);changed['masses'][0][field] = 'different'
            with self.subTest(field=field):
                self.assertNotEqual(m.producer_semantics(old), m.producer_semantics(changed))

    def test_producer_boolean_integer_float_choice_types_are_exact(self):
        old = {'masses': [{'occurrence': 1, 'reading_choice': False}]}
        for field, value in [('occurrence', True), ('occurrence', 1.0), ('reading_choice', 0)]:
            changed = copy.deepcopy(old);changed['masses'][0][field] = value
            with self.subTest(field=field, value=repr(value)):
                self.assertNotEqual(m.canonical(m.producer_semantics(old)), m.canonical(m.producer_semantics(changed)))

    def test_metadata_coverage_counts_without_body_are_ineligible(self):
        value = {'coverage': {'available': 9999}, 'reader_version': {'label': 'Missal'}, 'masses': []}
        self.assertFalse(self.versions['contribution_from_published'](propers=value)['eligible'])

    def test_restricted_and_withheld_bodies_are_ineligible(self):
        for node in [
            {'translations': [{'text': 'words', 'rights': 'restricted', 'lang': 'en'}]},
            {'text': 'words', 'latin': {'withheld': True}, 'coverage': {'languages': [
                {'lang': 'la', 'availability': 'available', 'publication_basis': 'public-domain'}]}},
            {'kind': 'rubric', 'translations': [{'text': 'words', 'rights': 'public-domain', 'lang': 'en'}]},
        ]:
            with self.subTest(node=node):
                self.assertFalse(self.versions['contribution_from_published'](propers={'masses': [{'propers': [node]}]})['eligible'])

    def test_current_six_reviewed_producer_inputs_preserve_contribution_counts(self):
        validation = json.loads((ROOT / m.NAMES / 'VALIDATION.json').read_bytes())
        for row in validation['actual_current_reader_contributions']:
            values = []
            for ref in row['input_files']:
                values.append(json.loads(m.pinned(ROOT, ref['path'], ref['sha256'])))
            actual = self.versions['contribution_from_published'](propers=values[0], ordinary=values[1])
            self.assertEqual(actual, row['actual_current_published_contribution'])
            self.assertTrue(actual['eligible'])

    def test_aliases_resolve_only_declared_readers_and_refuse_books(self):
        temp = tempfile.TemporaryDirectory(dir=HERE);self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        catalog = json.loads(self.after['src/sources/calendars/recensions.json'])
        (root / 'recensions.json').write_bytes(m.encoded(catalog))
        normalize = self.versions['normalize_calendar_key']
        for row in catalog['reader_views']:
            for key in [row['calendar'], row['reader_version']['id'], *row['reader_version']['aliases']]:
                self.assertEqual(normalize(root, key), row['calendar'])
        for key in ['unknown-reader', *(r['id'] for r in catalog['books'])]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                normalize(root, key)

    def test_alias_collision_refuses(self):
        temp = tempfile.TemporaryDirectory(dir=HERE);self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        catalog = json.loads(self.after['src/sources/calendars/recensions.json'])
        catalog['reader_views'][2]['reader_version']['aliases'].append('roman-1962')
        (root / 'recensions.json').write_bytes(m.encoded(catalog))
        with self.assertRaisesRegex(ValueError, 'ambiguous reader alias'):
            self.versions['normalize_calendar_key'](root, 'roman-1962')


if __name__ == '__main__':
    unittest.main(verbosity=2)
