"""Join current source-reader proofs to compact inline browser print parts.

Source selection, rights and canonical coverage belong to ``_print_catalog``.
This hot assembler reads no files and creates no source proof or print assets.
The caller supplies final route-relative font records and adds the controls.
"""
from __future__ import annotations

from collections.abc import Mapping
import html
from pathlib import PurePosixPath
import posixpath
import re
from urllib.parse import urlsplit

from _print_catalog import (PRINT_PRODUCT_SCHEMA, _canonical, _sha,
                            _check_print_envelope, _check_print_units)
from _web_print_common import PrintError, compact_descriptor, normalize_html, part_statistics

PART_ID = "source-complete"
PART_SELECTOR = '[data-print-part="source-complete"]'
HELPERS = ("scripts/_web_print_sources.py", "scripts/_web_print_common.py", "scripts/_print_catalog.py")
_SHA = re.compile(r"[a-f0-9]{64}\Z")


class SourcePrintError(PrintError):
    """A source owner proof or its final inline part is inconsistent."""


def _need(condition, message):
    if not condition:
        raise SourcePrintError(message)


def _relative(value, *, suffix=None):
    _need(isinstance(value, str) and value and not any(ord(char) < 32 for char in value)
          and not any(char in value for char in "\\?#"), "invalid canonical source print path")
    path = PurePosixPath(value)
    _need(bool(path.parts) and not path.is_absolute() and ".." not in path.parts and str(path) == value,
          "source print path must be canonical and relative")
    _need(suffix is None or path.suffix == suffix, "source print route must be HTML")
    return value


def _fonts(records, route):
    _need(isinstance(records, list) and records, "source print fonts must be supplied for the final route")
    for record in records:
        _need(isinstance(record, dict) and isinstance(record.get("family"), str) and record["family"]
              and isinstance(record.get("sha256"), str) and _SHA.fullmatch(record["sha256"]),
              "source print font has no pinned identity")
        href = record.get("href")
        _need(isinstance(href, str) and href and "\\" not in href
              and not any(char.isspace() or ord(char) < 32 for char in href),
              "source print font has no route-relative href")
        parsed = urlsplit(href)
        target = posixpath.normpath(posixpath.join(posixpath.dirname(route), parsed.path))
        _need(not parsed.scheme and not parsed.netloc and not parsed.query and not parsed.fragment
              and not parsed.path.startswith("/") and target != ".." and not target.startswith("../"),
              "source print font escapes the published site")
    return records


def prepare_sources(source_pages, *, stylesheet_sha256, fonts_for_route):
    """Return compact inline products and legacy actions without doing I/O.

Only complete owner declarations create products. Period components remain in
the caller's original page set, and legacy volumes retain their own controller.
The returned inline page fragment has no controls, stylesheet or script; the
site owner adds them around these exact, finally measured part bytes.
"""
    _need(isinstance(source_pages, Mapping), "source pages must be a route mapping")
    _need(isinstance(stylesheet_sha256, str) and _SHA.fullmatch(stylesheet_sha256),
          "source print stylesheet identity is invalid")
    _need(callable(fonts_for_route), "source print fonts require a final-route callback")
    result = {"products": {}, "pages": {}, "reader_actions": {}, "source_paths": []}
    source_paths, seen = set(HELPERS), set()
    for route, page in source_pages.items():
        _relative(route, suffix=".html")
        _need(isinstance(page, Mapping), "source reader page must be a mapping")
        inputs = page.get("source_paths", ())
        _need(isinstance(inputs, (list, tuple)), "source print inputs must be an ordered path list")
        for path in inputs:
            _relative(path)
            _need(not path.startswith((".scratch/", "build/", "release/papal-documents/inputs/"))
                  and PurePosixPath(path).suffix.lower() != ".pdf",
                  "source print inputs must retain canonical text or metadata")
            source_paths.add(path)
        if "print_product" not in page:
            continue
        owner = page["print_product"]
        _need(isinstance(owner, Mapping), "source print owner metadata must be a mapping")
        identifier, mode = owner.get("output_id"), owner.get("mode")
        _need(isinstance(identifier, str) and re.fullmatch(r"(?:papal|reading-plan):[a-z0-9][a-z0-9./:-]*", identifier),
              "source print output has no canonical namespaced identity")
        _need(identifier not in seen, "source print output is declared by more than one reader")
        seen.add(identifier)
        _need(mode in {"inline", "legacy-volume"}, "unsupported source print mode")
        _need(owner.get("id", identifier) == identifier and owner.get("root_route", route) == route,
              "source print owner route or identity disagrees")
        result["reader_actions"][route] = {"output_id": identifier, "mode": mode}
        if mode == "legacy-volume":
            continue
        _need(owner.get("schema") == PRINT_PRODUCT_SCHEMA and owner.get("id") == identifier
              and owner.get("print_type") == "source-volume", "unsupported inline source print owner schema")
        _need(isinstance(owner.get("title"), str) and owner["title"]
              and isinstance(owner.get("source_id"), str) and owner["source_id"],
              "inline source print lacks its source identity or title")
        _need(all(isinstance(owner.get(key), str) and _SHA.fullmatch(owner[key])
                  for key in ("source_digest", "selection_digest")), "invalid source print input identities")
        _need(isinstance(page.get("html"), str) and page["html"], "inline source reader has no complete HTML")
        _need(owner.get("source_paths") == page.get("source_paths"), "source print owner input paths disagree")
        units, proof = owner.get("expected_units"), owner.get("coverage_result")
        _need(isinstance(units, list) and units and isinstance(proof, Mapping),
              "inline source print has no independent canonical coverage proof")
        fragment = ('<section data-print-part="' + PART_ID + '" data-print-document="' +
                    html.escape(identifier, quote=True) + '" data-print-source="' + owner["source_digest"] + '">\n' +
                    page["html"] + '\n</section>')
        fragment = normalize_html(fragment, profile="source-volume")
        try:
            actual_sha = _check_print_units(units, fragment)
            envelope_sha = _check_print_envelope(owner.get("envelope"), fragment)
        except (KeyError, TypeError, ValueError) as error:
            raise SourcePrintError("inline source print no longer matches its owner selection or envelope: " + str(error)) from error
        _need(proof.get("actual_units_sha256") == actual_sha,
              "inline source print differs from its independent owner content check")
        _need(proof.get("envelope_sha256") == owner.get("envelope_sha256") == envelope_sha,
              "inline source print differs from its independent owner envelope check")
        selection_sha = _sha(_canonical({"output_id": identifier, "source_digest": owner["source_digest"],
                                        "expected_units": units, "envelope": owner["envelope"]}))
        _need(owner["selection_digest"] == selection_sha,
              "inline source print envelope is not bound to the canonical selection")
        part = {"id": PART_ID, "selector": PART_SELECTOR,
                **part_statistics(fragment, part_id=PART_ID)}
        descriptor = {**owner, "style_sha256": stylesheet_sha256,
                      "parts": [part], "assets": [], "fonts": _fonts(fonts_for_route(route), route)}
        compact = compact_descriptor(descriptor)
        compact.update(output_id=identifier, source_id=owner["source_id"], root_route=route, mode=mode)
        result["products"][identifier] = compact
        result["pages"][route] = {**page, "html": fragment, "output_id": identifier}
    result["source_paths"] = sorted(source_paths)
    return result
