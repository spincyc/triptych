"""Read the checked ancient-source frames through the production consumers.

Compile the current inventory, rather than the potentially stale served JSON.
The JavaScript probe uses the production adapters and repository native DOM;
it is a semantic and rendering contract, not a Chromium layout test.
"""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / "src/sources"
INVENTORY = SOURCES / "inventories/postconciliar-ordo-missae-v1.toml"
PROBE = ROOT / "tools/tests/postconciliar_ordinary_source_frames.cjs"
SCRATCH = Path(os.environ.get("TRIPTYCH_TEST_SCRATCH", ROOT / ".scratch"))


class PostconciliarOrdinarySourceFrames(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        directory = tempfile.TemporaryDirectory(
            prefix="postconciliar-source-frames-", dir=SCRATCH
        )
        cls.addClassCleanup(directory.cleanup)
        cls.payload = Path(directory.name) / "postconciliar.json"

        loader = importlib.machinery.SourceFileLoader(
            "ordinary_source_frames_tool", str(ROOT / "tools/mass-ordinary")
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        tool = importlib.util.module_from_spec(spec)
        loader.exec_module(tool)
        library = tool.artifact_records(SOURCES)
        current = tool.calendar_structure(SOURCES, INVENTORY, library)
        cls.payload.write_text(json.dumps(current, ensure_ascii=False), encoding="utf-8")

    def probe(self, mode):
        result = subprocess.run(
            ["node", str(PROBE), str(ROOT), str(self.payload), mode],
            cwd=ROOT, capture_output=True, text=True, check=False, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["mode"], mode)
        self.assertGreater(report["cases"], 0)

    def test_source_kinds_actors_and_parent_boundaries(self):
        self.probe("source")

    def test_greeting_selection_requires_the_explicit_bishop_option(self):
        self.probe("selection")

    def test_source_qualifications_and_actor_cues_survive_both_displays(self):
        self.probe("rendering")

    def test_the_held_sixfold_kyrie_obeys_its_penitential_condition(self):
        self.probe("conditions")

    def test_the_actual_frame_keeps_the_source_spans_and_propers_in_order(self):
        self.probe("order")


if __name__ == "__main__":
    unittest.main()
