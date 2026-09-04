# Handoff: the Fourteenth Sunday, and the convergence work it paid for

This is the historical handoff written 2026-09-04 on
`impl/proper-54-production`, at the end of a session
that ran out of budget mid-verification. Read `PROJECT-WORK.md`, sections
"The Fourteenth Sunday blocked on an accounting defect, 2026-09-04" and
"What three cold reviews changed, and what they cost", first. Its tip,
`a7547b253`, has now been merged into `feature/propers-chronology`; the notes
below preserve both the original state and the integration disposition.

## Where the branch was

`impl/proper-54-production`, pushed. Four commits past the merge base:

| commit | what |
| --- | --- |
| `9ca815a90` | the Fourteenth Sunday leaf as run `90dcdddcb6780e60` left it |
| `0d18c253d` | the convergence work: budget, prose screens, lane ownership, tracked record |
| `a00b4f043` | merge of `origin/main`, reconciling two independent budget fixes |
| `a7547b253` | the source-branch handoff |

`origin/main` is **not** touched. The leaf is still held out of it, per the
decision recorded in PROJECT-WORK.md, because its production has not finished.

## Verification

Verified before the merge, on the pre-merge tree: **746 workflow tests, 53
house-voice tests, 14 latin-body-damage tests, and the
`check-content-preflight` shell smoke test, all passing.**

An earlier integrated checkpoint passed all **783 workflow tests**. After the
integration added duplicate-id validation, chronology publication, hold-link
filtering and their tests, the final tree passed all **788 workflow tests** in
995.751 seconds. Both pipeline files load, and `check-content-preflight --list`
reports thirteen checks.

`test_generation_metadata` fails 11 on ecclesiastical-latin curriculum
documents. That is pre-existing — verified against a clean `HEAD` worktree —
and is nothing to do with this work.

## Merge reconciliation verified

The merge combined two independent rewrites of `_failure_budget_spent`. The
verified combined rule is:

- a reviser's `finding_dispositions` displaces the id comparison wherever the
  receiving stage declares `reports_repairs`;
- where no stage on the route can report, the comparison stays, and is
  owner-aware — an id returning under a *different* `repair_target` is
  progress, not a repeat;
- a gate keeps the comparison whatever a reviser says, because a gate's ids
  are its own check ids.

Result validation now also rejects duplicate finding ids within one result and
across the engine's joined fan-out, so the owner-aware comparison cannot be
spoofed by last-write-wins identity collisions.

## The Fourteenth Sunday itself

Run `90dcdddcb6780e60` is BLOCKED and cannot be advanced or statused against
the current pipelines. Its ignored directory did not cross the original Git
handoff, and this clone still has no formal
`evaluations/blocking-findings-v1.toml`. The source data originally survived
only in run `90dcdddcb6780e60` of the originating `triptych/proper-54`
workspace. The exact final joined result and the sole second revision-pass
result have now been copied into the leaf as
`research/production-content-evaluation-0002.json` (SHA-256
`0524513300e424331c4fee02595ccb156002a7564203680d4424cd02fe2e03fb`) and
`research/production-content-revision-0001.json` (SHA-256
`f89dfec80d884273343d639c2611b01be1fcd11428be254fd70ac75140f22a62`).

The seven blocking findings in the final joined evaluation are:

- `CON-EVI-020` — remove or qualify the unchecked Mozarabic Latin wording and
  the uncollated `quam`/`quoniam` variant.
- `CON-EVI-021` — correct the false claim that the Latin vice list is longer
  than the Greek list; the verified counts are 17/17 for vices and 12/9 for
  fruits.
- `CON-REC-010` — carry Aquinas and Hilary on Matthew 6:33 into both editions,
  explicitly as readings of the Gospel verse rather than the antiphon.
- `CON-CIT-020` — correct the King James reference entry so it describes and
  locates the comparison work actually used throughout the guide.
- `CON-CIT-021` — restore the page-image punctuation, capitalization, and
  `Soloman` spelling in the fourth gallery entry, or narrow its verification
  claim.
- `CON-PRO-001` — remove checksum and byte-matching mechanics from six
  reader-facing passages while retaining the source and evidence bounds.
- `CON-PRO-002` — rewrite the sixteen reader-facing process/provenance labels
  as claims about sources, texts, witnesses, or facts.

This enumeration is a recovery synopsis, not a claim that the old engine wrote
the formal standing-findings file. The tracked joined-result copy preserves
every full location, problem and required result, while the originating lane
files remain available for lane-level provenance.
`build/tpt-runs/ca03f1b357e7ec25` may be swept; its eight findings are
accounted for by id in PROJECT-WORK.md, seven closed and one reopened.

A new production seeds against `proper-finish` v3. It will now get
`DOCUMENT_ROOT` and `REPAIR_TARGETS` in its packets, a `content-preflight`
carrying thirteen checks, including all three chronology checks and both prose
screens, and a `content-evaluation` that writes its standing findings to a
tracked file.

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

The apparent five-fields disagreement is resolved: the contract is anchors
plus four fields, or five mechanically checkable requirements. Proposal count
remains a separate possible `proposal-count` check rather than being silently
added to `proposal-fields`.

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
