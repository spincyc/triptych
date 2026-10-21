"""Latin Proper provenance is per text; publication is a separate decision."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import tomllib
import unittest
from importlib.machinery import SourceFileLoader
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import _calendars  # noqa: E402
from _proper_latin import (  # noqa: E402
    CLI_SURFACES,
    POLICY,
    SCHEMA,
    SIDECAR_SUFFIX,
    STRUCTURE_SURFACES,
    SURFACES,
    LatinKey,
    body_owners,
    decision_for,
    publication_records,
    read_sidecar,
    render_unresolved_sidecar,
    sanitize_mass,
    sanitize_proper,
    sidecar_problems,
    text_owners,
    text_sha256,
)


CALENDARS = ROOT / "src/sources/calendars"
INVENTORIES = ROOT / "src/sources/inventories"
EDITORIAL_PROJECTION = (
    ROOT
    / "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection"
)


def registered_artifact(artifact_id: str) -> dict:
    """One source-library artifact record, read from its canonical path."""
    _, work_owner, work, edition, artifact = artifact_id.split(".")
    record = tomllib.loads(
        (
            ROOT
            / "src/sources/works"
            / work_owner
            / work
            / "editions"
            / edition
            / "artifacts"
            / artifact
            / "artifact.toml"
        ).read_text(encoding="utf-8")
    )
    if record.get("id") != artifact_id:
        raise AssertionError(
            f"{artifact_id}: artifact record names {record.get('id')!r}"
        )
    return record


def load_tool(name: str):
    return SourceFileLoader(
        f"test_{name.replace('-', '_')}", str(ROOT / "tools" / name)
    ).load_module()


def demo_document(*propers: dict) -> dict:
    return {
        "schema": "triptych-calendar-masses/v1",
        "calendar": "demo",
        "edition": "Demo",
        "psalm_numbering": "vulgate",
        "sections": {
            "01": {
                "kind": "seasonal",
                "masses": [
                    {
                        "key": "day",
                        "name": "Demo Day",
                        "registry": "d1",
                        "propers": list(propers),
                    }
                ],
            }
        },
    }


def toml_ledger(entry: str, *, defaults: str | None = None) -> str:
    return f'''schema = "{SCHEMA}"
calendar = "demo"
language = "la"
policy = "{POLICY}"

[defaults]
{defaults or '''provenance_status = "unresolved"
publication_status = "unresolved"
publication_basis = "unresolved"
surfaces = []'''}

[[entries]]
mass = "day"
form = ""
proper = "Collect"
course = ""
cycle = ""
occurrence = 1
{entry}
'''


def permitted_nonexact_fields() -> list[str]:
    return [
        'provenance_status = "collated"',
        'source_id = "artifact.target.unresolved"',
        'source_date = "1962"',
        'locator = "p. 1"',
        'relationship = "collated-non-exact"',
        'verification_source_id = "artifact.historical.public-domain"',
        'verification_locator = "p. 1"',
        "transformations = []",
        'provenance_evidence = "Per-text comparison"',
        'provenance_authority = "Human page-image collation"',
        'provenance_confidence = "high"',
        'publication_status = "permitted"',
        'publication_basis = "non-exact-historical-witness"',
        'surfaces = ["web", "download", "print", "cli", "corpus-data", "public-git"]',
        'publication_source_ids = ["artifact.target.unresolved"]',
        'publication_locator = "artifact rights record"',
        'publication_evidence = "Synthetic non-exact claim"',
    ]


class ProductionLedgerTests(unittest.TestCase):
    def test_christmas_three_forms_keep_principal_oration_sources_distinct(self):
        document = _calendars.load_document(CALENDARS, "roman-1962")
        mass = next(row for _, _, row in _calendars.departures_of(document)
                    if row["key"] == "nativitate-domini-octave")
        form_names = {'night': 'Ad primam Missam in nocte', 'dawn': 'Ad secundam Missam in aurora', 'day': 'Ad tertiam Missam in die'}
        expected = {('night', 'Collect'): '43cf746196c66232af49c9d4a1c2f1927e452c82869582052845c2fe1ff8d166', ('night', 'Secret'): 'e7e29c76ab1a0ccf0b8eb4bd35ded4431d55db9e8a9272fbdb1cef93b25528e7', ('night', 'Postcommunion'): '53f6ace4a9b54ab897e13e4e7de8fc6ff97fff5c3f38eb5238d4ce88f0d99c7e', ('dawn', 'Collect'): 'bb56efd1e9a1608c3ee3e4a694011f50736b85d3028d2d01ca6df948bd7872d8', ('dawn', 'Secret'): '7c0c7d86dc2da4c2c0ec3c46de1517efd96080bbd0f15c7128e04e72b122dee2', ('dawn', 'Postcommunion'): '13ca23a543baa7a5891f687119e4c9b9d2c2059a1d46e46c36dfd1b474b126e7', ('day', 'Collect'): '56acab1dd52c97f54e612270f44534e3372c3ad3ffee7fc49f6ce12ec97a54ad', ('day', 'Secret'): '5e684d0b826f149f3cbd875f31c87287990d5fa1bbc4f25f18a5672d9bd18d04', ('day', 'Postcommunion'): '959f01005caf1c72a9e22382504447c8723e6f61b41f818f3a88e7616deda780'}
        self.assertEqual(form_names, {form["id"]: form["name"] for form in mass["forms"]})
        records, problems = read_sidecar(INVENTORIES / "roman-1962-proper-latin-provenance-v1.toml")
        self.assertEqual([], problems)
        seen = set()
        import hashlib
        import copy
        unchanged = copy.deepcopy(mass)
        unchanged.pop("notes", None)
        for form in unchanged["forms"]:
            form["propers"] = [p for p in form["propers"]
                               if p["name"] not in {"Collect", "Secret", "Postcommunion"}]
        self.assertEqual('e9cca9b307fde1df85b16efe33465ac8936d5309cb4fb8d850f9508f1fca68d4',
                         hashlib.sha256(json.dumps(unchanged, ensure_ascii=False, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest())
        for form in mass["forms"]:
            self.assertEqual({'night': ['Introit', 'Collect', 'Epistle', 'Gradual', 'Alleluia', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'dawn': ['Introit', 'Collect', 'Epistle', 'Gradual', 'Alleluia', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'day': ['Introit', 'Collect', 'Epistle', 'Gradual', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion']}[form["id"]], [p["name"] for p in form["propers"]])
            for proper in form["propers"]:
                address = (form["id"], proper["name"])
                if address not in expected:
                    continue
                with self.subTest(form=form["id"], proper=proper["name"]):
                    self.assertEqual(expected[address], text_sha256(proper["text"]))
                    self.assertNotIn("text_status", proper)
                    self.assertFalse({"actor", "speaker", "role"} & set(proper))
                    key = LatinKey("nativitate-domini-octave", form["name"], proper["name"], occurrence=1)
                    row = records[key]
                    self.assertEqual("collated", row["provenance_status"])
                    self.assertEqual("editorial-projection-exact-to-target", row["relationship"])
                    self.assertEqual("public-domain", row["publication_basis"])
                    self.assertEqual("permitted", row["publication_status"])
                    self.assertEqual(set(SURFACES), set(row["surfaces"]))
                    self.assertTrue(row["source_id"].endswith(".christmas-" + form["id"] + "-" + proper["name"].lower()))
                    self.assertEqual('artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.christmas-nine-orations-la-checked-825c69f4', row["publication_source_ids"][1])
                    seen.add(address)
        self.assertEqual(set(expected), seen)
        source = registered_artifact('artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.christmas-nine-orations-la-checked-825c69f4')
        historical = (ROOT / source["path"]).read_text().strip().split("\n\n")
        self.assertEqual(9, len(historical))
        historical_day_collect = " ".join(historical[6].split())
        self.assertTrue(historical_day_collect.endswith("Per eúmdem Dóminum."))
        self.assertNotIn("Amen", historical_day_collect)
        self.assertNotIn("℟", historical_day_collect)
        self.assertIn("Per eúmdem Dñm.", " ".join(historical[3].split()))
        day = next(form for form in mass["forms"] if form["id"] == "day")
        day_collect = next(p["text"] for p in day["propers"] if p["name"] == "Collect")
        self.assertTrue(" ".join(day_collect.split()).endswith(
            "in unitate Spiritus Sancti, Deus: per omnia saecula saeculorum. ℟. Amen."))
        self.assertNotIn("R. Amen.", day_collect)
        historical_day_secret = " ".join(historical[7].split())
        self.assertTrue(historical_day_secret.endswith("Per eúmdem Dóminum nostrum Jesum Christum."))
        day_secret = next(p["text"] for p in day["propers"] if p["name"] == "Secret")
        self.assertTrue(" ".join(day_secret.split()).endswith("Per eundem Dominum."))

    def test_immaculate_feast_bodies_preserve_source_qualification_and_active_order(self):
        document = _calendars.load_document(CALENDARS, "roman-1962")
        mass = next(row for _, _, row in _calendars.departures_of(document)
                    if row["key"] == 'conceptione-immaculata-beatae-mariae-virginis')
        self.assertEqual(["Introit", "Collect", "Lesson", "Gradual", "Alleluia",
                          "Gospel", "Offertory", "Secret", "Communion", "Postcommunion"],
                         [p["name"] for p in mass["propers"]])
        expected = {'Collect': '3dd9b9b0db918ec4f65b9a175e77347c0a54b5875fb874f50ed0bbe636b311f2', 'Secret': '6755a936e24660ef77e7c0ceffba13c28d21a82cc941bf8fb9ba5b57863f31a9', 'Communion': 'e26ba7251680129e9e04187733f30e4601c1479cdc157f20b6d160dbe4007936', 'Postcommunion': 'aa2efdb79676b0a403afaeb0f5bfacd9e9888af5af507f6d0cd09296cf5bf5d0'}
        unchanged = [p for p in mass["propers"] if p["name"] not in expected]
        import hashlib
        self.assertEqual('649063bf9f7a74b95285676bee8f81cd11da10ec8212dd0ad2bf3257c9fa04d9',
                         hashlib.sha256(json.dumps(unchanged, ensure_ascii=False,
                                                   sort_keys=True, separators=(",", ":")).encode()).hexdigest())
        appointed, problems = _calendars.resolve_propers(document, mass)
        self.assertEqual([], problems)
        found = {p["name"]: (p, origin) for _, p, origin in appointed if p["name"] in expected}
        self.assertEqual(set(expected), set(found))
        records, problems = read_sidecar(INVENTORIES / "roman-1962-proper-latin-provenance-v1.toml")
        self.assertEqual([], problems)
        for name, digest in expected.items():
            proper, origin = found[name]
            self.assertIsNone(origin)
            self.assertEqual(digest, text_sha256(proper["text"]))
            self.assertEqual("composed", proper["source"])
            row = records[LatinKey('conceptione-immaculata-beatae-mariae-virginis', "", name, "", "", 1)]
            self.assertEqual(digest, row["text_sha256"])
            self.assertEqual('passage.catholic-church.missale-romanum.vatican-typica-1962.immaculate-conception-selected-feast-four-propers-word-collation-2026-10-20', row["verification_source_id"])
        secret = " ".join(found["Secret"][0]["text"].split())
        self.assertIn("quam in solemnitate immaculatae", secret)
        self.assertNotIn("commemoratione", secret)
        self.assertIn("commemoratione", found["Secret"][0]["notes"])
        self.assertEqual("Gloriosa dicta sunt de te, Maria: quia fecit tibi magna qui potens est.",
                         " ".join(found["Communion"][0]["text"].split()))
        self.assertNotIn("verses", found["Communion"][0])
        historical = registered_artifact('artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.immaculate-conception-four-propers-la-checked-18084e74')
        self.assertEqual('18084e74e99af80af96f5879b9392fa5ab29b84a1cea955eef36604621a14c82', historical["sha256"])
        source = (ROOT / historical["path"]).read_text()
        self.assertIn("Per eumdem Dominum.", source)
        self.assertNotIn("commemoratione", source)
        self.assertTrue(source.rstrip().endswith("Per Dominum."))
        self.assertIn("post Septuagesimam", mass["notes"])
        self.assertIn("Psalm86:1-2,3,5".replace("Psalm86", "Psalm 86"), mass["notes"])
        self.assertIn("not represented", mass["notes"])

    def test_all_saints_own_bodies_keep_order_citations_and_source_boundaries(self):
        document = _calendars.load_document(CALENDARS, "roman-1962")
        mass = next(row for _, _, row in _calendars.departures_of(document)
                    if row["key"] == "omnium-sanctorum")
        self.assertEqual(
            ["Introit", "Collect", "Lesson", "Gradual", "Alleluia", "Gospel",
             "Offertory", "Secret", "Communion", "Postcommunion"],
            [row["name"] for row in mass["propers"]],
        )
        expected = {'Introit': '05d6cd5dae69b6c05a69f9379ebd558836a0a630ab3072cc53cd54db0ae9d68d', 'Collect': 'b858d54df308cea45ae480dc0a715ba730661f8d9af1db5f8875353fc1e4cff0', 'Secret': '0f451845add633adda1c7fa6c23fe6332715561e5e21404b631b4c94e760c22a', 'Postcommunion': 'c64fbf6c5e2927c2ebb150c3a83ee0936a225bd459845b06da2fab85fe83eb21'}
        unchanged = [row for row in mass["propers"] if row["name"] not in expected]
        import hashlib
        self.assertEqual(
            '8a3a65633b4ed48cc631001e526a392ea7969fb000071a79fc5bcb23b1345c6e',
            hashlib.sha256(json.dumps(unchanged, ensure_ascii=False, sort_keys=True,
                                      separators=(",", ":")).encode()).hexdigest(),
        )
        appointed, problems = _calendars.resolve_propers(document, mass)
        self.assertEqual([], problems)
        found = {p["name"]: (p, origin) for _, p, origin in appointed
                 if p["name"] in expected}
        self.assertEqual(set(expected), set(found))
        for name, digest in expected.items():
            proper, origin = found[name]
            self.assertIsNone(origin, name)
            self.assertEqual(digest, text_sha256(proper["text"]))
            self.assertNotIn("text_status", proper)
        introit = found["Introit"][0]
        self.assertEqual("mixed", introit["source"])
        self.assertEqual([{"book": "Psalms", "ranges": [{
            "begin": {"chapter": 32, "verse": 1},
            "end": {"chapter": 32, "verse": 1}}], "ref": "Psalms 32:1"}],
            introit["verses"])
        self.assertTrue(introit["text"].startswith("Gaudeamus omnes in Domino"))
        self.assertTrue(introit["text"].rstrip().endswith("V. Gloria Patri."))
        self.assertNotIn("Sicut erat", introit["text"])
        self.assertNotIn("Judicant Sancti", introit["text"])
        for name in ("Collect", "Secret"):
            self.assertTrue(" ".join(found[name][0]["text"].split())
                            .endswith("Per Dominum."))
        self.assertTrue(" ".join(found["Postcommunion"][0]["text"].split())
                        .endswith("Per Dominum nostrum."))

    def test_theodore_own_orations_do_not_fall_back_to_common_prayers(self):
        document = _calendars.load_document(CALENDARS, "roman-1962")
        mass = next(row for _, _, row in _calendars.departures_of(document)
                    if row["key"] == "comm-s-theodori-martyris")
        appointed, problems = _calendars.resolve_propers(document, mass)
        self.assertEqual([], problems)
        expected = {'Secret': '52a4292532f4f9eeb18101fa444e03d11a4a9f3e250b333f6f327fd800a6f094', 'Postcommunion': '40ac4d221ce22bfb2101d84e61f51f83495c09fe8c19a6b7af6210b2ded3f144'}
        found = {proper["name"]: (proper, origin)
                 for _, proper, origin in appointed if proper["name"] in expected}
        self.assertEqual(set(expected), set(found))
        for name, digest in expected.items():
            proper, origin = found[name]
            self.assertIsNone(origin, name)
            self.assertNotIn("text_status", proper)
            self.assertEqual(digest, text_sha256(proper["text"]))
            self.assertIn("beato Theodoro Martyre tuo", proper["text"])
            self.assertTrue(proper["text"].rstrip().endswith("et regnat in unitate."))

    def test_cold_review_repairs_are_bound_to_the_read_target_pages(self) -> None:
        document = yaml.safe_load(
            (CALENDARS / "roman-1962/propers.yaml").read_text(encoding="utf-8")
        )
        bodies = {
            (mass["key"], proper["name"]): " ".join(proper["text"].split())
            for section in document["sections"].values()
            for mass in section["masses"]
            for proper in mass.get("propers", [])
            if "text" in proper
        }
        readings = {
            ("comm-s-felicis-presbyteri-martyris", "Collect"): (
                "Concede, quaesumus, omnipotens Deus:", "Per Dominum nostrum."
            ),
            ("ss-vincentii-anastasii-martyrum", "Secret"): (
                "devotionis offerimus: quae", "Per Dominum."
            ),
            ("comm-s-petri-apostoli", "Postcommunion"): (
                "munus oblatum: ut, sicut", "Qui tecum vivit et regnat in unitate."
            ),
            ("cathedrae-s-petri-apostoli", "Postcommunion"): (
                "per illum tuae", "indulgentiae largitatem."
            ),
            ("s-ubaldi-episcopi-confessoris", "Collect"): (
                "Auxilium tuum nobis, Domine, quaesumus, placatus impende:",
                "Per Dominum.",
            ),
            ("s-petri-caelestini-papae-confessoris", "Collect"): (
                "quique illum humilitati postponere docuisti:",
                "Qui tecum vivit et regnat in unitate.",
            ),
            ("comm-s-petri-apostoli-2", "Postcommunion"): (
                "per illum tuae", "Per Dominum."
            ),
        }
        ledger = tomllib.loads(
            (INVENTORIES / "roman-1962-proper-latin-provenance-v1.toml").read_text()
        )
        rows = {(row["mass"], row["proper"]): row for row in ledger["entries"]}
        for key, (reading, conclusion) in readings.items():
            with self.subTest(key=key):
                self.assertIn(reading, bodies[key])
                self.assertTrue(bodies[key].endswith(conclusion))
                self.assertNotRegex(bodies[key], r"\bilium\b|sanitaria|Oratio|AUxflium|V -")
                self.assertIn(
                    ".recovery-2026-10-01-", rows[key]["verification_source_id"]
                )
        self.assertIn(
            "nobis salutaria, te miserante, reddantur",
            bodies["ss-vincentii-anastasii-martyrum", "Secret"],
        )
        self.assertIn(
            "printed p. 446; artifact PDF p. 532",
            rows["s-ubaldi-episcopi-confessoris", "Collect"]["publication_locator"],
        )

    def test_ledgers_cover_every_direct_text_without_name_collapse(self) -> None:
        paths = [
            CALENDARS / calendar / "propers.yaml"
            for calendar in ("postconciliar", "roman-1962", "roman-pre-1955")
        ]
        self.assertEqual(
            [],
            sidecar_problems(paths, inventory_root=INVENTORIES, required=True),
        )
        expected = {
            "postconciliar": (329, 4),
            # 1112 since 2026-10-01: the KI-054 page reading landed the
            # Agnes secundo Secret, a witness-gap slot with no stub row before.
            # 1114 later that day: St Angela Merici's own Secret and
            # Postcommunion, new slots, each with a new collated row.
            # 1120 since 2026-10-20 (C3): St Lucy's Communion carries the
            # Missal antiphon rather than a Bible reconstruction.
            # +3 on 2026-10-20: source-backed Christ-the-King orations.
            "roman-1962": (1145, 5),
            "roman-pre-1955": (0, 0),
        }
        for calendar, (total, repeated) in expected.items():
            records, problems = read_sidecar(
                INVENTORIES / f"{calendar}{SIDECAR_SUFFIX}"
            )
            self.assertEqual([], problems)
            self.assertEqual(total, len(records))
            self.assertEqual(
                # 46 since 2026-10-01: KI-054 published 31 quarantined bodies.
                {"postconciliar": 329, "roman-1962": 46}.get(calendar, 0),
                sum(row.get("body_status") == "removed" for row in records.values()),
            )
            # Four duplicate-name pairs and one six-item procession are all
            # separate permission decisions, never last-row-wins dict entries.
            self.assertEqual(repeated, sum(key.occurrence > 1 for key in records))

    def test_publication_loader_validates_production_source_metadata(self) -> None:
        # 1114 since 2026-10-01: St Angela Merici's Secret and Postcommunion.
        # 1120 since 2026-10-20 (C3): St Lucy's Communion has its own body.
        expected = {"postconciliar": 329, "roman-1962": 1145, "roman-pre-1955": 1145}
        for calendar, count in expected.items():
            records, problems = publication_records(CALENDARS, calendar, INVENTORIES)
            self.assertEqual([], problems)
            self.assertEqual(count, len(records))

    def test_production_ledgers_publish_only_the_exact_historical_recoveries(self) -> None:
        permitted = []
        nonpermitted = []
        for calendar in ("postconciliar", "roman-1962", "roman-pre-1955"):
            records, _ = read_sidecar(INVENTORIES / f"{calendar}{SIDECAR_SUFFIX}")
            for key, row in records.items():
                (permitted if row["publication_status"] == "permitted" else nonpermitted).append(
                    (calendar, key, row)
                )
        roman = {key for calendar, key, _ in permitted if calendar == "roman-1962"}
        # Every permitted body is pinned by SHAPE rather than by key. Pinning
        # keys stopped scaling when the 2026-09-03 backfill took the publishable
        # set from 13 to 290 across all five sections of the calendar, and a
        # list nobody can read is not a guard. What actually protects the set is
        # below and per row: each must name an editorial-projection passage of a
        # known edition, carry a collated provenance, a public-domain basis, an
        # independent public-domain artifact beside the projection, and a
        # verification passage in the 1962 target. The count here is the
        # tripwire: it moves only by a visible edit to this number.
        calendar_masses = {
            mass["key"]
            for section in yaml.safe_load(
                (CALENDARS / "roman-1962/propers.yaml").read_text(encoding="utf-8")
            )["sections"].values()
            for mass in section["masses"]
        }
        self.assertTrue(
            {k.mass for k in roman} <= calendar_masses,
            sorted({k.mass for k in roman} - calendar_masses),
        )
        # 1066 since 2026-10-01: the 32 KI-054 bodies, each read on the 1962
        # page image and on a page image of the 1862 Pustet or the 1922 Mame.
        # 1068 later that day: St Angela Merici's own Secret and Postcommunion,
        # read on the 1962 page image and on the 1862 Pustet's (and the Mame's).
        # 1074 since 2026-10-20 (C3): St Lucy's Communion is independently
        # collated on the 1962 and public-domain Mame 1922 page images.
        self.assertEqual(1099, len(permitted))
        self.assertEqual(1099, len(roman))
        target_artifact = (
            "artifact.catholic-church.missale-romanum."
            "vatican-typica-1962.cmaa-facsimile-pdf"
        )
        projection_specs = {
            "editorial-projection-2026-08-27": {
                "artifact_id": (
                    "artifact.triptych.roman-1962-latin-proper-editorial-projection."
                    "editorial-projection-2026-08-27."
                    "normalized-latin-propers-0bf4adcc"
                ),
                "publication_source_ids": {
                    "artifact.francis-xavier-lasance.the-new-roman-missal."
                    "benziger-revised-1945.new-roman-missal-text-80b34759"
                },
                "projected_from": {
                    "artifact.francis-xavier-lasance.the-new-roman-missal."
                    "benziger-revised-1945."
                    "internet-archive-facsimile-pdf-6cf3c3d0",
                    target_artifact,
                },
            },
            "editorial-projection-2026-08-28": {
                "artifact_id": (
                    "artifact.triptych.roman-1962-latin-proper-editorial-projection."
                    "editorial-projection-2026-08-28.augustine-orations-8a2a938d"
                ),
                "publication_source_ids": {
                    "artifact.catholic-church.missale-romanum."
                    "1922-tours-mame-editio-quarta-iuxta-typicam."
                    "ia-scan-pdf-9873693a"
                },
                "projected_from": {
                    "artifact.catholic-church.missale-romanum."
                    "1922-tours-mame-editio-quarta-iuxta-typicam."
                    "ia-scan-pdf-9873693a",
                    target_artifact,
                },
            },
            # The first seasonal projection, and the first whose public-domain
            # antecedent is the tracked 1862 Pustet text layer rather than a
            # page-image witness.
            "editorial-projection-2026-09-03": {
                "artifact_id": (
                    "artifact.triptych.roman-1962-latin-proper-editorial-projection."
                    "editorial-projection-2026-09-03."
                    "post-pentecosten-14-orations-8ad972fc"
                ),
                "publication_source_ids": {
                    "artifact.catholic-church.missale-romanum."
                    "pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf",
                    "artifact.catholic-church.missale-romanum."
                    "1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a",
                },
                "projected_from": {
                    "artifact.catholic-church.missale-romanum."
                    "pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf",
                    "artifact.catholic-church.missale-romanum."
                    "1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a",
                    target_artifact,
                },
            },
            # The dated MVP recovery binds three Christ-the-King prayers to
            # a bounded, independently publishable 1929 Schott derivative.
            "editorial-projection-2026-10-20": {
                "artifact_id": "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.christ-the-king-orations-dc4287d2",
                "publication_source_ids": {"artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.christ-the-king-orations-la-checked-32eecc40", "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.theodore-two-orations-la-checked-638fc0c5", "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.all-saints-four-propers-la-checked-82edd79a", 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.immaculate-conception-four-propers-la-checked-18084e74', "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.christmas-nine-orations-la-checked-825c69f4"},
                "projected_from": {"artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.christ-the-king-orations-la-checked-32eecc40", target_artifact, "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.theodore-two-orations-la-checked-638fc0c5", "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.all-saints-four-propers-la-checked-82edd79a", 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.immaculate-conception-four-propers-la-checked-18084e74', "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.christmas-nine-orations-la-checked-825c69f4"},
            },
        }

        used_projection_editions = set()
        supplemented = []
        for calendar, key, row in permitted:
            with self.subTest(calendar=calendar, key=key):
                matches = [
                    edition
                    for edition in projection_specs
                    if f".{edition}." in row["source_id"]
                ]
                self.assertEqual(1, len(matches), row["source_id"])
                edition = matches[0]
                used_projection_editions.add(edition)
                spec = projection_specs[edition]
                self.assertEqual("roman-1962", calendar)
                self.assertIsNone(row.get("body_status"))
                self.assertEqual("collated", row["provenance_status"])
                # One reviewed dated-feast selection has a conservative grade;
                # every other legacy row still satisfies the exact-target rule.
                if key == LatinKey('conceptione-immaculata-beatae-mariae-virginis', "", "Secret", "", "", 1):
                    self.assertEqual("roman-1962", calendar)
                    self.assertEqual('6755a936e24660ef77e7c0ceffba13c28d21a82cc941bf8fb9ba5b57863f31a9', row["text_sha256"])
                    self.assertEqual("collated-exact", row["relationship"])
                    self.assertEqual('passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.immaculate-conception-secret', row["source_id"])
                    self.assertEqual('passage.catholic-church.missale-romanum.vatican-typica-1962.immaculate-conception-selected-feast-four-propers-word-collation-2026-10-20', row["verification_source_id"])
                    self.assertEqual(['artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.immaculate-conception-four-propers-5f582ed9', 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.immaculate-conception-four-propers-la-checked-18084e74'],
                                     row["publication_source_ids"])
                    self.assertIn("solemnitate feast selection only", row["provenance_evidence"])
                    self.assertIn("commemoratione alternative is not represented", row["provenance_evidence"])
                else:
                    self.assertEqual(
                        "editorial-projection-exact-to-target", row["relationship"]
                    )
                self.assertTrue(row["transformations"])
                self.assertEqual("public-domain", row["publication_basis"])
                self.assertEqual(set(SURFACES), set(row["surfaces"]))
                # The 2026-09-03 edition carries one projection artifact per
                # backfill lane, so a row names an artifact *of* that edition
                # rather than one fixed id; the public-domain witness beside it
                # is still pinned exactly.
                ids = row["publication_source_ids"]
                self.assertGreaterEqual(len(ids), 2, ids)
                self.assertTrue(
                    ids[0].startswith(
                        "artifact.triptych.roman-1962-latin-proper-editorial-"
                        f"projection.{edition}."
                    ),
                    ids[0],
                )
                # A projection edition may rest on more than one public-domain
                # witness, because a formulary the 1862 does not carry has the
                # 1922 Mame as its antecedent rather than as corroboration --
                # Holy Family, granted 1893 and universal 1921, is the case.
                self.assertIn(ids[1], spec["publication_source_ids"], ids[1])
                # Anything after the pinned witness is a further registered
                # artifact of that SAME public-domain printing, never a new
                # basis. The pentecost-16 Postcommunion is the case: its 1862
                # text layer drops `et` at a line break, so the printed page
                # itself (Internet Archive leaf n426, retrieved 2026-09-05) was
                # registered and named beside the text layer in 1529f6bef to
                # close that gap.
                witness = registered_artifact(ids[1])
                for extra in ids[2:]:
                    supplement = registered_artifact(extra)
                    self.assertEqual(
                        witness["edition_id"], supplement["edition_id"], extra
                    )
                    self.assertEqual(
                        "public-domain", supplement["rights_status"], extra
                    )
                if ids[2:]:
                    supplemented.append((key, ids[2:]))
                # Sanctoral recoveries came first; the seasonal ones name a
                # temporal- passage of the same target edition.
                self.assertTrue(
                    row["verification_source_id"].startswith(
                        "passage.catholic-church.missale-romanum."
                        "vatican-typica-1962."
                    )
                )
        self.assertEqual(set(projection_specs), used_projection_editions)
        # The same kind of tripwire as the permitted count: a further witness
        # beside the pinned one is rare, so each is a visible edit here.
        # 30 since 2026-10-01: the 29 KI-054 rows resting on the 1862 name its
        # registered facsimile PDF beside the text layer, because the words were
        # read on that printing's page images, not on its damaged text layer.
        # 32 later that day: St Angela Merici's Secret and Postcommunion, read
        # on the 1862's appendix leaves n813-n814, do the same.
        # Seven further cold-review repairs bind the 1862 page image as well.
        # 44 since 2026-10-19 (C3): the five Pentecost rows name the 1862
        # page-image leaves n384-n386 they were read on.
        self.assertEqual(44, len(supplemented), supplemented)

        work = tomllib.loads((EDITORIAL_PROJECTION / "work.toml").read_text())
        self.assertEqual("Triptych contributors", work["responsible"])
        artifacts = {
            row["id"]: row
            for path in EDITORIAL_PROJECTION.glob(
                "editions/*/artifacts/*/artifact.toml"
            )
            for row in [tomllib.loads(path.read_text())]
        }
        passages = {
            row["id"]: row
            for path in EDITORIAL_PROJECTION.glob("editions/*/passages/*.toml")
            for row in [tomllib.loads(path.read_text())]
        }
        for edition, spec in projection_specs.items():
            with self.subTest(edition=edition):
                # An edition may carry several projection artifacts -- the
                # 2026-09-03 backfill emits one per lane -- and every one of
                # them must stand on the same two witnesses.
                own = [a for i, a in artifacts.items() if f".{edition}." in i]
                self.assertTrue(own, edition)
                for artifact in own:
                    self.assertEqual("project-created", artifact["rights_status"])
                    self.assertTrue(artifact["transformation"].strip())
                    # An artifact stands on the witnesses its own masses used,
                    # which is a subset of what the edition may rest on: within
                    # one lane most formularies take the Pustet and a few take
                    # the Mame. The target must always be there.
                    stands_on = set(artifact["projected_from"])
                    self.assertTrue(
                        stands_on <= spec["projected_from"],
                        sorted(stands_on - spec["projected_from"]),
                    )
                    self.assertIn(target_artifact, stands_on)
        for _, _, row in permitted:
            passage = passages[row["source_id"]]
            artifact = artifacts[passage["artifact_id"]]
            payload = (ROOT / artifact["path"]).read_text().splitlines(
                keepends=True
            )
            projected_body = "".join(
                line
                for start, end in passage["physical_line_ranges"]
                for line in payload[start - 1 : end]
            )
            self.assertEqual(row["text_sha256"], text_sha256(projected_body))
        self.assertEqual(375, len(nonpermitted))
        collated = [
            item for item in nonpermitted if item[2]["provenance_status"] == "collated"
        ]
        self.assertEqual(4, len(collated))
        st_albert = [
            item
            for item in collated
            if item[1].mass == "s-alberti-magni-episcopi-confessoris-ecclesiae"
        ]
        # These three stay rights-withheld deliberately. A 2026-09-03 sanctoral
        # lane found no public-domain witness for them, which is right for a
        # saint canonised in 1931, but retyping them to witness-gap would have
        # destroyed ledger rows carrying a collated-exact reading of the 1962
        # facsimile and its Lasance 1945 evidence: a witness-gap proper owns no
        # removed body, so its row goes with it. An absent verdict is about
        # public-domain witnesses, not about whether an exemplar is held.
        self.assertEqual(3, len(st_albert))
        self.assertTrue(
            all(
                calendar == "roman-1962"
                and row["publication_status"] == "withheld"
                and row["publication_basis"] == "unresolved"
                and row["surfaces"] == []
                for calendar, _, row in st_albert
            )
        )
        vianney = [
            item
            for item in collated
            if item[1].mass == "s-ioannis-mariae-vianney-confessoris"
        ]
        self.assertEqual(1, len(vianney))
        _, vianney_key, vianney_row = vianney[0]
        self.assertEqual("Collect", vianney_key.proper)
        self.assertEqual("collated-non-exact", vianney_row["relationship"])
        self.assertEqual("withheld", vianney_row["publication_status"])
        self.assertEqual(
            "non-exact-historical-witness",
            vianney_row["publication_basis"],
        )
        self.assertEqual([], vianney_row["surfaces"])

        # The seventeen the Pustet review withheld are published as of
        # 2026-09-03, on the 1922 Mame, under the rule that a witness must carry
        # the same WORDS and not the same string. That review's findings about
        # the Pustet stand and are still checked by
        # test_roman_pustet_common_collation; what changed is that a non-exact
        # Pustet page no longer keeps a body off every surface, because the
        # repository publishes its own declared orthography and has never served
        # an exact 1962 string anywhere. Only St Albert's three and Vianney's one
        # remain collated but withheld.
        pustet = [
            item
            for item in collated
            if item not in st_albert and item not in vianney
        ]
        self.assertEqual(0, len(pustet))
        unresolved = [
            row for _, _, row in nonpermitted if row["provenance_status"] == "unresolved"
        ]
        self.assertEqual(371, len(unresolved))
        self.assertTrue(all(row["publication_basis"] == "unresolved" for row in unresolved))
        postconciliar = [
            row for calendar, _, row in nonpermitted if calendar == "postconciliar"
        ]
        self.assertEqual(329, len(postconciliar))
        self.assertTrue(
            all(
                row["body_status"] == "removed"
                and row["provenance_status"] == "unresolved"
                and row["publication_status"] == "unresolved"
                and row["surfaces"] == []
                for row in postconciliar
            )
        )


class ModelTests(unittest.TestCase):
    def test_nonexact_historical_witness_cannot_be_made_publishable(self) -> None:
        body = "Oratio non exacte collata."
        all_surfaces = [
            "web",
            "download",
            "print",
            "cli",
            "corpus-data",
            "public-git",
        ]
        entry = "\n".join(
            [f'text_sha256 = "{text_sha256(body)}"', *permitted_nonexact_fields()]
        )
        invalid = tomllib.loads(toml_ledger(entry))["entries"][0]
        with tempfile.TemporaryDirectory() as room:
            sources = Path(room) / "sources"
            calendars = sources / "calendars"
            inventories = sources / "inventories"
            (calendars / "demo").mkdir(parents=True)
            inventories.mkdir()
            (calendars / "demo/propers.yaml").write_text(
                yaml.safe_dump(
                    demo_document(
                        {"name": "Collect", "source": "composed", "text": body}
                    ),
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            path = inventories / f"demo{SIDECAR_SUFFIX}"
            path.write_text(toml_ledger(entry), encoding="utf-8")
            records, problems = read_sidecar(path)
            loaded, loader_problems = publication_records(
                calendars,
                "demo",
                inventories,
                registered_sources={
                    "artifact.target.unresolved": {
                        "record_type": "artifact",
                        "rights_status": "unresolved",
                    },
                    "artifact.historical.public-domain": {
                        "record_type": "artifact",
                        "rights_status": "public-domain",
                    },
                },
            )
        self.assertEqual({}, records)
        self.assertTrue(
            any("intrinsically nonpublishable" in problem for problem in problems),
            problems,
        )
        self.assertEqual({}, loaded)
        self.assertTrue(
            any(
                "intrinsically nonpublishable" in problem
                for problem in loader_problems
            ),
            loader_problems,
        )

        # Projection remains fail-closed even if an unvalidated caller hands the
        # decision layer this row directly.  Neither the browser/download/print
        # structure nor the CLI may become an alternate publication path.
        key = LatinKey("day", "", "Collect", occurrence=1)
        decision = decision_for(key, body, {key: invalid})
        self.assertFalse(decision.permits(all_surfaces))
        self.assertIn(
            "non-exact-historical-witness",
            decision.projection(all_surfaces)["reason"],
        )
        mass = demo_document(
            {"name": "Collect", "source": "composed", "text": body}
        )["sections"]["01"]["masses"][0]
        for surfaces in (STRUCTURE_SURFACES, CLI_SURFACES):
            with self.subTest(surfaces=sorted(surfaces)):
                proper = sanitize_mass(mass, {key: invalid}, surfaces)["propers"][0]
                self.assertIsNone(proper["text"])
                self.assertTrue(proper["latin"]["withheld"])
                self.assertIn(
                    "non-exact-historical-witness", proper["latin"]["reason"]
                )

    def test_never_held_body_is_not_a_removed_body_or_latin_ledger_owner(self) -> None:
        source_id = "artifact.public-domain.example"
        for reason in (
            {"kind": "witness-gap", "source_id": source_id},
            {"kind": "no-exemplar"},
        ):
            with self.subTest(reason=reason["kind"]), tempfile.TemporaryDirectory() as room:
                status = {
                    "state": "unavailable",
                    "scope": "proper-body",
                    "reasons": [reason],
                }
                document = demo_document(
                    {
                        "name": "Collect",
                        "source": "composed",
                        "text_status": status,
                    }
                )
                self.assertEqual([], list(body_owners(document)))

                sources = Path(room) / "sources"
                calendar_dir = sources / "calendars/demo"
                inventory_dir = sources / "inventories"
                calendar_dir.mkdir(parents=True)
                inventory_dir.mkdir()
                calendar = calendar_dir / "propers.yaml"
                calendar.write_text(
                    yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
                sidecar = inventory_dir / f"demo{SIDECAR_SUFFIX}"
                empty_ledger = render_unresolved_sidecar("demo", document).replace(
                    "\n[defaults]\n", "\nentries = []\n\n[defaults]\n", 1
                )
                sidecar.write_text(
                    empty_ledger, encoding="utf-8"
                )

                records, ledger_problems = read_sidecar(sidecar)
                self.assertEqual({}, records)
                self.assertEqual([], ledger_problems)
                self.assertEqual(
                    [],
                    sidecar_problems(
                        [calendar],
                        inventory_root=inventory_dir,
                        required=True,
                        registered_source_ids={source_id},
                    ),
                )
                projected = sanitize_mass(
                    document["sections"]["01"]["masses"][0],
                    records,
                    STRUCTURE_SURFACES,
                )["propers"][0]
                self.assertEqual(status, projected["text_status"])
                self.assertNotIn("latin", projected)

    def test_removed_body_retains_hash_without_fabricating_provenance(self) -> None:
        former = "Corpus quarantined."
        source_id = "artifact.public-domain.example"
        status = {
            "state": "unavailable",
            "scope": "proper-body",
            "reasons": [{"kind": "rights-withheld", "source_id": source_id}],
        }
        document = demo_document(
            {
                "name": "Collect",
                "source": "composed",
                "incipit": "Corpus",
                "text_status": status,
            }
        )
        entry = f'''text_sha256 = "{text_sha256(former)}"
body_status = "removed"'''
        with tempfile.TemporaryDirectory() as room:
            sources = Path(room) / "sources"
            calendar_dir = sources / "calendars/demo"
            inventory_dir = sources / "inventories"
            calendar_dir.mkdir(parents=True)
            inventory_dir.mkdir()
            calendar = calendar_dir / "propers.yaml"
            calendar.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            sidecar = inventory_dir / f"demo{SIDECAR_SUFFIX}"
            sidecar.write_text(toml_ledger(entry), encoding="utf-8")
            records, ledger_problems = read_sidecar(sidecar)
            problems = sidecar_problems(
                [calendar],
                inventory_root=inventory_dir,
                required=True,
                registered_source_ids={source_id},
            )

            self.assertEqual([], ledger_problems)
            self.assertEqual([], problems)
            self.assertEqual(
                [(LatinKey("day", "", "Collect", occurrence=1), None, "removed")],
                list(body_owners(document)),
            )
            projected = sanitize_mass(
                document["sections"]["01"]["masses"][0],
                records,
                STRUCTURE_SURFACES,
            )["propers"][0]
            self.assertNotIn("text", projected)
            self.assertEqual(
                {
                    "target": "Collect",
                    "state": "unavailable",
                    "held": False,
                    "available": False,
                    "withheld": True,
                },
                projected["latin"],
            )
            self.assertEqual(status, projected["text_status"])
            with self.assertRaisesRegex(ValueError, "cannot reconstruct removed"):
                render_unresolved_sidecar("demo", document)

            document["sections"]["01"]["masses"][0]["propers"][0]["text"] = former
            calendar.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            problems = sidecar_problems(
                [calendar],
                inventory_root=inventory_dir,
                required=True,
                registered_source_ids={source_id},
            )
        self.assertTrue(any("retains text" in problem for problem in problems), problems)

    def test_checker_accepts_only_typed_rights_quarantine_on_a_proper(self) -> None:
        checker = load_tool("check-calendar-masses")
        source_id = "artifact.demo"
        checker.source_ids = lambda: ({source_id}, [])
        proper = {
            "name": "Collect",
            "source": "composed",
            "text_status": {
                "state": "unavailable",
                "scope": "proper-body",
                "reasons": [{"kind": "rights-withheld", "source_id": source_id}],
            },
        }
        problems: list[str] = []
        checker.check_proper("demo", proper, problems)
        self.assertEqual([], problems)

        checker.check_proper("demo", {**proper, "text": "still resident"}, problems := [])
        self.assertTrue(any("must not coexist with text" in one for one in problems), problems)

    def test_missing_and_stale_records_fail_closed(self) -> None:
        key = LatinKey("day", "", "Collect")
        proper = {"name": "Collect", "text": "Non publicetur."}
        missing = sanitize_proper(proper, key, {}, STRUCTURE_SURFACES)
        self.assertIsNone(missing["text"])
        self.assertTrue(missing["latin"]["withheld"])
        self.assertIn("no per-text", missing["latin"]["reason"])

        stale_key = LatinKey("day", "", "Collect", occurrence=1)
        stale = sanitize_proper(
            proper,
            stale_key,
            {
                stale_key: {
                    "text_sha256": text_sha256("other"),
                    "provenance_status": "collated",
                    "publication_status": "permitted",
                    "publication_basis": "public-domain",
                    "surfaces": sorted(STRUCTURE_SURFACES),
                }
            },
            STRUCTURE_SURFACES,
        )
        self.assertIsNone(stale["text"])
        self.assertIn("stale", stale["latin"]["reason"])

    def test_malformed_cycle_shape_does_not_crash_latin_join(self) -> None:
        proper = {
            "name": "Gospel Acclamation",
            "cycles": ["not-a-mapping"],
        }
        document = demo_document(proper)
        self.assertEqual([], list(body_owners(document)))
        mass = document["sections"]["01"]["masses"][0]
        projected = sanitize_mass(mass, {}, STRUCTURE_SURFACES)
        self.assertEqual(["not-a-mapping"], projected["propers"][0]["cycles"])

    def test_occurrence_is_source_identity_and_hash_lookup_never_guesses(self) -> None:
        first = LatinKey("day", "", "Procession Antiphon", occurrence=1)
        second = LatinKey("day", "", "Procession Antiphon", occurrence=2)
        records = {
            first: {
                "text_sha256": text_sha256("Prima."),
                "provenance_status": "unresolved",
                "publication_status": "unresolved",
                "publication_basis": "unresolved",
                "surfaces": [],
            },
            second: {
                "text_sha256": text_sha256("Secunda."),
                "provenance_status": "unresolved",
                "publication_status": "unresolved",
                "publication_basis": "unresolved",
                "surfaces": [],
            },
        }
        resolved = decision_for(LatinKey("day", "", "Procession Antiphon"), "Secunda.", records)
        self.assertEqual(2, resolved.key.occurrence)

        records[first] = dict(records[first], text_sha256=text_sha256("Secunda."))
        ambiguous = decision_for(
            LatinKey("day", "", "Procession Antiphon"), "Secunda.", records
        )
        self.assertIn("ambiguous", ambiguous.reason)
        self.assertFalse(ambiguous.permits(STRUCTURE_SURFACES))

    def test_repeated_names_render_and_validate_as_distinct_records(self) -> None:
        document = demo_document(
            {"name": "Procession Antiphon", "source": "composed", "text": "Prima."},
            {"name": "Procession Antiphon", "source": "composed", "text": "Secunda."},
        )
        owners = list(text_owners(document))
        self.assertEqual([1, 2], [key.occurrence for key, _ in owners])
        with tempfile.TemporaryDirectory() as room:
            path = Path(room) / f"demo{SIDECAR_SUFFIX}"
            path.write_text(render_unresolved_sidecar("demo", document), encoding="utf-8")
            records, problems = read_sidecar(path)
        self.assertEqual([], problems)
        self.assertEqual(2, len(records))

    def test_provenance_may_identify_a_restricted_witness_without_permission(self) -> None:
        body = "Oratio moderna."
        entry = f'''text_sha256 = "{text_sha256(body)}"
provenance_status = "identified"
source_id = "artifact.holy-see.example"
source_date = "2002"
locator = "p. 1"
relationship = "exact-transcription"
transformations = []
provenance_evidence = "Artifact identity record demo-1"
provenance_authority = "Human transcription record"
provenance_confidence = "high"
publication_status = "unresolved"
publication_basis = "unresolved"
surfaces = []'''
        with tempfile.TemporaryDirectory() as room:
            path = Path(room) / f"demo{SIDECAR_SUFFIX}"
            path.write_text(toml_ledger(entry), encoding="utf-8")
            records, problems = read_sidecar(path)
        self.assertEqual([], problems)
        decision = decision_for(LatinKey("day", "", "Collect"), body, records)
        self.assertEqual("artifact.holy-see.example", decision.source_id)
        self.assertFalse(decision.permits(STRUCTURE_SURFACES))

    def test_public_domain_requires_exact_collation_and_each_output_surface(self) -> None:
        body = "Oratio antiqua."
        entry = f'''text_sha256 = "{text_sha256(body)}"
provenance_status = "collated"
source_id = "artifact.public-domain.example"
source_date = "1862"
locator = "p. 2"
relationship = "collated-exact"
verification_source_id = "artifact.public-domain.example"
verification_locator = "p. 2, second reading"
transformations = []
provenance_evidence = "Per-text witness comparison demo-1"
provenance_authority = "Human page-image collation"
provenance_confidence = "high"
publication_status = "permitted"
publication_basis = "public-domain"
surfaces = ["web", "download", "print", "corpus-data", "public-git"]
publication_source_ids = ["artifact.public-domain.example"]
publication_locator = "artifact rights record"
publication_evidence = "Per-text public-domain analysis demo-1"'''
        with tempfile.TemporaryDirectory() as room:
            path = Path(room) / f"demo{SIDECAR_SUFFIX}"
            path.write_text(toml_ledger(entry), encoding="utf-8")
            records, problems = read_sidecar(path)
        self.assertEqual([], problems)
        decision = decision_for(LatinKey("day", "", "Collect"), body, records)
        self.assertTrue(decision.permits(STRUCTURE_SURFACES))
        self.assertFalse(decision.permits(CLI_SURFACES))

    def test_defaults_cannot_be_used_as_a_blanket_permission(self) -> None:
        body = "Oratio."
        entry = f'text_sha256 = "{text_sha256(body)}"'
        defaults = '''provenance_status = "collated"
publication_status = "permitted"
publication_basis = "public-domain"
surfaces = ["web", "download", "print", "cli"]'''
        with tempfile.TemporaryDirectory() as room:
            path = Path(room) / f"demo{SIDECAR_SUFFIX}"
            path.write_text(toml_ledger(entry, defaults=defaults), encoding="utf-8")
            _, problems = read_sidecar(path)
        self.assertTrue(any("decided per text" in problem for problem in problems), problems)

    def test_permission_requires_authority_notice_and_retrieval_evidence(self) -> None:
        body = "Oratio."
        entry = f'''text_sha256 = "{text_sha256(body)}"
provenance_status = "identified"
source_id = "artifact.example"
source_date = "2026"
locator = "p. 1"
relationship = "exact-transcription"
transformations = []
provenance_evidence = "Transcription record"
provenance_authority = "Human page reading"
provenance_confidence = "high"
publication_status = "permitted"
publication_basis = "permission"
surfaces = ["web", "corpus-data", "public-git"]
publication_evidence = "Grant page"'''
        with tempfile.TemporaryDirectory() as room:
            path = Path(room) / f"demo{SIDECAR_SUFFIX}"
            path.write_text(toml_ledger(entry), encoding="utf-8")
            _, problems = read_sidecar(path)
        self.assertTrue(any("named authority" in problem for problem in problems), problems)
        self.assertTrue(any("conditioned notice" in problem for problem in problems), problems)
        self.assertTrue(any("retrieval date" in problem for problem in problems), problems)

    def test_checker_rejects_unregistered_transcription_witness(self) -> None:
        body = "Oratio."
        document = demo_document({"name": "Collect", "source": "composed", "text": body})
        entry = f'''text_sha256 = "{text_sha256(body)}"
provenance_status = "identified"
source_id = "artifact.not-registered"
source_date = "1900"
locator = "p. 1"
relationship = "exact-transcription"
transformations = []
provenance_evidence = "Transcription record"
provenance_authority = "Human page reading"
provenance_confidence = "high"
publication_status = "unresolved"
publication_basis = "unresolved"
surfaces = []'''
        with tempfile.TemporaryDirectory() as room:
            sources = Path(room) / "sources"
            calendar_dir = sources / "calendars/demo"
            inventory_dir = sources / "inventories"
            calendar_dir.mkdir(parents=True)
            inventory_dir.mkdir()
            calendar = calendar_dir / "propers.yaml"
            calendar.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
            (inventory_dir / f"demo{SIDECAR_SUFFIX}").write_text(
                toml_ledger(entry), encoding="utf-8"
            )
            problems = sidecar_problems(
                [calendar],
                inventory_root=inventory_dir,
                required=True,
                registered_source_ids=set(),
            )
        self.assertTrue(any("not registered" in problem for problem in problems), problems)

    def test_publication_loader_rechecks_exact_witness_rights(self) -> None:
        body = "Oratio antiqua."
        document = demo_document(
            {"name": "Collect", "source": "composed", "text": body}
        )
        entry = f'''text_sha256 = "{text_sha256(body)}"
provenance_status = "collated"
source_id = "artifact.modern.example"
source_date = "1962"
locator = "p. 2"
relationship = "collated-exact"
verification_source_id = "artifact.antecedent.example"
verification_locator = "p. 2"
transformations = []
provenance_evidence = "Per-text comparison"
provenance_authority = "Human page-image collation"
provenance_confidence = "high"
publication_status = "permitted"
publication_basis = "public-domain"
surfaces = ["web", "download", "print", "cli", "corpus-data", "public-git"]
publication_source_ids = ["artifact.rights.example"]
publication_locator = "artifact rights record"
publication_evidence = "Public-domain analysis"'''
        with tempfile.TemporaryDirectory() as room:
            sources = Path(room) / "sources"
            calendars = sources / "calendars"
            inventories = sources / "inventories"
            (calendars / "demo").mkdir(parents=True)
            inventories.mkdir()
            (calendars / "demo/propers.yaml").write_text(
                yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
            )
            (inventories / f"demo{SIDECAR_SUFFIX}").write_text(
                toml_ledger(entry), encoding="utf-8"
            )
            records, problems = publication_records(
                calendars,
                "demo",
                inventories,
                registered_sources={
                    "artifact.modern.example": {
                        "record_type": "artifact",
                        "rights_status": "unresolved",
                    },
                    "artifact.antecedent.example": {
                        "record_type": "artifact",
                        "rights_status": "unresolved",
                    },
                    "artifact.rights.example": {
                        "record_type": "artifact",
                        "rights_status": "unresolved",
                    },
                },
            )
        self.assertEqual({}, records)
        self.assertTrue(
            any("registered public-domain" in problem for problem in problems),
            problems,
        )

    def test_recension_inherits_witness_identity_but_not_permission(self) -> None:
        body = "Oratio antiqua."
        base = demo_document({"name": "Collect", "source": "composed", "text": body})
        base["calendar"] = "base"
        entry = f'''text_sha256 = "{text_sha256(body)}"
provenance_status = "collated"
source_id = "artifact.public-domain.example"
source_date = "1862"
locator = "p. 2"
relationship = "collated-exact"
verification_source_id = "artifact.public-domain.example"
verification_locator = "p. 2, second reading"
transformations = []
provenance_evidence = "Per-text comparison"
provenance_authority = "Human page-image collation"
provenance_confidence = "high"
publication_status = "permitted"
publication_basis = "public-domain"
surfaces = ["web", "download", "print", "cli", "corpus-data", "public-git"]
publication_source_ids = ["artifact.public-domain.example"]
publication_locator = "artifact rights record"
publication_evidence = "Public-domain analysis"'''
        older = {
            "schema": "triptych-calendar-masses/v1",
            "calendar": "older",
            "edition": "Older Demo",
            "psalm_numbering": "vulgate",
            "text_from": "base",
            "sections": {},
        }
        empty = f'''schema = "{SCHEMA}"
calendar = "older"
language = "la"
policy = "{POLICY}"
entries = []

[defaults]
provenance_status = "unresolved"
publication_status = "unresolved"
publication_basis = "unresolved"
surfaces = []
'''
        with tempfile.TemporaryDirectory() as room:
            sources = Path(room) / "sources"
            calendars = sources / "calendars"
            inventories = sources / "inventories"
            for name, document in (("base", base), ("older", older)):
                (calendars / name).mkdir(parents=True, exist_ok=True)
                (calendars / name / "propers.yaml").write_text(
                    yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
                )
            inventories.mkdir()
            (inventories / f"base{SIDECAR_SUFFIX}").write_text(
                toml_ledger(entry).replace('calendar = "demo"', 'calendar = "base"'),
                encoding="utf-8",
            )
            (inventories / f"older{SIDECAR_SUFFIX}").write_text(empty, encoding="utf-8")
            records, problems = publication_records(
                calendars,
                "older",
                inventories,
                registered_sources={
                    "artifact.public-domain.example": {
                        "record_type": "artifact",
                        "id": "artifact.public-domain.example",
                        "rights_status": "public-domain",
                    }
                },
            )
        self.assertEqual([], problems)
        decision = decision_for(LatinKey("day", "", "Collect"), body, records)
        self.assertEqual("artifact.public-domain.example", decision.source_id)
        self.assertFalse(decision.permits(STRUCTURE_SURFACES))
        self.assertIn("target-recension", decision.note)


class ProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.room = tempfile.TemporaryDirectory()
        self.sources = Path(self.room.name) / "sources"
        self.calendars = self.sources / "calendars"
        self.inventories = self.sources / "inventories"
        (self.calendars / "demo").mkdir(parents=True)
        self.inventories.mkdir(parents=True)
        self.document = demo_document(
            {"name": "Collect", "source": "composed", "text": "Secretum Latinum."},
            {
                "name": "Acclamation",
                "source": "composed",
                "cycles": {"A": {"source": "composed", "text": "Arcanum A."}},
            },
        )
        (self.calendars / "demo/propers.yaml").write_text(
            yaml.safe_dump(self.document, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
        (self.inventories / f"demo{SIDECAR_SUFFIX}").write_text(
            "\n".join(
                line
                for source_line in render_unresolved_sidecar(
                    "demo", self.document
                ).splitlines()
                for line in (
                    [source_line]
                    if not source_line.startswith("text_sha256 = ")
                    else [
                        source_line,
                        *permitted_nonexact_fields(),
                    ]
                )
            )
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.room.cleanup()

    def test_browser_download_and_print_structure_contain_state_not_wording(self) -> None:
        mass_propers = load_tool("mass-propers")
        built = mass_propers.calendar_structure(self.calendars, "demo", {})
        encoded = json.dumps(built, ensure_ascii=False)
        self.assertNotIn("Secretum Latinum", encoded)
        self.assertNotIn("Arcanum A", encoded)
        propers = built["masses"][0]["propers"]
        self.assertTrue(propers[0]["latin"]["withheld"])
        self.assertTrue(propers[1]["cycles"]["A"]["latin"]["withheld"])

    def test_cli_machine_and_reading_views_do_not_bypass_the_decision(self) -> None:
        command = [
            sys.executable,
            str(ROOT / "tools/mass-propers"),
            "show",
            "--root",
            str(self.calendars),
            "--calendar",
            "demo",
            "--mass",
            "day",
        ]
        machine = subprocess.run(
            [*command, "--format", "json"], check=True, capture_output=True, text=True
        ).stdout
        reading = subprocess.run(command, check=True, capture_output=True, text=True).stdout
        for output in (machine, reading):
            self.assertNotIn("Secretum Latinum", output)
            self.assertNotIn("Arcanum A", output)
        self.assertIn("Latin text unavailable", reading)
        self.assertNotIn("publication basis", reading)
        self.assertNotIn("publication_status", reading)
        self.assertNotIn("publication_basis", reading)
        payload = json.loads(machine)
        self.assertTrue(payload["appointed"][0]["proper"]["latin"]["withheld"])


if __name__ == "__main__":
    unittest.main()
