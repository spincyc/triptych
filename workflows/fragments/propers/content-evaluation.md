# Content / Evidence Evaluation

## Your task

You are a fresh evaluator. Evaluate the content and evidence quality of the
canonical proper leaf. Do not rediscover what mechanical gates will check
later (build success, PDF existence, undefined references). Focus on
scholarly content.

## Evaluation criteria

1. **Evidence discipline**: Are the five evidence states kept distinct
   (verified source text, checked quotation/paraphrase, source-grounded
   synthesis, editorial/AI proposal, unverified lead)?
2. **Source verification**: Are claims verified from primary, official,
   edition-identified sources? Are OCR and secondary citations treated as
   leads until checked?
3. **Reception sweep**: Was a broad and deep patristic/saintly reception
   sweep conducted for each appointed passage? Are direct witnesses retained
   where found?
4. **Cross-proper synthesis**: Is the synthesis a redistilled cross-proper
   argument (not an abridged procession)? Does each unit draw from multiple
   elements and witnesses?
5. **Exploratory proposals**: Are proposals labeled as exploratory? Does each
   join at least 2 elements?
6. **Material disagreement**: Are disagreements, uncertainty, and
   currentness preserved rather than silently harmonized?
7. **Citations**: Are only sources actually used cited? No invented searches,
   verifications, quotations, attributions, doctrines, laws, or historical
   facts?
8. **English rule**: Is English quoted from registered public-domain
   witnesses (Douay-Rheims for scripture, public-domain hand missal for
   orations)? No composed/translated/adapted English?
9. **Pagination**: Does the content structure match the required reader order
   and page assignments from the profile?
10. **Provenance**: Do source records (verified.md, retrieved.txt, scope.md)
    exist and follow the profile's format?

## Lane scope

This stage is a fan-out stage: the criteria above are partitioned across
the workflow's evaluation lanes, and the lane fragment that follows names
exactly which of them you own. Report findings for your own criteria only.
Another lane owns each of the others, and tpt joins every lane's findings
itself.

## Repair ownership

Every **blocking** finding must name who has to repair it:

```json
"repair_target": "research" | "brief" | "authoring"
```

Ask the three questions in this order and stop at the first yes.

- `research` — **does the repair need retrieval that has not happened?** No
  record in the brief supports the claim and none could without a fresh sweep:
  the witness was never obtained, a reception field was never swept, a source
  the claim depends on was never read. Only a research lane can go and get it.
- `brief` — **is the material already held, and stated wrongly?** The brief has
  the evidence and misstates it — a wrong locus, a wrong edition, a relation
  named against the component manifest — or it recorded a bound and does not
  carry that bound forward into what it asserts. Nothing new has to be
  retrieved: the correction is a sentence of `research/scope.md`, which no
  stage but `research-synthesis` may touch.
- `authoring` — **is the brief adequate, and the leaf departing from it?** The
  prose, the structure, or the use of citations in the canonical leaf is
  defective while the brief it was written from is right.

`brief` exists because `research/scope.md` has exactly one writer,
`research-synthesis`, and so a defect in the brief can be repaired in no other
stage. Naming such a defect `research` does not reach that writer any sooner:
it discards the brief and re-runs every research lane only to arrive back at
the same stage with the same evidence.

The line between `research` and `brief` is retrieval, not severity. A worked
example: the brief cited the Gelasian Postcommunion at "Book II sect. LXIX,
p. 207", where the printing's own contents put the Vigil at sect. LXVIII,
p. 206. The witness is held, the reading was taken, and the locus is written
down wrong. That is `brief`. It would be `research` only if the witness itself
had never been obtained.

`tpt` reads this field and routes the repair itself, in the order the workflow
declares its routes — `research`, then `brief`, then `authoring`. The earliest
owner that any blocking finding names wins, and only the findings that named
that owner travel the route:

- any finding naming `research` → the `research` stage, then
  `research-synthesis`, then `author-proper`, then a fresh content evaluation;
- otherwise, any finding naming `brief` → `research-synthesis`, then
  `author-proper`, then a fresh content evaluation;
- otherwise → `content-revision`.

You do not choose the route and the controller does not choose the route: the
field decides it.

Because the earlier owner is corrected first and everything downstream of it is
regenerated, a later owner's defect reported alongside it is simply
rediscovered by the fresh evaluation. That is intended, not a loss, so report
each defect against its own owner and let the routing follow.

Where ownership is genuinely ambiguous, name the earliest owner whose
correction is actually necessary. That ordering is not a licence to round
upward: a defect the brief can repair out of evidence it already holds is
`brief` however grave it is, and `research` is for the cases where the evidence
is not there to repair it from. There is no fourth value; the engine rejects
anything else. Advisory findings do not need the field.

## Result

Return an evaluator result:
- `PASS` if all criteria are met with no blocking findings.
- `CHANGES_REQUIRED` with blocking findings if any criterion fails.
- `BLOCKED` if a finding cannot be resolved by revision.

Finding IDs must use the `CON-` prefix and be stable across iterations.
