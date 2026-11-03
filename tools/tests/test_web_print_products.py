"""Cold print dispatch, independent proof, and compact private transport."""
from __future__ import annotations

import base64
from collections import Counter
import copy
import gc
import json
from pathlib import Path
import sys
import tempfile
import tomllib
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / ".scratch/web-print-products/tests"
sys.path.insert(0, str(ROOT / "scripts"))
import _web_print_prepare as prepare
import _web_print_products as producer
from _web_print_common import inventory


def recipe(name="fixture", *, family="publication", kind="article"):
    return {"id": "bible:" + name if family == "bible" else "publication:fixture/" + name,
            "family": family, "provider": "fixture", "document": name, "kind": kind,
            "entrypoint": "src/fixture/" + name + "/main.tex", "edition": "main"}


def product(selected=None):
    selected = selected or recipe()
    identity = selected["id"]
    units = [{"id": "u-1", "source": "src/fixture/main.tex", "occurrence": "first"},
             {"id": "u-2", "source": "src/fixture/main.tex", "occurrence": "second"}]
    value = {"id": identity, "output_id": identity, "title": "Complete source fixture", "print_type": "flow",
            "source_digest": "a" * 64, "selection_digest": "b" * 64, "expected_units": units,
            "coverage_result": {"status": "pass", "output_id": identity, "source_digest": "a" * 64,
                                "selection_digest": "b" * 64, "expected_units": copy.deepcopy(units)},
            "parts": [{"id": "first", "html": '<p id="u-1" data-print-unit="u-1">First &amp; full.</p>'},
                      {"id": "second", "html": '<p id="u-2" data-print-unit="u-2">Second complete body.</p>'}],
            "source_paths": ["src/fixture/main.tex"], "assets": [],
            "fonts": [{"source": "audit-only"}], "style_sha256": "c" * 64}
    for part in value["parts"]:
        part["html_sha256"] = prepare.digest(part["html"])
    return value


def semantic_product():
    value = product()
    full = [{"id": "u-2", "source_ref": {"path": "src/fixture/main.tex", "selected_line": 20}, "kind": "note"},
            {"id": "u-1", "source_ref": {"path": "src/fixture/main.tex", "selected_line": 10}, "kind": "paragraph"}]
    ledger = {"units": full, "containers": [], "macro_state_digest": "d" * 64, "selection_digest": value["selection_digest"]}
    ledger["ledger_digest"] = prepare.digest(json.dumps(ledger, sort_keys=True))
    value.update(expected_units=full, expected_ledger=ledger, expected_print_units=["u-1", "u-2"])
    from _web_print_publication import unit_expectations
    value["print_unit_expectations"] = unit_expectations(ledger, value["expected_print_units"])
    value["coverage_result"] = {"status": "pass", "complete": True, "ledger_digest": ledger["ledger_digest"],
                                "macro_state_digest": "d" * 64, "matched_units": [{"id": "u-2"}, {"id": "u-1"}]}
    return value


class ScratchTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)


class SelectionTests(ScratchTests):
    def test_compiler_inventory_binds_semantics_geometry_and_the_entire_curriculum_package(self):
        paths = set(producer.compiler_paths(ROOT))
        for name in ("_web_print_semantics.py", "_web_print_flow.py", "_web_print_diagrams.py", "_web_print_server_diagrams.py", "_web_print_dictionary_context.py", "_web_print_server_schedule.py", "_web_print_server_card_schedule.py"):
            self.assertIn("scripts/" + name, paths)
        package = ROOT / "scripts/_web_print_curriculum"
        self.assertTrue({path.relative_to(ROOT).as_posix() for path in package.rglob("*.py")} <= paths)
        self.assertIn("scripts/_web_print_curriculum/response_geometry.py", paths)
        self.assertIn("scripts/_web_print_marks.py", paths)
        self.assertIn("src/common/browser-print-marks.json", paths)
        self.assertNotIn("scripts/_web_print.py", paths)

    def test_complete_canonical_output_census_and_dispatch_exclude_holds(self):
        # Independent declaration/release inventory, without producer enumeration.
        expected = set()
        for manifest in (ROOT / "src").rglob("publication.toml"):
            leaf = manifest.parent
            if not (leaf / "web-edition.toml").is_file():
                continue
            provider = manifest.relative_to(ROOT / "src").parts[0]
            relative = leaf.relative_to(ROOT / "src" / provider).as_posix()
            outputs = [relative]
            companions = leaf / "proper-components.toml"
            if companions.is_file():
                from _proper_components import outputs as declared_outputs
                outputs.extend(value for key, value in declared_outputs(tomllib.loads(companions.read_text())).items()
                               if key in {"synthesis", "homily"})
            declaration = tomllib.loads((leaf / "web-edition.toml").read_text())
            for output in outputs:
                release = json.loads((ROOT / "release/publications" / provider / (output + ".json")).read_bytes())
                if release["status"] == "alpha" and not declaration.get("withdrawn"):
                    expected.add("publication:" + provider + "/" + output)
        from _bible_editions import EDITIONS
        expected.update("bible:" + name for name, row in EDITIONS.items() if row.get("publishable"))
        selected = producer.admitted_recipes(ROOT)
        self.assertEqual({row["id"] for row in selected}, expected)
        self.assertEqual(len(selected), 288)
        self.assertEqual(Counter(map(producer.adapter_name, selected)),
                         {"publication": 231, "curriculum": 37, "server": 7, "dictionary": 6, "bible": 7})
        self.assertEqual([row["id"] for row in selected], sorted(expected))

    def test_unknown_family_and_missing_release_refuse(self):
        with self.assertRaisesRegex(ValueError, "unowned"):
            producer.adapter_name({"family": "invented", "kind": "article"})
        selected = {**recipe(), "canonical": "fixture"}
        leaf = self.root / "src/fixture/fixture"
        leaf.mkdir(parents=True)
        (leaf / "web-edition.toml").write_text("withdrawn = false\n")
        with patch("_print_document.recipes", return_value=[selected]), self.assertRaises(FileNotFoundError):
            producer.admitted_recipes(self.root)


class PreparationTests(ScratchTests):
    def geometry_product(self, *, empty=False):
        from _web_print_curriculum.response_geometry import check, render, signature
        raw = product(); raw["print_type"] = "curriculum"
        expected = []
        if not empty:
            event = {**signature("Blank"), "id": "response-1", "source_ref": {"path": "src/fixture/main.tex", "occurrence": 1, "coordinate_space": "canonical-expansion"},
                     "source_payload_digest": "d" * 64, "definition_refs": []}
            expected.append(event)
            raw["parts"][0]["html"] += render(event, 1)
            raw["parts"][0]["html_sha256"] = prepare.digest(raw["parts"][0]["html"])
        raw["expected_response_geometry"] = expected
        raw["response_geometry_coverage"] = check(expected, "".join(part["html"] for part in raw["parts"]))
        return raw

    def test_complete_body_routes_and_compact_proof_without_audit_leak(self):
        raw = product()
        raw["projections"] = {"audit-only": "large source snippets"}
        result = prepare.prepare_product(raw, recipe())
        self.assertEqual(result["root_route"], "print/fixture/fixture.html")
        self.assertEqual(result["parts"][0]["route"], result["root_route"])
        self.assertIn("selector", result["parts"][0])
        self.assertEqual(result["parts"][1]["href"], "print/fixture/fixture/parts/second.html")
        for original, part in zip(raw["parts"], result["parts"]):
            self.assertIn(original["html"], part["html"])
            self.assertIn('data-print-document="' + raw["id"] + '"', part["html"])
            self.assertIn('data-print-source="' + "a" * 64 + '"', part["html"])
        descriptor = result["descriptor"]
        self.assertEqual(descriptor["unit_inventory"], inventory(["u-1", "u-2"]))
        self.assertEqual(descriptor["coverage_result"]["status"], "pass")
        for field in ("expected_units", "projections", "expected_ledger", "matched_units", "fonts", "style_sha256"):
            self.assertNotIn(field, descriptor)
        self.assertLess(len(prepare.canonical_json(descriptor)), prepare.DESCRIPTOR_LIMIT)
        self.assertTrue(all("html" not in row for row in descriptor["parts"]))

    def test_bible_existing_relative_routes_remain_inside_bible_owner(self):
        selected = recipe("edition", family="bible")
        raw = product(selected)
        raw.update(print_type="bible", root_route="print/bibles/edition.html")
        raw["parts"][0]["selector"] = "#frontmatter"
        raw["parts"][1]["href"] = "edition/Genesis/part-1.html"
        result = prepare.prepare_product(raw, selected)
        self.assertEqual(result["parts"][1]["route"], "print/bibles/edition/Genesis/part-1.html")

    def test_source_bound_dom_order_can_differ_from_source_ledger_order(self):
        raw = semantic_product()
        result = prepare.prepare_product(raw, recipe())
        self.assertEqual(result["descriptor"]["unit_inventory"], inventory(["u-1", "u-2"]))
        self.assertEqual(raw["expected_units"][0]["id"], "u-2")
        self.assertNotIn("expected_ledger", result)

    def test_invented_dom_expectations_and_wrong_ledger_refuse(self):
        for mutation in ("source", "unknown-unit", "ledger", "ledger-content", "matched", "incomplete"):
            with self.subTest(mutation=mutation):
                raw = semantic_product()
                if mutation == "source": raw["print_unit_expectations"][0]["source"] = "src/other/main.tex"
                elif mutation == "unknown-unit":
                    raw["expected_print_units"][0] = "invented"
                    raw["print_unit_expectations"][0]["id"] = "invented"
                elif mutation == "ledger": raw["expected_ledger"]["ledger_digest"] = "f" * 64
                elif mutation == "ledger-content": raw["expected_ledger"]["containers"].append({"id": "invented"})
                elif mutation == "matched": raw["coverage_result"]["matched_units"].pop()
                else: raw["coverage_result"]["complete"] = False
                with self.assertRaises(ValueError): prepare.prepare_product(raw, recipe())

    def test_wrong_namespace_selection_owner_body_or_pass_refuse(self):
        for mutation in ("id", "selection", "source", "unit-order", "status", "body-pin", "incomplete"):
            with self.subTest(mutation=mutation):
                raw = product()
                if mutation == "id": raw["id"] = "publication:other/fixture"
                elif mutation == "selection": raw["coverage_result"]["selection_digest"] = "e" * 64
                elif mutation == "source": raw["coverage_result"]["source_digest"] = "e" * 64
                elif mutation == "unit-order": raw["parts"].reverse()
                elif mutation == "status": raw["coverage_result"]["status"] = "complete-mechanically"
                elif mutation == "body-pin": raw["parts"][0]["html_sha256"] = "e" * 64
                else: raw["coverage_result"]["complete"] = False
                with self.assertRaises(ValueError): prepare.prepare_product(raw, recipe())

    def test_unknown_styles_active_markup_bad_routes_and_hidden_extra_body_refuse(self):
        for fragment in ('<p style="display:none">hidden</p>', '<script>run()</script>',
                         '<p onclick="run()">click</p>', '<img src="data:image/svg+xml,x">',
                         '<a href="java&#x0a;script:run()">unsafe</a>',
                         '<!DOCTYPE html><p>body</p>', '<?php unsafe ?>',
                         '<section data-print-part="first" data-print-document="publication:fixture/fixture" '
                         'data-print-source="' + "a" * 64 + '"><p data-print-unit="u-1">body</p></section>lost source'):
            with self.subTest(fragment=fragment), self.assertRaises(ValueError):
                raw = product(); raw["parts"][0]["html"] = fragment
                raw["parts"][0]["html_sha256"] = prepare.digest(fragment)
                prepare.prepare_product(raw, recipe())
        for path in ("../outside.html", "/absolute.html", "edition/../outside.html", "bad\\path.html"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                raw = product(); raw["parts"][1]["href"] = path
                prepare.prepare_product(raw, recipe())

    def test_existing_typed_wrapper_does_not_discard_or_duplicate_source_body(self):
        raw = product()
        original = raw["parts"][0]["html"]
        raw["parts"][0]["html"] = '<section data-print-part="first" data-print-document="' + raw["id"] + '" data-print-source="' + "a" * 64 + '">' + original + '</section>'
        raw["parts"][0]["html_sha256"] = prepare.digest(raw["parts"][0]["html"])
        result = prepare.prepare_product(raw, recipe())
        self.assertEqual(result["parts"][0]["html"], raw["parts"][0]["html"])
        self.assertEqual(result["parts"][0]["html"].count(original), 1)

    def test_part_body_and_compact_descriptor_budgets_are_enforced(self):
        raw = product()
        raw["parts"][0]["html"] += "x" * prepare.PART_LIMIT
        raw["parts"][0]["html_sha256"] = prepare.digest(raw["parts"][0]["html"])
        with self.assertRaisesRegex(ValueError, "HTML budget"):
            prepare.prepare_product(raw, recipe())
        raw = product(); raw["parts"] = []; units = []
        for index in range(1000):
            uid = "unit-" + str(index)
            units.append({"id": uid, "source": "src/fixture/main.tex", "occurrence": str(index)})
            raw["parts"].append({"id": "part-" + str(index), "html": '<p data-print-unit="' + uid + '">Complete.</p>'})
            raw["parts"][-1]["html_sha256"] = prepare.digest(raw["parts"][-1]["html"])
        raw["expected_units"] = units; raw["coverage_result"]["expected_units"] = units
        with self.assertRaisesRegex(ValueError, "descriptor exceeds budget"):
            prepare.prepare_product(raw, recipe())

    def test_owner_body_and_all_supplied_statistics_are_checked_before_normalization(self):
        from _web_print_common import part_statistics
        for field in ("html_sha256", "text_sha256", "structure_sha256", "expected_ids", "units", "counts"):
            with self.subTest(field=field):
                raw = product(); part = raw["parts"][0]
                part.update(part_statistics(part["html"]))
                if field == "html_sha256": part.pop(field)
                elif field in {"text_sha256", "structure_sha256"}: part[field] = "e" * 64
                elif field == "counts": part[field] = {"span": 1}
                else: part[field] = ["invented"]
                with self.assertRaisesRegex(ValueError, "owner pin"):
                    prepare.prepare_product(raw, recipe())
        raw = product(); part = raw["parts"][0]
        part.update(part_statistics(part["html"]))
        part["html"] = part["html"].replace("First", "Mutated")
        part["html_sha256"] = prepare.digest(part["html"])
        with self.assertRaisesRegex(ValueError, "text_sha256 differs"):
            prepare.prepare_product(raw, recipe())

    def test_typed_normalization_must_preserve_the_owner_words(self):
        def mutated(fragment, **kwargs):
            return fragment.replace("First", "Mutated")
        with patch.object(prepare, "normalize_html", side_effect=mutated), self.assertRaisesRegex(ValueError, "changed source words"):
            prepare.prepare_product(product(), recipe())

    def test_curriculum_requires_source_geometry_proof_even_when_no_fields_exist(self):
        for empty in (False, True):
            raw = self.geometry_product(empty=empty)
            result = prepare.prepare_product(raw, recipe())
            self.assertEqual(result["metadata"]["response_geometry_coverage"], raw["response_geometry_coverage"])
            self.assertNotIn("expected_response_geometry", result)
            raw.pop("response_geometry_coverage")
            with self.assertRaisesRegex(ValueError, "geometry lacks complete"):
                prepare.prepare_product(raw, recipe())

    def test_wrong_source_geometry_digest_or_changed_final_variant_refuses(self):
        for mutation in ("incomplete", "digest", "source-plan", "source-path", "variant", "dropped"):
            with self.subTest(mutation=mutation):
                raw = self.geometry_product()
                if mutation == "incomplete": raw["response_geometry_coverage"]["complete"] = False
                elif mutation == "digest": raw["response_geometry_coverage"]["expected_digest"] = "e" * 64
                elif mutation == "source-plan": raw["expected_response_geometry"][0]["source_payload_digest"] = "e" * 64
                elif mutation == "source-path":
                    from _web_print_curriculum.response_geometry import check
                    raw["expected_response_geometry"][0]["source_ref"]["path"] = "/host/temporary/source.tex"
                    raw["response_geometry_coverage"] = check(raw["expected_response_geometry"], "".join(part["html"] for part in raw["parts"]))
                else:
                    part = raw["parts"][0]
                    part["html"] = part["html"].replace("response-blank-short", "response-blank-long") if mutation == "variant" else part["html"].split('<span class="response-space')[0]
                    part["html_sha256"] = prepare.digest(part["html"])
                with self.assertRaises(ValueError): prepare.prepare_product(raw, recipe())
        def changed_geometry(fragment, **kwargs):
            return fragment.replace("response-blank-short", "response-blank-long")
        with patch.object(prepare, "normalize_html", side_effect=changed_geometry), self.assertRaises(ValueError):
            prepare.prepare_product(self.geometry_product(), recipe())


class AssetTests(ScratchTests):
    def setUp(self):
        super().setUp()
        self.destination = self.root / prepare.PREFIX
        self.pool = prepare.AssetPool(self.root, self.destination)

    def record(self, body=b"<svg>complete artwork</svg>", **extra):
        return {"id": "semantic-one", "body": body, "sha256": prepare.digest(body), "bytes": len(body),
                "mime": "image/svg+xml", "role": "diagram", **extra}

    def test_body_hash_deduplicates_different_semantic_ids_without_raw_source(self):
        row = self.record(source_inputs={"src/source.tex": "a" * 64})
        first = self.pool.add(row)
        self.assertEqual(self.pool.add({**row, "id": "semantic-two"}), first)
        self.assertEqual(self.pool.add({key: value for key, value in row.items() if key != "body"}), first)
        self.assertEqual(len(self.pool.rows()), 1)
        private = prepare.read_asset(self.root, self.pool.rows()[0])
        self.assertEqual(base64.b64decode(private["body_base64"]), row["body"])
        self.assertNotIn("source_inputs", private["asset"])
        self.assertEqual(private["asset"]["id"], first)
        self.assertEqual(private["asset"]["src"], "print-assets/" + first + ".svg")

    def test_conflicting_metadata_and_wrong_hash_size_or_missing_bytes_refuse(self):
        row = self.record()
        self.pool.add(row)
        for mutated in ({**row, "role": "illustration"}, {**row, "mime": "image/png"},
                        {**row, "family": "conflict"}, {**row, "sha256": "0" * 64},
                        {**row, "bytes": 1}, {"id": "x", "sha256": "f" * 64, "mime": "image/svg+xml"}):
            with self.subTest(mutated=mutated), self.assertRaises(ValueError): self.pool.add(mutated)

    def test_canonical_raster_is_pinned_and_svg_is_embedded(self):
        source = self.root / "src/artwork/image.png"
        source.parent.mkdir(parents=True)
        source.write_bytes(b"canonical PNG fixture")
        row = self.record(body=source.read_bytes(), mime="image/png", role="illustration", source="src/artwork/image.png")
        row.pop("body")
        key = self.pool.add(row)
        private = prepare.read_asset(self.root, {"id": key, "path": "assets/" + key + ".json"})
        self.assertEqual(private["canonical_path"], "src/artwork/image.png")
        self.assertNotIn("body_base64", private)
        source.with_suffix(".svg").write_bytes(b"canonical SVG fixture")
        svg = self.record(body=source.with_suffix(".svg").read_bytes(), source="src/artwork/image.svg")
        svg.pop("body")
        key = self.pool.add(svg)
        self.assertIn("body_base64", prepare.read_asset(self.root, {"id": key, "path": "assets/" + key + ".json"}))
        source.write_bytes(b"mutated canonical PNG")
        with self.assertRaisesRegex(ValueError, "hash mismatch"): self.pool.add(row)

    def test_canonical_asset_symlink_and_traversal_refuse(self):
        (self.root / "src").mkdir()
        (self.root / "src/alias.png").symlink_to(ROOT / "LICENSE")
        for path in ("src/alias.png", "../outside.png", ".scratch/image.png"):
            with self.subTest(path=path), self.assertRaises((ValueError, OSError)):
                self.pool.add(self.record(mime="image/png", source=path))

    def test_base_faces_and_marks_share_their_two_canonical_licenses(self):
        body = b"license fixture"
        target = self.root / "src/common/browser-print-fonts/OFL.txt"
        target.parent.mkdir(parents=True); target.write_bytes(body)
        license_record = self.record(body, mime="text/plain", role="font-license")
        faces = [self.record(("font fixture " + str(index)).encode(), mime="font/woff2", role="font",
                            family="Fixture", weight=str(index * 100), style="normal", unicode_range="U+0000-FFFF",
                            license=license_record) for index in range(8)]
        mark_license_body = b"Junicode license fixture"
        mark_license_path = self.root / "src/web/browser/shared/fonts/OFL-Junicode.txt"
        mark_license_path.parent.mkdir(parents=True); mark_license_path.write_bytes(mark_license_body)
        marks = self.record(b"source marks face", mime="font/woff2", role="font", family="Triptych Source Marks",
                            weight="400", style="normal", unicode_range="U+211F,U+2123,U+21A9,U+2610,U+2720",
                            license=self.record(mark_license_body, mime="text/plain", role="font-license"))
        with patch("_web_print_assets.font_assets", return_value=faces), patch.dict(sys.modules, {"_web_print_marks": SimpleNamespace(font_asset=lambda *args, **kwargs: marks)}):
            producer.global_fonts(self.root, self.pool)
        self.assertEqual(len(self.pool.rows()), 11)
        fonts = [row["asset"] for row in self.pool.records.values() if row["asset"]["role"] == "font"]
        self.assertEqual(len(fonts), 9)
        base = [face for face in fonts if face["family"] == "Fixture"]
        self.assertEqual(len(base), 8)
        self.assertTrue(all(face["license"] == "print-assets/" + prepare.digest(body) + ".txt" for face in base))
        self.assertTrue(all(face["unicode_range"] == "U+0000-FFFF" for face in base))
        supplement = next(face for face in fonts if face["family"] == "Triptych Source Marks")
        self.assertEqual(supplement["license"], "print-assets/" + prepare.digest(mark_license_body) + ".txt")
        self.assertEqual(supplement["unicode_range"], "U+211F,U+2123,U+21A9,U+2610,U+2720")
        marks["unicode_range"] = "U+0000-FFFF"
        with patch("_web_print_assets.font_assets", return_value=faces), patch.dict(sys.modules, {"_web_print_marks": SimpleNamespace(font_asset=lambda *args, **kwargs: marks)}), self.assertRaisesRegex(ValueError, "five-glyph contract"):
            producer.global_fonts(self.root, self.pool)


class GeneratorTests(ScratchTests):
    def run_generate(self, selected, render, out=None):
        with patch("_web_print_publication.require_print_toolchain"), patch.object(producer, "admitted_recipes", return_value=selected), \
             patch.object(producer, "global_fonts"), patch.object(producer, "render_product", side_effect=render):
            return producer.generate(self.root, out or self.root / ".scratch/output")

    def test_streaming_drops_full_audits_before_next_product_and_writes_json_only(self):
        alive = set()
        class Tracked(dict):
            def __init__(self, value, name): super().__init__(value); self.name = name; alive.add(name)
            def __del__(self): alive.discard(self.name)
        def render(root, selected, pool, audit):
            gc.collect(); self.assertFalse(alive)
            self.assertTrue(audit.is_relative_to(self.root / ".scratch/web-print-products"))
            (audit / "full-audit.txt").write_text("large ignored proof ledger")
            value = product(selected); value["projections"] = ["audit only"]
            return Tracked(value, selected["id"])
        selected = [recipe("one"), recipe("two")]
        self.assertEqual(self.run_generate(selected, render)["products"], 2)
        self.assertFalse(alive)
        data = self.root / ".scratch/output"
        index = prepare.read_index(data)
        self.assertEqual([row["id"] for row in index["products"]], [row["id"] for row in selected])
        for row in index["products"]:
            private = prepare.read_product(data, row)
            self.assertEqual(private["asset_ids"], {})
            self.assertNotIn("projections", private)
        self.assertTrue(all(path.suffix == ".json" for path in data.rglob("*") if path.is_file()))
        self.assertFalse(list((self.root / ".scratch/web-print-products").glob("audit-*")))

    def test_failed_owner_never_publishes_catalog_and_fresh_output_is_required(self):
        def refused(*args): raise ValueError("owner proof failed")
        with self.assertRaisesRegex(ValueError, "owner proof failed"): self.run_generate([recipe()], refused)
        self.assertFalse((self.root / ".scratch/output" / prepare.PREFIX / "catalog.json").exists())
        with self.assertRaisesRegex(ValueError, "fresh output"): self.run_generate([recipe()], lambda *args: product())

    def test_sealed_outside_and_symlink_outputs_refuse_before_adapter(self):
        cache = self.root / ".scratch/sealed"
        cache.mkdir(parents=True); (cache / ".browser-products-cache-v1").write_text("sealed")
        (self.root / ".scratch/alias").symlink_to(cache, target_is_directory=True)
        for out in (cache / "new", self.root / "public-output", self.root / ".scratch/alias/new"):
            with self.subTest(out=out), self.assertRaises(ValueError):
                self.run_generate([recipe()], lambda *args: self.fail("adapter must not run"), out)

    def test_content_addressed_product_tampering_and_index_escape_refuse(self):
        self.run_generate([recipe()], lambda *args: product())
        data = self.root / ".scratch/output"
        index = prepare.read_index(data); row = index["products"][0]
        path = data / prepare.PREFIX / row["path"]
        value = json.loads(path.read_bytes()); value["parts"][0]["html"] += "changed"
        prepare.write_json(path, value)
        with self.assertRaisesRegex(ValueError, "filename differs"): prepare.read_product(data, row)
        index["products"][0]["path"] = "products/../../outside.json"
        prepare.write_json(data / prepare.PREFIX / "catalog.json", index)
        with self.assertRaisesRegex(ValueError, "unsafe relative"): prepare.read_index(data)

    def test_generation_is_deterministic_and_semantic_asset_ids_are_per_product(self):
        selected = [recipe("one"), recipe("two")]
        def render(root, selected, pool, audit):
            raw = product(selected)
            body = ("<svg>" + selected["document"] + "</svg>").encode()
            raw["assets"] = [{"id": "shared-semantic-id", "body": body, "sha256": prepare.digest(body),
                              "bytes": len(body), "mime": "image/svg+xml", "src": "assets/source.svg", "role": "diagram"}]
            return raw
        first = self.root / ".scratch/first"; second = self.root / ".scratch/second"
        self.run_generate(selected, render, first); self.run_generate(selected, render, second)
        files = lambda folder: {path.relative_to(folder).as_posix(): path.read_bytes() for path in folder.rglob("*.json")}
        self.assertEqual(files(first), files(second))
        with patch.object(producer, "render_product", side_effect=AssertionError("cached reads must not render")):
            index = prepare.read_index(first)
            mappings = [prepare.read_product(first, row)["asset_ids"] for row in index["products"]]
            self.assertEqual(len(index["assets"]), 2)
            self.assertEqual(set(mappings[0]), {"shared-semantic-id"})
            self.assertNotEqual(mappings[0], mappings[1])
            for row in index["assets"]: prepare.read_asset(first, row)


if __name__ == "__main__":
    unittest.main()
