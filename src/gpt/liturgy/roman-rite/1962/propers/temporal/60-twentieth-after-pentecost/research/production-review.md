# Production and review record

## Expansive study author proof — 5 October 2026

This entry records author verification for `proper-study` version 9, run
`e80cd019cbe2d2f4`, stage `author-study`, iteration 0. It does not record an
independent review or acceptance of either companion.

The canonical study is complete: a substantive opening and fourteen-element
map, the appointed Latin and identified historical English study material,
element-by-element commentary, two developed whole-formulary readings with
separate four-sense distillations, a concluding comparison, the reviewed
canonical chronology, terminal scope and references, and the shared generation
record and rights colophon. Both conditional branches of the Maternity
commemoration remain explicit. The schema-2 manifest declares the future
concise-study and homily components without claiming that they exist yet.

The settled author PDF has **21 physical pages**. Substantive exposition has
**6,338 words** by a source-token count of the opening prose, detailed
commentary, both interpretive readings including their four-sense summaries,
and the concluding comparison. The count excludes the map, appointed texts,
chronology, terminal apparatus, headings, footnotes, labels, and TeX commands;
hyphenated compounds count as separate words. Component counts are 336, 1,783,
1,891, 1,980, and 348 respectively. This count measures authored exposition,
not reproduced primary texts or apparatus.

### Exact proof and author checks

- Canonical PDF: `build/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost.pdf`.
- Preserved proof: `build/tpt-runs/e80cd019cbe2d2f4/artifacts/author-study-0000/author-proof.pdf`.
- SHA-256 of both: `5245826b7ad9bbff3120e366f2f8ecc9cbdf61e52c33e20b37228392a849a7d2`.
- Displayed finalization timestamp: `2026-10-05T15:44:04Z`.
- `make doc DOC=liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost PROVIDER=gpt` passed.
- `tools/check-proper-components --provider gpt --document liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost --phase artifacts --edition research` passed.
- `tools/check-content-preflight --provider gpt --document liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost --edition research` passed, including all 24 live source bindings, seven chronology elements, and both complete interpretive readings.
- The final TeX log has no overfull or underfull boxes, undefined references, or warnings. PDF inspection confirms letter paper and embedded, subset Latin Modern fonts. The build's anchor check passed for 41 contents entries.
- Every full-page raster, pages 1–21, and both contact sheets were visually inspected. The appointed texts, footnotes, two readings, split chronology table, references, timestamp, and colophon remain readable; no clipping, overlapping text, blank pages, or stranded headings were observed. The natural page flow does not add empty pages to meet the length range.
- `git diff --check` passed. The references gate recognized zero machine-indexed entries in the descriptive reference list; author verification therefore included reading the actual reference entries and their body citations rather than treating that zero as citation validation.

Proof copies, build and preflight logs, extracted text, and the count record
are preserved beneath `build/tpt-runs/e80cd019cbe2d2f4/artifacts/author-study-0000/`.
Raster evidence is in that directory's replaceable `rasters/` child. Its
contact sheets are
`rasters/build/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost/contact-sheets/sheet-001.png`
and `sheet-002.png`; full-page images are in the adjacent `pages/` directory.
This 21-page proof supersedes the preliminary 24-page author proof.

### Evidence read and limits preserved

The author read the reviewed local research and retained primary-source
passages used for the arguments: Augustine's John XVI and relevant psalm
expositions; Gregory's Latin Homily II.28.1–3; Chrysostom's Ephesians XIX,
including the distinct editorial note 404; Jerome on Daniel 3:29;
Bellarmine on Psalms 136 and 144; and Schuster's matching Sunday chapter,
volume III, pages 174–178. Reuse rests on those readings and the inspected
research evidence, not on a predecessor's PASS. No new retrieval or alteration
of the reviewed research was performed by this author stage. The textual
facsimile collations recorded in `propers/verified.md` remain research-stage
work; this entry does not claim a new independent facsimile collation.

The liturgical English retains its documented historical/public-domain
basis; the modern restricted witnesses are not reproduced. Biblical English
is distinguished from adapted chant Latin. The author's whole-Mass readings
are editorial syntheses: the Fathers are not represented as commentators on
this complete formulary. Gregory and Augustine's different estimates of the
ruler's initial faith remain visible, as does the disagreement between
Chrysostom and the NPNF editorial note over thanksgiving in affliction.
Schuster's actual Sunday exposition is distinguished from editorial treatment
of the Trinity Preface and the dated Marian commemoration.

Chronology preserves the reviewed distinctions between attribution,
composition, narrated event, historical background, and duration. The
Petavius alternative is retained only with its existing printed-page
verification limit. No unestablished precise occasion or writing site is
supplied for the psalms. The general-calendar occurrence does not settle a
local patronal/dedication calendar or current celebration permissions.

No new upstream research defect was established during this author audit.
Independent cold study review, derivation and review of the concise study and
homily, the final shared-timestamp three-document build, and independent
visual/publication review remain outstanding workflow stages.

## Concise study author proof — 5 October 2026

This records completed author work for `proper-study` version 9, run
`e80cd019cbe2d2f4`, stage `derive-synthesis`, iteration 0, packet SHA-256
`15b3a4498e5c5f7770d69c3547738739dfb816929c1f5d4ef5eefa6cfede032f`.
It is not the subsequent independent concise review or final visual acceptance.

`synthesis.tex` and its six declared `sections/concise/` components now
provide a standalone comparison derived from the expansive study. The
four-page opening contains the complete fourteen-element inventory with
the conditional Maternity branch, exactly four overview senses, the same
reviewed generated chronology, and a substantive two-page thematic movement.
Five cross-proper questions then interleave the witnesses' reasoning about
faith and signs, confession and suffering, divine provision and human
generosity, thanksgiving and lament, and sacramental healing and obedience.
The terminal scope, usable source loci, revision timestamp and rights
colophon complete the concise edition. The existing manifest already named
these exact paths and synthesis-only roles; it required no alteration.

The settled proof has **10 physical pages** and **3,784 substantive words**:
1,059 in the thematic movement and 2,725 in integrated commentary. The count
uses English prose tokens, excluding the inventory, overview table,
chronology, apparatus, headings, footnotes, labels and TeX commands.
Hyphenated compounds count separately. The earlier 9-page draft was developed
with further reasoning already present in the expansive study, including the
furnace's refusal to make fidelity conditional on rescue and Augustine's songs
of pilgrimage; no new research claim was introduced to obtain the extent.

### Exact concise proof and verification

The retained evidence directory is
`build/tpt-runs/e80cd019cbe2d2f4/artifacts/derive-synthesis-0000/`.

- PDF: `author-proof.pdf`, SHA-256
  `aaf119ae625f1204f99a08d3c1e63c1757540bb79d9de0b946c5abe3bea59b18`.
- Settled auxiliary file: `author-proof.aux`, SHA-256
  `89d1ce3d48a87698f8b7193ae57f93babe3d5347116e41189e4acb789f113269`.
- TeX log: `author-proof.log`, SHA-256
  `c95b4496f95b99cd56eff12335c8af4d6162ac0e33b1a54627a1857303b76f8e`.
- The mirrored build PDF is
  `build/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost-synthesis.pdf`;
  its bytes equal the retained proof.
- Finalization timestamp: `2026-10-05T16:25:22Z`. The shared generation
  record preserves the exact workflow provenance and prior contribution,
  and adds the actual concise author contribution.
- The required `make doc` synthesis build and synthesis artifact component
  gate passed. `build.log` and `artifacts-gate.log` retain their output.
  Physical zref evidence places inventory and all four overview rows on 1,
  chronology alone on 2, themes on 3–4, and developed commentary beginning on 5.
- Synthesis content preflight passed (`preflight.log`): all 24 bindings,
  the unchanged seven-element chronology projection, two per-passage dates,
  source and rights checks, component coverage, and house-voice checks.
  The reference screen recognizes no entries in this descriptive bibliography;
  its zero was not treated as proof of citations. The actual source notes
  were compared with the expansive study's loci.
- The settled TeX log contains no warnings, undefined references, overfull
  or underfull boxes. The build anchor check passed for all 14 entries.
  PDF structure and extraction were checked; all fonts are embedded, subset
  Latin Modern, letter paper, 469,604 bytes (well below both size triggers).
- Every page was opened at full-page raster size. The final small wording
  correction and timestamp were reinspected on pages 6 and 10, and the final
  ten-page contact sheet was inspected. Tables, body text, notes and colophon
  remain readable with no clipping, overlap, blank page or stranded heading.
  The final page contains substantial references as well as the colophon.
  Raster evidence is confined to the replaceable `rasters/` child; its full
  pages are under
  `rasters/build/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost-synthesis/pages/`,
  and `contact-sheets/sheet-001.png` is the adjacent overview.

### Derivation bounds

The author read the complete accepted expansive study, its research scope,
interpretation record, appointed texts and generated chronology rather than
treating its accepted verdict as the evidence. No new retrieval, source
collation, chronology regeneration or change to accepted study prose was
performed. Gregory and Augustine's different estimates of the ruler's
initial faith remain explicit, as does Chrysostom's disagreement with the
NPNF editorial note. Bellarmine's duties of generosity remain distinct from
Augustine's encouragement of the person waiting for help. The literal cure,
the spiritual senses, conditional Marian petitions and Trinity Preface retain
their separate roles. The complete generated historical-background dates and
their verification limits remain visible on the chronology page.

The recorded narrow coordinator correction removed a possible resurrection
implication from the concluding description of the child: the sentence now
says that he returns to health. No upstream defect was established in this
derivation. The shared timestamp means the earlier expansive author proof is
historical; the final three-document build must rebuild every consumer after
the homily and metadata settle. Independent concise review, homily production,
final artifact/visual review and installation remain subsequent workflow work.

## Homily author proof — 5 October 2026

This records completed author work for `proper-study` version 9, run
`e80cd019cbe2d2f4`, stage `derive-homily`, iteration 0, packet SHA-256
`5ead29da6cee0c02b9a8151ebd5eab6cd13a325aaf3dd2c50cf5e34225a62cea`.
It records neither independent homily acceptance nor the later visual review.

`homily.tex` and its two declared local components provide **The Journey
Home**, finished preaching for an adult parish assembly. The speech follows
`word-heals`, with the compatible lament-and-hope connection from
`song-exile`. John 4:50 supplies the decisive change in understanding:
the father begins to act on Christ's word before the servants' report in
4:51–53. The listener's desire to know an outcome before accepting a duty
is answered by this specific sequence, not by a general injunction to be
optimistic. The matching hour then shows the father that the child was
already healed during his journey; the servants' testimony and the whole
household's belief carry the final movement into shared faith. Ephesians
5:15–21 supplies wise conduct and mutual service;
the Collect, Secret and Postcommunion make pardon, healing and obedience
gifts to be sought. The Offertory and Communion keep this actual cure from
becoming a guarantee of bodily recovery for every petitioner. Replacing
these appointments would remove the narrative reversal, the two moments
of belief and the specific prayer sequence that carry the argument.

The body has **1,377 spoken words**, counted as English word tokens with
internal apostrophes retained and hyphenated compounds counted separately.
Only `sections/homily/10-body.tex` is counted. At an unhurried **115–125
words per minute**, the estimate is **11.0–12.0 minutes**. A silent
editorial read-through checked sense, transitions, intelligibility and
sentence cadence. No audible rehearsal or timed human delivery occurred.
The opening road image returns at the conclusion. One developed illustration,
an honest admission of fault, moves from relinquishing control of the answer
to sharing the fruit of pardon at home. No anecdote, clerical identity,
attributed invented speech or new recited prayer was supplied.

Both reviewed studies and their research records were read. The retained
Gregory II.28.1–3 Latin, Augustine Psalm 118 §§50–51, Chrysostom Ephesians
XIX's opening and concluding reciprocal-service passages, and Schuster's
Sunday discussion on pp.175–178 were inspected. The source roles and exact
loci remain those of the reviewed study. No new research, facsimile
collation or upstream prose repair is claimed. Gregory's description of
initial faith is attributed to him; Augustine contributes the distinct
promise-and-consolation argument. The two verbatim Gospel quotations match
the study's identified Douay–Rheims–Challoner witness. No upstream defect
was established. Both commemoration branches remain possible because the
speech does not assert that the conditional Marian prayers are always said.

### Author-stage intervention and superseded proof

The coordinator's recorded manual intervention 0001 identified repeated
application lists and a recurrent grace–Eucharist–one-action closing sequence.
The author read that intervention in full and revised the speech before
submission. The repeated lists and the closing one-action instruction were
removed. The final movement now develops the matching hour, Christ's mercy
already given, the servants' testimony and the household's belief. The
qualification about continued suffering remains. Only the accepted studies'
claims and sources were used, and the revised speech received another silent
sense-and-cadence reading. This was author-stage editorial feedback, not an
independent review verdict.

The actual 1,283-word pre-intervention body, apparatus and three-page PDF
are preserved under the proof directory's
`superseded-pre-intervention-1283/` child. That PDF's SHA-256 is
`5a4c069db18833d8b208b028a239572f8f84bde6bc5559b56453c50bf296367f`.
The earlier 1,285-word source was already overwritten and was not
reconstructed. The revised proof below supersedes both preliminary drafts.

### Exact revised homily proof and verification

The retained proof directory is
`build/tpt-runs/e80cd019cbe2d2f4/artifacts/derive-homily-0000/`.

- `author-proof.pdf`: **3 physical pages**, 270,020 bytes, SHA-256
  `f066abdb02582d6e74b35adc09eeccb48d034e3ea34551db651dc993cfc44405`.
- `author-proof.aux`: SHA-256
  `8eeefe0f97a33ab99b0c820a66a0d01281e4aab82c2922fc169dab80acb5429e`.
- `author-proof.log`: SHA-256
  `0091564a7aef6ed06258c8df323f34eec38c15aa9832813f28b89bf2f58e88f4`.
- The mirrored build PDF is
  `build/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost-homily.pdf`;
  its bytes equal the retained proof. The finalization timestamp is
  `2026-10-05T16:54:34Z`, with the exact run provenance and actual homily
  contribution recorded in the shared generation file.
- The homily `make doc` build, artifact component check and full homily
  content preflight passed. The log contains no warnings, overfull or
  underfull boxes, or undefined references. Both contents entries have
  their own anchors. The descriptive References list produces zero
  machine-indexed entries; its actual four entries and body uses were
  therefore checked directly, not accepted on that zero count.
- All three final full-page rasters were inspected after the intervention
  revision, and the final contact sheet was inspected. The
  full-width title precedes two columns of speech; the note, references,
  timestamp and readable rights colophon occupy page 3. No overlap,
  clipping, blank page or stranded heading was observed.
- Rasters remain exclusively below `rasters/`, with full pages under
  `rasters/build/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost-homily/pages/`
  and the adjacent `contact-sheets/sheet-001.png`.
- PDF structure, metadata and extracted text were checked. All ten fonts
  are embedded, subset Latin Modern; paper is letter. The short PDF
  exceeds the per-page size investigation trigger (about 87.9 KiB/page)
  but is only 263.7 KiB overall: it has no image objects, and its shared
  title, body and apparatus use the embedded font subsets. No independent
  PDF optimization was performed.

The final three-document build must rebuild every consumer of the shared
timestamp. Aggregate source-inventory refresh and `make check-sources`
remain coordinator integration work; this stage did not alter shared
integration records. Independent homily review, final artifact and visual
review, installation and publication remain subsequent workflow work.

## Final three-document artifact build — 5 October 2026

This records `proper-study` version 9, run `e80cd019cbe2d2f4`, stage
`build-artifacts`, iteration 0, packet SHA-256
`915272b0a412b26e35fb22c9b5641923469ec40b5b3fbd34f9e683a04a1fd0aa`.
The three required `make doc` commands passed with the shared finalization
record `2026-10-05T16:54:34Z`. The study and concise study were rebuilt;
the unchanged homily was already current. No accepted prose, evidence,
entrypoint, layout, generation metadata or content-review seal was edited.

| Final artifact | Physical pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Study | 21 | 492676 | `df4e168056800cea5d0836c98136dea4224c886ff1e8a3b75e953be211ce6d87` |
| Concise study | 10 | 469604 | `0626703ad457fbdb83297b310e3f2a21eed69b3d46d343cd2a50d06fd93a7ad3` |
| Homily | 3 | 270020 | `f066abdb02582d6e74b35adc09eeccb48d034e3ea34551db651dc993cfc44405` |

The final PDFs occupy the canonical mirrored paths beneath
`build/gpt/liturgy/roman-rite/1962/propers/temporal/`, with the bare
`60-twentieth-after-pentecost` name and its `-synthesis` and `-homily`
companions. Exact copies, auxiliary files, final TeX logs, recorder files,
PDF metadata, font reports, image inventories and extracted text are preserved
under `build/tpt-runs/e80cd019cbe2d2f4/artifacts/build-artifacts-0000/proofs/`,
named `study`, `synthesis` and `homily`. The enclosing directory holds the
build logs, artifact-check output, snapshot copy and `build-report.json`.
All preserved PDF copies were compared byte for byte with the final builds.

The three settled TeX logs contain no fatal errors, undefined references,
overfull or underfull boxes, or warnings. The build's anchor checks passed
for 41 study and 14 concise contents entries; the current homily proof retains
its two checked entries. The LaTeX kernel's informational notice that an old
`listings` first-aid patch is no longer applied is not a layout warning;
these publications contain no listings.

The final concise auxiliary evidence places inventory, overview and each of
its four sense markers on physical page 1, chronology on 2, themes on 3–4,
and commentary on 5. Both the component artifact check and the snapshot
artifact check passed, with presentation, shared format and author-standing
contracts required. The repository snapshot command wrote
`research/artifacts.json`, binding all three PDF hashes, render inputs and
pagination evidence. This receipt records bytes, not a visual verdict.

PDF parsing and metadata inspection used `pdfinfo`; extraction used
`pdftotext -layout`; font and image inventories used `pdffonts` and
`pdfimages -list`. All 34 extracted pages were inspected, with no blank
page, replacement character or NUL, and each edition displays the final
revision timestamp once. All fonts are embedded and subset Latin Modern,
with Unicode maps: 15 fonts in the study, 16 in the concise study and 10 in
the homily. All three PDFs are unencrypted letter-size PDF 1.7 without
JavaScript. The homily exceeds the 75 KiB/page size investigation trigger
at about 87.9 KiB/page, but is only 263.7 KiB overall and contains no image
objects; its ten font subsets account for the short document's overhead.
No independent PDF optimization was performed. `qpdf` and `mutool` were
unavailable; no checks with either tool are claimed.

`tools/tpt pdf-review` successfully prepared all 34 bounded full-page rasters
and four contact sheets under the dedicated replaceable
`build/tpt-runs/e80cd019cbe2d2f4/artifacts/build-artifacts-0000/rasters/`
child. Within it, each mirrored PDF stem has `pages/page-N.png` and
`contact-sheets/sheet-001.png`; the 21-page study additionally has
`sheet-002.png`. `review-run.json` records the exact input hashes and page
counts. These are the prepared artifacts for the following fresh visual
worker, not a claim of independent visual acceptance by this build stage.
No new upstream semantic defect was established during the build inspection.

`git diff --check` passed. Independent all-page visual review, installation,
canonical web work and publication checks remain subsequent workflow work;
aggregate source, catalog and release refresh remain coordinator work.

## Canonical web conversion — 5 October 2026

The `proper-study` version 9 `generate-web` stage, iteration 0, converted
the canonical study through `tools/tpt web-edition`. The generated file is
`build/web/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost.md`:
76,668 bytes, SHA-256
`f24141b7c8fe79ea1b0ea92b0485eabdaa978803932668946165e15882c4b31c`.
The repository snapshot command recorded those exact bytes in
`research/web-artifact.json`. No conversion or declaration repair was needed;
the accepted TeX sources and shared finalization timestamp remain unchanged.

The converter's source-graph, appointed-anchor, table, quotation, chronology,
footnote, link and metadata audits passed, as did the leaf's web-eligibility
check. The generated Markdown was read through, including both interpretations,
their distinct four senses, the comparison, historical appendix and terminal
apparatus. A separate structural check with the site's pinned Markdown renderer
confirmed 14 unique appointed-text targets, two interpretation targets, four
sense terms in each interpretation, 34 source footnotes and 34 generated notes,
28 separate blockquotes, and resolving internal links. All 34 substantial
source paragraphs containing no TeX commands were compared with normalized
rendered text and preserved. That bounded comparison supplements the
converter audits; it is not a claim of independent substantive acceptance.
The revision timestamp and rights notice appear once, and internal model and
run metadata are absent from the edition. No concise or homily web leaf was
created. Independent web evaluation and installation remain subsequent stages.

## Study reference repair and author proof — 5 October 2026

This records `proper-study` version 9, run `e80cd019cbe2d2f4`, stage
`author-study`, iteration 1, packet SHA-256
`8d4da23498ec5933a8f54c3196fa221c6b1d4c9273581d1a3bb2460c8760659d`.
WEB-001 is repaired in `sections/90-study-apparatus.tex`: Bellarmine's
reference now links to
`https://www.ecatholic2000.com/bellarmine/commentary-on-psalms.shtml`.
The named O'Sullivan 1866 translation and Psalm 136:1–4 and 144:14–17
loci are unchanged. A fresh complete GET returned HTTP 200; its 2,228,529
bytes have SHA-256
`c74854f03e4fa1e8d36ea55260a4ca84a5428419b923acd46c5172f2cd8f61d3`,
matching the registered full-text HTML artifact. The title, translation
identity and both Psalm headings were checked. This verifies the delivery
route and identity; it is not a new collation or research acceptance.

The coordinator's recorded intervention 0002 also authorized the existing
VIS-001 advisory repair. The newline space before footnote 34 in
`sections/40-song-exile.tex` was removed, attaching the callout directly to
the punctuation after “remembered.” The prose and citation are unchanged.
The historical finding retains its advisory severity; this intervention is
not an additional forwarded blocking finding. The chronology layout accepted
under VIS-002 was preserved. No research evidence, interpretation plan,
companion prose, source binding or historical review record was altered.

The shared finalization timestamp is `2026-10-05T17:56:39Z`, and the
generation record adds this repair's actual contribution while preserving
the run provenance and earlier contributions. The study still contains
**6,338 substantive words**, recomputed with the earlier source-token method
and exclusions. Its two readings, fourteen-element scope, source limits,
rights qualifications and conditional commemoration remain unchanged.

- Canonical proof: `build/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost.pdf`.
- Preserved proof: `build/tpt-runs/e80cd019cbe2d2f4/artifacts/author-study-0001/author-proof.pdf`.
- Both copies: **21 physical pages**, 492,811 bytes, SHA-256
  `abc824e7f341eaba7b242d5a74bf5d381b749ece9cd5e331a575c137dc3d87af`.
- The required study `make doc`, research artifact component check and
  research content preflight passed. The preflight validates all 24 source
  bindings and the current seven-element chronology projection. Its zero
  machine-indexed bibliography entries is not a claim of citation review.
- The settled TeX log contains no warnings, undefined references, overfull
  or underfull boxes. PDF metadata, text extraction, embedded Latin Modern
  fonts and the rendered Bellarmine link destination were checked.
  `pdftohtml` extracted the corrected URI from the PDF annotation.
- Every full-page raster, pages 1–21, was inspected. Footnote 34 now stays
  attached on page 16, and the corrected reference and final colophon are
  readable on page 21. No clipping, overlap or blank page was observed.
  Exact raster comparison with the prior artifact build shows only pages
  16 and 21 changed; chronology pages 18–19 remain byte-identical rasters.
- Proof, log, auxiliary and recorder copies, extraction and font reports,
  repair evidence, page-comparison record and word count are retained in
  the iteration's artifact directory. Rasters occupy its exclusive
  replaceable `rasters/` child. Prior iteration artifacts were preserved.
- `git diff --check` passed. An optional Python PDF-library inspection was
  unavailable because `pypdf` is not installed; Poppler's link extraction
  supplied the actual annotation check instead.

This is author verification, not renewed independent acceptance. The
workflow must rederive and review both companions, rebuild all three
consumers of the shared timestamp, and regenerate and review the canonical
web edition. No generated Markdown was patched. Aggregate source, catalog
and release refresh and `make check-sources` remain coordinator integration
work. No new upstream research defect was established in this repair.


## Renewed concise derivation and author proof — 5 October 2026

This records `proper-study` version 9, run `e80cd019cbe2d2f4`, stage
`derive-synthesis`, iteration 1, packet SHA-256
`f8ceb82bb7e7d0d566ad34e6278b1f86d36c8071e9826995fd96b4fe1f114b22`.
The complete current expansive study and concise study were read together,
with the interpretation audit, research scope and generated chronology.
The study repair changed a Bellarmine URL and attached its existing
footnote 34; it changed no argument or source locus requiring a new concise
formulation. The concise reference already identifies O'Sullivan's 1866
translation and the correct psalm loci without the replaced URL.

The entrypoint, all six concise components, common manifest and generated
chronology remain byte-identical to the iteration-0 concise source record.
Both controlling interpretations, their interleaved reasoning, their
meaningful disagreements, the conditional Marian branch and all fourteen
appointed elements remain present. No evidence-dependent claim, research
record or accepted study component was revised. The shared revision stays
`2026-10-05T17:56:39Z`: this iteration changed no rendered source. A distinct
nonrendered contribution records the actual renewed comparison and proof
verification. A rebuild after that declaration reproduced the reviewed PDF
byte for byte.

The repeated source-token count is **3,784 substantive words**, comprising
1,059 in the themes and 2,725 in commentary. It uses the earlier method:
English prose tokens, excluding headings, notes, TeX commands, inventory,
overview, chronology and apparatus, with hyphenated compounds separated.

The preserved proof directory is
`build/tpt-runs/e80cd019cbe2d2f4/artifacts/derive-synthesis-0001/`.

- `author-proof.pdf`: **10 physical pages**, 469,604 bytes, SHA-256
  `3b3437ccabc41ad73cd3be6072fb4d90ada392e65fdc5cd1f05bbc42236d67b7`.
- `author-proof.aux`: SHA-256
  `89d1ce3d48a87698f8b7193ae57f93babe3d5347116e41189e4acb789f113269`.
- `author-proof.log`: SHA-256
  `1ec5a28d336caa057f363181b58db168f0f6af1c56cd389fed74c0ae2bfc0a17`.
- Both `make doc` builds, the synthesis artifact component checks and full
  synthesis content preflight passed. The preflight validates 24 source
  bindings and the current seven-element chronology. Its zero machine-indexed
  reference entries does not verify the descriptive bibliography; the actual
  concise loci were compared with the expansive source's references.
- Settled zref labels place inventory and the four overview senses on page 1,
  chronology alone on 2, themes on 3–4, and commentary starting on 5.
  The final TeX log has no warnings, undefined references or box overflows.
- PDF parsing, extraction, metadata and font inventories were inspected.
  All sixteen fonts are embedded subset Latin Modern with Unicode maps.
  The letter-size PDF contains no image objects and falls below the size
  investigation thresholds. It displays the shared revision exactly once.
- All ten full-page rasters were opened and inspected. Tables, notes and
  final colophon are readable without clipping or overlap. Pages 1–9 are
  byte-identical rasters to the prior concise proof; page 10 changes only
  the shared revision timestamp. Dedicated raster evidence remains under
  `rasters/`; proofs, logs and hash comparisons are outside that replaceable
  child. Prior artifacts were preserved.
- `git diff --check` passed. No upstream defect was established; no new
  retrieval, facsimile collation or external source verification is claimed.

This is renewed author verification. Independent concise review, subsequent
homily derivation and review, final three-document artifact/visual checks and
web/publication work remain the workflow's responsibility. Aggregate source,
catalog and release refresh and `make check-sources` remain coordinator work.

## Renewed homily derivation and author proof — 5 October 2026

This records `proper-study` version 9, run `e80cd019cbe2d2f4`, stage
`derive-homily`, iteration 1, packet SHA-256
`cc7787d5b528651d9d15d753a786707e03b1f9a9be7c59a97a2f379788f7eacc`.
Both current studies were read completely, together with their appointed
texts, interpretation audit and the relevant research evidence. The study's
Bellarmine URL and footnote-attachment repairs change no claim carried by
the homily. Its entrypoint, spoken component, source-and-delivery component
and component manifest remain unchanged. No new source-dependent claim or
upstream repair was introduced.

The renewed derivation retains `word-heals` as the governing reading and
the compatible lament-and-hope contribution of `song-exile`. The decisive
detail is still the departure in John 4:50 before the report in 4:51–53:
the listener's wish to control an outcome before accepting a duty gives
way to trust in the Lord whose word directs action. The matching hour
then identifies mercy already given, and household belief makes its fruit
communal. Ephesians 5:15–21 gives this trust wise conduct and mutual service;
the Collect, Secret and Postcommunion give it pardon, healing and obedience
received from Christ. The Offertory's tears and Communion's consolation
prevent the particular cure from becoming a guarantee of bodily recovery.
These specific textual movements would disappear with unrelated readings.

Gregory II.28.1–3 was reread in the retained Latin transcription;
Augustine's Psalm 118 §§50–51 in the retained NPNF English; Chrysostom's
Ephesians XIX opening and concluding mutual-service exposition in NPNF;
and Schuster's Sunday exposition, pp.174–178, in the retained OCR.
The latter is a renewed reading of the argument, not fresh image collation.
The two Gospel quotations were compared with the study's identified
Douay–Rheims–Challoner wording. Gregory supplies the initial-faith account;
Augustine supplies the distinct promise-and-consolation argument. No
additional retrieval, source-library mutation or new facsimile verification
is claimed. No upstream defect was established.

A fresh count confirms **1,377 spoken words**, using English tokens with
internal apostrophes retained and hyphenated compounds separated, solely
from the spoken component. At **115–125 words per minute**, the estimate
remains **11.0–12.0 minutes**. A silent editorial read-through checked
sentence sense, transitions and oral clarity; no audible rehearsal or timed
human delivery occurred. The finished speech ends with the household's
shared faith and the fruit of mercy, without an invented recited prayer.

The shared revision remains `2026-10-05T17:56:39Z`, since this iteration
changes no rendered source. The generation record adds the actual renewed
homily contribution without altering provenance or earlier contributions.
Proof evidence is retained under
`build/tpt-runs/e80cd019cbe2d2f4/artifacts/derive-homily-0001/`:

- `author-proof.pdf`: **3 physical pages**, 270,020 bytes, SHA-256
  `dce7cd982b53f153098d0ace7ac2f5aaa0aa7b7b9b57d11427c2b91dfe9aa24f`.
- The `make doc` homily build, artifact component check and complete homily
  content preflight passed. The preflight validates all 24 source bindings;
  its zero machine-indexed reference entries does not validate the
  descriptive bibliography. The actual references and cited loci were read.
- The settled TeX log has no warnings, undefined references or overfull or
  underfull boxes. Both contents entries have their own anchors. PDF parsing,
  extraction and metadata checks passed; all ten font subsets are embedded
  Latin Modern with Unicode maps, and the PDF has no image objects.
- The approximately 87.9 KiB/page size exceeds the per-page investigation
  trigger because ten font subsets serve a short, 263.7 KiB document; the
  image inventory is empty. No independent PDF optimization was performed.
- Every full-page raster was opened and inspected. The full-width title,
  two-column speech, separate terminal note and references, timestamp and
  final colophon are legible without clipping, overlap or blank pages.
  Pages 1–2 are byte-identical rasters to the prior author proof; page 3
  carries the current shared timestamp. Exact source hashes, word count,
  page comparisons, PDF reports, logs and proof copies are outside the
  dedicated replaceable `rasters/` child. Prior evidence was preserved.

This is renewed author verification, not independent homily acceptance or
final visual acceptance. Subsequent artifact, visual, web and publication
work belongs to the workflow; aggregate source, catalog and release refresh
and `make check-sources` remain coordinator integration work.

## Renewed three-document artifact build — 5 October 2026

This records `proper-study` version 9, run `e80cd019cbe2d2f4`, stage
`build-artifacts`, iteration 1, packet SHA-256
`0210221df9276a07366117c80acbf9f714224589163bf96d950bf60b3e4ea6f9`.
All three required `make doc` commands passed against the current shared
revision `2026-10-05T17:56:39Z`. No accepted prose, evidence, layout,
entrypoint, generation metadata or content-review seal was edited.

| Final artifact | Physical pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Study | 21 | 492811 | `abc824e7f341eaba7b242d5a74bf5d381b749ece9cd5e331a575c137dc3d87af` |
| Concise study | 10 | 469604 | `3b3437ccabc41ad73cd3be6072fb4d90ada392e65fdc5cd1f05bbc42236d67b7` |
| Homily | 3 | 270020 | `dce7cd982b53f153098d0ace7ac2f5aaa0aa7b7b9b57d11427c2b91dfe9aa24f` |

The final build paths remain beneath
`build/gpt/liturgy/roman-rite/1962/propers/temporal/`, using the bare
`60-twentieth-after-pentecost` name and its `-synthesis` and `-homily`
companions. Byte-identical preserved copies occupy
`build/tpt-runs/e80cd019cbe2d2f4/artifacts/build-artifacts-0001/proofs/`,
as `study.pdf`, `synthesis.pdf` and `homily.pdf`. Each has adjacent final
auxiliary, log, recorder and contents files, extracted text, PDF metadata,
font and image reports. The enclosing directory retains the build logs,
component and artifact check logs, snapshot copy and `build-report.json`.
Earlier stage and iteration evidence was preserved.

The settled logs contain no fatal errors, undefined references, overfull
or underfull boxes, unresolved references or layout warnings. The build's
metadata and component checks passed. The concise auxiliary evidence places
inventory, overview and all four sense markers on physical page 1,
chronology on 2, themes on 3–4 and commentary on 5. The component artifact
check and proper-study artifact check passed, the latter requiring the
presentation, shared-format and author-standing contracts. The repository
snapshot command refreshed `research/artifacts.json` from the actual PDFs,
render inputs and pagination evidence; the snapshot asserts bytes, not a
visual-review verdict.

All 34 extracted pages were read for build integrity. No empty page,
replacement character, NUL, missing terminal timestamp or apparent extraction
loss was found; the shared revision appears once in each edition. Poppler
`pdfinfo` parsed all three as unencrypted letter-size PDF 1.7, with no
JavaScript and the declared modification time. `pdffonts` reports embedded,
subset Latin Modern fonts with Unicode maps throughout: 15 in the study,
16 in the concise study and 10 in the homily. `pdfimages -list` reports no
image objects. The homily's 87.9 KiB/page exceeds the size investigation
trigger, while its total is only 263.7 KiB; ten font subsets supply overhead
for three pages. No independent PDF optimization was performed. `qpdf` and
`mutool` are unavailable; no checks with those tools are claimed.

`tools/tpt pdf-review` prepared 34 full-page rasters and four bounded contact
sheets under the exclusive replaceable
`build/tpt-runs/e80cd019cbe2d2f4/artifacts/build-artifacts-0001/rasters/`
child. Each mirrored PDF stem there contains `pages/page-N.png` and
`contact-sheets/sheet-001.png`; the study also has `sheet-002.png`.
`review-run.json` binds the input hashes and page counts. This is preparation
for the following fresh visual worker, not independent all-page visual
acceptance. No new upstream semantic defect was established in this build
inspection. Installation, renewed canonical web work and publication checks
remain later workflow work; shared source, catalog and release refresh
remain coordinator integration work.

## Reviewed family installation — 5 October 2026

This records `proper-study` version 9, run `e80cd019cbe2d2f4`, stage
`install-publication`, iteration 0, packet SHA-256
`0079664c1e16710fc87a05e3715bef49ad19c219fe0415a6a0eaa2b57e3f9829`.
It records completed installation and wiring, not terminal workflow acceptance
or deployment.

The engine results beneath `build/tpt-runs/e80cd019cbe2d2f4/results/`
record `PASS` for `research-review-0001.json`, `study-review-0001.json`,
`synthesis-review-0001.json`, `homily-review-0001.json`,
`visual-review-0001.json` and `web-review-0001.json`. Those actual results
were read for this installation. The research re-review resolved RES-001
and RES-002 using the retained identified witnesses; it did not reverify
live USCCB delivery after the reported HTTP 403. The first web review's
WEB-001 Bellarmine URL defect returned to the study owner, followed by renewed
study and companion reviews, artifact build, visual review, conversion and web
review. The final visual result records inspection of all 34 full-page
rasters. The final web result records desktop/mobile rendering, note navigation
and all twelve external destinations. These are the respective reviewers'
recorded events, not new source, visual or browser reviews by the installer.

The artifact check passed before installation. Each of the three prescribed
`make install-doc DOC=<id> PROVIDER=gpt` invocations then passed with normal
dependencies and checks. No dependency suppression, timestamp adjustment,
accepted-source edit or receipt refresh was used. Build and installed bytes
were compared with the immutable visual-review PDF hashes and matched:

| Installed PDF under `pdf/gpt/liturgy/roman-rite/1962/propers/temporal/` | Pages | SHA-256 |
| --- | ---: | --- |
| `60-twentieth-after-pentecost.pdf` | 21 | `abc824e7f341eaba7b242d5a74bf5d381b749ece9cd5e331a575c137dc3d87af` |
| `60-twentieth-after-pentecost-synthesis.pdf` | 10 | `3b3437ccabc41ad73cd3be6072fb4d90ada392e65fdc5cd1f05bbc42236d67b7` |
| `60-twentieth-after-pentecost-homily.pdf` | 3 | `dce7cd982b53f153098d0ace7ac2f5aaa0aa7b7b9b57d11427c2b91dfe9aa24f` |

The canonical conversion was copied byte for byte from
`build/web/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost.md`
to `web/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost.md`
and staged in Git. Both match the accepted web hash
`c812431a575cf7705e1e9597fb0a19e5be8df76ab35a3841d56c2c330f50acd8`.
There is no companion web authority. The shared source timestamp remains
`2026-10-05T17:56:39Z`; the accepted generation record, artifact receipt and
web receipt remain unchanged.

The three normal `make add-publication` invocations created records under
`release/publications/gpt/liturgy/roman-rite/1962/propers/temporal/`, named
`60-twentieth-after-pentecost.json`,
`60-twentieth-after-pentecost-synthesis.json` and
`60-twentieth-after-pentecost-homily.json`. Each names its exact output ID,
`library/traditional-latin-mass.md`, status `alpha` and standing authorization
`perpetual-public-repository-2026`. The existing Sunday 60 row now has
`Full PDF`, `Synthesis PDF`, `Homily PDF` and `Read` links in the ChatGPT
cell, preserving the Claude cell. Exactly one unqualified canonical marker
was added under the manifest's primary-provider rule.

The leaf-scoped proper-study publication check passed after installation and
wiring, including current artifact and web receipts, all installed/build byte
comparisons, exact records, catalog links, tracked Markdown and web eligibility.
The aggregate document catalog, source inventories, source-reader data and
scoped release bindings are serialized coordinator integration work. Their
refresh and global checks, and the actual terminal engine gate, are not claimed
by this installation audit. No commit, push, deployment or timed human homily
delivery is recorded here.

## Terminal workflow acceptance — 5 October 2026

Actual `proper-study` v9 run `e80cd019cbe2d2f4` reached terminal
`ACCEPTED` after `publication-gates-0000`. The engine returned “Workflow
complete. All stages passed.” with no escalations. This records the actual
local workflow result; it is not a deployment claim.

The accepted sequence includes fresh research review iteration 1, study
review iteration 1, concise review iteration 1, homily review iteration 1,
visual review iteration 1 and web review iteration 1. The final content,
visual and web reviews had no findings. The visual reviewer inspected all
34 full-page rasters and four contact sheets. The web reviewer checked the
complete canonical text/PDF relationship, both desktop and phone layouts,
fourteen proper anchors, 34 note/backlink pairs and twelve external URLs,
all returning HTTP 200. Browser and driver were stopped afterward. These
bounded checks do not claim physical printing, an audible timed rehearsal,
a real mobile-device test or an assistive-technology audit.

Normal Make installation preserved the exact reviewed bytes:

| Output | Pages | SHA-256 |
| --- | ---: | --- |
| Expansive study | 21 | `abc824e7f341eaba7b242d5a74bf5d381b749ece9cd5e331a575c137dc3d87af` |
| Concise study | 10 | `3b3437ccabc41ad73cd3be6072fb4d90ada392e65fdc5cd1f05bbc42236d67b7` |
| Homily | 3 | `dce7cd982b53f153098d0ace7ac2f5aaa0aa7b7b9b57d11427c2b91dfe9aa24f` |

The installed PDF paths use the prefix
`pdf/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost`
with the exact suffixes `.pdf`, `-synthesis.pdf` and `-homily.pdf`.
The canonical `web/gpt/liturgy/roman-rite/1962/propers/temporal/60-twentieth-after-pentecost.md`
is byte-identical to its reviewed build output, SHA-256
`c812431a575cf7705e1e9597fb0a19e5be8df76ab35a3841d56c2c330f50acd8`.
Three exact per-publication records and the GPT catalog cell were installed;
the shared owning-tool refreshes were serialized with the coordinator. The
terminal gate passed reviewed snapshot currency, installed/build identity,
release bindings, public-alpha eligibility, deterministic document catalog
and canonical web freshness.

The authoritative manifest, bootstrap, state, events, packets, submitted
results, gate logs and interventions are preserved byte for byte in
`workflows/reviews/gpt-1962-60-production-2026-10-05/accepted-run-e80cd019cbe2d2f4/`.
Its 171 copied files total 3,385,876 bytes; `FILES.sha256` has SHA-256
`6d55f91e51efeba343493fb6ada2aa0e41e00b498ef77e1c240f1dfb47363ad2`.
No private-path redaction was required in that record set. Earlier failed
findings, the held superseded run and superseded author proofs remain
historical evidence; they were not rewritten as successful reviews.

This terminal audit append changes only this nonrendered research record.
The coordinator will refresh its inventory fingerprint and perform final
aggregate integration checks. It does not change any accepted source prose,
PDF, web output, generation timestamp or review receipt.
