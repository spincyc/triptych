"""Publication source contracts join real liturgical inventories and renderers."""
from __future__ import annotations

import json
import os
import py_compile
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _document_schema as schemas
from document_schema_checks import liturgy

SERVER = Path("liturgy/roman-rite/1962/reference/altar-server-guides")
DICTIONARY = Path("liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary")


def copy_sources(source: Path, destination: Path) -> None:
    for path in source.rglob("*"):
        if path.is_file() and path.suffix in {".tex", ".toml", ".md", ".sty", ".py", ".json", ".txt", ".yaml", ".yml", ".bib"}:
            target = destination / path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)


def record(root: Path, leaf: Path) -> dict:
    data = schemas.adapter_manifest(root, root / "src/gpt" / leaf)
    return schemas._normalise(root, data, None)


def save_components(data: dict, path: Path) -> None:
    lines = []
    for key, value in data.items():
        if key not in {"outputs", "components", "lanes"}:
            lines.append(f"{key} = {json.dumps(value)}")
    lines.append("[outputs]")
    lines.extend(f"{key} = {json.dumps(value)}" for key, value in data["outputs"].items())
    for table in ("components", "lanes"):
        for item in data[table]:
            lines.append(f"[[{table}]]")
            lines.extend(f"{key} = {json.dumps(value)}" for key, value in item.items())
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


class LiturgySchemaTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/schema-lit-checks"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def test_validator_loader_ignores_stale_bytecode_and_creates_no_source_cache(self):
        path = self.root / "src/fixture-validator.py"
        path.parent.mkdir()
        path.write_text('value = "stale"\n')
        source_stat = path.stat()
        cached = Path(py_compile.compile(str(path), doraise=True))
        bytecode = cached.read_bytes()
        path.write_text('value = "fresh"\n')
        os.utime(path, ns=(source_stat.st_atime_ns, source_stat.st_mtime_ns))
        liturgy._module.cache_clear()
        self.addCleanup(liturgy._module.cache_clear)
        self.addCleanup(sys.modules.pop, "_document_schema_src_fixture_validator_py", None)
        with mock.patch.object(liturgy, "CODE_ROOT", self.root), mock.patch.object(sys, "dont_write_bytecode", False):
            self.assertEqual(liturgy._module("src/fixture-validator.py").value, "fresh")
            self.assertEqual(cached.read_bytes(), bytecode)
            shutil.rmtree(cached.parent)
            liturgy._module.cache_clear()
            self.assertEqual(liturgy._module("src/fixture-validator.py").value, "fresh")
            self.assertFalse(cached.parent.exists())

    def server(self, name="02-missa-cantata-cue-cards"):
        owner = self.root / "src/gpt" / SERVER
        copy_sources(ROOT / "src/common", self.root / "src/common")
        copy_sources(ROOT / "src/gpt" / SERVER, owner)
        return owner, record(self.root, SERVER / name)

    def proper(self):
        leaf = self.root / "src/gpt/proper"
        (leaf / "research").mkdir(parents=True)
        elements = ["introit", "collect", "gospel", "communion"]
        data = dict(schema=2, record_type="proper-components", document="proper", calendar="roman-1962",
                    entrypoint="main.tex", synthesis_entrypoint="synthesis.tex", homily_entrypoint="homily.tex",
                    appointed_text_completeness="complete", element_keys=elements,
                    outputs=dict(research="proper", synthesis="proper-synthesis", homily="proper-homily",
                                 web="proper", canonical_label="Full PDF", synthesis_label="Synthesis PDF", homily_label="Homily PDF"),
                    components=[], lanes=[])
        for key, kind, modes in (("appointed", "appointed-text", ["research"]),
                                  ("treatment", "proper-treatment", ["research"]),
                                  ("augustine", "interpretive-lane", ["research"]),
                                  ("gregory", "interpretive-lane", ["research"]),
                                  ("integrated", "integrated-commentary", ["synthesis"]),
                                  ("sermon", "homily", ["homily"]),
                                  ("terminal", "terminal-apparatus", ["research", "synthesis", "homily"])):
            data["components"].append(dict(key=key, kind=kind, path=key + ".tex", modes=modes,
                                           element_keys=list(elements), references=[], depends_on=[]))
            (leaf / f"{key}.tex").write_text(f"Substantive {key} fixture prose.\n")
        for key in ("augustine", "gregory"):
            data["lanes"].append(dict(key=key, authors=[key.title(), "Thomas Aquinas"],
                                      sources=["research/interpretations.md"],
                                      senses=["literal", "allegorical", "moral", "anagogical"],
                                      element_keys=list(elements), component_keys=[key]))
        (leaf / "research/interpretations.md").write_text("Source-locus-identified interpretation evidence.\n")
        (leaf / "generation-metadata.tex").write_text("Fixture provenance.\n")
        for mode, filename in (("research", "main.tex"), ("synthesis", "synthesis.tex"), ("homily", "homily.tex")):
            body = "".join("\\input{proper/" + item["path"] + "}\n" for item in data["components"] if mode in item["modes"])
            (leaf / filename).write_text(body)
        path = leaf / "proper-components.toml"
        save_components(data, path)
        publication = dict(id="gpt/proper", provider="gpt", leaf="proper", source_dir="src/gpt/proper",
                           kind="proper-1962", entrypoint="main.tex", contracts={"component_schema": 2},
                           outputs=[dict(role="canonical", entrypoint="main.tex"), dict(role="synthesis", entrypoint="synthesis.tex"),
                                    dict(role="homily", entrypoint="homily.tex")],
                           structure=[dict(role="proper-components", source="proper-components.toml")])
        return leaf, path, data, publication

    def chronology_proper(self):
        leaf_id = Path("liturgy/roman-rite/1962/propers/temporal/f02-all-saints")
        leaf = self.root / "src/gpt" / leaf_id
        copy_sources(ROOT / "src/common", self.root / "src/common")
        copy_sources(ROOT / "src/gpt" / leaf_id, leaf)
        # Read the same canonical typed corpus; test mutations remain confined
        # to this publication's copied generated files and source rows.
        (self.root / "src/sources").symlink_to(ROOT / "src/sources", target_is_directory=True)
        return leaf, record(self.root, leaf_id)

    def test_complete_component_source_graph_passes_without_artifacts(self):
        _, _, _, publication = self.proper()
        self.assertEqual(liturgy.check(self.root, publication), [])

    def test_missing_lane_sense_is_refused(self):
        _, path, data, publication = self.proper()
        data["lanes"][0]["senses"].pop()
        save_components(data, path)
        self.assertIn("all four senses", "\n".join(liturgy.check(self.root, publication)))

    def test_lane_must_cover_every_appointed_unit(self):
        _, path, data, publication = self.proper()
        data["lanes"][0]["element_keys"].pop()
        save_components(data, path)
        self.assertIn("every element", "\n".join(liturgy.check(self.root, publication)))

    def test_detached_interpretive_component_is_refused(self):
        leaf, _, _, publication = self.proper()
        path = leaf / "main.tex"
        path.write_text(path.read_text().replace("\\input{proper/augustine.tex}\n", ""))
        self.assertIn("include graph", "\n".join(liturgy.check(self.root, publication)))

    def test_generated_orientation_cannot_drop_an_appointed_row(self):
        leaf, publication = self.chronology_proper()
        self.assertEqual(liturgy.check(self.root, publication), [])
        path = leaf / "sections/70-date-location.tex"
        text = path.read_text()
        _, start, end = next(liturgy._calls(text, "chronologyorientationrow", 2))
        path.write_text(text[:start] + text[end:])
        self.assertIn("each generated row once", "\n".join(liturgy.check(self.root, publication)))

    def test_generated_chronology_keeps_its_typed_relation_to_the_corpus(self):
        leaf, publication = self.chronology_proper()
        path = leaf / "research/chronology.toml"
        text = path.read_text().replace('relation = "composition"', 'relation = "narrated-event"', 1)
        path.write_text(text)
        self.assertIn("not what the chronology corpus answers", "\n".join(liturgy.check(self.root, publication)))

    def test_removing_an_element_from_every_component_still_fails_appointment_coverage(self):
        leaf, publication = self.chronology_proper()
        path = leaf / "proper-components.toml"
        path.write_text(path.read_text().replace('"collect", ', ''))
        self.assertIn("canonical appointed-text inventory", "\n".join(liturgy.check(self.root, publication)))

    def test_actual_sung_card_selection_passes(self):
        _, publication = self.server()
        self.assertEqual(liturgy.check(self.root, publication), [])

    def test_solemn_action_cannot_omit_its_actor_argument(self):
        owner, publication = self.server("03-solemn-mass")
        self.assertEqual(liturgy.check(self.root, publication), [])
        path = owner / "shared/solemn-ceremony.tex"
        path.write_text(path.read_text().replace(
            r"\actionrowid{SO-006}{Entrance}{All lay servers}",
            r"\actionrowid{SO-006}{Entrance}", 1))
        self.assertIn("actionrowid SO-006", "\n".join(liturgy.check(self.root, publication)))

    def test_removed_low_mass_pair_cannot_shrink_the_declared_deck(self):
        owner, publication = self.server("01-low-mass-flash-cards")
        path = owner / "01-low-mass-flash-cards/main.tex"
        text = liturgy._text(path)
        removals = [(start, end) for command in ("LowMassFrontCard", "LowMassBackCard")
                    for args, start, end in liturgy._calls(text, command, 5) if args[2] == "01"]
        for start, end in sorted(removals, reverse=True):
            text = text[:start] + text[end:]
        path.write_text(text)
        self.assertIn("manifest ID", "\n".join(liturgy.check(self.root, publication)))

    def test_card_back_cannot_read_another_existing_response(self):
        owner, publication = self.server("01-low-mass-flash-cards")
        path = owner / "01-low-mass-flash-cards/main.tex"
        path.write_text(path.read_text().replace("{01}{FOOT/ALTAR}{\\ServerLatinData{A1}}", "{01}{FOOT/ALTAR}{\\ServerLatinData{A2}}"))
        self.assertIn("detached from canonical response A1", "\n".join(liturgy.check(self.root, publication)))

    def test_unmirrored_source_card_row_is_refused(self):
        owner, publication = self.server()
        path = owner / "shared/missa-cantata-action-cards.tex"
        text = path.read_text().replace(r"\actionflashback{MC-A02}", r"\actionflashback{MC-A01}", 1)
        path.write_text(text)
        self.assertIn("row-mirrored", "\n".join(liturgy.check(self.root, publication)))

    def test_deleted_response_datum_is_not_replaced_by_a_nonempty_inventory(self):
        owner, publication = self.server()
        path = owner / "shared/response-reference.tex"
        text = liturgy._text(path)
        for args, start, end in liturgy._calls(text, "serveranswer", 6):
            if args[0].startswith("A2 ---"):
                text = text[:start] + text[end:]
                break
        path.write_text(text)
        self.assertIn("complete canonical inventory", "\n".join(liturgy.check(self.root, publication)))

    def test_response_data_cannot_lose_its_form_specific_voice(self):
        owner, publication = self.server()
        path = owner / "shared/response-reference.tex"
        text = liturgy._text(path)
        args, start, end = next(liturgy._calls(text, "DefineResponseVoice", 4))
        path.write_text(text[:start] + "\\DefineResponseVoice{" + args[0] + "}{}{" + args[2] + "}{" + args[3] + "}" + text[end:])
        self.assertIn("complete DefineResponseVoice record", "\n".join(liturgy.check(self.root, publication)))

    def test_actual_dictionary_typed_inventory_and_selection_pass(self):
        owner = self.root / "src/gpt" / DICTIONARY
        copy_sources(ROOT / "src/gpt" / DICTIONARY, owner)
        publication = record(self.root, DICTIONARY / "altar-server")
        self.assertEqual(liturgy.check(self.root, publication), [])

    def test_dictionary_role_cannot_substitute_main_for_objects(self):
        owner = self.root / "src/gpt" / DICTIONARY
        copy_sources(ROOT / "src/gpt" / DICTIONARY, owner)
        publication = record(self.root, DICTIONARY / "altar-server")
        for item in publication["structure"]:
            if item["role"] == "object-records":
                item.pop("data", None)
                item["source"] = "main.tex"
        self.assertIn("object-records must name", "\n".join(liturgy.check(self.root, publication)))

    def test_dictionary_duplicate_edition_selection_is_refused(self):
        owner = self.root / "src/gpt" / DICTIONARY
        copy_sources(ROOT / "src/gpt" / DICTIONARY, owner)
        publication = record(self.root, DICTIONARY / "altar-server")
        path = owner / "shared/schema/edition-selections.toml"
        path.write_text(path.read_text().replace('id = "ed-sacristan"', 'id = "ed-altar-server"'))
        self.assertIn("duplicate stable IDs", "\n".join(liturgy.check(self.root, publication)))

    def test_dictionary_relationship_cannot_point_to_a_removed_object(self):
        owner = self.root / "src/gpt" / DICTIONARY
        copy_sources(ROOT / "src/gpt" / DICTIONARY, owner)
        publication = record(self.root, DICTIONARY / "altar-server")
        path = owner / "shared/objects/linens/altar-cloths.toml"
        path.write_text(path.read_text().replace('related_objects = []', 'related_objects = ["obj-missing"]'))
        self.assertIn("unknown object obj-missing", "\n".join(liturgy.check(self.root, publication)))

    def test_calendar_counts_are_bound_to_actual_source_rows(self):
        leaf_id = Path("liturgy/roman-rite/1962/reference/liturgical-calendar")
        leaf = self.root / "src/gpt" / leaf_id
        copy_sources(ROOT / "src/common", self.root / "src/common")
        copy_sources(ROOT / "src/gpt" / leaf_id, leaf)
        publication = record(self.root, leaf_id)
        self.assertEqual(liturgy.check(self.root, publication), [])
        path = leaf / "sections/50-sanctorale-jan-jun.tex"
        text = path.read_text()
        _, start, end = next(liturgy._calls(text, "calentry", 3))
        path.write_text(text[:start] + text[end:])
        self.assertIn("January: 22 source rows disagree with 23", "\n".join(liturgy.check(self.root, publication)))

    def test_postconciliar_coequal_dates_keep_distinct_discriminators(self):
        leaf_id = Path("liturgy/roman-rite/postconciliar/roman-missal-third-edition-en-us-2011/reference/liturgical-calendar")
        leaf = self.root / "src/gpt" / leaf_id
        copy_sources(ROOT / "src/common", self.root / "src/common")
        copy_sources(ROOT / "src/gpt" / leaf_id, leaf)
        publication = record(self.root, leaf_id)
        self.assertEqual(liturgy.check(self.root, publication), [])
        path = leaf / "sections/50-general-calendar.tex"
        path.write_text(path.read_text().replace(r"\caldiscriminator{sebastian}", ""))
        self.assertIn("duplicate singular fixed-date source row", "\n".join(liturgy.check(self.root, publication)))


if __name__ == "__main__":
    unittest.main()
