"""Public native-print selections, their print pages and small web controls.

The native typesetters can build more documents than the public site admits.
This module narrows them to the site's publication dispositions, declared
reading volumes, publishable Bible editions and advertised papal witnesses.
Each admitted edition has one thin print page that carries the Generate PDF
controls and the edition's selection. A reader page carries a Print action
linking there; on a plain click the controller reads that selection and
generates the PDF in place, so the reader stays on the page.
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
# A link to an edition's print page that carries `print=1` requests its PDF:
# the reader Print action, and the publisher's rewritten PDF links.
_PRINT_LINK = re.compile(r"""\bhref=(["'])[^"']*?\bprint/[^"'?#]+\.html\?(?:[^"'#]*?&(?:amp;)?)?print=1(?:[&#]|\1)""")
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


def _admitted_recipes(root: Path, inputs: set | None = None) -> list[dict]:
    """Every declared publication output and Bible, less withdrawals and holds."""
    from _print_document import recipes
    result = []
    for recipe in recipes(root, family="publication"):
        declared = "src/" + recipe["provider"] + "/" + recipe["canonical"] + "/web-edition.toml"
        disposition = "release/publications/" + recipe["provider"] + "/" + recipe["document"] + ".json"
        if inputs is not None:
            inputs.update((declared, disposition))
        try:
            declaration = tomllib.loads((root / declared).read_text(encoding="utf-8"))
            from _document_schema import release_record
            release = release_record(root, root / disposition)
        except (OSError, ValueError) as error:
            raise NativePrintError("cannot read publication disposition: " + recipe["id"]) from error
        _need(release.get("id") == recipe["document"] and release.get("status") in {"alpha", "hold"},
              "publication release identity or disposition is invalid: " + recipe["id"])
        if not declaration.get("withdrawn") and release["status"] != "hold":
            result.append(recipe)
    result.extend(recipes(root, family="bible"))
    result.sort(key=lambda row: row["id"])
    _need(result and len({row["id"] for row in result}) == len(result),
          "public print selection is empty or duplicated")
    return result


def admission_inputs(root: Path) -> list[str]:
    """The declarations and release dispositions that decide publication admission."""
    inputs = set()
    _admitted_recipes(Path(root).resolve(), inputs)
    return sorted(inputs)


def admitted_documents(root: Path) -> dict[str, dict]:
    """Return the public output universe, never the unrestricted native list."""
    from _print_document import _plan_records
    root = Path(root).resolve()
    result = {}

    def add(identity, document, edition, title, **extra):
        _need(identity not in result, "duplicate public native print output: " + identity)
        _need(edition in {"main", "synthesis", "homily"}, "invalid native print output edition")
        result[identity] = dict(id=identity, output_id=identity, document=document,
                                edition=edition, title=title or identity, **extra)

    for row in _admitted_recipes(root):
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


def print_route(identity: str, reader: str | None = None) -> str:
    """The print page of one admitted edition.

    Publications and Bibles keep their established `print/` routes. A source
    reader's edition (papal document, reading-plan volume) prints from the same
    path under `print/`.
    """
    family, _, name = identity.partition(":")
    _identifier(name)
    if family == "publication":
        return "print/" + name + ".html"
    if family == "bible":
        return "print/bibles/" + name + ".html"
    _need(family in {"papal", "reading-plan"} and isinstance(reader, str) and reader.endswith(".html")
          and not reader.startswith("print/") and _identifier(reader.removesuffix(".html")),
          "a source edition's print page requires its reader route")
    return "print/" + reader


def _link(route: str, target: str) -> str:
    path, hash_, fragment = target.partition("#")
    return html.escape(posixpath.relpath(path, posixpath.dirname(route) or ".") + hash_ + fragment, quote=True)


def reader_action(route: str, target: str) -> str:
    """The Print action a reader page carries to its edition's print page.

    A plain click generates the PDF in place (`link_extras`); the link itself
    still opens the print page in a new tab or without JavaScript.
    """
    _need(target.startswith("print/") and target.endswith(".html"), "invalid print page route")
    return ('<p class="print-actions"><a href="' + _link(route, target) + '?print=1">'
            'Print / Generate PDF</a></p>')


def landing(identity: str, route: str, context: dict, *, label: str, reader: str | None = None,
            reader_label: str = "Read this edition online") -> dict:
    """One small print page: identity, the native controls and a way back to reading."""
    row = context["documents"].get(identity)
    _need(row is not None, "native print output is not publicly admitted: " + identity)
    _need(isinstance(label, str) and label.strip(), "print page requires its edition label")
    wasm = context.get("native_catalog") is not None
    note = ("Generate PDF typesets this edition in your browser from its current TeX sources, "
            "with the edition's own fonts and page layout. The first run downloads the "
            "typesetting engine and can take a minute." if wasm else
            "Generate PDF requests this edition newly typeset from its current TeX sources, "
            "with the edition's own fonts and page layout.")
    reading = ('<p class="native-print-landing__reader"><a href="' + _link(route, reader)
               + '">' + html.escape(reader_label) + '</a></p>') if reader else ""
    head, tail = extras(route, wasm=wasm)
    body = ('<article class="native-print-landing" data-print-edition="' + html.escape(identity, quote=True) + '">'
            + '<header><h1>' + html.escape(row["title"]) + '</h1><p class="native-print-landing__label">'
            + html.escape(label) + '</p></header><p>' + note + '</p>'
            + controls(identity, route, context) + reading + '</article>')
    return {"output_id": identity, "title": row["title"], "html": body, "head_extra": head, "body_extra": tail}


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


# Classification directories that say where a publication is filed, not what it
# is. They are dropped from download names; every other directory is kept, so a
# series member keeps its series ("roman-sanctuary-dictionary-comprehensive").
_FILING = frozenset((
    "liturgy roman-rite propers temporal sanctoral ritual general-calendar ordinary reference "
    "articles faith canon-law scripture biographies theology mariology heresies history "
    "devotions novenas curriculums roman-missal-third-edition-en-us-2011 2008-latin-2011-us-english").split())
# Vatican page identities embed the act's date and incipit:
# ``hf-l-xiii-enc-15051891-rerum-novarum`` (DDMMYYYY) or ``...-19260430-...``.
_VATICAN = re.compile(r"(?:^|\.)hf-[a-z0-9-]*?-([0-9]{8})-([a-z0-9-]+?)(?:\.([a-z0-9.-]+))?\Z")


def _slug(value: str, words: int | None = None) -> str:
    import unicodedata
    text = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    parts = [part for part in re.split(r"[^a-z0-9]+", text) if part]
    return "-".join(parts[:words] if words else parts)


def _vatican_date(digits: str) -> str | None:
    for day, month, year in ((digits[:2], digits[2:4], digits[4:]), (digits[6:], digits[4:6], digits[:4])):
        if 1 <= int(day) <= 31 and 1 <= int(month) <= 12 and 1500 <= int(year) <= 2100:
            return year + "-" + month + "-" + day
    return None


def download_name(identity: str, row: dict) -> str:
    """A portable PDF file name that is unique across the admitted editions.

    Publications: kept directories, the leaf (which carries -synthesis/-homily)
    and the provider: ``1962-f02-all-saints-synthesis-claude.pdf``. Papal
    witnesses end in a bare language code, so they are named by date and incipit
    where the identity carries them (``1891-05-15-rerum-novarum-en.pdf``),
    otherwise by the opening words of the title plus the witness identity.
    """
    family, _, rest = identity.partition(":")
    if family == "publication":
        provider, *path = rest.split("/")
        leaf = path[-1]
        kept = [part for part in path[:-1] if part not in _FILING
                and not (part == "postconciliar" and leaf.startswith("pc-"))]
        stem = _slug("-".join(kept + [leaf])) + "-" + provider
    elif family == "bible":
        stem = _slug(rest) + "-bible"
    elif family == "reading-plan":
        stem = "reading-plan-" + _slug(rest)
    else:
        witness, _, language = rest.rpartition("/")
        match = _VATICAN.search(witness)
        date = match and _vatican_date(match.group(1))
        if date:
            stem = "-".join(part for part in (date, match.group(2), _slug(match.group(3) or "")) if part)
        elif witness.startswith("papal."):
            stem = _slug(witness.removeprefix("papal."))
        else:
            parts = witness.split(".")
            if parts[0] == "acta" and len(parts) >= 4:
                # acta.aas.012.archive.aas.012.l019212 -> aas-012-l019212
                prefix = parts[1] + "-" + parts[2]
                witness = prefix + "-" + parts[-1].removeprefix(prefix + "-")
            stem = _slug(row["title"], 6) + "-" + _slug(witness)
        stem += "-" + language
    stem = stem.strip("-")[:190].rstrip("-")
    _need(re.fullmatch(r"[a-z0-9][a-z0-9-]*", stem or ""), "cannot name native print output: " + identity)
    return stem + ".pdf"


def controls(identity: str, route: str, context: dict) -> str:
    """Small, inert selection manifest; the browser never receives a credential."""
    row = context["documents"].get(identity)
    _need(row is not None, "native print output is not publicly admitted: " + identity)
    value = {"schema": SCHEMA, "id": identity,
             **{field: row[field] for field in ("document", "edition", "title")},
             "filename": download_name(identity, row),
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
            + '<p data-native-print-status role="status" aria-live="polite"></p>'
            + '<p class="native-print-progress" data-native-print-progress></p>' + historical
            + '<noscript><p>JavaScript is required to request a newly typeset PDF.</p></noscript>'
            + '<script type="application/json" data-native-print-manifest>' + descriptor + '</script></section>')


def link_extras(route: str, content: str) -> tuple[str, str]:
    """The controller a page loads when its content carries a PDF request link.

    The controller generates on a plain click without leaving the page, and
    loads the compiler only when a reader asks for a PDF.
    """
    return extras(route) if _PRINT_LINK.search(content) else ("", "")


def extras(route: str, *, wasm=False):
    relative = lambda target: html.escape(posixpath.relpath(target, posixpath.dirname(route) or "."), quote=True)
    compiler = '<script src="' + relative("shared/native-tex.js") + '" defer></script>' if wasm else ""
    return ('<link rel="stylesheet" href="' + relative(STYLE) + '">',
            compiler + '<script src="' + relative(SCRIPT) + '" defer></script>')
