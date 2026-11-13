"""Selected History products retain the strict producer's evidence and bytes."""
from contextlib import nullcontext
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _reader_history_products as reader
import _eucharistic_texts as texts

SCRATCH = ROOT / ".scratch/history-reader/tests"


class Index:
    def __init__(self, files):
        self.files = dict(files)
        self.identities = {path: (hashlib.sha256(body).hexdigest(), len(body))
                           for path, body in files.items()}
        self.reads = []

    def read(self, path):
        self.reads.append(path)
        body = self.files[path]
        if (hashlib.sha256(body).hexdigest(), len(body)) != self.identities[path]:
            raise ValueError("stale canonical source")
        return body

    def metadata(self, path):
        return self.identities[path]

    def verified_reads(self):
        return nullcontext({})

    def paths(self, prefix, suffix):
        return tuple(sorted(path for path in self.files if path.startswith(prefix) and path.endswith(suffix)))


class ReaderHistoryProductsTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def binding_index(self):
        book = {"id": "fixture", "title": "Fixture constituent", "stage_ids": ["fixture-stage"],
                "catalogue_witness_ids": ["fixture:witness"], "components": ["ordinary"],
                "witnesses": [{"id": "witness", "edition_id": "edition.fixture"}],
                "extent_kind": "constituent"}
        self.book_path = texts.NATIVE_BOOK_DIRECTORY + "/fixture.json"
        self.body_path = "src/sources/works/fixture/body.txt"
        files = {self.book_path: reader._json(book), self.body_path: b"Literal fixture words.\n"}
        stamps = [{"path": path, "sha256": hashlib.sha256(body).hexdigest(), "byte_size": len(body)}
                  for path, body in sorted(files.items())]
        data = {"schema": reader.INDEX_SCHEMA, "editorial_approval": False,
                "tools_sha256": reader._digest([]), "stages_sha256": reader._digest([]),
                "inputs": [row["path"] for row in stamps],
                "bindings": {"native-book:fixture": {"inputs": list(range(len(stamps))),
                                                    "sha256": reader._digest(stamps)}}}
        return Index({**files, reader.INDEX_PATH: reader._json(data)})

    def test_catalogue_binding_reads_metadata_without_opening_literal_text(self):
        index = self.binding_index()
        with patch.object(reader, "_tool_paths", return_value=()):
            payload = reader.NativeBindings(self.root, index)("native-book:fixture", self.root)
        self.assertEqual("Fixture constituent", payload["title"])
        self.assertEqual(["fixture-stage"], payload["book_binding"]["stage_ids"])
        self.assertFalse(payload["scope"]["whole_book_complete"])
        self.assertEqual([reader.INDEX_PATH, self.book_path], index.reads)
        self.assertNotIn("units", payload)
        self.assertEqual(2, len(payload["inputs"]))

    def test_changed_native_dependency_is_refused_without_opening_its_body(self):
        index = self.binding_index()
        index.identities[self.body_path] = ("0" * 64, 22)
        with patch.object(reader, "_tool_paths", return_value=()):
            with self.assertRaisesRegex(texts.AdapterError, "dependencies changed"):
                reader.NativeBindings(self.root, index)("native-book:fixture", self.root)
        self.assertNotIn(self.body_path, index.reads)

    def test_missing_binding_is_not_silently_reconstructed_or_advertised(self):
        index = self.binding_index()
        with patch.object(reader, "_tool_paths", return_value=()):
            with self.assertRaises(texts.AdapterError):
                reader.NativeBindings(self.root, index)("native-book:unlisted", self.root)
        self.assertEqual([reader.INDEX_PATH], index.reads)

    def test_changed_gate_implementation_invalidates_binding_lookup(self):
        index = self.binding_index()
        with patch.object(reader, "_tool_paths", return_value=("scripts/_eucharistic_texts.py",)):
            with self.assertRaisesRegex(ValueError, "lookup is stale"):
                reader.NativeBindings(self.root, index)

    def test_changed_book_bytes_are_verified_even_when_metadata_is_unchanged(self):
        index = self.binding_index()
        index.files[self.book_path] += b" "
        with patch.object(reader, "_tool_paths", return_value=()):
            with self.assertRaisesRegex(texts.AdapterError, "stale canonical source"):
                reader.NativeBindings(self.root, index)("native-book:fixture", self.root)

    def test_changed_stage_membership_cannot_keep_a_retired_binding_available(self):
        from _eucharistic_stages import DIRECTORY
        index = self.binding_index()
        path = DIRECTORY + "/changed.json"
        index.files[path] = b"{}"
        index.identities[path] = (hashlib.sha256(b"{}").hexdigest(), 2)
        with patch.object(reader, "_tool_paths", return_value=()):
            with self.assertRaisesRegex(ValueError, "stage membership changed"):
                reader.NativeBindings(self.root, index)

    def test_selected_act_fragment_matches_complete_projection_and_writes_nothing(self):
        act = reader._act_tool()
        data = act.load(ROOT / "src/sources/inventories/roman-holy-week-acts-v1.toml")
        complete = {}
        totals = act.fragments(data, self.root, data["slice"],
                               emit=lambda path, value: complete.setdefault(path.relative_to(self.root).as_posix(), value))
        selected = next(path for path in complete if "/station/" in path)
        held = {}
        selected_totals = act.fragments(data, self.root, data["slice"], selected=selected,
                                       emit=lambda path, value: held.setdefault(path.relative_to(self.root).as_posix(), value))
        self.assertEqual({selected: complete[selected]}, held)
        self.assertEqual(totals, selected_totals)
        self.assertEqual([], list(self.root.iterdir()))
        act.structure(data, self.root)
        path = self.root / "structure/act-history" / (data["slice"] + ".json")
        self.assertEqual(path.read_bytes(), reader._json(act.map_payload(data, totals)))

    def test_encyclicals_keep_canonical_bytes_and_refuse_withdrawn_rights(self):
        import _encyclicals
        for relative in (_encyclicals.INDEX_RELATIVE, _encyclicals.RELEASE_RELATIVE):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / relative).read_bytes())
        expected = _encyclicals.render(self.root / _encyclicals.INDEX_RELATIVE,
                                      self.root / _encyclicals.RELEASE_RELATIVE, self.root).encode()
        self.assertEqual(expected, reader.resolve("encyclicals/index.json", self.root, Index({})))
        source = json.loads((self.root / _encyclicals.INDEX_RELATIVE).read_bytes())
        selected = next(row for row in source["encyclicals"] if row["readers"])["readers"][0]
        release_path = self.root / _encyclicals.RELEASE_RELATIVE
        release = json.loads(release_path.read_bytes())
        document = next(row for row in release["documents"]
                        if (row["id"], row["language"]) == (selected["release_id"], selected["language"]))
        document["source"]["rights_status"] = "restricted"
        release_path.write_bytes(reader._json(release))
        with self.assertRaisesRegex(_encyclicals.EncyclicalsError, "public-domain"):
            reader.resolve("encyclicals/index.json", self.root, Index({}))

    def test_unrelated_family_does_not_open_history(self):
        index = Index({})
        self.assertIsNone(reader.resolve("structure/sources/index.json", self.root, index))
        self.assertEqual([], index.reads)


if __name__ == "__main__":
    unittest.main()
