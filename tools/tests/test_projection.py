"""The projection derives rules, and writes none where an edition agrees.

`guidance/versification.md` §8.0 settles the shape. These tests assert the three
properties that make it worth having, one that the first implementation got
wrong, and — since the resolver now reads its alias rules through the projection
— that every registered edition can actually be projected.

Which editions exist, where their artifacts are, and what numbering each is in
are all read from `index-bible`'s registry rather than named here. A second list
of editions beside the registry is the fault this whole apparatus exists to
prevent, and a test carrying one would go green against the wrong file.
"""
from __future__ import annotations

import sys
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import _projection  # noqa: E402


def load_tool(name: str):
    path = REPOSITORY_ROOT / "tools" / name
    loader = SourceFileLoader(f"_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


index_bible = load_tool("index-bible")
WORKS = REPOSITORY_ROOT / "src/sources/works"


def edition_root(name: str) -> Path:
    """Where the registry says this edition's artifacts are, one directory up."""
    return (WORKS / str(index_bible.EDITIONS[name]["artifacts"])).parent


def tracked() -> list[str]:
    """The registered editions whose artifacts are in this checkout.

    Everything registered but licensed lives outside the repository and is
    reached with `--source-root`; nothing else may be missing, and
    `test_only_a_licensed_edition_is_out_of_reach` holds that line so that a
    misfiled artifact directory cannot quietly shrink this list to nothing.
    """
    return sorted(
        name
        for name in index_bible.EDITIONS
        if (edition_root(name) / "artifacts").is_dir()
    )


DOUAY = edition_root("douay-rheims")
CLEMENTINE = edition_root("clementine-vulgate")


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

    def test_an_edition_in_the_canonical_numbering_may_still_renumber(self) -> None:
        """Declaring a numbering is not the same as printing it.

        This test asserted the opposite until 2026-07-31, on the Clementine, and
        the Clementine was the edition it was least true of: it declares
        `vulgate` and restarts Psalms 115 and 147 at verse 1, so nineteen verses
        answer to different numbers there and `Bible.verse('Ps', 115, 10)`
        returned the last verse of the psalm. Identity still writes nothing —
        which is why the Douay, whose printed psalter is the one the numbering is
        read from, renumbers nowhere.
        """
        douay = _projection.divergence(_projection.project(DOUAY, "vulgate"))
        self.assertEqual(douay["renumber"], 0)
        clementine = _projection.divergence(_projection.project(CLEMENTINE, "vulgate"))
        self.assertEqual(clementine["renumber"], 19)
        self.assertGreater(clementine["total"], clementine["displaced"])

    def test_a_projection_measures_distance_from_the_canon(self) -> None:
        """A Vulgate-numbered edition costs tens of rules; a Hebrew one thousands."""
        vulgate = _projection.divergence(_projection.project(DOUAY, "vulgate"))
        self.assertLess(vulgate["total"], 100)
        self.assertGreater(vulgate["merge"], 0)

    def test_a_refusal_never_resolves_to_anything(self) -> None:
        """`absent`, `unrecorded`, `displaced` and `split` say where the text is not."""
        for root in (DOUAY, CLEMENTINE):
            for row in _projection.project(root, "vulgate"):
                if row.kind in _projection.REFUSING:
                    self.assertEqual(row.resolves_to, "", row)

    def test_every_row_carries_a_known_override(self) -> None:
        for row in _projection.project(DOUAY, "vulgate"):
            self.assertIn(row.kind, _projection.OVERRIDES, row)

    def test_an_unmapped_alias_kind_raises_rather_than_defaulting(self) -> None:
        """A new alias kind must be given a meaning, not silently bucketed."""
        self.assertNotIn("some-new-kind", _projection.ALIAS_KINDS)
        for meaning in _projection.ALIAS_KINDS.values():
            self.assertIn(meaning, _projection.OVERRIDES)


class EveryEditionProjectsTest(unittest.TestCase):
    """The gate: an edition nobody can project is an edition nobody can resolve.

    `index-bible` now reads its alias rules through `_projection`, so a
    projection that will not derive stops that edition's build. These run the
    same derivation over the whole registry, which the per-edition build cannot
    do, so a table that breaks an edition nothing happened to rebuild is still
    caught.
    """

    def test_only_a_licensed_edition_is_out_of_reach(self) -> None:
        """Guards every other test here against passing on an empty list."""
        missing = sorted(set(index_bible.EDITIONS) - set(tracked()))
        self.assertEqual(
            missing,
            sorted(
                name
                for name, edition in index_bible.EDITIONS.items()
                if edition["rights"] == "licensed"
            ),
        )
        self.assertGreater(len(tracked()), 1)

    def test_every_tracked_edition_derives_a_projection(self) -> None:
        for name in tracked():
            with self.subTest(edition=name):
                rows = _projection.project(
                    edition_root(name), str(index_bible.EDITIONS[name]["numbering"])
                )
                counts = _projection.divergence(rows)
                self.assertEqual(counts["total"], len(rows))

    def test_a_total_is_the_sum_of_its_parts_and_not_a_constant(self) -> None:
        """Two editions may total the same; none may total a number nothing made.

        The King James and the Revised Version both come to 4313 and differ
        inside it, so equality across editions proves nothing either way. What
        does is that each total decomposes into the four derivations that
        produced it — which the `displaced=3` bug would have failed, because it
        made one part the same for everyone.
        """
        for name in tracked():
            numbering = str(index_bible.EDITIONS[name]["numbering"])
            with self.subTest(edition=name):
                aliases = _projection.alias_rows(edition_root(name))
                psalms = _projection.psalm_rows(numbering)
                displaced = _projection.displaced_psalms()
                psalter = _projection.psalter_rows(edition_root(name), numbering)
                self.assertEqual(
                    len(_projection.project(edition_root(name), numbering)),
                    len(aliases) + len(psalms) + len(displaced) + len(psalter),
                )
                self.assertEqual(bool(psalms), numbering != _projection.CANONICAL)

    def test_the_resolver_and_the_projection_read_one_table(self) -> None:
        """`Bible.aliases` is the projection's alias rules, not a second parse."""
        for name in tracked():
            with self.subTest(edition=name):
                root = edition_root(name)
                table = _projection.alias_table(root)
                rows = _projection.alias_rows(root)
                self.assertEqual(len(table), len(rows))
                bible = index_bible.Bible(root / "artifacts")
                self.assertEqual(bible.aliases, table)
                for row in rows:
                    cited = _projection.point(row.cited_locus, name)
                    if row.kind in ("absent", "unrecorded"):
                        self.assertIsNone(table[cited], row)
                    else:
                        self.assertIsNotNone(table[cited], row)

    def test_an_edition_with_no_alias_artifact_is_refused_not_assumed_empty(self) -> None:
        """An absent departure table and a forgotten one read exactly alike."""
        with self.assertRaises(_projection.ProjectionError):
            _projection.alias_table(REPOSITORY_ROOT / "src/sources/works")


if __name__ == "__main__":
    unittest.main()
