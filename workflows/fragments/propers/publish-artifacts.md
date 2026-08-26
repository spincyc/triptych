# Publish the Accepted PDFs

## Your task

Install the two accepted PDFs from the build tree into the tracked
publication tree. Artifact acceptance is behind you: `final-acceptance`
rechecked the canonical PDF, the synthesis PDF, the component manifest, and
the generation metadata on the artifacts as they now stand, and passed. This
stage moves those exact artifacts into `pdf/{provider}/` and changes nothing
about them.

Do not rebuild, retypeset, or edit the leaf. A rebuild here would install an
artifact nothing has accepted, and the accepted artifact would be the one
left behind.

## Steps

1. Install the canonical PDF:
   ```
   make install-doc DOC={proper} PROVIDER={provider}
   ```
2. Install the synthesis PDF:
   ```
   make install-doc DOC={proper}-synthesis PROVIDER={provider}
   ```
   The install rule verifies each PDF against its metadata stamp before
   copying, so a mismatch between the build tree and the validated artifact
   stops the install rather than publishing past it.
3. Confirm both installed files exist and are byte-identical to the accepted
   builds:
   ```
   cmp build/{provider}/{proper}.pdf pdf/{provider}/{proper}.pdf
   cmp build/{provider}/{proper}-synthesis.pdf \
       pdf/{provider}/{proper}-synthesis.pdf
   ```
4. Record the two installed paths.

## Note

The publication gates at the end of this phase re-verify the installed
artifacts programmatically, including the component manifest and the
generation metadata against the installed canonical PDF. Your job here is to
install, verify, and report. If an install fails, report the failure in your
summary rather than working around it.

## Result

Return a worker result with `disposition: "PASS"`, `artifact_path` set to
`pdf/{provider}/{proper}.pdf`, and a summary naming both installed paths and
the result of each `cmp`.

Return `disposition: "BLOCKED"` when an install cannot be completed — a
metadata stamp that does not match the current PDF is the standing case,
because it means the artifact in the build tree is not the artifact that was
validated, and that is not repairable from this stage.
