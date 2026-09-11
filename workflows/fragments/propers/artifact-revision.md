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
3. Where the repair changed a file the document builds from, which a build
   repair ordinarily does, bring `generation-metadata.tex` forward before you
   rebuild. Update `\AIDocumentRevisionTimestamp` to this revision, in the
   UTC whole-second form `YYYY-MM-DDTHH:MM:SSZ` the check requires, and
   append an `\AIModelContribution{model}{qualifiers}{runtime}` record for
   this pass, in the form the records already in the file use. Put it beside
   the records that carry the same model and qualifiers rather than at the
   end of the file: `check-generation-metadata` requires each
   model-and-qualifier group to be contiguous, and two agents of one
   production appended to a tail belonging to another group, failed the
   check, and had to move the record up beside its own. Leave
   `\AIGenerationProvenance` alone, since it names the run and not the pass.
   The declaration is what sets the built PDF's `ModDate` and prints the one
   "Last revised (UTC)" line the reader sees, so it has to move before the
   rebuild rather than after it, and a repair that leaves it where it was is
   invisible to every gate downstream, which finds source and artifact
   consistent at the stale value. One leaf was published with a timestamp of
   17:30 over sections revised at 18:08, because no fragment had told the
   reviser the file existed.
4. Rebuild the canonical and synthesis PDFs.
5. Verify the fixes resolve the gate findings.

## Result

Return a worker result with `disposition: "PASS"`, the artifact paths, and a
summary listing each finding addressed and what was changed.
