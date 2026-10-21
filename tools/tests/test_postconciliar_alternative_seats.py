"""Exact normal-reading labels; special rites retain their declared frames."""
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

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
DATA_ROOT = Path(os.environ.get("TRIPTYCH_ALTERNATIVE_SEAT_ROOT", ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
loader = SourceFileLoader("_normal_alternative_ordinary", str(ROOT / "tools/mass-ordinary"))
spec = spec_from_loader(loader.name, loader)
O = module_from_spec(spec)
sys.modules[spec.name] = O
loader.exec_module(O)
LABELS = {
    "Second Reading (common provision)": ("ascension", "day", "lectio-secunda"),
    "Second Reading (Year C optional)": ("ascension", "day", "lectio-secunda"),
    "Responsorial Psalm (alternative)": ("ot-15", "main", "psalmus-responsorius"),
    "Gospel (ad libitum)": ("ot-18-tuesday", "main", "evangelium"),
    "First Reading (ad libitum)": ("ot-19-friday", "main", "lectio-prima"),
}


class NormalAlternativeSeats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = tomllib.loads((DATA_ROOT / "src/sources/inventories/postconciliar-ordo-missae-v1.toml").read_text())
        cls.ordinary = json.loads((ROOT / "src/web/data/structure/ordinary/postconciliar.json").read_text())
        cls.ordinary["slots"] = O.slot_table(source, cls.ordinary["sections"], "postconciliar")
        cls.propers = json.loads((ROOT / "src/web/data/structure/propers/postconciliar.json").read_text())
        cls.index = {mass["key"]: mass for mass in cls.propers["masses"]}

    @classmethod
    def rows(cls, mass, form):
        owner = cls.index[mass]
        return owner["propers"] if form == "main" else next(f["propers"] for f in owner["forms"] if f["id"] == form)

    def test_each_current_normal_label_has_its_exact_role_seat(self):
        for label, (mass, form, seat) in LABELS.items():
            with self.subTest(label=label):
                row = next(p for p in self.rows(mass, form) if p["name"] == label)
                self.assertEqual(row["ordinary_disposition"]["kind"], "alternative")
                ordinal = O.proper_slot(self.ordinary["slots"], label)
                self.assertGreaterEqual(ordinal, 0)
                self.assertEqual(self.ordinary["slots"][ordinal]["key"], seat)
                self.assertFalse(self.ordinary["slots"][ordinal]["qualified"])
                O.check_form_seating(self.ordinary, self.rows(mass, form), mass + "/" + form, full=True)

    def test_entire_current_calendar_seating_and_special_frame_boundaries(self):
        result = O.check_calendar_seating(self.ordinary, self.propers)
        self.assertEqual(result["failures"], 0)
        self.assertGreater(result["full_forms"], 0)
        self.assertGreater(result["nonfull_forms"], 0)
        for mass in ("palm-sunday", "good-friday", "easter-vigil"):
            self.assertNotEqual(O.effective_ordinary_frame(self.index[mass], None, mass)["applicability"], "full")
        for label in ("Blessing of Branches", "Prayer", "Prayer after the First Reading", "Responsorial Psalm (alternative after the First Reading)"):
            self.assertEqual(O.proper_slot(self.ordinary["slots"], label), -1)

    def test_cross_seat_and_undeclared_qualifier_still_refuse(self):
        bad = copy.deepcopy(self.rows("ascension", "day"))
        next(p for p in bad if p["name"] == "Second Reading (common provision)")["name"] = "Gospel (shorter form)"
        with self.assertRaisesRegex(O.SourceError, "spans Ordinary slots"):
            O.check_form_seating(self.ordinary, bad, "cross-seat", full=True)
        unknown = copy.deepcopy(self.rows("ascension", "day"))
        next(p for p in unknown if p["name"] == "Second Reading (common provision)")["name"] = "Second Reading (unreviewed option)"
        with self.assertRaisesRegex(O.SourceError, "has no usable Ordinary seat"):
            O.check_form_seating(self.ordinary, unknown, "unknown-label", full=True)
        cases = [{"label": label, "seat": seat, "rows": self.rows(mass, form)} for label, (mass, form, seat) in LABELS.items()]
        code = r"""const S=require(process.argv[1]);let raw='';process.stdin.on('data',c=>raw+=c);process.stdin.on('end',()=>{const x=JSON.parse(raw),shown=x.ordinary.sections.flatMap(section=>section.elements.map(element=>({section,element}))),seating=S.seats(x.ordinary,shown);function run(rows,label){try{const p=S.seatPropers(rows,seating,r=>r.name==='Placeholder'),events=S.massEvents(shown,p);const found=events.find(e=>e.kind==='proper_choice'&&e.options.some(o=>o.rows.some(r=>r.proper.name===label)));return{seat:found&&found.seat.key,broke:p.broke};}catch(e){return{error:e.message};}}process.stdout.write(JSON.stringify({good:x.cases.map(c=>run(c.rows,c.label)),cross:run(x.cross,''),unknown:run(x.unknown,'')}));});"""
        node = shutil.which("node")
        if node is None:
            self.skipTest("node is not installed")
        result = subprocess.run([node, "-e", code, str(ROOT / "src/web/browser/liturgy/ordinary-seating.js")], input=json.dumps({"ordinary": self.ordinary, "cases": cases, "cross": bad, "unknown": unknown}), text=True, capture_output=True, check=True)
        out = json.loads(result.stdout)
        for case, got in zip(cases, out["good"]):
            self.assertEqual(got, {"seat": case["seat"], "broke": False})
        self.assertIn("one usable semantic Ordinary seat", out["cross"]["error"])
        self.assertIn("one usable semantic Ordinary seat", out["unknown"]["error"])


if __name__ == "__main__":
    unittest.main()
