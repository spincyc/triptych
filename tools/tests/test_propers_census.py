"""One census, derived once, carried by every document that states it.

The count of the two calendars existed in three retyped copies — `docs/the-mass.md`,
`guidance/propers-for-agents.md`, and the table in `src/sources/calendars/README.md` —
and all three disagreed. A page that said "counted from the files, not estimated"
and named a date was reporting a 1962 sanctoral section of 247 against a file
holding 307.

Two failures are held here. The first is the counting key: a mass whose
placeholders sit inside a `forms` block holds nothing but placeholders, and the
key in use read the mass's own `propers` and reported it substantive, which is
five masses' worth of understatement. The second is drift: the block is written
by one verb into every document that carries it, so the documents cannot
disagree with each other, and `--check` refuses a document that has fallen
behind the calendars.
"""

from __future__ import annotations

import copy
import csv
import unittest
import tomllib
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[2]


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


propers = load_tool("mass-propers")


def placeholder(name: str = "Placeholder") -> dict:
    return {"name": name, "source": "composed", "text": "..."}


def section(kind: str, masses: list[dict]) -> dict:
    return {"kind": kind, "label": kind.title(), "masses": masses}


class CountingKeyTests(unittest.TestCase):
    def test_a_mass_whose_placeholders_sit_inside_forms_holds_only_placeholders(self) -> None:
        mass = {
            "key": "nativity",
            "forms": [
                {"name": "in nocte", "propers": [placeholder()]},
                {"name": "in die", "propers": [placeholder()]},
            ],
        }
        self.assertTrue(propers.placeholder_only(mass))

    def test_a_mass_holding_one_real_proper_is_not_placeholder_only(self) -> None:
        mass = {
            "key": "vigil-and-day",
            "forms": [
                {"name": "vigil", "propers": [placeholder()]},
                {"name": "day", "propers": [{"name": "Collect", "source": "composed"}]},
            ],
        }
        self.assertFalse(propers.placeholder_only(mass))

    def test_a_mass_with_no_propers_at_all_is_not_placeholder_only(self) -> None:
        self.assertFalse(propers.placeholder_only({"key": "empty"}))

    def test_a_proper_carrying_cycles_counts_once_not_three_times(self) -> None:
        gospel = {
            "name": "Gospel",
            "cycles": {
                "A": {"source": "scripture", "verses": []},
                "B": {"source": "scripture", "verses": []},
                "C": {"source": "scripture", "verses": []},
            },
        }
        counted = propers.census_of(
            {"sections": {"seasonal": section("seasonal", [{"key": "advent-1", "propers": [gospel]}])}}
        )
        self.assertEqual(counted["propers"], 1)
        self.assertEqual(counted["cycle_propers"], 1)
        self.assertEqual(counted["scripture_bearing_propers"], 1)

    def test_placeholders_are_inside_the_totals_and_counted_again_on_their_own(self) -> None:
        counted = propers.census_of(
            {
                "sections": {
                    "sanctoral": section(
                        "sanctoral",
                        [
                            {"key": "one", "propers": [placeholder()]},
                            {"key": "two", "propers": [{"name": "Introit", "source": "scripture"}]},
                        ],
                    )
                }
            }
        )
        self.assertEqual(counted["propers"], 2)
        self.assertEqual(counted["placeholder_propers"], 1)
        self.assertEqual(counted["substantive_propers"], 1)
        self.assertEqual(counted["placeholder_only_masses"], 1)

    def test_propers_inside_forms_are_in_the_total_and_named_separately(self) -> None:
        counted = propers.census_of(
            {
                "sections": {
                    "seasonal": section(
                        "seasonal",
                        [
                            {
                                "key": "nativity",
                                "forms": [{"name": "in die", "propers": [placeholder(), placeholder()]}],
                            }
                        ],
                    )
                }
            }
        )
        self.assertEqual(counted["propers"], 2)
        self.assertEqual(counted["propers_in_forms"], 2)

    def test_sections_are_emitted_in_a_fixed_order_whatever_the_file_does(self) -> None:
        document = {
            "sections": {
                "sanctoral": section("sanctoral", []),
                "marian": section("marian", []),
                "seasonal": section("seasonal", []),
                "christological": section("christological", []),
            }
        }
        self.assertEqual(
            [row["kind"] for row in propers.census_of(document)["sections"]],
            list(propers.KIND_ORDER),
        )

    def test_roman_1962_counts_source_established_unavailable_slots_as_propers(
        self,
    ) -> None:
        document = propers.load_calendar(
            ROOT / "src" / "sources" / "calendars",
            "roman-1962",
            effective=False,
        )
        counted = propers.census_of(document)

        self.assertEqual(
            {
                row["kind"]: (row["masses"], row["propers"])
                for row in counted["sections"]
            },
            {
                "seasonal": (128, 1352),
                "christological": (8, 96),
                "marian": (18, 124),
                "sanctoral": (307, 1511),
                "common": (30, 358),
            },
        )
        self.assertEqual(counted["masses"], 491)
        self.assertEqual(counted["propers"], 3441)
        self.assertEqual(counted["substantive_propers"], 3441)
        self.assertEqual(counted["propers_in_forms"], 182)
        self.assertEqual(counted["scripture_bearing_propers"], 2194)
        self.assertEqual(counted["slot_names"], 120)


class RankCensusTests(unittest.TestCase):
    """The third hand derivation of a rank census, made the last one.

    A rank census had been recomputed ad hoc in Python over
    `sections[].masses[].rank` three times, most recently to settle whether the
    postconciliar index is scoped to Sundays, solemnities and the Triduum. It is
    not, and retiring the sentence that said it was turned on that count. The
    count will be wanted again, so it is derived here rather than retyped.

    The joined entries are the whole difficulty. One entry can print two
    celebrations or three, and the index says so only in the entry's `name`; the
    plural rank word marks some of them and not others, and never says how many.
    """

    def ranks(self, masses: list[dict]) -> dict[str, dict]:
        counted = propers.census_of({"sections": {"sanctoral": section("sanctoral", masses)}})
        return {row["rank"]: row for row in counted["ranks"]}

    def test_an_entry_printing_no_rank_is_a_row_and_not_a_silence(self) -> None:
        rows = self.ranks([{"key": "feria", "name": "Feria"}])
        self.assertEqual(rows[propers.NO_RANK]["entries"], 1)

    def test_an_empty_rank_string_counts_as_no_rank(self) -> None:
        rows = self.ranks([{"key": "feria", "name": "Feria", "rank": ""}])
        self.assertEqual(list(rows), [propers.NO_RANK])

    def test_a_joined_entry_is_one_entry_and_the_celebrations_it_names(self) -> None:
        rows = self.ranks(
            [
                {
                    "key": "saint-fabian-pope-martyr",
                    "name": "Saint Fabian, Pope and Martyr; Saint Sebastian, Martyr",
                    "rank": "Optional memorials",
                }
            ]
        )
        self.assertEqual(rows["Optional memorials"]["entries"], 1)
        self.assertEqual(rows["Optional memorials"]["celebrations"], 2)

    def test_a_joined_entry_naming_three_is_not_assumed_to_name_two(self) -> None:
        """Two of the eighteen postconciliar joined entries name three saints.

        Hard-coding two celebrations for a plural rank would have been right
        sixteen times and wrong twice, and silently.
        """
        rows = self.ranks(
            [
                {
                    "key": "saint-bede",
                    "name": "Saint Bede; Saint Gregory VII; Saint Mary Magdalene de' Pazzi",
                    "rank": "Optional memorials",
                }
            ]
        )
        self.assertEqual(rows["Optional memorials"]["celebrations"], 3)

    def test_a_singular_rank_can_join_celebrations_too(self) -> None:
        """The 1962 index joins the Greater Litanies to Saint Mark under rank II.

        The join is not a property of the plural rank word; reading it out of the
        rank rather than the name would miss this entry entirely.
        """
        rows = self.ranks(
            [
                {
                    "key": "litania-maior",
                    "name": "Litania maior; S. Marci Evangelistae",
                    "rank": "II",
                }
            ]
        )
        self.assertEqual(rows["II"]["entries"], 1)
        self.assertEqual(rows["II"]["celebrations"], 2)

    def test_an_unnamed_entry_still_keeps_one_mass(self) -> None:
        rows = self.ranks([{"key": "anonymous", "rank": "Feast"}])
        self.assertEqual(rows["Feast"]["celebrations"], 1)

    def test_rank_strings_are_never_normalised_into_each_other(self) -> None:
        rows = self.ranks(
            [
                {"key": "a", "name": "A", "rank": "Optional memorial"},
                {"key": "b", "name": "B; C", "rank": "Optional memorials"},
            ]
        )
        self.assertEqual(rows["Optional memorial"]["entries"], 1)
        self.assertEqual(rows["Optional memorials"]["entries"], 1)

    def test_the_unranked_row_leads_and_the_rest_are_ordered_by_name(self) -> None:
        """Order follows the rank string, so a row moves only when a rank does.

        Ordering by size would reshuffle the whole table each time a mass landed,
        which is the reflow the derived block exists to avoid.
        """
        rows = propers.census_of(
            {
                "sections": {
                    "sanctoral": section(
                        "sanctoral",
                        [
                            {"key": "a", "name": "A", "rank": "Solemnity"},
                            {"key": "b", "name": "B", "rank": "Feast"},
                            {"key": "c", "name": "C", "rank": "Feast"},
                            {"key": "d", "name": "D"},
                        ],
                    )
                }
            }
        )["ranks"]
        self.assertEqual([row["rank"] for row in rows], [propers.NO_RANK, "Feast", "Solemnity"])

    def test_the_rank_rows_sum_to_the_calendars_own_mass_total(self) -> None:
        """The arithmetic that keeps the table readable as one book.

        It holds on the real calendars, not only on a fixture: an entry counted
        under a rank and not under a section, or the reverse, is a defect this
        assertion is the only thing that would find.
        """
        for name, counted in propers.census(ROOT / "src" / "sources" / "calendars").items():
            with self.subTest(calendar=name):
                self.assertEqual(
                    sum(row["entries"] for row in counted["ranks"]), counted["masses"]
                )
                self.assertGreaterEqual(
                    sum(row["celebrations"] for row in counted["ranks"]), counted["masses"]
                )

    def test_the_block_carries_the_rank_table_and_check_therefore_gates_it(self) -> None:
        """`--check` gates the new rows because they are inside the one block.

        `test_the_carried_block_still_matches_the_calendars` compares the whole
        region byte for byte, so nothing further is needed to gate these rows —
        but only if they are actually in the block, which is what this asserts.
        """
        block = propers.render_census(propers.census(ROOT / "src" / "sources" / "calendars"))
        self.assertIn("| Calendar | Rank | Entries | Celebrations |", block)
        self.assertIn(f"| {propers.NO_RANK} |", block)

    def test_the_rank_key_is_stated_in_its_own_paragraph(self) -> None:
        """Kept separate so that adding it re-wrapped no line of the older key.

        Appending to CENSUS_KEYS would have re-flowed a paragraph that had not
        changed, and a derived block whose diff shows lines that did not move is
        a block nobody reads the diff of.
        """
        self.assertNotIn(propers.CENSUS_RANK_KEYS, propers.CENSUS_KEYS)
        block = propers.render_census(propers.census(ROOT / "src" / "sources" / "calendars"))
        import textwrap

        self.assertIn("\n".join(textwrap.wrap(propers.CENSUS_KEYS, propers.WIDTH)), block)
        self.assertIn("\n".join(textwrap.wrap(propers.CENSUS_RANK_KEYS, propers.WIDTH)), block)


class EnglishCoverageTests(unittest.TestCase):
    """Derived from this side, written nowhere.

    `english_oration_census` in the 1962 translations sidecar states the same
    coverage in hand-typed prose. That block is not this tool's to write, so the
    figures are derived and reported; what these tests hold is that the
    derivation is the browser's own and not a second opinion about it.
    """

    def test_a_borrowed_proper_is_keyed_to_the_entry_that_prints_it(self) -> None:
        taken = {"mass": "comm-martyris", "form": "", "proper": "Collect"}
        self.assertEqual(
            propers.overlay_key({"key": "s-agapiti"}, "", {"name": "Collect"}, taken),
            ("comm-martyris", "", "Collect"),
        )

    def test_an_unborrowed_proper_is_keyed_to_its_own_mass_and_form(self) -> None:
        self.assertEqual(
            propers.overlay_key({"key": "advent-1"}, "vigil", {"name": "Secret"}, None),
            ("advent-1", "vigil", "Secret"),
        )

    def test_a_rubrical_qualifier_does_not_make_a_new_slot_family(self) -> None:
        self.assertEqual(propers.slot_family("Secret (Pro Martyre tantum)"), "Secret")
        self.assertEqual(propers.slot_family("Secret"), "Secret")
        self.assertEqual(propers.slot_family(None), "")

    def test_english_coverage_does_not_count_another_language(self) -> None:
        entry = {
            "translations": [
                {"lang": "fr", "text": "Texte français"},
                {"lang": "de", "text": "Deutscher Text"},
            ]
        }
        self.assertFalse(propers.has_translation(entry, "en"))
        entry["translations"].append({"lang": "en", "text": "English text"})
        self.assertTrue(propers.has_translation(entry, "en"))

    def test_a_calendar_with_no_translation_ledger_reports_nothing(self) -> None:
        """Silence, not a row of zeroes: nothing has claimed to cover it."""
        root = ROOT / "src" / "sources" / "calendars"
        named = {row["calendar"] for row in propers.coverage(root)}
        for name in propers.calendars(root):
            overlay, untranslated, _, _ = propers.translation_overlay(name)
            with self.subTest(calendar=name):
                self.assertEqual(name in named, bool(overlay or untranslated))

    def test_every_ledger_row_and_every_covered_slot_is_inside_the_slot_total(self) -> None:
        """The arithmetic of the reported line, on the real corpus.

        A covered or ledgered slot outside the total would mean the denominator
        and the numerators were keyed differently, which is exactly how the
        hand-typed block came to state figures that do not add up.
        """
        for row in propers.coverage(ROOT / "src" / "sources" / "calendars"):
            with self.subTest(calendar=row["calendar"]):
                self.assertNotIn("error", row)
                self.assertEqual(
                    row["with_english"]
                    + row["rights_restricted"]
                    + row["ledgered_untranslated"]
                    + row["unaccounted"],
                    row["slots"],
                )
                self.assertEqual(
                    row["with_english_held"],
                    row["with_english"] + row["rights_restricted"],
                )

    def test_stale_incipits_and_cycle_absences_do_not_answer_a_whole_slot(self) -> None:
        proper = {
            "name": "Gospel Acclamation",
            "incipit": "Live incipit",
            "source": "mixed",
            "cycles": {
                "A": {"source": "mixed", "incipit": "Cycle A"},
                "C": {"source": "mixed", "incipit": "Cycle C"},
            },
        }
        stale = {
            "incipit": "Former incipit",
            "translations": [{"lang": "en", "text": "Former words"}],
        }
        self.assertFalse(propers.translation_answers(stale, proper, "en"))

        records = [
            {
                "mass": "demo", "form_id": "main", "proper": "Gospel Acclamation",
                "lang": "en", "cycle": "C", "occurrence": 1,
                "extent": "incipit", "incipit": "Cycle C",
                "availability": "unavailable", "reason": {"kind": "no-exemplar"},
                "note": "No body exemplar was found.",
            },
            {
                "mass": "demo", "form_id": "main", "proper": "Gospel Acclamation",
                "lang": "en", "cycle": "B", "occurrence": 1,
                "extent": "incipit", "incipit": "Cycle B",
                "availability": "unavailable", "reason": {"kind": "no-exemplar"},
                "note": "No body exemplar was found.",
            },
            {
                "mass": "demo", "form_id": "main", "proper": "Gospel Acclamation",
                "lang": "en", "cycle": "all", "occurrence": 1,
                "extent": "incipit", "incipit": "Former incipit",
                "availability": "unavailable", "reason": {"kind": "no-exemplar"},
                "note": "No body exemplar was found.",
            },
        ]
        matching = propers.matching_untranslated_records(proper, records)
        self.assertEqual([row.get("cycle") for row in matching], ["C"])
        self.assertEqual(
            propers.matching_untranslated_records(
                proper, records, cycle="C", extent="body"
            ),
            [],
            "an incipit-only finding must never close a missing body",
        )
        partial = dict(records[0])
        partial.pop("cycle")
        self.assertFalse(
            propers.untranslated_record_matches(proper, partial),
            "a missing cycle must not default to all",
        )
        carried = dict(proper, untranslated=matching, text="Latin fallback")
        english = {
            row["lang"]: row
            for row in propers.proper_language_capabilities(carried)
        }["en"]
        self.assertEqual(english["status"], "fallback-latin")
        self.assertEqual(english["reason"], {"kind": "no-translation-recorded"})

    def test_cycle_body_absence_answers_only_its_exact_composed_cycle(self) -> None:
        proper = {
            "name": "Gospel Acclamation",
            "cycles": {
                "A": {"source": "composed", "text": "Cycle A body"},
                "B": {"source": "composed", "text": "Cycle B body"},
                "C": {"source": "scripture", "verses": []},
            },
        }
        units = propers.coverage_slot_units(
            proper, ("demo", "main", "Gospel Acclamation", 1)
        )
        self.assertEqual([identity[3] for identity, _ in units], ["A", "B"])
        record = {
            "mass": "demo",
            "form_id": "main",
            "proper": "Gospel Acclamation",
            "cycle": "A",
            "occurrence": 1,
            "extent": "body",
            "lang": "en",
            "availability": "unavailable",
            "reason": {"kind": "no-exemplar"},
            "note": "No exemplar",
        }
        self.assertTrue(
            propers.untranslated_record_matches(
                proper, record, cycle="A", extent="body"
            )
        )
        self.assertFalse(
            propers.untranslated_record_matches(
                proper, record, cycle="B", extent="body"
            )
        )
        whole = dict(record, cycle="all")
        self.assertFalse(
            propers.untranslated_record_matches(
                proper, whole, cycle="A", extent="body"
            ),
            "an all-sentinel row is not a composed cycle's body",
        )

    def test_a_recension_names_the_translation_ledger_it_inherits(self) -> None:
        """Equal coverage totals must not imply independent translation work."""
        rows = {
            row["calendar"]: row
            for row in propers.coverage(ROOT / "src" / "sources" / "calendars")
        }
        self.assertEqual(rows["roman-1962"]["translation_ledger_calendar"], "roman-1962")
        self.assertFalse(rows["roman-1962"]["translation_ledger_inherited"])
        self.assertEqual(
            rows["roman-pre-1955"]["translation_ledger_calendar"],
            "roman-pre-1955",
        )
        self.assertEqual(
            rows["roman-pre-1955"]["translation_ledger_calendars"],
            ["roman-1962", "roman-pre-1955"],
        )
        self.assertTrue(rows["roman-pre-1955"]["translation_ledger_inherited"])
        self.assertEqual(
            rows["roman-pre-1955"]["inherited_inapplicable_records"], 48
        )

    def test_translation_ledger_inheritance_follows_a_recension_chain(self) -> None:
        """A future middle recension must not cut its descendant off."""
        with TemporaryDirectory() as temporary:
            repository = Path(temporary)
            calendars = repository / "src" / "sources" / "calendars"
            inventories = repository / "src" / "sources" / "inventories"
            inventories.mkdir(parents=True)
            for name, base in (("base", None), ("middle", "base"), ("leaf", "middle")):
                directory = calendars / name
                directory.mkdir(parents=True)
                inherited = f"text_from: {base}\n" if base else ""
                (directory / "propers.yaml").write_text(
                    "schema: triptych-calendar-masses/v1\n"
                    f"calendar: {name}\n"
                    f"{inherited}"
                    "sections: {}\n",
                    encoding="utf-8",
                )
            (inventories / "base-proper-translations-v1.toml").write_text(
                'translations_schema = 1\ncalendar = "base"\n',
                encoding="utf-8",
            )
            previous = propers.ROOT
            propers.ROOT = repository
            try:
                self.assertEqual(
                    propers.translation_ledger_calendar("leaf", calendars), "base"
                )
            finally:
                propers.ROOT = previous

    def test_translation_overlay_uses_the_passed_root_and_rejects_collisions(self) -> None:
        with TemporaryDirectory() as temporary:
            sources = Path(temporary) / "sources"
            calendars = sources / "calendars"
            inventories = sources / "inventories"
            (calendars / "demo").mkdir(parents=True)
            inventories.mkdir(parents=True)
            (calendars / "demo" / "propers.yaml").write_text(
                "schema: triptych-calendar-masses/v1\n"
                "calendar: demo\n"
                "sections: {}\n",
                encoding="utf-8",
            )
            ledger = inventories / "demo-proper-translations-v1.toml"
            ledger.write_text(
                'calendar = "demo"\n'
                '[[entries]]\nmass = "m"\nform = ""\nproper = "Collect"\n'
                '[[entries.translations]]\nlang = "en"\nrights = "project-created"\ntext = "Here"\n',
                encoding="utf-8",
            )
            overlay, _, _, _ = propers.translation_overlay("demo", calendars)
            self.assertEqual(
                overlay[("m", "main", "Collect", "all", 1)]["translations"][0]["text"],
                "Here",
            )

            ledger.write_text(
                ledger.read_text(encoding="utf-8")
                + '[[entries]]\nmass = "m"\nform = ""\nproper = "Collect"\n'
                + '[[entries.translations]]\nlang = "en"\nrights = "project-created"\ntext = "Again"\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate translation entry"):
                propers.translation_overlay("demo", calendars)

            ledger.write_text(
                'calendar = "demo"\n'
                '[[sources]]\nid = "one"\nsource_id = "edition.same"\n'
                '[[sources]]\nid = "two"\nsource_id = "edition.same"\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate translation source alias"):
                propers.translation_overlay("demo", calendars)

            ledger.write_text(
                'calendar = "demo"\n'
                '[[sources]]\nid = "same"\nsource_id = "edition.one"\n'
                '[[sources]]\nid = "same"\nsource_id = "edition.two"\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate translation source id"):
                propers.translation_overlay("demo", calendars)

            ledger.write_text(
                'calendar = "demo"\n'
                '[[entries]]\nmass = "m"\nform = ""\nproper = "Collect"\n'
                'form_id = "main"\ncycle = "all"\noccurrence = 1\n'
                '[[entries.translations]]\nlang = "en"\nrights = "project-created"\n'
                'text = "Here"\n'
                '[[untranslated]]\nmass = "m"\nform_id = "main"\n'
                'proper = "Collect"\ncycle = "all"\noccurrence = 1\n'
                'extent = "body"\nlang = "en"\navailability = "unavailable"\n'
                'note = "No exemplar"\nreason = {kind = "no-exemplar"}\n',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValueError, "translation and untranslated target collide"
            ):
                propers.translation_overlay("demo", calendars)

    def test_recension_sidecar_exclusions_must_match_their_typed_departure(self) -> None:
        with TemporaryDirectory() as temporary:
            sources = Path(temporary) / "sources"
            calendars = sources / "calendars"
            inventories = sources / "inventories"
            inventories.mkdir(parents=True)
            for name in ("base", "child"):
                (calendars / name).mkdir(parents=True)
            (calendars / "base" / "propers.yaml").write_text(
                "schema: triptych-calendar-masses/v1\n"
                "calendar: base\n"
                "sections:\n"
                "  seasonal:\n"
                "    kind: seasonal\n"
                "    masses:\n"
                "    - key: replaced\n"
                "      name: Replaced\n"
                "      season: test\n"
                "      propers:\n"
                "      - {name: Collect, source: composed, text: Latin collect}\n"
                "      - {name: Secret, source: composed, text: Latin secret}\n"
                "    - key: kept\n"
                "      name: Kept\n"
                "      season: test\n"
                "      propers:\n"
                "      - {name: Collect, source: composed, text: Latin kept}\n"
                "      - {name: Secret, source: composed, text: Latin kept secret}\n",
                encoding="utf-8",
            )
            (calendars / "child" / "propers.yaml").write_text(
                "schema: triptych-calendar-masses/v1\n"
                "calendar: child\n"
                "text_from: base\n"
                "sections:\n"
                "  seasonal:\n"
                "    kind: seasonal\n"
                "    masses:\n"
                "    - key: replaced\n"
                "      name: Replaced earlier form\n"
                "      season: test\n"
                "      departure: replaced\n"
                "      basis: exact source collation\n"
                "      propers:\n"
                "      - {name: Placeholder, source: composed, text: workflow note}\n",
                encoding="utf-8",
            )
            (inventories / "base-proper-translations-v1.toml").write_text(
                'calendar = "base"\n'
                '[[entries]]\nmass = "replaced"\nform = ""\nproper = "Collect"\n'
                'form_id = "main"\ncycle = "all"\noccurrence = 1\n'
                '[[entries.translations]]\nlang = "en"\nrights = "project-created"\ntext = "Old"\n'
                '[[entries]]\nmass = "kept"\nform = ""\nproper = "Collect"\n'
                'form_id = "main"\ncycle = "all"\noccurrence = 1\n'
                '[[entries.translations]]\nlang = "en"\nrights = "project-created"\ntext = "Kept"\n'
                '[[untranslated]]\nmass = "replaced"\nform_id = "main"\nproper = "Secret"\n'
                'cycle = "all"\noccurrence = 1\nextent = "body"\nlang = "en"\n'
                'availability = "unavailable"\nnote = "No exemplar"\n'
                'reason = {kind = "no-exemplar"}\n',
                encoding="utf-8",
            )
            child = inventories / "child-proper-translations-v1.toml"
            child.write_text(
                'calendar = "child"\n'
                '[[inherited_inapplicable]]\nrecord = "entry"\nmass = "replaced"\n'
                'form_id = "main"\nproper = "Collect"\ncycle = "all"\noccurrence = 1\n'
                'reason = "recension-replaced"\nbasis = "calendar-departure"\n'
                '[[inherited_inapplicable]]\nrecord = "untranslated"\nmass = "replaced"\n'
                'form_id = "main"\nproper = "Secret"\ncycle = "all"\noccurrence = 1\n'
                'reason = "recension-replaced"\nbasis = "calendar-departure"\n'
                '[[untranslated]]\nmass = "kept"\nform_id = "main"\nproper = "Secret"\n'
                'cycle = "all"\noccurrence = 1\nextent = "body"\nlang = "en"\n'
                'availability = "unavailable"\nnote = "No exemplar"\n'
                'reason = {kind = "no-exemplar"}\n',
                encoding="utf-8",
            )

            overlay, unavailable, _, _ = propers.translation_overlay("child", calendars)
            self.assertEqual(propers.translation_ledger_calendars("child", calendars), ["base", "child"])
            self.assertEqual(
                set(overlay), {("kept", "main", "Collect", "all", 1)}
            )
            self.assertEqual(set(unavailable), {("kept", "main", "Secret")})
            self.assertEqual(propers.inherited_inapplicable_count("child", calendars), 2)

            child.write_text(
                child.read_text(encoding="utf-8").replace(
                    'mass = "replaced"\nform_id = "main"\nproper = "Collect"',
                    'mass = "kept"\nform_id = "main"\nproper = "Collect"',
                    1,
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValueError, "not owned by a calendar departure 'replaced'"
            ):
                propers.translation_overlay("child", calendars)

            child.write_text(
                child.read_text(encoding="utf-8")
                .replace(
                    'mass = "kept"\nform_id = "main"\nproper = "Collect"',
                    'mass = "replaced"\nform_id = "main"\nproper = "Collect"',
                    1,
                )
                .replace('reason = "recension-replaced"', 'reason = "recension-absent"', 1),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ValueError,
                "not owned by a calendar departure 'absent'.*recension-absent",
            ):
                propers.translation_overlay("child", calendars)

    def test_every_tracked_multiform_translation_authors_its_stable_identity(self) -> None:
        inventories = ROOT / "src" / "sources" / "inventories"
        for path in sorted(inventories.glob("*-proper-translations-v1.toml")):
            document = tomllib.loads(path.read_text(encoding="utf-8"))
            for table in ("entries", "untranslated"):
                for index, row in enumerate(document.get(table) or []):
                    if not isinstance(row, dict) or not row.get("form"):
                        continue
                    with self.subTest(path=path.name, table=table, index=index):
                        self.assertIsInstance(row.get("form_id"), str)
                        self.assertTrue(row["form_id"])
                        self.assertEqual(row.get("cycle"), "all")
                        self.assertIsInstance(row.get("occurrence"), int)
                        self.assertGreater(row["occurrence"], 0)

    def test_every_tracked_untranslated_row_has_no_legacy_identity_path(self) -> None:
        inventories = ROOT / "src" / "sources" / "inventories"
        for path in sorted(inventories.glob("*-proper-translations-v1.toml")):
            document = tomllib.loads(path.read_text(encoding="utf-8"))
            for index, row in enumerate(document.get("untranslated") or []):
                with self.subTest(path=path.name, index=index):
                    self.assertNotIn("form", row)
                    self.assertNotIn("text", row)
                    identity = propers.untranslated_record_identity(row, path)
                    self.assertEqual(identity[3], row["cycle"])
                    self.assertEqual(identity[4], row["occurrence"])

    def test_publication_bound_translations_fail_closed_on_any_stale_edge(self) -> None:
        path = (
            ROOT
            / "src/sources/inventories/roman-1962-proper-translations-v1.toml"
        )
        document = tomllib.loads(path.read_text(encoding="utf-8"))
        rows = [
            row
            for row in document.get("entries") or []
            if "publication_artifact_id" in row
        ]
        cummiskey_source = (
            "edition.eugene-cummiskey.roman-missal-english-laity."
            "philadelphia-1861"
        )
        expected = [
            row
            for row in document.get("entries") or []
            if any(
                translation.get("source_id") == cummiskey_source
                for translation in row.get("translations") or []
            )
        ]
        self.assertEqual(
            {
                (
                    row["mass"],
                    row["form_id"],
                    row["proper"],
                    row["cycle"],
                    row["occurrence"],
                )
                for row in rows
            },
            {
                (
                    row["mass"],
                    row["form_id"],
                    row["proper"],
                    row["cycle"],
                    row["occurrence"],
                )
                for row in expected
            },
            "every deliberate Cummiskey positive must have a publication binding",
        )
        for row in rows:
            with self.subTest(
                mass=row.get("mass"),
                form_id=row.get("form_id"),
                proper=row.get("proper"),
            ):
                self.assertEqual(
                    [
                        (translation.get("lang"), translation.get("rights"))
                        for translation in row.get("translations") or []
                    ],
                    [("en", "public-domain")],
                )
                propers.validate_translation_publication_binding(
                    row, propers.DEFAULT_ROOT, path
                )
        source_root = (
            ROOT
            / "src/sources/works/eugene-cummiskey/roman-missal-english-laity"
            / "editions/philadelphia-1861"
        )
        artifact_path = (
            source_root
            / "artifacts/common-marian-verified-en/common-marian-verified-en.tsv"
        )
        artifact = tomllib.loads(
            (artifact_path.parent / "artifact.toml").read_text(encoding="utf-8")
        )
        with artifact_path.open(encoding="utf-8", newline="") as handle:
            published = next(
                row
                for row in csv.DictReader(handle, delimiter="\t")
                if row["mass"] == "commune-festorum-bmv"
                and row["proper"] == "Gradual"
            )
        candidate = {
            "mass": published["mass"],
            "form_id": published["form_id"],
            "proper": published["proper"],
            "cycle": "all",
            "occurrence": 1,
            "artifact_id": (
                "artifact.eugene-cummiskey.roman-missal-english-laity."
                "philadelphia-1861.ia-scan-pdf"
            ),
            "passage_id": (
                "passage.eugene-cummiskey.roman-missal-english-laity."
                "philadelphia-1861.verify-commune-festorum-bmv-gradual"
            ),
            "ia_leaf_range": [515, 515],
            "publication_artifact_id": artifact["id"],
            "publication_artifact_sha256": artifact["sha256"],
            "publication_passage_id": (
                "passage.eugene-cummiskey.roman-missal-english-laity."
                "philadelphia-1861.publish-commune-festorum-bmv-gradual"
            ),
            "translations": [
                {
                    "lang": "en",
                    "rights": "public-domain",
                    "source_id": artifact["edition_id"],
                    "text": published["english"],
                }
            ],
        }
        propers.validate_translation_publication_binding(
            candidate, propers.DEFAULT_ROOT, path
        )

        partial = copy.deepcopy(candidate)
        partial.pop("publication_passage_id")
        with self.assertRaisesRegex(ValueError, "partial translation publication"):
            propers.validate_translation_publication_binding(
                partial, propers.DEFAULT_ROOT, path
            )

        stale = copy.deepcopy(candidate)
        stale["publication_artifact_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "artifact hash is stale"):
            propers.validate_translation_publication_binding(
                stale, propers.DEFAULT_ROOT, path
            )

        changed = copy.deepcopy(candidate)
        changed["translations"][0]["text"] += " changed"
        with self.assertRaisesRegex(ValueError, "body differs"):
            propers.validate_translation_publication_binding(
                changed, propers.DEFAULT_ROOT, path
            )

    def test_the_coverage_is_not_written_into_the_carried_block(self) -> None:
        """It belongs to a file this tool does not own, so it is reported only."""
        block = propers.render_census(propers.census(ROOT / "src" / "sources" / "calendars"))
        for row in propers.coverage(ROOT / "src" / "sources" / "calendars"):
            with self.subTest(calendar=row["calendar"]):
                self.assertNotIn("English orations", block)
                self.assertNotIn(f"{row['slots']} slots", block)


class LanguageCapabilityTests(unittest.TestCase):
    """Capability says what renders; it does not make a provenance claim."""

    @staticmethod
    def state(proper: dict, lang: str) -> dict:
        return {
            row["lang"]: row for row in propers.proper_language_capabilities(proper)
        }[lang]

    def test_requested_text_withheld_scripture_and_fallback_are_distinct(self) -> None:
        published = {
            "name": "Collect",
            "text": "Latin body",
            "translations": [{"lang": "en", "text": "English body"}],
        }
        self.assertEqual(self.state(published, "la")["status"], "full-text")
        self.assertEqual(self.state(published, "en")["status"], "full-text")

        restricted = {
            "name": "Collect",
            "latin": {"withheld": True},
            "unavailable_translations": [
                {"target": "Collect", "lang": "en", "state": "rights-restricted"}
            ],
        }
        self.assertEqual(self.state(restricted, "la")["status"], "unavailable")
        self.assertFalse(self.state(restricted, "la")["held"])
        self.assertFalse(self.state(restricted, "la")["available"])
        self.assertEqual(self.state(restricted, "la")["reason"], "text-withheld")
        self.assertEqual(self.state(restricted, "en")["status"], "rights-withheld")
        self.assertFalse(self.state(restricted, "en")["held"])
        self.assertFalse(self.state(restricted, "en")["available"])

        removed_latin = {
            "name": "Collect",
            "latin": {
                "target": "Collect",
                "state": "unavailable",
                "held": False,
                "available": False,
                "withheld": False,
            },
        }
        self.assertEqual(self.state(removed_latin, "la")["status"], "unavailable")
        self.assertFalse(self.state(removed_latin, "la")["held"])
        self.assertFalse(self.state(removed_latin, "la")["available"])
        self.assertIsNone(self.state(removed_latin, "la")["reason"])

        scripture = {
            "name": "Epistle",
            "source": "scripture",
            "citations": [{"ref": "Romans 1:1"}],
        }
        self.assertEqual(
            self.state(scripture, "en")["status"], "scripture-delegated"
        )
        fallback = {"name": "Collect", "text": "Latin body", "untranslated": True}
        self.assertEqual(self.state(fallback, "en")["status"], "fallback-latin")
        self.assertEqual(
            self.state(fallback, "en")["reason"]["kind"],
            "ledgered-untranslated",
        )
        self.assertFalse(self.state(fallback, "en")["held"])

        bodyless = {
            "name": "Collect",
            "text_status": {"state": "unavailable", "scope": "proper-body"},
            "untranslated": [{"lang": "en", "state": "unavailable"}],
        }
        self.assertEqual(self.state(bodyless, "en")["status"], "unavailable")
        self.assertEqual(
            self.state(bodyless, "en")["reason"]["kind"],
            "ledgered-untranslated",
        )
        self.assertFalse(self.state(bodyless, "en")["held"])

    def test_a_placeholder_is_absent_even_when_its_note_uses_text(self) -> None:
        placeholder = {
            "name": propers.PLACEHOLDER,
            "text": "This is a workflow note, not liturgical content.",
        }
        for row in propers.proper_language_capabilities(placeholder):
            self.assertEqual(row["status"], "absent")
            self.assertEqual(row["reason"], "placeholder")
            self.assertFalse(row["held"])

    def test_aggregate_rows_partition_every_unit_and_hold_only_full_text(self) -> None:
        units = [
            {"name": "Collect", "text": "Latin body"},
            {"name": "Epistle", "citations": [{"ref": "Romans 1:1"}]},
            {"name": "Secret", "incipit": "Incipit"},
            {"name": propers.PLACEHOLDER, "text": "Workflow note"},
        ]
        for unit in units:
            unit["languages"] = propers.proper_language_capabilities(unit)
        rows = propers.language_capability([{"propers": units}])
        counted = set(propers.LANGUAGE_STATUSES)
        for row in rows:
            with self.subTest(lang=row["lang"]):
                self.assertEqual(
                    row["units"],
                    sum(row[name.replace("-", "_")] for name in counted),
                )
                self.assertEqual(row["held"], row["full_text"] + row["withheld"])
                self.assertEqual(row["available"], row["full_text"])


class LatinRecensionCoverageTests(unittest.TestCase):
    """Residence, antecedence and direct target attestation remain separate."""

    def test_the_categories_are_mutually_exclusive_on_a_synthetic_calendar(self) -> None:
        def mass(key: str, proper: dict) -> dict:
            return {"key": key, "name": key, "propers": [proper]}

        document = {
            "calendar": "postconciliar",
            "sections": {
                "one": {
                    "kind": "seasonal",
                    "masses": [
                        mass("old", {"name": "Collect", "source": "composed", "text": "A"}),
                        mass("related", {"name": "Collect", "source": "composed", "text": "B"}),
                        mass("unrelated", {"name": "Collect", "source": "composed", "text": "C"}),
                        mass("incipit", {"name": "Collect", "source": "composed", "incipit": "D"}),
                        mass("absent", {"name": "Collect", "source": "composed"}),
                        mass("scripture", {"name": "Epistle", "source": "scripture", "verses": [{"ref": "Romans 1:1"}]}),
                        mass("placeholder", {"name": propers.PLACEHOLDER, "source": "composed", "text": "note"}),
                    ],
                }
            },
        }
        overlay = {
            ("old", "main", "Collect", "all", 1): {
                "antecedent_latin_here": "Older body"
            },
            ("related", "main", "Collect", "all", 1): {
                "ancient_witness": "Witness",
                "witness_edition_id": "edition.witness",
                "witness_artifact_id": "artifact.witness",
                "relation": "verbatim",
            },
            ("extra", "main", "Collect", "all", 1): {
                "verified_url": "English exemplar only"
            },
        }
        row = propers.latin_recension_coverage(document, overlay)
        self.assertEqual(row["slots"], 5)
        self.assertEqual(row["resident_bodies"], 3)
        self.assertEqual(row["antecedent_substitute_bodies"], 1)
        self.assertEqual(row["resident_bodies_with_antecedent_relation"], 1)
        self.assertEqual(row["resident_bodies_without_slot_relation"], 1)
        self.assertEqual(row["incipit_only"], 1)
        self.assertEqual(row["absent"], 1)
        self.assertEqual(row["unmatched_overlay_records"], 1)
        self.assertEqual(
            row["target_edition_artifact_attestation"], "not-represented"
        )

    def test_the_real_row_partitions_slots_without_claiming_target_attestation(self) -> None:
        row = propers.postconciliar_latin_coverage(
            ROOT / "src" / "sources" / "calendars"
        )
        self.assertIsNotNone(row)
        assert row is not None
        self.assertEqual(
            row["resident_bodies"],
            row["antecedent_substitute_bodies"]
            + row["resident_bodies_with_antecedent_relation"]
            + row["resident_bodies_without_slot_relation"],
        )
        self.assertEqual(
            row["slots"],
            row["resident_bodies"] + row["incipit_only"] + row["absent"],
        )
        self.assertEqual(
            row["target_edition_artifact_attestation"], "not-represented"
        )


class FindingAidCoverageTests(unittest.TestCase):
    """Structural resolution is a finding aid, never a whole-book assertion."""

    def test_raw_records_and_effective_occurrences_are_counted_apart(self) -> None:
        document = {
            "calendar": "demo",
            "sections": {
                "one": {
                    "kind": "seasonal",
                    "masses": [
                        {
                            "key": "source",
                            "propers": [
                                {"name": "Collect", "source": "composed", "text": "A"},
                                {"name": propers.PLACEHOLDER, "source": "composed", "text": "note"},
                            ],
                        },
                        {"key": "whole-ref", "takes_from": {"mass": "source"}},
                        {
                            "key": "proper-ref",
                            "propers": [
                                {"name": "Collect", "takes_from": {"mass": "source"}}
                            ],
                        },
                        {"key": "empty", "propers": []},
                    ],
                }
            },
        }
        row = propers.finding_aid_coverage(document)
        self.assertEqual(row["represented_masses"], 4)
        self.assertEqual(row["represented_proper_records"], 3)
        self.assertEqual(row["direct_proper_records"], 1)
        self.assertEqual(row["placeholder_proper_records"], 1)
        self.assertEqual(row["mass_reference_records"], 1)
        self.assertEqual(row["proper_reference_records"], 1)
        self.assertEqual(row["resolved_proper_occurrences"], 5)
        self.assertEqual(row["direct_resolved_occurrences"], 2)
        self.assertEqual(row["referenced_resolved_occurrences"], 3)
        self.assertEqual(row["effective_celebrations"], 4)
        self.assertEqual(row["masses_resolving_no_propers"], 1)
        self.assertEqual(row["resolution_errors"], [])

    def test_resolution_errors_name_the_mass_and_problem(self) -> None:
        document = {
            "calendar": "broken",
            "sections": {
                "one": {
                    "kind": "seasonal",
                    "masses": [
                        {"key": "lost", "takes_from": {"mass": "missing"}}
                    ],
                }
            },
        }
        row = propers.finding_aid_coverage(document)
        self.assertEqual(row["resolution_errors"][0]["mass"], "lost")
        self.assertIn("missing", " ".join(row["resolution_errors"][0]["problems"]))

    def test_a_recension_diff_is_not_reported_as_its_effective_projection(self) -> None:
        rows = {
            row["calendar"]: row
            for row in propers.finding_aid_coverages(
                ROOT / "src" / "sources" / "calendars"
            )
        }
        recension = rows["roman-pre-1955"]
        self.assertEqual(recension["effective_celebrations"], 490)
        self.assertEqual(rows["roman-1962"]["effective_celebrations"], 492)
        self.assertEqual(rows["postconciliar"]["effective_celebrations"], 619)
        self.assertLess(
            recension["represented_proper_records"],
            recension["resolved_proper_occurrences"],
        )
        self.assertEqual(
            recension["resolved_proper_occurrences"],
            recension["direct_resolved_occurrences"]
            + recension["referenced_resolved_occurrences"],
        )


class RegionTests(unittest.TestCase):
    def test_the_region_is_replaced_and_the_surrounding_prose_is_not(self) -> None:
        text = f"before\n\n{propers.CENSUS_BEGIN}\nold\n{propers.CENSUS_END}\n\nafter\n"
        rewritten = propers.replace_census(text, f"{propers.CENSUS_BEGIN}\nnew\n{propers.CENSUS_END}\n")
        self.assertEqual(rewritten, f"before\n\n{propers.CENSUS_BEGIN}\nnew\n{propers.CENSUS_END}\n\nafter\n")

    def test_a_document_without_markers_is_refused_rather_than_appended_to(self) -> None:
        with self.assertRaises(ValueError):
            propers.replace_census("no markers here\n", "block\n")

    def test_an_inverted_region_is_refused(self) -> None:
        text = f"{propers.CENSUS_END}\n{propers.CENSUS_BEGIN}\n"
        with self.assertRaises(ValueError):
            propers.replace_census(text, "block\n")


class CarriedBlockTests(unittest.TestCase):
    """The tracked documents, as they stand."""

    def region(self, relative: str) -> str:
        text = (ROOT / relative).read_text(encoding="utf-8")
        begin = text.index(propers.CENSUS_BEGIN)
        end = text.index(propers.CENSUS_END) + len(propers.CENSUS_END)
        return text[begin:end]

    def test_every_listed_document_carries_the_region_exactly_once(self) -> None:
        for relative in propers.CENSUS_DOCUMENTS:
            with self.subTest(document=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertEqual(text.count(propers.CENSUS_BEGIN), 1)
                self.assertEqual(text.count(propers.CENSUS_END), 1)

    def test_the_documents_carry_one_identical_block(self) -> None:
        regions = {relative: self.region(relative) for relative in propers.CENSUS_DOCUMENTS}
        self.assertEqual(len(set(regions.values())), 1, regions.keys())

    def test_the_carried_block_still_matches_the_calendars(self) -> None:
        """The same assertion `make check-propers-census` makes."""
        derived = propers.render_census(propers.census(ROOT / "src" / "sources" / "calendars"))
        for relative in propers.CENSUS_DOCUMENTS:
            with self.subTest(document=relative):
                self.assertEqual(self.region(relative) + "\n", derived)

    def test_no_listed_document_restates_a_figure_outside_the_block(self) -> None:
        """The whole defect: a total typed beside the table it came from.

        The key is a whole number standing on its own, not a substring. Plain
        containment was the key in use and it went red on 2026-08-02 for three
        totals, none of them a restatement: `0` inside `2008`, `6` inside `1962`,
        and `137` inside the citation `Psalm 118:137`. Nothing had been retyped —
        the corpus had simply moved until its totals collided with prose that was
        never a census figure, and a check that cries wolf at `1962` on a page
        about the 1962 Missal is a check nobody can act on.

        So a match must not be flanked by a digit, and must not follow a colon,
        which is a chapter-verse citation and never a count. A restated total
        reads `491 masses` or `there are 269`, and is still caught.

        SHORT TOTALS ARE NOT CHECKED, and this is a stated floor rather than a
        proof. A one- or two-digit total is indistinguishable from ordinary prose
        in these documents — `Y mod 3 = 0` is Year C, `Malachi 4:1-6`, `ot-6`, a
        numbered list item — and no rule over the digits alone separates them
        from a retyped count. The figures actually retyped in the incident this
        test exists for were three-digit ones (a sanctoral section stated as 247
        against a file holding 307), so the guard is kept where it discriminates
        and is declared absent where it does not.
        """
        import re

        shortest = 3
        totals = {
            str(counted[key])
            for counted in propers.census(ROOT / "src" / "sources" / "calendars").values()
            for key in ("masses", "propers", "placeholder_only_masses", "substantive_propers")
        }
        for relative in propers.CENSUS_DOCUMENTS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            outside = text.replace(self.region(relative), "")
            for total in sorted(totals):
                with self.subTest(document=relative, total=total):
                    if len(total) < shortest:
                        self.skipTest(f"{total} is too short to tell from prose")
                    # The second lookbehind is for comma-grouped thousands.
                    # `(?<![\d:])` alone accepts a comma as a left boundary, so
                    # prose reading "rewrote 4,269 lines" was reported as a
                    # restatement of the census total 269 -- a figure about a
                    # diff, sharing three digits with a count of masses. A
                    # detector that cries wolf on ordinary prose gets silenced,
                    # which costs more than the collision it caught.
                    found = re.search(
                        rf"(?<![\d:])(?<!\d,){re.escape(total)}(?!\d)", outside
                    )
                    self.assertIsNone(
                        found,
                        f"{relative} restates the census total {total}: "
                        f"...{outside[max(0, found.start() - 60):found.start() + 30]}..."
                        if found
                        else "",
                    )


if __name__ == "__main__":
    unittest.main()
