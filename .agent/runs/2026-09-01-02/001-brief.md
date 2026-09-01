---
protocol: relay-v1
run: 2026-09-01-02
turn: 001
role: planner
agent: gpt-5.6-sol
branch: integration/catena-omnia-convergence
base: 09437907472581df4a8969010bd494249a3539a5
---

## Objective

Build a clean, reviewable, main-descended Catena Omnia convergence candidate that carries forward the accepted B0/B1 corpus-browser foundation work and the recovered Catena Omnia vision/roadmap, while explicitly reconciling the repository's remote branch families so old Catena evidence is not re-merged and unrelated active lanes are not accidentally swallowed. The result must be a bounded integration candidate on this branch, not a merge to `main` and not a release.

The user-visible outcome is: one coherent candidate another reviewer can inspect without reconstructing fifteen historical commits, plus a concise branch-family disposition that makes clear what is already subsumed, what this candidate carries, and what remains an independent lane.

## Scope boundary

You own only `integration/catena-omnia-convergence` and the relay files for run `2026-09-01-02`.

Start from exact released main `09437907472581df4a8969010bd494249a3539a5`. The accepted donor tree is exact commit `639b9a6fc84b9a169948b951b59972acae24b0a2`; it is fifteen commits ahead of that main with the same merge base. A later independent real-Chromium review accepted the B0/B1 selector-oracle candidate with no implementation changes. Treat `639b9a6f` as the implementation/durable-guidance donor, not as a patch queue whose entire history must be replayed.

You may change only paths necessary to construct and document this convergence candidate: accepted donor implementation/tests, durable Catena/corpus-browser guidance and operational records, and one concise branch-reconciliation record if the existing owning guidance cannot hold the information cleanly.

Do not touch protected Liturgy production files. Do not reopen Catena E0/E1 product behavior. Do not start CO-02 shell cutover, C2/D1/F1/I1 surfaces, Search, relationships, acquisition, or the CO-03 benchmark. Do not delete branches. Do not force-push. Do not merge or push `main`. Do not refresh release bindings, sign, deploy, or claim release acceptance.

Transient historical artifacts are not integration payload. Do not carry `.agent/**` from any donor branch, `NEXT-AGENT-INSTRUCTIONS.md`, `guidance/NEXT-*`, review-only handoffs, ignored/build evidence, ZIPs, or one-off dispatch prose merely because they occur in donor ancestry.

## Acceptance criteria

1. **Exact topology is proved before mutation.** Fetch all refs; record current `origin/main`, this branch tip, donor `639b9a6fc84b9a169948b951b59972acae24b0a2`, merge bases, and ahead/behind counts. If `origin/main` has moved from `09437907472581df4a8969010bd494249a3539a5`, inspect the exact delta first. If it overlaps materially with this lane, stop `partial`/`blocked` rather than silently rebasing the program onto a changed base.

2. **Every donor path is dispositioned.** For every changed path in `09437907472581df4a8969010bd494249a3539a5..639b9a6fc84b9a169948b951b59972acae24b0a2`, classify it as exactly one of:
   - `CARRY_ACCEPTED_FINAL_STATE`;
   - `DROP_TRANSIENT_HANDOFF_OR_REVIEW`;
   - `DROP_SUPERSEDED_OR_REJECTED`;
   - `LEAVE_SEPARATELY_OWNED`.
   The candidate must contain every path classified `CARRY_ACCEPTED_FINAL_STATE` at the correct final bytes or with a narrowly justified current-state reconciliation. No donor path may disappear by accident.

3. **Carry the accepted Catena Omnia north star.** The candidate must contain the final corrected `guidance/catena-omnia-vision.md` and `guidance/catena-omnia-roadmap.md` from the donor line, preserving the closed E0/E1 contract, Scripture-first hierarchy, L1/L2/L3 distinction, canonical projection/refusal semantics, natural extents, edition/rights/voice/chronology truth, typed relationships only, protected Liturgy boundary, static-first scaling, and the doctrine that acquisition progresses in parallel with foundation work.

4. **Carry accepted B0/B1 behavior, not historical ceremony.** Reconcile the final B0/B1 implementation and tests from the donor, including the browser-model coverage gate and the browser-native selector-oracle correction, plus the accepted neutral scoping changes that created the known stale bindings for Scripture and Sources CSS. Do not mechanically cherry-pick review/dispatch commits. Prefer a small number of coherent commits that make the resulting tree easy to review.

5. **Preserve the independent-review result.** The selector oracle must still fail closed for distinct-compound simultaneous user-state selectors, consume the `interactive` measurement as a load-bearing assertion, keep Chromium as reach authority, preserve the protected Liturgy inventories, and leave the known stale release-binding set exactly scoped unless a current-main change proves otherwise. Do not refresh those bindings here.

6. **Reconcile branch families without mass-merging.** Enumerate all `origin/*` branches and group obvious families. For each family/tip, determine ancestry against current `main` and donor/candidate and record a concise disposition:
   - `SUBSUMED_BY_MAIN`;
   - `SUBSUMED_BY_CONVERGENCE`;
   - `ACTIVE_INDEPENDENT_LANE`;
   - `UNIQUE_UNREVIEWED_OR_UNACCEPTED`;
   - `SUPERSEDED_HISTORICAL_EVIDENCE`.
   Old Catena E1 correction/review/evidence branches that are already represented by released main or the accepted donor must not be merged again. `feature/bible-dating`, `feature/pictographic`, metaphysical-demonstration work, TPT/guidance work, and any other genuinely independent program must remain separate unless ancestry proves it is already subsumed. Do not infer acceptance merely because a branch is ahead.

7. **Durable state becomes intelligible.** Update the owning durable records so they no longer describe CO-00/B0-B1 as awaiting review: record that the final independent disposition is ACCEPT, while preserving the separately owned protected-Liturgy blocker and release-binding stop line. Keep records concise; do not add another giant process narrative.

8. **No product drift.** Catena production bytes and generated Catena data must remain byte-identical to `main` unless a carried shared-foundation change necessarily reaches a shared file; if any Catena-visible behavior changes, this lane has exceeded its intended scope and must stop for review rather than blessing it.

9. **Release state is explicit.** The expected candidate may have exactly the already-known stale release bindings caused by accepted `src/web/browser/scripture/scripture.css` and `src/web/browser/sources/sources.css` changes. Report the exact stale set. Any third stale path is a blocker to calling the candidate complete.

10. **Stop at a pushed review candidate.** Commit coherent work to this branch, push it, and return exact work SHA(s), path disposition summary, branch-family summary, validation results, stale-binding set, and the smallest next integration/release action. Do not merge, deploy, sign, or self-accept.

## Verification

Use current repository commands discovered from `AGENTS.md`, `tmt.json`, and the Makefile. At minimum, run and report:

```text
PYTHONDONTWRITEBYTECODE=1 python -m unittest tools.tests.test_browser_collisions
PYTHONDONTWRITEBYTECODE=1 python -m unittest tools.tests.test_browser_model_gate
make check-browser-static
make check-browser-models
python3 scripts/_catena.py check
make check-promised-deliverables
make public-preview
make check-deployment-sources
python3 tools/release-bindings status
git diff --check
```

If `make check-browser-models` stops at the known release-integrity sentinel, execute every downstream named model module individually and compare failure identities exactly, as the accepted review did; do not convert a fail-fast sentinel into an unexplained partial test run.

Also compare Catena production/generated paths against exact main and prove any intended byte identity. Run enough full discovery to establish whether the candidate adds a new failure/error identity relative to the exact base; compare identities, not only counts.

## Context

Read current branch/main instructions first:

- `AGENTS.md`
- `guidance/repository.md`
- `guidance/corpus-browser-master-plan.md`
- `guidance/corpus-browser-vision.md`
- `guidance/corpus-browser-roadmap.md`
- `guidance/corpus-browser-implementation.md`
- `guidance/catena.md`
- `guidance/liturgy-browser-vision.md`
- `PROJECT-WORK.md`
- `promised-deliverables.toml`
- `tmt.json`

The accepted donor `639b9a6fc84b9a169948b951b59972acae24b0a2` contains the final Catena Omnia vision/roadmap and accepted B0/B1 implementation state. Inspect it path-by-path with ordinary git commands. Do not read any other relay run directory; the facts needed from the prior review are restated here.

Known accepted-review facts to reproduce rather than blindly trust:

- donor merge base with released main is `09437907472581df4a8969010bd494249a3539a5`;
- the B0/B1 selector review disposition is ACCEPT;
- the corrected selector suite previously passed 36 tests in real Chromium;
- protected Liturgy selector inventories were 12 / 3 / 2 / 3 for `day-missal.css`, `reader-shell.css`, `reader-instrument.css`, and `reader-visual-reset.css`;
- the production selector scan was 1,193 unique arms with zero refusals;
- the known intentionally stale binding set was exactly Scripture CSS and Sources CSS;
- protected Liturgy remains separately owned and must not be edited here.

The goal is not to preserve these numbers forever; reproduce current truth on the candidate and report drift honestly.

## When blocked

Follow relay-v1 preflight and blocked-channel rules exactly. Do not improvise around a dirty checkout, wrong repository/branch, stale brief, failed fetch/push, rebase/merge state, or protocol mismatch.

If current `main` moved and overlaps this lane, if donor classification exposes an accepted path whose ownership cannot be safely reconciled, if a third release binding becomes stale, or if Catena product behavior changes unexpectedly, publish `status: partial` or `blocked` with the exact dependency rather than broadening scope.
