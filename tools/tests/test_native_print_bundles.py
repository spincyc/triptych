"""Native source bundles transport canonical bytes, never print HTML or PDFs."""
from __future__ import annotations

import copy
import hashlib
import gzip
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _document_schema as schema
import _native_print_bundles as bundles
import _print_document as printing


class NativeSourceBundleTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / ".scratch/prepared-publisher/source-assembly/tests"
        base.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.leaf = self.root / "src/gpt/articles/faith/example"
        self.leaf.mkdir(parents=True)
        self.main = self.leaf / "main.tex"
        self.main.write_bytes(b"\\input{common/preamble}\r\n\\input{articles/faith/example/body}\r\n")
        (self.leaf / "body.tex").write_text("Exact canonical words: æ, œ, †.\n", encoding="utf-8")
        common = self.root / "src/common"
        common.mkdir(parents=True)
        (common / "preamble.tex").write_bytes(b"\\documentclass{article}\n% untouched typography\n")
        (self.root / "Makefile").write_text("# source recipe\n", encoding="utf-8")
        self.manifest = schema.adapter_manifest(self.root, self.leaf)
        (self.leaf / "publication.toml").write_text(schema.dumps_manifest(self.manifest), encoding="utf-8")
        self.identity = "publication:gpt/articles/faith/example"
        self.documents = {self.identity: {"id": self.identity, "document": self.identity,
                                         "edition": "main", "title": "Example"}}
        self.recipe = {"id": self.identity, "family": "publication", "provider": "gpt",
                       "canonical": "articles/faith/example", "document": "articles/faith/example",
                       "edition": "main", "entrypoint": "src/gpt/articles/faith/example/main.tex",
                       "dependencies": ["Makefile", "src/gpt/articles/faith/example/main.tex"]}
        self.revision = "a" * 40

    def prepare(self, **changes):
        arguments = dict(root=self.root, documents=self.documents, revision=self.revision,
                         recipe=self.recipe)
        arguments.update(changes)
        with patch.object(printing, "check", side_effect=lambda recipe, **_: recipe):
            return bundles.prepare_bundle(self.identity, **arguments)

    def test_original_source_bytes_paths_and_native_working_directory_survive(self):
        result = self.prepare()
        actual = {row["path"]: bundles.file_bytes(row) for row in result["files"]}
        self.assertEqual(result["schema"], bundles.SCHEMA)
        self.assertEqual(result["entrypoint"], "src/gpt/articles/faith/example/main.tex")
        self.assertEqual(result["cwd"], "src/gpt")
        self.assertEqual(result["environment"], {"TEXINPUTS": "..:"})
        self.assertEqual(result["engine"], "pdftex")
        self.assertEqual(result["format"], "pdflatex")
        self.assertEqual(actual[result["entrypoint"]], self.main.read_bytes())
        self.assertEqual(actual["src/common/preamble.tex"], (self.root / "src/common/preamble.tex").read_bytes())
        self.assertEqual(actual["src/gpt/articles/faith/example/body.tex"], (self.leaf / "body.tex").read_bytes())
        self.assertTrue(result["options"]["settle_auxiliary_files"])
        self.assertFalse(result["options"]["shell_escape"])
        self.assertFalse(any(path.suffix == ".pdf" for path in self.root.rglob("*")))

    def test_literal_import_is_included_even_when_make_graph_omits_it(self):
        result = self.prepare()
        self.assertIn("src/gpt/articles/faith/example/body.tex", [row["path"] for row in result["files"]])
        self.assertIn("src/gpt/articles/faith/example/body.tex", [row["path"] for row in result["source_inputs"]])

    def test_missing_literal_import_refuses_source_preparation(self):
        (self.leaf / "body.tex").unlink()
        with self.assertRaisesRegex(ValueError, "unresolved literal input"):
            self.prepare()

    def test_unadmitted_or_wrong_output_is_rejected_before_native_selection(self):
        with patch.object(printing, "select") as select:
            with self.assertRaisesRegex(bundles.BundleError, "not publicly admitted"):
                self.prepare(documents={})
            select.assert_not_called()
        other = dict(self.recipe, id=self.identity + "-synthesis")
        with self.assertRaisesRegex(bundles.BundleError, "does not match"):
            self.prepare(recipe=other)

    def test_companion_selection_keeps_its_own_identity_and_source(self):
        companion = self.leaf / "synthesis.tex"
        companion.write_bytes(b"Distinct concise prose.\n")
        identity = self.identity + "-synthesis"
        selected = dict(self.recipe, id=identity, edition="synthesis", entrypoint=companion.relative_to(self.root).as_posix())
        documents = {identity: {"id": identity, "document": self.identity, "edition": "synthesis", "title": "Concise"}}
        selected["dependencies"] = list(selected["dependencies"]) + [selected["entrypoint"]]
        # The fixture's canonical manifest intentionally has one output; the
        # bundle still cannot confuse a selected source with the main entry.
        with patch.object(printing, "check", side_effect=lambda recipe, **_: recipe):
            result = bundles.prepare_bundle(identity, root=self.root, documents=documents,
                                             revision=self.revision, recipe=selected)
        self.assertEqual(result["output_id"], identity)
        self.assertEqual(result["document"], self.identity)
        self.assertEqual(result["edition"], "synthesis")
        self.assertEqual(result["entrypoint"], selected["entrypoint"])
        self.assertNotEqual(result["content_sha256"], self.prepare()["content_sha256"])

    def test_source_and_render_changes_invalidate_bundle_identity(self):
        original = self.prepare()
        (self.leaf / "body.tex").write_text("Changed canonical words.\n", encoding="utf-8")
        changed = self.prepare()
        self.assertNotEqual(original["content_sha256"], changed["content_sha256"])
        (self.root / "src/common/preamble.tex").write_text("Changed geometry.\n", encoding="utf-8")
        restyled = self.prepare()
        self.assertNotEqual(changed["content_sha256"], restyled["content_sha256"])

    def test_traversal_symlink_and_hash_tampering_are_refused(self):
        for value in ("../secret.tex", "/secret.tex", "src//main.tex", "src/.git/config", "src/main\\other.tex"):
            with self.subTest(value=value), self.assertRaises(bundles.BundleError):
                bundles._file(value, b"words")
        linked = self.leaf / "linked.tex"
        linked.symlink_to(self.leaf / "body.tex")
        recipe = copy.deepcopy(self.recipe)
        recipe["dependencies"].append(linked.relative_to(self.root).as_posix())
        with self.assertRaisesRegex(bundles.BundleError, "symlink"):
            self.prepare(recipe=recipe)
        result = self.prepare()
        tampered = copy.deepcopy(result)
        tampered["files"][0]["content"] += "different"
        with self.assertRaisesRegex(bundles.BundleError, "identity mismatch"):
            bundles.validate_bundle(tampered)

    def test_binary_asset_transport_is_lossless_and_strict(self):
        payload = b"\x89PNG\r\n\x1a\n\xff\x00exact"
        record = bundles._file("src/gpt/articles/faith/example/image.png", payload)
        self.assertEqual(record["encoding"], "base64")
        self.assertEqual(bundles.file_bytes(record), payload)
        record["bytes"] += 1
        with self.assertRaisesRegex(bundles.BundleError, "size or hash"):
            bundles.file_bytes(record)

    def test_production_binary_assets_are_deduplicated_and_hash_bound(self):
        image = self.leaf / "image.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\n\xffexact illustration")
        (self.leaf / "body.tex").write_text("\\includegraphics{articles/faith/example/image.png}\n", encoding="utf-8")
        recipe = copy.deepcopy(self.recipe)
        recipe["dependencies"].append(image.relative_to(self.root).as_posix())
        assets = {}
        first = self.prepare(recipe=recipe, external_assets=assets)
        second = self.prepare(recipe=recipe, external_assets=assets)
        self.assertEqual(len(assets), 1)
        self.assertEqual(first, second)
        record = next(row for row in first["files"] if row["path"].endswith("image.png"))
        self.assertEqual(record["encoding"], "url")
        self.assertNotIn("content", record)
        self.assertEqual(record["href"], "../assets/" + hashlib.sha256(image.read_bytes()).hexdigest() + ".png")
        self.assertEqual(next(iter(assets.values())), image.read_bytes())
        self.assertIs(bundles.validate_bundle(first), first)

    def test_unreferenced_binary_directory_sibling_is_not_published(self):
        image = self.leaf / "superseded.png"
        image.write_bytes(b"\x89PNG\xffunselected precursor")
        recipe = copy.deepcopy(self.recipe)
        recipe["dependencies"].append(image.relative_to(self.root).as_posix())
        result = self.prepare(recipe=recipe)
        self.assertNotIn(image.relative_to(self.root).as_posix(), [row["path"] for row in result["files"]])

    def test_comments_and_prose_mentions_do_not_admit_an_image(self):
        image = self.leaf / "superseded.png"
        image.write_bytes(b"\x89PNG\xffunselected precursor")
        (self.leaf / "body.tex").write_text(
            "% rejected precursor: articles/faith/example/superseded.png\n"
            "% \\includegraphics{articles/faith/example/superseded.png}\n"
            "The old artwork path was articles/faith/example/superseded.png.\n", encoding="utf-8")
        recipe = copy.deepcopy(self.recipe)
        recipe["dependencies"].append(image.relative_to(self.root).as_posix())
        result = self.prepare(recipe=recipe)
        self.assertNotIn(image.relative_to(self.root).as_posix(), [row["path"] for row in result["files"]])

    def test_unknown_computed_image_selection_requires_an_owner(self):
        image = self.leaf / "selected.png"
        image.write_bytes(b"\x89PNG\xffimage")
        (self.leaf / "body.tex").write_text("\\includegraphics{\\ChosenArtwork}\n", encoding="utf-8")
        recipe = copy.deepcopy(self.recipe)
        recipe["dependencies"].append(image.relative_to(self.root).as_posix())
        with self.assertRaisesRegex(bundles.BundleError, "owning selection adapter"):
            self.prepare(recipe=recipe)

    def test_source_change_during_assembly_refuses_transport(self):
        original = bundles._publication_files
        def change(*arguments):
            files = original(*arguments)
            (self.leaf / "body.tex").write_text("Concurrent change.\n", encoding="utf-8")
            return files
        with patch.object(bundles, "_publication_files", side_effect=change):
            with self.assertRaisesRegex(bundles.BundleError, "inputs changed"):
                self.prepare()

    def test_generated_source_uses_owning_producer_without_pdf_engine(self):
        identity = "bible:example"
        documents = {identity: {"id": identity, "document": identity, "edition": "main", "title": "Example Bible"}}
        recipe = {"id": identity, "family": "bible", "document": "example", "dependencies": ["Makefile"]}
        def render(root, name, *arguments):
            self.assertEqual(name, "typeset-bible")
            self.assertEqual(arguments[:3], ("render", "--bible", "example"))
            out = Path(arguments[arguments.index("--out") + 1])
            out.mkdir(parents=True)
            path = out / "example.tex"
            path.write_bytes(b"Original native Bible typography and complete text.\n")
            return {"rendered": [{"path": str(path)}]}
        with patch.object(printing, "check", side_effect=lambda recipe, **_: recipe), \
                patch.object(printing, "_json_tool", side_effect=render):
            result = bundles.prepare_bundle(identity, root=self.root, documents=documents,
                                             recipe=recipe, revision=self.revision)
        self.assertEqual(result["entrypoint"], "native/bible/example/example.tex")
        self.assertEqual(result["cwd"], "native/bible/example")
        self.assertEqual(len(result["files"]), 1)
        self.assertEqual(result["input_contract"], "owning-native-source-producer/v1")
        self.assertFalse(any(path.suffix == ".pdf" for path in self.root.rglob("*")))

    def test_catalog_binds_routes_bytes_hashes_and_exact_output_universe(self):
        with patch.object(printing, "select", return_value=self.recipe), \
                patch.object(printing, "check_many", side_effect=lambda recipes, **_: [
                    dict(recipe, status="valid", validation={"fixture_source_check": "pass"}) for recipe in recipes]):
            result = bundles.prepare_catalog(self.root, documents=self.documents, revision=self.revision)
        descriptor = result["bundles"][self.identity]
        payload = result["assets"][descriptor["route"]]
        self.assertEqual(descriptor["sha256"], hashlib.sha256(payload).hexdigest())
        self.assertEqual(descriptor["bytes"], len(payload))
        self.assertEqual(json.loads(payload)["output_id"], self.identity)
        self.assertIn("src/common/preamble.tex", result["source_paths"])
        self.assertTrue(descriptor["route"].startswith("native-tex/sources/"))
        self.assertEqual(len(result["assets"]), 1)
        with self.assertRaisesRegex(bundles.BundleError, "unadmitted or duplicate"):
            bundles.prepare_catalog(self.root, documents=self.documents, revision=self.revision,
                                    output_ids=[self.identity, self.identity])


class SharedNativeSourceTests(unittest.TestCase):
    setUp = NativeSourceBundleTests.setUp
    prepare = NativeSourceBundleTests.prepare

    def test_browser_source_transport_adversarial_cases(self):
        run = subprocess.run(["node", "--test", str(ROOT / "tools/tests/native_source_transport.mjs")],
                             cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_revision_is_provenance_and_exact_render_inputs_are_identity(self):
        original = self.prepare()
        later = self.prepare(revision="b" * 40)
        self.assertNotEqual(original["content_sha256"], later["content_sha256"])
        self.assertEqual(original["render_sha256"], later["render_sha256"])
        for field, value in (("entrypoint", "src/gpt/articles/faith/example/body.tex"),
                             ("cwd", "src"), ("engine", "xetex"), ("format", "xelatex"),
                             ("document", "other"), ("output_id", "other"), ("edition", "synthesis"),
                             ("environment", {"TEXINPUTS": ".:"}), ("options", {})):
            with self.subTest(field=field):
                changed = dict(original, **{field: value})
                self.assertNotEqual(original["render_sha256"], bundles.render_identity(changed))
        changed = copy.deepcopy(original)
        changed["files"][0]["sha256"] = "c" * 64
        changed["content_sha256"] = bundles._sha(bundles.canonical({k: v for k, v in changed.items() if k != "content_sha256"}))
        with self.assertRaises(bundles.BundleError):
            bundles.validate_bundle(changed)

    def shared(self):
        # Compression is beneficial for these exact canonical style bytes.
        (self.root / "src/common/preamble.tex").write_bytes(b"\\documentclass{article}\r\n" + b"% exact shared typography\r\n" * 100)
        (self.leaf / "body.tex").write_text("Original æ, œ, †.\r\n" * 100, encoding="utf-8", newline="")
        original = self.prepare()
        assets = {}
        result = bundles._externalize(original, assets, shared_text={row["sha256"] for row in original["files"]})
        return original, result, assets

    def test_shared_transports_preserve_every_byte_path_and_render_identity(self):
        original, result, assets = self.shared()
        self.assertEqual(original["render_sha256"], result["render_sha256"])
        self.assertNotEqual(original["content_sha256"], result["content_sha256"])
        self.assertEqual([row["path"] for row in original["files"]], [row["path"] for row in result["files"]])
        expected = {row["sha256"]: bundles.file_bytes(row) for row in original["files"]}
        for row in result["files"]:
            self.assertEqual(assets["native-tex/" + row["href"][3:]], expected[row["sha256"]])
        self.assertTrue(result["sourcePacks"])
        for pack in result["sourcePacks"]:
            payload = assets["native-tex/" + pack["href"][3:]]
            self.assertEqual(hashlib.sha256(payload).hexdigest(), pack["sha256"])
            self.assertEqual(payload[4:8], b"\0" * 4)
            self.assertEqual(payload[9], 255)
            expanded = gzip.decompress(payload)
            self.assertEqual(len(expanded), pack["expanded_bytes"])
            for member in pack["files"]:
                self.assertEqual(expanded[member["offset"]:member["offset"] + member["bytes"]], expected[member["sha256"]])
        first_assets = dict(assets)
        repeated = bundles._externalize(original, assets, shared_text=set(expected))
        self.assertEqual(repeated, result)
        self.assertEqual(first_assets, assets)
        # The controller consumes the Python producer's real canonical hash.
        fixture = self.root / ".scratch" / "controller-fixture.json"
        fixture.write_text(json.dumps({"bundle": result, "assets": {key: list(value) for key, value in assets.items()}}), encoding="utf-8")
        run = subprocess.run(["node", str(ROOT / "tools/tests/native_source_transport.mjs"), "--fixture", str(fixture)],
                             cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)

    def test_pack_metadata_refuses_substitution_duplicate_gaps_and_oversize(self):
        _, original, _ = self.shared()
        mutations = [lambda p: p.update(href="../assets/elsewhere.bin"),
                     lambda p: p.update(expanded_bytes=8 * 1024 * 1024 + 1),
                     lambda p: p.update(bytes=True), lambda p: p.update(compression="zip"),
                     lambda p: p.update(extra="unowned"),
                     lambda p: p["files"][0].update(sha256="f" * 64),
                     lambda p: p["files"][0].update(offset=1),
                     lambda p: p["files"][0].update(bytes=True),
                     lambda p: p["files"].append(copy.deepcopy(p["files"][0])),
                     lambda p: p.update(expanded_bytes=p["expanded_bytes"] + 1)]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                changed = copy.deepcopy(original)
                mutate(changed["sourcePacks"][0])
                changed["content_sha256"] = bundles._sha(bundles.canonical({k: v for k, v in changed.items() if k != "content_sha256"}))
                with self.assertRaises(bundles.BundleError):
                    bundles.validate_bundle(changed)

    def test_unprofitable_and_oversize_packs_keep_exact_raw_transport(self):
        original = self.prepare()
        with patch.object(bundles, "_SOURCE_PACK_BYTES", 1):
            assets = {}
            result = bundles._externalize(original, assets, shared_text={row["sha256"] for row in original["files"]})
        self.assertNotIn("sourcePacks", result)
        self.assertTrue(all(row["encoding"] == "url" for row in result["files"]))
        self.assertEqual(result["render_sha256"], original["render_sha256"])

    def test_catalog_style_changes_only_affected_render_inputs_and_transports(self):
        self.shared()
        companion = self.leaf / "synthesis.tex"
        companion.write_text("Distinct companion words.\n")
        identity = self.identity + "-synthesis"
        documents = {**self.documents, identity: {"id": identity, "document": self.identity, "edition": "synthesis", "title": "Concise"},
                     "bible:unrelated": {"id": "bible:unrelated", "document": "bible:unrelated", "edition": "main", "title": "Unrelated"}}
        other = dict(self.recipe, id=identity, edition="synthesis", entrypoint=companion.relative_to(self.root).as_posix(),
                     dependencies=[*self.recipe["dependencies"], companion.relative_to(self.root).as_posix()])
        recipes = {(self.identity, "main"): self.recipe, (self.identity, "synthesis"): other,
                   ("bible:unrelated", "main"): {"id": "bible:unrelated", "family": "bible", "document": "unrelated", "dependencies": ["Makefile"]}}
        def catalog(revision):
            with patch.object(printing, "select", side_effect=lambda document, edition, **_: recipes[document, edition]), \
                    patch.object(printing, "check_many", side_effect=lambda recipes, **_: [dict(r, status="valid", validation={"source": "pass"}) for r in recipes]), \
                    patch.object(bundles, "_generated_files", return_value=({"native/bible/unrelated/main.tex": b"Independent Bible source.\n"}, "native/bible/unrelated/main.tex", "native/bible/unrelated")), \
                    patch.object(bundles, "_run") as compiler:
                result = bundles.prepare_catalog(self.root, documents=documents, revision=revision)
                compiler.assert_not_called()
                return result
        original = catalog(self.revision)
        later = catalog("b" * 40)
        read = lambda cat, identity: json.loads(cat["assets"][cat["bundles"][identity]["route"]])
        for selected in documents:
            self.assertEqual(read(original, selected)["render_sha256"], read(later, selected)["render_sha256"])
        style = self.root / "src/common/preamble.tex"
        style.write_bytes(style.read_bytes() + b"% changed style only\n")
        restyled = catalog(self.revision)
        for selected in (self.identity, identity):
            before, after = read(original, selected), read(restyled, selected)
            self.assertNotEqual(before["render_sha256"], after["render_sha256"])
            before_files = {row["path"]: row for row in before["files"]}
            after_files = {row["path"]: row for row in after["files"]}
            for path in before_files:
                if path != "src/common/preamble.tex":
                    self.assertEqual(before_files[path], after_files[path])
            before_packs = {p["href"] for p in before.get("sourcePacks", [])}
            after_packs = {p["href"] for p in after.get("sourcePacks", [])}
            self.assertEqual(len(before_packs - after_packs), 1)
            self.assertEqual(len(after_packs - before_packs), 1)
        self.assertEqual(read(original, "bible:unrelated"), read(restyled, "bible:unrelated"))


if __name__ == "__main__":
    unittest.main()
