# Register remediation, 21 October 2026

## Request

The maintainer reported that produced documents still fall into "unearned
profundity, empty significance, jargon, ham-fisted hokiness, little subtlety",
naming the Claude 1962 Christ the King documents (run `7397c12187517ff2`,
`proper-study` v12, published in `c71314375`). The request: find the cause,
remediate it, execute the remediation on those documents to verify it works,
sanity-check, cold-review, and ask where a decision was the maintainer's.

Decisions the maintainer took on 21 October 2026, when asked:

- revise the three published documents in place, and separately test
  generation from scratch under the new guidance with blind comparison;
- reframe the homily's list of rhetorical devices rather than keep it;
- bump `proper-study` to version 14 so that review fragments carry a register
  criterion;
- call a study's interpretations "interpretations" in reader prose, since
  "the first reading" already names the Epistle.

## What the documents did

Two independent census lanes read all three documents. Approximate counts:

| Defect | Expansive study | Concise study | Homily |
| --- | ---: | ---: | ---: |
| Maxim or paradox closers | 22–25 | 8–10 | 10–12 |
| Asserted significance or coherence | ~20 | 9–11 | 4 |
| Antithesis against a position nobody holds | 22–25 | 7 | 6–9 |
| Production vocabulary (formulary, element, reading, witness) | ~70 tokens | ~45 tokens | 1–3 |
| Texts made agents of the study's inferences | 20–30 | 8–15 | 1–2 |
| Hokey devices (Monday tag, relatable lists, stock calls) | ~2 | 0–3 | 6–8 |
| Emphatic fragments, questions answered at once | — | 3 | ~14 |

Both lanes found the problem structural. Each of the study's three
interpretations ended in a roll call assigning all eleven texts a part ("Read
in this way, every element of the formulary takes a place in one movement";
"The Offertory is the reading's centre"). The concise study's themes pages
restated coherence to fill two fixed pages. Nearly every homily paragraph was
built to end on a maxim ("There is no Monday outside his kingdom"). The
patristic exposition between these seams was sound.

A comparison lane read the GPT Christ the King documents and earlier Claude
leaves (49, 57, 61, pc-s52):

- the maxim closers, emphatic fragments and the "on which the whole X turns"
  formula are Claude's own habit, present from the first Claude homily (57,
  18 September) at similar rates;
- the production vocabulary and the asserted coherence are as heavy in GPT's
  study prose, and GPT's homily closes on the same "This week, choose one
  place…" formula, which points at the shared guidance;
- the defect is not new: the July Claude 49 themes section has every marker.

## Causes, strongest first

1. **The coverage mandate.** `guidance/liturgy/propers-three-documents.md`
   required each interpretation to "state a unifying interpretation of the
   whole formulary" and "let every appointed element contribute"; study review
   checked "each engaging the entire appointed formulary"; run 60's reviewer
   blocked a study for omitting the Alleluia from such a roll call. The roll
   call is a coverage certificate written as prose.
2. **The homily recipe.** The profile listed devices — a question, contrast,
   measured repetition, a return to the opening image, a practicable response
   — and asked for a "decisive turn"; review required "concrete pastoral
   fruit". The author's audit for this homily lists the Monday device under
   those headings, and both providers converged on the same closing formula.
3. **The themes pages.** A thesis and a "movement" filling two fixed pages,
   recoverable by signpost scan, invite connecting sentences that assert
   coherence.
4. **The subject rule.** `editorial.md` made "a source, a text, a witness" the
   legitimate subject of a qualifying sentence, its example sentence was "The
   Introit establishes exile as the formulary's opening condition", and the
   house-voice repair is "change the grammatical subject". Together they
   taught the personified-text sentence.
5. **Vocabulary leakage.** Manifest and workflow terms ("formulary",
   "element", "witness", "carry", "the reading") reached reader prose.
6. **The register of the instructions** (weak). The shared packet text is
   epigrammatic; no output maxim could be traced to an input one.

No rule named the defect, no review criterion reached it, and no proper-study
packet pointed authors or reviewers at `editorial.md`. All five reviews of the
run raised no register finding; the homily review praised its "turn".

## Remediation

- `guidance/editorial.md`: new section "Say what the texts say, plainly" with
  tests a writer applies to each sentence, its counterweight "Plain is not
  flat", and the rule that an inference moved off a text must not be moved
  onto a Father. The example sentence and the subject rule now point at it.
- `guidance/liturgy/propers-three-documents.md`: coverage shown where the
  argument uses a text, no closing roll call; themes pages filled with textual
  detail and the Fathers' reasoning, oriented for the reader; the homily's
  device list replaced by plain teaching, one response said to the people in
  the second person, written for one hearing; acceptance now names the rule.
- `guidance/liturgy/roman-1962-propers.md`: the register rule governs the same
  reader-facing words; real synthesis is textual detail.
- `proper-study` version 14 (`workflows/OPERATOR.md`): the contract and the
  authoring fragments point at the rule; `review.md` makes register a reviewed
  criterion, blocking when a pattern recurs, never `accepted`, and asks a
  register repair's attributions to be checked; the study, synthesis and
  homily review fragments name their own forms.
- **No screen**, by decision. A lexical screen refuses fixed phrases and the
  writer routes around them, and the house-voice screen's own repair is one
  of the causes above. Register is judged in review.

## Verification

### Mechanical

- Workflow and house-voice test suites (36 files): failure sets identical to
  the baseline after the guidance change and after the final edits; six
  suites fail at the base for reasons outside this work.
- The three documents build at 33, 12 and 4 pages with no undefined
  references or overfull boxes; the concise study's page 1 holds the map and
  four senses, page 2 the dates, pages 3–4 the themes, both full, and the
  commentary begins on page 5.
- `check-proper-components` passes for all three editions. The content
  preflight's errors are identical to the baseline in every edition (the
  leaf's chronology record had already gone stale against the corpus);
  house-voice, structural-meta-labels and references-used pass.
- Every quotation, Latin phrase, work, locus and page reference of the
  original survives, except two deliberate cuts: the comparison's catalogue of
  which Father contributes to which interpretation (its works are cited
  elsewhere) and six quoted table-column labels in the date notes.
- Reader-prose counts, before and after: "formulary" 10 → 0, "witnesses"
  21 → 0, "element" 21 → 0 (labels only remain), "reading" 61 → 19 (a
  Father's reading of a verse, and the Mass's readings).
- The web edition is regenerated under the pinned Markdown 3.10.3;
  `check-web-editions-current`, `check-release-bindings` (one web edition and
  the catalogue re-recorded) and `check-document-catalogue` pass.

### Does review now catch it?

Fresh reviewers applied only the version-14 register criterion to the
original documents (results in `evidence/v14-reviews/`):

| Document | v12 review | v14 register review |
| --- | --- | --- |
| Expansive study | passed, no register finding | 7 blocking, 1 advisory |
| Concise study | passed, no register finding | 6 blocking, 2 advisory |
| Homily | passed, no register finding | 4 blocking, 4 advisory |
| Claude 1962 leaf 61 homily (not quoted by the guidance) | passed | 7 blocking, 1 advisory |

The guidance quotes Christ the King sentences as examples, so the first three
rows are not independent of them; the leaf-61 row is.

### Does authoring now avoid it?

Fresh authors wrote the homily and the themes pages from the frozen reviewed
study under the new guidance, without sight of the existing texts. Two blind
judges (one Opus, one Sonnet) compared each draft with the original, texts
stripped of markup and authoring comments, labels randomised (keys in
`evidence/blind-keys/`).

| Round | Guidance state | Result |
| --- | --- | --- |
| 1 | rule without counterweight | all four judges preferred the original: the drafts avoided the named traps but read as a catalogue of Fathers, Latin left to construe, no landing |
| 2 | "Plain is not flat" added | homily: original > round 2 > round 1 for both judges |
| 3 (homily) | one hearing, gloss only the unfamiliar, response from the argument, second person | both judges ranked round 3 first, above the original and the revision |
| 2 (themes) | as round 2 | both judges ranked round 2 first, above the original and the revision |

The final judges were told to weigh the maintainer's stated complaint first;
earlier rounds weighed both complaints equally. The first-round results were
the reason for the counterweight now in the rule.

### The revised documents

Each document was revised twice: once against its version-14 review, and
once against blind judges' lists of what the first revision lost (all three
first revisions over-corrected, cutting argument with ornament; findings in
`evidence/second-pass-findings/`). Final blind comparison against the
original:

| Document | Opus judge | Sonnet judge |
| --- | --- | --- |
| Expansive study (00, 20, 30, 50) | revision, high | revision, medium |
| Concise study (overview, themes, commentary) | revision, medium | original, medium |
| Themes pages alone (three-way) | round-2 draft > original > revision | round-2 draft > revision > original |
| Homily (three-way) | round-3 draft > revision > original | round-3 draft > original > revision |

After the final judging the coordinator made four sentence changes to the
homily and two to the study at sentences both judges named.

An independent fidelity review read every changed sentence against the
baseline and the research records. It found three blocking errors the
revision had introduced — an inference moved into Augustine's mouth, the
study's own "bounded by place" gloss presented as Aquinas's reasoning, and two
stale cross-references in the homily note — and twelve advisories. All were
corrected. A second cold reviewer confirmed the thirteen corrections, found
residues in four of them and three further instances (the concise study still
credited Augustine with the same identity; three places reduced Aquinas's two
ways of asking, by prayer and by passion, to one; one sentence could read the
fight against sin as Schuster's), and these were corrected as well. The
editorial rule now forbids moving an inference from a text onto a Father, and
the shared review fragment asks a register repair's attributions to be
checked.

Every page of the three final PDFs was inspected as a raster: no blocking
defect. The advisories concern the shared template (a running head naming the
section that begins on a page, an unnumbered last page), as before the
revision.

## Installing the from-scratch homily and themes pages

Asked afterwards, the maintainer chose to install the round-3 homily and the
round-2 themes pages, which every final judge had ranked first, after checks,
and to push the result to main.

- **Install.** Fresh lanes converted each draft into the leaf's conventions
  without rewriting it: the homily's body matched the draft word for word, the
  themes pages kept their page markers. Every quotation (22 in the homily, 50
  in the themes pages) is verbatim in the study as published. The concise
  commentary was trimmed in fifteen places where it repeated the new themes
  pages, and one quotation there that had never been verbatim was corrected.
- **Coordinator's changes.** The homily was cut from 1,631 to about 1,530
  spoken words, removing a sentence that blended Bellarmine's readings of two
  psalms and a second *Quas primas* point the judges found opaque, and
  correcting "at the beginning of Mass" (the Introit, not the Collect, begins
  it). The PDF subject now describes the new speech.
- **Fidelity.** An independent review of the installed texts found three
  blocking errors — the "bounded by place" reasoning again credited to
  Aquinas in the homily, the themes pages' opening thesis credited to "the
  Fathers" as a body, a wrong word count in the homily note — and advisories,
  most of them antecedents left dangling by the commentary's trims. All were
  corrected and the corrections re-checked by a second reviewer.
- **Checks.** 33, 12 and 4 pages; the concise opening holds, pages 3–4 full
  and the commentary from page 5. `check-proper-components` passes; the
  content preflight's errors equal the baseline's and house-voice,
  structural-meta-labels and references-used pass; the web edition,
  catalogue and release bindings are regenerated and exact.
- **Selection.** The concise study now quotes a different selection: 25
  quotations the revision carried are gone, most of them restatements moved
  out of the commentary, and every References entry is still used.

The judged drafts remain in `evidence/generated/`; the installed texts differ
from them by the changes above.

## What the judges can and cannot show

Every judge is a Claude model, and the defect is a Claude habit. Judges
rated the original's maxims only mildly and repeatedly called sentences the
census had flagged "the argumentative heart". Their preference for the
original's "life" is partly that taste; their concrete complaints about the
drafts (Latin left raw, authorities strung by name, an application from
nowhere, an orphaned "second place") were real and were acted on. The
maintainer is the judge of the register this record is about.

## Open

- Version 14 has not yet driven a full `proper-study` run; the authoring
  evidence comes from stage-level experiments outside the engine.
- The same defects stand in other published leaves: the leaf-61 homily
  review above, and the GPT Christ the King documents. On 21 October 2026 the
  maintainer decided to let the next real `proper-study` production under
  version 14 test the guidance and review end to end before any backfill of
  older documents.
