# Triptych — Continue Corpus Browser Program: B0/B1 Shared Foundation

## Agent

**Use a fresh Claude CLI agent.**

This is the next program lane after Catena E1 was merged, release-bound, deployed, and verified live.

Your job is to reconcile the **current mainline** against the corpus-browser master plan's B0/B1 shared-foundation sequence, implement every currently authorized and unblocked design-neutral foundation item, produce a clean review candidate on this branch, push it, report exact remaining blockers, and stop.

Do **not** merge to `main`.
Do **not** deploy.
Do **not** force-push.
Do **not** reopen Catena E1.
Do **not** start C2, D1, F1, G1, H1, I1, Search, relationships, or final cutover in this lane.
Do **not** silently cross a still-protected Liturgy ownership seam.

---

# 1. Exact starting point

Repository:

`spincyc/triptych`

Working branch:

`impl/corpus-foundation-b0-b1`

Exact branch base / current main at dispatch:

`09437907472581df4a8969010bd494249a3539a5`

That commit is the Catena E1 post-merge release-binding refresh. Catena E1 is already complete end-to-end and live.

Require before work:

```bash
git fetch --all --prune
git rev-parse HEAD
git rev-parse origin/main
git rev-parse origin/impl/corpus-foundation-b0-b1
```

The branch must descend directly from `09437907472581df4a8969010bd494249a3539a5` before your own changes.

If `origin/main` has advanced, **do not rebase automatically**. Record the new SHA, inspect whether any new main changes overlap this lane, and continue from the dispatched branch unless a real overlap makes the dispatch stale.

Use a full standalone checkout. **No git worktrees.**

---

# 2. Governing authorities — read first

Read current versions from this branch/main, not historical chat summaries:

1. `AGENTS.md`
2. `guidance/repository.md`
3. `guidance/corpus-browser-master-plan.md`
4. `guidance/corpus-browser-vision.md`
5. `guidance/corpus-browser-roadmap.md`
6. `guidance/corpus-browser-implementation.md`
7. `guidance/liturgy-browser-vision.md`
8. `guidance/liturgy-browser-roadmap.md`
9. `guidance/liturgy-reader-state.md`
10. `guidance/web-data.md`
11. `guidance/web-editions.md`
12. `PROJECT-WORK.md`
13. `promised-deliverables.toml`

The master plan currently identifies the implementation order as:

- B0/B1 shared foundation and neutral browser gates;
- then C2 Home/Publications;
- D1 Reader;
- F1 Sources;
- G/H/I History/Law/Scripture;
- later J Search, K relationships, L whole-site acceptance, M integration/cutover.

E1 Catena has already been completed independently. Do not treat the older text saying E1 is merely authorized as current state.

---

# 3. Current fail-closed operational state to reconcile

At dispatch, `promised-deliverables.toml` still records:

`corpus-browser-foundation-hardening-2026-08-08`

as `in_progress`.

Its recorded passing requirements include:

- durable architecture record;
- built-artifact Chromium gate;
- four-reader-harness target;
- published URL/hash contracts pinned;
- no visual/product decision.

Its remaining open requirement is:

`shared-shell-blocking-collisions-resolved`

The historical implementation record says three collision/plumbing items were solved on an old branch and one protected Liturgy selector hazard remained blocked. **Do not assume those historical commits are present on current main. Verify current bytes.**

The operational ledger also still records:

`liturgy-reader-live-ritual-flow-2026-08-07`

as `in_progress` at dispatch.

That means protected Liturgy ownership is still real unless current tracked authority now says otherwise.

---

# 4. Mission

Create a **current-main B0/B1 convergence candidate** that answers, with code and evidence:

1. Which master-plan steps 1–9 are already satisfied on current main?
2. Which accepted historical fixes were never integrated and are still needed?
3. Which items can be safely implemented now without changing accepted visual/product design?
4. Which items are still blocked specifically by protected Liturgy ownership?
5. After this branch, what exact smallest remaining action is needed to unlock C2/D1/F1 and later shared-shell cutover?

Do not mechanically replay old commits.
Do not cherry-pick the old foundation-hardening branch wholesale.
Reconcile behavior and intent against current main path by path.

---

# 5. Preserve Catena E1 as a closed product lane

Catena production is now live from main.

Do not redesign it.
Do not reopen its V13–V16 hardening history.
Do not alter its accepted voice semantics, projection/transport/cache model, absence/refusal behavior, URL contract, or release records merely because shared files are nearby.

Any shared-foundation change that reaches Catena must prove **no product regression** on the real Catena route.

At minimum preserve:

- `/catena/index.html` route identity;
- exact accepted voices `original`, `translation:en`, `translation:la`;
- no `translation:grc` manufacture;
- semantic author/work delimiter;
- visible recovery focus;
- same-path/late/cache ownership behavior;
- current Catena browser assertion identity/status universe unless an independently owned shared-shell defect is intentionally exposed rather than hidden.

---

# 6. First task: build a current-main B0/B1 status matrix

Before editing production code, inspect the current tree and record each master-plan implementation step 1–9 as one of:

- `SATISFIED_ON_MAIN`
- `PARTIALLY_SATISFIED`
- `MISSING`
- `BLOCKED_BY_PROTECTED_OWNER`
- `SUPERSEDED_BY_CURRENT_MAIN`

The historical sequence in `guidance/corpus-browser-implementation.md` is:

1. honest baseline;
2. runnable Chromium harness target;
3. narrow browser-model gate;
4. blanket JS syntax + browser-page structural lint;
5. shared-shell collision/plumbing hazards;
6. promote reader shell to shared;
7. shared primitives;
8. shared accessibility blocks;
9. design-neutral per-route regression harness.

Do not infer completion from prose alone. Check code, tests, Makefile targets, actual execution, and current operational ledger.

Commit the status matrix into the durable implementation/roadmap record rather than an ignored continuity file.

---

# 7. Baseline discipline

The implementation guidance contains historical red-baseline counts from an old base. Those counts are not automatically today's baseline.

Establish a fresh baseline at exact dispatch base `09437907472581df4a8969010bd494249a3539a5` for the tests you will use.

For broad discovery, compare **failure/error identities**, not only raw counts.

Do not make a known-red suite green by deleting assertions, skipping without cause, blessing new failures, or changing expected counts to match your branch.

Do not spend this lane fixing unrelated red tests.

---

# 8. B0/B1 step 2 — Chromium harness target

Verify whether current main already has the target that:

- builds `public-preview` first;
- resolves `TRIPTYCH_CHROME`;
- runs the existing real-Chromium reader harnesses;
- reads each harness's actual report channel correctly;
- records honest inherited failures;
- stays out of `make check` if that remains the accepted contract.

If already correct, do not rewrite it.
If incomplete, make only the smallest mechanical correction and add focused tests.

Do not weaken reader assertions to force green.

---

# 9. B0/B1 steps 3–4 — neutral gates

Verify current main for:

- narrow browser-model gate under `make check` as authorized;
- `node --check` coverage for all published browser JS;
- static browser-page structural/head-whitelist validation before deployment;
- design-neutral artifact checking rather than pixel expectations.

Implement only missing pieces.

Do not wire the entire historically slow/red unit suite into `make check` without explicit authority.

---

# 10. Step 5 — shared-shell collision/plumbing hazards

Re-audit all four hazards from the implementation authority against current main:

### A. Shared error/banner destination plumbing

Verify `T.fail` / banner behavior does not hard-code only one page's landmark and does not regress current Catena recovery/focus behavior.

### B. History `.field` collision

Verify the history change-row selector no longer collides with shared form-control `.field` semantics.

### C. Publications/texts `.detail` collision

Verify the record card no longer shadows the shared detail component.

### D. Protected Liturgy `day-missal.css` site-header selectors

Verify whether unscoped `body > .site-header` rules still exist and whether the current Liturgy operational authority allows this corpus lane to scope them.

**Critical rule:**

If `liturgy-reader-live-ritual-flow-2026-08-07` or another current deliverable still owns/protects `day-missal.css` or the affected canonical reader seam and no tracked carve-out/waiver exists, **do not edit that protected file in this lane**.

Record:

- exact selectors;
- exact affected routes;
- why they block shared-shell promotion;
- the smallest proposed mechanical scoping change;
- the exact authority/carve-out needed.

Do not silently mark `shared-shell-blocking-collisions-resolved` pass while D remains blocked.

---

# 11. Step 6 — reader-shell promotion

The historical plan proposes moving or promoting `reader-shell.js` / `reader-shell.css` into `shared/`, parameterizing only:

- `majorSelector`;
- `headingSelector`;
- `defaultGroup`;

with current Liturgy behavior as defaults.

This step is allowed **only if current operational authority explicitly releases or carves out those protected files**.

If still protected:

- do not move them;
- do not duplicate them into a competing shared shell;
- do not create a second modal owner;
- do not patch Liturgy through an indirect shared import;
- mark step 6 `BLOCKED_BY_PROTECTED_OWNER` and continue only with work that does not depend on it.

If current tracked authority now permits the move, prove exact Day/Propers behavior and file-ownership consequences before and after, update promised-deliverable evidence paths truthfully, and keep the change behavior-neutral.

---

# 12. Step 7 — shared primitives

Only execute if its dependencies are genuinely satisfied on current main.

Reconcile, rather than blindly port, the historical proposals for shared:

- lazy disclosure block;
- memoized JSON loading with render ownership;
- citation rendering;
- act-record vocabulary / common fact rendering.

A primitive belongs in shared code only when at least two current production surfaces use the same semantic contract.

Do not centralize a false commonality.
Do not change visible wording merely to deduplicate code.
Do not flatten rights, absence, refusal, or provenance distinctions.

Use production behavior tests, not source-line similarity, as the acceptance criterion.

---

# 13. Step 8 — shared accessibility blocks

Only execute if dependencies and ownership permit.

Design-neutral accessibility improvements may include current-authority equivalents of:

- forced-colors token remap;
- reduced-motion behavior;
- browser print fallback rules;
- visible focus preservation.

Do not redesign accepted surfaces.
Do not change canonical PDF authority.
Do not add permanent chrome.
Do not weaken Catena's now-verified focus recovery.

Any rule moved to shared CSS must be checked for selector leakage across every published browser entrance.

---

# 14. Step 9 — B1 design-neutral regression harness

Current main already contains corpus browser gating according to the ledger; verify its actual coverage before adding anything.

The B1 harness is neutral infrastructure, not a visual oracle.

It should cover current published browser routes and detect, as applicable:

- console errors;
- failed requests / HTTP errors;
- unnamed interactive accessibility nodes;
- document-level horizontal overflow at 320 CSS px;
- obviously undersized interactive targets under the governing contract;
- clipping at representative 400% zoom/reflow;
- forced-colors and reduced-motion execution;
- structural landmark failures.

Do **not** add pixel-diff baselines.
Do **not** turn known inherited failures into accepted visual snapshots.

If current `corpus_browser_gate.mjs` already satisfies the lane, improve nothing merely for aesthetics.

---

# 15. Nested-main and site-navigation work are NOT automatically in scope

Master-plan steps 10 and 11 are beyond the B0/B1 foundation lane:

- generated site navigation;
- nested `<main>` repair.

Do not begin them merely because the B1 gate reports them.

Record them as downstream blockers/findings unless a current authority explicitly folds a mechanical prerequisite into B0/B1.

The final non-Liturgy shared-shell cutover remains separately authorized work.

---

# 16. Do not start surface implementation

Even if foundation work becomes clean, stop before:

- C2 Home/Publications implementation;
- D1 Publication Reader;
- F1 Source Library;
- G1 History;
- H1 Law;
- I1 Scripture;
- J Search;
- K relationships.

Your output is the shared-foundation candidate and an exact next-lane readiness matrix.

---

# 17. Authority reconciliation

The corpus guidance contains historical state that may be stale relative to later accepted Wave 1 work and Catena E1.

Reconcile only facts you can prove from current tracked evidence.

In particular:

- do not leave E1 described as merely unstarted/authorized where a current summary is being updated;
- do not mark A0–A4 accepted operational requirements complete unless the repository contains the required independent disposition evidence under the existing promise schema;
- do not invent waivers;
- do not delete open requirements to make a deliverable complete;
- if a stale candidate/open state is contradicted by a later tracked independent acceptance, update it only with exact evidence and the repository's normal marker/ledger rules.

Run the promised-deliverables checker after every ledger change.

---

# 18. Release bindings

This is an implementation/review-candidate branch.

Do **not** broadly refresh or re-sign release bindings merely because source bytes changed.

Do not use unfiltered:

```bash
make refresh-release-bindings ADOPT=1
```

If candidate changes make release bindings stale, record the exact stale path set and leave the final scoped adoption for the accepted integration/release step unless current repository authority explicitly requires a feature-branch scoped refresh.

Never hand-edit hashes.
Never invent an approval note.

---

# 19. Validation

Use the smallest current authoritative set that proves this lane.

At minimum run, where applicable:

```bash
python3 -m unittest discover -s tools/tests
```

and record exact failure/error identity comparison to dispatch base.

Run current focused browser-foundation tests and targets, including current equivalents of:

- promised-deliverables / repository ledger validation;
- browser URL/hash contracts;
- browser collision tests;
- browser syntax/HTML structural lint;
- corpus browser gate;
- reader harness target;
- `make public-preview`;
- `make verify-public-preview` when release-binding state permits meaningful verification, otherwise separate genuine source/build failures from the intentionally stale binding set.

Use real Chromium if available:

```bash
TRIPTYCH_CHROME=/usr/bin/chromium
```

or the resolved local path.

For any shared change, smoke at least:

- Home/public entry;
- Publications;
- Publication Reader;
- Catena;
- Sources;
- History;
- Law;
- Scripture;
- canonical Day and Propers if shared code can reach them.

Do not recapture a broad visual-review package unless a changed surface actually requires it.

---

# 20. Regression bar

A B0/B1 blocker requires one of:

1. current production route / data / browser event → changed foundation code → wrong user-visible or semantic result;
2. regression against exact dispatch base;
3. violation of a current promised-deliverable ownership or fail-closed requirement;
4. governed build/release/size/accessibility gate newly failing because of this branch.

Do not restart synthetic adversarial hardening unrelated to production.

---

# 21. Commit discipline

Keep commits small and reviewable.

Prefer conceptual commits such as:

1. current-main B0/B1 authority/status reconciliation;
2. missing neutral gates;
3. unprotected collision/plumbing fixes;
4. permitted shared primitives/accessibility changes;
5. tests and durable status reconciliation.

Always inspect `git status --short` before commit.
Name paths explicitly in commits where practical.
No force push.
No history rewrite.

---

# 22. Candidate branch and push

Stay on:

`impl/corpus-foundation-b0-b1`

Push coherent checkpoints and the final candidate to that branch.

Do not merge to main.

The final candidate must have:

- clean working tree;
- local HEAD == remote branch head;
- exact dispatch-base ancestry;
- durable current-main status matrix;
- no self-acceptance.

---

# 23. Required final disposition

Return exactly one program disposition:

## `B0/B1 CANDIDATE READY FOR INDEPENDENT REVIEW`

Use if every currently authorized B0/B1 requirement is implemented and no protected-owner dependency remains necessary for the claimed candidate boundary.

## `B0/B1 PARTIAL CANDIDATE — PROTECTED LITURGY CARVE-OUT REQUIRED`

Use if the branch closes all unprotected foundation work but the current Liturgy deliverable still blocks step 5(d), reader-shell promotion, or another necessary shared seam.

This is not failure. Name the **smallest exact carve-out** needed and stop.

## `CHANGES REQUIRED BEFORE REVIEW`

Use only if your own implementation has a real production regression or unresolved in-scope defect.

Do not broaden into another hardening loop.

---

# 24. Stop-condition report

Return:

- branch;
- dispatch base SHA;
- current `origin/main` SHA at finish;
- final branch HEAD;
- push verification;
- clean-tree status;
- B0/B1 step 1–9 matrix;
- exact already-satisfied-on-main items;
- exact changes implemented;
- exact historical fixes deliberately not reused and why;
- foundation-hardening promise state before/after;
- foundation-design stale-authority reconciliation, if any;
- current Liturgy protected-owner state;
- whether `day-missal.css` remains a blocker;
- whether reader-shell promotion was permitted/executed;
- protected files changed, if any, with authority citation;
- Catena regression result;
- focused test results;
- full-discovery base/head counts and identity delta;
- real Chromium gate result;
- reader-harness result;
- 320px overflow result;
- accessibility-name/request/console result;
- public-preview build result;
- link/static verification result;
- release-binding stale path set, if any;
- unexpected changed-path count;
- governed budget/size result if touched;
- exact remaining downstream blockers;
- exact next lane unlocked by this candidate;
- final disposition;
- exact next action.

Then stop.

Do not start C2/D1/F1 or shared-shell cutover in the same session.
