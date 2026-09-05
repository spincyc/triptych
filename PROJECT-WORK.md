# Project Work Register

This is Triptych's provider-neutral operational memory. Read it together with
`promised-deliverables.toml` before starting or resuming work, after a context
handoff, and before reporting completion. “Published,” “built,” “committed,”
“pushed,” “review copy,” and “complete” are different states.

Last reconciled: 2026-09-05.

## GPT Sixteenth Sunday after Pentecost workflow, 2026-09-05

<!-- promised-deliverable: gpt-sixteenth-after-pentecost-workflow-2026-09-05 -->

The maintainer requested execution of the prescribed `proper` v25 workflow
for provider `gpt`, identity
`liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost`,
through its `ACCEPTED` or `BLOCKED` disposition. The workflow's own packets
govern stage order, worker count, reasoning effort, findings and acceptance.
This request opens this provider and identity alone; the dated authorization
is recorded in `guidance/liturgy/propers-production-plan.md`.

**In progress.** The registered-identity, provider and scope checks passed.
The target had no publication leaf when work began. Its appointed formulary
is `pentecost-16`; the generated and checked chronology record is now at
`src/gpt/liturgy/roman-rite/1962/propers/temporal/56-sixteenth-after-pentecost/research/chronology.toml`.
The source-audit stage passed: `propers/verified.md` records all ten elements
collated against the CMAA 1962 pages, the page-checked 1862 Latin antecedent,
and exact Challoner and Cummiskey English controls; `propers/retrieved.txt`
preserves the uncorrected finding-aid extract. Source-library validation
passed. A successful `make -j4 install-all` restored the existing installed
PDF tree required by checks in a fresh clone. The broader promised-deliverable
check now passes. Regenerating the document catalogue reconciled two rebuilt
page counts and the Claude Fourteenth Sunday after Pentecost PDFs previously
marked absent.

The seven research lanes completed their sweeps, and the engine accepted their
108 joined findings in declared lane order. Research synthesis passed and
the complete `research/scope.md` now preserves those findings, five integrated
claims, six precedent-covered proposals, five cultural entries, the immutable
chronology audit and every reader-facing section's evidence position.
Source registration passed over its outputs: 79 receipts resolved to 71
distinct artifacts, with 60 new records, 11 already held, and one additional
government-page derivative. The 38 retained payloads total 96,539,390 bytes;
protected witnesses retain their identities and rights records without their
payloads. The source-reader projection is current. The source-family catalogue
checkpoint was reconciled while preserving all prior pending review units.

The authored leaf now has the real `main.tex` owner, the full and synthesis
branches, all ten received text pairs, the component manifest and 54 source
bindings. The authoring reuse audit records exact Latin and English agreement
with the accepted controls. The current builds contain 20 full-edition pages
and 14 synthesis-edition pages. The prescribed authoring stage passed, including
focused preflight, run provenance, component pagination and web eligibility.
The workflow's program content-preflight gate passed. Its first content
evaluation joined all five lane results and required changes. The engine's
standing findings are `CON-EVI-001`, `CON-SYN-001`, `CON-CIT-001a`,
`CON-CIT-001b`, `CON-CIT-002a` and `CON-CIT-002b`. It routed the two
research-owned citation findings to research iteration 1 and carried the four
authoring findings forward. The complete findings are preserved unchanged in
the leaf's engine-written `evaluations/blocking-findings-v1.toml`. All seven
fresh research lanes completed their second full sweeps at the packet-specified
efforts. The engine joined 116 findings and accepted research synthesis
iteration 1. The revised brief preserves that complete evidence set and all
fourteen chronology assertions, supplies the missing Gerard and Anthony
citation bundles, and carries all six standing findings. Source registration
iteration 1 is in progress. The standing findings remain open until the
workflow's subsequent evaluation accepts their repairs.

The full `make check-sources` check now **passes**. The documented inventory
refresh added the target's actual source surface and reconciled the two
inherited stale hashes for the GPT altar-server format and sanctuary artwork
manifest. An actual source-record review classified the new publication's
eleven broad source strata. The inventory covers 140 GPT publications and
2,118 source-surface files; the family ledger retains 151 explicitly pending
review units, without claiming family screening or atomic citation coverage.
The generated document catalogue now records both new editions as not
installed. No placeholder publication owner or checker change was needed.

Passing content evaluation, review of both PDFs, the canonical web edition
and release records remain outstanding. No guide has
been installed or accepted. Reconcile this entry to the engine's terminal
disposition and preserve any unresolved findings before reporting the
workflow finished; a `BLOCKED` run does not establish publication acceptance.

## The 1962 Latin backfill, 2026-09-03/04

The 1962 calendar published three Latin oration bodies on the morning of
2026-09-03 and 1,034 by the end of 2026-09-04. Every composed oration in it has
now been decided one way or the other. What follows is the state, the rules that
produced it, and what is left.

### Why it had been stuck

522 elements carried `text_status.state = unavailable` with a `rights-withheld`
reason naming the 1962 Vatican typical edition, 220 of them seasonal. That was
never a rights finding. `missale-romanum-1962-facsimile-rights-v1.toml`, recorded
2026-08-01, already held that the Latin travels on 17 U.S.C. 103(b) plus a
public-domain witness and names the seasonal orations as preexisting material.
The rows recorded that nobody had run the collation.

Two further causes emerged as the work went on, and both were mechanical rather
than legal. Most `witness-gap` rows had been typed against the CMAA FACSIMILE
ITSELF — an earlier pass could not get a readable target out of a layer that
wrecks ornamental initials and welds marginal numbers to words. And
`pdftotext -layout` interleaves the two columns of both PDF witnesses, so every
absence reached over it was worthless.

### The state

| | published | rights-withheld | witness-gap | scripture, citation only |
| --- | --- | --- | --- | --- |
| roman-1962 | 1,034 | 77 | 84 | 2,176 |
| postconciliar | 0 | 326 | 1 | 2,620 |

Of the 161 unpublished 1962 orations, 41 are `absent` from every pre-1931
witness, 16 are `variant` where 1955 or 1960 revised the wording, 10 are genuine
1955 composition, and **33 are `blocked` on a string that needs reading on a
page image**. Only that last group is likely to become publishable.

### The witnesses

Four public-domain books, all registered:

  * `pustet-ratisbon-1862` — tracked text layer, `prose-latin`, no page images
    for the temporal or sanctoral runs;
  * `1922-tours-mame-editio-quarta-iuxta-typicam` — **the only one whose page
    images render**, and the one that carries the nineteenth- and
    twentieth-century feasts the 1862 cannot. It supplied more antecedents than
    the 1862 in every sanctoral lane;
  * `venice-1570` and `vatican-typica-1604` — `degraded-latin`, corroboration
    only.

Both 1962 witnesses (the CMAA facsimile and the Benziger conformed printing) are
`storage = "remote"` by rights design; they were fetched once against their
registered hashes into session scratch and are not retained.

### The rules the maintainer settled, all in guidance/propers-for-agents.md

  * **A transformation changes how a word is spelled; a variant changes which
    word is said.** The repository publishes its own declared orthography and
    has never served an exact 1962 string: it prints `justitiae` with a j where
    the facsimile prints 231 i-forms and none the other way, and `Alleluia`
    where the Mame prints 797 `Alleluja`. An exact-string rule applied honestly
    would withhold every body in the calendar.
  * **An order is not a contribution.** 1955 mostly selected, cut, restored and
    reordered; 103(b) reaches the prayer a reform composed, never the new
    position it gave an old one. This recovered eleven Easter Vigil texts that
    a lane had reported wholly absent — three of the four prophecy collects sit
    at the 1862's 4th, 8th and 12th ordinals.
  * **Filling a rubrical blank is not authorship**, where the 1962 writes the
    day's saint into a Common's slot.
  * **Reproduce the conclusion the target prints, at the length it prints it.**
    This closed an `open_collation_items` entry.
  * **A chant body carries the sung words, not the printed citation**, which the
    `verses` field already holds.
  * **The ceiling is a text's first publication, not the saint's canonisation.**
    St John Leonardi was canonised in 1938 and his whole formulary is in the
    1922 Mame under `B. Joannis Leonardi`.

### Two guards, and why a screen is not enough

`scripts/_latin_body_damage.py`, run by `check-calendar-masses`, refuses a body
that is a recogniser reading rather than a page reading: accents read as digits,
the ae ligature read as se or x or a question mark, u read as ii, welded words,
characters no prayer carries. 133 bodies were quarantined by it. Its tests carry
the false positives that shaped it — `praesidiis`, `audisset`, `cor`, `ego`,
`da`, `Ps. 77, 1`, `«Hosanna»`, the `/` of Gloria laus — because a length rule
tried and removed had refused all of them, and one lane's finalizer had already
DELETED `es`, `Da`, `O` and `qui` from a body on that reasoning.

`tools/audit-latin-body-substitutions` finds what no pattern can: a token that
becomes a word the corpus already uses under exactly one substitution.
`seterna`, `quassumus`, `animas`, `lsetificas` all damage into ordinary-looking
Latin and passed every screen. It found eleven in already-committed bodies; a
repair lane read all eleven on page images and **none read as stored**. It
reports and never edits, and its two page-confirmed false positives are recorded
in it: `per maris undas` is the sea St Raymund crossed.

The lesson behind both: a cross-witness check cannot see damage two witnesses
share. The 1862 layer has 306 instances of `qusesumus` and the Benziger 397.

### Where the unpublished 100 are recorded

`src/sources/inventories/roman-1962-latin-backfill-findings-v1.toml` carries one
entry per appointed oration the backfill did not publish: the verdict, the
confidence, the lane that reached it, the target and antecedent loci, every
recorded difference, and the evidence sentence the lane wrote. It exists because
the reasoning cost more than the reading did — each absence rests on an
end-to-end sweep of the four public-domain witnesses with a positive control,
and without the record a later pass re-derives an answer this one already has.

Read it before re-testing anything in the `absent`, `variant` or `new-matter`
classes. The 32 `blocked` are the ones worth another lane: their collation
stands and only the stored 1962 string was recogniser damage, so what they need
is eyes on a page image, not another sweep.

### The toolkit

`scripts/latin_backfill/` — apply, land, reconcile, and the j-orthography map,
with a README recording what each guard is for and what it cost to learn. Not
registered tools: each is a step in a human-driven sequence, not one question
with a byte-stable answer.

A lane brief lives at `.scratch/backfill/LANE-BRIEF.md` while a session runs and
does not survive it. Its durable content is in guidance; its operational content
— the page mappings, the traps — is reproduced below.

### Traps a future lane will hit

  * `pdftotext -layout` interleaves two-column pages; use `-raw` for searching.
    `-bbox` interleaves the same way.
  * A page with a mid-page full-width feast title has two STACKED column blocks,
    which `-raw` does not fix. Split horizontally at the heading first.
  * The Mame's recogniser prints `æ` as `z` or drops it to `e`; the literal
    string `ae` occurs 279 times in 2.27 MB of that layer, so any Mame negative
    reached over `ae` is worthless.
  * A body can lose its OPENING WORD entirely to a dropped ornamental initial
    and still be well-formed Latin. Check each against the calendar's `incipit`.
  * Page mappings, each to be verified against the page's own printed folio:
    1962 temporal and sanctoral PDF = printed + 81; the 1962 Commune is
    separately paginated at PDF = printed bracketed + 808; the Mame at
    PDF = printed + 114, and its Commune at PDF = printed starred + 878.
  * A day's Mass usually begins at the foot of the preceding folio, so the
    running head lags the formulary. The FORMA MISSAE BREVIOR between Ember
    Saturday of Lent I and Dominica II puts every later day one off if you count
    Introits.

### Outstanding, in the order I would take it

  1. **The 33 blocked bodies** — one repair lane. The only category likely to
     become publishable. Includes the four whose stored target was truncated
     mid-prayer (`s-hilarii` Secret, `comm-s-petri-apostoli` Secret,
     `comm-s-pauli-apostoli` Postcommunion, `s-gregorii-i` Postcommunion),
     which need a collation lane rather than a repair lane, since a repair lane
     may not manufacture the rest of a prayer.
  2. **The 2,176 sung propers of the 1962 calendar.** The reader currently
     prints a Bible wherever the Missal recasts: for the Fourteenth Sunday's
     Communion it shows `Quaerite ergo primum regnum Dei, et justitiam ejus`
     where the Missal prints `Primum quaerite regnum Dei, et omnia adjicientur
     vobis, dicit Dominus`. A recast antiphon is `mixed`, not `scripture`, so
     each needs its `source` changed as well as a body.
  3. **The postconciliar calendar**, 327 composed and 2,620 sung. Its rights
     position is genuinely different — ICEL English, a 2002 typical edition in
     copyright, its own settled records — and the 1962 rules do not carry over
     unexamined.

### Things left in a state a reader should know about

  * The Exsultet stays `variant` and the question is closed on a decree, not a
    failed search: the SRC's *Urbis et Orbis* of 23 September 1860 ordered that
    the imperial commemoration no longer be RECITED but still be PRINTED in new
    Missals, which is why a republican printing still prints an emperor. A
    Baltimore 1835 and a Tours Mame 1882 were read on page images to confirm it.
    The one unopened route: no pre-1931 Pustet New York or Benziger New York
    altar Missal is scanned anywhere reachable.
  * The seventeen Common and Saturday-BVM chants that
    `roman-1962-pustet-common-collation-v1.toml` withheld on 2026-08-26 are now
    published on the Mame. That record is superseded for publication and says so
    in its own words; every finding it makes about the Pustet stands.
  * 35 release bindings were stale before this work began and were adopted with
    the rest. Nobody has investigated why those web editions changed.
  * The Claude Fourteenth Sunday remains held: it has no installed PDF, and
    both of its release records state `status: hold`. Its partial production is
    being integrated on `feature/propers-chronology`, not promoted to `main`.

### Superseded restart plan after the first two failed runs, 2026-09-04

This section records the decision at that point; it is not a current runbook.
Run `90dcdddcb6780e60` later blocked as well. Current restarts bind
`proper-finish` v3 or `proper` v25; see "The Fourteenth Sunday blocked on an
accounting defect" below.

Neither of the two runs known at that point could be advanced.

  * `ca03f1b357e7ec25` (`proper` v17) is BLOCKED and recorded above as not
    replayable, because from its iteration 2 the coordinator supplemented each
    lane brief out of packet.
  * `416bacef11b97508` (`proper` v19) stopped awaiting a `source-audit` result.
    The `proper` pipeline on disk was then v22 and its source digest had moved, so
    `load_bound_workflow` fails closed: *"Seed a new run against the new
    version."* A run is bound to the pipeline, fragment and schema bytes it
    started with. `status` still reports on it; nothing else will.

The plan at that point had two routes:

  * `tools/tpt proper-finish 54-fourteenth-after-pentecost seed --provider
    claude` — v1, the rescue pipeline that starts at `author-proper` and skips
    seed, authorize-target, scope-gate, resolve-context and the seven research
    lanes. It is the shape that fits: the leaf is fully authored, all five
    profile-required records are present, and what remains is a revision
    clearing the eight findings, then build and publish. Proper 55 was finished
    this way. Its cost is that it has no `research-synthesis` stage and so no
    `Prior-production carry-forward`; the eight findings reach it only through
    `intervene`, which OPERATOR.md counts as workflow debt. All eight are real
    defects still standing in the committed leaf, so a fresh
    `content-evaluation` should raise them on its own — but that is to be
    verified, not assumed.
  * `tools/tpt proper 54-fourteenth-after-pentecost seed --provider claude` —
    v22, the full pipeline, whose `research-synthesis` carries prior findings
    forward by design and which re-runs the seven research lanes against a
    corpus that has moved a long way. Much more expensive.

Whichever is taken: the rights wall the earlier runs stopped at is largely gone.
The three orations that carried `text_status` rights-withheld — Collect *Custodi
Domine*, Secret *Concede nobis*, Postcommunion *Purificent semper* — have
published Latin bodies as of 2026-09-04. Anything either run concluded about
Latin availability is stale.

### Historical deployment-inventory defect, resolved during integration, 2026-09-04

At the time, `make check` failed on `origin/main` at
`check-deployment-sources`, before this work landed. `1ed7fd9a4 Checkpoint
Proper 55 rescue leaf` put
`src/gpt/.../55-fifteenth-after-pentecost/` on `main` without registering it in
`publications-v1.toml`, so `source-inventory` reports the publication and its
twenty source-bearing files as missing from the inventory. The GPT Proper 55
gap was repaired on main. Integrating the Claude Proper 54 source later exposed
the same invariant; its source inventory and classification review were
refreshed while its separate release records remained on hold.

## The Fourteenth Sunday blocked on an accounting defect, 2026-09-04

`proper-finish` v1 run `90dcdddcb6780e60` (Claude, Fourteenth Sunday after
Pentecost) reached BLOCKED at the `content-evaluation` iteration bound. The
leaf as it left it is committed at `9ca815a90`; nothing was built into `pdf/`
or `web/`, nothing installed, no release binding moved.

### The eight findings of `ca03f1b357e7ec25` are accounted for

Seven closed and verified against the leaf: `CON-REC-002`, `CON-REC-003`,
`CON-SYN-002`, `CON-CIT-004`, `CON-CIT-020`, `CON-CIT-021`, `CON-CIT-022`.
`CON-PRO-003`, the register defect that ended that run, was not closed: it was
raised again on its own evidence and worked for three more iterations without
being exhausted. `build/tpt-runs/ca03f1b357e7ec25` holds nothing this entry
does not account for and may be swept.

The ignored run directory did not cross the Git handoff into this clone, and no
`evaluations/blocking-findings-v1.toml` exists for this leaf. Its exact final
joined result and sole second revision-pass result are now tracked under the
leaf's `research/` directory, and its seven final blocking findings are
enumerated in `HANDOFF-proper-54-convergence.md`, without falsely claiming that
the old run wrote a formal standing-findings record. The originating
`triptych/proper-54` workspace is therefore no longer the sole copy.

The run repaired eighteen blocking findings in two revision passes, two of
which the previous production never reached. A sentence stood in quotation
marks in `40-notable.tex`, attributed to the *Semi-weekly interior journal* of
19 November 1895 at a named page, that no research record of this leaf carries;
`evidence-discipline` and `citation-integrity` found it independently of each
other. And `Carter v. Harris` carried a two-century span claim while
`research/scope.md` §12.5 records it "not opened and not relied on".

The ignored run directory was not itself portable. Integration therefore
preserves its final joined evaluation and its sole second revision-pass result
verbatim in the leaf as `research/production-content-evaluation-0002.json` and
`research/production-content-revision-0001.json`; the tracked handoff records
their SHA-256 digests and enumerates the seven blocking findings still open.

### Why it blocked, which was not the document

The repeat budget compared blocking finding ids across iterations. It named
`CON-CIT-020`, `CON-CIT-021`, `CON-PRO-001` and `CON-PRO-002` as still
unrepaired at 3/3. Every one of those names a different defect in a different
file each iteration, and the earlier ones were gone from the leaf.
`stage_failures` stood at 3 against a ceiling of 6: the run converged the whole
way -- seven blocking findings, then eleven, then seven, each iteration
clearing the set before it, one lane clean from the second iteration on -- and
was stopped at half the allowance the engine's own design granted it.

No lane caused it and none could have prevented it. A fan-out evaluator's lane
packets carry an empty `PRIOR_FINDINGS` by design and lanes are told not to
read earlier results, so **no lane can know which ids an earlier iteration
used**. One lane guessed at `010`/`011` to dodge a collision it could not see;
another minted `020`/`021` to dodge ids recorded in the brief and landed on the
previous iteration's. An id is a handle a lane minted for its own report, not
an identity for a defect. This is the hazard the entry below on unstable ids
records, arriving as a termination condition rather than a carry-forward
nuisance.

### What was built in answer, 2026-09-04

- **The budget reads the reviser where a reviser can answer.** A stage that
  declares `reports_repairs` returns `finding_dispositions`, one entry per
  blocking finding it was given, `repaired` or `not-repaired`. Omitting one is
  refused: a dropped finding reads exactly like a repaired one. The
  declaration is per stage because a fan-out `research` re-entry produces a
  result the engine composed from lanes, so no agent can speak for it.

  **Where no report exists the id comparison stays, deliberately.** That is
  wherever the stage a failure's findings were routed to does not declare the
  key: two of `content-evaluation`'s three repair routes, `research` and
  `brief`; `research-synthesis`, whose failure re-enters the `research`
  fan-out; and every gate.
  Deleting it there would leave such a stage bounded by `max_total_iterations`
  alone, silently doubling every limit an operator declared. A gate keeps it
  whatever its reviser reports, and there it is not a heuristic: a gate's ids
  are a program's, so a repeat is the same check refusing the same leaf again
  after a repair was claimed, which is better evidence of a loop than the
  claim is of progress. Ground truth displaces the heuristic exactly where it
  exists.
- **`house-voice` and `proposal-fields`**, two new `content-preflight` checks.
  The first is `scripts/_house_voice.py`, modelled on `_latin_body_damage.py`,
  and it drains in a gate loop what cost two productions their whole evaluation
  budget. It reports 28 loci on the Fourteenth Sunday leaf against 22 the lanes
  found, 20 of the 22 recovered. **It refuses 8 of the 12 leaves carrying a
  manifest, published ones included** -- the habit is the corpus's, not this
  leaf's -- and it found a retrieval-mechanics defect in published leaf 52 that
  no evaluation ever reported, and five proposals in gpt leaf 52 that state no
  "what the element-by-element reading misses" field at all.
- **Lane ownership for three ownerless classes.** Proposal fields to
  `synthesis-argument`, stated counts to `citation-integrity` (criterion 7 is
  now "Citations and stated counts"), Latin orthography against
  `propers/verified.md` to `evidence-discipline`, each with a matching "not
  yours" note in the lanes that declined it.
- **Criterion 12's scope ambiguity resolved** in favour of the governing
  sentence; the enumerated list is demoted to a checklist that is explicitly
  not the boundary. The ambiguity is real and it is in the fragment: at
  iteration 2 of `90dcdddcb6780e60` the lane raised the appointed text's
  `\englishgap` blocks under criterion 12 while the fragment's list of
  sections did not name that section and its never-a-finding exceptions did
  not cover it, so the lane had to settle for itself both that the section was
  in scope and which half of an English-gap block the profile asks for. It
  settled both correctly and the leaf was repaired. Nothing made that the only
  available reading — the same list read as a boundary excludes the section
  outright, and a lane reading it that way would have left the defect
  standing. The stronger claim this entry first made, that a later iteration
  declined the section as out of scope, is **not supported by the run
  record**: no `profile-conformance` result in any surviving run directory
  contains the phrase, and iteration 3's silence about that file is explained
  by `content-revision-0001.json`, which reports the blocks repaired.
- **`observations`**, a non-blocking array on evaluator results, joined and
  recorded, for what a lane saw outside its criteria. It is a backstop, not a
  substitute for ownership.
- **`DOCUMENT_ROOT`** in the packet header, from a `document_root` template.
  A lane swept `src/gpt/...` to completion against a packet reading
  `"provider":"claude"` and discarded a finished max-effort sweep.
- **A tracked home for the findings standing against a leaf.** The stage
  declaring `records_standing_findings` — `content-evaluation`, in both
  pipelines, and no other stage — writes
  `<document_root>/evaluations/blocking-findings-v1.toml` after each of its
  evaluations, terminal ones included, rewritten whole. It is written before
  the run's commit, so a failed write aborts the advance instead of leaving
  the run advanced and the obvious retry failing on a stage mismatch. The key
  is per stage because every evaluator wrote the path at first, which let a
  `web-evaluation` replace a leaf's content findings with findings about
  generated HTML. The engine's write has its own root so a test harness cannot
  dirty `src/`; that defect was found and fixed during this work.

  **Nothing reads it back into a run.** Reading it at seed was built and then
  backed out, a third cold review having found it wrong three ways at once:
  the pristine recompile in `_load_verified_bootstrap` knew nothing of the
  extra argument, so a run seeded against a non-empty record could never be
  seeded again — breaking the seed idempotency `OPERATOR.md` promises in terms
  and a whole suite exists to protect, and invisible because every driven test
  points the record at an empty scratch directory; the file is untracked
  working-tree state that no `repo_commit` moves with and no
  `workflow_source_digest` covers, so one run id could produce different
  bootstrap bytes; and on `proper.json` the findings reached only the `seed`
  stage's packet, unfiltered by `repair_target`, so a record last written by
  `research-synthesis` would have handed `brief`-owned findings to a stage
  that repairs only `authoring`. Automatic carry-forward is still owed, and
  owed somewhere the run's identity can cover it: either an operator
  subcommand whose output is committed, so `repo_commit` moves with the
  record, or the record's own hash in `compute_run_id` and in the acceptance
  audit.

  Against the entry below on run state being called durable, this is progress
  and not closure. That entry owes three things. `OPERATOR.md` no longer calls
  the run directory durable: done. Step 11 of
  `workflows/fragments/propers/research-synthesis.md` now says what an empty
  `grep build/tpt-runs/*/state.json` means — the directories are gone, not
  that there was no prior production — and names the tracked record and the
  inherited brief as what to read instead: done. The tracked home itself is
  half done. Blocking findings and observations have one; **escalations still
  live only in `state["escalations"]` under `build/`**, and the only part of
  an escalation that reliably leaves a run is the terminal console message.
  And the thing that entry actually wanted — a later production reading a
  committed record rather than an ignored directory — is not built, because
  nothing reads the record.

### Four defects found while building the answer

Three were introduced by this work and caught before it landed; one was not
this work's and had been hiding.

  * The engine's tracked-record write went into the working tree, so running
    the test suite left a real file under `src/gpt/`. It has its own root now:
    production writes to the tree, every harness writes to disposable storage,
    and `None` turns it off.
  * The TOML writer special-cased `"""` and mangled a finding whose prose ended
    in one. It escapes every quote in both string forms now, which is more than
    TOML needs and short enough to be obviously correct; 20,000 fuzz cases
    round-trip, 3,000 of them as a test.
  * Requiring the repair report of every stage broke every `research`
    re-entry: a fan-out result is composed by the engine from lane results, so
    no agent wrote it and no lane can speak for the whole. The requirement is a
    `reports_repairs` declaration in the pipeline now.
  * `bindings-valid` resolved `tools/source-library` relative to `--root`, so
    under any root but the repository it ran a script that was not there and
    reported the interpreter's exit 2 as though the library had refused the
    leaf. Every `--root` invocation had been failing for a reason with nothing
    to do with bindings.

**`proper-finish` leaves were escaping the chronology contract.** Its scope
rule keyed on the workflow id `proper`, so a leaf whose provenance record says
`proper-finish` read as "no proper provenance record" and was reported out of
scope. A rescue run could have authored a leaf with no chronology record at
all and been passed for want of an answer. The contract now binds `proper`
from v17 and `proper-finish` from every version, it having been written after
the contract. The Fourteenth Sunday leaf was in scope anyway, through the
branch that catches a leaf carrying a record, so nothing was let through.

`tests/tools/check-content-preflight.test` was red on `main` before any of
this, in three independent ways: a stale check count, a synthetic fixture two
`source-library` schema changes behind, and the tool-path defect above. It
passes now. That was verified against a clean `HEAD` worktree rather than
assumed.

### What three cold reviews changed, and what they cost

The work above was reviewed cold by three independent readers -- engine,
prose checks, guidance -- each told the author's account was not evidence.
They were right about a great deal, and the change is materially different for
it. What they found, and what it means for anyone reading this later:

**A feature was backed out rather than patched.** The tracked findings record
was to be read at seed, giving a pipeline that begins after research the
carry-forward it has no stage for. It was wrong three ways at once:
`_load_verified_bootstrap` recompiles the seed packet from pristine state and
did not know about the argument, so a run seeded against a non-empty record
could never be seeded again -- breaking the idempotency OPERATOR.md promises
and `test_workflow_seed_idempotency.py` protects, invisibly, because every
driven test points the record at an empty directory; the file is untracked
working-tree state that no `repo_commit` moves with and no
`workflow_source_digest` covers, so one run id could yield different bootstrap
bytes; and on `proper` the findings reached only the `seed` packet anyway,
unfiltered by owner. **The write stays and nothing reads it.** Carrying
findings between productions still wants doing, and wants doing where the run's
identity can cover it: an operator subcommand whose output is committed, or the
record's hash in `compute_run_id` and the acceptance audit.

**Four more defects in the same write**, all found by review and all fixed: it
skipped the terminal transition, so a run that blocked -- the case it exists
for -- recorded nothing; a stray `U+007F` in quoted source made the file
unparseable and the reader, catching that, discarded every well-formed finding
in it; `provider` is free text no validator constrains, so a typo wrote a
`src/gtp/...` tree and `..` wrote anywhere; and every evaluator wrote the same
path, so a `web-evaluation` could replace a leaf's content findings with
findings about generated HTML. It is now declared per stage
(`records_standing_findings`), containment- and symlink-checked, written before
the run's commit so a failure aborts cleanly, and `status` reports what it
holds.

**`house-voice` was unsafe and is now sound.** It tested the subject of a
relative clause rather than the sentence's, so it refused bounds on negative
results, denominators, and the 17 U.S.C. 103(b) rights clause -- six firings of
that clause across five leaves. Its message told a reviser to move the material
to an appendix "which already carries it", a fact it never checked. Fixed: a
clause test, five topic rules deleted, quotations taken from the source and
greppable, and the appendix advice gone. The cost is priced and real: 28 loci
on the Fourteenth Sunday leaf became 20, all 20 genuine, and recall against the
lanes fell from 20/22 to 17/22. Corpus-wide 119 firings became 88, the same
eight leaves refused, and none of the 88 refuses a bound, a denominator or a
rights basis.

**A version test was reading a five-year-old line.** `OPERATOR.md` repeats "The
`proper` workflow is at version N." for every historical version, so when a
rewording dropped the period the pattern needed, the test did not fail for
finding nothing -- it matched the version-12 changelog entry and asserted
against that. It now checks both pipelines and tolerates line wrapping.

Both pipelines are bumped: `proper` 22 to 23, `proper-finish` 1 to 2.

### Left standing, and worth a maintainer's decision

`house-voice` refuses 8 of 12 leaves, and that number did not move when the
false positives were removed -- the eight are the same eight. Every remaining
refusal was read against `guidance/editorial.md` and is a form it names, so the
check is not obviously wrong and the corpus is not obviously right. Nothing was
repaired in another leaf on the strength of it. Two it found that no evaluation
ever reported: retrieval mechanics in the reader-facing body of published
`claude/52`, and five proposals in `gpt/52` that state no "what the ordinary
element-by-element reading misses" field at all.

Two judgement calls in the screen fail toward silence rather than deletion, and
are recorded in its tests: a real locus at `30-commentary.tex:1177` is
suppressed because no rule distinguishes its form from a denominator, and the
possessive rule carries no clause guard, so a codicological "The leaf's verso"
would fire it. The corpus does not currently write that.

`scripts/replay_examples.py`'s `TrackedGuard` snapshots the dirty set at start
and reverts anything that changed during the run. Two concurrent workers hit
it: it reported reverting `PROJECT-WORK.md` and a fragment another worker was
editing. Nothing was lost here, but running it while anyone else writes can
silently revert their work.

The engine reviewer's design point stands unaddressed: `reports_repairs` on a
stage and the gate carve-out in the budget are two special cases for one
property -- who minted the id. An id from a program is an identity; an id from
a lane that cannot see the previous iteration is a handle. That belongs on the
stage as one declaration, and a deterministic evaluator or a fan-out gate will
need a third carve-out before it is.

## Standing public-alpha authority

On 27 July 2026 the maintainer approved every Triptych document for
conspicuously labeled public-alpha distribution so that priests and other
qualified readers can review it from stable public links. This is a standing
workflow authorization: changed source may be researched, built, inspected,
installed, bound as an exact current public-review snapshot, validated, and
committed without requesting a new
document-by-document alpha approval.

A clean direct Codex session on `main` has standing authority to make ordinary
coherent commits for authorized work and regularly push validated checkpoints
to `origin/main` after each independently reviewable unit. Before each push,
run the checks required by the affected guidance, inspect the exact outgoing
range, and confirm that every newly reachable object is intended for public
disclosure. Because each `origin/main` push triggers GitHub Pages, this
authority includes the resulting automatic deployment attempt. It does not
authorize force-pushing, amending or otherwise rewriting published history,
changing remotes, integrating a retained worker, or triggering another
deployment mechanism. Never represent a snapshot as live until its Pages run
has succeeded and the affected production routes have been verified.

Public-alpha authorization is distribution authority only. It never records
or implies human, priestly, specialist, ecclesiastical, rights, intended-reader,
physical-print, or final editorial approval that has not actually occurred.

On 31 July 2026 the maintainer retired the six-concern alpha completion
assessment — source support, rights and distribution status, safety, artifact
consistency, mechanical correctness, every-page visual inspection — as
bookkeeping the project imposed on itself. No tool ever read those fields; they
were prose scoring prose. A publication is alpha when it is built, checked by
the gates that actually run, and published.

What that retirement does not touch, because none of it was ever the
bookkeeping: a known defect still stays explicit in the research records,
release inventory, catalogs, and this register — recording a defect is how a
reader learns of it, not a gate. Passing an internal check still does not imply
external approval, and the workflow still creates no placeholder gate for a
reviewer who is not coming. Those are statements about what is true, and
withdrawing a scoring scheme does not make them false.

## Research staleness is suspended

On 31 July 2026 the maintainer suspended the research-staleness signal. Nothing
is to be flagged stale, and **the papers are to be left exactly as they are**.
No research is re-read, no review record is written, and no edition is
rebaselined until the suspension is lifted.

Two reasons, and the second is the larger. The signal measures the wrong thing:
it reports a publication stale when any artifact appears under a work it cites,
not when an input it binds changes, so a paper on the virtues reported 156
changed inputs, every one a Clementine verse table it does not bind. And the
tooling under these papers is still moving — the calendars, the concordance, the
commentary chain and the source library all changed materially in a single day —
so anything this tooling will eventually invalidate, it has not finished
invalidating. A baseline taken now is taken against a moving one.

**Suspended, deliberately not rebaselined.** Rebaselining writes down that the
research was re-read against the changed inputs. That review did not happen, and
recording it would put a false statement in 24 editions to make a number go to
zero. Suspension records the true thing instead: measurement has stopped.

`make check-staleness` reports the suspension and exits clean;
`make measure-staleness` still runs the raw signal for anyone who wants to look
at it without acting on it. Nothing in the ledger or in any paper was touched.

**How this ends:** one full pass back through the research, when the tooling has
matured — not edition by edition as the flag fires. TASK-93 repairs what
staleness measures and is a prerequisite of that pass, not of lifting the
suspension.

Research is not limited to publicly reachable sources. On 31 July 2026 the
maintainer withdrew the rule that had forbidden purchasing an edition, using a
paid subscription, requesting credentials, or asking the maintainer to fund
source access, on the ground that it was never a requirement of anything — it
was a self-imposed limit that turned an ordinary cost question into a permanent
evidence gap. Where a witness would settle a question, name it and what it
would cost; the maintainer decides whether to obtain it.

Two things this does not change, because neither was ever a project rule.
Copyright and licence terms bind whatever the research budget is: a text the
project may read is not thereby a text it may republish, and the standing
public-alpha authorization is authority to distribute this project's own work,
never someone else's. And a witness that has not actually been consulted is
still unconsulted — record what was read, not what was reachable.

The maintainer authorizes creation and revision of project-owned AI artwork
for the sanctuary pictorial dictionaries and altar-server guide series. Each
asset must remain grounded in publicly reachable, source-controlled evidence;
carry its exact generation or edit provenance, references, hash, rights,
corrections, consumers, and review state; and remain visibly provisional where
review is open. Artwork may not invent or silently resolve an object's
identity, morphology, scale, arrangement, ceremonial use, historical state, or
an actor's liturgical action. AI creation supplies no human artwork,
liturgical, ceremonial, or ecclesiastical review.

No external human-review cycle will be available for some time. Human,
priestly, specialist, intended-reader, physical-use, and ecclesiastical review
are therefore neither promised workflow steps nor alpha completion gates.
Continue research, revision, artwork production, mechanical and AI-assisted
audit, building, installation, public-alpha binding, integration, push, and
deployment against the six concrete concerns above. Record an external review
only if it actually occurs, and never convert internal or AI checking into a
claim of human approval.

## Current integration and publication state

The repaired public-alpha snapshot is integrated on `main`; pull request 1 was
merged, and subsequent validated checkpoints have continued through the direct
`main` workflow. The stable review landing page, PDF, and web-edition routes
for the exorcism paper have resolved in production checks. The current
repository source, installed PDF, web edition, comprehensive plan, and exact-
snapshot audit agree on a completed bounded study of 116 physical pages,
including 103 substantive narrative pages. Each later `origin/main` checkpoint
requires its own successful Pages run and verification of the affected
production routes before it is represented as live.

## Clean direct-main workflow

For a clean direct Codex session started from current `main`, use this
instruction:

> Read `AGENTS.md`, `PROJECT-WORK.md`, `promised-deliverables.toml`,
> `guidance/promised-deliverables.md`, and the guidance and research records
> applicable to the first selected workstream. Reconcile the register against
> current `main` and production Pages before editing. Continue the highest
> actionable open requirement; do not infer completion from a commit, PDF,
> catalog link, push, or deployment. Update the register and ledger before each
> checkpoint commit. After validating each independently reviewable unit,
> inspect its exact outgoing range and push it to `origin/main`; then verify the
> resulting Pages run and affected production routes.

The restarting agent must then:

1. Run `git status`, confirm the current branch is `main`, reconcile it with
   `origin/main`, and preserve unrelated changes.
2. Confirm that `f6e9d2e2` is contained by `main`. If it is not, stop content
   work and report that integration remains open.
3. Run `tools/tpt check-promised-deliverables` and `make check`. Do **not** act
   on research staleness: it is suspended, `make check-staleness` reports the
   suspension, and the papers are left as they are until the tooling settles.
   `make check-source-family-screening` still fails, and honestly — 144 review
   units are unscreened and marking them screened would record a review that did
   not happen. Record the count; do not close it by writing it down.
4. Build and verify the public artifact with `tools/tpt public-alpha check`,
   `tools/tpt public-alpha build`, and `tools/tpt public-alpha verify
   --deployment-target github-pages`; separately verify the live production
   routes after Pages completes.
5. Resume in this order unless the maintainer gives a new priority:
   `task-2-exorcism-100-pages`; `project-recent-paper-hard-review`;
   `task-1-altar-server-guides`;
   `task-4-missa-cantata`; `task-5-solemn-mass`;
   `task-3-sanctuary-dictionaries`; `task-6-linen-restoration`; then the
   repository-wide staleness, source-family, exact-snapshot, and artwork queues.
6. For the exorcism work, begin with its tracked comprehensive expansion plan,
   scope, source audit, and final exact-snapshot review record. Acquire and
   verify research before drafting; preserve the 100 substantive-page
   requirement and the source, safety, law, PDF, web, and every-page gates.
7. Reconcile this file after each independently reviewable work unit. Keep
   completed facts, current evidence, open criteria, blockers, and superseded
   decisions distinct. Commit the coherent unit, run its required validation,
   inspect the exact outgoing range and public-exposure consequences, and push
   the checkpoint to `origin/main`. Verify the Pages result before calling that
   snapshot live, but never call the underlying deliverable complete unless
   its ledger gate passes.

Retained-worker integration, non-Pages deployment, remote changes,
force-pushing, and all other history rewriting remain separately authorized
operations.

## Corpus browser redesign

A multi-agent project to make the non-PDF web surfaces one navigable scholarly
corpus rather than a set of separately built instruments. The PDFs remain the
canonical printable editions and are not a redesign target.

The governing plan on this branch is `guidance/corpus-browser-master-plan.md`.
It splits the work: a design lane owns the visual and product contract, and an
implementation lane owns production code and tests.

`guidance/corpus-browser-implementation.md` is the implementation lane's durable
technical record — how the surfaces are actually built, what will refuse a
change, the proposed sequencing, the ranked risks, and the conflicts returned for
disposition. Reconnaissance is done.

Two facts from that record belong here because they bind unrelated work. First,
`make check` fails at `c27d69153` on `check-tool-registry` and `check-examples`,
and `python3 -m unittest discover -s tools/tests` fails with 14 failures and 13
errors out of 1226; both were reproduced at the base commit in a separate
checkout, so the redness is pre-existing and no later lane may be credited or
blamed for it. Eight of those thirteen errors were later shown to be a stale
fixture rather than a defect — every `test_public_alpha` case wrote a stub root
hardcoding `Markdown==3.10.2` after the repository's lock moved to 3.10.3 —
and `f434c5b91` on `impl/shell-plumbing` fixed it, moving the baseline to **14
failures and 5 errors on that branch and its descendants**. A branch based
before `f434c5b91`, including `impl/foundation-hardening`, should still expect
14 and 13. Second, the corpus lanes overlap the in-progress deliverable
below, which owns `reader-shell.js` and `reader-instrument.css` and declares
public-navigation redesign unauthorized. Sequencing the two was returned as the
first open conflict in that document; the review recorded below settled it.

### Which branch carries what

**Superseded by the 2026-08-10 foundation integration recorded below.** `main`
now carries the six corpus documents, the accepted design and engineering
foundation, and the three corpus ledger entries. The table and cautions below
are kept as the pre-integration state they document; read current documents on
`main`.

No corpus-browser document was on `main`, which was `fc3092de9` as of 2026-08-08
and six commits ahead of the shared base `c27d69153`. The seven lane branches
all still based on `c27d69153`; the two `fix/*` branches did not, because they
were bug fixes taken against `main` itself.

Branch heads, all read from `origin` on 2026-08-08:

| Branch | Head | Bases on | Carries |
| --- | --- | --- | --- |
| `main` | `fc3092de9` | — | no corpus-browser document |
| `impl/foundation` | `af2c9613c` | `c27d69153` | master plan, implementation record, `build/agent-continuity/corpus-browser-foundation-recon.md` |
| `impl/foundation-hardening` | `ecfb4e7b8` | `impl/foundation` | the same three, plus §19 of the implementation record, which exists nowhere else |
| `impl/shell-plumbing` | `c62b83904` | `impl/foundation` at `b87dfc744` | the same three; its implementation record lacks §19 |
| `impl/catena-wave-1` | `efd7559a9` | `impl/foundation` at `b87dfc744` | the same three; its implementation record lacks §19 |
| `ux/foundation` | `3b5938a0d` | `c27d69153` | vision, roadmap, inventory, research, `docs/triptych-world-class-corpus-master-plan.md`, `src/web/browser/prototypes/corpus-foundation/`, `tools/tests/test_corpus_foundation_prototype.py`, `tools/tests/corpus_foundation_prototype_browser.mjs`, `build/agent-continuity/corpus-browser-foundation.md`, and the design lane's ledger entry |
| `ux/corpus-wave-1` | `e42b92874` | `c27d69153` **directly** | vision, roadmap, inventory, research, master plan, implementation record — six documents, and none of the prototype or continuity files |
| `ux/corpus-wave-1-review-fixes` | `ecbd93a05` | `ux/corpus-wave-1` | the same six |
| `fix/day-missal-switch` | `f099e2280` | merged into `main` | — |
| `fix/browser-truthfulness` | `fc3092de9` | merged into `main`; it *is* `main` | — |

Read every one of those documents on the branch that owns it —
`git show <branch>:<path>` — rather than here. They are deliberately not
reproduced, summarised, or paraphrased in this register: a fact has one owner,
and a second copy of a design contract is a disagreement waiting to happen.
`ux/foundation` also carries the design lane's own ledger entry and
work-register section, which is why neither appears on this branch.

Two cautions the table above is the evidence for. First, this table as it stands
on `impl/shell-plumbing` (`PROJECT-WORK.md:215` there) tells a reader that
`guidance/corpus-browser-implementation.md` lives on
`impl/foundation-hardening` — that is, not on the branch they are reading it
on. It is on four branches and the four copies differ. Second, the
`ux/corpus-wave-1*` copies of the
implementation record are a **rewrite pinned at `af2c9613c`**, so they carry as
live four defects that `impl/foundation-hardening` has since fixed — the
`none-claimed` gloss, history's `.field` collision, texts' `.detail` shadow and
`T.fail`'s silent no-op. A Wave-1 agent reading its own branch's copy would act
on repaired work. `guidance/corpus-browser-implementation.md` §5, §11 step 5 and
§20 on `impl/foundation-hardening` are the current statement.

### Acceptance, 2026-08-08

The coordinator dispositioned both lanes on 2026-08-08.

| Lane | Disposition |
| --- | --- |
| A0, surface inventory | accepted |
| A1, research synthesis | accepted |
| A2, site-wide product vision | accepted with amendments D1–D20 |
| A3, tokens and Reader/Catalogue/Instrument archetypes | accepted as foundation direction, not as pixel acceptance of any production route |
| A4, shared navigation, Jump, Related, and shell interaction | accepted with the bounded-Jump and protected-liturgy amendments |
| Claude reconnaissance | accepted |
| the neutral gates | accepted for integration |

The A3 wording governs what implementation may assume. The direction is
accepted; no production route is visually accepted, so no route may cite A3 as
approval of how it renders. The roadmap on `ux/foundation` still records A0–A4
as candidates awaiting independent review; this register is later than that
record, and the design lane had not yet written the dispositions down. (Since
the 2026-08-10 integration, the roadmap on `main` is the Wave 1 rewrite, which
carries the amended dispositions; the `ux/foundation` ledger entry keeps its
honest `candidate` state because its own independent-disposition requirement
was answered by this register and the later Wave 1 review, not by the ZIP
review it originally named.)

### Foundation integration, 2026-08-10

The blocker this section used to record — "B0 cannot start" because no
integration base existed — is resolved. The accepted foundation was
reconciled onto **current `main`** (not the stale `c27d69153` base) and landed
as three merges plus this record:

1. `ux/foundation` (`3b5938a0d`) — consumed in full: A0–A4 documents, the
   corpus-foundation prototype and harnesses, continuity record, and the
   design ledger entry, per the 2026-08-08 coordinator dispositions above.
2. `impl/foundation` + `impl/foundation-hardening` (`81fa65d76`) — consumed in
   full: implementation record with §19, recon continuity record, the neutral
   gates (static parse, artifact gate, URL-contract, harness-runner, and
   collision suites), preview-build wiring, five design-neutral browser
   fixes, and the fail-closed hardening ledger entry, which honestly remains
   `in_progress` with `shared-shell-blocking-collisions-resolved` open on the
   protected `day-missal.css` hazard.
3. `ux/corpus-wave-1` + `ux/corpus-wave-1-review-fixes` (`01eb3eb1e`) —
   documents consumed: the rewritten program-level master plan, vision,
   roadmap, inventory, research, the Wave 1 ledger entry (complete), and the
   acceptance records. The disposable prototype overlay and its harnesses
   were deliberately **not** merged, per the acceptance's own scope limit;
   they remain on the preserved branches. The wave's rewritten implementation
   record was replaced by the engineering lane's, as this register directed.

Semantic reconciliation against the six newer `main` commits (missal-switch,
truthfulness, and URL/page-truth fixes): `history.js` and `texts.js` carry
both lines of fixes; the release bindings were regenerated with
`tools/release-bindings` for the seven browser files the integration changed,
on top of `main`'s current hashes, so no old signature resurrected.

**Deliberately not integrated**, each awaiting its own recorded gate:

- `impl/shell-plumbing` (`c62b83904`): generator/layout plumbing, Makefile
  target hygiene, the stale `test_public_alpha` fixture fix (`f434c5b91`),
  and the single-`main`-landmark change. No acceptance record exists. Its
  content is the natural input to B0 and should be consumed under B0's own
  gates, not merged wholesale.
- `impl/catena-wave-1` (`efd7559a9`): the E1 implementation of the accepted
  E0 contract, with its 36-test suite and re-signing. E1 was authorized to
  proceed independently, but no acceptance disposition of the implementation
  is recorded; under the plan's acceptance model it stays off `main` until
  independent review dispositions it. It is the nearest-to-ready pending
  lane.
- `impl/didach-domain` and `ux/didach-identity`: the abandoned `didach.ai`
  direction; not part of this program.

**Domain state.** The public origin moved to `https://mystago.gy/` through
GitHub Pages settings and DNS; the old project-path origin 301-redirects.
`tools/public-alpha` now declares the custom-domain origin, constructs and
verifies canonical `og:url` and `og:image` metadata there, and keeps all
in-artifact navigation relative so the same static artifact remains portable
under a GitHub Pages project-path preview. Triptych remains the product and
repository identity; this repository change corrects metadata and does not
perform or imply a deployment.

**Gate baseline for this tree.** `check-browser-gate` over the built site:
2,290 assertions, **228** failures — 117 single-`main`, 82 target-size, 27
skip-link/modal-trap, 2 narrow-320 overflows (`/sources/` by 24px, `/texts/`
by 56px). The same gate over a pure-`main` build reports the identical 228,
so the two overflow findings are main's newer surfaces measured for the first
time, not an integration regression. The hardening branch's recorded 226
described its own older tree.

**Next action.** B0/B1 — the production shared-shell primitives and their
regression harness — are unblocked and authorized: the design contracts and
shared-shell acceptance are recorded above, and the plan's sequence
(foundation → catalogue/reader/instrument lanes → cross-object links/search →
final acceptance) is unchanged. A Claude engineering lane should start B0
from the current `main` tip on a fresh `impl/` branch, consuming
`impl/shell-plumbing`'s work under B0's gates. New lanes start from `main`;
no standing integration branch exists or is a dependency.

**Deviation, recorded because it is real: Wave 1 started off-base.** The master
plan requires that "once `corpus/foundation-integration` is pushed, all new
Wave 1 work starts from its exact head"
(`guidance/corpus-browser-master-plan.md:1585`, and again at `:1658` and
`:1790`). `ux/corpus-wave-1` (`e42b92874`) was created as a single commit
directly on `c27d69153`, not on any integration head, and
`ux/corpus-wave-1-review-fixes` (`ecbd93a05`) descends from it. Neither branch
descends from `ux/foundation` or from any impl branch; the two lanes' documents
were reconciled onto that branch by hand instead, which is precisely the work
the integration branch exists to do once and durably. The consequence is already
visible: those branches carry a rewritten implementation record pinned at
`af2c9613c` that presents four repaired defects as live. The wave should be
rebased onto the integration head when it exists, and its implementation record
replaced rather than merged.

The narrower claim this section used to make — that no shared shell is
implemented on any branch — still holds. `impl/shell-plumbing` changed the
generator and the layout wrapper; it built no shared shell.

### Foundation hardening

The 2026-08-08 review settled the sequencing question above by protecting the
liturgy surface family outright, so promoting `reader-shell.js` into a shared
shell is withdrawn rather than deferred: reuse its ideas, not the owned file.

`impl/foundation-hardening` carries the work that does not depend on the visual
contract, each commit cherry-pickable by path. The four real-Chromium
harnesses are invoked at last by `check-browser-harnesses`, which depends on
`public-preview` because three of them address it as their data root — the
reason they were read as broken for months was a missing build, not rot. The
artifact gate moved to the governing matrix and gained no-JavaScript, subpath
deep-link, link-resolution and focus-indicator coverage. Every published hash
contract is pinned by 46 tests before anyone cleans up a router. Both new gates
stay out of `make check`, which builds no artifact and cannot assume a browser.

Three things that lane found are worth recording outside it. The gate's
skip-link failures are a modal focus trap in the Propers reader, not a missing
link, and belong to the liturgy deliverable rather than to any corpus lane. The
Source Library's "Back to the corpus" does not leave a bare fragment as
reported; it leaves the entire reader hash, so a reload reopens the edition the
reader just closed. And target size fails on all nineteen routes — history alone
has 909 undersized controls — which is a design-lane dependency, not a hardening
defect.

Measured baselines for anyone comparing. `make check` takes about 310 seconds
and is red at the base for reasons this project did not cause.

`check-browser-gate` is no longer "about 74 seconds" and no longer reports 146
failures; both figures were true at `0fcf0cb95` and are true nowhere now. The
gate was widened to the five-viewport governing matrix, which took it to 2,290
assertions and surfaced an entire new failure class. **Re-run at `ecfb4e7b8` on
`impl/foundation-hardening`: 93 seconds, 2,290 assertions, 1,836 passed, 226
failed, 228 skipped**, across 19 routes and 9 states, with two consecutive runs
agreeing. The 226 are 117 `single-main-element`, 82
`primary-controls-meet-target-size` and 27 `skip-link-targets-existing-element`,
and nothing else.

**The number differs by branch and a single figure would be false on one of
them.** On `impl/shell-plumbing` the same gate reports **109**, because
`6b5742bf2` gave every published page exactly one main landmark and closed the
117; that branch's figure is taken from that commit's own measurement rather
than re-run here. Cite the branch with the number.
`guidance/corpus-browser-implementation.md` §17.5 owns the full arc and §20 owns
the disposition of each surviving class. Compare failure sets, never exit codes.

The lane also gave ten previously unrecorded browser defects a tracked home, and
recorded eight reported findings that re-checking refuted, in
`guidance/corpus-browser-implementation.md` §20. Before that section they existed
only in agent reports in a scratch directory, which §14's amendment D10
forbids — and a scratch directory is deleted, so they were one `rm` from being
rediscovered at full cost.

### Ledger gap: the implementation lane has no promised deliverable

The design lane recorded `corpus-browser-foundation-design-2026-08-08` in
`promised-deliverables.toml` on `ux/foundation`. **The implementation lane
recorded nothing.** Its diff against `c27d69153` touches `PROJECT-WORK.md` and
does not touch the ledger, so nothing fail-closed tracks the implementation work
at all — no promise, no acceptance criteria, and no requirement that a later
session must either satisfy or explicitly supersede. That is a live breach of
`guidance/promised-deliverables.md`, which requires a substantive outcome to be
recorded with a stable ID *before* material implementation, and this lane shipped
material implementation: two new gates, a harness target, 46 hash-contract tests,
three production renames and signature changes, and seven re-signed browser
files.

The promise and its completion criteria are known, so per that guidance they are
specified here for immediate promotion into the TOML ledger. **The ledger file
itself is outside this task's exclusive file boundary and was deliberately not
written**, because `promised-deliverables.toml` is shared across every branch
and a malformed entry breaks `make check` everywhere; the write belongs to
whoever holds the ledger. Adding only the `<!-- promised-deliverable: … -->`
marker was also rejected: the validator checks ledger ids against the register
and not the reverse, so a bare marker would pass silently while pointing at a
promise that does not exist, and would then read as a duplicate the moment the
entry landed.

The entry to add, `id = "corpus-browser-foundation-hardening-2026-08-08"`, owner
`guidance/corpus-browser-implementation.md`, state `in_progress` — not
`candidate`, because one prerequisite is open and the record is on no integrated
branch:

| Requirement | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| `durable-architecture-record` | A tracked record states how the non-PDF browser surfaces are built, what will refuse a change, the verifiable sequencing, the ranked risks, the conflicts returned for disposition, and the defect register with each finding's status and each refuted finding's refutation. | `pass` | `guidance/corpus-browser-implementation.md` |
| `artifact-gate-over-the-built-site` | A design-neutral gate drives real Chromium over the built artifact across the five-viewport governing matrix, asserts no visual contract, skips cleanly with a stated reason when no browser resolves, and stays out of `make check`. | `pass` | `tools/tests/corpus_browser_gate.mjs`, `Makefile` |
| `chromium-harnesses-are-run` | The four reader harnesses have a target that builds their data root first and holds them to a recorded pass floor rather than to a zero exit. | `pass` | `Makefile`, `tools/tests/test_browser_harnesses.py` |
| `published-hash-contracts-pinned` | Every published hash key of every instrument is pinned by test before any router cleanup, including the keys that are deliberately input-only. | `pass` | `tools/tests/test_browser_url_contract.py` |
| `shared-shell-blocking-collisions-resolved` | The four selector and plumbing hazards that block a shared shell are resolved with an unchanged rendered DOM: the `#reading`/`#banner` hard-coding, history's `.field`, texts' `.detail`, and `day-missal.css`'s unscoped `body > .site-header`. | `open` — three of four done (`a912e182e`, `bad976039`, `9e980ff5b`); `day-missal.css` is protected liturgy and needs that deliverable's authority | `src/web/browser/shared/browser-core.js`, `src/web/browser/history/history.css`, `src/web/browser/texts/texts.css`, `tools/tests/test_browser_collisions.py` |
| `no-visual-or-product-decision` | The lane changes no visual contract, accepts no screenshot baseline as an oracle, and makes no production change to a protected liturgy asset. | `pass` | `guidance/corpus-browser-implementation.md` |

<!-- promised-deliverable: corpus-browser-foundation-hardening-2026-08-08 -->

The entry above is now in `promised-deliverables.toml`, and this comment is its
one work-register marker. Five requirements pass; the sixth stays open because
`day-missal.css` is protected liturgy and needs that deliverable's authority,
which is the honest state rather than a rounding of it.

## Promised work

### Mary as the New Ark: journey, dogmas, and virginal marriage

<!-- promised-deliverable: gpt-mary-new-ark-journey-2026-08-15 -->

**Corrected, reviewed, installed, pushed, and verified live on 16 August
2026.** The two provider editions now share one catalog
row while retaining their different titles, provider-qualified routes, PDF
bytes, the published GPT web reader, and each edition's own drawings. The GPT
edition replaces its rough wavy-line schematics with a source-first two-panel
graphite atlas and five finely detailed graphite Ark/sanctuary plates.
Reader-facing prose calls the scene 2 Samuel 6 and uses ``2 Reigns'' only when
it explicitly explains the Septuagint title; the older Douay ``2 Kings'' name
is likewise identified rather than silently mixed with modern numbering.

The source-audited study gives a vivid account of the Ark's journey; receives Mary
confidently as its living New-Covenant fulfillment because she bears Christ;
synthesizes exact patristic, saintly, liturgical, and magisterial witnesses;
and shows the four Marian dogmas as the full unfolding of that vocation without
displacing Christ as the covenant's definitive fulfillment.

Joseph and Mary's chastity is neither omitted nor reduced to a negative Uzzah
analogy. Their true virginal marriage receives a positive synthesis centered
on Joseph's commanded reception of Mary, Davidic fatherhood, spousal love, and
ordered guardianship of the divine Presence. Uzzah remains only a bounded
contrast between unappointed handling and obedient service; the study rejects
any implication that marriage is defiling, Mary physically dangerous, or
Joseph's continence terror-driven.

The reviewed and installed GPT PDF is 46 letter-size pages at SHA-256
`0d995ac1d447f53cc55496fa8907c16a7940639b986fee02579b16e87d7164da`;
the generated and installed GPT web edition is byte-identical at SHA-256
`8083f51e35ce1d72fdd306d23c378361e70f778ee27f1a7acaeb915c1e27a2d4`.
The rebuilt and installed 65-page Claude PDF is byte-identical at SHA-256
`7877add8a640a9d2f237eb149e35440bc8c392ce84fe30a24e16a03b54c3d7d0`.
All 46 GPT pages and all 65 Claude pages were reviewed; the atlas and the five
GPT graphite plates received original-resolution checks; the GPT web
equivalence and independent Catholic sanity review pass; and the installed
provider PDFs remain distinct. The current source-first map uses pinned Natural
Earth 5.1.2 and Mapzen Terrain Tiles beneath a project-authored semantic overlay
that distinguishes narrated, inferred, traditional, candidate, regional, and
unknown geography. The Ark and sanctuary captions distinguish commanded or
attested data from unrecoverable form and location.

Content commit `2b9233978bcd8e798467bffaccf699b96031d97a` was pushed to
`origin/main` without rewriting history. GitHub Pages run
[`31957951080`](https://github.com/spincyc/triptych/actions/runs/31957951080)
completed successfully for that exact head. The live
[Mariology catalog](https://mystago.gy/library/mariology.html),
[GPT web reader](https://mystago.gy/web/gpt/theology/mariology/ark-of-the-covenant.html),
[GPT PDF](https://mystago.gy/pdf/gpt/theology/mariology/ark-of-the-covenant.pdf),
and [Claude PDF](https://mystago.gy/pdf/claude/theology/mariology/ark-of-the-covenant.pdf)
each returned HTTP 200. The two deployed PDFs matched the reviewed SHA-256
identities above, and the live catalog contained exactly one shared Ark row
with each distinct provider title and route. All twelve acceptance requirements
pass.

The earlier 42-page GPT artifact `a520adb39130bb3b65a3bd7d92926fbc77126650fdf593d0680fc10bee125843`,
web artifact `3a5e96c2405e1d311acf65ef931a45ebee502e459817f5a744833858ce62d1bc`,
commit `a35dc5cfb82be027256d74c6f2b256f830f1073e`, and Pages run
[`31935618065`](https://github.com/spincyc/triptych/actions/runs/31935618065)
are superseded baseline evidence, not evidence for this correction.

### Corpus browser foundation design

<!-- promised-deliverable: corpus-browser-foundation-design-2026-08-08 -->

**Candidate on isolated branch `ux/foundation` from exact base
`c27d6915319785686d1df6a1401a489aa9921f6f`; no production or PDF change is
authorized and independent acceptance remains open.** A0-A4 inventory the
complete public surface, synthesize checked
scholarly-interface research, establish the site-wide corpus-browser vision,
define one visual system with Reader/Catalogue/Instrument archetypes, and
specify shared navigation, bounded synthetic Jump behavior, typed contextual
navigation, and shell behavior. Production global typed search remains J0-J2.
The accepted Liturgical Instrument remains the liturgy-specific reference and
is not reopened. `PROJECT-WORK.md` and `promised-deliverables.toml` remain the
fail-closed operational authorities; durable design and execution detail lives
in `guidance/corpus-browser-vision.md`, `guidance/corpus-browser-roadmap.md`, and
`build/agent-continuity/corpus-browser-foundation.md`. One standard external-
review ZIP will present the committed candidate; creating it will not mark the
foundation accepted or authorize production implementation, integration, or
public cutover.

### Corpus browser Wave 1 real-data design

<!-- promised-deliverable: corpus-browser-wave-1-design-2026-08-08 -->

**Complete as a Wave 1 visual and product-design deliverable; production
remains unimplemented.** Independent review of Wave 1 at exact head
`e42b9287485a5a6d18ad8a528ab0f0f3f0024ff9` accepted C0 Home, C1
Publications, D0 Reader, and E0 Catena as design contracts. Independent review
of the corrected checkpoint at exact head
`ecbd93a0575c4b890cc814af7cd20d01f5af7beb` then recorded **F0 Source
Library — ACCEPT** and **Shared non-Liturgy shell — ACCEPT**, closing the two
remaining design-review gates. Accessibility and resilience remain accepted
production requirements with production proof outstanding. Browser print
remains accepted only as a non-canonical fallback.

The original branch started from exact `origin/main` base
`c27d6915319785686d1df6a1401a489aa9921f6f`. Its task-specific dispatch
superseded the former integration-branch precursor, so no
`corpus/foundation-integration` ancestry is claimed. Accepted knowledge and
artifacts were carried selectively from Codex foundation SHA
`3b5938a0dba88831763ec09c762ae1572007a27e` and Claude foundation SHA
`af2c9613ccda48679face4e43f59c002f93056ef`.

The durable design authority is
[`guidance/corpus-browser-vision.md`](guidance/corpus-browser-vision.md); the
execution, evidence, and disposition register is
[`guidance/corpus-browser-roadmap.md`](guidance/corpus-browser-roadmap.md).

C0, C1, D0, and E0 were not reopened by the correction checkpoint. The
accepted F0 contract distinguishes Work/Edition ownership from the
Artifact/Segment relation controlling Passage text. For the reviewed
one-Passage Edition, it retains the selector, exact `Passage 1 of 1`, and
rights, provenance, and inspection-scope truth while omitting impossible
Previous and Next actions. The accepted wide shell has exactly one
current-location signal, no duplicate wide domain identity, and Browse as a
bounded destination control distinct from Jump; the compact shell preserves
domain identity, Menu, Jump, target sizing, and no document-level overflow at
393 and 320 CSS pixels. The correction changed no
production behavior, protected Liturgy, canonical PDF, production route or
hash contract, release binding, public mapping, or deployment state.

**Evidence and reviewed handoff.** The immutable reviewed record is
`build/agent-handoffs/20260809T000346Z-corpus-wave-1-design-review/`, with its
matching one-root ZIP. Its browser report covers 83 real-route cases and 1,979
assertions: 1,917 pass, 62 disclosed inherited findings are non-gating, and no
gate fails. It contains 83 main captures, all 25 required before/after pairs,
one 236-page Reader print PDF, and all 236 page rasters. The bounded correction
is complete at design/test head
`c66c143643ff75a6cd54afdbe1fcd6eac0aca1b6`. Its full capture run covers 85
real-route cases and 2,296 assertions with zero gating failures. The 64
non-gating findings are 52 inherited nested-`main` findings, eight before-state
useful-content findings, two before-only narrow-overflow findings, and two
inherited Reader no-JavaScript overlay limitations. The correction package
`20260809T014145Z-corpus-wave-1-review-fixes` is superseded for handoff-protocol
defects. Independent review of the fresh immutable package
`build/agent-handoffs/20260809T021953Z-corpus-wave-1-review-fixes/` and its
matching ZIP at packaged head `ecbd93a0575c4b890cc814af7cd20d01f5af7beb`;
recorded the F0 and shared-shell ACCEPT dispositions. The ZIP SHA-256 is
`d5fde51b14f143db05f762178896284d7768c0b2a11fc222fc2b32da63e22062`.
The exact reviewed-base-to-head range has zero changes under protected
`src/web/browser/liturgy/` and `pdf/`.

The following findings are non-blocking only for these design dispositions;
none is waived, satisfied, or reassigned by acceptance. The inherited
nested-`main` defect remains a production blocker. Reader table-cell reflow and
full no-JavaScript behavior remain production obligations. Comprehensive
Menu/Browse destination-activation tests remain an implementation and
hardening obligation. The prototype stylesheet used 8,171 of its 8,192-byte
gzip-9 ceiling, so it provides no meaningful implementation headroom or
production CSS budget. The stale Fortescue Artifact note remains open and may
be corrected only by its proper source-data authority owner.

For this program, Codex owns product and visual design, correction evidence,
and independent product review. Claude owns production implementation, coding,
and implementation testing on named lanes. Neither role may cross declared
single-owner boundaries or accept, merge, or deploy its own work by implication.

The F0 and shared-shell design-review dependencies are satisfied. F1 Sources is
eligible only for separate owner-authorized production dispatch; final
shared-shell cutover remains blocked on clean foundation plumbing and explicit
cutover authority. E1 Catena may proceed
within its existing independent boundary; Home/Publications/Reader
implementation still requires clean shell ownership. Production implementation
remains owned by the appropriate Claude lanes. This acceptance does not
authorize merging the disposable prototype overlay, merging or pushing
`main`, deployment, public cutover, a protected Liturgy change, or a canonical
PDF change.

### Live Reader — Ritual Flow & Orientation

<!-- promised-deliverable: liturgy-reader-live-ritual-flow-2026-08-07 -->

**In progress as a new production refinement phase against the independently
accepted live canonical Day and Propers readers.** The completed migration and
same-path cutover are not reopened. This phase protects the accepted first
viewport and Instrument foundation while improving sustained-reading
orientation, making Contents a current-place map, and restoring hierarchy
between principal ritual action and source-owned rubric, provenance, or
conditional/reference material.

The implementation may expose existing semantic and renderer state through
narrow shared presentation hooks. It may not manufacture liturgical
applicability, locality, selection, source, translation, or content. Search,
Study, Compare, print redesign, public-navigation redesign, candidate/oracle
cleanup, source/translation/recension expansion, and a new visual direction
remain separate and unauthorized. Exact baseline, decisions, checkpoints,
Pages runs, and the independent-review stopping point live in
`build/agent-continuity/liturgy-reader-visual-plan.md`.

### Liturgical Instrument public cutover

<!-- promised-deliverable: liturgy-reader-instrument-public-cutover-plan-2026-08-06 -->

**Complete; the canonical Day and Propers URLs serve the independently accepted
Liturgical Instrument, public navigation is unchanged, and retained candidate
and oracle cleanup is deferred.** Planning began from synchronized accepted-
integration boundary `7b7044dea7f5c35a2d32ff85f26eb5b182bf40ef`. It inventoried
the canonical `liturgy/day.html` and `liturgy/index.html` contracts against
the accepted `liturgy/day-reader.html` and `liturgy/propers-reader.html`
implementations, selected same-path promotion as the smallest reversible
mechanism, made the disclosed date-dependent Day gate deterministic without a
product change, and produced exact patch, rollback, acceptance, deployment,
and cache-window procedures.

Independent review accepted source-level same-path promotion behind the
unchanged canonical filenames, the rollback and static-hosting model, the
canonical-route and visual-oracle gates, and the deterministic Day fixture. It
also fixed the compatibility decisions: Roman 1962 is the intentional empty-Day
default; `why=1` and every held territorial branch are preserved; Propers uses
stable `cycle`, `alternative`, and `translation-witness` keys; retained
candidates are source-static noindex; visible controller wording is route-
neutral; and counterpart/context navigation belongs in Details without a fifth
primary action. Compatibility implementation
`3f3949617a04ffa68a1070058d0f7bc5ac74dc93` closes those contracts on the
authorized candidate/shared seams. Pages run `31148986910` succeeded for that
exact commit. Day passes 40/40, Propers 32/32, the shared shell 18/18, and
governed visual assertions 24/24 over 113 captures. Production integration,
compatibility closure, and their durable handoffs are independently accepted
and complete.

Planning checkpoint `c7124de25` records the route, state, navigation, static-
hosting, cache, mechanism, rollback, and execution-gate maps. Test-only commit
`5e1b82b51` proves and removes the disclosed wall-clock dependency while
keeping the first-visit URL empty. The obsolete first patch was superseded
after gate repair by the accepted 19-path patch. Its prospective 230/230 focused
Python, 40/40 Day, 32/32 Propers, 18/18 shared-shell, and 24/24 governed
Instrument gates were repeated successfully in the promoted real tree before
commit. The planning package remains at
`build/agent-handoffs/20260806T212148Z-liturgy-reader-instrument-public-cutover-plan/`
and the removed compatibility package remains recoverable from its historical
introduction commit `e69d91ffff5823dc2970f867f1be8c9eb5b6363b`.

Independent post-deployment review passed all nine final questions and accepts
the public cutover as complete. Exact cutover SHA
`9b5f21c0ca26bf02af03d207ddd2617021e16fb3` owns qualifying successful Pages
run `31175722949`. Immediate live verification passed 936/936 across 36
original-pixel states; ordinary-cache verification passed 216/216 after 613
seconds without mixed-generation behavior. The removed immutable execution
handoff remains recoverable from historical introduction commit
`1d60b49bcf2a46e5ee43d6326af3e13a43265b72`; its ZIP SHA-256 was
`06752126a3a3235a342f54ec08811faaf4fc2622924008c4362dda519624c410`.
Canonical Day and Propers now serve the accepted Instrument without redirects.
Public navigation was not redesigned; retained candidate and oracle routes
remain intact and nonindexable, and cleanup is deferred and unauthorized. The
governed full gate remains non-green only at the unrelated stored-example
transcript replay; no transcript was recaptured or blessed.

### Liturgical Instrument production integration

<!-- promised-deliverable: liturgy-reader-instrument-production-integration-2026-08-06 -->

**Complete; production integration is independently accepted and its exact
reviewed handoff is durably archived in Git history rather than the current
tree. The separately reviewed public cutover is also complete;
public-navigation redesign remains outside both phases.**
Independent Round 1 accepted the
Liturgical Instrument visual foundation and all seven correction dispositions.
Production integration begins from `b3ae6bddaab631661d342380f61365d851be160c`
through four bounded units: PI-A inventories the accepted hooks and selects the
smallest shared presentation seam; PI-B integrates the shell and Day
Read/Missal presentation; PI-C proves Propers Read/Browse parity; and PI-D
captures the full parity matrix, runs the governed checks, and assembles an
immutable integration-review candidate.

The completed inventory selects a new last-loaded, candidate-scoped
`src/web/browser/liturgy/reader-instrument.css` layer. This keeps public-loaded
`day-missal.css` unchanged and preserves `reader-shell.js`, the M1 state and
adapter owners, production renderers, Ordinary seating, invalid-state failure,
semantic-location restoration, focus, race ownership, and the four one-step
actions. Stable masthead and action-label hooks are added to the two production
candidate HTML files. Only generation-safe presentation composition may touch
the Day or Propers adapters: the authoritative Day commit exposes its current
mode as a styling attribute, and renderer-owned absence nodes may be grouped or
moved without replacing their text or semantics. The accepted comparison
prototype remains unmodified and available as the parity oracle. That seam is
now implemented in both unlinked candidates. The extended Chromium harness
passes 19/19 assertions over 100 captures and includes 23 exact
prototype/production pairs covering Read, Missal, partial coverage,
postconciliar coverage, Propers, all open surfaces, deep scroll, 200% text,
forced colors, reduced motion, and keyboard focus. The accepted 768×1024
636-pixel/~75-character measure is exact; production mobile Missal principal
text is 3.43 pixels earlier than the accepted oracle and otherwise retains the
same 351-pixel plane and action geometry.

Successful deployed correction parity remains Pages run `31109086658` for
`c388ab42dfc4f5c7d49abc71596d6bb511af5742`. Later runs
`31110517661`, `31113461987`, and `31114653517` each passed repository-owned
build/upload work and then failed at GitHub deployment polling; none is claimed
as successful. The production-integration deliverable remains open until its
own evidence, deployment record, and independent integration disposition are
complete. The implementation checkpoint is not represented as deployed until
its own push has a successful Pages result and direct asset verification.
Implementation commit `3cd46072b164ff39b00639bb67ad6b8943a255dc` is pushed
to `origin/main`. Its clean-tree full gate reached only the governed unrelated
example-replay divergence: 200 examples, 188 replayed, 23 divergent, 35 known
stale, 6 never run, and 6 unrunnable here. It exits 2 and is not represented as
green. As of 2026-08-06T18:04:26Z, GitHub had not materialized the automatic
Pages run for this push in the Actions API; this is recorded as a pending
workflow event, not a deployment success or failure.
Continuity checkpoint `e35f81c1e67c744aead0e4eaa73e079516751e66` is also
pushed. As of 2026-08-06T18:08:35Z GitHub likewise had no Actions record for
that head. Direct deployed Day and Propers candidates remain HTTP 200 at the
prior artifact, which does not contain `reader-instrument.css`; deployed
integration parity therefore remains explicitly open.
GitHub later materialized automatic run `31125352169` for implementation commit
`3cd46072b164ff39b00639bb67ad6b8943a255dc`, but at
2026-08-06T18:27:03Z it had remained queued for more than 15 minutes with no
runner or repository step started. This is a queued external-state result, not
a successful or failed deployment; deployed parity remains open.
The next delayed automatic run, `31125898045`, succeeded for exact intended
production commit `5444d89fc9b379a1babef5b2220323fe1508b2b3` at
2026-08-06T18:29:55Z. Every repository build, verification, upload, and deploy
step passed. Direct Day, Propers, and both accepted oracle routes return HTTP
200; Day/Propers reference the Instrument stylesheet, the oracle routes remain
noindex, and deployed Instrument CSS, Day/Propers JavaScript, and accepted
oracle CSS/JavaScript byte-match source. Deployed production-integration parity
is complete. The deliverable remains a candidate solely for independent
integration review; public navigation and cutover remain unauthorized.

Independent production-integration review passed all six requested questions:
Day parity, Propers parity with canonical Browse retained, responsive shell and
accessibility behavior, reading and ritual geometry, frozen behavioral/source
ownership, and final integration disposition. No product, visual, evidence,
harness, or deployment correction was requested. The only closeout finding was
that the exact reviewed handoff remained ignored locally.

Under the review's path-bounded force-add authority, archival commit
`8c6e1270f692ca4136f2f6a60002bacd3af0440c` pushes the byte-identical reviewed
directory and ZIP. All 216 manifest entries verify, the archive has one
top-level directory, and its SHA-256 remains
`ebf0361309ac33b4580cbb535e4bbd3eabd144756e6c078aa140e716c748f05f`.
The canonical continuity file carries the complete review and Codex response.
Production integration and durable handoff closeout are therefore complete.
At that integration boundary the Day browser remained 33/34 only at its
date-dependent expectation; the subsequent deterministic cutover fixture and
canonical execution pass 40/40. The full gate remains non-green only at
unrelated example transcript divergence. The separately reviewed public
cutover is now accepted and complete; public-navigation redesign was not part
of it.

### Liturgical Instrument visual correction accepted

<!-- promised-deliverable: liturgy-reader-instrument-correction-2026-08-05 -->

**Complete; independent Round 1 acceptance authorized the now-complete
production integration, but did not itself authorize navigation or cutover.**
Liturgical Instrument is the
accepted production visual foundation. Quiet Folio and Contemporary Reader
remain frozen comparison references, and the accepted visual and behavioral
seams are not reopened absent a concrete production-integration conflict.

The bounded correction owns seven findings: integrate the persistent controls
with the reading composition; advance the first principal Missal text; remove
the empty Read gutter; constrain the 768-pixel portrait measure; subordinate
partial and postconciliar coverage warnings to available text; replace or
simplify the provisional masthead mark and progress treatment; and finish
mobile ritual spacing and narrow division-title wrapping. The canonical plan,
review mailbox, measurements, checkpoint record, and resume state are tracked
at `build/agent-continuity/liturgy-reader-visual-plan.md` under this task's
explicit build-tree exception. Work units A–C now implement and measure the
bounded visual corrections: one 39.75rem Read axis, earlier Missal action,
integrated rail/dock, authored masthead, consolidated warnings, tighter ritual
rhythm, and deliberate 320-pixel wrapping. Work unit D now supplies the full
matrix, measured before/after package, honest governed-check record, verified
Pages deployment, and an immutable tracked handoff now retained only in
historical introduction commit
`50288ddf9759f56e8a25e4907d8de25e27e25e8f`.
Independent review round 1 passed six of seven original findings and confirmed
the direction, typography, ritual grid, warnings, masthead, and Ordinary/Proper
composition. It retained the original shell blocker only at 1024×768 and added
the related 200%-text mid-word label reflow blocker. The bounded follow-up now
uses the opaque square edge dock immediately below the 72rem rail breakpoint
and a labeled 2×2 dock only at extreme root-font reflow. The 54-capture run
passes 15/15 assertions, including end-content reserve, whole labels, accessible
names, target size, and overflow. Correction commit
`ab89758e3f3ee165e0141e3605be88051450134b`
is pushed. Its first Pages run passed every build/verification step but timed
out while GitHub held the deployment queued, so deployed corrected-asset parity
remains open and is not claimed. A second automatic run for continuity
checkpoint `c6b7f7f0a79468cfa1a503235044c92bd88c27b2` again built and uploaded the
verified artifact, then timed out only in deploy-pages polling; the durable
continuity record owns both exact stops. A third automatic run again passed all
repository-owned build/upload work and was canceled only when the job reached
its 15-minute ceiling during deploy polling. The following immutable-handoff
push succeeded as Pages run `31109086658`; direct Day/Propers routes are HTTP
200/noindex and deployed CSS/JS byte-match source. The removed final narrow
immutable re-review handoff remains recoverable from historical introduction
commit `4daf7d8a1e1c509edb81a738cc71223170bbbd2d`.
Independent Round 1 acceptance passed shell continuity, 200% labeled reflow,
and absence of accepted-geometry regressions. It independently verified the
ZIP, all 109 manifest entries, candidate/source CSS parity, and all corrected
original-pixel screenshots. Production integration may now begin through the
shared presentation seam; it must stop for independent integration review
before any separately authorized public cutover. Pages run `31110517661` for
post-deployment evidence commit `4daf7d8a1e1c509edb81a738cc71223170bbbd2d`
failed at deployment polling and is not represented as successful; successful
deployed parity remains owned by run `31109086658` for
`c388ab42dfc4f5c7d49abc71596d6bb511af5742`.
The acceptance-record push at `1608f0ee0ee61df956247072a91647147548c5ad`
passed every repository-owned Pages build/upload step, then run `31113461987`
failed after 600 seconds of `deployment_in_progress` polling. Direct prototype
routes remain HTTP 200/noindex and their deployed CSS/JS still byte-match the
accepted source; the new run is not represented as successful.

Accepted M1–M3 and W3 state, assembly, renderers, Ordinary seating, failure,
location, focus, race, action-reachability, and isolation behavior remain
binding. This completed correction does not add Study, Compare, search, Propers
Missal, sources, editions, recensions, translations, or public links, and it
does not change `liturgy/day.html` or `liturgy/index.html`.

### Liturgy reader visual-reset direction candidate

<!-- promised-deliverable: liturgy-reader-visual-reset-candidate-2026-08-05 -->

**Complete as a direction-selection study; Liturgical Instrument selected.**
The completed M1–M3 and W3 records remain authoritative for state,
production assembly and rendering reuse, fail-closed behavior, focus and
semantic-location restoration, responsive access, and render-race ownership.
They were never a finding that the beige card, enlarged mobile-style command
bar, improvised glyphs, typography, spacing, or desktop composition constituted
a finished or world-class visual reader.

This distinct visual-design work item compared Quiet Folio, Liturgical
Instrument, and Contemporary Reader over one shared semantic DOM and interaction
foundation. It uses real production Day Read/Missal and Propers Read content at
unlinked, noindex prototype routes, while preserving the accepted state,
calendar, Ordinary seating, Proper rendering, source, and coverage boundaries.
Its external review selected Liturgical Instrument. The work does not reopen
the completed Day Missal engineering deliverable, alter public Day or Propers,
start Study/Compare/search, or authorize public cutover.

The visual-reset candidate was implemented and independently reviewed, with
**Liturgical Instrument selected as the production visual foundation**. Quiet
Folio is the calmest editorial leaf; Liturgical Instrument adds an edition-neutral
ritual cue grid, disciplined divisions, and a speaker/action gutter for actual
following; Contemporary Reader supplies the most compact application chrome
and polished title-led Propers Browse flow. All three are query-selected
presentations over the same HTML, SVG icon set, shared shell controller, and
accepted Day/Propers production adapters. The selection favors Instrument's
continuous ritual legibility. Folio and Reader remain frozen comparison
references rather than ingredients for a merged compromise. The review also
found seven bounded visual blockers, now owned by
`liturgy-reader-instrument-correction-2026-08-05`; selection does not make the
foundation world-class or authorize production integration.

The current evidence contains 52 same-run comparison captures at the required
desktop, tablet, mobile, enlarged-text, forced-color, reduced-motion, keyboard,
deep-scroll, surface, partial-coverage, and before/after states. Twelve focused
Chromium assertions pass with no console, failed-request, HTTP, overflow, or
unnamed-interactive-node result; a 26-page PDF is retained only as a print smoke
check, not a print redesign. Exact hashes prove the public Day and Propers
routes, both accepted candidates, shared shell, M1 state seams, production
seating, and accepted adapters unchanged. The implementation is this candidate
commit; its immutable visual-review handoff was created after the validated
push. The direction-selection decision is complete. Corrected visual review,
production-integration execution, and every public-cutover decision remain
open under the separate correction deliverable above.

### Liturgy Day Missal-mode W3 integration accepted

<!-- promised-deliverable: liturgy-day-missal-w3-candidate-2026-08-05 -->

This task extends the accepted internal Day reader at
`liturgy/day-reader.html` with the next bounded W3/M3 production-integration
slice: Read remains the default appointed-Propers view, and Missal presents the
continuous production Ordinary with those same propers seated at their actual
semantic locations. The candidate must reuse the accepted M1 Day state,
production calendar assembly, Ordinary data and renderer, Ordinary seating,
and shared Proper renderer. It may not create a second liturgical sequence,
renderer, seating engine, event-order engine, URL parser, or public route.

**Accepted** — the internal W3 Day Missal-mode integration has passing
implementation and independent external-review evidence. Its contract includes
Roman 1962 and postconciliar parity,
fail-closed Ordinary language and Eucharistic Prayer handling, explicit
coverage and absence,
semantic-location preservation across Read/Missal and history transitions,
race ownership, responsive and accessible interaction, continuous Missal
print, performance measurement, and production isolation. Study, Compare,
Propers Missal mode, search, new recension or source coverage, public route
cutover, and redesign of the accepted shell or complete print system remain
out of scope.

The implementation base is
`c4c071d6ba962524487bc8f4c6a4b781981851c7`. The initial candidate, two bounded
corrections, three immutable handoffs, and their successive review dispositions
remain recorded below as the durable audit trail. This acceptance does not
amend the accepted M1, M2, M3, or Propers Read records.

External review of implementation
`a1221755d4fac2a6b9a009a91b99cd1da82eee9e` and immutable handoff
`20260805T145914Z-day-missal-mode-integration` returned **changes requested**.
It passed the production-renderer, seating, edition, option-validity,
ergonomics, isolation, and scope boundaries, but identified three bounded
acceptance blockers: non-ready outcomes can retain history-dependent mode
chrome; an inline Eucharistic Prayer change replaces the focused radio without
restoring its semantic equivalent; and direct-load evidence can observe an old
ready flag before the new document's render commits. Correction work is limited
to deterministic outcome presentation, inline-option focus restoration, and
generation-safe browser assertions and replacement captures. The candidate and
its independent external-review requirement remain open; no acceptance,
closeout, public cutover, or deployment is authorized by the correction work.

The bounded correction is now implemented and locally proven, but remains
**pending independent correction review**. Every render outcome commits one
mode presentation (including a neutral, unchecked presentation for invalid
`ordinary` state); invalid, deferred, unresolved/territorial, and unrenderable
outcomes carry distinct diagnostics; and stale navigation, location, focus,
metadata, and selection state is cleared before an outcome commits. Keyboard
changes among the postconciliar Eucharistic Prayers restore focus to the newly
rendered checked radio without losing the semantic reading location. The
browser harness now distinguishes fresh documents by a unique non-semantic
query nonce and document token, and same-document transitions by an exact hash
and a greater committed render generation, followed by the UI's animation-frame
boundary. The complete browser and print evidence was regenerated with that
harness. These results resolve the three correction requirements for re-review;
they do not accept or close the candidate.

External review of correction
`ce5fce8364d24156e41c444c43673e7de31555d8` and immutable handoff
`20260805T183500Z-day-missal-mode-corrections` returned a second, narrowly
bounded **changes requested** disposition. The substantive product corrections
passed review: deterministic outcome chrome, neutral invalid-Ordinary state,
distinct failure classes, inline-option focus restoration, generation-safe
document navigation, and production isolation remain accepted correction
evidence. Acceptance is still blocked because the Chromium harness waited only
two animation frames while inherited smooth scrolling could remain in flight,
and because duplicate `ordinary` keys were not exercised directly in Chromium.
The evidence-settlement correction is limited to animation-frame scroll/target
stability, settled default- and reduced-motion Eucharistic Prayer focus proof,
both duplicate-key orderings from fresh and transitioned states, wholly
regenerated evidence, and a new independent handoff. Product reader and shared
shell behavior remain unchanged unless settled testing proves a real defect.
The candidate, completion count, and external-review requirement remain open.

The evidence-settlement micro-correction is now implemented and locally
proven, but remains **pending independent external review**. Committed-render
synchronization still requires exact document tokens and generations; a
separate animation-frame loop now requires five stable scroll/target/focus
frames, viewport intersection, cleared pending navigation, and a bounded
diagnostic timeout before assertion or capture. Default-motion keyboard changes
through EP I, III, IV, and II and a separate reduced-motion change preserve the
settled semantic event and checked-radio focus. The stabilized test exposed one
local Day-adapter defect: the correctly focused checked radio could settle above
the viewport. The adapter now aligns that inline option group deterministically
after semantic restoration, leaving the shared shell and global scrolling rules
unchanged. Both `ordinary=0&ordinary=1` and `ordinary=1&ordinary=0` now produce
neutral, unchecked mode chrome on fresh loads and transitions from Read and
Missal. All browser and print evidence was regenerated; the public routes,
Propers candidate, shared shell, M1 seams, seating, and production data remain
unchanged. These results satisfy the bounded proof requirement for re-review;
they do not accept, close, deploy, or cut over the candidate.

Independent external review now **accepts and closes this internal W3 Day
Missal-mode slice** at micro-correction
`86a9816c1bffdcbdd09469f5f8d005c666a8045e`; every blocking review question is
resolved and no further handoff is required. The complete reviewed sequence is
candidate `a1221755d4fac2a6b9a009a91b99cd1da82eee9e`, first correction
`ce5fce8364d24156e41c444c43673e7de31555d8`, and the accepted micro-correction
above, with immutable handoffs
`20260805T145914Z-day-missal-mode-integration`,
`20260805T183500Z-day-missal-mode-corrections`, and
`20260805T201722Z-day-missal-mode-evidence-corrections`. Acceptance covers
reuse of the production Ordinary presenter, Proper renderer, M1 event stream,
and single seating path; Roman 1962 and postconciliar structures;
deterministic fail-closed state; semantic location, history, and render-race
ownership; settled inline Eucharistic Prayer keyboard focus; responsive,
accessibility, performance, and print evidence; and production isolation. It
does not authorize public-route cutover, public links, Propers Missal mode,
Study, Compare, search, source or recension expansion, or print redesign.

### Liturgy Propers Read W3 integration accepted

<!-- promised-deliverable: liturgy-propers-read-w3-candidate-2026-08-04 -->

**Accepted** — the W3 Propers Read integration enters the same production
reader shell as the accepted Day candidate, preserves current valid formulary
semantics through the M1 Propers state and production Proper renderer, leaves
missing identity unresolved, fails closed on invalid state, preserves cycles
and alternatives independently, requests translation witnesses only when
formulary-specific translated material requires a choice, and remains isolated
from the public Day and Propers routes.

External review first requested bounded Browse witness, Browse-race, tracking,
and handoff corrections from candidate
`b0b1e5b63ba4a1d389b53276fa0bf9944c0ee909` and handoff
`20260804T212821Z-propers-reader-shell-integration`. It then accepted correction
`1e4587dfe04a11c18e996a16f7fbbdb54bc744a4` and immutable handoff
`20260804T225215Z-propers-reader-shell-corrections` after manifest verification.
The reviewed evidence records 84 focused M1/shell/Day/Propers tests, 90
public-alpha/gallery tests, and respectively 27, 25, and 18 Chromium assertions
for Propers, Day, and the shared shell. The exact shared-shell hashes are
`bf1c062453f8fcfd5a68c1fe30e31aca89ea1a3c8adeef9a5525d8081ae8c707`
for `reader-shell.js` and
`e7195cd86ed4fc4a8455e97369702239eb22d709a13d3d8462d7759c01fe814a`
for `reader-shell.css`.

Production-isolation evidence confirms that public Day and Propers, the
accepted Day candidate, navigation and selectors, M1 semantics, production
liturgical and generated data, and public URL behavior remain unchanged. The
approved example baseline remains the same 23 unrelated pre-existing records
and the same two promised-deliverable commands; acceptance changes only the
candidate count from 18 tracked, 12 complete to 18 tracked, 13 complete.
Public cutover, Missal, Study, Compare, search, and recension expansion remain
deferred. Excess cycle-choice print whitespace remains non-blocking debt for a
later print-refinement workstream.

### Liturgy Day reader-shell M3 accepted

<!-- promised-deliverable: liturgy-day-reader-shell-m3-candidate-2026-08-04 -->

The first W3 integration slice extracts the accepted quiet persistent reader
shell into a reusable production foundation and connects an unlinked, noindex
Day Read-mode candidate to the existing production assembly and rendering path
through the accepted M1 reader-state boundary. The candidate preserves
Read-compatible legacy URL meaning, fails closed on invalid explicit state,
and discloses later-mode state with an equivalent link to the unchanged live
Day route rather than silently dropping or partially rendering it.

This was an **M3 candidate pending external review**, not a production cutover.
The live Day and Propers routes, public navigation and selectors, M1 semantics,
liturgical and calendar data, and generated public data remain outside the
implementation boundary. Missal, Study, Compare, Propers integration, search,
and public release remain deferred.

The candidate is implemented at the unlinked `liturgy/day-reader.html` build
route. `reader-shell.js` and `reader-shell.css` contain only the accepted
persistent action bar, modal lifecycle, focus and scroll restoration, semantic
Contents tracking, responsive sheets, safe-area behavior, and print removal.
The separate Day adapter parses and validates M1 state, calls the existing
calendar assembly and M1 Day adapter, and renders the selected real production
Proper with the existing shared renderer. It supports date, missal, Bible,
oration language, and readable-formulary state; it preserves later-mode state
and links it intact to `day.html`, and it fails closed on invalid explicit
values.

Focused static, M1, current-route, Ordinary, public-alpha, and real-Chromium
checks cover both production-backed M1 Day fixtures, a readable displaced
formulary, typed partial coverage, invalid and deferred state, all four modal
surfaces, 320-pixel and 200% reflow, accessibility, deep-scroll reachability,
Back, lazy Details, print, and live-route parity. The immutable external-review
handoff is `20260804T154620Z-day-reader-shell-integration`. M3 remains a
candidate until external review accepts it.

External review accepted the W3 architecture and requested three bounded
corrections before M3 acceptance. The correction distinguishes inactive latent
Ordinary, rubric, and why preferences from active later-mode requests; clears
all selection-specific state before every render attempt so rejected,
unresolved, deferred, or failed navigation cannot expose an earlier result;
restores exact weekday presentation from the assembly model; and keeps raw
source-hook coordinates out of reader-facing Details. The compact correction
handoff is
`20260804T173010Z-day-reader-shell-integration-corrections`. M3 remains a
candidate pending correction review; the live Day and Propers routes remain
unchanged.

M3 is now **accepted**. Accepted — the production Day Read candidate reuses
the existing assembly and Proper renderer behind the shared persistent shell,
preserves Read-compatible legacy state, explicitly defers later-mode state,
fails closed across invalid and superseded asynchronous transitions, and
remains isolated from the live Day and Propers routes. The final serial-token
micro-fix is `c604edb8a1fffb1e5c0981798800ecb801258e7c`; deterministic Chromium
tests release delayed valid, malformed, invalid-destination, and history
requests only after the newer outcome is ready, then prove that identity,
Proper text, Contents, Date, Details, semantic state, and render counters do
not change.

Acceptance evidence comprises original candidate
`45a6b76249e015f68830495ca2971e9dbc4a4e14`, correction
`d0872545ccc92106cb457b448f37201381c5bb2d`, the final micro-fix above,
handoffs `20260804T154620Z-day-reader-shell-integration` and
`20260804T173010Z-day-reader-shell-integration-corrections`, the original W3
changes-requested review, and the W3 conditional-acceptance disposition. M3
acceptance does not replace or redirect live Day, integrate Propers, expose
public navigation, begin later modes, authorize public cutover, or begin the
1956–1960 recension.

### Liturgy reader-shell M2 accepted

<!-- promised-deliverable: liturgy-reader-shell-m2-candidate-2026-08-03 -->

The first W2 milestone is a visible, interactive, responsive shell prototype,
not a production-route integration. It will live in an unlinked nested
`src/web/browser/liturgy/prototypes/reader-shell/` route, which the existing
top-level-only public browser copier excludes. The candidate must reuse the
current Proper renderer, keep Day and Propers as distinct entrances to one
shared shell, compare quiet persistent and scroll-reveal reachability, and
measure wide, intermediate, mobile, 320-pixel reflow, accessibility,
performance, and print behavior. It may use clearly marked M1 contract-only
fixtures for Compare and unresolved-choice layout, but it must not implement
later semantic engines or change public generated data.

The candidate now has one shared shell, persistent and scroll-reveal variants,
real-renderer Day and Propers states, layout-only later-mode fixtures, semantic
Contents, a coherent Study apparatus, 94 responsive review captures, a tagged
four-page print review, and focused static and real-browser coverage. The
measured decision recommends the quiet persistent shell: every global action
remains one activation away at deep scroll while the shell occupies about
58–59 CSS pixels and causes no measured layout shift. The immutable handoff is
`20260804T101952Z-liturgy-reader-shell-prototype`.

External review of candidate `68becc59b396aca830c233b88ec74991563603d1`
in handoff `20260804T101952Z-liturgy-reader-shell-prototype` accepted that
persistent-shell direction and the shared Day/Propers model, but its *M2
prototype changes-requested disposition* required three bounded corrections.
Correction `75234e72c402f0b25a681fbe074da70d895f7274`, reviewed through handoff
`20260804T142747Z-liturgy-reader-shell-corrections`, removed complete-state
diagnostic noise, eliminated auxiliary-surface overflow and raw
machine-shaped Study output, and distinguished temporary Details from pinned
wide-desktop Study and reversible mobile Study sheets.

Accepted on 4 August 2026. The *M2 responsive reader-shell acceptance and
closeout disposition* records: **Accepted — the quiet persistent reader shell
is the M2 direction. Complete Read states are free of diagnostic noise, all
auxiliary surfaces reflow without internal horizontal scrolling, and
temporary Details is distinct from wide-desktop pinned Study and mobile Study
sheets. Production Day and Propers routes remain unchanged.** Focused shell,
M1, current-route, public-alpha, Chromium, print, syntax, registry, and
whitespace checks passed. The repository example comparison preserves the 23
pre-existing divergences and changes only the same two promised-deliverable
rows from `16 tracked, 10 complete` to `16 tracked, 11 complete`; no transcript
was modified or recaptured. Scroll-reveal remains prototype evidence only.
M2 acceptance does not start M3, W3, W4, W5, or production integration, and it
does not change M1 semantics, current URLs, calendar or liturgical data,
search, semantic comparison, or recension coverage.

### Liturgy reader-state M1 accepted

<!-- promised-deliverable: liturgy-reader-state-m1-2026-08-03 -->

The first W1/W9 integration slice defines one versioned, DOM-free semantic
reader-state and legacy-URL contract for the distinct Day and Propers
entrances. Production-backed and explicitly non-public synthetic fixtures hold
identity, calendar result, semantic event order, Proper and Ordinary seating,
text selection, provenance, typed coverage and absence, unresolved choices,
and Compare anchors across Day, Propers, and `mass-today --expanded` without a
second liturgical engine or a visible production change.

Accepted on 3 August 2026. The implementation at
`259573d393cd6a6bac09fc751ac1d14ec9477853`, the reviewed cycle and validation
correction at `c6b8070ae76e75153448895a19a0b916c18806ea`, and the final
property-presence micro-fix at `c1a590f5854215d68d167d9040e188f41762663e`
preserve Propers cycle alternatives and make explicit `sourceHooks` fail
closed unless they are arrays. The external review dispositions *M1 liturgy
reader-state contract*, *M1 reader-state corrections*, and *M1 acceptance
closeout count delta* accepted the resulting contract; the focused suite
passed all 38 tests. The full repository gate remains red only at the approved
23-entry example baseline and the same two promised-deliverable captures, whose
sole authorized closeout change is `15 tracked, 9 complete` to
`15 tracked, 10 complete`. No transcript was recaptured. The deployed Day and
Propers routes still do not load either M1 module, and this acceptance does not
begin W2, W3, or W7 or integrate visible reader behavior.

### GPT deep-research redevelopment

<!-- promised-deliverable: project-gpt-deep-research-redevelopment-2026-07-29 -->

The maintainer identified substantive underdevelopment—not merely stale dates
or presentation—in five GPT publication leaves: the 1962 Tenth Sunday after
Pentecost; Years A, B, and C of the postconciliar Eighteenth Sunday in Ordinary
Time; and *Catholic Exorcism: History, Discipline, and Pastoral Practice*. Each
requires a full source-first redevelopment that broadens the relevant source
families and deepens treatment of the strongest witnesses, material
disagreements, transmission, and limits. Existing prose is provisional, and
page count or repeated source summaries do not establish completion.

The authorized scope is GPT only. Claude publications may be inspected to
understand cross-provider staleness or dependencies, but they must not receive
material source, PDF, web, catalog, release, or baseline changes under this
work. Provider-neutral reusable evidence may be corrected or extended only
where the GPT research requires it; such a change does not authorize rebuilding
or revising a Claude consumer. Completion requires current publication-local
research records, source and rights gates, rebuilt and installed GPT PDFs and
web editions, every-page visual inspection, coherent release records, and
validated pushed checkpoints.

Completed 29 July 2026. The five GPT leaves now contain new comparative
research dossiers or synthesis, checked reusable source records and bindings,
superseding material-change reviews, and exact production records. Nine PDFs
(the five full publications and four proper syntheses) and five canonical web
editions were rebuilt, inspected page by page, installed with exact build
identity, and passed the repository's metadata, component, web-currentness,
source-library, source-inventory, source-family-screening, public-alpha, and
release-binding gates. The affected GPT staleness records are fresh. No file
under `src/claude`, `pdf/claude`, or `web/claude` changed.

### Exorcism reference

<!-- promised-deliverable: task-2-exorcism-100-pages -->

The requested result is a researched, substantive 100+ page Catholic exorcism
reference, not a padded PDF. The current public-alpha edition is 120 physical
pages, of which the first 108 numbered pages are substantive narrative under
the tracked exclusion rule. The comprehensive plan, delivery plan, source
audit, evidence map, scope record, and final exact-snapshot review agree that
the bounded representative study meets the promised extent and that its
source, evidence, rights, safety, jurisdiction, currentness, PDF/web anti-
drift, and every-page visual gates pass on one exact snapshot. The installed
PDF and reviewed build are byte-identical, as are the freshly generated and
tracked web editions. Protected critical editions, direct control of 1614
p. 220, exhaustive manuscript collation, additional local rites and cases,
and Eastern particular law remain explicit future-research ceilings; they do
not reopen the bounded completion verdict or imply ecclesiastical approval.
The controlling evidence is
`research/final-exact-snapshot-review-2026-07-29.md` beside the publication.

### Linen-cloths restoration

<!-- promised-deliverable: task-6-linen-restoration -->

Commit `242aa461` restored bounded burial-practice and material context in the
GPT paper and rebuilt its artifacts. Both provider editions now have one
reproduced exact-current snapshot: the GPT and Claude PDFs rebuild
byte-for-byte to the installed artifacts, their web conversions likewise
match, and all 46 pages have current visual-review evidence. Exact-byte
distribution clearance and internal review do not imply independent
exegetical, patristic, rabbinic, text-critical, or ecclesiastical approval.

### Altar-server guide series

<!-- promised-deliverable: task-1-altar-server-guides -->

Commit `be940904` repaired the seven guide/card PDFs and replaced the four
retained old Low Mass images. All are publicly discoverable review copies on
the branch. The current PDFs carry no reader-facing release-state strip or
label; page counts, card counts, maps, hashes, and production records agree,
and every page has been visually reviewed.
The remaining ledger requirement is exact-snapshot agreement among the Low
Mass and trainer PDFs, maps, hashes, artwork records, and every-page visual
evidence. Rights or liturgical-text permission uncertainty and any concrete
source, safety, artifact, mechanical, or visual defect remain open when
recorded; unavailable external review is not a placeholder gate.
The series-wide sequenced checklist is
`src/gpt/liturgy/roman-rite/1962/reference/altar-server-guides/research/delivery-work-plan-2026-07-27.md`;
it governs the shared Low Mass work and the Missa Cantata and Solemn Mass
deliverables without conflating their remaining gates.

### Sanctuary pictorial dictionaries

<!-- promised-deliverable: task-3-sanctuary-dictionaries -->

The six sanctuary pictorial dictionaries have current inventory, omission,
source, artwork, page-count, and review records that agree with their installed
PDFs. The artwork validator reports zero notices; unsupported identities or
uses remain omitted or held rather than being invented. These objective
records establish the current alpha state without implying human artwork,
priestly, or ecclesiastical approval.
The sequenced inventory, artwork, edition, and publication checklist is
`src/gpt/liturgy/roman-rite/1962/reference/roman-sanctuary-dictionary/research/delivery-work-plan-2026-07-27.md`.

### Missa Cantata guide and cards

<!-- promised-deliverable: task-4-missa-cantata -->

The rebuilt guide and cue cards are installed and linked as public-alpha
copies. Completion remains open until their source support, rights and
distribution status, safety, artifact consistency, mechanical correctness,
and every-page visual evidence agree on one exact snapshot. This does not
imply external ceremonial or ecclesiastical approval.

### Solemn Mass guide and cards

<!-- promised-deliverable: task-5-solemn-mass -->

The rebuilt guide and cue cards are installed and linked as public-alpha
copies. Completion remains open until their source support, rights and
distribution status, safety, artifact consistency, mechanical correctness,
and every-page visual evidence agree on one exact snapshot. This does not
imply external ceremonial or ecclesiastical approval.

### Review-publication discoverability

<!-- promised-deliverable: project-review-discoverability -->

Repository policy now keeps produced PDFs discoverable while honestly labeling
review state. Branch validation found 164 release publications, 14 review
publications, and no held publication in the generated public-alpha artifact.
Production-site route and review-label validation passed for the previously
deployed artifact. The current repository release inventory contains 164
release publications and 14 review publications, 178 total; the exorcism
source, installed PDF, web edition, and audit records agree on 116 physical
pages, including 103 substantive narrative pages.
The standing 27 July 2026 public-alpha authority permits future exact-current
snapshots to be installed and deployed without repeated document-by-document
authorization while preserving every concrete defect in the six alpha
concerns.

### Recently discussed paper hard review

<!-- promised-deliverable: project-recent-paper-hard-review -->

The required set is Catholic Exorcism, Last Supper, Abraham and the Daylight
Stars, John 6, and Linen Cloths. The exorcism and GPT linen work received
substantive repair, but the set has not passed one complete current-guidance
audit. Publication-local internal current-guidance audits now identify and
reconcile the exact installed, web, catalog, and release states for Last
Supper, both Abraham editions, and GPT John 6 while preserving all disclosed
evidence ceilings and without implying external approval. Exorcism and both Linen
editions remain separate exact-snapshot boundaries, and the set-level promise
remains open.

## Full repository discrepancy audit

The 2026-07-27 audit establishes the following actionable backlog:

| Audit ID | Finding | Current measure | Completion evidence |
| --- | --- | ---: | --- |
| `AUD-INTEGRATE-001` | Repair integration and Pages deployment | Integrated through `b93e64b4`; Pages run `30296605957` succeeded | passed; exact catalog-text discrepancy retained under the affected work |
| `AUD-STALE-001` | Rendered publications disagree with current inputs or records | 92 recovered baseline editions; 93 in this checkpoint because the exorcism source audit and delivery plan now correctly make that edition stale pending its later rebuild | `make check-staleness` passes |
| `AUD-SOURCES-001` | Reusable-source family screening | 140 of 140 review units screened across 229 source families; 806 reviewed owner-family presences; atomic citation coverage remains false | `make check-source-family-screening` passes |
| `AUD-REVIEW-001` | Public-alpha copies require exact-snapshot evidence or explicit concrete defects | 14 publications at the recorded checkpoint | each work-specific record resolves the six alpha concerns against its exact snapshot |
| `AUD-ART-001` | Dictionary artwork identification/resolution notices | 0 validator notices; held unsupported assets remain explicit | artwork validator passes without implying external approval |
| `AUD-MEMORY-001` | Conversation outcomes were not exhaustively represented in tracked work records | prior ledger had 8 broad items | every known agreement is represented here and in the ledger when criteria are known |

The audit findings promoted to acceptance-criterion work are tracked below.

<!-- promised-deliverable: project-integrate-and-deploy -->
<!-- promised-deliverable: project-stale-editions -->
<!-- promised-deliverable: project-source-family-screening -->
<!-- promised-deliverable: project-public-review-gates -->
<!-- promised-deliverable: project-dictionary-artwork-holds -->

The recovered baseline had 92 stale editions spanning articles, biographies,
histories, liturgy, Mariology, theology, curricula, and devotions. This
checkpoint intentionally changes two exorcism research records, so the current
working-tree audit reports 93 until that existing edition is rebuilt in its
queued source/drafting or public-artifact work. The immediately discussed
stale papers are named above; the authoritative reproducible inventory,
including the current provider split, is the output of `make
check-staleness`. Staleness is a work queue, not proof that every edition needs
the same substantive edit.

The source-family screening backlog is closed at the family level. Complete
semantic review of all 140 exact owner surfaces added 242 missing presences,
removed 13 false-positive or redundant presences, and retained 806 reviewed
owner-family relationships in total. This does not assert atomic citation
coverage, which remains explicitly false, and unsupported catalog-expansion
leads remain outside the ledger until their own family records are justified.

## Commentary discovery chain

The research algorithm maps a scripture passage to the commentary works worth
pulling into the source vault, then unions those mappings across every proper.
`commentary-work-index discover` is the repo-maintained lookup and
`build-corpus` the union. `tools/harvest` populates the index and
`src/sources/commentary/passage-commentary-index.yaml` now carries the result of
six harvest runs, so a lookup resolves to the works the harvest actually
recorded rather than to nothing.

Weighting is already implemented and needs no schema change. Each mapping
carries a `confidence` float that orders works within a passage, and
`build-corpus` accumulates a reciprocal-rank `score` across passages, so a work
recurring at good rank through many propers outranks one appearing once.

On 30 July 2026 the maintainer accepted the nondeterminism of a model-ranked
"top 20", judging the head of the list unlikely to differ materially between
runs. The concern was that a generated ranking is not a measured citation count
and that variance is largest for obscure passages, which is where the volume is
— 572 of 1301 distinct references are Psalms, many of them ferial antiphon
fragments. The accepted resolution is to define `confidence` as multi-run
agreement frequency rather than a model-asserted score, so the stability claim
is measured rather than assumed and low-agreement works self-identify for
review. Harvest results belong in a dated, tracked ledger; every downstream
tool reads that ledger, which is what keeps the chain repeatable even though
the harvest step is stochastic.

## Tool CLI consolidation backlog

The 2026-07-30 tool review left a deliberate remainder. Delivered: the layout
returned to `tools/<id>` so `tmt check` gates it; the launcher's controls became
dash-prefixed options that a registry id cannot shadow; every registered tool
gained a `tests/tools/<id>.test`; and registry drift, hardcoded paths, and
`usage` staleness are asserted in `tools/tests/test_tool_registry.py`.

The remainder changes interfaces the Makefile, guidance, and release records
depend on, so each needs its own scoped unit rather than an incidental edit:

| Item | Change | Blast radius |
| --- | --- | --- |
| Flag vocabulary | One meaning per flag: `--root` currently carries four, leaf identity has five spellings, `--provider` three shapes | ~20 tools, Makefile, guidance, source READMEs |
| Shared dispatcher | Adopt `scripts/_tooling.py`'s `run_verb_cli` beyond its four current users, giving every tool `--json` and one error contract | 17 tools |
| Verb vocabulary | Collapse 27 verbs onto a closed lifecycle set; `check`/`validate`/`verify` and `bootstrap`/`prepare`/`build-corpus` are synonyms today | 11 verb-bearing tools, Makefile, guidance |
| Id naming | Retire the `check-*` prefix into a `check` verb on the domain tool; `web-edition` and `check-web-edition` already declare the dependency | 7 registry ids, Makefile, guidance, release hash records |

Sequence the flag and dispatcher work first: neither renames an id, and both
make the verb and id changes mechanical. The id renames come last because they
move release hash records and every smoke-test filename together.

## Reconciliation history

- 2026-08-10: **Foundation integration.** The accepted corpus foundation
  landed on `main` from a fresh checkout: `ux/foundation`,
  `impl/foundation-hardening` (with `impl/foundation`), and the six design
  documents of `ux/corpus-wave-1-review-fixes` (with `ux/corpus-wave-1`) were
  merged and semantically reconciled against the six newer `main` bug-fix
  commits; the Wave 1 prototype overlay stayed on its branches by the
  acceptance's own terms; release bindings were regenerated for the seven
  changed browser files. `impl/shell-plumbing` and `impl/catena-wave-1`
  remain deliberately unintegrated pending their recorded gates. The
  `mystago.gy` cutover is external to the repository and untouched. Details
  under "Foundation integration, 2026-08-10".

- 2026-07-31: Twenty-two commits, none pushed. **Site shape.** The landing page
  became the library and its prose moved to `ABOUT.md`, which still opens
  "Don't Panic"; the separate Library page was retired as a second name for the
  same thing. The four reading pages were being copied into the artifact rather
  than rendered, so they alone carried no Triptych header, navigation, footer or
  robots metadata — they now render through `layout.html` like the other 131,
  and all 135 were audited. Two hand-copied duplicates of the site's section
  palette were deleted with that change. `doc/` became `pdf/`, so `src`, `pdf`
  and `web` read as the three forms of every publication.
  **Calendars.** Sixty commemorations folded into 1962 feast names became
  entries of their own, and `check-calendar-masses` now refuses the pattern;
  five absent celebrations were authored and three refused for want of a
  witness; eight masses that existed and no date could reach were dated. Both
  calendars are wholly reachable, 459 of 459 and 268 of 268.
  **Scripture.** Every publishable bible now typesets as a two-column volume
  carrying its own rights notice. 926 of 2190 propers citations were missing the
  commentary index, 888 of them because the lookup preferred "Psalm" over the
  parsed "Psalms". The Knox copyright question was settled from the primary
  record: the US registrations were renewed, R525394 and R646862, so it is
  protected until 2039 and 2043.
  **Policy.** The maintainer withdrew the research-conduct rule, the
  family-screening requirement and the six-concern alpha assessment, and
  suspended research staleness. Nothing was rebaselined and no paper was
  touched, because a cleared flag would have asserted a review that did not
  happen.
- 2026-07-31: Retired `PROJECT-HANDOFF-2026-07-30.md`. Every task in its "where
  to pick up" section had landed and its opening line, "nothing is committed,"
  had stopped being true. The two facts it held that no other artifact did — that
  no authorised bulk source exists for the NRSV or the NABRE, and what is lost by
  not having the NABRE — moved into `guidance/bibles-for-agents.md` as a recorded
  access boundary. Re-measured that document's open-work and
  fails-silently sections against the repository rather than against memory: the
  clamp in `Bible.span` is gone, `citation_divergences` covers twelve books
  rather than four, and the unresolved counts rose in every edition because a
  citation that used to be truncated into a neighbour now refuses.
  `guidance/liturgy/postconciliar-illustrated-dictionary-handoff.md` is a forward
  handoff for unstarted work and was left alone.
- 2026-07-29: Reorganized the public library into the seven approved portals:
  Faith, Scripture, Liturgy, History, Formation, Mary, and Law. Applied their
  muted white, gold, red, green, violet, rose, and black accents and distinct
  ornament pairs throughout the generated site, reserving ℣/℟ for Liturgy.
  Removed reader-facing release-state banners and document labels. Installed
  the expanded 16-page Tenth Sunday synthesis, the sparse lower-third exorcism
  title page with consolidated terminal endnote, and the exact reviewed
  no-label GPT PDF set; Claude publication sources and artifacts were not
  changed.
- 2026-07-29: Retired unavailable human, priestly, specialist,
  intended-reader, physical-use, and ecclesiastical review as placeholder
  alpha gates. Recast current completion tracking around source support, rights
  and distribution status, safety, artifact consistency, mechanical
  correctness, and every-page visual inspection. External approval is recorded
  only when it actually occurs and is never inferred from internal or AI
  review.
- 2026-07-28: Reconciled the exorcism promise ledger and work register to the
  exact bounded-completion evidence: 116 physical pages, 103 substantive
  narrative pages, and passing source, safety, rights, law/currentness,
  PDF/web anti-drift, and every-page review gates. Retained explicit future-
  research ceilings and the public-alpha non-approval boundary.
- 2026-07-28: Superseded the isolated-worker/final-maintainer-push boundary
  with the clean direct-`main` workflow. Authorized ordinary coherent commits
  and regular validated checkpoint pushes to `origin/main`, including their
  automatic Pages deployment attempts, while retaining exact outgoing-range
  review, public-disclosure checks, live-route verification, and the
  prohibition on force-pushing or rewriting published history.
- 2026-07-27: Reconstructed the altar-server, dictionary, exorcism, linen,
  discoverability, and recent-paper commitments from tracked evidence and
  current user direction. Confirmed five repair commits and the public-alpha
  binding commit are pushed but not integrated.
- 2026-07-27: Ran the repository-wide staleness, source-family, public-review,
  artwork, and integration audit. Recorded unresolved counts without promoting
  them to completion.
- 2026-07-27: Added the clean-agent post-merge restart sequence, priority
  queue, exact verification commands, exorcism re-entry point, and authority
  boundary.
- 2026-07-27: Confirmed that pull request 1 was merged, `main` contains the
  repair series through `b93e64b4`, and Pages workflow run `30296605957`
  successfully deployed that commit. Retained the exorcism landing page's
  20-versus-29-page discrepancy as open exact-production reconciliation.
- 2026-07-27: Completed the first bounded exorcism expansion tranche from
  already verified patristic bindings. The changed source builds to an
  uninstalled 32-page candidate; web regeneration, every-page review,
  installation, and all final completion gates remain open.
- 2026-07-27: Combined that tranche with bounded canon-law and safeguarding
  repairs, built and inspected all 32 pages, installed byte-identical PDF and
  web artifacts, corrected the landing-page extent, and bound the exact alpha
  snapshot. At that checkpoint the promised 100 substantive pages remained
  open; production would not change until maintainer integration and push.
- 2026-07-27: Recorded the maintainer's standing authority to publish every
  document as a conspicuously provisional public-alpha snapshot for priestly
  and qualified-reader review. This authorizes the ordinary build, install,
  exact-snapshot binding, validation, and worker-commit workflow without
  repeated alpha approvals, but supplies no human or ecclesiastical review and
  closes no substantive completion gate. Final integration into `main` and
  push are reserved to the maintainer.
- 2026-07-27: Limited all continued research to publicly reachable sources.
  Paid editions, subscriptions, credentials, and maintainer-funded acquisition
  are outside scope; inaccessible necessary witnesses remain explicit evidence
  gaps after proportionate public-source alternatives are pursued.
- 2026-07-27: Authorized project-owned AI artwork creation and revision for
  the sanctuary pictorial dictionaries and altar-server guides, subject to
  exact provenance, rights, source-control, consumer, and review records and
  without treating generated output as human factual or artistic review.
- 2026-07-27: Recorded the then-current expectation that external review would
  be deferred. The 2026-07-29 reconciliation supersedes its use as an alpha
  completion gate while retaining the non-approval boundary.
- 2026-07-27: Replaced the worker's earlier integration, push, and deployment
  authority with the maintainer's final boundary: complete and commit every
  predecessor step in the isolated worker, but leave integration into `main`
  and every push to the maintainer.
- Earlier conversation history is not itself a durable repository source.
  Any additional remembered agreement must be added here immediately and
  reconciled against the repository rather than inferred away.

## Claude Eleventh through Thirteenth Sundays after Pentecost

<!-- promised-deliverable: claude-eleventh-thirteenth-after-pentecost-2026-08-19 -->

On 2026-08-19 the maintainer reopened the closed 1962 temporal propers
boundary for exactly three targets: the Claude guides `51`–`53`, the Eleventh
through Thirteenth Sundays after Pentecost, authored to the current
componentized profile with deep and broad patristic reception research. The
production plan records the boundary decision; this section records the work
authority. The collection remains otherwise closed, and no GPT publication
receives a material change under this work.

For this work the maintainer authorized, in the 2026-08-19 session: full
publication — commit to `main`, the deploy gates
(`make check-deployment-sources`, `make public-site`,
`public-alpha verify --deployment-target github-pages`), and a push to
`origin/main` with its automatic Pages deployment. This supersedes, for this
work only, the 2026-07-27 boundary that reserved integration and push to the
maintainer acting outside a session.

Research verified for these guides enriches the provider-neutral source
library (works, editions, passages, schema-2 bindings) rather than remaining
publication-local; the mass-commentary corpus blocks for `pentecost-11`,
`-12`, and `-13` are the L1 lead lists, and every retained witness is checked
at its work and locus before publication.

**Delivered 2026-08-20.** All three guides are published: Full editions of 34,
36 and 43 pages with Synthesis companions of 17, 19 and 19, each installed from
a page-by-page visual review with installed bytes matching the reviewed build,
and each with an installed web edition. Eleven new passage records entered the
source library (Bede on Luke, the Gelasian and Gregorian sacramentaries in
Wilson's editions, four Bellarmine psalms, four Theodoret psalms) and were
reviewed into their existing families; the classification review resolved the
three new publications to the same eight source strata as the Ninth Sunday.

Three findings are worth recording because they correct or constrain what the
series may claim. The Eleventh Sunday's Introit sings `unanimes`, which is
Cassiodorus's own lemma rather than the Clementine reading — a patristic gloss
that became the chant text — while its Gradual's `ne discedas a me` has no
patristic lemma at all; and its Epistle stops one clause short of the words on
which the whole Augustine–Gregory–Aquinas grace argument turns, which the
commentary reckons with rather than eliding. The Thirteenth Sunday's psalmody
sweep found that `Respice in testamentum tuum` has four rival answers, not one,
and that two of twelve collation divergences are Septuagint or Roman-psalter
transmission rather than chant liberty — which forced an interpretive proposal
resting on the contrary assumption to be rewritten.

Two matters are left for the maintainer rather than settled here. The 1962
proper-guide profile's "full research sequence" sentence and its Reader-Facing
Order list can be read to place the complete appointed formulary differently,
and the three lanes initially resolved it three ways; all three now follow the
`24-tenth-after-pentecost` exemplar, which prints the formulary before the
element-by-element sweep and satisfies both statements, but the profile prose
that invited the divergence is unchanged and should be clarified. Separately,
`TLM text / reference` is a column header in the shared `properstable` macro in
`src/common/preamble.tex`, which `guidance/editorial.md` forbids as apparatus
wording; it appears in every published proper guide and needs one
repository-wide fix rather than a per-leaf fork.

## GPT Eleventh through Thirteenth Sundays after Pentecost

<!-- promised-deliverable: gpt-eleventh-thirteenth-after-pentecost-2026-08-20 -->

On 2026-08-20 the maintainer independently reopened the closed 1962 temporal
propers boundary for the GPT guides `51`–`53`, the Eleventh through Thirteenth
Sundays after Pentecost. The request requires full source-first research, broad
and deep patristic and later saintly reception, Catholic-faithful scholarly
treatment, and enrichment of the provider-neutral shared corpus wherever the
verified research warrants it. The existing Claude editions are source leads
and parallel publications, not prose owners; the GPT editions remain
independently authored and audited.

Each target follows the current componentized profile: one canonical full
research leaf, one mechanically derived synthesis companion, one canonical web
edition, source bindings and reception matrices, installed reviewed PDFs,
catalog links, and provider-qualified release records. This decision changes no
other 1962 identity and authorizes no material revision of a Claude publication.

**Complete.** The three canonical GPT leaves, their mechanically derived
synthesis companions, and their web editions were independently content-audited,
component-checked, built, and visually inspected page by page before the six
reviewed PDFs and three web editions were installed. The source library now
includes reusable checked records for Gregory the Great on Mark 7, Bonaventure
on Wisdom 16, Honorius's relevant whole-proper reception, Anthony of Padua's
critical Latin sermon text, and the official NABRE introductions and notes used
by the guides. Source, inventory, family, catalogue, web, metadata, release, and
deployment gates passed on the integrated tree. GitHub Pages run `32446141366`
then completed successfully, and the live catalog, all three GPT Reader routes,
and all three full-PDF routes returned HTTP 200. The outgoing range made no
material change to a Claude publication; the unrelated local `directions.md`
remained untracked and outside both commits and deployment.

**Reopened on 2026-08-21.** The maintainer rejected the published editions as
an insufficient first pass. The revision must make `Themes and Movement` two
substantively complete pages, replace non-answers in the date/location sheet
with responsibly sourced traditional Catholic dates and attributions, render
patristic and saintly interpretations faithfully within their own theological
grammar rather than organizing the discussion around apology or suspicion,
and greatly deepen both intra-proper exposition and cross-proper development.
That superseded public snapshot remains live until this independently reviewed
substantive revision is redeployed.

**Revised editions deployed on 2026-08-21.** The expanded source-first revision
was independently audited for content, citations, traditional Catholic
chronology and attribution, and every rendered page. The reviewed Full and
Synthesis PDFs and canonical web editions were installed with the page-2
chronology dossier, two complete `Themes and Movement` pages, and detailed
commentary beginning on page 5. Commit `2810f6aba` reached `origin/main`; GitHub
Pages run `32498704134` completed successfully. The live catalog and all three
GPT Reader routes returned the revised timestamps, and all six live PDF routes
matched the reviewed SHA-256 hashes exactly. The unrelated local
`directions.md` and `-.png` remained untracked and outside the commits and
deployment.

## Scripture chronology corpus

<!-- promised-deliverable: scripture-chronology-corpus-2026-08-26 -->

On 2026-08-26 the maintainer requested the project's first durable,
translation-independent Scripture chronology corpus: every Scripture locus this
repository can address should resolve to a stable, reusable set of zero or more
typed temporal assertions, so that propers, the Catena, Scripture studies, the
web reader, the PDFs and every future consumer stop independently re-deriving
biblical dates.

The chronology is deliberately **traditional Catholic chronology**, preserved on
its own terms. It is not an attempt to reconcile the biblical and traditional
reckoning with modern archaeological, Egyptological, Assyriological or
critical-historical chronologies where those diverge. A modern or critical
chronology, if ever wanted, is a separate named profile and never a silent
correction of this one.

**What the corpus is.** It sits behind the existing citation and
versification/projection machinery and in front of document synthesis. Assertions
are keyed to canonical Scripture loci in the `vulgate` system — the system
`scripts/_projection.py` already projects into and both tracked calendars cite in
— never to any translation's verse strings. One locus resolves to any number of
typed assertions across eight relations (`composition`, `narrated-event`,
`utterance`, `historical-setting`, `superscription-setting`,
`retrospective-event`, `prophecy-given`, `prophetic-referent`). An event is dated
once in `events.yaml` and bound from every locus that needs it, so the four
Gospels cannot acquire four Crucifixion dates; a binding carries no date and the
loader refuses one that tries to. Composition chronology inherits from a textual
unit to the verses inside it, and two units of equal width over one verse is a
load error rather than a tie the corpus breaks.

**What it refuses.** No universal verse space: where the psalm or deuterocanon
concordance refuses, chronology refuses, and says which kind of refusal it is.
No date without a prose basis and a source-library record behind it. No numeric
confidence. No harmonising two traditional claims into a third nobody asserted.
No Anno Mundi converted to B.C., because that requires an epoch no ranked source
in this repository has been inspected asserting. No bare coverage percentage.

**State on 2026-08-26.** The governing contract, the traditional profile, the
data model, the loader and its validation, the query, the coverage derivation,
the gated derived table, the registered tool and the repository gate are in
place, and **all twelve promised requirements pass**. The corpus holds 274
events, 59 composition units, 375 bindings and 20 typed gaps, resting on 128
registered source artifacts - signed Catholic Encyclopedia articles across all
fifteen volumes, Eusebius's *Church History* I to III, and Augustine's *De
consensu evangelistarum* III - each acquired over HTTPS, hashed, and read for
the sentence it is cited for.

Coverage, by category, over the canonical Clementine edition's 35 809 verses:

| Category | Verses |
| --- | --- |
| substantive event assertions (`dated`) | 12 406 |
| inherited composition only | 16 687 |
| undated in tradition, sources inspected | 6 716 |
| research-pending | 0 |
| carrying more than one relation type | 7 975 |
| carrying preserved alternative traditional claims | 12 897 |
| blocked by Scripture identity or alignment | 0 |

There is deliberately no single percentage. A headline would be true of a corpus
that had researched nothing, since what it would count is keys in a file.

**`research-pending` reached zero, and the guard that removed was replaced.**
Every locus now resolves to a substantive assertion, an inherited composition,
or an authored gap row naming the source that was read and found silent. That
is a real result and a bounded one: two thirds of the canon is `inherited`, and
`undated-in-tradition` is the second largest share precisely because the
traditional apparatus dates so little composition. While the corpus was
incomplete, the printed `research-pending` count was itself the proof that no
coverage claim ran ahead of the research. `guidance/scripture-chronology.md`
§9.2 records what replaced it: `tools/tests/test_chronology.py` now refuses a
gap row that names no source record - the exact shape a fabricated coverage
number would have to take - and refuses any status reaching a verse that no
author asserted, checked against `AUTHORED_STATUSES`, which `_chronology` names
once so the loader and the test cannot drift apart.

**A finding recorded here was wrong.** The first entry stated that not one
inspected source says when any psalm was *written*. Re-reading Drum's "Psalms"
in full overturned that in three places, and only three: the article dates
Vulgate Ps 82 ("seems to have been written at the time of the havoc wrought by
the Assyrian invasion of Tiglath-pileser III in 737 B.C."), Vulgate Ps 73
("probably written, as Briggs surmises, during the Babylonian Exile, after 586
B.C."), and the Korahite psalms as a period. It dates nothing else in 150
psalms, David included, and the Miserere is genuinely not among them - so the
half of the finding that mattered for Psalm 50 stands.

**What auditing the population proved.** Every book was populated by a lane that
read ranked sources and quoted them, and every lane's work was then re-read
against those same sources by an independent one. The audit found five classes
of defect that had passed their own lane's review, loaded clean and audited
clean: a quotation from memory (the Authorised Version's wording of Genesis
18:10 standing in for the tracked Douay's); a `relative` anchor that existed but
was the wrong one (Jacob's twenty years measured from a birth Genesis places
fourteen years into the term); a modern-critical figure admitted to the
traditional profile ("as most critics think ... about B.C. 300" dating both
books of Esdras, which §4.3 excludes and which the same lane had correctly
refused an hour earlier in another sentence); a claim about four articles with
no retained retrieval, which turned out to be false for two of them once
fetched; and a refusal that went stale inside its own wave, giving two psalms
with one superscription two different answers. All are fixed, and
`guidance/scripture-chronology.md` §15.1 names them so the next lane can look
for them by name. The two Esdras composition units were withdrawn rather than
re-labelled, which moved 684 verses out of `composition`: coverage went down,
and that was the honest direction.

The hard cases still hold. The four Gospels reach one Crucifixion, dated once
and disputed seven ways because the Catholic Encyclopedia declines to settle its
own question, while each Gospel keeps its own composition chronology. Psalm 21
binds to that same Crucifixion under `prophetic-referent` and never under
`narrated-event`. Psalm 50 takes its setting from its own printed title and
answers to Hebrew 51 through the existing concordance. Sirach refuses in the
Greek arrangement, because there are two texts and not two numberings.

**What is left, and is not a promised requirement.** Thirteen dated events are
bound to nothing, because no Scripture passage narrates them and no inspected
source names one. The Hallel at the Last Supper (CE: "He recited the Hallels at
the last Passover, Pss. cxiii-cxiv before the Last Supper, Pss. cxv-cxviii
thereafter") is an `utterance` binding worth some ninety verses that no lane
owned. Van Hoonacker supplies three restoration figures - B.C. 445, 433 and 398
- that belong as further claims on events already held, and Schets a fourth,
598 B.C. for Joachin's deportation. Two corpus-wide questions want a
maintainer: whether `precision: relative` may carry a duration *within* an
anchor rather than an interval *from* it, which is what all eighteen judges'
spans and several older events do; and whether an authorship ascription may
become an occasion, which the corpus refuses for Ps 88 and allows for Ps 21.

## Correction lane, 2026-08-27: the ontology, before an independent audit

The population of 2026-08-26 was marked complete by its own author. That
disposition was premature and is reversed here. **The research was not the
problem; the ontology was.** Four defects were corrected, the promise was
reopened, and the corpus now waits on a cold independent source audit that this
lane may not perform and did not.

**A named system is not a translation, and a mapping refusal is not silence.**
Chronology was authored in `vulgate` alone and returned a concordance refusal as
its own answer, conflating two questions: whether a locus may be asserted
equivalent to another, and whether it can carry chronology at all. The Greek
Ecclesiasticus is the standing case — 1 355 of its 1 356 printed loci refuse the Vulgate
because there are two texts and not two numberings — and the corpus already knew
it had nowhere to put the fact: `composition.book-of-ecclesiasticus` carried a
note warning that three dates in Gigot's article "must not be conflated",
written by an author who could not act on it. The Greek translation is now dated
natively to "not long after ... the year 132 B.C." while the concordance goes on
refusing, and both are true at once. Systems are read from the modules that own
them rather than restated, the check is `(system, book)` so `hebrew` cannot name
Matthew, and native authoring is refused wherever the concordance carries the
text safely — which makes "one fact, one place" a load-time gate rather than a
convention.

**Applicability is not directness.** `dated` required a *direct* substantive
assertion, which said two wrong things: 271 verses of Ezechiel reached by a
whole-book `prophecy-given` looked undated though the oracle applies to every
one of them, and a directly authored composition unit alone would have reported
event chronology nobody had researched. Status now asks what applies;
`direct`/`inherited` rides on each returned assertion as provenance and decides
nothing. Measured: **zero verses change status** — `direct` was dead code,
because no composition unit is scoped to verses — but the definition was false
of **7 354** verses, which is what was corrected. The status formerly called
`inherited` is `composition-only`, since it was a directness word doing a scope
job, and coverage reports the provenance split beside the statuses.

**A duration is not an offset.** All 216 `relative` claims were classified
against their sources. **47** were lengths wearing an offset's clothes — the
whole Judges family among them, nineteen and not the eighteen previously
reported, because `israel.judges.heli-judgeship` is the nineteenth and any
migration selecting on the book of Judges would have missed it. `duration` is
now its own precision and the distinction is structural: no offset anchor, no
endpoints, no zero or negative length, and a `within` that is validated as a
real event but is deliberately not returned as an anchor. Seven wrong anchors
were corrected besides — one that ran backwards onto the mission it precedes,
two circular regnal datelines, one naming the wrong king's accession. Six claims
are genuinely ambiguous in their sources and are left as `relative` for reviewer
disposition rather than guessed.

**Authorship is not occasion.** Ps 21's `historical-setting` conceded in its own
note that the title "names no occasion" and then took the occasion to be "the
reign of David itself". Ps 88 had already refused exactly that move in its own
words. Ps 21's was withdrawn; six of the seven Psalm settings rest on real
occasion evidence and stand. Ps 21 keeps its Passion `prophetic-referent` and
every verse of it stays dated. The hard case "one verse carries three relation
types" moved from Ps 21:2 to Ps 17:2, which carries four on evidence, rather
than propping a count up with a binding the sources do not support.

**A defect this lane found in a test.** The World English Catholic edition is
two hops from the Vulgate, through the Greek. Chronology asked for a direct row,
the direct index is empty, and all 2 094 of the loci it prints returned
`textually-distinct` — and a test asserted that refusal as correct behaviour.
730 of those loci are the Vulgate's own text, and under the corrected coverage
rules every one of the 2 094 would have counted as new Scripture. A refusal is
evidence about a route until the route has been checked.

**Coverage, over a universe that is now named rather than assumed.**

| Vulgate/Clementine primary universe | Loci |
| --- | --- |
| total | 35 809 |
| substantive (`dated`) | 12 406 |
| composition-only | 16 687 |
| undated-in-tradition | 6 716 |
| research-pending | 0 |
| — of the substantive: direct only | 3 646 |
| — inherited only | 7 354 |
| — both | 1 406 |

| Additional native loci | Printed | Shared | Already counted | Additional |
| --- | --- | --- | --- | --- |
| `greek` | 2 156 | 800 | 0 | **1 356** |
| `hebrew` | 2 528 | 2 528 | 0 | 0 |
| `world-english-catholic` | 2 094 | 730 | 1 358 | **6** |

Corrected universe: **37 171**, restated on 2026-08-27 after the post-audit
correction lane found `_system_loci` filling each chapter from its first printed
verse to its last, which invented 38 `greek` and 37 `world-english-catholic`
verse numbers no witness prints. The figures above were 2 194 / 1 391 and
2 131 / 9 against a universe of 37 209.

Every additional native locus now reaches a chronology status of its own: the
seven that carried a mapping word instead — one Greek Esther locus and six World
English Catholic ones — answer `research-pending`, on the chronology axis, beside
the mapping refusal on the mapping axis. Three of the ten the cold audit counted
were among the invented loci and were never text. `exhaustive-coverage` stays
open on its own criterion while any locus is `research-pending`, which is the
honest reading and not a defect.

**The promise is reopened and stays open.** Thirteen requirements now, three of
them open: `translation-independent-identity` and `exhaustive-coverage`, both
rewritten to require what they were meant to require, and a new
`independent-source-audit` which **this lane may not mark pass**. Machine-valid
is not source-verified: the population wave passed every gate and its own
authors' review, and a second reader still found a quotation from memory, a
wrong relative anchor, a modern-critical figure inside the traditional profile,
an unretained claim of source silence that proved false for half its subjects,
and a refusal that went stale mid-wave. Author self-review cannot discharge
this.

**The cold audit's review target is tracked**, at
`src/sources/chronology/cold-audit-manifest.tsv`. It holds 72 factual claims —
one row per subject-and-claim, never per binding, so a claim reused by a
thousand verses is reviewed once — selected by a rule reproducible from the file
alone: strata of (precision, disposition), ordered within each by
`sha256(seed + id)` with the seed recorded, round-robined until 72 are taken.
Nothing was hand-picked, and a reviewer can regenerate the identical list. Four
high-risk classes are excluded from the sample because they are to be inspected
**completely**, not sampled: 47 migrated durations, 9 Psalm historical-settings,
2 derived spans, and the 1 native non-Vulgate claim. Those class sizes total 59
and the excluded set is **57**, because two claims belong to two classes —
`israel.monarchy.saul-reign#0` and `israel.exile.seventy-years#0` are durations
AND Psalm historical-settings. The manifest header now carries the predicate,
and the post-audit lane verified that it reproduces all 72 rows in order. What the reviewer must verify per claim is in
`guidance/scripture-chronology.md`; the five source-fidelity failure modes from
§15.1 and the five new semantic ones are named there so they can be looked for
by name.

### Cold-audit handoff: the exact review target

| | |
| --- | --- |
| branch | `feature/bible-dating` (unmerged, and to stay so) |
| population HEAD this lane started from | `f1bf113564f57a90dfc593eab4742268b5ffe587` |
| correction HEAD | `68c8d8ef2b2bfd25a147cbaf56cbb11781126f9e` |
| base compared against | `origin/main` `2778285849f2973ea89d1cfd5b2751ed4ae58e54` |
| promised deliverable | `scripture-chronology-corpus-2026-08-26`, **in_progress**, 10 pass / 3 open |
| open requirements | `translation-independent-identity`, `exhaustive-coverage`, `independent-source-audit` |

**Corpus files.** `src/sources/chronology/{profiles,events,composition,bindings,gaps}.yaml`
authored; `coverage.tsv` derived and gated; `cold-audit-manifest.tsv` the review
target. Loader `scripts/_chronology.py`; tool `tools/scripture-chronology`;
tests `tools/tests/test_chronology.py` and `tests/tools/scripture-chronology.test`.

**Source families the claims rest on.** The Catholic Encyclopedia (New Advent
transcriptions, all fifteen volumes, `storage = "remote"`, no bytes retained);
the Douay-Rheims as its own rank-1 witness, cited `bible:douay-rheims:<locus>`;
the Haydock 2014 Loreto/Feeney Memorial printing, via tracked passage records;
Eusebius's *Church History* I-III; Augustine's *De consensu evangelistarum* III.

**What this lane changed in production data**, and which the reviewer should
treat as unreviewed: 47 claims migrated from `relative` to `duration`; 7 anchors
corrected; 1 binding withdrawn (Ps 21 `historical-setting`); 1 composition unit
added (`composition.book-of-ecclesiasticus.greek`); 2 anchor events added
(`israel.judges.ark-comes-to-cariathiarim`,
`israel.exile.nabuchodonosor-accession`); notes corrected on the Ps 88 setting
and the Micheas 1-3 unit.

**Six claims left ambiguous for reviewer disposition**, not guessed:
`israel.judges.period` (Acts 13:20 — the Douay word order attaches the 450
years to what precedes, the Greek to the judges; a textual variant, not a
reading choice), `israel.monarchy.absalom-revolt` ("after forty years" with no
stated origin), `israel.exodus.moses-in-madian` ×2 (the ambiguity is in the
subject: one event denotes both the flight and the shepherd years),
`israel.exodus.mara-and-elim`, `israel.conquest.war-against-the-kings-of-chanaan`
("a long time", unquantified). All six were dispositioned by name by the
post-audit correction lane; see `post-audit-corrections.tsv`.

**The wrong anchors: fourteen, not four, and the record no longer lives in
`.scratch`.** This paragraph said four were "dispositioned rather than changed"
and pointed at `.scratch/audit/durations.md` §3.1 — a file `wt tidy` deletes
without asking, holding the tracked acceptance record for the question. §3.1
names **fourteen**. The cold audit re-derived every one against the corpus and
put the whole table in `cold-audit-report.md`, which is tracked and immutable:
nine are genuinely fixed, and the five that were not are dispositioned in the
correction ledger. Nothing about this question now depends on a scratch file.

**Inherited broad-suite failures**, identical on branch and base and none of
them chronology: `check-web-editions-current` (one stale tracked web edition),
`check-sources` (pinned migration snapshots stale), `check-tool-registry` (8
tools using a sibling without declaring it), `check-examples` (4 diverged on the
branch, 6 on base; this paragraph said 24 and the cold audit re-measured it).

**No branch regression against `origin/main`. This paragraph said there was one
and was wrong; the cold audit re-measured it.**
`tools/tests/test_tool_registry.py::test_shell_smoke_tests_pass` fails on
`tests/tools/source-family-migration.test`, which reports that
`src/sources/inventories/source-family-migration-v1.toml`'s pinned
`canonical_catalog_snapshot` and `inventory_snapshot` are stale. That failure is
**inherited and base-identical**: run in a clean worktree at the merge-base
`22528396a` it fails with the same two errors, naming the base worktree's own
path. Comparing failure names rather than counts, the branch introduces none and
the base carries one the branch does not — `pdf-review.test`, which needs a built
PDF a fresh worktree has no copy of, an environment difference rather than a code
one. Full suite: branch 36 failures, base 37, and the 1 820 − 1 736 test-count
difference is exactly the 84 chronology tests this branch adds.

The staleness itself is real and is what makes `check-sources` fail on base and
branch alike. Its cause is the population lane of 2026-08-26 registering 128 new
source artifacts behind a pin that has not been re-reviewed. **It has deliberately
not been refreshed.** Re-pinning a snapshot asserts that the review the pin stands
for has been performed, and it has not been — the cold audit reviewed the
chronology corpus, which is a different question, and so discharges nothing here.
It needs a maintainer, or the source-family review lane, not a lane rewriting a
timestamp to make a gate green.

**What the cold reviewer must verify, per claim**: the cited artifact or record
exists; the cited locus actually supports the claim; quoted wording matches the
retained text exactly; the claim is in the source's own voice or correctly
attributed; the traditional-profile rank is admissible and no modern-critical
figure is silently treated as traditional; the date structure preserves the
source's precision and its hedge; the relation type is semantically right;
anchor, containment and duration semantics are right; the event identity is
right; the binding scope does not reach past what the source supports;
alternatives are not quietly reconciled; and a negative or silence claim is
actually supported by retained inspected evidence. PASS / CHANGES REQUIRED per
finding, plus an overall disposition. **No same-agent self-review satisfies
this**, which is why the requirement exists and why this lane left it open.

**Not in this lane.** Propers, the Catena, the web reader and the PDFs are not
wired to the corpus, and no proper document was revised. The consumer contract
that binds them when they are is stated in `guidance/scripture-chronology.md`
§14: a consumer must read the corpus and must not re-derive, and where the
corpus is unresolved the consumer preserves that state or omits the date.

### The final cold-acceptance handoff

The cold audit returned `CHANGES_REQUIRED` and a correction lane closed all 104
findings. A targeted cold re-review then read all 92 changed rows and returned
`CHANGES_REQUIRED` again — 23 rows, 9 major, none critical — and disclosed that
it had run in the same session as the lane it reviewed, so it could not satisfy
`independent-source-audit` whatever it found. A bounded repair lane has now
closed those 23. It is in the same position and accepts nothing.

**What that repair changed, beyond the 23.** Ruling RR-090 required treating
Howlett's concluding sentence as one provenance unit, and that ruling does not
stop at the one figure the row names: the same sentence supplies the dates of
the Exodus, Saul's accession, David's accession, Solomon's accession and the
building of the Temple, and the section after it derives more from the same
Assyriological reconstruction. Withdrawing one while keeping the others would
have reproduced the defect the row condemns. The whole sentence was therefore
ruled, and every withdrawn figure is recorded in its subject's note rather than
lost.

**What the review apparatus could not see, and now can.** The 92-row manifest
compared `str(claim.date)`, which renders a relative date's statement and not
its anchor, so ten claims that moved anchor were labelled by what else changed
and three were labelled `changed:note` alone — a wrong anchor being the class
the audit rated major. It compared binding scope alone, so four binding groups
that changed materially without changing scope appeared on no row, two of them
corrected misquotations of the tracked Douay. It enumerated no guidance or
loader change, so the contract drifting behind the implementation was caught by
a reviewer's eye rather than by the apparatus. And its 92 rows are **96**
distinct cases: two rows duplicate others and two are bundles naming eight
source records between them.

All three are now derivations rather than habits.
`scripts/chronology_review_diff.py` loads each revision's corpus through **that
revision's own loader** — which matters, because the loader has since been
tightened to refuse duplicate mapping keys and the older corpus contains
some — and diffs the loaded objects over claims, bindings, gaps, source
records, contracts and code.
`scripts/build_rereview_manifest.py` and
`scripts/build_final_acceptance_manifest.py` derive the two manifests from it,
and `scripts/check_final_acceptance_manifest.py` proves the final one complete
in both directions and proves that none of the 218 prior review ids was dropped.

**The review surface is `src/sources/chronology/final-acceptance-manifest.tsv`.**
Every row is reviewed; nothing is sampled.
`src/sources/chronology/final-repair-report.md` carries the head references by
sha, the two source-retrieval hazards a cold reviewer will otherwise hit, and
the cold-review requirement itself.

**The next lane is not this one, and may not be.** `independent-source-audit`
is closed only by a reviewer in a clean new agent or session that performed
none of the population, the first audit, the post-audit correction, the
targeted re-review, or this repair — reading repository artifacts only,
reopening sources, and instructed to distrust the ledgers and the tests,
including the ones this lane wrote. No same-session subagent arrangement
satisfies it. Until that review returns PASS and a maintainer accepts, nothing
merges and propers integration does not begin.

## Complete Missal corpus remediation

<!-- promised-deliverable: complete-missal-remediation-2026-08-26 -->

**Completed and deployed on 2026-08-28.** Work began on
`feature/complete-missal` from synchronized base
`2778285849f2973ea89d1cfd5b2751ed4ae58e54`. The maintainer requested one
source-honest program that audits and remediates the postconciliar, Roman 1962,
and Roman pre-1955 Missal data in English and Latin; corrects calendar,
recension, Common, Proper, Ordinary, dialogue, presentation, provenance, and
publication-boundary defects; verifies the complete one-year matrix; commits
and pushes coherent feature work; receives a cold review; then reconciles with
current `main` and advances `origin/main` without rewriting history.

The audit baseline covers every civil date from 2026-08-26 through 2027-08-25:
three calendars by two requested languages by 365 dates, with 2,190 successful
JSON renders and 2,190 successful text renders, no invocation or JSON-parse
failure, and empty standard error. It found ten whole-Mass postconciliar
placeholders and four historical placeholders; seven placeholder
postconciliar Commons and seven structurally incomplete Roman Commons; 89
explicit postconciliar English Proper gaps and 166 historical English Proper
gaps; 391 unselected postconciliar weekday reading or psalm slots; incomplete
postconciliar Eucharistic Prayers; and a historical Ordinary witness that does
not by itself establish a target 1962 or 1920 recension. Roman pre-1955 remains
primarily inherited 1962 material with six Holy Week deltas, and the 1956-1960
middle recension is not held as a complete source-grounded corpus.

The same baseline records the historical January 4 no-Mass result, the
postconciliar 2027-06-05 equal-rank conflict, ambiguous Common selection,
Roman calendar-spine identity failures, scoped-rubric/global-index drift, and
language, territorial, option, weekday-cycle, diagnostic, and generated-data
freshness weaknesses. Rights review found tracked ICEL-facing material without
an adequate per-text/per-surface publication filter, provenance mismatches,
misclassified Gospel Acclamations, missing FDLC artifact records, and Latin
surfaces without sufficient per-text rights evidence. No unavailable or
uncleared text may be filled by reconstruction, an unofficial copy, or silent
cross-recension fallback; an unresolved or withheld state is the correct
result until an exact permitted witness exists.

The visual baseline and browser evidence under the ignored review tree already
establish a calmer 39.75rem reading measure, a readable three-rem cue axis,
cross-browser serif fallback, print/reflow/accessibility coverage, and event,
text, Proper, Ordinary, state, source, seat, and rubric parity for representative
Roman 1962 and postconciliar states. Structured dialogue work may add only
source-owned turns and semantically honest role or versicle/response cues; it
may not split opaque prose by string matching or equate Priest/Server with
versicle/response.

**Exact successor snapshot internally accepted for deployment on independent
AI cold-review evidence; production integration is verified below.** Feature
commit
`a1a7ab774a7318cb0b66d74462090856347d5915` (tree
`b70bdf637387ba552d66d6f7e38704a5ed116f19`) was pushed exactly to
`origin/feature/complete-missal` at that stage before the later
deployment-record and workflow commits, descends without a rewrite from the
then-current `origin/main` base
`2778285849f2973ea89d1cfd5b2751ed4ae58e54`, and its tracked worktree and index
were clean at the exact Firefox capture and handoff assembly. Independent
semantic, source-identity,
rights, generated-freshness, path-integrity, deployment-artifact, commit-scope,
and exact-handoff reviews found no successor blocker.

The accepted source tree carries 619 postconciliar Mass identities, 491 Roman
1962 identities, 489 effective Roman pre-1955 identities, and eight explicit
pre-1955 departure records. The source library validates at 537 works, 722
editions, 1,837 artifacts, 3,295 passages, 72 segments, and 2,167 bindings.
The registered `complete-missal` audit measures all fifteen completion
dimensions over 2020--2120 and reports 39 typed unresolved audit-dimension
cells instead of inventing text or silently borrowing a recension: 8/492/619
represented celebrations and at least 5,158/5,247/3,056 modeled text slots for
pre-1955/Roman 1962/postconciliar respectively. Its source-honest `--check`
passes; its stricter `--require-resolved` mode intentionally refuses while
those explicit cells remain. They are completion-dimension findings, not a
claim that 39 whole texts are absent.

The authoritative full Python run passes 2,302 tests with no failure or error
and ten intentional skips. `make check` replays 203 of 212 captured examples
with no divergence, stale capture, or tracked write; six are policy-exempt or
never-run and three have unavailable fixtures. The annual gate passes all six
tests over 365 days, three calendars, and two languages: 2,190 cases and 4,380
successful JSON/text renders. Five focused Chromium production harness
contracts pass all 134 assertions within six passing unittest gate tests.
Fresh Firefox 154.0.1 evidence is intrinsically bound to the exact clean
feature commit; automated metrics plus AI visual inspection of the canonical
full-Mass desktop 1440x900 and mobile 393x852 states found no horizontal
overflow, duplicate IDs, or failed page requests. The broad Chromium
accessibility run retains exit 1 at the exact inherited baseline rather than a
green gate: 2,290 assertions, 1,850 passes, 212 failures,
and 228 skips, comprising 108 duplicate-main, 77 target-size, and 27 modal
skip-link findings. The other long-running FINAL5 gates ran on the frozen
precommit candidate subsequently committed unchanged; their logs do not embed
a commit or tree identifier and are forensic workflow evidence rather than
intrinsically commit-bound records.

The final deployment-source, public-site, and GitHub-Pages-target verification
gates pass on the frozen successor. The resulting local artifact contains
20,549 regular files and 1,978 directories totaling 436,003,351 bytes, with
20,548 matching checksum entries and no symlink, special file, unsafe link,
forbidden path, residue name, or quarantined-body match. Act-history projects
all 505 canonical files and rejects replaced or linked projection roots;
public-alpha uses descriptor-rooted, no-follow creation and an immutable
verification snapshot with identity-bound cleanup. All generator, Act-history,
release-binding, calendar, and source-reader freshness gates and the tmt
registry check pass.

Rights-withheld bodies are absent from current public structures; formerly
composite celebration identities are split; calendar and option ambiguity
fails closed; and Ordinary and Proper consumers share typed availability,
source, and dialogue semantics. Ten Roman 1962 Latin Proper prayer bodies,
each byte-identical to its selected passage in a Triptych-created editorial-
projection artifact, are published under a record that attributes only the
bounded selection, transcription layout, normalization decisions, and
collation record to Triptych. The underlying prayer wording remains public
domain in the United States; the Lasance antecedent supplies that basis and the
restricted 1962 facsimile remains a separate comparison witness. No new human
collation or approval is claimed. Current-tree
ICEL payloads, quarantined Roman 1962 Latin Proper bodies, and the superseded
Lasance OCR artifact with the excluded 1302a--1302d insert are absent from the
tracked tree, generated surfaces, deployment artifact, and current review
handoff. Reachable earlier Git history still contains protected or superseded
objects. Whether that history requires rewriting, replacement, access
restriction, or another remedy remains a maintainer/counsel release-policy
decision; the required fast-forward workflow deliberately does not rewrite it.

The exact successor review handoff is
`build/agent-handoffs/20260828T172422Z-complete-missal-final-review/`, with a
verified one-root ZIP beside it. Its 15-entry manifest has SHA-256
`9e53c26fd3588f009c770f22a6cf4a7bb3ad8acd48f8c85919e69a88f4d4bd03`;
the ZIP has SHA-256
`e0d42528ccabb6889f8dadd771a6f94b1c068e6744c76e52b1fbf51c17075907`.
It supersedes the preserved `20260828T170544Z` package, which superseded
`20260828T164734Z`; that package superseded the earlier `20260828T045009`
recovery package. This is
AI-assisted and automated review evidence, not human, priestly, specialist,
intended-reader, physical-use, ecclesiastical, or new exact-snapshot human
approval.

**Production integration and live verification complete.** `origin/main` first
advanced by genuine fast-forward from
`2778285849f2973ea89d1cfd5b2751ed4ae58e54` to
`de7c78334d2f7418c20c7a595e6aae9ce45f39c9` after all three local deployment
gates passed on that exact clean tree. Exact Pages run
[`33196238024`](https://github.com/spincyc/triptych/actions/runs/33196238024)
then reached artifact verification only after checkout, dependency
installation, source verification, and the public build had passed; GitHub
cancelled the job at its configured 15-minute ceiling before verification,
upload, or deployment could complete. That is infrastructure-timeout evidence,
not a successful or failed content gate, and no production deployment is
claimed from it.

The narrowly scoped timeout correction raised the workflow ceiling to 30
minutes without changing the gate sequence. `origin/feature/complete-missal`
first advanced by genuine fast-forward to exact commit
`0817b42b500a35002ceb892ade89832093b93522`; the three local deployment gates
then passed on that exact clean correction tree; and `origin/main` then
advanced by genuine fast-forward to the same commit. Pages run
[`33197920174`](https://github.com/spincyc/triptych/actions/runs/33197920174)
and its sole deploy job
[`98939717180`](https://github.com/spincyc/triptych/actions/runs/33197920174/job/98939717180)
completed successfully for that exact `main` head; all source verification,
public build, artifact verification, configuration, upload, and deployment
steps passed. GitHub deployment `6146198392`, final status `17472596177`, binds
that exact commit and `main` ref to the `github-pages` environment and
<https://mystago.gy/>.

A fresh production verification parsed the served checksum inventory and
proved it byte-identical to the local 20,548-entry `SHA256SUMS` artifact, whose
SHA-256 is
`f192be2f12357e141c83f6b2338a9b2ead9e6f221848c26567d8332f25e59bf2`.
All 20,548 inventoried local files were independently authenticated against
that target inventory. Against the captured pre-integration inventory the
verifier identified 16 added, 1,249 modified, and zero deleted paths, then
fetched and matched all 1,265 affected live routes byte for byte with no HTTP,
redirect, truncation, or checksum failure. This closes the promised production
requirement for the deployed content while retaining every audit-dimension,
broad-browser, review-authority, and reachable-history qualification above; it
is not a global legal clearance or human,
specialist, priestly, intended-reader, physical-use, or ecclesiastical
approval.

## E1 Catena integration candidate

The convergence review (branch `review/catena-e1-convergence`, commit
`f1a5bbad763b847ded8799748223898de6ad4de9`) classified the remaining Catena E1
state with zero `MERGE_BLOCKER` and zero `INTEGRATION_BLOCKER` findings,
cancelled the V17 semantic lane as `CANCEL_V17_SEMANTIC`, left the inherited
chapter-root getter, hostile-thenable, and body-write retry findings as
`HARDENING_BACKLOG`, left the eight package/history/replay/scanner defects as
`EVIDENCE_TOOLING_BACKLOG`, left twenty release, shell, data, validation,
Liturgy, PDF, and final-integration concerns `SEPARATELY_OWNED`, and
dispositioned the line **`READY_FOR_INTEGRATION_BRANCH`**.

Acting on that disposition and its exact bring-across manifest,
`integration/catena-e1` was created from the exact authorized main base
`2778285849f2973ea89d1cfd5b2751ed4ae58e54` (origin `main` had not moved past
it), with the reviewed V16 implementation `cc1f2fb8625f044558c26edd358b99cd7dcc7646`
used as final implementation truth rather than merged. The candidate integrates
exactly:

- the final production Catena route, model, page, and stylesheet
  (`src/web/browser/catena/catena-model.js`, `catena.js`, `catena.css`,
  `index.html`), which main had not independently changed since the reviewed
  fork point, so no current-main work was displaced;
- the `scripts/_catena.py` voice-authority change and its deterministic
  regeneration of `src/web/data/structure/catena/index.json`, which now
  publishes the held voice set `original`, `translation:en`,
  `translation:la`, plus the Isaiah 8 chapter file `27-is/008.json`
  regenerated from main's own source records and byte-identical to the
  reviewed V16 generated output;
- the 78-line fail-closed generator-contract expansion of
  `tools/tests/test_catena.py` (56 tests total); and
- `tools/tests/test_catena_production.py`, 419 production-policy regressions
  curated verbatim from the V16 wave-1 suite for publication atomicity,
  owner/completion identity, same-path/late isolation, exact voices with
  `translation:grc` refused, refusal/absence/provenance truthfulness, path
  namespace closure, cache completion isolation, malformed canonical data,
  and the governed budget assertions.

The 17,315-line synthetic wave-1 harness, the hostile
prototype/getter/thenable classes, evidence tooling, attempt history,
packages, correction-lane bookkeeping, and V16-side release or shared-shell
changes were not brought across. The three hardening findings and eight
evidence-tooling findings remain backlog; the twenty separately owned concerns
were not touched; the four Catena release bindings were not refreshed (they
belong to the release owner after accepted integration bytes).

Fresh validation on the integrated tree: the generator contract reports
1,351 fragments / 1 book / 73 canon entries; the focused Catena suites pass
56/56 and 419/419 under node; static browser checks pass 5/5; real-Chromium
route-only runs over `/catena/index.html` produce the same 121 assertion
identities with the same 95 pass / 14 inherited shared-shell fail / 12 skip
statuses at the exact base and at the candidate, with zero status changes;
full discovery runs 1,736 tests at the base (46 failures, 13 errors, 11 skips)
and 2,159 tests at the candidate with identical failure and error identities,
zero new integration-caused failure identities, and zero Catena failures; the
governed gzip-9 budgets measure CSS 7,629/8,000 whole and JS 12,965/13,000
whole with the suite's stripped-ceiling assertions (2,700 and 8,800) passing
and `catena-model.js` uncapped.

Status: **awaiting independent integration review** under the fixed loop of
one independent Codex integration review, at most one bounded correction pass,
one confirmation review, then merge. E1 is not accepted and not integrated; no
merge to `main`, deployment, or release signing has occurred. The candidate
head is the commit carrying this record.

## E1 Catena bounded integration correction

<!-- promised-deliverable: corpus-browser-catena-e1-integration-candidate-2026-08-28 -->

The independent integration review (branch `review/catena-e1-integration`,
commit `c3698563e3b45e35a672db37616e39ef27eb3d08`) returned **CHANGES
REQUIRED** against the candidate head
`9810a29c38f6138069d11cb7c735d8bb8b190326`, with exactly two `MERGE_BLOCKER`
findings and exactly two `BOUNDED_INTEGRATION_CORRECTION` findings, ratifying
`GenuinelyLateStaleWorkTest` and adding one new `HARDENING_BACKLOG` finding
(the empty no-JavaScript `h2`, untouched here). This is the one authorized
bounded correction pass over those four items and nothing else. The V17
semantic lane stays cancelled, the hardening and evidence-tooling backlogs stay
backlog, the twenty separately owned concerns stay untouched, and the four
Catena release bindings stay unrefreshed.

**Merge blocker 1 — translation-absence identities were flattened together.**
`renderAbsences` appended `.absence-author` and `.absence-work` as adjacent
element children with nothing between them, so a row's flattened text — what a
screen reader announces, what a copy takes, what a text-only rendering shows —
read `Ambrose of MilanHexameron`. Corrected with a semantic DOM delimiter (a
`' — '` text node, written only where both halves are present, matching the
`renderLeads` convention the page already keeps), not with CSS: a margin, a
`gap` or a `::before` would move the spans apart on screen and leave the
flattened text exactly as it was. Reproduced first in real Chromium against the
built artifact, then pinned by `AbsenceRowFlatteningTest` (7 tests) on the real
production route, which reads each row's recursive `textContent` and its
child-node sequence, names the reviewed string as absent and its replacement as
present, and carries an adjacent-identity control over two further real rows
(`Jerome — Liber quaestionum hebraicarum in Genesim`, `Remigius of Auxerre —
Commentarius in Genesim`) so a fix written for one row cannot pass. The
disclosure state, its open-on-arrival contract, the eight reasons and the two
partial offers are asserted unchanged.

**Merge blocker 2 — keyboard recovery focus was invisible.** Recovery moves
focus to `#reading`, and the shared shell's `.reading:focus { outline: none }`
out-ranked the universal `:focus-visible` rule, so the browser drew nothing: a
keyboard reader was moved somewhere the page would not show them. The replay
suite could not see it and both existing recovery-focus classes passed
throughout — the shim has no cascade and no computed style, so `activeElement`
was all it could report. Corrected with one rule,
`.catena-page .reading:focus-visible { outline: 3px solid var(--focus); }`:
higher specificity than the shared suppression, `:focus-visible` only so a
mouse press is left undecorated, `var(--focus)` resolving to the section's own
violet ink so the Catena style is preserved, and `outline-offset: 2px`
inherited from the universal rule because it is not part of the `outline`
shorthand. The shared shell is unchanged and the focus-management behaviour is
not removed. Proved by `tools/tests/catena_recovery_focus_gate.mjs`, a
dependency-free CDP gate over the BUILT artifact, run and asserted by
`RecoveryFocusVisibilityTest` (6 tests): on the success path and on the
reviewed failure/recovery path it reads `getComputedStyle` on the element the
browser reports as active and requires `outline-style: solid`,
`outline-width: 3px`, a ring distinguishable from the same element at rest, and
a computed WCAG contrast ratio at or above 3:1 (measured 10.95:1 against the
region's resolved surface); it also requires a mouse press on a document of its
own to draw no ring, and the next keyboard stop after that press to draw one.
Its falsifiability is not assumed: reverting the two product edits in a copy of
the build fails exactly `absence-rows-read-apart-when-flattened`,
`recovery-focus-is-visible-in-real-chromium` and
`failed-recovery-focus-is-visible-in-real-chromium` with `outline-style is
none — this is the reviewed defect` and `flattened together: Ambrose of
MilanHexameron…`, and nothing else moves. The gate reports nothing rather than
reporting a pass it did not observe: with no Chromium or no built site it exits
3, and the Python test skips with the reason and the variable that would enable
it.

**Bounded correction 1 — curated-suite cleanup, with a measured inventory.**
The forbidden candidate SHA pin (`MODEL_SHA256` and
`test_the_model_is_byte_identical`) is removed and not replaced by another
commit or version pin. Twelve synthetic hostile/evidence-only classes and one
hostile method are removed, and with them the harness machinery that existed
only to serve them: the `Map.prototype` publication probe, the failing-body-write
seam, the prototype-contamination and inherited-accessor transport seams, the
drifting-descriptor and walking-inventory `Proxy` builders, the six-bucket
observation counters, the realm-pollution hook, the projected-row override, the
mutation-attempt authority probe, and the eight journal channels that only they
wrote to. `GenuinelyLateStaleWorkTest` is retained as ratified, with its
`GUARDED` dependency. The 2026-08-11 print pin `test_the_focus_overrides_are_gone`
asserted that no focus rule of any kind lives in `catena.css`, which is wider
than the finding it encoded; it is replaced by
`test_the_only_focus_rule_defers_to_the_shared_role`, which pins exactly one
focus rule, its exact selector and body, the absence of any bare `:focus`, and
its absence from the print block.

The ordinary coverage the first curation lost along with its hostile classes is
restored rather than argued away: chronology grouping, absence counts,
paragraph counts, author-filter recovery, leads copy, shared-field generator
drift, null and list bootstrap truth, visible failure text, and unregressed
Scripture (nine classes, 35 tests, with the seven plain scenarios they read).
The disproved `8 hostile + 40 non-manifest` split is not retained. Counted the
same way for both files — a class is runnable if it defines at least one
`test_` method — the truthful inventory is:

| | runnable classes | tests | dependency-only bases |
| --- | --- | --- | --- |
| corrected candidate suite | 71 | 394 | 3 |
| V16 wave-1 source | 105 | 604 | 3 |
| omitted | 36 | 221 | 0 |
| added by this correction | 2 | 13 | 0 |

Two retained classes are one test lighter than in wave-1 (`FrozenContractTest`
lost the SHA pin; `V15TransportOwnershipTest` lost the write-break probe). All
nine required coverage categories are represented: exact voices, refusal /
absence / provenance, namespace closure, projection and transport ownership,
same-path and late isolation, cache isolation, malformed production data,
governed budgets (`PayloadTest`), and the generator contract
(`V7SharedFieldDriftTest`, which reads `scripts/_catena.py` itself, with
`tools/tests/test_catena.py`). The file is 9,797 lines, down from 12,836.

**Bounded correction 2 — record integrity.** The candidate ledger entry
`corpus-browser-catena-e1-integration-candidate-2026-08-28` had no
`<!-- promised-deliverable: ID -->` marker, which is the one work-register
marker the register requires and the cause of the
`test_promised_deliverables.PromisedDeliverableTests.test_repository_ledger_is_valid`
failure; the marker above is it. The recorded generator command
`scripts/_catena.py check` is not executable as written — the file is mode 644
and a bare invocation returns `Permission denied` — and is corrected to
`python3 scripts/_catena.py check`, which is the command actually run. Full
discovery is rerun at the exact base and the exact corrected head.

Fresh validation at the corrected head: `python3 scripts/_catena.py check`
reports 1,351 fragments / 1 book / 73 canon entries; `python3 scripts/_catena.py
structure` and `paragraphs` regenerate `src/web/data` byte-identically (zero
changed paths); `test_catena.py` passes 56/56 and the corrected curated suite
394/394 including the live Chromium gate; static browser checks pass 5/5;
governed gzip-9 budgets measure CSS 7,921/8,000 whole and 2,698/2,700 stripped,
JS 12,992/13,000 whole and 7,843/8,800 stripped, with no ceiling raised and
`catena-model.js` uncapped; real-Chromium route-only runs over
`/catena/index.html` produce the same 121 assertion identities with the same
95 pass / 14 inherited shared-shell fail / 12 skip statuses at the exact base
`2778285849f2973ea89d1cfd5b2751ed4ae58e54` and at the corrected head, with zero
status changes and zero identity changes; full discovery runs 1,736 tests at the
base and 2,134 tests at the corrected head, both reporting 46 failures, 13
errors and 11 skips over the identical 24 failure identities and 13 error
identities, so there are **zero new integration-caused failure or error
identities** and zero Catena failures.

Status: **awaiting one confirmation Codex review**, scoped to these four
corrections and a regression check. E1 is not accepted and not integrated; no
merge to `main`, deployment, release signing, or self-acceptance has occurred,
and no new hardening lane was opened.

## E1 Catena integration merged to main

The confirmation review (branch `review/catena-e1-integration-confirmation`,
durable review commit `7dfd944494a8d9355264579156214f16d3722a9f`) examined the
corrected candidate against the pre-correction head
`9810a29c38f6138069d11cb7c735d8bb8b190326` and the integration base, and
dispositioned the line **`CONFIRMED — CATENA E1 INTEGRATION READY TO MERGE`**.
Acting only on that disposition, the exact confirmed candidate
`b832cdc5bc01391cea67c01437318d25e0c7c315` was merged into the exact reviewed
`main` head `004615faf506eb4083d484d41b18ee1c61f0aa7f` as a true merge
commit, preserving both parents rather than squashing or rewriting either lane.

The merge-tree rehearsal and the merge itself found exactly the two textual
conflicts the confirmation review predicted, both append-only records, and no
production, source, test, data, configuration, shared-shell, Liturgy, or PDF
conflict. `PROJECT-WORK.md` kept both lanes whole: every current-main Missal
remediation and post-base record, and every Catena E1 integration,
bounded-correction, and confirmation record, with nothing deleted and nothing
duplicated. `promised-deliverables.toml` needed the structural care the
confirmation reviewer flagged — the shared `[[deliverables]]` header sat above
the hunk and a single array terminator below it, so concatenation would have
nested one deliverable inside another — and was resolved into two complete
independent entries, each with its own header and every array closed:
`complete-missal-remediation-2026-08-26` unchanged at `complete`, and
`corpus-browser-catena-e1-integration-candidate-2026-08-28` moved from
`candidate` to `complete` with one added requirement recording the confirmation
review and this merge. The ledger validates at 32 tracked and 24 complete with
no duplicate identifier, and `test_repository_ledger_is_valid` passes.

The merge introduces exactly thirteen paths against current `main`: the twelve
tracked manifest paths and the one authorized new gate
`tools/tests/catena_recovery_focus_gate.mjs`. The merged index carries no
content delta from the confirmed candidate across
`src/web/browser/catena`, `scripts/_catena.py`,
`src/web/data/structure/catena`, `tools/tests/test_catena.py`,
`tools/tests/test_catena_production.py`, and that gate, so no Catena
production, test, or generated byte was altered by conflict resolution. No
shared shell, Liturgy, PDF, release-binding, deployment-configuration, or
unrelated data or CLI path was touched.

Minimal post-merge validation on the merged tree: `python3 scripts/_catena.py
check` reports 1,351 fragments / 1 book / 73 canon entries;
`tools/tests/test_catena.py` passes 56/56; the curated production suite passes
394/394 with zero skips, the real-Chromium recovery-focus gate executing rather
than skipping and reporting a measured focus-ring contrast of 10.95:1 with no
failed assertion; the static browser checks pass 6/6, which is current `main`'s
own count after it added a sixth check above the integration base and therefore
supersedes the candidate-era 5/5; and the real-Chromium route-only run over
`/catena/index.html` reproduces the confirmed status universe exactly at 121
assertion identities, 95 passing, 14 failing and 12 skipped, with the fourteen
failures being only the inherited shared-shell identities
`single-main-element` (9) and `primary-controls-meet-target-size` (5), which
are separately owned baseline rather than merge blockers.

Nothing beyond the merge was reopened. The three hardening findings remain
`HARDENING_BACKLOG`, the eight package/history/replay/scanner defects remain
`EVIDENCE_TOOLING_BACKLOG`, the twenty release, shell, data, validation,
Liturgy, PDF, and final-integration concerns remain `SEPARATELY_OWNED` and
untouched, and the V17 semantic lane stays cancelled. At the merge commit the
Catena release bindings were still unrefreshed and no release record had been
re-signed; the section below records why that could not stand and what was
authorized instead. The push that advances `main` authorizes only the
repository's automatic GitHub Pages attempt that any `main` push triggers,
which is not itself evidence of a verified live snapshot.

## E1 Catena release bindings refreshed so the merged bytes can publish

The merge commit `85f41e4e467d5f4b4331ee71da0666a1c0ebddf9` reached `origin/main`
with the confirmed Catena bytes and the Catena release bindings deliberately
left as the integration lane had them. Pages run
[`33265104292`](https://github.com/spincyc/triptych/actions/runs/33265104292)
therefore failed at `public-alpha verify --deployment-target github-pages`, the
gate that refuses when a site source no longer matches its approved SHA-256:
authorization `perpetual-public-repository-2026` still recorded the
pre-integration hashes for `catena-model.js`, `catena.css`, `catena.js`,
`index.html`, and `src/web/data/structure/catena/index.json`, and had no record
at all for the newly generated `src/web/data/structure/catena/27-is/008.json`.
The run stopped before Configure Pages, Upload, and Deploy, so nothing was
published and deployment `6158143411` ended `failure`; the live site continued
to serve the previous `004615faf` snapshot throughout. This was the predicted
consequence of landing accepted integration bytes while their approved record
still described the superseded ones, not a defect in the merge: the merged tree
carries no content delta from the confirmed candidate.

Refreshing that record is release-owned re-signing, which the merge lane
explicitly withheld, so it was not done as part of the merge. The maintainer
then authorized it directly. `make refresh-release-bindings ADOPT=1` was run
under `ONLY=` naming exactly the six affected paths, so the authorization
carries only the reviewed Catena bytes forward and could not sign for any other
entry; it re-recorded the five changed site sources, adopted the one new
generated file, and updated the rights table and its `rights_record_sha256`,
which are mechanically derived from those same paths. No hash was hand-edited
and no approval note was invented. `make check-release-bindings` then reports
`exact: 0 stale binding(s)`, and every re-recorded value equals the hash of the
file as merged.

All three gates the Pages workflow itself runs then passed locally on the exact
refreshed tree: `make check-deployment-sources`, `make public-site`, and
`python3 tools/tpt public-alpha verify --deployment-target github-pages`, the
last reporting `verified build/public-alpha/site`. The Catena integration
validation above was not rerun and is unchanged; this work touched only
`release/public-alpha.json` and `release/rights/public-alpha-2026-07-15.md`. The
hardening and evidence-tooling backlogs, the twenty separately owned concerns,
and the V17 cancellation all remain exactly as the merge left them.

## Fan-out lanes share one scratch directory, 2026-09-02

During the `proper` v17 run `ca03f1b357e7ec25` (Claude, Fourteenth Sunday after
Pentecost), the seven research lanes ran concurrently and two of them worked in
the same scratch directory. The `patristic-reception` lane reported that a
sibling overwrote its `build.py` mid-run, under a filename either lane would
plausibly have chosen; it noticed, re-established its work under a
lane-specific subdirectory, and lost no findings. Nothing else noticed. The
lane reported it in the prose of its own hand-back, and there is no check that
would have reported it otherwise.

The cause is that the `FANOUT / HOST-MAX` execution policy — composed in
`_driver_instructions` in `scripts/_workflow.py` — dictates a great deal about
dispatch and nothing about where a lane works. It fixes the lane count, forbids
inventing or combining lanes, pins each result to its `lane_packet_hash`, and
reserves the join to `tpt`. All of that protects lane *identity*. None of it
can see a lane whose evidence was computed by a script a sibling replaced,
because the driver, not the workflow, decides where lanes work, and every
concurrent delegate inherits the same default working area from its host unless
its brief says otherwise. That a research lane is read-only with respect to the
repository does not help: it writes no tracked file and still writes scripts and
intermediate output.

This is §1 of `guidance/the-shape.md` arriving in the apparatus again — a
script that resolves successfully and wrongly. The failure mode is silent by
construction: a lane that had not happened to notice would have returned
findings computed by another lane's code, correctly shaped, correctly hashed,
correctly joined, and wrong.

Nothing in the engine was changed while a run was in flight. The coordinator
instead gave every subsequent stage of that run a `.scratch/<stage>/`
directory of its own by hand, and the maintainer's own delegation guidance was
amended so that a lane brief must name the lane's scratch directory — an
unnamed one is a shared one.

Owed to this repository, and not yet done:

- Extend the `FANOUT / HOST-MAX` policy text in `_driver_instructions` to
  require that each lane be given a working area of its own, disjoint from
  every sibling's. Keep it host-neutral: the engine should state the
  requirement, not name a path shape belonging to one host.
- Update the two tests that assert on that text —
  `tools/tests/test_workflow_execution_policy.py:372` and
  `tools/tests/test_workflow_research_fanout.py:696` — and the policy
  descriptions in `workflows/OPERATOR.md` (lines 184, 231) and
  `workflows/ARCHITECTURE.md` (line 788).

The rule belongs in the driver instructions and not in
`workflows/fragments/common/agent-brief.md`, for two reasons. It is the
dispatcher's decision, not the worker's: a lane cannot allocate itself a
directory disjoint from siblings it cannot see. And `workflow_source_digest`
covers the pipeline JSON, every fragment, and the schemas, but not
`scripts/_workflow.py`, so amending the policy text moves no recorded digest
and invalidates no run in flight, whereas amending the fragment would
invalidate every one.

## Run state is called durable and is not, 2026-09-02

`workflows/OPERATOR.md` opens its run-state section with "Each run has a
durable state directory" and then names `build/tpt-runs/<run-id>/`. Nothing
about that path is durable. `.gitignore` line 1 is `/build/`, so no run state
has ever been tracked; `make clean` is `rm -rf build`; and in a `wt` agent
workspace `wt tidy` deletes everything the clone ignores, without asking. The
word is load-bearing and it is wrong.

It is load-bearing because step 11 of
`workflows/fragments/propers/research-synthesis.md` makes that directory the
carry-forward mechanism. The integrator is told to find earlier productions of
the same target with

    grep -l '"proper": "{proper}"' build/tpt-runs/*/state.json

and to read every `content-evaluation` and `research-synthesis` result those
runs recorded, so that the blocking findings of an earlier production are
carried into the brief rather than spent twice. The fragment knows the hazard
it is guarding: it records that re-seeding starts a run with an empty history,
and that one real re-seed dropped fourteen standing evaluation findings, of
which five were recovered only because a person carried them by hand and one
survived into the next production verbatim because nobody did.

In run `ca03f1b357e7ec25` that lookup returned only the run performing it.
`build/tpt-runs/` held exactly one directory. The leaf's own
`research/scope.md` names seven run ids; six of them are prior productions
whose directories are gone. The carry-forward nonetheless mostly held, because
each integration had copied the previous findings into the tracked brief — but
that is a convention observed by successive workers, not a mechanism. A
`research-synthesis` result reaches a tracked file because writing the brief is
the stage's job. A `content-evaluation` result reaches nothing tracked at all.

So it has already broken once, in the direction the design leaves open. §12.5
of the brief records run `e5b24f405bde9691` as unrecoverable: this run could
not read its `content-evaluation` results or its escalations, and therefore
cannot say whether a content evaluation ran against the leaf after it and
raised anything. The brief states the hole instead of papering over it, which
is the right disposition and not a repair.

This is the same defect as the fan-out scratch collision recorded above, in its
larger form: state a later stage is required to read, kept only where nothing
preserves it, failing silently and leaving an artifact that looks complete.
§1 of `guidance/the-shape.md` again, and again in the apparatus.

Owed to this repository, and not yet done:

- Correct `workflows/OPERATOR.md`. Either the directory stops being described
  as durable, or it becomes durable; describing an ignored, `rm -rf`-able path
  as durable is the part that misleads a reader deciding whether to preserve
  anything.
- Give a run's blocking findings and escalations a tracked home, so
  carry-forward reads a committed record rather than an ignored directory. The
  brief already serves that purpose for `research-synthesis`; the gap is
  `content-evaluation`, whose findings are the ones step 11 most wants and the
  ones nothing preserves.
- Have step 11 say what an empty lookup means. An absent run directory and an
  absent prior production are indistinguishable through that `grep`, and the
  fragment asks the integrator to tell them apart using the very directory
  pruning empties.

Unlike the fan-out policy text, `research-synthesis.md` is a fragment, and
`workflow_source_digest` covers every fragment's bytes. Amending step 11
invalidates every run in flight, so it is done between runs, never during one.

## Run ca03f1b357e7ec25 blocked with eight findings outstanding, 2026-09-03

The `proper` v17 run against
`liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost`,
provider `claude`, reached BLOCKED at the `content-evaluation` iteration bound:
three of three iterations ended with a finding the stage had already raised
still unrepaired. Nothing was built into `pdf/` or `web/`, nothing was
installed, and no release binding moved. The leaf as the run left it is
committed as work in progress, and this section is where its outstanding
findings live: the run's own results are under `build/tpt-runs/`, which is
ignored output that `make clean` and `wt tidy` delete without asking, and a
`content-evaluation` result reaches nothing tracked on its own.

### The eight outstanding findings

Every one is `repair_target: authoring`, and every one is unrepaired.

| id | lane | where | what it requires |
| --- | --- | --- | --- |
| `CON-REC-002` | reception-sweep | `sections/90-scope.tex` 146–150 | The appendix says Theodoret was read in Greek at Pss. 33, 83, 94 and 117. `research/scope.md` §4.2 records Ps. 33 as **deliberately not fetched** (the acquired volumes are Tomus 2, Pss. 71–87, and Tomus 3, Pss. 87–150). Correct the reach to Pss. 83, 94 and 117 and state the negative it conceals: no Greek witness in this sweep expounds the Offertory's Ps. 33 at the appointed verses. Make the item count agree with the list it heads. |
| `CON-REC-003` | reception-sweep | synthesis edition; dangling back-reference at `sections/90-scope.tex` 267 | The Secret's and Postcommunion's reception negative is printed only in the canonical edition, while the shared appendix bounds a negative the synthesis reader is never given. Carry it to that reader with its bound — no patristic or medieval exegetical reception located for either prayer, bounded over a Patrologia Latina exact-phrase index, the Collect expressly outside it — without creating a second authority. |
| `CON-SYN-002` | synthesis-argument | `sections/synthesis/20-integrated-commentary.tex` 26–30 | The one unit treating the orations partitions the formulary on an element set the appointed Latin does not bear: the `salut-` root stands four times and the fourth is the Alleluia's `salutári`, a sung element. Restate it as C6, the brief synthesis and P3 already do — `salut-` once each in Collect, Alleluia, Secret and Postcommunion; `propitia-` in Collect and Secret only; `semper` and `perpetu-` in Collect and Postcommunion only. |
| `CON-CIT-004` | citation-integrity | `sections/99-references.tex` 5–9 | The References explain that Papias and Eusebius are "named on page 2" as bounded negatives. Page 2 was rebuilt this run and names neither; that sentence is the only occurrence of either name in the leaf. Delete the sentence or restore the page-2 negatives it answers. The standing bound — this repository holds no record of either and nothing is asserted from them — survives either way, and the Jerome and Hesbert narrowings beside it are accurate and stay. |
| `CON-CIT-020` | citation-integrity | `sections/35-source-grounded-synthesis.tex` 249–254 **and** `sections/synthesis/20-integrated-commentary.tex` 223–226 | Both assert a uniform two-Sunday Gelasian offset "with no exception". The leaf's own commentary and `research/scope.md` §6.1(a) give N+2 across Book III sects. I–XI and N+4 across XII–XVI, with Pamelius at N+1 unbroken. Report the split; "uniformly" and "with no exception" go, or attach only to Pamelius, of whom they are true. |
| `CON-CIT-021` | citation-integrity | `sections/50-interpretive.tex` 140–149 (P4), `sections/20-themes.tex` 86–90, `sections/synthesis/20-integrated-commentary.tex` 212–218 | The hope-formula P4 rests on is printed as `beatus … qui sperat in eo` "at the close of Ps. 33 (v. 23)". Ps. 33:23 has no `beatus` and a plural verb; Ps. 83:13 reads `in te`; the Gradual contains neither word. Give the loci as Ps. 33:9b and Ps. 83:13, differing in the prepositional object, and describe the Gradual as singing the hope *vocabulary*, not the formula. |
| `CON-CIT-022` | citation-integrity | `sections/99-references.tex` 24 | The `Rubricae generales` entry lists RG 77 and RG 465, cited nowhere in the guide or its records, and omits RG 18, which is cited. List the numbers the guide actually cites — RG 18, 117, 127 b, 434 b, 435. The facsimile identity, page range and artifact id are correct and stay. |
| `CON-PRO-003` | profile-conformance | `sections/30-commentary.tex` (~40 sites) **and** `sections/synthesis/20-integrated-commentary.tex` | **This is the finding that hit the bound.** Reader-facing prose still takes the guide, its sweep, or the repository's holdings as its grammatical subject, and each edition still prints a disclaimer `guidance/editorial.md` forbids outright: `the disagreement is preserved rather than adjudicated` (`30-commentary.tex` 1296) and `that displacement is not smoothed over here` (`synthesis/20-integrated-commentary.tex` 210). It was repaired in the canonical edition at iterations 1 and 2 and **survived both times in the synthesis file**, which neither repair reached. |

### Two facts about this run's provenance

**The run is not replayable and must not be advanced.** From iteration 2 the
coordinator added to each lane brief an instruction that was not in that lane's
packet: that the leaf builds two editions from one source tree and a repair to
one is not a repair to the other. The fan-out execution policy directs a driver
to give each lane its packet "and nothing else" and not to supplement a lane's
work. Iteration 2's lane results are therefore not a function of their packets
alone, a replay of `ca03f1b357e7ec25` would not reproduce them, and the run is
to be read as a record and not resumed.

**Two findings cite that out-of-packet instruction.** `CON-REC-003` and
`CON-CIT-020` name it in their own text as what prompted them. Both were
checked against the leaf when this entry was written and both are real, but a
reader should verify them against the leaf rather than treat them as
packet-derived evidence.

Both facts cut the other way as well, and the entry above is the place to say
so: the same blind spot the hint named is why `CON-PRO-003` survived three
rounds in a file no reviser was told to open, and it is what ended the run.

### Finding ids were not stable across iterations

Twenty distinct ids were raised across the three rounds and twelve cleared.
That is a count of ids, not of defects: the citation-integrity lane reused
`CON-CIT-001` and `CON-CIT-003` at iteration 1 for defects unrelated to those
it gave the same ids at iteration 0 — the first pair concerned the Cummiskey
translation-ledger citations and the barred Migne columns, the second the
unnamed translators of Guéranger and Schuster and an invented two-century
interval between Honorius and Godfrey. `common/result-format.md` requires that
an id name the same issue every time it appears. A carry-forward that reads
these results by id will conflate them unless it reads each finding's text.
