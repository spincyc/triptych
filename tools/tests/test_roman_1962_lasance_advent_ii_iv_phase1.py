"""Nine exact held Lasance AdventII–IV orations, not expanded target endings."""
from __future__ import annotations

import copy
import csv
import hashlib
import importlib.machinery
import importlib.util
from pathlib import Path
import sys
import tomllib
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / 'src/sources/calendars'
LEDGER = ROOT / 'src/sources/inventories/roman-1962-proper-translations-v1.toml'
PREFIX = 'francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945'
EDITION = 'edition.' + PREFIX
EDITION_PATH = ROOT / 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945'
PDF = 'artifact.' + PREFIX + '.internet-archive-facsimile-pdf-6cf3c3d0'
PDF_SHA = '6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70'
TARGET_SHA = '648fdb8fe830ed65a08aa4a95de6f94424c533ddf2398c8fc26b18735fd3518a'
ARTIFACT_SHA = 'a106d2a587ef20ccd75a28548d95ba35554a383e5cbc6a8fcf75e92e43ff6024'
ARTIFACT_SLUG = 'advent-ii-iv-orations-en-checked-a106d2a5'
ARTIFACT = 'artifact.' + PREFIX + '.' + ARTIFACT_SLUG
EXPECTED = {
    ('advent-2', 'Collect'): ('acfbdb00b27e8097a5294fe180005dfc960e68664d901d23e5e2749d1f06d7ff', [107, 108], '106-107', 84, 3, 12, 'Qui tecum.', 'Qui tecum vivit et regnat in unitate.'),
    ('advent-2', 'Secret'): ('5ac16883af6b9c91146aedbf10663ac61780cf17bb096bf8381f261a728fefd5', [110, 110], '109', 85, 4, 18, 'Per Dominum nostrum.', 'Per Dominum.'),
    ('advent-2', 'Postcommunion'): ('879f911de092881efaea36fa43b394f8a62693de54881884d91504c4054b6a41', [110, 110], '109', 85, 4, 20, 'Per Dominum nostrum.', 'Per Dominum.'),
    ('advent-3', 'Collect'): ('2b81be5e96065956bf062e03ef9e2a95692e0c0e3797e8c0774b2a32b8d94b0a', [111, 111], '110', 85, 4, 22, 'Qui vivis.', 'Qui vivis et regnas cum Deo Patre in unitate.'),
    ('advent-3', 'Secret'): ('8158f4caf6b826be428ff6955182e8d69189d2ee60601ab2710932aa47920457', [113, 113], '112', 86, 5, 28, 'Per Dominum.', 'Per Dominum.'),
    ('advent-3', 'Postcommunion'): ('e8d7be1c405c86d96f6d129846283274e5e9f9b60e0fb50fc04a7a185c8cc0a7', [114, 114], '113', 86, 5, 30, 'Per Dominum.', 'Per Dominum.'),
    ('advent-4', 'Collect'): ('9eaab53e7ad1ad4fbc6b1310308249b586216fe955e4882e0b8b98de9d4e36d5', [131, 131], '130', 95, 14, 89, 'Qui vivis.', 'Qui vivis et regnas cum Deo Patre in unitate.'),
    ('advent-4', 'Secret'): ('d3361db50d5f53019e2c809b21040698b2dea8ec87bed24bc5c2c74592c95554', [133, 133], '132', 96, 15, 95, 'Per Dominum.', 'Per Dominum nostrum.'),
    ('advent-4', 'Postcommunion'): ('ac7e9bd2e457e7b0652edb809fc5e2d4fd948d025fb984b13c7dd358f464333f', [133, 133], '132', 96, 15, 97, 'Per Dominum.', 'Per Dominum nostrum Jesum Christum, Filium tuum: Qui tecum vivit et regnat in unitate.'),
}
ACTIVE = {key: value for key, value in EXPECTED.items() if key != ('advent-2', 'Collect')}


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def load_propers():
    loader = importlib.machinery.SourceFileLoader(
        'lasance_advent_ii_iv_phase1_propers', str(ROOT / 'tools/mass-propers'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


class LasanceAdventIIIVPhase1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = tomllib.loads(LEDGER.read_text())
        cls.entries = {(r['mass'], r['proper']): r for r in cls.document['entries']
                       if (r['mass'], r['proper']) in ACTIVE}
        cls.artifact = tomllib.loads(
            (EDITION_PATH / 'artifacts' / ARTIFACT_SLUG / 'artifact.toml').read_text())

    def test_eight_exact_identities_replace_only_their_absences(self):
        self.assertEqual(len(self.entries), 8)
        self.assertEqual(set(self.entries), set(ACTIVE))
        for key, expected in ACTIVE.items():
            row = self.entries[key]
            with self.subTest(key=key):
                self.assertEqual(
                    (row['form_id'], row['cycle'], row['occurrence'], row['witness']),
                    ('main', 'all', 1, 'lasance-1945'))
                self.assertEqual(len(row['translations']), 1)
                translation = row['translations'][0]
                self.assertEqual(
                    (translation['lang'], translation['rights'], translation['source_id']),
                    ('en', 'public-domain', EDITION))
                self.assertEqual(sha(translation['text']), expected[0])
                ending = 'Who livest.' if key[1] == 'Collect' else 'Through our Lord.'
                self.assertTrue(translation['text'].endswith(ending))
                self.assertFalse(translation['text'].endswith('Amen.'))
                self.assertIn('Former Cummiskey1861 lead remains unbound', row['witness_note'])
                self.assertIn('no cross-appointment reuse', row['witness_note'])
                self.assertFalse({'speaker', 'actor', 'text_structure'} & row.keys())
        self.assertFalse([r for r in self.document['untranslated']
                          if (r['mass'], r['proper']) in ACTIVE])

    def test_source_discrepancies_are_retained_not_silently_corrected(self):
        self.assertNotIn(('advent-2', 'Collect'), self.entries)
        absences = [r for r in self.document['untranslated']
                    if (r['mass'], r['proper']) == ('advent-2', 'Collect')]
        self.assertEqual(len(absences), 1)
        self.assertEqual(absences[0]['reason'], {'kind': 'witness-gap', 'source_id': EDITION})
        self.assertIn('evidence-only', absences[0]['note'])
        collect = tomllib.loads((EDITION_PATH / 'passages' /
            'verify-phase1-advent-2--main--collect--all--1.toml').read_text())
        for phrase in ('internal source conclusion discrepancy', 'Source Latin ending: Qui tecum.',
                       'not an equivalent English expansion', 'not corrected or harmonized',
                       'not attached to the target overlay'):
            self.assertIn(phrase, collect['notes'])
        self.assertIn('we beseech thee,', self.entries['advent-4', 'Collect']['translations'][0]['text'])
        self.assertIn('O Lord upon', self.entries['advent-4', 'Secret']['translations'][0]['text'])
        self.assertIn('this holy Mystery', self.entries['advent-3', 'Secret']['translations'][0]['text'])

    def test_exact_payload_and_separate_page_and_publication_passages(self):
        artifact = self.artifact
        self.assertEqual((artifact['id'], artifact['edition_id'], artifact['derived_from']),
                         (ARTIFACT, EDITION, PDF))
        self.assertEqual((artifact['storage'], artifact['rights_status'], artifact['rights_jurisdiction']),
                         ('tracked', 'public-domain', 'United States'))
        self.assertIn('80b34759fb18ec60f6205460c2ac24dc9e4a861938a94ef1f8e04a08a398ac9a',
                      artifact['rights_basis'])
        self.assertIn('Independent cold review remains required', artifact['provenance'])
        payload = (ROOT / artifact['path']).read_bytes()
        self.assertEqual(sha(payload), ARTIFACT_SHA)
        self.assertEqual(len(payload), artifact['byte_size'])
        rows = list(csv.DictReader(payload.decode().splitlines(), delimiter='\t'))
        self.assertEqual([(r['mass'], r['proper']) for r in rows], list(EXPECTED))
        for line, (key, expected) in enumerate(EXPECTED.items(), 2):
            digest, pages, printed, target_page, target_printed, unit, source_end, target_end = expected
            mass, proper = key
            row = self.entries.get(key)
            suffix = f'phase1-{mass}--main--{proper.lower()}--all--1.toml'
            verify = tomllib.loads((EDITION_PATH / 'passages' / ('verify-' + suffix)).read_text())
            publish = tomllib.loads((EDITION_PATH / 'passages' / ('publish-' + suffix)).read_text())
            with self.subTest(key=key):
                self.assertEqual((publish['artifact_id'], publish['artifact_sha256'],
                                  publish['physical_line_ranges']),
                                 (ARTIFACT, ARTIFACT_SHA, [[line, line]]))
                self.assertEqual((verify['artifact_id'], verify['artifact_sha256'],
                                  verify['artifact_page_ranges']), (PDF, PDF_SHA, [pages]))
                if row is not None:
                    self.assertEqual((row['passage_id'], row['publication_passage_id']),
                                     (verify['id'], publish['id']))
                self.assertEqual(verify['locus'], publish['locus'])
                self.assertEqual(verify['locus'], f'{mass}/{proper.lower()}')
                if row is not None:
                    self.assertEqual(row['ia_leaf_range'], [p - 1 for p in pages])
                    self.assertEqual(row['ia_leaf'], pages[0] - 1)
                    self.assertEqual(row['printed_page'], printed)
                self.assertEqual(verify['verified_on'], '2026-10-22')
                for phrase in (f'Source Latin ending: {source_end}', f'Target Latin ending: {target_end}',
                               f'temporal-{mass}-orations', TARGET_SHA,
                               f'PDF{target_page}/printed{target_printed}, unit{unit}'):
                    self.assertIn(phrase, verify['notes'])
                self.assertEqual(sha(rows[line - 2]['english']), digest)
                if row is not None:
                    self.assertEqual(rows[line - 2]['english'], row['translations'][0]['text'])
        private = tomllib.loads((EDITION_PATH /
            'artifacts/internet-archive-facsimile-pdf-6cf3c3d0/artifact.toml').read_text())
        self.assertEqual((private['rights_status'], private['storage']), ('unresolved', 'remote'))

    def test_production_overlay_and_both_calendar_censuses_remain_accounted(self):
        propers = load_propers()
        overlay, untranslated, stale, witnesses = propers.translation_overlay('roman-1962', CALENDARS)
        self.assertEqual(stale, [])
        self.assertEqual(witnesses[EDITION]['witness_relation'], 'antecedent')
        self.assertNotIn(('advent-2', 'main', 'Collect', 'all', 1), overlay)
        for mass, proper in ACTIVE:
            row = overlay[mass, 'main', proper, 'all', 1]
            self.assertEqual(row['publication_artifact_id'], ARTIFACT)
            self.assertEqual(row['publication_artifact_sha256'], ARTIFACT_SHA)
            self.assertEqual(row['translations'], self.entries[mass, proper]['translations'])
        for calendar in ('roman-1962', 'roman-pre-1955'):
            census = propers.english_coverage(CALENDARS, calendar)
            for field in ('unaccounted', 'outside_the_ledger', 'unmatched_records', 'stale_translation_records'):
                self.assertEqual(census[field], 0, (calendar, field))

    def test_missing_publication_triple_stale_hash_and_changed_body_fail_closed(self):
        propers = load_propers()
        _, _, _, witnesses = propers.translation_overlay('roman-1962', CALENDARS)
        original = self.entries['advent-3', 'Collect']
        for field in ('publication_artifact_id', 'publication_artifact_sha256', 'publication_passage_id'):
            changed = copy.deepcopy(original)
            del changed[field]
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'partial translation publication'):
                propers.validate_translation_publication_binding(changed, CALENDARS, LEDGER, witnesses)
        changed = copy.deepcopy(original)
        changed['publication_artifact_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'artifact hash is stale'):
            propers.validate_translation_publication_binding(changed, CALENDARS, LEDGER, witnesses)
        changed = copy.deepcopy(original)
        changed['translations'][0]['text'] += ' Amen.'
        with self.assertRaisesRegex(ValueError, 'body differs'):
            propers.validate_translation_publication_binding(changed, CALENDARS, LEDGER, witnesses)

    def test_page_proof_stale_hash_range_and_verification_state_fail_closed(self):
        propers = load_propers()
        _, _, _, witnesses = propers.translation_overlay('roman-1962', CALENDARS)
        records, trouble = propers._source_library_records(CALENDARS)
        original = self.entries['advent-3', 'Collect']
        # Whole-library diagnostics have their own validator. Establish this
        # exact binding first, then mutate only its in-memory proof record.
        propers.validate_translation_publication_binding(original, CALENDARS, LEDGER, witnesses)
        for field, value, diagnostic in (
            ('artifact_sha256', '0' * 64, 'verification passage artifact hash is stale'),
            ('artifact_page_ranges', [[111, 112]], 'exact IA leaf range'),
            ('states', ['inspected'], 'not inspected and dated verified'),
        ):
            changed_records = dict(records)
            changed_records[original['passage_id']] = dict(records[original['passage_id']], **{field: value})
            with self.subTest(field=field), mock.patch.object(
                    propers, '_source_library_records', return_value=(changed_records, trouble)):
                with self.assertRaisesRegex(ValueError, diagnostic):
                    propers.validate_translation_publication_binding(original, CALENDARS, LEDGER, witnesses)


if __name__ == '__main__':
    unittest.main()
