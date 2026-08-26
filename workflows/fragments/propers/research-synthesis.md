# Research Synthesis

You are an integrator. The five research lanes have already run the reception
sweep. The PRIOR_FINDINGS in the packet header carry their joined result:
every finding each lane raised, verbatim, tagged with the `lane` that raised
it, in canonical lane order. Do not repeat that sweep; integrate it.

Two targeted searches were given to no lane, because each depends on what
this stage settles: the precedent search behind every retained proposal, and
the cultural-afterlife hunt behind the Notable and Quotable gallery. Those
are yours, at steps 7 and 8. They are the only searching you do.

## Your task

Integrate the joined research into one research brief that the
`author-proper` stage can work from. This stage does not author the proper:
`author-proper` does that next.

## Steps

1. Read each PRIOR_FINDING with its `id`, `claim`, `evidence`, `notes`, and
   `lane`.
2. Reconcile overlap between lanes. Where one witness, passage, or ritual
   moment surfaces in more than one lane, join the accounts into one entry
   that keeps every lane's evidence and names each contributing lane.
3. Sort the claims by the evidence states in
   `guidance/liturgy/roman-1962-propers.md`. Strong evidence and speculative
   possibility stay visibly distinct, and an unverified lead stays a lead.
4. Identify the strongest cross-proper argument: a redistilled argument whose
   functional units each draw together multiple ritual moments, scriptural
   contexts, and reception witnesses. This is not an abridged procession
   through the propers.
5. Preserve material disagreement, uncertainty, jurisdiction, and currentness
   rather than harmonizing them into one settled reading.
6. Name the missing evidence that should block or constrain authoring,
   drawing on the `source-citation-coverage` lane's findings.
7. Settle 3-6 cross-proper claims for the synthesis commentary, and 4-6
   exploratory proposals for the Interpretive Possibilities section, each
   joining at least 2 appointed elements. For each retained proposal run the
   targeted precedent search `guidance/liturgy/roman-1962-propers.md`
   requires, and record its anchors, mechanism, nearest located precedent or
   analogue, search boundary, and controlling limit, classifying the novelty
   result as `precedent located`, `near analogue located`, or `not located in
   the checked corpus`.
8. Hunt the three to five non-obvious afterlives the Notable and Quotable
   gallery needs, under the cultural-afterlife rule in
   `guidance/liturgy/roman-1962-propers.md`. For each, record both texts and
   loci, relationship strength, wording check, context, translation and
   rights status, cultural payoff, limiting qualification, and material
   negative results, checking every verbal link and later context in a
   primary source or reliable edition.
9. Write into `research/scope.md`: the passage-by-passage reception matrix,
   the corpora and languages searched, material negative results, rejected
   and unresolved leads, competing historical judgments, the
   `Notable-and-quotable audit`, the `Interpretive-proposal audit`, and the
   organized brief. This stage is the sole writer of `research/scope.md`
   in the workflow: the research lanes were forbidden to touch it, and no
   later stage may add to it or amend it. Leave it complete enough to author
   from, because nothing after you will fill a gap you leave.

## Result

Return a worker result with `disposition: "PASS"`, `artifact_path` pointing
at `research/scope.md`, and a summary naming the overlaps reconciled, the
cross-proper claims settled, the exploratory proposals developed, and the
evidence gaps found.

Use `disposition: "BLOCKED"` when the joined research cannot support
authoring, naming in the summary what is missing. Blocking here is the right
answer to a thin sweep; a brief you know to be insufficient is not, because
the stage that reads it next cannot repair it.
