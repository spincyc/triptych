"""Selected-source print recipes; never install or depend on installed PDFs.

Publication typography remains authored TeX. Source editions retain their owning
typesetters and rights gates. This is orchestration, not another text converter.
The cheap publication_recipe API is also used by static print landing pages.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from _bible_editions import EDITIONS
from _proper_components import companion_owner, outputs
from _tooling import examples_live_on_the_verbs, print_json, with_examples

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "triptych-print-document/v1"
FAMILIES = ("publication", "bible", "reading-plan", "papal")
PROVIDERS = ("claude", "gpt")
SAFE_ID = re.compile(r"[a-z0-9][a-z0-9./-]*\Z")


class PrintError(ValueError):
    pass


def _identifier(value: str) -> str:
    if (not isinstance(value, str) or not SAFE_ID.fullmatch(value)
            or ".." in value or "//" in value or value.endswith("/")):
        raise PrintError("document identities must be lowercase relative identifiers without traversal")
    return value


def _source_path(root: Path, value: str) -> Path:
    path = root / value
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise PrintError("source path escapes the repository or is a symlink: " + value)
    return path


def _environment() -> dict[str, str]:
    # A caller's parent Make invocation must not broaden the selected build.
    environment = {key: value for key, value in os.environ.items()
                   if key not in {"MAKEFLAGS", "MFLAGS", "MAKEOVERRIDES"}
                   and not key.startswith("PAPAL_")}
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return environment


def _run(argv: list[str], root: Path, *, log: Path | None = None) -> str:
    try:
        result = subprocess.run(argv, cwd=root, env=_environment(), text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as error:
        raise PrintError(f"cannot run {argv[0]}: {error}") from error
    if log is not None:
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode:
        detail = (result.stderr.strip() or result.stdout.strip())[-3000:]
        location = f"; log: {log}" if log is not None else ""
        raise PrintError(f"{argv[0]} failed ({result.returncode}){location}: {detail}")
    return result.stdout


def _tool(root: Path, name: str, *arguments: str) -> list[str]:
    return [sys.executable, str(root / "tools" / name), *arguments]


def _json_tool(root: Path, name: str, *arguments: str) -> dict:
    try:
        return json.loads(_run(_tool(root, name, *arguments, "--json"), root))
    except json.JSONDecodeError as error:
        raise PrintError(f"{name} did not return a JSON object") from error


def _relative(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as error:
        raise PrintError("print dependency escapes the repository") from error


def publication_recipe(provider: str, output: str, *, root: Path = ROOT) -> dict:
    """Describe one actual entrypoint without requiring a PDF or conversion.

``output`` may be a canonical leaf or a declared synthesis/homily output stem.
The dependency roots are a discovery aid; check resolves Make's declared render
inputs, and build retains the existing recorder validation of that graph.
"""
    root = Path(root).resolve()
    if provider not in PROVIDERS:
        raise PrintError("unknown publication provider: " + str(provider))
    _identifier(output)
    source_root = root / "src" / provider
    leaf = source_root / output
    entry = leaf / "main.tex"
    edition = "main"
    if not entry.is_file():
        try:
            companion = companion_owner(source_root, output)
        except (ValueError, OSError) as error:
            raise PrintError(str(error)) from error
        if companion is None:
            raise PrintError("no canonical or declared companion entrypoint: " + provider + "/" + output)
        leaf, entry = companion
        edition = "homily" if output.endswith("-homily") else "synthesis"
    _source_path(root, _relative(root, entry))
    if not entry.is_file():
        raise PrintError("missing publication entrypoint")
    try:
        from _corpus import title_of
        title = title_of(entry, provider, root=root).text
    except (OSError, ValueError, RuntimeError):
        title = None
    canonical = leaf.relative_to(source_root).as_posix()
    identity = f"publication:{provider}/{output}"
    dependencies = [_relative(root, entry), "Makefile"]
    for filename in ("generation-metadata.tex", "proper-components.toml"):
        path = leaf / filename
        if path.is_file():
            dependencies.append(_relative(root, path))
    return {"id": identity, "family": "publication", "provider": provider,
            "document": output, "canonical": canonical, "edition": edition,
            "title": title, "entrypoint": _relative(root, entry), "source_format": "latex",
            "formats": ["pdf"], "dependencies": sorted(set(dependencies)),
            "dependency_roots": [_relative(root, leaf), "src/common"],
            "dependency_model": "selected Make target; recorder-checked during compilation",
            "recipe": "make doc", "command": ["tools/tpt", "print-document", "build", "--document", identity],
            "qualifications": ["Canonical authored layout, figures and source notices are preserved.",
                               "Generated output is not a new visual-review or publication approval."]}


def _publication_records(root: Path, provider: str | None) -> list[dict]:
    records = []
    for owner in (provider,) if provider else PROVIDERS:
        for entry in sorted((root / "src" / owner).glob("**/main.tex")):
            leaf = entry.parent.relative_to(root / "src" / owner).as_posix()
            records.append(publication_recipe(owner, leaf, root=root))
            manifest = entry.parent / "proper-components.toml"
            if manifest.is_file():
                import tomllib
                try:
                    declared = outputs(tomllib.loads(manifest.read_text(encoding="utf-8")))
                except (OSError, ValueError) as error:
                    raise PrintError(f"invalid companion manifest {manifest}: {error}") from error
                for mode in ("synthesis", "homily"):
                    if mode in declared:
                        records.append(publication_recipe(owner, declared[mode], root=root))
    return records


def _bible_recipe(identifier: str, root: Path) -> dict:
    _identifier(identifier)
    record = EDITIONS.get(identifier)
    if record is None:
        raise PrintError("unknown Bible edition: " + identifier)
    if not record.get("publishable"):
        raise PrintError("Bible edition is not authorized for redistribution or print: " + identifier)
    artifact_root = root / "src/sources/works" / str(record["artifacts"])
    # The owning resolver also reads the canonical concordances and paragraph
    # projection, even when the selected wording is another edition's.
    canonical = root / "src/sources/works" / str(EDITIONS["douay-rheims"]["artifacts"])
    dependencies = {path for folder in (artifact_root, canonical)
                    for path in folder.rglob("*") if path.is_file()}
    dependencies.update(folder.parent / "edition.toml" for folder in (artifact_root, canonical))
    dependencies.update(root / relative for relative in (
        "tools/typeset-bible", "tools/index-bible", "scripts/_bible_editions.py",
        "scripts/_bible_artifacts.py", "scripts/_paragraphs.py", "scripts/_projection.py",
        "scripts/_psalms.py", "scripts/_deuterocanon.py", "scripts/_canon.py"))
    identity = "bible:" + identifier
    return {"id": identity, "family": "bible", "document": identifier,
            "title": record["label"], "source_format": "verse-tsv", "formats": ["pdf", "tex"],
            "dependencies": sorted(_relative(root, path) for path in dependencies),
            "recipe": "typeset-bible", "command": ["tools/tpt", "print-document", "build", "--document", identity],
            "qualifications": ["The selected edition's rights, native numbering, paragraph provenance and font substitutions remain explicit."]}


def _plan_records(root: Path) -> list[dict]:
    plans = sorted((root / "src/sources/reading-plans").glob("*.yaml"))
    records = []
    for plan in plans:
        data = _json_tool(root, "typeset-bible", "list", "--plan", plan.stem)
        for volume in data.get("volumes", []):
            identity = "reading-plan:" + volume["id"]
            bible = _bible_recipe(volume["bible"], root)
            records.append({"id": identity, "family": "reading-plan", "document": volume["id"],
                            "plan": plan.stem, "bible": volume["bible"], "tier": volume["tier"],
                            "title": volume["track"] + " — " + volume["label"],
                            "source_format": "reading-plan-yaml-and-verse-tsv", "formats": ["pdf", "tex"],
                            "dependencies": sorted(set(bible["dependencies"] + [_relative(root, plan)])),
                            "recipe": "typeset-bible --volume",
                            "command": ["tools/tpt", "print-document", "build", "--document", identity],
                            "qualifications": ["An abridged selection, preserving its omissions, notes, tier and selected Bible's own rights and font qualifications."]})
    return records


def _papal_plan(root: Path) -> dict:
    # Make owns the ordered component set, including optional new withdrawals.
    # Resolving metadata writes only a disposable plan, never a reader PDF.
    scratch = _scratch_root(root)
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="source-plan-", dir=scratch) as folder:
        target = Path(folder) / "current.json"
        _run(["make", "--no-print-directory", "papal-plan", f"PYTHON={sys.executable}",
              f"PAPAL_CURRENT_MANIFEST={target}"], root)
        try:
            data = json.loads(target.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise PrintError("cannot read the current papal source-selection plan") from error
    if data.get("schema") != "triptych-papal-typeset/v1" or not isinstance(data.get("documents"), list):
        raise PrintError("current papal source-selection plan is malformed")
    return data


def _papal_records(root: Path, plan: dict) -> list[dict]:
    records = []
    plan_inputs = [item["path"] for item in plan.get("selection_plan", {}).get("inputs", [])]
    for row in plan["documents"]:
        identity = "papal:" + row["id"] + "/" + row["language"]
        payload = _source_path(root, row["text_path"])
        dependencies = [row["text_path"], _relative(root, payload.parent / "artifact.toml")]
        if row.get("segment_path"):
            dependencies.append(row["segment_path"])
            edition = _source_path(root, row["segment_path"]).parents[1] / "edition.toml"
        else:
            edition = payload.parents[2] / "edition.toml"
        dependencies.append(_relative(root, edition))
        records.append({"id": identity, "family": "papal", "document": row["id"],
                        "language": row["language"], "title": row["title"],
                        "source_format": "source-library-plaintext-selection", "formats": ["pdf", "tex"],
                        "dependencies": sorted(set(dependencies + plan_inputs)),
                        "recipe": "typeset-papal, current source selection",
                        "command": ["tools/tpt", "print-document", "build", "--document", identity],
                        "qualifications": [row.get("source_note", "Source transcription; typesetting is not historical image collation."),
                                           row.get("rights_notice", row["rights_basis"])],
                        "_source_row": row, "_revision": plan["revision"]})
    return records


def recipes(root: Path = ROOT, *, family: str | None = None, provider: str | None = None) -> list[dict]:
    root = Path(root).resolve()
    selected = (family,) if family else FAMILIES
    records = []
    if "publication" in selected:
        records.extend(_publication_records(root, provider))
    if "bible" in selected:
        records.extend(_bible_recipe(name, root) for name, value in EDITIONS.items() if value.get("publishable"))
    if "reading-plan" in selected:
        records.extend(_plan_records(root))
    if "papal" in selected:
        records.extend(_papal_records(root, _papal_plan(root)))
    return sorted(records, key=lambda row: row["id"])


def select(identity: str, edition: str = "main", *, root: Path = ROOT) -> dict:
    root = Path(root).resolve()
    family, separator, identifier = identity.partition(":")
    if not separator or family not in FAMILIES:
        raise PrintError("document requires a family prefix: " + ", ".join(name + ":ID" for name in FAMILIES))
    _identifier(identifier)
    if family == "publication":
        provider, slash, document = identifier.partition("/")
        if not slash:
            raise PrintError("publication identity requires provider/leaf")
        if edition in {"synthesis", "homily"}:
            base = publication_recipe(provider, document, root=root)
            if base["edition"] not in {"main", edition}:
                raise PrintError("edition contradicts the selected output identity")
            document = base["canonical"] + "-" + edition
        return publication_recipe(provider, document, root=root)
    if edition not in {"main", "research", "full"}:
        raise PrintError("companion edition choices apply only to provider publications")
    if family == "bible":
        return _bible_recipe(identifier, root)
    if family == "reading-plan":
        candidates = _plan_records(root)
    else:
        candidates = _papal_records(root, _papal_plan(root))
    matches = [row for row in candidates if row["id"] == identity]
    if len(matches) != 1:
        raise PrintError("no unique current print recipe: " + identity)
    return matches[0]


def _scratch_root(root: Path) -> Path:
    """Allow a service to isolate every request without moving canonical sources."""
    configured = os.environ.get("TRIPTYCH_PRINT_WORK_ROOT")
    scratch = root / ".scratch/print-document" if configured is None else Path(configured)
    if configured is not None and (not configured or not scratch.is_absolute()):
        raise PrintError("TRIPTYCH_PRINT_WORK_ROOT must be a nonempty absolute path")
    if scratch == Path(scratch.anchor):
        raise PrintError("print scratch must not be the filesystem root")
    if any(path.is_symlink() for path in (scratch, *scratch.parents)):
        raise PrintError("print scratch directories must not contain symlinks")
    return _destination(scratch, root)


def _work_root(root: Path, recipe: dict) -> Path:
    digest = hashlib.sha256(recipe["id"].encode()).hexdigest()[:16]
    work = _scratch_root(root) / digest
    if work.is_symlink():
        raise PrintError("print scratch directories must not be symlinks")
    return work


def _make_arguments(recipe: dict, work: Path) -> tuple[list[str], Path]:
    family, document = recipe["family"], recipe["document"]
    if family == "publication":
        build = work / "build" / recipe["provider"]
        return ["make", "--no-print-directory", "doc", f"PROVIDER={recipe['provider']}",
                f"DOC={document}", f"DOCUMENTS={document}", f"BUILD_ROOT={build}",
                f"PYTHON={sys.executable}", "PDFLATEX=pdflatex"], build / (document + ".pdf")
    variable = "BIBLE_BUILD_ROOT" if family == "bible" else "READING_BUILD_ROOT"
    build = work / "build"
    pdf = build / (document + ".pdf")
    return ["make", "--no-print-directory", str(pdf), f"{variable}={build}", f"PYTHON={sys.executable}", "PDFLATEX=pdflatex"], pdf


def _declared_dependencies(root: Path, recipe: dict) -> list[str]:
    """Ask Make for the selected PDF's graph without executing any recipe."""
    command, target = _make_arguments(recipe, _work_root(root, recipe))
    command = ["make", "--no-print-directory", "-qp", str(target), *command[3:]]
    run = subprocess.run(command, cwd=root, env=_environment(), capture_output=True, text=True)
    if run.returncode not in (0, 1):
        raise PrintError("cannot inspect the selected Make dependency graph: " + run.stderr[-2000:])
    prefix = str(target) + ":"
    line = next((line for line in run.stdout.splitlines() if line.startswith(prefix)), None)
    if line is None:
        raise PrintError("selected PDF target is absent from Make's dependency graph")
    return _dependencies_from_line(root, recipe, line[len(prefix):])


def _dependencies_from_line(root: Path, recipe: dict, prerequisites: str) -> list[str]:
    dependencies = set(recipe["dependencies"])
    for value in prerequisites.split("|", 1)[0].split():
        if value.endswith(".revision.tex"):
            continue  # the build's derived stamp (scripts/_edition_revision.py), not a source
        path = Path(value)
        if not path.is_absolute():
            path = root / path
        if path.is_dir():
            dependencies.update(_relative(root, child) for child in path.rglob("*") if child.is_file())
        elif path.is_file() and path.resolve().is_relative_to(root):
            dependencies.add(_relative(root, path))
    return sorted(dependencies)


def _declared_dependencies_many(root: Path, recipes: list[dict]) -> dict[str, list[str]]:
    """Read the selected targets together, with the same Make-owned edges."""
    if len({recipe["id"] for recipe in recipes}) != len(recipes):
        raise PrintError("batch print recipes must have unique document identities")
    dependencies = {}
    for provider in PROVIDERS:
        selected = [recipe for recipe in recipes if recipe["provider"] == provider]
        if not selected:
            continue
        work = _scratch_root(root) / "dependency-query" / provider
        base, _ = _make_arguments(selected[0], work)
        targets = {str(_make_arguments(recipe, work)[1]): recipe for recipe in selected}
        variables = [argument for argument in base[3:]
                     if not argument.startswith(("DOC=", "DOCUMENTS="))]
        variables.append("DOCUMENTS=" + " ".join(sorted(recipe["document"] for recipe in selected)))
        command = ["make", "--no-print-directory", "-qp", *targets, *variables]
        run = subprocess.run(command, cwd=root, env=_environment(), capture_output=True, text=True)
        if run.returncode not in (0, 1):
            raise PrintError("cannot inspect the selected Make dependency graph: " + run.stderr[-2000:])
        pending = set(targets)
        for line in run.stdout.splitlines():
            target, separator, prerequisites = line.partition(":")
            if separator and target in pending:
                recipe = targets[target]
                dependencies[recipe["id"]] = _dependencies_from_line(root, recipe, prerequisites)
                pending.remove(target)
        if pending:
            raise PrintError("selected PDF target is absent from Make's dependency graph")
    if len(dependencies) != len(recipes):
        raise PrintError("batch print recipes require known publication providers")
    return dependencies


def public_recipe(recipe: dict) -> dict:
    return {key: value for key, value in recipe.items() if not key.startswith("_")}


def check(recipe: dict, *, root: Path = ROOT) -> dict:
    root = Path(root).resolve()
    recipe = dict(recipe)
    if recipe["family"] == "publication":
        _run(_tool(root, "check-generation-metadata", "--provider", recipe["provider"],
                   "--document", recipe["document"]), root)
        recipe["dependencies"] = _declared_dependencies(root, recipe)
        validation = {"source_metadata": "pass", "declared_build_graph": "pass"}
    elif recipe["family"] in {"bible", "reading-plan"}:
        flag = "--bible" if recipe["family"] == "bible" else "--volume"
        validation = _json_tool(root, "typeset-bible", "check", flag, recipe["document"])
    else:
        import _typeset_papal as papal
        try:
            papal.validate_document(recipe["_source_row"], root)
        except (ValueError, OSError) as error:
            raise PrintError(str(error)) from error
        validation = {"exact_source_selection": "pass", "distribution_rights": "pass"}
    recipe["validation"] = validation
    recipe["status"] = "valid"
    return recipe


def check_many(recipes: list[dict], *, root: Path = ROOT) -> list[dict]:
    """Check one held selection without repeating Make discovery per edition.

    Metadata and non-publication checks remain the owning single-document gates.
    No result is cached across calls, and no Make recipe or TeX engine runs.
    """
    root = Path(root).resolve()
    recipes = list(recipes)
    publications = [recipe for recipe in recipes if recipe["family"] == "publication"]
    for recipe in publications:
        _run(_tool(root, "check-generation-metadata", "--provider", recipe["provider"],
                   "--document", recipe["document"]), root)
    dependencies = _declared_dependencies_many(root, publications)
    checked = []
    for recipe in recipes:
        if recipe["family"] != "publication":
            checked.append(check(recipe, root=root))
            continue
        result = dict(recipe, dependencies=dependencies[recipe["id"]], status="valid",
                      validation={"source_metadata": "pass", "declared_build_graph": "pass"})
        checked.append(result)
    return checked


def _destination(path: Path, root: Path) -> Path:
    path = path.expanduser()
    if path.is_symlink():
        raise PrintError("print destination must not be a symlink")
    target = path.resolve()
    if target == root or target.is_relative_to(root):
        allowed = any(target.is_relative_to(root / directory) and target != root / directory
                      for directory in (".scratch", "build"))
        if not allowed:
            raise PrintError("inside the repository, print output belongs beneath .scratch/ or build/")
    return target


def _fingerprints(root: Path, dependencies: list[str]) -> list[dict]:
    records = []
    for value in dependencies:
        path = _source_path(root, value)
        if not path.is_file():
            raise PrintError("missing canonical print dependency: " + value)
        payload = path.read_bytes()
        records.append({"path": value, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    return records


def _copy(source: Path, target: Path) -> None:
    if target.is_symlink():
        raise PrintError("refusing to replace a symlink output")
    with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".print-", delete=False) as stream:
        temporary = Path(stream.name)
    try:
        shutil.copyfile(source, temporary)
        temporary.replace(target)
    finally:
        temporary.unlink(missing_ok=True)


def _render_environment(recipe: dict, product: Path, output_format: str) -> dict:
    """Describe the effective local render, without claiming a pinned toolchain."""
    result = {"identity_scope": "source-output-attestation",
              "limitation": "External TeX packages, fonts and system libraries are not pinned by this receipt; another toolchain can produce different PDF bytes.",
              "options": {"output_format": output_format, "recipe": recipe["recipe"],
                          "paper_and_typography": "declared in the hashed canonical or generated TeX"}}
    if recipe["family"] == "papal":
        result["options"]["render_revision"] = recipe["_source_row"].get("revision", recipe["_revision"])
    if output_format != "pdf":
        return result
    engine = "xelatex" if recipe["family"] == "papal" else "pdflatex"
    versions = {}
    for executable, flag in ((engine, "--version"), ("pdfinfo", "-v")):
        run = subprocess.run([executable, flag], capture_output=True, text=True, env=_environment())
        if run.returncode:
            raise PrintError("cannot identify print toolchain: " + executable)
        lines = (run.stdout + run.stderr).strip().splitlines()
        versions[executable] = lines[0] if lines else "version not reported"
    fonts = subprocess.run(["pdffonts", str(product)], capture_output=True, text=True, env=_environment())
    if fonts.returncode:
        raise PrintError("cannot inspect the generated PDF's embedded fonts")
    result.update(versions=versions, embedded_font_report=fonts.stdout.splitlines(),
                  environment={key: os.environ[key] for key in ("LANG", "LC_ALL", "LC_CTYPE", "TZ", "SOURCE_DATE_EPOCH", "FORCE_SOURCE_DATE") if key in os.environ})
    return result


def _settle_generated_pdf(root: Path, product: Path, work: Path) -> int:
    """Close source-edition references at an auxiliary-file fixed point.

The owning Make recipe still runs first. This strengthens its two-pass Bible
and warning-based track recipes without weakening any of their source gates.
"""
    def fingerprint():
        return [(path.name, hashlib.sha256(path.read_bytes()).hexdigest())
                for path in sorted(product.parent.glob(product.stem + ".*"))
                if path.is_file() and path.suffix not in {".pdf", ".log", ".fls"}]

    previous = fingerprint()
    for count in range(1, 6):
        _run(["pdflatex", "-no-shell-escape", "-recorder", "-interaction=nonstopmode", "-halt-on-error",
              "-output-directory=" + str(product.parent), str(product.with_suffix(".tex"))],
             root, log=work / f"settle-{count}.log")
        current = fingerprint()
        log = product.with_suffix(".log").read_text(encoding="utf-8", errors="replace")
        unresolved = re.search(r"Rerun to get cross-references right|undefined references|Missing character", log)
        if current == previous and not unresolved:
            return count
        previous = current
    raise PrintError("selected source edition's references or glyphs did not settle in five additional passes")


def _portable_receipt(result: dict, root: Path, work: Path, destination: Path) -> dict:
    """Keep physical paths in the runtime result, not in shareable metadata."""
    replacements = ((str(destination), "<output>"), (str(work), "<print-work>"),
                    (str(root), "<repository>"))

    def clean(value):
        if isinstance(value, str):
            if value == sys.executable:
                value = "<python>"
            elif value == "PYTHON=" + sys.executable:
                value = "PYTHON=<python>"
            for physical, logical in replacements:
                value = value.replace(physical, logical)
            if re.search(r"(?<![A-Za-z0-9:/])/(?:home|Users|tmp|var/tmp)/", value):
                raise PrintError("print metadata contains an unredacted machine-local path")
            return value
        if isinstance(value, list):
            return [clean(item) for item in value]
        if isinstance(value, dict):
            return {key: clean(item) for key, item in value.items()}
        return value

    saved = clean(result)
    saved["path_base"] = "receipt-directory"
    saved["output"] = Path(result["output"]).name
    saved["receipt"] = Path(result["receipt"]).name
    return saved


def _assert_papal_current(recipe: dict, root: Path) -> None:
    # An optional withdrawal manifest can be added without modifying any file
    # already in the first plan's input set. Re-resolve before exporting bytes.
    plan = _papal_plan(root)
    selected = [row for row in plan["documents"]
                if (row.get("id"), row.get("language")) == (recipe["document"], recipe["language"])]
    if len(selected) != 1 or selected[0] != recipe["_source_row"]:
        raise PrintError("papal source selection changed or was withdrawn during printing; no output was exported")


def _build(recipe: dict, *, output_format: str = "pdf", out: Path | None = None, root: Path = ROOT) -> dict:
    root = Path(root).resolve()
    if output_format not in recipe["formats"]:
        raise PrintError("selected recipe supports only: " + ", ".join(recipe["formats"]))
    work = _work_root(root, recipe)
    destination = _destination(out if out is not None else work / "output", root)
    recipe = check(recipe, root=root)
    software = ("Makefile", "tools/print-document", "scripts/_print_document.py")
    if recipe["family"] == "papal":
        software += ("scripts/_typeset_papal.py", "scripts/_papal_collection.py")
    recipe["dependencies"] = sorted(set(recipe["dependencies"]) |
                                    {name for name in software if (root / name).is_file()})
    inputs = _fingerprints(root, recipe["dependencies"])
    work.mkdir(parents=True, exist_ok=True)
    family = recipe["family"]
    qualification = "Generated from canonical sources; no new visual-review or publication approval is implied."
    if family == "papal":
        import _typeset_papal as papal
        row = papal.validate_document(recipe["_source_row"], root)
        manifest = {"schema": papal.SCHEMA, "revision": recipe["_revision"], "documents": [recipe["_source_row"]]}
        receipt = papal.render_documents(manifest, [row], work / "build", compile_pdf=output_format == "pdf", jobs=1)
        if receipt["errors"]:
            raise PrintError("selected papal render failed: " + receipt["errors"][0]["error"])
        generated = receipt["documents"][0]
        product = work / "build" / generated[output_format]
        validation = {"owning_typesetter": generated}
    elif output_format == "tex":
        flag = "--bible" if family == "bible" else "--volume"
        rendered = _json_tool(root, "typeset-bible", "render", flag, recipe["document"], "--out", str(work / "build"))
        if len(rendered.get("rendered", [])) != 1:
            raise PrintError("typesetter did not produce exactly one selected source")
        product = Path(rendered["rendered"][0]["path"])
        validation = {"owning_typesetter": rendered}
    else:
        command, product = _make_arguments(recipe, work)
        if not product.resolve().is_relative_to(work.resolve()):
            raise PrintError("selected build path escapes its print scratch directory")
        _run(command, root, log=work / "build.log")
        validation = {"owning_build": "pass", "command": command}
        if family in {"bible", "reading-plan"}:
            validation["fixed_point_additional_passes"] = _settle_generated_pdf(root, product, work)
    if not product.is_file() or product.stat().st_size == 0:
        raise PrintError("selected recipe did not create its expected nonempty output")
    render_environment = _render_environment(recipe, product, output_format)
    if family == "papal":
        generated_source = work / "build" / generated["tex"]
    elif family in {"bible", "reading-plan"}:
        generated_source = product.with_suffix(".tex")
    else:
        generated_source = None
    if generated_source is not None:
        render_environment["generated_tex_sha256"] = hashlib.sha256(generated_source.read_bytes()).hexdigest()
    if family == "papal":
        _assert_papal_current(recipe, root)
        validation["current_selection_rechecked"] = True
    if inputs != _fingerprints(root, recipe["dependencies"]):
        raise PrintError("canonical inputs changed during printing; no output was exported")
    destination.mkdir(parents=True, exist_ok=True)
    name = recipe["document"].rsplit("/", 1)[-1][:100] + "--" + work.name
    target = destination / (name + "." + output_format)
    receipt_path = destination / (name + ".print.json")
    if receipt_path.is_symlink():
        raise PrintError("refusing to replace a symlink receipt")
    result = {"schema": SCHEMA, "status": "built", "document": public_recipe(recipe),
              "output": str(target), "output_format": output_format,
              "output_sha256": hashlib.sha256(product.read_bytes()).hexdigest(),
              "bytes": product.stat().st_size, "inputs": inputs, "mechanical_validation": validation,
              "receipt_kind": "source-output-attestation", "render_environment": render_environment,
              "review_status": "generated-unreviewed", "qualification": qualification}
    result["receipt"] = str(receipt_path)
    saved = _portable_receipt(result, root, work, destination)
    _copy(product, target)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination, prefix=".print-", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(json.dumps(saved, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    try:
        temporary.replace(receipt_path)
    finally:
        temporary.unlink(missing_ok=True)
    return result


def build(recipe: dict, *, output_format: str = "pdf", out: Path | None = None, root: Path = ROOT) -> dict:
    root = Path(root).resolve()
    if output_format not in recipe["formats"]:
        raise PrintError("selected recipe supports only: " + ", ".join(recipe["formats"]))
    work = _work_root(root, recipe)
    _destination(out if out is not None else work / "output", root)
    work.mkdir(parents=True, exist_ok=True)
    lock = work / "print.lock"
    if lock.is_symlink():
        raise PrintError("print lock must not be a symlink")
    with lock.open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        return _build(recipe, output_format=output_format, out=out, root=root)


def main(argv: list[str] | None = None, *, examples: dict | None = None) -> int:
    examples = examples or {}
    parser = argparse.ArgumentParser(prog="print-document", description="Print one selected canonical publication or source edition on demand.")
    examples_live_on_the_verbs(parser, "print-document")
    commands = parser.add_subparsers(dest="verb", required=True)
    for name in ("list", "check", "build"):
        sub = commands.add_parser(name)
        with_examples(sub, examples.get(name, ()))
        sub.add_argument("--json", action="store_true", help="emit one machine-readable JSON object")
        sub.add_argument("--format", choices=("text", "json"), default="text", help="report format")
        if name == "list":
            sub.add_argument("--family", choices=FAMILIES)
            sub.add_argument("--provider", choices=PROVIDERS)
        else:
            sub.add_argument("--document", required=True, help="publication:provider/leaf, bible:ID, reading-plan:volume, or papal:ID/language")
            sub.add_argument("--edition", choices=("main", "research", "full", "synthesis", "homily"), default="main")
        if name == "build":
            sub.add_argument("--output-format", choices=("pdf", "tex"), default="pdf")
            sub.add_argument("--out", type=Path, help="output directory; default: .scratch/print-document/<selection>/output")
    arguments = parser.parse_args(argv)
    try:
        if arguments.verb == "list":
            rows = recipes(family=arguments.family, provider=arguments.provider)
            result = {"schema": SCHEMA, "status": "ok", "documents": [public_recipe(row) for row in rows]}
        else:
            selected = select(arguments.document, arguments.edition)
            if arguments.verb == "check":
                result = {"schema": SCHEMA, "status": "valid", "document": public_recipe(check(selected))}
            else:
                result = build(selected, output_format=arguments.output_format, out=arguments.out)
        if arguments.json or arguments.format == "json":
            print_json(result)
        elif arguments.verb == "list":
            for row in result["documents"]:
                print(row["id"] + "\t" + ",".join(row["formats"]) + "\t" + (row.get("title") or row["id"]))
        elif arguments.verb == "check":
            print("valid: " + result["document"]["id"])
        else:
            for label, key in (("built", "output"), ("receipt", "receipt")):
                path = Path(result[key])
                display = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
                print(label + ": " + display)
        return 0
    except (PrintError, OSError, ValueError) as error:
        print("print-document error: " + str(error), file=sys.stderr)
        return 2
