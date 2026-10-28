"""Vatican body extraction and rights-gated papal source typesetting."""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
import unicodedata
from urllib.parse import urlsplit

from _tooling import examples_live_on_the_verbs, with_examples

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-papal-typeset/v1"
EXTRACTOR = "vatican-richtext-plain-v1"
LANGUAGES = {"la": "Latin", "en": "English", "it": "Italian", "fr": "French",
             "es": "Spanish", "de": "German", "pt": "Portuguese", "pl": "Polish",
             "mul": "Multilingual"}
ADMITTED_RIGHTS = {"public-domain", "licensed", "permission"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
BLOCK = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "blockquote", "tr", "pre"}
SKIP = {"script", "style", "noscript"}


class PapalTypesetError(ValueError):
    """An input or source cannot safely be typeset."""


class _LoadedManifest(dict):
    """Parsed input and the exact bytes read together, without a later path read."""

    def __init__(self, data, payload):
        super().__init__(data)
        self.input_bytes = payload


class Node:
    def __init__(self, tag="", attrs=(), parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children = []

    @property
    def classes(self):
        return set((self.attrs.get("class") or "").split())


class DocumentParser(HTMLParser):
    """Small tree builder that keeps void elements and omitted p ends bounded."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        if tag in {"p", "li"} and self.stack[-1].tag == tag:
            self.stack.pop()
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def walk(node):
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from walk(child)


def _visible(node):
    if isinstance(node, str):
        return node
    if node.tag in SKIP or "translation-field" in node.classes:
        return ""
    if node.tag == "br":
        return "\n"
    separator = " " if node.tag in {"td", "th"} else ""
    return "".join(_visible(child) for child in node.children) + separator


def _text(node):
    return re.sub(r"\s+", " ", _visible(node)).strip()


def _has_ancestor_class(node, name):
    parent = node.parent
    while parent is not None:
        if name in parent.classes:
            return True
        parent = parent.parent
    return False


def _list_marker(number, style):
    if style in {"a", "A"} and number > 0:
        letters, value = "", number
        while value:
            value, digit = divmod(value - 1, 26)
            letters = chr(ord("a") + digit) + letters
        return letters.upper() if style == "A" else letters
    if style in {"i", "I"} and 0 < number < 4000:
        roman, value = "", number
        for integer, token in ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
                               (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
                               (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")):
            count, value = divmod(value, integer)
            roman += token * count
        return roman if style == "I" else roman.lower()
    return str(number)


def _list_blocks(node):
    if "list-style" in node.attrs.get("style", "").lower():
        raise PapalTypesetError("custom CSS list numbering requires explicit source review")
    items = [child for child in node.children if isinstance(child, Node) and child.tag == "li"]
    reverse = "reversed" in node.attrs
    try:
        number = int(node.attrs.get("start", len(items) if reverse else 1))
    except (ValueError, TypeError) as error:
        raise PapalTypesetError("ordered-list start is not an integer") from error
    result = []
    for item in items:
        try:
            number = int(item.attrs.get("value", number))
        except (ValueError, TypeError) as error:
            raise PapalTypesetError("list-item value is not an integer") from error
        blocks = _rich_blocks(item)
        marker = _list_marker(number, node.attrs.get("type", "1")) + "." if node.tag == "ol" else "•"
        if blocks:
            blocks[0] = {**blocks[0], "text": marker + " " + blocks[0]["text"]}
        else:
            blocks = [{"kind": "paragraph", "text": marker}]
        result.extend(blocks)
        number += -1 if reverse else 1
    return result


def _rich_blocks(node):
    pending, result = [], []

    def flush():
        value = re.sub(r"\s+", " ", "".join(pending)).strip()
        pending.clear()
        return [{"kind": "paragraph", "text": value}] if value else []

    for child in node.children:
        if isinstance(child, str):
            pending.append(child)
        elif child.tag in SKIP or "translation-field" in child.classes:
            continue
        elif child.tag in {"ol", "ul"}:
            result.extend(flush())
            result.extend(_list_blocks(child))
        elif child.tag in BLOCK:
            result.extend(flush())
            nested = any(desc is not child and (desc.tag in BLOCK or desc.tag in {"ol", "ul"}) for desc in walk(child))
            if nested and child.tag != "tr":
                result.extend(_rich_blocks(child))
            else:
                value = _text(child)
                if value:
                    kind = "heading" if re.fullmatch("h[1-6]", child.tag) else "paragraph"
                    result.append({"kind": kind, "text": value})
        elif any(desc.tag in BLOCK for desc in walk(child)):
            result.extend(flush())
            result.extend(_rich_blocks(child))
        else:
            pending.append(_visible(child))
    result.extend(flush())
    return result


def extract_document(html_bytes: bytes, url: str = "") -> dict:
    """Normalize rich-text whitespace without repairing, translating or renumbering."""
    charset = re.search(br"charset\s*=\s*[\"']?([A-Za-z0-9_-]+)", html_bytes[:10000], re.I)
    encoding = charset.group(1).decode("ascii") if charset else "utf-8"
    try:
        source = html_bytes.decode(encoding)
    except (UnicodeError, LookupError) as error:
        raise PapalTypesetError(f"cannot decode document as {encoding}") from error
    parser = DocumentParser()
    parser.feed(source)
    parser.close()
    rich = [node for node in walk(parser.root) if "vaticanrichtext" in node.classes
            and _has_ancestor_class(node, "testo") and _has_ancestor_class(node, "documento")
            and not _has_ancestor_class(node, "vaticanrichtext")]
    if not rich:
        raise PapalTypesetError("Vatican document rich-text body is absent; no page-wide fallback")
    blocks = [block for node in rich for block in _rich_blocks(node)]
    text = "\n\n".join(block["text"] for block in blocks) + "\n"
    if len(text.strip()) < 100:
        raise PapalTypesetError("Vatican document body is unexpectedly short")
    title = next((node for node in walk(parser.root) if node.tag == "title"), None)
    return {"blocks": blocks, "text": text, "title": _text(title) if title else "",
            "source_url": url, "extractor": EXTRACTOR}


def safe_id(identifier: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", identifier.lower()).strip("-")[:140]
    if not value:
        raise PapalTypesetError("document id has no usable characters")
    return value + "-" + hashlib.sha256(identifier.encode("utf-8")).hexdigest()[:8]


def output_stem(document: dict) -> str:
    return f"{document.get('date') or 'undated'}-{safe_id(document['id'])}-{document['language']}"


def safe_label(identifier: str, language: str) -> str:
    return f"papal:{safe_id(identifier)}:{language}"


TEX_SPECIAL = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "$": r"\$",
               "&": r"\&", "#": r"\#", "%": r"\%", "_": r"\_",
               "^": r"\textasciicircum{}", "~": r"\textasciitilde{}", "\f": " "}
CYRILLIC_RUN = re.compile(r"[\u0400-\u052f\u1c80-\u1c8f\u2de0-\u2dff\ua640-\ua69f]")
UNICODE_RUN = re.compile(r"[\u0370-\u052f\u1f00-\u1fff\u1c80-\u1c8f\u2de0-\u2dff\ua640-\ua69f][\u0370-\u052f\u1f00-\u1fff\u1c80-\u1c8f\u2de0-\u2dff\ua640-\ua69f\u0300-\u036f]*|.[\u0300-\u036f]+|[\u0300-\u036f]+")
SYMBOL_RUN = re.compile(r"[\u25ba]")
FONT_RUN = re.compile(UNICODE_RUN.pattern + "|" + SYMBOL_RUN.pattern)


def tex_escape(text: str) -> str:
    if any(ord(char) < 32 and char not in "\n\r\t\f" for char in text):
        raise PapalTypesetError("source contains a control character")
    return "".join(TEX_SPECIAL.get(char, char) for char in text)


def source_tex_escape(text: str) -> str:
    """Preserve Greek, Cyrillic and combining characters with supporting fonts."""
    parts, offset = [], 0
    for match in FONT_RUN.finditer(text):
        parts.append(tex_escape(text[offset:match.start()]))
        if SYMBOL_RUN.search(match.group()):
            parts.append(r"{\PapalSymbolFont " + tex_escape(match.group()) + "}")
        elif CYRILLIC_RUN.search(match.group()):
            parts.append(r"{\PapalCyrillicFont " + tex_escape(match.group()) + "}")
        else:
            # Some composed abbreviation glyphs omit their mark in ToUnicode.
            actual = match.group().encode("utf-16-be").hex().upper()
            parts.append(r"\PapalUnicodeText{" + actual + "}{" + tex_escape(match.group()) + "}")
        offset = match.end()
    parts.append(tex_escape(text[offset:]))
    return "".join(parts)


def body_tex_escape(text: str, allow_long_token_breaks=False) -> str:
    """Optionally wrap literal long OCR runs without adding source characters."""
    if not allow_long_token_breaks:
        return source_tex_escape(text)
    parts, offset = [], 0
    for match in re.finditer(r"\S{48,}", text):
        parts.append(source_tex_escape(text[offset:match.start()]))
        clusters = []
        for char in match.group():
            if clusters and unicodedata.category(char).startswith("M"):
                clusters[-1] += char
            else:
                clusters.append(char)
        parts.append(r"\allowbreak{}".join(source_tex_escape(cluster) for cluster in clusters))
        offset = match.end()
    parts.append(source_tex_escape(text[offset:]))
    return "".join(parts)


def _resolve_path(value: str, root: Path) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise PapalTypesetError("text_path must be relative to the source root without traversal")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise PapalTypesetError("text_path escapes the source root")
    return resolved


def _validate_revision(value, owner="manifest") -> str:
    try:
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
            raise ValueError()
        dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError) as error:
        raise PapalTypesetError(f"{owner} revision must be an explicit whole-second UTC timestamp") from error
    return value


def validate_document(document: dict, root: Path = ROOT) -> dict:
    for name in ("id", "title", "pope", "language", "source_url", "text_path", "sha256",
                 "artifact_id", "rights_status", "rights_basis"):
        if not isinstance(document.get(name), str) or not document[name].strip():
            raise PapalTypesetError(f"document requires nonempty {name}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9.-]*", document["id"]):
        raise PapalTypesetError("document id must use lowercase ASCII letters, digits, dots and hyphens")
    if document["language"] not in LANGUAGES:
        raise PapalTypesetError(f"unsupported language: {document['language']}")
    if "revision" in document:
        _validate_revision(document["revision"], "document")
    if "language_label" in document:
        label = document["language_label"]
        if (not isinstance(label, str) or not label.strip()
                or label != label.strip() or len(label) > 120
                or any(ord(char) < 32 or char in "\u2028\u2029" for char in label)):
            raise PapalTypesetError("language_label requires a bounded single-line label")
    if document["rights_status"] not in ADMITTED_RIGHTS:
        raise PapalTypesetError("document lacks an admitted distribution rights status")
    for name in ("source_note", "rights_notice"):
        if name in document and (not isinstance(document[name], str) or not document[name].strip()):
            raise PapalTypesetError(f"optional {name} must be a nonempty string")
    if document.get("date"):
        try:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", document["date"]):
                raise ValueError()
            dt.date.fromisoformat(document["date"])
        except (TypeError, ValueError) as error:
            raise PapalTypesetError("document date must be an ISO calendar date") from error
    split = urlsplit(document["source_url"])
    if (split.scheme not in {"https", "http"} or not split.netloc or split.username or split.password
            or any(char.isspace() or ord(char) < 32 for char in document["source_url"])):
        raise PapalTypesetError("source_url must be a public HTTP(S) URL")
    if not re.fullmatch(r"[a-f0-9]{64}", document["sha256"]):
        raise PapalTypesetError("document requires a bare SHA-256 digest")
    path = _resolve_path(document["text_path"], root)
    try:
        payload = path.read_bytes()
        artifact = tomllib.loads((path.parent / "artifact.toml").read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise PapalTypesetError("text and adjacent source-library artifact manifest must be readable") from error
    digest = hashlib.sha256(payload).hexdigest()
    if digest != document["sha256"]:
        raise PapalTypesetError("text payload SHA-256 mismatch")
    for key, expected in (("record_type", "artifact"), ("id", document["artifact_id"]),
                          ("storage", "tracked"), ("rights_status", document["rights_status"]),
                          ("rights_basis", document["rights_basis"]), ("sha256", digest),
                          ("byte_size", len(payload))):
        if artifact.get(key) != expected:
            raise PapalTypesetError(f"source-library artifact disagrees on {key}")
    file_value = artifact.get("path")
    if not isinstance(file_value, str) or _resolve_path(file_value, root) != path:
        raise PapalTypesetError("source-library artifact path does not own text_path")
    if not str(artifact.get("media_type", "")).startswith("text/plain"):
        raise PapalTypesetError("source-library artifact is not plain text")
    if "source_url" in artifact and artifact["source_url"] != document["source_url"]:
        raise PapalTypesetError("source_url disagrees with the controlling source-library artifact")
    selected_owner, edition_path = artifact, path.parents[2] / "edition.toml"
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PapalTypesetError("text payload is not UTF-8") from error
    if not text.strip():
        raise PapalTypesetError("text payload is empty")
    if document.get("segment_id"):
        segment_path = document.get("segment_path")
        if not isinstance(segment_path, str):
            raise PapalTypesetError("segment entry requires segment_path")
        try:
            selected_segment_path = _resolve_path(segment_path, root)
            segment = tomllib.loads(selected_segment_path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as error:
            raise PapalTypesetError("segment manifest is not readable") from error
        for key, expected in (("schema", 2), ("record_type", "segment"), ("id", document["segment_id"]),
                              ("artifact_id", document["artifact_id"]), ("artifact_sha256", digest),
                              ("physical_line_ranges", document.get("physical_line_ranges"))):
            if segment.get(key) != expected:
                raise PapalTypesetError(f"segment manifest disagrees on {key}")
        # A constituent may have a different language from its containing volume.
        selected_owner, edition_path = segment, selected_segment_path.parents[1] / "edition.toml"
        lines = text.split("\n")
        if lines[-1] == "":
            lines.pop()
        ranges, last = document.get("physical_line_ranges"), 0
        if not isinstance(ranges, list) or not ranges:
            raise PapalTypesetError("segment requires physical line ranges")
        excerpts = []
        for pair in ranges:
            if not isinstance(pair, list) or len(pair) != 2 or not all(type(n) is int for n in pair):
                raise PapalTypesetError("segment range must be two integers")
            start, end = pair
            if not last < start <= end <= len(lines):
                raise PapalTypesetError("segment ranges overlap or escape the controlling artifact")
            excerpts.append("\n".join(line.removesuffix("\r") for line in lines[start - 1:end]))
            last = end
        continuations = document.get("range_continuations", [])
        if (not isinstance(continuations, list)
                or any(type(index) is not int or not 0 <= index < len(excerpts) - 1 for index in continuations)
                or continuations != sorted(set(continuations))):
            raise PapalTypesetError("range_continuations must contain ordered unique nonterminal range indices")
        text = excerpts[0]
        for index, excerpt in enumerate(excerpts[1:]):
            # The registered bounds and controller hash remain authoritative.
            # Only an explicitly declared selection boundary loses its paragraph
            # break; every retained non-whitespace character stays literal.
            text = text.rstrip() + " " + excerpt.lstrip() if index in continuations else text + "\n\n" + excerpt
    elif document.get("physical_line_ranges") or document.get("segment_path") or "range_continuations" in document:
        raise PapalTypesetError("bounded text selection requires a registered segment_id")
    try:
        edition = tomllib.loads(edition_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise PapalTypesetError("selected source edition manifest must be readable") from error
    if (edition.get("record_type") != "edition" or not selected_owner.get("edition_id")
            or edition.get("id") != selected_owner["edition_id"]):
        raise PapalTypesetError("selected source edition identity disagrees with its artifact or segment")
    if edition.get("language") != document["language"]:
        raise PapalTypesetError("document language disagrees with the selected source edition")
    tex_escape(text)
    blocks = document.get("blocks")
    if blocks is not None:
        if not isinstance(blocks, list) or not all(isinstance(block, dict)
                and block.get("kind") in {"paragraph", "heading"}
                and isinstance(block.get("text"), str) and block["text"].strip()
                for block in blocks):
            raise PapalTypesetError("blocks must be nonempty paragraph/heading records")
        if "\n\n".join(block["text"] for block in blocks) + "\n" != text:
            raise PapalTypesetError("block wording disagrees with the hashed text payload")
    else:
        blocks = [{"kind": "paragraph", "text": paragraph.strip()}
                  for paragraph in re.split(r"\n\s*\n", text.strip()) if paragraph.strip()]
    keep = document.get("keep_with_next", [])
    if (not isinstance(keep, list) or any(type(index) is not int or not 0 <= index < len(blocks) - 1 for index in keep)
            or keep != sorted(set(keep))):
        raise PapalTypesetError("keep_with_next must contain ordered unique paragraph indices before the final block")
    if document.get("keep_with_next_mode", "paragraph") not in ("paragraph", "first-line"):
        raise PapalTypesetError("keep_with_next_mode must be paragraph or first-line")
    terminal = document.get("terminal_keep_blocks", 0)
    if type(terminal) is not int or not 0 <= terminal <= len(blocks):
        raise PapalTypesetError("terminal_keep_blocks must be a bounded source-block count")
    if type(document.get("compact_layout", False)) is not bool:
        raise PapalTypesetError("compact_layout must be an explicit boolean")
    if type(document.get("allow_long_token_breaks", False)) is not bool:
        raise PapalTypesetError("allow_long_token_breaks must be an explicit boolean")
    if "compact_margin" in document and (not document.get("compact_layout", False)
            or type(document["compact_margin"]) not in (int, float)
            or document["compact_margin"] not in (0.5, 0.55, 0.6, 0.65)):
        raise PapalTypesetError("compact_margin requires compact_layout and a supported 0.5–0.65 inch margin")
    return {**document, "blocks": blocks, "text": text, "artifact_manifest": artifact, "keep_with_next": keep}


def read_manifest(path: Path, root: Path = ROOT, selected=()) -> tuple[dict, list[dict]]:
    try:
        payload = path.read_bytes()
        manifest = json.loads(payload.decode("utf-8"))
    except (OSError, ValueError) as error:
        raise PapalTypesetError("typeset manifest is not readable JSON") from error
    if not isinstance(manifest, dict) or manifest.get("schema") != SCHEMA:
        raise PapalTypesetError(f"typeset manifest requires schema {SCHEMA}")
    _validate_revision(manifest.get("revision"))
    rows = manifest.get("documents")
    if not isinstance(rows, list):
        raise PapalTypesetError("typeset manifest requires a documents array")
    seen = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not isinstance(row.get("language"), str):
            raise PapalTypesetError("typeset manifest has malformed document identity")
        key = (row.get("id"), row.get("language"))
        if key is None or key in seen:
            raise PapalTypesetError("typeset manifest has malformed or duplicate editions")
        seen.add(key)
    unknown = set(selected) - {row.get("id") for row in rows}
    if unknown:
        raise PapalTypesetError("unknown document: " + ", ".join(sorted(unknown)))
    documents = [validate_document(row, root) for row in rows if not selected or row["id"] in selected]
    if not documents:
        raise PapalTypesetError("no admitted document editions selected")
    return _LoadedManifest(manifest, payload), documents


def _manifest_snapshot(manifest: dict, documents: list[dict]) -> bytes:
    payload = getattr(manifest, "input_bytes", None)
    if payload is not None and json.loads(payload.decode("utf-8")) != manifest:
        raise PapalTypesetError("loaded manifest changed after validation; reload the intended input")
    rows = {(row["id"], row["language"]): row for row in manifest["documents"]}
    fields = ("title", "pope", "date", "revision", "language_label", "source_url", "text_path", "sha256",
              "artifact_id", "rights_status", "rights_basis", "rights_notice", "source_note",
              "segment_id", "segment_path", "physical_line_ranges", "range_continuations", "keep_with_next", "keep_with_next_mode",
              "terminal_keep_blocks", "compact_layout", "compact_margin", "allow_long_token_breaks", "blocks")
    defaults = {"keep_with_next": [], "keep_with_next_mode": "paragraph", "terminal_keep_blocks": 0, "compact_layout": False}
    for document in documents:
        row = rows.get((document["id"], document["language"]))
        if row is None:
            raise PapalTypesetError("rendered edition is absent from its input manifest")
        for key in fields:
            if key == "blocks" and key not in row:
                continue  # Derived from the exact retained text during validation.
            if row.get(key, defaults.get(key)) != document.get(key, defaults.get(key)):
                raise PapalTypesetError(f"rendered edition disagrees with its input manifest on {key}")
    return payload if payload is not None else (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def render_body(document: dict, start=0, end=None, include_label=True, no_break_after=False) -> str:
    output = [f"% Source artifact: {document['artifact_id']}", f"% SHA-256: {document['sha256']}"]
    if include_label:
        output.extend([r"\phantomsection", r"\label{" + safe_label(document["id"], document["language"]) + "}"])
    if UNICODE_RUN.search(document["text"]):
        output.append(r"\providecommand{\PapalUnicodeText}[2]{#2}")
    if CYRILLIC_RUN.search(document["text"]):
        output.append(r"\providecommand{\PapalCyrillicFont}{}")
    keep = set(document.get("keep_with_next", []))
    first_line = document.get("keep_with_next_mode", "paragraph") == "first-line"
    for index, block in enumerate(document["blocks"][start:end], start):
        if index in keep and (first_line or index - 1 not in keep):
            output.append(r"\begin{samepage}")
        value = body_tex_escape(block["text"], document.get("allow_long_token_breaks", False))
        output.append(r"\subsection*{" + value + "}" if block["kind"] == "heading" else value + "\n\\par")
        if first_line:
            if index in keep:
                output.extend([r"\end{samepage}", r"\nopagebreak[4]"])
        else:
            if index in keep:
                output.append(r"\nopagebreak[4]")
            elif index - 1 in keep:
                output.append(r"\end{samepage}")
        if no_break_after:
            output.append(r"\nopagebreak[4]")
    return "\n\n".join(output) + "\n"


def render_tex(document: dict, revision: str) -> str:
    revision = document.get("revision", revision)
    stem = output_stem(document)
    title, pope = source_tex_escape(document["title"]), source_tex_escape(document["pope"])
    # PDF string keys accept line breaks, but TeX paragraph tokens are illegal
    # in hypersetup. Collapse only blank lines here; source/display text stays exact.
    metadata_title, metadata_pope = (tex_escape(re.sub(r"\n[ \t\r\n]*\n", " ", document[key]))
                                      for key in ("title", "pope"))
    font_setup = ""
    if any(UNICODE_RUN.search(str(document.get(key, ""))) for key in ("text", "title", "pope", "source_note", "rights_notice", "rights_basis", "language_label")):
        # Native ActualText stays attached to shaped glyphs after line breaking.
        font_setup = (r"\newfontfamily\PapalUnicodeFont[Ligatures=TeXOff]{Junicode}" + "\n"
                      + r"\newcommand{\PapalUnicodeText}[2]{{\PapalUnicodeFont\XeTeXgenerateactualtext=1 #2}}" + "\n")
    if any(CYRILLIC_RUN.search(str(document.get(key, ""))) for key in ("text", "title", "pope", "source_note", "rights_notice", "rights_basis", "language_label")):
        font_setup += r"\newfontfamily\PapalCyrillicFont[Ligatures=TeXOff]{FreeSerif}" + "\n"
    if any(SYMBOL_RUN.search(str(document.get(key, ""))) for key in ("text", "title", "pope", "source_note", "rights_notice", "rights_basis", "language_label")):
        font_setup += r"\newfontfamily\PapalSymbolFont[Ligatures=TeXOff]{FreeSerif}" + "\n"
    language_text = document.get("language_label") or LANGUAGES[document["language"]]
    language, metadata_language = source_tex_escape(language_text), tex_escape(language_text)
    date = document.get("date")
    identification = " · ".join([pope] + ([date] if date else []) + [language])
    pdf_date = "D:" + re.sub(r"[^0-9]", "", revision) + "Z"
    terminal = document.get("terminal_keep_blocks", 0)
    body_input = r"\input{" + stem + ".body.tex}\n"
    terminal_end = ""
    apparatus_keep = ""
    if terminal:
        body_input = (r"\input{" + stem + ".before-ending.tex}\n" + r"\begin{samepage}" + "\n"
                      + r"\input{" + stem + ".ending.tex}\n")
        terminal_end = "\\end{samepage}\n"
        apparatus_keep = "\\nopagebreak[4]\n"
    trailer = "0" * 32
    source = r"""\documentclass[10pt,twocolumn]{article}
\usepackage[letterpaper,margin=0.7in,columnsep=0.26in]{geometry}
\usepackage{fontspec}
\setmainfont[Ligatures=TeXOff]{TeX Gyre Pagella}
""" + font_setup + r"""\usepackage{microtype}
\usepackage[unicode,hidelinks,breaklinks]{hyperref}
\usepackage{xurl}
\setlength{\parindent}{1em}
\setlength{\parskip}{2pt}
\setlength{\emergencystretch}{3em}
\raggedbottom
\hyphenpenalty=10000
\hypersetup{pdftitle={""" + metadata_title + r"""},pdfauthor={""" + metadata_pope + r"""},pdfsubject={Papal source edition; """ + metadata_language + r"""},pdfcreationdate={},pdfmoddate={""" + pdf_date + r"""}}
\special{pdf:trailerid [<""" + trailer + "><" + trailer + r""">]}
\begin{document}
\twocolumn[\begin{center}
{\LARGE\bfseries """ + title + r"""\par}
\medskip
{""" + identification + r"""\par}
\end{center}\bigskip]
\raggedright
\setlength{\parindent}{1em}
""" + body_input + r"""\smallskip
\begingroup\footnotesize\raggedright\setlength{\parindent}{0pt}\setlength{\parskip}{2pt}
\textbf{Source.} \href{""" + tex_escape(document["source_url"]) + r"""}{Open the source witness}. """ + source_tex_escape(document.get("rights_notice", document["rights_basis"])) + " " + source_tex_escape(document.get("source_note", "Text reproduced from the identified source witness. Its wording and numbering are preserved.")) + " Revision: " + revision + r""".

""" + apparatus_keep + r"""\smallskip
\begin{samepage}
Triptych organization and typesetting: CC BY 4.0. Source text retains its own rights. See LICENSE and THIRD\_PARTY.md.
\par\end{samepage}\endgroup
""" + terminal_end + r"""\end{document}
"""
    if document.get("compact_layout", False):
        # A selected layout remedy keeps the body at 10pt and preserves all text.
        margin = format(document.get("compact_margin", 0.65), "g")
        source = source.replace("margin=0.7in,columnsep=0.26in", f"margin={margin}in,columnsep=0.24in", 1)
        source = source.replace(r"\setlength{\parskip}{2pt}", r"\setlength{\parskip}{1pt}", 1)
    identity_body = render_body(document) + (f"\0terminal_keep_blocks={terminal}" if terminal else "")
    identifier = hashlib.sha256((source + "\0" + identity_body).encode("utf-8")).hexdigest()[:32]
    old_line = r"\special{pdf:trailerid [<" + trailer + "><" + trailer + ">]}"
    new_line = r"\special{pdf:trailerid [<" + identifier + "><" + identifier + ">]}"
    return source.replace(old_line, new_line, 1)


def _write_changed(path: Path, content: str):
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def _write_rendered(document: dict, revision: str, folder: Path) -> bool:
    stem = output_stem(document)
    changed = _write_changed(folder / (stem + ".body.tex"), render_body(document))
    terminal = document.get("terminal_keep_blocks", 0)
    if terminal:
        start = len(document["blocks"]) - terminal
        changed = _write_changed(folder / (stem + ".before-ending.tex"), render_body(document, end=start)) or changed
        changed = _write_changed(folder / (stem + ".ending.tex"), render_body(document, start=start, include_label=False, no_break_after=True)) or changed
    return _write_changed(folder / (stem + ".tex"), render_tex(document, revision)) or changed


def pdf_body_fidelity(pdf: Path, document: dict, pages: int) -> dict:
    """Check the whole body in content-stream order, excluding generated page feet."""
    run = subprocess.run(["pdftotext", "-raw", "-enc", "UTF-8", str(pdf), "-"],
                         capture_output=True, text=True, check=True)
    sections = run.stdout.split("\f")
    if sections and not sections[-1].strip():
        sections.pop()
    if len(sections) != pages:
        raise PapalTypesetError("PDF extraction page extent disagrees with pdfinfo")
    body = []
    for number, section in enumerate(sections, 1):
        clean, count = re.subn(r"(?:^|\n)" + str(number) + r"\s*$", "", section)
        if count != 1:
            raise PapalTypesetError(f"generated page footer is absent on page {number}")
        body.append(clean)

    def normalize(value):
        return re.sub(r"\s+", "", unicodedata.normalize("NFKC", value).replace("\u00ad", ""))

    expected = normalize(document["text"])
    normalized_pages = [normalize(page) for page in body]
    actual = "".join(normalized_pages)
    offset = actual.find(expected)
    if offset < 0:
        raise PapalTypesetError("PDF body differs from the complete source text after whitespace/Unicode compatibility normalization")
    source_end = offset + len(expected)
    extent, source_first_page, source_last_page = 0, None, None
    for number, page in enumerate(normalized_pages, 1):
        extent += len(page)
        if source_first_page is None and extent > offset:
            source_first_page = number
        if extent >= source_end:
            source_last_page = number
            break
    if source_first_page != 1:
        raise PapalTypesetError("typeset title creates a page before the complete source body")
    if source_last_page != pages:
        raise PapalTypesetError("terminal apparatus creates a page after the complete source body")
    return {"status": "pass", "method": "pdf-raw-whitespace-soft-hyphen-nfkc-v2", "pages": pages,
            "source_characters": len(document["text"]), "source_normalized_characters": len(expected),
            "source_first_page": source_first_page, "source_last_page": source_last_page}


def _compile(tex: Path, revision: str, document: dict) -> dict:
    revision = document.get("revision", revision)
    engine = shutil.which("xelatex")
    if not engine:
        raise PapalTypesetError("xelatex is unavailable")
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = str(int(dt.datetime.strptime(revision, "%Y-%m-%dT%H:%M:%SZ")
                                     .replace(tzinfo=dt.timezone.utc).timestamp()))
    env["FORCE_SOURCE_DATE"] = "1"
    for pass_number in range(1, 3):
        run = subprocess.run([engine, "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                             cwd=tex.parent, env=env, capture_output=True, text=True, timeout=180)
        (tex.parent / (tex.stem + f".pass-{pass_number}.txt")).write_text(run.stdout + run.stderr, encoding="utf-8")
        if run.returncode:
            raise PapalTypesetError(f"XeLaTeX failed for {tex.stem}; see its pass-{pass_number} log")
    log = tex.with_suffix(".log").read_text(encoding="utf-8", errors="replace")
    warnings = [line.strip() for line in log.splitlines()
                if re.search(r"Overfull \\[hv]box|Underfull \\[hv]box|LaTeX Warning|Missing character", line)]
    severe = [line for line in warnings if "Overfull" in line or "Missing character" in line or "undefined" in line.lower()]
    if severe:
        raise PapalTypesetError(f"unresolved layout or glyph warning for {tex.stem}: {severe[0]}")
    pdf = tex.with_suffix(".pdf")
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True)
    pages = re.search(r"^Pages:\s+(\d+)", info.stdout, re.M)
    if not pages:
        raise PapalTypesetError("pdfinfo did not report a page count")
    page_count = int(pages.group(1))
    fidelity = pdf_body_fidelity(pdf, document, page_count)
    return {"pdf": pdf.name, "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "pages": page_count, "warnings": warnings, "text_fidelity": fidelity}


def _compile_with_layout(tex: Path, revision: str, document: dict) -> dict:
    try:
        return _compile(tex, revision, document)
    except PapalTypesetError as error:
        if "terminal apparatus creates a page" not in str(error):
            raise
    # A short closing source group travels with its apparatus; the full reusable
    # body remains a separate, complete fragment of the same canonical source.
    blocks, count, characters = document["blocks"], 0, 0
    for block in reversed(blocks[-3:]):
        if count and characters + len(block["text"]) > 900:
            break
        count += 1
        characters += len(block["text"])
    start = len(blocks) - count
    while start > 0 and start - 1 in document.get("keep_with_next", []):
        start -= 1
    count = len(blocks) - start
    fitted = {**document, "terminal_keep_blocks": count}
    _write_rendered(fitted, revision, tex.parent)
    result = _compile(tex, revision, fitted)
    result.update(terminal_keep_blocks=count, source_ending_blocks=[start, len(blocks) - 1],
                  support_tex=[f"{tex.parent.name}/{tex.stem}.before-ending.tex", f"{tex.parent.name}/{tex.stem}.ending.tex"],
                  layout="closing-source-with-apparatus")
    return result


def safe_output(path: Path) -> Path:
    resolved = path.resolve()
    if resolved.is_relative_to(ROOT) and not any(resolved.is_relative_to(ROOT / part) for part in (".scratch", "build")):
        raise PapalTypesetError("render output must be beneath .scratch or build, never a publication/source tree")
    return resolved


def render_index(out: Path, documents: list[dict], receipt: dict) -> str:
    """Local metadata navigation; source bodies never enter the batch index."""
    escape = lambda value: html.escape(str(value), quote=True)
    sources = {(document["id"], document["language"]): document for document in documents}
    language_notice = ("Two-column source editions; multilingual witnesses retain their identified languages."
                       if any(document["language"] == "mul" for document in documents)
                       else "Single-language, two-column source editions.")
    rows = []
    for item in receipt["documents"]:
        source = sources.get((item["id"], item["language"]))
        if source is None:
            raise PapalTypesetError("batch receipt names an edition absent from its source manifest")
        links = []
        if item["status"] == "compiled" and (out / item.get("pdf", "")).is_file():
            links.append(f'<a href="{escape(item["pdf"])}">PDF</a>')
        if (out / item["tex"]).is_file():
            links.append(f'<a href="{escape(item["tex"])}">TeX</a>')
        status = escape(item["status"])
        if item.get("error"):
            status += ": " + escape(item["error"])
        fields = [escape(source["title"]), escape(source["pope"]), escape(source.get("date") or "Unknown"),
                  escape(source.get("language_label") or LANGUAGES[source["language"]]), escape(item.get("pages") or "—"),
                  " · ".join(links) or "—", status]
        rows.append("<tr>" + "".join("<td>" + field + "</td>" for field in fields) + "</tr>")
    return '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' + \
        '<title>Papal source editions</title><style>body{font:16px system-ui,sans-serif;margin:2rem;line-height:1.5}table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;padding:.5rem;border-bottom:1px solid #ccc}th{background:#eee}footer{margin-top:2rem;font-size:.9rem}a{color:#14528c}</style></head><body>' + \
        '<h1>Papal source editions</h1><p>' + escape(receipt["summary"]["compiled"]) + ' compiled PDF(s); ' + escape(receipt["summary"]["failed"]) + ' failure(s). <a href="receipt.json">Build receipt</a>.</p>' + \
        '<div style="overflow-x:auto"><table><thead><tr><th>Title</th><th>Pope or issuer</th><th>Date</th><th>Language</th><th>Pages</th><th>Files</th><th>Status</th></tr></thead><tbody>' + \
        "\n".join(rows) + '</tbody></table></div><footer>' + language_notice + ' Historical web transcriptions and OCR retain their recorded limitations; see each PDF’s source note. Source text retains its own rights.</footer></body></html>\n'


def render_documents(manifest: dict, documents: list[dict], out: Path, compile_pdf=False, jobs=1) -> dict:
    snapshot = _manifest_snapshot(manifest, documents)
    out = safe_output(out)
    out.mkdir(parents=True, exist_ok=True)
    snapshot_path = out / "frozen-manifest.json"
    if not snapshot_path.exists() or snapshot_path.read_bytes() != snapshot:
        snapshot_path.write_bytes(snapshot)
    results = []
    for document in documents:
        stem = output_stem(document)
        folder = out / stem
        folder.mkdir(exist_ok=True)
        body, tex = folder / (stem + ".body.tex"), folder / (stem + ".tex")
        changed = _write_rendered(document, manifest["revision"], folder)
        results.append({"id": document["id"], "language": document["language"], "stem": stem,
                        "artifact_id": document["artifact_id"], "source_sha256": document["sha256"],
                        "render_revision": document.get("revision", manifest["revision"]),
                        "tex": f"{stem}/{tex.name}", "body_tex": f"{stem}/{body.name}",
                        "changed": changed, "status": "rendered"})
        for key in ("segment_id", "physical_line_ranges"):
            if key in document:
                results[-1][key] = document[key]
        for key in ("compact_layout", "compact_margin", "allow_long_token_breaks", "range_continuations", "keep_with_next", "keep_with_next_mode", "terminal_keep_blocks"):
            if document.get(key):
                results[-1][key] = document[key]
    errors = []
    if compile_pdf:
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
            pending = {pool.submit(_compile_with_layout, out / item["tex"], manifest["revision"], document): item
                       for item, document in zip(results, documents)}
            for future in concurrent.futures.as_completed(pending):
                item = pending[future]
                try:
                    compiled = future.result()
                    compiled["pdf"] = f"{item['stem']}/{compiled['pdf']}"
                    item.update(compiled, status="compiled")
                except (PapalTypesetError, OSError, subprocess.SubprocessError) as error:
                    item.update(status="failed", error=str(error))
                    errors.append({"id": item["id"], "language": item["language"], "error": str(error)})
    receipt = {"schema": "triptych-papal-typeset-receipt/v1", "revision": manifest["revision"],
               "generator": "typeset-papal", "generator_version": 1,
               "options": {"columns": 2, "body_alignment": "ragged-right", "punctuation": "literal", "automatic_hyphenation": False, "soft_hyphen": "nonprinting", "form_feed": "layout-whitespace", "unicode_text_mapping": "xetex-native"},
               "index": "index.html", "receipt": "receipt.json",
               "input_manifest": "frozen-manifest.json", "input_manifest_sha256": hashlib.sha256(snapshot).hexdigest(),
               "documents": results, "errors": errors,
               "summary": {"selected": len(results), "compiled": sum(item["status"] == "compiled" for item in results), "failed": len(errors)}}
    _write_changed(out / "index.html", render_index(out, documents, receipt))
    _write_changed(out / "receipt.json", json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    return receipt


def main(argv=None, examples=None):
    examples = examples or {}
    parser = argparse.ArgumentParser(prog="typeset-papal", description="Typeset admitted papal source editions in two columns.")
    examples_live_on_the_verbs(parser, "typeset-papal")
    verbs = parser.add_subparsers(dest="verb", required=True)
    for name in ("check", "render"):
        sub = verbs.add_parser(name, description="Validate exact source artifacts" if name == "check" else "Write TeX and optionally compile PDFs",
                               formatter_class=argparse.RawDescriptionHelpFormatter)
        with_examples(sub, examples.get(name, ()))
        sub.add_argument("--manifest", type=Path, default=ROOT / "src/sources/papal-documents/typeset-manifest.json")
        sub.add_argument("--source-root", type=Path, default=ROOT, help="base for repo-relative text payloads")
        sub.add_argument("--document", action="append", default=[], help="exact document id; repeat to select several")
        sub.add_argument("--json", action="store_true")
        if name == "render":
            sub.add_argument("--out", type=Path, default=ROOT / ".scratch/papal-typeset")
            sub.add_argument("--compile", action="store_true", dest="compile_pdf")
            sub.add_argument("--jobs", type=int, choices=range(1, 9), default=1)
    collect = verbs.add_parser("collect", description="Collect verified local reader batches and exact review/supersession records",
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    with_examples(collect, examples.get("collect", ()))
    collect_inputs = collect.add_mutually_exclusive_group(required=True)
    collect_inputs.add_argument("--batch", action="append", nargs=3, metavar=("NAME", "RECEIPT", "MANIFEST"))
    collect_inputs.add_argument("--empty-plan", type=Path, help="validated source plan with zero active selections")
    collect.add_argument("--supersessions", action="append", type=Path, default=[])
    collect.add_argument("--review", action="append", type=Path, default=[])
    collect.add_argument("--out", type=Path, default=ROOT / ".scratch/papal-collection")
    collect.add_argument("--json", action="store_true")
    plan = verbs.add_parser("plan", description="Resolve current source selections before rendering",
                            formatter_class=argparse.RawDescriptionHelpFormatter)
    with_examples(plan, examples.get("plan", ()))
    plan.add_argument("--base", action="append", nargs=2, required=True, metavar=("NAME", "MANIFEST"))
    plan.add_argument("--correction", action="append", nargs=2, default=[], metavar=("NAME", "MANIFEST"))
    plan.add_argument("--out", type=Path, default=ROOT / ".scratch/papal-pdfs/current-manifest.json")
    plan.add_argument("--json", action="store_true")
    prepare_install = verbs.add_parser("prepare-install", description="Prepare exact current, fully page-reviewed PDFs for inspection before installation",
                                       formatter_class=argparse.RawDescriptionHelpFormatter)
    with_examples(prepare_install, examples.get("prepare-install", ()))
    prepare_install.add_argument("--plan", type=Path, required=True)
    prepare_install.add_argument("--batch-pairs", type=Path, required=True)
    prepare_install.add_argument("--review", action="append", type=Path, default=[])
    prepare_install.add_argument("--out", type=Path, default=ROOT / ".scratch/papal-install/prepared.json")
    prepare_install.add_argument("--json", action="store_true")
    install = verbs.add_parser("install", description="Install a reviewed preparation after revalidating its exact current inputs",
                               formatter_class=argparse.RawDescriptionHelpFormatter)
    with_examples(install, examples.get("install", ()))
    install.add_argument("--prepared", type=Path, required=True)
    install.add_argument("--json", action="store_true")
    check_install = verbs.add_parser("check-install", description="Check installed PDF bytes, durable evidence and current source selections",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    with_examples(check_install, examples.get("check-install", ()))
    check_install.add_argument("--plan", type=Path, required=True)
    check_install.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.verb in {"prepare-install", "install", "check-install"}:
            from _papal_install import prepare_install, install_prepared, check_install, RELEASE
            from _papal_collection import PapalCollectionError
            try:
                if args.verb == "prepare-install":
                    prepared = prepare_install(args.plan, args.batch_pairs, args.out, args.review)
                    payload = {"schema": prepared["schema"], "summary": prepared["summary"],
                               "prepared": os.path.relpath(args.out.resolve(), ROOT),
                               "sha256": hashlib.sha256(args.out.read_bytes()).hexdigest()}
                elif args.verb == "install":
                    released = install_prepared(args.prepared)
                    payload = {"schema": released["schema"], "summary": released["summary"],
                               "release": RELEASE.as_posix()}
                else:
                    payload = check_install(args.plan)
            except PapalCollectionError as error:
                raise PapalTypesetError(str(error)) from error
        elif args.verb in {"collect", "plan"}:
            from _papal_collection import collect_batches, plan_sources, PapalCollectionError
            try:
                if args.verb == "collect":
                    if args.empty_plan:
                        from _papal_collection import collect_empty_plan
                        if args.supersessions or args.review:
                            raise PapalTypesetError("empty-plan collection takes its exclusions from the validated plan")
                        payload = collect_empty_plan(args.empty_plan, safe_output(args.out))
                    else:
                        batches = [{"name": name, "receipt": Path(receipt), "manifest": Path(manifest)}
                                   for name, receipt, manifest in args.batch]
                        payload = collect_batches(batches, safe_output(args.out), args.supersessions, args.review)
                else:
                    out = safe_output(args.out)
                    planned = plan_sources([{ "name": name, "path": Path(path)} for name, path in args.base],
                                           [{ "name": name, "path": Path(path)} for name, path in args.correction], out)
                    payload = {"schema": "triptych-papal-source-plan/v1", "summary": planned["selection_plan"]["summary"],
                               "manifest": os.path.relpath(out, ROOT), "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}
            except PapalCollectionError as error:
                raise PapalTypesetError(str(error)) from error
        else:
            manifest, documents = read_manifest(args.manifest, args.source_root.resolve(), args.document)
            if args.verb == "check":
                payload = {"schema": SCHEMA, "selected": len(documents), "status": "valid"}
            else:
                payload = render_documents(manifest, documents, args.out, args.compile_pdf, args.jobs)
        if args.json:
            print(json.dumps({**payload, "v": 1}, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        elif args.verb == "check":
            print(f"valid: {len(documents)} admitted source editions")
        elif args.verb == "collect":
            summary = payload["summary"]
            print(f"collected: {summary['documents']} source editions; {summary['compiled']} compiled PDFs; {summary['layout_reviewed']} layout reviewed")
        elif args.verb == "plan":
            print(f"planned: {payload['summary']['selected']} current source editions; {payload['summary']['excluded']} obsolete selections excluded")
        elif args.verb in {"prepare-install", "install"}:
            print(f"{'prepared' if args.verb == 'prepare-install' else 'installed'}: {payload['summary']['ready']} reviewed PDFs; {payload['summary']['current']} current source editions")
        elif args.verb == "check-install":
            print(f"{payload['status']}: {payload['installed']} installed PDFs; {payload['current']} current source editions; {payload['not_installed']} not installed")
        else:
            for item in payload["documents"]:
                print(f"{item['id']} ({item['language']}): {item['status']}")
        return 1 if payload.get("errors") else 0
    except (PapalTypesetError, OSError) as error:
        if args.json:
            print(json.dumps({"code": "input", "error": str(error), "status": "error", "v": 1}, sort_keys=True, separators=(",", ":")), file=sys.stderr)
        else:
            print(f"typeset-papal: {error}", file=sys.stderr)
        return 2
