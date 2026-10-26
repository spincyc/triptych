"""Configured historical papal series: exact containers and reviewed constituents."""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tomllib
from urllib.parse import urlsplit
import urllib.request
import xml.etree.ElementTree as ET

import _bullarium as legacy
from _tooling import HEADING, with_examples

ROOT = Path(__file__).resolve().parents[1]
CONFIG_SCHEMA = "triptych-papal-series-config/v1"
CATALOG_SCHEMA = "triptych-papal-series-catalog/v1"
REVIEW_SCHEMA = "triptych-papal-series-boundary-reviews/v1"
TYPESET_SCHEMA = "triptych-papal-typeset/v1"
METHOD = "configured-papal-series-raw-lines-v1"
SERIES = {"bullarium-continuatio", "benedict-xiv-bullarium", "gregory-xvi-acta", "pius-ix-acta"}
DECISIONS = {"admit", "fragment", "hold", "duplicate", "non-papal", "non-act", "split"}
SHA256 = re.compile(r"[0-9a-f]{64}")
IDENTIFIER = re.compile(r"[a-z0-9]+(?:[.-][a-z0-9]+)*")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path) -> dict:
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    def invalid(value):
        raise ValueError(f"nonfinite JSON number: {value}")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique, parse_constant=invalid)


def revision(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value):
        raise ValueError("revision must be an explicit whole-second UTC instant")
    dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    return value


def local(root: Path, value: str | Path, *, scratch=False) -> Path:
    path = (root / value).resolve()
    boundary = (root / ".scratch").resolve() if scratch else root.resolve()
    if path == boundary or not path.is_relative_to(boundary):
        raise ValueError("path must stay below " + ("repository .scratch" if scratch else "repository root"))
    return path


def web_url(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("source URL must be text")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password or any(c.isspace() for c in value):
        raise ValueError("source URL must be an absolute public HTTPS URL")
    return value


def ranges(value, size: int | None = None) -> list[list[int]]:
    if not isinstance(value, list) or not value:
        raise ValueError("nonempty exact physical line ranges are required")
    end = 0
    for pair in value:
        if (not isinstance(pair, list) or len(pair) != 2 or any(type(n) is not int for n in pair)
                or not 0 < pair[0] <= pair[1] or pair[0] <= end or size is not None and pair[1] > size):
            raise ValueError("physical line ranges must be bounded, ordered and nonoverlapping")
        end = pair[1]
    return value


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + " must be nonempty text")
    return value


def paths_for(series: str) -> dict[str, str]:
    if series not in SERIES:
        raise ValueError("unregistered historical series namespace")
    prefix = "src/sources/papal-documents/" + series
    return {"config": prefix + "-config.json", "catalog": prefix + "-catalog.json",
            "manifest": prefix + "-manifest.json", "fragments": prefix + "-fragment-manifest.json"}


def validate_config(config: dict) -> dict:
    if not isinstance(config, dict) or config.get("schema") != CONFIG_SCHEMA:
        raise ValueError("unknown historical series configuration schema")
    paths_for(config.get("series_id"))
    _text(config.get("title"), "series title")
    revision(config.get("revision"))
    if not isinstance(config.get("volumes"), list) or not config["volumes"]:
        raise ValueError("configuration must identify at least one physical source container")
    seen = set()
    for volume in config["volumes"]:
        key = volume.get("key")
        if not isinstance(key, str) or not re.fullmatch(r"(?:volume-[0-9]{2}(?:-[0-9]{2})?|pars-[0-9]{2}-volume-[0-9]{2})", key) or key in seen:
            raise ValueError("physical source container keys must be unique zero-padded volume labels")
        seen.add(key)
        for field in ("title", "responsible", "publication", "printing_basis", "rights_basis"):
            _text(volume.get(field), key + " " + field)
        year = volume.get("publication_year")
        if type(year) is not int or not 1 <= year <= 1930:
            raise ValueError("historical publication year must be positively identified by 1930")
        if volume.get("language") not in {"la", "it", "en", "fr", "mul"}:
            raise ValueError("container language must identify the actual acquired printing")
        if not isinstance(volume.get("languages"), list) or not volume["languages"] or any(
                not re.fullmatch(r"[a-z]{2,3}", str(item)) for item in volume["languages"]):
            raise ValueError("container work languages must be explicit")
        if not re.fullmatch(r"[a-z]+(?:-[a-z]+)*", str(volume.get("place_slug", ""))):
            raise ValueError("printing place slug must be explicit lowercase text")
        bounds = ranges(volume.get("body_line_ranges"))
        evidence = volume.get("boundary_evidence")
        if not isinstance(evidence, dict) or not evidence.get("basis") or not evidence.get("contexts"):
            raise ValueError("body boundaries require literal source contexts and their reviewed basis")
        if not isinstance(volume.get("inputs"), dict) or not {"ocr", "xml", "imprint"} <= volume["inputs"].keys():
            raise ValueError("whole OCR, whole layout XML and inspected imprint input are required")
        for kind, source in volume["inputs"].items():
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", kind) or not isinstance(source, dict):
                raise ValueError("invalid input kind")
            web_url(source.get("source_url"))
            if not SHA256.fullmatch(str(source.get("sha256", ""))) or type(source.get("byte_size")) is not int or source["byte_size"] < 1:
                raise ValueError("every exact input needs its measured SHA-256 and size")
            filename = source.get("filename")
            if not isinstance(filename, str) or Path(filename).name != filename or filename in {".", ".."} or "\\" in filename:
                raise ValueError("input filename must be a single portable component")
            if source.get("sha1") is not None and not re.fullmatch(r"[0-9a-f]{40}", str(source["sha1"])):
                raise ValueError("invalid source-declared SHA-1")
            dt.date.fromisoformat(source["retrieved_on"][:10])
            _text(source.get("media_type"), "input media type")
            if source.get("storage", "tracked") not in {"tracked", "remote"}:
                raise ValueError("input storage must identify tracked or remote exact bytes")
            if source.get("storage") == "remote" and kind in {"ocr", "labels"}:
                raise ValueError("controlling OCR and embedded labels must remain tracked")
            if source.get("rights_status", "public-domain") not in {"public-domain", "unresolved"}:
                raise ValueError("historical inputs require an explicit supported source rights disposition")
            if source.get("rights_status") == "unresolved" and source.get("storage") != "remote":
                raise ValueError("unresolved full-wrapper rights require remote evidence storage")
            if source.get("rights_basis") is not None:
                _text(source["rights_basis"], "input-specific rights basis")
            generation = source.get("generation")
            if generation is not None:
                if (kind != "ocr" or not isinstance(generation, dict)
                        or generation.get("method") != "xml-word-line-text-v1" or generation.get("source_kind") != "xml"
                        or generation.get("source_sha256") != volume["inputs"]["xml"]["sha256"]
                        or generation.get("recipe_sha256") != sha(xml_text_recipe()) or source.get("sha1") is not None
                        or source["source_url"] != volume["inputs"]["xml"]["source_url"]):
                    raise ValueError("generated OCR must pin the exact XML parent and archived WORD/LINE replay recipe")
        if evidence.get("source_sha256") and evidence["source_sha256"] != volume["inputs"]["ocr"]["sha256"]:
            raise ValueError("body-boundary evidence identifies a different OCR witness")
        if not isinstance(volume.get("heading_patterns"), list):
            raise ValueError("heading patterns must be explicitly configured")
        for pattern in volume["heading_patterns"] + volume.get("protocol_patterns", []):
            re.compile(pattern)
        overrides = volume.get("heading_overrides", [])
        if not isinstance(overrides, list) or any(type(item.get("line")) is not int or not item.get("reason") for item in overrides):
            raise ValueError("heading exceptions require a line and source reason")
        for override in overrides:
            if not any(start <= override["line"] <= end for start, end in bounds):
                raise ValueError("heading exception lies outside configured body")
    return config


def load_config(root: Path, path: Path) -> dict:
    return validate_config(read_json(local(root, path)))


def _input_path(root: Path, cache: Path, volume: dict, kind: str) -> Path:
    source = volume["inputs"][kind]
    return local(root, cache / volume["key"] / (kind + "-" + source["sha256"][:12]) / source["filename"], scratch=True)


def exact_input(path: Path, source: dict) -> bytes:
    payload = path.read_bytes()
    if len(payload) != source["byte_size"] or sha(payload) != source["sha256"]:
        raise ValueError("whole input size or SHA-256 differs: " + path.name)
    if source.get("sha1") and hashlib.sha1(payload).hexdigest() != source["sha1"]:
        raise ValueError("whole input differs from provider-declared SHA-1: " + path.name)
    return payload


def acquire(root: Path, config: dict, cache: Path, input_map: dict | None = None) -> dict:
    imported = downloaded = reused = generated = generated_reused = generated_bytes = total = 0
    for volume in config["volumes"]:
        for kind, source in sorted(volume["inputs"].items(), key=lambda row: bool(row[1].get("generation"))):
            target = _input_path(root, cache, volume, kind)
            if source.get("generation"):
                xml_source = volume["inputs"]["xml"]
                xml_bytes = exact_input(_input_path(root, cache, volume, "xml"), xml_source)
                payload = xml_word_line_text(xml_bytes)
                if sha(payload) != source["sha256"] or len(payload) != source["byte_size"]:
                    raise ValueError("generated XML WORD/LINE text differs from its configured exact bytes")
                if target.exists():
                    exact_input(target, source)
                    generated_reused += 1
                else:
                    legacy.write(target, payload)
                    generated += 1
                generated_bytes += len(payload)
                continue
            if target.exists():
                exact_input(target, source)
                reused += 1
            elif input_map and source["sha256"] in input_map:
                origin = local(root, input_map[source["sha256"]])
                legacy.write(target, exact_input(origin, source))
                imported += 1
            else:
                request = urllib.request.Request(source["source_url"], headers={"User-Agent": "Triptych-Papal-Series/1 historical source acquisition"})
                with urllib.request.urlopen(request, timeout=180) as response:
                    payload = response.read()
                if len(payload) != source["byte_size"] or sha(payload) != source["sha256"] or source.get("sha1") and hashlib.sha1(payload).hexdigest() != source["sha1"]:
                    raise ValueError("download differs from exact configured whole input")
                legacy.write(target, payload)
                downloaded += 1
            total += source["byte_size"]
    return {"status": "ok", "containers": len(config["volumes"]), "responses_imported": imported,
            "responses_downloaded": downloaded, "responses_reused": reused, "representations_generated": generated,
            "representations_reused": generated_reused, "generated_representation_bytes": generated_bytes,
            "whole_response_bytes": total}


def _toml_value(value):
    if isinstance(value, dict):
        return "{ " + ", ".join(key + " = " + _toml_value(item) for key, item in value.items()) + " }"
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(item) for item in value) + "]"
    return legacy.toml_value(value)


def new_record(path: Path, record: dict):
    payload = ("\n".join(f"{key} = {_toml_value(value)}" for key, value in record.items()) + "\n").encode()
    if path.exists() and tomllib.loads(path.read_text(encoding="utf-8")) != record:
        raise ValueError("existing source record would change: " + str(path))
    legacy.write(path, payload)


def source_paths(root: Path, identifier: str, filename: str) -> list[Path]:
    return [path for path in (root / "src/sources/works").glob("*/*/" + filename)
            if tomllib.loads(path.read_text(encoding="utf-8")).get("id") == identifier]


def _container_owner(root: Path, config: dict, volume: dict) -> tuple[str, Path, str, Path]:
    series, key = config["series_id"], volume["key"]
    work_id = "work." + series + "." + key
    base = root / "src/sources/works" / series / key
    edition_key = f"{volume['publication_year']}-{volume['place_slug']}-{volume['language']}"
    edition_id = "edition." + series + "." + key + "." + edition_key
    owner = volume.get("canonical_container")
    if owner:
        if not owner.get("identity_evidence"):
            raise ValueError("existing container reuse requires positive printing/volume evidence")
        matches = source_paths(root, owner["work_id"], "work.toml")
        if len(matches) != 1:
            raise ValueError("configured canonical container work is absent or ambiguous")
        work_id, base = owner["work_id"], matches[0].parent
        if owner.get("edition_id"):
            editions = [p for p in base.glob("editions/*/edition.toml")
                        if tomllib.loads(p.read_text()).get("id") == owner["edition_id"]]
            if len(editions) != 1:
                raise ValueError("configured canonical printing is absent or ambiguous")
            edition_id, parent = owner["edition_id"], editions[0].parent
        else:
            edition_key = volume.get("edition_key", edition_key)
            if not re.fullmatch(str(volume["publication_year"]) + r"-[a-z0-9]+(?:-[a-z0-9]+)*", edition_key):
                raise ValueError("new source edition key must retain its identified printing-year prefix")
            edition_id = "edition." + work_id.removeprefix("work.") + "." + edition_key
            parent = base / "editions" / edition_key
    else:
        parent = base / "editions" / edition_key
    return work_id, base, edition_id, parent


def xml_word_line_text(xml_bytes: bytes) -> bytes:
    """Serialize every exact native WORD once, without inferring reading order."""
    output, expected = [], []

    def add_line(words):
        if words:
            output.append(" ".join(words))

    def walk(node):
        if node.tag == "LINE":
            add_line([token for word in node.iter("WORD") for token in "".join(word.itertext()).split()])
            return
        if node.tag == "WORD":
            add_line("".join(node.itertext()).split())
            return
        for child in node:
            walk(child)
        if node.tag in ("PARAGRAPH", "OBJECT"):
            output.append("")

    for _, obj in ET.iterparse(io.BytesIO(xml_bytes), events=("end",)):
        if obj.tag == "OBJECT":
            expected.extend(token for word in obj.iter("WORD") for token in "".join(word.itertext()).split())
            walk(obj)
            obj.clear()
    if not expected:
        raise ValueError("XML text serialization needs a nonempty native OBJECT/WORD stream")
    payload = ("\n".join(output) + "\n").encode("utf-8")
    if payload.decode("utf-8").split() != expected:
        raise ValueError("XML serialization does not preserve every native WORD token exactly once")
    return payload


def xml_text_recipe() -> bytes:
    source = Path(__file__).read_text(encoding="utf-8")
    function = next(ast.get_source_segment(source, node) for node in ast.parse(source).body
                    if isinstance(node, ast.FunctionDef) and node.name == "xml_word_line_text")
    wrapper = '''
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--xml", required=True, type=Path)
    p.add_argument("--xml-sha256", required=True)
    p.add_argument("--out", required=True, type=Path)
    a = p.parse_args()
    payload = a.xml.read_bytes()
    if hashlib.sha256(payload).hexdigest() != a.xml_sha256:
        raise ValueError("whole XML differs from its pinned SHA-256")
    a.out.write_bytes(xml_word_line_text(payload))
'''
    return ("import hashlib, io\nfrom pathlib import Path\nimport xml.etree.ElementTree as ET\n\n" + function + "\n" + wrapper).encode()


def register_xml_text_recipe(root: Path, when: str) -> str:
    payload = xml_text_recipe()
    base = root / "src/sources/works/triptych/historical-papal-line-mapping"
    # The established project processing-method work also owns this exact input
    # representation recipe; it never transfers papal source authorship to code.
    if not (base / "work.toml").exists():
        register_mapping_recipe(root, when)
    for path in base.glob("editions/*/artifacts/*/artifact.toml"):
        item = tomllib.loads(path.read_text(encoding="utf-8"))
        if item.get("sha256") == sha(payload):
            exact_input(local(root, item["path"]), item)
            return item["id"]
    work_id = "work.triptych.historical-papal-line-mapping"
    edition_key = when[:10] + "-xml-line-text-v1-" + sha(payload)[:8]
    edition_id = "edition.triptych.historical-papal-line-mapping." + edition_key
    parent = base / "editions" / edition_key
    new_record(parent / "edition.toml", {"schema": 1, "record_type": "edition", "id": edition_id,
        "work_id": work_id, "title": "Exact native XML WORD/LINE text serialization replay recipe",
        "language": "en", "date": when[:10], "publication": "Triptych project processing recipe, xml-word-line-text-v1",
        "notes": "Immutable archived implementation witness. The editable authority is scripts/_bullarium_series.py. This recipe preserves the XML word sequence and declares line/page whitespace; it neither repairs words nor establishes column reading order."})
    directory = parent / "artifacts" / ("recipe-" + sha(payload)[:12])
    target = directory / "rebuild-xml-line-text.py"
    legacy.write(target, payload)
    identifier = "artifact." + edition_id.removeprefix("edition.") + ".recipe-" + sha(payload)[:12]
    new_record(directory / "artifact.toml", {"schema": 1, "record_type": "artifact", "id": identifier,
        "edition_id": edition_id, "artifact_type": "mechanical-text-derivation-recipe", "media_type": "text/x-python",
        "storage": "tracked", "rights_status": "licensed", "license": "MIT", "retrieved": when[:10],
        "rights_basis": "Project-created software under the repository MIT license; historical input words retain their own rights.",
        "sha256": sha(payload), "byte_size": len(payload), "path": str(target.relative_to(root)),
        "provenance": "Self-contained immutable snapshot of the exact XML serialization function and SHA-pinned command-line replay. Shared across matching source representations, with Triptych contributors responsible for processing only."})
    return identifier


def mapping_recipe() -> bytes:
    source = Path(legacy.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = [ast.get_source_segment(source, node) for name in ("sha", "lines", "page_map")
                 for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(functions) != 3:
        raise ValueError("line-map implementation functions are unavailable")
    wrapper = '''
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--ocr", required=True, type=Path)
    p.add_argument("--xml", required=True, type=Path)
    p.add_argument("--labels", type=Path)
    p.add_argument("--recipe-id", required=True)
    p.add_argument("--out", required=True, type=Path)
    a = p.parse_args()
    labels = json.loads(a.labels.read_text()) if a.labels else {"pages": []}
    result = page_map(a.ocr.read_bytes(), a.xml, labels)
    digest = sha(Path(__file__).read_bytes())
    if not a.recipe_id.endswith(".recipe-" + digest[:12]):
        raise ValueError("recipe artifact ID does not identify these exact bytes")
    result["replay_recipe_artifact_id"] = a.recipe_id
    result["replay_recipe_sha256"] = digest
    result["source_inputs"] = {"ocr": "ocr.txt"}
    if a.labels:
        result["source_inputs"]["labels"] = "page_numbers.json"
    a.out.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\\n")
'''
    return ("import hashlib, json, re\nfrom pathlib import Path\nimport xml.etree.ElementTree as ET\n\n" + "\n\n".join(functions) + "\n" + wrapper).encode()


def register_mapping_recipe(root: Path, when: str) -> str:
    payload = mapping_recipe()
    base = root / "src/sources/works/triptych/historical-papal-line-mapping"
    for path in base.glob("editions/*/artifacts/*/artifact.toml"):
        item = tomllib.loads(path.read_text(encoding="utf-8"))
        if item.get("sha256") == sha(payload):
            exact_input(local(root, item["path"]), item)
            return item["id"]
    work_id = "work.triptych.historical-papal-line-mapping"
    work = {"schema": 1, "record_type": "work", "id": work_id,
        "title": "Exact token and line-to-leaf mapping for historical papal sources",
        "responsible": "Triptych contributors", "work_type": "processing-method", "languages": ["en"],
        "description": "Project software that checks complete OCR/XML token identity and records physical source lines and explicit scan leaf identifiers. The method does not establish textual accuracy, reading order or authenticity."}
    if not (base / "work.toml").exists():
        new_record(base / "work.toml", work)
    elif tomllib.loads((base / "work.toml").read_text()).get("id") != work_id:
        raise ValueError("shared mapping recipe work identity conflict")
    edition_key = when[:10] + "-v1-" + sha(payload)[:8]
    edition_id = "edition.triptych.historical-papal-line-mapping." + edition_key
    parent = base / "editions" / edition_key
    new_record(parent / "edition.toml", {"schema": 1, "record_type": "edition", "id": edition_id,
        "work_id": work_id, "title": "Standalone exact mapping replay recipe " + when[:10],
        "language": "en", "date": when[:10], "publication": "Triptych project processing recipe, " + METHOD,
        "notes": "Immutable archived implementation snapshot. The editable implementation remains in the registered tool's private module; this archive preserves the exact recipe for prior source artifacts."})
    directory = parent / "artifacts" / ("recipe-" + sha(payload)[:12])
    target = directory / "rebuild-line-map.py"
    legacy.write(target, payload)
    identifier = "artifact." + edition_id.removeprefix("edition.") + ".recipe-" + sha(payload)[:12]
    new_record(directory / "artifact.toml", {"schema": 1, "record_type": "artifact", "id": identifier,
        "edition_id": edition_id, "artifact_type": "mechanical-mapping-recipe", "media_type": "text/x-python",
        "storage": "tracked", "rights_status": "licensed", "license": "MIT", "rights_basis": "Project-created software under the repository MIT license; historical inputs retain their own rights.",
        "retrieved": when[:10],
        "sha256": sha(payload), "byte_size": len(payload), "path": str(target.relative_to(root)),
        "provenance": "Exact source extraction of the pure SHA, LF-line and whole-token mapping functions with a standalone command-line wrapper. One shared immutable recipe controls all matching series maps."})
    return identifier


def register_container(root: Path, config: dict, volume: dict, cache: Path, mapping: dict) -> dict:
    work_id, base, edition_id, parent = _container_owner(root, config, volume)
    if volume.get("container_work_id", work_id) != work_id or volume.get("container_edition_id", edition_id) != edition_id:
        raise ValueError("configured physical container identity differs from its registered owner")
    rights = volume["rights_basis"]
    if not volume.get("canonical_container"):
        new_record(base / "work.toml", {"schema": 1, "record_type": "work", "id": work_id,
            "title": volume["title"], "responsible": volume["responsible"], "work_type": "historical-document-container",
            "languages": volume["languages"], "description": "Historical collection containing acts, constituent instruments and editorial apparatus. Acquiring this container establishes no complete census or authentication of its acts."})
    if not volume.get("canonical_container", {}).get("edition_id"):
        new_record(parent / "edition.toml", {"schema": 1, "record_type": "edition", "id": edition_id,
            "work_id": work_id, "title": volume["title"] + f" — {volume['publication_year']}",
            "language": volume["language"], "date": str(volume["publication_year"]),
            "publication": volume["publication"], "notes": volume["printing_basis"] + " Raw OCR remains uncorrected and uncollated; automated page labels do not establish printed pagination."})
    artifacts = {}
    for kind, source in volume["inputs"].items():
        original = _input_path(root, cache, volume, kind)
        payload = exact_input(original, source)
        suffix = kind + "-" + sha(payload)[:12]
        directory = parent / "artifacts" / suffix
        artifact_id = "artifact." + edition_id.removeprefix("edition.") + "." + suffix
        if source.get("artifact_id", artifact_id) != artifact_id:
            raise ValueError("configured exact input artifact identity differs from its owner")
        remote = source.get("storage", "remote" if kind == "xml" else "tracked") == "remote"
        item = {"schema": 1, "record_type": "artifact", "id": artifact_id, "edition_id": edition_id,
            "artifact_type": {"ocr": "uncorrected-ocr", "xml": "ocr-layout-xml", "labels": "automated-pagination-map",
                              "scandata": "mechanical-scan-sequence", "imprint": "historical-title-page-image"}.get(kind, "historical-source-evidence"),
            "media_type": source["media_type"], "storage": "remote" if remote else "tracked",
            "rights_status": source.get("rights_status", "public-domain"), "rights_basis": source.get("rights_basis", rights), "rights_jurisdiction": "United States",
            "source_url": source["source_url"], "retrieved": source["retrieved_on"][:10],
            "sha256": sha(payload), "byte_size": len(payload),
            "provenance": "Whole exact response mechanically acquired and matched to configured size, SHA-256 and provider SHA-1 where recorded. " + source.get("purpose", ""),
            "notes": ((f"The exact {len(payload):,}-byte verbose XML remains remote for its measured size. Complete raw OCR, exact token/line/leaf correspondence and a standalone replay recipe are retained offline. " if kind == "xml"
                      else f"The complete {len(payload):,}-byte source evidence was acquired and measured; this artifact preserves its remote identity without claiming a different image representation. ")
                      if remote else "Exact whole offered response retained without changing its bytes. ") + "A token match or an imprint check does not establish complete image collation or act authentication."}
        if not remote:
            extension = {"text/plain": ".txt", "application/xml": ".xml", "application/json": ".json",
                         "image/jpeg": ".jpg", "image/png": ".png", "image/jp2": ".jp2", "application/pdf": ".pdf"}.get(source["media_type"])
            if extension is None:
                raise ValueError("unsupported retained source input media type")
            target = directory / (kind + extension)
            legacy.write(target, payload)
            item["path"] = str(target.relative_to(root))
        if kind == "ocr":
            item.update(indexable=True, encoding="utf-8")
        if kind == "imprint" and source["media_type"] == "application/pdf":
            item["artifact_type"] = "historical-printing-evidence-container"
        if source.get("generation"):
            recipe_id = register_xml_text_recipe(root, config["revision"])
            xml_source = volume["inputs"]["xml"]
            xml_id = "artifact." + edition_id.removeprefix("edition.") + ".xml-" + xml_source["sha256"][:12]
            item.update(artifact_type="uncorrected-xml-word-line-text", derived_from=xml_id,
                transformation="Serialize each native XML WORD whitespace token once in native LINE/OBJECT order, one space between tokens, LF after LINE and blank LF after PARAGRAPH/OBJECT. Replay with " + recipe_id + ".",
                provenance="Mechanical representation of exact XML SHA-256 " + xml_source["sha256"] + "; separately identified from any different offered TXT. Processing recipe SHA-256 " + source["generation"]["recipe_sha256"] + ".",
                notes="Generated input representation, not an HTTP response and not lexical correction. Native XML token order may interleave parallel columns or marginalia; individual extents remain held until reviewed.")
        new_record(directory / "artifact.toml", item)
        artifacts[kind] = {"id": artifact_id, "manifest": str((directory / "artifact.toml").relative_to(root)),
                           "sha256": sha(payload), "path": item.get("path")}
    recipe_id = register_mapping_recipe(root, config["revision"])
    mapping = {**mapping, "replay_recipe_artifact_id": recipe_id, "replay_recipe_sha256": sha(mapping_recipe()),
               "source_inputs": {"ocr": "ocr.txt"}}
    if "labels" in artifacts:
        mapping["source_inputs"]["labels"] = "page_numbers.json"
    payload = legacy.json_bytes(mapping)
    suffix = "line-map-" + sha(payload)[:12]
    directory = parent / "artifacts" / suffix
    target = directory / "line-map.json"
    legacy.write(target, payload)
    map_id = "artifact." + edition_id.removeprefix("edition.") + "." + suffix
    new_record(directory / "artifact.toml", {"schema": 1, "record_type": "artifact", "id": map_id,
        "edition_id": edition_id, "artifact_type": "mechanical-line-leaf-map", "media_type": "application/json",
        "storage": "tracked", "rights_status": "licensed", "license": "CC-BY-4.0",
        "retrieved": config["revision"][:10],
        "rights_basis": "Project-created factual correspondence data under CC BY 4.0; source words retain their separately identified historical rights.",
        "sha256": sha(payload), "byte_size": len(payload), "path": str(target.relative_to(root)),
        "derived_from": artifacts["xml"]["id"],
        "support_artifacts": [{"artifact_id": artifacts[kind]["id"], "embedded_reference": reference}
                              for kind, reference in mapping["source_inputs"].items()],
        "transformation": "Compare every whole TXT whitespace token with every XML WORD token; derive raw LF positions and leaf identifiers from explicit XML filenames. Automated labels join by leaf ID. Replay with " + recipe_id + ".",
        "provenance": "Mechanical correspondence over complete acquired inputs; no generated source text.",
        "notes": "Mapping pins exact OCR and XML hashes. Layout flags are conservative leads, not verified reading order or printed pagination."})
    return {"work_id": work_id, "edition_id": edition_id, "edition_path": str(parent.relative_to(root)),
            "artifacts": artifacts, "line_map_id": map_id, "line_map_path": str(target.relative_to(root)),
            "line_map_recipe_id": recipe_id, "rights_basis": rights}


def _literal_contexts(raw: list[str], evidence: dict):
    for context in evidence["contexts"]:
        bounds = ranges([context["physical_lines"]], len(raw))[0]
        actual = "\n".join(raw[bounds[0] - 1:bounds[1]])
        if actual != context["text"]:
            raise ValueError("configured boundary context is not literal source text")


def discover(ocr: bytes, volume: dict, mapping: dict, series: str) -> list[dict]:
    raw = legacy.lines(ocr)
    bounds = ranges(volume["body_line_ranges"], len(raw))
    _literal_contexts(raw, volume["boundary_evidence"])
    patterns = [re.compile(pattern) for pattern in volume["heading_patterns"]]
    protocol_patterns = [re.compile(pattern, re.I | re.M) for pattern in volume.get("protocol_patterns", [])]
    overrides = {item["line"]: item for item in volume.get("heading_overrides", [])}
    units = []
    for body_start, body_end in bounds:
        found = {}
        for number in range(body_start, body_end + 1):
            value = raw[number - 1].strip()
            match = next((match for pattern in patterns if (match := pattern.fullmatch(value))), None)
            if match:
                token = match.groupdict().get("number", value)
                found[number] = {"heading_line": number, "selection_start": number,
                                 "act_number_raw": token, "act_number": int(token) if token.isdigit() else legacy.numeral(token)}
        for number, override in overrides.items():
            if body_start <= number <= body_end:
                start = override.get("selection_start", number)
                if type(start) is not int or not body_start <= start <= number:
                    raise ValueError("heading selection start must remain inside its body range")
                prefix = [line for line in found if start <= line < number]
                for line in prefix:
                    del found[line]
                token = override.get("act_number_raw")
                found[number] = {"heading_line": number, "selection_start": start,
                    "act_number_raw": token, "act_number": int(token) if isinstance(token, str) and token.isdigit() else legacy.numeral(token) if token else None,
                    "heading_exception": {**override, "suppressed_prefix_heading_lines": prefix}}
        if not found or min(item["selection_start"] for item in found.values()) > body_start:
            found[body_start] = {"heading_line": body_start, "selection_start": body_start,
                                 "act_number_raw": None, "act_number": None,
                                 "heading_exception": {"reason": "Configured body begins before a recognized numeral; source extent retained for review."}}
        starts = sorted(found.values(), key=lambda item: (item["selection_start"], item["heading_line"]))
        if len({item["selection_start"] for item in starts}) != len(starts):
            raise ValueError("configured headings share a selection start")
        for index, item in enumerate(starts):
            start = item["selection_start"]
            end = starts[index + 1]["selection_start"] - 1 if index + 1 < len(starts) else body_end
            while end > start and not raw[end - 1].strip():
                end -= 1
            window = "\n".join(raw[item["heading_line"] - 1:min(end, item["heading_line"] + 240)])
            protocol = None
            for pattern in protocol_patterns:
                match = pattern.search(window)
                if match:
                    protocol = {"raw": match[0], "line": item["heading_line"] + window[:match.start()].count("\n")}
                    break
            pages = [p for p in mapping["pages"] if p["physical_line_start"] is not None
                     and p["physical_line_start"] <= end and p["physical_line_end"] >= start]
            holds = ["unreviewed-constituent-boundaries-and-reading-order"]
            if not protocol:
                holds.append("papal-issuer-not-established")
            holds.extend(sorted({reason for page in pages for reason in page["layout_hold_reasons"]}))
            units.append({**item, "id": f"{series}.{volume['key']}.line-{start:08d}", "volume_key": volume["key"],
                "title_raw": " ".join(value.strip() for value in raw[item["heading_line"] - 1:min(end, item["heading_line"] + 18)] if value.strip()),
                "source_heading_raw": raw[item["heading_line"] - 1], "date": None,
                "date_raw": [{"line": n, "raw": "\n".join(raw[n - 1:min(n + 5, end)])}
                             for n in range(start, end + 1) if legacy.DATE.search(raw[n - 1])],
                "protocol": protocol, "physical_line_ranges": [[start, end]],
                "artifact_pages": [p["artifact_page"] for p in pages], "scan_leaf_ids": [p["leaf"] for p in pages],
                "status": "held", "hold_reasons": holds,
                "boundary_evidence": {"next_heading_line": starts[index + 1]["heading_line"] if index + 1 < len(starts) else None,
                                      "body_range": [body_start, body_end]}})
    return units


def prepare(root: Path, config: dict, cache: Path, when: str) -> dict:
    revision(when)
    target = root / paths_for(config["series_id"])["catalog"]
    previous = read_json(target) if target.exists() else {"documents": []}
    old = {item["id"]: item for item in previous["documents"]}
    volumes, documents, prepared = [], [], []
    retained_ids = set()
    # Complete discovery and review-preservation checks for every volume before
    # registering even one container. A changed configuration cannot silently
    # retire reviewed history or leave its still-active reader orphaned.
    for volume in config["volumes"]:
        ocr = exact_input(_input_path(root, cache, volume, "ocr"), volume["inputs"]["ocr"])
        xml = _input_path(root, cache, volume, "xml")
        exact_input(xml, volume["inputs"]["xml"])
        labels = read_json(_input_path(root, cache, volume, "labels")) if "labels" in volume["inputs"] else {"pages": []}
        mapping = legacy.page_map(ocr, xml, labels)
        candidates = discover(ocr, volume, mapping, config["series_id"])
        edition_id = _container_owner(root, config, volume)[2]
        controller = "artifact." + edition_id.removeprefix("edition.") + ".ocr-" + sha(ocr)[:12]
        for item in candidates:
            retained_ids.add(item["id"])
            prior = old.get(item["id"])
            if prior and prior.get("review"):
                if (prior["artifact_sha256"] != sha(ocr) or prior["artifact_id"] != controller
                        or prior["heading_line"] != item["heading_line"]):
                    raise ValueError("a reviewed discovery identity changed")
        for prior in previous["documents"]:
            if prior.get("parent_id") and prior["volume_key"] == volume["key"]:
                if prior["artifact_sha256"] != sha(ocr) or prior["artifact_id"] != controller:
                    raise ValueError("a reviewed constituent source changed")
                retained_ids.add(prior["id"])
        prepared.append((volume, ocr, mapping, candidates))
    lost = sorted(item["id"] for item in previous["documents"]
                  if (item.get("review") or item.get("status") in {"admitted-complete", "admitted-fragment"})
                  and item["id"] not in retained_ids)
    if lost:
        raise ValueError("a reviewed discovery would disappear; explicit source reconciliation is required: " + ", ".join(lost))
    for volume, ocr, mapping, candidates in prepared:
        container = register_container(root, config, volume, cache, mapping)
        for item in candidates:
            item.update(artifact_id=container["artifacts"]["ocr"]["id"], artifact_sha256=sha(ocr), line_map_id=container["line_map_id"])
            prior = old.get(item["id"])
            documents.append(prior if prior and prior.get("review") else item)
        for prior in previous["documents"]:
            if prior.get("parent_id") and prior["volume_key"] == volume["key"]:
                documents.append(prior)
        volumes.append({"key": volume["key"], "title": volume["title"], "language": volume["language"],
                        "publication_year": volume["publication_year"], "container": container,
                        "physical_lines": mapping["physical_line_count"], "artifact_pages": len(mapping["pages"]),
                        "body_line_ranges": volume["body_line_ranges"], "candidate_documents": len(candidates)})
    catalog = {"schema": CATALOG_SCHEMA, "series_id": config["series_id"], "revision": when,
               "config_sha256": sha(legacy.json_bytes(config)), "method": METHOD,
               "scope": "Configured historical source containers and proposed constituents; no complete historical papal-act census or authenticity determination.",
               "volumes": volumes, "documents": sorted(documents, key=lambda item: item["id"])}
    catalog["coverage"] = coverage(catalog)
    legacy.write(target, legacy.json_bytes(catalog))
    for kind in ("manifest", "fragments"):
        manifest_path = root / paths_for(config["series_id"])[kind]
        if not manifest_path.exists():
            legacy.write(manifest_path, legacy.json_bytes({"schema": TYPESET_SCHEMA, "revision": when, "documents": [],
                "source_note": "Raw source candidates remain held until their individual boundaries, issuer, language and source extent have been reviewed. No whole-volume or placeholder act readers are selected."}))
    return {"status": "ok", **catalog["coverage"]}


def coverage(catalog: dict) -> dict:
    return {"source_containers": len(catalog["volumes"]), "raw_candidates": sum(not item.get("parent_id") for item in catalog["documents"]),
            "complete_printed_witnesses": sum(item["status"] == "admitted-complete" for item in catalog["documents"]),
            "fragment_witnesses": sum(item["status"] == "admitted-fragment" for item in catalog["documents"]),
            "unreviewed_candidates": sum(item["status"] == "held" for item in catalog["documents"]),
            "specifically_held": sum(item["status"] == "specifically-held" for item in catalog["documents"]),
            "note": "Candidates include false headings and non-papal units. Counts describe source witnesses, not authenticated unique acts."}


def _literal(raw, bounds, text):
    start, end = ranges([bounds], len(raw))[0]
    literal = " ".join("\n".join(raw[start - 1:end]).split())
    if " ".join(text.split()) not in literal:
        raise ValueError("reviewed metadata is not literal at its pinned source locus")


def _review_attribution(root: Path, raw: list[str], item: dict, bounds: list[list[int]], volume: dict):
    locus = ranges([item["source_attribution_lines"]], len(raw))[0]
    _literal(raw, locus, item["printed_attribution"])
    inside = any(start <= locus[0] <= locus[1] <= end for start, end in bounds)
    context = item.get("source_attribution_context")
    if inside and not context:
        return
    if not isinstance(context, dict) or context.get("kind") not in {"shared-running-header", "pontificate-section-heading"}:
        raise ValueError("outside-body issuer requires a bounded reviewed running-header or section-heading context")
    if context.get("artifact_sha256") != item["artifact_sha256"]:
        raise ValueError("attribution context does not pin the exact source artifact")
    _text(context.get("basis"), "per-act attribution context basis")
    scope = ranges(context.get("scope_line_ranges"), len(raw))
    if not all(any(a <= start <= end <= b for a, b in scope) for start, end in bounds):
        raise ValueError("act extent escapes the reviewed attribution scope")
    proof = context.get("protocol_and_closing_review")
    if not isinstance(proof, dict) or proof.get("finding") != "consistent" or proof.get("conflicting_issuer"):
        raise ValueError("attribution context is contradicted or unresolved by the act protocol/closing")
    _text(proof.get("basis"), "act protocol/closing consistency basis")
    for field in ("protocol_lines", "closing_lines"):
        start, end = ranges([proof.get(field)], len(raw))[0]
        if not any(a <= start <= end <= b for a, b in bounds):
            raise ValueError("attribution consistency evidence is outside the selected act")
    mapping_path = local(root, volume["container"]["line_map_path"])
    metadata = tomllib.loads((mapping_path.parent / "artifact.toml").read_text())
    if metadata["id"] != volume["container"]["line_map_id"] or sha(mapping_path.read_bytes()) != metadata["sha256"]:
        raise ValueError("attribution context page map changed")
    mapping = read_json(mapping_path)
    actual = {(page["artifact_page"], page["leaf"]) for page in mapping["pages"]
              if page["physical_line_start"] is not None
              and page["physical_line_start"] <= locus[1] and page["physical_line_end"] >= locus[0]}
    evidence = context.get("page_evidence")
    if not isinstance(evidence, list) or not evidence:
        raise ValueError("attribution context needs exact source page/leaf evidence")
    declared = set()
    for page in evidence:
        if type(page.get("artifact_page")) is not int or type(page.get("leaf")) is not int:
            raise ValueError("attribution evidence page/leaf must be literal integers")
        _text(page.get("basis"), "source page attribution evidence")
        declared.add((page["artifact_page"], page["leaf"]))
    if declared != actual or not actual:
        raise ValueError("attribution context page/leaf evidence differs from exact source correspondence")


def _review_fragment(raw: list[str], item: dict, bounds: list[list[int]]):
    if item.get("decision") != "fragment":
        return
    if item.get("extent_kind") != "fragment" or "fragment" not in item["title"].lower() or not item.get("missing_content"):
        raise ValueError("historical fragment requires a visible title and missing-content finding")
    evidence = item.get("substantive_fragment_evidence")
    if not isinstance(evidence, dict) or evidence.get("finding") != "substantive-body-survives":
        raise ValueError("fragment reader requires surviving substantive body; protocol/incipit-only references remain held")
    _text(evidence.get("basis"), "substantive fragment basis")
    for start, end in ranges(evidence.get("physical_line_ranges"), len(raw)):
        if not any(a <= start <= end <= b for a, b in bounds):
            raise ValueError("substantive fragment evidence escapes the selected source extent")
    literal = _text(evidence.get("literal"), "surviving substantive source wording")
    if not any(" ".join(literal.split()) in " ".join("\n".join(raw[a - 1:b]).split())
               for a, b in evidence["physical_line_ranges"]):
        raise ValueError("substantive fragment evidence is not literal at its source locus")


def _review_editorial_omission(raw: list[str], item: dict, bounds: list[list[int]]):
    evidence = item.get("editorial_omission_review")
    if evidence is None:
        return
    if (not isinstance(evidence, dict) or evidence.get("finding") != "non-substantive-publishing-furniture"
            or evidence.get("outside_papal_text") is not True or evidence.get("not_substantive_historical_note") is not True):
        raise ValueError("editorial omission needs positive proof outside papal text and substantive historical notes")
    _text(evidence.get("basis"), "editorial omission identification basis")
    _text(item.get("reader_source_note"), "reader qualification for the editorial omission")
    loci = evidence.get("omitted_loci")
    if not isinstance(loci, list) or not loci:
        raise ValueError("editorial omission requires exact excluded source loci")
    for locus in loci:
        _text(locus.get("basis"), "excluded source locus basis")
        if "physical_lines" in locus:
            start, end = ranges([locus["physical_lines"]], len(raw))[0]
            if any(max(start, a) <= min(end, b) for a, b in bounds):
                raise ValueError("excluded editorial locus overlaps selected papal text")
            _literal(raw, [start, end], _text(locus.get("literal"), "excluded literal source block"))
        else:
            web_url(locus.get("source_url"))
            if (not SHA256.fullmatch(str(locus.get("sha256", "")))
                    or type(locus.get("byte_size")) is not int or locus["byte_size"] < 1
                    or type(locus.get("artifact_page")) is not int or locus["artifact_page"] < 1
                    or type(locus.get("leaf")) is not int or locus["leaf"] < 0):
                raise ValueError("OCR-absent editorial caption needs an exact whole native-page image pin")
            box = locus.get("image_bounds")
            if (not isinstance(box, list) or len(box) != 4 or any(type(n) is not int or n < 0 for n in box)
                    or not box[0] < box[2] or not box[1] < box[3]):
                raise ValueError("OCR-absent editorial caption needs its bounded native image locus")
            _text(locus.get("printed_caption"), "identified native editorial caption")


def _review_recorded_rescript(raw: list[str], item: dict, bounds: list[list[int]], *, root=None, volume=None):
    if item.get("document_form") != "recorded-audience-rescript":
        return
    evidence = item.get("recorded_rescript_evidence")
    if not isinstance(evidence, dict):
        raise ValueError("recorded audience rescript requires its documentary-form evidence")
    _text(item.get("recording_official"), "recording official or office")
    _text(item.get("papal_context"), "papal context")
    _text(evidence.get("basis"), "recorded rescript identification basis")
    for field, literal in (("audience_lines", "audience_formula"), ("response_lines", "response_formula"),
                           ("date_lines", "date_raw"), ("subscription_lines", None)):
        start, end = ranges([evidence.get(field)], len(raw))[0]
        if not any(a <= start <= end <= b for a, b in bounds):
            raise ValueError("recorded rescript evidence escapes its selected documentary extent")
        _literal(raw, [start, end], item["recording_official"] if literal is None else _text(evidence.get(literal), literal))
    if not re.search(r"audientia", evidence["audience_formula"], re.I):
        native = evidence.get("native_audience_evidence")
        if not isinstance(native, dict) or root is None or volume is None:
            raise ValueError("recorded audience rescript lacks its literal audience formula or registered native-image evidence")
        _text(native.get("basis"), "native audience-formula inspection basis")
        if not re.search(r"\bex\s+audientia\b", _text(native.get("printed_formula"), "printed audience formula"), re.I):
            raise ValueError("native image must positively identify the printed ex-audientia formula")
        image_records = [value for value in volume["container"]["artifacts"].values()
                         if value["id"] == native.get("artifact_id")]
        if len(image_records) != 1:
            raise ValueError("native audience image must be an exact registered artifact of this source container")
        image_record = tomllib.loads(local(root, image_records[0]["manifest"]).read_text())
        if (image_record["sha256"] != native.get("artifact_sha256")
                or not image_record["media_type"].startswith("image/") or image_record["storage"] != "tracked"):
            raise ValueError("native audience evidence differs from its registered whole image")
        exact_input(local(root, image_record["path"]), image_record)
        mapping_path = local(root, volume["container"]["line_map_path"])
        metadata = tomllib.loads((mapping_path.parent / "artifact.toml").read_text())
        if metadata["id"] != volume["container"]["line_map_id"] or sha(mapping_path.read_bytes()) != metadata["sha256"]:
            raise ValueError("native audience evidence page map changed")
        start, end = evidence["audience_lines"]
        actual = {(page["artifact_page"], page["leaf"]) for page in read_json(mapping_path)["pages"]
                  if page["physical_line_start"] is not None
                  and page["physical_line_start"] <= end and page["physical_line_end"] >= start}
        if any(type(native.get(key)) is not int for key in ("artifact_page", "leaf")) or actual != {(native["artifact_page"], native["leaf"])}:
            raise ValueError("native audience evidence differs from the exact source page/leaf")


def admit(root: Path, config: dict, review_paths: list[Path], when: str) -> dict:
    revision(when)
    paths = paths_for(config["series_id"])
    catalog = read_json(root / paths["catalog"])
    units = {item["id"]: item for item in catalog["documents"]}
    volumes = {item["key"]: item for item in catalog["volumes"]}
    configs = {item["key"]: item for item in config["volumes"]}
    staged, seen = [], set()
    # Validate every requested decision before writing any constituent records.
    for path in review_paths:
        packet = read_json(path)
        if packet.get("schema") != REVIEW_SCHEMA or packet.get("series_id") != config["series_id"]:
            raise ValueError("boundary review has the wrong series or schema")
        pending = list(packet.get("reviews", [])) + list(packet.get("extra_dispositions", []))
        for item in pending:
            identifier = item.get("document_id")
            if identifier not in units and item.get("parent_id") in units:
                parent = units[item["parent_id"]]
                if (not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier)
                        or not identifier.startswith(parent["id"] + ".") or item.get("artifact_sha256") != parent["artifact_sha256"]):
                    raise ValueError("additional source discovery must identify its exact parent and artifact")
                child_ranges = ranges(item.get("physical_line_ranges"))
                units[identifier] = {**parent, "id": identifier, "parent_id": parent["id"],
                                     "heading_line": item.get("heading_line", child_ranges[0][0]),
                                     "act_number_raw": item.get("act_number_raw"), "act_number": None,
                                     "protocol": None, "physical_line_ranges": child_ranges, "status": "held"}
                units[identifier].pop("review", None)
                units[identifier].pop("segment_id", None)
                units[identifier].pop("segment_path", None)
            if identifier not in units or identifier in seen:
                raise ValueError("review document ID is missing or repeated")
            seen.add(identifier)
            unit, decision = units[identifier], item.get("decision")
            if decision not in DECISIONS:
                raise ValueError("unknown reviewed disposition")
            if item.get("artifact_sha256") != unit["artifact_sha256"]:
                raise ValueError("review does not pin the exact acquired OCR")
            _text(item.get("review_note"), "review note")
            if unit.get("review") and unit["review"] != legacy.durable_review(item):
                raise ValueError("an existing reviewed disposition requires explicit supersession rather than overwrite")
            if decision == "split":
                if not isinstance(item.get("constituents"), list) or not item["constituents"]:
                    raise ValueError("a compound proposal requires reviewed constituent dispositions")
                for index, child in enumerate(item["constituents"], 1):
                    pending.append({**child, "document_id": identifier + f".part-{index:02d}",
                                    "parent_id": identifier, "artifact_sha256": unit["artifact_sha256"]})
                staged.append((unit, item, None, None))
                continue
            if decision not in {"admit", "fragment"}:
                staged.append((unit, item, None, None))
                continue
            volume = volumes[unit["volume_key"]]
            artifact = tomllib.loads(local(root, volume["container"]["artifacts"]["ocr"]["manifest"]).read_text())
            raw = legacy.lines(exact_input(local(root, artifact["path"]), artifact))
            bounds = ranges(item.get("physical_line_ranges"), len(raw))
            if unit.get("parent_id"):
                unit["source_heading_raw"] = raw[unit["heading_line"] - 1]
                unit["title_raw"] = unit["source_heading_raw"]
            for key in ("title", "printed_attribution", "reviewed_extent", "language", "genre"):
                _text(item.get(key), key)
            if not re.fullmatch(r"[a-z]{2,3}", item["language"]):
                raise ValueError("reviewed constituent language must be explicit")
            _review_attribution(root, raw, item, bounds, volume)
            _review_recorded_rescript(raw, item, bounds, root=root, volume=volume)
            _review_editorial_omission(raw, item, bounds)
            if not item.get("boundary_review") or not item.get("reading_order_review") or not item.get("source_extent_review"):
                raise ValueError("admission requires explicit boundary, reading-order and source-extent findings")
            if item.get("date") is not None:
                dt.date.fromisoformat(item["date"])
                if not item.get("date_evidence"):
                    raise ValueError("normalized date requires its source evidence")
            _review_fragment(raw, item, bounds)
            if item.get("canonical_work_id"):
                proof = item.get("identity_evidence", {})
                if proof.get("existing_work_id") != item["canonical_work_id"] or not all(proof.get(key) for key in ("issuer", "date", "incipit", "body", "basis")):
                    raise ValueError("existing act join requires positive issuer/date/incipit/body evidence")
                matches = source_paths(root, item["canonical_work_id"], "work.toml")
                if len(matches) != 1:
                    raise ValueError("existing act identity is absent or ambiguous")
            staged.append((unit, item, artifact, bounds))
    active = {item["id"]: item for item in catalog["documents"] if item["status"] in {"admitted-complete", "admitted-fragment"} and item["id"] not in seen}
    for unit, item, artifact, bounds in staged:
        if bounds is None:
            continue
        for other, other_item, other_art, other_bounds in staged:
            if other["id"] >= unit["id"] or other_bounds is None or other_art["id"] != artifact["id"]:
                continue
            if any(max(a, c) <= min(b, d) for a, b in bounds for c, d in other_bounds):
                raise ValueError("independently admitted extents overlap")
        for prior in active.values():
            if prior["artifact_id"] == artifact["id"] and any(max(a, c) <= min(b, d) for a, b in bounds for c, d in prior["review"]["physical_line_ranges"]):
                raise ValueError("new admission overlaps an existing admitted constituent")
    for unit, item, artifact, bounds in staged:
        unit["review"] = legacy.durable_review(item)
        if bounds is None:
            unit["status"] = {"hold": "specifically-held", "duplicate": "duplicate-witness", "non-papal": "non-papal-source-unit", "non-act": "not-an-independent-act", "split": "split-into-constituents"}[item["decision"]]
            continue
        volume, config_volume = volumes[unit["volume_key"]], configs[unit["volume_key"]]
        fragment = item["decision"] == "fragment"
        work_id = item.get("canonical_work_id", "work." + unit["id"])
        base = source_paths(root, work_id, "work.toml")[0].parent if item.get("canonical_work_id") else root / "src/sources/works" / config["series_id"] / unit["id"].removeprefix(config["series_id"] + ".").replace(".", "-")
        edition_key = f"{config_volume['publication_year']}-{config['series_id']}-{unit['volume_key']}-{item['language']}"
        edition_id = "edition." + work_id.removeprefix("work.") + "." + edition_key
        parent = base / "editions" / edition_key
        note = item["review_note"] + " Exact source extent and surrounding boundaries were inspected as uncorrected OCR; no complete print-image collation or historical authentication is claimed."
        recorded = item.get("document_form") == "recorded-audience-rescript"
        responsible = item.get("source_responsible", item["recording_official"]) if recorded else item["printed_attribution"]
        if recorded:
            note += " A formally recorded papal response, attributed to its recording official or office; papal context: " + item["papal_context"] + "."
        if not item.get("canonical_work_id"):
            new_record(base / "work.toml", {"schema": 1, "record_type": "work", "id": work_id,
                "title": item["title"], "responsible": responsible,
                "work_type": "historical-papal-act-fragment" if fragment else "recorded-papal-response" if recorded else "historically-attributed-papal-act",
                "languages": item.get("languages", [item["language"]]), "description": note, "relations": [volume["container"]["work_id"]]})
        new_record(parent / "edition.toml", {"schema": 1, "record_type": "edition", "id": edition_id,
            "work_id": work_id, "title": item["title"] + " — " + config_volume["publication"],
            "language": item["language"], "date": str(config_volume["publication_year"]),
            "publication": config_volume["publication"], "notes": note})
        segment_id = "segment." + work_id.removeprefix("work.") + "." + edition_key + ".source-ocr"
        segment_path = parent / "segments/source-ocr.toml"
        new_record(segment_path, {"schema": 2, "record_type": "segment", "id": segment_id,
            "edition_id": edition_id, "artifact_id": artifact["id"], "artifact_sha256": artifact["sha256"],
            "segment_type": "constituent-fragment" if fragment else "constituent-work", "physical_line_ranges": bounds,
            "states": ["cataloged", "acquired", "inspected"], "context": note,
            "notes": "Review extent: " + item["reviewed_extent"] + (" Missing content: " + item["missing_content"] if fragment else "")})
        unit.update(status="admitted-fragment" if fragment else "admitted-complete", work_id=work_id,
                    edition_id=edition_id, segment_id=segment_id, segment_path=str(segment_path.relative_to(root)),
                    render_revision=unit.get("render_revision", when))
    catalog["documents"] = sorted(units.values(), key=lambda item: item["id"])
    catalog["revision"], catalog["coverage"] = when, coverage(catalog)
    legacy.write(root / paths["catalog"], legacy.json_bytes(catalog))
    manifests = {False: [], True: []}
    for unit in catalog["documents"]:
        if unit["status"] not in {"admitted-complete", "admitted-fragment"}:
            continue
        item, volume = unit["review"], volumes[unit["volume_key"]]
        artifact = tomllib.loads(local(root, volume["container"]["artifacts"]["ocr"]["manifest"]).read_text())
        fragment = unit["status"] == "admitted-fragment"
        recorded = item.get("document_form") == "recorded-audience-rescript"
        responsible = item.get("source_responsible", item["recording_official"]) if recorded else item["printed_attribution"]
        manifests[fragment].append({"id": unit["id"], "title": item["title"], "pope": responsible,
            "revision": unit["render_revision"],
            "date": item.get("date"), "document_type": item["genre"], "language": item["language"],
            "source_url": artifact["source_url"], "text_path": artifact["path"], "artifact_id": artifact["id"],
            "sha256": artifact["sha256"], "segment_id": unit["segment_id"], "segment_path": unit["segment_path"],
            "physical_line_ranges": item["physical_line_ranges"], "rights_status": artifact["rights_status"],
            "rights_basis": artifact["rights_basis"], "extent_kind": "fragment" if fragment else "printed-act",
            "source_note": configs[unit["volume_key"]]["publication"] + " Uncorrected, uncollated OCR transcription of the identified constituent. " +
                ("Complete papal body; editorial caption or non-substantive publishing furniture omitted as separately identified in the source review. " if item.get("editorial_omission_review")
                 else "Historical synopsis, source notes, dating and subscriptions are retained as this witness gives them; literal abbreviations are not expanded. ") +
                item.get("reader_source_note", "") + (" Missing content: " + item["missing_content"] if fragment else ""),
            "rights_notice": "Historical source wording is public domain in the United States; project typesetting does not relicense it."})
        if item.get("language_label"):
            manifests[fragment][-1]["language_label"] = item["language_label"]
        if recorded:
            manifests[fragment][-1]["pope_context"] = item["papal_context"]
            manifests[fragment][-1]["source_note"] += " A papal audience response recorded by " + item["recording_official"] + "; papal context: " + item["papal_context"] + "."
    for fragment, rows in manifests.items():
        legacy.write(root / paths["fragments" if fragment else "manifest"], legacy.json_bytes({"schema": TYPESET_SCHEMA, "revision": when, "documents": rows}))
    return {"status": "ok", **catalog["coverage"]}


def check(root: Path, config: dict) -> dict:
    catalog = read_json(root / paths_for(config["series_id"])["catalog"])
    if catalog.get("schema") != CATALOG_SCHEMA or catalog.get("series_id") != config["series_id"]:
        raise ValueError("catalog schema or source series mismatch")
    seen, sources = set(), {}
    for volume in catalog["volumes"]:
        for item in volume["container"]["artifacts"].values():
            record = tomllib.loads(local(root, item["manifest"]).read_text())
            if record["id"] != item["id"] or record["sha256"] != item["sha256"]:
                raise ValueError("source artifact identity mismatch")
            if record["storage"] == "tracked":
                exact_input(local(root, record["path"]), record)
            sources[record["id"]] = record
    for item in catalog["documents"]:
        if item["id"] in seen or item["artifact_id"] not in sources or item["artifact_sha256"] != sources[item["artifact_id"]]["sha256"]:
            raise ValueError("duplicate discovery or changed controlling source")
        seen.add(item["id"])
        if item["status"] != "held" and not item.get("review"):
            raise ValueError("source candidate was promoted without review")
        if item["status"] in {"admitted-complete", "admitted-fragment"}:
            segment = tomllib.loads(local(root, item["segment_path"]).read_text())
            if segment["id"] != item["segment_id"] or segment["artifact_sha256"] != item["artifact_sha256"] or segment["physical_line_ranges"] != item["review"]["physical_line_ranges"]:
                raise ValueError("reviewed constituent differs from its source pin")
    if catalog["coverage"] != coverage(catalog):
        raise ValueError("catalog coverage counters are stale")
    units = {item["id"]: item for item in catalog["documents"]}
    for kind, status in (("manifest", "admitted-complete"), ("fragments", "admitted-fragment")):
        manifest = read_json(root / paths_for(config["series_id"])[kind])
        if manifest.get("schema") != TYPESET_SCHEMA or not isinstance(manifest.get("documents"), list):
            raise ValueError("active series manifest has the wrong schema")
        selected = set()
        for row in manifest["documents"]:
            identifier = row.get("id")
            unit = units.get(identifier)
            if unit is None or unit.get("status") != status or identifier in selected:
                raise ValueError("active series reader lacks one matching admitted catalog entry")
            selected.add(identifier)
            expected = {"artifact_id": unit["artifact_id"], "sha256": unit["artifact_sha256"],
                        "segment_id": unit["segment_id"], "segment_path": unit["segment_path"],
                        "physical_line_ranges": unit["review"]["physical_line_ranges"],
                        "language": unit["review"]["language"], "text_path": sources[unit["artifact_id"]]["path"]}
            if any(row.get(key) != value for key, value in expected.items()):
                raise ValueError("active series reader disagrees with its admitted catalog source")
    return {"status": "ok", **catalog["coverage"]}


def parser(examples=None):
    p = argparse.ArgumentParser(prog="bullarium series", description=__doc__)
    p.formatter_class = argparse.RawDescriptionHelpFormatter
    p.epilog = HEADING + "\n  $ tools/bullarium series --help\n  $ tools/bullarium series prepare --help"
    if examples and examples.get("series"):
        with_examples(p, examples["series"])
    p.add_argument("--root", type=Path, default=ROOT)
    sub = p.add_subparsers(dest="verb", required=True)
    for verb in ("acquire", "prepare", "admit", "check", "status"):
        command = sub.add_parser(verb, epilog=HEADING + "\n  $ tools/bullarium series " + verb + " --help\n  $ tools/bullarium series --help", formatter_class=argparse.RawDescriptionHelpFormatter)
        if examples and examples.get("series-" + verb):
            with_examples(command, examples["series-" + verb])
        command.add_argument("--config", required=True, type=Path)
        command.add_argument("--json", action="store_true")
        if verb in {"acquire", "prepare"}:
            command.add_argument("--cache", type=Path, required=True)
        if verb == "acquire":
            command.add_argument("--input-map", type=Path)
        if verb in {"prepare", "admit"}:
            command.add_argument("--revision", required=True)
        if verb == "admit":
            command.add_argument("--review", type=Path, action="append", required=True)
    return p


def main(argv=None, examples=None):
    args = parser(examples).parse_args(argv)
    try:
        root = args.root.resolve()
        config = load_config(root, args.config)
        if args.verb == "acquire":
            result = acquire(root, config, local(root, args.cache, scratch=True), read_json(args.input_map) if args.input_map else None)
        elif args.verb == "prepare":
            result = prepare(root, config, local(root, args.cache, scratch=True), args.revision)
        elif args.verb == "admit":
            result = admit(root, config, args.review, args.revision)
        elif args.verb == "check":
            result = check(root, config)
        else:
            result = read_json(root / paths_for(config["series_id"])["catalog"])["coverage"]
        print(json.dumps({"v": 1, **result}, ensure_ascii=False, sort_keys=True, separators=(",", ":")) if args.json else "\n".join(f"{key}: {value}" for key, value in result.items()))
        return 0
    except (ValueError, KeyError, TypeError, OSError, ET.ParseError) as error:
        print(json.dumps({"v": 1, "status": "error", "error": str(error)}, ensure_ascii=False, sort_keys=True) if args.json else f"bullarium series: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
