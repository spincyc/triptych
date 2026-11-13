"""Source-owned embedded quotations do not become additional spoken readings."""
import contextlib
import copy
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest

from tools.tests._product_data import browser_data_root

ROOT = Path(__file__).resolve().parents[2]


def tool(name):
    loader = importlib.machinery.SourceFileLoader("_citation_roles_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class ProperCitationRoles(unittest.TestCase):
    def test_source_roles_survive_production_and_both_cli_readers(self):
        props, today = tool("mass-propers"), tool("mass-today")
        payload = props.find_mass(ROOT / "src/sources/calendars", "roman-1962", "palm-sunday")
        raw = next(p for p in payload["mass"]["propers"] if p.get("incipit") == "Omnes collaudant nomen tuum")
        masses = json.loads((browser_data_root(ROOT) / "structure/propers/roman-1962.json").read_text())["masses"]
        generated = next(p for m in masses if m["key"] == "palm-sunday" for p in m["propers"] if p.get("incipit") == raw["incipit"])
        self.assertEqual([v["reading_role"]["kind"] for v in raw["verses"]], ["embedded-quotation", "following-psalm"])
        for old, verse in zip(generated["citations"], raw["verses"]):
            made = props.citation_structure(verse, "vulgate", {"Matthew": "Matt", "Psalms": "Ps"}, owner_source="mixed")
            self.assertEqual(made, old)
        proper = {**generated, "verses": raw["verses"]}
        normalized = lambda value: " ".join(value.split())
        for language, bible_id in (("en", "douay-rheims"), ("la", "clementine-vulgate")):
            with self.subTest(language=language):
                bible = props.load_bible(bible_id, ROOT / "src/sources/bibles")
                resolved = props.resolve_passages(payload, bible, [("", proper, None)])
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    props.render_reading(payload, language, resolved, appointed=[("", proper, None)])
                enriched = {**proper, "verses": [dict(v, **resolved[v["ref"]]) for v in proper["verses"]]}
                expanded = "\n".join(today.proper_lines(enriched, today.Style(), " ", lang=language, witness=None, seat=None, why=False))
                for result in (stdout.getvalue(), expanded):
                    self.assertNotIn(normalized(resolved["Matthew 21:9"]["text"]), normalized(result))
                    self.assertIn("Matthew 21:9", result)
                    self.assertIn("target Missal wording not established", result)
                    self.assertIn(normalized(resolved["Psalm 147"]["text"]), normalized(result))
                    body = proper["text"] if language == "la" else next(t["text"] for t in proper["translations"] if t["lang"] == language)
                    self.assertLess(normalized(result).index(normalized(body)), normalized(result).index(normalized(resolved["Psalm 147"]["text"])))
                missing = copy.deepcopy(proper)
                missing.update(text=None, translations=[])
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    props.render_reading(payload, language, resolved, appointed=[("", missing, None)])
                self.assertIn(normalized(resolved["Matthew 21:9"]["text"]), normalized(stdout.getvalue()))

    def test_native_renderer_terminal_and_refusal_contract(self):
        done = subprocess.run(["node", str(ROOT / "tools/tests/proper_citation_roles.mjs"), str(ROOT), str(browser_data_root(ROOT))], capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
        result = json.loads(done.stdout)
        self.assertEqual(len(result["presentations"]), 3)
        self.assertEqual(result["missingBodyAndRoleControls"], 6)
        self.assertEqual(result["malformedRolesRefused"], 9)
