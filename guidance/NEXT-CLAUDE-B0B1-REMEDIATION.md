# B0/B1 cold-review remediation — implementation instructions

You are the **implementation agent** for one narrow remediation pass in the Triptych repository.

Your task is to fix the **two specific blockers found by the independent cold review** of the B0/B1 corpus-foundation candidate, update the durable record truthfully, commit and push the remediation candidate to the same feature branch, and stop.

This is **not** a new product lane and **not** a fresh architectural redesign.

Do not merge, deploy, release-sign, refresh release bindings, touch protected Liturgy production files, reopen accepted Catena E0/E1 product design, begin Catena Omnia acquisition, implement Search, cut over the shared shell, or begin another corpus surface.

---

## 1. Repository, branch, and authority

Repository:

`spincyc/triptych`

Target feature branch:

`impl/corpus-foundation-b0-b1`

The independent review checkpoint you are remediating is:

`bda54d55c65e0447a26aff0cf76bc51f5fd54ca5`

That checkpoint recorded:

- **B0/B1 — CHANGES_REQUIRED**;
- **Catena Omnia vision — ACCEPT_WITH_CORRECTIONS**;
- **Catena Omnia roadmap — ACCEPT**.

The accepted vision correction and accepted roadmap are **not implementation scope for this task**.

This instruction file is committed after the review checkpoint, so the remote branch head you fetch will normally be newer than `bda54d55...`. Start from the current remote feature-branch head containing this file and verify that `bda54d55...` is an ancestor. Record the exact fetched `origin/main`, remote feature head, merge base, and starting HEAD before changing anything.

Use a fresh full checkout or otherwise prove an uncontaminated checkout. **Do not use a worktree or shared index.**

If the remote branch has materially advanced beyond this instruction commit through unrelated implementation, do not guess at conflict resolution: recover the new state, state the divergence in your report, and restrict any work to changes that remain clearly authorized by this file.

---

## 2. Read before editing

Read the current versions of at least:

- `AGENTS.md`
- `guidance/corpus-browser-master-plan.md`
- `guidance/corpus-browser-vision.md`
- `guidance/corpus-browser-roadmap.md`
- `guidance/corpus-browser-implementation.md`
- `guidance/catena-omnia-vision.md`
- `guidance/catena-omnia-roadmap.md`
- `guidance/liturgy-browser-vision.md`
- `guidance/NEXT-COLD-AGENT-CATENA-OMNIA.md`
- `PROJECT-WORK.md`
- `promised-deliverables.toml`
- the independent review commit/diff at `bda54d55...`

Inspect before editing:

- `Makefile`
- `tools/tests/test_browser_model_gate.py`
- `tools/tests/test_browser_collisions.py`
- `src/web/browser/shared/browser-core.css`
- `release/public-alpha/layout.html`
- every production stylesheet under `src/web/browser/` that the collision test analyzes
- `src/web/browser/scripture/scripture.css`
- `src/web/browser/scripture/index.html`
- `src/web/browser/scripture/track.html`

Inspect protected Liturgy only as read-only evidence where needed. Do not edit it.

---

## 3. The two blocking findings to fix

The independent reviewer found two blockers. Treat them as requirements, not suggestions.

### Blocker A — the coverage guarantee is not itself gated

Current intent:

- `make check` reaches `check-browser-models`;
- `check-browser-models` runs the explicitly named `BROWSER_MODEL_TESTS`;
- `tools/tests/test_browser_model_gate.py` contains the crucial meta-test that scans `tools/tests/test_*.py` and fails when a suite drives browser JavaScript but is neither gated nor explicitly recorded in `UNGATED_WITH_REASON`.

Cold-review finding:

**`make check` does not actually run `test_browser_model_gate.py`, so the assertion intended to prevent future silent omissions can itself remain outside the gate. A new JavaScript-driving suite can therefore appear without being named or excused while `make check` remains green.**

This must be fixed.

### Blocker B — the site-chrome collision detector proves too little

Current intent:

`SiteChromeScopeTest` should prevent an instrument stylesheet from restyling the public layout's chrome unless the rule is positively scoped to that instrument/page.

Cold-review findings:

1. `site_chrome_selectors()` detects selectors through layout-owned **classes**, so it misses a broad element selector such as:

   ```css
   a { ... }
   ```

   even though the published layout contains links and the rule can therefore restyle global masthead/footer chrome when that stylesheet reaches the built page.

2. It mistakes a non-layout class anywhere in the selector for positive page scope. A selector such as:

   ```css
   .site-header:not(.route-only)
   ```

   is **not** positively scoped to `.route-only`; the negative condition broadens/excludes and must not count as route ownership.

3. `SITE_CHROME_UNSCOPED` freezes protected `liturgy/day-missal.css` only by the number `12`. A protected selector can disappear and a different one appear while the count remains 12, and the test would accept the mutation.

4. This is not merely hypothetical: `src/web/browser/scripture/scripture.css` currently contains a bare link rule near its top:

   ```css
   a {
     color: var(--section-ink);
     text-underline-offset: 0.15em;
     text-decoration-thickness: from-font;
   }
   ```

   plus the broad `a:hover` rule. The current detector does not report them.

The detector must be strengthened so the test contract actually expresses the hazard it claims to prevent.

---

## 4. Required remediation A — make the model-gate meta-test unavoidable

Repair the Make/test topology so the browser-model coverage meta-test is genuinely under the normal `make check` contract.

### Required properties

1. `make check` must still reach the browser-model gate.
2. The model-driving suites must remain an **explicit named list**, not a glob whose membership grows accidentally.
3. `test_browser_model_gate.py` itself must execute whenever the browser-model gate executes under `make check`.
4. Do **not** add `test_browser_model_gate` to `BROWSER_MODEL_TESTS` if doing so makes the existing invariant "every `BROWSER_MODEL_TESTS` entry actually drives browser JavaScript" false. Preserve the semantic distinction between:
   - model-driving suites; and
   - the meta-test that proves the gate's coverage.
5. `check-tests` must remain a separate opt-in whole-suite target unless a current governing document independently changed that decision. This task does not authorize importing the entire test suite into `make check`.
6. Add/update focused tests so the Makefile topology itself is pinned: a future edit that removes the meta-test from the normal gate must fail.
7. The existing `UNGATED_WITH_REASON` entries must be re-audited against the current tree. Keep only exclusions that are still true and specific.
8. Do not paper over the blocker by rewriting the test's prose or weakening `drives_browser_javascript()` until the old tree passes. The coverage guarantee must become stronger, not easier to satisfy.

### Adversarial proof

Prove that the repaired topology detects the failure mode the reviewer described.

Use a deterministic test or bounded temporary mutation that demonstrates this property:

> if a new `test_*.py` suite genuinely drives browser JavaScript and is neither in the named gate nor in the explicit exclusion map, the meta-test fails; and because that meta-test is under the normal browser-model gate, the relevant `make check` path cannot silently pass.

Do not leave the synthetic mutation in the repository.

### Runtime

Measure the actual standalone browser-model gate after the fix. The cold review measured the pre-remediation gate at **362 tests in about 166 seconds**, not the older 358-test figure. Report the new exact count and elapsed time. Do not invent a new arbitrary performance ceiling in order to pass this task.

---

## 5. Required remediation B — make site-chrome scope detection match the promise

The test does not need to become a standards-complete CSS parser, but it **must correctly cover the selector classes that can occur in this repository and the concrete counterexamples that defeated the old implementation**.

Design the smallest robust solution that proves the stated invariant rather than merely adding special cases for two strings.

### The invariant

For each production instrument stylesheet analyzed by this gate:

> A selector that can match a public-layout chrome element is unsafe unless its match is positively constrained by route/instrument-owned context, or it is an exact, explicitly authorized protected exception.

`layout.html` remains the source of truth for the site chrome. Derive as much as practical from the actual layout rather than maintaining a second stale imitation of it.

### Required counterexamples

Add focused tests proving at least all of these:

#### Must be rejected as unscoped

```css
.site-header { ... }
body > .site-header { ... }
a { ... }
a:hover { ... }
.site-header:not(.route-only) { ... }
body .site-footer a { ... }
```

Also cover at least one grouped/comma selector where only one arm is unsafe; the unsafe arm must not be hidden by the safe arm.

#### Must be accepted as positively page-scoped

Examples equivalent in semantics to:

```css
.sources-page .page-footer a { ... }
body:has(> .sources-page) .site-footer a { ... }
.plan-page a { ... }
.track-page a:hover { ... }
.route-only .site-header { ... }
```

Do not mechanically hard-code those example class names as the definition of safety. The test should reason from positive route/instrument context versus layout-owned chrome.

### Negative pseudo-class rule

A non-layout class occurring only inside a negative condition such as `:not(...)` is **not positive page scope**.

The implementation must correctly reject at least:

```css
.site-header:not(.route-only)
```

and an equivalent nested/compound case representative of selectors the repository could plausibly contain.

If you support `:is()`, `:where()`, or `:has()` in the analysis, treat their semantics deliberately. In particular, the repository already uses `:has()` as positive relational scoping, e.g. `body:has(> .sources-page) ...`; do not accidentally reject that established pattern merely because it contains a pseudo-class.

If a selector form is genuinely too ambiguous for this bounded source-level analysis, **fail closed or require an explicit exact reviewed exception** rather than silently classifying it safe.

### Broad element selectors

The corrected detector must recognize that the public layout owns not only class names but actual elements such as links inside its site header/footer. A bare subject such as `a` can therefore reach layout chrome even though it contains no class token.

Derive relevant layout element/tag facts from `release/public-alpha/layout.html` where practical. Do not solve only the literal `a` string.

### Exact protected exception identity

Replace the count-only protected exception for `liturgy/day-missal.css` with an exact readable identity contract.

The test must fail if, while remaining at the same count:

- one recorded protected selector disappears;
- a different selector appears;
- an existing protected selector changes its matching meaning sufficiently to produce a different normalized selector identity.

Prefer an explicit normalized selector set/list with the owning Liturgy authority and reason stated beside it. A digest may supplement but should not make the exception opaque if a readable exact set is feasible.

**Do not edit `src/web/browser/liturgy/day-missal.css`.**

The last independent review verified that twelve protected selectors remain and the Liturgy owner has not released the seam. Re-read the current promise ledger and governing Liturgy state; if still protected, freeze what is actually there and keep the foundation requirement blocked. Do not ask this lane to fix it.

---

## 6. Disposition the real `scripture.css` broad rule

The corrected detector is expected to expose the existing bare `a` / `a:hover` rules in `src/web/browser/scripture/scripture.css` unless current main/branch state has already changed them.

Do not add Scripture to an exemption merely to make the gate pass.

### If the rule is still present and Scripture is not protected

Make the smallest route-scoping correction that preserves the intended Scripture-page content styling while preventing the instrument stylesheet from restyling layout-owned masthead/footer chrome.

The source pages currently distinguish at least:

- `body.plan-page` in `scripture/index.html`;
- `body.track-page` in `scripture/track.html`.

The public build may project those page classes onto the outer generated `<main>` rather than `<body>`, so choose a selector form that is correct **both for source/off-disk behavior and for the built artifact**. Inspect the actual build path and prove it rather than assuming a body class survives unchanged.

Do not redesign Scripture typography or color. This is selector ownership/scoping only.

### Proof required for a Scripture CSS correction

Before and after the change, prove at representative source/built routes that:

- Scripture-owned content links retain the intended section treatment;
- layout-owned global masthead/footer links are no longer styled merely because `scripture.css` is loaded;
- no document-level overflow or focus regression is introduced;
- the public route still builds;
- the change does not create a Catena or Liturgy regression.

Use the repository's existing Chromium/artifact tooling where possible. A source-level assertion alone is not enough for this actual production selector change.

### If additional real hazards appear

Run the corrected detector over the entire production browser stylesheet tree.

For each newly revealed hazard:

- if it is unprotected and the correction is clearly the same mechanical route-scoping class, fix it minimally and prove the affected route behavior;
- if it belongs to a protected or separately owned surface, do not edit it—record it as an exact blocked/owned exception with authority and evidence;
- if fixing it would require a genuine product/visual design decision, stop that path and record it for owner disposition rather than widening this lane.

Do not convert this remediation into a generic CSS refactor or component-library project.

---

## 7. Boundaries that remain binding

### Catena E0/E1 is closed

Do not modify:

- `src/web/browser/catena/index.html`
- `src/web/browser/catena/catena.css`
- `src/web/browser/catena/catena.js`
- `src/web/browser/catena/catena-model.js`
- Catena generated data
- Catena source semantics
- Catena voice/projection/transport/cache/absence/refusal/URL contracts

Run enough Catena regression evidence to prove your shared-foundation changes did not reach it.

### Protected Liturgy remains protected

Do not modify production files under the protected Day/Propers reader family, especially:

`src/web/browser/liturgy/day-missal.css`

Do not use this task to add the non-Liturgy shell to Liturgy, add a fifth action, alter the first viewport, or revive the withdrawn reader-shell-to-shared proposal.

### Accepted Catena Omnia design documents

Do not reopen `guidance/catena-omnia-roadmap.md`.

Do not casually rewrite `guidance/catena-omnia-vision.md`; the independent review already incorporated its required correction. Only update these if your implementation uncovers a direct factual contradiction, and if so keep the correction minimal and call it out explicitly.

### No release signing

The branch already intentionally carries a stale release binding for:

`src/web/browser/sources/sources.css`

The independent review recorded:

- recorded digest prefix: `a78f8cf...ee4`
- actual digest prefix: `b039d50e...a66`

If this remediation changes another release-bound production stylesheet such as `scripture.css`, the exact stale-binding path set may legitimately grow.

That is **not authority to sign it**.

Do not run a broad `refresh-release-bindings`, do not hand-edit a digest, and do not run release approval. Record the exact stale path set at the candidate head for the later release owner.

---

## 8. Durable record corrections

Update the minimum necessary durable records so a future cold agent does not have to reconstruct the remediation from chat or commit prose.

At minimum inspect whether updates are required in:

- `guidance/corpus-browser-implementation.md`
- `guidance/corpus-browser-roadmap.md`
- `PROJECT-WORK.md`
- `promised-deliverables.toml`

Record:

- the independent `CHANGES_REQUIRED` findings being remediated;
- the actual implementation chosen for the meta-test topology;
- the strengthened selector-scope contract and its known limits;
- the exact protected Liturgy selector exception identity and owner;
- every real additional selector hazard found and its disposition;
- the Scripture broad-selector disposition;
- exact validation counts measured at the remediation candidate;
- the intentionally stale release-binding path set;
- the fact that Catena and protected Liturgy production paths were untouched;
- that B0/B1 remains awaiting independent rereview after remediation.

Do **not** mark B0/B1 independently accepted. You are the implementing agent, not the reviewer.

The `shared-shell-blocking-collisions-resolved` requirement remains `blocked` if the protected `day-missal.css` selectors still exist under the same unreleased Liturgy ownership. Do not convert `blocked` to `pass` merely because the detector now describes the blocker correctly.

---

## 9. Validation

Use the repository's current commands after inspecting the Makefile and guidance. The names below state required evidence, not permission to ignore newer canonical commands.

### Focused unit/source validation

Run the relevant equivalents of:

- `python3 -m unittest tools.tests.test_browser_model_gate`
- `python3 -m unittest tools.tests.test_browser_collisions`
- any focused tests you add for selector classification and Make topology
- static browser checks applicable to changed production CSS

### Browser-model gate

Run `make check-browser-models` (or its current canonical equivalent) and report:

- exact test count;
- pass/fail/skip;
- elapsed time;
- confirmation that the coverage meta-test actually executed in this invocation.

### Aggregate gate

Run the relevant `make check` path and report exact status and failure identities. If the intentionally stale release binding makes an aggregate target red, classify that identity rather than hiding or signing it away.

### Build

Run at least:

- `make public-preview` where still canonical;
- `make public-site`;
- relevant structural/link/browser-static verification.

### Real Chromium / built artifact

Run the existing corpus browser artifact gate over the remediation starting point and candidate where practical.

The previous independent review measured the old candidate/head as:

- 2,290 rows/assertions;
- 1,850 pass;
- 212 inherited fail;
- 228 skip;
- byte-identical rows relative to the original base.

Do not assume those totals remain identical after a deliberate Scripture scoping fix. Compare **identity and detail strings**, and explain every changed row. A corrected global-chrome style is allowed to alter evidence that directly observes the defective selector; unrelated route/state identities must not drift.

Capture enough focused Chromium evidence to prove the actual Scripture route behavior if `scripture.css` changes.

### Catena regression

Run the current canonical Catena checks sufficient to preserve the closed product contract, including the equivalents of:

- Catena generator/model check;
- the 56-test Catena model suite if still current;
- the curated Catena production suite (394 tests at the last review, if still current);
- relevant real-Chromium Catena route evidence if the shared browser gate reaches it.

Report actual current counts; do not force them to match these historical numbers.

### Full discovery identity comparison

Run full Python test discovery on at least:

1. the remediation review checkpoint `bda54d55...` (or an exact clean checkout of it); and
2. your remediation candidate head.

Also retain the original B0/B1 dispatch base `09437907472581df4a8969010bd494249a3539a5` as historical context where useful.

The cold review corrected the historical record to:

- original base `094379074...`: **2,707 tests, 23 failures, 10 skipped**;
- reviewed pre-remediation head `407dfad...`: **2,719 tests, 24 failures, 10 skipped**;
- exactly one new failure identity there: the stale release-binding oracle.

Do not overwrite those reproduced historical facts with older 24/25-failure prose. For your candidate, compare **failure/error/skip identities**, not only totals.

### Release bindings

Run release-binding verification only to report the exact stale set.

Do not refresh or approve it.

---

## 10. Git and commit discipline

Keep the implementation coherent and reviewable.

Recommended structure:

1. one implementation commit containing the gate fixes, any minimal same-class selector scoping repairs, and focused tests;
2. one record/validation commit if separating measured record updates materially improves reviewability.

A single coherent commit is acceptable if the changes are naturally inseparable. Do not manufacture commit count for its own sake.

Push only to:

`origin/impl/corpus-foundation-b0-b1`

No force push.

At finish, fetch the remote again and prove the remote feature head equals your local HEAD. Working tree must be clean.

---

## 11. Required final report

Use a compact mechanically useful report containing at least:

- `STATUS: B0/B1 REMEDIATION CANDIDATE — INDEPENDENT REREVIEW REQUIRED` (unless a new blocker makes even candidate status false);
- branch;
- starting remote head;
- `origin/main` at start and finish;
- merge base;
- final local/remote HEAD;
- commits created by this remediation;
- exact changed-path inventory;
- protected Liturgy production paths changed: must be zero;
- Catena production/generated paths changed: must be zero;
- **Blocker A disposition** and proof the meta-test now executes under the normal gate;
- standalone browser-model exact count/runtime;
- **Blocker B disposition** and the selector semantics now covered;
- exact protected `day-missal.css` exception selector identity/count and confirmation the file itself was untouched;
- Scripture broad-selector disposition and changed selectors, if any;
- any additional real site-chrome hazards discovered and their dispositions;
- focused test results;
- `make check`/aggregate result with failure identities;
- full-discovery start/candidate totals and new identities;
- Chromium artifact comparison and every intentional changed identity;
- Catena regression result;
- public build result;
- exact stale release-binding path set;
- working-tree clean status;
- explicit statement that no merge, deployment, signing, binding refresh, protected-Liturgy edit, Catena product edit, Search work, acquisition work, or next lane was performed;
- exact next action: **independent cold rereview of the remediation candidate**.

---

## 12. Stopping line

After implementing only the authorized remediation, validating it, updating durable records, committing, pushing, verifying remote equality, and printing the final report, **stop**.

Do not merge.

Do not sign release bindings.

Do not request or exercise the Liturgy carve-out yourself.

Do not start the Catena Omnia roadmap.

The next actor must be an independent cold reviewer who decides whether the two `CHANGES_REQUIRED` findings are actually closed.