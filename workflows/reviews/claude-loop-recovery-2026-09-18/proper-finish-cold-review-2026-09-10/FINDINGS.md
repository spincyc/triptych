# Cold review: gate-less transitions, unowned classes, unroutable repairs, contradictory results

Reviewer: fresh reader of `workflows/`, `tools/check-content-preflight`,
`scripts/_workflow.py`, the schemas, and the leaves under `src/`. Read-only
throughout; nothing under `workflows/` was touched.

Eighteen findings, in four families. Everything marked **verified** was
established by reading the files named or by running a read-only script over
the corpus; everything marked **inferred** is a reading of the files that I
could not settle by measurement.

Two constraints governed every proposal below, both taken from `OPERATOR.md`
and the fragments:

- Where a program can decide it, do not spend an evaluator on it — the
  `house-voice` precedent (`OPERATOR.md`, "the two most recent are prose
  screens... a gate loop drains it at no evaluator cost").
- Where it needs judgement, do not put it in a gate — the counting precedent
  (`workflows/fragments/propers/lanes/content-citation-integrity.md`: a
  counting screen "fired eight times and was wrong eight times... Narrowed
  until it stopped being wrong, it judged nothing at all").
- And a screen that refuses most of the corpus is a finding about the corpus.
  Where I propose a screen I say what it does to the fifteen companion-bearing
  leaves in the tree today.

---

## Fix first

| # | Finding | Change | Why first |
|---|---|---|---|
| 1 | **1.1 / 3.1** `content-preflight` reads the companion but cannot repair it, and never reads the companion this run writes | one tool function gains an edition scope; one new gate stage | Demonstrated run-stopper in the tree today (claude/52, claude/53), and it opens the companion to the thirteen checks in the same stroke |
| 2 | **1.3** Four revising stages were never told `generation-metadata.tex` exists | four paragraphs of fragment text, copied from `content-revision.md` step 10 | No schema, pipeline or engine change; arms an *existing* gate against a class already sighted in the tree |
| 3 | **2.6** `synthesis-evaluation` erases `content-evaluation`'s standing record | ~20 lines in `_record_standing_findings` | Verified in the tree; silently defeats the whole of standing-findings schema 3 on every run that succeeds |

---

## Family 1 — missing mechanical screens

### 1.1 The companion edition this run writes passes through no program gate

**What it is.** `content-preflight` is reachable from exactly two stages in
either pipeline — `author-proper` and `content-revision` (`next:
"content-preflight"` on both, in `workflows/pipelines/proper.json` and
`proper-finish.json`). Both of those are forbidden to write the companion
(`author-proper.md` lines 9–16 and step 2; `content-revision.md` step 9,
lines 60–68). The stages that *do* write the companion — `derive-synthesis`
and `synthesis-revision` — run after `content-evaluation` passes, and the
only gate between them and publication is `mechanical-gates`, whose three
checks are `proper-components`, `make doc DOC={proper}` and `make doc
DOC={proper}-synthesis`. So every companion-owned byte written by this run
reaches `synthesis-evaluation`'s two AI lanes without any program having read
it.

This is the same shape as the defect that prompted the review, but it is a
wider surface than References locus clauses: it is all thirteen checks,
including the two prose screens `OPERATOR.md` added at v25 precisely because
a five-lane evaluation could not afford the class.

**The evidence.** Verified:

- `tools/check-content-preflight:1755` `reader_facing()` follows both
  editions' `\input` graph from `EDITIONS = ("main.tex", "synthesis.tex")`
  (line 1751) and therefore *does* read `sections/synthesis/**`. So the tool
  is already edition-blind-but-complete; what is missing is a *place in the
  pipeline* where it runs after the companion is written.
- Running `scripts/_house_voice.house_voice()` over every companion-only file
  in the corpus (18 files across 15 leaves): 2 hits in
  `src/claude/.../52-twelfth-after-pentecost/sections/synthesis/20-integrated-commentary.tex`
  ("This guide has composed, translated, adapted and paraphrased nothing.";
  "…his sentence is this guide's rule…"), 2 in the claude/53 equivalent
  ("The guide prints four."), 0 in the other 16. A further hit sits in
  claude/52's `synthesis.tex` itself.
- So the screen fires on real companion prose and does **not** refuse the
  corpus: 2 of 15 leaves, 5 sites. That is the opposite of `house-voice`'s
  canonical-side profile, which `OPERATOR.md` records as "refuses most leaves
  in the corpus today".

**What it costs.** `synthesis-evaluation` declares `max_iterations: 3` and no
`max_total_iterations` (so a default ceiling of 6) with two lanes at `high`.
A lexically-marked class in companion prose drains that budget one subset at a
time — the exact pathology `OPERATOR.md` records for `house-voice` on the
canonical side ("three successive max-effort evaluations of one leaf spent an
entire iteration budget on that single class"). At worst it publishes: no lane
of `synthesis-evaluation` owns register at all (see 2.1).

**The proposed repair.** A pipeline declaration plus one small tool change.

1. Give the tool an edition scope. `reader_facing(leaf)` and `leaf_tex(leaf)`
   (line 188) take an `edition` argument; a new `--edition
   canonical|synthesis|leaf` flag selects it, defaulting to `leaf` so every
   existing hand invocation is unchanged. Resolving
   `\ifdefined\TriptychSynthesisEdition` for one edition is about thirty lines
   — I wrote a working resolver during this review to measure the References
   class, and the guards in the corpus are all flat (no nesting).
2. Declare a `synthesis-preflight` gate stage in both pipelines between
   `derive-synthesis`/`synthesis-revision` and `synthesis-evaluation`, with
   `pass_transition: "synthesis-evaluation"`, `fail_transition:
   "synthesis-revision"`, `max_iterations: 3`, and the checks that are true of
   a companion: `house-voice`, `structural-meta-labels`, `proposal-fields`,
   `unquoted-not-quoted`, `restricted-not-reproduced`, `references-used`, each
   with `--edition synthesis`. `derive-synthesis.next` and
   `synthesis-revision.next` both become `synthesis-preflight`.

**Confidence.** High that the gap exists (topology; verified). Medium-high on
the payoff. **Falsified by**: the house-voice hits being confined to leaves
that predate the v25 screen and that no future run will re-derive — I did not
establish which leaves are queued for re-production.

### 1.2 Canonical prose can move after `content-evaluation` passes, and nothing re-screens or re-evaluates it

**What it is.** Once `content-evaluation` returns `PASS`, no route re-enters
it (`_clear_failures` at `scripts/_workflow.py:2944`; the topology has no edge
back). `content-preflight` never runs again either. Three later stages may
still write the leaf's `.tex`:

- `synthesis-revision` — for a `seam` finding it edits the shared files
  `sections/20-themes.tex`, `35-source-grounded-synthesis.tex`,
  `50-interpretive.tex`, `90-scope.tex`, `99-references.tex`
  (`synthesis-revision.md` lines 30–53);
- `visual-revision` — "Rewriting dense paragraphs", "Moving headings"
  (`visual-revision.md` lines 16–22);
- `artifact-revision` — "fix the underlying issue" (`artifact-revision.md`
  lines 14–18), unbounded in terms.

The only defence against a canonical regression is a mechanical check asked of
an AI on its honour: `synthesis-revision.md` lines 61–64 — "Rebuild the
canonical edition and compare its `pdftotext` output against the build before
your change: the only line allowed to differ is the revision timestamp."

**The evidence.** Verified from the fragments and the pipeline. Also verified
that the acceptance audit does not close it: `_verify_final_acceptance`
(`scripts/_workflow.py:2615`) requires each evaluator's and gate's *last
recorded* result to be `PASS`, and `content-evaluation`'s last result is a
`PASS` recorded against a document that has since changed.

Corroborating in the tree: in run `05f2d2fd7c2cf8b3` the seam repairs added
guards to five shared files (10, 8, 6, 4, 8 by the fourth round, per the
`derivation-fidelity` observation in
`src/claude/.../55-fifteenth-after-pentecost/evaluations/blocking-findings-v1.toml`)
— thirty-six edits to canonical files after their evaluation closed.

**What it costs.** A wrong publication, silently: `mechanical-gates` measures
that both editions build, `final-acceptance` measures that the PDFs exist and
that generation metadata agrees with the render, and none of them reads prose.

**The proposed repair.** Two parts, and only the first is cheap.

- **Gate:** fold the twelve tree-only preflight checks into the
  `synthesis-preflight` stage of 1.1 with `--edition canonical`, so a seam
  repair that damages canonical prose is refused before the companion is
  judged. This is a pipeline declaration on a stage 1.1 already creates.
- **Engine (optional, larger):** the run already computes what a
  byte-identity check would need. `_document_file_hashes`
  (`scripts/_workflow.py:2726`) hashes every leaf file, and
  `_update_review_scope` (`:2883`) keeps `stage_scope_baseline` per scoping
  stage. A `canonical_frozen: true` declaration on `synthesis-evaluation`
  could refuse a transition where a file outside
  `{synthesis.tex, sections/synthesis/**, proper-components.toml,
  generation-metadata.tex}` moved since `content-evaluation`'s baseline,
  *unless* a forwarded `seam` finding named it. That is precise and it is a
  real engine change; I would do the gate first.

**Confidence.** High on the gap. Medium on the repair — putting prose checks
behind a gate whose `fail_transition` is a reviser with the right mandate is
what makes it work, and `mechanical-gates` (whose reviser is
`artifact-revision`) is the wrong home for them.

### 1.3 The v27 `generation-metadata.tex` instruction was given to three revising stages and withheld from four

**What it is.** `OPERATOR.md` records at v27: "Three revising stages are told
about `generation-metadata.tex`, which only the author had been told existed:
`content-revision`, `derive-synthesis` and `synthesis-revision` bring the
revision timestamp forward and record their contribution, after a companion
derived at 19:06 was found stamped 17:30." The other four revising stages were
not told: `artifact-revision.md`, `visual-revision.md`, `web-revision.md` and
`publication-revision.md` do not mention the file. Two of them are explicitly
authorized to change what the document says — `visual-revision.md` step 2
("Rewriting dense paragraphs", "Restructuring tables", "Moving headings") and
`web-revision.md` step 2 ("the canonical leaf's markup", "the component
anchors").

**The evidence.** Verified in the four fragments and in the tree: the
`profile-conformance` observation in
`src/claude/.../56-sixteenth-after-pentecost/evaluations/blocking-findings-v1.toml`
names exactly this class — "the leaf's ten contribution records … stop one
revision short … No mechanical gate catches it … the reviser is not told to
update because only the author-proper fragment carries the instruction".

Verified in the tool: `tools/check-generation-metadata` `validate_pdf_info`
compares the rendered PDF's ModDate against the source's
`\AIDocumentRevisionTimestamp` and requires exactly one rendered
"Last revised (UTC): <ts>". So the check *cannot* see a source edit that did
not move the timestamp — both sides stay consistent at the stale value.

**What it costs.** Two things. A leaf published with "Last revised (UTC)"
predating its own content — already observed once. And, worse, it disarms the
only check that could have caught 1.2 and 1.4: had the reviser moved the
timestamp, the very next `generation-metadata` gate (at `final-acceptance`, or
at `publication-gates` against the *installed* PDF) would have refused.

**The proposed repair.** Copy `content-revision.md` step 10 into
`artifact-revision.md`, `visual-revision.md`, `web-revision.md` and
`publication-revision.md`, adapted: bring `\AIDocumentRevisionTimestamp`
forward and append an `\AIModelContribution` record whenever this stage
changed a file the document builds from; leave `\AIGenerationProvenance`
alone. Four fragment paragraphs. No schema, pipeline or engine change.

**Confidence.** High. **Falsified by**: a build rule that already stamps the
timestamp from the file mtimes rather than from the source declaration — I did
not read the `make doc` recipe, only `check-generation-metadata`'s comparison.

### 1.4 `web-revision` may edit the canonical leaf after acceptance, with no rebuild, re-gate or re-acceptance

**What it is.** `web-revision.md` step 2 permits the repair to land in "the
canonical leaf's markup" or "the component anchors". `web-revision.next` is
`web-evaluation`. By then `final-acceptance` has passed and
`publish-artifacts` has installed the two PDFs. Nothing rebuilds. Contrast the
sibling stage: `visual-revision.next` is `mechanical-gates`, and its own
fragment gives the reason — "The workflow will re-run mechanical gates and
then re-evaluate visually, because any rebuild can invalidate downstream
gates" (`visual-revision.md` lines 9–11).

**The evidence.** Verified from the two fragments and the two `next`
declarations. Verified that `publication-gates` cannot see it:
`installed-pdf-matches-accepted` is `cmp -s build/... pdf/...` and neither
side moved; `generation-metadata` compares the source's (unmoved) timestamp
against the installed PDF's (unmoved) ModDate.

**What it costs.** A run reaching `ACCEPTED` with a tracked source that no
longer builds the published PDF — the canonical failure this pipeline's whole
acceptance apparatus exists to prevent.

**The proposed repair.** Narrow the permission rather than widen the loop.
`web-revision.md` step 2 should keep `web-edition.toml` and anchors that
render nothing, and send a conversion defect needing leaf markup to the
`BLOCKED` disposition the fragment already names for prose ("a finding against
the accepted canonical prose is the standing case"). With 1.3 applied, an edit
made anyway becomes visible at `publication-gates` instead of silent.

**Confidence.** High that the hole exists; the repair is a judgement call
between narrowing the stage and re-entering the artifact loop.

### 1.5 Four mechanical facts are attested by workers rather than measured

**What it is.** A recurring shape: a fragment asks an agent to perform a
comparison a program could perform, and the run records the agent's word.

| Fragment | The self-attested measurement |
|---|---|
| `synthesis-revision.md` 61–64 | rebuild and `pdftotext`-diff the canonical edition; only the timestamp may differ |
| `brief-revision.md` 57–58 | "Confirm the byte size of `research/scope.md` moved by no more than the sentences you changed, and that no other file in the leaf changed" |
| `resolve-context.md` 21–30 | `test -f` on the generated chronology record |
| `research-synthesis.md` 111, 266 | compare every selected audit entry against the lane finding; do not pass before the `Prior-production carry-forward` heading is present |

**The evidence.** Verified in the fragments. The precedent for treating this
as a defect is `OPERATOR.md` at v13: four site checks "are now gate checks
judged by exit code rather than steps `install-publication` asked a worker to
run and report on… what changed is that no worker's account of a check now
stands between a run and `ACCEPTED`."

**What it costs.** Varies. The `research-synthesis` heading rule is the one
with recorded cost: `OPERATOR.md` v11 — "one re-seed dropped fourteen standing
findings, five recovered by hand and one surviving verbatim into the next
production because nobody carried it."

**The proposed repair.** Only one of these is worth a gate on its own, and it
is the cheapest: a `brief-preflight` gate after `research-synthesis` (in
`proper`) and after `brief-revision` (in `proper-finish`) with a single check
that `research/scope.md` carries the mandated headings —
`Prior-production carry-forward`, `Scriptural chronology audit`,
`Notable-and-quotable audit`, `Interpretive-proposal audit`. That is a `grep`,
it decides nothing about content, and it is the only mechanical screening the
brief gets in either pipeline (no `content-preflight` check reads
`research/scope.md`). The others I would leave: the `pdftotext` diff belongs
with 1.2's engine option, and the chronology `test -f` is close to a tautology
(see Rejected).

**Confidence.** Medium. **Falsified by**: the four headings not being
consistently spelled across the three leaves in the tree — the `CON-PRO-003`
escalation shows the *profile* names the audit's fields two different ways,
which is a warning that heading text may not be stable enough to grep.

---

## Family 2 — unowned classes

### 2.1 The companion's own prose is judged against four criteria; the canonical's against fourteen

**What it is.** This is the general form of both known unowned classes, and of
several others standing in the tree right now. `content-evaluation` carries
fourteen numbered criteria partitioned across five lanes. `synthesis-evaluation`
carries four across two, and all four are *comparative*: does the companion
assert more than the canonical (1); does it carry the canonical's bounds (2);
is it a redistillation rather than a copy (3); does its own build and its own
arithmetic conform (4). Nothing asks whether the companion's *own new prose* —
up to ~950 words per commentary unit, written this run, read by no earlier
stage — is clear, correctly cited, true of the appointed texts, true of its
own contents, or in the house voice. Every canonical criterion is explicitly
withdrawn from the companion: all five content lanes carry the paragraph
"nothing under `sections/synthesis/` is yours at all."

**The evidence.** Verified in the fragments, and verified by four standing
observations in
`src/claude/.../55-fifteenth-after-pentecost/evaluations/blocking-findings-v1.toml`
(run `05f2d2fd7c2cf8b3`, `synthesis-evaluation` iteration 3), each of which
says in terms that no criterion reaches it:

| Sighting | Rounds standing | Lane's own words |
|---|---|---|
| `sections/synthesis/20-integrated-commentary.tex` unit 1: "that vowel" refers to the wrong vowel, inverting the sentence | 4 | "the defect is referential ambiguity in companion-owned prose, not derivation fidelity, evidence state or reuse" |
| Companion cites Augustine at `En. Ps. 85 §2` in unit 3 and `En. Ps. 85.5` three pages earlier | 3 | "my criteria reach whether a statement is true of the companion, not whether a citation aligns" |
| `\pfield{What the element-by-element reading misses}` × 5 in an edition that prints no element-by-element sweep | 4 | "not decidable under any criterion this lane was given" |
| The colophon class (2.2) | 4, two lanes | "no lane is given the colophon's own arithmetic about the edition it describes, or its prose" |

Note the citation case in particular: a wrong section number in the companion
is a `CON-CIT-` defect on the canonical side (criterion 7, "no invented …
attributions") and reaches nobody on the companion side.

**What it costs.** The companion is a published artifact with its own release
record and its own catalog cell (`publication-gates`:
`synthesis-release-record`, `catalog-links`). Its new prose currently receives
about a quarter of the scrutiny the canonical edition's does, and the four
sightings above are all in one leaf of one run.

**The proposed repair.** A fragment change, and the smallest honest one is a
fifth criterion on `synthesis-evaluation.md`, owned by `derivation-fidelity`:

> 5. **The companion's own prose.** The companion's integrated commentary is
>    prose this run wrote and no earlier stage read. On material the companion
>    owns, apply the canonical evaluation's criteria for what prose must be:
>    a citation resolves and agrees with every other statement of it in this
>    edition; a statement about an appointed text is true of the text as
>    `propers/verified.md` prints it; a statement about this edition's own
>    contents is true of the companion's build; and the register is the house
>    voice's. This is not a re-evaluation of the canonical edition and never
>    reaches it.

Plus the mechanical half in 1.1, which takes the lexically-decidable part of
"register" out of the lane's hands entirely.

**Confidence.** High that the classes are unowned — the lanes state it in
their own notes, which is what `OPERATOR.md` asks them to do ("A class of
defect that keeps appearing in `observations` is a fragment that needs to give
some lane the criterion"). Medium on the partition: adding four criteria to a
two-lane stage may want a third lane, and I have not weighed that cost.

### 2.2 (known, confirmed) The `\AIModelContribution` colophon

**What it is.** The three arguments of `\AIModelContribution` render nothing.
`src/common/preamble.tex` lines 88–90:
`\newcommand{\AIModelContribution}[3]{\AIDisplayDocumentRevisionTimestamp}`.
The prose inside them is therefore unreachable by any reader-facing criterion,
and it is also unreachable by any preflight check: `leaf_tex()`
(`tools/check-content-preflight:188`) excludes `generation-metadata.tex` by
name, and `reader_facing()`'s `NOT_PROSE` (line 1752) excludes it too. The one
check that opens the file, `provenance-matches-run`, reads only the five
`\AIGenerationProvenance` fields. `check-generation-metadata` validates the
record's *shape*.

**The evidence.** Verified. Four sightings in run `05f2d2fd7c2cf8b3` across two
lanes (`derivation-fidelity` at iterations 1, 2 and 3; `companion-conformance`
at 2 and 3). The content is not only arithmetic: at iteration 3 the
`companion-conformance` lane records both a miscount ("twenty-one clauses in
the four files both editions input", against thirty-six guards in five files,
counted) and a mangled sentence in the newly appended entry ("The class
SYN-CON-005, SYN-CON-006 and SYN-CON-008 have each named one site of was then
swept rather than decremented"). The lane adds: "neither admitted repair owner
fits: the file is not under `sections/synthesis/` and carries no canonical
sentence made false by the companion's form".

**What it costs.** Four observations from `high`-effort lanes in one run, each
re-derived from scratch (the arithmetic was recounted every round), and a
tracked provenance record that states things about the run that are not so.

**The proposed repair.** Not a criterion — no reader meets this text, and the
caution against adding an AI criterion where a program would do applies. Two
moves, in order of preference:

1. **Stop putting checkable arithmetic in an unchecked container.** Add to
   `author-proper.md`'s `generation-metadata.tex` section (step 5), which
   `content-revision`, `derive-synthesis` and `synthesis-revision` all inherit:
   *An `\AIModelContribution` record states what the stage did, not how many of
   anything it did. It renders nothing, so no reader and no check will ever
   correct a number in it. Name the findings addressed and the files touched;
   do not state totals, page assignments, or counts of sites, guards or
   clauses.* The profile asks for "materially distinct AI contributions"
   (`guidance/liturgy/roman-1962-propers.md` l.365), not a tally.
2. **If a number must stand**, it needs a check, and the check is trivial:
   a fourteenth preflight check `contribution-record-sane` that reads
   `generation-metadata.tex` directly (bypassing `leaf_tex`'s exclusion) and
   refuses a record whose stated count of `\ifdefined\TriptychSynthesisEdition`
   guards, or whose stated brief-synthesis page assignment, disagrees with the
   tree and the `.aux`.

**Confidence.** High on the diagnosis; high that (1) is right and (2) is
optional.

### 2.3 (known, confirmed and split) A published quotation whose exact bytes no tracked record holds

**What it is.** Nothing compares a printed passage's bytes against the bytes
of the record it is bound to. `unquoted-not-quoted` compares the leaf against
itself; `restricted-not-reproduced` reads rights; `bindings-valid` reads the
binding record's schema; criterion 8 asks whether English is *quoted from* a
registered witness; criterion 7 forbids an *invented* quotation. None of them
asks whether the printed words are the record's words.

**The evidence.** Verified: no check in `tools/check-content-preflight` reads
a source record's `text` field. Verified that the comparison is available —
a `passage` record carries it, e.g.
`src/sources/works/eugene-cummiskey/roman-missal-english-laity/editions/philadelphia-1861/passages/post-pentecosten-15--secret.toml`
carries `text = "May thy mysteries, O Lord, preserve us…"` and
`transcription_segments`. And `restricted-not-reproduced` already has the
machinery to pair a printed `\begin{sourcecard}{attribution}` block with the
bound source it names, including the discriminating-anchor logic that refuses
to guess when two bound sources share a word.

**The class splits, and the two halves want different instruments.**

- **Bound half — mechanical.** A printed passage attributed to a source the
  leaf binds, whose bound record is a `passage` with a `text` field, is a byte
  comparison. This is a preflight check, not a criterion.
- **Unbound half — judgement.** A patristic quotation whose only warrant is a
  research lane's retrieval, held in `research/scope.md` as prose, cannot be
  compared mechanically. Criterion 7 reaches "invented" and does not reach
  "misquoted".

**The proposed repair.**

1. `tools/check-content-preflight` gains `quoted-text-matches-record`, modelled
   on `check_restricted_not_reproduced`: for each `attributed_blocks(leaf)`
   entry whose attribution discriminates a single bound `passage` record,
   normalise whitespace and LaTeX accents and compare against that record's
   `text`; report a mismatch with both strings. Declared in
   `content-preflight.checks` in both pipelines.
2. `content-citation-integrity.md` criterion 7 gains one clause: *a quotation
   whose exact wording no tracked passage record and no sentence of the brief
   holds is this criterion's defect, and it is `research` when the witness was
   never read and `authoring` when the brief holds the wording and the leaf
   departs from it.*

**Confidence.** Medium-high on the mechanical half; the check must be measured
against the corpus before it is declared. **Falsified by**: printed passages
routinely being composites or elisions of the record's `text` (an incipit, a
bracketed omission), in which case the check refuses correct leaves and the
caution applies. I did not run that measurement.

### 2.4 A work-wide bound duplicated between the terminal apparatus and the body — unowned, and grown by its own repair

**What it is.** The profile confines work-wide bounds and qualifications to
the terminal apparatus (`guidance/liturgy/roman-1962-propers.md` l.279, l.359
"Do not duplicate this apparatus earlier or inside References", l.382).
Criterion 1 requires that a claim carry the same bound wherever it recurs.
Discharging a criterion 1 finding therefore *creates* the duplication, and no
lane owns the duplication.

**The evidence.** Verified in the tree. The `profile-conformance` observation
in `src/claude/.../56-sixteenth-after-pentecost/evaluations/blocking-findings-v1.toml`
states it exactly, with counts: raised "at iteration 0 of this run and at five
consecutive iterations of the prior production, and the two revisions since
have enlarged it rather than reduced it — CON-EVI-024's repair at iteration 2
put the Sarum optical-layer bound into the body of C1 as well as into the
appendix and References, which is the third bound to travel that way… no lane
in this stage owns 'a work-wide bound duplicated between the terminal
apparatus and the body'." It also names the discrimination the repair must
settle: "the profile also permits a limit that materially changes a claim to
stand beside that claim, so the widened criterion would have to say which of
these five is claim-local and which is work-wide; that judgement is exactly
what no lane is currently asked to make."

**What it costs.** A class that grows monotonically under the repair loop, and
five sites in one leaf. It is also a Family 4 generator (see 4.2).

**The proposed repair.** Fragment, two files, and it must be one change, not
two. In `content-evaluation.md`, criterion 1 gains the discrimination — a
*claim-local* bound (one that changes the truth of this claim) stands beside
the claim wherever the claim recurs; a *work-wide* bound (one that qualifies
the guide's whole sweep) stands once in the terminal apparatus and is pointed
at. In `content-profile-conformance.md`, criterion 10 widens from "the source
records exist and follow the profile's format" to include the profile's own
non-duplication rule, so the second half has an owner. Neither is a program
check: telling a claim-local bound from a work-wide one is precisely the
judgement `OPERATOR.md` reserves for a lane.

**Confidence.** High that the class is unowned. Medium on the wording — the
lane itself says the discrimination is hard.

### 2.5 `research-synthesis` can record neither an observation nor an escalation

**What it is.** `workflows/schema/research-synthesis-result.json` restricts
`severity` to `["blocking", "advisory"]`, defines no `observation_fields`, and
defines no `escalation_finding_fields`. `_validate_result`
(`scripts/_workflow.py:4730`) refuses observations from a stage whose schema
does not define them. So the one stage that reads all seven lanes' joined
findings, and the sole writer of the brief, has no way to say "I saw something
real that my criteria do not reach" or "this defect is in an artifact no stage
of this run may write".

**The evidence.** Verified in the schema and in the validator. The v18 history
is what this would have caught: a `source-citation-coverage` demand that
reached the author as a bar it was forbidden to clear, and `research-synthesis`
sat between them with nothing to say. `OPERATOR.md` says of `research` lanes
that they have no observations by design — that reasoning is about a
read-only lane that judges nothing, and does not transfer to the integrator,
which `OPERATOR.md` itself calls "an evaluator too".

**What it costs.** Inferred, not measured: an integrator's sighting dies in
its `summary`, which lives under `build/` and is deleted by `make clean`.

**The proposed repair.** Schema change, four lines: add `observations` to
`optional_fields`, `observation_fields = ["location", "note"]`, `escalation`
to the severity enum, and `escalation_finding_fields = ["escalated_to"]` in
`workflows/schema/research-synthesis-result.json`. The engine already handles
both generically — `_record_escalations` (`:2451`) keys off severity alone.

**Confidence.** High on the fact, medium on the payoff.

### 2.6 Two stages own one tracked record, and the second erases the first's non-blocking content

**What it is.** Both `content-evaluation` and `synthesis-evaluation` declare
`records_standing_findings: true` in both pipelines. `_record_standing_findings`
(`scripts/_workflow.py:2959`) rewrites
`<document_root>/evaluations/blocking-findings-v1.toml` *whole*, from the
single `result` it is handed. `synthesis-evaluation` always runs after
`content-evaluation` has passed. So on every run that reaches
`derive-synthesis` — that is, every run that succeeds — the content
evaluation's observations, accepted findings and advisories are deleted from
the tracked record and replaced by the synthesis evaluation's.

Only escalations survive, and only because they are written from
`state["escalations"]`, the whole-run ledger, rather than from the result.

**The evidence.** Verified in the engine and verified in the tree.
`src/claude/.../55-fifteenth-after-pentecost/evaluations/blocking-findings-v1.toml`
now reads `stage = "synthesis-evaluation"`, and carries seven observations,
all from `derivation-fidelity` and `companion-conformance`, plus two
`content-evaluation` escalations. No content-lane observation is present. For
contrast, the three leaves whose last recorded stage is `content-evaluation`
(claude/54, claude/56, all `proper-finish` v4) carry content-lane observations
and nothing else.

This is the identical failure `OPERATOR.md` records at v25 and gives as the
reason the declaration is per stage — "every evaluator used to write this
path: a `web-evaluation` asking for changes replaced the leaf's content
findings with findings about generated HTML" — recreated by giving a second
stage the declaration in v26/v28.

**What it costs.** The whole purpose of standing-findings schema 3, as the
engine's own comment states it, for every content-evaluation verdict in every
successful run: "a verdict that dies with the run is met again by the next cold
read as though nobody had ever weighed it, and weighed again — which is how a
document in good shape spends a whole iteration budget." It also breaks the id
recovery `content-evaluation.md` instructs the next production's lanes to
perform ("Read it, and where you find a defect it already names, keep that
id"): the next production's lanes will read a file containing `SYN-` ids.

**The proposed repair.** Engine, ~20 lines in `_record_standing_findings`.
Read the existing file first; merge by `(stage, id)` for findings, accepted
and advisories, and by `(stage, location, note)` for observations, exactly as
the escalation ledger already merges; replace only the entries this stage
raised, keep entries recorded by other stages of this run, and carry the
per-stage header block into a `[[evaluations]]` array so the file states which
stage last spoke for each. The alternative — one record path per stage — is
simpler but scatters what is meant to be one record for a person.

**Confidence.** High (verified both sides).

### 2.7 Two fragments contradict the engine and each other about that record

**What it is.** Two small, exact fragment defects, both about the same file.

- `content-evaluation.md` line 532 tells a lane the record holds "blocking
  findings, observations and escalations and no advisory", and therefore to
  mint a fresh id when restating an advisory. Since schema 3 the engine writes
  `[[advisories]]` and `[[accepted]]` (`_record_standing_findings`, and
  `result-format.md` lines 264–270 says so). Minting a fresh id for an
  advisory the record already names is exactly the id churn the record exists
  to stop, and it is what `_check_accepted_not_reraised` and the
  no-promotion rule depend on being able to see.
- `result-format.md` lines 264–267 tells *every* evaluator lane that an
  accepted finding "is written to `<document_root>/evaluations/…` under
  `[[accepted]]`". For `visual-evaluation` and `web-evaluation` this is false:
  neither declares `records_standing_findings`, and no stage that does runs
  after them, so their accepted verdicts, advisories and observations die
  under `build/`. The observations paragraph at lines 379–382 hedges
  correctly; the accepted paragraph does not.

**The evidence.** Verified against `_record_standing_findings` and the two
pipelines' stage flags.

**What it costs.** Small but real: a lane acting on either sentence records a
judgement in a place it is not recorded, or renumbers a defect the record
already names.

**The proposed repair.** Fragment text. Change `content-evaluation.md` line
532 to name all four collections. Hedge `result-format.md` line 264 the way
line 379 is hedged, or give `visual-evaluation` and `web-evaluation` their own
record path (which is 2.6's alternative, and would fix both).

**Confidence.** High.

---

## Family 3 — repair owners that do not exist

### 3.1 `content-preflight` reads the companion and routes its failures to a reviser forbidden to repair it

**What it is.** `reader_facing()` (`tools/check-content-preflight:1755`)
deliberately follows both editions, so `house-voice`, `proposal-fields` and
the other prose screens read `sections/synthesis/**` and `synthesis.tex`.
`content-preflight.fail_transition` is `content-revision`, and
`content-revision.md` step 9 forbids that stage to touch any of those files.
The reviser's only honest answer is `not-repaired`. And a gate keeps the id
comparison whatever the reviser says — `_failure_budget_spent`
(`scripts/_workflow.py:3237`): `reported = stage_id in unrepaired_map and
stage["type"] != GATE`. The same check id refuses again, `stage_repeats`
climbs, and at `max_iterations: 3` the run is `BLOCKED`.

**The evidence.** Verified mechanically. Running the screen over the corpus:
`src/claude/.../52-twelfth-after-pentecost` carries 2 house-voice hits in
`sections/synthesis/20-integrated-commentary.tex` and 1 in `synthesis.tex`;
`src/claude/.../53-thirteenth-after-pentecost` carries 2 in its companion
commentary. Both leaves have canonical-side hits too (9 and 17), which
`content-revision` *can* clear; the companion-side ones it cannot. A
`proper-finish` run over either leaf today fails `house-voice` three times and
blocks.

**What it costs.** A stopped run on a leaf whose defect is real, whose repair
is a sentence, and which the pipeline forbids the only reviser in that loop to
make.

**The proposed repair.** The edition scope of 1.1, used the other way:
`content-preflight` runs the prose screens with `--edition canonical`, so the
gate in front of the canonical loop judges only what that loop owns, and the
new `synthesis-preflight` gate (whose reviser is `synthesis-revision`) judges
the companion. This is the same separation v26 made for the evaluators, applied
to the gate that was left edition-blind.

**Confidence.** High. **Falsified by**: `tools/tpt check-content-preflight`
being a wrapper that scopes files differently from the module I invoked
directly — I called `_house_voice.house_voice()` on each file rather than
running the gate command, deliberately, to stay read-only.

### 3.2 The publication phase has no escalation channel at all

**What it is.** `escalation` severity, and the `escalated_to` field it
requires, exist only in `content-evaluation-result.json`,
`content-evaluation-finish-result.json` and `synthesis-evaluation-result.json`.
`evaluator-result.json` (used by `visual-evaluation` and `web-evaluation`)
declares no `finding_enums` and no `escalation_finding_fields`;
`gate-result.json` has no severities beyond what `_run_gate` mints;
`worker-result.json` has no `findings` at all. And even if a `visual-evaluation`
lane smuggled an escalation past the permissive validator, no stage declaring
`records_standing_findings` runs after `synthesis-evaluation`, so the ledger
would never reach the tree.

**The evidence.** Verified in the five schemas and in `_validate_result`.
The concrete instances are named by the fragments themselves:

- `install-publication.md` lines 68–70: "**Do not write the row itself.** …
  If this identity has no row, return `BLOCKED` naming the missing row rather
  than inventing one" — a maintainer decision, recorded only in a worker's
  `summary` under `build/tpt-runs/`, which `.gitignore` line 1 covers and
  `wt tidy` deletes.
- `publication-revision.md` lines 49–53: three more standing cases — a finding
  answerable only by regenerating the web edition, a missing catalog row, a
  withdrawn authorization — all `BLOCKED`, none reaching a person durably.

Contrast `OPERATOR.md` v11, which created the escalation severity for exactly
this: "`profile-conformance` found a genuine contradiction in the propers
profile's macro-order and could only file it advisory, where it was restated
every iteration and acted on in none."

**What it costs.** A run that is complete and correct ends `BLOCKED`, and the
one sentence a maintainer needs — *this identity has no catalog row* — lives
in an untracked directory that routine cleanup deletes. `_escalation_note`
(`scripts/_workflow.py:4408`) exists to put exactly that in the terminal
message, and no publication-phase stage can populate it.

**The proposed repair.** Three parts, smallest first.

1. Add `escalation` + `escalated_to` and `accepted` + `accepted_because` to
   `evaluator-result.json` (or split `visual-evaluation` and `web-evaluation`
   onto their own schemas), so the two late evaluators can escalate.
2. Give `worker-result.json` an optional `escalations` list with the same
   shape, and have `_record_escalations` read it — a worker that must `BLOCK`
   for a maintainer's decision then says so in the ledger rather than in prose.
3. Write the escalation ledger to the tree on any terminal transition, not
   only from a `records_standing_findings` stage. The engine already writes
   the whole ledger; what it lacks is a late stage that triggers the write.

**Confidence.** High on the gap. The repair is a design choice and (3) is the
one that actually closes it.

### 3.3 (known, re-characterised) The `propers/` orthography defect — and why `escalation` does not cover it

**What it is.** A `proper-finish` evaluation lane observed that an orthography
defect inside the leaf's `propers/` provenance records has no nameable owner,
since that pipeline admits only `brief` and `authoring`. The known statement of
the gap is not quite right, and the correction matters for the repair.

`propers/verified.md` *is* writable by a stage of the pipeline:
`author-proper.md` step 7 owns it, and `content-revision`'s packet carries
`author-proper.md` in full and step 8 says "Follow the same authoring rules as
the author-proper stage". So `authoring` is a true owner — while the content
loop is still open. The defect is unroutable only when it is found *after* that
loop closes: `synthesis-evaluation` admits `derivation` and `seam`, and no edge
returns from it to `content-revision`.

**Does `escalation` cover it?** No, and it cannot, because the fragments define
escalation by the wrong test. `content-evaluation.md`: "Escalation is for a
defect in an artifact **no stage of this workflow may write**". A stage of this
workflow *can* write `propers/verified.md`; it just will not run again. A lane
following the rule as written is forbidden to escalate, and `synthesis-evaluation.md`
tells it the same ("A defect that is equally true of the canonical edition… is
neither"). The record shows lanes doing the only thing left: an observation,
which routes nothing.

**The evidence.** Verified in the fragments and the pipeline topology.
Corroborating: the `CON-CIT-003` escalation standing in the claude/55 record is
about `src/sources/`, which genuinely no stage may write — the test works there
and only there.

**What it costs.** A real defect in a tracked provenance record, found at
maximum-effort cost, reaching neither a reviser nor a maintainer's ledger.

**The proposed repair.** Fragment, one sentence, in both
`content-evaluation.md` ("When no stage owns the repair") and
`synthesis-evaluation.md` ("Repair ownership"). Widen the test from *no stage
of this workflow may write it* to *no stage that will still run may write it*:

> The test is whether an owner will still run. An artifact no stage of this
> workflow may write — repository guidance, `src/sources/`, `tools/`,
> `workflows/` — is the standing case. So is an artifact this pipeline owns
> whose owner is behind you: once the canonical content loop has passed, no
> route re-enters it, and a defect in the canonical leaf or its provenance
> records found afterwards has no owner in this run however clearly it has one
> in the pipeline. Escalate it, naming the file and the stage that owns it.

That makes the existing ledger correct rather than adding machinery, and it is
the honest description of a sequenced pipeline.

**Confidence.** High on the analysis. The alternative repair — a third
`synthesis-evaluation` owner routing back into the canonical loop — is exactly
what v26 removed to make the sequence converge, and I would not propose it.

### 3.4 `publication-gates` bundles checks whose repairer is not `install-publication`

**What it is.** `publication-gates` runs twenty-one checks with a single
`fail_transition: "publication-revision"`, whose `revision_target` is
`install-publication` and whose fragment forbids regenerating the web edition
or touching the leaf (`publication-revision.md` lines 18–26). Several of the
checks are not about wiring: `web-edition-valid` (`check-web-edition` on the
leaf's own declaration), `site-web-editions-current` (which regenerates every
eligible edition and `cmp`s it against the tracked file — verified in the
`Makefile` recipe), and the three whole-repository site checks. Their true
repairer is `generate-web`/`web-revision`, or the maintainer, or another
publication entirely.

**The evidence.** Verified in the check list and the two fragments. The
fragment names the consequence itself: "Return `disposition: "BLOCKED"` …
The standing cases are a finding that can only be answered by regenerating the
web edition, which would bypass the evaluation that accepted it."

**What it costs.** A stopped run at the last gate, on a defect whose owner
exists two stages upstream.

**The proposed repair.** Either a second repair route on the gate — but
`_validate_repair_routes` (`scripts/_workflow.py:4641`) refuses `repair_routes`
on anything but an evaluator, so this is an engine change — or split the gate:
a `web-gate` after `web-evaluation` carrying `web-edition-valid`,
`no-synthesis-web-edition` and `web-edition-declared`, with `fail_transition:
"web-revision"`, leaving `publication-gates` the wiring checks it can route.
The split is the smaller change and needs no engine work.

**Confidence.** Medium-high. **Falsified by**: those checks being provably
impossible to fail at `publication-gates` given that `generate-web` already
ran them — `generate-web.md` steps 2–3 do run `check-web-edition`, so
`web-edition-valid` really may be belt-and-braces. `site-web-editions-current`
is not: it depends on the leaf not having moved, which 1.4 permits.

---

## Family 4 — contradictory required results

### 4.1 `seam` is a structurally perpetual route loser: its findings are carried, never reported, and never charge the budget

**What it is.** `synthesis-evaluation.repair_routes` declares `derivation`
first and `seam` second, and both transition to `synthesis-revision`.
`_repair_route` (`scripts/_workflow.py:4612`) takes declaration order, so any
round carrying at least one `derivation` finding routes by `derivation`.
`_extract_prior_findings` (`:3515`) then keeps *only* the findings naming the
winning target; the `seam` findings arrive at the same stage, in the same
packet, under `CARRIED_FINDINGS`. And `result-format.md` lines 95–98:
"**`CARRIED_FINDINGS` is not part of this report.**" `_record_repair_outcomes`
(`:3153`) holds the reviser only to `findings_forwarded_ids`.

Consequences, all verified in the code:

- A `seam` finding can never be reported `not-repaired` — naming it in
  `finding_dispositions` is refused as "a finding the engine did not forward".
- `_failure_budget_spent` sets `reported = True` (the derivation report
  exists), so `looping = unrepaired`, which contains only derivation ids. A
  `seam` id repeating round after round charges `stage_repeats` nothing.
- `_carried_findings` (`:3593`) marks a target `answered` once any stage
  declaring that target in `repairs` has run since. `synthesis-revision` is the
  only owner of `seam`, so a seam finding is delivered exactly once and never
  re-carried; the next evaluation must rediscover it from cold.

**The evidence.** Verified in the engine. Corroborated in the tree: the
`derivation-fidelity` observation in the claude/55 record quotes the reviser's
own colophon entry as "naming four blocking derivation findings and five
carried seam findings", and the SYN-CON class ran 005 → 006 → 008 → 009 across
four rounds.

**What it costs.** The honest `not-repaired` channel that v25 built, and that
`OPERATOR.md` calls "the only way the engine learns that the stage has stopped
converging", is closed for exactly the class v28 created the `seam` owner for.
The `da04e65ca4ec963b` failure — "twenty-four dangling locators were reported
unrepaired in one round" — could not be reported at all under v6 in a mixed
round. The run then terminates on `max_novel_iterations` or the ceiling, and
the message describes the wrong thing.

**The proposed repair.** Engine, four lines. In `_extract_prior_findings`,
forward every blocking finding whose owner's declared route transitions to the
*same stage* as the winning route, not only those naming the winning target:

```python
route = _repair_route(stage, result)
if route is not None:
    same = {r[REPAIR_TARGET] for r in stage.get(REPAIR_ROUTES, [])
            if r["transition"] == route["transition"]}
    forwarded = [f for f in forwarded if f.get(REPAIR_TARGET) in same]
```

Nothing about routing changes; the reviser receives the same findings it
receives today, in one list instead of two, and now owes an account of each.
`_carried_findings` already skips anything in `forwarded`.

**Confidence.** High on the mechanism (read directly from the code and
corroborated by the run). Medium on how much it costs in practice — I have one
run's worth of evidence.

### 4.2 The partition itself generates contradictory pairs: one lane owns *less*, another owns *true of what is there*

**What it is.** The observed instance — a derivation finding removing material
from a unit in the same round that a conformance finding directed a pointer at
that unit — is not an accident of one round. It is the standing shape of every
place two lanes are partitioned across the same sentence, one asking for
reduction and the other for accuracy about what remains. Four instances, all
verified in the fragments:

| Pair | The collision |
|---|---|
| `synthesis-fidelity` crit. 3 (redistillation, remove reuse) vs `synthesis-conformance` crit. 4 (every statement about the other edition true of the companion) | remove the unit / make the pointer to it resolve — the observed instance |
| `content-synthesis-argument` crit. 4 (one fullest home; "remove repeated quotations, recaps") vs `content-evidence-discipline` crit. 1 (same bound wherever a claim recurs) and `author-proper.md`'s "A restatement inherits the evidence state of what it restates" | delete the restatement / qualify it |
| `content-synthesis-argument` crit. 4 vs `content-citation-integrity` crit. 7 (stated counts) | removing a recap falsifies a count that heads it elsewhere |
| `visual-density-and-hierarchy` crit. 1 ("too dense") vs `visual-page-rhythm` crit. 7 ("nearly empty") vs `visual-fixed-pagination` crit. 8 (fixed pages must stay legible), over a profile that fixes pages 1, 2 and 3–4 | add air / remove spill / do neither on the fixed pages |

The system already knows the shape exists: `content-evaluation.md` criterion 12
carries a hand-written warning that "a criterion 12 repair which removes such a
bound… trades this criterion's defect for criteria 1 and 2's", and
`OPERATOR.md` v26 records the cost — "that oscillation cost that run three
regressions, the last of which stopped it". The warning is per-pair prose in
one criterion, and it does not generalise to the other four.

Two structural aggravations:

- `visual-evaluation` declares no `repair_routes` at all, so nothing orders its
  four lanes' findings; `visual-revision` receives them as one undifferentiated
  list.
- 2.4's case is worse than a collision: it is a *ratchet*. Clearing the
  criterion 1 finding enlarges the criterion 10 defect, round after round, and
  nobody owns the second half.

**The evidence.** Verified in the fragments and the pipeline. The observed
instance and the criterion 12 case are recorded; the other three are inferred
from reading the criteria against each other, and I did not find a run in the
tree that exhibits them.

**What it costs.** A reviser handed two `required_result` fields it cannot both
satisfy either picks one and reports the other `repaired` (which is the
optimistic report the whole budget design fears), or reports one
`not-repaired` with a note nobody reads as a conflict. Either way the next
round re-raises, and the collision is invisible to every counter.

**The proposed repair.** Not a fifth per-pair warning. One paragraph in
`common/result-format.md`, under the `finding_dispositions` contract, that
makes the collision *visible* rather than trying to prevent it:

> **Two findings you cannot both satisfy.** Where two forwarded blocking
> findings name the same passage and their `required_result` fields cannot both
> be met — one asks you to remove material another asks you to point at, one
> asks for a bound another asks you to move — do not choose silently. Repair
> the one whose criterion is categorical, and report the other `not-repaired`
> with the conflicting id and both `required_result` fields in the note. That
> is not a failure of yours: it is the only record that two criteria met at one
> sentence, and it is what tells the run that the partition, and not the
> document, is what needs the repair.

This costs nothing, uses machinery that exists, converts a silent oscillation
into a budgeted `not-repaired`, and puts the evidence for a fragment repair in
the standing record. A stricter option — refusing at join time any
`CHANGES_REQUIRED` whose blocking findings name the same `location` from two
lanes without a `conflicts_with` field — is precise but adds a field and would
misfire on two genuinely independent defects in one file. I would not do it.

**Confidence.** Medium-high that the shapes are real, high that the reporting
change is safe and cheap, low that the stricter engine option is worth it.

---

## Considered and rejected

**Per-edition `references-used` as the mechanical screen for the SYN-CON
class.** I built the edition resolver and ran a per-edition `references-used`
over all fifteen companion-bearing leaves: **0 dangling entries, in either
edition, in every leaf.** The class is a *locus clause inside* an entry
("…and at the eight loci of Ps. 94:3"), not an unused entry, and
`anchors()`/`COMMON` matching is far too permissive to see it — the Hesbert
entry counts as "used" because the word Hesbert appears in a section both
editions render. Rejected: it would have caught none of SYN-CON-005/006/008/009.

The screen that *would* catch them is a lexical one on the `house-voice`
pattern — over the synthesis-resolved text, refuse a sentence naming apparatus
the profile forbids the companion ("element-by-element", "element
subsections", "the appointed-text section", "the Gospel subsection") — and
that is the named defect's own repair, so it is out of scope here. I note it
only because it belongs in the `synthesis-preflight` gate of 1.1 if that gate
is built.

**A gate check for stated counts.** `content-citation-integrity.md` records
that this was tried: "It fired eight times and was wrong eight times…
Narrowed until it stopped being wrong, it judged nothing at all." Rejected on
the fragment's own measured evidence.

**A `chronology-record-current` gate after `resolve-context`.** Attractive on
the v20 history, and I verified it would run on a leaf that has only
`research/` (`_chronology_scope` returns `required = True` as soon as the
record is carried). But `resolve-context` *generates* the record by running
`tools/tpt proper-chronology record --write`, so a check that regenerates and
compares is near-tautological at that point; the v20 failure was the record's
*absence*, which the fragment's `test -f` now covers. Residual value is only
that a gate is a measurement where `test -f` is a worker's word. Low priority;
not proposed.

**`installed-web-edition-matches-evaluated`** (a `cmp -s build/web/... web/...`
beside `installed-pdf-matches-accepted`). Rejected as largely redundant:
`make check-web-editions-current` regenerates every eligible edition and
`cmp`s it against the tracked file, verified in the `Makefile` recipe. The hole
it leaves is that it compares against *current* sources, so a leaf edit made by
`web-revision` is invisible — which is finding 1.4, and better fixed there.

**A `canonical-render-unchanged` gate check across the synthesis loop.** The
right idea, and I could not find a baseline the gate could read: gate commands
are shell invocations with `{run.*}` substitution and no access to run state.
The engine has what is needed (`_document_file_hashes`,
`stage_scope_baseline`), so this belongs as the engine option in 1.2, not as a
gate check.

**Adding a `repair_target` for the colophon class.** Rejected: the right answer
is to stop writing checkable arithmetic into a container that renders nothing
(2.2), not to give an unreadable record a repair owner.

**A third lane on `synthesis-evaluation`.** Considered as the repair for 2.1
and set aside in favour of a fifth criterion on the existing
`derivation-fidelity` lane, because a two-lane stage at `high` effort is
already cheap and I have no evidence that the added criteria need their own
reader. Flagged as the alternative if the criteria turn out to crowd the lane.

---

## Where the evidence was too thin to judge

- **How much 1.1 actually pays.** Two of fifteen companion files carry
  house-voice hits, and both leaves predate the v25 screen. Whether a *fresh*
  `derive-synthesis` writes companion prose that trips the screen is not
  something two pre-screen leaves can tell me. The gap is certain; the yield
  is not.
- **Whether `quoted-text-matches-record` (2.3) refuses the corpus.** The check
  is clearly implementable and clearly mechanical. Whether printed passages in
  this corpus are byte-faithful to their `passage` records — as against
  elisions, incipits, bracketed omissions and typographic normalisation — I did
  not measure, and `OPERATOR.md`'s caution about `house-voice` says that
  measurement decides whether the check is worth adding.
- **The three inferred collisions in 4.2.** The observed instance and the
  criterion 12 case are on the record. The synthesis-vs-bound, count-vs-recap
  and density-vs-rhythm pairs I read out of the criteria; no run in the tree
  exhibits them, and three of the six standing-findings records predate the
  fragments that would generate them.
- **Whether the `proper` pipeline exhibits 3.1 at all.** In `proper` the leaf
  is authored from scratch, so `sections/synthesis/**` may not exist when
  `content-preflight` runs, and the unroutable-gate-failure case may be
  specific to `proper-finish` over a leaf that already carries a companion.
  Every leaf in the tree carries one, so the case is live for `proper-finish`;
  I could not establish it for `proper`.
- **The `make doc` stamping rule** behind 1.3. I read
  `check-generation-metadata`'s comparison, not the recipe that produces the
  PDF's ModDate. If the build stamps from mtime rather than from
  `\AIDocumentRevisionTimestamp`, 1.3's second-order benefit (arming an
  existing gate against 1.2 and 1.4) does not hold, though the first-order
  defect — a published leaf whose stated revision predates its content — still
  does.
- **The `interventions/` debt ledger.** `OPERATOR.md` describes it and
  `tpt debt`; no run directory survives in the tree for me to read, so I could
  not tell whether any of these classes has already been recorded there as
  unencoded debt.
