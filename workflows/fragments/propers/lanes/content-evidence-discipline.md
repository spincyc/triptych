# Lane: Evidence Discipline

## Your lane

You own criteria **1 (Evidence discipline)** and **2 (Source verification)**
of the shared criteria list above, and nothing else. Another lane owns each
of the remaining criteria; do not report on them, and do not judge the work
as a whole.

Read the canonical leaf and its research records, and answer only:

1. Are the five evidence states kept distinct throughout — verified source
   text, checked quotation or paraphrase, source-grounded synthesis,
   editorial or AI proposal, unverified lead? Is any claim presented at a
   higher evidence state than its record supports?
2. Are claims verified from primary, official, edition-identified sources?
   Are OCR text and secondary citations treated as leads until checked
   against the edition itself?

## Both editions are yours

The leaf builds more than one reader-facing document out of one source tree,
as the shared fragment above explains. A claim restated in a second edition
carries its own evidence state, and the short form that reaches only the
synthesis edition can stand a lead flat where the canonical prose bounded it.
Reading the canonical build alone would never show that. Read what every
document renders, and name in each finding the file the claim is in.

## Result

Return an evaluator result for this lane. `PASS` when neither criterion is
violated, `CHANGES_REQUIRED` with blocking findings when either is, `BLOCKED`
when a finding cannot be resolved by revision.

Finding IDs must use the `CON-EVI-` prefix and be stable across iterations.
