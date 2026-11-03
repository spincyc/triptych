"""Exercise the HOT catalogue from a test-only held private preparation tree.

The core snapshot is mocked at its documented boundary. Tiny fixture font bytes
exercise transport identities, not browser font decoding or publication proof.
No converter, source acquisition, real descriptor or cache record is involved.
"""
from __future__ import annotations

import base64
import copy
from html.parser import HTMLParser
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import posixpath
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _bible_editions as editions
import _web_print as web
from _web_print_common import inventory, part_statistics, sha256
from _web_print_prepare import AssetPool, CATALOG_SCHEMA, PREFIX, PreparationError, canonical_json, digest, prepare_product, write_json

SCRATCH = ROOT / ".scratch/web-print-catalog-tests"


class Elements(HTMLParser):
    def __init__(self, fragment):
        super().__init__(convert_charrefs=True)
        self.ids, self.hrefs, self.images, self.manifests = set(), [], [], []
        self.image_attrs = []
        self.manifest = None
        self.feed(fragment)
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a":
            self.hrefs.append(values["href"])
        if tag == "img":
            self.images.append(values["src"])
            self.image_attrs.append(attrs)
        if tag == "script" and "data-web-print-manifest" in values:
            self.manifest = []
    def handle_data(self, data):
        if self.manifest is not None:
            self.manifest.append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self.manifest is not None:
            self.manifests.append(json.loads("".join(self.manifest)))
            self.manifest = None


class WebPrintCatalogTest(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.data = self.root / ".scratch/private-products"
        self.destination = self.data / PREFIX
        self.destination.mkdir(parents=True)
        for relative in ("scripts/_web_print.py", "scripts/_web_print_sources.py", "scripts/_web_print_links.py", "scripts/_print_catalog.py",
                         "scripts/_web_print_common.py", "scripts/_web_print_prepare.py"):
            self.write(relative, b"# canonical fixture helper\n")
        for relative, body in (
            (web.SHARED + "web-print.css", b"/* pinned fixture style */"),
            (web.SHARED + "web-print.js", b"// pinned fixture controller\n"),
            (web.SHARED + "fonts/triptych-punctus-elevatus.woff2", b"wOF2punctus-fixture"),
            (web.SHARED + "fonts/OFL-Junicode.txt", b"Fixture font licence\n"),
            ("src/common/browser-print-fonts/OFL.txt", b"Fixture OFL licence\n"),
            ("src/common/browser-print-source-marks/OFL.txt", b"Fixture source marks OFL licence\n"),
            ("src/gpt/work/main.tex", b"Canonical fixture study\n"),
            ("src/sources/bibles/fixture.tsv", b"Canonical fixture verse\n"),
            ("requirements-public-alpha.txt", (ROOT / "requirements-public-alpha.txt").read_bytes()),
        ):
            self.write(relative, body)
        self.pool = AssetPool(self.root, self.destination)
        licence = self.pool.add({"mime": "text/plain", "body": b"Fixture OFL licence\n",
            "sha256": sha256(b"Fixture OFL licence\n")}, role="font-license",
            canonical_path="src/common/browser-print-fonts/OFL.txt")
        for index, (family, weight, style) in enumerate((
            ("Libertinus Serif", "400", "normal"), ("Libertinus Serif", "400", "italic"),
            ("Libertinus Serif", "700", "normal"), ("Libertinus Serif", "700", "italic"),
            ("Libertinus Sans", "400", "normal"), ("Libertinus Sans", "400", "italic"),
            ("Libertinus Sans", "700", "normal"), ("Libertinus Math", "400", "normal"),
        )):
            body = b"wOF2fixture-face-" + str(index).encode()
            self.pool.add({"mime": "font/woff2", "body": body, "sha256": sha256(body),
                "family": family, "weight": weight, "style": style,
                "license": self.pool.records[licence]["asset"]["src"]}, role="font")
        marks_licence = self.pool.add({"mime": "text/plain", "body": b"Fixture source marks OFL licence\n",
            "sha256": sha256(b"Fixture source marks OFL licence\n")}, role="font-license",
            canonical_path="src/common/browser-print-source-marks/OFL.txt")
        marks_body = b"wOF2fixture-source-marks"
        self.marks_id = self.pool.add({"mime": "font/woff2", "body": marks_body, "sha256": sha256(marks_body),
            "family": "Triptych Source Marks", "weight": "400", "style": "normal",
            "unicode_range": "U+211F,U+2123,U+21A9,U+2610,U+2720",
            "license": self.pool.records[marks_licence]["asset"]["src"]}, role="font")
        self.image_path = "src/gpt/work/plate.png"
        image = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aCfoAAAAASUVORK5CYII=")
        self.write(self.image_path, image)
        self.image_id = self.pool.add({"source": self.image_path, "mime": "image/png", "sha256": sha256(image)}, role="illustration")
        self.identifier, self.bible = "publication:gpt/work", "bible:fixture"
        self.publication = self.raw_product(self.identifier, "flow", [
            {"id": "opening", "html": '<h1 id="heading">Full source title</h1><p id="fnref1" data-print-unit="body">Opening source '
                '<a href="#fn1">1</a>.</p><figure><img data-print-asset="plate" src="plate.png" alt="Source illustration"></figure>'},
            {"id": "notes", "html": '<p id="fn1" data-print-unit="notes">Terminal source qualification. <a href="#fnref1">Return</a></p>'},
        ], ["body", "notes"])
        self.publication["title"] = "Full source </script><script>metadata</script>"
        bible = self.raw_product(self.bible, "bible", [
            {"id": "chapter", "html": '<p id="verse" data-print-unit="verse">Complete fixture verse.</p>'},
        ], ["verse"])
        bible.update(root_route="print/bibles/fixture.html", source_id="edition.fixture")
        self.recipes = {
            self.identifier: {"id": self.identifier, "provider": "gpt", "document": "work", "kind": "article",
                "entrypoint": "src/gpt/work/main.tex", "source_paths": ["src/gpt/work/main.tex"]},
            self.bible: {"id": self.bible, "entrypoint": "src/sources/bibles/fixture.tsv", "source_paths": ["src/sources/bibles/fixture.tsv"]},
        }
        self.index = {"schema": CATALOG_SCHEMA, "products": [], "assets": self.pool.rows(),
                      "source_paths": sorted(self.pool.source_paths)}
        self.store_product(self.publication, asset_ids={"plate": self.image_id})
        self.store_product(bible)
        self.save_index()
        self.editions = mock.patch.dict(editions.EDITIONS, {"fixture": {"publishable": True, "source_id": "edition.fixture"}}, clear=True)
        self.editions.start()
        self.addCleanup(self.editions.stop)

    def write(self, relative, body):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)

    def raw_product(self, identifier, profile, parts, ids):
        units = [{"id": uid, "source": "canonical.fixture", "occurrence": str(index + 1)} for index, uid in enumerate(ids)]
        result = {"id": identifier, "output_id": identifier, "title": "Complete fixture", "print_type": profile,
            "source_digest": "a" * 64, "selection_digest": "b" * 64, "parts": parts, "expected_units": units,
            "coverage_result": {"status": "pass", "output_id": identifier, "source_digest": "a" * 64,
                "selection_digest": "b" * 64, "expected_units": units}}
        # The synthetic fixture owner has established its independent ledger
        # above. Pin those final body bytes afterward, exactly as real owners do.
        for part in result["parts"]:
            part["html_sha256"] = digest(part["html"])
        return result

    def store_product(self, raw, *, asset_ids=None):
        prepared = prepare_product(raw, self.recipes[raw["id"]], asset_ids=asset_ids)
        self.replace_product(raw["id"], prepared)

    def replace_product(self, identifier, product):
        previous = next((row for row in self.index["products"] if row["id"] == identifier), None)
        if previous:
            (self.destination / previous["path"]).unlink()
            self.index["products"].remove(previous)
        path = "products/" + digest(canonical_json(product)) + ".json"
        write_json(self.destination / path, product)
        self.index["products"].append({"id": identifier, "path": path})

    def save_index(self):
        write_json(self.destination / "catalog.json", self.index)
        files = {path.relative_to(self.data).as_posix(): path for path in self.data.rglob("*.json")}
        self.held = SimpleNamespace(data_root=self.data, files=files,
            delivery_by_path={path: "print-preparation" for path in files})

    def mutate_product(self, change):
        row = next(row for row in self.index["products"] if row["id"] == self.identifier)
        value = json.loads((self.destination / row["path"]).read_bytes())
        change(value)
        self.replace_product(self.identifier, value)
        self.save_index()

    def catalog(self, **kwargs):
        with mock.patch.object(web.core, "require_products", return_value=self.held), \
                mock.patch("subprocess.Popen", side_effect=AssertionError("HOT catalogue invoked a subprocess")):
            return web.catalog(self.root, [("gpt", "work")], browser_data_root=kwargs.pop("browser_data_root", self.data),
                source_pages=kwargs.pop("source_pages", {}),
                canonical_asset_routes={self.image_path: "assets/gallery/plate.png"}, **kwargs)

    def publisher(self):
        loader = importlib.machinery.SourceFileLoader("catalog_fixture_publisher", str(ROOT / "tools/public-alpha"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        module.ROOT = self.root
        self.write("src/web/data/bibles.json", canonical_json({"bibles": [{
            "id": "fixture", "numbering": "vulgate", "source_id": "edition.fixture",
            "print": {"id": self.bible, "kind": "bible", "format": "browser",
                      "href": "print/bibles/fixture.html?print=1"},
        }]}))
        return module

    def test_complete_private_snapshot_has_inline_and_fetched_parts_exact_fonts_and_reused_gallery(self):
        result = self.catalog()
        self.assertEqual(set(result["products"]), {self.identifier, self.bible})
        descriptor = result["products"][self.identifier]
        self.assertIn("selector", descriptor["parts"][0])
        self.assertIn("href", descriptor["parts"][1])
        self.assertEqual(descriptor["unit_inventory"], inventory(["body", "notes"]))
        self.assertEqual(len(descriptor["fonts"]), 10)
        self.assertEqual(next(font["unicode_range"] for font in descriptor["fonts"]
                              if font["family"] == "Triptych Source Marks"), "U+211F,U+2123,U+21A9,U+2610,U+2720")
        root = descriptor["root_route"]
        for font in descriptor["fonts"]:
            route = posixpath.normpath(posixpath.join(posixpath.dirname(root), font["href"]))
            asset = result["assets"][route]
            self.assertEqual(asset["sha256"], font["sha256"])
            self.assertIn(asset["license"], result["assets"])
        self.assertEqual(len({asset["license"] for asset in result["assets"].values() if asset["role"] == "font"}), 3)
        self.assertIn("assets/gallery/plate.png", result["assets"])
        self.assertEqual(result["assets"]["assets/gallery/plate.png"]["path"], self.root / self.image_path)
        self.assertFalse(any(path.startswith(PREFIX) for path in result["pages"] | result["assets"]))

    def test_each_catalog_validates_one_fresh_context_shared_only_by_its_projections(self):
        before = copy.deepcopy(self.publication)
        with mock.patch.object(web, "RoutingContext", wraps=web.RoutingContext) as construct, \
                mock.patch.object(web, "project_parts", wraps=web.project_parts) as project:
            first = self.catalog()
            self.assertEqual(construct.call_count, 1)
            first_calls = list(project.call_args_list)
            self.assertEqual(len(first_calls), 2)
            context = first_calls[0].kwargs["context"]
            self.assertTrue(all(call.kwargs["context"] is context for call in first_calls))
            self.assertTrue(all(set(call.kwargs) == {"entrypoint", "context"} for call in first_calls))
            second = self.catalog()
            self.assertEqual(construct.call_count, 2)
            self.assertIsNot(project.call_args_list[2].kwargs["context"], context)
            self.assertIs(project.call_args_list[2].kwargs["context"], project.call_args_list[3].kwargs["context"])
        self.assertEqual(first, second)
        self.assertEqual(self.publication, before)

    def test_verified_image_geometry_defers_root_alias_and_fetched_parts_without_changing_source(self):
        self.publication["parts"][1]["html"] += '<figure><img data-print-asset="plate" src="plate.png" alt="Repeated source illustration"></figure>'
        self.publication["parts"][1]["html_sha256"] = digest(self.publication["parts"][1]["html"])
        self.store_product(self.publication, asset_ids={"plate": self.image_id})
        self.save_index()
        with mock.patch.object(web, "_png_dimensions", return_value=None):
            eager = self.catalog()
        result = self.catalog()
        image_pages = 0
        for route, page in result["pages"].items():
            before, after = Elements(eager["pages"][route]["html"]), Elements(page["html"])
            self.assertEqual(after.images, before.images)
            self.assertEqual(after.ids, before.ids)
            self.assertEqual(after.hrefs, before.hrefs)
            if after.images:
                image_pages += 1
            for old, new in zip(before.image_attrs, after.image_attrs, strict=True):
                self.assertEqual(new, old + [("width", "1"), ("height", "1"), ("loading", "lazy")])
                self.assertEqual(len(new), len(dict(new)), "alias must not duplicate image attributes")
            for descriptor in after.manifests:
                for part in descriptor["parts"]:
                    body = page["html"] if "selector" in part else result["pages"][posixpath.normpath(
                        posixpath.join(posixpath.dirname(route), part["href"]))]["html"]
                    measured = part_statistics(body, part_id=part["id"], selectors=tuple(part["counts"]))
                    for field in ("text_sha256", "structure_sha256", "counts"):
                        self.assertEqual(measured[field], part[field])
                    self.assertEqual(inventory(measured["units"]), part["units"])
        self.assertEqual(image_pages, 3)

    def test_image_projection_preserves_authored_geometry_loading_and_unknown_dimensions(self):
        for attributes in (' width="42"', ' height="17"', ' loading="eager"',
                           ' width="42" height="17" loading="lazy"'):
            with self.subTest(attributes=attributes):
                body = '<img data-print-asset="plate" src="old.png" alt="Source"' + attributes + ' />'
                self.assertEqual(web._Images(body, {"plate": "new.png"}, {"plate": (1, 1)}).result(),
                                 body.replace("old.png", "new.png"))
        body = '<img data-print-asset="plate" src="old.svg" alt="Source"/>'
        self.assertEqual(web._Images(body, {"plate": "new.svg"}).result(), body.replace("old.svg", "new.svg"))
        projected = web._Images(body, {"plate": "new.png"}, {"plate": (1, 1)}).result()
        self.assertTrue(projected.endswith('width="1" height="1" loading="lazy"/>'))

    def test_geometry_requires_intact_png_header_and_positive_bounded_dimensions(self):
        png = (self.root / self.image_path).read_bytes()
        self.assertEqual(web._png_dimensions(png), (1, 1))
        for body in (png[:32], b"not a PNG" + png, png[:29] + b"\0\0\0\0" + png[33:]):
            self.assertIsNone(web._png_dimensions(body))
        for width in (0, 2**31):
            body = png[:16] + width.to_bytes(4, "big") + png[20:]
            body = body[:29] + web.zlib.crc32(body[12:29]).to_bytes(4, "big") + body[33:]
            self.assertIsNone(web._png_dimensions(body))

    def test_source_marks_face_refuses_an_unbound_or_broadened_unicode_range(self):
        path = self.destination / "assets" / (self.marks_id + ".json")
        record = json.loads(path.read_bytes())
        for value in (None, "U+0000-FFFF", "U+211F,U+2123,U+21A9,U+2720", "U+211F,U+2123"):
            changed = copy.deepcopy(record)
            if value is None:
                del changed["asset"]["unicode_range"]
            else:
                changed["asset"]["unicode_range"] = value
            write_json(path, changed)
            with self.subTest(unicode_range=value), self.assertRaisesRegex(PreparationError, "exact source-mark supplement"):
                self.catalog()

    def test_actual_catalog_result_passes_independent_publisher_contract(self):
        publisher = self.publisher()
        with mock.patch.object(publisher, "included_document_pages", return_value={}):
            result = self.catalog()
            publisher.validate_web_print_catalog(result, {("gpt", "work")}, {})

    def test_invalid_runtime_schema_or_coverage_is_refused_by_catalog_or_independent_publisher(self):
        publisher = self.publisher()
        for field in ("schema", "coverage"):
            def change(value):
                if field == "schema":
                    value["descriptor"]["schema"] = "unrecognized-runtime-schema"
                else:
                    value["descriptor"]["coverage_result"]["selection_digest"] = "c" * 64
            self.mutate_product(change)
            with self.subTest(field=field), mock.patch.object(publisher, "included_document_pages", return_value={}), \
                    self.assertRaises((PreparationError, publisher.ReleaseError)):
                publisher.validate_web_print_catalog(self.catalog(), {("gpt", "work")}, {})
            self.store_product(self.publication, asset_ids={"plate": self.image_id})
            self.save_index()

    def test_alias_keeps_inline_body_links_source_units_and_pins_independent_of_canonical(self):
        result = self.catalog()
        root = result["products"][self.identifier]["root_route"]
        alias = "web/gpt/work.html"
        page = result["pages"][alias]
        self.assertIn("Opening source", page["html"])
        self.assertNotIn("Generate the PDF", page["html"])
        descriptor = Elements(page["html"]).manifests[0]
        self.assertEqual(descriptor["unit_inventory"], result["products"][self.identifier]["unit_inventory"])
        self.assertNotEqual(descriptor["parts"][0]["structure_sha256"], result["products"][self.identifier]["parts"][0]["structure_sha256"])
        measured = part_statistics(page["html"], part_id="opening", selectors=tuple(descriptor["parts"][0]["counts"]))
        self.assertEqual(measured["structure_sha256"], descriptor["parts"][0]["structure_sha256"])
        for route in (root, alias):
            parsed = Elements(result["pages"][route]["html"])
            for href in parsed.hrefs + parsed.images:
                uri = urlsplit(href)
                if uri.scheme or uri.netloc:
                    continue
                target = route if not uri.path else posixpath.normpath(posixpath.join(posixpath.dirname(route), unquote(uri.path)))
                self.assertIn(target, result["pages"] | result["assets"])
                if uri.fragment:
                    self.assertIn(unquote(uri.fragment), Elements(result["pages"][target]["html"]).ids)

    def test_snapshot_identity_membership_and_delivery_boundaries_fail_closed(self):
        with self.assertRaisesRegex(PreparationError, "caller's held"):
            self.catalog(browser_data_root=self.root / "other")
        self.held.files["print/preparation/unlisted.json"] = self.data / "unlisted.json"
        self.held.delivery_by_path["print/preparation/unlisted.json"] = "print-preparation"
        with self.assertRaisesRegex(PreparationError, "exactly own"):
            self.catalog()
        self.save_index()
        member = next(iter(self.held.files))
        self.held.delivery_by_path[member] = "browser-data"
        with self.assertRaisesRegex(PreparationError, "exactly own|delivery boundary"):
            self.catalog()

    def test_corrupted_product_bytes_and_changed_canonical_asset_refuse(self):
        row = next(row for row in self.index["products"] if row["id"] == self.identifier)
        path = self.destination / row["path"]
        original = path.read_bytes()
        path.write_bytes(original.replace(b"Opening source", b"Changed source"))
        with self.assertRaisesRegex(PreparationError, "filename differs"):
            self.catalog()
        path.write_bytes(original)
        self.write(self.image_path, b"changed image bytes")
        with self.assertRaisesRegex(PreparationError, "asset changed"):
            self.catalog()

    def test_changed_raw_owner_body_cannot_reuse_its_previous_successful_pin(self):
        product = copy.deepcopy(self.publication)
        product["parts"][0]["html"] = product["parts"][0]["html"].replace("Opening source", "Changed source")
        with self.assertRaisesRegex(PreparationError, "required owner pin"):
            prepare_product(product, self.recipes[self.identifier], asset_ids={"plate": self.image_id})

    def test_reordered_source_parts_and_held_output_selection_refuse(self):
        def reorder(value):
            value["parts"].reverse()
            value["descriptor"]["parts"].reverse()
        self.mutate_product(reorder)
        with self.assertRaisesRegex(PreparationError, "complete source selection"):
            self.catalog()
        self.store_product(self.publication, asset_ids={"plate": self.image_id})
        self.index["products"].append({"id": "publication:gpt/held", "path": self.index["products"][0]["path"]})
        self.save_index()
        with self.assertRaisesRegex(PreparationError, "admitted output selection"):
            self.catalog()

    def test_malformed_declared_owner_or_part_pin_refuses(self):
        for field in ("owner", "structure", "units"):
            def mutate(value):
                if field == "owner":
                    value["descriptor"]["id"] = "publication:gpt/held"
                elif field == "structure":
                    value["descriptor"]["parts"][0]["structure_sha256"] = "c" * 64
                else:
                    value["descriptor"]["parts"][0]["units"] = inventory(["invented"])
            self.mutate_product(mutate)
            with self.subTest(field=field), self.assertRaises(PreparationError):
                self.catalog()
            self.store_product(self.publication, asset_ids={"plate": self.image_id})
            self.save_index()

    def test_reviewed_reader_body_is_preserved_with_guard_and_complete_destination(self):
        source = "web/gpt/work.md"
        self.write(source, b"# Reviewed source\n\nTerminal reviewed qualification.\n")
        result = self.catalog(site_routes={source: "web/gpt/work.html"})
        self.assertNotIn("web/gpt/work.html", result["pages"])
        original = '<h1>Reviewed title</h1><p id="qualification">Terminal reviewed qualification &amp; limits.</p>'
        content, head, body = web.decorate_reader(original, "web/gpt/work.html", result, relative_link=web.relative_link)
        self.assertIn(original, content)
        self.assertIn("data-web-print-reader-content", content)
        self.assertIn("data-web-print-reader-notice", content)
        self.assertIn("../../print/gpt/work.html?print=1", content)
        self.assertNotIn("data-web-print-document", content)
        self.assertIn("../../shared/web-print.css", head)
        self.assertEqual(body, "")

    def test_legacy_volume_keeps_existing_body_and_owner_action_without_new_product(self):
        route, identifier = "reading-plans/legacy.html", "reading-plan:legacy"
        page = {"title": "Existing complete volume", "html": '<section data-print-volume="legacy">Owned volume controls.</section>',
                "source_paths": [], "print_product": {"output_id": identifier, "mode": "legacy-volume"}}
        before = copy.deepcopy(page)
        result = self.catalog(source_pages={route: page})
        self.assertEqual(page, before)
        self.assertNotIn(route, result["pages"])
        self.assertNotIn(identifier, result["products"])
        self.assertEqual(result["reader_actions"][route], {"output_id": identifier, "mode": "legacy-volume"})

    def test_root_manifest_json_is_inert_and_alias_stays_below_html_budget(self):
        parts = [{"id": part["id"], "html": part["html"]} for part in self.publication["parts"]]
        parts[0]["html"] = parts[0]["html"].replace("Opening source", "X" * 700_000)
        product = self.raw_product(self.identifier, "flow", parts, ["body", "notes"])
        product["title"] = self.publication["title"]
        self.store_product(product, asset_ids={"plate": self.image_id})
        self.save_index()
        result = self.catalog()
        for route in ("print/gpt/work.html", "web/gpt/work.html"):
            body = result["pages"][route]["html"]
            self.assertLess(len(body.encode()), 1_000_000)
            self.assertNotIn("</script><script>metadata", body)
            descriptors = Elements(body).manifests
            self.assertEqual(len(descriptors), 1)
            self.assertEqual(descriptors[0]["title"], self.publication["title"])


if __name__ == "__main__":
    unittest.main()
