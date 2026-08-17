# Project Work Register

This is Triptych's provider-neutral operational memory. Read it together with
`promised-deliverables.toml` before starting or resuming work, after a context
handoff, and before reporting completion. “Published,” “built,” “committed,”
“pushed,” “review copy,” and “complete” are different states.

Last reconciled: 2026-08-17.

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

**Domain state, recorded so nobody manufactures a fix.** The public origin
moved to `https://mystago.gy/` entirely through GitHub Pages settings and
DNS; no repository change accomplished it and none was made by this
integration. The old origin 301-redirects. `tools/public-alpha` still
declares `SITE_ORIGIN = "https://spincyc.github.io/triptych"`, so `og:url`
and `og:image` metadata name the old origin (reachable via the redirect), and
`tools/tests/liturgy_reader_visual_reset_browser.mjs` baselines against the
old URL. Correcting the canonical origin is product/domain-architecture work
under the master plan, not a bug fix to smuggle in; Triptych remains the
product and repository identity.

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

### E1 Catena route-owned correction lane, pass 2

<!-- promised-deliverable: corpus-browser-catena-e1-corrections-v2-2026-08-11 -->

The 2026-08-11 independent correction review (`8f8f424ec5ccd5300dcee997a529f79fc23a8959`,
branch `ux/catena-wave-1-e1-correction-review`) held E1 Catena at **CHANGES
REQUIRED** for correction head `dfc636665df26563138ff893bd2a9f9afc7d80c0`: the
URL parser accepted contradictory duplicate keys and malformed translation
voices; an identical invalid address validated and recovered differently
depending on the controls a reader left behind, and recovery lost focus; stale
load failures could erase newer state; blocked and empty claims could
contradict one another, and integrity or invalid states could label a voice an
absence; lead and licence rendering overstated or suppressed what the record
supplies; browser print omitted the selected Scripture edition while keeping
interactive footer matter; the accepted forced-colors correction carried a
route focus rule that overrode the accepted shared role; and the first handoff
package was protocol-incomplete, with inaccurate head, page-count, gate and
navigation claims, absent referenced captures, and machine-private values.

This second bounded lane, from unmoved main `9b9ff74a77d1bcd7d454d2a7fc448b8a6c8f1fd4`
on branch `impl/catena-wave-1-e1-corrections-v2`, carried the useful route/test
commit `67191afd1d6281006e5cb947596452481c0d9692` forward and corrected every
route-owned defect above in `981959b4f78209401ba00bfbdcc430e23e09c8bb`, inside the exclusive boundary of
`src/web/browser/catena/catena.js`, `catena.css`, `index.html`, and
`tools/tests/test_catena_wave_1.py`. The focused suite grew from 99 to 179
tests and stays green; the original 8,000/13,000-byte whole-file gzip-9
ceilings hold unraised at 7,629 and 12,996; `catena-model.js` is byte-identical
to main; and the browser-gate failure identity/status set is unchanged from the
pristine-main baseline, with 15 Catena assertion `detail` texts differing and
no assertion changing status — the rows are not byte-identical and this record
does not call them so. `check-release-bindings` deliberately fails closed on
the three changed route assets, and the single new `check-examples` divergence
is that same unsigned-binding condition seen through
`tools/public-alpha verify --preview`, until the release owner re-signs.

An internal adversarial audit of this lane's own candidate found six further
route-owned defects — a stranded focus on the failure arm of recovery, a
superseded arrival's voice leaking into the next reader action, the route's own
history echo reverting a reader who had already moved, a blocked-only chapter
manufacturing a voice absence, malformed payload, lead and blocked values
coerced into words, and a malformed acknowledgement suppressing a valid one —
each now fixed and pinned by its own regression test. Ten further observations
are recorded as decisions or limitations in the handoff rather than silently
fixed, and two belong to other owners.

No real assistive-technology session was possible in this environment, so that
requirement is recorded as unmet with labelled accessibility-tree and
keyboard-sequence supplements in its place, and forced-colors evidence is
labelled browser emulation rather than a system palette. Generator/data,
release, common-gate, and B0/shared-shell prerequisites remain with their
owners in the roadmap subsection and the package's unresolved-blocker ledger. A
new immutable sanitized handoff, `20260811T212656Z-catena-e1-corrections-v2`, records the exact
candidate head; the sole next action is a fresh independent review of that head
and its package. Nothing here is accepted, integrable, merged, re-signed, or
deployed.

### E1 Catena route-owned correction lane, V3

<!-- promised-deliverable: corpus-browser-catena-e1-corrections-v3-2026-08-12 -->

The independent review of correction V2 (`4c30d86f7118d69eb27d12dc9b63568e531918eb`,
branch `review/catena-wave-1-e1-corrections-v2-independent`) dispositioned the
reviewed head `17f031b37840d8320c664a128d72b502108fe075` **CHANGES REQUIRED**. It
found the V2 URL, history, asynchronous-ownership, truth-state, lead, print,
focus and responsive corrections sound under adversarial replay, the package
mechanics and unraised budgets sound, and named exactly four things for this
lane. Two are implementation defects and two are inaccurate statements; every
other finding remains with the owner the review assigned it to.

First, a structurally well-formed but unsupported voice. `voice=translation:zz`
satisfied the closed two-or-three-lowercase-letter grammar and was then carried
into the page as `none in ZZ translation`, which converts an unsupported voice
into a claim about what the corpus holds. Shape and support are now distinct
questions: the supported language set is read from `index.held[].languages` —
Catena-owned runtime truth the route already has in memory before any voice is
resolved, requiring no new request — and a well-formed voice naming a language
the corpus holds nothing in fails closed through the existing invalid-address
state, exactly as an unpublished `bible` value does. A voice the chapter merely
lacks is unchanged and still names itself rather than widening.

Second, untyped displayed provenance. Every provenance value this route shows
now passes one typed gate before it can become words. The review named
`edition`, `edition_published` and one `translators` item; this lane's own
audit found the same coercion on `locator`, `review`, `author`, `work`, `date`,
`language`, the author heading, the author-filter label and the numbering
refusal note, and one case that was worse than a coercion: a `translators`
value carrying a `length` and no `join` threw out of the asynchronous render,
so the tally, the announcement, focus recovery and the route write never ran
and the reading region kept `aria-busy` for ever. Each translator entry is now
judged alone, so a malformed one is dropped while its valid siblings still
render, and no scalar fact is withheld because a neighbour is malformed.

The two evidence corrections change records, not behaviour. The V2 handoff
claimed without qualification that a stranger's key is "neither honoured nor
disturbed"; the exact behaviour is that unrecognized hash keys are judged by
nothing and survive exactly as long as the route writes nothing, while every
write it does make replaces the whole fragment with the four recognized keys,
so an unrecognized key is discarded by partial-address completion, by a reader
action, and by the recovery link. Only the value-identical case is proven by
test, and the discard cases are labelled as read from the code. The V2
`AT-LIMITATION.md` also said no AT-SPI bus launcher exists; that is false, and
the accurate limitation is that no usable display, AT bus session, screen
reader, speech channel or braille stack was available, so no successful
real-assistive-technology evidence was produced. No implementation was changed
to make either statement true.

The changed paths are `src/web/browser/catena/catena.js` and
`tools/tests/test_catena_wave_1.py` alone, plus these durable records.
`catena.css` and `index.html` are byte-identical to the reviewed head and
`catena-model.js` to main. The focused suite is 249 tests green, up from 231.
The recorded ceilings are unraised and were paid for by deletion rather than by
waiver: `catena.css` is unchanged at 7,629/8,000, and `catena.js` is
12,995/13,000 whole and 8,799/8,800 comment-stripped, funded by removing a
provably dead voice lookup repeated four times, folding six per-field guards
into one typed gate, and tightening three expressions. That left no room for
the explanatory prose this file's style would ordinarily carry, so one
precondition is pinned by a test rather than a comment and the trade is
recorded as a limitation. `check-release-bindings` still fails closed on the
changed Catena route assets and was not repaired; it is the release owner's.
A new immutable handoff, `20260812T184146Z-catena-e1-corrections-v3`, records the
exact V3 head, and the V2 package is unchanged. The sole next action is a fresh
independent review of that head and package. Nothing here is accepted,
integrable, merged, re-signed, or deployed.

### E1 Catena route-owned correction lane, V4

The V3 independent review at `9b1c23680c8da6b9a83bb7fb8ca689fbf9d2004c` is
**CHANGES REQUIRED**. It accepted the shared fail-closed mechanism, the
substance of the stranger-key correction, the core AT-SPI correction and the E0
visual direction, and it found three things wrong.

**The voice classifier.** `index.held[].languages` is a language inventory, not
a voice authority. Greek stands in this corpus only as an original — the exact
source pairs are `original:grc`, `original:la`, `translation:en` and
`translation:la`, and there are zero Greek translations — so answering support
from the language inventory accepted `translation:grc` and rendered "Greek
translation — none here", a holdings claim nothing supports. V4 publishes the
exact voice keys the corpus holds as a top-level `voices` array of the catena
index, counted by the generator from the `voice` it already derives per row,
and the route judges the whole key against it. `translation:grc` now fails
closed; Genesis 10 in `translation:en` still says "none here", because that one
is true. This is the one generator/data seam the review authorised explicitly.

**The typed-presentation boundary.** Nine sinks remained: absence `author`,
`work`, `reason` and `partial` bypassed the gate; a scalar translator container
was widened into valid-looking provenance; malformed translation language
reached the voice label, the control value, the written URL and the DOM `lang`;
malformed authors collapsed into one unnamed, corpus-wide filter key;
structured extent members stringified into a locus; and a throw in the render
tail stranded `aria-busy`, focus, the tally, the announcement and the route.
They are closed as one boundary in `catena-model.js` — text, list, record, a
number as carried, and a fact that may be a finite number — asked once so the
page and the model cannot answer differently.

**The V3 package.** It published an account name, a PID, a uid, a D-Bus name
and a session-bus path while its own sanitizer reported zero hits, because
every rule knew the username only as a path component and the sanitizer shipped
its own denylist in a form invisible to its own scan. V4 replaces it with a new
sanitized immutable package whose sealer reads identities from the environment,
matches the account name on word boundaries, scans every file and every path,
and refuses to write the manifest on any hit. Run against the sealed V3
package, it refuses to seal. The V3 package is not mutated: it is evidence of a
review that happened.

`catena-model.js` changed, which the V3 lane deliberately avoided. It carries
no byte ceiling while `catena.js` had one byte of margin, and two of the nine
findings — the translated-language metadata and the structured extents — live
inside `voiceKey` and `formatExtent` and cannot be closed from the page at all.
`MODEL_SHA256` is updated deliberately and a fourth release binding is now
stale; no release record was re-signed.

Measured at the V4 head: focused suite 266 green, up from 249; full discovery
1,617 tests against the base's 1,600, with **no new failure identity**; browser
gate 2,290 assertions, 1,836 pass / 226 fail / 228 skip, its assertion set,
statuses and details equal to the base object for object; `catena.css`
unchanged at 7,629/8,000 and 2,676/2,700; `catena.js` **12,981/13,000** whole
and **8,749/8,800** stripped, both improved on V3 and neither ceiling raised.
One pre-existing failure's detail is attributable to V4: a day-reader test
forbidding any `src/web/data/` change now lists the two catena data paths the
authorised seam writes. Regenerating also restored Isaiah 8, whose chapter file
and `present` entry were missing from the committed data; the unmodified
generator at `f2c9bc49` produces the same output, so that drift predates this
lane.

E1 is **awaiting fresh independent review**. Nothing here is accepted,
integrable, merged, re-signed, or deployed, and the separately owned
generator/data, release, common-gate, B0/shared-shell and real-AT
prerequisites remain open.

### E1 Catena route-owned correction lane, V4.1

V4 completed at `e40720d5d622e8b0528b8c714cc5caee0b21cee3` and explicitly
disclosed two requirements of the V3 review it had **not** met: the refusal copy
was not made neutral, and the required screenshots were not produced. This lane
answers exactly those two and nothing else.

**The refusal copy.** The review's "Fail-closed presentation" finding accepted
the mechanism and rejected the copy, because "address could not be read" is
imprecise for a value that parsed cleanly and is merely unsupported. Three
shared strings in `renderInvalid` changed: the reference line from `Address not
recognised` to `Address not used`, the heading from `This address names what the
page does not have` to `This address cannot be used as written`, and the status
write from `The address could not be read; its invalid values are shown,
unchanged.` to `The address is unchanged; the values not used are listed.` The
old heading asserted a holdings negative over addresses refused on grammar, and
`invalid values` located the fault in the reader. The typed per-value reason is
untouched, so unsupported and malformed refusals stay distinguishable. Seven
wording pins moved and one narrow regression was added, which fails on the
previous copy. The wider non-neutral phrasing elsewhere on the page was
deliberately left alone and is raised as a scope question for the reviewer.

**The screenshots.** V4's stated reason — no display was available — was
incorrect: headless Chromium needs no display server, and the repository already
drives it over the DevTools Protocol. 53 real captures were produced from
`make public-site` artifacts at both the parent and this head, covering nine
route states at 1440x900, 393x852 and 320x852, plus forced-colors and print
emulation, with before/after pairs for the two states whose copy changed. They
prove rendering, not announcement; V4's real-AT limitation stands unsuperseded.

Measured at the V4.1 head: focused suite 267 green, the 266 inherited plus the
new regression; full discovery 1,618 tests against the base's 1,617, the extra
test being this lane's, with the 27-entry failure/error name set **identical**
under `diff`; browser gate 2,290 assertions whose whole report is deep-equal to
the base across 480,881 bytes, `generatedAt` excepted; `make -k check` exit 2
with the same three failing targets; `catena.css` byte-identical at 7,629/8,000
and 2,676/2,700; `catena.js` **12,970/13,000** whole and **8,734/8,800**
stripped, both *smaller* than V4 because the replacement copy is shorter. No
ceiling raised. Four stale release bindings, unchanged in count, none re-signed.

The `src/web/data/` contradiction is **preserved untouched** for independent
adjudication: a day-reader guard forbids every `src/web/data/` change while the
V3 review authorised exactly one. This lane wrote nothing under `src/web/data/`,
and did not weaken, delete, whitelist or expect-mark the test.

E1 remains **awaiting fresh independent review**. Nothing here is accepted,
integrable, merged, re-signed, or deployed.

### E1 Catena route-owned correction lane, V5

<!-- promised-deliverable: corpus-browser-catena-e1-corrections-v5-2026-08-14 -->

The fresh independent review of V4.1 —
`7f69575b982926e827974f2ed236b1c8bfd8aaad`, on branch
`review/catena-wave-1-e1-corrections-v4-1-independent` — recorded **CHANGES
REQUIRED** at exact candidate `f93757854b54c19e50bdcb97ca0fed9b48d22bb7`.
That disposition is this lane's starting fact, and this lane does not review
its own work: it records no acceptance of anything.

The review passed, and this lane did not reopen, the exact voice-key
projection (`original`, `translation:en`, `translation:la`, with
`translation:grc` failing closed), the neutral refusal umbrella, the recorded
budgets, the 53-image visual matrix, and the sealed V4.1 package's integrity.
It found five blocking classes, all of one kind — **malformed or unsupported
structured metadata becoming visible semantics through coercion or an
unchecked collection shape**:

1. raw language metadata rendering `lang="[object Object]"`;
2. malformed collection members creating false counts and refusals, or
   erasing valid siblings;
3. absence records discarding the generator's typed `finding` and
   manufacturing unsupported negative claims;
4. numeric, verse, path and bootstrap metadata coercing into presentation or
   leaving incomplete terminal state;
5. committed malformed-data regressions that do not prove partial-arrival or
   action route completion.

V5 answers all five behind **one record boundary**, and answers them in
`catena-model.js` rather than in the page. That placement is the whole shape
of the correction and it is deliberate: `catena.js` had thirty gzipped bytes
of margin, and a boundary bought out of thirty bytes would have been a list of
one-off guards. The model carries no ceiling, so it now owns what a *number*
of this corpus is (`whole`: a positive safe integer, refusing `true`, `"5"`,
`[5]`, `0` and a fraction alike), what a *language code* is (`tongue`, a shape
check, because `lang` is machine-read; and `voiceLanguage`, narrower still,
because a voice key becomes a URL this page must accept back from itself),
what the *members* of a collection are (`records`), and then the derivations
the page used to perform by concatenation over raw members: the canon,
chapter and paragraph addresses, the chapter's verse lines, and the absence
rows and their summary. The page only calls them, and is **smaller** for it:
8,734 → 8,363 stripped bytes.

Three findings are worth naming because they were not in the review, and were
found by writing its required regressions.

- **The harness could not see the sink the review proved.** The replay shim
  stored `element.lang` as a plain JavaScript property; the HTML DOM reflects
  it into the content attribute, stringifying whatever it is given. That is
  why real Chromium showed `lang="[object Object]"` while every committed test
  passed. The shim now reflects `lang` exactly as it already reflected `id`,
  and `inspect()` projects every language attribute under the reading region
  for every scenario — so the cross-scenario coercion sweep covers DOM
  attributes, not only text.
- **Sound text is not a language.** `sound()` passed the string `"not a
  language code"`, and the shared namer printed it back, uppercased, as a
  language. The visible language chip and the voice key are now gated on
  shape, not on non-emptiness.
- **A silent return is not a terminal state.** Beneath the throw the review
  named, `render()` had a guard that returned quietly when the controls could
  not name a book — which is exactly what a malformed canon produces. Reached
  that way it left `Loading…` standing with nothing said: the same dead end as
  the throw, invisible for the same reason. Both now reach `startFailed`.

On absence semantics the correction is narrow by design. The generator closes
`finding` at four values in `scripts/_catena.py` and says a different thing
with each — `none-published` about the world, `in-copyright` about the law,
`partial-public-domain` an offer not taken, `not-surveyed` an admission that
nobody looked. The page read none of them, classifying by whether a `partial`
string happened to be attached, so `not-surveyed` was spoken as *no English
this project may publish*: a closed claim about publishing rights,
manufactured out of an admission of ignorance. V5 classifies from the finding,
adds no fifth finding, and gives a finding it cannot read a clause that claims
nothing rather than the nearest claim it can make.

The adversarial fixture the review named is rebuilt rather than re-asserted.
Not one of its absence rows carried a `finding` at all, which is why it could
manufacture four closed negatives from four malformed neighbours; its rows now
put a real typed finding beside malformed siblings and malformed findings
beside sound ones, so the two questions are separable. Nothing was weakened to
pass: the one source-text assertion that changed —
`(index.voices || []).includes` to `list(index.voices).includes` — is the
stricter form of the same requirement, because `|| []` let a string `voices`
answer `.includes` by substring.

Fresh results at the V5 head are recorded in the roadmap subsection and in the
new immutable handoff. The focused Catena suite is **306 tests green**, up
from 267, the 39 new ones covering malformed language under Everything held,
mixed valid/malformed/scalar/null collection members, the five typed-absence
cases, numeric, verse, path and bootstrap metadata, and seven route-completion
scenarios that begin canonical — because every committed malformed scenario
began malformed, and so proved nothing about a page that had already
established a route, a history and a rendered chapter. `catena.css`,
`index.html` and every path under `src/web/data/` are byte-identical.
`catena.js` and `catena-model.js` are the only production files changed. No
ceiling is raised and no release binding is re-signed; the four stale Catena
bindings remain stale, unsigned and correctly fail-closed.

The `src/web/data/` contradiction is again **preserved untouched**. V5 wrote
nothing under `src/web/data/` and did not weaken, delete, whitelist or
expect-mark the day-reader guard. It remains a separate owner's adjudication.

The new immutable handoff is `build/agent-handoffs/20260814T123524Z-catena-e1-corrections-v5`,
sealed at the exact V5 head. It does not mutate the V4.1 package, whose digest
was re-verified byte-exact first.

E1 remains **awaiting fresh independent review**. Nothing here is accepted,
integrable, merged, re-signed, or deployed, and every separately owned
release, common-gate, B0/shared-shell, real-device/AT, protected Liturgy and
PDF prerequisite stays open with its owner.

### E1 Catena route-owned correction lane, V6

<!-- promised-deliverable: corpus-browser-catena-e1-corrections-v6-2026-08-14 -->

The disposition answered is **CHANGES REQUIRED** at exact candidate
`19982ab433dd25704ed60b1ac6ddb678bc3a98f9`, recorded by the independent review
`fa5b2f601565508acee2b1b236b0c69138af07a3` on branch
`review/catena-wave-1-e1-corrections-v5-independent`, whose evidence is
`fe71d03e51bc3a89f01b9262cd3a4d9077bb0cef` and whose package digest
`18500400ce617365ef8322e41f011f44dc5a0a88dc39fbbcb5deb1abd78b75ea` this lane
re-verified byte-exact before starting. That review is a sibling of this line
at the reviewed parent and is **not merged into it**: what follows records
implementation-lane facts only.

The review found one thing said fourteen ways, and the thing is the difference
between a SHAPE and a MEMBERSHIP. V5 validated that a value was an object and
never asked whether the object was a member of the collection it stood in, nor
whether a string was an identity this corpus had issued. So `{}` counted
itself as a work this project holds and cannot name, and refused a boundary in
Scripture's own numbering; `sources[["1"]]` resolved to `sources["1"]`, and a
one-member list took a real edition's author, rights and language for a
fragment that named no edition at all; a fragment id that was sound text
composed `../../../etc/passwd.json` and the page requested it.

Where truth was unavailable, V5 substituted rather than omitted. An unreadable
language became `en`, which tells a screen reader to read Latin commentary in
an English voice on the authority of a fallback; an unreadable testament
became "New Testament" on the authority of an `else`; and a Bible record whose
language nobody could read reached the edition control as
`Douay-Rheims ([object Object])`. Each of those is a fact about the corpus
manufactured out of a record nobody could read, and none of them is a smaller
defect than the coercion it replaced. V6 omits the unsupported claim and
preserves every valid fact beside it.

Finding selection was first-match, so the same two records listed the other
way round made a different claim about one work's rights. Findings are read as
a SET now: one recognized finding is the record speaking, two different ones
are a record contradicting itself and the page declines rather than choosing
the harsher of two claims about somebody's property. A stray `partial`
licenses nothing; only `partial-public-domain` does, in its own name.
`^[0-9]+$` admitted `"01"` beside `"1"` and `Number()` folded them together,
so verse 1 rendered twice, each row claiming to be the verse the edition
numbers 1. JSON `null` is a valid document and not an index, and read raw it
threw past the bootstrap's request catch and left `Loading…` standing for
ever; the parent still does this, reproducibly, and the unfiltered log is in
the package. One defect the review did not name was found by writing its
required regression: judged against an empty canon the page answered
"Gen is not a book of this canon", which is a claim about the canon drawn from
a parse failure.

The review's finding about the PROOFS was sharper than its finding about the
code, and it is why the test delta is larger than the correction. Three V5
oracles could not fail on the defect they were written for. The word-tally
oracle counted a deduplicated set of class names, so one chip and seven were
the same value and reverting the gate to `Number(x) > 0` left it green. The
verse oracle swept the commentary while its fixture corrupted the bible
chapter. The "nothing stale" case released its payload before navigating, so
no late work existed to reject. Eight oracles that expected the defects are
corrected in place rather than deleted, each carrying the reason. The harness
now projects the rendered verses and their numbers, the uncounted tally chips,
the edition options and their route values, the testament line, the absence
rows' own author and work, the visible failure paragraph, and a count of
parked requests actually released — which turns "nothing stale survived" from
an argument into a measurement.

Two regressions exist because a delegated lane reported its own assertions
vacuous rather than passing: opening only the safe fragment proved nothing
about six refused ids nothing had asked for. Both now ask.

The numbers are recorded as measured, each against the command and the head
that produced it. Focused Catena suite `423` at this head, exit 0, against
`306` at the parent. Replaying the V6 test file against the parent with NO
filter kills the harness on the JSON-null bootstrap — `TypeError: Cannot read
properties of null (reading 'canon')` out of `catena.js:981` — and every
`ReplayTest` class errors in `setUpClass`; that log is preserved unfiltered,
and the three-scenario filter needed to get a per-class reading is preserved
as an exact patch beside it. Filtered, the parent runs `371` and fails `71`
with `14` errors — 85 FAIL/ERROR identities across 24 distinct classes,
which decompose as `19 + 4 + 1`: 19 of the 23 classes V6 adds, 4 of the 5
pre-existing classes whose oracles V6 corrected, and the model-digest pin,
which holds no corrected oracle. The two sets do not coincide and are not
summed as though they did — an earlier draft of this paragraph said
`19 + 5 + 1`, which is 25. Four V6 classes and one corrected-oracle class
do NOT fail at the parent, and that is stated rather than rounded away:
they are the positive control over the real corpus, and oracles that read
the production sinks for behaviour V5 had already made correct. A
regression defending an earlier fix with a better instrument does not
prove this one. Full discovery
`1,774` at this head against `1,657` at the parent — `14` failures, `13`
errors and `11` skips at BOTH ends, with an identical 27-entry FAIL/ERROR
identity set. The head runs 117 more tests, so no literal count identity is
claimed; the two name files are byte-identical, which is the result being
reported rather than evidence for it, and both source logs and the extraction
script ship so it can be re-derived. Fresh browser gates at parent and head both report `2,290`
assertions — `1,836` pass, `226` fail, `228` skip — and the two reports are
**deep-equal excluding four volatile fields**, `generatedAt`, `root`,
`durationMs` and `browser`, which is stated in four because the V4.1 record
named one. `make -k check` exits `2` at the same three inherited targets as the parent —
`check-release-bindings`, `check-tool-registry` and `check-examples`. Promise ledger valid. Catena check
valid at `1,351` fragments, 1 book, 73 canon books. `catena.css` and
`index.html` are byte-identical to the parent and nothing under
`src/web/data/` changed at all.

Budgets hold unraised: `catena.css` 7,629/8,000 whole and 2,676/2,700
stripped, both unchanged; `catena.js` 12,993/13,000 whole and 8,202/8,800
stripped, the composition 161 bytes lighter than V5 left it. The boundary
moved into `catena-model.js` again, which carries no ceiling, and the
relocation is disclosed with its cost rather than presented as unchanged
load. Measured at this head against the parent: the model grows `11,171`
to `15,767` gzipped whole, `+4,596`, of which `+1,093` is composition and
`+3,503` is explanation the model carries deliberately. The two files
gzipped together grow `23,449` to `28,028`, `+4,579`; gzipped separately
and summed, `24,161` to `28,760`, `+4,599`. Both measures are given
because neither alone is the load a reader pays. The commit message of
`ee1048c90` quotes `+4,593` and `+4,576` for the first two: those were
measured before the NUL correction in `83cb63b61`, which is five source
bytes longer, and the figures above supersede them.

Four stale release bindings remain fail-closed and none was re-signed. The
`src/web/data/` test contradiction is preserved untouched for its owner, and
the two Day-reader guard failures it causes are inherited identically at the
parent. E1 remains **awaiting fresh independent review**. Nothing here is
accepted, integrable, merged, re-signed, or deployed, and every separately
owned release, common-gate, B0/shared-shell, real-device/AT, protected Liturgy
and PDF prerequisite stays open with its owner. This lane does not review its
own work.

### E1 Catena route-owned correction lane, V7

<!-- promised-deliverable: corpus-browser-catena-e1-corrections-v7-2026-08-15 -->

The disposition answered is **CHANGES REQUIRED** at exact candidate
`4639b139f2179b1fca7f9cb1e4ba3ac19c9bbc46`, recorded by the independent review
`f183ed1b0afc6f14574a3507f6eaf3102dc999fa` on branch
`review/catena-wave-1-e1-corrections-v6-independent`, whose evidence is
`ca2a8659010b3fca2ccada24f9c431796ca702b1` and whose package digest this lane
re-verified before starting. That review is a sibling of this line at the
reviewed parent and is **not merged into it**: what follows records
implementation-lane facts only.

The review's central finding is about a SHAPE, and the shape is a shallow
copy. `chapterFragments` copied every own property of the shared source record
and then of the fragment into one object, and cleared afterwards the two
fields it knew were dangerous — `text_path` only when a valid composed form
existed. Where the fragment's id or its file's prefix could not be read, the
record's own `text_path` survived the copy and `openFragment` handed it to the
real request sink. `'../../../etc/passwd'` is a string, and a string was all
the copy asked for. The wider fault is the loop above it: a shallow copy
carries whatever the data happens to hold, so the boundary has to be
re-established at every later sink, which is why V4, V5 and V6 each found one
more sink where it had not been.

V7 projects. A fragment is read into a record of known, validated fields and
nothing else crosses; there is no `joined[name] = raw[name]` left in the file.
`text_path` is COMPOSED from the file's own prefix and the fragment's own
identity. Where a spine states no prefix — the sample corpus does not — a
carried path may stand in only when it is a relative JSON file of this data
root's grammar AND its stem is that fragment's own validated id, so the one
thing it can address is the text of the fragment that carried it. All 47
sample-corpus paths satisfy that unchanged, and an injected path names some
other file by definition.

The same reading closes the other six classes. A hollow fragment makes no row
and no tally. An absence SOURCE is validated before it claims a work's row, so
a source naming neither author nor work no longer renders a blank entry while
masking the valid sibling behind it. A refusal needs the whole typed record
the projection writes — the closed kind, and the chapter matched against the
chapter being read: the reviewed fixture's one well-formed refusal states
chapter 1 and V6 printed it under Genesis 2 with the sentence interpolated to
say Genesis 2. A contradiction now contributes no prose at all, where V6
blanked the finding and then printed one side's `reason`, chosen by ranking
the two on length. `scripts/_catena.py` stops coercing `partial`:
`str(row.get("partial") or "")` turned a mapping into `"{'a': 1}"` and the
page printed it as "Partly public domain — …".

And the unreadable roots: holdings, canon, voices, the edition manifest, the
paragraph layer, the verses container and the chapter spine itself each now
distinguish *we read the corpus and found nothing* from *we could not
establish what the corpus holds*. Those are not interchangeable sentences and
every one of them was answering the first while meaning the second.

The oracles had blessed each defect, which is why the V6 suite was green while
they stood. Ten `CORRECTED ORACLE (V7)` blocks correct them in place with
their reasons recorded rather than deleted; the sharpest is the one whose own
name forbade what it pinned — `test_the_late_arrival_manufactures_no_absence_and_no_false_refusal`
asserted the false refusal. The late-work guard grew from thirteen keys to
thirty-six, because the review found it omitted the FINAL STATUS SINK: it
compared the announcement journal, which a stale write cannot shorten, rather
than the live region's current contents, which a stale write could replace.

**This lane attacked its own change three times, and every pass found real
defects in it.** The first found five. One was introduced by the
correction — a fragment could inherit its `id`, and so its Source Library href
and the one request it can cause, from its edition's shared record. Four the
correction had not reached: `paragraphPath` still fell back to a digit width
of 1, which is verbatim the code the same commit removed from `chapterPath`;
an edition's own unreadable record answered `''`, the value reserved for an
edition that publishes no layer; `chapterPath` consulted its readability flag
on only one of two exits; and a chapter spine answering 200 with `null` or a
list was read as an empty chapter.

The second pass found the same class again one level under three of those
fixes, which is the finding worth recording. The chapter PAYLOAD had been
given a third answer and its CONTENTS had not, so a spine whose `fragments` is
a record, or whose `sources` is a list, or whose `refusals` is a string, came
through as readable — and the last of those dropped Rule 4's refusal in
silence, the strongest claim this page makes, failing open. `null` had been
made the mark of an unreadable document in one place and left as the mark of a
404 in three others: the paragraph root, a paragraph file and a fragment's own
text each read a successful, unreadable 200 as "there is no such file". The
optional paragraph layer's transport failure still took down the whole
bootstrap and blamed the catena index. And two address spellings passed the
grammar and then rendered something else: `#chapter=007` showed chapter 1 and
rewrote the address to say so, and `#book=%20Ex` showed Genesis 3 and rewrote
the address to say the reader had asked for Genesis.

The third pass found eleven more, three of them introduced by the second
round's own fixes, and by then the pattern was the finding: each round had
closed a CONTAINER and left its MEMBERS, or replaced one data-comparable
sentinel and left three, or caught one optional fetch and left the one beside
it. The `sources` root was guarded and its members were not, so the voice
control still said "none here" of a chapter holding nine Latin fragments. A
`fragments` list was checked for being a list and never for yielding a
fragment, so a list of hollow members answered "Nothing held here" over a
chapter the index says holds 1,351 — trading an over-claim for a manufactured
negative. And the new absence sentinel was compared by VALUE, so a payload
carrying a key named `absent` could forge the page's own 404 and suppress the
paragraph layer of every chapter of every edition; the same forgery worked on
`unfetched`, whose payload-chosen string was printed to a reader inside the
page's own failure sentence. A sentinel a payload can carry is not one.

Beside those, four older instances of the same class: an unreadable `breaks`
member set reported as an edition that divides nothing, the optional paragraph
FILE's transport failure still taking the whole page down one scope under the
root whose failure had just been caught, the `absences` root left unguarded
while `refusals` had just been given one, and the voice key trimmed before the
grammar tier judged it so `translation:%20en` was refused as a voice this
corpus does not hold rather than as a value that is not a voice key.
`bibleRecord` was the last raw copy in the model, forty lines from the comment
saying there must not be one again, and `ident()` trimmed — so `" x"` silently
became the identity `x` and was fetched and linked as one.

All are fixed with regressions, and every one of the 562 tracked spines, 561
fixture spines and all 5,547 paragraph records still reads as readable. A new
guard asserts what the others cannot: no exported model function throws on a
hostile argument, over every export and 225 argument shapes. It found three
that did. Two confirmed findings are recorded UNFIXED. A record stating
nothing but `source` is still counted as a fragment held here, because closing
it means moving a line V6 drew and this review left standing, and V6's request
asked that exact question and got no answer. And `bibles.json` arriving
unreadable is reported as "lists no translations" — a claim about the manifest
drawn from a document nobody could read — because the sentence is composed in
`loadBibles`, which is shared-shell ownership this lane does not hold; the
route carries the truthful sentence and cannot reach it. Both are named at
their seams rather than repaired across an ownership boundary.

The evidence half of the review was about truthfulness rather than mechanism.
V6's package was mechanically intact and descriptively untrue: it named a head
it was not sealed for, said 45 sealer tests where its own log says 46, four
commits where five exist, three changed files where six exist, and sixteen
raster pairs where fifteen exist. Every one was available to a program.
`logs/derive-claims.py` now computes them and writes `claims.json` and
`DERIVED-CLAIMS.md` from one pass, so the machine-readable record and the
readable one cannot disagree; `logs/head-consistency.py` reads them back and
refuses a package whose prose names a commit it may not name, calls the head a
parent, names a path the package lacks, or leaves a member unreferenced. A
commit the package legitimately DISCUSSES must be declared with a reason;
the default is refusal.

The sealer's own two defects are fixed. `--check-only`, documented as never
rewriting a member, deleted `MANIFEST.sha256` on failure — in a mode the
package's own instructions tell a REVIEWER to run, and whose account-name
pattern the same document concedes false-hits on an ordinary English username.
And `verify()` never opened the ZIP: the tree was proved against the manifest
and the archive against its sidecar, and nothing joined them, so the artifact
a reviewer actually receives was the one whose contents nothing checked.
Writing that check immediately caught a third thing — the sealer's own test
helper built its archive in the layout the guidance forbids.

There are no screenshots, and the count is derived as zero rather than
described as none: the stylesheet and the markup are byte-identical and the
change is semantic, so a raster of a valid chapter would be identical at both
ends. What replaces them is the V7 test file replayed against the PARENT's
production files — same scenarios, same oracles, other code — with the class
decomposition derived from that log rather than asserted. Two of the classes
V7 adds do NOT fail at the parent, and they are named as what they are: one
closes a proof gap the review identified rather than a defect, and one covers
a generator correction the browser half already had right. V6's roadmap
claimed every one of its classes failed at the parent and its own shipped
decomposition contradicted it.

Budgets hold unraised. `catena.css` is unchanged. `catena.js` is SMALLER than
V6 left it in both measures, because the raw reads and the repeated guards
left with the derivations. The boundary moved into `catena-model.js` again,
which carries no ceiling, and the relocation is disclosed with its cost rather
than presented as unchanged load — both ways of measuring the two files'
combined payload, because neither alone is what a reader pays. `catena.js`
finished V6 with SEVEN gzipped bytes of margin, which is the whole of the
reason the move was not optional. The V5 and V6 reviews each asked whether
that much explanation belongs in an unbudgeted model and neither was answered;
this lane trimmed its own additions by a measured amount in a commit that says
so, and asks a third time rather than taking silence for consent.

Four stale release bindings remain fail-closed and none was re-signed. The
`src/web/data/` test contradiction is preserved untouched for its owner, and
`src/web/data/` has zero new changes: the adversarial fixtures live in the
test file and are served by the replay harness's own stub network, and no
generated file was altered to make a malformed test pass. The common-gate
failure population, `check-tool-registry` and `check-examples` are inherited,
red at both ends, and separately owned; none was worked around, whitelisted,
weakened or expect-marked.

Status: **awaiting fresh independent review.** This lane records no acceptance
of its own work, marks no separately owned prerequisite complete, and does not
review itself.

### E1 Catena route-owned correction lane, V11

<!-- promised-deliverable: corpus-browser-catena-e1-corrections-v11-2026-08-16 -->

The disposition answered is **CHANGES REQUIRED** at exact candidate
`ea15d16d22d7ceaed989ed9907c236f967738a03`, recorded by the independent
review `f7cad8b0219de8343a0b2cce95e89558ded6946e` on branch
`review/catena-wave-1-e1-corrections-v10-independent`, which independently
inspected evidence `ff49c83e4f26570bd4c07d8fc8703f94c331d92a` and verified
package `build/agent-handoffs/20260816T111714Z-catena-e1-corrections-v10`
with ZIP SHA-256
`4c71d1c15bd1f1992bf29a1d84342f11a8b671b5b5bd6bdcc4341de091e23e2f`. That
review is a sibling of this line at the reviewed head and is **not merged
in**; this record states its disposition rather than importing its commits.
Current `origin/main` is `e7f468e842727a817631d12f0854f8249556a8ff`, and
this lane is not integrated with it.

The review passed what V10 got right and did not reopen it: ordinary
normalized refusal consumption before the cache and request sink, genuine
absence distinguished from ordinary refusal, the V9 request closure, the
cold, present-valid and prewarmed terminal vectors, the representative
primitive namespace matrix, the production ownership boundaries, and the
existing CSS and JavaScript ceilings. It found five things, and this lane
answers those five and nothing else.

**The exported claim boundary closed only its shapes.** `bag()` established
that a record arrived; ordinary property lookup then answered from wherever
it found an answer. So `Object.create({stated: false, trail: ''})`
presented itself as this route's own absence and opened the carried
fallback door with `text_refused: false`, and an inherited
`{stated: true, trail: 'structure/catena/text/deeper/'}` composed a usable
text address the page never derived. Mixed own-and-inherited forms did the
same and an accessor could throw. The committed matrix was eight plain
object literals and probed no inherited, hybrid or accessor claim at all.
Every semantic member is now read once, as own data, through its property
descriptor: nothing inherited is seen, and an own accessor is **never
invoked** — so a getter with a side effect does not run, and a getter that
would answer differently on a second read has no second read to disagree
with. Where the claim's own three-member contract is partly written above
it — a valid own statement beside an inherited refusal marker — the claim
fails closed rather than being adjudicated, because deciding which half of
a contradiction to believe is not this page's to do. The same own-data
reading now applies to the spine's own `text_prefix`, the carried
`text_path`, the fragment's `id` and `source`, the edition join, and the
extent members. This is a boundary correction, not a security rewrite: the
wide fragment and edition contracts are still validated field by field, and
that limit is stated in the handoff.

**One sentence was doing the work of two.** `A text reference was supplied
for this fragment, but it cannot be used as written` asserts two facts of
its own — that a reference was supplied, and that it was written unusably —
and V10 gave it to every state that resolved no text. A spine whose
`text_prefix` was `null`, a record, a list, a number, a flag, `''` or
whitespace establishes neither; nor does a bare, contradictory, inherited or
accessor-backed direct claim. The projected claim now carries `said` —
whether a non-empty textual value was supplied at all — and the weaker
state gets the weaker sentence: `No text reference is established for this
fragment, so no text is shown.` It makes no holdings claim, no
file-existence claim, no request-failure claim and no accusation; it does
not say a reference was supplied, and it does not say how anything was
written. The two supplied-and-refused states — a real `structure/paragraphs/`
prefix, and the right namespace wrapped in whitespace — keep the stronger
sentence, because for them it is true. The model chooses and the row
carries the result, because `catena.js` stood at 13 gzipped bytes of
ceiling and this file has none; the page's whole diff is one line, and its
whole-file headroom improves to 20 bytes.

**The proof had three holes, and they are pinned shut.** A fourteen-case
inherited and accessor matrix drives the exported boundary and pins that no
such claim creates a request, reopens the carried door, composes a text
path, changes the refusal or absence state, renders body text or alters
ownership — and asserts the planted accessors were invoked **zero** times,
which is stronger than reading them once and trusting the answer. The
ordinary absent, valid and refused dispositions are asserted beside it as
positive controls, and the projection is asserted to carry only own data
properties. Every unestablished prefix is driven to the **visible and the
request sink**, against the same planted carried body the V9 family uses:
the V10 neutrality test blacklisted nine phrases inside the constant and
drove no state anywhere. The genuinely-late terminal vector now states an
expected value for **all 36** guarded fields rather than 13 of them, at
both ends of the release, and a coverage test fails the moment a field
joins the guard without joining the proof; the release is pinned as the one
thing permitted to move, named by sequence and address. A `forceRow` hook
pins the renderer's before-the-sink ordering with the normalized
`{text_refused: true, text_path: <usable>}` row the model never emits,
against a control that really does fetch — the V10 review's point being
that moving the check below `fragmentText()` changed no journal and left
all 466 wave-1 methods green.

**The packaged evidence could not reproduce its own ownership claim.** The
live harness recorded it and the dump threw it away: a fourteen-name
whitelist kept the flat path list and dropped `requests`, `fragmentIds`,
`historyState` and `replacedStates`. The journal row is now the five facts
a reader needs without the harness — sequence, address, the kind of record
that address holds, the step that owned the request, and what became of it:
completed, held while parked, released once let go, or failed — printed as
a human-readable table beside the JSON, and a name the harness stops
emitting is now a hard failure instead of a silent `null`.

**The package protocol was corrected where the review found it false.** The
P8 verifier no longer imports or executes any Python extracted from the
reviewed ZIP; it runs three tools from a trusted out-of-archive anchor,
records each tool's trusted and shipped SHA-256, and fails hard on
divergence rather than trusting the archive to audit itself. It recomputes
the ZIP size and SHA-256 after every check and states pre-check and
post-check values with an explicit equality verdict, closing the V10
finding that P8 performed no final rehash; its escaping-path refusal is now
a typed signal rather than a substring match on English prose. Provenance
is read per command rather than once per battery, so a step that dirties
the tree is recorded dirty on its own row instead of inheriting a
preflight's `clean`. Log identity is allocated from an append-only attempt
ledger outside the log directory, so a rerun cannot reproduce a previous
attempt's filenames; a log index is derived mechanically; the final
assembly writes an outer invocation log; the gate comparison is a recorded
step; and every failure path marks the abandoned attempt non-authoritative
with exactly one reason, so one attempt is one disposition. ZIP entries are
written with a fixed DOS-epoch timestamp and suffix-derived mode bits, so
the archive no longer discloses the builder's UTC offset or umask. The
sanitizer gained rules for the workspace and lane-evidence path
conventions — a reusable shape, not a V11-specific literal — and rewrites a
local-offset timestamp to its UTC instant so ordering and elapsed time
survive while the offset does not; one prior test that pinned the leak as
correct behaviour is corrected and says so. A new handoff-inventory tool
checks `HANDOFF.md` against the ten required contents of
`guidance/external-review-handoffs.md` and reproduces the review's finding
against the V10 package unaided.

Fresh validation at this head. Focused Catena is **534** green, up from
522. `scripts/_catena.py check` passes at 1,351 fragments / 1 book / 73
canon entries. Full discovery is **1,885** tests with the inherited 14
failures / 13 errors / 11 skips and the same 27-entry identity set, none of
them a Catena identity. The browser gate is 2,290 assertions, 1,836 / 226 /
228 across 171 pages and 19 routes — identical to the V10 report.
`make -k check` exits 2 on **the same four targets at the parent and at
this head** — `check-web-editions-current`, `check-release-bindings`,
`check-tool-registry` and `check-examples` — measured at both endpoints;
all four are inherited, and the V10 package's claim that the web-edition
target was additional at its head was wrong and is not repeated here.
Budgets unraised: `catena.css` byte-identical at 7,629/8,000 whole and
2,676/2,700 stripped; `catena.js` **12,980**/13,000 whole and 7,554/8,800
stripped — the page's code got smaller, not larger. The unbudgeted model
grows 29,741 to 32,406 gzipped whole and 7,664 to 7,973 stripped;
disclosed, not presented as unchanged load, and the standing question of
whether the model and the combined route payload need a governed ceiling
remains the budget owner's. Four stale release bindings remain fail-closed
and unsigned, none re-signed; `src/web/data/` has zero changes.

One measurement caution is recorded because it nearly became a false
figure: running full discovery concurrently with `make -k check` reports
250 errors rather than 13, because the make target builds and then removes
`build/.web-current` and the public site underneath the tests. The batteries
run them in sequence; the 1,885 / 14 / 13 / 11 figure above is from an
isolated run, and the raced run is not used for any claim.

Every other blocker remains open and untouched, as the V10 review left it:
projection not yet the sole semantic source beyond this inherited-claim
boundary; orphan raw sources; source-only fragments still counting; scalar
and nested translator coercion; malformed and padded absence findings;
refusal verse validation; the broader partial-selection ordering defects;
unreadable roots and the unreadable `bibles.json` prose; the broader
terminal and corrected-oracle proofs outside this lane's vectors; the
CLI/web duplicated semantic model; the uncapped combined and model payload
question, answered here only by accurate disclosure; and the historical
data-seam contradiction. Release bindings, the common gate, B0/shared
shell, real-device and assistive-technology evidence, protected Liturgy and
PDFs remain separately owned. E1 is not integrated.

Status: **awaiting fresh independent review** of the exact V11 head and its
immutable handoff archived on `evidence/catena-e1-corrections-v11-handoff`.
This lane records no acceptance of its own work, marks no separately owned
prerequisite complete, and does not review itself.

### E1 Catena route-owned correction lane, V11 independent review

Disposition: **CHANGES REQUIRED** for exact candidate
`0255b84996e1dc24da3ce75ac318c4f774b7957c`. Its actual Git parent is
`3b93f74f032e74de9a50c1e2f1b35aa5b567f8d8`; the V10 head and reviewed
baseline from which the two-commit V11 range starts is
`ea15d16d22d7ceaed989ed9907c236f967738a03`. This review addresses V10
independent review `f7cad8b0219de8343a0b2cce95e89558ded6946e`, inspected
`evidence/catena-e1-corrections-v11-handoff` at
`0ec8cae646f0e3e60c76635b88e51439c7146796`, and verified the final package
`build/agent-handoffs/20260816T172726Z-catena-e1-corrections-v11` and its
4,462,009-byte, 95-member ZIP with SHA-256
`00e93c0f539a7928281912038f135b44666aebb84af4249cb906f54238cae257`.
The review branch is
`review/catena-wave-1-e1-corrections-v11-independent`.

Current `origin/main` is
`549bf0790503bd873dd8ce6ea0a64cc34f91271d`. Its merge base with the
candidate is `9b9ff74a77d1bcd7d454d2a7fc448b8a6c8f1fd4`, with ten main-only and 35
candidate-only commits. Main has 250 divergent paths and the candidate 13;
only `PROJECT-WORK.md` and `promised-deliverables.toml` overlap, no Catena
source or test path overlaps, and a no-write merge-tree check found no
conflict. No integrated tree was built or tested. The exact reviewed V11
range is two commits and seven paths, 1,208 insertions / 47 deletions: four
durable records, `catena-model.js`, one line in `catena.js`, and the Catena
wave-1 test. It changes no generated or source data, release binding, common
gate, shared shell, Liturgy, PDF, CLI, CSS, ceiling, merge, re-signing,
deployment, or cutover path.

The inherited/accessor closure is not complete. First,
`chapterFragments()` reads the spine's `text_prefix` through `ownData`, but
treats an inherited valid prefix as if the spine had stated genuine absence.
The committed test explicitly equates that polluted record with ordinary
absence, so an own-stem carried `text_path` reopens and reaches
`fragmentText()`, the cache, and `T.loadJSON`. This contradicts the required
own-absence-plus-inherited-trail result: zero request, fallback, or body.
Second, `ownContract()` checks only `stated`, `said`, and `trail` on
`Object.prototype`. With `Object.prototype.text_refused = true`, an otherwise
own-valid claim still projects the composed path
`structure/catena/text/deeper/fallback-owned.json` with
`text_refused: false`, so the exact own-valid-plus-inherited-refusal-marker
combination also reaches the request sink. Third, the carried `text_path` is
descriptor-read once for its own-stem suffix check and again for use. A
drifting `getOwnPropertyDescriptor` trap can therefore validate
`fallback-owned.json` first and return `other.json` second; the unchecked
second path is projected with two descriptor reads and `text_refused: false`.
These are implementation defects, not evidence qualifications.

Ordinary accessors on the claimed prefix, id, source, carried path, edition
join, and extent members are not invoked; the adversarial counters remain
zero. The projected row and nested extent are normal objects whose projected
members are own data properties, and the renderer consumes the projected row
and returns on `text_refused` before its request sink. Those facts pass, but
the twice-read path means the request-critical input is not one stable
read-once snapshot. Broader raw `fragments`, `sources`, translators, voices,
and absence rescans remain the explicitly open projection/translator blockers
rather than being accepted here. The fail-closed prototype-pollution design is
**acceptable**: inherited semantic input is untrusted, ordinary JSON records
are unaffected, and a contaminated contract should resolve to one conservative
malformed state. V11 simply does not apply that policy to all combinations this
review was required to test.

The three reader-facing text states themselves pass. Genuine absence says the
fragment carries no text file; an own non-empty textual reference refused by
the namespace contract says it was supplied but cannot be used as written;
and malformed or unestablished input says no text reference is established.
The seven production-malformed prefix shapes reach the visible and request
sinks with no planted body. The ordinary ABSENT / PRESENT+VALID /
PRESENT+INVALID controls, the cold refused, present-valid, and prewarmed
refusal vectors, the V9 request closure, the primitive namespace matrix, and
the renderer's refused-plus-usable-path ordering regression all pass. The two
inherited contradictions above prevent this from being the required complete
contradictory-state closure.

The genuinely-late proof passes. Its expected table and guard both contain
exactly these 36 fields: `hash`, `hashWrites`, `replaced`, `statusWrites`,
`statusText`, `tallyText`, `busy`, `activeElement`, `referenceText`,
`selectValues`, `fragmentCount`, `fragmentIds`, `fragmentTexts`,
`errorSections`, `sectionHeadings`, `failureText`, `notices`, `dataStates`,
`asideNotes`, `refusalCount`, `refusal`, `absenceSummary`, `absenceReasons`,
`absencePartials`, `paragraphNote`, `chapterCounts`, `verseNumbers`, `leads`,
`blocked`, `voice`, `voiceLabels`, `stepButtons`, `classes`, `langAttributes`,
`acknowledgements`, and `authorGroups`. Every field is exact-pinned before and
after, guard/expected coverage equality is enforced, A is held while B settles,
the release is exactly `0 -> 1`, and only the named release may move. The four
additional ownership fields — `fetched`, `requests`, `replacedStates`, and
`historyState` — are retained in the terminal evidence. The packaged request
journal independently carries sequence, address, kind, owner, and outcome,
including held and released rows; its ownership claim is sufficient.

The P8 and byte-level package mechanisms pass. Trusted external copies, bound
by digest to the shipped tools, inspect archive code only as bytes; the ZIP is
not changed, and the post-check byte count and SHA-256 exactly equal the
pre-check values. The package has one safe root, 95 unique regular members,
94 manifest rows covering every other member, 90 frozen plus five derived
members, valid CRCs, 6,937,913 uncompressed bytes, and exact central-directory
and EOCD arithmetic with no trailing bytes. All entries use the fixed DOS
epoch, empty extra/comment fields, suffix-derived modes (83 at 0644 and 12 at
0755), and no builder offset. Text and binary inspection found 206 blobs: 142
valid UTF-8 text blobs and 64 binary blobs, with zero NUL or forbidden-control
findings. The package, sidecars, P8 transcript, filenames, logs, provenance,
and all 31 PNGs pass the workspace/session and supplemental privacy scans; the
PNGs contain no ancillary metadata.

The final package's authority and attempt protocol do not pass. Its enumerated
`logs/attempts.json` calls superseded attempt
`package-20260816T172114Z-07835xnr` authoritative and final attempt
`package-20260816T172726Z-08vvjhkw` unresolved, with only the final attempt's
P1 row frozen. `checks.txt` repeats that no terminal row is present, while the
outer assembly log calls the final attempt authoritative and the sibling
supersession marker says not to review the earlier package. `PROVENANCE.md`
claims every attempt has one terminal disposition and calls the superseded
attempt the survivor. The two browser `.log` members are empty, repeated
assembly attempts reuse `logs/gate-comparison.log` and
`logs/sealer-tests.log`, and the four discarded attempts' claimed partial
directories and self-markers are not preserved in the evidence tree. Thus
unique, non-overwriting attempt evidence and one noncontradictory terminal
authority are still absent even though the head/parent battery rows correctly
record their contemporaneous clean/dirty states. The earlier package is
properly marked superseded outside itself; the final package repeats the
authority contradiction its marker says it corrected.

`HANDOFF.md` contains all ten required contents. The 31 screenshots are
structurally sound and truthfully show the absence, supplied-refusal,
unestablished, and present-valid states at desktop and mobile sizes; six of
eight before/after pairs are correctly reported byte-identical and only the
two unestablished pairs differ. Print, no-JavaScript, and keyboard-focus PNGs
are not required for this bounded no-HTML/no-CSS correction: those properties
remain objective gate requirements, not mandatory raster classes here. The
captures bind the production commit `3b93f74f...`, not the record-only final
head `0255b849...`; that limitation is disclosed and the browser-loaded files
are byte-identical. Four narrower route screenshots described as default
arrival actually show mid-chapter scroll, so they do not evidence the shell at
those viewports; this qualification is not the reason for the disposition.

Independent validation on the exact head produced 534/534 focused Catena
tests and `catena valid: fragments=1351 books=1 canon=73`. The built browser
gate reproduced 2,290 assertions at 1,836 pass / 226 fail / 228 skip over 171
pages and 19 routes. `make -k check` exited 2 on the same four inherited red
targets as the package and parent: `check-web-editions-current`,
`check-release-bindings`, `check-tool-registry`, and `check-examples`.
Sandboxed full discovery executed 1,823 tests with 19 failures / 26 errors / 11
skips; relative to the sealed isolated 1,885-test run, the extra five failures
and thirteen class errors and the 62 unexecuted methods came from localhost
bind `EPERM`. The affected browser-citation module passed 44/44 when rerun
outside that restriction. The authoritative isolated head and baseline remain
1,885 tests with the same inherited 14 failures / 13 errors / 11 skips and no
Catena identity. The promise ledger is valid at 36 tracked / 19 complete, and
four Catena release bindings remain stale and unsigned.

Budgets remain unraised: `catena.css` is 7,629/8,000 whole and 2,676/2,700
stripped; `catena.js` is 12,980/13,000 whole and 7,554/8,800 stripped. The
unbudgeted model is 32,406 whole and 7,973 stripped; model and combined-route
budget governance remains open. No V11-caused regression or ownership
expansion was found.

The broader blockers remain open and are not reasons for this disposition:
projection is not the sole semantic source; orphan raw sources manufacture
voices and absence rows; source-only fragments count; scalar and nested
translator coercion; malformed and padded absence findings; refusal is not a
whole typed member and five kind-dependent verse shapes are unchecked; broader
partial selection and its NUL-delimited ordering key; unreadable roots, empty
layers, missing verses, the shared-verse negative, and unreadable
`bibles.json` prose; complete terminal vectors and corrected-oracle proof
outside this lane; CLI/web semantic duplication; model/combined payload budget
governance; the historical data-seam contradiction; four stale release
bindings; common-gate nested-main and target-size work; B0/shared shell;
real-device/AT evidence; protected Liturgy; PDFs; and cumulative-history
reconciliation. E1 remains off main.

Exact next action: start one bounded V12 from exact V11 head
`0255b84996e1dc24da3ce75ac318c4f774b7957c`. Treat an inherited spine prefix
and an inherited refusal marker as contaminated fail-closed state; snapshot a
carried path once and use that same value for validation and projection; add
production request/cache/body/ownership regressions for both inherited
combinations and the drifting descriptor. Then issue a fresh immutable package
that supersedes both V11 packages, contains its own terminal authoritative
attempt row, uses attempt-root-qualified unique logs, preserves every discarded
attempt and marker or retracts the claim, accurately scopes `checks.txt` and
the browser JSON/log transcript roles, and mechanically rejects cross-record
authority disagreement. Return the exact corrected head and package for fresh
independent review. Do not enter another E1 blocker, integrate, merge, re-sign,
deploy, or cut over.

### E1 Catena route-owned correction lane, V10

<!-- promised-deliverable: corpus-browser-catena-e1-corrections-v10-2026-08-16 -->

The disposition answered is **CHANGES REQUIRED** at exact candidate
`3c5b78249193df065c4e1c2ee5a98e5989c6e582`, recorded by the independent review
`55df5c236a1dfda12bb974efdbb9f46d0aeb3436` on branch
`review/catena-wave-1-e1-corrections-v9-independent` with published review
head `4f00e04bdd1fd63702a51bfdafef256b468bef77`, which independently
inspected evidence `eb1ee9987425339c2b5522987bee1fb862cd7d33` and verified
package `build/agent-handoffs/20260816T044924Z-catena-e1-corrections-v9`
with ZIP SHA-256
`4872b04ed47873d84e5a8090aff42d3e43b7a2c11653484d659205db5488d945`. That
review is a sibling of this line at the reviewed parent and is **not merged
into it**: what follows records implementation-lane facts only.

The review passed the V9 request-layer closure entire — three-state
composition through the request decision, the carried door opened only on
genuine absence, the exact V8 escape closed cold, prewarmed and late, the
thirteen-shape matrix, the primitive namespace regressions, ownership
boundaries and budgets — and found the third state stopped at the model:
`text_refused` was projected and no production consumer read it, so
`catena.js` sent the refused row's empty path through the same `ABSENT`
sentinel as genuine absence and told the reader the fragment `carries no
text file` — false of a fragment whose spine stated a text reference this
page declined, and doubly false prewarmed, where the reviewer's exact
carried file had already been fetched. Beside it the review found the
exported claim boundary accepted the contradictory
`{stated: false, trail: <valid>}` as absence; the cold, prewarmed, late and
present-valid terminal proofs materially incomplete — a focus assertion
anchored to a scenario whose own focus was unpinned, a filtered journal
slice a substitute request could pass, a control asserting only request and
body, a late guard comparing B's terminal state only to itself,
`history.state` uncaptured, ownership inferred from counts — and the V9
package protocol still short: overwritten `request-journals` logs,
provenance asserted only in prose after the fact, a P8 transcript that
never names the ZIP it verified, stale V8 labels, a collapsed parent
decomposition, an assembler that deletes rather than refuses, and the
required handoff and review-request structure missing. One exact next
action: render the distinct refused state, fail contradictory claims
closed, exact-pin the four terminal vectors, and rebuild the protocol in a
new timestamp. This lane is that correction and nothing else.

The refusal now reaches the reader. The page consumes `fragment.text_refused`
before the request sink — never inferring refusal from raw input — and a
refused row renders one neutral sentence, stated once in the unbudgeted
model as `TEXT_REFUSED`: `A text reference was supplied for this fragment,
but it cannot be used as written, so no text is shown.` It claims only what
the refusal establishes — not that the corpus lacks the text, the file is
missing, a request failed, or anything is blocked — and because it is
consumed before the sink, no path, carried, cached, or late, may answer it.
Genuine absence keeps its own sentence and its carried door; a valid prefix
still composes its own byte-exact address and renders its body; the two
no-text sentences are pinned as visibly distinct claims with a positive
control each way. The exported claim boundary is closed with it: absence at
`fragmentRow` is exactly one shape, `{stated: false, trail: ''}`, and every
contradictory or malformed direct claim — the review's exact shape included
— resolves no text and projects as refused, so no contradictory pairing can
compose a request, substitute a cached body, or leak body text.

The four terminal vectors are pinned to expected values, not to each other.
The replay journals every request with its sequence and owning step and
captures every `replaceState` state argument and the standing
`history.state` — the sink the review found uncaptured. Cold,
present-valid, prewarmed, and genuinely-late each pin the whole owned
journal, row identity and count, the refused or composed body with the
absence sentence proven absent where refusal stands, tally, the
announcement journal and the standing `statusText`, `aria-busy`, hash and
history journals and `history.state`, focus pinned to its own expected
value, and the error and failure sinks. The late vector pins B's complete
terminal baseline before AND after the release, retains the full 36-field
guarded comparison, and pins the release at exactly zero-then-one. Driven
against the uncorrected parent, the V10 file runs 466 wave-1 tests and
yields nine failing subtest identities across seven behavioral methods —
the two V10 presentation methods, the upgraded V8 terminal-claim method,
the upgraded unsafe-prefix method, and the upgraded V9 cold (two
scenarios), prewarmed, and late (two snapshots) vectors — beside the
model-digest frozen-contract pin; the neutrality sweep and the
present-valid, genuine-absence, and late-non-vacuity controls pass at the
parent, stated so because a collapsed count was one of the review's label
findings.

The package protocol is corrected in the pipeline this lane will seal with,
not by patching prose: every battery entry writes a unique indexed log and
an existing target is refused, never overwritten, with discarded runs
keeping their own marked rows; the battery ledgers emit exact-SHA,
clean-tree and sanitized-cwd provenance contemporaneously at preflight and
postflight as execution happens; the assembler refuses a reused timestamp
outright; the P8 read-only transcript binds itself to the exact ZIP
basename, byte size and SHA-256, adds independent duplicate-row checks, and
derives the member partition and final byte totals from the ZIP alone; and
the claims deriver carries accurate lane labels with the parent
decomposition reported as methods run, controls passing, and failing
subtest identities. The handoff will carry all ten protocol items and a
review request structured as Blockers and Optional feedback, naming the
superseded V9 package.

Fresh figures at this head: focused Catena suite 522 (V9: 519), all green;
`scripts/_catena.py check` passes at 1,351 fragments / 1 book / 73 canon
entries; full discovery 1,873 tests (V9: 1,870, plus the three V10
presentation methods) with the inherited 14 failures / 13 errors / 11
skips and the same 27-entry name set; browser gate 2,290 assertions,
1,836 / 226 / 228 across 171 pages and 19 routes; `make -k check` fails on
the same three inherited targets before this record and additionally on
`check-web-editions-current` after it, because this durable-record edit
makes its derived web editions stale; promise ledger valid at 35 tracked /
19 complete. Budgets unraised: `catena.css` byte-identical at 7,629/8,000
whole and 2,676/2,700 stripped; `catena.js` 12,987/13,000 whole and
7,565/8,800 stripped — the refusal's consumption paid inside the margin,
86 gzipped bytes whole. The unbudgeted model grows 29,179 to 29,741
gzipped whole and 7,571 to 7,664 stripped, so the two files' combined
payload is 42,728 summed and 42,010 one-stream against V9's 42,080 and
41,392 — disclosed, not presented as unchanged load. Four stale release
bindings remain fail-closed, none re-signed; `src/web/data/` has zero
changes.

Every other blocker remains open and untouched here, recorded as the V9
review left it: projection not yet the sole semantic source; orphan raw
sources; source-only fragments still counting; scalar and nested translator
coercion; malformed and padded absence findings; refusal verse validation;
the broader partial-selection ordering defects; unreadable roots and the
unreadable `bibles.json` prose; the broader terminal and corrected-oracle
proofs outside this lane's four vectors; the CLI/web duplicated semantic
model; the uncapped combined and model payload question, answered here only
by accurate disclosure; and the historical data-seam contradiction. Release
bindings, the common gate, B0/shared shell, real-device/AT evidence,
protected Liturgy and PDFs remain separately owned.

Status: **awaiting fresh independent review** of the exact V10 head and its
immutable handoff archived on `evidence/catena-e1-corrections-v10-handoff`.
This lane records no acceptance of its own work, marks no separately owned
prerequisite complete, and does not review itself.

### E1 Catena route-owned correction lane, V9

<!-- promised-deliverable: corpus-browser-catena-e1-corrections-v9-2026-08-16 -->

The disposition answered is **CHANGES REQUIRED** at exact candidate
`7e4df42a21bc2be2d28ff14943f63af3e7e3a6f8`, recorded by the independent review
`611b5eed8128ad5f84f6bf73ac9f9ead5959ab7f` on branch
`review/catena-wave-1-e1-corrections-v8-independent`, which independently
inspected evidence `60122b472c3f9a09aff5f8663eb3b062c585a557` and verified
package `build/agent-handoffs/20260816T011521Z-catena-e1-corrections-v8` with
ZIP SHA-256
`002a75d587a3535d7df9d2b3239d71d811cc7948e9d219e5d9118edcb21e4ff7`. That
review is a sibling of this line at the reviewed parent and is **not merged
into it**: what follows records implementation-lane facts only.

The review passed every isolated V8 namespace case and found the COMPOSED
rule open: `textTrail` maps a prefix the file never stated and a prefix the
file stated and the page refused to the same `''`, and `fragmentRow`'s
`prefix ?` read that one `''` as leave to consult the carried `text_path` —
so a refused `structure/paragraphs/` prefix still fetched the valid
same-stem `structure/catena/text/fallback-owned.json` it carried and
rendered its planted body as an ordinary success. The review also found the
package's machine inventory was not a record of the final sealed bytes —
`claims.json` understated the final uncompressed total by 1,822 bytes with
five stale member rows — and gave one exact next action: preserve the
absent / valid / present-invalid distinction, permit a carried path only on
genuine absence, prove it cold, prewarmed and late at the production sinks
with complete terminal assertions, and rebuild a truthful immutable
package. This lane is that correction and nothing else.

The prefix is now a statement, not a string. `chapterFragments` derives
`{stated, trail}` — `stated` is property presence on the spine record
itself, so `null`, a record, a list, a number, a flag, `''`, whitespace and
a wrong namespace are each a statement this page refused, never an absence
— and `fragmentRow` re-asks both members, composes from a valid statement,
opens the carried door only on `stated === false`, and keeps the refusal on
the row as `text_refused`. A refused statement is terminal: no composed
request, no carried fallback, no rewrite, no claim beyond the truthful
no-text row. `catena.js` is untouched; the decision closes inside the model
before projection completes.

The regressions drive the reviewer's exact vector at the real sinks and
fail nine ways at the uncorrected parent. Cold, the whole fetched journal
is pinned to the bootstrap and the planted body reaches no sink, with every
terminal projection asserted — rows, tally, the announcement journal AND
the standing `statusText` the review found unasserted, `aria-busy`, hash,
history, `activeElement`, error and failure sinks. Prewarmed, a body
legitimately cached under genuine absence is neither substituted into the
refused route nor re-requested by it. Genuinely late, a held carried
resolution released only after the refused route settled terminal moves no
guarded projection, and the release is proved to have happened. Both doors
the closure must not close are pinned from their own side: genuine absence
still opens the carried path, and a valid prefix composes its own address
while a planted body at the carried address goes unasked. A model-level
classification matrix drives the exported `chapterFragments` through
thirteen refused shapes, the absent state and the valid state.

The package correction is answered in the sealing protocol, not by patching
rows: the member inventory is frozen before derivation; members written at
or after derivation are named, never sized or hashed; claimed rows and
derived members partition the member set exactly; the manifest is written
after the last member write; the archive digest and byte size live only in
the external sidecar; and a read-only post-seal verification re-derives
member list, sizes, totals, manifest and archive digest from the final ZIP
alone. The provenance ledger explicitly records the retained clean
exact-SHA parent run and the `/tmp` run the V8 lane discarded for its
environment-caused `pdf-review.test` failure, which is used in no
comparison or claim.

Fresh figures at this head: focused Catena suite 519 (V8: 510), all green;
`scripts/_catena.py check` passes at 1,351 fragments / 1 book / 73 canon
entries; full discovery 1,870 tests with the same inherited 14 failures /
13 errors / 11 skips and the same 27-entry name set; browser gate 2,290
assertions, 1,836 / 226 / 228, the whole report identical to the reviewed
V8 baseline including the 117/82/27 identity; `make -k check` fails on the
same three inherited targets; promise ledger valid; budgets unraised and
unmoved — `catena.css` 7,629/8,000 whole and 2,676/2,700 stripped,
`catena.js` 12,901/13,000 whole and 7,530/8,800 stripped, both
byte-identical to the reviewed head. The closure lives in
`catena-model.js`, which carries no ceiling: gzipped it grows 28,346 to
29,179 whole and 7,485 to 7,571 stripped, so the two files' combined
payload is 42,080 gzipped against V8's 41,247 — disclosed, as the review
requires, rather than presented as unchanged load. Four stale release
bindings remain fail-closed, none re-signed; `src/web/data/` has zero
changes.

Every other V7 finding remains open and untouched here, recorded as the V8
review left it: projection not yet the sole semantic source (orphan
sources, scalar-translator coercion); source-only fragments still counting;
absence members manufacturing rows and suppressing valid siblings; partial
selection neither closed nor order-independent beyond this prefix
composition; refusal verse validation; unreadable roots and the unreadable
`bibles.json` prose; the broader terminal and corrected-oracle proofs; the
CLI/web duplicated semantic model; and the uncapped combined route payload
question, answered here only by accurate disclosure. Release bindings, the
common gate, B0/shared shell, real-device/AT evidence, protected Liturgy
and PDFs remain separately owned.

Status: **awaiting fresh independent review** of the exact V9 head and its
immutable handoff archived on `evidence/catena-e1-corrections-v9-handoff`.
This lane records no acceptance of its own work, marks no separately owned
prerequisite complete, and does not review itself.

### E1 Catena route-owned correction lane, V8

<!-- promised-deliverable: corpus-browser-catena-e1-corrections-v8-2026-08-15 -->

The disposition answered is **CHANGES REQUIRED** at exact candidate
`e876b29e5797edcc6e86422daa807f4b1104ec81`, recorded by the independent review
`d9ad5ec1ae35c308a0da5ed3456fd05fdad97cbd` on branch
`review/catena-wave-1-e1-corrections-v7-independent`, which independently
inspected evidence `92c88ab8c2d2b671009e8cf9f36aa5dd352f9b61` and verified
package `build/agent-handoffs/20260815T174121Z-catena-e1-corrections-v7` with
ZIP SHA-256
`823ac17da5f0c0f79e11688f088638d73a453ecd4adb58cf46dcac01c275a5b8`. That
review is a sibling of this line at the reviewed parent and is **not merged
into it**: what follows records implementation-lane facts only.

The review enumerated ten required production corrections, an architecture
and combined-payload judgment, and a package-truthfulness correction, and
gave **one exact next action**: start one V8 correction from the exact
reviewed head and make its first bounded commit only the text namespace
closure — byte-exact `structure/catena/text/` for both prefix and fallback
paths, with same-stem wrong-namespace production request-sink regressions.
This lane is that commit and nothing else, and it stops there deliberately:
the review's continuation into the other enumerated blockers belongs to the
next authorized pass, not to a micro-lane that would widen its own diff.

The defect was a namespace nobody had stated. `trail` and `leaf` say what a
path of this data root looks like; nothing said which directory this route
owns, so a `text_prefix` of `structure/paragraphs/` composed and requested
another namespace's file, a carried
`structure/paragraphs/text/<same-id>.json` — same identity-looking tail,
wrong namespace — passed the same-stem check and fetched a real Sources text
sharing that id, and whitespace around either was trimmed into validity. The
model now states the namespace once — `TEXT_HOME`, byte-exact
`structure/catena/text/` — and `textTrail`/`textLeaf` require it at a
directory boundary with no whitespace repair, for the composed and the
carried form alike, before projection completes. An address outside the owned
namespace becomes no request, no fallback, no rewritten path and no claim:
the row stands and says it carries no text file, which is the truth about it.
`catena.js` is untouched.

The regressions are driven at the real sink. Three adversarial replay
scenarios — the reviewer's prefix vector, the padded right-namespace prefix,
and a ten-way carried matrix (same-stem `structure/paragraphs/text/`,
sibling, parent, root, other-corpus, traversal in and out, absolute,
`structure/catena/textual/` boundary spoof, padded) — each plant a real text
body at the wrong-namespace address, so a leak would be served and rendered
rather than quietly 404ing. Each pins the entire fetched journal, asserts
the planted words appear at no sink, and holds the terminal state: `aria-busy`
released, status written once, no error section, no history write, nothing
replaced, no stale substitution. The adversarial paths are test fixtures
stamped as such; the production corpus emits exactly one prefix,
`structure/catena/text/`, and no hostile path — demonstrated, not assumed.

Fresh figures at this head: focused Catena suite 510 (V7: 505), all green;
`scripts/_catena.py check` passes at 1,351 fragments / 1 book / 73 canon
entries, so all 1,356 real text paths and all 47 fixture carried paths stand
unchanged; full discovery 1,861 tests with the same 14 failures / 13 errors /
11 skips and the same 27-entry inherited name set; browser gate 2,290
assertions, 1,836 / 226 / 228 with the same inherited 117/82/27 failure
identity; `make -k check` exit and failing-target set unchanged; promise
ledger valid; budgets unraised and unmoved — `catena.css` 7,629/8,000 whole
and 2,676/2,700 stripped, `catena.js` 12,901/13,000 whole and 7,530/8,800
stripped, both byte-identical to the reviewed head. The closure lives in
`catena-model.js`, which carries no ceiling: gzipped it grows 27,832 to
28,346 whole and 7,385 to 7,485 stripped, so the two files' combined payload
is 41,247 gzipped against V7's 40,733 — disclosed, as the review requires,
rather than presented as unchanged load. Four stale release bindings remain
fail-closed, none re-signed; `src/web/data/` has zero changes.

Every other V7 finding remains open and untouched here, recorded as the
review left it: projection not yet the sole semantic source (orphan sources,
scalar-translator coercion); source-only fragments still counting; absence
members manufacturing rows and suppressing valid siblings; partial selection
neither closed nor order-independent; refusal verse validation; unreadable
roots becoming Catena claims; the locally suppressible unreadable
`bibles.json` prose; the partial terminal proof and the missing full
late-work sink vector; the oracles that still bless those defects; the
CLI/web duplicated semantic model; the uncapped combined route payload
question, asked again above and still awaiting its owner; and the package
truthfulness and supersession corrections, which this lane answers only for
its own new package.

Status: **awaiting fresh independent review** of the exact V8 head and its
immutable handoff archived on `evidence/catena-e1-corrections-v8-handoff`.
This lane records no acceptance of its own work, marks no separately owned
prerequisite complete, and does not review itself.

## Promised work

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
commit. Planning and compatibility packages remain at
`build/agent-handoffs/20260806T212148Z-liturgy-reader-instrument-public-cutover-plan/`
and
`build/agent-handoffs/20260807T052836Z-liturgy-reader-public-cutover-compatibility/`.

Independent post-deployment review passed all nine final questions and accepts
the public cutover as complete. Exact cutover SHA
`9b5f21c0ca26bf02af03d207ddd2617021e16fb3` owns qualifying successful Pages
run `31175722949`. Immediate live verification passed 936/936 across 36
original-pixel states; ordinary-cache verification passed 216/216 after 613
seconds without mixed-generation behavior. The immutable execution handoff is
`build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution/`;
its ZIP SHA-256 is
`06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410`.
Canonical Day and Propers now serve the accepted Instrument without redirects.
Public navigation was not redesigned; retained candidate and oracle routes
remain intact and nonindexable, and cleanup is deferred and unauthorized. The
governed full gate remains non-green only at the unrelated stored-example
transcript replay; no transcript was recaptured or blessed.

### Liturgical Instrument production integration

<!-- promised-deliverable: liturgy-reader-instrument-production-integration-2026-08-06 -->

**Complete; production integration is independently accepted and its exact
reviewed handoff is durably archived. The separately reviewed public cutover is
also complete; public-navigation redesign remains outside both phases.**
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
Pages deployment, and immutable tracked handoff at
`build/agent-handoffs/20260806T112813Z-liturgy-reader-instrument-correction/`.
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
200/noindex and deployed CSS/JS byte-match source. The final narrow immutable
re-review handoff is
`build/agent-handoffs/20260806T141831Z-liturgy-reader-instrument-correction/`.
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
