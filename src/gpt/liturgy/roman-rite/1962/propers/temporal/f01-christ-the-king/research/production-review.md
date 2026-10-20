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

# Homily author proof

Draft finalized 20 October 2026 for `proper-study` v13, run `095fe00a9fe8cfee`,
`derive-homily`, iteration 0, with shared revision `2026-10-20T13:20:44Z`.
The homily, *Learning to Hear the King*, addresses an adult parish assembly.
The stable source checkpoint precedes author build and the independent reviews.

## Argument, delivery and decisive detail

The speech develops the accepted hearing-king interpretation, with its compatible
sacrificial-peace application from reconciled-creation. It begins with Jesus and
Pilate in the governor's hall and returns to that scene at the end. Augustine's
distinction between a kingdom not *of* the world and one absent *from* it is the
decisive textual detail: a hearer expecting kingship to mean the prisoner's
ability to command a rescue is led instead to ask how grace makes people capable
of obedient hearing within their existing responsibilities. John 18:37's order of
belonging and hearing, Colossians' rescue and fitness for inheritance, and the
Secret's petition to the sacrificial giver of peace carry the inference into
conversion and Eucharistic participation. The practical response concerns a
specific correction or resentment. The Communion and Postcommunion lead from
received peace through adversity toward perseverance and shared reign.
Replacing the readings with unrelated texts would remove the origin/presence
distinction, truth/hearing order, rescue/fitness argument and sacrificial means
that make this response intelligible.

The body has **1,276 spoken words**, measured by whitespace-separated word count
of the prose-only component; it contains no TeX commands, footnotes, headings or
stage directions. At **110–125 words per minute**, calculated delivery is
**10.2–11.6 minutes**, approximately 10–12 minutes. Silent reading checked sense,
transitions, pronoun references and oral clarity. No audible rehearsal, timed
human delivery, personal experience or clerical identity is claimed. Practical
examples are applications, not historical anecdotes or patristic quotations.
The ending is exhortation, with no newly composed recited prayer.

Both accepted studies were read. Existing evidence was reused through reading
the scope, interpretation and reception records and directly rereading the
retained NPNF witnesses: Augustine, John 115.1–4; Psalm 28.10–11; Chrysostom,
Colossians II on 1:12–15 and III on creative dependence, reconciliation and the
peace application. No new research claim, source binding or accepted upstream
prose was added. The declared manifest already provides the two homily-only
components and all eleven informing element keys. The entrypoint uses the three
shared imports in order, a full-width title, and only the literal spoken-body
import within `properhomily`; sources and delivery notes follow its page break.

## Completed homily checks

- `make doc` for the GPT `f01-christ-the-king-homily` target completed with
  **3 physical pages**, two of speech and one of source/delivery apparatus.
  The settled log has no warnings, undefined references, overfull or underfull
  boxes. Title, subject and revision metadata are correct; every listed Latin
  Modern font is embedded. The PDF is 245,941 bytes; its 81,980 bytes per page
  crosses the size-review trigger because a short three-page document embeds
  ten font subsets. No images are embedded; the total remains below 1 MiB and
  no independent PDF transformation was applied.
- Homily component content and artifact checks passed. Full homily content
  preflight passed, including bindings, chronology currency, house voice, source
  identifiers, used references, relation coverage, restricted-source reproduction,
  structural labels and quotation checks. All three reference entries are used.
- All three full-page rasters generated by the registered `pdf-review` tool were
  visually inspected. The full-width title precedes two readable columns;
  the speech continues in order onto page 2 and ends before the page break.
  Page 3 carries the separate note, References, timestamp and readable rights
  colophon, with no clipping, overlap or rights-only spill. Ordinary paragraph
  continuations cross column and page boundaries without lost text. Extracted
  text was read to confirm the speech and terminal sequence.

Built proof:
`build/gpt/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king-homily.pdf`.
Raster evidence:
`build/tpt-runs/095fe00a9fe8cfee/artifacts/derive-homily-0000/rasters/`.
The registered raster tool requires a build-tree destination; other stage
logs and the identical retained author proof are in the driver's assigned scratch
area. This is author verification, not independent homily or visual acceptance.
No installed PDF, accepted study prose, research evidence or shared inventory
was changed. The shared timestamp requires the later three-document build.
The parent driver owns source-inventory/family refresh, `make check-sources`,
commits and publication. No forwarded findings or upstream defects arose.

Exact homily author-proof SHA-256:
`c80c025401979949296f42f28597c5b679a0f3783120ffb6489460f17b10fc08`.

# Expansive study reentry: Secret addressee

Author-stage iteration 1 completed on 20 October 2026 for `proper-study` v13,
run `095fe00a9fe8cfee`, after the research correction prompted by HOM-001.
The revised research distinguishes the Father addressed by the Secret from
the sacrificial Son who gives the requested unity and peace. The detailed
commentary and both interpretive lanes now express that distinction. The
source prayer, research evidence, appointed-text mode, chronology, manifest
and other supported arguments remain unchanged. The shared generation record
was finalized at `2026-10-20T13:37:56Z`; the companions require their subsequent
workflow derivation and review.

The revised study has **7,628 substantive words** by the same Pandoc method
recorded above: component counts are 607, 1,615, 1,946, 1,975, 381 and 1,104.
Its full-text scope and source limits remain those stated above. Comparison
against the reviewed record again confirmed all thirteen Latin and thirteen
historical-English blocks after the documented typographic normalization.

`make doc` completed with **23 physical pages**, 481,236 bytes, correct title,
subject and revision metadata, and all listed Latin Modern fonts embedded.
The settled log has no warnings, undefined references or overfull/underfull
boxes. The research artifact component check and all research content-preflight
checks passed. The web probe passed with Pandoc and pinned Python Markdown
3.10.3; an initial invocation using the host's 3.11.2 was correctly refused,
then rerun with the pinned dependency without changing source or converter.

All 23 rendered pages were inspected in regenerated contact sheets. Full-size
inspection of corrected pages 9, 12 and 14 and final page 23 confirmed readable
paragraphs, ordinary continuations, unclipped footnotes, and the timestamp and
rights colophon together on the last page. Text extraction confirms the revised
Father/Son distinction in all three corrected passages. No new layout defect
was observed. This is author proof, not independent content, visual or web
acceptance; no PDF or web edition was installed by this stage.

Exact built PDF:
`build/gpt/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king.pdf`.
Byte-identical retained proof:
`build/tpt-runs/095fe00a9fe8cfee/artifacts/author-study-0001/author-proof.pdf`.
SHA-256:
`d8f12b25001f80cda0cb083c0b94669493bce24bafde1806b31f90046cd9c09c`.
The same stage directory retains build, component, preflight and web-probe
logs, extracted text, source-transfer and word-count evidence, and replaceable
rasters. No new upstream defect was identified; shared inventory refresh,
integration checks and final publication remain with the parent driver.

# Concise study reentry: Secret addressee

`derive-synthesis` iteration 1 completed on 20 October 2026 for `proper-study`
v13, run `095fe00a9fe8cfee`. The concise inventory, thematic movement and
comparative commentary now distinguish the Father addressed by the Secret from
the sacrificial Son who gives unity and peace. The change derives from the
accepted expansive study's corrected detailed commentary and both interpretive
lanes, and the corrected research summaries. All remaining concise references
to the Secret were checked for consistency. No new evidence-dependent claim or
upstream revision was introduced.

The two interpretations, their comparative reasoning, four senses, source
qualifications, generated chronology and six synthesis-only components remain
intact. The existing manifest accurately declares their modes and presentation
roles; the entrypoint retains literal unconditional imports of the shared
formats and its components. The shared generation timestamp is
`2026-10-20T13:46:08Z`, with this contribution appended to the existing record.

The settled proof has **10 physical pages**, **406,474 bytes**, and **4,149
substantive words** by the previous concise proof's Pandoc method. The component
counts are 173 for the inventory, 74 for the overview, 958 for themes, and 2,944
for developed commentary. Chronology, footnotes, terminal apparatus and the
generation colophon are excluded as before.

The specified synthesis `make doc` build, synthesis artifact component check,
and complete synthesis content preflight passed. The settled log has no
warnings, undefined references or overfull/underfull boxes. All listed Latin
Modern fonts are embedded; title, subject and revision metadata are correct.
The auxiliary evidence retains inventory and all four overview rows on physical
page 1, chronology on page 2, themes on pages 3–4, and commentary beginning on
page 5. The nine generated orientation rows and their dates, relation labels,
alternatives and unresolved states are unchanged.

All ten pages were visually inspected in the regenerated contact sheet, with
full-size inspection of pages 1, 2, 4, 7 and 10. The three corrected passages
are readable without clipping or overlap. The page-2 lookup still pairs John
18:33–37's Jerusalem interrogation with its unresolved event date, separately
from the Gospel's composition alternatives; Colossians distinguishes the
traditional Roman prison from Colossae; and the Introit's Apocalypse passages
remain distinct from its Psalm. The final page keeps scope, references,
timestamp and readable rights colophon together. Extracted text confirms the
Father/Son distinction at all three revised locations.

Built PDF:
`build/gpt/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king-synthesis.pdf`.
The byte-identical retained proof and associated evidence are under
`build/tpt-runs/095fe00a9fe8cfee/artifacts/derive-synthesis-0001/`:

| File | SHA-256 |
| --- | --- |
| `author-proof.pdf` | `8f15120552c8c72f5ade7fb43eb310cc94978580a86021ea147f55c2a384f026` |
| `author-proof.aux` | `fc869f5656388d79f742546941ab414e9338201a0da760450138901cfa54054a` |
| `author-proof.log` | `988803800ddccc120a2f33c2f30b99003a1c6607ed7d289bb0bcdd798589ec2f` |

That directory retains build, component and preflight logs, extracted text,
font and metadata reports, hashes and word-count evidence. Raster evidence
occupies its replaceable `rasters/` child. This is author verification, not cold
concise acceptance or final three-document visual review. There were no
forwarded findings, and no new upstream defect was identified. No PDF or web
edition was installed. The parent driver owns global source-inventory checks,
integration, commits and publication; the later homily derivation and final
common build must use the resulting shared metadata.

# Homily reentry: Secret addressee

`derive-homily` iteration 1 completed on 20 October 2026 for `proper-study`
v13, run `095fe00a9fe8cfee`. Both revised studies were read, together with the
research scope, interpretation audit and appointed-text component. The spoken
Secret paragraph now says that the prayer asks the Father that his Son give
unity and peace among the nations. The following sentence still identifies
the offered Son as the giver. The terminal source note states the same
distinction. This supersedes the iteration-0 audit's description of the Secret
as a petition addressed to the sacrificial giver. The Missal's no. 3947 remains
the exact source locus, and no new source-dependent claim was introduced.

The adult-parish audience, hearing-king argument and compatible sacrificial
peace application remain intact. The decisive textual detail is still
Augustine's reading of John 18:36: the kingdom's different origin does not
remove its people from this world. That distinction changes an opening question
about the prisoner's visible power into the question of grace-enabled hearing
within ordinary responsibilities. John 18:37, Colossians 1:12–20, the Collect,
Secret, Communion and Postcommunion carry the movement toward conversion and
hope. Correctly identifying the Father addressed by the Secret preserves the
Son's sacrificial gift within that movement.

The revised body has **1,280 spoken words**, counted as whitespace-separated
words in its prose-only component, four more than the previous version.
At **110–125 words per minute**, the calculated duration is **10.2–11.6
minutes**, still approximately 10–12 minutes. The entire speech was read
silently for sense and oral clarity, including the revised sentence's reference
to the Father and his Son. No audible rehearsal or timed human delivery is
claimed. The practical applications and preaching conclusion remain unchanged;
no newly composed prayer is supplied.

The entrypoint and manifest needed no change. The three shared imports remain
in their prescribed order; only the spoken import is inside `properhomily`,
with the terminal apparatus after its page break. The generation record carries
the packet's exact provenance, finalization time `2026-10-20T13:56:23Z`, and
the added homily-revision contribution. No accepted study prose or research
evidence was changed.

The homily `make doc` build, artifact component check and complete homily content
preflight passed. The settled PDF has **3 physical pages** and **246,092 bytes**.
Its log has no warnings, undefined references or overfull/underfull boxes.
Title, subject and revision metadata are correct, and all ten listed Latin
Modern font subsets are embedded. The approximately 82,031 bytes per page
again crosses the size-review trigger for a short document embedding ten font
subsets; total size remains below 1 MiB, and no PDF transformation was applied.
All three reference entries are used.

All three full-page rasters were visually inspected. The full-width title and
two-column speech remain readable; the corrected paragraph appears on page 2.
The speech ends there, and page 3 holds the source/delivery note, References,
timestamp and compact rights colophon without clipping, overlap or a spill.
Text extraction confirms the revised sentence, the source-note distinction and
the updated word count.

Built proof:
`build/gpt/liturgy/roman-rite/1962/propers/temporal/f01-christ-the-king-homily.pdf`.
SHA-256:
`1ad22ec21d738d3028a7252b9d2d92b6b7f3dc9eac80249c87bc7116a7eb1af2`.
An identical proof, logs and extraction are retained in the driver's assigned
scratch area. The registered tool's raster destination is
`build/tpt-runs/095fe00a9fe8cfee/artifacts/derive-homily-0001/rasters/`.
This is author verification, not independent homily or final visual acceptance.
There were no forwarded findings and no new upstream defect was identified.
The parent driver owns source-inventory checks, the final common build,
integration and publication; no PDF or web edition was installed here.
