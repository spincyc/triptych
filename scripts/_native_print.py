"""Public native-print selections and their deliberately small web controls.

The native typesetters can build more documents than the public site admits.
This module narrows them to the site's publication dispositions, declared
reading volumes, publishable Bible editions and advertised papal witnesses.
It never builds a PDF, fetches a source, or treats an archive as current text.
"""
from __future__ import annotations

import html
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import tomllib
from urllib.parse import urlsplit

SCHEMA = "triptych-native-print/v1"
CONFIG = "src/common/native-print-service.toml"
SCRIPT = "shared/native-print.js"
STYLE = "shared/native-print.css"
HELPERS = ("scripts/_native_print.py", CONFIG,
           "src/web/browser/shared/native-print.js", "src/web/browser/shared/native-print.css")
_REVISION = re.compile(r"[0-9a-f]{40}\Z")
_RELATIVE = re.compile(r"[a-z0-9][a-z0-9./-]*\Z")


class NativePrintError(ValueError):
    pass


def _need(condition, message):
    if not condition:
        raise NativePrintError(message)


def _json(root: Path, relative: str):
    path = root / relative
    _need(not path.is_symlink() and path.resolve().is_relative_to(root.resolve()),
          "native print input escapes the repository")
    try:
        return json.loads(path.read_bytes())
    except (OSError, ValueError) as error:
        raise NativePrintError("cannot read native print input: " + relative) from error


def _identifier(value):
    _need(isinstance(value, str) and _RELATIVE.fullmatch(value)
          and all(part not in {"", ".", ".."} for part in value.split("/")),
          "invalid native print identity")
    return value


def source_revision(root: Path) -> str:
    """The exact source checkout served by both site and compilation service."""
    try:
        value = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                               capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise NativePrintError("native printing requires an identified source revision") from error
    _need(_REVISION.fullmatch(value), "native printing requires a full source revision")
    return value


def service_endpoint(root: Path) -> str:
    path = root / CONFIG
    _need(not path.is_symlink(), "native print configuration must not be a symlink")
    try:
        config = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise NativePrintError("cannot read native print service configuration") from error
    _need(set(config) == {"schema_version", "endpoint"} and config["schema_version"] == 1,
          "invalid native print service configuration")
    value = os.environ.get("TRIPTYCH_NATIVE_PRINT_ENDPOINT", config["endpoint"])
    _need(isinstance(value, str), "native print endpoint must be text")
    if not value:
        return ""
    _need(not any(char.isspace() or ord(char) < 32 for char in value)
          and "\\" not in value, "invalid native print service endpoint")
    parsed = urlsplit(value)
    _need(parsed.scheme == "https" or parsed.scheme == "http" and
          parsed.hostname in {"localhost", "127.0.0.1", "::1"},
          "native print service requires HTTPS")
    _need(parsed.hostname and not parsed.username and not parsed.password
          and not parsed.query and not parsed.fragment,
          "native print endpoint must be a public base URL")
    _need(not any(part in {".", ".."} for part in parsed.path.split("/"))
          and not parsed.path.rstrip("/").endswith("/v1"),
          "native print endpoint must not include an API version")
    return value.rstrip("/")


def admitted_documents(root: Path) -> dict[str, dict]:
    """Return the public output universe, never the unrestricted native list."""
    from _web_print_products import admitted_recipes
    from _print_document import _plan_records
    root = Path(root).resolve()
    result = {}

    def add(identity, document, edition, title, **extra):
        _need(identity not in result, "duplicate public native print output: " + identity)
        _need(edition in {"main", "synthesis", "homily"}, "invalid native print output edition")
        result[identity] = dict(id=identity, output_id=identity, document=document,
                                edition=edition, title=title or identity, **extra)

    # This is the existing cold producer's exact withdrawal/hold disposition.
    for row in admitted_recipes(root):
        identity = row["id"]
        if row["family"] == "publication":
            document = "publication:" + row["provider"] + "/" + row["canonical"]
            add(identity, document, row["edition"], row["title"])
        else:
            add(identity, identity, "main", row["title"])
    if list((root / "src/sources/reading-plans").glob("*.yaml")):
        for row in _plan_records(root):
            add(row["id"], row["id"], "main", row["title"])

    index_path = "src/sources/papal-documents/encyclicals-index.json"
    if (root / index_path).exists():
        index = _json(root, index_path)
        release = _json(root, "release/papal-documents.json")
        _need(index.get("schema") == "triptych-encyclicals-index/v2"
              and release.get("schema") == "triptych-papal-release/v1",
              "invalid papal native print admissions")
        installed = {}
        for row in release["documents"]:
            key = row["id"], row["language"]
            _need(key not in installed, "duplicate papal release selection")
            installed[key] = row
        for act in index["encyclicals"]:
            for reader in act["readers"]:
                key = _identifier(reader["release_id"]), _identifier(reader["language"])
                row = installed.get(key)
                _need(row is not None and row.get("review", {}).get("status") == "PASS"
                      and row.get("text_fidelity", {}).get("status") == "pass"
                      and row.get("source", {}).get("rights_status") == "public-domain"
                      and all(reader.get(field) == row.get(field)
                              for field in ("pdf", "pdf_sha256", "pages")),
                      "advertised papal native print is not a reviewed release selection")
                identity = "papal:" + key[0] + "/" + key[1]
                add(identity, identity, "main", row["source"]["title"])
    return dict(sorted(result.items()))


def admitted_selections(root: Path) -> dict[tuple[str, str], dict]:
    result = {}
    for row in admitted_documents(root).values():
        key = row["document"], row["edition"]
        _need(key not in result, "ambiguous native print selection")
        result[key] = row
    return result


def _archives(root: Path):
    path = root / "release/print-archive.json"
    if not path.exists():
        return {}
    value = _json(root, "release/print-archive.json")
    snapshot = value.get("snapshot", "")
    _need(value.get("schema") == "triptych-print-archive/v1" and _REVISION.fullmatch(snapshot),
          "invalid historical print archive")
    result = {}
    for row in value["publications"]:
        identity = _identifier(row["id"])
        filename = row.get("filename")
        _need(isinstance(filename, str) and PurePosixPath(filename).name == filename
              and filename.endswith(".pdf") and re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", ""))
              and type(row.get("bytes")) is int and row["bytes"] > 0
              and row.get("legacy_pdf") == "pdf/" + identity + ".pdf"
              and row.get("url") == "https://github.com/spincyc/triptych-artifacts/releases/download/prints-"
                  + snapshot[:7] + "/" + filename,
              "invalid historical native print delivery")
        _need("publication:" + identity not in result, "duplicate historical native print")
        result["publication:" + identity] = {**row, "snapshot": snapshot}
    return result


def site_context(root: Path, *, documents=None, revision=None, endpoint=None, native_catalog=None):
    root = Path(root).resolve()
    revision = revision if revision is not None else source_revision(root)
    _need(isinstance(revision, str) and _REVISION.fullmatch(revision), "invalid native print source revision")
    result = {"documents": admitted_documents(root) if documents is None else documents,
              "source_revision": revision,
              "endpoint": service_endpoint(root) if endpoint is None else endpoint,
              "archives": _archives(root)}
    if native_catalog is not None:
        _need(set(native_catalog["selections"]) == set(result["documents"]),
              "native TeX bundles do not cover the exact public print universe")
        result["native_catalog"] = native_catalog
    return result


def controls(identity: str, route: str, context: dict) -> str:
    """Small, inert selection manifest; the browser never receives a credential."""
    row = context["documents"].get(identity)
    _need(row is not None, "native print output is not publicly admitted: " + identity)
    value = {"schema": SCHEMA, "id": identity,
             **{field: row[field] for field in ("document", "edition", "title")},
             "source_revision": context["source_revision"], "endpoint": context["endpoint"]}
    if context.get("native_catalog") is not None:
        catalog = context["native_catalog"]
        bundle, runtime = catalog["selections"][identity], catalog["runtime"]
        relative = lambda target: posixpath.relpath(target, posixpath.dirname(route) or ".")
        value["wasm"] = {"bundle": relative(bundle["bundle_href"]),
                         "bundle_sha256": bundle["bundle_sha256"], "bundle_bytes": bundle["bundle_bytes"],
                         "runtime": relative(runtime["href"]),
                         "runtime_sha256": runtime["sha256"], "runtime_bytes": runtime["bytes"]}
    descriptor = json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("<", "\\u003c")
    archive = context["archives"].get(identity)
    historical = ""
    if archive:
        historical = ('<p class="native-print-archive"><a href="' + html.escape(archive["url"], quote=True)
                      + '">Download earlier TeX PDF</a> — preserved printed edition ('
                      + html.escape(archive["snapshot"][:7])
                      + '). It may precede the current text.</p>')
    return ('<section class="native-print-actions" data-native-print="' + html.escape(identity, quote=True)
            + '"><p>The PDF uses this edition’s original TeX typography, fonts and page layout.</p>'
            + '<button type="button" data-native-print-start>Generate PDF</button> '
            + '<button type="button" data-native-print-cancel hidden>Cancel</button> '
            + '<a data-native-print-download hidden>Download PDF</a>'
            + '<p data-native-print-status role="status" aria-live="polite"></p>' + historical
            + '<noscript><p>JavaScript is required to request a newly typeset PDF.</p></noscript>'
            + '<script type="application/json" data-native-print-manifest>' + descriptor + '</script></section>')


def extras(route: str, *, wasm=False):
    relative = lambda target: html.escape(posixpath.relpath(target, posixpath.dirname(route) or "."), quote=True)
    compiler = '<script src="' + relative("shared/native-tex.js") + '" defer></script>' if wasm else ""
    return ('<link rel="stylesheet" href="' + relative(STYLE) + '">',
            compiler + '<script src="' + relative(SCRIPT) + '" defer></script>')
