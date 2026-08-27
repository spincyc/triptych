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
actually appoints, and it never closes a cycle. A same-named borrowed proper is
the referenced object itself. A differently named wrapper is only a shallow
projection carrying its local display name; the target still owns all nested
content. In either case a correction to the Common corrects every saint that
takes it, in one edit, with nothing retyped beside it to fall out of step.
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


COMMON_SOURCE = (
    "artifact.catholic-church.missale-romanum.2010-english-icel-antiphonary."
    "antiphonary-pdf"
)
MISSAL_SOURCE = "edition.catholic-church.missale-romanum.vatican-typica-tertia-2002"


def common_from(target: str = "commune-martyrum") -> dict:
    return {
        "scope": "missal-propers-except-collect",
        "source_id": COMMON_SOURCE,
        "locus": "artifact page 112, printed page 104",
        "options": [{"mass": target, "selection": "For Several Martyrs"}],
    }


def text_status(scope: str) -> dict:
    return {
        "state": "unavailable",
        "scope": scope,
        "reasons": [{"kind": "rights-withheld", "source_id": MISSAL_SOURCE}],
    }


def partial_text_status() -> dict:
    return {
        "state": "partial",
        "scope": "missal-formulary",
        "reasons": [{"kind": "witness-gap", "source_id": MISSAL_SOURCE}],
    }


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

    def test_an_unavailable_proper_collect_is_excluded_from_a_borrowed_formulary(self):
        common = {
            "key": "commune-confessoris",
            "propers": [
                composed("Collect", "Deus"),
                composed("Collect (alternative)", "Deus alter"),
                composed("Secret", "Suscipe"),
                composed("Postcommunion", "Praesta"),
            ],
        }
        saint = {
            "key": "saint",
            "takes_from": {"mass": "commune-confessoris"},
            "text_status": text_status("proper-collect"),
        }
        entries, problems = _calendars.resolve_propers(
            document([common, saint]), saint
        )
        self.assertEqual(problems, [])
        self.assertEqual(names(entries), ["Secret", "Postcommunion"])
        self.assertEqual(
            [proper["text"] for _, proper, _ in entries],
            ["Suscipe", "Praesta"],
        )
        self.assertTrue(
            all(
                provenance and provenance["mass"] == common["key"]
                for _, _, provenance in entries
            )
        )

    def test_real_historical_collect_gaps_keep_the_rest_of_the_common(self):
        cases = {
            "s-gregorii-barbadici-episcopi-confessoris":
                "commune-confessoris-pontificis-1",
            "s-laurentii-brundusio-confessoris-ecclesiae-doctoris":
                "commune-doctorum-pontificis",
            "s-antonii-mariae-claret-episcopi-confessoris":
                "commune-confessoris-pontificis-2",
        }
        root = ROOT / "src/sources/calendars"
        for calendar_name in ("roman-1962", "roman-pre-1955"):
            calendar = _calendars.load_document(root, calendar_name)
            index = _calendars.mass_index(calendar)
            for key, target_key in cases.items():
                with self.subTest(calendar=calendar_name, mass=key):
                    target, target_problems = _calendars.resolve_propers(
                        calendar, index[target_key]
                    )
                    resolved, problems = _calendars.resolve_propers(
                        calendar, index[key]
                    )
                    self.assertEqual(target_problems, [])
                    self.assertEqual(problems, [])
                    self.assertEqual(
                        names(resolved),
                        [name for name in names(target) if name != "Collect"],
                    )
                    self.assertNotIn("Collect", names(resolved))
                    self.assertIn("Secret", names(resolved))
                    self.assertIn("Postcommunion", names(resolved))
                    self.assertTrue(
                        all(
                            provenance and provenance["mass"] == target_key
                            for _, _, provenance in resolved
                        )
                    )

    def test_a_malformed_collect_status_does_not_change_raw_resolution(self):
        common = {
            "key": "commune-confessoris",
            "propers": [
                composed("Collect", "Deus"),
                composed("Secret", "Suscipe"),
            ],
        }
        for status in (
            {**text_status("proper-collect"), "state": "available"},
            text_status("missal-formulary"),
        ):
            with self.subTest(status=status):
                saint = {
                    "key": "saint",
                    "takes_from": {"mass": "commune-confessoris"},
                    "text_status": status,
                }
                entries, problems = _calendars.resolve_propers(
                    document([common, saint]), saint
                )
                self.assertEqual(problems, [])
                self.assertEqual(names(entries), ["Collect", "Secret"])

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
                {
                    "name": "Sequence (ad libitum)",
                    "takes_from": {"mass": "easter", "proper": "Sequence"},
                }
            ],
        }
        entries, problems = _calendars.resolve_propers(
            document([sunday, octave]), octave
        )
        self.assertEqual(problems, [])
        self.assertEqual(entries[0][1]["name"], "Sequence (ad libitum)")
        self.assertEqual(entries[0][1]["text"], "Victimae")
        self.assertEqual(entries[0][2]["proper"], "Sequence")

    def test_real_qualified_aliases_keep_their_local_names(self):
        calendar = _calendars.load_document(
            ROOT / "src/sources/calendars", "roman-1962"
        )
        index = _calendars.mass_index(calendar)
        expected = {
            (
                "commune-martyrum-tempore-paschali-1",
                "Collect (Pro Martyre tantum)",
                "commune-unius-martyris-3",
                "Collect",
            ),
            (
                "commune-martyrum-tempore-paschali-1",
                "Secret (Item altera secreta)",
                "commune-unius-martyris-2",
                "Secret",
            ),
            (
                "commune-martyrum-tempore-paschali-1",
                "Secret (Pro Martyre tantum)",
                "commune-unius-martyris-3",
                "Secret",
            ),
            (
                "commune-martyrum-tempore-paschali-1",
                "Postcommunion (Item altera postcommunio)",
                "commune-unius-martyris-2",
                "Postcommunion",
            ),
            (
                "commune-martyrum-tempore-paschali-2",
                "Collect (Item altera oratio)",
                "commune-plurimorum-martyrum-3",
                "Collect",
            ),
            (
                "commune-martyrum-tempore-paschali-2",
                "Secret (Pro pluribus Martyribus tantum)",
                "commune-plurimorum-martyrum-2",
                "Secret",
            ),
            (
                "commune-non-virginum-1",
                "Postcommunion (Pro pluribus Martyribus quae non sint Virgines)",
                "commune-martyrum-tempore-paschali-2",
                "Postcommunion (Pro pluribus Martyribus tantum)",
            ),
            (
                "commune-virginum-4",
                "Gospel",
                "commune-non-virginum-1",
                "Gospel",
            ),
            (
                "commune-virginum-4",
                "Gospel (vel)",
                "commune-virginum-3",
                "Gospel",
            ),
            (
                "missa-de-s-maria-in-sabbato-4",
                "Alleluia",
                "commune-festorum-bmv",
                "Alleluia (Tempore paschali)",
            ),
        }
        actual = set()
        for mass_key, mass in index.items():
            for wrapper in mass.get("propers") or []:
                reference = _calendars.reference_of(wrapper)
                if reference is None or not reference.get("proper"):
                    continue
                edge = (
                    mass_key,
                    str(wrapper.get("name")),
                    str(reference.get("mass")),
                    str(reference.get("proper")),
                )
                # This test inventories differently named aliases.  The first
                # Virgin IV Gospel is the one source-order exception: its
                # wrapper is literally `Gospel`, but it still belongs here
                # beside the following `Gospel (vel)` because both borrow
                # differently appointed passages from separately printed
                # Commons.  Every other same-name reference is tested by the
                # general resolver cases rather than expanding this inventory.
                if wrapper.get("name") == reference.get("proper") and edge not in expected:
                    continue
                actual.add(edge)

                entries, problems = _calendars.resolve_propers(calendar, mass)
                self.assertEqual(problems, [], edge)
                resolved = [
                    (proper, provenance)
                    for _, proper, provenance in entries
                    if proper.get("name") == wrapper.get("name")
                ]
                self.assertEqual(len(resolved), 1, edge)
                proper, provenance = resolved[0]
                self.assertEqual(provenance["mass"], reference["mass"], edge)
                self.assertEqual(provenance["proper"], reference["proper"], edge)

                target_entries, target_problems = _calendars.resolve_propers(
                    calendar, index[reference["mass"]]
                )
                self.assertEqual(target_problems, [], edge)
                target = next(
                    target_proper
                    for _, target_proper, _ in target_entries
                    if target_proper.get("name") == reference["proper"]
                )
                expected_proper = dict(target)
                expected_proper["name"] = wrapper["name"]
                self.assertEqual(proper, expected_proper, edge)
                if mass_key == "commune-virginum-4":
                    # These qualified alternatives are structural aliases to
                    # fully encoded scripture passages, not composed-text
                    # placeholders.  The local label changes; verses and the
                    # deliberate absence of a `text` body do not.
                    self.assertEqual(proper["source"], "scripture", edge)
                    self.assertEqual(proper["verses"], target["verses"], edge)
                    self.assertNotIn("text", proper, edge)

        self.assertEqual(actual, expected)

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

    def test_a_proper_may_take_from_a_directly_printed_sibling_form(self):
        sequence = composed("Sequence", "Dies irae")
        mass = {
            "key": "all-souls",
            "forms": [
                {"name": "First Mass", "propers": [sequence]},
                {
                    "name": "Second Mass",
                    "propers": [
                        composed("Tract", "Absolve"),
                        {
                            "name": "Sequence",
                            "takes_from": {
                                "mass": "all-souls",
                                "form": "First Mass",
                                "proper": "Sequence",
                                "citation": "ut supra",
                            },
                        },
                    ],
                },
            ],
        }
        entries, problems = _calendars.resolve_propers(document([mass]), mass)
        self.assertEqual(problems, [])
        second = [entry for entry in entries if entry[0] == "Second Mass"]
        self.assertEqual(names(second), ["Tract", "Sequence"])
        self.assertIs(second[1][1], sequence)
        self.assertEqual(
            second[1][2],
            {
                "mass": "all-souls",
                "form": "First Mass",
                "proper": "Sequence",
                "citation": "ut supra",
            },
        )

    def test_a_same_form_proper_reference_is_a_cycle(self):
        mass = {
            "key": "all-souls",
            "forms": [
                {
                    "name": "First Mass",
                    "propers": [
                        {
                            "name": "Sequence",
                            "takes_from": {
                                "mass": "all-souls",
                                "form": "First Mass",
                            },
                        }
                    ],
                }
            ],
        }
        _, problems = _calendars.resolve_propers(document([mass]), mass)
        self.assertEqual(len(problems), 1)
        self.assertIn("closes a cycle", problems[0])

    def test_a_sibling_reference_must_land_on_a_directly_printed_proper(self):
        mass = {
            "key": "all-souls",
            "forms": [
                {
                    "name": "First Mass",
                    "propers": [
                        {
                            "name": "Sequence",
                            "takes_from": {
                                "mass": "all-souls",
                                "form": "Second Mass",
                            },
                        }
                    ],
                },
                {
                    "name": "Second Mass",
                    "propers": [
                        {
                            "name": "Sequence",
                            "takes_from": {
                                "mass": "all-souls",
                                "form": "First Mass",
                            },
                        }
                    ],
                },
            ],
        }
        _, problems = _calendars.resolve_propers(document([mass]), mass)
        self.assertEqual(len(problems), 2)
        self.assertTrue(
            all("itself takes from elsewhere" in problem for problem in problems),
            problems,
        )

    def test_real_all_souls_later_forms_inherit_the_first_sequence(self):
        calendar = _calendars.load_document(
            ROOT / "src/sources/calendars", "roman-1962"
        )
        mass = _calendars.mass_index(calendar)[
            "commemoratione-omnium-fidelium-defunctorum"
        ]
        entries, problems = _calendars.resolve_propers(calendar, mass)
        self.assertEqual(problems, [])
        by_form = {
            form: [entry for entry in entries if entry[0] == form]
            for form in (
                "First Mass (Ad primam Missam)",
                "Second Mass (Ad secundam Missam)",
                "Third Mass (Ad tertiam Missam)",
            )
        }
        self.assertEqual([len(entries) for entries in by_form.values()], [11, 11, 11])
        expected = [
            "Introit", "Collect", "Lesson", "Gradual", "Tract", "Sequence",
            "Gospel", "Offertory", "Secret", "Communion", "Postcommunion",
        ]
        first_sequence = next(
            proper
            for _, proper, _ in by_form["First Mass (Ad primam Missam)"]
            if proper["name"] == "Sequence"
        )
        for form, form_entries in by_form.items():
            appointed = names(form_entries)
            if form == "First Mass (Ad primam Missam)":
                self.assertEqual(appointed, [*expected[:2], "Epistle", *expected[3:]])
                continue
            self.assertEqual(appointed, expected)
            sequence = next(entry for entry in form_entries if entry[1]["name"] == "Sequence")
            self.assertIs(sequence[1], first_sequence)
            self.assertEqual(sequence[2]["form"], "First Mass (Ad primam Missam)")
            self.assertEqual(sequence[2]["proper"], "Sequence")

    def test_real_nativity_octave_days_mix_day_form_with_dawn_readings(self):
        calendar = _calendars.load_document(
            ROOT / "src/sources/calendars", "roman-1962"
        )
        index = _calendars.mass_index(calendar)
        resolved = []
        for key in (
            "fifth-day-within-octave",
            "sixth-day-within-octave",
            "seventh-day-within-octave",
        ):
            with self.subTest(mass=key):
                entries, problems = _calendars.resolve_propers(calendar, index[key])
                self.assertEqual(problems, [])
                appointed = {
                    proper["name"]: (proper, provenance)
                    for _, proper, provenance in entries
                }
                self.assertEqual(
                    [verse["ref"] for verse in appointed["Epistle"][0]["verses"]],
                    ["Titus 3:4-7"],
                )
                self.assertEqual(
                    [verse["ref"] for verse in appointed["Gospel"][0]["verses"]],
                    ["Luke 2:15-20"],
                )
                for name in ("Epistle", "Gospel"):
                    self.assertEqual(
                        appointed[name][1]["form"], "Ad secundam Missam in aurora"
                    )
                for name in ("Introit", "Gradual", "Offertory", "Communion"):
                    self.assertEqual(
                        appointed[name][1]["form"], "Ad tertiam Missam in die"
                    )
                references = {
                    verse["ref"]
                    for proper, _ in appointed.values()
                    for verse in proper.get("verses", [])
                }
                self.assertNotIn("Hebrews 1:1-12", references)
                self.assertNotIn("John 1:1-14", references)
                resolved.append(
                    [(proper, provenance) for _, proper, provenance in entries]
                )
        self.assertEqual(resolved[1:], [resolved[0], resolved[0]])

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

    def test_a_chain_of_qualified_proper_aliases_keeps_terminal_provenance(self):
        first = {"key": "a", "propers": [composed("Sequence", "one")]}
        second = {
            "key": "b",
            "propers": [
                {
                    "name": "Sequence (optional)",
                    "takes_from": {"mass": "a", "proper": "Sequence"},
                }
            ],
        }
        third = {
            "key": "c",
            "propers": [
                {
                    "name": "Sequence (ad libitum)",
                    "takes_from": {
                        "mass": "b",
                        "proper": "Sequence (optional)",
                    },
                }
            ],
        }
        entries, problems = _calendars.resolve_propers(
            document([first, second, third]), third
        )
        self.assertEqual(problems, [])
        self.assertEqual(entries[0][1]["name"], "Sequence (ad libitum)")
        self.assertEqual(entries[0][1]["text"], "one")
        self.assertEqual(entries[0][2]["mass"], "a")
        self.assertEqual(entries[0][2]["proper"], "Sequence")


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

    def historical_collect_gap(self) -> dict:
        return {
            "key": "saint",
            "name": "Saint",
            "registry": "x",
            "date": "01-14",
            "kind": "sanctoral",
            "rank": "III",
            "takes_from": {"mass": "commune-confessoris"},
            "text_status": text_status("proper-collect"),
        }

    def forms_entry(self, ids: list[object]) -> dict:
        return {
            "key": "several-forms",
            "name": "Several Forms",
            "registry": "x",
            "season": "advent",
            "forms": [
                {
                    "id": form_id,
                    "name": f"Form {index}",
                    "propers": [composed("Collect", f"Prayer {index}")],
                }
                for index, form_id in enumerate(ids, 1)
            ],
        }

    def partial_entry(self) -> dict:
        return {
            "key": "octave",
            "name": "Octave",
            "registry": "x",
            "season": "christmas",
            "text_status": partial_text_status(),
            "propers": [composed("Epistle", "Multifariam")],
        }

    def test_a_partial_formulary_coexists_with_local_propers_or_forms(self):
        self.assertEqual(self.check(self.partial_entry()), [])
        mass = self.partial_entry()
        del mass["season"]
        mass.update(date="01-01", kind="christological", rank="I")
        self.assertEqual(self.check(mass), [])

    def test_an_unavailable_seasonal_formulary_is_typed_and_text_free(self):
        mass = {
            "key": "unheld-rite",
            "name": "Unheld Rite",
            "registry": "x",
            "season": "holy-week",
            "text_status": text_status("missal-formulary"),
        }
        self.assertEqual(self.check(mass), [])
        mass["propers"] = [composed("Placeholder", "Not source text")]
        problems = self.check(mass)
        self.assertTrue(any("Placeholder is not a source-owned Proper" in p for p in problems))
        self.assertTrue(any("must not also carry propers or forms" in p for p in problems))

    def test_cycle_owner_may_carry_a_typed_removed_body_and_translation(self):
        mass = {
            "key": "cycle-body",
            "name": "Cycle Body",
            "registry": "x",
            "season": "ordinary-time",
            "propers": [
                {
                    "name": "Gospel Acclamation",
                    "cycles": {
                        "A": {
                            "source": "composed",
                            "text_status": text_status("proper-body"),
                            "translations": [
                                {
                                    "lang": "en",
                                    "rights": "project-created",
                                    "text": "Lawfully retained English.",
                                }
                            ],
                        }
                    },
                }
            ],
        }
        self.assertEqual(self.check(mass), [])
        branch = mass["propers"][0]["cycles"]["A"]
        branch["text"] = "Removed Latin must not return."
        self.assertTrue(
            any("removed body and must not coexist with text" in p for p in self.check(mass))
        )
        mass = self.partial_entry()
        del mass["propers"]
        mass["forms"] = self.forms_entry(["vigil", "day"])["forms"]
        self.assertEqual(self.check(mass), [])

    def test_a_partial_formulary_requires_exactly_one_local_text_container(self):
        mass = self.partial_entry()
        del mass["propers"]
        self.assertTrue(
            any("must coexist with exactly one of propers or forms" in problem
                for problem in self.check(mass))
        )
        mass = self.partial_entry()
        mass["forms"] = self.forms_entry(["only"])["forms"]
        self.assertTrue(
            any("must coexist with exactly one of propers or forms" in problem
                for problem in self.check(mass))
        )

    def test_a_partial_formulary_requires_a_dated_or_seasonal_mass(self):
        mass = self.partial_entry()
        del mass["season"]
        self.assertTrue(
            any("belongs only to a non-Common dated or seasonal mass" in problem
                for problem in self.check(mass))
        )

    def test_a_partial_formulary_refuses_references_and_other_scopes(self):
        for pointer, value in (
            ("takes_from", {"mass": "christmas-day"}),
            ("common_from", common_from()),
        ):
            with self.subTest(pointer=pointer):
                mass = self.partial_entry()
                mass[pointer] = value
                self.assertTrue(
                    any("cannot coexist with takes_from or common_from" in problem
                        for problem in self.check(mass))
                )
        mass = self.partial_entry()
        mass["text_status"]["scope"] = "proper-collect"
        self.assertTrue(
            any("partial text_status is only for scope 'missal-formulary'" in problem
                for problem in self.check(mass))
        )

    def test_a_proper_body_remains_unavailable_only(self):
        mass = self.partial_entry()
        mass["propers"] = [
            {
                "name": "Collect",
                "source": "composed",
                "text_status": {
                    **partial_text_status(),
                    "scope": "proper-body",
                },
            }
        ]
        self.assertTrue(
            any("text_status.state must be one of ['unavailable']" in problem
                for problem in self.check(mass))
        )

    def test_takes_from_may_pair_with_an_unavailable_proper_collect_only(self):
        self.assertEqual(self.check(self.historical_collect_gap()), [])
        for field, value in (("state", "available"), ("scope", "missal-formulary")):
            with self.subTest(field=field):
                mass = self.historical_collect_gap()
                mass["text_status"][field] = value
                self.assertNotEqual(self.check(mass), [])

    def test_a_collect_gap_refuses_local_collect_family_members(self):
        for name in ("Collect", "Collect (Altera oratio)"):
            with self.subTest(name=name):
                mass = self.historical_collect_gap()
                mass["propers"] = [composed(name, "Deus")]
                self.assertTrue(
                    any("also carries a Collect" in problem for problem in self.check(mass))
                )

    def test_a_collect_gap_refuses_forms_and_an_unresolved_common_direction(self):
        mass = self.historical_collect_gap()
        mass["forms"] = self.forms_entry(["only"])["forms"]
        self.assertTrue(
            any("must not also carry forms" in problem for problem in self.check(mass))
        )
        mass = self.historical_collect_gap()
        mass["common_from"] = common_from()
        self.assertTrue(
            any("cannot coexist with common_from" in problem for problem in self.check(mass))
        )

    def test_a_proper_collect_status_needs_one_formulary_pointer(self):
        mass = self.historical_collect_gap()
        del mass["takes_from"]
        self.assertTrue(
            any("must accompany exactly one of common_from" in problem for problem in self.check(mass))
        )

    def test_forms_require_stable_source_authored_ids(self):
        self.assertEqual(self.check(self.forms_entry(["vigil", "during-the-day"])), [])
        for malformed in (None, "", "Vigil", "vigil_mass", "-vigil", "vigil-"):
            with self.subTest(form_id=malformed):
                problems = self.check(self.forms_entry([malformed]))
                self.assertTrue(
                    any("form id must be a nonempty lowercase kebab-case" in problem for problem in problems)
                )

    def test_form_ids_are_unique_and_main_is_reserved_in_multi_form_masses(self):
        duplicates = self.check(self.forms_entry(["vigil", "vigil"]))
        self.assertTrue(any("duplicate form id 'vigil'" in problem for problem in duplicates))
        reserved = self.check(self.forms_entry(["main", "day"]))
        self.assertTrue(any("form id 'main' is reserved" in problem for problem in reserved))

    def test_form_display_names_are_unique_while_legacy_lookup_exists(self):
        mass = self.forms_entry(["vigil", "day"])
        mass["forms"][1]["name"] = mass["forms"][0]["name"]
        problems = self.check(mass)
        self.assertTrue(
            any("duplicate form name 'Form 1'" in problem for problem in problems),
            problems,
        )

    def test_form_shape_is_closed_and_display_name_is_a_string(self):
        mass = self.forms_entry(["vigil"])
        mass["forms"][0]["name"] = 7
        self.assertTrue(
            any("form name must be a nonempty string" in p for p in self.check(mass))
        )
        mass = self.forms_entry(["vigil"])
        mass["forms"][0]["label"] = "restated display name"
        self.assertTrue(
            any("form carries unknown field(s) label" in p for p in self.check(mass))
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
            any(
                "exactly one of propers, forms" in p and "takes_from" in p
                for p in problems
            )
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


class ValidateCommonDirection(unittest.TestCase):
    def check(self, entry: dict, section_kind: str = "") -> list[str]:
        problems: list[str] = []
        checker.check_entry(entry, 0, problems, section_kind=section_kind)
        return problems

    def common(self) -> dict:
        return {
            "key": "commune-martyrum",
            "name": "Commune Martyrum",
            "registry": "pc-C-martyrum",
            "text_status": text_status("missal-formulary"),
        }

    def saint(self) -> dict:
        return {
            "key": "saint",
            "name": "Saint",
            "registry": "pc-01-01",
            "date": "01-01",
            "kind": "sanctoral",
            "rank": "Optional memorial",
            "common_from": common_from(),
            "text_status": text_status("proper-collect"),
        }

    def test_an_unavailable_common_is_an_explicit_text_free_mass(self):
        self.assertEqual(self.check(self.common(), checker.COMMON_KIND), [])

    def test_an_unavailable_common_remains_text_free(self):
        common = self.common()
        common["propers"] = [composed("Collect", "Deus")]
        self.assertTrue(
            any("must not also carry propers or forms" in problem
                for problem in self.check(common, checker.COMMON_KIND))
        )

    def test_a_common_formulary_can_never_be_partial(self):
        common = self.common()
        common["text_status"] = partial_text_status()
        self.assertTrue(
            any("text_status.state must be one of ['unavailable']" in problem
                for problem in self.check(common, checker.COMMON_KIND))
        )

    def test_a_common_direction_with_a_collect_status_needs_no_fake_proper(self):
        self.assertEqual(self.check(self.saint()), [])

    def test_a_common_direction_does_not_resolve_absent_target_text(self):
        saint, common = self.saint(), self.common()
        source = {
            "sections": {
                "sanctoral": {"kind": "sanctoral", "masses": [saint]},
                "common": {"kind": "common", "masses": [common]},
            }
        }
        entries, problems = _calendars.resolve_propers(source, saint)
        self.assertEqual(entries, [])
        self.assertEqual(problems, [])

    def test_a_common_direction_without_text_status_is_refused(self):
        saint = self.saint()
        del saint["text_status"]
        self.assertTrue(
            any("requires text_status" in problem for problem in self.check(saint))
        )

    def test_a_common_direction_must_not_carry_local_propers(self):
        saint = self.saint()
        saint["propers"] = [composed("Prayer over the Offerings", "Suscipe")]
        problems = self.check(saint)
        self.assertTrue(any("must not also carry local propers" in p for p in problems))

    def test_unknown_common_direction_and_status_fields_are_refused(self):
        saint = self.saint()
        saint["common_from"]["page"] = 112
        saint["text_status"]["note"] = "prose is not a status axis"
        problems = self.check(saint)
        self.assertTrue(any("unknown field(s) page" in problem for problem in problems))
        self.assertTrue(any("unknown field(s) note" in problem for problem in problems))

    def test_every_common_option_must_land_in_the_common_section(self):
        saint, common = self.saint(), self.common()
        self.assertEqual(
            checker.common_reference_problems(
                [("sanctoral", saint), (checker.COMMON_KIND, common)]
            ),
            [],
        )
        problems = checker.common_reference_problems(
            [("sanctoral", saint), ("seasonal", common)]
        )
        self.assertTrue(any("not the Commune Sanctorum" in p for p in problems))

    def test_a_common_target_must_be_typed_unavailable_and_text_free(self):
        saint, common = self.saint(), self.common()
        del common["text_status"]
        problems = checker.common_reference_problems(
            [("sanctoral", saint), (checker.COMMON_KIND, common)]
        )
        self.assertTrue(any("not explicitly unavailable" in p for p in problems))
        common["text_status"] = text_status("missal-formulary")
        common["propers"] = [composed("Collect", "Deus")]
        problems = checker.common_reference_problems(
            [("sanctoral", saint), (checker.COMMON_KIND, common)]
        )
        self.assertTrue(any("explicitly text-free Common" in p for p in problems))

    def test_no_exemplar_omits_a_source_but_other_reasons_require_one(self):
        common = self.common()
        common["text_status"]["reasons"] = [{"kind": "no-exemplar"}]
        self.assertEqual(self.check(common, checker.COMMON_KIND), [])
        common["text_status"]["reasons"][0]["source_id"] = MISSAL_SOURCE
        self.assertTrue(any("must omit source_id" in p for p in self.check(common, checker.COMMON_KIND)))
        common["text_status"]["reasons"] = [{"kind": "rights-withheld"}]
        self.assertTrue(any("source_id must be" in p for p in self.check(common, checker.COMMON_KIND)))

    def test_a_missing_common_target_is_refused(self):
        problems = checker.common_reference_problems([("sanctoral", self.saint())])
        self.assertTrue(any("no entry for" in problem for problem in problems))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
