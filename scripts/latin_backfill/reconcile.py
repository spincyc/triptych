"""Bring the Latin provenance ledger back into agreement with the calendar.

Three things go wrong after bodies land, and each has gone wrong at least once:

  * a row's text_sha256 still hashes the old body, because the YAML block scalar
    the calendar stores is not the string the applier hashed;
  * a landed row sits BESIDE the removed stub it should have replaced, and the
    duplicate key makes one proper read as a missing entry;
  * a row survives whose proper is no longer a body owner at all.

The owner walk is the checker's own `body_owners`, not a re-derivation, so
forms, courses and cycles are counted exactly as the checker counts them. That
matters: a hand-rolled walk once missed a form-bearing proper and dropped the
row the checker then demanded.

A row carrying a collated finding is never dropped for being unowned without
being named on stdout, because such a row is often the more valuable record --
St Albert's Collect is collated-exact against the 1962 facsimile with a Lasance
1945 passage in evidence, and an earlier pass discarded it silently.
"""

import re
import sys

sys.path.insert(0, "scripts")
import yaml  # noqa: E402
from _proper_latin import (  # noqa: E402
    SIDECAR_SUFFIX,
    body_owners,
    read_sidecar,
    text_owners,
    text_sha256,
)
from pathlib import Path  # noqa: E402

CALENDAR = "src/sources/calendars/roman-1962/propers.yaml"
LEDGER = "src/sources/inventories/roman-1962-proper-latin-provenance-v1.toml"


def key_of(block):
    field = lambda name: (re.search(rf'^{name} = "([^"]*)"', block, re.M) or [None, ""])[1]
    occurrence = int(re.search(r"^occurrence = (\d+)", block, re.M).group(1))
    return (
        field("mass"), field("form"), field("proper"),
        field("course"), field("cycle"), occurrence,
    )


def main():
    document = yaml.safe_load(open(CALENDAR, encoding="utf-8"))
    live = {
        (k.mass, k.form, k.proper, k.course, k.cycle, k.occurrence): text_sha256(text)
        for k, text in text_owners(document)
    }
    owned = {
        (r[0].mass, r[0].form, r[0].proper, r[0].course, r[0].cycle, r[0].occurrence)
        for r in body_owners(document)
    }

    raw = open(LEDGER, encoding="utf-8").read()
    head, blocks = raw.split("[[entries]]\n")[0], raw.split("[[entries]]\n")[1:]

    chosen, order, duplicates = {}, [], 0
    for block in blocks:
        key = key_of(block)
        if key in chosen:
            duplicates += 1
            # A landed row always beats a leftover removed stub.
            if 'body_status = "removed"' in block:
                continue
            chosen[key] = block
            continue
        chosen[key] = block
        order.append(key)

    kept, rehashed, dropped, named = [], 0, 0, []
    for key in order:
        block = chosen[key]
        if key in live:
            want = live[key]
            have = re.search(r'^text_sha256 = "([0-9a-f]{64})"', block, re.M).group(1)
            if have != want:
                block = re.sub(
                    r'^text_sha256 = "[0-9a-f]{64}"',
                    f'text_sha256 = "{want}"', block, count=1, flags=re.M,
                )
                rehashed += 1
        elif key not in owned:
            dropped += 1
            if 'provenance_status = "collated"' in block or "publication_evidence" in block:
                named.append("/".join(str(part) for part in key[:3]))
            continue
        kept.append(block.rstrip("\n") + "\n\n")

    open(LEDGER, "w", encoding="utf-8").write(
        (head + "[[entries]]\n" + "[[entries]]\n".join(kept)).rstrip("\n") + "\n"
    )
    rows, problems = read_sidecar(Path("src/sources/inventories") / f"roman-1962{SIDECAR_SUFFIX}")
    print(
        f"duplicates collapsed {duplicates}, hashes resynced {rehashed}, "
        f"unowned rows dropped {dropped} | ledger reads {len(rows)} rows, "
        f"{len(problems)} problems"
    )
    for one in named:
        print(f"  dropped a row that carried a collated finding: {one}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
