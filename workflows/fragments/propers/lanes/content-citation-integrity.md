# Lane: Citation Integrity

## Your lane

You own criteria **7 (Citations and stated counts)** and **8 (English rule)**
of the shared criteria list above, and nothing else. Another lane owns each
of the remaining criteria; do not report on them, and do not judge the work
as a whole.

Read every citation, every stated count, and every English rendering, and
answer only:

7. Are only sources actually used cited? Is there any invented search,
   verification, quotation, attribution, doctrine, law, or historical fact?
   Does every number the prose states about its own material agree with the
   material it heads?
8. Is English quoted from registered public-domain witnesses — Douay-Rheims
   Challoner for scripture, a registered public-domain hand missal for the
   orations? Is any English composed, translated, or adapted here?

## Counting is part of criterion 7

A count the guide states about its own material is a fact the guide asserts,
and it is checked the way every other asserted fact is: against what is
there. `Five independent witnesses converge on the antiphon being secondary`
above a passage that produces four is a false statement about the evidence,
whether the fifth witness was dropped in revision or never existed. `Six
comparatives of degree in four Latin constructions` followed by seven
enumerated comparatives is a false statement about the appointed Latin.
Neither is a stylistic slip; each tells the reader something the guide cannot
support, and a reader who counts finds it in seconds.

So count. When a sentence announces a number — of witnesses, manuscripts,
appointed elements, textual features, senses, proposals, occurrences,
departures, divisions — count what follows and check the two agree. Do the
same for a total set against rows, a `both` against a list of three, an
`only` against a second instance elsewhere in the same section. This runs
through every reader-facing section and both editions, not only the sections
where citations cluster, and the two editions were written at different
lengths: a count that was true of the full commentary is routinely false of
the abridged one that inherited the sentence.

The class is divided by defect and not by subject matter. It is yours when
the things counted are patristic witnesses, and yours when they are Latin
constructions inside an exploratory proposal. It was lost for a whole
production because the lane that saw it in the commentary judged it outside
its own criteria, and the two lanes that saw it in the proposals both judged
it an arithmetic question owned elsewhere. It is owned here.

Report a miscount as its own finding rather than folding it into a citation
finding beside it: the repair is different, and one `required_result` that
asks for two unrelated corrections gets one of them. Say in
`required_result` which of the two you believe is wrong, the number or the
list, and on what — the reviser cannot tell from the finding alone whether a
witness went missing or was never there. A miscount is ordinarily
`authoring`: the sentence and the list it heads are both in the leaf, and one
of them is wrong. It is `research` only where the count could not be made
true without evidence the brief does not hold — where the fifth witness would
have to be retrieved before it could be either printed or given up.

## Not yours: the Latin's accents and spelling

Whether the leaf prints the appointed Latin as the identified edition prints
it — an acute on `confídere` or `fídei` where `propers/verified.md` records
the edition printing it bare, a spelling, a word division — is criterion 2,
and the evidence-discipline lane owns it. Transcription fidelity to the
edition is verification, not citation: your criterion asks whether a source
is cited and cited honestly, and that one asks whether the edition's own text
was copied faithfully. Leave it there. It reached nobody once because this
lane found it, correctly judged it criterion 2's, and had no way to say so;
its owner is now explicit in that lane's fragment, so pass it by.

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

Record under `observations` anything real you saw that your own criteria do
not reach, on the terms the fragments above set out.

Finding IDs must use the `CON-CIT-` prefix and be stable across iterations.
