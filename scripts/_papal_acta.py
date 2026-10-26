"""Mechanical ASS/AAS acquisition, witness ownership, and act boundaries.

Recipes are reviewed source assertions, never an automatic heading splitter.
Only complete, single-language acts with exact bounds enter the render manifest.
"""
from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
import hashlib
from http.client import HTTPException
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib
from urllib.error import URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

from _tooling import examples_live_on_the_verbs, with_examples

ROOT = Path(__file__).resolve().parents[1]
CATALOG = Path("src/sources/papal-documents/acta-catalog.json")
MANIFEST = Path("src/sources/papal-documents/acta-manifest.json")
ARCHIVES = Path("src/sources/papal-documents/archives.json")
SOURCE_ROOT = Path("src/sources/works/acta-papal-archives")
RECIPE_SCHEMA = "triptych-acta-recipes/v1"
CATALOG_SCHEMA = "triptych-papal-acta-catalog/v1"
SAFE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
HASH = re.compile(r"^[a-f0-9]{64}$")
LANGUAGES = {"la", "en", "it", "fr", "de", "es", "pt", "nl", "pl"}
OCR_NOTE = "Archival OCR reconstruction and mechanical extraction; no facsimile image collation is claimed. OCR errors, historical spelling, line breaks, and unverified pagination remain source limitations."


def literal_act_date(clause: str) -> str | None:
    """Parse complete day/year tokens in an already identified dating clause.

    Keep lexical boundaries: deleting separators and matching [MDCLXVI]+ can
    turn damaged MDCCCCTV into the valid prefix MDCCCC (1900). Never repair
    missing letters, infer a year from the issuer, or search beyond this clause.
    Additive historical numerals, including MDCCCCIV, remain admissible.
    """
    months = ("ianuarii", "februarii", "martii", "aprilis", "maii", "iunii",
              "iulii", "augusti", "septembris", "octobris", "novembris", "decembris")
    numeral = re.compile(r"M{0,4}(?:CM|CD|D?C{0,4})(?:XC|XL|L?X{0,4})(?:IX|IV|V?I{0,4})")
    def number(token: str) -> int | None:
        token = token.upper()
        if token.isascii() and token.isdigit():
            return int(token)
        if not token or not numeral.fullmatch(token):
            return None
        values = {"M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1}
        return sum(-values[c] if i + 1 < len(token) and values[c] < values[token[i+1]] else values[c]
                   for i, c in enumerate(token))
    # Read the entire whitespace/punctuation-delimited token, including damaged
    # combining marks or OCR symbols. A \w boundary could still accept a Roman
    # prefix before a combining accent or zero-width damaged glyph.
    token = r"([^\s,;:.()\[\]]+)"
    pattern = re.compile(r"\bdie\s+" + token + r"\s+(" + "|".join(months) + r")\s+(?:anno\s+)?" + token, re.I)
    dates = []
    for match in pattern.finditer(clause):
        day, year = number(match[1]), number(match[3])
        if day is None or year is None:
            return None
        try:
            dates.append(dt.date(year, months.index(match[2].lower()) + 1, day).isoformat())
        except ValueError:
            return None
    return dates[0] if dates and len(set(dates)) == 1 else None


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def physical_lines(data: bytes) -> list[bytes]:
    """LF alone delimits physical lines; FF remains source content."""
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    return lines


def bounds(value: object, count: int, *, required: bool = True) -> list[list[int]]:
    if value is None and not required:
        return []
    if not isinstance(value, list) or (required and not value):
        raise ValueError("expected nonempty ordered inclusive line/page ranges")
    previous = 0
    for pair in value:
        if not isinstance(pair, list) or len(pair) != 2 or any(type(n) is not int for n in pair):
            raise ValueError("a range must contain two integers")
        start, end = pair
        if not previous < start <= end <= count:
            raise ValueError("ranges overlap, are unordered, or escape their exact artifact")
        previous = end
    return value


def resolve(root: Path, value: str | Path) -> Path:
    path = Path(value)
    path = (root / path if not path.is_absolute() else path).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("path escapes repository root")
    return path


def relative(root: Path, path: Path) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def scratch(root: Path, value: str | Path) -> Path:
    path = resolve(root, value)
    if not path.is_relative_to((root / ".scratch").resolve()):
        raise ValueError("acquired and staging bytes must remain under repository .scratch")
    return path


def write(path: Path, data: bytes, *, immutable: bool = False) -> None:
    if path.exists():
        if path.read_bytes() == data:
            return
        if immutable:
            raise ValueError("refusing to replace an existing source record or payload: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".new")
    temporary.write_bytes(data)
    temporary.replace(path)


def write_json(path: Path, data: object) -> None:
    write(path, (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode())


def toml(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ", ".join(toml(item) for item in value) + "]"
    raise ValueError("unsupported TOML scalar")


def record(path: Path, data: dict) -> None:
    write(path, ("\n".join(f"{key} = {toml(value)}" for key, value in data.items()) + "\n").encode(), immutable=True)


def safe_evidence(value: object) -> str:
    if value is None:
        return "Unknown"
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)


def clean_slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9.-]+", "-", value.lower()).strip(".-")
    if not value or not SAFE.fullmatch(value):
        raise ValueError("cannot derive a safe stable identifier")
    return value


def volume_identity(volume: dict) -> str:
    return clean_slug(volume["archive_id"].removeprefix("archive."))


def pope_name(value: str) -> str:
    match = re.fullmatch(r"([a-z]+)-([ivxlcdm]+)", value)
    return match[1].capitalize() + " " + match[2].upper() if match else value


def act_work_path(root: Path, volume: dict, act: dict) -> Path:
    slug = volume_identity(volume) + "-" + act.get("work_local_id", act["local_id"])
    prefix = act.get("date") if not act.get("work_date_discrepancy") else None
    return root / SOURCE_ROOT / ((prefix or "undated") + "-" + slug)


def source_url(value: str) -> str:
    parts = urlsplit(value)
    if (parts.scheme != "https" or parts.hostname not in {"www.vatican.va", "vatican.va"}
            or parts.username or parts.password or parts.port not in {None, 443}
            or any(ord(c) < 33 for c in value)):
        raise ValueError("archival source must be a public HTTPS Vatican URL")
    return value


def revision(value: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        raise ValueError("revision must be a whole-second UTC timestamp")
    dt.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return value


def printing_year(volume: dict) -> int:
    year = volume.get("historical_printing_year", volume["publication_year"])
    if type(year) is not int or year < 1:
        raise ValueError("historical printing year must be a positive integer")
    return year


def derivatives(volume: dict) -> list[dict]:
    return [volume] + volume.get("additional_derivatives", [])


def extraction_description(value: object) -> str:
    text = safe_evidence(value)
    text = re.sub(r"(?:/[^\s\"']*)?\.scratch/[^\s\"']+", "<transient-path>", text)
    return re.sub(r"/home/[^\s\"']+", "<transient-path>", text)


def source_parent(root: Path, derivative: dict) -> tuple[bytes, str] | None:
    if not derivative.get("source_parent_text_path"):
        return None
    payload = scratch(root, derivative["source_parent_text_path"]).read_bytes()
    digest = sha(payload)
    if digest != derivative.get("source_parent_text_sha256"):
        raise ValueError("reordered derivative's exact source extraction hash disagrees")
    if derivative.get("source_parent_text_bytes", len(payload)) != len(payload):
        raise ValueError("reordered derivative's source extraction extent disagrees")
    payload.decode("utf-8")
    selection = derivative.get("ordered_source_line_ranges")
    slices = derivative.get("ordered_source_line_slices")
    if selection is not None and slices is not None:
        raise ValueError("choose source line ranges or Unicode column slices, not both")
    if selection is not None:
        lines = physical_lines(payload)
        if not isinstance(selection, list) or not selection:
            raise ValueError("ordered extraction selection requires source line ranges")
        numbers = []
        for pair in selection:
            bounds([pair], len(lines))
            numbers.extend(range(pair[0], pair[1] + 1))
        selected = b"\n".join(lines[number - 1] for number in numbers) + b"\n"
        if selected != scratch(root, derivative["text_path"]).read_bytes():
            raise ValueError("ordered extraction selection does not reproduce the exact derivative")
    if slices is not None:
        if not isinstance(slices, list) or not slices:
            raise ValueError("ordered extraction slices must be a nonempty list")
        lines = [line.decode("utf-8") for line in physical_lines(payload)]
        selected = []
        previous_source_line = None
        for item in slices:
            if (not isinstance(item, dict) or not {"physical_line_range", "unicode_columns"} <= set(item)
                    or set(item) - {"physical_line_range", "unicode_columns", "join_previous"}):
                raise ValueError("source slice requires physical_line_range and unicode_columns")
            start, end = bounds([item["physical_line_range"]], len(lines))[0]
            columns = item["unicode_columns"]
            if columns is None:
                left, right = 0, None
            else:
                if (not isinstance(columns, list) or len(columns) != 2 or type(columns[0]) is not int
                        or columns[0] < 0 or columns[1] is not None
                        and (type(columns[1]) is not int or columns[1] < columns[0])):
                    raise ValueError("Unicode columns must be a nonnegative half-open pair, with optional null end")
                left, right = columns
            join = item.get("join_previous", False)
            if type(join) is not bool or join and (not selected or start != end or previous_source_line != start):
                raise ValueError("joining slices requires consecutive fragments of the same source LF line")
            fragments = [line[left:right] for line in lines[start - 1:end]]
            if join:
                selected[-1] += fragments[0]
            else:
                selected.extend(fragments)
            previous_source_line = end
        if ("\n".join(selected) + "\n").encode("utf-8") != scratch(root, derivative["text_path"]).read_bytes():
            raise ValueError("ordered Unicode slices do not reproduce the exact derivative")
    return payload, digest


def validate_recipe(root: Path, volume: dict) -> None:
    identifier = volume.get("archive_id", "")
    if not isinstance(identifier, str) or not SAFE.fullmatch(identifier):
        raise ValueError("invalid archival volume identity")
    source_url(volume["source_url"])
    if type(volume.get("publication_year")) is not int or not 1 <= volume["publication_year"] <= 9999:
        raise ValueError("volume requires a publication year")
    pdf = scratch(root, volume["pdf_path"]).read_bytes()
    if not pdf.startswith(b"%PDF-"):
        raise ValueError("archival PDF lacks a PDF signature")
    if sha(pdf) != volume.get("pdf_sha256") or len(pdf) != volume.get("pdf_bytes"):
        raise ValueError(identifier + ": whole PDF hash or extent mismatch")
    if type(volume.get("page_count")) is not int or volume["page_count"] < 1:
        raise ValueError("exact PDF page count is required")
    by_path = {}
    for derivative in derivatives(volume):
        path = derivative["text_path"]
        if path in by_path:
            raise ValueError("duplicate extraction path in volume")
        payload = scratch(root, path).read_bytes()
        payload.decode("utf-8")
        if sha(payload) != derivative.get("text_sha256") or len(payload) != derivative.get("text_bytes"):
            raise ValueError(identifier + ": whole extraction hash or extent mismatch")
        lines = physical_lines(payload)
        if not lines:
            raise ValueError("empty archival extraction")
        for field in ("historical_text_line_ranges", "excluded_wrapper_ranges"):
            if derivative.get(field) is not None:
                bounds(derivative[field], len(lines), required=field == "historical_text_line_ranges")
        source_parent(root, derivative)
        by_path[path] = {"recipe": derivative, "payload": payload, "line_count": len(lines)}
    historical = not volume.get("metadata_only") and volume["publication_year"] <= 1930
    if historical:
        if not volume.get("historical_printing_basis"):
            raise ValueError(identifier + ": historical printing evidence is required before retention")
        if printing_year(volume) > 1930:
            raise ValueError("historical print eligibility depends on the actual printing year")
        for item in by_path.values():
            _, item["mapping"], _ = retain_derivative(root, volume, item["recipe"])
    identifiers = set()
    if not isinstance(volume.get("acts"), list) or not isinstance(volume.get("gaps", []), list):
        raise ValueError("volume acts and gaps must be lists")
    for act in volume["acts"]:
        local_id = act.get("local_id")
        if not isinstance(local_id, str) or not SAFE.fullmatch(local_id) or local_id in identifiers:
            raise ValueError("duplicate or invalid local act identity")
        identifiers.add(local_id)
        state = act.get("completeness")
        for field in ("title", "document_type"):
            if not isinstance(act.get(field), str) or not act[field].strip():
                raise ValueError("act requires " + field)
        if act.get("pope") is not None and (not isinstance(act["pope"], str) or not act["pope"].strip()):
            raise ValueError("act issuer must be a nonempty source-supported name or null")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", act["document_type"]):
            raise ValueError("document_type must preserve a lowercase kebab-case source genre")
        if act.get("date") is not None:
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", act["date"]):
                raise ValueError("act date must be ISO or null")
            dt.date.fromisoformat(act["date"])
        if state not in {"complete", "unresolved", "metadata-only"}:
            raise ValueError("unknown act boundary/completeness state")
        chosen = act.get("text_path", volume["text_path"])
        if chosen not in by_path:
            raise ValueError("act names an undeclared extraction derivative")
        line_count = by_path[chosen]["line_count"]
        for field in ("physical_line_ranges", "index_line_ranges"):
            if act.get(field):
                bounds(act[field], line_count)
        if act.get("artifact_page_ranges"):
            bounds(act["artifact_page_ranges"], volume["page_count"])
        if state == "complete":
            if not historical:
                raise ValueError("later AAS cannot admit public bodies without a separate rights basis")
            if act.get("language") not in LANGUAGES:
                raise ValueError("complete act must identify one supported language")
            if not act.get("pope"):
                raise ValueError("complete act requires its actual issuer")
            if not act.get("physical_line_ranges") or not act.get("identity_evidence") or not act.get("boundary_evidence"):
                raise ValueError("complete act lacks exact bounds or reviewed identity/boundary evidence")
            remap(act["physical_line_ranges"], by_path[chosen]["mapping"])
        if act.get("work_local_id"):
            if not SAFE.fullmatch(act["work_local_id"]) or not act.get("work_identity_evidence"):
                raise ValueError("language-witness grouping requires reviewed work identity evidence")
        if act.get("canonical_work_id"):
            if not SAFE.fullmatch(act["canonical_work_id"]) or not act.get("canonical_join_evidence"):
                raise ValueError("canonical work join requires reviewed author/date/incipit evidence")


def read_recipes(root: Path, paths: list[Path]) -> list[dict]:
    volumes, seen = [], set()
    for path in paths:
        data = json.loads(resolve(root, path).read_text(encoding="utf-8"))
        if data.get("schema") != RECIPE_SCHEMA or not isinstance(data.get("volumes"), list):
            raise ValueError("expected " + RECIPE_SCHEMA)
        for volume in data["volumes"]:
            validate_recipe(root, volume)
            if volume["archive_id"] in seen:
                raise ValueError("duplicate archival volume identity")
            seen.add(volume["archive_id"])
            volumes.append(volume)
    return sorted(volumes, key=lambda item: item["archive_id"])


def retain_derivative(root: Path, volume: dict, derivative: dict) -> tuple[bytes, dict[int, int], str]:
    """Keep declared historical lines and map their exact original LF loci."""
    original = scratch(root, derivative["text_path"]).read_bytes()
    if sha(original) != derivative.get("text_sha256") or len(original) != derivative.get("text_bytes"):
        raise ValueError("whole extraction hash or extent mismatch before retention")
    lines = physical_lines(original)
    keep = derivative.get("historical_text_line_ranges")
    excluded = {n for a, b in derivative.get("excluded_wrapper_ranges", []) for n in range(a, b + 1)}
    if keep is None:
        keep = []
        for number in range(1, len(lines) + 1):
            if number in excluded:
                continue
            if keep and keep[-1][1] == number - 1:
                keep[-1][1] = number
            else:
                keep.append([number, number])
    bounds(keep, len(lines))
    selected = [n for start, end in keep for n in range(start, end + 1)]
    if any(number in excluded for number in selected):
        raise ValueError("historical ranges intersect excluded modern wrapper lines")
    historical = b"\n".join(lines[number - 1] for number in selected) + b"\n"
    lowered = historical.lower()
    if b"johnson reprint" in lowered or b"reprinted with the permission" in lowered:
        raise ValueError("modern reprint wrapper remains inside proposed historical text")
    mapping = {old: new for new, old in enumerate(selected, 1)}
    transform = ("Retain precisely historical LF lines " + json.dumps(keep, separators=(",", ":"))
                 + "; omit all other lines; join retained lines with LF and one terminal LF. No source words or characters are corrected.")
    return historical, mapping, transform


def remap(ranges: list[list[int]], mapping: dict[int, int]) -> list[list[int]]:
    bounds(ranges, max(mapping, default=0))
    result = []
    for start, end in ranges:
        for old in range(start, end + 1):
            if old not in mapping:
                raise ValueError("act bound intersects excluded modern/nonhistorical material")
            target = mapping[old]
            if result and result[-1][1] + 1 == target:
                result[-1][1] = target
            else:
                result.append([target, target])
    return result


def source_index(root: Path) -> dict:
    works, artifacts, ids = {}, {}, {}
    for path in (root / "src/sources/works").glob("*/*/work.toml"):
        data = tomllib.loads(path.read_text())
        works[data["id"]] = path.parent
    for path in (root / "src/sources/works").glob("*/*/editions/*/artifacts/*/artifact.toml"):
        data = tomllib.loads(path.read_text())
        ids[data["id"]] = (path, data)
        if data.get("sha256"):
            artifacts.setdefault(data["sha256"], []).append((path, data))
    return {"works": works, "artifacts": artifacts, "ids": ids}


def public_metadata(value: object) -> object:
    """Acquisition locations are transient implementation details."""
    if isinstance(value, dict):
        return {k: public_metadata(v) for k, v in value.items()
                if k not in {"pdf_path", "text_path", "recipe_text_path", "mapping", "additional_derivatives", "source_parent_text_path"}}
    if isinstance(value, list):
        return [public_metadata(item) for item in value]
    if isinstance(value, str) and (".scratch/" in value or value.startswith("/home/")):
        return "Transient acquisition location omitted; exact artifact hashes identify the source."
    return value


def rights_basis(volume: dict, derivative: dict) -> str:
    basis = derivative.get("historical_printing_basis", volume.get("historical_printing_basis"))
    if not basis:
        raise ValueError("historical printing evidence is required before retention")
    return ("United States public domain: identified historical printing published by 1930; expired maximum term under 17 U.S.C. 304–305, with 104A remainder where applicable. "
            + safe_evidence(basis) + " The mechanical historical-text derivative excludes separately identified modern wrappers and makes no claim over modern creative revision. Rights position: src/sources/inventories/papal-documents-rights-v1.toml. Source wording is excluded from Triptych's CC BY 4.0 license.")


def register_volume(root: Path, volume: dict, index: dict, retrieved: str) -> dict:
    slug = volume_identity(volume)
    is_aas = slug.startswith("aas.")
    journal_slug = "acta-apostolicae-sedis" if is_aas else "acta-sanctae-sedis"
    journal_title = "Acta Apostolicae Sedis" if is_aas else "Acta Sanctae Sedis"
    established = "work.holy-see." + journal_slug
    work_id = established if established in index["works"] else "work.acta-papal-archives." + journal_slug
    container = index["works"].get(work_id, root / SOURCE_ROOT / journal_slug)
    edition_slug = str(printing_year(volume)) + "-acta-" + slug.replace(".", "-")
    edition_dir = container / "editions" / edition_slug
    edition_id = "edition.acta-papal-archives." + slug + "." + edition_slug
    held = [(p, d) for p, d in index["artifacts"].get(volume["pdf_sha256"], []) if d.get("media_type") == "application/pdf"]
    if held:
        parent_path, parent = sorted(held, key=lambda item: str(item[0]))[0]
        edition_dir = parent_path.parents[2]
        edition = tomllib.loads((edition_dir / "edition.toml").read_text())
        edition_id, work_id, raw_id = edition["id"], edition["work_id"], parent["id"]
        controlling_url = parent.get("source_url", volume["source_url"])
    else:
        controlling_url = volume["source_url"]
        title = volume.get("title", journal_title + " — source witness " + slug)
        if not (container / "work.toml").exists():
            record(container / "work.toml", {"schema": 1, "record_type": "work", "id": work_id,
                "title": journal_title, "responsible": "Holy See" if is_aas else "Acta Sanctae Sedis editors", "work_type": "periodical",
                "description": "Historical journal container; curial and editorial contents are distinct from bounded individual papal formal acts. " + OCR_NOTE})
            index["works"][work_id] = container
        record(edition_dir / "edition.toml", {"schema": 1, "record_type": "edition", "id": edition_id, "work_id": work_id,
            "title": title, "language": "mul", "publication": safe_evidence(volume.get("historical_printing_basis", "Source-listed archival journal or index edition; underlying printing is not cleared for local text.")),
            "date": str(printing_year(volume)), "notes": OCR_NOTE})
        raw_id = "artifact.acta-papal-archives." + slug + ".vatican-pdf-" + volume["pdf_sha256"][:8]
        record(edition_dir / "artifacts" / ("vatican-pdf-" + volume["pdf_sha256"][:8]) / "artifact.toml", {
            "schema": 2, "record_type": "artifact", "id": raw_id, "edition_id": edition_id,
            "artifact_type": "archival-ocr-pdf", "media_type": "application/pdf", "storage": "restricted", "rights_status": "unresolved",
            "rights_basis": "Exact Vatican delivery, including digital construction and any modern wrapper, is not asserted redistributable. Historical underlying wording is assessed separately per derived artifact.",
            "source_url": volume["source_url"], "retrieved": retrieved, "sha256": volume["pdf_sha256"], "byte_size": volume["pdf_bytes"], "page_count": volume["page_count"],
            "provenance": "Whole source-listed PDF mechanically acquired and hashed before extraction.",
            "notes": "Complete raw PDF is held only in transient scratch; offline readers can open any separately cleared historical-text derivative. " + OCR_NOTE})
    result = public_metadata({key: value for key, value in volume.items() if key != "acts"})
    if controlling_url != volume["source_url"]:
        result["discovery_source_url"] = volume["source_url"]
        result["source_url"] = controlling_url
    result.update({"container_work_id": work_id, "container_edition_id": edition_id, "pdf_artifact_id": raw_id, "derivatives": []})
    historical = not volume.get("metadata_only") and volume["publication_year"] <= 1930 and printing_year(volume) <= 1930
    raw_records = {data["sha256"]: data["id"] for _, data in index["ids"].values()
                   if data.get("edition_id") == edition_id and data.get("artifact_type") == "mechanical-pdf-text-extraction"
                   and data.get("sha256")}
    for derivative in derivatives(volume):
        payload = scratch(root, derivative["text_path"]).read_bytes()
        raw_text_id = raw_records.get(derivative["text_sha256"], "artifact.acta-papal-archives." + slug + ".extracted-text-" + derivative["text_sha256"][:8])
        raw_text_dir = edition_dir / "artifacts" / ("acta-extracted-" + derivative["text_sha256"][:8])
        extraction = extraction_description(derivative.get("extraction_command", volume.get("extraction_command")))
        if derivative.get("transformation"):
            extraction += "; " + extraction_description(derivative["transformation"])
        parent_id = raw_id
        source = source_parent(root, derivative)
        if source is not None and source[1] != derivative["text_sha256"]:
            source_bytes, source_hash = source
            parent_id = raw_records.get(source_hash, "artifact.acta-papal-archives." + slug + ".extracted-text-" + source_hash[:8])
            parent_dir = edition_dir / "artifacts" / ("acta-extracted-" + source_hash[:8])
            if source_hash not in raw_records:
                record(parent_dir / "artifact.toml", {"schema": 1, "record_type": "artifact", "id": parent_id, "edition_id": edition_id,
                    "artifact_type": "mechanical-pdf-text-extraction", "media_type": "text/plain", "storage": "restricted", "rights_status": "unresolved",
                    "rights_basis": "Exact unfiltered extraction remains transient; a separately cleared historical derivative identifies retained wording.",
                    "retrieved": retrieved, "sha256": source_hash, "byte_size": len(source_bytes), "derived_from": raw_id,
                    "transformation": extraction_description(derivative.get("source_parent_extraction_command", "Mechanical PDF text extraction; exact flags are not separately supplied for this intermediate.")), "notes": OCR_NOTE})
                raw_records[source_hash] = parent_id
            if derivative.get("ordered_source_line_ranges"):
                extraction += "; concatenate source LF ranges in this declared order: " + json.dumps(derivative["ordered_source_line_ranges"], separators=(",", ":")) + "; join with LF and one terminal LF"
            if derivative.get("ordered_source_line_slices"):
                extraction += "; select inclusive 1-based LF ranges and 0-based half-open Unicode columns in this declared order: " + json.dumps(derivative["ordered_source_line_slices"], separators=(",", ":")) + "; join_previous concatenates consecutive fragments of the same source LF line before its LF; otherwise append LF after each selected source line/slice, preserving all selected characters"
            if derivative.get("transformation"):
                extraction += "; " + extraction_description(derivative["transformation"])
        if derivative["text_sha256"] not in raw_records:
            record(raw_text_dir / "artifact.toml", {"schema": 1, "record_type": "artifact", "id": raw_text_id, "edition_id": edition_id,
            "artifact_type": "mechanical-pdf-text-extraction", "media_type": "text/plain", "storage": "restricted", "rights_status": "unresolved",
            "rights_basis": "Exact extraction may contain protected text or modern wrappers and remains transient. Separately manifested historical text excludes uncleared material.",
            "retrieved": retrieved, "sha256": derivative["text_sha256"], "byte_size": len(payload), "derived_from": parent_id, "transformation": extraction, "notes": OCR_NOTE})
            raw_records[derivative["text_sha256"]] = raw_text_id
        descriptor = {"recipe_text_path": derivative["text_path"], "raw_artifact_id": raw_text_id,
                      "raw_sha256": derivative["text_sha256"], "raw_byte_size": len(payload)}
        if not historical:
            result["derivatives"].append(descriptor)
            continue
        historical, mapping, transform = retain_derivative(root, volume, derivative)
        digest = sha(historical)
        basis = rights_basis(volume, derivative)
        # Same bytes have one retained owner, even when extraction modes coincide.
        prior = next((d for d in result["derivatives"] if d["sha256"] == digest), None)
        if prior:
            result["derivatives"].append(prior | descriptor | {"mapping": mapping})
            continue
        held_text = next((data for _, data in index["artifacts"].get(digest, [])
                          if data.get("edition_id") == edition_id and data.get("storage") == "tracked"
                          and data.get("rights_status") == "public-domain" and data.get("media_type") == "text/plain"), None)
        if held_text:
            result["derivatives"].append(descriptor | {"artifact_id": held_text["id"], "text_path": held_text["path"],
                "sha256": digest, "byte_size": len(historical), "rights_basis": held_text["rights_basis"], "mapping": mapping})
            continue
        art_slug = "acta-historical-text-" + digest[:8]
        art_id = "artifact.acta-papal-archives." + slug + ".historical-text-" + digest[:8]
        artifact_dir = edition_dir / "artifacts" / art_slug
        text_path = artifact_dir / "historical.txt"
        write(text_path, historical, immutable=True)
        record(artifact_dir / "artifact.toml", {"schema": 1, "record_type": "artifact", "id": art_id, "edition_id": edition_id,
            "artifact_type": "historical-text-derivative", "media_type": "text/plain", "storage": "tracked", "rights_status": "public-domain", "rights_jurisdiction": "United States",
            "rights_basis": basis, "retrieved": retrieved, "sha256": digest, "byte_size": len(historical), "path": relative(root, text_path),
            "derived_from": raw_text_id, "transformation": transform, "encoding": "utf-8", "indexable": True,
            "provenance": "Mechanical derivative of the complete hashed archival PDF through its separately hashed UTF-8 extraction.",
            "notes": OCR_NOTE + " " + safe_evidence(derivative.get("limitations", volume.get("limitations", [])))})
        result["derivatives"].append(descriptor | {"artifact_id": art_id, "text_path": relative(root, text_path), "sha256": digest,
                                                   "byte_size": len(historical), "rights_basis": basis, "mapping": mapping})
    # Subset recipes of one annual PDF retain the established exact owner.
    for path in edition_dir.glob("artifacts/*/artifact.toml"):
        data = tomllib.loads(path.read_text())
        index["ids"][data["id"]] = (path, data)
        if data.get("sha256") and not any(old[1]["id"] == data["id"] for old in index["artifacts"].get(data["sha256"], [])):
            index["artifacts"].setdefault(data["sha256"], []).append((path, data))
    return result


def register_act(root: Path, volume: dict, registered: dict, act: dict, index: dict) -> dict:
    identifier = "acta." + volume_identity(volume) + "." + act["local_id"]
    result = public_metadata(act) | {"id": identifier, "date": act.get("date"), "archive_id": volume["archive_id"], "source_url": registered["source_url"],
        "record_role": act.get("record_role", "source-index-entry" if act["completeness"] == "metadata-only" else "bounded-source-act"), "source_quality": "uncollated-archival-ocr", "text_available": False}
    if registered.get("discovery_source_url"):
        result["discovery_source_url"] = registered["discovery_source_url"]
    if pope_name(act["pope"]) != act["pope"]:
        result["pope_id"] = act["pope"]
        result["pope"] = pope_name(act["pope"])
    derivative = next(item for item in registered["derivatives"] if item["recipe_text_path"] == act.get("text_path", volume["text_path"]))
    result.update({"source_extraction_artifact_id": derivative["raw_artifact_id"], "source_extraction_sha256": derivative["raw_sha256"]})
    if act["completeness"] != "complete":
        return result
    ranges = remap(act["physical_line_ranges"], derivative["mapping"])
    work_id = act.get("canonical_work_id")
    if work_id:
        if work_id not in index["works"]:
            raise ValueError("reviewed canonical act work is absent: " + work_id)
        work_dir = index["works"][work_id]
    else:
        group = index["work_groups"][(volume["archive_id"], act.get("work_local_id", act["local_id"]))]
        primary = group[0]
        slug = volume_identity(volume) + "-" + act.get("work_local_id", act["local_id"])
        work_id = "work.acta-papal-archives." + slug
        work_dir = act_work_path(root, volume, primary)
        evidence = primary.get("work_identity_evidence", primary["identity_evidence"])
        data = {"schema": 1, "record_type": "work", "id": work_id, "title": primary["title"], "responsible": pope_name(primary["pope"]),
                "work_type": primary["document_type"], "languages": sorted({item["language"] for item in group}),
                "description": "Individual papal formal act identified from archival body evidence. " + safe_evidence(evidence)}
        if primary.get("date") and len({item.get("date") for item in group}) == 1:
            data.update({"composed": primary["date"], "composed_basis": safe_evidence(evidence)})
        record(work_dir / "work.toml", data)
    edition_slug = str(printing_year(volume)) + "-acta-" + volume_identity(volume).replace(".", "-") + "-" + act["local_id"]
    edition_dir = work_dir / "editions" / edition_slug
    edition_id = "edition.acta-papal-archives." + volume_identity(volume) + "." + act["local_id"]
    record(edition_dir / "edition.toml", {"schema": 1, "record_type": "edition", "id": edition_id, "work_id": work_id,
        "title": act["title"], "language": act["language"], "date": str(printing_year(volume)), "publication": safe_evidence(volume["historical_printing_basis"]), "authority": pope_name(act["pope"]),
        "notes": "Constituent witnessed within " + volume["archive_id"] + ", printed pages " + safe_evidence(act.get("printed_pages")) + ". " + OCR_NOTE})
    segment_id = "segment.acta-papal-archives." + volume_identity(volume) + "." + act["local_id"]
    segment_path = edition_dir / "segments" / "historical-text.toml"
    record(segment_path, {"schema": 2, "record_type": "segment", "id": segment_id, "edition_id": edition_id,
        "artifact_id": derivative["artifact_id"], "artifact_sha256": derivative["sha256"], "segment_type": "constituent-work", "states": ["cataloged", "acquired", "inspected"],
        "physical_line_ranges": ranges, "context": safe_evidence(act["identity_evidence"]), "notes": safe_evidence(act["boundary_evidence"]) + " " + OCR_NOTE})
    if act.get("artifact_page_ranges"):
        record(edition_dir / "segments" / "archival-pdf.toml", {"schema": 2, "record_type": "segment", "id": segment_id + ".pdf", "edition_id": edition_id,
            "artifact_id": registered["pdf_artifact_id"], "artifact_sha256": volume["pdf_sha256"], "segment_type": "archival-act-locator", "states": ["cataloged", "acquired", "inspected"],
            "artifact_page_ranges": act["artifact_page_ranges"], "context": safe_evidence(act["boundary_evidence"]),
            "notes": "Artifact-page locators are distinct from the printed page labels " + safe_evidence(act.get("printed_pages")) + ". " + OCR_NOTE})
    result.update({"work_id": work_id, "edition_id": edition_id, "segment_id": segment_id, "segment_path": relative(root, segment_path), "artifact_id": derivative["artifact_id"],
        "text_path": derivative["text_path"], "sha256": derivative["sha256"], "physical_line_ranges": ranges, "source_physical_line_ranges": act["physical_line_ranges"],
        "rights_status": "public-domain", "rights_basis": derivative["rights_basis"], "text_available": True})
    return result


def catalog(root: Path, volumes: list[dict], render_revision: str, *, register: bool) -> dict:
    revision(render_revision)
    index = source_index(root) if register else {}
    index["work_groups"] = {}
    if register:
        # A reviewed republication may join a truthful work introduced by
        # another volume in this same batch, regardless of processing order.
        for volume in volumes:
            for act in volume.get("acts", []):
                if act.get("completeness") == "complete" and not act.get("canonical_work_id"):
                    slug = volume_identity(volume) + "-" + act.get("work_local_id", act["local_id"])
                    index["works"].setdefault("work.acta-papal-archives." + slug, act_work_path(root, volume, act))
    # All byte, rights, and canonical-identity checks precede the first mutation.
    for volume in volumes:
        validate_recipe(root, volume)
        if register:
            for act in volume["acts"]:
                if act.get("canonical_work_id") and act["canonical_work_id"] not in index["works"]:
                    raise ValueError("reviewed canonical act work is absent: " + act["canonical_work_id"])
                if act["completeness"] == "complete":
                    key = (volume["archive_id"], act.get("work_local_id", act["local_id"]))
                    index["work_groups"].setdefault(key, []).append(act)
    for group in index["work_groups"].values():
        if len({act["pope"] for act in group}) != 1:
            raise ValueError("grouped language witnesses disagree on issuer")
        if len({act.get("date") for act in group}) != 1 and not all(act.get("work_date_discrepancy") for act in group):
            raise ValueError("grouped language witnesses disagree on act date without source-explicit discrepancy evidence")
        if len({act.get("canonical_work_id") for act in group}) != 1:
            raise ValueError("grouped language witnesses disagree on canonical work identity")
    volume_rows, documents = [], []
    for volume in volumes:
        if register:
            registered = register_volume(root, volume, index, render_revision[:10])
            for act in volume["acts"]:
                documents.append(register_act(root, volume, registered, act, index))
            for derivative in registered["derivatives"]:
                derivative.pop("mapping", None)
                derivative.pop("recipe_text_path", None)
            volume_rows.append(registered)
        else:
            volume_rows.append(public_metadata({key: value for key, value in volume.items() if key != "acts"}))
            for act in volume["acts"]:
                documents.append(public_metadata(act) | {"id": "acta." + volume_identity(volume) + "." + act["local_id"], "date": act.get("date"),
                    "archive_id": volume["archive_id"], "source_url": volume["source_url"], "text_available": False})
    return {"schema": CATALOG_SCHEMA, "revision": render_revision,
        "scope": "Source-supported formal papal acts from identified ASS/AAS witnesses; related curial and editorial matter stays distinct. Source-index records are source assertions, not authenticated abstract works. This inventory does not establish exhaustive historical papal coverage.",
        "coverage": coverage(volume_rows, documents),
        "volumes": volume_rows, "documents": documents,
        "limitations": [OCR_NOTE, "Discovery, source quality, act boundaries, work identity, rights, and rendering review are independent states.",
                        "Later AAS bodies remain metadata-only; annual and issue routes are not double-counted as independent acts."]}


def coverage(volumes: list[dict], documents: list[dict]) -> dict:
    totals = Counter(act["completeness"] for act in documents)
    identified = {act["work_id"] for act in documents if act.get("work_id")}
    grouped = sum(bool(act.get("grouped_instruments") or act.get("source_unit_kind") == "grouped-instruments"
                       or act.get("record_role") == "grouped-instruments") for act in documents)
    numbered = {}
    for volume in volumes:
        match = re.match(r"^archive\.(ass|aas)\.(\d+)(?:\.|$)", volume.get("parent_archive_id", volume["archive_id"]))
        if match:
            numbered.setdefault(match[1].upper(), set()).add(int(match[2]))
    return {"volumes": len(volumes), "source_container_witnesses": len(volumes),
            "unique_pdf_witnesses": len({volume["pdf_sha256"] for volume in volumes}),
            "numbered_volumes_by_series": {series: len(numbers) for series, numbers in sorted(numbered.items())},
            "source_act_records": len(documents), "source_witness_records": len(documents),
            "identified_works": len(identified), "complete_bounds": totals["complete"], "metadata_only": totals["metadata-only"],
            "metadata_index_records": totals["metadata-only"], "grouped_index_records": grouped, "unresolved": totals["unresolved"],
            "retained_act_witnesses": sum(bool(act.get("text_available")) for act in documents),
            "retained_fragment_witnesses": sum(bool(act.get("retained_fragment_available")) for act in documents),
            "gaps": sum(len(volume.get("gaps", [])) for volume in volumes)}


def make_manifest(data: dict, render_revision: str) -> dict:
    revision(render_revision)
    documents, seen = [], set()
    volumes = {volume["archive_id"]: volume for volume in data.get("volumes", [])}
    for act in data["documents"]:
        if not act.get("text_available") or act.get("completeness") != "complete":
            continue
        key = (act["work_id"], act["language"])
        if key in seen:
            continue
        seen.add(key)
        names = ("id", "title", "pope", "document_type", "language", "source_url", "text_path", "sha256", "artifact_id", "rights_status", "rights_basis", "segment_id", "segment_path", "physical_line_ranges", "work_id", "edition_id")
        note = act.get("source_note") or OCR_NOTE
        volume = volumes.get(act.get("archive_id"), {})
        match = re.match(r"archive\.(ass|aas)\.(\d+)", act.get("archive_id", ""))
        if match:
            citation = match[1].upper() + " " + str(int(match[2]))
            if volume.get("publication_year"):
                citation += " (" + str(volume["publication_year"]) + ")"
            if isinstance(act.get("printed_pages"), (str, int)):
                citation += ", printed pages " + str(act["printed_pages"])
            note = citation + ". " + note
        documents.append({name: act[name] for name in names} | {"date": act.get("date"),
            "source_note": note,
            "rights_notice": "Historical source wording is public domain in the United States on its identified pre-1931 publication basis; status elsewhere may differ. Source wording is excluded from Triptych's project license. Exact edition and rights evidence remain in the controlling source record."})
    return {"schema": "triptych-papal-typeset/v1", "revision": render_revision, "documents": documents}


def validate_catalog(root: Path, data: dict) -> dict:
    if data.get("schema") != CATALOG_SCHEMA or not isinstance(data.get("documents"), list):
        raise ValueError("expected " + CATALOG_SCHEMA)
    revision(data["revision"])
    seen, text_cache = set(), {}
    for act in data["documents"]:
        if not SAFE.fullmatch(act["id"]) or act["id"] in seen:
            raise ValueError("duplicate or invalid source-act identity")
        seen.add(act["id"])
        if not act.get("text_available"):
            continue
        if act.get("completeness") != "complete" or act.get("language") not in LANGUAGES:
            raise ValueError("unresolved or mixed-language act cannot expose a complete body")
        path = resolve(root, act["text_path"])
        if path not in text_cache:
            payload = path.read_bytes()
            artifact = tomllib.loads((path.parent / "artifact.toml").read_text())
            if (artifact.get("storage") != "tracked" or artifact.get("media_type") != "text/plain"
                    or artifact.get("sha256") != sha(payload) or artifact.get("byte_size") != len(payload)
                    or resolve(root, artifact.get("path", "")) != path):
                raise ValueError("controlling source artifact ownership, hash, or extent mismatch")
            text_cache[path] = (payload, artifact)
        payload, artifact = text_cache[path]
        for name in ("sha256", "rights_status", "rights_basis"):
            if artifact.get(name) != act.get(name):
                raise ValueError("catalog disagrees with source artifact on " + name)
        if artifact.get("id") != act["artifact_id"]:
            raise ValueError("catalog disagrees with controlling artifact identity")
        bounds(act["physical_line_ranges"], len(physical_lines(payload)))
        segment = tomllib.loads(resolve(root, act["segment_path"]).read_text())
        for name, expected in (("schema", 2), ("record_type", "segment"), ("id", act["segment_id"]), ("edition_id", act["edition_id"]),
                               ("artifact_id", act["artifact_id"]), ("artifact_sha256", act["sha256"]), ("physical_line_ranges", act["physical_line_ranges"])):
            if segment.get(name) != expected:
                raise ValueError("catalog disagrees with source segment on " + name)
    expected = coverage(data["volumes"], data["documents"])
    if data.get("coverage") != expected:
        raise ValueError("catalog coverage counters disagree with actual records")
    return {"status": "valid", **expected}


def acquire(args: argparse.Namespace, root: Path) -> dict:
    data = json.loads(resolve(root, args.archives).read_text())
    stage = scratch(root, args.scratch)
    stage.mkdir(parents=True, exist_ok=True)
    receipts = []
    for volume in data["volumes"]:
        if (volume.get("series") not in {"ASS", "AAS"} or args.series and volume["series"] != args.series
                or args.volume and volume["volume"] not in args.volume):
            continue
        downloads = volume["downloads"]
        first_name = Path(urlsplit(downloads[0]["url"]).path).name
        annual = first_name.upper().startswith(("ASS-", "AAS-")) or "indice" in first_name.lower()
        chosen = downloads[:1] if annual else downloads
        for number, download in enumerate(chosen, 1):
            url = source_url(download["url"])
            filename = Path(unquote(urlsplit(url).path)).name
            if not filename or filename in {".", ".."}:
                raise ValueError("source URL has no safe PDF basename")
            matches = sorted((root / ".scratch").rglob(filename))
            destination = matches[0] if matches else stage / filename
            content_length = None
            if not destination.exists():
                with urlopen(Request(url, headers={"User-Agent": "Triptych archival source acquisition"}), timeout=180) as response:
                    source_url(response.geturl())
                    payload = response.read()
                    content_length = response.headers.get("Content-Length")
                if content_length and len(payload) != int(content_length):
                    raise ValueError("incomplete whole HTTP response for " + filename)
                if not payload.startswith(b"%PDF-"):
                    raise ValueError("download is not a PDF: " + filename)
                write(destination, payload, immutable=True)
            else:
                with urlopen(Request(url, method="HEAD", headers={"User-Agent": "Triptych archival source acquisition"}), timeout=180) as response:
                    source_url(response.geturl())
                    content_length = response.headers.get("Content-Length")
            payload = destination.read_bytes()
            if content_length and len(payload) != int(content_length):
                raise ValueError("cached PDF extent disagrees with the source HTTP Content-Length: " + filename)
            if not payload.startswith(b"%PDF-"):
                raise ValueError("cached download is not a PDF: " + filename)
            info = subprocess.run(["pdfinfo", str(destination)], check=True, capture_output=True, text=True).stdout
            match = re.search(r"^Pages:\s+(\d+)", info, re.M)
            if not match:
                raise ValueError("PDF page count unavailable")
            text_path = stage / (filename + ".txt")
            subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", "-eol", "unix", str(destination), str(text_path)], check=True, capture_output=True)
            text = text_path.read_bytes()
            identifier = volume["id"] + (".issue-" + str(number).zfill(2) if not annual else "")
            receipts.append({"archive_id": identifier, "parent_archive_id": volume["id"], "source_url": url,
                "pdf_path": relative(root, destination), "text_path": relative(root, text_path), "pdf_sha256": sha(payload), "pdf_bytes": len(payload),
                "text_sha256": sha(text), "text_bytes": len(text), "page_count": int(match[1]), "publication_year": volume["publication_year"],
                "metadata_only": volume["publication_year"] > 1930, "extraction_command": "pdftotext -layout -enc UTF-8 -eol unix", "limitations": [OCR_NOTE], "acts": [],
                "gaps": [{"kind": "unsegmented-volume", "detail": "Whole archival witness acquired; individual act identity, historical printing and boundaries await source review."}]})
    write_json(stage / "acquisition.json", {"schema": RECIPE_SCHEMA, "volumes": receipts})
    return {"status": "ok", "volumes": len(receipts), "receipt": relative(root, stage / "acquisition.json")}


def command(args: argparse.Namespace) -> dict:
    root = args.root.resolve()
    if args.verb == "acquire":
        return acquire(args, root)
    if args.verb in {"index", "register"}:
        volumes = read_recipes(root, args.recipes)
        result = catalog(root, volumes, args.revision, register=args.verb == "register")
        write_json(resolve(root, args.out), result)
        if args.verb == "register":
            write_json(resolve(root, args.manifest), make_manifest(result, args.revision))
        return {"status": "ok", **result["coverage"], "catalog": relative(root, resolve(root, args.out))}
    data = json.loads(resolve(root, args.catalog).read_text())
    if args.verb == "check":
        return validate_catalog(root, data)
    if args.verb == "manifest":
        validate_catalog(root, data)
        output = make_manifest(data, args.revision)
        write_json(resolve(root, args.out), output)
        return {"status": "ok", "documents": len(output["documents"]), "manifest": relative(root, resolve(root, args.out))}
    rows = [act for act in data["documents"] if not args.series or act["archive_id"].split(".")[1].upper() == args.series]
    if args.summary:
        return {"status": "ok", "count": len(rows), "complete_bounds": sum(act["completeness"] == "complete" for act in rows),
                "metadata_only": sum(act["completeness"] == "metadata-only" for act in rows), "unresolved": sum(act["completeness"] == "unresolved" for act in rows)}
    return {"status": "ok", "count": len(rows), "documents": [{key: act.get(key) for key in ("id", "title", "pope", "date", "document_type", "language", "completeness", "text_available")} for act in rows]}


def parser(examples: dict | None = None) -> argparse.ArgumentParser:
    p = examples_live_on_the_verbs(argparse.ArgumentParser(prog="papal-acta", description=__doc__), "papal-acta")
    sub = p.add_subparsers(dest="verb", required=True)
    helps = (("acquire", "acquire whole source-listed archival witnesses"), ("index", "merge reviewed source recipes as metadata"),
             ("register", "register historical derivatives and bounded act segments"), ("manifest", "select one historical witness per work and language"),
             ("check", "validate registered source boundaries and hashes"), ("list", "inspect source-act metadata"))
    for verb, help_text in helps:
        child = sub.add_parser(verb, help=help_text)
        child.add_argument("--root", type=Path, default=ROOT)
        child.add_argument("--json", action="store_true")
        if verb == "acquire":
            child.add_argument("--archives", type=Path, default=ARCHIVES)
            child.add_argument("--scratch", type=Path, default=Path(".scratch/acta_reconstruction/acquire"))
            child.add_argument("--series", choices=("ASS", "AAS"))
            child.add_argument("--volume", type=int, action="append")
        elif verb in {"index", "register"}:
            child.add_argument("--recipes", type=Path, action="append", required=True)
            child.add_argument("--revision", required=True)
            child.add_argument("--out", type=Path, default=CATALOG)
            if verb == "register":
                child.add_argument("--manifest", type=Path, default=MANIFEST)
        else:
            child.add_argument("--catalog", type=Path, default=CATALOG)
            if verb == "manifest":
                child.add_argument("--out", type=Path, default=MANIFEST)
                child.add_argument("--revision", required=True)
            if verb == "list":
                child.add_argument("--series", choices=("ASS", "AAS"))
                child.add_argument("--summary", action="store_true", help="print source record counts without individual titles")
        with_examples(child, (examples or {}).get(verb, ()))
    return p


def main(argv: list[str] | None = None, *, examples: dict | None = None) -> int:
    args = parser(examples).parse_args(argv)
    try:
        result = command(args)
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError, subprocess.CalledProcessError, URLError, HTTPException) as error:
        data = {"status": "error", "code": "input", "error": str(error), "v": 1}
        print(json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if args.json else "papal-acta: " + str(error), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result | {"v": 1}, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    else:
        for key, value in result.items():
            print(f"{key}\t{value}")
    return 0
