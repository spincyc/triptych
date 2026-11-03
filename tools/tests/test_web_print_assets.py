"""Offline source-bound render product lookup and hostile delivery rejection."""
from __future__ import annotations
import copy
import io
import json
from pathlib import Path
import struct
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _artifact_store as transport
import _web_print_assets as assets
import _web_print_diagrams as diagrams


class WebPrintAssetTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/web-print-asset-domain/tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.pack = self.root / ".scratch/pack"
        production = json.loads((ROOT / assets.INDEX_PATH).read_text())
        self.data = {"schema": assets.SCHEMA, "provenance": {}, "payloads": {},
                     "server": {"origin": {}, "source_inputs": {}, "definitions": {}, "variants": production["server"]["variants"], "entries": {}},
                     "generic": {"origin": {}, "outputs": {}},
                     "fonts": copy.deepcopy(production["fonts"])}
        self.payloads = {}
        self.svg = b'<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/></svg>'
        self.server_src = self.payload(self.svg, "image/svg+xml", "project-render-product")
        self.source = assets.SERVER_OWNER + "shared/test-diagrams.tex"
        macro = r"\newcommand{\DemoDiagram}{canonical definition}"
        self.write(self.source, macro.encode())
        pin = assets.digest(macro)
        self.data["server"]["source_inputs"] = {self.source: pin}
        self.data["server"]["definitions"] = {pin: {"source": self.source, "line": 1, "start": 0, "end": len(macro), "sha256": pin}}
        self.data["server"]["entries"] = {"child:DemoDiagram": {"variant": "child", "macro": "DemoDiagram", "payload": self.server_src, "includes_caption": False, "definition": pin, "definition_closure": [{"macro": "DemoDiagram", "definition": pin}], "usage": [{"source": self.source, "line": 1}]}}
        self.output_id = "gpt/test"
        self.generic_source = "src/gpt/test/main.tex"
        body = r"\begin{tikzpicture}\node {Actual label};\end{tikzpicture}"
        self.write(self.generic_source, body.encode())
        state = {"entrypoint": self.generic_source, "role": "main", "flags": {"TriptychPrintEdition": False, "TriptychSynthesisEdition": False, "TriptychHomilyEdition": False}, "ordered_inputs": [{"path": self.generic_source, "occurrence": 1, "sha256": assets.digest(body), "selected_sha256": assets.digest(body)}]}
        state["selection_digest"] = assets.digest(assets.canonical_json(state))
        self.selection = {"head": "", "body": body, "selection": state, "chunks": [{"path": self.generic_source, "occurrence": 1, "selected_line": 1, "text": body}]}
        generic_src = self.payload(self.svg.replace(b"1 1", b"2 2"), "image/svg+xml", "project-render-product")
        unit = {**diagrams.diagram_spans(body)[0], "asset_id": "tikz-" + "a" * 24, "index": 1, "payload": generic_src, "svg_sha256": assets.digest(self.payloads[generic_src]), "bytes": len(self.payloads[generic_src]), "width": "1pt", "height": "1pt", "viewBox": "0 0 1 1", "labels_sha256": assets.digest(assets.canonical_json(diagrams.node_labels(body))), "source_refs": diagrams.selected_source_refs(self.selection, 0, len(body)), "selection_digest": state["selection_digest"], "source_closure_digest": assets.digest(assets.canonical_json(diagrams.closure(self.selection))), "recipe_digest": "0" * 64, "runtime_fingerprint": "1" * 64, "includes_caption": False}
        self.data["generic"]["outputs"][self.output_id] = {"selection_digest": state["selection_digest"], "head_sha256": assets.digest(""), "body_sha256": assets.digest(body), "source_closure": {self.generic_source: assets.digest(body)}, "entrypoint": self.generic_source, "role": "main", "flags": state["flags"], "diagrams": [unit]}
        coverage = json.loads((ROOT / assets.FONT_ROOT / "glyph-coverage.json").read_text())
        for face, cmap in zip(self.data["fonts"]["faces"], coverage["faces"]):
            body = bytearray(48 + len(face["name"]))
            body[:4] = b"wOF2"; struct.pack_into(">I", body, 8, len(body)); body[48:] = face["name"].encode()
            face["payload"] = self.payload(bytes(body), "font/woff2", "font-software")
            cmap["woff2_sha256"] = assets.digest(body); cmap["woff2_bytes"] = len(body)
        for field in ("license", "coverage", "control_policy"):
            row = self.data["fonts"][field]
            body = (assets.canonical_json(coverage) if field == "coverage" else (ROOT / row["path"]).read_bytes())
            self.write(row["path"], body); row.update(sha256=assets.digest(body), bytes=len(body))
        entries = [{"path": path, **record} for path, record in self.data["payloads"].items()]
        archives, members = transport.pack_delivery_archives(self.root, self.pack, entries, resolver=lambda root, path: self.root / ".scratch/inputs" / path, release="test", archive_prefix="test")
        self.delivery = {"schema": assets.DELIVERY_SCHEMA, "archives": archives, "artifacts": members}
        self.save()

    def write(self, path, body):
        destination = self.root / path; destination.parent.mkdir(parents=True, exist_ok=True); destination.write_bytes(body)

    def payload(self, body, media, kind):
        pin = assets.digest(body)
        src = assets.PREFIX + pin + (".svg" if media == "image/svg+xml" else ".woff2")
        self.data["payloads"][src] = {"sha256": pin, "bytes": len(body), "media_type": media, "kind": kind}
        self.payloads[src] = body; self.write(".scratch/inputs/" + src, body)
        return src

    def save(self):
        self.data["registry_digest"] = assets.digest(assets.canonical_json({k: v for k, v in self.data.items() if k != "registry_digest"}))
        transport._json(self.root / assets.INDEX_PATH, self.data)
        transport._json(self.root / assets.DELIVERY_PATH, self.delivery)

    def hydrate(self):
        return assets.hydrate(self.root, archive_dir=self.pack)

    def test_metadata_check_needs_no_payloads_or_network(self):
        with patch.object(transport, "urlopen", side_effect=AssertionError("network")):
            self.assertEqual(assets.validate_registry(self.root)["payloads"], 10)
            with self.assertRaises(FileNotFoundError):
                assets.server_asset(self.root, "child", "DemoDiagram")
            with self.assertRaises(FileNotFoundError):
                assets.hydrate(self.root)

    def test_offline_roundtrip_and_api(self):
        with patch.object(transport, "urlopen", side_effect=AssertionError("network")):
            self.assertEqual(self.hydrate()["hydrated"], 10)
            record = assets.server_asset(self.root, "child", "DemoDiagram")
            self.assertEqual(record["body"], self.svg)
            self.assertEqual(record["source_inputs"], self.data["server"]["source_inputs"])
            self.assertFalse(record["includes_caption"])
            self.assertNotIn("body", assets.server_asset(self.root, "child", "DemoDiagram", include_body=False))
            generic = assets.generic_assets(self.root, self.output_id, self.selection)
            self.assertEqual(generic[0]["labels"], ["Actual label"])
            self.assertEqual(assets.asset_bytes(self.root, generic[0]["asset_id"]), generic[0]["body"])
            fonts = assets.font_assets(self.root)
            self.assertEqual(len(fonts), 8)
            self.assertEqual(assets.asset_bytes(self.root, fonts[0]["id"]), fonts[0]["body"])
            self.assertEqual(assets.asset_bytes(self.root, fonts[0]["license"]["src"]), fonts[0]["license"]["body"])

    def test_explicit_fetch_only(self):
        archive = self.delivery["archives"][0]
        with patch.object(transport, "urlopen", return_value=io.BytesIO((self.pack / archive["name"]).read_bytes())) as download:
            self.assertEqual(assets.hydrate(self.root, fetch=True)["hydrated"], 10)
            download.assert_called_once()

    def test_current_source_tamper_rejected(self):
        self.hydrate(); self.write(self.source, b"changed canonical source")
        with self.assertRaisesRegex(assets.AssetError, "source closure"):
            assets.server_asset(self.root, "child", "DemoDiagram")

    def test_source_span_tamper_rejected_even_with_valid_registry_digest(self):
        definition = next(iter(self.data["server"]["definitions"].values()))
        definition["start"] += 1; self.save()
        with self.assertRaisesRegex(assets.AssetError, "macro source span"):
            assets.validate_registry(self.root)

    def test_generic_selected_text_tamper_rejected(self):
        self.hydrate(); selected = copy.deepcopy(self.selection); selected["body"] += " changed"
        with self.assertRaisesRegex(assets.AssetError, "stale selected-output"):
            assets.generic_assets(self.root, self.output_id, selected)

    def test_generic_label_and_occurrence_pins_rejected(self):
        self.hydrate(); row = self.data["generic"]["outputs"][self.output_id]["diagrams"][0]
        row["labels_sha256"] = "0" * 64; self.save()
        with self.assertRaisesRegex(assets.AssetError, "label/source"):
            assets.generic_assets(self.root, self.output_id, self.selection)

    def test_missing_generic_projection_fails_only_for_active_diagram(self):
        with self.assertRaisesRegex(assets.AssetError, "no verified"):
            assets.generic_assets(self.root, "gpt/missing", self.selection)
        self.assertEqual(assets.generic_assets(self.root, "gpt/missing", {"body": "plain text"}), [])

    def test_cached_asset_tamper_rejected(self):
        self.hydrate(); entry = next(r for r in self.delivery["artifacts"] if r["path"] == self.server_src)
        target = transport.cache_path(self.root, entry); target.chmod(0o600); target.write_bytes(self.svg + b"x")
        with self.assertRaisesRegex(ValueError, "hash or size"):
            assets.server_asset(self.root, "child", "DemoDiagram")

    def test_returned_body_is_verified_after_read(self):
        self.hydrate()
        original = transport._verify
        def changed_after_verification(path, entry):
            result = original(path, entry)
            if entry.get("path") == self.server_src:
                path.chmod(0o600); path.write_bytes(self.svg.replace(b"1 1", b"9 9"))
            return result
        with patch.object(transport, "_verify", side_effect=changed_after_verification):
            with self.assertRaisesRegex(assets.AssetError, "changed during read"):
                assets.server_asset(self.root, "child", "DemoDiagram")

    def test_registry_delivery_identity_mismatch_rejected(self):
        self.delivery["artifacts"][0]["sha256"] = "f" * 64; self.save()
        with self.assertRaisesRegex(assets.AssetError, "identity mismatch"):
            assets.validate_registry(self.root)

    def test_historical_evidence_kind_not_accepted(self):
        self.delivery["artifacts"][0]["kind"] = "source-evidence"; self.save()
        with self.assertRaises(assets.AssetError): assets.validate_registry(self.root)

    def test_undeclared_local_file_not_used(self):
        self.write("web-print-assets/undeclared.svg", self.svg)
        with self.assertRaisesRegex(assets.AssetError, "unknown browser-print"):
            assets.asset_bytes(self.root, "web-print-assets/undeclared.svg")

    def test_symlinked_cache_parent_rejected(self):
        self.hydrate(); entry = self.delivery["artifacts"][0]
        target = transport.cache_path(self.root, entry); moved = target.parent.with_name("moved")
        target.parent.rename(moved); target.parent.symlink_to(moved, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            assets.asset_bytes(self.root, entry["path"])

    def test_archive_traversal_or_link_rejected(self):
        for mode in ("traversal", "symlink", "extra"):
            with self.subTest(mode=mode):
                archive = self.delivery["archives"][0]; path = self.pack / archive["name"]
                with tarfile.open(path, "w") as stream:
                    info = tarfile.TarInfo("../escape" if mode == "traversal" else "extra" if mode == "extra" else self.server_src)
                    if mode == "symlink": info.type = tarfile.SYMTYPE; info.linkname = "../escape"
                    else: info.size = len(self.svg)
                    stream.addfile(info, io.BytesIO(self.svg) if info.isreg() else None)
                old = archive["id"]; archive.update(id=transport._digest(path), sha256=transport._digest(path), bytes=path.stat().st_size)
                for row in self.delivery["artifacts"]:
                    if row["archive"] == old: row["archive"] = archive["id"]
                self.save()
                with self.assertRaises(ValueError): self.hydrate()
                self.assertFalse((self.root / "escape").exists())

    def test_svg_active_content_external_resources_and_entities_rejected(self):
        bad = [b'<svg xmlns="http://www.w3.org/2000/svg"><script/></svg>',
               b'<svg xmlns="http://www.w3.org/2000/svg" onload="evil()"/>',
               b'<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.org/x.png"/></svg>',
               b'<svg xmlns="http://www.w3.org/2000/svg"><path fill="url(https://example.org/x)"/></svg>',
               b'<!DOCTYPE svg [<!ENTITY x "x">]><svg xmlns="http://www.w3.org/2000/svg"/>']
        for body in bad:
            with self.subTest(body=body), self.assertRaises(assets.AssetError): assets._typed(body, "image/svg+xml")

    def test_font_magic_length_and_license_tamper_rejected(self):
        for body in (b"not a font", b"wOF2" + b"\0" * 50):
            with self.assertRaises(assets.AssetError): assets._typed(body, "font/woff2")
        self.write(self.data["fonts"]["license"]["path"], b"changed license")
        with self.assertRaises(ValueError): assets.validate_registry(self.root)

    def test_cmap_ranges_and_face_binding_rejected(self):
        row = self.data["fonts"]["coverage"]
        coverage = json.loads((self.root / row["path"]).read_text())
        coverage["faces"][0]["ranges"] = [[0xD800, 0xDFFF]]
        body = assets.canonical_json(coverage); self.write(row["path"], body)
        row.update(sha256=assets.digest(body), bytes=len(body)); self.save()
        with self.assertRaisesRegex(assets.AssetError, "coverage ranges"):
            assets.validate_registry(self.root)

    def test_registry_mutation_copy_and_duplicate_keys(self):
        data = assets.load_index(self.root); data["schema"] = "changed"
        self.assertEqual(assets.load_index(self.root)["schema"], assets.SCHEMA)
        self.write(assets.INDEX_PATH, b'{"schema":"x","schema":"y"}')
        with self.assertRaises(assets.AssetError): assets.load_index(self.root)

    def test_compact_production_registry_contains_no_source_copies(self):
        production = json.loads((ROOT / assets.INDEX_PATH).read_text())
        forbidden = {"definition_tex", "body", "head", "source", "labels", "commands", "runtime_closure"}
        def walk(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if key == "source":
                        self.assertIsInstance(child, (str, dict))
                        if isinstance(child, str): self.assertTrue(child.startswith("src/"))
                    else: self.assertNotIn(key, forbidden)
                    walk(child)
            elif isinstance(value, list):
                for child in value: walk(child)
        walk(production)
        self.assertEqual(len(production["server"]["entries"]), 39)
        self.assertEqual(sum(len(r["diagrams"]) for r in production["generic"]["outputs"].values()), 21)


if __name__ == "__main__":
    unittest.main()
