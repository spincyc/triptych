# Lane: Density and Hierarchy

## Your lane

You own criteria **1 (Crowding)**, **2 (Weak hierarchy)**, and **4 (Poor line
lengths)** of the shared criteria list above, and nothing else. Another lane
owns each of the remaining criteria; do not report on them, and do not judge
the artifacts as a whole.

Follow the shared inspection method: open every full-size page raster of both
the canonical and the synthesis PDF, and answer only:

1. Is any page too dense to read comfortably?
2. Are headings, sections, and body text visually distinguishable?
4. Are lines too long or too short for comfortable reading?

## Result

Return an evaluator result for this lane. `PASS` when none of these defects
is present, `CHANGES_REQUIRED` with blocking findings for each that is,
`BLOCKED` when a defect cannot be resolved by revision.

Finding IDs must use the `VIS-DEN-` prefix and be stable across iterations.
