"""Offline producers for disposable browser data, with canonical input scopes.

Recipes own logical output paths. Every invocation receives an explicit empty
staging destination; the old tracked projection and sealed caches are never
producer inputs. A recipe declares only the data its producer reads: data
trees and individual files outside scripts/ and tools/. Its code is never
listed here; `_browser_product_inputs` computes each producer's code closure,
and `tools/browser-products audit` proves that the two together cover every
repository path the producer touches. Source and act-history deliberately
retain broad data scopes, and the other source-text consumers the whole source
library, until a narrower data closure has been proved.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile

from _browser_products import ProductError, _validate_recipes, assert_working_output
from _browser_product_inputs import ADAPTERS


# Neither act-history nor source-reader reads workflows/ beyond the authority
# records below (2026-11-04 audit), so new review records stale neither.
_BROAD = ["src/sources", "src/gpt", "src/claude", "src/common", "web"]
_SOURCE = ["src/sources"]
# The source library preflights and loads every publication's bindings.
_LIBRARY = ["src/sources", "src/gpt", "src/claude"]
_CALENDAR = ["src/sources/calendars", "src/sources/inventories"]
# Reviewed authority records the proper text pipeline reads by fixed path.
_LATIN_AUTHORITIES = [
    "workflows/reviews/missal-english-completion-2026-10-29/roman-1962/finite-latin-authority-v2.json",
    "workflows/reviews/missal-reader-completion-2026-10-26/gregem-damasus-qualified-rights-adoption.json",
]
_EXECUTION_AUTHORITIES = [
    "workflows/reviews/reader-completion-2026-10-26/finite-name-two-authority.json",
    "workflows/reviews/reader-completion-2026-10-26/finite-name-two-root-adoption.json",
    "workflows/reviews/reader-completion-2026-10-26/oration-execution-six-authority.json",
]


def _recipe(identifier, prefix, argv, trees, files=(), *, delivery):
    return {
        "id": identifier, "version": 1, "output_prefixes": [prefix],
        "argv": argv, "input_trees": list(trees), "input_files": list(files),
        "exclude_paths": [], "delivery": delivery,
    }


# Tokens are expanded as complete argv entries, never as shell text. Options
# that determine corpus membership or civil dates are explicit and timeless.
RECIPES = (
    _recipe("bibles", "bibles.json", ["tools/index-bible", "manifest", "--bible-root", "{root}/src/sources/bibles"], _SOURCE, delivery="browser-data"),
    _recipe("encyclicals", "encyclicals", ["scripts/_encyclicals.py", "--root", "{root}", "structure"],
            ["src/sources/papal-documents", "release/papal-documents"], ["release/papal-documents.json"], delivery="browser-data"),
    _recipe("act-history", "structure/act-history", ["tools/act-history", "structure"], _BROAD,
            ["guidance/liturgical-text-publication-policy.md"], delivery="browser-data"),
    _recipe("calendar", "structure/calendar", ["tools/calendar-days", "structure", "--root", "{root}/src/sources/calendars", "--first", "2020", "--last", "2120"], _CALENDAR, delivery="browser-data"),
    _recipe("catena", "structure/catena", ["scripts/_catena.py", "--root", "{root}", "structure"], _SOURCE,
            ["src/web/browser/catena/catena-model.js"], delivery="browser-data"),
    # Assembly resolves both provider-owned inputs and fallbacks under src/;
    # its postconciliar projection also reads the fixed registry authority.
    _recipe("documents", "structure/documents", ["tools/document-library", "structure"],
            ["src", "web", "workflows/fragments", "workflows/pipelines", "workflows/schema", "release/publications"],
            ["guidance/liturgy/postconciliar-propers-registry.md"], delivery="browser-data"),
    _recipe("ordinary", "structure/ordinary", ["tools/mass-ordinary", "structure", "--root", "{root}/src/sources"], _SOURCE, delivery="browser-data"),
    _recipe("paragraphs", "structure/paragraphs", ["scripts/_catena.py", "--root", "{root}", "paragraphs"], _SOURCE, delivery="browser-data"),
    _recipe("propers", "structure/propers", ["tools/mass-propers", "structure", "--root", "{root}/src/sources/calendars"], _LIBRARY,
            [*_LATIN_AUTHORITIES, *_EXECUTION_AUTHORITIES], delivery="browser-data"),
    _recipe("readings", "structure/readings", ["tools/reading-plan", "structure", "--root", "{root}/src/sources/reading-plans"], _SOURCE, delivery="browser-data"),
    _recipe("rubrics", "structure/rubrics", ["tools/calendar-rubrics", "structure", "--root", "{root}/src/sources/calendars"], _CALENDAR, delivery="browser-data"),
    _recipe("sources", "structure/sources", ["tools/source-reader", "structure", "--strict"], _BROAD,
            _LATIN_AUTHORITIES, delivery="browser-data"),
    # Every web reader's Markdown, converted at build time from canonical TeX
    # (guidance/web-editions.md). Consumed by the site build, never published as
    # browser data; the pinned Pandoc lock lives under src/common.
    # Release records decide each reader's publication status, so they are
    # inputs too (the cold audit found the read).
    _recipe("web-editions", "web-editions", ["tools/web-edition", "products"], ["src", "release/publications"],
            ["guidance/liturgy/postconciliar-propers-registry.md"],
            delivery="site-build"),
)


class RecipeError(ProductError):
    """A cold producer could not derive its complete declared family."""


_COLD_INPUT_GUARD = r'''
import os
import sys

_original_root = os.path.join(sys.argv[1], "release", "papal-documents", "inputs")
_original_roots = (os.path.abspath(_original_root), os.path.realpath(_original_root))

def _guard_original(path, directory=None):
    if isinstance(path, int):
        return
    path = os.fsdecode(path)
    if not os.path.isabs(path):
        if directory is None:
            path = os.path.join(os.getcwd(), path)
        else:
            try:
                parent = os.readlink("/proc/self/fd/" + str(directory))
            except OSError as error:
                raise PermissionError("cold producer cannot resolve a descriptor-relative input") from error
            path = os.path.join(parent, path)
    candidates = (os.path.abspath(path), os.path.realpath(path))
    if any(candidate == root or candidate.startswith(root + os.sep)
           for candidate in candidates for root in _original_roots):
        raise PermissionError("cold producer may not open historical input originals; use attested input-records")

def _audit_original(event, arguments):
    if event == "open":
        _guard_original(arguments[0])

_system_open = os.open
def _descriptor_open(path, flags, mode=0o777, *, dir_fd=None):
    _guard_original(path, dir_fd)
    return _system_open(path, flags, mode, dir_fd=dir_fd)

os.open = _descriptor_open
sys.addaudithook(_audit_original)
'''


def _owned(name: str, recipe: dict) -> bool:
    return any(name == prefix or name.startswith(prefix + "/")
               for prefix in recipe["output_prefixes"])


def _files(out: Path) -> set[str]:
    found = set()
    for path in out.rglob("*"):
        if path.is_symlink():
            raise RecipeError(f"producer output is a symlink: {path.relative_to(out)}")
        if path.is_dir():
            continue
        if not path.is_file() or path.suffix != ".json":
            raise RecipeError(f"producer output is not a regular JSON file: {path.relative_to(out)}")
        found.add(path.relative_to(out).as_posix())
    return found


def _run(root: Path, out: Path, recipe: dict, environment: dict) -> None:
    arguments = [value.replace("{root}", str(root)).replace("{out}", str(out)) for value in recipe["argv"]]
    arguments[0] = str(root / arguments[0])
    if "--out" not in arguments:
        arguments.extend(["--out", str(out)])
    program = _COLD_INPUT_GUARD + (
        "\nimport runpy\n"
        "tool_arguments = sys.argv[2:]\n"
        "sys.path.insert(0, os.path.dirname(tool_arguments[0]))\n"
        "sys.argv = tool_arguments\n"
        "runpy.run_path(tool_arguments[0], run_name='__main__')\n"
    )
    command = [sys.executable, "-B", "-c", program, str(root), *arguments]
    if recipe["id"] in ADAPTERS:
        # The owning replay supplies fresh isolated source parsers without
        # consulting the former installed projection.
        # The adapter module is part of the family's code closure.
        adapter = Path(ADAPTERS[recipe["id"]])
        program = _COLD_INPUT_GUARD + "\n" + (
            "from pathlib import Path; import sys; "
            f"sys.path.insert(0,str(Path(sys.argv[1])/{adapter.parent.as_posix()!r})); "
            f"from {adapter.stem} import _replay; "
            "_replay(Path(sys.argv[1]),Path(sys.argv[2]))"
        )
        command = [sys.executable, "-B", "-c", program, str(root), str(out)]
    finished = subprocess.run(
        command, cwd=root,
        env=environment, text=True, capture_output=True, check=False,
    )
    if finished.returncode:
        detail = (finished.stderr or finished.stdout).strip()
        raise RecipeError(f"{recipe['id']} producer exited {finished.returncode}: {detail[-3000:]}")


def generate(root: Path, out: Path, product_ids=None, *, environment=None) -> dict:
    """Derive selected families offline; omitted families never enter staging.

    Cross-layer checks consume product dependencies only after generation.
    None of these structure writers needs another browser family to exist.
    Source parsers may share newly populated process caches, but inherited
    stat-keyed disk caches and stale Python bytecode cannot seed a cold build.
    `environment` adds variables for an observer such as the input audit; it
    cannot re-enable a cache or bytecode this function disables.
    """
    _validate_recipes(list(RECIPES))
    root, out = Path(root).resolve(), Path(out).absolute()
    if out.is_symlink() or out == root / "src/web/data":
        raise RecipeError("cold generation requires a separate unsealed staging root")
    out = assert_working_output(root, out)
    if out.exists() and any(out.iterdir()):
        raise RecipeError("cold generation requires an empty staging root")
    requested = {recipe["id"] for recipe in RECIPES} if product_ids is None else set(product_ids)
    unknown = requested - {recipe["id"] for recipe in RECIPES}
    if unknown:
        raise RecipeError(f"unknown browser product families: {', '.join(sorted(unknown))}")
    if not requested:
        raise RecipeError("select at least one browser product family")
    out.mkdir(parents=True, exist_ok=True)
    summaries = []
    scratch = root / ".scratch/browser-product-recipes"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="cold-", dir=scratch) as state:
        environment = {
            **os.environ, **(environment or {}), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
            "PYTHONPYCACHEPREFIX": str(Path(state) / ("python-" + secrets.token_hex(12))),
            "TRIPTYCH_CORPUS_CACHE": "0", "TRIPTYCH_YAML_CACHE": "0",
            "TRIPTYCH_CONTAINMENT_CACHE": "0",
            "TRIPTYCH_LIBRARY_CACHE_DIR": str(Path(state) / "library"),
            "TRIPTYCH_SOURCE_LIBRARY_CACHE": "0", "LC_ALL": "C.UTF-8", "TZ": "UTC",
        }
        for recipe in RECIPES:
            if recipe["id"] not in requested:
                continue
            family_out = Path(state) / recipe["id"]
            family_out.mkdir()
            _run(root, family_out, recipe, environment)
            emitted = _files(family_out)
            if not emitted or any(not _owned(name, recipe) for name in emitted):
                raise RecipeError(f"{recipe['id']} emitted no complete family or wrote outside its owned paths")
            # Parsing is bounded by the actual emitted family and rejects a
            # successful command that wrote malformed or non-finite JSON.
            for name in sorted(emitted):
                source, target = family_out / name, out / name
                json.loads(source.read_bytes(), parse_constant=lambda value: (_ for _ in ()).throw(RecipeError(f"invalid JSON number {value}")))
                if target.exists() or target.is_symlink():
                    raise RecipeError(f"producer output overlaps another family: {name}")
                target.parent.mkdir(parents=True, exist_ok=True)
                source.rename(target)
            summaries.append({"id": recipe["id"], "files": len(emitted)})
    return {"products": summaries, "files": sum(item["files"] for item in summaries)}
