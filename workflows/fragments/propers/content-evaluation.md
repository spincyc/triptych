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
"repair_target": "research" | "authoring"
```

- `research` — the defect is in the research evidence or in
  `research/scope.md`: an unsupported or missing research premise, missing
  reception coverage in the brief, a weak evidence foundation.
- `authoring` — the brief is adequate, but the canonical proper's prose,
  structure, or use of citations is defective: prose that ignores an
  adequate brief, bad organization of the leaf, a citation placement or use
  problem where the source evidence is already adequate.

`tpt` reads this field and routes the repair itself. If any blocking finding
from any lane is `research`, the run re-enters the `research` stage, then
`research-synthesis`, then `author-proper`, then a fresh content evaluation.
Otherwise it goes to `content-revision`. You do not choose the route and the
controller does not choose the route: the field decides it.

Because research is corrected first and the whole downstream is regenerated,
an authoring defect reported alongside a research one is simply rediscovered
by the fresh evaluation. That is intended, not a loss, so report each defect
against its own owner and let the routing follow.

Where ownership is genuinely ambiguous, name the earliest authoritative
owner whose correction is necessary — that is, prefer `research`. There is
no third value; the engine rejects anything else. Advisory findings do not
need the field.

## Result

Return an evaluator result:
- `PASS` if all criteria are met with no blocking findings.
- `CHANGES_REQUIRED` with blocking findings if any criterion fails.
- `BLOCKED` if a finding cannot be resolved by revision.

Finding IDs must use the `CON-` prefix and be stable across iterations.
