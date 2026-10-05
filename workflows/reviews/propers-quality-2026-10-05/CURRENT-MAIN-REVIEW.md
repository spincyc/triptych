# Current-main supplement to the comparative quality review

Read-only review, 5 October 2026. The controlling snapshot for this supplement is
`b373dd5db96ea67b1975b27de411cfd6cf2e1ee6`, the fetched `origin/main`, read with
`git show` while the coordinator rebased. The original
`comparative-quality-report.txt` examined local
`a53e262d00d2658ac079801b07b26deeffb05a6d`, which proved to be 112 commits stale.
Its evidence remains a historical record; this supplement controls the current
verdict and explicitly corrects the findings changed by upstream work.

The current finished Nineteenth Sunday pair supports the main editorial
diagnosis: GPT chooses a narrower range of questions and develops a more uniform
moral argument; Claude preserves more distinct interpretations and makes their
differences drive the study and homily. This is a comparison of these finished
artifacts, not proof of a model regression, hidden effort setting, or general
provider ranking. GPT59 contains substantial reasoning that the next packet
should retain. One formerly reported workflow contradiction has already been
settled upstream and must not be presented as a current defect.

## Corpus, provenance and what changed

Abbreviations below resolve to these exact repository paths; line numbers refer
to the pinned current-main snapshot:

| Prefix | Repository path |
| --- | --- |
| G59 | `src/gpt/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost` |
| C59 | `src/claude/liturgy/roman-rite/1962/propers/temporal/59-nineteenth-after-pentecost` |
| C57 | `src/claude/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost` |
| G57 | `src/gpt/liturgy/roman-rite/1962/propers/temporal/57-seventeenth-after-pentecost` |

There is now a matched pair for the Nineteenth Sunday, 4 October 2026, in
addition to the Seventeenth Sunday, 20 September. The earlier statement that
Claude59 was absent describes only the stale checkout. The Eighteenth Sunday,
27 September, remains contextual evidence rather than a matched GPT/Claude pair.

C59 `generation-metadata.tex:3–5` identifies `claude-opus-5-5[1m]` for the three
authoring stages. It explicitly says actual reasoning effort was unexposed:
the workflow declared high, but the harness inherited the driver effort instead
of enforcing each stage's declaration. Do not describe its actual effort as
verified high. Lines 6–7 record substantive Claude postacceptance corrections;
line 8 records GPT-6 chronology recovery on 1 October. G59 metadata lines 3–9
identify GPT-6, author effort high and review effort xhigh, with exact model
variant unexposed; line 10 records its later chronology recovery. The older
mixed authorship of the Seventeenth Sunday still prevents calling all recent
Claude prose an untouched Opus 5.5 sample.

The G59 diff since the original snapshot changes twelve files: chronology,
source/bibliographic records, date dossiers, metadata and receipts. Its main
interpretive sections, developed concise commentary and spoken homily are
unchanged. Thus its positive and negative prose evidence survives exactly.
G57's main interpretive and spoken bodies are also unchanged. C57 received
real corrections: for example, its Christological discussion now identifies
Chrysostom's use of Mark's scribe, and the homily removes an overcompressed
version of that attribution. The central discovery from David's son to David's
Lord remains. Older C57 line references should therefore be treated as
snapshot-specific, not silently reused as current locators.

This supplement read both current 59 homilies, developed concise arguments,
the Claude whole-formulary readings and comparison, GPT's corresponding
commentary/comparison, and relevant research and revision records. It does not
claim a new exhaustive patristic source verification or PDF visual acceptance.

## Ranked current findings

### 1. High: question selection explains the most important difference

G59 gives the first part of Matthew 22 an accurate narrative account in
`sections/20-commentary.tex:180–196`, then principally asks what fruitful
membership requires. Its two readings concern charity and renewed action;
`sections/50-comparison.tex:3–18` distinguishes the presumption of membership
from the gap between general goodness and a neighbour's particular need.
These are legitimate complementary questions. They leave the repeated
invitations, burned city and identity of the callers and called relatively thin.

C59 asks a genuinely different historical and theological question: who called,
whom he called, and what happened to the call when refused. Its concise
`sections/concise/10-commentary.tex:11–46` follows Chrysostom from the vineyard
parable to Acts 13:46, Irenaeus from the two dispensations to the same God, and
Hilary and Jerome through their different identifications. Lines 48–91
distinguish Augustine's highways as Gentile teachings, Gregory's as failed
worldly undertakings, and the city as historical Jerusalem or the persecutors
in eternal fire. These differences alter interpretation; they are not added
names decorating the same conclusion. The comparison
`sections/50-comparison.tex:21–46,51–74` states the distinct questions, textual
weight and strongest difficulty of each reading.

The narrower evidence selection is documented. G59 `research/scope.md:132–171`
develops Augustine and Gregory on the Gospel and Chrysostom on the Epistle;
`:263–268` accurately summarizes its bounded corpus. It does not record the
direct Chrysostom Matthew 69, Hilary, Irenaeus and Jerome Gospel readings that
carry C59's historical lane. This supports an upstream selection explanation,
not a claim of exhaustive searching or deliberate avoidance. C59's
`research/interpretations.md:14–32` also shows review-driven expansion, including
a correction to the false negative that Augustine did not raise the highways
question. Its finished richness is partly the result of research and revision.

**Action:** before settling the readings, identify the text's difficult or
apparently disconnected units and what substantial question each poses. Review
what the chosen interpretations leave unexplained. Broaden research when a
material question remains thin; do not require a third lane or extra names by
quota. This is the strongest actionable explanation of the perceived loss.

### 2. High: Claude59 makes the listener discover more; GPT59 explains practical consequences especially well

C59 `sections/homily/10-homily.tex:19–29` places the listener beside the silent
guest already inside. Lines 48–62 eliminate baptism, faith and altar attendance
before arriving at charity as the Bridegroom's own dress. Lines 85–106 move
from bound hands, to works of mercy, to Christ's hands on the Cross and the
altar. The objection at 110–124—how could roadside guests possess the
garment?—makes grace the answer to a difficulty the speech has actually raised.
The two wishes at 136–145 and return to “Friend” at 157–167 change the opening
question into an examination and a hope. The argument advances through images
and objections rather than merely accumulating applications.

G59 `sections/homily/10-body.tex:1–30` is itself text-specific and coherent:
the prepared feast, the insiders' judgment, charity, the Bridegroom. Its
`:37–55` lucidly develops Chrysostom's eye/foot argument and anger fed overnight;
its practical qualification that reconciliation need not deny the injury is
pastorally valuable. The later sequence at 78–125, however, follows the familiar
pattern of demanding charity, enabling grace, Eucharistic healing and one
concrete act. This resembles G57's arc more than C59's unfolding discovery.

That is an editorial preference with textual grounds, not a failure verdict
for GPT's sermon. C59 names five patristic voices and quotes repeatedly; some
listeners may find GPT's fewer voices and plainer exposition easier. C59 is
1,453 spoken words against G59's 1,301, too small a difference to explain the
quality distinction by length alone. Do not turn the stronger Claude craft into
a mandatory silence hook, list of Fathers, or quota of rhetorical turns.

**Action:** have the homily reviewer identify the opening question/image, the
interpretive turn that changes the listener's understanding, and the response
that follows. Preserve GPT's concrete psychological explanation and careful
pastoral qualifications while demanding movement specific to the Sunday.

### 3. Medium: genuine disagreement creates useful density; GPT59 already demonstrates the remedy

C59's concise commentary develops why Gregory places Matthew's feast in the
present Church: a guest can still be expelled, unlike the final banquet
(`sections/concise/10-commentary.tex:107–140`). It then preserves Hilary's and
Schuster's future banquet at 142–158 instead of crediting them with the same
claim. At 314–360 it distinguishes Augustine's evening sacrifice of the
Passion from Hilary's works of mercy in the world's last age. The consequences
of those differences carry the comparison.

GPT59 is important contrary evidence. Its concise `10-commentary.tex:6–34`
explains Augustine's elimination of gifts shared by good and bad and
Chrysostom's account of renewal; `:66–75` explicitly contrasts Augustine's
reasoning from the recipient with Gregory's reasoning from the Bridegroom.
This is strong theological exposition, not merely moral advice or summary.
Its main commentary also preserves the Augustine/Bellarmine disagreement
over the Introit psalm's voice (`20-commentary.tex:34–42`). The initial report's
compression/repetition criticism applies especially to G57; it should not be
promoted into a universal characterization of GPT59.

**Action:** preserve premise, interpretive move and consequence in condensation.
Remove repeated applications only when they add no new conclusion. An exact
disagreement or qualification earns space; extra bibliography alone does not.

## Corrections to the original workflow and chronology findings

**Homily coverage: retract the claim of a current contradiction and the proposed
subset repair as a necessary fix.** Upstream commit `6f3a3567c99e47dacd7370775451432b66389f3f`
explicitly settled the meaning of the homily manifest.
`guidance/liturgy/propers-three-documents.md:511–518` now says all
`element_keys` declare the research informing the speech, not what the speech
recites. The checker did not change; the contract clarified its intent.
The old pc-s53 production record still proves historical author confusion and
pressure toward inventory, but it does not prove a current contradictory
contract or causation of either 59 homily. Preserve the settlement unless there
is a separate, explicit decision to change the schema's semantics. A useful
bounded improvement is to repeat this distinction where the author receives
the manifest instruction; do not force extra minor-proper sentences into speech.

The same upstream commit strengthens clause-level attribution at profile
`:169–179`. C59's revisions show why: an opening that assigns a whole thesis to
several Fathers can overcredit individual clauses. C59
`research/interpretations.md:34–54` and `generation-metadata.tex:6–7` record
corrections to Schuster's banquet, Honorius's mismatching Gospel, the
Postcommunion's actual wording, source loci and condensed attribution. This is
contrary evidence to a simple “Claude succeeded effortlessly” narrative.

Other controls are already upstream: `workflows/fragments/proper-study/contract.md:7–11`
excludes old cultural-gallery and exploratory-proposal quotas; `research.md:38–49`
describes automatic sealing of chronology computation inputs, cited source
ancestry and payload, rather than relying on a manually exhaustive declaration.
The original historical source-containment defect was already repaired during
Claude58. These are not new fixes required for the upcoming run.

**Chronology: narrow the earlier finding to what remains thin.** Current G59
`sections/70-date-location.tex:5–9` supplies a Davidic regnal frame for Psalms
137 and 140, explicitly as traditional attribution rather than composition.
Its Gospel event paragraph at `:26` now uses Maas's Tuesday after the entry
into Jerusalem and explicitly labels the year as derived. Those repairs
invalidate any current claim that every Psalm cell contains only a broad
Psalter boundary or that this Gospel event remains numerically unresolved.
The remaining historical-orientation limitation is visible at `:14–19`:
Psalm 77's deliverances and failures and Psalm 104's covenant, Joseph, Exodus
and land are summarized without separately locating those remembered events.
That is a bounded opportunity for sourced context, not evidence that the
printed composition boundary is false. Continue to distinguish an attributed
frame, narrated or retrospective event, composition and reception; a contextual
Exodus narrative must not falsely date every appointed opening verse.

## Production implication

Use the corrected current contract and shared chronology. The editorial work
needed is chiefly better discrimination at existing research, study and homily
reviews: ask which actual textual problem a reading solves, make its sources'
reasoning visible, retain consequential disagreements, and ensure the homily
takes its listener through a discovery. Existing prompts already require
depth and source reasoning, so the diagnosis is not that they command thinness
or that a hidden token cap has been established. The matched current 59 pair
strengthens the finding of narrower selection and a more repetitive rhetorical
range, while decisively preserving GPT59's substantial counterexamples.

No tracked file was edited, and no claim is made about unrecorded model
settings or author intentions. This supplement supersedes the original
report where explicitly stated; the old evidence is retained for audit.
