# Lane: Profile Conformance

## Your lane

You own criteria **9 (Pagination)**, **10 (Provenance)** and **12
(Declarative discipline)** of the shared criteria list above, and nothing
else. Another lane owns each of the remaining criteria; do not report on
them, and do not judge the work as a whole.

Read the leaf's structure and its source records against the profile in
`guidance/liturgy/roman-1962-propers.md`, and answer only:

9. Does the content structure match the required reader order and page
   assignments from the profile?
10. Do the source records — `propers/verified.md`, `propers/retrieved.txt`,
    and `research/scope.md` — exist and follow the profile's format?
12. Does the reader-facing prose state its findings, or does it repeatedly
    narrate how the editors reasoned, what principles guided inclusion, why
    caution was necessary, what methodology governs the section, or why an
    interpretation is being presented at all? Weigh recurrence rather than a
    single sentence: a claim-local qualification that keeps a claim accurate
    is required by the profile, and so is the terminal apparatus. The habit
    counts the same whether it is written as a sentence, a run-in label, a
    standing per-entry field, or a table column. Read every reader-facing
    section: the four senses, `Scriptural Date and Location`, `Themes and
    Movement`, `Detailed Commentary`, the integrated commentary, the
    source-grounded synthesis, `Notable and Quotable`, and the proposals of
    `Interpretive Possibilities`. Out of scope, as qualification by design,
    are `Appendix: Scope and Qualifications`, `References`, and — within
    `Interpretive Possibilities` — the exploratory notice, the novelty
    classification, and the mandated controlling-limit field, however it is
    labelled. Page 2's required attribution, modern critical horizon,
    uncertainty and claim-local sources are never a finding, and neither are
    a gallery entry's required phrase, later user or work, exact locus and
    turn in meaning; what is a finding in those two sections is the audit's
    own apparatus printed for the reader — a dossier narrating the sheet's
    conduct, or a standing `Control` or `Rights and limit` block under every
    entry. A criterion 12 finding is `authoring`, and it is repaired by
    rewriting the sentence, never by deleting what it was about.

## Both editions are yours

The leaf builds more than one reader-facing document out of one source tree,
as the shared fragment above explains. Reader order and page assignment are
properties of a built document, so a second edition has its own and is judged
against the profile on its own; and a register that has moved into the body
may have moved into one edition's prose and not the other's, because the two
were written at different lengths. Read what every document renders, and name
in each finding the file the defect is in.

Criteria 9 and 10 are judged from the leaf's structure and its source
records. Criterion 12 is judged by reading the reader-facing prose itself:
open the sources that carry the sections named above and read what they
say, because a register that has moved into the body is visible nowhere
else. The mechanical gates measure the rendered pages — build success,
page counts, ordering, required blocks, undefined references — and you do
not rediscover what they check.

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

Return an evaluator result for this lane. `PASS` when none of the three is
violated, `CHANGES_REQUIRED` with blocking findings when any is, `BLOCKED`
when a finding cannot be resolved by revision.

Finding IDs must use the `CON-PRO-` prefix and be stable across iterations.
