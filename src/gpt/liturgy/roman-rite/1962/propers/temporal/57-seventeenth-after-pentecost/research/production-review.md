# Production and review record

This record reports completed production events for `proper-study` run
`80a724fb8410dc3d`, version 1, workflow digest
`1375f708d8670b2f4ccaf1869cfaa6fe67fe6946dc2b962c766bcdc499d3b47e`,
seeded at commit `af9b2d10a98a6aac2ce44cc84d6358ede8e630e8`.
It does not substitute for an evaluator result or terminal acceptance.

## Completed stages

| Stage | Iteration | Recorded result | Disposition |
| --- | ---: | --- | --- |
| scope-gate | 0 | Authorized identity and dated scope | PASS |
| resolve-context | 0 | Context, inventory and source plan | PASS |
| research | 0 | Research records submitted | PASS |
| research-preflight | 0 | `GATE-RESEARCH-RECORDS`: declaration included controls outside source owners under `src/` | FAIL |
| research | 1 | Removed workflow review receipts and `THIRD_PARTY.md` from the source-owner dependency array; preserved their distinct audit/control roles | PASS |
| research-preflight | 1 | Corrected dependency declaration and evidence snapshot | PASS |
| research-review | 0 | Fresh independent source review; initial RES-001 withdrawn after full-resolution image reinspection | PASS |
| author-study | 0 | Canonical study and author proof submitted | PASS |
| study-preflight | 0 | Schema, evidence, prose and provenance checks | PASS |
| study-review | 0 | Fresh whole-study, interpretive-coherence and citation review; all 14 sealed files unchanged | PASS |
| derive-synthesis | 0 | Concise interleaved study and author proof submitted | PASS |
| synthesis-preflight | 0 | Concise component, evidence, prose and provenance checks | PASS |
| synthesis-review | 0 | Fresh interleaving, compression and source-fidelity review; eight sealed files unchanged | PASS |
| derive-homily | 0 | Spoken homily, separate source/delivery note and author proof submitted | PASS |
| homily-preflight | 0 | Homily component, evidence, prose and provenance checks | PASS |
| homily-review | 0 | Fresh spoken-text, exegesis, pedagogical and fidelity review; eight sealed files unchanged | PASS |
| build-artifacts | 0 | Final PDFs and exact source/artifact snapshot prepared | PASS |
| artifact-gates | 0 | Mechanical three-artifact checks | PASS |
| visual-review | 0 | Exact PDFs and all 32 full-page rasters independently inspected | PASS |
| generate-web | 0 | Canonical Markdown converted, compared and snapshotted | PASS |
| web-review | 0 | Full fidelity and rendered desktop/mobile review; WEB-001 superscript display | CHANGES_REQUIRED |
| generate-web | 1 | WEB-001 repaired through reviewed converter; exact new receipt | PASS |
| web-review | 1 | Full fidelity, desktop/mobile rendering and repaired verse superscripts | PASS |
| install-publication | 0 | Exact reviewed bytes installed; scoped wiring and actual shared refresh verified | PASS |
| publication-gates | 0 | STALE-STUDY-REVIEW: five layout-source changes require current-byte source approval | FAIL |
| author-study | 1 | Current source verified and resubmitted; independent stale-seal repair still pending | PASS |
| study-preflight | 1 | Current study mechanical checks | PASS |
| study-review | 1 | Fresh independent current-source and argument review; all 14 sealed inputs unchanged | PASS |
| derive-synthesis | 1 | Existing concise study independently verified by fresh author and retained unchanged | PASS |
| synthesis-preflight | 1 | Current concise-study mechanical checks | PASS |
| synthesis-review | 1 | Fresh independent complete concise-study/source comparison; eight sealed inputs match | PASS |
| derive-homily | 1 | Existing spoken homily freshly verified against both studies and retained unchanged | PASS |
| homily-preflight | 1 | Current homily mechanical checks | PASS |
| homily-review | 1 | Fresh independent spoken-argument and exact-source review; eight sealed inputs match | PASS |
| build-artifacts | 1 | Current 23/5/4-page PDFs rebuilt after operator labels; exact snapshot and 32 rasters | PASS |
| artifact-gates | 1 | Current three-PDF mechanical artifact checks | PASS |
| visual-review | 1 | Fresh independent inspection of all 32 current PDF pages and exact artifact inputs | PASS |
| generate-web | 2 | Current canonical conversion with ten explicit unique source and HTML element anchors | PASS |
| web-review | 2 | Full current canonical conversion, ten anchors and desktop/mobile browser review | PASS |
| install-publication | 1 | Current accepted bytes installed; scoped wiring, staged web and shared completion verified | PASS |
| publication-gates | 1 | STALE-STUDY-REVIEW after ten operator labels; actual source-owner route | FAIL |
| author-study | 2 | Anchored source verified and resubmitted unchanged; fresh independent acceptance still pending | PASS |
| study-preflight | 2 | Current anchored study mechanical checks | PASS |
| study-review | 2 | Fresh independent complete content/source approval of current anchored study; 14 files match | PASS |
| derive-synthesis | 2 | Current concise companion freshly compared and preserved unchanged; renewed study seal intact | PASS |
| synthesis-preflight | 2 | Current concise-study mechanical checks | PASS |
| synthesis-review | 2 | Fresh complete concise-study and cited-source review, five proof pages inspected, eight inputs match | PASS |
| derive-homily | 2 | Homily freshly verified and retained unchanged; current study seals and 19 render inputs match | PASS |
| homily-preflight | 2 | Current homily mechanical checks | PASS |
| homily-review | 2 | Fresh exact-source and spoken-argument review; eight sealed inputs and both upstream seals match | PASS |
| build-artifacts | 2 | Actual Make and all artifact checks; byte-identical PDFs and 19 render inputs, fresh 32 rasters | PASS |
| artifact-gates | 2 | Current three-artifact mechanical checks | PASS |
| visual-review | 2 | Fresh independent full-page inspection of all 32 current pages and receipt/input integrity | PASS |
| generate-web | 3 | Actual current canonical conversion and snapshot; complete 71024-byte output unchanged | PASS |
| web-review | 3 | Independent current-source and browser review; 238 blocks, 50 notes, ten anchors, all superscripts and fourteen desktop/mobile proof images; no findings. | PASS |
| install-publication | 2 | Exact normal Make installs and canonical web copy match all accepted bytes; 53 current sealed inputs and scoped publication/catalog/release wiring verified; shared final source refresh remains pending. | PASS |
| publication-gates | 2 | Actual terminal gate passed all current-source seals, exact three-document publication, release, scoped public-alpha/catalog and global web-current checks; engine terminal ACCEPTED with no escalations. | PASS |

Fresh worker dispatches use the effort declared by their compiled packets:
`high` for authors and `xhigh` for cold reviewers. Research review passed with
no findings. The entries below record subsequent artifact, visual, web and
installation events. The two failed publication gates routed changed study
inputs to real owner reentry and independent review; study-review iteration 2
has now approved the current anchored source. Its downstream chain is still
in progress; final workflow acceptance and human delivery are not claimed.

The initial, unsubmitted research review alleged a missing first `et` at
Matthew 22:37 in Pustet 1862, printed p. 342. Independent inspection located
the conjunction at the right end of the line. The same reviewer reopened
both witnesses at original resolution and withdrew RES-001 before submission;
the correct 1962 wording and all evidence records remained unchanged. The
initial raw report is retained distinctly from the engine-accepted result,
and no stale-input transition occurred.

## Retained engine evidence

[Exact result files and packet/result hashes](../evaluations/proper-study-results/80a724fb8410dc3d/record.md)
preserve the engine-retained JSON bytes after successful submission, including
failures. Review seals, when present, are injected by the engine rather than
authored by a worker. Build directories remain disposable.

## Scope and outstanding production

The production is exclusively the 1962 Seventeenth Sunday after Pentecost,
studied for 20 September 2026 under the universal calendar without a specified
local calendar. The intended outputs are an expansive study, concise
interleaved comparison and an adult-parish homily of approximately 10–12
minutes. The entries below record substantive word counts, estimated delivery,
rendered page counts, artifact hashes and completed checks at their actual
production stages. Current source limits remain in `scope.md` and the
source-specific audit records.

## Author-study, iteration 0 — 17 September 2026

The canonical expansive study is complete for author-stage submission. It
contains a substantive opening and ten-element map, the complete collated
Latin proper, canonical Douay–Rheims study English and Cummiskey's three
historical English orations, detailed commentary on all ten elements, three
whole-formulary interpretations with distinct four-sense distillations, a
concluding comparison, and terminal scope and used references. The schema-2
manifest declares the three future outputs and their separate components;
only the research-mode entrypoint and fragments have been authored in this
stage. No companion prose was created or accepted.

The substantive word count is **7,443**: opening and map 522; element
commentary 1,900; healed charity 1,464; gathered people 1,523; faithful
offering 1,672; final comparison 362. The count uses Pandoc's LaTeX abstract
syntax tree, excludes headings, footnotes, raw commands, the entire
appointed-text component and terminal apparatus, and includes the opening
map. Quoted proper text and bibliography do not supply the study's extent.

The canonical study uses 11-point Palatino-compatible text through
`mathpazo`, a 1.12 line-spread factor, one-inch side margins, and restrained
running headers. The shared preamble also loads Latin Modern. No new
ornamental macros or graphic dependencies were introduced. A 26-page
author proof compiled, its terminal path overflows were repaired using
breakable paths, and two subsequent passes settled without overfull or
underfull boxes or LaTeX/package warnings. Exact Latin paragraphs were
mechanically compared with `propers/verified.md`; all matched. The biblical
English was copied programmatically from the bound verse payloads, retaining
canonical verse numbers and the distinctions from the adapted Latin.

Completed author checks: research-edition schema-2 component validation;
all research-edition content-preflight checks (including 24 valid bindings,
three whole-formulary lanes, 12 used reference entries, house voice, rights
and structural labels); exact workflow/header provenance; canonical web
eligibility; and the author proof's PDF/revision/display metadata. The
single generation record repeats this run's actual header and discloses the
exposed GPT-6 identity and high effort without inventing an exact variant or
client version.

This author proof is not the workflow's final build or a visual acceptance.
No page-by-page visual review, installation, web conversion, publication
acceptance, or human delivery is claimed. The final artifact stages still
own those events. No research evidence was changed during authoring.
Source limits remain those in `scope.md`: abridged historical translations,
Jerome/Bellarmine transcription limits, no direct ancient commentary on the
exact orations established, no inferred compiler intent, and no specified
local calendar. All three interpretations are editorial whole-Mass
constructions, not arguments attributed as a whole to an ancient author.

## Derive-synthesis, iteration 0 — 17 September 2026

The concise study, *Love Received and Lived*, is complete for author-stage
submission. Five cross-proper movements compare the same three readings at
the Gospel's command and lordship, grace-enabled love, common prayer,
continuing fidelity, and eternal healing. The comparisons retain the
questioner's possible motives, Chrysostom's alternative meanings of one
spirit, created and spiritual heavens, Head-and-members prayer, Jerome's
alternative accounts of confession, common fidelity and particular vows,
and Bellarmine's and Augustine's differing emphases on judgment. The four
senses remain distinguishable for each reading. No new evidence-dependent
claim or source was introduced, and no accepted study or research prose was
changed.

The substantive word count is **1,686**, or **22.65%** of the expansive
study's 7,443 words. Pandoc's LaTeX abstract syntax tree supplies the count:
space-separated prose tokens in the concise body, excluding headings,
footnotes, raw commands, and the separate terminal apparatus. The result is
within both the ordinary 1,500–2,500-word range and the approximate one-third
limit; no exception is needed. The terminal apparatus gives scope, source
limits and six used bibliographic entries, followed by the shared timestamp
and common rights colophon.

The already declared synthesis-only component paths and mode membership
match the authored include graph and passed content-phase component
validation. The common generation record now includes the actual concise
authoring contribution and the finalization timestamp
`2026-09-17T20:50:33Z`; it preserves the packet's exact workflow provenance
and seed commit. No source-library, shared-tooling, or inventory changes
were made.

Completed author checks: all synthesis-edition content-preflight checks,
including 24 valid bindings and six used reference entries; explicit
header/provenance comparison; and PDF generation-metadata validation.
The final five-page author proof settled over two successive passes without
LaTeX/package warnings, overfull or underfull boxes, or undefined references.
Its SHA-256 is
`0d10c8c36a5506e58efc5e2d99c93b33523bb1d357f919abdca57b28607cded7`.
All fonts are embedded. Author inspection opened all five final page
rasters; the body uses the study's 11-point type, while the compact terminal
source note uses 10-point type. The final page carries the readable rights
colophon with the references; there is no rights-only spill page. Widow and
club penalties avoid isolated single-line paragraph fragments.

This is an author proof and inspection, not the workflow's independent
concise review or final visual acceptance. Those stages, final builds,
installation and publication remain outstanding. The shared timestamp
changes all three eventual artifacts' metadata; final artifact production
must rebuild every consumer from the finalized common record.

## Derive-homily, iteration 0 — 17 September 2026

The standalone homily, *The Heart That Learns to Love*, is complete for
author-stage submission. It addresses an adult parish assembly in continuous
spoken prose. Its governing reading is `healed-charity`, with compatible
applications of shared baptism from `one-people` and continuing fidelity from
`faithful-offering`. Both reviewed studies were read in full. The speech
connects Matthew's two love commands and David's Son/Lord dialogue, Paul's
patient charity, and the Introit, Collect, Secret and Postcommunion. An opening
moment before a potentially hurtful sentence returns at the conclusion;
the practical response is one concrete act of patient charity. No anecdote,
personal experience, clerical identity, composed prayer, new source-dependent
claim, or repair to accepted upstream prose was introduced.

The spoken body contains **1,283 words**, counted as whitespace-separated
tokens in its prose-only component. Title, source note, references and metadata
are excluded. At 110–120 words per minute the estimated delivery is
**10.7–11.7 minutes**. This is not a timed human delivery. A silent editorial
reading checked the sense and oral flow of every paragraph, including the
transition from command to prayer, the explanation of Christ's lordship,
the distinction between sacramental preservation and automatic immunity,
and the final return to the opening image. No audible or human rehearsal
is claimed.

Exact sources used, with edition details in the terminal References:

- *Missale Romanum* (1962), pp. 398–400, nos. 1602–1611, especially
  Introit, Collect, Secret and Postcommunion; American 1899 Douay–Rheims,
  Matthew 22:34–46, Ephesians 4:1–6 and Psalm 118:124,137.
- Augustine, *De doctrina christiana* I.22.20–21 and *Expositions on the
  Psalms*, Psalm 118, English paragraph 123 (NPNF1 volume 8's Psalm 119).
- Chrysostom, *Homilies on Matthew* 71, opening exposition of 22:37–46.
- Thomas, *Super Ephesios* 4, lecture 1, Dessain volume 2 (1857),
  pp. 312–315; *Summa theologiae* III, question 79, articles 1–2 and 6,
  corpus, and article 6 reply 1, English Dominican/Gutenberg Tertia witness.

The homily uses 13-point Palatino-compatible type on 18-point leading,
ragged-right paragraphs, one-inch side margins, and widow/club protection.
The separate source-and-delivery note and five-entry References occupy the
terminal fourth page, outside the three-page speech. The existing manifest's
homily-only paths already matched the authored include graph; no manifest or
shared-format alteration was needed. The common generation record adds the
actual homily contribution and finalization timestamp
`2026-09-17T21:07:26Z`, preserving the exact packet provenance.

Completed checks: homily content-phase component validation; every homily
content-preflight check, including 24 valid source bindings and five used
reference entries; explicit packet/header provenance comparison; rendered
generation metadata; font embedding; PDF text extraction; and author
inspection of all four page rasters. The used-reference screen initially
required the Missal's formal title outside References; the terminal source
note now names the actual Missal and biblical witnesses without adding
scholarly apparatus to the speech. Two final LaTeX passes produced identical
PDF bytes with no LaTeX/package warnings, undefined references, overfull or
underfull boxes. The proof SHA-256 is
`fbd5b48b76d1b7397b2f3b9ecd9189fec2d5ed0dd8d44904864cdd0961e41c57`.
The final-page rights colophon is legible and creates no spill page.

This is an author proof and author inspection, not independent homily or
visual acceptance. Final artifact production must rebuild all three outputs
with the shared generation timestamp. Shared source inventories and their
global gates remain the coordinating driver's responsibility. No source
library, tooling, inventory, installation, or publication record was changed
by this author stage; no upstream defect was identified for referral.


## Build-artifacts, iteration 0 — 17 September 2026

All three outputs were built with their actual `make doc DOC=<id>
PROVIDER=gpt` targets. The initial canonical build exposed a shared-tooling
coupling to an unfinished, unrelated postconciliar leaf. Production paused
until the coordinator's scoped metadata repair received independent code
review; the final targets retain source and rendered-metadata checks, including
cached outputs. That review is retained under
`workflows/reviews/propers-three-documents-scoped-metadata-2026-09-17/`.
The packet's workflow digest, run identifier and original seed commit remain
unchanged.

The first complete study build had 26 pages. Extraction and contact-sheet
inspection exposed sparse spill pages 6, 11, 15 and 19. Presentation repair
removed only the initial `\clearpage` line from each of
`sections/20-commentary.tex`, `sections/30-healed-charity.tex`,
`sections/40-one-people.tex`, and `sections/50-faithful-offering.tex`.
The study entrypoint `main.tex` also gained `\widowpenalty=10000` and
`\clubpenalty=10000`, matching the companions' protection against lone
paragraph lines. Byte comparison against the stage's pre-edit copies proves
that all other bytes of those five files are unchanged. No prose, quotation,
citation, source role, research evidence, type size or margin changed.
The shared generation record adds this actual layout/build contribution and
sets finalization to `2026-09-17T21:41:11Z`; all three consumers were then
rebuilt. Earlier content review records were not edited or refreshed by this
worker.

Comparison with the retained `study-review-0000.json` confirms that exactly
those five study files now differ from its accepted input hashes. Their
meaning-bearing content is preserved by the byte comparisons above, but the
earlier byte seal is stale. This is disclosed for the fresh reviewer and the
engine's publication-gate enforcement; the builder neither refreshes that
seal nor decides the required review disposition.

The final outputs share the directory
`build/gpt/liturgy/roman-rite/1962/propers/temporal/`:

| PDF filename | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `57-seventeenth-after-pentecost.pdf` | 23 | 192310 | `d4b5a62c07900ca572fffb0636c97904c48e384c455701469c2d55b02331e5c5` |
| `57-seventeenth-after-pentecost-synthesis.pdf` | 5 | 128539 | `65ce2123ca8aa8a3933ede37db2fbc4bcb1186873488f554a3916098980639fe` |
| `57-seventeenth-after-pentecost-homily.pdf` | 4 | 90269 | `e138fbefcb8e80053c8b2c9cbd867fed3540e11d5696ebe4f038486bb620008a` |

Final LaTeX logs contain no fatal errors, undefined references, overfull or
underfull boxes, or LaTeX/package warnings. All three pass rendered generation
metadata validation. `pdfinfo` parses each as an unencrypted Letter-size PDF
1.7 without suspect structure, forms or JavaScript. Ghostscript's null-page
interpreter reads every page with exit status zero and no diagnostic output.
`pdffonts` reports every font embedded, subsetted and equipped with a Unicode
mapping: five fonts in each study, four in the homily. The fonts are URW
Palladio L and Latin Modern. Each PDF remains below 1 MiB and 75 KiB per page.
These are ordinary untagged PDFs; no PDF/UA or tagged-accessibility conformance
is claimed.

The extracted texts were inspected for reading order, intact appointed text,
headings, footnotes, references and terminal matter. All 32 pages extract,
without replacement or null characters, with one final revision display and
one rights colophon per PDF. The homily's three-page speech remains separate
from its fourth-page source note. Its substantive text and word count have
not changed. Final source/PDF identity is recorded mechanically in
[`artifacts.json`](artifacts.json); the artifact-phase consistency check passes.

The bounded `pdf-review` helper prepared 32 full-page rasters, thumbnails and
four contact sheets under
`build/tpt-runs/80a724fb8410dc3d/artifacts/build-artifacts-0000/rasters/`.
Its `review-run.json` records the actual PDF hashes and page counts; the
per-PDF outputs mirror the build paths beneath that raster root. Build logs,
font reports, extracted texts, structure checks, content-preservation checks
and `checks.json` are siblings of `rasters/`. The dedicated raster destination
is intentional: the helper atomically replaces its entire output tree.

### Transient evidence loss during preparation

The first companion-only helper invocation used the packet's broad
`artifacts/` destination. Its replacement of that tree removed the earlier
`derive-homily-0000` author-proof PDF and rasters, as confirmed by the
coordinator, together with this worker's 12 transient reports: three build
logs, the initial rasterization log, and the two sets of PDF information,
font, extraction and structure reports. The earlier author-proof hash remains
a historical record, not a recovered file. The then-current homily mirror was
independently measured as
`fbd5b48b76d1b7397b2f3b9ecd9189fec2d5ed0dd8d44904864cdd0961e41c57`,
matching that recorded hash; subsequent shared timestamp changes produced
the final hash in the table above. No deleted historical proof or log was
fabricated or retrospectively accepted. The global metadata refusal was
captured again from a real repeated command, and final reports describe the
newly executed checks. No earlier full inventory of the replaced directory
was taken, so this is the confirmed loss rather than an exhaustive claim.

Final contact-sheet inspection checked the pagination repair, but this stage
is artifact preparation, not independent all-page visual acceptance. The
fresh visual reviewer must inspect the final 23/5/4-page set. No installation,
web conversion, publication acceptance, or human delivery is claimed here.
No semantic defect was identified for upstream referral during these build
and extraction checks; research limitations remain those already recorded
in `scope.md` and the accepted source audits.

## Generate-web, iteration 0 — 17 September 2026

The canonical study was converted with the exact compiled-packet command:

```sh
tools/tpt web-edition --provider gpt --output build/web/gpt liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost
```

The initial invocation stopped on the four braced `\path` source-record
locators in `sections/90-study-apparatus.tex`. The shared converter owner
added conversion support and payload-preservation checks; the coordinator
cleared the corrected implementation after independent code review. This
worker changed neither accepted TeX nor shared tooling. A fresh invocation
then succeeded with `tools/web-edition` SHA-256
`010e7d412d24fa2497f54a84f4bb21b88afe8f804a0f10f563c573df86ae4de3`
and `scripts/web-shim.tex` SHA-256
`679ff8592e5e8ae1a9755aed9b856710e7fcc49adca32050a54896a723022b22`.

The converter interprets `--output` as the parent of its provider directory,
so the packet's option produced
`build/web/gpt/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.md`.
The generated file was moved without editing to the snapshot's required path,
`build/web/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.md`.
Its SHA-256 before and after relocation was
`340048411a88a76e554eed2becdf2e2a3540dbcc3002cf83a6804ebaeeb82535`;
its size is 70,565 bytes. The frozen workflow command and the converter's
provider-directory semantics were not changed.

The conversion's automatic fidelity checks pass. Inspection and targeted
checks confirm nine section headings, 35 subsection headings, all three
interpretations and their twelve four-sense paragraphs, all fifty source
footnotes, the twelve reference entries, every source hyperlink, all four
source-record locators, one revision display and one rights notice. The
per-leaf web declaration and the existing three-PDF artifact consistency
check also pass. No render-relevant source changed, so the recorded revision
time remains `2026-09-17T21:41:11Z`.

`python3 scripts/_proper_study.py snapshot-web --provider gpt --document
liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost`
recorded the generated bytes in `research/web-artifact.json`; its digest
matches the actual Markdown. This is a generation receipt, not independent
web acceptance. No synthesis or homily web leaf, installed web file, release
record or catalog change was made in this stage.

## Generate-web, iteration 1 — 17 September 2026

The independent iteration-0 web review returned `CHANGES_REQUIRED` for
`WEB-001`: all thirty biblical verse numbers reached the site renderer as
literal caret notation. Its rejected Markdown remains a historical conversion,
SHA-256 `340048411a88a76e554eed2becdf2e2a3540dbcc3002cf83a6804ebaeeb82535`;
the original generated receipt has SHA-256
`5c51204cbd57b94ab17f4fceec9fe39e0474c3ff25a1e2aac5299f459943ae6a`.
The driver preserved those exact files under
`build/tpt-runs/80a724fb8410dc3d/artifacts/web-review-0000/rejected-web/`.
This repair does not alter the earlier review or claim acceptance of its bytes.

After the coordinator cleared the independently reviewed shared converter
repair, the exact compiled-packet conversion command was executed again.
The converter SHA-256 was
`1ee4437ba79468709d75cad1c8f83dadcebfb7ae1ce148645aad20bb1b924fc2`;
the unchanged shim SHA-256 was
`679ff8592e5e8ae1a9755aed9b856710e7fcc49adca32050a54896a723022b22`.
The converter now emits semantic HTML superscript tags for the verse numbers.
This worker changed neither shared tooling nor accepted publication sources.

The packet's `--output build/web/gpt` again produced
`build/web/gpt/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.md`,
because the converter appends its provider directory. The sole generated file
was moved without editing to the required snapshot path,
`build/web/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.md`.
Before and after relocation its SHA-256 was
`6c3fde3e841b05d124938ef842978a4b1e91ac5f8f9dd73020a3d56d02cb648f`;
its size is 70,835 bytes. This records a path correction, not a second
conversion or a hand edit of generated content.

Whole-file comparison proves that the only changed Markdown bytes are the
thirty verse numbers' replacement of caret delimiters by `<sup>` tags. Their
values and order match all thirty `textsuperscript` commands in the appointed
text source. Every other byte remains unchanged, including the argument,
three interpretive boundaries, twelve four-sense paragraphs, fifty footnotes,
nine section and thirty-five subsection headings, source links and locators,
twelve bibliography entries, revision timestamp and rights colophon.

The exact new Markdown was rendered with `tools/public-alpha.render_page`
and the locked Python-Markdown 3.10.3. HTML inspection confirms thirty actual
verse-number superscript elements, no visible caret-delimited numbers, all
101 fragment links resolved and no duplicate identifiers. The rendered proof
and unchanged site stylesheet are under
`build/tpt-runs/80a724fb8410dc3d/artifacts/generate-web-0001/`.
The scoped web-declaration check and existing three-PDF artifact consistency
check pass. All 54 pre-existing leaf files outside this production audit and
the web receipt retain their preparation-time hashes. No render-relevant
TeX changed; the source revision remains `2026-09-17T21:41:11Z`.

The exact packet `snapshot-web` command refreshed `research/web-artifact.json`
with the new generated Markdown hash; independent digest comparison confirms
the receipt matches. This receipt records generation identity only. The new
conversion is submitted for fresh independent web review; installation,
release records and catalog wiring were not performed by this worker.

## Install-publication, iteration 0 — 17 September 2026

The recorded engine results below were read directly during installation.
These are completed historical review events, not a new review by the
installation worker or a claim that every earlier content seal is current.
Their paths are under `build/tpt-runs/80a724fb8410dc3d/results/`, with
`.json` appended to each name.

| Result | Disposition | SHA-256 of engine result |
| --- | --- | --- |
| `research-review-0000` | PASS | `be86aee39a7e5306aebbe18844ec40a379947315a8a9afc27295b14242ed445f` |
| `study-review-0000` | PASS | `2f9104a99c6103242144b144592ba4f6393bca4e9740da39d29c1302306b1021` |
| `synthesis-review-0000` | PASS | `beae308cbd7238c9b5e1c8dee186c846f18e6b7a6b73fda2d5d6f5b4a418efdf` |
| `homily-review-0000` | PASS | `671ffa5a37ecc6d1178a37402b9f1c2a0707899440a6968b61f7c409595624b1` |
| `visual-review-0000` | PASS | `de649c6d323cbb9be50b34080152a6df3194f8cae6d1bc61252cb1a941ae6696` |
| `web-review-0000` | CHANGES_REQUIRED | `6ae8f579cda1617b9213de0f9d08f55f89a2ed5a02f25bb51ea2bf8886d15edb` |
| `web-review-0001` | PASS | `62ec6c404d562c3b4b45158afe6147dd61d733112071a18976768e7259935d6a` |

The accepted visual result identifies the exact 23-page study, five-page
concise study and four-page homily recorded above in the build audit. The
iteration-1 web result accepts the repaired canonical conversion after the
iteration-0 superscript defect. Its Markdown SHA-256 is
`6c3fde3e841b05d124938ef842978a4b1e91ac5f8f9dd73020a3d56d02cb648f`.
This installation records those review facts without claiming a new source
collation, page review, browser review or human rehearsal.

After coordinator clearance, the three exact `make install-doc DOC=<id>
PROVIDER=gpt` targets installed the bare, `-synthesis` and `-homily` outputs
under `pdf/gpt/liturgy/roman-rite/1962/propers/temporal/`. The canonical
Markdown was installed unchanged under the corresponding `web/gpt/` path.
All four destination files were compared byte for byte against their build
sources and against the approved installation proposal's SHA-256 values.
The three PDF hashes remain exactly those in the build audit's table;
the installed Markdown is 70,835 bytes with the hash above. The artifact
snapshot checker passed before and after installation.

The canonical install used the cached PDF. The mandated companion install
targets unexpectedly invoked LaTeX again as a dependency; this was not an
intentional retypesetting step. Both resulting PDFs reproduced the accepted
bytes exactly, as confirmed against the unchanged artifact receipt and
visual-review seal. No accepted TeX, content, metadata, receipt or review
result was edited. Install command logs and the four-output byte comparison
are retained under `.scratch/tlm-production/install-publication-0000/`.

The study's earlier content seal remains stale for the five layout-only
changes described in the build audit. Neither copying accepted artifacts
nor passing byte checks renews it. The terminal engine gate must decide that
review boundary; this installation makes no claim of final publication
acceptance or deployment. Catalog, release, inventory and index mutations
belong to the coordinator and will be verified when its wiring is complete.

The coordinator subsequently created the three per-publication records under
`release/publications/gpt/liturgy/roman-rite/1962/propers/temporal/`, with
filenames `57-seventeenth-after-pentecost.json`,
`57-seventeenth-after-pentecost-synthesis.json`, and
`57-seventeenth-after-pentecost-homily.json`. Independent inspection confirms
schema 1, the exact output IDs, `library/traditional-latin-mass.md`, `alpha`,
and `perpetual-public-repository-2026` in each. The catalog diff adds one
canonical marker and changes only row 57's GPT cell, in Full PDF, Synthesis
PDF, Homily PDF, Read order, preserving Claude's Planned state. The coordinator
staged the exact reviewed canonical Markdown; `git ls-files` confirms its
index presence. The scoped `scripts/_proper_study.py check --phase publication`
command passes, including artifacts, record identities, catalog links, sole
web ownership, tracked Markdown and web declaration. This scoped check does
not replace the engine's accepted-review-seal check or global refresh gates.

The shared refresh subsequently completed. The coordinator's actual logs
record successful `make document-catalogue`, source-inventory refresh,
source-family refresh/check and `make check-sources`. The deterministic
catalog contains 142 works, 194 documents, 218 issues and 6,200 canonical
pages; this worker independently reran `document-library structure --check`
and confirmed it current. Its own TLM entry has the 23-page canonical PDF,
five-page synthesis and four-page homily with their exact paths. Source-family
screening remains explicitly pending for 153 units; the routine source gate
passes without representing that separate screening as complete.

The coordinator used scoped release refresh for the installed TLM web,
1962 catalog and document projection. This worker independently compared
all three actual file hashes to the standing authorization's `site_sources`
and verified its rights-record digest. The scoped publication checker passed
again after these refreshes. Shared command evidence is retained in
`.scratch/integration/tlm-first-shared-refresh.log`,
`.scratch/integration/tlm-first-release-refresh.log`,
`.scratch/integration/tlm-first-family-refresh.log`, and
`.scratch/integration/check-sources-stable-first-install.log`.

The unrelated production's web admission is still outside this completed
installation scope. No global release-gate PASS, final workflow acceptance,
commit, push or deployment is asserted here. The known stale study content
seal remains unchanged for the terminal engine to enforce.

## Author-study, iteration 1 — 17 September 2026

The publication gate forwarded `STALE-STUDY-REVIEW`: the study's current
inputs differ from its iteration-0 review seal. This reentry read the complete
current study, its schema-2 component contract, the interpretation evidence
map, scope, text and English audits, and the preliminary research handoff.
The ten-element treatment, three developed whole-formulary interpretations,
their separate four senses, comparison and terminal apparatus remain complete.
No new research claim or substantive defect was identified in that comparison.

An independent byte check against the historical study-review seal confirms
exactly five changed files. Removing only the two widow/orphan penalties from
the current `main.tex` recovers its accepted SHA-256. Prefixing only the
original `\clearpage` line to each of `sections/20-commentary.tex`,
`sections/30-healed-charity.tex`, `sections/40-one-people.tex`, and
`sections/50-faithful-offering.tex` recovers each accepted SHA-256. The other
nine sealed files already match. This establishes that the differences are
exactly the layout repairs previously recorded, without restoring those
unwanted breaks or editing the historical review.

The study is resubmitted with its current render sources unchanged. A fresh
Pandoc LaTeX AST count reproduces **7,443 substantive words**, with the same
six component counts recorded at iteration 0. The count splits text-node
words on whitespace, excludes headings, notes and raw commands, includes the
opening map, and excludes the appointed texts and terminal apparatus.
The schema-2 study component check, content-phase check, complete
research-edition content preflight, exact packet-provenance comparison and
canonical web-declaration check all pass. The preflight confirms 24 valid
bindings, three whole-formulary lanes and 12 used reference entries.

Source limits remain unchanged: abridged historical translations,
uncollated Jerome and Bellarmine transcriptions, doctrinal illumination
rather than established ancient exposition of the exact orations, and no
specified local-calendar overlay. No fresh facsimile collation, independent
review or rendered-page acceptance is claimed by this author. Because no
render-relevant source changed, the shared revision timestamp remains
`2026-09-17T21:41:11Z`; the exact original workflow provenance and exposed
GPT-6 contribution disclosures remain intact.

The stale-review finding is not yet cleared: obtaining independent acceptance
of these current bytes belongs to the following study-review stage. This
author-stage completion neither manufactures that acceptance nor updates
an old seal. The engine's dependent companion and artifact stages remain
responsible for their subsequent work. Evidence for this reentry is in
`.scratch/tlm-production/author-study-0001/`; it is transient, and the
reproducible findings are recorded here.

## Derive-synthesis, iteration 1 — 17 September 2026

The current expansive study and the complete concise companion were read
together after the renewed study review. The concise study retains the three
controlling questions through five cross-proper movements, with the authors'
answers interleaved at their points of comparison. Its treatment preserves
the questioner's alternative motives, the meanings of one spirit, created
and spiritual heavens, Head-and-members prayer, Daniel's alternative
accounts of confession, common fidelity and particular vows, and the
distinct public and inward emphases of judgment. The sacramental argument
still distinguishes divine help from guaranteed perseverance. Each reading's
four senses remains identifiable, and all ten appointed elements contribute.

The companion's claims and source loci remain supported by the current
study; no new evidence-dependent claim or upstream defect was identified.
Its prose, terminal source note, entrypoint and synthesis-only manifest
membership were retained unchanged. The shared revision timestamp remains
`2026-09-17T21:41:11Z` because no render-relevant source changed. The existing
GPT-6 concise-authoring contribution accurately covers this same author-stage
work, with high effort and the unexposed exact variant explicitly recorded;
no duplicate contribution or invented model qualifier was added. The original
packet provenance remains intact.

A fresh Pandoc LaTeX AST count gives **1,686 substantive words**, or **22.65%**
of the current expansive study's **7,443**. The method counts whitespace-split
text-node words, excluding headings, notes, raw commands and terminal
apparatus; the study count also excludes appointed texts and includes its
opening map. Both ordinary concision bounds are met without an exception.

The synthesis content-phase component check, complete synthesis-edition
content preflight, explicit packet-provenance comparison and source
generation-metadata check all pass. The preflight reports 24 valid bindings,
six used reference entries and three whole-formulary lanes. Count and command
evidence is retained in `.scratch/tlm-production/derive-synthesis-0001/`.
Only this production record changed. No new rendering, page review,
installation, source collation or independent concise acceptance is claimed;
the subsequent workflow stages own those events.

## Derive-homily, iteration 1 — 17 September 2026

Both current reviewed studies and the complete homily were read together.
The homily's governing healed-charity argument remains supported, with
compatible applications of shared baptism and continuing fidelity from the
other readings. It meaningfully joins Matthew's two commands and David's
Son/Lord dialogue, Ephesians' patient charity, and the Introit, Collect,
Secret and Postcommunion. The source attributions and exact loci in the
terminal References remain supported by the studies and their research
evidence map. No new source-dependent claim or upstream defect was identified.

The spoken body, terminal source-and-delivery note, entrypoint and component
membership were retained unchanged. A fresh whitespace-token count of the
prose-only body reproduces **1,283 words**, excluding the title and apparatus:
**10.7–11.7 minutes** at 110–120 words per minute for an adult parish assembly.
A fresh silent editorial reading checked all paragraphs for sense, oral
clarity, transitions, the practical response and the return to the opening
image. This was neither audible rehearsal nor timed human delivery. The
distinction between sacramental help and automatic perseverance remains
explicit, and the conclusion is preaching rather than an invented prayer.

The homily content-phase component check, complete homily-edition content
preflight, exact packet-provenance comparison and source generation-metadata
check all pass. Preflight reports 24 valid bindings, five used reference
entries and three whole-formulary lanes. The source retains 13-point speaking
type on 18-point leading and separate terminal apparatus. No render-relevant
source changed, so the shared revision remains `2026-09-17T21:41:11Z` and the
original packet provenance remains intact. The existing GPT-6 homily
contribution accurately covers the same author-stage work and records high
effort and the unexposed exact model variant; no duplicate declaration was
added.

Count, command and unchanged-source evidence is retained under
`.scratch/tlm-production/derive-homily-0001/`. Only this production record
changed. No fresh source collation, rendering, page review, installation or
independent homily acceptance is claimed; the following workflow stages own
those events.


## Build-artifacts, iteration 1 — 17 September 2026

After the operator released the build hold, the unchanged compiled build
packet was executed on the current inputs. Before this worker's build, the
coordinating operator added exactly ten standard `\label{proper-<element-key>}`
commands immediately after their own appointed headings in
`sections/10-appointed-text.tex`. This worker did not edit that component
or any other accepted prose or evidence. The durable evidence is
[`operator-anchor-proof.json`](../evaluations/proper-study-results/80a724fb8410dc3d/operator-anchor-proof.json),
[`operator-anchor-labels.patch`](../evaluations/proper-study-results/80a724fb8410dc3d/operator-anchor-labels.patch),
and the engine's actual
[`intervention-0000.json`](../evaluations/proper-study-results/80a724fb8410dc3d/intervention-0000.json).
The build worker independently removed exactly those ten commands in memory
and verified that every remaining byte equals the preserved original.

The appointed component changed from SHA-256
`2fb2c9afd135bc6298c1cee602019b71f42610f4218c3f628540e99cf3b786e3`
to `b956cfcc904b09e1cc577030253694825c6a2a04e3819454592ba343acdfdb42`.
Comparison of current engine-derived review inputs with the actual
`study-review-0001.json` shows this is the sole changed file among its fourteen
sealed files; its component contract and generation provenance still match.
The study acceptance is therefore stale by bytes. The synthesis and homily
iteration-1 seals still match their complete current scopes. No review result,
seal, acceptance or engine stage was edited or manufactured. The later
review/publication stages must enforce the stale-study boundary; this build
completion does not renew source acceptance.

The shared finalization timestamp is now `2026-09-17T23:45:46Z`, with an
accurate GPT-6 build contribution at the packet's high effort and the exact
model variant, other qualifiers, client version and server revision explicitly
unexposed. The original workflow id, version, digest, run id and seed commit
remain unchanged. All three outputs were rebuilt through their exact
`make doc DOC=<id> PROVIDER=gpt` targets, which reached fixed points and passed
source and rendered generation-metadata checks.

The final PDFs are under
`build/gpt/liturgy/roman-rite/1962/propers/temporal/`:

| PDF filename | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `57-seventeenth-after-pentecost.pdf` | 23 | 192310 | `111bb840a0cb669f4d058d9467f7e26c09815bb517f1d84a1ced1c3db5654b7f` |
| `57-seventeenth-after-pentecost-synthesis.pdf` | 5 | 128539 | `f9bd82d76591565e3c433fcb53b1974530a74e262765953aa712c73324ca2372` |
| `57-seventeenth-after-pentecost-homily.pdf` | 4 | 90269 | `c8bf81d0525aa180905cc13013f0dccaf6d6bec5a266cb6bfa7574b8c7f55034` |

All three final LaTeX logs are free of fatal errors, undefined references,
overfull or underfull boxes, missing characters and LaTeX/package warnings.
`pdfinfo` parses each as an unencrypted Letter-size PDF 1.7 with no suspect
structure, forms or JavaScript. Ghostscript's null-page interpreter reads all
32 pages successfully without diagnostics. `pdffonts` reports all fonts
embedded, subsetted and supplied with Unicode mappings: five each in the
study and concise study, four in the homily, using URW Palladio L and Latin
Modern. All outputs remain below 1 MiB and 75 KiB per page. These are untagged
PDFs; tagged accessibility or PDF/UA conformance is not claimed.

Text extraction succeeds for all 23/5/4 pages, with no replacement or null
characters, one revision display and one rights colophon per output.
Whole-file comparisons, including every page boundary, prove that all three
extracted texts equal their previously installed versions after replacing
only the revision timestamp. Inspection checked appointed text, headings,
references, source notes and terminal matter; the homily speech remains on
three pages and its separate apparatus on the fourth. This establishes text
and pagination preservation, not a renewed scholarly or all-page visual
acceptance. No semantic defect was identified during the build/extraction
checks; the existing bounded research limitations remain unchanged.

The exact packet `snapshot` command replaced `research/artifacts.json` with
the actual three PDF hashes and current render inputs. The artifact-phase
consistency check passes. The repository `pdf-review` helper generated 32
full-page rasters, 32 thumbnails and four contact sheets under
`build/tpt-runs/80a724fb8410dc3d/artifacts/build-artifacts-0001/rasters/`.
Its `review-run.json` identifies the exact current PDFs. Dedicated sibling
files outside that replaceable raster tree hold all build logs, copied final
LaTeX logs, PDF information, font reports, extracted text, Ghostscript output,
source-seal comparisons and preservation checks.

The fresh visual reviewer must inspect every page of this exact new set.
No PDF was installed, no canonical web conversion was run, and no release,
catalog or shared-source record was changed by this build worker. The
previous installed artifacts are older snapshots. Current web conversion
and independent acceptance remain separate downstream work.

## Install-publication, iteration 1 — 17 September 2026

The actual engine results `visual-review-0001.json` and
`web-review-0002.json` both record PASS. Independent comparison before and
after installation confirms that all 22 PDF/render inputs in the visual
review and the canonical Markdown in the web review still match their sealed
hashes. The artifact-phase consistency check passes.

Each PDF was installed with its exact `make install-doc DOC=<id>
PROVIDER=gpt` target. The canonical target copied the existing build. The
companion targets' broad prerequisites caused them to recompile during the
installation command; pre/post SHA-256 comparisons prove that both rebuilt
PDFs are byte-identical to their accepted artifacts. No dependency checks were
suppressed, accepted source was edited, or review receipt was renewed.
The reviewed canonical Markdown was copied byte for byte to its sole web
destination. All four installed files equal their build counterparts:

| Installed path | SHA-256 |
| --- | --- |
| `pdf/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf` | `111bb840a0cb669f4d058d9467f7e26c09815bb517f1d84a1ced1c3db5654b7f` |
| `pdf/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis.pdf` | `f9bd82d76591565e3c433fcb53b1974530a74e262765953aa712c73324ca2372` |
| `pdf/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily.pdf` | `c8bf81d0525aa180905cc13013f0dccaf6d6bec5a266cb6bfa7574b8c7f55034` |
| `web/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.md` | `a2ab850cd6fc7ea3487e719d54ca6f7b28ab94f9f148ffec8b7bdb0cc65b822f` |

The existing three release records under
`release/publications/gpt/liturgy/roman-rite/1962/propers/temporal/` were
preserved and independently verified: schema 1, the exact bare,
`-synthesis`, and `-homily` IDs, `library/traditional-latin-mass.md`,
`alpha`, and authorization `perpetual-public-repository-2026`. The catalog
retains exactly one canonical marker under the GPT primary-provider rule;
row 57 links Full PDF, Synthesis PDF, Homily PDF and Read in manifest order
and preserves Claude's Planned cell. There are no companion catalog rows or
web authorities.

The coordinator staged the exact canonical Markdown; an independent read of
the Git index proves its bytes equal the accepted web artifact. The initial
document-catalog check reported drift before the coordinator's refresh.
After `make document-catalogue`, the independent check passes with 142 works,
194 documents, 218 issues and 6,200 pages. The coordinator's actual scoped
web and document-projection binding refreshes are recorded in
`.scratch/integration/tlm-web2-binding-refresh.log`,
`.scratch/integration/document-catalogue-tlm-install1.log`, and
`.scratch/integration/tlm-install1-corpus-binding-refresh.log`.
Independent SHA-256 comparison confirms the current canonical web, 1962
catalog and document projection against their authorization bindings, and
confirms the rights-record digest. The scoped publication checker passes
after those completed writes.

Command logs, installed-byte comparisons, accepted-review input checks and
shared-record verification are retained under
`.scratch/tlm-production/install-publication-0001/`. This append records
installation facts only. The global source-inventory refresh awaits the
coordinator's shared archive freeze; no new global-source or global-release
PASS is asserted. The iteration-1 study review still differs solely in
`sections/10-appointed-text.tex`, as the build audit explains. Installation
does not renew that acceptance. The actual terminal engine gate owns the
stale-study boundary and final acceptance; no terminal acceptance, commit,
push or deployment is claimed here.


## Author-study, iteration 2 — 17 September 2026

The publication gate forwarded `STALE-STUDY-REVIEW` after the ten appointed-text
navigation labels were added. This author reentry read the complete current
study, its schema-2 manifest and interpretation evidence map. The substantive
opening, all ten appointed texts and detailed treatments, three sustained
whole-formulary readings with separate four senses, comparison and terminal
apparatus remain complete. No new claim or prose repair was needed.

A fresh byte comparison against the iteration-1 study-review seal found
exactly one changed file among its 14 sealed files:
`sections/10-appointed-text.tex`. Removing only its ten unique
`\label{proper-...}` commands in memory reproduces the reviewed SHA-256
`2fb2c9afd135bc6298c1cee602019b71f42610f4218c3f628540e99cf3b786e3`.
The current file's SHA-256 is
`b956cfcc904b09e1cc577030253694825c6a2a04e3819454592ba343acdfdb42`.
The other 13 files match the seal. The labels follow the ten element keys in
liturgical order. They remain in place; all render sources remain unchanged.

A fresh Pandoc LaTeX AST count reproduces **7,443 substantive words**:
opening and map 522; commentary 1,900; healed charity 1,464; gathered people
1,523; faithful offering 1,672; comparison 362. As in the original count,
headings, footnotes, raw commands, appointed texts and terminal apparatus are
excluded, while the opening map is included. The research-edition content
preflight, content-phase component check, exact original packet-provenance
comparison, source and rendered generation-metadata checks, and canonical
web-eligibility check pass. The preflight confirms 24 valid bindings, three
whole-formulary lanes and 12 used references.

All 19 render-input hashes and all three PDF hashes in the existing artifact
record match their current bytes. The canonical PDF remains
`111bb840a0cb669f4d058d9467f7e26c09815bb517f1d84a1ced1c3db5654b7f`.
This comparison is not a new build or rendered-page review. With no change to
render-relevant sources, the shared finalization timestamp remains
`2026-09-17T23:45:46Z`; original run provenance and actual GPT-6 contribution
disclosures remain unchanged. No companion, research-evidence, shared-tool,
publication, historical review-result or review-seal file was edited.

Source limits remain those of the reviewed research and terminal appendix:
abridged historical English, uncollated Jerome and Bellarmine transcriptions,
no established direct ancient commentary on the exact orations, and no
specified local-calendar overlay. This reentry performs no new facsimile
collation or reception sweep. The complete study is ready for renewed cold
review, but the forwarded stale-review finding is **not yet repaired**:
independent acceptance of current bytes belongs to the following study-review
stage. No independent acceptance or terminal workflow success is claimed.
Task-local comparison and check evidence is held in
`.scratch/tlm-production/author-study-0002/`; the reproducible findings above
are the durable record.

## Installation recipe clarification history

During installation iteration 1, the worker observed that the declared companion Make targets would recompile because of their existing dependencies. It proposed `-o` and performed only a dry run, which failed its own no-retypesetting assertion; no dependency-suppressed installation was executed. The driver paused that proposed deviation, and the coordinator directed the exact declared Make commands with pre/post accepted-hash checks. Those actual commands reproduced both accepted companion PDFs byte for byte. The original dry-run and command evidence remains in `.scratch/tlm-production/install-publication-0001/`. A future workflow recipe clarification is separate; active v1 and these actual results were not rewritten.

## Derive-synthesis, iteration 2 — 17 September 2026

The complete current expansive study, interpretation evidence map, concise
study and terminal apparatus were read against the three-document contract.
An independent SHA-256 comparison confirms that all 14 files sealed by
`study-review-0002.json` still match. The concise argument continues to
interleave healed charity, the gathered people and faithful offering through
five common questions. All ten appointed elements contribute, and each
interpretation's literal, allegorical, moral and anagogical senses remain
identifiable. The questioner's motives, meanings of one spirit, created and
spiritual heavens, Head-and-members prayer, Daniel's confession, common and
particular vows, and public and inward judgment retain their distinctions.
Sacramental help remains distinct from advance absolution or guaranteed
perseverance. Its exact attributions and source qualifications remain
supported by the renewed study; no new claim or upstream defect was found.

A fresh Pandoc LaTeX AST count gives **1,686 substantive words**, **22.65%**
of the expansive study's independently recounted **7,443**. The method counts
whitespace-separated text-node words, excludes headings, footnotes and raw
commands, and excludes terminal apparatus and appointed texts; the study's
opening map is included. Both ordinary concision bounds are met without an
exception. The synthesis content-phase component check, full synthesis
content preflight, exact packet-provenance check and source generation-metadata
check pass. Preflight confirms 24 valid source bindings, six used reference
entries and three whole-formulary interpretations.

No render-relevant source changed. The prose, entrypoint, synthesis-only
component membership, original provenance and shared finalization timestamp
`2026-09-17T23:45:46Z` remain unchanged. The existing GPT-6 concise-authoring
contribution records this same high-effort work with its exact variant and
other unavailable qualifiers explicitly unexposed; no duplicate declaration
was added. Only this production audit changed. Count, seal-comparison and
command evidence is retained in
`.scratch/tlm-production/derive-synthesis-0002/`. This author reentry claims
no new source collation, build, page review, installation or independent
concise acceptance; those remain distinct workflow events.

## Derive-homily, iteration 2 — 17 September 2026

The complete current expansive and concise studies, their terminal apparatus,
the interpretation evidence map, and the existing homily were read against
the exact three-document and homily-authoring contract. Independent SHA-256
comparison confirms that the 14 files sealed by `study-review-0002.json` and
the eight files sealed by `synthesis-review-0002.json` still match. The homily
continues to develop healed charity, with compatible applications of shared
baptism and continuing fidelity. Its argument joins both halves of Matthew
22:34–46, the patient charity of Ephesians 4:1–6, and the Introit, Collect,
Secret and Postcommunion. The five terminal reference entries and attributed
paraphrases remain supported by the renewed studies; no new source-dependent
claim or upstream defect was found.

A fresh silent editorial reading checked every paragraph for sense, oral
clarity, transitions, the practical response and the return to the opening
image. The prose-only body has **1,283 whitespace-separated words**, excluding
title and apparatus: **10.7–11.7 minutes** at 110–120 words per minute for an
adult parish assembly. This remains an estimate, not audible rehearsal or
timed human delivery. The speech distinguishes sacramental nourishment and
preservation from automatic perseverance, and concludes as preaching rather
than as an invented prayer. The exact loci and delivery information remain
outside the spoken body.

The full homily content preflight, content-phase component check, exact
packet-provenance comparison and source generation-metadata check pass.
Preflight confirms 24 valid bindings, five used reference entries and three
whole-formulary interpretations. All 19 render-input hashes and three PDF
hashes in the existing artifact record match current bytes. The homily PDF
remains `c8bf81d0525aa180905cc13013f0dccaf6d6bec5a266cb6bfa7574b8c7f55034`.
These comparisons are not a fresh build or rendered-page review.

No render-relevant source changed. The homily prose, terminal note,
entrypoint, 13-point type on 18-point leading and component membership remain
unchanged, as do the shared timestamp `2026-09-17T23:45:46Z` and original
packet provenance. The existing GPT-6 homily contribution describes this
same high-effort author-stage work and explicitly records the unexposed
exact model variant; no duplicate declaration was added. Only this factual
production audit changed. Task-local check logs and byte/count evidence are
under `.scratch/tlm-production/derive-homily-0002/`. No new source collation,
reception research, rendering, installation or independent homily acceptance
is claimed; renewed cold homily review belongs to the following stage.

## Build-artifacts, iteration 2 — 17 September 2026

All three exact `make doc DOC=<id> PROVIDER=gpt` commands completed
successfully. Make found the canonical study current and recompiled the
concise study and homily through its declared fixed-point recipes. The final
PDFs are byte-identical to the preceding artifact snapshot:

| PDF under `build/gpt/liturgy/roman-rite/1962/propers/temporal/` | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `57-seventeenth-after-pentecost.pdf` | 23 | 192310 | `111bb840a0cb669f4d058d9467f7e26c09815bb517f1d84a1ced1c3db5654b7f` |
| `57-seventeenth-after-pentecost-synthesis.pdf` | 5 | 128539 | `f9bd82d76591565e3c433fcb53b1974530a74e262765953aa712c73324ca2372` |
| `57-seventeenth-after-pentecost-homily.pdf` | 4 | 90269 | `c8bf81d0525aa180905cc13013f0dccaf6d6bec5a266cb6bfa7574b8c7f55034` |

Inspection of all three final LaTeX logs found no fatal errors, undefined
references, missing characters, overfull or underfull boxes, or warnings.
Fresh `pdfinfo` and Ghostscript null-page checks succeeded for every PDF;
Ghostscript produced no diagnostics. The files are unencrypted Letter-size
PDF 1.7 documents, without suspect structure, forms or JavaScript. `pdffonts`
confirms five embedded, subsetted fonts with Unicode mappings in each study
and four in the homily. All files remain below the publication-size review
thresholds. These are untagged PDFs; PDF/UA conformance is not asserted.

Fresh layout-preserving text extraction succeeded for all 32 pages. The
complete extracted texts were read, including appointed texts, headings,
footnotes, reference lists and terminal notes. No extraction defect or new
upstream semantic defect was identified in that inspection. There are no
replacement or null characters, and each output has one visible revision
stamp and a terminal rights colophon. The homily speech occupies three pages
with its source-and-delivery note on the fourth. This build inspection does
not renew scholarly acceptance or constitute all-page visual review.

The exact packet `snapshot` command regenerated `research/artifacts.json`.
It is byte-identical to its prior version and records the same three PDF
hashes and 19 render inputs, each independently checked against current bytes.
The artifact-phase consistency and rendered metadata checks pass. Independent
comparison also confirms all files in the iteration-2 study, synthesis and
homily review seals: respectively 14, eight and eight files, with no mismatch.
No presentation repair was required, so the accepted prose, navigation labels,
layout, original run provenance and `2026-09-17T23:45:46Z` finalization timestamp
remain unchanged. No historical review seal was edited.

The repository `pdf-review` helper prepared 32 full-page rasters, 32 thumbnails
and four bounded contact sheets under
`build/tpt-runs/80a724fb8410dc3d/artifacts/build-artifacts-0002/rasters/`.
Its `review-run.json` was checked against the actual current PDF hashes and
page counts. The sibling `checks/` directory holds Make logs, copied final
LaTeX logs, PDF information and font reports, extracted texts, Ghostscript
results, snapshot comparisons and review-input checks. The helper's existing
content-addressed raster cache was used; cache identity is preparation
information, not visual acceptance. A fresh worker must inspect all pages of
this exact set before the workflow advances through visual review.

Only this factual audit append changes tracked content in this stage. The
snapshot was rewritten with identical bytes. No PDF was installed and no web,
release, catalog, source-library or shared-tool record was changed. The
previous research limitations remain; no new source verification, audible
rehearsal, human delivery or external approval is claimed.

## Generate-web, iteration 3 — 17 September 2026

The frozen packet's exact conversion command completed successfully:

```text
tools/tpt web-edition --provider gpt --output build/web/gpt liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost
```

The converter appends its provider beneath the supplied output root, so the
actual output was
`build/web/gpt/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.md`.
The driver authorized byte-preserving relocation to the required review path,
`build/web/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.md`.
The original and destination were compared before removing the extra-path
copy: both contained 71,024 bytes and SHA-256
`a2ab850cd6fc7ea3487e719d54ca6f7b28ab94f9f148ffec8b7bdb0cc65b822f`.
No generated prose was edited. The exact command, paths, both hashes and
reason were recorded before snapshot in
`.scratch/tlm-production/generate-web-0003/relocation.json`.

The converter's built-in fidelity audits and the leaf's web-declaration check
passed. The complete generated Markdown was read. Additional source/output
comparison confirmed all 44 source section and subsection headings (allowing
ordinary typographic apostrophe conversion), all 18 explicit source links,
and all 50 source footnotes. The three interpretations remain distinct, each
with its literal, allegorical, moral and anagogical distillation. A fresh
invocation of the converter's site-rendered schema-2 target audit confirmed
all ten unique appointed-text anchors. The appointed texts, element commentary,
comparison, scope appendix, 12 reference entries, revision timestamp and
rights notice remain present. No conversion or declaration repair was needed.

Independent hashes also confirmed all 19 render inputs and all three PDFs
against `research/artifacts.json`. No reviewed study or companion source,
label, declaration or generation metadata changed; the existing revision
stamp remains `2026-09-17T23:45:46Z`. No separate synthesis or homily web
edition was generated. These generation checks do not constitute independent
web acceptance, renewed source research or publication approval. The following
worker reviews the snapshotted bytes. Task-local conversion, declaration and
comparison evidence is under `.scratch/tlm-production/generate-web-0003/`.

The exact packet `snapshot-web` command regenerated `research/web-artifact.json`;
its path and digest were checked against the current relocated bytes and the
original-output hash. The receipt records conversion identity only. No web
installation, release, catalog or shared-tool mutation was performed here.

## Install-publication, iteration 2 — 17 September 2026

The actual engine results `visual-review-0002.json` and
`web-review-0003.json` both record PASS. Before and after installation,
independent SHA-256 comparisons confirmed all 53 sealed input entries across
study review 2, synthesis review 2, homily review 2, visual review 2 and web
review 3. The artifact receipt remains current; no accepted source, review
seal or receipt was changed during installation.

All three exact `make install-doc DOC=<id> PROVIDER=gpt` commands completed
successfully. The canonical study was current. The declared companion
prerequisites caused synthesis and homily to recompile; both reproduced the
accepted PDFs byte for byte. No dependency was suppressed. The canonical
Markdown was copied byte for byte to its sole installed web destination.
All four installed paths and SHA-256 values remain those listed in the
iteration-1 installation table above: study `111bb840a0cb669f4d058d9467f7e26c09815bb517f1d84a1ced1c3db5654b7f`,
synthesis `f9bd82d76591565e3c433fcb53b1974530a74e262765953aa712c73324ca2372`,
homily `c8bf81d0525aa180905cc13013f0dccaf6d6bec5a266cb6bfa7574b8c7f55034`,
and canonical web `a2ab850cd6fc7ea3487e719d54ca6f7b28ab94f9f148ffec8b7bdb0cc65b822f`.
An independent Git-index read confirms that the coordinator-staged canonical
Markdown equals the accepted bytes.

The existing three publication records were read and preserved. Each has
schema version 1, its exact bare, `-synthesis` or `-homily` ID, catalog
`library/traditional-latin-mass.md`, status `alpha`, and authorization
`perpetual-public-repository-2026`. The catalog has exactly one canonical
marker under its GPT primary-provider rule, and row 57 links Full PDF,
Synthesis PDF, Homily PDF and Read in manifest order while retaining Claude's
Planned cell. No companion row or web authority was added. The independent
artifact-phase check, scoped publication-phase check and scoped document
catalog check pass.

The coordinator retains shared catalog, source-inventory and authorization
refreshes and the final global barrier; these checks do not claim their
completion. This append records installation facts only, not terminal workflow
acceptance, commit, push, deployment, new source verification or human delivery.
Command logs, accepted-input comparisons, installed-byte checks and exact
shared-record verification remain under
`.scratch/tlm-production/install-publication-0002/`.

Before this worker returned, the coordinator completed the actual
`make document-catalogue` refresh and scoped release-binding refresh. Their
logs are `.scratch/integration/document-catalogue-final-install.log` and
`.scratch/integration/final-install-release-binding-refresh.log`. An independent
`document-library structure --check` now passes: 142 works, 194 documents,
218 issues and 6,220 pages. Independent digest comparison confirms the
current 1962 catalog, canonical web edition and document projection against
their authorization bindings. All 53 accepted input entries, four installed
files and staged web bytes still match. The source and family inventories
remain the coordinator's next shared step after the final installation
archives; no completed global source check or terminal gate is asserted.

## Terminal completion

The actual program gate `publication-gates`, iteration 2, returned PASS with no findings and the engine reached **ACCEPTED** for run `80a724fb8410dc3d`. The terminal status records 57 packets and 57 results, no standing findings and no escalations. The original version-1 workflow digest and seed commit stated above remain unchanged. No run state, earlier result, seal or workflow definition was rewritten to obtain acceptance.

The current three PDFs are 23, 5 and 4 pages and match the exact hashes in `research/artifacts.json`; all 32 pages received fresh independent full-page visual review. The canonical web matches `research/web-artifact.json` and received fresh complete source/PDF comparison and desktop/mobile browser review after the shared breadcrumb correction. Its exact HTML, stylesheet/icon, fourteen inspected PNGs and hashed evidence manifest remain at `build/tpt-runs/80a724fb8410dc3d/artifacts/web-review-0003/`. This is article-conversion acceptance, not a new full-site visual review or deployment claim.

The source review counts remain 7,443 substantive study words, 1,686 concise words and 1,283 spoken homily words. Homily delivery is estimated at 10.7–11.7 minutes at 110–120 words per minute; no timed human performance is claimed. Historical translation/collation limits and the universal-calendar/local-observance distinction remain as recorded in the research and prose.

Exact engine-retained stage results, original manifest/bootstrap, actual terminal response/status and actual terminal replay are archived under `evaluations/proper-study-results/80a724fb8410dc3d/`; `record.md` binds their hashes. Terminal replay reports retained packet integrity with `deterministic: null`; it does not re-perform any editorial review or reconstruct all prior decisions. The prior real nonterminal deterministic replay is separately retained. The operator label intervention and the historical transient proof loss remain honestly recorded; terminal acceptance does not erase either event.

## Proper-study v6 author-study, iteration 0 — 21 September 2026

The expansive study was freshly read against the independently reviewed
research for `proper-study` version 6, run `090e496c9d6d4104`, workflow digest
`a965af881c1e4110b6e4698001b4f06b9a688a93a1f1652c292d15002afe1768`,
seeded at commit `30c7baebd99056e4faac09a0f13cb085f9de1ea7`. It remains a
complete 1962 Seventeenth Sunday after Pentecost study: the opening maps all
ten appointed elements; the lawful Latin and historical English witnesses are
identified; each element receives substantive commentary; three distinct
whole-formulary readings develop multiple checked Fathers or saints and their
own literal, allegorical, moral and anagogical senses; and a short comparison
and the reviewed scriptural chronology precede the terminal apparatus. No
postconciliar appointment or interpretation supplies this leaf.

The interpretive exposition remains **7,443 substantive words**: opening and
map 522; element commentary 1,900; healed charity 1,464; gathered people
1,523; faithful offering 1,672; comparison 362. This reproduces the established
Pandoc LaTeX-AST count of prose text nodes, excluding headings, notes, raw
commands, the appointed-text reproduction, the separately generated historical
chronology appendix and terminal apparatus. The source limits remain those in
`scope.md`: the retained historical English witnesses are not new critical
collations; Jerome and Bellarmine are used through disclosed retained
transcriptions; no direct ancient commentary on the exact three orations was
established; the whole-Mass readings are editorial syntheses rather than
attributions to a Father; and no local-calendar overlay was specified.

The exact packet build command completed twice and settled a **22-page**
author proof with no fatal error, undefined reference, overfull or underfull
box, or LaTeX/package warning. The required research-edition artifact-phase
component check passed. `pdfinfo` reports an unencrypted Letter-size PDF 1.7,
471,419 bytes. All 22 full-page rasters were inspected: the appointed-text
continuations, interpretive lane transitions, four-senses blocks, chronology
tables, footnotes, references, revision display and final rights colophon are
legible and unclipped, with no sparse spill page or damaged running matter.

The exact proof submitted for cold review is
`build/tpt-runs/090e496c9d6d4104/artifacts/author-study-0000/proof/57-seventeenth-after-pentecost-author-proof.pdf`,
SHA-256
`0ecd7d768fb793e92cc2e2b06f0d9cd3ec504874bc692eed7a7aae9d1bb2b305`.
Its copied LaTeX log is beside the proof under the same stage artifact root,
and its dedicated replaceable raster tree is
`build/tpt-runs/090e496c9d6d4104/artifacts/author-study-0000/rasters/`.
This is author verification, not independent study acceptance or final
three-document visual review. No research evidence, study prose, shared
formatting source, companion, installed publication, prior review result or
historical run record was changed in this stage.

## Proper-study v6 derive-synthesis, iteration 0 — 21 September 2026

The existing concise study was freshly compared with the accepted expansive
study and its three reviewed interpretations for `proper-study` version 6,
run `090e496c9d6d4104`. Its fixed opening maps all ten appointed elements,
prints exactly four overview senses, carries the generated chronology on page
2, and develops the formulary's movement on pages 3--4. The integrated
commentary begins on page 5 and interleaves healed charity, the gathered
people and faithful offering through five cross-proper questions. It preserves
the important differences concerning the Gospel questioner's motive, the
meanings of one spirit, created and spiritual heavens, Head-and-members
prayer, Daniel's confession, common and particular vows, and public and inward
judgment. All ten appointed elements contribute, and the three readings'
literal, allegorical, moral and anagogical conclusions remain distinguishable.
No new evidence-dependent claim or upstream defect was found, so the accepted
prose, component membership and shared generation record were retained.

The current concise argument contains **3,975 substantive words**: 249 in the
appointed-elements map, 99 in the four-senses overview, 1,094 in the thematic
movement and 2,533 in the integrated commentary. The count uses Pandoc's
LaTeX abstract syntax tree and counts prose text nodes while excluding
headings, footnotes and raw commands. The generated chronology dossier and
terminal apparatus are excluded, consistently with the study count's
exclusion of its generated chronology appendix. The earlier 1,686-word audit
entries describe the pre-pagination-recovery commentary and do not describe
this settled ten-page source.

The packet's exact build command completed through its fixed-point passes and
produced a settled **10-page** author proof. The required synthesis artifact
component check passed. The auxiliary evidence places inventory and overview
on physical page 1, chronology on page 2, themes on pages 3--4 and integrated
commentary on page 5. The final log contains no fatal error, undefined
reference, overfull or underfull box, or LaTeX/package warning. `pdfinfo`
reports an unencrypted Letter-size PDF 1.7, 462,521 bytes. All ten full-page
rasters were inspected; the dense chronology sheet, opening argument,
commentary, footnotes, scope appendix, references, revision display and rights
colophon are legible and unclipped, with no damaged running matter or spill
page.

The exact proof submitted for cold review is
`build/tpt-runs/090e496c9d6d4104/artifacts/derive-synthesis-0000/proof/57-seventeenth-after-pentecost-synthesis-author-proof.pdf`,
SHA-256
`ba14d046656b05e0af8094895f149c88fa27054b68e939dd4d4fef6d8446261c`.
Its settled auxiliary file has SHA-256
`5b66a7d44b75f8372c1289acff6651da0b33a1d85b1b855d4f3659e1e1cef055`,
and the copied final log has SHA-256
`14797ec0a6d485afe1c2e3e7c56b329dd1070218e1b50f4b6551e778a6a252dc`.
Both are beside the proof. The dedicated replaceable raster tree is
`build/tpt-runs/090e496c9d6d4104/artifacts/derive-synthesis-0000/rasters/`.
This is author verification, not independent synthesis acceptance or the
workflow's final three-document visual review.

## Proper-study v6 derive-homily, iteration 0 — 21 September 2026

Both reviewed studies, their terminal apparatus and the interpretation record
were freshly read with the standalone homily for `proper-study` version 6,
run `090e496c9d6d4104`. The homily's governing healed-charity argument remains
coherent and source-bounded. It joins both movements of Matthew 22:34--46---the
twofold command of love and David's Son confessed as Lord---with the patient
charity and received unity of Ephesians 4:1--6, then places that demand within
the Introit's appeal to mercy, the Collect's request for purified allegiance,
the Secret's plea for cleansing and preservation, and the Postcommunion's
eternal remedy. Its practical treatment of correction preserves the reviewed
distinction between charitable truth and humiliation, and its account of the
Eucharist preserves continuing freedom rather than implying automatic
perseverance. No new source-dependent claim or upstream defect was found, so
the accepted speech, terminal apparatus, component membership and shared
generation record were retained.

A fresh silent editorial reading checked sentence sense, transitions, oral
clarity, the concrete opening question, the practicable response and the final
return to the next sentence. The prose-only body contains **1,283 words** by a
fresh Pandoc plain-text count, excluding title and apparatus. At 110--120 words
per minute this supports the stated **10.7--11.7 minute** estimate for an adult
parish assembly. This was neither an audible rehearsal nor a timed human
delivery. The exact loci, interpretation relation, audience and delivery
estimate remain outside the spoken body under `Source and delivery note` and
`References`.

The homily-edition component check and complete content preflight pass. The
preflight confirms 32 valid bindings, five used reference entries, three
whole-formulary interpretation lanes and exact version-6 packet provenance.
The document build completed its two settling passes and produced an
unencrypted, three-page Letter-size PDF 1.7 of 242,757 bytes. Its log contains
no fatal error, undefined reference, overfull or underfull box, or
LaTeX/package warning. All three full-page rasters were inspected: the
two-column speech is legible and continuous across its two pages, and the
source-and-delivery note, five references, revision display and rights
colophon are legible and unclipped on page 3.

The exact author proof submitted for cold review is
`build/tpt-runs/090e496c9d6d4104/artifacts/derive-homily-0000/proof/57-seventeenth-after-pentecost-homily-author-proof.pdf`,
SHA-256
`63eb6b1126af403fadc67c08b4eca0d8f718f2247692a6d6c759a30ef8dc348d`.
Its settled auxiliary file has SHA-256
`96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486`,
and its copied final log has SHA-256
`77c7fc454b6534a9513d0d578028f60e3123294fb48549971bd19a596a63f3b5`.
Both are beside the proof; the dedicated raster tree is under the same stage
artifact root. This is author verification, not independent homily acceptance
or the workflow's final three-document visual review.

## Proper-study v6 build-artifacts, iteration 0 — 21 September 2026

All three packet-prescribed `make doc` builds completed successfully for
`proper-study` version 6, run `090e496c9d6d4104`. No layout or other source
edits were made in this stage. The final build artifacts are:

| Output | Pages | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| `build/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.pdf` | 22 | 471,419 | `0ecd7d768fb793e92cc2e2b06f0d9cd3ec504874bc692eed7a7aae9d1bb2b305` |
| `build/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-synthesis.pdf` | 10 | 462,521 | `ba14d046656b05e0af8094895f149c88fa27054b68e939dd4d4fef6d8446261c` |
| `build/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost-homily.pdf` | 3 | 242,757 | `63eb6b1126af403fadc67c08b4eca0d8f718f2247692a6d6c759a30ef8dc348d` |

The expansive and concise works satisfy their required 20--50-page and
10--12-page ranges. Settled absolute-page labels in the concise auxiliary put
the complete inventory and all four overview senses on physical page 1,
chronology alone on page 2, themes from page 3 through page 4, and developed
commentary beginning on page 5. The auxiliary hashes are
`5cebdacde2e5647ca86cae0a9fb9765ade3088094caca2d3dc1fb57e77e92e6e`
for the expansive study and
`5b66a7d44b75f8372c1289acff6651da0b33a1d85b1b855d4f3659e1e1cef055`
for the concise study.

The three final logs contain no fatal error, undefined reference, overfull or
underfull box, rerun request, or LaTeX/package warning. Ghostscript parsed all
three PDFs with the null-page device without an error. `pdfinfo` reports three
unencrypted Letter-size PDF 1.7 files, and `pdffonts` reports every font
embedded, subsetted and Unicode-mapped. Layout-preserving extraction succeeded
for every page: the expansive extraction is 12,494 words and 85,780 bytes, the
concise extraction 6,066 words and 43,696 bytes, and the homily extraction
1,780 words and 13,592 bytes. Page-by-page extraction inspection found the
expected running matter and section sequence, complete terminal references and
rights matter, and no replacement or NUL characters.

The PDFs, settled auxiliaries, final logs, table of contents and extracted
texts are retained under
`build/tpt-runs/090e496c9d6d4104/artifacts/build-artifacts-0000/proof/`.
`research/artifacts.json` records the exact three PDF hashes, the expansive and
concise pagination evidence, and all render-input hashes after the final build.
The bounded review helper produced 35 page rasters under
`build/tpt-runs/090e496c9d6d4104/artifacts/build-artifacts-0000/rasters/`.
Those rasters are prepared for the following fresh visual reviewer; this build
stage does not claim that independent visual acceptance. No remaining build,
pagination, extraction, font-embedding or PDF-structure limitation was found,
and no PDF was installed.

## Proper-study v6 visual review, web review and installation, iteration 0 — 21 September 2026

The workflow's independent visual-review result passed after inspection of all
35 rendered pages. The accepted PDF receipts are
`0ecd7d768fb793e92cc2e2b06f0d9cd3ec504874bc692eed7a7aae9d1bb2b305`
for the 22-page expansive study,
`ba14d046656b05e0af8094895f149c88fa27054b68e939dd4d4fef6d8446261c`
for the 10-page concise study, and
`63eb6b1126af403fadc67c08b4eca0d8f718f2247692a6d6c759a30ef8dc348d`
for the three-page homily. The independent web-review result also passed for
the canonical Markdown with SHA-256
`a90987a6a5e6bfcb0e7cc98c9802ae1812f057e21c5811abaa7b5217659ea9bf`.

The three normal `make install-doc` recipes completed for the bare,
`-synthesis`, and `-homily` IDs. Each installed PDF is byte-identical to both
its reviewed build artifact and the accepted receipt above. The reviewed
canonical Markdown was installed byte-for-byte at
`web/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost.md`
and staged for the publication gate; its installed SHA-256 remains the accepted
web receipt above. The three existing per-publication records were checked and
preserved: each names its exact output ID, `library/traditional-latin-mass.md`,
`alpha`, and `perpetual-public-repository-2026`. The calendar row already links
the Full PDF, Synthesis PDF, Homily PDF and canonical web edition in schema-2
order, and the canonical primary-provider publication marker remains unique.

## Proper-study v6 installation repair, iteration 1 — 21 September 2026

The publication gate returned one blocking finding,
`GATE-WEB-EDITIONS-CURRENT`: fifteen tracked web editions were stale after the
reviewed converter changed hard line breaks from trailing spaces to semantic
`<br>` elements. The fifteen editions were regenerated from their canonical
sources with `tools/tpt web-edition`. A byte-level comparison proved that every
change was limited to that semantic hard-break substitution and removal of
trailing horizontal whitespace; no source prose was changed. The generated
bytes were installed at their existing tracked `web/` paths, and the release
binding refresh was restricted to those fifteen paths. It updated those
fifteen bindings and the two deterministic release authorization records.

Before that repair, the artifact snapshot check passed and the three normal
`make install-doc` recipes were rerun for the bare, `-synthesis`, and `-homily`
IDs. Build and installed bytes remain equal to the accepted review seals:
`0ecd7d768fb793e92cc2e2b06f0d9cd3ec504874bc692eed7a7aae9d1bb2b305`,
`ba14d046656b05e0af8094895f149c88fa27054b68e939dd4d4fef6d8446261c`,
and
`63eb6b1126af403fadc67c08b4eca0d8f718f2247692a6d6c759a30ef8dc348d`,
respectively. The reviewed canonical Markdown for this owner remains
byte-identical to its accepted receipt,
`a90987a6a5e6bfcb0e7cc98c9802ae1812f057e21c5811abaa7b5217659ea9bf`.

The document catalog, source-reader projection, publication-source inventory,
and source-family ledger were refreshed with their owning tools. The scoped
publication check, release-binding check, scoped public-alpha check, document
catalog check, global web-current check, and `make check-sources` all pass.
The web-current sweep subsequently exposed one presentation defect in a
different 1962 reference work: print-only checkbox geometry had disappeared
from its generated web checklist. The shared web shim now gives that existing
macro a semantic empty-box rendering, with focused regression coverage. The
reference edition was regenerated and independently rechecked; no proper-study
PDF, source paragraph, appointment or reviewed Sunday web byte changed.

## Proper-study v6 terminal disposition and archive — 22 September 2026

Publication-gates iteration 0 returned one corpus-wide web-current failure and
routed it to installation. After the generated-edition repair above,
install-publication iteration 1 passed and publication-gates iteration 1
returned `PASS` with no findings or escalations. The engine reached
`ACCEPTED`.

The owning leaf preserves the exact v6 history under
`evaluations/proper-study-results/090e496c9d6d4104/`: 23 accepted result
submissions, their 23 packet texts, the immutable seed manifest and bootstrap,
the terminal engine state, and exact terminal status and replay outputs. Fresh
status and replay commands reproduce those terminal records; replay reports
`recorded_file_intact: true`. This archive records the failed global gate and
its real repair rather than presenting a synthetic straight-line success.
