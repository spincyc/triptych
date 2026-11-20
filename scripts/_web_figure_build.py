"""Prepare web-edition figures from a held, verified browser-product snapshot."""
from __future__ import annotations

import json
from pathlib import Path

import _web_edition_figures as figures


def prepare(root: Path, products, out: Path, *, runner: str, candidates: Path | None = None,
            force: bool = False) -> dict:
    try:
        index = json.loads(products.files["web-editions/index.json"].read_bytes())
        if index.get("schema") != "triptych-web-editions/v1":
            raise figures.FigureError("unsupported web-edition product index")
        records = []
        for row in index["editions"]:
            if row["figures"]:
                edition = json.loads(products.files[row["path"]].read_bytes())
                records.extend(edition["figures"])
    except KeyError as error:
        raise figures.FigureError(f"web-edition products are not available: {error}") from error

    wanted = {record["id"] for record in records}
    if candidates is None and not force and not figures.check(out, wanted):
        return {"figures": len(wanted), "out": str(out), "status": "current"}
    manifest = figures.compile_figures(records, out, root=root, runner=runner, candidates=candidates, force=force)
    return {"figures": len(manifest["figures"]), "out": str(out), "toolchain": manifest["toolchain"]}
