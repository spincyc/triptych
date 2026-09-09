# Lane: Synthesis and Proposals

## Your lane

You own criteria **4 (Cross-proper synthesis)** and **5 (Exploratory
proposals)** of the shared criteria list above, and nothing else. Another
lane owns each of the remaining criteria; do not report on them, and do not
judge the work as a whole.

Read the synthesis and the interpretive possibilities, and answer only:

4. Is the synthesis a redistilled cross-proper argument rather than an
   abridged procession through the propers? Does each unit draw on more than
   one appointed element and more than one witness?
5. Is every exploratory proposal labeled as exploratory, and does each join
   at least two appointed elements? Does each carry all four of the fields
   the profile mandates for a proposal, under headings that state the fields
   the profile asks for?

## The mandated proposal fields are yours

Criterion 5 above names the four fields and requires each under a heading that
states the field the profile asks for. They come from one sentence of the
profile, the same sentence that requires the two joined elements you are
already checking, so they are the same criterion and not an extra one: check
every field of every proposal.

A proposal that prints a differently headed field in place of a mandated one
has dropped the mandated one. A real case: a proposal headed its third field
`The control the corpus supplies` and gave a genuine external control, while
`What the element-by-element reading misses` — the field the profile names,
which every other proposal in the same section carried — was absent. The
substitute was good material. The requirement was still unmet, and the
section no longer answers the same question of each proposal.

Judge the field by what it is asked to do rather than by its exact wording:
the profile says the limit field counts "however it is labelled", and the
same latitude applies to the others. A heading that plainly does the
mandated work satisfies it; a heading that does different work does not,
however good it is.

This is criterion 5 and not criterion 9 or 12. Reader order and page
assignment are properties of the built document and belong to the
profile-conformance lane; the fields inside a proposal are properties of the
proposal and belong to you. That split has cost a production already: this
lane found the missing field at three iterations and filed it as profile
conformance, the profile-conformance lane found it once and read it as
criterion 5, and it was repaired by neither.

## Not yours: a count the prose contradicts

A number a proposal or a synthesis unit states about its own material that
the enumeration under it does not bear out — `Six comparatives of degree in
four Latin constructions` followed by seven — is criterion 7 and belongs to
the citation-integrity lane. That is so even inside `The Propers:
Interpretive Possibilities`, which is otherwise your section, and even when
the count is the mechanism's own load-bearing observation. Your criterion 5
asks whether the proposal joins at least two elements and carries its
mandated fields; whether its arithmetic is right is asked once, in one lane,
across the whole guide. Do not report it, and do not withhold an otherwise
sound criterion 5 finding because a miscount sits in the same paragraph.

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

Finding IDs must use the `CON-SYN-` prefix and be stable across iterations.
