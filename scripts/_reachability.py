#!/usr/bin/env python3
"""Turn catalogue hits into a measured answer about reachable text.

The availability probe answers "does a catalogue return anything under these
names". That is a lead and nothing more: Basil's own search returned a LibriVox
recording and a YouTube video, and Nicholas of Lyra's returned a manuscript
catalogue card. This pass asks the next question, which is the one that decides
acquisition — **is there a text layer, whose is it, and may it be redistributed**
— and answers it from the item's own metadata rather than from its title.

Three states are kept apart, because collapsing them is how an unmeasured work
comes to be counted as an absent one:

- `no-candidate`   nothing the probe returned resembles the work.
- `images-only`    an item exists and carries no machine-readable text layer.
- `text`           a text layer exists, with its byte size and declared rights.

Rights are read per item and never inferred from the author's dates. An item
with no `licenseurl` and no `rights` field is recorded `unresolved`, not free:
`guidance/sources.md` requires an affirmative recorded basis before anything is
tracked, and a successful download is not one.

    python3 scripts/_reachability.py --survey build/sources/genesis-availability.json \\
        --out build/sources/genesis-reachability.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
AGENT = "triptych-source-survey/1.0 (+commentary reachability probe)"


def _fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text or "").lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _words(text: str) -> set[str]:
    return {word for word in _fold(text).split() if len(word) > 3}


def metadata(identifier: str) -> dict[str, Any]:
    url = f"https://archive.org/metadata/{identifier}"
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return json.loads(response.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as error:
        return {"_error": str(error)}


def _rights_of(meta: dict[str, Any]) -> tuple[str, str]:
    licence = str(meta.get("licenseurl") or "")
    rights = str(meta.get("rights") or "")
    if "publicdomain" in licence:
        return "public-domain", licence
    if "creativecommons" in licence:
        return "creative-commons", licence
    if rights:
        return "stated", rights
    # No affirmative basis. Not the same as "in copyright", and not the same as
    # free: it is unresolved, and unresolved forbids tracking.
    return "unresolved", ""


def inspect(identifier: str, aliases: set[str]) -> dict[str, Any]:
    payload = metadata(identifier)
    if "_error" in payload:
        return {"identifier": identifier, "state": "error", "detail": payload["_error"]}
    meta = payload.get("metadata", {})
    title = str(meta.get("title") or "")
    texts = [
        {"name": f["name"], "size": int(f.get("size") or 0)}
        for f in payload.get("files", [])
        if f["name"].endswith("_djvu.txt")
    ]
    status, basis = _rights_of(meta)
    overlap = len(_words(title) & aliases)
    return {
        "identifier": identifier,
        "title": title[:160],
        "year": meta.get("year") or meta.get("date"),
        "language": meta.get("language"),
        "alias_word_overlap": overlap,
        "rights": status,
        "rights_basis": basis,
        "state": "text" if texts else "images-only",
        "text_files": texts,
        "text_bytes": max((t["size"] for t in texts), default=0),
    }


def survey_group(group: dict[str, Any], limit: int) -> dict[str, Any]:
    aliases: set[str] = set()
    for name in group.get("aliases_tried") or []:
        aliases |= _words(name)

    candidates = group.get("internet_archive") or []
    ranked = sorted(
        (doc for doc in candidates if doc.get("identifier")),
        key=lambda doc: -len(_words(str(doc.get("title") or "")) & aliases),
    )[:limit]

    with ThreadPoolExecutor(max_workers=6) as pool:
        items = list(
            pool.map(lambda doc: inspect(str(doc["identifier"]), aliases), ranked)
        )

    with_text = [item for item in items if item.get("state") == "text"]
    redistributable = [
        item for item in with_text if item.get("rights") in {"public-domain", "creative-commons"}
    ]
    if not items:
        state = "no-candidate"
    elif with_text:
        state = "text"
    else:
        state = "images-only"

    return {
        "id": group["id"],
        "canonical": group.get("canonical"),
        "aliases_tried": len(group.get("aliases_tried") or []),
        "candidates_examined": len(items),
        "state": state,
        "items_with_text": len(with_text),
        "items_redistributable": len(redistributable),
        "wikisource_hits": len(group.get("wikisource") or []),
        "gutenberg_hits": len(group.get("gutenberg") or []),
        "items": items,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--survey", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--limit", type=int, default=8, help="candidates examined per group")
    parser.add_argument("--groups", type=int, default=4)
    arguments = parser.parse_args(argv)

    groups = json.loads(Path(arguments.survey).read_text(encoding="utf-8"))
    out = Path(arguments.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    done: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=arguments.groups) as pool:
        for index, result in enumerate(
            pool.map(lambda g: survey_group(g, arguments.limit), groups), 1
        ):
            print(
                f"{index}/{len(groups)} {result['id']}: {result['state']} "
                f"text={result['items_with_text']} free={result['items_redistributable']}",
                file=sys.stderr,
                flush=True,
            )
            done.append(result)
            out.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
