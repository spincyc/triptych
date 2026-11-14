"""The `qualified-public-domain` token: one scoped priority-6 basis, visibly marked.

The holding and limits live in the adopted rights record; the contract lives in
`scripts/_qualified_public_domain.py`. These tests hold every consumer to it:
an admitted text is published with its notice, and a text outside the record's
limits -- pre-1931, post-1975, a postconciliar target, a 1964-1977 notice, a
non-Vatican first publication -- is refused rather than quietly marked.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "scripts")]

import _proper_latin as L  # noqa: E402
import _qualified_public_domain as Q  # noqa: E402


def load_tool(name: str):
    loader = SourceFileLoader("qualified_pd_" + name.replace("-", "_"), str(ROOT / "tools" / name))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    sys.modules[spec.name] = module
    loader.exec_module(module)
    return module


CARRIER = "artifact.fixture.holy-see.qualified-carrier"
AAS_EDITION = "edition.fixture.holy-see.aas-47-1955"
AAS_SCAN = "artifact.fixture.holy-see.aas-47-1955.scan"
EDITION_2002 = "edition.catholic-church.missale-romanum.vatican-typica-tertia-2002"
TARGET_2002 = "artifact.catholic-church.missale-romanum.vatican-typica-tertia-2002.secondary-digital-pdf-0b458944"
TARGET_PASSAGE = "passage.catholic-church.missale-romanum.vatican-typica-tertia-2002.fixture-comparison"
PASSAGE = "passage.fixture.holy-see.aas-1955.collect"
BODY = "Oratio anni millesimi nongentesimi quinquagesimi quinti.\n"


def latin_row(**changes) -> dict:
    row = {
        "mass": "day", "form": "", "proper": "Collect", "course": "", "cycle": "",
        "occurrence": 1, "text_sha256": L.text_sha256(BODY),
        "provenance_status": "collated", "source_id": PASSAGE, "source_date": "1955",
        "locator": "AAS 47 (1955) p. 470", "relationship": "exact-transcription",
        "verification_source_id": PASSAGE, "verification_locator": "page image",
        "transformations": [], "provenance_evidence": "page-image collation fixture",
        "provenance_authority": "fixture", "provenance_confidence": "high",
        "publication_status": "permitted", "publication_basis": Q.BASIS,
        "surfaces": sorted(L.SURFACES), "publication_source_ids": [CARRIER],
        "publication_locator": Q.RECORD + " [admission]",
        "publication_evidence": "Holy See 1955 first publication; no US notice (fixture)",
        "publication_authority": Q.RECORD, "notice": Q.notice("latin"),
        "first_publication": "Acta Apostolicae Sedis 47 (1955)",
        "first_publication_year": 1955,
        "first_publication_imprint": "Acta Apostolicae Sedis",
        "first_publication_body": "Sacred Congregation of Rites",
        "us_formality": "published-abroad-without-us-notice",
    }
    row.update(changes)
    return row


def ledger(calendar: str, row: dict) -> str:
    lines = [f'schema = "{L.SCHEMA}"', f'calendar = "{calendar}"', 'language = "la"',
             f'policy = "{L.POLICY}"', "", "[defaults]",
             'provenance_status = "unresolved"', 'publication_status = "unresolved"',
             'publication_basis = "unresolved"', "surfaces = []", "", "[[entries]]"]
    for key, value in row.items():
        if isinstance(value, bool):
            raise TypeError(key)
        lines.append(f"{key} = {value}" if isinstance(value, int)
                     else f"{key} = {json.dumps(value, ensure_ascii=False)}")
    return "\n".join(lines) + "\n"


class AdoptedRecordTests(unittest.TestCase):
    def test_record_carries_the_maintainer_decision_and_the_machine_contract(self):
        record = tomllib.loads((ROOT / Q.RECORD).read_text(encoding="utf-8"))
        self.assertEqual("adopted", record["status"])
        self.assertEqual(Q.BASIS, record["basis_token"])
        self.assertEqual("medium-low", record["confidence"])
        self.assertEqual("2026-11-14", record["decision"]["decided_on"])
        self.assertEqual("if the italian copyright holds, apply it",
                         record["decision"]["instruction"])
        self.assertEqual([1931, 1975], record["admission"]["first_publication_years"])
        self.assertIn("postconciliar", record["admission"]["later_editions"]["target_calendars"])
        self.assertIn(EDITION_2002, record["admission"]["later_editions"]["target_editions"])
        self.assertFalse(record["payload_guard"]["contains_liturgical_payload"])
        for kind in Q.NOTICE_KINDS:
            text = Q.notice(kind)
            self.assertIn("priority 6", text)
            self.assertIn("medium-low", text)
            self.assertIn("Not adjudicated", text)

    def test_only_an_adopted_record_can_supply_the_contract(self):
        with self.assertRaises(Q.AdmissionError):
            Q.admission("src/sources/inventories/missale-romanum-1962-facsimile-rights-v1.toml")
        row = latin_row()
        with tempfile.TemporaryDirectory() as room:
            fake = Path(room) / Q.RECORD
            fake.parent.mkdir(parents=True)
            text = (ROOT / Q.RECORD).read_text(encoding="utf-8")
            fake.write_text(text.replace('status = "adopted"', 'status = "proposed"'),
                            encoding="utf-8")
            Q.admission.cache_clear()
            try:
                with mock.patch.object(Q, "TRUSTED_REPOSITORY", Path(room)):
                    with self.assertRaises(Q.AdmissionError):
                        Q.admission()
                    self.assertTrue(any("not an adopted" in one
                                        for one in Q.latin_row_problems(row)))
            finally:
                Q.admission.cache_clear()


class LatinProvenanceTests(unittest.TestCase):
    def test_admitted_row_validates_projects_and_permits_every_surface(self):
        row = latin_row()
        self.assertEqual([], L._row_problems("row", row))
        decision = L.decision_for(L.LatinKey("day", "", "Collect"), BODY,
                                  {L.LatinKey.from_mapping(row): row})
        self.assertTrue(decision.permits(L.SURFACES))
        publication = decision.projection(L.SURFACES)["publication"]
        self.assertEqual(Q.BASIS, publication["basis"])
        self.assertEqual(Q.notice("latin"), publication["notice"])
        self.assertEqual(Q.RECORD, publication["authority"])
        self.assertEqual(1955, publication["first_publication_year"])
        self.assertEqual("Sacred Congregation of Rites", publication["first_publication_body"])

    def test_limits_are_refused_not_marked(self):
        cases = (
            ({"first_publication_year": 1930}, "before 1931"),
            ({"first_publication_year": 1976}, "after 1975"),
            ({"first_publication_year": 2002}, "postconciliar 1976+"),
            ({"first_publication_year": "1955"}, "integer first_publication_year"),
            ({"first_publication_imprint": "Marietti"}, "first_publication_imprint"),
            ({"first_publication_body": "Benziger Brothers"}, "first_publication_body"),
            ({"first_publication_year": 1965, "us_formality": "us-notice-unrenewed"},
             "renewed automatically"),
            ({"us_formality": "unknown"}, "us_formality must be one of"),
            ({"notice": "Public domain."}, "verbatim Latin notice"),
            ({"notice": Q.notice("english_study")}, "verbatim Latin notice"),
            ({"publication_authority": "src/sources/inventories/other-rights-v1.toml"},
             "adopted rights record"),
            ({"first_publication": ""}, "first_publication naming"),
            ({"relationship": "collated-non-exact"}, "exact witness relationship"),
        )
        for changes, message in cases:
            with self.subTest(changes=changes):
                problems = L._row_problems("row", latin_row(**changes))
                self.assertTrue(any(message in one for one in problems), problems)
        missing = latin_row()
        del missing["us_formality"]
        self.assertTrue(any("us_formality" in one for one in L._row_problems("row", missing)))

    def test_only_the_token_declares_first_publication_fields(self):
        row = latin_row(publication_basis="public-domain")
        row.pop("notice"), row.pop("publication_authority")
        problems = L._row_problems("row", row)
        self.assertTrue(any("only a qualified-public-domain row declares" in one
                            for one in problems), problems)

    def test_sidecar_admits_1962_and_names_the_comparison_in_a_later_edition_calendar(self):
        with tempfile.TemporaryDirectory() as room:
            for calendar, row in (("roman-1962", latin_row()),
                                  ("postconciliar", latin_row(verification_source_id=TARGET_PASSAGE))):
                with self.subTest(calendar=calendar):
                    path = Path(room) / f"{calendar}{L.SIDECAR_SUFFIX}"
                    path.write_text(ledger(calendar, row), encoding="utf-8")
                    records, problems = L.read_sidecar(path)
                    self.assertEqual([], problems)
                    self.assertEqual(1, len(records))
        self.assertTrue(any("text-free comparison passage" in one for one in Q.calendar_problems(
            {k: v for k, v in latin_row().items() if k != "verification_source_id"}, "postconciliar")))

    def test_publication_sources_must_be_public_and_carry_the_token(self):
        def sources(rights):
            return {PASSAGE: {"record_type": "passage", "artifact_id": CARRIER},
                    CARRIER: {"record_type": "artifact", "rights_status": rights}}
        row = latin_row()
        self.assertEqual([], L._source_record_problems(
            "row", row, sources(Q.BASIS), authority_root=ROOT, effective_calendar="roman-1962"))
        for rights, message in (("public-domain", "with rights_status 'qualified-public-domain'"),
                                ("unresolved", "only ['public-domain'"),
                                ("restricted", "only ['public-domain'")):
            with self.subTest(rights=rights):
                problems = L._source_record_problems(
                    "row", row, sources(rights), authority_root=ROOT,
                    effective_calendar="roman-1962")
                self.assertTrue(any(message in one for one in problems), problems)

    def later_edition_graph(self):
        return copy.deepcopy({
            PASSAGE: {"record_type": "passage", "artifact_id": AAS_SCAN, "edition_id": AAS_EDITION},
            AAS_SCAN: {"record_type": "artifact", "rights_status": "restricted", "edition_id": AAS_EDITION},
            CARRIER: {"record_type": "artifact", "rights_status": Q.BASIS,
                      "edition_id": "edition.fixture.qualified-carrier", "projected_from": [AAS_SCAN]},
            TARGET_PASSAGE: {"record_type": "passage", "artifact_id": TARGET_2002, "edition_id": EDITION_2002},
            TARGET_2002: {"record_type": "artifact", "rights_status": "restricted", "edition_id": EDITION_2002},
        })

    def postconciliar_problems(self, row, sources):
        return (L._row_problems("row", row)
                + L._source_record_problems("row", row, sources, authority_root=ROOT,
                                            effective_calendar="postconciliar"))

    def test_postconciliar_slot_admits_unchanged_1955_wording_from_the_earlier_publication(self):
        row = latin_row(verification_source_id=TARGET_PASSAGE,
                        verification_locator="2002 p. 512, text-free comparison")
        self.assertEqual([], self.postconciliar_problems(row, self.later_edition_graph()))
        decision = L.decision_for(L.LatinKey("day", "", "Collect"), BODY,
                                  {L.LatinKey.from_mapping(row): row})
        self.assertTrue(decision.permits(L.SURFACES))
        self.assertEqual(1955, decision.projection(L.SURFACES)["publication"]["first_publication_year"])

    def test_postconciliar_refuses_later_missals_later_carriers_and_missing_comparison(self):
        base = latin_row(verification_source_id=TARGET_PASSAGE,
                         verification_locator="2002 p. 512, text-free comparison")
        cases = []
        cases.append(("1970 Missal first publication",
                      dict(base, first_publication="Missale Romanum, editio typica (1970)",
                           first_publication_year=1970, first_publication_imprint="Typis Polyglottis Vaticanis"),
                      None, "1970-or-later Missal edition"))
        cases.append(("1970 Missal named under a 1955 year",
                      dict(base, first_publication="Missale Romanum (Typis Polyglottis Vaticanis, 1970)"),
                      None, "1970-or-later Missal edition"))
        cases.append(("1965 printing with US notice",
                      dict(base, first_publication_year=1965, us_formality="us-notice-unrenewed"),
                      None, "renewed automatically"))
        graph = self.later_edition_graph()
        graph[TARGET_2002]["rights_status"] = Q.BASIS
        cases.append(("carrier is the 2002 artifact",
                      dict(base, publication_source_ids=[TARGET_2002]), graph,
                      "is or derives from a later typical edition"))
        graph = self.later_edition_graph()
        graph[CARRIER]["projected_from"] = [TARGET_2002]
        cases.append(("carrier projected from the 2002 artifact", base, graph,
                      "is or derives from a later typical edition"))
        cases.append(("source witness is the 2002 edition",
                      dict(base, source_id=TARGET_PASSAGE), None, "must witness the earlier"))
        cases.append(("comparison not on a target edition",
                      dict(base, verification_source_id=PASSAGE), None,
                      "comparison passage on its later typical edition"))
        graph = self.later_edition_graph()
        graph[TARGET_PASSAGE]["text"] = "verba"
        cases.append(("comparison carries words", base, graph, "text-free"))
        for label, row, graph, message in cases:
            with self.subTest(label=label):
                problems = self.postconciliar_problems(row, graph or self.later_edition_graph())
                self.assertTrue(any(message in one for one in problems), problems)
        # The edition rules bind in every calendar, not only the postconciliar one.
        graph = self.later_edition_graph()
        graph[TARGET_2002]["rights_status"] = Q.BASIS
        problems = L._source_record_problems(
            "row", dict(base, publication_source_ids=[TARGET_2002]), graph,
            authority_root=ROOT, effective_calendar="roman-1962")
        self.assertTrue(any("later typical edition" in one for one in problems), problems)


class TranslationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.propers = load_tool("mass-propers")
        cls.calendar = load_tool("check-calendar-masses")

    def english(self, **changes):
        entry = {"lang": "en", "rights": Q.BASIS, "source_id": "edition.fixture.us-missal-1957",
                 "text": "O God, who on this day...", "notice": Q.notice("english_carried")}
        entry.update(changes)
        return entry

    def test_carried_english_needs_its_source_and_verbatim_notice(self):
        self.assertEqual([], Q.translation_problems(self.english()))
        for changes, message in (({"notice": None}, "verbatim notice"),
                                 ({"notice": Q.notice("latin")}, "verbatim notice"),
                                 ({"source_id": None}, "source_id"),
                                 ({"lang": "de"}, "English only")):
            with self.subTest(changes=changes):
                entry = {k: v for k, v in self.english(**changes).items() if v is not None}
                self.assertTrue(any(message in one for one in Q.translation_problems(entry)))

    def test_mass_propers_ledger_and_public_projection(self):
        tool = self.propers
        tool.validate_translation_payload({"translations": [self.english()]}, Path("ledger"))
        self.assertTrue(tool.translation_is_publishable({"name": "Collect"}, self.english()))
        unmarked = self.english()
        del unmarked["notice"]
        with self.assertRaisesRegex(ValueError, "verbatim notice"):
            tool.validate_translation_payload({"translations": [unmarked]}, Path("ledger"))
        self.assertFalse(tool.translation_is_publishable({"name": "Collect"}, unmarked))

    def test_check_calendar_masses_requires_notice_and_registered_source(self):
        tool = self.calendar
        with mock.patch.object(tool, "source_ids", return_value=({"edition.fixture.us-missal-1957"}, None)):
            problems: list[str] = []
            tool.check_translation_list("p", [self.english()], problems, "Collect")
            self.assertEqual([], problems)
            unmarked = self.english()
            del unmarked["notice"]
            problems = []
            tool.check_translation_list("p", [unmarked], problems, "Collect")
            self.assertTrue(any("required notice" in one for one in problems), problems)
            self.assertTrue(any("verbatim notice" in one for one in problems), problems)

    def test_study_english_over_admitted_latin_is_visibly_qualified(self):
        study = {"lang": "en", "rights": "project-created", "text": "Grant, we pray..."}
        self.assertTrue(Q.study_translation_problems([study]))
        study["notice"] = Q.notice("english_study")
        self.assertEqual([], Q.study_translation_problems([study]))

    def test_public_latin_state_refuses_an_unmarked_qualified_body(self):
        tool = self.propers
        latin = {"text_sha256": "0" * 64, "withheld": False, "reason": None,
                 "provenance": {"status": "collated", "relationship": "exact-transcription"},
                 "publication": {"status": "permitted", "basis": Q.BASIS,
                                 "surfaces": sorted(L.SURFACES), "source_ids": [CARRIER],
                                 "notice": Q.notice("latin")}}
        self.assertEqual(latin, tool.public_latin_state(copy.deepcopy(latin), "Collect"))
        latin["publication"].pop("notice")
        with self.assertRaisesRegex(ValueError, "verbatim notice"):
            tool.public_latin_state(latin, "Collect")


class OrdinaryAndLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ordinary = load_tool("mass-ordinary")

    def witness(self, **changes):
        entry = {"id": "edition.fixture.ordo-1955", "lang": "la", "label": "fixture",
                 "rights": Q.BASIS, "acknowledgement": Q.notice("latin"),
                 "artifacts": [CARRIER]}
        entry.update(changes)
        return entry

    def test_ordinary_witness_carries_its_notice_and_matching_library_rights(self):
        tool = self.ordinary
        library = {CARRIER: {"rights_status": Q.BASIS}}
        held = tool.witness_table({"witnesses": [self.witness()]}, library, "fixture")
        self.assertEqual(Q.BASIS, held[("edition.fixture.ordo-1955", "la")]["rights"])
        for changes, library_rights, message in (
                ({"acknowledgement": None}, Q.BASIS, "acknowledgement"),
                ({"acknowledgement": Q.notice("english_carried")}, Q.BASIS, "acknowledgement"),
                ({"lang": "fr"}, Q.BASIS, "Latin and English only"),
                ({}, "public-domain", "recorded as 'public-domain'"),
                ({}, "unresolved", "recorded as 'unresolved'")):
            with self.subTest(changes=changes, library=library_rights):
                entry = {k: v for k, v in self.witness(**changes).items() if v is not None}
                with self.assertRaisesRegex(tool.SourceError, message):
                    tool.witness_table({"witnesses": [entry]},
                                       {CARRIER: {"rights_status": library_rights}}, "fixture")

    def test_source_library_artifact_cites_the_record_and_its_notice(self):
        artifact = {"rights_status": Q.BASIS, "rights_jurisdiction": "United States",
                    "rights_basis": f"{Q.notice('latin')} See {Q.RECORD}."}
        self.assertEqual([], Q.artifact_problems(artifact))
        for changes in ({"rights_jurisdiction": "Italy"},
                        {"rights_basis": "Public domain in the United States."},
                        {"rights_basis": f"See {Q.RECORD}."}):
            with self.subTest(changes=changes):
                self.assertTrue(Q.artifact_problems(dict(artifact, **changes)))
        self.assertEqual([], Q.artifact_problems({"rights_status": "public-domain"}))


BROWSER_HARNESS = r"""
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = process.argv[1];
const notice = process.argv[2];
const dom = require(path.join(root, 'scripts/lectern/dom.js'));
Object.assign(globalThis, {document: dom.document, window: globalThis,
  location: {search: '', hash: '', pathname: '/'},
  history: {replaceState() {}, pushState() {}}, addEventListener() {}});
vm.runInThisContext(fs.readFileSync(path.join(root,
  'src/web/browser/shared/browser-core.js'), 'utf8'));
const T = Triptych;
const flat = node => dom.read(node).map(block => block.runs.map(run => run.text).join('')).join('\n');
const owner = () => ({name: 'Collect', source: 'composed', text: 'Oratio anni MCMLV.',
  latin: {text_sha256: '0'.repeat(64), withheld: false, reason: null,
    provenance: {status: 'collated', relationship: 'exact-transcription'},
    publication: {status: 'permitted', basis: 'qualified-public-domain', notice,
      first_publication: 'Acta Apostolicae Sedis 47 (1955)',
      first_publication_body: 'Sacred Congregation of Rites'}},
  translations: []});
"""


class BrowserPresentationTests(unittest.TestCase):
    def run_case(self, source):
        result = subprocess.run(
            ["/usr/bin/node", "-e", BROWSER_HARNESS + source, str(ROOT), Q.notice("latin")],
            text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_latin_shows_its_notice_and_first_publication_beside_the_words(self):
        self.run_case(r"""
const node = T.renderProper(owner(), {}, null, {orations: 'la'});
const mark = node.querySelector('.latin-rights-qualification');
assert.equal(mark.textContent, notice);
assert.equal(mark.getAttribute('data-publication-basis'), 'qualified-public-domain');
assert.ok(flat(node).includes('Oratio anni MCMLV.'));
assert.ok(flat(node).includes('First published: Acta Apostolicae Sedis 47 (1955) · Sacred Congregation of Rites'));
""")

    def test_unmarked_qualified_latin_or_english_fails_closed(self):
        self.run_case(r"""
const bare = owner();
delete bare.latin.publication.notice;
assert.throws(() => T.renderProper(bare, {}, null, {orations: 'la'}), /lacks its rights notice/);
assert.throws(() => T.translationCredits({rights: 'qualified-public-domain', text: 'x', lang: 'en'}),
  /lacks its rights notice/);
const withheld = owner();
withheld.latin.withheld = true;
assert.equal(T.renderProper(withheld, {}, null, {orations: 'la'}).querySelector('.latin-rights-qualification'), null);
""")


class FiniteScopeKeyTests(unittest.TestCase):
    """A general-token row is not claimed by a calendar-less finite key."""

    def test_postconciliar_row_sharing_a_roman_finite_key_is_not_claimed(self):
        import _proper_qualified_latin as PQ
        row = latin_row(mass="good-friday", proper="Improperia")
        self.assertTrue(PQ.finite_20261029.claims_row(row))
        self.assertFalse(PQ._finite_20261029_claims(row))
        self.assertEqual([], PQ.row_problems(row))

    def test_a_row_reusing_a_finite_carrier_is_still_claimed(self):
        import _proper_qualified_latin as PQ
        carrier = ("artifact.triptych.roman-1962-latin-proper-editorial-projection."
                   "editorial-projection-2026-10-29.improperia-whole-qualified-83cbd703")
        row = latin_row(mass="good-friday", proper="Improperia",
                        publication_source_ids=[CARRIER, carrier])
        self.assertTrue(PQ._finite_20261029_claims(row))
        self.assertTrue(PQ.row_problems(row))


if __name__ == "__main__":
    unittest.main()
