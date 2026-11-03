"""Hot source assembly measures complete owned readers without doing I/O."""
from __future__ import annotations

import copy
from pathlib import Path
import posixpath
import re
import socket
import subprocess
import sys
import unittest
from unittest.mock import patch

if __package__:
    from . import test_print_catalog as fixtures
    from . import test_papal_input_receipt as receipt_fixtures
else:
    import test_print_catalog as fixtures
    import test_papal_input_receipt as receipt_fixtures

ROOT = fixtures.ROOT
sys.path.insert(0, str(ROOT / "scripts"))
import _print_catalog as owner
import _web_print_common as common
import _web_print_sources as sources


class SourceAssemblyTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".scratch/web-print-source-catalog"
        scratch.mkdir(parents=True, exist_ok=True)
        extracted = receipt_fixtures.InputReceiptTests("runTest")
        with patch.object(fixtures, "ROOT", scratch):
            extracted.setUp()
        self.addCleanup(extracted.doCleanups)
        extracted.cold()
        self.fixture = extracted.fixture
        self.route, self.page = next(iter(owner._papal_pages(self.fixture.root).items()))
        self.font_calls = []

    def fonts(self, route):
        self.font_calls.append(route)
        fonts = [{"family": "Fixture Serif", "weight": str(400 + (index % 2) * 300),
                  "style": "italic" if index % 4 >= 2 else "normal",
                  "sha256": str(index + 1) * 64,
                  "href": posixpath.relpath(f"print-assets/font-{index}.woff2", posixpath.dirname(route))}
                 for index in range(8)]
        fonts.append({"family": "Triptych Punctus Elevatus", "weight": "400", "style": "normal",
            "unicode_range": "U+2E4E", "sha256": "a" * 64,
            "href": posixpath.relpath("shared/fonts/triptych-punctus-elevatus.woff2", posixpath.dirname(route))})
        return fonts

    def prepare(self, pages=None, **kwargs):
        return sources.prepare_sources(pages if pages is not None else {self.route: self.page},
            stylesheet_sha256="c" * 64, fonts_for_route=kwargs.get("fonts_for_route", self.fonts))

    def test_entire_reader_is_one_compact_finally_measured_source_part(self):
        before = copy.deepcopy(self.page)
        result = self.prepare()
        identifier = self.page["print_product"]["output_id"]
        self.assertEqual(set(result), {"products", "pages", "reader_actions", "source_paths"})
        self.assertEqual(set(result["products"]), {identifier})
        compact, page = result["products"][identifier], result["pages"][self.route]
        self.assertEqual(self.page, before)
        self.assertEqual(page["output_id"], identifier)
        self.assertEqual(page["source_paths"], self.page["source_paths"])
        self.assertEqual(page["print_product"], self.page["print_product"])
        self.assertIn(self.page["html"], page["html"])
        self.assertTrue(page["html"].startswith('<section data-print-part="source-complete" data-print-document="' + identifier))
        self.assertIn('data-print-source="' + self.page["print_product"]["source_digest"] + '"', page["html"])
        self.assertIn("Historical fragment", page["html"])
        self.assertIn("outside the project licence", page["html"])
        self.assertNotIn("data-web-print-start", page["html"])
        self.assertNotIn("head_extra", page)
        self.assertNotIn("body_extra", page)
        self.assertEqual(compact["root_route"], self.route)
        self.assertEqual(compact["output_id"], identifier)
        self.assertEqual(compact["source_id"], self.page["print_product"]["source_id"])
        self.assertEqual(compact["style_sha256"], "c" * 64)
        self.assertEqual(compact["unit_inventory"], common.inventory(["papal-block-1", "papal-block-2", "papal-block-3"]))
        self.assertNotIn("expected_units", compact)
        self.assertNotIn("sources", compact)
        self.assertNotIn("html", compact["parts"][0])
        part = compact["parts"][0]
        self.assertEqual(part["selector"], '[data-print-part="source-complete"]')
        self.assertNotIn("href", part)
        measured = common.part_statistics(page["html"], part_id="source-complete")
        for key in ("text_sha256", "structure_sha256", "counts"):
            self.assertEqual(part[key], measured[key])
        self.assertEqual(part["units"], common.inventory(measured["units"]))
        self.assertEqual(part["expected_ids"], common.inventory(measured["expected_ids"]))
        self.assertEqual(result["reader_actions"], {self.route: {"output_id": identifier, "mode": "inline"}})
        self.assertTrue(set(self.page["source_paths"]).issubset(result["source_paths"]))
        self.assertTrue(set(sources.HELPERS).issubset(result["source_paths"]))

    def test_fonts_use_final_reader_route_and_retain_punctus_range(self):
        result = self.prepare()
        self.assertEqual(self.font_calls, [self.route])
        descriptor = next(iter(result["products"].values()))
        self.assertEqual(len(descriptor["fonts"]), 9)
        glyph = descriptor["fonts"][-1]
        self.assertEqual(glyph["href"], "../shared/fonts/triptych-punctus-elevatus.woff2")
        self.assertEqual(glyph["unicode_range"], "U+2E4E")
        self.assertTrue(all(face["href"].startswith("../") for face in descriptor["fonts"]))

    def test_legacy_roots_and_period_components_do_not_create_common_products(self):
        legacy_route, part_route = "reading-plans/full.html", "reading-plans/full/period-one.html"
        legacy = {"html": '<article data-print-volume-ready="false"><script src="../shared/print-volume.js"></script></article>',
                  "source_paths": ["src/web/browser/shared/print-volume.js"],
                  "print_product": {"output_id": "reading-plan:full", "mode": "legacy-volume"}}
        part = {"html": "<article><p>One period only.</p></article>", "source_paths": ["LICENSE"]}
        pages = {self.route: self.page, legacy_route: legacy, part_route: part}
        before = copy.deepcopy(pages)
        result = self.prepare(pages)
        self.assertEqual(pages, before)
        self.assertEqual(set(result["pages"]), {self.route})
        self.assertEqual(len(result["products"]), 1)
        self.assertEqual(result["reader_actions"][legacy_route], {"output_id": "reading-plan:full", "mode": "legacy-volume"})
        self.assertNotIn(part_route, result["reader_actions"])
        self.assertEqual(self.font_calls, [self.route])

    def test_hot_assembly_performs_no_file_process_or_network_access(self):
        with patch.object(Path, "open", side_effect=AssertionError("hot file access")), \
                patch.object(Path, "read_bytes", side_effect=AssertionError("hot file access")), \
                patch.object(subprocess, "run", side_effect=AssertionError("hot process")), \
                patch.object(socket, "socket", side_effect=AssertionError("hot network")):
            self.assertEqual(len(self.prepare()["products"]), 1)

    def test_unproved_wrong_output_or_stale_content_never_receives_pass(self):
        for mutation in ("status", "output", "selection", "units", "actual", "wording", "unmarked"):
            with self.subTest(mutation=mutation):
                page = copy.deepcopy(self.page)
                product = page["print_product"]
                if mutation == "status":
                    product["coverage_result"]["status"] = "not-checked"
                elif mutation == "output":
                    product["coverage_result"]["output_id"] = "papal:other/en"
                elif mutation == "selection":
                    product["coverage_result"]["selection_digest"] = "d" * 64
                elif mutation == "units":
                    product["coverage_result"]["expected_units"] = []
                elif mutation == "actual":
                    product["coverage_result"]["actual_units_sha256"] = "d" * 64
                elif mutation == "wording":
                    page["html"] = page["html"].replace("Historical note;", "Rewritten note;")
                else:
                    page["html"] = page["html"].replace(' data-print-unit="papal-block-3"', "")
                with self.assertRaises(ValueError):
                    self.prepare({self.route: page})

    def test_unsupported_styles_broken_tree_and_repeated_unit_are_refused(self):
        changes = [self.page["html"].replace('<p data-print-unit="papal-block-1"',
                                            '<p style="display:none" data-print-unit="papal-block-1"'),
                   self.page["html"].replace("</article>", "</p></article>"),
                   self.page["html"].replace('data-print-unit="papal-block-3"', 'data-print-unit="papal-block-2"')]
        for body in changes:
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.prepare({self.route: {**self.page, "html": body}})

    def test_complete_canonical_qualifications_cannot_be_deleted_rewritten_or_reordered(self):
        body = self.page["html"]
        extent = re.search(r'<p class="source-extent">.*?</p>', body).group()
        variants = [body.replace(extent, ""),
            re.sub(r'<footer class="source-apparatus">.*?</footer>', "", body, flags=re.S),
            body.replace("OCR is not collation", "OCR is fully collated"),
            body.replace("outside the project licence", "inside the project licence"),
            body.replace("Source &lt;title&gt;", "A different title"),
            body.replace(extent, "").replace("</article>", extent + "</article>"),
            body.replace("</article>", "<p>New unmarked qualification.</p></article>"),
            body.replace('href="https://example.org/source"', 'href="https://example.org/other"'),
            body.replace('lang="en"', 'lang="la"')]
        for variant in variants:
            with self.subTest(body=variant), self.assertRaisesRegex(ValueError, "envelope"):
                self.prepare({self.route: {**self.page, "html": variant}})

    def test_rewritten_envelope_cannot_borrow_the_previous_selection_proof(self):
        page = copy.deepcopy(self.page)
        product = page["print_product"]
        page["html"] = page["html"].replace('href="https://example.org/source"', 'href="https://example.org/other"')
        product["envelope"]["hrefs"] = ["https://example.org/other"]
        with self.assertRaisesRegex(ValueError, "owner envelope check"):
            self.prepare({self.route: page})
        # Updating a local envelope hash still cannot inherit the old source
        # selection's independent proof and its bound canonical envelope.
        envelope_sha = owner._sha(owner._canonical(product["envelope"]))
        product["envelope_sha256"] = product["coverage_result"]["envelope_sha256"] = envelope_sha
        with self.assertRaisesRegex(ValueError, "not bound to the canonical selection"):
            self.prepare({self.route: page})

    def test_duplicate_output_unsafe_routes_and_binary_source_paths_fail(self):
        for other_route in ("../outside.html", "/absolute.html", "papal-documents//duplicate.html"):
            with self.subTest(route=other_route), self.assertRaises(ValueError):
                self.prepare({other_route: self.page})
        duplicate = copy.deepcopy(self.page)
        duplicate["print_product"]["root_route"] = "papal-documents/duplicate.html"
        with self.assertRaisesRegex(ValueError, "more than one reader"):
            self.prepare({self.route: self.page, "papal-documents/duplicate.html": duplicate})
        for path in ("pdf/old.pdf", "release/papal-documents/inputs/frozen.json", ".scratch/cache/text.txt"):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "canonical text or metadata"):
                self.prepare({self.route: {**self.page, "source_paths": [path]}})

    def test_missing_or_remote_font_pins_are_refused(self):
        bad_fonts = [[], [{"family": "Fixture", "href": "../font.woff2", "sha256": "not-a-hash"}],
                     [{"family": "Fixture", "href": "https://example.org/font.woff2", "sha256": "b" * 64}],
                     [{"family": "Fixture", "href": "../../outside.woff2", "sha256": "b" * 64}]]
        for fonts in bad_fonts:
            with self.subTest(fonts=fonts), self.assertRaises(ValueError):
                self.prepare(fonts_for_route=lambda route: fonts)


if __name__ == "__main__":
    unittest.main()
