# Content / Evidence Evaluation

## Your task

You are a fresh evaluator. Evaluate the content and evidence quality of the
proper leaf — every reader-facing document it builds, which the next section
tells you how to find. Do not rediscover what mechanical gates will check
later (build success, PDF existence, undefined references). Focus on
scholarly content.

## What the leaf builds

A leaf is one source tree, and it may build more than one reader-facing
document out of it. Establish which before you read anything, because "the
proper leaf" names that source tree and not a single document.

List the leaf's top-level `.tex` files. `main.tex` builds the canonical
guide. A `synthesis.tex` beside it builds a second published document, and
what that document contains is read out of the files rather than inferred
from the name:

- Where `synthesis.tex` is a two-line stub that defines
  `\TriptychSynthesisEdition` and inputs `main.tex`, `main.tex`'s own
  `\ifdefined\TriptychSynthesisEdition` branches decide what each edition
  carries. A branch may swap one `\input` for another, or fence off prose
  written inline.
- Where `synthesis.tex` is a document in its own right, its `\input` list
  decides, and it may share some section files with `main.tex` and not
  others.

Follow the inputs both ways and write down what each document puts in front
of a reader. Prose that reaches only one of them is parallel prose: the same
claim is made twice, in two places, and a lane that read only the canonical
build has not read the document. Read both editions.

Then name in every finding the file the defect is in, and the line or the
sentence within it, never only the section it belongs to.
`sections/30-commentary.tex` and
`sections/synthesis/20-integrated-commentary.tex` are two files that both
answer to "the detailed commentary", and a finding naming only "the detailed
commentary" leaves the reviser to guess which to open — where a claim is
stated in both, guessing repairs one edition and publishes the other.

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
    a defect; the defect is a recurring rhetorical habit, and it counts the
    same whether it is written as a sentence, a run-in label, a standing
    per-entry field, or a table column. Every reader-facing section is in
    scope: the page-1 four senses, `Scriptural Date and Location`, `The
    Propers: Themes and Movement`, `The Propers: Detailed Commentary`, the
    integrated commentary, the source-grounded synthesis, `The Propers:
    Notable and Quotable`, and the proposals of `The Propers: Interpretive
    Possibilities`. Out of scope, as qualification by design, are `Appendix:
    Scope and Qualifications`, `References`, and — within `The Propers:
    Interpretive Possibilities` — the exploratory notice, the novelty
    classification, and the controlling-limit field the profile mandates for
    each proposal, however that field is labelled. Two sections are in scope
    for their register and not for their required content. Page 2 must carry
    the traditional attribution, the modern critical horizon, the
    uncertainty, and the claim-local sources, and none of those is ever a
    finding; what is a finding is a dossier that turns to narrating the
    sheet's own conduct, as `this sheet reports it unresolved` does where the
    fact and the witnesses who differ would say it. Each gallery entry must
    carry its phrase, later user or work, exact locus, and turn in meaning,
    and none of those is ever a finding; what is a finding is the
    `Notable-and-quotable audit` printed for the reader as a standing
    `Control` or `Rights and limit` block under every entry, where the
    profile keeps that material in `research/scope.md`.

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

The route decides where the run goes next. It no longer decides who hears: a
finding whose owner did not win the route is carried to that owner in the
packet of whichever stage that owns it runs next, under `CARRIED_FINDINGS`. So
report each defect against its own owner and let the routing follow — naming
the true owner is now the only way the true owner is told.

This used to be false, and the difference is the reason to be exact. When only
the winning route's findings travelled, a single `brief` defect sent the run to
`research-synthesis`, the seven `authoring` findings raised in the same
evaluation reached nobody, and the author re-authored from an empty packet. The
next evaluation spent five lanes rediscovering what the run already knew.

A criterion 11 or 12 finding is `authoring`. Voice is not an evidence
defect: the material was researched, the prose is what mishandled it, and
rewriting the prose is the whole repair. Excessive methodological narration,
editorial self-justification, secular skeptical framing, and unnecessary
distancing from patristic interpretation all route that way. The single
exception is a passage for which the evidence supplies no Catholic reception
at all — there is then nothing for the guide to speak from, the distance
belongs to the evidence rather than to the author, and the finding is
`research`.

`brief` is not a third answer for those two criteria. The three questions
above separate the owners by what the repair needs, and a voice defect needs a
sentence of the leaf rewritten whatever seeded it — including a brief whose
own register the author pasted, which `research-synthesis` is separately told
not to write. A reception the lanes swept and the brief never carried forward
is a real `brief` defect, but it is a criterion 3 finding rather than a
criterion 11 one; report it there and the ordinary discriminator routes it.

Where ownership is genuinely ambiguous, name the earliest owner whose
correction is actually necessary. That ordering is not a licence to round
upward: a defect the brief can repair out of evidence it already holds is
`brief` however grave it is, and `research` is for the cases where the evidence
is not there to repair it from. That tie-breaker does not reach criteria 11 and
12, whose owner the paragraphs above already fix. There is no fourth value; the
engine rejects anything else. Advisory findings do not need the field.

## When no stage owns the repair

Some real defects are in neither the research, the brief, nor the leaf. A rule
in `guidance/liturgy/roman-1962-propers.md` can contradict another rule, or the
profile's own checklist; a source record can be wrong; a check in this pipeline
can be. No stage of this workflow may write any of those files, so no
`repair_target` is true of them, and both of the answers left were wrong.
Blocking would end a run whose document is correct. Advisory is where such a
defect actually went, and it was restated in every iteration of a real run and
acted on in none, because nothing outlived the run to act on it.

Use the third severity:

```json
"severity": "escalation",
"escalated_to": "guidance/liturgy/roman-1962-propers.md, the rules you name"
```

Name the file and the lines, and state the contradiction. The defect this
severity was added for had exactly that shape: the profile stated its
macro-order twice and incompatibly, and `profile-conformance` could only file
it advisory. The reader-order rewrite has since settled that one — sequence is
stated once, and every passage that needs it links there — which is what an
escalation reaching the maintainer is for.

An escalation carries **no** `repair_target` — having no owner in this run is
what makes it one, and the engine refuses a finding that claims both. It does
not block the run, does not spend the iteration budget, and does not stop
acceptance. It is written into the run's escalation ledger under its finding
id, restated into the same slot if you raise it again, and reported in the
terminal message and in `tpt proper status`, so it survives the run and reaches
the maintainer.

An escalation does not change your lane's disposition. Your criteria are met —
the leaf conforms as well as anything could — so the lane returns `PASS` and
files the escalation alongside. An evaluation carrying nothing but escalations
is a `PASS` and the run continues to `build-artifacts`, which is the point: the
document is finished and the defect is somewhere else. Returning
`CHANGES_REQUIRED` with only an escalation names no owner and the engine
refuses it.

The test is ownership, not gravity. Escalation is for a defect in an artifact
**no stage of this workflow may write**: repository guidance, `src/sources/`,
`tools/`, `workflows/`. If the leaf is wrong, or the brief is, or the research
is, one of the three repair targets is true and you must use it. Do not reach
for an escalation to avoid naming an owner, and say in `required_result` what
the maintainer is being asked to decide.

## Result

Return an evaluator result:
- `PASS` if all criteria are met with no blocking findings.
- `CHANGES_REQUIRED` with blocking findings if any criterion fails.
- `BLOCKED` if a finding cannot be resolved by revision.

Finding IDs must use the `CON-` prefix and be stable across iterations. This
is now load-bearing and not only tidy. The iteration budget charges a repeat:
an evaluation that raises a blocking id this stage already had standing has not
moved, and the run is that much closer to blocking. An evaluation that raises
different ids has found different work and costs the run nothing but its place
against the absolute ceiling. So reuse an id for the same unrepaired defect,
never for a different one, and never mint a new id for a defect you are
restating.
