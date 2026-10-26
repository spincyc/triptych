"""Publisher-proved WEB doxology coordinates recover held wording unchanged."""
from __future__ import annotations

import hashlib
import sys
import unittest
import tomllib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import _loci
from _projection import alias_table

loader = SourceFileLoader('_index_bible_web_romans', str(ROOT / 'tools/index-bible'))
spec = spec_from_loader(loader.name, loader)
index_bible = module_from_spec(spec)
loader.exec_module(index_bible)
ARTIFACTS = index_bible.SOURCE_ROOT / str(index_bible.EDITIONS['world-english-bible-catholic']['artifacts'])
PRIMARY_MEMBER = ROOT / 'src/sources/works/ebible-org/world-english-bible/editions/catholic-eng-web-c/artifacts/usfm-75-romeng-web-c-35fc9b00/75-ROMeng-web-c.usfm'
PRIMARY_SHA256 = '35fc9b00970d6a15bcc5b897335009d9a79ff7c1796ab64ea7b315bc3f3bf6a1'
PARENT_RECORD = ROOT / 'src/sources/works/ebible-org/world-english-bible/editions/catholic-eng-web-c/artifacts/ebible-usfm-6fedbef9/artifact.toml'


class WebRomansProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bible = index_bible.Bible(ARTIFACTS)

    def test_complete_publisher_book_explicitly_states_both_number_ranges(self):
        raw = PRIMARY_MEMBER.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), PRIMARY_SHA256)
        member = tomllib.loads((PRIMARY_MEMBER.parent / 'artifact.toml').read_text())
        parent = tomllib.loads(PARENT_RECORD.read_text())
        self.assertEqual(member['storage'], 'tracked')
        self.assertEqual(member['rights_status'], 'public-domain')
        self.assertEqual(member['derived_from'], parent['id'])
        self.assertEqual(member['sha256'], PRIMARY_SHA256)
        self.assertEqual(parent['sha256'], '6fedbef919e0850ecbe7a9480012c2549f327db7aa7bccf79d1bf6261e9992c1')
        self.assertEqual(parent['storage'], 'remote')
        self.assertEqual(parent['rights_status'], 'unresolved')
        self.assertNotIn('path', parent)
        lines = raw.decode('utf-8-sig').splitlines()
        self.assertIn('TR places verses 24-26 after Romans 16:24 as verses 25-27.', lines[542])
        self.assertIn('TR places Romans 14:24-26 at the end of Romans instead of at the end of chapter 14, and numbers these verses 16:25-27.', lines[626])
        for verse, line_number in ((24, 541), (25, 542), (26, 543)):
            body = lines[line_number - 1].removeprefix(f'\\v {verse} ').split('\\f ', 1)[0].strip()
            self.assertEqual(body, self.bible.verses[('Rom', 14, verse)])

    def test_three_aliases_are_the_exact_publisher_stated_correspondence(self):
        table = alias_table(ARTIFACTS.parent)
        for cited, native in ((25, 24), (26, 25), (27, 26)):
            self.assertEqual(table.get(('Rom', 16, cited)), ('Rom', 14, native))

    def test_complete_doxology_resolves_to_held_native_words(self):
        text, problem = self.bible.passage('Rom', [{
            'begin': {'chapter': 16, 'verse': 25}, 'end': {'chapter': 16, 'verse': 27},
        }])
        self.assertEqual(problem, '')
        self.assertEqual(text, ' '.join(self.bible.verses[('Rom', 14, n)] for n in (24, 25, 26)))

    def test_cross_chapter_carriers_keep_the_cited_reading_order(self):
        text, problem = self.bible.passage('Rom', [{
            'begin': {'chapter': 16, 'verse': 24}, 'end': {'chapter': 16, 'verse': 27},
        }])
        self.assertEqual(problem, '')
        self.assertEqual(text, ' '.join([self.bible.verses[('Rom', 16, 24)],
            *(self.bible.verses[('Rom', 14, n)] for n in (24, 25, 26))]))

    def test_unproved_next_verse_stays_unavailable_and_refuses_a_whole_range(self):
        self.assertIsNone(self.bible.verse('Rom', 16, 28))
        text, problem = self.bible.passage('Rom', [{
            'begin': {'chapter': 16, 'verse': 25}, 'end': {'chapter': 16, 'verse': 28},
        }])
        self.assertEqual(text, '')
        self.assertIn('Rom 16:28', problem)

    def test_native_chapter_and_verse_text_are_unchanged(self):
        self.assertEqual(self.bible.chapters[('Rom', 16)], (1, 24))
        self.assertEqual(self.bible.chapters[('Rom', 14)], (1, 26))
        for n in (24, 25, 26):
            self.assertEqual(self.bible.verse('Rom', 14, n), self.bible.verses[('Rom', 14, n)])

    def test_browser_projection_selects_native_run_without_runtime_arithmetic(self):
        departures, refused = _loci.edition_departures('Rom', {
            key: [{'chapter': 16, 'first': 25, 'last': 27}]
            for key in ('vulgate', 'hebrew', 'hebrew-unnumbered-titles')
        }, {})
        self.assertEqual(departures, {
            'world-english-bible-catholic': [{'chapter': 14, 'first': 24, 'last': 26}],
        })
        self.assertEqual(refused, {})

    def test_unverified_other_book_remains_explicitly_refused(self):
        text, problem = self.bible.passage('Ecclus', [{
            'begin': {'chapter': 3, 'verse': 1}, 'end': {'chapter': 3, 'verse': 1},
        }])
        self.assertEqual(text, '')
        self.assertIn('no exact selection recorded', problem)
