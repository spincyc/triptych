"""Recover edition-native readings without widening a joined source verse."""
from functools import lru_cache
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _loci


@lru_cache(maxsize=1)
def register():
    loader = SourceFileLoader("_source_join_index", str(ROOT / "tools/index-bible"))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


@lru_cache(maxsize=None)
def bible(name):
    index = register()
    return index.Bible(index.SOURCE_ROOT / index.EDITIONS[name]["artifacts"])


def reader(name):
    return next(item for item in _loci.edition_readers() if item.id == name)


class NativeSourceJoinTests(unittest.TestCase):
    def test_hosea_return_reading_includes_all_nine_native_verses(self):
        for name in ("world-english-bible-catholic", "king-james-version", "revised-version-1895"):
            with self.subTest(edition=name):
                loci, reason = _loci.placed(reader(name), "Os", [{"chapter": 14, "first": 2, "last": 10}])
                self.assertEqual(reason, "")
                self.assertEqual(loci, [{"chapter": 14, "first": 1, "last": 9}])
                self.assertEqual(bible(name).carrier("Os", 14, 1), ("Os", 13, 16))

    def test_dra_sleeping_brethren_reading_recovers_its_native_opening(self):
        loci, reason = _loci.placed(reader("douay-rheims-american-1899"), "1Thess", [
            {"chapter": 4, "first": 13, "last": 18}])
        self.assertEqual(reason, "")
        self.assertEqual(loci, [{"chapter": 4, "first": 12, "last": 17}])

    def test_second_thessalonians_keeps_the_discontinuous_appointment(self):
        for name in ("douay-rheims-american-1899", "catholic-public-domain-version"):
            with self.subTest(edition=name):
                loci, reason = _loci.placed(reader(name), "2Thess", [
                    {"chapter": 2, "first": 1, "last": 3},
                    {"chapter": 2, "first": 14, "last": 17}])
                self.assertEqual(reason, "")
                self.assertEqual(loci, [
                    {"chapter": 2, "first": 1, "last": 3},
                    {"chapter": 2, "first": 13, "last": 16}])

    def test_a_joined_native_verse_never_reads_as_an_exact_point(self):
        for name, token, chapter, first, last in (
            ("douay-rheims-american-1899", "1Thess", 4, 11, 12),
            ("douay-rheims-american-1899", "2Thess", 2, 10, 11),
            ("catholic-public-domain-version", "2Thess", 2, 10, 11),
        ):
            for low, high in ((first, first), (last, last), (first, last)):
                with self.subTest(edition=name, token=token, low=low, high=high):
                    loci, reason = _loci.placed(reader(name), token, [
                        {"chapter": chapter, "first": low, "last": high}])
                    self.assertEqual(loci, [])
                    self.assertIn("no exact selection recorded", reason)

    def test_cpdv_first_thessalonians_does_not_inherit_a_douay_shift(self):
        native = [{"chapter": 4, "first": 13, "last": 18}]
        self.assertEqual(_loci.placed(reader("catholic-public-domain-version"), "1Thess", native), (native, ""))

    def test_whole_hosea_chapter_retains_the_previous_native_chapter_end(self):
        for name in ("world-english-bible-catholic", "king-james-version", "revised-version-1895"):
            with self.subTest(edition=name):
                self.assertEqual(_loci.placed(reader(name), "Os", [
                    {"chapter": 14, "first": None, "last": None}]), ([
                    {"chapter": 13, "first": 16, "last": 16},
                    {"chapter": 14, "first": 1, "last": 9}], ""))

    def test_bible_resolver_reads_held_native_bodies_without_rewriting(self):
        for name, token, chapter, low, high, native_low, native_high in (
            ("world-english-bible-catholic", "Os", 14, 2, 10, 1, 9),
            ("king-james-version", "Os", 14, 2, 10, 1, 9),
            ("revised-version-1895", "Os", 14, 2, 10, 1, 9),
            ("douay-rheims-american-1899", "1Thess", 4, 13, 18, 12, 17),
            ("douay-rheims-american-1899", "2Thess", 2, 14, 17, 13, 16),
            ("catholic-public-domain-version", "2Thess", 2, 14, 17, 13, 16),
        ):
            with self.subTest(edition=name, token=token):
                native = bible(name)
                text, reason = native.passage(token, [{
                    "begin": {"chapter": chapter, "verse": low},
                    "end": {"chapter": chapter, "verse": high}}])
                self.assertEqual(reason, "")
                self.assertEqual(text, " ".join(native.verses[(token, chapter, verse)]
                    for verse in range(native_low, native_high + 1)))


    def test_direct_whole_hosea_uses_the_complete_recorded_cited_domain(self):
        for name in ("world-english-bible-catholic", "king-james-version", "revised-version-1895"):
            with self.subTest(edition=name):
                native = bible(name)
                text, reason = native.passage("Os", [{
                    "begin": {"chapter": 14}, "end": {"chapter": 14}}])
                self.assertEqual(reason, "")
                self.assertIn(("Os", 14), native.open_bounds)
                self.assertEqual(native.open_bounds[("Os", 14)], (1, 10))
                expected = [native.verses[("Os", 13, 16)]]
                expected.extend(native.verses[("Os", 14, verse)] for verse in range(1, 10))
                self.assertEqual(text, " ".join(expected))

    def test_partial_cross_book_rows_do_not_claim_complete_open_bounds(self):
        from unittest.mock import patch
        index = register()
        # Three printed verses exist; the aliases cover only the first two,
        # plus one verse in another book. The missing third carrier prevents
        # treating cited 10--12 as the whole native chapter's domain.
        verses = {("Native", 1, 1): "first", ("Native", 1, 2): "second",
            ("Native", 1, 3): "last", ("Other", 2, 7): "elsewhere"}
        aliases = {("Native", 1, 10): ("Other", 2, 7),
            ("Native", 1, 11): ("Native", 1, 1),
            ("Native", 1, 12): ("Native", 1, 2)}
        with patch.object(index, "load_books", return_value={}), \
             patch.object(index, "load_verses", return_value=verses), \
             patch.object(index, "load_aliases", return_value=aliases), \
             patch.object(index, "alias_rows", return_value=[]):
            native = index.Bible(ROOT)
        self.assertNotIn(("Native", 1), native.open_bounds)
        self.assertEqual(native.chapters[("Native", 1)], (1, 3))


if __name__ == "__main__":
    unittest.main()
