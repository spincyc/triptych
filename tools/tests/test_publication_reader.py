from __future__ import annotations

from pathlib import Path
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import _publication_reader as reader


class PublicationReaderTest(unittest.TestCase):
    def setUp(self):
        self.records, self.products, self.routes, self.admitted = {}, {}, set(), set()

    def add(self, leaf, *, provider="gpt", roles=("canonical", "synthesis", "homily"), kind="proper-1962", title=None):
        owner = provider + "/" + leaf
        for role in roles:
            output = leaf if role == "canonical" else leaf + "-" + role
            key = (provider, output)
            self.records[key] = ({"id": owner, "kind": kind}, {"id": provider + "/" + output, "role": role})
            self.admitted.add(key)
            self.routes.add(f"web/{provider}/{output}.html")
            self.products[f"publication:{provider}/{output}"] = {"title": title or leaf.rsplit("/", 1)[-1]}
        return (provider, leaf)

    def contexts(self):
        return reader.contexts(self.records, self.admitted, self.products, self.routes)

    def test_companions_follow_declared_owner_roles_and_admission(self):
        key = self.add("propers/temporal/10-sunday")
        self.add("propers/temporal/11-sunday", roles=("canonical",))
        self.add("propers/temporal/12-sunday", provider="claude")
        self.add("propers/votive/10-mass")
        self.add("propers/temporal/13-document", kind="article")
        held = ("gpt", key[1] + "-homily")
        self.admitted.remove(held)
        contexts = self.contexts()
        self.assertNotIn(held, contexts)
        self.assertEqual([row["label"] for row in contexts[key]["outputs"]], ["Full Study Guide", "Synthesis"])
        self.assertEqual([row["owner"] for row in contexts[key]["choices"]],
                         ["gpt/propers/temporal/10-sunday", "gpt/propers/temporal/11-sunday"])

    def test_filename_similarity_does_not_create_companion(self):
        first = self.add("propers/temporal/a", roles=("canonical",))
        second = self.add("propers/temporal/a-homily", roles=("canonical",))
        contexts = self.contexts()
        self.assertEqual(len(contexts[first]["outputs"]), 1)
        self.assertEqual(contexts[second]["current"]["label"], "Full Study Guide")

    def test_adjacent_choice_preserves_treatment_and_names_fallback(self):
        self.add("propers/temporal/10-first")
        self.add("propers/temporal/11-second", roles=("canonical",))
        self.add("propers/temporal/12-third")
        current = self.contexts()[("gpt", "propers/temporal/10-first-homily")]
        self.assertTrue(current["choices"][1]["fallback"])
        self.assertEqual(current["choices"][2]["href"], "web/gpt/propers/temporal/12-third-homily.html")
        page = reader.wrap('<h2 id="opening">Opening</h2>', current, "web/gpt/propers/temporal/10-first-homily.html")
        self.assertIn('Next celebration — Full Study Guide', page)
        self.assertNotIn('rel="prev"', page)
        self.assertIn('rel="next"', page)

    def test_missing_route_is_not_offered_and_print_only_route_is_real(self):
        key = self.add("reference", roles=("canonical",), kind="reference")
        self.routes.clear()
        self.assertEqual(self.contexts(), {})
        self.routes.add("print/gpt/reference.html")
        self.assertEqual(self.contexts()[key]["current"]["href"], "print/gpt/reference.html")

    def test_body_and_sealed_print_parts_survive_byte_for_byte(self):
        key = self.add("propers/temporal/66-sunday")
        body = ('<section data-web-print-document="publication:gpt/example">'
                '<div data-web-print-content><section data-print-part="complete">'
                '<h1>Title</h1><h2 id="sec:appointed">Appointed <em>texts</em></h2>'
                '<p>Exact source &amp; qualification.</p><h3 id="note-one">Note</h3>'
                '<table><tr><td>Latin</td></tr></table></section></div>'
                '<script type="application/json" data-web-print-manifest>{"complete":true}</script></section>')
        page = reader.wrap(body, self.contexts()[key], "print/gpt/propers/temporal/66-sunday.html")
        self.assertEqual(page.count(body), 1)
        self.assertIn('href="#sec%3Aappointed">Appointed texts</a>', page)
        self.assertIn('href="#note-one">Note</a>', page)
        self.assertIn('href="../../../../web/gpt/propers/temporal/66-sunday-homily.html"', page)

    def test_anchor_collisions_and_unsafe_labels_do_not_change_existing_ids(self):
        key = self.add("work", title='Title <script> & "quoted"')
        body = '<h2 id="reader-content">Text &lt;source&gt;</h2><p id="reader-content-2">A</p>'
        page = reader.wrap(body, self.contexts()[key], "web/gpt/work.html")
        self.assertIn('data-reader-content id="reader-content-3"', page)
        self.assertIn('href="#reader-content">Text &lt;source&gt;</a>', page)
        self.assertIn('Title &lt;script&gt; &amp; &quot;quoted&quot;', page)
        self.assertEqual(page.count(body), 1)

    def test_unanchored_heading_can_use_existing_section_boundary_without_mutation(self):
        key = self.add("work")
        body = '<section id="section-a"><h2>Section A</h2><p>Complete.</p></section>'
        page = reader.wrap(body, self.contexts()[key], "web/gpt/work.html")
        self.assertIn('href="#section-a">Section A</a>', page)
        self.assertIn(body, page)

    def test_empty_contents_have_an_existing_whole_document_target(self):
        key = self.add("work")
        page = reader.wrap('<h1>Title</h1><p>Body.</p>', self.contexts()[key], "web/gpt/work.html")
        self.assertIn('href="#reader-content">Document</a>', page)
        self.assertIn('id="reader-content"', page)

    def test_real_publisher_wraps_both_routes_and_preserves_print_descriptor(self):
        from .test_public_alpha import load_tool
        tool = load_tool()
        key = self.add("propers/temporal/66-sunday")
        body = '<section data-web-print-document><div data-web-print-content><h2 id="body">Body</h2></div></section>'
        manifest = {"provider": "gpt", "providers": ["gpt", "claude"]}
        with mock.patch.object(tool, "load_manifest", return_value=manifest), \
                mock.patch.object(tool, "publication_reader_contexts", return_value=self.contexts()):
            for route in ("web/gpt/propers/temporal/66-sunday.html", "print/gpt/propers/temporal/66-sunday.html"):
                rendered, head, tail = tool.publication_reader_shell(body, route, "publication:gpt/propers/temporal/66-sunday")
                self.assertIn(body, rendered)
                self.assertIn('class="publication-reader"', rendered)
                self.assertIn("publication-reader.css", head)
                self.assertIn("publication-reader.js", tail)
                self.assertIn("catalogue-navigation.js", tail)
            self.assertEqual(tool.publication_reader_shell(body, "liturgy/day.html"), (body, "", ""))
            self.assertEqual(tool.publication_reader_shell(body, "print/bibles/clementine.html"), (body, "", ""))

    def test_legacy_catalogue_labels_use_declared_output_role(self):
        from .test_public_alpha import load_tool
        tool = load_tool()
        # Neither the old generic label nor the filename establishes a role.
        key = ("gpt", "propers/temporal/66-companion")
        declaration = ({"id": "gpt/propers/temporal/66", "kind": "proper-1962"}, {"role": "homily"})
        with mock.patch.object(tool, "publication_source_records", return_value={key: declaration}), \
                mock.patch.object(tool, "source_to_output", return_value="66-companion.html"):
            self.assertEqual(tool.rewrite_links("library/test.md", "library/test.html",
                             "[PDF](../pdf/gpt/propers/temporal/66-companion.pdf)", {key}),
                             "[Homily](66-companion.html)")
            self.assertEqual(tool.rewrite_links("library/test.md", "library/test.html",
                             "[Synthesis](../pdf/gpt/propers/temporal/66-companion.pdf)", {key}),
                             "[Synthesis](66-companion.html)")


if __name__ == "__main__":
    unittest.main()
