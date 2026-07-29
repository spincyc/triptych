#!/usr/bin/env python3
"""Structural checks for terminal Alpha matter in altar-server card decks."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
GUIDES = (
    ROOT
    / "src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides"
)


class ServerCardAlphaApparatusTest(unittest.TestCase):
    def test_shared_terminal_explains_alpha_and_preserves_deck_boundary(self):
        text = (GUIDES / "shared/server-guide-format.tex").read_text()
        apparatus = text.split(
            r"\newcommand{\CardCompanionTerminalApparatus}", 1
        )[1]
        self.assertIn("Alpha names the review gate", apparatus)
        self.assertIn("not mean final, complete, official", apparatus)
        self.assertIn("Safe use", apparatus)
        self.assertIn("Rights", apparatus)
        self.assertIn("not part of the cut grid", apparatus)
        self.assertIn(r"\clearpage", apparatus)

    def test_only_companions_with_an_approved_terminal_sheet_render_it(self):
        paths = (
            "01-low-mass-flash-cards/main.tex",
            "02-missa-cantata-cue-cards/main.tex",
        )
        for relative in paths:
            with self.subTest(relative=relative):
                text = (GUIDES / relative).read_text()
                self.assertEqual(
                    text.count(r"\CardCompanionTerminalApparatus"), 1
                )

        solemn = (
            GUIDES / "03-solemn-mass-cue-cards/main.tex"
        ).read_text()
        self.assertNotIn(r"\CardCompanionTerminalApparatus", solemn)
        self.assertIn(r"\CardCompanionRightsNotice", solemn)

    def test_card_grid_sources_are_not_changed_into_explanatory_pages(self):
        for relative in (
            "shared/missa-cantata-action-cards.tex",
            "shared/solemn-action-cards.tex",
        ):
            with self.subTest(relative=relative):
                text = (GUIDES / relative).read_text()
                self.assertNotIn("Alpha names the review gate", text)


if __name__ == "__main__":
    unittest.main()
