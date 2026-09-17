# Build all three artifacts for visual review

Build the bare document, `{proper}-synthesis`, and `{proper}-homily` with
`make doc DOC=<id> PROVIDER={provider}`. The Makefile owns fixed-point passes,
declared dependencies and metadata validation. Inspect all three logs and
extracted texts; resolve fatal errors, undefined references, overflow and
unresolved layout warnings. Check PDF structure and font embedding. Do not
change accepted prose or evidence here. Layout repairs may change presentation
but must preserve all content and source roles. Report semantic defects for
the visual reviewer to send upstream.

After the final builds, record the exact PDF and render-input snapshot:

    python3 scripts/_proper_study.py snapshot --provider {provider} --document {proper}

Generate bounded page rasters only with the repository helper:

    tools/tpt pdf-review --output build/tpt-runs/<run-id>/artifacts build/{provider}/{proper}.pdf build/{provider}/{proper}-synthesis.pdf build/{provider}/{proper}-homily.pdf

Use the actual run ID from the packet. Record artifact paths, page counts,
log/font/extraction results and remaining limitations in the production audit.
The helper writes `research/artifacts.json`; it records real bytes and declared
source inputs, never a claim of review. A fresh worker visually inspects every
page next. Do not install PDFs yet. On reentry, update render finalization
metadata after a layout change, rebuild every affected consumer, and replace
the snapshot only before the new visual review. Return the concrete outputs.
