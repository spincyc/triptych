# Derive the concise comparison

Read the accepted expansive study and write `synthesis.tex` and its components.
Import `common/preamble` then `common/propers-format`, using the shared title,
inventory, overview and dossier forms. Do not re-derive their layouts, change
fonts or margins, or import the homily column helper. Emit literal unconditional
component imports and keep literal markers in their declared source owners.
The finished PDF targets 10–12 physical pages. Restore the first four pages
specified in `guidance/liturgy/propers-three-documents.md`: page 1, complete
propers map and four senses overview; page 2, Scriptural Date and Location;
pages 3–4, The Propers: Themes and Movement. Developed interleaved commentary
begins on page 5. Declare the presentation component roles and place the
profile's physical-page zref markers around their actual content. No cover
may shift these positions. Use the same owner's reviewed generated chronology;
preserve its exact dates, alternatives, relation labels and unresolved states.
Use `chronology_presentation = "orientation-v2"` and the generated row interface
in `chronologyorientationtable` as the profile directs. Pair each passage with
the actual occurrence or dated subject, its place and concise date alternatives.
Consolidate identical answers; keep full evidence in the reviewed historical
appendix. Do not paste detailed annotation blocks or audit statuses into cells.

Write a standalone developed argument organized around cross-proper questions
or movements. Interleave the authors' alternatives where they address the same
question; a sequence of miniature lane summaries does not satisfy the task.
The first two thematic pages orient the reader; the later commentary earns
its extent by explaining and comparing witnesses' reasoning. The earlier
1,500–2,500-word and one-third ratio limits do not govern this revised contract.
The commentary must deepen the first two thematic pages through explanations
and comparisons the reader has not already been given. Fill the thematic pages
with textual detail and the Fathers' reasoning, not with sentences saying that
a text turns, orders or holds together the Mass; every reader sentence follows
`guidance/editorial.md`, "Say what the texts say, plainly", including its
warning against the flat opposite: orient the reader in the Mass's order,
translate Latin, and give a Father's point plainly where his exact words are
not needed. In reader prose the study's interpretations are interpretations,
not readings.

Preserve every interpretation's controlling claim, meaningful agreements and
differences, exact source attributions, and truth-changing qualifications.
Distinguish complementary emphases from real disagreement. Let the four senses
remain intelligible where their differences matter. Do not reproduce the full
study's commentary or apparatus simply to fill pages. Keep a useful terminal
source note, scope, timestamp and rights notice.

Add no new evidence-dependent claim. A missing argument or source is an
upstream defect to report, not permission to edit accepted research or study.
Maintain synthesis-only components and truthful mode membership in the common
manifest. Update the common generation timestamp and actual contribution
record, and record the substantive word count in the production audit. A
fresh reviewer compares this work both on its own and against its source study.

Build an author proof with
`make doc DOC={proper}-synthesis PROVIDER={provider}`. Run
`tools/check-proper-components --provider {provider} --document {proper} --phase artifacts --edition synthesis`
and inspect the settled PDF and physical-page
evidence. Give the reviewer exact PDF, auxiliary and log paths with hashes;
retain them beneath this run's stage/iteration artifact directory. Keep raster
evidence in a dedicated child because its helper replaces the destination.
An author proof does not replace the final three-document build or cold visual
review after the shared generation metadata has settled.
