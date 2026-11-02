"""An active alias ID chooses exact owned bytes while preserving old evidence."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _bible_artifacts as aliases
import _bible_editions
import _projection
import _psalms

HEADER = "cited_locus\tresolves_to\tkind\tnote\n"
EDITION = "edition.synthetic.bible.test-1900"


def toml(data):
    return "\n".join(f"{key} = {json.dumps(value, ensure_ascii=False)}" for key, value in data.items()) + "\n"


class ActiveAliasArtifacts(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.home = Path(self.temporary.name)
        self.root = self.home / "src/sources/works/synthetic/bible/editions/test-1900"
        self.root.mkdir(parents=True)
        self.edition = {"schema": 1, "record_type": "edition", "id": EDITION}
        (self.root / "edition.toml").write_text(toml(self.edition))
        self.registry = {"synthetic": {"source_id": EDITION, "artifacts": "synthetic/bible/editions/test-1900/artifacts"}}
        self.old = self.artifact(HEADER + "Ps.28.11\tPs.28.10\tmerged-verse\tOld exact evidence.\n")

    def artifact(self, text, role="verse-aliases"):
        payload = text.encode("utf-8")
        digest = sha256(payload).hexdigest()
        folder = self.root / "artifacts" / (role + "-" + digest[:8])
        folder.mkdir(parents=True)
        path = folder / aliases.ROLES[role][1]
        path.write_bytes(payload)
        record = {"schema": 1, "record_type": "artifact", "id": "artifact.synthetic.bible.test-1900." + role + "-" + digest[:8],
            "edition_id": EDITION, "artifact_type": "reference-table", "media_type": "text/tab-separated-values; charset=utf-8",
            "storage": "tracked", "rights_status": "project-created", "rights_basis": "Synthetic project reference facts.",
            "sha256": digest, "byte_size": len(payload), "path": path.relative_to(self.home).as_posix(), "indexable": True, "encoding": "utf-8"}
        (folder / "artifact.toml").write_text(toml(record))
        return path, record

    def select(self):
        return aliases.select_verse_aliases(self.root, registry=self.registry)

    def activate(self, artifact):
        self.registry["synthetic"][aliases.ACTIVE_ALIAS_FIELD] = artifact[1]["id"]

    def test_unique_legacy_table_selects_exact_existing_bytes(self):
        self.assertEqual(self.select(), self.old[0])
        self.assertEqual(sha256(self.select().read_bytes()).hexdigest(), self.old[1]["sha256"])

    def test_multiple_tables_require_declared_id_and_preserve_history(self):
        newer = self.artifact(HEADER + "Ps.150.6\tPs.150.5\tmerged-verse\tNew exact evidence.\n")
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        with self.assertRaisesRegex(aliases.AliasArtifactError, "require a declared"):
            self.select()
        self.activate(newer)
        self.assertEqual(self.select(), newer[0])
        self.activate(self.old)
        self.assertEqual(self.select(), self.old[0])
        self.assertEqual(before, {path: path.read_bytes() for path in before})

    def test_projection_and_psalm_witness_share_the_active_selector(self):
        newer = self.artifact(HEADER + "Ps.150.6\tPs.150.5\tmerged-verse\tNew exact evidence.\n")
        self.activate(newer)
        with patch.dict(_bible_editions.EDITIONS, self.registry, clear=True):
            self.assertEqual(_projection.alias_rows(self.root)[0].cited_locus, "Ps.150.6")
            self.assertEqual(_projection.alias_table(self.root)[_projection.Locus("Ps", 150, 6)], _projection.Locus("Ps", 150, 5))
            _psalms.witness_merges.cache_clear()
            try:
                with patch.object(_psalms, "CONCORDANCE_ROOT", self.root / "artifacts"):
                    self.assertEqual(_psalms.witness_merges(), ((150, 6),))
            finally:
                _psalms.witness_merges.cache_clear()

    def test_missing_or_foreign_active_id_never_falls_back_to_legacy(self):
        for artifact_id in ("artifact.synthetic.missing", "artifact.foreign.edition.aliases"):
            with self.subTest(artifact_id=artifact_id):
                self.registry["synthetic"][aliases.ACTIVE_ALIAS_FIELD] = artifact_id
                with self.assertRaisesRegex(aliases.AliasArtifactError, "exactly one local artifact"):
                    self.select()

    def test_optional_control_requires_exact_artifact_id(self):
        for value in (None, "", False, 1, [], {}, "verse-aliases.tsv", "artifact bad", "artifact.x/../y"):
            with self.subTest(value=value):
                self.registry["synthetic"][aliases.ACTIVE_ALIAS_FIELD] = value
                with self.assertRaisesRegex(aliases.AliasArtifactError, "exact artifact ID"):
                    self.select()

    def test_conflicting_registry_declarations_refuse(self):
        self.activate(self.old)
        self.registry["conflict"] = {**self.registry["synthetic"], aliases.ACTIVE_ALIAS_FIELD: "artifact.synthetic.other"}
        with self.assertRaisesRegex(aliases.AliasArtifactError, "conflicting"):
            self.select()

    def test_misspelled_control_or_wrong_config_path_refuses(self):
        self.registry["synthetic"]["verse_alias_artifact_id"] = self.old[1]["id"]
        with self.assertRaisesRegex(aliases.AliasArtifactError, "unknown fields"):
            self.select()
        self.registry["synthetic"].pop("verse_alias_artifact_id")
        self.registry["synthetic"]["artifacts"] = "synthetic/foreign/editions/test-1900/artifacts"
        with self.assertRaisesRegex(aliases.AliasArtifactError, "disagree"):
            self.select()

    def test_book_index_role_selects_independently_and_preserves_both_histories(self):
        header = "ordinal\ttoken\ttestament\tmodern_name\tdouay_title\talternate_names\tfile\tchapters\tverses\n"
        first = self.artifact(header + "1\tGen\tOT\tGenesis\tGenesis\t\t01-genesis.tsv\t1\t1\n", "book-index")
        self.assertEqual(aliases.select_book_index(self.root, registry=self.registry), first[0])
        second = self.artifact(header + "1\tGen\tOT\tGenesis checked\tGenesis\t\t01-genesis.tsv\t1\t1\n", "book-index")
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        with self.assertRaisesRegex(aliases.AliasArtifactError, "book_index_artifact_id"):
            aliases.select_book_index(self.root, registry=self.registry)
        self.registry["synthetic"][aliases.ACTIVE_BOOK_FIELD] = second[1]["id"]
        self.assertEqual(aliases.select_book_index(self.root, registry=self.registry), second[0])
        self.assertEqual(self.select(), self.old[0])
        self.assertEqual(before, {path: path.read_bytes() for path in before})
        # A role may never borrow another role's selected exact artifact.
        self.registry["synthetic"][aliases.ACTIVE_BOOK_FIELD] = self.old[1]["id"]
        with self.assertRaisesRegex(aliases.AliasArtifactError, "exactly one local artifact"):
            aliases.select_book_index(self.root, registry=self.registry)

    def test_indexing_and_typesetting_read_same_selected_book_order_and_extent(self):
        from importlib.machinery import SourceFileLoader
        from importlib.util import module_from_spec, spec_from_loader
        def tool(name):
            loader = SourceFileLoader("_alias_test_" + name.replace("-", "_"), str(ROOT / "tools" / name))
            spec = spec_from_loader(loader.name, loader)
            module = module_from_spec(spec)
            # Dataclass-bearing tools resolve their module through sys.modules.
            sys.modules[loader.name] = module
            loader.exec_module(module)
            return module
        index = tool("index-bible")
        typesetter = tool("typeset-bible")
        self.assertIs(index.EDITIONS, _bible_editions.EDITIONS)
        header = "ordinal\ttoken\ttestament\tmodern_name\tdouay_title\talternate_names\tfile\tchapters\tverses\n"
        body = "1\tGen\tOT\tGenesis\tGenesis\t\t01-genesis.tsv\t1\t1\n"
        old = self.artifact(header + body, "book-index")
        new = self.artifact(header + body.replace("Genesis\tGenesis", "Genesis checked\tGenesis"), "book-index")
        self.registry["synthetic"][aliases.ACTIVE_BOOK_FIELD] = new[1]["id"]
        verses = self.root / "artifacts/verse-text-synthetic/01-genesis.tsv"
        verses.parent.mkdir()
        verses.write_text("book\tchapter\tverse\ttext\nGen\t1\t1\tExact synthetic body.\n")
        edition = typesetter.Edition.__new__(typesetter.Edition)
        edition.id, edition.artifacts = "synthetic", self.root / "artifacts"
        with patch.dict(_bible_editions.EDITIONS, self.registry, clear=True):
            self.assertEqual(index.load_books(edition.artifacts)["genesis checked"], "Gen")
            books = edition._books()
        self.assertEqual([(b.ordinal, b.token, b.name, b.declared_chapters, b.declared_verses) for b in books], [(1, "Gen", "Genesis checked", 1, 1)])
        books[0].load()
        self.assertEqual(books[0].verses, [(1, 1, "Exact synthetic body.")])
        self.assertEqual(sha256(old[0].read_bytes()).hexdigest(), old[1]["sha256"])

    def test_duplicate_artifact_identity_refuses(self):
        newer = self.artifact(HEADER + "Ps.150.6\tPs.150.5\tmerged-verse\tNew exact evidence.\n")
        newer[1]["id"] = self.old[1]["id"]
        (newer[0].parent / "artifact.toml").write_text(toml(newer[1]))
        self.activate(self.old)
        with self.assertRaisesRegex(aliases.AliasArtifactError, "found 2"):
            self.select()

    def test_selected_metadata_corruption_fails_closed(self):
        self.activate(self.old)
        for key, value in (("edition_id", "edition.foreign.bible"), ("record_type", "passage"),
                ("schema", True), ("schema", 3), ("rights_status", "restricted"), ("rights_status", "unresolved"),
                ("rights_basis", ""), ("storage", "remote"), ("sha256", "0" * 64), ("sha256", "bad"),
                ("byte_size", True), ("byte_size", -1), ("byte_size", 0), ("indexable", False),
                ("encoding", "latin-1"), ("media_type", "text/plain"), ("artifact_type", "scan"),
                ("path", "../verse-aliases.tsv"), ("path", "/absolute/verse-aliases.tsv"),
                ("path", "src/sources/works/synthetic/bible/editions/foreign/artifacts/" + self.old[0].parent.name + "/verse-aliases.tsv"),
                ("path", self.old[1]["path"].replace("/artifacts/", "/artifacts/../artifacts/"))):
            with self.subTest(key=key, value=value):
                changed = {**self.old[1], key: value}
                (self.old[0].parent / "artifact.toml").write_text(toml(changed))
                with self.assertRaises(aliases.AliasArtifactError):
                    self.select()
        (self.old[0].parent / "artifact.toml").write_text(toml(self.old[1]))

    def test_unique_legacy_manifest_is_also_validated(self):
        self.old[0].write_text("corrupted")
        with self.assertRaisesRegex(aliases.AliasArtifactError, "recorded hash or size"):
            self.select()

    def test_missing_selected_payload_and_missing_metadata_refuse(self):
        self.activate(self.old)
        payload = self.old[0].read_bytes()
        self.old[0].unlink()
        with self.assertRaises(aliases.AliasArtifactError):
            self.select()
        self.old[0].write_bytes(payload)
        (self.old[0].parent / "artifact.toml").unlink()
        with self.assertRaises(aliases.AliasArtifactError):
            self.select()

    def test_missing_unique_payload_does_not_become_an_empty_alias_table(self):
        self.old[0].unlink()
        with self.assertRaises(aliases.AliasArtifactError):
            self.select()

    def test_missing_edition_or_foreign_registry_path_refuses(self):
        (self.root / "edition.toml").unlink()
        with self.assertRaisesRegex(aliases.AliasArtifactError, "edition.toml"):
            self.select()
        (self.root / "edition.toml").write_text(toml(self.edition))
        self.registry["synthetic"]["source_id"] = "edition.foreign.bible"
        with self.assertRaisesRegex(aliases.AliasArtifactError, "disagree"):
            self.select()

    def test_payload_symlink_refuses_but_hardlink_preserves_exact_bytes(self):
        self.activate(self.old)
        target = self.home / "independent-exact-bytes.tsv"
        target.write_bytes(self.old[0].read_bytes())
        self.old[0].unlink()
        self.old[0].symlink_to(target)
        with self.assertRaises(aliases.AliasArtifactError):
            self.select()
        self.old[0].unlink()
        os.link(target, self.old[0])
        self.assertEqual(self.select(), self.old[0])

    def test_metadata_symlink_refuses_before_opening_foreign_bytes(self):
        self.activate(self.old)
        metadata = self.old[0].parent / "artifact.toml"
        target = self.home / "independent-manifest.toml"
        target.write_bytes(metadata.read_bytes())
        metadata.unlink()
        metadata.symlink_to(target)
        with self.assertRaisesRegex(aliases.AliasArtifactError, "symlink"):
            self.select()

    def test_artifact_directory_link_and_nonregular_payload_refuse(self):
        self.activate(self.old)
        folder = self.old[0].parent
        outside = self.home / "foreign-artifact-owner"
        folder.rename(outside)
        folder.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(aliases.AliasArtifactError):
            self.select()
        folder.unlink()
        outside.rename(folder)
        self.old[0].unlink()
        self.old[0].mkdir()
        with self.assertRaisesRegex(aliases.AliasArtifactError, "regular file"):
            self.select()

    def test_public_domain_reference_needs_jurisdiction_and_utf8_is_checked(self):
        self.activate(self.old)
        changed = {**self.old[1], "rights_status": "public-domain"}
        metadata = self.old[0].parent / "artifact.toml"
        metadata.write_text(toml(changed))
        with self.assertRaisesRegex(aliases.AliasArtifactError, "jurisdiction"):
            self.select()
        changed["rights_jurisdiction"] = "United States"
        metadata.write_text(toml(changed))
        self.assertEqual(self.select(), self.old[0])
        invalid = b"\xff\xfe"
        self.old[0].write_bytes(invalid)
        changed.update(sha256=sha256(invalid).hexdigest(), byte_size=len(invalid))
        metadata.write_text(toml(changed))
        with self.assertRaisesRegex(aliases.AliasArtifactError, "UTF-8"):
            self.select()

    def test_absent_table_preserves_projection_absence_contract(self):
        self.old[0].unlink()
        (self.old[0].parent / "artifact.toml").unlink()
        self.assertIsNone(self.select())
        with patch.dict(_bible_editions.EDITIONS, self.registry, clear=True):
            self.assertEqual(_projection.alias_rows(self.root), [])
            with self.assertRaisesRegex(_projection.ProjectionError, "no verse-aliases artifact"):
                _projection.alias_table(self.root)

    def test_bare_unregistered_technical_fixture_retains_bounded_compatibility(self):
        root = self.home / "bare-fixture"
        first = root / "artifacts/verse-aliases-legacy/verse-aliases.tsv"
        first.parent.mkdir(parents=True)
        first.write_text(HEADER)
        self.assertEqual(aliases.select_verse_aliases(root, registry={}), first)
        second = root / "artifacts/verse-aliases-second/verse-aliases.tsv"
        second.parent.mkdir()
        second.write_text(HEADER)
        with self.assertRaisesRegex(aliases.AliasArtifactError, "require a declared"):
            aliases.select_verse_aliases(root, registry={})

    def test_edition_root_symlink_refuses_with_and_without_source_metadata(self):
        self.activate(self.old)
        physical = self.home / "physical-edition-owner"
        self.root.rename(physical)
        self.root.symlink_to(physical, target_is_directory=True)
        with self.assertRaisesRegex(aliases.AliasArtifactError, "edition root.*symlink"):
            self.select()
        bare = self.home / "bare-physical"
        payload = bare / "artifacts/verse-aliases-legacy/verse-aliases.tsv"
        payload.parent.mkdir(parents=True)
        payload.write_text(HEADER)
        pointer = self.home / "bare-symlink"
        pointer.symlink_to(bare, target_is_directory=True)
        with self.assertRaisesRegex(aliases.AliasArtifactError, "edition root.*symlink"):
            aliases.select_verse_aliases(pointer, registry={})

    def test_registry_requires_full_canonical_owner_path_for_each_role(self):
        book = self.artifact("token\tmodern_name\nGen\tGenesis\n", "book-index")
        self.activate(self.old)
        self.registry["synthetic"][aliases.ACTIVE_BOOK_FIELD] = book[1]["id"]
        canonical = "synthetic/bible/editions/test-1900/artifacts"
        invalid = ("test-1900/artifacts", "artifacts", "bible/editions/test-1900/artifacts",
            "/" + canonical, "../" + canonical, canonical.replace("/editions/", "/editions/../editions/"),
            canonical.replace("/editions/", "/./editions/"), canonical.replace("/", "\\"),
            canonical + "/", canonical.replace("synthetic/", "synthetic//"),
            canonical.replace("/editions/", "/impressions/"))
        for value in invalid:
            self.registry["synthetic"]["artifacts"] = value
            for role in aliases.ROLES:
                with self.subTest(value=value, role=role):
                    with self.assertRaisesRegex(aliases.AliasArtifactError, "canonical full owner-relative"):
                        aliases.select_reference_artifact(self.root, role, registry=self.registry)
        self.registry["synthetic"]["artifacts"] = canonical
        self.assertEqual(self.select(), self.old[0])
        self.assertEqual(aliases.select_book_index(self.root, registry=self.registry), book[0])

    def test_root_dotdot_and_claimed_source_id_path_disagreement_refuse(self):
        self.activate(self.old)
        traversing = self.root / ".." / self.root.name
        with self.assertRaisesRegex(aliases.AliasArtifactError, "edition root must be canonical"):
            aliases.select_verse_aliases(traversing, registry=self.registry)
        self.registry["synthetic"]["source_id"] = "edition.foreign.bible"
        with self.assertRaisesRegex(aliases.AliasArtifactError, "disagree"):
            self.select()


if __name__ == "__main__":
    unittest.main()
