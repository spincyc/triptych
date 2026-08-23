# Eighth Sunday after Pentecost — research scope

**Provider:** Anthropic Claude.
**Publication:** `liturgy/roman-rite/1962/propers/temporal/48-eighth-after-pentecost`
(Claude edition, `src/claude/…`).
**Profile:** `guidance/liturgy/roman-1962-propers.md` with `guidance/editorial.md`.
**Last updated:** 2026-07-25. All checks below were performed on 2026-07-25
unless another date is given.

This is an audit record, not a diary. It holds the search boundary, the source
roles, the reception matrix, the negative results, and the operational
qualifications deliberately kept out of the rendered guide. Verified appointed
text and its provenance are in `../propers/verified.md`; the unedited machine
pull is in `../propers/retrieved.txt`; per-claim source checks are in
`source-audit.md`; central source identities are bound in
`source-bindings.toml`.

## Independence

This is an independent Claude edition. From the gpt sibling only two files were
opened, each once and for a stated purpose: `research/scope.md`, for topic
parity, and `propers/verified.md`, solely to learn which witness carries this
formulary and at what pages. The gpt `main.tex` was never opened. Every Latin
form published here was re-verified by this edition at the facsimile; every
patristic and Doctoral witness was re-read at its own work and locus; the
English witness, the collation against the Clementine psalter, the temporal-cycle
observations, the notable-and-quotable gallery, and the interpretive proposals
were developed here and share no text with any sibling. A completed Claude
document (`src/claude/theology/mariology/lourdes/`) was read for repository voice
and record patterns only.

## Document identity and included/excluded scope

- **Formulary:** one, and only one — `DOMINICA OCTAVA post Pentecosten`,
  `II classis`, *Missale Romanum* editio typica 1962, printed pp. 387–388,
  marginal nos. 1512–1521.
- **Included:** the ten appointed elements; the two directions printed inside
  the formulary (`Credo`, `Præfatio de Ssma Trinitate`); the rank and its
  occurrence rule from the book's own `Rubricæ generales`; the formulary's place
  in the Sundays-after-Pentecost epistle sequence; the identical Introit at the
  Purification; the collation of every appointed scriptural form against the
  Clementine Vulgate; complete-context study of all seven appointed passages;
  patristic, medieval and Doctoral reception; documented cultural afterlives;
  bounded editorial proposals.
- **Excluded, deliberately:** calendar assembly and precedence beyond the rank
  rules the book itself prints (that is `guidance/liturgy/roman-1962-assembly.md`
  territory); the Ordinary and Canon; chant notation, modes, and the *Graduale*;
  the postconciliar Lectionary's treatment of Luke 16; any claim about present
  authorization to use the 1962 book; any sacramental appendix (no ritual Mass
  is involved).

## Witnesses and their roles

| Source | Role | State |
|---|---|---|
| CMAA facsimile of the 1962 Vatican typical edition, SHA-256 `648fdb8f…3518a` | **textual control** for every published Latin form | acquired; page images inspected; verified 2026-07-25 |
| Embedded machine text of the same facsimile, pp. 468–469 | locating aid only; never controls wording | retained unedited in `../propers/retrieved.txt` |
| *The Roman Missal translated into the English language for the use of the laity* (Cummiskey, 1861), IA `romanmissaltran00churgoog`, pp. 411–413 | **identified public-domain English witness** for every appointed text quoted in English | page images inspected; verified |
| The same translation in the 1843 Philadelphia printing, IA `romanmissaltran00englgoog`, pp. 411–413 | corroboration of the 1861 readings, and independent attestation of the `nimis`/`valde` split | OCR read; images not required |
| Clementine Vulgate and Douay–Rheims at drbo.org | canonical-context control and standard of comparison | inspected |
| New Advent patristic library (NPNF) | direct patristic exegesis in English | inspected at each cited locus |
| Corpus Thomisticum | Aquinas's Latin, and the checked Latin transmission of the *Catena aurea* | inspected at each cited locus |
| *Patrologia Latina* text at Corpus Corporum (mlat.uzh.ch) | the only accessible Latin for Ambrose, Jerome, Bede | inspected; **machine-read Migne, OCR risk recorded below** |
| Internet Archive scan `p2commentaryupon00cyriuoft` (Payne Smith's Cyril) | Cyril of Alexandria on this pericope | inspected |
| Project Gutenberg; UK Historic Hansard | documented later uses | inspected |

**Not used and not independent.** The Internet Archive Benziger item
(`MissaleRomanum1962RomanMissalColorLatin`) scans a different edition and was
not needed, because no reading in the controlling facsimile was unclear. Its
OCR and its images derive from one item and are not independent witnesses of
each other.

## Corpora and languages searched, with the boundary stated

- **Corpora:** New Advent's patristic library and Summa; the Christian Classics
  Ethereal Library's NPNF series; Documenta Catholica Omnia; the *Patrologia
  Latina* text at Corpus Corporum; Corpus Thomisticum (Pauline commentaries,
  *Summa*, *Catena aurea*); the Internet Archive; drbo.org; Project Gutenberg;
  UK Historic Hansard and the Parliament Hansard API.
- **Languages:** Latin (primary, for the missal, Ambrose, Jerome, Bede,
  Aquinas), English (NPNF and Payne Smith translations, and all later uses).
  Greek witnesses were reached through Latin or English translation, not read in
  Greek, except where a variant is expressly discussed.
- **Not used:** critical editions (CSEL, CCSL, Sources Chrétiennes, Leonine),
  the *Corpus Christianorum* apparatus, TLG, Migne image scans for collation of
  the OCR'd Latin, chant manuscripts, and any Latin psalter witness other than
  the Clementine. Every negative result below is bounded by exactly this list
  and is correctable.

## Passage-by-passage reception matrix

Seven distinct directly appointed passages, in Catholic canonical order.
"Direct" means exegesis of the appointed passage itself; "reuse" means the
passage is deployed to illuminate something else.

### 1. Ps 17 (18):28 and 32 — Offertory (no. 1518)

- **Direct ancient exegesis checked:** Augustine, *Enarr. in Ps.* 17.28 and
  17.32 (New Advent numbers it Ps. 18; its inline verse numbers run one lower
  than the Vulgate). Both retained. §28 identifies the humble as those who
  confess their sins and the proud through Rom 10:3; §32 identifies God as the
  inheritance the sons will possess after good service.
- **Use in the guide:** §32 is the pivot of the strongest documented link in the
  formulary, joining the Offertory to the Epistle's `heredes quidem Dei` and to
  Aquinas's `bonum autem principale quo Deus dives est, est ipsemet`.
- **Also searched, negative:** no direct patristic commentary on this verse pair
  was located outside the *Enarrationes* within the corpora above. The doublet at
  2 Kings (2 Samuel) 22 was checked in the Douay text and is reported as a
  textual observation, not as a source-critical judgment.

### 2. Ps 30 (31):3 — Gradual responsory (no. 1515)

- **Direct ancient exegesis checked:** Augustine, *Enarr. in Ps.* 30, Enarratio
  I, §§1 and 3 (New Advent: Ps. 31). Retained for the assignment of speech (the
  Mediator first, then the redeemed people) and for the gloss on `esto mihi in
  Deum protectorem`.
- **Material limitation recorded in the guide:** Augustine's lemma is `in domum
  refugii`, the Clementine reading, **not** the Gradual's `in locum refugii`. He
  is therefore reception of the psalm, not of the chant.
- **Negative result:** NPNF/New Advent carries only Enarratio I on this psalm.
  The three sermons of Enarratio II were not read in a checkable text and
  support no claim here.

### 3. Ps 33 (34):9 — Communion (no. 1520)

- **Direct ancient exegesis checked:** Augustine, *Enarr. in Ps.* 33, sermo 2,
  §§1 and 11 (New Advent: Ps. 34). Retained in full: the Eucharistic reading,
  Christ "carried in his own hands," John 6:52–53 as the psalm's foil, and "if
  you understand not, you are king Achis."
- **Structural caution recorded:** the New Advent page prints sermo 2 only and
  omits sermo 1, so its section numbers do not correspond to the Latin edition's.
  The guide cites by content and by New Advent's own numbering, and says so.
- **Title/narrative discrepancy:** checked directly in the Douay text of 1 Kings
  (1 Samuel) 21:10–15. Reported as a discrepancy, not harmonised.

### 4. Ps 47 (48):2 and 10–11 — Introit (no. 1512) and Alleluia (no. 1516)

- **Direct ancient exegesis checked:** Augustine, *Enarr. in Ps.* 47 §§2, 8, 9
  (New Advent: Ps. 48). §2 retained (Daniel 2:35, the mountain that came to us);
  §9 retained (universality as the answer to sectarian remnant claims).
- **Material negative result, published in the guide:** Augustine's lemma at
  v. 10 reads **`in medio populi tui`**, not `in medio templi tui`. His entire
  exegesis of that verse depends on the variant and does not transfer to the
  Introit as sung. The guide states this rather than quoting him as commentary
  on the antiphon, and retains only the section's closing John 1:12 sentence,
  which does not depend on the variant.
- **Unresolved:** the `nimis` / `valde` split, on which see below.

### 5. Ps 70 (71):1 — Gradual verse (no. 1515)

- **Direct ancient exegesis checked:** Augustine, *Enarr. in Ps.* 70, sermo 1,
  §§3 and 5 (New Advent: Ps. 71). Both retained.
- **Positive textual finding:** Augustine's lemma at v. 1 is `Deus, in te
  speravi; Domine, non confundar in aeternum` — the transposed form the missal's
  Gradual verse prints, against the Clementine `In te, Domine, speravi`. This is
  reported as a fact about Augustine's text, not as a claim about which Latin
  psalter the chant descends from.
- **Also retained:** §5 on v. 3, "God Himself has become the place of your
  fleeing unto, who at first was the fearful object of your fleeing from," which
  bears on the Gradual's borrowed `locum`.

### 6. Luke 16:1–9 — Gospel (no. 1517)

The largest search in this leaf, because the passage is genuinely disputed.

- **Direct exegesis checked and retained:** Ambrose, *Exp. in Lucam* VII.245;
  Jerome, *Ep.* 121 q. 6; Augustine, *Quaest. Evang.* II.34 and *Sermo* 113
  §§1–2; Bede, *In Lucam* V; Cyril of Alexandria, *Comm. in Lucam*, Sermon 108;
  and Gregory, *Moralia* XXI.19.29 (reuse, not commentary, and labelled as
  such). Aquinas: *Catena aurea in Lucam* c. 16 lect. 1–2 as the checked Latin
  transmission, plus *ST* II-II q. 32 a. 7 as his own resolution.
- **Chrysostom:** *Hom. in Heb.* I retained, and expressly labelled as
  illuminating reuse rather than commentary on the pericope.
- **Material negative results, all published in the guide's scope appendix:**
  (a) **Ambrose does not comment on the narrative of Luke 16:1–8 at all.** In the
  Migne text his chapter XVI treats vv. 13, 9 and 12, in that order, and passes
  over the parable's action. (b) **Gregory the Great has no homily on this
  pericope**; his Luke 16 homily (*Hom. in Ev.* 40) is on Dives and Lazarus.
  (c) **No connected Chrysostom exposition of Lk 16:1–9 was located** in the
  NPNF corpus. (d) **Jerome himself records a negative result** — he searched for
  Origen's and Didymus's explanations of the parable and found neither, and could
  not tell whether the works had perished or never existed.
- **Attribution held open:** the *Catena aurea*'s "Origenes" lemma
  (`abusive dictum est`) could not be verified against any extant Origen text in
  the corpora searched, and Jerome's negative result tells against it. The guide
  cites it as the *Catena*'s Origen and says why.
- **Attribution held open:** Theophilus of Antioch's allegory survives, so far as
  this search established, only inside Jerome's letter. Cited as Theophilus
  *apud Hieronymum*.
- **Cited at the level of transmission only:** Basil and Theophylact, whose own
  works were not opened; the guide says so at the reference.
- **Competing historical and exegetical judgments preserved, not harmonised:**
  five cruces are set out in the commentary — who commends; whether the fraud is
  censured (Ambrose against Augustine); what makes the mammon iniquitous (five
  answers, four of which Aquinas stacks); who receives into the eternal dwellings
  (Ambrose/Augustine/Gregory against Chrysostom's grammatical argument, with
  Jerome's restriction against Augustine's indiscriminate counsel); and whether
  the hearer or the money fails (Cyril's `when it has failed` against Augustine's
  `cum deficere coeperitis`).
- **Textual variant reported without adjudication:** the Greek behind `cum
  defeceritis` varies between a third-person singular and a second-person plural
  verb. Payne Smith's own note at Cyril, Sermon 108, discusses the Syriac
  diacritic and reports the Peshitta and Philoxenian readings. The guide reports
  the divergence and expressly declines to adjudicate the Greek text, because no
  Greek critical apparatus was consulted.

### 7. Romans 8:12–17 — Epistle (no. 1514)

- **Direct exegesis checked and retained:** John Chrysostom, *Hom. in Rom.* XIV
  (which opens on 8:12–13, so the whole appointed lection falls inside it);
  Augustine, *De spiritu et littera* 32.56 on 8:15; Aquinas, *Super Rom.* c. 8
  lect. 2 (vv. 12–13) and lect. 3 (vv. 14–17); Aquinas, *ST* III q. 23 aa. 1–4
  on adoption.
- **Corrected division recorded:** Corpus Thomisticum divides Romans 8 so that
  vv. 12–13 close lectio 2 and vv. 14–17 form lectio 3. The guide cites
  accordingly rather than assuming a single lectio.
- **Citation-form limitation:** Corpus Thomisticum prints Busa index numbers,
  not Marietti paragraph numbers, for the Pauline commentaries. The guide
  therefore cites by chapter and lectio only, and claims no Marietti number.
- **Not verified, therefore not used:** Ambrosiaster's *Commentarius in
  epistulam ad Romanos* was located only as an image-only Migne PDF without a
  text layer. No claim in the guide rests on it.
- **Documented chain retained:** the "how can one inherit from a Father who never
  dies" question runs from *Super Rom.* c. 8 l. 3 to *ST* III q. 23 a. 1 ad 3,
  where Aquinas names the Gloss on Rom 8 as his source. The guide reports the
  Gloss as Aquinas's own attribution; the Gloss itself was not opened.

## Textual collation: what was compared, and what was found

Every appointed scriptural form was collated word by word against the
Clementine Vulgate at drbo.org. Ten divergences were found; all are printed in
the guide's collation table and recorded in `../propers/verified.md`. None was
resolved in favour of either witness and none was emended.

**Unresolved question, expressly left open.** Psalm 47:2 appears twice in this
one formulary, `laudábilis nimis` in the Introit's psalm verse and `laudábilis
valde` in the Alleluia verse, both under the printed reference `Ps. 47, 2`. The
Clementine reads `nimis`. The 1843 and 1861 hand missals print the same split,
so it is transmitted rather than a 1962 setting error. Assigning the two forms to
named Latin psalters (Gallican, Roman, or another) would require collation
against psalter witnesses that this study did not undertake, and is therefore not
claimed. This is a discoverable omission left for later research.

## Operational qualifications displaced from the rendered guide

- **OCR risk on the Latin Fathers.** The Ambrose, Jerome and Bede Latin was read
  in the machine-read *Patrologia Latina* text at Corpus Corporum, whose own
  front matter warns of recognition errors. Visible errors were observed in the
  Ambrose file (`illlecebris` for `illecebris`; `tentabat` where the *Catena*'s
  clean text reads `tentat`). Consequently: where a Latin sentence from Ambrose,
  Gregory, Basil, Theophylact or Chrysostom is quoted in the guide, the form
  printed is the *Catena aurea*'s clean Corpus Thomisticum text, and the
  underlying work and locus are named separately. The two sentences quoted from
  the Migne text directly (Ambrose's `Nec reprehenditur villicus…` and Jerome's
  `quod adversus Dominum quidem fraudulenter…` and `non quoslibet pauperes…`)
  showed no OCR damage at the words quoted, but have not been collated against a
  critical edition or an image scan. A reader relying on the exact orthography
  should consult CSEL/CCSL.
- **Migne section numbering.** Ambrose's §245 and Gregory's XXI.19.29 are
  Migne's numbers; CSEL 32/4 and CCSL may number differently.
- **Bede variant not relied on.** The Migne text of Bede reads `si laudari
  potuit ille a domino **cui** fraudem faciebat`, where Augustine's text and the
  *Catena* read `**qui**`. The variant would sharpen the sense considerably. It
  is not used in the guide and no claim rests on it.
- **New Advent numbering of the *Enarrationes*.** New Advent numbers Augustine's
  expositions by the Hebrew psalm number (18, 31, 34, 48, 71 for Vulgate 17, 30,
  33, 47, 70) and its inline verse citations run one lower than the Vulgate. Every
  citation in the guide states the Vulgate number and flags the offset.
- **Web currentness.** drbo.org, New Advent, Corpus Thomisticum, Corpus Corporum,
  Project Gutenberg and Hansard are mutable web witnesses read on 2026-07-25.
  Only the controlling facsimile is pinned by hash.

## Rejected and unresolved leads

- **The identical Introit at the Purification** was verified in the 1962 book by
  image (no. 2107, printed p. 467) before being used. Retained.
- **The Fourth Sunday's Rom 8:18–23** was verified by image of the printed
  heading at p. 382 before being used. Retained.
- **A tract at *Comm. Sanct. pro aliquibus locis*** (no. 5911) uses Ps 47:10–12
  with `sic et laus tua`, against the Introit's `ita`. Noted during the search;
  not published, because it belongs to a different formulary and adds nothing the
  Clementine collation does not already establish.
- **Ambrosiaster on Romans 8** — image-only witness; unresolved; unused.
- **Chrysostom, *Homiliae IX de poenitentia*** — not text-mined; whether it
  treats this parable is open; unused.
- **A liturgical-historical explanation of the pericope boundary at Rom 8:17** —
  no sourced account of why the lection stops mid-verse was located within the
  corpora searched. The guide therefore reports the boundary as a fact and
  expressly declines to explain it, and interpretive proposal 5 names this gap as
  its own disconfirming condition.

## Notable-and-quotable audit

Five entries retained. Method: a full-text sweep of a large Project Gutenberg
corpus of nineteenth-century English prose for every appointed phrase and its
Authorised-Version equivalents, plus queries against UK Historic Hansard and the
Parliament Hansard API. Every quotation below was read at the cited primary text
or official record on 2026-07-25.

| # | Appointed text | Later use and locus | Relationship | Wording check | Cultural payoff | Limiting qualification |
|---|---|---|---|---|---|---|
| 1 | Lk 16:9 | Trollope, *The Way We Live Now* (1875), ch. LXXXI | echo; exact AV wording, unattributed | read in PG ebook 5231 | Christ's counsel as a swindler's only article of contrition | Trollope does not name the parable; the reader must supply it |
| 2 | Lk 16:8–9 | HC Deb 3 Feb 1931, vol. 247, cc. 1662–1664 | documented; the parable named three times | read in Historic Hansard | eschatological `tabernacula` demoted to a ministry's tenure; the pericope's central crux raised as a four-word interjection | political speech, not exegesis; Young's reading is improvised |
| 3 | Lk 16:3, 16:6–7 | Kingsley, *Westward Ho!* (1855), ch. XVIII | documented; "hundred measures… write fifty" | read in PG ebook 1860 | two verses turned against two clerical castes in consecutive speeches | polemical fiction; the anti-Catholic charge is Kingsley's, reported not endorsed |
| 4 | Lk 16:1–9 | Trollope, *Barchester Towers* (1857), ch. XXXIX | documented; "the unjust steward" named | read in PG ebook 3409 | exact congruence of office, total incongruity of scale | comic aside; Trollope draws no conclusion |
| 5 | Lk 16:1–2 | Ruskin, *Sesame and Lilies* (1865), lecture I | documented; "the unjust stewards of all men's ideas" | read in PG ebook 1293 | the parable migrates into ideology-critique; the steward is not a person | Ruskin's use is metaphorical and does not engage the parable's difficulty |

**Rights and translation status.** All four literary items are public domain (US)
and were read in Project Gutenberg texts. The Hansard item is Parliamentary
copyright, quoted under the Open Parliament Licence. Every English biblical
phrase in every item is Authorised Version wording, not Douay and not the
missal's Latin; the guide states this at the head of the gallery, because the
phrases that entered English are a Protestant rendering of the verses this Mass
appoints.

**Material negative results.**

- **Abraham Lincoln quoting "the children of this world are wiser in their
  generation" — not verified; rejected.** The phrase, and "children of light,"
  "mammon," "steward" and "unjust steward," return zero hits in the seven-volume
  *Papers and Writings of Abraham Lincoln* (PG 2653–2659), in *Speeches and
  Letters of Abraham Lincoln* (PG 21267), and in the volumes of Basler's
  *Collected Works* obtainable in full text. Several Basler volumes are
  lending-restricted and the Michigan searchable edition returned HTTP 403, so
  this is a bounded failure to verify, not a refutation. Not used.
- **"To dig I am not able; to beg I am ashamed" as a general English proverb —
  not established.** Swept across the whole corpus: no occurrence in Chaucer,
  Shakespeare, Dickens, Trollope, Thackeray or Melville. The only genuine
  literary occurrence located is Kingsley's, which is why entry 3 carries it.
- **"Give an account of thy stewardship" in Trollope's *The Warden* —
  refuted.** The phrase is not in Trollope's text (PG 619); it appears only in a
  1910 abridgement, i.e. an abridger's interpolation.
- **`Non confundar in aeternum` in a secular or ironic setting — not found** in
  the corpus or in Hansard; all located uses are liturgical or musicological.
- **"Taste and see" used commercially — no verifiable instance found.**
- **Romans 8:17 "joint heirs" — rejected.** Every corpus hit for
  "co-heir/joint-heir" is the ordinary Roman-law property sense; the dependence
  runs the other way, since Paul borrowed the legal term.
- **"Abba" — rejected.** Corpus hits are proper names (Abba Thule in Melville;
  Abba Salama in Gibbon). The Swedish pop group's name is an acronym of its
  members' initials and no evidence displaces that; it is not offered.
- **Denise Levertov, "O Taste and See" (1964) — strong lead, not verified to
  standard, not used.** The poem does redirect Ps 33:9 and attributes the phrase
  to a subway Bible poster, but it could not be read in a primary or reliable
  edition (the Poetry Foundation URL 404s; the Internet Archive copies are
  lending-restricted), and it is in copyright. Recorded as an unresolved lead.
- **"Stewardship" in modern corporate-governance and environmental usage —
  rejected.** "Steward" is native Old English (*stigweard*), so the bare noun
  cannot be shown to depend on Luke 16. Only the full formula "give an account of
  one's stewardship" is demonstrably Lucan, and the cleanest verified instance
  found is a Speaker's aside in the Commons (28 June 2004), which is an echo and
  too thin for the gallery.
- **Further verified items not used, to keep the gallery varied:** Michael Foot
  MP asking the Prime Minister to circulate the parable of the unjust steward to
  her Cabinet (HC Deb 5 May 1987, PMQs); Michael Alison MP citing "the mammon of
  unrighteousness" as warrant for the Church Commissioners' investment portfolio
  (HC Deb 10 July 1995); Thackeray, *Vanity Fair* ch. XLI (Becky Sharp);
  Dickens, *Our Mutual Friend* I.10; Scott, *Redgauntlet* ch. X. All were read
  and would qualify; five entries is the profile's ceiling and two Hansard items
  would have narrowed the gallery's range.

## Interpretive-proposal audit

Six proposals, all in `The Propers: Interpretive Possibilities` and nowhere
else. For each: the named anchors, the connecting mechanism, the targeted
precedent search actually run, its result, and the controlling limit. Novelty
results are bounded by the corpora listed above and are correctable; no claim is
made that any connection is universally unknown.

| # | Anchors | Mechanism | Targeted precedent search | Result | Controlling limit |
|---|---|---|---|---|---|
| 1 | Int. `suscépimus` + Gosp. `redde rationem villicationis tuae` | the same speech act (acknowledgement of receipt) at both ends of one Mass; the assembly concedes the parable's premise before hearing it | searched the checked corpus for any witness joining the Introit to the Gospel of this Sunday, and for any patristic linkage of `suscipere` with `reddere rationem` | **not located in the checked corpus** | no verbal dependence; the Introit is probably chosen for its temple imagery, which the Purification's shared use makes likely |
| 2 | Int. (identical at the Purification, no. 2107) + Postcomm. `reparátio mentis et córporis` | the antiphon that on 2 February has a body carried into a temple here has none, until the Postcommunion asks for bodily effect after a body is received | searched for any source connecting the shared Introit across the two formularies, and for any patristic reading of `in medio templi tui` as the communicant's body | **not located in the checked corpus** | 1 Cor 6:19 is not appointed in this Mass; and the simpler explanation of the shared antiphon — a well-known chant fitting any mercy-and-sanctuary Mass — is probably true |
| 3 | Gosp. `fodere non valeo, mendicare erubesco` + Off. `populum humilem… oculos superborum` | the steward's two refusals are the two ways down; the next chant sorts the world by exactly that criterion; his fault is located in pride rather than dishonesty | searched Augustine on both Ps 17:28 and Lk 16, and the *Catena* on v. 3, for any witness reading the two refusals as a refusal of humility | **near analogue located**: Bede eschatologises the two excuses (digging as this life's work; begging as the foolish virgins' shame), but does not connect them to Ps 17:28 | Augustine reads `populum humilem` morally (those who confess their sins), not socially, which weakens the mapping of `fodere` onto poverty; the digging half is an editorial extension |
| 4 | Gosp. `accipe cautionem tuam… scribe` + the printed `Credo` | both are instruments executed in one's own hand or voice; neither can be performed by proxy | searched for any source treating the Creed's placement after this Gospel as significant | **not located in the checked corpus** | `Credo` is prescribed on all Sundays by general rubric, not chosen for this formulary; the proposal cannot explain why it is not equally significant elsewhere, and is marked in the guide as the section's weakest anchor |
| 5 | Ep. ending at `coheredes autem Christi` + Comm. `gustate et videte` | the Mass twice offers something deliberately partial: an inheritance without its printed condition, and a mode of knowing that reports presence without extent | searched for any sourced account of why the lection stops inside Rom 8:17, and for any witness joining the pericope boundary to the Communion antiphon | **not located in the checked corpus**; and the search turned up the disconfirming fact used in the guide | the same book appoints Rom 8:18–23 on the Fourth Sunday, so nothing is withheld from the liturgical year; if the division is inherited for reasons of length or station the proposal collapses. Stated in the guide as the disconfirming condition |
| 6 | Grad. (Ps 30:3 responsory + Ps 70:1 verse, two near-duplicate psalms) + Ep. `Abba (Pater)`, one address in two languages | both are the same rhetorical figure — one thing said twice; the Epistle's doubling is explained by Augustine and Aquinas as two peoples in one cry, and the proposal reads the Gradual's unexplained doubling by that light | searched Augustine's and Aquinas's treatments of Rom 8:15 and the checked expositions of Pss 30 and 70 for any witness connecting the two figures, and for any account of why the Gradual pairs two overlapping psalms | **not located in the checked corpus** | the parallel is formal only: the Epistle's doubling is across two *languages*, which is what carries the patristic argument, while the Gradual's two psalms are both Latin and its doubling is more plausibly the ordinary responsory-plus-verse practice |

## Review state

Generation provenance and source audit are recorded. No independent specialist,
theological, canonical, or ecclesiastical review has occurred and none is
claimed. Outstanding review items: the psalter attribution of the
`nimis`/`valde` split; collation of the Ambrose, Jerome and Bede Latin against a
critical edition; the Ambrosiaster witness; the *Catena*'s "Origen"; a sourced
account of the Rom 8:17 pericope boundary.

## Research-staleness verdict — 2026-07-26

Modified and independent-rewrite candidates were compared claim by claim
against the exact Missal and paired-provider inputs. No material correction was
found; the study edition may be exactly rebaselined. Full-text candidates were
outside this review.
