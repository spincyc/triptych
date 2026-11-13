"""Finite Postconciliar admission stays inactive; positive authority is synthetic.

The synthetic authority is installed only by unittest.mock into a temporary
data root. It is never a repository admission or a publication source.
"""
import copy
from contextlib import redirect_stdout
from hashlib import sha256
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import tomllib
import types
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get('TRIPTYCH_FINITE_LATIN_TEST_ROOT', Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT / 'scripts'))
import _calendars as C
import _missal_coverage as COVERAGE
import _proper_latin as L
import _proper_qualified_latin as Q
import _proper_finite_latin_20261029 as ROMAN
import _proper_finite_latin_20261112_postconciliar as F


def tool(name):
    path = ROOT / 'tools' / name
    # A test-only scratch harness may supply the candidate consumer postimage.
    source = Path(os.environ.get('TRIPTYCH_FINITE_LATIN_POSTIMAGES', ROOT)) / 'tools' / name
    if not source.is_file():
        source = path
    module = types.ModuleType('finite_latin_test_' + name.replace('-', '_'))
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    exec(compile(source.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


def synthetic_cases():
    result = []
    for ordinal, key in enumerate(sorted(F.EXPECTED_KEYS), 1):
        body = f'Synthetic body {ordinal}.\nSynthetic conclusion.\nSynthetic response.'
        aid, sid, old = (f'{kind}.finite.postconciliar.fixture{ordinal}' for kind in ('artifact', 'passage', 'artifact.old'))
        payload_sha, body_sha = sha256((body + '\n').encode()).hexdigest(), sha256(body.encode()).hexdigest()
        artifact = {'record_type': 'artifact', 'id': aid, 'edition_id': 'edition.finite.synthetic',
                    'path': f'src/sources/synthetic/{ordinal}.txt', 'sha256': payload_sha,
                    'media_type': 'text/plain; charset=utf-8', 'artifact_type': 'editorial-projection',
                    'storage': 'tracked', 'rights_status': 'project-created',
                    'rights_basis': 'Synthetic contract test only; ' + F.METHOD_ID,
                    'projected_from': [old]}
        passage = {'record_type': 'passage', 'id': sid, 'edition_id': 'edition.finite.synthetic',
                   'artifact_id': aid, 'artifact_sha256': payload_sha,
                   'physical_line_ranges': [[1, 3]], 'language': 'la'}
        records = {aid: artifact, sid: passage, old: {'record_type': 'artifact', 'id': old,
                   'rights_status': 'public-domain', 'storage': 'remote', 'sha256': 'a' * 64}}
        note = 'Synthetic source-based Latin study reconstruction; printed 2002 and 2008 correspondence unestablished.'
        passage['notes'] = note
        row = {**dict(zip(F.KEY_FIELDS, key)), 'text_sha256': body_sha,
               'provenance_status': 'collated', 'source_id': sid, 'source_date': 'Synthetic historical witness',
               'locator': 'Synthetic carrier lines 1–3', 'relationship': F.RELATIONSHIP,
               'verification_source_id': old, 'verification_locator': 'Synthetic old whole source',
               'transformations': ['Synthetic change'], 'provenance_evidence': 'Synthetic source proof',
               'provenance_authority': 'Synthetic assessment', 'provenance_confidence': 'medium',
               'publication_status': 'permitted', 'publication_basis': F.BASIS,
               'surfaces': sorted(F.SURFACES), 'publication_source_ids': [aid, old],
               'publication_locator': 'Synthetic exact-source tuple', 'publication_evidence': 'Synthetic only',
               'publication_authority': F.METHOD_ID, 'note': note}
        scope = {'calendar': 'postconciliar', 'key': list(key), 'row_sha256': F._digest(row),
                 'body_sha256': body_sha, 'source_id': sid, 'artifact_id': aid,
                 'artifact_payload_sha256': payload_sha, 'verification_source_id': old,
                 'publication_source_ids': row['publication_source_ids'], 'projected_from': [old],
                 'physical_line_ranges': [[1, 3]], 'record_sha256': {k: F._digest(v) for k, v in records.items()},
                 'proof_files': None, 'public': {'relationship': F.RELATIONSHIP, 'source_date': row['source_date'],
                     'provenance_confidence': 'medium', 'note': note, 'notice': 'Synthetic qualified assessment; no general permission.'}}
        proper = {'name': key[2], 'source': 'composed', 'text': body, 'notes': note,
                  'translations': [{'lang': 'en', 'source_id': 'synthetic-study', 'rights': 'project-created',
                                    'text': 'Unchanged synthetic study English.', 'caution': 'Synthetic English caution.'}]}
        result.append({'scope': scope, 'row': row, 'proper': proper, 'records': records})
    return result


class FinitePostconciliarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mass = tool('mass-propers')
        cls.today = tool('mass-today')
        cls.reader = tool('source-reader')

    def setUp(self):
        scratch = Path(os.environ.get('TRIPTYCH_FINITE_LATIN_TEST_SCRATCH',
                                     ROOT / '.scratch/modern-finite-latin-contract/test-runs'))
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        candidate_path = os.environ.get('TRIPTYCH_FINITE_LATIN_CANDIDATE_FIXTURES')
        self.cases = (copy.deepcopy(json.loads(Path(candidate_path).read_text())['cases'])
                      if candidate_path else synthetic_cases())
        self.assertEqual({tuple(c['scope']['key']) for c in self.cases}, F.EXPECTED_KEYS)
        proof = b'SYNTHETIC UNIT TEST AUTHORITY. No source admission or publication permission.\n'
        def pin(name):
            relative = 'workflows/reviews/synthetic-finite-test/' + name + '.txt'
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(proof)
            return {'path': relative, 'sha256': sha256(proof).hexdigest()}
        for c in self.cases:
            c['scope']['proof_files'] = {'source_review': pin('source-review'), 'latin_merits': pin('latin-merits')}
            artifact = c['records'][c['scope']['artifact_id']]
            path = self.root / artifact['path']
            path.parent.mkdir(parents=True, exist_ok=True)
            payload = (c['proper']['text'] + '\n').encode()
            self.assertEqual(sha256(payload).hexdigest(), c['scope']['artifact_payload_sha256'])
            path.write_bytes(payload)
        self.authority = {'schema': 'triptych-postconciliar-finite-latin-authority/v1', 'method_id': F.METHOD_ID,
                          'state': 'adopted', 'adoption': pin('root-adoption'),
                          'scopes': [c['scope'] for c in self.cases]}
        self.path = self.root / F.ADOPTION_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.pin_patch = patch.multiple(F, TRUSTED_ROOT=self.root, ADOPTION_SHA256='',
                                       RECOGNITION=F.recognition_from_scopes(self.authority['scopes']))
        self.pin_patch.start()
        self.addCleanup(self.pin_patch.stop)
        self.seal()

    def seal(self):
        payload = json.dumps(self.authority, sort_keys=True).encode()
        self.path.write_bytes(payload)
        F.ADOPTION_SHA256 = sha256(payload).hexdigest()

    def private(self, c):
        return L._decision(L.LatinKey(*c['scope']['key']), c['proper']['text'], c['row']).projection(L.SURFACES)

    def reading(self, c, passage=None, artifact=None):
        records = copy.deepcopy(c['records'])
        artifact = artifact or records[c['scope']['artifact_id']]
        passage = passage or records[c['scope']['source_id']]
        records[artifact['id']] = artifact
        library = types.SimpleNamespace(root=self.root, records={k: types.SimpleNamespace(data=v) for k, v in records.items()})
        return self.reader.reading_of(library, passage)

    def test_every_exact_scope_passes_only_under_explicit_test_authority(self):
        self.assertEqual(len(F._scopes()), 6)
        for c in self.cases:
            with self.subTest(owner=c['scope']['key']):
                row, records = c['row'], c['records']
                self.assertEqual(Q.row_problems(row), [])
                self.assertEqual(L._row_problems('synthetic', row), [])
                self.assertEqual(L._source_record_problems('synthetic', row, records,
                                 authority_root=self.root, effective_calendar='postconciliar'), [])
                self.assertEqual(Q.authority_problems(self.root, row=row), [])
                self.assertEqual(Q.artifact_problems(self.root, records[c['scope']['artifact_id']], sources=records), [])
                read = self.reading(c)
                self.assertTrue(read['readable'], read)
                self.assertEqual(read['text'], c['proper']['text'])

    def test_inactive_missing_pending_and_stale_authority_close_all_routes(self):
        c = self.cases[0]
        for kind in ('empty-pin', 'missing', 'pending', 'tampered'):
            self.authority['state'] = 'adopted'
            self.seal()
            if kind == 'empty-pin': F.ADOPTION_SHA256 = ''
            elif kind == 'missing': self.path.unlink()
            elif kind == 'pending': self.authority['state'] = 'pending'; self.seal()
            else: self.path.write_bytes(self.path.read_bytes() + b' ')
            with self.subTest(kind=kind):
                self.assertFalse(F._scopes())
                self.assertTrue(Q.row_problems(c['row']))
                self.assertTrue(Q.authority_problems(self.root, row=c['row']))
                self.assertFalse(self.reading(c)['readable'])
                self.assertIsNone(Q.public_scope(self.private(c)))
                with self.assertRaisesRegex(ValueError, 'lacks exact admission'):
                    self.mass.public_latin_state(self.private(c), c['proper']['name'])

    def test_sources_edition_keeps_exact_latin_qualification(self):
        for c in self.cases:
            passage = dict(c['records'][c['scope']['source_id']], reading=self.reading(c))
            work = dict.fromkeys(('id', 'title', 'author', 'category', 'languages', 'alternate_titles', 'description'))
            edition = dict.fromkeys(('id', 'title', 'language', 'date', 'year', 'publication',
                                     'editors', 'translators', 'authority', 'jurisdiction'))
            edition.update(passages=[passage], artifacts=[])
            projected = self.reader.edition_payload(work, edition)['passages'][0]
            self.assertTrue(projected['readable'])
            self.assertIn(c['scope']['public']['note'], projected['notes'])
            # Re-pinning a malformed test packet cannot erase the qualification.
            records = copy.deepcopy(c['records'])
            records[c['scope']['source_id']]['notes'] = 'Unqualified replacement.'
            c['scope']['record_sha256'][c['scope']['source_id']] = F._digest(records[c['scope']['source_id']])
            self.seal()
            self.assertTrue(Q.source_problems(c['row'], records, effective_calendar='postconciliar'))

    def test_every_owner_body_proof_surface_and_qualification_mutation_is_refused(self):
        for c in self.cases:
            for field, value in {'mass': 'ot-20', 'form': 'alternative', 'proper': 'Collect',
                'course': 'cycles', 'cycle': 'A', 'occurrence': 2, 'text_sha256': '0' * 64,
                'source_id': 'passage.other', 'verification_source_id': 'passage.wrong',
                'publication_basis': 'public-domain', 'publication_status': 'unresolved',
                'publication_source_ids': [], 'surfaces': ['web'], 'note': '',
                'relationship': 'editorial-projection-exact-to-target', 'provenance_confidence': 'low',
                'unexpected': True}.items():
                with self.subTest(owner=c['scope']['key'], field=field):
                    row = dict(c['row'], **{field: value})
                    self.assertTrue(Q.row_problems(row))
                    self.assertTrue(Q.source_problems(row, c['records'], effective_calendar='postconciliar'))

    def test_no_other_calendar_or_inheritance_is_admitted(self):
        for c in self.cases:
            for calendar in ('', 'roman-1962', 'roman-pre-1955', 'postconciliar-copy'):
                self.assertTrue(Q.source_problems(c['row'], c['records'], effective_calendar=calendar))
            self.assertFalse(Q.inherited_row_exact(c['row']))

    def test_changed_or_missing_controller_is_refused(self):
        for c in self.cases:
            for name in c['records']:
                changed = copy.deepcopy(c['records'])
                changed[name]['changed'] = True
                with self.subTest(owner=c['scope']['key'], source=name):
                    self.assertTrue(Q.source_problems(c['row'], changed, effective_calendar='postconciliar'))
            changed = dict(c['records']); changed.pop(c['scope']['verification_source_id'])
            self.assertTrue(Q.source_problems(c['row'], changed, effective_calendar='postconciliar'))

    def test_carrier_whole_selection_and_newline_are_independent_pins(self):
        for c in self.cases:
            artifact, passage = (c['records'][c['scope'][f]] for f in ('artifact_id', 'source_id'))
            for text in (c['proper']['text'] + '\n', c['proper']['text'].splitlines()[0],
                         c['proper']['text'].replace('\n', ' '), None):
                self.assertTrue(Q.reading_problems(self.root, passage, artifact, sources=c['records'], text=text))
            for field, value in {'physical_line_ranges': [[1, 2]], 'text': 'Different text',
                                 'language': 'en', 'artifact_id': 'artifact.other'}.items():
                self.assertTrue(Q.reading_problems(self.root, dict(passage, **{field: value}), artifact,
                                                  sources=c['records'], text=c['proper']['text']))
            (self.root / artifact['path']).write_text(c['proper']['text'])
            self.assertFalse(self.reading(c)['readable'])

    def test_copied_body_and_wrapper_cannot_strip_recognition(self):
        for c in self.cases:
            row = dict(c['row'], mass='unknown', source_id='passage.copy', publication_basis='public-domain',
                       publication_source_ids=['artifact.copy'], publication_authority='', note='')
            self.assertTrue(Q.row_problems(row))
            for wrapped in (False, True):
                artifact = copy.deepcopy(c['records'][c['scope']['artifact_id']])
                passage = copy.deepcopy(c['records'][c['scope']['source_id']])
                text = c['proper']['text'] + '\n'
                if wrapped: text = 'Prefix.\n' + text + 'Suffix.\n'
                artifact.update(id='artifact.copy', rights_basis='Independent public-domain',
                                path='src/sources/copy.txt', sha256=sha256(text.encode()).hexdigest())
                passage.update(id='passage.copy', artifact_id='artifact.copy', artifact_sha256=artifact['sha256'],
                               physical_line_ranges=[[2, 4]] if wrapped else [[1, 3]])
                (self.root / artifact['path']).write_text(text)
                self.assertFalse(self.reading(c, passage, artifact)['readable'])
        self.path.unlink()
        self.assertTrue(Q.row_problems(row))
        self.assertFalse(self.reading(c, passage, artifact)['readable'])

    def test_malformed_authority_stays_closed_even_when_test_repin_matches(self):
        original = copy.deepcopy(self.authority)
        mutations = [lambda a: a['scopes'].pop(), lambda a: a['scopes'].append(copy.deepcopy(a['scopes'][0])),
            lambda a: a['scopes'][0].update(calendar='roman-1962'),
            lambda a: a['scopes'][0]['key'].__setitem__(-1, True),
            lambda a: a['scopes'][0]['public'].update(relationship='editorial-projection-exact-to-target'),
            lambda a: a['scopes'][0]['public'].update(note=''),
            lambda a: a['scopes'][0]['proof_files'].pop('latin_merits'),
            lambda a: a['scopes'][0]['proof_files']['source_review'].pop('sha256'),
            lambda a: a['scopes'][0]['proof_files']['source_review'].update(path='../outside'),
            lambda a: a['scopes'][0]['proof_files']['source_review'].update(path='.scratch/proof'),
            lambda a: a['scopes'][0].update(record_sha256={}), lambda a: a.update(adoption=None)]
        for index, mutate in enumerate(mutations):
            self.authority = copy.deepcopy(original); mutate(self.authority); self.seal()
            with self.subTest(index=index): self.assertFalse(F._scopes())

    def test_proof_mutation_and_symlink_close_existing_process(self):
        proof = self.root / self.authority['scopes'][0]['proof_files']['source_review']['path']
        before = Q.cache_fingerprint(self.root)
        proof.write_text('Changed proof')
        self.assertNotEqual(before, Q.cache_fingerprint(self.root))
        self.assertFalse(F._scopes())
        proof.unlink(); target = self.root / 'outside.txt'; target.write_text('Synthetic')
        proof.symlink_to(target)
        self.assertFalse(F._scopes())

    def test_public_projection_preserves_qualification_and_unresolved_target_grade(self):
        for c in self.cases:
            private = self.private(c); before = copy.deepcopy(private)
            public = self.mass.public_latin_state(private, c['proper']['name'])
            self.assertEqual(private, before)
            self.assertEqual(public['provenance']['relationship'], F.RELATIONSHIP)
            self.assertEqual(public['provenance']['provenance_confidence'], c['row']['provenance_confidence'])
            self.assertEqual(public['note'], c['scope']['public']['note'])
            self.assertEqual(public['publication']['notice'], c['scope']['public']['notice'])
            self.assertEqual(public['publication']['source_ids'], [c['scope']['artifact_id']])
            self.assertNotIn('verification_source_id', public['provenance'])
            self.assertNotIn('evidence', public['publication'])
            self.assertEqual(COVERAGE.latin_evidence(public)['relationship'], 'unresolved')
            self.assertEqual(self.mass.public_latin_state(public, c['proper']['name']), public)

    def test_tampered_public_metadata_is_not_laundered(self):
        for c in self.cases:
            private = self.private(c)
            mutations = [lambda p: p['provenance'].update(relationship='editorial-projection-exact-to-target'),
                lambda p: p['provenance'].update(provenance_confidence='low'),
                lambda p: p['provenance'].update(source_date='another source'),
                lambda p: p.update(note=''), lambda p: p['publication'].update(notice='unqualified'),
                lambda p: p['publication'].update(basis='public-domain'),
                lambda p: p['publication'].update(source_ids=['artifact.unknown']),
                lambda p: p['provenance'].update(verification_source_id='passage.unknown'),
                lambda p: p.update(withheld=True), lambda p: p.update(state='unavailable'),
                lambda p: p.update(reason='unresolved source'),
                lambda p: p['publication'].update(surfaces=['web']),
                lambda p: p['publication'].update(status='unresolved')]
            for mutate in mutations:
                changed = copy.deepcopy(private); mutate(changed)
                with self.assertRaisesRegex(ValueError, 'lacks exact admission'):
                    self.mass.public_latin_state(changed, c['proper']['name'])

    def test_public_refusal_aborts_body_serialization_in_nested_owners(self):
        for c in self.cases:
            proper = copy.deepcopy(c['proper']); proper['latin'] = self.private(c)
            proper['latin']['note'] = ''
            for payload in ({'appointed': [proper]}, {'mass': {'forms': [{'propers': [proper]}]}},
                            {'mass': {'propers': [{'name': proper['name'], 'cycles': {'A': proper}}]}}):
                with self.assertRaisesRegex(ValueError, 'lacks exact admission'):
                    json.dumps(self.mass.rights_safe_copy(payload))

    def test_cli_refuses_body_when_source_qualification_or_proof_fails(self):
        for c in self.cases:
            original = copy.deepcopy(c['proper']); original['latin'] = self.private(c)
            for mutate in (lambda p: p['latin'].update(note=''),
                           lambda p: p['latin']['publication'].update(status='unresolved'),
                           lambda p: p['latin']['provenance'].update(relationship='editorial-projection-exact-to-target'),
                           lambda p: p.update(text=p['text'] + ' changed')):
                proper = copy.deepcopy(original); mutate(proper)
                for lang in ('la', 'fr'):
                    for select in (C.texts_of, self.mass.select_texts):
                        with self.assertRaisesRegex(ValueError, 'lacks exact admission'):
                            select(proper, lang)
                    with self.assertRaisesRegex(ValueError, 'lacks exact admission'):
                        self.today.proper_lines(proper, self.today.Style(), '', lang=lang, witness=None, seat=None, why=False)
        self.path.unlink()
        with self.assertRaisesRegex(ValueError, 'lacks exact admission'):
            C.texts_of(original, 'la')

    def test_actual_source_sanitizer_removes_stale_body_before_json_projection(self):
        for c in self.cases:
            proper = copy.deepcopy(c['proper'])
            proper['text'] += ' tampered'
            key = c['scope']['key']
            document = {'sections': {'seasonal': {'masses': [{'key': key[0], 'propers': [proper]}]}}}
            records = {L.LatinKey(*key): c['row']}
            carried = self.mass.sanitize_source_proper(document, tuple(key[:3]),
                        (key[0], 'main', key[2], 1), proper, records, L.STRUCTURE_SURFACES)
            public = self.mass.rights_safe_copy(carried)
            self.assertIsNone(public['text'])
            self.assertTrue(public['latin']['withheld'])
            self.assertNotIn('tampered', json.dumps(public))
            self.assertEqual(public.get('translations'), proper.get('translations'))

    def test_all_existing_provenance_rows_keep_their_previous_gate_results(self):
        baseline = types.ModuleType('finite_latin_previous_dispatcher')
        baseline.__file__ = str(ROOT / 'scripts/_proper_qualified_latin.py')
        exec(compile((ROOT / 'scripts/_proper_qualified_latin.py').read_bytes(), baseline.__file__, 'exec'), baseline.__dict__)
        for path in (ROOT / 'src/sources/inventories').glob('*-proper-latin-provenance-v1.toml'):
            table = tomllib.loads(path.read_text())
            for entry in table.get('entries', []):
                row = {**table.get('defaults', {}), **entry}
                with self.subTest(file=path.name, owner=[row.get(f) for f in F.KEY_FIELDS]):
                    self.assertEqual(Q.row_problems(row), baseline.row_problems(row))

    def test_repinning_row_digest_does_not_break_scope_links(self):
        c = self.cases[0]
        original_row, original_scope = copy.deepcopy(c['row']), copy.deepcopy(c['scope'])
        for field, value in {'text_sha256': 'a' * 64, 'source_id': 'passage.other',
                             'verification_source_id': 'passage.other',
                             'publication_source_ids': [c['scope']['artifact_id']]}.items():
            changed = dict(original_row, **{field: value})
            c['scope']['row_sha256'] = F._digest(changed)
            self.seal()
            with self.subTest(field=field):
                self.assertTrue(F.row_problems(changed))
                self.assertTrue(F.source_problems(changed, c['records'], effective_calendar='postconciliar'))
        c['scope'].update(original_scope)

    def test_both_clis_keep_direct_and_fallback_latin_qualification_and_english(self):
        for c in self.cases:
            proper = copy.deepcopy(c['proper']); proper['latin'] = self.mass.public_latin_state(self.private(c), proper['name'])
            note = c['scope']['public']['note']; notice = c['scope']['public']['notice']
            for lang in ('la', 'fr'):
                for select in (C.texts_of, self.mass.select_texts):
                    text, credit, qualification = select(proper, lang)[0]
                    self.assertEqual(text, proper['text']); self.assertIn('Latin source:', credit)
                    self.assertIn(note, qualification); self.assertIn(notice, qualification)
                daily = '\n'.join(self.today.proper_lines(proper, self.today.Style(), '', lang=lang, witness=None, seat=None, why=False))
                stream = io.StringIO()
                with redirect_stdout(stream):
                    self.mass.render_reading({'mass': {'name': 'Synthetic Mass', 'propers': [proper]}}, lang, {})
                for output in (daily, stream.getvalue()):
                    self.assertIn(note, output); self.assertIn(notice, output)
            before = copy.deepcopy(proper)
            selected = C.texts_of(proper, 'en')
            if proper.get('translations'):
                self.assertNotIn(note, repr(selected)); self.assertEqual(proper, before)

    def test_existing_roman_module_and_contract_are_unchanged(self):
        self.assertEqual(sha256((ROOT / 'scripts/_proper_finite_latin_20261029.py').read_bytes()).hexdigest(),
                         '295dcd80507643b4182f998c6ce8fc74c89e2278f0b60bb2fd02049b31162984')
        self.assertEqual(Q.authority_problems(ROOT), [])
        self.assertEqual(ROMAN.authority_problems(ROOT), [])
        self.assertEqual(ROMAN.ADOPTION_PATH,
                         'workflows/reviews/missal-reader-resume-2026-11-12/pius-secret/finite-latin-authority-v6.json')
        self.assertEqual(ROMAN.ADOPTION_SHA256,
                         '7212997024f229fa25f8d4a93901f572fc2b3df325d279120fd81f870db40c1b')
        self.assertEqual(len(ROMAN._scopes()), 38)
        self.assertEqual(Q._digest({name: str(getattr(Q, name)) for name in
            ('ROW_SHA256', 'CONTROLLER_SHA256', 'ARTIFACT_SHA256', 'PARENT_FIELDS', 'SCOPES', 'INHERITED_ROW_SHA256')}),
            '062fe30a78347a6b0fde731a34815dde501c2c0112ada9ab17e470a3d3eaa223')


if __name__ == '__main__':
    unittest.main()
