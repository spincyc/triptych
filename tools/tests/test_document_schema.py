from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _document_schema as schema  # noqa: E402


class DocumentSchemaTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/schema-core"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.leaf = self.root / "src/gpt/articles/faith/example"
        (self.leaf / "research").mkdir(parents=True)
        (self.leaf / "main.tex").write_text("Substantive body.\n", encoding="utf-8")
        (self.leaf / "research/scope.md").write_text("Actual bounded scope.\n", encoding="utf-8")
        (self.leaf / "research/source-audit.md").write_text("Actual sources and loci.\n", encoding="utf-8")
        self.data = schema.adapter_manifest(self.root, self.leaf)

    def write(self, data=None):
        path = self.leaf / "publication.toml"
        path.write_text(schema.dumps_manifest(data or self.data), encoding="utf-8")
        return path

    def load(self):
        return schema.load_manifest(self.root, self.write())

    def test_roundtrip_and_normalized_record_revalidation(self):
        record = self.load()
        self.assertEqual(record["id"], "gpt/articles/faith/example")
        self.assertEqual(record["outputs"][0]["source_path"], "src/gpt/articles/faith/example/main.tex")
        self.assertTrue(schema.validate(self.root, record)["ok"])
        self.assertEqual(schema.dumps_manifest(record), schema.dumps_manifest(self.data))

    def test_identity_and_validation_read_through_the_callers_operation_assembly(self):
        from unittest import mock
        import _document_types
        record = self.load()
        alone = schema.identities(self.root, record)
        assembly = _document_types.Assembly(self.root)
        with mock.patch.object(_document_types, "Assembly",
                               side_effect=AssertionError("the caller's assembly was not used")):
            shared = schema.identities(self.root, record, assembly=assembly)
            self.assertTrue(schema.validate(self.root, record, assembly=assembly)["ok"])
        self.assertEqual(alone, shared)

    def test_identity_and_closure_use_current_template_without_refreshing_leaf(self):
        type_dir = self.root / "src/common/document-types/article-fixture-v1"
        type_dir.mkdir(parents=True)
        (type_dir / "type.toml").write_text('''schema = 1
record_type = "document-type"
id = "article-fixture-v1"
description = "Assembly identity fixture"
kinds = ["article-faith"]
[editions.main]
role = "canonical"
template = "main.template.tex"
entrypoint = "main.tex"
regions = ["body"]
''')
        template = type_dir / "main.template.tex"
        template.write_text("%@ region body\n")
        (self.leaf / "body.tex").write_text("Current authored section.\n")
        manifest = self.write()
        with manifest.open("a") as stream:
            stream.write('\n[document]\ntype = "article-fixture-v1"\n'
                         '[document.main]\nbody = ["body"]\n')
        record = schema.load_manifest(self.root, manifest)
        entry = self.leaf / "main.tex"
        original = entry.read_text()
        first = schema.identities(self.root, record)
        self.assertEqual(entry.read_text(), original)
        self.assertIn("src/gpt/articles/faith/example/body.tex", first["content"]["inputs"])
        entry.write_text("Stale saved projection with a bogus \\input{missing}.\n")
        stale = schema.identities(self.root, record)
        self.assertEqual(first["content"]["sha256"], stale["content"]["sha256"])
        template.write_text("Current shared introduction.\n%@ region body\n")
        revised = schema.identities(self.root, record)
        self.assertNotEqual(first["content"]["sha256"], revised["content"]["sha256"])
        self.assertNotEqual(first["render"]["sha256"], revised["render"]["sha256"])

    def test_validation_and_identity_accept_one_operation_assembly(self):
        from _document_types import Assembly
        record = self.load()
        expected = schema.identities(self.root, record)
        assembly = Assembly(self.root)
        with mock.patch("_document_types.Assembly", side_effect=AssertionError("new assembly")):
            self.assertTrue(schema.validate(self.root, record, assembly=assembly)["ok"])
            self.assertEqual(schema.identities(self.root, record, assembly=assembly), expected)
        foreign = Assembly(self.root / "other")
        self.assertFalse(schema.validate(self.root, record, assembly=foreign)["ok"])
        with self.assertRaisesRegex(schema.SchemaError, "another repository"):
            schema.identities(self.root, record, assembly=foreign)

    def test_a_minimal_manifest_derives_everything_its_path_and_records_state(self):
        # The leaf's path, its registered kind and its research records say
        # all of this; the manifest need not (guidance/document-schemas.md).
        (self.leaf / "publication.toml").write_text("", encoding="utf-8")
        record = schema.load_manifest(self.root, self.leaf / "publication.toml")
        for key in ("schema_version", "id", "kind", "profile", "source_format", "entrypoint", "outputs"):
            with self.subTest(field=key):
                self.assertEqual(record[key], self.data[key] if key != "outputs" else record[key])
        self.assertEqual([{k: o[k] for k in schema.OUTPUT_FIELDS} for o in record["outputs"]],
                         self.data["outputs"])
        self.assertEqual(sorted((item["role"], item.get("source")) for item in record["structure"]),
                         sorted((item["role"], item.get("source")) for item in self.data["structure"]))
        self.assertTrue(schema.validate(self.root, record, phase="content")["ok"])
        self.assertEqual(schema.minimal_manifest(self.root, record), {"structure": []})

    def test_an_explicit_value_must_agree_with_its_derivation(self):
        for line in ('kind = "article-scripture"', 'id = "gpt/articles/faith/other"',
                     'profile = "guidance/biographies.md"', 'entrypoint = "body.tex"',
                     'schema_version = 2', 'source_format = "structured"',
                     'canonical_owner = "gpt/articles/faith/other"',
                     '[[outputs]]\nid = "gpt/articles/faith/example"\nrole = "canonical"\n'
                     'entrypoint = "main.tex"\nderivation = "projection"'):
            with self.subTest(line=line):
                path = self.leaf / "publication.toml"
                path.write_text(line + "\n", encoding="utf-8")
                with self.assertRaises(schema.SchemaError):
                    schema.load_manifest(self.root, path)
        # An explicit value that agrees is redundant, not wrong.
        path.write_text('kind = "article-faith"\nid = "gpt/articles/faith/example"\n', encoding="utf-8")
        self.assertEqual(schema.load_manifest(self.root, path)["kind"], "article-faith")

    def test_a_missing_required_record_is_still_refused(self):
        (self.leaf / "publication.toml").write_text("", encoding="utf-8")
        (self.leaf / "research/source-audit.md").unlink()
        record = schema.load_manifest(self.root, self.leaf / "publication.toml")
        report = schema.validate(self.root, record, phase="content")
        self.assertIn("missing required role: source-audit", report["errors"])

    def test_a_release_record_derives_its_id_version_and_kind_catalog(self):
        path = self.root / "release/publications/gpt/articles/faith/example.json"
        path.parent.mkdir(parents=True)
        path.write_text('{"status": "alpha", "authorization": "standing"}\n', encoding="utf-8")
        self.assertEqual(schema.release_record(self.root, path), {
            "status": "alpha", "authorization": "standing", "schema_version": 1,
            "id": "articles/faith/example", "catalog": "library/faith.md"})
        for field, value in (("id", "articles/faith/other"), ("catalog", "library/prayer.md"),
                             ("schema_version", 2)):
            with self.subTest(field=field):
                path.write_text(json.dumps({"status": "hold", "authorization": None, field: value}))
                with self.assertRaisesRegex(schema.SchemaError, "contradicts its derivation"):
                    schema.release_record(self.root, path)
        self.assertEqual(schema.minimal_release_record(
            self.root, "gpt", "articles/faith/example",
            {"schema_version": 1, "id": "articles/faith/example", "catalog": "library/faith.md",
             "status": "alpha", "authorization": "standing"}),
            {"status": "alpha", "authorization": "standing"})

    def test_a_component_manifest_derives_its_identity_entrypoints_and_outputs(self):
        import _proper_components as components

        leaf = self.root / "src/gpt/liturgy/roman-rite/postconciliar/edition/propers/temporal/x"
        derived = components.derived_fields(
            {"schema": 2, "appointed_text_completeness": "rights-limited"}, leaf)
        document = "liturgy/roman-rite/postconciliar/edition/propers/temporal/x"
        self.assertEqual(derived["document"], document)
        self.assertEqual(derived["calendar"], "postconciliar")
        self.assertEqual(derived["homily_entrypoint"], "homily.tex")
        self.assertEqual(derived["outputs"], {
            "research": document, "synthesis": document + "-synthesis",
            "homily": document + "-homily", "web": document,
            "canonical_label": "Research PDF", "synthesis_label": "Synthesis PDF",
            "homily_label": "Homily PDF"})
        # An explicit value stays as written, for the validators to refuse.
        self.assertEqual(components.complete({"schema": 2, "document": "other"}, leaf)["document"], "other")
        with self.assertRaisesRegex(ValueError, "outputs.research"):
            components.outputs(components.complete(
                {"schema": 2, "appointed_text_completeness": "complete",
                 "outputs": {"research": "other"}}, leaf))

    def test_discovery_retains_missing_and_invalid_manifest_leaves(self):
        missing = schema.discover(self.root)
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0]["manifest_origin"], "adapter")
        self.assertFalse(schema.validate(self.root, missing[0])["ok"])
        self.write()
        (self.leaf / "publication.toml").write_text("malformed = [", encoding="utf-8")
        invalid = schema.discover(self.root)
        self.assertEqual(len(invalid), 1)
        self.assertIn("discovery_error", invalid[0])

    def test_orphan_manifest_is_reported(self):
        self.write()
        (self.leaf / "main.tex").unlink()
        records = schema.discover(self.root)
        self.assertEqual(len(records), 1)
        self.assertIn("orphan", records[0]["discovery_error"])

    def test_unknown_fields_rejected_at_every_level(self):
        for location in ("publication", "output", "structure", "contracts"):
            with self.subTest(location=location):
                data = copy.deepcopy(self.data)
                target = data if location == "publication" else data["outputs"][0] if location == "output" else data["structure"][0] if location == "structure" else data.setdefault("contracts", {})
                target["invented"] = "bad"
                # Serializer is strict too; hand-written input exercises loader.
                text = schema.dumps_manifest(self.data)
                if location == "publication":
                    text = 'invented="bad"\n' + text
                elif location == "contracts":
                    text += '\n[contracts]\ninvented="bad"\n'
                else:
                    text = text.replace(f"[[{location if location == 'structure' else 'outputs'}]]", f"[[{location if location == 'structure' else 'outputs'}]]\ninvented=\"bad\"", 1)
                path = self.leaf / "publication.toml"
                path.write_text(text, encoding="utf-8")
                with self.assertRaisesRegex(schema.SchemaError, "unknown fields"):
                    schema.load_manifest(self.root, path)

    def test_unknown_kind_and_wrong_profile_and_owner_are_rejected(self):
        for key, value in (("kind", "unregistered"), ("profile", "guidance/biographies.md"),
                           ("id", "claude/articles/faith/example")):
            data = dict(self.data, **{key: value})
            with self.subTest(key=key), self.assertRaises(schema.SchemaError):
                schema.load_manifest(self.root, self.write(data))

    def test_no_traversal_absolute_or_noncanonical_paths(self):
        for path in ("../secret.tex", "/tmp/secret.tex", "part/../secret.tex", "./main.tex", "a//b.tex", "C:/secret.tex", "a\\b.tex"):
            data = copy.deepcopy(self.data)
            data["structure"][0]["source"] = path
            with self.subTest(path=path), self.assertRaises(schema.SchemaError):
                schema.load_manifest(self.root, self.write(data))

    def test_symlink_cannot_escape_repository_leaf_or_provider(self):
        other = self.root / "src/claude/articles/faith/other.tex"
        other.parent.mkdir(parents=True)
        other.write_text("Other provider.\n", encoding="utf-8")
        link = self.leaf / "linked.tex"
        link.symlink_to(other)
        data = copy.deepcopy(self.data)
        data["structure"][0]["source"] = "linked.tex"
        with self.assertRaises(schema.SchemaError):
            schema.load_manifest(self.root, self.write(data))

    def test_missing_or_directory_inputs_and_cross_provider_data_rejected(self):
        for item in ({"role": "body", "source": "missing.tex"},
                     {"role": "body", "source": "research"},
                     {"role": "body", "source": "missing/*.tex"},
                     {"role": "body", "data": "src/claude/other.tex"}):
            data = copy.deepcopy(self.data)
            data["structure"] = [item]
            with self.subTest(item=item), self.assertRaises(schema.SchemaError):
                schema.load_manifest(self.root, self.write(data))

    def test_structure_cycles_and_unknown_dependencies_rejected(self):
        for dependencies in (("b", "a"), ("unknown", "")):
            data = copy.deepcopy(self.data)
            data["structure"] = [
                {"key": "a", "role": "body", "source": "main.tex", "depends_on": [dependencies[0]]},
                {"key": "b", "role": "argument", "source": "main.tex", "depends_on": [dependencies[1]] if dependencies[1] else []},
            ]
            with self.subTest(dependencies=dependencies), self.assertRaises(schema.SchemaError):
                schema.load_manifest(self.root, self.write(data))

    def test_literal_include_cycle_rejected_without_executing_tex(self):
        (self.leaf / "main.tex").write_text("\\input{second}\n", encoding="utf-8")
        (self.leaf / "second.tex").write_text("\\input{main}\n", encoding="utf-8")
        report = schema.validate(self.root, self.load())
        self.assertFalse(report["ok"])
        self.assertTrue(any("cycle" in x for x in report["errors"]))

    def test_computed_tex_is_recorded_as_unproven_not_executed(self):
        (self.leaf / "main.tex").write_text("\\input{\\ChosenSource}\n", encoding="utf-8")
        result = schema.identities(self.root, self.load())
        self.assertTrue(any("computed input" in x for x in result["limitations"]))

    def test_missing_literal_input_is_a_source_error(self):
        (self.leaf / "main.tex").write_text("\\input{does-not-exist}\n", encoding="utf-8")
        report = schema.validate(self.root, self.load())
        self.assertFalse(report["ok"])
        self.assertTrue(any("unresolved literal input" in e for e in report["errors"]))

    def test_declared_markdown_owner_is_discovered_without_a_tex_marker(self):
        data = copy.deepcopy(self.data)
        data["source_format"] = "markdown"
        data["entrypoint"] = "main.md"
        data["outputs"][0]["entrypoint"] = "main.md"
        data["structure"][0]["source"] = "main.md"
        (self.leaf / "main.md").write_text("# Subject\n\nSubstantive argument.\n", encoding="utf-8")
        (self.leaf / "main.tex").unlink()
        self.write(data)
        records = schema.discover(self.root)
        self.assertEqual(len(records), 1)
        self.assertNotIn("discovery_error", records[0])
        self.assertTrue(schema.validate(self.root, records[0])["ok"])

    def test_outputs_have_exact_ownership_and_derivation(self):
        for change in ({"id": "gpt/articles/faith/other"}, {"derivation": "projection"}, {"role": "homily"}):
            data = copy.deepcopy(self.data)
            data["outputs"][0].update(change)
            with self.subTest(change=change), self.assertRaises(schema.SchemaError):
                schema.load_manifest(self.root, self.write(data))

    def test_schema_two_companions_are_authored_and_schema_one_projection(self):
        for version in (1, 2):
            with self.subTest(version=version):
                leaf = self.root / f"src/gpt/liturgy/roman-rite/1962/propers/temporal/{version:02d}-example"
                leaf.mkdir(parents=True)
                for name in ("main.tex", "synthesis.tex", "homily.tex"):
                    (leaf / name).write_text("Actual prose.\n", encoding="utf-8")
                (leaf / "proper-components.toml").write_text(f"schema={version}\n", encoding="utf-8")
                data = schema.adapter_manifest(self.root, leaf)
                roles = {o["role"]: o["derivation"] for o in data["outputs"]}
                self.assertEqual(roles["synthesis"], "authored" if version == 2 else "projection")
                self.assertEqual("homily" in roles, version == 2)

    def test_selected_edition_allows_future_companions_but_full_validation_refuses(self):
        leaf = self.root / "src/gpt/liturgy/roman-rite/1962/propers/temporal/67-example"
        leaf.mkdir(parents=True)
        (leaf / "main.tex").write_text("Complete study.\n", encoding="utf-8")
        (leaf / "proper-components.toml").write_text("schema=2\n", encoding="utf-8")
        manifest = leaf / "publication.toml"
        manifest.write_text('''[[structure]]
role = "companion-exposition"
source = "sections/future-synthesis.tex"
outputs = ["synthesis"]
''', encoding="utf-8")
        record = schema.load_manifest(self.root, manifest, output_entrypoint="main.tex")
        self.assertEqual([o["role"] for o in record["outputs"]],
                         ["canonical", "synthesis", "homily"])
        with self.assertRaisesRegex(schema.SchemaError, "input has no existing file"):
            schema.load_manifest(self.root, manifest)
        with self.assertRaisesRegex(schema.SchemaError, "input has no existing file"):
            schema.load_manifest(self.root, manifest, output_entrypoint="synthesis.tex")
        with self.assertRaisesRegex(schema.SchemaError, "input has no existing file"):
            schema.load_manifest(self.root, manifest, output_entrypoint="homily.tex")
        with self.assertRaisesRegex(schema.SchemaError, "one declared output"):
            schema.load_manifest(self.root, manifest, output_entrypoint="other.tex")
        (leaf / "main.tex").unlink()
        with self.assertRaisesRegex(schema.SchemaError, "input has no existing file"):
            schema.load_manifest(self.root, manifest, output_entrypoint="main.tex")

    def test_selected_edition_keeps_shared_inputs_and_other_output_ownership_checks(self):
        manifest = self.write()
        (self.leaf / "research/scope.md").unlink()
        with self.assertRaisesRegex(schema.SchemaError, "input has no existing file"):
            schema.load_manifest(self.root, manifest, output_entrypoint="main.tex")
        (self.leaf / "research/scope.md").write_text("Restored scope.\n", encoding="utf-8")
        (self.leaf / "proper-components.toml").write_text("schema=2\n", encoding="utf-8")
        manifest.write_text("# Derived declarations.\n", encoding="utf-8")
        other = self.root / "src/claude/other/main.tex"
        other.parent.mkdir(parents=True)
        other.write_text("Other provider.\n", encoding="utf-8")
        (self.leaf / "synthesis.tex").symlink_to(other)
        with self.assertRaisesRegex(schema.SchemaError, "output entrypoint escapes"):
            schema.load_manifest(self.root, manifest, output_entrypoint="main.tex")

    def test_audit_and_render_source_changes_have_distinct_identities(self):
        record = self.load()
        before = schema.identities(self.root, record)
        (self.leaf / "research/source-audit.md").write_text("New audit finding.\n", encoding="utf-8")
        audit = schema.identities(self.root, record)
        self.assertNotEqual(before["evidence"]["sha256"], audit["evidence"]["sha256"])
        self.assertEqual(before["content"]["sha256"], audit["content"]["sha256"])
        self.assertEqual(before["render"]["sha256"], audit["render"]["sha256"])
        (self.leaf / "main.tex").write_text("Changed argument.\n", encoding="utf-8")
        changed = schema.identities(self.root, record)
        self.assertNotEqual(audit["content"]["sha256"], changed["content"]["sha256"])
        self.assertNotEqual(audit["outputs"]["canonical"]["sha256"], changed["outputs"]["canonical"]["sha256"])

    def test_review_dependency_metadata_changes_evidence_not_content(self):
        dependency = self.root / "src/sources/inventories/rights.toml"
        dependency.parent.mkdir(parents=True)
        dependency.write_text('right="permitted"\n', encoding="utf-8")
        (self.leaf / "research/review-dependencies.toml").write_text('paths=["src/sources/inventories/rights.toml"]\n', encoding="utf-8")
        record = self.load()
        before = schema.identities(self.root, record)
        dependency.write_text('right="restricted"\n', encoding="utf-8")
        after = schema.identities(self.root, record)
        self.assertNotEqual(before["evidence"]["sha256"], after["evidence"]["sha256"])
        self.assertEqual(before["content"]["sha256"], after["content"]["sha256"])

    def test_operational_review_receipts_do_not_invalidate_their_own_identity(self):
        record = self.load()
        before = schema.identities(self.root, record)
        for filename in ("production-review.md", "artifacts.json", "web-artifact.json", "standing-findings.json"):
            (self.leaf / "research" / filename).write_text("New acceptance or installation receipt.\n", encoding="utf-8")
        after = schema.identities(self.root, record)
        self.assertEqual(before["content"]["sha256"], after["content"]["sha256"])
        self.assertEqual(before["evidence"]["sha256"], after["evidence"]["sha256"])
        self.assertEqual(before["outputs"]["canonical"]["sha256"], after["outputs"]["canonical"]["sha256"])

    def test_web_inspection_receipts_do_not_invalidate_the_reviewed_identity(self):
        path = self.leaf / "web-edition.toml"
        declaration = 'eligibility="eligible"\nreviewed="2026-11-04"\n'
        path.write_text(declaration)
        record = self.load()
        before = schema.identities(self.root, record)
        inspection = ('inspected="2026-11-05"\ninspected_by="gpt fixture"\n'
                      'inspection="Compared exact reader bytes with source."\n')
        for tables in ("", "[companions.synthesis]\n", "[companions.homily]\n"):
            with self.subTest(table=tables):
                path.write_text(declaration + tables + inspection)
                self.assertEqual(before, schema.identities(self.root, record))
                path.write_text(path.read_text().replace("gpt fixture", "updated actual reviewer"))
                self.assertEqual(before, schema.identities(self.root, record))

    def test_reader_declaration_decisions_remain_part_of_identity(self):
        path = self.leaf / "web-edition.toml"
        declaration = ('eligibility="eligible"\nreviewed="2026-11-04"\n'
                       'blocking_constructs=[]\ncontents=false\n')
        path.write_text(declaration)
        record = self.load()
        before = schema.identities(self.root, record)
        for changed in (
            declaration.replace('"eligible"', '"conditional"'),
            declaration.replace("2026-11-04", "2026-11-05"),
            declaration.replace("[]", '["wide-table"]'),
            declaration.replace("false", "true"),
            declaration + 'withdrawn="2026-11-05"\n',
        ):
            with self.subTest(declaration=changed):
                path.write_text(changed)
                after = schema.identities(self.root, record)
                for identity in ("content", "render", "outputs"):
                    self.assertNotEqual(before[identity], after[identity])

    def test_inspection_named_fields_outside_recognized_receipts_remain_sealed(self):
        path = self.leaf / "web-edition.toml"
        declaration = 'eligibility="eligible"\n'
        path.write_text(declaration)
        record = self.load()
        before = schema.identities(self.root, record)
        for table in ("unrelated", "companions.other", "companions.synthesis.unrelated"):
            with self.subTest(table=table):
                path.write_text(declaration + f'[{table}]\ninspection="Content, not a receipt."\n')
                self.assertNotEqual(before, schema.identities(self.root, record))
        path.write_text(declaration)
        unrelated = self.leaf / "research/other.toml"
        unrelated.write_text('inspection="First evidence judgment."\n')
        before = schema.identities(self.root, record)
        unrelated.write_text('inspection="Changed evidence judgment."\n')
        self.assertNotEqual(before, schema.identities(self.root, record))

    def test_declared_dependencies_cannot_smuggle_other_provider_or_scratch(self):
        other = self.root / "src/claude/shared.tex"
        other.parent.mkdir(parents=True)
        other.write_text("Other provider substance.\n", encoding="utf-8")
        scratch = self.root / ".scratch/private.txt"
        scratch.parent.mkdir()
        scratch.write_text("Transient.\n", encoding="utf-8")
        for pattern in ("src/claude/shared.tex", ".scratch/private.txt"):
            data = dict(self.data, content_inputs=[pattern])
            with self.subTest(pattern=pattern), self.assertRaises(schema.SchemaError):
                schema.load_manifest(self.root, self.write(data))

    def test_render_gates_cover_every_pdf_and_content_gates_need_no_pdf(self):
        record = self.load()
        render = schema.gates(self.root, record, "render")
        self.assertIn("--pdf", render[0]["command"])
        content = schema.gates(self.root, record, "content")
        self.assertNotIn("--pdf", content[0]["command"])

    def test_review_dependency_directory_and_explicit_text_use_metadata_owner(self):
        artifact = self.root / "src/sources/works/author/book/editions/edition/artifacts/witness"
        artifact.mkdir(parents=True)
        manifest = artifact / "artifact.toml"
        manifest.write_text('sha256="' + 'a' * 64 + '"\n', encoding="utf-8")
        payload = artifact / "witness.txt"
        payload.write_text("Received source text.\n", encoding="utf-8")
        directory = artifact.relative_to(self.root).as_posix()
        direct = payload.relative_to(self.root).as_posix()
        (self.leaf / "research/review-dependencies.toml").write_text(f'paths=["{directory}","{direct}"]\n', encoding="utf-8")
        record = self.load()
        before = schema.identities(self.root, record)
        self.assertIn(manifest.relative_to(self.root).as_posix(), before["evidence"]["inputs"])
        self.assertNotIn(direct, before["evidence"]["inputs"])
        payload.write_text("Changed payload; metadata receipt still pins its prior hash.\n", encoding="utf-8")
        self.assertEqual(before["evidence"]["sha256"], schema.identities(self.root, record)["evidence"]["sha256"])
        payload.unlink()
        self.assertEqual(before["evidence"]["sha256"], schema.identities(self.root, record)["evidence"]["sha256"])
        self.assertEqual(schema.evidence_metadata(self.root, [payload]), {manifest})

    def test_bound_artifact_metadata_ancestry_changes_without_reading_payload(self):
        work = self.root / "src/sources/works/author/book"
        artifact = work / "editions/edition/artifacts/witness"
        artifact.mkdir(parents=True)
        (work / "work.toml").write_text('schema=1\nrecord_type="work"\nid="work.author.book"\ntitle="Book"\nresponsible="Author"\n', encoding="utf-8")
        edition = work / "editions/edition/edition.toml"
        edition.write_text('schema=1\nrecord_type="edition"\nid="edition.author.book.edition"\nwork_id="work.author.book"\ntitle="Edition"\nlanguage="en"\n', encoding="utf-8")
        manifest = artifact / "artifact.toml"
        manifest.write_text('schema=1\nrecord_type="artifact"\nid="artifact.author.book.edition.witness"\nedition_id="edition.author.book.edition"\nsha256="' + 'a' * 64 + '"\n', encoding="utf-8")
        payload = artifact / "witness.pdf"
        payload.write_bytes(b"External witness; identity must not read these bytes.")
        (self.leaf / "research/source-bindings.toml").write_text('schema=2\nrecord_type="bindings"\n[[bindings]]\nsource_id="artifact.author.book.edition.witness"\n', encoding="utf-8")
        # Seed canonical ID paths as a loader-independent fixture; the source
        # library's own validation has separate exhaustive coverage.
        schema._SOURCE_INDEX[self.root] = {
            "work.author.book": work / "work.toml",
            "edition.author.book.edition": edition,
            "artifact.author.book.edition.witness": manifest,
        }
        record = self.load()
        before = schema.identities(self.root, record)
        payload.write_bytes(b"Different bytes; exhaustive evidence verification owns this check.")
        self.assertEqual(before["evidence"]["sha256"], schema.identities(self.root, record)["evidence"]["sha256"])
        manifest.write_text(manifest.read_text() + 'rights="restricted"\n', encoding="utf-8")
        after = schema.identities(self.root, record)
        self.assertNotEqual(before["evidence"]["sha256"], after["evidence"]["sha256"])
        self.assertIn(manifest.relative_to(self.root).as_posix(), after["evidence"]["inputs"])
        self.assertNotIn(payload.relative_to(self.root).as_posix(), after["evidence"]["inputs"])

    def test_content_cannot_claim_main_tex_is_a_missing_source_audit(self):
        record = self.load()
        for item in record["structure"]:
            if item["role"] == "source-audit":
                item["source"] = "main.tex"
        report = schema.validate(self.root, record, phase="content")
        self.assertFalse(report["ok"])
        self.assertTrue(any("bounded canonical record" in error for error in report["errors"]))

    def test_cli_reports_nonzero_for_missing_manifests_and_invalid_content(self):
        command = [sys.executable, str(ROOT / "tools/document-schema"), "check", "--root", str(self.root), "--json"]
        process = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(process.returncode, 2)
        report = json.loads(process.stdout)
        self.assertEqual(report["documents"], 1)
        self.assertEqual(report["status"], "error")

    def test_optional_neutral_sources_do_not_change_provider_census_or_default(self):
        self.write()
        command = [sys.executable, str(ROOT / "tools/document-schema"), "check", "--root", str(self.root), "--json"]
        default = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(default.returncode, 0, default.stdout + default.stderr)
        provider = json.loads(default.stdout)
        self.assertNotIn("source_editions", provider)
        included = subprocess.run(command + ["--include-sources"], capture_output=True, text=True)
        self.assertEqual(included.returncode, 2, included.stdout + included.stderr)
        report = json.loads(included.stdout)
        self.assertEqual((report["documents"], report["outputs"]), (1, 1))
        self.assertEqual(report["provider_errors"], 0)
        self.assertGreater(report["source_errors"], 0)
        self.assertEqual(report["source_editions"]["id"], "source-editions")


if __name__ == "__main__":
    unittest.main()
