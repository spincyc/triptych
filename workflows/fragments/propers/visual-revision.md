# Visual Revision

You are a reviser. The visual evaluator found blocking findings that must
be addressed. The PRIOR_FINDINGS in the packet header list each blocking
finding verbatim from the evaluator.

## Your task

Address each blocking visual finding. After making changes, rebuild the
artifacts. The workflow will re-run mechanical gates and then re-evaluate
visually, because any rebuild can invalidate downstream gates.

## Steps

1. Read each PRIOR_FINDING in the packet header.
2. For each finding, make the specific visual change required by its
   `required_result` field. This may involve:
   - Adjusting LaTeX page breaks (`\needspace`, `\pagebreak`)
   - Rewriting dense paragraphs
   - Restructuring tables
   - Moving headings
   - Adjusting spacing
3. Every repair step 2 admits lands in a file the document builds from, so
   bring `generation-metadata.tex` forward before you rebuild. Update
   `\AIDocumentRevisionTimestamp` to this revision, in the UTC whole-second
   form `YYYY-MM-DDTHH:MM:SSZ` the check requires, and append an
   `\AIModelContribution{model}{qualifiers}{runtime}` record for this pass, in
   the form the records already in the file use. Put it beside the records
   that carry the same model and qualifiers rather than at the end of the
   file: `check-generation-metadata` requires each model-and-qualifier group
   to be contiguous, and two agents of one production appended to a tail
   belonging to another group, failed the check, and had to move the record up
   beside its own. Leave `\AIGenerationProvenance` alone, since it names the
   run and not the pass. The declaration is what sets the built PDF's
   `ModDate` and prints the one "Last revised (UTC)" line the reader sees, so
   it has to move before the rebuild rather than after it. A rewritten
   paragraph or a moved heading under an unmoved timestamp is invisible to
   every gate downstream, which finds source and artifact consistent at the
   stale value: one leaf was published with a timestamp of 17:30 over sections
   revised at 18:08, because no fragment had told the reviser the file
   existed.
4. Rebuild the canonical and synthesis PDFs:
   ```
   make doc DOC={proper} PROVIDER={provider}
   make doc DOC={proper}-synthesis PROVIDER={provider}
   ```
5. Generate new review rasters and verify the visual issues are resolved.
6. Do not relitigate accepted work. Focus on the forwarded findings.

## Result

Return a worker result with `disposition: "PASS"`, the artifact paths, and a
summary listing each finding addressed and what was changed.
