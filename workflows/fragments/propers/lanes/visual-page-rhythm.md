# Lane: Page Rhythm

## Your lane

You own criteria **3 (Broken page rhythm)**, **5 (Bad table or callout
breaks)**, **6 (Stranded headings)**, and **7 (Sparse spill pages)** of the
shared criteria list above, and nothing else. Another lane owns each of the
remaining criteria; do not report on them, and do not judge the artifacts as
a whole.

Follow the shared inspection method: open every full-size page raster of both
the canonical and the synthesis PDF, and answer only:

3. Do page breaks disrupt the reading flow?
5. Are tables or callout boxes split across pages inappropriately?
6. Is a heading left at the bottom of a page with its content on the next?
7. Is a page nearly empty with only a few lines?

## Result

Return an evaluator result for this lane. `PASS` when none of these defects
is present, `CHANGES_REQUIRED` with blocking findings for each that is,
`BLOCKED` when a defect cannot be resolved by revision.

Finding IDs must use the `VIS-RHY-` prefix and be stable across iterations.
