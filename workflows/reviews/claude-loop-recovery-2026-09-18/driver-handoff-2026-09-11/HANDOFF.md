# Handoff: three Claude propers leaves under the tpt workflow engine

Written 2026-09-11 at the operator's request, for a clean agent to inspect.
Everything here is read off run state, commits and result files on disk, not
recalled. Paths are relative to
`<checkout of the claude/propers/tlm/merge workspace>`.

**Read this section first if you read nothing else.** The task has consumed
roughly 12 hours and five workflow runs. One leaf (55) is authored, typeset,
installed and stopped on six *site-level* gates; one leaf (56) is two stages
from done; one leaf (54) has not been started. The operator's judgement is
that this is not converging. Section 6 is my honest account of where the time
went and which of it was avoidable. Section 7 says what I would do next and
what I would stop doing.

---

## 1. The task as given

Drive three leaves to completion under `tools/tpt proper-finish`, one at a
time, in order: `55-fifteenth-after-pentecost`, then
`56-sixteenth-after-pentecost`, then `54-fourteenth-after-pentecost`.

Branch `feature/claude/propers/tlm/merge`, starting at `57bae9ebf`.

Driving rules the operator set:

- Follow the exact command tpt prints after every advance; stop only at
  ACCEPTED or BLOCKED.
- One fresh subagent per stage, or one per lane on a fan-out stage, at the
  effort the roster names. Hand each its packet by absolute path plus the
  SHA-256 tpt printed; it verifies the hash before reading.
- Never do a stage yourself; never summarise or merge lane results — tpt
  performs the join.
- Before any fan-out join, run
  `python3 .scratch/tpt/validate-lanes.py RUN_ID STAGE ITERATION`.
- Commit the leaf at each checkpoint, saying what was repaired and verified.
- Do not edit anything under `workflows/` while a run is live: a run is bound
  to the workflow-source digest and an edit kills it.
- If a run stops because review did not terminate, that stop is a question
  for the driver, not a verdict on the leaf.

---

## 2. Where everything stands right now

### Commits on the branch, newest first

```
51523b23f  09-11 07:11  56-sixteenth-after-pentecost: clear the visual review
1ed09fa7c  09-11 04:59  propers(56): settle the companion on the second run
99490db98  09-11 03:55  propers(56): settle the canonical edition and its brief on the second run
05b8887a7  09-11 01:23  propers(56): record the review-termination stop and what it left standing
f1bf45bc6  09-11 01:00  propers(56): drain the seam class through its third surface
0fdba17e3  09-10 23:34  propers(56): derive the companion and clear its seam in one round
4acde50da  09-10 22:38  propers(56): re-anchor the Sixteenth Sunday on the chronology corpus as it now stands
9f7674645  09-10 21:14  workflow: read the companion with a program, and stop one evaluator erasing the other (v29 / finish v7)
05ebbb86e  09-10 17:23  propers(55): install the Fifteenth Sunday's publication
d7ef40121  09-10 16:54  web-edition: splice an inline edition branch without breaking its sentence
411149765  09-10 15:46  propers(55): separate the heading levels and spend the page-2 escape on size alone
59fdc0aaa  09-10 14:22  propers(55): clear the seam the companion's form makes visible
533410c3b  09-10 12:00  propers(55): settle the canonical edition under proper-finish v6
57bae9ebf  09-10 10:10  workflow: stop reviewing a document that is not getting worse (v28 / finish v6)
8ec91c1e3  09-09 ...    propers(55): rewrite the companion commentary as its own argument
```

Working tree at time of writing: clean (leaf 56 committed at `51523b23f`).

### Leaf 55 — `55-fifteenth-after-pentecost`

**Stopped at six site-level gates, not at anything wrong with the leaf.**

Live run `05f2d2fd7c2cf8b3`, workflow `proper-finish` **v6**, current stage
`publication-revision`. Its last four packets were `web-evaluation 1`,
`install-publication 0`, `publication-gates 0`, `publication-revision 0`.

Standing blocking ids, all on `publication-gates`:

```
GATE-CATALOG-READ-LINK-RESOLVES
GATE-SITE-DOCUMENT-CATALOGUE
GATE-SITE-PUBLIC-ALPHA
GATE-SITE-RELEASE-BINDINGS
GATE-SITE-WEB-EDITIONS-CURRENT
GATE-WEB-EDITION-TRACKED
```

Every one of those is a property of the **site**, not of leaf 55: they ask
whether the whole corpus's PDF tree, catalogue and web editions are present
and current. They could not pass while most of the corpus had never been
built. That is why the corpus build was authorised and done (see §5).

Accepted ids bound in that run: `SYN-CON-009`; `VIS-DEN-002`, `VIS-DEN-003`,
`VIS-RHY-003`; `WEB-002`.

The run is at workflow v6 and the workflow is now v7, so **this run cannot be
advanced** — the workflow-source digest it is bound to no longer matches. It
must be re-seeded under v7. Two earlier 55 runs are dead: `6fb5fba4867eb8cf`
(v5, BLOCKED) and `da04e65ca4ec963b` (v5, retired by the version bump).

Leaf 55's standing-findings record is at
`src/claude/.../55-fifteenth-after-pentecost/evaluations/blocking-findings-v1.toml`
— still **schema 3**, written by run `05f2d2fd7c2cf8b3` at
`synthesis-evaluation` iteration 3, `standing = 0`, `accepted_count = 1`.
(The schema is now 4; this file predates the change and will be rewritten on
the next run.)

Two findings were left standing unrepaired on an earlier 55 run —
`SYN-CON-001` and `SYN-CON-002`, twenty-four locators and four statements
that resolve in the canonical and dangle in the companion — plus an
escalation `CON-CIT-003` addressed to a human maintainer. Check the record
above for whether they still stand before assuming they do.

### Leaf 56 — `56-sixteenth-after-pentecost`

**Two stages from done.** Live run `b16414357535992e`, workflow v7, current
stage `web-evaluation` (iteration 0 was in flight when I stopped).

Completed in this run: `author-proper` 1, `brief-revision` 3,
`content-preflight` 4, `content-evaluation` 4, `content-revision` 3,
`derive-synthesis` 1, `synthesis-preflight` 2, `synthesis-evaluation` 2,
`synthesis-revision` 1, `build-artifacts` 1, `mechanical-gates` 3,
`visual-evaluation` 3, `visual-revision` 2, `final-acceptance` 1,
`publish-artifacts` 1, `generate-web` 1, `web-evaluation` 1.

Remaining: finish `web-evaluation`, then `install-publication`, then
`publication-gates`. **`publication-gates` will very likely stop on the same
six site gates that stopped leaf 55** unless the corpus state now satisfies
them — this is the single most important thing for a fresh agent to check
before driving anything else.

Artifacts installed (ignored paths, `.gitignore:14 /pdf/*`):

```
pdf/claude/.../56-sixteenth-after-pentecost.pdf            45 pages  365919670f05c42c…
pdf/claude/.../56-sixteenth-after-pentecost-synthesis.pdf  29 pages  0770adf737bd0cf2…
```

Web edition generated at
`build/web/claude/.../56-sixteenth-after-pentecost.md` (205,597 bytes,
sha256 `dfc8289d0565…`). Not yet in the tracked `web/` tree;
`install-publication` writes that.

Accepted ids bound in the run: `VIS-DEN-002`, `VIS-DEN-003`, `VIS-FIX-001`,
`VIS-RHY-004`.

An earlier 56 run `53bdb2eaab3ba398` (v7) is BLOCKED — it stopped on review
non-termination at `synthesis-evaluation` after 4 iterations. Its findings
`SYN-FID-005` and `SYN-CON-012` survived into the current run through the
standing-findings record, which is the schema-4 merge working as intended.

### Leaf 54 — `54-fourteenth-after-pentecost`

**Not started.** One defect is already known from the corpus build: its
companion's brief synthesis begins on page 4 where the profile fixes page 3.
The corpus build halted on exactly this:

```
proper-component error: brief synthesis must begin on page 3,
as the profile fixes it, not page 4
```

so `54-fourteenth-after-pentecost-synthesis.pdf` is the one claude PDF
missing from the installed tree (claude 59/60).

---

## 3. Iteration ledger — every run, every stage

Read straight from each run's `state.json`. `build/tpt-runs/<run>/` holds the
packets, results and interventions for each.

| run | leaf | wf | state | stage iterations |
|---|---|---|---|---|
| `6fb5fba4867eb8cf` | 55 | v5 | BLOCKED | author-proper 1, brief-revision 5, content-preflight 9, content-evaluation 8, content-revision 8 |
| `da04e65ca4ec963b` | 55 | v5 | retired by version bump | author-proper 1, content-preflight 2, content-evaluation 2, content-revision 1, derive-synthesis 1, synthesis-evaluation 2, synthesis-revision 1 |
| `05f2d2fd7c2cf8b3` | 55 | v6 | live, at publication-revision | author-proper 1, content-preflight 3, content-evaluation 3, content-revision 2, derive-synthesis 1, synthesis-evaluation 4, synthesis-revision 3, build-artifacts 1, mechanical-gates 2, visual-evaluation 2, visual-revision 1, final-acceptance 1, publish-artifacts 1, generate-web 1, web-evaluation 2, web-revision 1, install-publication 1, publication-gates 1, publication-revision 1 |
| `53bdb2eaab3ba398` | 56 | v7 | BLOCKED (review non-termination) | author-proper 1, brief-revision 1, content-preflight 2, content-evaluation 2, content-revision 1, derive-synthesis 1, synthesis-preflight 4, synthesis-evaluation 4, synthesis-revision 3 |
| `b16414357535992e` | 56 | v7 | live, at web-evaluation | see §2 |

**The churn is visible in row one.** Leaf 55's first run spent 9
content-preflight, 8 content-evaluation and 8 content-revision iterations and
still blocked. Everything since has been an attempt to stop that from
recurring, and it did not recur — the same stage on the current 56 run took
4 / 4 / 3.

### Interventions (run debt I recorded)

```
build/tpt-runs/6fb5fba4867eb8cf/interventions/  0000…0006  (7)
build/tpt-runs/da04e65ca4ec963b/interventions/  0000…0002  (3)
build/tpt-runs/05f2d2fd7c2cf8b3/interventions/  0000        (1)
build/tpt-runs/53bdb2eaab3ba398/interventions/  0000, 0001  (2)
build/tpt-runs/b16414357535992e/interventions/  0000…0002  (3)
```

`build/tpt-runs/b16414357535992e/interventions/0002.json` is the newest and
the most important: it records that **an `accepted` rationale is never checked
against repository guidance**, and because `accepted` binds a run, a wrong
acceptance is final. See §4.

---

## 4. The convergence problem: what I found and what I changed

### 4a. The seam class (leaf 55, then 56)

Both leaves cycled because one class of defect kept reappearing wearing a new
surface each round. The class: a shared clause that is true in the canonical
edition and false or dangling in the companion. Its surfaces, in order of
appearance: locator words; then "what this edition did with a source"; then
"lists of loci / canons / sections a source supplies". Each round an evaluator
met the class as if new.

**What I did:** front-loaded the class's full history into revision briefs.
Effect: leaf 55 took 3 rounds to clear the seam; leaf 56 took 1.

**What is still wrong:** nothing in the workflow carries this. It worked
because the driver remembered. A fresh driver will not.

### 4b. No program gate between `derive-synthesis` and `synthesis-evaluation`

`proper-finish` sent a freshly derived companion straight to an AI evaluator
with no mechanical screen, so evaluators spent iterations on defects a program
can find. `content-preflight` had a counterpart on the canonical side; the
companion had none.

**Fixed in v29 / finish v7** (commit `9f7674645`): added a
`synthesis-preflight` gate stage (`type: gate`, `execution.mode: program`,
`pass_transition: synthesis-evaluation`, `fail_transition: synthesis-revision`,
`max_iterations: 3`) with seven checks — `references-used`,
`identifiers-resolve`, `restricted-not-reproduced`, `unquoted-not-quoted`,
`structural-meta-labels`, `house-voice`, `proposal-fields`. `derive-synthesis.next`
and `synthesis-revision.next` both route to it.

`tools/check-content-preflight` gained `--edition canonical|synthesis|leaf`
(default `leaf`, so existing invocations are byte-identical), with
`flag_defined()` reading definedness off `synthesis.tex` rather than assuming
it, and `resolve_edition()` walking guards over a comment-masked copy.

### 4c. One evaluator erasing another's standing findings

`_record_standing_findings` rewrote the whole record each time, so whichever
evaluation stage wrote last erased the other's findings. Both propers
pipelines declare `records_standing_findings` on two stages, not one; the docs
claimed otherwise and were wrong.

**Fixed in v29 / finish v7:** `STANDING_FINDINGS_SCHEMA = 4` in
`scripts/_workflow.py` — the record is now read, merged by `(stage, id)` for
findings/accepted/advisories and by `(stage, location, note)` for
observations, and only the recording stage's entries are replaced. Verified in
production twice: within a run, and across runs (56 run 1's `SYN-FID-005` and
`SYN-CON-012` survived four content-evaluation writes in run 2).

`workflows/OPERATOR.md` and `workflows/ARCHITECTURE.md` were corrected where
they asserted the single-stage claim.

### 4d. `accepted` can be granted against explicit guidance — OPEN

Found today on leaf 56 and recorded as run debt. At `visual-evaluation`
iteration 0 the `page-rhythm` lane filed `VIS-RHY-004` — canonical page 45
carrying only the rights colophon — as **accepted**, reasoning:

> "a colophon standing alone on a final page is a conventional book form, so
> a reader who reaches it is not misled and does not read it as a fault."

Three guidance lines forbid that form in as many words:

- `guidance/editorial.md:318` — "It must never force a rights-only page."
- `guidance/repository.md:244` — "it must not force a dedicated page."
- `guidance/editorial.md:395` — the pre-install alpha gate tests the colophon
  for having "created a spill page", as an item *distinct* from sparse spill
  pages generally.

Because `accepted` binds the run, that acceptance would have shipped a
guidance violation. It was caught only because a *different* lane reached the
same page under a different criterion at iteration 1 and raised it with the
citations attached (`VIS-APP-004`, repaired). A single-lane stage, or a lane
roster whose criteria did not happen to overlap, would have shipped it.

**Proposed fix, not implemented:** require an accepted finding to state that
it checked the applicable guidance and found no rule against the form; and
give lane fragments the guidance loci their criteria touch, so acceptance is
made against the text rather than typographic intuition.

### 4e. Advisory forwarding follows the route winner, not the file owner

Observed three times on leaf 56 run 2: leaf advisories stranded at
`brief-revision`, and `content-revision` twice dispatched with a wholly empty
packet. Recorded as run debt; not fixed.

### 4f. A canonical defect found after `content-evaluation` passes has no repair owner

Re-seeding restores `author-proper`'s reach, which is how 56 run 2 repaired
four defects run 1 could see but not route. Structural; not fixed.

### 4g. Other workflow changes made this session

- **v28 / finish v6** (`57bae9ebf`, pre-existing at task start): `stage_novel`
  counter bounded by `max_novel_iterations`; `REVIEW_SCOPE` diff-scoped
  evaluation with `out_of_scope_reason`; the `accepted` severity; a `seam`
  repair owner on `synthesis-evaluation` routed to `synthesis-revision`.
- **`tools/web-edition`** (`d7ef40121`): `select_web_branches` kept the
  newlines around the inline `\ifdefined\TriptychSynthesisEdition … \else …
  \fi{}` form, which pandoc read as paragraph boundaries — splitting **32
  sentences mid-clause** across the corpus. Now splices flush at both seams
  for the inline form only (identified by `\fi{}`); the 59 block-level
  conditionals are untouched. Added a conversion check for a paragraph opening
  on a lowercase word after a block that closed no sentence. All 118 eligible
  editions regenerated with exactly one file moving.
- **`.scratch/tpt/validate-lanes.py`** patched (scratch, not `workflows/`): it
  assumed every evaluator schema declares `finding_enums`, but
  `visual-evaluation` uses the generic `evaluator-result.json`, which declares
  none. Now treats a stage with no admitted `repair_target` as one that routes
  none, and flags a finding that carries the field anyway.

### 4h. Cold review

`.scratch/tpt/cold-review/FINDINGS.md` (1007 lines) holds 18 findings from the
cold review the operator asked for. Roughly 3 are implemented (§4b, §4c and
the `check-content-preflight` edition flag). **~15 remain unimplemented and
unreported to the operator.** `.scratch/tpt/cold-review/PLAN.md` records the
authorised sequence. A fresh agent should read FINDINGS.md and triage.

---

## 5. The corpus build

Authorised by the operator so `check-public-alpha` and
`check-document-catalogue` could pass at all. `make install-all` halted on
leaf 54's companion (the page-3 profile violation in §2), so it was restarted
with `make -k install-all`, then `make -k install PROVIDER=gpt` separately
because `install-all`'s `set -eu` loop stops before gpt.

Result: **217 PDFs — claude 59/60, gpt 152/152.** The one missing is
`54-fourteenth-after-pentecost-synthesis.pdf`.

`src/web/data/structure/documents/corpus.json` regenerated with
`tools/document-library structure`: 140 works, 192 documents, 212 issues,
6177 pages.

Logs: `.scratch/tpt/install-all.log`, `install-all-2.log`, `install-gpt.log`.

---

## 6. Honest account of where 12 hours went

- **Leaf 55's first run (`6fb5fba4867eb8cf`) burned ~25 stage iterations and
  blocked.** That is the single largest loss. The cause was the seam class
  (§4a) plus the missing companion gate (§4b), neither of which I diagnosed
  until after the run had blocked.
- **Two workflow version bumps mid-task**, each of which killed live runs and
  forced a re-seed. v28→v29 was necessary and I would do it again; but it cost
  leaf 55 a complete run and is why 55 sits on a v6 run that can no longer be
  advanced.
- **I chose to fix the engine rather than route around it.** The operator
  endorsed that (fix the workflow, drive 56 and 54 under the new version,
  re-seed 55). It was the right call for the corpus and the wrong call for the
  clock: it front-loaded all the cost onto this session.
- **The corpus build** (217 PDFs) was necessary for the gates leaf 55 stopped
  on, and took a long wall-clock slice.
- **Self-inflicted:** at 55's `synthesis-evaluation` i3 I wrote the budget
  position into two lane briefs, contrary to the established practice that
  evaluators are never told it. I caught it, stopped both agents before they
  wrote anything, confirmed run state untouched, and re-dispatched clean. Cost:
  one round of two lanes.
- **Per-stage dispatch is inherently slow.** Each evaluation lane reads 74
  page rasters and takes 10–15 minutes of wall clock; a four-lane round is
  ~15 minutes, and leaf 56 alone has had three such rounds plus two revisions.
  The engine's design puts a fresh agent on every stage by rule, and the
  driver cannot batch that away.

**What I would not defend:** I kept driving stage-to-stage without stopping to
tell the operator that the end was not in sight. The instruction was to stop
only at ACCEPTED or BLOCKED, and I read that as licence to keep going rather
than as a rule about the *engine's* stopping conditions. A status check after
leaf 55's first run blocked would have been the right moment to raise it.

---

## 7. What I would do next

In this order:

1. **Check the six site gates before driving anything.** Run leaf 55's
   `publication-gates` checks by hand against the current corpus state (the
   PDF tree and `corpus.json` are now built). If they still fail, no leaf can
   finish and that is the thing to fix — not another leaf.
2. **Finish leaf 56**: `web-evaluation` (iteration 0 was in flight), then
   `install-publication`, then `publication-gates`.
3. **Leaf 54.** Its known defect is the companion's brief synthesis starting
   on page 4 where the profile fixes page 3 — a `synthesis-preflight` /
   visual matter that the new v7 gate may now catch mechanically.
4. **Re-seed leaf 55 under v7** and carry it to ACCEPTED. Its content is
   already settled; the run that holds that work is stranded on v6.
5. **Re-pin the 4 stale prose-screen fixtures** in
   `tools/tests/test_workflow_content_preflight.py`. They are pinned to
   already-repaired specimens in claude/54 and gpt/54 and cannot be restored
   by driving; they need re-pinning, which is a test edit safe only when no
   run is live. (Expect 5 failures there until then; the 5th is separate.)
6. **Triage the ~15 unimplemented cold-review findings** in
   `.scratch/tpt/cold-review/FINDINGS.md`, starting with §4d above.

### Things a fresh driver must know

- `.scratch/tpt/DRIVER-NOTES.md` holds the accumulated driving practice —
  including "evaluators are never told the budget position".
- `.scratch/tpt/LANE-BRIEF-TEMPLATE.md` is the lane dispatch shape.
- `visual-evaluation` does **not** declare `records_standing_findings`, so its
  findings never reach the tracked record and lane packets carry an empty
  `PRIOR_FINDINGS`. **A lane cannot recover the ids it minted last round.**
  The driver must read them out of `state.json` and hand each lane *its own*
  ids. Re-raising an `accepted` id as blocking is refused by the engine and
  costs **all four lanes** their work.
- `pdf/` is gitignored (`.gitignore:14`), so `publish-artifacts` produces
  nothing to commit and an empty `git status` after it is correct.
- `generate-web` writes `build/web/…`; the tracked `web/…` tree is written by
  `install-publication`.
- Seed files used so far: `.scratch/tpt/seed-55.json`, `seed-55-second.json`,
  `seed-55-v6.json`, `seed-56-second.json`, `seed-56-v7.json`.

---

## 8. Late finding: the `web-edition` splice fix (`d7ef40121`) is incomplete

Added after §7 was written. Leaf 56's `web-evaluation` iteration 0 returned
**CHANGES_REQUIRED** with 2 blocking, 1 advisory, 2 accepted and 3
observations. Result file:
`.scratch/tpt/b16414357535992e/web-evaluation-0000.result.json`.
The run is now at `web-revision`, which nothing has been dispatched for.

**This is the same defect class `d7ef40121` was supposed to close, and the fix
was under-scoped.** `select_branch` applies the flush splice only when `\fi`
is followed by `{}` — the inline form. A **block-form** guard that happens to
stand *mid-sentence* keeps both its newlines, and pandoc still reads them as
paragraph boundaries. The fix closed the inline case and left the block case
open wherever a block guard is not at a block boundary.

- **WEB-001 (blocking).** The Council of Trent entry in References is split
  into three paragraphs, two of them sentence fragments. The accepted PDF sets
  it as one continuous bullet (p. 43). Source: `sections/99-references.tex:366-372`.
  The converter's own lowercase-opening audit **cannot see this** — both
  fragments open on capitals. So the audit added in `d7ef40121` gives false
  assurance on exactly this case.
- **WEB-002 (blocking).** `the *Tractatus* on John , Chrysostom's` — a space
  before a comma, from `sections/90-scope.tex:93-98`, where the `%`-terminated
  line before `\ifdefined` becomes a pandoc space and the selected branch opens
  on a comma. The only space-before-punctuation in the whole 205 KB file, and
  in none of the seven published siblings. PDF p. 37 has no space.

**A factual correction to the record.** §2 and the dispatch brief said this
leaf has 2 inline and 22 block guards. That is wrong. Running the tool's own
`SYNTHESIS_EDITION_BRANCH_RE` plus its `following == "{}"` test gives
**8 inline, 16 block**. The inline ones are `90-scope.tex` 19, 68, 95, 125,
208 and `99-references.tex` 76, 207, 300. Of the 16 block guards, 14 sit at
block or `\item` boundaries and splice correctly; the 2 that sit inside a
sentence are WEB-001 and WEB-003. The "2" in the earlier count was the subset
of inline guards with non-empty text on both sides. I passed the wrong number
into a dispatch brief; the evaluating agent tested it rather than trusting it
and caught the error.

**Two accepted ids bind this run and are corpus-wide, not leaf defects:**
`WEB-004` (all four `\textperiodcentered` separators dropped from the identity
block, and nested emphasis collapsing the Latin/roman distinction — byte-
identical in all five installed claude propers 51–55 and in the gpt edition,
and the repair would desynchronize the just-accepted PDFs) and `WEB-005`
(no component anchors: `anchor_appointed_elements` keys on `\fulltextheading`,
which exists only under `src/gpt/`; claude leaves use
`\subsection*{N. Introit \cue{Int.}}`). Both are worth a maintainer's decision
independently of any leaf.

**What passed, for context:** the conversion reproduced byte-identically,
exit 0, empty stderr; 30,958 PDF words against 30,990 markdown with the delta
fully accounted for; heading counts 10/41/2 matching exactly with no level
skipped; 5 tables → 5, 69 boxes → 69; colophon identical to the PDF's;
timestamp agreeing across `generation-metadata.tex`, markdown and PDF
`ModDate`; no LaTeX residue anywhere.

**Implication for the fix queue.** The right repair is probably in
`tools/web-edition`, not in the leaf: extend the flush splice to any guard
whose seams fall inside a sentence rather than keying on the `{}` marker, and
strengthen the audit so it catches a fragment opening on a capital. That is a
shared-tool change and would want re-running all 118 eligible editions, as
`d7ef40121` did. Repairing it leaf-side instead (rewriting two guards into the
inline form) would clear leaf 56 and leave the corpus defect standing.
