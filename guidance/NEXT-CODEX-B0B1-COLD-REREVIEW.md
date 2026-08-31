# B0/B1 remediation — independent cold Codex rereview

You are the **independent cold reviewer** for the B0/B1 corpus-foundation remediation in `spincyc/triptych`.

Your job is to determine whether the remediation candidate genuinely closes the two blockers previously returned as `CHANGES_REQUIRED`, whether it introduces any new correctness or ownership defect, and whether B0/B1 is now acceptable for its next integration/release-owned step.

This is a **review and disposition task**, not an implementation task.

Do not trust the implementation report, commit message, prior chat, or these instructions as proof. Recover the repository state, reproduce the evidence, attack the new tests and selector analyzer adversarially, record an independent disposition, and stop.

Do not merge, deploy, release-sign, refresh release bindings, alter protected Liturgy production, change Catena production, begin Search, begin Catena Omnia acquisition, cut over the shared shell, or start another feature lane.

---

## 1. Repository, branch, and known checkpoints

Repository:

`spincyc/triptych`

Feature branch:

`impl/corpus-foundation-b0-b1`

Known independent-review checkpoint that returned `CHANGES_REQUIRED`:

`bda54d55c65e0447a26aff0cf76bc51f5fd54ca5`

Known remediation-instruction commit:

`e135e65bbea80877eb75a39945b750fc7566642f`

Known remediation candidate to rereview:

`de0bbc1aa1436a82b74346fda486fea6f398f3d1`

Last known `origin/main` and merge base when the candidate was produced:

`09437907472581df4a8969010bd494249a3539a5`

**Fetch first. Do not assume any of those refs are still current.**

Use a fresh full checkout or otherwise prove an uncontaminated checkout. Do not use a worktree or shared index.

Record before reviewing:

- exact fetched `origin/main`;
- exact remote `impl/corpus-foundation-b0-b1` head;
- merge base;
- branch distance from main;
- whether `de0bbc1...` is still the current remediation candidate or merely an ancestor;
- clean working-tree state;
- any later commits and whether they are review-only, unrelated, or materially change the candidate.

If the branch has materially advanced beyond the candidate, review the actual remote state but distinguish the `de0bbc1...` remediation delta from later changes. Do not silently attribute later work to the remediation.

---

## 2. Recover governing authority before judging implementation

Read the current versions of at least:

- `AGENTS.md`
- `guidance/corpus-browser-master-plan.md`
- `guidance/corpus-browser-vision.md`
- `guidance/corpus-browser-roadmap.md`
- `guidance/corpus-browser-implementation.md`
- `guidance/catena.md`
- `guidance/catena-omnia-vision.md`
- `guidance/catena-omnia-roadmap.md`
- `guidance/liturgy-browser-vision.md`
- `PROJECT-WORK.md`
- `promised-deliverables.toml`
- the prior independent-review diff at `bda54d55...`
- the remediation diff from `e135e65...` to `de0bbc1...`

Inspect directly:

- `Makefile`
- `tools/tests/test_browser_model_gate.py`
- `tools/tests/test_browser_collisions.py`
- `release/public-alpha/layout.html`
- `tools/public-alpha` and the actual layout/wrapping code imported by the collision tests
- `src/web/browser/shared/browser-core.css`
- all production stylesheets under `src/web/browser/`
- `src/web/browser/scripture/scripture.css`
- `src/web/browser/scripture/index.html`
- `src/web/browser/scripture/track.html`
- the four protected Liturgy stylesheets now recorded as site-chrome exceptions

Protected Liturgy files are read-only evidence for this review unless a newer explicit authority has released them. Do not edit them merely because the reviewer finds them ugly, broad, or technically inconvenient.

Catena E0/E1 remains a closed product lane. Review its regression evidence, not its design.

---

## 3. Prior blockers that must now be independently closed

The previous cold review returned two blockers.

### Blocker A — the coverage meta-test was outside the gate it claimed to protect

The prior defect was:

- `make check` reached `check-browser-models`;
- `check-browser-models` ran explicitly named browser-driving test modules;
- `test_browser_model_gate.py` contained the assertion that discovers browser-JS-driving suites missing from both the named gate and `UNGATED_WITH_REASON`;
- but that meta-test itself was not reached by the normal `make check` path.

Therefore future omission could remain silent while `make check` passed.

The remediation claims to close this with:

- a separate `BROWSER_MODEL_GATE_TESTS` variable;
- a `check-browser-model-coverage` target;
- `check-browser-models: check-browser-model-coverage`;
- topology tests that walk prerequisites and inspect dry-run recipes;
- adversarial proof using a temporary unnamed browser-driving suite.

Do not accept that architecture from inspection alone. Reproduce it.

### Blocker B — the site-chrome detector proved too little

The prior detector missed:

- broad element selectors such as `a` and `a:hover`;
- negative pseudo-class pseudo-scope such as `.site-header:not(.route-only)`;
- replacement of one protected selector with another while retaining the same count.

A real unprotected example existed in `src/web/browser/scripture/scripture.css`.

The remediation claims to close this by:

- rendering the actual public/preview shell through the build's own wrapping code;
- parsing shell/chrome elements while excluding page-content subtree semantics appropriately;
- matching selector arms against actual chrome elements;
- treating scope as positive rather than merely noticing a foreign class token;
- explicitly handling combinators plus `:not()`, `:root`, `:is()`, `:where()`, and `:has()`;
- failing closed on selector syntax the bounded analyzer cannot classify;
- replacing a count-only exception with exact ordered selector inventories across four protected Liturgy files;
- mechanically scoping the real Scripture `a`/`a:hover` rules through page identity.

Again: do not accept this because the suite grew large. Attack it.

---

## 4. Cold review of Blocker A — make/test topology

Answer each question explicitly.

### 4.1 Is the meta-test genuinely unavoidable?

Prove from the actual Make dependency graph that:

- `make check` reaches `check-browser-models`;
- `check-browser-models` reaches `check-browser-model-coverage`;
- `check-browser-model-coverage` actually executes `test_browser_model_gate.py`;
- a direct `make check-browser-models` also executes it;
- the test is not only named in a variable that the recipe never consumes;
- a future maintainer cannot remove the dependency while the supposedly protective topology tests still pass trivially.

Use both source inspection and execution/dry-run evidence.

### 4.2 Preserve the semantic split

Confirm that:

- `BROWSER_MODEL_TESTS` still means browser-JS-driving suites;
- the meta-test is not falsely classified as one of them;
- explicit naming remains deliberate rather than a glob;
- `check-tests` remains separate and opt-in;
- the remediation did not quietly turn normal `make check` into the entire unit-test corpus.

### 4.3 Re-audit every exclusion

Independently verify all entries in `UNGATED_WITH_REASON`.

For each exclusion establish:

- the suite exists;
- it really drives browser JavaScript if that is why it is in scope;
- the stated alternative target actually exists;
- that alternative target is really reachable from `check` if the reason claims it is;
- the target actually executes the claimed suite/model rather than only being similarly named;
- the closed Catena production-suite exclusion and prototype exclusion remain legitimate under current authority.

A stale reason is a defect even if the omission detector is technically green.

### 4.4 Adversarial omission proof

Reproduce the exact failure mode independently.

Create a bounded temporary `test_*.py` that clearly:

- invokes Node;
- names/reaches browser JavaScript under `src/web/browser`;
- is absent from `BROWSER_MODEL_TESTS`;
- is absent from `UNGATED_WITH_REASON`.

Verify at least:

- `make check-browser-model-coverage` fails;
- `make check-browser-models` fails before silently running past the omission;
- the relevant `make check` path cannot remain green because of the missing suite.

Delete the mutation and prove the tree returns to the intended state.

Do not commit synthetic adversarial files.

### 4.5 Runtime and failure semantics

Measure the actual repaired browser-model gate.

The implementation reported approximately:

- 13 model modules;
- 401 tests across the model loop/coverage topology;
- about 175 seconds in a non-fail-fast measurement;
- direct `make check-browser-models` currently red only when the stale release-binding oracle is encountered.

Reproduce the real count/runtime and classify every failure by identity.

Do not equate an exit code with a model regression. If the only red identity is an intentionally stale release binding, state that precisely.

Also determine whether coupling a release-binding oracle into the browser-model gate remains acceptable technical debt or has become a blocker to the gate's claimed semantic boundary. Do not invent a blocker solely because the layering is imperfect; decide whether it threatens correctness, diagnosability, or future maintenance enough to require another change.

---

## 5. Cold review of Blocker B — selector/chrome analyzer

This is the highest-risk part of the remediation because the test implementation grew substantially. Review it as a bounded static analyzer, not as ordinary unit-test boilerplate.

### 5.1 Verify the shell model is actually the production shell model

Confirm that the test really uses the repository's production `wrap_in_layout`/public-alpha machinery rather than reconstructing a lookalike shell.

Inspect what is rendered for:

- normal public shell;
- preview shell;
- page classes projected onto generated `<main>`;
- body/main/footer/header relationships;
- skip link, brand, site navigation, release banner, and site footer.

Check whether discarding the `<main>` subtree while retaining `<main>` itself is the correct boundary for the promise being tested. Look for chrome-like nodes injected inside main or content-like nodes outside main that could invalidate the assumption.

### 5.2 Reproduce all originally required counterexamples

The analyzer must reject at least selectors equivalent to:

```css
.site-header { ... }
body > .site-header { ... }
a { ... }
a:hover { ... }
.site-header:not(.route-only) { ... }
body .site-footer a { ... }
```

It must reject an unsafe arm in a comma/grouped selector even if another arm is safely scoped.

It must accept positively scoped equivalents such as:

```css
.sources-page .page-footer a { ... }
body:has(> .sources-page) .site-footer a { ... }
.plan-page a { ... }
.track-page a:hover { ... }
.route-only .site-header { ... }
```

Do not merely run the existing unit tests. Independently create temporary inputs or use direct helper invocation so the reviewer verifies behavior rather than the test author's expected values.

### 5.3 Attack pseudo-class semantics

Specifically probe:

- `:not()` where route identity exists only negatively;
- nested `:not()`;
- `:is()` with all-safe alternatives;
- `:is()` with one unsafe alternative;
- `:where()` with mixed alternatives;
- `:has()` used as positive parent/relational route scope;
- `:root`;
- unsupported or unusual pseudo-classes;
- pseudo-elements if they occur in production selectors;
- multiple functional pseudos in one compound selector.

The implementation report says:

- `:is()`/`:where()` count as scoped only when every alternative is scoped;
- `:has()` can provide positive scope;
- unmodelled pseudos are treated as satisfiable;
- unparsable selectors raise/fail closed.

Verify those statements from behavior and judge whether they are sound enough for the repository's actual selector grammar.

Pay special attention to false safety introduced by a route class occurring in a branch of a functional pseudo that does not constrain every match.

### 5.4 Attack combinator semantics

Probe at least:

- descendant;
- child `>`;
- adjacent sibling `+`;
- general sibling `~`;
- multiple combinators in one selector;
- selectors beginning from `body`, `html`, or `:root`;
- an instrument scope that occurs on a sibling/ancestor relation which cannot actually constrain the matched chrome node the way the analyzer assumes.

The analyzer need not implement arbitrary CSS Selectors Level 4 perfectly. It must, however, either correctly model the forms used in this repository or fail closed when it cannot prove safety.

### 5.5 Look for parser/tokenizer weaknesses

Because CSS is not safely parsed by naive comma/parenthesis/string splitting, inspect handling of:

- commas inside functional pseudos;
- parentheses nesting;
- comments;
- escaped identifiers;
- attribute selectors containing punctuation or commas;
- selector lists inside functional pseudos;
- pseudo-elements;
- whitespace/comment placement around combinators;
- media/supports blocks and whether rules inside them are still inspected.

You do not need to demand a standards-complete parser if the repository grammar is bounded and the implementation fails closed outside it. But a malformed or unsupported production selector silently disappearing from analysis is a blocker.

### 5.6 Independently scan the entire production stylesheet tree

Run the analyzer over every production stylesheet it is supposed to govern.

Do not assume the only unsafe selectors are the four protected Liturgy files.

Search manually as a second method for broad/global rules, especially:

- tag selectors (`a`, `button`, `header`, `footer`, etc.);
- `body`, `html`, `:root` rules;
- layout-owned class names;
- focus rules;
- selector arms hidden in lists;
- negative pseudo-class patterns;
- broad descendants that can reach header/footer links.

Compare manual findings with analyzer output.

Any real unprotected hazard the analyzer misses is `CHANGES_REQUIRED`.

---

## 6. Exact protected Liturgy exception audit

The remediation reports that the old single count-only exception became exact inventories for four protected files:

- `src/web/browser/liturgy/day-missal.css` — 12 selectors;
- `src/web/browser/liturgy/reader-shell.css` — 3 selectors;
- `src/web/browser/liturgy/reader-instrument.css` — 2 selectors;
- `src/web/browser/liturgy/reader-visual-reset.css` — 3 selectors.

Do not accept those exceptions merely because the files are under `liturgy/`.

For each file:

1. verify the current promise ledger and governing Liturgy authority actually protect that file/seam;
2. derive the unsafe selector inventory independently;
3. compare it exactly with the recorded inventory;
4. verify the test fails if one recorded selector is removed;
5. verify it fails if one selector is replaced by a different unsafe selector while the count remains constant;
6. verify normalization does not erase a meaningful selector change;
7. confirm no fifth protected file should be in the set;
8. confirm none of the four is now actually owner-released and should therefore be fixed instead of exempted.

Do **not** edit these Liturgy files during cold review.

If the exception is truthful but blocks shared-shell completion, keep `shared-shell-blocking-collisions-resolved` blocked. An exact exception is evidence, not completion.

---

## 7. Scripture selector correction review

The remediation changed the real production rule from broad:

```css
a { ... }
a:hover { ... }
```

to page-scoped equivalents using:

```css
:where(.plan-page, .track-page) a
:where(.plan-page, .track-page) a:hover
```

The implementation says this is needed because source pages have body classes but `browser_page_parts` projects those classes onto generated `<main>` in the public artifact.

Independently verify all of the following.

### 7.1 Scope correctness

Confirm the selector applies to intended Scripture content links in:

- source/off-disk `index.html`;
- source/off-disk `track.html`;
- generated public plan route;
- generated public track route.

Confirm it does **not** match global site masthead/footer links in the generated artifact.

### 7.2 Specificity/cascade correctness

Verify `:where()` preserves the intended effective specificity behavior, especially against:

- `.eyebrow a`;
- shared link rules;
- hover/focus rules;
- forced-colors rules if relevant.

Check actual computed style rather than reasoning only from source.

### 7.3 Visual disposition

The implementation reported:

- all Scripture in-content links retained their intended colors;
- six of seven chrome links remained unchanged;
- footer links changed from accidental Scripture-local color to site-owned oxblood (`rgb(143, 53, 64)`), matching other routes.

Reproduce representative measurements in real Chromium at the built artifact.

Judge whether this is truly removal of cross-surface leakage rather than a hidden visual redesign.

If site-owned `site.css` is indeed the authority for those footer links and comparable routes already render that color, this is not a product-design regression merely because pixels changed.

### 7.4 Accessibility/regression

Verify at least:

- no new horizontal overflow;
- visible focus behavior remains correct;
- skip link remains usable;
- link accessible names unchanged;
- no forced-colors break introduced by the new selector scope;
- no Catena or protected-Liturgy route change from this stylesheet correction.

---

## 8. B0/B1 changed-path and ownership audit

Compare the actual remediation delta from `e135e65...` to `de0bbc1...` (or the equivalent actual refs if branch advanced).

The implementation reported eight changed paths:

- `Makefile`
- `tools/tests/test_browser_model_gate.py`
- `tools/tests/test_browser_collisions.py`
- `src/web/browser/scripture/scripture.css`
- `guidance/corpus-browser-implementation.md`
- `guidance/corpus-browser-roadmap.md`
- `PROJECT-WORK.md`
- `promised-deliverables.toml`

Verify the list independently.

Require:

- zero protected Liturgy production changes;
- zero Catena production changes;
- zero Catena generated-data changes;
- zero Catena generator changes;
- no release-binding edits;
- no release approval/signing changes;
- no shared-shell cutover;
- no Search/acquisition/next-lane implementation.

If another changed path exists, classify it rather than assuming it is harmless.

---

## 9. Durable-record audit

The implementing agent updated four records. Verify the records tell the truth rather than merely echoing the implementation report.

At minimum check:

- `guidance/corpus-browser-implementation.md` §11.3;
- prior §11.1/§11.2 statements corrected or preserved appropriately;
- current roadmap disposition row;
- `PROJECT-WORK.md` remediation subsection;
- relevant `promised-deliverables.toml` requirements/comments.

Confirm:

- the previous `CHANGES_REQUIRED` disposition is not rewritten away;
- remediation is recorded as a candidate awaiting rereview, not accepted;
- `shared-shell-blocking-collisions-resolved` remains blocked while protected selectors remain;
- exact protected selector inventories and their authority are recorded;
- Scripture's real visual delta is disclosed rather than described as literally byte/pixel unchanged;
- exact measured test counts correspond to actual commands;
- stale release bindings are clearly intentional candidate state, not represented as green;
- no document grants merge, release, signing, deployment, or Liturgy authority it does not own.

Documentation-only inaccuracies may be corrected narrowly by the cold reviewer if doing so is necessary to leave a truthful review record. Do not repair substantive implementation defects yourself; return `CHANGES_REQUIRED` for those.

If you make review-record corrections, commit and push them separately and identify their SHA.

---

## 10. Regression and validation matrix

Use the repository's current commands after inspecting Makefile/guidance. Do not blindly trust stale command names from this file.

At minimum run/reproduce the applicable equivalents of:

### Focused remediation tests

- `test_browser_model_gate.py`
- `test_browser_collisions.py`
- direct browser-model coverage target
- direct browser-model gate
- adversarial missing-suite mutation
- adversarial selector mutations
- exact protected-selector replacement/removal mutations

### Browser/static foundation

- `check-browser-static`
- `check-browser-harnesses`
- full production stylesheet scan
- real Chromium built-artifact gate
- representative Scripture visual/computed-style proof

### Catena regression

Catena production is not remediation scope, but shared-foundation changes must not regress it. Run the current equivalents of:

- Catena generator/model validation;
- the 56 focused Catena tests if still current;
- the curated production suite (reported 394 tests);
- real-browser Catena identities/focus behavior where the existing gate defines them.

Do not reopen Catena design because unrelated inherited shell failures exist.

### Builds and bindings

- public preview/site build as required by current guidance;
- release-binding verification **without refreshing**;
- example verification if it is part of the normal candidate matrix.

### Full discovery

Run full unit-test discovery on a suitable base and candidate so new failure identities can be separated from inherited ones.

The implementation reported on its host:

- remediation base `e135e65...`: 2,719 tests / 24 failures / 0 errors / 10 skips;
- candidate: 2,750 / 24 / 0 / 10;
- same failure identities;
- 31 new tests exactly accounted for by test-suite growth.

Reproduce counts and **failure identities**. If counts vary because current branch/main moved or environment differs, explain why. Identity comparison matters more than historical totals.

### Chromium artifact matrix

The implementation reported both compared states as:

- 2,290 assertions;
- 1,850 pass;
- 212 inherited fail;
- 228 skip;
- byte-identical rows and detail strings;
- inherited fail classes 108 / 77 / 27.

Reproduce rather than quote.

If Scripture CSS changed built bytes but the generic matrix remains byte-identical, explain exactly what the gate is measuring so the statement is not misleading.

---

## 11. Stale release-binding audit

Do not refresh or sign bindings.

The remediation reports exactly two stale production paths:

- `src/web/browser/sources/sources.css`
- `src/web/browser/scripture/scripture.css`

It reports approximately:

- Sources recorded `a78f8cf8...`, actual `b039d50e...`;
- Scripture recorded `c2f974b7...`, actual `e10a02f6...`.

Derive the exact current stale set yourself.

Verify that:

- no third path is stale because of this branch;
- neither digest was hand-edited;
- no refresh command was run/committed;
- the stale oracle is the same cause when it appears inside another target;
- `check-examples` divergences are correctly classified and not hiding a separate product regression.

Do not mark B0/B1 defective merely because an implementation candidate has deliberately unsigned changed production bytes. Do return `CHANGES_REQUIRED` if stale-binding state is broader, unexplained, or misrepresented.

---

## 12. Decision standard

Your primary disposition is for **B0/B1 after remediation**.

Use one of:

- `ACCEPT`
- `ACCEPT_WITH_RECORD_CORRECTIONS`
- `CHANGES_REQUIRED`

### ACCEPT

Use only if both previous blockers are genuinely closed, no new implementation blocker is found, ownership boundaries are intact, and the remaining red state is fully explained by inherited or deliberately unsigned release-owned conditions.

### ACCEPT_WITH_RECORD_CORRECTIONS

Use only when implementation is substantively acceptable but narrow durable-record inaccuracies need correction. Do not use this status to waive an implementation/test defect.

### CHANGES_REQUIRED

Use for any substantive defect such as:

- meta-test still bypassable from normal `check` path;
- stale/false `UNGATED_WITH_REASON` coverage claim;
- selector analyzer false negative on a real/plausible repository selector class;
- selector analyzer silently accepts unsupported syntax rather than failing closed;
- a real unprotected site-chrome hazard remains;
- protected selector inventory can mutate without detection;
- protected exception lacks actual owner authority;
- Scripture scoping breaks intended content styling/accessibility;
- new failure identity caused by remediation;
- unexpected changed production path;
- Catena regression caused by remediation;
- stale-binding set broader or differently caused than represented.

Do not manufacture changes merely to achieve perfection. The standard is whether the B0/B1 foundation now truthfully provides the bounded protection it promises.

---

## 13. Catena Omnia vision and roadmap scope

Do **not** perform another wholesale review of the Catena Omnia vision or roadmap in this pass.

Their prior dispositions were:

- vision: `ACCEPT_WITH_CORRECTIONS`, with the required narrow-reading-order/projection-refusal correction incorporated;
- roadmap: `ACCEPT`.

The remediation did not modify those documents.

Only reopen them if this rereview discovers a direct factual contradiction introduced by the remediation or by a newly fetched authoritative mainline change. Otherwise state that their prior dispositions stand and move on.

---

## 14. Git authority and stopping line

You are a reviewer.

You may:

- inspect;
- build;
- run tests;
- perform temporary adversarial mutations and revert them;
- make **narrow documentation/review-record corrections only** if necessary;
- commit/push those review-record corrections to the same feature branch.

You may not:

- repair substantive implementation defects;
- merge;
- deploy;
- refresh/sign release bindings;
- approve a release;
- modify protected Liturgy production;
- modify Catena production/generated/generator code;
- cut over shared shell;
- begin Search;
- begin acquisition;
- begin any next product lane.

If substantive changes are required, document them precisely and stop.

After any review-record commit, fetch again, verify remote equality, verify clean working tree, and report the exact final branch head.

---

## 15. Required final report

Return a concise but mechanically complete report containing:

- `STATUS`
- `B0/B1 DISPOSITION`
- reviewed branch
- exact fetched `origin/main`
- exact starting remote branch head
- exact remediation commit reviewed
- final branch head after any review-record correction
- merge base
- branch distance from main
- clean-tree state
- exact changed-path inventory for remediation
- protected-Liturgy production changed paths: expected zero
- Catena production/generated/generator changed paths: expected zero
- Blocker A verdict and reproduced adversarial proof
- `UNGATED_WITH_REASON` audit result
- actual browser-model gate count/runtime and failure identities
- Blocker B verdict
- shell-model/parser/analyzer limitations and whether each is acceptable
- independent selector counterexample results
- full production stylesheet scan result
- exact four-file protected Liturgy exception inventory and authority disposition
- exact-mutation proof for protected selector inventories
- Scripture CSS/scoping/computed-style/accessibility disposition
- focused test results
- `make check` result classified by failure identity/cause
- full-discovery base/head totals and new failure identities
- Chromium artifact base/head identity comparison
- Catena regression results
- public build result
- exact stale release-binding path set
- `check-examples` classification if red
- durable-record accuracy disposition
- any documentation-only review correction commit SHA
- unresolved externally owned blockers
- prior Catena Omnia vision/roadmap dispositions still standing, unless a real contradiction was found
- explicit statement that no merge, deployment, signing, binding refresh, protected-Liturgy edit, Catena implementation, Search, acquisition, or next lane was performed
- **exact next authorized action**

If B0/B1 is accepted, the next action should be stated narrowly in terms of the governing roadmap/ownership — likely integration/release-owned handling of accepted production paths and the still-protected Liturgy blocker — rather than simply saying “continue development.”

Stop after the independent disposition and any narrowly necessary review-record correction.