"""Lossless native TeX source transport for admitted, on-demand print editions.

These bundles prepare the inputs of the existing native recipes, not another
document representation.  No TeX engine is invoked here.  The browser mounts
the original paths and compiles with the original working-directory semantics.
The separately delivered runtime owns the engine, packages, formats and fonts.
"""
from __future__ import annotations

import base64
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-native-print-source-bundle/v1"
CATALOG_SCHEMA = "triptych-native-print-source-catalog/v1"
SOURCE_ROUTE = "native-tex/sources"
_RENDER_SUFFIXES = {".tex", ".sty", ".cls", ".bib", ".bst", ".png", ".jpg", ".jpeg", ".eps"}
_TEXT_SUFFIXES = {".tex", ".sty", ".cls", ".bib", ".bst"}
_DICTIONARY = "liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary"
_REVISION = re.compile(r"[0-9a-f]{40}\Z")
_SOURCE_PACK_FILES = 32
_SOURCE_PACK_BYTES = 8 * 1024 * 1024
_RENDER_FIELDS = ("document", "output_id", "edition", "engine", "format", "entrypoint", "cwd", "environment", "options")


class BundleError(ValueError):
    pass


def _need(condition, message):
    if not condition:
        raise BundleError(message)


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _relative(value: str) -> str:
    _need(isinstance(value, str) and value and "\\" not in value and "\0" not in value
          and not value.startswith("/") and all(part not in {"", ".", "..", ".git", ".scratch", "__pycache__"}
                                                for part in value.split("/"))
          and not any(ord(char) < 32 for char in value), "unsafe native source path")
    _need(PurePosixPath(value).as_posix() == value, "noncanonical native source path")
    return value


def _source(root: Path, value: str) -> Path:
    value = _relative(value)
    current = root
    for part in value.split("/"):
        current = current / part
        _need(not current.is_symlink(), "native source path contains a symlink: " + value)
    _need(current.resolve().is_relative_to(root) and current.is_file(),
          "missing native source file: " + value)
    return current


def _fingerprints(root: Path, paths, cache: dict | None = None) -> list[dict]:
    result = []
    for value in sorted(set(paths)):
        path = _source(root, value)
        before = path.stat()
        signature = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
        held = cache.get(value) if cache is not None else None
        if held is not None and held[0] == signature:
            row = held[1]
        else:
            payload = path.read_bytes()
            after = path.stat()
            _need(signature == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns),
                  "canonical source changed while preparing native print: " + value)
            row = {"path": value, "bytes": len(payload), "sha256": _sha(payload)}
            if cache is not None:
                cache[value] = signature, row
        result.append(dict(row))
    return result


def _file(value: str, payload: bytes) -> dict:
    value = _relative(value)
    try:
        content, encoding = payload.decode("utf-8"), "utf8"
    except UnicodeDecodeError:
        content, encoding = base64.b64encode(payload).decode("ascii"), "base64"
    return {"path": value, "encoding": encoding, "content": content,
            "bytes": len(payload), "sha256": _sha(payload)}


def file_bytes(row: dict) -> bytes:
    """Strict decoding is also useful to independent transport/verifier callers."""
    _need(isinstance(row, dict) and set(row) == {"path", "encoding", "content", "bytes", "sha256"},
          "invalid native source file record")
    _relative(row["path"])
    _need(isinstance(row["content"], str) and type(row["bytes"]) is int and row["bytes"] >= 0,
          "invalid native source file content")
    try:
        if row["encoding"] == "utf8":
            payload = row["content"].encode("utf-8")
        elif row["encoding"] == "base64":
            payload = base64.b64decode(row["content"], validate=True)
            _need(base64.b64encode(payload).decode("ascii") == row["content"], "noncanonical source base64")
        else:
            raise BundleError("unsupported native source file encoding")
    except (UnicodeError, ValueError) as error:
        raise BundleError("invalid native source file encoding") from error
    _need(len(payload) == row["bytes"] and _sha(payload) == row["sha256"],
          "native source file size or hash mismatch")
    return payload


def render_identity(bundle: dict) -> str:
    """Bind the exact mounted project and invocation, independently of transport."""
    value = {key: bundle[key] for key in _RENDER_FIELDS}
    value["files"] = [{key: row[key] for key in ("path", "bytes", "sha256")}
                      for row in sorted(bundle["files"], key=lambda row: row["path"])]
    return _sha(canonical(value))


def _externalize(bundle: dict, assets: dict[str, bytes], *, shared_text=()) -> dict:
    """Share exact artwork and repeated text; keep their canonical virtual paths."""
    files = []
    groups = defaultdict(list)
    for row in bundle["files"]:
        shared = (row["encoding"] == "utf8" and row["sha256"] in shared_text and row["bytes"] > 0
                  and PurePosixPath(row["path"]).suffix.lower() in _TEXT_SUFFIXES)
        if row["encoding"] != "base64" and not shared:
            files.append(row)
            continue
        payload = file_bytes(row)
        suffix = PurePosixPath(row["path"]).suffix.lower()
        _need(suffix in _RENDER_SUFFIXES, "unsupported external native artwork format")
        name = row["sha256"] + (".bin" if shared else suffix)
        route = "native-tex/assets/" + name
        if route in assets:
            _need(assets[route] == payload, "conflicting native artwork content identity")
        else:
            assets[route] = payload
        files.append({"path": row["path"], "encoding": "url", "href": "../assets/" + name,
                      "bytes": row["bytes"], "sha256": row["sha256"]})
        if shared:
            groups[str(PurePosixPath(row["path"]).parent)].append((row, payload))
    result = {key: value for key, value in bundle.items() if key != "content_sha256"}
    result["files"] = files
    packs, packed = [], set()
    for directory in sorted(groups):
        rows = sorted(groups[directory], key=lambda pair: pair[0]["path"])
        # Fixed canonical-path groups avoid reshuffling later packs when a
        # stylesheet changes length or content hash. Oversize groups use URLs.
        for start in range(0, len(rows), _SOURCE_PACK_FILES):
            members, chunks, offset = [], [], 0
            selected = set()
            for row, payload in rows[start:start + _SOURCE_PACK_FILES]:
                if row["sha256"] in packed or row["sha256"] in selected:
                    continue
                selected.add(row["sha256"])
                members.append({"sha256": row["sha256"], "bytes": len(payload), "offset": offset})
                chunks.append(payload)
                offset += len(payload)
            if not members or offset > _SOURCE_PACK_BYTES:
                continue
            compressed = bytearray(gzip.compress(b"".join(chunks), compresslevel=9, mtime=0))
            compressed[9] = 255  # Portable gzip OS marker, independent of the host.
            payload = bytes(compressed)
            if len(payload) >= offset:
                continue
            digest = _sha(payload)
            route = "native-tex/source-packs/" + digest + ".bin"
            _need(route not in assets or assets[route] == payload, "conflicting native source pack")
            assets[route] = payload
            packs.append({"href": "../source-packs/" + digest + ".bin", "sha256": digest,
                          "bytes": len(payload), "compression": "gzip", "expanded_bytes": offset,
                          "files": members})
            packed.update(selected)
    if packs:
        result["sourcePacks"] = packs
    result["content_sha256"] = _sha(canonical(result))
    validate_bundle(result)
    return result


def _scratch(root: Path, configured: Path | None) -> Path:
    from _print_document import _destination
    path = root / ".scratch/native-print-bundles" if configured is None else Path(configured)
    _need(path.is_absolute(), "native bundle scratch must be absolute")
    _need(not any(part.is_symlink() for part in (path, *path.parents)), "native bundle scratch contains a symlink")
    path = _destination(path, root)
    path.mkdir(parents=True, exist_ok=True)
    return path


def _run(argv: list[str], root: Path):
    from _print_document import _environment
    try:
        run = subprocess.run(argv, cwd=root, env=_environment(), capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise BundleError("native source preparation failed") from error
    _need(run.returncode == 0, "native source preparation failed: " + (run.stderr or run.stdout)[-2000:])
    return run.stdout


def _dictionary_files(root: Path, recipe: dict, work: Path) -> dict[str, bytes]:
    """Run the same typed TeX producer used by Make, without a PDF prerequisite."""
    base = f"src/{recipe['provider']}/{_DICTIONARY}"
    source = root / base
    target = work / "dictionary"
    _run([sys.executable, str(root / "tools/render-sanctuary-dictionary"),
          "--schema", str(source / "shared/schema/inventory-schema.toml"),
          "--selections", str(source / "shared/schema/edition-selections.toml"),
          "--artwork-manifest", str(source / "research/artwork-manifest.toml"),
          "--records", str(source / "shared/objects"), "--output", str(target)], root)
    prefix = f"build/{recipe['provider']}/{_DICTIONARY}/shared/generated"
    return {f"{prefix}/{path.name}": path.read_bytes() for path in sorted(target.glob("*.tex"))}


def _binary_selection(root: Path, recipe: dict, kind: str, dependencies: set[str]):
    """Positive selected artwork only; a Make shared-directory glob is not admission."""
    if kind == "pictorial-dictionary":
        from _web_print_dictionaries import render_dictionary
        product = render_dictionary(root, recipe["provider"], recipe["id"])
        selected = set()
        for row in product["assets"]:
            path = _source(root, row["source"])
            _need(_sha(path.read_bytes()) == row["sha256"], "selected dictionary artwork identity changed")
            selected.add(row["source"])
        dependencies.update(product["source_paths"])
        dependencies.update(value for value in ("scripts/_web_print_dictionaries.py",
                            "scripts/_web_print_dictionary_context.py", "scripts/_web_print_common.py")
                            if (root / value).is_file())
        return selected
    if kind.startswith("server-"):
        from _web_print_server import expected_card_print_selection, expected_guide_print_selection
        import _web_print_server_diagrams as diagrams
        name = recipe["canonical"].rsplit("/", 1)[-1]
        cards = name.endswith(("flash-cards", "cue-cards"))
        expectation = (expected_card_print_selection if cards else expected_guide_print_selection)(
            root, recipe["provider"], recipe["document"])
        dependencies.update(expectation["source_selection"]["source_inputs"])
        dependencies.update(value for value in ("scripts/_web_print_server.py",
                            "scripts/_web_print_server_diagrams.py", "scripts/document_schema_checks/liturgy.py",
                            "tools/web-edition") if (root / value).is_file())
        if cards:
            return set()
        variant = "trainer" if "trainer-manual" in name else "child" if name.startswith("01-") else "sung"
        inventory = diagrams.inventory(root)
        pattern = re.compile(re.escape(diagrams.TEX_OWNER) + r"/shared/artwork/pencil/[A-Za-z0-9._-]+\.png")
        selected = set()
        for unit in expectation["print_unit_expectations"]:
            if unit["kind"] != "diagram":
                continue
            macro = unit["source_refs"][0]["macro"]
            entry = inventory["entries"].get(variant + ":" + macro)
            _need(entry is not None, "selected native server diagram has no canonical definition")
            for definition in entry["definition_closure"].values():
                selected.update("src/" + recipe["provider"] + "/" + value
                                for value in pattern.findall(definition["definition_tex"]))
        return selected
    # The other current illustrated owner is the Ark study: five project plate
    # calls and one PGF raster. Read bounded actual graphics arguments, never
    # filename mentions in comments/bibliography or arbitrary sibling files.
    from _corpus import active_tex
    candidates = {value for value in dependencies if PurePosixPath(value).suffix.lower()
                  in _RENDER_SUFFIXES - _TEXT_SUFFIXES}
    if not candidates:
        return set()
    prefix = f"src/{recipe['provider']}/"
    selected = set()
    calls = re.compile(r"\\(includegraphics|pgfimage|arkgraphiteplate)\s*(?:\[[^\]]*\]\s*)?\{([^{}]*)\}")
    for value in sorted(dependencies):
        if PurePosixPath(value).suffix.lower() not in _TEXT_SUFFIXES:
            continue
        text = active_tex(_source(root, value).read_text(encoding="utf-8"))
        for command, argument in calls.findall(text):
            argument = argument.strip()
            if "\\" in argument or "#" in argument:
                # This is the one current native plate wrapper, whose literal
                # invocations below carry the selected image path. An unknown
                # computed image needs its own owner instead of a broad copy.
                _need(recipe["canonical"] == "theology/mariology/ark-of-the-covenant"
                      and command == "includegraphics" and argument == "#1"
                      and value.endswith("/sections/57-ark-and-sanctuaries.tex"),
                      "computed native artwork requires its owning selection adapter")
                continue
            resolved = posixpath.normpath(prefix + argument)
            matches = {path for path in candidates if path == resolved or
                       not PurePosixPath(argument).suffix and path.rsplit(".", 1)[0] == resolved}
            _need(matches, "literal native artwork has no declared source: " + argument)
            selected.update(matches)
    return selected


def _publication_inputs(root: Path, recipe: dict):
    from _document_schema import _literal_closure, load_manifest
    dependencies = set(recipe["dependencies"])
    manifest_path = root / f"src/{recipe['provider']}/{recipe['canonical']}/publication.toml"
    _need(manifest_path.is_file(), "native source bundle requires a declared publication manifest")
    declaration = load_manifest(root, manifest_path)
    # The literal graph is an independent supplement to Make's conservative
    # owned/shared input sets. Computed inputs retain their original definitions;
    # their selected typed-family closure is provided by the owning Make graph.
    literal, computed = _literal_closure(root, declaration)
    dependencies.add(manifest_path.relative_to(root).as_posix())
    dependencies.update(path.relative_to(root).as_posix() for path in literal)
    if declaration["kind"] == "pictorial-dictionary":
        dependencies.add("tools/render-sanctuary-dictionary")
        base = f"src/{recipe['provider']}/{_DICTIONARY}"
        dependencies.add(base + "/research/artwork-manifest.toml")
        dependencies.update(path.relative_to(root).as_posix()
                            for path in (root / base / "shared").rglob("*.toml"))
    allowed_binary = _binary_selection(root, recipe, declaration["kind"], dependencies)
    dependencies.update(allowed_binary)
    return dependencies, computed, declaration["kind"], allowed_binary


def _publication_files(root: Path, recipe: dict, work: Path, dependencies, kind, allowed_binary):
    files = {}
    for value in sorted(dependencies):
        path = _source(root, value)
        if path.suffix.lower() in _RENDER_SUFFIXES:
            _need(value.startswith((f"src/{recipe['provider']}/", "src/common/")),
                  "native publication render input has no provider/shared owner: " + value)
            if path.suffix.lower() in _TEXT_SUFFIXES or value in allowed_binary:
                files[value] = path.read_bytes()
    if kind == "pictorial-dictionary":
        files.update(_dictionary_files(root, recipe, work))
    entrypoint = recipe["entrypoint"]
    _need(entrypoint in files, "native source bundle is missing its selected entrypoint")
    return files, entrypoint, f"src/{recipe['provider']}"


def _generated_files(root: Path, recipe: dict, work: Path):
    family = recipe["family"]
    if family == "papal":
        import _typeset_papal as papal
        row = papal.validate_document(recipe["_source_row"], root)
        manifest = {"schema": papal.SCHEMA, "revision": recipe["_revision"], "documents": [recipe["_source_row"]]}
        result = papal.render_documents(manifest, [row], work / "papal", compile_pdf=False, jobs=1)
        _need(not result["errors"] and len(result["documents"]) == 1, "papal native source producer failed")
        generated = result["documents"][0]
        source = work / "papal" / generated["tex"]
        prefix = "native/papal/" + source.parent.name
        files = {prefix + "/" + path.name: path.read_bytes()
                 for path in sorted(source.parent.glob("*.tex"))}
        return files, prefix + "/" + source.name, prefix
    from _print_document import _json_tool
    flag = "--bible" if family == "bible" else "--volume"
    result = _json_tool(root, "typeset-bible", "render", flag, recipe["document"], "--out", str(work / family))
    _need(len(result.get("rendered", [])) == 1, "native source producer did not select exactly one edition")
    source = Path(result["rendered"][0]["path"])
    _need(source.resolve().is_relative_to(work.resolve()) and source.suffix == ".tex" and not source.is_symlink(),
          "native source producer returned an unsafe output")
    prefix = "native/" + family + "/" + recipe["document"]
    return {prefix + "/" + source.name: source.read_bytes()}, prefix + "/" + source.name, prefix


def prepare_bundle(output_id: str, *, root: Path = ROOT, scratch_root: Path | None = None,
                   documents: dict | None = None, revision: str | None = None,
                   recipe: dict | None = None, fingerprint_cache: dict | None = None,
                   external_assets: dict[str, bytes] | None = None, _checked: bool = False) -> dict:
    """Prepare one publicly admitted native output; never invoke a TeX engine.

    Explicit documents/recipe/revision permit a publisher to hold one verified
    source snapshot over a batch. They are trusted Python inputs, not HTTP or
    browser parameters. Output identity and selection are still cross-checked.
    """
    from _native_print import admitted_documents, source_revision
    import _print_document as printing
    root = Path(root).resolve()
    documents = admitted_documents(root) if documents is None else documents
    _need(output_id in documents, "native print output is not publicly admitted: " + str(output_id))
    selected = documents[output_id]
    revision = source_revision(root) if revision is None else revision
    _need(isinstance(revision, str) and _REVISION.fullmatch(revision), "invalid native source revision")
    recipe = (printing.select(selected["document"], selected["edition"], root=root)
              if recipe is None else dict(recipe))
    _need(recipe.get("id") == output_id and recipe.get("edition", "main") == selected["edition"],
          "native recipe does not match the admitted output")
    if _checked:
        _need(recipe.get("status") == "valid" and isinstance(recipe.get("validation"), dict),
              "native source batch recipe has not passed its owning checks")
    else:
        recipe = printing.check(recipe, root=root)
    dependencies = set(recipe["dependencies"])
    dependencies.update(value for value in ("Makefile", "scripts/_native_print_bundles.py", "scripts/_print_document.py")
                        if (root / value).is_file())
    guarded_inputs = _fingerprints(root, dependencies, fingerprint_cache)
    computed, kind, allowed_binary = [], None, set()
    if recipe["family"] == "publication":
        additions, computed, kind, allowed_binary = _publication_inputs(root, recipe)
        dependencies.update(additions)
    else:
        software = ("tools/typeset-bible",) if recipe["family"] in {"bible", "reading-plan"} else (
            "scripts/_typeset_papal.py", "scripts/_papal_collection.py")
        dependencies.update(value for value in software if (root / value).is_file())
    inputs = _fingerprints(root, dependencies, fingerprint_cache)
    scratch = _scratch(root, scratch_root)
    with tempfile.TemporaryDirectory(prefix="source-", dir=scratch) as temporary:
        work = Path(temporary)
        if recipe["family"] == "publication":
            files, entrypoint, cwd = _publication_files(root, recipe, work, dependencies, kind, allowed_binary)
        else:
            files, entrypoint, cwd = _generated_files(root, recipe, work)
        # A dependency snapshot precedes publication of the transport and is
        # re-read after assembly. Missing or concurrently changed sources fail.
        records = [_file(value, payload) for value, payload in sorted(files.items())]
        _need(len({row["path"].casefold() for row in records}) == len(records), "case-colliding native source paths")
        engine = "xetex" if recipe["family"] == "papal" else "pdftex"
        bundle = {"schema": SCHEMA, "document": selected["document"], "output_id": output_id,
                  "edition": selected["edition"], "title": selected["title"], "source_revision": revision,
                  "engine": engine, "format": "xelatex" if engine == "xetex" else "pdflatex",
                  "entrypoint": entrypoint, "cwd": cwd,
                  "environment": {"TEXINPUTS": "..:"} if recipe["family"] == "publication" else {},
                  "options": {"shell_escape": False, "minimum_passes": 2, "max_passes": 8,
                              "settle_auxiliary_files": True},
                  "input_contract": "native-make-declared-and-literal-closure/v1" if recipe["family"] == "publication"
                                    else "owning-native-source-producer/v1",
                  "computed_source_inputs": computed, "files": records, "source_inputs": inputs,
                  "runtime_requirement": "matching-versioned-engine-format-packages-and-original-fonts",
                  "review_status": "source-prepared-not-render-reviewed"}
        _need(inputs == _fingerprints(root, dependencies, fingerprint_cache), "canonical native print inputs changed during preparation")
        _need(guarded_inputs == _fingerprints(root, (row["path"] for row in guarded_inputs), fingerprint_cache),
              "canonical native print inputs changed during selection")
    bundle["render_sha256"] = render_identity(bundle)
    bundle["content_sha256"] = _sha(canonical(bundle))
    validate_bundle(bundle)
    return _externalize(bundle, external_assets) if external_assets is not None else bundle


def validate_bundle(bundle: dict) -> dict:
    _need(isinstance(bundle, dict) and bundle.get("schema") == SCHEMA, "invalid native source bundle")
    expected = bundle.get("content_sha256")
    _need(isinstance(expected, str) and expected == _sha(canonical({key: value for key, value in bundle.items()
                                                                  if key != "content_sha256"})),
          "native source bundle identity mismatch")
    _need(_REVISION.fullmatch(bundle.get("source_revision", "")) and bundle.get("engine") in {"pdftex", "xetex"},
          "invalid native source engine or revision")
    _need(bundle.get("format") == {"pdftex": "pdflatex", "xetex": "xelatex"}[bundle["engine"]],
          "native source engine/format mismatch")
    _relative(bundle["cwd"])
    _relative(bundle["entrypoint"])
    records = bundle.get("files")
    _need(isinstance(records, list) and records, "native source bundle is empty")
    paths = []
    for row in records:
        if row.get("encoding") == "url":
            _need(set(row) == {"path", "encoding", "href", "bytes", "sha256"}
                  and type(row["bytes"]) is int and row["bytes"] > 0
                  and isinstance(row["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]),
                  "invalid native artwork delivery record")
            _relative(row["path"])
            suffix = PurePosixPath(row["path"]).suffix.lower()
            suffixes = {suffix, ".bin"} if suffix in _TEXT_SUFFIXES else {suffix}
            _need(suffix in _RENDER_SUFFIXES
                  and row["href"] in {"../assets/" + row["sha256"] + ending for ending in suffixes},
                  "native artwork delivery must use its exact content-addressed route")
        else:
            file_bytes(row)
        paths.append(row["path"])
    _need(paths == sorted(paths) and len({value.casefold() for value in paths}) == len(paths)
          and bundle["entrypoint"] in paths, "invalid native source file order or entrypoint")
    _need(bundle.get("options") == {"shell_escape": False, "minimum_passes": 2, "max_passes": 8,
                                    "settle_auxiliary_files": True}, "unsupported native compilation options")
    if "render_sha256" in bundle:
        _need(bundle["render_sha256"] == render_identity(bundle), "native source render identity mismatch")
    if "sourcePacks" in bundle:
        packs = bundle["sourcePacks"]
        expected = {row["sha256"]: row["bytes"] for row in records
                    if row["encoding"] == "url" and PurePosixPath(row["path"]).suffix.lower() in _TEXT_SUFFIXES}
        _need(isinstance(packs, list) and len(packs) <= len(expected), "invalid native source packs")
        packed = set()
        for pack in packs:
            _need(isinstance(pack, dict) and set(pack) == {"href", "sha256", "bytes", "compression", "expanded_bytes", "files"}
                  and isinstance(pack["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", pack["sha256"])
                  and pack["href"] == "../source-packs/" + pack["sha256"] + ".bin"
                  and type(pack["bytes"]) is int and pack["bytes"] > 0
                  and pack["compression"] == "gzip" and type(pack["expanded_bytes"]) is int
                  and 0 < pack["expanded_bytes"] <= _SOURCE_PACK_BYTES
                  and isinstance(pack["files"], list) and 0 < len(pack["files"]) <= _SOURCE_PACK_FILES,
                  "invalid native source pack")
            offset = 0
            for member in pack["files"]:
                _need(isinstance(member, dict) and set(member) == {"sha256", "bytes", "offset"}
                      and isinstance(member["sha256"], str) and member["sha256"] in expected
                      and member["sha256"] not in packed and type(member["bytes"]) is int
                      and member["bytes"] == expected[member["sha256"]]
                      and type(member["offset"]) is int and member["offset"] == offset,
                      "invalid native source pack inventory")
                packed.add(member["sha256"])
                offset += member["bytes"]
            _need(offset == pack["expanded_bytes"], "incomplete native source pack inventory")
    return bundle


def prepare_catalog(root: Path = ROOT, *, scratch_root: Path | None = None,
                    documents: dict | None = None, revision: str | None = None,
                    output_ids=None) -> dict:
    """Prepare source transports and a route map for the held admitted universe."""
    from _native_print import admitted_documents, source_revision
    import _print_document as printing
    root = Path(root).resolve()
    documents = admitted_documents(root) if documents is None else documents
    revision = source_revision(root) if revision is None else revision
    wanted = sorted(documents if output_ids is None else output_ids)
    _need(len(set(wanted)) == len(wanted) and all(value in documents for value in wanted),
          "native source catalog contains an unadmitted or duplicate output")
    papal = {}
    if any(value.startswith("papal:") for value in wanted):
        papal = {row["id"]: row for row in printing._papal_records(root, printing._papal_plan(root))}
    recipes = [papal.get(identity) or printing.select(documents[identity]["document"],
               documents[identity]["edition"], root=root) for identity in wanted]
    checked = printing.check_many(recipes, root=root)
    routes, assets, source_paths, cache, prepared = {}, {}, set(), {}, {}
    for identity, recipe in zip(wanted, checked, strict=True):
        bundle = prepare_bundle(identity, root=root, scratch_root=scratch_root, documents=documents,
                                revision=revision, recipe=recipe, fingerprint_cache=cache,
                                external_assets=assets, _checked=True)
        prepared[identity] = bundle
        source_paths.update(row["path"] for row in bundle["source_inputs"])
    occurrences = Counter(row["sha256"] for bundle in prepared.values() for row in bundle["files"]
                          if row["encoding"] == "utf8" and row["bytes"] > 0
                          and PurePosixPath(row["path"]).suffix.lower() in _TEXT_SUFFIXES)
    shared_text = {digest for digest, count in occurrences.items() if count > 1}
    for identity in wanted:
        original = prepared.pop(identity)
        bundle = _externalize(original, assets, shared_text=shared_text)
        payload = canonical(bundle) + b"\n"
        route = SOURCE_ROUTE + "/" + bundle["content_sha256"] + ".json"
        _need(route not in assets, "duplicate native source bundle transport")
        assets[route] = payload
        routes[identity] = {"route": route, "bytes": len(payload), "sha256": _sha(payload)}
    return {"schema": CATALOG_SCHEMA, "source_revision": revision, "bundles": routes,
            "assets": assets, "source_paths": sorted(source_paths)}


# Descriptive alias retained for callers that prepare a complete held batch.
prepare_bundles = prepare_catalog
