# Handoff: the Fifteenth Sunday, blocked three findings short

Written 2026-09-09 on `feature/claude/propers/tlm/55`, at the end of a session
that drove workflow `proper v25` run `2bd4a1ab7521853d` from an empty leaf to
`BLOCKED`. The leaf is complete and builds; it stopped on the workflow's
absolute iteration ceiling, not on a failure to repair. Read
`HANDOFF-proper-54-convergence.md` first if you have not: this run is the
convergence work of that session being exercised for the first time on a leaf
authored from nothing.

## The run

| | |
| --- | --- |
| run id | `2bd4a1ab7521853d` |
| workflow | `proper` v25, digest `ad4a5ea8193bdaf4b5f7a3f261fd5377fd49208f49b709cd794aeb635d20cd46` |
| seed commit | `b743814e521622eb8dbea56316e6138d45e8f7f3` |
| document | `liturgy/roman-rite/1962/propers/temporal/55-fifteenth-after-pentecost` |
| provider | `claude` |
| final state | `BLOCKED` — 36 packets emitted, 36 results received, 0 refused |

Stage executions: `research` 1, `research-synthesis` 3, `source-registration` 3,
`author-proper` 3, `content-preflight` 8, `content-evaluation` 8,
`content-revision` 5. The run never reached `build-artifacts`; 13 pipeline
stages after `content-evaluation` were never run.

## Why it blocked, and why that is not a repair failure

```
iteration limit exceeded for content-evaluation: 8/8 consecutive failures.
The repeat budget (3/4) never ran out because no round reported a repair it
could not make; the absolute ceiling stops a stage that finds something new forever.
```

The two counters in `_failure_budget_spent` say different things and the
difference is the whole result.

- **`stage_repeats` finished at 3 of 4.** This is what `max_iterations`
  bounds, and it charges only when a reviser reports a finding it attempted
  and could not repair. It was charged once, on the first failure of the
  streak, and never again. **No reviser in this run ever returned a
  `not-repaired`,** and every one of those reports was independently verified
  against the files before it was submitted.
- **`stage_failures` reached 8 of 8.** `max_total_iterations` defaults to
  `2 * max_iterations`, the test is `count >= ceiling`, and it charges every
  consecutive failure whatever the reviser reports.

So the run died in exactly the case the budget's own docstring reserves that
ceiling for: "this ceiling is reached only by a stage doing genuine new work
every time." Eight evaluations each found new defects. None of the three
findings standing at the end is a survivor of any earlier round.

**Do not read this as a converging run that was cut off arbitrarily.** It is
also true that the leaf never got clean, and that the last three rounds each
found three fresh defects in prose that seven prior max-effort evaluations had
passed over. Whether that is a document that needed two more rounds or a
document whose defect density was never going to reach zero under this
criteria set is the open question — see *The structural finding* below.

## Round by round, and what drove each re-iteration

Blocking counts and the route each round took. `brief` route means the
earliest owner named was `research-synthesis`, which re-ran `author-proper`
after it; `authoring` means `content-revision`.

| round | blocking | route | what drove the next iteration |
| --- | --- | --- | --- |
| it0 | 18 | authoring | first evaluation of the first draft |
| it1 | 17 | **brief** | one `brief` finding won the route; the 16 `authoring` findings travelled as `CARRIED_FINDINGS` |
| it2 | 10 | **brief** | again a brief defect; `research/scope.md` repaired twice, then re-authored |
| it3 | 5 | authoring | first round where the brief was sound; pure revision from here on |
| it4 | 5 | authoring | count held at 5 but every id was new — the it3 five were all cleared |
| it5 | 3 | authoring | `CON-CIT-019` was **introduced by the `CON-CIT-016` repair** |
| it6 | 3 | authoring | `CON-EVI-024`, a 22-site orthography defect, found for the first time |
| it7 | 3 | — | ceiling reached; run blocked |

Convergence in blocking findings: **18 → 17 → 10 → 5 → 5 → 3 → 3 → 3.**

Three things are worth extracting from that table.

1. **The `brief` route is expensive.** Two rounds went to
   `research-synthesis`, and each cost a re-authoring of the whole leaf
   (`author-proper` ran 3 times, not once). Both were real brief defects, but
   between them they consumed a quarter of the run's total budget.
2. **A repair introduced a defect at least once, provably.** `CON-CIT-019`
   ("four words" where the Latin yields no such count) was created by the
   previous round's repair of `CON-CIT-016`. That is the strongest argument
   for the smallest-change discipline, and against broad rewrites late in a
   run.
3. **`CON-PRO-002` needed a change of method, not more effort.** The
   declarative-discipline habit survived two site-by-site repairs. It cleared
   only when the third reviser was told the named-site approach had failed
   twice and swept the class by taxonomy instead — it rewrote 25 sites, 13
   named and 12 it found itself, and `profile-conformance` returned a clean
   PASS and stayed clean for the rest of the run. The same move worked again
   at it6 (`CON-EVI-024`), where a scripted sweep against the tracked edition
   found a 23rd site no lane had named.

## What stands: three blocking findings

All `authoring`, all in `evaluations/blocking-findings-v1.toml`, all verified
by the driver against the files before the run was advanced.

| id | file | defect |
| --- | --- | --- |
| `CON-EVI-027` | `sections/90-scope.tex` 39–43, `sections/99-references.tex` 25–27 | Says all three older Missals were "classified degraded in their own source records". The Pustet Ratisbon 1862's artifact record classifies its layer **`prose-latin`** (Latin function-word share 0.1792, comfortably above the ~10% threshold); only the Venice 1570 is `degraded-latin`. The Pustet's only "degraded" string is `pdf_degraded = invalid-page-size`, about the PDF derivative. Load-bearing: the Pustet layer corroborates seven reported readings, and this is the sentence telling a reader what that corroboration is worth. `research/source-bindings.toml:115` already restricts the attribution correctly. |
| `CON-EVI-028` | `sections/40-notable.tex` 93 | Prints `exspectavi` — the missal's `xs` cluster without the missal's acute. The appointed form `exspectávi` is correct at four sites including line 71 of the same entry; Sorley's title `expectavi` is correct at three others. A third form belonging to neither identified text. (`sections/30-commentary.tex:825` also reads `exspectavi`, but that is Cassiodorus's unaccented PL lemma and is correct.) |
| `CON-CIT-026` | `sections/20-themes.tex` 122–125 | "at three places in this Mass's two psalm-antiphons Augustine's lemma is not the chant's" — the leaf's own commentary produces four: three at Ps. 85 (`30-commentary.tex` 239–245) and a fourth at Ps. 39 (`30-commentary.tex` 793–795, "his lemma is not the antiphon's… `Attendit mihi`"). The brief holds five. The sentence's Cassiodorus half is correctly scoped to both antiphons, which is what makes the Augustine half read as a total. |

All three are leaf-local and need no retrieval. The evidence each repair needs
is already in `research/scope.md`, `propers/verified.md`, or the tracked
`src/sources/` records named above.

## Seven escalations waiting for a maintainer

These are in artifacts **no stage of this workflow may write**. They do not
block and they were never repairable here. They live in the run's escalation
ledger under `build/`, which `make clean` removes and `wt tidy` sweeps — this
document is now the durable copy.

| id | target | decision needed |
| --- | --- | --- |
| `CON-CIT-012`, `CON-EVI-011` | `src/sources/inventories/roman-1962-proper-translations-v1.toml` ~5881–5916 | The three `pentecost-15` `[[untranslated]]` rows type the Cummiskey 1861 orations `rights-withheld` "until a binding exists", while the tracked artifact and three passage records exist and two are `verified`. Same disposition covers `pentecost-13` and `-14`, so it is repository-wide. Either clear the rows or withdraw the passage records' publication basis. |
| `CON-EVI-008`, `CON-EVI-012` | `.../philadelphia-1861/passages/post-pentecosten-15--secret.toml:16` and `--postcommunion.toml:16` | Both records state verification against the **wrong Latin** — marginal 1571 for a Secret that is 1589, and a different prayer entirely at 1573 for a Postcommunion that is `Mentes nostras et corpora possideat` at 1591. Both marked `verified 2026-07-25`. The English they carry is right; the verification note is not. Amending moves fingerprints and the bindings pinned to them. |
| `CON-EVI-007`, `CON-EVI-013` | `.../antiphonale-missarum-sextuplex/editions/vromant-1935/edition.toml` | Every antiphonary datum in both editions rests on gregorien.info's index, which that record calls "a lead, not a substitute for Hesbert's pages", and no US redistribution basis was established. Criterion 2 asks that a secondary citation be checked against the edition; here it can never be. Commission a rights review, or record the index as the permanent ceiling. |
| `CON-PRO-004` | `tools/check-proper-components` 142, 240–254 and `tools/tests/test_proper_components.py:102`, against `guidance/liturgy/roman-1962-propers.md` 163, 168–179, 246–263 | **The gate and the profile require opposite orders.** The profile puts `Notable and Quotable` at reader position 7 and `Interpretive Possibilities` at 8; the check requires `exploratory-synthesis` *before* `notable-quotable` in `[[components]]`. Every 1962 leaf in the repo — all six Claude and all seven GPT leaves — declares a manifest order its own profile forbids, while `main.tex` renders the profile's order. The finding proposes three concrete resolutions. |

`CON-PRO-004` is the one to fix first. It is repository-wide, it makes
criterion 9 unanswerable without a convention every lane has to rediscover,
and its fix is mechanical and changes no rendered page.

## The structural finding: observations do not route

Nine observations reached the tracked record. Three of them are **real,
reader-facing factual errors that this run could not repair**, because
`observations` carry no severity and no `repair_target` by design, and the
workflow states that no later run reads that file back.

- `sections/20-themes.tex` 32–34 and `sections/50-interpretive.tex` 22 — "the
  incapacity is stated before anything at all is asked" / "before it asks
  anything". The Collect opens with a petition (`Ecclésiam tuam, Dómine,
  miserátio continuáta mundet et múniat`); the incapacity clause follows it.
  Raised at **three consecutive evaluations**. `20-themes.tex:39` states the
  accurate form two lines later.
- `sections/20-themes.tex` 30–31 — "The two prayers that frame the communion
  rite", naming the Collect and the Postcommunion. The Collect belongs to the
  Mass of the Catechumens; the pair frames the Mass.
- `sections/50-interpretive.tex` 11–12 — the exploratory notice says the
  precedent search is "summarised in the terminal appendix". It is not;
  `90-scope.tex` names the record and enumerates what it holds. Raised at
  **four consecutive evaluations**.

**Four separate lanes independently called this a missing criterion**, in the
`note` field, on the terms the shared fragment invites. Nothing in the twelve
criteria asks whether a claim inside a synthesis unit or an exploratory
proposal is *true*: criterion 2 covers transcription of the appointed Latin,
criterion 7 covers stated counts and citations, criteria 4 and 5 cover
structure and mandated fields. A false assertion about what a printed prayer
says falls between all of them.

Two further recurring observations point the same way:

- `sections/90-scope.tex` 80–81 prints this workflow's own vocabulary
  ("reconciling it belongs to the lane that owns it") to a reader. Criterion
  12 exempts the appendix wholesale, and `scripts/_house_voice.py` masks
  `Appendix\b.*` before its rules run, so the one mechanical rule matching
  that exact form never sees it. Three rounds.
- Several observations record places where **`research/scope.md` is wrong and
  the leaf is right** — the Wilson numbering witnesses ("four" against its own
  five sigla), the Hebrews `Hodie` returns ("four" against three of five
  loci), the formulary extent (pp. 396-398 against `verified.md`'s 396–397),
  and §1.1's "exactly one place" against its own §6. No criterion owns the
  factual correctness of the brief: criterion 10 reaches it for existence and
  format only.

**If you change one thing before the next run, make it this.** A criterion
that asks whether reader-facing assertions about the appointed texts are true,
owned by one lane, would have caught all three factual errors, and probably
several of the defects that arrived late as `CON-CIT-` findings.

## What the driver verified, and where it was wrong

Every lane and reviser claim that decided a transition was checked against the
files before the run advanced — `make check-sources` attribution, the LXX
3 Kingdoms verse position, the Clementine Ps. 94 title, the Communion
antiphons in `src/sources/calendars/roman-1962/propers.yaml`, `research/scope.md`
hashes at every round, `src/sources/` mtimes at every round, the Clementine
orthography, the Pustet classification, the sacramentary counts, and a full
re-run of `check-content-preflight` before each submission. Every one of the
five-lane submissions was schema-validated before `advance`, because one
malformed finding refuses all five lanes and costs a whole round trip. None
was ever refused.

Two driver errors are worth recording so they are not repeated:

1. **A wrong clearance.** At it5 the driver verified the "three places…
   Augustine's lemma" figure and reported it correct. It was not — the leaf
   states a fourth departure at `30-commentary.tex:793` in terms, and the
   check had grepped for the quoted Latin and read line 795 as exposition
   prose. `CON-CIT-026` is that error surfacing two rounds later. **Grepping
   for a quotation is not the same as reading the sentence that frames it.**
2. **A budget misstatement.** The driver initially told the user that repeated
   finding ids charge the iteration budget. They do not, on this route: the
   engine reads the reviser's `finding_dispositions`, and the docstring says
   in terms that id collision across iterations is architecturally guaranteed
   and "comparing ids across iterations compares nothing."

Two recoveries from host rate limits are also on record. Both times the
correct move was to **verify state, then resume the agent rather than restart
it** — the agents held their packets and partial sweeps in context. The it6
`evidence-discipline` lane, resumed and challenged on its own unfinished note,
found two more sites, removed a false brief reference, and corrected four line
spans. A restart would have lost that.

## How this session drove the workflow, in case it helps

- **Packets were handed by absolute path plus sha256 once they exceeded a few
  KB,** with an explicit statement that nothing had been abridged. Retyping a
  46 KB packet into a prompt risks transcription drift; reading the bytes does
  not. Every lane echoed its `lane_packet_hash` and none was ever rejected.
- **Evaluators were never told the budget position.** A lane that knows the
  run is one finding from death is not an independent lane. Revisers *were*
  told, together with an explicit instruction that a false `repaired` is the
  worse outcome and that the run should block honestly instead.
- **The driver never wrote a finding of its own.** Where a real defect had no
  owner, it was left in `observations` and reported to the user. Injecting it
  as work would have made the run unreplayable from its own packets, which is
  the failure the fan-out policy exists to prevent.
- **Standing ids were passed to lanes as "spent", never as "still true",**
  with the numbering floor stated. Lanes were told what not to reuse, not what
  to find.

## Resuming

The leaf is three small, localised repairs from a clean content evaluation.
Nothing about it needs re-research: `research/scope.md` has been byte-identical
(`e4c44c66794dcd1c…`) since it was written, and `src/sources/` was never
written outside `source-registration`.

A fresh `proper v25` run over this leaf starts at `authorize-target` with a
document three defects from clean rather than from nothing, and gets a full
budget. That is the straightforward route. Before starting it:

1. Fix `CON-PRO-004` — it is repository-wide and cheap.
2. Consider adding the truth-of-assertion criterion described above, and
   fixing the three observation-only factual errors by hand, since a new run
   will not repair them either.
3. Note that `content-evaluation` has `max_iterations: 4` and therefore a
   ceiling of 8. A leaf of this density used all of it. If the criteria set
   grows, the ceiling should probably grow with it.

The build tree under `build/` is ignored and stale; `build-artifacts` never
ran, so no PDF in this branch is authoritative. Both editions do build — 35
and 22 pages, twelve preflight checks passing — as of the final revision.
