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
   at least two appointed elements?

## Both editions are yours

This lane meets that fact most directly. The leaf builds more than one
reader-facing document out of one source tree, as the shared fragment above
explains, and the second is commonly the synthesis itself — rendered from
section files the canonical build never inputs, or from prose a
`\ifdefined\TriptychSynthesisEdition` branch fences off. Reading `main.tex`
alone can leave the very synthesis you are judging unread. Read what every
document renders, and name in each finding the file the defect is in.

## Result

Return an evaluator result for this lane. `PASS` when neither criterion is
violated, `CHANGES_REQUIRED` with blocking findings when either is, `BLOCKED`
when a finding cannot be resolved by revision.

Finding IDs must use the `CON-SYN-` prefix and be stable across iterations.
