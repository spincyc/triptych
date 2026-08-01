#!/usr/bin/env python3
"""Probe the public catalogues for each commentary, under every name it carries.

`guidance/sources.md` makes alias resolution policy, and policy that is not
executed is decoration. This probe drives its queries from
`src/sources/commentary/genesis-work-aliases.yaml` and from nothing else, so a
name that file does not carry was not tried, and the survey it writes says which
names were.

Nothing here consults a model. It calls four public catalogue APIs over HTTPS,
records what each returned, and stops. It retrieves no source text: a catalogue
answer is a lead, and the byte-level retrieval that turns a lead into an
artifact is a separate act performed by `curl` and hashed on arrival. That
separation is the whole reason this file exists rather than a prompt.

    python3 scripts/_availability.py --out build/sources/genesis-availability.json

The output is a build product and is not tracked. What is tracked is the survey
conclusion a human draws from it, in
`src/sources/commentary/genesis-availability.yaml`, because a catalogue hit is
not a holding, a holding is not a licence, and a licence is not a text.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ALIASES = ROOT / "src/sources/commentary/genesis-work-aliases.yaml"
AGENT = "triptych-source-survey/1.0 (+https://github.com/; commentary availability probe)"
PAUSE = 0.34


def _get(url: str, timeout: int = 45) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _json(url: str) -> Any:
    try:
        return json.loads(_get(url))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as error:
        return {"_error": str(error)}


def internet_archive(query: str, rows: int = 8) -> list[dict[str, Any]]:
    """Items whose metadata matches, with the rights statement each declares.

    `licenseurl` and `rights` are asked for by name because a successful
    download is not a licence: an item with neither is unresolved, not free.
    """
    fields = ["identifier", "title", "creator", "year", "licenseurl", "rights", "language"]
    params = urllib.parse.urlencode(
        [("q", query), ("rows", str(rows)), ("page", "1"), ("output", "json")]
        + [("fl[]", field) for field in fields]
    )
    payload = _json(f"https://archive.org/advancedsearch.php?{params}")
    if "_error" in payload:
        return [{"_error": payload["_error"]}]
    return payload.get("response", {}).get("docs", [])


def wikisource(term: str, language: str = "en", limit: int = 6) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "list": "search",
            "srsearch": term,
            "srlimit": str(limit),
            "format": "json",
            "formatversion": "2",
        }
    )
    payload = _json(f"https://{language}.wikisource.org/w/api.php?{params}")
    if "_error" in payload:
        return [{"_error": payload["_error"]}]
    return [
        {"title": hit.get("title"), "size": hit.get("size"), "wiki": f"{language}.wikisource"}
        for hit in payload.get("query", {}).get("search", [])
    ]


def gutenberg(term: str) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"search": term})
    payload = _json(f"https://gutendex.com/books?{params}")
    if "_error" in payload:
        return [{"_error": payload["_error"]}]
    return [
        {
            "id": book.get("id"),
            "title": book.get("title"),
            "authors": [person.get("name") for person in book.get("authors", [])],
            "languages": book.get("languages"),
        }
        for book in payload.get("results", [])[:6]
    ]


def _terms(group: dict[str, Any]) -> list[tuple[str, str]]:
    """Every (author, title) pair the group declares. Both halves, not one."""
    authors = list(dict.fromkeys(group.get("author_aliases") or []))
    titles = list(dict.fromkeys(group.get("title_aliases") or []))
    pairs: list[tuple[str, str]] = []
    for author in authors[:4]:
        for title in titles[:4]:
            pairs.append((author, title))
    return pairs


def probe(group: dict[str, Any]) -> dict[str, Any]:
    authors = group.get("author_aliases") or []
    titles = group.get("title_aliases") or []
    tried: list[str] = []
    archive: list[dict[str, Any]] = []
    seen: set[str] = set()

    for author, title in _terms(group)[:8]:
        query = f'creator:("{author}") AND title:("{title}")'
        tried.append(query)
        for doc in internet_archive(query, rows=4):
            key = str(doc.get("identifier"))
            if key not in seen:
                seen.add(key)
                archive.append(doc)
        time.sleep(PAUSE)

    # Title alone, because a catalogue's creator field is frequently a printer,
    # an editor or "Migne, J.-P." rather than the author of the work.
    for title in titles[:4]:
        query = f'title:("{title}")'
        tried.append(query)
        for doc in internet_archive(query, rows=4):
            key = str(doc.get("identifier"))
            if key not in seen:
                seen.add(key)
                archive.append(doc)
        time.sleep(PAUSE)

    migne = group.get("migne")
    if migne and migne != "none" and not str(migne).startswith("none"):
        for volume in re.findall(r"(P[LG])\s*(\d+)", str(migne)):
            series, number = volume
            query = f'"patrologia" AND "{series.lower()}" AND {number}'
            tried.append(query)
            for doc in internet_archive(query, rows=3):
                key = str(doc.get("identifier"))
                if key not in seen:
                    seen.add(key)
                    archive.append(doc)
            time.sleep(PAUSE)

    wiki: list[dict[str, Any]] = []
    for language in ("en", "la", "el"):
        for title in titles[:3]:
            tried.append(f"{language}.wikisource:{title}")
            wiki.extend(wikisource(title, language))
            time.sleep(PAUSE)
    for author in authors[:2]:
        tried.append(f"en.wikisource:{author}")
        wiki.extend(wikisource(author, "en"))
        time.sleep(PAUSE)

    guten: list[dict[str, Any]] = []
    for term in (titles[:2] + authors[:1]):
        tried.append(f"gutenberg:{term}")
        guten.extend(gutenberg(term))
        time.sleep(PAUSE)

    return {
        "id": group.get("id"),
        "canonical": group.get("canonical"),
        "aliases_tried": tried,
        "alias_count": len(set(tried)),
        "internet_archive": archive,
        "wikisource": [w for w in wiki if w.get("title")],
        "gutenberg": guten,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aliases", default=str(ALIASES))
    parser.add_argument("--out", required=True)
    parser.add_argument("--only", action="append", help="probe only these group ids")
    arguments = parser.parse_args(argv)

    try:
        import yaml
    except ImportError:
        print("PyYAML is required", file=sys.stderr)
        return 2

    table = yaml.safe_load(Path(arguments.aliases).read_text(encoding="utf-8"))
    groups = [g for g in table["groups"] if g.get("canonical")]
    if arguments.only:
        groups = [g for g in groups if g["id"] in set(arguments.only)]

    out = Path(arguments.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    surveyed = []
    for index, group in enumerate(groups, 1):
        print(f"{index}/{len(groups)} {group['id']}", file=sys.stderr, flush=True)
        surveyed.append(probe(group))
        out.write_text(json.dumps(surveyed, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"surveyed {len(surveyed)} groups -> {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
