# Lane: Clipping and Terminal Apparatus

## Your lane

You own criteria **9 (Clipping)**, **10 (Bad terminal apparatus)**, and **11
(Other visible defects)** of the shared criteria list above, and nothing
else. Another lane owns each of the remaining criteria; do not report on
them, and do not judge the artifacts as a whole.

Follow the shared inspection method: open every full-size page raster of both
the canonical and the synthesis PDF, and answer only:

9. Is any text or image cut off at the page margins?
10. Are the references, generation metadata, or scope sections poorly
    formatted or broken?
11. Is any other visual defect present that current Triptych guidance defines
    in `guidance/editorial.md` or `guidance/repository.md`, and that no other
    lane above owns?

## Result

Return an evaluator result for this lane. `PASS` when none of these defects
is present, `CHANGES_REQUIRED` with blocking findings for each that is,
`BLOCKED` when a defect cannot be resolved by revision.

Finding IDs must use the `VIS-APP-` prefix and be stable across iterations.
