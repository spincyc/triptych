# B0/B1 selector-oracle remediation — independent cold Codex rereview

You are the **independent cold reviewer** for the browser-native selector-oracle
remediation of B0/B1 corpus foundation in `spincyc/triptych`.

Your job is to determine whether the one remaining substantive blocker of the
third independent cold review is genuinely closed — the site-chrome selector
verdict was unsound because Python inferred CSS selector semantics — whether the
replacement introduces any new correctness, ownership, or record defect, and
whether B0/B1 is now acceptable for its next integration/release-owned step.

This is a **review and disposition task**, not an implementation task.

Do not trust the implementation report, the commit message, the durable record,
the prior chat, or these instructions as proof of anything. Recover the
repository state yourself, reproduce the evidence, attack the new oracle
adversarially — including by making the oracle wrong on purpose — record an
independent disposition, and stop.

You must not implement, merge, deploy, release-sign, refresh release bindings,
approve a release, edit protected Liturgy production, edit Catena production,
generated data, or generator code, cut over the shared shell, begin Search,
begin Catena Omnia acquisition, or start any next product lane.

---

## 1. Repository, branch, and exact refs

Repository:

`spincyc/triptych`

Feature branch:

`impl/corpus-foundation-b0-b1`

Known refs at dispatch:

| Ref | SHA | What it is |
| --- | --- | --- |
| remediation candidate to rereview | `73363fcbc` | "Decide site-chrome selector safety in the browser" |
| remediation base / instruction commit | `2440e3e84` | "Add browser-native selector oracle remediation instructions", which added `guidance/NEXT-CLAUDE-B0B1-BROWSER-SELECTOR-ORACLE.md` |
| third cold-review instruction commit | `9cb4ffe65` | "Add cold Codex rereview instructions for B0/B1 remediation", which added `guidance/NEXT-CODEX-B0B1-COLD-REREVIEW.md` |
| first cold-review checkpoint (`CHANGES_REQUIRED`) | `bda54d55c` | first independent review |
| first remediation candidate | `de0bbc1aa` | Blocker A close plus the Python analyzer this pass replaces |
| `origin/main` and merge base at dispatch | `094379074` | the merge base is `origin/main` itself |
| branch distance from main | 12 commits ahead, 0 behind | at dispatch |

**Fetch first. Do not assume any of those refs are still current.**

Use a fresh full checkout, or otherwise prove an uncontaminated checkout. Do not
use a worktree, a shared index, or a directory another agent holds.

Record before reviewing:

- exact fetched `origin/main`;
- exact remote `impl/corpus-foundation-b0-b1` head;
- merge base;
- branch distance from main in both directions;
- whether `73363fcbc` is still the branch head or only an ancestor;
- clean working-tree state and absence of stashes;
- any later commits, and for each whether it is review-only, unrelated, or
  materially changes the candidate.

If the branch has advanced beyond `73363fcbc`, review the actual remote state
but keep the `2440e3e84..73363fcbc` delta distinguishable from later work. Do
not attribute later work to this remediation, and do not credit this remediation
with a fix that landed afterwards.

---

## 2. Recover governing authority before judging implementation

Read the current versions of at least:

- `AGENTS.md`
- `guidance/NEXT-CLAUDE-B0B1-BROWSER-SELECTOR-ORACLE.md` — the authority this
  candidate had to satisfy; every binding clause in its §5, §6, §7, §8, §9,
  §11, §12 is a promise you must test rather than read
- `guidance/NEXT-CODEX-B0B1-COLD-REREVIEW.md` — the third cold review's own
  instructions, so you can tell which findings were already dispositioned
- `guidance/corpus-browser-implementation.md`, especially §11.2, §11.3 (whose
  "fails closed" paragraph was corrected in place) and the new §11.4
- `guidance/corpus-browser-master-plan.md`
- `guidance/corpus-browser-vision.md`
- `guidance/corpus-browser-roadmap.md`
- `guidance/catena.md`, `guidance/catena-omnia-vision.md`,
  `guidance/catena-omnia-roadmap.md`
- `guidance/liturgy-browser-vision.md`
- `PROJECT-WORK.md`, especially `### Selector-oracle remediation, 2026-08-31`
  and the preceding remediation subsection it corrects
- `promised-deliverables.toml`

Inspect directly:

- `tools/tests/site_chrome_selector_oracle.mjs` (new, ~840 lines)
- `tools/tests/test_browser_collisions.py` (rewritten)
- `tools/tests/test_browser_model_gate.py`
- `Makefile`
- `tools/public-alpha` and the real `wrap_in_layout` / `browser_page_parts` path
- `release/public-alpha/layout.html`
- every production stylesheet under `src/web/browser/`
- `src/web/browser/scripture/scripture.css`, `index.html`, `track.html`
- the four protected Liturgy stylesheets recorded as site-chrome exceptions

Protected Liturgy files are read-only evidence for this review. Do not edit them
because you find their selectors broad, ugly, or inconvenient. Catena E0/E1 is a
closed product lane: review its regression evidence, not its design.

---

## 3. What is already dispositioned — do not relitigate

- **Blocker A (the coverage meta-test outside its own gate) is CLOSED**, proved
  independently by the third cold review. Verify only that it did not regress.
- **Scripture's mechanical page scoping** (`:where(.plan-page, .track-page) a`
  and `:hover`) was independently accepted as behaving correctly, including its
  footer-colour disclosure. Verify only that the new oracle still classifies it
  safe and that the routes still render correctly.
- **The exact protected Liturgy inventories** already survived removal and
  same-count substitution mutation. Verify that the browser-derived inventory
  reproduces them and that mutation detection survived the rewrite.
- **Catena Omnia vision (`ACCEPT_WITH_CORRECTIONS`, correction incorporated) and
  roadmap (`ACCEPT`)** stand. Do not review them again; reopen only on a direct
  factual contradiction introduced by this candidate or by newly fetched
  mainline authority.

---

## 4. The claims to disprove

Everything below is a **claim the candidate makes**, not a finding you may
adopt. Your task for each is to attempt disproof by independent observation, not
confirmation by reading the record that asserts it. For each claim record:
disproved, not disproved, or could not be tested and why.

### 4.1 Architecture claims

1. **Chromium and not Python decides selector safety.** The safety verdict for
   every governed selector arm is produced by a real browser's selector engine,
   and no Python code path can return "safe" on its own reasoning. Prove there
   is no residual Python decision — including no fallback, cache, allowlist,
   short-circuit, or exception handler — that can yield a safe verdict without
   the browser having answered.
2. **The hand-written matcher and scope inferencer are deleted.** The compound
   parser, attribute matcher, combinator walker, negation stripper, scope
   inferencer, and the in-memory chrome element model that duplicated
   `layout.html` are gone from `tools/tests/test_browser_collisions.py`, not
   merely unused or renamed. Diff `2440e3e84..73363fcbc` and search the tree.
3. **Python keeps only extraction, identity normalization, orchestration, and
   inventory comparison.** Judge whether the retained extraction layer is itself
   correct for the current production grammar: nested parentheses, top-level
   comma splitting with quotes/brackets respected, comments, escaped
   identifiers, attribute values containing commas and punctuation,
   pseudo-elements, at-rule bodies (`@media`, `@supports`). An arm that silently
   disappears from extraction is a blocker regardless of how sound the browser
   verdict is for the arms that survive.
4. **The shells are the build's own.** All 36 states are rendered by
   `wrap_in_layout` from `tools/public-alpha`, not by a second copy of the
   layout: two neutral shells (public and preview, page identity absent from
   `<main>`), thirteen published browser pages as the build renders them, and
   four site pages outside the browser tree. Verify the count, the projection of
   page classes onto `<main>` rather than `<body>`, and that the preview state
   is where the release banner is judged. Look for chrome-like nodes inside
   `<main>` or content-like nodes outside it that would invalidate the
   boundary.
5. **The verdict is a differential, not a name scan.** An arm is unsafe when it
   reaches site chrome in the neutral shell, whatever route-looking text it
   carries; it is positively scoped only when its reach genuinely depends on an
   identity the layout does not own. Attack this: construct an arm whose
   route-looking text is inert and confirm it is called unsafe, and an arm whose
   scope is real and confirm it is called safe.

### 4.2 Semantic claims

6. **All six cold-review counterexamples are caught**, each with a recorded
   witness sub-state:

   ```css
   a:not(:hover)
   .site-header:not(:focus-within)
   [class~="SITE-HEADER" i]
   a[href$=".html"]
   body:has(.plan-page, .site-header) .site-footer a
   :is(:not(.plan-page), .plan-page) a
   ```

   Feed each through the oracle yourself rather than reading the test's expected
   values, and independently corroborate at least the non-obvious ones with a
   direct `querySelectorAll()` observation in the same rendered shell.

7. **Legitimately route-scoped forms still pass.** Equivalents of:

   ```css
   .sources-page .page-footer a
   body:has(> .sources-page) .site-footer a
   .plan-page a
   .track-page a:hover
   .route-only .site-header
   ```

   remain safe. A gate that calls everything unsafe is not sound, it is useless;
   check for over-refusal as carefully as for under-refusal.

8. **Invalid and unsupported arms fail closed as a stated refusal**, never
   silently. Confirm the reported refusals (`..dot`, `:not()`, an unterminated
   attribute, `%bad`, `a:visited`) and add your own malformed and
   exotic-but-valid forms. Confirm `:visited` is refused because its truth is
   withheld from script, and that the refusal is surfaced in output rather than
   folded into a pass.
9. **Pseudo-element arms are judged conservatively by their origin element**,
   because `querySelectorAll('*::before')` matches nothing — the most dangerous
   possible answer — and the direction of that over-approximation is proved
   through the style engine by reading a non-inherited declaration back on the
   pseudo-element. Verify the sentinel actually proves the direction rather than
   asserting it, and that no pseudo-element arm is dropped.
10. **The bounded user-state walk is sufficient for the actual grammar.**
    Pointer over every chrome leaf, a held press, keyboard focus after one real
    Tab (so `:focus-visible` holds), and the document fragment target, run on
    the two neutral shells plus one published preview page, with a quiescent
    pass on every state. Verify each of `:hover`, `:focus`, `:focus-visible`,
    `:active`, `:target` is reachable only through its own sub-state, and test
    the stated reason the walk omits `:disabled`, `:checked`, `:open` — that the
    layout emits no form control, `<details>`, or `<dialog>` — as a measured
    fact rather than an assumption. If any chrome state is reachable in
    production but unreachable in the walk, say so.

### 4.3 Coverage and inventory claims

11. **The four protected Liturgy inventories are exactly 12 / 3 / 2 / 3** for
    `src/web/browser/liturgy/day-missal.css`, `reader-shell.css`,
    `reader-instrument.css`, `reader-visual-reset.css`, derived by the browser
    rather than transcribed. Derive them independently and compare exact ordered
    identities, not counts.
12. **The inventories are mutation-proof** against removal, against substitution
    that keeps the count while changing identity, and against a substitution
    whose commas sit inside a functional pseudo (the case naive normalization
    would hide). Perform all three mutations yourself and prove the suite fails
    for each, then restore.
13. **Zero new hazards exist across 1,193 production arms**, with the per-file
    unsafe inventory being browser-core 10 (its own job), day-missal 12,
    reader-instrument 2, reader-shell 3, reader-visual-reset 3, and every other
    file 0, in about 2.6 s over 72 navigations and 431 evaluations with zero
    refusals. Run the full scan and also search the tree manually as a second
    method — tag selectors, `body`/`html`/`:root` rules, layout-owned class
    names, focus rules, arms hidden inside selector lists, negative pseudo-class
    patterns, broad descendants that can reach header or footer links. Any real
    unprotected hazard the oracle misses is `CHANGES_REQUIRED`.
14. **Scripture's accepted `:where(.plan-page, .track-page)` scoping classifies
    safe** under the new verdict, and both routes still render correctly:
    content-link colours, footer links site-owned, focus, accessible names, skip
    link, no horizontal overflow at 320px.
15. **The oracle uses one browser session and the focused suite is 34 tests in
    about 9 s**, with the full-tree scan a single batched request. Verify the
    session count and batching behaviour empirically — count launches, not
    claims — and confirm normal unit discovery has not acquired hundreds of
    browser startups.
16. **Blocker A stays closed**: `test_browser_model_gate` is 22 tests OK and the
    topology is unchanged. Confirm `check` still reaches
    `check-browser-models`, which still reaches `check-browser-model-coverage`,
    which still executes the meta-test. A short adversarial re-proof is enough;
    a full omission campaign is not required unless the topology moved.

---

## 5. Adversarially mutate the oracle itself

Reading the oracle's output only tells you what it says. This section is
mandatory and is the core of the rereview: **make the oracle wrong on purpose,
and prove the suite notices.**

A gate whose own correctness is unverified is a gate that will silently rot. For
each mutation below, apply it, run the focused suite, record whether it fails,
and revert:

1. **Neuter the neutral shell.** Give the neutral shell the page identity it is
   supposed to lack (or project page classes onto `<body>` instead of `<main>`)
   and prove the counterexample tests fail rather than passing on a shell that
   can no longer expose unscoped reach.
2. **Break the differential.** Make the unsafe verdict depend on the instrument
   state rather than the neutral state, and prove at least one counterexample
   flips and is caught.
3. **Fail open instead of closed.** Make a Chromium-rejected arm, and separately
   a `:visited` arm, return safe instead of refused, and prove the refusal tests
   fail.
4. **Drop the pseudo-element handling.** Send a pseudo-element arm straight to
   `querySelectorAll` so it matches nothing, and prove the suite fails rather
   than silently accepting the arm.
5. **Weaken the state walk.** Remove the hover, the held press, the Tab focus,
   and the fragment target one at a time, and prove the corresponding
   state-keyed arm is no longer caught and that a test fails for each.
6. **Corrupt extraction.** Split selector lists naively on every comma (so a
   comma inside a functional pseudo or an attribute value breaks an arm), and
   prove the suite fails rather than losing an arm quietly.
7. **Shrink the governed set.** Omit one production stylesheet, or one published
   page state, from the scan and prove a test fails rather than the inventory
   simply reporting fewer arms.
8. **Silence the browser.** Make the CDP session return an empty or partial
   result set, and prove the suite errors or fails rather than concluding that
   nothing reaches chrome. A gate that reads absence of evidence as safety is a
   blocker.
9. **Break the skip path.** Confirm that where no Chromium can be driven the
   selector tests skip with a stated reason and never pass on a weaker answer,
   and that the skip cannot be reached while a browser is in fact available.

Do not commit any mutation. After each, restore the tree and prove it is clean.
If any mutation leaves the suite green, that is a defect of the gate and
`CHANGES_REQUIRED` unless you can show another test in the reachable `check`
path catches it.

---

## 6. Durable-record audit — hunt overstatement specifically

The candidate updated `PROJECT-WORK.md`, `guidance/corpus-browser-implementation.md`
§11.4, `guidance/corpus-browser-roadmap.md`, and `promised-deliverables.toml`.
Read them against what you measured, not against the commit message.

Check at minimum:

- the corrected wording that **stale bindings are not the whole reason
  `make check` is red** — verify the correction is truthful and complete, that
  inherited base red identities, branch-introduced stale-binding identities,
  targets that merely echo the stale-binding cause, and unchanged
  `check-examples` divergences are each separated correctly, and that the older
  overstated claim is corrected rather than deleted from the history;
- the **now-refuted older claim that the Python analyzer "failed closed"** —
  verify §11.3 is corrected in place, that the correction states the truth (it
  failed closed only on forms it could not parse, and reported scoped precisely
  where it did not understand), and that no other record still repeats the
  refuted claim;
- that §11.4's stated non-claims are honest: no specificity or cascade
  computation, no `@media`/`@supports` condition evaluation, no complete CSS
  semantics beyond Chromium's own, and scope keyed on any non-layout class
  treated as positive scope — including a class every page carries. Decide
  whether that last convention is still acceptable or has become a loophole;
- every number in the record corresponds to a command you actually ran;
- the third cold review's `CHANGES_REQUIRED` disposition is preserved, not
  rewritten away;
- this pass is recorded as a candidate awaiting independent rereview and B0/B1
  is not self-accepted;
- `shared-shell-blocking-collisions-resolved` remains `blocked`;
- the exact protected inventories and their owning authority are recorded;
- no document grants merge, release, signing, deployment, Liturgy, or Catena
  authority it does not own.

Narrow documentation corrections needed to leave a truthful review record are
permitted, committed separately and identified by SHA. Do not repair substantive
implementation defects yourself; return `CHANGES_REQUIRED` for those.

---

## 7. Changed-path and ownership audit

The candidate reports six changed paths in `2440e3e84..73363fcbc`:

- `tools/tests/site_chrome_selector_oracle.mjs` (new)
- `tools/tests/test_browser_collisions.py`
- `PROJECT-WORK.md`
- `guidance/corpus-browser-implementation.md`
- `guidance/corpus-browser-roadmap.md`
- `promised-deliverables.toml`

Verify that inventory independently, and require:

- **zero production bytes changed** — the candidate claims none, which is why
  the stale binding set should be unchanged;
- zero protected Liturgy production changes;
- zero Catena production, generated-data, or generator changes;
- no release-binding edit, refresh, or digest hand-edit;
- no release approval or signing change;
- no shared-shell cutover;
- no Search, acquisition, or next-lane implementation.

Any additional changed path must be classified, not assumed harmless.

---

## 8. Known red baseline — compare identities, not exit codes

`make check` is red at the base for reasons this remediation does not cause.
Compare failure **identities** against the baseline below and say which set you
compared against. Reproduce rather than quote; if your host differs, explain
why, and treat identity agreement as the standard.

### Full unit discovery

| Tree | Tests | Failures | Skips |
| --- | --- | --- | --- |
| base `2440e3e84` | 2,750 | 24 | 11 |
| candidate `73363fcbc` | 2,752 | 24 | 10 |

Failure identities are claimed identical on both sides, with no new identity.

### `make -k check`

Red targets, and the cause each is claimed to have:

- `check-release-bindings` — two deliberately stale paths,
  `src/web/browser/scripture/scripture.css` and
  `src/web/browser/sources/sources.css`;
- the **same** release-binding oracle echoed inside `check-browser-models`;
- inherited
  `test_day_reader_integration.DayReaderIntegrationTests.test_accepted_shell_and_visual_oracle_hashes_are_current`;
- `check-examples` — 16 divergences of 212 captured examples, of which 12 are
  inherited (they diverge at the base too) and 4 are the stale-binding cause
  echoed through captured transcripts.

### Green baselines

- Chromium artifact gate: 2,290 rows = 1,850 pass / 212 inherited fail / 228
  skip;
- `check-browser-static`: 6/6;
- browser harnesses: 6/6;
- Catena: 56 focused tests and 394 production tests.

### Stale release bindings

Derive the exact stale set yourself. It should be exactly the two paths above.
Verify no third path is stale because of this branch, that neither digest was
hand-edited, that no refresh command was run or committed, that the oracle
appearing inside another target is the same cause, and that `check-examples`
divergences are classified rather than hiding a separate product regression.

Do not refresh or sign bindings. Do not mark B0/B1 defective merely because a
candidate deliberately carries unsigned changed production bytes from an earlier
pass. Do return `CHANGES_REQUIRED` if the stale state is broader, differently
caused, unexplained, or misrepresented.

---

## 9. Validation matrix

Use the repository's current commands after inspecting `Makefile` and guidance;
do not trust stale command names from this file. At minimum run or reproduce the
applicable equivalents of:

**Selector oracle** — the full `test_browser_collisions.py` suite; the six
counterexamples; the positively scoped forms; escaped, nested, comma-bearing
attribute, grouped, and all-combinator cases; dynamic-state cases; refusal
cases; the protected-inventory removal, substitution, and functional-pseudo
substitution mutations; the full production tree scan; direct
`querySelectorAll()` and computed-style corroboration; session count, batching,
and runtime; every mutation in §5.

**Blocker A** — `test_browser_model_gate.py`; the direct coverage target; the
model gate itself; a bounded re-proof that an unlisted browser-driving suite
still fails the coverage target.

**Browser and build** — `check-browser-static`; browser harnesses; public
preview/site build as current guidance requires; the real-Chromium artifact
gate; representative Scripture route proof; release-binding verification
**without refreshing**; `check-examples` identity comparison.

**Catena regression** — generator/model validation; the focused suite (56); the
curated production suite (394); real-browser Catena identities and focus
behaviour where the existing gate defines them. Do not reopen Catena design
because unrelated inherited failures exist.

**Repository-wide** — full unit discovery on base and candidate; `make -k check`
with every red target classified by root cause.

---

## 10. Decision standard

Your primary disposition is for **B0/B1 after the selector-oracle remediation**.
Use exactly one of:

- `ACCEPT`
- `ACCEPT_WITH_CORRECTIONS`
- `CHANGES_REQUIRED`

### ACCEPT

Both prior blockers are genuinely closed, the browser-native verdict is sound
within a bounded and honestly stated claim, no new implementation blocker
exists, ownership boundaries are intact, and every remaining red identity is
inherited or a deliberately unsigned release-owned condition.

### ACCEPT_WITH_CORRECTIONS

Implementation is substantively acceptable but narrow durable-record
inaccuracies need correction. Do not use this status to waive an implementation
or gate defect.

### CHANGES_REQUIRED

Any substantive defect, including:

- any Python path that can still return a safe verdict without the browser;
- a residual scope inference, allowlist, or fallback that decides safety;
- a false negative on a real or plausible repository selector class;
- an unsupported or invalid arm accepted rather than refused and reported;
- an arm silently lost in extraction, or a stylesheet or state silently outside
  the scan;
- an oracle mutation from §5 that leaves the suite green;
- absence of browser evidence read as safety;
- a real unprotected site-chrome hazard remaining;
- a protected inventory that can mutate without detection;
- a protected exception without actual owner authority;
- Scripture scoping broken, or a route regression;
- a new failure identity caused by the remediation;
- an unexpected changed path, especially any production byte;
- a Catena regression caused by the remediation;
- a stale-binding set broader or differently caused than represented;
- a durable record that overstates what the gate proves.

Do not manufacture changes to reach perfection. The standard is whether B0/B1
now truthfully provides the bounded protection it claims, and whether the gate
that claims it would notice if it stopped being true.

---

## 11. Required final report

Return a concise but mechanically complete report containing:

- `STATUS`
- `B0/B1 DISPOSITION` — one of `ACCEPT` / `ACCEPT_WITH_CORRECTIONS` /
  `CHANGES_REQUIRED`
- reviewed branch
- exact fetched `origin/main`
- exact starting remote branch head
- exact remediation commit reviewed, and whether it is still the head
- final branch head after any review-record correction
- merge base and branch distance from main
- clean-tree and no-stash state
- exact changed-path inventory for `2440e3e84..73363fcbc`
- production bytes changed: expected zero
- protected-Liturgy changed paths: expected zero
- Catena production/generated/generator changed paths: expected zero
- per-claim disposition for every claim in §4, marked disproved / not disproved
  / untestable with reason
- whether Python can still decide selector safety anywhere (expected: no), with
  the evidence
- deletion proof for the matcher, attribute matcher, combinator walker,
  negation stripper, scope inferencer, and in-memory chrome model
- extraction-layer audit result
- shell-fixture audit: state count, `wrap_in_layout` provenance, page-class
  projection, `<main>` boundary
- results for all six cold-review counterexamples, with witness sub-states
- results for the positively scoped forms
- escaped / nested / attribute / grouped / combinator / dynamic-state results
- refusal results, including `:visited` and invalid arms
- pseudo-element handling and sentinel disposition
- state-walk sufficiency and its measured bound
- **§5 oracle-mutation table: each mutation, whether the suite failed, and the
  verdict**
- full production tree scan result, per-file unsafe inventory, and any hazard
  found by manual second-method search
- exact four-file protected inventory (expected 12 / 3 / 2 / 3) and authority
  disposition
- exact-mutation proof for the inventories: removal, same-count substitution,
  functional-pseudo comma substitution
- Scripture classification and route/computed-style/accessibility disposition
- browser session count, batching behaviour, and focused runtime
- focused test counts and results
- Blocker A regression result, including topology re-proof
- full-discovery base/candidate totals and any new failure identity
- `make -k check` result with every red target classified by cause, compared
  against the §8 baseline
- Chromium artifact base/candidate identity comparison
- `check-browser-static` and harness results
- Catena regression results
- public build/preview result
- `check-examples` classification
- exact stale release-binding path set
- durable-record accuracy disposition, naming explicitly the stale-binding
  wording correction and the refuted "fails closed" claim
- any documentation-only review-record correction commit SHA
- unresolved externally owned blockers, including whether
  `shared-shell-blocking-collisions-resolved` must stay blocked
- prior Catena Omnia vision/roadmap dispositions still standing, unless a real
  contradiction was found
- explicit statement that no merge, deployment, signing, binding refresh,
  protected-Liturgy edit, Catena edit, Search, acquisition, or next lane was
  performed
- **exact next authorized action**, stated narrowly in terms of the governing
  roadmap and ownership — likely integration or release-owned handling of
  accepted production paths and the still-protected Liturgy blocker — rather
  than "continue development"

---

## 12. Stopping line

Record the review, commit it, and stop. Do not implement or accept anything
else.
