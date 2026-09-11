# Web Edition Revision

You are a reviser. The web-edition evaluator found blocking fidelity findings
that must be addressed. The PRIOR_FINDINGS in the packet header list each
blocking finding verbatim from the evaluator.

## Your task

Address each blocking finding and regenerate the web edition. Repair the
conversion, not the accepted material: the canonical prose was accepted at
content evaluation and the artifacts at final acceptance, and this stage is
downstream of both. A finding that can only be answered by rewriting the
accepted prose is out of reach from here.

## Steps

1. Read each PRIOR_FINDING in the packet header.
2. For each finding, make the specific change required by its
   `required_result` field. The repair belongs in one of:
   - `src/{provider}/{proper}/web-edition.toml`, where the edition declares
     what it includes, how it is ordered, and how it is titled
   - the canonical leaf's markup, where a construct the converter cannot
     carry needs a form it can
   - the component anchors, where an anchor is positional or absent
3. Do not add prose the canonical leaf does not carry, and do not delete
   material to make a finding go away.
4. Where the repair reached a file the built document inputs — the canonical
   leaf's markup does, and so do the anchors, which are its labels and its
   headings, while `web-edition.toml` and the generated edition do not — bring
   `generation-metadata.tex` forward. Update `\AIDocumentRevisionTimestamp`
   to this revision, in the UTC whole-second form `YYYY-MM-DDTHH:MM:SSZ` the
   check requires, and append an
   `\AIModelContribution{model}{qualifiers}{runtime}` record for this pass, in
   the form the records already in the file use and beside the records that
   carry the same model and qualifiers rather than at the end of the file:
   `check-generation-metadata` requires each model-and-qualifier group to be
   contiguous, and two agents of one production appended to a tail belonging
   to another group, failed the check, and had to move the record up beside
   its own. Leave `\AIGenerationProvenance` alone, since it names the run and
   not the pass. Where the repair stayed in `web-edition.toml` or in the
   generated edition, the built document did not change and this file is left
   exactly as it is: a timestamp moved for a change no artifact carries is a
   false record, and the publication gate refuses it.
5. Regenerate the web edition from the canonical leaf.
6. Verify each finding is resolved in the regenerated edition, and that
   nothing previously faithful has been lost.

## When the repair reaches the built document

This stage is downstream of both acceptances and rebuilds nothing. The two
PDFs were built, gated, evaluated and installed before this packet was
compiled, so a repair in the canonical leaf's markup leaves them behind, and
tracked source that no longer builds the published artifact is the one state
the acceptance apparatus exists to prevent. Bringing the revision timestamp
forward is what keeps such an edit from being silent: the publication gate
runs `check-generation-metadata` against the *installed* PDF and compares its
`ModDate` and its one rendered "Last revised (UTC)" line with the source's
`\AIDocumentRevisionTimestamp`, so a source that has moved past the artifact
is refused there and reaches a person, where an unmoved timestamp leaves both
sides consistent at the stale value and nothing downstream can see the
change. Name in your summary every file the built document inputs that you
changed, and say that the installed artifacts predate it.

## Result

Return a worker result with `disposition: "PASS"`, the regenerated edition's
path, and a summary listing each finding addressed and what was changed.

Return `disposition: "BLOCKED"` instead when a finding cannot be addressed
from this stage: a finding against the accepted canonical prose is the
standing case, because reopening accepted material is not a revision this
stage may make. Name the finding and why it is out of reach.
