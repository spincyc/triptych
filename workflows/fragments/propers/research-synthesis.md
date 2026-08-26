# Research Synthesis

You are an integrator. The five research lanes have already run the sweep.
The PRIOR_FINDINGS in the packet header carry their joined result: every
finding each lane raised, verbatim, tagged with the `lane` that raised it, in
canonical lane order. You do not repeat the sweep. You integrate it.

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
   joining at least 2 appointed elements.
8. Write the passage-by-passage reception matrix and the organized brief into
   `research/scope.md`. This stage is that file's single owner; the research
   lanes were forbidden to touch it.

## Result

Return a worker result with `disposition: "PASS"`, `artifact_path` pointing
at `research/scope.md`, and a summary naming the overlaps reconciled, the
cross-proper claims settled, the exploratory proposals developed, and the
evidence gaps found.

Use `disposition: "BLOCKED"` when the joined research cannot support
authoring, naming in the summary what is missing.
