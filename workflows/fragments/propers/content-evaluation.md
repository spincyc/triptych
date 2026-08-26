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
6. **Material disagreement**: Where the sources disagree, is the
   disagreement present in the prose and attributed to the sources that hold
   it? Is uncertainty carried where it bears on a claim, and currentness
   where it bears? Judge what the text contains. Never judge whether the
   guide announces that it preserved anything: a sentence saying a difference
   was retained rather than silently harmonized is not evidence of compliance,
   it is a criterion 12 defect, and asking for it is how a criterion produces
   the fault it meant to prevent.
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
11. **Interpretive voice**: Does the guide speak from within the Catholic
    tradition — Scripture, liturgy, doctrine, patristic reception, typology,
    and saintly interpretation presented in their own theological grammar and
    attributed to the witnesses who taught them? Or has secular skepticism
    become the narrator's default stance: inherited interpretation held at
    arm's length as an object viewed from outside rather than inhabited and
    explained, typology reflexively distanced from, modern criticism treated
    as the authority that validates or invalidates a theological reading,
    "later Christians believed" standing in for straightforward attribution
    where no historical distinction requires it? Accurate modern dating, a
    genuine authorship dispute, factual source criticism, historically
    documented disagreement, and the secular afterlives of `The Propers:
    Notable and Quotable` in their own section are never findings here: the
    profile requires them, and a finding that would delete one is wrong.
12. **Declarative discipline**: Does the prose state its findings, or does it
    repeatedly tell the reader how the editors reasoned, what principles
    guided inclusion, why caution was necessary, what methodology governs the
    section, or why the interpretation is being presented at all, instead of
    giving the conclusion? A few necessary claim-local qualifications are not
    a defect; the defect is a recurring rhetorical habit. `Appendix: Scope and
    Qualifications`, `References`, and the exploratory notice and `Strongest
    limit` field of `The Propers: Interpretive Possibilities` are
    qualification by design and out of scope for this criterion, which
    reaches only their register leaking into the substantive body.

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

A criterion 11 or 12 finding is `authoring`. Voice is not an evidence
defect: the material was researched, the prose is what mishandled it, and
rewriting the prose is the whole repair. Excessive methodological narration,
editorial self-justification, secular skeptical framing, and unnecessary
distancing from patristic interpretation all route that way. The single
exception is a passage for which the evidence supplies no Catholic reception
at all — there is then nothing for the guide to speak from, the distance
belongs to the evidence rather than to the author, and the finding is
`research`.

Where ownership is genuinely ambiguous, name the earliest authoritative
owner whose correction is necessary — that is, prefer `research`. That
tie-breaker does not reach criteria 11 and 12, whose owner the paragraph
above already fixes. There is no third value; the engine rejects anything
else. Advisory findings do not need the field.

## Result

Return an evaluator result:
- `PASS` if all criteria are met with no blocking findings.
- `CHANGES_REQUIRED` with blocking findings if any criterion fails.
- `BLOCKED` if a finding cannot be resolved by revision.

Finding IDs must use the `CON-` prefix and be stable across iterations.
