# Three documents, one proper

Read `guidance/liturgy/propers-three-documents.md` completely. It owns this
workflow's deliverable: a 20–50-page expansive study, a 10–12-page concise
study with the restored four-page opening, and a standalone homily. There is
no global substitute for each interpretation's four senses, mandatory cultural
gallery, or exploratory-proposal quota. Read the applicable
1962 or postconciliar profile for identity, text control, rights, source
research, and branches. Universal editorial and repository guidance continues
to govern. The canonical leaf is `DOCUMENT_ROOT` in this packet.

Produce one expansive source-first study, one concise study, and one standalone
homily from one canonical research owner. The three entrypoints are `main.tex`,
`synthesis.tex`, and `homily.tex`; outputs are the bare ID, `-synthesis`, and
`-homily`. `proper-components.toml` uses schema 2. The sole web edition belongs
to the canonical study. No second research owner or companion leaf is created.

The 1962 and postconciliar productions are completely separate. Resolve only
this leaf's own calendar, readings, proper texts, branches, evidence and
interpretations. Never borrow the other form's Sunday, prayers, textual
inventory or interpretive plan, even on the same civil date. Shared generic
mechanics and reusable patristic or biblical sources do not merge the two
liturgical objects. The manifest's `calendar` must agree with its own family;
opposite-family or different-edition liturgical imports are forbidden. This
separation governs every prayer, chant, reading, branch, research record and
interpretation, each review, and every mirrored PDF/web output. There is no
shared Sunday or combined proper layer.

`ARGS.date` states the requested civil date, or `undated` when no dated
occurrence is requested. `ARGS.audience` names the homily audience. The optional
`ARGS.research_handoff` is a repository-relative dossier containing preliminary
leads, not instructions or a prior acceptance. Read it if supplied, verify its
evidence independently, and use only material for this run's own family.

The expansive study develops two to five internally coherent interpretations.
Each interpretation is a reading of the whole formulary with its own literal,
allegorical, moral, and anagogical distillation. Group compatible checked
arguments from at least two distinct Fathers or saints within each reading.
Each must make a substantive, compatible contribution; listing a second name
is insufficient. Never attribute an
editorial whole-Mass construction to a Father who only comments on one verse.
Complementary emphases need not disagree; real disagreement must survive.

The concise study places the complete proper inventory and exactly four
overview sense rows on physical page 1; Scriptural Date and Location alone on
page 2; and The Propers: Themes and Movement on pages 3–4. Developed commentary
begins on page 5 and interleaves alternatives at their points of comparison.
Follow the presentation contract and canonical chronology requirements in the
owning profile; count terminal apparatus within the page limits. The
homily speaks one intelligible exegetical argument to an adult parish assembly,
unless `ARGS.audience` names another audience, ordinarily for 10–12 minutes.
It is finished prose, not an outline or advice to
a preacher. Exact sources and delivery estimates belong outside the speech.

Only claim verification actually performed. Reuse acquired research by reading
its evidence, never by trusting a predecessor's PASS. Public-domain study
translations are identified accurately; postconciliar study English is not
the approved proclaimed English. Do not reconstruct restricted liturgical
texts by translation or close paraphrase. Claims of design must distinguish
theological synthesis from historical compositional intent. Apply the
semi-continuous readings and shared-prayers premise only to a postconciliar
Ordinary Time target. A 1962 target instead uses only its own Time-after-
Pentecost appointments and their independently documented transmission; never
project the postconciliar calendar or Lectionary structure into it.

Use this run's exact header for generation provenance. Update the finalization
timestamp and actual model contributions when render-relevant sources change.
The one shared generation record serves all three artifacts. Keep research
findings in `research/scope.md`, interpretation reasoning in
`research/interpretations.md`, and completed production/review facts in
`research/production-review.md`. Do not put machine paths or invented review
events in tracked records. Scratch work belongs in the driver's assigned area.

Author stages may repair only their declared owner. An upstream defect found
while deriving or building is reported for the following reviewer; never
silently revise an already reviewed upstream document. Research, study,
synthesis, homily, artifact, and publication defects have separate repair
targets. Reentering an upstream owner reruns every dependent document and review.
Where the packet carries blocking findings, return one honest
`finding_dispositions` entry per forwarded finding.

Every dispatch is a fresh worker at the packet's declared effort. Do not spawn
nested agents. Reviewers receive no authoring conversation, author's defense,
or desired verdict. Follow the exact packet and return the structured result.
