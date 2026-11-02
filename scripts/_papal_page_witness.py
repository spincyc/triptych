"""Extract explicitly selected native PDF witnesses; never infer rights or review.

The project-created Pii IX Acta extraction recipe is an immutable replay witness.
Its native bilevel packaging is generalized here; future callers use this module.
Native page extraction uses Poppler and may produce different trailer IDs on a
replay. Exact registered bytes are immutable; image parity is not byte identity.
Native-page copying can retain document metadata; caller rights evidence must
cover the selected output, not merely the age of its underlying printing.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import tomllib
import zlib

SCHEMA = "triptych-papal-page-witness/v1"
RECEIPT_SCHEMA = "triptych-papal-page-witness-receipt/v1"
SAFE = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
HASH = re.compile(r"^[0-9a-f]{64}$")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def run(arguments: list[str]) -> bytes:
    result = subprocess.run(arguments, capture_output=True, check=False)
    if result.returncode:
        raise ValueError(f"{Path(arguments[0]).name} failed: " + result.stderr.decode(errors="replace")[:500])
    return result.stdout


def repo_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError("source record paths must be repository-relative")
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError("source record path escapes repository")
    return path


def preflight(root: Path, recipe: dict, cached_pdf: Path, scratch: Path) -> dict:
    root = root.resolve()
    scratch = scratch.resolve()
    if not scratch.is_relative_to(root / ".scratch"):
        raise ValueError("scratch must be beneath repository .scratch")
    if not isinstance(recipe, dict) or recipe.get("schema") != SCHEMA:
        raise ValueError("expected " + SCHEMA)
    stamp = recipe.get("revision", "")
    if not isinstance(stamp, str) or not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", stamp):
        raise ValueError("recipe requires an explicit UTC revision")
    dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    for key in ("slug", "parent_artifact_id", "edition_id"):
        if not SAFE.fullmatch(str(recipe.get(key, ""))):
            raise ValueError("invalid " + key)
    for key in ("title", "rights_basis", "rights_jurisdiction", "extent_note"):
        if not isinstance(recipe.get(key), str) or not recipe[key].strip():
            raise ValueError("caller must supply " + key)
    if recipe.get("rights_status") not in {"public-domain", "licensed"}:
        raise ValueError("affirmative caller-supplied rights assessment required")
    pages = recipe.get("pages")
    if (not isinstance(pages, list) or not pages or any(type(n) is not int or n < 1 for n in pages)
            or pages != sorted(set(pages))):
        raise ValueError("pages must be explicit increasing unique one-based integers")
    method = recipe.get("method", "native-pages")
    if method not in {"native-pages", "native-bilevel-images"}:
        raise ValueError("unknown extraction method")
    parent_path = repo_path(root, recipe.get("parent_artifact_path"))
    source_root = root / "src/sources/works"
    if (not parent_path.is_relative_to(source_root) or parent_path.name != "artifact.toml"
            or parent_path.parents[1].name != "artifacts"):
        raise ValueError("parent must be an existing canonical artifact record")
    parent = tomllib.loads(parent_path.read_text())
    edition_dir = parent_path.parents[2]
    edition = tomllib.loads((edition_dir / "edition.toml").read_text())
    if parent.get("id") != recipe["parent_artifact_id"] or parent.get("media_type") != "application/pdf":
        raise ValueError("parent is not the declared canonical PDF artifact")
    if parent.get("edition_id") != recipe["edition_id"] or edition.get("id") != recipe["edition_id"]:
        raise ValueError("same-edition parent ownership required")
    if (not HASH.fullmatch(str(recipe.get("parent_sha256", ""))) or type(recipe.get("parent_byte_size")) is not int
            or recipe["parent_byte_size"] <= 0 or parent.get("sha256") != recipe["parent_sha256"]
            or parent.get("byte_size") != recipe["parent_byte_size"]):
        raise ValueError("recipe must pin the complete canonical parent hash and size")
    cached_pdf = cached_pdf.resolve()
    if not cached_pdf.is_relative_to(root / ".scratch") and cached_pdf != repo_path(root, parent.get("path", "")):
        raise ValueError("cached PDF must be in .scratch or the exact tracked parent")
    payload = cached_pdf.read_bytes()
    if len(payload) != parent["byte_size"] or digest(payload) != parent["sha256"] or not payload.startswith(b"%PDF-"):
        raise ValueError("whole cached PDF does not match canonical parent")
    if method == "native-bilevel-images":
        selectors = recipe.get("image_selectors")
        if (not isinstance(selectors, list) or any(not isinstance(s, dict) for s in selectors)
                or [s.get("page") for s in selectors] != pages):
            raise ValueError("explicit native image selector required for every page")
        for selector in selectors:
            if (any(type(selector.get(k)) is not int or selector[k] < 1 for k in ("width", "height", "dpi"))
                    or type(selector.get("ordinal")) is not int or selector["ordinal"] < 0
                    or not HASH.fullmatch(str(selector.get("pixel_sha256", "")))):
                raise ValueError("image selectors require exact dimensions, ordinal, dpi and pixel hash")
    return {"root": root, "scratch": scratch, "parent": parent, "edition_dir": edition_dir,
            "cached_pdf": cached_pdf, "method": method}


def pdf_information(path: Path, page: int | None = None) -> dict:
    args = ["pdfinfo"] + (["-f", str(page), "-l", str(page), "-box"] if page else []) + [str(path)]
    text = run(args).decode()
    count = re.search(r"^Pages:\s+(\d+)\s*$", text, re.M)
    if not count or not re.search(r"^Encrypted:\s+no\b", text, re.M):
        raise ValueError("expected a readable unencrypted PDF")
    geometry = [re.sub(r"^Page\s+\d+\s+", "Page ", line).strip()
                for line in text.splitlines() if re.match(r"^Page\s+\d+\s+(?:size|rot|\w+Box):", line)]
    return {"pages": int(count[1]), "geometry": geometry}


def image_listing(path: Path, page: int) -> list[dict]:
    text = run(["pdfimages", "-f", str(page), "-l", str(page), "-list", str(path)]).decode()
    rows = []
    for line in text.splitlines():
        fields = line.split()
        if len(fields) >= 16 and fields[0].isdigit():
            rows.append({"ordinal": int(fields[1]), "type": fields[2], "width": int(fields[3]),
                         "height": int(fields[4]), "color": fields[5], "components": int(fields[6]),
                         "bpc": int(fields[7]), "encoding": fields[8], "interpolate": fields[9]})
    return rows


def image_snapshot(path: Path, page: int, temporary: Path) -> dict:
    temporary.mkdir()
    prefix = temporary / "image"
    run(["pdfimages", "-f", str(page), "-l", str(page), "-all", str(path), str(prefix)])
    files = [{"file": p.name, "sha256": digest(p.read_bytes()), "byte_size": p.stat().st_size}
             for p in sorted(temporary.iterdir())]
    return {"images": image_listing(path, page), "native_streams": files}


def bilevel_pixels(path: Path, page: int, selector: dict, temporary: Path) -> bytes:
    images = image_listing(path, page)
    matches = [i for i in images if i["ordinal"] == selector["ordinal"]]
    if len(matches) != 1 or any(matches[0][k] != selector[k] for k in ("width", "height")) or matches[0]["bpc"] != 1 or matches[0]["type"] != "image":
        raise ValueError("native bilevel image does not match explicit selector")
    temporary.mkdir()
    prefix = temporary / "image"
    run(["pdfimages", "-f", str(page), "-l", str(page), "-j", str(path), str(prefix)])
    payload = (temporary / f"image-{selector['ordinal']:03}.pbm").read_bytes()
    header = re.match(br"P4\s+(\d+)\s+(\d+)\n", payload)
    if not header or tuple(map(int, header.groups())) != (selector["width"], selector["height"]):
        raise ValueError("unexpected native PBM header")
    bits = payload[header.end():]
    if len(bits) != ((selector["width"] + 7) // 8) * selector["height"] or digest(bits) != selector["pixel_sha256"]:
        raise ValueError("native image pixel hash or size differs from caller pin")
    return bits


def bilevel_pdf(images: list[tuple[dict, bytes]]) -> bytes:
    """Lossless native-bit packaging generalized from immutable Quanta recipe."""
    objects = [b"", b"<< /Type /Catalog /Pages 2 0 R >>", b""]
    kids = []
    for selector, pixels in images:
        width, height = selector["width"], selector["height"]
        wp, hp = width * 72 / selector["dpi"], height * 72 / selector["dpi"]
        page_id, image_id, content_id = len(objects), len(objects)+1, len(objects)+2
        kids.append(f"{page_id} 0 R")
        objects.append((f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {wp:.4f} {hp:.4f}] /Resources << /XObject << /Im0 {image_id} 0 R >> >> /Contents {content_id} 0 R >>").encode())
        data = zlib.compress(pixels, level=9)
        objects.append((f"<< /Type /XObject /Subtype /Image /Width {width} /Height {height} /ColorSpace /DeviceGray /BitsPerComponent 1 /Decode [1 0] /Filter /FlateDecode /Length {len(data)} >>\nstream\n").encode()+data+b"\nendstream")
        content = f"q {wp:.4f} 0 0 {hp:.4f} 0 0 cm /Im0 Do Q\n".encode()
        objects.append(f"<< /Length {len(content)} >>\nstream\n".encode()+content+b"endstream")
    objects[2] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(images)} >>".encode()
    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for ordinal, obj in enumerate(objects[1:], 1):
        offsets.append(len(output))
        output += f"{ordinal} 0 obj\n".encode()+obj+b"\nendobj\n"
    xref = len(output)
    output += f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode()
    for offset in offsets[1:]:
        output += f"{offset:010} 00000 n \n".encode()
    output += f"trailer\n<< /Size {len(objects)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(output)


def validate_receipt(recipe: dict, receipt: dict, output: Path) -> None:
    """Bind reused bytes and mechanical facts to the exact immutable recipe."""
    expected = {"schema": RECEIPT_SCHEMA, "revision": recipe["revision"],
                "parent_artifact_id": recipe["parent_artifact_id"], "parent_sha256": recipe["parent_sha256"],
                "parent_byte_size": recipe["parent_byte_size"], "recipe_sha256": digest(json_bytes(recipe)),
                "method": recipe.get("method", "native-pages"), "pages": recipe["pages"], "page_count": len(recipe["pages"]),
                "rights_assessment": "caller-supplied; not inferred by extraction",
                "source_review": "not assessed; no passage or verified status created",
                "visual_review": "not performed; use pdf-review separately"}
    if not isinstance(receipt, dict) or any(receipt.get(k) != v for k, v in expected.items()):
        raise ValueError("receipt does not bind the exact recipe, parent, method and pages")
    payload = output.read_bytes()
    if (digest(payload) != receipt.get("output_sha256") or len(payload) != receipt.get("output_byte_size")
            or pdf_information(output)["pages"] != len(recipe["pages"])):
        raise ValueError("receipt output hash, size or actual page count mismatch")
    checks = receipt.get("checks")
    if (not isinstance(checks, list) or len(checks) != len(recipe["pages"])
            or any(not isinstance(c, dict) or c.get("source_page") != original or c.get("output_page") != target
                   for target, (original, c) in enumerate(zip(recipe["pages"], checks), 1))):
        raise ValueError("receipt mechanical check page mapping differs from recipe")


def mechanical_checks(recipe: dict, source: Path, output: Path, temporary: Path, images=None) -> list[dict]:
    """Recompute parent-to-output parity; staged receipts are never authority."""
    if pdf_information(output)["pages"] != len(recipe["pages"]):
        raise ValueError("output page count mismatch")
    checks = []
    if recipe.get("method", "native-pages") == "native-pages":
        for target, original in enumerate(recipe["pages"], 1):
            before = pdf_information(source, original)["geometry"]
            after = pdf_information(output, target)["geometry"]
            text = lambda p, n: run(["pdftotext", "-f", str(n), "-l", str(n), "-layout", str(p), "-"])
            old_text, new_text = text(source, original), text(output, target)
            old_images = image_snapshot(source, original, temporary/f"old-{target}")
            new_images = image_snapshot(output, target, temporary/f"new-{target}")
            if not before or before != after or old_text != new_text or old_images != new_images:
                raise ValueError("native page geometry, text or image parity failed against pinned parent")
            checks.append({"source_page": original, "output_page": target, "geometry": before,
                           "text_sha256": digest(old_text), "native_images": old_images})
    else:
        if images is None:
            images = [(s, bilevel_pixels(source, s["page"], s, temporary/f"bits-{s['page']}")) for s in recipe["image_selectors"]]
        # This backend has a deterministic minimal container. Exact reconstruction
        # also excludes added text, vector objects or wrapper content hidden
        # beside otherwise matching historical image bits.
        if output.read_bytes() != bilevel_pdf(images):
            raise ValueError("bilevel output differs from pinned parent images and packaging")
        for target, (selector, _) in enumerate(images, 1):
            bilevel_pixels(output, target, dict(selector, ordinal=0), temporary/f"out-bits-{target}")
            checks.append({"source_page": selector["page"], "output_page": target,
                           "selector": selector, "native_pixel_parity": "pass"})
    return checks


def extract_witness(root: Path, recipe: dict, cached_pdf: Path, scratch: Path) -> dict:
    context = preflight(root, recipe, cached_pdf, scratch)
    scratch = context["scratch"]
    scratch.mkdir(parents=True, exist_ok=True)
    source = context["cached_pdf"]
    info = pdf_information(source)
    if context["parent"].get("page_count", info["pages"]) != info["pages"]:
        raise ValueError("canonical parent page count does not match whole PDF")
    if recipe["pages"][-1] > info["pages"]:
        raise ValueError("selected native page exceeds complete parent PDF")
    stage = scratch / recipe["slug"]
    encoded_recipe = json_bytes(recipe)
    if stage.exists():
        if (stage / "recipe.json").read_bytes() != encoded_recipe:
            raise ValueError("staging recipe collision; use a new slug")
        receipt = json.loads((stage / "receipt.json").read_text())
        validate_receipt(recipe, receipt, stage / "witness.pdf")
        with tempfile.TemporaryDirectory(prefix="recheck-stage-", dir=scratch) as temporary:
            observed = mechanical_checks(recipe, source, stage/"witness.pdf", Path(temporary))
        if observed != receipt["checks"]:
            raise ValueError("staged receipt checks differ from independently recomputed parent parity")
        return {"stage": stage, "receipt": receipt, "context": context, "reused": True}
    with tempfile.TemporaryDirectory(prefix="native-pages-", dir=scratch) as temporary:
        temp = Path(temporary)
        output = temp / "witness.pdf"
        images = None
        if context["method"] == "native-pages":
            parts = []
            for n in recipe["pages"]:
                part = temp / f"page-{n}.pdf"
                run(["pdfseparate", "-f", str(n), "-l", str(n), str(source), str(part)])
                parts.append(part)
            if len(parts) == 1:
                shutil.copyfile(parts[0], output)
            else:
                run(["pdfunite", *map(str, parts), str(output)])
        else:
            images = [(s, bilevel_pixels(source, s["page"], s, temp/f"bits-{s['page']}")) for s in recipe["image_selectors"]]
            output.write_bytes(bilevel_pdf(images))
        checks = mechanical_checks(recipe, source, output, temp, images)
        payload = output.read_bytes()
        receipt = {"schema": RECEIPT_SCHEMA, "revision": recipe["revision"], "parent_artifact_id": recipe["parent_artifact_id"],
                   "parent_sha256": recipe["parent_sha256"], "parent_byte_size": recipe["parent_byte_size"],
                   "recipe_sha256": digest(encoded_recipe), "method": context["method"], "pages": recipe["pages"],
                   "output_sha256": digest(payload), "output_byte_size": len(payload), "page_count": len(recipe["pages"]),
                   "implementation": {"path": "scripts/_papal_page_witness.py", "sha256": digest(Path(__file__).read_bytes())},
                   "tools": {},
                   "checks": checks, "rights_assessment": "caller-supplied; not inferred by extraction",
                   "source_review": "not assessed; no passage or verified status created",
                   "visual_review": "not performed; use pdf-review separately",
                   "replay_limit": "Poppler native-page extraction can change trailer IDs. Exact output hashes identify retained bytes; mechanical content parity does not promise byte-identical replay."}
        for tool in ("pdfseparate", "pdfunite", "pdfimages", "pdfinfo", "pdftotext"):
            version = subprocess.run([tool, "-v"], capture_output=True, check=True)
            receipt["tools"][tool] = (version.stdout+version.stderr).decode().splitlines()[0]
        validate_receipt(recipe, receipt, output)
        stage.mkdir()
        (stage / "recipe.json").write_bytes(encoded_recipe)
        (stage / "witness.pdf").write_bytes(payload)
        (stage / "receipt.json").write_bytes(json_bytes(receipt))
    return {"stage": stage, "receipt": receipt, "context": context, "reused": False}


def artifact_bundle(root: Path, edition_dir: Path, recipe: dict, payloads: list[bytes]) -> list[tuple]:
    """One record contract is used for creation and exact immutable reuse."""
    if len(payloads) != 3:
        raise ValueError("witness bundle requires PDF, recipe and receipt")
    slug = recipe["slug"]
    base = "artifact." + recipe["edition_id"].removeprefix("edition.") + "."
    targets = [(slug, "witness.pdf"), (slug+"-recipe", "recipe.json"), (slug+"-receipt", "receipt.json")]
    result = []
    for n, ((name, filename), payload) in enumerate(zip(targets, payloads)):
        directory = edition_dir/"artifacts"/name
        project = n != 0
        record = {"schema": 2, "record_type": "artifact", "id": base+name, "edition_id": recipe["edition_id"],
                  "artifact_type": ["bounded-native-page-witness", "project-created-extraction-recipe", "project-created-extraction-receipt"][n],
                  "media_type": "application/json" if project else "application/pdf", "storage": "tracked",
                  "rights_status": "project-created" if project else recipe["rights_status"],
                  "rights_basis": "Project-created mechanical extraction metadata; no rights in source material are granted." if project else recipe["rights_basis"],
                  "retrieved": recipe["revision"][:10], "sha256": digest(payload), "byte_size": len(payload),
                  "path": str((directory/filename).relative_to(root.resolve())), "indexable": False}
        if n == 0:
            record.update({"rights_jurisdiction": recipe["rights_jurisdiction"], "page_count": len(recipe["pages"]),
                           "derived_from": recipe["parent_artifact_id"], "transformation": recipe.get("method", "native-pages")+": explicit native PDF pages "+str(recipe["pages"])+". "+recipe["extent_note"],
                           "provenance": "Fresh extraction from the pinned whole parent; prior staging bytes are not promoted. Mechanical checks establish neither source wording accuracy nor legal clearance. Recipe and final extraction receipt are separately retained."})
        else:
            record["provenance"] = "Immutable mechanical recipe/receipt; source review and caller rights assessment remain separate. The receipt pins the exact implementation hash and tool versions."
        result.append((directory, filename, payload, record))
    return result


def register_witness(root: Path, recipe: dict, cached_pdf: Path, scratch: Path) -> dict:
    """Register only NEW immutable derivatives under the parent's own edition."""
    from _papal_sources import write_record
    context = preflight(root, recipe, cached_pdf, scratch)
    edition_dir, slug = context["edition_dir"], recipe["slug"]
    directories = [edition_dir/"artifacts"/name for name in (slug, slug+"-recipe", slug+"-receipt")]
    if any(p.exists() for p in directories):
        files = [p/name for p, name in zip(directories, ("witness.pdf", "recipe.json", "receipt.json"))]
        held = [p.read_bytes() for p in files]
        if held[1] != json_bytes(recipe):
            raise ValueError("registered witness recipe collision; use a new slug")
        receipt = json.loads(held[2])
        validate_receipt(recipe, receipt, files[0])
        records = artifact_bundle(root, edition_dir, recipe, held)
        for directory, _, _, expected in records:
            if tomllib.loads((directory/"artifact.toml").read_text()) != expected:
                raise ValueError("registered immutable witness recipe collision or record contract mismatch")
        return {"status": "reused", "artifact_ids": [r[3]["id"] for r in records], "receipt": receipt,
                "registration_source": "immutable-canonical-reuse"}
    scratch = context["scratch"]
    scratch.mkdir(parents=True, exist_ok=True)
    staged_hash = None
    if (scratch/slug).exists():
        staged = extract_witness(root, recipe, cached_pdf, scratch)
        staged_hash = staged["receipt"]["output_sha256"]
    # Geometry/text/images cannot prove the absence of extra vector graphics.
    # Never promote a caller-mutable staged PDF. Build every new canonical
    # witness directly from the pinned parent in a private empty directory.
    with tempfile.TemporaryDirectory(prefix="register-from-parent-", dir=scratch) as temporary:
        extracted = extract_witness(root, recipe, cached_pdf, Path(temporary))
        payloads = [(extracted["stage"]/name).read_bytes() for name in ("witness.pdf", "recipe.json", "receipt.json")]
        validate_receipt(recipe, extracted["receipt"], extracted["stage"]/"witness.pdf")
    for path in sorted((edition_dir/"artifacts").glob("*/artifact.toml")):
        held = tomllib.loads(path.read_text())
        if held.get("media_type") == "application/pdf" and held.get("sha256") == digest(payloads[0]):
            raise ValueError("identical derived PDF already has canonical owner: " + held["id"])
    records = artifact_bundle(root, edition_dir, recipe, payloads)
    for directory, filename, payload, record in records:
        directory.mkdir(parents=True)
        (directory/filename).write_bytes(payload)
        write_record(directory/"artifact.toml", record)
    result = {"status": "registered", "artifact_ids": [r[3]["id"] for r in records], "receipt": extracted["receipt"],
              "registration_source": "fresh-pinned-parent-extraction"}
    if staged_hash:
        result["staged_output_sha256"] = staged_hash
    return result
