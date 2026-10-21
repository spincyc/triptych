from __future__ import annotations

import copy
import re
import tomllib
import unittest
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
CALENDAR = ROOT / "src/sources/calendars/postconciliar/propers.yaml"
INVENTORY = (
    ROOT
    / "src/sources/inventories/postconciliar-sanctoral-commons-v1.toml"
)
ORDO_ARTIFACT = (
    ROOT
    / "src/sources/works/catholic-church/ordo-lectionum-missae/editions"
    / "latin-editio-typica-altera-1981/artifacts"
    / "internet-archive-scan-pdf-ed4bc14e/artifact.toml"
)
ANTIPHONARY_ARTIFACT = (
    ROOT
    / "src/sources/works/catholic-church/missale-romanum/editions"
    / "2010-english-icel-antiphonary/artifacts/antiphonary-pdf/artifact.toml"
)

ANTIPHONARY_SOURCE_ID = (
    "artifact.catholic-church.missale-romanum.2010-english-icel-antiphonary"
    ".antiphonary-pdf"
)

COMMON_PATTERNS = (
    ("dedication-of-a-church", r"dedicationis ecclesiae"),
    ("blessed-virgin-mary", r"beatae Mariae Virginis"),
    ("martyrs", r"\bmartyrum\b"),
    ("pastors", r"\bpastorum\b"),
    ("doctors-of-the-church", r"doctorum Ecclesiae"),
    ("virgins", r"\bvirginum\b"),
    ("saints-and-holy-women", r"\bsanctorum\b|\bsanctarum\b"),
)
COMMON_MASS_CATEGORIES = {
    "commune-dedicationis-ecclesiae": "dedication-of-a-church",
    "commune-beatae-mariae-virginis": "blessed-virgin-mary",
    "commune-martyrum": "martyrs",
    "commune-pastorum": "pastors",
    "commune-doctorum-ecclesiae": "doctors-of-the-church",
    "commune-virginum": "virgins",
    "commune-sanctorum": "saints-and-holy-women",
}


def _categories(heading: str) -> list[str]:
    found = []
    for category, pattern in COMMON_PATTERNS:
        match = re.search(pattern, heading, re.IGNORECASE)
        if match:
            found.append((match.start(), category))
    return [category for _, category in sorted(found)]


def _heading_from_ordo_note(notes: str) -> str | None:
    match = re.search(
        r"The Ordo heads it (De Communi.*?)(?=, and this repository|"
        r" and notes that|\. |\.$)",
        notes,
        re.DOTALL,
    )
    if match:
        return match.group(1)
    match = re.search(
        r"The Ordo prints a proper formulary and adds "
        r"(Vel de Communi.*?) after it;",
        notes,
        re.DOTALL,
    )
    return match.group(1) if match else None


def _standard_ordo_row(section: str, mass: dict, heading: str) -> dict:
    notes = mass["notes"]
    locator = re.search(
        r"artifact page (\d+), printed page (\d+), n\. (\d+)", notes
    )
    if not locator:
        raise AssertionError(f"missing exact Ordo locator for {mass['key']}")
    categories = _categories(heading)
    if not categories:
        raise AssertionError(f"unclassified Common heading for {mass['key']}")
    return {
        "key": f"postconciliar-common.{mass['key']}",
        "mass_key": mass["key"],
        "registry": mass["registry"],
        "date": mass["date"],
        "section": section,
        "celebration": mass["name"],
        "basis": "ordo-lectionum-missae-1981",
        "evidence_scope": "lectionary-readings",
        "source": "ordo-1981",
        "source_locus": (
            f"artifact page {locator.group(1)}, printed page "
            f"{locator.group(2)}, n. {locator.group(3)}"
        ),
        "artifact_page": int(locator.group(1)),
        "printed_page": int(locator.group(2)),
        "entry_number": locator.group(3),
        "heading": heading,
        "categories": categories,
        "subselections": re.findall(r"\[([^\]]+)\]", heading),
        "alternatives": len(categories) > 1,
        "wrong_edition_evidence": (
            "ANTECEDENT, NOT THE CONTROLLING EDITION" in notes
        ),
        "target_formulary_body_authority": False,
        "resolvable": False,
    }


def _annex_row(section: str, mass: dict) -> dict:
    notes = mass["notes"]
    ordo = re.search(
        r"IN ORDINEM LECTIONUM MISSAE, n\. ([^:]+): '([^']+)'", notes
    )
    missal = re.search(r"IN MISSALE ROMANUM, [^:]+: '([^']+)'", notes)
    source_url = re.search(r"https://[^, ]+\.pdf", notes)
    if not (ordo and missal and source_url):
        raise AssertionError(f"incomplete official-annex note for {mass['key']}")
    heading = ordo.group(2)
    categories = _categories(heading)
    page = re.search(
        r"(?:PDF page|page image, page|page images, PDF page) (\d+)", notes
    )
    source_locus = (
        f"PDF page {page.group(1)}"
        if page
        else "page not stated in the current calendar note"
    )
    return {
        "key": f"postconciliar-common.{mass['key']}",
        "mass_key": mass["key"],
        "registry": mass["registry"],
        "date": mass["date"],
        "section": section,
        "celebration": mass["name"],
        "basis": "official-additiones-recovered-from-calendar-note",
        "evidence_scope": "reported-missal-and-lectionary-directions",
        "source_url": source_url.group(0),
        "source_locus": source_locus,
        "entry_number": ordo.group(1),
        "heading": heading,
        "missal_heading": missal.group(1),
        "categories": categories,
        "subselections": re.findall(r"\[([^\]]+)\]", heading),
        "alternatives": len(categories) > 1,
        "wrong_edition_evidence": False,
        "target_formulary_body_authority": False,
        "resolvable": False,
    }


def _antiphonary_row(section: str, mass: dict) -> dict:
    relation = mass["common_from"]
    if relation["source_id"] != ANTIPHONARY_SOURCE_ID:
        raise AssertionError(f"invalid Antiphonary source for {mass['key']}")
    locator = re.fullmatch(
        r"artifact page ([1-9]\d*), printed page ([1-9]\d*)"
        r"(?:; Common target printed pages [1-9]\d*(?:, [1-9]\d*)*)?",
        relation["locus"],
    )
    if not locator:
        raise AssertionError(f"invalid Antiphonary locator for {mass['key']}")
    categories = [
        COMMON_MASS_CATEGORIES[option["mass"]] for option in relation["options"]
    ]
    return {
        "key": f"postconciliar-common.{mass['key']}",
        "mass_key": mass["key"],
        "registry": mass["registry"],
        "date": mass["date"],
        "section": section,
        "celebration": mass["name"],
        "basis": "icel-antiphonary-2010",
        "evidence_scope": relation["scope"],
        "source": "icel-antiphonary-2010",
        "source_locus": relation["locus"],
        "artifact_page": int(locator.group(1)),
        "printed_page": int(locator.group(2)),
        "categories": categories,
        "subselections": [
            option["selection"]
            for option in relation["options"]
            if option.get("selection")
        ],
        "alternatives": len(categories) > 1,
        "wrong_edition_evidence": False,
        "target_formulary_body_authority": False,
        "resolvable": False,
    }


def derive_rows(calendar: dict) -> list[dict]:
    rows = []
    for section, payload in calendar["sections"].items():
        for mass in payload["masses"]:
            if not mass.get("date"):
                continue
            notes = mass.get("notes", "")
            heading = _heading_from_ordo_note(notes)
            if heading:
                rows.append(_standard_ordo_row(section, mass, heading))
            elif "IN ORDINEM LECTIONUM MISSAE" in notes and "De Communi" in notes:
                rows.append(_annex_row(section, mass))
            elif mass.get("common_from"):
                rows.append(_antiphonary_row(section, mass))
    return sorted(rows, key=lambda row: (row["date"], row["mass_key"]))


class PostconciliarSanctoralCommonsInventoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.calendar = yaml.safe_load(CALENDAR.read_text(encoding="utf-8"))
        cls.inventory = tomllib.loads(INVENTORY.read_text(encoding="utf-8"))
        cls.rows = cls.inventory["rows"]
        cls.expected = derive_rows(cls.calendar)

    def test_structured_common_targets_keep_exact_pointer_and_option_metadata(self) -> None:
        expected = {
            "saint-raymond-penyafort-priest": (97, 89, "161", ["pastors"],
                ["For One Pastor (p. 161 )"]),
            "saint-hilary-bishop-doctor-church": (97, 89, "159, 165",
                ["pastors", "doctors-of-the-church"], ["For a Bishop (p. 159 )"]),
            "saint-apollinaris-bishop-martyr": (121, 113, "154, 159",
                ["martyrs", "pastors"], ["For One Martyr (p. 154 )", "For a Bishop (p. 159 )"]),
            "saint-peter-claver-priest": (131, 123, "161, 172",
                ["pastors", "saints-and-holy-women"],
                ["For One Pastor (p. 161 )", "For Those Who Practiced Works of Mercy (p. 172 )"]),
        }
        masses = {mass["key"]: (section, mass)
                  for section, payload in self.calendar["sections"].items()
                  for mass in payload["masses"]}
        rows = {row["mass_key"]: row for row in self.rows}
        for key, (artifact, printed, targets, categories, subselections) in expected.items():
            with self.subTest(mass=key):
                section, mass = masses[key]
                relation = mass["common_from"]
                row = _antiphonary_row(section, mass)
                self.assertEqual(row, rows[key])
                self.assertEqual((row["artifact_page"], row["printed_page"]), (artifact, printed))
                self.assertEqual(row["source_locus"],
                    f"artifact page {artifact}, printed page {printed}; Common target printed pages {targets}")
                self.assertEqual(row["source_locus"], relation["locus"])
                self.assertEqual(relation["source_id"], ANTIPHONARY_SOURCE_ID)
                self.assertEqual(row["categories"], categories)
                self.assertEqual(len(row["categories"]), len(relation["options"]))
                self.assertEqual(row["subselections"], subselections)
                self.assertEqual(row["alternatives"], len(relation["options"]) > 1)

    def test_antiphonary_locator_and_source_remain_strict(self) -> None:
        mass = next(mass for payload in self.calendar["sections"].values()
                    for mass in payload["masses"] if mass["key"] == "saint-raymond-penyafort-priest")
        invalid = [
            "artifact page 97",
            "artifact page 97, printed page 89; Common target printed pages ",
            "artifact page 97, printed page 89; Common target printed pages unknown",
            "artifact page 97, printed page 89; Common target printed pages 159-165",
            "artifact page 97, printed page 89; Common target printed pages 159,165",
            "artifact page 97, printed page 89; Common target printed pages 161; arbitrary suffix",
            "artifact page 0, printed page 89",
            "artifact page 97, printed page 0",
        ]
        for locus in invalid:
            mutated = copy.deepcopy(mass)
            mutated["common_from"]["locus"] = locus
            with self.subTest(locus=locus), self.assertRaisesRegex(AssertionError, "invalid Antiphonary locator"):
                _antiphonary_row("sanctoral", mutated)
        wrong_source = copy.deepcopy(mass)
        wrong_source["common_from"]["source_id"] = "artifact.unrelated-antiphonary"
        with self.assertRaisesRegex(AssertionError, "invalid Antiphonary source"):
            _antiphonary_row("sanctoral", wrong_source)

    def test_held_ordo_evidence_keeps_precedence_over_common_direction(self) -> None:
        masses = {mass["key"]: mass for payload in self.calendar["sections"].values()
                  for mass in payload["masses"]}
        overlap = [row for row in self.rows
                   if row["basis"] == "ordo-lectionum-missae-1981"
                   and masses[row["mass_key"]].get("common_from")]
        self.assertTrue(overlap)
        derived = {row["mass_key"]: row for row in derive_rows(self.calendar)}
        for row in overlap:
            with self.subTest(mass=row["mass_key"]):
                self.assertEqual(derived[row["mass_key"]], row)
                self.assertEqual(row["evidence_scope"], "lectionary-readings")

    def test_inventory_is_exact_current_note_recovery(self) -> None:
        self.assertEqual(self.rows, self.expected)
        self.assertEqual(len(self.rows), len({row["key"] for row in self.rows}))
        self.assertEqual(
            len(self.rows), len({row["mass_key"] for row in self.rows})
        )
        for row in self.rows:
            with self.subTest(row=row["key"]):
                self.assertNotIn(";", row["mass_key"])
                self.assertRegex(row["mass_key"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    def test_declared_counts_are_derived_from_rows(self) -> None:
        counts = self.inventory["counts"]
        actual = {
            "rows": len(self.rows),
            "ordo_1981": sum(
                row["basis"] == "ordo-lectionum-missae-1981"
                for row in self.rows
            ),
            "official_additiones": sum(
                row["basis"]
                == "official-additiones-recovered-from-calendar-note"
                for row in self.rows
            ),
            "antiphonary": sum(
                row["basis"] == "icel-antiphonary-2010" for row in self.rows
            ),
            "alternatives": sum(row["alternatives"] for row in self.rows),
            "with_subselection": sum(
                bool(row["subselections"]) for row in self.rows
            ),
            "wrong_edition_evidence": sum(
                row["wrong_edition_evidence"] for row in self.rows
            ),
        }
        self.assertEqual(counts["rows"], actual)
        self.assertEqual(
            counts["sections"], dict(Counter(row["section"] for row in self.rows))
        )
        self.assertEqual(
            counts["category_appearances"],
            {
                category: Counter(
                    item
                    for row in self.rows
                    for item in row["categories"]
                )[category]
                for category, _ in COMMON_PATTERNS
            },
        )

    def test_recovery_rows_are_not_resolver_inputs(self) -> None:
        self.assertEqual(
            self.inventory["status"], "recovery-not-resolution"
        )
        forbidden = {"takes_from", "common_from", "mass", "target_mass"}
        for row in self.rows:
            with self.subTest(row=row["key"]):
                self.assertFalse(forbidden & row.keys())
                self.assertFalse(row["target_formulary_body_authority"])
                self.assertFalse(row["resolvable"])
                if row["basis"] == "ordo-lectionum-missae-1981":
                    self.assertEqual(row["evidence_scope"], "lectionary-readings")
                if row["basis"] == "icel-antiphonary-2010":
                    self.assertEqual(row["evidence_scope"], "missal-antiphons")

    def test_registered_witnesses_match_exact_artifacts(self) -> None:
        witnesses = self.inventory["witnesses"]
        for key, path in (
            ("ordo-1981", ORDO_ARTIFACT),
            ("icel-antiphonary-2010", ANTIPHONARY_ARTIFACT),
        ):
            artifact = tomllib.loads(path.read_text(encoding="utf-8"))
            with self.subTest(witness=key):
                self.assertEqual(witnesses[key]["artifact_id"], artifact["id"])
                self.assertEqual(
                    witnesses[key]["artifact_sha256"], artifact["sha256"]
                )
                self.assertEqual(witnesses[key]["storage"], artifact["storage"])


if __name__ == "__main__":
    unittest.main()
