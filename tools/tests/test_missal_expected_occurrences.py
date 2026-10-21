"""Source-owned occurrence joins for repeated Proper names, not body fidelity."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import _missal_coverage as coverage

FIXTURE = ROOT / 'tools/tests/fixtures/missal-expected-occurrences/roman-1962-ember-oratio-v1.json'


def toml_value(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, (str, int, float)):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return '[' + ', '.join(toml_value(item) for item in value) + ']'
    if isinstance(value, dict):
        return '{' + ', '.join(key + ' = ' + toml_value(item) for key, item in value.items()) + '}'
    raise TypeError(value)


def inventory_text(document):
    lines = [f'{key} = {toml_value(value)}' for key, value in document.items()
             if key not in {'slices', 'targets', 'boundaries'}]
    for kind in ('slices', 'targets', 'boundaries'):
        for row in document[kind]:
            lines += ['', f'[[{kind}]]']
            lines += [f'{key} = {toml_value(value)}' for key, value in row.items()]
    return '\n'.join(lines) + '\n'


def report(document, masses):
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / 'expected.toml'
        path.write_text(inventory_text(document))
        return coverage.expectations(path, 'roman-1962', masses)


def states(result):
    return {row['id']: row['state'] for row in result['targets']}


def small_inventory(*, occurrence='absent', name='Oratio', form='main'):
    parent = {'id': 'form', 'slice_id': 'source', 'kind': 'form', 'identity_state': 'established',
              'calendar_mass_key': 'mass', 'form_id': form}
    target = {'id': 'slot', 'slice_id': 'source', 'kind': 'text-slot', 'identity_state': 'established',
              'parent_id': 'form', 'calendar_proper_name': name}
    if occurrence != 'absent':
        target['calendar_proper_occurrence'] = occurrence
    return {'schema': 'triptych-missal-expected-targets/v1', 'slices': [{
        'id': 'source', 'calendar': 'roman-1962', 'recension_id': 'roman-1962',
        'territory': 'universal', 'languages': ['la', 'en'], 'date_range': 'bounded fixture',
        'source_refs': ['source-record.toml'], 'enumeration_state': 'complete-within-slice',
        'basis': 'Source-owned structural appointment fixture only',
    }], 'targets': [parent, target], 'boundaries': [{
        'id': 'whole-book', 'slice_id': 'source', 'kind': 'text-slots', 'state': 'unenumerated'}]}


class ExpectedProperOccurrenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text())

    def test_all_26_source_qualified_targets_match_the_reviewed_raw_model(self):
        fixture = self.fixture
        joined = states(report(fixture['inventory'], fixture['model_masses']))
        by_mass = {mass['key']: mass for mass in fixture['model_masses']}
        self.assertEqual(len(fixture['joins']), 26)
        for row in fixture['joins']:
            with self.subTest(target=row['target_id']):
                self.assertEqual(joined[row['target_id']], 'represented')
                form = next(form for form in by_mass[row['mass']]['forms'] if form['id'] == row['form_id'])
                named = [proper for proper in form['propers'] if proper['name'] == row['calendar_proper_name']]
                selected = named[row['calendar_proper_occurrence'] - 1]
                self.assertEqual(selected['fixture_target_id'], row['target_id'])
                self.assertEqual(selected['fixture_raw_model_index'], row['frozen_raw_model_index'])
                self.assertTrue(row['source_record'] and row['source_locus'])

    def test_occurrence_counts_all_exact_name_nodes_without_a_body_filter(self):
        mass = {'key': 'mass', 'propers': [
            {'name': 'Antiphon', 'source': 'scripture'},
            {'name': 'Antiphon (other role)', 'source': 'composed'},
            {'name': 'Antiphon', 'source': 'composed'},
        ]}
        for occurrence, expected in ((1, 'represented'), (2, 'represented'), (3, 'not-represented')):
            with self.subTest(occurrence=occurrence):
                self.assertEqual(states(report(small_inventory(occurrence=occurrence, name='Antiphon'), [mass]))['slot'], expected)

    def test_absent_qualifier_preserves_the_legacy_unique_name_rule(self):
        for count, expected in ((0, 'not-represented'), (1, 'represented'), (2, 'not-represented')):
            mass = {'key': 'mass', 'propers': [{'name': 'Oratio'} for _ in range(count)]}
            with self.subTest(count=count):
                self.assertEqual(states(report(small_inventory(), [mass]))['slot'], expected)
        # Explicit occurrence1 retains the same unique-node behavior.
        self.assertEqual(states(report(small_inventory(occurrence=1), [{'key': 'mass', 'propers': [{'name': 'Oratio'}]}]))['slot'], 'represented')

    def test_an_occurrence_cannot_borrow_from_a_sibling_or_missing_form(self):
        mass = {'key': 'mass', 'forms': [
            {'id': 'longer', 'propers': [{'name': 'Oratio'} for _ in range(5)]},
            {'id': 'shorter', 'propers': [{'name': 'Oratio'}]},
        ]}
        for form, expected in (('longer', 'represented'), ('shorter', 'not-represented'), ('missing', 'not-represented')):
            with self.subTest(form=form):
                self.assertEqual(states(report(small_inventory(occurrence=2, form=form), [mass]))['slot'], expected)

    def test_missing_named_nodes_fail_only_their_source_form_joins(self):
        fixture = self.fixture
        changed = copy.deepcopy(fixture['model_masses'])
        mass = next(mass for mass in changed if mass['key'] == 'advent-ember-saturday')
        form = next(form for form in mass['forms'] if form['id'] == 'longer')
        form['propers'] = [proper for proper in form['propers'] if proper['name'] != 'Oratio']
        joined = states(report(fixture['inventory'], changed))
        for row in fixture['joins']:
            with self.subTest(target=row['target_id']):
                expected = 'not-represented' if (row['mass'], row['form_id']) == ('advent-ember-saturday', 'longer') else 'represented'
                self.assertEqual(joined[row['target_id']], expected)

    def test_unresolved_source_identity_and_unclosed_denominator_stay_unresolved(self):
        document = small_inventory(occurrence=2)
        document['targets'][1]['identity_state'] = 'target-correspondence-unresolved'
        result = report(document, [{'key': 'mass', 'propers': [{'name': 'Oratio'}, {'name': 'Oratio'}]}])
        self.assertEqual(states(result)['slot'], 'unresolved')
        self.assertEqual(result['whole_inventory_state'], 'unresolved')
        self.assertEqual(result['boundaries'][0]['state'], 'unenumerated')
        self.assertEqual(result['slices'][0]['enumeration_state'], 'complete-within-slice')

    def test_invalid_or_detached_occurrence_qualifiers_are_rejected(self):
        for value in (0, -1, True, False, 1.0, '1', [], {'value': 1}):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'calendar_proper_occurrence'):
                report(small_inventory(occurrence=value), [])
        for change in ('no-proper', 'ordinary', 'not-text-slot'):
            document = small_inventory(occurrence=1)
            target = document['targets'][1]
            if change != 'not-text-slot':
                target.pop('calendar_proper_name')
            if change == 'ordinary':
                target.update(calendar_ordinary_appointment='preface', calendar_ordinary_option='trinitate')
            if change == 'not-text-slot':
                target['kind'] = 'celebration'
            with self.subTest(change=change), self.assertRaises(ValueError):
                report(document, [])

    def test_qualifier_is_source_only_and_does_not_change_public_report_fields(self):
        result = report(self.fixture['inventory'], self.fixture['model_masses'])
        self.assertEqual(result['whole_inventory_state'], 'unresolved')
        def keys(value):
            if isinstance(value, dict):
                return set(value) | set().union(*(keys(item) for item in value.values()))
            if isinstance(value, list):
                return set().union(*(keys(item) for item in value))
            return set()
        for output in (result, coverage.published_expectations(result)):
            self.assertNotIn('calendar_proper_occurrence', keys(output))
            self.assertNotIn('fixture_target_id', keys(output))
        # Qualifying existing targets changes no source enumeration or IDs.
        self.assertEqual(len([row for row in result['targets'] if row['kind'] == 'text-slot']), 26)


if __name__ == '__main__':
    unittest.main()
