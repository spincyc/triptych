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
   against the edition itself? And does the leaf print the appointed Latin as
   the edition prints it?

## The appointed Latin, against `propers/verified.md`

`propers/verified.md` is the leaf's own record of what the typical edition
puts on the page, transcribed and re-read at the resolution its notes name.
Where the leaf prints the appointed Latin — the appointed-text section, the
page-1 map, the detailed commentary, the gallery, the proposals, the
synthesis edition's own prose — it must print what that record holds. An
acute the edition does not carry is the standing case: `confídere` and
`fídei` where the record says the accent is absent because it would fall on
the `i` of a `fi` ligature. Spelling and word division are checked the same
way.

This is criterion 2 and it is yours. It has fallen between lanes before,
because it looks like a quotation defect and quotations look like criterion 7
— but citation integrity asks whether a source is cited, honestly and as
used, and this asks whether the identified edition's own text was transcribed
faithfully. That is what verification from the edition itself means, and no
other lane's criteria reach it.

Read the record before the leaf, sweep every place the leaf prints the
affected text rather than the first, and name them all: they are one
departure from one edition, and a finding that names one place gets one place
repaired. Where the leaf agrees with `propers/verified.md` and it is the
record you believe is wrong about the edition, that is this criterion too;
say which of the two you checked and against what, because the answer decides
the repair owner and not the criterion.

## Not yours: a count the prose contradicts

A number stated in reader-facing prose that the list under it does not bear
out — `Five independent witnesses` heading four — is criterion 7 and belongs
to the citation-integrity lane. It stays there when the things being counted
are witnesses, sources, or evidence of any other kind: the class is divided
by defect and not by subject matter, so a miscount inside the evidence is
still a miscount. Do not report it, and do not treat its presence as an
evidence-state defect of your own.

## The canonical edition only

You read the document `main.tex` builds, and only that. The synthesis
companion is written later, by `derive-synthesis`, from whatever this
evaluation settles, and it is judged by its own lanes against the edition you
are reading. Where `main.tex` carries an `\ifdefined\TriptychSynthesisEdition`
branch, the arm that runs with the macro undefined is yours and the other arm
is not; nothing under `sections/synthesis/` is yours at all.

A defect that exists only in the companion is not a finding of yours. Raising
it here routes a repair to a stage that has not run, and the companion may not
even carry the passage once it is derived from the corrected canonical prose.

## Result

Return an evaluator result for this lane. `PASS` when neither criterion is
violated, `CHANGES_REQUIRED` with blocking findings when either is, `BLOCKED`
when a finding cannot be resolved by revision.

Record under `observations` anything real you saw that your own criteria do
not reach, on the terms the fragments above set out.

Finding IDs must use the `CON-EVI-` prefix and be stable across iterations.
