# Research scope — Fourteenth Sunday after Pentecost (1962 Roman Rite)

Audit record for the proper at
`liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost`.

Written by the `research-synthesis` stage of workflow `proper v11`, run
`6b83fad5ae2ed53e`, iteration 0, integrating the joined findings of seven
research lanes (203 findings: 34 `scripture-context`, 74
`patristic-reception`, 27 `liturgical-history`, 23 `theological-synthesis`,
11 `source-citation-coverage`, 16 `cultural-afterlife`, 18
`precedent-search`). `CARRIED_FINDINGS` was empty on this iteration.

**Amended in place by the same stage at workflow `proper v11`, run
`e5b24f405bde9691`, iteration 0 (2026-08-31)**, which integrates a fresh
seven-lane join of 69 findings (25 `scripture-context`, 4
`patristic-reception`, 4 `liturgical-history`, 13 `theological-synthesis`,
8 `source-citation-coverage`, 4 `cultural-afterlife`, 11 `precedent-search`),
run against the leaf as re-authored at commit `7c2aaafce` from this brief.
`CARRIED_FINDINGS` was empty on that iteration also. **The amendment is an
amendment, not a replacement**: the 203 findings of the first integration
remain this brief's evidentiary base, the fresh lanes cite this file's
sections throughout as their evidence of record, and nothing below has been
rewritten except where the fresh join corrects it. The two joins share the id
space and are not continuous; fresh finding ids are cited as `[fresh:ID]`
and bare ids keep their first-join meaning.

**This brief replaces the file of the same name written by the `proper v10`
production, run `b68cca80edb75854`, entirely.** That file's finding ids belong
to a different run and are not continuous with the ids used here; where this
brief cites a prior-run id it does so because a lane of *this* run restated it,
and it says so. **A restatement inherits the evidence state of what it
restates** — a lane reporting that the prior sweep found X has not thereby
raised X, and this brief marks the difference at every locus where it matters.

**This stage is the sole writer of this file.** The research lanes were
forbidden to touch it; no later stage may add to it or amend it. Nothing after
this stage can repair a gap left here, so every position this brief takes is
stated rather than implied, including the positions that are negative. **The
lanes could see this file but could not change it, and several of them found
errors in it. Every such correction is settled at §0.3 and applied throughout;
none is left as a note.**

The text control for this formulary is `propers/verified.md`, not this file and
not the calendar registry. Where this brief reports a reading of the appointed
Latin it reports what the `source-audit` stage collated at 500 dpi against the
Church Music Association of America facsimile of the Vatican typical edition,
printed pp. 394–396, marginal nos. 1572–1581, the formulary bounded by
nos. 1571 and 1582.

Claim classes are those of `guidance/liturgy/roman-1962-propers.md`:
(1) textual observation, (2) documented historical orientation,
(3) documented reception, (4) source-grounded synthesis, (5) exploratory
proposal. Classes 1–4 may appear in source-grounded sections; class 5 appears
only in `The Propers: Interpretive Possibilities`.

Evidence states are those of `guidance/sources.md` — cataloged, acquired,
indexable, searched, inspected, verified — and they are cumulative **only where
the record establishes each one**. Possession is not reading; a search hit is
not inspection; **inspection of a transcription is not collation against a page
image.** No patristic witness in this brief is *verified* in the
source-library sense, and the brief says so at every locus rather than once.
Two cultural-afterlife entries **are** collated against page images this run
and are the only items anywhere in this brief that may carry the word
*verified* (§8, §11.2).

Lane finding ids are cited in brackets throughout. They are the authority for
everything here; where this brief and a lane finding differ, the lane finding
is what was established and this brief has erred.

---

## 0. What this brief settles

### 0.1 What this run changed, and where the weight of it fell

The `proper v10` production reached a complete, committed leaf: twenty-one
files, both PDFs building at 46 and 28 pages, all five `content-preflight`
checks passing, `check-proper-components` valid. **This run is therefore not a
first draft. It is a second, much larger evidence base laid against a finished
guide**, and the integration question is not "is there enough" but "what does
the new evidence change".

Four things changed materially, and they are the shape of this brief.

**(a) The reception sweep stopped being Latin-and-English and became
Latin-and-Greek.** The prior sweep read two Greek authors, neither in Greek.
This run read Theodoret of Cyrus on Pss. 83, 94 and 117 **in Greek** and
Chrysostom on Gal. 5:19–25 **in Greek**, from TLG transcriptions with real text
layers [PAT-300, PAT-310]. It also retrieved, in Latin and at first hand, five
works the prior sweep named as its largest gaps: Augustine's *Expositio ad
Galatas* — the prior brief's own "single most valuable repair" [PAT-100];
Jerome on Galatians [PAT-150]; Jerome and Hilary on Matthew [PAT-120, PAT-110];
Cassiodorus's *Expositio in Psalterium*, complete, commenting on **all four**
appointed psalms [PAT-200]; and Aquinas's *Super Matthaeum* [PAT-130]. **Six of
the ten appointed elements gained a witness they did not have.**

**(b) A negative the prior brief carried as bounded turned out to be an
artefact of a URL scheme.** The Cassiodorus absence rested on
documentacatholicaomnia.eu failing TLS certificate verification. The host still
fails TLS and still serves the identical bytes over plain HTTP with a 200
[PAT-403]. **The prior negative was avoidable, and correcting it yielded a
Latin psalm commentator on every chant of the formulary.** This is recorded at
the head of the brief because it is the clearest available demonstration that a
retrieval negative is a statement about a retrieval and not about the world.

**(c) The liturgical-history case both widened and was corrected against
itself.** One of the five sacramentary books behind the displacement is now
open at the locus [LIT-011]; the origin of the offset, which the prior brief
left as its principal unresolved lead, is closed from Wilson's own Introduction
[LIT-010]; the run of displaced Masses is sixteen sections and not eleven
[LIT-009]; and the Gregorian Hadrianum carries **all three** orations as one
Mass, so the prior brief bounded its own claim more tightly than the evidence
required [LIT-023].

**(d) Two cultural-afterlife entries were collated against page images.** For
the first time in this target's history, two gallery entries stand at
*verified* and the method for bringing any other newspaper entry to the same
state is recorded and cheap [CUL-008, CUL-011, CUL-015].

**What did *not* change, and the author must not expect it to.** The page-2
modern-critical-horizon position is unchanged: no NABRE artifact is registered
for Matthew or for Pss. 34, 84, 95, 118, and no lane retrieved a substitute, so
those cells remain bounded negatives printed on the page (§10 row 2). The three
composed orations still have no located exegetical reception, now bounded over
roughly five and a half megabytes more Latin than before [PAT-400]. And the
cheapest repair for that negative — Schuster's *Liber Sacramentorum* vol. 3,
registered in this repository — was again not retrieved [PAT-400, COV-011].

**The page-2 evidencing decision, carried forward unchanged and still
governing.** Page 2 is evidenced from what this repository already holds or may
already cite at an exact locus, in the two-witness form the published
collection uses — a named traditional orientation and a named modern critical
horizon, each at a locus, with the disagreement printed and neither preferred.
Where one of the two is not available, **the row prints a bounded negative
naming what was checked and what the limit is. The author does not go and get
it.** Nothing in this brief authorises retrieval, and the profile's page-2 rule
is satisfied by an honest bound as surely as by a witness. One page-2 bounded
negative is materially relieved this run and one page-2 statement is corrected;
both are at §0.3.

### 0.2 Overlaps reconciled between lanes

Where one witness, passage or ritual moment surfaced in more than one lane, the
accounts are joined and every contributing lane is named. Fourteen joins were
material.

| # | Subject | Lanes | Disposition |
|---|---------|-------|-------------|
| 1 | The Epistle's list lengths, and what a Greek Father may be quoted on | `scripture-context`, `patristic-reception` | **Adjudicated** at §0.3(a). SCR-008 and SCR-034 supply the counts and the mechanism; PAT-101, PAT-151, PAT-152, PAT-153 and PAT-312 supply four Fathers' own lemmata in two languages. The counts and the word list in the prior brief's instruction were both wrong; the instruction itself is sound. Joined at §2.2 |
| 2 | Feltoe 1896 and the Veronense negative | `liturgical-history`, `source-citation-coverage` | **Adjudicated** at §0.3(b). LIT-001 and COV-001 reached the same defect independently and from different directions — LIT-001 by refetching and reproducing both digests, COV-001 by auditing the leaf's own sentences. The negative survives; its stated reason does not. Joined at §4.7 |
| 3 | Cassiodorus | `patristic-reception`, `source-citation-coverage` | **Adjudicated** at §0.3(f). PAT-200/403 retrieved him over plain HTTP; COV-003 independently established that three Cassiodorus editions are registered, one a complete hashed 721-page CCSL 98 scan, and that the TLS failure the prior brief recorded against him belongs to the Honorius host. Two different corrections of one sentence, and both hold. Joined at §2.1, §2.3, §2.4, §2.6 |
| 4 | The precedent corpus boundary | `precedent-search`, `liturgical-history` | **Adjudicated** at §0.3(d). PRE-001 and PRE-003 widen §3.5 by seven full-text missal payloads and by 182 published Triptych documents; LIT-021 finds the same species of defect in §3.3, where a declared snapshot-hashed corpus record went unnamed. One diagnosis covers both: every member is `storage='remote'` or `restricted` with `indexable=false`, so a lane establishing holdings by grepping the working tree sees nothing. Joined at §3.3, §3.5 |
| 5 | `respice in faciem Christi tui` | `patristic-reception`, `theological-synthesis` | Joined at §2.1 and §6.4. PAT-206 adds Cassiodorus naming the figure (hypallage) and PAT-301 adds Theodoret reading the face as the saved people; THE-035 supplies the formulary-internal observation that `Christi` stands twice and both times in the genitive of belonging. **Two readings became three, and the third is patristic, Greek and read in Greek** |
| 6 | The Offertory's `Gustate` | `patristic-reception`, `scripture-context`, `precedent-search`, `theological-synthesis` | Joined at §2.6 and §9.5. PAT-202 supplies Cassiodorus's eucharistic reading anchored in the appointed verbs themselves — which lifts the limit the prior brief had to set on Augustine's, anchored in a superscription the antiphon does not print; SCR-024 supplies the 1 Pet. 2:3 reuse and the `suavis`/`dulcis` split; PRE-010 supplies the Mozarabic rite still singing it at communion; THE-042 supplies the ritual inversion against the Communion |
| 7 | The allegory question at the Gospel's images | `patristic-reception`, `scripture-context` | **Adjudicated** at §0.3(c). PAT-111, PAT-112, PAT-121 and PAT-141 establish that the Latin tradition is namedly divided; SCR-031 independently warns that the lexical fields of `clibanum` and of the grass-and-glory topos invite exactly the move Augustine forbids. Joined at §2.5, §6.6, §7.3 |
| 8 | The displacement of the orations | `liturgical-history`, `precedent-search`, `theological-synthesis` | Joined at §6.1–§6.3 and §7.4. LIT-004, LIT-006 – LIT-016, LIT-019, LIT-023, LIT-024, LIT-026 carry the whole case; PRE-015 adds the Pustet's own adjacency of this formulary to the `Inclina, Domine` formulary; THE-049 supplies the defeater that bounds every Epistle–Gospel join |
| 9 | The Ottobonianus chant cues | `liturgical-history` (this run) **against** the prior run's page-image reading | **Preserved as a live disagreement** at §6.8. LIT-025 fixes the cue blocks' content with certainty and reads their attachment differently from the prior run; **the page image controls and the lane says so itself.** What survives either reading is carried at §7.5 |
| 10 | `concupiscere` across the Introit's psalm verse and the Epistle | `scripture-context`, `theological-synthesis`, `precedent-search` | Joined at §9.6. SCR-023 establishes the shared finite form and the asymmetry (the shared word is inside the appointed Introit; `caro` is one clause past its cut); THE-034 supplies the per-element counts and the cross-proper control; PRE-011 supplies the precedent classification and finds the string absent from all 2,269 lines of the prior brief. **Three lanes reached independently a conjunction no prior lane reached** |
| 11 | `idolorum servitus` glossed as avarice | `scripture-context`, `theological-synthesis`, `precedent-search` | Joined at §2.2 and §9.7. SCR-027 shows both other Vulgate occurrences of the formula gloss avarice, so Anthony's medieval reading has plain scriptural warrant and is not free association; THE-040 supplies the `servi-` distribution joining Epistle and Gospel; PRE-012 classifies the conjunction. **None of the three establishes that Anthony drew it from Eph. 5:5 or Col. 3:5, and none may say so** |
| 12 | The Alleluia's `iubilemus` | `patristic-reception`, `scripture-context`, `theological-synthesis` | Joined at §2.4 and §6.7. PAT-210 (Cassiodorus's wordless jubilus) and PAT-303 (Theodoret's shout of victors) disagree about the one word the Alleluia contributes; SCR-029 shows the collocation `Deo salutari` is rare and its only New Testament occurrence is the Magnificat; SCR-030 and THE-030 show `salutari` is the element's only tie to the rest of the formulary, and that the tie is to three composed orations. **The formulary's thinnest element is no longer thin** |
| 13 | Retrieval traps that resolve successfully and wrongly | `patristic-reception`, `liturgical-history`, `precedent-search`, `cultural-afterlife`, `theological-synthesis` | Joined at §11.3. **Nine instances of one species**, four inherited and five new |
| 14 | The provenance of the guide's patristic English | `source-citation-coverage`, `patristic-reception` | Joined at §4.10 and §11.2. COV-004 establishes that all 70 registered New Advent artifacts have ceased to reproduce and that the loci this guide quotes have no artifact record at all; PAT-311 shows that at one load-bearing sentence the NPNF English is a paraphrase the Greek sharpens. **The text risk is low and the provenance risk is real, and they are different risks** |

### 0.3 Adjudications this brief makes, and the corrections it carries to the prior brief

Nine matters needed deciding rather than recording. **Six are corrections to the
brief this one replaces.** The lanes could not make them, because the file was
immutable to them; this stage is the only stage that may, and leaving one
unmade would republish it.

**(a) The prior brief's instruction about Greek witnesses is sound and its
arithmetic is wrong; it is restated here with the right numbers and the right
words.** The prior §0.3(f) read: "seventeen against fifteen and twelve against
nine — so two appointed vices (`luxuria`, `homicidia`) and three appointed
fruits (`modestia`, `continentia`, `castitas`) receive no comment from a Greek
witness commenting on his own text." **That sentence disagrees with the same
brief's §2.2**, which said of the fruits that "`modestia` and `castitas` answer
nothing" — two words, not three [SCR-034]. Settled as follows.

- *The vice counts.* The **Byzantine** Greek vice-list runs to **seventeen**,
  including φαρμακεία and φόνοι; **fifteen** is the **critical** text's figure,
  produced by the `{NA}` braces deleting μοιχεία and φόνοι [SCR-008]. The
  17/17 equality is arithmetically accidental: the Latin has no counterpart for
  μοιχεία and the Greek no distinct counterpart for the fourth Latin word, and
  the two lists correspond one-to-one only from `idolorum servitus` onward
  [SCR-008]. **A guide saying "the Latin and Greek vice-lists agree in length"
  would be true and misleading.**
- *`homicidia` and `veneficia` fall out of the instruction.* Chrysostom's own
  Greek vice lemma has seventeen and includes both φόνοι and φαρμακεία
  [PAT-312], so the premise that a Greek Father's own text lacks them does not
  hold for the witness this guide actually uses. `luxuria` remains: it is the
  Latin head-word with no distinct Greek counterpart [SCR-008].
- *The fruit surplus is two, not three.* Twelve Latin against nine Greek is a
  surplus of three, but **Jerome states in his own voice that `longanimitas`
  and `patientia` are two renderings of the single μακροθυμία** [PAT-153], and
  `continentia` renders ἐγκράτεια. The appointed fruits with no Greek
  counterpart are therefore **`modestia` and `castitas`** [SCR-034]. The
  three-word reading is arithmetically possible only on a mapping that pairs
  `longanimitas` with ἐγκράτεια, which is not lexically defensible.
- *The ninefold form is the Greek's, and three Fathers in two languages attest
  it.* Augustine's Latin lemma has nine fruits [PAT-101], Jerome's has the same
  nine in the same order [PAT-152], and Chrysostom's Greek has nine in that
  order [PAT-312]. **Any argument built on the number twelve is an argument
  about the Vulgate's rendering, and saying so is not optional.**

**The instruction, restated:** do not put a comment on `luxuria`, `modestia` or
`castitas` into a Greek Father's mouth on the strength of a witness whose list
does not contain the word. Aquinas and Anthony of Padua expound all twelve and
close that gap in Latin (§2.2). **The prior brief's version of this instruction
is reproduced verbatim in the leaf's own `sections/30-commentary.tex`; the
author must correct it there, and this paragraph is the authority for the
correction.**

**(b) Feltoe 1896 *is* registered, and the Veronense negative is now
replayable.** The prior §4.7 stated that "neither Feltoe nor any Veronense
edition is registered, so the search cannot be replayed here at all." Two lanes
found this false independently. The repository registers
`work.catholic-church.sacramentarium-veronense`, the edition
`feltoe-1896`, and **two independent Internet Archive OCR artifacts**, both
members of the declared snapshot-hashed corpus
`corpus.catholic-church.ancient-sacramentaries-2026-08-01`; the work was added
at commit `4acc3743e` on 2026-08-01, before the prior run [LIT-001, COV-001].
Both digests and both line counts were reproduced exactly by refetching
[LIT-001]. **The substantive negative is untouched and is now stronger than
carried**: none of the three orations occurs in either optical layer, on a
seventeen-string search after de-hyphenation and accent stripping [LIT-002].
The defensible reason the prior brief was reaching for is a different one and
is available in the same records: both artifacts are `storage='remote'`,
`indexable=false`, with no bytes in the tree, so **no negative-search binding
could validate against them** [COV-001]. The same paragraph of the prior §4.7
contained the contradiction in adjacent sentences — "neither layer is
registered as indexable", which presupposes registration, followed by "neither
is registered at all" [LIT-001].

**(c) The Latin tradition is namedly divided about allegorising the Gospel's
images, and that resolves the guide's page-1 tension in the tradition's own
favour.** The prior brief carried Augustine's prohibition (its PAT-061, restated
this run inside [PAT-141]) as a live
constraint on the profile's required allegorical row, with no way out but to
preserve the tension. There is now a way out, and it is the tradition's own.
**Hilary of Poitiers argues that the literal sense of this pericope does not
cohere with what precedes it and that a deeper sense is therefore required**,
and allegorises across the appointed verses completely: the birds are the
unclean spirits, the cubit is the resurrection body raised to the measure of
the perfect man, the lilies are the brightness of the angels, the hay burnt
tomorrow is the gentiles [PAT-111, PAT-112]. **Jerome expressly forbids
allegorising the birds**, and on a ground internal to the appointed verse — if
the birds were angels the *a fortiori* to men would not follow [PAT-121]. So
the division is: Hilary for, Jerome and Augustine against, with a fourth
reading (Remigius, birds and lilies as holy men) reaching this brief **only
through the Catena and remaining a lead** [PAT-141]. **Settled: the guide
reports a named, checked, patristic allegorical reading and reports the two
Fathers who forbid it, and adjudicates neither.** Two qualifications travel
with Hilary and must not be dropped: his hay-as-gentiles reading ends in a
doctrine of the bodily eternity of the damned that no other witness in the
sweep states, and his birds-as-unclean-spirits reading works *against* the
pericope's consoling sense [PAT-112]. And Jerome's target is a reading of the
**birds** as angels while Hilary reads the **lilies** as angels; **Jerome must
not be reported as refuting Hilary**, though Jerome names Hilary among the
Latin commentators he had read [PAT-121].

**(d) The precedent corpus is wider than §3.5 declared, and every "not located"
classification is bounded by the wider corpus now.** The prior §3.5 bounded
every classification to the Pustet 1862 missal plus the published Triptych
propers leaves, and stated "It reaches no sanctoral or votive tree." Seven
further full-text missal payloads are tracked, indexable and present in the
working tree — three Mozarabic, three Ambrosian, and the Venice 1570 and
Vatican 1604 Roman editions [PRE-001] — and the enumeration omitted the
articles, theology, devotions, history, biographies, curriculum and reference
trees, of which at least four documents treat this formulary's appointed
material directly [PRE-003]. **This does not by itself relocate any
classification**, and the lane says so: it says the boundary moved and names
what moved it [PRE-001]. Two consequences are real. The Ambrosian and Mozarabic
books yielded genuine comparative evidence (§6.9, §9.2) that the old boundary
excluded by construction. And **the OCR of five of the seven is worse than the
Pustet's**, so a whole-phrase negative over them is weak evidence of absence —
the Ambrosian Pachel 1499 text returns zero for `dominus`, `oremus`,
`evangelium` and `introitus` over a million characters and cannot support
phrase search at all [PRE-002].

**(e) Two quotations in the prior brief's notable-and-quotable audit were
attributed to the wrong speaker, and both are corrected here.** At the prior
§8.2, "the authoritative declaration that no man can serve two masters" was
presented as the Supreme Court's own phrase. **It is not.** It is the Court of
Claims' phrase, in *Michigan Steel Box Co. v. United States*, 49 Ct. Cl. 421,
439, quoted in a footnote by both *Mississippi Valley* and *Capital Gains*, and
must be attributed there [CUL-002]. And the sentence "the rule is not intended
to be remedial of actual wrong, but preventive of the possibility of it" is not
*Everhart v. Searle* speaking in its own voice: it is the court's quotation of
**Hare and Wallace's Notes, 1 *Leading Cases in Equity*, p. 210** [CUL-002].
Both errors came of reassembling API snippets; both were found by reading the
Caselaw Access Project's continuous transcription of the printed reporter. The
prior brief also recorded that the ordering of the two *Everhart* fragments was
not established; **it is now** — the two-masters invocation opens the opinion
and the Hare and Wallace quotation comes later, in the discussion of policy
[CUL-002].

**(f) The Cassiodorus statement was wrong twice over, and both halves are
corrected.** The prior §4.2 read: "Cassiodorus, registered but with no payload,
and the probe of documentacatholicaomnia.eu failed on TLS certificate
verification." *Holdings:* three Cassiodorus editions are registered, one of
them a complete hashed 721-page Google scan of **CCSL 98** (Pss. 71–150),
`storage='restricted'`, whose title pages and one interior page were rendered
and visually inspected [COV-003]. *Provenance:* documentacatholicaomnia.eu is
the **Honorius** host, and its certificate failure is recorded in the Honorius
artifact record, not Cassiodorus's [COV-003]. *And the underlying absence is
gone*: the complete *Expositio in Psalterium* was retrieved in Latin from
Corpus Corporum and comments on all four appointed psalms [PAT-200]. **Two
limits replace the false one.** CCSL 98 runs Pss. 71–150, so it reaches
Pss. 83, 94 and 117 but **not Ps. 33**, which is the appointed psalm the guide
most needs him for; and Adriaen's 1958 edition is in copyright, so that
artifact is summarise-only and can never supply published Latin [COV-003]. The
Latin actually quotable is the Corpus Corporum transcription of Migne PL 70,
which is **inspected and not verified**: no PL 70 page image and no CCSL
collation [PAT-405].

**(g) The `hope-formula-past-the-cut` membership is upheld, on the criterion
the prior brief adjudicated, and the criterion is now bounded across the whole
Vulgate.** The relation keeps `[introit, gradual, offertory]`. The prior
adjudication turned on the relation being named *past the cut* and not
*contains*. `scripture-context` now bounds it further: the formula
`beatus [noun] qui sperat` stands in **exactly two verses of the whole
Clementine Vulgate** — Ps. 33:9b and Ps. 83:13 — **and those are precisely the
two psalms supplying this Mass's Offertory and Introit** [SCR-016]. That makes
the coincidence precise rather than impressionistic. **The weakness travels
unchanged and must be printed with it:** the three cuts have duller
explanations, metrical length and the ordinary bounds of an antiphon among
them, and **no intent is established by anything in any lane** [SCR-016].

**(h) `fruit-count-unsettled` stays dropped as an interpretive proposal, and
the reason is now stronger.** The prior brief dropped it because the count is
not unsettled at the level of the tracked texts and because the fruit list
stands in the Epistle alone, failing the two-element floor. Both hold. What is
added is that the *reception* is now richly divided about the two lists'
asymmetry — **four distinct accounts of it**, from the prior run's THE-020, Augustine
[PAT-102], Origen through Jerome [PAT-156] and Chrysostom [PAT-313] — so the
material is better than it was and is retained as documented reception in the
detailed commentary (§2.2), where it belongs. **It is not a proposal, and the
manifest's element membership `[epistle, communion, gospel]` for that relation
is still unsupported by anything any lane has gathered.**

**(i) `sunday-number-not-the-mass-own` stays routed to source-grounded
synthesis as claim C4, not to Interpretive Possibilities.** Unchanged, and
independently reproduced by this run's precedent lane, which reaches the same
disposition for the same reasons and adds only the Pustet corroboration of the
adjacency [PRE-015]. It joins no two appointed elements by a mechanism of its
own, and published as a proposal it would restate a neighbouring guide's
sourced finding.

### 0.4 The fresh join of run `e5b24f405bde9691`, and what it changes

The seven lanes ran again against the re-authored leaf and returned 69
findings. The sweep is **re-verificatory in character**: the scripture,
patristic and liturgical-history lanes re-ran the first join's mechanical
comparisons and retrievals from scratch rather than restating them, and every
leg they re-ran held. What the fresh join adds falls into five classes, and
this section is the settlement of all five.

**(a) One correction to a settled claim: the C6 imperative distribution.**
The first join's C6 carried a third distribution — every imperative addressed
to God is `aspice`, `respice`, `Custodi` and the orations' subjunctives, and
the only imperative addressed to the assembly is `Quaerite`/`Primum quaerite`
[THE-036]. **A fresh mechanical probe of the appointed Latin contradicts both
halves**: the Secret opens with a fourth God-directed imperative, `Concéde`
(verified at `propers/verified.md` element 8, line 413, working tree), and the
scriptural elements carry at least seven further assembly-directed imperatives
besides `Quaerite` — `ambulate` (Ep.), `Venite` (All.), `Respícite`,
`Considerate`, `Nolite … esse` (Gosp.), `gustate`, `videte` (Off.)
[fresh:THE-107]. The correction is applied at §7.6 below; **the published
sentence in `sections/20-themes.tex` lines 126–128 states the withdrawn
three-item list and must be corrected by the author.**

**(b) Fresh candidate movements for the cross-proper layer.** The
theological-synthesis lane re-derived its stem distributions from the appointed
text and returned thirteen findings. Their dispositions:

| Fresh id | Subject | Disposition |
|---|---|---|
| fresh:THE-101 | `servi-` in exactly two elements (Epistle's `idolorum servitus`, Gospel's `servire` twice) | **Confirms and sharpens** the brief's §2.2/§9.7 material; the constructional asymmetry (noun-phrase genitive against finite-verb complement) and the Anthony-numbering defeater travel with any use |
| fresh:THE-102 | `concupi-` in exactly two elements with opposite objects | **Confirms** §9.6/P6 from the appointed text; both recorded bounds travel (the `caro` clause lies past the Introit's cut; ordinary-verb senses; no compiler intent) |
| fresh:THE-103 | Comparative a fortiori as the formulary's argument form, with the Gospel's `Ideo` hinge | **Confirms** §9.1/P1's corrected mechanism; the Hebrew-idiom defeater and the no-softening rule travel unchanged |
| fresh:THE-104 | `regnum Dei` as the only three-element substantive content word | **Confirms** C1 (§7.1); the fresh lane verified the `regn-` leg and the divine-name spot-checks directly and leaves the exact-form pairwise map a floor, not a ceiling |
| fresh:THE-105 | The flesh crucified is not the body fed (`caro`/`corp-` disjoint) | **Confirms** C2 (§7.2); the class-1 lexical disjointness and the class-3 three-way resolution both re-verified |
| fresh:THE-106 | Propitiation and salvation saturate the unsung prayers, Alleluia the single tie | **Confirms** P3 (§9.3); the `propiti-` family's eleven-of-fifteen figure remains carried from the prior run and NOT re-verified, so the claim stays about the substantive |
| fresh:THE-107 | **The C6 imperative distribution is contradicted by the appointed text** | **Correction** — applied at §7.6; see (a) above |
| fresh:THE-108 | Fear and trust as paired dispositions across Gradual and Offertory | **Recorded as an unresolved lead, NOT retained as a proposal**: no precedent or conjunction search has reached it (the lane's own bound), so the profile's precedent rule forbids publishing it; both defeaters travel (stock psalm vocabulary; two contested patristic divisions) |
| fresh:THE-109 | `adic-` confined to Gospel and Communion; Aquinas half is documented reception | **Confirms** P2 (§9.2) in its reduced form; the forced reductions at §9.2 travel unchanged |
| fresh:THE-110 | Petition against promise as the formulary's central tension, resolved by the objects differing | **Confirms** C6's substance; integrates fresh:THE-107's correction into its third distribution |
| fresh:THE-111 | The two temporal horizons (Introit's one day; Postcommunion's perpetual effect) | **Confirms** the brief's anagogical material; Cassiodorus's dependence caveat and Theodoret's contrary reading travel |
| fresh:THE-112 | **Bounded negative**: no theological stem joins two or more elements beyond the recorded exceptions (`concupi-`, `servi-`, `christ-`) | **New bound for §7/§9**: the Epistle's law-inclusio and its fourfold `adversus` remain single-element readings and may not be published as cross-proper claims under the two-element floor |
| fresh:THE-113 | The Communion's recasting gives the Gospel's last verse to the communicant as address, with Aquinas's three-member exposition the nearest thing to Doctoral commentary on it | **Confirms** C5 (§7.5); the C5/C3 data-sharing rule and the not-crossing line at §7.5 travel whole |

**(c) Fresh precedent classifications, and two registry discoveries.** The
precedent lane re-ran its conjunction sweep against the widened corpus and
returned eleven classifications, all recorded with their anchors, search
boundaries and controlling limits at new §9.10. Two discoveries are material
beyond the classifications. **First, chants this Mass presents as single-use
are not**: the tracked 1962 registry appoints this Sunday's Gradual verses
(Ps. 117:8–9, `Bonum est confidere`) a second time on Friday of the Fourth
Week of Lent, and the Introit's psalm text (Ps. 83:10, 9) three further times
as Gradual or Second Gradual — Monday of the First Week of Lent and the Lent
and September Ember Saturdays [fresh:PRE-005]. **The leaf nowhere records
these, and the author must not present the chants as single-use.** Secondly,
**a second 1962 Mass hears this Sunday's Gospel**: the registry gives
Mt. 6:24–33 also to the S. Caietani Confessoris formulary (registry
1962-08-07), and a bounded negative search confirms the leaf nowhere mentions
it [fresh:PRE-006] — relevant to any claim about the Gospel–formulary bond and
to C4's Sunday-number material at §7.4.

**(d) Fresh cultural-afterlife candidates.** The lane re-ran its sweep and
returned four findings: two are fresh re-establishments of entries this brief
already carries at §8.2 and §8.3 (the two-masters rule and `Adversus
huiusmodi non est lex`, each now read continuously from the CAP
transcriptions with the corrections of §0.3(e) confirmed) [fresh:CUL-001,
fresh:CUL-002], and two carry a **new family** — the lily clause "they toil
not, neither do they spin" (Mt. 6:28) inverted into the standing judicial
description of swindlers and idlers, with *State v. Tracy* (Mo. 1922) read
whole as a second attestation independent of *State v. Whiteaker*
[fresh:CUL-003, fresh:CUL-004]. That family was already this brief's strongest
unselected candidate (§8.6, CUL-020); the fresh sweep upgrades its evidence
state and is recorded at new §8.7. **The gallery's published selection of five
is unchanged** — the cap of five and the mechanism overlap with §8.5 still
govern — and the fresh material is left to the author as the strongest
documented substitute.

**(e) Fresh coverage findings against the re-authored leaf.** The
source-citation-coverage lane audited the leaf as re-authored and returned
eight findings, recorded with their evidence at new §10.1. In summary:
`sections/99-references.tex` was not re-authored with the rest of the leaf and
now affirmatively contradicts the body (it names Augustine's *Expositio ad
Galatas* among instruments not retrieved while the same commit's commentary
uses it extensively) [fresh:COV-012]; `research/source-bindings.toml` is stale
in the same direction, its header declaring six witnesses NOT REACHED that the
body uses [fresh:COV-013]; the Enarrationes entry asserts a restricted New
Advent registration that exists at none of the four appointed psalms
[fresh:COV-014]; every patristic witness the re-authoring added has no
source-library record at the loci used, so the guide's new citations rest on
transcriptions held nowhere in the repository [fresh:COV-015]; the primary
witnesses that would replace the derivative citations (PL 37 complete, the
complete Theodoret PG 80 facsimile, Schuster vol. 3) are registered, hashed
and remote [fresh:COV-016]; the NABRE bounded negative re-checked clean
[fresh:COV-017]; the rights risks are enumerated [fresh:COV-018]; and the
References exclusion list's holdings statements for Papias, Eusebius HE III,
Irenaeus III.1.1 and Jerome's Comm. in Gal. were re-verified and check out
[fresh:COV-019]. **All four repairs are authoring-stage work**; none is
research this workflow owes, and none blocks authoring, but §10.1 states
where each must land.

**(f) Re-verification confirmations, recorded rather than restated.** The
scripture lane re-ran the whole mechanical comparison of the appointed blocks
against the tracked Clementine and reproduced the first join's opcode counts
exactly, including the exhaustive negative: apart from the Communion's
recasting, every departure is exhausted by orthography, pointing, the
capitalisation rows, the supplied incipits and the three clean cuts
[fresh:SCR-002, fresh:SCR-024, confirming §1.2]. It re-counted the formulary's
loci and lexical map [fresh:SCR-001, fresh:SCR-007, fresh:SCR-023,
confirming §1.1, §1.3 and §1.4], re-established the `beatus … qui sperat` two-verse
coincidence over the whole Vulgate [fresh:SCR-008, confirming §0.3(g) and
§9.4], and re-ran the stem probes behind §2 and §9's lexical ties
[fresh:SCR-012–SCR-019, fresh:SCR-025]. The patristic lane re-fetched
Cassiodorus complete from Corpus Corporum and reproduced **exactly the route
and digest this brief records at §3.2** (`idno=21404`, sha256 `c23aef1a…a153`),
then re-read his direct commentary at all four appointed psalms with the same
substantive results [fresh:PAT-001–fresh:PAT-004, confirming §2.1, §2.3,
§2.4, §2.6]. The liturgical-history lane re-fetched the Wilson 1915 Hadrianum
OCR from its registered source, reproduced the registered SHA-256, byte size
and line count exactly, and re-confirmed the first join's LIT-023 finding —
the Hadrianum carrying all three orations of this Mass as one Sunday Mass —
from freshly refetched bytes of the same witness, which is corroboration in
the same evidence state and not an independent witness [fresh:LIT-101,
fresh:LIT-102, confirming §6.1 and §2.8].

**(g) Two bounds the fresh join leaves open, named so that silence cannot
restate them.** First, the liturgical-history lane's evidence for
fresh:LIT-103 (the N+1 Gregorian offset, corroborated over five consecutive
sections) declares a cross-check against the tracked 1962 registry
`in progress as part of this sweep; to be recorded at its own finding`, and
**the join carries no finding recording that cross-check's completion**. The
identifications therefore stand at the level of OCR read against the tracked
registry — a repository derivative — with the printed missal controlling
where they disagree, exactly as §6.1 already bounds. Second,
fresh:THE-108's fear-and-trust conjunction was reached by no precedent
search: it is a lead under §9.7's discipline, and it may not be published as
a proposal unless a later authorised sweep reaches its conjunction.

---

## 1. The formulary, its appointed text, and what was verified about it

### 1.1 Inventory

The formulary appoints six distinct biblical loci across seven scriptural
elements, and its three orations quote no Scripture directly [SCR-001]:

| Element | Locus (Vulgate) | Modern English number | Relation to source |
|---|---|---|---|
| Introit antiphon | Ps. 83:10–11a | Ps. 84:9–10a | verbatim; cut at `super millia` |
| Introit psalm verse | Ps. 83:2–3a | Ps. 84:1–2a | verbatim; cut at `in atria Domini` |
| Collect | — | — | composed |
| Epistle | Gal. 5:16–24 | — | verbatim, less the incipit |
| Gradual | Ps. 117:8–9 | Ps. 118:8–9 | verbatim, two whole verses, nothing cut |
| Alleluia | Ps. 94:1 | Ps. 95:1 | verbatim from `Venite` |
| Gospel | Mt. 6:24–33 | — | verbatim, less the incipit |
| Offertory | Ps. 33:8–9a | Ps. 34:7–8a | verbatim; cut at `suavis est Dominus` |
| Secret | — | — | composed |
| Communion | Mt. 6:33 recast | — | **the one substantive recasting** |
| Postcommunion | — | — | composed |

The Communion is a seventh element on a sixth locus: it reuses Mt. 6:33,
already appointed as the Gospel's last verse. The formulary appoints no Tract,
Sequence, second oration, blessing or ritual text. **The negative about the
orations is bounded to direct quotation**: loose verbal echo in a composed
oration is a different question, no lane searched for it, and no lane makes any
claim either way [SCR-001, SCR-033(d)].

### 1.2 Text-critical facts established mechanically this run

Every appointed biblical text except the Communion is a **verbatim** quotation
of the tracked Clementine Vulgate. This was re-executed independently this run,
not carried: each appointed Latin block was normalised (accents, i/j, u/v,
ae/oe, ii/i, ll/l, punctuation, case) and compared word for word — the Epistle
body at 108 normalised words against 108, the Gospel body at 176 against 176,
with `difflib` reporting no non-equal opcode in either [SCR-002]. This matters
because `guidance/bibles-for-agents.md` warns in terms that Mass chants must
not be assumed to match any tracked psalter. Here the check was run and, for
this formulary, they do.

**The bound is the same bound the prior sweep recorded and must travel with the
result:** this answers *does the appointed wording match the tracked
Clementine*, which is narrower than *which psalter does this chant descend
from*. No Psalterium Romanum, Vetus Latina, *iuxta Hebraeos*, Sabatier,
Weber/Stuttgart or Nova Vulgata witness is registered here, and no chant book
was consulted, so **the Gallican-versus-Roman question remains unanswerable in
this repository** [SCR-002, SCR-021, SCR-033(b)].

The normalisation deliberately absorbs real but non-verbal orthographic
differences: the missal prints `milia`, `adicere`, `adicientur`, `huiusmodi`,
`iubilemus` where the tracked Clementine prints `millia`, `adjicere`,
`adjicientur`, `hujusmodi`, `jubilemus` [SCR-033(a)].

**The Communion departs from Mt. 6:33 in exactly four ways** [SCR-003]:
`ergo` is dropped and `Primum` promoted to head the clause; `et iustitiam eius`
is omitted; `haec` is dropped before `omnia`; and `dicit Dominus` is added.
`dicit Dominus` stands in none of Clementine Mt. 6:33, Clementine Lk. 12:31 or
Robinson-Pierpont Mt. 6:33. **Two things about the Lucan parallel, and the
second is new this run.** Luke keeps `iustitiam eius`, so the omission is not
explained by Lucan conflation; and **Luke also places `primum` after the verb,
not at the head**, so the antiphon's word order is not borrowed from the Lucan
form either. That leaves the promotion unexplained by any tracked Gospel text —
which is a statement about what the tracked texts do not supply and **not** a
claim about what produced the antiphon [SCR-003].

**No second substantive recasting exists** [SCR-033(a)]. Apart from the
Communion, the departures found across every appointed block are exhausted by
orthography, pointing, the two capitals below, the supplied incipits, and the
clean cuts at Ps. 83:11a, Ps. 83:3a and Ps. 33:9a. **No centonisation,
transposition or interpolation was found in any element.** This is the
strongest of the run's negatives because it rests on an exhaustive mechanical
comparison rather than on a failure to find.

**Two capitalisation differences fall exactly on the words that would carry
typological weight** [SCR-020]: the missal prints `faciem Christi tui` where the
tracked Clementine prints lower-case `christi`, and `Immittet Angelus Domini`
where the Clementine prints lower-case `angelus`. **Firm caveat that must
travel with any use of this:** capitalisation in a modern electronic Clementine
is that e-text's editorial convention and capitalisation in the 1962 missal is
that book's; neither is evidence of what the Latin intends, and in the psalm's
own sense `christus` is the anointed king. It would be easy to build a
typological claim on the missal's capital C or a christological one on its
capital A, as though the psalm supplied them. It does not. **Cassiodorus is
positive evidence that a Latin reader could take the Offertory's angel
otherwise** (§2.6) [PAT-203].

### 1.3 Psalm numbering, read from the concordance and not restated from memory

The appointed loci's modern English numbers are Ps. 84:9–10 with 84:1–2,
Ps. 118:8–9, Ps. 95:1 and Ps. 34:7–8, and the offset is produced by whether the
psalm's superscription is separately numbered [SCR-019]. Read directly from the
tracked project-created concordance
(`…/challoner-gutenberg-1581/artifacts/psalm-numbering-ee3c7757/psalm-numbering.tsv`),
which `scripts/_psalms.py` declares the sole authority and which
`guidance/bibles-for-agents.md` forbids restating from memory. Rows read: Ps. 33
and Ps. 83 at `english_offset=1` with the inscription mapped to English
`title`; Pss. 94 and 117 at `english_offset=0`; all four
`english_offset_uniform=yes`. These agree with the numbers the leaf's own
`propers/verified.md` prints after its 2026-08-27 correction [SCR-019].

**Bound the author must carry:** "modern English" is not "Masoretic". The
concordance's Hebrew column numbers the superscription in both offset psalms,
so under strict Masoretic versification the Introit is 84:10–11 and the
Offertory 34:8–9. The parenthetical a reader needs is the English one. **No
Hebrew text of these psalms is held here**, so the Masoretic half rests on the
concordance's declared columns and not on a Hebrew Bible [SCR-019, SCR-021].

**Two numbering hazards in the reception sweep, and the second is new.** (1)
The New Advent/NPNF pages for Augustine's *Enarrationes* carry two numbering
systems at once, so every appointed psalm locus must be shifted twice; the
offset is absent at Pss. 117 and 94 for reasons peculiar to those psalms, which
is a coincidence and not a general property. (2) **Cassiodorus's own verse
numbering for Ps. 33 runs one behind the missal's**, so his *Vers.* 7 and 8 are
the missal's Offertory vv. 8 and 9, and the same offset appears at Ps. 83,
where his *Vers.* 1 is the missal's v. 2 [PAT-205]. **A lane resolving loci
from Cassiodorus's verse tags will mis-cite the Offertory by one verse.**

### 1.4 The lexical map of the ten appointed elements

New this run and exhaustive at its threshold, so it may be used as a floor on
the ties between elements [SCR-022]. The ten elements were normalised, reduced
to word forms of more than three letters with a function-word stop list
removed, and intersected pairwise. Exact forms only, no lemmatisation.

**Forms standing in three or more elements:** `deus` (Introit, Gospel,
Postcommunion); `domine` (Introit, Collect, Secret); **`regnum` (Epistle,
Gospel, Communion)**. No other form reaches three. **`Regnum` is therefore the
only substantive content word joining three appointed elements; every other
three-element form is a divine name.**

Complete pairwise content-word ties: Introit–Collect `domine`; Introit–Epistle
`christi`, `concupiscit`; Introit–Gospel `anima`, `deus`; Introit–Offertory
`domini`; Introit–Secret `domine`; Introit–Postcommunion `deus`; Collect–Secret
`domine`, `quaesumus`; Epistle–Gospel `regnum`, `sicut`; Epistle–Communion
`regnum`; Gradual–Alleluia `domino`; Gospel–Communion `adicientur`, `primum`,
`quaerite`, `regnum`; Gospel–Postcommunion `deus`; Offertory–Communion
`dominus`.

Supporting stem counts over the same ten elements: `caro`/`carn-` 5, Epistle
only; `corp-` 2, Gospel only; `spiritu-` 5, Epistle only; `sper-` 2 and
`confid-` 2, Gradual only; `exsult-`/`iubil-` 2, Alleluia only; `christ-` 2,
Introit and Epistle only; `propitia-` 2, Collect and Secret only; `perpetu-` 2,
Collect and Postcommunion only; `salut-`/`salv-` 4, one each in Collect,
Alleluia, Secret and Postcommunion [SCR-030]; `sollicit-` 3, Gospel only, all
prohibitive, and `tim-` 1, Offertory only [THE-038]; `advers-` 4, Epistle only
[THE-043]; `lex`/`leg-` 2, Epistle only [THE-041]; `fid-` in exactly three
elements — Epistle 1, Gospel 1, Gradual 2 as the compound `confidere`
[THE-051]; `servi-` in exactly two, Epistle 1 and Gospel 2 [THE-040];
`concupi-` in exactly two, Introit 1 and Epistle 2 [THE-034].

**Limit, and it is the reason the stem counts are listed separately:** the
pairwise map is exact forms only. A tie carried by different inflections of one
root, or by synonymy, does not appear in it, **so it is a floor on the ties and
not a ceiling** [SCR-022]. Two of this brief's claims turn on a *semantic*
thread the map by construction cannot see (§7.6, THE-037). And whether any tie
is meaningful is synthesis, which the map does not settle.

**Two counting traps a later worker will meet** [THE-044, THE-038]: a bare
`tim` search hits `vestimento`/`vestimentum` in the Gospel and a bare `anim`
search hits `longanimitas` in the Epistle; and a literal multi-word sweep over
the collated `verified.md` records is defeated by line wrapping, which produced
a false negative on `sperat in eo` until newlines were collapsed and blockquote
markers stripped.

---

## 2. Passage-by-passage reception matrix

Every distinct appointed passage receives a row. "Direct exegesis" means a
witness commenting on the appointed verse itself; "illuminating reuse" means a
witness using it for something else. **No witness below is *verified* in the
source-library sense**; the state given is the highest each record establishes,
and §11.2 states the ceiling for the whole class.

| # | Passage | Other propers using it | Direct ancient exegesis checked | Medieval / Doctoral / later reception checked | Material negative |
|---|---|---|---|---|---|
| 2.1 | Ps. 83:10–11a, 2–3a (Introit) | Ps. 83 also supplies the Fifth Sunday after Pentecost's Gradual, in an **adapted** form (`super servos tuos` for `in faciem Christi tui`) — the prior run's PRE-019, independently reproduced this run at [THE-035] | Augustine, *Enarr. in Ps. LXXXIII* §6, §14, §15 — Latin collated (prior run, restated); **Cassiodorus, *Expos. in Ps.* LXXXIII vv. 2, 10, 11–12, in Latin** [PAT-206, PAT-207, PAT-208]; **Theodoret, *Interpretatio in Ps.* LXXXIII, PG 80:1541–1545, read in Greek** [PAT-301, PAT-302] | Guéranger, *The Liturgical Year* XI, pp. 326–327, reading it nuptially and differently from both Latin Fathers (prior run, restated) | Ps. 33 aside, no Latin witness offers a historical setting for this psalm; Theodoret's Babylonian-captivity setting is his own reconstruction [PAT-302]. Cassiodorus at the antiphon is **probably dependent on Augustine and is not a second independent vote** [PAT-207] |
| 2.2 | Gal. 5:16–24 (Epistle) | none in the collated set | **Augustine, *Expositio ad Galatas* ss. 45–53, continuous on the whole appointed pericope, in Latin** [PAT-100 – PAT-108]; **Jerome, *Comm. in Gal.* lib. III ad 5:16–24, verse by verse, in Latin** [PAT-150 – PAT-161]; **Chrysostom, *In ep. ad Galatas* PG 61:673–674, read in Greek** [PAT-310 – PAT-315]; Origen, *Stromata* lib. X, **only through Jerome** [PAT-155, PAT-156] | Aquinas, *Super Galatas* cap. 5 lect. 5–6, in Latin (prior run, restated); Anthony of Padua, *Sermo Dominica XIV post Pentecosten*, in Latin (prior run, restated); Guéranger p. 328 tying the Collect to the vice-list (prior run, restated) | Theodoret's *Interpretatio epistolae ad Galatas* (PG 82) not retrieved [PAT-401]; Ambrosiaster, Marius Victorinus, Pelagius, the *Glossa ordinaria*, Nicholas of Lyra, Denis the Carthusian and a Lapide's commentary proper not swept [PAT-402]; Cyprian's *De zelo et livore*, named by Jerome, not opened [PAT-159] |
| 2.3 | Ps. 117:8–9 (Gradual) | none in the collated set | Augustine, *Enarr. in Ps. CXVII* §4 — Latin collated (prior run, restated); **Cassiodorus, *Expos. in Ps.* CXVII vv. 7–9, in Latin** [PAT-211, PAT-212, PAT-213]; **Theodoret, *Interpretatio in Ps.* CXVII, PG 80:1812, read in Greek** [PAT-305, PAT-306] | — | Chrysostom's *Expositio in Ps. CXVII* (PG 55) not retrieved, twice now [PAT-401]; Bellarmine's Latin *Explanatio in Psalmos* not swept [PAT-402]; **PL 37 not opened, so the accusative/ablative variant at Augustine's lemma is still unresolved** — though Cassiodorus's lemma agrees with the missal's ablative and is one data point against it [PAT-213] |
| 2.4 | Ps. 94:1 (Alleluia) | none in the collated set | Augustine, *Enarr. in Ps. XCIV* §§2–3 — Latin collated (prior run, restated); **Cassiodorus, *Expos. in Ps.* XCIV v. 1, in Latin** [PAT-209, PAT-210]; **Theodoret, *Interpretatio in Ps.* XCIV, read in Greek** [PAT-303, PAT-304] | — | No medieval or later witness located for this verse. Theodoret's Josiah setting is his own reconstruction from 4 Kgs 22–23 and not something the psalm states [PAT-304] |
| 2.5 | Mt. 6:24–33 (Gospel) | Mt. 6:33 is also this Mass's Communion, recast | Augustine, *De sermone Domini in monte* II.47–58 (prior run, restated); Chrysostom, *Hom. in Matt.* 21–22, **still NPNF English only** (prior run, restated); **Hilary, *Comm. in Matt.* cap. V ss. 5–13, in Latin** [PAT-110 – PAT-113, PAT-136]; **Jerome, *Comm. in Matt.* lib. I ad 6:24–34, in Latin** [PAT-120 – PAT-126] | **Aquinas, *Super Matthaeum* cap. 6 lect. 5, in Latin — a continuous commentary, distinct from the Catena** [PAT-130 – PAT-135]; *Catena aurea* cap. 6 lect. 17–21, **now a checked map for Hilary and Jerome and a lead-map for the rest** [PAT-140]; Augustine, *De opere monachorum* (prior run, restated) | Chrysostom's *Hom. in Matt.* 21–22 in Greek (PG 57) not retrieved [PAT-401]; Bede, Rabanus, Paschasius, Christian of Stavelot, Remigius in his own person, Bruno of Segni, Albert, Nicholas of Lyra, Maldonado and the *Opus imperfectum* in its own right not swept [PAT-402]; Augustine's *De haeresibus* still unopened, so the Euchite identification is still an unverified lead [PAT-132] |
| 2.6 | Ps. 33:8–9a (Offertory) | Ps. 33:9 **whole**, with the hope-clause, is the Eighth Sunday after Pentecost's Communion, now attested from **two tracked primary printings** [PRE-008]; Ps. 33:8–9 has exactly two Roman Offertory uses in the searched missals, the other after the Canaanite-woman Gospel, confirmed in a witness 292 years earlier than the Pustet [PRE-008] | Augustine, *Enarr. in Ps. XXXIII* **Sermo II** — Latin collated (prior run, restated); Cyril of Jerusalem, *Myst. Cat.* V.20 and Ambrose, *De mysteriis* IX.58 (prior run, restated); **Cassiodorus, *Expos. in Ps.* XXXIII vv. 7–8 and the *Divisio psalmi*, in Latin** [PAT-201 – PAT-204] | Bellarmine registered but at Ps. 33 vv. 2–3, reaching no appointed verse, in an abridged English translation (prior run, restated) | Theodoret on Ps. 33 is in *Interpretatio in Psalmos* Tomus 1 and was not fetched this run, **because a verified passage record for him at PG 80:1101–1109 is already held** [PAT-300]; Cyril's authorship disputed and not swept |
| 2.7 | Mt. 6:33 recast (Communion) | see 2.5 | Augustine, *De serm. Dom.* II.53, II.55, II.56 on `primum` — the decisive sentence corroborated in Latin from an independent thirteenth-century witness (prior run, restated) | **Aquinas, *Super Matthaeum* cap. 6 lect. 5, expounding all three members of the verse** [PAT-135]; **Hilary, cap. V s. 12, reading the seeking as the wage of our life** [PAT-136]; Guéranger p. 342 judging the antiphon **not primitive** (prior run, restated) | **No witness comments on the antiphon**; every witness comments on Mt. 6:33 in its Gospel place, so the observation that the antiphon promotes `Primum` remains editorial and not patristic [PAT-135] |
| 2.8 | Collect, Secret, Postcommunion (composed) | Secret has a second Gelasian home at Book III sect. XLI, a Lenten ferial home at Gerbert p. 60 and a saints'-Mass home in the same volume [LIT-013]; Postcommunion has a saint-adapted recension at Book II sect. **LXVIII** [LIT-015] and stands in Wilson's appended, unnumbered series at p. 237 [LIT-014] | **none located** | Guéranger only: one interpretive sentence on the Collect, one restating sentence each on the Secret and Postcommunion (prior run, restated) | **NEGATIVE, BOUNDED, and now bounded over roughly 5.5 MB more Latin** [PAT-400] — see §4.1 |

### 2.1 Introit — Ps. 83:10–11a with Ps. 83:2–3a

**Textual setting** [SCR-012]. Ps. 83 is a Korahite psalm of desire for the
sanctuary: the sparrow and turtle-dove at the altars (v. 4), those who dwell in
the house (v. 5), the ascents through the vale of tears (vv. 6–7), `ibunt de
virtute in virtutem` (v. 8), and the prayer `Domine Deus virtutum, exaudi
orationem meam` (v. 9) standing immediately before the antiphon's own v. 10.
**The two cuts have opposite effects on what the excerpt carries in:** cutting
v. 11 at `super millia` removes the psalm's explicit two-way choice between the
house of God and the tents of sinners; cutting v. 3 at `in atria Domini`
removes `cor meum et caro mea exsultaverunt in Deum vivum` — **the only place
in this Mass's psalm sources where `caro` carries a positive sense**, verified
against the ten appointed elements, where `caro`/`carn-` stands five times in
the Epistle and nowhere else [SCR-012, SCR-022]. Both dropped clauses are the
psalm's, not the antiphon's, and the antiphon asserts neither.

**A rare idiom, inverted, and now bounded across the Vulgate** [SCR-026]. The
collocation `faciem christi tui` stands in exactly three verses of the
Clementine — Ps. 83:10, Ps. 131:10 and 2 Par. 6:42 — and **the Introit is the
only one of the three in which it is a positive petition to look**; in the
other two it is a petition *not to turn away*. Widening to
`(avertas|averteris|avertat|avertisti) faciem` returns nine verses, of which
only those two apply the idiom to the face of the anointed; the other seven
have God's own face as object. **The caveat at §1.2 governs any use of this:**
the Clementine prints `christi` lower-case in all three places, and in the
psalms' own sense `christus` is the anointed king. The distribution establishes
that the Introit inverts a rare idiom's usual direction; **it establishes
nothing about who the anointed is, and no typological reading is licensed by
it.** The lane also flags, and does not assert, that 2 Par. 6:42 is a
temple-dedication prayer, that the Introit is a temple psalm, and that the
appointed Gospel names Solomon — **joined by nothing in the appointed texts,
and flagged as inference** [SCR-026].

**Augustine reads the two halves as one movement of desire** (prior run,
restated at [PAT-207] through Cassiodorus's dependence on him). On the psalm
verse: "My soul longs and fails for the courts of the Lord." On the antiphon:
"one day, an everlasting day, to which no yesterday yields, which no tomorrow
presses" — `unum diem, diem sempiternum, cui non cedit hesternus, quem non urget
crastinus`. **A material limit, unchanged:** Augustine's §15 expounds the rest
of v. 11, the clause the Introit cuts off. **The Father's unit and the
liturgy's unit do not coincide.**

**Cassiodorus expounds the same verse in terms very close to Augustine's, and
he is corroboration and not a second witness** [PAT-207]. `quia semper aeterna
est, quae solis adventu non oritur, nec eius finitur occasu; quam non sequitur
crastina, nec praecedit hesterna`. **State the dependence rather than counting
two witnesses**; the wording is close enough that he is almost certainly
working from Augustine here, and a guide presenting them as two independent
readings will have inflated the evidence. **His own contributions are two**: the
gloss on `super millia` as "this world, where thousands of days come to an
end", and the naming of the comparative figure as *parison*. He also expounds
v. 11 together with v. 12, exactly as Augustine does, so the same limit applies.

**On `respice in faciem Christi tui` there are now three readings, not two, and
the third is Greek** [PAT-206, PAT-301].

- **Augustine** turns the petition outward and missionary: `Fac innotescere
  omnibus Christum tuum` (prior run, restated).
- **Cassiodorus** refuses the obvious reading exactly as Augustine does, turns
  it outward to the gentiles, **and names the figure**: `Haec figura dicitur
  hypallage, Latine permutatio, quoties dicitur respici magis ille qui
  respicit` [PAT-206]. He gives two psalm parallels, Ps. 13:2 and Ps. 5:2.
- **Theodoret**, read in Greek, gives a third: **the face of Christ is the
  saved people**, because the Apostle calls them the body of Christ — `Τοῦτον
  γὰρ ἐπεκάλεσε πρόσωπον τοῦ Χριστοῦ`, citing 1 Cor. 12:27 with 12:21
  [PAT-301].

**Consequence the author must carry:** the third reading is nearer Guéranger's
ecclesial direction than Augustine's, but rests on a different Pauline text and
carries no nuptial figure, so it corroborates neither. **It removes the ground
for treating the inward-ecclesial reading as a nineteenth-century departure
from the Fathers** [PAT-301]. Preserve all four positions (§6.4).

**On the antiphon Theodoret differs from both Latins about what the one day
is** [PAT-302]. Augustine and Cassiodorus read the one eternal day that has no
rising or setting; Theodoret reads an argument from profit — what one may reap
in a single day in the courts he could not gather elsewhere though he spent
thousands of days — and anchors the psalm historically in the Babylonian
captives. **This is the Antiochene historical method against the Latin
spiritual reading, on the same words, and both are now checkable in their own
languages.**

**Cassiodorus comments directly on the clause the Introit's psalm verse cuts
off** [PAT-208]: distinguishing `cor` as the understanding from `caro`, and
marvelling that not the soul only but the flesh broke out into heavenly
gladness. **This turns a cross-element observation a lane made for itself into
one a Father makes** — but the clause is not in the appointed Introit, and any
use must say that the missal cuts before it.

**A retrieval trap specific to this Introit, carried forward** (prior run,
restated; its lane finding is the prior run's PRE-024). `Protector noster aspice,
Deus` opens this
Mass's Introit, the Fifth Sunday's Gradual (adapted, with `super servos tuos`),
and a composed collect that quotes no psalm at all. **An incipit-driven search
for reception of the Introit returns material on a different chant of a
different Sunday**, and the third case is precisely what the profile warns
about at page 2. The cross-proper control is independently reproduced this run:
`christi tui` in appointed Latin occurs in **this formulary alone** across the
21 collated records, the one other hit being audit prose recording the Fifth
Sunday's substitution [THE-035].

### 2.2 Epistle — Gal. 5:16–24

**The pericope's two boundaries** [SCR-007]. It begins by **replacing** Paul's
own connective: Clementine Gal. 5:16 reads `Dico autem: Spiritu ambulate`; the
appointed Epistle reads `Fratres: Spiritu ambulate`. `Dico autem` ties v. 16
back to the liberty of v. 13 — where Paul's own vocative `fratres` stands,
inside the sentence the pericope drops — and to the law fulfilled in love at
v. 14. And it ends two verses before the unit's own closing inclusio: v. 25's
`Si Spiritu vivimus, Spiritu et ambulemus` returns v. 16's verb in the
hortatory subjunctive. **In Greek the two verbs differ** (περιπατεῖτε at v. 16,
στοιχῶμεν at v. 25), so **the inclusio is a property of the Vulgate's rendering
and not of the Greek**, and any claim that the lesson stops short of Paul's own
closing echo is a claim about the Latin the missal prints. The leaf's own
`propers/verified.md` independently records that Gal. 5:25 is the incipit of
the **following** Sunday's lesson, so the cut is a boundary between two Sundays
and not simply an omission [SCR-007].

**Augustine's connective is one verse further back still** [PAT-107]: he reads
`Spiritu ambulate` as the answer to the biting and devouring of v. 15, which
the pericope also cuts, and names humility and meekness as the first and great
gift of the Spirit — `Primum enim et magnum munus est spiritus, humilitas et
mansuetudo`. **`Mansuetudo` is in the appointed fruit list, so this is a link
the appointed text can carry.**

**The list lengths, the mechanism, and the four Fathers' own lemmata.** See
§0.3(a) for the adjudication; the evidence is:

- *Appointed Latin*: seventeen vices, twelve fruits, counted item by item
  [SCR-008].
- *Byzantine Greek*: seventeen vices, nine fruits. *Critical text*, through the
  `{NA}` braces: fifteen and nine [SCR-008].
- *Augustine's own Latin lemma*: **thirteen** vices and **nine** fruits, with
  `animositates` for the missal's `irae` and `haereses` for `sectae`, and
  `regnum Dei non possidebunt` where the missal prints `non consequentur`
  [PAT-101].
- *Jerome's own Latin lemma*: **fifteen** vices — and he rules explicitly that
  no more than fifteen are named, recording `adulterium`, `impudicitia` and
  `homicidia` as additions found *in Latinis codicibus*: `Sed sciendum non plus
  quam quindecim carnis opera nominata` [PAT-151]. **The 1962 Epistle prints
  two of the three he rejects, in a list of seventeen.** He numbers the items
  through his exposition (*septimum locum contentio*, *octava aemulatio*,
  *quartumdecimum ebrietas*, *quintadecima commessatio*), so the count is his
  and not a modern tally. His fruit lemma is Augustine's nine, in the same
  order [PAT-152].
- *Chrysostom's Greek lemma*: nine fruits in exactly that order, and seventeen
  vices including both μοιχεία and φόνοι [PAT-312].

**Bound on Jerome's ruling, and it must travel:** this is Jerome on the Latin
codices he knew about 386–388, **not** a judgement about the Clementine's
descent, and no claim is made about how the 1962 text got its seventeen
[PAT-151]. **One complication is preserved rather than smoothed:** the long
Origen extract Jerome translates at Gal. 5:13 runs through a sequence naming
`patientia`, `fides`, `temperantia`, `continentia` and `castitas`, which looks
like the twelve-fruit series, yet Jerome's own lemma has nine [PAT-152]. **What
that means for the transmission is not established here.**

**Jerome comments on the missal's own word `vitiis`** [PAT-154]: `Ubi Latinus
interpres vitia posuit, in Graeco pathemata, id est, passiones leguntur`, and
he explains why the Apostle added `desideria` — so as not to seem to deny the
nature of the body in spiritual men, but its vices. **His reasoning defends the
appointed word rather than correcting it**, and it also explains Augustine's
divergent lemma `passionibus` [PAT-106]: the two Latin forms are two renderings
of one Greek noun, not two different texts. Chrysostom's Greek independently
confirms both the παθήμασι behind `vitiis` and the missal's `Qui autem sunt
Christi` against Augustine's `Qui sunt in Christo Iesu`, so **on this clause
the appointed Latin is the better witness to Paul** [PAT-315].

**Jerome's philology of the vice-list is Greek-anchored and checkable**
[PAT-159]: `aemulatio` = ζῆλος; `rixae` renders ἐριθεία and not μάχη;
`haeresis` from ἑλέσθαι, choosing; and the distinction between `iracundus`
(always angry) and `iratus` (roused for a time). **Where a guide needs a
definition of one of the appointed vices this is the better source** than the
moralising medieval etymologies, several of which are fanciful. Cyprian's *De
zelo et livore*, which Jerome names, was not opened and remains a lead.

**Jerome distinguishes `modestia` from `continentia`** — `modestia` belonging
to the perfect, `continentia` to those still on the way whose desires are not
yet stilled [PAT-160]. **This is not the medieval pair.** The prior run
recorded that Anthony and Aquinas independently share a definition of
`continentia`/`castitas` attributed to the Gloss; **Jerome's pairing is
`modestia`/`continentia` and is a different distinction, not that pair's
source.** Recorded so a later worker does not collapse the two.

**Four accounts of the two lists' asymmetry, and the later worker must not
flatten them.** This is the run's richest single vein [PAT-313].

1. **The prior run's THE-020, a textual reading restated here**: the vice list is left
   open (`et his similia`) and the fruit list closed with a verdict (`Adversus
   huiusmodi non est lex`).
2. **Augustine refuses the argument from the counts altogether** [PAT-102]:
   `Non enim hoc suscepit, ut doceret, quot sint, sed in quo genere` — and he
   reads **both** lists as open, grounding it on the missal's own word:
   `Non enim ait: Adversus haec non est lex, sed: Adversus huiusmodi`.
   **This points the opposite way from (1) and both must stand.**
3. **Origen, transmitted verbatim by Jerome** [PAT-156]: the works of the flesh
   are called *manifest* and the fruit of the Spirit is not, so the fruit must
   be sought with labour. Origen reaches this brief **only through Jerome** and
   is a checked report of an unchecked source; **and Jerome himself partly
   withdraws from the reading he transmits**, saying at 5:19–21 that on
   reflection the named vices seem to him to belong to the plain sense.
4. **Chrysostom's reason** [PAT-313]: evil works come from us alone, so Paul
   calls them works; the good things need not our care only but God's kindness,
   so he calls them fruit. **Jerome's reason is different again** — vices end in
   themselves and perish, virtues sprout and overflow — so the Greek reason is
   about grace and the Latin about fecundity.

**Augustine's systematic opposition of the two lists, and why it cannot be
mapped onto the missal** [PAT-103]. He works the lists into a point-for-point
opposition (`Recte igitur fornicationi opponitur caritas`) and distinguishes
`aemulatio` from `invidia` by what each grieves at. **It is built on his own
thirteen-vice and nine-fruit lemma and cannot be mapped onto the missal's
seventeen and twelve without distortion. Reporting the pairing as a reading of
the appointed lists would be an error.** It is nevertheless the only patristic
attempt located to read the two lists as answering each other, and it is a
different scheme from Aquinas's ordering of the fruits by what each perfects.

**On v. 17, two Fathers deny that the verse removes free choice, by two
different routes, and the difference must be preserved** [PAT-104, PAT-157].
Augustine answers that the verse is addressed to those who will not hold the
grace of faith, and reads the passage through his four-stage scheme — before
the law, under the law, under grace, in eternal peace. **The argument is
anti-Pelagian in shape and draws on Rom. 5–8, none of which is in the appointed
extract.** Jerome answers by a tripartite anthropology: the soul stands in the
middle between flesh and spirit with good and evil in its own power, and what
is done is credited to whichever of the two it joins, with the analogy
`caro=terra, anima=aurum, spiritus=ignis`. **Same objection, two different
middle terms, and they yield different accounts of what the appointed verse
describes. Chrysostom raises the same difficulty in Greek and answers it as
Jerome does** — the soul lies between vice and virtue and makes the body
spiritual or earthly by what it does with it [PAT-314]. **That is a genuine
Greek–Latin convergence, and one the appointed pericope invites, because the
lesson names only `caro` and `spiritus` and leaves the soul unmentioned.
Nothing shows dependence in either direction; report the agreement as
agreement.**

**On v. 16 Augustine makes the argument turn on the mood of the verb**
[PAT-105]: Paul said not that you shall not *have* the desires of the flesh but
that you shall not *fulfil* them, `Quippe non eas omnino habere, non iam
certamen sed certaminis praemium est`. **Two textual bounds:** his lemma reads
`concupiscentias carnis ne perfeceritis` where the missal prints `desideria
carnis non perficietis`, and his v. 18 reads `non ADHUC estis sub lege`.
**The argument survives into the missal's wording, because `perficietis` is
still about fulfilling and not about having; say so rather than quoting his
lemma as the Epistle's.**

**On v. 18 Jerome tells a Latin reader that the appointed Latin
under-determines a distinction the Greek makes** [PAT-158]: `spiritus` here
stands without the article and without an addition, so it is the Holy Spirit
and not the human spirit — `quae quidem minutiae magis in Graeco, quam in
nostra lingua observatae (qui arthra penitus non habemus)`. **A related
editorial fact must be kept separate and not put in his mouth:** the 1962
typical edition prints lower-case `spiritu` at v. 18 and capital `Spiritus` at
v. 22, which is the printers' choice making visible what Jerome says the
language cannot.

**On v. 24, the verse the lesson ends on** — and a witness that reads it as its
own climax is worth more to this guide than one that runs on to v. 25.
Augustine grounds the crucifixion of the flesh in **chaste fear**, contrasting
the fear of the adulteress with the fear of the chaste wife, and reads it
through Ps. 118:120 (`Confige clavis a timore tuo carnes meas`) and the taking
up of the cross [PAT-106]. **Chrysostom, in Greek, insists the crucifixion is
not the destruction of the flesh** — `Οὐ γὰρ δὴ τὴν σάρκα ἀνεῖλον· ἐπεὶ πῶς
ἔμελλον ζῆν;` — and reads it as exact discipline, ἀκριβὴς φιλοσοφία
[PAT-315]. **That bears directly on cross-proper claim C2.**

**A documented ancient disagreement about how to divide the last clause**
[PAT-155]. Jerome records Origen construing v. 24 with v. 23 and taking
`Christi` with `carnem` — that those against whom there is no law crucified the
flesh **of Christ** — and declines it in favour of the *Vulgata editio*: `ut
non carnem Christi, sed suam eos crucifixisse dicamus`. **This is a divided
reading of the very clause the appointed lesson ends on, with Jerome naming the
reading he follows.** Origen reaches this brief only through Jerome; the Greek
behind it was not opened and **no claim about Origen's own text may be
published from this alone.**

**On the clause the fruit list closes with, two Latin Fathers converge on one
proof-text** [PAT-108, PAT-161]. Both Augustine and Jerome expound `Adversus
huiusmodi non est lex` from 1 Tim. 1:8–10, that the law is not laid down for
the just. **Convergence, not dependence: nothing shows either drawing on the
other, and no transmission was traced.** It is nevertheless the firmest
reception the sweep found for that clause, and **the one place where two Latin
Fathers reach the appointed wording with the same argument.**

**Chrysostom's two sentences the prior brief leaned on are confirmed at the
Greek, and one is confirmed with a correction** [PAT-311]. `Οὐκ εἶπε, τὸ ἔργον
τοῦ πνεύματος, ἀλλ', Ὁ καρπός` is verbatim NPNF's "He says not, the work of the
Spirit, but, the fruit". But "by the flesh, he does not mean the body" is a
**paraphrase**: the Greek reads `Ὁρᾷς ὅτι οὔ φησι τὴν σάρκα ἐνταῦθα, ἀλλὰ τὸν
γεώδη λογισμὸν καὶ χαμαὶ συρόμενον` — the object is σάρξ and the contrast term
is λογισμός, an earthly cast of mind, not σῶμα. **A guide quoting NPNF's
wording is not misrepresenting the sense, but the Greek makes a sharper claim
about the word the Epistle actually uses, and a guide arguing from the
appointed `caro` should prefer it. Present the English as NPNF's** (§11.2).

**Aquinas and Anthony of Padua** (prior run, restated) remain the only
witnesses expounding the missal's own twelve-item list, and §0.3(a) is why that
matters. Aquinas orders the twelve by what each perfects and reads the number
as answering Apoc. 22:2 — **his own move, to be attributed to him**; he groups
the seventeen vices by object, derives `veneficia` from `venenum`, and answers
the objection Chrysostom raises by a **different route**, Augustine's *De civ.
Dei* XIV.2 that whoever lives according to himself lives according to the
flesh. **Preserve the difference; do not report a single patristic-scholastic
consensus.** *De civ. Dei* XIV.2 was again not opened this run and remains a
lead [PAT-402].

**Anthony of Padua's gloss of `idolorum servitus` as avarice has plain
scriptural warrant, which is new this run** [SCR-027]. The formula stands in
exactly three verses of the Vulgate, and **in both of the other two it glosses
avarice rather than the cult of images**: Eph. 5:5 predicates it of `avarus`,
Col. 3:5 of `avaritiam`, and both also share the appointed Epistle's first two
vices in order. **What this does not say:** that Anthony drew it from either.
No such dependence was checked, and establishing it would require reading his
sermon for that purpose. **The observation is recorded only so that the gloss
is not reported as arbitrary.**

**The canonical context of the Epistle's exclusion formula, bounded** [SCR-028].
`Regnum Dei non consequentur` belongs to a small closed set of Pauline
parallels: 1 Cor. 6:9–10 (a vice list closed by the same exclusion, sharing
`fornicarii`, `idolis servientes` and `ebriosi`, and a **registered and
verified** source-library record), Eph. 5:5, and 1 Cor. 15:50, which joins
`caro` and `regnum Dei` in one clause. **Two consequences.** The Epistle's
`regnum Dei` is the only kingdom-word in Galatians [SCR-005] but is **not** an
isolated Pauline usage, and a guide should not present it as though Paul
reached for the phrase once and nowhere else. And 1 Cor. 15:50 is the nearest
Pauline analogue to the appointed Epistle's own move, which bears on C2.
**None of the three is appointed and nothing in the ten elements points to
them; their standing is as the canonical context of the appointed wording.**

**The defeater that must be disclosed wherever Epistle and Gospel are joined**
[THE-049, which carries and generalises the prior run's THE-031]. The library's sole registered treatment of
Gal. 5:16–24 is Anthony's sermon, and his Sunday numbering runs one ahead of
the 1962 missal's, consistently across all three registered Anthony sermons:
his Introit is `Inclina, Domine` and his Gospel is Luke 17:11–19. **A major
medieval preacher expounding this Epistle does so beside a different Gospel and
a different Introit.** So every cross-element candidate joining the Epistle to
another element is a claim about how the 1962 formulary reads when taken whole,
and **not** a claim about how the tradition read those texts together. **The
defeater is now generalised to the Introit as well as the Gospel** [THE-049],
and it attaches to C1, C2, C6 and to P1, P6 and the material at §2.2 above.
Every prose use must carry it.

### 2.3 Gradual — Ps. 117:8–9

**A negative worth recording, and something positive now stands beside it**
[SCR-013, PAT-213]. Unlike the Introit and the Offertory the Gradual takes two
complete verses and cuts nothing, so there is no omission to report. What can
be said positively instead is Cassiodorus's: **the two appointed verses are
governed by anaphora**, the same words doubled at the head of each — `Et nota
quod in principiis amborum versuum eadem verba geminavit. Quae figura dicitur
anaphora`. **Exactly on the appointed wording.**

**Context** [SCR-013]. vv. 6–7 twice call the Lord `adjutor` and name `homo` as
what need not be feared, so v. 8's `quam confidere in homine` generalises a
contrast the psalm has just made concrete; v. 1's `quoniam bonus` supplies the
adjective the Gradual's `Bonum est` turns into a comparative formula. The
tracked Clementine prints `Alleluja.` at the head of v. 1 — a liturgical
rubric-word and not a counted superscription, which is why the Vulgate,
Masoretic and English numbers agree here. **Theodoret's psalm heading is
Ἀλληλούϊα, a small independent convergence** [PAT-306].

**The verse two before the Gradual is quoted verbatim in the New Testament, and
that is a fact about Hebrews and not a relation the formulary makes**
[SCR-025]. Ps. 117:6 stands word for word at Heb. 13:6, and a whole-Bible
search on `dominus mihi adiutor` returns exactly Ps. 117:6, 117:7 and Heb. 13:6.
The Gradual's `homine` is the `homo` of v. 6 and its `confidere` answers
Hebrews' framing adverb `confidenter`. **The same bound SCR-018 applies to
Mt. 21 applies here: the Gradual does not appoint v. 6.** Heb. 13:5's warning
against avarice and exhortation to contentment is thematically close to this
Mass's Gospel; **that is flagged as inference and an author must not present it
as a connection the liturgy draws.**

**Three witnesses now expound the two verses, and they divide three ways about
what the princes are.** This is the strongest Greek–Latin comparison the sweep
can support [PAT-305].

- **Augustine** escalates the excluded second term progressively — bad men,
  good men, **good angels** — and still it loses: "For angels also are called
  princes, even as we read in Daniel, Michael, your prince" (prior run,
  restated).
- **Cassiodorus** frames the two verses as **carnal against spiritual** rather
  than as a moral climb, and lets `princeps` cover **both the devil and the
  good angel** — `Princeps enim et diabolus appellatur … Sic et bonus angelus
  dictus est princeps, sicut in Daniele legitur` [PAT-211]. **Both reach
  Michael in Daniel, so the shared proof-text is probably dependence and not
  independent invention; say so.**
- **Theodoret**, in Greek, has ἄρχοντες who are **earthly rulers whose
  authority is temporary**, grounding the comparison in will, power and
  duration: God is good, wills the good, can do what he wills and has
  imperishable authority, while men are corruptible by nature and changeable in
  purpose [PAT-305]. His preface makes them the persecuting rulers, demagogues,
  kings and generals whom the gentile believers outlasted [PAT-306].

**Cassiodorus also gives the Gradual a doctrinal content it otherwise lacks in
this sweep** [PAT-212]: he reads the first verse against presumption of the
will, citing Jas. 4:13–15, Phil. 2:13 and Jer. 17:5, and names Augustine's books
against Pelagius, Caelestius and Julian as what settles the point. **That
converges with the anti-Pelagian shape of Augustine's reading of the appointed
Epistle at Gal. 5:17** [PAT-104] — **but the convergence is between two
elements as read by the tradition, not something either text asserts, and a
guide joining them owes the reader that distinction.** Cassiodorus's reference
to the anti-Pelagian works is a pointer and not a checked locus.

**A textual point still open** [PAT-213]. The prior run observed a modern
transcription of Augustine reading the accusative `sperare in Dominum … in
principes` where the missal prints the ablative, and flagged it as unresolved
without PL 37. **PL 37 was again not opened.** Cassiodorus's lemma reads the
ablative, agreeing with the missal, which is **one data point against the
accusative variant but does not settle it.**

*A cross-relation flagged as a lead and not as any Father's claim:* the
escalation to good angels makes the Gradual's exclusion absolute rather than
moral, which is the Gospel's own logic at `Nemo potest duobus dominis servire`.
**Augustine does not cite Mt. 6:24 there.**

### 2.4 Alleluia — Ps. 94:1

**The element the prior brief called the formulary's thinnest is no longer
thin.** It now carries two Latin witnesses and one Greek, read in Greek, and
they disagree productively about its one distinctive word.

**Augustine takes `Venite` as the load-bearing word and denies it means
motion** (prior run, restated): "It is not by place, but by being unlike Him,
that a man is afar from God." **Cassiodorus makes the same move by a different
proof-text** [PAT-209]: `Venite enim illis dicitur, qui longe positi sentiuntur
… tamen longinqui efficimur, cum actuum nostrorum qualitatibus submovemur`,
grounding it on Is. 29:13 where Augustine argues from likeness and unlikeness.
**Cassiodorus likewise specifies `exsultemus` with `Domino` precisely to
exclude a worldly exultation** — `quoniam est et saeculi istius exsultatio, quae
maxime animos occupat infideles, addidit, Domino` — which is Augustine's second
move reached independently. **Two Latin witnesses now make both of the moves
the prior brief had from Augustine alone.**

**The Latin recovers a play the translation loses** (prior run, restated):
Augustine closes on a jingle built from the appointed verb — `Pie debes Domino
exsultare, si vis securus mundo insultare` — which NPNF renders "piously joy in
the Lord, if you dost wish safely to trample upon the world", and the play
vanishes. **The play depends on the missal's own word `exsultemus`.**

**The two accounts of `iubilare`, and they disagree** [PAT-210, PAT-303].
Cassiodorus gives the classical Latin account of the *jubilus*, standing
directly on the appointed word: `Jubilare saepe diximus magnum motum esse
laetitiae, qui quamvis verbis nequeat explicari, tamen amplissima voce
declaratur, intus esse designans gaudium cui sermo non sufficit`. Theodoret,
in Greek, reads ἀλαλάξωμεν as **the shout of victors** and the psalm as an
**epinician hymn**: `Ὁ γὰρ ἀλαλαγμὸς νικώντων ἐστὶ φωνή`. **Preserve the
disagreement: it is the most interesting thing the sweep found about this
element.** Note that the appointed Latin is `iubilemus`, which renders
ἀλαλάξωμεν, so **Theodoret's argument is about the word the missal translates
and not about the missal's word** [PAT-303].

**Cassiodorus glosses `salutari`** as the Lord Saviour, who by dying granted
salvation, by suffering gave an example, and by rising bestowed saving gifts
[PAT-210] — which bears on the one word the Alleluia shares with the rest of
the formulary.

**Theodoret sets the psalm in a named historical situation** [PAT-304]: it is
composed in the person of King Josiah and the priests, foreseeing his reform,
with Huldah the prophetess; and he reports that the psalm is **untitled among
the Hebrews**. **Bounded:** no Latin witness in this sweep offers any historical
setting for Ps. 94 at all, and Theodoret's is his own reconstruction from
4 Kgs 22–23, not something the psalm states. His remark about the title bears on
the numbering evidence at §1.3 and is offered as a reception fact; **the textual
conclusion is not the reception lane's to draw.**

**The canonical resonance of the appointed verse, new this run and outside the
formulary** [SCR-029]. `Deo salutari` stands in exactly four verses of the
Vulgate — Deut. 32:15, Ps. 23:5, Ps. 94:1 and **Lk. 1:47**, the Magnificat,
which shares the Alleluia's `exsult-` verb as well as its noun; widening to
`salutari (meo|nostro|tuo)` reaches 1 Kings (=1 Samuel) 2:1, the Canticle of
Anna, pairing the same verb with the same noun. **This stands alongside, and
does not contradict, the structural fact below:** the one is a claim about ties
*within* the ten elements, the other about the appointed verse's canonical
resonance *outside* them. **Both should be carried, because a guide told only
the first may conclude the Alleluia is a thin text, which its vocabulary does
not support.** *Flagged:* whether Lk. 1:47 echoes Ps. 94:1, 1 Sam. 2:1 or a
common Septuagintal idiom **is not settled and cannot be here** — no Greek
psalter is held, so the shared Greek behind the shared Latin could not be
checked.

**A material limit on the reception, unchanged** (prior run, restated). This
*enarratio*'s centre of gravity is vv. 7–11, `Hodie si vocem eius audieritis`,
which the Alleluia does not appoint. **A guide taking Augustine on this psalm
must not import that ending into a chant that stops at v. 1.** The same limit
governs the canonical relationship at [SCR-014]: Hebrews quotes Ps. 94:8–11 at
3:7–11, repeats it at 3:15 and expounds it through 4:1–11, and the tracked
Vulgate's psalter and its Hebrews **disagree at three words and divide the
forty years differently** — `in irritatione` against `in exacerbatione`,
`offensus fui generationi illi` against `infensus fui generationi huic`, `ut
iuravi` against `sicut iuravi`; and Ps. 94:9–10 attach `Quadraginta annis` to
the offence where Heb. 3:9–10 attach it to the seeing. **Every one of those
verses lies past the single verse the Alleluia appoints**, and that the
Alleluia's one verse carries the whole psalm's warning of exclusion from rest
**is an inference, not something the appointed text states** [SCR-014].

**The structural fact that constrains synthesis, confirmed and now bounded at
both ends** (the prior run's THE-030, restated within [SCR-029] and [SCR-030], with [SCR-022]). The Alleluia is the least
lexically integrated element of the formulary: `exsult-` and `iubil-` occur
nowhere else in the ten elements, and its only substantive tie is `salutari`.
**The count now names the other end of that tie: it is to three *composed
orations* and to no other chant or lesson**, because `salut-`/`salv-` stands
exactly four times in the formulary, once each in Collect, Alleluia, Secret and
Postcommunion [SCR-030]. **The joy of the Alleluia remains a natural thing for
a synthesis to reach for as the resolution of the Gospel's anxiety, and the
appointed texts still do not supply the lexical warrant**: the Epistle's
`gaudium` and the Alleluia's `exsultemus` are different roots in different
elements with nothing joining them, and **Cassiodorus says nothing about the
Epistle** [PAT-210]. A writer wanting the Alleluia in a joy-resolves-anxiety
argument must build it as an exploratory proposal.

### 2.5 Gospel — Mt. 6:24–33

**The pericope is cut out of a continuous argument at both ends** [SCR-009]. It
begins bare at v. 24 with no connective, immediately after the treasure and eye
sayings, and stops at v. 33 without v. 34. `Sollicit-` stands in exactly four
verses of Matthew 6 (25, 28, 31, 34, the last twice) and the pericope carries
three, **ending on the promise of v. 33 rather than on the restriction to
today**. That this lets the Communion take the Gospel's last verse as its own
antiphon is a further textual fact; **what the compiler meant by the boundary is
not established by anything in any lane.**

**The pericope contains the second member of a repetition internal to Matthew 6
and not the first** [SCR-010]. `Scit enim Pater vester` stands in **exactly two
verses of the whole Vulgate** — Mt. 6:8 and Mt. 6:32 — and the Lord's Prayer,
asking for the kingdom's coming and for bread, stands between them. **Only the
second falls inside the appointed pericope. Flagged as inference:** any claim
that the pericope is meant to be heard against the Our Father is a lane's
inference, not the text's assertion.

**Both sayings have Lucan parallels in different settings, and Luke orders the
material the other way round** [SCR-011]. Luke places the two-masters saying at
16:13 after the unjust steward and adds `servus`; the two Latin texts differ in
**three** words and not only the one usually noticed — Luke adds `servus`, reads
`odiet` for Matthew's periphrastic `odio habebit`, and `uni adhaerebit` for
Matthew's `unum sustinebit`. **That third difference matters here**, because the
strongest patristic move on this Gospel is an argument about which of two verbs
the text uses: the Lucan parallel shows the verb pair is not fixed across the
two Latin Gospels — **a fact about the texts and not an objection to Augustine,
who is commenting on Matthew.** `Mammon-` stands in exactly four verses of the
whole Vulgate: Mt. 6:24, Lk. 16:9, 16:11, 16:13.

**Augustine reads v. 24's asymmetry as deliberate** (prior run, restated):
Christ says of the second master `contemnet` and not `odio habebit`, because
almost no one's conscience can hate God. **Aquinas fastens on the other member
of the same four-verb figure and explains it from the same asymmetry**
[PAT-131]: `Et non dicit, diliget, quia Diabolus naturaliter diligi non potest.
Deus naturaliter diligitur; Diabolus vero sustinetur.` **The two observations
are complementary and both are checkable against the appointed Latin, which
prints all four verbs.**

**Aquinas reads the whole saying as a claim about ultimate ends** [PAT-131]:
`impossibile est quod animus feratur ad duos fines simul et semel`, and
`Omne autem in quo quis ponit finem suum, Deus suus est`, citing Phil. 3:19.

**Two Fathers give different etymologies of `mammonae`, and the guide should
give both** [PAT-122]. Jerome: `Mammona sermone Syriaco divitiae nuncupantur`.
Augustine: Punic for gain (prior run, restated). **Neither was checked against
a Semitic authority here; the finding is that two Fathers disagree, not that
one is right** — and the prior brief's flag that Augustine's remark rests on no
Semitic authority now has a documented rival from the Father who knew the
eastern languages best.

**Jerome draws the distinction on which any non-ascetical reading depends**
[PAT-123]: `non dixit, qui habet divitias, sed qui servit divitiis. Qui enim
divitiarum servus est, divitias custodit, ut servus; qui autem servitutis
excussit iugum, distribuit eas, ut dominus.` **Aquinas repeats the same
distinction in almost the same words** — `aliud est habere divitias ut dominus,
aliud ut servus`. **This is documented reception for what the prior brief could
hold only as an exploratory proposal** (P1, that goods are ordered and not
refused): it now rests on a Father reading the appointed verb `servire` and on
a Doctor agreeing. **Whether Aquinas draws on Jerome was not traced; report the
agreement, not the dependence.**

**The allegory question: the Latin tradition is namedly divided.** See §0.3(c)
for the adjudication. The evidence is [PAT-141]:

- **Hilary** argues the literal sense does not cohere — `Quae consequuntur, non
  satis propositionibus congruunt. Numquid et unius domini servus non possit
  circa vestem esse cibumque sollicitus?` — and reads the whole pericope as
  doctrine about the **resurrection of the body**, on the ground that the sense
  of unbelievers is corrupted about what the risen body and its food will be
  [PAT-111]. His allegory is specific and complete across the appointed verses:
  **birds = the unclean spirits**; **the cubit = the resurrection body raised to
  the measure of the perfect man** (Eph. 4:13); **lilies = the brightness of the
  angels**, with men made like angels in the resurrection; **hay burnt tomorrow
  = the gentiles**, who are raised to eternal fire [PAT-112].
- **Jerome** expressly rebuts allegorising the birds, naming those who read them
  as angels and ministering powers, and refutes them from the logic of the
  *a fortiori* itself — `Si hoc ita est, ut intelligi volunt, quomodo sequitur
  dictum ad homines: Nonne vos magis pluris estis illis? Simpliciter ergo
  accipiendum` [PAT-121]. **This is a better ground than Augustine's for the
  guide's purpose, because it is internal to the appointed verse.**
- **Augustine** forbids allegorising these examples (prior run, restated, and
  independently reproduced in the Catena this run) [PAT-141].
- **Remigius**, birds and lilies as holy men, reaches this brief **only through
  the Catena and remains a lead** [PAT-141].

**Two qualifications on Hilary that must not be dropped** [PAT-112]: the
hay-as-gentiles reading ends in a doctrine of the bodily eternity of the damned
that no other witness states, and the birds-as-unclean-spirits reading is the
one place where his allegory works **against** the pericope's consoling sense.
**Report the reading, and do not use it to soften the doctrine it carries.**

**Jerome's own comment on the lilies is aesthetic and not allegorical**
[PAT-126] — `quod sericum, quae regum purpura, quae pictura textricum potest
floribus comparari?` — consistent with his refusal at v. 26 and **inconsistent
with the reading later ascribed to him** (below).

**A concrete misattribution trap, new this run** [PAT-133]. **Aquinas's *Super
Matthaeum* ascribes the lilies-as-angels reading to Jerome; the reading is
Hilary's**, and the *Catena aurea*, Thomas's own compilation, attributes it
correctly to `Hilarius in Matth.` **A writer taking the sentence from *Super
Matthaeum* will attribute to Jerome a reading Jerome's own commentary argues
against in kind.** *Super Matthaeum* cap. 6 lect. 5 is a *reportatio* and the
slip is most likely the reporter's; **report it as a misattribution in that
text, not as an error of Thomas.**

**Chrysostom reads the illustrations as rhetorically engineered** (prior run,
restated), the lilies progressively degraded — lilies, grass of the field,
which is today, cast into the **oven**. **Hilary's Latin lemma lacks the last
step** [PAT-113]: he reads `cras in ignem mittitur` where the missal prints
`cras in clibanum mittitur`, and also `non serunt, neque congregant in horrea`
without `neque metunt`. **So the step Chrysostom's rhetoric turns on is not in
every ancient Latin witness**, and the medieval Gloss knows the variant and
says so: `Alii libri habent in ignem, vel in acervum, qui habet speciem
clibani`. Textual observation about two witnesses; **no claim is made about
which reading is prior.**

**A lexical field that pulls against the plain sense, and three cautions with
it** [SCR-031]. `Clibanum` stands in exactly four Vulgate verses: Mt. 6:30,
Lk. 12:28, and, in the Old Testament, Os. 7:6 and Ps. 20:10, **in both of which
it is an image of judicial wrath**. And the grass-and-glory topos of Is. 40:6–8
sets `omnis gloria eius` against `foenum` and `flos agri` in a clause whose
subject is `omnis caro` — **the Epistle's governing term**. **The cautions are
the reason this is recorded at all:** (1) the Gospel's `clibanum` is plainly
domestic and the wrath-resonance is a fact about the word's distribution and
not about Matthew's sense; (2) Isaiah 40 is not appointed and nothing in the
ten elements points to it, so the convergence is a fact about Isaiah exactly as
the Mt. 21 convergence is a fact about Matthew 21; (3) **the principal Latin
Father on this pericope has ruled against the move these distributions most
invite.** The narrative background to Mt. 6:29 was read: 3 Kings 10:4–7 with
2 Par. 9:3–6, the queen of Saba overcome by Solomon's house, table, servants'
`vestes` and offerings.

**Jerome states the limit against over-reading in one sentence anchored inside
the appointed bounds** [PAT-124]: `labor exercendus est, sollicitudo tollenda`
(ad v. 25), with `De praesentibus ergo concessit debere esse sollicitos qui
futura prohibet cogitare` at vv. 31ff. **This is the better citation on both
counts and supersedes the prior brief's advice.** The prior brief preferred
Chrysostom's sentence because Augustine's material there is anchored partly in
v. 34, which the lesson excludes, and Chrysostom was available in English only.
**Jerome's formulation is anchored at vv. 25 and 31, both inside the lesson,
and is available in Latin** — and it makes a **third** independent Father
setting the same limit.

**Jerome records a variant the missal does not print** [PAT-125]: `In
nonnullis codicibus additum est neque quid bibatis` at v. 25. The missal's
shorter form is the one Jerome treats as his own. **Do not turn this into a
claim of descent:** the missal's reading is not shown to come from his, only to
agree with it against a variant he records.

**On the cubit, Aquinas argues that growth is not from ourselves but from God,
and that the verse is an experimental proof of the providence already argued
from the birds** [PAT-134]: `augmentum non est nobis ex nobis, sed ex Deo: unde
de providentia Dei non debetis desperare`. **This is documented reception for
what the prior brief held as the interpretive proposal P2**, and §9.2 reconciles
the two rather than leaving both standing.

**Hilary reads the pericope as ending in a command to seek the kingdom, and
grounds `Haec enim omnia gentes inquirunt` in unbelief rather than appetite**
[PAT-136]: `regnumque Dei vitae nostrae stipendiis quaeramus`; `Gentium igitur
est, infidelitatis istius cura angi`. **This is the one place where his
resurrection reading and the plain sense converge.** His exposition runs on to
v. 34, which the lesson excludes.

**A documented *controversial* reception, and a medieval identification that
does not close its lead** (prior run, restated; [PAT-132]). Augustine wrote *De
opere monachorum* against monks who quoted these verses to argue they need not
work. **Aquinas independently names the sect in his own Matthew lectures** —
`destruit hic error Euticharum, qui dicebant quod viri apostolici non debebant
laborare`, answered from 2 Thess. 3:10. **This does not close the lead:** it
shows only that the medieval tradition makes the same identification.
*De haeresibus* is still unopened, and **no claim that Augustine names the
Euchites may be published as checked.** `Euticharum` is the Turin text's
spelling and should be reproduced as printed.

**The Catena aurea is now a checked map for two of its authorities and a
lead-map for the rest** [PAT-140]. **Every Hilarius and Hieronymus excerpt on
the appointed Gospel was checked sentence by sentence against the
independently retrieved underlying works and reproduces them faithfully**, so
those attributions are no longer unverified leads. **Gregory, Rabanus, Remigius
and the Gloss were NOT checked and remain leads**, and the `Chrysostomus super
Matth.` excerpts remain the *Opus imperfectum*, whose ascription to Chrysostom
is rejected. **The check was made against the same Migne recensions the Catena
drew on, not against critical editions**, so it establishes faithful
transmission and not the Migne text's own correctness.

**1 Peter 2 quotes two of this Mass's three appointed psalms within five
verses, and that is a warning and not a finding** [SCR-032]. 1 Pet. 2:3 quotes
Ps. 33:9a, which the Offertory **does** appoint; 1 Pet. 2:7 quotes Ps. 117:22,
which is thirteen verses outside the appointed Gradual. **The asymmetry must be
stated if this is used at all**: the first half is a real canonical
relationship to the Offertory, the second is a fact about 1 Peter and Ps. 117
only. **Reporting the two halves as one relationship would manufacture a
connection the appointed texts do not make.**

### 2.6 Offertory — Ps. 33:8–9a

**The psalm is anchored by its own superscription to a named deliverance
narrative, and the narrative does not fit the name** [SCR-015]. `Davidi, cum
immutavit vultum suum coram Achimelech`. The tracked Douay prints the
cross-reference as "[1 Kings 21.]", which in Douay book-naming is modern
**1 Samuel 21** — a hazard `guidance/bibles-for-agents.md` names explicitly. But
that chapter read whole shows **Achimelech the priest at Nobe in vv. 1–9 and
the change of countenance at v. 13 before Achis, king of Geth**, in the second
half of the chapter. **The divergence is a textual observation; the explanation
is not settled here and must not be supplied.** The tracked Catholic Public
Domain Version reads `Abimelech` at the superscription where the Clementine and
both tracked Douay texts read `Achimelech`. **This bears materially on the
Offertory**, because Augustine's Eucharistic reading of v. 9 is anchored in the
superscription and in David *before Achish* — that is, on the narrative's
Achis, while the Latin superscription names Achimelech. **A common scholarly
explanation of the divergence exists but no source for it is registered here,
so it is recorded as unresolved rather than stated.**

**The acrostic can now be stated as documented reception, which lifts a
bounded negative the prior brief carried as unassertable** [PAT-204]. The prior
brief recorded that Ps. 33 (MT 34) is commonly described as an alphabetic
acrostic and that this **could not be verified**: no Hebrew psalter is held,
neither tracked Latin nor tracked English edition carries acrostic apparatus,
and Bellarmine, the one registered witness noting it, does so at a locus
reaching no appointed verse and in an abridged Victorian translation. **There is
now a checked sixth-century Latin witness stating it and locating the appointed
verses within it.** Cassiodorus, *Divisio psalmi*: `Per totum psalmum verba
prophetae sunt, alphabeti Hebraei litteras, excepta sexta, in capitibus versuum
per ordinem ponentis`; he tags every verse with its letter, **HETH at the
Offertory's first verse and TETH at its second**; and on the skipped letter he
says he found no settled patristic judgement — `Ego enim non inveni Patrum
definitam de hac parte sententiam`. **Two bounds, both material, and both must
be printed with it:** this is **Cassiodorus reporting about the Hebrew and not a
Hebrew text**, so it is documented reception (class 3) and **not** a textual
observation (class 1); and the reception lane expressly declines to say whether
the acrostic may now be asserted as a fact about the psalm, leaving that to the
lane that owns the scriptural claim. **This brief settles it as follows: the
guide may state that a checked sixth-century Latin commentator says the psalm
is alphabetic and locates the appointed verses at HETH and TETH; it may not
state that the psalm is an acrostic as a fact about the Hebrew, because no
Hebrew is held** (§4.5).

**Augustine rejects a rival reading and defends the one the missal prints**
(prior run, restated): `mendosi codices: Immittet Angelum Dominus … sed sic:
Immittet Angelus Domini`, and he identifies that Angel as Christ, the Angel of
the great Counsel. The locus is *Enarratio in Ps. XXXIII* **Sermo II**, not
Sermo I. **And his text continues `et ERUET eos` where the missal prints
`et ERIPIET eos`** — the two agree exactly on the point in dispute and differ
on the following verb, which is evidence the missal's text is not simply
Augustine's and must be reported alongside the agreement.

**The convergence is materially strengthened this run, and in a sharper form**
[PAT-201]. **Cassiodorus's lemma reads `Immittet angelum Dominus`** — exactly
the reading Augustine denounced as belonging to faulty copies. **So the variant
Augustine fought was still standard in the principal medieval Latin psalm
commentary, and the 1962 Offertory follows Augustine against Cassiodorus.**
The missal does not merely happen to agree with Augustine; it agrees with him
**against** the reading the sixth century carried. **It remains a convergence
and not a descent:** nothing traces transmission, and Cassiodorus is a witness
to a text, not evidence about the missal's ancestry.

**Cassiodorus does not identify the angel with Christ, and that is a
disagreement to preserve rather than stack** [PAT-203]. He reads the appointed
verb `Immittet` as deliberately covert — `propter insolentiam humanae
fragilitatis non palam facit, sed occultis immissionibus operatur` — and turns
to the moral sense: `Angelus autem minister est voluntatis divinae. Quapropter
si vis te angelum fieri, fac quod praecipit … Tunc enim spiritu angeli sumus,
quando ministri supernae voluntatis efficimur.` **Augustine's christological
identification is the reading a guide will reach for, and the principal
medieval Latin commentator on the same verse does not make it.** The prior brief
warned that the missal's capital `Angelus` is an orthographic fact and not
evidence of the christological reading; **Cassiodorus is positive evidence that
a Latin reader could take the verse otherwise.**

**Cassiodorus's eucharistic reading of `Gustate` lifts a limit the prior brief
had to set** [PAT-202]. Augustine's eucharistic reading of the same verse is
anchored in the psalm's superscription, which the Offertory antiphon does not
print, so it was available only as reception of the psalm. **Cassiodorus's is
anchored in the appointed verbs themselves:** `Gustate non pertinet ad palatum,
sed animae suavissimum sensum, qui divina contemplatione saginatur. Nam ut ipsum
gustum intelligeres, sequitur, videte, quod utique non ad os pertinet` — and he
reads it eucharistically from the verb, citing Jn. 6:53 and the life-giving
flesh taken from the Virgin. **So the reading is available to a hearer of the
antiphon alone.** Note the convergence with Cyril of Jerusalem's "trust not the
judgment to your bodily palate", reached in Latin and without dependence on the
Jerusalem catechesis.

**Two fourth-century mystagogical witnesses attest the verse as the Church's
own communion invitation, and the 1962 Mass does not use it that way** (prior
run, restated). Cyril of Jerusalem reports it chanted at the communion; Ambrose
cites it **with** the clause `beatus vir qui sperat in eo` that the Roman
Offertory omits. **In the 1962 Fourteenth Sunday the same verse stands at the
OFFERTORY, before the consecration, and this Mass's Communion is a different
text entirely.** *Bounds:* both witnesses in nineteenth-century English only,
neither collated; Cyril's authorship disputed and not swept. **And the
displacement is now attested as living practice in a surviving Western rite**
[PRE-010]: the Mozarabic *Missale mixtum* prints `Gustate et videte quam suavis
est Dominus` as the *ad accedentes* chant `dicat chorus` at communion time,
cued by incipit 34 times across the book. **As liturgical fact the displacement
is well precedented and a worker must not present it as a discovery** (§9.5).

**The Offertory's second clause is quoted in the New Testament, and the same
Latin Bible renders the underlying Greek adjective two different ways**
[SCR-024]. Ps. 33:9a reads `quoniam suavis est Dominus`; 1 Pet. 2:3 reads
`quoniam dulcis est Dominus`, and a whole-Bible search returns exactly these
two. The Greek of 1 Pet. 2:3 is χρηστός; Brenton renders the psalm's adjective
"good". **The Douay levels the split, rendering both "sweet", so the split is in
the Latin.** *Bound:* that the Greek psalter reads χρηστός at Ps. 33:9 is a
**lead** and is not verified — no Greek psalter is held, and Brenton is an
English translation of the Septuagint, so it evidences the sense and not the
word. **The inference that the Vulgate has split one Greek word between two
renderings is well supported but not closed, and closing it costs one
registration.**

**The Offertory's argument runs close to the Gospel's two verses past its own
cut** [SCR-017]. Ps. 33:10–11 and Mt. 6:32–33 both set seeking God against want
of food and both promise that those who seek will not lack. **Clearly flagged as
inference:** a similarity of argument, not of wording, and the Gospel's own
`inquirunt` is used of the gentiles **negatively** where the psalm's participle
is positive — **a counter-indication and not a support.** Recorded because the
appointed excerpt does not contain the psalm verses at all.

### 2.7 Communion — Mt. 6:33 recast

See §1.2 for the four departures and §7.5 for the settled cross-proper claim.

**Augustine's exegesis bears on the antiphon's word order, and the two must be
kept apart** (prior run, restated). On `primum` he argues an ordering of
**importance and not of time** — `non tempore, sed dignitate` — corroborated in
Latin from an independent thirteenth-century witness. **That is corroboration,
not verification**; PL 34 was again not opened this run.

**Aquinas expounds all three members of the verse the antiphon recasts**
[PAT-135]: the kingdom sought as the **end**, because the kingdom is beatitude
and `Regnum dicitur a regendo: tunc enim homo regitur, quando voluntati regentis
subditur`; the justice called **his** and not man's, `quia per iustitiam
propriam nullus potest venire ad regnum`; and the rest added over and above,
`quasi, ultra forum`. He adds `non debemus evangelizare ut comedamus, sed potius
e converso`. **This is the closest thing the sweep has to Doctoral commentary on
the appointed Communion.**

**Two limits stand, and the second is new** [PAT-135]. Aquinas is expounding
Mt. 6:33 **in its Gospel place, not the antiphon**, so the prior brief's line
holds unchanged: **the observation that the antiphon promotes `Primum` to first
position is an editorial observation and not patristic.** And his gloss on
`iustitiam eius` answers a question **the antiphon's own recasting raises**,
since the antiphon drops the phrase; **whether the recaster meant anything by
the omission is not established.**

**The line the author must not cross.** (1) Augustine's and Aquinas's exegesis
of Mt. 6:33 is documented reception and is theirs. (2) The observation about
word order is editorial, and **no witness in either sweep comments on the
antiphon.** A guide may state both; it must not present the second as
patristic.

### 2.8 The three composed orations

**Reception: a bounded negative, re-run over a much larger corpus, and it
holds** [PAT-400]. No patristic or medieval commentary on the Collect `Custodi,
Domine`, the Secret `Concede nobis, Domine`, or the Postcommunion `Purificent
semper et muniant` was located. This run added roughly **5.5 MB of Latin** to
the corpus over which the prior negative was stated — Augustine's *Expositio ad
Galatas*, Hilary's and Jerome's *In Matthaeum*, Jerome's *In Galatas*,
Cassiodorus's *Expositio in Psalterium* and Aquinas's *Super Matthaeum* cap.
6–12 with the *Catena* cap. 5–9 — searched on `Custodi`, `propitiatione
perpetua`, `labitur humana mortalitas`, `abstrahatur a noxiis`, `hostia
salutaris`, `purgatio delictorum`, `propitiatio potestatis`, `Purificent`,
`perpetuae salvationis` and `salvationis effectum`. **The only hit of any kind
is a coincidental use of the verb in Cassiodorus** — `multiplici colluctatione
purificent, et ad aeternam vitam` — **which is not commentary on the
Postcommunion.**

**Why the negative is expected rather than surprising:** these are anonymous
composed Roman orations, and the patristic genres swept do not take liturgical
orations as their object. **Bounds, unchanged and real:** a literal string
search cannot exclude paraphrase, a different incipit, or an oration cited by
its Sunday rather than its words [PAT-400, THE-045].

**The cheapest repair is still unmade, and is now named for the third time.**
Schuster's *Liber Sacramentorum* vol. 3 is registered here at sha256
`410f6d11…7239`, **and the coverage lane establishes that the volume is
registered complete, hashed, 462 pages, `rights_status = "public-domain"`, with
printed page 123 already visually inspected in the exact hashed facsimile and
registered passages at adjacent Sundays (vol. 3 p. 123, the Tenth Sunday's
Postcommunion; vol. 3 pp. 132–134, the Thirteenth Sunday's propers)**
[COV-011]. **The Fourteenth Sunday therefore sits a few printed pages further
into bytes this repository has already identified and inspected.** The bindings
file's phrase "registered here and deliberately not retrieved" describes a
legitimate scope decision but, **as a statement about holdings, reads as though
the volume were unavailable, and it is not** [COV-011].

**A second instrument the guide has never consulted, and it is the highest-value
gap this run found** [COV-002]. The repository registers the **Usuarium Corpus
Orationum digital concordance** — the standard per-oration index of the Latin
oration tradition — as `work.elte-usuarium.corpus-orationum-digital`, with a
dated web edition, a per-entry retrieval route proven end to end (entry CO 4829,
artifact and passage both registered), and a `locus_pattern` of `co-<n>`. **A
grep of the whole leaf for `usuarium`, `corpus orationum` or
`corpus-orationum` returns nothing.** What it would yield is **which
sacramentaries carry each oration and the printed CO volume and page at which
to check it** — precisely what would replace, or at minimum corroborate, the
guide's admitted sole dependence on Wilson's apparatus, and it would give the
Veronense question an independent route. **Three limits keep this a
lead-mapping repair and not a verification one:** the work record itself says it
is "a finding and text-control aid, not a replacement for the printed critical
apparatus"; the artifact is `rights_status = "restricted"`, so its bytes may not
be reproduced and any published wording must come from elsewhere; and it is a
dated web state, so a fresh consultation needs its own dated artifact record.
**This brief records it as an unclosed gap. This stage may not retrieve it, and
no later stage of this workflow may either.**

**The one positive is thin, and its thinness is the finding** (prior run,
restated at [THE-045]). Guéranger's remarks on Secret and Postcommunion are one
sentence each and are paraphrase rather than exegesis; only the Collect note
makes an interpretive move — that the "abyss of vice" is specifically the
Epistle's catalogue — and even that is an association asserted rather than
argued. **A guide must not inflate a one-sentence editorial gloss into
documented reception.** One genuine convergence worth keeping: he construes
`propitiatio potestatis` as the appeasing of God's power, independently agreeing
with `verified.md`.

**Guéranger is a reception witness only and never a text witness** (prior run,
restated). His printed Latin differs from the typical edition at four points.
**A guide must not quote the appointed Latin from him.**

**What the older books show these prayers being used for, which is new this
run** [LIT-020]. Gerbert's *Dominica XVI* carries two elements the 1962
formulary does not: a **second Collect** (`Praesta nobis misericors Deus, ut
placationem tuam promptis mentibus exoremus, et peccatorum veniam consequentes,
a noxiis liberemur incursibus`) and a **proper Preface of the priesthood**
(`qui aeternitate sacerdotii sui omnes tibi servientes sanctificat sacerdotes,
quoniam mortali carne circumdati, ita cottidianis peccatorum remissionibus
indigemus…`). **Two observations the sources carry:** the older Preface reads
this Mass's action as the priest's own daily need of remission joined to the
people's, a different accent from the Trinity Preface 1962 appoints; and the
older second Collect turns the first Collect's own phrase `a noxiis` from a
petition for the Church to be drawn away from harm into a petition for the
individual to be freed from its assaults, **so the pair moves from ecclesial
preservation to personal pardon within one Mass. Whether either bears on the
1962 formulary as celebrated is a judgment for the author.** **Three bounds:**
Gerbert's Preface is read in OCR only, no page image; the second Collect and
proper Preface are a feature of the R/S tradition **and not of the Gregorian**,
so they are not evidence about the Roman use behind 1962; and the disappearance
of proper Prefaces is a general fact of the Roman Missal's development, not
something proper to this Sunday. **A fourth caution, and it must not be
smoothed:** Gerbert's second Collect and the pre-1960 seasonal second and third
orations abolished by *Variationes* cap. IV n. 18, AAS 52 (1960) p. 709, are
**not the same thing** — the one is a proper second Collect of this Mass in the
Frankish Gelasian, the others are seasonal orations appointed by rubric across
many Masses. **The continuity is a continuity of shape, not of text** [LIT-012].

---

## 3. Corpora, languages and works searched

Recorded per lane, because the bounds differ per lane and a bound stated once
for the whole run would be false.

### 3.1 Scriptural corpora

| Corpus | State | What it controlled |
|---|---|---|
| Clementine Vulgate, tracked, local JSON chapter files | read whole for Pss. 33, 83, 94, 117, Gal. 5, Matt. 6; **plus targeted whole-Bible normalised searches across all 73 books** | Every collation at §1.2 and every whole-Vulgate distribution at §2 [SCR-002, SCR-016, SCR-026, SCR-027, SCR-028, SCR-029, SCR-031] |
| Douay–Rheims (Challoner) and Douay-American 1899, tracked | read at the appointed loci, at Ps. 33:1 and at 1 Kings 21 whole | The English of the Vulgate; the 1 Kings 21 = 1 Samuel 21 correspondence and the Achimelech/Achis divergence [SCR-015] |
| Catholic Public Domain Version, tracked | read at Ps. 33 | The `Abimelech` reading at the superscription [SCR-015] |
| Robinson-Pierpont Byzantine Textform, `rp2018-byztxt-unicode-csv`, MAT, GAL, 1PE | tracked; the `{NA}` braces read **structurally, not by string search** | Greek for Mt. 6:24–33; Gal. 5:16–25; 1 Pet. 2:3; the list counts and the critical-text apparatus [SCR-006, SCR-008] |
| Brenton, *The Septuagint with an English Translation* | tracked, public-domain, whole psalter | LXX **versification** at all four psalms — direct evidence for versification, **a lead only for LXX wording** [SCR-019, SCR-024] |
| Project-created psalm-numbering concordance `psalm-numbering-ee3c7757` | tracked; rows read directly | The Vulgate/English/Hebrew correspondence, per `scripts/_psalms.py`'s declaration that it is the sole authority [SCR-019] |

**Languages actually read:** Latin, Greek, English. **No network retrieval of any
kind; everything read from local tracked files** [SCR-021].

### 3.2 Reception corpora

**Languages actually read this run: Latin and Greek and English.** This is a
change from the prior run, which read no text in Greek.

| Witness | Route and state |
|---|---|
| Augustine, *Expositio ad Galatas* ss. 45–53 | augustinus.it Latin, curl 2026-08-28, 150,090 bytes, sha256 `92b0b0a5…9670`. **Acquired, searched, inspected in Latin.** Machine transcription of Migne; **PL 35 page image not collated; CSEL 84 (Divjak) not consulted** [PAT-100] |
| Jerome, *Comm. in Ep. ad Galatas* lib. III | Corpus Corporum transcription of Migne via Latin Wikisource `?action=raw`, curl 2026-08-28, 329,953 bytes, sha256 `f50b3e2b…200b6`. **Acquired, searched, inspected in Latin; PL 26 not collated; CCSL 77 not consulted** [PAT-150] |
| Hilary, *Comm. in Matthaeum* cap. V ss. 5–13 | Same route, 339,548 bytes, sha256 `548a3de3…2f1793`. **Inspected in Latin; PL 9 not collated; SC 254 not consulted** [PAT-110] |
| Jerome, *Comm. in Matthaeum* lib. I | Same route, 473,464 bytes, sha256 `1e8407fa…d99f`. **Inspected in Latin; PL 26 not collated** [PAT-120] |
| Cassiodorus, *Expositio in Psalterium*, complete | Corpus Corporum TEI XML, `mlat.uzh.ch/php_modules/download.php?type=file-xml&idno=21404`, curl 2026-08-28, 3,364,651 bytes, sha256 `c23aef1a…a153`. **Inspected in Latin; PL 70 page image not collated; CCSL 97–98 not consulted** [PAT-200] |
| Aquinas, *Super Evangelium S. Matthaei lectura* cap. 6 lect. 5 | Corpus Thomisticum Busa/Alarcon transcription of Taurini 1951, 336,694 bytes, sha256 `c7884311…8f3d`. **Inspected in Latin; no Marietti or Leonine page collated. This is a *reportatio* (Leodegarius Bissuntinus), not Thomas's own pen, and must be cited as such** [PAT-130] |
| Aquinas, *Catena aurea in Matthaeum* cap. 6 lect. 17–21 | Corpus Thomisticum, 437,678 bytes, sha256 `55b33797…4ac32`. **Now a checked map for Hilarius and Hieronymus; a lead-map for Gregorius, Rabanus, Remigius and the Glossa** [PAT-140] |
| Theodoret, *Interpretatio in Psalmos* Tomus 2 (Pss. 71–87) and Tomus 3 (Pss. 87–150), PG 80 | TLG text posted on Documenta Catholica Omnia by authorisation of 15 May 2008; fetched by curl **over plain HTTP** 2026-08-28, 7,806,557 bytes sha256 `a00b9017…85c5` and 9,737,900 bytes sha256 `e9763a32…052b`; text extracted locally with `pdftotext` from a **real text layer, not OCR of an image**. **Acquired, searched, inspected IN GREEK; PG 80 page image not collated** [PAT-300] |
| Chrysostom, *In epistulam ad Galatas commentarius*, PG 61:673–674 | Same source and route, 4,249,429 bytes, sha256 `b9408b20…4b19`. **Inspected in Greek; PG 61 not collated. Not a full collation of the homily: three specific claims were checked and the rest of the NPNF text remains English-only** [PAT-310] |
| Augustine, *Enarrationes in Ps.* 33 (Sermo II), 83, 94, 117 | Prior run, restated. NPNF English via New Advent plus Latin collation from augustinus.it; **PL 36–37 not collated** — and see §4.10 on the New Advent provenance risk |
| Augustine, *De sermone Domini in monte* II; *De opere monachorum*; Chrysostom *Hom. in Matt.* 21–22; Cyril of Jerusalem *Myst. Cat.* V; Ambrose *De mysteriis* IX.58 | Prior run, restated. **NPNF English only**; PL 34, PG 57, PG 33 and PL 16 not collated |
| Aquinas, *Super Galatas*; Anthony of Padua, *Sermo Dominica XIV*; Guéranger, *The Liturgical Year* XI | Prior run, restated. Latin (Aquinas, Anthony) and English (Guéranger); Anthony's artifact is `storage='restricted'` and only his thirteenth-century Latin may be quoted |

**Rights, and it governs two of the new witnesses** [PAT-300, PAT-310,
PAT-405]. The Documenta Catholica Omnia Greek PDFs carry the **Thesaurus
Linguae Graecae's copyright on the digitisation**, authorised for posting;
Theodoret's and Chrysostom's Greek is public domain by age and is what may be
quoted, **and the digitisation may not be reproduced wholesale.** No bytes were
written into the repository by any lane.

**The evidence-state ceiling for everything in this table** [PAT-405]: **nothing
retrieved this run was collated against a printed Patrologia page or a critical
edition, so every witness added stands at *inspected* and none at *verified*.**
Two further qualifications carry with particular findings: the Corpus Corporum
Latin is **normalised to classical orthography**, which is why Jerome and Hilary
appear here with `j` and `ae` spellings a PL page would print differently; and
the DCO Greek carries TLG's copyright as above. **No later worker may mistake
the volume of new material for a rise in its state.**

**Method discipline, unchanged** [PAT-403 and the prior run's PAT-001]: every
witness reached by `curl` to a local file, hashed, converted locally and grepped
locally. **The WebFetch tool, which interposes a model, was not used for any
source text**, per `guidance/sources.md`.

### 3.3 Liturgical-history corpora

**This section is corrected against the prior brief; see §0.3(b) and §0.3(d).**
The prior version listed three witnesses and did not name the declared corpus
record.

**The declared search boundary this repository already holds** [LIT-021]:
`src/sources/corpora/ancient-sacramentaries-2026-08-01.toml`, snapshot sha256
`af104231…a759dd`, **eight optical text layers of six printed critical
editions** — Feltoe 1896 Veronense (two scans), Wilson 1894 Old Gelasian (two
scans), Wilson 1915 Hadrianum, Férotin 1912 *Liber mozarabicus sacramentorum*,
Bannister 1917 *Missale Gothicum*, Lowe 1917 *Bobbio Missal*. **All eight
digests were reproduced by refetching this run.** Its declared scope is "the
boundary within which this project searched for the ancient ancestors of the
postconciliar orations", and **its own completeness note is candid and binding:
it holds no eighth-century Gelasian (Gellone, Angoulême, Rheinau, Bergomense),
no Ambrosian book, no Gregorian supplement beyond what Wilson prints, no
monastic or diocesan medieval sacramentary, and no later Roman missal**, and
"Acquisition is not inspection. Nothing in this corpus has been collated against
page images." **The four unopened books of §4.6 are therefore not reachable
through it.**

| Witness | Route and state |
|---|---|
| Wilson, *The Gelasian Sacramentary* (Clarendon 1894) | Registered **twice** under two work identities [LIT-005]. Identity B carries **two independent IA OCR layers**, sha256 `039123ca…684d84` (1,098,845 bytes, 37,086 lines) and `25586b16…7fb16f1` (1,147,494 bytes, 47,554 lines); both digests and line counts reproduced. **Read this run in both layers, which agree verbatim on every sentence quoted; no page image consulted.** The prior run read page images, which is the stronger state per locus [LIT-006 – LIT-010, LIT-014, LIT-015, LIT-019] |
| Wilson, *The Gregorian Sacramentary under Charles the Great* (HBS XLIX, 1915) | Registered OCR layer sha256 `3613cce6…6a20`, digest reproduced. **Read at printed pp. 43 and 173–174 plus the index; single layer, no second optical witness exists in the corpus; no page image** [LIT-023, LIT-024, LIT-025] |
| Feltoe, *Sacramentarium Leonianum* (Cambridge 1896) | **Registered** — see §0.3(b). Two IA OCR layers, digests and line counts reproduced by refetching; searched, **no page image** [LIT-001, LIT-002, LIT-003] |
| Férotin 1912 Mozarabic, Bannister 1917 Gothicum, Lowe 1917 Bobbio | Corpus members, digests reproduced, searched on eleven distinctive strings; **no page image** [LIT-022] |
| Gerbert, *Monumenta veteris liturgiae Alemannicae* vol. 1 | **Opened at the locus for the first time** [LIT-011], in **two independent Internet Archive OCR digitisations** (`monumentaveteri00gerbgoog`, `bub_gb_RIkPAAAAIAAJ`) which agree verbatim. **NEITHER is a registered artifact of this repository.** The registered e-rara excerpt covers only the first 50 PDF leaves and stops 123 pages short of printed p. 173 [COV-011]. Eighteenth-century long-s type, a hard case for OCR; **no page image collated** |
| Pamelius, *Liturgica Latinorum* | **Acquired in the wrong volume.** IA item `liturgicalatinorum1571` is **Tomus I** only, per its own title page; Wilson's citation "Pam. 410" is in Tomus II [LIT-026] |
| Mohlberg, Eizenhöfer and Siffrin 1960 critical Gelasian | Registered, `storage='restricted'`, `indexable=false`, 357 pages, sha256 `71f1b198…068f`. **Not fetched; no searchable text exists here.** It is the edition that would give these prayers their standard modern numbers [LIT-027] |
| Honorius, *Gemma animae* IV.72, PL 172 cols. 717–718 | **NOT reopened this run.** Every statement about Honorius at §6.3 is taken from the prior run's page-image reading as the prior brief reports it [LIT-017, LIT-027] |
| `src/sources/calendars/roman-1962/propers.yaml` | Tracked. Read this run for `pentecost-13`, `-14`, `-15`, `-16` and `-9`. **A repository derivative, NOT a facsimile collation**; the profile makes the printed missal controlling where the two disagree [LIT-017, LIT-018, LIT-025] |

**Repository sweep repeated 2026-08-28** over `src/sources/` for Rheinau,
Rhenaug, Gallen, Sangall, Pamel, Pamelius, Menard, Menardus, *Liturgica
Latinorum*, Liturgicon: **no record of any kind for any of those four books.**
**Gerbert is registered and the prior brief's blanket "no record exists for any
of the five" was false for him** — work, edition, a hash-verified 51-page
e-rara scan-excerpt and a verified passage record at printed p. 18, added at
commit `01fcbfda2` on 2026-07-29, before the prior run [LIT-004].

**The diagnosis that covers §0.3(b), §0.3(d) and this section** [LIT-021]:
every member of the sacramentaries corpus is `storage='remote'` with
`indexable=false` and no payload in the tree, **so a lane that establishes what
the library holds by grepping the working tree will see nothing and conclude the
library holds nothing.** The corpus record is the index that answers the
question, and it is one file.

**This lane is an optical-text lane throughout** [LIT-027]. **No page image of
any kind was consulted by it**, and where a prior run read a page image **that
reading controls** (§6.8). Every finding that says "confirms the prior run" is a
corroboration from a weaker evidence state.

### 3.4 Source-library enumeration

The coverage lane enumerated **registered records**, not tracked payloads,
because a restricted artifact has bytes identified and hashed but not retained
and so has nothing to grep [COV-010]. **The bound of the survey:** every work
directory under `src/sources/works/` was enumerated and the relevant ones opened
to edition, artifact, segment and passage level; `src/sources/corpora/` and
`src/sources/inventories/` were read in full listing and the two files bearing
on this leaf read entire. **It is a survey of registered records and not of the
reachable web: an absence there means this repository holds no record, not that
the work is unobtainable.**

### 3.5 Precedent corpus

**Corrected and widened; see §0.3(d).** Every "not located" classification in §9
is bounded by exactly this.

**(a) Eight full-text missal payloads, all tracked, indexable and present in the
working tree** [PRE-001]:

| Artifact | Bytes | Calibration count for `dominus` [PRE-002] |
|---|---|---|
| Missale Romanum, Pustet Ratisbon 1862 | 2,503,914 | 299 |
| Missale Romanum, Vatican typica 1604 | 2,025,007 | 287 |
| Missale Romanum, Venice 1570 | 1,636,559 | 163 |
| Missale Ambrosianum, Milan de Sirturis 1712 | 1,868,008 | 986 |
| Missale Ambrosianum, Milan Sirturi 1640 | 1,948,375 | 589 |
| Missale Ambrosianum, Milan Pachel 1499 | 1,277,898 | **0 — unusable** |
| Missale mixtum Mozarabicum, Rome Monaldini 1755 (two scans) | 1,491,426 / 794,299 | 750 |
| Liturgia Mozarabica, PL 85 Migne 1862 | 4,622,815 | 634 |

**(b) 182 published Triptych documents carrying a `main.tex` under
`src/claude` and `src/gpt`** — not only the propers leaves, but the articles,
theology, devotions, history, biographies, curriculum and reference trees, of
which at least four treat this formulary's appointed material directly
[PRE-003]. Searched by accent-stripped normalised index over all **2,865** `.tex`
and `.md` files under the two provider trees. **Bounded:** those four documents
were checked for the appointed loci and for the conjunctions of §9; **they were
not read end to end**, and the curriculum volumes were not swept for incidental
quotation.

**(c) Still not reached, for every conjunction alike** [PRE-016]: any printed
chant repertory (Graduale Romanum, Antiphonale, Hesbert's *Corpus
Antiphonalium*), of which this repository holds no full-text payload for the
relevant genres; any pre-Tridentine commentary tradition; any sanctoral or
votive Triptych leaf, because none exists; and the medieval Ambrosian and
Mozarabic manuscript traditions behind the printed books searched.

**The OCR caveat is not theoretical, is worse than the prior brief recorded, and
governs every negative below** [PRE-002, PRE-017]. Three worked demonstrations:
(i) `grep -i immittet` over the Pustet misses the Lenten occurrence entirely,
broken as `Immit-`/`tet`; (ii) the phrase `circuitu timentium` returns **0 in
all eight artifacts**, yet the Pustet demonstrably prints the Offertory, as
`in cirdiitu tim6ntium eum et erlpiet eos` — **diacritic-substitution OCR, a
second species beyond hyphenation**; (iii) `venite exsultemus domino` returns 0
everywhere, while the Pustet prints `uenite exultemus d6mino` without the `s`.
**The Vatican typica 1604 text returns 0 for `post pentecosten`, `pentecoste`
and `postcommunio` while returning 174 for `dominica` and 152 for `communio`:
it cannot carry a negative about the Sundays after Pentecost at all.** **Every
negative reported over these artifacts is bounded to whole-phrase and fragment
searches actually run, is correctable by a page image, and is stated as "not
located" and never as "absent".**

### 3.6 Cultural-afterlife corpora

**Answered on 2026-08-28** [CUL-015]: the **Caselaw Access Project** static file
service at `static.case.law`, which serves per-case JSON transcriptions of the
printed reporters and paginated HTML with star-page labels — **this is new to
the lane's toolkit and is why most of this run's legal evidence was read as
CONTINUOUS text rather than reassembled search snippets**; the CourtListener
REST API v4 search endpoint; the UK Hansard search API and the full historic
report; **loc.gov's per-page services** — the word-coordinates service at
`tile.loc.gov/text-services/` and the IIIF image service at
`tile.loc.gov/image-services/iiif/`, which together allow a phrase's ALTO
coordinates to be converted into an image crop **and read as a page image**;
archive.org item metadata and downloads; Project Gutenberg plain text.

**Refused on 2026-08-28, itemised so the gaps are correctable** [CUL-015]:
HathiTrust full-text search (HTTP 403 with and without a browser user-agent,
**not searched at all**, as on 2026-08-27); the **Google Books API (HTTP 429,
quota exceeded — a new refusal not recorded by the prior sweep), not searched at
all**; the CourtListener `/opinions/` endpoint (HTTP 401 without a token);
courtlistener.com's own opinion pages (empty HTTP 202); the Internet Archive
full-text endpoints (unresolved or 404), so IA could be searched at metadata
level only.

**The controlling limit on every loc.gov count and every loc.gov negative,
re-established by calibration this run** [CUL-015]: **loc.gov's quoted-string
search does not do exact-phrase matching — it degrades to an AND of terms.** The
query for `against such there is no law` returns **46,635** items with visibly
unrelated ranked results, **the identical number the prior sweep obtained on
2026-08-27**, which confirms the defect is stable and not a transient.
**Consequence: no loc.gov figure anywhere in this brief is a phrase count, and
no loc.gov negative extends past the ranked results actually opened.**

**The method that closed the gap between *inspected* and *verified*, recorded so
it can be repeated cheaply** [CUL-015]. Fetch
`https://www.loc.gov/resource/<lccn>/<date>/ed-1/?sp=<page>&fo=json`, take
`resource.fulltext_file`, request it with `format=alto_xml` for per-word
bounding boxes, note that **the ALTO coordinate space maps to the IIIF image at
a 1:4 reduction on every page tested**, then request the IIIF crop and read the
JPEG. **One trap, and it cost time: request the crop at `full` size.** Asking
IIIF to upscale returns unreadable blur, and on a low-resolution master such as
the 1908 *Spanish American* page (3292 × 5235) **only the native-size crop is
legible at all**. **Collation paid for itself immediately** — it settled three
questions the prior brief left open and lifted a reconstructed-punctuation
warning (§8.4, §8.5). **It is the single cheapest quality improvement available
to this target.**

**Further bounds on the whole cultural return** [CUL-015]. **Language: English
only.** Jurisdiction: the legal corpus is CourtListener's and the Caselaw Access
Project's, both overwhelmingly American, and **no English or Commonwealth
case-law sweep was run**, so no finding may state a claim about Anglo-American
law as a whole. Press: Chronicling America only — English-language American
newspapers, thin after 1922 and effectively ending about 1963; **no British,
Irish, Continental or Latin-American press was searched at all.** Books: **not
searched, because both book corpora refused.** Parliament: the UK only. **Every
exact-phrase count reported is the API's own and was not audited item by item.**
Quote aggregators and attribution sites were not used as evidence anywhere.

---

## 4. Material negative results

Each is bounded and correctable, and each names what would correct it.

### 4.1 No exegetical reception of the three orations

Stated in full at §2.8 [PAT-400, THE-045]. **The negative survives a corpus
5.5 MB larger than the one it was first stated over.** Two repairs are named and
neither was made: **Schuster vol. 3**, registered complete, hashed, inspected at
p. 123, with registered passages at adjacent Sundays [COV-011]; and the
**Usuarium Corpus Orationum concordance**, registered with a proven per-entry
route and never consulted by this guide [COV-002].

### 4.2 The Greek side is materially better than it was, and is still bounded

**Read in Greek this run** [PAT-401]: Theodoret on Pss. 83, 94 and 117;
Chrysostom on Gal. 5:19–25 at PG 61:673–674. **That is two Greek authors read in
Greek where the prior run had two read in English.**

**NOT retrieved, each named so a later attempt can tell an unreachable work from
one merely not looked for** [PAT-401]: Chrysostom's *Homiliae in Matthaeum*
21–22 in Greek (PG 57), **so the Gospel material from him remains NPNF English
only**; Chrysostom's *Expositio in Ps. CXVII* (PG 55), which the prior sweep also
failed to reach; Theodoret's *Interpretatio epistolae ad Galatas* (PG 82);
Theodoret on Ps. 33 (Tomus 1), **deliberately not fetched because a verified
passage record for him at PG 80:1101–1109 is already held** [PAT-300].

**NOT swept at all, for any appointed passage** [PAT-401]: Origen's own Greek,
Basil, Gregory of Nyssa, Gregory of Nazianzus, Cyril of Alexandria, Theophylact,
Euthymius Zigabenus, Didymus, Athanasius.

**Three instructions, and one is now easier to obey.** (1) Nothing supports a
claim about the Fathers **as a body**; every claim names its witnesses. (2) **A
guide must not present a Greek–Latin comparison as evenly grounded without
saying what was and was not read** — it is now grounded on two Greek authors
read in Greek rather than two read in English, which is a real improvement, but
it is still two authors. (3) **The route is now known and cheap**: the DCO MGR
PDFs carry TLG-transcribed Greek with a real text layer, so Chrysostom on
Matthew and on Ps. 117, and Theodoret on Galatians, are each one `curl` away
[PAT-401, PAT-403].

### 4.3 A named list of Latin and later witnesses not swept

Given so a later attempt spends its budget on what has not been tried
[PAT-402]. **Galatians:** Ambrosiaster, Marius Victorinus, Pelagius's
*Expositio*, the *Glossa ordinaria*, Nicholas of Lyra, Denis the Carthusian,
Cornelius a Lapide's commentary proper. **Matthew:** Bede, Rabanus Maurus,
Paschasius Radbertus, Christian of Stavelot, Remigius of Auxerre in his own
person, Bruno of Segni, Albert the Great, Nicholas of Lyra, Maldonado, the *Opus
imperfectum* in its own right. **Psalms:** Bellarmine's *Explanatio in Psalmos*
in the Latin, Prosper, Arnobius the Younger, Pseudo-Jerome's *Breviarium*, Peter
Lombard, Bruno the Carthusian.

**Named-but-unopened leads inside works that WERE read** [PAT-402]: Cyprian's
*De zelo et livore*, named by Jerome at Gal. 5:21; Augustine's *De civitate Dei*
XIV.2, named by Aquinas on the Epistle; **Augustine's *De haeresibus*, still the
unclosed lead behind the Euchite identification**; Augustine's anti-Pelagian
books, named by Cassiodorus at Ps. 117:8.

**These works exist in the world and are not hard to obtain; they are simply not
registered here, and the gap is not closable from the library's holdings** —
**every witness this run retained was reached by direct retrieval** [PAT-402].

### 4.4 The registered library holds almost nothing at the appointed loci

Re-checked against the library and every declared absence stands [COV-010].

- **Chrysostom on Galatians has no record of any kind.** `src/sources/works/john-chrysostom/` holds Matthew, Colossians, Ephesians, 1 Corinthians, John, Romans and the Statues, and nothing on Galatians; NPNF1-13, which prints that translation, is not among the held NPNF volumes. **This is the sharpest of the confirmed gaps, because the guide's Epistle reception rests on a work with no identity in the library at all.**
- **Jerome on Galatians:** no record. `src/sources/works/jerome/` holds the Matthew commentary, *De viris illustribus*, letters 106 and 108, and *Quaestiones hebraicae*.
- **Augustine's *Expositio ad Galatas*:** absent from the library, though **retrieved directly this run** [PAT-100].
- **Eusebius:** the only Greek artifact is *Die Kirchengeschichte, Bücher VI–X*; the English edition is Book VI. **HE III.24.6 and III.39.16 are genuinely unreachable, and Papias has no record at all.**
- **Hesbert, *Antiphonale Missarum Sextuplex*:** work and edition records, **no artifact**, so "not retrieved" is exact. **It is the only chant book registered anywhere in the library**, which confirms §4.5's "no chant book of any kind was consulted".
- **Hebrew:** only Kittel Leipzig vol. 1 (1909) with four page images at Gen. 15 and 1 Sam. 16 — **no psalm of any number.**
- **Greek psalter:** Swete's *Old Testament in Greek*, Cambridge vol. 1 only (Genesis–4 Kingdoms). The CATSS LXX morphology dataset is `storage='restricted'`, `indexable=false`, bytes not retained, **so it supports no replayable psalm query here.**
- **Ambrosiaster:** 1 Corinthians only. **Marius Victorinus and Cassian on Galatians: no records.**
- **The six Greek Fathers recorded as unswept hold nothing reaching an appointed passage:** Origen (*Contra Celsum*, *De principiis*), Basil, Gregory of Nyssa, Cyril of Alexandria, Theophylact (John only); Gregory of Nazianzus holds nothing on these loci.
- **Irenaeus III.1.1 is confirmed reachable** in searchable bytes: segment `ia-djvu-ocr-12cdc519` gives physical line ranges [[37256, 73656]] over the complete translated body and the facsimile segment gives artifact page ranges [[333, 585]] — **but there is no passage record for the locus, and registering one would yield an *inspected* and not a *verified* witness** [COV-010].

### 4.5 Editions absent from the scripture side

Re-run this run over `src/sources/works` for vetus-latina, psalterium, sabatier,
stuttgart, weber, nova-vulgata, nestle, aland, ubs: **no match of any kind**
[SCR-021, COV-009]. **No Psalterium Romanum and no Psalterium iuxta Hebraeos.
No Hebrew text of Pss. 33, 83, 94 or 117. No Greek psalter. No chant book of any
kind was consulted.**

**A precision correction to the prior brief, and it does not change the
substance** [COV-009]. The prior References state flatly that "no critical
edition is registered here." **Two are** — Westcott and Hort (registered only in
its 1882 Introduction and Appendix, so it carries editorial reasoning on select
readings and no continuous Greek text) and the INTF *Editio Critica Maior* for
**Mark**. **Neither touches Matt. 6 or Gal. 5**, so the guide's substantive
position is undisturbed. **The repair is to say what the prior §4.5 already said
correctly: no critical edition reaching an appointed passage is registered.**

**Three consequences that constrain what may be published** [SCR-021,
SCR-033]: (a) **it cannot be checked here whether the appointed psalm wording is
Gallican as against Roman or *iuxta Hebraeos*** — §1.2's result answers the
narrower question; (b) the acrostic structure of Ps. 33/34 cannot be verified
from a Hebrew text, and what stands in its place is Cassiodorus's report (§2.6);
(c) every critical-text statement at §2.2 is one step removed from a critical
edition, reaching the lane only through the `{NA}` braces. **Each is bounded to
this repository at commit `f4534e4cd` and each is correctable by one
registration.**

### 4.6 Four of the five sacramentary books remain unopened, and the reasons are specific

**Gerbert is now open at the locus** [LIT-011] — see §6.1. The other four, each
with a bounded attempt and its reason [LIT-026]:

- **Pamelius:** acquired in the **wrong volume**. IA `liturgicalatinorum1571` is Tomus I (the *Ritus et Ordo Missae*, the Ambrosian Masses, the Mozarabic Mass) per its own title page; Wilson's "Pam. 410" is in Tomus II. Zero hits for any `Custodi`/`ecclesiam` pattern, and **the volume's own text confirms the absence is a volume boundary and not a reading.** The other IA candidate, `ita-bnc-mag-00002780-001`, is likewise volume one.
- **Menard:** Internet Archive advanced search for creator "Menard, Hugues" and title "Divi Gregorii papae liber sacramentorum" **returned no results at all.**
- **Rheinau** (Zurich, Zentralbibliothek Rh. 30) and **S. Gallen** (Stiftsbibliothek 348): **manuscripts, not printed books.** No digitisation was sought, and neither is reachable by the searches run.
- **Gerbert's e-rara endpoints retried 2026-08-28:** both IIIF manifest URLs return HTTP 404; the title-info page and the DOI resolve 200 but expose no parsable page-range download.

**What a later sweep should do, in descending order of value** [LIT-026]:
acquire and register the two IA Gerbert digitisations, or better an e-rara
page-range covering printed p. 173, and collate §6.1 against a page image; find
Pamelius Tomus II and open p. 410; **recheck the Ottobonianus cue attachment
(§6.8) on Wilson 1915's page images**; and register the Feltoe and Wilson OCR
findings so the Veronense negative never has to be carried unreplayable again.

### 4.7 The Veronense negative — replayable, and the reason the prior brief gave was wrong

See §0.3(b). **The negative** [LIT-002]: none of the three orations occurs in
either hash-verified Feltoe layer, on a search after Unicode decomposition,
accent stripping, lowercasing, de-hyphenation across line ends and reduction to
single-spaced alphabetic text, over seventeen distinctive strings including
`custodi domine`, `propitiatione perpetua`, `labitur humana`, `abstrahatur`,
`ad salutaria dirigatur`, `hostia salutaris`, `purgatio delictorum`,
`propitiatio potestatis`, `muniant tua sacramenta`, `ducant salvationis` and
`salvationis effectum`.

**Four bounds, which must travel with it** [LIT-002]. (1) This is a search of
**two uncorrected OCR derivatives, not a reading of printed pages**; a clause
mangled identically in both scans would be missed, though the record's own note
says agreement between the two layers is the intended detector. (2) Feltoe 1896
is a **diplomatic edition printing the codex's nomina sacra and contractions**
(`Dne`, `Ds`, `Spm`, `scs`), so a search on expanded orthography can be trusted
only for clauses containing no contractible word: **the zero counts for `custodi
domine` and `concede nobis domine` are weaker than the others.** (3)
De-hyphenation was applied, which is the trap at §11.3 item 4. (4) **The
Veronense has no ordered Sunday series at all** — it is a libellus collection
running by month from April with no Advent or Lent — **so absence there is much
weaker evidence about a Sunday formulary than absence from an ordered
sacramentary would be.**

**The positive half, which no prior finding records and which is the more useful
half** [LIT-003]. The Veronense does **not** contain the 1962 Postcommunion but
**does contain, twice, the prayer-shape it uses** — `Purificent` with holy
things as subject and a second protective verb yoked to it: `tua nos quaesumus,
D(omi)ne, s(an)c(t)a purificent, et operationes suae perficiant nos pacatos` and
`Ab occultis nostris tua nos, D(omi)ne, s(an)c(t)a purificent, et ab externis
erroribus perpetua virtute defendant`. **The second is the closer, because
`purificent … et … defendant` matches `puríficent … et múniant` in both verbs'
function.** Cognate-but-distinct stock: `tuae propitiationis` occurs nine and ten
times across the two layers, against the Secret's `tuae propitiatio potestatis`;
`a noxiis` occurs once in each layer, in a fasting prayer, not in the Collect's
clause. **This places the 1962 prayer's *idiom*, though not the prayer, in the
oldest Roman euchological stratum. The claim is about diction and prayer-shape,
not derivation: nothing shows the 1962 Postcommunion was made from either, and
the purify-plus-protect pair is a commonplace of the Roman postcommunion.**
*Evidence state:* located in an uncorrected OCR layer of a registered edition,
**not verified against a page image**, and the printed page and section number
of neither `purificent` prayer were established.

### 4.8 The three orations swept against the whole declared corpus: a clean division

New this run [LIT-022]. On eleven distinctive strings after de-hyphenation and
accent stripping: **zero hits in Feltoe layer A, Feltoe layer B, Férotin's
*Liber mozarabicus sacramentorum*, Bannister's *Missale Gothicum* and Lowe's
*Bobbio Missal*; hits in Wilson 1894 (Old Gelasian) and Wilson 1915
(Hadrianum).**

**The Mozarabic, Gallican and Bobbio negatives are new** — no prior finding
records a sweep of any of them for this formulary — **and they are the most
interesting of the four, because they say the three orations belong to the Roman
euchological stream and not to the non-Roman Latin rites.**

**Bounds, all real** [LIT-022]. This is a literal string search over uncorrected
optical text, which cannot see a paraphrase, a recentonised descendant, or a
prayer whose scan is damaged; three of the four books are diplomatic editions of
manuscripts with heavy contraction, so expanded-orthography terms are weak for
any clause containing `Domine` or `Deus`; and the corpus's own note says a
prayer absent there may still be ancient. **Do not upgrade this to "these
prayers are Roman in origin". It supports only "these prayers are not in these
six editions, and are in the two Roman ones among them."**

### 4.9 Cultural afterlives: four appointed elements produced nothing

**Swept again this run in the American legal corpus and producing nothing
qualifying: the Introit, the Alleluia and the Offertory** [CUL-014]; and **no
candidate exists for any of the three composed orations** [CUL-024]. Specifics,
with the returned counts: `a day in thy courts is better than a thousand` = 0;
`how amiable are thy tabernacles` = 0; `a joyful noise` = 1, and it describes a
congregation's actual worship in a public-nuisance case — **straight description
of religious practice, not a redirection**; `the angel of the Lord encampeth` =
0; `O taste and see` = 0.

**The Epistle's two most quotable clauses produced only devotional reception:**
`walk in the Spirit` = 7 and `the fruit of the Spirit` = 6, **every located use
being religious content quoted as religious content** — a church constitution's
statement of purpose, a victim-impact statement, a prison ministry's own
curriculum quoted as evidence of its religious character, an employer's
religious-liberty pleading, and a footnote on a juror. `the flesh lusteth
against the spirit` = 0. And at the Communion, `seek ye first the kingdom` = 3
and `all these things shall be added` = 2, **of which two are the registrant's
or claimant's own religious self-description quoted by the court and neither
redirects the wording.**

**What the negatives DO support, within what was swept** [CUL-014]: **the
appointed Psalmody of this Mass barely enters secular American usage at all,
while the Gospel is detached from the liturgy and put to other work repeatedly,
in at least five distinct verses (6:24, 6:26, 6:27, 6:28, 6:29) and across two
centuries.** The Epistle enters at one clause and the Gradual at one joke.
**That asymmetry matches the four elements the manifest assigns to the
notable-and-quotable component — epistle, gradual, gospel, communion — which are
exactly the four where qualifying candidates were found; and it independently
reproduces the same asymmetry the prior brief recorded from a different
corpus. Two corpora agreeing is worth more than either alone, and it is the
strongest thing this negative supports.**

**One caution against over-reading it** [CUL-014]: the Gospel's dominance may
partly reflect that Matthew 6 is simply the most familiar chapter of the New
Testament in English-speaking countries, **not anything about this formulary's
selection.**

**What the negative does NOT cover** [CUL-014]: the American newspaper corpus,
because loc.gov cannot return a phrase count; HathiTrust and Google Books, which
refused; any British, Irish, Commonwealth, Continental or Latin-American corpus;
any non-English corpus; and any variant wording. **A phrase returning 0 there
may well be attested elsewhere, and the negative is correctable by anyone with a
working phrase index.**

### 4.10 The guide's patristic English has no pinned witness

New this run and recorded because it changes what a source correction could ever
reach [COV-004]. **The entire patristic layer this guide quotes in English was
read through New Advent pages, not one of which is a registered artifact at the
loci used**, and the repository committed a review on 2026-08-28
(`src/sources/inventories/newadvent-delivery-drift-review-2026-08-28.md`, commit
`27d359797`, an ancestor of the run commit) finding that **across all 70
registered New Advent artifacts, none now reproduces** — 61 at −3 bytes, 5 at
−2, 3 at −1, one HTTP 404 — with the cause identified as machine-rewritten page
furniture behind Cloudflare and **the translated text unaffected**. The review's
own words: "This class of drift is structurally invisible. `source-library
validate` passes clean and never re-fetches remote artifacts."

**Severity: moderate-to-high as a provenance risk, low as a text risk, and the
two must not be confused** [COV-004]. The drift review re-checked a live page
against a tracked checked transcription and found it verbatim, **so nothing
suggests the guide's quoted English is wrong.** The risk is that **for each
locus quoted there is no artifact record, no hash, no rights record and no
retrieval date, so there is nothing that could be re-checked or that a source
correction could propagate to.** Specifics: Augustine's *Enarrationes* register
artifacts for Pss. 17, 25, 51, 55, 65, 69, 77, 90, 144 — **none of the appointed
Pss. 33, 83, 94, 117**; Chrysostom's *Hom. in Matt.* holds homilies 23 and 49
while the guide cites 21 and 22; Cyril holds the procatechesis and mystagogical
1 and 4 while the guide cites V.20; Ambrose holds a passage at 47–49 while the
guide cites IX.58. **And the NPNF volumes the guide's English actually comes
from are not held as volume records either** — NPNF1-03, NPNF1-06, NPNF1-08,
NPNF1-10 and NPNF2-10 are all absent, and only Cyril's NPNF2-07 is held.
**The References sentence asserting that "the New Advent transcription of it is
registered restricted" asserts a registration that does not exist at these
loci.** The library shows the discharge pattern used elsewhere for exactly this
problem — a small tracked checked-text artifact beside the restricted or remote
delivery, as at Honorius `iv.65-68-checked-text` and Guéranger
`vol-xi-p-271-checked-text` — **and it was not used here.**

**The cheapest substantive upgrade available to the patristic layer** [COV-005].
**Migne PL 37 is registered as a complete hashed public-domain volume**
(`internet-archive-google-pdf-afe6878f`, sha256 `afe6878f…97bb4`, 481 pages,
retrieved 2026-08-21, with artifact PDF p. 63 already rendered and read for
Augustine's Ps. 88), carrying the *Enarrationes* on **Pss. 80–150**; and the
cross-work segment mechanism that reaches Augustine inside it is already built
(`…/segments/psalm-88-columns-1139-1140.toml`, `…/passages/88-sermo-ii-12.toml`).
**Pss. 83, 94 and 117 all fall inside that range, so three of the guide's four
Augustine psalm loci are collatable in a volume this repository already holds,
at public-domain rights, by a route already proven.** **Ps. 33 is in PL 36,
which is not registered in any form, so the fourth locus stays where it is.**
Two cautions: this would raise the Latin from unregistered corroboration to a
collated witness **but would not change the published English, which is and
should remain NPNF's**; and the Latin transcriptions the guide currently
corroborates from are outside the library entirely, **so at present nothing pins
the corroboration either.**

### 4.11 Binding coverage, and the one place where it has a live rights edge

**Nine sources the guide actually uses are registered here — three of them with
verified passage records at the loci used — and none is bound in
`research/source-bindings.toml`, whose header states as uniform a condition that
is false for at least Anthony of Padua** [COV-006]. **Anthony has three passage
records all at states `[cataloged, acquired, inspected, verified]`, verified
2026-08-21, one of them recorded as closing "by relating the return to the fruits
of the Spirit in Galatians 5:22-23" — the appointed Epistle.** So the header's
"none of its witnesses has a passage record here at the loci used" is false as
written. Wilson's two sacramentary editions and Guéranger have passages at other
loci in artifacts the guide read at its own loci; **Honorius and Aquinas *Super
Galatas* have artifacts registered complete over the loci used, needing only
passage records**; and the 1604 Missale Romanum is `storage='tracked'`,
`indexable=true`, **the only one of three unbound missals that could carry a
replayable receipt.** **This is a binding-coverage gap, not an evidence gap: in
every case the guide's own account of what it read is accurate.**

**Its live edge** [COV-007]. The guide **reproduces Anthony of Padua's Latin
verbatim** from an artifact registered `storage='restricted'`,
`rights_status='restricted'`, **whose own three passage records each carry the
instruction "Paraphrase the modern delivery and apparatus unless a separately
lawful checked transcription is supplied" — and no such transcription is
registered**, the edition holding exactly one artifact, the restricted PDF. **The
comparable cases in the library each do have one** (Honorius, Guéranger).
**And no gate can see any of this**, because `check-content-preflight`'s
`check_restricted_not_reproduced` iterates only over `bound_sources(leaf)` and
its own docstring says so: "the rights of an artifact nobody recorded cannot be
read from a record that does not exist." **The bindings file has 24 bound
sources, the single restricted one being the NABRE Galatians introduction
passage; Anthony, Honorius, Aquinas *Super Galatas*, Cassiodorus CCSL 98 and the
Corpus Orationum entry are all registered restricted and all unbound.**

**This lane is not making a rights determination and neither is this brief**
[COV-007]. The guide's own argument is coherent and stated plainly in its
References and commentary: Anthony's thirteenth-century Latin is public domain
by age, the modern apparatus is restricted, only the former is quoted, the
latter is paraphrased, and no bytes were retained. **That argument is very
likely right.** The finding is that **it is asserted only in prose, while the
library records the same judgement as a condition to be discharged by an
artifact, and the artifact that would discharge it exists for the two comparable
witnesses and not for this one.** **The practical consequence is the invisible
one: the restricted-not-reproduced check passes on 24 sources without ever
examining the one restricted artifact the guide quotes at length.**

### 4.12 The blanket statement about replayable search receipts is wrong for its strongest half

[COV-008]. The bindings file states that no negative-search binding appears
because the searches "ran over optical layers that are not registered as
indexable, so no replayable search receipt exists for any of them." **That is
right about a real and important subset** — the sacramentary OCR layers, the
Benziger text layer, the Migne and Centro Studi facsimiles and the Corpus
Orationum entry are all `indexable=false`, and that covers the Veronense and
sacramentary negatives of §4.7 and §4.8. **It is wrong as a blanket.** The
Pustet Ratisbon 1862 artifact is `storage='tracked'`,
`rights_status='public-domain'`, `indexable=true`, 2,503,914 bytes; so are the
Venice 1570 and Vatican 1604 texts; and across the two Bible works bound as
controls, the Douay–Rheims artifacts run 154 indexable against 1 not, and the
Clementine 82 against 12. **`guidance/sources.md` accepts a negative-search
binding over exactly that condition and validation replays its zero-result
receipt.** **None of the published negatives is called into doubt by this; what
is at stake is whether the strongest of them can be pinned as the library
intends rather than resting on prose. The correct form of the sentence
distinguishes the two halves.**

### 4.13 Bounded negatives internal to the formulary

Each bounded to the ten appointed elements as printed, and nothing wider
[SCR-022, SCR-030, THE-041, THE-043, THE-050, with the prior run's THE-025 as
restated at [SCR-001]]:

- **The Holy Spirit is named in exactly one element.** `Spiritu-` occurs five times in the Epistle and nowhere else; the three orations never name the Spirit. **This must be stated with its bound or it is simply false**: the printed rubric appoints the Preface of the Most Holy Trinity, so the Mass *as celebrated* names the Spirit. The negative is about the proper, and it bounds how far a Spirit-centred reading can be pressed.
- **The only law-vocabulary in the formulary is two clauses of the Epistle, and both are negative** — `non estis sub lege` before the vice-list and `Adversus huiusmodi non est lex` after the fruit-list, so law brackets the two catalogues [THE-041]. **This is confined to one element, fails the two-element floor, and may not be published as an interpretive proposal** (§9.8). It is Paul's own frame in Galatians 5 and the missal took the pericope whole.
- **`Adversus` occurs four times, all in the Epistle**, and the fourth reverses the sense of the first three [THE-043]. **Same disposition: one element, no proposal.**
- No parousia, resurrection or judgment vocabulary beyond the Epistle's `regnum Dei non consequentur` and the Postcommunion's `perpetuae salvationis`.
- No saint named and no Marian reference. One angel named, in the Offertory, and no other created spirit.
- No penitential, fasting or almsgiving language, despite a seventeen-item vice list.
- The Church is named **once**, in the Collect — though the first-person plurals of Introit, Alleluia, Secret and Postcommunion are corporate in their own way, which softens any contrast built on it.
- **The Communion antiphon contains no eating vocabulary at all** [THE-042]: `gust-` occurs once and is in the Offertory; `manduc-`/`esc-` occur only in the Gospel.

### 4.14 The method bound on the theological sweep

[THE-044]. That sweep was **mechanical and corpus-internal**: per-element stem
counts over the ten appointed elements and accent- and whitespace-normalised
string sweeps over **21 collated `propers/verified.md` records covering 15
distinct 1962 Roman formulary identities** (claude 48, 49, 51, 52, 53, 54; gpt
m01, 39, 41, 43–54). **It retrieved no new source, opened no patristic or
liturgical work, and therefore establishes nothing in the third claim class.**
The prior run cited "twenty collated records"; **the count is now 21, so a
repetition will not reproduce that denominator.** Specifically **not** swept and
therefore open: any 1962 formulary this repository has not collated, which is
most of the missal; the Pustet 1862 and Benziger OCR artifacts; any concordance
over the orations of the whole missal; any non-Roman rite. **The records swept
are themselves audit records, not page images, so a sweep over them is evidence
about those records and not about the missal.**

---

## 5. Rejected and unresolved leads

| Lead | Status | Why |
|---|---|---|
| Catena excerpts under **Hilarius and Hieronymus** on the appointed Gospel | **NO LONGER LEADS — checked** | Every one was cross-checked sentence by sentence against the independently retrieved underlying works and reproduces them faithfully [PAT-140]. **The check was against the same Migne recensions the Catena drew on, not against critical editions**, so it establishes faithful transmission and not the Migne text's correctness |
| Catena excerpts under **Gregorius, Rabanus, Remigius, Glossa** | **Unverified leads. Must not be cited from the Catena** | Underlying works not opened [PAT-140] |
| Every `Chrysostomus super Matth.` excerpt in the Catena | **Rejected as Chrysostom** | It is the *Opus imperfectum*, universally rejected as his; the identification rests on the citation formula and the *Opus imperfectum* was not retrieved in its own right [PAT-140, PAT-402] |
| **Aquinas's *Super Matthaeum* ascribing the lilies-as-angels reading to Jerome** | **REJECTED as Jerome; it is Hilary's** | The Catena attributes it correctly to `Hilarius in Matth.`, and Jerome's own commentary argues against the move in kind at v. 26. **Report it as a misattribution in a *reportatio*, not as an error of Thomas** [PAT-133] |
| Origen on Gal. 5:13 and 5:24 | **Checked report of an unchecked source** | Reaches this brief entirely through Jerome; the Greek was not opened, **and no claim about Origen's own text may be published from this alone** [PAT-155, PAT-156]. **Jerome himself partly withdraws from the reading he transmits** |
| Remigius on the birds and lilies | Unverified lead | Reaches this brief only through the Catena [PAT-141] |
| Augustine, *De haeresibus*, on the Euchitae | **Still an unverified lead, and the medieval agreement does not close it** | Aquinas independently names `Euticharum` in *Super Matthaeum* [PAT-132], which shows the medieval tradition makes the same identification and nothing more. **No claim that Augustine names the Euchites may be published as checked** |
| Aquinas's citation of *De civ. Dei* XIV.2; Cyprian's *De zelo et livore*; Augustine's anti-Pelagian books | Unverified leads | Named inside works that were read; none opened [PAT-402, PAT-159, PAT-212] |
| Anthony's inner quotations from the Gloss and Isidore | Unverified leads | Prior run, restated. **Attribute to Anthony's use** |
| **Whether Anthony drew `idolorum servitus` = avarice from Eph. 5:5 or Col. 3:5** | **Not established and must not be asserted** | The scriptural warrant for the gloss is now documented [SCR-027]; the dependence is not, and establishing it would require reading his sermon for that purpose |
| Guéranger's report that the antiphon is absent from Tommasi's manuscripts | **Checked report of an unchecked claim** | Prior run, restated. Attribute to Guéranger; **do not restate as established chant history** |
| Hesbert, *Antiphonale Missarum Sextuplex* | **Unavailable** | The instrument that would date the Communion substitution; **registered at catalog level only, with no artifact, and it is the only chant book registered anywhere in the library** [LIT-018, LIT-027, COV-010] |
| **The origin of the +2 offset** | **RESOLVED — this run closes the prior brief's principal unresolved lead** | Wilson states it himself in his Introduction, pp. lxxi–lxxiii: Book III's Sunday series begins at what R and S call the seventh Sunday after Pentecost and what the Gregorian text calls the sixth. **The whole displacement is a difference in where each tradition starts counting, and nothing inside the run produces any part of it** [LIT-010]. See §6.1 |
| **How the two units of offset decompose** | **Unresolved, and narrower than before** | Wilson names the `post Pentecosten` / `post Octavas Pentecostes` equivalence as a discrepancy **inside Muratori's own Gregorian text**, and which single Sunday each of the three traditions counts as its first was not established [LIT-010] |
| Which recension of the Postcommunion is prior | Unresolved | Nothing read bears on the direction of the adaptation [LIT-014] |
| **`Deus` against `Domine`, and `perpetuae` against `perfectae`, in the Postcommunion** | **Two attested variant axes, neither settled** | `Deus` at Wilson p. 237, Gerbert at the Sunday and 1962; `Domine` at Wilson's Andrew Vigil and Gerbert's Marian series. `Perpetuae` everywhere but Gerbert at the Sunday, which reads `perfectae` — **which may well be a compositor's or optical error and is a lead**, no page image having been checked [LIT-014] |
| **`Maiestatis` against `potestatis` in the Secret** | **UPGRADED from a lead to a documented reading, and it tracks the assignment** | Two different critical editions of two different books both print `tuae propitiatio MAIESTATIS` at the same Lenten station Mass — Monday of the fifth week of Lent, *ad Sanctum Chrysogonum* — while both print `potestatis` where the same prayer serves the Sunday [LIT-024]. **Bound: still OCR readings, on three optical layers of two books, no page image collated; but three layers of two independently edited books agreeing on an unusual word is far past what an optical error explains.** *Not* established: which reading is prior, whether the two are one prayer or two, and whether either bears on Cummiskey's "Majesty" — **recorded as a checkable coincidence and no claim made about it**, the 1861 book's Latin not having been read |
| **Which oration-section each Ottobonianus cue block attaches to** | **LIVE DISAGREEMENT — see §6.8** | The prior run's page-image reading and this run's optical reading differ, **and the page image controls** [LIT-025] |
| Ottobonianus cue `b` reading `Bonum est confidere` where 1962 gives the Fifteenth Sunday `Bonum est confiteri` | **Observed, not interpreted — and stronger than recorded** | **Both** block (a) and block (b) read `Bonum est confidere`, so **a shared respond across two consecutive Sundays is a better explanation than a copying error**, though this sweep still cannot decide [LIT-025] |
| Block (a)'s Alleluia reading `Iubilate Deo` and not the 1962 Fourteenth's `Venite exsultemus` | **Observed, new, and nobody has recorded it** | A third displaced element in that cue block [LIT-025] |
| Whether Honorius's Ember week and Wilson's interpolated Masses are the same disturbance | **Lead only** | Prior run, restated. The two witnesses number their Sundays differently |
| The identity of the compiler of the Gregorian supplement | Unresolved | Wilson attributes it to Alcuin; the modern reattribution rests on scholarship not registered here. **The compiler stays unnamed** |
| Whether Mt. 21:42–43's convergence bears on this formulary | **REJECTED, emphatically — and the prior brief's number is corrected** | Mt. 21:42 quotes Ps. 117:22 and Mt. 21:43 is one of Matthew's four `regnum Dei` verses and uses `fructus`; but the appointed Gradual is Ps. 117:8–9, and **the distance is THIRTEEN verses from v. 9, not the nine the prior §5 states** [SCR-018]. **The rejection is unaffected and is if anything strengthened; only the number was wrong, and wrong in the direction of understating the distance.** It is a fact about Matthew 21, not about this formulary |
| Whether Heb. 13:6's verbatim quotation of Ps. 117:6 bears on the Gradual | **Flagged inference, offered only as such** | Hebrews quotes v. 6, which the Gradual does **not** appoint [SCR-025]. Heb. 13:5's warning against avarice is thematically close to this Gospel and **nothing in the appointed texts points to Hebrews** |
| Whether 1 Pet. 2's use of two of this Mass's psalms is one relationship | **REJECTED as one relationship; carried as two, with the asymmetry stated** | 1 Pet. 2:3 quotes appointed wording and is a real relation to the Offertory; 1 Pet. 2:7 quotes Ps. 117:22, thirteen verses outside the appointed Gradual. **Reporting the two halves as one would manufacture a connection the appointed texts do not make** [SCR-032] |
| Whether Is. 40:6–8's `caro`/`foenum`/`gloria` convergence bears on the formulary | **Flagged inference, not asserted** | Isaiah 40 is not appointed and nothing in the ten elements points to it [SCR-031] |
| Whether the Gospel's `clibanum` carries the wrath-resonance of its Old Testament occurrences | **Rejected as Matthew's sense** | A fact about the word's distribution and not about Matthew, whose use is plainly domestic [SCR-031] |
| Whether the appointed Gospel is meant to be heard against the Our Father | **Flagged inference** | Matthew supplies the proximity; nothing in the appointed formulary points to it [SCR-010] |
| Whether the Alleluia's single verse carries the whole psalm's warning | **Flagged inference** | The formulary appoints v. 1 and no more [SCR-014] |
| Whether Lk. 1:47 echoes Ps. 94:1 | **Not settled and cannot be here** | No Greek psalter is held, so the shared Greek behind the shared Latin could not be checked [SCR-029] |
| The Ps. 33:10–11 / Mt. 6:32–33 parallel | **Flagged inference, with a counter-indication** | Similarity of argument, not wording; the shared verb is used with **opposite valuation** in the two places [SCR-017] |
| The temple-dedication Solomon of 2 Par. 6:42 against the Gospel's Solomon | **Flagged inference, not asserted** | Joined by nothing in the appointed texts [SCR-026] |
| Whether the Greek psalter reads χρηστός at Ps. 33:9 | **Lead, well supported and not closed** | Brenton evidences the sense and not the word; **closing it costs one registration of a Greek psalter** [SCR-024] |
| Whether the appointed psalm wording is Gallican, Roman or *iuxta Hebraeos* | **Unanswerable in this repository** | No psalter recension of any kind is registered and no chant book was consulted [SCR-021, SCR-033(b)] |
| Whether the three orations contain loose scriptural **echo** | **Untested and no claim either way** | The negative at §1.1 is bounded to **direct quotation** only; **no search for echo was run**, and the profile expressly warns against mislabelling loose echoes as direct quotations [SCR-033(d)] |
| The `dicit Dominus` tag's expressiveness | Untested | A common formulaic tag; the count over other communion antiphons was not run |
| **`Circuit` / `in circuitu`, the Third Sunday's devil against this Offertory's angel** | **REJECTED by its own lane and by this brief** | Different formularies, a common Latin verb and preposition, no liturgical relation: a coincidence [THE-038, THE-050] |
| **The Gospel's six clothing terms against the Epistle's crucified flesh** | **Not pursued** | Nothing in the other nine elements shares the vocabulary and the join is thematic only; **no mechanism worth stating was found** [THE-050] |
| **`Unus`/`una` across Gospel and Introit** | **Rejected** | No semantic relation; **numerology without textual control, which the profile rejects** [THE-050] |
| Nkrumah's own first utterance of the political-kingdom motto | **Not acquired, and the bound stands** | *Ghana: The Autobiography* is lending-restricted with search-inside closed; HathiTrust 403, Google Books 429. **The claim is bounded to circulation and reception, never coinage** [CUL-001, CUL-023] |
| **Carlyle's "Gospel of Mammonism"** | **REFUSED on strength — and it is the single most tempting literary lead for this formulary** | The whole verbal link is the one word `mammon`. A grep of the complete *Past and Present* for `two masters`, `God and Mammon`, `serve God`, `lilies`, `toil not`, `little faith` and `take no thought` returns nothing but one unrelated "two Masters of the Vestry"; and `Mammon` personified as a devil long predates Carlyle and is as available from Luke 16 as from the appointed Matthew [CUL-023] |
| ***Sacred Heart Academy v. Karsch*** (Tenn. 1938) | **Borderline; returned as a lead only** | The court quietly **reverses the direction of the appointed verse** — Matthew promises the material things will be *added* to one who seeks the kingdom, and the court reasons that to gain the kingdom one must first *supply* them. **A genuine turn**, but performed in the service of straight doctrinal reasoning about the religious life, which the gallery rule excludes, and reached by importing Matthew 25 rather than by working on the appointed wording. **Anyone minded to use it must argue the point rather than assume it** [CUL-023] |
| The three Psalm 146 cases and six of the nine `fowls of the air` cases | **REFUSED on identity** | Psalm 146 is a flat prohibition where the appointed Gradual is a comparative; six of the nine `fowls` hits are Genesis 1:26 [CUL-019, CUL-021] |
| `serve God and mammon` (22 opinions), the five later Wallingford citations, and the variants `a cubit to his stature`, `one cubit to his stature`, singular `fowl of the air` | **Unexhausted, and said to be so** | Each is a cheap and bounded piece of work for a later sweep [CUL-023] |
| The pin cite of *McLean v. Arkansas* | **Not settled** | The Caselaw Access Project record is internally inconsistent — official citation 529 F. Supp. 1255, first page recorded as 1249, the lilies passage at page label 1265. **The star page must be checked against a reliable reporter before a pin cite is printed**; the structural locus is safe meanwhile [CUL-016] |

---

## 6. Competing historical judgments preserved

### 6.1 The displacement: the claim, the corrections, and the bound

**The claim, materially widened and in two places corrected against the prior
brief.**

**(a) The run is sixteen consecutive sections, not eleven, and Menard tracks
R/S/Gerbert throughout** [LIT-009]. Wilson's Book III sects. I–XVI were read in
one pass in both registered OCR layers. **Sects. I–XI stand at N+2 for
R/S/Gerbert and Menard and N+1 for Pamelius; sects. XII–XVI stand at N+4 for
R/S/Gerbert and Menard while Pamelius stays at N+1 without a break.** **That
makes the pattern stronger than the prior brief reports, because the offset
survives a documented interpolation and resumes a new constant rather than
becoming noise.** Menard is present at every section readable and **always
agrees with R/S/Gerbert and never with Pamelius**; prose pairing Menard with
Pamelius because both are Gregorian editions would be wrong.

**A caution the prior brief did not carry** [LIT-009]: **Wilson's per-section
wording varies in scope** — sect. IX excepts the Secret, sect. V excepts the
Postcommunion, sect. VI covers "the two Collects and the Secret", sect. XII
covers "the first Collect, Secret, and Postcommunion". **The OFFSET is uniform
while the SET of prayers it covers is not. Do not flatten that.**

**(b) The origin of the offset is resolved, and Wilson states it himself**
[LIT-010]. Introduction, printed pp. lxxi–lxxiii: "With the seventh Sunday after
Pentecost in R. and S., or the sixth Sunday after Pentecost, according to
Muratori's text, we reach a set of missae corresponding on the whole to the
first part of the series contained in the third book of V." **Combining that
with the identification of Book III sect. I as the 1962 Fifth Sunday gives
R/S = 1962 + 2 and the Gregorian = 1962 + 1 arithmetically, with no residue: the
offset is a numeration base, not an interpolation.** Wilson names the mechanism
in a footnote — the `post Pentecosten` / `post Octavas Pentecostes` equivalence,
"a discrepancy between the first and the supplementary portions of Muratori's
text in regard to the numeration of the Sundays after Pentecost" — and describes
what R and S insert before reaching the series. **What remains open and must not
be overstated:** which single Sunday each of the three traditions counts as its
first was not established, so **the decomposition of the two units of offset
between the Octave question and R/S's inserted missae is not settled here.**
**The break at sect. XII is now doubly sourced** — Wilson's Introduction and his
footnotes agree that R and S insert the two September Ember-week Sundays and
rejoin Book III at their twentieth.

**(c) The Gregorian Hadrianum carries ALL THREE orations as one Mass, so the
prior brief bounded its own claim more tightly than the evidence required**
[LIT-023]. At section CXXXIII, "DOMINICA .XV. POST PENTECOSTEN", printed
pp. 173–174: Collect `Custodi domine quaesumus ecclesiam tuam propitiatione
perpetua…`; Super oblata `Concede nobis domine quaesumus…`; **Ad complendum
`Purificent semper et muniant . tua sacramenta nos deus . et ad perpetuae ducant
salvationis effectum` — the 1962 Postcommunion word for word, including `deus`
and `perpetuae`.** The next section opens with the 1962 **Fifteenth** Sunday's
Collect, confirming N+1 at the following section too. Wilson's index of
liturgical forms lists that Postcommunion at p. 174 as **its only occurrence in
the volume.**

**The prior §0.3(b) reasoning is sound as far as it goes** — Wilson's Gelasian
footnote at Book III sect. X does cover only the Collects and Secret, and
sect. X does print two other Postcommunions — **but that is a fact about the
Vatican manuscript's Book III and not about the Gregorian book.** Combined with
Gerbert's *Dominica XVI*, which also has all three, **the position is: in BOTH
traditions the whole 1962 oration set travels as a unit, at N+1 in the Gregorian
and N+2 in the Frankish Gelasian, and the narrow attestation is peculiar to how
the Vatican manuscript arranges its unassigned Sunday Masses.** **The prior
one-sentence form's clause "the assignment covers only two of the formulary's
ten elements" is therefore not right and must not be reproduced.**

**(c2) What Wilson's footnote at sect. X actually covers, and the two halves of
it prose must keep together** [LIT-007, LIT-008]. **His "The Collects" is a
plural and means both collects of that section**: sect. X prints five prayers,
and the unit that moved in the older books is a Mass-set of **three orations
plus, in Gerbert, a proper Preface** — of which only two are elements of the
1962 formulary. **Prose that says "two elements moved" is right about 1962 and
wrong about the transmission; prose that says "the Mass moved" is right about
the transmission and overstates 1962. Both halves are needed**, and the 1962
formulary is what survives of that set after the second orations were abolished
(§2.8).

**And the near-miss at sect. X's Postcommunion is a near-miss of a particular
kind** [LIT-008]. The prior brief is exactly right that neither of sect. X's two
Postcommunions is the one 1962 prints. What is worth adding is that the
bracketed one reads **`Purificent nos, Domine, sacramenta quae sumpsimus, et a
cunctis efficiant vitiis absolutos`** — **a different prayer of the same incipit
family** — and that **Wilson's own index of incipits lists two distinct prayers
separately**, "Purificent nos Dne. sacramenta, 230, 253, 356" and "Purificent
semper et muniant, 207, 237, 355", **three printed occurrences each. A search on
the incipit alone will conflate them**, which is the same species of trap as the
shared `Protector noster` incipit, one book further back (§11.3 item 3). Wilson
also records that the Vatican manuscript **wrongly titles that prayer
`Secreta`**, "but its contents show that this is an error of the scribe".

**(d) One of the five books is now open at the locus** [LIT-011]. Gerbert prints
at his printed p. 173, under the heading **"Dominica XVI. post Pentecosten"**, a
five-item Mass whose Collect, Secret **and** Postcommunion are the three
composed orations of this formulary, plus a second Collect and a proper Preface
(§2.8). **What raises confidence well above ordinary OCR:** the printed page
number 173 matches Wilson's independent marginal citation "Gerb. 173"; **the
five incipits match Wilson's independent Appendix tabulation at p. 355 item for
item and in order**; and two independently produced digitisations agree
verbatim. **What it changes: the displacement is no longer a claim resting
entirely on one editor's apparatus, because Gerbert's own printed section
heading now says it.** **What it does not change: Rheinau, S. Gallen, Pamelius
and Menard remain unopened, and Gerbert is the LEAST independent of the five**
(§6.2).

**(e) The section-to-Sunday mapping is independently checkable and it checks
out** [LIT-019]. Wilson's Book III sect. XI prints the 1962 **Fifteenth**
Sunday's Collect (`Ecclesiam tuam, Domine, miseratio continuata mundet et
muniat…`) and sect. IX the **Thirteenth**'s (`Omnipotens sempiterne Deus, da
nobis fidei, spei, et caritatis augmentum…`), with sect. X printing this Mass's,
**exactly as the mapping of sects. I–XI to 1962 Sundays 5–15 requires**, checked
against `src/sources/calendars/roman-1962/propers.yaml`. **This matters because
the displacement is an arithmetic claim and arithmetic on a misaligned mapping
would be worthless.**

**The bound, and it must travel with all of the above** [LIT-011, LIT-016,
LIT-026, LIT-027]: **four of the five books remain unopened** (§4.6); Gerbert is
read in **uncorrected OCR of eighteenth-century long-s type with no page image
collated**, and the two digitisations, while independently produced, are of the
same edition and possibly of related scans; **this whole lane is an optical-text
lane and every "confirms the prior run" is a corroboration from a weaker
evidence state**; and Honorius's Fourteenth Sunday agrees with 1962 in four
elements and differs in four (§6.3).

**The one-sentence form a later writer should not simplify past, restated for
this run:** *the three composed orations of this Mass stand two Sundays later in
the Frankish Gelasian books and one Sunday later in the Gregorian, uniformly
across sixteen consecutive sections, on a published critical collation two of
whose manuscripts the editor read himself and one of whose printed witnesses has
now been opened at the locus — and the offset is a difference in where each
tradition begins counting rather than an interpolation, four of the five books
are still unopened, and the rest of the formulary was assembled on a different
schedule again.*

### 6.2 The books agreeing on the sixteenth Sunday are not independent witnesses

**Every one of the prior brief's four corrections to how Wilson has been quoted
about Gerbert is confirmed verbatim this run** [LIT-016], and one of them bounds
this run's own largest find. Wilson, p. xx: "it seems almost ungrateful to
criticise the method and execution of a scholar of the last century, to whom
students of Liturgy owe so much as we owe to Gerbert. But it must be said that
his text is one which requires to be used with caution … and that his mode of
handling his materials, and of explaining what those materials were, is **at
times** exceedingly confused and misleading." **Quoting the phrase bare
overstates Wilson.** Wilson, p. xix note: Gerbert's third principal manuscript
T, *Sangallensis olim nunc Turicensis*, "cannot now be traced". And: "the
'Gelasian' portions of the 'triple text' of T. (and therefore of Gerbert's
printed text) do not represent the original text of the 'Gelasian' books, but a
revision of that text, apparently based upon the text of the Sacramentaries of
the 'Gregorian' type".

**So opening Gerbert proves that Wilson cited him accurately and does not add a
fourth independent manuscript voice** [LIT-016]. **The honest count is
unchanged:** two Frankish Gelasian manuscripts Wilson collated himself, plus a
printed edition dependent on a lost manuscript revised toward the Gregorian
type, plus one Gregorian edition (Menard), with the other Gregorian edition
(Pamelius) at the fifteenth. **What IS changed is that a Gerbert mis-citation is
now excluded, which was one of the live ways the pattern could have been an
artefact.** **And the caution in the other direction still holds: R's and S's
own Sunday headings are Wilson's own collation and do not depend on Gerbert at
all.**

**One dependence prose must not double-count:** the Gregorian numbering and
Pamelius's N+1 in Wilson's Gelasian apparatus **agree because Pamelius is an
edition of the Gregorian book. They are not two independent witnesses to N+1.**
**And Gerbert's second Collect and proper Preface are a feature of R and S as
against the Gregorian**, so their presence in his Dominica XVI is **further
evidence of his dependence on the Frankish Gelasian side and not a third
independent voice** [LIT-012].

### 6.3 Honorius's Fourteenth Sunday is not the 1962 Fourteenth Sunday — and his divergences are one fact, not three

**Not reopened this run.** Every statement about Honorius here is taken from the
prior run's page-image reading of *Gemma animae* IV.72, PL 172 cols. 717–718, as
the prior brief reports it, **and if that report is wrong this section inherits
the error** [LIT-017, LIT-027].

By the early twelfth century the 1962 Sunday number and this Introit are already
paired: the chapter is headed "Dominica decima quarta post Pentecosten
« Protector noster, » sub lege". **But within one and the same chapter his
Introit, Collect, Epistle and Offertory are the 1962 Fourteenth Sunday's, while
his Gospel is the 1962 Thirteenth Sunday's** (Luke 17:11–19, the ten lepers).

**What this run adds, and it changes the shape of the claim** [LIT-017]. His
three differing chants are **not** three separate facts. Collated against
`src/sources/calendars/roman-1962/propers.yaml`, **his Gradual (`Bonum est
confiteri Domino`, Ps. 91), his Alleluia (`Quoniam Deus magnus`, Ps. 94:3) and
his Communion (`Panis, quem ego dabo`) are precisely the 1962 FIFTEENTH Sunday's
chant set.** So **in one chapter his chant strand stands one Sunday later than
his oration strand while his Gospel stands one Sunday earlier: a spread of
exactly two Sundays.**

**That converges in DIRECTION, though not in magnitude, with the Ottobonianus
cues** (§6.8), where the chant set beside `Custodi, Domine` also runs later than
the orations: **two independent witnesses in which the chants of this Mass run
later than its orations. Bounds: one is +1 and the other +2, so they do not
corroborate a single number**; and the 1962 side of this collation rests on the
calendar registry rather than on a facsimile collation, **so prose should say
"as the tracked 1962 registry records" and not "as the missal prints" unless
someone collates pp. 396–398 of the typical edition** [LIT-017, LIT-018].

**Why this matters to the whole question:** the earlier books do not simply carry
the 1962 formulary under a different number. **Different strands — orations,
chants, Gospel — were numbered and paired independently and settled at different
times, and prose reporting "this Mass stood at a different Sunday" as one clean
fact will be reporting something no witness actually says.**

*A caution on the printing, carried from the prior run:* in Migne's text the two
parenthetical references in the Gradual and Gospel sentences are **transposed**.
**A reader taking either at face value from that column will be misled.**

### 6.4 Four readings of `respice in faciem Christi tui`, and they do not stack

Augustine christological-missionary; **Cassiodorus the same, formalised as
hypallage** [PAT-206]; **Theodoret ecclesial, the face of Christ being the saved
people, on 1 Cor. 12:27, read in Greek** [PAT-301]; Guéranger inward and
nuptial, on 1 Cor. 11 and Eph. 5. **Not reconcilable by stacking. Preserve all
four**, and note that the third **removes the ground for treating the
inward-ecclesial reading as a nineteenth-century departure from the Fathers**,
while being on a different Pauline text and without the nuptial figure, so it
corroborates neither Augustine nor Guéranger. See §2.1.

### 6.5 Four accounts of the two lists' asymmetry

The prior run's THE-020, an open-vice-list reading; **Augustine reading both lists as open on the
missal's own word `huiusmodi`** [PAT-102]; **Origen through Jerome, that the
works are called *manifest* and the fruit is not, so the fruit must be sought
with labour** [PAT-156]; **Chrysostom, that evil works come from us alone while
the good need God's kindness too** [PAT-313], against **Jerome's own different
reason, that vices end in themselves while virtues sprout and overflow**.
**Four accounts of one feature of the appointed text is the sweep's richest
single vein and the author must not flatten it.** See §2.2.

### 6.6 The Latin tradition divided on allegorising the Gospel's images

Hilary allegorises throughout and argues that the literal sense fails; Jerome
forbids it on a ground internal to the appointed verse; Augustine forbids it;
Remigius allegorises but reaches this brief only as a lead. **Preserve the
disagreement; do not adjudicate it.** See §0.3(c) and §2.5.

### 6.7 Two accounts of `iubilare`, one Greek and one Latin

Cassiodorus's wordless jubilus against Theodoret's shout of victors. **They
disagree about what the one word the Alleluia contributes means**, and it is the
most interesting thing the sweep found about the element the prior brief called
the least integrated. See §2.4.

### 6.8 A live disagreement about the Ottobonianus cue attachment, and the page image controls

**This is the run's one unresolved conflict between a lane and the prior
production, and it is preserved rather than settled** [LIT-025].

**What is now fixed with certainty, and is not in dispute:** Wilson 1915 prints
three consecutive cue blocks at pp. 173–174 —
(a) `Ant. Protector noster. Resp. Bonum est confidere. Off. Inmittit angelum.
Com. Panis quem ego. All. Iubilate deo.`;
(b) `Ant. Inclina domine aurem. Resp. Bonum est confidere. Off. Expectans
expe(ctaui). Com. Qui manducat. All. Domine deus salu(tis).`;
(c) `Ant. Miserere mihi domine quoniam. Resp. Timebunt gentes. Off. Domine in
auxilium me(um). Com. Domine memorabor. All. Laudate dominum.`
**Against the tracked registry these are the 1962 Fourteenth, Fifteenth and
Sixteenth Sundays' chant sets in that order, with two Communions displaced**;
block (c) matches the 1962 Sixteenth in all four checkable elements.

**What is in dispute:** which oration-section each block attaches to. The prior
run, **reading the footnote reference marks on page images**, placed the cue set
beside `Custodi, Domine` as the 1962 **Sixteenth** Sunday's, an offset of +2.
This run's optical reading places block (a) at section CXXXIII, whose Collect is
`Custodi domine`, **which would make the cue offset zero.**

**The lane's own disposition, which this brief adopts:** *"I am NOT correcting
the brief here and the disagreement must not be resolved in my favour. The prior
run read the footnote reference marks on page images; the marks are exactly what
an optical layer destroys, and my placement is an inference from adjacency in a
text stream that also reorders marginal columns. The page image controls and
someone must go back to it."* **The prior run's reading stands, and this
disagreement is printed rather than harmonised.**

**What survives either reading, because it is a fact about block content and not
about attachment:** the cue set whose Introit is `Protector noster` — this
Mass's own Introit — has Communion **`Panis quem ego`** and **not** `Primum
quaerite`. **That is the second witness to the same thing after Honorius (§6.3),
and it materially strengthens C5** (§7.5).

### 6.9 The Ambrosian rite reads this Gospel's material penitentially and split

Comparative evidence the prior corpus boundary excluded by construction, and it
is bounded severely [PRE-014, PRE-005]. The Ambrosian missal (Milan de Sirturis
1712) appoints Mt. 6:22–26 and Mt. 6:27–33 as **two consecutive Lenten ferial
pericopes in the second week of Lent**, splitting the Roman Fourteenth Sunday's
pericope at exactly v. 26/27; **it keeps both occurrences of `adicere` inside a
single lesson**; and it pairs the second with **the Judgment of Solomon
(3 Kings 3:16–28) as its Old Testament lesson**, with the psalmellus `Conserva
me Domine quoniam in te speravi` between them and an Ambrosian-only *Oratio
super sindonem* closing each.

**Its force is comparative and bounded.** It shows that another Latin rite reads
the same Sermon material penitentially and split, not as a green Sunday's whole
argument, and that its lectionary makes a Solomon-to-Solomon join across lesson
and Gospel that the Roman book does not make. **Severe limits, all the lane's:**
(i) evidence state is **searched OCR only**, the ferial headings around the
locus are badly recognised, and **the exact feria was NOT established** — the
two pericopes sit in the second week of Lent and are consecutive, and which
weekdays is unknown; (ii) the 1712 printing is an eighteenth-century Ambrosian
book with 1733 Masses bound in, **so it is evidence about that book and not
about the medieval Ambrosian lectionary**; (iii) the Ambrosian 1499 text cannot
corroborate anything (§3.5); (iv) **whether the Solomon pairing is deliberate is
exactly the kind of claim about a compiler the profile forbids without a
witness. The checkable fact is the adjacency. A worker must state it as
adjacency and must not call it design.** And **no Triptych document anywhere
uses a non-Roman Western rite as comparative evidence for an appointed text**,
so this form is unprecedented in the collection as well as new to this leaf.

### 6.10 Two answers to the same objection about the Epistle's list; two middle terms in the same a fortiori

Chrysostom argues from moral choice against nature; Aquinas from Augustine's
*De civ. Dei* XIV.2. **Preserve the difference; do not report a single
patristic-scholastic consensus.** And Augustine grounds the *a fortiori* in the
**rank** of the creature where Chrysostom grounds it in its **vileness** and in
gift rather than rank. Both prior run, restated. See §2.2, §2.5.

### 6.11 Two middle terms for the soul, and a Greek–Latin convergence beside them

Augustine answers the free-choice objection at Gal. 5:17 by saying the verse is
addressed to those who will not hold the grace of faith; **Jerome answers it by
a tripartite anthropology in which the soul is a third term between flesh and
spirit** [PAT-104, PAT-157]. **Chrysostom raises the same difficulty in Greek
and answers it as Jerome does** [PAT-314] — **a genuine convergence, with
nothing showing dependence in either direction.** See §2.2.

### 6.12 Three positions on the Gradual's princes

Augustine's good angels, Cassiodorus's devil-and-good-angel, Theodoret's earthly
rulers whose authority is temporary. **A real three-way division, now
recoverable in both languages, and the strongest Greek–Latin comparison the
sweep can support** [PAT-305]. **Augustine and Cassiodorus both reach Michael in
Daniel, so between those two the shared proof-text is probably dependence.** See
§2.3.

### 6.13 Two accounts of the Offertory's angel

Augustine identifies him as Christ; **Cassiodorus does not, and turns instead to
the moral sense** [PAT-203]. **A material disagreement to preserve rather than
stack**, and positive evidence that a Latin reader could take the verse
otherwise. See §2.6.

---

## 7. Cross-proper claims settled for the synthesis commentary

**Six claims. Each draws together multiple ritual moments, multiple scriptural
contexts and multiple reception witnesses; none is an abridged procession
through the propers.** Claim classes are given per claim, and where a claim
mixes classes the mixture is stated rather than averaged.

**The two-element floor governs this section exactly as it governs §9, and the
element line of each claim names the members it joins.** Every claim joins at
least two precisely named **appointed elements of this formulary**. **The
guide's own apparatus — its four senses, its page-2 sheet, its gallery — is
never a member of a conjunction**: it is a feature of the publication and not a
ritual moment of the Mass, and where a claim bears on it that bearing is
recorded as a **consequence**. This is the same floor that drops
`fruit-count-unsettled` at §0.3(h) and refuses the Introit-incipit conjunction
at §9.8.

**A candidate frame the theological sweep offers, recorded because it is a
useful cross-check and not because it is adopted** [THE-047]. That lane
consolidated five movements running across the appointed texts, each anchored in
named elements: (1) single lordship against divided service; (2) flesh and
Spirit with their catalogues; (3) providence answered by the refusal of anxiety;
(4) propitiation, purification and salvation, carried entirely by the priest's
own prayers; (5) ordered preference stated comparatively. **Movement (4) is the
one a reader following only the readings would miss, and it is P3's material;
movement (2) is confined to a single element and clears no two-element floor by
itself, so it must not be presented as a cross-proper relation.** The six claims
below are this stage's settlement and are not that inventory; **they are offered
against it, and every element it names is accounted for by one of them.**

**The strongest cross-proper argument this run supports, and the one a
three-to-six-unit integrated commentary should be built around, is C1 with C2
and C6 as its two halves and C3 as its hinge**: one phrase carries the Mass; the
Epistle and Gospel divide the human subject between them without contradicting
each other; the formulary asks for nothing it promises and promises nothing it
asks; and at the one verse the Mass lifts out and says again at the moment of
reception, the tradition that refuses figure at the images reads doctrine.
**C4 and C5 supply the historical spine that keeps the argument from floating
free of the book.**

### 7.1 — C1. One phrase carries the Mass, and it is not the phrase Matthew usually uses

**Elements: Epistle, Gospel, Communion.** Classes 1 and 3.

`Regnum Dei` stands verbatim in three appointed elements and carries one
argument across them: the Epistle names who is **excluded** (`qui talia agunt,
regnum Dei non consequentur`), the Gospel commands that it be **sought first**,
and the Communion repeats that command as **the Lord's own word at the moment of
reception**. The negative and positive forms are two faces of one claim about
the kingdom, not two positions set against each other.

**Four textual facts sharpen it, and the fourth is new and is the strongest.**
(a) `Regnum Dei` is **rare in Matthew**: four occurrences in the whole Gospel
(6:33, 12:28, 21:31, 21:43) against thirty-four occurrences of `regnum caelorum`
across thirty-two verses, and Mt. 6:33 is the first of the four [SCR-004]. (b)
`Gal. 5:21` carries **not merely the only `regnum Dei` in Galatians but the only
word of the `regn-` stem in the whole letter** [SCR-005] — so the Epistle's
contribution is not one instance among several but the letter's single use of
the vocabulary. (c) Across the fifteen 1962 Roman formularies this repository
has collated, `regnum Dei` occurs in **this formulary alone**, and `regnum
caelorum` in no record at all, so the negative is not an artefact of a competing
kingdom-formula [THE-008]. (d) **`Regnum` is the only substantive content word
standing in three or more of the ten appointed elements; every other
three-element form is a divine name** [SCR-022]. **The three-element spine is
unique in this formulary, and that is now bounded rather than asserted.**

**Reception at the hinge, and it is now Doctoral as well as patristic.**
Augustine's `non tempore, sed dignitate` remains the best-attested Latin
sentence in the sweep. **Aquinas expounds all three members of the verse**
[PAT-135]: the kingdom sought as the end because the kingdom is beatitude and
`Regnum dicitur a regendo: tunc enim homo regitur, quando voluntati regentis
subditur`; the justice called *his* because `per iustitiam propriam nullus
potest venire ad regnum`; and the rest added `quasi, ultra forum`. **Hilary
reads the pericope as ending in a command to seek the kingdom and makes the
seeking the wage of our life** [PAT-136].

**Limits.** The sample for (c) is fifteen collated formularies, small and
non-random; **it is emphatically not a claim about the missal as a whole and
must name the sample** [THE-008]. The count at (a) is of the tracked
Clementine's Latin and **was not repeated in Greek** [SCR-004]. The pairwise map
at (d) is exact forms only and is a floor, not a ceiling [SCR-022]. **A new
bound, and it must be stated:** the Epistle's `regnum Dei` is the only
kingdom-word in Galatians but is **not** an isolated Pauline usage — 1 Cor. 6:9–10,
Eph. 5:5 and 1 Cor. 15:50 form a small closed set of parallels closing vice
lists with the same exclusion — **so a guide must not present Paul as reaching
for the phrase once and nowhere else in his letters** [SCR-028]. The defeater on
the third leg stands: a Communion antiphon drawn from the day's Gospel is
ordinary practice, **though that does not touch the Epistle's independent
occurrence, which comes from a different book and a different pericope**. And
§2.2's defeater applies with full force [THE-049].

### 7.2 — C2. The flesh that is crucified is not the body that is fed, and the tradition now says so three times in two languages

**Elements: Epistle, Gospel.** Classes 1 and 3.

The two elements are **lexically disjoint**: `caro`/`carn-` five times in the
Epistle and nowhere else; `corp-` twice in the Gospel and nowhere else
[THE-011, SCR-022]. **This is one unit, not a contrast.** The point is not that
Epistle and Gospel disagree about the body but that they use different words for
different things, and that reading them together dissolves the appearance of
disagreement. **A writer who builds this as "Epistle mortifies vs Gospel
provides" has inverted it.**

**The doctrinal resolution is documented reception, and this run adds a third
route and sharpens the first.**

- **Chrysostom, now read in Greek** [PAT-311, PAT-315]. His governing move
  survives, and it is sharper than NPNF makes it: the Greek reads `Ὁρᾷς ὅτι οὔ
  φησι τὴν σάρκα ἐνταῦθα, ἀλλὰ τὸν γεώδη λογισμὸν καὶ χαμαὶ συρόμενον` — **the
  object is σάρξ and the contrast term is λογισμός, an earthly cast of mind, not
  σῶμα.** NPNF's "he does not mean the body" is a paraphrase; it does not
  misrepresent the sense, **but a guide arguing from the appointed `caro` should
  prefer the Greek's sharper claim about the word the Epistle actually uses.**
  And at the appointed v. 24 he insists the crucifixion is **not the destruction
  of the flesh** — `Οὐ γὰρ δὴ τὴν σάρκα ἀνεῖλον· ἐπεὶ πῶς ἔμελλον ζῆν;` — but
  exact discipline. **On the fullest Greek exposition of the lesson's last
  verse, the crucifixion of the flesh is not an ascetical destruction of the
  body. That is the claim's strongest single support.**
- **Aquinas** answering the same objection through Augustine's *De civ. Dei*
  XIV.2, that `caro` here stands for the whole man (prior run, restated).
  **Preserve both answers; they differ in kind.**
- **Jerome's philology of the missal's own word** [PAT-154]: where the Latin
  translator put `vitia` the Greek reads παθήματα, *passiones*, and the Apostle
  added `desideria` **precisely so as not to seem to deny the nature of the body
  in spiritual men, but its vices** — `ut non naturam corporis videretur in
  spiritualibus viris negare, sed vitia`. **A Father defending the appointed
  word on exactly this ground is better evidence for C2 than any of the others,
  because it is anchored in the word the missal prints.**

**A convergence the pericope itself invites** [PAT-314, PAT-157]. The lesson
names only `caro` and `spiritus` and leaves the soul unmentioned; **Chrysostom
in Greek and Jerome in Latin independently raise that difficulty and answer it
the same way** — the soul lies between and makes the body spiritual or earthly
by what it does with it. **Report the agreement as agreement; nothing shows
dependence.** Augustine's *De opere monachorum* supplies the third leg from the
other direction: **the ascetic misreading of the Gospel half actually happened,
and a whole treatise was written against it.**

**Limits.** Gal. 5:24's `carnem suam crucifixerunt` is read by some as including
the body proper, and the Vulgate elsewhere uses `caro` for the body simply; **the
disjunction is a fact about these two pericopes as printed, not a lexical law**
[THE-011]. **The Introit's psalm source has `caro` in a positive sense at
Ps. 83:3b, and Cassiodorus comments on exactly that clause** [PAT-208] — **but
the clause falls outside the appointed cut and any use must say the missal cuts
before it.** 1 Cor. 15:50 puts `caro` and `regnum Dei` in one clause with the
same exclusion and is the nearest Pauline analogue to the appointed Epistle's
move [SCR-028] — **it is not appointed and nothing in the ten elements points to
it.** All Latin witnesses are transcriptions uncollated against Migne; the Greek
is a TLG transcription uncollated against PG 61. **And §0.3(a) governs: no Greek
witness may be quoted on `luxuria`, `modestia` or `castitas`.**

### 7.3 — C3. The tradition is namedly divided about whether the images may be figures, and the one verse the Mass lifts out of them is read as doctrine by both sides

**Elements: Gospel, Communion.** Classes 1 and 3. **This claim is materially
restated this run: its Gospel half is no longer a single patristic rule but a
documented division.**

**The Gospel half — a division, not a rule.** Augustine forbids allegorising the
birds and lilies: "these examples are not to be treated as allegories … they
stand here, in order that from smaller matters we may be persuaded respecting
greater ones." **Jerome forbids it too, and on a better ground for this guide's
purpose because it is internal to the appointed verse**: if the birds were
angels, the *a fortiori* drawn to men would not follow — `Si hoc ita est, ut
intelligi volunt, quomodo sequitur dictum ad homines: Nonne vos magis pluris
estis illis? Simpliciter ergo accipiendum` [PAT-121]. **Hilary of Poitiers does
the opposite**, and not in passing: he argues that the literal reading **fails**
— `Quae consequuntur, non satis propositionibus congruunt` — and reads the whole
pericope as doctrine about the resurrection of the body, allegorising every one
of the appointed images [PAT-111, PAT-112]. **Chrysostom reads them as
arguments too, but as rhetorically engineered ones**, the illustration
progressively degraded so the *a fortiori* grows at every step — **and Hilary's
Latin lemma lacks the last step, reading `cras in ignem` where the missal prints
`cras in clibanum`, so the step Chrysostom's rhetoric turns on is not in every
ancient Latin witness** [PAT-113].

**Where the Fathers who agree still differ, and it is the interesting half.**
Augustine's middle term is the **rank** of the creature; Chrysostom's is its
**vileness**, and his anthropological ground is **gift** rather than rank. The
two yield different homiletic conclusions from the same verses.

**The Communion half, which is this claim's second appointed element.** The
formulary appoints Mt. 6:33 twice: once as the Gospel's last verse and again,
recast, as the Communion antiphon — the formulary's single substantive departure
from its Bible text (§1.1, §1.2). **On that one verse nobody argues from a
lesser example.** Augustine reads `primum` as an ordering of **importance and
not of time**, `non tempore, sed dignitate`, and makes the point by denying the
sequence the word invites. **Aquinas expounds the three members as end, justice
and surplus** [PAT-135]. **Hilary — the Father who allegorises everything else
in the pericope — reads this verse plainly**, as a command to seek the kingdom
with the wage of our life, and grounds `Haec enim omnia gentes inquirunt` in
unbelief rather than appetite [PAT-136]. **So the two appointed elements that
carry Matthew 6 in this Mass are read in two different registers by the tradition
as a whole and by Hilary in particular: figure contested at the images, doctrine
read at the imperative — and the sentence the missal lifted out to say at the
moment of reception is the one on which even the allegorist reads doctrine.**

**What follows for the guide's own page 1 — a consequence of the claim, not a
member of it, and it is now a resolution rather than a tension.** The profile
requires an allegorical row. **The guide can now report a named, checked
patristic allegorical reading of these very images rather than either
suppressing the row or inventing one** (§0.3(c)). **The disagreement is
preserved and not adjudicated**, and Hilary's two qualifications travel with him:
the hay-as-gentiles reading ends in a doctrine of the bodily eternity of the
damned no other witness states, and the birds-as-unclean-spirits reading works
against the pericope's consoling sense.

**Limits.**

- **Do not report Jerome as refuting Hilary** [PAT-121]. Jerome's target is a reading of the **birds** as angels; Hilary reads the **lilies** as angels. That Jerome names Hilary among the Latin commentators he had read is not evidence that he has him in view here.
- **Remigius is not a checked witness** and must not be made one; that excerpt reaches this brief only through the Catena [PAT-141].
- **A retrieval trap sits directly on this claim** [PAT-133]: *Super Matthaeum* ascribes the lilies-as-angels reading **to Jerome**, and the reading is Hilary's.
- Chrysostom's Gospel material is **still NPNF English only**; PG 57 was not retrieved [PAT-401]. His observations are about wording, so their force depends on the sequence being the same in Greek, Latin and English at these points; **the Latin correspondences were checked and do hold, the Greek was not.**
- **The Communion membership carries C1's defeater.** A Communion antiphon drawn from the day's Gospel is ordinary practice, so this second element may be a mechanical carry-over. That bears on how *interesting* the join is; it does not dissolve it, because the criterion is two **ritual moments**. **Unlike C1, this claim has no third element from a different book to fall back on, and that is its principal weakness.**
- **No compiler's intent is claimed.** That the pericope stops at v. 33 is what lets the Communion take the Gospel's last verse, **and what the compiler meant by it is not established** [SCR-009].
- **This claim and C5 share one datum and must not be merged.** Both notice the promotion of `Primum`. C5 puts it to the extent and antiquity of the recasting; C3 puts it to the difference between the two registers. Each needs its own home.
- **A guide reaching for the lexical fields of `clibanum` or of the grass-and-glory topos should know that two of the three Latin Fathers on this pericope have ruled against the move those distributions most invite** [SCR-031].
- Augustine's exposition of Mt. 6:33 runs into v. 34, which the pericope excludes. **Where a claim must rest inside the appointed bounds, prefer Jerome's `labor exercendus est, sollicitudo tollenda`, anchored at vv. 25 and 31 and available in Latin** [PAT-124] — **which supersedes the prior brief's advice to prefer Chrysostom here.**

### 7.4 — C4. The Sunday's number is the least stable thing about the Mass, and its strands were assembled on different schedules

**Elements: Collect, Secret, Postcommunion; and, at the second remove, the
chants and the Gospel.** Class 2, with class 4 in the conclusion.

The whole case, its corrections and its bound are at §6.1–§6.3 and §6.8. What
makes it a synthesis claim rather than a chronology is the second half: **the
earlier books do not carry the 1962 formulary under a different number.**

- **The orations travel as a unit**, displaced uniformly by two Sundays in the Frankish Gelasian and one in the Gregorian, across sixteen consecutive sections, **and the Gregorian book carries all three of them together at its Dominica XV** [LIT-009, LIT-023]. **The offset is a numeration base and not an interpolation** [LIT-010].
- **The chants run later than the orations, on two independent witnesses that disagree about the magnitude.** In Honorius the whole chant set of this Mass is what 1962 sings on the **following** Sunday, +1 [LIT-017]; in the Ottobonianus apparatus the cue set runs +2 on the prior run's page-image reading [LIT-025, §6.8]. **They converge in direction and not in number, and prose must say so.**
- **The Gospel runs earlier**: Honorius's is the 1962 Thirteenth Sunday's, and that offset holds across three consecutive Sundays [LIT-017].
- **And the Communion of this Mass is attested in the Ottobonianus apparatus at a different Mass, in a rotation and not a single replacement** [LIT-018, LIT-025]. **The third leg of that rotation is now closed inside this repository**, which the prior brief could not do: the 1962 Fifteenth Sunday's Communion is `Panis, quem ego dedero` (Jn. 6:52) in the tracked registry, so all three 1962 assignments are attested against repository data — pentecost-9 `Qui manducat meam carnem`, pentecost-14 `Primum quaerite`, pentecost-15 `Panis, quem ego dedero` — **the exact reverse cycle of the older pairing.**
- **The Secret is not proper to this Sunday in the older books at all** [LIT-013]: the same prayer serves a Lenten ferial station Mass (*ad Sanctum Chrysogonum*) and a saints' Mass in one volume of Gerbert, and two Book III sections in Wilson. **That materially qualifies any prose treating its presence at the sixteenth Sunday as its home.**
- **The Postcommunion is not a Sunday prayer in the Vatican manuscript at all** but one of a floating appended, unnumbered series standing outside the numbered sections [LIT-014] — **which is the mechanism behind its narrower Gelasian attestation and why only R's margin carries it there.**

**Routing decision:** source-grounded synthesis and documented historical
orientation, **not** an interpretive proposal — §0.3(i) and §9.8.

**Limits.** **The 1962 side of the Honorius collation and of the rotation rests
on the calendar registry, a repository derivative and not a facsimile
collation**, so prose should say "as the tracked 1962 registry records" unless
someone collates pp. 396–398 of the typical edition [LIT-017, LIT-018]. **What
the closed rotation establishes is what the older pairing was, not when the
substitution happened**; Hesbert's *Sextuplex*, the instrument that would date
it, is registered at catalog level only with no artifact [LIT-018]. **The cue
attachment is in live disagreement and the page image controls** (§6.8). The
Ottobonianus evidence is about the cues of **one manuscript** and is not a bound
on the oration displacement, which rests on a wholly different body of books.
**Honorius was not reopened this run** [LIT-027].

### 7.5 — C5. The formulary makes exactly one substantive recasting, it is at the Communion, and it is older than this book

**Elements: Gospel, Communion.** Classes 1, 2 and 3.

The four departures are at §1.2 and were re-verified mechanically this run, in
Latin and against the Greek [SCR-002, SCR-003]. **And the run establishes there
is no second one**: an exhaustive mechanical comparison of every appointed block
found no centonisation, transposition or interpolation anywhere else
[SCR-033(a)]. **That is what makes "exactly one" a bounded claim rather than an
impression.**

Two departures bear theologically: adding `dicit Dominus`, which stands nowhere
in Matthew at this verse or its Lucan parallel or in the tracked Greek, **turns a
saying inside a sermon into an address made to the communicant at the moment of
reception**; and dropping `et iustitiam eius` leaves the kingdom to be sought
without the justice the Gospel names beside it — **on which Aquinas's gloss,
that the justice is called *his* because no one comes to the kingdom by a
justice of his own, answers a question the antiphon's own recasting raises**
[PAT-135]. A third, promoting `Primum`, falls exactly where Augustine's argument
makes word order carry the doctrine, **which is an editorial observation and not
a patristic one.**

**The promotion is now unexplained by any tracked Gospel text** [SCR-003].
Neither the Matthaean nor the Lucan form fronts `primum`: Luke places it after
the verb too. **That is a statement about what the tracked texts do not supply,
and not a claim about what produced the antiphon.**

**The recasting is not proper to the 1962 edition:** the same form is printed in
the Pustet Missal of Ratisbon 1862, which this repository tracks as
public-domain text, and the Pustet's own arrangement places this formulary
immediately before the `Inclina, Domine` formulary exactly as 1962 does
[PRE-015]. **Read that corroboration narrowly: it establishes the adjacency of
the two formularies in the pre-1955 book and says nothing about the sacramentary
displacement.**

**Four independent witnesses now converge on the antiphon being secondary in
this position, where the prior brief had three.** (a) The appointed text itself:
it is the formulary's one substantive departure. (b) Guéranger, p. 342, that the
Communion-anthem "was not the one primitively used" — **a checked report of an
unchecked claim, to be attributed to him.** (c) **The Ottobonianus cue block
whose Introit is `Protector noster` has Communion `Panis quem ego` and not
`Primum quaerite`** — and **that survives the live disagreement at §6.8, because
it is a fact about block content and not about attachment** [LIT-025]. (d)
**Honorius's Communion for this Sunday is `Panis, quem ego dabo`** [LIT-017].
**Two independent witnesses, a manuscript apparatus and a twelfth-century
liturgical commentator, place a different Communion beside this Mass's other
elements.**

**And a control from within the same Office, which is the strongest single thing
here and which anyone can check in the same pages** (prior run, restated).
Guéranger prints this Sunday's Magnificat antiphon at Vespers as `Quaerite
primum regnum Dei, et justitiam ejus, et haec omnia adjicientur vobis.
Alleluia.` **That antiphon retains both `et iustitiam eius` and `haec` — exactly
the two clauses the Mass's Communion drops — and leaves `primum` in its
Matthaean position after the verb.**

**Limits.** Guéranger's judgment rests on Tommasi's Antiphonary and "the ancient
liturgists", neither consulted. Antiphon texts are routinely shortened for chant
and `dicit Dominus` is a common formulaic tag, so both changes may be
conventional rather than expressive, **and that count was not run.** The Pustet
witness shows the recasting is old but says nothing about why it was made. **No
witness in either sweep comments on the antiphon**, so every reading of it is a
reading of Mt. 6:33 in its Gospel place applied to the antiphon by the guide
[PAT-135]. And the Communion's selecting the imperative rather than the
pericope's three prohibitions may be an artefact of taking the final verse —
**a real weakness in the third step of that argument, though not in the first
two.**

### 7.6 — C6. The Mass petitions nothing it promises and promises nothing it petitions

**Elements: Collect, Secret, Postcommunion, Gospel, Communion — five.**
Classes 1 and 4. **New this run, and the sharpest cross-proper argument the
theological sweep found** [THE-036].

**The three orations ask for no temporal good whatever.** Read complete:
`Custodi … Ecclesiam tuam propitiatione perpetua`, `tuis semper auxiliis et
abstrahatur a noxiis, et ad salutaria dirigatur`; `ut haec hostia salutaris, et
nostrorum fiat purgatio delictorum, et tuae propitiatio potestatis`; `Purificent
semper et muniant tua sacramenta nos, Deus: et ad perpetuae ducant salvationis
effectum`. **No term for food, drink, clothing, health, harvest, peace or any
other temporal good occurs in any of the three.**

**And the only goods the Mass promises are exactly those.** The Gospel states
the antecedent twice — `Quid manducabimus, aut quid bibemus, aut quo
operiemur?` and `Scit enim Pater vester, quia his omnibus indigetis` — and then
promises `et haec omnia adicientur vobis`; the Communion repeats the promise
alone. **Food, drink and clothing, which no prayer of the day asks for.**

**A third distribution, corrected by the fresh join and no longer publishable
as it first stood** [THE-036; fresh:THE-107]. The first statement of this
distribution — every imperative addressed to God in the formulary is `aspice`,
`respice`, `Custodi` and the orations' subjunctives, and the only imperative
addressed to the assembly is `Quaerite`/`Primum quaerite` — **is contradicted
by the appointed Latin and is withdrawn.** The Secret opens with a fourth
God-directed imperative, `Concéde nobis, Dómine, quǽsumus`, which is
imperative mood and not subjunctive (collated at `propers/verified.md`
element 8); and the scriptural elements carry at least seven further
assembly-directed imperatives besides `Quaerite` — `ambulate` (Ep.),
`Venite` (All.), `Respícite`, `Considerate`, `Nolite … esse` (Gosp.),
`gustate`, `videte` (Off.) [fresh:THE-107, whose mechanical imperative-form
probe found the 2pl forms and the four 2sg imperatives and no 2pl imperative
in Postcommunion, Gradual, Collect or Secret]. **The narrower contrast
survives and is the one to publish**: the three orations never command the
assembly and ask for no temporal good (above); their material addressed to God
is otherwise subjunctival; and the command the Mass repeats at reception is
the promise's own `Quaerite`. **The published sentence in
`sections/20-themes.tex` lines 126–128 states the withdrawn three-item list
and must be corrected by the author; this paragraph is the authority for the
correction.**

**Why this is a claim and not a curiosity.** It is the resolution of the tension
the formulary most obviously raises — a Gospel that forbids anxiety about food
inside a rite whose whole business is petition — **and the resolution is
readable off the page rather than imported: the objects differ.** The orations
never ask for what the Gospel forbids anxiety about. **Two of the tradition's
own moves stand behind it without being it:** Jerome's `labor exercendus est,
sollicitudo tollenda` [PAT-124] and Jerome's `non dixit, qui habet divitias, sed
qui servit divitiis` [PAT-123], both of which distinguish the thing from the
anxiety about it. **Neither Father says what C6 says; they license the
distinction C6 observes.**

**The strongest limit, and it is unrun rather than answered** [THE-036]. **Roman
orations of the season are conventionally non-temporal in their petitions, so
the disjunction may be a genre fact rather than a fact about this formulary —
and the counter-test that would settle it, a survey of temporal petitions in the
orations of the other fourteen collated identities, was NOT run.** **Until it is
run this is a bounded observation about this Mass and must not be stated as a
distinctive one.** The author has two honest routes: state it as a reading of
this formulary with the genre question printed beside it, or state it as
contingent on a counter-test nobody has performed. **What is not available is
stating it as distinctive.**

**Two further limits.** The claim rests entirely on class-1 distributions and a
class-4 conclusion; **the three orations have no located exegetical reception at
all** (§4.1), **so no part of the oration half can ever rise to documented
reception on the evidence now held** [THE-045]. And **§2.2's defeater does not
reach this claim's oration members**, which is one of its quiet strengths: the
Collect, Secret and Postcommunion are not texts a medieval preacher expounded
beside a different Gospel.

---

## 8. Notable-and-quotable audit

**Five candidates selected from the `cultural-afterlife` lane's ten qualifying
returns, under the cultural-afterlife rule in
`guidance/liturgy/roman-1962-propers.md`. The selection is a selection; no
candidate was sought by this stage and none may be** [CUL-024]. Element
coverage is **Communion, Gospel, Epistle and Gradual — exactly the four the
manifest assigns to the `notable-and-quotable` component**, and the four where
qualifying candidates exist at all.

**The evidence-state rule governing the gallery, and it has changed this run.**
The prior brief had to say that **nothing** the lane returned rose above
*inspected*. **Two entries are now collated against page images and are the only
items in this brief that may carry the word *verified*: §8.4 and §8.5**
[CUL-008, CUL-011, CUL-015]. **The other three remain at "retrieved and read in
a digital surrogate" and may NOT be called verified** — though that state is
itself better than the prior run's for §8.2 and §8.3, whose passages were then
reassembled from API snippets and are now read as continuous text from the
Caselaw Access Project's transcription of the printed reporters. **"Retrieved
and read in a digital surrogate" and "verified" are different states under
`guidance/sources.md`, and the distance between them is exactly a page image.**
The method for closing it is at §3.6 and is cheap.

**Three states are used below and they are not interchangeable** [CUL-015]:
**VERIFIED BY COLLATION AGAINST THE PAGE IMAGE**, and only for the crop regions
named; **RETRIEVED AND READ IN A DIGITAL SURROGATE**, meaning continuous text
from a CAP transcription, the official Hansard digitisation, or an uncorrected
OCR layer; **INSPECTED VIA SEARCH SNIPPET ONLY**, meaning the passage was seen
in a highlighted match window and nowhere else — **and any case at that state
must be read in full before it is quoted.**

**Rights: all five rest on public-domain or official-report material** —
nineteenth- and twentieth-century American newspapers digitised by the Library
of Congress, US court opinions and official reporters, and the UK official
parliamentary report. **No protected text is reproduced by any of them.** Quoted
extracts should stay brief.

**The identity rule for this formulary, and it is the dominant failure mode
here** [CUL-023]. **The appointed texts of this Mass are unusually rich in
phrases with near-twins elsewhere in the same Bible**: Mt. 6:24 shares its last
clause with Lk. 16:13; Ps. 117:8–9 shares its subject with Ps. 145(146):3;
Mt. 6:26 shares its idiom with Gen. 1:26 and Acts 10:12; "O ye of little faith"
recurs at Mt. 8:26, 14:31 and 16:8. **Any candidate for this Mass must be tested
for locus before it is tested for wit.** Three of the six refusals at §8.6 are
refusals on **identity** and not on quality.

### 8.1 The political kingdom — Communion (and Gospel), Mt. 6:33

| Field | Record |
|---|---|
| **Appointed text and locus** | *Antiphona ad Communionem*, Mt. 6:33, marginal no. 1580: `Primum quaerite regnum Dei, et omnia adiicientur vobis, dicit Dominus`; the same verse closes the appointed Gospel |
| **Later texts and loci** | Kwame Nkrumah's motto. **UK House of Commons, 3 Dec 1962, debate "Central Africa"**, Humphry Berkeley: "Outside the Parliament building in Accra there is a statue of President Nkrumah the inscription on which is couched in Biblical language … The inscription reads: Seek ye first the political kingdom and all things will be added unto you. That is what the Africans want." **UK House of Lords, 19 Dec 1962, col. 1203**, Lord Milverton, at 6.27 p.m., naming "the growing popularity of the doctrine which is inscribed, as we all know, in a famous place in Accra, 'Seek ye first the political kingdom and all things will be added unto you'. … that motto, if accepted fully, has caused a lot of trouble." ***The Spark* (Accra), no. 159, 5 Nov 1965**, on the Ghana Co-operative Movement: "For, Osagyefo has repeatedly said, 'Seek ye first the poli-tical kingdom and all other things shall be added unto you.'" |
| **Relationship strength** | **Documented verbal dependence, not echo.** The motto keeps Matthew's imperative, its object-plus-addition structure and the KJV's archaic diction, substituting only "political" for "of God" and dropping "and his righteousness" |
| **Wording check** | Three attestations, **two variants**: "all other things shall be added unto you" (*Spark* 1965) against "all things will be added unto you" (both 1962 speakers). **The two 1962 speakers agree while being independent of one another — different Houses, sixteen days apart, one describing a statue inscription and one "a famous place in Accra" — which is itself evidence that they were reporting a circulating inscription rather than copying a text.** **None of the three reads "all these things shall be added unto you", which is the KJV's own wording and the form most often quoted secondhand** |
| **A coincidence to hedge or omit** | **The appointed Communion antiphon also omits "and his righteousness" / `et iustitiam eius`, exactly as the motto does. There is no dependence whatever** — the antiphon's omission is a pre-1962 liturgical recasting and the motto's a modern political abridgement — **and the coincidence must be presented as a coincidence or not at all** |
| **Context and turn** | **Political, and contested in its own time.** Berkeley reports the inscription approvingly, as the authentic voice of African nationalism; Milverton lists the same sentence among the causes of the Federation's failure. **Within sixteen days the same appointed verse is deployed in Parliament both as the thing to be understood and as the thing to be blamed** |
| **Rights / translation** | UK official parliamentary report; public-domain OCR of an openly-readable Internet Archive item. No protected text |
| **Cultural payoff** | The antiphon the congregation hears at Communion, standing as a monumental inscription in Accra and debated as state doctrine in both Houses at Westminster |
| **Limiting qualification** | **None of the three sources is Nkrumah's own first utterance.** *The Spark* reports what "Osagyefo has repeatedly said"; the two 1962 speakers report an inscription. **The claim is bounded to the motto's circulation and reception and must never be stated as its coinage or dated to a first utterance.** Berkeley attributes the inscription to a statue outside the Parliament building; Milverton says only "a famous place"; **neither location was independently checked and the statue's own text was not seen** |
| **Evidence state** | **RETRIEVED AND READ IN A DIGITAL SURROGATE.** The two Hansard passages read as continuous text in the official report's own digitisation, **which is better than the prior run's**; the *Spark* passage is an uncorrected OCR layer with visible damage. **Not verified** |
| **Material negatives** | Hansard search API, `TotalContributions=2` for the motto — exactly the two 1962 contributions and no others in that index. Internet Archive metadata full-text search, `numFound=2`, both the UNESCO *General History of Africa* vol. VIII, **copyright-restricted secondary works, not opened**. **And a false negative caught by luck in this very candidate:** a grep of *Spark* issues for "political kingdom" returned zero because the OCR broke it as `poli-`/`tical` |

### 8.2 The rule against divided loyalty — Gospel, Mt. 6:24

**Two attributions in the prior brief's version of this entry are corrected
here; see §0.3(e).**

| Field | Record |
|---|---|
| **Appointed text and locus** | Gospel, Mt. 6:24, marginal no. 1577: `Nemo potest duobus dominis servire: aut enim unum odio habebit, et alterum diliget: aut unum sustinebit, et alterum contemnet. Non potestis Deo servire, et mammonae` |
| **Later texts and loci** | ***United States v. Mississippi Valley Generating Co.*, 364 U.S. 520 (9 Jan 1961)**, Warren C.J., on 18 U.S.C. §434: "The moral principle upon which the statute is based has its foundation in the Biblical admonition that no man may serve two masters, **Matt. 6:24**, a maxim which is especially pertinent if one of the masters happens to be economic self-interest." ***SEC v. Capital Gains Research Bureau*, 375 U.S. 180 (9 Dec 1963)**, Goldberg J., quoting the same. ***Everhart v. Searle*, 71 Pa. 256 (13 May 1872)**, Thompson C.J., opening: "We have the authority of Holy Writ for saying that 'no man can serve two masters…'" ***Knights of Pythias v. Withers*, 177 U.S. 260 (1900)** and ***NLRB v. Health Care & Retirement Corp.*, 511 U.S. 571 (1994)**, Ginsburg J. dissenting — **both quotations of a third party (a state court and a congressman) and not the Supreme Court speaking, and both must be described that way.** *Carter v. Harris*, 4 Rand. 199 (Va. 1826) is the earliest in the searched corpus |
| **Relationship strength** | **Explicit and self-declared dependence, not echo.** *Everhart* names "Holy Writ"; ***Mississippi Valley* gives the chapter-and-verse citation "Matt. 6:24", which is the appointed Gospel's own opening verse** — so this entry does **not** have the Luke/Matthew identity problem that sank the 1914 advertisement at §8.6 |
| **Wording check** | Courts quote the KJV against the appointed Vulgate. **Every use located stops before "Ye cannot serve God and mammon" / `Non potestis Deo servire, et mammonae`, so the second master is never named — but Warren immediately re-supplies it in secular dress ("especially pertinent if one of the masters happens to be economic self-interest"), which is the sharpest single element of the turn and should be quoted with the maxim** |
| **TWO CORRECTIONS to the prior audit** | (1) **"The authoritative declaration" is NOT the Supreme Court's own phrase.** It is the Court of Claims' in *Michigan Steel Box Co. v. United States*, 49 Ct. Cl. 421, 439, quoted in a footnote by both *Mississippi Valley* and *Capital Gains*, **and must be attributed there.** (2) **The "remedial of actual wrong" sentence in *Everhart* is not the court speaking in its own voice** but its quotation of **Hare and Wallace's Notes to 1 *Leading Cases in Equity*, p. 210**. Both were found by reading continuous text rather than API snippets [CUL-002] |
| **Context and turn** | In Matthew the sentence asserts the impossibility of divided religious allegiance and grounds a command not to be anxious. **In law it becomes a prophylactic rule of positive obligation enforced without proof of wrongdoing** — the quoted authority states that "it matters not that there was no fraud meditated and no injury done; the rule is not intended to be remedial of actual wrong, but preventive of the possibility of it" |
| **Rights / translation** | US court opinions and an official reporter; no protected text |
| **Cultural payoff** | The appointed Gospel's incipit operating as a rule of secular commercial law from 1826 to 1994, from a Virginia trust case to the Supreme Court, with the courts openly borrowing scriptural authority |
| **Limiting qualification** | The CourtListener corpus is **overwhelmingly American** and **no English or Commonwealth sweep was run**, so nothing may be claimed about Anglo-American law beyond the United States. **The count of 331 is the API's and was not audited item by item.** CAP gives the *Mississippi Valley* decision date as 1961-01-09 while CourtListener reads 1961-03-20; **the official reporter date should be preferred** |
| **Evidence state** | **RETRIEVED AND READ IN A DIGITAL SURROGATE, and one step better than the prior sweep**: CAP's transcription of the official printed reporter read **continuously with no reassembled ellipses**. **Not collated against a page image; not verified** |
| **Ordering, now settled** | The prior brief recorded that the ordering of the two *Everhart* fragments was not established. **It is now: the two-masters invocation is the opinion's opening paragraph and the Hare and Wallace quotation comes later, in the discussion of policy** |

### 8.3 Against such there is no law — Epistle, Gal. 5:23

| Field | Record |
|---|---|
| **Appointed text and locus** | Epistle, Gal. 5:23, marginal no. 1574: `Adversus huiusmodi non est lex` |
| **Later texts and loci** | ***Johnston v. The Commonwealth*, 22 Pa. 102 (1853)**, construing the Pennsylvania Sunday-observance act, which prohibited "any worldly employment or business whatsoever" except works of charity and necessity, on a prosecution for driving an omnibus by the month on Sunday: "perhaps all would agree, that visiting and administering to the sick and destitute, and labors for the spiritual welfare of men, are works both of charity and necessity. **Certain it is, that against such there is no law, and they may be performed on any day.**" Companion case *Omit v. Commonwealth*, 21 Pa. 426 (1853). ***Sullens v. State*, 191 Miss. 856, 4 So. 2d 356 (10 Nov 1941)**, a **criminal-contempt prosecution of a newspaper editor** for published criticism of the courts: "When one functioning within the circle of free speech runs out thoughtlessly to the full length of his tether he is apt to be brought up abruptly to his discomfiture, to find himself entangled amid the brambles of bad taste which fringe the border lines of discretion. **Against such there is no law.** Where the courts can not compel they can not condemn." |
| **Relationship strength** | **Strong verbal dependence but undeclared.** Neither court names Galatians. The clause is reproduced word for word in its KJV form and **is not a phrase that arises independently in English**, so this is **documented borrowing, to be described as unattributed borrowing and never as a citation** |
| **Wording check** | KJV "against such there is no law" exactly, in both; the appointed Latin is `Adversus huiusmodi non est lex`. *Johnston* prefixes "Certain it is, that"; *Sullens* stands the clause alone as its own sentence |
| **Context and turn** | **The pivot is the word "law", and it is a pun.** Paul's subject is twelve named virtues standing outside the **condemning** reach of the Mosaic law; *Johnston*'s is a statutory term of art — works of charity and necessity standing outside the **prohibiting** reach of a penal statute against Sunday labour — **so a theological claim about justification becomes a canon of statutory construction.** *Sullens* pushes it further from Paul: conduct that is in bad taste but not punishable, **in a First Amendment contempt case** |
| **Rights / translation** | US court opinions; no protected text |
| **Cultural payoff** | The appointed Epistle's closing clause doing duty as the operative sentence in a Sabbath-breaking prosecution and, ninety years later, in a contempt case about a newspaper editor's insults. **It is the gallery's only Epistle entry** |
| **Limiting qualification** | **Whether either court intended the scriptural allusion or was reaching for a stock formula is not established and must not be asserted.** The two uses are 88 years and two jurisdictions apart and **no line of transmission between them was established.** The exact-phrase query returns exactly 2 opinions, which is a statement about CourtListener's coverage and not about American law at large. **The American newspaper corpus could not be phrase-searched for this clause, so no claim, positive or negative, is made about its presence there** |
| **Evidence state** | **RETRIEVED AND READ IN A DIGITAL SURROGATE, and a material upgrade on the prior audit**, which had to reassemble the *Johnston* passage from three overlapping API snippets and warn that the internal ellipses were the lane's. **Both passages above are continuous CAP text with no ellipses.** Not collated against a page image; **not verified** |
| **A detail the prior audit understated** | *Sullens* was described only as "conduct improper but not punishable". **It is specifically a criminal-contempt-of-court prosecution of a newspaper editor, which raises the payoff and should be stated** |

### 8.4 Solomon was not arrayed — Gospel, Mt. 6:29 — **PAGE-IMAGE COLLATED**

| Field | Record |
|---|---|
| **Appointed text and locus** | Gospel, Mt. 6:28–29, marginal no. 1577: `Considerate lilia agri quomodo crescunt: non laborant, neque nent. Dico autem vobis, quoniam nec Salomon in omni gloria sua coopertus est sicut unum ex istis` |
| **Later texts and loci** | ***The Progressive Farmer* (Winston/Raleigh, N.C.), 15 Jan 1889, p. 8, "SOLOMON AND HIS GLORY"**, LCCN sn92073049, reprinting the rural editor of *Farm, Field and Stockman*: the soprano, then bass, then alto, then tenor each declare in turn that "Solomon in all his glory was not arrayed"; then, "when the feelings of the congregation had been harrowed up sufficiently, and our sympathies all aroused for poor Solomon, whose numerous wives allowed him to go about in such a fashion even in that climate", the choir supplies "like one of these" — "These what? So long a time had elapsed since they sung of the lilies that the thread was entirely lost, and by 'these' one naturally concluded that the choir was designed. … Solomon in a Prince Albert or cutaway coat? Solomon with an eye-glass and mustache, his hair cut Pompadour? No, most decidedly." ***The Spanish American* (Roy, N.M.), 11 Apr 1908, p. 9, "A FREEZE-OUT"**, LCCN sn92061524, credited to the *Illustrated Sunday Magazine*: a stagestruck singer breaks down twice at "Solomon in all his glory was not arrayed—" and "a voice from the audience remarked in appropriate comment: 'Bad fix for Solomon on a night like this!'" |
| **Relationship strength** | **Explicit.** The 1889 piece names the text "that scriptural poem that compares Solomon with the lilies of the field, somewhat to the former's disadvantage"; the 1908 piece names the song "Consider the Lilies" |
| **Wording check — NOW SETTLED ON THE PAGE IMAGES, and it lifts the prior audit's warning** | The prior brief warned that its punctuation and italics were reconstructed by the lane and must not be presented as the printed pointing. **The punctuation above IS the printed pointing.** The 1889 text sets the choir's words in double quotation marks exactly as given **and prints "Soloman" for Solomon in the bass sentence, which is the paper's own inconsistency and should be reproduced or silently noted, not corrected.** The 1908 text ends both broken-off quotations with a **printed em-dash inside the closing quotation mark** and prints the punchline with an exclamation mark. **Both depend on the KJV clause being interrupted before "like one of these"** |
| **Context and turn** | **Humorous, and in both cases the humour is produced by the appointed wording itself rather than merely attached to a musical occasion — which is what keeps the entry clear of the gallery rule's exclusion of a bare musical setting.** The 1889 sketch is a joke about syntax carried through four voices: a comparative clause severed from its second term turns a statement about Solomon's inferiority to a wildflower into a statement that Solomon was **unclothed**; the delayed "these" is then mis-referred to the choir; and the appointed verse ends by praising the tailoring of a fashionable congregation, with a closing run of anachronisms dressing Solomon as a Gilded Age dandy. The 1908 piece gets the same result in five lines by freezing the singer at the same syllable |
| **Rights / translation** | Public-domain American newspapers digitised by the Library of Congress; no protected text |
| **Cultural payoff** | The appointed Gospel's best-known comparison surviving in American newspaper humour as a standing joke about being caught with nothing on, twice, nineteen years and two thousand miles apart |
| **Limiting qualification** | **Both items are reprints** — the 1889 piece credits *Farm, Field and Stockman*, the 1908 piece the *Illustrated Sunday Magazine* — **and neither original printing was retrieved, so the wording collated is the reprinting paper's.** Whether the two jokes are independent or descend from a common source was not established: **they are two attestations of a joke-type, not two independent inventions.** The 1889 piece is a North Carolina paper reprinting a Chicago farm journal and applying it to churches "not a hundred miles from Raleigh", **so the congregation satirised is the reprinting editor's target.** No claim is made about how widely the joke-type circulated |
| **Evidence state** | **VERIFIED BY COLLATION AGAINST THE PAGE IMAGE** for both passages quoted, **within the crop regions named in the finding**; matter outside those regions on either page remains uninspected. **Note the low-resolution master of the 1908 page: only the native-size crop is legible** |

### 8.5 Princes — or railroads — Gradual, Ps. 117:9 — **PAGE-IMAGE COLLATED**

| Field | Record |
|---|---|
| **Appointed text and locus** | Gradual, Ps. 117:8–9, marginal no. 1575: `Bonum est confidere in Domino, quam confidere in homine. V. Bonum est sperare in Domino, quam sperare in principibus` |
| **Later text and locus** | ***Semi-Weekly Interior Journal* (Stanford, Ky.), 19 Nov 1895, p. 2**, LCCN sn85052020, article headed "**THE ATLANTA EXPOSITION / And Other Incongruvial Notes Picked Up There and Thereabouts.**", datelined "ATLANTA, Nov. 16": "**It is better to serve the Lord than to put confidence in princes or railroads, especially the latter.** I thought when I got on the 'Exposition Flyer,' my trials were ended, but alas for human hopes. The engine broke down midway between stations five miles apart and refused to turn a wheel. A flagman had to be sent for another engine 2 1/2 miles afoot … Finally 2 1/4 hours late I reached Chattanooga" |
| **Relationship strength** | **Explicit verbal dependence, unattributed.** The writer reproduces the second half of the appointed Gradual verse almost intact and then adds to it, **which only works if the reader recognises where the sentence was going to stop** |
| **Wording check — NOW SETTLED ON THE PAGE IMAGE, correcting the prior audit in three places** | (1) **The printed verb is "serve", not "trust".** The prior sweep saw only the OCR reading "servo" and could not tell whether the divergence was the writer's, a compositor's or the scanner's; **the page image shows "It is better to serve the Lord" in clean type, so the OCR is exonerated and the divergence is the newspaper's.** Whether writer or compositor made it is still not established. **It must not be silently corrected to "trust" if the sentence is quoted.** (2) **There is no dash.** The prior brief printed "confidence in princes — or railroads"; the page reads "in princes or railroads, especially the latter", with a line break inside "prin-ces" and **no punctuation at all before "or"**. **Any dash in a published quotation would be the editor's.** (3) **The heading needs no conjecture**: "Incongruvial" is what the paper set, and the prior brief's bracketed reconstruction should be dropped. Two further details corrected: the stations are **five** miles apart, not the OCR's "Ave miles", and the writer reached Chattanooga **2 1/4** hours late, not "2 hours". The rest matches KJV Ps. 118:9 word for word |
| **Context and turn** | **Humorous and idiomatic, achieved by a single appended noun.** The psalm's antithesis is between divine and human reliability, with "princes" standing for the highest human power; the letter keeps the grammar and slips a railway company into the princes' place. **"Especially the latter" is what makes it a redirection rather than a quotation, because it ranks the railroad below princes** |
| **Rights / translation** | Public-domain American newspaper digitised by the Library of Congress; no protected text |
| **Cultural payoff** | The Gradual — otherwise the least quoted element of this formulary in every corpus swept — surviving as a traveller's grumble about the Exposition Flyer. **It is the entry that broadens a gallery otherwise dominated by the Gospel** |
| **Limiting qualification** | An unremarkable local newspaper, not a canonical text; the entry's value is the neatness of the redirection. **THE LETTER IS ANONYMOUS**, and the authorship question is now settled negatively on the page image: **"W. P. WALTON" is the paper's editorial column masthead line set above the article, not a byline on the letter**, which is datelined and carries no signature. **He is a plausible author, the page does not say so, and he must not be printed as the writer.** Whether the writer knew he was quoting Ps. 118:9 rather than a floating proverb is not established. **No claim is made about how widely this joke-form circulated** |
| **Evidence state** | **VERIFIED BY COLLATION AGAINST THE PAGE IMAGE** for the wording quoted and for the masthead, **and only for the two crop regions named in the finding**; anything else on the page remains uninspected |
| **The identity trap this entry survives, and which every Gradual candidate must** | **Every "trust in princes" hit in the American legal corpus is Psalm 146 and not the appointed Gradual** [CUL-019]. The discriminating marks: **the appointed Gradual is a COMPARATIVE ("it is better to trust in the Lord THAN to put confidence in princes"); Psalm 146 is a flat PROHIBITION ("put not your trust in princes")**; and the Gradual pairs princes with "man" in a doubled verse where Psalm 146 pairs them with "the son of man". **Any candidate lacking the comparative frame is Psalm 146 and must be refused. CUL-011 is the only located use that keeps it** |

### 8.6 Candidates returned and **not** selected, with the reason

Recorded so the judgement is visible and so a later reader does not mistake
absence for oversight. **Five of the ten qualifying candidates are not
selected**, and the cap of five is the reason for the first four.

| Candidate | Reason not selected |
|---|---|
| **CUL-020**, "they toil not, neither do they spin" **inverted** into the standing judicial description of swindlers, gamblers and racketeers, 1891–1975, and made the stated reason blue-sky and consumer-protection statutes are read broadly | **The strongest turn in the whole return, and the strongest substitute for any Gospel entry above.** *State v. Whiteaker*, 118 Or. 656 (1926) fuses the appointed clause with J. Rufus Wallingford, the pulp-fiction confidence man, inside one sentence about a securities statute, and is then quoted in at least five later opinions across four jurisdictions; *State ex rel. Garrett v. McPeters*, 256 Ala. 555 (1951) cites **"Matthew 6:28"** and appends the exception that destroys it — jackals of greed who toil not "except at the handle of a 'one armed bandit'". **A complete reversal of valuation: in Matthew not toiling is the point in the lilies' favour; here it is the indictment. Not selected only because the gallery is capped at five and its "wrong noun appended" mechanism is the same move §8.5 already carries.** Its own limits: the five later citations were seen in match windows only, and the variant with Matthew's internal comma was not swept |
| **CUL-016**, Mt. 6:28–29 quoted in a creationist high-school biology textbook and quoted back by Overton J. in ***McLean v. Arkansas Board of Education*, 529 F. Supp. 1255 (E.D. Ark. 1982)** as documentary proof the book was religious | **A genuine double turn — Matthew's lilies converted into an argument from design offered as biology, then converted again into forensic evidence proving a statute unconstitutional — and the only scientific-then-judicial register available.** Displaced by the cap, and by one practical defect: **the pin cite is not settled** (§5). The structural locus is safe to cite meanwhile. **The textbook itself was not retrieved; the wording verified is the court's reproduction of trial exhibit Px 129** |
| **CUL-017**, "add one cubit unto his stature" as a maxim of institutional incapacity, 1906–1993 | **A real and datable gradient — cited scripture (*Okaloosa Island*, 1978, giving "Matt. 6:27 (King James version)"), quoted with the whole rhetorical question (*Hockaday*, 1906), quoted anonymously (*Ruvido*, 1940), and finally dead idiom (*Marriott v. Ramada*, 1993, "can not add one cubit to the advertisement which is annexed thereto")** — with *Thompson v. Talmadge* setting it inside the Georgia three-governors crisis. Displaced by the cap. Its own limits: four of the nine were seen in match windows only; **variants such as "a cubit to his stature" were not swept, so the population is larger than nine and the entry must not claim to be exhaustive** |
| **CUL-018**, "Solomon in all his glory" drifting in judicial usage **from raiment to wisdom** | Two attestations of the wisdom-sense 89 years and two states apart (*South-Western Railroad v. Paulk*, 24 Ga. 356 (1858); *Cameron & Henderson v. Franks*, 199 Okla. 143 (1947)), plus **Jackson J. dissenting in *Carlton v. Carlton*, 756 P.2d 86 (Utah App. 1988), citing "Matthew 6:29" to mock his own colleagues for having "clothed this case in the raiment of complexity"**. The fusion is real — Matthew's Solomon is a byword for splendid clothes and for **losing** a comparison, and the wisdom belongs to 3 Kings 3 — **but it duplicates §8.4's element and verse, and two attestations 89 years apart are two attestations of a usage and not evidence of a continuous tradition** |
| **CUL-021**, the birds of Mt. 6:26 cited as **lexicographical evidence** for the English word "fowl", in *State v. Davis*, 72 N.J.L. 345 (1905) — a pigeon-shooting prosecution turning on a single-object constitutional challenge — and, at one further remove, in *Pacific Trading Co. v. United States*, 8 Cust. Ct. 221 (1942), on whether frogs' legs are fowl | **Displaced by the cap, and weakened by identity.** *Davis* is explicit and cited, setting Matthew beside Genesis and Shakespeare as three witnesses to English usage, and the register (philological, then tariff) is genuinely unlike the rest. **But two thirds of the corpus hits for "the fowls of the air" are Genesis 1:26 and not this Gospel** [CUL-021], and *Pacific Trading* is **echo only** — the phrase reaches the court inside a dictionary entry with no locus, and the plural occurs in the KJV at several places besides Mt. 6:26. **Only *Davis* survives the identity test on documented grounds** |
| **CUL-022**, "O ye of little faith" as an IRS manager's e-mail tease, reproduced in *United States v. Greve*, 490 F.3d 566 (7th Cir. 2007) | **Rejected on the rule, and the lane says so itself.** **Echo, and it must be described as an echo**: the five words are exact KJV and Mt. 6:30 is their first occurrence, **but the same English tag renders Mt. 8:26, 14:31 and 16:8**, the phrase is a dead idiom in modern English, the e-mail attributes nothing, and **dependence on Matthew rather than on general usage is not documented.** Under the gallery rule an idiom used with no sign the speaker knew it was scriptural sits close to the excluded category of "an independently similar phrase". **It is the weakest of the ten and was returned for breadth, not for publication** |
| **Carlyle's "Gospel of Mammonism"**; ***Sacred Heart Academy v. Karsch***; the three Psalm 146 cases; six of the nine "fowls of the air" cases; *Wagner v. Sanders* | **Refused before selection**, on strength, on the rule, or on identity. See §5 |

### 8.7 Fresh cultural-afterlife findings, run `e5b24f405bde9691` (2026-08-31)

The fresh lane re-ran its sweep and returned four findings, recorded here
under the same rules as §8 — this stage selects, it does not go looking
[fresh:CUL-001–fresh:CUL-004].

**Two are fresh re-establishments of entries already carried above.**
fresh:CUL-001 re-establishes §8.2 from scratch: it re-reads *Everhart v.
Searle* and *United States v. Mississippi Valley Generating Co.* as continuous
CAP transcriptions of the printed reporters, reproduces the §0.3(e)
corrections exactly (the "authoritative declaration" phrasing is the Court of
Claims' in *Michigan Steel Box Co.*, quoted in a footnote; the "remedial of
actual wrong" sentence is the court's quotation of Hare and Wallace's Notes),
adds the corpus measurement (CourtListener exact-phrase count 331, earliest
dated hit *Carter v. Harris*, Va. 1826, **not opened and not relied on**), and
confirms that every legal use located stops before `Non potestis Deo servire,
et mammonae`, with Warren C.J. re-supplying the second master in secular
dress. fresh:CUL-002 re-establishes §8.3 the same way: *Johnston v. The
Commonwealth* (1853) and *Sullens v. State* (1941) read whole, the
exact-phrase query returning exactly 2 opinions, the pun on "law" and the
unattributed-borrowing description all confirmed. **Both entries' evidence
states are unchanged** — retrieved and read in a digital surrogate, not
verified — and §8.2/§8.3 stand as corrected.

**Two carry the lily-clause inversion family, and the fresh sweep upgrades
its evidence state.** fresh:CUL-003 records *State v. W. Harrison Whiteaker*
(Or. 1926, the "J. Rufus Wallingford" sentence), *State ex rel. Garrett v.
McPeters* (Ala. 1951, citing "Matthew 6: 28" explicitly, the jackals passage),
and *Sperry & Hutchinson Co. v. Hudson* (Or. 1951, quoting Whiteaker), each
read whole from CAP transcriptions, with the corpus measurement (8 hits with
Matthew's internal comma, 13 without, 1922–1982). fresh:CUL-004 records
*State v. Tracy*, 294 Mo. 372 (Mo. 1922) read whole — a prosecutor's opening
argument quoting the clause as a jibe about a professional burglar — **as a
second attestation of the inversion that does not descend from Whiteaker**,
which the first join's CUL-020 could not establish (its five later citations
were seen in match windows only). The turn is unchanged from §8.6's record:
in Matthew not toiling is the point in the lilies' favour; in the case law it
is the indictment, a complete reversal of valuation. **Limits, all carried
from the fresh findings**: only four of the thirteen corpus hits were read;
the other nine are named from search metadata and asserted for nothing; the
comma-less and comma-free variants were not swept, so the population is larger
than thirteen and no exhaustiveness may be claimed; the Wallingford
identification as a pulp-fiction confidence man was not verified in a primary
source and must be checked or dropped before publication; CAP and
CourtListener disagree on the Whiteaker date (1926-07-20 against 1926-07-02)
and the official reporter should settle it.

**Selection outcome, stated so the author cannot mistake it**: the published
gallery stays at the five of §8.1–§8.5 — the cap of five governs, and this
family's "wrong noun appended" mechanism is the move §8.5 already carries —
**and this family remains the strongest documented substitute for any Gospel
entry, now with two whole-text attestations of the inversion's independence
where the first join had match-window citations only.** If the author
substitutes it, the Tracy independence datum and the four limits above travel
with it.

---

## 9. Interpretive-proposal audit

**Six proposals. Every one is selected from the `precedent-search` lane's
conjunction set and grounded in it, and its classification is carried through
unchanged.** That lane reached **eleven** distinct conjunctions against a floor
of six, **four of them not reached by the prior run at all**, so there is no
shortfall [PRE-016]. **No proposal is retained whose distinctive conjunction
that lane did not reach.**

**The coverage gap the prior brief had to record is closed** [PRE-016]. The
prior audit warned that its precedent lane had not re-searched the conjunctions
of the six then-published proposals. **This run's lane states expressly that
the five conjunctions currently published as P1–P5 correspond to PRE-004,
PRE-005, PRE-006, PRE-007 and PRE-009, so a synthesis that retains them is
covered by this sweep and not only by the prior run's.** P6 below is new and is
covered by PRE-011.

**An ordering honesty the lane requires be stated** [PRE-016]: **the lane ran
before this stage settled which proposals are retained, so its eleven are
searches of the precedent field the appointed elements invite, not searches per
retained proposal.** That is why the coverage is stated as a set rather than
one-to-one.

**The search boundary for every classification below** is §3.5 as widened at
§0.3(d), with the OCR caveats of [PRE-002] and [PRE-017]. **No classification
asserts that a connection is unknown, unprecedented, first, or authored by the
model**; "not located in the checked corpus" is bounded and correctable and
means only what it says.

### 9.1 — P1. Goods are ordered, not refused

| Field | Record |
|---|---|
| **Anchors** | Introit, Gradual, Gospel, Communion, Collect [`goods-ordered-not-refused`] |
| **Mechanism — CORRECTED this run, and the correction supplies the Gospel anchor the prior statement lacked** | The prior mechanism read "the chants comparatively … the readings exclusively". **That is inaccurate for one of the two readings** [THE-033]. **The Gospel carries BOTH registers, and the hinge inside it is the word `Ideo`**: the exclusive premise (`Nemo potest duobus dominis servire`; `Non potestis Deo servire, et mammonae`) is stated as **the ground of** the comparative argument that follows (`Ideo dico vobis, ne solliciti sitis`; `Nonne anima plus est quam esca: et corpus plus quam vestimentum?`; `Nonne vos magis pluris estis illis?`; `quanto magis vos modicae fidei?`; and the negated comparison at Solomon). **So the two registers are one argument and not two voices.** The register split is real **between the chants and the Epistle** — the Introit's `melior est dies una … super millia` and the Gradual's two `quam` comparatives against an Epistle that is wholly adversative (`adversus` three times, `adversantur`, `non perficietis`, `non estis sub lege`, `non consequentur`) and carries no comparative at all — **and the Gospel sits on both sides of it.** The comparative register is what keeps the exclusive one from reading as contempt for created goods |
| **Fruit** | A doctrine of ordered preference preached without contempt for creation; the reason the Mass can command an absolute exclusion and still promise that all things shall be added |
| **Precedent classification** | **NEAR ANALOGUE LOCATED** [PRE-004], reproduced unchanged, **and the widened corpus supplies nothing nearer** |
| **Nearest located analogue** | GPT leaf 43, "Temporal goods become a road only by changing grammar" (Coll., Off., Sec., Postcomm.) on `sic transeamus per bona temporalia, ut non amittamus aeterna`, as a means–end relay. Also GPT 41, "A good becomes dangerous when it becomes an exemption" (Coll., Ep., Gosp.); Claude postconciliar pc-s43 proposal 2; GPT postconciliar pc-s44, "A school of receiving" |
| **Why near and not exact** | The Third Sunday's ordering is stated in its own appointed Collect where this one must be reconstructed across chants the Collect does not mention; the nearest hit has no Gospel or chant anchor; and it has no "added unto you" verb. **The trustful-surrender articles PRE-003 adds to the corpus state the providence theme but join no two appointed elements of any formulary** [PRE-004] |
| **Search boundary** | §3.5 as widened: the eight missal artifacts, all 182 published Triptych documents, and **every interpretive-proposal file in the repository**. **Not reached:** any pre-Tridentine Latin commentary tradition, and the printed chant repertories, of which this repository holds none |
| **Controlling limit** | **A serious defeater the author must address or concede, and it is undiminished:** the comparative in Ps. 117:8–9 is arguably a **Hebrew idiom of exclusion** rather than of degree, in which case both registers are exclusive and the proposal collapses into the mammon reading. **THE-033 does not remove it, because the Gospel's own comparatives are Greek-derived and not the Hebrew idiom** [THE-048]. Either address it or state the proposal as contingent on the comparative reading of the Latin `quam`. Secondly, **the theological sweep's nearest lexically grounded set is `[introit, gradual, epistle, gospel]`, and the Epistle it reaches is not among the manifest's members**, so **the author should say which members carry lexical weight and which are thematic.** Thirdly, **this must not be built as "chants soften the readings": it is one unit, not a two-sided contrast.** Fourthly, **part of this proposal's content is now documented reception and must move out of it**: Jerome's `non dixit, qui habet divitias, sed qui servit divitiis`, with Aquinas repeating the distinction in almost the same words [PAT-123], **says in a Father's voice what P1 says in the guide's. That belongs in the detailed commentary, and what remains exploratory is the cross-element register claim and not the doctrine of ordered goods itself** |

### 9.2 — P2. What man cannot add

| Field | Record |
|---|---|
| **Anchors** | Gospel, Communion, Collect, Epistle [`what-man-cannot-add`] |
| **Mechanism** | `Adicere` carries the exchange: the Gospel denies that any man can **add** a cubit to his stature and then promises that all things **shall be added**; the Communion repeats the promise alone; and the Collect and Epistle supply the same incapacity in other words (`quia sine te labitur humana mortalitas`; `ut non quaecumque vultis, illa faciatis`). **What man cannot add to himself, God adds to him** |
| **Precedent classification** | **NOT LOCATED IN THE CHECKED CORPUS** as a Triptych treatment [PRE-005], reproduced unchanged, **with a near analogue newly located OUTSIDE the Roman rite** |
| **Nearest located analogue** | Same-identity: GPT leaf 54, "What is added does not become what leads" (Coll., Gosp., Comm., Postcomm.), itself classified there "not located in the checked corpus" — **but its mechanism is the three-verb distinction `adicientur`/`ad salutaria dirigatur`/`ducant`, not the incapacity.** Outside the identity: Claude leaf 48's commentary on `qui sine te esse non possumus` — commentary prose, not a proposal, with no Epistle or Communion anchor and no "add" verb. **NEW: the Ambrosian missal keeps both occurrences of the verb inside a single appointed pericope** (Mt. 6:27–33 as one Lenten ferial Gospel) [PRE-005] |
| **What the Ambrosian control does, and it cuts both ways** | **It shows that a Latin rite independently preserved the `adicere` pair as one unit, which supports the join; and it shows the pair can be carried without any of the Roman chants, Collect or Communion, which weakens the claim that the four-element Roman unit is doing the work.** *Evidence state:* searched OCR only; **the pericope's extent and the split point at v. 26/27 were read off a noisy layer and should be confirmed before printing** |
| **A REDUCTION this run forces, and it is the audit's most consequential change to a retained proposal** | **The core move is no longer exploratory. Aquinas makes it, on the same verse** [PAT-134]: `Hic probat experimento, quod sicut providet avibus, ita et nobis … Unde augmentum non est nobis ex nobis, sed ex Deo: unde de providentia Dei non debetis desperare.` **A Doctor reads the cubit as an experimental proof of providence and grounds growth in God and not in ourselves.** **That half is documented reception (class 3) and belongs in the detailed commentary at §2.5, not in Interpretive Possibilities.** **What remains a class-5 proposal is the cross-element half Aquinas does not make**: joining the incapacity to the *promise* two verses later, to the Communion's repetition of the promise alone, and to the Collect's `sine te labitur humana mortalitas`. **The proposal is retained in that reduced form and must be published in it.** A proposal that presented the incapacity-as-providence reading as the guide's own would be putting an editorial proposal where a Doctor's teaching stands |
| **A second reduction, in the other direction** | **The Roman orations themselves use `adicere` for exactly the divine supplement P2 reads off Matthew**: the **Eleventh** Sunday's Collect asks God to `adicias quod oratio non praesumit` [THE-039], and a normalised sweep over the 21 collated records finds `adici-` **only** in the leaf-51 and leaf-54 records. **This STRENGTHENS the proposal by showing the doctrine is idiomatic and not imposed, and WEAKENS its novelty, because the conjunction is less distinctive once a neighbouring formulary's oration states it. Both must be said.** What limits the strengthening: `adicias` there governs `quod oratio non praesumit`, a thing prayer does not ask, where Mt. 6:33's `adicientur` governs food and clothing — **the objects are not the same and the overlap is the verb plus the agent, not the gift.** This does **not** contradict PRE-005's boundary statement, which is about interpretive proposals; **it adds an appointed-text occurrence the boundary does not cover** |
| **Search boundary** | §3.5 as widened. The cubit/`adicere`/`staturam` anchor occurs in **no interpretive proposal anywhere in the checked corpus** outside the two Fourteenth-Sunday leaves. **Not reached:** sermon literature generally |
| **Controlling limit** | **Neither the Collect nor the Epistle uses the verb**, so the four-element unit rests on a **doctrinal and not a lexical join at those two members — a weaker join than P4's and P6's, and it must be stated as such.** Evidence-state caveat unchanged: the Benziger OCR spells the root `adiicere` in all three places, and **a writer quoting the Benziger form must not present it as a tense variant without checking a page image**, that artifact being `storage='remote'` with no payload |

### 9.3 — P3. Propitiation and salvation saturate the prayers the people do not sing

| Field | Record |
|---|---|
| **Anchors** | Collect, Secret, Postcommunion, Alleluia [`propitiation-and-salvation-saturated`] |
| **Mechanism** | The three orations and the Alleluia carry vocabulary no other element does, and the distribution is now exact [SCR-030, SCR-022]: **`salut-`/`salv-` occurs four times in the whole formulary, once each in Collect (`ad salutaria dirigatur`), Alleluia (`Deo salutari nostro`), Secret (`haec hostia salutaris`) and Postcommunion (`ad perpetuae ducant salvationis effectum`), and in none of the Introit, Epistle, Gradual, Gospel, Offertory or Communion**; `propitia-` twice, Collect and Secret only; `semper` twice and `perpetu-` twice, Collect and Postcommunion only. **So the sung and read elements state the problem in the language of service, trust and anxiety while the priest's own prayers state it in the language of expiation and rescue — and the Alleluia's `salutari` is the single word tying the day's one purely jubilant chant into that thread** |
| **Fruit** | The Mass has two registers of address, and the reader who follows only the readings hears only one of them; **it also explains why the Alleluia, the formulary's least lexically integrated element, is not simply decorative** |
| **Precedent classification** | **NEAR ANALOGUE LOCATED** [PRE-006], reproduced unchanged; **nothing nearer in the widened corpus** |
| **Nearest located analogue** | Claude leaf 53, "The two askings of *augmentum* bracket the nine who stopped" (Coll., Postcomm., Gosp.), classified in that leaf "near analogue located"; leaf 53's commentary on `Propitiare, Domine, populi tui propitiatus muneribus`; GPT 52/53's source-grounded sections treating propitiation doctrinally at the Secret with Trent session XXII |
| **Why near and not exact** | **The precedented move is reading one repeated Latin word as a bracket across a formulary's orations. What is not precedented is doing it across three orations plus a chant, nor with this vocabulary** |
| **A refinement the audit adopts, which P3's block treatment obscured** | **The Collect and the Postcommunion are the only two elements carrying `semper` and `perpetu-`, and each carries both, so the day's first prayer and its last form a lexical bracket in the vocabulary of duration — while the Secret between them carries neither** [THE-046]. **The Secret, the one oration said over the gifts, is the one that does not ask for anything perpetual, and asks instead for purgation and propitiation here and now.** That asymmetry is real and should be published inside P3 rather than flattened by it |
| **Search boundary** | §3.5 as widened. **Not reached, and still not run:** any lexical concordance over the orations of the whole missal. The precedent lane states expressly that **it ran phrase and fragment searches and not a lexical concordance, and that the OCR calibration of §3.5 means a concordance over the Pustet layer would in any case undercount** [PRE-006] |
| **Controlling limit** | The vocabulary of the three orations is the standard vocabulary of Roman collects generally, **so the saturation may be unremarkable.** **The counter-test was run and it holds, but only narrowly:** the substantive `propitiatio` appears in the appointed Latin of **no other** formulary among the fifteen collated, the one apparent counter-example being English audit prose in the GPT leaf-46 record and not appointed text [THE-009]; **but the wider `propiti-` family reportedly hits eleven of the fifteen**, so the claim is specifically about the **substantive** and collapses if restated about the word-family generally — **and that eleven-of-fifteen figure is carried from the prior run and was NOT re-verified this run** [THE-009]. **Fifteen collated formularies is the sample, not the missal.** And **this proposal is invisible in the guide's registered English witness**: Cummiskey 1861 drops `propitiatio` at the Collect, turns it into a verb at the Secret, and drops both `semper` and the substantive at the Postcommunion, **so every measurement supporting it must be conducted on the Latin.** A stem caveat: `salutaris` of a victim and `salutaria` of things that save are related in form and not identical in sense, **and a guide leaning on the four-fold count must say so** [SCR-030] |

### 9.4 — P4. The hope-formula lies past the cut, and is handed on at another Mass

| Field | Record |
|---|---|
| **Anchors** | Introit, Gradual, Offertory [`hope-formula-past-the-cut`] — **membership upheld at §0.3(g)** |
| **Mechanism, now bounded across the whole Vulgate** | **The formula `beatus [noun] qui sperat` stands in exactly two verses of the entire Clementine Vulgate — Ps. 33:9b and Ps. 83:13 — and those are precisely the two psalms supplying this Mass's Offertory and Introit** [SCR-016]. Widened to `beat\w+ (\w+ ){0,3}(spera\|confid)` the only further verse in the Bible is Ps. 2:13. It lies **past the Introit antiphon's cut at v. 11a and past its psalm verse's cut at v. 3a**; **one clause past the Offertory's cut at v. 9a**; and **the Gradual alone sings the hope vocabulary outright**, `sper-` and `confid-` occurring twice each there and in no other element. **Three appointed excerpts stop short of the same formula and a fourth sings it. The Introit belongs because the formula lies beyond both its boundaries, not because it uses hope vocabulary — which it does not** |
| **Fruit** | The formulary's chief coherence is a shared editorial boundary, and it is verifiable rather than thematic; it also gives the Gradual, the day's plainest maxim, a structural role it does not obviously have |
| **Precedent classification** | **PRECEDENT LOCATED** [PRE-007], **and the prior audit's classification was UNDERSTATED as to which precedent is nearest** |
| **Located precedent — CORRECTED this run** | The prior audit named Claude leaf 51 and Claude postconciliar pc-s42. **The nearest instance is one leaf nearer: Claude leaf 48's own proposal 5**, "A withheld condition and a partial mode of knowing (Ep. + Comm.)", which **anchors on the very same Ps. 33 verse** (`Communion Gustate et videte`), performs the identical "the cut is the meaning" move — "It hands the congregation an inheritance and stops one clause short of the terms on which the inheritance is held … the truncated verse is not an accident of length" — **and states in advance the identical defeater this proposal must concede**: "If the pericope division is inherited from an earlier lectionary for reasons of length or of the ancient Roman station, then nothing is being withheld and this proposal collapses into a coincidence of scissors." **Consequence for the author: P4's method and its candour are a house convention, not a novelty, and a worker who presents that concession as newly conceded would be overstating it** [PRE-007] |
| **What the prior audit got right, and it stands** | Leaf 48's proposal 5 **nowhere mentions `beatus vir qui sperat in eo`, nowhere mentions the Fourteenth Sunday's Offertory, and nowhere notices that the hope-formula it declines to discuss is the very clause the other Mass cuts. The join is indeed available and unmade** [PRE-007] |
| **The control, now upgraded from a sibling collation to two tracked primary printings** | **Six Sundays earlier the same Psalm 33 verse is appointed with the hope clause this Offertory stops before.** The prior brief could rest this only on a sibling provider's collation and a second agreeing record, "not from a page image". **It now rests on the Pustet Ratisbon 1862 and the Venice 1570 text layers, both tracked**, each printing the Eighth Sunday's Communion `Gustate et videte … beatus vir qui sperat in eo` whole, and the Venice 1570 printing the Fourteenth Sunday's Offertory stopping at `Dominus` immediately before this formulary's Secret [PRE-008]. **This also independently reproduces the two-Roman-Offertory-uses figure in a witness 292 years earlier than the Pustet, which makes it a stable feature of the Tridentine book rather than an artefact of one printing** |
| **Search boundary** | §3.5 as widened, plus the 21 collated `verified.md` records. **Bounds on the control:** the upgrade is to *searched* and not to *inspected* — **neither reading was collated against a page image**, and **the Venice 1570 text is column-interleaved by the OCR, so the running head "dominica nona post pentecosten" beside the Eighth Sunday's Communion is layout noise and must not be read as the antiphon's assignment** [PRE-008]. The "no third Roman Offertory use" negative remains weak per §3.5 |
| **Controlling limit** | **The strongest limit is that the antiphons' extents are inherited chant tradition and the cuts were not made to suppress anything.** `scripture-context` flags explicitly that the three cuts have duller explanations — metrical length, the ordinary bounds of an antiphon — and **that no intent is established by anything in that lane** [SCR-016]. Secondly, `confidere` is a trust word rather than a hope word strictly: a stricter `spes`-vocabulary count finds `sperare` twice in the Gradual and nothing else, **a slightly different and weaker statement.** Thirdly, **Ambrose quotes the fuller verse in the fourth century**, which sharpens the observation about the Roman cut and says nothing about why it was made |

### 9.5 — P5. Two chants, two divisions: the Fathers disagree at the Offertory and at the Gradual, and the formulary resolves neither

| Field | Record |
|---|---|
| **Anchors** | Offertory, Gradual [`fathers-divided-on-angel-and-comparison`] |
| **Mechanism — materially stronger this run, because both divisions are now three-way or two-language** | Each of the two chants carries an **independent** documented division and the Mass prints both without adjudicating. **At the Offertory:** Augustine argues about which noun governs the verb, defending `Immittet Angelus Domini` against "some bad copies", and identifies that Angel as Christ — **while Cassiodorus, the principal medieval Latin commentator, reads the same verse and does NOT make the christological identification, turning instead to the moral sense** [PAT-203]; **and Cassiodorus's own lemma reads `Immittet angelum Dominus`, the very reading Augustine denounced** [PAT-201]; **and the verse is attested by Cyril and Ambrose, and still sung in the Mozarabic rite, as a COMMUNION chant while the 1962 book assigns it to the offertory** [PRE-010]. **At the Gradual:** three positions on what the princes are — Augustine's good angels, Cassiodorus's devil-and-good-angel, Theodoret's earthly rulers whose authority is temporary [PAT-305]. **The angel who is the Mass's rescuer at one chant is the Mass's excluded object of trust at the other, and the Fathers reached each position separately** |
| **Fruit** | A cross-chant tension genuinely in the sources and not manufactured, which the formulary's own arrangement stages; and a way to treat the Offertory's angel without either flattening the christological identification or asserting it |
| **Precedent classification** | **NEAR ANALOGUE LOCATED** [PRE-009], reproduced unchanged; the widened corpus adds no nearer instance |
| **Nearest located analogue** | Claude leaf 51's source-grounded section, "The tradition genuinely disagrees at four points, and the formulary resolves none of them", closing "They yield different sermons, and the guide prints them as four positions rather than one consensus"; leaf 53 on `in manu mediatoris` producing two surviving readings with Aquinas declining to choose. **The angel/princes division itself is documented only in the GPT edition of this identity**, "The angel and the princes distinguish mediation from mastery" (Grad., Gosp., Off.), classified there "near analogue located" |
| **Why near and not exact** | The precedented move is treating a documented division as itself the cross-element unit. **What the Claude collection does not show is doing it where BOTH members of a two-chant pairing carry independent divisions** |
| **The genre-displacement half, and how far it may be pressed** | **PRE-010 packs two classifications and they must not be merged.** (i) **As liturgical fact the displacement is well precedented and a worker must not present it as a discovery**: the Mozarabic *Missale mixtum* prints `Gustate et videte quam suavis est Dominus` as the *ad accedentes* chant at communion, and leaf 48's own aside that "`gustate et videte` is the commonest of Communion antiphons" is the nearest thing in the Triptych corpus to the observation. (ii) **As a Triptych treatment joining two appointed elements, it is not located in the checked corpus** — a negative sweep for "assigned to the offertory\|as an offertory" returns zero across all 2,865 indexed files. **A sharp caution on the sources:** the second Mozarabic citation printing the verse whole with the hope clause is from the "Saec. XI monumenta liturgica" section of PL 85, **an eleventh-century Roman-FORM votive collection printed in the same volume and not the Mozarabic rite**, given away by its Graduale/Offertorium/Communio vocabulary; **the genuine Mozarabic witness reads `quam suavis` where the Roman book reads `quoniam suavis`**, and the OCR is poor enough that **neither reading is safe to quote as Latin without a page image** [PRE-010] |
| **What this run adds to the Offertory half, and it lifts a limit** | **Cassiodorus's eucharistic reading is anchored in the appointed verbs `Gustate` and `videte` themselves**, where Augustine's is anchored in the psalm's superscription the antiphon does not print [PAT-202]. **So the eucharistic reading is now available to a hearer of the antiphon alone, which it was not before** |
| **Search boundary** | §3.5 as widened. **Not reached:** Migne PL 37 itself, **which this repository DOES hold as a complete hashed public-domain volume covering Pss. 80–150** [COV-005] but which no lane opened, so the accusative/ablative variant at the Gradual is still unresolved (§2.3) |
| **Controlling limit** | **The cross-relation between the Gradual's absolute exclusion and the Gospel's `Nemo potest duobus dominis servire` is a lead and not Augustine's claim: he does not cite Mt. 6:24 at that locus.** The Offertory half carries four limits: Augustine's text differs from the missal's at the following verb (`eruet`/`eripiet`), **which is evidence the missal's text is not simply his**; the missal's capital `Angelus` is orthography and **does not encode** his identification, **and Cassiodorus is positive evidence a Latin reader could take it otherwise**; Cyril's authorship is disputed and unswept; and **the Mozarabic evidence is searched OCR of a poor layer.** The Gradual half's three-way division is secure, **but Augustine and Cassiodorus both reach Michael in Daniel, so between those two the shared proof-text is probably dependence and not independent invention** [PAT-211]. **All Latin witnesses are transcriptions and the Greek a TLG transcription; none collated against Migne** |

### 9.6 — P6. The one verb the Mass appoints twice, with its object reversed

| Field | Record |
|---|---|
| **Anchors** | **Introit (psalm verse), Epistle.** New this run [PRE-011, SCR-023, THE-034] |
| **Mechanism** | **`Concupiscere` stands three times in the appointed text, in exactly two elements, with opposite objects.** The Introit's psalm verse has the **soul** concupiscing *toward* the courts of the Lord — `concupíscit, et déficit ánima mea in átria Dómini` — and the Epistle has the **flesh** concupiscing *against* the spirit — `Caro enim concupíscit advérsus spíritum` — and closes on `cum vítiis et concupiscéntiis`. **The shared form is an identical third-person singular present indicative, verifiable in the tracked Latin** [SCR-023]. **And the pairwise map bounds it: `christi` and `concupiscit` are the ONLY two content-word ties between the Introit and the Epistle in the whole formulary** [SCR-022]. So the formulary's doctrine is that **desire is redirected rather than abolished, and it says so lexically and not only thematically** |
| **The detail that makes it more than a coincidence of vocabulary, and its own asymmetry** | **The clause one word past the Introit's cut supplies `caro`** — Ps. 83:3b, `cor meum et caro mea exsultaverunt in Deum vivum` — **so the Epistle's governing sentence uses exactly the two words that stand on either side of the Introit's boundary, with the valuation reversed** [SCR-023]. **But the asymmetry must be printed with it and it weakens any strong reading:** `concupiscit` is **inside** the appointed Introit text, and **`caro` is NOT** — it lies one clause past the cut, so a hearer of the appointed chant alone never hears it. **The relation is between the Epistle and the Introit's SOURCE PSALM as much as between two appointed texts, and a guide using it must say which** |
| **Fruit** | The lexical backbone P1 lacks: the formulary does not refuse desire, it names the same act with two objects and prefers one. **And it gives the Introit's psalm verse — otherwise the element most easily treated as ancillary — a place in the argument** |
| **Precedent classification** | **NOT LOCATED IN THE CHECKED CORPUS** as a treatment; **NEAR ANALOGUE LOCATED** for the method [PRE-011] |
| **Nearest located analogue for the method** | Claude leaf 49, "The granted prayer is the danger the Collect is built against", anchoring the Collect's `fac eos, quae tibi sunt placita, postulare` against the Epistle's `Non simus concupiscentes malorum` — **a published proposal built on precisely this root, joining an oration to a reading** |
| **Why the conjunction itself is not located** | **The string `concupisc` occurs ZERO times in all 2,269 lines of the prior brief**, so no lane of the prior run reached it and its §9 does not list it among its eight conjunctions [PRE-011]. **Three lanes of this run reached it independently** — `scripture-context` at the shared finite form and the asymmetry, `theological-synthesis` at the per-element counts and the cross-proper control, `precedent-search` at the classification — **which is the strongest convergence in the run on any single conjunction** |
| **Cross-proper control** | A normalised sweep over the 21 collated records finds `concupi-` in the appointed text of **only one other identity**, the Ninth Sunday after Pentecost, at 1 Cor. 10:6 `Non simus concupiscentes malorum, sicut et illi concupierunt` — **where the valence is negative only** [THE-034]. **The reversal is peculiar to this formulary within the collated set**, and the sample is fifteen identities and must be named |
| **Search boundary** | §3.5 as widened: the eight missal artifacts and all 2,865 indexed Triptych files. **Not reached:** any Latin concordance of the Vulgate psalter against Galatians, **and any patristic locus joining the two, which is the reception lane's ground and was not swept** [PRE-011] |
| **Controlling limit** | **The two senses are the ordinary Latin senses of an ordinary verb**, whose neutral-to-negative range is unremarkable, **so the opposition may be a coincidence of the Vulgate's vocabulary before it is a compositional choice, and no compiler's intent is claimed** [SCR-023, THE-034]. **The Introit's occurrence is in the PSALM VERSE and not the antiphon**, so it is liable to be omitted where the verse is not sung, **and §0.3(g)'s adjudication about which Introit boundary counts bears on that** [PRE-011]. **The `caro` half lies past the cut and must be labelled as the source psalm's, not the appointed chant's.** And **§2.2's defeater applies with full force** [THE-049]: no checked witness read this Introit beside this Epistle, so this is a claim about how the 1962 formulary reads when taken whole and never about how the tradition read the two texts together |

### 9.7 Conjunctions reached and **not** retained as proposals

| Conjunction | Classification carried | Disposition |
|---|---|---|
| `sunday-number-not-the-mass-own` [PRE-015] | **PRECEDENT LOCATED** | **Routed to source-grounded synthesis as claim C4** (§7.4). It restates a neighbouring guide's sourced finding and joins no two appointed elements by a mechanism of its own. §0.3(i) |
| **The Offertory's genre displacement** [PRE-010] | **PRECEDENT LOCATED as liturgical fact; NOT LOCATED IN THE CHECKED CORPUS as a Triptych treatment** | **Folded into P5 rather than retained separately**, because its Offertory anchor and its patristic division are P5's and publishing both would run one datum twice. **Its liturgical-fact half must be presented as well precedented and never as a discovery** |
| **`Idolorum servitus` to mammon** [PRE-012] | **NOT LOCATED IN THE CHECKED CORPUS** | **Not retained as a proposal; routed to the detailed commentary at §2.2.** The material is already in the brief as documented reception, and **the bridge is a Father's moralising gloss and not the lesson's plain sense**, so a worker building on it builds on reception. **Two further weaknesses:** `servire` is a noun-phrase genitive in the Epistle and a finite-verb complement in the Gospel, **so the shared root is weaker than it looks** [PRE-012]; and **the newly documented scriptural warrant** — both other Vulgate occurrences of the formula gloss avarice [SCR-027] — **makes the gloss less arbitrary but does not make the Epistle-to-Gospel bridge the liturgy's.** The negative sweep is clean: `idolorum servitus` returns exactly one hit outside this leaf, at the Ninth Sunday and on a different verse; `duobus dominis` returns zero outside this leaf |
| **Both readings' supplied incipits** [PRE-013] | **NEAR ANALOGUE LOCATED** | **Not retained, and the reason is the lane's own severe limit:** liturgical incipits are near-universal formulae of the Roman lectionary rather than choices made for this Mass, **so the conjunction risks being a fact about the book and not about the Sunday.** The defensible narrow version — that at this Mass the supplied words do specific and different work at each reading, one displacing a connective that carries Paul's argument and the other narrowing an audience Matthew left wide — **would have to be stated as an effect on the hearer and never as evidence about a compiler**, and leaf 49 already does the single-reading version in commentary with the displaced clause printed in brackets. **Retained as textual observation at §2.2 and in the Gospel's incipit note, and as a reusable form leaf 49 supplies** |
| **The Ambrosian split pericopes and the Solomon pairing** [PRE-014] | **NOT LOCATED IN THE CHECKED CORPUS** | **Not retained as a proposal: it joins no two appointed elements of *this* formulary.** It is comparative evidence and is routed to §6.9 as a competing historical judgment, **with the lane's four limits printed there** |
| `fruit-count-unsettled` | **NOT LOCATED IN THE CHECKED CORPUS** (prior run) | **Dropped as a proposal; retained as documented reception at §2.2, where it is now much richer.** §0.3(h) |
| The Introit incipit across three genres [PRE-024, prior run] | **PRECEDENT LOCATED** | **Not retained: it joins only one appointed element of this formulary and the profile requires at least two.** Retained as textual observation and as a retrieval warning at §2.1 |
| The Introit against Ps. 83's other Roman use | **PRECEDENT LOCATED** | Same disposition; retained at §2.1, and independently reproduced this run by THE-035's cross-proper sweep |

### 9.8 Two readings that do NOT clear the two-element floor, recorded so nobody revives them as proposals

[THE-041, THE-043, THE-050]. **The law inclusio** — `lex`/`leg-` confined to the
Epistle's two negative clauses, bracketing the two catalogues — and **the
fourfold `adversus`**, likewise confined to the Epistle, whose fourth occurrence
reverses the sense of the first three. **Both are confined to one appointed
element and neither may be published as an interpretive proposal.** They are
readings of the Epistle's internal structure and belong in the element-by-element
commentary. **This is the same floor that drops `fruit-count-unsettled` and
refuses the Introit-incipit conjunction.** The law inclusio could clear the floor
only if joined to a second element by a mechanism, and the nearest available join
is doctrinal rather than lexical — the Gospel's `iustitiam eius` against the law
that has nothing to say against the Spirit's fruit — **which this brief does not
retain.** And in both cases the defeater is the same: **it is Paul's own frame in
Galatians 5 and the missal took the pericope whole.**

### 9.9 Form note, offered and not required

The target has not adopted GPT leaf 54's dated `### Targeted search boundary`
subsection listing the literal Latin strings searched [PRE-018]. **That is what
makes a negative correctable by someone else, and this run supplies two live
demonstrations that it matters more than the prior run could show**: `circuitu
timentium` and `venite exsultemus Domino` **both return zero from books that
demonstrably print both** (§3.5). **The observation is stronger now than when it
was made, because the widened corpus adds five artifacts whose OCR is worse than
the Pustet's.** The profile does not mandate the form, and this brief records
its boundaries in prose at §3.5 and per proposal above instead. **Whether the
target adopts it is an authoring decision.**

### 9.10 Fresh precedent classifications, run `e5b24f405bde9691` (2026-08-31)

The fresh precedent lane re-ran its conjunction sweep against the widened
corpus and returned eleven classifications [fresh:PRE-001–fresh:PRE-011].
**They are recorded here with the anchors, mechanism, nearest located
precedent or analogue, search boundary and controlling limit each finding
carries, and each classification is carried through unchanged.** The first
join's classifications at §9.1–§9.6 are not superseded: every fresh
classification that reaches a retained proposal corroborates it, and the two
that add substance are flagged.

| Fresh id | Conjunction | Classification | Disposition in this brief |
|---|---|---|---|
| fresh:PRE-001 | The same-identity precedent field | — | The sibling GPT leaf for this Sunday carries five proposals over the same elements, four near analogue and one not located; read in full at its interpretive section only. Confirms §9.1–§9.6's precedent map |
| fresh:PRE-002 | One choice in two grammatical registers (comparative chants, exclusive readings) | **NEAR ANALOGUE LOCATED** | Same family as P1's register claim. Nearest: a postconciliar sibling's Collect means–end relay (`sic transeamus per bona temporalia`) and GPT 41's ordered-goods proposal; **no checked witness makes the two-register join**. Bounds: sermon literature generally not reached, including Anthony of Padua's sermon for this very Sunday; no lexical concordance over chant incipits. Available to the author inside P1, not as a separate proposal |
| fresh:PRE-003 | What man cannot add | **NOT LOCATED IN THE CHECKED CORPUS** | **Confirms P2's classification** with a bounded search (both providers' 1962 interpretive files; the appointed-text and commentary occurrences inside the two 54 leaves are expected and not counterexamples). Not reached: sermon literature including Anthony's Sunday XIV sermon, and any patristic homily series on Mt 6 |
| fresh:PRE-004 | Propitiation and salvation saturating the unsung orations plus the Alleluia | **NEAR ANALOGUE LOCATED** | **Confirms P3's classification**; the substantive `propitiatio` appears in no interpretive proposal of either provider's 1962 collection outside this leaf. Nearest: leaf 53's shared-noun oration bracket. Not reached: a lexical concordance over the whole Missal's orations |
| fresh:PRE-005 | The hope-formula past the cut, handed on at another Mass | **PRECEDENT LOCATED** | **Confirms P4's classification and adds registry evidence the leaf nowhere records**: the tracked 1962 registry gives this Sunday's Gradual verses a second appointment (Friday of the Fourth Week of Lent, Gradual `Bonum est confidere in Domino`, after lesson 1 Kings 17:17–24) and the Introit's psalm text three further second uses as Gradual/Second Gradual (Monday of the First Week of Lent, lines 3158/3558; the Lent and September Ember Saturdays), while corroborating the two known Ps. 33:8–9 second uses and the Eighth-Sunday control. **The author must not present any of these chants as single-use; §7.4 and the chant commentary must carry the multiple appointments.** Bounded: the sweep covers the tracked 1962 registry only, not the pre-1955 or 1570 artifacts |
| fresh:PRE-006 | The Sunday number is not the Mass's own | **PRECEDENT LOCATED** | Confirms the C4 routing (§7.4). **Adds a new witness: the registry gives the S. Caietani Confessoris formulary (1962-08-07) the same Gospel, Mt. 6:24–33** — a second 1962 Mass hearing this Gospel, relevant to any claim about the Gospel–formulary bond; the leaf nowhere mentions it (bounded negative over the leaf's tracked files). Anthony of Padua's Dominica XIV sermon, taking the Thirteenth Sunday's Gospel under this number, remains the historical control for the displaced numbering |
| fresh:PRE-007 | The Fathers divided at both chants, and the formulary resolves neither | **NEAR ANALOGUE LOCATED** | **Confirms P5's classification**: the precedent for presenting a documented division as itself the cross-element unit is leaf 51; the two-chant-pair form is attested only in the sibling GPT leaf, which joins the chants through the Gospel's master-saying, not through two divisions. The Gradual half's ablative/accusative variant still needs PL 37 checked (§9.5's boundary; not re-verified, the lane did not open PL) |
| fresh:PRE-008 | The chant or psalm supplies the referent the Gospel leaves unnamed (Mt 6:26 birds, 6:28 lilies) | **NEAR ANALOGUE LOCATED; CONJUNCTION OPEN** | **A reached conjunction this brief does not retain as a proposal**: the nearest precedent is postconciliar pc-s42 proposal 6, the same shape for another Gospel, and a two-provider search for the birds/lilies wording returns no leaf making the join for this Sunday. **It is available to the author within the profile's four-to-six range only by substituting for an existing proposal**, and it carries the pc-s42 limit pattern (an unchecked witness may already read the birds doctrinally) and the profile's rejection of generic applications. Recorded so the conjunction's precedent search is not lost |
| fresh:PRE-009 | The Communion repeats the day's Gospel | **PRECEDENT LOCATED (against the proposal)** | **Negative control, unchanged**: repository precedent treats Gospel-sourced Communion antiphons as ordinary practice, so no proposal may rest on the repetition as such; C5's recasting, not the reuse, is the substantive |
| fresh:PRE-010 | The two consecutive Sundays' Galatians lessons and the two Collects' shared sine-te incapacity grammar | **NOT LOCATED IN THE CHECKED CORPUS** | Reached and not retained: the leaf records the adjacent-Sunday material only as historical orientation, the Fifteenth Sunday's Collect (`quia sine te non potest salva consistere`) and its Gal. 5:25–6:10 continuation are registry facts, and **no interpretive join exists in the checked corpus**. Not reached: sacramentary scholarship on whether the two Collects share a compositional family. Remains a lead under §9.7's discipline |
| fresh:PRE-011 | The proposal-schema structure itself | — | The target's newer schema (explicit Precedent / Search boundary / Controlling limit fields) remains the working structural precedent; the leaf's relation keys match the six conjunctions the fresh sweep covered. No action for this stage |

**Net effect on §9.1–§9.6**: every retained proposal's classification is
reproduced by the fresh sweep, P2's and P3's and P4's and P5's with fresh
corroboration and P4 with the fresh registry additions of fresh:PRE-005
recorded above. **No proposal's conjunction is left unreached by some
precedent search of this workflow**: P1's register claim is covered by
fresh:PRE-002, P6's by the first join's [PRE-011 in the first join's
numbering, at §9.6], re-verified textually this run by fresh:THE-102 and
fresh:SCR-014.

---

## 10. Section-by-section evidence coverage

**Required by this stage's own fragment. It is a statement of fact and not a bar
to clear.** For each position of the `Reader-Facing Order` in
`guidance/liturgy/roman-1962-propers.md` that carries reader-facing content,
this states whether **this brief supplies the evidence that section needs**, and
names every section for which it does not. **A `PASS` asserts that every one of
these sections has its evidence position stated. It does not assert that every
one of them has evidence.** Where evidence is not supplied, the entry names the
corpora, languages and loci checked and the limit reached, **and the guide
carries that bound in place of the claim.**

**All twelve positions of the reader order are stated below.** The prior brief
listed ten and did not state a position for **position 4, the complete appointed
text**, or **position 6, `Source-Grounded Synthesis Across the Propers`**.
**Silence is the one thing this statement may not do, so both are stated here.**

| # | Reader-order position | Supplied? | What is supplied, or the bound that stands in its place |
|---|---|---|---|
| 1 | **Page 1: Propers map and four senses** | **YES — and the one named constraint the prior brief carried is now RELIEVED** | The complete element inventory with incipits, scriptural axes and demonstrable connections (§1.1, §1.2, §1.4); the appointed Latin as `verified.md` settled it. **Four-senses grounding: Literal** from §2.1–§2.7 throughout; **Allegorical** — **and this is the change** — from a **named, checked, patristic allegorical reading of the pericope's own images**, Hilary of Poitiers reading birds, cubit, lilies and hay [PAT-111, PAT-112], **printed beside Jerome's and Augustine's refusals**, so the row rests on the tradition's own division and not on the guide's invention (§0.3(c), §7.3); also available, Augustine's christological reading of `faciem Christi tui`, Cassiodorus's naming of it as hypallage [PAT-206] and Theodoret's ecclesial third reading [PAT-301], and **Cassiodorus's eucharistic reading of `Gustate` anchored in the appointed verbs** [PAT-202]. **Moral** from Jerome's Greek-anchored philology of the vice-list [PAT-159], Chrysostom and Aquinas on both lists, and the **three** independent Fathers setting the limit against over-reading the Gospel, of whom **Jerome's is anchored inside the appointed bounds and is the one to prefer** [PAT-124]. **Anagogical** from Augustine's and Cassiodorus's "one day, an everlasting day" [PAT-207], **with Theodoret's contrary argument-from-profit printed beside it** [PAT-302]. **The constraint that remains, and it is Hilary's own:** his hay-as-gentiles reading carries a doctrine of the bodily eternity of the damned, and his birds-as-unclean-spirits reading works against the pericope's consoling sense; **report the reading and do not use it to soften the doctrine it carries** |
| 2 | **Page 2: `Scriptural Date and Location`** | **PARTIALLY — and this remains the one section for which the brief does not supply part of the evidence. One item is newly relieved and one statement is corrected** | **SUPPLIED in full for the traditional attribution and chronology in every one of the six rows**: superscription and authorship evidence [SCR-012, SCR-013, SCR-015, SCR-019]; the PBC responsa I–VIII, AAS 2 (1910) 354–355, verified, public-domain; Corbett, CE IV, verified, matching the registered passage exactly; Maas, CE VIII, verified; Cornelius a Lapide, Antwerp 1614, verified; the Douay 1 Kings 21 = 1 Samuel 21 correspondence **with the Achimelech/Achis divergence inside the narrative now recorded and unexplained** [SCR-015]; the Vulgate/English/Hebrew numbering read from the tracked concordance. **NEWLY AVAILABLE, and it relieves one of the seven bounded negatives:** the **acrostic structure of Ps. 33/34** may now be carried **as documented reception** — Cassiodorus states it and tags the appointed verses HETH and TETH [PAT-204] — **but NOT as a fact about the Hebrew, no Hebrew being held** (§2.6, §4.5). **Also newly available for the Alleluia row:** Theodoret's report that Ps. 94 is **untitled among the Hebrews** and his Josiah setting, both **his own reconstruction and not what the psalm states** [PAT-304]; and for the Gradual row, Theodoret's psalm heading Ἀλληλούϊα agreeing with the tracked Clementine [PAT-306]. **STILL NOT SUPPLIED, each with its bound:** (i) **a modern critical horizon for Mt. 6 and for Pss. 33, 83, 94 and 117** — no registered NABRE artifact for Matthew or for NABRE Pss. 34, 84, 95, 118, **so there is nothing here to cite or to summarise from**, and no lane retrieved a substitute; (ii) **the content of the Catholic Encyclopedia articles "Gospel of St. Matthew" (`cathen/10057a.htm`) and "Epistle to the Galatians" (`cathen/06336a.htm`)** — citable in form at an exact article locus, **retrieved by no lane in either run**, so the guide may not assert what either says; (iii) **Papias, Eusebius *HE* III.24.6 and III.39.16, and Jerome *Comm. in Gal.* lib. II prol.** — **not held in this repository in any form**, re-confirmed this run [COV-010]; (iv) **Theodoret on Ps. 83 and Ps. 94, and Irenaeus *Adv. haer.* III.1.1** — **Theodoret is now READ IN GREEK at both psalms** [PAT-300], so the dossier may cite him at PG 80 with the route and state stated, **but there is still no registered passage record**, and Irenaeus is still held as searchable bytes with no passage record [COV-010]; (v) **Jerome *De vir. ill.* 3** — registered at ch. 2, an English edition against a claim of Latin reading, artifact no longer byte-reproducible; (vi) **Haydock's A.M. 2944** — `rights_status='unresolved'`, summarise-only. **CORRECTED:** the References' flat statement that "no critical edition is registered here" is imprecise — **two are, and neither reaches an appointed passage**, which is what should be said [COV-009]. **The disposition for every unsupplied item is a bounded negative printed on the page. The author does not retrieve.** **And the structural warning stands:** the sheet must occupy exactly one page, and these bounded negatives can be stated briefly and should not become another layer of argument on the page |
| 3 | **`The Propers: Themes and Movement`** (pages 3–4) | **YES** | **Six cross-proper claims at §7**, each joining at least two precisely named appointed elements of this formulary and each drawing multiple ritual moments, scriptural contexts and reception witnesses, with class, limits and defeaters. **Three to five developed functional units can be built from them, and §7's preamble names the strongest argument and its shape.** Every appointed element is accounted for: Introit (C4 second remove, P4, P6), Collect (C4, C6, P2, P3), Epistle (C1, C2, P6), Gradual (P4, P5), Alleluia (P3, and §2.4's negative), Gospel (C1, C2, C3, C5, C6), Offertory (P4, P5), Secret (C4, C6, P3), Communion (C1, C3, C5, C6), Postcommunion (C4, C6, P3). **A signpost-only scan can recover thesis, movement, decisive evidence and principal limits from §7's preamble plus the six claim headings** |
| 4 | **The complete appointed text** (research edition only, opening page 5) | **YES — and it needs nothing from this brief beyond what is already fixed** | **This position is textual, not evidential.** Its control is `propers/verified.md`, the facsimile-collated appointed text in liturgical order with its provenance, **not this file** — and §1.1's inventory, §1.2's collation results and §1.3's numbering are the brief's complete contribution to it. **The one thing the brief must supply and does: the divergence apparatus.** The four Communion departures [SCR-003], the two capitalisation differences and their firm caveat [SCR-020], the orthographic normalisations absorbed [SCR-033(a)], **and the finding that there is no second substantive recasting anywhere in the formulary** [SCR-033(a)] are all at §1.2. **NOT SUPPLIED and not needed here:** nothing. **The English is fixed by the profile and not by research** — Douay–Rheims Challoner for the scriptural elements and the registered Cummiskey 1861 for the orations — and §11.1 carries the rights posture |
| 5 | **`The Propers: Detailed Commentary`** | **YES for the seven scriptural elements; NOT for the exegetical reception of the three orations** | **Every appointed scriptural passage now has complete-context research and at least one direct witness checked at its work and locus** (§2.1–§2.7), with direct exegesis distinguished from illuminating reuse, real differences preserved (§6.4–§6.13), and the composed texts' verbal echo, doctrinal illumination and documented liturgical reception kept apart. **Six of the ten elements gained a witness this run**, and the Alleluia and the Gradual — the two thinnest — gained two and two. **NOT SUPPLIED:** any patristic or medieval commentary on the Collect, Secret or Postcommunion. Corpora and search terms are itemised at §2.8 and §4.1; **the languages searched were Latin and Greek and English**; the limit reached is that the genres swept do not take liturgical orations as their object; **and two named repairs remain unmade — Schuster vol. 3, registered complete and already inspected at p. 123, and the Usuarium Corpus Orationum concordance, registered with a proven route and never consulted** [COV-011, COV-002]. **The orations' history is supplied in full** (§6.1–§6.3, §7.4, §2.8's Gerbert material), **and the guide should carry the bounded negative on reception beside it.** Three bounds carry into this section: the Greek side is better and still bounded (§4.2); **no Greek witness may speak on `luxuria`, `modestia` or `castitas`** (§0.3(a)); and **no witness anywhere comments on the Communion antiphon as such** [PAT-135] |
| 6 | **`Source-Grounded Synthesis Across the Propers`** | **YES** | **This position is what §7's six claims exist for**, and the brief supplies each with its class mixture stated rather than averaged, its reception witnesses named individually, and its defeaters printed. **The unbounded source-grounded section may draw on classes 1–4 only**, and §7 marks the class of every limb. **Two things the brief supplies that this position specifically needs:** the **competing historical judgments** at §6, which are what keep the synthesis from manufacturing consensus — ten of them, of which one (§6.8) is a live disagreement with the prior production that must be printed as unresolved; and the **bounded negatives** at §4, which are what keep an unbounded section from overreaching. **NOT SUPPLIED, and named:** C6's genre counter-test was not run (§7.6), so **that claim may not be stated as distinctive**; and the missal-wide oration concordance behind P3's counter-test was not run either (§9.3) |
| 7 | **`The Propers: Notable and Quotable`** | **YES** | **Five source- and locus-identified non-obvious afterlives at §8**, spanning political, legal-institutional, legal-punning, humorous and humorous-idiomatic registers across **Communion, Gospel, Epistle and Gradual**, with five further qualifying candidates and their reasons for non-selection at §8.6 and the refusals at §5. **Two bounds are part of the supply and not exceptions to it:** **two entries are VERIFIED by page-image collation and three are not, and the three may not be called verified** (§8); and **no qualifying candidate exists for the Introit, the Alleluia, the Offertory or any of the three orations** — swept twice now, in two different corpora, with the counts at §4.9. **Two attributions in the prior gallery are corrected at §0.3(e) and must be corrected in the guide** |
| 8 | **`The Propers: Interpretive Possibilities`** | **YES** | **Six proposals at §9**, each joining at least two precisely named appointed elements, each selected from and grounded in the `precedent-search` lane's eleven conjunctions, each carrying that lane's classification unchanged, with anchors, mechanism, fruit, nearest located precedent or analogue, search boundary and controlling limit. **Within the profile's range of four to six.** **The prior audit's coverage gap is closed** (§9). **One reduction is mandatory and is stated at §9.2: P2's core move is now documented reception and must move to the commentary, the proposal being retained only in its reduced cross-element form.** **And §9.8 names two readings that do not clear the two-element floor, so nobody revives them** |
| 9 | **`Sacramental Appendix`** | **NOT REQUIRED — no evidence needed** | This is an ordinary Sunday of the temporal cycle. The formulary appoints no ritual text, no blessing and no sacramental rite, and no non-Eucharistic sacrament is celebrated with it [SCR-001]. The profile requires the imported summary only "when a ritual Mass is celebrated with or specifically for a non-Eucharistic sacrament". **The section is omitted, and its omission needs no evidence** |
| 10 | **`Appendix: Scope and Qualifications`** | **YES** | Edition and formulary identity from the `source-audit` stage; text-verification state from `verified.md`; source scope, corpora and languages at §3; search limits and material negatives at §4; competing judgments at §6; rights boundary at §11.1; evidence-state discipline at §11.2. **The global bounds that must reach this appendix rather than the body:** the Greek/Latin imbalance and what was and was not read (§4.2); the loc.gov AND-count calibration (§3.6); **the absence of any Hebrew psalter, Greek psalter, Vetus Latina or NA/UBS edition, and the precise form of the critical-edition statement** (§4.5); **the four still-unopened sacramentary books and the specific reason for each** (§4.6); **the Veronense negative, now replayable, with its four bounds** (§4.7); **the fact that every witness added this run stands at *inspected* and none at *verified*** (§11.2); **the fact that two gallery entries and no others are verified** (§8); and **the fact that no mechanical gate in this repository can check a rights claim against the prose** (§11.4) |
| 11 | **`References`** | **YES, with an exclusion rule and two corrections** | Every retained witness in §2 and §7–§9 carries author, work, exact locus, edition or stable link and source role sufficient to verify its claims. **Exclusion rule the author must apply:** the three witnesses this repository does not hold in any form — Papias, Eusebius *HE* Book III, Jerome *Comm. in Gal.* — **must not appear as used sources.** Where a page-2 row states a bounded negative naming them, the naming belongs in the row and not in `References`. **Correction 1:** the flat "no critical edition is registered here" should read "no critical edition **reaching an appointed passage** is registered here" [COV-009]. **Correction 2:** the References sentence asserting that "the New Advent transcription of it is registered restricted" **asserts a registration that does not exist at these loci** (§4.10) [COV-004]. **And Bellarmine should be cited by the edition actually registered** (O'Sullivan's abridged English, Duffy 1866) rather than by the Latin title — noting that all five published Claude siblings use the Latin title, **so this is a collection-wide inherited form and correcting it here is a local improvement, not a repair of a local error.** **Every witness added this run must be cited with its route and state**, per §3.2 |
| 12 | **`Generation Metadata`** | **NOT APPLICABLE — no research evidence required** | Terminal, mechanically imported from the leaf's `generation-metadata.tex` under the universal metadata standard |

**Summary of the statement.** **Twelve positions. Nine are supplied.** One
(position 5, Detailed Commentary) is supplied for its scriptural elements and
carries a named bounded negative for the orations' exegetical reception. One
(position 9, Sacramental Appendix) is not required and needs no evidence. One
(position 12) requires no research evidence. **One — page 2 — is partially
supplied, and its six remaining unsupplied items are named individually above
with the corpora, loci and limits behind each; one of the prior brief's seven,
the acrostic, is relieved this run and is now available as documented
reception.** **No position's evidence position is left unstated.**

### 10.1 Coverage statement updated by the fresh join, run `e5b24f405bde9691` (2026-08-31)

The fresh source-citation-coverage lane audited the leaf as re-authored and
returned eight findings. **They change the state of two positions and leave
the other ten as stated above.**

- **Position 11, `References` — SUPPLIED, WITH NAMED DEFECTS THE AUTHOR MUST
  REPAIR.** The subsection was not re-authored with the rest of the leaf: it
  omits every witness the re-authoring commit's commentary newly uses, and it
  still names Augustine's *Expositio ad Galatas* among four instruments "not
  retrieved" while the same commit's commentary uses that work extensively —
  the apparatus contradicting the body, which is the defect the profile's
  References rule exists to prevent [fresh:COV-012, whose evidence names the
  commit's 2-line References change against 717 changed commentary lines].
  The Enarrationes entry asserts a restricted New Advent registration that
  exists at none of the four appointed psalms — the registered artifacts are
  at psalms 17, 25, 51, 55, 65, 69, 77, 90 and 144 only — so the sentence
  must either name the registered loci it is true at or drop the registration
  claim [fresh:COV-014, which re-establishes against the current working tree
  the defect the first join carried as COV-004/Correction 2].
- **Position 12, `Generation Metadata` and the research apparatus — one
  further named staleness.** `research/source-bindings.toml` is stale against
  the re-authored leaf: its header declares Cassiodorus, Jerome's Comm. in
  Gal., Chrysostom's Expositio in Ps. CXVII, Theodoret on Pss. 83 and 94,
  Gregory on Ezekiel and Schuster vol. 3 "NOT REACHED", while the body uses
  each as a read source; its 24 bindings name no record for any of the new
  patristic layer. The file's schema-2 text-control and translation-control
  bindings remain valid [fresh:COV-013].
- **The evidence ceiling for the new patristic layer, now stated as a bound
  that governs every section carrying it.** Every witness the re-authoring
  added — Hilary's Commentarius in Matthaeum, Jerome's Comm. in Gal.,
  Augustine's Expositio ad Galatas, Chrysostom's Comm. in Gal., Cassiodorus
  at the four appointed psalms, Theodoret at Pss. 83, 94 and 117 — has no
  source-library record of any kind at the loci used, so none of these
  citations can acquire a fingerprint, a passage record or a rights
  disposition from the library as it stands, and the References cannot supply
  edition identity beyond what the prose states [fresh:COV-015]. **This is
  the bound the guide carries in place of a stronger claim; the gap is
  diagnostic and registering these witnesses is later-stage work, not this
  workflow's.**
- **The cheapest upgrades, recorded so nobody has to re-derive them.** The
  repository already holds, hashed and remote: PL 37 complete (Augustine's
  Enarrationes for Pss. 80–150, 481 pages, public domain, with a
  verified-segment precedent at Ps. 88 — reaching Pss. 83, 94 and 117 but not
  Ps. 33), the complete Theodoret PG 80 facsimile (1068 pages), and Schuster's
  Liber Sacramentorum vol. 3 (462 pages, public domain, with registered
  passages at pp. 123 and 132–134) [fresh:COV-016]. Using them requires
  re-retrieval, which no lane of this run was authorised to do.
- **Positions re-checked clean.** The page-2 NABRE bounded negative stands
  exactly as printed: the registered NABRE stratum holds no artifact for
  Matthew or for NABRE Pss. 34, 84, 95 and 118, the only locus reaching an
  appointed passage being the Galatians introduction [fresh:COV-017,
  re-running the enumeration]. The References exclusion list's holdings
  statements for Papias, Eusebius HE Book III, Irenaeus III.1.1 and Jerome's
  Comm. in Gal. all check out against the working tree, and the page-2
  bounded negatives for them are correctly bounded — **a positive
  verification, recorded because an audit that only reports defects cannot
  establish that the negatives it leaves alone are sound** [fresh:COV-019,
  which also confirms Irenaeus III.1.1 is reachable in searchable bytes
  without a passage record, exactly as the leaf states].
- **Rights posture, unchanged in substance and restated with the fresh
  enumeration.** All 70 registered New Advent artifacts have ceased to
  reproduce (deltas of −1 to −3 bytes plus one 404), so their digests stand
  only as historical attestations and registration claims about that stratum
  must be locus-specific [fresh:COV-018, resting on the repository's own
  2026-08-28 drift review]; the Adriaen CCSL 98 Cassiodorus and the Centro
  Studi Anthony apparatus remain rights-restricted (summarise-only); the
  Haydock 2014 Loreto printing's rights remain recorded unresolved.

**The twelve positions of the reader order remain stated as at §10 above;
this subsection adds defects and bounds to positions 2, 11 and 12 and to the
patristic-layer evidence state that several positions share.**

---

## 11. Operational qualifications displaced from the PDF

### 11.1 Rights posture, per source class

| Class | Rule |
|---|---|
| **Documenta Catholica Omnia MGR Greek PDFs (Theodoret, Chrysostom)** | **The digitisation is the Thesaurus Linguae Graecae's and the PDF carries TLG's copyright notice**, authorised for posting. **The ancient Greek is public domain by age and is what may be quoted; the digitisation may not be reproduced wholesale.** No bytes were written into the repository [PAT-300, PAT-310, PAT-405] |
| **Corpus Corporum / Latin Wikisource transcriptions of Migne (Jerome, Hilary, Cassiodorus)** | Transcriptions of public-domain Migne text. Quotable. **Note the Corpus Corporum Latin is normalised to classical orthography**, which is why these witnesses appear with `j` and `ae` spellings a PL page would print differently [PAT-405] |
| **augustinus.it (Augustine, *Expositio ad Galatas*)** | Machine transcription of a Migne text; quotable, **inspected and not verified** [PAT-100] |
| **Cassiodorus, CCSL 98 (Adriaen 1958) scan** | `storage='restricted'`, `rights_status='restricted'`. **Adriaen's edition, lineation and apparatus remain in copyright: summarise only, and it may never supply published Latin wording** [COV-003] |
| **Anthony of Padua, Centro Studi 2021 PDF** | `storage='restricted'` because of the modern apparatus. **Anthony's thirteenth-century Latin is public domain by age and may be quoted; the modern apparatus must be paraphrased only.** No bytes in the repository. **See §4.11: the guide quotes this Latin at length, the artifact's own passage records instruct that the delivery be paraphrased unless a lawful checked transcription is supplied, no such transcription is registered, and because the source is unbound no gate can see any of it** |
| **Usuarium Corpus Orationum** | `rights_status='restricted'`. **Its bytes may not be reproduced here; any published wording must come from elsewhere. It is a finding aid, not a replacement for the printed apparatus** [COV-002] |
| **New Advent per-page HTML** | Restricted transcription over public-domain underlying text. **Summarise; never reproduce.** And see §4.10: **all 70 registered New Advent artifacts have ceased to reproduce, and the loci this guide quotes have no artifact record at all** |
| Catholic Encyclopedia, **volume facsimile** (vols. 4, 8) | Public-domain. **May be quoted** |
| Catholic Encyclopedia, unheld volumes | Citable at an exact article locus by title, URL, volume and year. **No content was retrieved in either run, so nothing may be asserted from them** |
| NABRE / USCCB | All registered artifacts `rights_status='restricted'`. **Summarise; never reproduce.** Only the Galatians introduction bears on this proper |
| Haydock, 2014 Loreto printing | `rights_status='unresolved'` — a recorded **non-determination**, not a restriction. **Summarise-only is the correct conservative reading** |
| Honorius, PL 172 Migne facsimile | `storage='restricted'`; the prior run fetched to scratchpad, read, retained nothing. **Not reopened this run** |
| Migne **PL 37** | **Registered complete, `rights_status='public-domain'`, 481 pages, hashed and partly rendered.** Quotable, and **it is the cheapest available upgrade to three of the four Augustine psalm loci** (§4.10) |
| Wilson 1894 and 1915, Feltoe 1896, Férotin 1912, Bannister 1917, Lowe 1917 | Public-domain optical layers of public-domain editions. Quotable; **all `indexable=false` with no bytes in the tree** |
| Gerbert IA digitisations; Pamelius IA item | **NOT registered artifacts of this repository.** Nothing was written into the repository. Public-domain by age |
| Tracked missal texts (Pustet 1862, Venice 1570, Vatican 1604), Ambrosian and Mozarabic texts | Tracked, public-domain, **`indexable=true`** — **which is why §4.12's blanket about replayable receipts is wrong for this class** |
| Tracked Bible text (Clementine, Douay, Douay-American, CPDV, Brenton, KJV, WEB) and the Robinson-Pierpont CSVs | Tracked, public-domain. Quotable |
| US court opinions and official reporters; UK official parliamentary report; LoC-digitised newspapers; Project Gutenberg | Public-domain or official. Quotable; **keep extracts brief** |
| ICEL, Knox, Jerusalem/NJB, RSV/NRSV, NABRE, Grail | **Never reproduced at any length that would substitute for the book** |

### 11.2 Evidence-state discipline

**No patristic or medieval witness in this brief is *verified* in the
source-library sense**, because verification under this profile means collating
the locus against the controlling critical or Migne edition, **and Migne was
opened for none of them, in either run** [PAT-405]. The tiering used is:
**acquired** (exact bytes obtained and hashed), **searched** (query run over the
retained artifact), **inspected** (the identified passage read with surrounding
context), and, where a second witness independently agrees in the original
language, **corroborated** — which is short of collation.

**This run added a great deal of material and did not raise the ceiling.**
Sixteen new witness-works were retrieved and every one stands at *inspected*
[PAT-405]. **No later worker may mistake the volume for a rise in state.**

**Two entries in this brief DO stand at *verified*, and they are not patristic.**
The two page-image-collated newspaper items at §8.4 and §8.5, **and only for the
crop regions their findings name** [CUL-008, CUL-011, CUL-015]. **Nowhere else
in this brief may the word be used.**

**Three witnesses are better attested than the rest and the guide may lean on
them accordingly:** **Anthony of Padua** and **Guéranger**, whose downloaded
digests reproduced already-registered artifact records bit for bit; and
**Augustine on `primum`**, corroborated in Latin from a second, independent,
separately hashed thirteenth-century witness.

**Every English quotation from a patristic or medieval witness must name the
translation it is quoting, on the page and not only in this brief.** With the
exception of the Latin read from Aquinas, Anthony, the *Catena*, the
`augustinus.it` *Enarrationes*, and **the Latin and Greek read directly this
run**, **every** patristic string this brief supplies in English is somebody's
translation, reached by one of the routes at §3.2. **The translations to name,
and no more precisely than that: NPNF first series** for Augustine's
*Enarrationes*, *De sermone Domini in monte* and *De opere monachorum*, and for
Chrysostom's *Commentary on Galatians* and *Homilies on Matthew*; **NPNF second
series vol. 7** for Cyril of Jerusalem; **NPNF second series vol. 10** for
Ambrose; and for Guéranger the **Duffy 1900 English edition**. **No lane
established who translated the Guéranger volume, so name the edition and never a
translator.**

**A new instance of exactly why that rule exists** [PAT-311]. Chrysostom's
sentence "by the flesh, he does not mean the body", on which cross-proper claim
C2 partly rests, **is NPNF's paraphrase**: the Greek contrasts σάρξ with
λογισμός, not with σῶμα. **The English is not wrong and the Greek is sharper,
and a page that presents the English as the Father's own words has removed the
reader's ability to notice the difference.**

**Latin quoted in Latin needs no translation attribution but needs its route and
state** (§3.2) **like everything else**, and where this brief gives an English
rendering beside a Latin collation the English is still the translator's.

### 11.3 Retrieval traps — nine instances of one species

All are queries that **resolve successfully and wrongly**, returning well-formed
material about the wrong text. **Four are inherited and five are new.**

1. **The doubled psalm-numbering offset on New Advent** (prior run). Page title in the modern number, inline verse tags one verse behind the Clementine: a locus must be shifted **twice**. Absent at Pss. 117 and 94 for reasons peculiar to those psalms — **an agreement that is a coincidence, not a general property.**
2. **The running head that names the section the page reaches** (prior run, and independently met again this run) [LIT-015]. Two loci in Wilson 1894 were misread this way. **Confirmed at first hand this run:** printed p. 207's running head reads "II. lxix." while the page opens inside sect. lxviii, and p. 206's head names two sections at once. **Any locus in either Wilson edition taken from a running head is suspect until checked against the section heading itself.**
3. **The shared incipit** (prior run). `Protector noster aspice, Deus` opens this Mass's Introit, the Fifth Sunday's Gradual and a composed collect. **A search hit on an incipit proves nothing on its own.** Related: the augustinus.it file index is a running document number, not the psalm number.
4. **OCR hyphenation and phrase-search degradation** (prior run, and now with five worked demonstrations). `grep -i immittet` misses `Immit-`/`tet`; a grep of *Spark* issues for "political kingdom" returned zero while the phrase was present as `poli-`/`tical`; **`circuitu timentium` returns 0 in all eight missal artifacts from books that print it, defeated by diacritic-substitution OCR (`cirdiitu`, `tim6ntium`)**; `venite exsultemus domino` returns 0 from a book printing `uenite exultemus d6mino`; **and a literal multi-word sweep over the collated `verified.md` records is defeated by line wrapping, which produced a false negative on `sperat in eo` until newlines were collapsed** [PRE-002, PRE-017, THE-044]. **A search that finds nothing has not established that nothing is there; it has established what the search did.**
5. **NEW — the interleaved two-column page** [LIT-015]. Gerbert's p. 173 carries two columns and two formularies, and the OCR interleaves them **so that a prayer belonging to the Sunday appears, in the text stream, in the middle of the Marian Mass.** The lane misread Gerbert's Postcommunion that way on first pass **and only Wilson's independent Appendix tabulation caught it.** The same device produces the Venice 1570 running-head noise at [PRE-008].
6. **NEW — the commentator whose verse numbering is offset from the missal's** [PAT-205]. **Cassiodorus's Ps. 33 verse tags run one behind**, so his *Vers.* 7 and 8 are the missal's Offertory vv. 8 and 9, and the same offset appears at Ps. 83. **A lane resolving loci from his tags will mis-cite the Offertory by one verse.**
7. **NEW — the partial source that looks complete** [PAT-404]. **Latin Wikisource's *Expositio in Psalterium* carries only Psalms 1 to 30**, so **all four appointed psalms are absent from it and a lane that stopped there would have recorded a false negative for Cassiodorus.** **The failure mode is specific and quiet: the index page looks complete, the subpage naming is regular, and the missing psalms return ordinary 404s indistinguishable from a wrong URL.**
8. **NEW — the misattribution inside a Doctor's own work** [PAT-133]. **Aquinas's *Super Matthaeum* ascribes the lilies-as-angels reading to Jerome; the reading is Hilary's**, and the Catena attributes it correctly.
9. **NEW — the TLS failure that is not an availability failure** [PAT-403]. **documentacatholicaomnia.eu fails certificate verification and serves the identical bytes over plain HTTP with a 200.** A negative the prior brief carried as bounded and correctable **turned out to be correctable by changing the URL scheme**, and the correction yielded a Latin commentator on all four appointed psalms. **This is the run's clearest demonstration that a retrieval negative is a statement about a retrieval.**

**A tenth, carried from the prior run and still standing:** `Chrysostomus super
Matth.` in the Catena **is not Chrysostom** (§2.5).

**And two route facts recorded as method, not as claims about any text**
[PAT-403]: **Documenta Catholica Omnia's MLT (Latin) PDFs are JBIG2 image scans
with NO text layer** — Jerome's and Hilary's Matthew commentaries both yield 81
bytes from `pdftotext` — **and should not be downloaded again**; **its MGR
(Greek) PDFs are TLG transcriptions WITH a real text layer and are the working
route to Greek patristic text.** Corpus Corporum serves TEI XML for any
Patrologia Latina work through `php_modules/download.php?type=file-xml&idno=N`,
where N is found by walking `php_modules/navigate.php?load=/38`.

### 11.4 What no gate can check

Recorded because it changes what a green build means [COV-007]. **The only
preflight check touching quotation is a self-consistency check between the
leaf's own References and its own quotation environments; it never reads
`src/sources/` or any storage or rights field**, and
`check_restricted_not_reproduced` **iterates only over `bound_sources(leaf)`,
its own docstring conceding that "the rights of an artifact nobody recorded
cannot be read from a record that does not exist."** `tpt source-library
validate` validates the library against itself. **There is no mechanical rights
gate over reproduction from a restricted artifact anywhere in this repository,
and the one restricted artifact this guide quotes at length is unbound and
therefore invisible to the check that would examine it** (§4.11). **A gate
passing is not evidence that the tree is rights-clean.**

**And a second class of invisibility, new this run** [COV-004]: the New Advent
delivery drift "is structurally invisible. `source-library validate` passes
clean and never re-fetches remote artifacts."

### 11.5 Manifest observations for whoever owns `proper-components.toml`

Recorded as observations, not as edits; **this stage does not amend the
manifest.**

- `hope-formula-past-the-cut` `[introit, gradual, offertory]` — **membership upheld** on the criterion at §0.3(g), now bounded across the whole Vulgate. **The manifest's key is accurate; a lexical reading of it is not.**
- `fruit-count-unsettled` `[epistle, communion, gospel]` — **membership still not supported.** The fruit list stands in the Epistle alone and nothing joins the Communion or the Gospel to a question about the count. **What is genuinely unsettled lies in the reception and is now four-fold** (§2.2, §6.5).
- `goods-ordered-not-refused` `[introit, gradual, gospel, communion, collect]` — **the mechanism as previously stated is inaccurate and is corrected at §9.1**: the Gospel carries both registers, hinged on `Ideo`. The nearest lexically grounded set remains `[introit, gradual, epistle, gospel]`; the Communion and Collect are thematic members.
- `what-man-cannot-add` and `propitiation-and-salvation-saturated` were independently reproduced element for element by the prior run's theological lane. **P2's element set is unchanged; what changes is that half its content is now documented reception** (§9.2).
- **No manifest key exists for P6.** The `concupiscere` conjunction is new this run and **the manifest declares no relation for it.** Whoever owns the manifest will need one if P6 is published; **naming it is not this stage's to do.**
- The relation keys occur in exactly two files repository-wide — the manifest and this file.
- Structural precedent worth keeping: the single-source stub is what the target already uses and is what keeps the two editions from drifting; **leaf 49 has demonstrably drifted** against the profile's fixed order. **Two of the five siblings are pre-correction work — 48 on page-2 evidencing and 49 on section order — so "the siblings do X" is only a safe argument when 51, 52 and 53 do X.**

### 11.6 Observations for whoever owns `research/source-bindings.toml`

Recorded as observations and not as edits, in the same posture as §11.5. **This
stage writes `research/scope.md` and nothing else**; the binding file belongs to
the stage that owns the canonical leaf's records. **It is stated here because
this brief is the authority on what was actually reached, and because a later
run deciding what still needs retrieving will read the binding file.**

**Four statements in that file are false or misleading on this brief's own
record.**

| Statement in the bindings file | What this brief records |
|---|---|
| "the patristic and medieval layer is bound here almost not at all, because **none of its witnesses has a passage record in this library at the loci used**" | **False for Anthony of Padua**, who has **three passage records at states `[cataloged, acquired, inspected, verified]`, verified 2026-08-21, one of them explicitly reaching Gal. 5:22–23** [COV-006]. Wilson and Guéranger have passages at other loci in the artifacts the guide read; Honorius and Aquinas *Super Galatas* have artifacts registered complete over the loci used |
| "**no negative-search binding appears** … so no replayable search receipt exists for any of them" | **Right for the sacramentary OCR layers, the Benziger layer, the Migne and Centro Studi facsimiles and the Corpus Orationum entry; wrong as a blanket.** The Pustet 1862, Venice 1570 and Vatican 1604 texts are tracked, public-domain and `indexable=true`, and the Douay–Rheims and Clementine artifacts are overwhelmingly indexable [COV-008]. **The correct form distinguishes the two halves** |
| "Cassiodorus on Psalms 33, 83, 94 and 117: **registered with no payload; the probe of the host that carries him failed on certificate verification**" | **Wrong twice and now moot on the substance.** Three editions are registered, one a complete hashed 721-page CCSL 98 scan; the certificate failure belongs to the **Honorius** host; and **the complete work was retrieved in Latin this run** [COV-003, PAT-200] |
| "**No Veronense edition is registered at all, Feltoe included**" | **False.** Work, edition and two hashed IA OCR artifacts, all corpus members, added 2026-08-01 [LIT-001, COV-001] |
| "Schuster, *Liber Sacramentorum* vol. 3: registered here and **deliberately not retrieved**" | **Accurate as a scope decision and misleading as a statement about holdings.** The volume is registered complete, hashed, 462 pages, public-domain, **printed p. 123 already visually inspected in the exact hashed facsimile**, with registered passages at pp. 123 and 132–134 [COV-011] |

**The same holds for the header's list of witnesses "every one reached at an
exact locus and read directly".** **Papias, Eusebius *HE* III, and Jerome
*Comm. in Gal.* are held in no form** [COV-010] — though Jerome on Galatians was
**retrieved directly this run and remains unregistered** [PAT-150]. **Theodoret
on Pss. 83 and 94 was NOT retrieved by the prior run and WAS read in Greek by
this one** [PAT-300], and still has no passage record. **Chrysostom's *Expositio
in Ps. CXVII* is still not retrieved.** **Ambrosiaster, Cassian and Marius
Victorinus on Galatians were not swept.**

**The defect is that one sentence collapses a mixed list into a uniform claim**,
and a research record asserting direct reading of witnesses the same publication
declares unretrieved is worse than one that says nothing, **because it is the
file consulted to decide what still needs retrieving.** Nothing reader-facing
depends on the correction. **The honest form is the one this brief uses
throughout: name what was reached, name what was not, and say which is which.**

**Two additions the binding owner should make, both of which this run makes
possible:** bind Anthony, **so that the restricted-not-reproduced check can
finally see the one restricted artifact the guide quotes at length** (§4.11);
and register the Feltoe and Wilson OCR layers' findings **so the Veronense
negative never has to be carried unreplayable again** (§4.6, §4.7).

---

## 12. Prior-production carry-forward

**Required by this stage's own fragment, and it is not optional.** Re-seeding
produces a run with an empty history — the run id derives from the workflow
version, the commit and the arguments — and one real re-seed dropped fourteen
standing evaluation findings on the floor. **This stage is the first stage of
this production that writes anything durable and the only one positioned to
carry them.** What is not permitted is not looking, or looking and not saying.

**Prior runs against this target were found by**
`grep -l '"proper": "liturgy/roman-rite/1962/propers/temporal/54-fourteenth-after-pentecost"' build/tpt-runs/*/state.json`,
**which returns five runs: this one and four others. Each of the four was read
at its `state.json`, and for every `content-evaluation` and
`research-synthesis` entry in `result_hashes` the named result file was read.
The blocking findings of each stage's LAST result were taken, together with any
`escalations`. No prior run recorded an escalation of any kind.**

### 12.1 The two runs that produced nothing downstream

- **`bd3b8b31e16d9214`** — workflow v8, terminal disposition **BLOCKED**. Its only result is `seed-0000.json`, itself BLOCKED. **No `content-evaluation` and no `research-synthesis` entry exists. `escalations` is null. Nothing to carry.**
- **`d17e882ad8f6e774`** — workflow v8, `current_stage` `seed`, `result_hashes` empty. **No results of any kind. `escalations` is null. Nothing to carry.**

### 12.2 `b68cca80edb75854` — workflow v10, terminal BLOCKED — one standing finding, and it is RESOLVED

**This is the most recent real production and the one whose leaf this run is
laid against.** Its **last `research-synthesis`** is `research-synthesis-0001.json`,
disposition **PASS** with `findings: []` — **nothing standing from that stage.**
Its **last `content-evaluation`** is `content-evaluation-0002.json`, disposition
CHANGES_REQUIRED, 21 findings of which **exactly one is `blocking`**. Twenty
advisory findings were recorded and do not block. **`escalations` is null.**

| Finding | Run | What it required | Status |
|---|---|---|---|
| **CON-EVI-008**, `severity: blocking`, `repair_target: authoring`, location `sections/30-commentary.tex`, the two paragraphs between witnessnotes in the Gospel element | `b68cca80edb75854`, content-evaluation iteration 2 | Four English patristic quotations — Augustine's "a rational being such as man has a higher rank in the nature of things than irrational ones" and "that even in looking after such things we should think of the kingdom of God…", and Chrysostom's "you, to whom He gave a soul, for whom He fashioned a body…" and "He said not, we must not sow, but we must not take thought…" — stand **outside** any `witnessnote` environment and so with no named translation reaching them, against `research/scope.md` §11.2. **Required:** extend the two Gospel state lines so their scope reaches the discussion between the notes, **naming the edition (NPNF first series) and NOT a translator**, while preserving every existing bound — `Patrologia Latina` 34 not collated, `Patrologia Graeca` 57 not collated, nothing presented as his Greek, and the recorded defect that the retrieved page for Homily 22 prints its lemma header as "Matthew 5:28-29" — and without disturbing the three "Same route and state" notes | **RESOLVED at commit `f4534e4cd`, and verified against the finding rather than taken on trust.** `sections/30-commentary.tex` now reads, in the Augustine *De sermone Domini* note, "every English string quoted from him below, **in this note and in the comparative discussion that follows it**, is NPNF's rendering and not Augustine's Latin", and in the Chrysostom *Hom. in Matt.* note "which is the rendering reproduced by every English string quoted from him below, **in this note and in the comparative discussion that follows it**, and not his Greek". **The PL 34 and PG 57 bounds and the Homily 22 lemma-header defect all survive beside them, and no translator is named.** The commit message records that both PDFs rebuild at 46 and 28 pages with identical page counts, Themes span and warning set against a reverted baseline, so the repair moved nothing on the page but the two state lines |

**One consequence for this run, and it is why the finding is worth carrying even
though it is closed.** The rule CON-EVI-008 enforces — **every English patristic
quotation names its translation on the page** — is restated at §11.2 **and now
has a fresh instance behind it**: Chrysostom's "by the flesh, he does not mean
the body" is NPNF's paraphrase of a Greek sentence that says something sharper
[PAT-311]. **The rule is not a formality and the author must apply it to every
witness added this run as well.**

### 12.3 `7521f033d37e8997` — workflow v8, abandoned mid-`research` — fourteen standing findings

**This is the run the profile's step 11 warns about.** Its disposition is null
and its `current_stage` is `research`; it ran `content-evaluation` twice,
`research-synthesis` three times and `author-proper` twice, and then stopped.
**Its last `research-synthesis` is `research-synthesis-0002.json`, PASS with
`findings: []` — nothing standing from that stage. `escalations` is null.**

Its **last `content-evaluation`** is `content-evaluation-0001.json`,
CHANGES_REQUIRED, **33 findings of which fourteen are `blocking`. These fourteen
reached no owner. They are recorded here individually, with what each required
and its status at this run's commit.**

**How status was determined.** Each finding was checked against **the leaf as it
now stands at `f4534e4cd`**, by bounded string checks for the exact wording each
finding quotes, **and against this run's seven-lane join.** **The leaf was
completely re-authored by the `b68cca80edb75854` production, twice, so most of
these findings are against prose that no longer exists.** That is recorded as
*no longer applies* with the reason, which is one of the three dispositions the
fragment admits.

| # | Finding | Target | What it required | Status at `f4534e4cd` |
|---|---|---|---|---|
| 1 | **CON-EVI-005** | authoring | Drop or bound the psalter-wide ranking "among the most quoted verses of the psalter in the New Testament" | **NO LONGER APPLIES.** The string is absent from `sections/`. Note that this run's join independently bounds the underlying fact: `caput anguli` returns exactly five New Testament verses plus Ps. 117:22 itself [SCR-018] |
| 2 | **CON-EVI-007** | authoring | Restate "Mt. 6:33 is not in dispute in any witness tracked here" at the evidence state the record supports, the leaf's own record documenting patristic lemma variation at that verse | **NO LONGER APPLIES.** Neither string is in `sections/`. **And this run makes the underlying point sharper still:** neither the Matthaean nor the Lucan form fronts `primum` [SCR-003], and Chrysostom's Greek confirms the missal's `Qui autem sunt Christi` against Augustine's differing lemma [PAT-315] |
| 3 | **CON-EVI-008** (of that run) | authoring | Report four books at two Sundays later and Pamelius at one, and stop counting Pamelius in both bodies | **NO LONGER APPLIES as written**: `sections/35-source-grounded-synthesis.tex` l. 236 and `sections/30-commentary.tex` l. 255 both now read "two Sundays later and Pamelius uniformly one, with no exception". **BUT the underlying fact is materially revised by this run and the author must restate it anyway**: the run is **sixteen** sections and not eleven, with R/S/Gerbert/Menard at N+2 for I–XI and N+4 for XII–XVI while Pamelius holds N+1 unbroken [LIT-009]; and the Gregorian Hadrianum carries **all three** orations [LIT-023]. See §6.1 |
| 4 | **CON-EVI-009** | authoring | Bring inside the declared corpus ceiling or remove three universal claims: "Paul's baptismal idiom", "the language of every Roman Secret", and "the Roman repertory's natural Communion text" | **NO LONGER APPLIES.** All three strings are absent. **The ceiling itself is restated in this brief at §7.1 and §9.3 and still governs: every uniqueness claim must name the fifteen collated formularies and never "the Missal"** |
| 5 | **CON-EVI-010** | authoring | Give `sections/20-themes.tex` a witness-state preamble or mark each witness's state at its point of use, and restore two caveats — Theodoret's Greek forms as reconstructions, Cassiodorus at the Introit as probable dependence on Augustine | **NO LONGER APPLIES at its point of use.** `20-themes.tex` now carries state marking ("NPNF's English, first series, uncollated against…", "uncollated against `Patrologia Latina` 34"), and **neither Theodoret nor Cassiodorus appears in that file at all.** **Both caveats are nevertheless live for this run's material and are carried: Theodoret is now read IN GREEK and no longer needs the reconstruction caveat** [PAT-300], **while the Cassiodorus dependence caveat is renewed and strengthened at §2.1** [PAT-207] |
| 6 | **CON-EVI-016** | authoring | Carry the 1570-derived wording changes as leads read off an uncorrected optical layer, not as collated 1570 readings; the sentence "The wording settled once … and then did not move again" must not assert an uncollated transmission history | **NO LONGER APPLIES.** The string is absent. **The discipline it enforces is renewed by this run in a harder form:** §3.5 records three worked demonstrations that a positive or negative reading off these layers is evidence about the layer, and §5 carries `maiestatis`/`potestatis`, `Deus`/`Domine` and `perpetuae`/`perfectae` each at its own state |
| 7 | **CON-EVI-017** | authoring | Restore the retained wording, or move the substituted word outside the quotation span: `ut innotescere mundo Dominum Salvatorem` was printed where the record reads `deprecatur innotescere mundo Dominum Salvatorem` | **NO LONGER APPLIES.** The string is absent |
| 8 | **CON-REC-003** | authoring | State the Alleluia's New Testament negative at the strength its method supports — verbal quotation, not reception — and carry the brief's bound that a literal Latin sweep can miss a quotation rendered in different words | **NO LONGER APPLIES.** The string "entire New Testament reception" is absent. **The discipline is renewed at §2.4 and §4.9: no lane's negative may be presented as stronger than its bound** |
| 9 | **CON-CIT-005** | authoring | Remove Mt. 21:42 from the Douay entry's cited-for-context list, and narrow the Brenton entry, which claimed versification use the body did not make | **PART ONE NO LONGER APPLIES:** Mt. 21:42 is absent from `sections/99-references.tex`. **PART TWO IS ANSWERED BY THIS RUN'S JOIN:** `scripture-context` classes Brenton as **direct evidence for versification and a lead only for LXX wording** [SCR-021, SCR-024], which is exactly what the current entry says |
| 10 | **CON-CIT-006** | authoring | Drop the quotation marks from three Guéranger appellations, or quote him as the brief has him; in no case leave "the Sunday of the two masters" inside quotation marks, that string not being in the source | **NO LONGER APPLIES.** The string is absent from `sections/` |
| 11 | **CON-CIT-011** | **research** | Establish on the page image which Gelasian section carries the `Purificent semper` recension reading `nos, Domine` with Andrew's intercession, and correct the brief and then the leaf so that section number, printed page and Vigil-or-Natale description agree | **ANSWERED BY THIS RUN'S JOIN.** `liturgical-history` read Book II sects. LXVIII and LXIX in both registered Wilson OCR layers and confirms: **sect. LXVIII is "In Vigilia sancti Andreae", printed pp. 206–207, and it carries the Postcommunion**; sect. LXIX is "Item in Natali eiusdem" and begins below it; **and the internal evidence settles it without the section number at all**, the Preface's `dicato ieiunio` and the Collect's `cuius natalitia PRAEVENIMUS` being vigil language [LIT-015]. **The running-head hazard behind the original error is confirmed at first hand** — p. 207's head reads "II. lxix." while the page opens inside lxviii — **and is carried at §11.3 item 2.** The leaf already prints **LXVIII** with an explicit correction note. **This finding is closed** |
| 12 | **CON-CIT-012** | authoring | Drop the count "seven places at vv. 6, 22 and 26" or state a count matching an enumeration the guide can show | **NO LONGER APPLIES.** The string is absent. **This run supplies a checkable bound for one leg:** `caput anguli` returns exactly five New Testament verses plus the psalm [SCR-018], and Heb. 13:6 quotes v. 6 verbatim [SCR-025] |
| 13 | **CON-CIT-013** | authoring | Name the translations for the English of Irenaeus, Eusebius and Papias on page 2 — McGiffert and Roberts-Rambaut — or drop the quotation marks and report all three as sense only | **NO LONGER APPLIES, because the quotations were withdrawn.** `sections/10-date-location.tex` now carries all three as **bounded holdings negatives** instead. **And their factual base is independently confirmed by this run:** Papias has no record of any kind, Eusebius is held only at Books VI–X in Greek and Book VI in English, and Irenaeus III.1.1 is reachable in searchable bytes with **no passage record** [COV-010] |
| 14 | **CON-PRO-001** | authoring | Make the page-2 measurement declarations true and mutually consistent: three departures were made, one was declared, `format.tex` denied its own column change, and both declarations misstated the magnitude as six per cent and omitted Proper as a donor column | **NO LONGER APPLIES.** `format.tex` now declares **THREE** departures explicitly — D1 the summary-tier column widths (profile 0.14/0.18/0.35/0.16, here 0.13/0.21/0.34/0.15), D2 the spanning-row width 0.98, D3 the spanning-row font size — states the net movement as **0.03\linewidth into Citation, donated 0.01 each by Proper, Location and Date**, and **names Proper as a donor**; `sections/90-scope.tex` carries no departure-count declaration to contradict it |

### 12.4 What the carry-forward amounts to

**Fifteen blocking findings stood across two prior productions of this target.
None is lost and none is left unstated.**

- **One is resolved** and verified at this run's own commit: `b68cca80edb75854`'s **CON-EVI-008** (§12.2).
- **Two are answered by this run's seven-lane join**, with the lane finding named: **CON-CIT-011** by [LIT-015], and the Brenton half of **CON-CIT-005** by [SCR-021].
- **Twelve no longer apply**, because the prose they were raised against was replaced when the `b68cca80edb75854` production re-authored the leaf. **Each is recorded above with the string checked and the reason.**
- **None is unresolved.** Had one been, that would have been a legitimate `PASS` and a bound the guide must carry; none is.
- **No prior run recorded an escalation.**

**Three of the twelve carry a live consequence even though the finding itself is
closed, and the author must act on all three:** **#3**, because the Gelasian
distribution the leaf now states correctly is **itself superseded** by [LIT-009]
and [LIT-023] and must be restated again (§6.1); **#5**, because the Cassiodorus
dependence caveat is renewed and strengthened by [PAT-207] (§2.1); and
**#12.2's CON-EVI-008**, because the translation-naming rule it enforces now
applies to sixteen newly retrieved witnesses (§11.2).

### 12.5 Updated at run `e5b24f405bde9691` (2026-08-31): the v11 predecessor run, and the fresh join's re-checks

**A third prior run now exists and is accounted for.** Run
`6b83fad5ae2ed53e` — `proper v11` at commit `f4534e4cd`, this target, this
provider — is the run whose research-synthesis wrote the first 3,526 lines of
this file; at this stage's iteration it is a prior production. Its **last
`research-synthesis` result is a `PASS` carrying no blocking finding** (its
artifact is the file this brief amends), and its **last `content-evaluation`
result is a `BLOCKED` with an empty `findings` array**: all five evaluation
lanes (`evidence-discipline`, `reception-sweep`, `synthesis-argument`,
`citation-integrity`, `profile-conformance`) returned BLOCKED with no
findings, and no escalation was recorded at the run level or in any result.
**It therefore contributes no standing finding** — there is nothing in it to
answer, resolve, or declare inapplicable — and its terminal state is recorded
here so that a later reader does not mistake an empty blocked evaluation for
a silent one.

**The fifteen findings above were string-checked by the first v11 integration
against the leaf as it then stood; the fresh join re-checked the load-bearing
ones against the leaf as re-authored at `7c2aaafce`, and the checks held in
both directions:**

- **fresh:COV-019 re-verifies finding #13's factual base positively**: Papias
  has no record of any kind, Eusebius is held only at Books VI–X in Greek and
  Book VI in English, and Irenaeus III.1.1 is reachable in searchable bytes
  with no passage record — exactly what #13's bounded negatives state.
- **fresh:COV-014 re-establishes, against the current working tree, the
  New Advent Enarrationes registration defect** behind the first join's
  COV-004/Correction 2: the re-authored References still asserts a restricted
  New Advent registration of the Enarrationes that exists at none of the four
  appointed psalms. **This is a live defect of the same species as finding
  #9's second half, newly located in the re-authored text, and it is recorded
  with its repair at §10.1.**
- **fresh:COV-012 and fresh:COV-013 add two new same-species defects** — the
  References subsection contradicting the re-authored body, and the stale
  source-bindings header — also recorded with their repairs at §10.1.

**No standing finding of either prior production is reopened by the fresh
join, and none is left unresolved.** The count for this target now stands at
fifteen blocking findings across three prior runs, all accounted for above.

---

## 13. Lane finding concordance

Where each lane's findings are used in this brief. **A finding not listed at a
section was read and judged not to bear on a published claim there; none was
discarded as wrong.**

| Lane | Findings | Count | Principally at |
|---|---|---|---|
| `scripture-context` | SCR-001 – SCR-034 | 34 | §1 (all), §2.1–§2.7, §4.5, §4.13, §5, §7.1, §7.2, §7.5, §9.4, §9.6, §0.3(a), §0.3(g) |
| `patristic-reception` | PAT-100 – PAT-108, PAT-110 – PAT-113, PAT-120 – PAT-126, PAT-130 – PAT-136, PAT-140, PAT-141, PAT-150 – PAT-161, PAT-200 – PAT-213, PAT-300 – PAT-306, PAT-310 – PAT-315, PAT-400 – PAT-405 | 74 | §0.3(a)(c)(f), §2 (all), §3.2, §4.1–§4.3, §5, §6.4–§6.7, §6.10–§6.13, §7.1–§7.3, §7.5, §9.2, §9.5, §10 rows 1 and 5, §11.1–§11.3 |
| `liturgical-history` | LIT-001 – LIT-027 | 27 | §0.2, §0.3(b)(d), §2.8, §3.3, §4.6–§4.8, §5, §6.1–§6.3, §6.8, §7.4, §7.5, §11.3, §11.6 |
| `theological-synthesis` | THE-001, THE-008, THE-009, THE-011, THE-033 – THE-051 | 23 | §1.4, §4.13, §4.14, §7.1–§7.6, §9.1–§9.3, §9.6–§9.8, §11.5 |
| `source-citation-coverage` | COV-001 – COV-011 | 11 | §0.3(b)(f), §2.8, §3.4, §4.4, §4.5, §4.10–§4.12, §10 row 2, §11.1, §11.4, §11.6 |
| `cultural-afterlife` | CUL-001 – CUL-003, CUL-008, CUL-011, CUL-014 – CUL-024 | 16 | §0.3(e), §3.6, §4.9, §5, §8 (all) |
| `precedent-search` | PRE-001 – PRE-018 | 18 | §0.3(d), §2.6, §3.5, §5, §6.9, §7.5, §9 (all) |

**Total: 203, and every one is accounted for.**

**Fresh join, run `e5b24f405bde9691` (2026-08-31) — 69 findings, every one
accounted for:**

| Lane | Findings | Count | Principally at |
|---|---|---|---|
| `scripture-context` | fresh:SCR-001 – fresh:SCR-025 | 25 | §0.4(f), §1.1–§1.4 (re-confirmed), §2 (re-confirmed), §7.1 (fresh:SCR-007), §9.4 (fresh:SCR-008), §9.6 (fresh:SCR-014) |
| `patristic-reception` | fresh:PAT-001 – fresh:PAT-004 | 4 | §0.4(f), §3.2 (route and digest re-confirmed), §2.1, §2.3, §2.4, §2.6 (re-confirmed) |
| `liturgical-history` | fresh:LIT-101 – fresh:LIT-104 | 4 | §0.4(f), §0.4(g), §6.1 (re-confirmed), §2.8 (re-confirmed) |
| `theological-synthesis` | fresh:THE-101 – fresh:THE-113 | 13 | §0.4(a)(b)(g), §7.6 (corrected), §7.1–§7.5 (re-confirmed), §9.1–§9.3, §9.6 (re-confirmed), §9.7 (fresh:THE-108 recorded as a lead) |
| `source-citation-coverage` | fresh:COV-012 – fresh:COV-019 | 8 | §10.1, §12.5 |
| `cultural-afterlife` | fresh:CUL-001 – fresh:CUL-004 | 4 | §0.4(d), §8.2, §8.3 (re-confirmed), §8.7 (new) |
| `precedent-search` | fresh:PRE-001 – fresh:PRE-011 | 11 | §0.4(c), §9.10 (all), §7.4 (fresh:PRE-006), §9.4 (fresh:PRE-005) |

**Total across both joins: 272, and every one is accounted for.**

---

**End of brief.** Written by one stage, which is the only stage that may write
it. **It replaced the `proper v10` brief of the same name in its entirety and
was then amended in place once, by the same stage at run
`e5b24f405bde9691`; no later stage may add to this brief or amend it**, and
every gap it leaves is named as a gap rather than left for the author to
discover.
