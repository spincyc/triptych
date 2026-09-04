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
   leads until checked? This criterion reaches the appointed Latin as the
   leaf prints it. `propers/verified.md` records what the typical edition
   actually prints, accent by accent, and the leaf must print that: an acute
   the edition does not carry, a spelling, or a word division the record does
   not hold is a criterion 2 defect wherever in the leaf it stands. That is
   this criterion and no other — transcription fidelity to the identified
   edition is what "verified from the edition itself" means, and a lane that
   files it under citations or under provenance files it where nobody owns
   it.
3. **Reception sweep**: Was a broad and deep patristic/saintly reception
   sweep conducted for each appointed passage? Are direct witnesses retained
   where found?
4. **Cross-proper synthesis**: Is the synthesis a redistilled cross-proper
   argument (not an abridged procession)? Does each unit draw from multiple
   elements and witnesses?
5. **Exploratory proposals**: Are proposals labeled as exploratory? Does each
   join at least 2 elements? And does each carry every field the profile
   mandates for a proposal — the connecting mechanism, the theological,
   intellectual, spiritual or pastoral fruit, what the ordinary
   element-by-element reading misses, and the strongest material limit,
   alternative, or disconfirming condition — each under a heading that states
   the field the profile asks for? A proposal that prints some other field in
   place of one of these has dropped the field, however good the substitute
   is on its own. The mandated fields of a proposal are criterion 5 and not
   criterion 9: reader order and page assignment are properties of the
   document, and the fields inside a proposal are properties of the proposal.
6. **Material disagreement**: Where the sources disagree, is the
   disagreement present in the prose and attributed to the sources that hold
   it? Is uncertainty carried where it bears on a claim, and currentness
   where it bears? Judge what the text contains. Never judge whether the
   guide announces that it preserved anything: a sentence saying a difference
   was retained rather than silently harmonized is not evidence of compliance,
   it is a criterion 12 defect, and asking for it is how a criterion produces
   the fault it meant to prevent.
7. **Citations and stated counts**: Are only sources actually used cited? No
   invented searches, verifications, quotations, attributions, doctrines,
   laws, or historical facts? A number the prose states about its own
   material is such a fact, and it is checked by counting what follows it:
   `Five independent witnesses` heading four, `Six comparatives of degree in
   four Latin constructions` enumerating seven, a total that does not add up
   to the rows above it, a `three` that introduces two. Every stated count in
   reader-facing prose is this criterion's, in every section and in both
   editions, whatever the material being counted is — witnesses, textual
   features, manuscripts, elements, proposals. It is not divided by subject
   matter: the arithmetic belongs here even when the things counted are
   evidence, or Latin constructions, or the appointed elements themselves.
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
    per-entry field, or a table column. **Every reader-facing section is in
    scope** — every section either edition puts in front of a reader, with no
    exception but the ones named next. The out-of-scope list below is the
    entire boundary; nothing else narrows it. Out of scope, as qualification
    by design, are `Appendix: Scope and Qualifications`, `References`, and —
    within `The Propers: Interpretive Possibilities` — the exploratory
    notice, the novelty classification, and the controlling-limit field the
    profile mandates for each proposal, however that field is labelled.
    Where to look, which is a reading checklist and not the boundary: the
    page-1 four senses, `Scriptural Date and Location`, `The Propers: Themes
    and Movement`, the complete appointed text, `The Propers: Detailed
    Commentary`, the integrated commentary, the source-grounded synthesis,
    `The Propers: Notable and Quotable`, and the proposals of `The Propers:
    Interpretive Possibilities`. A reader-facing section this checklist does
    not happen to name is in scope all the same, and the checklist being
    short of one is never a reason to leave a section unread: read what the
    leaf actually builds. Three sections are in scope for their register and
    not for their required content. Page 2 must carry the traditional
    attribution, the modern critical horizon, the
    uncertainty, and the claim-local sources, and none of those is ever a
    finding; what is a finding is a dossier that turns to narrating the
    sheet's own conduct, as `this sheet reports it unresolved` does where the
    fact and the witnesses who differ would say it. Each gallery entry must
    carry its phrase, later user or work, exact locus, and turn in meaning,
    and none of those is ever a finding; what is a finding is the
    `Notable-and-quotable audit` printed for the reader as a standing
    `Control` or `Rights and limit` block under every entry, where the
    profile keeps that material in `research/scope.md`. The complete
    appointed text is the third. What the profile requires of it is narrow —
    where no public-domain English exists for an element, say so, give the
    Latin incipit, describe what the prayer asks, and supply no rendering of
    the project's own — and a leaf that goes further and states what the
    registered English leaves of the Latin unanswered is stating a fact about
    the two texts, which is never a finding. What is a finding is the same
    block turning from the two texts to the guide's handling of them — `so
    they are printed whole with the sung portion marked`, `it stands
    bracketed above in the missal's own Latin and untranslated`, `the
    doxology cue is not translated here` — where saying what the Latin has
    and the English has not would do the work. That section is named here
    because an earlier checklist left it out, and a lane had to decide for
    itself both that it was in scope and which half of an English-gap block
    the profile asks for. It is in scope, on the same terms as the other
    two.

## Lane scope

This stage is a fan-out stage: the criteria above are partitioned across
the workflow's evaluation lanes, and the lane fragment that follows names
exactly which of them you own. Report findings for your own criteria only.
Another lane owns each of the others, and tpt joins every lane's findings
itself.

## When you see something real and your criteria do not reach it

Record it under `observations`, whose shape and limits the result-format
fragment above states. It exists because the alternative was that such a
sighting died in a lane's hand-back prose: four real defects, falling into
three classes, were once located by max-effort lanes and reported by none,
each sitting between adjacent lanes' criteria, and the only route from a lane
into the run record was the driver writing a finding of its own, which the
fan-out policy forbids and which is what made an earlier run unreplayable.

Two things it is not, on this stage in particular.

- **It is not a way around the partition.** Where this fragment or your lane
  fragment names a class as another lane's, leave it to that lane: do not
  report it and do not observe it either. Duplicating an owned class into
  observations is how a partition rots, and the owner has been told in terms
  that the class is theirs.
- **It is not the place for a class that keeps recurring.** The same kind of
  thing arriving run after run means a lane is missing a criterion, and the
  repair is to the fragments and not to the lane's diligence. The three
  classes those four defects fell into — the mandated proposal fields, a
  stated count its own list contradicts, and the appointed Latin's orthography
  against `propers/verified.md` — now have owners in criteria 5, 7 and 2
  respectively. Say so plainly in the `note` if you think you have found a
  fourth class.

## Repair ownership

Every **blocking** finding must name who has to repair it:

```json
"repair_target": "research" | "brief" | "authoring"
```

**Your packet's `REPAIR_TARGETS` header names the values this run admits, and
it is the authority — not the three above.** A pipeline that begins after
research owns no research and no brief, so it admits `authoring` alone, and a
finding naming an owner the run does not have is refused. On a fan-out stage
that refusal costs every lane's result, not only yours. Where the header names
one value, every blocking finding you raise carries that value; where the
defect genuinely needs an owner the run does not have, it is not a blocking
finding of yours at all but an escalation, which carries no `repair_target` —
see *When no stage owns the repair* below.

Where the header names all three, ask the three questions in this order and
stop at the first yes.

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

Before naming `authoring`, inspect the finding's `required_result` against the
read-only `research/scope.md` and verify that every fact and citation detail it
requires is explicitly present there. Never say that the brief holds a title,
creator or institution, edition or date, stable URL, access date, or locus
without locating that value in the brief. A prior lane result or run artifact
does not make evidence available to the author: the immutable brief is its
whole research input. If a necessary online citation value is missing from the
brief, the evidence-retrieval defect is `research`; if the correct value is
present elsewhere in the brief but its audit states it wrongly, the defect is
`brief`.

One blocking finding names one defect and one repair owner. When a passage of
the leaf needs revision but the revision also depends on evidence the brief
does not contain, split the compound report into separate findings: the
missing-evidence finding goes to `research` or `brief` under the rules above,
and the leaf-only finding goes to `authoring`. Do not hide two owners behind a
single `required_result`; only the owner named on that finding will receive it.

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
id, restated into the same slot if you raise it again, and reported in
`tpt proper status` and in the terminal message of an accepted or blocked run.

Be exact about how far that carries. The ledger is part of the run state
under `build/`, which is ignored, which `make clean` removes and `wt tidy`
sweeps, and which nothing preserves between productions. A blocking finding
and an observation reach a tracked record beside the document; an escalation
does not, and the only part of it that reliably leaves is the terminal
message a person reads. Write it so that message is enough on its own: name
the file and the lines, state the contradiction, and say in `required_result`
what the maintainer is being asked to decide.

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

An escalation is not an observation, and the two answer different questions.
An escalation is a finding of yours, under your own criteria, about a defect
this run cannot repair because the file belongs to nobody in it; it carries a
severity and a `required_result` and it reaches the maintainer. An
observation is about your criteria and not about the file: you saw something
real in a document this run can perfectly well repair, and no criterion you
own reaches it. Ask which of the two is true — is the defect outside the
run's reach, or outside your lane's — and the answer picks the shape.

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
