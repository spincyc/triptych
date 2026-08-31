# B0/B1 remaining remediation — browser-native selector oracle

You are the **implementation agent** for one final narrow B0/B1 remediation pass in `spincyc/triptych`.

Your task is to close the **one remaining substantive blocker** from the second independent cold review: the site-chrome selector analyzer is still unsound for valid CSS because it attempts to infer selector semantics in Python. Replace that unsafe decision mechanism with a browser-native semantic oracle, preserve everything already accepted, update the durable record truthfully, commit and push a new remediation candidate to the same feature branch, and stop for another independent cold rereview.

This is not a new product lane, not a CSS redesign, and not permission to reopen Blocker A, Catena, Catena Omnia, Scripture design, Search, acquisition, shared-shell cutover, or protected Liturgy.

---

## 1. Repository, branch, checkpoints, and authority

Repository:

`spincyc/triptych`

Target feature branch:

`impl/corpus-foundation-b0-b1`

Known first cold-review checkpoint:

`bda54d55c65e0447a26aff0cf76bc51f5fd54ca5`

Known first remediation candidate:

`de0bbc1aa1436a82b74346fda486fea6f398f3d1`

Known second cold-review instructions commit:

`9cb4ffe6545a829edf0f6346a8cd0f890229c5a2`

The second independent cold review disposition is:

- **B0/B1 — CHANGES_REQUIRED**;
- **Blocker A — CLOSED**;
- **Blocker B — OPEN**;
- prior Catena Omnia vision/roadmap dispositions remain standing;
- Scripture's mechanical scoping correction was independently accepted as behaving correctly;
- exact protected-Liturgy selector inventories were independently shown to detect removal and same-count substitution.

Fetch before doing anything. Record the exact fetched:

- `origin/main`;
- remote feature-branch head;
- merge base;
- branch distance from main;
- starting HEAD;
- clean-tree state.

Use a fresh full checkout or otherwise prove an uncontaminated checkout. **Do not use a worktree or shared index.**

If the remote branch has advanced beyond this instruction commit, inspect those commits first. Preserve valid unrelated/review-only work and restrict implementation to the remaining blocker unless a newly fetched governing authority materially changes ownership.

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
- `PROJECT-WORK.md`
- `promised-deliverables.toml`
- `Makefile`
- `tools/tests/test_browser_model_gate.py`
- `tools/tests/test_browser_collisions.py`
- `tools/tests/corpus_browser_gate.mjs` and other existing Chromium/CDP harnesses relevant to reuse
- `tools/public-alpha` and the public/preview layout-generation path
- `release/public-alpha/layout.html`
- all production stylesheets under `src/web/browser/`
- the four currently recorded protected Liturgy stylesheets
- `src/web/browser/scripture/scripture.css`

Read the prior cold-review record and the remediation record in `guidance/corpus-browser-implementation.md` §11.2/§11.3 and current `PROJECT-WORK.md`.

Protected Liturgy may be inspected as read-only evidence but not edited.

---

## 3. What is already closed — do not reopen it

### Blocker A is closed

The second cold reviewer independently proved the model-gate topology is now real:

- `check` reaches `check-browser-models`;
- `check-browser-models` reaches `check-browser-model-coverage`;
- the coverage meta-test runs under both normal and direct model-gate paths;
- a synthetic unlisted browser-JS-driving suite made both relevant targets fail;
- all seven `UNGATED_WITH_REASON` entries were independently found factual.

Do **not** redesign this topology unless your selector-oracle implementation directly breaks it. Keep its tests green and record it as unchanged.

### Scripture selector scoping is accepted implementation

The second cold reviewer independently verified the existing change from broad `a` / `a:hover` to page-scoped `:where(.plan-page, .track-page) ...`:

- generated page classes are on `<main>`, with built `<body>` classless;
- all intended Scripture content-link colors remain correct;
- footer links return to site-owned oxblood rather than leaked section color;
- focus, accessible names, skip-link behavior, overflow, and 320px width remain correct.

Do not redesign or revert this change.

### Exact protected inventories are useful and should remain

The current exact exception inventories for protected Liturgy survived mutation testing. Preserve the concept and readable exact inventories unless the current fetched owner state has legitimately changed.

Do not edit the protected Liturgy files.

---

## 4. The remaining blocker, exactly

The Python selector analyzer in `tools/tests/test_browser_collisions.py` still produces **false negatives for valid CSS**.

The second independent cold reviewer reproduced two classes of unsoundness.

### Finding 1 — unknown pseudo states fail open inside negation

The implementation treats unknown pseudos as satisfiable. Under `:not(...)`, that reverses conservative reasoning.

Concrete valid CSS examples the current analyzer wrongly accepts or fails to detect:

```css
a:not(:hover)
.site-header:not(:focus-within)
```

Real Chromium matches site chrome for both in ordinary states.

The reviewer also found valid case-insensitive attribute matching is missed, e.g.:

```css
[class~="SITE-HEADER" i]
```

### Finding 2 — route scope is derived from raw selector text rather than semantic positive conditions

The current `_names()`-style scope inference scans selector text and can invent route scope from tokens that do not constrain the match.

Concrete false-safe examples:

```css
a[href$=".html"]
body:has(.plan-page, .site-header) .site-footer a
:is(:not(.plan-page), .plan-page) a
```

Problems:

- `.html` is a value suffix, not a route class;
- `body:has(.plan-page, .site-header)` is global whenever the `.site-header` alternative is true;
- `:is(:not(.plan-page), .plan-page)` is a tautology, so the selector is globally broad;
- escaped identifiers and nested functional pseudos are not reliably interpreted by raw-text name extraction.

Therefore the existing claim that the analyzer “fails closed” is false.

The next implementation must close these semantic holes **without continuing to grow a hand-written CSS selector engine in Python**.

---

## 5. Required architecture — use the browser as the semantic selector oracle

The design goal is to stop deciding CSS selector truth by reimplementing selector semantics.

Use **real Chromium's selector engine** as the authority for whether a selector can match site chrome under the relevant route-marker states.

Prefer reusing the repository's existing dependency-free CDP/Chromium harness conventions rather than introducing a new framework, npm dependency, browser library, or server dependency.

The exact code organization is yours to design, but the semantic contract below is binding.

### 5.1 Build the actual shell DOM using repository-owned production machinery

Use the same public/preview layout generation the site actually uses. Do not author a synthetic lookalike shell by hand.

Generate or serve representative shell documents containing the real:

- skip link;
- `site-header`;
- Triptych mark/brand;
- global navigation links;
- release banner where applicable;
- generated `<main>`;
- `site-footer` and its links;
- public and preview shell variants if both matter to the current release machinery.

Route/page classes must be projected exactly where production puts them. The current repository projects browser page identity onto `<main>` in generated output; verify rather than assume this remains true.

### 5.2 Evaluate selectors using `querySelectorAll` / `matches` in Chromium

For each selector arm from each governed instrument stylesheet, ask Chromium directly whether the selector matches any chrome element in the rendered shell state.

Do not use Python emulation to determine whether `:not()`, `:is()`, `:where()`, `:has()`, attributes, escapes, nested functional pseudos, combinators, pseudo-state negation, or selector-list semantics match.

If Chromium rejects a selector as syntactically invalid/unsupported in the browser version that actually ships the gate, **fail closed** and report the selector. Do not silently permit it.

Pseudo-elements cannot be queried by DOM APIs in the same way as element selectors. Handle them explicitly and conservatively: either normalize them to the underlying element selector when that is semantically sound for the property-reach question, or fail closed/review them explicitly. Do not silently drop an arm because `querySelectorAll()` rejects a pseudo-element.

### 5.3 Determine positive route scope by comparing DOM states, not by extracting names

The key question is not “does the selector text mention a route class?”

The key question is:

> **Does this selector still reach site chrome when the intended route/instrument identity is absent?**

For each instrument stylesheet, construct at least:

1. a **neutral shell state** with the instrument/page route marker absent;
2. one or more **instrument shell states** with the stylesheet's legitimate page/route markers projected exactly where production puts them.

A selector that matches site chrome in the neutral state is **unscoped/unsafe**, regardless of whether route-looking text appears somewhere inside it.

A selector can be regarded as positively scoped only when its ability to reach the relevant chrome genuinely depends on the intended instrument/page state.

This semantic differential naturally must classify the reviewer's counterexamples correctly:

```css
/* unsafe in neutral shell */
a:not(:hover)
.site-header:not(:focus-within)
[class~="SITE-HEADER" i]
a[href$=".html"]
body:has(.plan-page, .site-header) .site-footer a
:is(:not(.plan-page), .plan-page) a
```

and must continue to permit legitimate positively scoped forms when route state actually matters, e.g. equivalents of:

```css
.sources-page .page-footer a
body:has(> .sources-page) .site-footer a
.plan-page a
.track-page a:hover
.route-only .site-header
```

Do not assume those literal selectors/classes are the only valid scopes. The oracle must judge behavior from DOM state.

### 5.4 Dynamic pseudo states

Ordinary page state is sufficient to expose many broad selectors such as `a:not(:hover)`, but do not assume one quiescent state proves every selector safe.

Inspect the actual production selectors and define the bounded dynamic-state matrix needed to avoid false safety for stateful selectors that can reach chrome. At minimum consider selectors involving:

- `:hover`;
- `:focus`;
- `:focus-visible`;
- `:focus-within`;
- `:active` where practical/relevant;
- enabled/disabled/checked states if they occur on chrome or governed selectors;
- target/hash state if relevant to production selectors.

The gate need not explore the infinite browser state space. It must cover the actual selector grammar/states present in the governed tree and fail closed for selector forms whose safety it cannot establish.

A good implementation may classify selector arms first by syntax/features and then ask Chromium under the required finite state set; the **truth of matching must remain browser-native**, not Python emulation.

### 5.5 Keep runtime bounded

Do not launch Chromium once per selector.

Prefer one or a small bounded number of browser sessions that:

- receive the shell fixtures once;
- evaluate all selector arms in batches;
- evaluate needed route-marker and dynamic states deterministically;
- return machine-readable results to the Python test.

Measure and report the focused collision-gate runtime before and after. Do not introduce an arbitrary budget solely to pass this task, but avoid turning normal unit discovery into hundreds of browser startups.

If Chromium is unavailable, follow existing repository policy for browser-dependent gates: state/implement the correct skip/fail behavior according to current governing guidance. Do not create a false green that claims semantic selector proof without a browser.

---

## 6. Keep source extraction and exact inventories separate from selector semantics

It is still reasonable for Python to:

- locate CSS rules/selector lists in tracked files;
- split or transport selector arms using a robust bounded parser/extractor;
- derive production stylesheet inventory;
- maintain readable exact protected-selector exception inventories;
- compare analyzer/oracle output to those inventories;
- coordinate Chromium and assert results.

But Python must no longer infer selector truth by scanning names or reimplementing matching semantics.

Review the current selector extraction itself for correctness around nested parentheses, commas in functional pseudos, comments, attributes, escapes, and at-rules. If the extraction step cannot reliably produce complete selector arms for the current production grammar, strengthen or replace that **extraction** layer narrowly. Do not conflate extraction with matching.

If an entire valid selector arm cannot be extracted/classified safely, fail closed and surface it for review.

---

## 7. Mandatory permanent regressions from the second cold review

Add permanent regressions proving the new browser-native oracle handles every reported false-negative case.

At minimum include:

### Must be detected as chrome-reaching / unsafe without positive route dependence

```css
a:not(:hover)
.site-header:not(:focus-within)
[class~="SITE-HEADER" i]
a[href$=".html"]
body:has(.plan-page, .site-header) .site-footer a
:is(:not(.plan-page), .plan-page) a
```

Also include:

- an escaped identifier case;
- nested functional pseudo case;
- a comma/grouped selector with one safe and one unsafe arm;
- an attribute selector containing punctuation/commas where extraction could be confused;
- representative descendant/child/adjacent/general-sibling combinators;
- at least one dynamic pseudo-state case where ordinary-state evaluation alone would be insufficient, if such a selector is in or plausibly admitted by the production grammar.

### Must remain recognized as legitimately route-dependent when semantics actually require route state

Test equivalents of:

```css
.sources-page .page-footer a
body:has(> .sources-page) .site-footer a
.plan-page a
.track-page a:hover
.route-only .site-header
```

For each important regression, where practical compare the oracle result against a direct independent `querySelectorAll()`/computed browser observation rather than only testing helper return values.

---

## 8. Re-audit the entire real production stylesheet tree

After the browser-native oracle exists, run it across every production stylesheet governed by this foundation test.

Do not assume the current four protected Liturgy files are the complete unsafe set.

For every selector arm that reaches chrome in neutral/global state:

### Protected/separately owned

If current authority protects it, do not edit it. Add/retain its **exact readable selector identity** in the protected exception inventory with owning authority and reason.

### Unprotected and mechanically page-scopable

If you discover another real unprotected selector of the same mechanical ownership class, fix it only if doing so is clearly within B0/B1 neutral scoping authority and requires no product/visual judgment. Prove the affected route in Chromium.

### Requires product/visual decision

Do not widen this remediation. Record it as an owner-blocked finding and stop that path.

Do not create broad exemptions to make the gate pass.

---

## 9. Preserve and independently revalidate the exact protected Liturgy inventories

The second cold review reported these current protected inventories:

- `liturgy/day-missal.css`: 12 selectors;
- `liturgy/reader-shell.css`: 3 selectors (`:root`, `html`, `html` in their distinct rule occurrences/identities);
- `liturgy/reader-instrument.css`: 2 selectors (`:root`, `:root`);
- `liturgy/reader-visual-reset.css`: 3 selectors (`:root`, `a:focus-visible`, `:root`).

Do not simply copy those counts. Re-read the current files and authority, and preserve exact normalized identities in the form the existing remediation established.

The gate must still fail when:

- one recorded protected unsafe selector is removed;
- one is replaced with a different unsafe selector while count stays constant;
- normalization changes would otherwise hide a materially different selector.

The browser-native oracle decides what is unsafe; the exact inventory decides which unsafe selectors are explicitly tolerated because another owner protects them.

**Do not edit protected Liturgy production files.**

`shared-shell-blocking-collisions-resolved` remains `blocked` while these protected unsafe selectors remain.

---

## 10. Preserve the accepted Scripture correction

Do not rewrite `src/web/browser/scripture/scripture.css` unless the new oracle reveals a direct new correctness issue in the already reviewed page-scoping change.

Re-run enough evidence to prove the new oracle still classifies the scoped Scripture rules as safe and the built routes remain correct:

- route classes on generated `<main>`;
- content links keep intended section styling;
- footer/global chrome does not receive Scripture-local styling;
- focus and accessible names remain correct;
- no horizontal overflow at 320px;
- forced colors remain acceptable if applicable.

No further aesthetic tuning is authorized.

---

## 11. Correct the known durable-record inaccuracy

The second cold reviewer identified a documentation issue in `PROJECT-WORK.md` around the prior claim that stale release bindings are **the whole reason** `make check` is red.

That is too strong because inherited red identities also exist at the base, including tool-registry failures and the existing example divergences.

Correct this narrowly and truthfully.

Distinguish:

- inherited/base red identities;
- branch-introduced deliberately stale release-binding identities;
- targets that echo the same stale-binding cause;
- unchanged `check-examples` divergences.

Also inspect `guidance/corpus-browser-implementation.md` §11.3 and any other durable record for the now-refuted statement that the Python selector analyzer “fails closed.” Update those claims to describe the browser-native oracle actually implemented and its measured limits.

Do not rewrite historical review dispositions. Preserve that the second cold review returned `CHANGES_REQUIRED` and that this pass is a remediation candidate awaiting independent rereview.

---

## 12. Hard boundaries

### Do not reopen Blocker A

No redesign of the browser-model gate unless required to keep it working. Its focused tests must remain green.

### Catena E0/E1 is closed

Do not modify:

- Catena HTML/CSS/JS/model;
- Catena generator;
- Catena generated data;
- Catena voice/projection/transport/cache/absence/refusal/URL behavior.

Run regression evidence only.

### Catena Omnia vision/roadmap remain accepted under their previous dispositions

Do not edit them unless this implementation uncovers a direct factual contradiction. This remediation should not.

### Protected Liturgy remains protected

Do not edit the four protected Liturgy stylesheets or any other protected Day/Propers production file.

### No shared-shell cutover

This task only strengthens the safety gate. It does not authorize installing the shared shell.

### No Search, acquisition, or next corpus lane

Do not begin them.

### No release signing

Do not refresh or hand-edit release bindings. The branch intentionally carried stale bindings for:

- `src/web/browser/sources/sources.css`;
- `src/web/browser/scripture/scripture.css`.

If this pass changes no other release-bound production bytes, the exact stale set should remain those two paths. Derive it rather than assume it.

No `refresh-release-bindings`, no release approval, no digest hand-editing.

---

## 13. Validation requirements

Use current repository commands after inspecting Makefile/guidance.

At minimum run/reproduce the applicable equivalents of:

### Selector-oracle focused validation

1. all `test_browser_collisions.py` tests;
2. the six mandatory cold-review counterexamples;
3. escaped/nested/attribute/grouped/combinator adversarial cases;
4. dynamic-state adversarial cases;
5. invalid/unsupported selector fail-closed behavior;
6. exact protected-inventory removal/substitution mutations;
7. full production stylesheet scan;
8. direct Chromium comparison showing the oracle agrees with browser matching for adversarial cases;
9. focused runtime measurement and browser-launch count/batching behavior.

### Blocker A regression

10. `test_browser_model_gate.py` remains green;
11. direct coverage target remains reachable;
12. do not need to repeat a large synthetic omission campaign unless the topology changed, but prove the closed blocker did not regress.

### Browser/build regression

13. `check-browser-static`;
14. `check-browser-harnesses`;
15. public preview/site build;
16. relevant real-Chromium artifact gate;
17. representative Scripture route proof;
18. no unexpected console/network/accessibility regression from the new testing machinery or any production scoping correction.

### Catena regression

19. current Catena generator/model check;
20. current focused Catena tests (previously 56);
21. current curated Catena production suite (previously 394);
22. existing browser Catena identity/focus evidence where required.

### Repository-wide identity comparison

23. full unit-test discovery on an appropriate remediation base and candidate;
24. compare failure **identities**, not only totals;
25. run `make -k check` or current governing aggregate and classify each red target by underlying cause;
26. `check-examples` identity comparison where still part of the matrix;
27. release-binding verification without refresh;
28. exact stale-binding path set.

The previous cold rereview reported:

- base `e135e65...`: 2,719 tests / 24 failures / 0 errors / 10 skips;
- candidate `de0bbc1...`: 2,750 / 24 / 0 / 10;
- all 24 failure identities identical;
- Chromium artifact: 2,290 identical rows = 1,850 pass / 212 inherited fail / 228 skip;
- browser static 6/6;
- browser harnesses 6/6;
- Catena 56/56 focused and 394/394 production;
- Catena route 95 pass / 14 inherited fail / 12 skip;
- `check-examples` base/candidate 16/212 divergences with identical command identities;
- exactly two intentionally stale binding paths: Scripture CSS and Sources CSS.

Treat those as historical claims to compare against the new candidate, not hard-coded success criteria.

---

## 14. Implementation design constraints

The desired outcome is **less bespoke CSS-semantics code**, not more.

A good candidate should delete, bypass, or demote the unsound Python matching/scope inference where Chromium can answer directly.

Do not keep the hand-written analyzer as the authoritative decision and merely add browser tests around a few counterexamples. The browser-native result must control the safety verdict.

It is acceptable to retain small Python helpers for parsing/extracting tracked CSS, building fixtures, normalizing exact exception identities, orchestrating CDP, and reporting results.

Avoid new third-party dependencies. Use the repository's current Node/Chromium/CDP capabilities.

Keep the test deterministic, static-host compatible, and understandable to a future maintainer.

Document the bounded semantic claim precisely. Do not claim “complete CSS proof” if the implementation proves only selectors under the repository's supported browser/version and fixture/state matrix.

---

## 15. Durable record updates

Update the minimum necessary records, likely including:

- `guidance/corpus-browser-implementation.md`;
- `guidance/corpus-browser-roadmap.md` if its candidate/disposition row needs an appended remediation entry;
- `PROJECT-WORK.md`;
- `promised-deliverables.toml` comments/evidence if required.

Record:

- second cold-review `CHANGES_REQUIRED` findings;
- Blocker A remains closed/unchanged;
- browser-native oracle architecture;
- exact shell fixtures/states used;
- selector extraction boundary;
- dynamic-state coverage;
- unsupported-selector fail-closed policy;
- exact protected inventories and owner authority;
- every additional real hazard found and dispositioned;
- focused oracle runtime/browser-session count;
- repository-wide validation identity results;
- exact stale-binding set;
- zero protected-Liturgy changes;
- zero Catena production/generated/generator changes;
- candidate awaits independent cold rereview.

Do **not** mark B0/B1 accepted yourself.

---

## 16. Git, push, and stopping line

Make coherent commits on:

`impl/corpus-foundation-b0-b1`

Push normally; no force push.

Fetch afterward and verify remote feature head equals local HEAD.

Leave the working tree clean and no stashes.

Then stop.

Do not merge, deploy, sign, refresh bindings, self-accept, modify protected Liturgy, modify Catena, begin Search/acquisition, or start any next lane.

---

## 17. Required final report

Return a concise but mechanically complete report containing:

- `STATUS: B0/B1 SELECTOR-ORACLE REMEDIATION CANDIDATE — AWAITING INDEPENDENT REREVIEW`
- branch;
- fetched `origin/main`;
- starting branch head;
- final candidate head;
- merge base;
- branch distance;
- commits created;
- remote equality and clean tree;
- exact changed-path inventory;
- protected-Liturgy changed paths: zero;
- Catena production/generated/generator changed paths: zero;
- Blocker A regression status;
- browser-native selector-oracle architecture;
- whether old Python semantic matching/scope inference remains authoritative (expected: no);
- exact adversarial counterexample results for all six cold-review cases;
- escaped/nested/attribute/grouped/combinator/dynamic-state results;
- invalid/unsupported selector fail-closed proof;
- browser batching/session count and focused runtime;
- full production stylesheet scan and any new hazards;
- exact protected Liturgy inventories and mutation-proof status;
- Scripture regression result;
- focused collision-test count/results;
- browser model/coverage results;
- full-discovery base/head totals and new failure identities;
- `make check`/aggregate red targets classified by root cause;
- Chromium artifact identity comparison;
- browser static/harness results;
- Catena regression results;
- public build/preview verification;
- `check-examples` identity classification;
- exact stale release-binding path set;
- durable records updated, including correction of the “whole reason make check is red” wording;
- unresolved externally owned blockers;
- explicit statement that no merge, deployment, signing, binding refresh, protected-Liturgy edit, Catena edit, Search, acquisition, or next lane was performed;
- exact next action: **independent cold Codex rereview of the selector-oracle remediation candidate**.

Implement only this remediation, commit, push, report, and stop.
