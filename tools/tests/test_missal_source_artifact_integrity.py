#!/usr/bin/env python3
"""Missal source records keep exact provenance edges and derived censuses honest."""

from __future__ import annotations

import collections
import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INVENTORIES = ROOT / "src" / "sources" / "inventories"
WORKS = ROOT / "src" / "sources" / "works"
MISSAL_GUIDANCE = ROOT / "guidance" / "missals.md"
SOURCE_GUIDANCE = ROOT / "guidance" / "sources.md"
LITURGICAL_POLICY = ROOT / "guidance" / "liturgical-text-publication-policy.md"
LITURGICAL_ENGLISH_RIGHTS = INVENTORIES / "liturgical-english-rights-v1.toml"
MISSAL_ACQUISITION = INVENTORIES / "missal-acquisition-audit-v1.toml"
POSTCONCILIAR_LATIN_RIGHTS = (
    INVENTORIES / "postconciliar-latin-rights-v1.toml"
)

ELLC_ARTIFACT = (
    WORKS
    / "english-language-liturgical-consultation"
    / "praying-together"
    / "editions"
    / "1998"
    / "artifacts"
    / "common-texts-en"
    / "artifact.toml"
)
CUMMISKEY_ARTIFACTS = (
    WORKS
    / "eugene-cummiskey"
    / "roman-missal-english-laity"
    / "editions"
    / "philadelphia-1861"
    / "artifacts"
)
CUMMISKEY_JPEG_TRANSCRIPTIONS = (
    "canon-missae-la",
    "ordinarium-praeparatio-la",
    "ordinarium-oblatio-la",
    "ordinarium-communio-la",
    "ordinarium-conclusio-la",
    "praefationes-la",
)
ICEL_RIGHTS_INVENTORY = INVENTORIES / "icel-web-permission-rights-v1.toml"
POSTCONCILIAR_TRANSLATIONS = (
    INVENTORIES / "postconciliar-proper-translations-v1.toml"
)
PRESIDENTIAL_TONES_ARTIFACT = (
    WORKS
    / "international-commission-on-english-in-the-liturgy"
    / "music-for-the-roman-missal"
    / "editions"
    / "2010-chants-web-2026-08-21"
    / "artifacts"
    / "presidential-tones"
    / "artifact.toml"
)
PSP_ROOT = (
    WORKS
    / "congregation-for-divine-worship-and-the-discipline-of-the-sacraments"
    / "decree-implementing-canon-838-2021"
)
PSP_EDITION = PSP_ROOT / "editions" / "2021-english-press-office-bulletin"
PSP_ARTIFACT = (
    PSP_EDITION / "artifacts" / "press-office-pdf-9fd22cb8" / "artifact.toml"
)
PSP_PASSAGE_IDS = {
    number: (
        "passage.congregation-for-divine-worship-and-the-discipline-of-the-"
        "sacraments.decree-implementing-canon-838-2021."
        f"english-press-office-bulletin-2021-10-22.{number}"
    )
    for number in ("2", "3", "40")
}
PSP_PROJECTION = (
    ROOT
    / "src"
    / "web"
    / "data"
    / "structure"
    / "sources"
    / "editions"
    / "congregation-for-divine-worship-and-the-discipline-of-the-sacraments"
    / "decree-implementing-canon-838-2021"
    / "2021-2021-english-press-office-bulletin.json"
)


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


class ExactSourceEdgeTests(unittest.TestCase):
    def test_postquam_summus_pontifex_keeps_canonical_identity_and_rights_limit(
        self,
    ) -> None:
        work = load_toml(PSP_ROOT / "work.toml")
        self.assertIn("Postquam Summus Pontifex", work["alternate_titles"])
        self.assertIn("PSP", work["alternate_titles"])

        edition = load_toml(PSP_EDITION / "edition.toml")
        self.assertEqual(edition["work_id"], work["id"])

        artifact = load_toml(PSP_ARTIFACT)
        self.assertEqual(
            artifact["sha256"],
            "9fd22cb8a225c7c44bed7703e82c9e0669ad1f7c5c3c7887c513efb543f3bc27",
        )
        self.assertEqual(artifact["byte_size"], 244_554)
        self.assertEqual(artifact["page_count"], 20)
        self.assertEqual(artifact["storage"], "restricted")
        self.assertEqual(artifact["rights_status"], "restricted")
        self.assertNotIn("path", artifact)

        expected_pages = {
            "2": [[2, 2], [17, 17]],
            "3": [[2, 2], [17, 17]],
            "40": [[6, 6]],
        }
        for number, page_ranges in expected_pages.items():
            with self.subTest(number=number):
                passage = load_toml(PSP_EDITION / "passages" / f"{number}.toml")
                self.assertEqual(passage["id"], PSP_PASSAGE_IDS[number])
                self.assertEqual(passage["artifact_page_ranges"], page_ranges)
                self.assertEqual(
                    passage["artifact_sha256"], artifact["sha256"]
                )
                self.assertEqual(
                    passage["states"],
                    ["cataloged", "acquired", "inspected", "verified"],
                )

        policy = LITURGICAL_POLICY.read_text(encoding="utf-8")
        self.assertIn("current registered word", policy)
        self.assertNotIn("PSP is not registered anywhere", policy)
        for passage_id in PSP_PASSAGE_IDS.values():
            self.assertIn(passage_id, policy)

        rights = load_toml(LITURGICAL_ENGLISH_RIGHTS)
        self.assertTrue(
            {PSP_PASSAGE_IDS["2"], PSP_PASSAGE_IDS["3"]}
            <= set(rights["the_latin"]["source_ids"])
        )
        self.assertIn(
            PSP_PASSAGE_IDS["40"], rights["the_icel_translation"]["source_ids"]
        )

        projection = json.loads(PSP_PROJECTION.read_text(encoding="utf-8"))
        self.assertEqual(projection["edition"]["id"], artifact["edition_id"])
        self.assertEqual(
            {row["id"] for row in projection["passages"]},
            set(PSP_PASSAGE_IDS.values()),
        )
        for row in projection["passages"]:
            self.assertFalse(row["readable"])
            self.assertEqual(row["rights"], "restricted")
            self.assertEqual(row["storage"], "restricted")
            self.assertEqual(row["withheld"], "rights")

    def test_ellc_rights_page_is_not_claimed_as_the_text_parent(self) -> None:
        artifact = load_toml(ELLC_ARTIFACT)

        self.assertNotIn("derived_from", artifact)
        provenance = artifact["provenance"]
        self.assertNotIn("transformation", artifact)
        self.assertIn("nine text pages", provenance)
        self.assertEqual(provenance.count("https://www.englishtexts.org/"), 9)
        self.assertIn("not registered as exact source artifacts", provenance)
        self.assertIn("permissions page is rights evidence only", provenance)

    def test_cummiskey_jpeg_transcriptions_do_not_claim_the_pdf_as_parent(self) -> None:
        for name in CUMMISKEY_JPEG_TRANSCRIPTIONS:
            path = CUMMISKEY_ARTIFACTS / name / "artifact.toml"
            with self.subTest(artifact=name):
                artifact = load_toml(path)
                self.assertNotIn("derived_from", artifact, path)
                provenance = artifact["provenance"]
                self.assertNotIn("transformation", artifact, path)
                self.assertIn("page/n<leaf>_w1400.jpg", provenance, path)
                self.assertIn("not from that PDF's exact bytes", provenance, path)
                self.assertIn("not retained or hashed as artifacts", provenance, path)

    def test_exact_pdf_transcription_keeps_its_pdf_parent(self) -> None:
        path = CUMMISKEY_ARTIFACTS / "common-marian-verified-en" / "artifact.toml"
        artifact = load_toml(path)

        self.assertEqual(
            artifact.get("derived_from"),
            "artifact.eugene-cummiskey.roman-missal-english-laity."
            "philadelphia-1861.ia-scan-pdf",
        )
        self.assertIn("one-based PDF artifact pages", artifact["transformation"])

    def test_presidential_tones_records_all_three_orations(self) -> None:
        artifact = load_toml(PRESIDENTIAL_TONES_ARTIFACT)

        self.assertEqual(
            artifact["sha256"],
            "6e03d4d01cd09ac2d32642b0d797bdb6f903e490b8166c7df6a70322617e97e6",
        )
        self.assertEqual(artifact["byte_size"], 111_608)
        self.assertEqual(artifact["page_count"], 6)
        notes = artifact["notes"]
        self.assertIn("prints three Proper-of-Time orations whole", notes)
        self.assertIn("Epiphany of the Lord, Mass during the Day", notes)
        self.assertIn("across artifact pp. 2-3 and again on artifact p. 6", notes)

        translations = load_toml(POSTCONCILIAR_TRANSLATIONS)
        rows = [
            row
            for row in translations["untranslated"]
            if row["mass"] == "epiphany"
            and row["form_id"] == "day"
            and row["proper"] == "Prayer over the Offerings"
            and row["cycle"] == "all"
            and row["occurrence"] == 1
            and row["lang"] == "en"
            and row["extent"] == "body"
        ]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["availability"], "unavailable")
        self.assertEqual(row["reason"]["kind"], "rights-withheld")
        self.assertEqual(row["witness"], "icel-music-2010")
        self.assertEqual(row["witness_artifact_id"], artifact["id"])
        self.assertEqual(row["verified_artifact_page"], 2)
        self.assertIn(
            "Prayer over the Offerings (The Epiphany of the Lord, "
            "The Mass during the Day)",
            row["verified_heading"],
        )
        self.assertEqual(
            row["quarantined_text_sha256"],
            ["410fcea9a4b127bcddfdefffea3e598154e3bf67514481ae3b3fa14a3714e22e"],
        )
        self.assertNotIn("text", row)

        rights = load_toml(ICEL_RIGHTS_INVENTORY)
        reasoning = rights["as_of_when"]["reasoning"]
        self.assertIn("prints three Proper-of-Time orations whole", reasoning)
        self.assertIn(
            "Epiphany of the Lord, Mass during the Day",
            " ".join(reasoning.split()),
        )
        survey = rights["what_this_lane_registered"]["inventory"]
        self.assertIn("49 had a free official source and 153 did not", survey)
        self.assertNotIn("48 had a free official source and 154 did not", survey)


class InventoryCensusTests(unittest.TestCase):
    def test_acquisition_alias_guidance_uses_existing_schema_owners(self) -> None:
        guidance = SOURCE_GUIDANCE.read_text(encoding="utf-8")

        self.assertIn("`work.alternate_titles`", guidance)
        self.assertIn("The aliases actually tried are acquisition provenance", guidance)
        self.assertIn("artifact's `provenance`", guidance)
        self.assertIn("owning acquisition audit or inventory", guidance)
        self.assertIn("Do not invent a placeholder artifact", guidance)
        self.assertNotIn("record them with\nthe artifact", guidance)

    def test_icel_conflict_is_resolved_without_opening_bundled_surfaces(self) -> None:
        inventory = load_toml(MISSAL_ACQUISITION)
        book = next(
            row
            for row in inventory["books"]
            if row["id"] == "roman-missal-english-2011"
        )
        correction = next(
            row
            for row in inventory["corrections"]
            if row["id"] == "icel-internet-clause"
        )

        self.assertEqual(book["may_publish_text"], "no")
        self.assertIn("approved-english-publication-restriction", book["rights_basis"])
        self.assertIn("official-exemplar-not-carried", book["rights_basis"])
        self.assertNotIn("marks it `absent: icel`", book["rights_basis"])
        self.assertEqual(correction["status"], "applied on 2026-08-27")
        self.assertIn("HISTORICAL FINDING, RECORDED ON 2026-08-01", correction["finding"])
        self.assertIn(
            "guidance/liturgical-text-publication-policy.md sections 2, 3.4, 6, and 15.2",
            correction["finding"],
        )
        self.assertIn("`may_publish_text = \"no\"`", correction["consequences"])

    def test_missal_acquisition_counts_match_every_book_category(self) -> None:
        inventory = load_toml(MISSAL_ACQUISITION)
        counts = inventory["counts"]
        books = inventory["books"]

        publication_fields = {
            "yes": "may_publish_yes",
            "yes, subject to the title-page confirmation named in rights_basis": (
                "may_publish_conditional"
            ),
            "no": "may_publish_no",
            "mixed": "may_publish_mixed",
            "unresolved": "may_publish_unresolved",
        }
        rights_fields = {
            "public-domain-us-pre-1931": "rights_public_domain_us_pre_1931",
            "public-domain-us-not-renewed": "rights_public_domain_us_not_renewed",
            "holy-see-post-1929": "rights_holy_see_post_1929",
            "mixed": "rights_mixed",
            "unresolved": "rights_unresolved",
            "third-party-copyright": "rights_third_party_copyright",
        }
        retrievable_fields = {
            "whole": "retrievable_whole",
            "bounded": "retrievable_bounded",
            "restricted": "retrievable_restricted",
            "not-located": "retrievable_not_located",
            "unresolved": "retrievable_unresolved",
        }

        for key, fields in (
            ("may_publish_text", publication_fields),
            ("rights", rights_fields),
            ("retrievable", retrievable_fields),
        ):
            actual = collections.Counter(book[key] for book in books)
            self.assertEqual(set(actual), set(fields), f"unmapped {key} category")
            for category, field in fields.items():
                self.assertEqual(counts[field], actual[category], field)

        self.assertEqual(counts["books_recorded"], len(books))
        self.assertEqual(
            sum(counts[field] for field in publication_fields.values()),
            len(books),
        )
        self.assertEqual(
            sum(counts[field] for field in rights_fields.values()),
            len(books),
        )
        self.assertEqual(
            sum(counts[field] for field in retrievable_fields.values()),
            len(books),
        )

    def test_negative_retrieval_verdicts_are_bounded_and_unsearched_are_unresolved(
        self,
    ) -> None:
        inventory = load_toml(MISSAL_ACQUISITION)
        books = {row["id"]: row for row in inventory["books"]}

        for book_id in (
            "missale-romanum-1920-typica",
            "missale-romanum-1971-reimpressio",
        ):
            with self.subTest(book=book_id):
                row = books[book_id]
                self.assertEqual(row["retrievable"], "unresolved")
                self.assertIn("No bounded external repository search", row["retrievable_basis"])
                self.assertTrue(row["bound_reached"].strip())

        self.assertEqual(books["missale-romanum-1971-reimpressio"]["aliases_tried"], [])
        for row in inventory["books"]:
            if row["retrievable"] != "not-located":
                continue
            with self.subTest(book=row["id"]):
                self.assertTrue(row["repositories_searched"])
                self.assertTrue(row["retrievable_basis"].strip())
                basis = row["retrievable_basis"].casefold()
                self.assertTrue(
                    any(repository.casefold() in basis for repository in row["repositories_searched"]),
                    "retrievable_basis must name its bounded repository",
                )

    def test_missal_acquisition_has_one_complete_vocabulary(self) -> None:
        raw = MISSAL_ACQUISITION.read_text(encoding="utf-8")
        self.assertEqual(raw.count("`rights` takes one of:"), 1)
        vocabulary = raw.split("`rights` takes one of:", 1)[1].split("The value", 1)[0]
        for value in (
            "public-domain-us-pre-1931",
            "public-domain-us-not-renewed",
            "holy-see-post-1929",
            "third-party-copyright",
            "unresolved",
            "mixed",
        ):
            self.assertIn(f"`{value}`", vocabulary)
        self.assertIn("`mixed`", vocabulary.split("`may_publish_text`", 1)[1])

    def test_postconciliar_latin_rights_audit_is_text_free_and_fail_closed(
        self,
    ) -> None:
        audit = load_toml(POSTCONCILIAR_LATIN_RIGHTS)
        acquisition = load_toml(MISSAL_ACQUISITION)

        self.assertEqual(audit["civil_law_status"], "unresolved")
        self.assertEqual(audit["affirmative_distribution_basis"], "not-established")
        self.assertEqual(audit["operational_decision"], "withhold")
        self.assertEqual(audit["payload_disposition"], "identity-and-rights-metadata-only")
        self.assertFalse(audit["payload_guard"]["contains_liturgical_payload"])
        self.assertFalse(audit["payload_guard"]["contains_source_quotation"])
        self.assertEqual(audit["authority_gap"]["status"], "open")
        self.assertIn("13 May 2005", audit["authority_gap"]["missing"])

        forbidden_payload_keys = {"text", "quote", "quotation", "transcription"}

        def walk(value: object) -> None:
            if isinstance(value, dict):
                self.assertTrue(forbidden_payload_keys.isdisjoint(value))
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)

        walk(audit)
        state_ids = audit["affected_missal_states"]["book_ids"]
        self.assertEqual(audit["affected_missal_states"]["count"], len(state_ids))
        self.assertEqual(len(state_ids), len(set(state_ids)))
        books = {row["id"]: row for row in acquisition["books"]}
        for book_id in state_ids:
            with self.subTest(book=book_id):
                self.assertEqual(books[book_id]["may_publish_text"], "no")
                self.assertIn(
                    "postconciliar-latin-rights-v1.toml",
                    books[book_id]["rights_basis"],
                )

    def test_lt_hist_counts_and_current_prose_share_one_partition(self) -> None:
        inventory = load_toml(INVENTORIES / "lt-hist-rights-audit-v1.toml")
        counts = inventory["counts"]
        actual = collections.Counter(row["verdict"] for row in inventory["versions"])
        count_fields = {
            "admissible": "admissible",
            "withdrawn": "withdrawn_after_fold_in",
            "excluded": "excluded",
            "undecided": "undecided",
        }

        self.assertEqual(set(actual), set(count_fields))
        for verdict, field in count_fields.items():
            self.assertEqual(counts[field], actual[verdict], field)
        self.assertEqual(counts["versions_audited"], sum(actual.values()))
        self.assertEqual(counts["admissible_on_age"], 5)
        self.assertEqual(counts["admissible_on_a_renewal_record"], 1)

        self.assertIn("The five that may come on age", inventory["holding"])
        self.assertNotIn("The six that may come on age", inventory["holding"])
        lasance = next(
            row
            for row in inventory["versions"]
            if row["id"] == "1937-lasance-new-roman-missal-english"
        )
        self.assertIn("five pre-1931 rows", lasance["lt_hist_basis_rejected"])
        self.assertNotIn("six pre-1931 rows", lasance["lt_hist_basis_rejected"])

        guidance = MISSAL_GUIDANCE.read_text(encoding="utf-8")
        self.assertIn("six remain admissible: five on pre-1931 publication", guidance)
        self.assertIn(
            "6 admissible + 1 withdrawn + 14 excluded + 4 open =\n25",
            guidance,
        )
        self.assertNotIn("versions, 7 are admissible", guidance)


if __name__ == "__main__":
    unittest.main()
