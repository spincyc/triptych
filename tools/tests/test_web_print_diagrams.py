"""Immutable diagrams remain bound to the exact selected canonical source."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _web_print_diagrams as diagrams


class DiagramTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/web-print-diagram-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.root = Path(self.temporary.name)
        self.base = self.root / "delivery"
        (self.base / "assets").mkdir(parents=True)
        self.body = r"Before.\begin{tikzpicture}\node {Amen.};\end{tikzpicture}After."
        source = self.root / "src/gpt/fixture/main.tex"
        source.parent.mkdir(parents=True)
        source.write_text(self.body)
        state = {"entrypoint": "src/gpt/fixture/main.tex", "role": "main", "flags": {},
                 "ordered_inputs": [{"path": "src/gpt/fixture/main.tex", "occurrence": 1,
                                     "sha256": diagrams.digest(self.body), "selected_sha256": diagrams.digest(self.body)}]}
        state["selection_digest"] = diagrams.digest(diagrams.canonical_json(state))
        self.selection = {"head": "", "body": self.body, "selection": state,
                          "chunks": [{"path": "src/gpt/fixture/main.tex", "occurrence": 1,
                                      "selected_line": 1, "text": self.body}]}
        svg = b'<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/></svg>'
        (self.base / "assets/drawing.svg").write_bytes(svg)
        span = diagrams.diagram_spans(self.body)[0]
        self.unit = {**span, "asset_id": "tikz-" + "a" * 24,
                     "asset": "assets/drawing.svg", "svg_sha256": diagrams.digest(svg), "bytes": len(svg),
                     "selection_digest": state["selection_digest"],
                     "source_closure_digest": diagrams.digest(diagrams.canonical_json(diagrams.closure(self.selection))),
                     "labels": ["Amen."], "source_refs": diagrams.selected_source_refs(self.selection, span["start"], span["end"])}
        self.manifest = {"schema": "triptych-selected-diagram-assets/v1", "outputs": {
            "gpt/fixture": {"selection_digest": state["selection_digest"], "head_sha256": diagrams.digest(""),
                            "body_sha256": diagrams.digest(self.body), "source_closure": diagrams.closure(self.selection),
                            "diagrams": [self.unit]}}}
        self.pin = diagrams.digest(diagrams.canonical_json(self.manifest))
        self.manifest["projection_digest"] = self.pin
        self.write_manifest()

    def tearDown(self):
        self.temporary.cleanup()

    def write_manifest(self):
        (self.base / "manifest.json").write_text(json.dumps(self.manifest))

    def resolve(self, selection=None):
        return diagrams.resolve(self.root, "gpt/fixture", selection or self.selection,
                                asset_root=self.base, expected_projection_digest=self.pin)

    def test_valid_lookup_and_projection_spawn_no_renderer(self):
        with patch("subprocess.run", side_effect=AssertionError("unexpected renderer")):
            records = self.resolve()
            projected = diagrams.project(self.selection, records, asset_url=lambda row: "web-print-assets/" + row["svg_sha256"] + ".svg")
        self.assertEqual(projected["canonical_body"], self.body)
        self.assertNotIn(r"\begin{tikzpicture}", projected["body"])
        self.assertIn(r"\SemanticDiagram{" + self.unit["asset_id"] + "}", projected["body"])
        self.assertIn("web-print-assets/", projected["diagram_projection"]["lua_filters"][0])

    def test_changed_svg_bytes_refuse(self):
        (self.base / "assets/drawing.svg").write_bytes(b"changed")
        with self.assertRaisesRegex(diagrams.DiagramRefused, "hash/size"):
            self.resolve()

    def test_changed_canonical_owner_refuses(self):
        (self.root / "src/gpt/fixture/main.tex").write_text("Changed source.")
        with self.assertRaisesRegex(diagrams.DiagramRefused, "source closure"):
            self.resolve()

    def test_stale_selection_refuses(self):
        changed = copy.deepcopy(self.selection)
        changed["body"] = changed["body"].replace("Amen.", "Other.")
        with self.assertRaises(diagrams.DiagramRefused):
            self.resolve(changed)

    def test_rewritten_manifest_without_trusted_pin_refuses(self):
        self.manifest["outputs"]["gpt/fixture"]["diagrams"][0]["labels"] = ["Other."]
        self.manifest["projection_digest"] = diagrams.digest(diagrams.canonical_json({key: value for key, value in self.manifest.items() if key != "projection_digest"}))
        self.write_manifest()
        with self.assertRaisesRegex(diagrams.DiagramRefused, "pinned projection"):
            self.resolve()

    def test_missing_or_shifted_projection_occurrence_refuses(self):
        records = self.resolve()
        with self.assertRaises(diagrams.DiagramRefused):
            diagrams.project(self.selection, [])
        changed = copy.deepcopy(records)
        changed[0]["start"] += 1
        with self.assertRaises(diagrams.DiagramRefused):
            diagrams.project(self.selection, changed)


if __name__ == "__main__":
    unittest.main()
