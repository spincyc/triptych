# Next cold agent — Catena Omnia / corpus foundation review

You are the **independent cold reviewer** for the next Triptych corpus-browser step.

Do not treat prior reports, commit messages, or this instruction file as proof. Recover the relevant state from GitHub and reproduce the evidence yourself from a fresh full checkout. Do not use a worktree or shared index.

## Repository and branch

Repository:

`spincyc/triptych`

Review branch:

`impl/corpus-foundation-b0-b1`

The branch contained the B0/B1 implementation candidate at:

`3d323f0880859b5cf8d380a7bb04ef29584d1e81`

It then received the Catena Omnia vision and roadmap commit:

`4ef5062ca2c01b25f642bd9abe7bfa462c0fd04d`

**Do not assume those are still the remote heads. Fetch first and record the exact remote branch head and `origin/main` you actually review.**

The last known main baseline when these documents were authored was:

`09437907472581df4a8969010bd494249a3539a5`

Again: fetch; do not assume main is still there.

## Your role

Your task is **review and disposition**, not feature implementation.

Do not begin another Catena feature, corpus acquisition wave, Search implementation, shared-shell redesign, or Liturgy change during this review.

Do not merge, deploy, refresh release bindings, approve a release, force-push, rewrite history, or self-accept the branch.

You may make and push **review-record corrections on this feature branch** if they are necessary to make the durable record truthful and internally consistent. Keep such changes narrow and identify them explicitly.

## Recover the governing design before reviewing code

Read, at minimum:

- `guidance/catena.md`
- `guidance/catena-omnia-vision.md`
- `guidance/catena-omnia-roadmap.md`
- `guidance/corpus-browser-master-plan.md`
- `guidance/corpus-browser-vision.md`
- `guidance/corpus-browser-roadmap.md`
- `guidance/corpus-browser-implementation.md`
- `guidance/liturgy-browser-vision.md`
- `ABOUT.md`
- `promised-deliverables.toml`
- the relevant current `PROJECT-WORK.md` entries

Also inspect the live Catena production sources on the reviewed ancestry:

- `src/web/browser/catena/index.html`
- `src/web/browser/catena/catena.css`
- `src/web/browser/catena/catena.js`
- `src/web/browser/catena/catena-model.js`
- `scripts/_catena.py`
- Catena generated structure/data relevant to the checks

The design you are protecting is not “a commentary page.” The core product contract is:

- Scripture is the anchor.
- Only held publishable commentary text appears as commentary.
- acquisition leads, held-but-blocked material, translation absence, projection refusal, uncertainty, and transport error remain distinct states.
- fragments are stored at their natural Scripture extent and chapter views are derived.
- canonical locus precedes projected Bible numbering.
- exact commentary words retain edition, voice/language, rights, provenance, chronology, and source identity.
- actual commentary remains visually distinct from things that are not commentary.
- narrow screens have one reading order.
- the accepted E0/E1 Catena product is closed unless a new explicitly authorized work unit reopens it.
- protected Day/Propers Liturgy remains a separate owner and must not receive the non-Liturgy shell or an unapproved Catena integration.

The new vision extends the horizon to a whole-canon, deep, source-auditable Catena connected to the rest of Triptych by typed relationships. It explicitly does **not** claim that “Omnia” means complete historical coverage, and it does not authorize AI-inferred relationships or AI synthesis inside the historical chain.

## Primary review target: B0/B1 candidate

Cold-review the B0/B1 foundation work whose original candidate head was `3d323f088...`.

The intended changes were narrowly:

1. add `check-browser-models` to `make check` as an explicit named model-driving gate;
2. add `tools/tests/test_browser_model_gate.py` to prove that gate's declared coverage and explicit exclusions;
3. scope `src/web/browser/sources/sources.css` rules that were restyling layout-owned site chrome without page scope;
4. add/extend `tools/tests/test_browser_collisions.py` so this class of site-chrome collision is detected, while recording the protected `day-missal.css` remainder rather than editing it;
5. reconcile stale B0/B1 guidance, roadmap, project-work, and promise-ledger state against current main;
6. make **no Catena product change**, **no shared-shell cutover**, and **no protected Liturgy production change**.

## The two record inconsistencies you must resolve

Do not wave these away as prose differences.

### A. Full-discovery failure identity

The immutable B0/B1 commit narrative records that full discovery at the candidate reproduced the base's 24 failures with **no new identity**.

The final handoff report instead said:

- base: 2,707 tests, 24 failures, 0 errors, 11 skipped;
- head: 2,719 tests, 25 failures, 0 errors, 10 skipped;
- exactly one new failure: `test_day_reader_integration.test_accepted_shell_and_visual_oracle_hashes_are_current`, explained as the deliberately stale release binding for the changed `sources.css`.

Re-run from a clean checkout and determine which statement is true at the exact reviewed commits. Report **failure identities**, not only counts or exit status.

If the durable branch record is wrong, correct it narrowly on the feature branch and commit/push the correction. Do not refresh release bindings merely to make the test green; signing is release-owned.

### B. Commit count language

The final report said “3 commits pushed,” while the branch comparison from the old main baseline showed four commits of ancestry because the branch already contained an earlier continuation-instructions commit.

State both facts precisely:

- total branch commits ahead of the actual merge base/main you review;
- commits created by the B0/B1 execution being reviewed.

Correct durable prose if needed so a future agent cannot confuse those quantities.

## B0/B1 cold-review questions

Answer each explicitly.

### Gate design

- Does `check-browser-models` actually run under `make check`?
- Is it deliberately named rather than globbed?
- Does every named module exist and genuinely drive browser JavaScript?
- Does the test detect a newly added browser-JS-driving suite that is neither gated nor recorded with a reason?
- Are all current `UNGATED_WITH_REASON` entries still true?
- Does the gate remain narrow rather than silently importing the entire opt-in test suite?
- Is its runtime cost acceptable for the role it now has? Record measurement; do not invent a budget after the fact.

### Collision/scoping work

- Reproduce the old `sources.css` hazard from the base: layout-owned `.brand` / `.site-footer` (and any relevant `.page-footer`) styling depended on stylesheet reach rather than page scope.
- Verify the candidate scopes the rule to Sources without changing Sources' rendered behavior.
- Verify the new source-level test derives layout-owned classes from the actual release layout rather than a stale hand-maintained list where possible.
- Verify a new unscoped site-chrome selector would fail.
- Verify the protected exception cannot quietly grow beyond its recorded selector count.
- Independently search the current browser tree for equivalent unrecorded hazards; do not assume the test is exhaustive merely because it passes.

### Protected Liturgy boundary

Inspect the current `promised-deliverables.toml` and current Liturgy ownership state.

The last known B0/B1 conclusion was that `src/web/browser/liturgy/day-missal.css` still had twelve unscoped `body > .site-header` selectors loaded by four published Liturgy pages, and that the smallest mechanical fix would be page scoping such as `body:has(> .page-browser) > .site-header`.

Confirm whether that is still true on the fetched branch/main.

If the Liturgy owner has **not** granted the narrow carve-out, do not edit the file. The foundation promise remains blocked.

If a newer mainline commit has legitimately removed or released the seam, record that changed fact rather than replaying the old blocker mechanically.

Do **not** resurrect the withdrawn proposal to promote `reader-shell.js/css` into `shared/`.

### Catena regression boundary

The B0/B1 candidate should not change Catena production sources or generated Catena data.

Prove this from the actual diff.

Run the available Catena model/production/browser checks needed to show that the shared-foundation work does not regress:

- Scripture-first rendering;
- held commentary chain;
- lead/absence/refusal distinctions;
- voice behavior;
- URL contract;
- lazy fragment transport;
- focus recovery/visibility;
- narrow reading order;
- built-artifact Catena identities where the existing gate defines them.

Do not reinterpret inherited shared-shell failures as Catena product regressions unless the candidate actually changed their identity.

### Built-artifact evidence

Re-run the relevant real-Chromium artifact gate over both the true base and reviewed candidate where practical.

Compare identities and detail strings, not merely totals.

The last reported matrix was 19 routes × 9 states = 2,290 assertions, with 1,850 pass, 212 fail, 228 skip and byte-identical rows between base and candidate. The reported 212 inherited failures were:

- 108 nested-`main` rows across 12 routes;
- 77 target-size rows under the gate's WCAG 2.2 AAA choice;
- 27 skip-link/focus rows on three protected Liturgy routes.

Treat those numbers as claims to reproduce, not axioms.

### Release-binding state

The implementation candidate deliberately changed a published source (`sources.css`) without release-owned re-signing.

Verify the exact stale release-binding path set at the reviewed head.

Do not run a broad refresh and do not hand-edit a digest. If a later authorized release step is needed, it must be separately scoped to exact accepted paths.

## Review the new Catena Omnia vision

The vision already contains a cold-review section, but you are independent of it. Challenge it again.

At minimum test these questions:

1. Does “Omnia” remain explicitly a whole-corpus horizon rather than a completeness claim?
2. Does the vision protect Scripture from becoming a sidebar to a huge commentary plane?
3. Does it preserve L1 lead / L2 holding / L3 fragment distinctions?
4. Does it preserve canonical locus, natural extent, chronology, edition, voice, rights, and typed uncertainty?
5. Does it keep Sources, Scripture, Liturgy, History, Law, Publications, and Commentary as connected typed views rather than collapsing them into Catena?
6. Does it prohibit inferred relationships from appearing as established corpus edges?
7. Does it keep AI synthesis separate from historical commentary and optional?
8. Does it preserve static-first architecture without forbidding evidence-based future chunking changes?
9. Does it avoid faux-manuscript ornament as a substitute for ecclesial credibility?
10. Does it clearly defer protected Liturgy integration to a Liturgy-owned seam?

Disposition the vision as `ACCEPT`, `ACCEPT_WITH_CORRECTIONS`, or `CHANGES_REQUIRED` and record concrete corrections if any. Do not redesign E0/E1 merely because you would personally make different aesthetic choices.

## Review the new Catena Omnia roadmap

Again, challenge rather than endorse it.

Key questions:

1. Is the roadmap executable in bounded waves rather than an unbounded wish list?
2. Does it avoid a purely serial dependency that would block useful corpus acquisition behind shell work?
3. Does it insert scale measurement before large corpus growth or transport redesign?
4. Does it keep acquisition and UI/foundation progress moving together?
5. Are breadth, depth, voice/translation, source/citation, typed relationships, Search, and advanced views separated cleanly?
6. Does it avoid optimizing raw fragment count?
7. Does it preserve natural extent as the only stored placement truth?
8. Does it put rights before publication rather than after ingestion?
9. Does Search remain J0/J1/J2 rather than becoming a Catena-only search engine?
10. Are Liturgy-to-Catena, tradition threads, and AI synthesis sequenced behind the explicit authority/schema/citation prerequisites they need?
11. Are continuous accessibility, built-artifact browser, rights, and visual cold reviews strong enough for deep-corpus states?
12. Are release signing, merge, deployment, and acceptance still separate authorities?
13. Does the roadmap explicitly distinguish interface-complete, corpus-broad, corpus-deep, mature, and ongoing acquisition states?

Disposition the roadmap as `ACCEPT`, `ACCEPT_WITH_CORRECTIONS`, or `CHANGES_REQUIRED`. If corrections are necessary, update only the roadmap/vision/review records needed to make the plan truthful; do not begin an implementation phase.

## Validation expectations

Use the repository's actual current commands and guidance after you inspect them. Do not blindly paste stale commands from old handoffs.

At minimum, the review should cover the relevant equivalents of:

- branch/main fetch and exact SHA recording;
- clean working tree before and after;
- diff/path inventory against the actual merge base;
- B0/B1 focused Python suites;
- `check-browser-models` standalone and as part of the intended aggregate path;
- `check-browser-harnesses` where available;
- Catena model/generator and curated production checks;
- browser static checks;
- built public preview/site;
- release-binding verification without unauthorized refresh;
- real-Chromium artifact evidence;
- full test discovery on base and head with identity comparison.

If a command is prohibitively broad or an inherited baseline is red, do not convert that into “not run.” Run what the repository contract requires, then classify inherited versus new identities accurately.

## Final disposition format

Your final report should be concise but mechanically useful. Include:

- `STATUS`;
- reviewed branch;
- actual fetched `origin/main`;
- actual reviewed head;
- merge base;
- whether working tree is clean;
- total branch commits ahead and B0/B1 execution commits separately;
- `B0/B1 DISPOSITION`;
- `CATENA OMNIA VISION DISPOSITION`;
- `CATENA OMNIA ROADMAP DISPOSITION`;
- exact changed-path inventory;
- protected-file touch count;
- Catena production-path touch count;
- full-discovery base/head totals **and new failure identities**;
- Chromium artifact base/head identity comparison;
- stale release-binding path set;
- unresolved protected-Liturgy blocker state;
- any durable record corrections you committed and their SHAs;
- exact next authorized action;
- explicit statement that you did not merge, deploy, release-sign, self-accept, or begin the next feature lane.

## Stopping line

Stop after independent review, any narrowly necessary review-record corrections, commit/push of those corrections to the same feature branch, and the final disposition report.

Do not proceed into CO-01, CO-03, acquisition, Search, Scripture implementation, Sources implementation, shell cutover, or Liturgy changes. The review must first leave the branch in a state another agent can understand without reconstructing contradictions from chat history.
