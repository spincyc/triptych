"""Cold, offline preparation of complete admitted publication and Bible prints."""
from __future__ import annotations

import argparse
import gc
import json
from pathlib import Path
import sys
import tempfile
import tomllib

sys.dont_write_bytecode = True

from _browser_products import assert_working_output
from _web_print_prepare import (AssetPool, CATALOG_SCHEMA, PREFIX, canonical_json, digest,
                                need, prepare_product, source_path, write_json)

ROOT = Path(__file__).resolve().parents[1]
HELPERS = ("scripts/_web_print_products.py", "scripts/_web_print_prepare.py", "scripts/_web_print_common.py",
           "scripts/_web_print_assets.py", "scripts/_print_document.py",
           "scripts/_web_print_publication.py", "scripts/_web_print_bibles.py",
           "scripts/_web_print_server.py", "scripts/_web_print_dictionaries.py",
           "scripts/_web_print_dictionary_context.py",
           "scripts/_web_print_server_schedule.py", "scripts/_web_print_server_card_schedule.py",
           "scripts/_web_print_semantics.py", "scripts/_web_print_flow.py", "scripts/_web_print_diagrams.py",
           "scripts/_web_print_server_diagrams.py", "scripts/_source_projection_receipt.py",
           "scripts/_web_print_marks.py", "src/common/browser-print-marks.json",
           "scripts/_browser_products.py", "scripts/_artifact_store.py", "scripts/_document_schema.py",
           "scripts/_print_catalog.py", "scripts/_bible_editions.py", "scripts/_bible_artifacts.py",
           "tools/web-edition",
           "src/common/browser-print-assets.json", "src/common/browser-print-assets-delivery.json",
           "src/common/browser-print-toolchain.toml", "src/common/browser-print-fonts/OFL.txt",
           "src/common/browser-print-fonts/glyph-coverage.json", "src/common/browser-print-fonts/glyph-control-policy.json")


def compiler_paths(root):
    paths = set(HELPERS)
    paths.update(path.relative_to(root).as_posix() for path in (Path(root) / "scripts/_web_print_curriculum").rglob("*.py"))
    return sorted(source_path(path) for path in paths)


def admitted_recipes(root):
    """Enumerate every declared output, then apply its exact release disposition."""
    from _print_document import recipes
    root = Path(root).resolve()
    result = []
    for recipe in recipes(root, family="publication"):
        leaf = root / "src" / recipe["provider"] / recipe["canonical"]
        declaration = tomllib.loads((leaf / "web-edition.toml").read_text())
        release_path = root / "release/publications" / recipe["provider"] / (recipe["document"] + ".json")
        release = json.loads(release_path.read_bytes())
        need(release.get("id") == recipe["document"] and release.get("status") in {"alpha", "hold"}, "publication release identity or disposition is invalid: " + recipe["id"])
        if declaration.get("withdrawn") or release["status"] == "hold":
            continue
        manifest = tomllib.loads((leaf / "publication.toml").read_text())
        need(isinstance(manifest.get("kind"), str) and manifest["kind"], "publication kind is absent: " + recipe["id"])
        result.append({**recipe, "kind": manifest["kind"], "source_paths": [
            (leaf / filename).relative_to(root).as_posix()
            for filename in ("web-edition.toml", "publication.toml")] + [release_path.relative_to(root).as_posix()]})
    result.extend({**recipe, "kind": "bible"} for recipe in recipes(root, family="bible"))
    result.sort(key=lambda row: row["id"])
    need(result and len({row["id"] for row in result}) == len(result), "cold print selection is empty or duplicated")
    return result


def adapter_name(recipe):
    if recipe["family"] == "bible":
        return "bible"
    need(recipe["family"] == "publication", "unowned cold print family")
    kind = recipe["kind"]
    if kind.startswith("curriculum-"):
        return "curriculum"
    if kind in {"server-low-mass", "server-trainer", "server-sung", "server-cards"}:
        return "server"
    if kind == "pictorial-dictionary":
        return "dictionary"
    return "publication"


def global_fonts(root, pool):
    from _web_print_assets import font_assets
    from _web_print_marks import font_asset
    faces = font_assets(root, include_body=True)
    need(len(faces) == 8, "the cold print family requires all eight registered font faces")
    def register(face, license_path):
        face = dict(face)
        license_record = face.pop("license")
        license_id = pool.add(license_record, role="font-license", canonical_path=license_path)
        face["license"] = pool.records[license_id]["asset"]["src"]
        pool.add(face, role="font")
    for face in faces:
        register(face, "src/common/browser-print-fonts/OFL.txt")
    marks = font_asset(root, include_body=True)
    need(marks.get("family") == "Triptych Source Marks" and marks.get("unicode_range") == "U+211F,U+2123,U+21A9,U+2610,U+2720" and
         marks.get("weight") == "400" and marks.get("style") == "normal" and marks.get("mime") == "font/woff2",
         "the source marks font differs from its exact five-glyph contract")
    register(marks, "src/web/browser/shared/fonts/OFL-Junicode.txt")


def render_product(root, recipe, pool, audit_dir):
    """Delegate all source selection and coverage to the publication's owner."""
    name = adapter_name(recipe)
    if name == "bible":
        from _web_print_bibles import render_bible
        return render_bible(root, recipe["id"].removeprefix("bible:"))
    provider, output = recipe["provider"], recipe["document"]
    if name == "curriculum":
        from _web_print_curriculum import render_publication
        return render_publication(root, provider, output)
    if name == "server":
        from _web_print_assets import server_asset
        from _web_print_server import render_server_document
        def resolve(checkout, variant, macro):
            record = server_asset(checkout, variant, macro, include_body=True)
            pool.add(record, role="diagram")
            return record
        return render_server_document(root, provider, output, asset_resolver=resolve)
    if name == "dictionary":
        from _web_print_dictionaries import render_dictionary
        return render_dictionary(root, provider, output)
    from _web_print_assets import generic_assets
    from _web_print_publication import render_publication
    def resolve(checkout, identity, selection):
        records = generic_assets(checkout, identity, selection, include_body=True)
        for record in records:
            pool.add(record, role="diagram")
        return records
    return render_publication(root, provider, output, asset_resolver=resolve, audit_dir=audit_dir)


def generate(root, out):
    """Stream one independently proved product at a time into a fresh JSON tree."""
    from _web_print_publication import require_print_toolchain
    root = Path(root).resolve()
    out = assert_working_output(root, Path(out))
    need(out.is_relative_to(root / ".scratch") or out.is_relative_to(root / "build"), "cold print output must remain under ignored repository output")
    destination = out / PREFIX
    need(not destination.exists(), "cold print preparation requires a fresh output tree")
    require_print_toolchain(root)
    selected = admitted_recipes(root)
    destination.mkdir(parents=True)
    pool = AssetPool(root, destination)
    global_fonts(root, pool)
    records = []
    sources = set(compiler_paths(root))
    scratch = root / ".scratch/web-print-products"
    scratch.mkdir(parents=True, exist_ok=True)
    for recipe in selected:
        with tempfile.TemporaryDirectory(prefix="audit-", dir=scratch) as temporary:
            raw = render_product(root, recipe, pool, Path(temporary))
            assets = {}
            for record in raw.get("assets", ()):
                identity = record.get("id")
                need(isinstance(identity, str) and identity and identity not in assets, "print output repeats a semantic asset ID")
                assets[identity] = pool.add(record)
            prepared = prepare_product(raw, recipe, asset_ids=assets)
            sources.update(prepared["source_paths"])
            filename = "products/" + digest(canonical_json(prepared)) + ".json"
            write_json(destination / filename, prepared)
            records.append({"id": recipe["id"], "path": filename})
            # Detailed source ledgers and converter audits never enter the cache.
            del raw, prepared
        gc.collect()
    sources.update(pool.source_paths)
    catalog = {"schema": CATALOG_SCHEMA, "products": records, "assets": pool.rows(),
               "source_paths": sorted(source_path(path) for path in sources)}
    write_json(destination / "catalog.json", catalog)
    return {"products": len(records), "assets": len(pool.records), "source_paths": len(sources)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path, required=True, help="fresh unsealed browser-data output under .scratch or build")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(generate(args.root, args.out), sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print("web-print-products: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
