"""Index identity, evidence bounds, and resumable retrieval for papal metadata."""
from contextlib import redirect_stdout
from datetime import date
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _papal_documents as p


def index(title="Alpha (January 2, 1900)", stem="hf_enc_02011900_alpha", lang="en", links=""):
    return (f'<div class="vaticanindex"><ul><li><div class="item"><h2>{title}</h2>'
            f'<div class="translation-field"><a href="/content/leo-xiii/{lang}/encyclicals/documents/{stem}.html">{lang.upper()}</a></div>'
            f'</div></li></ul></div>{links}').encode()


def row(title="Alpha (January 2, 1900)", stem="hf_enc_02011900_alpha", lang="en", kind="encyclical"):
    url = f"{p.BASE}/content/leo-xiii/{lang}/encyclicals.index.html"
    parsed = p.parse_index(index(title, stem, lang), url)[0][0]
    return {**parsed, "pope_id": "leo-xiii", "document_type": kind}


class IndexTests(unittest.TestCase):
    def test_only_index_items_are_documents(self):
        raw = b'<div class="item"><h2>Navigation</h2></div>' + index()
        rows, _ = p.parse_index(raw, p.BASE + "/content/leo-xiii/en/encyclicals.index.html")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["date"], "1900-01-02")

    def test_historical_unlinked_heading_keeps_language_links(self):
        raw = index("Bull <i>Alpha</i> (2 gennaio 1700)", "bolla-alpha", "it")
        rows, _ = p.parse_index(raw, p.BASE + "/content/benedictus-xiv/en.html")
        self.assertEqual(rows[0]["document_type"], "bull")
        self.assertEqual(rows[0]["date"], "1700-01-02")
        self.assertIn("it", rows[0]["languages"])

    def test_heading_link_survives_missing_translation_field(self):
        raw = b'<div class="vaticanindex"><div class="item"><h2><a href="/content/leo-xiii/en/encyclicals/documents/alpha.html">Alpha</a></h2></div></div>'
        rows, _ = p.parse_index(raw, p.BASE)
        self.assertIn("en", rows[0]["languages"])

    def test_all_language_codes_preserved_and_fragments_removed(self):
        raw = index().replace(b'</div></div>', b'<a href="/content/leo-xiii/zh_cn/encyclicals/documents/alpha.html#top">ZH_CN</a></div></div>')
        rows, _ = p.parse_index(raw, p.BASE)
        self.assertIn("zh_cn", rows[0]["languages"])
        self.assertNotIn("#", rows[0]["languages"]["zh_cn"])

    def test_same_category_pagination_followed_but_documents_not(self):
        links = [p.BASE + "/content/leo-xiii/en/encyclicals.index.2.html", p.BASE + "/content/leo-xiii/en/encyclicals/documents/alpha.html", p.BASE + "/content/leo-xiii/fr/encyclicals.index.html", p.BASE + "/content/leo-xiii/en/speeches.index.html"]
        self.assertEqual(p.index_links(links, "leo-xiii", "en"), [links[0]])

    def test_historical_root_pagination(self):
        target = p.BASE + "/content/benedictus-xiv/en.index.1.html"
        self.assertEqual(p.index_links([target], "benedictus-xiv", "en"), [target])

    def test_italian_encyclical_is_not_generic_letter(self):
        self.assertEqual(p.category_of(p.BASE, "Lettera enciclica Alpha"), "encyclical")
        self.assertEqual(p.category_of(p.BASE, "Epistola Encyclica Alpha"), "encyclical")


class DateAndIdentityTests(unittest.TestCase):
    def test_dates_have_to_be_valid_and_unambiguous(self):
        self.assertIsNone(p.parse_date("February 30, 1900"))
        self.assertIsNone(p.parse_date("1900"))
        self.assertIsNone(p.parse_date("January 2, 1900 or January 3, 1900"))
        self.assertEqual(p.parse_date("January 2nd, 1900"), "1900-01-02")
        self.assertEqual(p.parse_date("2 Ianuarii 1900"), "1900-01-02")
        self.assertEqual(p.parse_date("d. 23 m. Februarii a. 1929"), "1929-02-23")
        self.assertEqual(p.title_parts("Alpha, d. 23 m. Februarii a. 1929")[1], "Alpha, d. 23 m. Februarii a. 1929")

    def test_repeated_incipit_on_another_date_is_distinct(self):
        rows = [row(), row("Alpha (January 3, 1900)", "hf_enc_03011900_alpha")]
        self.assertEqual(len(p.merge_rows(rows)), 2)

    def test_shared_edition_url_unites_translated_titles(self):
        a, b = row(), row("Alfa (2 gennaio 1900)", lang="it")
        b["languages"]["en"] = a["languages"]["en"]
        merged = p.merge_rows([a, b])
        self.assertEqual(len(merged), 1)
        self.assertEqual(set(merged[0]["languages"]), {"en", "it"})
        self.assertEqual(len(merged[0]["source_index_urls"]), 2)

    def test_date_token_order_is_file_alias_not_second_work(self):
        a, b = row(), row("Alpha (2 gennaio 1900)", "hf_enc_19000102_alpha", "it")
        merged = p.merge_rows([a, b])
        self.assertEqual(len(merged), 1)
        self.assertEqual(len(merged[0]["url_aliases"]), 2)

    def test_same_date_same_title_is_not_enough_to_merge(self):
        self.assertEqual(len(p.merge_rows([row(stem="first"), row(stem="second")])), 2)

    def test_conflicting_index_dates_are_preserved_without_guessing(self):
        a, b = row(), row("Alpha (January 3, 1900)")
        merged = p.merge_rows([a, b])[0]
        self.assertIsNone(merged["date"])
        self.assertEqual({x["date"] for x in merged["date_conflicts"]}, {"1900-01-02", "1900-01-03"})

    def test_filename_date_is_labelled_unverified(self):
        merged = p.merge_rows([row("Alpha")])[0]
        self.assertEqual(merged["date"], "1900-01-02")
        self.assertEqual(merged["date_basis"], "filename-unverified")

    def test_new_translation_retains_existing_id(self):
        a, b = row(lang="it"), row(lang="en")
        b["languages"]["it"] = a["languages"]["it"]
        previous = {"documents": p.merge_rows([a])}
        self.assertEqual(p.merge_rows([a, b], previous)[0]["id"], previous["documents"][0]["id"])

    def test_unlinked_rows_have_explicit_availability(self):
        a = row()
        a["languages"] = {}
        self.assertEqual(p.merge_rows([a])[0]["availability"], "index-row-without-linked-edition")

    def test_identical_unlinked_source_rows_merge(self):
        a = row()
        a["languages"] = {}
        self.assertEqual(len(p.merge_rows([a, dict(a)])), 1)

    def test_unlinked_rows_on_different_pages_have_distinct_ids(self):
        a, b = row(), row()
        a["languages"], b["languages"] = {}, {}
        b["source_index_url"] = p.BASE + "/content/leo-xiii/it/encyclicals.index.html"
        merged = p.merge_rows([a, b])
        self.assertEqual(len({r["id"] for r in merged}), 2)

    def test_overlapping_document_types_are_memberships(self):
        a, b = row(kind="apostolic-letter"), row(kind="motu-proprio")
        merged = p.merge_rows([a, b])[0]
        self.assertEqual(merged["document_types"], ["apostolic-letter", "motu-proprio"])
        self.assertNotIn("document_type_conflicts", merged)


class FetchTests(unittest.TestCase):
    def test_cache_must_be_under_scratch(self):
        with self.assertRaisesRegex(ValueError, "scratch"):
            p.Fetcher(ROOT / "src")

    def test_whole_bytes_are_hashed_and_cache_is_verified(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch") as temp:
            class Response(io.BytesIO):
                headers = {}
                status = 200
                url = p.BASE + "/content/leo-xiii/en.html"
            with patch.object(p, "urlopen", return_value=Response(b"whole response")) as request:
                fetcher = p.Fetcher(temp, pace=0)
                raw, receipt = fetcher.fetch(Response.url)
                self.assertEqual(raw, b"whole response")
                self.assertEqual(receipt["sha256"], hashlib.sha256(raw).hexdigest())
                self.assertEqual(fetcher.fetch(Response.url)[0], raw)
                self.assertEqual(request.call_count, 1)
            next(Path(temp).glob("*.html")).write_bytes(b"damaged")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                fetcher.fetch(Response.url)

    def test_missing_index_is_recorded_as_failure(self):
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch") as temp:
            url = p.BASE + "/content/leo-xiii/en.html"
            with patch.object(p, "urlopen", side_effect=HTTPError(url, 404, "missing", {}, None)):
                raw, receipt = p.Fetcher(temp, pace=0).fetch(url)
            self.assertIsNone(raw)
            self.assertEqual(receipt["status"], "not-found")
            self.assertEqual(receipt["http_status"], 404)


class OverrideTests(unittest.TestCase):
    def test_reviewed_url_aliases_preserve_canonical_identity_and_witnesses(self):
        a, b = row(stem="old-file"), row(stem="different-file", lang="la")
        previous = {"documents": p.merge_rows([a, b])}
        canonical = previous["documents"][0]["id"]
        overrides = {"schema": p.OVERRIDES_SCHEMA, "aliases": [{"canonical_id": canonical, "urls": [*a["languages"].values(), *b["languages"].values()], "evidence": "Reviewed same act, distinct deliveries."}], "records": {}}
        merged = p.merge_rows([a, b], previous, overrides)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["id"], canonical)
        self.assertEqual(len(merged[0]["url_aliases"]), 2)
        self.assertEqual(len(merged[0]["identity_aliases"]), 1)
        self.assertEqual(p.merge_rows([a, b], {"documents": merged}, overrides)[0]["identity_aliases"], merged[0]["identity_aliases"])

    def test_date_resolution_preserves_conflicting_source_dates(self):
        a, b = row(), row("Alpha (January 3, 1900)")
        identity = p.merge_rows([a, b])[0]["id"]
        proof = {"source_url": p.BASE + "/archive/source.pdf", "locus": "printed p. 2, closing dateline"}
        overrides = {"schema": p.OVERRIDES_SCHEMA, "records": {identity: {"resolved_date": "1900-01-04", "date_resolution": proof}}}
        merged = p.merge_rows([a, b], overrides=overrides)[0]
        self.assertIsNone(merged["date"])
        self.assertEqual(merged["resolved_date"], "1900-01-04")
        self.assertEqual(len(merged["date_conflicts"]), 2)

    def test_constituent_and_composite_bounds_remain_explicit(self):
        a = row()
        overrides = {"schema": p.OVERRIDES_SCHEMA, "records": {a["languages"]["en"]: {"record_role": "composite", "constituents": [{"subject": "First act"}, {"subject": "Second act"}], "issues": ["One source delivery contains two acts."]}}}
        merged = p.merge_rows([a], overrides=overrides)[0]
        self.assertEqual(merged["record_role"], "composite")
        self.assertEqual(len(merged["constituents"]), 2)

    def test_unproved_date_or_alias_is_refused(self):
        with self.assertRaisesRegex(ValueError, "source proof"):
            p.validate_overrides({"schema": p.OVERRIDES_SCHEMA, "records": {"id": {"resolved_date": "1900-01-01"}}})
        with self.assertRaisesRegex(ValueError, "evidence"):
            p.validate_overrides({"schema": p.OVERRIDES_SCHEMA, "aliases": [{"urls": [p.BASE + "/first", p.BASE + "/second"]}]})

    def test_related_regulation_needs_separate_attribution_and_source(self):
        record = {"record_role": "constituent", "source_work_type": "curial-regulation"}
        overrides = {"schema": p.OVERRIDES_SCHEMA, "records": {"id": record}}
        with self.assertRaisesRegex(ValueError, "own attribution and source proof"):
            p.validate_overrides(overrides)
        record.update(source_responsible="Cardinal Merry del Val", display_responsible="Cardinal Merry del Val",
                      source_unit_identity={"kind": "related-regulation", "source_url": p.BASE + "/archive/source.pdf",
                                            "locus": "pp. 440–461", "basis": "Complete Latin regulation signed by its actual issuer."})
        self.assertIs(p.validate_overrides(overrides), overrides)


class ContractTests(unittest.TestCase):
    def test_failed_page_never_looks_like_completed_discovery(self):
        document = p.merge_rows([row()])[0]
        url = document["source_index_urls"][0]
        catalog = {"schema": p.SCHEMA, "scope": {"all_historical_papal_documents": False}, "documents": [document], "coverage": [{"url": url, "status": "ok"}, {"url": p.BASE + "/missing", "status": "fetch-error"}]}
        report = p.check_catalog(catalog)
        self.assertTrue(report["ok"])
        self.assertFalse(report["discovery_complete"])
        self.assertEqual(report["failed_pages"], [p.BASE + "/missing"])

    def test_duplicate_edition_and_missing_evidence_are_refused(self):
        document = p.merge_rows([row()])[0]
        duplicate = {**document, "id": "papal.leo-xiii.other"}
        report = p.check_catalog({"schema": p.SCHEMA, "scope": {"all_historical_papal_documents": False}, "documents": [document, duplicate], "coverage": []})
        self.assertFalse(report["ok"])
        self.assertTrue(any("assigned twice" in x for x in report["errors"]))
        self.assertTrue(any("unacquired" in x for x in report["errors"]))

    def test_discovery_follows_declared_pages_and_excludes_root_features(self):
        root = p.BASE + "/content/leo-xiii/en.html"
        target = p.BASE + "/content/leo-xiii/en/encyclicals.index.html"
        page2 = p.BASE + "/content/leo-xiii/en/encyclicals.index.2.html"
        pages = {root: b'<a href="' + target.encode() + b'">Encyclicals</a>',
                 target: index(links=f'<a href="{page2}">2</a>'),
                 page2: index("Beta (January 3, 1900)", "hf_enc_03011900_beta")}
        def fetch(_self, url):
            raw = pages.get(url, b"<html></html>")
            return raw, {"url": url, "status": "ok", "sha256": hashlib.sha256(raw).hexdigest(), "retrieved_on": "2026-01-01", "byte_size": len(raw)}
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch") as temp, patch.object(p.Fetcher, "fetch", fetch):
            catalog = p.discover(temp, ["leo-xiii"], workers=2, pace=0)
        self.assertEqual(len(catalog["documents"]), 2)
        self.assertEqual(len(catalog["coverage"]), 5)
        self.assertEqual(catalog["scope"]["interface_languages"], ["en", "it", "la"])
        self.assertFalse(catalog["scope"]["all_historical_papal_documents"])

    def test_type_filter_includes_overlapping_source_categories(self):
        document = p.merge_rows([row(kind="apostolic-letter"), row(kind="motu-proprio")])[0]
        catalog = {"schema": p.SCHEMA, "scope": {"all_historical_papal_documents": False}, "documents": [document], "coverage": [{"url": document["source_index_urls"][0], "status": "ok"}]}
        with tempfile.TemporaryDirectory(dir=ROOT / ".scratch") as temp:
            path = Path(temp) / "catalog.json"
            path.write_text(json.dumps(catalog))
            output = io.StringIO()
            with redirect_stdout(output):
                code = p.main(["list", "--catalog", str(path), "--type", "motu-proprio", "--json"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["count"], 1)

    def test_json_input_refusal_has_no_traceback(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = p.main(["check", "--catalog", ".scratch/catalog_pipeline/absent-forever.json", "--json"])
        self.assertEqual(code, 2)
        self.assertFalse(json.loads(output.getvalue())["ok"])


if __name__ == "__main__":
    unittest.main()
