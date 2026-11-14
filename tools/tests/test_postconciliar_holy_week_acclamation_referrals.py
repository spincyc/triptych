"""OLM 1981 p. 140: two unavailable verses and one non-cumulative referral.

This tests appointment structure and exact English absence joins, not possession
of liturgical wording, full target-2008 correspondence or annual completeness.
"""
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tomllib
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
CALENDARS = ROOT / "src/sources/calendars"
LEDGER = ROOT / "src/sources/inventories/postconciliar-proper-translations-v1.toml"
TARGET = (
    "edition.catholic-church.missale-romanum."
    "vatican-typica-tertia-reimpressio-emendata-2008"
)
KEYS = ("holy-monday", "holy-tuesday", "holy-wednesday")
GROUP = "main/holy-week-acclamation"
sys.path.insert(0, str(ROOT / "scripts"))
from _calendars import resolve_propers  # noqa: E402
from _proper_latin import body_owners  # noqa: E402


def load_tool(name):
    loader = SourceFileLoader(
        "_holy_week_referral_" + name.replace("-", "_"), str(ROOT / "tools" / name)
    )
    module = module_from_spec(spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


class HolyWeekAcclamationReferralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = yaml.safe_load(
            (CALENDARS / "postconciliar/propers.yaml").read_text()
        )
        cls.masses = {
            mass["key"]: mass
            for section in cls.document["sections"].values()
            for mass in section["masses"]
        }
        cls.owner = load_tool("mass-propers")

    @classmethod
    def public_masses(cls):
        # Keep raw-source checks independent of unrelated library validation;
        # projection checks still use the normal, fully validated shared owner.
        if not hasattr(cls, "_public"):
            structure = cls.owner.calendar_structure(
                CALENDARS, "postconciliar", cls.owner.book_tokens()
            )
            cls._public = {mass["key"]: mass for mass in structure["masses"]}
        return cls._public

    def acclamations(self, key):
        return [
            proper for proper in self.masses[key]["propers"]
            if proper["name"].startswith("Gospel Acclamation")
        ]

    def test_two_printed_roles_have_no_inferred_citation_or_words(self):
        # Gap campaign 2026-11-14: n. 257 (Monday) is an exact contiguous selection
        # of a public-domain Pustet 1862 verse and now carries its Latin body; n. 258
        # (Tuesday) is an abridgment and keeps its unavailable Latin body.
        for key, number in zip(KEYS[:2], (257, 258)):
            with self.subTest(mass=key):
                proper, = self.acclamations(key)
                self.assertEqual(proper["source"], "composed")
                if key == "holy-monday":
                    self.assertIsInstance(proper["text"], str)
                    self.assertNotIn("text_status", proper)
                else:
                    self.assertEqual(proper["text_status"], {
                        "state": "unavailable", "scope": "proper-body",
                        "reasons": [{"kind": "witness-gap", "source_id": TARGET}],
                    })
                    self.assertNotIn("text", proper)
                self.assertIn(f"n. {number}", proper["notes"])
                self.assertIn("artifact page 194 / printed page 140", proper["notes"])
                self.assertIn("target-2008 correspondence remains unestablished", proper["notes"])
                self.assertFalse({
                    "verses", "incipit", "translations", "cycles",
                    "weekday_cycles", "body_status", "takes_from",
                } & set(proper))
        owners = [
            (identity.mass, status) for identity, _, status in body_owners(self.document)
            if identity.mass in KEYS
            and identity.proper.startswith("Gospel Acclamation")
        ]
        self.assertEqual(owners, [("holy-monday", "present")],
                         "only the admitted Monday body is a Latin owner")

    def test_wednesday_preserves_exact_terminal_owners_and_one_choice(self):
        rows = self.acclamations("holy-wednesday")
        self.assertEqual([row["name"] for row in rows], [
            "Gospel Acclamation", "Gospel Acclamation (alternative)",
        ])
        for row, source, option in zip(rows, KEYS[:2], ("monday", "tuesday")):
            self.assertEqual(row["takes_from"], {
                "mass": source, "proper": "Gospel Acclamation",
                "citation": "OLM 1981 n. 259: nn. 257-258",
            })
            self.assertEqual(set(row), {"name", "takes_from", "ordinary_disposition"})
            disposition = row["ordinary_disposition"]
            self.assertEqual(
                {key: disposition[key] for key in ("kind", "group", "option")},
                {"kind": "alternative", "group": "holy-week-acclamation", "option": option},
            )
        self.assertEqual(
            rows[0]["ordinary_disposition"]["basis"],
            rows[1]["ordinary_disposition"]["basis"],
        )
        resolved, problems = resolve_propers(
            self.document, self.masses["holy-wednesday"]
        )
        self.assertEqual(problems, [])
        inherited = [
            (proper, taken) for _, proper, taken in resolved
            if proper["name"].startswith("Gospel Acclamation")
        ]
        self.assertEqual(len(inherited), 2)
        for (proper, taken), owner in zip(inherited, KEYS[:2]):
            self.assertEqual(taken["mass"], owner)
            self.assertEqual(self.owner.source_slot_identity(
                self.document, self.masses["holy-wednesday"], "", proper, taken
            ), (owner, "main", "Gospel Acclamation", 1))
            self.assertNotIn("verses", proper)
            if owner == "holy-monday":
                self.assertIsInstance(proper["text"], str)
            else:
                self.assertEqual(proper["text_status"]["state"], "unavailable")
                self.assertNotIn("text", proper)

    def test_repaired_seats_preserve_existing_readings_and_order(self):
        expected = {
            "holy-monday": ("Isaiah 42:1-7", "Psalm 27:1, 2, 3, 13-14", "John 12:1-11"),
            "holy-tuesday": (
                "Isaiah 49:1-6", "Psalm 71:1-2, 3-4a, 5-6ab, 15, 17",
                "John 13:21-33, 36-38",
            ),
            "holy-wednesday": (
                "Isaiah 50:4-9a", "Psalm 69:8-10, 21bcd-22, 31, 33-34",
                "Matthew 26:14-25",
            ),
        }
        for key, references in expected.items():
            with self.subTest(mass=key):
                rows = self.masses[key]["propers"]
                names = [proper["name"] for proper in rows]
                index = names.index("Responsorial Psalm")
                acclamations = [row["name"] for row in self.acclamations(key)]
                self.assertEqual(
                    names[index:index + len(acclamations) + 2],
                    ["Responsorial Psalm", *acclamations, "Gospel"],
                )
                self.assertEqual(tuple(
                    next(row for row in rows if row["name"] == name)["verses"][0]["ref"]
                    for name in ("First Reading", "Responsorial Psalm", "Gospel")
                ), references)

    def test_projection_retains_partial_masses_and_unavailable_bodies(self):
        public = self.public_masses()
        for key, owners in (
            ("holy-monday", ("holy-monday",)),
            ("holy-tuesday", ("holy-tuesday",)),
            ("holy-wednesday", KEYS[:2]),
        ):
            with self.subTest(mass=key):
                mass = public[key]
                self.assertEqual(mass["text_status"], {
                    "state": "partial", "scope": "missal-formulary",
                })
                rows = [row for row in mass["propers"]
                        if row["name"].startswith("Gospel Acclamation")]
                self.assertEqual(len(rows), len(owners))
                for row, owner in zip(rows, owners):
                    for field in ("citations", "incipit", "cycles"):
                        self.assertFalse(row.get(field), (key, field))
                    if owner == "holy-monday":
                        self.assertEqual(row["latin"]["provenance"]["relationship"],
                                         "editorial-projection-exact-to-target")
                        self.assertFalse(row.get("text_status"))
                    else:
                        self.assertEqual(row["text_status"], {
                            "state": "unavailable", "scope": "proper-body",
                        })
                        self.assertFalse(row.get("latin"))

    @unittest.skipUnless(shutil.which("node"), "node is required for shared seating")
    def test_shared_owner_requires_one_option_and_never_selects_by_order(self):
        code = r"""
const fs = require('node:fs');
const S = require('./src/web/browser/liturgy/ordinary-seating.js');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
function run(rows, choices) {
  const p = S.prepareProperAppointments(rows, {
    calendar: 'postconciliar', entrance: 'propers', choices
  });
  const events = S.unframedEvents(p.rows, null, p.selections);
  const choice = events.find(e => e.kind === 'proper_choice');
  return {selection: choice.selection, options: choice.options.map(o => o.id),
    groups: events.filter(e => e.kind === 'proper_choice').length,
    next: events[events.indexOf(choice) + 1].proper.name};
}
const out = {
  implicit: run(input.rows, {}),
  reversed: run([...input.rows].reverse(), {}),
  monday: run(input.rows, {'main/holy-week-acclamation': 'monday'}),
  tuesday: run(input.rows, {'main/holy-week-acclamation': 'tuesday'})
};
try { run(input.rows, {'main/holy-week-acclamation': 'invented'}); }
catch (error) { out.invalid = error.message; }
process.stdout.write(JSON.stringify(out));
"""
        rows = self.public_masses()["holy-wednesday"]["propers"]
        # Reversal checks default-selection invariance only, not liturgical order.
        completed = subprocess.run(
            ["node", "-e", code], cwd=ROOT, input=json.dumps({"rows": rows}),
            text=True, capture_output=True, check=True,
        )
        out = json.loads(completed.stdout)
        for label in ("implicit", "reversed"):
            self.assertEqual(out[label]["selection"], {"state": "required", "option": None})
            self.assertEqual(out[label]["groups"], 1)
        self.assertEqual(out["implicit"]["options"], ["monday", "tuesday"])
        self.assertEqual(out["implicit"]["next"], "Gospel")
        for option in ("monday", "tuesday"):
            self.assertEqual(out[option]["selection"], {"state": "selected", "option": option})
        self.assertTrue(out.get("invalid"))

    def test_english_absences_are_exact_terminal_rows_not_recipient_duplicates(self):
        # Gap campaign 2026-11-14 replaced both no-exemplar rows: Monday carries
        # Lefebvre 1925 antecedent English of its exact Latin clause, Tuesday a
        # project study translation of the abridged verse.
        ledger = tomllib.loads(LEDGER.read_text())
        records = [
            row for row in ledger["untranslated"]
            if row["mass"] in KEYS
            and row["proper"].startswith("Gospel Acclamation")
        ]
        self.assertEqual(records, [])
        entries = {
            row["mass"]: row for row in ledger["entries"]
            if row["mass"] in KEYS and row["proper"].startswith("Gospel Acclamation")
        }
        self.assertEqual(set(entries), set(KEYS[:2]))
        self.assertEqual(entries["holy-monday"]["witness"], "lefebvre-1925")
        self.assertEqual(entries["holy-monday"]["translations"][0]["rights"], "public-domain")
        self.assertEqual(entries["holy-tuesday"]["relation"], "abridged")
        self.assertEqual(entries["holy-tuesday"]["translations"][0]["rights"], "project-created")
        for row in entries.values():
            self.assertEqual(
                (row["form_id"], row["proper"], row["cycle"], row["occurrence"]),
                ("main", "Gospel Acclamation", "all", 1),
            )

    def test_public_english_follows_both_terminal_referrals(self):
        public = self.public_masses()
        for key, owners in (
            ("holy-monday", ("holy-monday",)),
            ("holy-tuesday", ("holy-tuesday",)),
            ("holy-wednesday", KEYS[:2]),
        ):
            with self.subTest(mass=key):
                rows = [
                    row for row in public[key]["propers"]
                    if row["name"].startswith("Gospel Acclamation")
                ]
                self.assertEqual(len(rows), len(owners))
                for row, owner in zip(rows, owners):
                    self.assertFalse(row.get("untranslated"))
                    states = {
                        state["lang"]: state
                        for state in self.owner.proper_language_capabilities(row)
                    }
                    self.assertTrue(states["en"]["available"])
                    self.assertEqual(states["la"]["available"], owner == "holy-monday")
                    self.assertEqual(len(row["translations"]), 1)

    def test_passage_keeps_fresh_inspection_and_prior_artifact_provenance_distinct(self):
        path = (
            ROOT / "src/sources/works/catholic-church/ordo-lectionum-missae/"
            "editions/latin-editio-typica-altera-1981/passages/"
            "holy-week-acclamation-referrals-257-259.toml"
        )
        passage = tomllib.loads(path.read_text())
        self.assertEqual(passage["artifact_page_ranges"], [[194, 194]])
        self.assertEqual(passage["verified_on"], "2026-10-22")
        self.assertIn("not the complete PDF", passage["notes"])
        self.assertNotIn("text", passage)
        self.assertNotIn("transcription_segments", passage)


if __name__ == "__main__":
    unittest.main()
