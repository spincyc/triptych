"""Exact source-ref targets may rule on one numbering without opening a locus."""
from __future__ import annotations

import copy
import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))

def load(name):
    loader = SourceFileLoader('_exact_numbering_' + name.replace('-', '_'), str(ROOT / 'tools' / name))
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module

index = load('index-bible')
propers = load('mass-propers')
canon = load('citations')
from _loci import Divergences

REF = 'John 6:64b, 69b'
TARGET = {'vulgate': REF, 'hebrew': 'John 6:63c, 68c'}
ENTRY = canon.parse_citation(REF)
LOCUS = {'book': 'John', 'chapters': [6], 'divergence': 'The exact source pointer identifies two different printed coordinates.',
         'numbering': {'hebrew': 'unrecorded'}, 'citations': {REF: TARGET}}

def table(target=TARGET, numbering='hebrew', stance='unrecorded'):
    locus = copy.deepcopy(LOCUS)
    locus['citations'][REF] = target
    locus['numbering']['hebrew'] = stance
    return Divergences('fixture', {'citation_divergences': [locus]}, [ENTRY], canon, numbering, numberings=('hebrew',))


class ClosedTargetMapTests(unittest.TestCase):
    def test_exact_target_precedes_the_whole_locus_unrecorded_stance(self):
        ranges, problem = table().apply(ENTRY, ENTRY['ranges'])
        self.assertEqual(problem, '')
        self.assertEqual(ranges, canon.parse_citation(TARGET['hebrew'])['ranges'])
        self.assertEqual(ranges[0]['begin']['part'], 'c')

    def test_vulgate_table_shape_and_result_remain_compatible(self):
        scalar, mapped = table(REF, 'vulgate'), table(TARGET, 'vulgate')
        self.assertEqual(scalar.resolved, mapped.resolved)
        self.assertEqual(scalar.apply(ENTRY, ENTRY['ranges']), mapped.apply(ENTRY, ENTRY['ranges']))

    def test_an_omitted_alternate_keeps_its_existing_stance(self):
        for stance in ['unrecorded', 'resolved', 'as-cited']:
            with self.subTest(stance=stance):
                scalar = table(REF, stance=stance)
                mapped = table({'vulgate': REF}, stance=stance)
                self.assertEqual(scalar.apply(ENTRY, ENTRY['ranges']), mapped.apply(ENTRY, ENTRY['ranges']))

    def test_other_references_in_the_same_locus_still_refuse(self):
        for reference in ['John 6:51', 'John 6:63c, 68c', 'John 6:65', 'John 6:64, 69']:
            entry = canon.parse_citation(reference)
            ranges, problem = table().apply(entry, entry['ranges'])
            self.assertEqual(ranges, [])
            self.assertIn('unrecorded', problem)

    def test_an_unregistered_query_numbering_keeps_the_existing_refusal(self):
        ranges, problem = table(numbering='unknown').apply(ENTRY, ENTRY['ranges'])
        self.assertEqual(ranges, [])
        self.assertIn('unrecorded', problem)

    def test_only_closed_registered_target_keys_and_strings_are_accepted(self):
        invalid = [{}, {'hebrew': 'John 6:63c, 68c'}, {'vulgate': REF, 'english': REF},
                   {'vulgate': REF, 'hebrew-unnumbered-titles': REF},
                   {'vulgate': REF, 'note': 'source proof'}, {'vulgate': REF, 'hebrew': ''},
                   {'vulgate': REF, 'hebrew': {'ref': 'John 6:63c, 68c'}},
                   {'vulgate': REF, 'hebrew': 'not a reference'},
                   {'vulgate': REF, 'hebrew': 'Amos 6:1'}]
        for target in invalid:
            with self.subTest(target=target), self.assertRaises(ValueError):
                table(target)

    def test_old_stale_book_and_chapter_guards_cover_the_map(self):
        for changed in [{'citations': {'John 6:65': TARGET}}, {'book': 'Amos'}, {'chapters': [5]}]:
            locus = {**copy.deepcopy(LOCUS), **changed}
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                Divergences('fixture', {'citation_divergences': [locus]}, [ENTRY], canon,
                            'hebrew', numberings=('hebrew',))

    def test_confirm_uses_only_the_selected_exact_target(self):
        class Held:
            def __init__(self): self.ranges = []
            def token(self, _): return 'John'
            def passage(self, token, ranges): self.ranges.append(ranges); return 'held', ''
        bible = Held()
        table().confirm(bible)
        self.assertEqual(bible.ranges, [canon.parse_citation(TARGET['hebrew'])['ranges']])

    def test_confirm_refuses_an_unaddressable_alternate_only_where_it_applies(self):
        artifacts = ROOT / 'src/sources/works' / index.EDITIONS['king-james-version']['artifacts']
        bible = index.Bible(artifacts)
        target = {'vulgate': REF, 'hebrew': 'John 6:999'}
        with self.assertRaises(ValueError): table(target).confirm(bible)
        # The unrelated target cannot invalidate a Vulgate correction.
        table(target, 'vulgate').confirm(bible)


class HeldAnselmTargetTests(unittest.TestCase):
    def test_current_data_preserves_source_ref_and_maps_only_one_exact_alternate(self):
        document = propers.load_calendar(propers.DEFAULT_ROOT, 'postconciliar')
        entries = [entry for _, mass in propers.masses_of(document)
                   for entry, _ in propers.numbered_entries(mass, document['psalm_numbering'])]
        tables = {numbering: index.Divergences('postconciliar', document, entries, canon, numbering)
                  for numbering in propers.SYSTEMS}
        structured = propers.citation_structure(ENTRY, 'hebrew', propers.book_tokens(), tables)
        self.assertEqual(structured['ref'], REF)
        self.assertEqual(structured['loci']['vulgate'], [{'chapter': 6, 'first': 64, 'last': 64},
                                                       {'chapter': 6, 'first': 69, 'last': 69}])
        for addressing in ['hebrew', 'hebrew-unnumbered-titles']:
            self.assertEqual(structured['loci'][addressing], [{'chapter': 6, 'first': 63, 'last': 63},
                                                             {'chapter': 6, 'first': 68, 'last': 68}])
        self.assertEqual(ENTRY['ranges'][0]['begin']['part'], 'b')
        self.assertEqual(set(tables['hebrew'].addressed), {(REF, 'hebrew')})
        other = canon.parse_citation('John 6:51')
        self.assertIn('unrecorded', propers.citation_structure(other, 'hebrew', propers.book_tokens(), tables)['refused']['hebrew'])

    def test_all_seven_held_editions_carry_the_two_sayings(self):
        editions = ['douay-rheims', 'douay-rheims-american-1899', 'clementine-vulgate',
                    'catholic-public-domain-version', 'king-james-version',
                    'revised-version-1895', 'world-english-bible-catholic']
        for edition in editions:
            with self.subTest(edition=edition):
                config = index.EDITIONS[edition]
                bible = index.Bible(ROOT / 'src/sources/works' / config['artifacts'])
                resolution = table(numbering=config['numbering'])
                ranges, problem = resolution.apply(ENTRY, ENTRY['ranges'])
                self.assertEqual(problem, '')
                resolution.confirm(bible)
                text, problem = bible.passage('John', ranges)
                self.assertEqual(problem, '')
                expected = [64, 69] if config['numbering'] == 'vulgate' else [63, 68]
                self.assertEqual(text, ' ... '.join(bible.verses[('John', 6, verse)] for verse in expected))
                self.assertTrue('life' in text.lower() or 'vit' in text.lower())


if __name__ == '__main__':
    unittest.main()
