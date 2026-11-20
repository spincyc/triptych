"""Same-run Pages publication source partitions reproduce the canonical owner API."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _document_schema as schema
import _native_print_bundles as bundles
import _native_print_compile as gate
import _native_print_reference as native
import _publication_source_reference as sources
import _print_document as printing
from tools.tests.test_public_alpha import load_tool


class PublicationReferenceTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/publication-source-reference-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temporary.cleanup)
        self.work = Path(temporary.name)
        self.root = self.work / "checkout"
        self.root.mkdir()
        self.git("init", "-q")
        (self.root / ".git/info/exclude").write_text(".scratch/\nbuild/\n")
        self.docs = {}
        for name in ("alpha", "beta", "held", "markdown-only"):
            leaf = self.root / "src/gpt/articles/faith" / name
            (leaf / "research").mkdir(parents=True)
            (leaf / "research/scope.md").write_text("Current scope.\n")
            (leaf / "research/source-audit.md").write_text("Current evidence.\n")
            (leaf / "main.tex").write_text("Canonical textual source.\n")
            declaration = schema.adapter_manifest(self.root, leaf)
            if name == "markdown-only":
                (leaf / "main.tex").rename(leaf / "main.md")
                declaration.update(source_format="markdown", entrypoint="main.md")
                declaration["outputs"][0]["entrypoint"] = "main.md"
                declaration["structure"][0]["source"] = "main.md"
            if name in ("alpha", "beta"):
                key = "publication:" + declaration["id"]
                self.docs[key] = {"id": key, "document": key, "edition": "main", "title": name}
            (leaf / "publication.toml").write_text(schema.dumps_manifest(declaration))
        self.leaf = self.root / "src/gpt/articles/faith/alpha"
        (self.leaf / "web-edition.toml").write_text('eligibility="eligible"\ninspected="2026-11-20"\n')
        template = self.root / "src/common/document-types/article-test-v1"
        template.mkdir(parents=True)
        (template / "type.toml").write_text('schema=1\nrecord_type="document-type"\nid="article-test-v1"\n'
            'description="Generated article"\nkinds=["article-faith"]\n[editions.main]\nrole="canonical"\n'
            'template="main.template.tex"\nentrypoint="main.tex"\nregions=["body"]\n')
        (template / "main.template.tex").write_text("%@ region body\n")
        (self.leaf / "body.tex").write_text("Authored section.\n")
        with (self.leaf / "publication.toml").open("a") as out:
            out.write('\n[document]\ntype="article-test-v1"\n[document.main]\nbody=["body"]\n')
        (self.root / "Makefile").write_text("# Fixture\n")
        self.git("add", ".")
        self.commit()
        self.tool = load_tool()
        self.tool.ROOT = self.root
        self.tool.MANIFEST_PATH = self.root / "release/public-alpha.json"
        self.keys, self.parts = {}, {}
        self.shards, self.merged = self.work / "shards", self.work / "merged"
        env = patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_SHA": self.revision,
                                      "GITHUB_RUN_ID": "12", "GITHUB_RUN_ATTEMPT": "2"})
        env.start()
        self.addCleanup(env.stop)
        for key in ("TRIPTYCH_NATIVE_REFERENCE_DIR", "TRIPTYCH_NATIVE_REFERENCE_SHA256"):
            os.environ.pop(key, None)

    def git(self, *arguments):
        return subprocess.run(["git", *arguments], cwd=self.root, capture_output=True,
                              text=True, check=True).stdout

    def commit(self):
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-qam", "Fixture")
        self.revision = self.git("rev-parse", "HEAD").strip()

    def prepare(self):
        real_catalog, real_part = bundles.prepare_catalog, sources.prepare_partition
        assemblies = []
        def catalog(*args, **kwargs):
            assemblies.append(kwargs["assembly"])
            return real_catalog(*args, **kwargs)
        def partition(*args):
            self.assertIs(args[-1], assemblies.pop())
            return real_part(*args)
        with patch("_native_print.admitted_documents", return_value=self.docs), \
                patch.object(printing, "check_many", side_effect=lambda rows, **_: [
                    dict(row, status="valid", validation={"source": "pass"}) for row in rows]), \
                patch.object(bundles, "prepare_catalog", side_effect=catalog), \
                patch.object(sources, "prepare_partition", side_effect=partition):
            for n in (1, 2):
                result = gate.prepare(self.root, self.work / f"print-{n}", shard=(n, 2),
                                      export_reference=self.shards / str(n), run_id="12", run_attempt="1",
                                      publication_sources=True)
                self.keys[str(n)] = result["reference_sha256"]

    def merge(self):
        self.parts = {}
        result = native.merge_reference_catalogs(self.shards, root=self.root, documents=self.docs,
            revision=self.revision, run_id="12", run_attempt="2", shards=2, expected_keys=self.keys,
            publication_parts=self.parts)
        return native.write_reference_catalog(self.merged, result, run_id="12", run_attempt="2",
                                              publication_parts=self.parts)

    def capture(self):
        keys = [tuple(key.removeprefix("publication:").split("/", 1)) for key in self.docs]
        self.tool.prefetch_publication_dependencies(keys)
        return self.tool.publication_source_records(), {key: self.tool.publication_source_identity(*key) for key in keys}

    def load(self, digest):
        with patch.dict(os.environ, {"TRIPTYCH_NATIVE_REFERENCE_DIR": str(self.merged),
                                     "TRIPTYCH_NATIVE_REFERENCE_SHA256": digest}), \
                patch("_native_print.admitted_documents", return_value=self.docs), self.tool.held_repository_inputs():
            self.tool._hold_pages_publication_sources(2)
            with patch.object(schema, "identities", side_effect=AssertionError("local identity reran")), \
                    patch.object(schema, "discover", side_effect=AssertionError("local discovery reran")), \
                    patch.object(self.tool, "document_assembly", side_effect=AssertionError("local projection reran")):
                return self.capture()

    def test_native_partition_and_protected_pages_operation_match_separate_canonical_sources(self):
        with self.tool.held_repository_inputs():
            expected = self.capture()
        self.prepare()
        digest = self.merge()
        self.assertEqual(self.load(digest), expected)
        self.assertEqual((len(expected[0]), len(expected[1])), (4, 2))
        self.assertTrue(any(row.get("virtual") for part in self.parts.values() for row in part["records"].values()))
        with self.assertRaisesRegex(ValueError, "digest"):
            self.load("0" * 64)
        with self.assertRaisesRegex(self.tool.ReleaseError, "protected"):
            self.tool._hold_pages_publication_sources(2)
        original = sources.verify_partitions
        def source_changes_during_join(*args):
            verified = original(*args)
            (self.leaf / "new-input.tex").write_text("New wildcard member.\n")
            return verified
        with patch.object(sources, "verify_partitions", side_effect=source_changes_during_join), \
                self.assertRaisesRegex(self.tool.ReleaseError, "clean"):
            self.load(digest)
        with self.assertRaisesRegex(self.tool.ReleaseError, "clean"):
            self.load(digest)

    def test_changed_inputs_wrong_origin_and_missing_partitions_are_refused(self):
        self.prepare()
        self.merge()
        def verify(parts):
            return sources.verify_partitions(self.root, self.docs, self.revision, "12", "2", 2, parts)
        def row(part):
            return next(item for item in part["records"].values() if item.get("virtual"))
        mutations = (lambda p: p.update(attempt="3"), lambda p: p.update(revision="0"*40),
                     lambda p: p.update(run_id="13"), lambda p: row(p)["output_hashes"].update(canonical="0"*64),
                     lambda p: row(p)["virtual"].update({"../escape":"0"*64}),
                     lambda p: row(p)["identity"]["render"].update(sha256="0"*64),
                     lambda p: p["records"].pop(next(iter(p["records"]))))
        for mutate in mutations:
            parts = copy.deepcopy(self.parts)
            target = next(p for p in parts.values() if any(r.get("virtual") for r in p["records"].values()))
            mutate(target)
            with self.assertRaises(ValueError):
                verify(parts)
        with self.assertRaisesRegex(ValueError, "partition set"):
            verify({"1": self.parts["1"]})
        (self.leaf / "research/source-audit.md").write_text("Different evidence.\n")
        with self.assertRaisesRegex(ValueError, "changed evidence source"):
            verify(self.parts)
        path = self.shards / "1/catalog.json"
        desc = json.loads(path.read_bytes())
        del desc["publication_parts"]
        desc["schema"] = native.SCHEMA
        path.write_bytes(bundles.canonical(desc))
        self.keys["1"] = bundles._sha(path.read_bytes())
        with self.assertRaisesRegex(ValueError, "publication partition"):
            self.merge()

    def test_held_pages_census_joins_real_sources_once_and_releases_all_facts(self):
        import _native_print as admissions
        from _native_tex_publication import catalog
        for leaf in ("alpha", "beta", "held"):
            directory = self.root / "src/gpt/articles/faith" / leaf
            (directory / "web-edition.toml").write_text('eligibility="eligible"\n')
            disposition = self.root / "release/publications/gpt/articles/faith" / (leaf + ".json")
            disposition.parent.mkdir(parents=True, exist_ok=True)
            disposition.write_text(json.dumps({"status": "hold" if leaf == "held" else "alpha"}))
        self.git("add", ".")
        self.commit()
        # This fixture provides publications only. Admission and withdrawal
        # still use the normal disk-based declaration and release selectors.
        with patch.dict(printing.EDITIONS, {}, clear=True), patch.dict(os.environ, {"GITHUB_SHA": self.revision}):
            self.docs = admissions.admitted_documents(self.root)
            self.assertEqual(len(self.docs), 2)
            paths = admissions.admission_inputs(self.root)
            self.assertEqual(len(paths), 6)  # held edition still controls admission
            owners = schema.publication_owners(self.root)
            self.assertEqual(len(owners), 4)  # includes the Markdown-only leaf
            self.prepare()
            digest = self.merge()
            env = {"TRIPTYCH_NATIVE_REFERENCE_DIR": str(self.merged), "TRIPTYCH_NATIVE_REFERENCE_SHA256": digest}
            with (patch.dict(os.environ, env), self.tool.held_repository_inputs(),
                  patch.object(admissions, "_admitted_recipes", wraps=admissions._admitted_recipes) as recipes,
                  patch.object(schema, "publication_owners", wraps=schema.publication_owners) as census):
                with admissions.held_source_admissions(self.root):
                    self.tool._hold_pages_publication_sources(2)
                    # The publisher receives the same source catalog and
                    # membership as a fresh pass through the native selector.
                    with (patch("_native_tex_assets.public_manifest", return_value={}),
                          patch("_native_tex_assets.payload_paths", return_value={}),
                          patch("_native_tex_publication.build_catalog", side_effect=lambda root, **kw: kw)):
                        native_inputs = catalog(self.root, source_loader=self.tool._native_reference_loader())
                    self.assertEqual(native_inputs["documents"], self.docs)
                    self.assertTrue(set(paths) <= set(native_inputs["source_catalog"]["source_paths"]))
                    self.assertEqual(admissions.publication_source_owners(self.root), owners)
                    # Mutable API results belong to the caller.
                    key = next(iter(self.docs))
                    admissions.admitted_documents(self.root)[key]["title"] = "changed"
                    admissions.admission_inputs(self.root).clear()
                    admissions.publication_source_owners(self.root).clear()
                    self.assertEqual(admissions.admitted_documents(self.root), self.docs)
                    self.assertEqual(admissions.admission_inputs(self.root), paths)
                    self.assertEqual(admissions.publication_source_owners(self.root), owners)
                    self.assertEqual(recipes.call_count, 1)
                    self.assertEqual(census.call_count, 1)
                    self.assertEqual(admissions.publication_source_owners(self.work), set())
                self.assertEqual(admissions.admission_inputs(self.root), paths)
                self.assertEqual(recipes.call_count, 2)
            # A change after discovery and before accepting the authenticated
            # partitions must still fail the real full-checkout guard.
            with patch.dict(os.environ, env):
                with self.assertRaisesRegex(self.tool.ReleaseError, "clean"):
                    with self.tool.held_repository_inputs(), admissions.held_source_admissions(self.root):
                        added = self.root / "src/gpt/articles/faith/extra/main.tex"
                        added.parent.mkdir()
                        added.write_text("New canonical owner.")
                        self.tool._hold_pages_publication_sources(2)
            self.assertEqual(admissions.publication_source_owners(self.root), owners | {"gpt/articles/faith/extra"})
            with self.assertRaisesRegex(admissions.NativePrintError, "disposition"):
                with admissions.held_source_admissions(self.root):
                    self.fail("invalid new edition acquired a held census")

    def test_an_unadmitted_owner_with_a_missing_manifest_blocks_source_export(self):
        (self.leaf.parent / "held/publication.toml").unlink()
        self.commit()
        with self.assertRaisesRegex(ValueError, "missing publication.toml"):
            self.prepare()
