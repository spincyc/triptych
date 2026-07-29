# Final exact-snapshot review — 2026-07-27

## Scope and exact snapshot

This internal AI-agent review covers publication-local source bindings and claims,
historical and patristic limits, theological and canonical currentness,
clinical and safeguarding boundaries, rights, PDF and web production, and
exact-snapshot distribution state. It is not ecclesiastical approval.

- publication-source aggregate:
  `sha256:0afc61fcda20c472428d25b16fd142311698b242aa186f3ce6316d5f91dc653b`
- research-control aggregate, excluding filenames containing `review`:
  `sha256:c52f8cede81fb3d829eba29db836597c1f64e40e7ef2bbd755a65ef1292950bd`
- source bindings:
  `sha256:0625cc997d08a48a9ff3b99a0f2f94085fe27ea0ebd8214edefda631ae6139ba`
- built PDF:
  `sha256:8d1e47c299f84151334df3b93f1bcf423ead9d1c961c5f07d5bae6d55c4db47c`
- tracked web edition:
  `sha256:d129315ea6077d91605f93edacd3e99b946120cfd85b1644dfca6b3a6faca76f`

The source aggregate is the hash of a bytewise-path-ordered `sha256sum`
manifest covering `main.tex`, `generation-metadata.tex`,
`web-edition.toml`, and every direct `sections/*.tex` file. The research
aggregate uses the same method over every direct regular file in `research/`
whose filename does not contain `review`. This record is excluded from both
aggregates.

## Findings

The built PDF is 20 pages, 361,881 bytes, and has the expected title, subject,
revision-derived modification date, embedded subset fonts, extractable text,
and no encryption, forms, JavaScript, or automatic creation date. The build
log has no fatal error, undefined reference, overflow, or layout warning. All
20 review rasters were inspected. No clipping, overlap, broken table, isolated
heading, unreadable colophon, or unintended blank page was found. The final
page is intentionally light because generation metadata and the compact rights
colophon conclude the work.

The tracked web edition exactly matches a fresh conversion of the reviewed
source. Gene Wolfe's quotation, attribution, rights note, and generation
contribution are absent from the current source, PDF text, and web edition.
The web edition retains the generation disclosure and rights colophon.

The publication remains non-operational. It supplies no ritual formulas,
alleged signs, self-test, commands, names, interview script, or sequence.
Consent, withdrawal, continuing treatment, emergency and protective action,
privacy, territorial law, clinical competence, and accountable ecclesial
authority remain explicit. WHO material is confined to clinical
classification and differential assessment and is not used to adjudicate a
preternatural cause.

The medieval negatives are appropriately bounded. The PRG is only a
bibliographic coordinate; no content, circulation, local-use, office-duty,
frequency, named-case, or cross-genre medieval synthesis is inferred from the
unacquired critical loci. Named cases remain excluded without asserting that
no adequate archive exists.

The canonical and theological claims remain bounded to the Latin Church,
identified U.S. implementation, exact Catechism and canon-law controls, and
the stated currentness date. Latin canon 1172 is not projected onto an Eastern
Church, the current ritual is not reproduced, and historical existence is not
treated as present authorization.

## Blocking inconsistencies

The exact-snapshot publication gate does **not** pass:

1. Restored exact Tertullian, Origen, Jerusalem, and Eusebius passage bindings
   and reader claims contradict `ancient-biblical-patristic-audit.md`,
   `source-audit.md`, and the resolution appended to
   `patristic-ancient-context-review-2026-07-27.md`, which still say those
   exact reusable artifacts or passages are outstanding or unavailable.
   `sections/30-apostolic-patristic-initiation.tex` also calls these passages
   exact and checked while its concluding table still labels the relevant
   broader patristic leads “uncontrolled.” The exact restored passages may
   stand, but the audit and review-state descriptions must be reconciled
   without implying control of the unbound *Apostolic Tradition* or Laodicea
   loci.

2. `scope.md`, `sections/130-scope-method-coordinates.tex`, and
   `theology-law-reception-audit.md` still describe historical, patristic,
   liturgical, clinical, safeguarding, pastoral, rights, or production lanes
   as outstanding although dated review records now pass several of those
   lanes. The current source must state one coherent review state.

3. Every prior exact-snapshot review that includes
   `research/source-bindings.toml`, the full publication-source aggregate, or
   the research-control aggregate is stale. The present binding hash is
   `0625cc997d08a48a9ff3b99a0f2f94085fe27ea0ebd8214edefda631ae6139ba`;
   the historical-liturgical resolution records different source and research
   aggregates, and the theological and safeguarding reviews pin earlier
   binding hashes. Their substantive conclusions may inform review, but they
   do not authorize this exact restored snapshot.

4. `make check-sources` does not pass for the working tree. The canonical
   source library itself validates, but the exhaustive inventory is stale
   because of concurrent changes in another publication. The required
   repository-wide final source gate therefore remains open.

5. No installed PDF exists at
   `doc/gpt/history/catholic-exorcism/01-history-and-current-practice.pdf`.
   There is consequently no installed byte-identity check and no installed
   snapshot to authorize.

6. `release/public-alpha.json` retains this publication at `hold` with
   `complete-reusable-source-registration` and
   `independent-multidisciplinary-review` open, and `approval` is `null`.
   Its authorization inventory also pins an older web-edition hash. No current
   PDF hash or exact-snapshot distribution approval exists.

## Verdict

**Fail for installation and distribution authorization.** The reviewed
20-page build is production-clean and the current non-operational,
safeguarding, historical-ceiling, web-fidelity, and Wolfe-removal checks pass.
Publication remains blocked until the contradictory audit and review-state
records are reconciled, the affected independent lanes reattach to the current
hashes, the repository source gate passes, the reviewed PDF is separately
authorized and installed, installed/build identity is proved, and the release
manifest receives a fresh exact-snapshot approval. No imprimatur, nihil obstat,
canonical permission, installation authority, or distribution authority is
created by this review.

## Superseding exact-snapshot re-review

The following determination supersedes the fail verdict above for content and
production only. The source and audit contradictions identified in items 1–3
were reconciled and reviewed. The current exact snapshot is:

- publication-source aggregate:
  `sha256:55198dd1e35e27529a2df45ad8a09e4bc02b63100d7c416a7218a89cf432712f`
- research-control aggregate, excluding filenames containing `review`:
  `sha256:deedee4a9dbcca8cff62d07661508621393c04186c84a902cedfed778783ec52`
- source bindings:
  `sha256:2a8f292eaf4e0115eb595de30ac99a20048f0955fd6bf58a0762170e01b59db5`
- source audit:
  `sha256:9dd56e6e35ad3632880f727aef54ab498ad5823aa4d40b65c2ff5a8071a937cf`
- evidence map:
  `sha256:559296dc5565b7569b12c37f0481d29d7ab94d196da4bbe77a93270ca8191381`
- scope record:
  `sha256:cd30aa825f4f6b0109100af1bab8a7a04e1b0823731142b82536e51784e0f3c0`
- built PDF:
  `sha256:1840f2c3a3d559d186dbf688e67c6a63b23ecd5870062918034a86c90f088124`
- tracked web edition:
  `sha256:6010565a060ac96650aa4b0ab3c70121fd6aceeaae352a8536fa063330c3a77d`

The restored Tertullian, Origen, Jerusalem, and Eusebius claims now agree
across reader prose, bindings, source audit, evidence map, ancient-patristic
audit, and the superseding resolution in the patristic review. They remain
translation-bounded literary claims. The uncontrolled *Apostolic Tradition*
and Laodicea leads do not support reader claims. PRG, medieval practice,
cross-genre synthesis, frequency, outcomes, and named-case limits remain
explicit and proportionate.

The theological, canonical, clinical, safeguarding, pastoral, rights, and
review-state records are mutually consistent for their bounded lanes. The
work remains non-operational and preserves consent, treatment, emergency,
privacy, jurisdiction, and authorization limits. The current ritual is not
reproduced. No Wolfe wording, attribution, rights note, or generation
contribution remains.

The rebuilt PDF remains 20 pages. A fresh raster run and inspection of all
pages found no clipping, overlap, broken table, isolated heading, unintended
blank page, or illegible colophon. The log contains no fatal error, undefined
reference, overflow, or layout warning. PDF metadata, extracted text, and
embedded subset fonts pass. A fresh web conversion is byte-identical to the
tracked web edition and retains the generation and rights disclosures.

The exorcism source graph validated at the reconciled checkpoint within a
canonical library reporting 527 artifacts, 4 corpora, 449 editions, 930
passages, 56 segments, 326 works, and 1,473 bindings. A later repository-wide
run encountered concurrently added malformed source records owned by other
publications, and the repository-wide web-current check found two unrelated
stale web leaves. Those global working-tree defects do not change this
publication's exact source, PDF, or web verdict and must not be represented as
exorcism validation failures.

**Content verdict: pass. Production verdict: pass for the exact built PDF and
tracked web edition above.**

The only remaining gates for this publication are root-owned lifecycle and
release actions: authorize and install the reviewed PDF; prove installed/build
byte identity; add or confirm the catalog link only after installation; and
replace the release manifest's `hold`, open gate list, `approval: null`, stale
web authorization hash, and absent PDF hash with a separately authorized exact
snapshot disposition. Until those actions occur, this review grants no
installation or distribution authority and no ecclesiastical approval.

## Current 32-page public-alpha checkpoint

This checkpoint supersedes the operational-state and current-byte statements
above while preserving their historical findings about the snapshots they
identify. It records an internal source and production audit, not independent
human, clinical, canonical, priestly, or ecclesiastical review.

The current exact controls are:

- `main.tex`:
  `sha256:139a2f4372502ced03abbbfe3213474e004e07ebfce4ff643b0cede4f58d8a2d`
- patristic chapter:
  `sha256:830538882b98a56811616961e69f58c2fb8cdd53684d995febd667d6abe4152f`
- modern-law chapter:
  `sha256:35d4877f7ff6d9ccf72786fd823216b64cfdb58e734ff352f5bb5cda06a44894`
- safeguarding chapter:
  `sha256:219389975a546bf9f2ed7701c1b37bc4550ef102c07ee223824a5cbc00ea6e0c`
- terminal scope appendix:
  `sha256:239936e6f514cdcc9a701c91f37517072cd02b8471393d37838af12b3f1c6ea4`
- source bindings:
  `sha256:61d19c61623ace3e65ec2951af02014901fb43bab9a31d17044d21f09492a521`
- source audit:
  `sha256:84c92fb19d9a068511138d886adc94e35153d728a826411a386dc08d20338391`
- installed PDF:
  `sha256:655264bafd4d2ba937d6448a2f0c30b9e8767dc27424aa013ca5b6f592f11f16`
- tracked web edition:
  `sha256:597f6458e10824fef854837f7233d1194dd569414d97304a29c7c2f14e5363d9`

Two pdfTeX passes produced a 32-page, 400,570-byte US-letter PDF. The final log
contains no fatal error, undefined reference, overfull or underfull box,
package warning, or unresolved rerun request. Every font reported by
`pdffonts` is embedded, subsetted, and carries a Unicode map; text extraction
is nonempty and contains no replacement character. The reviewed build and
installed PDF are byte-identical. The generated and tracked web Markdown are
byte-identical.

Repository review tooling rasterized the installed PDF. Inspection of all 32
pages, including full-sheet comparison and full-size checks where needed,
found no clipping, collision, broken table, isolated heading, unintended blank
page, or illegible final apparatus. The title and terminal qualification
conspicuously identify this as a 32-page interim public-alpha paper toward the
promised 100-plus substantive-page reference.

The changed patristic chapter uses only the verified Tertullian, Origen,
Jerusalem, and Eusebius bindings and keeps Justin, Irenaeus, Laodicea, and the
church-order complex outside the positive chain. The changed law chapter now
binds canon 1 and the Code's promulgation and effective date, while describing
the amendment/currentness check at its actual bounded ceiling. The changed
safeguarding chapter corrects the WHO fingerprint, removes false independent-
review language, narrows competence and capacity claims, and binds the
territorial CPS and Home Office controls without universalizing them.

**Internal source verdict: pass for the bounded current claims. Production
verdict: pass for the exact installed PDF and tracked web edition above.
Public-alpha distribution verdict: authorized and bound as a provisional
review snapshot.**

The promised 100 substantive pages and remaining source families remain open.
This checkpoint is neither the promised completed reference nor evidence of
ecclesiastical authority.

## Current 36-page reconciliation checkpoint

This 2026-07-28 checkpoint supersedes only the current-byte and present-state
claims above. Earlier dated findings remain evidence for the snapshots they
identify. The umbrella completion task remains open.

The current exact controls are:

- `main.tex`:
  `sha256:9f1ce8e6fd38da5cd940a6d26260db4cbfdb71e99675647c88fba216fd797561`
- patristic chapter:
  `sha256:031e27650bbc53966d0be66f1a8556be866ecd9f006030e18448184a3eb21217`
- medieval chapter:
  `sha256:6fee65d4d4c77b08e5b1b9f56ff284569ffa9fe89fdf5b9d455b611763c4a5d1`
- dated orientation:
  `sha256:40b2860ab0620ea8eb346147b16ae16d3f6ac77a4a424c9737714936cc642334`
- source audit:
  `sha256:9d4d26e8d6f1ca2486d8269ad8aa30087e439b2529370fd41e8f8b5adcdeee52`
- source bindings:
  `sha256:d2b91cb6b9d64ef7e01d7b8b5eebb7362c0e61954ca659966d7e8b5e8ad1b112`
- installed PDF:
  `sha256:27dbbf0566e0ac24c1ac66cf3561114034f2d3ba4a04004de917cc765df2626f`
- tracked web edition:
  `sha256:da24c39450f0c21b978426abd40223e70dc9acfcb0694aab909ce8716b9cb362`

Two pdfTeX passes produced a 36-page US-letter PDF. The installed and built
PDFs are byte-identical; the generated and tracked web editions are likewise
byte-identical. Repository review tooling rasterized all 36 pages, and review
of both contact sheets found no clipping, collision, broken table, isolated
heading, unintended blank page, or illegible terminal material.

The plans, scope, and source audit now distinguish the exact controls already
closed for present wording from broader E2 modules that remain partial or open.
The patristic chapter no longer denies the old-edition Latin and Greek controls
it now uses. The medieval chapter no longer says its local witnesses lack exact
bindings, and the dated orientation identifies the exact Vogel--Elze pages.
Repeated typological, non-linear, and non-operational ceilings were
consolidated where the claim-local distinction remained intact.

**Internal source verdict: pass for the bounded current claims. Production
verdict: pass for this exact installed PDF and tracked web edition. Completion
verdict: open.** The 100-page deliverable, incomplete E2 dependencies, remaining
draft modules, final-as-of checks, and exact-snapshot completion gates remain
unfinished.

## Current 116-page bounded-completion snapshot — 2026-07-28

This addendum supersedes the preceding present-state and completion verdicts
without rewriting their dated findings. It records the exact public-alpha
snapshot after the bounded-completion reconciliation.

“Comprehensive” is bounded and representative: every included period, module,
and consequential claim is source-audited, while inaccessible protected
critical editions, direct control of 1614 p. 220, exhaustive manuscript
collation, additional local rites and cases, and Eastern particular law remain
explicit future ceilings. They are neither silently closed nor presumed
evidence.

Exact identities:

- publication-source aggregate:
  `sha256:5f185ed607b000205bd211f0378c3c567a01ae342dd1d0646be93fb54271a447`
- research-control aggregate, excluding filenames containing `review`:
  `sha256:23227a0ebfaf05ff43562051cb011e8e713d0ba8c4c9c3168c873702189ceb39`
- `main.tex`:
  `sha256:4e8d13403b055f4c7384abfdc0397aaed988751480821a3908c418394b610362`
- generation metadata:
  `sha256:158d0d000c66c9fb409da9dab1b46f0372d1875af433ec6411e305a7a9b02d4c`
- source bindings:
  `sha256:ca226b9ee982b00c2105191c54c51bff7980171c05d889bc5b24448a61b18f43`
- source audit:
  `sha256:d2699cd6b621b50502be52fb9e696ade95b2d20782c0c089f6eb57e4e14315a9`
- evidence map:
  `sha256:354246118cb2abb70d1d8cf0fac6e9dcbe28339bbfbd6dc2385bd26025a0b3b7`
- scope:
  `sha256:814ecb6539b568891532fff94c7b8bf681f6001b3a85e43658b88897a03e9468`
- delivery plan:
  `sha256:4cf922f41db315632902f89c5111a856d19144de6ce7706459abc16ee109398f`
- comprehensive plan:
  `sha256:4b30bb0bb7f21ae80e1f2398dec4c776a9d68861d59e418c1fd9100b64dbb3d8`
- built and installed PDF:
  `sha256:3df98f535a1aa2d7cb57480da74669c097aaf7e3382c8c0ddf8b84ef14586a87`
- generated and tracked web edition:
  `sha256:49f6f99656b789c6eb06dc19ed4e1615d36efba1ace93332f4f3f4dbd5dfb707`

A fresh official-only currentness pass on 2026-07-28 found no substantive
correction to the governing claims. The official Code pages retain canons 1,
134, 230, 1166, and 1172 as described; the published
authentic-interpretations compilation has no entry for canons 134 or 1172,
which remains a bounded register check. The DDWDS catalog calls the book
*Editio typica, 1998* and *Editio typica emendata, 2004*. It distinguishes the
DESQ *Variationes* of 21 October 2021 from the related general executory decree
of 22 October 2021. The current USCCB page retains the published U.S.
implementation and pastoral statements; no visible update date is inferred.

Two pdfTeX passes produced a 116-page, 739,419-byte US-letter PDF. The first
103 numbered pages remain substantive narrative under the plan's exclusion
rule. The log contains no fatal error, undefined reference, overfull box, or
unresolved rerun request; a few pre-existing underfull boxes remain. All fonts
are embedded and subsetted with Unicode maps. The PDF is unencrypted and has
no forms or JavaScript.

Repository review tooling rasterized all 116 pages. All six contact sheets were
inspected, with the title, changed scope/currentness pages, and final metadata
pages checked full-size. No clipping, collision, broken table, unintended blank
page, sparse spill, or illegible terminal material was found. The reviewed
build and installed PDF are byte-identical. A fresh web conversion and tracked
web edition are byte-identical.

The source, evidence, rights, safety, jurisdiction, currentness, identity,
mechanical, PDF/web anti-drift, and every-page visual gates pass for this exact
bounded snapshot. It remains non-operational: no ritual formula, alleged-sign
checklist, diagnostic advice, self-test, sensational case adjudication, or
unauthorized ministry is introduced. Consent, withdrawal, continuing care,
emergency and protective action, privacy, professional competence,
safeguarding, territorial law, and accountable ecclesial authority remain
explicit.

The canonical source library remains blocked at repository scope only by a
preserved unrelated Claude publication fingerprint mismatch. The public-alpha
policy passes with 178 alpha and zero hold entries, release bindings report zero
stale entries, and journal validation passes. The unrelated repository mismatch
does not alter this publication's exact source graph or bounded verdict.

**Internal source verdict: pass. Safety and rights verdict: pass. Production
verdict: pass. Bounded completion verdict: pass.** Public alpha remains a
publication-maturity label and conveys no ecclesiastical approval.

## Alpha-apparatus release checkpoint — 2026-07-28

This addendum supersedes only the current-byte and alpha-apparatus statements
above. The source claims, source bindings, evidence map, rights analysis,
safety controls, and bounded currentness findings are unchanged.

Exact identities:

- publication-source aggregate:
  `sha256:9c7ce49994d6d46447c38906c471842fa226327a50a8ae8b0a11a9311f149100`
- research-control aggregate, excluding filenames containing `review`:
  `sha256:23227a0ebfaf05ff43562051cb011e8e713d0ba8c4c9c3168c873702189ceb39`
- `main.tex`:
  `sha256:db8039c1fc25a42d239f88c3772904d48914bfab76e2723750663673bd0a3367`
- generation metadata:
  `sha256:c3d627403896dcd316a5142470c4dc2a05cfb1458efaa229c61e6670de46c064`
- terminal scope appendix:
  `sha256:bc2dd17cf1dae76f7951723e58f4ccf5be2ab906c26dc6647ff5e4c391f195ae`
- source bindings:
  `sha256:ca226b9ee982b00c2105191c54c51bff7980171c05d889bc5b24448a61b18f43`
- source audit:
  `sha256:d2699cd6b621b50502be52fb9e696ade95b2d20782c0c089f6eb57e4e14315a9`
- evidence map:
  `sha256:354246118cb2abb70d1d8cf0fac6e9dcbe28339bbfbd6dc2385bd26025a0b3b7`
- scope:
  `sha256:814ecb6539b568891532fff94c7b8bf681f6001b3a85e43658b88897a03e9468`
- built PDF:
  `sha256:30f31cbb2e532867158d5920b7e20ccb2bd12e8dde957115dd18311ad35145f1`
- generated and tracked web edition:
  `sha256:a46014d034d8dda1aa13e5d2d9887fa4107ec8765fad5a5e0b6c24622c787a92`

The title page now carries only the terse status marker `Alpha`. The terminal
scope appendix owns the work-wide explanation of alpha distribution,
completion, review state, non-approval, and reliance boundaries. Immediate
safety and non-authority language remains on the title page because delayed
notice would create reliance risk. No epigraph or previously removed
third-party quotation was restored.

Two pdfTeX passes produced a 116-page, 736,388-byte US-letter PDF. The final
log has no fatal error, undefined reference, overfull box, or unresolved rerun
request. All fonts are embedded and subsetted with Unicode maps; the PDF is
unencrypted and has no forms or JavaScript. Repository review tooling
rasterized all 116 pages. Inspection of all six contact sheets, with the title,
changed terminal appendix, generation metadata, and final colophon checked at
full size where needed, found no clipping, collision, broken table, unintended
blank page, sparse spill, or illegible terminal material.

The generated and tracked web editions are byte-identical and reproduce the
same terminal alpha apparatus and generation timestamp. The rebuilt PDF is
authorized for installation only as the exact reviewed artifact identified
above; installed/build byte identity and release-artifact verification remain
separate mechanical gates.

**Internal source verdict: unchanged pass. Safety and rights verdict:
unchanged pass. Alpha-apparatus and production verdict: pass for the exact PDF
and web edition above.** Alpha remains a distribution state and conveys no
ecclesiastical approval.

## Superseding epigraph review — 2026-07-28

This section supersedes only the earlier findings that the Wolfe quotation and
the pop-culture-derived epigraph were absent. The restored opening uses the
reader-attested Wolfe wording at the attested first-Orb-edition p. 207 locus,
attributes the fictional speaker and author, and immediately explains that
fiction is neither Catholic teaching, evidence that curses work, nor permission
to experiment. The research records expressly state that the project did not
independently collate the protected page.

The second line is no longer attributed to “Anonymous.” It is labeled
“Editorial adaptation after Chuck Palahniuk, *Fight Club*, ch. 6 (1996);
popularized in Jim Uhls's screenplay for David Fincher's *Fight Club* (1999).”
Metadata-only source records and publication-local bindings identify both
protected works; no novel, screenplay, or film bytes are retained, and the
publication does not present underlying wording as a quotation. The terminal
scope and references identify the quotation, adaptation, fair-use critical
purpose, license exclusion, and evidence boundary. The immediate safety notice,
non-operational character, and terminal alpha apparatus remain unchanged.

Two pdfTeX passes produced a 116-page PDF with SHA-256
`3e21a13bef618e1efa3a6369280b0c833481f692f5056baf4fc1c813190e9b80`.
The final log has no fatal error, undefined reference, overfull box, or
unresolved rerun request. Repository review tooling rasterized all 116 pages
to a task-specific ignored build directory. All six contact sheets were
inspected, and the changed opening was also inspected at full size. The
epigraphs, attributions, section heading, thesis box, and immediate analysis
are legible, unclipped, and free of collisions; no pagination spill or
unintended blank page was introduced. The generated web edition has SHA-256
`308959d34c02b4db4957db1a0642cc62d7eff7bfb123ce1f5b2abaa69f68434d`
and retains both epigraphs, both attribution boundaries, the immediate
analysis, terminal rights notice, references, and generation disclosure.

Source-library validation, the leaf generation-metadata check, and the leaf
web-edition declaration check pass. The reviewed PDF and generated web edition
remain in ignored `build/` pending the coordinated installation and
release-inventory refresh after concurrent source-tree work settles; this
review does not authorize a stale release-manifest update.

## Superseding public-metadata production checkpoint — 2026-07-28

This checkpoint supersedes only the artifact identities and installation state
in the preceding epigraph review. The epigraph wording, attribution, analysis,
source bindings, rights boundary, safety language, narrative pagination, and
source verdict are unchanged.

The shared public-metadata convention now renders the revision timestamp
without a standalone `Generation Metadata` heading and without reader-facing
model, effort, runtime, or contribution-history fields. Two fresh pdfTeX passes
produced a 116-page, 714,335-byte PDF with SHA-256
`a473f7b520c1927c4838bbc036381cfd65ef1f221ccdb24deaac32d649a712f3`.
The final log has no fatal error, undefined reference, overfull box, or
unresolved rerun request. Repository review tooling rasterized all 116 pages.
All six contact sheets were inspected; the opening and terminal metadata page
were also inspected at full size. No clipping, collision, unintended blank
page, table failure, or illegible material was found.

The generated web edition has SHA-256
`48f4963ad86240e3460d8b47d612d146b127d45e27e877c99f49f730ffe527e1`.
It retains both epigraphs, both attribution boundaries, immediate analysis,
terminal rights and alpha notices, references, and the public revision
timestamp while suppressing the same nonpublic provenance details as the PDF.
Source-library validation, the leaf PDF metadata check, and the provider web
declaration check pass. The exact PDF and web artifacts identified here are the
reviewed installation candidates; shared inventories and aggregate release
records remain outside this leaf-owned checkpoint.

## Superseding record-consistency checkpoint — 2026-07-29

This checkpoint supersedes the preceding artifact identities and reconciles
the publication's scope, evidence map, references, and publication-state
records with the already source-controlled Loudun module, the exact Joannou
control for Laodicea 26, and the installed public-alpha state. The substantive
extent is now defined reproducibly as Arabic-numbered pages 1--104, from the
governing thesis through the pastoral conclusion; terminal apparatus begins on
page 105. No specialist, clerical, intended-reader, or ecclesiastical review is
introduced as an alpha gate.

Two settled pdfTeX passes produced a 116-page, 714,658-byte PDF with SHA-256
`8120b6d7a8554a21909f793c853bb8839dd2a75d7f03bc17d8751bc8a2d613d1`.
The final log has no fatal error, undefined reference, overfull box, or
unresolved rerun request. Repository review tooling rasterized all 116 pages
and generated six contact sheets. Every contact sheet was inspected, with the
corrected scope, Laodicea reference, and final colophon also checked at full
size; no clipping, collision, spill page, unintended blank page, or illegible
material was found.

The regenerated web edition has SHA-256
`859949795f023003f592b622910fdaecbcf20304062a55ab311571c11fb71696`
and carries the same corrected scope, evidence boundary, reference ceiling,
publication state, page metric, and revision timestamp. The leaf generation
metadata and web-edition declaration pass. Provider-wide source-library and web
currency checks are presently blocked only by unrelated dirty-tree defects
identified in the Abraham/daylight-stars and Linen publications; they do not
alter this leaf's exact build or web/PDF identity.
