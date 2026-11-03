"""Href projection keeps canonical source text and cross-part anchors intact."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import posixpath
import sys
import unittest
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import _web_print_links as links


def project(parts, **kwargs):
    return links.project_parts(parts, entrypoint="src/gpt/guide/main.tex",
        publication_routes=kwargs.pop("publication_routes", {}), site_routes=kwargs.pop("site_routes", {}),
        repository_paths=kwargs.pop("repository_paths", set()), repository_ref="a" * 40, **kwargs)


class Hrefs(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.hrefs = []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(value for name, value in attrs if name == "href")


class WebPrintLinksTest(unittest.TestCase):
    def parts(self):
        return [
            {"id": "body", "route": "print/gpt/guide.html", "html":
                '<section data-print-unit="body"><h1 id="title">Full title</h1><p id="ref">Body '
                '<a class="footnote-ref" href="#fn1">1</a>.</p></section>'},
            {"id": "notes", "route": "print/gpt/guide/notes.html", "html":
                '<section data-print-unit="notes"><p id="fn1">Complete qualification. '
                '<a href="#ref">Return</a></p></section>'},
        ]

    def assert_graph(self, pages):
        ids = {route: set(links.Identity(body).ids) for route, body in pages.items()}
        for route, body in pages.items():
            for href in Hrefs(body).hrefs:
                uri = urlsplit(href)
                destination = posixpath.normpath(posixpath.join(posixpath.dirname(route), unquote(uri.path))) if uri.path else route
                self.assertIn(destination, pages)
                self.assertIn(unquote(uri.fragment), ids[destination])

    def test_footnotes_backrefs_and_web_alias_resolve_across_parts_without_text_changes(self):
        original = self.parts()
        canonical, events = project(original)
        self.assertEqual(len(events), 2)
        alias, _ = project(original, route_overrides={"body": "web/gpt/guide.html"})
        pages = {part["route"]: part["html"] for part in canonical}
        pages[alias[0]["route"]] = alias[0]["html"]
        self.assert_graph(pages)
        for before, after in zip(original, canonical):
            self.assertEqual(links.Identity(before["html"]).text_sha256, after["text_sha256"])
            self.assertEqual(links.Identity(before["html"]).ids, links.Identity(after["html"]).ids)
            self.assertEqual(links.Identity(before["html"]).units, links.Identity(after["html"]).units)
        repeated, _ = project(canonical)
        self.assertEqual([part["html"] for part in canonical], [part["html"] for part in repeated])

    def test_source_relative_files_resolve_before_shallower_print_route_context(self):
        original = [{"id": "body", "route": "print/gpt/guide.html", "html":
            '<p><a href="../../../README.md">Library</a> '
            '<a href="../../../pdf/gpt/other.pdf#section">Other study</a></p>'}]
        changed, _ = project(original, site_routes={"README.md": "index.html"},
            publication_routes={"pdf/gpt/other.pdf": "web/gpt/other.html"},
            site_ids={"web/gpt/other.html": {"section"}})
        self.assertEqual(Hrefs(changed[0]["html"]).hrefs, ["../../index.html", "../../web/gpt/other.html#section"])

    def test_source_repository_fallback_requires_explicit_public_file_and_pinned_revision(self):
        source = "src/gpt/guide/research/source-audit.md"
        part = {"id": "body", "route": "print/gpt/guide.html", "html":
            '<p><a data-note="href=untouched" href="research/source-audit.md#L2">Audit &amp; limits</a></p>'}
        changed, _ = project([part], repository_paths={source})
        self.assertIn("/blob/" + "a" * 40 + "/" + source + "#L2", changed[0]["html"])
        self.assertIn('data-note="href=untouched"', changed[0]["html"])
        self.assertEqual(links.Identity(part["html"]).text_sha256, changed[0]["text_sha256"])
        with self.assertRaisesRegex(links.LinkError, "exact published commit"):
            links.project_parts([part], entrypoint="src/gpt/guide/main.tex", publication_routes={},
                site_routes={}, repository_paths={source}, repository_ref="main")

    def test_live_main_navigation_requires_explicit_opt_in_and_never_rewrites_external_citations(self):
        source = "src/gpt/guide/research/source-audit.md"
        part = {"id": "body", "route": "print/gpt/guide.html", "html":
            '<p><a href="research/source-audit.md">Current source record</a> '
            '<a href="https://example.org/witness.pdf#page=4">Exact external citation</a></p>'}
        kwargs = {"entrypoint": "src/gpt/guide/main.tex", "publication_routes": {}, "site_routes": {},
                  "repository_paths": {source}, "repository_ref": "main", "live_repository_navigation": True}
        changed, _ = links.project_parts([part], **kwargs)
        self.assertEqual(Hrefs(changed[0]["html"]).hrefs, [
            "https://github.com/spincyc/triptych/blob/main/" + source,
            "https://example.org/witness.pdf#page=4"])
        self.assertEqual(links.Identity(part["html"]).text_sha256, changed[0]["text_sha256"])
        for reference, opt_in in (("feature/topic", True), ("HEAD", True), ("main", False), ("main", "yes")):
            with self.subTest(reference=reference, opt_in=opt_in), self.assertRaises(links.LinkError):
                links.project_parts([part], **{**kwargs, "repository_ref": reference, "live_repository_navigation": opt_in})

    def test_inert_source_urn_citations_are_preserved_but_unknown_schemes_and_controls_refuse(self):
        urn = "urn:triptych:source:artifact.fixture#paragraph-4"
        part = {"id": "body", "route": "print/gpt/guide.html",
                "html": '<p><a href="' + urn + '">Source identification</a></p>'}
        changed, events = project([part])
        self.assertEqual(changed[0]["html"], part["html"])
        self.assertEqual(events, [])
        for href in ("javascript:bad()", "unrecognized:source", "urn:triptych:bad%00id", "urn:triptych:bad%C2%85id", "urn:triptych:bad id", "urn:triptych:bad%Q1id"):
            with self.subTest(href=href), self.assertRaises(links.LinkError):
                project([{**part, "html": '<p><a href="' + href + '">Citation</a></p>'}])

    def test_explicit_source_qualified_bare_url_stays_inert_without_inventing_https(self):
        entrypoint = "src/claude/theology/mariology/ark-of-the-covenant/main.tex"
        original = '<p id="source" data-print-unit="body"><a class="citation" href="lyricstranslate.com">lyricstranslate.com</a></p>'
        part = {"id": "body", "route": "print/claude/theology/mariology/ark-of-the-covenant.html", "html": original}
        options = {"entrypoint": entrypoint, "publication_routes": {}, "site_routes": {}, "repository_paths": set(),
                   "repository_ref": "a" * 40, "inert_source_urls": {entrypoint: {"lyricstranslate.com", "goarch.org/entrance-theotokos"}}}
        changed, events = links.project_parts([part], **options)
        self.assertEqual(Hrefs(changed[0]["html"]).hrefs, [])
        self.assertIn('title="Source URL: lyricstranslate.com"', changed[0]["html"])
        self.assertNotIn("https://lyricstranslate", changed[0]["html"])
        for field in ("ids", "units", "tags", "text_sha256"):
            self.assertEqual(getattr(links.Identity(original), field), getattr(links.Identity(changed[0]["html"]), field))
        self.assertEqual(events[0]["kind"], "inert-source-url")
        changed, _ = links.project_parts([{**part, "html": original.replace("lyricstranslate.com", "goarch.org/entrance-theotokos")}], **options)
        self.assertIn('title="Source URL: goarch.org/entrance-theotokos"', changed[0]["html"])
        self.assertEqual(Hrefs(changed[0]["html"]).hrefs, [])
        for source, target in (("src/gpt/guide/main.tex", "lyricstranslate.com"), (entrypoint, "unknown.example")):
            with self.subTest(source=source, target=target), self.assertRaises(links.LinkError):
                links.project_parts([{**part, "html": original.replace("lyricstranslate.com", target)}],
                                    **{**options, "entrypoint": source})
        for target in ("goarch.org/../escape", "goarch.org/%2e%2e/escape", "goarch.org/path?q=x", "goarch.org/path#fragment", "javascript:bad()"):
            with self.subTest(policy=target), self.assertRaises(links.LinkError):
                links.project_parts([part], **{**options, "inert_source_urls": {entrypoint: {target}}})
        rewriter = links.AnchorRewriter('<a href="bare.example" title="Original title">Words</a>', lambda target: None, inert_title=True)
        self.assertEqual(rewriter.result(), '<a  title="Original title">Words</a>')

    def test_transported_navigation_requires_declared_public_route_and_source_context_wins(self):
        part = {"id": "body", "route": "print/gpt/guide.html", "html": '<p><a href="other.html">Other study</a></p>'}
        changed, _ = project([part], site_routes={"print/gpt/other.html": "print/gpt/other.html"})
        self.assertEqual(Hrefs(changed[0]["html"]).hrefs, ["other.html"])
        changed, _ = project([part], site_routes={"print/gpt/other.html": "print/gpt/other.html",
                                                "src/gpt/guide/other.html": "library/owned-source.html"})
        self.assertEqual(Hrefs(changed[0]["html"]).hrefs, ["../../library/owned-source.html"])
        with self.assertRaises(links.LinkError):
            project([part])

    def test_missing_duplicate_private_active_and_escaping_targets_fail_closed(self):
        for href in ("#missing", "../../../pdf/gpt/held.pdf", "research/private.md", "javascript:bad()", "/src/private", "../../../../secret"):
            with self.subTest(href=href), self.assertRaises(links.LinkError):
                project([{"id": "body", "route": "print/gpt/guide.html", "html": '<p><a href="' + href + '">Words</a></p>'}])
        parts = self.parts()
        parts[1]["html"] += '<p id="ref">Ambiguous</p>'
        with self.assertRaisesRegex(links.LinkError, "repeated"):
            project(parts)

    def test_href_projection_preserves_entities_styles_and_existing_text_pin(self):
        original = '<p id="x" style="text-align: left;">A &amp; B <a href=#x title="href=untouched">Return</a></p>'
        pin = links.Identity(original).text_sha256
        changed, _ = project([{"id": "body", "route": "print/gpt/guide.html", "html": original, "text_sha256": pin}])
        self.assertEqual(changed[0]["html"], original)
        self.assertEqual(changed[0]["text_sha256"], pin)


if __name__ == "__main__":
    unittest.main()
