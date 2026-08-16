#!/usr/bin/env python3
"""Dump the replay harness's request journals for the namespace scenarios.

The V7 review's standard is the ACTUAL REQUEST SINK: the proof is the journal
of paths that reached the stubbed `fetch`, not a helper's return value. This
runs the replay harness exactly as the test suite does — the production
`browser-core.js`, `catena-model.js` and `catena.js` under node, every
scenario driven to its labelled snapshots — and prints, for each scenario
named below, the complete fetched journal and the terminal sinks the
directions require: status writes, `aria-busy`, the visible per-fragment
text, history writes, and the failure paragraph.

Run at the head, the V8 scenarios show zero wrong-namespace requests and the
preserved valid ones, and the V9 scenarios show zero requests after a
refused prefix — cold, prewarmed and late. Run at the parent with the head's
test file copied in, the same scenarios show the defect's own journal — the
carried-fallback request made after the refused prefix — which is the
demonstration, not the assumption. V9 dumps EVERY labelled snapshot of each
scenario, not the terminal one alone, so the prewarmed and late phases are
readable in order, and adds the standing status text, the focus target and
the released-request count to the sinks.

V11, THE V10 REVIEW: the live harness captured request OWNERSHIP and this
dump threw it away. `FIELDS` was a fourteen-name whitelist that kept the flat
`fetched` list and dropped `requests`, `fragmentIds`, `historyState` and
`replacedStates` — so the packaged log could not reproduce the ownership
claim the package made, and a reader had to rerun the harness to check it.
Two things follow.

First, the whitelist now carries all four. `requests` is the owned journal
proper: every row states its sequence, the address it asked for, the KIND of
record that address holds, the step that owned the request, and what became
of it — `completed`, `held` while parked, `released` once let go, or
`failed`. That is enough to reproduce every ownership claim from the package
alone.

Second, a whitelist that silently yields `null` for a field the harness no
longer emits is how the omission survived. Every name is now checked against
the snapshot, and a missing one is a hard failure that names itself, so the
dump cannot quietly go hollow again.

Beside the JSON, a compact human-readable ownership table is printed for each
scenario: the same rows, in sequence, readable without a JSON parser. Both
are the same data; neither is derived from prose.

Usage: journal-dump.py PATH/TO/test_catena_wave_1.py
"""
import importlib.util
import json
import sys

NAMES = [
    "v8-wrong-namespace-prefix",
    "v8-padded-prefix",
    "v8-wrong-namespace-carried",
    "v7-text-path",
    "v7-text-path-no-prefix",
    "v9-refused-prefix-carried",
    "v9-padded-prefix-carried",
    "v9-absent-prefix-carried",
    "v9-valid-prefix-carried",
    "v9-prewarmed-fallback",
    "v9-late-fallback",
    # V11 §2 — every unestablished prefix, at the visible and request sinks.
    "v11-unestablished-null",
    "v11-unestablished-record",
    "v11-unestablished-list",
    "v11-unestablished-number",
    "v11-unestablished-flag",
    "v11-unestablished-empty",
    "v11-unestablished-whitespace",
    # V11 §3 — the renderer's order, and its non-vacuity control.
    "v11-renderer-order",
    "v11-renderer-order-control",
]

# The sinks the directions require, plus the four the V10 review found
# missing. `requests` is the owned journal; `fragmentIds` names the rows;
# `historyState` and `replacedStates` are the history-write evidence.
FIELDS = (
    "fetched", "requests", "fragmentCount", "fragmentIds", "tallyText",
    "statusWrites", "statusText", "busy", "activeElement", "released",
    "errorSections", "hash", "hashWrites", "replaced", "replacedStates",
    "historyState", "failureText", "fragmentTexts",
)

# The five facts a journal row states. Named here so the table below and any
# reader of the JSON agree on what a row is.
ROW_FIELDS = ("seq", "path", "kind", "phase", "outcome")


def project(snapshot, where):
    """The named sinks of one snapshot. A missing name is a hard failure."""
    missing = [name for name in FIELDS if name not in snapshot]
    if missing:
        raise SystemExit(
            "%s: the harness no longer emits %s; this dump would have "
            "silently reported them as null, which is the V10 defect"
            % (where, ", ".join(missing)))
    return {name: snapshot[name] for name in FIELDS}


def table(pages):
    """The owned journal as text: one line per request, in sequence."""
    lines = ["OWNED REQUEST JOURNAL — seq | kind | outcome | phase (owning "
             "step) | path",
             "Every request the page made, in the order it made it. `phase` "
             "is the step in",
             "force when the request was issued; `start` is the bootstrap, "
             "before any step ran.",
             "`outcome` is what became of it: completed, held (parked in "
             "flight), released",
             "(let go by a later step), or failed.",
             ""]
    for name in NAMES:
        page = pages.get(name)
        lines.append("== " + name)
        if page is None:
            lines += ["   (scenario not present in this test file)", ""]
            continue
        if "error" in page:
            lines += ["   ERROR: " + str(page["error"]), ""]
            continue
        for label, snapshot in page["snapshots"].items():
            lines.append("   -- snapshot: " + label)
            rows = snapshot.get("requests") or []
            if not rows:
                lines.append("      (no request recorded)")
            for row in rows:
                lines.append(
                    "      %3s | %-15s | %-9s | %-12s | %s"
                    % tuple(row.get(field, "?") for field in ROW_FIELDS[:1]
                            + ("kind", "outcome", "phase", "path")))
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__.strip().splitlines()[-1])
    spec = importlib.util.spec_from_file_location("catena_wave_1", sys.argv[1])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    pages = module.replayed()
    out = {}
    for name in NAMES:
        page = pages.get(name)
        if page is None:
            out[name] = "(scenario not present in this test file)"
        elif "error" in page:
            out[name] = {"error": page["error"]}
        else:
            out[name] = {
                label: project(snapshot, name + "/" + label)
                for label, snapshot in page["snapshots"].items()}
    print(table(pages))
    print()
    print(json.dumps(out, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
