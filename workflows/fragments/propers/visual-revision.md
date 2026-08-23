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
3. Rebuild the canonical and synthesis PDFs:
   ```
   make doc DOC={proper} PROVIDER={provider}
   make doc DOC={proper}-synthesis PROVIDER={provider}
   ```
4. Generate new review rasters and verify the visual issues are resolved.
5. Do not relitigate accepted work. Focus on the forwarded findings.

## Result

Return a worker result with `disposition: "PASS"`, the artifact paths, and a
summary listing each finding addressed and what was changed.
