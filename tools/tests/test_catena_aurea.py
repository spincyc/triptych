"""Boundary tests for the offline Catena Aurea extraction recipe."""

import importlib.util
import json
import tomllib

import yaml
from pathlib import Path
import unittest

SPEC = importlib.util.spec_from_file_location(
    "catena_aurea", Path(__file__).resolve().parents[2] / "scripts/_catena_aurea.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class CatenaAureaTests(unittest.TestCase):
    def test_markup_tails_attributions_and_uncertain_labels_survive(self):
        raw = b'''<ThML><ThML.head>modern wrapper</ThML.head><ThML.body>
        <div2 title="Chapter 1"><p class="scripture" id="a">1. A <i>word</i>.</p>
        <p class="scripture" id="b">2-3. More.</p>
        <p class="normal" id="c">Bede: The <pb n="5"/> text.</p>
        <p class="scripture" id="d">l. Uncertain.</p>
        <p class="normal" id="e">Pseudo-Jerome: Another.</p></div2>
        <div2 title="Index"><p>modern index</p></div2></ThML.body></ThML>'''
        text, index = MODULE.extract(raw, "Mark", 1)
        self.assertEqual(text.decode(), "Chapter 1\n1. A word.\n2-3. More.\nBede: The text.\nl. Uncertain.\nPseudo-Jerome: Another.\n")
        self.assertEqual(index["blocks"][0]["native_verse_labels"], [[1, 1], [2, 3]])
        self.assertEqual(index["blocks"][0]["line_end"], 4)
        self.assertEqual(index["blocks"][1]["unparsed_lemma_lines"], [5])
        self.assertEqual(index["blocks"][1]["native_verse_labels"], [])

    def test_mark_sections_replay_the_complete_english_witness(self):
        root = Path(__file__).resolve().parents[2] / "src/sources"
        edition = root / "works/thomas-aquinas/catena-aurea-in-marcum/editions/1842-english-oxford-ccel"
        text = (edition / "artifacts/text-790ed587/source.txt").read_text().splitlines()
        index = json.loads((edition / "artifacts/candidates-756967a9/candidates.json").read_bytes())
        edges = yaml.load((root / "commentary/fragment-loci.yaml").read_bytes(),
                          Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
        extents = {row["passage_id"]: row["extent"] for row in edges["fragments"]}
        ranges = []
        for path in sorted((edition / "passages").glob("*.toml")):
            passage = tomllib.loads(path.read_text())
            with self.subTest(passage=path.stem):
                (first, last), = passage["physical_line_ranges"]
                lines = text[first - 1:last]
                self.assertEqual(passage["text"], " ".join(lines))
                self.assertEqual(passage["transcription_segments"],
                                 [{"line": i, "text": line} for i, line in enumerate(lines, start=first)])
                self.assertIn(passage["id"], extents)
                ranges.append((first, last))
        self.assertEqual(sorted(ranges), [(b["line_start"], b["line_end"]) for b in index["blocks"]])
        # Native chapter 9 opens one verse before the Vulgate chapter break.
        passage_id = "passage.thomas-aquinas.catena-aurea-in-marcum.1842-english-oxford-ccel.09-01-08"
        self.assertEqual(extents[passage_id], dict(token="Mark", first_chapter=8, first_verse=39,
                                                   last_chapter=9, last_verse=7))

    def test_missing_chapter_refuses(self):
        with self.assertRaisesRegex(ValueError, "chapter sequence"):
            MODULE.extract(b'<ThML><div2 title="Chapter 2"/></ThML>', "Mark", 2)

    def test_unheaded_paragraph_refuses(self):
        with self.assertRaisesRegex(ValueError, "unheaded commentary"):
            MODULE.extract(b'<ThML><div2 title="Chapter 1"><p>Text</p></div2></ThML>', "Mark", 1)


if __name__ == "__main__":
    unittest.main()
