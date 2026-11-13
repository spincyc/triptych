"""Thin discovery and bounded reading keep bodies and authority in their owners."""
from contextlib import contextmanager, nullcontext
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _reader_products as reader
import _proper_latin as latin
import _calendars


class Index:
    def __init__(self, files):
        self.files = files
        self.reads = []

    def read(self, path):
        self.reads.append(path)
        return self.files[path]

    @contextmanager
    def verified_reads(self):
        yield {}


class ReaderProductTests(unittest.TestCase):
    def fixture(self):
        mass = {"key": "advent-1", "name": "Advent I", "kind": "seasonal",
                "propers": [{"name": "Collect", "latin": {"text": "source body"}}],
                "forms": [{"id": "main", "name": "Mass", "ordinal": 1,
                           "ordinary_frame": {"kind": "full"},
                           "propers": [{"name": "Collect", "text": "source body"}]}]}
        structure = {"schema": "triptych-propers-structure/v1", "calendar": "roman-1962",
                     "translations": [{"lang": "en", "source_id": "witness"}], "masses": [mass]}
        body = reader._json(reader._skeleton(structure))
        index = Index({"src/index/propers/roman-1962.json": body,
                       reader.MANIFESTS: reader._json({"bibles.json": {"bibles": [{"id": "offered"}]}})})
        return mass, structure, index

    def test_discovery_omits_reading_bodies_and_preserves_form_identity(self):
        mass, structure, index = self.fixture()
        result = json.loads(reader.resolve("structure/propers/roman-1962.json", ROOT, index))
        self.assertNotIn("source body", json.dumps(result))
        self.assertEqual(result["masses"][0]["forms"], [{"id": "main", "name": "Mass", "ordinal": 1,
                                                       "ordinary_frame": {"kind": "full"}}])
        self.assertEqual(result["generation"], hashlib.sha256(index.files[index.reads[0]]).hexdigest())
        self.assertEqual(result["translations"], structure["translations"])
        self.assertIn("propers", mass)  # No mutation of the producer's object.
        self.assertEqual(reader.resolve("structure/propers/reader/roman-1962.json", ROOT, index),
                         reader.resolve("structure/propers/roman-1962.json", ROOT, index))

    def test_split_payloads_keep_exact_masses_for_every_calendar(self):
        mass, structure, _ = self.fixture()
        owner = reader._tool("mass-propers")
        for calendar in ("roman-1962", "roman-pre-1955", "postconciliar"):
            selected = dict(structure, calendar=calendar)
            thin = owner.reader_structure(selected)
            generation = hashlib.sha256(reader._json(thin)).hexdigest()
            catalog, payloads = owner.read_payloads(selected, generation)
            self.assertEqual(payloads[mass["key"]]["mass"], mass)
            self.assertEqual(payloads[mass["key"]]["generation"], generation)
            self.assertEqual(catalog["calendar"], calendar)
            self.assertEqual(thin["masses"][0]["payload"],
                             f"structure/propers/mass/{calendar}/{mass['key']}.json")

    def test_mass_calls_only_selected_shared_projection_with_global_witness_order(self):
        mass, structure, index = self.fixture()
        owner = SimpleNamespace(READ_MASS_SCHEMA="triptych-propers-read-mass/v1",
                                book_tokens=Mock(return_value={"Genesis": "Gen"}),
                                calendar_structure=Mock(return_value={"masses": [mass]}))
        with patch.object(reader, "_tool", return_value=owner), \
                patch("_reader_bibles.bible_context", return_value=nullcontext()):
            body = reader.resolve("structure/propers/mass/roman-1962/advent-1.json", ROOT, index)
        self.assertEqual(json.loads(body)["mass"], mass)
        owner.calendar_structure.assert_called_once_with(
            ROOT / "src/sources/calendars", "roman-1962", {"Genesis": "Gen"},
            mass_keys={"advent-1"}, translation_order=structure["translations"])

    def test_unknown_mass_refuses_before_any_body_projection(self):
        _, _, index = self.fixture()
        owner = SimpleNamespace(calendar_structure=Mock())
        with patch.object(reader, "_tool", return_value=owner):
            with self.assertRaisesRegex(ValueError, "not in the reader index"):
                reader.resolve("structure/propers/mass/roman-1962/unknown.json", ROOT, index)
        owner.calendar_structure.assert_not_called()

    def test_chapters_require_offered_membership_and_read_only_exact_file(self):
        _, _, index = self.fixture()
        path = "src/sources/bibles/offered/chapters/Gen/1.json"
        index.files[path] = b'{"verses":{"1":"held"}}'
        self.assertEqual(reader.resolve("offered/chapters/Gen/1.json", ROOT, index), index.files[path])
        self.assertEqual(index.reads, [reader.MANIFESTS, path])
        with self.assertRaisesRegex(ValueError, "not offered"):
            reader.resolve("withheld/chapters/Gen/1.json", ROOT, index)
        self.assertNotIn("src/sources/bibles/withheld/chapters/Gen/1.json", index.reads)

    def test_unsafe_routes_are_never_joined_to_canonical_paths(self):
        index = Index({})
        for route in ("../outside", "/absolute", "a//b", "a/./b", "a\\b", "a\0b"):
            with self.subTest(route=route), self.assertRaises(ValueError):
                reader.resolve(route, ROOT, index)
        self.assertEqual(index.reads, [])

    def test_lazy_records_context_does_not_leak_or_load_the_whole_graph(self):
        held = {"artifact.sample": {"id": "artifact.sample"}}
        with patch.object(latin, "_source_library_cache_entry", side_effect=AssertionError("full scan")):
            with latin.reading_records(held):
                actual, problems = latin._source_library_records(ROOT / "src/sources/calendars")
                self.assertIs(actual, held)
                self.assertEqual(problems, [])
        self.assertIsNone(latin._READING_RECORDS.get())

    def test_verified_parse_cache_reads_each_time_and_never_shares_mutable_results(self):
        source = SimpleNamespace(read_bytes=Mock(side_effect=[b'{"v":[1]}', b'{"v":[1]}', b'{"v":[2]}']))
        parse = Mock(side_effect=json.loads)
        with _calendars.verified_parse_cache({}):
            first = _calendars._cached_parse(source, "json", parse)
            first["v"].append("caller change")
            self.assertEqual(_calendars._cached_parse(source, "json", parse), {"v": [1]})
            self.assertEqual(_calendars._cached_parse(source, "json", parse), {"v": [2]})
        self.assertEqual(source.read_bytes.call_count, 3)
        self.assertEqual(parse.call_count, 2)


if __name__ == "__main__":
    unittest.main()
