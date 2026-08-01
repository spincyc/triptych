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

        Checked against the totals only. A stray four-digit number elsewhere in
        the prose is not necessarily a census figure, but a document's own
        totals appearing outside its own block always is.
        """
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
                    self.assertNotIn(total, outside)


if __name__ == "__main__":
    unittest.main()
