"""Exact English dispositions for newly addressed 1962 Common chant bodies."""
from __future__ import annotations

import copy
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import unittest

ROOT = Path(os.environ.get('TRIPTYCH_REVIEW_ROOT', Path(__file__).resolve().parents[2]))
MODULE_ROOT = Path(os.environ.get('TRIPTYCH_COMMON_ENGLISH_OWNER_ROOT', ROOT))
DATA_ROOT = Path(os.environ.get('TRIPTYCH_COMMON_ENGLISH_DATA_ROOT', ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
loader = importlib.machinery.SourceFileLoader('_common_english_propers', str(MODULE_ROOT / 'tools/mass-propers'))
spec = importlib.util.spec_from_loader(loader.name, loader)
MP = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = MP
loader.exec_module(MP)
for key, value in list(vars(MP).items()):
    if isinstance(value, Path) and value.is_relative_to(MODULE_ROOT):
        setattr(MP, key, ROOT / value.relative_to(MODULE_ROOT))
MP.ROOT = ROOT
if DATA_ROOT != ROOT:
    # The scratch overlay retains registered payloads through symlinks. The
    # record scanner does not recurse those directories: bind its unchanged
    # graph input to the actual repository while retaining every validator.
    source_records = MP._source_library_records
    MP._source_library_records = lambda ignored: source_records(ROOT / 'src/sources/calendars')

EXPECTED = {
    ('commune-unius-martyris-2', 'main', 'Alleluia', 'all', 1): 'composed',
    ('commune-plurimorum-martyrum-3', 'main', 'Alleluia', 'all', 1): 'composed',
    ('commune-confessoris-pontificis-1', 'main', 'Alleluia (Tempore paschali)', 'all', 1): 'mixed',
    ('commune-non-virginum-1', 'main', 'Alleluia (Tempore paschali)', 'all', 1): 'mixed',
    ('commune-non-virginum-2', 'main', 'Alleluia (Tempore paschali)', 'all', 1): 'mixed',
}
# eeab39fef replaced these two no-exemplar absences with one confirmed Lasance
# entry each ([[accepted]] core39 in
# src/sources/inventories/roman-1962-english-recovery-2026-10-23.toml).
RECEIVED = {
    ('commune-unius-martyris-2', 'main', 'Alleluia', 'all', 1): 'lasance-1945',
    ('commune-plurimorum-martyrum-3', 'main', 'Alleluia', 'all', 1): 'lasance-1945',
}


def unaccounted(slots, overlay, untranslated):
    missing = []
    for identity, (proper, owner, legacy) in slots.items():
        entry = MP.translation_entry_for(overlay, legacy, identity) or {}
        absent = MP.matching_untranslated_records(
            proper, untranslated.get(MP.untranslated_key(identity)) or [],
            identity[4], cycle=identity[3], extent='body',
        )
        if not MP.translation_answers(entry, owner, 'en') and not absent:
            missing.append(identity)
    return sorted(missing)


class Roman1962CommonNewEnglishAbsencesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.calendar_root = DATA_ROOT / 'src/sources/calendars'
        cls.document = MP.load_calendar(cls.calendar_root, 'roman-1962')
        cls.overlay, cls.untranslated, _, _ = MP.translation_overlay('roman-1962', cls.calendar_root)
        owners = MP._calendars.mass_index(cls.document)
        cls.slots = {}
        cls.borrowers = set()
        for _, mass in MP.masses_of(cls.document):
            for form, proper, origin in MP.appointed_propers(cls.document, mass):
                identity = MP.source_slot_identity(cls.document, mass, form, proper, origin, owner_masses=owners)
                for exact, owner in MP.coverage_slot_units(proper, identity):
                    if exact not in EXPECTED:
                        continue
                    cls.slots[exact] = (proper, owner, MP.overlay_key(mass, form, proper, origin))
                    if mass['key'] != exact[0]:
                        cls.borrowers.add((mass['key'], exact))

    def test_five_slots_are_real_terminal_non_scripture_owners(self):
        self.assertEqual(set(self.slots), set(EXPECTED))
        self.assertTrue(self.borrowers)
        for identity, (proper, owner, legacy) in self.slots.items():
            with self.subTest(identity=identity):
                self.assertEqual(proper['source'], EXPECTED[identity])
                self.assertEqual(legacy, (identity[0], '', identity[2]))
                self.assertNotEqual(owner.get('source'), 'scripture')

    def test_each_whole_english_body_has_one_exact_disposition(self):
        for identity, (proper, owner, legacy) in self.slots.items():
            with self.subTest(identity=identity):
                records = MP.matching_untranslated_records(
                    proper, self.untranslated.get(MP.untranslated_key(identity)) or [],
                    identity[4], cycle=identity[3], extent='body',
                )
                if identity in RECEIVED:
                    entry = MP.translation_entry_for(self.overlay, legacy, identity) or {}
                    self.assertEqual(records, [])
                    self.assertTrue(MP.translation_answers(entry, owner, 'en'))
                    self.assertEqual((entry.get('witness'), entry.get('collation_result')),
                                     (RECEIVED[identity], 'confirmed'))
                    continue
                self.assertEqual(len(records), 1)
                record = records[0]
                self.assertEqual(MP.untranslated_record_identity(record), identity)
                self.assertEqual(record['lang'], 'en')
                self.assertEqual(record['extent'], 'body')
                self.assertEqual(record['availability'], 'unavailable')
                self.assertEqual(record['reason'], {'kind': 'no-exemplar'})
                self.assertFalse(MP.translation_answers(MP.translation_entry_for(self.overlay, legacy, identity) or {}, owner, 'en'))

    def test_new_slots_have_no_unaccounted_english_body(self):
        self.assertEqual(unaccounted(self.slots, self.overlay, self.untranslated), [])

    def test_losing_the_whole_4312_english_absence_is_detected(self):
        identity = ('commune-confessoris-pontificis-1', 'main', 'Alleluia (Tempore paschali)', 'all', 1)
        reduced = copy.deepcopy(self.untranslated)
        key = MP.untranslated_key(identity)
        reduced[key] = [r for r in reduced.get(key, []) if MP.untranslated_record_identity(r) != identity]
        self.assertEqual(unaccounted(self.slots, self.overlay, reduced), [identity])


if __name__ == '__main__':
    unittest.main()
