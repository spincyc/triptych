from __future__ import annotations

import hashlib
import html
from collections import Counter
from contextlib import ExitStack
from copy import deepcopy
from html.parser import HTMLParser
import importlib.machinery
import importlib.util
from pathlib import Path
import tempfile
import tomllib
import unittest
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TOOL_PATH = REPOSITORY_ROOT / "tools/public-alpha"


def load_tool():
    loader = importlib.machinery.SourceFileLoader(
        "test_pictorial_gallery_tool", str(TOOL_PATH)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    if spec is None:
        raise RuntimeError("could not load tools/public-alpha")
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class DictionaryMarkup(HTMLParser):
    """Small structural reader so the table tests do not rely on string layout."""

    def __init__(self, source: str) -> None:
        super().__init__(convert_charrefs=True)
        self.nodes: list[dict] = []
        self.stack: list[dict] = []
        self.feed(source)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = {"tag": tag, "attrs": dict(attrs), "parents": tuple(self.stack), "text": []}
        self.nodes.append(node)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]["tag"] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        for node in self.stack:
            node["text"].append(data)

    def find(self, tag: str | None = None, css_class: str | None = None) -> list[dict]:
        return [node for node in self.nodes
                if (tag is None or node["tag"] == tag)
                and (css_class is None or css_class in node["attrs"].get("class", "").split())]

    @staticmethod
    def text(node: dict) -> str:
        return " ".join(" ".join(node["text"]).split())


class PictorialGalleryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tool = load_tool()
        cls.cards = cls.tool.pictorial_gallery_data()

    def test_release_ready_union_is_exactly_deduplicated(self) -> None:
        self.assertEqual(len({card["source_relative"] for card in self.cards}), len(self.cards))
        self.assertEqual(len({card["destination"] for card in self.cards}), len(self.cards))
        self.assertEqual(
            sum(len(card["artwork_ids"]) for card in self.cards) - len(self.cards),
            5,
            "full and compact records should merge five duplicate identities",
        )

    def test_gallery_matches_each_native_edition_and_their_union(self) -> None:
        from _native_print_artwork import DICTIONARY, DICTIONARY_LEAVES, dictionary_artwork

        union = set()
        for leaf in DICTIONARY_LEAVES:
            with self.subTest(edition=leaf):
                selected, _ = dictionary_artwork(REPOSITORY_ROOT, "gpt", DICTIONARY + "/" + leaf)
                cards = self.tool.pictorial_gallery_data(leaf)
                self.assertEqual({card["source_relative"] for card in cards}, selected)
                union.update(selected)
        self.assertEqual({card["source_relative"] for card in self.cards}, union)
        with self.assertRaisesRegex(self.tool.ReleaseError, "unknown pictorial dictionary edition"):
            self.tool.pictorial_gallery_data("unknown")

    def test_current_artwork_replaces_superseded_and_unconsumed_views(self) -> None:
        names = {Path(card["source_relative"]).name for card in self.cards}
        self.assertIn("RPD-FIG-vestments-0002-alb-v3-alpha.png", names)
        self.assertNotIn("RPD-FIG-vestments-0002-alb-v2.png", names)
        for stem in ("0001-amice", "0004-maniple"):
            self.assertIn(f"RPD-FIG-vestments-{stem}-cross-2026.png", names)
            self.assertNotIn(f"RPD-FIG-vestments-{stem}-v3-alpha.png", names)
        self.assertNotIn("RPD-FIG-sacred-vessels-0003-comparison-paten-exemplar.png", names)
        # These source-admitted isolated views were wrongly omitted by the old
        # gallery's independent requirement for completed native print reviews.
        self.assertIn("RPD-FIG-sacred-vessels-0007-iso-communion-plate.png", names)
        self.assertIn("RPD-FIG-processional-objects-0003-iso-acolyte-candlestick-v2.png", names)
        # Fixed historical illustration and edition-specific pontifical views
        # must survive; replacing the manifest scan with only one leaf loses them.
        self.assertIn("RPD-FIG-sanctuary-0001-ecce-homo-chapel-rijks-graphite.png", names)
        pontifical = "RPD-FIG-pontifical-0001-three-mitre-forms-v1-alpha-canonical.png"
        self.assertIn(pontifical, names)
        comprehensive = self.tool.pictorial_gallery_data("comprehensive")
        self.assertIn(pontifical, {Path(card["source_relative"]).name for card in comprehensive})

    def test_selected_artwork_without_description_is_refused(self) -> None:
        selected, inputs = self.tool.pictorial_gallery_selection()
        selected["comprehensive"].add("src/gpt/missing-gallery-description.png")
        with mock.patch.object(self.tool, "pictorial_gallery_selection", return_value=(selected, inputs)):
            with self.assertRaisesRegex(self.tool.ReleaseError, "no gallery description"):
                self.tool.pictorial_gallery_data()

    def test_every_card_has_checked_definition_and_accessible_image_data(self) -> None:
        for card in self.cards:
            self.assertGreater(card["width"], 0)
            self.assertGreater(card["height"], 0)
            self.assertRegex(card["sha256"], r"^[0-9a-f]{64}$")
            self.assertTrue(card["definitions"])
            for definition in card["definitions"]:
                self.assertTrue(definition["name"].strip())
                self.assertTrue(definition["definition"].strip())
        under_audit = [
            definition
            for card in self.cards
            for definition in card["definitions"]
            if definition["under_audit"]
        ]
        self.assertTrue(under_audit)
        self.assertTrue(
            all(
                definition["definition"]
                == self.tool.PICTORIAL_UNAVAILABLE_DEFINITION
                for definition in under_audit
            )
        )

    def test_admitted_assets_are_exact_bytes_and_bound_site_sources(self) -> None:
        bound = self.tool.pictorial_gallery_source_paths()
        for card in self.cards:
            data = card["source"].read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), card["sha256"])
            self.assertEqual(len(data), card["source"].stat().st_size)
            self.assertIn(card["source_relative"], bound)
        self.assertIn(
            self.tool.PICTORIAL_MANIFEST_RELATIVE.as_posix(),
            bound,
        )
        self.assertTrue(self.tool.pictorial_object_source_paths() <= bound)
        self.assertIn("scripts/_native_print_artwork.py", bound)
        self.assertIn("tools/render-sanctuary-dictionary", bound)
        self.assertIn("release/public-alpha/" + self.tool.PICTORIAL_SCRIPT_ASSET, bound)
        owner = self.tool.PICTORIAL_ROOT_RELATIVE.as_posix()
        for source in ("shared/schema/edition-selections.toml", "shared/generated-record-renderer.tex",
                       "shared/dictionary-format.tex", "comprehensive/main.tex",
                       "pontifical-ceremonies/main.tex"):
            self.assertIn(owner + "/" + source, bound)

    def test_expected_artifact_is_exhaustive_for_gallery_pngs(self) -> None:
        # Other publication/browser products have their own cache-context
        # integration tests. Exercise gallery asset admission without building
        # the entire corpus to ask about this single generated page.
        with ExitStack() as stack:
            for name in ("included_document_pages", "included_web_figures", "source_print_pages",
                         "publication_reader_routes", "web_data_files", "web_browser_pages"):
                stack.enter_context(mock.patch.object(self.tool, name, return_value={}))
            stack.enter_context(mock.patch.object(self.tool, "native_print_pages", return_value={"pages": {}}))
            stack.enter_context(mock.patch.object(self.tool, "native_tex_catalog", return_value={"assets": {}}))
            expected = self.tool.expected_artifact_files({}, {}, False, {})
        expected_pngs = {
            path
            for path in expected
            if path.startswith(self.tool.PICTORIAL_GALLERY_ASSET_ROOT.as_posix() + "/")
        }
        self.assertEqual(
            expected_pngs,
            {card["destination"] for card in self.cards},
        )
        self.assertEqual(len(expected_pngs), len(self.cards))
        self.assertIn(self.tool.PICTORIAL_GALLERY_OUTPUT, expected)
        self.assertIn(self.tool.PICTORIAL_SCRIPT_ASSET, expected)

    def test_tlm_shelf_gallery_link_resolves_to_generated_route(self) -> None:
        with mock.patch.object(self.tool, "web_data_manifest_path", return_value=REPOSITORY_ROOT):
            self.assertEqual(
                self.tool.source_to_output(
                    "library/traditional-latin-mass.md",
                    "library/traditional-latin-mass.html",
                    "sanctuary-picture-dictionary.html",
                    set(),
                ),
                "sanctuary-picture-dictionary.html",
            )

    def render_dictionary(self) -> str:
        with (mock.patch.object(self.tool, "pictorial_gallery_data", return_value=self.cards),
              mock.patch.object(self.tool, "native_print_pages", return_value={"readers": {}})):
            return self.tool.render_pictorial_gallery(False, {})

    def test_dictionary_is_one_semantic_table_with_compact_object_rows(self) -> None:
        rendered = self.render_dictionary()
        markup = DictionaryMarkup(rendered)
        tables = markup.find("table")
        self.assertEqual(len(tables), 1)
        table = tables[0]
        headers = [DictionaryMarkup.text(node) for node in markup.find("th")
                   if node["attrs"].get("scope") == "col"]
        self.assertEqual(headers[:3], ["Picture", "Object", "Grouping"])
        self.assertEqual(headers[3].replace(" ", "").casefold(), "identification/use")
        self.assertEqual(len(headers), 4)
        rows = self.tool.pictorial_dictionary_rows(self.cards)
        primary = markup.find("tr", "dictionary-row")
        detail = markup.find("tr", "dictionary-detail-row")
        self.assertEqual(len(primary), len(rows))
        self.assertEqual(len(detail), len(rows))
        self.assertTrue(all(any(parent is table for parent in row["parents"])
                            for row in primary + detail))
        for row in primary:
            cells = [node for node in markup.nodes if node["tag"] in {"td", "th"}
                     and node["parents"] and node["parents"][-1] is row]
            self.assertEqual(len(cells), 4)
            self.assertTrue(any(cell["tag"] == "th" and cell["attrs"].get("scope") == "row"
                                for cell in cells))
        for row in detail:
            cells = [node for node in markup.find("td")
                     if node["parents"] and node["parents"][-1] is row]
            self.assertEqual(len(cells), 1)
            self.assertEqual(cells[0]["attrs"].get("colspan"), "4")
            disclosure = [node for node in markup.find("details", "dictionary-details")
                          if any(parent is row for parent in node["parents"])]
            self.assertEqual(len(disclosure), 1)
            self.assertNotIn("open", disclosure[0]["attrs"])
        self.assertFalse(markup.find(css_class="gallery-card"))
        self.assertNotIn('id="objects-together"', rendered)
        self.assertNotIn("Objects within this image are not to common scale", rendered)
        self.assertFalse(markup.find(css_class="gallery-view"))
        self.assertNotIn("Return to", rendered)
        self.assertIn('href="../license.html"', rendered)
        self.assertIn('href="../third-party.html"', rendered)
        self.assertIn("Public Domain Rijksmuseum image", rendered)
        scripts = [node for node in markup.find("script")
                   if node["attrs"].get("src") == "../" + self.tool.PICTORIAL_SCRIPT_ASSET]
        self.assertEqual(len(scripts), 1)
        self.assertIn("defer", scripts[0]["attrs"])

    def test_table_definitions_and_image_expansions_have_unique_resolvable_targets(self) -> None:
        rendered = self.render_dictionary()
        markup = DictionaryMarkup(rendered)
        ids = [node["attrs"]["id"] for node in markup.nodes if "id" in node["attrs"]]
        self.assertEqual(len(ids), len(set(ids)))
        for node in markup.find("a"):
            href = node["attrs"].get("href", "")
            if href.startswith("#"):
                self.assertIn(href[1:], ids)
        objects = {definition["id"]: definition for card in self.cards for definition in card["definitions"]}
        paragraphs = Counter(DictionaryMarkup.text(node) for node in markup.find("p"))
        for object_id, definition in objects.items():
            self.assertEqual(ids.count(f"gallery-{object_id}"), 1)
            self.assertEqual(paragraphs[" ".join(definition["definition"].split())], 1, object_id)
        image_sources = {node["attrs"]["src"] for node in markup.find("img")}
        self.assertEqual(image_sources, {"../" + card["destination"] for card in self.cards})
        for card in self.cards:
            view_id = "view-" + Path(card["destination"]).stem
            toggles = [node for node in markup.find("a", "dictionary-image-toggle")
                       if node["attrs"].get("data-image") == view_id]
            self.assertEqual(len(toggles), 1, view_id)
            toggle = toggles[0]
            url = "../" + card["destination"]
            self.assertEqual(toggle["attrs"].get("href"), url, "no-JavaScript fallback must open the drawing")
            self.assertTrue(toggle["attrs"].get("aria-label"))
            self.assertIn(toggle["attrs"].get("data-detail"), ids)
            figures = [node for node in markup.find("figure") if node["attrs"].get("id") == view_id]
            self.assertEqual(len(figures), 1)
            figure = figures[0]
            self.assertTrue(any(parent["attrs"].get("id") == toggle["attrs"]["data-detail"]
                                for parent in figure["parents"]))
            panel = next(parent for parent in figure["parents"]
                         if parent["attrs"].get("id") == toggle["attrs"]["data-detail"])
            for pictured in card["definitions"]:
                # Opening a shared view must carry the other pictured objects'
                # qualifications, even when their full entries live elsewhere.
                for text in pictured["qualifications"] + pictured["handling"].get("warnings", []):
                    self.assertIn(" ".join(text.split()), DictionaryMarkup.text(panel))
            disclosures = [parent for parent in figure["parents"] if parent["tag"] == "details"]
            self.assertTrue(disclosures)
            self.assertTrue(all("open" not in node["attrs"] for node in disclosures))
            images = [node for node in markup.find("img") if node["attrs"].get("src") == url]
            self.assertEqual(len(images), 2, "one thumbnail and one expanded drawing")
            self.assertTrue(all(node["attrs"].get("alt") and node["attrs"].get("width")
                                and node["attrs"].get("height") for node in images))
            self.assertTrue(any(any(parent is toggle for parent in node["parents"]) for node in images))
            self.assertTrue(any(any(parent is figure for parent in node["parents"]) for node in images))
            for statement in card["rights"]:
                self.assertIn(" ".join(statement.split()), DictionaryMarkup.text(figure))

    def test_table_owns_objects_and_context_without_losing_or_repeating_images(self) -> None:
        rows = self.tool.pictorial_dictionary_rows(self.cards)
        objects = {definition["id"] for card in self.cards for definition in card["definitions"]}
        primary = {row["definition"]["id"]: row for row in rows}
        self.assertEqual(set(primary), objects - {"obj-book-marker", "obj-communion-rail"})
        occurrences = Counter(definition["id"] for row in rows
                              for definition in [row["definition"], *row["contexts"]])
        self.assertEqual(occurrences, Counter({object_id: 1 for object_id in objects}))
        self.assertEqual([item["id"] for item in primary["obj-altar-missal"]["contexts"]], ["obj-book-marker"])
        self.assertEqual([item["id"] for item in primary["obj-altar-candlestick"]["contexts"]], ["obj-communion-rail"])
        self.assertEqual(
            Counter(image["destination"] for row in rows for image in row["images"]),
            Counter(card["destination"] for card in self.cards),
        )
        for object_id in ("obj-altar-cruet", "obj-epistle-book"):
            self.assertEqual(len(primary[object_id]["images"]), 2)
        for filename, owner in (
            ("RPD-FIG-prepared-chalice-0001-formation-alpha.png", "obj-chalice"),
            ("RSD-cassock-surplice-worn-2026-11-05.png", "obj-cassock"),
            ("RPD-FIG-pontifical-0103-ring-over-right-glove-alpha-canonical.png", "obj-pontifical-gloves"),
        ):
            self.assertIn(filename, {Path(image["source_relative"]).name for image in primary[owner]["images"]})
        owned = {image["destination"]: row["definition"]["id"] for row in rows for image in row["images"]}
        for row in rows:
            for image in row["shared"]:
                self.assertIn(image["destination"], owned)
                self.assertNotEqual(owned[image["destination"]], row["definition"]["id"])
                self.assertIn(row["definition"]["id"], {item["id"] for item in image["definitions"]})
        self.assertTrue(primary["obj-pontifical-tunicle"]["images"] or primary["obj-pontifical-tunicle"]["shared"])
        self.assertEqual(rows, self.tool.pictorial_dictionary_rows(list(reversed(self.cards))))

    def test_table_order_follows_object_relationships_instead_of_alphabetical_names(self) -> None:
        rows = self.tool.pictorial_dictionary_rows(self.cards)
        positions = {row["definition"]["id"]: index for index, row in enumerate(rows)}
        self.assertEqual(rows[0]["definition"]["id"], "obj-altar")
        self.assertNotEqual([row["definition"]["name"] for row in rows],
                            sorted(row["definition"]["name"] for row in rows))
        for earlier, later in (("obj-altar-candle", "obj-altar-candlestick"),
                               ("obj-lavabo-basin", "obj-lavabo-towel"),
                               ("obj-amice", "obj-alb"), ("obj-alb", "obj-cincture"),
                               ("obj-pontifical-buskin", "obj-pontifical-sandal"),
                               ("obj-cassock", "obj-surplice")):
            self.assertLess(positions[earlier], positions[later])
        groups = [row["group_id"] for row in rows]
        for group in set(groups):
            indices = [index for index, value in enumerate(groups) if value == group]
            self.assertEqual(indices, list(range(min(indices), max(indices) + 1)))
        self.assertTrue(all(row["group"].strip() and row["group"] != row["group_id"] for row in rows))

    def test_table_refuses_undefined_organization_and_conflicting_identity(self) -> None:
        unknown = deepcopy(self.cards[0])
        unknown["definitions"][0]["id"] = "obj-unmapped-test-object"
        with self.assertRaises(self.tool.ReleaseError):
            self.tool.pictorial_dictionary_rows([unknown])
        conflicting = deepcopy(self.cards[0])
        conflicting["definitions"][0]["definition"] += " A contradictory definition."
        with self.assertRaises(self.tool.ReleaseError):
            self.tool.pictorial_dictionary_rows([*self.cards, conflicting])

    def test_contextual_identity_without_its_object_owner_is_refused(self) -> None:
        for object_id in ("obj-book-marker", "obj-communion-rail"):
            card = deepcopy(next(card for card in self.cards
                                 if object_id in {item["id"] for item in card["definitions"]}))
            card["definitions"] = [item for item in card["definitions"] if item["id"] == object_id]
            with self.subTest(object=object_id), self.assertRaises(self.tool.ReleaseError):
                self.tool.pictorial_dictionary_rows([card])

    def test_new_combined_view_requires_an_explicit_placement(self) -> None:
        objects = {definition["id"]: definition for card in self.cards for definition in card["definitions"]}
        unsupported = deepcopy(self.cards[0])
        unsupported["definitions"] = [objects["obj-altar"], objects["obj-chalice"]]
        with self.assertRaisesRegex(self.tool.ReleaseError, "view has no editorial placement"):
            self.tool.pictorial_dictionary_rows([unsupported])

    def test_dictionary_keeps_light_paper_and_monochrome_image_contrast(self) -> None:
        css = (
            REPOSITORY_ROOT / "release/public-alpha/assets/site.css"
        ).read_text(encoding="utf-8")
        self.assertNotIn("mix-blend-mode: screen", css)
        self.assertIn("color-scheme: only light", css)
        self.assertNotIn("prefers-color-scheme: dark", css)

    def test_asset_resolution_rejects_traversal_and_symlinks(self) -> None:
        with self.assertRaises(self.tool.ReleaseError):
            self.tool._resolve_pictorial_asset_path("../outside.png", "test asset")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dictionary = root / "dictionary"
            dictionary.mkdir()
            target = root / "target.png"
            target.write_bytes(b"png")
            (dictionary / "link.png").symlink_to(target)
            with (
                mock.patch.object(self.tool, "ROOT", root),
                mock.patch.object(self.tool, "PICTORIAL_ROOT", dictionary),
            ):
                with self.assertRaises(self.tool.ReleaseError):
                    self.tool._resolve_pictorial_asset_path("link.png", "test asset")


class PictorialObjectDetailsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tool = load_tool()

    def record(self, relative: str) -> dict:
        return tomllib.loads((REPOSITORY_ROOT / self.tool.PICTORIAL_OBJECTS_RELATIVE / relative).read_text())

    def render_record(self, record: dict) -> str:
        definition, under_audit = self.tool._checked_definition(record)
        details = self.tool._pictorial_object_details(record, definition, {})
        card = {
            "definitions": [{"id": record["id"], "name": record["preferred_english_name"], "latin": record["latin_headword"],
                             "category": record["categories"][0], "definition": definition,
                             "under_audit": under_audit, **details}],
            "views": {"isolated"}, "rights": set(), "scale_modes": {"not-to-common-scale"},
            "destination": "assets/pictorial-gallery/fixture.png", "width": 100, "height": 100,
            "source_relative": "src/gpt/fixture.png",
        }
        with (mock.patch.object(self.tool, "pictorial_gallery_data", return_value=[card]),
              mock.patch.object(self.tool, "native_print_pages", return_value={"readers": {}})):
            return self.tool.render_pictorial_gallery(False, {})

    def test_print_reader_keeps_its_own_assets_without_dictionary_injection(self) -> None:
        page = {"title": "Other print reader", "html": "<p>Print content</p>",
                "body_extra": '<script src="print-specific.js"></script>'}
        reader_body = '<script src="publication-reader.js"></script>'
        with (mock.patch.object(self.tool, "publication_reader_shell",
                                return_value=(page["html"], "", reader_body)),
              mock.patch.object(self.tool, "wrap_in_layout", return_value="<html>Print reader</html>") as wrap):
            rendered = self.tool.render_print_page("print/gpt/fixture.html", page, False, {})
        self.assertEqual(rendered, "<html>Print reader</html>")
        self.assertEqual(wrap.call_args.kwargs["body_extra"], page["body_extra"] + reader_body)
        self.assertNotIn("dictionary", wrap.call_args.kwargs["body_extra"])

    def test_reservation_and_unveiled_view_qualifications_survive(self) -> None:
        for relative, qualifier in (
            ("ciborium.toml", "covered with a white silk veil"),
            ("altar-appointments/tabernacle.toml", "an unveiled identification view does not show the complete prepared arrangement"),
        ):
            with self.subTest(record=relative):
                record = self.record(relative)
                rendered = self.render_record(record)
                self.assertIn(qualifier, rendered)
                self.assertIn("recognizes only", rendered)
                self.assertIn("Ordinary handler:", rendered)
                self.assertNotIn("Objects within this image are not to common scale", rendered)
                self.assertRegex(rendered, r"Canon 12(?:69|70)")
                self.assertIn("Missale Romanum", rendered)
                self.assertIn("1962", rendered)
                self.assertNotIn("src-ciborium-", rendered)
                self.assertNotIn("src-tabernacle-", rendered)
                for warning in record["handling"]["warnings"]:
                    self.assertIn(html.escape(warning), rendered)
                self.assertIn("The Ceremonies of the Roman Rite Described, seventh edition", rendered)
                self.assertIn("1943", rendered)

    def test_altar_construction_and_preparation_are_not_inferred_from_the_picture(self) -> None:
        rendered = self.render_record(self.record("altar-appointments/altar.toml"))
        self.assertIn("an altar stone may instead rest in a supporting table or framework", rendered)
        self.assertIn("a blessed antimension is an alternative only by Apostolic indult", rendered)
        self.assertIn("three blessed cloths", rendered)
        self.assertIn("525–529", rendered)

    def test_unverified_claim_and_unsupported_audience_note_are_not_projected(self) -> None:
        record = self.record("ciborium.toml")
        record["claims"].append({"id": "unverified", "kind": "appearance", "text": "Invented form",
                                 "evidence_state": "unverified-lead", "source_ids": []})
        record["audience_note"].append({"audience": "sacristan", "text": "Invented preparation",
                                        "claim_ids": ["unverified"]})
        rendered = self.render_record(record)
        self.assertNotIn("Invented form", rendered)
        self.assertNotIn("Invented preparation", rendered)

    def test_source_bibliography_and_locus_use_bound_metadata(self) -> None:
        record = self.record("ciborium.toml")
        details = self.tool._pictorial_object_details(record, record["claims"][0]["text"], {})
        citation = next(item for item in details["citations"] if "Missale Romanum" in item["label"])
        self.assertIn("1962", citation["label"])
        self.assertEqual(citation["locus"], record["sources"][0]["locus"])
        self.assertTrue(any(path.endswith("vatican-typica-1962/edition.toml") for path in citation["inputs"]))
        fallback = self.tool._pictorial_source_reference({"binding": "legacy.exact-reference", "locus": "p. 4"}, {})
        self.assertEqual(fallback, {"label": "legacy.exact-reference", "locus": "p. 4", "inputs": set()})


if __name__ == "__main__":
    unittest.main()
