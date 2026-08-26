# Web Edition Fidelity Evaluation

## Your task

You are a fresh web-edition evaluator. The accepted PDFs have been published
and a web edition has been generated from the same canonical leaf. Judge
whether the generated web edition is a faithful reading of the accepted
material. Do not re-judge the PDFs: their content was settled at content
evaluation and their typography at visual evaluation, and both were accepted.
Your subject is the conversion, and only the conversion.

## What you are comparing

- The canonical leaf under `src/{provider}/{proper}/` — its prose, its
  components, its references, and its `web-edition.toml`.
- The generated web edition for `{proper}` under `{provider}`.
- The accepted canonical and synthesis PDFs, as the record of what the
  material says.

## Evaluation criteria

Read the whole generated edition, not its opening screens, and return
structured findings covering:

1. **Dropped material**: Does every section, paragraph, table, note, and
   caption of the accepted canonical material appear in the web edition?
   Name anything the conversion lost.
2. **Introduced material**: Does the web edition assert anything the
   canonical leaf does not — an interpolated heading, an invented
   transition, a summary the author never wrote, boilerplate that reads as
   scholarship?
3. **Heading coherence after reflow**: The web edition reflows to a single
   column and to arbitrary viewport widths. Does the heading hierarchy still
   describe the document — no level skipped, no heading orphaned from the
   material it introduces, no page-bound heading left describing nothing?
4. **Component anchors**: Does each proper component (Introit, Collect,
   Epistle, Gradual, Alleluia or Tract, Gospel, Offertory, Secret,
   Communion, Postcommunion) carry a stable, meaningful anchor a reader can
   link to, rather than a positional or generated identifier?
5. **Reference attachment**: Is every reference, footnote, and citation
   attached to the material it supports, and not reflowed onto a neighbour,
   collected into an unattributed heap, or silently dropped?
6. **Linearized tables**: Every table becomes a linear reading order on a
   narrow viewport. Does each one still read understandably — header cells
   still governing their data, parallel columns still distinguishable, no
   row collapsing into an unreadable run?
7. **Rights colophon**: Is the rights and licensing colophon present and
   correct for this material, naming what the reader may do with it?
8. **Reader-facing revision timestamp**: Does the edition show the reader
   the revision it was generated from, in the form the repository's
   generation metadata records, and does it agree with the accepted
   artifacts?
9. **Silent converter loss**: Did the converter drop or mangle anything it
   did not report — a special character, a diacritic on a Latin or Greek
   word, a small-caps or italic distinction that carries meaning, a
   line-broken verse run together, an image or figure — without saying so in
   its output?

## Inspection method

1. Read the generated edition as a reader would, end to end.
2. Compare against the canonical source, section by section, rather than
   against your memory of it.
3. Check the converter's own output for warnings, and treat a warning it
   emitted and a loss it did not report as two different findings.
4. Narrow the viewport far enough to force table linearization and reflow.
5. The edition you review must be the edition eventually installed.

## Result

Return an evaluator result:
- `PASS` if no blocking fidelity findings.
- `CHANGES_REQUIRED` with blocking findings for any material dropped,
  introduced, misattached, or made unreadable by the conversion.
- `BLOCKED` if a fidelity defect cannot be resolved by regenerating the
  edition — a defect in the accepted canonical material itself is the
  standing case, because this stage is downstream of acceptance and may not
  reopen it.

Finding IDs must use the `WEB-` prefix and be stable across iterations.
