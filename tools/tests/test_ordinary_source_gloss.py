#!/usr/bin/env python3
"""Keep source translations nonspoken and source letters separate from roles."""
import csv
import hashlib
import importlib.machinery
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from _ordinary_text import element_lines
from _tooling import Style


class OrdinarySourceGloss(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        loader = importlib.machinery.SourceFileLoader("ordinary_gloss_tool", str(ROOT / "tools/mass-ordinary"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        cls.tool = importlib.util.module_from_spec(spec)
        loader.exec_module(cls.tool)

    def test_gloss_requires_review_and_excludes_spoken_or_action_metadata(self):
        tool = self.tool
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch") as directory:
            root = Path(directory)
            (root / "text.tsv").write_text(
                "element_key\tseq\ttext\nunit\t10\tP. Invocation.\nunit\t20\tPrinted translation.\n")
            library = {"artifact.synthetic.gloss": {
                "id": "artifact.synthetic.gloss", "path": "text.tsv", "_source_root": root}}
            parts = [{"key": "invocation", "seq": [10], "speaker": "priest", "printed_marker": "P."},
                     {"key": "source-gloss", "seq": [20], "gloss": True}]
            entry = {"english_turns": parts, "turns_basis": "Source page: roman invocation followed by an italic translation."}
            project = lambda value: tool.structured_turns(
                value, "english", library, "artifact.synthetic.gloss", ["unit"],
                "text", "section/unit", "synthetic", "P. Invocation.\nPrinted translation.")
            rows = project(entry)
            self.assertTrue(rows[1]["gloss"])
            self.assertEqual(rows[1]["text"], "Printed translation.")
            self.assertTrue(all(rows[1][field] is None for field in ("speaker", "dialogue_role", "action", "printed_marker")))
            self.assertEqual("\n".join(row["text"] for row in rows), "P. Invocation.\nPrinted translation.")
            for extra in ({"gloss": False}, {"gloss": "true"}, {"speaker": "priest"},
                          {"dialogue_role": "response"}, {"action": True}, {"printed_marker": "R."}):
                with self.subTest(extra=extra), self.assertRaises(tool.SourceError):
                    project(entry | {"english_turns": [parts[0], parts[1] | extra]})
            with self.assertRaises(tool.SourceError):
                project({"english_turns": parts})
            with self.assertRaises(tool.SourceError):
                tool.artifact_turn_partition_table({"key": "s", "turn_partitions": [
                    {"element": "unit", "lang": "en", "parts": parts}]}, "synthetic")

    def test_cli_uses_explicit_roles_and_preserves_gloss_when_rubrics_hide(self):
        # These deliberately cross person and role. A source R. on a server
        # must not create a response glyph; a priest may carry that response.
        speaker_only = {"speaker": "server", "dialogue_role": None, "printed_marker": "R.",
                        "text": "R. Server begins.", "action": None}
        call = speaker_only | {"dialogue_role": "versicle"}
        answer = {"speaker": "priest", "dialogue_role": "response", "printed_marker": "P.",
                  "text": "P. Priest answers.", "action": None}
        gloss = {"speaker": None, "dialogue_role": None, "printed_marker": None, "action": None,
                 "gloss": True, "text": "Printed translation."}
        action = {"speaker": None, "dialogue_role": None, "printed_marker": None,
                  "action": True, "text": "Bow."}
        def render(turns, tier="unicode", rubrics=True):
            held = {"lang": "en", "text": "\n".join(row["text"] for row in turns), "turns": turns}
            return "\n".join(element_lines({"kind": "dialogue", "translations": [held]}, "en",
                                           Style(tier), show_rubrics=rubrics))
        plain_server = render([speaker_only])
        self.assertIn("Server: Server begins.", plain_server)
        self.assertNotIn("℟", plain_server)
        for tier in ("plain", "unicode", "rich"):
            shown = render([call, answer, action, gloss], tier)
            self.assertIn("Server: Server begins.", shown)
            self.assertIn("Priest: Priest answers.", shown)
            self.assertIn("[ Source translation: Printed translation. ]", shown)
            self.assertIn("[ Bow. ]", shown)
            self.assertNotIn("R. Server", shown)
            self.assertNotIn("P. Priest", shown)
            without_rubrics = render([call, answer, action, gloss], tier, False)
            self.assertNotIn("Bow.", without_rubrics)
            self.assertIn("Printed translation.", without_rubrics)
        unicode = render([call, answer])
        self.assertIn("℣ — Server:", unicode)
        self.assertIn("℟ — Priest:", unicode)

    def test_complete_source_derivatives_rejoin_exact_parents(self):
        tool = self.tool
        library = tool.artifact_records(ROOT / "src/sources")
        inventory = tomllib.loads((ROOT / "src/sources/inventories/roman-1962-ordo-missae-v1.toml").read_text())
        selected = [section[field] for section in inventory["sections"] for field in ("artifact", "artifact_latin")
                    if field in section and "2026-10-20" in section[field]]
        self.assertEqual(len(selected), 10)
        divided = 0
        for identifier in selected:
            child = library[identifier]
            parent = library[child["derived_from"]]
            self.assertEqual(child["edition_id"], parent["edition_id"])
            self.assertEqual(child["rights_status"], "public-domain")
            def read(record):
                raw = (ROOT / record["path"]).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), record["sha256"])
                return list(csv.DictReader(io.StringIO(raw.decode()), delimiter="\t"))
            originals = {int(row["seq"]): row for row in read(parent)}
            children = {int(row["seq"]): row for row in read(child)}
            text_field = "english" if "english" in next(iter(originals.values())) else "latin"
            accounted = set()
            for seq, original in originals.items():
                if seq in children:
                    self.assertEqual(original, children[seq])
                    accounted.add(seq)
                    continue
                held = [row for number,row in children.items() if number not in originals and number // 100 == seq]
                self.assertGreaterEqual(len(held), 2)
                self.assertEqual(" ".join(row[text_field] for row in held), original[text_field])
                self.assertTrue(all(row["element_key"] == original["element_key"] for row in held))
                accounted.update(int(row["seq"]) for row in held)
                divided += 1
            self.assertEqual(accounted, set(children))
        self.assertEqual(divided, 38)


if __name__ == "__main__":
    unittest.main()
