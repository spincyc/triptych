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

# Concise study author proof

Completed 20 October 2026 for `proper-study` v13, run `095fe00a9fe8cfee`,
`derive-synthesis`, iteration 0. The shared generation record now carries
`2026-10-20T13:07:28Z` and the actual concise-author contribution. This section
records author verification, not cold concise acceptance or the final visual
review of the three documents after their shared metadata settles.

## Derived argument and extent

The concise study, *Hearing and Peace*, derives from the accepted expansive
study and its reviewed evidence. It preserves both controlling claims: the King
makes a people capable of hearing him, and the Creator restores communion by
giving himself. Five cross-proper questions interleave Augustine, Jerome,
Chrysostom and Bellarmine at the points where their arguments meet. The
commentary develops the grace/hearing order, received human dominion and
uncreated primacy, heavenly reconciliation, differing readings of Psalm 71's
opening and universal homage, and peace amid adversity and chosen enmity.
The overview and commentary retain the four senses and the distinct consequences
of the two readings. Victorinus's received-text qualifications and the difference
between universal authority, voluntary obedience and final acknowledgment remain.

The settled proof has **10 physical pages** and **4,139 substantive words**:
170 in the inventory, 74 in the four-sense overview, 954 in the thematic movement
and 2,941 in developed commentary. The count follows the expansive proof's
method: Pandoc plain-text rendering with footnotes removed, including headings
and excluding chronology, terminal scope/references and the generation colophon;
custom-macro arguments discarded by Pandoc are excluded. The counted components
and exact method are retained in the artifact's `word-count.json`.

The existing manifest already declared six synthesis-only components, their
presentation roles and truthful mode membership. They are now authored and
imported literally and unconditionally by `synthesis.tex`. No manifest change
was necessary. All eleven active elements appear in liturgical order. The
chronology imports the reviewed generated definitions once and uses all nine
`orientation-v2` rows unchanged, with short sourced place descriptions and
precise H1--H5 references to the expansive historical appendix. The Daniel
duration, Davidic attribution, composition alternatives, unresolved Psalm
occasions and unresolved trial date remain distinct. No new evidence-dependent
claim, chronology assertion or source binding was added. Accepted study and
research content was not revised; only this production audit and the shared
generation record changed among existing files.

## Checks and physical inspection

- The specified `make doc` synthesis build completed. The settled log has no
  warnings, overfull or underfull boxes, or undefined references. The PDF title,
  subject and revision date are correct; every listed Latin Modern font is
  embedded. The PDF is 406,442 bytes, below both size-review triggers.
- Synthesis component content and artifact checks passed. The auxiliary labels
  place inventory and overview, including exactly four sense markers, on physical
  page 1; chronology begins and ends on page 2; themes begin on 3 and end on 4;
  developed commentary begins on 5. Commentary fills pages 5--9, and scope,
  references, timestamp and compact rights colophon share page 10.
- The complete synthesis content preflight passed: source bindings, current
  chronology record and annotations, supported chronological claims, house
  voice, identifiers, used references, relation coverage, restricted-text and
  quotation checks, and structural labels. The references check reported seven
  used entries and all three mechanically held loci cited in the body.
- All ten rendered pages were inspected at full-page scale. The initial
  eleven-page proof had a short terminal spill; concise scope wording removed
  it without dropping its material qualifications or altering fonts, margins,
  shared formats or the substantive argument. The final page was reinspected.
  No clipping, overlap, broken headings or rights-only page remains.
- The page-2 lookup was exercised directly: John 18:33--37 pairs the Jerusalem
  interrogation with its unresolved event date and separately pairs the Gospel's
  traditional Ephesus writing frame with both generated composition ranges;
  Colossians distinguishes the prison setting from Colossae; the Introit's
  Apocalypse clauses have their own composition row, separate from its Psalm.
  The three Psalm rows separately identify attribution, occasion and composition.
  The generated repeated passage lists are long but readable; no local
  substitution or edited date shortens them.

There were no forwarded blocking, carried or advisory findings to dispose of.
No upstream blocker was identified. These checks do not install the proof or
replace the remaining independent reviews, final three-document build or
publication gates. Global source-inventory/family refresh and `make check-sources`
remain with the parent integration driver; this stage did not mutate those
shared records.

## Exact concise proof for the cold reviewer

Built source artifact:
`build/gpt/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king-synthesis.pdf`.
The retained proof is byte-identical. The following files are under
`build/tpt-runs/095fe00a9fe8cfee/artifacts/derive-synthesis-0000/`:

| File | SHA-256 |
| --- | --- |
| `author-proof.pdf` | `12a6afdfd04679772bba99a662c4a9fd09086d8442176ec396737c9d322dd0e9` |
| `author-proof.aux` | `fc869f5656388d79f742546941ab414e9338201a0da760450138901cfa54054a` |
| `author-proof.log` | `1675e6711b04ba4dc6a2c8abcdb0db8c17b8a91a23eae490e0201d656a85efb4` |

The same directory retains the build, component and preflight logs, extracted
text, font report and word-count record. The replaceable `rasters/` child holds
all page images and the contact sheet. The stable proof and logs sit outside
that child. The later homily's shared timestamp will require the final common
build and visual review; these bytes remain the exact concise author proof.
