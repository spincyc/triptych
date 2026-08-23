# Artifact Revision

You are a reviser. The mechanical artifact gates found blocking findings
that must be addressed. The PRIOR_FINDINGS in the packet header list each
blocking finding verbatim from the gate.

## Your task

Address each blocking finding from the gate. Rebuild the affected artifacts
after making changes.

## Steps

1. Read each PRIOR_FINDING in the packet header.
2. For each finding, fix the underlying issue (build failure, missing
   artifact, etc.) as specified by its `required_result` field.
3. Rebuild the canonical and synthesis PDFs.
4. Verify the fixes resolve the gate findings.

## Result

Return a worker result with `disposition: "PASS"`, the artifact paths, and a
summary listing each finding addressed and what was changed.
