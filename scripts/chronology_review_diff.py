#!/usr/bin/env python3
"""Diff two revisions of the chronology corpus and its evidence, as OBJECTS.

Why this exists, and why it does not diff text
----------------------------------------------
A review manifest that claims to list "every claim this lane changed" is worth
exactly what its diff is worth. `git diff` of the YAML answers a different
question: it reports reflowed prose, reordered keys and re-indentation as
changes, and reports a claim that moved between two events as a deletion and an
addition of unrelated text. This tool loads both revisions through the
chronology loader and compares the loaded OBJECTS, so a reformat is invisible
and a moved anchor is not.

Which loader, and why it matters
--------------------------------
Each revision is loaded by the loader AS IT STOOD AT THAT REVISION, in its own
subprocess. That is not fussiness. `scripts/_chronology.py` gains refusals over
time -- it gained a duplicate-YAML-key refusal on 2026-08-27 -- and a later
loader run over an earlier corpus refuses to read history that was valid when
it was written. A review artifact pinned to two shas must stay re-derivable
after the loader moves, or it is not evidence.

The comparison itself is therefore NOT the loader's. Every rendering a
comparison depends on -- how a date prints, how a span prints -- is recomputed
here, from the structure, identically for both sides (`_date_text`,
`_span_text`). A change to `Date.__str__` cannot arrive dressed as a change to
a claim, and neither can a change to a refusal.

Shared reference data -- `src/sources/bibles` and `src/sources/works`, which
`_canon`, `_psalms` and `_deuterocanon` read -- is taken from the INVOKING
checkout for both revisions, so the book index and the two concordances are one
lens over both corpora. Where those paths differ between the revisions the tool
says so, and the `sources` section reports the difference as its own case.

What it compares
----------------
claims     one row per authored claim (`event:<id>#n` / `unit:<id>#n`), over
           the field set named by --fields
bindings   grouped by (relation, event) -- the identity a manifest row names --
           comparing the union of authored scopes, and, under `full`, the
           notes and the sources
gaps       keyed by (status, scope), comparing reason and sources
sources    the work/edition/artifact/passage TOML registry, field by field
contracts  `guidance/` files, which state contracts
code       `scripts/`, `tools/`, `tests/`, which state behaviour

Usage
-----
    python3 scripts/chronology_review_diff.py BASE HEAD
    python3 scripts/chronology_review_diff.py BASE HEAD --section claims --fields manifest
    python3 scripts/chronology_review_diff.py BASE HEAD --json > diff.json

BASE and HEAD are any two git revisions. Nothing under `.scratch/` is read,
nothing outside a temporary directory is written, and the working tree is not
touched -- so it runs against a clean checkout with uncommitted work present.
"""

from __future__ import annotations

import argparse
import collections
import io
import json
import subprocess
import sys
import tarfile
import tempfile
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHRONOLOGY = "src/sources/chronology"
WORKS = "src/sources/works"
BIBLES = "src/sources/bibles"

# Read from the invoking checkout for both revisions; see the module docstring.
SHARED = (BIBLES, WORKS)


# --- git -------------------------------------------------------------------

def _git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args],
                          check=True, capture_output=True, text=True).stdout


def _extract(repo: Path, rev: str, into: Path, *pathspecs: str) -> None:
    into.mkdir(parents=True, exist_ok=True)
    blob = subprocess.run(["git", "-C", str(repo), "archive", rev, "--", *pathspecs],
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(blob)) as tar:
        tar.extractall(into, filter="data")


def _blobs(repo: Path, rev: str, pathspec: str) -> dict[str, str]:
    found = {}
    for line in _git(repo, "ls-tree", "-r", rev, "--", pathspec).splitlines():
        meta, path = line.split("\t", 1)
        _mode, kind, sha = meta.split()
        if kind == "blob":
            found[path] = sha
    return found


def _blob_text(repo: Path, sha: str) -> str:
    return subprocess.run(["git", "-C", str(repo), "cat-file", "blob", sha],
                          check=True, capture_output=True
                          ).stdout.decode("utf-8", "replace")


# --- loading one revision, with its own loader ----------------------------

# Runs inside the extracted tree of ONE revision, with that revision's
# `scripts/` first on the path. It dumps structure and never a rendering: every
# string a comparison depends on is built on this side of the boundary by
# `_date_text` and `_span_text`, so two revisions are rendered by one function.
WORKER = r'''
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
import _chronology as C

def endpoint(e):
    return None if e is None else [e.year, e.era, e.month, e.day, e.calendar]

def date(d):
    return {"precision": d.precision, "begin": endpoint(d.begin),
            "end": endpoint(d.end), "relative": d.relative, "label": d.label,
            "derivation": d.derivation, "duration": d.duration}

def claim(c):
    return {"profile": c.profile, "disposition": c.disposition, "date": date(c.date),
            "basis": c.basis, "sources": list(c.sources), "note": c.note}

def span(s):
    return [s.system, s.token, s.chapter, s.first, s.last]

corpus = C.load(Path(sys.argv[1]))
out = {"claims": {}, "bindings": [], "gaps": []}
for event in corpus.events.values():
    for i, c in enumerate(event.claims):
        out["claims"]["event:%s#%d" % (event.id, i)] = claim(c)
for unit in corpus.units.values():
    for i, c in enumerate(unit.claims):
        out["claims"]["unit:%s#%d" % (unit.id, i)] = claim(c)
for b in corpus.bindings:
    out["bindings"].append({"relation": b.relation, "event": b.event,
                            "scope": [span(s) for s in b.scope],
                            "note": b.note, "sources": list(b.sources)})
for g in corpus.gaps:
    out["gaps"].append({"status": g.status, "scope": [span(s) for s in g.scope],
                        "reason": g.reason, "sources": list(g.sources)})
json.dump(out, sys.stdout, sort_keys=True, default=str)
'''


def load_revision(repo: Path, rev: str, workdir: Path) -> dict:
    """The corpus at `rev`, read by the loader at `rev`, as plain structure."""
    tree = workdir / rev.replace("/", "_")
    _extract(repo, rev, tree, "scripts", CHRONOLOGY)
    for shared in SHARED:
        link = tree / shared
        link.parent.mkdir(parents=True, exist_ok=True)
        if not link.exists():
            link.symlink_to(repo / shared)
    worker = tree / "_review_projection.py"
    worker.write_text(WORKER)
    done = subprocess.run([sys.executable, str(worker), str(tree / CHRONOLOGY)],
                          capture_output=True, text=True, cwd=str(tree))
    if done.returncode:
        raise SystemExit(
            f"the corpus at {rev} would not load with the loader at {rev}:\n"
            + done.stderr.strip())
    return json.loads(done.stdout)


# --- renderings, computed HERE and not by either loader --------------------

ERA = {"bc": "B.C.", "ad": "A.D.", "am": "A.M."}
DURATION_UNITS = ("years", "months", "days")


def _endpoint_text(e) -> str:
    if e is None:
        return "?"
    year, era, month, day, _calendar = e
    if year is None:
        if month is None:
            return "?"
        return f"{month:02d}-{day:02d}" if day else f"month {month}"
    label = ERA[era or "ad"]
    if month and day:
        return f"{year} {label}, {month:02d}-{day:02d}"
    return f"{year} {label}"


def _duration_text(duration: dict) -> str:
    parts = [f"{duration[u]} {u[:-1] if duration[u] == 1 else u}"
             for u in DURATION_UNITS if duration.get(u)]
    return " ".join(parts) or "?"


def _date_text(d: dict) -> str:
    if d["precision"] == "duration" and d["duration"]:
        return str(d["duration"].get("statement") or _duration_text(d["duration"]))
    if d["precision"] == "relative" and d["relative"]:
        return str(d["relative"].get("statement") or d["relative"])
    if d["begin"] is None:
        return "?"
    if d["begin"] == d["end"] or d["end"] is None:
        head = _endpoint_text(d["begin"])
        return f"about {head}" if d["precision"] == "approximate-year" else head
    joiner = "-" if d["precision"] == "range" else " to "
    return f"{_endpoint_text(d['begin'])}{joiner}{_endpoint_text(d['end'])}"


def _span_text(s) -> str:
    _system, token, chapter, first, last = s
    if chapter is None:
        return token
    if first is None and last is None:
        return f"{token}.{chapter}"
    if first == last:
        return f"{token}.{chapter}.{first}"
    return f"{token}.{chapter}.{first or 1}-{last if last is not None else ''}"


# --- the fields a claim is compared over -----------------------------------

def _anchor(c) -> object:
    """The event a date is measured FROM. A duration's `within` is not one."""
    rel = c["date"]["relative"]
    return rel.get("of") if rel else None


def _within(c) -> object:
    dur = c["date"]["duration"]
    return dur.get("within") if dur else None


def _j(value) -> str:
    return json.dumps(value, sort_keys=True, default=str)


# The eight fields the re-review manifest compares, in the order its `why`
# column prints them. `anchor` and `within` are the two the first generator was
# missing: `str(date)` renders a relative date's STATEMENT, so an anchor moved
# without a restated statement compared equal and printed as `changed:note`.
FIELDS_MANIFEST = (
    ("disposition", lambda c: c["disposition"]),
    ("date", lambda c: _date_text(c["date"])),
    ("anchor", _anchor),
    ("within", _within),
    ("label", lambda c: c["date"]["label"]),
    ("sources", lambda c: c["sources"]),
    ("basis", lambda c: c["basis"]),
    ("note", lambda c: c["note"]),
)

# Everything a claim holds. `str(date)` renders none of the rest either, and a
# production diff that must miss nothing compares the structure.
FIELDS_FULL = FIELDS_MANIFEST + (
    ("profile", lambda c: c["profile"]),
    ("precision", lambda c: c["date"]["precision"]),
    ("endpoints", lambda c: _j((c["date"]["begin"], c["date"]["end"]))),
    ("relative", lambda c: _j(c["date"]["relative"])),
    ("duration", lambda c: _j(c["date"]["duration"])),
    ("derivation", lambda c: _j(c["date"]["derivation"])),
)

FIELD_SETS = {"manifest": FIELDS_MANIFEST, "full": FIELDS_FULL}


# --- the diffs -------------------------------------------------------------

def diff_claims(old: dict, new: dict, fields=FIELDS_MANIFEST) -> list[dict]:
    before, after = old["claims"], new["claims"]
    rows = []
    for key in sorted(set(before) | set(after)):
        if key not in after:
            rows.append({"kind": "claim", "id": key, "why": "withdrawn",
                         "detail": "present at base, absent now"})
        elif key not in before:
            rows.append({"kind": "claim", "id": key, "why": "added",
                         "detail": "absent at base"})
        else:
            moved = [n for n, get in fields if get(before[key]) != get(after[key])]
            if moved:
                rows.append({"kind": "claim", "id": key,
                             "why": "changed:" + "+".join(moved), "detail": ""})
    return rows


def _binding_groups(corpus: dict) -> dict[tuple[str, str], dict]:
    """Grouped by the identity a manifest row names: relation + event.

    Several authored rows collapse into one. Their scopes are unioned, because
    comparing per-row lists reports a scope split as one deletion and two
    additions of the same fact.
    """
    grouped = collections.defaultdict(
        lambda: {"scope": set(), "notes": set(), "sources": set()})
    for binding in corpus["bindings"]:
        cell = grouped[(binding["relation"], binding["event"])]
        cell["scope"].update(_span_text(s) for s in binding["scope"])
        cell["notes"].add(binding["note"])
        cell["sources"].add(tuple(binding["sources"]))
    return grouped


def _text(scope: set[str]) -> str:
    return ",".join(sorted(scope))


def diff_bindings(old: dict, new: dict, full: bool = False) -> list[dict]:
    before, after = _binding_groups(old), _binding_groups(new)
    rows = []
    for key in sorted(set(before) | set(after)):
        name = f"{key[0]} -> {key[1]}"
        if key not in after:
            rows.append({"kind": "binding", "id": name, "why": "withdrawn",
                         "locus": _text(before[key]["scope"]), "detail": ""})
        elif key not in before:
            rows.append({"kind": "binding", "id": name, "why": "added",
                         "locus": _text(after[key]["scope"]), "detail": ""})
        else:
            a, b = before[key], after[key]
            if a["scope"] != b["scope"]:
                rows.append({"kind": "binding", "id": name, "why": "scope-changed",
                             "locus": f"was: {_text(a['scope'])} | "
                                      f"now: {_text(b['scope'])}", "detail": ""})
            elif full and (a["notes"] != b["notes"] or a["sources"] != b["sources"]):
                moved = ([] if a["notes"] == b["notes"] else ["note"]) + \
                        ([] if a["sources"] == b["sources"] else ["sources"])
                rows.append({"kind": "binding", "id": name,
                             "why": "changed:" + "+".join(moved),
                             "locus": _text(b["scope"]), "detail": ""})
    return rows


def diff_gaps(old: dict, new: dict) -> list[dict]:
    def keyed(corpus):
        return {(g["status"], ",".join(_span_text(s) for s in g["scope"])): g
                for g in corpus["gaps"]}
    before, after = keyed(old), keyed(new)
    rows = []
    for key in sorted(set(before) | set(after)):
        name = f"{key[0]} @ {key[1]}"
        if key not in after:
            rows.append({"kind": "gap", "id": name, "why": "withdrawn", "detail": ""})
        elif key not in before:
            rows.append({"kind": "gap", "id": name, "why": "added", "detail": ""})
        else:
            a, b = before[key], after[key]
            if (a["reason"], a["sources"]) != (b["reason"], b["sources"]):
                moved = ([] if a["reason"] == b["reason"] else ["reason"]) + \
                        ([] if a["sources"] == b["sources"] else ["sources"])
                rows.append({"kind": "gap", "id": name,
                             "why": "reason-or-sources-changed",
                             "detail": "+".join(moved)})
    return rows


# --- the source registry ---------------------------------------------------

def record_id(path: str) -> str | None:
    """`.../works/<a>/<w>/editions/<e>/artifacts/<x>/artifact.toml` is
    `artifact.<a>.<w>.<e>.<x>`. The id IS the path, which is why no record
    restates it."""
    parts = path.split("/")
    if parts[:3] != ["src", "sources", "works"]:
        return None
    rest = parts[3:]
    if len(rest) == 3 and rest[2] == "work.toml":
        return "work." + ".".join(rest[:2])
    if len(rest) == 5 and rest[2] == "editions" and rest[4] == "edition.toml":
        return "edition." + ".".join((rest[0], rest[1], rest[3]))
    if len(rest) == 7 and rest[2] == "editions" and rest[4] == "artifacts" \
            and rest[6] == "artifact.toml":
        return "artifact." + ".".join((rest[0], rest[1], rest[3], rest[5]))
    if len(rest) == 6 and rest[2] == "editions" and rest[4] == "passages" \
            and rest[5].endswith(".toml"):
        return "passage." + ".".join((rest[0], rest[1], rest[3], rest[5][:-5]))
    return None


def _flatten(value, prefix: str = "") -> dict[str, str]:
    flat: dict[str, str] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            flat.update(_flatten(item, f"{prefix}.{key}" if prefix else str(key)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            flat.update(_flatten(item, f"{prefix}[{index}]"))
    else:
        flat[prefix] = str(value)
    return flat


def diff_sources(repo: Path, base: str, head: str) -> list[dict]:
    before, after = _blobs(repo, base, WORKS), _blobs(repo, head, WORKS)
    rows = []
    for path in sorted(set(before) | set(after)):
        if before.get(path) == after.get(path):
            continue
        rid = record_id(path)
        if rid is None:
            rows.append({"kind": "registry-asset", "id": path, "detail": "",
                         "why": "added" if path not in before
                                else "removed" if path not in after else "changed"})
            continue
        if path not in after:
            rows.append({"kind": "source-record", "id": rid, "why": "removed",
                         "detail": path})
        elif path not in before:
            rows.append({"kind": "source-record", "id": rid, "why": "added",
                         "detail": path})
        else:
            try:
                a = _flatten(tomllib.loads(_blob_text(repo, before[path])))
                b = _flatten(tomllib.loads(_blob_text(repo, after[path])))
            except tomllib.TOMLDecodeError as exc:
                rows.append({"kind": "source-record", "id": rid,
                             "why": "unparseable", "detail": f"{path}: {exc}"})
                continue
            moved = sorted({k for k in set(a) | set(b) if a.get(k) != b.get(k)})
            if moved:
                rows.append({"kind": "source-record", "id": rid,
                             "why": "changed:" + "+".join(moved), "detail": path})
    return rows


# --- contracts and behaviour ----------------------------------------------

def diff_paths(repo: Path, base: str, head: str, pathspec: str, kind: str) -> list[dict]:
    rows = []
    for line in _git(repo, "diff", "--numstat", "--find-renames",
                     f"{base}..{head}", "--", pathspec).splitlines():
        added, removed, path = line.split("\t", 2)
        rows.append({"kind": kind, "id": path, "detail": "",
                     "why": f"changed:+{added}/-{removed}"})
    return rows


# --- CLI -------------------------------------------------------------------

SECTIONS = ("claims", "bindings", "gaps", "sources", "contracts", "code")


def build(repo: Path, base: str, head: str, sections, fieldset: str) -> dict:
    result: dict[str, list[dict]] = {}
    if {"claims", "bindings", "gaps"} & set(sections):
        with tempfile.TemporaryDirectory(prefix="chronology-review-") as tmp:
            work = Path(tmp)
            old = load_revision(repo, base, work)
            new = load_revision(repo, head, work)
        if "claims" in sections:
            result["claims"] = diff_claims(old, new, FIELD_SETS[fieldset])
        if "bindings" in sections:
            result["bindings"] = diff_bindings(old, new, full=(fieldset == "full"))
        if "gaps" in sections:
            result["gaps"] = diff_gaps(old, new)
    if "sources" in sections:
        result["sources"] = diff_sources(repo, base, head)
    if "contracts" in sections:
        result["contracts"] = diff_paths(repo, base, head, "guidance", "contract")
    if "code" in sections:
        result["code"] = sum(
            (diff_paths(repo, base, head, where, "code")
             for where in ("scripts", "tools", "tests")), [])
    return result


def shared_data_warnings(repo: Path, base: str, head: str) -> list[str]:
    """The bible index and the two concordances are read from the invoking
    checkout for both revisions. Say so when they moved between them."""
    said = []
    for pathspec in SHARED:
        if _blobs(repo, base, pathspec) != _blobs(repo, head, pathspec):
            said.append(f"# {pathspec} differs between {base} and {head}; both "
                        f"corpora were read through the invoking checkout's copy")
    return said


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("base")
    parser.add_argument("head")
    parser.add_argument("--repo", default=str(REPO))
    parser.add_argument("--section", action="append", choices=SECTIONS)
    parser.add_argument("--fields", choices=tuple(FIELD_SETS), default="full")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    sections = args.section or list(SECTIONS)
    result = build(repo, args.base, args.head, sections, args.fields)
    warnings = shared_data_warnings(repo, args.base, args.head)

    if args.json:
        json.dump({"base": _git(repo, "rev-parse", args.base).strip(),
                   "head": _git(repo, "rev-parse", args.head).strip(),
                   "fields": args.fields, "warnings": warnings,
                   "sections": result}, sys.stdout, indent=1, sort_keys=True)
        print()
        return 0
    for line in warnings:
        print(line, file=sys.stderr)
    for section in sections:
        for row in result.get(section, []):
            print("\t".join((row["kind"], row["id"], row["why"],
                             row.get("locus", ""), row.get("detail", ""))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
