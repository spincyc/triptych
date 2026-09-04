# Lane: Citation Integrity

## Your lane

You own criteria **7 (Citations)** and **8 (English rule)** of the shared
criteria list above, and nothing else. Another lane owns each of the
remaining criteria; do not report on them, and do not judge the work as a
whole.

Read every citation and every English rendering, and answer only:

7. Are only sources actually used cited? Is there any invented search,
   verification, quotation, attribution, doctrine, law, or historical fact?
8. Is English quoted from registered public-domain witnesses — Douay-Rheims
   Challoner for scripture, a registered public-domain hand missal for the
   orations? Is any English composed, translated, or adapted here?

## Both editions are yours

The leaf builds more than one reader-facing document out of one source tree,
as the shared fragment above explains. A citation or an English rendering
carried in each is two published instances of it: an invented attribution
corrected in one edition and left standing in the other is still published,
and a rendering composed rather than quoted is still composed in the edition
nobody opened. Read what every document renders, and name in each finding the
file the citation is in.

For an online citation defect, compare the leaf with the read-only
`research/scope.md` before assigning its repair. An exact title, responsible
creator or institution, edition or datestamp, stable URL, access date, or locus
that the repair requires must actually be present in the read-only brief before
the finding may name `authoring`. If a required value is absent, report that
evidence defect separately as `research`; if the brief holds the correct value
elsewhere but states it wrongly in its audit, report it separately as `brief`.
Keep a leaf-only omission in its own `authoring` finding rather than combining
different owners into one citation finding.

## Result

Return an evaluator result for this lane. `PASS` when neither criterion is
violated, `CHANGES_REQUIRED` with blocking findings when either is, `BLOCKED`
when a finding cannot be resolved by revision.

Finding IDs must use the `CON-CIT-` prefix and be stable across iterations.
