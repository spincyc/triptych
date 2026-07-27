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

The promised 100 substantive pages, remaining source families, and every
unperformed external human, professional, rights, specialist, priestly, and
ecclesiastical review remain open and deferred. This checkpoint is neither the
promised completed reference nor evidence that any human or ecclesiastical
authority reviewed or approved it.
