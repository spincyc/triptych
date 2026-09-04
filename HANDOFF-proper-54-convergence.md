# Handoff: the Fourteenth Sunday, and the convergence work it paid for

Written 2026-09-04 on `impl/proper-54-production`, at the end of a session
that ran out of budget mid-verification. Read `PROJECT-WORK.md`, sections
"The Fourteenth Sunday blocked on an accounting defect, 2026-09-04" and
"What three cold reviews changed, and what they cost", first: this file says
only what that one cannot, which is where things stand right now and what the
next session should do in what order.

## Where the branch is

`impl/proper-54-production`, pushed. Four commits past the merge base:

| commit | what |
| --- | --- |
| `9ca815a90` | the Fourteenth Sunday leaf as run `90dcdddcb6780e60` left it |
| `0d18c253d` | the convergence work: budget, prose screens, lane ownership, tracked record |
| `a00b4f043` | merge of `origin/main`, reconciling two independent budget fixes |

`origin/main` is **not** touched. The leaf is still held out of it, per the
decision recorded in PROJECT-WORK.md, because its production has not finished.

## What is verified

**On the merged tree: 767 workflow tests pass, and the
`check-content-preflight` shell smoke test passes.** Before the merge, on the
pre-merge tree: 746 workflow tests, 53 house-voice tests and 14
latin-body-damage tests.

`test_generation_metadata` fails 11 on ecclesiastical-latin curriculum
documents. That is pre-existing — verified against a clean `HEAD` worktree —
and is nothing to do with this work.

The merge itself produced seven failures on the first run and four on the
second, every one of them worth knowing about because they are the shape of
this kind of merge:

- **Two were a real semantic collision.** Main's `OwnerChangeIsNotARepeatTests`
  asserted that an id returning to the same owner is charged; under the merged
  rule it is not, when the reviser reported success. Resolved toward the
  report, because run `90dcdddcb6780e60` blocked at 3/3 on exactly that shape
  and main's owner refinement does not separate those cases — all four of its
  ids named `authoring`. Main's tests keep their meaning, restated to say
  `not-repaired` explicitly, and the argument is in the test's docstring. **If
  the author of `2b9ed3c8a` disagrees, that is the place to argue it.**
- **The rest were bad conflict resolution of mine.** Resolving "keep both
  sides" is right for additive blocks and wrong for definitions: main's second
  copy of the check-list constants silently overwrote mine, dropping
  `house-voice` and `proposal-fields` out of the suite entirely, and the shell
  test ended up with two contradictory count assertions and two chronology
  fixtures on different providers. None of that is visible in the conflict
  markers.

## The combined budget rule

The merge combined two independent rewrites of `_failure_budget_spent`:

- a reviser's `finding_dispositions` displaces the id comparison wherever the
  receiving stage declares `reports_repairs`;
- where no stage on the route can report, the comparison stays, and is
  owner-aware — an id returning under a *different* `repair_target` is
  progress, not a repeat;
- a gate keeps the comparison whatever a reviser says, because a gate's ids
  are its own check ids.

If something fails there, that combination is where to look.

## The Fourteenth Sunday itself

Run `90dcdddcb6780e60` is BLOCKED and cannot be advanced — and now cannot
even be `status`ed against the current pipelines, because the version moved
past it. Its results are readable directly at
`build/tpt-runs/90dcdddcb6780e60/results/`.

**Do not sweep `build/tpt-runs/90dcdddcb6780e60`.** Its
`content-evaluation-0002*.json` files are the only record of the seven
blocking findings standing against the leaf: no
`evaluations/blocking-findings-v1.toml` exists anywhere under `src/`, because
the tracked record was built in this session and no run has written one yet.
`build/tpt-runs/ca03f1b357e7ec25` may be swept; its eight findings are
accounted for by id in PROJECT-WORK.md, seven closed and one reopened.

A new production seeds against `proper-finish` v3. It will now get
`DOCUMENT_ROOT` and `REPAIR_TARGETS` in its packets, a `content-preflight`
carrying twelve checks including the two prose screens, and a
`content-evaluation` that writes its standing findings to a tracked file.

## Decisions waiting for the maintainer

1. **`house-voice` refuses 8 of 12 leaves with a manifest**, published ones
   included, and that number did not move when the false positives were
   removed. Every remaining refusal was read against `guidance/editorial.md`
   and is a form it names. The check is not obviously wrong and the corpus is
   not obviously right. Nothing was repaired in another leaf on the strength
   of it. Two defects it found that no evaluation ever reported: retrieval
   mechanics in the reader-facing body of published `claude/52`, and five
   proposals in `gpt/52` stating no "what the ordinary element-by-element
   reading misses" field.
2. **Whether `proposal-fields` should also check the profile's 4-6 proposal
   count.** Equally mechanical, equally missable; left out because the check
   id says *fields*.
3. **`check-content-preflight` says a proposal has five mandated fields;
   every fragment and the profile say four**, because the check counts
   `anchors`. One side should move. Reported by the guidance reviewer, not
   yet acted on.

## Owed work, named and not done

- **Carrying findings between productions.** The tracked record is written
  and nothing reads it, deliberately: reading it at seed broke seed
  idempotency, put untracked working-tree state into hashed packet material,
  and on `proper` reached only the `seed` packet. It wants doing where the
  run's identity can cover it — an operator subcommand whose output is
  committed, or the record's hash in `compute_run_id` and the acceptance
  audit. `_standing_findings` is the reader and defines the format.
- **Escalations still live only in `state["escalations"]`**, under `build/`.
  Half of the older "run state is called durable" entry is still open.
- **`reports_repairs` and the gate carve-out are two special cases for one
  property** — who minted the id. The engine reviewer's point, and it is
  right: an id from a program is an identity, an id from a lane that cannot
  see the previous iteration is a handle. That belongs on the stage as one
  declaration, and a deterministic evaluator or a fan-out gate will need a
  third carve-out before it is.
- **Two judgement calls in the screen fail toward silence**, recorded in its
  tests: a real locus at `30-commentary.tex:1177` is suppressed because no
  rule distinguishes its form from a denominator, and the possessive rule has
  no clause guard.

## One hazard to know about

`scripts/replay_examples.py`'s `TrackedGuard` snapshots the dirty set at
start and reverts anything that changed during the run. With two workers
editing concurrently it reported reverting `PROJECT-WORK.md` and a fragment
another worker was writing. Nothing was lost here, but do not run it while
anyone else is writing.

## How this session worked, in case it helps

The three cold reviews were worth more than everything before them. They
found a severe bug (seed idempotency, from a feature that has since been
backed out), four more in the same code, and an unsafe prose screen that
would have refused rights bases and bounds on negative results. Every one of
those was in work that already had passing tests. If you extend this, review
it cold before you trust it.
