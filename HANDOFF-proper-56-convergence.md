# Handoff: the Sixteenth Sunday, and why the workflow now sequences its editions

Written 2026-09-09 on `feature/claude/propers/tlm/56`, at the end of a session
that hit a weekly model limit inside `derive-synthesis`. It covers two things
that happened in one session: a production of the Sixteenth Sunday after
Pentecost that exhausted its iteration ceiling, and the workflow change that
diagnosis paid for — `proper` v25 → v26 and `proper-finish` v3 → v4.

Read this before touching the leaf or the pipelines. The short version: the
canonical edition is finished and has passed a five-lane content evaluation
with zero findings; the synthesis companion is **half-derived and not
finished**; and the run is live and resumable at `derive-synthesis`.

## State on arrival

| | |
| --- | --- |
| branch | `feature/claude/propers/tlm/56`, pushed |
| live run | `29f20fa20e542429`, `proper-finish` v4 |
| current stage | `derive-synthesis`, awaiting iteration 0 |
| dead run | `e4aebcbd941b6b1a`, `proper` v25 — fails closed on the version bump |
| leaf | `src/claude/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost` |

Both editions build. Canonical 45 pp., companion 29 pp. All twelve
`check-content-preflight` checks pass. `research/scope.md` is 341,720 bytes and
has not been touched since `research-synthesis` wrote it.

**Resume with:**

```
tools/tpt proper-finish \
  liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost \
  status 29f20fa20e542429
```

The packet to execute is
`build/tpt-runs/29f20fa20e542429/packets/derive-synthesis-0000.txt`, at
reasoning effort `xhigh`, exactly one subagent, result to
`build/tpt-runs/29f20fa20e542429/results/derive-synthesis-0000.json` carrying
`"stage": "derive-synthesis"` and `"iteration": 0`.

## The unfinished work, precisely

`derive-synthesis` ran and died mid-edit. It wrote **no result file**, so the
engine still awaits iteration 0 and a fresh subagent may simply redo the stage.
What it left behind:

- `sections/synthesis/20-integrated-commentary.tex` — **partially rewritten**,
  mtime `09-06 19:06`. Its own last words were "let me correct several claims
  where my rewrite drifted from the canonical", so it knew its draft had drift
  in it and did not get to fix it. **Do not trust this file.** Re-derive it
  against the settled canonical edition rather than reading it as a base.
- Everything else untouched: `synthesis.tex`, `format.tex`, `main.tex` and all
  canonical `sections/` still carry their content-evaluation mtimes (`09-06
  18:0x` or earlier).

Three staleness items were recorded for this stage by the stages that could not
fix them. Verify each rather than trusting this list:

1. the companion still says commentators reach Philippians 2 "while expounding
   three different chants" where the canonical edition now prints **one** reach
   (the canonical was corrected under `CON-CIT-001`);
2. the companion still says "three-word petition" where the canonical now reads
   **four-word** (corrected under `CON-CIT-010`);
3. `format.tex`'s canonical `\editionnote` asserts the companion "adds nothing
   this edition does not contain", and `sections/90-scope.tex` carries a fenced
   sentence asserting the NPNF English is named at each use in the synthesis
   edition. Under the sequence these are **constraints the derivation must
   satisfy**, not descriptions of an existing artifact.

## What the production cost, and why

Run `e4aebcbd941b6b1a` (`proper` v25) ran seven content evaluations over 29
hours, 84 packets, ~50 subagent dispatches and 1.6 GB of retrieved sources, and
reached its absolute ceiling with the document in good shape. Blocking findings
per round:

```
18 → 12 → 10 → 8 → 7 → 5 → 7
```

That looks like convergence and is not. Three measured causes:

**1. The advisory channel was a queue, not a verdict.** 19 of 62 blocking
findings — **31%** — were the same lane's own advisory from an earlier round,
promoted a mean of 1.1 rounds later. One lane filed four advisories at
iteration 0 and raised those exact four as blocking at iteration 1; another
filed four at iteration 4 and raised those four at iteration 5. Lanes were not
misbehaving: advisories routed to nobody, so re-filing as blocking was the only
way to be heard, and one lane said so in as many words.

**2. Two lanes carry unbounded verification obligations.**
`citation-integrity` and `evidence-discipline` returned `CHANGES_REQUIRED` in
7 of 7 rounds; `synthesis-argument` failed once and passed six times. Criterion
7 ("every stated count in reader-facing prose") is an exhaustive re-derivation
over ~2,500 lines, so a pass **samples** the checkable claims rather than
enumerating them. Proof: `CON-CIT-029` — a "three witnesses" heading a list of
four — was raised fresh at iteration 6 against text no revision had touched,
after the same lane had read that file at maximum effort six times.

**3. Repairs injected defects.** Documented three times by the lanes:
`CON-PRO-010` was created by the `CON-EVI-012` repair; `CON-PRO-006` went
advisory→blocking because the `CON-CIT-020` repair added a fifth conduct clause;
iteration 6 found revision 3 had reintroduced one clause of a class blocked at
iteration 4.

A fourth cause was **hypothesised and disproved** — see "Two things I got
wrong" below.

## What changed in the workflow

`proper` v26 / `proper-finish` v4. Both manuals updated
(`workflows/OPERATOR.md`, `workflows/ARCHITECTURE.md`).

### The editions are now produced largest first

`author-proper` and the content loop settle the **canonical guide alone**.
Only when it passes does `derive-synthesis` write the companion from it, and
`synthesis-evaluation` — two lanes, `derivation-fidelity` and
`companion-conformance`, single repair owner `derivation` routing to
`synthesis-revision` — judges the companion **against** the settled canonical
edition before the artifacts build.

New files: `workflows/fragments/propers/derive-synthesis.md`,
`synthesis-evaluation.md`, `synthesis-revision.md`,
`lanes/synthesis-fidelity.md`, `lanes/synthesis-conformance.md`,
`workflows/schema/synthesis-evaluation-result.json`.

Rewritten: `content-evaluation.md` and all five content lane fragments, from
"both editions are yours" to canonical-only.

This removed a class rather than policing it. It also gave an owner to the
synthesis↔commentary duplication that two lanes had recorded as an **unowned
observation at six consecutive iterations**: it is decidable only when one
edition is fixed and the other is being derived from it, which is exactly where
`derivation-fidelity` now stands.

### Advisories now travel

`ADVISORY_FINDINGS` is a third packet header beside `PRIOR_FINDINGS` and
`CARRIED_FINDINGS`, carrying an evaluation's non-blocking findings to whichever
stage the route sent the repair. They gate nothing, spend no budget, and are
owed no `finding_dispositions` entry — naming one there is refused, because
`findings_forwarded_ids` records blocking ids only.

`common/result-format.md` now states that **severity is a verdict, not a queue
position**, and that promoting an advisory to blocking is forbidden.

Engine change is in `scripts/_workflow.py`: `_extract_advisory_findings`,
threaded through `_compile_packet` / `_compile_stage_packets` and called
symmetrically from the live transition and from
`_load_prior_findings_for_current`, so replay recompiles identical bytes.

## Two things I got wrong, corrected

**The budget diagnosis was wrong.** I first reported that `stage_repeats` is
charged by comparing finding ids against the immediately-prior standing set.
It is not, for this route: `scripts/_workflow.py` ~2944–3055 charges it from
the reviser's own `finding_dispositions`, and the id heuristic applies only
where no reviser report exists. Every revision reported 100% repaired, so
nothing was charged. The code anticipates exactly this — *"an optimistic
reviser is now the failure mode this has to catch"* — which is what
`stage_failures` and the doubled ceiling are for. **The budget worked as
designed. I changed nothing.**

**Moving the counting into preflight does not work.** I built a
`stated-counts` check for `tools/check-content-preflight`. On the real leaf it
fired eight times and was wrong eight times: `before and after, present and
future` is two items and not four, and `The Propers: Notable and Quotable` is a
title whose colon it read as introducing a list. Narrowed to unambiguous
separators it judged **zero** series — perfect precision, no recall, and a
"0 checked, every number agreeing" line that manufactures confidence. I
reverted it. The negative result is recorded in
`lanes/content-citation-integrity.md` so it is not retried blindly. The
counting class stays a lane criterion because telling an item from a clause is
the judgement the lane is there for.

**A materiality gate was considered and deliberately not built.** Having
already misdiagnosed once, I would not let a subjective "is this material?"
filter suppress real defects on my own judgment. It is the maintainer's call.

## Verification of the workflow change

Compared against a **true baseline**, not exit codes: I stashed every change,
ran the full suite, restored, and diffed the failure sets.

- baseline (stash applied): **216 failures, 3 errors**, 3586 tests
- after the change: **216 failures, 3 errors**, 3595 tests
- **new failures introduced: zero**

All **334** workflow tests pass. Regenerating the document catalogue
(`make document-catalogue`) fixed three pre-existing staleness failures.

Test modules updated to the new contract, not deleted:
`test_workflow_two_editions` was **rewritten** to guard the same hazard under
the sequence — it now asserts the canonical evaluation reads one edition, that
`author-proper` does not write the companion, that the pipeline really is a
sequence, that `derive-synthesis` derives the leaf's form rather than asserting
one, and that `synthesis-evaluation` is where both documents are read together.
Its matchers are still held against the text they replaced, and
`PRE_CHANGE_BOTH_AT_ONCE` exists so the intermediate answer cannot satisfy the
rule that replaced it.

## The new run, round by round

`proper-finish` v4, run `29f20fa20e542429`, seeded against the existing leaf so
that research, the brief and four rounds of prior repair were preserved.

| round | blocking | lanes passing | notes |
| --- | --- | --- | --- |
| author | — | — | provenance record still named the dead run; AMS 188 count left 1 of 6 manuscripts unaccounted; PG 62 cited as though Chrysostom's Greek had been opened; 4 registration statements in `verified.md` contradicted by `src/sources/`; `\allowbreak` printing literally inside a `\url` |
| 0 | 4 | 2 of 5 | 11 advisories forwarded, **9 cleared** by the reviser |
| 1 | 2 | 3 of 5 | 5 advisories forwarded, **all 5 cleared** |
| 2 | 4 | 3 of 5 | went **up**; all four genuinely new small factual errors |
| 3 | **0** | **5 of 5** | PASS |

Ended at 3 of 6 failures and **1 of 3 repeats — nothing was ever re-found**.

Three results worth keeping:

- `synthesis-argument` passed six consecutive rounds in the old run with zero
  findings, then raised a blocking criterion-4 finding on its **first** read
  under the sequence: five passages of the source-grounded synthesis reprinting
  evidence whose fullest home is the commentary, one sentence repeated word for
  word, bold included. The defect was always there; splitting its attention
  across two documents had hidden it.
- `profile-conformance` found the old run's lane results on disk, recognised
  its seven advisories were unrepaired, and **declined to promote them**,
  citing the new rule. In the old run that lane promoted advisories twice.
- Round 2 going 2 → 4 is the sampling problem, undiminished. The structural
  fixes removed the backlog dynamics; they do not make a lane an exhaustive
  detector.

## Decisions waiting for the maintainer

**`CON-PRO-013`, escalation, in the live run's ledger.**
`tools/check-proper-components` ll. 240–254 requires manifest order
`… source-grounded-synthesis, exploratory-synthesis, notable-quotable`, while
`guidance/liturgy/roman-1962-propers.md` ll. 246–265 puts *Notable and
Quotable* at position 7 and *Interpretive Possibilities* at 8, and ll. 168–171
claim the sequence is stated once. The postconciliar profile (ll. 202–203)
agrees with the 1962 one, so **the tool contradicts both profiles corpus-wide**.
Verified by experiment twice, on scratch copies, with the repository manifest
confirmed untouched by sha256. All 18 manifests across `src/claude` and
`src/gpt` carry the tool's order; the documents render the profile's. The check
binds at three gates. Escalations live under `build/`, which `make clean`
removes — **this one needs to leave the run or it is lost.**

## Owed work, named and not done

1. **Finish `derive-synthesis`** and the `synthesis-evaluation` /
   `synthesis-revision` loop, then the mechanical gates, visual evaluation and
   publication. The stage has never completed; this run would be its first.
2. **`generation-metadata.tex` is not brought forward by `content-revision`.**
   Found at iteration 3 and independently confirmed: the file is stamped
   `17:30:18` while revision 2 edited sections at `18:08`–`18:09`, so the
   printed timestamp predates the content by ~39 minutes.
   `content-revision.md` never mentions the file — only `author-proper.md`
   does — and neither check catches it (`check-generation-metadata` validates
   shape; `provenance-matches-run` holds only the five run-identity fields).
   One-line fragment fix, deliberately **not** made here because it would move
   the workflow digest and kill the live run.
3. **A fourth unowned class, four consecutive sightings, unchanged passages.**
   Two reader-facing sections state the same evidence bound at different
   strengths: P3 and P5 say flatly that no chant repertory was reached, while
   C2 reports AMS 188 results from six named graduals; only
   `sections/90-scope.tex` reconciles them. The brief agrees with the leaf, so
   nothing is misreported. It **survived the sequencing change**, so it is a
   genuine missing criterion rather than an artifact of reading two editions.
4. **`format.tex`'s "adds nothing this edition does not contain"** — eight
   sightings across both productions. Under the sequence it is a claim about an
   artifact that does not exist when the canonical lanes read it, and no
   synthesis lane is pointed at it either. Needs an owner.
5. **`CON-PRO-009`**, advisory and unrepairable here: `research/scope.md`
   receipts three retrievals at `build/tpt-runs/e4aebcbd941b6b1a/artifacts/` —
   a dead run's directory under ignored, sweepable `build/`. Only
   `research-synthesis` writes the brief and `proper-finish` has no such stage.
6. **`research/scope.md` l. 3188** repeats the Exod. 23:5 error the leaf fixed
   under `CON-CIT-012` (23:5 is an ass under a burden; the fallen ox is Deut.
   22:4). Immutable to every stage of a `proper-finish` run.
7. The Sarum binding's `context` in `research/source-bindings.toml` still says
   no 1662 text was opened, which the leaf's Brightman/Blunt material
   supersedes.

## One hazard to know about

**Any edit to a pipeline, fragment or schema kills every live run.**
`load_bound_workflow` (`scripts/_workflow.py` ~463) fails closed on a changed
digest, and separately on a version bump. That is what ended
`e4aebcbd941b6b1a`; it is by design and it is right, but it means workflow
repair and production cannot proceed in the same breath. Finish the run, or
accept that fixing the workflow ends it and seed again.

`proper-finish` is the tool for the second case: it begins at `author-proper`
and reuses the existing brief and leaf, so a workflow change costs the
authoring and evaluation rounds but not the research.

## How this session worked, in case it helps

Every stage was dispatched as the packet's execution policy declared: one fresh
subagent for `SINGLE`, five concurrent for `FANOUT / HOST-MAX`, at the effort
the roster named. Every lane result was validated before the join — schema
shape, `lane_packet_hash` against the packet's own bytes, all five mandatory
fields on every finding, `repair_target` on blocking only, `escalated_to` on
escalations only — and every revision's `finding_dispositions` was checked to
name exactly the forwarded set. `research/scope.md`'s byte size and the
companion's mtime were checked after every stage that was forbidden to touch
them.

Two things I would do differently. I inlined ~9k-token lane packets five at a
time for the first production's evaluation rounds; delivering by file path, as
the second production did throughout, is equally faithful and much cheaper.
And I twice reported page counts and labels from a build that predated the
edits I was verifying — check the PDF's mtime against the newest source mtime
before quoting either.
