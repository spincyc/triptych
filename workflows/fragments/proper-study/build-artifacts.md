# Validate source outputs and selected print exports

Validate the bare document, `{proper}-synthesis`, and `{proper}-homily` as the
three declared outputs of one `publication.toml` owner:

    tools/document-schema check --provider {provider} --document {proper} --phase content --run-gates
    tools/document-schema identities --provider {provider} --document {proper}

Check actual source entrypoints, ordered components, dependencies, chronology,
metadata, and the upstream research, study, synthesis, and homily review closure.
Do not change accepted prose or evidence here. Report a source, schema, or
evidence defect to its earliest affected owner for fresh dependent review;
never refresh a seal to conceal changed inputs. Record concrete validation
results and source identities. The normal source/HTML run requires no TeX,
Poppler, PDF, raster receipt, or installed PDF mirror.

When the packet explicitly requests a print export, read `docs/printing.md` and
use `tools/print-document` for only the selected outputs. Keep fixed-point build
logs and exact exported bytes; reject fatal errors, undefined references,
overflow, unresolved layout warnings, invalid PDF structure, and missing fonts.
Apply every physical gate relevant to those outputs: the study's 20–50 pages,
the concise work's 10–12 pages, and its settled physical opening markers (map
and senses on 1, chronology on 2, themes on 3–4, commentary beginning on 5).
Logical counter resets, padding, and unreadable type cannot meet those gates.

Prepare bounded page rasters only with `tools/tpt pdf-review`, using a dedicated
replaceable `rasters` child beneath this stage and iteration's artifact area.
Keep logs, proofs, and other evidence outside that child. Record actual artifact
paths, hashes, page counts, log/font/extraction results, and limitations. A
receipt identifies bytes; it does not claim visual inspection. A fresh reviewer
must inspect every page of each selected export before it is called reviewed.
A format-only change follows print-template review scope; it does not renew or
invalidate unrelated source/evidence acceptance. Any changed PDF needs a new
exact-artifact review. Do not track or install generated PDFs for site release.
