"""The Roman 1962 finding aid never promotes representation to completeness.

The record checked here is deliberately small and static.  Moving figures are
derived by ``mass-propers census``; this gate owns the evidence paths, closed
limitation vocabulary, edition identities and the absence of copied totals.
"""

from __future__ import annotations

import csv
import hashlib
import json
import tomllib
import unittest
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "src/sources/inventories/roman-1962-finding-aid-coverage-v1.toml"
GUIDE = ROOT / "guidance/liturgy/roman-1962-propers.md"
CATALOG = ROOT / "src/sources/calendars/recensions.json"
ROMAN_TRANSLATIONS = (
    ROOT / "src/sources/inventories/roman-1962-proper-translations-v1.toml"
)
PRE1955_TRANSLATIONS = (
    ROOT / "src/sources/inventories/roman-pre-1955-proper-translations-v1.toml"
)
CUMMISKEY_SOURCE = (
    "edition.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861"
)
CUMMISKEY_PAGE_ARTIFACT = (
    "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861."
    "ia-scan-pdf"
)
CUMMISKEY_PUBLICATION_ARTIFACT = (
    "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861."
    "common-marian-verified-en"
)
CUMMISKEY_PUBLICATION_SHA256 = (
    "1c414c2fb24abd25f211841302a0b4ac95ff89d47a998afbefd2b9a323896851"
)
CUMMISKEY_PALM_PUBLICATION_ARTIFACT = (
    "artifact.eugene-cummiskey.roman-missal-english-laity.philadelphia-1861."
    "palm-sunday-procession-antiphons-en"
)
CUMMISKEY_PALM_PUBLICATION_SHA256 = (
    "95cfd5a0821db3a1c0b9cfbdec21ee3898f9c844dd26dc2db28683010a3b55ae"
)
LASANCE_SOURCE = (
    "edition.francis-xavier-lasance.the-new-roman-missal.benziger-revised-1945"
)
WITHHELD_SURFACES = [
    "site-display",
    "corpus-data",
    "public-git",
    "command-line",
    "download",
]

TARGET_EDITION = (
    ROOT
    / "src/sources/works/catholic-church/missale-romanum/editions"
    / "vatican-typica-1962/edition.toml"
)
TARGET_ARTIFACT = (
    TARGET_EDITION.parent / "artifacts/cmaa-facsimile-pdf/artifact.toml"
)
CUMMISKEY_EDITION = (
    ROOT
    / "src/sources/works/eugene-cummiskey/roman-missal-english-laity/editions"
    / "philadelphia-1861/edition.toml"
)
CUMMISKEY_PUBLICATION_TSV = (
    CUMMISKEY_EDITION.parent
    / "artifacts/common-marian-verified-en/common-marian-verified-en.tsv"
)
CUMMISKEY_PALM_PUBLICATION_TSV = (
    CUMMISKEY_EDITION.parent
    / "artifacts/palm-sunday-procession-antiphons-en/"
    "palm-sunday-procession-antiphons-en.tsv"
)
CUMMISKEY_RECOVERED_PUBLICATION_TSV = (
    CUMMISKEY_EDITION.parent
    / "artifacts/roman-1962-recovered-en/roman-1962-recovered-en.tsv"
)
ANTECEDENT_EDITION = (
    ROOT
    / "src/sources/works/catholic-church/missale-romanum/editions"
    / "vatican-typica-1920/edition.toml"
)

TOP_FIELDS = {
    "schema",
    "record_type",
    "recension_id",
    "calendar",
    "target_edition_id",
    "target_artifact_id",
    "as_of",
    "status",
    "completeness_claim",
    "central_catalog",
    "finding_aid",
    "rights_record",
    "accounting",
    "evidence",
    "limitations",
    "source_requirements",
}
DOMAINS = {
    "propers",
    "commons",
    "ordinary",
    "translations",
    "provenance",
    "rights",
}
LIMITATION_KINDS = {
    "scope-exclusion",
    "data-transcription",
    "page-image-collation",
    "provenance-gap",
    "rights-restriction",
}
ACCOUNTING_DIMENSIONS = {
    "represented-masses",
    "represented-proper-records",
    "direct-proper-records",
    "placeholder-proper-records",
    "mass-reference-records",
    "proper-reference-records",
    "resolved-proper-occurrences",
    "direct-resolved-occurrences",
    "referenced-resolved-occurrences",
    "masses-resolving-no-propers",
    "resolution-errors",
}


def load(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def values(value):
    """Every nested value, so a hand-entered numeric total cannot hide."""
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from values(child)
    elif isinstance(value, list):
        for child in value:
            yield from values(child)


def load_mass_propers():
    loader = SourceFileLoader(
        "roman_finding_aid_mass_propers", str(ROOT / "tools/mass-propers")
    )
    spec = spec_from_loader(loader.name, loader)
    assert spec is not None
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


class Roman1962FindingAidTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = load(RECORD)

    def test_the_record_names_the_supported_identity_and_target_witness(self) -> None:
        self.assertEqual(set(self.record), TOP_FIELDS)
        self.assertEqual(
            self.record["schema"], "triptych-roman-1962-finding-aid-coverage/v1"
        )
        self.assertEqual(self.record["record_type"], "roman-1962-finding-aid-coverage")
        self.assertEqual(self.record["recension_id"], "roman-1962")
        self.assertEqual(self.record["calendar"], "roman-1962")
        self.assertEqual(self.record["status"], "partial")
        self.assertEqual(self.record["completeness_claim"], "not-established")

        edition = load(TARGET_EDITION)
        artifact = load(TARGET_ARTIFACT)
        self.assertEqual(self.record["target_edition_id"], edition["id"])
        self.assertEqual(self.record["target_artifact_id"], artifact["id"])
        self.assertEqual(artifact["edition_id"], edition["id"])

    def test_the_central_catalog_points_to_this_record_as_a_finding_aid(self) -> None:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        rows = [
            row
            for row in catalog["recensions"]
            if row.get("id") == self.record["recension_id"]
        ]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["calendar"], self.record["calendar"])
        self.assertEqual(
            row["coverage_ref"]["propers"], RECORD.relative_to(ROOT).as_posix()
        )
        self.assertEqual(
            row["capabilities"]["propers"],
            {
                "data_availability": "partial",
                "publication_availability": "partial",
                "collation": "finding-aid",
            },
        )

    def test_accounting_is_derived_and_carries_no_moving_totals(self) -> None:
        accounting = self.record["accounting"]
        self.assertEqual(
            set(accounting), {"command", "mode", "dimensions", "interpretation"}
        )
        self.assertEqual(accounting["command"], "tools/tpt mass-propers census --json")
        self.assertEqual(accounting["mode"], "derived-only")
        self.assertEqual(set(accounting["dimensions"]), ACCOUNTING_DIMENSIONS)
        self.assertEqual(len(accounting["dimensions"]), len(ACCOUNTING_DIMENSIONS))
        self.assertFalse(
            any(
                isinstance(value, (int, float)) and not isinstance(value, bool)
                for value in values(self.record)
            ),
            "finding-aid coverage records carry semantics and evidence, never copied totals",
        )
        for key in self.record:
            self.assertNotIn(key, {"count", "counts", "total", "totals"})

    def test_every_evidence_row_is_bounded_and_replayable(self) -> None:
        expected = {
            "seasonal-scripture-citation-collation",
            "sanctoral-common-pointer-recovery",
            "ordinary-frame-and-historical-witness",
            "historical-english-proper-witnesses",
            "target-edition-rights-analysis",
        }
        editions = {
            load(TARGET_EDITION)["id"],
            load(CUMMISKEY_EDITION)["id"],
        }
        artifacts = {load(TARGET_ARTIFACT)["id"]}
        rows = self.record["evidence"]
        self.assertEqual({row["id"] for row in rows}, expected)
        self.assertEqual(len(rows), len(expected))
        for row in rows:
            with self.subTest(row=row["id"]):
                self.assertEqual(
                    set(row),
                    {
                        "id",
                        "domains",
                        "grade",
                        "edition_ids",
                        "artifact_ids",
                        "record",
                        "establishes",
                        "does_not_establish",
                    },
                )
                self.assertTrue(set(row["domains"]) <= DOMAINS)
                self.assertIn(row["grade"], {"page-image", "mixed", "policy"})
                self.assertTrue(set(row["edition_ids"]) <= editions)
                self.assertTrue(set(row["artifact_ids"]) <= artifacts)
                self.assertTrue((ROOT / row["record"]).is_file(), row["record"])
                self.assertTrue(row["establishes"].strip())
                self.assertTrue(row["does_not_establish"].strip())

    def test_every_open_limitation_has_a_typed_requirement(self) -> None:
        expected = {
            "expected-universe-not-modeled",
            "represented-is-not-full-text",
            "commons-and-proper-orations-remain-held",
            "ordinary-not-target-collated",
            "proper-level-target-attestation-missing",
            "target-edition-modern-matter",
            "icel-does-not-supply-historical-english",
        }
        rows = self.record["limitations"]
        self.assertEqual({row["id"] for row in rows}, expected)
        self.assertEqual(len(rows), len(expected))
        for row in rows:
            with self.subTest(row=row["id"]):
                self.assertEqual(
                    set(row),
                    {
                        "id",
                        "domains",
                        "kind",
                        "status",
                        "basis",
                        "requirement",
                        "source_refs",
                    },
                )
                self.assertTrue(set(row["domains"]) <= DOMAINS)
                self.assertIn(row["kind"], LIMITATION_KINDS)
                self.assertEqual(row["status"], "open")
                self.assertTrue(row["basis"].strip())
                self.assertTrue(row["requirement"].strip())
                self.assertTrue(row["source_refs"])
                for path in row["source_refs"]:
                    self.assertTrue((ROOT / path).is_file(), path)

    def test_source_requirements_distinguish_held_bytes_from_missing_artifacts(self) -> None:
        expected = {
            "target-vatican-typica-1962": "registered-remote-collation-required",
            "identified-1920-typical-impression": "artifact-required",
            "restored-holy-week-1956": "edition-and-artifact-registration-required",
        }
        rows = self.record["source_requirements"]
        self.assertEqual({row["id"]: row["status"] for row in rows}, expected)
        self.assertEqual(len(rows), len(expected))
        registered_editions = {
            load(TARGET_EDITION)["id"],
            load(ANTECEDENT_EDITION)["id"],
        }
        registered_artifacts = {load(TARGET_ARTIFACT)["id"]}
        for row in rows:
            with self.subTest(row=row["id"]):
                self.assertEqual(
                    set(row),
                    {
                        "id",
                        "domains",
                        "edition_identity",
                        "edition_id",
                        "artifact_id",
                        "status",
                        "requirement",
                    },
                )
                self.assertTrue(set(row["domains"]) <= DOMAINS)
                self.assertTrue(row["edition_identity"].strip())
                self.assertTrue(row["requirement"].strip())
                if row["edition_id"]:
                    self.assertIn(row["edition_id"], registered_editions)
                if row["artifact_id"]:
                    self.assertIn(row["artifact_id"], registered_artifacts)

    def test_the_profile_points_to_the_record_and_refuses_inference(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        self.assertIn(RECORD.relative_to(ROOT).as_posix(), guide)
        self.assertIn("tools/tpt mass-propers census --json", guide)
        self.assertIn("Never fill the difference by inference or generated text.", guide)


class HistoricalEnglishAccountingTest(unittest.TestCase):
    """Exact gaps and recension departures close without supplying text."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.base = load(ROMAN_TRANSLATIONS)
        cls.child = load(PRE1955_TRANSLATIONS)

    @staticmethod
    def identity(row: dict) -> tuple[str, str, str, str, int]:
        return (
            row["mass"],
            row["form_id"],
            row["proper"],
            row["cycle"],
            row["occurrence"],
        )

    @staticmethod
    def main_identities(
        rows: dict[str, set[str]],
    ) -> set[tuple[str, str, str, str, int]]:
        return {
            (mass, "main", proper, "all", 1)
            for mass, propers in rows.items()
            for proper in propers
        }

    @classmethod
    def source_established_unavailable_identities(
        cls,
    ) -> set[tuple[str, str, str, str, int]]:
        propers = load_mass_propers()
        document = propers.load_calendar(
            ROOT / "src" / "sources" / "calendars",
            "roman-1962",
            effective=False,
        )
        target_artifact_id = load(TARGET_ARTIFACT)["id"]
        identities: set[tuple[str, str, str, str, int]] = set()

        for section in document["sections"].values():
            for mass in section["masses"]:
                groups = [("main", mass.get("propers", []))]
                groups.extend(
                    (str(form["id"]), form.get("propers", []))
                    for form in mass.get("forms", [])
                )
                for form_id, proper_rows in groups:
                    occurrences: dict[str, int] = {}
                    for proper in proper_rows:
                        name = proper["name"]
                        occurrences[name] = occurrences.get(name, 0) + 1
                        status = proper.get("text_status") or {}
                        if (
                            status.get("state") == "unavailable"
                            and status.get("scope") == "proper-body"
                            and any(
                                reason.get("kind") == "witness-gap"
                                and reason.get("source_id") == target_artifact_id
                                for reason in status.get("reasons", [])
                                if isinstance(reason, dict)
                            )
                        ):
                            identities.add(
                                (
                                    mass["key"],
                                    form_id,
                                    name,
                                    "all",
                                    occurrences[name],
                                )
                            )

        return identities

    @classmethod
    def exact_gap_identities(cls) -> set[tuple[str, str, str, str, int]]:
        identities = cls.main_identities(
            {
                "s-hilarii-episcopi-confessoris-ecclesiae-doctoris": {
                    "Collect",
                    "Secret",
                    "Postcommunion",
                },
                "s-ioannis-mariae-vianney-confessoris": {"Collect"},
                "commune-summorum-pontificum": {
                    "Collect (in plurali)",
                    "Collect (Altera oratio, in plurali)",
                    "Postcommunion (in plurali)",
                    "Collect (Altera oratio)",
                    "Secret",
                    "Secret (Altera secreta)",
                    "Postcommunion",
                    "Postcommunion (Altera postcommunio)",
                },
                "commune-non-virginum-1": {
                    "Collect",
                    "Secret",
                    "Postcommunion",
                    "Collect (Pro pluribus Martyribus quae non sint Virgines)",
                    "Secret (Pro pluribus Martyribus quae non sint Virgines)",
                },
                "palm-sunday": {
                    "Hymn to Christ the King",
                    "Oration to Conclude the Procession",
                },
                "mass-of-the-lords-supper": {
                    "Mandatum Antiphon 8",
                    "Prayer of the Mandatum",
                    "Hymn at the Translation of the Blessed Sacrament",
                },
                "good-friday": {
                    "Prayer after the Prostration",
                    "Solemn Intercessions",
                    "Antiphons at the Translation of the Blessed Sacrament",
                    "First Prayer after Communion",
                    "Second Prayer after Communion",
                    "Third Prayer after Communion",
                },
                "easter-vigil": {
                    "Blessing of the Paschal Candle",
                    "Blessing of the Lighted Candle",
                    "Exsultet (Praeconium paschale)",
                    "Litany of the Saints, first part",
                    "Prayer at the Font",
                    "Renewal of Baptismal Promises",
                    "Litany of the Saints, second part",
                },
                "comm-s-telesphori-papae-martyris": {
                    "Collect",
                    "Secret",
                    "Postcommunion",
                },
                "comm-s-hygini-papae-martyris": {
                    "Collect",
                    "Secret",
                    "Postcommunion",
                },
                "comm-s-sabinae-martyris": {"Collect"},
                "ss-cornelii-papae-cypriani-episcopi-martyrum": {"Collect"},
                "comm-ss-placidi-sociorum-martyrum": {
                    "Collect",
                    "Postcommunion",
                },
                "comm-s-mennae-martyris": {"Collect"},
                "comm-s-sabbae-abbatis": {"Collect"},
                "comm-s-silvestri-i-papae-confessoris": {"Collect"},
                "comm-s-bonifatii-martyris": {"Postcommunion"},
                "comm-ss-symphorosae-septem-eius-filiorum": {
                    "Collect",
                    "Postcommunion",
                },
                "comm-ss-xysti-ii-papae-felicissimi": {"Collect"},
                "comm-s-eusebii-confessoris": {"Collect"},
                "comm-ss-cypriani-iustinae-virginis-martyrum": {
                    "Postcommunion"
                },
                "commune-dedicationis-ecclesiae": {
                    "Gradual",
                    "Alleluia (Tempore paschali)",
                },
                "commune-festorum-bmv": {
                    "Introit",
                    "Alleluia (Tempore paschali)",
                    "Communion",
                },
                "commune-virginum-4": {
                    "Alleluia (Tempore paschali)",
                },
                "missa-de-s-maria-in-sabbato-4": {
                    "Introit",
                    "Communion",
                },
            }
        )
        identities |= {
            ("palm-sunday", "main", "Procession Antiphon", "all", occurrence)
            for occurrence in (5, 6, 7)
        }
        identities |= {
            (
                "commemoratione-omnium-fidelium-defunctorum",
                form,
                proper,
                "all",
                1,
            )
            for form in ("second", "third")
            for proper in ("Collect", "Secret", "Postcommunion")
        }
        identities |= cls.source_established_unavailable_identities()
        return identities

    @classmethod
    def exact_publication_bound_identities(
        cls,
    ) -> set[tuple[str, str, str, str, int]]:
        return {
            cls.identity(row)
            for row in cls.base["entries"]
            if any(
                translation.get("source_id") == CUMMISKEY_SOURCE
                for translation in row.get("translations") or []
            )
        }

    @classmethod
    def exact_child_exclusions(
        cls,
    ) -> set[tuple[str, tuple[str, str, str, str, int]]]:
        entries = cls.main_identities(
            {
                "palm-sunday": {
                    "Blessing of the Palms",
                    "Collect",
                    "First Antiphon at the Distribution of Palms",
                    "Postcommunion",
                    "Responsory at the Entrance into the Church",
                    "Second Antiphon at the Distribution of Palms",
                    "Secret",
                    "Versicle at the Beginning of the Procession",
                },
                "good-friday": {"Collect", "Improperia", "Showing of the Cross"},
                "easter-vigil": {
                    "Blessing of the Baptismal Water",
                    "Blessing of the New Fire",
                    "Collect",
                    "Lumen Christi",
                    "Oration after the First Prophecy",
                    "Oration after the Fourth Prophecy",
                    "Oration after the Second Prophecy",
                    "Oration after the Third Prophecy",
                    "Postcommunion",
                    "Secret",
                },
            }
        )
        absent = cls.main_identities(
            {
                "palm-sunday": {
                    "Hymn to Christ the King",
                    "Oration to Conclude the Procession",
                },
                "good-friday": {
                    "Antiphons at the Translation of the Blessed Sacrament",
                    "First Prayer after Communion",
                    "Prayer after the Prostration",
                    "Second Prayer after Communion",
                    "Solemn Intercessions",
                    "Third Prayer after Communion",
                },
                "easter-vigil": {
                    "Blessing of the Lighted Candle",
                    "Blessing of the Paschal Candle",
                    "Exsultet (Praeconium paschale)",
                    "Litany of the Saints, first part",
                    "Litany of the Saints, second part",
                    "Prayer at the Font",
                    "Renewal of Baptismal Promises",
                },
            }
        )
        absent |= {
            ("palm-sunday", "main", "Procession Antiphon", "all", occurrence)
            for occurrence in (5, 6, 7)
        }
        absent |= cls.main_identities(
            {"chrism-mass": {"Collect", "Secret", "Postcommunion"}}
        )
        absent |= cls.main_identities(
            {
                "s-ioseph-opificis-sponsi-beatae-mariae": {
                    "Collect",
                    "Secret",
                    "Postcommunion",
                }
            }
        )
        affected = entries | absent
        affected |= {
            ("palm-sunday", "main", "Procession Antiphon", "all", occurrence)
            for occurrence in (1, 2, 3)
        }
        positive = {
            (
                row["mass"],
                row.get("form_id", "main"),
                row["proper"],
                row.get("cycle", "all"),
                row.get("occurrence", 1),
            )
            for row in cls.base["entries"]
        }
        unavailable = {cls.identity(row) for row in cls.base["untranslated"]}
        if missing := affected - positive - unavailable:
            raise AssertionError(f"child exclusion targets missing from parent: {missing!r}")
        return {
            ("entry" if identity in positive else "untranslated", identity)
            for identity in affected
        }

    def test_historical_english_gaps_are_an_exact_typed_text_free_set(self) -> None:
        expected = self.exact_gap_identities()
        source_established = self.source_established_unavailable_identities()
        typed = {
            self.identity(row): row
            for row in self.base["untranslated"]
            if isinstance(row.get("reason"), dict)
        }
        self.assertEqual(len(source_established), 666)
        self.assertEqual(len(expected), 737)
        self.assertTrue(expected.issubset(typed))
        quarantined = set(typed) - expected
        self.assertEqual(len(quarantined), 360)
        self.assertEqual(
            {
                (
                    typed[identity]["reason"]["kind"],
                    typed[identity]["reason"].get("source_id"),
                ): sum(
                    1
                    for candidate in quarantined
                    if (
                        typed[candidate]["reason"]["kind"],
                        typed[candidate]["reason"].get("source_id"),
                    )
                    == (
                        typed[identity]["reason"]["kind"],
                        typed[identity]["reason"].get("source_id"),
                    )
                )
                for identity in quarantined
            },
            {
                ("rights-withheld", CUMMISKEY_SOURCE): 348,
                ("witness-gap", CUMMISKEY_SOURCE): 12,
            },
        )
        self.assertEqual(len(typed), len(self.base["untranslated"]))
        rights_withheld = self.main_identities(
            {
                "commune-summorum-pontificum": {
                    "Collect (Altera oratio)",
                    "Secret",
                    "Secret (Altera secreta)",
                    "Postcommunion",
                    "Postcommunion (Altera postcommunio)",
                },
                "palm-sunday": {"Hymn to Christ the King"},
                "mass-of-the-lords-supper": {
                    "Mandatum Antiphon 8",
                    "Prayer of the Mandatum",
                    "Hymn at the Translation of the Blessed Sacrament",
                },
            }
        )
        lasance_witness_gap = self.main_identities(
            {"s-ioannis-mariae-vianney-confessoris": {"Collect"}}
        )
        for identity in expected:
            with self.subTest(identity=identity):
                row = typed[identity]
                required = {
                    "mass",
                    "form_id",
                    "proper",
                    "cycle",
                    "occurrence",
                    "lang",
                    "extent",
                    "availability",
                    "reason",
                    "note",
                }
                witness_fields = {
                    "witness_artifact_id",
                    "witness_passage_id",
                    "verified_artifact_page",
                    "verified_on_page",
                    "verified_printed_page",
                    "verified_heading",
                    "verified_url",
                }
                self.assertTrue(required.issubset(row))
                self.assertTrue(set(row).issubset(required | witness_fields))
                if set(row) & witness_fields:
                    self.assertTrue(
                        {
                            "witness_artifact_id",
                            "witness_passage_id",
                            "verified_artifact_page",
                            "verified_on_page",
                        }.issubset(row)
                    )
                self.assertEqual(row["availability"], "unavailable")
                self.assertEqual(row["lang"], "en")
                self.assertEqual(row["extent"], "body")
                self.assertNotIn("text", row)
                if identity in source_established:
                    self.assertEqual(row["reason"], {"kind": "no-exemplar"})
                elif identity in quarantined:
                    if row["reason"]["kind"] == "rights-withheld":
                        self.assertEqual(
                            row["reason"],
                            {
                                "kind": "rights-withheld",
                                "source_id": CUMMISKEY_SOURCE,
                                "surfaces": WITHHELD_SURFACES,
                            },
                        )
                    else:
                        self.assertEqual(
                            row["reason"],
                            {"kind": "witness-gap", "source_id": CUMMISKEY_SOURCE},
                        )
                elif identity in rights_withheld:
                    self.assertEqual(
                        row["reason"],
                        {
                            "kind": "rights-withheld",
                            "source_id": LASANCE_SOURCE,
                            "surfaces": WITHHELD_SURFACES,
                        },
                    )
                elif identity in lasance_witness_gap:
                    self.assertEqual(
                        row["reason"],
                        {"kind": "witness-gap", "source_id": LASANCE_SOURCE},
                    )
                else:
                    self.assertEqual(
                        row["reason"],
                        {"kind": "witness-gap", "source_id": CUMMISKEY_SOURCE},
                    )
                self.assertTrue(row["note"].strip())

    def test_cummiskey_publication_bindings_cover_every_deliberate_positive(
        self,
    ) -> None:
        expected = self.exact_publication_bound_identities()
        bound = {
            self.identity(row): row
            for row in self.base["entries"]
            if any(
                translation.get("source_id") == CUMMISKEY_SOURCE
                for translation in row.get("translations") or []
            )
            and "publication_artifact_id" in row
        }
        self.assertEqual(len(expected), 60)
        self.assertEqual(set(bound), expected)
        self.assertTrue(expected.isdisjoint(self.exact_gap_identities()))
        self.assertEqual(
            hashlib.sha256(CUMMISKEY_PUBLICATION_TSV.read_bytes()).hexdigest(),
            CUMMISKEY_PUBLICATION_SHA256,
        )
        self.assertEqual(
            hashlib.sha256(CUMMISKEY_PALM_PUBLICATION_TSV.read_bytes()).hexdigest(),
            CUMMISKEY_PALM_PUBLICATION_SHA256,
        )
        publication_paths = (
            CUMMISKEY_PUBLICATION_TSV,
            CUMMISKEY_PALM_PUBLICATION_TSV,
            CUMMISKEY_RECOVERED_PUBLICATION_TSV,
        )
        publication_artifacts = {
            load(path.parent / "artifact.toml")["id"]: load(
                path.parent / "artifact.toml"
            )
            for path in publication_paths
        }
        source_rows = {}
        recovered_rows = []
        for path in publication_paths:
            with path.open(encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle, delimiter="\t"):
                    identity = (
                        row["mass"],
                        row["form_id"],
                        row["proper"],
                        row.get("cycle") or "all",
                        int(row.get("occurrence") or 1),
                    )
                    self.assertNotIn(identity, source_rows)
                    source_rows[identity] = row
                    if path == CUMMISKEY_RECOVERED_PUBLICATION_TSV:
                        recovered_rows.append(row)
        self.assertEqual(len(recovered_rows), 106)
        self.assertEqual(
            hashlib.sha256(CUMMISKEY_RECOVERED_PUBLICATION_TSV.read_bytes()).hexdigest(),
            publication_artifacts[
                "artifact.eugene-cummiskey.roman-missal-english-laity."
                "philadelphia-1861.roman-1962-recovered-en"
            ]["sha256"],
        )
        rejected_candidate = (
            "commune-dedicationis-ecclesiae",
            "main",
            "Gradual",
            "all",
            1,
        )
        self.assertTrue(expected.issubset(source_rows))
        self.assertNotIn(rejected_candidate, bound)
        recovered_identities = {
            (
                row["mass"],
                row["form_id"],
                row["proper"],
                row.get("cycle") or "all",
                int(row.get("occurrence") or 1),
            )
            for row in recovered_rows
        }
        self.assertEqual(len(recovered_identities & expected), 48)
        self.assertEqual(len(recovered_identities - expected), 58)

        sources = [
            row for row in self.base["sources"] if row["id"] == "cummiskey-1861"
        ]
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0]["source_id"], CUMMISKEY_SOURCE)
        self.assertTrue(sources[0]["caution"].strip())

        propers = load_mass_propers()
        for identity in expected:
            with self.subTest(identity=identity):
                row = bound[identity]
                source = source_rows[identity]
                self.assertEqual(row["incipit"], source["latin_incipit"])
                self.assertEqual(row["printed_page"], source["printed_page"])
                leaf_range = [
                    int(value) for value in source["ia_leaf_range"].split("-")
                ]
                self.assertEqual(row["ia_leaf_range"], leaf_range)
                self.assertEqual(row["ia_leaf"], leaf_range[0])
                self.assertEqual(row["witness"], "cummiskey-1861")
                self.assertEqual(row["artifact_id"], CUMMISKEY_PAGE_ARTIFACT)
                publication_artifact = publication_artifacts[
                    row["publication_artifact_id"]
                ]
                self.assertEqual(
                    row["publication_artifact_sha256"],
                    publication_artifact["sha256"],
                )
                propers.validate_translation_publication_binding(
                    row, propers.DEFAULT_ROOT, ROMAN_TRANSLATIONS
                )
                self.assertEqual(row["collation_result"], "confirmed")
                self.assertEqual(len(row["translations"]), 1)
                translation = row["translations"][0]
                self.assertEqual(
                    set(translation), {"lang", "rights", "source_id", "text"}
                )
                self.assertEqual(translation["lang"], "en")
                self.assertEqual(translation["rights"], "public-domain")
                self.assertEqual(translation["source_id"], CUMMISKEY_SOURCE)
                self.assertEqual(translation["text"], source["english"])

    def test_child_sidecar_excludes_only_exact_typed_inherited_departures(self) -> None:
        rows = self.child["inherited_inapplicable"]
        actual = {(row["record"], self.identity(row)) for row in rows}
        expected = self.exact_child_exclusions()
        self.assertEqual(len(expected), 48)
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), len(rows))
        self.assertEqual({row["record"] for row in rows}, {"entry", "untranslated"})
        self.assertEqual(
            sum(row["record"] == "entry" for row in rows), 13
        )
        self.assertEqual(
            sum(row["record"] == "untranslated" for row in rows), 35
        )
        for row in rows:
            with self.subTest(record=row["record"], identity=self.identity(row)):
                self.assertEqual(
                    set(row),
                    {
                        "record",
                        "mass",
                        "form_id",
                        "proper",
                        "cycle",
                        "occurrence",
                        "reason",
                        "basis",
                    },
                )
                self.assertEqual(
                    row["reason"],
                    "recension-absent"
                    if row["mass"]
                    in {"chrism-mass", "s-ioseph-opificis-sponsi-beatae-mariae"}
                    else "recension-replaced",
                )
                self.assertEqual(row["basis"], "calendar-departure")

        self.assertNotIn("entries", self.child)
        self.assertNotIn("untranslated", self.child)

    def test_both_historical_recensions_have_closed_english_accounting(self) -> None:
        propers = load_mass_propers()
        root = ROOT / "src/sources/calendars"
        rows = {
            calendar: propers.english_coverage(root, calendar)
            for calendar in ("roman-1962", "roman-pre-1955")
        }
        for calendar, row in rows.items():
            with self.subTest(calendar=calendar):
                self.assertIsNotNone(row)
                for field in (
                    "unaccounted",
                    "unmatched_records",
                    "stale_translation_records",
                    "outside_the_ledger",
                ):
                    self.assertEqual(row[field], 0)
        self.assertEqual(rows["roman-1962"]["inherited_inapplicable_records"], 0)
        self.assertEqual(
            rows["roman-pre-1955"]["inherited_inapplicable_records"], 48
        )
        self.assertTrue(rows["roman-pre-1955"]["translation_ledger_inherited"])


if __name__ == "__main__":
    unittest.main()
