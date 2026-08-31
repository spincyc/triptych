# Project Work Register

This is Triptych's provider-neutral operational memory. Read it together with
`promised-deliverables.toml` before starting or resuming work, after a context
handoff, and before reporting completion. “Published,” “built,” “committed,”
“pushed,” “review copy,” and “complete” are different states.

Last reconciled: 2026-08-28.

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

## Corpus browser redesign

A multi-agent project to make the non-PDF web surfaces one navigable scholarly
corpus rather than a set of separately built instruments. The PDFs remain the
canonical printable editions and are not a redesign target.

The governing plan on this branch is `guidance/corpus-browser-master-plan.md`.
It splits the work: a design lane owns the visual and product contract, and an
implementation lane owns production code and tests.

`guidance/corpus-browser-implementation.md` is the implementation lane's durable
technical record — how the surfaces are actually built, what will refuse a
change, the proposed sequencing, the ranked risks, and the conflicts returned for
disposition. Reconnaissance is done.

Two facts from that record belong here because they bind unrelated work. First,
`make check` fails at `c27d69153` on `check-tool-registry` and `check-examples`,
and `python3 -m unittest discover -s tools/tests` fails with 14 failures and 13
errors out of 1226; both were reproduced at the base commit in a separate
checkout, so the redness is pre-existing and no later lane may be credited or
blamed for it. Eight of those thirteen errors were later shown to be a stale
fixture rather than a defect — every `test_public_alpha` case wrote a stub root
hardcoding `Markdown==3.10.2` after the repository's lock moved to 3.10.3 —
and `f434c5b91` on `impl/shell-plumbing` fixed it, moving the baseline to **14
failures and 5 errors on that branch and its descendants**. A branch based
before `f434c5b91`, including `impl/foundation-hardening`, should still expect
14 and 13. Second, the corpus lanes overlap the in-progress deliverable
below, which owns `reader-shell.js` and `reader-instrument.css` and declares
public-navigation redesign unauthorized. Sequencing the two was returned as the
first open conflict in that document; the review recorded below settled it.

### Which branch carries what

**Superseded by the 2026-08-10 foundation integration recorded below.** `main`
now carries the six corpus documents, the accepted design and engineering
foundation, and the three corpus ledger entries. The table and cautions below
are kept as the pre-integration state they document; read current documents on
`main`.

No corpus-browser document was on `main`, which was `fc3092de9` as of 2026-08-08
and six commits ahead of the shared base `c27d69153`. The seven lane branches
all still based on `c27d69153`; the two `fix/*` branches did not, because they
were bug fixes taken against `main` itself.

Branch heads, all read from `origin` on 2026-08-08:

| Branch | Head | Bases on | Carries |
| --- | --- | --- | --- |
| `main` | `fc3092de9` | — | no corpus-browser document |
| `impl/foundation` | `af2c9613c` | `c27d69153` | master plan, implementation record, `build/agent-continuity/corpus-browser-foundation-recon.md` |
| `impl/foundation-hardening` | `ecfb4e7b8` | `impl/foundation` | the same three, plus §19 of the implementation record, which exists nowhere else |
| `impl/shell-plumbing` | `c62b83904` | `impl/foundation` at `b87dfc744` | the same three; its implementation record lacks §19 |
| `impl/catena-wave-1` | `efd7559a9` | `impl/foundation` at `b87dfc744` | the same three; its implementation record lacks §19 |
| `ux/foundation` | `3b5938a0d` | `c27d69153` | vision, roadmap, inventory, research, `docs/triptych-world-class-corpus-master-plan.md`, `src/web/browser/prototypes/corpus-foundation/`, `tools/tests/test_corpus_foundation_prototype.py`, `tools/tests/corpus_foundation_prototype_browser.mjs`, `build/agent-continuity/corpus-browser-foundation.md`, and the design lane's ledger entry |
| `ux/corpus-wave-1` | `e42b92874` | `c27d69153` **directly** | vision, roadmap, inventory, research, master plan, implementation record — six documents, and none of the prototype or continuity files |
| `ux/corpus-wave-1-review-fixes` | `ecbd93a05` | `ux/corpus-wave-1` | the same six |
| `fix/day-missal-switch` | `f099e2280` | merged into `main` | — |
| `fix/browser-truthfulness` | `fc3092de9` | merged into `main`; it *is* `main` | — |

Read every one of those documents on the branch that owns it —
`git show <branch>:<path>` — rather than here. They are deliberately not
reproduced, summarised, or paraphrased in this register: a fact has one owner,
and a second copy of a design contract is a disagreement waiting to happen.
`ux/foundation` also carries the design lane's own ledger entry and
work-register section, which is why neither appears on this branch.

Two cautions the table above is the evidence for. First, this table as it stands
on `impl/shell-plumbing` (`PROJECT-WORK.md:215` there) tells a reader that
`guidance/corpus-browser-implementation.md` lives on
`impl/foundation-hardening` — that is, not on the branch they are reading it
on. It is on four branches and the four copies differ. Second, the
`ux/corpus-wave-1*` copies of the
implementation record are a **rewrite pinned at `af2c9613c`**, so they carry as
live four defects that `impl/foundation-hardening` has since fixed — the
`none-claimed` gloss, history's `.field` collision, texts' `.detail` shadow and
`T.fail`'s silent no-op. A Wave-1 agent reading its own branch's copy would act
on repaired work. `guidance/corpus-browser-implementation.md` §5, §11 step 5 and
§20 on `impl/foundation-hardening` are the current statement.

### Acceptance, 2026-08-08

The coordinator dispositioned both lanes on 2026-08-08.

| Lane | Disposition |
| --- | --- |
| A0, surface inventory | accepted |
| A1, research synthesis | accepted |
| A2, site-wide product vision | accepted with amendments D1–D20 |
| A3, tokens and Reader/Catalogue/Instrument archetypes | accepted as foundation direction, not as pixel acceptance of any production route |
| A4, shared navigation, Jump, Related, and shell interaction | accepted with the bounded-Jump and protected-liturgy amendments |
| Claude reconnaissance | accepted |
| the neutral gates | accepted for integration |

The A3 wording governs what implementation may assume. The direction is
accepted; no production route is visually accepted, so no route may cite A3 as
approval of how it renders. The roadmap on `ux/foundation` still records A0–A4
as candidates awaiting independent review; this register is later than that
record, and the design lane had not yet written the dispositions down. (Since
the 2026-08-10 integration, the roadmap on `main` is the Wave 1 rewrite, which
carries the amended dispositions; the `ux/foundation` ledger entry keeps its
honest `candidate` state because its own independent-disposition requirement
was answered by this register and the later Wave 1 review, not by the ZIP
review it originally named.)

### Foundation integration, 2026-08-10

The blocker this section used to record — "B0 cannot start" because no
integration base existed — is resolved. The accepted foundation was
reconciled onto **current `main`** (not the stale `c27d69153` base) and landed
as three merges plus this record:

1. `ux/foundation` (`3b5938a0d`) — consumed in full: A0–A4 documents, the
   corpus-foundation prototype and harnesses, continuity record, and the
   design ledger entry, per the 2026-08-08 coordinator dispositions above.
2. `impl/foundation` + `impl/foundation-hardening` (`81fa65d76`) — consumed in
   full: implementation record with §19, recon continuity record, the neutral
   gates (static parse, artifact gate, URL-contract, harness-runner, and
   collision suites), preview-build wiring, five design-neutral browser
   fixes, and the fail-closed hardening ledger entry, which honestly remains
   `in_progress` with `shared-shell-blocking-collisions-resolved` open on the
   protected `day-missal.css` hazard.
3. `ux/corpus-wave-1` + `ux/corpus-wave-1-review-fixes` (`01eb3eb1e`) —
   documents consumed: the rewritten program-level master plan, vision,
   roadmap, inventory, research, the Wave 1 ledger entry (complete), and the
   acceptance records. The disposable prototype overlay and its harnesses
   were deliberately **not** merged, per the acceptance's own scope limit;
   they remain on the preserved branches. The wave's rewritten implementation
   record was replaced by the engineering lane's, as this register directed.

Semantic reconciliation against the six newer `main` commits (missal-switch,
truthfulness, and URL/page-truth fixes): `history.js` and `texts.js` carry
both lines of fixes; the release bindings were regenerated with
`tools/release-bindings` for the seven browser files the integration changed,
on top of `main`'s current hashes, so no old signature resurrected.

**Deliberately not integrated**, each awaiting its own recorded gate:

- `impl/shell-plumbing` (`c62b83904`): generator/layout plumbing, Makefile
  target hygiene, the stale `test_public_alpha` fixture fix (`f434c5b91`),
  and the single-`main`-landmark change. No acceptance record exists. Its
  content is the natural input to B0 and should be consumed under B0's own
  gates, not merged wholesale.
- `impl/catena-wave-1` (`efd7559a9`): the E1 implementation of the accepted
  E0 contract, with its 36-test suite and re-signing. E1 was authorized to
  proceed independently, but no acceptance disposition of the implementation
  is recorded; under the plan's acceptance model it stays off `main` until
  independent review dispositions it. It is the nearest-to-ready pending
  lane.
- `impl/didach-domain` and `ux/didach-identity`: the abandoned `didach.ai`
  direction; not part of this program.

**Domain state.** The public origin moved to `https://mystago.gy/` through
GitHub Pages settings and DNS; the old project-path origin 301-redirects.
`tools/public-alpha` now declares the custom-domain origin, constructs and
verifies canonical `og:url` and `og:image` metadata there, and keeps all
in-artifact navigation relative so the same static artifact remains portable
under a GitHub Pages project-path preview. Triptych remains the product and
repository identity; this repository change corrects metadata and does not
perform or imply a deployment.

**Gate baseline for this tree.** `check-browser-gate` over the built site:
2,290 assertions, **228** failures — 117 single-`main`, 82 target-size, 27
skip-link/modal-trap, 2 narrow-320 overflows (`/sources/` by 24px, `/texts/`
by 56px). The same gate over a pure-`main` build reports the identical 228,
so the two overflow findings are main's newer surfaces measured for the first
time, not an integration regression. The hardening branch's recorded 226
described its own older tree.

**Next action.** B0/B1 — the production shared-shell primitives and their
regression harness — are unblocked and authorized: the design contracts and
shared-shell acceptance are recorded above, and the plan's sequence
(foundation → catalogue/reader/instrument lanes → cross-object links/search →
final acceptance) is unchanged. A Claude engineering lane should start B0
from the current `main` tip on a fresh `impl/` branch, consuming
`impl/shell-plumbing`'s work under B0's gates. New lanes start from `main`;
no standing integration branch exists or is a dependency.

**Deviation, recorded because it is real: Wave 1 started off-base.** The master
plan requires that "once `corpus/foundation-integration` is pushed, all new
Wave 1 work starts from its exact head"
(`guidance/corpus-browser-master-plan.md:1585`, and again at `:1658` and
`:1790`). `ux/corpus-wave-1` (`e42b92874`) was created as a single commit
directly on `c27d69153`, not on any integration head, and
`ux/corpus-wave-1-review-fixes` (`ecbd93a05`) descends from it. Neither branch
descends from `ux/foundation` or from any impl branch; the two lanes' documents
were reconciled onto that branch by hand instead, which is precisely the work
the integration branch exists to do once and durably. The consequence is already
visible: those branches carry a rewritten implementation record pinned at
`af2c9613c` that presents four repaired defects as live. The wave should be
rebased onto the integration head when it exists, and its implementation record
replaced rather than merged.

The narrower claim this section used to make — that no shared shell is
implemented on any branch — still holds. `impl/shell-plumbing` changed the
generator and the layout wrapper; it built no shared shell.

### Foundation hardening

The 2026-08-08 review settled the sequencing question above by protecting the
liturgy surface family outright, so promoting `reader-shell.js` into a shared
shell is withdrawn rather than deferred: reuse its ideas, not the owned file.

`impl/foundation-hardening` carries the work that does not depend on the visual
contract, each commit cherry-pickable by path. The four real-Chromium
harnesses are invoked at last by `check-browser-harnesses`, which depends on
`public-preview` because three of them address it as their data root — the
reason they were read as broken for months was a missing build, not rot. The
artifact gate moved to the governing matrix and gained no-JavaScript, subpath
deep-link, link-resolution and focus-indicator coverage. Every published hash
contract is pinned by 46 tests before anyone cleans up a router. Both new gates
stay out of `make check`, which builds no artifact and cannot assume a browser.

Three things that lane found are worth recording outside it. The gate's
skip-link failures are a modal focus trap in the Propers reader, not a missing
link, and belong to the liturgy deliverable rather than to any corpus lane. The
Source Library's "Back to the corpus" does not leave a bare fragment as
reported; it leaves the entire reader hash, so a reload reopens the edition the
reader just closed. And target size fails on all nineteen routes — history alone
has 909 undersized controls — which is a design-lane dependency, not a hardening
defect.

Measured baselines for anyone comparing. `make check` takes about 310 seconds
and is red at the base for reasons this project did not cause.

`check-browser-gate` is no longer "about 74 seconds" and no longer reports 146
failures; both figures were true at `0fcf0cb95` and are true nowhere now. The
gate was widened to the five-viewport governing matrix, which took it to 2,290
assertions and surfaced an entire new failure class. **Re-run at `ecfb4e7b8` on
`impl/foundation-hardening`: 93 seconds, 2,290 assertions, 1,836 passed, 226
failed, 228 skipped**, across 19 routes and 9 states, with two consecutive runs
agreeing. The 226 are 117 `single-main-element`, 82
`primary-controls-meet-target-size` and 27 `skip-link-targets-existing-element`,
and nothing else.

**The number differs by branch and a single figure would be false on one of
them.** On `impl/shell-plumbing` the same gate reports **109**, because
`6b5742bf2` gave every published page exactly one main landmark and closed the
117; that branch's figure is taken from that commit's own measurement rather
than re-run here. Cite the branch with the number.
`guidance/corpus-browser-implementation.md` §17.5 owns the full arc and §20 owns
the disposition of each surviving class. Compare failure sets, never exit codes.

The lane also gave ten previously unrecorded browser defects a tracked home, and
recorded eight reported findings that re-checking refuted, in
`guidance/corpus-browser-implementation.md` §20. Before that section they existed
only in agent reports in a scratch directory, which §14's amendment D10
forbids — and a scratch directory is deleted, so they were one `rm` from being
rediscovered at full cost.

### Ledger gap: the implementation lane has no promised deliverable

The design lane recorded `corpus-browser-foundation-design-2026-08-08` in
`promised-deliverables.toml` on `ux/foundation`. **The implementation lane
recorded nothing.** Its diff against `c27d69153` touches `PROJECT-WORK.md` and
does not touch the ledger, so nothing fail-closed tracks the implementation work
at all — no promise, no acceptance criteria, and no requirement that a later
session must either satisfy or explicitly supersede. That is a live breach of
`guidance/promised-deliverables.md`, which requires a substantive outcome to be
recorded with a stable ID *before* material implementation, and this lane shipped
material implementation: two new gates, a harness target, 46 hash-contract tests,
three production renames and signature changes, and seven re-signed browser
files.

The promise and its completion criteria are known, so per that guidance they are
specified here for immediate promotion into the TOML ledger. **The ledger file
itself is outside this task's exclusive file boundary and was deliberately not
written**, because `promised-deliverables.toml` is shared across every branch
and a malformed entry breaks `make check` everywhere; the write belongs to
whoever holds the ledger. Adding only the `<!-- promised-deliverable: … -->`
marker was also rejected: the validator checks ledger ids against the register
and not the reverse, so a bare marker would pass silently while pointing at a
promise that does not exist, and would then read as a duplicate the moment the
entry landed.

The entry to add, `id = "corpus-browser-foundation-hardening-2026-08-08"`, owner
`guidance/corpus-browser-implementation.md`, state `in_progress` — not
`candidate`, because one prerequisite is open and the record is on no integrated
branch:

| Requirement | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| `durable-architecture-record` | A tracked record states how the non-PDF browser surfaces are built, what will refuse a change, the verifiable sequencing, the ranked risks, the conflicts returned for disposition, and the defect register with each finding's status and each refuted finding's refutation. | `pass` | `guidance/corpus-browser-implementation.md` |
| `artifact-gate-over-the-built-site` | A design-neutral gate drives real Chromium over the built artifact across the five-viewport governing matrix, asserts no visual contract, skips cleanly with a stated reason when no browser resolves, and stays out of `make check`. | `pass` | `tools/tests/corpus_browser_gate.mjs`, `Makefile` |
| `chromium-harnesses-are-run` | The four reader harnesses have a target that builds their data root first and holds them to a recorded pass floor rather than to a zero exit. | `pass` | `Makefile`, `tools/tests/test_browser_harnesses.py` |
| `published-hash-contracts-pinned` | Every published hash key of every instrument is pinned by test before any router cleanup, including the keys that are deliberately input-only. | `pass` | `tools/tests/test_browser_url_contract.py` |
| `shared-shell-blocking-collisions-resolved` | The four selector and plumbing hazards that block a shared shell are resolved with an unchanged rendered DOM: the `#reading`/`#banner` hard-coding, history's `.field`, texts' `.detail`, and `day-missal.css`'s unscoped `body > .site-header`. | `open` — three of four done (`a912e182e`, `bad976039`, `9e980ff5b`); `day-missal.css` is protected liturgy and needs that deliverable's authority | `src/web/browser/shared/browser-core.js`, `src/web/browser/history/history.css`, `src/web/browser/texts/texts.css`, `tools/tests/test_browser_collisions.py` |
| `no-visual-or-product-decision` | The lane changes no visual contract, accepts no screenshot baseline as an oracle, and makes no production change to a protected liturgy asset. | `pass` | `guidance/corpus-browser-implementation.md` |

<!-- promised-deliverable: corpus-browser-foundation-hardening-2026-08-08 -->

The entry above is now in `promised-deliverables.toml`, and this comment is its
one work-register marker. Five requirements pass; the sixth stays open because
`day-missal.css` is protected liturgy and needs that deliverable's authority,
which is the honest state rather than a rounding of it.

## Promised work

### Mary as the New Ark: journey, dogmas, and virginal marriage

<!-- promised-deliverable: gpt-mary-new-ark-journey-2026-08-15 -->

**Corrected, reviewed, installed, pushed, and verified live on 16 August
2026.** The two provider editions now share one catalog
row while retaining their different titles, provider-qualified routes, PDF
bytes, the published GPT web reader, and each edition's own drawings. The GPT
edition replaces its rough wavy-line schematics with a source-first two-panel
graphite atlas and five finely detailed graphite Ark/sanctuary plates.
Reader-facing prose calls the scene 2 Samuel 6 and uses ``2 Reigns'' only when
it explicitly explains the Septuagint title; the older Douay ``2 Kings'' name
is likewise identified rather than silently mixed with modern numbering.

The source-audited study gives a vivid account of the Ark's journey; receives Mary
confidently as its living New-Covenant fulfillment because she bears Christ;
synthesizes exact patristic, saintly, liturgical, and magisterial witnesses;
and shows the four Marian dogmas as the full unfolding of that vocation without
displacing Christ as the covenant's definitive fulfillment.

Joseph and Mary's chastity is neither omitted nor reduced to a negative Uzzah
analogy. Their true virginal marriage receives a positive synthesis centered
on Joseph's commanded reception of Mary, Davidic fatherhood, spousal love, and
ordered guardianship of the divine Presence. Uzzah remains only a bounded
contrast between unappointed handling and obedient service; the study rejects
any implication that marriage is defiling, Mary physically dangerous, or
Joseph's continence terror-driven.

The reviewed and installed GPT PDF is 46 letter-size pages at SHA-256
`0d995ac1d447f53cc55496fa8907c16a7940639b986fee02579b16e87d7164da`;
the generated and installed GPT web edition is byte-identical at SHA-256
`8083f51e35ce1d72fdd306d23c378361e70f778ee27f1a7acaeb915c1e27a2d4`.
The rebuilt and installed 65-page Claude PDF is byte-identical at SHA-256
`7877add8a640a9d2f237eb149e35440bc8c392ce84fe30a24e16a03b54c3d7d0`.
All 46 GPT pages and all 65 Claude pages were reviewed; the atlas and the five
GPT graphite plates received original-resolution checks; the GPT web
equivalence and independent Catholic sanity review pass; and the installed
provider PDFs remain distinct. The current source-first map uses pinned Natural
Earth 5.1.2 and Mapzen Terrain Tiles beneath a project-authored semantic overlay
that distinguishes narrated, inferred, traditional, candidate, regional, and
unknown geography. The Ark and sanctuary captions distinguish commanded or
attested data from unrecoverable form and location.

Content commit `2b9233978bcd8e798467bffaccf699b96031d97a` was pushed to
`origin/main` without rewriting history. GitHub Pages run
[`31957951080`](https://github.com/spincyc/triptych/actions/runs/31957951080)
completed successfully for that exact head. The live
[Mariology catalog](https://mystago.gy/library/mariology.html),
[GPT web reader](https://mystago.gy/web/gpt/theology/mariology/ark-of-the-covenant.html),
[GPT PDF](https://mystago.gy/pdf/gpt/theology/mariology/ark-of-the-covenant.pdf),
and [Claude PDF](https://mystago.gy/pdf/claude/theology/mariology/ark-of-the-covenant.pdf)
each returned HTTP 200. The two deployed PDFs matched the reviewed SHA-256
identities above, and the live catalog contained exactly one shared Ark row
with each distinct provider title and route. All twelve acceptance requirements
pass.

The earlier 42-page GPT artifact `a520adb39130bb3b65a3bd7d92926fbc77126650fdf593d0680fc10bee125843`,
web artifact `3a5e96c2405e1d311acf65ef931a45ebee502e459817f5a744833858ce62d1bc`,
commit `a35dc5cfb82be027256d74c6f2b256f830f1073e`, and Pages run
[`31935618065`](https://github.com/spincyc/triptych/actions/runs/31935618065)
are superseded baseline evidence, not evidence for this correction.

### Corpus browser foundation design

<!-- promised-deliverable: corpus-browser-foundation-design-2026-08-08 -->

**Candidate on isolated branch `ux/foundation` from exact base
`c27d6915319785686d1df6a1401a489aa9921f6f`; no production or PDF change is
authorized and independent acceptance remains open.** A0-A4 inventory the
complete public surface, synthesize checked
scholarly-interface research, establish the site-wide corpus-browser vision,
define one visual system with Reader/Catalogue/Instrument archetypes, and
specify shared navigation, bounded synthetic Jump behavior, typed contextual
navigation, and shell behavior. Production global typed search remains J0-J2.
The accepted Liturgical Instrument remains the liturgy-specific reference and
is not reopened. `PROJECT-WORK.md` and `promised-deliverables.toml` remain the
fail-closed operational authorities; durable design and execution detail lives
in `guidance/corpus-browser-vision.md`, `guidance/corpus-browser-roadmap.md`, and
`build/agent-continuity/corpus-browser-foundation.md`. One standard external-
review ZIP will present the committed candidate; creating it will not mark the
foundation accepted or authorize production implementation, integration, or
public cutover.

### Corpus browser Wave 1 real-data design

<!-- promised-deliverable: corpus-browser-wave-1-design-2026-08-08 -->

**Complete as a Wave 1 visual and product-design deliverable; production
remains unimplemented.** Independent review of Wave 1 at exact head
`e42b9287485a5a6d18ad8a528ab0f0f3f0024ff9` accepted C0 Home, C1
Publications, D0 Reader, and E0 Catena as design contracts. Independent review
of the corrected checkpoint at exact head
`ecbd93a0575c4b890cc814af7cd20d01f5af7beb` then recorded **F0 Source
Library — ACCEPT** and **Shared non-Liturgy shell — ACCEPT**, closing the two
remaining design-review gates. Accessibility and resilience remain accepted
production requirements with production proof outstanding. Browser print
remains accepted only as a non-canonical fallback.

The original branch started from exact `origin/main` base
`c27d6915319785686d1df6a1401a489aa9921f6f`. Its task-specific dispatch
superseded the former integration-branch precursor, so no
`corpus/foundation-integration` ancestry is claimed. Accepted knowledge and
artifacts were carried selectively from Codex foundation SHA
`3b5938a0dba88831763ec09c762ae1572007a27e` and Claude foundation SHA
`af2c9613ccda48679face4e43f59c002f93056ef`.

The durable design authority is
[`guidance/corpus-browser-vision.md`](guidance/corpus-browser-vision.md); the
execution, evidence, and disposition register is
[`guidance/corpus-browser-roadmap.md`](guidance/corpus-browser-roadmap.md).

C0, C1, D0, and E0 were not reopened by the correction checkpoint. The
accepted F0 contract distinguishes Work/Edition ownership from the
Artifact/Segment relation controlling Passage text. For the reviewed
one-Passage Edition, it retains the selector, exact `Passage 1 of 1`, and
rights, provenance, and inspection-scope truth while omitting impossible
Previous and Next actions. The accepted wide shell has exactly one
current-location signal, no duplicate wide domain identity, and Browse as a
bounded destination control distinct from Jump; the compact shell preserves
domain identity, Menu, Jump, target sizing, and no document-level overflow at
393 and 320 CSS pixels. The correction changed no
production behavior, protected Liturgy, canonical PDF, production route or
hash contract, release binding, public mapping, or deployment state.

**Evidence and reviewed handoff.** The immutable reviewed record is
`build/agent-handoffs/20260809T000346Z-corpus-wave-1-design-review/`, with its
matching one-root ZIP. Its browser report covers 83 real-route cases and 1,979
assertions: 1,917 pass, 62 disclosed inherited findings are non-gating, and no
gate fails. It contains 83 main captures, all 25 required before/after pairs,
one 236-page Reader print PDF, and all 236 page rasters. The bounded correction
is complete at design/test head
`c66c143643ff75a6cd54afdbe1fcd6eac0aca1b6`. Its full capture run covers 85
real-route cases and 2,296 assertions with zero gating failures. The 64
non-gating findings are 52 inherited nested-`main` findings, eight before-state
useful-content findings, two before-only narrow-overflow findings, and two
inherited Reader no-JavaScript overlay limitations. The correction package
`20260809T014145Z-corpus-wave-1-review-fixes` is superseded for handoff-protocol
defects. Independent review of the fresh immutable package
`build/agent-handoffs/20260809T021953Z-corpus-wave-1-review-fixes/` and its
matching ZIP at packaged head `ecbd93a0575c4b890cc814af7cd20d01f5af7beb`;
recorded the F0 and shared-shell ACCEPT dispositions. The ZIP SHA-256 is
`d5fde51b14f143db05f762178896284d7768c0b2a11fc222fc2b32da63e22062`.
The exact reviewed-base-to-head range has zero changes under protected
`src/web/browser/liturgy/` and `pdf/`.

The following findings are non-blocking only for these design dispositions;
none is waived, satisfied, or reassigned by acceptance. The inherited
nested-`main` defect remains a production blocker. Reader table-cell reflow and
full no-JavaScript behavior remain production obligations. Comprehensive
Menu/Browse destination-activation tests remain an implementation and
hardening obligation. The prototype stylesheet used 8,171 of its 8,192-byte
gzip-9 ceiling, so it provides no meaningful implementation headroom or
production CSS budget. The stale Fortescue Artifact note remains open and may
be corrected only by its proper source-data authority owner.

For this program, Codex owns product and visual design, correction evidence,
and independent product review. Claude owns production implementation, coding,
and implementation testing on named lanes. Neither role may cross declared
single-owner boundaries or accept, merge, or deploy its own work by implication.

The F0 and shared-shell design-review dependencies are satisfied. F1 Sources is
eligible only for separate owner-authorized production dispatch; final
shared-shell cutover remains blocked on clean foundation plumbing and explicit
cutover authority. E1 Catena may proceed
within its existing independent boundary; Home/Publications/Reader
implementation still requires clean shell ownership. Production implementation
remains owned by the appropriate Claude lanes. This acceptance does not
authorize merging the disposable prototype overlay, merging or pushing
`main`, deployment, public cutover, a protected Liturgy change, or a canonical
PDF change.

### Live Reader — Ritual Flow & Orientation

<!-- promised-deliverable: liturgy-reader-live-ritual-flow-2026-08-07 -->

**In progress as a new production refinement phase against the independently
accepted live canonical Day and Propers readers.** The completed migration and
same-path cutover are not reopened. This phase protects the accepted first
viewport and Instrument foundation while improving sustained-reading
orientation, making Contents a current-place map, and restoring hierarchy
between principal ritual action and source-owned rubric, provenance, or
conditional/reference material.

The implementation may expose existing semantic and renderer state through
narrow shared presentation hooks. It may not manufacture liturgical
applicability, locality, selection, source, translation, or content. Search,
Study, Compare, print redesign, public-navigation redesign, candidate/oracle
cleanup, source/translation/recension expansion, and a new visual direction
remain separate and unauthorized. Exact baseline, decisions, checkpoints,
Pages runs, and the independent-review stopping point live in
`build/agent-continuity/liturgy-reader-visual-plan.md`.

### Liturgical Instrument public cutover

<!-- promised-deliverable: liturgy-reader-instrument-public-cutover-plan-2026-08-06 -->

**Complete; the canonical Day and Propers URLs serve the independently accepted
Liturgical Instrument, public navigation is unchanged, and retained candidate
and oracle cleanup is deferred.** Planning began from synchronized accepted-
integration boundary `7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`. It inventoried
the canonical `liturgy/day.html` and `liturgy/index.html` contracts against
the accepted `liturgy/day-reader.html` and `liturgy/propers-reader.html`
implementations, selected same-path promotion as the smallest reversible
mechanism, made the disclosed date-dependent Day gate deterministic without a
product change, and produced exact patch, rollback, acceptance, deployment,
and cache-window procedures.

Independent review accepted source-level same-path promotion behind the
unchanged canonical filenames, the rollback and static-hosting model, the
canonical-route and visual-oracle gates, and the deterministic Day fixture. It
also fixed the compatibility decisions: Roman 1962 is the intentional empty-Day
default; `why=1` and every held territorial branch are preserved; Propers uses
stable `cycle`, `alternative`, and `translation-witness` keys; retained
candidates are source-static noindex; visible controller wording is route-
neutral; and counterpart/context navigation belongs in Details without a fifth
primary action. Compatibility implementation
`3f3949617a04ffa68a1070058d0f7bc5ac74dc93` closes those contracts on the
authorized candidate/shared seams. Pages run `31148986910` succeeded for that
exact commit. Day passes 40/40, Propers 32/32, the shared shell 18/18, and
governed visual assertions 24/24 over 113 captures. Production integration,
compatibility closure, and their durable handoffs are independently accepted
and complete.

Planning checkpoint `c7124de25` records the route, state, navigation, static-
hosting, cache, mechanism, rollback, and execution-gate maps. Test-only commit
`5e1b82b51` proves and removes the disclosed wall-clock dependency while
keeping the first-visit URL empty. The obsolete first patch was superseded
after gate repair by the accepted 19-path patch. Its prospective 230/230 focused
Python, 40/40 Day, 32/32 Propers, 18/18 shared-shell, and 24/24 governed
Instrument gates were repeated successfully in the promoted real tree before
commit. The planning package remains at
`build/agent-handoffs/20260806T212148Z-liturgy-reader-instrument-public-cutover-plan/`
and the removed compatibility package remains recoverable from its historical
introduction commit `e69d91ffff5823dc2970f867f1be8c9eb5b6363b`.

Independent post-deployment review passed all nine final questions and accepts
the public cutover as complete. Exact cutover SHA
`9b5f21c0ca26bf02af03d207ddd2617021e16fb3` owns qualifying successful Pages
run `31175722949`. Immediate live verification passed 936/936 across 36
original-pixel states; ordinary-cache verification passed 216/216 after 613
seconds without mixed-generation behavior. The removed immutable execution
handoff remains recoverable from historical introduction commit
`1d60b49bcf2a46e5ee43d6326af3e13a43265b72`; its ZIP SHA-256 was
`06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410`.
Canonical Day and Propers now serve the accepted Instrument without redirects.
Public navigation was not redesigned; retained candidate and oracle routes
remain intact and nonindexable, and cleanup is deferred and unauthorized. The
governed full gate remains non-green only at the unrelated stored-example
transcript replay; no transcript was recaptured or blessed.

### Liturgical Instrument production integration

<!-- promised-deliverable: liturgy-reader-instrument-production-integration-2026-08-06 -->

**Complete; production integration is independently accepted and its exact
reviewed handoff is durably archived in Git history rather than the current
tree. The separately reviewed public cutover is also complete;
public-navigation redesign remains outside both phases.**
Independent Round 1 accepted the
Liturgical Instrument visual foundation and all seven correction dispositions.
Production integration begins from `b3ae6bddaab631661d342380f61365d851be160c`
through four bounded units: PI-A inventories the accepted hooks and selects the
smallest shared presentation seam; PI-B integrates the shell and Day
Read/Missal presentation; PI-C proves Propers Read/Browse parity; and PI-D
captures the full parity matrix, runs the governed checks, and assembles an
immutable integration-review candidate.

The completed inventory selects a new last-loaded, candidate-scoped
`src/web/browser/liturgy/reader-instrument.css` layer. This keeps public-loaded
`day-missal.css` unchanged and preserves `reader-shell.js`, the M1 state and
adapter owners, production renderers, Ordinary seating, invalid-state failure,
semantic-location restoration, focus, race ownership, and the four one-step
actions. Stable masthead and action-label hooks are added to the two production
candidate HTML files. Only generation-safe presentation composition may touch
the Day or Propers adapters: the authoritative Day commit exposes its current
mode as a styling attribute, and renderer-owned absence nodes may be grouped or
moved without replacing their text or semantics. The accepted comparison
prototype remains unmodified and available as the parity oracle. That seam is
now implemented in both unlinked candidates. The extended Chromium harness
passes 19/19 assertions over 100 captures and includes 23 exact
prototype/production pairs covering Read, Missal, partial coverage,
postconciliar coverage, Propers, all open surfaces, deep scroll, 200% text,
forced colors, reduced motion, and keyboard focus. The accepted 768×1024
636-pixel/~75-character measure is exact; production mobile Missal principal
text is 3.43 pixels earlier than the accepted oracle and otherwise retains the
same 351-pixel plane and action geometry.

Successful deployed correction parity remains Pages run `31109086658` for
`c388ab42dfc4f5c7d49abc71596d6bb511af5742`. Later runs
`31110517661`, `31113461987`, and `31114653517` each passed repository-owned
build/upload work and then failed at GitHub deployment polling; none is claimed
as successful. The production-integration deliverable remains open until its
own evidence, deployment record, and independent integration disposition are
complete. The implementation checkpoint is not represented as deployed until
its own push has a successful Pages result and direct asset verification.
Implementation commit `3cd46072b164ff39b00639bb67ad6b8943a255dc` is pushed
to `origin/main`. Its clean-tree full gate reached only the governed unrelated
example-replay divergence: 200 examples, 188 replayed, 23 divergent, 35 known
stale, 6 never run, and 6 unrunnable here. It exits 2 and is not represented as
green. As of 2026-08-06T18:04:26Z, GitHub had not materialized the automatic
Pages run for this push in the Actions API; this is recorded as a pending
workflow event, not a deployment success or failure.
Continuity checkpoint `e35f81c1e67c744aead0e4eaa73e079516751e66` is also
pushed. As of 2026-08-06T18:08:35Z GitHub likewise had no Actions record for
that head. Direct deployed Day and Propers candidates remain HTTP 200 at the
prior artifact, which does not contain `reader-instrument.css`; deployed
integration parity therefore remains explicitly open.
GitHub later materialized automatic run `31125352169` for implementation commit
`3cd46072b164ff39b00639bb67ad6b8943a255dc`, but at
2026-08-06T18:27:03Z it had remained queued for more than 15 minutes with no
runner or repository step started. This is a queued external-state result, not
a successful or failed deployment; deployed parity remains open.
The next delayed automatic run, `31125898045`, succeeded for exact intended
production commit `5444d89fc9b379a1babef5b2220323fe1508b2b3` at
2026-08-06T18:29:55Z. Every repository build, verification, upload, and deploy
step passed. Direct Day, Propers, and both accepted oracle routes return HTTP
200; Day/Propers reference the Instrument stylesheet, the oracle routes remain
noindex, and deployed Instrument CSS, Day/Propers JavaScript, and accepted
oracle CSS/JavaScript byte-match source. Deployed production-integration parity
is complete. The deliverable remains a candidate solely for independent
integration review; public navigation and cutover remain unauthorized.

Independent production-integration review passed all six requested questions:
Day parity, Propers parity with canonical Browse retained, responsive shell and
accessibility behavior, reading and ritual geometry, frozen behavioral/source
ownership, and final integration disposition. No product, visual, evidence,
harness, or deployment correction was requested. The only closeout finding was
that the exact reviewed handoff remained ignored locally.

Under the review's path-bounded force-add authority, archival commit
`8c6e1270f692ca4136f2f6a60002bacd3af0440c` pushes the byte-identical reviewed
directory and ZIP. All 216 manifest entries verify, the archive has one
top-level directory, and its SHA-256 remains
`ebf0361309ac33b4580cbb535e4bbd3eabd144756e6c078aa140e716c748f05f`.
The canonical continuity file carries the complete review and Codex response.
Production integration and durable handoff closeout are therefore complete.
At that integration boundary the Day browser remained 33/34 only at its
date-dependent expectation; the subsequent deterministic cutover fixture and
canonical execution pass 40/40. The full gate remains non-green only at
unrelated example transcript divergence. The separately reviewed public
cutover is now accepted and complete; public-navigation redesign was not part
of it.

### Liturgical Instrument visual correction accepted

<!-- promised-deliverable: liturgy-reader-instrument-correction-2026-08-05 -->

**Complete; independent Round 1 acceptance authorized the now-complete
production integration, but did not itself authorize navigation or cutover.**
Liturgical Instrument is the
accepted production visual foundation. Quiet Folio and Contemporary Reader
remain frozen comparison references, and the accepted visual and behavioral
seams are not reopened absent a concrete production-integration conflict.

The bounded correction owns seven findings: integrate the persistent controls
with the reading composition; advance the first principal Missal text; remove
the empty Read gutter; constrain the 768-pixel portrait measure; subordinate
partial and postconciliar coverage warnings to available text; replace or
simplify the provisional masthead mark and progress treatment; and finish
mobile ritual spacing and narrow division-title wrapping. The canonical plan,
review mailbox, measurements, checkpoint record, and resume state are tracked
at `build/agent-continuity/liturgy-reader-visual-plan.md` under this task's
explicit build-tree exception. Work units A–C now implement and measure the
bounded visual corrections: one 39.75rem Read axis, earlier Missal action,
integrated rail/dock, authored masthead, consolidated warnings, tighter ritual
rhythm, and deliberate 320-pixel wrapping. Work unit D now supplies the full
matrix, measured before/after package, honest governed-check record, verified
Pages deployment, and an immutable tracked handoff now retained only in
historical introduction commit
`50288ddf9759f56e8a25e4907d8de25e27e25e8f`.
Independent review round 1 passed six of seven original findings and confirmed
the direction, typography, ritual grid, warnings, masthead, and Ordinary/Proper
composition. It retained the original shell blocker only at 1024×768 and added
the related 200%-text mid-word label reflow blocker. The bounded follow-up now
uses the opaque square edge dock immediately below the 72rem rail breakpoint
and a labeled 2×2 dock only at extreme root-font reflow. The 54-capture run
passes 15/15 assertions, including end-content reserve, whole labels, accessible
names, target size, and overflow. Correction commit
`ab89758e3f3ee165e0141e3605be88051450134b`
is pushed. Its first Pages run passed every build/verification step but timed
out while GitHub held the deployment queued, so deployed corrected-asset parity
remains open and is not claimed. A second automatic run for continuity
checkpoint `c6b7f7f0a79468cfa1a503235044c92bd88c27b2` again built and uploaded the
verified artifact, then timed out only in deploy-pages polling; the durable
continuity record owns both exact stops. A third automatic run again passed all
repository-owned build/upload work and was canceled only when the job reached
its 15-minute ceiling during deploy polling. The following immutable-handoff
push succeeded as Pages run `31109086658`; direct Day/Propers routes are HTTP
200/noindex and deployed CSS/JS byte-match source. The removed final narrow
immutable re-review handoff remains recoverable from historical introduction
commit `4daf7d8a1e1c509edb81a738cc71223170bbbd2d`.
Independent Round 1 acceptance passed shell continuity, 200% labeled reflow,
and absence of accepted-geometry regressions. It independently verified the
ZIP, all 109 manifest entries, candidate/source CSS parity, and all corrected
original-pixel screenshots. Production integration may now begin through the
shared presentation seam; it must stop for independent integration review
before any separately authorized public cutover. Pages run `31110517661` for
post-deployment evidence commit `4daf7d8a1e1c509edb81a738cc71223170bbbd2d`
failed at deployment polling and is not represented as successful; successful
deployed parity remains owned by run `31109086658` for
`c388ab42dfc4f5c7d49abc71596d6bb511af5742`.
The acceptance-record push at `1608f0ee0ee61df956247072a91647147548c5ad`
passed every repository-owned Pages build/upload step, then run `31113461987`
failed after 600 seconds of `deployment_in_progress` polling. Direct prototype
routes remain HTTP 200/noindex and their deployed CSS/JS still byte-match the
accepted source; the new run is not represented as successful.

Accepted M1–M3 and W3 state, assembly, renderers, Ordinary seating, failure,
location, focus, race, action-reachability, and isolation behavior remain
binding. This completed correction does not add Study, Compare, search, Propers
Missal, sources, editions, recensions, translations, or public links, and it
does not change `liturgy/day.html` or `liturgy/index.html`.

### Liturgy reader visual-reset direction candidate

<!-- promised-deliverable: liturgy-reader-visual-reset-candidate-2026-08-05 -->

**Complete as a direction-selection study; Liturgical Instrument selected.**
The completed M1–M3 and W3 records remain authoritative for state,
production assembly and rendering reuse, fail-closed behavior, focus and
semantic-location restoration, responsive access, and render-race ownership.
They were never a finding that the beige card, enlarged mobile-style command
bar, improvised glyphs, typography, spacing, or desktop composition constituted
a finished or world-class visual reader.

This distinct visual-design work item compared Quiet Folio, Liturgical
Instrument, and Contemporary Reader over one shared semantic DOM and interaction
foundation. It uses real production Day Read/Missal and Propers Read content at
unlinked, noindex prototype routes, while preserving the accepted state,
calendar, Ordinary seating, Proper rendering, source, and coverage boundaries.
Its external review selected Liturgical Instrument. The work does not reopen
the completed Day Missal engineering deliverable, alter public Day or Propers,
start Study/Compare/search, or authorize public cutover.

The visual-reset candidate was implemented and independently reviewed, with
**Liturgical Instrument selected as the production visual foundation**. Quiet
Folio is the calmest editorial leaf; Liturgical Instrument adds an edition-neutral
ritual cue grid, disciplined divisions, and a speaker/action gutter for actual
following; Contemporary Reader supplies the most compact application chrome
and polished title-led Propers Browse flow. All three are query-selected
presentations over the same HTML, SVG icon set, shared shell controller, and
accepted Day/Propers production adapters. The selection favors Instrument's
continuous ritual legibility. Folio and Reader remain frozen comparison
references rather than ingredients for a merged compromise. The review also
found seven bounded visual blockers, now owned by
`liturgy-reader-instrument-correction-2026-08-05`; selection does not make the
foundation world-class or authorize production integration.

The current evidence contains 52 same-run comparison captures at the required
desktop, tablet, mobile, enlarged-text, forced-color, reduced-motion, keyboard,
deep-scroll, surface, partial-coverage, and before/after states. Twelve focused
Chromium assertions pass with no console, failed-request, HTTP, overflow, or
unnamed-interactive-node result; a 26-page PDF is retained only as a print smoke
check, not a print redesign. Exact hashes prove the public Day and Propers
routes, both accepted candidates, shared shell, M1 state seams, production
seating, and accepted adapters unchanged. The implementation is this candidate
commit; its immutable visual-review handoff was created after the validated
push. The direction-selection decision is complete. Corrected visual review,
production-integration execution, and every public-cutover decision remain
open under the separate correction deliverable above.

### Liturgy Day Missal-mode W3 integration accepted

<!-- promised-deliverable: liturgy-day-missal-w3-candidate-2026-08-05 -->

This task extends the accepted internal Day reader at
`liturgy/day-reader.html` with the next bounded W3/M3 production-integration
slice: Read remains the default appointed-Propers view, and Missal presents the
continuous production Ordinary with those same propers seated at their actual
semantic locations. The candidate must reuse the accepted M1 Day state,
production calendar assembly, Ordinary data and renderer, Ordinary seating,
and shared Proper renderer. It may not create a second liturgical sequence,
renderer, seating engine, event-order engine, URL parser, or public route.

**Accepted** — the internal W3 Day Missal-mode integration has passing
implementation and independent external-review evidence. Its contract includes
Roman 1962 and postconciliar parity,
fail-closed Ordinary language and Eucharistic Prayer handling, explicit
coverage and absence,
semantic-location preservation across Read/Missal and history transitions,
race ownership, responsive and accessible interaction, continuous Missal
print, performance measurement, and production isolation. Study, Compare,
Propers Missal mode, search, new recension or source coverage, public route
cutover, and redesign of the accepted shell or complete print system remain
out of scope.

The implementation base is
`c4c071d6ba962524487bc8f4c6a4b781981851c7`. The initial candidate, two bounded
corrections, three immutable handoffs, and their successive review dispositions
remain recorded below as the durable audit trail. This acceptance does not
amend the accepted M1, M2, M3, or Propers Read records.

External review of implementation
`a1221755d4fac2a6b9a009a91b99cd1da82eee9e` and immutable handoff
`20260805T145914Z-day-missal-mode-integration` returned **changes requested**.
It passed the production-renderer, seating, edition, option-validity,
ergonomics, isolation, and scope boundaries, but identified three bounded
acceptance blockers: non-ready outcomes can retain history-dependent mode
chrome; an inline Eucharistic Prayer change replaces the focused radio without
restoring its semantic equivalent; and direct-load evidence can observe an old
ready flag before the new document's render commits. Correction work is limited
to deterministic outcome presentation, inline-option focus restoration, and
generation-safe browser assertions and replacement captures. The candidate and
its independent external-review requirement remain open; no acceptance,
closeout, public cutover, or deployment is authorized by the correction work.

The bounded correction is now implemented and locally proven, but remains
**pending independent correction review**. Every render outcome commits one
mode presentation (including a neutral, unchecked presentation for invalid
`ordinary` state); invalid, deferred, unresolved/territorial, and unrenderable
outcomes carry distinct diagnostics; and stale navigation, location, focus,
metadata, and selection state is cleared before an outcome commits. Keyboard
changes among the postconciliar Eucharistic Prayers restore focus to the newly
rendered checked radio without losing the semantic reading location. The
browser harness now distinguishes fresh documents by a unique non-semantic
query nonce and document token, and same-document transitions by an exact hash
and a greater committed render generation, followed by the UI's animation-frame
boundary. The complete browser and print evidence was regenerated with that
harness. These results resolve the three correction requirements for re-review;
they do not accept or close the candidate.

External review of correction
`ce5fce8364d24156e41c444c43673e7de31555d8` and immutable handoff
`20260805T183500Z-day-missal-mode-corrections` returned a second, narrowly
bounded **changes requested** disposition. The substantive product corrections
passed review: deterministic outcome chrome, neutral invalid-Ordinary state,
distinct failure classes, inline-option focus restoration, generation-safe
document navigation, and production isolation remain accepted correction
evidence. Acceptance is still blocked because the Chromium harness waited only
two animation frames while inherited smooth scrolling could remain in flight,
and because duplicate `ordinary` keys were not exercised directly in Chromium.
The evidence-settlement correction is limited to animation-frame scroll/target
stability, settled default- and reduced-motion Eucharistic Prayer focus proof,
both duplicate-key orderings from fresh and transitioned states, wholly
regenerated evidence, and a new independent handoff. Product reader and shared
shell behavior remain unchanged unless settled testing proves a real defect.
The candidate, completion count, and external-review requirement remain open.

The evidence-settlement micro-correction is now implemented and locally
proven, but remains **pending independent external review**. Committed-render
synchronization still requires exact document tokens and generations; a
separate animation-frame loop now requires five stable scroll/target/focus
frames, viewport intersection, cleared pending navigation, and a bounded
diagnostic timeout before assertion or capture. Default-motion keyboard changes
through EP I, III, IV, and II and a separate reduced-motion change preserve the
settled semantic event and checked-radio focus. The stabilized test exposed one
local Day-adapter defect: the correctly focused checked radio could settle above
the viewport. The adapter now aligns that inline option group deterministically
after semantic restoration, leaving the shared shell and global scrolling rules
unchanged. Both `ordinary=0&ordinary=1` and `ordinary=1&ordinary=0` now produce
neutral, unchecked mode chrome on fresh loads and transitions from Read and
Missal. All browser and print evidence was regenerated; the public routes,
Propers candidate, shared shell, M1 seams, seating, and production data remain
unchanged. These results satisfy the bounded proof requirement for re-review;
they do not accept, close, deploy, or cut over the candidate.

Independent external review now **accepts and closes this internal W3 Day
Missal-mode slice** at micro-correction
`86a9816c1bffdcbdd09469f5f8d005c666a8045e`; every blocking review question is
resolved and no further handoff is required. The complete reviewed sequence is
candidate `a1221755d4fac2a6b9a009a91b99cd1da82eee9e`, first correction
`ce5fce8364d24156e41c444c43673e7de31555d8`, and the accepted micro-correction
above, with immutable handoffs
`20260805T145914Z-day-missal-mode-integration`,
`20260805T183500Z-day-missal-mode-corrections`, and
`20260805T201722Z-day-missal-mode-evidence-corrections`. Acceptance covers
reuse of the production Ordinary presenter, Proper renderer, M1 event stream,
and single seating path; Roman 1962 and postconciliar structures;
deterministic fail-closed state; semantic location, history, and render-race
ownership; settled inline Eucharistic Prayer keyboard focus; responsive,
accessibility, performance, and print evidence; and production isolation. It
does not authorize public-route cutover, public links, Propers Missal mode,
Study, Compare, search, source or recension expansion, or print redesign.

### Liturgy Propers Read W3 integration accepted

<!-- promised-deliverable: liturgy-propers-read-w3-candidate-2026-08-04 -->

**Accepted** — the W3 Propers Read integration enters the same production
reader shell as the accepted Day candidate, preserves current valid formulary
semantics through the M1 Propers state and production Proper renderer, leaves
missing identity unresolved, fails closed on invalid state, preserves cycles
and alternatives independently, requests translation witnesses only when
formulary-specific translated material requires a choice, and remains isolated
from the public Day and Propers routes.

External review first requested bounded Browse witness, Browse-race, tracking,
and handoff corrections from candidate
`b0b1e5b63ba4a1d389b53276fa0bf9944c0ee909` and handoff
`20260804T212821Z-propers-reader-shell-integration`. It then accepted correction
`1e4587dfe04a11c18e996a16f7fbbdb54bc744a4` and immutable handoff
`20260804T225215Z-propers-reader-shell-corrections` after manifest verification.
The reviewed evidence records 84 focused M1/shell/Day/Propers tests, 90
public-alpha/gallery tests, and respectively 27, 25, and 18 Chromium assertions
for Propers, Day, and the shared shell. The exact shared-shell hashes are
`bf1c062453f8fcfd5a68c1fe30e31aca89ea1a3c8adeef9a5525d8081ae8c707`
for `reader-shell.js` and
`e7195cd86ed4fc4a8455e97369702239eb22d709a13d3d8462d7759c01fe814a`
for `reader-shell.css`.

Production-isolation evidence confirms that public Day and Propers, the
accepted Day candidate, navigation and selectors, M1 semantics, production
liturgical and generated data, and public URL behavior remain unchanged. The
approved example baseline remains the same 23 unrelated pre-existing records
and the same two promised-deliverable commands; acceptance changes only the
candidate count from 18 tracked, 12 complete to 18 tracked, 13 complete.
Public cutover, Missal, Study, Compare, search, and recension expansion remain
deferred. Excess cycle-choice print whitespace remains non-blocking debt for a
later print-refinement workstream.

### Liturgy Day reader-shell M3 accepted

<!-- promised-deliverable: liturgy-day-reader-shell-m3-candidate-2026-08-04 -->

The first W3 integration slice extracts the accepted quiet persistent reader
shell into a reusable production foundation and connects an unlinked, noindex
Day Read-mode candidate to the existing production assembly and rendering path
through the accepted M1 reader-state boundary. The candidate preserves
Read-compatible legacy URL meaning, fails closed on invalid explicit state,
and discloses later-mode state with an equivalent link to the unchanged live
Day route rather than silently dropping or partially rendering it.

This was an **M3 candidate pending external review**, not a production cutover.
The live Day and Propers routes, public navigation and selectors, M1 semantics,
liturgical and calendar data, and generated public data remain outside the
implementation boundary. Missal, Study, Compare, Propers integration, search,
and public release remain deferred.

The candidate is implemented at the unlinked `liturgy/day-reader.html` build
route. `reader-shell.js` and `reader-shell.css` contain only the accepted
persistent action bar, modal lifecycle, focus and scroll restoration, semantic
Contents tracking, responsive sheets, safe-area behavior, and print removal.
The separate Day adapter parses and validates M1 state, calls the existing
calendar assembly and M1 Day adapter, and renders the selected real production
Proper with the existing shared renderer. It supports date, missal, Bible,
oration language, and readable-formulary state; it preserves later-mode state
and links it intact to `day.html`, and it fails closed on invalid explicit
values.

Focused static, M1, current-route, Ordinary, public-alpha, and real-Chromium
checks cover both production-backed M1 Day fixtures, a readable displaced
formulary, typed partial coverage, invalid and deferred state, all four modal
surfaces, 320-pixel and 200% reflow, accessibility, deep-scroll reachability,
Back, lazy Details, print, and live-route parity. The immutable external-review
handoff is `20260804T154620Z-day-reader-shell-integration`. M3 remains a
candidate until external review accepts it.

External review accepted the W3 architecture and requested three bounded
corrections before M3 acceptance. The correction distinguishes inactive latent
Ordinary, rubric, and why preferences from active later-mode requests; clears
all selection-specific state before every render attempt so rejected,
unresolved, deferred, or failed navigation cannot expose an earlier result;
restores exact weekday presentation from the assembly model; and keeps raw
source-hook coordinates out of reader-facing Details. The compact correction
handoff is
`20260804T173010Z-day-reader-shell-integration-corrections`. M3 remains a
candidate pending correction review; the live Day and Propers routes remain
unchanged.

M3 is now **accepted**. Accepted — the production Day Read candidate reuses
the existing assembly and Proper renderer behind the shared persistent shell,
preserves Read-compatible legacy state, explicitly defers later-mode state,
fails closed across invalid and superseded asynchronous transitions, and
remains isolated from the live Day and Propers routes. The final serial-token
micro-fix is `c604edb8a1fffb1e5c0981798800ecb801258e7c`; deterministic Chromium
tests release delayed valid, malformed, invalid-destination, and history
requests only after the newer outcome is ready, then prove that identity,
Proper text, Contents, Date, Details, semantic state, and render counters do
not change.

Acceptance evidence comprises original candidate
`45a6b76249e015f68830495ca2971e9dbc4a4e14`, correction
`d0872545ccc92106cb457b448f37201381c5bb2d`, the final micro-fix above,
handoffs `20260804T154620Z-day-reader-shell-integration` and
`20260804T173010Z-day-reader-shell-integration-corrections`, the original W3
changes-requested review, and the W3 conditional-acceptance disposition. M3
acceptance does not replace or redirect live Day, integrate Propers, expose
public navigation, begin later modes, authorize public cutover, or begin the
1956–1960 recension.

### Liturgy reader-shell M2 accepted

<!-- promised-deliverable: liturgy-reader-shell-m2-candidate-2026-08-03 -->

The first W2 milestone is a visible, interactive, responsive shell prototype,
not a production-route integration. It will live in an unlinked nested
`src/web/browser/liturgy/prototypes/reader-shell/` route, which the existing
top-level-only public browser copier excludes. The candidate must reuse the
current Proper renderer, keep Day and Propers as distinct entrances to one
shared shell, compare quiet persistent and scroll-reveal reachability, and
measure wide, intermediate, mobile, 320-pixel reflow, accessibility,
performance, and print behavior. It may use clearly marked M1 contract-only
fixtures for Compare and unresolved-choice layout, but it must not implement
later semantic engines or change public generated data.

The candidate now has one shared shell, persistent and scroll-reveal variants,
real-renderer Day and Propers states, layout-only later-mode fixtures, semantic
Contents, a coherent Study apparatus, 94 responsive review captures, a tagged
four-page print review, and focused static and real-browser coverage. The
measured decision recommends the quiet persistent shell: every global action
remains one activation away at deep scroll while the shell occupies about
58–59 CSS pixels and causes no measured layout shift. The immutable handoff is
`20260804T101952Z-liturgy-reader-shell-prototype`.

External review of candidate `68becc59b396aca830c233b88ec74991563603d1`
in handoff `20260804T101952Z-liturgy-reader-shell-prototype` accepted that
persistent-shell direction and the shared Day/Propers model, but its *M2
prototype changes-requested disposition* required three bounded corrections.
Correction `75234e72c402f0b25a681fbe074da70d895f7274`, reviewed through handoff
`20260804T142747Z-liturgy-reader-shell-corrections`, removed complete-state
diagnostic noise, eliminated auxiliary-surface overflow and raw
machine-shaped Study output, and distinguished temporary Details from pinned
wide-desktop Study and reversible mobile Study sheets.

Accepted on 4 August 2026. The *M2 responsive reader-shell acceptance and
closeout disposition* records: **Accepted — the quiet persistent reader shell
is the M2 direction. Complete Read states are free of diagnostic noise, all
auxiliary surfaces reflow without internal horizontal scrolling, and
temporary Details is distinct from wide-desktop pinned Study and mobile Study
sheets. Production Day and Propers routes remain unchanged.** Focused shell,
M1, current-route, public-alpha, Chromium, print, syntax, registry, and
whitespace checks passed. The repository example comparison preserves the 23
pre-existing divergences and changes only the same two promised-deliverable
rows from `16 tracked, 10 complete` to `16 tracked, 11 complete`; no transcript
was modified or recaptured. Scroll-reveal remains prototype evidence only.
M2 acceptance does not start M3, W3, W4, W5, or production integration, and it
does not change M1 semantics, current URLs, calendar or liturgical data,
search, semantic comparison, or recension coverage.

### Liturgy reader-state M1 accepted

<!-- promised-deliverable: liturgy-reader-state-m1-2026-08-03 -->

The first W1/W9 integration slice defines one versioned, DOM-free semantic
reader-state and legacy-URL contract for the distinct Day and Propers
entrances. Production-backed and explicitly non-public synthetic fixtures hold
identity, calendar result, semantic event order, Proper and Ordinary seating,
text selection, provenance, typed coverage and absence, unresolved choices,
and Compare anchors across Day, Propers, and `mass-today --expanded` without a
second liturgical engine or a visible production change.

Accepted on 3 August 2026. The implementation at
`259573d393cd6a6bac09fc751ac1d14ec9477853`, the reviewed cycle and validation
correction at `c6b8070ae76e75153448895a19a0b916c18806ea`, and the final
property-presence micro-fix at `c1a590f5854215d68d167d9040e188f41762663e`
preserve Propers cycle alternatives and make explicit `sourceHooks` fail
closed unless they are arrays. The external review dispositions *M1 liturgy
reader-state contract*, *M1 reader-state corrections*, and *M1 acceptance
closeout count delta* accepted the resulting contract; the focused suite
passed all 38 tests. The full repository gate remains red only at the approved
23-entry example baseline and the same two promised-deliverable captures, whose
sole authorized closeout change is `15 tracked, 9 complete` to
`15 tracked, 10 complete`. No transcript was recaptured. The deployed Day and
Propers routes still do not load either M1 module, and this acceptance does not
begin W2, W3, or W7 or integrate visible reader behavior.

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

- 2026-08-10: **Foundation integration.** The accepted corpus foundation
  landed on `main` from a fresh checkout: `ux/foundation`,
  `impl/foundation-hardening` (with `impl/foundation`), and the six design
  documents of `ux/corpus-wave-1-review-fixes` (with `ux/corpus-wave-1`) were
  merged and semantically reconciled against the six newer `main` bug-fix
  commits; the Wave 1 prototype overlay stayed on its branches by the
  acceptance's own terms; release bindings were regenerated for the seven
  changed browser files. `impl/shell-plumbing` and `impl/catena-wave-1`
  remain deliberately unintegrated pending their recorded gates. The
  `mystago.gy` cutover is external to the repository and untouched. Details
  under "Foundation integration, 2026-08-10".

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

## Claude Eleventh through Thirteenth Sundays after Pentecost

<!-- promised-deliverable: claude-eleventh-thirteenth-after-pentecost-2026-08-19 -->

On 2026-08-19 the maintainer reopened the closed 1962 temporal propers
boundary for exactly three targets: the Claude guides `51`–`53`, the Eleventh
through Thirteenth Sundays after Pentecost, authored to the current
componentized profile with deep and broad patristic reception research. The
production plan records the boundary decision; this section records the work
authority. The collection remains otherwise closed, and no GPT publication
receives a material change under this work.

For this work the maintainer authorized, in the 2026-08-19 session: full
publication — commit to `main`, the deploy gates
(`make check-deployment-sources`, `make public-site`,
`public-alpha verify --deployment-target github-pages`), and a push to
`origin/main` with its automatic Pages deployment. This supersedes, for this
work only, the 2026-07-27 boundary that reserved integration and push to the
maintainer acting outside a session.

Research verified for these guides enriches the provider-neutral source
library (works, editions, passages, schema-2 bindings) rather than remaining
publication-local; the mass-commentary corpus blocks for `pentecost-11`,
`-12`, and `-13` are the L1 lead lists, and every retained witness is checked
at its work and locus before publication.

**Delivered 2026-08-20.** All three guides are published: Full editions of 34,
36 and 43 pages with Synthesis companions of 17, 19 and 19, each installed from
a page-by-page visual review with installed bytes matching the reviewed build,
and each with an installed web edition. Eleven new passage records entered the
source library (Bede on Luke, the Gelasian and Gregorian sacramentaries in
Wilson's editions, four Bellarmine psalms, four Theodoret psalms) and were
reviewed into their existing families; the classification review resolved the
three new publications to the same eight source strata as the Ninth Sunday.

Three findings are worth recording because they correct or constrain what the
series may claim. The Eleventh Sunday's Introit sings `unanimes`, which is
Cassiodorus's own lemma rather than the Clementine reading — a patristic gloss
that became the chant text — while its Gradual's `ne discedas a me` has no
patristic lemma at all; and its Epistle stops one clause short of the words on
which the whole Augustine–Gregory–Aquinas grace argument turns, which the
commentary reckons with rather than eliding. The Thirteenth Sunday's psalmody
sweep found that `Respice in testamentum tuum` has four rival answers, not one,
and that two of twelve collation divergences are Septuagint or Roman-psalter
transmission rather than chant liberty — which forced an interpretive proposal
resting on the contrary assumption to be rewritten.

Two matters are left for the maintainer rather than settled here. The 1962
proper-guide profile's "full research sequence" sentence and its Reader-Facing
Order list can be read to place the complete appointed formulary differently,
and the three lanes initially resolved it three ways; all three now follow the
`24-tenth-after-pentecost` exemplar, which prints the formulary before the
element-by-element sweep and satisfies both statements, but the profile prose
that invited the divergence is unchanged and should be clarified. Separately,
`TLM text / reference` is a column header in the shared `properstable` macro in
`src/common/preamble.tex`, which `guidance/editorial.md` forbids as apparatus
wording; it appears in every published proper guide and needs one
repository-wide fix rather than a per-leaf fork.

## GPT Eleventh through Thirteenth Sundays after Pentecost

<!-- promised-deliverable: gpt-eleventh-thirteenth-after-pentecost-2026-08-20 -->

On 2026-08-20 the maintainer independently reopened the closed 1962 temporal
propers boundary for the GPT guides `51`–`53`, the Eleventh through Thirteenth
Sundays after Pentecost. The request requires full source-first research, broad
and deep patristic and later saintly reception, Catholic-faithful scholarly
treatment, and enrichment of the provider-neutral shared corpus wherever the
verified research warrants it. The existing Claude editions are source leads
and parallel publications, not prose owners; the GPT editions remain
independently authored and audited.

Each target follows the current componentized profile: one canonical full
research leaf, one mechanically derived synthesis companion, one canonical web
edition, source bindings and reception matrices, installed reviewed PDFs,
catalog links, and provider-qualified release records. This decision changes no
other 1962 identity and authorizes no material revision of a Claude publication.

**Complete.** The three canonical GPT leaves, their mechanically derived
synthesis companions, and their web editions were independently content-audited,
component-checked, built, and visually inspected page by page before the six
reviewed PDFs and three web editions were installed. The source library now
includes reusable checked records for Gregory the Great on Mark 7, Bonaventure
on Wisdom 16, Honorius's relevant whole-proper reception, Anthony of Padua's
critical Latin sermon text, and the official NABRE introductions and notes used
by the guides. Source, inventory, family, catalogue, web, metadata, release, and
deployment gates passed on the integrated tree. GitHub Pages run `32446141366`
then completed successfully, and the live catalog, all three GPT Reader routes,
and all three full-PDF routes returned HTTP 200. The outgoing range made no
material change to a Claude publication; the unrelated local `directions.md`
remained untracked and outside both commits and deployment.

**Reopened on 2026-08-21.** The maintainer rejected the published editions as
an insufficient first pass. The revision must make `Themes and Movement` two
substantively complete pages, replace non-answers in the date/location sheet
with responsibly sourced traditional Catholic dates and attributions, render
patristic and saintly interpretations faithfully within their own theological
grammar rather than organizing the discussion around apology or suspicion,
and greatly deepen both intra-proper exposition and cross-proper development.
That superseded public snapshot remains live until this independently reviewed
substantive revision is redeployed.

**Revised editions deployed on 2026-08-21.** The expanded source-first revision
was independently audited for content, citations, traditional Catholic
chronology and attribution, and every rendered page. The reviewed Full and
Synthesis PDFs and canonical web editions were installed with the page-2
chronology dossier, two complete `Themes and Movement` pages, and detailed
commentary beginning on page 5. Commit `2810f6aba` reached `origin/main`; GitHub
Pages run `32498704134` completed successfully. The live catalog and all three
GPT Reader routes returned the revised timestamps, and all six live PDF routes
matched the reviewed SHA-256 hashes exactly. The unrelated local
`directions.md` and `-.png` remained untracked and outside the commits and
deployment.

## Complete Missal corpus remediation

<!-- promised-deliverable: complete-missal-remediation-2026-08-26 -->

**Completed and deployed on 2026-08-28.** Work began on
`feature/complete-missal` from synchronized base
`2778285849f2973ea89d1cfd5b2751ed4ae58e54`. The maintainer requested one
source-honest program that audits and remediates the postconciliar, Roman 1962,
and Roman pre-1955 Missal data in English and Latin; corrects calendar,
recension, Common, Proper, Ordinary, dialogue, presentation, provenance, and
publication-boundary defects; verifies the complete one-year matrix; commits
and pushes coherent feature work; receives a cold review; then reconciles with
current `main` and advances `origin/main` without rewriting history.

The audit baseline covers every civil date from 2026-08-26 through 2027-08-25:
three calendars by two requested languages by 365 dates, with 2,190 successful
JSON renders and 2,190 successful text renders, no invocation or JSON-parse
failure, and empty standard error. It found ten whole-Mass postconciliar
placeholders and four historical placeholders; seven placeholder
postconciliar Commons and seven structurally incomplete Roman Commons; 89
explicit postconciliar English Proper gaps and 166 historical English Proper
gaps; 391 unselected postconciliar weekday reading or psalm slots; incomplete
postconciliar Eucharistic Prayers; and a historical Ordinary witness that does
not by itself establish a target 1962 or 1920 recension. Roman pre-1955 remains
primarily inherited 1962 material with six Holy Week deltas, and the 1956-1960
middle recension is not held as a complete source-grounded corpus.

The same baseline records the historical January 4 no-Mass result, the
postconciliar 2027-06-05 equal-rank conflict, ambiguous Common selection,
Roman calendar-spine identity failures, scoped-rubric/global-index drift, and
language, territorial, option, weekday-cycle, diagnostic, and generated-data
freshness weaknesses. Rights review found tracked ICEL-facing material without
an adequate per-text/per-surface publication filter, provenance mismatches,
misclassified Gospel Acclamations, missing FDLC artifact records, and Latin
surfaces without sufficient per-text rights evidence. No unavailable or
uncleared text may be filled by reconstruction, an unofficial copy, or silent
cross-recension fallback; an unresolved or withheld state is the correct
result until an exact permitted witness exists.

The visual baseline and browser evidence under the ignored review tree already
establish a calmer 39.75rem reading measure, a readable three-rem cue axis,
cross-browser serif fallback, print/reflow/accessibility coverage, and event,
text, Proper, Ordinary, state, source, seat, and rubric parity for representative
Roman 1962 and postconciliar states. Structured dialogue work may add only
source-owned turns and semantically honest role or versicle/response cues; it
may not split opaque prose by string matching or equate Priest/Server with
versicle/response.

**Exact successor snapshot internally accepted for deployment on independent
AI cold-review evidence; production integration is verified below.** Feature
commit
`a1a7ab774a7318cb0b66d74462090856347d5915` (tree
`b70bdf637387ba552d66d6f7e38704a5ed116f19`) was pushed exactly to
`origin/feature/complete-missal` at that stage before the later
deployment-record and workflow commits, descends without a rewrite from the
then-current `origin/main` base
`2778285849f2973ea89d1cfd5b2751ed4ae58e54`, and its tracked worktree and index
were clean at the exact Firefox capture and handoff assembly. Independent
semantic, source-identity,
rights, generated-freshness, path-integrity, deployment-artifact, commit-scope,
and exact-handoff reviews found no successor blocker.

The accepted source tree carries 619 postconciliar Mass identities, 491 Roman
1962 identities, 489 effective Roman pre-1955 identities, and eight explicit
pre-1955 departure records. The source library validates at 537 works, 722
editions, 1,837 artifacts, 3,295 passages, 72 segments, and 2,167 bindings.
The registered `complete-missal` audit measures all fifteen completion
dimensions over 2020--2120 and reports 39 typed unresolved audit-dimension
cells instead of inventing text or silently borrowing a recension: 8/492/619
represented celebrations and at least 5,158/5,247/3,056 modeled text slots for
pre-1955/Roman 1962/postconciliar respectively. Its source-honest `--check`
passes; its stricter `--require-resolved` mode intentionally refuses while
those explicit cells remain. They are completion-dimension findings, not a
claim that 39 whole texts are absent.

The authoritative full Python run passes 2,302 tests with no failure or error
and ten intentional skips. `make check` replays 203 of 212 captured examples
with no divergence, stale capture, or tracked write; six are policy-exempt or
never-run and three have unavailable fixtures. The annual gate passes all six
tests over 365 days, three calendars, and two languages: 2,190 cases and 4,380
successful JSON/text renders. Five focused Chromium production harness
contracts pass all 134 assertions within six passing unittest gate tests.
Fresh Firefox 154.0.1 evidence is intrinsically bound to the exact clean
feature commit; automated metrics plus AI visual inspection of the canonical
full-Mass desktop 1440x900 and mobile 393x852 states found no horizontal
overflow, duplicate IDs, or failed page requests. The broad Chromium
accessibility run retains exit 1 at the exact inherited baseline rather than a
green gate: 2,290 assertions, 1,850 passes, 212 failures,
and 228 skips, comprising 108 duplicate-main, 77 target-size, and 27 modal
skip-link findings. The other long-running FINAL5 gates ran on the frozen
precommit candidate subsequently committed unchanged; their logs do not embed
a commit or tree identifier and are forensic workflow evidence rather than
intrinsically commit-bound records.

The final deployment-source, public-site, and GitHub-Pages-target verification
gates pass on the frozen successor. The resulting local artifact contains
20,549 regular files and 1,978 directories totaling 436,003,351 bytes, with
20,548 matching checksum entries and no symlink, special file, unsafe link,
forbidden path, residue name, or quarantined-body match. Act-history projects
all 505 canonical files and rejects replaced or linked projection roots;
public-alpha uses descriptor-rooted, no-follow creation and an immutable
verification snapshot with identity-bound cleanup. All generator, Act-history,
release-binding, calendar, and source-reader freshness gates and the tmt
registry check pass.

Rights-withheld bodies are absent from current public structures; formerly
composite celebration identities are split; calendar and option ambiguity
fails closed; and Ordinary and Proper consumers share typed availability,
source, and dialogue semantics. Ten Roman 1962 Latin Proper prayer bodies,
each byte-identical to its selected passage in a Triptych-created editorial-
projection artifact, are published under a record that attributes only the
bounded selection, transcription layout, normalization decisions, and
collation record to Triptych. The underlying prayer wording remains public
domain in the United States; the Lasance antecedent supplies that basis and the
restricted 1962 facsimile remains a separate comparison witness. No new human
collation or approval is claimed. Current-tree
ICEL payloads, quarantined Roman 1962 Latin Proper bodies, and the superseded
Lasance OCR artifact with the excluded 1302a--1302d insert are absent from the
tracked tree, generated surfaces, deployment artifact, and current review
handoff. Reachable earlier Git history still contains protected or superseded
objects. Whether that history requires rewriting, replacement, access
restriction, or another remedy remains a maintainer/counsel release-policy
decision; the required fast-forward workflow deliberately does not rewrite it.

The exact successor review handoff is
`build/agent-handoffs/20260828T172422Z-complete-missal-final-review/`, with a
verified one-root ZIP beside it. Its 15-entry manifest has SHA-256
`9e53c26fd3588f009c770f22a6cf4a7bb3ad8acd48f8c85919e69a88f4d4bd03`;
the ZIP has SHA-256
`e0d42528ccabb6889f8dadd771a6f94b1c068e6744c76e52b1fbf51c17075907`.
It supersedes the preserved `20260828T170544Z` package, which superseded
`20260828T164734Z`; that package superseded the earlier `20260828T045009`
recovery package. This is
AI-assisted and automated review evidence, not human, priestly, specialist,
intended-reader, physical-use, ecclesiastical, or new exact-snapshot human
approval.

**Production integration and live verification complete.** `origin/main` first
advanced by genuine fast-forward from
`2778285849f2973ea89d1cfd5b2751ed4ae58e54` to
`de7c78334d2f7418c20c7a595e6aae9ce45f39c9` after all three local deployment
gates passed on that exact clean tree. Exact Pages run
[`33196238024`](https://github.com/spincyc/triptych/actions/runs/33196238024)
then reached artifact verification only after checkout, dependency
installation, source verification, and the public build had passed; GitHub
cancelled the job at its configured 15-minute ceiling before verification,
upload, or deployment could complete. That is infrastructure-timeout evidence,
not a successful or failed content gate, and no production deployment is
claimed from it.

The narrowly scoped timeout correction raised the workflow ceiling to 30
minutes without changing the gate sequence. `origin/feature/complete-missal`
first advanced by genuine fast-forward to exact commit
`0817b42b500a35002ceb892ade89832093b93522`; the three local deployment gates
then passed on that exact clean correction tree; and `origin/main` then
advanced by genuine fast-forward to the same commit. Pages run
[`33197920174`](https://github.com/spincyc/triptych/actions/runs/33197920174)
and its sole deploy job
[`98939717180`](https://github.com/spincyc/triptych/actions/runs/33197920174/job/98939717180)
completed successfully for that exact `main` head; all source verification,
public build, artifact verification, configuration, upload, and deployment
steps passed. GitHub deployment `6146198392`, final status `17472596177`, binds
that exact commit and `main` ref to the `github-pages` environment and
<https://mystago.gy/>.

A fresh production verification parsed the served checksum inventory and
proved it byte-identical to the local 20,548-entry `SHA256SUMS` artifact, whose
SHA-256 is
`f192be2f12357e141c83f6b2338a9b2ead9e6f221848c26567d8332f25e59bf2`.
All 20,548 inventoried local files were independently authenticated against
that target inventory. Against the captured pre-integration inventory the
verifier identified 16 added, 1,249 modified, and zero deleted paths, then
fetched and matched all 1,265 affected live routes byte for byte with no HTTP,
redirect, truncation, or checksum failure. This closes the promised production
requirement for the deployed content while retaining every audit-dimension,
broad-browser, review-authority, and reachable-history qualification above; it
is not a global legal clearance or human,
specialist, priestly, intended-reader, physical-use, or ecclesiastical
approval.

## E1 Catena integration candidate

The convergence review (branch `review/catena-e1-convergence`, commit
`f1a5bbad763b847ded8799748223898de6ad4de9`) classified the remaining Catena E1
state with zero `MERGE_BLOCKER` and zero `INTEGRATION_BLOCKER` findings,
cancelled the V17 semantic lane as `CANCEL_V17_SEMANTIC`, left the inherited
chapter-root getter, hostile-thenable, and body-write retry findings as
`HARDENING_BACKLOG`, left the eight package/history/replay/scanner defects as
`EVIDENCE_TOOLING_BACKLOG`, left twenty release, shell, data, validation,
Liturgy, PDF, and final-integration concerns `SEPARATELY_OWNED`, and
dispositioned the line **`READY_FOR_INTEGRATION_BRANCH`**.

Acting on that disposition and its exact bring-across manifest,
`integration/catena-e1` was created from the exact authorized main base
`2778285849f2973ea89d1cfd5b2751ed4ae58e54` (origin `main` had not moved past
it), with the reviewed V16 implementation `cc1f2fb8625f044558c26edd358b99cd7dcc7646`
used as final implementation truth rather than merged. The candidate integrates
exactly:

- the final production Catena route, model, page, and stylesheet
  (`src/web/browser/catena/catena-model.js`, `catena.js`, `catena.css`,
  `index.html`), which main had not independently changed since the reviewed
  fork point, so no current-main work was displaced;
- the `scripts/_catena.py` voice-authority change and its deterministic
  regeneration of `src/web/data/structure/catena/index.json`, which now
  publishes the held voice set `original`, `translation:en`,
  `translation:la`, plus the Isaiah 8 chapter file `27-is/008.json`
  regenerated from main's own source records and byte-identical to the
  reviewed V16 generated output;
- the 78-line fail-closed generator-contract expansion of
  `tools/tests/test_catena.py` (56 tests total); and
- `tools/tests/test_catena_production.py`, 419 production-policy regressions
  curated verbatim from the V16 wave-1 suite for publication atomicity,
  owner/completion identity, same-path/late isolation, exact voices with
  `translation:grc` refused, refusal/absence/provenance truthfulness, path
  namespace closure, cache completion isolation, malformed canonical data,
  and the governed budget assertions.

The 17,315-line synthetic wave-1 harness, the hostile
prototype/getter/thenable classes, evidence tooling, attempt history,
packages, correction-lane bookkeeping, and V16-side release or shared-shell
changes were not brought across. The three hardening findings and eight
evidence-tooling findings remain backlog; the twenty separately owned concerns
were not touched; the four Catena release bindings were not refreshed (they
belong to the release owner after accepted integration bytes).

Fresh validation on the integrated tree: the generator contract reports
1,351 fragments / 1 book / 73 canon entries; the focused Catena suites pass
56/56 and 419/419 under node; static browser checks pass 5/5; real-Chromium
route-only runs over `/catena/index.html` produce the same 121 assertion
identities with the same 95 pass / 14 inherited shared-shell fail / 12 skip
statuses at the exact base and at the candidate, with zero status changes;
full discovery runs 1,736 tests at the base (46 failures, 13 errors, 11 skips)
and 2,159 tests at the candidate with identical failure and error identities,
zero new integration-caused failure identities, and zero Catena failures; the
governed gzip-9 budgets measure CSS 7,629/8,000 whole and JS 12,965/13,000
whole with the suite's stripped-ceiling assertions (2,700 and 8,800) passing
and `catena-model.js` uncapped.

Status: **awaiting independent integration review** under the fixed loop of
one independent Codex integration review, at most one bounded correction pass,
one confirmation review, then merge. E1 is not accepted and not integrated; no
merge to `main`, deployment, or release signing has occurred. The candidate
head is the commit carrying this record.

## E1 Catena bounded integration correction

<!-- promised-deliverable: corpus-browser-catena-e1-integration-candidate-2026-08-28 -->

The independent integration review (branch `review/catena-e1-integration`,
commit `c3698563e3b45e35a672db37616e39ef27eb3d08`) returned **CHANGES
REQUIRED** against the candidate head
`9810a29c38f6138069d11cb7c735d8bb8b190326`, with exactly two `MERGE_BLOCKER`
findings and exactly two `BOUNDED_INTEGRATION_CORRECTION` findings, ratifying
`GenuinelyLateStaleWorkTest` and adding one new `HARDENING_BACKLOG` finding
(the empty no-JavaScript `h2`, untouched here). This is the one authorized
bounded correction pass over those four items and nothing else. The V17
semantic lane stays cancelled, the hardening and evidence-tooling backlogs stay
backlog, the twenty separately owned concerns stay untouched, and the four
Catena release bindings stay unrefreshed.

**Merge blocker 1 — translation-absence identities were flattened together.**
`renderAbsences` appended `.absence-author` and `.absence-work` as adjacent
element children with nothing between them, so a row's flattened text — what a
screen reader announces, what a copy takes, what a text-only rendering shows —
read `Ambrose of MilanHexameron`. Corrected with a semantic DOM delimiter (a
`' — '` text node, written only where both halves are present, matching the
`renderLeads` convention the page already keeps), not with CSS: a margin, a
`gap` or a `::before` would move the spans apart on screen and leave the
flattened text exactly as it was. Reproduced first in real Chromium against the
built artifact, then pinned by `AbsenceRowFlatteningTest` (7 tests) on the real
production route, which reads each row's recursive `textContent` and its
child-node sequence, names the reviewed string as absent and its replacement as
present, and carries an adjacent-identity control over two further real rows
(`Jerome — Liber quaestionum hebraicarum in Genesim`, `Remigius of Auxerre —
Commentarius in Genesim`) so a fix written for one row cannot pass. The
disclosure state, its open-on-arrival contract, the eight reasons and the two
partial offers are asserted unchanged.

**Merge blocker 2 — keyboard recovery focus was invisible.** Recovery moves
focus to `#reading`, and the shared shell's `.reading:focus { outline: none }`
out-ranked the universal `:focus-visible` rule, so the browser drew nothing: a
keyboard reader was moved somewhere the page would not show them. The replay
suite could not see it and both existing recovery-focus classes passed
throughout — the shim has no cascade and no computed style, so `activeElement`
was all it could report. Corrected with one rule,
`.catena-page .reading:focus-visible { outline: 3px solid var(--focus); }`:
higher specificity than the shared suppression, `:focus-visible` only so a
mouse press is left undecorated, `var(--focus)` resolving to the section's own
violet ink so the Catena style is preserved, and `outline-offset: 2px`
inherited from the universal rule because it is not part of the `outline`
shorthand. The shared shell is unchanged and the focus-management behaviour is
not removed. Proved by `tools/tests/catena_recovery_focus_gate.mjs`, a
dependency-free CDP gate over the BUILT artifact, run and asserted by
`RecoveryFocusVisibilityTest` (6 tests): on the success path and on the
reviewed failure/recovery path it reads `getComputedStyle` on the element the
browser reports as active and requires `outline-style: solid`,
`outline-width: 3px`, a ring distinguishable from the same element at rest, and
a computed WCAG contrast ratio at or above 3:1 (measured 10.95:1 against the
region's resolved surface); it also requires a mouse press on a document of its
own to draw no ring, and the next keyboard stop after that press to draw one.
Its falsifiability is not assumed: reverting the two product edits in a copy of
the build fails exactly `absence-rows-read-apart-when-flattened`,
`recovery-focus-is-visible-in-real-chromium` and
`failed-recovery-focus-is-visible-in-real-chromium` with `outline-style is
none — this is the reviewed defect` and `flattened together: Ambrose of
MilanHexameron…`, and nothing else moves. The gate reports nothing rather than
reporting a pass it did not observe: with no Chromium or no built site it exits
3, and the Python test skips with the reason and the variable that would enable
it.

**Bounded correction 1 — curated-suite cleanup, with a measured inventory.**
The forbidden candidate SHA pin (`MODEL_SHA256` and
`test_the_model_is_byte_identical`) is removed and not replaced by another
commit or version pin. Twelve synthetic hostile/evidence-only classes and one
hostile method are removed, and with them the harness machinery that existed
only to serve them: the `Map.prototype` publication probe, the failing-body-write
seam, the prototype-contamination and inherited-accessor transport seams, the
drifting-descriptor and walking-inventory `Proxy` builders, the six-bucket
observation counters, the realm-pollution hook, the projected-row override, the
mutation-attempt authority probe, and the eight journal channels that only they
wrote to. `GenuinelyLateStaleWorkTest` is retained as ratified, with its
`GUARDED` dependency. The 2026-08-11 print pin `test_the_focus_overrides_are_gone`
asserted that no focus rule of any kind lives in `catena.css`, which is wider
than the finding it encoded; it is replaced by
`test_the_only_focus_rule_defers_to_the_shared_role`, which pins exactly one
focus rule, its exact selector and body, the absence of any bare `:focus`, and
its absence from the print block.

The ordinary coverage the first curation lost along with its hostile classes is
restored rather than argued away: chronology grouping, absence counts,
paragraph counts, author-filter recovery, leads copy, shared-field generator
drift, null and list bootstrap truth, visible failure text, and unregressed
Scripture (nine classes, 35 tests, with the seven plain scenarios they read).
The disproved `8 hostile + 40 non-manifest` split is not retained. Counted the
same way for both files — a class is runnable if it defines at least one
`test_` method — the truthful inventory is:

| | runnable classes | tests | dependency-only bases |
| --- | --- | --- | --- |
| corrected candidate suite | 71 | 394 | 3 |
| V16 wave-1 source | 105 | 604 | 3 |
| omitted | 36 | 221 | 0 |
| added by this correction | 2 | 13 | 0 |

Two retained classes are one test lighter than in wave-1 (`FrozenContractTest`
lost the SHA pin; `V15TransportOwnershipTest` lost the write-break probe). All
nine required coverage categories are represented: exact voices, refusal /
absence / provenance, namespace closure, projection and transport ownership,
same-path and late isolation, cache isolation, malformed production data,
governed budgets (`PayloadTest`), and the generator contract
(`V7SharedFieldDriftTest`, which reads `scripts/_catena.py` itself, with
`tools/tests/test_catena.py`). The file is 9,797 lines, down from 12,836.

**Bounded correction 2 — record integrity.** The candidate ledger entry
`corpus-browser-catena-e1-integration-candidate-2026-08-28` had no
`<!-- promised-deliverable: ID -->` marker, which is the one work-register
marker the register requires and the cause of the
`test_promised_deliverables.PromisedDeliverableTests.test_repository_ledger_is_valid`
failure; the marker above is it. The recorded generator command
`scripts/_catena.py check` is not executable as written — the file is mode 644
and a bare invocation returns `Permission denied` — and is corrected to
`python3 scripts/_catena.py check`, which is the command actually run. Full
discovery is rerun at the exact base and the exact corrected head.

Fresh validation at the corrected head: `python3 scripts/_catena.py check`
reports 1,351 fragments / 1 book / 73 canon entries; `python3 scripts/_catena.py
structure` and `paragraphs` regenerate `src/web/data` byte-identically (zero
changed paths); `test_catena.py` passes 56/56 and the corrected curated suite
394/394 including the live Chromium gate; static browser checks pass 5/5;
governed gzip-9 budgets measure CSS 7,921/8,000 whole and 2,698/2,700 stripped,
JS 12,992/13,000 whole and 7,843/8,800 stripped, with no ceiling raised and
`catena-model.js` uncapped; real-Chromium route-only runs over
`/catena/index.html` produce the same 121 assertion identities with the same
95 pass / 14 inherited shared-shell fail / 12 skip statuses at the exact base
`2778285849f2973ea89d1cfd5b2751ed4ae58e54` and at the corrected head, with zero
status changes and zero identity changes; full discovery runs 1,736 tests at the
base and 2,134 tests at the corrected head, both reporting 46 failures, 13
errors and 11 skips over the identical 24 failure identities and 13 error
identities, so there are **zero new integration-caused failure or error
identities** and zero Catena failures.

Status: **awaiting one confirmation Codex review**, scoped to these four
corrections and a regression check. E1 is not accepted and not integrated; no
merge to `main`, deployment, release signing, or self-acceptance has occurred,
and no new hardening lane was opened.

## E1 Catena integration merged to main

The confirmation review (branch `review/catena-e1-integration-confirmation`,
durable review commit `7dfd944494a8d9355264579156214f16d3722a9f`) examined the
corrected candidate against the pre-correction head
`9810a29c38f6138069d11cb7c735d8bb8b190326` and the integration base, and
dispositioned the line **`CONFIRMED — CATENA E1 INTEGRATION READY TO MERGE`**.
Acting only on that disposition, the exact confirmed candidate
`b832cdc5bc01391cea67c01437318d25e0c7c315` was merged into the exact reviewed
`main` head `004615faf506eb4083d484d41b18ee1c61f0aa7f` as a true merge
commit, preserving both parents rather than squashing or rewriting either lane.

The merge-tree rehearsal and the merge itself found exactly the two textual
conflicts the confirmation review predicted, both append-only records, and no
production, source, test, data, configuration, shared-shell, Liturgy, or PDF
conflict. `PROJECT-WORK.md` kept both lanes whole: every current-main Missal
remediation and post-base record, and every Catena E1 integration,
bounded-correction, and confirmation record, with nothing deleted and nothing
duplicated. `promised-deliverables.toml` needed the structural care the
confirmation reviewer flagged — the shared `[[deliverables]]` header sat above
the hunk and a single array terminator below it, so concatenation would have
nested one deliverable inside another — and was resolved into two complete
independent entries, each with its own header and every array closed:
`complete-missal-remediation-2026-08-26` unchanged at `complete`, and
`corpus-browser-catena-e1-integration-candidate-2026-08-28` moved from
`candidate` to `complete` with one added requirement recording the confirmation
review and this merge. The ledger validates at 32 tracked and 24 complete with
no duplicate identifier, and `test_repository_ledger_is_valid` passes.

The merge introduces exactly thirteen paths against current `main`: the twelve
tracked manifest paths and the one authorized new gate
`tools/tests/catena_recovery_focus_gate.mjs`. The merged index carries no
content delta from the confirmed candidate across
`src/web/browser/catena`, `scripts/_catena.py`,
`src/web/data/structure/catena`, `tools/tests/test_catena.py`,
`tools/tests/test_catena_production.py`, and that gate, so no Catena
production, test, or generated byte was altered by conflict resolution. No
shared shell, Liturgy, PDF, release-binding, deployment-configuration, or
unrelated data or CLI path was touched.

Minimal post-merge validation on the merged tree: `python3 scripts/_catena.py
check` reports 1,351 fragments / 1 book / 73 canon entries;
`tools/tests/test_catena.py` passes 56/56; the curated production suite passes
394/394 with zero skips, the real-Chromium recovery-focus gate executing rather
than skipping and reporting a measured focus-ring contrast of 10.95:1 with no
failed assertion; the static browser checks pass 6/6, which is current `main`'s
own count after it added a sixth check above the integration base and therefore
supersedes the candidate-era 5/5; and the real-Chromium route-only run over
`/catena/index.html` reproduces the confirmed status universe exactly at 121
assertion identities, 95 passing, 14 failing and 12 skipped, with the fourteen
failures being only the inherited shared-shell identities
`single-main-element` (9) and `primary-controls-meet-target-size` (5), which
are separately owned baseline rather than merge blockers.

Nothing beyond the merge was reopened. The three hardening findings remain
`HARDENING_BACKLOG`, the eight package/history/replay/scanner defects remain
`EVIDENCE_TOOLING_BACKLOG`, the twenty release, shell, data, validation,
Liturgy, PDF, and final-integration concerns remain `SEPARATELY_OWNED` and
untouched, and the V17 semantic lane stays cancelled. At the merge commit the
Catena release bindings were still unrefreshed and no release record had been
re-signed; the section below records why that could not stand and what was
authorized instead. The push that advances `main` authorizes only the
repository's automatic GitHub Pages attempt that any `main` push triggers,
which is not itself evidence of a verified live snapshot.

## E1 Catena release bindings refreshed so the merged bytes can publish

The merge commit `85f41e4e467d5f4b4331ee71da0666a1c0ebddf9` reached `origin/main`
with the confirmed Catena bytes and the Catena release bindings deliberately
left as the integration lane had them. Pages run
[`33265104292`](https://github.com/spincyc/triptych/actions/runs/33265104292)
therefore failed at `public-alpha verify --deployment-target github-pages`, the
gate that refuses when a site source no longer matches its approved SHA-256:
authorization `perpetual-public-repository-2026` still recorded the
pre-integration hashes for `catena-model.js`, `catena.css`, `catena.js`,
`index.html`, and `src/web/data/structure/catena/index.json`, and had no record
at all for the newly generated `src/web/data/structure/catena/27-is/008.json`.
The run stopped before Configure Pages, Upload, and Deploy, so nothing was
published and deployment `6158143411` ended `failure`; the live site continued
to serve the previous `004615faf` snapshot throughout. This was the predicted
consequence of landing accepted integration bytes while their approved record
still described the superseded ones, not a defect in the merge: the merged tree
carries no content delta from the confirmed candidate.

Refreshing that record is release-owned re-signing, which the merge lane
explicitly withheld, so it was not done as part of the merge. The maintainer
then authorized it directly. `make refresh-release-bindings ADOPT=1` was run
under `ONLY=` naming exactly the six affected paths, so the authorization
carries only the reviewed Catena bytes forward and could not sign for any other
entry; it re-recorded the five changed site sources, adopted the one new
generated file, and updated the rights table and its `rights_record_sha256`,
which are mechanically derived from those same paths. No hash was hand-edited
and no approval note was invented. `make check-release-bindings` then reports
`exact: 0 stale binding(s)`, and every re-recorded value equals the hash of the
file as merged.

All three gates the Pages workflow itself runs then passed locally on the exact
refreshed tree: `make check-deployment-sources`, `make public-site`, and
`python3 tools/tpt public-alpha verify --deployment-target github-pages`, the
last reporting `verified build/public-alpha/site`. The Catena integration
validation above was not rerun and is unchanged; this work touched only
`release/public-alpha.json` and `release/rights/public-alpha-2026-07-15.md`. The
hardening and evidence-tooling backlogs, the twenty separately owned concerns,
and the V17 cancellation all remain exactly as the merge left them.

## B0/B1 shared-foundation convergence against current main

The corpus-browser program's B0/B1 lane was dispatched again from
`origin/main` `09437907472581df4a8969010bd494249a3539a5`, the Catena E1
post-merge release-binding refresh, onto `impl/corpus-foundation-b0-b1`. The
task was reconciliation rather than implementation: most of what
`guidance/corpus-browser-implementation.md` §11 proposed had arrived on the
mainline by routes the document could not see, because it was written from
`impl/foundation-hardening`, which was never a descendant of `main`. The
step-by-step disposition, its evidence, and the one remaining blocker are
recorded in that document's new §11.1, which owns them; they are not restated
here.

Three facts are worth having in the operational record.

**The historical red baseline is not today's.** `python3 -m unittest discover -s
tools/tests` at the dispatch base is 2,707 tests, 24 failures, 0 errors, 11
skipped, and every failure is `test_tool_registry` — 23 worked-example subtests
and one `pdf-review.test` shell smoke test. Nothing browser-related is red.
§11's recorded "14 failures and 13 errors" belonged to `c27d69153`. The lane's
problem on current main was coverage `make check` does not reach, not failures it
does not fix, and step 3 — the narrow browser-model gate — was the one item of
steps 1-4 and 9 still missing. It is now `check-browser-models`: twelve modules,
358 tests, about 162 seconds, inside `make check`, with
`tools/tests/test_browser_model_gate.py` refusing a future suite that drives
browser JavaScript and is neither gated nor recorded as ungated with a reason.

**A fifth selector hazard of the recorded class was found in an unprotected
file.** `sources.css` set a 44-pixel target floor on `.brand a` and
`.site-footer a` — classes `release/public-alpha/layout.html` owns — with no page
scope, on the argument that the stylesheet is served only on one route. That is
the `.field` and `.detail` mistake with `<link>` presence standing in for
`<link>` order: in a shared bundle the rule restyles the masthead and footer of
every page on the site. It is scoped, and the class rather than the incident is
now held by `test_browser_collisions.SiteChromeScopeTest`, which reads the
layout's own classes out of `layout.html` and requires any remaining exception to
be recorded with the authority that owns it.

**`shared-shell-blocking-collisions-resolved` moves from `open` to `blocked`, and
not to `pass`.** The distinction is the point: `day-missal.css` still restyles
`body > .site-header` in twelve selectors, and that file is inside the protected
reader family which master-plan decisions D2 and D18 and boundary 4 close until
`liturgy-reader-live-ritual-flow-2026-08-07` releases or carves out the seam.
That deliverable remains `in_progress` with all six requirements `open`, so no
corpus lane may make the change. §11.1 states the twelve selectors, the four
routes that load them, why they block a shared shell, the smallest mechanical
scoping change, and the exact one-sentence carve-out required. Both `open` and
`blocked` are unmet states and neither may be waived without a `waiver_reason`
and a `waiver_authority`; `blocked` is the truthful one, because the work is not
merely undone.

Steps 6, 7, and 8 were deliberately not executed. Step 6, promoting
`reader-shell.js` and `reader-shell.css` to `shared/`, is **withdrawn** by D2 and
D18 rather than deferred, so it is not a carve-out anyone should ask for. Steps 7
and 8 are written as depending on it; step 7 would centralise a commonality no
current pair of production surfaces has demonstrated, and step 8's neutrality
could only be proved against surfaces this lane may not touch. Master-plan
steps 10 and 11 — generated site navigation and the nested `<main>` — remain
outside B0/B1 and are recorded as downstream blockers.

Validation was measured against the exact dispatch base rather than against an
exit code. Real Chromium over the built artifact at 19 routes by the nine-state
governing matrix returns identical reports at base and candidate: 2,290
assertions, 1,850 passed, 212 failed, 228 skipped, byte-identical rows including
every detail string. The 212 are three inherited identities that belong to
others — 108 nested-`main` rows over twelve routes (step 11), 77 target-size rows
measured against WCAG 2.2 AAA by the gate's own stated choice, and 27 skip-link
rows caused by the protected propers reader opening a modal on load. The five
reader harnesses pass their exact all-green contract. Full discovery at the
candidate head reproduces the base's 24 failures and 0 errors with no new
identity.

One release binding is deliberately stale:
`src/web/browser/sources/sources.css`. Re-signing is release-owned and this is an
implementation candidate, so `make refresh-release-bindings` was not run in any
form and no hash was hand-edited. `make check-release-bindings` therefore
reports one stale path on this branch, which is the expected state and not a
build or source failure. Nothing was merged, deployed, released, or
self-accepted, and no subsequent lane was begun.

### Independent cold disposition, 2026-08-30

The independent review used fresh full-checkout base
`09437907472581df4a8969010bd494249a3539a5` and exact fetched candidate
`407dfad76061460e1b3f5e3ad65ea41c73c5f746`.

**B0/B1: CHANGES_REQUIRED.** The current named browser-model modules are under
`make check`, but the meta-test that discovers a future omitted
JavaScript-driving suite is not; it runs only through opt-in full discovery.
The collision detector also misses broad element selectors and negative
pseudo-class scope, and records the protected exception by count rather than
exact identity. It therefore does not prove the stated selector class or that
`day-missal.css` is the only remaining site-chrome-reaching instrument rule.

The branch is six commits ahead of main at the reviewed head. Three were created
by the B0/B1 execution (`8ff111516`, `a39f4bce0`, `3d323f088`); with its earlier
continuation record the execution endpoint had four ancestry commits, and the
later Catena Omnia and cold-review records make six.

Fresh host evidence is 2,707 tests / 23 failures / 0 errors / 10 skips at base
and 2,719 / 24 / 0 / 10 at head. Exactly one identity is new:
`test_accepted_shell_and_visual_oracle_hashes_are_current`, reporting the one
deliberately stale `src/web/browser/sources/sources.css` release binding. The
earlier `pdf-review.test` smoke failure did not reproduce on this host. The
twelve named model modules contain 362 tests, not 358, and took 166 seconds in a
complete non-fail-fast run. Base and head Chromium reports remain identical at
2,290 rows (1,850 pass / 212 fail / 228 skip), including every identity and
detail.

The Sources CSS correction is render-neutral by that evidence. No protected
Liturgy source, shared production shell source, release record, Catena
production/generated source, or Catena generator changed. The twelve
`day-missal.css` selectors remain untouched and blocked by
`liturgy-reader-live-ritual-flow-2026-08-07`, still `in_progress` with all six
requirements open.

**Catena Omnia vision: ACCEPT_WITH_CORRECTIONS.** The narrow-order statement now
preserves accepted E1's projection refusal before affected Scripture while
retaining Scripture as canonical anchor. The whole-corpus horizon, exact
commentary/source binding, L1/L2/L3 distinction, protected-Liturgy boundary, and
separate optional AI synthesis are otherwise sound.

**Catena Omnia roadmap: ACCEPT.** It requires a scale benchmark before transport
redesign, advances bounded corpus acquisition alongside foundation work, puts
typed source-owned edges before advanced navigation, preserves Search as
J0/J1/J2, and keeps review, signing, deployment, and protected-surface authority
separate.

No release binding was refreshed. No implementation or protected-Liturgy
correction, merge, deployment, signing, self-acceptance, or next Catena feature
lane was performed.

### Remediation of the two blockers, 2026-08-30

Dispatched from `e135e65bbea80877eb75a39945b750fc7566642f` on the same branch,
scoped to the two `CHANGES_REQUIRED` findings and nothing else. The step matrix,
the strengthened contract, the exact protected inventories, and the measurements
are owned by `guidance/corpus-browser-implementation.md` §11.3 and are not
restated here. Four operational facts belong in this record.

**The coverage meta-test is now a `check` prerequisite, and the fix is a topology
change rather than a list change.** Adding `test_browser_model_gate` to
`BROWSER_MODEL_TESTS` would have run it and simultaneously falsified that
variable's own invariant, since the gate asserts that every module it names
drives browser JavaScript and the meta-test drives none. A separate
`BROWSER_MODEL_GATE_TESTS` variable and a `check-browser-model-coverage` target,
made a prerequisite of `check-browser-models`, close the hole with one edge and
run the meta-test before the 150-second model loop instead of after it. The
module grew from 8 tests to 22, and the new ones do not trust the edge they
depend on: they walk the prerequisite graph from `check`, require the recipe to
read the variable that names the module, and replay `make -n check` to confirm
the printed recipe really runs it. A synthetic unnamed browser-driving suite makes
both the coverage target and `check-browser-models` exit 2, and removing it
returns both to 0 — the exact scenario the review said was unenforced.

**The collision detector stopped reading selector text for names.** It now
imports `tools/public-alpha`'s own `wrap_in_layout`, renders both the published
and the preview shell, parses them into an element model that keeps `<main>` but
discards its subtree, and asks of every instrument selector whether any arm can
match any chrome element — with `:not()` and `:root` evaluated, positive-only
scope, `:is()`/`:where()` scoped only when every alternative is, and anything it
cannot classify raising rather than passing. That closes all three defects the
review named, and it found three unrecorded hazards of the same class while doing
it, all inside the protected reader family: `reader-shell.css`,
`reader-instrument.css`, and `reader-visual-reset.css`. They are recorded with
their authority rather than corrected, for the same reason `day-missal.css` is.
The exception record is now four files and exact selectors in order, so
substituting one unscoped selector for another fails where the old count of
twelve passed. That suite grew from 15 tests to 32.

**One production stylesheet changed, and it changes what two routes render.**
`scripture.css`'s bare `a` and `a:hover` are now scoped through
`:where(.plan-page, .track-page)` — `:where()` so the rules keep their
specificity and the file's own `.eyebrow a` override still wins, and the page
classes rather than a `body` prefix because `browser_page_parts` projects a
browser page's body classes onto `<main>`, leaving the published `<body>` with
none. Measured in real Chromium, every in-content link on both routes keeps its
colour and the footer links move from `rgb(69, 63, 56)` to `rgb(143, 53, 64)`.
That is the fix rather than a regression: the old value was the neutral
`--section-ink` fallback resolving outside `<main>`, and `/texts/`, `/law/`,
`/history/` and `/sources/` already render those footer links at
`rgb(143, 53, 64)`. Scripture was the one route where a page stylesheet
overrode chrome the site's own stylesheet owns. It is disclosed on
`no-visual-or-product-decision` in the ledger so a reviewer judges it rather
than discovers it.

**The stale binding set is now two paths, but the stale bindings are not the
whole reason `make check` is red — a prior version of this paragraph claimed
they were, and that claim was too strong.** `src/web/browser/scripture/scripture.css`
joins `src/web/browser/sources/sources.css`; both are deliberate, neither was
refreshed or hand-edited, and re-signing is release-owned. `make -k check`
fails `check-release-bindings`, the same oracle inside `check-browser-models`
that shells out to it, and `check-examples` with 16 divergences of 212
captured examples. Of those 16, twelve are inherited — they diverge at the
remediation base `e135e65b` too, predating the stale bindings — and four are
the stale-binding cause echoed through captured transcripts that recorded
`exact: 0 stale binding(s)` or a verified preview build. Red identities that
exist at the base independently of the stale bindings: the 12 inherited
`check-examples` divergences, and — in full test discovery rather than in
`make check`, where `tmt` is absent and `check-tool-registry` skips — the 23
worked-example failures of `test_tool_registry`. What the branch ADDED to the
red set is exactly: the two stale bindings, the release-binding oracle identity
inside `check-browser-models`, and the four echoed example divergences. Everything
else is green:
`check-browser-models` is 401 tests over 13 modules where it was 362 over 12,
the five reader harnesses hold their all-green contract, Catena is untouched and
still 1,351/1/73 with 56 and 394 tests passing, and the Chromium artifact gate
returns byte-identical 2,290-row reports at base and candidate. Full discovery
was run on both trees on this host: 2,719 tests / 24 failures / 0 errors / 10
skips at the base, 2,750 / 24 / 0 / 10 at the candidate, whose 31 extra tests are
exactly the 14 and 17 added to the two suites. The failure identities are the
same on both sides and no new one appears.

`shared-shell-blocking-collisions-resolved` remains `blocked`. Nothing was
merged, deployed, signed, self-accepted, refreshed, or begun as a next lane, no
protected Liturgy or Catena source was touched, and the candidate stops here for
independent cold rereview.

### Selector-oracle remediation, 2026-08-31

Dispatched from `2440e3e84929c81bc42631bcd3622c592f71da39` on the same branch,
scoped to the one remaining substantive blocker of the third independent cold
review and nothing else. That review returned **B0/B1 — CHANGES_REQUIRED** with
Blocker A closed, and reproduced two classes of false negative for VALID CSS in
the Python selector analyzer: an unmodelled pseudo-class treated as
satisfiable, which reverses conservative reasoning inside `:not()` (so
`a:not(:hover)`, `.site-header:not(:focus-within)` and the case-insensitive
`[class~="SITE-HEADER" i]` were read as unable to reach chrome they really
match), and route scope inferred from raw selector text (so `a[href$=".html"]`
was scoped by `.html`, a `:has()` list with a global alternative was scoped,
and a `:is()` tautology was scoped). The claim that the analyzer "fails closed"
is corrected in place: it failed closed only on forms it could not parse, and
reported scoped precisely where it did not understand.

**Whether a selector can reach the site's chrome is now decided by Chromium,
not by Python.** `tools/tests/site_chrome_selector_oracle.mjs` drives one real
Chromium — the repository's dependency-free CDP conventions, no new
dependency — over 36 shells rendered by the build's own `wrap_in_layout`: the
neutral shell with the page's identity absent from `<main>` (public and
preview), all thirteen published browser pages exactly as the build renders
them, and four site pages outside the browser tree. Python keeps only
extraction, identity normalization, orchestration and inventory comparison; the
compound parser, attribute matcher, combinator walker, negation stripper,
scope inferencer and the in-memory chrome element model are deleted. The
verdict is a differential rather than a name scan: an arm is unsafe when it can
reach site chrome in the neutral shell, whatever route-looking text it
carries, and positively scoped when reaching chrome genuinely depends on a
state the page projects. Fail-closed is now a stated refusal: an arm Chromium
rejects, or one naming `:visited` — whose truth Chromium withholds from
script — is reported and treated as unsafe, never silently permitted. A
pseudo-element arm is judged by the element it belongs to (Chromium's
`querySelectorAll('*::before')` matches nothing, the most dangerous answer
available), with the over-approximation's direction proved by reading a
non-inherited declaration back through the style engine. A bounded user-state
walk — pointer over every chrome leaf, a held press, keyboard focus after one
real Tab, the fragment target — runs on the two neutral shells plus one
preview page, because a quiescent document would call `a:hover` and every
state-keyed selector safe.

Measured: all six cold-review counterexamples are caught with recorded
witnesses; the browser reproduces the four protected Liturgy inventories
exactly (12/3/2/3) and finds zero new hazards across 1,193 production arms in
2.6 s, one session, one batched request; adversarial escaped, nested,
comma-bearing-attribute, grouped and all-combinator cases classify correctly;
`test_browser_collisions` is 34 tests in 9.1 s where the modeled version could
not answer these at all; `test_browser_model_gate` stays 22 tests OK; and the
protected-inventory mutations (substitution, removal, and a substitution whose
commas sit inside a functional pseudo) all fail. No production byte changed in
this pass — the only changed non-record paths are
`tools/tests/test_browser_collisions.py` and
the new `tools/tests/site_chrome_selector_oracle.mjs` — so the stale
release-binding set remains exactly `src/web/browser/scripture/scripture.css`
and `src/web/browser/sources/sources.css`, unrefreshed.

`shared-shell-blocking-collisions-resolved` remains `blocked`. No merge,
deployment, signing, binding refresh, protected-Liturgy edit, Catena edit,
Search, acquisition, or next lane was performed. The candidate awaits
independent cold rereview, and B0/B1 is not self-accepted.

### Independent cold rereview of the selector oracle, 2026-08-31

An independent reviewer fetched `73363fcbce22fc551528047c7e69f33275d54b58` into
its own clone, detached at that commit, drove the same Chromium the gate drives
(`Chrome/151.0.7922.173`), and returned **B0/B1 —
ACCEPT_WITH_CORRECTIONS**. It confirmed nine claims — that Chromium and not
Python decides selector truth (sabotaging the harness's `reach()` to answer
safe turns the suite red with 55 failures, and the whole matching machinery is
gone); that all six counterexamples reach chrome, reproduced with the
reviewer's own CDP script rather than through any harness helper; that the
route-dependent forms are still permitted; that fail-closed is real, with
eight of its own probes refused and CSS nesting failing closed in extraction;
that the four protected inventories are exactly 12/3/2/3, independently
re-derived and mutation-sensitive; that the production tree holds 1,193 unique
arms over 15 sheets with **zero refusals** and no new hazard; that the run is
one browser session, 1 batch, 72 navigations, 52 arms, 665 ms startup, 34 tests
in 9.154 s; that Blocker A stays closed at 22/OK; and that the candidate diff is
exactly six paths, none of them protected Liturgy, Catena or a release binding.
It probed 52 adversarial arms beyond the candidate's own list and found each one
classified as claimed.

It found **one latent fail-open, and the record overstating its own bound.** The
user-state walk forces one state at a time — plus whatever a press carries, which
is why `.site-header:hover a:focus` was caught by accident — so an arm needing
two simultaneous user states on two different chrome elements was reported safe.
After a real Tab and a real pointer move, real Chromium matches
`a:focus ~ .site-footer:hover` against `footer.site-footer` and
`.skip-link:focus ~ .site-footer:hover a` against two footer anchors, where the
harness reported `reach={}`. No production selector has that shape today, so it
was latent rather than live, which is why the disposition is
ACCEPT_WITH_CORRECTIONS: the six counterexamples, the four inventories, the
production scan and Blocker A all stand. Its four required corrections are the
bound's disclosure, failing closed for that shape, wiring up the harness's unread
`interactive` measurement, and one changed-path overstatement.

The rereview deliberately did NOT re-run full discovery on either side, `make -k
check` or any aggregate, `check-browser-static`, `check-browser-harnesses`, the
real-Chromium artifact gate, `check-examples`, release-binding verification, the
Catena suites and route evidence, the public or preview site build, or the
Scripture visual/accessibility/320 px route proof. It relied on the previously
measured baseline for all of those and spent the time on adversarial disproof
instead, so nothing here re-measures them.

### The rereview's four corrections, 2026-08-31

Exactly the four required, and nothing else: no production CSS or JS, no
protected Liturgy file, no Catena anything, no release binding, no `Makefile`
change, and no binding refresh.

**The two-state class now fails closed.** The oracle splits Chromium's own
serialization of an arm into compounds — at top-level whitespace and combinators
only, so a combinator inside `:has(…)` belongs to its compound — and refuses the
arm, with the reason stated, when two or more compounds name a forced user state.
It is the same lexical regex the walk already uses to decide which arms need the
walk, applied per compound, so no selector semantics returned to our code, and an
escape that hides a separator can only split a compound in two, which is the
direction that refuses. Two states in one compound (`a:hover:focus`) are not
refused, because the walk establishes that one. A refusal was already an unsafe
verdict, so nothing needed a new verdict path.
`test_two_simultaneous_user_states_are_refused_rather_than_called_safe` holds
both witnesses refused-and-unsafe permanently and holds `.track-page a:hover`
classified as before. **The harness's `interactive` measurement is now read**
rather than returned to nobody: the client keeps the `init` reply and asserts no
chrome element in any of the thirty-six shells can carry a form or element state
the walk does not force, so the layout gaining a `<button>`, `<details>` or
`<dialog>` outside `<main>` fails the gate. And §11.4's bound now discloses the
one-state-at-a-time walk with `a:focus ~ .site-footer:hover` named as the
witness, while the changed-path sentence says "the only changed non-record
paths", six paths having changed in all.

Re-measured on this host under `Chrome/151.0.7922.173`:
`test_browser_collisions` is **36 tests OK in 9.0 s** where it was 34, the two
new tests being the refusal regression and the `interactive` assertion;
`test_browser_model_gate` stays 22 tests OK; `check-browser-static` is 6 tests
OK; and the full production scan is unchanged at **1,193 unique arms with zero
refusals**, the same per-file unsafe counts, and the same exact 12/3/2/3
protected inventories. **No production arm became newly refused.** The three
witness arms are refused and unsafe, and `.site-header:hover a:focus` — which the
walk previously caught only because a press carries its own focus — is now
refused and still unsafe.

`shared-shell-blocking-collisions-resolved` remains `blocked`. Nothing was
merged, deployed, signed, refreshed or self-accepted, and the stale
release-binding set is still exactly `src/web/browser/scripture/scripture.css`
and `src/web/browser/sources/sources.css`.
