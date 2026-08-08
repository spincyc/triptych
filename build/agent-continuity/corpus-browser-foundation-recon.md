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
any change to a production browser surface, any push, any deploy, any merge to
`main`. `AGENTS.md` grants standing commit-and-push authority to Codex
sessions; this lane committed locally only and left `origin` untouched.

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

- No shared shell is implemented. B0 depends on an accepted A3/A4 visual
  contract that does not exist yet.
- `guidance/corpus-browser-vision.md` and `guidance/corpus-browser-roadmap.md`
  do not exist. They are the design lane's A2 output, not this lane's, and this
  lane deliberately did not create them.
- The four existing Chromium harnesses still have no target that runs them.
  They do not need repair: they need `make public-preview` first, which nothing
  says. See "What was learned" below — this was settled after the first version
  of this record was written, and it reversed the finding.
- No screenshot baseline was accepted as a visual oracle, because accepting one
  would be a visual decision.

Two design-neutral gates were built and committed, which the list above should
not be read as denying. `check-browser-static` runs inside `make check` and
needs no browser. `check-browser-gate` drives real Chromium over the built
artifact — the surface no existing harness looks at — and currently exits 1 on
three real defects: 117 states carrying a second `<main>`, 27 states on the
Propers routes with no usable skip link, and 320-pixel horizontal overflow on
the Source Library and Every Document. Those failures are the point of it; do
not weaken an assertion to make it green.

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
available.

**The baseline is red at the base commit, and the deploy cannot see it.**
`make -k check` exits 2; `check-tool-registry` and `check-examples` fail.
`python3 -m unittest discover -s tools/tests` exits 1 with 14 failures and 13
errors out of 1226. `check-tests` is not in `make check` (`Makefile:737` versus
`:842`), and CI runs neither — it runs `check-deployment-sources`,
`make public-site`, and `public-alpha verify`. Every one of those failures was
reproduced module-by-module in a clean separate checkout at the base SHA, with
identical counts, so none of it belongs to this branch. Anyone who adds a gate
here must not add it to a target that is already failing for unrelated reasons.

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
`guidance/external-review-handoffs.md`. Nothing in it has been reviewed or
accepted. No milestone is accepted. No gate has been satisfied beyond the
measured baseline above.

## Exact next action

Wait for the design lane's A3/A4 contract to be accepted, then implement B0
against it. Until then the only safe implementation work is design-neutral
verification, and the ordered list of it is in
`guidance/corpus-browser-implementation.md` under proposed sequencing.

Before any of that, whoever picks this up must settle the collision recorded in
that document: the in-progress deliverable
`liturgy-reader-live-ritual-flow-2026-08-07` owns `reader-shell.js` and
`reader-instrument.css`, has all six of its requirements open, and its own
brief declares that public-navigation redesign and a new visual direction are
separate and unauthorised. A corpus shell touches both files. That is a
sequencing decision for the maintainer, not something an implementation lane
may decide for itself.
