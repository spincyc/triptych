# Project Work Register

This is Triptych's provider-neutral operational memory. Read it together with
`promised-deliverables.toml` before starting or resuming work, after a context
handoff, and before reporting completion. “Published,” “built,” “committed,”
“pushed,” “review copy,” and “complete” are different states.

Last reconciled: 2026-07-27.

## Current integration and publication state

The repaired public-alpha snapshot is committed and pushed through commit
`5909c483`. Pull request 1 is open and mergeable against `main`. The repair
branch has not been integrated into `main`, and GitHub Pages has therefore not
deployed these repairs. The stable review landing page for the exorcism paper is
`library/catholic-exorcism.md`; its branch artifact links the PDF and web
edition. Production discoverability remains blocked on integration and the
Pages workflow.

## Promised work

### Exorcism reference

<!-- promised-deliverable: task-2-exorcism-100-pages -->

The requested result is a researched, substantive 100+ page Catholic exorcism
reference, not a padded PDF. The current review edition is 29 physical pages.
Commit `bc479596` expanded and published that interim edition and added a
dedicated landing page, but did not fulfill the extent or hard-review promise.
Research acquisition, claim-level source work, safety and canon-law review,
substantive expansion, and exact-snapshot every-page review remain open.

### Linen-cloths restoration

<!-- promised-deliverable: task-6-linen-restoration -->

Commit `242aa461` restored bounded burial-practice and material context in the
GPT paper and rebuilt its artifacts. Current source, PDF, web, audit, and
every-page evidence still require one exact-snapshot reconciliation. The
Claude edition is independently stale.

### Altar-server guide series

<!-- promised-deliverable: task-1-altar-server-guides -->

Commit `be940904` repaired the seven guide/card PDFs and replaced the four
retained old Low Mass images. All are publicly discoverable review copies on
the branch. Independent server-guide, rights, liturgical-text permission, and
applicable renewed-snapshot reviews remain open; a build is not those reviews.

### Sanctuary pictorial dictionaries

<!-- promised-deliverable: task-3-sanctuary-dictionaries -->

Commits `0b1f79ae`, `7a05f79e`, `50794fc6`, and `8533fcd9` created, exposed,
and repaired six priestly-review PDFs. Complete object inventories, exact
source collation, independent priestly review, and artwork review remain open.
The artwork audit also retains 15 held notices: two sub-300-DPI historical
assets and thirteen unidentified depicted-object cases.

### Missa Cantata guide and cards

<!-- promised-deliverable: task-4-missa-cantata -->

The rebuilt guide and cue cards are installed and linked as review copies.
Physical-print, intended-reader, independent ceremonial, rights, and
ecclesiastical review of the exact snapshot remain open.

### Solemn Mass guide and cards

<!-- promised-deliverable: task-5-solemn-mass -->

The rebuilt guide and cue cards are installed and linked as review copies.
Physical-print, intended-reader, independent ceremonial, rights, and
ecclesiastical review of the exact snapshot remain open.

### Review-publication discoverability

<!-- promised-deliverable: project-review-discoverability -->

Repository policy now keeps produced PDFs discoverable while honestly labeling
review state. Branch validation found 164 release publications, 14 review
publications, and no held publication in the generated public-alpha artifact.
Production-site route and visible-label validation remains open until the
branch is integrated and Pages deploys.

### Recently discussed paper hard review

<!-- promised-deliverable: project-recent-paper-hard-review -->

The required set is Catholic Exorcism, Last Supper, Abraham and the Daylight
Stars, John 6, and Linen Cloths. The exorcism and GPT linen work received
substantive repair, but the set has not passed one complete current-guidance
audit. Staleness currently reports Last Supper, GPT and Claude Abraham, GPT
John 6, and Claude Linen; this promise remains open.

## Full repository discrepancy audit

The 2026-07-27 audit establishes the following actionable backlog:

| Audit ID | Finding | Current measure | Completion evidence |
| --- | --- | ---: | --- |
| `AUD-INTEGRATE-001` | Pushed repairs are absent from production Pages | 1 open PR; branch not on `main` | integrated commit plus successful Pages artifact verification |
| `AUD-STALE-001` | Rendered publications disagree with current inputs or records | 88 editions | `make check-staleness` passes |
| `AUD-SOURCES-001` | Reusable-source family screening is incomplete | 140 of 227 review units pending | `make check-source-family-screening` passes |
| `AUD-REVIEW-001` | Public review copies retain unclosed completion gates | 14 publications | each work-specific review record closes against its exact snapshot |
| `AUD-ART-001` | Dictionary artwork has held identification/resolution notices | 15 notices | artwork validator and human review records close every notice |
| `AUD-MEMORY-001` | Conversation outcomes were not exhaustively represented in tracked work records | prior ledger had 8 broad items | every known agreement is represented here and in the ledger when criteria are known |

The audit findings promoted to acceptance-criterion work are tracked below.

<!-- promised-deliverable: project-integrate-and-deploy -->
<!-- promised-deliverable: project-stale-editions -->
<!-- promised-deliverable: project-source-family-screening -->
<!-- promised-deliverable: project-public-review-gates -->
<!-- promised-deliverable: project-dictionary-artwork-holds -->

The 88 stale editions comprise 33 Claude and 55 GPT editions. They span
articles, biographies, histories, liturgy, Mariology, theology, curricula, and
devotions. The immediately discussed stale papers are named above; the
authoritative reproducible inventory is the output of `make
check-staleness`. Staleness is a work queue, not proof that every edition needs
the same substantive edit.

## Reconciliation history

- 2026-07-27: Reconstructed the altar-server, dictionary, exorcism, linen,
  discoverability, and recent-paper commitments from tracked evidence and
  current user direction. Confirmed five repair commits and the public-alpha
  binding commit are pushed but not integrated.
- 2026-07-27: Ran the repository-wide staleness, source-family, public-review,
  artwork, and integration audit. Recorded unresolved counts without promoting
  them to completion.
- Earlier conversation history is not itself a durable repository source.
  Any additional remembered agreement must be added here immediately and
  reconciled against the repository rather than inferred away.
