#!/usr/bin/env python3
"""Regenerate `src/sources/chronology/post-audit-rereview-manifest.tsv`.

The manifest is the targeted cold re-review's review target: one row per claim,
binding scope, gap row or hard case the post-audit correction lane changed
between the audited corpus and the correction target. It is DERIVED, not
sampled, and this is the derivation.

It was first built by a script that lived under `.scratch/` and did not
survive, whose comparison tuple was
`(disposition, str(claim.date), label, sources, basis, note)`. `str(date)`
renders a `relative` date's `statement` and never its anchor, so ten claims
whose `date.relative.of` moved compared equal on that field; three of them
changed nothing else but their note and were published to the reviewer as
`changed:note`. A moved anchor is the class the cold audit rated `major`. This
generator puts `date.relative.of` and `date.duration.within` into the tuple, so
those rows read `changed:anchor`.

The ROW SET is unchanged by that fix and must stay unchanged: every one of the
ten rows was already present, and the manifest is the record of what the
re-review actually inspected. Sharpening a `why` label describes a row already
there; adding a row would say the re-review inspected something it did not.

    python3 scripts/build_rereview_manifest.py             # to stdout
    python3 scripts/build_rereview_manifest.py --check     # exit 1 if stale
    python3 scripts/build_rereview_manifest.py --write

Defaults reproduce the tracked file: base `2330d63a5` (the audited corpus),
head `214797e78` (the correction target). Nothing under `.scratch/` is read.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import chronology_review_diff as D  # noqa: E402

AUDITED_CORPUS = "2330d63a5"
CORRECTION_TARGET = "214797e78"
MANIFEST = "src/sources/chronology/post-audit-rereview-manifest.tsv"

HEADER = """\
# Targeted cold re-review manifest for the post-audit correction lane.
# Audited corpus: {base}.  Correction target: {head}.
# Every row is a factual claim, binding scope, gap row or hard case the
# correction lane CHANGED, derived by loading both corpora through
# scripts/_chronology.py and diffing the loaded OBJECTS. Nothing here is
# sampled: the next cold reviewer inspects 100% of it.
# Both revisions are named by sha and neither is "HEAD", because HEAD moves and
# this file does not.
# Regenerate with `python3 scripts/build_rereview_manifest.py`; check with
# `--check`. Comparing objects rather than YAML text means a reformat cannot
# hide a change, and comparing `date.relative.of` rather than only `str(date)`
# means a moved anchor cannot hide behind an unrestated statement.
"""

COLUMNS = ("review_id", "kind", "identifier", "why", "locus", "notes")

# The sixteen rows below are not derivable from a corpus diff, and are declared
# here rather than discovered: they are the architecture and hard cases the
# contract names for review -- the §15.1 defect classes, the native non-Vulgate
# axis, the gate regressions, and the source records this lane registered. They
# are carried verbatim from the manifest as the re-review received it, because
# the manifest is the record of what that review inspected.
HARD_CASES = (
    ("hard-case", "israel.patriarchs.call-of-abram / birth-of-abram", "critical-correction", "Gen.11.26; Gen.12.4", "the Flood-to-Abram intervals; verify they land on the call and not the birth"),
    ("hard-case", "greek Ecclus 36:16", "native-hard-case", "Ecclus.36.16 --system greek", "the one safely-shared Greek locus; both axes must answer and the native date must survive the mapping"),
    ("hard-case", "greek Ecclus 35:1", "native-hard-case", "Ecclus.35.1 --system greek", "mapping refuses, chronology answers"),
    ("hard-case", "hebrew Ps 51", "safe-shared-alternate-system", "Ps.51.3 --system hebrew", "must reach vulgate Ps.50.3 with identical assertions and no duplicate authored data"),
    ("hard-case", "mixed-validity native span", "gate-regression", "greek Ecclus 36", "a span whose first locus refuses and whose interior would duplicate must be refused at load"),
    ("hard-case", "greek EsthGr.15.10", "native-status-gap", "EsthGr.15.10 --system greek", "research-pending on the chronology axis, textually-distinct on the mapping axis"),
    ("hard-case", "world-english-catholic Dan.3.71", "native-status-gap", "Dan.3.71 --system world-english-catholic", ""),
    ("hard-case", "world-english-catholic Esth.1.1", "native-status-gap", "Esth.1.1 --system world-english-catholic", ""),
    ("hard-case", "world-english-catholic Esth.3.13", "native-status-gap", "Esth.3.13 --system world-english-catholic", ""),
    ("hard-case", "world-english-catholic Esth.5.1", "native-status-gap", "Esth.5.1 --system world-english-catholic", ""),
    ("hard-case", "world-english-catholic Esth.5.2", "native-status-gap", "Esth.5.2 --system world-english-catholic", ""),
    ("hard-case", "world-english-catholic Esth.8.13", "native-status-gap", "Esth.8.13 --system world-english-catholic", ""),
    ("hard-case", "world-english-catholic Esth.4.6 / Esth.9.5 / Esth.9.30", "withdrawn-native-loci", "", "the witness prints none of these; verify they are absent from the universe rather than statusless"),
    ("hard-case", "israel.monarchy.temple-begun#5", "maintainer-question", "", "Howlett's 958 B.C. survives as an alternate beneath rank-1 Scripture while its twins from the same sentence (Exodus 1277, Saul 1020) were withdrawn as modern-critical. A cold auditor passed this claim (P-008). The next reviewer should rule."),
    ("hard-case", "artifact.catholic-encyclopedia.alphabetical-index.*", "newly-registered-source", "", "two index pages registered by this lane; the Genesis and Numbers gap rows now rest on them"),
    ("hard-case", "artifact.catholic-encyclopedia.volume-6/9/11 newadvent-06412b, 06412c, 06413a, 06413c, 09207a, 11151a", "newly-registered-source", "", "six articles registered by this lane; gap rows rest on them"),
)

NOTE = {"added": "absent at {base}",
        "withdrawn": "present at {base}, absent now"}


def rows(repo: Path, base: str, head: str) -> list[tuple[str, ...]]:
    sections = D.build(repo, base, head,
                       ("claims", "bindings", "gaps"), "manifest")
    out: list[tuple[str, ...]] = []
    for row in sections["claims"]:
        out.append(("claim", row["id"], row["why"], "",
                    NOTE.get(row["why"], "").format(base=base)))
    for row in sections["bindings"]:
        out.append(("binding", row["id"], row["why"], row["locus"], ""))
    for row in sections["gaps"]:
        out.append(("gap", row["id"], row["why"], "", ""))
    out.extend(HARD_CASES)
    return out


def render(repo: Path, base: str, head: str) -> str:
    lines = [HEADER.format(base=base, head=head).rstrip("\n"), "\t".join(COLUMNS)]
    for index, row in enumerate(rows(repo, base, head), start=1):
        lines.append("\t".join((f"RR-{index:03d}", *row)))
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--repo", default=str(REPO))
    parser.add_argument("--base", default=AUDITED_CORPUS)
    parser.add_argument("--head", default=CORRECTION_TARGET)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    text = render(repo, args.base, args.head)
    target = repo / MANIFEST
    if args.check:
        if target.read_text() == text:
            count = sum(1 for line in text.splitlines()
                        if line.startswith("RR-"))
            print(f"{MANIFEST} is current: {count} rows")
            return 0
        print(f"{MANIFEST} differs from a fresh derivation", file=sys.stderr)
        return 1
    if args.write:
        target.write_text(text)
        print(f"wrote {MANIFEST}")
        return 0
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
