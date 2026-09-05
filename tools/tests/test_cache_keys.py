#!/usr/bin/env python3
"""A cache key must cover every tree its derivation reads.

The disk caches under `build/` all work the same way: a derivation is expensive,
its inputs are tracked files, and the key is a `tree_fingerprint` of those
files. The failure mode is not that a cache is slow or missing. It is that the
key covers less than the derivation reads, so an edit the derivation would have
noticed leaves the cache answering from before it.

That happened here. `_source_library_records` keys on `src/sources`, but the
library it projects also reads `src/gpt` and `src/claude` for publication
bindings. A binding added under a publication root left the cache serving the
registry from before it, and a ledger row naming the new artifact came back
"is not registered" --- a stale answer wearing the costume of a real finding,
which is the one defect `guidance/the-shape.md` says this repository exists to
refuse.

These tests are the guard. Each builds a sandbox with all three roots, takes
the cache key, changes one file under one root, and requires the key to move.
A key that ignores a root fails here rather than in whichever tool next asks it
a question.
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _proper_latin  # noqa: E402
from _tooling import tree_fingerprint  # noqa: E402

# The roots `source-library.load_library` reads, and therefore the roots every
# derivation over it must be keyed by.
LIBRARY_ROOTS = ("src/sources", "src/gpt", "src/claude")


def sandbox_repository(where: Path) -> Path:
    """A repository shaped enough for a cache key: all three roots, one file each."""
    for relative in LIBRARY_ROOTS:
        directory = where / relative
        directory.mkdir(parents=True)
        (directory / "record.toml").write_text("id = 'one'\n", encoding="utf-8")
    return where


class TreeFingerprintTests(unittest.TestCase):
    """The primitive every key is built from."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = sandbox_repository(Path(self.tmp.name))
        self.roots = [self.repo / relative for relative in LIBRARY_ROOTS]

    def test_the_same_tree_fingerprints_the_same_way_twice(self) -> None:
        """Otherwise the cache it guards would never hit."""
        first, counted = tree_fingerprint(self.roots)
        again, again_counted = tree_fingerprint(self.roots)
        self.assertEqual(first, again)
        self.assertEqual(counted, again_counted)
        self.assertEqual(counted, len(LIBRARY_ROOTS))

    def test_changed_content_moves_the_fingerprint(self) -> None:
        for relative in LIBRARY_ROOTS:
            with self.subTest(root=relative):
                before, _ = tree_fingerprint(self.roots)
                target = self.repo / relative / "record.toml"
                target.write_text("id = 'two'\n", encoding="utf-8")
                self.assertNotEqual(
                    before, tree_fingerprint(self.roots)[0],
                    f"an edit under {relative} left the fingerprint standing")

    def test_a_new_file_moves_the_fingerprint(self) -> None:
        before, _ = tree_fingerprint(self.roots)
        (self.repo / "src/gpt" / "added.toml").write_text("id = 'x'\n", encoding="utf-8")
        self.assertNotEqual(before, tree_fingerprint(self.roots)[0])


class SourceLibraryRecordsKeyTests(unittest.TestCase):
    """`_proper_latin`'s projection is keyed by everything the library reads."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = sandbox_repository(Path(self.tmp.name))
        # The floor exists so a throwaway sandbox is never cached; this test is
        # about the key, so it is lowered for the length of the test only.
        original = _proper_latin.SOURCE_LIBRARY_CACHE_FLOOR
        _proper_latin.SOURCE_LIBRARY_CACHE_FLOOR = 0
        self.addCleanup(
            setattr, _proper_latin, "SOURCE_LIBRARY_CACHE_FLOOR", original)

    def key(self) -> Path | None:
        return _proper_latin._source_library_cache_entry(self.repo)

    def test_every_root_the_library_reads_is_in_the_key(self) -> None:
        """The regression this file exists for: `src/gpt` was not in it."""
        for relative in LIBRARY_ROOTS:
            with self.subTest(root=relative):
                before = self.key()
                self.assertIsNotNone(before)
                (self.repo / relative / "record.toml").write_text(
                    f"id = 'changed-{relative}'\n", encoding="utf-8")
                self.assertNotEqual(
                    before, self.key(),
                    f"a change under {relative} did not move the cache key, so "
                    f"the cache would answer from before it")

    def test_an_unchanged_tree_keeps_its_key(self) -> None:
        self.assertEqual(self.key(), self.key())

    def test_the_floor_keeps_a_small_tree_out_of_the_cache(self) -> None:
        _proper_latin.SOURCE_LIBRARY_CACHE_FLOOR = 10_000
        self.assertIsNone(self.key())


if __name__ == "__main__":
    unittest.main()
