"""Complete dictionary print products preserve their canonical source owners."""
from __future__ import annotations

import hashlib
import html
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _web_print_dictionaries as dictionaries


class Rendered(HTMLParser):
    def __init__(self, value):
        super().__init__(convert_charrefs=True)
        self.ids, self.units, self.images, self.text, self.records = [], [], [], [], []
        self.feed(value)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if "data-print-unit" in attrs:
            self.units.append(attrs["data-print-unit"])
        if "data-source-record" in attrs:
            self.records.append(attrs["data-source-record"])
        if tag == "img":
            self.images.append(attrs)

    def handle_data(self, value):
        self.text.append(value)

    @property
    def plain(self):
        return " ".join("".join(self.text).split())


class DictionaryPrintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = dictionaries.Source(ROOT)
        cls.eligibility_before = {leaf: (cls.source.owner / leaf / "web-edition.toml").read_bytes()
                                  for leaf in dictionaries.LEAVES.values()}
        cls.products = {edition: dictionaries.render_dictionary(
            ROOT, "gpt", "publication:gpt/" + str(dictionaries.OWNER.relative_to("src/gpt") / leaf),
            _source=cls.source) for edition, leaf in dictionaries.LEAVES.items()}

    def owner_output(self, edition_id):
        """Expected coverage comes directly from the owning generator/data."""
        source = self.source
        edition = next(item for item in source.selections["editions"] if item["id"] == edition_id)
        gen = source.generator
        selected = [record for record in source.records.values()
                    if gen.alpha_selected(record, edition, source.alpha_assets)
                    and record["id"] not in gen.PUBLIC_RENDER_HOLD_IDS]
        selected.sort(key=lambda item: (item.get("sort_name", item["preferred_english_name"]).casefold(), item["id"]))
        generated = "\n".join(gen.dense_edition_tex(selected, edition, source.art_owners))
        order = re.findall(r"\\RSDObjectRecord\{([^}]+)\}", generated)
        return edition, selected, generated, order

    def test_all_six_exact_record_plate_and_asset_counts(self):
        expected = {"ed-comprehensive": (45, 10, 48), "ed-altar-server": (44, 9, 48),
                    "ed-sacristan": (45, 10, 49), "ed-mc-trainer": (45, 8, 49),
                    "ed-general-reader": (43, 9, 47), "ed-pontifical": (56, 14, 59)}
        for edition, counts in expected.items():
            with self.subTest(edition=edition):
                product = self.products[edition]
                self.assertEqual((product["record_count"], product["plate_count"], len(product["assets"])), counts)
                self.assertEqual(product["print_type"], "plates")
                self.assertTrue(product["output_id"].startswith("publication:gpt/liturgy/"))

    def test_each_record_and_plate_has_an_independent_ordered_owner_unit(self):
        for edition_id, product in self.products.items():
            with self.subTest(edition=edition_id):
                _, selected, generated, record_order = self.owner_output(edition_id)
                rendered = Rendered(product["parts"][0]["html"])
                expected_units = []
                starts = list(re.finditer(r"\\(RSD[A-Za-z]+PlateStart)\b", generated))
                for index, match in enumerate(starts):
                    args, begin = dictionaries.arguments(generated, match.end(), 2)
                    end = starts[index + 1].start() if index + 1 < len(starts) else len(generated)
                    plate_id = edition_id + "-" + dictionaries.slug(args[0]) + "-" + args[1]
                    expected_units.append(plate_id)
                    expected_units.extend(re.findall(r"\\RSDObjectRecord\{([^}]+)\}", generated[begin:end]))
                self.assertEqual(rendered.records, record_order)
                self.assertEqual(set(rendered.records), {record["id"] for record in selected})
                self.assertEqual(rendered.units, expected_units)
                self.assertEqual([unit["id"] for unit in product["expected_units"]], expected_units)
                record_units = [unit for unit in product["expected_units"] if unit["id"].startswith("obj-")]
                self.assertEqual(len(record_units), len(selected))
                for unit in record_units:
                    self.assertEqual(unit["occurrence"], 1)
                    self.assertEqual(unit["source"], self.source.record_paths[unit["id"]])
                self.assertEqual(product["coverage_result"]["status"], "pass")
                self.assertEqual(product["coverage_result"]["expected_units"], product["expected_units"])

    def test_required_assets_are_exact_visible_owner_artwork_and_cover_assets(self):
        for edition_id, product in self.products.items():
            with self.subTest(edition=edition_id):
                _, selected, generated, _ = self.owner_output(edition_id)
                expected = set()
                for record in selected:
                    position = generated.index(r"\RSDObjectRecord{" + record["id"] + "}")
                    previous = generated.rfind(r"\RSDEndObjectRecord", 0, position)
                    flags = generated[previous + len(r"\RSDEndObjectRecord") if previous >= 0 else 0:position]
                    limit = 1 if re.search(r"\\RSD(?:Story(?:Tall)?Hero|TallCard)Next\b", flags) else 2
                    art = [item for item in record["artwork"] if item["id"] not in self.source.generator.PUBLIC_ARTWORK_HOLD_IDS]
                    owned = any(self.source.art_owners[item["id"]] == record["id"] for item in art)
                    fallback = art[0]["id"] if art and not owned else None
                    visible = [item["asset"] for item in art if self.source.art_owners[item["id"]] == record["id"] or item["id"] == fallback]
                    expected.update(str(dictionaries.OWNER / self.source.generator.canonical_asset_path(value))
                                    for value in list(dict.fromkeys(visible))[:limit])
                title = dictionaries.definition(self.source.format, "DictionaryTitle")
                prefix = str(dictionaries.OWNER.relative_to("src/gpt")) + "/"
                expected.update(str(dictionaries.OWNER / args[0].strip()[len(prefix):])
                                for args, _, _ in dictionaries.calls(title, "includegraphics", 1))
                if edition_id == "ed-comprehensive":
                    main = dictionaries.clean_tex((self.source.owner / "comprehensive/main.tex").read_text())
                    opening = dictionaries.definition(main, "RSDOpeningComposition")
                    expected.update(str(dictionaries.OWNER / args[0].strip()[len(prefix):])
                                    for args, _, _ in dictionaries.calls(opening, "includegraphics", 1))
                self.assertEqual({asset["source"] for asset in product["assets"]}, expected)
                declared = {asset["id"]: asset for asset in product["assets"]}
                images = Rendered(product["parts"][0]["html"]).images
                self.assertEqual({image["data-print-asset"] for image in images}, set(declared))
                for image in images:
                    self.assertTrue(image["alt"])
                    self.assertEqual(image["src"], declared[image["data-print-asset"]]["href"])
                for asset in declared.values():
                    self.assertEqual(asset["sha256"], hashlib.sha256((ROOT / asset["source"]).read_bytes()).hexdigest())
                    self.assertEqual(asset["mime"], "image/png")

    def test_existing_record_and_artwork_holds_are_preserved(self):
        gen = self.source.generator
        held = set(gen.PUBLIC_RENDER_HOLD_IDS) | {
            key for key, record in self.source.records.items()
            if gen.alpha_gate_failure(record, self.source.alpha_assets) is not None}
        held_art_paths = {str(dictionaries.OWNER / gen.canonical_asset_path(art["asset"]))
                          for record in self.source.records.values() for art in record["artwork"]
                          if art["id"] in gen.PUBLIC_ARTWORK_HOLD_IDS}
        self.assertTrue(held)
        self.assertTrue(held_art_paths)
        for product in self.products.values():
            self.assertFalse(held & set(Rendered(product["parts"][0]["html"]).records))
            self.assertFalse(held_art_paths & {asset["source"] for asset in product["assets"]})

    def test_exact_visible_claim_audience_reference_and_handling_text(self):
        for edition_id, product in self.products.items():
            edition, selected, _, _ = self.owner_output(edition_id)
            plain = Rendered(product["parts"][0]["html"]).plain
            for record in selected:
                with self.subTest(edition=edition_id, record=record["id"]):
                    fields = {}
                    for claim in record["claims"]:
                        if claim["evidence_state"] == "editorial-proposal":
                            continue
                        if claim["kind"] in {"identity", "symbolism"}:
                            fields[claim["kind"]] = claim["text"]
                        elif claim["kind"] in {"liturgical-use", "ceremonial-presence"}:
                            fields["use"] = claim["text"]
                    for value in fields.values():
                        self.assertIn(" ".join(value.split()), plain)
                    notes = [note["text"] for note in record.get("audience_note", []) if note["audience"] == edition["audience"]]
                    if notes:
                        self.assertIn(" ".join(notes[-1].split()), plain)
                    for source in record.get("sources", []):
                        self.assertIn(source["binding"], plain)
                        self.assertIn(" ".join(source["locus"].split()), plain)
                    for value in record.get("handling", {}).get("warnings", []):
                        self.assertIn(" ".join(value.split()), plain)

    def test_source_title_captions_scope_revision_rights_and_under_audit_boundary(self):
        for product in self.products.values():
            text = html.unescape(product["parts"][0]["html"])
            for caption in ("One cruet", "Wine-and-water pair", "Representative, not universal.",
                            "not the family's complete inventory", "Reuse and rights.", "Last revised (UTC):", "under audit"):
                self.assertIn(caption, text, caption)
            self.assertEqual(product["reader_eligibility"], "ineligible")
            self.assertEqual(product["print_admission"], "under-audit")
        for leaf, original in self.eligibility_before.items():
            self.assertEqual((self.source.owner / leaf / "web-edition.toml").read_bytes(), original)

    def test_common_normalization_and_both_text_and_structure_pins(self):
        from _web_print_common import normalize_html, part_statistics
        for product in self.products.values():
            for part in product["parts"]:
                self.assertEqual(normalize_html(part["html"]), part["html"])
                statistics = part_statistics(part["html"], part_id=part["id"], selectors=tuple(part["counts"]))
                for key in ("text_sha256", "structure_sha256", "expected_ids", "units", "counts"):
                    self.assertEqual(part[key], statistics[key])
                self.assertEqual(part["html_sha256"], hashlib.sha256(part["html"].encode("utf-8")).hexdigest())
                self.assertEqual(product["print_descriptor"]["parts"][0]["html_sha256"], part["html_sha256"])
                self.assertLess(len(part["html"].encode()), 750_000)
                self.assertNotIn(' style="', part["html"])
            self.assertNotIn("css", product)
            self.assertEqual(product["print_descriptor"]["coverage_result"], product["coverage_result"])

    def test_full_owner_proof_compacts_without_publishing_the_audit_ledger(self):
        from _web_print_common import compact_descriptor
        for product in self.products.values():
            public = compact_descriptor(product["print_descriptor"])
            self.assertEqual(public["id"], product["output_id"])
            self.assertEqual(public["unit_inventory"]["count"], len(product["expected_units"]))
            self.assertNotIn("expected_units", public)
            self.assertNotIn("expected_units", public["coverage_result"])
            self.assertFalse(any("source" in asset or "target" in asset for asset in public["assets"]))

    def test_canonical_field_context_is_selected_before_rendering_and_bound_to_audit(self):
        for edition, product in self.products.items():
            with self.subTest(edition=edition):
                coverage = product["coverage_result"]
                context = coverage["expected_context"]
                self.assertEqual(context["schema"], "triptych-dictionary-context/v1")
                self.assertEqual(coverage["context_sha256"], dictionaries.json_digest(context))
                self.assertEqual(product["selection"]["context_sha256"], coverage["context_sha256"])
                self.assertEqual(product["selection_digest"], dictionaries.json_digest(product["selection"]))
                records = [record for frame in context["frames"] for record in frame.get("records", [])]
                self.assertEqual([record["id"] for record in records], self.owner_output(edition)[3])
                self.assertEqual(context["assets"], product["assets"])
                public = __import__("_web_print_common").compact_descriptor(product["print_descriptor"])
                self.assertNotIn("expected_context", public["coverage_result"])

    def test_pre_pin_record_omissions_and_changed_context_refuse_before_sealing(self):
        original = dictionaries._record_html
        mutations = {
            "review description and qualification removal": lambda value: re.sub(
                r'<p class="object-description">.*?</p>|<aside class="canonical-qualifications">.*?</aside>', "", value, flags=re.S),
            "Latin": lambda value: re.sub(r'(<p class="latin">).*?(</p>)', r'\1Changed Latin\2', value, flags=re.S),
            "audience": lambda value: re.sub(r'(<p class="audience-note">).*?(</p>)', r'\1Changed audience\2', value, flags=re.S),
            "reference target": lambda value: value.replace('href="#source-', 'href="#detached-'),
            "caption": lambda value: value.replace('One cruet</figcaption>', 'Changed caption</figcaption>'),
            "artwork alternative": lambda value: re.sub(r'alt="[^"]*"', 'alt="Changed alternative"', value),
            "artwork mapping": lambda value: value.replace('data-print-asset="asset-', 'data-print-asset="wrong-'),
            "concealed description": lambda value: value.replace('class="object-description"', 'class="object-description" hidden'),
        }
        for name, mutate in mutations.items():
            changes = []

            def tamper(*args):
                before = original(*args)
                after = mutate(before)
                if before != after: changes.append(True)
                return after

            with self.subTest(attack=name), mock.patch.object(dictionaries, "_record_html", tamper), \
                    mock.patch("_web_print_common.part_statistics", side_effect=AssertionError("sealing happened before source proof")):
                with self.assertRaisesRegex(ValueError, "canonical context"):
                    dictionaries.render_dictionary(ROOT, "gpt", "general-reader", _source=self.source)
                self.assertTrue(changes, "attack must actually alter selected source content")

    def test_pre_pin_native_title_opening_plate_terminal_and_rights_changes_refuse(self):
        original = dictionaries.TeXProse.render
        # Mutate the rendered prose, leaving its canonical native input intact.
        # The expected model must not call this renderer to establish truth.
        mutations = {
            "title": ("The Illustrated Dictionary of the Roman Sanctuary", "Changed dictionary title"),
            "subtitle": ("Objects, Vestments, Linens, Books, Furnishings, and Insignia", "Changed subtitle"),
            "edition": ("Comprehensive 1962 Roman Rite edition", "Changed edition"),
            "opening": ("One sanctuary, seen whole", "Changed witness"),
            "plate header": ("Visual field", "Changed field"),
            "plate footer": ("Compare form and use", "Changed comparison"),
            "terminal": ("Representative, not universal.", "Changed reader boundary"),
            "rights": ("Reuse and rights.", "Changed rights"),
            "license link": ("https://creativecommons.org/licenses/by/4.0/", "https://example.invalid/license"),
            "revision": ("Last revised (UTC):", "Changed revision:"),
        }
        for name, (needle, replacement) in mutations.items():
            changes = []

            def tamper(renderer, native):
                before = original(renderer, native)
                after = before.replace(needle, replacement)
                if before != after: changes.append(True)
                return after

            with self.subTest(attack=name), mock.patch.object(dictionaries.TeXProse, "render", tamper), \
                    mock.patch("_web_print_common.part_statistics", side_effect=AssertionError("sealing happened before source proof")):
                with self.assertRaisesRegex(ValueError, "canonical context"):
                    dictionaries.render_dictionary(ROOT, "gpt", "comprehensive", _source=self.source)
                self.assertTrue(changes, "attack must actually alter selected native prose")

    def test_pre_pin_source_apparatus_changes_refuse(self):
        original = dictionaries._record_html

        def tamper(source, edition, obj, assets, reference_rows):
            rendered = original(source, edition, obj, assets, reference_rows)
            if reference_rows:
                key, object_id, item = reference_rows[-1]
                reference_rows[-1] = (key, object_id, dict(item, note="Changed canonical source note"))
            return rendered

        with mock.patch.object(dictionaries, "_record_html", tamper), \
                mock.patch("_web_print_common.part_statistics", side_effect=AssertionError("sealing happened before source proof")):
            with self.assertRaisesRegex(ValueError, "canonical context"):
                dictionaries.render_dictionary(ROOT, "gpt", "general-reader", _source=self.source)

    def test_native_artwork_context_order_is_checked_before_pins(self):
        from _web_print_common import normalize_html

        def tamper(value):
            value = normalize_html(value)
            match = re.search(r'<header class="dictionary-title">(.*?)</header>', value, re.S)
            title = match[1]
            figures = re.findall(r'<figure>.*?</figure>', title, re.S)
            self.assertEqual(len(figures), 3)
            changed = re.sub(r'<figure>.*?</figure>', "", title, flags=re.S) + "".join(figures)
            # All image attrs/order and all prose remain identical. Their
            # positions beside the native cover context no longer agree.
            return value[:match.start(1)] + changed + value[match.end(1):]

        with mock.patch("_web_print_common.normalize_html", tamper), \
                mock.patch("_web_print_common.part_statistics", side_effect=AssertionError("sealing happened before source proof")):
            with self.assertRaisesRegex(ValueError, "canonical context"):
                dictionaries.render_dictionary(ROOT, "gpt", "general-reader", _source=self.source)

    def test_missing_required_artwork_refuses_the_complete_output(self):
        target = ROOT / self.products["ed-altar-server"]["assets"][0]["source"]
        original = Path.is_file
        with mock.patch.object(Path, "is_file", lambda path: False if path == target else original(path)):
            with self.assertRaisesRegex(ValueError, "required canonical artwork missing"):
                dictionaries.render_dictionary(ROOT, "gpt", "altar-server", _source=self.source)

    def test_unrecorded_changed_artwork_is_not_an_automatic_admission(self):
        source = dictionaries.Source(ROOT)
        required = self.products["ed-altar-server"]["assets"][0]["source"]
        relative = str(Path(required).relative_to(dictionaries.OWNER))
        source.expected_asset_hashes[relative] = "0" * 64
        with self.assertRaisesRegex(ValueError, "artwork identity changed"):
            source.asset(relative, alt="required source image")

    def test_asset_url_mapping_preserves_source_identity_and_source_paths(self):
        product = dictionaries.render_dictionary(ROOT, "gpt", "altar-server", _source=self.source,
                                                 asset_href=lambda value: "../../../" + value)
        original = self.products["ed-altar-server"]
        self.assertEqual(product["source_digest"], original["source_digest"])
        self.assertEqual(product["expected_units"], original["expected_units"])
        self.assertTrue(all(asset["href"].startswith("../../../assets/") for asset in product["assets"]))
        self.assertEqual({asset["source"] for asset in product["assets"]}, {asset["source"] for asset in original["assets"]})

    def test_unknown_output_provider_and_new_print_construct_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "unknown dictionary print output"):
            dictionaries.render_dictionary(ROOT, "gpt", "not-a-dictionary")
        with self.assertRaisesRegex(ValueError, "no canonical sanctuary dictionary owner"):
            dictionaries.render_dictionary(ROOT, "claude", "comprehensive")
        with self.assertRaisesRegex(ValueError, "another repository root"):
            dictionaries.render_dictionary(ROOT / ".scratch/not-the-owner", "gpt", "altar-server", _source=self.source)
        converter = dictionaries.TeXProse(self.source, revision="2026-01-01T00:00:00Z", required_assets={})
        with self.assertRaisesRegex(ValueError, "unsupported canonical print-prose command"):
            converter.render(r"\UnreviewedNewCommand{content}")

    def test_print_source_loading_never_reads_pdf_bytes(self):
        original = Path.read_bytes

        def source_only(path):
            self.assertNotEqual(path.suffix.lower(), ".pdf", str(path))
            return original(path)

        with mock.patch.object(Path, "read_bytes", source_only):
            product = dictionaries.render_dictionary(ROOT, "gpt", "general-reader")
        self.assertEqual(product["record_count"], 43)


if __name__ == "__main__":
    unittest.main()
