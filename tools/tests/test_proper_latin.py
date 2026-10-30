"""Latin Proper provenance is per text; publication is a separate decision."""
from __future__ import annotations

import hashlib
import json
import argparse
import subprocess
import sys
import tempfile
import tomllib
import unittest
from types import SimpleNamespace
from importlib.machinery import SourceFileLoader
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]

from tools.tests.test_roman_1962_octnov_commemoration_source_repair import (
    PHASE5_LATIN22, phase5_owner, phase5_predecessor_christmas, digest, canonical,
)
from tools.tests import _source_batch_guards as BATCH_GUARDS
import _calendars  # noqa: E402
from _missal_coverage import latin_evidence  # noqa: E402
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
# Preserve the original two qualified scopes as their own historical control.
LEGACY_QUALIFIED_KEYS = {
    LatinKey(mass, "", proper, "", "", occurrence)
    for mass, form, proper, cycle, occurrence in (
        scope["target"] for scope in json.loads(
            (ROOT / "workflows/reviews/missal-reader-completion-2026-10-26/"
             "gregem-damasus-qualified-rights-adoption.json").read_text()
        )["exact_scopes"])
    if form == "main" and cycle == "all"
}


CURRENT_AUTHORITY_PATH = ROOT / "workflows/reviews/missal-english-completion-2026-10-29/roman-1962/finite-latin-authority-v1.json"
CURRENT_AUTHORITY_RAW = CURRENT_AUTHORITY_PATH.read_bytes()
if hashlib.sha256(CURRENT_AUTHORITY_RAW).hexdigest() != "920299972ab84575183de8c84adcd3f7418bdc46304fbe1d6a4435fad1103ee3":
    raise AssertionError("exact adopted finite Latin authority")
CURRENT_QUALIFIED_SCOPES = {
    LatinKey(*scope["key"]): scope
    for scope in json.loads(CURRENT_AUTHORITY_RAW)["scopes"]
}
QUALIFIED_KEYS = LEGACY_QUALIFIED_KEYS | set(CURRENT_QUALIFIED_SCOPES)
DIRECT_DECLARATION_PATH = ROOT / "workflows/reviews/missal-english-completion-2026-10-29/roman-1962/sources/direct-pd-latin-proof-declaration-v1.json"
DIRECT_DECLARATION_RAW = DIRECT_DECLARATION_PATH.read_bytes()
if hashlib.sha256(DIRECT_DECLARATION_RAW).hexdigest() != "70716afc9012297f8600c837b129332a1b924b9520b8861d9d6ad33ae4f47752":
    raise AssertionError("exact25 direct public-domain proof declaration")
DIRECT_DECLARATION = json.loads(DIRECT_DECLARATION_RAW)
DIRECT_SOURCE_SPECS = {
    LatinKey(**spec["key"]): spec for spec in DIRECT_DECLARATION["records"]
}
PANGE_ASSEMBLY_KEY = LatinKey(
    "mass-of-the-lords-supper", "",
    "Hymn at the Translation of the Blessed Sacrament", "", "", 1,
)
DIRECT_PROOF_ARTIFACTS = {
    "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.english-completion-20261029-saints-chant-latin-10b19922": {
        "sha256": "10b19922a2fc07cd74be90ae8832d093e705247b93491fa155bf9a1090635e82",
        "projected_from": {
            "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.english-completion-20261029-saints-chant-pages-59c31d7f",
            "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ia-scan-pdf-9873693a",
            "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf",
        },
    },
    "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.pentecost-four-chants-20261029-d074f957": {
        "sha256": "d074f957761fb3fbfab186eb899a2ab096ffd62e9ce03e51f776be56dee64f16",
        "projected_from": {
            "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.pentecost-four-chants-20261029-checked-latin-0097a922",
            "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.pentecost-four-chants-20261029-pages",
            "artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf",
        },
    },
}
MARIAN_WRAPPER_KEYS = {
    LatinKey(mass, "", proper, "", "", 1)
    for mass, proper in (
        ("purificatione-beatae-mariae-virginis", "Alleluia"),
        ("apparitione-beatae-mariae-virginis-immaculatae", "Alleluia"),
        ("apparitione-beatae-mariae-virginis-immaculatae", "Tract"),
        ("annuntiatio-beatae-mariae-virginis", "Alleluia"),
        ("sanctissimi-nominis-beatae-mariae-virginis", "Gradual"),
        ("sanctissimi-nominis-beatae-mariae-virginis", "Alleluia"),
        ("sanctissimi-nominis-beatae-mariae-virginis", "Communion"),
        ("beatae-mariae-virginis-a-rosario", "Introit"),
        ("beatae-mariae-virginis-a-rosario", "Alleluia"),
    )
}


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
    def test_ember_advent_lent_orations_keep_source_order_and_exact_form_owners(self):
        # The ordered body oracle is independently collated against both printed
        # target forms; generic ordering cannot distinguish repeated Oratio heads.
        expected = {'advent-ember-saturday': {'longer': [(1, 'Collect', 1, '473f7257116cd8c0d2a86267683cc4fa8bc088fb43dcbec4f70dd27617e97e1d'), (4, 'Oratio', 1, 'c7461c7079181e3c24e5c0fb6eb6b607f432a9f3dc3d4936e199c33cb677e054'), (7, 'Oratio', 2, 'efdb1b2d638d7bba3c33ce95f71aff8f3df138a042de32e16bf1e0d7711a1d1e'), (10, 'Oratio', 3, '1b1a81d0920612209faa58bb6567bd4b5a89e404eb6db484b793ab71ba1121cb'), (13, 'Oratio', 4, '2d6a29be50863d4697c88f7c76f36cd568d1893afb91dc828cbe81919ac142a7'), (16, 'Oratio', 5, '7c0f207aee56711c8e4caf64e2318abe602d7d48771675419dfd1066b484c38b'), (21, 'Secret', 1, '94aab6eefb88e4df85a51f59335d50cb6215afff5fc34d7bf714c22fb7d24b31'), (23, 'Postcommunion', 1, 'dbb05b476bdb7ff698fc903a4ee0426a8f13178e19a2c9d098c9511b0a50b289')], 'shorter': [(1, 'Collect', 1, '473f7257116cd8c0d2a86267683cc4fa8bc088fb43dcbec4f70dd27617e97e1d'), (4, 'Oratio', 1, 'c7461c7079181e3c24e5c0fb6eb6b607f432a9f3dc3d4936e199c33cb677e054'), (9, 'Secret', 1, '94aab6eefb88e4df85a51f59335d50cb6215afff5fc34d7bf714c22fb7d24b31'), (11, 'Postcommunion', 1, '6c898e13277cdd2e3cc88affa700c0b638dab73ee606e4f6e949939bbfb15fd0')]}, 'lent-1-ember-saturday': {'longer': [(1, 'Collect', 1, '8a86af6147dcb73eb0bec31e1101f1a366cec3b7f3c363796afe4a04a6869533'), (4, 'Oratio', 1, 'c6ddb6df9f0a42a9ab9ce039dbc629722143433d60e0645981ece24ccf8f4dd6'), (7, 'Oratio', 2, '46fee93cb038dc64ed59374f11e1c0533c937b14ea0b93bcf568d846a57a5f99'), (10, 'Oratio', 3, 'a36c7c7a95d2050801796aa212e738889a99bb111c2924048602909a6e0495b9'), (13, 'Oratio', 4, 'ecf77a36fe4f22196746da9b2fe0cfc3c68ec9ab7ac42b5affed494a32393884'), (16, 'Oratio', 5, '7c0f207aee56711c8e4caf64e2318abe602d7d48771675419dfd1066b484c38b'), (21, 'Secret', 1, 'e9f5f554d58316aeb07ed474ef629fe23d4263206cd8eed948cdaeca45151ccd'), (23, 'Postcommunion', 1, '6115d2418c3ac487a4b206cda8686e5da8385c0264e530e2c65fd82f4179c781'), (24, 'Oratio', 6, 'ffd76454250595e7b5b42db4ab9af8b8cccdc8d9815dc6ecce3620cff3e1358b')], 'shorter': [(1, 'Collect', 1, '8a86af6147dcb73eb0bec31e1101f1a366cec3b7f3c363796afe4a04a6869533'), (4, 'Oratio', 1, 'c6ddb6df9f0a42a9ab9ce039dbc629722143433d60e0645981ece24ccf8f4dd6'), (9, 'Secret', 1, 'e9f5f554d58316aeb07ed474ef629fe23d4263206cd8eed948cdaeca45151ccd'), (11, 'Postcommunion', 1, '6115d2418c3ac487a4b206cda8686e5da8385c0264e530e2c65fd82f4179c781'), (12, 'Oratio', 2, 'c144bfe62c61c56def5d058e889745e00a1c03af0361b7ba206e898f73061e4c')]}}
        document = _calendars.load_document(CALENDARS, "roman-1962")
        records, problems = read_sidecar(INVENTORIES / "roman-1962-proper-latin-provenance-v1.toml")
        self.assertEqual([], problems)
        masses = {mass["key"]: mass for _, _, mass in _calendars.departures_of(document)}
        for key, form_oracles in expected.items():
            mass = masses[key]
            self.assertEqual("unavailable", mass["ordinary_frame"]["applicability"])
            self.assertEqual(["longer", "shorter"], [form["id"] for form in mass["forms"]])
            for form in mass["forms"]:
                oracle = form_oracles[form["id"]]
                occurrences = {}
                actual = []
                for index, proper in enumerate(form["propers"]):
                    name = proper["name"]
                    if name not in {"Collect", "Secret", "Postcommunion", "Oratio"}:
                        continue
                    occurrences[name] = occurrences.get(name, 0) + 1
                    occurrence = occurrences[name]
                    actual.append((index, name, occurrence, text_sha256(proper["text"])))
                    self.assertEqual("composed", proper["source"])
                    self.assertNotIn("text_status", proper)
                    self.assertNotIn("takes_from", proper)
                    row = records[LatinKey(key, form["name"], name, "", "", occurrence)]
                    self.assertEqual(text_sha256(proper["text"]), row["text_sha256"])
                    self.assertEqual("editorial-projection-exact-to-target", row["relationship"])
                    self.assertEqual(['artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-20.advent-lent-ember-orations-4ba2f77c', 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.advent-lent-ember-orations-la-checked-39b0b0aa'], row["publication_source_ids"])
                    self.assertEqual("permitted", row["publication_status"])
                self.assertEqual(oracle, actual, (key, form["id"]))
        # Equal underlying prayers retain each target occurrence's printed cue.
        advent = masses["advent-ember-saturday"]["forms"]
        post = [next(p["text"] for p in f["propers"] if p["name"] == "Postcommunion") for f in advent]
        self.assertTrue(post[0].rstrip().endswith("Per Dominum."))
        self.assertTrue(post[1].rstrip().endswith("Per Dominum nostrum Jesum Christum."))
        lent = masses["lent-1-ember-saturday"]["forms"]
        for form, ending in zip(lent, ("Per Dominum.", "Per Dominum nostrum Jesum Christum.")):
            self.assertEqual("Postcommunion", form["propers"][-2]["name"])
            final = form["propers"][-1]
            self.assertEqual("Oratio", final["name"])
            self.assertIn("Super populum", final["notes"])
            self.assertNotIn("Super populum", final["text"])
            self.assertNotIn("Humiliate", final["text"])
            self.assertTrue(final["text"].rstrip().endswith(ending))
        historical = registered_artifact('artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.advent-lent-ember-orations-la-checked-39b0b0aa')
        self.assertEqual('39b0b0aa30f03ed3ecad53520b095c551ffc1fe28237635d8d16cea35160eab1', historical["sha256"])
        source = (ROOT / historical["path"]).read_text()
        self.assertIn("Per Dm̃.", source)
        self.assertIn("quæ eos, et a tua voluntáte", " ".join(source.split()))
        self.assertIn("finiátur. Per.", source)
        self.assertNotIn("Per Dominum nostrum Jesum Christum", source)

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
        unchanged = phase5_predecessor_christmas(mass)
        unchanged.pop("notes", None)
        for form in unchanged["forms"]:
            form["propers"] = [p for p in form["propers"]
                               if p["name"] not in {"Collect", "Secret", "Postcommunion"}]
        self.assertEqual('2be17aea48a931cee2ce981fb995323730148601c3b6038897a1db34c860dda6',
                         hashlib.sha256(json.dumps(unchanged, ensure_ascii=False, sort_keys=True,
                                                   separators=(",", ":")).encode()).hexdigest())
        for form in mass["forms"]:
            self.assertEqual({'night': ['Introit', 'Collect', 'Epistle', 'Gradual', 'Alleluia', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'dawn': ['Introit', 'Collect', 'Epistle', 'Gradual', 'Alleluia', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion'], 'day': ['Introit', 'Collect', 'Epistle', 'Gradual', 'Alleluia', 'Gospel', 'Offertory', 'Secret', 'Communion', 'Postcommunion']}[form["id"]], [p["name"] for p in form["propers"]])
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

    def test_2008_collect_owners_distinguish_held_latin_from_unheld_english(self) -> None:
        document = yaml.safe_load((CALENDARS / "postconciliar/propers.yaml").read_text())
        masses = {m["key"]: m for section in document["sections"].values()
                  for m in section["masses"]}
        expected = {"saint-pius-pietrelcina-priest": "pio",
                    "saint-juan-diego-cuauhtlatoatzin": "juan-diego",
                    "our-lady-guadalupe": "guadalupe"}
        artifact = "artifact.holy-see.notitiae.volume-44-numbers-503-504-2008.official-pdf-74c8d174"
        inventory = tomllib.loads((INVENTORIES / "missal-expected-targets-v1.toml").read_text())
        target_by_id = {row["id"]: row for row in inventory["targets"]}
        english = tomllib.loads((INVENTORIES / "postconciliar-proper-translations-v1.toml").read_text())
        latin = tomllib.loads((INVENTORIES / "postconciliar-proper-latin-provenance-v1.toml").read_text())
        for mass_key, suffix in expected.items():
            with self.subTest(mass=mass_key):
                mass = masses[mass_key]
                self.assertEqual("partial", mass["text_status"]["state"])
                found = [p for p in mass["propers"] if p["name"] == "Collect"]
                self.assertEqual(1, len(found))
                proper = found[0]
                self.assertEqual("composed", proper["source"])
                self.assertEqual({"state": "unavailable", "scope": "proper-body",
                                  "body_status": "held-unpublished",
                                  "reasons": [{"kind": "rights-withheld", "source_id": artifact}]},
                                 proper["text_status"])
                self.assertTrue({"text", "incipit", "text_sha256", "provenance"}.isdisjoint(proper))
                self.assertEqual([], [r for r in latin["entries"] if r["mass"] == mass_key])
                target = target_by_id[f"postconciliar:2008:supplement:{suffix}-collect"]
                self.assertEqual("established", target["identity_state"])
                records = [r for r in english["untranslated"] if r["mass"] == mass_key and r["proper"] == "Collect"]
                self.assertEqual(1, len(records))
                row = records[0]
                self.assertEqual(("main", "all", 1, "en", "body", "unavailable"),
                    tuple(row[k] for k in ("form_id", "cycle", "occurrence", "lang", "extent", "availability")))
                self.assertEqual({"kind": "no-exemplar"}, row["reason"])
                self.assertIn("Latin source body is privately held", row["note"])
        sept8 = masses["nativity-blessed-virgin-mary"]
        # This separately admitted module supersedes the earlier two-option
        # packet's source gap; it does not change the three Collect refusals.
        review_root = ROOT / "workflows/reviews/missal-english-completion-2026-10-29/postconciliar"
        admission_raw = (review_root / "phase2-september8-admission.json").read_bytes()
        self.assertEqual("d9ec4ff8b7f8637068025635c394b4b88c2caaf9e848298231b022e828d1326c",
                         hashlib.sha256(admission_raw).hexdigest())
        admission = json.loads(admission_raw)
        names = [admission["known_target"][2], admission["retained_minimum_gap"][2]]
        offerings = [p for p in sept8["propers"] if p["name"].startswith("Prayer over the Offerings")]
        self.assertEqual(names, [p["name"] for p in offerings])
        self.assertEqual(["supplementum-2008", "retained-earlier-option"],
                         [p["ordinary_disposition"]["option"] for p in offerings])
        self.assertTrue(all(p["ordinary_disposition"]["kind"] == "alternative"
                            and p["ordinary_disposition"]["group"] == "september-8-offerings"
                            for p in offerings))
        for proper in offerings:
            self.assertEqual("composed", proper["source"])
            self.assertEqual(("unavailable", "proper-body"),
                             (proper["text_status"]["state"], proper["text_status"]["scope"]))
            self.assertTrue({"text", "text_sha256", "provenance"}.isdisjoint(proper))
        self.assertEqual("Unigeniti tui, Domine, nobis succurrat humanitas", offerings[0]["incipit"])
        self.assertNotIn("incipit", offerings[1])
        self.assertEqual([{"kind": "witness-gap", "source_id": admission["source_passage"]}],
                         offerings[0]["text_status"]["reasons"])
        self.assertEqual([{"kind": "no-exemplar"}], offerings[1]["text_status"]["reasons"])
        self.assertIn(admission["target_passage"], offerings[0]["notes"])
        self.assertEqual(1, len([r for r in english["entries"]
                                if r["mass"] == sept8["key"] and r["proper"] == names[0]]))
        retained = [r for r in english["untranslated"]
                    if r["mass"] == sept8["key"] and r["proper"] == names[1]]
        self.assertEqual(1, len(retained))
        self.assertEqual({"kind": "no-exemplar"}, retained[0]["reason"])
        # Superoblata followed by Vel establishes a bounded minimum, not the
        # complete prior option count or wording of a whole Mass.
        seat_raw = (review_root / "phase2-september8-seating-successor.json").read_bytes()
        self.assertEqual("01108c4a0e946781be94d118e3bfbd80f78d89c10fae83702267aa0f3eed96e0",
                         hashlib.sha256(seat_raw).hexdigest())
        seat = json.loads(seat_raw)
        ordinary = tomllib.loads((INVENTORIES / "postconciliar-ordo-missae-v1.toml").read_text())
        slot = next(row for row in ordinary["slots"] if row["key"] == seat["ordinary_slot_key"])
        self.assertEqual(seat["ordinary_anchor"], slot["after"])
        self.assertEqual(names, slot["propers"])

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
            # Phase 2 adds fifteen new owners and restores three removed ones:
            # eighteen complete October-November commemoration prayers.
            # Phase 3: seventeen new owners, two restored Collects; Dedication
            # changes four appointments but no body or ledger row.
            "roman-1962": (1289, 23),
            "roman-pre-1955": (0, 0),
        }
        for calendar, (total, repeated) in expected.items():
            records, problems = read_sidecar(
                INVENTORIES / f"{calendar}{SIDECAR_SUFFIX}"
            )
            self.assertEqual([], problems)
            if calendar != "roman-pre-1955":
                # Current repairs/restorations keep their exact live proof map.
                # Historical counts describe the original ledger values, not
                # the current values of owners that happened to exist then.
                BATCH_GUARDS.assert_current_latin(records, calendar)
                archived = tomllib.loads(BATCH_GUARDS.historical_text(
                    f"src/sources/inventories/{calendar}{SIDECAR_SUFFIX}"
                ))
                records = {
                    LatinKey.from_mapping(row): row
                    for entry in archived["entries"]
                    for row in [{**archived["defaults"], **entry}]
                }
                self.assertEqual(
                    BATCH_GUARDS.fixture()["latin_baseline_rows"][calendar],
                    {BATCH_GUARDS.key_string(key): BATCH_GUARDS.digest(
                        BATCH_GUARDS.canonical(row)
                    ) for key, row in records.items()},
                )
            self.assertEqual(total, len(records))
            self.assertEqual(
                # 46 since 2026-10-01: KI-054 published 31 quarantined bodies.
                {"postconciliar": 329, "roman-1962": 20}.get(calendar, 0),
                sum(row.get("body_status") == "removed" for row in records.values()),
            )
            # Four duplicate-name pairs and one six-item procession are all
            # separate permission decisions, never last-row-wins dict entries.
            # Advent/Lent Ember Oratio rows add ten repeated-name decisions.
            self.assertEqual(repeated, sum(key.occurrence > 1 for key in records))

    def test_publication_loader_validates_production_source_metadata(self) -> None:
        # 1114 since 2026-10-01: St Angela Merici's Secret and Postcommunion.
        # 1120 since 2026-10-20 (C3): St Lucy's Communion has its own body.
        expected = {"postconciliar": 329, "roman-1962": 1289, "roman-pre-1955": 1289}
        for calendar, count in expected.items():
            records, problems = publication_records(CALENDARS, calendar, INVENTORIES)
            self.assertEqual([], problems)
            records = BATCH_GUARDS.historical_latin_records(records, calendar)
            self.assertEqual(count, len(records))

    def test_exact25_direct_sources_have_distinct_records_and_production_decisions(self) -> None:
        self.assertEqual(25, len(DIRECT_SOURCE_SPECS))
        self.assertEqual(3, len(DIRECT_DECLARATION["primary_artifacts"]))
        self.assertEqual(
            {BATCH_GUARDS.key_string(key): spec for key, spec in DIRECT_SOURCE_SPECS.items()},
            BATCH_GUARDS.fixture()["direct_pd_permitted_specs"],
        )
        records, problems = publication_records(CALENDARS, "roman-1962", INVENTORIES)
        self.assertEqual([], problems)
        bodies = {key: text for key, text, state in body_owners(
            _calendars.load_document(CALENDARS, "roman-1962")) if state == "present"}
        for key, expected in DIRECT_SOURCE_SPECS.items():
            with self.subTest(key=key):
                row, text = records[key], bodies[key]
                self.assertEqual(expected["record"], row)
                self.assertEqual(expected["body_sha256"], hashlib.sha256(text.encode()).hexdigest())
                decision = decision_for(key, text, records)
                self.assertTrue(decision.permits(SURFACES))
                self.assertEqual(expected["production_decision"], decision.projection(SURFACES))
                self.assertFalse(decision_for(key, text + " changed", records).permits(SURFACES))
                for field, value in (("publication_basis", "unresolved"), ("surfaces", []),
                                     ("publication_status", "unresolved")):
                    changed = dict(records)
                    changed[key] = dict(row, **{field: value})
                    self.assertFalse(decision_for(key, text, changed).permits(SURFACES))
        for expected in DIRECT_DECLARATION["primary_artifacts"]:
            with self.subTest(artifact=expected["id"]):
                self.assertEqual(expected["record"], registered_artifact(expected["id"]))
                self.assertEqual(expected["sha256"], hashlib.sha256((ROOT / expected["path"]).read_bytes()).hexdigest())
                self.assertEqual(expected["payload_sha256"], hashlib.sha256((ROOT / expected["payload_path"]).read_bytes()).hexdigest())
                self.assertEqual("public-domain", expected["record"]["rights_status"])

    def assert_pange_source_assembly(self, row: dict) -> None:
        # This exact reviewed assembly is source-exact; the named 1962 referral
        # does not supply a full-word target collation or a new cue permission.
        review_raw = (ROOT / "workflows/reviews/missal-english-completion-2026-10-29/roman-1962/sources/source-review-7e5ddbe30004c407.json").read_bytes()
        self.assertEqual("7e5ddbe30004c40786311c8914bc394ebfa6f2e0d3c0de1a1ae8c9395ca4b67b", hashlib.sha256(review_raw).hexdigest())
        review = json.loads(review_raw)
        hashes = review["candidate"]["body_sha256"]
        grade = review["acceptance"]["vocabulary_and_source_grade"]
        ids = [
            "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.pange-source-prescribed-assembly-53086b37",
            "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-09-03.triduum-orations-21aa7a98",
            "artifact.prosper-gueranger.the-liturgical-year.english-duffy-1879-volume-10.pange-lingua-latin-checked-20261029-15c03ec1",
        ]
        self.assertEqual(ids, row["publication_source_ids"])
        self.assertEqual(hashes["latin_composite"], row["text_sha256"])
        self.assertEqual("exact-transcription", row["relationship"])
        self.assertEqual(grade["latin_relationship"], row["relationship"])
        self.assertEqual("passage.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.pange-source-prescribed-assembly", row["source_id"])
        self.assertEqual("passage.catholic-church.missale-romanum.vatican-typica-1962.holy-thursday-pange-hymn-referral-20261029", row["verification_source_id"])
        self.assertEqual("public-domain", row["publication_basis"])
        self.assertEqual(set(SURFACES), set(row["surfaces"]))
        self.assertTrue(row["transformations"])
        # Recheck the accepted Latin carrier/passage and inherited cue metadata;
        # the latter is a project carrier, not an independent PD printing.
        project_prefix = "src/sources/works/triptych/roman-1962-latin-proper-editorial-projection/"
        latin_prefix = "src/sources/works/prosper-gueranger/"
        for source in (review["candidate"]["source_files"] + review["existing_key_ancestors"]):
            path = source.get("repository_path", source.get("path"))
            if path.startswith((project_prefix, latin_prefix)):
                self.assertEqual(source["sha256"], hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), path)
        carrier = tomllib.loads((EDITORIAL_PROJECTION / "editions/2026-10-29-editorial-projection/artifacts/pange-source-prescribed-assembly-53086b37/artifact.toml").read_text())
        cue_carrier = tomllib.loads((EDITORIAL_PROJECTION / "editions/2026-09-03-editorial-projection/artifacts/triduum-orations-21aa7a98/artifact.toml").read_text())
        hymn = registered_artifact(ids[2])
        self.assertEqual(ids[0], carrier["id"])
        self.assertEqual(ids[1], cue_carrier["id"])
        self.assertEqual("project-created", carrier["rights_status"])
        self.assertEqual("project-created", cue_carrier["rights_status"])
        self.assertEqual("public-domain", hymn["rights_status"])
        self.assertEqual(ids[1:] + ["artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf"], carrier["projected_from"])
        assembled = (ROOT / carrier["path"]).read_bytes()
        hymn_bytes = (ROOT / hymn["path"]).read_bytes()
        cue_bytes = assembled.removesuffix(b"\n" + hymn_bytes)
        self.assertEqual(hashes["latin"], hashlib.sha256(hymn_bytes).hexdigest())
        self.assertEqual(hashes["old_cue"], hashlib.sha256(cue_bytes).hexdigest())
        self.assertEqual(cue_bytes + b"\n" + hymn_bytes, assembled)
        self.assertEqual(hashes["latin_composite"], hashlib.sha256(assembled).hexdigest())
        self.assertEqual(6, len(hymn_bytes.decode().strip().split("\n\n")))
        document = _calendars.load_document(CALENDARS, "roman-1962")
        text = next(text for key, text, state in body_owners(document)
                    if key == PANGE_ASSEMBLY_KEY and state == "present")
        self.assertEqual(assembled.decode(), text)
        mass = next(mass for _, _, mass in _calendars.departures_of(document)
                    if mass["key"] == PANGE_ASSEMBLY_KEY.mass)
        proper = next(proper for proper in mass["propers"]
                      if proper["name"] == PANGE_ASSEMBLY_KEY.proper)
        self.assertEqual([{"kind": "rubric", "offset": 0,
                           "text": cue_bytes.decode().removesuffix("\n")}],
                         proper["text_structure"]["actions"])
        self.assertEqual(147, len(proper["text_structure"]["actions"][0]["text"]))
        records, problems = publication_records(CALENDARS, "roman-1962", INVENTORIES)
        self.assertEqual([], problems)
        self.assertEqual(row, records[PANGE_ASSEMBLY_KEY])
        decision = decision_for(PANGE_ASSEMBLY_KEY, text, records)
        self.assertTrue(decision.permits(SURFACES))
        self.assertEqual({"relationship": "unresolved", "collation": "collated", "publication_basis": "public-domain"}, latin_evidence(decision.projection(SURFACES)))
        self.assertEqual(grade["actual_latin_coverage"], latin_evidence(decision.projection(SURFACES)))
        self.assertFalse(decision_for(PANGE_ASSEMBLY_KEY, text + " changed", records).permits(SURFACES))

    def test_production_ledgers_publish_only_the_exact_historical_recoveries(self) -> None:
        permitted = []
        nonpermitted = []
        for calendar in ("postconciliar", "roman-1962", "roman-pre-1955"):
            records, _ = read_sidecar(INVENTORIES / f"{calendar}{SIDECAR_SUFFIX}")
            if calendar != "roman-pre-1955":
                BATCH_GUARDS.assert_current_latin(records, calendar)
            for key, row in records.items():
                (permitted if row["publication_status"] == "permitted" else nonpermitted).append(
                    (calendar, key, row)
                )
        roman = {key for calendar, key, _ in permitted if calendar == "roman-1962"}
        # The exact25 direct-source proofs are a separate closed partition;
        # legacy project bodies retain every namespace and shape check below.
        # Every legacy body is pinned by SHAPE rather than by key. Pinning
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
        # Accepted Phase 1: 1187. Phase 2 independently adds exactly eighteen
        # full bodies (fifteen new ledger rows, three restored Saturninus rows).
        # Phase 3 adds nineteen complete bodies on two artifact-specific pairs.
        BATCH_GUARDS.assert_permitted_owners(permitted)
        direct = [(calendar, key, row) for calendar, key, row in permitted
                  if not row["publication_source_ids"][0].startswith(
                      "artifact.triptych.roman-1962-latin-proper-editorial-projection.")]
        self.assertEqual({("roman-1962", key) for key in DIRECT_SOURCE_SPECS},
                         {(calendar, key) for calendar, key, _ in direct})
        self.assertEqual(25, len(direct))
        projection_permitted = [item for item in permitted if item not in direct]
        self.assertEqual(len(permitted), len(projection_permitted) + len(direct))
        self.assertEqual(QUALIFIED_KEYS, {key for _, key, row in permitted
                                        if row["publication_basis"] == "qualified-nonoriginal-adaptation"})
        self.assertEqual(1269, len({BATCH_GUARDS.key_string(k) for k in roman} & set(BATCH_GUARDS.fixture()["latin_baseline_present_keys"])))
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
                    # Ignatius Postcommunion only (francis-one-ignatius-proof-adoption.json).
                    "artifact.catholic-church.missale-romanum."
                    "pustet-ratisbon-1862.ignatius-petition-formula-text-20261026",
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
                "publication_source_ids": {"artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.christ-the-king-orations-la-checked-32eecc40", "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.theodore-two-orations-la-checked-638fc0c5", "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.all-saints-four-propers-la-checked-82edd79a", 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.immaculate-conception-four-propers-la-checked-18084e74', "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.christmas-nine-orations-la-checked-825c69f4", 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.advent-lent-ember-orations-la-checked-39b0b0aa', 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.adapted-primary-readings-la-checked-e3a67098', "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ember-pentecost-september-la-checked-ea162251", 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.uncited-eight-chants-la-checked-d05badcc', 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.all-souls-twelve-bodies-la-checked-4a41c7e8'},
                "projected_from": {"artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.christ-the-king-orations-la-checked-32eecc40", target_artifact, "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.theodore-two-orations-la-checked-638fc0c5", "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.all-saints-four-propers-la-checked-82edd79a", 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.immaculate-conception-four-propers-la-checked-18084e74', "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.christmas-nine-orations-la-checked-825c69f4", 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.advent-lent-ember-orations-la-checked-39b0b0aa', 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.adapted-primary-readings-la-checked-e3a67098', "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.ember-pentecost-september-la-checked-ea162251", 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.uncited-eight-chants-la-checked-d05badcc', 'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.all-souls-twelve-bodies-la-checked-4a41c7e8'},
            },
            # One source-proved correction; existing permission count is unchanged.
            "editorial-projection-2026-10-21": {
                "artifact_id": 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-21.september-ember-wednesday-collect-7124589a',
                "publication_source_ids": {'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.september-ember-wednesday-collect-la-checked-ddf31f59'},
                "projected_from": {'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.september-ember-wednesday-collect-la-checked-ddf31f59', target_artifact},
            },
            "editorial-projection-2026-10-22": {
                "artifact_id": "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.boniface-three-orations-ae811235",
                "publication_source_ids": {
                    "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.boniface-page-445-883fb31d",
                },
                "projected_from": {
                    "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.boniface-page-445-883fb31d",
                    target_artifact,
                },
            },
        }

        # Keep the accepted Boniface witness pair exact. The second artifact
        # in this edition has its own independently proved bounded page set;
        # permitting either pair must not permit mixing their witnesses.
        october22_artifact_specs = {
            projection_specs["editorial-projection-2026-10-22"]["artifact_id"]:
                projection_specs["editorial-projection-2026-10-22"],
            "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase2-octnov-commemorations-20261022": {
                "artifact_id": "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase2-octnov-commemorations-20261022",
                "publication_source_ids": {
                    "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase2-octnov-commemoration-pages-20261022",
                },
                "projected_from": {
                    "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase2-octnov-commemoration-pages-20261022",
                    target_artifact,
                },
            },
        }
        # Separate Phase3 pairs: the full named Ursula petition is in Mame1922,
        # not in the older Pustet prayer that remains an inadequate witness.
        october22_artifact_specs.update({
            "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-winter-eighteen-orations-20261022": {
                "artifact_id": "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-winter-eighteen-orations-20261022",
                "publication_source_ids": {
                    "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-winter-oration-pages-20261022",
                },
                "projected_from": {
                    "artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase3-winter-oration-pages-20261022",
                    target_artifact,
                },
            },
            "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-ursula-postcommunion-20261022": {
                "artifact_id": "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase3-ursula-postcommunion-20261022",
                "publication_source_ids": {
                    "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase3-ursula-postcommunion-page-20261022",
                },
                "projected_from": {
                    "artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase3-ursula-postcommunion-page-20261022",
                    target_artifact,
                },
            },
        })
        # Phase4 exact pairs; Common retains its1862 OCR anchor plus scoped images.
        october22_artifact_specs.update({'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-mayoct-alexander-twentytwo-orations-20261022': {'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-mayoct-alexander-twentytwo-orations-20261022', 'publication_source_ids': {'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-mayoct-alexander-oration-pages-20261022'}, 'projected_from': {'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-mayoct-alexander-oration-pages-20261022', 'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'}}, 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-hilary-postcommunion-20261022': {'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-hilary-postcommunion-20261022', 'publication_source_ids': {'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase4-hilary-doctor-pontiff-pages-20261022'}, 'projected_from': {'artifact.catholic-church.missale-romanum.1922-tours-mame-editio-quarta-iuxta-typicam.phase4-hilary-doctor-pontiff-pages-20261022', 'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'}}, 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-common-virgin-ii-two-word-repair-ce623d9f': {'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-common-virgin-ii-two-word-repair-ce623d9f', 'publication_source_ids': {'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.missale-romanum-1862-text-f34bc7cf'}, 'projected_from': {'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf', 'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase4-common-virgin-ii-orations-pages-698-699-20261022'}}})
        # Phase5 is exactly 10 Pustet pairs, 5 Pustet triples, 6 Schott
        # pairs and one Schott triple. No arbitrary third witness is allowed.
        october22_artifact_specs.update({'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022': {'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022',
                                                                                                                                              'projected_from': {'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022',
                                                                                                                                                                 'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022',
                                                                                                                                                                 'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'},
                                                                                                                                              'publication_source_ids': {'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-petitions-and-formulas-20261022'}},
 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022': {'artifact_id': 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022',
                                                                                                                                              'projected_from': {'artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022',
                                                                                                                                                                 'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022',
                                                                                                                                                                 'artifact.catholic-church.missale-romanum.vatican-typica-1962.cmaa-facsimile-pdf'},
                                                                                                                                              'publication_source_ids': {'artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022'}}})
        BATCH_GUARDS.assert_current_projection_source_files()
        BATCH_GUARDS.add_projection_specs(projection_specs)
        batch_artifact_specs = BATCH_GUARDS.projection_artifact_specs()
        phase5_specs = {LatinKey(**s["key"]): s for s in PHASE5_LATIN22}
        phase5_groups = {}
        phase5_supplements = set()
        used_projection_editions = set()
        supplemented = []
        ignatius_witnessed = set()
        for calendar, key, row in projection_permitted:
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
                if key == PANGE_ASSEMBLY_KEY:
                    self.assertEqual("editorial-projection-2026-10-29", edition)
                    self.assert_pange_source_assembly(row)
                    supplemented.append((key, row["publication_source_ids"][2:]))
                    continue
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
                self.assertEqual(
                    "qualified-nonoriginal-adaptation" if key in QUALIFIED_KEYS else "public-domain",
                    row["publication_basis"])
                self.assertEqual(set(SURFACES), set(row["surfaces"]))
                if key in CURRENT_QUALIFIED_SCOPES:
                    scope = CURRENT_QUALIFIED_SCOPES[key]
                    self.assertEqual(scope["row_sha256"], hashlib.sha256(canonical(row).encode()).hexdigest())
                    self.assertEqual(scope["body_sha256"], row["text_sha256"])
                    self.assertEqual(scope["source_id"], row["source_id"])
                    self.assertEqual(scope["verification_source_id"], row["verification_source_id"])
                    self.assertEqual(scope["publication_source_ids"], row["publication_source_ids"])
                # The 2026-09-03 edition carries one projection artifact per
                # backfill lane, so a row names an artifact *of* that edition
                # rather than one fixed id; the public-domain witness beside it
                # is still pinned exactly.
                ids = row["publication_source_ids"]
                self.assertGreaterEqual(len(ids), 2, ids)
                if ids[1].endswith(".ignatius-petition-formula-text-20261026"):
                    ignatius_witnessed.add((calendar, key))
                if edition in BATCH_GUARDS.projection_specs():
                    self.assertIn(ids[0], batch_artifact_specs)
                    spec = batch_artifact_specs[ids[0]]
                if edition == "editorial-projection-2026-10-22":
                    self.assertIn(ids[0], october22_artifact_specs)
                    spec = october22_artifact_specs[ids[0]]
                    if key in phase5_specs:
                        accepted = phase5_specs[key]
                        self.assertEqual(accepted["publication_source_ids"], ids)
                        self.assertEqual(accepted["row_sha256"], digest(canonical(row)))
                        phase5_groups[(ids[0], len(ids))] = phase5_groups.get((ids[0], len(ids)), 0) + 1
                        if len(ids) == 3:
                            phase5_supplements.add(key)
                    else:
                        self.assertEqual(3 if ids[0] == 'artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase4-common-virgin-ii-two-word-repair-ce623d9f' else 2, len(ids), ids)
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
                    if key in QUALIFIED_KEYS:
                        # Disclosed attestations, not a same-printing basis;
                        # assert_supplemented_owners pins their exact ids.
                        continue
                    if key == LatinKey("s-teresiae-a-iesu-infante-virginis", "", "Collect", "", "", 1):
                        # Original bounded Schott petition/Pustet conclusion case.
                        self.assertEqual(['artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022', 'artifact.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929.phase5-latin22-seven-historical-prayers-20261022', 'artifact.catholic-church.missale-romanum.pustet-ratisbon-1862.phase5-latin22-conclusion-authority-20261022'], ids)
                        self.assertEqual("edition.anselm-schott.das-vollstandige-romische-messbuch.herder-second-revised-1929", witness["edition_id"])
                        self.assertEqual("edition.catholic-church.missale-romanum.pustet-ratisbon-1862", supplement["edition_id"])
                    elif BATCH_GUARDS.explicit_cross_supplement(key, extra):
                        BATCH_GUARDS.assert_explicit_cross_supplement(key, ids, extra, witness, supplement)
                    else:
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
        # The 2026-09-03 edition admits the Ignatius artifact for one row only.
        self.assertEqual({("roman-1962", LatinKey("s-ignatii-episcopi-martyris", "", "Postcommunion", "", "", 1))},
                         ignatius_witnessed)
        self.assertEqual(2, len(LEGACY_QUALIFIED_KEYS))
        self.assertEqual(16, len(CURRENT_QUALIFIED_SCOPES))
        self.assertEqual(18, len(QUALIFIED_KEYS))
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
        # Direct-source proofs also retain independently declared project
        # supplements; account for them without applying projection shape rules.
        direct_supplements = [(key, row["publication_source_ids"][2:])
                              for _, key, row in direct
                              if len(row["publication_source_ids"]) > 2]
        self.assertEqual(24, len(direct_supplements))
        self.assertEqual(set(DIRECT_PROOF_ARTIFACTS),
                         {artifact for _, ids in direct_supplements for artifact in ids})
        BATCH_GUARDS.assert_supplemented_owners(supplemented + direct_supplements)
        historical_rows = tomllib.loads(BATCH_GUARDS.historical_text(BATCH_GUARDS.LATIN_PATH))["entries"]
        historical_supplemented = [(LatinKey.from_mapping(row), row["publication_source_ids"][2:]) for row in historical_rows if row.get("publication_status") == "permitted" and len(row.get("publication_source_ids", [])) > 2]
        self.assertEqual(52, len(historical_supplemented), historical_supplemented)
        self.assertEqual({BATCH_GUARDS.key_string(k) for k, ids in historical_supplemented}, set(BATCH_GUARDS.fixture()["latin_baseline_supplemented_keys"]))
        self.assertEqual({('artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022', 2): 10,
 ('artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-pustet-projection-20261022', 3): 5,
 ('artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022', 2): 6,
 ('artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-22.phase5-latin22-schott-projection-20261022', 3): 1}, phase5_groups)
        self.assertEqual({LatinKey(**k) for k in [{'mass': 'thursday-after-ash-wednesday', 'form': '', 'proper': 'Oratio super populum', 'course': '', 'cycle': '', 'occurrence': 1}, {'mass': 'friday-after-ash-wednesday', 'form': '', 'proper': 'Oratio super populum', 'course': '', 'cycle': '', 'occurrence': 1}, {'mass': 'lent-1-monday', 'form': '', 'proper': 'Oratio super populum', 'course': '', 'cycle': '', 'occurrence': 1}, {'mass': 'lent-1-ember-wednesday', 'form': '', 'proper': 'Oratio', 'course': '', 'cycle': '', 'occurrence': 1}, {'mass': 'lent-1-ember-wednesday', 'form': '', 'proper': 'Oratio super populum', 'course': '', 'cycle': '', 'occurrence': 1}, {'mass': 's-teresiae-a-iesu-infante-virginis', 'form': '', 'proper': 'Collect', 'course': '', 'cycle': '', 'occurrence': 1}]}, phase5_supplements)

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
                    if artifact["id"] in DIRECT_PROOF_ARTIFACTS:
                        # These two carriers supplement the exact direct-PD
                        # proofs; neither serves as a primary publication body.
                        proof = DIRECT_PROOF_ARTIFACTS[artifact["id"]]
                        self.assertNotIn(artifact["id"],
                                         {row["publication_source_ids"][0] for _, _, row in permitted})
                        self.assertEqual("project-created", artifact["rights_status"])
                        self.assertTrue(artifact["transformation"].strip())
                        self.assertEqual(proof["projected_from"], set(artifact["projected_from"]))
                        self.assertEqual(proof["sha256"], artifact["sha256"])
                        self.assertEqual(proof["sha256"], hashlib.sha256((ROOT / artifact["path"]).read_bytes()).hexdigest())
                        continue
                    artifact_spec = spec
                    if edition in BATCH_GUARDS.projection_specs():
                        self.assertIn(artifact["id"], batch_artifact_specs)
                        artifact_spec = batch_artifact_specs[artifact["id"]]
                        self.assertEqual(artifact_spec["projected_from"], set(artifact["projected_from"]))
                    if edition == "editorial-projection-2026-10-22":
                        self.assertIn(artifact["id"], october22_artifact_specs)
                        artifact_spec = october22_artifact_specs[artifact["id"]]
                    self.assertEqual("project-created", artifact["rights_status"])
                    self.assertTrue(artifact["transformation"].strip())
                    # An artifact stands on the witnesses its own masses used,
                    # which is a subset of what the edition may rest on: within
                    # one lane most formularies take the Pustet and a few take
                    # the Mame. The target must always be there.
                    stands_on = set(artifact["projected_from"])
                    self.assertTrue(
                        stands_on <= artifact_spec["projected_from"],
                        sorted(stands_on - artifact_spec["projected_from"]),
                    )
                    self.assertIn(target_artifact, stands_on)
                    if edition == "editorial-projection-2026-10-22":
                        self.assertEqual(artifact_spec["projected_from"], stands_on)
        # Direct25 payloads and actual decisions are checked separately above;
        # this range projection applies only to the project passage namespace.
        marian_wrappers = set()
        for _, key, row in projection_permitted:
            passage = passages[row["source_id"]]
            self.assertEqual(row["publication_source_ids"][0], passage["artifact_id"])
            artifact = artifacts[passage["artifact_id"]]
            payload = (ROOT / artifact["path"]).read_text().splitlines(
                keepends=True
            )
            projected_body = "".join(
                line
                for start, end in passage["physical_line_ranges"]
                for line in payload[start - 1 : end]
            )
            if artifact["id"] == "artifact.triptych.roman-1962-latin-proper-editorial-projection.editorial-projection-2026-10-29.marian-ancient-chants-20261029":
                # This exact nine-body carrier records one identity line before
                # each Latin body. The identity line is not prayer wording.
                self.assertIn(key, MARIAN_WRAPPER_KEYS)
                marian_wrappers.add(key)
                self.assertEqual("94e82bd101d9f2b2251f8e48acc72e3aed0b9332975128b9fe162802e0782935",
                                 hashlib.sha256((ROOT / artifact["path"]).read_bytes()).hexdigest())
                selected = projected_body.splitlines(keepends=True)
                self.assertEqual(2, len(selected))
                self.assertEqual(f"{key.mass} | main | {key.proper} | all | 1\n", selected[0])
                projected_body = selected[1]
            self.assertEqual(row["text_sha256"], text_sha256(projected_body))
        self.assertEqual(MARIAN_WRAPPER_KEYS, marian_wrappers)
        # Preserve the post-Anthony historical348 control independently of the
        # current epoch, which also restores Silvester and Palm ordinals5/6.
        historical_nonpermitted = []
        anthony_key = LatinKey("s-antonii-padua-confessoris-ecclesiae-doctoris", "", "Collect", "", "", 1)
        for calendar in ("postconciliar", "roman-1962"):
            archived = tomllib.loads(BATCH_GUARDS.historical_text(
                f"src/sources/inventories/{calendar}{SIDECAR_SUFFIX}"))
            historical_nonpermitted.extend(
                row for entry in archived["entries"]
                for row in [{**archived["defaults"], **entry}]
                if row["publication_status"] != "permitted"
                and not (calendar == "roman-1962" and LatinKey.from_mapping(row) == anthony_key)
            )
        self.assertEqual(348, len(historical_nonpermitted))
        self.assertEqual(345, len(nonpermitted))
        collated = [
            item for item in nonpermitted if item[2]["provenance_status"] == "collated"
        ]
        self.assertEqual(3, len(collated))
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
        # Vianney's named Collect is now exact on the bounded Schott1929 Latin.
        vianney_key = LatinKey("s-ioannis-mariae-vianney-confessoris", "", "Collect", "", "", 1)
        records, problems = publication_records(CALENDARS, "roman-1962", INVENTORIES)
        self.assertEqual([], problems)
        accepted = phase5_owner(_calendars.load_document(CALENDARS, "roman-1962"),
                                vianney_key, records)
        self.assertIn("sanctum Joannem Mariam", accepted["body"])
        self.assertTrue(accepted["body"].endswith("eundem Dominum.\n"))
        self.assertEqual([], [item for item in collated if item[1] == vianney_key])

        # The seventeen the Pustet review withheld are published as of
        # 2026-09-03, on the 1922 Mame, under the rule that a witness must carry
        # the same WORDS and not the same string. That review's findings about
        # the Pustet stand and are still checked by
        # test_roman_pustet_common_collation; what changed is that a non-exact
        # Pustet page no longer keeps a body off every surface, because the
        # repository publishes its own declared orthography and has never served
        # an exact 1962 string anywhere. Only St Albert's three remain collated
        # but withheld; Vianney now has the exact independently dated Schott witness.
        pustet = [
            item
            for item in collated
            if item not in st_albert
        ]
        self.assertEqual(0, len(pustet))
        unresolved = [
            row for _, _, row in nonpermitted if row["provenance_status"] == "unresolved"
        ]
        # The same historical post-Anthony345 remains a separate exact control.
        self.assertEqual(345, sum(row["provenance_status"] == "unresolved"
                                  for row in historical_nonpermitted))
        self.assertEqual(342, len(unresolved))
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

    def test_held_unpublished_has_no_ledger_and_projects_only_neutral_state(self) -> None:
        source_id = "artifact.demo.held"
        status = {
            "state": "unavailable", "scope": "proper-body",
            "body_status": "held-unpublished",
            "reasons": [{"kind": "rights-withheld", "source_id": source_id}],
        }
        proper = {"name": "Collect", "source": "composed", "text_status": status}
        document = demo_document(proper)
        self.assertEqual([], list(body_owners(document)))
        with tempfile.TemporaryDirectory() as room:
            sources = Path(room) / "sources"
            calendar_dir = sources / "calendars/demo"
            inventory_dir = sources / "inventories"
            calendar_dir.mkdir(parents=True)
            inventory_dir.mkdir()
            calendar = calendar_dir / "propers.yaml"
            calendar.write_text(yaml.safe_dump(document, sort_keys=False))
            sidecar = inventory_dir / f"demo{SIDECAR_SUFFIX}"
            sidecar.write_text(render_unresolved_sidecar("demo", document).replace(
                "\n[defaults]\n", "\nentries = []\n\n[defaults]\n", 1))
            self.assertEqual([], sidecar_problems(
                [calendar], inventory_root=inventory_dir, required=True,
                registered_source_ids={source_id}))
            # A made-up former owner is forbidden, even with a syntactically
            # well-formed fixture hash: it is an orphan, not source evidence.
            sidecar.write_text(toml_ledger(
                f'text_sha256 = "{text_sha256("Fixture former words.")}"\n'
                'body_status = "removed"'))
            self.assertTrue(any("orphan entry" in item for item in sidecar_problems(
                [calendar], inventory_root=inventory_dir, required=True,
                registered_source_ids={source_id})))
        public = load_tool("mass-propers")
        wanted_latin = {"target": "Collect", "state": "unavailable",
                        "held": False, "available": False, "withheld": True}
        for surfaces in (STRUCTURE_SURFACES, CLI_SURFACES, SURFACES):
            with self.subTest(surfaces=surfaces):
                clean = sanitize_mass(document["sections"]["01"]["masses"][0], {}, surfaces)
                self.assertEqual(wanted_latin, clean["propers"][0]["latin"])
                visible = public.rights_safe_copy(clean)["propers"][0]
                self.assertEqual({"state": "unavailable", "scope": "proper-body"},
                                 visible["text_status"])
                self.assertEqual(wanted_latin, visible["latin"])
                self.assertNotIn("text", visible)
                self.assertNotIn("body_status", json.dumps(visible))
                self.assertNotIn(source_id, json.dumps(visible))
        # The projection also refuses accidentally resident private words;
        # validation independently rejects the contradictory source shape.
        invalid = {**proper, "text": "Private fixture words."}
        for invalid_status in (status, {**status, "state": "partial"},
                               {**status, "scope": "missal-formulary"},
                               {**status, "reasons": [{"kind": "no-exemplar"}]}):
            projected = sanitize_proper({**invalid, "text_status": invalid_status},
                                       LatinKey("day", "", "Collect"), {}, SURFACES)
            self.assertNotIn("text", projected)
            self.assertEqual(wanted_latin, projected["latin"])

    def test_held_unpublished_checker_requires_exact_registered_rights_witness(self) -> None:
        checker = load_tool("check-calendar-masses")
        exact = "artifact.demo.held"
        broad = "edition.demo"
        checker.source_ids = lambda: ({exact, broad}, None)
        checker.source_records = lambda: ({
            exact: SimpleNamespace(record_type="artifact"),
            broad: SimpleNamespace(record_type="edition"),
        }, None)
        proper = {
            "name": "Collect", "source": "composed",
            "text_status": {"state": "unavailable", "scope": "proper-body",
                            "body_status": "held-unpublished",
                            "reasons": [{"kind": "rights-withheld", "source_id": exact}]},
        }
        problems = []
        checker.check_proper("demo", proper, problems)
        self.assertEqual([], problems)
        variants = []
        def changed():
            return json.loads(json.dumps(proper))
        row = changed(); row["text"] = "Unexpected words."; variants.append(row)
        row = changed(); row["text_sha256"] = "a" * 64; variants.append(row)
        row = changed(); row["text_status"]["text_sha256"] = "a" * 64; variants.append(row)
        row = changed(); row["text_status"]["body_status"] = "removed"; variants.append(row)
        row = changed(); row["text_status"]["scope"] = "missal-formulary"; variants.append(row)
        row = changed(); row["text_status"]["state"] = "partial"; variants.append(row)
        row = changed(); row["text_status"]["reasons"][0]["kind"] = "witness-gap"; variants.append(row)
        row = changed(); row["text_status"]["reasons"][0] = {"kind": "no-exemplar"}; variants.append(row)
        row = changed(); row["text_status"]["reasons"][0]["source_id"] = broad; variants.append(row)
        row = changed(); row["text_status"]["reasons"][0]["source_id"] = "artifact.unregistered"; variants.append(row)
        row = changed(); row["text_status"]["reasons"].append({"kind": "rights-withheld", "source_id": exact}); variants.append(row)
        for index, row in enumerate(variants):
            with self.subTest(invalid=index):
                checker.check_proper("demo", row, problems := [])
                self.assertTrue(problems, row)
        checker.check_text_status("mass", proper["text_status"], problems := [])
        self.assertTrue(problems, "the private marker cannot be used on a Mass")
        for witness_type in ("segment", "passage"):
            checker.source_records = lambda t=witness_type: ({exact: SimpleNamespace(record_type=t)}, None)
            checker.check_proper("demo", proper, problems := [])
            self.assertEqual([], problems)

    def test_held_unpublished_does_not_shift_legacy_latin_ledger_ordinals(self) -> None:
        source_id = "artifact.demo.held"
        reason = [{"kind": "rights-withheld", "source_id": source_id}]
        held = {"name": "Collect", "source": "composed", "text_status": {
            "state": "unavailable", "scope": "proper-body",
            "body_status": "held-unpublished", "reasons": reason}}
        removed = {"name": "Collect", "source": "composed", "text_status": {
            "state": "unavailable", "scope": "proper-body", "reasons": reason}}
        present = {"name": "Collect", "source": "composed", "text": "Public fixture words."}
        owners = list(body_owners(demo_document(held, removed, present)))
        self.assertEqual([(LatinKey("day", "", "Collect", occurrence=1), None, "removed"),
                          (LatinKey("day", "", "Collect", occurrence=2), "Public fixture words.", "present")], owners)
        public = load_tool("mass-propers")
        rows = list(public.coverage_slot_units(held, ("day", "main", "Collect", 1)))
        self.assertEqual(("day", "main", "Collect", "all", 1), rows[0][0],
                         "the exact source seat still exists outside the Latin text ledger")

    def test_held_public_body_keeps_its_existing_permission_behavior(self) -> None:
        text = "Public fixture words."
        key = LatinKey("day", "", "Collect", occurrence=1)
        row = {"text_sha256": text_sha256(text), "provenance_status": "identified",
               "publication_status": "permitted", "publication_basis": "project-created",
               "surfaces": sorted(SURFACES), "transformations": [],
               "provenance_evidence": "Test fixture created here.",
               "provenance_confidence": "high"}
        proper = {"name": "Collect", "source": "composed", "text": text}
        clean = sanitize_proper(proper, key, {key: row}, SURFACES)
        self.assertEqual(text, clean["text"])
        self.assertFalse(clean["latin"]["withheld"])
        self.assertTrue(decision_for(key, text, {key: row}).permits(SURFACES))

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


    def test_held_unpublished_cli_structure_and_daily_dumps_keep_private_status_private(self) -> None:
        source_id = "artifact.private.fixture"
        status = {"state": "unavailable", "scope": "proper-body",
                  "body_status": "held-unpublished",
                  "reasons": [{"kind": "rights-withheld", "source_id": source_id}]}
        self.document = demo_document({"name": "Collect", "source": "composed", "text_status": status})
        (self.calendars / "demo/propers.yaml").write_text(yaml.safe_dump(self.document, sort_keys=False))
        (self.inventories / f"demo{SIDECAR_SUFFIX}").write_text(
            render_unresolved_sidecar("demo", self.document).replace(
                "\n[defaults]\n", "\nentries = []\n\n[defaults]\n", 1))
        neutral = {"target": "Collect", "state": "unavailable",
                   "held": False, "available": False, "withheld": True}
        def public_statuses(value):
            if isinstance(value, dict):
                if isinstance(value.get("text_status"), dict):
                    self.assertEqual({"state", "scope"}, set(value["text_status"]))
                for child in value.values(): public_statuses(child)
            elif isinstance(value, list):
                for child in value: public_statuses(child)
        mass_propers = load_tool("mass-propers")
        built = mass_propers.calendar_structure(self.calendars, "demo", {})
        public_statuses(built)
        self.assertEqual(neutral, built["masses"][0]["propers"][0]["latin"])
        command = [sys.executable, str(ROOT / "tools/mass-propers"), "show",
                   "--root", str(self.calendars), "--calendar", "demo", "--mass", "day"]
        machine = None
        for fmt in ("json", "yaml", "text"):
            result = subprocess.run([*command, "--format", fmt], check=True, capture_output=True, text=True)
            self.assertNotIn("held-unpublished", result.stdout)
            self.assertNotIn(source_id, result.stdout)
            if fmt == "text":
                self.assertIn("Latin text unavailable", result.stdout)
                continue
            payload = json.loads(result.stdout) if fmt == "json" else yaml.safe_load(result.stdout)
            public_statuses(payload)
            self.assertEqual(neutral, payload["appointed"][0]["proper"]["latin"])
            self.assertEqual(neutral, payload["mass"]["propers"][0]["latin"])
            machine = payload
        today = load_tool("mass-today")
        args = argparse.Namespace(form=None, lang="la", bible=None, witness=None, json=True, format="json")
        assembled = today.propers_of("demo", "day", args, payload=machine)
        self.assertNotIn("refused", assembled)
        self.assertEqual(neutral, assembled["propers"][0]["latin"])
        public_statuses(assembled)
        for fmt in ("json", "yaml"):
            # Exercise the actual dump function in a subprocess: print_json
            # binds its stream at import time, before redirect_stdout exists.
            program = ("import argparse,json,sys; from importlib.machinery import SourceFileLoader; "
                       "tool=SourceFileLoader('daily_dump',sys.argv[1]).load_module(); "
                       "args=argparse.Namespace(json=sys.argv[2]=='json',format=sys.argv[2]); "
                       "raise SystemExit(tool.render(json.load(sys.stdin),args))")
            output = subprocess.run([sys.executable, "-c", program,
                                     str(ROOT / "tools/mass-today"), fmt],
                                    input=json.dumps({"assembled": assembled}),
                                    check=True, capture_output=True, text=True).stdout
            self.assertNotIn("held-unpublished", output)
            self.assertNotIn(source_id, output)
            dumped = json.loads(output) if fmt == "json" else yaml.safe_load(output)
            public_statuses(dumped)



if __name__ == "__main__":
    unittest.main()
