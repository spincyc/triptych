---
protocol: relay-v1
run: 2026-09-01-01
turn: 002
role: planner
agent: gpt-5.6-sol
branch: feature/catena-omnia/b0-b1-selector-oracle
base: 788a132bd3bd482778bc913cf37e0aded909b3a7
abandons: .agent/runs/2026-09-01-01/001-brief.md
---

## Objective

Independently cold-confirm whether the corrected B0/B1 browser selector oracle at exact candidate `639b9a6fc84b9a169948b951b59972acae24b0a2` genuinely closes the four corrections required by the prior `ACCEPT_WITH_CORRECTIONS` rereview, without introducing a new correctness, coverage, ownership, or regression defect. Return an evidence-backed B0/B1 disposition suitable for the later integration/release owner. Do not perform that later integration or begin Catena Omnia acquisition.

## Scope boundary

You own only the independent review of candidate `639b9a6fc84b9a169948b951b59972acae24b0a2` and the relay artifacts for this run.

The only files you may commit are the relay claim and result files under `.agent/runs/2026-09-01-01/`. Use explicit pathspecs for those commits.

You may make temporary adversarial mutations while testing, but restore every such mutation before publishing the result and finish with a clean worktree except for the result file being prepared for its own commit. Do not commit a test mutation or implementation correction.

Do not edit implementation, production CSS or JavaScript, protected Liturgy files, Catena production, generators, generated corpus data, release bindings, durable project records, or Makefile. Do not merge, deploy, sign, refresh bindings, cut over the shared shell, start Search, start Catena Omnia acquisition, or begin another product lane.

Treat the existing implementation report, commit messages, durable records, prior review text, and this brief as claims to test, not as proof.

## Acceptance criteria

1. **Exact review target and topology are proved.** Record fetched `origin/main`, the review branch head after your claim, the ancestry of candidate `639b9a6fc84b9a169948b951b59972acae24b0a2`, its merge base with `origin/main`, and branch distance from main. Distinguish relay-only commits from the implementation candidate. Verify the implementation delta from prior rereview commit `373ce7f98b5d5c05a3b3d5df6acaeaf610bff60b` to candidate `639b9a6fc84b9a169948b951b59972acae24b0a2` contains no production CSS/JS change, protected Liturgy change, Catena change, Makefile change, release-binding change, merge, deployment, or signing work.

2. **The prior four required corrections are independently closed or explicitly found open.** The prior independent rereview at `373ce7f98b5d5c05a3b3d5df6acaeaf610bff60b` returned `ACCEPT_WITH_CORRECTIONS` because the state walk forced one user state at a time and therefore failed open for simultaneous user states on distinct compounds. It required exactly these corrections:
   - disclose the one-state-at-a-time bound and its witness in the durable record;
   - fail closed for selector arms requiring forced user states in two or more distinct compounds;
   - actually assert/use the harness `interactive` measurement instead of returning it unread;
   - correct the changed-path wording that overstated the implementation delta.

   Prove closure independently, not merely by reading the new prose.

3. **The latent two-compound fail-open is gone.** Drive real Chromium and show that at least these prior witnesses are now refused and unsafe rather than reported safe:
   - `a:focus ~ .site-footer:hover`
   - `.skip-link:focus ~ .site-footer:hover a`

   Also prove the correction is not a blanket ban on ordinary dynamic selectors: at minimum `a:hover` and `.track-page a:hover` must retain their intended classification, and a selector with multiple relevant state pseudos in one compound must not be refused solely because more than one state token appears.

4. **The new fail-closed rule is itself protected by regression tests.** Temporarily sabotage or bypass the distinct-compound forced-state refusal and prove the focused suite turns red. Restore immediately. A correction that works only because the current production tree lacks such a selector is insufficient.

5. **The `interactive` measurement is now load-bearing.** Independently demonstrate that the test/controller consumes it. Temporarily falsify the interactive measurement or otherwise sever its assertion path and prove a focused test fails; restore immediately. Confirm the measured production shells still contain none of the interactive chrome element/state classes whose absence justifies the bounded walk.

6. **The existing selector-oracle guarantees did not regress.** Reproduce, rather than trust, all of the following:
   - Chromium remains the authority for selector reach; Python does not infer a safe verdict through a fallback matcher or route-name scan.
   - the four protected Liturgy inventories remain exact ordered inventories with counts `12 / 3 / 2 / 3` for `day-missal.css`, `reader-shell.css`, `reader-instrument.css`, and `reader-visual-reset.css`;
   - the production scan remains 1,193 unique selector arms with zero refusals and no newly unprotected site-chrome hazard;
   - accepted Scripture route scoping remains safe;
   - Blocker A remains closed: the browser-model coverage meta-test is still unavoidable through the `check` -> `check-browser-models` -> `check-browser-model-coverage` topology.

7. **At least one adversarial mutation beyond the two correction-specific mutations is repeated.** Make the browser oracle return an obviously wrong reach/safety answer or otherwise sever browser authority, prove the focused suite fails materially, then restore. Record the observed failure count or identities. Do not rely on the historical claim that a previous sabotage produced 55 failures.

8. **The focused and static regression commands pass in the unmutated candidate.** Chromium must actually be available and driven; a skip-only result is not sufficient for acceptance. Record exact test counts, browser version, and meaningful scan metrics from this run rather than copying prior numbers.

9. **Disposition is explicit.** In the relay result, after the required relay `status`, include one of:
   - `B0_B1_DISPOSITION: ACCEPT`
   - `B0_B1_DISPOSITION: ACCEPT_WITH_RECORD_CORRECTIONS`
   - `B0_B1_DISPOSITION: CHANGES_REQUIRED`

   `ACCEPT` means the four prior corrections are genuinely closed and no new substantive blocker was found. `ACCEPT_WITH_RECORD_CORRECTIONS` is only for non-substantive record truth corrections that do not affect the gate. Any fail-open, missing coverage, unproved browser authority, live production hazard, regression, or inability to execute the required real-Chromium evidence is not `ACCEPT`.

10. **No later authority is exercised.** Even on `ACCEPT`, stop after publishing the relay result. Do not merge to main, refresh release bindings, deploy, sign, mark release promises complete, or begin Catena Omnia acquisition.

## Verification

Run these unmutated checks at minimum, with bytecode disabled where applicable:

```text
PYTHONDONTWRITEBYTECODE=1 python -m unittest tools.tests.test_browser_collisions
PYTHONDONTWRITEBYTECODE=1 python -m unittest tools.tests.test_browser_model_gate
make check-browser-static
make check-browser-models
git diff --check
```

In addition, perform the temporary adversarial mutations required by Acceptance Criteria 4, 5, and 7, running the smallest focused command that proves each mutation is detected, and restore each mutation before continuing.

If repository instructions expose a more canonical invocation for the same focused suites, use it and record the exact command. Do not weaken a required real-Chromium check into a skip or a source-only substitute.

## Context

**Recovery from abandoned turn 001.** Turn 001 was pasted into a checkout of a different repository (`spincyc/lacuna`) on a Lane 4 review branch. Relay preflight correctly stopped with `preflight-failed` before claim or work. At publication of this replacement brief, `origin/feature/catena-omnia/b0-b1-selector-oracle` contains no executor claim, result, or work commit after `.agent/runs/2026-09-01-01/001-brief.md`; its tip is still `788a132bd3bd482778bc913cf37e0aded909b3a7`. Do not infer any review evidence from the abandoned attempt.

**This turn must begin in the correct checkout before preflight.** The executor process must already be running in the `spincyc/triptych` checkout with current branch `feature/catena-omnia/b0-b1-selector-oracle`. The relay protocol intentionally does not authorize switching repositories or branches to repair a bad launch. If the process is again in any other repository or branch, stop with the blocked channel rather than checking out or switching.

The exact candidate is `639b9a6fc84b9a169948b951b59972acae24b0a2`, originally published on `impl/corpus-foundation-b0-b1` and used as the base of this relay branch.

The prior independent rereview is commit `373ce7f98b5d5c05a3b3d5df6acaeaf610bff60b`. Its disposition was `ACCEPT_WITH_CORRECTIONS`; it confirmed the browser-native architecture and found the latent two-distinct-compound simultaneous-state fail-open described above.

Read these repository paths as governing/current context at candidate `639b9a6fc84b9a169948b951b59972acae24b0a2`:

- `AGENTS.md`
- `guidance/NEXT-CODEX-B0B1-SELECTOR-ORACLE-REREVIEW.md` — prior cold-review specification; use it for the broader architecture and adversarial expectations, but this relay brief is authoritative for the narrower final confirmation
- `guidance/corpus-browser-implementation.md`, especially the selector-oracle sections around 11.4 and 11.5
- `PROJECT-WORK.md`, selector-oracle remediation entries
- `guidance/corpus-browser-master-plan.md`
- `guidance/corpus-browser-roadmap.md`
- `guidance/catena.md`
- `guidance/catena-omnia-vision.md`
- `guidance/catena-omnia-roadmap.md`
- `promised-deliverables.toml`
- `tools/tests/site_chrome_selector_oracle.mjs`
- `tools/tests/test_browser_collisions.py`
- `tools/tests/test_browser_model_gate.py`
- `tools/public-alpha`
- `release/public-alpha/layout.html`
- `Makefile`

Catena E0/E1 is a closed product lane for this review. Catena Omnia vision/roadmap are not under review. This turn determines only whether the shared B0/B1 selector-oracle foundation has cleared its last independent correction review.

## When blocked

Follow relay-v1 preflight and blocked-channel rules exactly. Do not improvise around a dirty checkout, wrong repository, wrong branch, stale/mutated brief, missing credentials, rejected push, rebase/merge state, or protocol mismatch.

If real Chromium cannot be driven, publish a relay result with `status: blocked` and `needs:` the exact missing browser capability; do not convert skips into acceptance.

If a required test is impossible for a repository-specific reason, publish `status: partial` or `blocked` as appropriate with the exact missing capability or authority. Do not repair the candidate. If you find a substantive defect, finish the review, return `B0_B1_DISPOSITION: CHANGES_REQUIRED`, publish the evidence in the result, and stop.
