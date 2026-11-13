"""Web and native assembly use current shared content without leaf rewrites."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from unittest.mock import patch

from tools.tests import test_document_types as fixture
from tools.tests.test_web_edition import DRIVER
from pathlib import Path

types = fixture.types


class DocumentAssemblyTests(unittest.TestCase):
    setUp = fixture.FixtureTests.setUp
    declare = fixture.FixtureTests.declare

    def assembly(self):
        return types.Assembly(self.root, projections=self.projections)

    def test_current_template_and_projection_override_stale_or_missing_snapshots(self):
        self.declare()
        main = self.leaf / "main.tex"
        main.write_text("Old generated entrypoint.\n")
        generated = self.leaf / "generated/fake.tex"
        generated.parent.mkdir()
        generated.write_text("Old generated page.\n")
        held = {path: path.read_bytes() for path in (main, generated)}
        assembly = self.assembly()
        self.assertIn("fixture/leaf/generated/fake", assembly.read_text(main))
        self.assertEqual(assembly.read_text(generated), "% page for fixture/leaf\n")
        self.assertIn(self.leaf / "research/fake.toml", assembly.files(self.leaf))
        self.assertEqual(held, {path: path.read_bytes() for path in held})
        generated.unlink()
        self.assertTrue(self.assembly().is_file(generated))
        self.assertFalse(generated.exists())

    def test_prefetched_dependency_traces_finish_exactly_as_asked_one_at_a_time(self):
        self.declare()
        traced = []
        projection = self.projections["fake"]

        def dependency_trace(context):
            traced.append(context.document)
            return {"reads": ["src/common/read.json"]}

        def dependencies(context, trace=None):
            trace = dependency_trace(context) if trace is None else trace
            return {context.root / value for value in trace["reads"]}

        projection.dependency_trace = dependency_trace
        projection.dependencies = dependencies
        alone = self.assembly().dependencies(self.leaf)
        self.assertEqual(traced, ["fixture/leaf"])
        assembly = self.assembly()
        assembly.prefetch_dependencies([self.leaf, self.leaf], jobs=2)
        self.assertEqual(traced, ["fixture/leaf", "fixture/leaf"])
        self.assertEqual(assembly.dependencies(self.leaf), alone)
        self.assertEqual(len(traced), 2)
        self.assertIn(self.root / "src/common/read.json", alone)

        def failing(context):
            raise types.DocumentTypeError("trace refused")

        projection.dependency_trace = failing
        assembly = self.assembly()
        assembly.prefetch_dependencies([self.leaf])
        with self.assertRaisesRegex(types.DocumentTypeError, "trace refused"):
            assembly.dependencies(self.leaf)

    def test_web_input_and_companion_selection_use_the_same_current_projection(self):
        self.declare()
        (self.root / "src/common/preamble.tex").write_text("% shared preamble\n")
        main = self.leaf / "main.tex"
        main.write_text("Old generated entrypoint.\n")
        with patch.object(DRIVER, "SRC", self.root / "src"), \
                patch.object(types, "discover_projections", return_value=self.projections):
            assembly = self.assembly()
            source = DRIVER.assemble(assembly.read_text(main), "claude", {}, assembly=assembly)
            self.assertIn("% page for fixture/leaf", source)
            self.assertNotIn("Old generated", source)
            selection = DRIVER.edition_selection("claude", main, "main")
            self.assertIn("% page for fixture/leaf", selection["source"])
            self.assertNotIn("Old generated", selection["canonical_body"])
        self.assertEqual(main.read_text(), "Old generated entrypoint.\n")

    def test_stage_changes_only_for_current_rendered_bytes_and_never_changes_leaf(self):
        self.declare()
        main = self.leaf / "main.tex"
        main.write_text("Old generated entrypoint.\n")
        destination = self.root / ".scratch/assembly"
        with patch.object(types, "discover_projections", return_value=self.projections):
            entry = types.stage(self.root, "claude", "fixture/leaf/main.tex", destination)
            manifest = destination / "manifest.json"
            previous = manifest.stat().st_mtime_ns
            original = manifest.read_bytes()
            types.stage(self.root, "claude", "fixture/leaf/main.tex", destination)
            self.assertEqual(manifest.stat().st_mtime_ns, previous)
            template = self.root / types.TYPES_DIR / "fixture-v1/main.template.tex"
            template.write_text(template.read_text().replace("\\title", "Fresh shared words.\n\\title"))
            types.stage(self.root, "claude", "fixture/leaf/main.tex", destination)
            self.assertNotEqual(manifest.read_bytes(), original)
            self.assertIn("Fresh shared words.", entry.read_text())
            paths = {row["path"] for row in json.loads(manifest.read_text())}
            self.assertIn("src/claude/fixture/leaf/generated/fake.tex", paths)
        self.assertEqual(main.read_text(), "Old generated entrypoint.\n")

    def test_an_orphan_generated_file_is_refused_without_rewriting_it(self):
        self.declare()
        orphan = self.leaf / "generated/orphan.tex"
        orphan.parent.mkdir()
        orphan.write_text("Old content.\n")
        with self.assertRaisesRegex(types.DocumentTypeError, "orphaned generated"):
            self.assembly().files(self.leaf)
        self.assertTrue(orphan.is_file())

    def test_staging_refuses_repository_unowned_directories_and_symlinks(self):
        self.declare()
        authored = self.leaf / "sections/10-a.tex"
        original = authored.read_bytes()
        unowned = self.root / ".scratch/unowned"
        unowned.mkdir(parents=True)
        other = unowned / "preserve.txt"
        other.write_text("Unrelated content.\n")
        linked = self.root / ".scratch/linked"
        linked.symlink_to(unowned, target_is_directory=True)
        with patch.object(types, "discover_projections", return_value=self.projections):
            for destination in (self.root, self.root.parent, self.root / "src", unowned, linked / "output"):
                with self.subTest(destination=destination), self.assertRaises(types.DocumentTypeError):
                    types.stage(self.root, "claude", "fixture/leaf/main.tex", destination)
        self.assertEqual(authored.read_bytes(), original)
        self.assertEqual(other.read_text(), "Unrelated content.\n")

    def test_owned_stage_preserves_unrelated_files_and_refuses_changed_generated_files(self):
        self.declare()
        destination = self.root / ".scratch/assembly"
        with patch.object(types, "discover_projections", return_value=self.projections):
            types.stage(self.root, "claude", "fixture/leaf/main.tex", destination)
            unrelated = destination / "src/claude/fixture/leaf/unrelated.tex"
            unrelated.write_text("Preserve this file.\n")
            types.stage(self.root, "claude", "fixture/leaf/main.tex", destination)
            self.assertEqual(unrelated.read_text(), "Preserve this file.\n")
            generated = destination / "src/claude/fixture/leaf/generated/fake.tex"
            generated.write_text("An operator changed this copy.\n")
            with self.assertRaisesRegex(types.DocumentTypeError, "modified staged content"):
                types.stage(self.root, "claude", "fixture/leaf/main.tex", destination)
            self.assertEqual(generated.read_text(), "An operator changed this copy.\n")


class ChronologyAssemblyCacheTests(unittest.TestCase):
    def test_new_assembly_observes_changed_canonical_chronology_without_rewriting_leaf(self):
        root = fixture.ROOT
        scratch = root / ".scratch/assembly-audit/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        document = "liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost"
        with tempfile.TemporaryDirectory(dir=scratch) as temporary:
            checkout = Path(temporary)
            leaf = checkout / "src/claude" / document
            shutil.copytree(root / "src/claude" / document, leaf)
            (checkout / "src/common").symlink_to(root / "src/common", target_is_directory=True)
            sources = checkout / "src/sources"
            sources.mkdir()
            for name in ("works", "bibles", "calendars"):
                (sources / name).symlink_to(root / "src/sources" / name, target_is_directory=True)
            shutil.copytree(root / "src/sources/chronology", sources / "chronology")
            table = leaf / "research/chronology-annotations.tex"
            held = table.read_bytes()
            before = types.Assembly(checkout).read_text(table)
            orientation = sources / "chronology/orientation.yaml"
            text = orientation.read_text()
            self.assertIn("composition.gospel-of-matthew: Matthew", text)
            orientation.write_text(text.replace("composition.gospel-of-matthew: Matthew",
                                                "composition.gospel-of-matthew: Updated Matthew label"))
            after = types.Assembly(checkout).read_text(table)
            self.assertNotEqual(before, after)
            self.assertIn("Updated Matthew label", after)
            self.assertEqual(table.read_bytes(), held)


if __name__ == "__main__":
    unittest.main()
