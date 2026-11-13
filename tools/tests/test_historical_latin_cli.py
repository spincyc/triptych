"""Historical Latin source qualifications travel through both reading CLIs."""
from __future__ import annotations

from contextlib import redirect_stdout
import copy
import hashlib
import importlib.machinery
import importlib.util
import io
from pathlib import Path
import sys
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _calendars  # noqa: E402


def load_tool(name: str):
    loader = importlib.machinery.SourceFileLoader(
        "historical_latin_" + name.replace("-", "_"), str(ROOT / "tools" / name)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


# Consumer projections of the independently reviewed Pange source admission.
# The actual Latin is read from its retained artifact, not repeated as a fixture.
SOURCE = (
    ROOT / "src/sources/works/prosper-gueranger/the-liturgical-year/editions/"
    "english-duffy-1879-volume-10/artifacts/"
    "pange-lingua-latin-checked-20261029-15c03ec1/latin.txt"
)
PASSAGE = (
    "passage.prosper-gueranger.the-liturgical-year."
    "english-duffy-1879-volume-10."
)
QUALIFICATION = (
    "Historical Latin of the named hymn option, transcribed from the 1879 Duffy "
    "witness; paired with the existing 1946 Lasance historical English. "
    "The secondary 2002 source names the option and stage but prints no complete "
    "hymn body. Exact 2008 wording and appointment remain uncollated. "
)
CASES = (
    (
        "Hymn at the Transfer of the Blessed Sacrament", 1, 27,
        "5849cc72f72aef91b897e11d20712b4f617b94df698f5e43b99b50826e8d34aa",
        "pange-transfer-four-stanzas-20261112",
        "First four stanzas only; no Amen. The source permits another Eucharistic chant.",
    ),
    (
        "Chant at the Place of Reposition", 29, 42,
        "14e54ab240d4d1cdadb55b7fa21fa8fb22b67fcd70d15d3c54fc5528e6085905",
        "pange-reposition-two-stanzas-20261112",
        "Final two stanzas with Amen. Taking Genitori after Tantum ergo is the "
        "independently identified historical closing-section interpretation, not "
        "an explicit two-stanza prescription at n.39. Another Eucharistic chant "
        "remains permitted.",
    ),
)


class HistoricalLatinCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.propers = load_tool("mass-propers")
        cls.today = load_tool("mass-today")
        cls.lines = SOURCE.read_text().splitlines()
        with (ROOT / "src/sources/inventories/postconciliar-proper-translations-v1.toml").open("rb") as stream:
            cls.english = tomllib.load(stream)["entries"]

    def fixtures(self):
        for name, first, last, digest, passage, ending in CASES:
            text = "\n".join(self.lines[first - 1:last])
            self.assertEqual(hashlib.sha256(text.encode()).hexdigest(), digest)
            english = next(row for row in self.english
                           if row["mass"] == "mass-of-the-lords-supper"
                           and row["proper"] == name)
            yield {
                "name": name, "source": "composed", "text": text,
                "notes": QUALIFICATION + ending,
                "translations": copy.deepcopy(english["translations"]),
                "latin": {
                    "text_sha256": digest, "withheld": False,
                    "provenance": {
                        "status": "collated", "relationship": "exact-transcription",
                        "source_id": PASSAGE + passage, "source_date": "1879",
                    },
                    "publication": {"status": "permitted", "basis": "public-domain"},
                    "note": QUALIFICATION + ending,
                },
            }

    def test_direct_latin_and_fallback_keep_the_source_qualification(self):
        for proper in self.fixtures():
            before = copy.deepcopy(proper)
            note = proper["latin"]["note"]
            for select in (_calendars.texts_of, self.propers.select_texts):
                with self.subTest(proper=proper["name"], selector=select.__name__):
                    self.assertEqual(select(proper, "la"),
                                     [(proper["text"], "Latin source: 1879", note)])
                    self.assertEqual(select(proper, "fr"), [(
                        proper["text"], "Latin source: 1879",
                        "no fr translation recorded; showing Latin. " + note,
                    )])
            self.assertEqual(proper, before)

    def test_both_reading_consumers_print_the_qualification_beside_latin(self):
        for proper in self.fixtures():
            for lang in ("la", "fr"):
                with self.subTest(proper=proper["name"], lang=lang):
                    daily = "\n".join(self.today.proper_lines(
                        proper, self.today.Style(), "", lang=lang,
                        witness=None, seat=None, why=False,
                    ))
                    captured = io.StringIO()
                    payload = {"mass": {"name": "Mass of the Lord's Supper", "propers": [proper]}}
                    with redirect_stdout(captured):
                        self.propers.render_reading(payload, lang, {})
                    for output in (daily, captured.getvalue()):
                        self.assertIn("Latin source: 1879", output)
                        self.assertIn(proper["latin"]["note"], output)
                        self.assertIn(proper["text"].splitlines()[0], output)
                        self.assertNotIn("The Latin original is shown", output)

    def test_english_selection_is_unchanged_and_does_not_inherit_latin_note(self):
        for proper in self.fixtures():
            translation = proper["translations"][0]
            self.assertEqual(_calendars.texts_of(proper, "en"), [(translation["text"], "", "")])
            self.assertEqual(self.propers.select_texts(proper, "en"), [(
                translation["text"], translation["source_id"], "",
            )])

    def test_english_caution_reaches_daily_reader_verbatim(self):
        proper = next(self.fixtures())
        translation = proper["translations"][0]
        caution = "Historical study English.\n\nExact target wording remains uncollated."
        translation["caution"] = caution
        before = copy.deepcopy(proper)
        self.assertEqual(_calendars.texts_of(proper, "en"), [(
            translation["text"], "", caution,
        )])
        daily = "\n".join(self.today.proper_lines(
            proper, self.today.Style(), "", lang="en",
            witness=None, seat=None, why=False,
        ))
        for paragraph in caution.split("\n\n"):
            self.assertIn(paragraph, daily)
        self.assertEqual(proper, before)

    def test_each_selected_witness_keeps_its_own_caution_and_attribution(self):
        proper = {"translations": [
            {"lang": "en", "text": "First prayer.", "source_id": "first",
             "caution": "First source qualification."},
            {"lang": "en", "text": "Second prayer.", "source_id": "second",
             "caution": "Second source qualification."},
        ]}
        self.assertEqual(_calendars.texts_of(proper, "en"), [
            ("First prayer.", "first", "First source qualification."),
            ("Second prayer.", "second", "Second source qualification."),
        ])
        self.assertEqual(_calendars.texts_of(proper, "en", "second"), [
            ("Second prayer.", "", "Second source qualification."),
        ])

    def test_missing_or_nonstring_caution_adds_no_note(self):
        proper = next(self.fixtures())
        translation = proper["translations"][0]
        for value in (None, False, 7, [], {"text": "Not a string"}):
            with self.subTest(value=value):
                translation["caution"] = value
                self.assertEqual(_calendars.texts_of(proper, "en"), [
                    (translation["text"], "", ""),
                ])
        del translation["caution"]
        self.assertEqual(_calendars.texts_of(proper, "en"), [
            (translation["text"], "", ""),
        ])

    def test_note_and_source_id_fallbacks_preserve_existing_qualification(self):
        proper = next(self.fixtures())
        del proper["latin"]["note"]
        del proper["latin"]["provenance"]["source_date"]
        selected = _calendars.texts_of(proper, "la")[0]
        self.assertEqual(selected[1], "Latin source: " + proper["latin"]["provenance"]["source_id"])
        self.assertEqual(selected[2], proper["notes"])
        proper["untranslated"] = [{"lang": "fr", "state": "unavailable"}]
        selected = _calendars.texts_of(proper, "fr")[0]
        self.assertEqual(selected[2],
                         "no fr recorded, deliberately; see the untranslated ledger. " + proper["notes"])

    def test_plain_exact_target_and_scripture_metadata_do_not_add_noise(self):
        proper = next(self.fixtures())
        plain = {"source": "composed", "text": proper["text"], "notes": "General apparatus."}
        target = copy.deepcopy(proper)
        target["latin"]["provenance"]["relationship"] = "editorial-projection-exact-to-target"
        no_note = copy.deepcopy(proper)
        del no_note["latin"]["note"]
        del no_note["notes"]
        for owner in (plain, target, no_note):
            with self.subTest(owner=owner.get("latin", {}).get("provenance")):
                self.assertEqual(_calendars.texts_of(owner, "la"), [(owner["text"], "", "")])
                self.assertEqual(_calendars.texts_of(owner, "fr"), [(
                    owner["text"], "", "no fr translation recorded; showing Latin",
                )])
        scripture = {"source": "scripture", "verses": [{"ref": "Psalm 25:1-3"}],
                     "notes": "Source apparatus", "latin": proper["latin"]}
        self.assertEqual(_calendars.texts_of(scripture, "la"), [("", "", "")])
        self.assertEqual(_calendars.texts_of(scripture, "fr"), [])

    def test_unpublished_or_uncollated_metadata_cannot_supply_the_credit(self):
        for path, value in (
            (("withheld",), True),
            (("state",), "unavailable"),
            (("publication", "status"), "withheld"),
            (("provenance", "status"), "identified"),
            (("provenance", "relationship"), "non-exact-historical-witness"),
        ):
            proper = next(self.fixtures())
            owner = proper["latin"]
            for part in path[:-1]:
                owner = owner[part]
            owner[path[-1]] = value
            with self.subTest(path=path, value=value):
                # Body permission stays with the existing producer gates; this
                # presentation helper supplies no source credit to invalid data.
                self.assertEqual(_calendars.texts_of(proper, "la")[0][1:], ("", ""))


if __name__ == "__main__":
    unittest.main()
