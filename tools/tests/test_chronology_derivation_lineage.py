#!/usr/bin/env python3
"""Corpus-specific lineage invariants for chronology derivations."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _chronology as chronology  # noqa: E402


class DerivationLineageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.corpus = chronology.load(ROOT / "src/sources/chronology")

    def test_maas_auc_derivations_name_the_single_claim_calibration(self) -> None:
        anchor_id = "chronology.maas-auc-782-ad-29-calibration"
        anchor = self.corpus.events[anchor_id]
        self.assertEqual(len(anchor.claims), 1)
        self.assertEqual(anchor.claims[0].date.label, "A.U.C. 782 = A.D. 29")

        for event_id in (
            "life-of-christ.raising-of-the-widows-son-at-naim",
            "life-of-christ.bread-of-life-discourse-at-capharnaum",
        ):
            with self.subTest(event=event_id):
                event = self.corpus.events[event_id]
                self.assertEqual(len(event.claims), 1)
                self.assertEqual(
                    event.claims[0].date.derivation["inputs"], [anchor_id]
                )


if __name__ == "__main__":
    unittest.main()
