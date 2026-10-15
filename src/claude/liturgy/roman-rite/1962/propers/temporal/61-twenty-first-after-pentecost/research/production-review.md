# Production review — Twenty-first Sunday after Pentecost (1962 Roman Rite)

Production and review record for the canonical leaf
`liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost`,
`proper-study` v11, run `a8bcc37ea3420a07`, seeded at commit
`cc2e968320e2416ef9049f1c6910ac281df8feb9`, for Sunday 18 October 2026 and an
adult parish assembly. It records completed production facts only; review
verdicts are added by the stages that reach them.

## Research (before this record)

Context, research and three rounds of cold research review were completed in
the same run on 15 October 2026. The third research review returned PASS with
no blocking findings and two advisories, RES-012 (pointing differences in the
St Luke collation table of `propers/verified.md`) and RES-013 (the account in
`research/interpretations.md` 3.3 and `research/scope.md` 4.4 of how
Augustine's "until the judgment" depends on the unsung v. 84a). The study
author owns neither file and changed neither. RES-013 bears on the study's
wording: the third reading states that Augustine's "the Church would exist on
earth until the judgment" comes from the order of the verse's two questions,
the first of which the Communion does not sing, and names what the reading
takes from his comment on the sung half (the martyrs' plea answered by
long-suffering, and the vengeance at the judgment).

## Author-study, iteration 0 (15 October 2026)

Authored: `main.tex`, `format.tex`, `generation-metadata.tex`,
`web-edition.toml`, the schema-2 `proper-components.toml` (presentation,
format, authority and `orientation-v1` chronology contracts; future concise and
homily components declared, not yet written), and the research-mode components
`sections/00-opening.tex`, `05-appointed-texts.tex`, `10-each-element.tex`,
`20-armour-under-providence.tex`, `30-debt-forgiven-from-the-heart.tex`,
`40-last-exodus-of-the-church.tex`, `50-comparison.tex`,
`80-date-location.tex` and `90-apparatus.tex`.

### Scope of the study

- The ten appointed elements, Latin from `propers/verified.md` with
  Douay–Rheims (Challoner) English at the canonical verses and the 1861
  Cummiskey English for the Offertory, the Communion, the opening sentence of
  the Introit and the three orations, each as recorded there. The Introit's
  later clauses and the Gradual's respond are given in the Douay at the
  Vulgate verses with the Missal's departures described; no English was
  composed.
- The added orations (*pro Fidei propagatione*; St Luke at low and conventual
  Masses) are named by incipit and locus with their rubrics and not
  reproduced. The *Ordo Missae* no. 1130 is cited by incipit only.
- Three readings, matching the lanes of `research/interpretations.md`:
  `armour-under-providence` (carried by Gregory the Great and John
  Chrysostom), `debt-forgiven-from-the-heart` (John Chrysostom and Augustine),
  `last-exodus-of-the-church` (Augustine and John Chrysostom), each with its
  own four senses, followed by a comparison.
- Scriptural Date and Location: one `chronologyorientationtable` printing all
  eleven generated orientation rows once, with authored place phrases, and a
  note for each passage giving the record's sources and limits. This is the
  reviewed home for the concise study's page-2 rows. No biblical date is
  written in prose.
- Unsung context (Esth 13:12–17; Mt 18:21–22; Eph 6:18–20; Ps 89:3–17;
  Ps 118:81 *Defecit*, 82–83, 84a, 85, 86a, 87–88) is labelled wherever used.
  Hilary's "now", and the PG 27 exposition on v. 84, are said to rest on the
  unsung v. 84a. Rupert, Durandus, Honorius and Sicard are cited only for the
  elements their Mass shared, and at the Gospel's own locus in their books;
  their other Gospel appears in one clause of the scope appendix.
- Latin from Migne text layers (PL 107, 109, 170, 213) and from Durandus is
  described, not quoted; Aquinas's *Super Iob* and the Alphonsus sermon are
  quoted in a short phrase at most. Theodoret, read in research as context
  only, is not used.

### Word counts

Counted on the component sources with markup stripped (`detex`), so the
figures include Latin and quotations: opening 1,757; appointed texts 2,909;
each element 4,588; first reading 3,782; second reading 3,495; third reading
3,006; comparison 1,221; Scriptural Date and Location 1,325; scope appendix and
References 1,728. Substantive exposition (opening, element settings, readings
and comparison, without the appointed texts, chronology appendix and
apparatus) is about 17,800 words by this count, above the profile's
6,000–10,000-word planning range; the three readings together are about
10,300. The rendered PDF has 36 physical pages, within the 20–50-page range.

### Author proof

- `make doc DOC=liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost PROVIDER=claude`:
  settled with no LaTeX warning, overfull or underfull box in the log; 67
  contents lines on distinct anchors; component manifest and generation
  metadata valid; every font embedded. Research-edition PDF: 36 pages,
  SHA-256 `a0adc2e9d097660db3ac3b8b78f01c251dee8bf1a2bfc4b25959a0fa293cbd3e`,
  timestamp 2026-10-15T14:36:54Z. Every page was rasterized and inspected; the
  rights colophon shares the final page with the References and timestamp.
- `tools/check-proper-components --phase artifacts --edition research` and
  `scripts/_proper_study.py check --phase content --edition research` with
  `--require-presentation --require-format --require-authority
  --require-orientation`: pass.
- `check-content-preflight --edition research`: references-used,
  identifiers-resolve, bindings-valid, restricted-not-reproduced,
  relation-coverage, unquoted-not-quoted, structural-meta-labels, house-voice,
  chronology-record-current, chronology-annotations-current,
  chronology-claims-supported and provenance-matches-run: pass.
- `tools/tpt web-edition` (canonical conversion probe, Python Markdown 3.10.3
  as pinned, pandoc 3.11): pass. A first probe failed the generated-row payload
  audit for two orientation rows whose place phrase used `\textit`, which the
  chronology preflight admits in a place phrase but the converter's payload
  comparison does not render; the italic was removed from those phrases. The
  mismatch between the two tools is reported for their owners.

### Source limits carried by the study

As recorded in `research/scope.md` sections 5 and 11: no Greek witness of
registered standing and unquestioned authorship on Pss 89 and 118:81–86 (the
PG 27 expositions are cited under their printed attribution); Ambrose on
Ps 118, Hilary and Bellarmine on Ps 118:1, Theophylact, Cornelius a Lapide,
Hugh of Saint-Cher, Augustine's *De spiritu et littera*, Gregory's own text for
the sentence Rabanus gives under his name, Amalarius and Anthony of Padua not
reached; English of the NPNF, Oxford *Moralia*, Bellarmine, Fromage and
Schuster quoted from tracked transcriptions not collated with page images.

## Author-study, iteration 1 (15 October 2026)

The first cold study review returned one blocking finding, STU-001, and nine
advisories, STU-002 to STU-010. The study was repaired in its own components;
no research record was changed.

- STU-001 (blocking): the place phrase of the Gospel's comparison row
  (`row-da30707e22c82488`) said that the NABRE introduction gives no place for
  the writing of Matthew. It names Antioch in Roman Syria as a plausible
  suggestion (passage record `matthew-introduction`). The phrase now reads
  "Writing place: Antioch in Syria, which the NABRE introduction offers as a
  plausible suggestion", and the Matthew note says the same with its
  qualification. The generated date cell and the Ephesians rows are unchanged.
- Advisories cleared in the same files: Bellarmine's preferred opinion (David
  the author of all the psalms, as he says Augustine holds) given beside his
  admission of Moses, with the "different sides" sentence removed; his general
  prefaces paraphrased rather than quoted, Preface II credited in the
  References as the manuscript preface in Michael J. Miller's translation;
  Gregory's judgment that Job's own authorship is the more probable;
  Chrysostom's apostrophe and Augustine's "This is not cruelty" given to their
  own speakers; Fromage alone credited with making the Offertory the Sunday's
  centre; the denarius as a day's wage (Mt 20:2) and Augustine's reckoning in
  Sermon 83.3 added to the two debts; the PG 27 exposition no longer counted
  among those who answer *quando*, and said to hold both answers; the
  comparison's account of which authors serve which reading, and of which
  readings take up the Communion's plea, corrected; sentences that reported the
  study's own footing rewritten with a witness as subject; the opening's
  page-and-column boundary sentence removed and its occurrence paragraph moved
  after the texts and the Sunday's question; the Hilary--Augustine difference
  given its fullest home in the comparison, *De sermone Domini* I.22.77 and
  Sermon 58.8 in the second reading, and verbatim re-quotations between the
  element settings and the readings reduced to cross-references.
- A research-record defect for the reviewer to route: `research/scope.md`
  (Bellarmine on the authorship of Ps 89) says that Bellarmine's judgment
  "stands against Augustine's *Enarr.* 89.2"; both prefaces prefer the
  Davidic opinion that Bellarmine attributes to Augustine, so the two differ
  only on whether Moses' authorship is admissible. And
  `research/interpretations.md` 4.1, which has Gregory and Aquinas serve
  readings 1 and 3, understates Aquinas, who serves all three. The study author
  changed neither record.

Word counts by the same `detex` method: opening 1,711; appointed texts 2,909;
each element 4,528; first reading 3,696; second reading 3,587; third reading
2,909; comparison 1,382; Scriptural Date and Location 1,396; scope appendix and
References 1,720. Substantive exposition is about 17,800 words; the three
readings together about 10,200. The proof has 36 physical pages.

Author proof: `make doc` settled with no LaTeX warning, overfull or underfull
box; every font embedded; research-edition PDF 36 pages, SHA-256
`0346d038054178ba1f8f4ea6e534707f8b809628edbcf86ed717babe74761b62`, timestamp
2026-10-15T15:03:29Z. Every page was rasterized and inspected; the rights
colophon shares the final page with the References and timestamp (an
intermediate build that put it on a page of its own was repaired by shortening
the scope appendix and the Bellarmine reference). The component checker, the
content check with all four `--require` flags, the twelve content-preflight
checks and the canonical web conversion probe (Python Markdown 3.10.3, pandoc
3.11) pass.

## Author-study, iteration 2 (15 October 2026)

The second cold study review returned one blocking finding, STU-011, with the
advisories STU-007 and STU-012 standing. The study was repaired in its own
components; no research record was changed.

- STU-011 (blocking): the first reading's third difficulty said that Hilary and
  Augustine "differ in the time, not in the object", and the third reading's
  second difficulty said that the comparison shows the Fathers not to differ
  about the last judgment or the persecutors. Both now credit each witness with
  his own answer, read again in the sources: Hilary asks for a present power by
  which the devil and his ministers are crushed and says that this is *non
  illud utique quod in resurrectionis saeculo meminit futurum*, while
  affirming that judgment (PL 9, Caph 5, read on the tracked text layer);
  Augustine hears the martyrs' cry for the final judgment on the Church's
  persecutors (*Enarr.* 118, Caph 84–88, NPNF); Bellarmine, the condemnation
  of the wicked who persecute and tempt (Ps 118:84–85); Cassiodorus joins
  Hilary's persecutors to the judgment at the end. Both passages say that the
  Fathers differ in what is asked and in whom the plea names as well as in the
  time, and call the answers compatible, not identical, through Hilary's
  affirmation of the last judgment and Thomas's men moved by the devil, which
  the first reading already gives. The comparison's "Where they differ"
  paragraph and its persecutors row for the third reading say the same, and its
  "closer than the difference of time suggests" sentence is gone.
- STU-007 (advisory) cleared in part: the Gospel's setting no longer says that
  the second reading "reckons" the size of the ten thousand talents; it says
  that the second reading gives the hundred pence's value and Augustine's
  reckoning. No value for the talent was added.
- STU-012 (advisory), a research-record defect, stands for the reviewer to
  route: `research/scope.md` (Bellarmine on Ps 89, 4.7, 7.4 and 11) omits
  Bellarmine's Preface II §5 and his Davidic reading of Ps 89, and
  `research/interpretations.md` 4.1 has Aquinas serve readings 1 and 3 only.
  The study states both correctly; the study author changed neither record.

Word counts by the same `detex` method: opening 1,711; appointed texts 2,909;
each element 4,536; first reading 3,811; second reading 3,587; third reading
3,022; comparison 1,458; Scriptural Date and Location 1,396; scope appendix and
References 1,720. Substantive exposition is about 18,100 words; the three
readings together about 10,400. The proof has 37 physical pages; the
comparison now ends on a page of its own before Scriptural Date and Location.

Author proof: `make doc` settled with no LaTeX warning, overfull or underfull
box; every font embedded; research-edition PDF 37 pages, timestamp
2026-10-15T15:22:00Z. The changed pages were rasterized and inspected; the
comparison table stands whole on one page, and the rights colophon shares the
final page with the References and timestamp. The component checker, the
content check with all four `--require` flags, the twelve content-preflight
checks and the canonical web conversion probe (Python Markdown 3.10.3, pandoc
3.11) pass.

## Derive-synthesis, iteration 0 (15 October 2026)

Authored after the third cold study review returned PASS at its iteration 2
with no blocking finding (advisories STU-005, STU-012, STU-013 and STU-014).
The stage ran as a Claude Code harness subagent, `claude-opus-5-5[1m]`,
dispatched at reasoning effort `high`. The concise companion is *The
Twenty-first Sunday after Pentecost: A Concise Study of the Proper in the 1962
Roman Missal*, built from `synthesis.tex` and derived from the accepted
expansive study of this leaf for the occurrence of 18 October 2026. No research
record, study component or manifest entry was edited for it; the manifest
already declared the six concise components, their modes and the presentation
roles. The shared `generation-metadata.tex` received a refreshed revision
timestamp and one appended contribution for this stage.

Components written:

- `concise-inventory` (`sections/concise/01-inventory.tex`): the map of the ten
  appointed elements in the order of the Mass, condensed from the study's map,
  with the 1861 English for the Introit's first sentence, the Collect, the
  Offertory, the Secret, the Communion and the Postcommunion, and the Douay at
  the canonical verses for the Scripture. A rubrical note gives second class,
  green, Gloria, Credo and the Trinity Preface, the commemoration of St Luke in
  low and conventual Masses only, and the oration *pro Fidei propagatione* in
  every Mass unless the Ordinary has appointed another day for the missions.
- `concise-overview` (`sections/concise/02-overview.tex`): exactly four rows,
  drawn from the three readings' own senses, each witness named beside the
  clause he states.
- `concise-date-location` (`sections/concise/03-date-location.tex`): the page-2
  sheet. It imports the generated annotations once and places all eleven
  `orientation-v1` rows once, in the generator's order and grouping, inside
  `chronologyorientationtable`, with the place phrases of the study's reviewed
  Scriptural Date and Location appendix unchanged (including the STU-001
  repair of the Gospel comparison row). A closing line refers the reader to
  that appendix for sources and attributions. No date is written by hand.
- `concise-themes` (`sections/concise/04-themes.tex`): *The Propers: Themes and
  Movement*, opening with a direct thesis (a will none resists, and what lives
  inside it: an adversary who must ask, a forgiven debtor who must forgive, a
  people out of Egypt that asks when). It follows the formulary in order with
  the textual returns the study records: the Introit's dropped condition, the
  Collect's *te protegente* and adversities beside the Gradual and Epistle, the
  Collect's *pietas* returning in the Secret's *potenti pietate*, *petiit* and
  *data est a Domino* against the Introit, Ps 118 at the Introit's verse and the
  Communion, and the Postcommunion's mouth and mind beside *Quod ore sumpsimus*
  (*Ordo Missae* no. 1130). It closes with the three readings' questions and
  carrying witnesses, and what they share, in the terms of the study's
  comparison.
- `concise-commentary` (`sections/concise/10-commentary.tex`): *The Propers:
  Detailed Commentary*, in six cross-proper units, each setting the readings'
  answers beside one another:
  - A will none resists, and an adversary who asks (Introit, Offertory,
    Collect; Gregory, Thomas, Rupert, Schuster; the second and third readings'
    hearing of Mardochai and Job; Rupert and Durandus).
  - Who is the enemy, and what is the armour? (Epistle, Gradual, the Gospel's
    torturers, the Secret; Chrysostom, Thomas, Jerome, Fromage, Bellarmine,
    Durandus; the first and second readings' meeting at Chrysostom's sentence).
  - What the king's mercy requires (Gospel with the Introit's verse, Collect,
    Secret and Postcommunion; Augustine, Chrysostom, Jerome, Thomas, Rabanus,
    Cassiodorus, Schuster; the three formulations of the pardon's return kept
    side by side, Thomas's narrower and real difference named).
  - When wilt thou judge? The Communion's persecutors (Augustine's answer to
    the charge of vengeance; Hilary, Augustine, Cassiodorus, Bellarmine and the
    PG 27 exposition on the thing asked, the persecutors and the time, with the
    unsung v. 84a named as the source of Hilary's "now" and Augustine's
    "until"). This is the difference's single home in the concise study, which
    answers the repetition STU-005 noted in the study. Per STU-013, the
    passage says "the witnesses differ", since Bellarmine and Cassiodorus are
    not Fathers.
  - A people on the march (Alleluia, the Epistle's girded loins and evil day,
    the Gradual's eternity, the Gospel's reckoning, Introit, Secret and
    Postcommunion; Augustine, Cassiodorus, Chrysostom, Fromage, Thomas,
    Honorius, Durandus, Alphonsus, Bellarmine).
  - One Mass, three answers (the demanding feature each reading meets, the
    second and third readings' meeting at Sermon 58.8, and the readings'
    allegorical, moral and anagogical senses compared where they differ).
- `concise-apparatus` (`sections/concise/90-apparatus.tex`): the scope note and
  the References for the sources this companion uses (24 entries). The scope
  note does not mention the commentators' other Gospel, as the three-document
  profile requires of the concise study.

Every reading's controlling claim is preserved, and so are the study's
differences: Gregory's two wills and Thomas's will and power; Jerome's
Christological and Thomas's moral armour; Chrysostom's revoking receiver,
Augustine's recalling God and Thomas's return *per ingratitudinem*; Jerome's
rejection of the devil as debtor and Rabanus's allegory; and the Communion's
persecutors and time in Hilary, Augustine, Cassiodorus, Bellarmine and the
PG 27 exposition. Set aside in compression, and carried by the study: the
element settings' Honorius, Sicard and Rabanus on Esther; Augustine and
Bellarmine on the authorship of Ps 89; Augustine's numerology in Sermon 83.6;
Hilary on Matthew; Chrysostom on Ps 113; Schuster on the Communion and the
Postcommunion; and Origen's own text. No new evidence-dependent claim was
added, and no upstream defect was found while deriving.

### Word counts

Counted with `detex` on the component sources, so the figures include Latin
and quotations: inventory 402; overview 267; Scriptural Date and Location 314
(authored text only; the generated rows are imported); Themes and Movement
1,571; commentary 4,913; scope note and References 1,491. The substantive
concise argument (overview, Themes and Movement, commentary) is about 6,750
words.

### Author proof

- `make doc DOC=liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost-synthesis PROVIDER=claude`:
  settled with no LaTeX warning, overfull or underfull box in the log; 10
  contents lines on distinct anchors; component manifest and generation
  metadata valid; every font embedded (Latin Modern, Type 1). Synthesis PDF:
  12 physical pages, SHA-256
  `6dac0a78aba16c93ba78a9148a162d9aab480388ce89b8bfcacebecebc846b9e`; auxiliary
  file `00c088503b8c419acd594f57901c37684856880c72c00b03508ac4d578967293`;
  timestamp 2026-10-15T15:44:10Z.
- Settled physical pages from the auxiliary file: inventory and all four sense
  markers and the overview on page 1; chronology on page 2; themes from page 3
  to page 4; commentary from page 5. The terminal apparatus ends on page 12 with
  the timestamp and rights colophon.
- Every page was rasterized and inspected. Two earlier proofs were repaired:
  the first spilled the overview onto page 2 and ran to 13 pages, cured by
  condensing the map, rubrical note and Literal row; the second left a third of
  page 4 empty, cured by adding the formulary's textual returns and the
  readings' meeting points to the themes.
- `tools/check-proper-components --phase artifacts --edition synthesis`,
  `scripts/_proper_study.py check --phase content --edition synthesis` with the
  four `--require` flags, the twelve `check-content-preflight --edition
  synthesis` checks and `provenance-matches-run`: pass. The research edition,
  rebuilt with the shared metadata, still has 37 pages with no warning and its
  colophon on the final page.

### Outstanding

Cold concise review; homily authoring and review; the shared-timestamp
three-document build; visual review; canonical web generation and review;
installation and publication gates.

## Derive-homily, iteration 0 (15 October 2026)

Authored after the cold concise review returned PASS at its iteration 0 with
no blocking finding (advisories SYN-001 to SYN-005, none of which touches the
homily). The stage ran as a Claude Code harness subagent,
`claude-opus-5-5[1m]`, dispatched at reasoning effort `high`. The homily is
*The Twenty-first Sunday after Pentecost: The Words That Saved Him*, built from
`homily.tex`, addressed to an adult parish assembly for the occurrence of
18 October 2026, and derived from the two accepted studies of this same leaf.
No research record, study or concise component, or manifest entry was edited
for it; the manifest already declared both homily components with complete
element keys and the references they use. The neighbouring Claude leaf
`60-twentieth-after-pentecost` was consulted only for the shape of its homily
files; no claim, locus or quotation was taken from it. The other provider's
leaf for this identity was not opened. The shared `generation-metadata.tex`
received a refreshed revision timestamp and one appended contribution for this
stage.

The entrypoint imports `common/preamble`, `common/propers-format` and
`common/propers-homily` in that order, then the leaf's `format.tex`, and uses
the shared full-width `\propertitle`. The `properhomily` environment encloses
only the literal import of the spoken component; the terminal note follows the
environment's closing page break and sets its running heads with
`\runninghead`. No font, geometry, title or column setting is overridden.

- `homily-body` (`sections/homily/10-homily.tex`): the spoken text, continuous
  preaching with no heading, no direction to a preacher and no citation inside
  the speech, in nine movements: the same plea said twice and the governing
  question; the two debts, with the denarius as a day's wage, Chrysostom's
  threat "of unspeakable tenderness" and gift beyond the request, and
  Augustine's every man a debtor with a debtor; the plea heard and refused,
  with Chrysostom's harbour not recognized; the debt that returns, with
  Chrysostom's receiver who revokes, Augustine's God who calls back, and
  Aquinas's narrower teaching; the wrong throat, with the Epistle, Chrysostom
  on Ephesians, the Introit, the Offertory with Gregory's bridle, and
  Chrysostom's devil become a cause of crowns; "from your hearts", with
  Augustine on tongue and heart and the surgeon; the Communion's plea, with
  Augustine's patience of God; a response for the week, with the Lord's Prayer
  as Augustine's covenant, the Collect and the Postcommunion; and the return to
  the king's house.
- `homily-note` (`sections/homily/90-note.tex`): the terminal note and the
  References, read aloud by nobody: audience and occasion, word count and pace,
  relation to the three reviewed readings, the route of each quoted text, and
  the exact loci.

### The argument, and the profile's test

The homily follows the second reading, `debt-forgiven-from-the-heart`,
sharpened by the first reading's redirect, as `research/interpretations.md`
§ 4.7 recommends. From `armour-under-providence` it takes Chrysostom's enemy
behind the human enemy (*Hom. in Eph.* 22), the Introit's will that none
resists, the Offertory's petition and permission with Gregory's bridle
(*Moralia* II.19), and Chrysostom's devil become a cause of crowns (*Hom. in
Matth.* 61.5). `last-exodus-of-the-church` and the witnesses' difference over
the Communion's persecutors are left to the studies; the Communion's plea is
met from Augustine's *Sermon* 58.8, as the second reading meets it.

- **Governing question.** What does a forgiven man owe the man who has wronged
  him?
- **Image.** The forgiven servant's hand on his fellow servant's throat
  (*tenens suffocabat eum*, Mt 18:28). It returns at the Epistle (the wrong
  throat), at the response for the week (whose throat we are holding), at the
  Postcommunion and at the close.
- **Decisive turn, and the textual detail that makes it.** The fellow
  servant's plea repeats the servant's own in the same words, *Patientiam habe
  in me, et omnia reddam tibi* (Mt 18:26, 29), so that the forgiven man hears
  and refuses the prayer that saved him (Chrysostom, *Hom.* 61.4); and *de
  cordibus vestris* (18:35) with *non est nobis colluctatio adversus carnem et
  sanguinem* (Eph 6:12). These change the familiar problem of a grudge one
  feels entitled to keep from "has he deserved my pardon?" to "do I recognize
  my own prayer in his mouth?", and the anger it carries from the man to the
  adversary who wants the grudge kept.
- **Text-substitution test.** The question, image and turn depend on this
  Gospel's two debts, its repeated plea, its returned *universum debitum* and
  its *de cordibus vestris*; the Epistle's enemy who is not flesh and blood,
  the Introit's *non est qui possit resistere voluntati tuae*, the Offertory's
  *petiit* and *data est ei potestas a Domino*, the Communion's *quando facies
  de persequentibus me iudicium?*, the Collect's *familiam tuam* and *continua
  pietate*, and the Postcommunion's *quod ore percepimus, pura mente sectemur*
  carry the movement. With unrelated readings the argument would not survive.

Bounds kept:

- Aquinas's distinction is kept beside Chrysostom and Augustine: the hearer is
  told that a grudge does not undo his baptism and that ingratitude makes him a
  debtor again (§ 2.3; study, "Who revokes the pardon?"). Aquinas is
  paraphrased, not quoted.
- Chrysostom's wrath poured on the devil is aimed at the devil alone, and the
  speech says that he does not call the wrong nothing or the wrongdoer
  innocent (§ 1.6).
- "From the heart" forbids rancour, not correction (Augustine, *Sermon* 83.8;
  § 2.3).
- No Father is said to join the Gospel to any chant or oration beyond the
  joins he makes himself (Chrysostom: the wronged man and the devil; the devil,
  Job and the man feared as an enemy). The joins are the homily's own and
  credited to no one: the servant's hand on the wrong throat, the Introit and
  Offertory as the measure of the enemy's reach, the Collect's family as the
  household of forgiven servants, the Postcommunion's mouth and mind beside the
  Gospel's heart, and the Communion's plea answered from a sermon that speaks
  of the martyrs not yet avenged and not of this chant. Gregory is cited only
  for Job's trial.
- The unsung context is not used: neither Peter's question nor *septuagies
  septies* (Mt 18:21–22), nor Ps 118:84a, nor Esth 13:12–17. No commentator's
  other Mass, no compilation history and no other Sunday is mentioned; the
  added oration and St Luke's commemoration are named only in the note.
- Augustine's numerology (*Sermon* 83.5–7) is not used (§ 2.6).

No English of a liturgical text was composed. The Introit's opening sentence,
the Collect, the Communion's question and the Postcommunion are quoted in the
1861 Cummiskey English; the Offertory is paraphrased. The note records that the
1861 "receive" renders *sectemur*, and the speech says that the Latin asks the
pure mind to follow. The Lord's Prayer is quoted only as Augustine's translator
gives it. The speech ends as preaching, with no recited prayer. No anecdote,
personal experience, clerical identity, miraculous story or attributed
quotation was manufactured.

### Verification performed at this stage

Every quoted or paraphrased witness was read at its locus in this stage, not
taken from the studies:

- Chrysostom, *Hom. 61 in Matth.*, in the tracked NPNF1-10 CCEL text (SHA-256
  `adb8f1c9…` recomputed and matched), §§ 3–5: "of unspeakable tenderness",
  "not that he should be sold", "The servant asked only for delay …",
  "straightway", "did not recognize so much as the harbor …", "it was not he
  that revoked it …", "if the devil hath become a cause of crowns …".
- Chrysostom, *Hom. 22 in Eph.*, in the tracked NPNF1-13 text (`54274dd9…`,
  recomputed), lines 15353–15356 and 15479–15482.
- Augustine, *Sermon* 83 (NPNF Sermon 33) §§ 2, 4, 7, 8 and *Sermon* 58
  (NPNF Sermon 8) § 8, in the tracked NPNF1-6 text (`ce371798…`, recomputed).
- Gregory, *Moralia* II.19, in the tracked Oxford text (`d9f9ed86…`,
  recomputed), line 2180.
- Aquinas, *Super Matth.* c. 18, in the tracked Venice 1745 OCR (`10aa155e…`,
  recomputed), lines 31276–31283: *Hic videtur innuere quod peccata dimissa
  redeant, sicut vult Origenes … Sed hoc non videtur, eo quod remissio
  efficaciam habet a sacramentis … Dicuntur autem redire per ingratitudinem.*
  Paraphrased, not quoted.
- Cummiskey 1861: the registered scan was fetched from its source URL into the
  run's scratch area; SHA-256 `85034c90…eae028898` and 24,767,551 bytes
  matched. PDF pp. 459 and 461 (printed pp. 450 and 452) were rendered at
  110 dpi and the Introit's first sentence, the Collect, the Offertory, the
  Communion and the Postcommunion read on the image. The Collect and
  Postcommunion were also matched in the tracked payload
  `temporal-orations-en` (SHA-256 `c79e9500…`, recomputed), lines 173 and 175.
- Scripture: every quoted verse matched in the tracked Challoner verse tables
  (Matthew `dd0ba183…`, Ephesians `10c79be0…`, digests recomputed); Mt 20:2,
  paraphrased, was read there.

The fetched scan stays in the run's scratch area; nothing was added to the
source library. A script then compared all 33 quoted spans of the speech with
those texts; all 33 were found, the two spans of the 1861 Introit and
Communion against the reading of the scan image.

**Spoken word count: 1,446 words.** The count is taken over
`sections/homily/10-homily.tex` alone: comments removed, every macro dropped,
whitespace-separated words carrying a letter or digit counted. The same count
over the extracted text of the built PDF's first two pages, without the title
block and running heads, is 1,456, the difference lying in the extraction's
splitting of words at line ends and around the spaced ellipsis. At an
unhurried 120 to 130 words a minute that is 11.1 to 12.1 minutes; at 110 it
would be 13.1. The figure is arithmetic and not a timed delivery: nobody has
spoken these words and no rehearsal was audible. The prose was read through in
full, silently, for sense, sentence length (111 sentences, mean 13.0 words,
median 12, longest 39, Chrysostom's sentence on pouring wrath on the devil
quoted whole) and ease of speech. A first draft of 1,554 words was cut. The
reading also shortened the account of Aquinas's teaching to what he says, and
replaced a sentence that made Augustine call the prayer itself, rather than its
condition, a covenant.

### Author proof and checks

The shared generation record carries a contribution for this stage and the
revision timestamp `2026-10-15T16:06:44Z`. All three documents were rebuilt
at that timestamp with `make doc`; each settled log carries no overfull or
underfull box, LaTeX warning, undefined reference or rerun request. An
intermediate homily build overfilled its second page by 10 pt inside the
columns; the spoken text was shortened, not the measure. The homily has 3
physical pages: the spoken body on pages 1–2 in two Latin Modern columns, the
note, References, revision timestamp and rights colophon on page 3. `pdffonts`
reports Latin Modern Roman and Mono only, all embedded Type 1 subsets. The
study is unchanged at 37 pages and the concise study at 12; the concise
auxiliary file is byte-identical to the one its review read, with inventory,
overview and the four sense markers on page 1, chronology on page 2, themes on
pages 3–4 and commentary from page 5. The final pages of all three carry the
timestamp and the colophon together.

These checks pass on the final sources:

- `scripts/_proper_study.py check … --date 2026-10-18 --phase content` for the
  homily, research and synthesis editions, with `--require-presentation
  --require-format --require-authority --require-orientation`;
- every `check-content-preflight --edition homily` check: bindings-valid,
  chronology-annotations-current, chronology-claims-supported,
  chronology-record-current, house-voice, identifiers-resolve,
  proposal-fields, references-used, relation-coverage,
  restricted-not-reproduced, structural-meta-labels, unquoted-not-quoted, and
  provenance-matches-run against this run's workflow, version, digest, run id
  and seed commit; the research and synthesis editions' preflight also passes;
- `tools/check-proper-components --phase artifacts` for the research,
  synthesis and homily editions;
- `tools/check-generation-metadata` for the leaf and for each of the three PDFs;
- the canonical web conversion probe of the study (`tools/tpt web-edition`,
  Python Markdown 3.10.3 as pinned) into the run's scratch area.

| File | SHA-256 |
| --- | --- |
| Homily proof PDF | `9e7fa1af5ce341a21d206ba843844f100b04915135e2f327cfb67ab1a487946e` |
| Homily auxiliary file | `96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486` |
| Homily log | `9dae3e6ba77cf83b5319450462cd49e138e66b0c3466f3e2d32aa030fe4f62d5` |
| Expansive study, rebuilt | `73a34a6fe54a279bf07d46eae892331c75cb7269d16b98f5bcd2e268a7018e36` |
| Concise study, rebuilt | `8f5dafd8a3b8c8ffa3de91151fff648474723ecaa3bd4247899207fa7deae625` |
| Concise auxiliary file | `00c088503b8c419acd594f57901c37684856880c72c00b03508ac4d578967293` |

The author read all three pages of the homily proof at 80 dpi, and the final
pages of the study and the concise study. This is an author proof inspection,
not the independent visual evaluation.

### Upstream observations reported for the homily's cold reviewer

- No missing argument or source was found for the homily.
- STU-012 still stands against `research/interpretations.md` § 4.1, which has
  Aquinas serve readings 1 and 3 only; the homily follows the study, in which
  he serves the second reading too.
- The 1861 book's English of the Introit, Offertory and Communion has no
  registered passage record (`propers/verified.md`, "English, the Sunday's
  orations"); the homily's two quotations from it rest on this stage's reading
  of the registered scan's page images.

### Outstanding

Cold homily review; the shared-timestamp three-document build; visual review;
canonical web generation and review; installation and publication gates.

## Derive-homily, iteration 1 (15 October 2026)

Revised after the cold homily review returned one blocking finding, HOM-001,
and four advisories, HOM-002 to HOM-005. The stage ran as a Claude Code harness
subagent, `claude-opus-5-5[1m]`, dispatched at reasoning effort `high`.
Changed: `sections/homily/10-homily.tex`, `sections/homily/90-note.tex`, the
PDF subject in `homily.tex`, and the shared `generation-metadata.tex`, whose
revision timestamp was refreshed and whose derive-homily contribution was
extended for this iteration. No research record, study or concise component,
or manifest entry was edited; the manifest already declares every element key
for both homily components.

### HOM-001: the movement through the Paschal mystery

The iteration-0 body moved from the parable to daily conduct without saying
where the unpayable debt is forgiven, mentioned Baptism only inside the Aquinas
paraphrase, and left the Secret to the studies. The revised body follows the
order of the Homiletic Directory, nos. 12–15, as
`guidance/liturgy/propers-three-documents.md` adopts it:

- **Proclamation.** A new movement after the two debts: the king forgives with
  a word, and the homily says what that word cost, the debt paid on the Cross
  in the blood of the King's own Son, the Father raising him from the dead,
  the ten thousand talents forgiven "on Calvary and at the empty tomb". The
  pardon reaches the hearer at the font, in Augustine's own join of the
  parable to Baptism, *Sermon* 83.7: "every man begins from Baptism; he goes
  out free, the 'ten thousand talents' are forgiven him; and when he goes out,
  he will soon find some fellow-servant his debtor." The next movement opens
  from that sentence ("Now watch the forgiven man go out"), so the later
  sentence "A grudge does not undo your baptism" now has its preparation.
- **Preparation for the Eucharist.** A new movement after the Communion's plea
  and before the response for the week. It quotes the Secret in the 1861
  English, "Mercifully receive, O Lord, these offerings, by which thou art
  pleased to be appeased, and restore us to salvation by thy powerful
  goodness", says that what is offered is the one sacrifice of the Cross made
  present and not a second payment beside it, and asks the assembly to come to
  Communion as the servant came to the king, with nothing to pay. It sets
  Augustine's sentence that in prayer we are all God's beggars and ask God for
  Christ the living Bread (*Sermon* 83.2, paraphrased) beside the altar, and
  names the Postcommunion's "food of immortality" and its petition, given from
  the Latin *sectemur*, as a share in the Lord's death and rising.
- **Consequence.** Only then the response for the week: name the debt; mean
  the condition of the Lord's Prayer, said at the altar before Communion; aim
  the anger at the adversary; and the Collect's family as a household
  "forgiven at the same price", ending with the sentence that no one who has
  received the Lord should take his brother by the throat, now a consequence
  of the preparation rather than its substitute. The close returns to the
  king's house with the King who forgave "at the price of his Son's blood, and
  feeds him at his own table".

No Father is credited with a join he does not make. Augustine joins the talents
to Baptism himself (83.7). His beggars and living Bread (83.2) are said of
prayer, and the note says so; the join to the altar is the homily's. The
Secret and Postcommunion are read as the homily's own synthesis, in line with
`research/interpretations.md` 2.4 (Secret: "editorial in joining to the king's
remission"; Postcommunion: editorial synthesis), and no Father or liturgical
commentator is cited for them in the speech.

### The advisories

- **HOM-002.** Augustine's *Sermon* 58 is introduced as "preaching on the
  Lord's Prayer", after the NPNF heading "Again on the Lord's Prayer"; the note
  names it the same way.
- **HOM-003.** The Epistle movement now opens "Why does the forgiven servant do
  it?"
- **HOM-004.** God's patience "waits for the conversion of the one who wronged
  us", so that "the enemy" keeps the adversary as its one referent.
- **HOM-005.** Quoted spans fall from 33 to 24 and from about 465 to 331
  words. Kept: the harbour not recognized, the pardon revoked by its receiver,
  the wrath poured on the devil, the tongue and the heart, the surgeon, and
  Augustine on Baptism. Paraphrased: the gift beyond the request, every man a
  debtor with a debtor, God's beggars. Dropped: the threat "of unspeakable
  tenderness", Chrysostom's "imagine not …" on Ephesians, Augustine's "I will
  call thee back", his "Better is it …", his covenant of the Lord's Prayer,
  Gregory's bridle (and with it Gregory's References entry) and Chrysostom's
  devil become a cause of crowns. "A few lines later he says" became "And so,
  he says", and "preaching on those words" became "Explaining this passage".

### The argument, and the profile's test

The governing question, image and decisive turn are unchanged from iteration
0: what does a forgiven man owe the man who has wronged him; the hand on the
fellow servant's throat; and the fellow servant's plea repeated in the same
words as the servant's own (Mt 18:26, 29), with *de cordibus vestris* (18:35)
and Eph 6:12. The repair adds a second textual hinge. The Secret's *hostias
quibus et te placari voluisti* names the sacrifice by which the remission is
won and given, so that the listener hears the parable's forgiveness as received
at this altar before he is asked to extend it. Under the text-substitution test
the new movements depend on this Gospel's unpayable debt and on this Mass's
Secret and Postcommunion; with unrelated readings they would not survive.

### Verification performed at this stage

All 24 quoted spans of the revised speech were compared by script, with
whitespace and quotation marks normalized, against the tracked texts, and all
were found: the Challoner Matthew and Ephesians verse tables (`dd0ba183…`,
`10c79be0…`); NPNF1-6 (`ce371798…`, SHA-256 recomputed and matched),
*Sermon* 83 §§ 2, 4, 7 and 8 and *Sermon* 58 § 8, with the heading of
*Sermon* 58 read at its line; NPNF1-10 *Hom.* 61 §§ 3–4; NPNF1-13 *Hom. in
Eph.* 22, whose wrath passage was read in the homily's moral part after the
exposition of Eph 6:10–13; and the 1861 payload `temporal-orations-en`
(`c79e9500…`, recomputed), lines 173–175, for the Collect, Secret and
Postcommunion. The Introit's first sentence and the Communion's question are
unchanged from iteration 0 and rest on that stage's reading of the 1861 scan
image; this stage matched them only against the study's printed English and
did not re-read the image.

**Spoken word count: 1,442 words** (iteration 0: 1,446), counted over
`sections/homily/10-homily.tex` alone as before: comments removed, macros
dropped, whitespace-separated words carrying a letter or digit. At 120 to 130
words a minute that is 11.1 to 12.0 minutes. The figure is arithmetic and not a
timed delivery; nobody has spoken the text and no rehearsal was audible. The
revised prose was read through in full, silently, for sense and oral clarity
(114 sentences). A first revision ran to 1,675 words and was cut by the
quotation reductions above. A later build put the body's last lines on a third
page; short paragraphs were joined and a sentence shortened, and the measure
was left alone.

### Author proof and checks

The shared generation record carries the revision timestamp
`2026-10-15T16:27:39Z`. All three documents were rebuilt at it with `make doc`;
their settled logs carry no overfull or underfull box, LaTeX warning,
undefined reference or rerun request. The homily has 3 physical pages: the
spoken body on pages 1–2 in two Latin Modern columns, and the note, References,
revision timestamp and rights colophon on page 3. `pdffonts` reports Latin
Modern Roman and Mono only, all embedded subsets. The study is 37 pages and the
concise study 12; the concise auxiliary file is byte-identical to the one its
review read. These checks pass on the final sources: `scripts/_proper_study.py
check` at phase content for the homily, research and synthesis editions with
`--date 2026-10-18 --require-presentation --require-format --require-authority
--require-orientation`; every `check-content-preflight` check for the three
editions, with provenance matched against this run; `tools/check-proper-components
--phase artifacts` for the three editions; `tools/check-generation-metadata`
for the leaf and the three PDFs; and the web conversion probe of the study
(`tools/tpt web-edition`, Python Markdown 3.10.3 as pinned) into the run's
scratch area.

| File | SHA-256 |
| --- | --- |
| Homily proof PDF | `88631112fc3a7c8dfb38fac0d9cb561a4d4487958fcb15593845d9102ebd0b44` |
| Homily auxiliary file | `96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486` |
| Expansive study, rebuilt | `e7c90080f6a14ba875742ebe822a86d3192027ae36c9a43a404d1ae1e1968285` |
| Concise study, rebuilt | `3e066c1b2ec5d240dfcf7a1b18a5421373b1da067b61ffdc57a1178bda0fd541` |
| Concise auxiliary file | `00c088503b8c419acd594f57901c37684856880c72c00b03508ac4d578967293` |

The author read the three homily pages at 80 dpi. This is an author proof
inspection, not the independent visual evaluation.

### Upstream observations reported for the homily's cold reviewer

- None new. The iteration-0 observations (STU-012 on
  `research/interpretations.md` § 4.1; no registered passage record for the
  1861 English of the Introit, Offertory and Communion) still stand.

### Outstanding

Cold homily review; visual review; canonical web generation and review;
installation and publication gates.

## Build-artifacts, iteration 0 (15 October 2026)

Run after the cold homily review returned PASS at its iteration 1 with no
blocking finding (advisories HOM-006 and HOM-007). The stage ran as a Claude
Code harness subagent, `claude-opus-5-5[1m]`, dispatched at reasoning effort
`high`. No source file of the leaf was edited: no layout repair was needed, so
the generation record, its revision timestamp `2026-10-15T16:27:39Z` and every
content seal stand as the reviews left them.

### Builds

All three documents were built with `make doc DOC=<id> PROVIDER=claude`. The
study and concise study were rebuilt by the Makefile; the homily, up to date,
was rebuilt by removing its build PDF first. Each build reproduced the bytes of
the derive-homily proofs exactly.

| Output | Physical pages | PDF SHA-256 |
| --- | --- | --- |
| `61-twenty-first-after-pentecost` (study) | 37 | `e7c90080f6a14ba875742ebe822a86d3192027ae36c9a43a404d1ae1e1968285` |
| `61-twenty-first-after-pentecost-synthesis` (concise) | 12 | `3e066c1b2ec5d240dfcf7a1b18a5421373b1da067b61ffdc57a1178bda0fd541` |
| `61-twenty-first-after-pentecost-homily` | 3 | `88631112fc3a7c8dfb38fac0d9cb561a4d4487958fcb15593845d9102ebd0b44` |

Auxiliary files kept with the PDFs under `build/claude/`: study
`8d378f83288e07c1f0544da91013f7da39596b575bd5a4121c82567e9d2a2b49`, concise
`00c088503b8c419acd594f57901c37684856880c72c00b03508ac4d578967293` (identical
to the one the concise review read), homily
`96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486`.

### Checks

- Logs: no error, LaTeX or package warning, overfull or underfull box,
  undefined reference or rerun request in any of the three settled logs. The
  Makefile reported 67 contents lines for the study and 10 for the concise
  study, each on its own anchor; component manifest and generation metadata
  valid.
- Structure and fonts: letter paper, PDF 1.7, pdfTeX; titles and subjects set
  for all three. `pdffonts` lists Latin Modern Roman and Mono only (Type 1),
  every font embedded and subset.
- Extraction: `pdftotext -layout` gives 24,876 words (study), 9,384 (concise)
  and 2,356 (homily, body and note); no `??`, stray control sequence or
  replacement character.
- Concise physical pages from the settled auxiliary file: inventory, overview
  and all four sense markers on page 1; chronology on page 2; themes from page
  3 to page 4; commentary from page 5.
- `scripts/_proper_study.py check --phase artifacts` with `--date 2026-10-18`
  and the four `--require` flags, after the snapshot: pass.
  `tools/check-proper-components --phase artifacts` for the research,
  synthesis and homily editions, and `tools/check-generation-metadata` for the
  three PDFs: pass.
- Snapshot: `scripts/_proper_study.py snapshot` wrote `research/artifacts.json`
  (receipt schema 2: the three PDFs, 27 render inputs, and the study and
  concise auxiliary files as pagination evidence). It records bytes, not a
  review.
- Rasters: `tools/tpt pdf-review` rendered all 52 pages with contact sheets
  into the run's raster directory. The builder looked at every contact sheet
  and at concise pages 1, 2, 4 and 12, study page 30 and homily pages 2 and 3
  at full size. No clipping, overflow, collision or stray blank page was seen.
  This is a builder's check, not the independent visual review.

### Remaining limitations

- The page-2 orientation rows give their generated passage labels in two
  forms (`Ps 118:1` beside `Psalm 89:1-2`, and hyphens in `Job 2:6-7` and
  `Matthew 18:23-35` where the authored text uses en dashes). These come from
  the generator's labels and were left alone; the visual reviewer may judge
  them.
- The upstream observations already reported (STU-012 on
  `research/interpretations.md` § 4.1; no registered passage record for the
  1861 English of the Introit, Offertory and Communion) still stand.

### Outstanding

Visual review; canonical web generation and review; installation and
publication gates.

## Author-study, iteration 3 (15 October 2026)

Re-entered after the artifact gates found the research review seal stale. The
only sealed input that had moved was `scripts/_tooling.py`, a chronology
computation input, changed by a tool-registry commit outside this leaf.
Research iteration 3 edited no file, and the fourth cold research review
returned PASS at its iteration 3 with no blocking finding (advisories RES-012
to RES-015). The packet forwarded no study finding. The stage ran as a Claude
Code harness subagent, `claude-opus-5-5[1m]`, dispatched at reasoning effort
`high`.

No study component, manifest entry, research record or generation record was
edited. All 21 inputs sealed by the study review at its iteration 2 were
re-hashed and are unchanged, so the revision timestamp `2026-10-15T16:27:39Z`
and the contribution history stand. The word counts recorded at iteration 2
still hold: substantive exposition about 18,100 words, the three readings
together about 10,400.

Author proof: the study PDF was removed and rebuilt with `make doc`. It
settled with no LaTeX warning, overfull or underfull box, or undefined
reference, and every font is embedded Latin Modern. The research-edition PDF
has 37 pages, SHA-256
`e7c90080f6a14ba875742ebe822a86d3192027ae36c9a43a404d1ae1e1968285`, the same
bytes as the build-artifacts build. A contact sheet of all 37 pages showed the
same layout. The component checker (artifacts phase, research edition), the
content check with all four `--require` flags, and all thirteen
content-preflight checks pass, including `provenance-matches-run`. The
canonical web conversion probe (Python Markdown 3.10.3, pandoc 3.11) also
passes. Its output differs from iteration 2's only in the revision timestamp.

Remaining limitations: unchanged from iteration 2 and the research record.

### Outstanding

Cold study review of the current bytes, then the re-derived concise study and
homily with their reviews, build, visual review, canonical web generation and
review, installation and publication gates.

## Derive-synthesis, iteration 1 (15 October 2026)

Re-entered after the cold study review returned PASS at its iteration 3 with
no blocking finding. The re-entry followed only the research seal moving on
`scripts/_tooling.py`, a chronology computation input changed by a
tool-registry commit outside this leaf; research iteration 3 and author-study
iteration 3 edited no content. The packet forwarded no synthesis finding. The
stage ran as a Claude Code harness subagent, `claude-opus-5-5[1m]`, dispatched
at reasoning effort `high`.

All 16 inputs sealed by the concise review at its iteration 0 were re-hashed
and are unchanged, as are the 21 inputs of the study review at its iteration
3. No concise component, manifest entry, research record, study component or
generation record was edited, so the revision timestamp
`2026-10-15T16:27:39Z` and the contribution history stand. The substantive
concise argument still counts about 6,750 words with `detex` (overview 267,
Themes and Movement 1,571, commentary 4,913).

Author proof: the concise PDF was removed and rebuilt with `make doc`. It
settled with no LaTeX warning, overfull or underfull box, or undefined
reference; 10 contents lines on distinct anchors; every font embedded Latin
Modern. It has 12 physical pages, SHA-256
`3e066c1b2ec5d240dfcf7a1b18a5421373b1da067b61ffdc57a1178bda0fd541`, the same
bytes as the build-artifacts build; the auxiliary file is unchanged
(`00c088503b8c419acd594f57901c37684856880c72c00b03508ac4d578967293`). The
settled markers place the inventory, overview and all four sense rows on page
1, chronology on page 2, themes on pages 3 to 4 and commentary from page 5. A
contact sheet of all twelve pages and pages 1 and 12 at full size showed the
same layout. The component checker (artifacts phase, synthesis edition), the
content and artifacts checks with all four `--require` flags, the twelve
content-preflight checks, `provenance-matches-run` and the generation-metadata
check pass.

Remaining limitations: unchanged from iteration 0, the concise review's
advisories SYN-001 to SYN-005, and the build-artifacts record.

### Outstanding

Cold concise review of the current bytes, then the homily and its review,
build, visual review, canonical web generation and review, installation and
publication gates.

## Derive-homily, iteration 2 (15 October 2026)

Re-entered after the cold concise review returned PASS at its iteration 1 with
no blocking finding. The re-entry followed only the research seal moving on
`scripts/_tooling.py`, a chronology computation input changed by a
tool-registry commit outside this leaf; research iteration 3, author-study
iteration 3 and derive-synthesis iteration 1 edited no content. The packet
forwarded no homily finding and no advisory. The stage ran as a Claude Code
harness subagent, `claude-opus-5-5[1m]`, dispatched at reasoning effort
`high`.

All 10 inputs sealed by the homily review at its iteration 1 were re-hashed
and are unchanged, as are the 16 inputs of the concise review at its iteration
1, the 21 of the study review at its iteration 3, and the 1,813 files and 13
chronology computation inputs of the research review at its iteration 3. The
spoken body, terminal note, entrypoint, manifest, research records and
generation record were not edited, so the revision timestamp
`2026-10-15T16:27:39Z` and the contribution history stand. The argument, its
decisive turn (the fellow servant's plea repeated in the servant's own words,
Mt 18:26, 29) and the verification recorded at iteration 1 are unchanged. The
spoken body still counts 1,442 words by the same method, 11.1 to 12.0 minutes
at 120 to 130 words a minute by arithmetic only; nobody has spoken or timed
it. The review's advisories HOM-006 and HOM-007 were not forwarded and stand
as the review left them.

Author proof: the homily PDF was removed and rebuilt with `make doc`. It has 3
physical pages and the same bytes as the reviewed and build-artifacts builds
(PDF `88631112fc3a7c8dfb38fac0d9cb561a4d4487958fcb15593845d9102ebd0b44`,
auxiliary file
`96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486`). Its log
carries no LaTeX or package warning, overfull or underfull box, undefined
reference or rerun request; `pdffonts` lists Latin Modern Roman and Mono only,
all embedded Type 1 subsets. The three pages were read at 80 dpi and show the
same layout. The content check for the homily, research and synthesis editions
with `--date 2026-10-18` and all four `--require` flags, every homily
content-preflight check with `provenance-matches-run`, the component checker
(artifacts phase) for all three editions, the generation-metadata check for
the leaf and the homily PDF, and the canonical web conversion probe of the
study (Python Markdown 3.10.3, pandoc 3.11) pass.

### Upstream observations reported for the homily's cold reviewer

- None new. STU-012 on `research/interpretations.md` § 4.1 and the missing
  passage record for the 1861 English of the Introit, Offertory and Communion
  still stand.

### Outstanding

Cold homily review of the current bytes, then build, visual review, canonical
web generation and review, installation and publication gates.

## Build-artifacts, iteration 1 (15 October 2026)

Re-entered after the artifact gates at their iteration 0 found the research
review seal stale. The only sealed input that had moved was
`scripts/_tooling.py`, a chronology computation input, changed by a
tool-registry commit outside this leaf. Since then research iteration 3,
author-study iteration 3, derive-synthesis iteration 1 and derive-homily
iteration 2 edited no content, and the research, study, concise and homily
reviews each returned PASS again with no blocking finding. The stage ran as a
Claude Code harness subagent, `claude-opus-5-5[1m]`, dispatched at reasoning
effort `high`. No source file of the leaf was edited and no layout repair was
needed, so the generation record, its revision timestamp
`2026-10-15T16:27:39Z` and the content seals stand as the reviews left them.

### Builds

Each build PDF was removed and the document rebuilt with
`make doc DOC=<id> PROVIDER=claude`. All three reproduced the bytes of the
iteration 0 build, and the auxiliary files are unchanged.

| Output | Physical pages | PDF SHA-256 |
| --- | --- | --- |
| `61-twenty-first-after-pentecost` (study) | 37 | `e7c90080f6a14ba875742ebe822a86d3192027ae36c9a43a404d1ae1e1968285` |
| `61-twenty-first-after-pentecost-synthesis` (concise) | 12 | `3e066c1b2ec5d240dfcf7a1b18a5421373b1da067b61ffdc57a1178bda0fd541` |
| `61-twenty-first-after-pentecost-homily` | 3 | `88631112fc3a7c8dfb38fac0d9cb561a4d4487958fcb15593845d9102ebd0b44` |

Auxiliary files kept with the PDFs under `build/claude/`: study
`8d378f83288e07c1f0544da91013f7da39596b575bd5a4121c82567e9d2a2b49`, concise
`00c088503b8c419acd594f57901c37684856880c72c00b03508ac4d578967293`, homily
`96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486`.

### Checks

- Logs: no error, LaTeX or package warning, overfull or underfull box,
  undefined reference or rerun request in any of the three settled logs. The
  Makefile reported 67 contents lines for the study and 10 for the concise
  study, each on its own anchor; component manifest and generation metadata
  valid.
- Structure and fonts: letter paper, PDF 1.7, pdfTeX, not encrypted; titles
  and subjects set for all three. `pdffonts` lists Latin Modern Roman and
  Mono only (Type 1), every font embedded and subset.
- Extraction: `pdftotext -layout` gives 24,876 words (study), 9,384 (concise)
  and 2,356 (homily, body and note); no `??`, stray control sequence or
  replacement character.
- Concise physical pages from the settled auxiliary file: inventory, overview
  and all four sense markers on page 1; chronology on page 2; themes from page
  3 to page 4; commentary from page 5; 12 pages in all.
- `scripts/_proper_study.py check --phase artifacts` with `--date 2026-10-18`
  and the four `--require` flags: pass. `tools/check-proper-components
  --phase artifacts` for the research, synthesis and homily editions, and
  `tools/check-generation-metadata` for the leaf and the three PDFs: pass.
- Snapshot: `scripts/_proper_study.py snapshot` rewrote
  `research/artifacts.json` byte-identically (SHA-256
  `3300cda72ead03d57937c68205e5306ceb9384f80a074aff2e366b0c62b63d98`): the
  three PDFs, 27 render inputs, and the study and concise auxiliary files as
  pagination evidence. It records bytes, not a review.
- Rasters: `tools/tpt pdf-review` rendered all 52 pages with contact sheets
  into the run's iteration 1 raster directory. The builder looked at every
  contact sheet and at concise page 1 at full size. No clipping, overflow,
  collision or stray blank page was seen. This is a builder's check, not the
  independent visual review.

### Remaining limitations

- Unchanged from iteration 0: the page-2 orientation rows mix `Ps` and
  `Psalm` in their generated passage labels and use hyphens in verse ranges
  where the authored text uses en dashes; this is generator output, left for
  the visual reviewer to judge.
- The upstream observations already reported (STU-012 on
  `research/interpretations.md` § 4.1; no registered passage record for the
  1861 English of the Introit, Offertory and Communion) still stand.

### Outstanding

Visual review; canonical web generation and review; installation and
publication gates.

## Derive-synthesis, iteration 2 (15 October 2026)

Re-entered after the cold visual review returned one blocking finding against
the concise study, VIS-001: on page 2 the orientation rows inside each ruled
group of Scriptural Date and Location had no white space between them, so in
the psalm group a passage label and its date could be paired only by reading
another column. The review's advisories VIS-002 to VIS-005 came with it. The
stage ran as a Claude Code harness subagent, `claude-opus-5-5[1m]`, dispatched
at reasoning effort `high`.

### Repairs

- VIS-001: `sections/concise/03-date-location.tex` now places `\addlinespace`
  between every two consecutive orientation rows that no `\midrule` already
  divides: three in the psalm group, two in the Gospel group and one in the
  Epistle group. The generated rows, their order, the place phrases and the
  shared table type size are unchanged. The chronology still stands alone on
  physical page 2 with both of its markers there; the page keeps room below
  the closing note.
- VIS-004 (advisory): the descriptive line of the concise title block in
  `synthesis.tex` now begins with a capital, as the study's does.

VIS-002 and VIS-003 lie in the expansive study, which this stage does not own,
and VIS-005 in the shared chronology generator; none of them was touched.

The revision timestamp became `2026-10-15T17:54:00Z` and the derive-synthesis
contribution records this iteration. No argument, attribution or evidence
changed: the substantive concise argument still counts about 6,750 words with
`detex` (overview 267, Themes and Movement 1,571, commentary 4,913).

### Author proof

The concise study was built with `make doc`. It settled with no LaTeX or
package warning, overfull or underfull box, or undefined reference; 10
contents lines on distinct anchors; every font embedded Latin Modern. It has
12 physical pages, PDF SHA-256
`963401884390649cde76c9dd2346bdb0c32af3597ba71cc3c364c13717717deb`; the
auxiliary file is byte-identical to the reviewed one
(`00c088503b8c419acd594f57901c37684856880c72c00b03508ac4d578967293`), so the
settled markers still place the inventory, overview and all four sense rows on
page 1, chronology on page 2, themes on pages 3 to 4 and commentary from page
5. Page 2 was read at 200 dpi: each psalm row's passage label and date now
stand apart from the next row's, as do the Gospel and Epistle rows. A contact
sheet of all twelve pages and page 1 at full size showed no other change. The
component checker (artifacts phase, synthesis edition), the content check
with `--date 2026-10-18` and all four `--require` flags for the synthesis,
research and homily editions, the synthesis content-preflight checks,
`provenance-matches-run` for all three editions and the generation-metadata
check for the leaf and the concise PDF pass. The artifacts-phase content check
now reports that the built PDFs and render inputs differ from the snapshot
prepared for visual review; that snapshot belongs to the final build and is
expected to be retaken there.

### Outstanding

Cold concise review of the current bytes, then the dependent homily and
reviews, the final three-document build and snapshot, visual review,
canonical web generation and review, installation and publication gates.

## Derive-homily, iteration 3 (15 October 2026)

Re-entered after the cold concise review returned PASS at its iteration 2 on
the derive-synthesis iteration 2 repair of VIS-001, a layout-only change to the
page-2 Scriptural Date and Location table, with the capitalized descriptive
line of the concise title block. The packet forwarded no homily finding and no
advisory. The stage ran as a Claude Code harness subagent,
`claude-opus-5-5[1m]`, dispatched at reasoning effort `high`.

All 10 inputs sealed by the homily review at its iteration 2 were re-hashed
and are unchanged, as are the 16 inputs of the concise review at its iteration
2, the 21 of the study review at its iteration 3, and the 1,813 files and 13
chronology computation inputs of the research review at its iteration 3. The
concise repair touches no passage the homily draws on: it adds white space
between table rows and capitalizes one word of a title line, and changes no
argument, attribution or evidence. The spoken body, terminal note, entrypoint,
manifest, research records and generation record were therefore not edited by
this stage. The shared revision timestamp `2026-10-15T17:54:00Z` and the
contribution history stand as derive-synthesis iteration 2 left them. The
argument, its decisive turn (the fellow servant's plea repeated in the
servant's own words, Mt 18:26, 29) and the verification recorded at iteration 1
are unchanged. The spoken body still counts 1,442 words by the same method,
11.1 to 12.0 minutes at 120 to 130 words a minute by arithmetic only; nobody
has spoken or timed it. The review's advisories HOM-006 to HOM-008 were not
forwarded and stand as the review left them.

Author proof: the homily PDF was removed and rebuilt with `make doc`. It has 3
physical pages, PDF SHA-256
`2137ef1d58e1a99bcaf2e9d562067416dda2e95fade04541d3fe36b38fec6b16`; the
auxiliary file is byte-identical to the reviewed one
(`96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486`). The PDF
differs from the reviewed bytes
(`88631112fc3a7c8dfb38fac0d9cb561a4d4487958fcb15593845d9102ebd0b44`) only
through the shared generation record. A separate build with the previous
generation record reproduced the reviewed PDF exactly. Between the two builds
the extracted text differs only in the printed revision timestamp. Pages 1 and
2 rasterize identically, and page 3 differs only in that line, which was read
at 80 dpi. The log carries no LaTeX or package warning, overfull or underfull
box, undefined reference or rerun request; `pdffonts` lists Latin Modern Roman
and Mono only, all embedded Type 1 subsets. The content check for the homily,
research and synthesis editions with `--date 2026-10-18` and all four
`--require` flags, every homily content-preflight check, `provenance-matches-run`
for all three editions, the component checker (artifacts phase) for all three
editions, the generation-metadata check for the leaf and the homily PDF, and
the canonical web conversion probe of the study (Python Markdown 3.10.3) pass.

### Upstream observations reported for the homily's cold reviewer

- None new. STU-012 on `research/interpretations.md` § 4.1 and the missing
  passage record for the 1861 English of the Introit, Offertory and Communion
  still stand.

### Outstanding

Cold homily review of the current bytes, then the final three-document build
and snapshot, visual review, canonical web generation and review,
installation and publication gates.

## Build-artifacts, iteration 2 (15 October 2026)

Re-entered after the cold visual review raised VIS-001 against the concise
study's page-2 row spacing. Derive-synthesis iteration 2 repaired it with
`\addlinespace` between consecutive orientation rows and capitalized the
concise title block's descriptive line, setting the shared revision timestamp
to `2026-10-15T17:54:00Z`. The concise review at its iteration 2 and the
homily review at its iteration 3 then returned PASS. The new timestamp prints
in all three documents, so each was rebuilt and the snapshot retaken. The
stage ran as a Claude Code harness subagent, `claude-opus-5-5[1m]`, dispatched
at reasoning effort `high`. No source file of the leaf was edited and no
layout repair was needed, so the generation record and the content seals stand
as the reviews left them.

### Builds

Each build PDF was removed and the document rebuilt with
`make doc DOC=<id> PROVIDER=claude`.

| Output | Physical pages | PDF SHA-256 |
| --- | --- | --- |
| `61-twenty-first-after-pentecost` (study) | 37 | `b29d4ebd2c792148b552fdc4ef812f209fcd3fc215a7a45362105b29ccc223ca` |
| `61-twenty-first-after-pentecost-synthesis` (concise) | 12 | `963401884390649cde76c9dd2346bdb0c32af3597ba71cc3c364c13717717deb` |
| `61-twenty-first-after-pentecost-homily` | 3 | `2137ef1d58e1a99bcaf2e9d562067416dda2e95fade04541d3fe36b38fec6b16` |

The concise and homily PDFs reproduce the derive-synthesis iteration 2 and
derive-homily iteration 3 author proofs byte for byte. Against the iteration 1
build, the study's extracted text differs only in the printed revision
timestamp. The homily's also differs only there. The concise text differs in
that line, the capitalized title line and the column spacing of the page-2
table. The auxiliary files are unchanged: study
`8d378f83288e07c1f0544da91013f7da39596b575bd5a4121c82567e9d2a2b49`, concise
`00c088503b8c419acd594f57901c37684856880c72c00b03508ac4d578967293`, homily
`96da8bd61cc21463cd3eda0260cb058d26e765e456536a181a79f8efa1798486`.

### Checks

- Logs: no error, LaTeX or package warning, overfull or underfull box,
  undefined reference or rerun request in any of the three settled logs. The
  Makefile reported 67 contents lines for the study and 10 for the concise
  study, each on its own anchor. The component manifest and generation
  metadata are valid.
- Structure and fonts: letter paper, PDF 1.7, pdfTeX, not encrypted; titles
  and subjects set for all three. `pdffonts` lists Latin Modern Roman and
  Mono only (Type 1), every font embedded and subset.
- Extraction: `pdftotext -layout` gives 24,876 words (study), 9,384 (concise)
  and 2,356 (homily, body and note), with no `??`, stray control sequence or
  replacement character. Each prints `Last revised (UTC):
  2026-10-15T17:54:00Z`.
- Concise physical pages from the settled auxiliary file: inventory, overview
  and all four sense markers on page 1; chronology on page 2; themes from page
  3 to page 4; commentary from page 5; 12 pages in all.
- `scripts/_proper_study.py check --phase artifacts` with `--date 2026-10-18`
  and the four `--require` flags passes, as do `tools/check-proper-components
  --phase artifacts` for the research, synthesis and homily editions and
  `tools/check-generation-metadata` for the leaf and the three PDFs.
- Snapshot: `scripts/_proper_study.py snapshot` rewrote
  `research/artifacts.json` (SHA-256
  `83d7b8e5719467563220a99474820b9f8b232137042230ca9f072074f27d0c39`). Against
  the iteration 1 snapshot, the three PDF hashes changed, as did the render
  inputs `generation-metadata.tex`, `synthesis.tex` and
  `sections/concise/03-date-location.tex`. The two auxiliary hashes did not
  change. The file records bytes, not a review.
- Rasters: `tools/tpt pdf-review` rendered all 52 pages with contact sheets
  into the run's iteration 2 raster directory. The builder looked at every
  contact sheet and at concise page 2 at full size. On page 2 each orientation
  row now stands apart from the next, and the table ends well above the foot
  of the page. No clipping, overflow, collision or stray blank page was seen.
  This is a builder's check, not the independent visual review.

### Remaining limitations

- The visual review's advisories VIS-002 and VIS-003 (in the expansive study)
  and VIS-005 (in the shared chronology generator's passage labels and date
  breaks) were not forwarded to a stage that owns them and are unchanged.
- The upstream observations already reported (STU-012 on
  `research/interpretations.md` § 4.1; no registered passage record for the
  1861 English of the Introit, Offertory and Communion) still stand.

### Outstanding

Visual review; canonical web generation and review; installation and
publication gates.

## Reviews and gates recorded by the engine

These are the engine's own recorded results for run `a8bcc37ea3420a07`, as the
run holds them when installation begins. No acceptance is claimed beyond them;
the terminal publication gates have not yet run. Each result's SHA-256 is the
hash the engine recorded for that result, and each was re-hashed from the run
directory and matched. Worker stages and program preflights, all PASS, are not
repeated here.

| Stage, iteration | Result | Findings and observations | Result SHA-256 |
| --- | --- | --- | --- |
| research-review 0 | CHANGES_REQUIRED | blocking RES-001, RES-002; advisory RES-003 to RES-007; two observations | `68b8f76ac7e302f315403d1389fe872cf89176139434a06eaf0e9854384a4735` |
| research-review 1 | CHANGES_REQUIRED | blocking RES-008, RES-009; advisory RES-010, RES-011; two observations | `2ee319b403a171e8754253e88b09d7f46c8ae9dcfc65ad24ade07abc22ea48c7` |
| research-review 2 | PASS | advisory RES-012, RES-013 | `24f242eba0b439911ff4885668ff4bfdaa64d8e480c5a7c7a0dcc3f25c04bc69` |
| study-review 0 | CHANGES_REQUIRED | blocking STU-001; advisory STU-002 to STU-010; two observations | `0fd7d95480499ae85d468361508e15b2fab3e833ac3499ce929f59c82ebfc0fc` |
| study-review 1 | CHANGES_REQUIRED | blocking STU-011; advisory STU-007, STU-012; one observation | `6f47214013ca210b9198b686c8387a055d02b68ad8ff133b31d49cb0e57b96e9` |
| study-review 2 | PASS | advisory STU-005, STU-012 to STU-014; one observation | `83a68f80e7d30b92bf8781727f0bad04b1628d5645c092b682bbd1b82616ef55` |
| synthesis-review 0 | PASS | advisory SYN-001 to SYN-005 | `9cef1aed11c70ba150999999b83c509257341ef9dafa0b55bd9fb454e2e55690` |
| homily-review 0 | CHANGES_REQUIRED | blocking HOM-001; advisory HOM-002 to HOM-005 | `5af77a02475f4adab38d840d9499ec41c8961b4130d6ee56940ee7f6e1db86cd` |
| homily-review 1 | PASS | advisory HOM-006, HOM-007; one observation | `744c2e8ea70823006b50251b3e0d8f10e34c06cbaa1969f9d71c2118f83b08f4` |
| artifact-gates 0 | FAIL | STALE-RESEARCH-REVIEW, routed to research | `7938e62ce435340b532ec78f8ecec92817dd420196c33150e2562e794d425283` |
| research-review 3 | PASS | advisory RES-012 to RES-015; one observation | `afecbfb02c6dd65ad79f57f6c6a008c96ce18750da437d7d0b0088c35dde8f8f` |
| study-review 3 | PASS | advisory STU-005, STU-013, STU-014; accepted STU-015; one observation | `b2cfcf0a512c3d37a4b51df12f12b584401e050f117337df9278dd43e07dbb12` |
| synthesis-review 1 | PASS | advisory SYN-001 to SYN-006 | `b11d8dab67343909a689cf5b38f472ebb00528978f42acaec535aa29b1636db0` |
| homily-review 2 | PASS | advisory HOM-006 to HOM-008; one observation | `9857b8fb6cf8ae6991ae09e420838d7197f9f166734fdea6a69925db5a686432` |
| artifact-gates 1 | PASS | none | `8d6a7c139b783c8489d67a5012f7cc8e3099b15e615f90603c523961611646cd` |
| visual-review 0 | CHANGES_REQUIRED | blocking VIS-001; advisory VIS-002 to VIS-005; one observation | `c699feb2867db24fc632439a7b93fc407750c40f40e6740a62786212ee257fbf` |
| synthesis-review 2 | PASS | advisory SYN-001 to SYN-006; one observation | `7a5405d0788263eb032d80fb7a287a62c034a54fa0f4ce272b02b3b3f2599204` |
| homily-review 3 | PASS | advisory HOM-006 to HOM-008; one observation | `ff117ab120e91145693efa536803570bd7d3822eb89cdb09ce259ed5842462e4` |
| artifact-gates 2 | PASS | none | `7981c4f2602b3b78a96c2e69320a92b1c660b9f5343e34f6f357f208e80283b5` |
| visual-review 1 | PASS | advisory VIS-002, VIS-003, VIS-005; one observation | `e743adc8c7dd3c3bf02712378d56706ce202c9ad41865ece3e994c09de6d5590` |
| generate-web 0 | PASS | worker stage | `8026cdf87f3f5443361f5220219d8f1cc9e8feaf30b8f7800964db68043dc1cf` |
| web-review 0 | PASS | none; two observations | `ea5b344927dfe5432db84c2867911c92d066441fe85ed0a039623b93f1ddd78c` |

The stages after the last artifact build, in brief:

- **Artifact gates, iteration 2.** `_proper_study.py check --phase artifacts`
  with `--date 2026-10-18` and the four `--require` flags passed against the
  snapshot in `research/artifacts.json`.
- **Visual review, iteration 1.** Every page of the three sealed PDFs was
  inspected at full size: 37 pages of the study, 12 of the concise study and 3
  of the homily. VIS-001, the missing space between orientation rows on the
  concise page 2, is resolved, and so is the advisory VIS-004 on the concise
  title's descriptive line. VIS-002 (the closing quotation-mark order in the
  study), VIS-003 (the study appendix's unspaced orientation rows) and VIS-005
  (the generated chronology labels) stand as advisories. The observation
  points to the chronology generator's row ending as the place for a
  generator-level fix.
- **Generate-web, iteration 0.** The canonical study alone was converted under
  the pinned Markdown 3.10.3. `research/web-artifact.json` records the
  conversion at SHA-256
  `9681daa54a44cab5fb3e11f4128da27bbc7a284e4eaa04e31af2924ab771eb3f`.
- **Web review, iteration 0.** No finding. The reviewer reproduced the
  conversion byte for byte, compared it with the reviewed 37-page PDF and
  viewed it through the site layout at 1280px and 390px. The two observations
  are the site stylesheet's horizontal scrolling of wide prose tables at phone
  width, and the generated chronology labels, which belong to the chronology
  generator.

## Install-publication, iteration 0 — 15 October 2026

The worker is a Claude Code harness subagent running as `claude-opus-5-5[1m]`,
dispatched at reasoning effort `high`. No reviewed source, generation
timestamp or receipt was changed at this stage.

### Installed PDFs

The snapshot was confirmed current before anything was installed.
`_proper_study.py check --phase artifacts --require-presentation
--require-format --require-authority --require-orientation --date 2026-10-18`
exited 0, and all 32 hashes in `research/artifacts.json` (three PDFs, 27
render inputs and two pagination `.aux` files) matched the files on disk. The
three PDFs were then installed with the normal recipe, one at a time. Nothing
was suppressed: no `-o`, no `-t`, no timestamp change and no source edit.

```sh
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost-synthesis PROVIDER=claude
make install-doc DOC=liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost-homily PROVIDER=claude
```

Each run validated the generation metadata and copied the bytes. Nothing was
retypeset: the build PDFs and their `.aux` files keep the build-artifacts
iteration 2 times, and the three `.aux` files still hash to the values that
stage recorded. The build PDF and the installed PDF each hash to the value
that the build, the artifact gates and the visual review recorded:

| Output | Pages | Bytes | SHA-256 (build and installed) |
| --- | ---: | ---: | --- |
| `61-twenty-first-after-pentecost.pdf` | 37 | 543,809 | `b29d4ebd2c792148b552fdc4ef812f209fcd3fc215a7a45362105b29ccc223ca` |
| `61-twenty-first-after-pentecost-synthesis.pdf` | 12 | 444,323 | `963401884390649cde76c9dd2346bdb0c32af3597ba71cc3c364c13717717deb` |
| `61-twenty-first-after-pentecost-homily.pdf` | 3 | 263,272 | `2137ef1d58e1a99bcaf2e9d562067416dda2e95fade04541d3fe36b38fec6b16` |

No hash differs, so no artifact defect is reported and no review boundary is
reopened.

### Web edition, release records and wiring

The reviewed conversion
`build/web/claude/liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost.md`
was installed byte for byte at
`web/claude/liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost.md`:
148,073 bytes, SHA-256
`9681daa54a44cab5fb3e11f4128da27bbc7a284e4eaa04e31af2924ab771eb3f`, the value
`research/web-artifact.json` and the web review record. The installing worker
runs no git state change; the run's driver stages the file so the publication
gate can prove it is tracked. No synthesis or homily web edition exists; the
canonical study is the only web authority.

`make add-publication ID=<id> CATALOG=library/traditional-latin-mass.md
PROVIDER=claude STATUS=alpha` created one release record per PDF under
`release/publications/claude/liturgy/roman-rite/1962/propers/temporal/`. No
Claude record existed beforehand. Each has schema version 1, its own output
id, the 1962 catalog, status `alpha` and the standing authorization
`perpetual-public-repository-2026`.

In `library/traditional-latin-mass.md`, the Claude cell of the existing row 61
changed from `Planned` to Full PDF, Synthesis PDF, Homily PDF and Read. That is
the order of the schema-2 manifest's `canonical_label`, `synthesis_label` and
`homily_label`, followed by the canonical web page. The ChatGPT cell, every
other row and every other catalog page are untouched, and no companion row was
added. `release/public-alpha.json` names `gpt` as the primary provider, so the
one new canonical marker carries the provider prefix,
`claude:liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost`,
beside the ChatGPT edition's unprefixed marker for the same identity.

### Catalogue, release bindings and source inventory

`make document-catalogue` regenerated
`src/web/data/structure/documents/corpus.json`. Every change belongs to this
leaf. The existing work for this identity gains the Claude edition: the study,
the concise study and the homily under `also`, the web page, the three
contribution records the leaf's generation metadata declares, and this run's
`produced` identity. Documents moved from 209 to 210, issues from 259 to 262
and pages from 7,081 to 7,118; the Claude provider tally moved from 60 to 61
and `claude-opus-5-5[1m]` from 89 to 90 documents. The work count stays 151,
because the identity's work already existed.

After the catalogue was regenerated, `make check-release-bindings` reported
exactly this stage's three writes: the catalog page and the projection as
stale and the new web edition as unrecorded. The refresh followed the
repository's scoped rule: `make refresh-release-bindings ADOPT=1
ONLY="library/traditional-latin-mass.md
web/claude/liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost.md
src/web/data/structure/documents/corpus.json"` made five changes. It adopted
the web edition, re-recorded the catalog page and the projection, and rewrote
the rights table and its digest. `make check-release-bindings` then reported
no stale binding. Nothing outside those three paths was re-recorded.

No source record under `src/sources/` changed in this run, so the source
library's reader projection needed no regeneration.

`tools/tpt source-inventory refresh
src/sources/inventories/claude-publications-v1.toml --review
src/sources/inventories/claude-classification-review-v1.toml --audited-on
2026-10-15` added this publication (60 to 61) and its 35 source-bearing files
(1,751 to 1,786) to the Claude publication inventory. The leaf's
classification row was then replaced from its placeholder by an audit of the
bindings in `research/source-bindings.toml`, the witness register and
negative results in `research/scope.md`, the dated witnesses in
`research/context.md` and the declarations in `research/review-dependencies.toml`:

- scripture: the Clementine Vulgate and the Douay–Rheims with Haydock's notes;
- liturgical: the 1962 typical edition with its general rubrics, the 1861
  Cummiskey English and Lasance's *New Roman Missal* for the orations pro
  Fidei propagatione;
- patristic: Hilary, Athanasius (the Psalm expositions printed under his
  name), Chrysostom, Jerome, Augustine, Theodoret, Cassiodorus and Gregory, in
  the Migne volumes and the Nicene and Post-Nicene Fathers;
- scholastic: Aquinas, Bellarmine, Rabanus Maurus and the medieval
  commentators on the Mass: Honorius, Rupert, Sicard and Durandus;
- historical-primary: the Migne volumes and their facsimiles and the Aquinas
  printings;
- institutional-current: the dated FSSP and ICRSP ordos for 18 October 2026
  and the USCCB introductions to the Psalms, Job, Matthew and Ephesians that
  the chronology cites;
- secondary: Schuster, *The Liturgical Year*, and the *Catholic Encyclopedia*;
- finding-aid: the calendar and rubric computations `research/context.md`
  adopts as finding aids only, and the commentary and containment joins behind
  the lead dispositions;
- repository-internal: the facsimile-rights inventory, the Latin provenance
  ledger, the translations overlay, the Lasance rights record, the
  author-standing inventory and the chronology corpus, each declared in
  `research/review-dependencies.toml` or sealed by the chronology computation.

No canon-law, magisterial, classical, prayer-devotional, archival or dataset
source occurs in the leaf's records, so none of those categories was
assigned. The review's `audited_on` became 2026-10-15, and the tool's own
render function recomputed both of its snapshots; `tools/tpt source-inventory
classify` then applied the row and `check` reports the inventory valid. The
inventory records this file's hash, so the refresh and `classify` were run
again after this entry was written. The provider-neutral inventory is
unchanged.

### Publication-gate commands run by this stage

These are this stage's own runs of the terminal gate commands, in the pinned
Markdown 3.10.3 environment, before the driver stages or commits anything.
They are not an acceptance.

- `_proper_study.py check --phase publication --require-presentation
  --require-format --require-authority --require-orientation --date
  2026-10-18` refuses while the web edition is unstaged: git does not know
  `web/claude/liturgy/roman-rite/1962/propers/temporal/61-twenty-first-after-pentecost.md`.
  Run against a scratch copy of the index in which that one file was added,
  leaving the repository's own index unchanged, it exits 0. The gate's own run
  follows the driver's staging.
- `make check-release-bindings` reports no stale binding.
- `tools/tpt public-alpha check --provider claude --document <leaf>` exits 0:
  the scoped policy is valid for the three outputs, and the global source,
  release and authorization records are valid for 262 publications.
- `tools/tpt document-library check --provider claude --document <leaf>` and
  `tools/tpt document-library structure --check` exit 0, and the projection
  is current.
- `make check-publication-inventories` exits 0 for both publication
  inventories.
- `make check-web-editions-current` exits 0: tracked web editions match
  current sources.

### Outstanding

The driver's staging of the installed web edition and of this stage's tracked
writes; the terminal publication gates.
