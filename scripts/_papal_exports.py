"""Metadata-only exports of the papal catalog for citations and presentations."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from datetime import date
from typing import Any
from urllib.parse import urlsplit


EXPORT_SCHEMA = "triptych-papal-export/v1"
FORMATS = ("json", "csv", "biblatex", "beamer")
CSV_FIELDS = (
    "id", "record_kind", "citation_key", "pope", "responsible", "title", "date", "document_type",
    "source_document_type", "document_types", "record_role", "resolved_date", "resolved_title", "language", "source_url",
)
LANGUAGES = {
    "en": "English", "la": "Latin", "it": "Italian", "fr": "French",
    "de": "German", "es": "Spanish", "pt": "Portuguese", "pl": "Polish",
}
ROLE_NOTES = {
    "composite": "Compound source delivery containing multiple documents",
    "constituent": "Constituent of a larger work or document package",
    "index-mislink": "Index label differs from the delivered document",
}


def citation_key(document_id: str, language: str) -> str:
    """Keep a citation stable when its title, date or delivery URL is corrected."""
    if not document_id or not re.fullmatch(r"[a-z][a-z0-9_-]*", language):
        raise ValueError("a citation requires a document id and a language code")
    stem = re.sub(r"[^a-z0-9]+", "-", document_id.lower()).strip("-")[:64]
    digest = hashlib.sha256(f"{document_id}\0{language}".encode()).hexdigest()[:16]
    return f"{stem or 'papal'}-{language}-{digest}"


def tex_escape(value: Any) -> str:
    """Treat catalog strings as text, including braces and TeX commands."""
    replacements = {
        "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}",
        "$": r"\$", "&": r"\&", "#": r"\#", "%": r"\%",
        "_": r"\_", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(c, c) for c in str(value).replace("\r", " ").replace("\n", " "))


def source_url(value: Any) -> str:
    """Only an ordinary absolute web URL may enter a generated TeX command."""
    value = str(value)
    parsed = urlsplit(value)
    if (parsed.scheme not in ("http", "https") or not parsed.netloc
            or parsed.username or parsed.password
            or any(c.isspace() or c in "{}\\" for c in value)):
        raise ValueError(f"invalid source URL: {value!r}")
    return value


def _documents(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    raw = catalog.get("documents")
    if not isinstance(raw, list):
        raise ValueError("catalog.documents must be an array")
    documents, seen = [], set()
    for item in raw:
        if not isinstance(item, dict):
            raise ValueError("every catalog document must be an object")
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier or identifier in seen:
            raise ValueError("catalog document ids must be nonempty and unique")
        seen.add(identifier)
        languages = item.get("languages")
        if not isinstance(languages, dict):
            raise ValueError(f"{identifier}: languages must be an object")
        document = {
            key: item.get(key) for key in
            ("id", "pope_id", "pope", "title", "date", "document_type")
        }
        for key in ("source_index_urls", "date_raw", "date_basis", "date_conflicts",
                    "index_titles", "index_title_raw", "identity_aliases", "url_aliases",
                    "edition_url_aliases", "language_url_conflicts", "document_types",
                    "document_type_conflicts", "record_role", "constituents", "issues",
                    "body_language_conflicts", "resolved_date", "date_resolution",
                    "resolved_title", "title_resolution", "source_unit_identity", "source_work_type",
                    "source_responsible", "display_responsible", "parent_work_id",
                    "source_work_id", "delivery_ownership"):
            if key in item:
                document[key] = item[key]
        for key in ("pope", "title", "document_type"):
            if not isinstance(document[key], str) or not document[key].strip():
                raise ValueError(f"{identifier}: {key} must be nonempty text")
        document["responsible"] = document.get("source_responsible", document["pope"])
        for field in ("date", "resolved_date"):
            value = document.get(field)
            if value is not None:
                if (not isinstance(value, str)
                        or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)):
                    raise ValueError(f"{identifier}: {field} must be ISO text or null")
                date.fromisoformat(value)
        document["languages"] = {}
        for language, url in sorted(languages.items()):
            citation_key(identifier, language)
            document["languages"][language] = source_url(url)
        documents.append(document)
    return sorted(documents, key=lambda d: (d.get("resolved_date") or d["date"] or "9999", d["pope"], d["id"]))


def _rows(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    rows, keys = [], set()
    for document in _documents(catalog):
        for language, url in document["languages"].items() or [(None, "")]:
            key = citation_key(document["id"], language or "und")
            if key in keys:
                raise ValueError(f"citation-key collision: {key}")
            keys.add(key)
            rows.append({
                **{field: document[field] for field in
                   ("id", "pope", "title", "date", "document_type")},
                "citation_key": key, "language": language, "source_url": url,
                "record_kind": "edition" if language else "work",
                "document_types": "; ".join(document.get("document_types", [document["document_type"]])),
                "record_role": document.get("record_role", "unreviewed-index-record"),
                "resolved_date": document.get("resolved_date"),
                "responsible": document["responsible"],
                "source_document_type": document["document_type"],
                "document_type": document.get("source_work_type", document["document_type"]),
                "resolved_title": document.get("resolved_title"),
            })
    return rows


def catalog_json(catalog: dict[str, Any]) -> str:
    """Export a deliberately closed metadata surface, with no cached text."""
    coverage_fields = (
        "url", "retrieved_on", "status", "http_status", "final_url", "sha256",
        "byte_size", "pope_id", "interface", "rows", "navigation_root",
        "index_links_followed", "error",
    )
    coverage = [
        {key: page[key] for key in coverage_fields if key in page}
        for page in catalog.get("coverage", [])
    ]
    return json.dumps({"schema": EXPORT_SCHEMA, "scope": catalog.get("scope"),
                       "retrieved_on": catalog.get("retrieved_on"),
                       "coverage": coverage, "documents": _documents(catalog),
                       "editions": [row for row in _rows(catalog) if row["record_kind"] == "edition"]},
                      ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def catalog_csv(catalog: dict[str, Any]) -> str:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=CSV_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(_rows(catalog))
    return output.getvalue()


def catalog_biblatex(catalog: dict[str, Any]) -> str:
    entries = []
    for row in _rows(catalog):
        fields = [
            ("author", "{" + tex_escape(row["responsible"]) + "}"),
            ("title", tex_escape(row["resolved_title"] or row["title"])),
            ("type", tex_escape(row["document_type"].replace("-", " "))),
        ]
        if row["language"]:
            fields.append(("language", LANGUAGES.get(row["language"], row["language"]).lower()))
            fields.append(("url", row["source_url"]))
        if row["resolved_date"] or row["date"]:
            fields.append(("date", row["resolved_date"] or row["date"]))
        if row["record_role"] in ROLE_NOTES:
            fields.append(("note", tex_escape(ROLE_NOTES[row["record_role"]])))
        kind = "online" if row["language"] else "misc"
        entries.append("@" + kind + "{" + row["citation_key"] + ",\n" +
                       "\n".join(f"  {key} = {{{value}}}," for key, value in fields) + "\n}")
    return "\n\n".join(entries) + ("\n" if entries else "")


def catalog_beamer(catalog: dict[str, Any], language: str = "en") -> str:
    """One source-link card per index record, preserving reviewed source roles."""
    if not re.fullmatch(r"[a-z][a-z0-9_-]*", language):
        raise ValueError("invalid preferred language")
    lines = [
        r"\documentclass[aspectratio=169]{beamer}",
        r"\usepackage{fontspec}", r"\setmainfont{Latin Modern Roman}",
        r"\setbeamertemplate{navigation symbols}{}", r"\begin{document}",
    ]
    for document in _documents(catalog):
        available = document["languages"]
        selected = next((lang for lang in (language, "en", "la", "it") if lang in available), next(iter(available), None))
        key = citation_key(document["id"], selected or "und")
        role = document.get("record_role")
        title = document.get("resolved_title") or document["title"]
        if role == "composite":
            title = "Compound source delivery"
        lines += [
            f"% citation key: {key}",
            r"\begin{frame}",
            r"\frametitle{\small " + tex_escape(title) + "}",
            r"\label{papal-card:" + key + "}",
            tex_escape(document["responsible"]) + r"\par\medskip",
            tex_escape(document.get("source_work_type", document["document_type"]).replace("-", " ").capitalize()) +
            " · " + tex_escape(document.get("resolved_date") or document["date"] or "Date unresolved") + r"\par\medskip",
        ]
        if role in ROLE_NOTES:
            lines.append(r"{\small " + tex_escape(ROLE_NOTES[role]) + r"\par}")
        if role == "composite":
            labels = [item.get("title") or item.get("subject")
                      for item in document.get("constituents", []) if isinstance(item, dict)]
            if labels and all(isinstance(label, str) and label for label in labels):
                lines.append(r"{\small " + tex_escape("; ".join(labels)) + r"\par\medskip}")
            else:
                lines.append(r"{\small Index label: " + tex_escape(document["title"]) + r"\par\medskip}")
        if selected:
            lines.append(r"\href{" + tex_escape(available[selected]) + "}{Read the " +
                         tex_escape(LANGUAGES.get(selected, selected)) + r" source}\par")
        else:
            lines.append(r"Source link unavailable\par")
        lines.append(r"\end{frame}")
    return "\n".join(lines + [r"\end{document}", ""])


def export_catalog(catalog: dict[str, Any], format: str, language: str = "en") -> str:
    exporters = {"json": catalog_json, "csv": catalog_csv, "biblatex": catalog_biblatex}
    if format == "beamer":
        return catalog_beamer(catalog, language)
    if format not in exporters:
        raise ValueError(f"unsupported export format: {format}")
    return exporters[format](catalog)
