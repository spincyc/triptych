"""Shared source-path admission precedes CLI material and language projection."""
from __future__ import annotations

import argparse
import contextlib
import copy
import importlib.machinery
import importlib.util
import io
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(os.environ.get('TRIPTYCH_REVIEW_ROOT', Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get('TRIPTYCH_SOURCE_PATH_CLI_ROOT', ROOT))
CORE_ROOT = Path(os.environ.get('TRIPTYCH_SOURCE_PATH_MODULE_ROOT', MODULE_ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(CORE_ROOT / 'scripts'))
import _calendars as C
loader = importlib.machinery.SourceFileLoader('_source_path_cli_today', str(MODULE_ROOT / 'tools/mass-today'))
spec = importlib.util.spec_from_loader(loader.name, loader)
TODAY = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = TODAY
loader.exec_module(TODAY)
TODAY.SEATING_MODEL = Path(os.environ.get('TRIPTYCH_APPOINTMENT_SEATING', ROOT / 'src/web/browser/liturgy/ordinary-seating.js'))
OLD = None
if os.environ.get('TRIPTYCH_SOURCE_PATH_CLI_BASELINE'):
    old_loader = importlib.machinery.SourceFileLoader('_source_path_cli_today_before', str(Path(os.environ['TRIPTYCH_SOURCE_PATH_CLI_BASELINE']) / 'tools/mass-today'))
    old_spec = importlib.util.spec_from_loader(old_loader.name, old_loader)
    OLD = importlib.util.module_from_spec(old_spec)
    old_loader.exec_module(OLD)
    OLD.SEATING_MODEL = TODAY.SEATING_MODEL

BASIS = 'Technical correlated-source fixture; no historical permission or words are asserted.'
ORDINARY = {'sections': [{'key': 'section', 'name': 'Technical frame', 'elements': [{'key': 'frame', 'kind': 'prayer', 'name': 'Technical prayer', 'translations': [{'lang': 'en', 'text': 'Technical frame body.'}]}]}], 'slots': [{'id': 'first-reading', 'anchor': 'frame', 'where': 'before', 'propers': ['First Reading']}, {'id': 'gospel', 'anchor': 'frame', 'where': 'before', 'propers': ['Gospel']}]}


def coordinate(name, occurrence=1):
    return {'mass': 'fixture', 'form_id': 'main', 'proper': name, 'occurrence': occurrence}


def member(name, cycle, occurrence=1):
    return {'appointment': coordinate(name, occurrence), 'material_cycle': {'family': 'cycles', 'cycle': cycle}}


def raw_payload(*, conditional=False, grouped=False):
    names = ['First Reading', 'Gospel'] + (['Gospel'] if grouped else [])
    propers = [{'name': name, 'source': 'scripture', 'cycles': {cycle: {'verses': [{'ref': f'Technical {name} {index} {cycle}'}]} for cycle in ('A', 'B', 'C')}} for index, name in enumerate(names)]
    if grouped:
        for index, option in ((1, 'longer'), (2, 'shorter')):
            propers[index]['ordinary_disposition'] = {'kind': 'alternative', 'group': 'gospel', 'option': option, 'basis': BASIS}
    paths = []
    for identifier, cycle, standing in [('native-b', 'B', 'principal'), ('optional-a', 'A', 'optional')]:
        path = {'id': identifier, 'standing': standing, 'calendar_cycles': {'family': 'sunday', 'in': ['B']}, 'choices': {'gospel': 'longer'} if grouped else {}, 'members': [member('First Reading', cycle), member('Gospel', cycle)]}
        if conditional and identifier == 'optional-a':
            path['when'] = {'fact': 'technical-actual-use', 'is': True}
        if grouped and identifier == 'native-b':
            path['choices'] = {'gospel': 'shorter'}
            path['members'][1] = member('Gospel', cycle, occurrence=2)
        paths.append(path)
    mass = {'key': 'fixture', 'propers': propers, 'proper_source_paths': [{'id': 'reading-set', 'form_id': 'main', 'basis': BASIS, 'paths': paths}]}
    document = {'calendar': 'postconciliar', 'sections': {'seasonal': {'kind': 'seasonal', 'masses': [mass]}}}
    appointed, errors = C.resolve_propers(document, mass, appointments=True)
    assert not errors, errors
    passages = {verse['ref']: {'text': f"Technical Bible words: {verse['ref']}"} for proper in propers for owner in proper['cycles'].values() for verse in owner['verses']}
    public_mass = copy.deepcopy(mass)
    public_mass['proper_source_paths'] = C.public_proper_source_paths(document, mass)
    return {'mass': public_mass, 'appointed': [{'form': form, 'form_id': 'main', 'proper': proper, 'taken_from': taken_from} for form, proper, taken_from in appointed], 'bible': {'id': 'fixture-bible', 'passages': passages}}


def arguments(*, machine=False, expanded=True, choices=None):
    return argparse.Namespace(date='2026-10-20', calendar='postconciliar', expanded=expanded, ordinary=False, ordinary_variant=None, territory=None, mass=None, form=None, proper_choice=choices or [], lang='en', bible='fixture-bible', witness=None, why=False, rubrics=True, json=False, format='json' if machine else 'text', style_resolved=TODAY.Style())


def selection(path='optional-a'):
    return 'proper-choice/postconciliar/fixture/main/reading-set=' + path


def mass_of(payload=None, args=None):
    args = args or arguments()
    mass = TODAY.propers_of('postconciliar', 'fixture', args, {'sunday': 'B', 'weekday': 'II'}, payload=payload or raw_payload())
    mass.update(key='fixture', name='Technical Mass')
    return mass


def prepared(mass, choices=None, facts=None, ordinary=None):
    context = {'date': '2026-10-20', 'season': 'ordinary', 'condition_facts': facts or {}}
    rows = [{'proper': proper, 'sourceIndex': index} for proper, index in zip(mass['propers'], mass['_proper_source_indices'])]
    return TODAY.mass_events(ordinary, rows, None, context, TODAY.proper_appointment_context_for('postconciliar', mass, context, choices))


class ProperSourcePathCliTests(unittest.TestCase):
    def test_raw_cycle_owners_survive_until_shared_admission(self):
        source = raw_payload(); snapshot = copy.deepcopy(source)
        mass = mass_of(source)
        self.assertNotIn('verses', source['appointed'][0]['proper'])
        self.assertEqual(source, snapshot)
        self.assertNotIn('verses', mass['propers'][0])
        self.assertEqual(mass['propers'][0]['cycles'], source['appointed'][0]['proper']['cycles'])
        self.assertNotIn('text', mass['propers'][0]['cycles']['A']['verses'][0])
        self.assertEqual(mass['_calendar_cycles'], {'sunday': 'B', 'weekday': 'II'})

    def test_authorized_material_a_does_not_change_calendar_b(self):
        mass = mass_of(); snapshot = copy.deepcopy(mass)
        for ordinary in (None, ORDINARY):
            with self.subTest(framed=ordinary is not None):
                result = prepared(mass, [selection()], ordinary=ordinary)
                actual = [event['proper'] for event in result['events'] if event['kind'] == 'proper']
                self.assertEqual([p['verses'][0]['ref'] for p in actual], ['Technical First Reading 0 A', 'Technical Gospel 1 A'])
                self.assertTrue(all(' A' in p['verses'][0]['text'] for p in actual))
                self.assertEqual(result['material_selections'], {'0': {'family': 'cycles', 'cycle': 'A'}, '1': {'family': 'cycles', 'cycle': 'A'}})
                self.assertEqual(result['source_path_selections']['main/reading-set'], {'state': 'selected', 'option': 'optional-a'})
        self.assertEqual(mass, snapshot)

    def test_multiple_held_paths_remain_required_without_body_claims(self):
        mass = mass_of()
        result = prepared(mass)
        self.assertEqual(result['events'], [])
        self.assertEqual(result['material_selections'], {})
        self.assertEqual(result['source_path_selections']['main/reading-set'], {'state': 'required', 'option': None})
        self.assertEqual(result['source_path_unresolved'][0]['kind'], 'source-path-required')
        language = TODAY.language_account([{'masses': [mass]}], 'en', {'id': 'fixture-bible', 'language': 'en'}, {id(mass): result['_prepared_rows']})
        self.assertEqual(language['selection']['units'], 0)
        self.assertTrue(all('language_selection' not in p for p in mass['propers']))

    def test_unknown_false_and_true_actual_use_are_distinct(self):
        mass = mass_of(raw_payload(conditional=True))
        unknown = prepared(mass)
        self.assertEqual(unknown['source_path_availability']['main/reading-set']['optional-a']['state'], 'unresolved')
        for value in (None, False):
            with self.subTest(value=value), self.assertRaises(TODAY.Refused):
                prepared(mass, [selection()], {'technical-actual-use': value})
        true = prepared(mass, [selection()], {'technical-actual-use': True})
        self.assertEqual(true['material_selections']['0']['cycle'], 'A')
        false = prepared(mass, facts={'technical-actual-use': False})
        self.assertEqual(false['source_path_selections']['main/reading-set']['option'], 'native-b')

    def test_mixed_tuple_wrong_cycle_and_stale_identity_refuse(self):
        mass = mass_of(raw_payload(grouped=True))
        with self.assertRaises(TODAY.Refused):
            prepared(mass, [selection(), 'proper-choice/postconciliar/fixture/main/gospel=shorter'])
        bad = copy.deepcopy(mass); bad['_calendar_cycles']['sunday'] = 'C'
        with self.assertRaises(TODAY.Refused):
            prepared(bad, [selection()])
        for choice in (selection('missing'), selection().replace('/fixture/', '/other/'), selection().replace('/main/', '/missing/')):
            with self.subTest(choice=choice), self.assertRaises(TODAY.Refused):
                prepared(mass, [choice])

    def test_inactive_invalid_cycle_is_validated_before_selection(self):
        mass = mass_of(); mass['propers'][0]['cycles']['D'] = {'verses': [{'ref': 'Technical invalid inactive course'}]}
        with self.assertRaises(TODAY.Refused):
            prepared(mass, [selection()])

    def test_language_absence_uses_admitted_owner(self):
        payload = raw_payload()
        payload['appointed'][0]['proper']['cycles']['A']['untranslated'] = [{'lang': 'en', 'state': 'rights-restricted', 'cycle': 'A'}]
        payload['appointed'][0]['proper']['cycles']['B']['untranslated'] = [{'lang': 'en', 'state': 'no-english-exemplar', 'cycle': 'B'}]
        mass = mass_of(payload)
        result = prepared(mass, [selection()])
        language = TODAY.language_account([{'masses': [mass]}], 'en', {'id': 'fixture-bible', 'language': 'en'}, {id(mass): result['_prepared_rows']})
        self.assertEqual(language['selection']['statuses']['withheld'], 1)
        self.assertEqual(mass['propers'][0]['language_selection']['status'], 'withheld')
        self.assertNotIn('language_selection', mass['propers'][0]['cycles']['B'])

    def test_ordinary_payload_without_relation_keeps_existing_projection(self):
        payload = raw_payload()
        payload['mass'].pop('proper_source_paths')
        for row in payload['appointed']:
            row['proper'].pop('source_path_relation', None)
            row['proper'].pop('appointment_identity', None)
        args = arguments()
        result = TODAY.propers_of('postconciliar', 'fixture', args, {'sunday': 'B'}, payload=copy.deepcopy(payload))
        self.assertNotIn('proper_source_paths', result)
        self.assertNotIn('_calendar_cycles', result)
        self.assertEqual(result['propers'][0]['verses'][0]['ref'], 'Technical First Reading 0 B')
        if OLD is not None:
            self.assertEqual(result, OLD.propers_of('postconciliar', 'fixture', args, {'sunday': 'B'}, payload=copy.deepcopy(payload)))
            self.assertEqual(TODAY.mass_events(None, result['propers'], None), OLD.mass_events(None, result['propers'], None))

    def test_missing_relation_cannot_bypass_raw_guard_in_text(self):
        payload = raw_payload(); payload['mass'].pop('proper_source_paths')
        for expanded in (False, True):
            args = arguments(expanded=expanded)
            output = io.StringIO()
            with contextlib.redirect_stdout(output), patch.object(TODAY, 'language_account', wraps=TODAY.language_account) as account, self.assertRaisesRegex(TODAY.Refused, 'relation'):
                self.run_day(args, payload)
            self.assertEqual(account.call_count, 0)
            self.assertNotIn('Technical Bible words:', output.getvalue())

    def run_day(self, args, payload=None, *, ranked=None, module=None):
        payload = payload or raw_payload()
        module = module or TODAY
        ranked = ranked or {'days': [{'calendar': 'postconciliar', 'season': 'ordinary', 'weekday': 'tuesday', 'liturgicalYear': {'lectionary': {'sunday': 'B', 'weekday': 'II'}}, 'options': [{'settled': True, 'winner': {'key': 'fixture', 'nature': 'feast'}, 'readable': [{'key': 'fixture', 'state': 'said'}]}]}]}
        def invoke(tool, argv):
            if tool == 'calendar-rubrics': return copy.deepcopy(ranked)
            if tool == 'mass-ordinary': return {'ordinary': [copy.deepcopy(ORDINARY)]}
            raise AssertionError(tool)
        with patch.object(module, 'invoke', side_effect=invoke), patch.object(module, 'invoke_propers', return_value={'fixture': payload}), patch.object(module, 'indexed_bible', return_value={'id': 'fixture-bible', 'language': 'en'}):
            return module.run_show(args)

    @unittest.skipIf(OLD is None, 'requires exact predecessor for full payload comparison')
    def test_no_source_feature_full_payload_equals_current_predecessor(self):
        source = raw_payload()
        source['mass'].pop('proper_source_paths')
        for row in source['appointed']:
            row['proper'].pop('source_path_relation', None)
            row['proper'].pop('appointment_identity', None)
        branches = [{'option': option, 'settled': True, 'winner': {'key': 'fixture', 'nature': 'feast'},
                     'readable': [{'key': 'fixture', 'state': 'said'}]} for option in ('technical-one', 'technical-two')]
        for machine, expanded, unresolved_territory in ((True, True, False), (False, True, False), (True, False, False), (True, False, True)):
            args = arguments(machine=machine, expanded=expanded)
            ranked = None if not unresolved_territory else {'days': [{'calendar': 'postconciliar', 'season': 'ordinary', 'weekday': 'tuesday', 'liturgicalYear': {'lectionary': {'sunday': 'B', 'weekday': 'II'}}, 'options': branches}]}
            with self.subTest(machine=machine, expanded=expanded, unresolved_territory=unresolved_territory):
                actual = self.run_day(args, copy.deepcopy(source), ranked=copy.deepcopy(ranked))
                expected = self.run_day(copy.deepcopy(args), copy.deepcopy(source), ranked=copy.deepcopy(ranked), module=OLD)
                self.assertEqual(actual, expected)

    def test_actual_run_show_text_machine_and_language_use_same_admission(self):
        for machine in (False, True):
            args = arguments(machine=machine, choices=[selection()])
            payload = self.run_day(args)
            mass = payload['days'][0]['masses'][0]
            self.assertEqual(mass['source_path_selections']['main/reading-set']['option'], 'optional-a')
            self.assertEqual(mass['propers'][0]['language_selection']['delegated_to']['references'], ['Technical First Reading 0 A'])
            self.assertEqual(payload['language']['selection']['units'], 2)
            self.assertNotIn('verses', mass['propers'][0])
            self.assertEqual(mass['propers'][0]['cycles']['B']['verses'][0]['ref'], 'Technical First Reading 0 B')
            if machine:
                self.assertNotIn('_calendar_cycles', mass)
                self.assertNotIn('_proper_source_indices', mass)
                self.assertEqual([e['source_index'] for e in mass['expanded_events'] if e['kind'] == 'proper'], [0, 1])
            else:
                output = io.StringIO()
                with contextlib.redirect_stdout(output): TODAY.render(payload, args)
                self.assertIn('Technical Bible words: Technical First Reading 0 A', output.getvalue())
                self.assertNotIn('Technical Bible words: Technical First Reading 0 B', output.getvalue())

    def test_only_admitted_owner_receives_bible_metadata_after_one_shared_bridge(self):
        for machine, expanded in ((True, True), (False, True), (True, False)):
            source = raw_payload()
            source_before = copy.deepcopy(source)
            args = arguments(machine=machine, expanded=expanded, choices=[selection()] if expanded else [])
            with self.subTest(machine=machine, expanded=expanded), patch.object(TODAY, 'mass_events', wraps=TODAY.mass_events) as bridge:
                payload = self.run_day(args, source)
                self.assertEqual(bridge.call_count, 1)
                mass = payload['days'][0]['masses'][0]
                if not expanded:
                    self.assertNotIn('expanded_events', mass)
                for index, row in enumerate(mass['propers']):
                    original = source_before['appointed'][index]['proper']
                    self.assertEqual(list(row['cycles']), list(original['cycles']))
                    for cycle in ('A', 'B', 'C'):
                        owner = row['cycles'][cycle]
                        original_owner = original['cycles'][cycle]
                        self.assertEqual([verse['ref'] for verse in owner['verses']], [verse['ref'] for verse in original_owner['verses']])
                        if expanded and cycle == 'A':
                            self.assertTrue(all('Technical Bible words:' in verse['text'] for verse in owner['verses']))
                        else:
                            self.assertEqual(owner, original_owner)
                if not machine:
                    with contextlib.redirect_stdout(io.StringIO()):
                        TODAY.render(payload, args)
                    self.assertEqual(bridge.call_count, 1)
            self.assertEqual(source, source_before)

    def test_unknown_paths_never_enrich_any_raw_material_owner(self):
        source = raw_payload()
        original = copy.deepcopy(source)
        payload = self.run_day(arguments(machine=True), source)
        mass = payload['days'][0]['masses'][0]
        self.assertEqual(mass['material_selections'], {})
        self.assertFalse(any(event['kind'] == 'proper' for event in mass['expanded_events']))
        for index, row in enumerate(mass['propers']):
            self.assertEqual(row['cycles'], original['appointed'][index]['proper']['cycles'])
            self.assertNotIn('language_selection', row)
        self.assertEqual(source, original)

    def test_compact_and_expanded_unresolved_paths_print_obligation(self):
        for expanded in (False, True):
            args = arguments(expanded=expanded)
            payload = self.run_day(args)
            output = io.StringIO()
            with contextlib.redirect_stdout(output): TODAY.render(payload, args)
            self.assertIn('Source path required: reading-set', output.getvalue())
            self.assertNotIn('Technical Bible words:', output.getvalue())
            self.assertEqual(payload['language']['selection']['units'], 0)


if __name__ == '__main__': unittest.main()
