from __future__ import annotations

import copy
import hashlib
import json
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
CORRECTIONS = "src/sources/inventories/postconciliar-common-recovery-corrections-v1.toml"
ENGLISH = "src/sources/inventories/postconciliar-proper-translations-v1.toml"
REVIEWED_RECIPIENTS = {
    "saint-jerome-emiliani": ("pc-02-08", "02-08", "februarii-8"),
    "saint-george-martyr": ("pc-04-23", "04-23", "aprilis-23"),
}
EDITION_1970 = "edition.catholic-church.missale-romanum.vatican-typica-1970"
EDITION_2008 = "edition.catholic-church.missale-romanum.vatican-typica-tertia-reimpressio-emendata-2008"
EDITION_2002 = "edition.catholic-church.missale-romanum.vatican-typica-tertia-2002"
EDITION_1861 = "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861"


def _require_correction(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(f"invalid correction evidence: {message}")


def load_correction_evidence(root: Path = ROOT) -> dict:
    """Read a bounded evidence contract, never the expected recovery rows."""
    contract = tomllib.loads((root / CORRECTIONS).read_text(encoding="utf-8"))
    _require_correction(
        contract.get("schema") == 2
        and contract.get("record_type") == "postconciliar-common-recovery-corrections"
        and contract.get("status") == "historical-evidence-only",
        "contract identity or disposition",
    )
    records = {}
    for alias, pin in contract["sources"].items():
        path = Path(pin["path"])
        _require_correction(
            not path.is_absolute() and ".." not in path.parts
            and path.as_posix().startswith("src/sources/works/")
            and path.suffix == ".toml"
            and (root / path).resolve().is_relative_to(root.resolve()),
            f"unsafe source path for {alias}",
        )
        try:
            raw = (root / path).read_bytes()
        except OSError as error:
            raise AssertionError(f"invalid correction evidence: missing {alias}") from error
        _require_correction(hashlib.sha256(raw).hexdigest() == pin["sha256"],
                            f"changed source record {alias}")
        record = tomllib.loads(raw.decode("utf-8"))
        _require_correction(record.get("id") == pin["id"], f"source identity {alias}")
        records[alias] = record
    return {"contract": contract, "records": records,
            "english": tomllib.loads((root / ENGLISH).read_text(encoding="utf-8"))}


def _reviewed_correction_keys(calendar: dict, evidence: dict) -> frozenset[str]:
    """Fail closed if either reviewed correction loses its independent evidence."""
    contract, records, english = (evidence[key] for key in ("contract", "records", "english"))
    cases = contract["corrections"]
    _require_correction(
        len(cases) == len(REVIEWED_RECIPIENTS)
        and {case["mass_key"] for case in cases} == set(REVIEWED_RECIPIENTS),
        "missing, duplicate or unreviewed recipient contract",
    )
    for alias, edition_id, date in (("comparison-edition", EDITION_1970, "1970"),
                                    ("historical-edition", EDITION_1861, "1861")):
        edition = records[alias]
        _require_correction(edition.get("record_type") == "edition"
                            and edition.get("id") == edition_id
                            and edition.get("date") == date, f"edition boundary {alias}")
    for alias, edition_id in (("comparison-artifact", EDITION_1970),
                              ("historical-scan", EDITION_1861),
                              ("historical-text", EDITION_1861)):
        artifact = records[alias]
        _require_correction(artifact.get("record_type") == "artifact"
                            and artifact.get("edition_id") == edition_id,
                            f"artifact edition {alias}")
    _require_correction(records["comparison-artifact"].get("storage") == "restricted"
                        and records["comparison-artifact"].get("indexable") is False,
                        "1970 witness must remain restricted")

    def passage(alias: str, artifact_alias: str, locus: str, locator: dict) -> dict:
        _require_correction(alias in records, f"missing source passage {alias}")
        record, artifact = records[alias], records[artifact_alias]
        _require_correction(
            record.get("record_type") == "passage"
            and record.get("edition_id") == artifact["edition_id"]
            and record.get("artifact_id") == artifact["id"]
            and record.get("artifact_sha256") == artifact["sha256"]
            and record.get("locus") == locus
            and {"cataloged", "acquired", "inspected", "verified"} <= set(record.get("states", []))
            and all(record.get(key) == value for key, value in locator.items()),
            f"source ownership, locus or verification {alias}",
        )
        return record

    for case in cases:
        key = case["mass_key"]
        registry, date, liturgical_locus = REVIEWED_RECIPIENTS[key]
        _require_correction(
            (case["registry"], case["date"], case["section"], case["proper"],
             case["form_id"], case["cycle"], case["occurrence"])
            == (registry, date, "sanctoral", "Collect", "main", "all", 1),
            f"recipient contract {key}",
        )
        recipients = [(section, mass) for section, payload in calendar["sections"].items()
                      for mass in payload["masses"] if mass["key"] == key]
        _require_correction(len(recipients) == 1, f"missing or duplicate recipient {key}")
        section, mass = recipients[0]
        _require_correction((section, mass.get("registry"), mass.get("date"))
                            == ("sanctoral", registry, date), f"calendar recipient {key}")
        _require_correction(mass.get("text_status") == {
            "state": "partial", "scope": "missal-formulary",
            "reasons": [{"kind": "witness-gap", "source_id": EDITION_2008}]},
            f"2008 witness gap {key}")
        collects = [proper for proper in mass.get("propers", []) if proper.get("name") == "Collect"]
        _require_correction(len(collects) == 1, f"Collect occurrence {key}")
        collect = collects[0]
        _require_correction(collect.get("source") == "composed"
                            and not ({"text", "verses", "cycles", "takes_from"} & collect.keys())
                            and collect.get("text_status") == {
                                "state": "unavailable", "scope": "proper-body",
                                "reasons": [{"kind": "rights-withheld", "source_id": EDITION_2002}]},
                            f"unavailable Latin Collect {key}")
        passage(case["comparison"], "comparison-artifact",
                f"proprium-de-sanctis/{liturgical_locus}/collecta",
                {"artifact_page_ranges": [[case["comparison_page"], case["comparison_page"]]]})
        verification = passage(case["historical_verification"], "historical-scan",
                               case["historical_locus"],
                               {"artifact_page_ranges": [[case["historical_page"], case["historical_page"]]]})
        publication = passage(case["historical_publication"], "historical-text",
                              case["historical_locus"],
                              {"physical_line_ranges": [[case["historical_line"], case["historical_line"]]]})
        positives = [row for row in english["entries"]
                     if row.get("mass") == key and row.get("proper") == "Collect"]
        negatives = [row for row in english["untranslated"]
                     if row.get("mass") == key and row.get("proper") == "Collect"]
        if case["english_disposition"] == "revised-historical-antecedent":
            _require_correction(len(positives) == 1 and not negatives,
                                f"revised English disposition {key}")
            row = positives[0]
            _require_correction(
                row.get("witness_relation") == "antecedent" and row.get("relation") == "revised"
                and row.get("passage_id") == verification["id"]
                and row.get("artifact_id") == verification["artifact_id"]
                and row.get("publication_passage_id") == publication["id"]
                and row.get("publication_artifact_id") == publication["artifact_id"]
                and row.get("publication_artifact_sha256") == publication["artifact_sha256"]
                and len(row.get("translations", [])) == 1
                and row["translations"][0].get("lang") == "en"
                and row["translations"][0].get("source_id") == EDITION_1861,
                f"historical revised English source {key}",
            )
        elif case["english_disposition"] == "historical-source-only-no-modern-english":
            _require_correction(not positives and len(negatives) == 1,
                                f"no modern English binding {key}")
            row = negatives[0]
            _require_correction(row.get("lang") == "en" and row.get("extent") == "body"
                                and row.get("availability") == "unavailable"
                                and row.get("reason") == {"kind": "no-exemplar"},
                                f"English no-exemplar refusal {key}")
        else:
            raise AssertionError(f"invalid correction evidence: unknown English disposition {key}")
        _require_correction((row.get("form_id"), row.get("cycle"), row.get("occurrence"))
                            == ("main", "all", 1), f"English recipient tuple {key}")
    return frozenset(REVIEWED_RECIPIENTS)

ANTIPHONARY_SOURCE_ID = (
    "artifact.catholic-church.missale-romanum.2010-english-icel-antiphonary"
    ".antiphonary-pdf"
)

LORETO_SOURCE_ID = 'artifact.holy-see.inscription-beatae-mariae-virginis-de-loreto-2019.vatican-bulletin-2019-10-31.official-html-9c6e1926'
LORETO_ARTIFACT = ROOT / 'src/sources/works/holy-see/inscription-beatae-mariae-virginis-de-loreto-2019/editions/vatican-bulletin-2019-10-31/artifacts/official-html-9c6e1926/artifact.toml'
LORETO_LOCUS = 'Official2019 Latin Missale Romanum annex:10December; De Communi beatae Mariae Virginis; entire Common direction precedes ownCollect'

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


def _standard_ordo_row(section: str, mass: dict, heading: str,
                       corrected_keys: frozenset[str]) -> dict:
    notes = mass["notes"]
    locator = re.search(
        r"artifact page (\d+), printed page (\d+), n\. (\d+)", notes
    )
    if not locator:
        raise AssertionError(f"missing exact Ordo locator for {mass['key']}")
    return _ordo_row(section, mass, heading,
                     (int(locator.group(1)), int(locator.group(2)), locator.group(3)),
                     mass["key"] in corrected_keys
                     or "ANTECEDENT, NOT THE CONTROLLING EDITION" in notes)


def _ordo_row(section: str, mass: dict, heading: str,
              locator: tuple[int, int, str], wrong_edition: bool) -> dict:
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
            f"artifact page {locator[0]}, printed page {locator[1]}, n. {locator[2]}"
        ),
        "artifact_page": locator[0],
        "printed_page": locator[1],
        "entry_number": locator[2],
        "heading": heading,
        "categories": categories,
        "subselections": re.findall(r"\[([^\]]+)\]", heading),
        "alternatives": len(categories) > 1,
        "wrong_edition_evidence": wrong_edition,
        "target_formulary_body_authority": False,
        "resolvable": False,
    }


def _martha_ordo_row(calendar: dict, evidence: dict) -> dict:
    """Keep the historical reading cue through the separately evidenced 2021 title change."""
    contract, records = evidence["contract"], evidence["records"]
    case = contract.get("martha_lectionary", {})
    _require_correction(
        (case.get("mass_key"), case.get("registry"), case.get("date"), case.get("section"),
         case.get("recipient_title"), case.get("source_title"), case.get("source_scope"),
         case.get("artifact_page"), case.get("printed_page"), case.get("entry_number"),
         case.get("raw_common_heading"), case.get("proper_gospel_cue"))
        == ("saints-martha-mary-lazarus", "pc-07-29", "07-29", "sanctoral",
            "Saints Martha, Mary, and Lazarus", "S. Marthae", "lectionary-readings",
            352, 298, "607", "De Communi sanctarum.", "Evangelium huius memoriae est proprium."),
        "Martha historical reading contract",
    )
    required = {"martha-ordo", "martha-annex", "martha-decree",
                "martha-book-boundaries", "martha-title-authority"}
    _require_correction(required <= records.keys(), "missing Martha source records")
    ordo = records["martha-ordo"]
    _require_correction(
        ordo.get("record_type") == "artifact"
        and ordo.get("id") == "artifact.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981.internet-archive-scan-pdf-ed4bc14e"
        and ordo.get("edition_id") == "edition.catholic-church.ordo-lectionum-missae.latin-editio-typica-altera-1981"
        and ordo.get("sha256") == "ed4bc14e6c5f885be9cb220f4edbdd23c1db749b53c1489058d6e54cfaf7fd0d"
        and ordo.get("storage") == "restricted", "Martha 1981 witness identity",
    )
    owner = "catholic-church.roman-calendar-martha-mary-lazarus-additions-2021.2021-official-latin-decree-and-annex"
    for alias, artifact_alias, suffix, locus in (
        ("martha-book-boundaries", "martha-annex", "book-boundaries", "annex/book-boundaries"),
        ("martha-title-authority", "martha-decree", "decree-calendar-and-annex-authority", "decree/calendar-and-annex-authority"),
    ):
        passage, artifact = records[alias], records[artifact_alias]
        _require_correction(
            passage.get("record_type") == "passage"
            and passage.get("id") == f"passage.{owner}.{suffix}"
            and passage.get("edition_id") == artifact.get("edition_id") == f"edition.{owner}"
            and artifact.get("record_type") == "artifact" and artifact.get("storage") == "restricted"
            and passage.get("artifact_id") == artifact.get("id")
            and passage.get("artifact_sha256") == artifact.get("sha256")
            and passage.get("locus") == locus
            and {"cataloged", "acquired", "inspected", "verified"} <= set(passage.get("states", [])),
            f"Martha title and book-boundary evidence {alias}",
        )
    _require_correction(records["martha-book-boundaries"].get("artifact_page_ranges") == [[1, 5]],
                        "Martha complete annex boundary")
    recipients = [(section, mass) for section, payload in calendar["sections"].items()
                  for mass in payload["masses"] if mass.get("key") == case["mass_key"]]
    _require_correction(len(recipients) == 1, "missing or duplicate Martha recipient")
    section, mass = recipients[0]
    _require_correction(
        (section, mass.get("registry"), mass.get("date"), mass.get("name"), mass.get("rank"), mass.get("kind"))
        == ("sanctoral", "pc-07-29", "07-29", case["recipient_title"], "Memorial", "sanctoral")
        and not (mass.keys() - {"key", "registry", "date", "name", "rank", "kind", "text_status", "propers", "notes"}),
        "Martha current recipient identity or unreviewed selection",
    )
    _require_correction(mass.get("text_status") == {
        "state": "partial", "scope": "missal-formulary",
        "reasons": [{"kind": "rights-withheld", "source_id": f"segment.{owner}.missal-formulary-pages-1-2"}]},
        "Martha held Missal-formulary boundary")
    propers = mass.get("propers", [])
    readings = [proper for proper in propers if proper.get("source") == "scripture"]
    reading_bytes = (json.dumps(readings, sort_keys=True, ensure_ascii=False,
                               separators=(",", ":")) + "\n").encode("utf-8")
    _require_correction(len(readings) == 5
                        and hashlib.sha256(reading_bytes).hexdigest() == case.get("reading_nodes_sha256"),
                        "Martha unchanged five historical reading nodes")
    held = [proper for proper in propers if proper.get("source") != "scripture"]
    slots = [("Entrance Antiphon", "entrance"), ("Collect", "collect"),
             ("Prayer over the Offerings", "offerings"), ("Communion Antiphon", "communion"),
             ("Prayer after Communion", "postcommunion")]
    _require_correction(len(propers) == 10 and [proper.get("name") for proper in held]
                        == [name for name, _ in slots], "Martha five held Missal roles")
    for proper, (name, suffix) in zip(held, slots):
        _require_correction(proper.get("source") == "composed"
                            and not (proper.keys() - {"name", "source", "text_status", "notes"})
                            and proper.get("text_status") == {
                                "state": "unavailable", "scope": "proper-body", "body_status": "held-unpublished",
                                "reasons": [{"kind": "rights-withheld", "source_id": f"passage.{owner}.{suffix}-appointment"}]},
                            f"Martha held role or body authority {name}")
    return _ordo_row(section, mass, case["raw_common_heading"].removesuffix("."),
                     (case["artifact_page"], case["printed_page"], case["entry_number"]), False)


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


def _official_missal_row(section: str, mass: dict) -> dict:
    """Recover only the exact reviewed 2019 direction, without resolving it."""
    relation = mass["common_from"]
    if (
        (mass["key"], mass["registry"], mass["date"])
        != ("our-lady-loreto", "pc-12-10", "12-10")
        or relation.get("source_id") != LORETO_SOURCE_ID
        or relation.get("scope") != "missal-antiphons"
        or relation.get("locus") != LORETO_LOCUS
        or relation.get("options") != [{"mass": "commune-beatae-mariae-virginis"}]
    ):
        raise AssertionError(f"unreviewed official Missal direction for {mass['key']}")
    return {
        "key": f"postconciliar-common.{mass['key']}",
        "mass_key": mass["key"],
        "registry": mass["registry"],
        "date": mass["date"],
        "section": section,
        "celebration": mass["name"],
        "basis": "official-missal-annex",
        "evidence_scope": "missal-antiphons",
        "source": "loreto-2019",
        "source_artifact_id": LORETO_SOURCE_ID,
        "source_locus": relation["locus"],
        "source_referral": "De Communi beatae Mariae Virginis",
        "source_referral_scope": "Broader Missal direction; this stored pointer records only its antiphon subset. Remaining lawful choices are unresolved.",
        "categories": ["blessed-virgin-mary"],
        "subselections": [],
        "alternatives": False,
        "wrong_edition_evidence": False,
        "target_formulary_body_authority": False,
        "resolvable": False,
    }


def derive_rows(calendar: dict, correction_evidence: dict | None = None) -> list[dict]:
    evidence = correction_evidence if correction_evidence is not None else load_correction_evidence()
    corrected_keys = _reviewed_correction_keys(calendar, evidence)
    martha_row = _martha_ordo_row(calendar, evidence)
    rows = []
    for section, payload in calendar["sections"].items():
        for mass in payload["masses"]:
            if not mass.get("date"):
                continue
            if mass["key"] == martha_row["mass_key"]:
                rows.append(martha_row)
                continue
            notes = mass.get("notes", "")
            heading = _heading_from_ordo_note(notes)
            if heading:
                rows.append(_standard_ordo_row(section, mass, heading, corrected_keys))
            elif "IN ORDINEM LECTIONUM MISSAE" in notes and "De Communi" in notes:
                rows.append(_annex_row(section, mass))
            elif mass.get("common_from"):
                if mass["common_from"].get("source_id") == LORETO_SOURCE_ID:
                    rows.append(_official_missal_row(section, mass))
                else:
                    rows.append(_antiphonary_row(section, mass))
    return sorted(rows, key=lambda row: (row["date"], row["mass_key"]))


class PostconciliarSanctoralCommonsInventoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.calendar = yaml.safe_load(CALENDAR.read_text(encoding="utf-8"))
        cls.inventory = tomllib.loads(INVENTORY.read_text(encoding="utf-8"))
        cls.rows = cls.inventory["rows"]
        cls.correction_evidence = load_correction_evidence()
        cls.expected = derive_rows(cls.calendar, cls.correction_evidence)

    def test_corrections_survive_prose_changes_without_reading_output_flags(self) -> None:
        changed = copy.deepcopy(self.calendar)
        for payload in changed["sections"].values():
            for mass in payload["masses"]:
                if mass["key"] in REVIEWED_RECIPIENTS:
                    mass["notes"] = mass["notes"].split("The Collect", 1)[0]
        rows = derive_rows(changed, self.correction_evidence)
        self.assertEqual(rows, self.expected)
        self.assertEqual(
            {row["mass_key"] for row in rows if row["wrong_edition_evidence"]},
            {row["mass_key"] for row in self.expected if row["wrong_edition_evidence"]},
        )
        unrelated_output = copy.deepcopy(self.rows)
        for row in unrelated_output:
            row["wrong_edition_evidence"] = False
        self.assertNotEqual(rows, unrelated_output)
        self.assertEqual(derive_rows(changed, self.correction_evidence), rows)

    def test_martha_historical_reading_recovery_is_independent_of_current_prose(self) -> None:
        changed = copy.deepcopy(self.calendar)
        mass = next(mass for payload in changed["sections"].values()
                    for mass in payload["masses"] if mass["key"] == "saints-martha-mary-lazarus")
        mass.pop("notes")
        self.assertEqual(derive_rows(changed, self.correction_evidence), self.expected)
        row = _martha_ordo_row(changed, self.correction_evidence)
        self.assertEqual(row["heading"], "De Communi sanctarum")
        self.assertEqual(row["evidence_scope"], "lectionary-readings")
        self.assertFalse(row["wrong_edition_evidence"])
        self.assertFalse(row["target_formulary_body_authority"])
        self.assertFalse(row["resolvable"])
        self.assertFalse(row["alternatives"])
        self.assertEqual(sum(proper.get("ordinary_disposition", {}).get("group") == "gospel"
                             for proper in mass["propers"]), 2)

    def test_martha_refuses_recipient_reading_or_held_role_changes(self) -> None:
        for mutation in ("missing", "duplicate", "registry", "date", "title", "rank",
                         "section", "common_from", "takes_from", "forms", "default",
                         "reading-missing", "reading-verse", "gospel-choice", "held-missing",
                         "held-body", "held-source", "held-status", "formulary-complete"):
            changed = copy.deepcopy(self.calendar)
            masses = changed["sections"]["sanctoral"]["masses"]
            mass = next(mass for mass in masses if mass["key"] == "saints-martha-mary-lazarus")
            reading = next(proper for proper in mass["propers"] if proper.get("source") == "scripture")
            collect = next(proper for proper in mass["propers"] if proper["name"] == "Collect")
            if mutation == "missing":
                masses.remove(mass)
            elif mutation == "duplicate":
                masses.append(copy.deepcopy(mass))
            elif mutation in {"registry", "date", "rank"}:
                mass[mutation] = "unreviewed"
            elif mutation == "title":
                mass["name"] = "Saint Martha"
            elif mutation == "section":
                masses.remove(mass)
                changed["sections"]["marian"]["masses"].append(mass)
            elif mutation in {"common_from", "takes_from", "forms", "default"}:
                mass[mutation] = "unreviewed"
            elif mutation == "reading-missing":
                mass["propers"].remove(reading)
            elif mutation == "reading-verse":
                reading["verses"][0]["ref"] = "unreviewed"
            elif mutation == "gospel-choice":
                gospel = next(proper for proper in mass["propers"] if proper.get("ordinary_disposition"))
                gospel.pop("ordinary_disposition")
            elif mutation == "held-missing":
                mass["propers"].remove(collect)
            elif mutation == "held-body":
                collect["text"] = "Unreviewed body"
            elif mutation == "held-source":
                collect["text_status"]["reasons"][0]["source_id"] = EDITION_2008
            elif mutation == "held-status":
                collect["text_status"]["body_status"] = "available"
            else:
                mass["text_status"]["state"] = "complete"
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(AssertionError, "invalid correction evidence"):
                    derive_rows(changed, self.correction_evidence)

    def test_martha_refuses_missing_cross_book_or_wrong_era_evidence(self) -> None:
        for mutation in ("missing-contract", "hours-heading", "modern-source-title", "missal-scope",
                         "wrong-page", "wrong-number", "wrong-readings-hash", "missing-record",
                         "wrong-ordo-edition", "wrong-ordo-bytes", "unverified-boundaries",
                         "wrong-book-locus", "shortened-boundary", "wrong-title-artifact"):
            changed = copy.deepcopy(self.correction_evidence)
            case, records = changed["contract"]["martha_lectionary"], changed["records"]
            if mutation == "missing-contract":
                changed["contract"].pop("martha_lectionary")
            elif mutation in {"hours-heading", "modern-source-title", "missal-scope", "wrong-page",
                               "wrong-number", "wrong-readings-hash"}:
                field, value = {
                    "hours-heading": ("raw_common_heading", "De Communi sanctorum."),
                    "modern-source-title": ("source_title", "Saints Martha, Mary, and Lazarus"),
                    "missal-scope": ("source_scope", "missal-formulary"),
                    "wrong-page": ("artifact_page", 353),
                    "wrong-number": ("entry_number", "608"),
                    "wrong-readings-hash": ("reading_nodes_sha256", "0" * 64),
                }[mutation]
                case[field] = value
            elif mutation == "missing-record":
                records.pop("martha-title-authority")
            elif mutation == "wrong-ordo-edition":
                records["martha-ordo"]["edition_id"] = EDITION_2008
            elif mutation == "wrong-ordo-bytes":
                records["martha-ordo"]["sha256"] = "0" * 64
            elif mutation == "unverified-boundaries":
                records["martha-book-boundaries"]["states"] = ["cataloged"]
            elif mutation == "wrong-book-locus":
                records["martha-book-boundaries"]["locus"] = "hours/common-referral"
            elif mutation == "shortened-boundary":
                records["martha-book-boundaries"]["artifact_page_ranges"] = [[2, 2]]
            else:
                records["martha-title-authority"]["artifact_id"] = records["martha-ordo"]["id"]
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(AssertionError, "invalid correction evidence"):
                    derive_rows(self.calendar, changed)

    def test_corrections_refuse_missing_or_changed_recipients_and_body_authority(self) -> None:
        for key in REVIEWED_RECIPIENTS:
            for mutation in ("missing", "duplicate", "registry", "date", "section",
                             "gap", "latin-status", "latin-body", "duplicate-collect"):
                changed = copy.deepcopy(self.calendar)
                masses = changed["sections"]["sanctoral"]["masses"]
                mass = next(mass for mass in masses if mass["key"] == key)
                collect = next(proper for proper in mass["propers"] if proper["name"] == "Collect")
                if mutation == "missing":
                    masses.remove(mass)
                elif mutation == "duplicate":
                    masses.append(copy.deepcopy(mass))
                elif mutation in {"registry", "date"}:
                    mass[mutation] = "unreviewed"
                elif mutation == "section":
                    masses.remove(mass)
                    changed["sections"]["marian"]["masses"].append(mass)
                elif mutation == "gap":
                    mass["text_status"]["reasons"] = []
                elif mutation == "latin-status":
                    collect["text_status"]["state"] = "complete"
                elif mutation == "latin-body":
                    collect["text"] = "Unreviewed body"
                else:
                    mass["propers"].append(copy.deepcopy(collect))
                with self.subTest(mass=key, mutation=mutation):
                    with self.assertRaisesRegex(AssertionError, "invalid correction evidence"):
                        derive_rows(changed, self.correction_evidence)

    def test_corrections_refuse_missing_crossed_or_promoted_sources(self) -> None:
        for mutation in ("missing-case", "duplicate-case", "wrong-recipient", "crossed-comparison",
                         "crossed-historical", "wrong-edition", "wrong-artifact", "wrong-hash",
                         "wrong-page", "unverified", "modern-edition", "public-artifact"):
            changed = copy.deepcopy(self.correction_evidence)
            cases, records = changed["contract"]["corrections"], changed["records"]
            if mutation == "missing-case":
                cases.pop()
            elif mutation == "duplicate-case":
                cases[1] = copy.deepcopy(cases[0])
            elif mutation == "wrong-recipient":
                cases[0]["registry"] = "pc-02-08-bakhita"
            elif mutation == "crossed-comparison":
                cases[0]["comparison"] = cases[1]["comparison"]
            elif mutation == "crossed-historical":
                cases[1]["historical_publication"] = cases[0]["historical_publication"]
            elif mutation == "modern-edition":
                records["comparison-edition"]["id"] = EDITION_2008
            elif mutation == "public-artifact":
                records["comparison-artifact"]["storage"] = "tracked"
            else:
                record = records[cases[0]["comparison"]]
                field, value = {
                    "wrong-edition": ("edition_id", EDITION_2008),
                    "wrong-artifact": ("artifact_id", "artifact.unrelated"),
                    "wrong-hash": ("artifact_sha256", "0" * 64),
                    "wrong-page": ("artifact_page_ranges", [[528, 528]]),
                    "unverified": ("states", ["cataloged", "acquired"]),
                }[mutation]
                record[field] = value
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(AssertionError, "invalid correction evidence"):
                    derive_rows(self.calendar, changed)

    def test_corrections_refuse_modern_english_binding_or_lost_refusal(self) -> None:
        for mutation in ("jerome-exact", "jerome-modern", "jerome-wrong-source",
                         "jerome-duplicate", "jerome-missing", "george-positive",
                         "george-missing", "george-duplicate", "george-wrong-reason",
                         "george-wrong-tuple"):
            changed = copy.deepcopy(self.correction_evidence)
            positives, negatives = changed["english"]["entries"], changed["english"]["untranslated"]
            jerome = next(row for row in positives if row["mass"] == "saint-jerome-emiliani"
                          and row["proper"] == "Collect")
            george = next(row for row in negatives if row["mass"] == "saint-george-martyr"
                          and row["proper"] == "Collect")
            if mutation == "jerome-exact":
                jerome["relation"] = "identical"
            elif mutation == "jerome-modern":
                jerome["witness_relation"] = "target"
            elif mutation == "jerome-wrong-source":
                jerome["publication_passage_id"] = changed["records"]["historical-publication-george"]["id"]
            elif mutation == "jerome-duplicate":
                positives.append(copy.deepcopy(jerome))
            elif mutation == "jerome-missing":
                positives.remove(jerome)
            elif mutation == "george-positive":
                wrong_binding = copy.deepcopy(jerome)
                wrong_binding["mass"] = "saint-george-martyr"
                positives.append(wrong_binding)
            elif mutation == "george-missing":
                negatives.remove(george)
            elif mutation == "george-duplicate":
                negatives.append(copy.deepcopy(george))
            elif mutation == "george-wrong-reason":
                george["reason"] = {"kind": "rights-withheld"}
            else:
                george["cycle"] = "A"
            with self.subTest(mutation=mutation):
                with self.assertRaisesRegex(AssertionError, "invalid correction evidence"):
                    derive_rows(self.calendar, changed)

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

    def test_official_missal_direction_retains_its_source_and_narrow_scope(self) -> None:
        mass = next(mass for payload in self.calendar["sections"].values()
                    for mass in payload["masses"] if mass["key"] == "our-lady-loreto")
        row = _official_missal_row("marian", mass)
        self.assertEqual(row, next(row for row in self.rows
                                  if row["mass_key"] == "our-lady-loreto"))
        self.assertEqual(row["basis"], "official-missal-annex")
        self.assertEqual(row["source_artifact_id"], LORETO_SOURCE_ID)
        self.assertEqual(row["evidence_scope"], "missal-antiphons")
        self.assertFalse(row["resolvable"])
        with self.assertRaisesRegex(AssertionError, "invalid Antiphonary source"):
            _antiphonary_row("marian", mass)

    def test_official_missal_direction_refuses_unreviewed_scope_or_recipient(self) -> None:
        mass = next(mass for payload in self.calendar["sections"].values()
                    for mass in payload["masses"] if mass["key"] == "our-lady-loreto")
        cases = []
        for field, value in (("source_id", ANTIPHONARY_SOURCE_ID),
                             ("scope", "missal-formulary"),
                             ("locus", "unreviewed locator"),
                             ("options", [{"mass": "commune-sanctorum"}])):
            changed = copy.deepcopy(mass)
            changed["common_from"][field] = value
            cases.append(changed)
        for field, value in (("key", "another-memorial"),
                             ("registry", "pc-12-11"), ("date", "12-11")):
            changed = copy.deepcopy(mass)
            changed[field] = value
            cases.append(changed)
        for changed in cases:
            with self.subTest(changed=changed["key"], relation=changed["common_from"]):
                with self.assertRaisesRegex(AssertionError, "unreviewed official Missal direction"):
                    _official_missal_row("marian", changed)

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
            "official_missal_annexes": sum(
                row["basis"] == "official-missal-annex" for row in self.rows
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
                if row["basis"] in {"icel-antiphonary-2010", "official-missal-annex"}:
                    self.assertEqual(row["evidence_scope"], "missal-antiphons")

    def test_registered_witnesses_match_exact_artifacts(self) -> None:
        witnesses = self.inventory["witnesses"]
        for key, path in (
            ("ordo-1981", ORDO_ARTIFACT),
            ("icel-antiphonary-2010", ANTIPHONARY_ARTIFACT),
            ("loreto-2019", LORETO_ARTIFACT),
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
