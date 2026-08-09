# Corpus browser — Claude foundation reconnaissance (B0/B1)

Recorded: `2026-08-08`

Read first:

1. `guidance/corpus-browser-master-plan.md` — the governing multi-agent plan.
2. `guidance/corpus-browser-implementation.md` — the durable technical record
   this task produced. That document, not this one, is the authority.
3. `guidance/liturgy-browser-vision.md` and `guidance/liturgy-browser-roadmap.md`
   — still governing for liturgical semantics and unchanged by this task.

This file exists to answer, for whoever picks the lane up: what was attempted,
what is finished, what is not, what was learned, and what the next action is.
It is a continuity record, not a design document and not a plan.

**Corrected on 2026-08-08, later the same day.** Everything below was written
when this lane was one branch that had committed nothing to `origin`, when the
design lane's dispositions did not exist, and when the artifact gate had run
once. Eight passages had gone false by evening. Each is corrected in place and
marked **Corrected**; where the fact now has an owner in tracked guidance, this
record points at the owner instead of restating it, per §14's amendment D10 in
`guidance/corpus-browser-implementation.md` — the rule this file was in breach
of by being the sole home of facts a later agent needs.

## Boundary

Branch `impl/foundation`, in a separate full checkout — not a Git worktree, as
the task required.

Base commit `c27d6915319785686d1df6a1401a489aa9921f6f` ("Ungate the controls
that leave a Day"), which was `origin/main` when the task started.

The task said to start from the same `origin/main` SHA the Codex foundation
task used. That was not stated anywhere, so it was established by inspection
rather than assumed: the Codex foundation checkout sits on branch
`ux/foundation` at `c27d69153`, the same commit. The two foundation lanes are
therefore genuinely aligned. If a later reader finds a different Codex base,
this branch's base is wrong and the reconciliation is theirs to make.

Authorised: reconnaissance, tracked documentation, and design-neutral test
infrastructure. Not authorised and not done: any visual or product decision,
any change to a production browser surface, any merge to `main` from this lane.

**Corrected.** Two claims here are no longer true. First, the lane no longer
committed locally only: `impl/foundation` is on `origin` at `af2c9613c`, and so
are its four descendants — `impl/foundation-hardening`, `impl/shell-plumbing`,
`impl/catena-wave-1`, and this record with them. Second, `AGENTS.md` no longer
grants standing commit-and-push authority to Codex sessions alone.
`origin/main:AGENTS.md`, under "Claude sessions", grants a Claude session a
narrower standing authority as of 2026-08-08: a bug fix found against `main`
may be merged and pushed provided the rebase is clean and the merge is a genuine
fast-forward, bounded to bug fixes, bounded to fast-forwards, gated on the three
deploy checks run locally first, and understood to authorize the Pages
deployment the push triggers. It was exercised twice that day —
`fix/day-missal-switch` and `fix/browser-truthfulness` are both merged to
`origin/main` (`fc3092de9`) and deployed. The impl branches do not carry that
`AGENTS.md` section, so an agent reading `AGENTS.md` on one of them reads the
superseded rule; read it on `main`.

## What was attempted

The B0/B1 reconnaissance of the master plan's Dispatch 2: audit the browser and
site architecture, the shared CSS and JavaScript, generated and static HTML
ownership, shell primitives, navigation, route generation, test and
browser-test infrastructure, screenshot and accessibility capability, viewport
and zoom coverage, console and request gates, the seams for a shared corpus
shell, conflicts between existing instruments, duplicated UI code, the GitHub
Pages constraints, and the practical implementation risks; then build as much
neutral regression infrastructure as can be built before a visual contract
exists.

Ten read-only reconnaissance lanes ran in parallel over the checkout, one per
subject area. Their findings were reconciled and the load-bearing ones were
re-verified first-hand before being written down. Two implementation lanes
followed: the durable technical record, and the neutral page gate.

## What is complete

- The base SHA question is settled by evidence, above.
- `guidance/corpus-browser-master-plan.md` is tracked. It previously existed
  only as an untracked file in a maintainer checkout, which is precisely the
  state `guidance/the-shape.md` argues against. It is under `guidance/`, beside
  the liturgy roadmap, and not under `docs/`, which holds reader-facing
  accounts linked from `README.md`.
- `guidance/corpus-browser-implementation.md` records the architecture, the
  constraints, the sequencing, and the risks.
- The verification baseline is measured and attributed, below.

## What is not complete

- No shared shell is implemented. **Corrected as to why.** This said B0 depends
  on an accepted A3/A4 visual contract that does not exist yet. A3 and A4 were
  accepted on 2026-08-08 — A3 as foundation direction only, expressly not as
  pixel acceptance of any production route — and §17-18 of
  `guidance/corpus-browser-implementation.md` then established that B0 never
  blocked the six instrument lanes in the first place: every non-liturgy page
  loads only `shared/browser-core` plus its own directory, and what gates an
  instrument lane is its own design. The shell is unimplemented because §11
  step 6 was **withdrawn** under the protected-liturgy amendment, not because
  a contract is missing. See "Exact next action".
- **Corrected: `guidance/corpus-browser-vision.md` and
  `guidance/corpus-browser-roadmap.md` exist.** They did not when this was
  written, and this lane deliberately did not create them because they are the
  design lane's A2 output. The design lane has since produced them, together
  with `guidance/corpus-browser-inventory.md`,
  `guidance/corpus-browser-research.md`,
  `docs/triptych-world-class-corpus-master-plan.md`, and the
  `src/web/browser/prototypes/corpus-foundation/` prototype with its two tests.
  All of it is on `ux/foundation` (`3b5938a0d`) and reachable with
  `git show ux/foundation:<path>`; none of it is on any impl branch or on
  `main`. `PROJECT-WORK.md` under "Which branch carries what" owns the full map.
- **Corrected: the four Chromium harnesses have a target.** `Makefile:778`,
  `check-browser-harnesses: public-preview`, added by `d766aa1a5`. The
  prerequisite is the whole of the fix, as "What was learned" below explains,
  and the target holds the three harnesses that exit non-zero to a recorded pass
  floor rather than to a zero exit.
- No screenshot baseline was accepted as a visual oracle, because accepting one
  would be a visual decision. This is still true.

Two design-neutral gates were built and committed, which the list above should
not be read as denying. `check-browser-static` runs inside `make check` and
needs no browser. `check-browser-gate` drives real Chromium over the built
artifact — the surface no existing harness looks at.

**Corrected: its failure list has moved four times and is not the same on two
branches.** `guidance/corpus-browser-implementation.md` §17.5 owns the current
figures and the arc; §20 owns the disposition of each failure class. In summary,
at `ecfb4e7b8` on `impl/foundation-hardening` the gate reports 226 failures out
of 2,290 assertions in 93 seconds, and they are three classes, not the three
listed above: 117 `single-main-element` (a real defect, and fixed on
`impl/shell-plumbing` by `6b5742bf2`, which takes that branch to 109); 82
`primary-controls-meet-target-size` (a class this record predates, and a
design-lane dependency rather than a defect); and 27
`skip-link-targets-existing-element` (re-diagnosed by `4b87fd14e` as a modal
focus trap in the Propers reader, not a missing or dangling skip link). The
320-pixel overflow on the Source Library and Every Document was fixed by
`862f25173` and fails nowhere. Those failures are still the point of the gate;
do not weaken an assertion to make it green.

## What was learned

The findings themselves are in `guidance/corpus-browser-implementation.md`.
Four are worth repeating here because they change what the next agent should
attempt first.

**The shared shell already exists.** `release/public-alpha/layout.html` and
`wrap_in_layout()` in `tools/public-alpha` wrap every published page, including
the hand-authored browser HTML, which is dismantled and re-wrapped rather than
copied. No hand-authored HTML reaches the artifact unmodified. Building a
"shared shell" without reckoning with that builds a third one.

**The publish step is where the accessibility defects are, and no harness looks
there.** Every browser-instrument page ships with two nested `<main>` elements
— `<main id="canon">` inside `<main id="main-content">` at `law/index.html:45`
and `:84` in the built artifact — and the page's own skip link is stripped
(`tools/public-alpha:2504`). Two published reader pages are titled
`Day — Triptych · Triptych` and `Propers — Triptych · Triptych`. All four
existing harnesses load the repository copies, so none of this is visible to
them. A gate that tests the built artifact is the cheapest real coverage
available. The nesting is still exactly as described here at
`build/public-alpha/site/law/index.html:45` and `:84` on this branch;
`6b5742bf2` fixed it on `impl/shell-plumbing` and nowhere else.

**The baseline is red at the base commit, and the deploy cannot see it.**
`make -k check` exits 2; `check-tool-registry` and `check-examples` fail.
`python3 -m unittest discover -s tools/tests` exits 1 with 14 failures and 13
errors out of 1226. `check-tests` is not in `make check` (`Makefile:737` versus
`:842`), and CI runs neither — it runs `check-deployment-sources`,
`make public-site`, and `public-alpha verify`. Every one of those failures was
reproduced module-by-module in a clean separate checkout at the base SHA, with
identical counts, so none of it belongs to this branch. Anyone who adds a gate
here must not add it to a target that is already failing for unrelated reasons.

**Corrected: eight of those thirteen errors were a stale fixture, and the
baseline is 14 and 5 on the branch that fixed it.** Every `test_public_alpha`
case wrote a stub root hardcoding `Markdown==3.10.2` after the repository's lock
had moved to 3.10.3, so the generator's own lock check correctly refused the
stub. `f434c5b91` on `impl/shell-plumbing` made the fixture read
`requirements-public-alpha.txt` from the repository, taking that module from 8
errors to 0 and the suite from 14 failures and 13 errors to **14 and 5**;
`517412cce` recorded it. A branch based before `f434c5b91` — this one
included — should still expect 13, and 14/13 remains the correct comparison here.

**Browser testing exists, works, and is dead code — and the reason it looked
dead is a prerequisite nobody wrote down.** Four dependency-free Chromium CDP
harnesses, about 5,950 lines, live at `tools/tests/*_browser.mjs`. They already
assert console errors, failed requests, HTTP errors, 400% scale,
`forced-colors`, `prefers-reduced-motion`, print media and keyboard dispatch.
No Makefile target and no Python test runs any of them; the suite only runs
`node --check`. They default to `/usr/bin/google-chrome-stable`, which the
installer deliberately does not install (`Makefile:72-76` declares `chromium`).

Run in a checkout that has not built the preview, all four fail — one with 0 of
25 assertions, all "Timed out waiting for … readiness". That is not rot. Three
of them hardcode `build/public-alpha/preview/` as their data root, so every
request 404s and readiness can never arrive. With `make public-preview` first
and no other change, they return **18/18 (exit 0), 39/41, 30/32 and 22/25** on
`/usr/bin/chromium`. Chromium was never the problem.

The seven residual failures are one finding, not seven: every one is a
coverage-or-absence notice the page no longer renders — `/not yet transcribed/i`
and `/not held/i` matched against empty strings, and "partial coverage stays
explicit" returning false. Absence surviving the renderer is the invariant this
repository is built on, and the in-progress ritual-flow phase set out to make
apparatus notes quieter. Do not act on it from a corpus lane; those files are
that deliverable's evidence paths. Report it and let the maintainer sequence it.

That finding has since been sized and written down where it belongs:
`guidance/corpus-browser-implementation.md` §19, added by `a37efd22f`, owns it.
It is larger than "seven assertions" — 233 of 491 `roman-1962` masses, 154 of
269 `postconciliar` and 232 of 491 `roman-pre-1955` render no Collect, Secret or
Postcommunion and report coverage `complete`, and in Missal mode print the
missal's own rubric directing the reader to the gap. Read §19, not this
paragraph. §19 exists **only** on `impl/foundation-hardening`: `a37efd22f`
landed after `impl/shell-plumbing` and `impl/catena-wave-1` both branched, so
their copies of the record carry the §9 statement of the finding with nothing
behind it. It should be cherry-picked to them.

## Known failed approach

None attempted and abandoned by this lane. The earlier failed approaches for
these surfaces are recorded where they belong — the scroll-reveal shell, the
floating shell card at 1024×768, the global rubric typography revert, the
per-page CSS themes, and the redirect-and-alias cutover mechanism are all in
`guidance/liturgy-reader-shell-prototype.md` and
`guidance/liturgy-browser-roadmap.md`. Read them before proposing any of them
again.

## Verification baseline at this branch

| Command | Exit | Result |
| --- | --- | --- |
| `make public-site` | 0 | 441 MB, 20,441 files, 144 HTML pages, 5.1s |
| `python3 tools/tpt public-alpha verify --deployment-target github-pages` | 0 | the exact command CI runs |
| 144 built routes over `python3 -m http.server` | 0 | 144/144 HTTP 200 |
| `make -k check` | 2 | 17/19 targets pass; `check-tool-registry` and `check-examples` fail |
| `python3 -m unittest discover -s tools/tests` | 1 | 1226 tests, 14 failures, 13 errors, 8 skipped, 466s |

Attribution, each re-run in a clean checkout at `c27d69153`: `test_public_alpha`
8 errors, `test_index_bible` 5 errors, `test_day_reader_integration` 2,
`test_day_missal_integration` 2, `test_propers_reader_integration` 2,
`test_mass_ordinary` 1, `test_tool_registry` 7. Sum 27, which is the whole of
the 14 failures and 13 errors. The red baseline is pre-existing.

Host: node v26.7.0, Chromium 151.0.7922.108, ChromeDriver 151. No npm, npx,
deno or bun. No `playwright` or `selenium` in Python. Python 3.14.6.

## Current external-review disposition

One handoff was produced for this task under
`guidance/external-review-handoffs.md`.

**Corrected: the coordinator dispositioned both lanes on 2026-08-08.** A0 and A1
accepted; A2 accepted with amendments D1–D20; A3 accepted as foundation
direction and expressly **not** as pixel acceptance of any production route, so
no route may cite A3 as approval of how it renders; A4 accepted with the
bounded-Jump and protected-liturgy amendments; this lane's reconnaissance
accepted; the neutral gates accepted for integration. `PROJECT-WORK.md` under
"Acceptance, 2026-08-08" owns the table; §14 of
`guidance/corpus-browser-implementation.md` owns which amendments bind
implementation. The design lane's own roadmap on `ux/foundation` still records
A0–A4 as candidates awaiting review and has not caught up; the register is
later and governs. The ledger entry
`corpus-browser-foundation-design-2026-08-08` on `ux/foundation` remains
`candidate` with `independent-foundation-disposition` open, so nothing here is
`complete`.

## Exact next action

**Corrected: the wait this section prescribed is over, and it ended in a
withdrawal rather than an acceptance.** The 2026-08-08 review protected the
liturgy surface family outright, so promoting `reader-shell.js` into a shared
shell — §11 step 6, the step this record called the highest-value move in the
lane — is withdrawn rather than deferred. Reuse its ideas, not the owned file.
§17-18 then established that B0 does not block the six instrument lanes at all:
every non-liturgy page loads only `shared/browser-core` plus its own directory,
and what gates an instrument lane is its own design, not the shared shell.

What genuinely still blocks is narrower and is recorded in `PROJECT-WORK.md`
under "Blocker: B0 cannot start": `corpus/foundation-integration` does not
exist, `impl/corpus-wave-1` bases on its head, and so that one lane cannot be
created. Creating the integration branch remains the unblocking act.

Until then the ordered list of safe design-neutral work is
`guidance/corpus-browser-implementation.md` §11, of which steps 1–4 and 5(a)–(c)
are done on `impl/foundation-hardening`. Step 5(d) — scoping `day-missal.css` —
is the one prerequisite still open, and it is protected liturgy, so it is not a
corpus lane's to make.

Before any of that, whoever picks this up must settle the collision recorded in
that document: the in-progress deliverable
`liturgy-reader-live-ritual-flow-2026-08-07` owns `reader-shell.js` and
`reader-instrument.css`, has all six of its requirements open, and its own
brief declares that public-navigation redesign and a new visual direction are
separate and unauthorised. A corpus shell touches both files. That is a
sequencing decision for the maintainer, not something an implementation lane
may decide for itself.
