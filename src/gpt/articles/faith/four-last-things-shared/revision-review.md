# Four Last Things: GPT revision, 12 October 2026

## Scope and decisions

This revision follows a cold review at
`5fc4fe6b6071d0c4da9bc36dbf8740172d944db0`. It covers the four GPT essays,
their research, generated web editions, print presentation, and their Faith
catalog entries. The maintainer expressly reserved all Claude documents for
a Claude agent. Claude source, web, and publication records are excluded.

The essays retain their titles and independent discursive arguments. Death
introduces the seasonal connections; Judgment explains purification and the
two judgments; Hell treats final loss and conversion; Heaven completes the
sequence with communion, resurrection, and renewed creation. Exact source
encounters replace duplicated exposition. Research and authority distinctions
remain in the owning leaves, with local qualifications beside affected claims.

The print format and companion navigation have one GPT owner in this directory.
Only the four GPT PDF targets import it. The short essays begin with a compact
title and substantive text; PDF bookmarks retain section navigation without
two pages of front matter. The web editions remain generated from the same
authoritative TeX sources. No global converter, site layout, or stylesheet
change is part of this revision.

## Content review

Two source-focused revision lanes prepared Death/Judgment and Hell/Heaven.
A separate GPT reviewer read all four bodies and reference lists, followed by
coordinator review. This is an internal editorial review, not ecclesiastical
or specialist approval. Each leaf's `research/source-audit.md` identifies
the passages actually consulted, their authority, rights, and evidence limits.
Live consultation does not certify an uninspected registered artifact.

The initial independent review accepted the collection after three corrections:
Judgment's unqualified assertion about identifying a particular damned person
was replaced by a bounded statement about our authority; its mercy heading
was brought into line with Aquinas's argument; Death's opening reference to
“this fact” was clarified after insertion of the seasonal paragraph. Selected
independent primary checks covered Augustine, *City of God* XXII.30, and
Aquinas, ST III.59.5 and I.21.4. These supported the new accounts of freedom,
memory, continuing consequences, and mercy underlying justice.

The accepted sequence gives each essay a distinct task:

| Essay | Governing argument and improved source encounter |
| --- | --- |
| Death | Christ overcomes an enemy without making grief faithless; Augustine XIII.4–5 explains why the baptized still die. Personal continuity, Baptism, Viaticum, resurrection, and suffrages remain connected. |
| Judgment | Particular judgment settles destiny; final judgment brings bodily consummation and completed public truth. ST III.59.5 excludes new postmortem merit or demerit; *Spe salvi* 47–48 connects purification and effective intercession. |
| Hell | Final loss differs from purification. Matthew 25, Augustine XXI.11 and 23, and identified Thomistic arguments support a bounded treatment of culpability, finality, justice, prayer, and hope. |
| Heaven | Communion with the Trinity fulfills the same person, soul and body. John 17, Irenaeus V.2.2–3, Augustine XXII.30, and Vatican II connect vision, Eucharist, resurrection, renewed creation, and present charity. |

The reviewer suggested optionally adding Florence to Heaven's degrees
paragraph. The present passage accurately identifies Aquinas's particular
explanation and makes no exhaustive claim about its authoritative witnesses.
The revision retains that bounded attribution without adding an unexamined
citation. No further substantive correction remained. Completeness here
means preserving the governing distinctions and connections within four
readable essays; it does not require a fifth essay, a survey of every school,
or added classroom apparatus.

## Initial accepted print editions

The publishable render sources were finalized at `2026-10-13T01:34:35Z`
(12 October locally). All four PDFs were built to the repository's fixed-point
criterion. A separate production reviewer used `tools/tpt pdf-review` and
inspected every page, with full-size inspection of openings, terminal pages,
and changed page breaks. The coordinator also inspected the opening and
verified the accepted files against the installed copies.

All four essays are five pages: twenty pages in total, down from twenty-seven.
This reduction comes from compact opening matter, focused prose, and natural
pagination while increasing the body to 11pt. Two isolated continuation lines
at page tops were corrected with local widow control and all twenty pages
reviewed again. References and rights colophons are intact and legible; no
clipping, overlap, overfull boxes, undefined references, or bookmark warnings
remain. The terminal underfull-box diagnostic is visually harmless.

| Essay | Pages | Section bookmarks | Accepted PDF SHA-256 |
| --- | ---: | ---: | --- |
| Death | 5 | 11 | `445ed8620ddd8238cece33e9551a03622163b5248bd594200dd753234a33dc63` |
| Judgment | 5 | 12 | `7f6a2f751bb99db894cb3c6529545a0f0ff14d991c50dafb4ef744a48ebf2143` |
| Hell | 5 | 9 | `2b7751aa50be0f3c42232d8031a64f6f31c0076754ecb49e7bb90ce441d72178` |
| Heaven | 5 | 11 | `7cd3a648ac877961cf3d6fbbc4175e244f5697eb43874a8aac21ac39f14a36af` |

All fonts are embedded with Unicode maps; extracted text is complete. Every
PDF companion link names an existing sibling PDF, and each section bookmark
has its own destination. `make install` verified byte identity with these
accepted builds. The PDFs are untagged; no assistive-technology certification
is claimed. [production-review.json](production-review.json) pins the accepted
PDFs, generated web editions, and render sources. PDFs remain ignored local
build/install products under the repository's normal source-build policy.

## Initial web and integration review

The four tracked web editions were regenerated solely from the authoritative
TeX, including the same companion navigation. The Faith catalog now identifies
the four subjects neutrally and displays each provider's actual title. No
Claude source, web edition, publication record, or generated catalog data was altered.
The shared format has a GPT-only source owner and four explicit Make consumers;
the regression test checks that it creates no Claude import edge.

The actual public-alpha renderer, pinned Python Markdown 3.10.3, release
layout, and stylesheet produced five local HTML routes: Faith and the four
essays. Chromium inspected all five at measured CSS viewports of 1440×900,
1024×768, 768×1024, 393×852, and 320×852. Local fixed-size frames supplied the
exact viewports because the headless command-line window clamps narrow sizes.
This was local-file responsive testing, not device emulation or HTTP serving.

The first browser pass found the catalog's long titles cramped in its
horizontal table at narrow widths. Four stacked subject entries with explicit
provider labels resolved that finding. All five catalog sizes were inspected
again; all sixteen reading/PDF links retain their correct provider, subject,
and bound PDF alias. The four article HTML outputs were byte-identical to their
previously reviewed versions. Each has one title, loaded release styles, four
working local companion destinations, and readable scope and reference
sections. No document or revised collection-section horizontal overflow
remained. Other catalog tables were not redesigned.

The review does not claim HTTP hosting, external-link availability, PDF-download
behavior, a complete rebuilt release, or deployment. The source inventories
retain existing evidence states; the added shared render owner is GPT-only.
The family ledger remains explicitly pending where it was pending before;
this revision does not claim a completed corpus-wide source-family migration.

## Initial integration disposition

The baseline and revised `make check-sources` pass. The settled publication
checks also pass: `make check-document-catalogue check-release-bindings
check-web-editions`, generation metadata, fixed-point PDF builds and installation,
all section-anchor checks, and generated-web anti-drift. The two targeted unit
suites, `tools.tests.test_source_inventory` and `tools.tests.test_publication_links`,
pass all 36 tests. The final release-binding refresh is restricted to Faith,
the document catalog data, and the four GPT web editions. Regeneration after
that refresh reproduces all five visually accepted HTML files byte-for-byte.

The complete `make check` reaches its example-transcript replay but does not
pass that repository-wide gate. The following fourteen example invocations
have pre-existing differences, established from the base Git objects and the
pre-edit source-check output, rather than inferred from this revision:

| Example group | Invocations | Recorded expectation and base state |
| --- | ---: | --- |
| Generation metadata | 2 | Captures expect 139 GPT and 58 Claude canonical records; the base already has 141 and 60. |
| Proper components | 2 | Captures expect 16 GPT component manifests; the base has 18. |
| Web declarations | 1 | Capture expects 72 eligible GPT leaves; the base has 74. |
| Commentary standing | 2 | Captures expect 25 of 25 published lane authors; the baseline reports 27 of 29. |
| Source reader | 3 | Captures expect 935 works, 1050 editions, 2918 artifacts, 5260 passages and 4132 structure files; the base has 936, 1056, 2936, 5277 and 4138. |
| Public-alpha check/preparation | 4 | Successful captures require the installed corpus. This fresh checkout began with none of its 253 issue PDFs installed; this task builds only its four GPT essays. |

The affected source-inventory, family-migration, source-library,
promised-deliverables, and research-staleness examples are recaptured from
their actual runs. No failing publication check is recaptured as a successful
one. The first broad replay also observed the coordinator's concurrent
research-record and catalog edits; those observations did not indicate writes
by the tools. The settled replay of affected examples and the targeted checks
own the final result: all 34 affected examples replayed with zero divergence
and zero tracked-state writes. The raw staleness examples intentionally return nonzero
when they report stale inputs; their captures retain that diagnostic behavior.

The completion-ledger check also requires evidence for earlier, unrelated
promises. Twenty-six existing PDF artifacts were recovered unchanged from
local caches, with their source revision metadata verified; older cached
revisions were replaced by matching existing copies. None was reauthored or
rebuilt. This permits `check-promised-deliverables --require-complete
gpt-four-last-things-2026-10-12` to pass without weakening historical evidence
requirements. It does not supply the complete installed corpus.

The staleness workflow remains suspended under `guidance/staleness.md`.
No baseline was reset to imply a comprehensive re-reading of unrelated
library growth, and no Claude state was cleared. The initially accepted work was a
coherent GPT revision on `feature/flt`; main integration and deployment were
outside that first authorization. The later authorization and correction
round are recorded below. Remaining corpus-wide example maintenance and unbuilt
unrelated PDFs do not invalidate the inspected and accepted four editions.

## Subsequent cold review and correction — 12 October 2026

A fresh reviewer read each GPT essay at `ed19fb6da73b9b09bc7a3350e76b825e76f97091`,
without relying on the initial acceptance. The coordinator reread the series,
verified the artifact identities, inspected all twenty PDF pages on contact
sheets with full-size openings and terminal pages, and inspected the four
mobile web openings. No major doctrinal, structural, or visual defect emerged.
Four minor findings were accepted and corrected after the maintainer expressly
authorized the repairs and a push to `main`:

- Death now identifies the Douay–Rheims American-1899 witness and supplies
  John 6:55 beside the Catechism's John 6:54 numbering. Both identify the
  same Eucharistic resurrection promise.
- Judgment attributes disclosure of forgiven sins to Thomas's account in
  Supplement q.87 a.2, preserves his opinion-level qualification and Peter
  Lombard's contrary view, and identifies the posthumous Supplement in its
  references. The source audit and catalog binding identify the live
  English Dominican/New Advent encounter without certifying an uninspected
  central artifact.
- Hell's redundant work-wide scope sentence is removed from the argument;
  the terminal limitation and all substantive hope distinctions remain.
- Heaven states directly that the risen neither marry nor are given in
  marriage, retaining the distinction between fulfilled love and conditions
  not revealed to us.

An independent review of these changes accepted all four corrections against
their primary controls. This bounded correction pass does not claim another
exhaustive review of unchanged content. The corrections preserve the existing
four-essay architecture and all Claude source, web, and publication records.

The corrected render sources were finalized at `2026-10-13T02:21:37Z`.
All four builds reach the repository's fixed-point criterion and remain five
pages each. The initial print hashes and browser observations above describe
the earlier snapshot; `production-review.json` identifies the corrected
accepted artifacts. All twenty corrected PDF pages were reviewed, including
full-size openings and terminal pages. Judgment's expanded references remain
legible on page five, with its colophon intact. Metadata, fonts, extracted
text, links and bookmarks pass, and installed bytes match the reviewed builds.
The faithful generated web editions were separately accepted at 1440, 393 and
320 CSS pixels: twelve changed-passage states and six title/reference
screenshots. No overflow, missing text, or navigation defect remained.

The four cold-review corrections are accepted. The previously
missing unchanged installed corpus has been recovered from the exact deployed
base snapshot: all 247 unchanged included PDFs match the live publication
manifest, their declared render inputs match the base, and their generation
metadata validates. This recovery changes no publication content and allows
complete local deployment validation of the corrected series.

The corrected editions pass `make check-sources check-deployment-sources
check-release-bindings check-web-editions check-promised-deliverables`, the
complete `make public-site`, and `public-alpha verify --deployment-target
github-pages`. The 36 source-inventory and publication-link tests pass again.
The complete site's four article HTML files are byte-identical to the
independently reviewed outputs.

The renewed broad `make check` reaches all 247 runnable examples with no
tracked-state writes. Before recapture, seventeen examples differ: two ledger
counts, four catalog counts, one preparation-inventory length, and the ten
inherited generation-metadata, proper-component, web-declaration, commentary-
standing and source-reader differences identified above. The first seven
are recaptured from actual runs for this accepted publication state; no
implementation changes are made to the tools. All eighteen examples in the
three refreshed tools then replay with no divergence or tracked-state writes.
The public-alpha example refresh changes its source checksum, so its narrow
release binding and production receipt are refreshed as well; the generated
article HTML remains identical to the visually accepted files.
Three unrelated examples still
require the absent `build/core-last-20.pdf`; six model/network or writing
examples remain deliberately exempt. The full release corpus has resolved
the initial deployment-artifact limitation.

## Verified publication — 13 October 2026 UTC

An ordinary fast-forward push placed the accepted revision on `origin/main`
at `6a9148ffe24fd28e05e60d87dff8b5bc12189968`. The automatically triggered
[Pages run 38337906346](https://github.com/spincyc/triptych/actions/runs/38337906346)
succeeded; its deployment job completed at `2026-10-13T02:52:05Z`.
[Repository-hygiene run 38337906324](https://github.com/spincyc/triptych/actions/runs/38337906324)
also passed. The hosted build independently passed its source gate, full
artifact build and GitHub Pages compatibility verification.

A separate reviewer fetched fifteen routes at <https://mystago.gy/> after
deployment: four GPT article HTML routes, four canonical PDF routes, their
four public PDF aliases, the Faith catalog, document catalog JSON, and the
publication manifest. Every response was HTTP 200 and byte-identical to the
accepted local site. All twelve article/PDF route hashes match the production
receipt, and all eight downloaded PDFs pass generation-metadata validation.
Faith retains the sixteen expected GPT and Claude links for the series.

The live manifest contains the same 251 publications as the preceding
deployment. Its four revised GPT PDF hashes match acceptance; all 247 other
publication PDF hashes remain unchanged. All sixty Claude document catalog
entries also compare equal to the base. This verifies both the corrected
publication and the protected Claude boundary. `production-review.json`
retains the commit, workflow, manifest hash and bounded live-check result.
The authorized revision, correction and main publication are complete.
