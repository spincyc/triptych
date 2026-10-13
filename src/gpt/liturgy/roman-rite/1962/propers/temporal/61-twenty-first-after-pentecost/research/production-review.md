# Final three-document artifact build

## Build-artifacts iteration 0

The fresh GPT-6 worker at high effort executed the complete proper-study v10
packet for run `a72731c5491066a3`, SHA-256
`0de56b683e35a6da261dd2131289b4838c83e4af51ebb3b4510fe6795f22110b`.
All three required `make doc` invocations passed with the current shared
render-source revision `2026-10-13T04:24:11Z`. The study and concise study
were recompiled; Make correctly reused the current homily PDF. No accepted
prose, research, layout source, generation declaration, or content seal changed.

The build directory is `build/gpt/liturgy/roman-rite/1962/propers/temporal/`.
Its exact final outputs are:

| PDF filename | Physical pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `61-twenty-first-after-pentecost.pdf` | 26 | 447318 | `53a30dd4b8d95831a3540252484508c8ef3c28792a9e05e19032a78ba809635d` |
| `61-twenty-first-after-pentecost-synthesis.pdf` | 10 | 386752 | `ccb26a8cc49035b06ecfe6067679b6eef4c7d318ec59f45152bfccd1f49af325` |
| `61-twenty-first-after-pentecost-homily.pdf` | 3 | 245076 | `cf59a2d2cd49c33189a55712761da1934c1e0ed909284e5a6d9622f775dc9e17` |

The required snapshot command produced `research/artifacts.json`, SHA-256
`9cdfa0bfa5d687e3b8f71b8aa512b48b639d7563025cb91b4e5e620f37d0e1a9`.
It records the actual PDF bytes, render inputs and pagination auxiliaries;
it is not an approval or a claim of visual review.

## Settled checks and retained evidence

Evidence is retained beneath
`build/tpt-runs/a72731c5491066a3/artifacts/build-artifacts-0000/`.
The `study-final.pdf`, `synthesis-final.pdf` and `homily-final.pdf` copies
are byte-identical to the outputs above. Their matching auxiliaries,
PDF metadata, font reports, layout and raw extractions, diagnostic summaries,
snapshot copy and `verification.json` accompany them outside `rasters/`.

- The complete artifact component check passes. All 13 concise zref markers
  settle on the required physical pages: inventory, overview and its four
  sense rows on 1; chronology on 2; themes start on 3 and end on 4;
  commentary starts on 5. The study and concise extents meet their ranges.
- All three native final TeX logs were checked for fatal diagnostics,
  warnings, overfull/underfull boxes, undefined references and missing
  characters: none was present. The concise auxiliary SHA-256 is
  `2bfdb9c12bb938b301e7352611b4e71ea54209a60b8fbb193cab564204c643b1`;
  its native log SHA-256 is
  `3979b3ff6373c33187f3db3bbad33ee85687cf33d54e989589616f9764298106`.
- The repository anchor checker passes all 57 study, 14 concise and 2 homily
  contents anchors. Poppler reads all PDFs as unencrypted PDF 1.7, Letter
  pages, with no JavaScript. Every font is embedded, subset and Unicode-mapped
  Latin Modern: 14, 15 and 10 font rows respectively. PDF modification dates
  match the shared revision; creation dates are absent.
- Every extracted page contains text, with no unresolved-reference or
  replacement-character marker. Layout extraction matches each respective
  final author proof exactly after normalizing only the revision timestamp.
  The concise opening and terminal matter were also inspected in extraction.
  The 1,257 homily spoken tokens match the source in order after removing
  running matter and normalizing line-break hyphenation and ligatures from
  raw extraction. Each PDF displays the current revision once and retains
  the rights colophon on its final page.
- `tools/tpt pdf-review` completed successfully in the dedicated `rasters/`
  child and produced all 39 full-page rasters. The sanitized public raster
  evidence has SHA-256
  `c63b254f81dff51ea3a010d05cc76ad2b6dbb23ee23c913971b9dad9b4c5d464`.
  It explicitly identifies its native receipt hash and allowlist derivation;
  native helper receipts and original logs remain local operational evidence.
  The files named `*-log-diagnostics.sanitized.txt` are diagnostic-only
  derivatives, not complete native logs. `public-evidence.sha256` binds these
  public derivatives and the other retained evidence. Public text evidence
  was screened for machine-specific path prefixes.

## Boundary and remaining work

This stage performed no fresh source verification and gives no cold visual
verdict. The separate visual worker must inspect every final page. Neither
`qpdf` nor `mutool` was available; structural checks used Poppler metadata
and extraction, repository anchor validation and successful all-page rendering.
The known aggregate document-catalogue drift remains a downstream publication
responsibility; this worker did not rerun or modify that global wiring.

Only this production audit and the tool-generated artifact snapshot changed
under the canonical leaf. All build, check and raster processes completed;
no background process remains. No installation, staging, commit, push or
workflow advancement was performed.

# Homily: author verification

## Current proof: derive-homily iteration 0

The fresh GPT-6 author at high effort completed the homily for proper-study
v10, run `a72731c5491066a3`, from the complete packet SHA-256
`c9d297825dc00025e30ba91adfdca862238f7172e88ac9220f95d7e9f3a13e74`.
Both accepted studies and their research arguments were read directly.
Their prose and research remain unchanged. The shared generation record
adds the actual homily contribution and records render-source revision
`2026-10-13T04:24:11Z`.

The finished speech, **The Words He Would Not Hear**, addresses an adult
parish assembly and develops the `mercy-received` reading. Its decisive
detail is the repeated plea for patience in Matthew 18:26,29, followed by
the deliberate refusal in verse 30. The king gives more than the first
servant requests; that recipient refuses even what his companion requests.
The listener's governing question therefore changes from what another owes
to what received mercy requires. The Epistle's exclusion of flesh and blood
as the ultimate enemy and the Postcommunion's inward fruit develop that
same argument. Job's initial uprightness prevents identifying every wounded
person with the condemned servant. Aquinas's real-pardon/new-culpability
distinction preserves the warning without making prior remission unreal.

The spoken component contains **1,257 words**, counted as alphabetic word
tokens with internal apostrophes and hyphens retained. Title, apparatus,
references and metadata are excluded. At 110–120 words per minute, the
estimate is **10.5–11.4 minutes before pauses**, approximately **11–12 minutes
with brief pauses**. A textual rehearsal checked sense, transitions, sentence
length, and oral clarity; one cumbersome sentence about completed pardon
was divided into two short sentences. No audible or timed human rehearsal,
personal experience, clerical identity, or new received prayer is claimed.

## Homily proof and checks

Evidence is retained under the repository-relative directory
`build/tpt-runs/a72731c5491066a3/artifacts/derive-homily-0000/`.
The proof `homily-proof.pdf` has **3 pages**, **245,076 bytes**, and SHA-256
`cf59a2d2cd49c33189a55712761da1934c1e0ed909284e5a6d9622f775dc9e17`.
It is byte-identical to the checked build. Speech occupies pages 1–2;
source/delivery note, References, revision and rights share page 3.

- `make doc` passed, including generation metadata and individual contents
  anchors. The settled TeX log has no warning, overfull/underfull box,
  undefined reference, missing character, or error.
- The homily artifact component check and complete homily content preflight
  passed. The latter validates 34 bindings and five used reference entries.
  The existing manifest already declared both homily components, so no
  manifest change was needed.
- Every page was opened as a full-page raster produced by `tools/pdf-review`
  in the dedicated replaceable `rasters/` child. The full-width title,
  two-column speech, running head, separate terminal page and compact rights
  colophon were inspected. No clipping, collision, stranded heading or
  illegible text was observed. Font inspection found embedded, subset,
  Unicode-mapped Latin Modern fonts; PDF structure reports Letter pages.
- The 1,257 spoken tokens match the PDF extraction in order after title,
  running heads and page numbers are removed. This comparison uses
  `pdftotext -raw`: its default extraction interleaves the two columns.
  Source whitespace checks passed. Proof logs have workstation prefixes
  removed; native raster-helper cache receipts are operational artifacts,
  not public evidence.
- `make check-sources` was run and exited 2 at `check-document-catalogue`:
  the generated document catalog has drifted from the completed sources.
  The tool requests `document-library structure`. This shared catalog belongs
  to the coordinator/publication owner and was reported for reconciliation;
  the homily author did not change it or the shared source inventories.

## Homily evidence and handback limits

The author directly read the accepted appointed texts and evidence maps,
Chrysostom's relevant Matthew LXI exposition (especially §§3–5),
Augustine's Sermon 83 §§1–8, Aquinas III q.88 a.1 and a.2's answer, the
relevant spiritual-conflict passage of Chrysostom's Ephesians XXII, and
Schuster's Secret/Postcommunion discussion on p.181. These were readings
of retained historical-text witnesses, including Schuster's OCR, not new
facsimile collations or a new exhaustive research sweep. The accepted
Missal collation and source limits remain controlling. No new source-dependent
claim, upstream defect, or shared-code repair was introduced.

Only the homily entrypoint, its two local components, the shared generation
record and this production record changed in this stage. All author-started
build, check and raster processes completed; no background process remains.
No staging, commit, push, installation or workflow advancement occurred.
Cold homily review, the final build of all three documents with the shared
timestamp, and the remaining independent artifact and publication reviews
remain required. This proof is author verification, not their acceptance.

# Concise study: author verification

## Current proof: derive-synthesis iteration 0

The fresh GPT-6 author at high effort derived the concise comparison for
proper-study v10, run `a72731c5491066a3`, from the complete packet SHA-256
`47ca5e8860547fe897d80744e622e57dfa403c09c13d5f758a21c5763f212b0b`.
The shared generation record preserves the workflow digest and seed commit,
adds the actual contribution, and records final render-source revision
`2026-10-13T03:56:10Z`.

The proof contains **10 physical pages** and **4,135 substantive words**:
inventory 242, overview 70, themes 978, and developed commentary 2,845.
The count uses English-alphabet word tokens with internal apostrophes and
hyphens retained. It includes headings and sense distillations but excludes
footnotes, TeX commands and marker arguments, generated chronology and its
historical notes, terminal apparatus, and generation metadata. It adapts the
existing study-author counting procedure; this is a prose count, not a count
of every printed token.

All seventeen dated or conditional inventory elements are present. The
mission and St Luke conditions retain their distinctions. The two accepted
whole-formulary readings are compared through questions of release, renewed
judgment, protection, sacramental food, and the Church's petition for judgment.
The comparison preserves the difference between innocent Job and the guilty
servant; Aquinas's distinction between completed remission and new liability;
Gregory's distinction between evil intent and bounded permitted power; the
historical editor's disagreement with Chrysostom; and Schuster's present
privation beside Augustine's and Bellarmine's final expectation. The later
commentary develops the witnesses' reasoning rather than repeating the opening.

## Retained proof and physical evidence

All paths below are relative to the repository. The proof directory is
`build/tpt-runs/a72731c5491066a3/artifacts/derive-synthesis-0000/`.

- `synthesis-proof.pdf`: 386,752 bytes; SHA-256
  `873a34706aeb564af9f308632dd120350c10d2930b56440438742621f06da7ab`.
- `synthesis-proof.aux`: 5,083 bytes; SHA-256
  `2bfdb9c12bb938b301e7352611b4e71ea54209a60b8fbb193cab564204c643b1`.
- `synthesis-proof.log`: 44,334 bytes; SHA-256
  `ae535e28d9643abbc527e816954e9c856b42b386c3b41371c77beb4433389c14`.
  Workstation prefixes were removed from this retained log; the original
  build log's SHA-256 is
  `6e28900e95738fd43d6be23f50e9fedffd55f4b51ccd64cdff528459b9fd20ab`.
  Diagnostics were checked against the original log before sanitization.

The auxiliary markers place inventory start/end, overview start/end, and all
four individual sense rows on physical page 1; chronology start/end on page 2;
themes start on page 3 and end on page 4; and commentary start on page 5.
The scope occupies page 9; References, revision and rights occupy page 10.
The PDF and auxiliary copies are byte-identical to the checked build.

Every final page, 1–10, was opened as a full-page raster generated by
`tools/pdf-review`, beneath the dedicated replaceable `rasters/` child.
No clipping, collision, stranded heading, broken table or illegible footnote
was observed. Page 2 was also checked as a reader's orientation table at
ordinary full-page size: the Gospel event and composition remain separate,
the Exodus interval remains distinct from Psalm composition, and the Davidic
attribution remains conditional. Modest spacing separates the nine row calls.
Short place phrases preserve the actual dated subjects; adjacent notes give
precise expansive-appendix pages and sources. No page-reference command enters
a row argument and no generated date, alternative or relation label changed.

## Actual checks and limits

- The required `make doc` completed successfully. All 14 contents anchors
  resolve. The synthesis-edition artifact component check and all twelve
  content preflight checks pass, including 34 bindings, nine generated
  chronology rows, current canonical chronology, five used reference entries,
  both interpretive lanes, rights and house voice.
- The original final TeX log contains no warning, overfull/underfull box,
  undefined reference, missing character or error. `pdfinfo`, `pdffonts`,
  text extraction and `git diff --check` pass. Pages are US Letter; all
  Latin Modern fonts are embedded, subset and Unicode-mapped. The visible
  revision matches the shared metadata. PDF extraction contains no unresolved
  page-reference marker.
- `make check-sources` was run and exits 2 after validating the reusable
  source library, including 3,815 bindings: the document catalogue requires
  the future declared `homily.tex`. The synthesis-stage artifact gate passes.
  This is a downstream dependency; no placeholder or shared-code edit was made.

The author read the accepted expansive text and canonical research directly,
including the chronology and its evidence bounds. Aquinas III q.88 aa.1–4 was
also reread in the retained English transcription for the technical account of
remission and renewed liability. This was not a new facsimile collation or a
new research sweep. Other source-verification limits remain those of the
accepted research and expansive-study records. No new evidence-dependent claim
or upstream defect requiring repair was identified.

Changed files are `synthesis.tex`, the six declared files under
`sections/concise/`, `generation-metadata.tex`, and this production record.
The existing manifest already declares their correct mode membership and
presentation owners and did not require editing. Accepted research, expansive
prose, generated chronology, source owners and shared code were not edited.
All author-started build, check and raster processes completed; no background
process remains. No staging, commit, push, installation or workflow advancement
was performed. This is author verification only: fresh concise review, homily
production, the final three-document build and independent reviews remain
required after the shared generation metadata has settled.

# Expansive study: author verification

## Current proof: author-study iteration 2

The fresh GPT-6 author at high effort reconciled the historical appendix with
the corrected research account, from packet SHA-256
`7f9dfc8f86a5c68f08b25b7b83924369ec3d2840bc0395ed5421f11a32eaafc2`.
Haydock's three reported conjectures now distinguish David instructing young
Solomon, David writing under Saul's persecution, and Daniel consoling the
captives. The Davidic chronology remains conditional and does not date the
Psalm's occasion or verse 81. Augustine's Mosaic-authorship caveat now cites
Psalm 89 §2 (NPNF Psalm 90). No generated date, source-owned qualification,
appointed text, or core argument changed. The final render-source revision
is `2026-10-13T03:24:49Z`.

The final author proof is
`build/tpt-runs/a72731c5491066a3/artifacts/author-study-0002/study-proof.pdf`:
**26 physical pages**, 447,319 bytes, SHA-256
`324c562aebd7ba283666721403b192f9a2a9fda11a43cb063e720192b21553aa`.
The iteration 1 and iteration 0 records below describe their earlier bytes.

- The required `make doc`, research-edition artifact component check, and
  complete research-edition content preflight passed. All 57 contents anchors
  resolve. The settled TeX log has no warning, overfull/underfull box, undefined
  reference, missing character, or error. The preflight validates all nine
  generated chronology rows and their currency, 34 source bindings, and
  14 used reference entries.
- The existing text-comparison/count procedure was rerun. All 17 Latin and
  17 English displayed bodies still match the collation under its documented
  formatting normalization; the unchanged core exposition has **7,233
  substantive words**, counted by the method below.
- Every final page, 1–26, was opened as a full-page raster from
  `tools/pdf-review`. No clipping, collisions, broken table, stranded heading,
  or illegible footnote was observed. Page 24 contains the corrected paragraph
  and Augustine locator; the chronology and references retain their previous
  page locations. The revision and rights colophon fit on page 26.
- PDF structure, extracted text, fonts, source whitespace, and the proof's
  byte identity with the checked build were checked. The proof has Letter
  pages and embedded/subset/Unicode-mapped Latin Modern fonts, one visible
  revision, and no unresolved page-reference marker.
- `make check-sources` validates the reusable source library, including
  3,815 bindings, then exits 2 because the document catalogue requires the
  declared future `homily.tex`. The study-stage artifact gate passes. This
  remains a later-stage dependency; no placeholder or shared-code repair was
  made.

The author read the current research evidence directly and inspected the
previously acquired Haydock facsimile images of printed pages 780–781
(PDF pages 816–817). Page 781 confirms the three conjectures and general
Davidic attribution. This was a fresh visual inspection of those retained
images, not a new download or whole-artifact hash verification. The author
also read Augustine's Psalm 90 §§1–3 directly in the retained NPNF/CCEL
transcription: §2 contains the authorship caveat. That reading was not a
fresh print-edition collation. Other accepted source checks and limitations
remain those of the earlier stages; this was no new exhaustive research sweep.

Only the historical appendix, generation record, and this production record
changed in this iteration. Canonical source owners and generated chronology
remain unchanged. No additional upstream research need or shared-code defect
was identified. All author-started build, check, and raster processes completed;
no background process remains. No staging, commit, push, installation, or
workflow advancement was performed. Cold study review and the subsequent
companion and publication stages remain required.

## Prior proof: author-study iteration 1

The fresh GPT-6 author at high effort completed the three forwarded mechanical
repairs from packet SHA-256
`54517be9d1f0df3603ae2ae5efee3b120d7229b5b02007c6ffc4d8b53ef320d5`.
The terminal scope and References now have separate semantic headings; the
scope paragraph formerly after the bibliography is with the other scope
paragraphs. The nine chronology cells retain their complete contextual prose,
with their page references consolidated directly below the table. No generated
date, source-owned qualification, appointed text, or interpretive argument
changed. The final render-source revision is `2026-10-13T02:24:13Z`.

The current author proof is
`build/tpt-runs/a72731c5491066a3/artifacts/author-study-0001/study-proof.pdf`:
**26 physical pages**, 447,250 bytes, SHA-256
`b4717e5f3508a872c6e59c9a213cb85708871ef7e1447bcdd004e94477ac4f54`.
The previous proof and verification below describe iteration 0, not these
current bytes.

- The required `make doc` and research-edition artifact component check passed.
  All 57 contents anchors resolve. The settled TeX log has no warning,
  overfull/underfull box, undefined reference, missing character, or error.
- All three forwarded checks pass: `references-used` recognizes 14 used
  entries; `unquoted-not-quoted` finds no conflict; and
  `chronology-claims-supported` validates all nine generated rows. The complete
  research-edition content preflight also passes, including chronology record
  and annotation currency, 34 source bindings, rights, house voice, and both
  whole-formulary lane declarations.
- The existing text-comparison/count procedure was rerun: all 17 Latin and 17
  English displayed bodies match the collation after its documented formatting
  normalization. The unchanged core exposition has **7,233 substantive words**
  by the method below.
- Every final page was opened as a full-page raster generated by
  `tools/pdf-review`. No clipping, collisions, broken table, stranded heading,
  or illegible footnote was observed. On page 23, the source-reference line
  correctly directs Esther to page 23; Job, Psalms, and Matthew to page 24;
  and Ephesians to page 25. References begins on page 25 and continues on
  page 26. The revision and compact rights colophon remain on page 26.
- PDF structure, text extraction, and fonts were checked: Letter pages,
  embedded/subset/Unicode-mapped Latin Modern fonts, one visible revision,
  and no unresolved page-reference marker. The proof is byte-identical to
  the checked build; the leaf's whitespace check passes.
- `make check-sources` was attempted. The reusable source library validates
  (including 3,815 bindings), but the aggregate exits 2 because its document
  catalogue check requires the declared, future `homily.tex`. The study-stage
  artifact gate permits those future companions and passes. No placeholder
  companion or shared-code change was introduced to satisfy a later-stage gate.

This repair reused the reviewed evidence map, chronology, and source limits;
it did not repeat the earlier author or research stage's external-source
inspection and claims no new source verification. All accepted research files,
source owners, and the two arguments remain unchanged. No new upstream
research need or shared-code defect was identified. The changed leaf files
are the historical appendix, study apparatus, generation record, and this
production record. All author-started build, check, and raster processes
completed; no background process remains. No staging, commit, push,
installation, or workflow advancement was performed. Cold study review and
all companion and publication stages remain the workflow's responsibility.

## Scope and provenance

Completed author-study iteration 0 for proper-study v10, run
`a72731c5491066a3`, from packet SHA-256
`373b377ba75ab6ba011a91b82c5aa35da7a59db405cdc044864c65fecffb5ef9`.
The author was GPT-6 at high effort through OpenAI Codex. The canonical
generation record carries the packet's workflow digest and seed commit;
the final render-relevant revision timestamp is `2026-10-13T02:17:00Z`.

The study concerns only the 1962 Twenty-first Sunday after Pentecost on
18 October 2026. It includes all seventeen appointed or conditional elements,
the documented mission-day and St Luke branches, detailed commentary, two
whole-formulary readings with their own four senses, a concluding comparison,
the reviewed chronology and historical appendix, and terminal references and
rights. No local calendar is supplied or inferred. The manifest declares the
future concise study and homily; those documents were not authored in this
stage. Accepted research, acquired sources, and shared code remain unchanged.

The core exposition contains approximately **7,233 substantive words**:
opening and map 651; element commentary 2,088; mercy reading 1,983;
pilgrimage reading 2,193; concluding comparison 318. The count uses
English-alphabet word tokens with internal apostrophes and hyphens retained,
excluding footnotes, TeX commands, displayed appointed texts, the historical
appendix, and terminal apparatus. It includes the readings' sense distillations.

## Proof and actual checks

The author proof is
`build/tpt-runs/a72731c5491066a3/artifacts/author-study-0000/study-proof.pdf`.
It has **26 physical pages** and SHA-256
`4f51be986a33deb748895c8f3f5825f33c81247ab9fad8bc4dc043d1ea9b4403`.

- `make doc DOC=liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost PROVIDER=gpt`
  completed. Generation metadata and PDF navigation checks passed; all 56
  contents anchors resolve individually. The final build log contains no
  warning, overfull/underfull box, undefined-reference, missing-character, or
  TeX-error diagnostics.
- `tools/check-proper-components --provider gpt --document liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost --phase artifacts --edition research`
  passed. The study uses shared formatting and the full schema-2 declaration.
- All seventeen Latin and seventeen English displayed bodies match
  `propers/verified.md` exactly after TeX escaping, verse-label formatting,
  and outer-whitespace trimming. No lexical change or new translation was
  introduced. Historical English variants and biblical comparators are
  identified at their uses.
- `pdfinfo`, `pdffonts`, text extraction, and the leaf's `git diff --check`
  were inspected. The proof is US Letter; its Latin Modern fonts are embedded,
  subset, and Unicode-mapped. The main source uses the required 11-point
  article and shared 0.75-inch margins.
- `tools/pdf-review` generated full-page rasters in the stage artifact's
  dedicated `rasters/` child. Every page was inspected at full-page scale
  across the settled drafts. The final proof's pages 5–10 are byte-identical
  PNGs to the inspected 27-page draft; the final proof's other unchanged
  pages are identical to the inspected preceding 26-page proof. Final pages
  1–4, 20, and 23–26 were also viewed directly after the last rebuild.
  The last rebuild changed only page 20's corrected Augustine verse locator
  and page 26's timestamp; both were inspected again. No clipping, collisions,
  broken tables, stranded headings, or unreadable footnotes were observed.

The proof directory contains the logs, font and PDF reports, text-integrity
and word-count result, diagnostic result, raster comparison, and structured
author evidence. Workstation prefixes were removed from archived logs.

## Native evidence read and limits

The author read the canonical evidence maps and source records, then opened
the retained texts rather than treating an earlier PASS as verification:
Chrysostom's Matthew LXI §§1–5 and Ephesians XXII–XXIV (including the disputed
editorial notes); Augustine's Sermon 83, Psalm 89 §§1–4, Psalm 113 §§1–6,
Psalm 118 Aleph and Caph, and De Trinitate III preface §3; Gregory's Moralia
II.10.16–11.19 and the relevant III.3.3–6.8 exposition; Aquinas III q.88
aa.1–4; Bellarmine's relevant Psalm 89, 113, and 118 verse comments; and
Schuster III pp.178–181. Carrying authors make distinct substantive arguments
within each reading. Whole-Mass constructions remain the study's editorial
work; disagreements and differences of emphasis are retained.

The registered Douay–Rheims biblical context was read for Esther 13–14,
Job 1–2, Matthew's surrounding discourse and geographical transitions,
Ephesians 6 and the relevant earlier ethical context, and the appointed
Psalm contexts. Retained historical Catholic Encyclopedia discussions were
read for Esther, Ephesians, Matthew, New Testament dating, biblical
chronology, Paul, and David. The two official USCCB book introductions were
reopened to confirm their bounded Job and Psalms dating claims; their modern
prose is paraphrased, not used as study-text English. That current web
inspection was not a hash comparison to the acquisition-time pages.

This stage is not a fresh critical Greek or Latin edition or a new exhaustive
research sweep. It reuses the accepted Missal collation and rights decisions.
The author did not repeat every liturgical facsimile collation or independently
inspect the Haydock page image. Gregory was read in the retained reset
transcription, Schuster in retained OCR, and De Trinitate in the disclosed
later-revised web delivery; no new author-side facsimile verification is
claimed for those witnesses. No upstream defect requiring a research repair
was identified.

## Handback boundary

This record describes author verification only. Cold study review, derivation
and review of both companions, the shared-timestamp three-document build,
and independent visual and publication reviews remain workflow work.
All author-started build and raster processes completed; no server, browser,
or background worker remains running. No Git staging, commit, push, or
workflow advancement was performed by this author.
