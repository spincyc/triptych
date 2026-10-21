"""July/August 1962 normal appointments, collated to numbered source units.

Expected citation constituents and unit/page addresses below come from the
held 1962 Missal page collation recorded in the chant appointment inventory.
These tests retain appointments and exact English whole-body identities;
they make no word-collation claim. Common primary-reading eligibility remains
with its owner: no reading choice or full Common execution is asserted here.
"""
from __future__ import annotations

from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
import sys
import tomllib
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _calendars import mass_index, resolve_propers


def tool(name):
    loader = SourceFileLoader("_jul_aug_source_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


# (Mass, Proper, artifact page, marginal unit, printed citation constituents).
PRINTED_CITATIONS = [('immaculati-cordis-beatae-mariae-virginis', 'Gradual', 714, 3427, ('Psalms 12:6', 'Psalms 44:18')),
 ('immaculati-cordis-beatae-mariae-virginis', 'Offertory', 715, 3432, ('Luke 1:47, 49',)),
 ('s-apollinaris-episcopi-martyris', 'Introit', 679, 3143, ('Daniel 3:84, 87', 'Daniel 3:57')),
 ('s-bernardi-abbatis-ecclesiae-doctoris', 'Offertory', 713, 3416, ('Psalms 91:13',)),
 ('s-caietani-confessoris', 'Gradual', 697, 3286, ('Psalms 91:13-14', 'Psalms 91:3')),
 ('s-caietani-confessoris', 'Alleluia', 697, 3287, ('James 1:12',)),
 ('s-camilli-lellis-confessoris', 'Alleluia', 671, 3082, ('Psalms 111:1',)),
 ('s-dominici-confessoris', 'Gradual', 694, 3262, ('Psalms 91:13-14', 'Psalms 91:3')),
 ('s-ignatii-confessoris', 'Introit', 689, 3224, ('Philippians 2:10-11', 'Psalms 5:12-13')),
 ('s-ignatii-confessoris', 'Gradual', 689, 3227, ('Psalms 91:13-14', 'Psalms 91:3')),
 ('s-ignatii-confessoris', 'Alleluia', 689, 3228, ('James 1:12',)),
 ('s-iosephi-calasanctii-confessoris', 'Alleluia', 720, 3472, ('James 1:12',)),
 ('s-irenaei-episcopi-martyris', 'Gradual', 659, 2975, ('Psalms 121:8', 'Psalms 36:37')),
 ('s-ludovici-regis-confessoris', 'Gradual', 718, 3458, ('Psalms 91:13-14', 'Psalms 91:3')),
 ('s-ludovici-regis-confessoris', 'Alleluia', 718, 3459, ('James 1:12',)),
 ('s-mariae-magdalenae-paenitentis', 'Alleluia', 678, 3137, ('Psalms 44:3',)),
 ('s-marthae-virginis', 'Alleluia', 686, 3203, ('Psalms 44:15-16',)),
 ('s-marthae-virginis', 'Communion', 687, 3208, ('Matthew 25:4, 6',)),
 ('ss-nazarii-celsi-martyrum-victoris-i', 'Gradual', 685, 3191, ('Exodus 15:11', 'Exodus 15:6'))]

# (Mass, own Proper, source kind, artifact page, marginal unit).
OWN_BODY_IDENTITIES = [('assumptione-beatae-mariae-virginis', 'Alleluia', 'composed', 709, 3382),
 ('s-ioannae-franciscae-fremiot-chantal-viduae', 'Postcommunion', 'composed', 714, 3422),
 ('s-ioannae-franciscae-fremiot-chantal-viduae', 'Secret', 'composed', 713, 3421),
 ('s-laurentii-brundusio-confessoris-ecclesiae-doctoris', 'Collect', 'composed', 675, 3117),
 ('ss-septem-fratrum-martyrum-ac-ss', 'Alleluia', 'composed', 664, 3015),
 ('vigil-assumption', 'Communion', 'composed', 707, 3374),
 ('vigil-assumption', 'Gradual', 'composed', 706, 3369),
 ('vigil-assumption', 'Offertory', 'composed', 706, 3371),
 ('visitatione-beatae-mariae-virginis', 'Alleluia', 'composed', 656, 2954),
 ('visitatione-beatae-mariae-virginis', 'Communion', 'composed', 657, 2959),
 ('visitatione-beatae-mariae-virginis', 'Gradual', 'composed', 656, 2953),
 ('visitatione-beatae-mariae-virginis', 'Introit', 'mixed', 655, 2949),
 ('visitatione-beatae-mariae-virginis', 'Offertory', 'composed', 656, 2956)]

VOTIVE_ONLY_NORMAL_MEMBERS = [('immaculati-cordis-beatae-mariae-virginis', 'Tract'),
 ('pretiosissimi-sanguinis-domini-nostri-iesu-christi', 'Tract'),
 ('pretiosissimi-sanguinis-domini-nostri-iesu-christi', 'Greater Alleluia'),
 ('s-irenaei-episcopi-martyris', 'Tract')]

# Nonprimary order at the repaired directly printed normal forms. Primary
# Common reading pools are deliberately not flattened into this sequence.
NORMAL_NONPRIMARY_ORDER = {'assumptione-beatae-mariae-virginis': ['Introit',
                                        'Collect',
                                        'Gradual',
                                        'Alleluia',
                                        'Offertory',
                                        'Secret',
                                        'Communion',
                                        'Postcommunion'],
 'immaculati-cordis-beatae-mariae-virginis': ['Introit',
                                              'Collect',
                                              'Gradual',
                                              'Alleluia',
                                              'Offertory',
                                              'Secret',
                                              'Communion',
                                              'Postcommunion'],
 'pretiosissimi-sanguinis-domini-nostri-iesu-christi': ['Introit',
                                                        'Collect',
                                                        'Gradual',
                                                        'Alleluia',
                                                        'Offertory',
                                                        'Secret',
                                                        'Communion',
                                                        'Postcommunion'],
 's-apollinaris-episcopi-martyris': ['Introit',
                                     'Collect',
                                     'Gradual',
                                     'Alleluia',
                                     'Offertory',
                                     'Secret',
                                     'Communion',
                                     'Postcommunion'],
 's-bernardi-abbatis-ecclesiae-doctoris': ['Introit',
                                           'Collect',
                                           'Gradual',
                                           'Alleluia',
                                           'Offertory',
                                           'Secret',
                                           'Communion',
                                           'Postcommunion'],
 's-caietani-confessoris': ['Introit',
                            'Collect',
                            'Gradual',
                            'Alleluia',
                            'Offertory',
                            'Secret',
                            'Communion',
                            'Postcommunion'],
 's-camilli-lellis-confessoris': ['Introit',
                                  'Collect',
                                  'Gradual',
                                  'Alleluia',
                                  'Offertory',
                                  'Secret',
                                  'Communion',
                                  'Postcommunion'],
 's-dominici-confessoris': ['Introit',
                            'Collect',
                            'Gradual',
                            'Alleluia',
                            'Offertory',
                            'Secret',
                            'Communion',
                            'Postcommunion'],
 's-ignatii-confessoris': ['Introit',
                           'Collect',
                           'Gradual',
                           'Alleluia',
                           'Offertory',
                           'Secret',
                           'Communion',
                           'Postcommunion'],
 's-iosephi-calasanctii-confessoris': ['Introit',
                                       'Collect',
                                       'Gradual',
                                       'Alleluia',
                                       'Offertory',
                                       'Secret',
                                       'Communion',
                                       'Postcommunion'],
 's-irenaei-episcopi-martyris': ['Introit',
                                 'Collect',
                                 'Gradual',
                                 'Alleluia',
                                 'Offertory',
                                 'Secret',
                                 'Communion',
                                 'Postcommunion'],
 's-ludovici-regis-confessoris': ['Introit',
                                  'Collect',
                                  'Gradual',
                                  'Alleluia',
                                  'Offertory',
                                  'Secret',
                                  'Communion',
                                  'Postcommunion'],
 's-mariae-magdalenae-paenitentis': ['Introit',
                                     'Collect',
                                     'Gradual',
                                     'Alleluia',
                                     'Offertory',
                                     'Secret',
                                     'Communion',
                                     'Postcommunion'],
 's-marthae-virginis': ['Introit',
                        'Collect',
                        'Gradual',
                        'Alleluia',
                        'Offertory',
                        'Secret',
                        'Communion',
                        'Postcommunion'],
 'ss-nazarii-celsi-martyrum-victoris-i': ['Introit',
                                          'Collect',
                                          'Gradual',
                                          'Alleluia',
                                          'Offertory',
                                          'Secret',
                                          'Communion',
                                          'Postcommunion'],
 'ss-septem-fratrum-martyrum-ac-ss': ['Introit',
                                      'Collect',
                                      'Gradual',
                                      'Alleluia',
                                      'Offertory',
                                      'Secret',
                                      'Communion',
                                      'Postcommunion'],
 'vigil-assumption': ['Introit', 'Collect', 'Gradual', 'Offertory', 'Secret', 'Communion', 'Postcommunion'],
 'visitatione-beatae-mariae-virginis': ['Introit',
                                        'Collect',
                                        'Gradual',
                                        'Alleluia',
                                        'Offertory',
                                        'Secret',
                                        'Communion',
                                        'Postcommunion']}


class JulyAugustSourceAppointments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load((ROOT / "src/sources/calendars/roman-1962/propers.yaml").read_text())
        cls.masses = mass_index(cls.document)
        cls.english = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml").read_text())
        cls.citations = tool("citations")
        cls.validator = tool("check-calendar-masses")

    def own(self, key, name):
        found = [p for p in self.masses[key].get("propers", []) if p["name"] == name]
        self.assertEqual(len(found), 1, f"{key}/{name}: exact own appointment")
        return found[0]

    def resolved(self, key):
        entries, problems = resolve_propers(self.document, self.masses[key])
        self.assertEqual(problems, [], key)
        return entries

    @staticmethod
    def numerical(entries):
        # Canonical ranges carry the address; a display ref cannot supply a
        # constituent absent from the actual ranges.
        return [(entry["book"], entry["ranges"]) for entry in entries]

    def test_all_printed_citation_constituents_survive(self):
        for key, name, page, unit, refs in PRINTED_CITATIONS:
            with self.subTest(mass=key, proper=name, page=page, unit=unit):
                actual = self.own(key, name)
                expected = [self.citations.parse_citation(ref) for ref in refs]
                self.assertEqual(self.numerical(actual["verses"]), self.numerical(expected))
                problems = []
                self.validator.check_proper(key, actual, problems, calendar="roman-1962")
                self.assertEqual(problems, [])

    def test_normal_appointments_keep_the_printed_nonprimary_order(self):
        for key, expected in NORMAL_NONPRIMARY_ORDER.items():
            with self.subTest(mass=key):
                names = [proper["name"] for _, proper, _ in self.resolved(key)
                         if proper["name"] not in {"Lesson", "Epistle", "Gospel"}]
                self.assertEqual(names, expected)

    def test_votive_members_do_not_execute_in_the_normal_form(self):
        for key, name in VOTIVE_ONLY_NORMAL_MEMBERS:
            with self.subTest(mass=key, proper=name):
                self.assertNotIn(name, [p["name"] for p in self.masses[key]["propers"]])
                self.assertNotIn(name, [p["name"] for _, p, _ in self.resolved(key)])

    def test_uncited_chants_and_own_orations_keep_real_body_identities(self):
        for key, name, kind, page, unit in OWN_BODY_IDENTITIES:
            with self.subTest(mass=key, proper=name, page=page, unit=unit):
                proper = self.own(key, name)
                self.assertEqual(proper["source"], kind)
                if not proper.get("text"):
                    status = proper.get("text_status", {})
                    self.assertEqual(status.get("state"), "unavailable")
                    self.assertEqual(status.get("scope"), "proper-body")
                    self.assertTrue(status.get("reasons"))
                problems = []
                self.validator.check_proper(key, proper, problems, calendar="roman-1962")
                self.assertEqual(problems, [])

    def test_visitation_psalm_companion_is_not_the_whole_introit(self):
        proper = self.own("visitatione-beatae-mariae-virginis", "Introit")
        self.assertEqual(proper["source"], "mixed")
        self.assertEqual(self.numerical(proper["verses"]),
                         self.numerical([self.citations.parse_citation("Psalms 44:2")]))
        self.assertTrue(proper.get("text") or proper.get("text_status", {}).get("scope") == "proper-body")

    def test_laurence_retains_own_collect_and_nonbishop_common_prayers(self):
        key = "s-laurentii-brundusio-confessoris-ecclesiae-doctoris"
        mass = self.masses[key]
        self.assertEqual(mass["takes_from"]["mass"], "commune-doctorum-non-pontificis")
        self.assertNotIn("text_status", mass)
        collect = self.own(key, "Collect")
        if not collect.get("text"):
            self.assertIn("rights-withheld", [r["kind"] for r in collect["text_status"]["reasons"]])
        orations = {p["name"]: provenance for _, p, provenance in self.resolved(key)
                    if p["name"] in {"Collect", "Secret", "Postcommunion"}}
        self.assertIsNone(orations["Collect"])
        for name in ["Secret", "Postcommunion"]:
            self.assertEqual(orations[name]["mass"], "commune-doctorum-non-pontificis")

    def chantal_source_order_problems(self, document):
        key = "s-ioannae-franciscae-fremiot-chantal-viduae"
        mass = mass_index(document)[key]
        # Scope the actual checker to this source, retaining its real header.
        # Other Masses' independently owned exception entries are irrelevant.
        fixture = {**document, self.validator.ORDER_EXCEPTIONS: [
            row for row in document.get(self.validator.ORDER_EXCEPTIONS, [])
            if row.get("mass") == key]}
        with patch.object(self.validator, "read_yaml", return_value=fixture), \
             patch.object(self.validator, "iter_masses", return_value=[("sanctoral", mass)]):
            return self.validator.order_problems([
                ROOT / "src/sources/calendars/roman-1962/propers.yaml"])

    def test_chantal_secret_and_postcommunion_override_the_common(self):
        key = "s-ioannae-franciscae-fremiot-chantal-viduae"
        # AP713/p632 prints own Oratio3420 then Secreta3421; AP714/p633
        # continues Postcommunio3422. The heading appoints CommonII[37]
        # "cum orationibus ut infra". No Common reading option is selected here.
        mass = self.masses[key]
        self.assertEqual([p["name"] for p in mass["propers"]],
                         ["Collect", "Secret", "Postcommunion"])
        self.assertEqual(mass["takes_from"]["mass"], "commune-non-virginum-2")
        self.assertEqual(self.chantal_source_order_problems(self.document), [])
        entries = self.resolved(key)
        names = [p["name"] for _, p, _ in entries]
        self.assertLess(names.index("Offertory"), names.index("Secret"))
        self.assertLess(names.index("Secret"), names.index("Communion"))
        self.assertLess(names.index("Communion"), names.index("Postcommunion"))
        # Ordinary legacy local overrides use exact Common names as anchors.
        common = self.masses["commune-non-virginum-2"]
        base, problems = resolve_propers(self.document, common)
        self.assertEqual(problems, [])
        base_names = [p["name"] for _, p, _ in base]
        for name in ["Collect", "Secret", "Postcommunion"]:
            self.assertEqual(names.index(name), base_names.index(name))
        for name in ["Secret", "Postcommunion"]:
            self.own(key, name)
            matches = [provenance for _, p, provenance in entries if p["name"] == name]
            self.assertEqual(matches, [None], name)

    def test_chantal_secret_after_communion_is_still_rejected(self):
        document = deepcopy(self.document)
        mass = mass_index(document)["s-ioannae-franciscae-fremiot-chantal-viduae"]
        own = {proper["name"]: proper for proper in mass["propers"]}
        # This is an invalid source-order control, not another appointment:
        # borrow the actual Common Communion, then place the own Secret late.
        mass["propers"] = [own["Collect"], {
            "name": "Communion", "takes_from": {
                "mass": "commune-non-virginum-2", "proper": "Communion"}},
            own["Secret"], own["Postcommunion"]]
        problems = self.chantal_source_order_problems(document)
        self.assertTrue(any("Secret stands behind" in row for row in problems), problems)

    def test_exact_english_whole_body_identities_are_accounted(self):
        fields = {"form_id": "main", "cycle": "all", "occurrence": 1}
        for key, name, _, page, unit in OWN_BODY_IDENTITIES:
            with self.subTest(mass=key, proper=name, page=page, unit=unit):
                target = {"mass": key, "proper": name, **fields}
                matches = lambda row: all(row.get(field) == value for field, value in target.items())
                positive = [row for row in self.english.get("entries", []) if matches(row)
                            and any(t.get("lang") == "en" and t.get("extent", "body") == "body"
                                    and t.get("text") for t in row.get("translations", []))]
                absent = [row for row in self.english.get("untranslated", []) if matches(row)
                          and row.get("lang") == "en" and row.get("extent") == "body"]
                # A Common's English or a Psalm companion has a different
                # target/extent and cannot satisfy this own whole body.
                self.assertEqual(len(positive) + len(absent), 1)
                if absent:
                    self.assertEqual(absent[0]["availability"], "unavailable")
                    reason = absent[0]["reason"]["kind"]
                    self.assertIn(reason, {"no-exemplar", "rights-withheld"})
                    if reason == "rights-withheld":
                        self.assertTrue(absent[0].get("witness_artifact_id"))
                        self.assertTrue(absent[0].get("witness_passage_id"))


if __name__ == "__main__":
    unittest.main()
