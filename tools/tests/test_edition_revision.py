"""The derived "Last revised" stamp: its closure, its history, and its refusals."""
from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _edition_revision as revision  # noqa: E402

GENERATED = revision.GENERATED_HEADER + " from src/common/document-types/x/main.template.tex\n"
NOW = dt.datetime(2026, 11, 4, 20, 0, 0, tzinfo=dt.timezone.utc)


def stamp(seconds: int) -> str:
    return dt.datetime.fromtimestamp(seconds, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Fixture(unittest.TestCase):
    """A small repository whose commit times the test chooses."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / "repository"
        self.root.mkdir()
        self.clock = 1_780_000_000
        self.git("init", "-q", "-b", "main")
        self.write("src/common/preamble.tex", "% shared typesetting\n")
        self.write("src/claude/doc/main.tex",
                   "\\input{common/preamble}\n\\input{doc/sections/body}\n"
                   "\\input{doc/generated/date}\n\\input{doc/generation-metadata}\n")
        self.write("src/claude/doc/homily.tex",
                   "\\input{common/preamble}\n\\input{doc/sections/homily}\n"
                   "\\input{doc/generation-metadata}\n")
        self.write("src/claude/doc/sections/body.tex", "Body.\n")
        self.write("src/claude/doc/sections/homily.tex", "Homily.\n")
        self.write("src/claude/doc/generated/date.tex", "Dates.\n")
        self.write("src/claude/doc/generation-metadata.tex", "\\AIModelContribution{m}{q}{r}\n")
        self.first = self.commit("create")

    def git(self, *arguments: str, cwd: Path | None = None) -> str:
        environment = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.invalid",
                           GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.invalid",
                           GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            environment.pop(key, None)
        if "GIT_COMMITTER_DATE" in self.__dict__:
            environment.update(self.__dict__["GIT_COMMITTER_DATE"])
        return subprocess.run(["git", *arguments], cwd=cwd or self.root, env=environment,
                              check=True, capture_output=True, text=True).stdout

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, message: str, *, committed_later: int = 0) -> int:
        self.clock += 3600
        when = f"@{self.clock} +0000"
        later = f"@{self.clock + committed_later} +0000"
        self.__dict__["GIT_COMMITTER_DATE"] = {"GIT_COMMITTER_DATE": later, "GIT_AUTHOR_DATE": when}
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)
        return self.clock

    def derive(self, document: str = "doc") -> revision.Revision:
        return revision.revision(self.root, "claude", document, now=NOW)


class ClosureAndHistoryTests(Fixture):
    def test_new_proper_revision_does_not_require_unauthored_companions(self) -> None:
        document = "liturgy/roman-rite/1962/propers/temporal/67-example"
        leaf = "src/claude/" + document
        self.write(leaf + "/main.tex", "Complete expansive study.\n")
        self.write(leaf + "/proper-components.toml", "schema=2\n")
        self.write(leaf + "/publication.toml", "# Derived declarations.\n")
        authored = self.commit("author the expansive study")
        value = self.derive(document)
        self.assertEqual(value.timestamp, stamp(authored))
        self.assertIn(leaf + "/main.tex", value.closure)
        self.assertFalse(value.uncommitted)
        self.assertFalse((self.root / leaf / "synthesis.tex").exists())
        self.assertFalse((self.root / leaf / "homily.tex").exists())
        with self.assertRaisesRegex(revision.SchemaError, "input has no existing file"):
            revision.load_manifest(self.root, self.root / leaf / "publication.toml")

    def test_explicit_leaf_relative_render_data_is_part_of_the_revision(self) -> None:
        document = "liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/altar-server"
        leaf = "src/claude/" + document
        self.write(leaf + "/main.tex", GENERATED + "\\input{doc/sections/body}\n")
        self.write(leaf + "/publication.toml",
                   '[[structure]]\nrole = "object-records"\nsource = "objects/*.toml"\n')
        record = leaf + "/objects/chalice.toml"
        self.write(record, 'description = "Original data"\n')
        self.commit("declare leaf-relative render data")
        self.write(record, 'description = "Corrected definition"\n')
        edited = self.commit("correct the rendered object")
        value = self.derive(document)
        self.assertEqual(value.timestamp, stamp(edited))
        self.assertIn(record, value.closure)

    def test_derived_dictionary_render_data_revises_a_minimal_manifest_edition(self) -> None:
        owner = "src/claude/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary"
        leaf = owner + "/altar-server"
        document = leaf.removeprefix("src/claude/")
        self.write(leaf + "/main.tex", GENERATED + "\\input{" +
                   owner.removeprefix("src/claude/") + "/shared/body}\n")
        self.write(owner + "/shared/body.tex", "Dictionary shell.\n")
        # These roles are supplied by the owning schema, so a minimized
        # publication manifest deliberately carries none of them.
        self.write(leaf + "/publication.toml", "# All structure roles are derived.\n")
        paths = [owner + "/shared/schema/inventory-schema.toml",
                 owner + "/shared/schema/edition-selections.toml",
                 owner + "/shared/objects/chalice.toml",
                 owner + "/research/artwork-manifest.toml"]
        for path in paths:
            self.write(path, 'description = "Original data"\n')
        self.commit("create dictionary")
        self.write(paths[2], 'description = "Corrected chalice definition"\n')
        edited = self.commit("correct the rendered object")
        # Generated entrypoints and common templates still cannot move stamps.
        self.write(leaf + "/main.tex", (self.root / (leaf + "/main.tex")).read_text() +
                   "% template change\n")
        self.write("src/common/dictionary-template.tex", "% typesetting only\n")
        self.commit("retune dictionary template")
        value = self.derive(document)
        self.assertEqual(value.timestamp, stamp(edited))
        self.assertTrue(set(paths).issubset(value.closure))
        self.assertNotIn(leaf + "/publication.toml", value.closure)
        self.write(paths[1], 'description = "Changed selection"\n')
        self.assertTrue(self.derive(document).uncommitted)

    def test_shared_projection_revises_only_editions_reading_it_without_refresh(self):
        self.write("src/common/document-types/fixture-v1/type.toml", '''schema = 1
record_type = "document-type"
id = "fixture-v1"
description = "Revision fixture"
kinds = ["fixture"]
[editions.main]
role = "canonical"
template = "main.template.tex"
entrypoint = "main.tex"
regions = ["body"]
[editions.homily]
role = "homily"
template = "homily.template.tex"
entrypoint = "homily.tex"
regions = ["body"]
''')
        self.write("src/common/document-types/fixture-v1/main.template.tex",
                   "%@ region body\n%@ slot fake/page\n")
        self.write("src/common/document-types/fixture-v1/homily.template.tex", "%@ region body\n")
        self.write("src/claude/doc/publication.toml", '''kind = "fixture"
[[outputs]]
role = "canonical"
entrypoint = "main.tex"
[[outputs]]
role = "homily"
entrypoint = "homily.tex"
[document]
type = "fixture-v1"
[document.main]
body = ["sections/body"]
[document.homily]
body = ["sections/homily"]
''')
        dates = self.root / "src/sources/dates.txt"
        generator = self.root / "scripts/date_generator.py"
        self.write("src/sources/dates.txt", "c. 1000 B.C.\n")
        self.write("scripts/date_generator.py", "# date prose generator\n")
        adopted = self.commit("assemble the date page")
        projection = SimpleNamespace(
            NAME="fake", OUTPUTS={"page": "generated/date.tex"},
            render=lambda context: {"generated/date.tex": dates.read_text()},
            dependencies=lambda context: {dates, generator})
        # This projection fixture has no registered publication genre or render data.
        with patch.object(revision, "_render_data", return_value=set()), \
                patch("_document_types.discover_projections", return_value={"fake": projection}):
            with patch.object(projection, "render", wraps=projection.render) as render:
                self.assertEqual(self.derive().timestamp, stamp(adopted))
            self.assertEqual(render.call_count, 1)
            assembly = revision.Assembly(self.root)
            with patch.object(projection, "render", wraps=projection.render) as render, \
                    patch.object(projection, "dependencies", wraps=projection.dependencies) as dependencies:
                main = revision.revision(self.root, "claude", "doc", assembly=assembly)
                homily = revision.revision_for_entrypoint(
                    self.root, "claude", self.root / "src/claude/doc/homily.tex", assembly=assembly)
                self.assertEqual(main.timestamp, stamp(adopted))
                self.assertEqual(homily.timestamp, stamp(self.first))
                self.assertIn("src/sources/dates.txt", main.closure)
                self.assertNotIn("src/sources/dates.txt", homily.closure)
            self.assertEqual(render.call_count, 1)
            self.assertEqual(dependencies.call_count, 1)
            self.assertEqual(self.derive("doc-homily").timestamp, stamp(self.first))
            self.write("src/claude/doc/generated/date.tex", "Stale saved copy.\n")
            self.assertFalse(self.derive().uncommitted)
            self.write("src/sources/dates.txt", "c. 1055–1015 B.C.\n")
            self.assertTrue(self.derive().uncommitted)
            revised = self.commit("clarify date range")
            self.assertEqual(self.derive().timestamp, stamp(revised))
            self.assertEqual(self.derive("doc-homily").timestamp, stamp(self.first))
            generator.write_text("# clearer date prose generator\n")
            self.assertTrue(self.derive().uncommitted)

    def test_dictionary_notes_revise_only_editions_using_the_selected_source_metadata(self):
        owner = "liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary"
        self.write("src/common/document-types/sanctuary-dictionary-v1/type.toml", '''schema = 1
record_type = "document-type"
id = "sanctuary-dictionary-v1"
description = "Dictionary note revision fixture"
kinds = ["pictorial-dictionary"]
[editions.main]
role = "canonical"
template = "main.template.tex"
entrypoint = "main.tex"
fields = ["selection"]
regions = ["body"]
''')
        self.write("src/common/document-types/sanctuary-dictionary-v1/main.template.tex", "%@ region body\n")
        self.write("tools/render-sanctuary-dictionary", '''def edition_source_note_inputs(root, owner, selection_id):
    return {root / "src/sources" / (selection_id + ".toml")}
''')
        for leaf in ("altar-server", "sacristan"):
            base = "src/claude/" + owner + "/" + leaf
            self.write(base + "/main.tex", GENERATED)
            self.write(base + "/body.tex", "Dictionary body.\n")
            self.write(base + "/publication.toml", '''[document]
type = "sanctuary-dictionary-v1"
[document.main]
selection = "''' + leaf + '''"
body = ["body"]
''')
            self.write("src/sources/" + leaf + ".toml", 'title = "Original source title"\n')
        original = self.commit("create selected source notes")
        note = "src/sources/altar-server.toml"
        other = "src/sources/sacristan.toml"
        self.write(note, 'title = "Corrected source title"\n')
        self.assertTrue(self.derive(owner + "/altar-server").uncommitted)
        other_value = self.derive(owner + "/sacristan")
        self.assertFalse(other_value.uncommitted)
        edited = self.commit("correct a rendered source title")
        value = self.derive(owner + "/altar-server")
        self.assertEqual(value.timestamp, stamp(edited))
        self.assertIn(note, value.closure)
        self.assertNotIn(other, value.closure)
        self.assertIn("tools/render-sanctuary-dictionary", value.closure)
        self.assertEqual(self.derive(owner + "/sacristan").timestamp, stamp(original))
        generator = self.root / "tools/render-sanctuary-dictionary"
        generator.write_text(generator.read_text() + "# revised note rendering\n")
        self.assertTrue(self.derive(owner + "/sacristan").uncommitted)
        (self.root / note).unlink()
        with self.assertRaisesRegex(revision.RevisionError, "source-note input is missing"):
            self.derive(owner + "/altar-server")

    def test_the_stamp_is_the_last_commit_to_the_editions_own_sources(self) -> None:
        self.assertEqual(self.derive().timestamp, stamp(self.first))
        self.write("src/claude/doc/sections/body.tex", "Body, revised.\n")
        revised = self.commit("revise the body")
        self.write("src/common/preamble.tex", "% shared typesetting, retuned\n")
        self.write("src/claude/doc/generation-metadata.tex", "\\AIModelContribution{m}{q}{r2}\n")
        self.commit("retune the preamble and log the contribution")
        value = self.derive()
        self.assertEqual(value.timestamp, stamp(revised))
        self.assertFalse(value.uncommitted)
        self.assertEqual(value.display, stamp(revised))
        self.assertNotIn("src/common/preamble.tex", value.closure)
        self.assertNotIn("src/claude/doc/generation-metadata.tex", value.closure)

    def test_the_stamp_is_author_time_which_cherry_pick_and_rebase_keep(self) -> None:
        self.write("src/claude/doc/sections/body.tex", "Body, revised.\n")
        authored = self.commit("revise", committed_later=86_400)
        self.assertEqual(self.derive().timestamp, stamp(authored))

    def test_a_none_trailer_is_looked_past_and_an_untrailered_commit_is_not(self) -> None:
        self.write("src/claude/doc/sections/body.tex", "Body, revised.\n")
        revised = self.commit("revise the body")
        self.write("src/claude/doc/sections/body.tex", "Body,\nrevised.\n")
        self.commit("move the body's text unchanged\n\nEdition-Revision: none")
        self.assertEqual(self.derive().timestamp, stamp(revised))
        self.write("src/claude/doc/sections/body.tex", "Body, revised again.\n")
        again = self.commit("revise the body again")
        self.assertEqual(self.derive().timestamp, stamp(again))

    def test_text_a_marked_refactor_moved_into_a_new_file_keeps_its_older_stamp(self) -> None:
        self.write("src/claude/doc/sections/body.tex", "Body, revised.\n")
        revised = self.commit("revise the body")
        self.write("src/claude/doc/sections/body.tex", "\\input{doc/sections/part}\n")
        self.write("src/claude/doc/sections/part.tex", "Body, revised.\n")
        self.commit("split the body into a part file\n\nEdition-Revision: none")
        value = self.derive()
        self.assertIn("src/claude/doc/sections/part.tex", value.closure)
        self.assertEqual(value.timestamp, stamp(revised))
        # The same split unmarked is a revision on this rule.
        self.write("src/claude/doc/sections/part.tex", "Body, revised; and now edited.\n")
        edited = self.commit("edit the part")
        self.assertEqual(self.derive().timestamp, stamp(edited))

    def test_only_none_is_a_valid_trailer_value(self) -> None:
        self.write("src/claude/doc/sections/body.tex", "Body, revised.\n")
        self.commit("revise\n\nEdition-Revision: minor")
        with self.assertRaisesRegex(revision.RevisionError, "only value"):
            self.derive()

    def test_an_edition_whose_every_commit_is_marked_none_has_no_stamp(self) -> None:
        self.git("commit", "-q", "--amend", "-m", "create\n\nEdition-Revision: none")
        with self.assertRaisesRegex(revision.RevisionError, "no commit in this history revised"):
            self.derive()

    def test_each_edition_of_a_leaf_has_its_own_stamp(self) -> None:
        self.write("src/claude/doc/generated/date.tex", "Dates, regenerated.\n")
        dated = self.commit("regenerate the chronology page")
        self.assertEqual(self.derive().timestamp, stamp(dated))
        self.assertEqual(self.derive("doc-homily").timestamp, stamp(self.first))

    def test_a_generated_entrypoints_history_moves_no_stamp(self) -> None:
        main = self.root / "src/claude/doc/main.tex"
        self.write("src/claude/doc/main.tex", GENERATED + main.read_text())
        self.commit("generate the entrypoint from a template")
        self.write("src/claude/doc/main.tex", GENERATED + "% retemplated\n"
                   + main.read_text().removeprefix(GENERATED))
        self.commit("change the template")
        value = self.derive()
        self.assertEqual(value.timestamp, stamp(self.first))
        self.assertIn("src/claude/doc/main.tex", value.closure)

    def test_macro_built_inputs_are_expanded_and_an_unknown_one_refused(self) -> None:
        self.write("src/claude/doc/main.tex",
                   "\\newcommand{\\DocRoot}{doc}\n\\newcommand{\\Part}{\\DocRoot/sections/body}\n"
                   "\\input{\\Part}\n\\input{\\DocRoot/generation-metadata}\n")
        self.commit("compute the inputs")
        self.assertIn("src/claude/doc/sections/body.tex", self.derive().closure)
        self.write("src/claude/doc/main.tex", "\\input{\\Undefined/sections/body}\n")
        self.commit("lose the definition")
        with self.assertRaisesRegex(revision.RevisionError, "cannot expand"):
            self.derive()


class WithoutUsableHistoryTests(Fixture):
    def test_uncommitted_or_untracked_sources_are_stamped_now_and_say_so(self) -> None:
        self.write("src/claude/doc/sections/body.tex", "Body, being edited.\n")
        value = self.derive()
        self.assertTrue(value.uncommitted)
        self.assertEqual(value.display, "2026-11-04T20:00:00Z (uncommitted sources)")
        self.assertIn("\\AIDocumentRevisionUncommitted", value.tex())
        # The homily reads none of it and stays committed.
        self.assertFalse(self.derive("doc-homily").uncommitted)
        self.git("checkout", "--", "src/claude/doc/sections/body.tex")
        self.write("src/claude/doc/sections/new.tex", "New.\n")
        self.write("src/claude/doc/homily.tex", "\\input{doc/sections/new}\n")
        self.assertTrue(self.derive("doc-homily").uncommitted)

    def test_a_shallow_clone_fails_closed(self) -> None:
        self.write("src/claude/doc/sections/body.tex", "Body, revised.\n")
        self.commit("revise")
        clone = self.root.parent / "shallow"
        self.git("clone", "-q", "--depth", "1", f"file://{self.root}", str(clone), cwd=self.root.parent)
        with self.assertRaisesRegex(revision.RevisionError, "shallow"):
            revision.revision(clone, "claude", "doc")

    def test_a_tree_outside_git_fails_closed(self) -> None:
        plain = self.root.parent / "plain"
        (plain / "src/claude/doc").mkdir(parents=True)
        with self.assertRaisesRegex(revision.RevisionError, "not a git work tree"):
            revision.revision(plain, "claude", "doc")
        nested = self.root / "src/claude"
        with self.assertRaisesRegex(revision.RevisionError, "not the top"):
            revision.Repository(nested)

    def test_the_build_file_keeps_an_uncommitted_stamp_until_the_sources_move(self) -> None:
        target = self.root.parent / "build/doc.revision.tex"
        committed = self.derive()
        self.assertTrue(revision.write(target, committed))
        self.assertFalse(revision.write(target, committed))
        self.write("src/claude/doc/sections/body.tex", "Body, being edited.\n")
        first = self.derive()
        self.assertTrue(revision.write(target, first))
        later = revision.revision(self.root, "claude", "doc", now=NOW + dt.timedelta(minutes=5))
        self.assertFalse(revision.write(target, later))
        self.assertIn(first.timestamp, target.read_text())
        self.write("src/claude/doc/sections/body.tex", "Body, edited again.\n")
        again = revision.revision(self.root, "claude", "doc", now=NOW + dt.timedelta(minutes=9))
        self.assertTrue(revision.write(target, again))
        self.assertIn(again.timestamp, target.read_text())


if __name__ == "__main__":
    unittest.main()
