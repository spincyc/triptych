"""Schema coverage for neutral editions, reusing their existing source owners.

This check reads canonical text and metadata only.  It does not acquire binary
evidence, rebuild projections, or infer source completeness from a catalogue.
Owning semantic gates that are not executed are explicitly reported as such.
"""
from __future__ import annotations

import csv
from contextlib import contextmanager
import json
from pathlib import Path
import re
import tomllib

import _print_catalog
from _bible_artifacts import select_book_index

REGISTRY = "src/common/document-schemas/source-types.toml"
BROWSER_DATA = "src/web/data"
BROWSER_DESCRIPTOR = "release/browser-products.json"


@contextmanager
def _held_browser_products(root):
    """Real product repositories never fall back to an unverified work tree."""
    module = root / "scripts/_browser_products.py"
    descriptor = root / BROWSER_DESCRIPTOR
    declared = any(path.exists() or path.is_symlink() for path in (module, descriptor))
    if not declared:
        yield None  # Sparse historical fixtures have no product contract.
        return
    _need(module.is_file() and not module.is_symlink(), "browser products require scripts/_browser_products.py")
    _need(descriptor.is_file() and not descriptor.is_symlink(),
          f"browser products require {BROWSER_DESCRIPTOR}; prepare the verified cache first")
    from _browser_products import ProductError, verified_products
    try:
        with verified_products(root) as products:
            yield products
    except ProductError as error:
        raise ValueError(f"{BROWSER_DESCRIPTOR}: {error}") from error


def _family_paths(root, patterns, products):
    """Pair stable logical identities with held bytes, never cache authority."""
    paths = {}
    for pattern in patterns:
        projected = pattern == BROWSER_DATA or pattern.startswith(BROWSER_DATA + "/")
        if projected and products is not None:
            suffix = pattern[len(BROWSER_DATA):].lstrip("/") or "."
            for path in products.data_root.glob(suffix):
                relative = path.relative_to(products.data_root).as_posix()
                logical = BROWSER_DATA + "/" + relative
                _need(relative in products.files and products.files[relative] == path
                      and path.is_file() and not path.is_symlink(),
                      f"{logical}: file is not in the verified browser product snapshot")
                paths[logical] = path
        else:
            for path in root.glob(pattern):
                paths[path.relative_to(root).as_posix()] = path
    return sorted(paths.items())


def _stable_error(error, root, products=None):
    message = str(error)
    if products is not None:
        message = message.replace(str(products.data_root), BROWSER_DATA)
    return message.replace(str(root) + "/", "")


def _need(condition, message):
    if not condition:
        raise ValueError(message)


def _read(path):
    if path.suffix == ".toml":
        return tomllib.loads(path.read_text(encoding="utf-8"))
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _source_projection(root, logical, data, products):
    """Validate every discovery shard through the held product membership."""
    counted = data.get("counted")
    _need(isinstance(counted, dict) and all(type(value) is int and value >= 0
          for value in counted.values()), f"{logical}: invalid projection counts")
    if data.get("schema") == "triptych-source-reader/v1":
        _need(isinstance(data.get("works"), list) and len(data["works"]) == counted.get("works"),
              f"{logical}: projection identity/counts disagree")
        return
    _need(data.get("schema") == "triptych-source-discovery/v3" and isinstance(data.get("shards"), list),
          f"{logical}: invalid source discovery manifest")
    _need(data.get("root") == "structure/sources/" and data.get("texts") == "structure/sources/text/",
          f"{logical}: invalid source discovery roots")
    totals = dict(works=0, editions=0, passages=0, readable=0)
    identities = set()
    expected = set()
    for number, shard in enumerate(data["shards"]):
        relative = f"structure/sources/catalogue/{number:04d}.json"
        message = f"{BROWSER_DATA}/{relative}: invalid source discovery shard"
        _need(isinstance(shard, dict) and shard.get("path") == relative and
              type(shard.get("works")) is int and 0 < shard["works"] <= 128, message)
        expected.add(relative)
        matches = _family_paths(root, [BROWSER_DATA + "/" + relative], products)
        _need(len(matches) == 1, message + " is missing from verified membership")
        path = matches[0][1]
        _need(path.is_file() and not path.is_symlink(), message + " is not a regular file")
        payload = _read(path)
        _need(isinstance(payload, dict) and payload.get("schema") == "triptych-source-catalogue/v2" and
              isinstance(payload.get("labels"), list) and all(isinstance(label, str) for label in payload["labels"]) and
              isinstance(payload.get("rows"), list) and len(payload["rows"]) == shard["works"], message)
        labels = payload["labels"]
        def label(value, optional=True):
            return (optional and value is None) or (type(value) is int and 0 <= value < len(labels))
        def identity(value):
            _need(isinstance(value, str) and value and value not in identities, message + " has duplicate/missing identity")
            identities.add(value)
        for row in payload["rows"]:
            _need(isinstance(row, list) and len(row) == 7, message + " has malformed work")
            identity(row[0])
            _need((row[1] is None or isinstance(row[1], str)) and label(row[2]) and label(row[3]) and
                  isinstance(row[4], list) and all(isinstance(alias, str) for alias in row[4]) and
                  isinstance(row[6], list), message + " has invalid work metadata")
            _need(row[5] is None and not row[6] or isinstance(row[5], str) and
                  re.fullmatch(r"editions/[a-z0-9._-]+/[a-z0-9._-]+/", row[5]) is not None,
                  message + " has invalid work route")
            totals["works"] += 1
            for edition in row[6]:
                _need(isinstance(edition, list) and len(edition) == 9, message + " has malformed edition")
                identity(edition[0])
                _need((edition[1] is None or isinstance(edition[1], str) or type(edition[1]) is int and edition[1] == 0) and
                      label(edition[2]) and label(edition[3]) and
                      (edition[4] is None or type(edition[4]) is int) and label(edition[5], False) and
                      re.fullmatch(r"[a-z0-9._-]+\.json", labels[edition[5]]) is not None and
                      type(edition[6]) is int and type(edition[7]) is int and 0 <= edition[7] <= edition[6] and
                      isinstance(edition[8], list) and all(label(right, False) for right in edition[8]),
                      message + " has invalid edition metadata")
                totals["editions"] += 1
                totals["passages"] += edition[6]
                totals["readable"] += edition[7]
    prefix = "structure/sources/catalogue/"
    if products is not None:
        actual = {name for name in products.files if name.startswith(prefix)}
    else:
        actual = {path.relative_to(Path(root) / BROWSER_DATA).as_posix()
                  for path in (Path(root) / BROWSER_DATA / prefix).glob("*.json")}
    _need(actual == expected, f"{logical}: source discovery shard membership differs")
    _need(all(counted.get(key) == value for key, value in totals.items()),
          f"{logical}: projection identity/counts disagree")


def source_types(root):
    data = _read(Path(root) / REGISTRY)
    _need(data.get("schema_version") == 1 and data.get("record_type") == "source-document-family-registry",
          "invalid neutral source-family registry")
    families = data.get("families", [])
    seen = set()
    for family in families:
        identifier = family.get("id")
        _need(isinstance(identifier, str) and identifier and identifier not in seen,
              "duplicate or missing source-family id")
        seen.add(identifier)
        for field in ("schema_ids", "paths", "required_fields", "validator"):
            _need(isinstance(family.get(field), list) and family[field]
                  and all(isinstance(value, str) and value for value in family[field]),
                  f"{identifier}: invalid {field}")
        _need(type(family.get("minimum_members")) is int and family["minimum_members"] >= 0,
              f"{identifier}: invalid cardinality")
        _need((Path(root) / family["owner"]).is_file(), f"{identifier}: missing existing schema owner")
    return families


def check_book_index(path, row_schema):
    """Apply the declared existing TSV-row vocabulary and collection uniqueness.

    The JSON Schema uses only object/string/required/enum/pattern/minLength;
    reading these declarations directly avoids a new runtime dependency.
    """
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        header = reader.fieldnames or []
        _need(len(header) == len(set(header)), f"{path}: duplicate book-index column")
        _need(set(row_schema["required"]) <= set(header), f"{path}: missing required book-index column")
        _need(set(header) <= set(row_schema["properties"]), f"{path}: unknown book-index column")
        rows = list(reader)
    _need(rows, f"{path}: empty book index")
    unique = {field: set() for field in ("ordinal", "token", "file", "modern_name")}
    previous = 0
    for number, row in enumerate(rows, 2):
        _need(set(row) == set(header), f"{path}:{number}: malformed TSV row")
        for field, value in row.items():
            definition = row_schema["properties"][field]
            _need(isinstance(value, str), f"{path}:{number}: {field} must be a string")
            _need(len(value) >= definition.get("minLength", 0), f"{path}:{number}: empty {field}")
            if "pattern" in definition:
                _need(re.fullmatch(definition["pattern"], value) is not None,
                      f"{path}:{number}: invalid {field}")
            if "enum" in definition:
                _need(value in definition["enum"], f"{path}:{number}: invalid {field}")
        ordinal = int(row["ordinal"])
        _need(ordinal > previous, f"{path}:{number}: book ordinals must increase")
        previous = ordinal
        for field, seen in unique.items():
            _need(row[field] not in seen, f"{path}:{number}: duplicate {field}")
            seen.add(row[field])
    return rows


def check_verse_addresses(book):
    """Validate printed addresses without inventing verses in historical gaps."""
    previous = None
    seen = set()
    for chapter, verse, text in book.verses:
        address = chapter, verse
        _need(type(chapter) is int and type(verse) is int and chapter >= 1 and verse >= 0
              and isinstance(text, str) and text.strip(), f"{book.token}: invalid verse row")
        _need(address not in seen and (previous is None or previous < address),
              f"{book.token}: duplicate or unordered printed verse address {chapter}:{verse}")
        seen.add(address)
        previous = address
    _need(seen, f"{book.token}: no printed verse text")


def _bibles(root, family):
    module = _print_catalog._bible_typesetter()
    schema = _read(root / family["row_schema"])
    records, counts = _print_catalog._Records(root), []
    for name in module.publishable(module.registry()):
        registered = module.entry(module.registry(), name)
        _need(all(field in registered for field in family["required_fields"]),
              f"{name}: incomplete canonical edition registry")
        edition = module.Edition(name, registered, root / "src/sources/works")
        check_book_index(select_book_index(edition.artifacts.parent), schema)
        _print_catalog._bible_sources(root, module, edition, records)
        edition.load()
        for book in edition.books:
            check_verse_addresses(book)
        counts.append({"id": name, "books": len(edition.books),
                       "verses": sum(len(book.verses) for book in edition.books)})
    return counts


def _plans(root):
    module = _print_catalog._bible_typesetter()
    checker = module.sibling("reading-plan")
    # The canonical tool owns the numbered witness and its exact bounds.
    tokens, bounds = checker.verse_text()
    plans = module.plans(root / "src/sources/reading-plans")
    volumes, rows = [], []
    for plan in plans:
        problems = checker.check_plan(plan.path, plan.document, tokens, bounds)
        _need(not problems, "; ".join(problems[:8]))
        rows.append({"id": plan.id, "readings": len(plan.readings)})
        volumes.extend({"id": module.volume_id(plan, tier, bible), "plan": plan.id,
                        "tier": tier, "bible": bible} for tier, bible in module.volumes(plan))
    return rows, volumes


def _papal_manifests(root):
    papal = _print_catalog.papal
    rows, selections, retained = 0, 0, {}
    def metadata(path):
        if path not in retained:
            retained[path] = _read(path)
        return retained[path]
    fields = ("id", "title", "pope", "language", "source_url", "text_path", "sha256",
              "artifact_id", "rights_status", "rights_basis")
    directory = root / "src/sources/papal-documents"
    paths = set(directory.glob("*manifest.json")) | set(directory.glob("*withdrawals.json"))
    for path in sorted(paths):
        data = _read(path)
        _need(isinstance(data, dict) and data.get("schema") == papal.SCHEMA,
              f"{path}: unknown papal selection schema")
        rows += 1
        papal._validate_revision(data.get("revision"))
        _need(isinstance(data.get("documents"), list), f"{path}: documents must be an array")
        _print_catalog._indexed(data["documents"], "papal manifest")
        for source in data["documents"]:
            selections += 1
            _need(all(isinstance(source.get(field), str) and source[field].strip() for field in fields),
                  f"{path}: incomplete source-selection record")
            _need(source["language"] in papal.LANGUAGES and re.fullmatch(r"[a-f0-9]{64}", source["sha256"]),
                  f"{path}: invalid source language/hash")
            text = _print_catalog._path(root, source["text_path"])
            _need(text.is_file(), f"{path}: missing canonical selection text")
            artifact = metadata(text.with_name("artifact.toml"))
            _need(artifact.get("id") == source["artifact_id"] and artifact.get("sha256") == source["sha256"]
                  and artifact.get("storage") == "tracked" and artifact.get("rights_status") == source["rights_status"]
                  and source["rights_status"] in papal.ADMITTED_RIGHTS,
                  f"{path}: source controller or rights provenance disagrees")
            bounds = source.get("physical_line_ranges")
            if source.get("segment_id"):
                segment = metadata(_print_catalog._path(root, source.get("segment_path")))
                _need(segment.get("id") == source["segment_id"]
                      and segment.get("artifact_id") == source["artifact_id"]
                      and segment.get("artifact_sha256") == source["sha256"]
                      and segment.get("physical_line_ranges") == bounds,
                      f"{path}: bounded source provenance disagrees")
                last = 0
                for pair in bounds or []:
                    _need(isinstance(pair, list) and len(pair) == 2 and all(type(n) is int for n in pair)
                          and last < pair[0] <= pair[1], f"{path}: invalid source bounds")
                    last = pair[1]
                _need(last, f"{path}: bounded source has no ranges")
            else:
                _need(not bounds and not source.get("segment_path"), f"{path}: unregistered bounded source")
    return rows, selections


def _check_source_editions(root, products=None):
    root = Path(root).resolve()
    report = {"id": "source-editions", "phase": "source", "ok": False, "status": "fail",
              "families": [], "errors": [], "external_gates": [], "warnings": [
        "Source structure and typed cardinalities do not establish full-source completeness, source-image collation, or semantic acceptance. Owning gates marked not-run remain separate obligations."]}
    try:
        families = source_types(root)
        by_id = {family["id"]: family for family in families}
        bibles = _bibles(root, by_id["bible-edition"])
        plans, volumes = _plans(root)
        manifests, selections = _papal_manifests(root)
        readers = _print_catalog._papal_pages(root, **({
            "data_root": products.data_root,
            "data_source_paths": sorted(products.source_paths),
        } if products is not None else {}))
        special = {"bible-edition": bibles, "reading-plan": plans, "reading-plan-volume": volumes,
                   "papal-selection": [{"manifests": manifests, "selections": selections}],
                   "papal-reader": [{"route": route} for route in readers]}
        for family in families:
            identifier = family["id"]
            paths = _family_paths(root, family["paths"], products)
            members = manifests if identifier == "papal-selection" else (
                len(special[identifier]) if identifier in special else len(paths))
            _need(members >= family["minimum_members"],
                  f"{identifier}: fewer members than declared minimum ({', '.join(family['paths'])})")
            if identifier not in special and identifier != "source-record":
                for logical, path in paths:
                    try:
                        data = _read(path)
                    except (ValueError, OSError, UnicodeError) as error:
                        raise ValueError(f"{logical}: {error}") from error
                    _need(isinstance(data, dict) and all(field in data for field in family["required_fields"]),
                          f"{logical}: required canonical schema fields missing")
                    schema = "acts_schema/" + str(data["acts_schema"]) if "acts_schema" in data else data.get("schema")
                    _need(schema in family["schema_ids"], f"{logical}: unexpected canonical schema {schema}")
                    if identifier == "source-reader-projection":
                        _source_projection(root, logical, data, products)
            semantic = identifier in special
            report["families"].append({"id": identifier, "schema_ids": family["schema_ids"],
                "members": members, "status": "pass", "semantic_checks": "performed" if semantic else "owning-gate",
                **({"records": special[identifier]} if semantic else {})})
            if not semantic:
                report["external_gates"].append({"id": identifier, "command": family["validator"], "status": "not-run"})
    except (ValueError, OSError, KeyError, TypeError) as error:
        report["errors"].append(str(error))
    report["ok"] = not report["errors"]
    report["status"] = "pass" if report["ok"] else "fail"
    return report


def check_source_editions(root):
    """Keep verified browser products held for the entire neutral source audit."""
    root = Path(root).resolve()
    products = None
    report = {"id": "source-editions", "phase": "source", "ok": False, "status": "fail",
              "families": [], "errors": [], "external_gates": [], "warnings": []}
    try:
        with _held_browser_products(root) as products:
            report = _check_source_editions(root, products)
            if products is not None:
                report["browser_products_identity"] = products.products_identity
    except (ValueError, OSError, KeyError, TypeError) as error:
        report["errors"].append(_stable_error(error, root, products))
    report["errors"] = [_stable_error(error, root, products) for error in report["errors"]]
    report["ok"] = not report["errors"]
    report["status"] = "pass" if report["ok"] else "fail"
    return report
