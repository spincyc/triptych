#!/usr/bin/env python3
"""THE GATE'S COUNTS, SO ITS TRANSCRIPT IS NOT EMPTY.

V12, the V11 review: the two browser `.log` members shipped at zero bytes.
The battery discarded the gate's stdout deliberately -- it is the same ~590KB
JSON the report member already carries, and shipping it twice is what this
discard exists to prevent -- but the note that explained the discard was
joined to the command with `&&`, so it printed only when the gate exited 0.
The gate exits 1 on this route's inherited failures, so the note never
printed and the transcript was empty exactly when there was something to
explain.

This prints the counts the reader wants from the report the gate did write,
so the transcript states what happened and points at the bytes that prove
it. Byte-stable: sorted keys, no timestamp.
"""

import json
import sys

report = sys.argv[1]
with open(report, encoding="utf-8") as handle:
    counts = json.load(handle).get("counts", {})
print("gate counts: " + json.dumps(counts, sort_keys=True))
