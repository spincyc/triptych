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
]

FIELDS = (
    "fetched", "fragmentCount", "tallyText", "statusWrites", "statusText",
    "busy", "activeElement", "released", "errorSections", "hash",
    "hashWrites", "replaced", "failureText", "fragmentTexts",
)


def main() -> int:
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
                label: {field: snapshot.get(field) for field in FIELDS}
                for label, snapshot in page["snapshots"].items()}
    print(json.dumps(out, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
