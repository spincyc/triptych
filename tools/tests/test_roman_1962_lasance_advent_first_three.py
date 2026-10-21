"""Exact first three Lasance Advent bodies and their two source bindings."""
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

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / 'src/sources/calendars'
LEDGER = ROOT / 'src/sources/inventories/roman-1962-proper-translations-v1.toml'
EDITION = 'edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945'
PREFIX = 'francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945'
EDITION_PATH = ROOT / 'src/sources/works/francis-xavier-lasance/the-new-roman-missal/editions/benziger-revised-1945'
PDF = 'artifact.' + PREFIX + '.internet-archive-facsimile-pdf-6cf3c3d0'
PDF_SHA = '6cf3c3d01b853bc4a35c1cc9b0a4e54a0489a5ccf5d9a742bb681ac10608ce70'
ARTIFACT_SHA = '6959278995fd1b8747e7ad2bd529ab84256e5c5c4ebedee456852a43ea356d42'
ARTIFACT = 'artifact.' + PREFIX + '.advent-first-three-orations-en-checked-69592789'
EXPECTED = {
    'Collect': ('af044b6295827b95e17438d092fa41ee6517f61b7ec2e8671e15d462911d39cd', 104, 103, 'Who livest.'),
    'Secret': ('6d5fd77c4a4600e95bdbc1334555bf3511355ca6ad75f6ac99208f97db89dd84', 106, 105, 'Through our Lord.'),
    'Postcommunion': ('eab520f9de3793e0dc7db8fa20421a1ce42f9c9596779d7b17f4663c11fc0081', 107, 106, 'Through our Lord.'),
}

def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()

def load_propers():
    loader = importlib.machinery.SourceFileLoader('lasance_advent_first_three_propers', str(ROOT / 'tools/mass-propers'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module

class LasanceAdventFirstThreeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = tomllib.loads(LEDGER.read_text())
        cls.entries = {row['proper']: row for row in cls.document['entries']
                       if row['mass'] == 'advent-1' and row['proper'] in EXPECTED}
        cls.artifact = tomllib.loads((EDITION_PATH / 'artifacts/advent-first-three-orations-en-checked-69592789/artifact.toml').read_text())

    def test_exact_three_source_bodies_keep_abbreviated_conclusions(self):
        self.assertEqual(set(self.entries), set(EXPECTED))
        for proper, (expected_sha, page, printed, ending) in EXPECTED.items():
            row = self.entries[proper]
            self.assertEqual((row['form_id'], row['cycle'], row['occurrence'], row['witness']), ('main', 'all', 1, 'lasance-1945'))
            self.assertEqual(len(row['translations']), 1)
            text = row['translations'][0]['text']
            self.assertEqual(sha(text), expected_sha)
            self.assertTrue(text.endswith(ending))
            self.assertFalse(text.endswith('Amen.'))
            self.assertNotIn('eternal', text)
            self.assertEqual((row['translations'][0]['lang'], row['translations'][0]['rights'], row['translations'][0]['source_id']), ('en', 'public-domain', EDITION))
            self.assertFalse({'speaker', 'actor', 'text_structure'} & set(row))
            self.assertIn('Former Cummiskey1861 lead remains unbound', row['witness_note'])
        absences = [r for r in self.document['untranslated'] if r['mass'] == 'advent-1' and r['proper'] in EXPECTED]
        self.assertEqual(absences, [])

    def test_exact_payload_one_row_passages_and_private_page_proofs(self):
        artifact = self.artifact
        self.assertEqual((artifact['id'], artifact['edition_id'], artifact['derived_from']), (ARTIFACT, EDITION, PDF))
        self.assertEqual((artifact['storage'], artifact['rights_status'], artifact['rights_jurisdiction']), ('tracked', 'public-domain', 'United States'))
        self.assertIn('80b34759fb18ec60f6205460c2ac24dc9e4a861938a94ef1f8e04a08a398ac9a', artifact['rights_basis'])
        payload = (ROOT / artifact['path']).read_bytes()
        self.assertEqual(sha(payload), ARTIFACT_SHA)
        self.assertEqual(len(payload), artifact['byte_size'])
        lines = payload.decode().splitlines()
        rows = list(csv.DictReader(lines, delimiter='\t'))
        self.assertEqual([r['proper'] for r in rows], list(EXPECTED))
        self.assertEqual(len(rows), 3)
        for line, (proper, (expected_sha, page, printed, ending)) in enumerate(EXPECTED.items(), 2):
            entry = self.entries[proper]
            verify = tomllib.loads((EDITION_PATH / ('passages/verify--advent-1--main--' + proper.lower() + '--all--1.toml')).read_text())
            publish = tomllib.loads((EDITION_PATH / ('passages/publish--advent-1--main--' + proper.lower() + '--all--1.toml')).read_text())
            self.assertEqual((publish['artifact_id'], publish['artifact_sha256'], publish['physical_line_ranges']), (ARTIFACT, ARTIFACT_SHA, [[line, line]]))
            self.assertEqual((verify['artifact_id'], verify['artifact_sha256'], verify['artifact_page_ranges']), (PDF, PDF_SHA, [[page, page]]))
            self.assertEqual(publish['locus'], verify['locus'])
            self.assertEqual((entry['publication_passage_id'], entry['passage_id']), (publish['id'], verify['id']))
            self.assertEqual(entry['ia_leaf_range'], [page - 1, page - 1])
            self.assertEqual(sha(rows[line - 2]['english']), expected_sha)
            self.assertEqual(rows[line - 2]['english'], entry['translations'][0]['text'])
        pdf_record = tomllib.loads((EDITION_PATH / 'artifacts/internet-archive-facsimile-pdf-6cf3c3d0/artifact.toml').read_text())
        self.assertEqual(pdf_record['rights_status'], 'unresolved')
        self.assertEqual(pdf_record['storage'], 'remote')

    def test_production_overlay_retains_historical_antecedent_identity(self):
        propers = load_propers()
        overlay, untranslated, stale, witnesses = propers.translation_overlay('roman-1962', CALENDARS)
        self.assertEqual(stale, [])
        for proper in EXPECTED:
            row = overlay['advent-1', 'main', proper, 'all', 1]
            self.assertEqual(row['translations'][0]['source_id'], EDITION)
            self.assertEqual(witnesses[EDITION]['witness_relation'], 'antecedent')
            self.assertEqual(row['publication_artifact_id'], ARTIFACT)
            self.assertEqual(row['publication_artifact_sha256'], ARTIFACT_SHA)
        self.assertIn(EDITION, witnesses)
        for calendar in ('roman-1962', 'roman-pre-1955'):
            census = propers.english_coverage(CALENDARS, calendar)
            for field in ('unaccounted', 'outside_the_ledger', 'unmatched_records', 'stale_translation_records'):
                self.assertEqual(census[field], 0, (calendar, field))

    def test_publication_triple_and_exact_body_fail_closed_when_stale(self):
        propers = load_propers()
        original = self.entries['Collect']
        # The real public loader first establishes the valid1945 route. These
        # independent mutations then exercise its existing atomic join guard.
        _, _, _, witnesses = propers.translation_overlay('roman-1962', CALENDARS)
        for field in ('publication_artifact_id', 'publication_artifact_sha256', 'publication_passage_id'):
            changed = copy.deepcopy(original)
            del changed[field]
            with self.subTest(missing=field), self.assertRaisesRegex(ValueError, 'partial translation publication'):
                propers.validate_translation_publication_binding(changed, CALENDARS, LEDGER, witnesses)
        changed = copy.deepcopy(original)
        changed['publication_artifact_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'artifact hash is stale'):
            propers.validate_translation_publication_binding(changed, CALENDARS, LEDGER, witnesses)
        changed = copy.deepcopy(original)
        changed['translations'][0]['text'] += ' Amen.'
        with self.assertRaisesRegex(ValueError, 'body differs'):
            propers.validate_translation_publication_binding(changed, CALENDARS, LEDGER, witnesses)

if __name__ == '__main__':
    unittest.main()
