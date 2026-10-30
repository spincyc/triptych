#!/usr/bin/env python3
"""The encyclicals catalogue the `/encyclicals/` page reads, and its gate.

One tracked source, `src/sources/papal-documents/encyclicals-index.json`, names
every encyclical the project lists: one row each, with its pope, date, incipit,
an AI-written one-line description, the installed two-column reading PDFs by
language and the Vatican page. This module checks that file against its schema
and against `release/papal-documents.json`, and writes the one data file the
browser fetches, `src/web/data/encyclicals/index.json`.

The v2 index also records existing external English translations in
`english_routes`, independently of local source readers and their distribution
basis. Each route names its source, authority, checked date, extent and review
qualification. Only an explicitly complete English reader or route counts as
complete English; fragments, damaged texts and unreviewed extents remain gaps.
The external route never adds an installed PDF or changes a source-rights claim.

Three things it refuses, because a catalogue that quietly repairs its input is
a catalogue nobody can trust:

* A reader that is not exactly a row of the release record. Its id, language,
  path, SHA-256 and page count are compared field by field, and the release row
  must still be a reviewed (`PASS`), public-domain installation. A PDF the
  release record does not own is not a PDF this page may link.
* A row whose availability is unstated. A row with no reader must say why no
  local text is offered (after 1930, or no qualifying printing acquired), and a
  row with readers must not carry such a reason.
* A description that could pass for the Pope's words without saying whose they
  are. Each row names the basis it was written from, and the file names its
  author, method and date once in `description_provenance`; the page prints both.

The output adds nothing the index does not state except arithmetic: the pope
list, the language list and the counts are derived here so the page does not
derive them a second way. `structure --check` asks whether the tracked file is
still what the index and the release record produce, and writes nothing.

Usage::

    python3 scripts/_encyclicals.py check     [--index PATH] [--release PATH]
    python3 scripts/_encyclicals.py structure [--index PATH] [--release PATH]
                                              [--out DATA_ROOT] [--check]
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
INDEX_RELATIVE = Path("src/sources/papal-documents/encyclicals-index.json")
RELEASE_RELATIVE = Path("release/papal-documents.json")
DATA_ROOT_RELATIVE = Path("src/web/data")
OUTPUT_RELATIVE = Path("encyclicals/index.json")

INDEX_SCHEMA = "triptych-encyclicals-index/v2"
OUTPUT_SCHEMA = "triptych-encyclicals-browser/v2"
RELEASE_SCHEMA = "triptych-papal-release/v1"

ROW_FIELDS = frozenset((
    "id", "pope", "pope_id", "pontificate_index", "date", "year", "title",
    "subject", "description", "description_basis", "readers", "links",
    "no_local_text_reason",
    "english_routes",
))
READER_FIELDS = frozenset((
    "language", "release_id", "pdf", "pdf_sha256", "pages", "witness", "extent",
))
PROVENANCE_FIELDS = frozenset(("author", "method", "written_on"))
ENGLISH_ROUTE_FIELDS = frozenset((
    "url", "label", "language", "extent", "authority", "checked_on",
    "source_index_url", "verification_note",
))
EXTENTS = ("complete", "fragment", "damaged")
DESCRIPTION_LIMIT = 160

# The language a reader is set in, as the page names it. A code missing here is
# refused rather than printed bare: a column headed "pt" is a column nobody can
# read. Latin and English lead because the page is about them; the rest follow
# in code order.
LANGUAGE_LABELS = {
    "la": "Latin",
    "en": "English",
    "de": "German",
    "el": "Greek",
    "es": "Spanish",
    "fr": "French",
    "it": "Italian",
    "mul": "Several languages",
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
}
LEADING_LANGUAGES = ("la", "en")

ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*[a-z0-9]$")
POPE_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
REVISION_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PDF_RE = re.compile(r"^pdf/papal-documents/[a-z0-9][a-z0-9.-]*\.pdf$")
VATICAN_RE = re.compile(r"^https://www\.vatican\.va/[^\s]*$")
BASIS_RE = re.compile(r"^(local-reader|vatican-page|other):(\S+)$")
HTTPS_RE = re.compile(r"^https://[^\s/]+/?\S*$")


class EncyclicalsError(Exception):
    """The index, the release record or the tracked output is not usable."""


def _shown(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError(f"invalid JSON number {value}")


def read_json(path: Path, label: str) -> tuple[object, bytes]:
    """Parse strictly: duplicate keys and NaN are refused, not resolved."""
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise EncyclicalsError(f"cannot read {label}: {error}") from error
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_invalid_constant,
        )
    except (UnicodeError, ValueError) as error:
        raise EncyclicalsError(f"{label} is not valid JSON: {error}") from error
    return value, raw


def release_documents(path: Path, label: str) -> dict[tuple[str, str], dict]:
    """The installed papal readers, by release id and language.

    The id alone is not an identity: an act installed in Latin and in a
    historical English translation is one id with two rows.
    """
    release, _raw = read_json(path, label)
    if not isinstance(release, dict) or release.get("schema") != RELEASE_SCHEMA:
        raise EncyclicalsError(f"{label} is not a {RELEASE_SCHEMA} record")
    documents = release.get("documents")
    if not isinstance(documents, list):
        raise EncyclicalsError(f"{label} has no documents list")
    found: dict[tuple[str, str], dict] = {}
    for position, document in enumerate(documents):
        if (
            not isinstance(document, dict)
            or not isinstance(document.get("id"), str)
            or not isinstance(document.get("language"), str)
        ):
            raise EncyclicalsError(f"{label} documents[{position}] has no id and language")
        key = (document["id"], document["language"])
        if key in found:
            raise EncyclicalsError(f"{label} records {key[0]!r} in {key[1]!r} twice")
        found[key] = document
    return found


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and value == value.strip()


def _valid_date(value: str) -> bool:
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _https_url(value: object) -> bool:
    if not isinstance(value, str) or not HTTPS_RE.fullmatch(value):
        return False
    try:
        parsed = urlsplit(value)
        return bool(parsed.hostname) and parsed.username is None and parsed.password is None
    except ValueError:
        return False


def _check_english_route(errors: list[str], where: str, route: object) -> None:
    if not isinstance(route, dict) or set(route) != ENGLISH_ROUTE_FIELDS:
        errors.append(f"{where}: English route fields differ from the schema")
        return
    for field in ("url", "source_index_url"):
        if not _https_url(route[field]):
            errors.append(f"{where}: {field} must be an https URL without credentials")
    for field in ("label", "verification_note"):
        if not _text(route[field]) or "\n" in route[field]:
            errors.append(f"{where}: {field} must be a stated single line")
    if route["language"] != "en":
        errors.append(f"{where}: an English route must have language 'en'")
    if route["extent"] not in EXTENTS + ("unreviewed",):
        errors.append(f"{where}: extent must be complete, fragment, damaged or unreviewed")
    if route["authority"] not in ("official", "third-party"):
        errors.append(f"{where}: authority must be official or third-party")
    elif route["authority"] == "official" and (
        not _https_url(route["url"]) or urlsplit(route["url"]).hostname != "www.vatican.va"
    ):
        errors.append(f"{where}: an official route must be on www.vatican.va")
    checked = route["checked_on"]
    if not isinstance(checked, str) or not DATE_RE.fullmatch(checked) or not _valid_date(checked):
        errors.append(f"{where}: checked_on must be a YYYY-MM-DD date")


def _check_reader(
    errors: list[str], where: str, reader: object, documents: dict[tuple[str, str], dict]
) -> None:
    if not isinstance(reader, dict):
        errors.append(f"{where}: a reader must be an object")
        return
    fields = set(reader)
    if fields != READER_FIELDS:
        missing = sorted(READER_FIELDS - fields)
        extra = sorted(fields - READER_FIELDS)
        errors.append(f"{where}: reader fields differ from the schema: missing={missing}, extra={extra}")
        return
    language = reader["language"]
    if language not in LANGUAGE_LABELS:
        errors.append(
            f"{where}: language {language!r} has no reader-facing label; add it to "
            "LANGUAGE_LABELS in scripts/_encyclicals.py"
        )
    if not isinstance(reader["pdf"], str) or not PDF_RE.fullmatch(reader["pdf"]):
        errors.append(f"{where}: pdf must name a file under pdf/papal-documents/: {reader['pdf']!r}")
    if not isinstance(reader["pdf_sha256"], str) or not SHA256_RE.fullmatch(reader["pdf_sha256"]):
        errors.append(f"{where}: pdf_sha256 must be 64 lowercase hex digits")
    if not _is_int(reader["pages"]) or reader["pages"] < 1:
        errors.append(f"{where}: pages must be a positive integer")
    if not _text(reader["witness"]) or "\n" in reader["witness"]:
        errors.append(f"{where}: witness must be a one-line printed-source label")
    if reader["extent"] not in EXTENTS:
        errors.append(f"{where}: extent must be one of {', '.join(EXTENTS)}")
    release_id = reader["release_id"]
    document = (
        documents.get((release_id, language))
        if isinstance(release_id, str) and isinstance(language, str)
        else None
    )
    if document is None:
        errors.append(
            f"{where}: {release_id!r} in {language!r} is not a document of "
            f"{RELEASE_RELATIVE.as_posix()}; only installed readers may be linked"
        )
        return
    for field in ("pdf", "pdf_sha256", "pages"):
        if document.get(field) != reader[field]:
            errors.append(
                f"{where}: {field} {reader[field]!r} does not match the release record's "
                f"{document.get(field)!r} for {release_id}"
            )
    review = document.get("review")
    if not isinstance(review, dict) or review.get("status") != "PASS":
        errors.append(f"{where}: release record shows no PASS review for {release_id}")
    source = document.get("source")
    if not isinstance(source, dict) or source.get("rights_status") != "public-domain":
        errors.append(
            f"{where}: release record gives {release_id} no public-domain distribution basis"
        )


def validate_index(index: object, documents: dict[tuple[str, str], dict]) -> list[str]:
    """Every way the index fails its schema or the release record, in order."""
    errors: list[str] = []
    if not isinstance(index, dict):
        return ["the encyclicals index must be a JSON object"]
    expected_top = {"schema", "revision", "scope", "description_provenance", "encyclicals"}
    if set(index) != expected_top:
        errors.append(
            "top-level fields differ from the schema: "
            f"missing={sorted(expected_top - set(index))}, extra={sorted(set(index) - expected_top)}"
        )
    if index.get("schema") != INDEX_SCHEMA:
        errors.append(f"schema must be {INDEX_SCHEMA!r}")
    revision = index.get("revision")
    if not isinstance(revision, str) or not REVISION_RE.fullmatch(revision):
        errors.append("revision must be a UTC whole-second timestamp such as 2026-10-28T00:00:00Z")
    if not _text(index.get("scope")):
        errors.append("scope must be a non-empty paragraph")
    provenance = index.get("description_provenance")
    if not isinstance(provenance, dict) or set(provenance) != PROVENANCE_FIELDS:
        errors.append("description_provenance must hold exactly author, method and written_on")
    else:
        for field in ("author", "method"):
            if not _text(provenance[field]):
                errors.append(f"description_provenance.{field} must be stated")
        written = provenance["written_on"]
        if not isinstance(written, str) or not DATE_RE.fullmatch(written) or not _valid_date(written):
            errors.append("description_provenance.written_on must be a YYYY-MM-DD date")
    rows = index.get("encyclicals")
    if not isinstance(rows, list) or not rows:
        errors.append("encyclicals must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    popes: dict[str, tuple[str, int]] = {}
    pope_by_index: dict[int, str] = {}
    previous_key: tuple | None = None
    latest_pontificate_by_date: list[tuple[str, int, str]] = []
    for position, row in enumerate(rows):
        where = f"encyclicals[{position}]"
        if not isinstance(row, dict):
            errors.append(f"{where}: a row must be an object")
            continue
        fields = set(row)
        if fields != ROW_FIELDS:
            errors.append(
                f"{where}: fields differ from the schema: "
                f"missing={sorted(ROW_FIELDS - fields)}, extra={sorted(fields - ROW_FIELDS)}"
            )
            continue
        identity = row["id"]
        if not isinstance(identity, str) or not ID_RE.fullmatch(identity):
            errors.append(f"{where}: id must be a lowercase stable identifier: {identity!r}")
        elif identity in seen_ids:
            errors.append(f"{where}: id {identity!r} is listed twice; one encyclical, one row")
        else:
            seen_ids.add(identity)
            where = f"{where} ({identity})"
        if not _text(row["pope"]):
            errors.append(f"{where}: pope must be named")
        pope_id = row["pope_id"]
        if not isinstance(pope_id, str) or not POPE_ID_RE.fullmatch(pope_id):
            errors.append(f"{where}: pope_id must be a slug: {pope_id!r}")
        pontificate = row["pontificate_index"]
        if not _is_int(pontificate):
            errors.append(f"{where}: pontificate_index must be an integer")
        elif isinstance(pope_id, str) and _text(row["pope"]):
            known = popes.setdefault(pope_id, (row["pope"], pontificate))
            if known != (row["pope"], pontificate):
                errors.append(
                    f"{where}: pope_id {pope_id!r} is {known[0]!r} at pontificate "
                    f"{known[1]} elsewhere, not {row['pope']!r} at {pontificate}"
                )
            holder = pope_by_index.setdefault(pontificate, pope_id)
            if holder != pope_id:
                errors.append(
                    f"{where}: pontificate_index {pontificate} already belongs to {holder!r}"
                )
        date = row["date"]
        year = row["year"]
        if date is not None:
            if not isinstance(date, str) or not DATE_RE.fullmatch(date) or not _valid_date(date):
                errors.append(f"{where}: date must be YYYY-MM-DD or null: {date!r}")
                date = None
            elif year != int(date[:4]):
                errors.append(f"{where}: year {year!r} does not match date {date}")
        if year is not None and not _is_int(year):
            errors.append(f"{where}: year must be an integer or null")
        if not _text(row["title"]):
            errors.append(f"{where}: title must be the incipit")
        if row["subject"] is not None and not _text(row["subject"]):
            errors.append(f"{where}: subject must be text or null, never empty")
        # A description not yet written is null, and the page leaves its cell
        # blank; a description that is present must be one short line.
        description = row["description"]
        if description is None:
            pass
        elif not _text(description) or "\n" in description:
            errors.append(f"{where}: description must be one line of plain English or null")
        elif len(description) > DESCRIPTION_LIMIT:
            errors.append(
                f"{where}: description is {len(description)} characters; the limit is "
                f"{DESCRIPTION_LIMIT}"
            )
        readers = row["readers"]
        reader_ids: list[str] = []
        reader_keys: set[tuple] = set()
        if not isinstance(readers, list):
            errors.append(f"{where}: readers must be a list")
            readers = []
        for reader_position, reader in enumerate(readers):
            reader_where = f"{where} readers[{reader_position}]"
            _check_reader(errors, reader_where, reader, documents)
            if isinstance(reader, dict) and isinstance(reader.get("release_id"), str):
                key = (reader["release_id"], reader.get("language"))
                if key in reader_keys:
                    errors.append(f"{reader_where}: {key[0]} in {key[1]!r} is listed twice")
                reader_keys.add(key)
                reader_ids.append(reader["release_id"])
        routes = row["english_routes"]
        if not isinstance(routes, list):
            errors.append(f"{where}: english_routes must be a list")
        else:
            seen_routes = set()
            for route_position, route in enumerate(routes):
                route_where = f"{where} english_routes[{route_position}]"
                _check_english_route(errors, route_where, route)
                url = route.get("url") if isinstance(route, dict) else None
                if isinstance(url, str):
                    if url in seen_routes:
                        errors.append(f"{route_where}: duplicate english_routes identity {url!r}")
                    seen_routes.add(url)
        basis = row["description_basis"]
        match = BASIS_RE.fullmatch(basis) if isinstance(basis, str) else None
        if description is None and basis is None:
            pass
        elif description is None:
            errors.append(f"{where}: description_basis names a basis for a description that is null")
        elif match is None:
            errors.append(
                f"{where}: description_basis must be local-reader:<release id>, "
                "vatican-page:<url> or other:<url>"
            )
        elif match.group(1) == "local-reader" and match.group(2) not in reader_ids:
            errors.append(
                f"{where}: description_basis names reader {match.group(2)!r}, which is "
                "not one of this row's readers"
            )
        elif match.group(1) != "local-reader" and not HTTPS_RE.fullmatch(match.group(2)):
            errors.append(f"{where}: description_basis must cite an https URL")
        links = row["links"]
        if not isinstance(links, dict) or set(links) != {"vatican"}:
            errors.append(f"{where}: links must hold exactly vatican")
        elif links["vatican"] is not None and (
            not isinstance(links["vatican"], str) or not VATICAN_RE.fullmatch(links["vatican"])
        ):
            errors.append(f"{where}: links.vatican must be an https://www.vatican.va/ URL or null")
        reason = row["no_local_text_reason"]
        if readers and reason is not None:
            errors.append(f"{where}: a row with readers must not carry no_local_text_reason")
        if not readers and not _text(reason):
            errors.append(
                f"{where}: a row with no reader must say why no local text is offered"
            )
        # Date order, then undated rows in pontificate order: the index is
        # the reading order, so it is checked here rather than sorted into
        # shape where nobody would see that it was not.
        if _is_int(pontificate):
            key = (0, date, 0) if date is not None else (1, "", pontificate)
            if previous_key is not None and key < previous_key:
                errors.append(
                    f"{where}: out of order; rows run by date, then undated rows by pontificate"
                )
            previous_key = key
            if date is not None:
                latest_pontificate_by_date.append((date, pontificate, where))
    # A pope's encyclicals cannot predate his predecessor's. Read in date order
    # the pontificate index never falls, and one that does is a mistyped date
    # or a mistyped index; either way the pope sort would lie.
    highest = None
    for date, pontificate, where in latest_pontificate_by_date:
        if highest is not None and pontificate < highest[0]:
            errors.append(
                f"{where}: dated {date} under pontificate {pontificate}, after "
                f"{highest[2]} under pontificate {highest[0]}"
            )
        if highest is None or pontificate >= highest[0]:
            highest = (pontificate, date, where)
    return errors


def language_order(codes: set[str]) -> list[str]:
    leading = [code for code in LEADING_LANGUAGES if code in codes]
    return leading + sorted(code for code in codes if code not in LEADING_LANGUAGES)


def english_availability(row: dict) -> dict[str, bool]:
    sources = [reader for reader in row["readers"] if reader["language"] == "en"]
    external = row["english_routes"]
    source_complete = any(reader["extent"] == "complete" for reader in sources)
    external_complete = any(route["extent"] == "complete" for route in external)
    complete = source_complete or external_complete
    any_english = bool(sources or external)
    return {"complete": complete, "source_complete": source_complete,
            "external_complete": external_complete,
            "incomplete_only": any_english and not complete, "unavailable": not any_english}


def browser_catalogue(index: dict, index_bytes: bytes) -> dict:
    """What the page fetches: the index rows, plus arithmetic over them."""
    rows = index["encyclicals"]
    popes: dict[str, dict] = {}
    languages: dict[str, dict] = {}
    with_text = 0
    pages = 0
    reader_count = 0
    english = dict.fromkeys(("complete", "source_complete",
                             "external_complete", "incomplete_only", "unavailable"), 0)
    english.update({"source_readers": 0, "external_routes": 0})
    for row in rows:
        for field, present in english_availability(row).items():
            english[field] += int(present)
        english["source_readers"] += sum(reader["language"] == "en" for reader in row["readers"])
        english["external_routes"] += len(row["english_routes"])
        entry = popes.setdefault(row["pope_id"], {
            "id": row["pope_id"],
            "name": row["pope"],
            "pontificate_index": row["pontificate_index"],
            "encyclicals": 0,
            "with_local_text": 0,
        })
        entry["encyclicals"] += 1
        if row["readers"]:
            entry["with_local_text"] += 1
            with_text += 1
        seen_here: set[str] = set()
        for reader in row["readers"]:
            reader_count += 1
            pages += reader["pages"]
            language = languages.setdefault(reader["language"], {
                "code": reader["language"],
                "label": LANGUAGE_LABELS[reader["language"]],
                "readers": 0,
                "encyclicals": 0,
            })
            language["readers"] += 1
            if reader["language"] not in seen_here:
                language["encyclicals"] += 1
                seen_here.add(reader["language"])
    return {
        "schema": OUTPUT_SCHEMA,
        "generator": "scripts/_encyclicals.py structure",
        "index": {
            "path": INDEX_RELATIVE.as_posix(),
            "revision": index["revision"],
            "sha256": hashlib.sha256(index_bytes).hexdigest(),
        },
        "scope": index["scope"],
        "description_provenance": index["description_provenance"],
        "popes": sorted(popes.values(), key=lambda pope: pope["pontificate_index"]),
        "languages": [languages[code] for code in language_order(set(languages))],
        "counts": {
            "encyclicals": len(rows),
            "with_local_text": with_text,
            "without_local_text": len(rows) - with_text,
            "readers": reader_count,
            "pages": pages,
            "english": english,
        },
        "encyclicals": rows,
    }


def render(index_path: Path, release_path: Path, root: Path = ROOT) -> str:
    """Validate and return the exact bytes of the browser file, as text."""
    index, index_bytes = read_json(index_path, _shown(index_path, root))
    documents = release_documents(release_path, _shown(release_path, root))
    errors = validate_index(index, documents)
    if errors:
        shown = "\n  ".join(errors[:40])
        more = f"\n  ... and {len(errors) - 40} more" if len(errors) > 40 else ""
        raise EncyclicalsError(
            f"{_shown(index_path, root)} is not publishable ({len(errors)} problem(s)):\n  "
            + shown + more
        )
    catalogue = browser_catalogue(index, index_bytes)
    return json.dumps(catalogue, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def output_path(out_root: Path) -> Path:
    return out_root / OUTPUT_RELATIVE


def _paths(root: Path, index: Path | None, release: Path | None, out: Path | None):
    return (
        index if index is not None else root / INDEX_RELATIVE,
        release if release is not None else root / RELEASE_RELATIVE,
        out if out is not None else root / DATA_ROOT_RELATIVE,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="_encyclicals.py",
        description="Check the encyclicals index and write the browser catalogue.",
    )
    parser.add_argument("--root", type=Path, default=ROOT)
    verbs = parser.add_subparsers(dest="verb", required=True)
    for name, text in (
        ("check", "validate the index against its schema and the papal release record"),
        ("structure", "write src/web/data/encyclicals/index.json from the index"),
    ):
        verb = verbs.add_parser(name, help=text)
        verb.add_argument(
            "--index", type=Path, default=None,
            help=f"the index to read (default {INDEX_RELATIVE.as_posix()})",
        )
        verb.add_argument(
            "--release", type=Path, default=None,
            help=f"the papal release record (default {RELEASE_RELATIVE.as_posix()})",
        )
        if name == "structure":
            verb.add_argument(
                "--out", type=Path, default=None,
                help=f"the data root to write into (default {DATA_ROOT_RELATIVE.as_posix()})",
            )
            verb.add_argument(
                "--check", action="store_true",
                help="exit 1 if the tracked file is not what the index produces, writing nothing",
            )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    index_path, release_path, out_root = _paths(
        root, args.index, args.release, getattr(args, "out", None)
    )
    try:
        text = render(index_path, release_path, root)
        if args.verb == "check":
            count = len(json.loads(text)["encyclicals"])
            print(f"encyclicals check: {_shown(index_path, root)} is valid ({count} rows)")
            return 0
        target = output_path(out_root)
        if args.check:
            current = target.read_text(encoding="utf-8") if target.is_file() else None
            if current != text:
                print(f"  stale {_shown(target, root)}")
                print(
                    "encyclicals structure: the tracked catalogue is not what the index "
                    "produces; rerun `make encyclicals-catalogue` and commit the result",
                    file=sys.stderr,
                )
                return 1
            print(f"encyclicals structure: {_shown(target, root)} is current")
            return 0
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        print(_shown(target, root))
        return 0
    except EncyclicalsError as error:
        print(f"encyclicals: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
