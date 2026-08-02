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

import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

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
                    row["with_english"] + row["ledgered_untranslated"] + row["unaccounted"],
                    row["slots"],
                )

    def test_the_coverage_is_not_written_into_the_carried_block(self) -> None:
        """It belongs to a file this tool does not own, so it is reported only."""
        block = propers.render_census(propers.census(ROOT / "src" / "sources" / "calendars"))
        for row in propers.coverage(ROOT / "src" / "sources" / "calendars"):
            with self.subTest(calendar=row["calendar"]):
                self.assertNotIn("English orations", block)
                self.assertNotIn(f"{row['slots']} slots", block)


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
                    found = re.search(rf"(?<![\d:]){re.escape(total)}(?!\d)", outside)
                    self.assertIsNone(
                        found,
                        f"{relative} restates the census total {total}: "
                        f"...{outside[max(0, found.start() - 60):found.start() + 30]}..."
                        if found
                        else "",
                    )


if __name__ == "__main__":
    unittest.main()
