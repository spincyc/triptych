"""The normal feast cannot execute the source's separate votive-only Tract."""

from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from _calendars import resolve_propers

# Independently enumerated from the registered CMAA page images. The numbered
# Tracts are excluded by each page's explicit votive-after-Septuagesima rubric.
SOURCE_NORMAL_UNITS = {
    's-matthaei-apostoli-evangelistae': (
        ('Introit', 3679), ('Collect', 3680), ('Lesson', 3681),
        ('Gradual', 3682), ('Alleluia', 3683), ('Gospel', 3684),
        ('Offertory', 3685), ('Secret', 3686), ('Communion', 3687),
        ('Postcommunion', 3688),
    ),
    's-teresiae-a-iesu-infante-virginis': (
        ('Introit', 3757), ('Collect', 3758), ('Lesson', 3759),
        ('Gradual', 3760), ('Alleluia', 3761), ('Gospel', 3764),
        ('Offertory', 3765), ('Secret', 3766), ('Communion', 3767),
        ('Postcommunion', 3768),
    ),
}
SOURCE_VOTIVE_TRACTS = {
    # Artifact p. 746 / printed p. 665, no. 3689.
    's-matthaei-apostoli-evangelistae': {
        'name': 'Tract', 'source': 'scripture',
        'verses': [{'book': 'Psalms', 'ranges': [
            {'begin': {'chapter': 20, 'verse': 3},
             'end': {'chapter': 20, 'verse': 4}}], 'ref': 'Psalms 20:3-4'}],
    },
    # Artifact p. 755 / printed p. 674, no. 3762. The source prints both loci.
    's-teresiae-a-iesu-infante-virginis': {
        'name': 'Tract', 'source': 'scripture',
        'verses': [
            {'book': 'Song of Songs', 'ranges': [
                {'begin': {'chapter': 2, 'verse': 11},
                 'end': {'chapter': 2, 'verse': 12}}], 'ref': 'Song of Songs 2:11-12'},
            {'book': 'Jeremiah', 'ranges': [
                {'begin': {'chapter': 31, 'verse': 3},
                 'end': {'chapter': 31, 'verse': 3}}], 'ref': 'Jeremiah 31:3'},
        ],
    },
}


def mass_by_key(document, key):
    return next(mass for section in document['sections'].values()
                for mass in section['masses'] if mass['key'] == key)


class VotiveOnlyChantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(
            (ROOT / 'src/sources/calendars/roman-1962/propers.yaml').read_text())

    def assert_source_normal_order(self, document, key):
        entries, problems = resolve_propers(document, mass_by_key(document, key))
        self.assertEqual(problems, [])
        self.assertEqual([proper['name'] for _, proper, _ in entries],
                         [name for name, _ in SOURCE_NORMAL_UNITS[key]])
        self.assertTrue(all(origin is None for _, _, origin in entries))

    def test_normal_feasts_follow_their_complete_printed_unit_order(self):
        for key in SOURCE_NORMAL_UNITS:
            with self.subTest(mass=key):
                self.assert_source_normal_order(self.document, key)

    def test_reinserting_a_votive_tract_breaks_the_normal_source_order(self):
        for key, tract in SOURCE_VOTIVE_TRACTS.items():
            with self.subTest(mass=key):
                altered = copy.deepcopy(self.document)
                mass = mass_by_key(altered, key)
                at = next(i for i, proper in enumerate(mass['propers'])
                          if proper['name'] == 'Gradual') + 1
                mass['propers'].insert(at, copy.deepcopy(tract))
                with self.assertRaises(AssertionError):
                    self.assert_source_normal_order(altered, key)


if __name__ == '__main__':
    unittest.main()
