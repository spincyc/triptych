"""The projection derives rules, and writes none where an edition agrees.

`guidance/versification.md` §8.0 settles the shape. These tests assert the three
properties that make it worth having, and one that the first implementation got
wrong.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import _projection  # noqa: E402


DOUAY = (
    REPOSITORY_ROOT
    / "src/sources/works/english-college-of-douay/douay-rheims-bible"
    / "editions/challoner-gutenberg-1581"
)
CLEMENTINE = (
    REPOSITORY_ROOT
    / "src/sources/works/catholic-church/vulgata-clementina/editions/ebible-latvuc"
)


class ProjectionTest(unittest.TestCase):
    def test_the_displaced_psalms_are_counted_from_the_table(self) -> None:
        """Sixteen, derived — not the length of the string "yes".

        The first implementation wrote `sorted(_psalms.ENGLISH_UNIFORM)`, which
        is the column's affirmative value and not a collection of psalms, so it
        yielded three letters and reported `displaced=3` for every edition. A
        plausible number, identical across seven editions, and wrong. This test
        exists so the next reader cannot reintroduce it.
        """
        flagged = _projection._non_uniform_psalms()
        self.assertEqual(len(flagged), 16)
        self.assertEqual(
            flagged, [2, 4, 13, 20, 29, 43, 44, 53, 56, 72, 100, 109, 126, 136, 146, 150]
        )
        self.assertTrue(all(isinstance(psalm, int) for psalm in flagged))

    def test_an_edition_in_the_canonical_numbering_needs_no_renumbering(self) -> None:
        """Identity writes nothing, which is what keeps a projection small."""
        rows = _projection.project(CLEMENTINE, "vulgate")
        counts = _projection.divergence(rows)
        self.assertEqual(counts["renumber"], 0)
        self.assertEqual(counts["total"], counts["displaced"])

    def test_a_projection_measures_distance_from_the_canon(self) -> None:
        """A Vulgate-numbered edition costs tens of rules; a Hebrew one thousands."""
        vulgate = _projection.divergence(_projection.project(DOUAY, "vulgate"))
        self.assertLess(vulgate["total"], 100)
        self.assertGreater(vulgate["merge"], 0)

    def test_a_refusal_never_resolves_to_anything(self) -> None:
        """`absent`, `unrecorded` and `displaced` say where the text is not."""
        for row in _projection.project(DOUAY, "vulgate"):
            if row.kind in ("absent", "unrecorded", "displaced"):
                self.assertEqual(row.resolves_to, "", row)

    def test_every_row_carries_a_known_override(self) -> None:
        for row in _projection.project(DOUAY, "vulgate"):
            self.assertIn(row.kind, _projection.OVERRIDES, row)

    def test_an_unmapped_alias_kind_raises_rather_than_defaulting(self) -> None:
        """A new alias kind must be given a meaning, not silently bucketed."""
        self.assertNotIn("some-new-kind", _projection.ALIAS_KINDS)
        for meaning in _projection.ALIAS_KINDS.values():
            self.assertIn(meaning, _projection.OVERRIDES)


if __name__ == "__main__":
    unittest.main()
