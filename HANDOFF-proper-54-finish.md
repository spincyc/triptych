# Handoff: the Fourteenth Sunday, two productions, and what each iteration cost

Written 2026-09-09 on `feature/claude/propers/tlm/54`, at a weekly rate limit
that killed four of five evaluation lanes mid-flight. Read
`HANDOFF-proper-54-convergence.md` first for what preceded this; that document
ends where this one begins.

Two productions ran. The first, `efff3a6f73c1f451` on `proper` v25, went from
seed to `BLOCKED` at the content loop's absolute ceiling. The second,
`45f0ddc21d634d9a` on `proper-finish` v4, is live and one lane short of a
complete evaluation. Between them a maintainer-approved repair pass encoded two
of the first run's findings into the workflow itself.

Everything below is what a successor needs that the run records do not already
carry.

## Where to resume, in one paragraph

Run `45f0ddc21d634d9a` awaits `content-evaluation` iteration 4. Its five lane
packets are compiled and `replay` reports all five deterministic and
`recorded_file_intact: true`. **One lane result is already written and valid** —
`synthesis-argument`, at
`.scratch/tpt/45f0ddc21d634d9a/content-evaluation-0004-lane-02-synthesis-argument.result.json`,
`PASS`. The other four lanes never wrote a result. Re-dispatch those four
against their existing packets, then advance with all five `--lane-result`
flags. Budget stands at 4/6 consecutive failures and 1/3 repeats. Note that
`.scratch/` and `build/tpt-runs/` are Git-ignored, so that surviving lane result
is not in this commit and will not survive `wt tidy`; if it is gone, re-dispatch
all five.

## The two runs, stage by stage

### Run `efff3a6f73c1f451` — `proper` v25, seed to BLOCKED

32 packets, 32 results. Stages passed on first attempt: `seed`,
`authorize-target` (target already authorized 2026-08-27, nothing written),
`scope-gate`, `resolve-context` (chronology already byte-current),
`source-audit`, `research` (seven lanes, 119 findings, no duplicate ids),
`research-synthesis` (`PASS`, zero findings, brief 5,854 → 8,862 lines),
`source-registration`, `author-proper`.

Then the content loop, which is the whole story:

| iter | blocking | lanes passing | reviser reported | actually survived |
| --- | --- | --- | --- | --- |
| 0 | 19 | 1 | 19/19 repaired | 4 |
| 1 | 17 | 1 | 17/17 repaired | 3 |
| 2 | 9 | 1 | 9 → 8 repaired, 1 not-repaired | 1 |
| 3 | 11 | 1 | 17/17 repaired | 1 |
| 4 | 13 | 1 | 13/13 repaired | 1 |
| 5 | 5 | 3 | 5/5 repaired | 0 |
| 6 | 7 | 1 | 7/7 repaired | 0 |
| 7 | 1 | **4** | — | — |

It blocked at 8/8 consecutive failures with **one** blocking finding standing
and four of five lanes passing. `tpt`'s own message is the accurate diagnosis:
*"The repeat budget (3/4) never ran out because no round reported a repair it
could not make; the absolute ceiling stops a stage that finds something new
forever."*

63 blocking findings were closed across seven revisions. The run did not fail at
repair. It failed because evaluation kept finding new work, and the ceiling
counts failures rather than progress.

### The repair pass — commit `9d7e9c348`

Approved by the maintainer after the block. Four changes:

1. **`CON-EVI-052` repaired in the leaf** — the word `unregistered` restored to
   the three Benziger page-image readings at `30-commentary.tex` ll. 12–17 and
   the two dependent table cells, with the reading as grammatical subject so
   criterion 12's conforming form is preserved. That was the run's one standing
   finding.
2. **Criterion 12 now states the conforming form of an evidence bound** —
   witness, text or reading as grammatical subject, with a worked example, and
   the rule that a criterion-12 repair removing such a bound *its qualifying
   adjective included* trades one criterion's defect for criteria 1 and 2's.
3. **`Generation Metadata` joins criterion 12's out-of-scope list**, settling
   escalation `CON-PRO-010` on the reading every iteration of that lane acted
   on.
4. **The id-stability instruction was reconciled with the engine.** See "What I
   got wrong" below — this one is not what it first looked like.

`proper` 25 → 26, `proper-finish` 3 → 4. Version-pinned tests, both manuals and
the tracked document catalogue were updated with them.

### Run `45f0ddc21d634d9a` — `proper-finish` v4, live

`author-proper` → `content-preflight` → four content evaluations and four
revisions:

| iter | blocking | lanes passing | reviser reported | survived |
| --- | --- | --- | --- | --- |
| 0 | 8 | 2 | 8/8 repaired | 0 |
| 1 | 4 | 3 | 4/4 repaired | 0 |
| 2 | 3 | 4 | 3/3 repaired | 0 |
| 3 | 2 | 4 | 1 repaired, 1 **not-repaired** | — |
| 4 | incomplete — 1 of 5 lanes reported | | | |

**Nothing has survived a repair in this run.** Every finding raised has closed
on independent verification the following round. That is the difference the
repair pass and `author-proper`'s advisory sweep made.

## What led to each re-iteration, and the four recurring causes

Read this section before dispatching anything. The counts above are noise; these
four mechanisms are the signal, and three of them are still live.

### 1. The criterion-12 ↔ criteria-1/2 oscillation (fixed in v4, verify it stays fixed)

Criterion 12 wants the guide's own handling out of reader-facing prose. Criteria
1 and 2 want an evidence bound stated where the reading is used. A repair to
either can delete what the other requires. In run one this fired **four times**:
`CON-EVI-003` twice, `CON-PRO-004` as a regression, and finally `CON-EVI-052`,
which ended the run — the criterion-12 repair removed the word `unregistered`.

v4's criterion 12 now gives the conforming form and names the adjective case.
Run two has not oscillated once. Intervention `0004` of run one records the
history.

### 2. A repair swinging past the truth in the other direction (live)

Run two, `CON-REC-001` → `CON-REC-011`. The Epistle's closing paragraph said
five Latin commentaries "add nothing to the question" though none was opened.
The repair narrowed it to "were not opened" — and the leaf **quotes Cornelius a
Lapide's Galatians *Argumentum* on page 2**. Three passes over one sentence:
too strong, too absolute, then exact.

The lane's own summary of the fix that held: the appendix and References now
*agree* with the commentary rather than merely differing less.

### 3. A count true when written, falsified by a sibling leaf (live, and structural)

`CON-CIT-105`. The guide's cross-formulary denominator said "twenty-one collated
text records covering fifteen distinct 1962 identities". The repository holds
**22 records over 16 identities**; the sixteenth, `src/gpt/.../55-fifteenth-after-pentecost`,
was committed at `f01cd6ed1` on 2026-09-03 — three days before this leaf was
authored. No gate can see this. It will recur for every leaf in the collection
whenever another one lands.

The reviser resolved it by **re-bounding rather than recounting**: `90-scope.tex`
now names the records *the research sweep behind this guide ran over*, because
publishing measurements over 22 records no research lane swept would be worse.
The disclosed cost: the leaf's cross-formulary claims are now explicitly bounded
to a sweep, not to the collection, and a reader comparing against the repository
will find sixteen identities where the guide says fifteen — correctly, and by
design.

### 4. Pagination cascade that no gate can see (live)

`\sectionguard` is `\Needspace{7\baselineskip}`, **not** `\clearpage`, so the
canonical edition flows continuously from page 5 to the end. A 28-word repair
inside an early `\correction` box displaced that unbreakable box and surfaced as
a two-line widow on a new page 51 — **forty-five pages downstream of the edit**.
It bit on three separate occasions and was caught each time only because a
worker read the built page count.

`check-proper-components --aux` verifies that the brief-synthesis anchors are
adjacent at N, N+1, N+2 — never that N is 3 — so it accepts the entire reader
order displaced by a constant, which is exactly what a page-1 overflow produces,
and it says nothing about a widow tens of pages away. Interventions `0000` and
`0001` of run two carry the mechanism and two candidate fixes; **recording the
canonical edition's expected total page count in `proper-components.toml` is the
one that would have caught all three instances.**

## What I got wrong, so you don't repeat it

**I proposed carrying prior-iteration finding ids into evaluator lane packets.**
That was wrong, and the engine says so: `scripts/_workflow.py` records the
decision explicitly — *"an id is a handle a lane minted for its own report; it is
not an identity for a defect, and comparing ids across iterations compares
nothing"* — which is precisely why v25 moved the budget onto the reviser's
`finding_dispositions`. The real defect was the **instruction**, which still told
lanes ids were "load-bearing" for a budget that no longer reads them. v4 now
says what is true and points lanes at the one id set they can recover: the
leaf's own `evaluations/blocking-findings-v1.toml`.

**I put `REPAIR_TARGETS: ["research","brief","authoring"]` in all five
iteration-0 dispatch headers of run two.** `proper-finish` admits **only
`authoring`** — it has no research or research-synthesis stage. A blocking
finding naming an unadmitted owner is refused and the refusal fails all five
lanes. The `synthesis-argument` lane caught it, treated its packet as
authoritative over my dispatch, and told me. Two lanes had already routed around
it unprompted. **The packet is the authority; say so in every dispatch and mean
it.**

**I miscounted the collated records as 21/15** when adjudicating a dispute
between two lane instances, because my glob covered only `temporal` and missed a
record. The correct figure is 22/16, which is what both lanes had said. Verify
before contradicting a lane.

## What is still open

**Two blocking findings, awaiting the incomplete evaluation:**

- `CON-CIT-107` — reported repaired after a class sweep that found five members
  beyond the nine named. Unverified.
- `CON-CIT-110` — reported **`not-repaired`**, on the ground that the finding is
  mistaken. This is the live dispute and the next `citation-integrity` lane must
  adjudicate it. The sentence at `30-commentary.tex` ll. 2638–2643 says three of
  the fifteen carry `semper` in an oration and this Sunday alone twice. Both
  lane instances are arithmetically right over different sets: three over the
  sweep's fifteen, four over the corpus's sixteen. The reviser argues the
  sentence is bounded where the reader meets it — *"Of the fifteen 1962
  formularies this guide has collated … the only one of those fifteen"* — and
  added a clause naming the exclusion outright. A finding withdrawn on evidence
  is a good outcome; this stage has seen a lane withdraw one before.

**One escalation, for the maintainer, in a file no run may write.**
`CON-SYN-206`: the profile at ll. 180–183 makes the synthesis companion carry
both an integrated commentary and a source-grounded synthesis over one formulary
and one evidence set, while ll. 193–195 and l. 305 forbid the resulting
duplication — and criterion 4 was lifted out of l. 305 but **stopped one sentence
short of "one fullest home"**. Measured across four iterations at 31.7–32.1%
verbatim overlap, with within-unit repetition at 0.0–6.4%, which is what makes it
the profile's bind rather than the leaf's sloppiness. Recorded eight times as an
observation in run one before a lane found the shape that carries a decision.

**Structural gaps worth a maintainer's attention:**

- **Advisories reach no reviser.** Only blocking findings are routed, so an
  advisory is write-only: it accumulates in the tracked findings file and no
  stage is obliged to disposition it. In run one `CON-SYN-002` stood
  byte-identical through eight evaluations because nobody was ever told, and
  `CON-PRO-009` grew from two loci to eight while advisory before going
  blocking. Run two's `author-proper` cleared roughly thirty of them **only
  because the driver told it they existed** — nothing in the workflow does.
- **A stale brief layer will regenerate a repaired defect.** `research/scope.md`
  §11.7(c) still writes the a Lapide negative loosely where §4.3/§5.2 write it
  narrowly. A later pass meeting §11.7(c) alone would reinstate exactly what two
  evaluations spent findings removing. No stage of `proper-finish` may write the
  brief.
- **Cross-edition references resolve in only one edition.** `CON-CIT-107`'s
  class: sentences in shared files pointing at canonical-only material. Fourteen
  found so far. Nothing checks that a locator in a shared file resolves in both
  editions.

## Practical notes for the next driver

- **Dispatch discipline.** One fresh subagent per lane, none besides. In run one
  a `profile-conformance` lane spawned helper agents whose output alone ran to
  ~2,600 lines, and that fan-out inside a lane is part of what exhausted a
  session budget and killed all five lanes mid-flight. Every dispatch since has
  said "do not spawn sub-agents", and none has.
- **Effort.** This host exposes no per-dispatch reasoning-effort control;
  subagents inherit the session level. The whole of both runs was answered at
  `xhigh` while `content-evaluation`'s five lanes and `source-audit` declare
  `max`. The maintainer decided that on 2026-09-05; intervention `0000` of run
  one records exactly which stages ran below and above their declared level.
- **What survives a cleanup.** `build/tpt-runs/` and `.scratch/` are Git-ignored.
  `wt tidy` and `wt sweep` delete both without asking — the run record, every
  packet, every result, and all seven interventions. The leaf's
  `evaluations/blocking-findings-v1.toml` is tracked and is the only part that
  outlives the workspace.
- **Verify, don't accept.** Every lane that caught a real regression did it by
  extracting the built PDFs, running its own greps, or diffing against a
  pre-repair build left in `build/`. The lanes that took a reviser's report at
  face value found nothing.
