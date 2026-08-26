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
4. Regenerate the web edition from the canonical leaf.
5. Verify each finding is resolved in the regenerated edition, and that
   nothing previously faithful has been lost.

## Result

Return a worker result with `disposition: "PASS"`, the regenerated edition's
path, and a summary listing each finding addressed and what was changed.

Return `disposition: "BLOCKED"` instead when a finding cannot be addressed
from this stage: a finding against the accepted canonical prose is the
standing case, because reopening accepted material is not a revision this
stage may make. Name the finding and why it is out of reach.
