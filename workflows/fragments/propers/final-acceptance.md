# Final Acceptance

## Your task

Confirm that all prior stages have passed and that the proper guide is ready
for installation. This is the final gate before ACCEPTED.

## Steps

1. Verify that the canonical PDF exists at
   `build/{provider}/{proper}.pdf`.
2. Verify that the synthesis PDF exists at
   `build/{provider}/{proper}-synthesis.pdf`.
3. Confirm that `check-proper-components` passes:
   ```
   tools/tpt check-proper-components --provider {provider} --document {proper}
   ```
4. Confirm that generation metadata is valid:
   ```
   tools/tpt check-generation-metadata --provider {provider} \
       --pdf {proper} build/{provider}/{proper}.pdf
   ```
5. Confirm that the proper-components.toml manifest is consistent with the
   built artifacts.
6. Confirm that the brief synthesis two-page gate passed (checked via
   `check-proper-components --aux`).
7. Record any remaining concerns as advisory (non-blocking) findings.

## Note

Installation into `pdf/` is a separate operator action outside this workflow.
The workflow ACCEPTED state means the artifacts are validated and ready for
installation. Do not install PDFs during this stage.

## Result

Return a worker result with `disposition: "PASS"` and a summary confirming
all checks passed, with any advisory findings noted.
