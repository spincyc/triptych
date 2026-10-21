"""The held shorter Second Reading uses its existing Ordinary seat."""
from __future__ import annotations
import copy
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import unittest
import yaml

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
DATA_ROOT = Path(os.environ.get("TRIPTYCH_SECOND_READING_ROOT", ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
loader = SourceFileLoader("_second_reading_ordinary", str(ROOT / "tools/mass-ordinary"))
spec = spec_from_loader(loader.name, loader)
O = module_from_spec(spec)
sys.modules[spec.name] = O
loader.exec_module(O)


class SecondReadingSeat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = tomllib.loads((DATA_ROOT / "src/sources/inventories/postconciliar-ordo-missae-v1.toml").read_text())
        cls.ordinary = json.loads((ROOT / "src/web/data/structure/ordinary/postconciliar.json").read_text())
        cls.ordinary["slots"] = O.slot_table(source, cls.ordinary["sections"], "postconciliar")
        document = yaml.safe_load((ROOT / "src/sources/calendars/postconciliar/propers.yaml").read_text())
        cls.mass = next(m for section in document["sections"].values() for m in section.get("masses", []) if m["key"] == "lent-1")

    def test_exact_source_slot_claims_the_existing_shorter_label_only(self):
        slots = self.ordinary["slots"]
        main = O.proper_slot(slots, "Second Reading")
        short = O.proper_slot(slots, "Second Reading (shorter form)")
        self.assertGreaterEqual(main, 0)
        self.assertEqual(main, short)
        self.assertEqual(slots[short]["key"], "lectio-secunda")
        self.assertFalse(slots[short]["qualified"])
        self.assertEqual(O.proper_slot(slots, "Second Reading (invented form)"), -1)
        self.assertEqual(O.proper_slot(slots, "Lesson"), -1)

    def test_actual_lent_one_source_passes_and_old_inventory_reproduces_failure(self):
        self.assertTrue(any(p["name"] == "Second Reading (shorter form)" for p in self.mass["propers"]))
        O.check_form_seating(self.ordinary, self.mass["propers"], "postconciliar/lent-1/main", full=True)
        old = copy.deepcopy(self.ordinary)
        for slot in old["slots"]:
            if slot["key"] == "lectio-secunda":
                slot["propers"].remove("Second Reading (shorter form)")
        with self.assertRaisesRegex(O.SourceError, "has no usable Ordinary seat"):
            O.check_form_seating(old, self.mass["propers"], "postconciliar/lent-1/main", full=True)

    def test_python_and_shared_runtime_reject_cross_seat_and_unknown_members(self):
        bad = copy.deepcopy(self.mass["propers"])
        next(p for p in bad if p["name"] == "Second Reading (shorter form)")["name"] = "Gospel (shorter form)"
        with self.assertRaisesRegex(O.SourceError, "spans Ordinary slots"):
            O.check_form_seating(self.ordinary, bad, "cross-seat-control", full=True)
        unknown = copy.deepcopy(self.mass["propers"])
        next(p for p in unknown if p["name"] == "Second Reading (shorter form)")["name"] = "Second Reading (invented form)"
        with self.assertRaisesRegex(O.SourceError, "has no usable Ordinary seat"):
            O.check_form_seating(self.ordinary, unknown, "unknown-name-control", full=True)
        code = r"""const S=require(process.argv[1]);let raw='';process.stdin.on('data',c=>raw+=c);process.stdin.on('end',()=>{const x=JSON.parse(raw), shown=x.ordinary.sections.flatMap(section=>section.elements.map(element=>({section,element}))),seating=S.seats(x.ordinary,shown);function run(rows){try{const placed=S.seatPropers(rows,seating,p=>p.name==='Placeholder');const events=S.massEvents(shown,placed);const group=events.find(e=>e.kind==='proper_choice'&&e.group==='second-reading');return{seat:group&&group.seat.key,options:group&&group.options.map(o=>o.id),broke:placed.broke};}catch(e){return{error:e.message};}}process.stdout.write(JSON.stringify({good:run(x.good),cross:run(x.cross),unknown:run(x.unknown)}));});"""
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is not installed")
        result = subprocess.run([node, "-e", code, str(ROOT / "src/web/browser/liturgy/ordinary-seating.js")],
                                input=json.dumps({"ordinary": self.ordinary, "good": self.mass["propers"], "cross": bad, "unknown": unknown}),
                                text=True, capture_output=True, check=True)
        out = json.loads(result.stdout)
        self.assertEqual(out["good"], {"seat": "lectio-secunda", "options": ["longer", "shorter"], "broke": False})
        self.assertIn("one usable semantic Ordinary seat", out["cross"]["error"])
        self.assertIn("one usable semantic Ordinary seat", out["unknown"]["error"])


if __name__ == "__main__":
    unittest.main()
