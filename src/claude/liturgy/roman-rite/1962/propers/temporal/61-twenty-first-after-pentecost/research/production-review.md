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
