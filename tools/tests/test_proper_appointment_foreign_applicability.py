"""Foreign appointment rules remain diagnosable without becoming active."""
from __future__ import annotations

import copy
import contextlib
import io
import json
import unittest
from unittest.mock import patch

import test_proper_appointment_contract as H
import test_proper_choice_cli_scope as S

C, MP, TODAY = H.C, H.MP, H.TODAY
SOURCE = 'roman-1962'
TARGET = 'roman-pre-1955'
COMMON = 'fixture-common'
BASIS = 'Technical source-only appointment condition; no historical rule is asserted.'
MARKER = {'state': 'unresolved', 'reason': 'foreign-source-applicability',
          'source_edition': SOURCE, 'target_edition': TARGET, 'basis': BASIS}
FACTS = {'fixture-season': {'edition': SOURCE, 'values': ['outside', 'paschal'],
                          'season_values': {'lent': 'outside', 'paschaltide': 'paschal'}, 'basis': BASIS}}


def body(name):
    return {'name': name, 'source': 'composed', 'text': 'Technical held body for ' + name + '.'}


def fixture(kind='conditional', separated=False):
    first = body('Gradual' if kind == 'conditional' else 'Gospel')
    if kind == 'conditional':
        first['ordinary_disposition'] = {'kind': 'conditional', 'group': 'fixture-gradual', 'basis': BASIS,
                                         'when': {'fact': 'fixture-season', 'in': ['outside']}}
        rows = [first]
    else:
        second = body('Gospel (vel)')
        for row, option in ((first, 'principal'), (second, 'other')):
            row['ordinary_disposition'] = {'kind': 'alternative', 'group': 'gospel', 'option': option, 'basis': BASIS}
            if kind != 'legacy':
                row['ordinary_disposition']['anchor'] = {'mass': COMMON, 'form_id': 'main', 'proper': 'Gospel', 'occurrence': 1}
            if kind == 'when':
                row['ordinary_disposition']['when'] = {'fact': 'fixture-season', 'in': ['outside' if option == 'principal' else 'paschal']}
        rows = [first, *([body('Offertory')] if separated else []), second]
    mass = {'key': COMMON, 'name': 'Technical Common', 'registry': 'fixture-common', 'kind': 'common', 'propers': rows}
    return {'calendar': SOURCE, 'psalm_numbering': 'vulgate', 'proper_appointment_facts': FACTS, 'sections': {'common': {'kind': 'common', 'masses': [mass]}}}


def inherited(source):
    target = {'calendar': TARGET, 'psalm_numbering': 'vulgate', 'sections': {}}
    return C._apply_departures(target, source, SOURCE)


def public_rows(document, key=COMMON):
    rows, problems = C.resolve_propers(document, C.mass_index(document)[key], appointments=True)
    if problems:
        raise AssertionError(problems)
    return rows


def runtime(rows, calendar=TARGET, choices=None):
    return TODAY.mass_events(None, [{'proper': {**p, 'form_id': 'main'}, 'sourceIndex': i}
                                   for i, (_, p, _) in enumerate(rows)], None, {},
                             {'calendar': calendar, 'entrance': 'day', 'facts': {}, 'choices': choices or {}})


class ForeignApplicabilityTest(unittest.TestCase):
    def test_marker_only_rows_refuse_machine_expanded_and_both_text_modes(self):
        marker = {**MARKER, 'source_edition': 'roman-source-fixture', 'target_edition': SOURCE}

        def marked_formulary(key):
            proper = {**body('Gradual'), 'form_id': 'main', 'appointment_applicability': marker}
            return {'propers': [proper], '_proper_source_indices': [7], 'placeholders': 0,
                    'forms': [], 'ordinary_frame': {'applicability': 'full'}}

        runner = S.ProperChoiceCliScopeTests()
        for machine, expanded in ((True, True), (False, True), (False, False)):
            with self.subTest(machine=machine, expanded=expanded):
                args = S.arguments(machine=machine, choices=[])
                args.expanded = expanded
                output = io.StringIO()
                with patch.object(S, 'formulary', side_effect=marked_formulary), contextlib.redirect_stdout(output), \
                     self.assertRaisesRegex(S.TODAY.Refused, 'applicability'):
                    payload = runner.run_day(args, ordinary='suppressed')
                    S.TODAY.render(payload, args)
                self.assertNotIn('Technical held body for Gradual.', output.getvalue())

    def test_marker_is_closed_derived_and_not_a_body_absence(self):
        self.assertEqual(C.validate_appointment_applicability(MARKER, TARGET), MARKER)
        for bad in ({**MARKER, 'text': 'not permitted'}, {**MARKER, 'state': 'active'},
                    {**MARKER, 'reason': 'witness-gap'}, {**MARKER, 'basis': ''},
                    {**MARKER, 'target_edition': SOURCE}, {**MARKER, 'source_edition': 'not an edition'}):
            with self.subTest(marker=bad), self.assertRaises(ValueError):
                C.validate_appointment_applicability(bad)
        with self.assertRaises(ValueError):
            C.validate_appointment_applicability(MARKER, 'another-calendar')
        source = fixture()
        own = C.mass_index(source)[COMMON]['propers'][0]
        own['appointment_applicability'] = MARKER
        self.assertTrue(C.resolve_propers(source, C.mass_index(source)[COMMON])[1])
        problems = []
        H.CHECK.check_proper('fixture', own, problems)
        self.assertTrue(any('unrecognised' in p for p in problems))
        with self.assertRaises(ValueError):
            inherited(source)

    def test_conditional_words_and_rows_survive_but_execution_refuses(self):
        source = fixture()
        original = copy.deepcopy(source)
        merged = inherited(source)
        self.assertEqual(source, original)
        self.assertNotIn('proper_appointment_facts', merged)
        raw = C.mass_index(merged)[COMMON]['propers'][0]
        self.assertNotIn('appointment_applicability', raw)
        self.assertEqual(getattr(raw, 'appointment_applicability'), MARKER)
        rows = public_rows(merged)
        self.assertEqual(rows[0][1]['appointment_applicability'], MARKER)
        self.assertEqual(rows[0][1]['text'], original['sections']['common']['masses'][0]['propers'][0]['text'])
        self.assertNotIn('text_status', rows[0][1])
        self.assertNotIn('ordinary_disposition', rows[0][1])
        with self.assertRaisesRegex(TODAY.Refused, 'applicability'):
            runtime(rows)

    def test_anchor_only_keeps_valid_legacy_fields_diagnostically_but_still_refuses(self):
        rows = public_rows(inherited(fixture('anchor')))
        for _, row, _ in rows:
            self.assertEqual(set(row['ordinary_disposition']), {'kind', 'group', 'option', 'basis'})
            self.assertEqual(row['appointment_applicability'], MARKER)
        with self.assertRaisesRegex(TODAY.Refused, 'applicability'):
            runtime(rows, choices={'main/gospel': 'principal'})

    def test_noncontiguous_group_strips_only_invalid_presentation_and_marks_all_members(self):
        source = fixture('anchor', separated=True)
        before = copy.deepcopy(source)
        rows = public_rows(inherited(source))
        self.assertEqual(source, before)
        self.assertEqual(len(rows), 3)
        for index in (0, 2):
            self.assertNotIn('ordinary_disposition', rows[index][1])
            self.assertEqual(rows[index][1]['appointment_applicability'], MARKER)
        self.assertNotIn('appointment_applicability', rows[1][1])
        self.assertEqual([p['text'] for _, p, _ in rows], [p['text'] for p in C.mass_index(before)[COMMON]['propers']])

    def test_old_four_field_legacy_group_remains_unmarked_and_exclusive(self):
        source = fixture('legacy')
        merged = inherited(source)
        self.assertEqual(C.mass_index(merged)[COMMON]['propers'], C.mass_index(source)[COMMON]['propers'])
        rows = public_rows(merged)
        self.assertTrue(all('appointment_applicability' not in p for _, p, _ in rows))
        result = runtime(rows, choices={'main/gospel': 'principal'})
        choices = [e for e in result['events'] if e['kind'] == 'proper_choice']
        self.assertEqual(len(choices), 1)
        self.assertEqual(choices[0]['selection']['option'], 'principal')

    def test_multi_hop_rebinds_target_without_relabeling_source_or_basis(self):
        source = fixture('when')
        first = inherited(source)
        target = {'calendar': 'roman-earlier-fixture', 'sections': {}}
        second = C._apply_departures(target, first, TARGET)
        expected = {**MARKER, 'target_edition': 'roman-earlier-fixture'}
        rows = public_rows(second)
        self.assertEqual(len(rows), 2)
        for _, proper, _ in rows:
            self.assertEqual(proper['appointment_applicability'], expected)
        self.assertEqual(C.mass_index(second)[COMMON][C.RECENSION]['calendar'], SOURCE)
        with self.assertRaisesRegex(TODAY.Refused, 'applicability'):
            runtime(rows, 'roman-earlier-fixture')
        with self.assertRaises(TODAY.Refused):
            runtime(rows, TARGET)

    def test_wording_reference_keeps_wrapper_marker_and_terminal_body_owner(self):
        source = fixture()
        mass = C.mass_index(source)[COMMON]
        words = {'key': 'fixture-words', 'propers': [body('Gradual')]}
        source['sections']['common']['masses'].append(words)
        annotation = mass['propers'][0]['ordinary_disposition']
        mass['propers'] = [{'name': 'Gradual', 'takes_from': {'mass': 'fixture-words', 'proper': 'Gradual'}, 'ordinary_disposition': annotation}]
        merged = inherited(source)
        rows = public_rows(merged)
        self.assertEqual(rows[0][1]['appointment_applicability'], MARKER)
        self.assertEqual(rows[0][2]['mass'], 'fixture-words')
        # An independently target-authored wording wrapper owns its own
        # appointment; borrowing foreign words cannot import target rules.
        local = {'key': 'fixture-target-wrapper', 'propers': [{'name': 'Gradual', 'takes_from': {'mass': COMMON, 'proper': 'Gradual'}}]}
        merged['sections']['common']['masses'].append(local)
        own = public_rows(merged, local['key'])
        self.assertNotIn('appointment_applicability', own[0][1])
        self.assertEqual(own[0][2]['mass'], 'fixture-words')

    def test_derived_repeated_terminal_owners_keep_distinct_occurrences(self):
        source = fixture()
        mass = C.mass_index(source)[COMMON]
        second = copy.deepcopy(mass['propers'][0])
        second['ordinary_disposition']['group'] = 'another-gradual'
        second['text'] = 'Second technical held body.'
        mass['propers'].append(second)
        merged = inherited(source)
        rows = public_rows(merged)
        self.assertEqual([MP.source_slot_identity(merged, C.mass_index(merged)[COMMON], form, proper, origin)[3]
                          for form, proper, origin in rows], [1, 2])

    def test_foreign_explicit_replacement_members_retain_their_own_unsupported_basis(self):
        source = fixture('anchor')
        own_key = 'fixture-own-replacement'
        override_basis = 'Technical exact source replacement permission; no foreign appointment claim.'
        override = {'mass': COMMON, 'form_id': 'main', 'group': 'gospel', 'state': 'replaced',
                    'by': [{'mass': own_key, 'form_id': 'main', 'proper': 'Gospel', 'occurrence': 1}],
                    'basis': override_basis}
        local = {'key': own_key, 'propers': [body('Gospel')],
                 'takes_from': {'mass': COMMON, 'appointment_overrides': [override]}}
        source['sections']['common']['masses'].append(local)
        self.assertEqual(C.resolve_propers(source, local)[1], [])
        merged = inherited(source)
        raw = C.mass_index(merged)[own_key]
        self.assertNotIn('appointment_overrides', raw['takes_from'])
        self.assertEqual(getattr(raw['propers'][0], 'appointment_applicability')['basis'], override_basis)
        rows = public_rows(merged, own_key)
        local_row = next(p for _, p, origin in rows if origin is None)
        self.assertEqual(local_row['text'], local['propers'][0]['text'])
        self.assertEqual(local_row['appointment_applicability']['basis'], override_basis)
        with self.assertRaisesRegex(TODAY.Refused, 'applicability'):
            runtime(rows)

    def test_producer_transports_marker_without_changing_body_publication_policy(self):
        source = fixture()
        merged = inherited(source)
        mass = C.mass_index(merged)[COMMON]
        with patch.object(MP, 'load_calendar', return_value=merged), patch.object(MP, 'masses_of', return_value=[('common', mass)]), \
             patch.object(MP, 'translation_overlay', return_value=({}, {}, [], {})), patch.object(MP, 'publication_records', return_value=({}, [])), \
             patch.object(MP._oration_execution, 'load_sources', return_value={}), \
             patch.object(MP._name_execution, 'load_name_sources', return_value={}):
            structure = MP.calendar_structure(H.ROOT / 'src/sources/calendars', TARGET, MP.book_tokens())
        row = structure['masses'][0]['propers'][0]
        self.assertEqual(row['appointment_applicability'], MARKER)
        original_mass = C.mass_index(source)[COMMON]
        with patch.object(MP, 'load_calendar', return_value=source), patch.object(MP, 'masses_of', return_value=[('common', original_mass)]), \
             patch.object(MP, 'translation_overlay', return_value=({}, {}, [], {})), patch.object(MP, 'publication_records', return_value=({}, [])), \
             patch.object(MP._oration_execution, 'load_sources', return_value={}), \
             patch.object(MP._name_execution, 'load_name_sources', return_value={}):
            original = MP.calendar_structure(H.ROOT / 'src/sources/calendars', SOURCE, MP.book_tokens())['masses'][0]['propers'][0]
        self.assertEqual(row['text'], original['text'])
        self.assertEqual(row.get('text_status'), original.get('text_status'))
        encoded = json.dumps(structure)
        self.assertNotIn('"source_proper":', encoded)
        self.assertNotIn('"_appointment_applicability":', encoded)


if __name__ == '__main__':
    unittest.main()
