"""Publish complete browser print editions from a held, verified JSON snapshot.

Conversion belongs to the cold producer. This module only projects admitted
routes, verifies payloads and joins the current source-reader owner proofs.
"""
from __future__ import annotations

import base64
import copy
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
from urllib.parse import urlsplit, urlunsplit

import _browser_products as core
from _source_projection_receipt import read_file
from _web_print_common import inventory, part_statistics, sha256
from _web_print_links import AnchorRewriter, Identity, RoutingContext, project_parts
from _web_print_prepare import PREFIX, read_index, read_product, read_asset, need, source_path

SHARED = "src/web/browser/shared/"
CSS = "shared/web-print.css"
JS = "shared/web-print.js"
PUNCTUS = "shared/fonts/triptych-punctus-elevatus.woff2"
PUNCTUS_LICENSE = "shared/fonts/OFL-Junicode.txt"
# This canonical \url has no scheme. Preserve its printed wording without
# inventing a web address or treating it as a repository-relative link.
INERT_SOURCE_URLS = {"src/claude/theology/mariology/ark-of-the-covenant/main.tex": {
    "lyricstranslate.com", "st-sergius.org", "goarch.org/entrance-theotokos",
    "catholicapologetics.info", "papalencyclicals.net", "newmanreader.org",
    "bible.usccb.org", "universalis.com", "scborromeo.org",
}}


def relative_link(route, target):
    return posixpath.relpath(target, posixpath.dirname(route) or ".")


def _json(value):
    # A JSON descriptor is inert even if a source title contains HTML syntax.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("<", "\\u003c")


def _extras(route):
    css = html.escape(relative_link(route, CSS), quote=True)
    js = html.escape(relative_link(route, JS), quote=True)
    return ('<link rel="stylesheet" href="' + css + '">',
            '<script src="' + js + '" defer></script>')


def _page(descriptor, fragment, route, *, source_paths=(), base=None, native_context=None):
    """Surround canonical part bytes with controls outside the printable body."""
    css = html.escape(relative_link(route, CSS), quote=True)
    title = html.escape(descriptor["title"])
    controls = ('<div class="print-actions">'
            + '<button type="button" data-web-print-start>Print / Save as PDF</button> '
            + '<button type="button" data-web-print-cancel hidden>Cancel</button>'
            + '<p data-web-print-status role="status" aria-live="polite"></p></div>')
    if native_context is not None:
        from _native_print import controls as native_controls
        controls = native_controls(descriptor["id"], route, native_context)
    notice = ("Use Generate PDF on this page to typeset the complete edition of "
              if native_context is not None else "Use Print / Save as PDF on this page to prepare the complete edition of ")
    body = ('<section data-web-print-document="' + html.escape(descriptor["id"], quote=True)
            + '" data-web-print-style="' + css + '">' + controls
            + '<p data-web-print-notice>' + notice
            + title + '.</p><div data-web-print-content>' + fragment + '</div>'
            + '<script type="application/json" data-web-print-manifest>' + _json(descriptor)
            + '</script></section>')
    head, tail = _extras(route)
    if native_context is not None:
        from _native_print import extras
        native_head, native_tail = extras(route, wasm=native_context.get("native_catalog") is not None)
        head += native_head
        tail += native_tail
    page = dict(base or {})
    page.update(output_id=descriptor["id"], title=descriptor["title"], html=body,
                head_extra=page.get("head_extra", "") + head,
                body_extra=page.get("body_extra", "") + tail,
                source_paths=sorted(set(page.get("source_paths", ())) | set(source_paths)))
    return page


def _part_page(descriptor, part, source_paths):
    route = part["route"]
    target = html.escape(relative_link(route, descriptor["root_route"]) + "?print=1", quote=True)
    link = '<a href="' + target + '">Print complete edition / Download PDF</a>'
    fragment = ('<section data-web-print-reader><p class="print-actions">' + link + '</p>'
                + '<p data-web-print-reader-notice>Use ' + link + ' to prepare the complete edition.</p>'
                + '<div data-web-print-reader-content>' + part["html"] + '</div></section>')
    head, _ = _extras(route)
    return {"output_id": descriptor["id"], "title": descriptor["title"], "html": fragment,
            "head_extra": head, "source_paths": source_paths}


class _Images(HTMLParser):
    """Replace only declared IMG source attributes, retaining source text."""
    def __init__(self, fragment, replacements):
        super().__init__(convert_charrefs=False)
        self.fragment, self.replacements, self.edits, self.seen = fragment, replacements, [], set()
        self.lines = [0]
        self.lines.extend(match.end() for match in re.finditer("\n", fragment))
        self.feed(fragment)
        self.close()

    def handle_starttag(self, tag, pairs):
        if tag != "img":
            return
        attrs = dict(pairs)
        key = attrs.get("data-print-asset")
        need(key in self.replacements, "print image is not in the exact product asset selection: " + str(key))
        raw = self.get_starttag_text()
        matches = list(re.finditer(r"(?<![\w:-])src\s*=\s*([\"'])(.*?)\1", raw, re.I | re.S))
        need(len(matches) == 1, "print image has an ambiguous or missing source")
        match = matches[0]
        row, column = self.getpos()
        start = self.lines[row - 1] + column
        self.edits.append((start + match.start(2), start + match.end(2),
                           html.escape(self.replacements[key], quote=True)))
        self.seen.add(key)

    handle_startendtag = handle_starttag

    def result(self):
        value = self.fragment
        for start, end, replacement in reversed(self.edits):
            value = value[:start] + replacement + value[end:]
        return value


def _measure(part, expected):
    measured = part_statistics(part["html"], selectors=tuple(expected["counts"]))
    for key in ("text_sha256", "structure_sha256", "counts"):
        need(measured[key] == expected[key], "prepared print part differs from its " + key + ": " + part["id"])
    for key in ("expected_ids", "units"):
        need(inventory(measured[key]) == expected[key], "prepared print part differs from its ordered " + key)
    return measured


def _alias_page(descriptor, parts, alias, source_paths, fonts_for_route, asset_routes, product, native_context=None):
    """Render the same reading parts with a descriptor pinned to this route."""
    cloned = copy.deepcopy(descriptor)
    cloned["fonts"] = fonts_for_route(alias)
    for asset in cloned["assets"]:
        asset["href"] = relative_link(alias, asset_routes[product["asset_ids"][asset["id"]]])
    inline, links = [], []
    for expected, part in zip(cloned["parts"], parts, strict=True):
        if "selector" not in expected:
            expected["href"] = relative_link(alias, part["route"])
            links.append('<li><a href="' + html.escape(expected["href"], quote=True) + '">'
                         + html.escape(part["id"].replace("-", " ")) + '</a></li>')
            continue

        def rebase(target):
            uri = urlsplit(target)
            if uri.scheme or uri.netloc or not uri.path:
                return target
            destination = posixpath.normpath(posixpath.join(posixpath.dirname(part["route"]), uri.path))
            return urlunsplit(("", "", relative_link(alias, destination), uri.query, uri.fragment))

        fragment = AnchorRewriter(part["html"], rebase).result()
        replacements = {semantic: relative_link(alias, asset_routes[sha])
                        for semantic, sha in product["asset_ids"].items()}
        fragment = _Images(fragment, replacements).result()
        measured = part_statistics(fragment, selectors=tuple(expected["counts"]))
        need(measured["text_sha256"] == expected["text_sha256"] and
             inventory(measured["units"]) == expected["units"], "compatibility route changed print source")
        expected["structure_sha256"] = measured["structure_sha256"]
        inline.append(fragment)
    navigation = '<nav aria-label="Edition parts"><ul>' + ''.join(links) + '</ul></nav>' if links else ''
    return _page(cloned, ''.join(inline) + navigation, alias, source_paths=source_paths,
                 native_context=native_context)


def _public_paths(root, known):
    """Admit current public text navigation without invoking Git or converters."""
    paths = set(known)
    extensions = {".md", ".tex", ".toml", ".json", ".yaml", ".yml", ".tsv", ".csv", ".txt", ".bib"}
    for directory in ("src", "guidance", "library", "docs", "release"):
        for parent, directories, files in os.walk(root / directory, followlinks=False):
            directories[:] = [name for name in directories if name not in {".scratch", "__pycache__", "data"}
                              and not (Path(parent) / name).is_symlink()]
            for filename in files:
                path = Path(parent) / filename
                if path.suffix.lower() in extensions and not path.is_symlink():
                    paths.add(path.relative_to(root).as_posix())
    paths.update(path.name for path in root.iterdir() if path.is_file() and not path.is_symlink()
                 and (path.suffix.lower() in extensions or path.name in {"LICENSE", "THIRD_PARTY.md"}))
    return paths


def _site_anchors(root, site_routes, source_pages):
    from _markdown_render import render_markdown
    anchors = {route: set(Identity(page["html"]).ids) for route, page in source_pages.items()}
    for source, route in site_routes.items():
        if source.endswith(".md"):
            anchors.setdefault(route, set()).update(Identity(render_markdown(read_file(root, source).decode(), root)).ids)
    return anchors


def _asset_envelopes(root, data_root, index, canonical_asset_routes):
    assets, routes, fonts, source_paths = {}, {}, [], set()
    for row in index["assets"]:
        record = read_asset(data_root, row)
        declared = record["asset"]
        canonical = record.get("canonical_path")
        if canonical:
            body = read_file(root, canonical)
            source_paths.add(canonical)
            payload = {"path": root / canonical}
        else:
            body = base64.b64decode(record["body_base64"], validate=True)
            payload = {"body": body}
        need(sha256(body) == declared["sha256"] and len(body) == declared["bytes"],
             "private print asset changed after its source proof")
        route = canonical_asset_routes.get(canonical, declared["src"])
        need(route not in assets, "ambiguous public print asset route")
        routes[row["id"]] = route
        asset = {**declared, **payload, "owners": set()}
        assets[route] = asset
        if asset["role"] == "font":
            fonts.append(asset)
    for font in fonts:
        license_route = font.get("license")
        # Licence paths in the private pool use its content-addressed route.
        if license_route not in assets:
            match = next((route for sha, route in routes.items()
                          if license_route and PurePosixPath(license_route).stem == sha), None)
            need(match is not None, "print font licence is not in the held asset pool")
            font["license"] = match
    base_fonts = [font for font in fonts if font["family"] in {"Libertinus Serif", "Libertinus Sans", "Libertinus Math"}]
    marks = [font for font in fonts if font["family"] == "Triptych Source Marks"]
    need(len(fonts) == 9 and len(base_fonts) == 8 and len(marks) == 1 and
         marks[0].get("unicode_range") == "U+211F,U+2123,U+21A9,U+2610,U+2720",
         "complete print editions require eight Libertinus faces and the exact source-mark supplement")
    return assets, routes, fonts, source_paths


def catalog(root, included, *, browser_data_root, source_pages, site_routes=None, canonical_asset_routes=None,
            native_context=None):
    """Join complete admitted editions; never convert, download or hydrate."""
    root = Path(root).resolve()
    if native_context is None and (root / "scripts/_native_print.py").is_file():
        from _native_print import site_context
        native_context = site_context(root)
    held = core.require_products(root)
    data_root = Path(browser_data_root).resolve()
    need(data_root == held.data_root.resolve(), "print data must be the caller's held verified snapshot")
    index = read_index(data_root)
    members = {PREFIX + "/catalog.json"} | {PREFIX + "/" + row["path"]
               for table in ("products", "assets") for row in index[table]}
    actual = {path for path in held.files if held.delivery_by_path.get(path) == "print-preparation"}
    need(actual == members and all(path.startswith(PREFIX + "/") for path in actual),
         "private print catalogue does not exactly own the verified preparation family")
    need(all(held.delivery_by_path.get(path) == "print-preparation" for path in members),
         "private print catalogue crossed a delivery boundary")
    from _bible_editions import EDITIONS
    allowed = {"publication:" + provider + "/" + output for provider, output in included}
    allowed.update("bible:" + key for key, row in EDITIONS.items() if row.get("publishable") is True)
    need({row["id"] for row in index["products"]} == allowed,
         "private print editions differ from the current admitted output selection")
    result = {"products": {}, "pages": {}, "assets": {}, "reader_actions": {}, "source_paths": []}
    site_routes = dict(site_routes or {})
    reviewed_routes = set(site_routes.values())
    for provider, output in included:
        for route in ("web/" + provider + "/" + output + ".html",
                      "print/" + provider + "/" + output + ".html"):
            site_routes[route] = route
    for key, row in EDITIONS.items():
        if row.get("publishable") is True:
            route = "print/bibles/" + key + ".html"
            site_routes[route] = route
    for route in {*site_routes.values(), *source_pages}:
        site_routes[route] = route
    assets, asset_routes, font_records, source_inputs = _asset_envelopes(
        root, data_root, index, canonical_asset_routes or {})
    source_inputs.update(index["source_paths"])
    for public, canonical, mime, role in ((CSS, SHARED + "web-print.css", "text/css", "stylesheet"),
                                        (JS, SHARED + "web-print.js", "text/javascript", "controller"),
                                        (PUNCTUS, SHARED + "fonts/triptych-punctus-elevatus.woff2", "font/woff2", "font"),
                                        (PUNCTUS_LICENSE, SHARED + "fonts/OFL-Junicode.txt", "text/plain", "font-license")):
        body = read_file(root, canonical)
        asset = {"path": root / canonical, "bytes": len(body), "sha256": sha256(body),
                 "mime": mime, "role": role, "owners": set()}
        if public == PUNCTUS:
            asset.update(family="Triptych Punctus Elevatus", weight="400", style="normal",
                         unicode_range="U+2E4E", license=PUNCTUS_LICENSE)
            font_records.append(asset)
        assets[public] = asset
        source_inputs.add(canonical)
    if native_context is not None:
        from _native_print import HELPERS, SCRIPT, STYLE
        source_inputs.update(HELPERS)
        source_inputs.add("release/print-archive.json")
        for public, mime, role in ((SCRIPT, "text/javascript", "controller"), (STYLE, "text/css", "stylesheet")):
            canonical = "src/web/browser/" + public
            body = read_file(root, canonical)
            assets[public] = {"path": root / canonical, "bytes": len(body), "sha256": sha256(body),
                              "mime": mime, "role": role, "owners": set()}
        if native_context.get("native_catalog") is not None:
            canonical, public = SHARED + "native-tex.js", "shared/native-tex.js"
            body = read_file(root, canonical)
            source_inputs.add(canonical)
            assets[public] = {"path": root / canonical, "bytes": len(body), "sha256": sha256(body),
                              "mime": "text/javascript", "role": "controller", "owners": set()}
    style_sha = assets[CSS]["sha256"]

    def fonts_for_route(route):
        faces = []
        for font in font_records:
            public = PUNCTUS if font["family"] == "Triptych Punctus Elevatus" else asset_routes[font["id"]]
            faces.append({**{key: font[key] for key in ("family", "sha256", "weight", "style", "unicode_range") if key in font},
                          "href": relative_link(route, public)})
        return faces

    publication_routes = {"pdf/" + provider + "/" + output + ".pdf":
                          "web/" + provider + "/" + output + ".html" for provider, output in included}
    publication_routes.update({"pdf/bibles/" + key + ".pdf": "print/bibles/" + key + ".html"
                               for key, row in EDITIONS.items() if row.get("publishable") is True})
    for route, page in source_pages.items():
        if page.get("legacy_pdf"):
            publication_routes[page["legacy_pdf"]] = route
    known_paths = _public_paths(root, source_inputs | set(site_routes))
    site_ids = _site_anchors(root, site_routes, source_pages)
    routing = RoutingContext(
        publication_routes=publication_routes, site_routes=site_routes,
        site_ids=site_ids, repository_paths=known_paths, repository_ref="main",
        live_repository_navigation=True, inert_source_urls=INERT_SOURCE_URLS)
    for row in index["products"]:
        product = read_product(data_root, row)
        descriptor = copy.deepcopy(product["descriptor"])
        identifier, route = descriptor["id"], product["root_route"]
        need(len(product["parts"]) == len(descriptor["parts"]), "print part declaration/body count differs")
        for part, expected in zip(product["parts"], descriptor["parts"], strict=True):
            need(part["id"] == expected["id"], "print part declaration order differs")
            _measure(part, expected)
        source_inputs.update(product["source_paths"])
        entrypoint = product["metadata"].get("entrypoint", "src/sources/bibles/print-source.tsv")
        parts, _ = project_parts(product["parts"], entrypoint=entrypoint, context=routing)
        public_assets, used_assets, units = [], set(), []
        for semantic, asset_id in product["asset_ids"].items():
            need(asset_id in asset_routes, "print product refers to an absent held asset")
            public = asset_routes[asset_id]
            asset = assets[public]
            asset["owners"].add(identifier)
            public_assets.append({"id": semantic, "href": relative_link(route, public),
                                  **{key: asset[key] for key in ("sha256", "mime", "role")}})
        for part, expected in zip(parts, descriptor["parts"], strict=True):
            replacements = {semantic: relative_link(part["route"], asset_routes[asset_id])
                            for semantic, asset_id in product["asset_ids"].items()}
            projection = _Images(part["html"], replacements)
            part["html"] = projection.result()
            used_assets.update(projection.seen)
            measured = part_statistics(part["html"], selectors=tuple(expected["counts"]))
            need(measured["text_sha256"] == expected["text_sha256"] and measured["counts"] == expected["counts"],
                 "print routing altered source words or semantic counts")
            for key in ("expected_ids", "units"):
                need(inventory(measured[key]) == expected[key], "print routing altered source occurrence order")
            units.extend(measured["units"])
            expected["structure_sha256"] = measured["structure_sha256"]
            if "href" in expected:
                expected["href"] = relative_link(route, part["route"])
        need(inventory(units) == descriptor["unit_inventory"], "print routing changed complete source selection")
        need(used_assets == set(product["asset_ids"]), "print product asset selection contains absent illustrations")
        descriptor.update(output_id=identifier, root_route=route, style_sha256=style_sha,
                          assets=public_assets, fonts=fonts_for_route(route))
        if "response_geometry_coverage" in product["metadata"]:
            descriptor["response_geometry_coverage"] = copy.deepcopy(product["metadata"]["response_geometry_coverage"])
        if product["metadata"].get("source_id"):
            descriptor["source_id"] = product["metadata"]["source_id"]
        result["products"][identifier] = descriptor
        inline = [part["html"] for part in parts if "selector" in part]
        links = ''.join('<li><a href="' + html.escape(relative_link(route, part["route"]), quote=True)
                        + '">' + html.escape(part["id"].replace("-", " ")) + '</a></li>'
                        for part in parts if "href" in part)
        fragment = ''.join(inline) + ('<nav aria-label="Edition parts"><ul>' + links + '</ul></nav>' if links else '')
        result["pages"][route] = _page(descriptor, fragment, route, source_paths=product["source_paths"],
                                        native_context=native_context)
        for part in parts:
            if part["route"] != route:
                need(part["route"] not in result["pages"], "print part routes collide")
                result["pages"][part["route"]] = _part_page(descriptor, part, product["source_paths"])
        if identifier.startswith("publication:"):
            alias = "web/" + identifier.removeprefix("publication:") + ".html"
            result["reader_actions"][alias] = {"output_id": identifier, "mode": "navigate", "target": route}
            if alias not in reviewed_routes:
                result["pages"][alias] = _alias_page(descriptor, parts, alias, product["source_paths"],
                                                     fonts_for_route, asset_routes, product, native_context)
    from _web_print_sources import prepare_sources
    source_catalog = prepare_sources(source_pages, stylesheet_sha256=style_sha, fonts_for_route=fonts_for_route)
    for identifier, descriptor in source_catalog["products"].items():
        need(identifier not in result["products"], "source print identity collides with a publication")
        result["products"][identifier] = descriptor
    for route, page in source_catalog["pages"].items():
        result["pages"][route] = _page(result["products"][page["output_id"]], page["html"], route,
                                      source_paths=page.get("source_paths", ()), base=page,
                                      native_context=native_context)
    result["reader_actions"].update(source_catalog["reader_actions"])
    if native_context is not None:
        from _native_print import controls, extras
        for route, action in result["reader_actions"].items():
            if action["mode"] == "legacy-volume":
                head, tail = extras(route, wasm=native_context.get("native_catalog") is not None)
                action.update(native_controls=controls(action["output_id"], route, native_context),
                              native_head_extra=head, native_body_extra=tail)
        expected_native = set(result["products"]) | {
            action["output_id"] for action in result["reader_actions"].values()
            if action["mode"] == "legacy-volume"}
        need(set(native_context["documents"]) == expected_native,
             "native PDF admissions differ from the complete public print universe")
    source_inputs.update(source_catalog["source_paths"])
    all_owners = set(result["products"])
    for route, asset in assets.items():
        if asset["role"] in {"font", "font-license", "stylesheet", "controller"}:
            asset["owners"].update(all_owners)
        if asset["owners"]:
            asset["owners"] = sorted(asset["owners"])
            result["assets"][route] = asset
    source_inputs.update({"scripts/_web_print.py", "scripts/_web_print_sources.py", "scripts/_web_print_links.py",
                          "scripts/_web_print_common.py", "scripts/_web_print_prepare.py"})
    for path in source_inputs:
        source_path(path)
        read_file(root, path)
    result["source_paths"] = sorted(source_inputs)
    return result


def decorate_reader(content, output_relative, inventory, *, relative_link):
    action = inventory["reader_actions"][output_relative]
    need(action["mode"] == "navigate", "publication reader has no complete print destination")
    target = html.escape(relative_link(output_relative, action["target"]) + "?print=1", quote=True)
    link = '<a href="' + target + '">Print / Download PDF</a>'
    body = ('<section data-web-print-reader><p class="print-actions">' + link + '</p>'
            + '<p data-web-print-reader-notice>Use ' + link + ' to prepare the complete edition.</p>'
            + '<div data-web-print-reader-content>' + content + '</div></section>')
    head, _ = _extras(output_relative)
    return body, head, ""


def decorate_source_page(relative, page, inventory):
    if relative in inventory["pages"]:
        return inventory["pages"][relative]
    action = inventory["reader_actions"].get(relative, {})
    if action.get("native_controls"):
        return {**page, "html": action["native_controls"] + page["html"],
                "head_extra": page.get("head_extra", "") + action["native_head_extra"],
                "body_extra": page.get("body_extra", "") + action["native_body_extra"]}
    return page
