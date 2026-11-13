"""Native CLI entrypoint with explicit source snapshots and product fixture.

The producer is run unchanged once per exact source owner. Bible passages are
unfilled: these tests prove source prayer selection, not Scripture coverage.
The production verified-products gate is never replaced outside this fixture.
"""
from contextlib import contextmanager, redirect_stderr, redirect_stdout
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

ROOT = Path(os.environ.get("TRIPTYCH_REVIEW_ROOT", Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT / "tools/tests"))
from _product_data import browser_data_root


def load_today():
    name = "_native_today_selection_fixture"
    module = ModuleType(name)
    module.__file__ = str(ROOT / "tools/mass-today")
    sys.modules[name] = module
    candidate = Path(os.environ.get("TRIPTYCH_REVIEW_CLI", module.__file__))
    exec(compile(candidate.read_text(), module.__file__, "exec"), module.__dict__)
    return module


class NativeTodayFixture:
    def __init__(self):
        self.today = load_today()
        self.data = browser_data_root(ROOT)
        self.manifest = json.loads((self.data / "bibles.json").read_text())["bibles"]
        rubrics = Path(os.environ.get("TRIPTYCH_REVIEW_RUBRICS", self.data / "structure/rubrics/roman-1962.json"))
        self.rubrics = json.loads(rubrics.read_text())
        self.model = os.environ.get("TRIPTYCH_REVIEW_MODEL", str(ROOT / "src/web/browser/liturgy/assembly-model.js"))
        self.native_invoke = self.today.invoke
        self.ordinary = self.native_invoke("mass-ordinary", ["show", "--calendar", "roman-1962"])
        self.raw = {}
        self.derived = {}
        self.fault = None

    def derive(self, date):
        if date not in self.derived:
            year = json.loads((self.data / f"structure/calendar/roman-1962/{date[:4]}.json").read_text())
            harness = "const fs=require('fs'),m=require(process.argv[1]);process.stdout.write(JSON.stringify(m.derive(JSON.parse(fs.readFileSync(0,'utf8')))));"
            done = subprocess.run(["node", "-e", harness, self.model], cwd=ROOT,
                input=json.dumps({"date": date, "year": year, "rubrics": self.rubrics}), capture_output=True, text=True, check=True)
            self.derived[date] = json.loads(done.stdout)
        return copy.deepcopy(self.derived[date])

    def invoke(self, tool, argv):
        if tool == "calendar-rubrics":
            value = self.derive(argv[argv.index("--date") + 1])
            if self.fault:
                self.fault("derived", value)
            return {"days": [value]}
        if tool == "mass-ordinary":
            return copy.deepcopy(self.ordinary)
        if tool != "mass-propers":
            raise AssertionError("Unexpected sibling dependency: " + tool)
        keys = [argv[i + 1] for i, flag in enumerate(argv) if flag == "--mass"]
        missing = [key for key in keys if key not in self.raw]
        if missing:
            args = ["show", "--calendar", "roman-1962"]
            for key in missing:
                args += ["--mass", key]
            result = self.native_invoke("mass-propers", args)
            for row in result.get("masses", [result]):
                self.raw[row["mass"]["key"]] = row
        bible = argv[argv.index("--bible") + 1] if "--bible" in argv else None
        rows = []
        for key in keys:
            value = copy.deepcopy(self.raw[key])
            value["bible"] = {"id": bible, "passages": {}} if bible else None
            if self.fault:
                self.fault("proper", value)
            rows.append(value)
        return {"masses": rows} if len(rows) > 1 else rows[0]

    @contextmanager
    def products(self, *args, **kwargs):
        yield SimpleNamespace(data_root=self.data)

    def run(self, date, language="en", mass=None, *, text=False, fault=None):
        args = ["show", "--date", date, "--calendar", "roman-1962", "--expanded", "--bible", "douay-rheims"]
        if language:
            args += ["--lang", language]
        if mass:
            args += ["--mass", mass]
        if not text:
            args += ["--json"]
        out, err = io.StringIO(), io.StringIO()
        self.fault = fault
        print_json = self.today.print_json
        with (patch.object(self.today, "print_json", lambda payload: print_json(payload, stream=out)),
              patch.object(self.today, "invoke", self.invoke),
              patch.object(self.today, "indexed_bibles", return_value=copy.deepcopy(self.manifest)),
              patch.object(self.today, "verified_products", self.products),
              redirect_stdout(out), redirect_stderr(err)):
            code = self.today.main(args)
        self.fault = None
        return SimpleNamespace(returncode=code, stdout=out.getvalue(), stderr=err.getvalue())
