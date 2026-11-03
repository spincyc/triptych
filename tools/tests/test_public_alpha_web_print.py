from __future__ import annotations

import copy
import hashlib
import importlib
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest import mock

from . import test_public_alpha_source_first as fixtures


def digest(body):
    return hashlib.sha256(body).hexdigest()


class PublicAlphaWebPrintTest(unittest.TestCase):
    """The publisher independently closes prepared print products and routes."""

    def setUp(self):
        self.base = fixtures.PublicAlphaSourceFirstTest(methodName="runTest")
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.tool, self.root = self.base.tool, self.base.root
        self.identifier = "publication:gpt/work"
        self.route = "print/gpt/work.html"
        self.body = '<section data-print-part="complete" data-print-unit="body"><h1>Full source title</h1><p>Terminal source qualification.</p></section>'
        units = [{"id": "body", "source": "src/gpt/work/main.tex", "occurrence": "body:1"}]
        product = {"schema": "triptych-web-print-document/v1", "id": self.identifier,
                   "output_id": self.identifier, "root_route": self.route, "print_type": "flow",
                   "source_digest": "a" * 64, "selection_digest": "b" * 64,
                   "expected_units": units, "parts": [{"id": "complete", "units": ["body"]}]}
        product["coverage_result"] = {"status": "pass", "output_id": self.identifier,
                                      "source_digest": "a" * 64, "selection_digest": "b" * 64,
                                      "expected_units": units}
        from _web_print_common import part_statistics
        statistics = part_statistics(self.body, part_id="complete", selectors=())
        product.pop("expected_units")
        product["unit_inventory"] = self.tool.print_unit_inventory(["body"])
        product["style_sha256"] = digest(b"/* complete print */")
        product["coverage_result"].pop("expected_units")
        product["coverage_result"]["unit_inventory"] = product["unit_inventory"].copy()
        product["parts"] = [{"id": "complete", "selector": '[data-print-part="complete"]',
                             **statistics, "expected_ids": self.tool.print_unit_inventory(statistics["expected_ids"]),
                             "units": self.tool.print_unit_inventory(statistics["units"])}]
        self.inventory = {
            "products": {self.identifier: product},
            "pages": {self.route: {"output_id": self.identifier, "title": "Full source title", "html": self.body}},
            "assets": {"shared/web-print.css": {"body": b"/* complete print */", "owners": [self.identifier],
                         "sha256": digest(b"/* complete print */"), "bytes": len(b"/* complete print */")}},
            "reader_actions": {"web/gpt/work.html": {"output_id": self.identifier, "mode": "navigate", "target": self.route}},
            "source_paths": ["src/gpt/work/main.tex"],
        }

    def checked(self, inventory=None):
        return self.tool.validate_web_print_catalog(inventory or self.inventory, {("gpt", "work")}, {})

    def install(self):
        self.base.write("scripts/_web_print.py", b"# declared source-first print orchestrator\n")
        self.catalog_requests = []

        def catalog(root, included_outputs, **kwargs):
            self.catalog_requests.append((root, included_outputs, kwargs))
            return copy.deepcopy(self.inventory)

        def decorate(content, route, inventory, *, relative_link):
            href = relative_link(route, self.route) + "?print=1"
            return ('<div data-web-print-reader><p data-web-print-reader-notice>Use Print to prepare the complete edition.</p>'
                    '<a href="' + href + '">Print</a><div data-web-print-reader-content>' + content + '</div></div>',
                    '<link rel="stylesheet" href="' + relative_link(route, 'shared/web-print.css') + '">', "")

        module = SimpleNamespace(catalog=catalog,
                                 decorate_reader=decorate,
                                 decorate_source_page=lambda route, page, inventory: page)
        patch = mock.patch.dict("sys.modules", {"_web_print": module})
        patch.start()
        self.addCleanup(patch.stop)

    def test_catalog_receives_current_page_routes_and_already_owned_gallery_asset_routes(self):
        self.install()
        self.base.write(self.tool.PICTORIAL_MANIFEST_RELATIVE.as_posix(), b"declared fixture gallery\n")
        source = self.root / "src/gpt/work/figure.png"
        with mock.patch.object(self.tool, "pictorial_gallery_data", return_value=[{
            "source": source, "destination": "assets/gallery/figure.png",
        }]), self.tool.held_repository_inputs():
            self.tool.web_print_catalog()
        _, _, request = self.catalog_requests[-1]
        self.assertEqual(request["site_routes"], {
            **self.tool.PAGE_MAP, **self.tool.included_document_pages({("gpt", "work")}),
        })
        self.assertEqual(request["canonical_asset_routes"], {"src/gpt/work/figure.png": "assets/gallery/figure.png"})

    def test_prepared_full_print_and_guarded_reviewed_reader_build_and_verify(self):
        self.install()
        publications, output = self.base.build_verified()
        page = (output / self.route).read_text()
        reader = (output / "web/gpt/work.html").read_text()
        self.assertIn("Terminal source qualification.", page)
        self.assertNotIn("Generate the PDF from a local", page)
        self.assertIn("The terminal appendix", reader)
        self.assertIn('data-web-print-reader-notice', reader)
        self.assertIn('href="../../print/gpt/work.html?print=1"', reader)
        self.assertTrue((output / "shared/web-print.css").is_file())
        publication_manifest = json.loads((output / "PUBLICATION-MANIFEST.json").read_text())
        self.assertEqual(publication_manifest["publications"][0]["print"], self.route)
        (output / self.route).write_text(page.replace("Terminal source qualification.", "Omitted."))
        self.tool.write_checksums(output)
        with self.assertRaisesRegex(self.tool.ReleaseError, "print page does not match|print landing does not match"):
            self.tool.verify_output(self.base.manifest, publications, output, False)

    def test_served_catalogue_automatic_print_covers_modern_and_legacy_admitted_outputs_only(self):
        held = {"id": "gpt/held", "status": "hold", "available": {"print": False}, "targets": {}}
        corpus = {"works": [{"editions": [{
            "id": "gpt/work", "provider": "gpt", "print_mode": "manual",
            "targets": {"reader": "web/gpt/work.html", "print": self.route},
            "also": [{"kind": "synthesis", "pdf": "pdf/gpt/work-synthesis.pdf", "print_mode": "manual"}, held],
        }]}]}
        relative = "src/web/data/structure/documents/corpus.json"
        original = json.dumps(corpus).encode()
        self.base.write(relative, original)
        aliases = {"pdf/gpt/work.pdf": "web/gpt/work.html",
                   "pdf/gpt/work-synthesis.pdf": "web/gpt/work-synthesis.html"}
        projected = lambda: json.loads(self.tool.projected_document_catalogue(
            "browse/structure/documents/corpus.json", self.root / relative, aliases))
        manual = projected()["works"][0]["editions"][0]
        self.assertEqual(manual["print_mode"], "manual")
        self.assertEqual(manual["targets"]["print"], self.route)
        self.install()
        browser = projected()["works"][0]["editions"][0]
        self.assertEqual(browser["print_mode"], "browser")
        self.assertEqual(browser["targets"]["print"], self.route + "?print=1")
        self.assertEqual(browser["also"][0]["print_mode"], "browser")
        self.assertEqual(browser["also"][0]["targets"]["print"], "print/gpt/work-synthesis.html?print=1")
        self.assertEqual(browser["also"][1], held)
        self.assertEqual((self.root / relative).read_bytes(), original)

    def test_held_output_unrelated_routes_wrong_reader_edge_and_changed_coverage_fail(self):
        for kind in ("held", "route", "edge", "coverage", "missing"):
            value = copy.deepcopy(self.inventory)
            if kind == "held":
                value["products"]["publication:gpt/held"] = value["products"][self.identifier]
            elif kind == "route":
                value["pages"]["print/gpt/held.html"] = value["pages"].pop(self.route)
            elif kind == "edge":
                value["reader_actions"]["liturgy/day.html"] = value["reader_actions"].pop("web/gpt/work.html")
            elif kind == "coverage":
                value["products"][self.identifier]["coverage_result"]["selection_digest"] = "c" * 64
            else:
                value["products"].clear()
            with self.subTest(kind=kind), self.assertRaises(self.tool.ReleaseError):
                self.checked(value)

    def test_print_fragment_cannot_replace_reviewed_reader_or_bypass_wrapper(self):
        for route, fragment in (("web/gpt/work.html", self.body), (self.route, "<html>Bypass</html>")):
            value = copy.deepcopy(self.inventory)
            value["pages"] = {route: {"output_id": self.identifier, "title": "Full", "html": fragment}}
            with self.assertRaises(self.tool.ReleaseError):
                self.checked(value)
        page = {"title": "Full", "html": "x" * self.tool.PREVIEW_DOCUMENT_LIMIT}
        with self.assertRaisesRegex(self.tool.ReleaseError, "1 MB"):
            self.tool.render_web_print_page(self.route, page, False, {})

    def test_exact_immutable_assets_reject_mutation_active_svg_and_symlink_source(self):
        for body in (bytearray(b"not immutable"), b'<svg xmlns="http://www.w3.org/2000/svg"><script/></svg>'):
            value = copy.deepcopy(self.inventory)
            value["assets"] = {"print/assets/figure.svg": {"body": body, "owners": [self.identifier],
                "bytes": len(body), "sha256": digest(body), "role": "diagram", "mime": "image/svg+xml"}}
            with self.assertRaises(self.tool.ReleaseError):
                self.checked(value)
        source = self.root / "alias.txt"
        source.symlink_to(self.root / "src/gpt/work/main.tex")
        value = copy.deepcopy(self.inventory)
        body = source.read_bytes()
        value["assets"] = {"print/assets/source.txt": {"path": source, "owners": [self.identifier],
            "bytes": len(body), "sha256": digest(body)}}
        with self.assertRaisesRegex(self.tool.ReleaseError, "symlink"):
            self.checked(value)

    def test_canonical_inputs_reject_cache_paths_and_compact_coverage_binds_inventory(self):
        value = copy.deepcopy(self.inventory)
        value["source_paths"] = [".scratch/generated.html"]
        with self.assertRaises(self.tool.ReleaseError):
            self.checked(value)
        product = value["products"][self.identifier]
        product["unit_inventory"] = self.tool.print_unit_inventory(["body"])
        product["coverage_result"]["unit_inventory"] = {"count": 1, "sha256": "c" * 64}
        with self.assertRaisesRegex(self.tool.ReleaseError, "compact"):
            self.tool.validate_print_coverage(self.identifier, product)

    def test_part_structure_text_and_order_are_measured_from_actual_canonical_html(self):
        for field in ("text", "structure", "ids", "units"):
            value = copy.deepcopy(self.inventory)
            product = value["products"][self.identifier]
            if field == "text":
                value["pages"][self.route]["html"] = self.body.replace("Terminal", "Missing")
            elif field == "structure":
                value["pages"][self.route]["html"] = self.body.replace("<h1>", '<h1 title="Changed structure">')
            elif field == "ids":
                product["parts"][0]["expected_ids"] = self.tool.print_unit_inventory(["invented"])
            else:
                # Even self-consistent whole-proof claims cannot change the
                # actual ordered units present in the emitted canonical part.
                product["unit_inventory"] = self.tool.print_unit_inventory(["other"])
                product["coverage_result"]["unit_inventory"] = product["unit_inventory"].copy()
            with self.subTest(field=field), self.assertRaises(self.tool.ReleaseError):
                self.checked(value)

    def test_bible_offer_requires_canonical_publishability_and_complete_matching_product(self):
        from _bible_editions import EDITIONS
        slug = "douay-rheims"
        identifier = "bible:" + slug
        route = "print/bibles/" + slug + ".html"
        row = {"id": slug, "source_id": EDITIONS[slug]["source_id"],
               "print": {"id": identifier, "kind": "bible", "format": "browser", "href": route + "?print=1"}}
        product = copy.deepcopy(self.inventory["products"][self.identifier])
        product.update(id=identifier, output_id=identifier, root_route=route, print_type="bible", source_id=row["source_id"])
        product["coverage_result"]["output_id"] = identifier
        catalog = {"products": {identifier: product}, "pages": {route: {"output_id": identifier}}}
        manifest = self.root / "bibles.json"
        with mock.patch.object(self.tool, "web_data_manifest_path", return_value=manifest):
            for mutate in (lambda: None, lambda: product.update(source_id="wrong"),
                           lambda: row.update(id="knox")):
                mutate()
                manifest.write_text(json.dumps({"bibles": [row]}))
                if row["id"] == slug and product["source_id"] == row["source_id"]:
                    self.tool.validate_bible_print_offers(catalog)
                else:
                    with self.assertRaises(self.tool.ReleaseError):
                        self.tool.validate_bible_print_offers(catalog)

    def source_fixture(self):
        from _print_catalog import _print_envelope
        from _web_print_common import part_statistics
        identifier, route = "papal:fixture/la", "papal-documents/fixture.html"
        value = copy.deepcopy(self.inventory)
        product = copy.deepcopy(value["products"][self.identifier])
        product.update(id=identifier, output_id=identifier, root_route=route, print_type="source-volume", source_id="edition.fixture")
        product["coverage_result"]["output_id"] = identifier
        source_body = ('<section data-print-part="complete" data-print-unit="body"><article lang="la">'
                       '<h1>Full source title</h1><p>Terminal source qualification. '
                       '<a href="https://example.org/witness">Canonical witness</a></p></article></section>')
        stats = part_statistics(source_body, part_id="complete")
        product["parts"] = [{"id": "complete", "selector": '[data-print-part="complete"]', **stats,
            "expected_ids": self.tool.print_unit_inventory(stats["expected_ids"]),
            "units": self.tool.print_unit_inventory(stats["units"])}]
        value["products"][identifier] = product
        value["pages"][route] = {"output_id": identifier, "title": "Full source", "html": source_body}
        value["reader_actions"][route] = {"output_id": identifier, "mode": "inline"}
        metadata = {"output_id": identifier, "mode": "inline", "source_id": "edition.fixture",
                    "source_digest": "a" * 64, "selection_digest": "b" * 64,
                    "expected_units": [{"id": "body", "source": "edition.fixture", "occurrence": "body:1"}],
                    "envelope": _print_envelope([
                        ("title", "fixture#title", "Full source title"),
                        ("body", "fixture#body", "Terminal source qualification."),
                        ("witness", "fixture#witness", "Canonical witness"),
                    ], hrefs=["https://example.org/witness"], language="la")}
        sources = {route: {"html": source_body, "print_product": metadata}}
        return value, sources, metadata, identifier, route

    def test_source_descriptor_must_match_current_independent_owner_proof(self):
        value, sources, metadata, identifier, route = self.source_fixture()
        self.tool.validate_web_print_catalog(value, {("gpt", "work")}, sources)
        metadata["selection_digest"] = "c" * 64
        with self.assertRaisesRegex(self.tool.ReleaseError, "current source-owner proof"):
            self.tool.validate_web_print_catalog(value, {("gpt", "work")}, sources)
        metadata["selection_digest"] = "b" * 64
        for omitted in ("product", "action", "all"):
            changed = copy.deepcopy(value)
            if omitted in {"product", "all"}:
                del changed["products"][identifier]
                del changed["pages"][route]
            if omitted in {"action", "all"}:
                del changed["reader_actions"][route]
            with self.subTest(omitted=omitted), self.assertRaises(self.tool.ReleaseError):
                self.tool.validate_web_print_catalog(changed, {("gpt", "work")}, sources)

    def test_recomputed_part_pins_cannot_replace_source_apparatus_links_or_language(self):
        from _web_print_common import part_statistics
        for kind in ("apparatus", "href", "language"):
            value, sources, _, identifier, route = self.source_fixture()
            body = value["pages"][route]["html"]
            if kind == "apparatus":
                body = body.replace('<a href="https://example.org/witness">Canonical witness</a>', "")
            elif kind == "href":
                body = body.replace("https://example.org/witness", "https://example.org/other")
            else:
                body = body.replace('lang="la"', 'lang="en"')
            value["pages"][route]["html"] = body
            stats = part_statistics(body, part_id="complete")
            value["products"][identifier]["parts"][0].update({
                **stats, "expected_ids": self.tool.print_unit_inventory(stats["expected_ids"]),
                "units": self.tool.print_unit_inventory(stats["units"]),
            })
            with self.subTest(kind=kind), self.assertRaisesRegex(self.tool.ReleaseError, "source print envelope"):
                self.tool.validate_web_print_catalog(value, {("gpt", "work")}, sources)

    def test_legacy_complete_volume_action_retains_its_existing_source_owner(self):
        route, identifier = "reading-plans/fullaccount.html", "reading-plan:fullaccount"
        value = copy.deepcopy(self.inventory)
        value["reader_actions"][route] = {"output_id": identifier, "mode": "legacy-volume"}
        sources = {route: {"print_product": {"output_id": identifier, "mode": "legacy-volume"}}}
        self.tool.validate_web_print_catalog(value, {("gpt", "work")}, sources)
        del value["reader_actions"][route]
        with self.assertRaisesRegex(self.tool.ReleaseError, "reader action"):
            self.tool.validate_web_print_catalog(value, {("gpt", "work")}, sources)
        value["reader_actions"][route] = {"output_id": identifier, "mode": "legacy-volume"}
        sources[route]["print_product"]["mode"] = "inline"
        with self.assertRaises(self.tool.ReleaseError):
            self.tool.validate_web_print_catalog(value, {("gpt", "work")}, sources)

    def test_provider_reader_action_is_required_and_targets_complete_root(self):
        for change in ("absent", "partial", "mode"):
            value = copy.deepcopy(self.inventory)
            if change == "absent":
                value["reader_actions"].clear()
            elif change == "partial":
                part_route = "print/gpt/work/notes.html"
                value["pages"][part_route] = copy.deepcopy(value["pages"][self.route])
                value["reader_actions"]["web/gpt/work.html"]["target"] = part_route
            else:
                value["reader_actions"]["web/gpt/work.html"]["mode"] = "inline"
            with self.subTest(change=change), self.assertRaisesRegex(self.tool.ReleaseError, "reader action"):
                self.checked(value)

    def test_private_delivery_is_exact_and_never_copied_by_prefix_guessing(self):
        files = {"bibles.json": Path("public"), "unusual/preparation.json": Path("private")}
        products = SimpleNamespace(files=files, delivery_by_path={
            "bibles.json": "browser-data", "unusual/preparation.json": "print-preparation"})
        self.assertEqual(self.tool.browser_delivery_files(products), {"bibles.json": Path("public")})
        for modes in ({"bibles.json": "browser-data"}, {name: "unknown" for name in files}):
            products.delivery_by_path = modes
            with self.assertRaises(self.tool.ReleaseError):
                self.tool.browser_delivery_files(products)


if __name__ == "__main__":
    unittest.main()
