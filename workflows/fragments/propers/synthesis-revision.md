# Synthesis Companion Revision

You are a reviser. The synthesis evaluation raised blocking findings against
the companion. The PRIOR_FINDINGS header lists each one verbatim; where
CARRIED_FINDINGS is not empty it holds further blocking findings against work
this stage owns that reached no owner earlier. Both are yours.

The ADVISORY_FINDINGS header holds findings the evaluation deliberately did
not block on. They gate nothing and are owed no entry in
`finding_dispositions` — naming one there is refused. Clear the ones you can
while you are already in those files, and leave the rest.

## What you may change

The companion, and only the companion: `synthesis.tex`, the
`\ifdefined\TriptychSynthesisEdition` branches in `main.tex`, and the files
under `sections/synthesis/`. `proper-components.toml` where the manifest must
follow.

**The canonical edition is settled and you may not revise it.** It passed a
content evaluation before the companion was derived. If a finding can only be
cleared by changing canonical prose, report it `not-repaired` with a note
saying so — that is the honest answer and it costs the run nothing it should
not cost. Editing settled canonical prose to clear a companion finding would
put unevaluated changes into the larger edition, which is the direction this
pipeline exists to prevent.

You may not write `research/scope.md` either, at any severity: the research
brief is immutable here and `research-synthesis` is its only writer. You may
not write `propers/verified.md` or `propers/retrieved.txt`.

## Steps

1. Read each PRIOR_FINDING and each CARRIED_FINDING in the packet header.
2. Make the specific change each `required_result` states. Do not paraphrase
   or reinterpret a finding; address it as written.
3. Where clearing a finding would require canonical prose to change, stop and
   report that finding `not-repaired` with the reason.
4. Read ADVISORY_FINDINGS and clear what is plainly stated and local.
5. Rebuild both editions and confirm the canonical build is unchanged in page
   count and reader order. A companion repair that moves the canonical
   edition's pages has edited something it should not have.

## Result

Return a worker result with `finding_dispositions`: exactly one entry per
forwarded blocking finding, `repaired` or `not-repaired`, with a note on each
`not-repaired`.

`not-repaired` is a legitimate outcome and reporting it is not a failure. It
is the only channel through which the engine learns whether repair is working,
because a fresh evaluator re-reading a changed document sees defects and not
the history of attempts on them. A production's central defect survived three
rounds because every round reported it repaired.
