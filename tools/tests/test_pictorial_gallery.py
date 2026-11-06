from __future__ import annotations

import hashlib
import html
from collections import Counter
from contextlib import ExitStack
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

    def test_gallery_markup_is_semantic_accessible_and_has_no_backlink(self) -> None:
        with mock.patch.object(self.tool, "native_print_pages", return_value={"readers": {}}):
            rendered = self.tool.render_pictorial_gallery(False, {})
        entries, compositions = self.tool.pictorial_gallery_entries(self.cards)
        self.assertEqual(rendered.count('class="gallery-card"'), len(entries) + len(compositions))
        self.assertEqual(rendered.count('loading="lazy"'), len(self.cards))
        self.assertEqual(rendered.count("<figure"), len(self.cards))
        self.assertEqual(rendered.count("<figcaption>"), len(self.cards))
        self.assertNotIn("Return to", rendered)
        self.assertIn("Definitions are drawn only from verified claims", rendered)
        self.assertIn('href="../license.html"', rendered)
        self.assertIn('href="../third-party.html"', rendered)
        self.assertIn("Each image follows its tracked artwork audit", rendered)
        self.assertIn("Public Domain Rijksmuseum image", rendered)
        self.assertIn("sizes across separate images are not a common scale", rendered)
        self.assertIn("<summary>Use and sources</summary>", rendered)
        self.assertIn('id="objects-together"', rendered)
        objects = {definition["id"]: definition for card in self.cards for definition in card["definitions"]}
        self.assertEqual(rendered.count('class="gallery-definition"'), len(objects))
        for object_id, definition in objects.items():
            self.assertEqual(rendered.count(f'id="gallery-{object_id}"'), 1)
            # A repeated depiction may repeat its immediate warnings, but not
            # the object's complete definition or its use/source apparatus.
            if not definition["under_audit"]:
                self.assertEqual(rendered.count(f'<p>{html.escape(definition["definition"])}</p>'), 1, object_id)
        for group in entries + compositions:
            for definition in group["related"]:
                self.assertIn(f'href="#gallery-{definition["id"]}"', rendered)

    def test_object_entries_group_alternates_without_absorbing_ensembles(self) -> None:
        entries, compositions = self.tool.pictorial_gallery_entries(self.cards)
        objects = {definition["id"] for card in self.cards for definition in card["definitions"]}
        occurrences = Counter(definition["id"] for entry in entries for definition in entry["definitions"])
        self.assertEqual(occurrences, Counter({object_id: 1 for object_id in objects}))
        self.assertEqual(
            Counter(image["destination"] for entry in entries + compositions for image in entry["images"]),
            Counter(card["destination"] for card in self.cards),
        )
        for name in ("Altar cruet", "Epistle book"):
            entry = next(entry for entry in entries if entry["definitions"][0]["name"] == name)
            self.assertEqual(len(entry["images"]), 2)
            self.assertEqual(len(entry["definitions"]), 1)
            self.assertIn("isolated", entry["images"][0]["views"])
        for filename, names in (
            ("RPD-FIG-prepared-chalice-0001-formation-alpha.png",
             {"Burse", "Chalice", "Chalice pall", "Chalice veil", "Corporal", "Paten", "Purificator"}),
            ("RSD-cassock-surplice-worn-2026-11-05.png", {"Cassock", "Surplice"}),
            ("RPD-FIG-pontifical-0103-ring-over-right-glove-alpha-canonical.png",
             {"Pontifical gloves", "Pontifical ring"}),
        ):
            group = next(group for group in compositions if any(
                Path(image["source_relative"]).name == filename for image in group["images"]))
            self.assertFalse(group["definitions"])
            self.assertEqual({definition["name"] for definition in group["related"]}, names)
        # Input order must not decide where an object's entry lives.
        reverse_entries, reverse_compositions = self.tool.pictorial_gallery_entries(list(reversed(self.cards)))
        self.assertEqual((entries, compositions), (reverse_entries, reverse_compositions))

    def test_gallery_css_blends_image_boundaries_on_the_light_paper(self) -> None:
        css = (
            REPOSITORY_ROOT / "release/public-alpha/assets/site.css"
        ).read_text(encoding="utf-8")
        self.assertIn("mix-blend-mode: multiply", css)
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
        }
        with (mock.patch.object(self.tool, "pictorial_gallery_data", return_value=[card]),
              mock.patch.object(self.tool, "native_print_pages", return_value={"readers": {}})):
            return self.tool.render_pictorial_gallery(False, {})

    def test_reservation_and_unveiled_view_qualifications_survive(self) -> None:
        for relative, qualifier in (
            ("ciborium.toml", "covered with a white silk veil"),
            ("altar-appointments/tabernacle.toml", "an unveiled identification view does not show the complete prepared arrangement"),
        ):
            with self.subTest(record=relative):
                record = self.record(relative)
                rendered = self.render_record(record)
                self.assertIn(qualifier, rendered.split("<details>")[0])
                self.assertIn("recognizes only", rendered)
                self.assertIn("Ordinary handler:", rendered)
                self.assertIn("Objects within this image are not to common scale", rendered)
                self.assertRegex(rendered, r"Canon 12(?:69|70)")
                self.assertIn("Missale Romanum", rendered)
                self.assertIn("1962", rendered)
                self.assertNotIn("src-ciborium-", rendered)
                self.assertNotIn("src-tabernacle-", rendered)
                for warning in record["handling"]["warnings"]:
                    self.assertIn(html.escape(warning), rendered.split("<details>")[0])
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
