"""The terminal manifest consumer reads only a held verified Bible product."""
from contextlib import contextmanager, nullcontext
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
loader = importlib.machinery.SourceFileLoader("mass_today_products", str(ROOT / "tools/mass-today"))
spec = importlib.util.spec_from_loader(loader.name, loader)
today = importlib.util.module_from_spec(spec)
loader.exec_module(today)


class BibleManifestProducts(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/next-product-consumers"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.data = self.root / "verified"
        self.data.mkdir()
        self.active = False

    @contextmanager
    def products(self, root, *, product_ids):
        self.assertEqual(root, self.root)
        self.assertEqual(product_ids, ["bibles"])
        self.active = True
        try:
            yield SimpleNamespace(data_root=self.data)
        finally:
            self.active = False

    def test_verified_manifest_controls_language_and_named_selection(self):
        rows = [{"id": "latin", "language": "la"}, {"id": "english", "language": "en"}]
        (self.data / "bibles.json").write_text(json.dumps({"bibles": rows}))
        legacy = self.root / "src/web/data"
        legacy.mkdir(parents=True)
        (legacy / "bibles.json").write_text('{"bibles":[{"id":"unverified","language":"en"}]}')
        read_text = Path.read_text

        def read(path, *args, **kwargs):
            if path == self.data / "bibles.json":
                self.assertTrue(self.active)
            return read_text(path, *args, **kwargs)

        with (patch.object(today, "ROOT", self.root),
              patch.object(today, "verified_products", self.products),
              patch.object(Path, "read_text", read)):
            self.assertEqual(today.indexed_bibles(), rows)
            self.assertEqual(today.default_bible("en"), rows[1])
            self.assertEqual(today.indexed_bible("latin"), rows[0])
        self.assertFalse(self.active)

    def test_missing_or_invalid_manifest_is_refused_instead_of_empty(self):
        for body in (None, "{", "{}", '{"bibles":null}'):
            with self.subTest(body=body):
                target = self.data / "bibles.json"
                if body is None:
                    target.unlink(missing_ok=True)
                else:
                    target.write_text(body)
                with (patch.object(today, "ROOT", self.root),
                      patch.object(today, "verified_products", self.products),
                      self.assertRaisesRegex(today.Refused, "published browser data is unavailable")):
                    today.indexed_bibles()
                self.assertFalse(self.active)

    def test_failed_verification_never_returns_a_smaller_library(self):
        with (patch.object(today, "verified_products", side_effect=today.ProductError("stale descriptor")),
              self.assertRaisesRegex(today.Refused, "stale descriptor")):
            today.indexed_bibles()


class DatedFormState(unittest.TestCase):
    def test_ordinary_hymns_receive_the_office_of_the_readable_branch(self):
        winner = {"key": "nativitate-domini-octave", "nature": "feast"}
        mass = today._SourceMass({"key": winner["key"]})
        mass._source_branch = {"settled": True, "winner": winner}
        mass._source_readable = {"key": winner["key"], "state": "said"}
        day = {"weekday": "friday", "season": "christmastide", "branches": []}
        expected = {"settled": True, "winner": winner, "formulary": winner["key"],
                    "standing": "said", "weekday": "friday"}
        self.assertEqual(today.ordinary_predicate_context_for(day, mass, "2026-12-25")["office"], expected)
        mass._source_readable = {"key": "another-mass", "state": "displaced"}
        office = today.ordinary_predicate_context_for(day, mass, "2026-12-25")["office"]
        self.assertEqual(office, {**expected, "formulary": "another-mass", "standing": "displaced"})
        self.assertIsNone(today.ordinary_predicate_context_for(day, dict(mass), "2026-12-25")["office"])

    def test_owned_form_and_verified_bible_reach_both_day_adapters(self):
        bible = {"id": "clementine-vulgate", "numbering": "vulgate"}
        cases = [
            (today.project_dated_conclusions, "roman-1962", "2026-12-25",
             "nativitate-domini-octave", "night"),
            (today.project_dated_conclusions, "roman-1962", "2026-11-02",
             "commemoratione-omnium-fidelium-defunctorum", "third"),
            (today.project_source_local_1970, "postconciliar", "2026-12-25",
             "nativity", "night"),
        ]
        validator = ROOT / "src/web/browser/liturgy/reader-state.js"
        for project, edition, date, owner, form in cases:
            with self.subTest(project=project.__name__, date=date):
                mass = {"key": owner, "selected": True, "standing": "said", "selected_form": form}
                day = {"calendar": edition, "settled": True, "masses": [mass]}
                payload = {"days": [day], "date": date, "scripture": {"id": bible["id"]}}
                args = SimpleNamespace(expanded=True, lang="la", json=True, mass=None, form=form,
                                       proper_choice=None, ordinary_variant=None, witness=None,
                                       territory=None, source_local_1970=True)
                with (patch.object(today, "verified_products",
                                   return_value=nullcontext(SimpleNamespace(data_root=ROOT))) as verify,
                      patch.object(today.subprocess, "run", return_value=SimpleNamespace(
                          returncode=0, stdout='{"members":[],"groups":[],"properRites":[]}')) as run):
                    project(payload, {edition: {}}, args, bible)
                verify.assert_called_once_with(ROOT, product_ids=["propers", "rubrics", "ordinary"])
                state = json.loads(run.call_args.kwargs["input"])["request"]
                self.assertEqual(state["selectedReadableFormulary"], {"id": owner})
                self.assertEqual(state["form"], form)
                self.assertEqual(state["languages"]["orations"], "la")
                self.assertEqual(state["bible"], bible)
                result = subprocess.run([
                    "node", "-e", "const S=require(process.argv[1]),fs=require('fs');"
                    "console.log(JSON.stringify(S.validateReaderState(JSON.parse(fs.readFileSync(0)))));",
                    str(validator),
                ], input=json.dumps(state), capture_output=True, text=True, check=True)
                validation = json.loads(result.stdout)
                self.assertTrue(validation["ok"], validation)


if __name__ == "__main__":
    unittest.main()
