"""Source-selected server products; SVG-cache validity is tested by its owner.

The metadata resolver fixture deliberately carries no SVG body or visual
acceptance: these tests exercise canonical text/order and the injection seam.
A separate held-asset integration check covers the actual vector delivery.
"""
from __future__ import annotations
from collections import Counter
import copy
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import _web_print_server as server


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []

    def handle_data(self, value):
        self.values.append(value)


def words(value):
    parser = Text()
    parser.feed(value)
    return " ".join(" ".join(parser.values).split())


def metadata_asset(root, variant, macro):
    """Source metadata only; no synthetic SVG or claimed visual proof."""
    source = root / "src/gpt" / server.BASE / "shared" / (
        "sung-mass-diagrams.tex" if variant == "sung" else "low-mass-diagrams.tex")
    return dict(id=variant + ":" + macro, src="web-print-assets/" + variant + "-" + macro + ".svg",
                sha256="a" * 64, bytes=1,
                source_inputs={source.relative_to(root).as_posix(): server.sha(source.read_bytes())},
                includes_caption=variant == "sung" and macro != "CommunionPatenSafetyDiagram")


@unittest.skipUnless(shutil.which("pandoc"), "pinned Pandoc is required")
class ServerProducts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.products = {}
        read_bytes = Path.read_bytes
        read_text = Path.read_text
        run = subprocess.run

        def guarded_bytes(path):
            if path.suffix.lower() in {".pdf", ".dvi"}:
                raise AssertionError("normal source generation consumed a PDF or DVI")
            return read_bytes(path)

        def guarded_text(path, *args, **kwargs):
            if path.suffix.lower() in {".pdf", ".dvi"}:
                raise AssertionError("normal source generation consumed a PDF or DVI")
            return read_text(path, *args, **kwargs)

        def guarded_run(argv, *args, **kwargs):
            if Path(argv[0]).name != "pandoc":
                raise AssertionError("normal source generation invoked a non-Pandoc subprocess: " + str(argv[0]))
            return run(argv, *args, **kwargs)

        with (patch.object(Path, "read_bytes", guarded_bytes),
              patch.object(Path, "read_text", guarded_text),
              patch.object(Path, "write_bytes", side_effect=AssertionError("adapter wrote output")),
              patch.object(Path, "write_text", side_effect=AssertionError("adapter wrote output")),
              patch.object(Path, "mkdir", side_effect=AssertionError("adapter created output")),
              patch.object(server.subprocess, "run", guarded_run)):
            for leaf in server.LEAVES:
                cls.products[leaf] = server.render_server_document(
                    ROOT, "gpt", server.BASE + "/" + leaf, asset_resolver=metadata_asset)

    def test_all_seven_source_products_have_exact_ordered_coverage(self):
        self.assertEqual(sum(len(p["expected_units"]) for p in self.products.values()), 497)
        images = 0
        asset_ids = set()
        for leaf, product in self.products.items():
            with self.subTest(leaf=leaf):
                self.assertEqual(product["id"], "publication:gpt/" + server.BASE + "/" + leaf)
                self.assertEqual(product["coverage_result"]["status"], "pass")
                self.assertEqual(product["render_toolchain"]["pandoc_binary_sha256"], "870b811354a230a1864dd2b50dec3b850a981926ff4659ae460aea96ab6b8d28")
                self.assertEqual(product["coverage_result"]["expected_units"], product["expected_units"])
                self.assertEqual(product["coverage_result"]["source_digest"], product["source_digest"])
                self.assertEqual(product["coverage_result"]["selection_digest"], product["selection_digest"])
                self.assertEqual(product["coverage_result"]["literal_coverage"]["status"], "pass")
                self.assertFalse(product["coverage_result"]["editorial_review"])
                actual = re.findall(r'data-unit-id="([^"]+)"', "".join(p["html"] for p in product["parts"]))
                self.assertEqual(actual, [unit["id"] for unit in product["expected_units"]])
                self.assertEqual(actual, product["expected_print_units"])
                self.assertEqual(len(actual), len(set(actual)))
                self.assertTrue(all(unit["source"] in product["sources"] for unit in product["expected_units"]))
                self.assertTrue(all(len(part["html"].encode()) < 750_000 for part in product["parts"]))
                self.assertTrue(all(part["html_sha256"] == server.sha(part["html"]) for part in product["parts"]))
                self.assertNotIn("SERVERPRINTBLOCK", "".join(part["html"] for part in product["parts"]))
                images += sum(part["html"].count("<img ") for part in product["parts"])
                asset_ids.update(asset["id"] for asset in product["assets"])
        self.assertEqual(images, 42)
        self.assertEqual(len(asset_ids), 39)

    def test_every_card_face_and_empty_slot_remain_in_mirrored_source_order(self):
        for leaf, faces, sheets in (("01-low-mass-flash-cards", 44, 6),
                                    ("02-missa-cantata-cue-cards", 72, 12),
                                    ("03-solemn-mass-cue-cards", 72, 12)):
            product = self.products[leaf]
            deck = [p for p in product["parts"] if p["kind"] == "card-sheet"]
            self.assertEqual(len(deck), sheets)
            self.assertEqual(sum(u["kind"] == "card-face" for u in product["units"]), faces)
            self.assertEqual(product["parts"][0]["kind"], "card-sheet")
            for i in range(0, len(deck), 2):
                front, back = deck[i:i + 2]
                ids = front["face_ids"]
                self.assertEqual(back["face_ids"], [v for j in range(0, len(ids), 2) for v in ids[j:j + 2][::-1]])
                self.assertEqual((front["side"], back["side"]), ("front", "back"))
        low = self.products["01-low-mass-flash-cards"]
        self.assertEqual(sum(part["html"].count('class="face blank"') for part in low["parts"]), 4)

    def test_source_duplex_metadata_and_canonical_terminal_conflicts_are_preserved(self):
        low = self.products["01-low-mass-flash-cards"]
        instructions = [u for u in low["units"] if u["kind"] == "duplex-instruction"]
        self.assertEqual([u["sheet"] for u in instructions], [2, 3, 4, 5, 6])
        self.assertEqual([words(u["html"]) for u in instructions], [
            "BACKS · LONG-EDGE DUPLEX", "FRONTS · PRINT AT 100%", "BACKS · LONG-EDGE DUPLEX",
            "FRONTS · PRINT AT 100%", "BACKS · LONG-EDGE DUPLEX"])
        for leaf in ("01-low-mass-flash-cards", "02-missa-cantata-cue-cards"):
            p = self.products[leaf]
            self.assertEqual(p["parts"][-1]["kind"], "apparatus")
            self.assertIn("About This Card Companion", words(p["parts"][-1]["html"]))
            self.assertTrue(p["coverage_result"]["gaps"])
        self.assertEqual(sum(u["kind"] == "revision-rights" for p in self.products.values() for u in p["units"]), 3)
        self.assertEqual(sum(u["kind"] == "apparatus" for p in self.products.values() for u in p["units"]), 2)

    def test_child_and_trainer_main_lanes_and_actions_share_the_same_source(self):
        child = self.products["01-low-mass"]["parts"][1:]
        trainer = self.products["01-low-mass-trainer-manual"]["parts"][1:]
        self.assertEqual(len(child), len(trainer))
        for a, b in zip(child, trainer):
            self.assertEqual(a["canonical_action_ids"], b["canonical_action_ids"])
            child_text = a["html"].split("</h2>", 1)[1].removesuffix("</section>")
            trainer_text = b["html"].split("</aside><div>", 1)[1].removesuffix("</div></div></section>")
            normalize = lambda text: re.sub(r"Last revised \(UTC\): \S+", "REVISION", words(text))
            self.assertEqual(normalize(child_text), normalize(trainer_text))
        for leaf, actions in (("01-low-mass", 43), ("01-low-mass-trainer-manual", 43),
                              ("02-missa-cantata", 57), ("03-solemn-mass", 70)):
            p = self.products[leaf]
            self.assertEqual(sum(u["kind"].startswith("ceremonial-action") for u in p["units"]), actions)

    def test_sung_response_fields_and_ipa_rows_retain_source_text(self):
        for leaf in ("02-missa-cantata-cue-cards", "03-solemn-mass-cue-cards"):
            for unit in self.products[leaf]["units"]:
                if unit["kind"] == "card-face" and unit["id"].startswith("R") and unit["id"].endswith(":back"):
                    text = words(unit["html"])
                    self.assertIn("℟.", text)
                    self.assertIn("LATIN CHUNKS", text)
                    self.assertIn("SAY IT LIKE", text)
        solemn_text = words(self.products["03-solemn-mass"]["parts"][0]["html"])
        self.assertIn("Scene 7:", solemn_text)
        self.assertIn("Scenes 2–4:", solemn_text)
        for leaf in ("02-missa-cantata", "03-solemn-mass"):
            value = self.products[leaf]["parts"][0]["html"]
            stop = value.index("Broad IPA for the complete response")
            table = value[value.rfind("<table>", 0, stop):value.index("</table>", stop)]
            self.assertEqual(table.count("<tr>"), 23)
            self.assertNotRegex(table, r"<td[^>]*>\s*<tr>")
            self.assertEqual(re.findall(r"<strong>(A\d+)</strong>", table), ["A" + str(i) for i in range(1, 23)])


    def test_final_assembly_rejects_body_losses_and_structure_changes_after_fragment_audits(self):
        from _web_print_server_schedule import verify_assembly
        selections = {}
        for leaf in ("01-low-mass", "01-low-mass-flash-cards", "02-missa-cantata"):
            adapter = server.Adapter(ROOT, "gpt", server.BASE + "/" + leaf, asset_resolver=metadata_asset)
            selections[leaf] = adapter._assembly_schedule
        cases = [
            ("01-low-mass", "title", lambda h: re.sub(r"<p>.*?</p>", "", h, count=1, flags=re.S)),
            ("01-low-mass", "scene-01", lambda h: re.sub(r"<p>.*?</p>", "", h, count=1, flags=re.S)),
            ("01-low-mass-flash-cards", "sheet-06-back", lambda h: re.sub(r'<footer class="sheet-notice".*?</footer>', "", h, flags=re.S)),
            ("01-low-mass-flash-cards", "sheet-01-front", lambda h: h.replace("℣", "", 1)),
            ("02-missa-cantata", "complete-guide", lambda h: h.replace('class="action"', 'class="omitted-role"', 1)),
            ("02-missa-cantata", "complete-guide", lambda h: re.sub(r"<img [^>]*>", "", h, count=1)),
            ("02-missa-cantata", "complete-guide", lambda h: re.sub(r"<h[1-6]>(.*?)</h[1-6]>", r"<p>\1</p>", h, count=1, flags=re.S)),
            ("02-missa-cantata", "complete-guide", lambda h: re.sub(r'<article class="action".*?</article>', lambda m: m[0].replace("Cue", "Omitted qualification", 1), h, count=1, flags=re.S)),
        ]
        for leaf, part_id, mutate in cases:
            with self.subTest(leaf=leaf, part=part_id, mutate=mutate):
                product = self.products[leaf]
                parts = copy.deepcopy(product["parts"])
                part = next(p for p in parts if p["id"] == part_id)
                changed = mutate(part["html"])
                self.assertNotEqual(changed, part["html"])
                part["html"] = changed
                part["html_sha256"] = server.sha(changed)
                with self.assertRaisesRegex(server.Refusal, "final assembly"):
                    verify_assembly(selections[leaf], parts, product["assets"], root=ROOT)
        # Reordering body fragments within a face preserves IDs, source
        # selection, every word and every self-supplied coverage counter.
        product = self.products["01-low-mass-flash-cards"]
        parts = copy.deepcopy(product["parts"])
        original = parts[0]["html"]
        paragraphs = list(re.finditer(r"<p>.*?</p>", original, re.S))
        first, second = paragraphs[:2]
        parts[0]["html"] = (original[:first.start()] + second[0] + original[first.end():second.start()]
                            + first[0] + original[second.end():])
        with self.assertRaisesRegex(server.Refusal, "final assembly"):
            verify_assembly(selections["01-low-mass-flash-cards"], parts, product["assets"], root=ROOT)
        # A matching caller-supplied HTML pin or successful fragment-audit
        # counter cannot manufacture a canonical source expectation.
        product = self.products["01-low-mass-flash-cards"]
        parts = copy.deepcopy(product["parts"])
        parts[0]["html"] = re.sub(r"<p>.*?</p>", "", parts[0]["html"], flags=re.S)
        parts[0]["html_sha256"] = server.sha(parts[0]["html"])
        with self.assertRaisesRegex(server.Refusal, "final assembly"):
            verify_assembly(selections["01-low-mass-flash-cards"], parts, product["assets"], root=ROOT)

    def test_source_schedule_is_complete_before_any_converter_or_render_call(self):
        with (patch.object(server.Adapter, "fragment", side_effect=AssertionError("source schedule called fragment")),
              patch.object(server.Adapter, "card_face", side_effect=AssertionError("source schedule called card_face")),
              patch.object(server.Adapter, "render_tex", side_effect=AssertionError("source schedule called render_tex")),
              patch.object(server.subprocess, "run", side_effect=AssertionError("source schedule spawned a converter"))):
            for leaf in server.LEAVES:
                adapter = server.Adapter(ROOT, "gpt", server.BASE + "/" + leaf, asset_resolver=metadata_asset)
                proof = adapter._assembly_schedule
                self.assertTrue(proof["occurrences"])
                self.assertTrue(all(o["context"]["source"].get("path") for o in proof["occurrences"]))
                self.assertTrue(all(o["context"]["expanded_sha256"] for o in proof["occurrences"]))
                self.assertEqual([p["id"] for p in proof["parts"]], [p["id"] for p in self.products[leaf]["parts"]])

    def test_exact_card_body_deletion_after_audit_and_omitted_fragment_call_refuse(self):
        output = server.BASE + "/01-low-mass-flash-cards"
        expectation = server.expected_card_print_selection(ROOT, "gpt", output)
        original_face = server.Adapter.card_face
        removed = []
        def changed_face(adapter, name, args):
            identity, side, body = original_face(adapter, name, args)
            removed.extend(re.findall(r"<p>.*?</p>", body, re.S))
            return identity, side, re.sub(r"<p>.*?</p>", "", body, flags=re.S)
        adapter = server.Adapter(ROOT, "gpt", output)
        with patch.object(server.Adapter, "card_face", changed_face):
            parts = adapter.render_cards()
        self.assertEqual(len(removed), 57)
        adapter.fragment_audits = [dict(ledger_digest="f" * 64, source_units=10000, expanded_sha256="f" * 64)]
        with self.assertRaisesRegex(server.Refusal, "final assembly"):
            adapter.finish(parts, expectation)
        adapter = server.Adapter(ROOT, "gpt", output)
        fragment = adapter.fragment
        omitted = []
        def missing_call(text):
            if not omitted:
                omitted.append(text)
                return ""
            return fragment(text)
        adapter.fragment = missing_call
        parts = adapter.render_cards()
        with self.assertRaisesRegex(server.Refusal, "final assembly"):
            adapter.finish(parts, expectation)


class SourceAndRefusalTests(unittest.TestCase):
    def test_independent_order_needs_no_conversion_or_prepared_assets(self):
        with patch.object(server, "pandoc_fragment", side_effect=AssertionError("source expectation converted text")):
            for leaf in server.LEAVES:
                callback = server.expected_card_print_selection if leaf.endswith(("flash-cards", "cue-cards")) else server.expected_guide_print_selection
                proof = callback(ROOT, "gpt", server.BASE + "/" + leaf)
                self.assertEqual(proof["expected_print_units"], [u["id"] for u in proof["print_unit_expectations"]])
                self.assertTrue(all(u["source_refs"] for u in proof["print_unit_expectations"]))

    def test_missing_or_reordered_source_inventory_identity_refuses(self):
        original = Path.read_bytes
        def changed(path):
            data = original(path)
            if path.name == "ceremonial-inventory.md":
                return data.replace(b"| LM-043 |", b"| LM-999 |")
            return data
        with patch.object(Path, "read_bytes", changed), self.assertRaisesRegex(server.Refusal, "independent Low Mass inventory"):
            server.expected_guide_print_selection(ROOT, "gpt", server.BASE + "/01-low-mass")

    def test_short_literal_omission_cannot_receive_a_coverage_pass(self):
        adapter = server.Adapter(ROOT, "gpt", server.BASE + "/01-low-mass-flash-cards",
                                 fragment_renderer=lambda source: "<p></p>")
        with self.assertRaisesRegex(server.Refusal, "lost canonical text"):
            adapter.fragment("Amen.")

    def test_unknown_output_provider_source_macro_and_ipa_refuse(self):
        with self.assertRaises(server.Refusal):
            server.Adapter(ROOT, "../gpt", server.BASE + "/01-low-mass")
        with self.assertRaises(server.Refusal):
            server.Adapter(ROOT, "gpt", "theology/angelology")
        adapter = server.Adapter(ROOT, "gpt", server.BASE + "/01-low-mass-flash-cards")
        with self.assertRaisesRegex(server.Refusal, "unimplemented"):
            adapter.fragment(r"\UnknownSemanticCommand{Important source text}")
        with self.assertRaises(server.Refusal):
            server.tipa_unicode(r"\unknownipa")
        self.assertEqual(server.tipa_unicode(r'"di.\textltailn um et "jus.tum est'), "ˈdi.ɲum et ˈjus.tum est")

    def test_typed_entrypoint_and_stale_or_mismatched_asset_refuse(self):
        record = server.document_schema.load_manifest(ROOT, ROOT / "src/gpt" / server.BASE / "01-low-mass/publication.toml")
        wrong = copy.deepcopy(record)
        wrong["entrypoint"] = "other.tex"
        with patch.object(server.document_schema, "load_manifest", return_value=wrong), self.assertRaisesRegex(server.Refusal, "exact canonical"):
            server.Adapter(ROOT, "gpt", server.BASE + "/01-low-mass")
        def stale(root, variant, macro):
            value = metadata_asset(root, variant, macro)
            value["source_inputs"] = {key: "0" * 64 for key in value["source_inputs"]}
            return value
        with self.assertRaisesRegex(server.Refusal, "stale"):
            server.Adapter(ROOT, "gpt", server.BASE + "/01-low-mass", asset_resolver=stale)
        adapter = server.Adapter(ROOT, "gpt", server.BASE + "/01-low-mass", asset_resolver=metadata_asset)
        adapter.asset_resolver = lambda *args: {**metadata_asset(*args), "id": "invented"}
        with self.assertRaisesRegex(server.Refusal, "mismatched"):
            adapter.diagram("LMSceneStart")
        adapter.asset_resolver = lambda *args: {**metadata_asset(*args), "body": b"corrupt"}
        with self.assertRaisesRegex(server.Refusal, "body"):
            adapter.diagram("LMSceneStart")

    def test_minipage_content_cannot_move_outside_its_canonical_container(self):
        adapter = server.Adapter(ROOT, "gpt", server.BASE + "/01-low-mass-flash-cards",
                                 fragment_renderer=lambda source: '<div class="minipage"></div><p>Amen.</p>')
        with self.assertRaisesRegex(server.Refusal, "minipage boundary"):
            adapter.fragment(r"\begin{minipage}{7in}Amen.\end{minipage}")

    def test_container_projection_cannot_accept_a_renderer_supplied_proof(self):
        with self.assertRaisesRegex(server.Refusal, "own source-container proof"):
            server._fragment_container_bindings('<div data-semantic-minipage="minipage-1"></div>', [{"id": "minipage-1"}])

    @unittest.skipUnless(shutil.which("pandoc"), "pinned Pandoc is required")
    def test_spacing_numbers_and_spanning_role_header_text_survive_pandoc(self):
        adapter = server.Adapter(ROOT, "gpt", server.BASE + "/02-missa-cantata")
        self.assertEqual(words(adapter.fragment(r"MODEL ALTAR:\quad 1 FIRST STEP\quad 2 SECOND STEP\quad 3 PREDELLA")),
                         "MODEL ALTAR: 1 FIRST STEP 2 SECOND STEP 3 PREDELLA")
        source = r"""\begin{longtable}{@{}>{\bfseries}p{0.14\linewidth}>{}p{0.40\linewidth}>{}p{0.40\linewidth}@{}}
\multicolumn{3}{@{}l}{\colorbox{black!7}{\parbox{\dimexpr\linewidth-2\fboxsep-6pt\relax}{\strut{\scriptsize\bfseries OPTIONAL ROLE ROUTES}\par{CB --- cross-bearer \quad L --- lesson singer}}}}\\
Scene & CB & L \\
\endhead
Ready & Complete CB route & Complete L route \\
\end{longtable}"""
        html = adapter.fragment(source)
        self.assertIn("OPTIONAL ROLE ROUTES", words(html))
        self.assertIn('colspan="3"', html)
        self.assertIn("Complete CB route", words(html))
        self.assertIn("Complete L route", words(html))

    @unittest.skipUnless(shutil.which("pandoc"), "pinned Pandoc is required")
    def test_source_generated_scene_labels_and_explicit_ranges_are_preserved(self):
        adapter = server.Adapter(ROOT, "gpt", server.BASE + "/03-solemn-mass")
        value = adapter.fragment(r"\begin{enumerate}[label=\textbf{Scene \arabic*:}]\item First source route.\item[\textbf{Scenes 2--4:}] Grouped source route.\item[\textbf{Scene 7:}] Ending source route.\end{enumerate}")
        self.assertIn("<dt><strong>Scene 1:</strong></dt>", value)
        self.assertIn("<dt><strong>Scenes 2–4:</strong></dt>", value)
        self.assertIn("<dt><strong>Scene 7:</strong></dt>", value)
        self.assertEqual(value.count("<dd>"), 3)
        self.assertIn("Ending source route.", words(value))

    def test_labeled_lists_require_a_supported_source_counter_and_scope(self):
        for source in (r"\begin{enumerate}[label=\roman*]\item Route.\end{enumerate}",
                       r"\begin{enumerate}[label=\arabic*,resume]\item Route.\end{enumerate}",
                       r"\begin{enumerate}[label=\arabic*]\item Outer.\begin{itemize}\item Inner.\end{itemize}\end{enumerate}"):
            with self.subTest(source=source), self.assertRaises(server.Refusal):
                server._labeled_list_projection(source)

    def test_changed_canonical_template_labels_refuse_before_conversion(self):
        read = Path.read_bytes
        cases = (("01-low-mass-flash-cards", "main.tex", b"PRIEST", b"UNSUPPORTED_SOURCE_ACTOR", "LowMassFrontCard"),
                 ("01-low-mass-flash-cards", "main.tex", b"LOW MASS", b"UNSUPPORTED SOURCE FORM", "LowMassFlashFrame"),
                 ("01-low-mass", "low-mass-book-format.tex", b"HOW / FINISH:", b"SOURCE CHANGED FINISH:", "LMAction"))
        for leaf, filename, before, after, template in cases:
            changed = []
            def changed_source(path):
                data = read(path)
                if path.name == filename and (filename != "main.tex" or path.parent.name == leaf):
                    rewritten = data.replace(before, after)
                    if rewritten != data:
                        changed.append(path)
                    return rewritten
                return data
            with self.subTest(template=template), patch.object(Path, "read_bytes", changed_source):
                with self.assertRaisesRegex(server.Refusal, "unsupported server source template: " + template):
                    server.Adapter(ROOT, "gpt", server.BASE + "/" + leaf, asset_resolver=metadata_asset,
                                   fragment_renderer=lambda source: self.fail("unsupported template reached conversion"))
            self.assertTrue(changed)

    def test_wrong_converter_binary_refuses(self):
        with patch.object(server.shutil, "which", return_value=sys.executable), self.assertRaisesRegex(server.Refusal, "Pandoc 3.11"):
            server.pandoc_command()


if __name__ == "__main__":
    unittest.main()
