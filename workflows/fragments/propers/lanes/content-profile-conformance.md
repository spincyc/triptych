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
    interpretation is being presented at all? Criterion 12 above states the
    boundary in full, and it is the boundary: the out-of-scope list is the
    whole of it, recurrence rather than a single sentence is the test, and the
    habit counts the same written as a sentence, a run-in label, a standing
    per-entry field or a table column. A criterion 12 finding is `authoring`,
    and it is repaired by rewriting the sentence, never by deleting what the
    sentence was about.

## Criterion 12's scope, and why this lane is told twice

The sections criterion 12 names are where to start reading and not where to
stop: a reader-facing section that list does not happen to name is in scope all
the same. List the leaf's own inputs and read what it actually builds.

The complete appointed text is spelled out there because a checklist like it
once left that section out, and the omission put a real defect at the mercy of
how one lane read a list. In run `90dcdddcb6780e60` this lane raised the
section's English-gap blocks under criterion 12 while the fragment's list of
sections did not name it and its never-a-finding exceptions did not cover it.
The lane had to settle two questions the fragment left open — whether the
section was in scope at all, and which half of an English-gap block the profile
asks for — and it settled both correctly; the leaf was repaired. Nothing made
that the only available reading. The same list read as a boundary excludes the
section outright, a lane that read it that way would have been just as
defensible, and the defect would have stood. The fragment was at fault, and it
says one thing now.

The terms are the terms of page 2 and the gallery. What the profile requires is
narrow — `guidance/liturgy/roman-1962-propers.md` lines 225-227: where no
public-domain English exists for an element, say so, give the Latin incipit,
describe what the prayer asks, and supply no rendering of the project's own.
Where a leaf goes further and states what the registered English leaves of the
Latin unanswered, that is a fact about the two texts and never a finding. What
is a finding is the block turning from the two texts to the guide's handling of
them: `so they are printed whole with the sung portion marked`, `it stands
bracketed above in the missal's own Latin and untranslated`, `the doxology cue
is not translated here`. Say what the Latin has and the English has not, and
the handling follows without narration. One such clause is not the defect; a
block that narrates its own procedure at every element is.

## Not yours: whether a proposal carries its mandated fields

Whether a proposal carries the fields the profile mandates is criterion 5 and
the synthesis-argument lane's. Your interest in those fields is register
alone — the notice, the novelty classification and the controlling-limit field
are out of scope for criterion 12 as qualification by design, and the
mechanism, the fruit and the `misses` field are in scope for their register
like any other prose. So a proposal printing `The control the corpus supplies`
where the profile asks for `What the element-by-element reading misses` is that
lane's finding and not yours, however plainly it reads as a departure from the
profile you have open. Reading the profile more closely than the other lanes do
is what this lane is for, which is exactly why this has to be said: the defect
was reported to nobody for three iterations because that lane called it profile
conformance and this lane called it criterion 5.

    Audit the structural labels separately from that recurrence judgment. A
    thesis may open directly as prose, but a reader-facing heading, box title,
    run-in label, or table heading called `Governing thesis`, `Thesis`, `Key
    takeaway`, `Argument map`, `Reading order`, or an equivalent rhetorical or
    editorial wrapper is categorically forbidden. One occurrence is a
    blocking criterion 12 finding with `repair_target: "authoring"`; do not
    wait for it to recur, count it as process prose, or excuse it because a
    prior leaf uses the same scaffold. Name the file and the structural
    surface in the finding. Legitimate authority, attribution, safety,
    contrast, accessibility, and profile-mandated semantic fields are not
    rhetorical meta-labels.

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
open every source either document inputs and read what it says, because a
register that has moved into the body is visible nowhere else. The checklist
above says where to start, not where to stop. The mechanical gates measure
the rendered pages — build success, page counts, ordering, required blocks,
undefined references — and you do not rediscover what they check.

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

Record under `observations` anything real you saw that your own criteria do
not reach, on the terms the fragments above set out.

Finding IDs must use the `CON-PRO-` prefix and be stable across iterations.
