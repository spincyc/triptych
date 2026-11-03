"""Source-owned print admission and coverage stay independent of rendered HTML."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

if __package__:
    from . import test_print_catalog as fixtures
else:
    import test_print_catalog as fixtures

ROOT = fixtures.ROOT
sys.path.insert(0, str(ROOT / "scripts"))
import _print_catalog as catalog
import _browser_products as products


class SourcePrintMetadataTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/web-print-source-metadata"
        scratch.mkdir(parents=True, exist_ok=True)
        self.fixture = fixtures.SourceFixture("runTest")
        with patch.object(fixtures, "ROOT", scratch):
            self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = self.fixture.root

    def papal_page(self):
        return next(iter(catalog._papal_pages(self.root).values()))

    def test_bounded_papal_units_and_source_identity_precede_html(self):
        page = self.papal_page()
        product = page["print_product"]
        self.assertEqual(product["schema"], "triptych-web-print-document/v1")
        self.assertEqual(product["output_id"], "papal:papal.fixture/en")
        self.assertEqual(product["id"], product["output_id"])
        self.assertEqual(product["print_type"], "source-volume")
        self.assertEqual(product["mode"], "inline")
        self.assertEqual(product["root_route"], "papal-documents/1903-01-01--fixture--en--1234567890123456.html")
        self.assertEqual(product["source_paths"], page["source_paths"])
        self.assertEqual(product["counts"], {"blocks": 3, "headings": 0, "paragraphs": 3})
        self.assertEqual([row["id"] for row in product["expected_units"]],
                         ["papal-block-1", "papal-block-2", "papal-block-3"])
        self.assertEqual(product["sources"]["text"]["physical_line_ranges"], [[2, 6]])
        self.assertEqual(product["sources"]["text"]["extent"], "fragment")
        self.assertEqual(product["sources"]["text"]["sha256"], self.fixture.source["sha256"])
        self.assertEqual(product["sources"]["text"]["segment_id"], self.fixture.source["segment_id"])
        proof = product["coverage_result"]
        for field in ("output_id", "source_digest", "selection_digest", "expected_units", "counts"):
            self.assertEqual(proof[field], product[field])
        self.assertEqual(proof["status"], "pass")
        for field in ("source_digest", "selection_digest"):
            self.assertRegex(product[field], r"^[a-f0-9]{64}$")
        self.assertRegex(proof["audit_sha256"], r"^[a-f0-9]{64}$")
        self.assertEqual(proof["actual_units_sha256"],
                         catalog._check_print_units(product["expected_units"], page["html"]))
        self.assertEqual(proof["envelope_sha256"], product["envelope_sha256"])
        self.assertEqual(product["envelope_sha256"], catalog._check_print_envelope(product["envelope"], page["html"]))
        self.assertEqual(product["envelope"]["hrefs"], [self.fixture.source["source_url"]])
        self.assertEqual(product["envelope"]["article_languages"], ["en"])
        self.assertNotIn("Body & body", json.dumps(product))
        for visible in ("Historical fragment", "OCR is not collation", "outside the project licence"):
            self.assertIn(visible, page["html"])
        self.assertNotIn("UNSELECTED", page["html"])
        self.assertFalse(any(path.endswith(".pdf") for path in product["source_paths"]))

    def test_lost_duplicated_reordered_or_changed_paragraph_cannot_pass(self):
        page = self.papal_page()
        units, body = page["print_product"]["expected_units"], page["html"]
        blocks = re.findall(r'<p data-print-unit="[^"]+">.*?</p>', body, re.S)
        self.assertEqual(len(blocks), 3)
        damaged = [body.replace(blocks[-1], ""), body.replace(blocks[0], blocks[0] * 2),
                   body.replace(blocks[0], "SWAP").replace(blocks[1], blocks[0]).replace("SWAP", blocks[1]),
                   body.replace("Historical note;", "Rewritten note;")]
        for changed in damaged:
            with self.subTest(changed=changed), self.assertRaisesRegex(
                    catalog.PrintCatalogError, "content or order"):
                catalog._check_print_units(units, changed)

    def test_rendered_subset_does_not_redefine_expected_coverage(self):
        original = catalog._papal_body

        def truncate(document, reader, **kwargs):
            return original({**document, "blocks": document["blocks"][:-1]}, reader, **kwargs)

        with patch.object(catalog, "_papal_body", side_effect=truncate), \
                self.assertRaisesRegex(catalog.PrintCatalogError, "content or order"):
            self.papal_page()

    def test_unmarked_additional_source_block_or_reading_is_refused(self):
        page = self.papal_page()
        with self.assertRaisesRegex(catalog.PrintCatalogError, "unmarked source print block"):
            catalog._check_print_units(page["print_product"]["expected_units"],
                page["html"].replace('<div class="source-text">',
                                     '<div class="source-text"><p>Unselected added wording.</p>'))
        volume = self.volume()
        units = catalog._reading_print_units(volume)
        body = "\n".join(catalog._period_html(volume, period, rows, print_units=True)
                         for period, rows in volume.periods)
        with self.assertRaisesRegex(catalog.PrintCatalogError, "unmarked canonical print reading"):
            catalog._check_print_units(units, body + '<section id="reading-8"><p>Added reading.</p></section>')

    def test_papal_envelope_is_independent_of_removed_or_changed_renderer_context(self):
        original = catalog._papal_body
        mutations = {
            "fragment": lambda body: re.sub(r'<p class="source-extent">.*?</p>', "", body),
            "apparatus": lambda body: re.sub(r'<footer class="source-apparatus">.*?</footer>', "", body, flags=re.S),
            "title": lambda body: body.replace("Source &lt;title&gt;", "Different source title"),
            "caveat": lambda body: body.replace("OCR is not collation", "OCR is a complete collation"),
            "rights": lambda body: body.replace("outside the project licence", "covered by the project licence"),
            "reorder": lambda body: re.sub(r'<p class="source-extent">.*?</p>', "", body).replace(
                "</article>", '<p class="source-extent">Historical fragment; the source note describes its extent.</p></article>'),
            "addition": lambda body: body.replace("</article>", "<p>New unmarked qualification.</p></article>"),
            "witness-target": lambda body: body.replace('href="https://example.org/source"', 'href="https://example.org/other"'),
            "language": lambda body: body.replace('lang="en"', 'lang="la"'),
        }
        for name, mutate in mutations.items():
            with self.subTest(mutation=name), patch.object(catalog, "_papal_body",
                    side_effect=lambda *args, **kwargs: mutate(original(*args, **kwargs))), \
                    self.assertRaisesRegex(catalog.PrintCatalogError, "envelope"):
                self.papal_page()
        self.fixture.reader["extent"] = "damaged"
        self.fixture.save_index()
        with patch.object(catalog, "_papal_body", side_effect=lambda *args, **kwargs:
                re.sub(r'<p class="source-extent">.*?</p>', "", original(*args, **kwargs))), \
                self.assertRaisesRegex(catalog.PrintCatalogError, "envelope"):
            self.papal_page()

    def test_publisher_envelope_check_selects_exact_part_and_ignores_controls(self):
        page = self.papal_page()
        envelope = page["print_product"]["envelope"]
        part = '<section data-print-part="source-complete">' + page["html"] + '</section>'
        shell = '<div><button>Print control outside source</button>' + part + \
                '<script type="application/json">{"control":"not source text"}</script></div>'
        self.assertEqual(catalog._check_print_envelope(envelope, shell, part_id="source-complete"),
                         page["print_product"]["envelope_sha256"])
        for broken in (shell.replace(part, ""), shell.replace(part, part * 2), part.removesuffix('</section>')):
            with self.subTest(broken=broken), self.assertRaises(catalog.PrintCatalogError):
                catalog._check_print_envelope(envelope, broken, part_id="source-complete")

    def volume(self, *, large=False):
        edition_path = self.root / "src/sources/works/test/act/editions/1903"
        edition = SimpleNamespace(id="fixture-edition", language="en", label="Fixture edition",
            artifacts=edition_path / "artifacts", record={"publication": "Synthetic fixture"},
            rights={"status": "public-domain", "jurisdiction": "United States",
                    "basis": "Synthetic fixture; no external wording."},
            name_of=lambda token: {"Ps": "Psalms", "Gen": "Genesis"}[token])
        readings = [{"order": 3, "title": "Retained <reading>", "cited": "Psalms 22:1-2",
            "here": "Psalms 23:1-2", "note": "First note.\n\nSecond note.", "refused": "",
            "verses": [("Ps", 23, 1, "First & verse."), ("Ps", 23, 2, "Second verse.")]},
            {"order": 7, "title": "Uncarried reading", "cited": "Judith 15:14", "here": "",
             "note": "Retained qualification.", "refused": "No exact selected verse in this edition.", "verses": []}]
        if large:
            for index, reading in enumerate(readings):
                reading.update(refused="", verses=[("Gen", 1, index + 1, "Long literal text. " * 24_000)])
        periods = [({"key": f"period-{index}", "label": f"Period {index}", "summary": "Period context."}, [row])
                   for index, row in enumerate(readings, 1)]
        plan_path = self.root / "src/sources/reading-plans/fixture.yaml"
        self.fixture.write(plan_path.relative_to(self.root).as_posix(), "Synthetic canonical plan.\n")
        plan = SimpleNamespace(path=plan_path, id="fixture", name="Fixture plan", omissions="Visible omissions.",
                               description=lambda tier: "A bounded fixture selection.", track=lambda tier: tier)
        return SimpleNamespace(plan=plan, tier="large" if large else "small",
            id="fixture-large" if large else "fixture-small", edition=edition,
            periods=periods, paragraphs={("Ps", 23, 1): "printed"},
            digest=lambda: catalog._sha(catalog._canonical(readings)),
            counts=lambda: {"readings": len(readings), "refused": sum(bool(row["refused"]) for row in readings),
                            "chapters": 1, "verses": sum(len(row["verses"]) for row in readings)})

    def test_reading_units_preserve_order_numbering_pilcrow_and_refusal(self):
        volume = self.volume()
        units = catalog._reading_print_units(volume)
        body = "\n".join(catalog._period_html(volume, period, rows, print_units=True)
                         for period, rows in volume.periods)
        self.assertEqual([row["id"] for row in units], ["reading-3", "reading-7"])
        self.assertEqual([row["source"] for row in units], ["plan#reading=3", "plan#reading=7"])
        self.assertEqual(units[0]["cited"], "Psalms 22:1-2")
        self.assertEqual(units[0]["carried"], "Psalms 23:1-2")
        self.assertEqual(units[1]["verse_count"], 0)
        self.assertEqual(units[1]["refused"], "No exact selected verse in this edition.")
        self.assertIn("¶ First &amp; verse.", body)
        self.assertTrue(catalog._check_print_units(units, body))
        for changed in (body.replace("¶ ", ""), body.replace("23:1-2", "22:1-2"),
                        body.replace("No exact selected verse", "A substituted verse"),
                        body.replace('<sup class="verse-number">2</sup>', '<sup class="verse-number">3</sup>')):
            with self.subTest(changed=changed), self.assertRaisesRegex(
                    catalog.PrintCatalogError, "content or order"):
                catalog._check_print_units(units, changed)

    def test_reading_envelope_binds_intro_period_context_rights_links_and_language(self):
        volume = self.volume()
        title = "Fixture plan: small (Fixture edition)"
        envelope = catalog._reading_print_envelope(volume, title)
        body = '\n'.join(['<article class="source-reader reading-plan" lang="en">',
            '<header><h1>' + title + '</h1></header>', catalog._volume_intro(volume),
            *(catalog._period_html(volume, period, rows, print_units=True) for period, rows in volume.periods),
            catalog._volume_rights(volume), '</article>'])
        self.assertTrue(catalog._check_print_envelope(envelope, body))
        changes = [body.replace(title, "An altered plan title"),
            body.replace("A bounded fixture selection.", ""), body.replace("Visible omissions.", ""),
            body.replace("Period 1", "Altered period"), body.replace("Period context.", "", 1),
            body.replace("Synthetic fixture; no external wording.", "A different rights claim."),
            body.replace("<p>Period context.</p>", "", 1).replace("</article>", "<p>Period context.</p></article>"),
            body.replace("</article>", "<p>Extra unmarked qualification.</p></article>"),
            body.replace('lang="en"', 'lang="la"'),
            body.replace("Fixture edition. Synthetic fixture", '<a href="https://example.org/wrong">Fixture edition</a>. Synthetic fixture')]
        for changed in changes:
            with self.subTest(changed=changed), self.assertRaisesRegex(catalog.PrintCatalogError, "envelope"):
                catalog._check_print_envelope(envelope, changed)

    def test_large_volume_keeps_controller_and_parts_do_not_claim_products(self):
        small, large = self.volume(), self.volume(large=True)
        module = SimpleNamespace(plans=lambda root: [small.plan],
            volumes=lambda plan: [("small", "fixture"), ("large", "fixture")],
            Volume=lambda plan, tier, name, root: small if tier == "small" else large,
            paragraphs_module=lambda: SimpleNamespace(PRINTED="printed"))
        source_paths = {small.plan.path.relative_to(self.root).as_posix(),
                        (small.edition.artifacts.parent / "edition.toml").relative_to(self.root).as_posix()}
        with patch.object(catalog, "_bible_typesetter", return_value=module), \
                patch.object(catalog, "_bible_sources", return_value=source_paths):
            pages = catalog._reading_plan_pages(self.root)
        inline = pages["reading-plans/fixture-small.html"]["print_product"]
        self.assertEqual(inline["output_id"], "reading-plan:fixture-small")
        self.assertEqual(inline["mode"], "inline")
        root_page = pages["reading-plans/fixture-large.html"]
        self.assertEqual(root_page["print_product"]["mode"], "legacy-volume")
        self.assertIn('data-print-volume-ready="false"', root_page["html"])
        self.assertIn('<script src="../shared/print-volume.js"></script>', root_page["html"])
        self.assertEqual(len(root_page["part_routes"]), 2)
        for route in root_page["part_routes"]:
            self.assertNotIn("print_product", pages[route])
            self.assertNotIn("legacy_pdf", pages[route])
            self.assertNotIn("data-print-unit=", pages[route]["html"])
            self.assertEqual(len(re.findall(r'<section id="reading-\d+">', pages[route]["html"])), 1)
        self.assertEqual(len(pages), 4)


class SourcePrintMetadataCorpusTests(unittest.TestCase):
    def test_complete_current_admissions_have_independent_source_proofs(self):
        verified = self.enterContext(products.verified_products(ROOT, product_ids={"encyclicals"}))
        original_open = Path.open

        def source_only(path, *args, **kwargs):
            self.assertNotEqual(path.suffix.lower(), ".pdf", "source print metadata read a PDF")
            self.assertNotIn("release/papal-documents/inputs/", path.as_posix(),
                             "source print metadata read an original historical snapshot")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", source_only):
            pages = catalog.source_pages(ROOT, data_root=verified.data_root,
                                         data_source_paths=[products.MANIFEST_RELATIVE])
        papal = [page for route, page in pages.items() if route.startswith("papal-documents/")]
        plans = [page for route, page in pages.items() if route.startswith("reading-plans/") and page.get("legacy_pdf")]
        parts = [page for route, page in pages.items() if route.startswith("reading-plans/") and not page.get("legacy_pdf")]
        self.assertEqual((len(papal), len(plans), len(parts)), (350, 6, 24))
        metadata = [page["print_product"] for page in papal + plans]
        self.assertEqual(len({row["output_id"] for row in metadata}), 356)
        self.assertEqual(sum(row["mode"] == "inline" for row in metadata), 354)
        self.assertEqual(sum(row["mode"] == "legacy-volume" for row in metadata), 2)
        self.assertTrue(all("print_product" not in page for page in parts))
        for page in papal + plans:
            product = page["print_product"]
            self.assertEqual(product["coverage_result"]["status"], "pass")
            if product["mode"] == "inline":
                self.assertEqual(catalog._check_print_units(product["expected_units"], page["html"]),
                                 product["coverage_result"]["actual_units_sha256"])
        print(json.dumps({"papal": len(papal), "reading_plan_roots": len(plans), "period_components": len(parts),
            "inline_products": 354, "legacy_volume_products": 2,
            "papal_blocks": sum(row["counts"]["blocks"] for row in metadata if row["output_id"].startswith("papal:")),
            "reading_units": sum(row["counts"]["readings"] for row in metadata if row["output_id"].startswith("reading-plan:"))}, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
