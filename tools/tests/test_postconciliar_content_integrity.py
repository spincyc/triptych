"""Corpus-level truthfulness checks for the postconciliar Missal state.

The postconciliar index is intentionally incomplete.  These checks do not turn
that fact into an invented completeness target: they hold the distinction
between text the project has, a Missal heading that points to a Common, and a
formulary whose structure has not yet been established from an admissible
witness.  Evidence-backed work may fill any gap without changing a count here;
what may not return is pseudo-text named ``Placeholder`` where the source
already supports a typed structural absence.
"""

from __future__ import annotations

import hashlib
import re
import sys
import tomllib
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src" / "sources" / "calendars"
PLACEHOLDER_TEXT = (
    "This entry is a placeholder pending formula migration and source verification."
)
COMMON_POINTER_SOURCE = (
    "artifact.catholic-church.missale-romanum.2010-english-icel-antiphonary."
    "antiphonary-pdf"
)
COMMON_HEADING_MASSES = {
    "our-lady-fatima",
    "our-lady-guadalupe",
    "saint-adalbert-bishop-martyr",
    "saint-catherine-alexandria-virgin-martyr",
    "saint-juan-diego-cuauhtlatoatzin",
    "saint-josephine-bakhita-virgin",
    "saint-louis-grignion-montfort-priest",
    "saint-peter-julian-eymard-priest",
    "saint-pius-pietrelcina-priest",
    "saint-rita-cascia-religious",
    "saint-sharbel-makhluf-priest",
    "saint-teresa-benedicta-cross-virgin-martyr",
    "saints-lawrence-ruiz-companions-martyrs",
    "saints-augustine-zhao-rong-priest-companions",
    "saints-christopher-magallanes-priest-companions-martyrs",
}
TRACKED_EVIDENCE = re.compile(
    r"src/sources/inventories/[A-Za-z0-9][A-Za-z0-9._-]*\.(?:md|toml)"
)
ORDINARY_INVENTORY = (
    ROOT / "src" / "sources" / "inventories" / "postconciliar-ordo-missae-v1.toml"
)
TRANSLATION_INVENTORY = (
    ROOT
    / "src"
    / "sources"
    / "inventories"
    / "postconciliar-proper-translations-v1.toml"
)
FORBIDDEN_COLLECT_SNIPPET_DIGESTS = {
    67: {"3fcad3a774378ec8fbc071c25be23935f93dd96cd4c60a1a8c27812f761dbf32"},
    68: {"e52d7fee49d6b4dea48d800d3a45312d9c9e36001f8ae4b3b9d0233fe6895358"},
    73: {"8551f0822cebcd4e74416579e1d0785189b3b9082871d5fe0ba1bd7f6d841d47"},
}
TEXT_FREE_REMOTE_COLLECT_NOTES = {
    "saint-john-xxiii-pope",
    "saint-john-paul-ii-pope",
    "saint-paul-vi-pope",
    "saint-maximilian-mary-kolbe-priest-martyr",
    "saint-teresa-calcutta-virgin",
    "saints-andrew-kim-tae-gon-priest",
    "saint-faustina-kowalska-virgin",
    "saints-andrew-dung-lac-priest-companions",
}

sys.path.insert(0, str(ROOT / "scripts"))

import _calendars  # noqa: E402


def load_tool(name: str):
    path = ROOT / "tools" / name
    loader = SourceFileLoader(f"_postconciliar_{name.replace('-', '_')}", str(path))
    spec = spec_from_loader(loader.name, loader)
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


propers_tool = load_tool("mass-propers")


def masses(document: dict):
    for section_name, body in (document.get("sections") or {}).items():
        if not isinstance(body, dict):
            continue
        for mass in body.get("masses") or []:
            if isinstance(mass, dict):
                yield section_name, body, mass


def direct_propers(mass: dict):
    for proper in mass.get("propers") or []:
        if isinstance(proper, dict):
            yield "", proper
    for form in mass.get("forms") or []:
        if not isinstance(form, dict):
            continue
        form_name = str(form.get("name") or "")
        for proper in form.get("propers") or []:
            if isinstance(proper, dict):
                yield form_name, proper


class PostconciliarContentIntegrityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = _calendars.load_document(
            CALENDARS, "postconciliar", effective=False
        )
        cls.rows = list(masses(cls.document))
        cls.ordinary = tomllib.loads(ORDINARY_INVENTORY.read_text(encoding="utf-8"))
        cls.translations = tomllib.loads(
            TRANSLATION_INVENTORY.read_text(encoding="utf-8")
        )

    def test_seven_commons_are_typed_unavailable_formularies_not_pseudo_text(self):
        """The acquired sevenfold heading is known; its formularies are not."""
        commons = [
            mass
            for section_name, body, mass in self.rows
            if section_name == "common" or body.get("kind") == "common"
        ]
        self.assertEqual(len(commons), 7)

        expected_status = {
            "state": "unavailable",
            "scope": "missal-formulary",
            "reasons": [
                {
                    "kind": "no-exemplar",
                }
            ],
        }
        for mass in commons:
            key = str(mass.get("key") or "")
            self.assertTrue(key, mass)
            self.assertEqual(mass.get("text_status"), expected_status, key)
            self.assertEqual(list(direct_propers(mass)), [], key)
            self.assertNotIn("common_from", mass, key)

    def test_every_common_heading_points_to_a_typed_common(self):
        """A Missal heading is a source-backed choice, not a dangling string."""
        common_keys = {
            str(mass["key"])
            for section_name, body, mass in self.rows
            if section_name == "common" or body.get("kind") == "common"
        }
        by_key = {str(mass.get("key") or ""): mass for _, _, mass in self.rows}
        self.assertLessEqual(COMMON_HEADING_MASSES, set(by_key))
        references = []
        for _, _, mass in self.rows:
            pointer = mass.get("common_from")
            if pointer is None:
                continue
            references.append((mass, pointer))

        self.assertTrue(references, "the calendar records no Missal Common headings")
        self.assertEqual(
            {str(mass.get("key") or "") for mass, _ in references},
            COMMON_HEADING_MASSES,
        )
        for mass, pointer in references:
            key = str(mass.get("key") or "")
            self.assertEqual(list(direct_propers(mass)), [], key)
            self.assertEqual(
                mass.get("text_status"),
                {
                    "state": "unavailable",
                    "scope": "proper-collect",
                    "reasons": [
                        {
                            "kind": "no-exemplar",
                        }
                    ],
                },
                key,
            )
            self.assertIsInstance(pointer, dict, key)
            self.assertEqual(pointer.get("scope"), "missal-propers-except-collect", key)
            self.assertEqual(pointer.get("source_id"), COMMON_POINTER_SOURCE, key)
            self.assertTrue(str(pointer.get("locus") or "").strip(), key)

            options = pointer.get("options")
            self.assertIsInstance(options, list, key)
            self.assertTrue(options, key)
            for option in options:
                self.assertIsInstance(option, dict, key)
                self.assertLessEqual(set(option), {"mass", "selection"}, (key, option))
                self.assertIn(str(option.get("mass") or ""), common_keys, (key, option))
                if "selection" in option:
                    self.assertTrue(str(option["selection"]).strip(), (key, option))

    def test_august_seventh_has_two_source_distinct_memorial_candidates(self):
        """OLM nn. 615-616 must never collapse into a joined title or Mass forms."""
        by_key = {str(mass.get("key") or ""): mass for _, _, mass in self.rows}
        expected = {
            "saints-sixtus-ii-pope-companions-martyrs": {
                "name": "Saints Sixtus II, Pope, and Companions, Martyrs",
                "registry": "pc-08-07",
                "locus": "n. 615",
                "refs": {
                    "First Reading": "Wisdom 3:1-9",
                    "Responsorial Psalm": "Psalm 126:1-2ab, 2cd-3, 4-5, 6",
                    "Gospel Acclamation": "James 1:12",
                    "Gospel": "Matthew 10:28-33",
                },
            },
            "saint-cajetan-priest": {
                "name": "Saint Cajetan, Priest",
                "registry": "pc-08-07-cajetan",
                "locus": "n. 616",
                "refs": {
                    "First Reading": "Sirach 2:7-13",
                    "Responsorial Psalm": "Psalm 112:1-2, 3-4, 5-7a, 7b-8, 9",
                    "Gospel Acclamation": "Matthew 5:3",
                    "Gospel": "Luke 12:32-34",
                },
            },
        }

        registries = [
            str(mass.get("registry") or "") for _, _, mass in self.rows
        ]
        self.assertEqual(len(registries), len(set(registries)))
        for key, wanted in expected.items():
            mass = by_key[key]
            self.assertEqual(mass.get("name"), wanted["name"], key)
            self.assertEqual(mass.get("registry"), wanted["registry"], key)
            self.assertEqual(mass.get("date"), "08-07", key)
            self.assertEqual(mass.get("rank"), "Optional memorial", key)
            self.assertEqual(mass.get("kind"), "sanctoral", key)
            self.assertNotIn("forms", mass, key)
            notes = str(mass.get("notes") or "")
            self.assertIn("artifact page 354, printed page 300", notes, key)
            self.assertIn(wanted["locus"], notes, key)
            self.assertIn("no Lectionary text is reproduced", notes, key)

            refs = {}
            for _, proper in direct_propers(mass):
                verses = proper.get("verses")
                if verses:
                    self.assertEqual(proper.get("source"), "scripture", (key, proper))
                    self.assertEqual(len(verses), 1, (key, proper))
                    refs[str(proper.get("name") or "")] = verses[0].get("ref")
            self.assertEqual(refs, wanted["refs"], key)

    def test_same_date_optional_memorials_have_distinct_mass_identities(self):
        """Calendar alternatives are choices, never forms of one celebration."""
        expected = {
            "01-20": ["saint-fabian-pope-martyr", "saint-sebastian-martyr"],
            "02-03": ["saint-blaise-bishop-martyr", "saint-ansgar-bishop"],
            "02-08": ["saint-jerome-emiliani", "saint-josephine-bakhita-virgin"],
            "04-23": ["saint-george-martyr", "saint-adalbert-bishop-martyr"],
            "04-28": ["saint-peter-chanel-priest-martyr", "saint-louis-grignion-montfort-priest"],
            "05-12": ["saints-nereus-achilleus-martyrs", "saint-pancras-martyr"],
            "05-25": ["saint-bede-venerable-priest-doctor-church", "saint-gregory-vii-pope", "saint-mary-magdalene-pazzi-virgin"],
            "06-22": ["saint-paulinus-nola-bishop", "saints-john-fisher-bishop-thomas-more"],
            "08-02": ["saint-eusebius-vercelli-bishop", "saint-peter-julian-eymard-priest"],
            "08-25": ["saint-louis", "saint-joseph-calasanz-priest"],
            "09-17": ["saint-robert-bellarmine-bishop-doctor-church", "saint-hildegard-bingen-virgin-doctor-church"],
            "09-28": ["saint-wenceslaus-martyr", "saints-lawrence-ruiz-companions-martyrs"],
            "10-09": ["saints-denis-bishop-companions-martyrs", "saint-john-leonardi-priest", "saint-john-henry-newman-priest-doctor"],
            "10-16": ["saint-hedwig-religious", "saint-margaret-mary-alacoque-virgin"],
            "10-19": ["saints-john-brebeuf-isaac-jogues-priests", "saint-paul-cross-priest"],
            "11-16": ["saint-margaret-scotland", "saint-gertrude-virgin"],
            "11-23": ["saint-clement-i-pope-martyr", "saint-columban-abbot"],
        }
        by_date: dict[str, list[dict]] = {}
        for _, _, mass in self.rows:
            by_date.setdefault(str(mass.get("date") or ""), []).append(mass)

        registries = []
        for date, keys in expected.items():
            rows = [mass for mass in by_date[date] if mass["key"] in keys]
            self.assertEqual([mass["key"] for mass in rows], keys, date)
            self.assertTrue(all(mass["rank"] == "Optional memorial" for mass in rows))
            self.assertTrue(all(";" not in mass["name"] for mass in rows))
            self.assertTrue(all("forms" not in mass for mass in rows))
            registries.extend(mass["registry"] for mass in rows)
        self.assertEqual(len(registries), 36)
        self.assertEqual(len(set(registries)), 36)
        self.assertFalse(
            any(mass.get("rank") == "Optional memorials" for _, _, mass in self.rows)
        )

    def test_remote_collect_notes_retain_no_exact_english_snippet(self):
        """A reviewed remote formulary is not a stored or publishable exemplar."""
        by_key = {str(mass.get("key") or ""): mass for _, _, mass in self.rows}
        canonical_absence = (
            "No authoritative English exemplar is retained for this Collect; "
            "no English wording is carried or published from this source record."
        )
        for key in TEXT_FREE_REMOTE_COLLECT_NOTES:
            notes = str(by_key[key].get("notes") or "")
            self.assertIn(canonical_absence, notes, key)
            folded = notes.casefold()
            for contradictory in (
                "publishable",
                "may be published",
                "not landed",
                "nothing is landed",
                "unlandable",
            ):
                self.assertNotIn(contradictory, folded, (key, contradictory))
            self.assertNotRegex(notes, r"(?i)proper Collect\s*\(", key)

            for length, forbidden in FORBIDDEN_COLLECT_SNIPPET_DIGESTS.items():
                observed = {
                    hashlib.sha256(notes[start : start + length].encode()).hexdigest()
                    for start in range(max(0, len(notes) - length + 1))
                }
                self.assertTrue(observed.isdisjoint(forbidden), key)

    def test_any_surviving_placeholder_is_bound_to_tracked_gap_evidence(self):
        """A source gap may survive, but generic filler may not explain itself."""
        for _, _, mass in self.rows:
            placeholders = [
                proper
                for _, proper in direct_propers(mass)
                if proper.get("name") == "Placeholder"
            ]
            if not placeholders:
                continue

            key = str(mass.get("key") or "")
            self.assertEqual(len(placeholders), 1, key)
            self.assertEqual(sum(1 for _ in direct_propers(mass)), 1, key)
            proper = placeholders[0]
            self.assertEqual(proper.get("source"), "composed", key)
            self.assertEqual(str(proper.get("text") or "").strip(), PLACEHOLDER_TEXT, key)
            for forbidden in (
                "verses",
                "cycles",
                "weekday_cycles",
                "takes_from",
                "translations",
            ):
                self.assertNotIn(forbidden, proper, (key, forbidden))

            notes = str(mass.get("notes") or "")
            records = TRACKED_EVIDENCE.findall(notes)
            self.assertTrue(records, f"{key}: placeholder cites no tracked gap record")
            for record in records:
                self.assertTrue((ROOT / record).is_file(), (key, record))

    def test_english_ledger_accounts_for_every_slot_it_claims(self):
        """Coverage may be incomplete, but it may not be silent or stale."""
        coverage = propers_tool.english_coverage(CALENDARS, "postconciliar")
        self.assertIsNotNone(coverage)
        self.assertEqual(coverage["outside_the_ledger"], 0, coverage)
        self.assertEqual(coverage["unaccounted"], 0, coverage)
        self.assertEqual(coverage["unmatched_records"], 0, coverage)
        self.assertEqual(coverage["stale_translation_records"], 0, coverage)

    def test_unavailable_translation_identity_is_explicit_and_unique(self):
        """Form, cycle, extent, and repeated-slot occurrence are never inferred."""
        masses_by_key = {
            str(mass.get("key") or ""): mass for _, _, mass in self.rows
        }
        identities = set()
        for row in self.translations.get("untranslated") or []:
            label = (row.get("mass"), row.get("form_id"), row.get("proper"))
            self.assertEqual(row.get("availability"), "unavailable", label)
            self.assertEqual(row.get("lang"), "en", label)

            form_id = row.get("form_id")
            self.assertIsInstance(form_id, str, label)
            self.assertTrue(form_id.strip(), label)
            mass = masses_by_key.get(str(row.get("mass") or ""))
            self.assertIsNotNone(mass, label)
            forms = mass.get("forms") or []
            if forms:
                form_ids = [form.get("id") for form in forms]
                self.assertTrue(all(form_ids), (label, form_ids))
                self.assertEqual(len(form_ids), len(set(form_ids)), (label, form_ids))
                self.assertNotIn("main", form_ids, (label, form_ids))
                self.assertIn(form_id, form_ids, (label, form_ids))
            else:
                self.assertEqual(form_id, "main", label)
            cycle = row.get("cycle")
            self.assertIn(cycle, {"all", "A", "B", "C", "I", "II"}, label)
            occurrence = row.get("occurrence")
            self.assertIs(type(occurrence), int, label)
            self.assertGreaterEqual(occurrence, 1, label)

            extent = row.get("extent")
            self.assertIn(extent, {"body", "incipit"}, label)
            if extent == "body":
                self.assertNotIn("incipit", row, label)
            else:
                self.assertTrue(str(row.get("incipit") or "").strip(), label)

            reason = row.get("reason")
            self.assertIsInstance(reason, dict, label)
            self.assertIn(reason.get("kind"), {"no-exemplar", "rights-withheld"}, label)
            for forbidden in ("text", "translation", "translations"):
                self.assertNotIn(forbidden, row, (label, forbidden))
            if reason.get("kind") == "no-exemplar":
                for false_provenance in (
                    "rights",
                    "witness",
                    "source_id",
                    "witness_artifact_id",
                ):
                    self.assertNotIn(false_provenance, row, (label, false_provenance))
            else:
                self.assertEqual(row.get("rights"), "permission", label)
                for required in ("witness", "source_id", "witness_artifact_id"):
                    self.assertTrue(str(row.get(required) or "").strip(), (label, required))
                digests = row.get("quarantined_text_sha256")
                self.assertIsInstance(digests, list, label)
                self.assertTrue(digests, label)
                for digest in digests:
                    self.assertRegex(str(digest), r"\A[0-9a-f]{64}\Z", label)

            identity = (
                str(row.get("mass") or ""),
                form_id,
                str(row.get("proper") or ""),
                cycle,
                occurrence,
            )
            self.assertTrue(identity[0], label)
            self.assertTrue(identity[2], label)
            self.assertNotIn(identity, identities, identity)
            identities.add(identity)

    def test_incipit_fallbacks_remain_latin_citation_apparatus(self):
        """A Latin cue is present metadata, never a full English text."""
        for _, _, mass in self.rows:
            for _, proper in direct_propers(mass):
                material = _calendars.incipit_only_of(proper, "en")
                if material is None:
                    continue
                label = (mass.get("key"), proper.get("name"))
                self.assertEqual(proper.get("source"), "scripture", label)
                self.assertTrue(proper.get("verses"), label)
                self.assertEqual(material.get("text"), proper.get("incipit"), label)
                self.assertEqual(material.get("language"), "la", label)
                self.assertEqual(material.get("extent"), "incipit", label)
                self.assertEqual(material.get("requested_language"), "en", label)
                self.assertNotIn("requested_witness", material, label)

    def test_ordinary_uses_every_specific_absence_reason(self):
        """The Ordinary may be incomplete; one generic ICEL bucket may not return."""
        declared = {}
        for row in self.ordinary.get("absences") or []:
            key = str(row.get("key") or "")
            self.assertTrue(key, row)
            self.assertNotEqual(key, "icel")
            self.assertTrue(str(row.get("kind") or "").strip(), key)
            self.assertTrue(str(row.get("what") or "").strip(), key)
            self.assertNotIn(key, declared)
            declared[key] = row

        referenced = set()
        for section in self.ordinary.get("sections") or []:
            holders = [section, *(section.get("elements") or [])]
            for holder in holders:
                for side in ("english", "latin"):
                    reason = holder.get(f"absent_{side}")
                    if reason:
                        referenced.add(str(reason))

        self.assertEqual(referenced, set(declared))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
