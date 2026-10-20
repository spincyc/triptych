# Expansive study author proof

Author-stage verification completed on 20 October 2026 for `proper-study` v13,
run `095fe00a9fe8cfee`, stage `author-study`, iteration 0. The canonical generation
record carries finalization time `2026-10-20T12:50:38Z` and the packet's exact
workflow digest and seed commit. This records author verification, not the later
independent content, visual or web review.

## Scope and extent

The canonical study treats the universal 1962 Roman Missal feast of Our Lord
Jesus Christ the King on 25 October 2026. It contains all eleven active proper
elements in full Latin and historical Lasance–Walsh English, detailed commentary,
and two developed whole-formulary interpretations. Each interpretation covers
all active elements and has its own literal, allegorical, moral and anagogical
distillation. Augustine and Jerome carry the first reading; Chrysostom and
Bellarmine carry the second. These are editorial constructions from their
particular exegetical arguments, not attributed ancient commentaries on this Mass.
The study includes the generated chronology orientation, five historical
discussions, the two inactive seasonal votive witnesses, scope and references.

The settled PDF has **23 physical pages**, including terminal apparatus, and
**7,612 substantive words**. The count uses Pandoc plain-text rendering of the
opening, detailed commentary, two interpretive components, concluding comparison
and historical appendix, after removing footnotes. It excludes full appointed
texts, inactive alternatives, terminal scope/references and generation colophon;
it includes expository headings and excludes custom-macro arguments discarded by
Pandoc. Component counts are 607, 1,606, 1,941, 1,973, 381 and 1,104 respectively.
The schema-2 manifest declares the future synthesis and homily components; those
companions have not been authored or reviewed at this stage.

## Source handling and limits

The appointed texts were transferred deterministically from this GPT leaf's
reviewed `propers/verified.md`. Comparison of all thirteen Latin and thirteen
historical-English blocks passed after whitespace and typographic normalization
(TeX escaping, cross glyph, response markers and emphasis). No new translation
was generated. The source record discloses an earlier Claude source-data
transcription lead independently checked against primary images; no other
provider's authored study prose or interpretation was reused. That provenance is
also disclosed in the printed scope appendix.

The full-text mode follows the reviewed research: manifest completeness is
`complete` and the canonical label is `Full PDF`. The source scope distinguishes
the 1962 controller from the historical English witness, preserves the witness's
printed errors, and limits its public-domain findings to the identified material,
not entire later facsimiles. Protected modern introductions and the modern papal
translation are used through original analysis, not reproduced bodies. The
received Victorinus attribution qualifications, incomplete NPNF Psalm 71 witness,
negative later-saint Apocalypse result, and unresolved chronology alternatives
remain visible. No new upstream evidence or rights claim was authored here; the
reviewed research records were not changed.

## Verification actually performed

- `make doc DOC=liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king PROVIDER=gpt`
  completed. The settled LaTeX log has no overfull/underfull boxes, warnings or
  undefined references. An intermediate label-change warning was resolved by
  the build's rerun. PDF metadata gives the correct title, date and subject;
  all listed Latin Modern fonts are embedded.
- The research-edition component content and artifact checks passed. The
  research-edition content preflight passed source bindings, chronology projection
  and supported claims, house voice, identifier resolution, used references,
  relation coverage, restricted-text and quotation checks.
- The native author-stage `tpt web-edition` probe passed using Pandoc and pinned
  Python Markdown 3.10.3. An earlier converter false positive treated PDF title
  metadata as a prose run; the driver repaired that shared audit and the author
  reran the native probe. No research or title was changed to evade that defect.
- The author inspected all 23 pages in regenerated contact sheets and inspected
  full-size title, appointed-text, interpretive-transition, chronology and final
  apparatus pages during layout proofing. Sparse forced-break spill pages were
  removed. A separated Postcommunion heading was moved with its text, and its
  final page was inspected again. The chronology table remains within its page;
  no clipping, overlap or missing text was observed. Text extraction and the
  source-block comparison supplement this visual inspection.

These checks do not replace the later shared-timestamp three-document build,
independent reviews or web acceptance. No human specialist or ecclesiastical
review is claimed. There were no prior, carried or advisory findings in this
packet, and no upstream blocker was identified during authoring.

## Exact proof for the cold reviewer

Built PDF:
`build/gpt/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king.pdf`.

Retained identical author proof:
`build/tpt-runs/095fe00a9fe8cfee/artifacts/author-study-0000/author-proof.pdf`.

SHA-256:
`42a95d5f8d2a5d682b788a8708da1facdeffeedcf81f86d0173e1f1a8eb8a1d6`.

The author-stage artifact directory holds build, preflight, artifact-gate and web
probe logs, extracted proof text and the measured text-verification record.
Raster evidence is in its replaceable `rasters` child; the converter output is
in its `web-probe` child. These paths are repository-relative, not machine paths.
