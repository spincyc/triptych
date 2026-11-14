"""Cold reading, incremental projection reuse and the real indexed bridge."""
from contextlib import contextmanager
import json
import shutil
import unittest
from unittest.mock import patch

import test_corpus_index as fixtures
import _corpus_index as corpus
from lectern import bridge
from lectern.data import ReaderData
from lectern.repo import Refused


class IndexedDataTests(unittest.TestCase):
    git = fixtures.CorpusIndexTests.git
    put = fixtures.CorpusIndexTests.put

    def setUp(self):
        fixtures.CorpusIndexTests.setUp(self)
        self.calls = []

        def resolve(name, root, index):
            self.calls.append(name)
            if name == "structure/missing.json":
                return None
            return json.dumps({"text": index.read(self.payload).decode()}).encode()

        self.enterContext(patch("_reader_products.resolve", side_effect=resolve))

    def test_cold_and_new_session_cache_use_only_requested_sources(self):
        reader = ReaderData(self.root)
        body = reader.read("structure/one.json")
        self.assertEqual(json.loads(body)["text"], "Original whole source\n")
        self.assertEqual(self.calls, ["structure/one.json"])
        reader.close()
        self.assertEqual(ReaderData(self.root).read("structure/one.json"), body)
        self.assertEqual(self.calls, ["structure/one.json"])

    def test_changed_dependency_rebuilds_but_unrelated_edit_reuses(self):
        self.put("src/unrelated.txt", "An unrelated input")
        corpus.refresh(self.root)
        ReaderData(self.root).read("structure/one.json")
        self.put("src/unrelated.txt", "Changed unrelated input")
        corpus.refresh(self.root)
        ReaderData(self.root).read("structure/one.json")
        self.assertEqual(len(self.calls), 1)
        self.put(self.payload, "Changed source\n")
        corpus.refresh(self.root)
        body = ReaderData(self.root).read("structure/one.json")
        self.assertEqual(json.loads(body)["text"], "Changed source\n")
        self.assertEqual(len(self.calls), 2)

    def test_added_source_invalidates_enumeration_dependent_cache(self):
        def listing(name, root, index):
            self.calls.append(name)
            return json.dumps({"paths": index.paths(prefix="src/")}).encode()
        with patch("_reader_products.resolve", side_effect=listing):
            first = json.loads(ReaderData(self.root).read("structure/list.json"))
            self.put("src/new-member.txt", "A new source member")
            corpus.refresh(self.root)
            second = json.loads(ReaderData(self.root).read("structure/list.json"))
        self.assertNotIn("src/new-member.txt", first["paths"])
        self.assertIn("src/new-member.txt", second["paths"])
        self.assertEqual(len(self.calls), 2)

    def test_cancelled_reader_refuses_even_an_in_memory_record(self):
        reader = ReaderData(self.root)
        reader.read("structure/one.json")
        reader.cancel()
        with self.assertRaisesRegex(ValueError, "cancelled"):
            reader.read("structure/one.json")

    def test_cache_corruption_is_recomputed_from_canonical_bytes(self):
        original = ReaderData(self.root).read("structure/one.json")
        cache = next((self.root / ".scratch/reader-data").glob("*.json"))
        row = json.loads(cache.read_bytes())
        row["body"] = "e30="
        cache.write_text(json.dumps(row))
        self.assertEqual(ReaderData(self.root).read("structure/one.json"), original)
        self.assertEqual(len(self.calls), 2)

    def test_session_bytes_are_immutable_and_later_unread_change_refuses(self):
        reader = ReaderData(self.root)
        body = reader.read("structure/one.json")
        self.put(self.payload, "Mutated source\n")
        self.assertEqual(reader.read("structure/one.json"), body)
        with self.assertRaises(corpus.CorpusIndexError):
            reader.read("structure/another.json")

    def test_a_checked_index_is_adopted_without_scanning_again(self):
        index = corpus.CorpusIndex(self.root)
        with patch.object(corpus, "_git_state", side_effect=AssertionError("scanned again")):
            reader = ReaderData(self.root, index)
            self.assertIs(reader.index, index)
            self.assertEqual(json.loads(reader.read("structure/one.json"))["text"], "Original whole source\n")

    def test_absence_and_traversal_do_not_generate_other_products(self):
        reader = ReaderData(self.root)
        self.assertIsNone(reader.read("structure/missing.json"))
        for name in ("../secrets.json", "/absolute.json", "structure//x.json", "x.txt"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                reader.read(name)
        self.assertEqual(self.calls, ["structure/missing.json"])


@unittest.skipUnless(shutil.which("node"), "Node is required for the actual browser bridge")
class IndexedBridgeTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.bodies = {
            "structure/rubrics/index.json": {"calendars": [], "advisory": "A reading — verified"},
            "structure/calendar/index.json": {"calendars": [], "span": {"first": 2020, "last": 2120}},
            "structure/propers/index.json": {"missals": [], "default": "roman-1962"},
            "bibles.json": {"bibles": []},
        }
        outer = self

        class Reader:
            def read(self, relative):
                outer.calls.append(relative)
                value = outer.bodies[relative]
                if isinstance(value, Exception):
                    raise value
                return json.dumps(value, ensure_ascii=False).encode()

        self.adopted = []

        @contextmanager
        def products(root, index=None):
            self.adopted.append(index)
            yield Reader()

        self.enterContext(patch.object(bridge, "indexed_products", products))
        self.client = bridge.Bridge()
        self.addCleanup(self.client.close)

    def test_real_model_requests_only_opening_records_and_restarts(self):
        result = self.client.call("liturgy", "opening")
        self.assertEqual(result["advisory"], "A reading — verified")
        self.assertEqual(set(self.calls), set(self.bodies))
        first = self.client.process
        self.client.close()
        self.assertIsNotNone(first.poll())
        self.assertFalse(self.client._data_pipes)
        self.assertEqual(self.client.call("liturgy", "opening"), result)
        self.assertIsNot(self.client.process, first)

    def test_large_unicode_payload_crosses_the_owned_pipe(self):
        text = "λόγος — " * 40000
        self.bodies["structure/rubrics/index.json"]["advisory"] = text
        self.assertEqual(self.client.call("liturgy", "opening")["advisory"], text)

    def test_index_failure_is_reported_without_a_missing_data_fallback(self):
        self.bodies["structure/rubrics/index.json"] = corpus.CorpusIndexError("changed canonical source")
        with self.assertRaisesRegex(Refused, "changed canonical source"):
            self.client.call("liturgy", "opening")

    def test_startup_check_opens_only_the_next_session(self):
        checked = object()
        self.client.adopt(checked)
        self.client.call("liturgy", "opening")
        self.client.close()
        self.client.call("liturgy", "opening")
        self.assertEqual(self.adopted, [checked, None])
        self.client.adopt(checked)
        self.client.close()
        self.client.call("liturgy", "opening")
        self.assertEqual(self.adopted, [checked, None, None])


if __name__ == "__main__":
    unittest.main()
