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
profiles   `profiles.yaml` as NORMALISED SEMANTICS -- every leaf of every
           profile, keyed by its path, with whitespace collapsed so a reflowed
           block scalar compares equal and a changed policy does not
answerability
           which claims the profile answers with, computed on both sides by the
           same function here, so a claim whose eligibility moved because the
           POLICY moved is enumerated even though its own YAML is untouched
bindings   grouped by (relation, event) -- the identity a manifest row names --
           comparing the union of authored scopes, and, under `full`, the
           notes and the sources
gaps       keyed by (status, scope), comparing reason and sources
sources    the work/edition/artifact/passage TOML registry, field by field
contracts  `guidance/` files, which state contracts
code       `scripts/`, `tools/`, `tests/`, which state behaviour

Why `profiles` and `answerability` are here
-------------------------------------------
`profiles.yaml` is PRODUCTION SEMANTIC STATE, not configuration. It decides
which stored claims are candidate answers, so a one-line policy edit can change
the meaning of hundreds of claims whose files nobody touched. Until 2026-09-01
this tool compared claims, bindings, gaps, sources, guidance and code, and
`profiles.yaml` fell in no bucket at all: the final cold audit changed the
conflict rule from "preserve the disagreement" to "harmonise freely" and the
diff reported nothing. A review artifact that cannot see that is not evidence.

The `answerability` section is the transitive half. A profile edit produces a
handful of `profile` rows and, potentially, a great many claims that stopped or
started being answerable. The reviewer needs the second list, and it cannot come
from either loader -- the older one has no notion of answerability -- so it is
computed here from the dumped structure, identically for both sides, exactly as
`_date_text` and `_span_text` already are.

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
    # `getattr` because the loader AT THE BASE REVISION may predate the
    # answerability axis entirely, and a review artifact pinned to two shas has
    # to stay derivable across the revision that introduced it. A claim from
    # before the axis existed was answerable, which is what the fallback says.
    return {"profile": c.profile, "disposition": c.disposition, "date": date(c.date),
            "basis": c.basis, "sources": list(c.sources), "note": c.note,
            "answerability": getattr(c, "answerability", "answerable"),
            "basis_class": getattr(c, "basis_class", ""),
            "reporting_exception": getattr(c, "reporting_exception", None)}

def span(s):
    return [s.system, s.token, s.chapter, s.first, s.last]

corpus = C.load(Path(sys.argv[1]))
out = {"claims": {}, "bindings": [], "gaps": [], "profiles": {}}
# The profile mapping AS AUTHORED. Normalisation happens on the other side of
# the boundary, so both revisions are normalised by one function.
for pid, entry in corpus.profiles.items():
    out["profiles"][pid] = entry
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


# The fields the re-review manifest compares, in the order its `why` column
# prints them. `anchor` and `within` are the two the first generator was
# missing: `str(date)` renders a relative date's STATEMENT, so an anchor moved
# without a restated statement compared equal and printed as `changed:note`.
# `answerability` and `basis_class` are the two the second was: a claim that
# stopped being a candidate answer is the most consequential thing a correction
# lane can do to one, and it moves no date and no source.
FIELDS_MANIFEST = (
    ("disposition", lambda c: c["disposition"]),
    ("answerability", lambda c: c.get("answerability", "answerable")),
    ("basis_class", lambda c: c.get("basis_class", "")),
    ("reporting_exception", lambda c: c.get("reporting_exception")),
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


# --- the profile, which is policy and therefore production state ----------

# Which part of the policy moved, for a reviewer scanning the section. The
# facets are the ones a profile edit can change the meaning of the corpus
# through: who wins, what is admissible, what the profile answers with, what it
# does when sources disagree, and what it merely preserves.
FACETS = {
    "authority": "authority-hierarchy",
    "non_authorities": "authority-hierarchy",
    "admissibility": "admissibility",
    "answerability": "answerability",
    "conflict": "conflict-policy",
    "display": "display-rules",
    "non_goals": "scope",
    "versioning": "scope",
}


def _facet(path: str) -> str:
    head = path.split(".", 1)[0].split("[", 1)[0]
    if path.startswith("admissibility.reporting_exceptions"):
        return "reporting-exceptions"
    if path.startswith("admissibility.bases"):
        return "admissibility"
    return FACETS.get(head, head)


def _normalised(profile: dict) -> dict[str, str]:
    """One profile as leaf paths to values, with prose whitespace collapsed.

    FORMATTING IS NOT POLICY. A YAML block scalar re-wrapped at a different
    column is the same rule, and a diff that reported it would train a reviewer
    to skim this section -- which is how the section stops being read at all.
    Collapsing runs of whitespace is the whole of the normalisation: nothing
    else about the text is touched, so a changed WORD is still a changed rule.
    """
    return {
        key: " ".join(value.split())
        for key, value in _flatten(profile).items()
    }


def _clip(text: str, width: int = 200) -> str:
    return text if len(text) <= width else text[: width - 1] + "\u2026"


def diff_profiles(old: dict, new: dict) -> list[dict]:
    """Every profile-policy leaf that moved, added, or went away.

    `profiles.yaml` used to fall in no section of this tool at all, so a policy
    edit produced an empty diff while changing what hundreds of untouched claims
    mean. That is the defect this section closes, and it closes it by comparing
    the whole normalised mapping rather than by watching named phrases: a rule
    this tool had to be taught to look for is a rule the next edit renames.
    """
    before, after = old.get("profiles", {}), new.get("profiles", {})
    rows: list[dict] = []
    for pid in sorted(set(before) | set(after)):
        if pid not in after:
            rows.append({"kind": "profile", "id": pid, "why": "withdrawn",
                         "locus": "profile", "detail": "present at base, absent now"})
            continue
        if pid not in before:
            rows.append({"kind": "profile", "id": pid, "why": "added",
                         "locus": "profile", "detail": "absent at base"})
            continue
        a, b = _normalised(before[pid]), _normalised(after[pid])
        for path in sorted(set(a) | set(b)):
            if a.get(path) == b.get(path):
                continue
            if path not in b:
                why, detail = "removed", f"was: {_clip(a[path])}"
            elif path not in a:
                why, detail = "added", f"now: {_clip(b[path])}"
            else:
                why = "changed"
                detail = f"was: {_clip(a[path])} | now: {_clip(b[path])}"
            rows.append({"kind": "profile", "id": f"{pid}:{path}", "why": why,
                         "locus": _facet(path), "detail": detail})
    return rows


# --- answerability, including the claims only the profile moved -----------

def policy_of(profile: dict | None) -> dict | None:
    """A profile's admissibility contract, as this tool needs to apply it.

    Returns None for a profile that declares none, which is what every revision
    before 2026-09-01 holds. That is not "admit nothing": before the contract
    existed every stored claim was a candidate, and a diff that read the older
    side as excluding everything would report the whole corpus as newly
    answerable on the day the field appeared.
    """
    if not isinstance(profile, dict):
        return None
    raw = profile.get("admissibility")
    if not isinstance(raw, dict):
        return None
    bases = {
        base.get("id"): bool(base.get("admissible"))
        for base in raw.get("bases") or []
        if isinstance(base, dict)
    }
    states = profile.get("answerability")
    return {
        "admissible": {name for name, ok in bases.items() if ok},
        "unstated_basis": raw.get("unstated") or "",
        "unstated_state": (states or {}).get("unstated") or "answerable",
        "exceptions": {
            lift.get("id"): lift.get("basis")
            for lift in raw.get("reporting_exceptions") or []
            if isinstance(lift, dict)
        },
    }


def answerable(claim: dict, policy: dict | None) -> bool:
    """THE SAME RULE ON BOTH SIDES, and computed by neither loader.

    `scripts/_chronology.Policy.answers_with` is the production copy. This one
    exists for the same reason `_date_text` does: a comparison that asked each
    revision's own code would report a change in the code as a change in the
    corpus, and a base revision that has no such code could not be asked at all.
    """
    if claim.get("answerability", "answerable") != "answerable":
        return False
    if policy is None:
        return True
    basis = claim.get("basis_class") or policy["unstated_basis"]
    if basis in policy["admissible"]:
        return True
    lift = claim.get("reporting_exception")
    return bool(lift and policy["exceptions"].get(lift) == basis)


def diff_answerability(old: dict, new: dict, fields=None) -> list[dict]:
    """Every claim whose candidate eligibility moved, and why it moved.

    The `profile-only` rows are the ones no other section can produce: the claim
    is byte-identical and means something different, because the policy it is
    read under changed. Enumerating them is the difference between a review
    surface and a file diff.
    """
    fields = fields or FIELDS_FULL
    before, after = old["claims"], new["claims"]
    policies_before = {pid: policy_of(entry)
                       for pid, entry in old.get("profiles", {}).items()}
    policies_after = {pid: policy_of(entry)
                      for pid, entry in new.get("profiles", {}).items()}
    rows = []
    for key in sorted(set(before) & set(after)):
        was = answerable(before[key], policies_before.get(before[key]["profile"]))
        now = answerable(after[key], policies_after.get(after[key]["profile"]))
        if was == now:
            continue
        moved = [name for name, get in fields if get(before[key]) != get(after[key])]
        rows.append({
            "kind": "answerability",
            "id": key,
            "why": ("answerable->preserved" if was else "preserved->answerable"),
            "locus": "profile-only" if not moved else "claim-changed",
            "detail": ("the claim did not change; the profile did"
                       if not moved else "+".join(moved)),
        })
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

SECTIONS = ("claims", "profiles", "answerability", "bindings", "gaps",
            "sources", "contracts", "code")


def build(repo: Path, base: str, head: str, sections, fieldset: str) -> dict:
    result: dict[str, list[dict]] = {}
    if {"claims", "profiles", "answerability", "bindings", "gaps"} & set(sections):
        with tempfile.TemporaryDirectory(prefix="chronology-review-") as tmp:
            work = Path(tmp)
            old = load_revision(repo, base, work)
            new = load_revision(repo, head, work)
        if "claims" in sections:
            result["claims"] = diff_claims(old, new, FIELD_SETS[fieldset])
        if "profiles" in sections:
            result["profiles"] = diff_profiles(old, new)
        if "answerability" in sections:
            result["answerability"] = diff_answerability(
                old, new, FIELD_SETS[fieldset]
            )
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
