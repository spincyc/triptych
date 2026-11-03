"""Complete, source-selected browser-print products for the Latin curriculum.

Products remain generated and unreviewed. The independent source ledger is
checked before a product is returned; the public publisher owns artifact routes
and compact descriptors rather than publishing the detailed audit ledgers.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tomllib

from .core import COURSE, CurriculumError, OFFICIAL_PANDOC_SHA256


def render_curriculum(root: Path, recipe: dict) -> dict:
    """Render one exact declared curriculum output and require complete coverage."""
    root = Path(root).resolve()
    manifest = tomllib.loads((root / recipe["entrypoint"]).with_name("publication.toml").read_text())
    kind = manifest["kind"]
    if kind == "curriculum-packet":
        from .core import render_packet
        product = render_packet(root, recipe)
    elif kind == "curriculum-poetry":
        from .poetry import render_packet
        product = render_packet(root, recipe)
    elif kind == "curriculum-assessment":
        from .assessments import render_assessment
        product = render_assessment(root, recipe)
    elif kind in {"curriculum-guide", "curriculum-reference", "curriculum-memory"}:
        from .companions import render_companion
        product = render_companion(root, recipe)
    else:
        raise CurriculumError("not a declared curriculum print type: " + kind)

    coverage = product.get("coverage_result", {})
    if coverage.get("complete") is not True or coverage.get("status") != "pass":
        raise CurriculumError("curriculum output lacks complete canonical semantic coverage")
    if product.get("render_toolchain", {}).get("sha256") != OFFICIAL_PANDOC_SHA256:
        raise CurriculumError("curriculum output lacks the verified official Pandoc identity")
    if product.get('response_geometry_coverage',{}).get('complete') is not True:
        raise CurriculumError('curriculum output lacks independent response geometry coverage')
    if "semantic_ledger" in product:
        product.setdefault("expected_source_occurrences", product.get("expected_units", []))
        product["expected_units"] = product["semantic_ledger"]["units"]
        if "semantic_selection" in product:
            product.setdefault("selector_digest", product["selection_digest"])
            product["selection_digest"] = product["semantic_selection"]["selection_digest"]

    parts = product["parts"]
    if not parts or len({part["id"] for part in parts}) != len(parts):
        raise CurriculumError("curriculum output requires uniquely identified ordered parts")
    if any(len(part["html"].encode()) >= 750000 for part in parts):
        raise CurriculumError("curriculum part exceeds the shared size contract")
    assembled = "".join(part["html"] for part in parts)
    if hashlib.sha256(assembled.encode()).hexdigest() != product["print_binding"]["output_sha256"]:
        raise CurriculumError("curriculum parts changed the complete source-bound HTML")
    if product["print_binding"]["input_sha256"] != product["html_profile"]["output_sha256"]:
        raise CurriculumError("curriculum binding did not use the complete normalized HTML")
    for part in parts:
        part['html_sha256']=hashlib.sha256(part['html'].encode()).hexdigest()
    from _web_print_publication import unit_expectations
    if "semantic_ledger" in product:
        product["print_unit_expectations"] = unit_expectations(product["semantic_ledger"], product["expected_print_units"])
    if [unit["id"] for unit in product.get("print_unit_expectations", [])] != product["expected_print_units"]:
        raise CurriculumError("print unit provenance differs from canonical DOM occurrence order")
    lock_path=root/"src/common/browser-print-toolchain.toml"
    product["source_paths"][lock_path.relative_to(root).as_posix()] = hashlib.sha256(lock_path.read_bytes()).hexdigest()
    product["canonical_source_digest"] = product["source_digest"]
    product["source_digest"] = hashlib.sha256(json.dumps({"canonical_source_digest":product["source_digest"],
        "toolchain_lock":{"path":lock_path.relative_to(root).as_posix(),"sha256":hashlib.sha256(lock_path.read_bytes()).hexdigest()}},sort_keys=True).encode()).hexdigest()
    product["output_id"] = recipe["id"]
    product["id"] = recipe["id"]
    product["role"] = recipe["edition"]
    product["entrypoint"] = recipe["entrypoint"]
    product["print_type"] = "curriculum"
    product["subtype"] = kind
    return product


def render_publication(root: Path, provider: str, output_id: str) -> dict:
    """Resolve and render one provider-relative or namespaced publication ID."""
    from _print_document import publication_recipe

    root = Path(root).resolve()
    logical = output_id.removeprefix("publication:")
    output = logical.removeprefix(provider + "/")
    recipe = publication_recipe(provider, output, root=root)
    if not recipe["canonical"].startswith(COURSE + "/"):
        raise CurriculumError("publication is outside the canonical curriculum owner")
    return render_curriculum(root, recipe)


def compact_product_metadata(product: dict) -> dict:
    """Small integration metadata; complete ledgers stay in ignored audit output."""
    coverage = product.get("coverage_result", {})
    if coverage.get("complete") is not True or coverage.get("status") != "pass":
        raise CurriculumError("cannot describe an incompletely verified curriculum product")
    profile = product["html_profile"]
    return {
        "output_id": product["output_id"],
        "print_type": product["print_type"],
        "subtype": product.get("subtype", product["print_type"]),
        "title": product["title"],
        "source_digest": product["source_digest"],
        "selection_digest": product["selection_digest"],
        "render_toolchain": product["render_toolchain"],
        "html_profile": {key: profile[key] for key in ("module_sha256", "input_sha256", "output_sha256")},
        "input_style_count": len(profile.get("input_styles", [])),
        "print_binding": product["print_binding"],
        "expected_print_unit_count": len(product["expected_print_units"]),
        "response_geometry_coverage":product['response_geometry_coverage'],
        "status": product.get("status", "generated-unreviewed"),
        "review_status": "generated-unreviewed",
        "coverage_result": {
            key: coverage[key] for key in ("status", "complete", "unit_count", "ledger_digest", "macro_state_digest")
        },
        "parts": [
            {"id": part["id"], "bytes": len(part["html"].encode()),
             "html_sha256": hashlib.sha256(part["html"].encode()).hexdigest()}
            for part in product["parts"]
        ],
        "assets": product.get("assets", []),
    }
