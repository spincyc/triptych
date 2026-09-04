"""The Latin body damage screen, and the false positives that shaped it."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from _latin_body_damage import body_damage  # noqa: E402


class DamageIsRefused(unittest.TestCase):
    """Each case is a string a lane actually stored as a publishable body."""

    def test_accent_read_as_digit_or_currency(self):
        for word in ("D6minum", "parit£rque", "cael6stis", "mund6mur"):
            self.assertIn(word, body_damage(f"et {word} nostrum"), word)

    def test_ae_ligature_read_as_se_or_x(self):
        for word in ("qusesumus", "quxsumus", "beatse"):
            self.assertIn(word, body_damage(f"Deus, {word} tuam"), word)

    def test_u_read_as_ii_before_a_consonant(self):
        for word in ("potiique", "siipplices", "commiinio"):
            self.assertIn(word, body_damage(f"nos {word} tui"), word)

    def test_two_words_welded_across_a_break(self):
        self.assertIn("IoannemOr", body_damage("beatum IoannemOr apostolum"))

    def test_a_wholly_mangled_opening(self):
        found = body_damage("eus > *l u keato Petro Apostolo tuo")
        self.assertTrue(found)

    def test_a_control_character_is_refused(self):
        # A page separator carried into a provenance note once made the whole
        # TOML ledger unreadable, surfacing as one proper's "missing entry".
        found = body_damage("Domine\x0cquaesumus")
        self.assertTrue(any("control characters" in one for one in found))


class LegitimateTextSurvives(unittest.TestCase):
    """Every case here is a real body the screen once wrongly refused."""

    def test_a_clean_oration(self):
        self.assertEqual(
            [],
            body_damage(
                "Custodi, Domine, quaesumus, Ecclesiam tuam propitiatione "
                "perpetua: et quia sine te labitur humana mortalitas; tuis "
                "semper auxiliis et abstrahatur a noxiis, et ad salutaria "
                "dirigatur. Per Dominum."
            ),
        )

    def test_ablative_plurals_in_iis(self):
        self.assertEqual(
            [], body_damage("praesidiis obsequiis insidiis gladiis gaudiis remedii")
        )

    def test_ordinary_short_words(self):
        # A length rule for split words refused all of these, and one lane's
        # finalizer had already deleted several from a body on that reasoning.
        self.assertEqual([], body_damage("cor ego mea da ita fac es est qui O"))

    def test_the_pluperfect_subjunctive(self):
        self.assertEqual([], body_damage("cum audisset et fecisset atque venisset"))

    def test_a_printed_citation_inside_a_chant_body(self):
        self.assertEqual(
            [],
            body_damage(
                "Salus populi ego sum, dicit Dominus. Ps. 77, 1 Attendite, "
                "popule meus, legem meam."
            ),
        )

    def test_the_missal_asks_and_exclaims(self):
        self.assertEqual([], body_damage("Quare, Domine, irasceris in populo tuo?"))
        self.assertEqual([], body_damage("Quam dilecta tabernacula tua, Domine virtutum!"))

    def test_liturgical_marks_and_quotation(self):
        self.assertEqual([], body_damage("Gloria, laus / et honor + tibi «Hosanna» ℣. ℟."))


if __name__ == "__main__":
    unittest.main()
