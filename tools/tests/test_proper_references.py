"""A mass may say where its text is printed instead of retyping it.

The books say it constantly and this schema could not. A fourth-class feria
takes the preceding Sunday's Mass; a resumed Sunday after the Epiphany takes
that Sunday's orations under the twenty-third Sunday after Pentecost's chants;
a third-class saint takes a whole Mass from the Commune Sanctorum and supplies
only a Collect. With no way to say any of it, the only way to carry such a day
was to retype the text beside itself.

The copies drift, and this repository can show it rather than assert it. Before
`takes_from` existed, `resumed-epiphany-3` through `-6` held the four Epiphany
Sundays' orations a second time and the twenty-third Sunday's chants a second
time, and the two copies had already disagreed in five ways: `caelestis`
against `coelestis`, `Caelestibus` against `Coelestibus`, `caelestibus` against
`coelestibus`, `Jeremiah 29:11-12, 14` encoded as one contiguous range against
`29:11, 12, 14` encoded as three, and a dozen incipits truncated differently.
Nothing compared them.

So the rules held here are the ones that make a reference safe to trust: it
lands on a mass this calendar actually has, it lands on a proper that mass
actually appoints, it never closes a cycle, and the borrowed proper is the
referenced object rather than a copy of it. The last is what the whole key is
for: `resolve_propers` returns the target's own mapping, so a correction to the
Common corrects every saint that takes it, in one edit, with nothing left
beside it to fall out of step.
"""

from __future__ import annotations

import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _calendars  # noqa: E402


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


checker = load_tool("check-calendar-masses")


def composed(name: str, text: str) -> dict:
    return {"name": name, "source": "composed", "text": text}


def document(masses: list[dict]) -> dict:
    return {"sections": {"seasonal": {"kind": "seasonal", "masses": masses}}}


def names(entries) -> list[str]:
    return [str(proper.get("name")) for _, proper, _ in entries]


class ResolveProper(unittest.TestCase):
    def test_a_mass_without_a_reference_is_unchanged(self):
        mass = {"key": "advent-1", "propers": [composed("Collect", "Excita")]}
        entries, problems = _calendars.resolve_propers(document([mass]), mass)
        self.assertEqual(problems, [])
        self.assertEqual(names(entries), ["Collect"])
        self.assertIsNone(entries[0][2])

    def test_a_mass_takes_a_whole_formulary(self):
        source = {"key": "advent-2", "propers": [composed("Collect", "Excita corda")]}
        feria = {"key": "advent-2-monday", "takes_from": {"mass": "advent-2"}}
        entries, problems = _calendars.resolve_propers(document([source, feria]), feria)
        self.assertEqual(problems, [])
        self.assertEqual(names(entries), ["Collect"])
        # The borrowed proper is the referenced object, not a copy of it.
        self.assertIs(entries[0][1], source["propers"][0])
        self.assertEqual(entries[0][2]["mass"], "advent-2")

    def test_a_local_proper_replaces_the_borrowed_one_by_name(self):
        common = {
            "key": "commune-doctorum",
            "propers": [
                composed("Collect", "In medio"),
                composed("Secret", "Sancti tui"),
            ],
        }
        saint = {
            "key": "s-hilarii",
            "takes_from": {"mass": "commune-doctorum", "citation": "[22]"},
            "propers": [composed("Collect", "Deus, qui populo tuo")],
        }
        entries, problems = _calendars.resolve_propers(document([common, saint]), saint)
        self.assertEqual(problems, [])
        self.assertEqual(names(entries), ["Collect", "Secret"])
        # The saint's own Collect wins and is not marked as borrowed; the
        # Common's Secret is carried through in the Common's own order.
        self.assertEqual(entries[0][1]["text"], "Deus, qui populo tuo")
        self.assertIsNone(entries[0][2])
        self.assertEqual(entries[1][2]["mass"], "commune-doctorum")
        self.assertEqual(entries[1][2]["citation"], "[22]")

    def test_a_local_proper_the_common_lacks_is_appended_not_dropped(self):
        common = {"key": "commune", "propers": [composed("Collect", "N.")]}
        saint = {
            "key": "saint",
            "takes_from": {"mass": "commune"},
            "propers": [composed("Sequence", "Stabat Mater")],
        }
        entries, _ = _calendars.resolve_propers(document([common, saint]), saint)
        self.assertEqual(names(entries), ["Collect", "Sequence"])

    def test_one_proper_may_be_taken_on_its_own(self):
        sunday = {
            "key": "pentecost-23",
            "propers": [
                {"name": "Gradual", "source": "scripture", "verses": [{"book": "Psalms"}]}
            ],
        }
        resumed = {
            "key": "resumed-epiphany-3",
            "propers": [
                composed("Collect", "Omnipotens"),
                {"name": "Gradual", "takes_from": {"mass": "pentecost-23"}},
            ],
        }
        entries, problems = _calendars.resolve_propers(
            document([sunday, resumed]), resumed
        )
        self.assertEqual(problems, [])
        self.assertEqual(names(entries), ["Collect", "Gradual"])
        self.assertIs(entries[1][1], sunday["propers"][0])
        self.assertEqual(entries[1][2]["mass"], "pentecost-23")

    def test_a_proper_may_take_a_differently_named_slot(self):
        sunday = {"key": "easter", "propers": [composed("Sequence", "Victimae")]}
        octave = {
            "key": "easter-monday",
            "propers": [
                {"name": "Sequence", "takes_from": {"mass": "easter", "proper": "Sequence"}}
            ],
        }
        entries, problems = _calendars.resolve_propers(
            document([sunday, octave]), octave
        )
        self.assertEqual(problems, [])
        self.assertEqual(entries[0][1]["text"], "Victimae")

    def test_a_reference_may_name_one_form_of_a_mass_printed_in_forms(self):
        vigil = {
            "key": "pentecost",
            "forms": [
                {"name": "Vigil Mass", "propers": [composed("Collect", "Vigil")]},
                {"name": "Day Mass", "propers": [composed("Collect", "Day")]},
            ],
        }
        borrower = {
            "key": "whit-monday",
            "takes_from": {"mass": "pentecost", "form": "Day Mass"},
        }
        entries, problems = _calendars.resolve_propers(
            document([vigil, borrower]), borrower
        )
        self.assertEqual(problems, [])
        self.assertEqual(entries[0][1]["text"], "Day")

    def test_a_reference_into_a_mass_of_forms_must_say_which(self):
        vigil = {
            "key": "pentecost",
            "forms": [
                {"name": "Vigil Mass", "propers": [composed("Collect", "Vigil")]},
                {"name": "Day Mass", "propers": [composed("Collect", "Day")]},
            ],
        }
        borrower = {"key": "whit-monday", "takes_from": {"mass": "pentecost"}}
        _, problems = _calendars.resolve_propers(document([vigil, borrower]), borrower)
        self.assertEqual(len(problems), 1)
        self.assertIn("without saying which", problems[0])

    def test_a_chain_of_references_resolves(self):
        first = {"key": "a", "propers": [composed("Collect", "one")]}
        second = {"key": "b", "takes_from": {"mass": "a"}}
        third = {"key": "c", "takes_from": {"mass": "b"}}
        entries, problems = _calendars.resolve_propers(
            document([first, second, third]), third
        )
        self.assertEqual(problems, [])
        self.assertEqual(entries[0][1]["text"], "one")


class RefuseProper(unittest.TestCase):
    def test_a_missing_target_is_reported(self):
        mass = {"key": "saint", "takes_from": {"mass": "commune-nowhere"}}
        _, problems = _calendars.resolve_propers(document([mass]), mass)
        self.assertEqual(len(problems), 1)
        self.assertIn("no entry for", problems[0])

    def test_a_missing_proper_is_reported(self):
        common = {"key": "commune", "propers": [composed("Collect", "N.")]}
        borrower = {
            "key": "saint",
            "propers": [{"name": "Tract", "takes_from": {"mass": "commune"}}],
        }
        _, problems = _calendars.resolve_propers(
            document([common, borrower]), borrower
        )
        self.assertEqual(len(problems), 1)
        self.assertIn("appoints no such proper", problems[0])

    def test_a_mass_may_not_point_at_itself(self):
        mass = {"key": "loop", "takes_from": {"mass": "loop"}}
        _, problems = _calendars.resolve_propers(document([mass]), mass)
        self.assertEqual(len(problems), 1)
        self.assertIn("points at itself", problems[0])

    def test_a_cycle_is_refused_rather_than_recursed(self):
        first = {"key": "a", "takes_from": {"mass": "b"}}
        second = {"key": "b", "takes_from": {"mass": "a"}}
        _, problems = _calendars.resolve_propers(document([first, second]), first)
        self.assertEqual(len(problems), 1)
        self.assertIn("closes a cycle", problems[0])


class ValidateProper(unittest.TestCase):
    def check(self, entry: dict) -> list[str]:
        problems: list[str] = []
        checker.check_entry(entry, 0, problems)
        return problems

    def test_a_mass_with_a_reference_needs_no_propers(self):
        self.assertEqual(
            self.check(
                {
                    "key": "feria",
                    "name": "Feria",
                    "registry": "x",
                    "season": "advent",
                    "takes_from": {"mass": "advent-2"},
                }
            ),
            [],
        )

    def test_a_mass_with_a_reference_may_carry_propers(self):
        self.assertEqual(
            self.check(
                {
                    "key": "saint",
                    "name": "Saint",
                    "registry": "x",
                    "date": "01-14",
                    "kind": "sanctoral",
                    "rank": "III",
                    "takes_from": {"mass": "commune-doctorum"},
                    "propers": [composed("Collect", "Deus")],
                }
            ),
            [],
        )

    def test_a_mass_with_a_reference_may_not_carry_forms(self):
        problems = self.check(
            {
                "key": "saint",
                "name": "Saint",
                "registry": "x",
                "season": "advent",
                "takes_from": {"mass": "commune"},
                "forms": [{"name": "One", "propers": [composed("Collect", "a")]}],
            }
        )
        self.assertTrue(any("must not also carry forms" in p for p in problems))

    def test_a_mass_with_neither_is_still_refused(self):
        problems = self.check(
            {"key": "empty", "name": "Empty", "registry": "x", "season": "advent"}
        )
        self.assertTrue(
            any("exactly one of propers, forms or takes_from" in p for p in problems)
        )

    def test_a_reference_needs_a_mass_key(self):
        problems = self.check(
            {
                "key": "feria",
                "name": "Feria",
                "registry": "x",
                "season": "advent",
                "takes_from": {"citation": "[4]"},
            }
        )
        self.assertTrue(any("needs the key of the mass" in p for p in problems))

    def test_an_unknown_reference_field_is_refused(self):
        problems = self.check(
            {
                "key": "feria",
                "name": "Feria",
                "registry": "x",
                "season": "advent",
                "takes_from": {"mass": "advent-2", "page": 4},
            }
        )
        self.assertTrue(any("unknown field(s) page" in p for p in problems))

    def test_a_mass_reference_may_not_name_a_single_proper(self):
        problems = self.check(
            {
                "key": "feria",
                "name": "Feria",
                "registry": "x",
                "season": "advent",
                "takes_from": {"mass": "advent-2", "proper": "Collect"},
            }
        )
        self.assertTrue(any("takes the whole formulary" in p for p in problems))

    def test_a_referring_proper_may_not_restate_the_text(self):
        problems = self.check(
            {
                "key": "octave",
                "name": "Octave",
                "registry": "x",
                "season": "easter",
                "propers": [
                    {
                        "name": "Sequence",
                        "takes_from": {"mass": "easter-sunday"},
                        "source": "composed",
                        "text": "Victimae paschali laudes",
                        "incipit": "Victimae",
                    }
                ],
            }
        )
        self.assertTrue(
            any("must not also carry source, text, incipit" in p for p in problems)
        )

    def test_a_referring_proper_needs_nothing_else(self):
        self.assertEqual(
            self.check(
                {
                    "key": "octave",
                    "name": "Octave",
                    "registry": "x",
                    "season": "easter",
                    "propers": [
                        {"name": "Sequence", "takes_from": {"mass": "easter-sunday"}}
                    ],
                }
            ),
            [],
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
