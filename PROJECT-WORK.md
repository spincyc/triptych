# Project Work Register

This is Triptych's provider-neutral operational memory. Read it together with
`promised-deliverables.toml` before starting or resuming work, after a context
handoff, and before reporting completion. “Published,” “built,” “committed,”
“pushed,” “review copy,” and “complete” are different states.

Last reconciled: 2026-07-27.

## Standing public-alpha authority

On 27 July 2026 the maintainer approved every Triptych document for
conspicuously labeled public-alpha distribution so that priests and other
qualified readers can review it from stable public links. This is a standing
workflow authorization: changed source may be researched, built, inspected,
installed, bound as an exact current public-review snapshot, committed,
integrated, pushed, and deployed without requesting a new document-by-document
alpha approval.

Public-alpha approval is distribution authority only. It never records or
implies human, priestly, specialist, ecclesiastical, rights, intended-reader,
physical-print, or final editorial review that has not actually occurred.
Every unresolved work-specific gate remains explicit in the research records,
release inventory, catalogs, and this register. A publication remains
conspicuously provisional until those gates are genuinely closed.

Research for the promised work is limited to publicly reachable sources. Do
not purchase an edition, use a paid subscription, request credentials, or ask
the maintainer to fund source access. When a necessary witness cannot be
reached publicly, pursue proportionate public primary, official, library, and
critical-edition alternatives, then record the access boundary and resulting
open evidence gate without inventing verification.

## Current integration and publication state

The repaired public-alpha snapshot is integrated on `main` through commit
`b93e64b4`; pull request 1 is merged, and GitHub Pages workflow run
`30296605957` successfully deployed that exact commit on 27 July 2026. The
stable review landing page, PDF, and web-edition routes for the exorcism paper
resolve in production. Exact production reconciliation remains open because
`library/catholic-exorcism.md` still labels the installed and deployed 29-page
PDF as a 20-page paper.

## Clean-agent restart

For the next clean isolated agent started from current `main`, use this
instruction:

> Read `AGENTS.md`, `PROJECT-WORK.md`, `promised-deliverables.toml`,
> `guidance/promised-deliverables.md`, and the guidance and research records
> applicable to the first selected workstream. Reconcile the register against
> current `main` and production Pages before editing. Continue the highest
> actionable open requirement; do not infer completion from a commit, PDF,
> catalog link, push, or deployment. Update the register and ledger before each
> checkpoint commit.

The restarting agent must then:

1. Run `git status`, confirm isolation, and preserve unrelated changes.
2. Confirm that `f6e9d2e2` is contained by `main`. If it is not, stop content
   work and report that integration remains open.
3. Run `scripts/check-promised-deliverables`, `make check`, `make
   check-staleness`, and `make check-source-family-screening`. The latter two
   are expected to fail until their recorded backlogs are actually closed;
   record changed counts rather than concealing the failures.
4. Build and verify the public artifact with `scripts/public-alpha check`,
   `scripts/public-alpha build`, and `scripts/public-alpha verify
   --deployment-target github-pages`; separately verify the live production
   routes after Pages completes.
5. Resume in this order unless the maintainer gives a new priority:
   `task-2-exorcism-100-pages`; `project-recent-paper-hard-review`;
   `task-1-altar-server-guides`;
   `task-4-missa-cantata`; `task-5-solemn-mass`;
   `task-3-sanctuary-dictionaries`; `task-6-linen-restoration`; then the
   repository-wide staleness, source-family, public-review, and artwork queues.
6. For the exorcism work, begin with its tracked comprehensive expansion plan,
   scope, source audit, and final exact-snapshot review record. Acquire and
   verify research before drafting; preserve the 100 substantive-page
   requirement and the source, safety, law, PDF, web, and every-page gates.
7. Reconcile this file after each independently reviewable work unit. Keep
   completed facts, current evidence, open criteria, blockers, and superseded
   decisions distinct. Commit and push coherent checkpoints when authority
   remains current, but never call the underlying deliverable complete unless
   its ledger gate passes.

Integration, target-branch updates, deployment, and any history rewriting
remain separately authorized operations. The restart instructions do not
grant those authorities.

## Promised work

### Exorcism reference

<!-- promised-deliverable: task-2-exorcism-100-pages -->

The requested result is a researched, substantive 100+ page Catholic exorcism
reference, not a padded PDF. The current review edition is 29 physical pages.
Commit `bc479596` expanded and published that interim edition and added a
dedicated landing page, but did not fulfill the extent or hard-review promise.
The next source-grounded tranche expands the patristic chapter from 1,225 to
3,076 words using only seven already verified passage bindings in Tertullian,
Origen, the Jerusalem catecheses, and Eusebius; its uninstalled build candidate
is 32 physical pages. Justin, Irenaeus, Laodicea, and the church-order complex
remain excluded from positive claims until their required controls are closed.
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
Production-site route and review-label validation passed for the deployed
artifact. Exact catalog-text reconciliation remains open because the exorcism
landing page understates the deployed PDF as 20 rather than 29 pages.
The standing 27 July 2026 public-alpha authority permits future exact-current
review snapshots to be installed and deployed without repeated
document-by-document approval while preserving every unresolved review gate.

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
| `AUD-INTEGRATE-001` | Repair integration and Pages deployment | Integrated through `b93e64b4`; Pages run `30296605957` succeeded | passed; exact catalog-text discrepancy retained under the affected work |
| `AUD-STALE-001` | Rendered publications disagree with current inputs or records | 88 editions | `make check-staleness` passes |
| `AUD-SOURCES-001` | Reusable-source family screening is incomplete | 140 of 140 review units pending across 227 source families | `make check-source-family-screening` passes |
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
- 2026-07-27: Added the clean-agent post-merge restart sequence, priority
  queue, exact verification commands, exorcism re-entry point, and authority
  boundary.
- 2026-07-27: Confirmed that pull request 1 was merged, `main` contains the
  repair series through `b93e64b4`, and Pages workflow run `30296605957`
  successfully deployed that commit. Retained the exorcism landing page's
  20-versus-29-page discrepancy as open exact-production reconciliation.
- 2026-07-27: Completed the first bounded exorcism expansion tranche from
  already verified patristic bindings. The changed source builds to an
  uninstalled 32-page candidate; web regeneration, every-page review,
  installation, and all final completion gates remain open.
- 2026-07-27: Recorded the maintainer's standing authority to publish every
  document as a conspicuously provisional public-alpha snapshot for priestly
  and qualified-reader review. This authorizes the ordinary build, install,
  exact-snapshot binding, commit, integration, push, and deployment workflow
  without repeated alpha approvals, but supplies no human or ecclesiastical
  review and closes no substantive completion gate.
- 2026-07-27: Limited all continued research to publicly reachable sources.
  Paid editions, subscriptions, credentials, and maintainer-funded acquisition
  are outside scope; inaccessible necessary witnesses remain explicit evidence
  gaps after proportionate public-source alternatives are pursued.
- Earlier conversation history is not itself a durable repository source.
  Any additional remembered agreement must be added here immediately and
  reconciled against the repository rather than inferred away.
