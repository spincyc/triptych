## Public-cutover execution retry — Codex response

Execution retry begins at synchronized starting SHA
`6bb0d02e50794b1cfe89faa5424e6eea42e55872`. Before this continuity append,
the worktree was clean and `HEAD`, local `main`, `origin/main`, and remote
`refs/heads/main` all agreed at that SHA.

The canonical replacement patch at
`build/agent-continuity/liturgy-reader-public-cutover-proposed.patch` has the
accepted SHA-256
`ce43cef0621e3e1bdf6eb53eb4ce62e479e54977bd739a26385068bcaa33b0e5`.
The gate-repair baseline ancestor check against
`e20b2f542ab51a2b4f0807e6394ca5ecb313699c` exited 0, and normal-context
`git apply --check` exited 0. No `--3way`, fuzz, regeneration, or manual
reconstruction will be used.

All nine gate-repair dispositions are recorded as accepted: the repairs are at
the test/harness boundary; scope is exactly 19 paths; accepted prospective
product/release bytes are unchanged; focused locked Python passes; all four
browser gates pass; repaired assertions remain strong; mechanical application
passed and was rechecked at this execution boundary; real canonical readers
remained unchanged and undeployed during repair; and entry into the bounded
execution/deployment/cache protocol is authorized.

The intended sequence is exact: append this continuity record; apply only the
accepted patch; verify the three frozen product/release hashes and exact scope;
run the complete real-tree canonical gate; create and push one bounded cutover
commit; require Pages success for that exact cutover SHA; run immediate live
canonical and byte-parity verification; wait beyond the observed cache window
and repeat the required non-cache-busted checks; then seal and push the execution
handoff and stop for independent public-cutover acceptance.

Any cutover-owned failure before commit triggers reversal of the uncommitted
application and review. Any material post-push canonical failure or uncertain
mixed deployment triggers an ordinary `git revert <CUTOVER_COMMIT>` followed by
push, exact-revert-SHA Pages success, restored-route verification, and immediate
and post-freshness checks; history will not be rewritten.

Public navigation changes and candidate/oracle cleanup remain forbidden.
Visual/product redesign, renderer/state refactoring, Ordinary changes,
source/translation expansion, and unrelated cleanup likewise remain outside
this execution authorization.

### Real-tree canonical pre-deployment checkpoint

The corrected patch was applied without regeneration or hand editing. Its
effect is exactly the accepted 19 paths plus this append-only continuity file.
The promoted source hashes are unchanged from the independently accepted
prospective values: Day `9a119a6aa87e900d6fc4c3e236191fe8a036abc305236eb576c09f823c7b7972`,
Propers `a6527316266365b79ff2ecdc193da3ab1034b1daa63408b869b192d2aeb85600`,
and the rights record
`5a4b4d4f8bfbcf8d5fd54249c0d8664be7215b4bee9e82ccc8a37f400e3cf31e`.

The actual promoted working tree passes locked focused Python 230/230; Day
Chromium 40/40; Propers Chromium 32/32; shared-shell Chromium 18/18; governed
Instrument Chromium 24/24; syntax checks for all changed Python and JavaScript
tests; promised-deliverables and tool registries; release bindings with zero
stale entries; `git diff --check`; and locked public-alpha policy, build, and
GitHub-Pages-target verification. The governed Instrument run initially found
the expected pre-cutover generated preview still on disk; after the required
locked preview build and verification, the same unmodified harness passed
24/24 against the promoted canonical filenames.

The governed full `make check` remains honestly non-green at `check-examples`
with exit 2. It replayed 200 captured examples, ran 188, and reported 21
divergences, 35 known-stale cases, six deliberately unrun network/mutating
examples, and six unavailable built-artifact examples. This is the already
disclosed unrelated stored-example transcript divergence; no transcript was
recaptured or blessed. No task-owned gate failed.

The next exact action is to commit and push this bounded cutover, then accept
only a successful Pages run whose source SHA equals that cutover commit. Public
navigation and retained candidate/oracle bytes remain outside the change.

### Exact-SHA deployment and immediate live checkpoint

Commit `9b5f21c0ca26bf02af03d207ddd2617021e16fb3` pushed the exact accepted
19-path promotion plus continuity. GitHub Pages run `31175722949` names that
exact source SHA and completed successfully; every build, verification, upload,
and deploy step passed. Earlier continuity and handoff runs remain explicitly
nonqualifying.

The immediate cache-bypassed live verifier completed at
`2026-08-07T12:16:10.158Z`: 936/936 assertions across 36 original-pixel states,
with zero console, required-request, HTTP, unnamed-control, duplicate-ID, or
required-overflow problem. It proves canonical HTTP 200/no-redirect behavior,
indexing metadata, empty-Day Roman 1962 default, Read/Missal, deep links,
why=1, two held territorial branches, Propers public option keys, fail-closed
alternative state, Details links, accessibility/reflow states, reload and
Back/Forward, retained candidate/oracle full noindex, and byte parity for 15
deployed HTML/JS/CSS assets against the locked build.

The governed original-pixel evidence is also green: Day 40/40 with 77 captures;
Propers 32/32; shared shell 18/18 with 94 captures; Instrument 24/24 with 113
captures. The immediate matrix was visually inspected as a labeled sheet and at
full size for the portrait Read measure, 200% dock, territorial branch, and
mobile Details states; no filename-change visual regression is visible.

The verifier enforces at least 601 seconds after the immediate completion before
the post-window pass. That pass may not begin before
`2026-08-07T12:26:11Z`. No rollback trigger has fired.

### Post-freshness-window checkpoint

The required ordinary-cache pass began after 613 elapsed seconds and completed
at `2026-08-07T12:26:32.943Z`: 216/216 assertions across the six required
canonical states, with zero console, request, HTTP, accessibility-name,
duplicate-ID, or overflow problem. It used a fresh Chrome profile, plain URLs,
normal cache behavior, and no cache-busting query or headers. Canonical default,
deep link, Missal, Propers deep link, Details, and territorial Why all settled;
all 15 checked deployed assets remained HTTP 200, unredirected, and byte-equal
to the locked build. No mixed-generation behavior appeared, and the ordinary
rollback trigger did not fire.

The exact execution handoff is
`build/agent-handoffs/20260807T115341Z-liturgy-reader-instrument-public-cutover-execution/`
with a matching ZIP to be sealed. The cutover remains pending independent
post-deployment acceptance; public navigation redesign, candidate/oracle
cleanup, and all other excluded work remain unauthorized.
