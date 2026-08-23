# Build Canonical + Synthesis Artifacts

## Your task

Build the canonical (research) PDF and the synthesis PDF from the proper
leaf. Both are produced from the same source tree.

## Steps

1. Build the canonical PDF:
   ```
   make doc DOC={proper} PROVIDER={provider}
   ```
2. Build the synthesis PDF:
   ```
   make doc DOC={proper}-synthesis PROVIDER={provider}
   ```
3. Inspect the build logs for fatal errors, undefined references, overflow,
   and layout warnings.
4. Generate review rasters for visual inspection:
   ```
   tools/tpt pdf-review --output build/tpt-runs/<run-id>/artifacts \
       build/{provider}/{proper}.pdf build/{provider}/{proper}-synthesis.pdf
   ```
5. Verify both PDFs exist and are non-empty.
6. Record the build output paths.

## Note

The mechanical gates stage that follows will re-run build commands and
validate them programmatically. Your job here is to build, inspect the logs,
and report. If the build fails, report the failure in your summary so the
gate stage can catch it deterministically.

## Result

Return a worker result with `disposition: "PASS"`, the artifact paths
(canonical PDF and synthesis PDF), and a summary of the build results
including any warnings found in the logs.
