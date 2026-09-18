# Build all three artifacts for visual review

Build the bare document, `{proper}-synthesis`, and `{proper}-homily` with
`make doc DOC=<id> PROVIDER={provider}`. The Makefile owns fixed-point passes,
declared dependencies and metadata validation. Inspect all three logs and
extracted texts; resolve fatal errors, undefined references, overflow and
unresolved layout warnings. Check PDF structure and font embedding. Verify
the required 20–50-page study, 10–12-page concise work and settled physical-page
markers for the concise opening: map and senses on 1, chronology on 2,
themes on 3–4, commentary beginning on 5. No logical counter reset can supply
missing physical pages. Keep the concise auxiliary and log evidence with the
final PDFs for the artifact snapshot and gate. Do not
change accepted prose or evidence here. Layout repairs may change presentation
but must preserve all content and source roles. Any such source edit invalidates
the affected content review: the following artifact gate checks the completed
research, study, synthesis and homily seals and routes changed bytes to the
earliest affected author, followed by fresh dependent reviews and a new build.
Record the exact layout edits; never refresh a content seal or describe an old
approval as current. Report semantic defects for
the visual reviewer to send upstream.

After the final builds, record the exact PDF and render-input snapshot:

    python3 scripts/_proper_study.py snapshot --provider {provider} --document {proper}

Generate bounded page rasters only with the repository helper:

    tools/tpt pdf-review --output build/tpt-runs/<run-id>/artifacts/build-artifacts-<iteration>/rasters build/{provider}/{proper}.pdf build/{provider}/{proper}-synthesis.pdf build/{provider}/{proper}-homily.pdf

Use the actual run ID and this stage's iteration from the packet. The helper
replaces its entire output directory: keep logs, author proofs and other review
evidence outside this dedicated raster child. Record artifact paths, page counts,
log/font/extraction results and remaining limitations in the production audit.
The helper writes `research/artifacts.json`; it records real bytes and declared
source inputs, never a claim of review. A fresh worker visually inspects every
page after the upstream seals and artifact checks pass. Do not install PDFs yet.
On reentry, update render finalization
metadata after a layout change, rebuild every affected consumer, and replace
the snapshot only before the new visual review. Return the concrete outputs.
