# Project Work Register

This is Triptych's provider-neutral operational memory. Read it together with
`promised-deliverables.toml` before starting or resuming work, after a context
handoff, and before reporting completion. “Published,” “built,” “committed,”
“pushed,” “review copy,” and “complete” are different states.

Last reconciled: 2026-07-31.

## Standing public-alpha authority

On 27 July 2026 the maintainer approved every Triptych document for
conspicuously labeled public-alpha distribution so that priests and other
qualified readers can review it from stable public links. This is a standing
workflow authorization: changed source may be researched, built, inspected,
installed, bound as an exact current public-review snapshot, validated, and
committed without requesting a new
document-by-document alpha approval.

A clean direct Codex session on `main` has standing authority to make ordinary
coherent commits for authorized work and regularly push validated checkpoints
to `origin/main` after each independently reviewable unit. Before each push,
run the checks required by the affected guidance, inspect the exact outgoing
range, and confirm that every newly reachable object is intended for public
disclosure. Because each `origin/main` push triggers GitHub Pages, this
authority includes the resulting automatic deployment attempt. It does not
authorize force-pushing, amending or otherwise rewriting published history,
changing remotes, integrating a retained worker, or triggering another
deployment mechanism. Never represent a snapshot as live until its Pages run
has succeeded and the affected production routes have been verified.

Public-alpha authorization is distribution authority only. It never records
or implies human, priestly, specialist, ecclesiastical, rights, intended-reader,
physical-print, or final editorial approval that has not actually occurred.

On 31 July 2026 the maintainer retired the six-concern alpha completion
assessment — source support, rights and distribution status, safety, artifact
consistency, mechanical correctness, every-page visual inspection — as
bookkeeping the project imposed on itself. No tool ever read those fields; they
were prose scoring prose. A publication is alpha when it is built, checked by
the gates that actually run, and published.

What that retirement does not touch, because none of it was ever the
bookkeeping: a known defect still stays explicit in the research records,
release inventory, catalogs, and this register — recording a defect is how a
reader learns of it, not a gate. Passing an internal check still does not imply
external approval, and the workflow still creates no placeholder gate for a
reviewer who is not coming. Those are statements about what is true, and
withdrawing a scoring scheme does not make them false.

## Research staleness is suspended

On 31 July 2026 the maintainer suspended the research-staleness signal. Nothing
is to be flagged stale, and **the papers are to be left exactly as they are**.
No research is re-read, no review record is written, and no edition is
rebaselined until the suspension is lifted.

Two reasons, and the second is the larger. The signal measures the wrong thing:
it reports a publication stale when any artifact appears under a work it cites,
not when an input it binds changes, so a paper on the virtues reported 156
changed inputs, every one a Clementine verse table it does not bind. And the
tooling under these papers is still moving — the calendars, the concordance, the
commentary chain and the source library all changed materially in a single day —
so anything this tooling will eventually invalidate, it has not finished
invalidating. A baseline taken now is taken against a moving one.

**Suspended, deliberately not rebaselined.** Rebaselining writes down that the
research was re-read against the changed inputs. That review did not happen, and
recording it would put a false statement in 24 editions to make a number go to
zero. Suspension records the true thing instead: measurement has stopped.

`make check-staleness` reports the suspension and exits clean;
`make measure-staleness` still runs the raw signal for anyone who wants to look
at it without acting on it. Nothing in the ledger or in any paper was touched.

**How this ends:** one full pass back through the research, when the tooling has
matured — not edition by edition as the flag fires. TASK-93 repairs what
staleness measures and is a prerequisite of that pass, not of lifting the
suspension.

Research is not limited to publicly reachable sources. On 31 July 2026 the
maintainer withdrew the rule that had forbidden purchasing an edition, using a
paid subscription, requesting credentials, or asking the maintainer to fund
source access, on the ground that it was never a requirement of anything — it
was a self-imposed limit that turned an ordinary cost question into a permanent
evidence gap. Where a witness would settle a question, name it and what it
would cost; the maintainer decides whether to obtain it.

Two things this does not change, because neither was ever a project rule.
Copyright and licence terms bind whatever the research budget is: a text the
project may read is not thereby a text it may republish, and the standing
public-alpha authorization is authority to distribute this project's own work,
never someone else's. And a witness that has not actually been consulted is
still unconsulted — record what was read, not what was reachable.

The maintainer authorizes creation and revision of project-owned AI artwork
for the sanctuary pictorial dictionaries and altar-server guide series. Each
asset must remain grounded in publicly reachable, source-controlled evidence;
carry its exact generation or edit provenance, references, hash, rights,
corrections, consumers, and review state; and remain visibly provisional where
review is open. Artwork may not invent or silently resolve an object's
identity, morphology, scale, arrangement, ceremonial use, historical state, or
an actor's liturgical action. AI creation supplies no human artwork,
liturgical, ceremonial, or ecclesiastical review.

No external human-review cycle will be available for some time. Human,
priestly, specialist, intended-reader, physical-use, and ecclesiastical review
are therefore neither promised workflow steps nor alpha completion gates.
Continue research, revision, artwork production, mechanical and AI-assisted
audit, building, installation, public-alpha binding, integration, push, and
deployment against the six concrete concerns above. Record an external review
only if it actually occurs, and never convert internal or AI checking into a
claim of human approval.

## Current integration and publication state

The repaired public-alpha snapshot is integrated on `main`; pull request 1 was
merged, and subsequent validated checkpoints have continued through the direct
`main` workflow. The stable review landing page, PDF, and web-edition routes
for the exorcism paper have resolved in production checks. The current
repository source, installed PDF, web edition, comprehensive plan, and exact-
snapshot audit agree on a completed bounded study of 116 physical pages,
including 103 substantive narrative pages. Each later `origin/main` checkpoint
requires its own successful Pages run and verification of the affected
production routes before it is represented as live.

## Clean direct-main workflow

For a clean direct Codex session started from current `main`, use this
instruction:

> Read `AGENTS.md`, `PROJECT-WORK.md`, `promised-deliverables.toml`,
> `guidance/promised-deliverables.md`, and the guidance and research records
> applicable to the first selected workstream. Reconcile the register against
> current `main` and production Pages before editing. Continue the highest
> actionable open requirement; do not infer completion from a commit, PDF,
> catalog link, push, or deployment. Update the register and ledger before each
> checkpoint commit. After validating each independently reviewable unit,
> inspect its exact outgoing range and push it to `origin/main`; then verify the
> resulting Pages run and affected production routes.

The restarting agent must then:

1. Run `git status`, confirm the current branch is `main`, reconcile it with
   `origin/main`, and preserve unrelated changes.
2. Confirm that `f6e9d2e2` is contained by `main`. If it is not, stop content
   work and report that integration remains open.
3. Run `tools/tpt check-promised-deliverables` and `make check`. Do **not** act
   on research staleness: it is suspended, `make check-staleness` reports the
   suspension, and the papers are left as they are until the tooling settles.
   `make check-source-family-screening` still fails, and honestly — 144 review
   units are unscreened and marking them screened would record a review that did
   not happen. Record the count; do not close it by writing it down.
4. Build and verify the public artifact with `tools/tpt public-alpha check`,
   `tools/tpt public-alpha build`, and `tools/tpt public-alpha verify
   --deployment-target github-pages`; separately verify the live production
   routes after Pages completes.
5. Resume in this order unless the maintainer gives a new priority:
   `task-2-exorcism-100-pages`; `project-recent-paper-hard-review`;
   `task-1-altar-server-guides`;
   `task-4-missa-cantata`; `task-5-solemn-mass`;
   `task-3-sanctuary-dictionaries`; `task-6-linen-restoration`; then the
   repository-wide staleness, source-family, exact-snapshot, and artwork queues.
6. For the exorcism work, begin with its tracked comprehensive expansion plan,
   scope, source audit, and final exact-snapshot review record. Acquire and
   verify research before drafting; preserve the 100 substantive-page
   requirement and the source, safety, law, PDF, web, and every-page gates.
7. Reconcile this file after each independently reviewable work unit. Keep
   completed facts, current evidence, open criteria, blockers, and superseded
   decisions distinct. Commit the coherent unit, run its required validation,
   inspect the exact outgoing range and public-exposure consequences, and push
   the checkpoint to `origin/main`. Verify the Pages result before calling that
   snapshot live, but never call the underlying deliverable complete unless
   its ledger gate passes.

Retained-worker integration, non-Pages deployment, remote changes,
force-pushing, and all other history rewriting remain separately authorized
operations.

## Promised work

### GPT deep-research redevelopment

<!-- promised-deliverable: project-gpt-deep-research-redevelopment-2026-07-29 -->

The maintainer identified substantive underdevelopment—not merely stale dates
or presentation—in five GPT publication leaves: the 1962 Tenth Sunday after
Pentecost; Years A, B, and C of the postconciliar Eighteenth Sunday in Ordinary
Time; and *Catholic Exorcism: History, Discipline, and Pastoral Practice*. Each
requires a full source-first redevelopment that broadens the relevant source
families and deepens treatment of the strongest witnesses, material
disagreements, transmission, and limits. Existing prose is provisional, and
page count or repeated source summaries do not establish completion.

The authorized scope is GPT only. Claude publications may be inspected to
understand cross-provider staleness or dependencies, but they must not receive
material source, PDF, web, catalog, release, or baseline changes under this
work. Provider-neutral reusable evidence may be corrected or extended only
where the GPT research requires it; such a change does not authorize rebuilding
or revising a Claude consumer. Completion requires current publication-local
research records, source and rights gates, rebuilt and installed GPT PDFs and
web editions, every-page visual inspection, coherent release records, and
validated pushed checkpoints.

Completed 29 July 2026. The five GPT leaves now contain new comparative
research dossiers or synthesis, checked reusable source records and bindings,
superseding material-change reviews, and exact production records. Nine PDFs
(the five full publications and four proper syntheses) and five canonical web
editions were rebuilt, inspected page by page, installed with exact build
identity, and passed the repository's metadata, component, web-currentness,
source-library, source-inventory, source-family-screening, public-alpha, and
release-binding gates. The affected GPT staleness records are fresh. No file
under `src/claude`, `pdf/claude`, or `web/claude` changed.

### Exorcism reference

<!-- promised-deliverable: task-2-exorcism-100-pages -->

The requested result is a researched, substantive 100+ page Catholic exorcism
reference, not a padded PDF. The current public-alpha edition is 120 physical
pages, of which the first 108 numbered pages are substantive narrative under
the tracked exclusion rule. The comprehensive plan, delivery plan, source
audit, evidence map, scope record, and final exact-snapshot review agree that
the bounded representative study meets the promised extent and that its
source, evidence, rights, safety, jurisdiction, currentness, PDF/web anti-
drift, and every-page visual gates pass on one exact snapshot. The installed
PDF and reviewed build are byte-identical, as are the freshly generated and
tracked web editions. Protected critical editions, direct control of 1614
p. 220, exhaustive manuscript collation, additional local rites and cases,
and Eastern particular law remain explicit future-research ceilings; they do
not reopen the bounded completion verdict or imply ecclesiastical approval.
The controlling evidence is
`research/final-exact-snapshot-review-2026-07-29.md` beside the publication.

### Linen-cloths restoration

<!-- promised-deliverable: task-6-linen-restoration -->

Commit `242aa461` restored bounded burial-practice and material context in the
GPT paper and rebuilt its artifacts. Both provider editions now have one
reproduced exact-current snapshot: the GPT and Claude PDFs rebuild
byte-for-byte to the installed artifacts, their web conversions likewise
match, and all 46 pages have current visual-review evidence. Exact-byte
distribution clearance and internal review do not imply independent
exegetical, patristic, rabbinic, text-critical, or ecclesiastical approval.

### Altar-server guide series

<!-- promised-deliverable: task-1-altar-server-guides -->

Commit `be940904` repaired the seven guide/card PDFs and replaced the four
retained old Low Mass images. All are publicly discoverable review copies on
the branch. The current PDFs carry no reader-facing release-state strip or
label; page counts, card counts, maps, hashes, and production records agree,
and every page has been visually reviewed.
The remaining ledger requirement is exact-snapshot agreement among the Low
Mass and trainer PDFs, maps, hashes, artwork records, and every-page visual
evidence. Rights or liturgical-text permission uncertainty and any concrete
source, safety, artifact, mechanical, or visual defect remain open when
recorded; unavailable external review is not a placeholder gate.
The series-wide sequenced checklist is
`src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/research/delivery-work-plan-2026-07-27.md`;
it governs the shared Low Mass work and the Missa Cantata and Solemn Mass
deliverables without conflating their remaining gates.

### Sanctuary pictorial dictionaries

<!-- promised-deliverable: task-3-sanctuary-dictionaries -->

The six sanctuary pictorial dictionaries have current inventory, omission,
source, artwork, page-count, and review records that agree with their installed
PDFs. The artwork validator reports zero notices; unsupported identities or
uses remain omitted or held rather than being invented. These objective
records establish the current alpha state without implying human artwork,
priestly, or ecclesiastical approval.
The sequenced inventory, artwork, edition, and publication checklist is
`src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/research/delivery-work-plan-2026-07-27.md`.

### Missa Cantata guide and cards

<!-- promised-deliverable: task-4-missa-cantata -->

The rebuilt guide and cue cards are installed and linked as public-alpha
copies. Completion remains open until their source support, rights and
distribution status, safety, artifact consistency, mechanical correctness,
and every-page visual evidence agree on one exact snapshot. This does not
imply external ceremonial or ecclesiastical approval.

### Solemn Mass guide and cards

<!-- promised-deliverable: task-5-solemn-mass -->

The rebuilt guide and cue cards are installed and linked as public-alpha
copies. Completion remains open until their source support, rights and
distribution status, safety, artifact consistency, mechanical correctness,
and every-page visual evidence agree on one exact snapshot. This does not
imply external ceremonial or ecclesiastical approval.

### Review-publication discoverability

<!-- promised-deliverable: project-review-discoverability -->

Repository policy now keeps produced PDFs discoverable while honestly labeling
review state. Branch validation found 164 release publications, 14 review
publications, and no held publication in the generated public-alpha artifact.
Production-site route and review-label validation passed for the previously
deployed artifact. The current repository release inventory contains 164
release publications and 14 review publications, 178 total; the exorcism
source, installed PDF, web edition, and audit records agree on 116 physical
pages, including 103 substantive narrative pages.
The standing 27 July 2026 public-alpha authority permits future exact-current
snapshots to be installed and deployed without repeated document-by-document
authorization while preserving every concrete defect in the six alpha
concerns.

### Recently discussed paper hard review

<!-- promised-deliverable: project-recent-paper-hard-review -->

The required set is Catholic Exorcism, Last Supper, Abraham and the Daylight
Stars, John 6, and Linen Cloths. The exorcism and GPT linen work received
substantive repair, but the set has not passed one complete current-guidance
audit. Publication-local internal current-guidance audits now identify and
reconcile the exact installed, web, catalog, and release states for Last
Supper, both Abraham editions, and GPT John 6 while preserving all disclosed
evidence ceilings and without implying external approval. Exorcism and both Linen
editions remain separate exact-snapshot boundaries, and the set-level promise
remains open.

## Full repository discrepancy audit

The 2026-07-27 audit establishes the following actionable backlog:

| Audit ID | Finding | Current measure | Completion evidence |
| --- | --- | ---: | --- |
| `AUD-INTEGRATE-001` | Repair integration and Pages deployment | Integrated through `b93e64b4`; Pages run `30296605957` succeeded | passed; exact catalog-text discrepancy retained under the affected work |
| `AUD-STALE-001` | Rendered publications disagree with current inputs or records | 92 recovered baseline editions; 93 in this checkpoint because the exorcism source audit and delivery plan now correctly make that edition stale pending its later rebuild | `make check-staleness` passes |
| `AUD-SOURCES-001` | Reusable-source family screening | 140 of 140 review units screened across 229 source families; 806 reviewed owner-family presences; atomic citation coverage remains false | `make check-source-family-screening` passes |
| `AUD-REVIEW-001` | Public-alpha copies require exact-snapshot evidence or explicit concrete defects | 14 publications at the recorded checkpoint | each work-specific record resolves the six alpha concerns against its exact snapshot |
| `AUD-ART-001` | Dictionary artwork identification/resolution notices | 0 validator notices; held unsupported assets remain explicit | artwork validator passes without implying external approval |
| `AUD-MEMORY-001` | Conversation outcomes were not exhaustively represented in tracked work records | prior ledger had 8 broad items | every known agreement is represented here and in the ledger when criteria are known |

The audit findings promoted to acceptance-criterion work are tracked below.

<!-- promised-deliverable: project-integrate-and-deploy -->
<!-- promised-deliverable: project-stale-editions -->
<!-- promised-deliverable: project-source-family-screening -->
<!-- promised-deliverable: project-public-review-gates -->
<!-- promised-deliverable: project-dictionary-artwork-holds -->

The recovered baseline had 92 stale editions spanning articles, biographies,
histories, liturgy, Mariology, theology, curricula, and devotions. This
checkpoint intentionally changes two exorcism research records, so the current
working-tree audit reports 93 until that existing edition is rebuilt in its
queued source/drafting or public-artifact work. The immediately discussed
stale papers are named above; the authoritative reproducible inventory,
including the current provider split, is the output of `make
check-staleness`. Staleness is a work queue, not proof that every edition needs
the same substantive edit.

The source-family screening backlog is closed at the family level. Complete
semantic review of all 140 exact owner surfaces added 242 missing presences,
removed 13 false-positive or redundant presences, and retained 806 reviewed
owner-family relationships in total. This does not assert atomic citation
coverage, which remains explicitly false, and unsupported catalog-expansion
leads remain outside the ledger until their own family records are justified.

## Commentary discovery chain

The research algorithm maps a scripture passage to the commentary works worth
pulling into the source vault, then unions those mappings across every proper.
`commentary-work-index discover` is the repo-maintained lookup and
`build-corpus` the union. `tools/harvest` populates the index and
`src/sources/commentary/passage-commentary-index.yaml` now carries the result of
six harvest runs, so a lookup resolves to the works the harvest actually
recorded rather than to nothing.

Weighting is already implemented and needs no schema change. Each mapping
carries a `confidence` float that orders works within a passage, and
`build-corpus` accumulates a reciprocal-rank `score` across passages, so a work
recurring at good rank through many propers outranks one appearing once.

On 30 July 2026 the maintainer accepted the nondeterminism of a model-ranked
"top 20", judging the head of the list unlikely to differ materially between
runs. The concern was that a generated ranking is not a measured citation count
and that variance is largest for obscure passages, which is where the volume is
— 572 of 1301 distinct references are Psalms, many of them ferial antiphon
fragments. The accepted resolution is to define `confidence` as multi-run
agreement frequency rather than a model-asserted score, so the stability claim
is measured rather than assumed and low-agreement works self-identify for
review. Harvest results belong in a dated, tracked ledger; every downstream
tool reads that ledger, which is what keeps the chain repeatable even though
the harvest step is stochastic.

## Tool CLI consolidation backlog

The 2026-07-30 tool review left a deliberate remainder. Delivered: the layout
returned to `tools/<id>` so `tmt check` gates it; the launcher's controls became
dash-prefixed options that a registry id cannot shadow; every registered tool
gained a `tests/tools/<id>.test`; and registry drift, hardcoded paths, and
`usage` staleness are asserted in `tools/tests/test_tool_registry.py`.

The remainder changes interfaces the Makefile, guidance, and release records
depend on, so each needs its own scoped unit rather than an incidental edit:

| Item | Change | Blast radius |
| --- | --- | --- |
| Flag vocabulary | One meaning per flag: `--root` currently carries four, leaf identity has five spellings, `--provider` three shapes | ~20 tools, Makefile, guidance, source READMEs |
| Shared dispatcher | Adopt `scripts/_tooling.py`'s `run_verb_cli` beyond its four current users, giving every tool `--json` and one error contract | 17 tools |
| Verb vocabulary | Collapse 27 verbs onto a closed lifecycle set; `check`/`validate`/`verify` and `bootstrap`/`prepare`/`build-corpus` are synonyms today | 11 verb-bearing tools, Makefile, guidance |
| Id naming | Retire the `check-*` prefix into a `check` verb on the domain tool; `web-edition` and `check-web-edition` already declare the dependency | 7 registry ids, Makefile, guidance, release hash records |

Sequence the flag and dispatcher work first: neither renames an id, and both
make the verb and id changes mechanical. The id renames come last because they
move release hash records and every smoke-test filename together.

## Reconciliation history

- 2026-07-31: Twenty-two commits, none pushed. **Site shape.** The landing page
  became the library and its prose moved to `ABOUT.md`, which still opens
  "Don't Panic"; the separate Library page was retired as a second name for the
  same thing. The four reading pages were being copied into the artifact rather
  than rendered, so they alone carried no Triptych header, navigation, footer or
  robots metadata — they now render through `layout.html` like the other 131,
  and all 135 were audited. Two hand-copied duplicates of the site's section
  palette were deleted with that change. `doc/` became `pdf/`, so `src`, `pdf`
  and `web` read as the three forms of every publication.
  **Calendars.** Sixty commemorations folded into 1962 feast names became
  entries of their own, and `check-calendar-masses` now refuses the pattern;
  five absent celebrations were authored and three refused for want of a
  witness; eight masses that existed and no date could reach were dated. Both
  calendars are wholly reachable, 459 of 459 and 268 of 268.
  **Scripture.** Every publishable bible now typesets as a two-column volume
  carrying its own rights notice. 926 of 2190 propers citations were missing the
  commentary index, 888 of them because the lookup preferred "Psalm" over the
  parsed "Psalms". The Knox copyright question was settled from the primary
  record: the US registrations were renewed, R525394 and R646862, so it is
  protected until 2039 and 2043.
  **Policy.** The maintainer withdrew the research-conduct rule, the
  family-screening requirement and the six-concern alpha assessment, and
  suspended research staleness. Nothing was rebaselined and no paper was
  touched, because a cleared flag would have asserted a review that did not
  happen.
- 2026-07-31: Retired `PROJECT-HANDOFF-2026-07-30.md`. Every task in its "where
  to pick up" section had landed and its opening line, "nothing is committed,"
  had stopped being true. The two facts it held that no other artifact did — that
  no authorised bulk source exists for the NRSV or the NABRE, and what is lost by
  not having the NABRE — moved into `guidance/bibles-for-agents.md` as a recorded
  access boundary. Re-measured that document's open-work and
  fails-silently sections against the repository rather than against memory: the
  clamp in `Bible.span` is gone, `citation_divergences` covers twelve books
  rather than four, and the unresolved counts rose in every edition because a
  citation that used to be truncated into a neighbour now refuses.
  `guidance/liturgy/postconciliar-illustrated-dictionary-handoff.md` is a forward
  handoff for unstarted work and was left alone.
- 2026-07-29: Reorganized the public library into the seven approved portals:
  Faith, Scripture, Liturgy, History, Formation, Mary, and Law. Applied their
  muted white, gold, red, green, violet, rose, and black accents and distinct
  ornament pairs throughout the generated site, reserving ℣/℟ for Liturgy.
  Removed reader-facing release-state banners and document labels. Installed
  the expanded 16-page Tenth Sunday synthesis, the sparse lower-third exorcism
  title page with consolidated terminal endnote, and the exact reviewed
  no-label GPT PDF set; Claude publication sources and artifacts were not
  changed.
- 2026-07-29: Retired unavailable human, priestly, specialist,
  intended-reader, physical-use, and ecclesiastical review as placeholder
  alpha gates. Recast current completion tracking around source support, rights
  and distribution status, safety, artifact consistency, mechanical
  correctness, and every-page visual inspection. External approval is recorded
  only when it actually occurs and is never inferred from internal or AI
  review.
- 2026-07-28: Reconciled the exorcism promise ledger and work register to the
  exact bounded-completion evidence: 116 physical pages, 103 substantive
  narrative pages, and passing source, safety, rights, law/currentness,
  PDF/web anti-drift, and every-page review gates. Retained explicit future-
  research ceilings and the public-alpha non-approval boundary.
- 2026-07-28: Superseded the isolated-worker/final-maintainer-push boundary
  with the clean direct-`main` workflow. Authorized ordinary coherent commits
  and regular validated checkpoint pushes to `origin/main`, including their
  automatic Pages deployment attempts, while retaining exact outgoing-range
  review, public-disclosure checks, live-route verification, and the
  prohibition on force-pushing or rewriting published history.
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
- 2026-07-27: Combined that tranche with bounded canon-law and safeguarding
  repairs, built and inspected all 32 pages, installed byte-identical PDF and
  web artifacts, corrected the landing-page extent, and bound the exact alpha
  snapshot. At that checkpoint the promised 100 substantive pages remained
  open; production would not change until maintainer integration and push.
- 2026-07-27: Recorded the maintainer's standing authority to publish every
  document as a conspicuously provisional public-alpha snapshot for priestly
  and qualified-reader review. This authorizes the ordinary build, install,
  exact-snapshot binding, validation, and worker-commit workflow without
  repeated alpha approvals, but supplies no human or ecclesiastical review and
  closes no substantive completion gate. Final integration into `main` and
  push are reserved to the maintainer.
- 2026-07-27: Limited all continued research to publicly reachable sources.
  Paid editions, subscriptions, credentials, and maintainer-funded acquisition
  are outside scope; inaccessible necessary witnesses remain explicit evidence
  gaps after proportionate public-source alternatives are pursued.
- 2026-07-27: Authorized project-owned AI artwork creation and revision for
  the sanctuary pictorial dictionaries and altar-server guides, subject to
  exact provenance, rights, source-control, consumer, and review records and
  without treating generated output as human factual or artistic review.
- 2026-07-27: Recorded the then-current expectation that external review would
  be deferred. The 2026-07-29 reconciliation supersedes its use as an alpha
  completion gate while retaining the non-approval boundary.
- 2026-07-27: Replaced the worker's earlier integration, push, and deployment
  authority with the maintainer's final boundary: complete and commit every
  predecessor step in the isolated worker, but leave integration into `main`
  and every push to the maintainer.
- Earlier conversation history is not itself a durable repository source.
  Any additional remembered agreement must be added here immediately and
  reconciled against the repository rather than inferred away.
