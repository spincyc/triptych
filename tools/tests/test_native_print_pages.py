"""Public native-print admission and native artwork selection."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _native_print as native
import _native_print_artwork as artwork


class AdmissionTests(unittest.TestCase):
    def test_admission_inputs_name_every_declaration_and_disposition(self):
        inputs = native.admission_inputs(ROOT)
        for row in native._admitted_recipes(ROOT):
            if row["family"] == "publication":
                self.assertIn("release/publications/" + row["provider"] + "/" + row["document"] + ".json", inputs)
                self.assertIn("src/" + row["provider"] + "/" + row["canonical"] + "/web-edition.toml", inputs)
        held = [path.relative_to(ROOT).as_posix() for path in (ROOT / "release/publications").glob("*/**/*.json")
                if json.loads(path.read_bytes()).get("status") == "hold"]
        self.assertTrue(set(held) <= set(inputs))
        self.assertTrue(all((ROOT / path).is_file() for path in inputs))

    def test_holds_and_withdrawals_are_not_admitted_and_bibles_are(self):
        documents = native.admitted_documents(ROOT)
        families = {identity.partition(":")[0] for identity in documents}
        self.assertEqual(families, {"publication", "bible", "papal", "reading-plan"})
        recipes = native._admitted_recipes(ROOT)
        self.assertEqual({row["id"] for row in recipes},
                         {identity for identity in documents if identity.startswith(("publication:", "bible:"))})
        for path in (ROOT / "release/publications").glob("*/**/*.json"):
            record = json.loads(path.read_bytes())
            provider = path.relative_to(ROOT / "release/publications").parts[0]
            if record.get("status") == "hold":
                self.assertNotIn("publication:" + provider + "/" + record["id"], documents)
        for path in ROOT.glob("src/*/**/web-edition.toml"):
            if tomllib.loads(path.read_text(encoding="utf-8")).get("withdrawn"):
                provider = path.relative_to(ROOT / "src").parts[0]
                leaf = path.parent.relative_to(ROOT / "src" / provider).as_posix()
                self.assertFalse(any(row["document"] == "publication:" + provider + "/" + leaf
                                     for row in documents.values()))


class ArtworkSelectionTests(unittest.TestCase):
    def test_dictionary_editions_select_owned_raster_artwork_only(self):
        owner = "src/gpt/" + artwork.DICTIONARY + "/"
        every = {path.relative_to(ROOT).as_posix() for path in (ROOT / owner).rglob("*.png")}
        for leaf in artwork.DICTIONARY_LEAVES:
            with self.subTest(leaf=leaf):
                selected, inputs = artwork.dictionary_artwork(ROOT, "gpt", artwork.DICTIONARY + "/" + leaf)
                self.assertTrue(selected)
                self.assertLess(len(selected), len(every))
                self.assertTrue(all(path.startswith(owner) and (ROOT / path).is_file() for path in selected))
                self.assertIn(owner + leaf + "/main.tex", inputs)
                self.assertIn(artwork.HELPER, inputs)
        with self.assertRaises(artwork.ArtworkError):
            artwork.dictionary_artwork(ROOT, "gpt", artwork.DICTIONARY + "/unknown")

    def test_server_guides_select_pencil_plates_through_active_diagrams_and_cards_none(self):
        pencil = re.compile(r"src/gpt/" + re.escape(artwork.SERVER) + r"/shared/artwork/pencil/[A-Za-z0-9._-]+\.png")
        for leaf in ("01-low-mass", "01-low-mass-trainer-manual", "02-missa-cantata", "03-solemn-mass"):
            with self.subTest(leaf=leaf):
                selected, inputs = artwork.server_artwork(ROOT, "gpt", artwork.SERVER + "/" + leaf)
                self.assertTrue(selected)
                self.assertTrue(all(pencil.fullmatch(path) for path in selected))
                self.assertIn("src/gpt/" + artwork.SERVER + "/" + leaf + "/main.tex", inputs)
        for leaf in ("01-low-mass-flash-cards", "02-missa-cantata-cue-cards", "03-solemn-mass-cue-cards"):
            with self.subTest(leaf=leaf):
                self.assertEqual(artwork.server_artwork(ROOT, "gpt", artwork.SERVER + "/" + leaf),
                                 (set(), {artwork.HELPER}))
        every = set((ROOT / "src/gpt" / artwork.SERVER / "shared/artwork/pencil").glob("*.png"))
        sung, _ = artwork.server_artwork(ROOT, "gpt", artwork.SERVER + "/02-missa-cantata")
        self.assertLess(len(sung), len(every))


if __name__ == "__main__":
    unittest.main()
