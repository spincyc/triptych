# Production review

## Author study — iteration 0

Run `b686b7a44f0e35e7`, workflow `proper-study` version 7. The expansive
study was authored on 28 September 2026 from the reviewed research for the
1962 Nineteenth Sunday after Pentecost, general-calendar occurrence
4 October 2026. This record covers author verification only. Independent
study review, companion derivation, the final shared-timestamp build, and
publication review remain subsequent workflow work.

### Completed scope

The study contains the complete ten-element inventory and historical study
texts, detailed commentary on every element, and two whole-formulary readings:
“The Invited People Clothed in Charity” and “The Renewal of Hands, Words, and
Desires.” Each has its own literal, allegorical, moral, and anagogical
conclusion. Augustine and Gregory carry the first reading; Chrysostom and
Bellarmine carry the second. Aquinas and Schuster contribute the bounded
arguments identified in the notes. Whole-Mass connections are editorial
syntheses except where Schuster directly treats this Sunday.

The canonical chronology is rendered in a terminal historical appendix,
followed by scope and qualifications, used references, the revision timestamp,
and rights colophon. Schema 2 declares all three intended entrypoints and
future concise and homily components; only the research components are
implemented at this stage. Canonical web eligibility is declared, without
claiming a generated web edition has been reviewed.

### Substantive length

The substantive opening, element commentary, two developed readings, their
sense distillations, and concluding comparison contain approximately **6,930
words**. This conservative source count excludes the inventory map, appointed
texts, all footnotes, heading and sense labels, TeX command names, chronology,
terminal scope, bibliography, provenance, and rights colophon. Alphabetic
words with internal apostrophes or hyphens count as one token. Breakdown:
opening 257; element commentary 2,447; charity reading 1,891; renewal reading
2,059; comparison 276. The settled PDF has **20 physical pages**, including
all terminal apparatus.

### Source limits preserved

The appointed Latin follows the reviewed 1962 witness and its public-domain
1862 antecedent. Cummiskey 1861 supplies the Introit antiphon and three
orations in historical English; Douay–Rheims–Challoner supplies biblical
English without reconstructing the Latin's liturgical additions or adapted
verb forms. The target 1962 edition is not declared public domain. Ordinary
texts are not reproduced; the Creed and Trinity Preface are appointments.

The reception sweep is bounded by the reviewed works, not exhaustive. The
study preserves Gregory's imperfect-charity distinction and his alternative
relations between Matthew's and Luke's feasts; it does not invent a universal
wedding-garment custom or a numerical salvation rate. Gregory's weaving image
uses upper and lower supports. Aquinas's inspected OCR supports paraphrase,
not a newly established critical text. Schuster's theological interpretation
does not establish ancient compilation history. The historical chronology
keeps competing composition proposals distinct, records the Gospel event date
as unresolved, and does not convert a broad Psalter boundary into a date for
each psalm's occasion. Reviewed research records were not revised by this
authoring stage.

### Author proof verification

The required `make doc` build and the research-edition component artifact
check passed. Research-edition content preflight also passed: 27 source
bindings resolve; the seven scriptural elements preserve the current
chronology projection; both lanes declare complete element and sense coverage;
and no bound restricted source is reproduced. The references are a manually
checked description list; the automatic references-used check recognizes zero
formal bibliography entries and therefore supplies no positive citation-use
audit for that list.

All 20 pages were inspected at page-raster scale with a contact-sheet overview;
changed pages were reinspected after pagination repairs. The opening map is
complete on page 1, the chronology dossier is together on page 18, and the
final references, timestamp, and rights colophon share page 20. Sparse
text-only spill pages were removed. No clipping, overlap, missing glyph,
or stranded heading was found in the settled proof. The final LaTeX log has
no warnings, undefined references, overfull boxes, or underfull boxes.
`pdfinfo` reports US Letter pages; `pdffonts` reports all 15 fonts embedded,
all from Latin Modern. The shared format supplies 11-point text, 0.75-inch
margins, and monochrome output.

The proof displays revision timestamp **2026-09-28T15:13:28Z**. The exact
cold-review copy is `study-author-proof.pdf` in run `b686b7a44f0e35e7`'s
`author-study-0000` artifact directory; its SHA-256 is
`f628a1b3635f1ef63ad1998de786d76dcddf0073bffce0afffacd81613674aad`.
The run directory also retains build and check logs, PDF information,
font evidence, and the dedicated replaceable raster child. This author
inspection does not replace the later independent visual evaluation.

## Author study — iteration 1

The study was revised on 28 September 2026 after research iteration 2.
The complete research scope, interpretation map and existing study components
were read. The acquired USCCB Ephesians introduction was independently read,
including its destination discussion and complete authorship paragraph;
the generated chronology comparison was checked against that evidence.

The historical appendix now explains the grounds for questioning direct
Pauline authorship and distinguishes the secretary under Paul's direction
from the later-disciple hypothesis. Only the latter receives the separately
displayed approximate interval. The traditional captivity alternatives,
uncertain composition location, destination proposals, and distinction between
writer and recipients remain visible. This incorporates the study-owner
follow-through identified as STU-CHR-001 in the reviewed research. The
references now cite the USCCB introduction's paragraphs 3–4 and correct
Gregory's Wikisource index URL, addressing STU-CIT-001. No reviewed research,
chronology projection, source binding, appointed text, or interpretive lane
was changed by this author stage.

The complete two-reading study remains **6,930 substantive words**, independently
recounted using the exclusions and token rule above. Its five counted components
retain the same breakdown. The historical appendix's redundant concluding
recap was shortened so its dossier and conclusion remain together on page 18;
the qualifications remain in the dossier and scope appendix. The final
proof remains **20 physical pages**. All pages were inspected as page rasters,
with the three changed terminal pages reinspected after that pagination
adjustment. Raster hashes establish that pages 1–17 were unchanged between
the two proofs inspected during this stage. No clipping, overlapping text,
missing glyph, or isolated heading was found. The final page contains the
references, one visible timestamp and the compact rights colophon.

The required author build and research component artifact check passed.
Research content preflight passed with 28 valid bindings, both whole-formulary
lanes, and the complete generated chronology for seven scriptural elements.
The manual bibliography retains the earlier automatic-check limitation:
the references-used check recognizes no formal bibliography entries. The
final LaTeX log has no warnings, undefined references, overfull boxes or
underfull boxes. PDF inspection confirms US Letter and 15 embedded Latin
Modern fonts. The current Ephesians evidence is paraphrased; no protected
liturgical English or newly composed prayer was added. Earlier source limits
remain as recorded above and in the reviewed research.

The exact run-provenance check passed. The broader `make check-sources`
command reached successful source-library validation but stopped in its
document-catalogue prerequisite because the manifest's future `homily.tex`
does not yet exist. This is the current author-study stage boundary, not a
completed global gate; the companion and later publication stages must
complete that check after their entrypoints exist. Shared inventory refresh
and integration remain with the workflow coordinator.

Finalized render timestamp: **2026-09-28T15:59:54Z**. The exact cold-review
copy is `study-author-proof.pdf` in this run's `author-study-0001` artifact
directory, SHA-256
`8d8e64a2ae4348ec9fb31e6e1cef189f80914c32f613c3ad451133fa2728f68c`.
Build diagnostics, component/content checks, word-count evidence, extracted
text, PDF/font information and a dedicated raster child accompany that copy.
This is author verification; the independent study verdict, companion
derivations, final shared-timestamp build and independent visual review are
separate subsequent events.

## Derive synthesis — iteration 0

The concise study, **Charity and the Renewed Life**, was derived on
28 September 2026 from the accepted expansive study and its reviewed
research. It implements the six already-declared synthesis components and
the literal imports in `synthesis.tex`. The common manifest already named
the correct synthesis-only membership, presentation roles, element coverage
and generated-chronology reference; no manifest repair was necessary.
The accepted study, chronology, evidence bindings and interpretation records
were not revised. The shared generation record now identifies this
contribution and the render-source finalization time **2026-09-28T16:26:54Z**.

The complete ten-element map and exactly four overview sense rows occupy
physical page 1. The canonical chronology, including all traditional
alternatives, both critical comparisons and the unresolved Gospel event
date, occupies page 2 alone. Its concise explanations retain the distinct
Aramaic/Greek Matthew objects and the conditional later-disciple Ephesians
interval. The source-grounded thematic movement occupies pages 3–4;
developed interleaved commentary begins on page 5. Six cross-proper
questions compare fruitful belonging with renewed action, preserving
Augustine's and Gregory's different arguments for charity, Chrysostom's
particular social commands, Bellarmine's grace/obedience distinction,
Gregory's imperfect-charity consolation and the actual reception differences.
No new evidence-dependent claim or additional research source was introduced.

The substantive themes and commentary contain **3,719 words**: 1,081 in
the thematic movement and 2,638 in the developed commentary. This source
count excludes footnotes, headings, zref labels, TeX commands, the inventory,
overview, chronology and terminal apparatus. Alphabetic words with internal
apostrophes or hyphens count as one. The settled author proof has **10
physical pages**, including all terminal content.

The required `make doc` author build and synthesis-edition component
artifact check passed. The settled auxiliary record proves inventory and
overview on page 1, chronology on page 2, themes on pages 3–4 and commentary
starting on page 5. Synthesis content preflight passed: 28 bindings resolve,
all seven chronology cells retain generated annotations, and the
house-voice, structural, rights and declared-coverage checks pass. The
manual description-list bibliography was compared with its uses; the
automatic references-used check recognizes no formal entries and does not
supply a positive audit of that list.

All ten page rasters were inspected; changed pages were reinspected after
strengthening the thematic exposition and attaching two footnote markers
to their preceding sentences. No clipping, overlap, missing glyph,
stranded heading or detached marker remains. The shared title, map,
overview and dossier forms retain house typography. Both thematic pages
are substantively filled, the chronology remains legible, and the final
references, single timestamp and compact rights colophon share page 10.
The final LaTeX log contains no warnings, undefined references, overfull
or underfull boxes. PDF inspection confirms US Letter, 17 embedded Latin
Modern font entries and 462,675 bytes, below the size-review thresholds.

The exact reviewer proof is retained in run `b686b7a44f0e35e7` under
`artifacts/derive-synthesis-0000/`, outside its dedicated replaceable
`rasters/` child:

| Artifact | SHA-256 |
| --- | --- |
| `synthesis-author-proof.pdf` | `a440660d94998ea71c70791b3d67eb2c16ab89d7000a46f3312091499553fac2` |
| `synthesis-author-proof.aux` | `5fa40538283f0773f66967f7302f515865ba94edee61c1d71b60e74cdf1873bd` |
| `synthesis-author-proof.log` | `4b2193be3777edf4b50940fd5a3b1d0c79b5cc8e8b22b32f27cf25c1afd1d518` |

The artifact directory also holds the recorder file, extracted text,
word-count method and totals, build and component/content check logs,
font/PDF information and `proof-manifest.json` with exact repository-relative
paths and hashes. This is author verification only; independent concise
review, homily derivation, the final three-document shared-timestamp build
and cold visual evaluation remain separate workflow events. No PDF was
installed at this stage.

The broader `make check-sources` reached successful source-library
validation, then stopped at the document-catalogue prerequisite because the
declared future `homily.tex` is not yet implemented. That global gate must
be completed after the homily stage. Shared source inventories, catalog
integration, commits and workflow advancement remain with the coordinator.

## Derive homily — iteration 0

The standalone homily, **The Garment of Charity**, was derived on
28 September 2026 after reading both reviewed studies in full and the
canonical research scope and interpretation records. It addresses the
packet's adult parish assembly for the 1962 Nineteenth Sunday after
Pentecost, 4 October 2026. It implements the already-declared `homily.tex`,
`homily-body` and `homily-apparatus` without changing the manifest, research
evidence or either study. The shared generation record identifies the
contribution and finalization timestamp **2026-09-28T16:45:22Z**.

The controlling argument is the charity interpretation: the prepared feast
calls its guests into the Bridegroom's love. The compatible renewed-action
reading supplies the Epistle's truthful speech, restrained anger and work
ordered to sharing. The Collect, Secret, Communion and Postcommunion place
those responses within divine help, fruitful reception and continuing
healing. The speech preserves the seriousness of judgment, the distinction
between culpable withholding and inability, and Gregory's consolation for
imperfect charity. Its practical examples are exhortations, not invented
events; it ends as preaching and includes no newly composed recited prayer.
No new source-dependent claim or upstream repair was introduced.

The supporting primary passages were independently reread in the retained
witnesses: Augustine, Sermon 90.4–6 and 9–10 (NPNF I.6, English Sermon XL),
and *Enarrationes* 118, opening Aleph exposition 4–5 (NPNF I.8, English
Psalm 119); Gregory, *Gospel Homilies* II.38.9–12; Chrysostom, *Ephesians*
XIV on 4:25–28; and Schuster, *Sacramentary* III, the Collect and concluding
Secret, Communion and Postcommunion exposition on pp. 171–174. The exact
loci and the connection to the reviewed interpretations appear outside the
speech under the source note and `References`. Historical transcriptions
and Schuster's OCR retain their recorded evidence limits; this was no fresh
facsimile collation of those editions.

The body contains **1,301 spoken words**, counting alphabetic words with
internal apostrophes or hyphens as one and excluding all title and terminal
matter. At 115–125 words per minute the estimate is **10.4–11.3 minutes**
before additional pauses, suitable for the requested approximate 10–12
minutes. A silent editorial read-through checked the narrative sequence,
sentence length, natural attribution, transitions, practical response and
return to the opening feast image. No audible rehearsal, human performance
or measured delivery time is claimed.

The author proof is **3 physical pages**. The literal shared imports occur
in the prescribed order; the full-width title precedes the shared
two-column `properhomily` environment. Only the spoken component occurs
inside that environment, on pages 1–2. Its closing page break places the
single-column source/delivery note, references, one visible timestamp and
rights colophon together on page 3. All three page rasters were inspected;
the extracted text was read. No clipping, overlap, missing glyph or stranded
heading was found. The final LaTeX log has no warnings, undefined references,
overfull boxes or underfull boxes. `pdfinfo` confirms US Letter and the
declared metadata; `pdffonts` confirms 11 embedded Latin Modern font entries.

The PDF is 275,105 bytes, approximately 89.6 KiB per page. The size threshold
was investigated: ten compressed embedded font streams account for 244,939
bytes (about 89 percent); `pdfimages -list` reports no raster images. This
short text-only PDF's font overhead explains the per-page ratio; no
independent PDF optimization or source-image alteration was performed.

The required `make doc` build, homily component artifact gate, complete
homily content preflight and exact run-provenance check passed. All 28 source
bindings resolve. The manual reference list was compared with actual uses;
the automated references-used check recognizes zero formal bibliography
entries and supplies no positive audit of this description list.
`git diff --check` passed. The broader `make check-sources` passed source
library validation but stopped at the shared catalogue and inventory checks:
the catalogue has drifted, and the source inventory lacks the new homily
files and has a stale evaluation-record hash. Those coordinator-owned
refreshes remain required before integration; no shared record was changed
in this dispatch.

The exact proof is `homily-author-proof.pdf` in run
`b686b7a44f0e35e7`'s `artifacts/derive-homily-0000/` directory, SHA-256
`75f155ca5c86429a1f487e6d076bffe3faf3026a4a6dbb9274be822344da963c`.
The proof's auxiliary, log and recorder files, extracted text, count/size
evidence, check logs and hash manifest accompany it outside the dedicated
replaceable raster child. This is author verification only. Independent
homily review, the final shared-timestamp three-document build, cold visual
review and installation remain subsequent workflow events. No PDF was
installed, and no commit or workflow transition was performed here.

## Coordinator provenance audit before final artifact production

The structured generation declarations now also account for context and
research work, workflow integration, and the independent source/content
review configuration already used in this run. The exposed worker efforts
are retained as `high` and `xhigh`; the coordinator's unexposed reasoning
effort and all unavailable model/runtime details remain explicitly named
as unexposed. No exact model variant or runtime version was inferred.
These audit-only additions do not alter the rendered timestamp, production
identity, prose, or inherited-source declarations. Content-review seals
exclude pure contribution declarations by their owning contract; the final
artifact snapshot and visual review will bind the complete metadata bytes.

## Build artifacts — iteration 0

All three final `make doc` builds completed on 28 September 2026 with the
shared render timestamp **2026-09-28T16:45:22Z**. No content, layout,
generation declaration or review seal was changed in this stage. The final
LaTeX logs contain no warnings, undefined references, missing characters,
overfull boxes or underfull boxes. The complete extracted texts were read;
all physical pages contain text and no replacement character was found.
`pdfinfo`, `pdffonts` and Ghostscript's null-page interpreter completed
successfully. All font entries are embedded Latin Modern; all pages are
US Letter. The component artifact check passed for the complete family.

| Output | Physical pages | Bytes | Embedded font entries | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| Study | 20 | 480574 | 15 | `52b155c7e4366f0ef8304871ac1dabbbc56733aaaaa589f12085b396d7f18d43` |
| Concise study | 10 | 462674 | 17 | `7681fbd92d4301f3138f5512d97f6273119a7364f2e02bbff2edb2ea115c1848` |
| Homily | 3 | 275105 | 11 | `75f155ca5c86429a1f487e6d076bffe3faf3026a4a6dbb9274be822344da963c` |

The concise auxiliary evidence and page-by-page extraction agree: the
complete inventory and four sense rows occupy physical page 1, chronology
alone page 2, themes pages 3–4, and developed commentary begins on page 5.
The study and concise totals include their terminal apparatus and meet
their respective 20–50 and 10–12 page bounds. Every final extraction contains
one revision timestamp and the rights colophon on its last physical page.

The homily's 89.6 KiB per-page ratio exceeds the size-investigation trigger.
Its bytes reproduce the previously investigated author proof exactly;
the retained measurement identifies 244,939 compressed font-stream bytes,
and a fresh `pdfimages -list` again finds no raster images. Font overhead
accounts for the ratio; no PDF-only optimization was performed.

`research/artifacts.json` records the exact final PDF hashes, render inputs
and pagination evidence. The concrete PDFs remain under
`build/gpt/liturgy/roman-rite/1962/propers/temporal/` with the bare identity,
`-synthesis` and `-homily` suffixes. This run's
`artifacts/build-artifacts-0000/` directory retains exact proof copies,
all three auxiliary, log and recorder files, build output, PDF/font/structure
checks, complete and per-page extractions, and `verification.json`.
The repository `pdf-review` helper generated every page raster and contact
sheet in that directory's dedicated replaceable `rasters/` child.

This stage records mechanical artifact preparation, not a visual acceptance.
The fresh visual reviewer must inspect all 33 pages after the upstream
seal and artifact gates pass. No PDF was installed. The earlier limits on
source evidence, bibliography automation and estimated delivery remain;
shared inventory/catalog integration belongs to the coordinator.

The stage's `make check-sources` passed source-library validation and found
the document catalogue current. It stopped on stale shared publication-
inventory hashes for this leaf's `evaluations/blocking-findings-v1.toml`
and `research/production-review.md`; the coordinator must refresh those
records before integration. `git diff --check` passed.

## Accepted visual review and canonical web generation

The actual `visual-review` iteration 0 result is PASS with no findings.
Its fresh reviewer inspected all 33 pages individually at full raster size,
checked the contact sheets and PDF diagnostics, and verified all 30 sealed
inputs. The exact PDFs remain those recorded in `research/artifacts.json`.

The first canonical web conversion exposed a converter defect: generated
chronology definitions imported through `sections/70-date-location.tex`
were not collected because the converter looked only in the preamble.
The generation worker repaired body-definition collection and removal,
with an exact generated-dispatcher exception in the unknown-command scan.
The publication's accepted sources, metadata and PDFs were unchanged.
The regression suite passed 131 tests, with the subsequently added strict
unknown-helper rejection assertion also passing in its focused test.
Existing installed web editions remain byte-current under the repaired
converter; the new edition's installation is still pending. The coordinator
reviewed the complete code and fidelity-contract diff, and `tmt check` passed.

The generated canonical Markdown has SHA-256
`dc4948bdc26ab27a24d562018196b556298903d256b7364bf918997b38c25eb5`.
Its conversion receipt is `research/web-artifact.json`. This is generation
evidence only; independent web review and installation are separate events.
The web checks use the repository-pinned Markdown 3.10.3 dependency in a
task-local environment, with no global dependency change.

## Accepted reviews and installation — iteration 0

The engine results for run `b686b7a44f0e35e7` record PASS with no findings
for research review iteration 2, study review iteration 1, synthesis review
iteration 0, homily review iteration 0, visual review iteration 0 and web
review iteration 0. These are the actual accepted results following the
earlier research and study repairs, not a new editorial or ecclesiastical
approval. The web reviewer compared the complete conversion with the sealed
study and checked representative desktop/mobile presentation, all fragment
targets and footnote navigation using the locked Markdown 3.10.3 renderer.
Remote URL availability and the deployed site were outside that review.

Before installation on 28 September 2026, the artifact checker confirmed
that `research/artifacts.json` still matched the three PDFs, render inputs
and pagination evidence. All three normal `make install-doc` recipes then
completed with their dependencies and metadata checks intact. Every build
and installed PDF retained its accepted hash:

| Installed PDF, below `pdf/gpt/liturgy/roman-rite/1962/propers/temporal/` | SHA-256 |
| --- | --- |
| `59-nineteenth-after-pentecost.pdf` | `52b155c7e4366f0ef8304871ac1dabbbc56733aaaaa589f12085b396d7f18d43` |
| `59-nineteenth-after-pentecost-synthesis.pdf` | `7681fbd92d4301f3138f5512d97f6273119a7364f2e02bbff2edb2ea115c1848` |
| `59-nineteenth-after-pentecost-homily.pdf` | `75f155ca5c86429a1f487e6d076bffe3faf3026a4a6dbb9274be822344da963c` |

The reviewed canonical Markdown was installed byte for byte at
`web/gpt/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost.md`
with SHA-256 `dc4948bdc26ab27a24d562018196b556298903d256b7364bf918997b38c25eb5`.
Neither companion has a separate web authority. The three independently
generated release records below
`release/publications/gpt/liturgy/roman-rite/1962/propers/temporal/`
name the exact output identities, `library/traditional-latin-mass.md`,
status `alpha` and the standing authorization
`perpetual-public-repository-2026`. The existing Nineteenth Sunday row
links Full PDF, Synthesis PDF, Homily PDF and Read in that order, with one
canonical primary-provider marker. Its Claude cell remains Planned.

The deterministic document catalogue and source projection were regenerated
with their owning tools. The publication-source inventory and family ledger
were refreshed; their only changed publication surface is this canonical
leaf's completed review and installation audit. The 16 task-owned site
inputs were rebound with exact path scoping, including scoped adoption of
the ten newly recognized inputs. Every other site-source binding was
preserved. The publication checker, scoped public-alpha policy check,
`make check-sources` and the full `make check-web-editions-current` recipe
passed. The scoped public-alpha check validates global source, release and
authorization records while requiring installed PDFs only for this family;
it does not verify unrelated PDFs or authorize a deployment.

Installation does not claim deployment or terminal workflow acceptance.
The publication gate remains the engine's subsequent decision. Earlier
source-evidence, bibliography-automation and estimated-delivery limits remain.

## Terminal workflow acceptance

The actual engine returned **ACCEPTED** for run `b686b7a44f0e35e7` on
28 September 2026, after publication-gates iteration 0 passed with no findings
or escalations. All installed artifacts retain the hashes recorded above.
The leaf's `evaluations/proper-study-results/b686b7a44f0e35e7/` preserves
the exact 30 packets and 30 accepted submissions, including failed review
dispositions, original seed manifest and bootstrap, terminal state, status
and replay output. Every copied packet and result matches its engine-recorded
hash. The replay reports the last packet intact and `deterministic: null`;
no fresh deterministic replay is claimed.

This terminal decision supersedes the pending-stage statements in the
historical entries above. It accepts the workflow's publication family; it
does not broaden the stated source-review, citation-automation, delivery-
timing or remote-site verification claims. Sources, release records, artifact
receipts and run evidence are committed on the workspace branch. Installed
PDFs remain intentionally untracked under repository policy. Final validation
and the concrete branch checkpoint are recorded in
`workflows/reviews/gpt-1962-59-production-2026-09-28/CYCLES.md` and the work
register; no main merge or live deployment is claimed.

## Contents links and bookmarks rebuild, 2026-10-01

On 1 October 2026 the maintainer reported that the PDFs' hyperlinks did not
jump to their claimed locations, and authorized regenerating every leaf built
with `src/common/propers-format.tex`, both providers. The cause was shared:
`common/preamble` loads hyperref before the format loads titlesec, so hyperref
never defined titlesec's anchor hooks and titlesec replaced them with
`\@gobble`. With `secnumdepth` 0 every section went without an anchor, and
each contents line, PDF bookmark and following `\label` pointed at the last
anchor before it, usually `table.1`. The shared format now defines hyperref's
own hooks after loading titlesec. No word, layout or page
changed: every page is pixel-identical to the previous installation, and only
link destinations and bookmarks differ. The three PDFs were rebuilt with the
normal recipes and installed byte-identical:

| PDF | Pages | SHA-256 |
| --- | ---: | --- |
| Study | 20 | `ca1dd6edd726240acaacb9800f321bfec1e1a2dbea914b70b88c526f418018a1` |
| Concise study | 10 | `ba7dfa7c14b95310ee677a33875476dbc8ab0b759925fe5c72160743987836db` |
| Homily | 3 | `0832932d754a44308aeac2435ee92df7184afafb8a7ca18be93932738e89213f` |

Verified on the installed PDFs, which print no contents
links: their 15 bookmarks each land on the page of their heading with the anchor at or above it, and
65 footnote links resolve. The artifacts-phase gate under this leaf's
declared contracts and `check-generation-metadata` pass, and
`research/artifacts.json` is re-recorded. An independent review
confirmed the cause, the definitions' identity with hyperref's, and the links,
bookmarks and pixels of all 27 rebuilt PDFs; its advisory that the References
anchor sat below its heading was answered by moving the anchor before it.
