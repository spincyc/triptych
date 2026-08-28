# Lane: Profile Conformance

## Your lane

You own criteria **9 (Pagination)** and **10 (Provenance)** of the shared
criteria list above, and nothing else. Another lane owns each of the
remaining criteria; do not report on them, and do not judge the work as a
whole.

Read the leaf's structure and its source records against the profile in
`guidance/liturgy/roman-1962-propers.md`, and answer only:

9. Does the content structure match the required reader order and page
   assignments from the profile?
10. Do the source records — `propers/verified.md`, `propers/retrieved.txt`,
    and `research/scope.md` — exist and follow the profile's format?

Judge the source structure only. The mechanical gates measure the rendered
pages; do not rediscover what they check.

This lane reads the profile more closely than any other, so it is the lane
most likely to find that the profile itself is at fault rather than the leaf.
It has happened: the profile states its macro-order twice and the two
statements cannot both be satisfied, and a leaf that takes the only jointly
satisfiable reading is right while the document governing it is wrong. When
the leaf conforms as well as anything could to a profile that contradicts
itself, that is not a leaf defect and it is not a note either. Raise it with
`severity: "escalation"` and `escalated_to` naming the guidance file and the
lines that disagree, exactly as the shared fragment above describes. Say in
`required_result` which readings could reconcile it, and leave the leaf alone.
Your lane still returns `PASS`: the leaf met your criteria, and the escalation
rides alongside that pass.

## Result

Return an evaluator result for this lane. `PASS` when neither criterion is
violated, `CHANGES_REQUIRED` with blocking findings when either is, `BLOCKED`
when a finding cannot be resolved by revision.

Finding IDs must use the `CON-PRO-` prefix and be stable across iterations.
