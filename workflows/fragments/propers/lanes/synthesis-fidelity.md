# Lane: Derivation Fidelity

## Your lane

You own criteria **1 (Derivation fidelity)**, **2 (Evidence state carried
down)** and **3 (Redistillation, not abridgement)** of the shared criteria
above, and nothing else. The companion-conformance lane owns criterion 4; do
not report on it, and do not judge the work as a whole.

Read the canonical edition and the companion side by side, and answer only:

1. Does the companion assert anything the canonical edition does not?
2. Does every bound the canonical edition attaches to a claim travel with that
   claim into the companion?
3. Is the companion a redistillation rather than the canonical commentary
   copied or lightly compressed?

## Criterion 3 is measured, not felt

This class has a history. It was reported as an unowned observation at six
consecutive iterations of run `e4aebcbd941b6b1a` — by two different lanes,
both saying plainly that no criterion reached it — while the two editions were
authored and evaluated together and nothing could adjudicate it. The
sequencing that produced your packet is what makes it decidable, and it is
yours now.

Measure it rather than judging it by impression. Compare the companion's
prose against the canonical files it stands in place of, and against any
canonical section that renders in both. Report the proportion of the
companion's words that fall in verbatim runs long enough to be reuse rather
than coincidence, and name the longest run and where it sits. The run that
made this a criterion measured 36.8% of the companion's integrated commentary
in seven-word verbatim runs against the canonical element-by-element sweep,
with a 47-word run, and 12.7% against a section both editions render — and
none of it reached a repair owner.

A number alone is not a finding. Say what the reuse costs the reader: a claim
met twice at full strength in one sitting, a paragraph that walks the
appointed order where the companion promised an argument, a conclusion whose
working was reproduced instead of being left in the larger edition.

## Not yours: a count the companion's own text contradicts

A number the companion states that its own shorter enumeration does not bear
out belongs to the companion-conformance lane under criterion 4. That is so
even when the count was true of the canonical edition and became false in the
abridgement — especially then. Leave it there.

## Not yours: the canonical edition's own defects

The canonical edition passed a content evaluation before you were dispatched.
Where the companion faithfully carries a canonical error, the companion is not
what is wrong: record it under `observations`, naming both files, and do not
raise it as a blocking finding against a derivation that did its job.

## Result

Return an evaluator result for this lane. `PASS` when none of the three is
violated, `CHANGES_REQUIRED` with blocking findings when any is, `BLOCKED`
when a finding cannot be resolved by revision.

Record under `observations` anything real your criteria do not reach.

Finding IDs must use the `SYN-FID-` prefix and be stable across iterations.
