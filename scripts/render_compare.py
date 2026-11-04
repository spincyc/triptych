#!/usr/bin/env python3
"""Prove a structural migration renders the same: snapshot, migrate, compare.

Moving a leaf onto a document type (``tools/tpt document-types``) changes its
entrypoints and may move text between files; the PDF a reader gets must not
change except where the migration intends it. This helper makes that a
two-command check that any lane can reuse:

    scripts/render_compare.py snapshot --leaf claude/<document> --out DIR/before
    ... migrate ...
    scripts/render_compare.py snapshot --leaf claude/<document> --out DIR/after
    scripts/render_compare.py compare DIR/before DIR/after [--expect HEADING]

``snapshot`` builds every edition the leaf's ``publication.toml`` declares
with ``tools/print-document build`` (host toolchain) and keeps, per edition,
the PDF, its page count and its per-page text. ``compare`` reports, per
edition, the page counts, every text difference outside pages that carry an
``--expect`` heading (a migration's intended change, such as a regenerated
page; page-number-only lines are ignored), and a raster comparison of pages
whose text is unchanged. Exit status 1 means an unexpected difference.

Nothing here is tracked output; snapshots belong under ``.scratch/``.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITIONS = {"canonical": "main", "synthesis": "synthesis", "homily": "homily"}
PAGE_NUMBER = re.compile(r"\A\s*[0-9ivxlc]+\s*\Z")


def _run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    run = subprocess.run(command, capture_output=True, text=True, **kwargs)
    if run.returncode:
        raise SystemExit(f"{' '.join(command[:4])} ... failed ({run.returncode}):\n"
                         + (run.stderr or run.stdout)[-3000:])
    return run


def editions(leaf: str) -> list[str]:
    # The outputs are derived from the leaf's records, not spelled in its
    # publication.toml; the schema loader is their one reader.
    sys.path.insert(0, str(ROOT / "scripts"))
    import _document_schema  # noqa: PLC0415

    provider, _, document = leaf.partition("/")
    data = _document_schema.load_manifest(ROOT, ROOT / "src" / provider / document / "publication.toml")
    return [EDITIONS[item["role"]] for item in data.get("outputs", []) if item.get("role") in EDITIONS]


def page_texts(pdf: Path) -> list[str]:
    text = _run(["pdftotext", "-layout", str(pdf), "-"]).stdout
    pages = text.split("\f")
    return pages[:-1] if pages and not pages[-1].strip() else pages


def snapshot(leaf: str, out: Path, selected: list[str] | None = None) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    report = {}
    for edition in selected or editions(leaf):
        work = Path(tempfile.mkdtemp(dir=out, prefix=f".{edition}-"))
        try:
            _run([str(ROOT / "tools/print-document"), "build", "--document", f"publication:{leaf}",
                  "--edition", edition, "--out", str(work)], cwd=ROOT)
            built = sorted(work.glob("*.pdf"))
            if len(built) != 1:
                raise SystemExit(f"{leaf} {edition}: expected one PDF in {work}")
            target = out / f"{edition}.pdf"
            shutil.copyfile(built[0], target)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        pages = page_texts(target)
        (out / f"{edition}.pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=0))
        report[edition] = len(pages)
    (out / "snapshot.json").write_text(json.dumps({"leaf": leaf, "pages": report}, indent=1))
    return report


def _normal(page: str) -> list[str]:
    return [" ".join(line.split()) for line in page.splitlines()
            if line.strip() and not PAGE_NUMBER.match(line)]


def _expected(page: str, headings: list[str]) -> bool:
    head = " ".join(" ".join(page.split()).split()[:40])
    return any(heading in head for heading in headings)


# Two rasters of the same typeset page can differ by a few antialiased pixels
# when the PDF's font subsets differ (a page elsewhere added glyphs). A page is
# reported different only when more than this many pixels change by more than
# a quarter of the grey range at 50 dpi -- a moved word changes hundreds.
RASTER_TOLERANCE = 40


def _raster(pdf: Path, page: int, scratch: Path) -> bytes:
    prefix = scratch / f"p{page}-{hashlib.sha256(str(pdf).encode()).hexdigest()[:8]}"
    _run(["pdftoppm", "-r", "50", "-gray", "-f", str(page), "-l", str(page), str(pdf), str(prefix)])
    image = next(scratch.glob(prefix.name + "*"))
    data = image.read_bytes()
    image.unlink()
    return data


def _same_raster(first: bytes, second: bytes) -> bool:
    if len(first) != len(second):
        return False
    changed = sum(1 for a, b in zip(first, second) if abs(a - b) > 64)
    return changed <= RASTER_TOLERANCE


def compare(before: Path, after: Path, headings: list[str], raster: int) -> dict:
    result: dict[str, dict] = {}
    for pages_file in sorted(before.glob("*.pages.json")):
        edition = pages_file.name.removesuffix(".pages.json")
        other = after / pages_file.name
        if not other.is_file():
            result[edition] = {"error": "missing after snapshot"}
            continue
        old = json.loads(pages_file.read_text())
        new = json.loads(other.read_text())
        old_kept = [(index, page) for index, page in enumerate(old, 1) if not _expected(page, headings)]
        new_kept = [(index, page) for index, page in enumerate(new, 1) if not _expected(page, headings)]
        old_lines = [line for _, page in old_kept for line in _normal(page)]
        new_lines = [line for _, page in new_kept for line in _normal(page)]
        diff = list(difflib.unified_diff(old_lines, new_lines, "before", "after", lineterm="", n=1))
        same_text = {}
        new_index = {tuple(_normal(page)): index for index, page in new_kept}
        for index, page in old_kept:
            match = new_index.get(tuple(_normal(page)))
            if match is not None:
                same_text[index] = match
        rasters = {"compared": 0, "identical": 0, "different": []}
        with tempfile.TemporaryDirectory() as scratch:
            for index, match in list(same_text.items())[:raster]:
                rasters["compared"] += 1
                if _same_raster(_raster(before / f"{edition}.pdf", index, Path(scratch)),
                                _raster(after / f"{edition}.pdf", match, Path(scratch))):
                    rasters["identical"] += 1
                else:
                    rasters["different"].append([index, match])
        result[edition] = {
            "pages": [len(old), len(new)],
            "expected_pages": [[i for i, p in enumerate(old, 1) if _expected(p, headings)],
                               [i for i, p in enumerate(new, 1) if _expected(p, headings)]],
            "text_differences": diff[2:],
            "raster": rasters,
        }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    shot = sub.add_parser("snapshot", help="build and record every edition of one leaf")
    shot.add_argument("--leaf", required=True, help="<provider>/<document>")
    shot.add_argument("--out", required=True, type=Path)
    shot.add_argument("--edition", action="append", help="limit to these editions")
    diff = sub.add_parser("compare", help="compare two snapshots of one leaf")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    diff.add_argument("--expect", action="append", default=[],
                      help="a heading whose pages are an intended change (repeatable)")
    diff.add_argument("--raster", type=int, default=6, help="text-identical pages to raster-compare")
    diff.add_argument("--json", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.command == "snapshot":
        print(json.dumps(snapshot(arguments.leaf, arguments.out, arguments.edition)))
        return 0
    report = compare(arguments.before, arguments.after, arguments.expect, arguments.raster)
    if arguments.json:
        print(json.dumps(report, indent=1, ensure_ascii=False))
    else:
        for edition, found in report.items():
            if "error" in found:
                print(f"{edition}: {found['error']}")
                continue
            raster = found["raster"]
            print(f"{edition}: pages {found['pages'][0]} -> {found['pages'][1]}; "
                  f"expected-change pages {found['expected_pages'][0]} -> {found['expected_pages'][1]}; "
                  f"{len(found['text_differences'])} text diff lines; raster "
                  f"{raster['identical']}/{raster['compared']} identical")
            for line in found["text_differences"][:60]:
                print("    " + line)
    unexpected = any("error" in found or found["text_differences"] or found["raster"]["different"]
                     for found in report.values())
    return 1 if unexpected else 0


if __name__ == "__main__":
    sys.exit(main())
